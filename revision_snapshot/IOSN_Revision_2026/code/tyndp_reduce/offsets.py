"""Reference-dependent, technology-resolved structural null-balance flows."""
import numpy as np


def structure_correction(detailed,agg,Rref,components):
    """components: dictionary technology -> signed nodal time-series (N,T).

    Exact decomposition against Rref on same full physical grid.
    This is NOT automatically the fitted constant reduced-network F0.
    """
    Rref=np.asarray(Rref,float)
    if not np.allclose(agg.P@Rref,np.eye(Rref.shape[1])):
        raise ValueError("P Rref must be identity")
    H=detailed.ptdf()
    parts={};total=None
    for key,p in components.items():
        p=np.asarray(p,float)
        if p.ndim!=2 or p.shape[0]!=detailed.n:raise ValueError(f"Bad carrier shape: {key}")
        intrazonal=p-Rref@(agg.P@p)
        if not np.allclose(agg.P@intrazonal,0,atol=1e-8):raise AssertionError("Nonzero zonal residual")
        f=agg.Gamma@H@intrazonal
        if not np.allclose(agg.A_z@f,0,atol=1e-7):raise AssertionError("Correction violates zonal balance")
        parts[key]=np.asarray(f)
        total=f.copy() if total is None else total+f
    return parts,total


def split_reference(detailed,agg,Rref,p_detail):
    """Check f = H_ref p_z + F_struct for physically balanced p_detail."""
    p=np.asarray(p_detail,float)
    if not np.allclose(p.sum(axis=0),0,atol=1e-7):raise ValueError("Expected balanced nodal injections")
    H=detailed.ptdf();pdz=agg.P@p
    ref=agg.Gamma@H@Rref@pdz
    corr=agg.Gamma@H@(p-Rref@pdz)
    target=agg.Gamma@detailed.flows(p)
    if not np.allclose(ref+corr,target,atol=1e-7):raise AssertionError("Split not exact")
    return ref,corr,target
