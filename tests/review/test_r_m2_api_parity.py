"""Independent R-M2-API parity and incompatibility witness.

Read-only review harness: uses exact A and B source copied from their pinned SHAs.
Fixtures are defined here independently of both implementation test suites.
No actual European system or real-data qualification is claimed.
"""
from dataclasses import replace
from hashlib import sha256

import numpy as np
import pytest

from tyndp_reduce.iosn_official.contracts import (
    Provenance, ACBranch as ABranch, HVDCTerminals as AHVDC,
    DetailedGridSnapshot as AGrid, TimeSet as ATime,
    ReferenceDispatchSet as ADispatch, NormalContingencyRatings as ARatings,
    DataContractError, RejectedComponent as ARejected,
)
from tyndp_reduce.iosn_official.country import CountryZoneBudget as ABudget
from tyndp_reduce.iosn_official.physical import reference_flows as a_flows
from tyndp_reduce.iosn_official.screen import screen_annual_overload as a_screen
from tyndp_reduce.iosn_official.seed import quota_seed as a_seed
from tyndp_reduce.iosn_official.operators import build_oriented_projection as a_projection

from tyndp_reduce.m2.contracts import (
    Evidence, Bus, ACBranch as BBranch, HVDCTerminalPair as BHVDC,
    DetailedGridSnapshot as BGrid, TimePoint, TimeSet as BTime,
    HVDCDispatch, PSTDispatch, ReferenceDispatchSet as BDispatch,
    NormalContingencyRatings as BRatings, CountryZoneBudget as BBudget,
    ContractError,
)
from tyndp_reduce.m2.physical import SparseACReference
from tyndp_reduce.m2.screening import screen_annual_overload as b_screen
from tyndp_reduce.m2.country import country_quota_busmap as b_seed
from tyndp_reduce.m2.projection import build_oriented_projection as b_projection


YEARS = tuple(f"REVIEW-Y{i+1}" for i in range(5))
STAMP = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
KEYS = tuple(f"T{i}" for i in range(5))
T = len(YEARS)


def ae(s):
    return Provenance("independent-"+s, "synthetic://r-m2-api/"+s,
                      "review-v1", sha256(s.encode()).hexdigest(), True)


def be(s):
    return Evidence("synthetic:r-m2-api/"+s, "review-v1",
                    sha256(s.encode()).hexdigest(), "2040")


def atime():
    return ATime(STAMP, YEARS, YEARS, np.ones(T),
                 ("winter",)*T, ae("time"))


def btime(fixture=True):
    points = tuple(TimePoint(KEYS[i], STAMP[i].replace("Z", "+00:00"),
                             YEARS[i], "winter", 1.) for i in range(T))
    return BTime(be("time"), YEARS, points, fixture=fixture)


def bf(cache):
    return np.asarray(cache.payload()["ac_flows_MW"], dtype=float)


def bmatrix(arr):
    return tuple(tuple(float(x) for x in row) for row in np.asarray(arr))


def independent_dense(branches, buses, injection, phase=None, base_mva=100.):
    """Stand-alone small dense oriented lossless DC oracle, NOT either API."""
    n, m = len(buses), len(branches)
    position = {k:i for i,k in enumerate(buses)}
    A = np.zeros((n,m))
    b = np.empty(m)
    for e,(name,u,v,x) in enumerate(branches):
        A[position[u],e] = 1.
        A[position[v],e] = -1.
        b[e] = base_mva/x
    phases = np.zeros((m, injection.shape[1])) if phase is None else phase
    L = (A*b)@A.T
    theta = np.zeros_like(injection, dtype=float)
    theta[1:] = np.linalg.solve(L[1:,1:],
                                (injection + A@(b[:,None]*phases))[1:])
    return b[:,None]*(A.T@theta-phases)


