"""Integrator-owned numerical and evidence tests, independent of review sources."""
from dataclasses import replace
from hashlib import sha256
from scipy.linalg import null_space
from scipy.sparse import issparse
from scipy.sparse import load_npz
import json
import numpy as np
import pytest

from tyndp_reduce.iosn_official.contracts import (
    ACBranch, HVDCTerminals, DetailedGridSnapshot, ReferenceDispatchSet,
    TimeSet, Provenance,
)
from tyndp_reduce.iosn_official.country import load_official_country_budget
from tyndp_reduce.iosn_official.physical import ac_topology, reference_flows
from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture
from tyndp_reduce.iosn_official.ma1 import execute_ma1


def source(key):
    return Provenance(key, "synthetic://rp1/physical/" + key, "1",
                      sha256(key.encode()).hexdigest(), synthetic=True)


def test_ten_bus_three_island_two_hvdc_two_pst_dense_kcl_cycle_oracle():
    names = ("a0","a1","a2","a3","a4","b0","b1","b2","c0","c1")
    branches = (
        ACBranch("a01","a0","a1",.12,400),
        ACBranch("a12","a1","a2",.20,400),
        ACBranch("a23","a2","a3",.08,225),
        ACBranch("a34","a3","a4",.11,225),
        ACBranch("a40","a4","a0",.15,400),
        ACBranch("a02","a0","a2",.30,225),
        ACBranch("apst","a1","a3",.22,400,kind="pst"),
        ACBranch("atr","a2","a4",.25,400,kind="transformer",
                 phase_shift_rad=.013),
        ACBranch("b01","b0","b1",.14,400),
        ACBranch("b12","b1","b2",.16,225),
        ACBranch("bpst","b2","b0",.20,400,kind="pst"),
        ACBranch("c01","c0","c1",.09,225),
    )
    grid = DetailedGridSnapshot(
        names, ("DE","DE","FR","DE","FR","FR","FR","FR","NI","NI"),
        branches, (HVDCTerminals("ab","a4","b1"),
                   HVDCTerminals("ca","c0","a0")), 123., source("grid"))
    years = tuple(f"W{i}" for i in range(5))
    times = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
    time = TimeSet(times, years, years, np.ones(5), ("winter",)*5, source("times"))
    base_net = np.array([20., -8., 4., -7., -9., 8., -5., -3., 2., -2.])
    net = base_net[:,None] * (1. + .1 * np.arange(5)[None,:])
    hvdc = {"ab":np.array([7.,8.,9.,10.,11.]),
            "ca":np.array([-3.,-4.,-5.,-6.,-7.])}
    terminal = np.zeros_like(net)
    for edge in grid.hvdc:
        terminal[names.index(edge.bus0)] -= hvdc[edge.identifier]
        terminal[names.index(edge.bus1)] += hvdc[edge.identifier]
    dispatch = ReferenceDispatchSet(
        names, times, net - terminal, hvdc,
        {"apst":np.array([.01,.02,-.01,.015,0.]),
         "bpst":np.array([-.02,.01,.03,-.015,0.])},
        source("dispatch"))
    incidence, _, island_ids, count = ac_topology(grid)
    assert issparse(incidence) and count == 3 and incidence.shape == (10,12)
    assert len(branches) - len(names) + count == 5
    out = reference_flows(grid, dispatch, time)
    a = np.zeros((len(names),len(branches)))
    for j,edge in enumerate(branches):
        a[names.index(edge.bus0),j] = 1
        a[names.index(edge.bus1),j] = -1
    cycles = null_space(a)
    assert cycles.shape == (12,5)
    x = np.array([b.x_pu for b in branches])/grid.base_mva
    operator = np.vstack((a, cycles.T @ np.diag(x)))
    for t in range(5):
        phase = np.array([
            dispatch.pst_phase_rad[e.identifier][t] if e.kind=="pst"
            else e.phase_shift_rad for e in branches
        ])
        rhs = np.r_[net[:,t], -cycles.T @ phase]
        dense, *_ = np.linalg.lstsq(operator, rhs, rcond=None)
        np.testing.assert_allclose(operator @ dense, rhs, atol=2e-9)
        np.testing.assert_allclose(out.flow_mw[:,t], dense, atol=2e-8)
        np.testing.assert_allclose(a @ out.flow_mw[:,t], net[:,t], atol=2e-9)
        for island in range(count):
            assert abs(np.sum(net[island_ids==island,t])) < 1e-10


