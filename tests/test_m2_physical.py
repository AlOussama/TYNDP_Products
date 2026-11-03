"""W-PHY synthetic AC-island/PST/HVDC reference witnesses (not real-grid evidence)."""
from hashlib import sha256
import numpy as np
import pytest

from tyndp_reduce.m2.contracts import (
    Evidence, Bus, ACBranch, HVDCTerminalPair, DetailedGridSnapshot,
    TimePoint, TimeSet, HVDCDispatch, PSTDispatch, ReferenceDispatchSet,
    ContractError, RejectedComponent,
)
from tyndp_reduce.m2.physical import SparseACReference, ReferenceFlowCache


def ev(label="fixture"):
    return Evidence("synthetic:"+label, "v1", sha256(label.encode()).hexdigest(), "2040")


def yearset():
    return TimeSet(ev("times"), ("wyA", "wyB"),
                   (TimePoint("t0", "2020-01-01T00:00:00+00:00", "wyA", "summer", 2.0),
                    TimePoint("t1", "2021-01-01T00:00:00+00:00", "wyB", "winter", 3.0)),
                   fixture=True)


def island_case():
    grid = DetailedGridSnapshot(
        ev("grid"), 100.0,
        (Bus("a", "Germany", 220), Bus("b", "Germany", 220),
         Bus("c", "Germany", 225), Bus("d", "France", 400), Bus("e", "France", 400)),
        (ACBranch("ab", "a", "b", .2, 220, "transformer"),
         ACBranch("bc", "b", "c", .1, 225),
         ACBranch("de", "d", "e", .2, 400)),
        (HVDCTerminalPair("dc", "c", "d"),),
        ties_110kv_complete=True, fixture=True)
    dispatch = ReferenceDispatchSet(
        ev("dispatch"), ("a", "b", "c", "d", "e"), ("t0", "t1"),
        ((20., 20.), (-10., -10.), (0., 0.), (5., 5.), (-15., -15.)),
        hvdc=(HVDCDispatch("dc", (-10., -10.), (10., 10.)),),
        observed_ac_flows_MW=((20., 20.), (10., 10.), (15., 15.)))
    return grid, yearset(), dispatch


def test_two_ac_islands_hvdc_bridge_and_transformer():
    grid, times, dispatch = island_case()
    physical = SparseACReference(grid)
    assert len(physical.islands) == 2
    assert physical.grid.branches[0].kind == "transformer"
    cache = physical.solve(dispatch, times)
    flow = np.asarray(cache.payload()["ac_flows_MW"])
    np.testing.assert_allclose(flow, [[20.,20.], [10.,10.], [15.,15.]], atol=1e-9)
    p = np.asarray(cache.payload()["p_net_MW"])
    np.testing.assert_allclose(physical.incidence @ flow, p, atol=1e-8)
    assert all(np.max(np.abs(p[list(island)].sum(axis=0))) < 1e-8
               for island in physical.islands)


def test_independent_direct_dense_dc_oriented_equations():
    grid, times, dispatch = island_case()
    s = SparseACReference(grid)
    result = s.solve(dispatch, times).payload()
    P = np.asarray(result["p_net_MW"])
    A = s.incidence.toarray()
    b = s.susceptance_MW
    L = A @ np.diag(b) @ A.T
    theta = np.zeros(P.shape)
    for island in s.islands:
        if len(island) > 1:
            free = list(island[1:])
            theta[free] = np.linalg.solve(L[np.ix_(free, free)], P[free])
    np.testing.assert_allclose(np.diag(b) @ A.T @ theta,
                               result["ac_flows_MW"], atol=1e-10)


def test_no_country_slack_even_when_europe_total_balanced():
    grid, times, dispatch = island_case()
    broken = ReferenceDispatchSet(ev("broken"), dispatch.bus_order, dispatch.time_keys,
                                  ((20.,20.),(-20.,-20.),(0.,0.),(5.,5.),(-5.,-5.)),
                                  hvdc=dispatch.hvdc)
    with pytest.raises(ContractError, match="island injection imbalance"):
        SparseACReference(grid).solve(broken, times)