def test_independent_triangle_pst_dense_vs_A_vs_B():
    buses = ("a","b","c")
    branch_data = (("ab","a","b",.1),("bc","b","c",.2),
                   ("ca","c","a",.3))
    av = tuple(ABranch(*v,225,"pst" if v[0]=="ca" else "line")
               for v in branch_data)
    bv = tuple(BBranch(*v,225,"pst" if v[0]=="ca" else "line")
               for v in branch_data)
    ag = AGrid(buses,("DE",)*3,av,(),100.,ae("triangle"))
    bg = BGrid(be("triangle"),100.,tuple(Bus(x,"Germany",225) for x in buses),
               bv,ties_110kv_complete=True,fixture=True)
    p = np.tile(np.array([20.,-10.,-10.])[:,None],(1,T))
    phases = np.array([0.,.07,-.03,.2,-.1])
    ac = a_flows(ag,ADispatch(buses,STAMP,p,{},{"ca":phases},ae("disp")),atime())
    bc = SparseACReference(bg).solve(
        BDispatch(be("disp"),buses,KEYS,bmatrix(p),
                  pst=(PSTDispatch("ca",tuple(phases)),)),btime())
    phase_matrix = np.zeros((3,T))
    phase_matrix[2] = phases
    dense = independent_dense(branch_data,buses,p,phase_matrix)
    np.testing.assert_allclose(ac.flow_mw,bc and bf(bc),atol=1e-10,rtol=0.)
    np.testing.assert_allclose(ac.flow_mw,dense,atol=1e-10,rtol=0.)
    print("INDEPENDENT_TRIANGLE_PST: A=B=dense, max_abs_MW=",
          float(np.max(np.abs(ac.flow_mw-dense))))


def island():
    buses = ("a","b","c","d","e")
    bd = (("ab","a","b",.2),("bc","b","c",.1),
          ("de","d","e",.2))
    ab = tuple(ABranch(*v,225) for v in bd)
    bb = tuple(BBranch(*v,225) for v in bd)
    ag = AGrid(buses,("DE",)*3+("FR",)*2,ab,
               (AHVDC("dc","c","d"),),100.,ae("islands"))
    bg = BGrid(be("islands"),100.,
               tuple(Bus(x,"Germany" if i<3 else "France",225)
                     for i,x in enumerate(buses)),bb,(BHVDC("dc","c","d"),),
               ties_110kv_complete=True,fixture=True)
    p = np.tile(np.array([20.,-10.,0.,5.,-15.])[:,None],(1,T))
    ad = ADispatch(buses,STAMP,p,{"dc":np.full(T,10.)},{},ae("islands-d"))
    bdsp = BDispatch(be("islands-d"),buses,KEYS,bmatrix(p),
                     hvdc=(HVDCDispatch("dc",(-10.,)*T,(10.,)*T),))
    return ag,bg,ad,bdsp


def test_independent_islands_hvdc_dense_vs_A_vs_B():
    ag,bg,ad,bd = island()
    a = a_flows(ag,ad,atime())
    b = SparseACReference(bg)
    out = b.solve(bd,btime())
    expected = np.tile(np.array([20.,10.,15.])[:,None],(1,T))
    np.testing.assert_allclose(a.flow_mw,expected,atol=1e-10)
    np.testing.assert_allclose(bf(out),expected,atol=1e-10)
    assert len(set(a.island_of_bus)) == len(b.islands) == 2
    assert np.max(np.abs(a.nodal_net_mw.sum(axis=0))) < 1e-12
    print("INDEPENDENT_TWO_ISLAND_HVDC: A=B, expected [20,10,15] MW")