def test_sparse_chain_1001_buses_with_actual_kcl():
    n = 1001
    bus = tuple(f"b{i}" for i in range(n))
    grid = DetailedGridSnapshot(
        bus, ("DE",)*n,
        tuple(ACBranch(f"l{i}",bus[i],bus[i+1],.08,400) for i in range(n-1)),
        (),100.,source("1001-grid"))
    ids = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
    years = tuple(f"Y{i}" for i in range(5))
    time = TimeSet(ids,years,years,np.ones(5),("winter",)*5,source("1001-time"))
    p = np.zeros((n,5)); p[0]=7.; p[-1]=-7.
    dispatch = ReferenceDispatchSet(bus,ids,p,{}, {},source("1001-disp"))
    a,_,_,islands=ac_topology(grid)
    assert islands == 1 and issparse(a) and a.nnz == 2000
    flow = reference_flows(grid,dispatch,time)
    np.testing.assert_allclose(flow.flow_mw,7.,atol=2e-8)
    np.testing.assert_allclose(a @ flow.flow_mw,p,atol=2e-8)


def test_sha_bound_synthetic_fixture_manifest_and_rating_contents(tmp_path):
    args=build_synthetic_fixture()
    result=execute_ma1(*args, protected_line_ids=("d12",))
    assert result.projection.verify(result.reference)
    manifest=result.export(tmp_path/"evidence",code_commit="CI_REAL_SHA_SET_BY_WORKFLOW")
    assert len(manifest["output_sha256"])==14
    assert len(manifest["ratings_content_sha256"])==64
    assert manifest["protected_line_ids"]==["d12"]
    assert len(manifest["budget_source_sha256"])==64
    assert manifest["budget_source_page_by_country"]=={}
    assert manifest["budget_page_evidence"]=="NOT_APPLICABLE_SYNTHETIC"
    assert manifest["real_network_qualified"] is False
    assert manifest["independent_reviewer_release"] is False
    for name,digest in manifest["output_sha256"].items():
        assert sha256((tmp_path/"evidence"/name).read_bytes()).hexdigest()==digest
    for name in ("P","Gamma","A_z","A_d"):
        assert load_npz(tmp_path/"evidence"/f"operator_{name}.npz").nnz>=0
    budget=load_official_country_budget()
    assert budget.source_pages["United Kingdom"]==27
    assert budget.source_pages["Switzerland"]==27
    assert budget.source_pages["Germany"]==26


def test_bounded_search_does_not_misstate_proof_for_17_nodes():
    from tyndp_reduce.iosn_official.country import CountryZoneBudget
    from tyndp_reduce.iosn_official.seed import quota_seed,QuotaFeasibilityError
    from types import SimpleNamespace
    names=tuple(f"v{i}" for i in range(17))
    edges=tuple(ACBranch(f"e{i}",names[i],names[i+1],.1,225)
                for i in range(16))
    g=SimpleNamespace(bus_ids=names,active_branches=edges,
                      incomplete_110kv_ties=False)
    with pytest.raises(QuotaFeasibilityError) as exc:
        quota_seed(g,("X",)*17,CountryZoneBudget.synthetic({"X":1}),
                   merge_cost_by_branch={e.identifier:1. for e in edges},
                   protected_line_ids=tuple(e.identifier for e in edges))
    assert exc.value.status == "HEURISTIC_STUCK"
