"""R-M2-MA1-PHY: independent adversarial scientific witnesses (2026-11-11).

Authored on a separate review branch, not imported from W-PHY's test fixtures.
The dense cycle-space KCL/KVL reference is mathematically independent of the
implementation's sparse nodal-Laplacian factorisation.

Known defects are strict xfails: after a worker repair they turn XPASS and
force explicit re-review, rather than silently changing their meaning.
No tests exercise real-network approval.
"""
from dataclasses import replace
from hashlib import sha256
import numpy as np
import pytest
from scipy.linalg import null_space
from scipy.sparse import issparse

from tyndp_reduce.iosn_official.contracts import (
    ACBranch, HVDCTerminals, DetailedGridSnapshot, ReferenceDispatchSet,
    TimeSet, NormalContingencyRatings, Provenance,
    DataContractError, RejectedComponent,
)
from tyndp_reduce.iosn_official.physical import ac_topology, reference_flows
from tyndp_reduce.iosn_official.preflight import preflight


def prov(label):
    return Provenance(
        dataset_id="R-PHY-" + label,
        source_uri="synthetic://independent-r-phy/" + label,
        version="review-20261111",
        source_sha256=sha256(("R-PHY:" + label).encode()).hexdigest(),
        synthetic=True,
    )


def independent_case():
    """Three electrical islands, five cycles, two HVDC inter-island links,
    two PST controls, one fixed-angle transformer and mixed-country AC mesh."""
    names = ("a0", "a1", "a2", "a3", "a4",
             "b0", "b1", "b2", "c0", "c1")
    countries = ("DE", "DE", "FR", "DE", "FR",
                 "FR", "FR", "FR", "NI", "NI")
    branches = (
        ACBranch("a01", "a0", "a1", .12, 400),
        ACBranch("a12", "a1", "a2", .20, 400),
        ACBranch("a23", "a2", "a3", .08, 225),
        ACBranch("a30", "a3", "a0", .15, 400),
        ACBranch("apst", "a1", "a3", .22, 400, kind="pst"),
        ACBranch("atr", "a0", "a2", .30, 225,
                 kind="transformer", phase_shift_rad=.012),
        ACBranch("a34", "a3", "a4", .11, 225),
        ACBranch("a41", "a4", "a1", .25, 400),
        ACBranch("b01", "b0", "b1", .14, 400, kind="transformer"),
        ACBranch("b12", "b1", "b2", .16, 225),
        ACBranch("bpst", "b2", "b0", .20, 400, kind="pst"),
        ACBranch("c01", "c0", "c1", .09, 225),
    )
    grid = DetailedGridSnapshot(
        names, countries, branches,
        (HVDCTerminals("a_to_b", "a2", "b1"),
         HVDCTerminals("c_to_a", "c0", "a4")),
        123.0, prov("grid"),
    )
    snapshots = tuple(f"202{year}-01-01T00:00:00Z" for year in range(5))
    years = tuple(f"R-WY-{year}" for year in range(5))
    time = TimeSet(snapshots, years, years, np.ones(5),
                   ("winter", "summer", "winter", "summer", "winter"), prov("time"))
    target = np.array([35., -20., 7., -12., -10.,
                       10., -6., -4., 3., -3.])
    net = target[:, None] * (1 + .08 * np.arange(5)[None, :])
    hvdc = {"a_to_b": np.array([9., 10., 11., 12., 13.]),
            "c_to_a": np.array([-4., -5., -6., -7., -8.])}
    terminal = np.zeros_like(net)
    for link in grid.hvdc:
        i = names.index(link.bus0)
        j = names.index(link.bus1)
        terminal[i] -= hvdc[link.identifier]
        terminal[j] += hvdc[link.identifier]
    dispatch = ReferenceDispatchSet(
        grid.bus_ids, snapshots, net - terminal, hvdc,
        {"apst": np.array([.01, .02, -.01, .015, 0.]),
         "bpst": np.array([-.025, .008, .01, -.02, 0.])},
        prov("dispatch"),
    )
    ratings = NormalContingencyRatings(
        snapshots,
        {line.identifier: np.full(5, 1000.) for line in branches},
        {line.identifier: np.full(5, 1200.) for line in branches},
        prov("ratings"),
    )
    return grid, dispatch, time, ratings


def cycle_space_flow(grid, net_mw, phase_by_branch):
    """Independent solution using KCL plus cycle-space KVL, *not* Bbus solve.

    A f = p.  For any cycle vector c with A c=0, KVL demands
    c.T diag(x/Sbase) f = -c.T phi.
    Solve the overdetermined, consistent system directly via least squares.
    """
    n, l = len(grid.bus_ids), len(grid.active_branches)
    index = {name: j for j, name in enumerate(grid.bus_ids)}
    a = np.zeros((n, l), dtype=float)
    x = np.empty(l)
    for j, branch in enumerate(grid.active_branches):
        a[index[branch.bus0], j] = +1
        a[index[branch.bus1], j] = -1
        x[j] = branch.x_pu / grid.base_mva
    cycles = null_space(a)
    matrix = np.vstack((a, cycles.T @ np.diag(x)))
    target = np.r_[net_mw, -(cycles.T @ phase_by_branch)]
    solution = np.linalg.lstsq(matrix, target, rcond=None)[0]
    np.testing.assert_allclose(matrix @ solution, target, atol=2e-9)
    return solution