def test_independent_three_country_quota_projection_equivalence():
    buses = ("de0","de1","fr0","ni0")
    labels = ("Germany","Germany","France","Northern Ireland")
    raw = ("DE","DE","FR","NI")
    data = (("e0","de0","de1",.1),("e1","de1","fr0",.2),
            ("e2","fr0","ni0",.25))
    ag = AGrid(buses,raw,tuple(ABranch(*v,225) for v in data),
               (),100.,ae("three-country"))
    bg = BGrid(be("three-country"),100.,
               tuple(Bus(name,country,225) for name,country in zip(buses,labels)),
               tuple(BBranch(*v,225) for v in data),
               ties_110kv_complete=True,fixture=True)
    p = np.tile(np.array([10.,0.,-5.,-5.])[:,None],(1,T))
    ac = a_flows(ag,ADispatch(buses,STAMP,p,{},{},ae("p3")),atime())
    physical = SparseACReference(bg)
    bc = physical.solve(BDispatch(be("p3"),buses,KEYS,bmatrix(p)),btime())
    qa = ABudget.synthetic({"Germany":1,"France":1,"Northern Ireland":1})
    qb = BBudget(be("q3"),(("Germany",1),("France",1),("Northern Ireland",1)))
    za = a_seed(ag,labels,qa,merge_cost_by_branch={x[0]:0. for x in data})
    zb = b_seed(bg,qb,np.zeros(3))
    assert za.zone_of_bus[0] == za.zone_of_bus[1]
    assert zb[0] == zb[1]
    assert len(set(za.zone_of_bus)) == len(set(zb)) == 3
    pa = a_projection(ag,za.zone_of_bus)
    pb = b_projection(physical,qb,zb)
    pa.verify(ac)
    pa_z, fa_z = pa.aggregate(ac)
    pb_z, fb_z = pb.verify(physical,bc)
    np.testing.assert_allclose(sorted(np.abs(fa_z[:,0])),
                               sorted(np.abs(fb_z[:,0])),atol=1e-9)
    np.testing.assert_allclose(sorted(np.abs(fa_z[:,0])),[5.,10.],atol=1e-9)
    np.testing.assert_allclose(sorted(pa_z[:,0]),sorted(pb_z[:,0]),atol=1e-9)
    print("INDEPENDENT_THREE_COUNTRIES: cuts [5,10] MW, 3 exact zones")


def test_detect_380kv_screening_semantic_incompatibility():
    buses=("a","b","c")
    p=np.tile(np.array([20.,0.,-20.])[:,None],(1,T))
    ag=AGrid(buses,("DE",)*3,
             (ABranch("ab","a","b",.1,380,screening_class_kv=400),
              ABranch("bc","b","c",.1,400)),(),100.,ae("380"))
    bg=BGrid(be("380"),100.,tuple(Bus(x,"Germany",400) for x in buses),
             (BBranch("ab","a","b",.1,380),BBranch("bc","b","c",.1,400)),
             ties_110kv_complete=True,fixture=True)
    ac=a_flows(ag,ADispatch(buses,STAMP,p,{},{},ae("380d")),atime())
    bc=SparseACReference(bg).solve(BDispatch(be("380d"),buses,KEYS,bmatrix(p)),
                                  btime())
    ratings_a=ARatings(STAMP,{k:np.full(T,10.) for k in ("ab","bc")},
                       {k:np.full(T,30.) for k in ("ab","bc")},ae("380r"))
    ratings_b=BRatings(be("380r"),("ab","bc"),KEYS,
                       ((10.,)*T,(10.,)*T),contingency_MW=((30.,)*T,(30.,)*T))
    a=a_screen(ag,ac,atime(),ratings_a)
    b=b_screen(bg,btime(),ratings_b,bc)
    assert set(a.screened_line_ids)=={"ab","bc"}
    assert all({r["branch_id"] for r in year}=={"bc"} for year in b.values())
    print("KNOWN_INCOMPATIBILITY_SCREEN_380KV: A includes ab, B silently drops ab")


