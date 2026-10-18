"""Research FBMC bridge for the TYNDP-style PyPSA reduction experiment.

This is NOT the Core CCR capacity calculation process, and NOT an official RAM.
It offers a transparent N-1 DC-PTDF polyhedron for static research examples.
All units of inputs are MW, and PTDFs and GSKs are dimensionless.

Notation:
    incidence A_d has +1 on the sending node of an oriented branch.
    H is nodal PTDF, mapping BALANCED nodal injections to line flows.
    P (market zones x buses) maps nodal injections to market net positions.
    G (buses x market zones) maps market NP *changes* to nodal changes.
    K (CNECs x lines) maps line flows to monitored N-1 line flows.
    Z = K @ H @ G and f0 = K @ (H @ p_ref + b) - Z @ NP_ref.
    Then:  Z @ NP <= Fmax - FRM - f0  (one row per oriented CNEC).

CNEC sign conventions: the signed (negative) counterpart is created in
``build_domain``, so provide only one orientation per physical CNEC.
"""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import linprog
from .security import bodf_from_ptdf


def market_partition(zone_of_bus):
    """Construct a zero-one market-bidding-zone partition from integer zone IDs."""
    z = np.asarray(zone_of_bus, dtype=int)
    if z.ndim != 1 or len(z) == 0 or (z < 0).any():
        raise ValueError('Nonempty nonnegative integer market-zone array required')
    if not np.array_equal(np.unique(z), np.arange(z.max()+1)):
        raise ValueError('Market zone IDs must be consecutive')
    P = np.zeros((z.max()+1, len(z)), dtype=float)
    P[z,np.arange(len(z))]=1.0
    return P


def validate_gsk(P, G, tol=1e-9):
    P=np.asarray(P,float);G=np.asarray(G,float)
    if P.ndim != 2 or G.shape != (P.shape[1],P.shape[0]):
        raise ValueError('P (Z,N), G (N,Z) dimension mismatch')
    if not np.all(np.isfinite(G)) or not np.allclose(P@G,np.eye(P.shape[0]),atol=tol):
        raise ValueError('GSK must satisfy P @ G == I (one MW in its own bidding zone)')
    return True


def gsk_uniform(P):
    P=np.asarray(P,float)
    if not np.all(np.isclose(P.sum(axis=0),1)) or not np.all((P==0)|(P==1)):
        raise ValueError('P must be a one-hot nodal partition')
    return (P/P.sum(axis=1)[:,None]).T


def gsk_from_positive_weights(P, weights):
    """Normalize nonnegative representative injection weights within each market zone.

    A zero-weight bidding zone falls back to uniform rather than dividing by zero.
    Such fixed weights approximate a GSK but need not match the *operational* GLSK.
    """
    P=np.asarray(P,float);w=np.asarray(weights,float)
    if w.shape!=(P.shape[1],) or not np.all(np.isfinite(w)) or (w<0).any():
        raise ValueError('Weights must be finite nonnegative vector of length N')
    out=np.zeros((P.shape[1], P.shape[0]))
    for z in range(P.shape[0]):
        ix=np.flatnonzero(P[z]); weight=w[ix]
        out[ix,z]=weight/weight.sum() if weight.sum()>0 else 1/len(ix)
    validate_gsk(P,out)
    return out


def cnec_operator(detailed, monitored, outages):
    """Build linear N-1 operator K, one *unsigned* monitored branch per row.

    monitored/outages are aligned sequences; outage=None means N-0.
    Islanding contingencies raise ValueError; neither BODF nor N-1 capacity
    validity may be silently inferred for them.
    """
    mon=list(monitored);outs=list(outages)
    if len(mon)!=len(outs) or not mon:
        raise ValueError('Aligned nonempty monitored/outages required')
    D, invalid = bodf_from_ptdf(detailed)
    K=np.zeros((len(mon), detailed.l))
    for r,(l,k) in enumerate(zip(mon,outs)):
        l=int(l)
        if not 0<=l<detailed.l: raise ValueError('monitored branch out of bounds')
        if k is None:
            K[r,l]=1
        else:
            k=int(k)
            if not 0<=k<detailed.l or k==l:raise ValueError('Bad N-1 CNEC pair')
            if k in invalid:raise ValueError('Islanding N-1 outage unsupported in DC BODF')
            K[r,l]=1
            K[r,k]+=D[l,k]
    return K


@dataclass(frozen=True)
class FlowBasedDomain:
    """Two-sided CNEC polyhedron in zonal NP coordinates (not regulatory RAM)."""
    zonal_ptdf: np.ndarray       # (C,Z) for one orientation of each CNEC
    f0: np.ndarray               # (C,) zero-market-position intercept
    f_ref: np.ndarray            # (C,) CNEC flow at nodal reference point
    np_ref: np.ndarray           # (Z,) zonal reference positions
    coefficient: np.ndarray      # (2*C,Z), rows +Z,-Z
    ram: np.ndarray              # (2*C,), right-hand sides
    raw_pos: np.ndarray
    raw_neg: np.ndarray
    labels: tuple[str, ...]

    def evaluate(self, np_z):
        np_z=np.asarray(np_z,float)
        if np_z.ndim != 1 or np_z.shape != (self.coefficient.shape[1],):
            raise ValueError('Expected a market-zone net position vector')
        if not np.isclose(np_z.sum(),0,atol=1e-8):
            raise ValueError('Total market net position must sum to zero')
        return self.coefficient@np_z-self.ram

    def feasible(self, np_z, tol=1e-8):
        return bool(np.max(self.evaluate(np_z))<=tol)