def test_multiloop_three_island_hvdc_pst_transformer_against_cycle_space_oracle():
    grid, dispatch, time, ratings = independent_case()
    A_sparse, susceptance, island_ids, n_islands = ac_topology(grid)
    assert n_islands == 3
    assert A_sparse.shape == (10, 12) and issparse(A_sparse)
    np.testing.assert_array_equal(island_ids, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2])
    assert np.all(susceptance > 0)
    ledger = preflight(grid, dispatch, time, ratings,
                       country_label_map={"DE": "Germany", "FR": "France",
                                          "NI": "Northern Ireland"})
    assert ledger.status == "PASS"
    assert len(ledger.ac_islands) == 3
    cache = reference_flows(grid, dispatch, time)
    np.testing.assert_allclose(A_sparse @ cache.flow_mw, cache.nodal_net_mw,
                               atol=2e-9)
    for t in range(5):
        phase = np.array([
            dispatch.pst_phase_rad[b.identifier][t] if b.kind == "pst"
            else b.phase_shift_rad for b in grid.active_branches
        ])
        expected = cycle_space_flow(
            grid, cache.nodal_net_mw[:, t], phase)
        np.testing.assert_allclose(cache.flow_mw[:, t], expected,
                                   rtol=1e-10, atol=2e-8)
        for island in range(n_islands):
            assert abs(cache.nodal_net_mw[island_ids == island, t].sum()) < 1e-10
    assert cache.flow_mw.flags.writeable is False
    with pytest.raises(ValueError):
        cache.flow_mw.setflags(write=True)


def test_reversing_pst_and_hvdc_orientation_preserves_physical_solution():
    grid, dispatch, time, _ = independent_case()
    original = reference_flows(grid, dispatch, time)
    branches = list(grid.ac_branches)
    j = next(i for i, b in enumerate(branches) if b.identifier == "apst")
    branches[j] = replace(branches[j], bus0="a3", bus1="a1")
    links = list(grid.hvdc)
    links[0] = replace(links[0], bus0="b1", bus1="a2")
    reversed_grid = replace(grid, ac_branches=tuple(branches), hvdc=tuple(links))
    reversed_dispatch = replace(
        dispatch,
        pst_phase_rad={"apst": -dispatch.pst_phase_rad["apst"],
                       "bpst": dispatch.pst_phase_rad["bpst"]},
        hvdc_transfer_mw={"a_to_b": -dispatch.hvdc_transfer_mw["a_to_b"],
                          "c_to_a": dispatch.hvdc_transfer_mw["c_to_a"]},
    )
    out = reference_flows(reversed_grid, reversed_dispatch, time)
    expectation = original.flow_mw.copy()
    expectation[j] *= -1
    np.testing.assert_allclose(out.flow_mw, expectation, atol=1e-8)
    np.testing.assert_allclose(out.nodal_net_mw, original.nodal_net_mw)


def test_island_imbalance_and_unsupported_equipment_rejected():
    grid, dispatch, time, ratings = independent_case()
    altered = {"a_to_b": dispatch.hvdc_transfer_mw["a_to_b"] + 1.,
               "c_to_a": dispatch.hvdc_transfer_mw["c_to_a"]}
    with pytest.raises(DataContractError, match="island"):
        reference_flows(grid, replace(dispatch, hvdc_transfer_mw=altered), time)
    with pytest.raises(DataContractError, match="PST"):
        reference_flows(grid, replace(dispatch, pst_phase_rad={"apst":
                        dispatch.pst_phase_rad["apst"]}), time)
    with pytest.raises(RejectedComponent):
        HVDCTerminals("lossy", "a0", "b0", lossless=False)
    with pytest.raises(RejectedComponent):
        ACBranch("svc", "a0", "a1", .1, 400, kind="SVC")
    with pytest.raises(RejectedComponent):
        reference_flows(replace(grid, unsupported_components=("SVC-X",)),
                        dispatch, time)
    rejected = preflight(replace(grid, incomplete_110kv_ties=True),
                         dispatch, time, ratings,
                         country_label_map={"DE": "Germany", "FR": "France",
                                            "NI": "Northern Ireland"})
    assert rejected.status == "BLOCKED_DATA"
    with pytest.raises(DataContractError):
        rejected.require_pass()
    with pytest.raises(DataContractError, match="MW"):
        replace(ratings, unit="MVA")