def test_detect_chronology_incompatibility():
    stamps=list(STAMP)
    stamps[0],stamps[1]=stamps[1],stamps[0]
    with pytest.raises(DataContractError):
        ATime(tuple(stamps),YEARS,YEARS,np.ones(T),("winter",)*T,ae("out-of-order"))
    points=tuple(TimePoint(KEYS[i],stamps[i].replace("Z","+00:00"),
                           YEARS[i],"winter",1.) for i in range(T))
    # Current B contract admits unsorted (but unique) UTC instants.
    result=BTime(be("out-of-order"),YEARS,points,fixture=True)
    assert result.points[0].timestamp > result.points[1].timestamp
    print("KNOWN_INCOMPATIBILITY_CHRONOLOGY: A rejects, B accepts")


def test_detect_nonfixture_observed_ac_flow_requirement():
    buses=("a","b")
    p=np.tile(np.array([10.,-10.])[:,None],(1,T))
    ag=AGrid(buses,("DE","DE"),(ABranch("ab","a","b",.1,225),),
             (),100.,ae("obs"))
    bg=BGrid(be("obs"),100.,(Bus("a","Germany",225),Bus("b","Germany",225)),
             (BBranch("ab","a","b",.1,225),),
             ties_110kv_complete=True,fixture=False)
    a=a_flows(ag,ADispatch(buses,STAMP,p,{},{},ae("obsd")),atime())
    np.testing.assert_allclose(a.flow_mw,10.,atol=1e-10)
    with pytest.raises(ContractError,match="observed AC flow witness missing"):
        SparseACReference(bg).solve(BDispatch(be("obsd"),buses,KEYS,bmatrix(p)),
                                    btime(fixture=False))
    print("KNOWN_INCOMPATIBILITY_OBSERVED_FLOW_GATE: B requires witness, A not")


def test_detect_lossy_hvdc_input_incompatibility():
    buses=("a","b","c","d")
    bg=BGrid(be("lossy"),100.,
             (Bus("a","Germany",225),Bus("b","Germany",225),
              Bus("c","France",225),Bus("d","France",225)),
             (BBranch("ab","a","b",.1,225),
              BBranch("cd","c","d",.1,225)),
             (BHVDC("hv","b","c"),),ties_110kv_complete=True,fixture=True)
    p=np.tile(np.array([10.,0.,-9.,0.])[:,None],(1,T))
    bc=SparseACReference(bg).solve(
        BDispatch(be("lossyd"),buses,KEYS,bmatrix(p),
                  hvdc=(HVDCDispatch("hv",(-10.,)*T,(9.,)*T),)),btime())
    np.testing.assert_allclose(bf(bc)[0],10.,atol=1e-9)
    with pytest.raises(ARejected,match="HVDC losses"):
        AHVDC("hv","b","c",lossless=False)
    print("KNOWN_INCOMPATIBILITY_LOSSY_HVDC: B signed terminals supported, A rejects")


def test_fixed_transformer_shift_not_representable_in_B():
    a=ABranch("tr","a","b",.1,225,kind="transformer",phase_shift_rad=.02)
    assert a.phase_shift_rad==.02
    with pytest.raises(TypeError):
        BBranch("tr","a","b",.1,225,kind="transformer",phase_shift_rad=.02)
    print("KNOWN_INCOMPATIBILITY_FIXED_SHIFT: A contract supports, B contract lacks")


def test_both_fail_closed_on_island_imbalance():
    ag,bg,ad,bd=island()
    pi=ad.injections_mw.copy()
    pi.flags.writeable=True
    pi[0]+=1.
    with pytest.raises(DataContractError,match="unbalanced"):
        a_flows(ag,replace(ad,injections_mw=pi),atime())
    rows=np.asarray(bd.nodal_injections_MW).copy()
    rows[0]+=1.
    with pytest.raises(ContractError,match="island injection imbalance"):
        SparseACReference(bg).solve(replace(bd,nodal_injections_MW=bmatrix(rows)),btime())
    print("INDEPENDENT_NEGATIVE_ISLAND_IMBALANCE: A and B reject")