def test_operational_hvdc_sign_and_missing_trajectory_fail_closed():
    grid, times, dispatch = island_case()
    missing = ReferenceDispatchSet(ev("missing"), dispatch.bus_order,
                                   dispatch.time_keys, dispatch.nodal_injections_MW)
    with pytest.raises(ContractError, match="HVDC terminal trajectories"):
        SparseACReference(grid).solve(missing, times)
    invalid = ReferenceDispatchSet(
        ev("invalid"), dispatch.bus_order, dispatch.time_keys,
        dispatch.nodal_injections_MW,
        hvdc=(HVDCDispatch("dc", (-10.,-10.), (12.,12.)),))
    with pytest.raises(ContractError, match="HVDC losses"):
        SparseACReference(grid).solve(invalid, times)


def test_neutral_calibration_requires_explicit_rebalanced_dispatch():
    grid, times, dispatch = island_case()
    with pytest.raises(ContractError, match="island injection imbalance"):
        SparseACReference(grid).solve(dispatch, times, mode="neutral_calibration")


def test_pst_operational_vs_neutral_loop_flow():
    grid = DetailedGridSnapshot(
        ev("pst-grid"), 100.,
        tuple(Bus(x, "Germany", 225) for x in "abc"),
        (ACBranch("ab","a","b",.1,225),
         ACBranch("bc","b","c",.1,225),
         ACBranch("ca","c","a",.1,225,"pst")),
        ties_110kv_complete=True, fixture=True)
    q = ReferenceDispatchSet(
        ev("pst-q"), tuple("abc"), ("t0","t1"),
        ((0.,0.),(0.,0.),(0.,0.)),
        pst=(PSTDispatch("ca",(0.,.3)),))
    s = SparseACReference(grid)
    ops = np.asarray(s.solve(q,yearset()).payload()["ac_flows_MW"])
    neutral = np.asarray(s.solve(q,yearset(),mode="neutral_calibration")
                         .payload()["ac_flows_MW"])
    np.testing.assert_allclose(ops[:,0],0,atol=1e-10)
    np.testing.assert_allclose(ops[:,1],[-100,-100,-100],atol=1e-8)
    np.testing.assert_allclose(neutral,0,atol=1e-10)


def test_branch_orientation_reverse_sign():
    grid,times,d = island_case()
    reversed_branch = ACBranch("de", "e", "d", .2, 400)
    reverse_grid = DetailedGridSnapshot(
        ev("reverse"),grid.base_mva,grid.buses,
        grid.branches[:2]+(reversed_branch,),grid.hvdc,
        ties_110kv_complete=True, fixture=True)
    no_observed = ReferenceDispatchSet(d.evidence,d.bus_order,d.time_keys,
                                       d.nodal_injections_MW,hvdc=d.hvdc)
    f = np.asarray(SparseACReference(reverse_grid).solve(no_observed,times)
                   .payload()["ac_flows_MW"])
    np.testing.assert_allclose(f[2],[-15.,-15.])


def test_unsupported_transformer_tap_rejected_explicitly():
    with pytest.raises(RejectedComponent, match="REJECTED_COMPONENT"):
        ACBranch("bad","a","b",.2,400,"transformer",tap_ratio=1.1)
    with pytest.raises(RejectedComponent, match="REJECTED_COMPONENT"):
        ACBranch("bad","a","b",.2,400,kind="series_compensator")


def test_immutable_cache_sha256_and_write_once(tmp_path):
    grid,times,q=island_case()
    cache=SparseACReference(grid).solve(q,times)
    path=tmp_path/"frozen.json"
    cache.write_once(path)
    with pytest.raises(FileExistsError):
        cache.write_once(path)
    assert ReferenceFlowCache.from_file(path).sha256 == cache.sha256
    with pytest.raises(ContractError, match="hash mismatch"):
        ReferenceFlowCache(cache.canonical_json+" ",cache.sha256).payload()


def test_sparse_solver_large_chain_without_dense_ptdf():
    n=700
    grid=DetailedGridSnapshot(
        ev("chain"),100.,
        tuple(Bus(str(i),"Germany",225) for i in range(n)),
        tuple(ACBranch(f"l{i}",str(i),str(i+1),.2,225) for i in range(n-1)),
        ties_110kv_complete=True, fixture=True)
    s=SparseACReference(grid)
    assert s.laplacian.getformat() == "csc"
    p=np.zeros((n,2));p[0]=5;p[-1]=-5
    q=ReferenceDispatchSet(ev("chainq"),tuple(str(i) for i in range(n)),
                           ("t0","t1"),tuple(map(tuple,p)))
    out=np.asarray(s.solve(q,yearset()).payload()["ac_flows_MW"])
    np.testing.assert_allclose(out,5.,atol=1e-9)