def test_utc_and_actual_numerical_content_change_reference_digest():
    grid, dispatch, time, ratings = independent_case()
    with pytest.raises(DataContractError, match="UTC-aware"):
        replace(time, snapshot_ids=tuple(t.removesuffix("Z") for t in time.snapshot_ids))
    with pytest.raises(DataContractError, match="chronological"):
        replace(time, snapshot_ids=tuple(reversed(time.snapshot_ids)),
                year_for_snapshot=tuple(reversed(time.year_for_snapshot)))
    with pytest.raises(DataContractError, match="ISO-8601"):
        replace(time, snapshot_ids=("not-a-timestamp",) + time.snapshot_ids[1:])
    baseline = reference_flows(grid, dispatch, time)
    adjusted = dispatch.injections_mw.copy()
    adjusted[0] += 1
    adjusted[1] -= 1
    revised = reference_flows(grid, replace(dispatch, injections_mw=adjusted), time)
    assert baseline.input_sha256 != revised.input_sha256
    assert np.any(np.abs(baseline.flow_mw - revised.flow_mw) > .01)
    blocked = preflight(grid, dispatch, time,
                        replace(ratings, snapshot_ids=tuple("x-" + s
                                              for s in ratings.snapshot_ids)),
                        country_label_map={"DE": "Germany", "FR": "France",
                                           "NI": "Northern Ireland"})
    assert blocked.status == "BLOCKED_DATA"


def test_sparse_scale_one_thousand_bus_chain_no_dense_ptdf_required():
    count = 1001
    buses = tuple(f"n{i}" for i in range(count))
    branches = tuple(ACBranch(f"l{i}", buses[i], buses[i+1], .08, 400)
                     for i in range(count - 1))
    grid = DetailedGridSnapshot(buses, ("DE",) * count, branches,
                                (), 100., prov("large-grid"))
    ids = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
    years = tuple(f"Y-{i}" for i in range(5))
    time = TimeSet(ids, years, years, np.ones(5), ("winter",) * 5,
                   prov("large-time"))
    p = np.zeros((count, 5))
    p[0] = +7
    p[-1] = -7
    dispatch = ReferenceDispatchSet(buses, ids, p, {}, {}, prov("large-dispatch"))
    a, _, labels, n_islands = ac_topology(grid)
    assert issparse(a) and a.nnz == 2 * (count - 1)
    assert n_islands == 1
    result = reference_flows(grid, dispatch, time)
    np.testing.assert_allclose(result.flow_mw, 7., atol=2e-8)
    np.testing.assert_allclose(a @ result.flow_mw, result.nodal_net_mw, atol=2e-8)


@pytest.mark.xfail(strict=True, reason="PHY-R01 P1: frozen grid retains mutable input list (TOCTOU)")
def test_known_repro_mutable_grid_branch_list_must_not_mutate_after_validation():
    grid, _, _, _ = independent_case()
    branches = list(grid.ac_branches)
    mutable_grid = replace(grid, ac_branches=branches)
    digest_at_validation = mutable_grid.fingerprint()
    branches.append(ACBranch("unexpected", "a0", "a1", .1, 400))
    # An immutable input contract must not change by mutating caller-owned lists.
    assert mutable_grid.fingerprint() == digest_at_validation


@pytest.mark.xfail(strict=True, reason="PHY-R02 P1: nonbool lossless='False' accepted")
def test_known_repro_lossless_string_flag_must_fail_closed():
    with pytest.raises((DataContractError, TypeError)):
        HVDCTerminals("bad", "a0", "a1", lossless="False")


@pytest.mark.xfail(strict=True, reason="PHY-R03 P1: nonbool in_service='False' accepted")
def test_known_repro_branch_service_status_string_must_fail_closed():
    with pytest.raises((DataContractError, TypeError)):
        ACBranch("bad", "a0", "a1", .1, 400, in_service="False")


@pytest.mark.xfail(strict=True, reason="PHY-R04 P1: atol_mw=infinity bypasses nodal KCL")
def test_known_repro_infinite_tolerance_must_not_bypass_island_kcl():
    buses = ("left", "right")
    grid = DetailedGridSnapshot(
        buses, ("DE", "DE"), (ACBranch("link", *buses, .1, 400),),
        (), 100., prov("tolerance-grid"))
    ids = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
    years = tuple(f"YEAR-{i}" for i in range(5))
    time = TimeSet(ids, years, years, np.ones(5), ("winter",) * 5,
                   prov("tolerance-time"))
    p = np.array([[20.] * 5, [-19.] * 5])
    dispatch = ReferenceDispatchSet(buses, ids, p, {}, {},
                                    prov("tolerance-dispatch"))
    with pytest.raises(DataContractError):
        reference_flows(grid, dispatch, time, atol_mw=float("inf"))