def build_domain(H, P, G, K, p_ref, fmax, frm, fixed_branch_flows=None,
                 labels=None, enforce_reference_security=False):
    """Make a transparent pre-adjustment research FB domain.

    Explicitly excludes regulatory AMR/minRAM, F_uaf, NRAO, IVAs, CVAs,
    long-term nominations and other operational steps. This is NOT JAO RAM.
    The frame is absolute NP (not NP deviations); zero-NP intercept is
    computed consistently from the same p_ref and G.
    """
    H=np.asarray(H,float); P=np.asarray(P,float);G=np.asarray(G,float)
    K=np.asarray(K,float); p_ref=np.asarray(p_ref,float)
    fmax=np.asarray(fmax,float);frm=np.asarray(frm,float)
    validate_gsk(P,G)
    C,L=K.shape
    if H.ndim!=2 or L!=H.shape[0] or P.shape[1]!=H.shape[1]:
        raise ValueError('H, P, K do not describe the same detailed grid')
    if p_ref.shape!=(H.shape[1],) or abs(p_ref.sum())>1e-7:
        raise ValueError('Reference nodal injections must be balanced')
    if fmax.shape!=(C,) or frm.shape!=(C,) or np.any(fmax<=0) or np.any(frm<0):
        raise ValueError('Fmax and FRM must be valid CNEC-length arrays')
    branch_offset=np.zeros(L) if fixed_branch_flows is None else np.asarray(fixed_branch_flows,float)
    if branch_offset.shape!=(L,):raise ValueError('Fixed detailed branch flows must be (L,)')
    Z=K@H@G
    np0=P@p_ref
    ref=K@(H@p_ref + branch_offset)
    zero=ref-Z@np0
    pos=fmax-frm-zero
    neg=fmax-frm+zero
    coeff=np.vstack([Z,-Z]);ram=np.r_[pos,neg]
    if labels is None: labels=tuple(f'CNEC_{i}' for i in range(C))
    if len(labels)!=C:raise ValueError('Labels must cover CNEC rows')
    domain=FlowBasedDomain(Z,zero,ref,np0,coeff,ram,pos,neg,
                           tuple(str(s)+' (+)' for s in labels)+tuple(str(s)+' (-)' for s in labels))
    if enforce_reference_security and not domain.feasible(np0):
        raise ValueError('Reference point is outside preliminary CNEC margins')
    return domain


def structural_offset(H,P,G,K,p_ref,fixed_branch_flows=None):
    """Calculate K H (I - G P) p_ref + K b, the *same* zero-NP intercept."""
    H=np.asarray(H,float);P=np.asarray(P,float);G=np.asarray(G,float)
    K=np.asarray(K,float);p=np.asarray(p_ref,float)
    b=np.zeros(H.shape[0]) if fixed_branch_flows is None else np.asarray(fixed_branch_flows,float)
    validate_gsk(P,G)
    return K@(H@(p-G@(P@p))+b)


def select_sensitive_cnecs(domain, threshold=0.05):
    """Pure research 5% zone-to-zone PTDF screening (NOT TSOs' complete CNEC process)."""
    if threshold<0:raise ValueError('threshold must be nonnegative')
    Z=domain.zonal_ptdf
    # Important: use differences of bidding-zone columns, NOT absolute
    # slack-dependent zone-to-slack coefficients.
    variation=np.ptp(Z,axis=1)
    return variation>=threshold


def bilateral_capacity(domain, exporter, importer, baseline=None):
    """Largest extra bilateral exchange t>=0 along NP0+t(e_exporter-e_importer).

    Other bidding zones are FIXED. This is just a 1D cross-section of the
    FB domain, not an independent bilateral NTC usable simultaneously.
    """
    z=domain.coefficient.shape[1]
    if exporter==importer or min(exporter,importer)<0 or max(exporter,importer)>=z:
        raise ValueError('Distinct, valid zone indices required')
    start=np.zeros(z) if baseline is None else np.asarray(baseline,float)
    if start.shape!=(z,) or not domain.feasible(start):
        raise ValueError('Baseline must be a feasible balanced market position')
    shift=np.zeros(z);shift[exporter]=1;shift[importer]=-1
    deriv=domain.coefficient@shift
    budget=domain.ram-domain.coefficient@start
    active=deriv>1e-10
    if not np.any(active):return float('inf')
    return float(max(0,np.min(budget[active]/deriv[active])))


def maximise_net_position(domain, zone, fixed=None):
    """LP for max zonal export with balance sum(NP)=0 and FB halfspaces.

    Without extra net-position or bidding limits this may be unbounded.
    """
    z=domain.coefficient.shape[1]
    if not 0<=zone<z:raise ValueError('Unknown bidding zone')
    c=np.zeros(z);c[zone]=-1
    ans=linprog(c,A_ub=domain.coefficient,b_ub=domain.ram,A_eq=np.ones((1,z)),b_eq=[0],
                bounds=[(None,None)]*z,method='highs')
    if not ans.success:raise RuntimeError('FB linear program was not solved: '+ans.message)
    return float(ans.x[zone]),ans.x
