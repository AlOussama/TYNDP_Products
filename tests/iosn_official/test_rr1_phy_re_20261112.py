"""RR1-R-PHY (2026-11-12): reviewer-owned ordinary-PASS adversarial replay.

The test inputs are independently constructed; no worker test module or original
strict-XFAIL tests are edited/imported. Scope: frozen RP1 repair source, synthetic
lossless DC, no real-network, regulator, MA2 or merge claim.
"""
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import json
import sys

import numpy as np
import pytest
from scipy.linalg import null_space
from scipy.sparse import issparse, load_npz

from tyndp_reduce.iosn_official.contracts import (
    ACBranch, HVDCTerminals, DetailedGridSnapshot, ReferenceDispatchSet,
    TimeSet, NormalContingencyRatings, Provenance, DataContractError,
    RejectedComponent,
)
from tyndp_reduce.iosn_official.physical import ac_topology, reference_flows
from tyndp_reduce.iosn_official.preflight import preflight
from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture
from tyndp_reduce.iosn_official.ma1 import execute_ma1

REPAIR_SHA = "fb201ef5f120f64696dea9aa99f77ece77546f9a"


def source(label):
    return Provenance(
        "RR1-PHY-" + label, "synthetic://rr1-phy/" + label, "rr1-20261112",
        sha256(("rr1-phy:" + label).encode()).hexdigest(), synthetic=True,
    )


def two_bus():
    ids = ("left", "right")
    grid = DetailedGridSnapshot(
        ids, ("DE", "DE"), (ACBranch("tie", "left", "right", .1, 400),),
        (), 100.0, source("two-bus-grid"),
    )
    snapshots = tuple(f"202{k}-01-01T00:00:00Z" for k in range(5))
    years = tuple(f"EXTERNAL-{k}" for k in range(5))
    time = TimeSet(snapshots, years, years, np.ones(5),
                   ("winter",) * 5, source("two-bus-time"))
    p = np.tile(np.array([20., -20.])[:, None], (1, 5))
    dispatch = ReferenceDispatchSet(ids, snapshots, p, {}, {}, source("two-bus-dispatch"))
    return grid, dispatch, time


# === Original four PHY-R01..04 failure-inducing classes, now ordinary PASS ===

def test_phy_r01_original_caller_mutation_is_not_topology_or_fingerprint_mutation():
    grid, dispatch, time = two_bus()
    caller_lines = list(grid.ac_branches)
    caller_bus = list(grid.bus_ids)
    caller_countries = list(grid.raw_country_ids)
    caller_dc = list(grid.hvdc)
    caller_unsupported = list(grid.unsupported_components)
    frozen = replace(grid, bus_ids=caller_bus, raw_country_ids=caller_countries,
                     ac_branches=caller_lines, hvdc=caller_dc,
                     unsupported_components=caller_unsupported)
    validated_hash = frozen.fingerprint()
    flow_hash = reference_flows(frozen, dispatch, time).input_sha256
    caller_lines.append(ACBranch("injected-after-validation", "left", "right", .01, 400))
    caller_bus.append("phantom")
    caller_countries.append("UK")
    caller_dc.append(HVDCTerminals("fake_dc", "left", "right"))
    caller_unsupported.append("SVC-attack")
    assert frozen.fingerprint() == validated_hash
    assert frozen.bus_ids == grid.bus_ids
    assert frozen.active_branches == grid.active_branches
    assert frozen.hvdc == ()
    assert reference_flows(frozen, dispatch, time).input_sha256 == flow_hash


def test_phy_r01_time_dispatch_ratings_and_cache_caller_lists_owned():
    grid, dispatch, time = two_bus()
    t0 = list(time.snapshot_ids)
    years = list(time.weather_year_ids)
    year_each = list(time.year_for_snapshot)
    seasons = list(time.season)
    frozen_time = replace(time, snapshot_ids=t0, weather_year_ids=years,
                          year_for_snapshot=year_each, season=seasons)
    for seq in (t0, years, year_each, seasons):
        seq.reverse()
    assert frozen_time.snapshot_ids == time.snapshot_ids
    assert frozen_time.weather_year_ids == time.weather_year_ids
    db, ds = list(dispatch.bus_ids), list(dispatch.snapshot_ids)
    frozen_dispatch = replace(dispatch, bus_ids=db, snapshot_ids=ds)
    db.clear()
    ds.clear()
    assert frozen_dispatch.bus_ids == grid.bus_ids
    assert frozen_dispatch.snapshot_ids == time.snapshot_ids
    ratings = NormalContingencyRatings(time.snapshot_ids,
                                      {"tie": np.ones(5) * 20},
                                      {"tie": np.ones(5) * 24}, source("ratings"))
    rs = list(ratings.snapshot_ids)
    frozen_ratings = replace(ratings, snapshot_ids=rs)
    rs.clear()
    assert frozen_ratings.snapshot_ids == ratings.snapshot_ids
    cache = reference_flows(grid, dispatch, time)
    cbr, cbu, cts, cis = (list(cache.branch_ids), list(cache.bus_ids),
                         list(cache.snapshot_ids), list(cache.island_of_bus))
    cache_copy = replace(cache, branch_ids=cbr, bus_ids=cbu,
                         snapshot_ids=cts, island_of_bus=cis)
    for seq in (cbr, cbu, cts, cis):
        seq.clear()
    assert cache_copy.to_manifest() == cache.to_manifest()


def test_phy_r01_numeric_array_input_cannot_mutate_after_validation():
    grid, dispatch, time = two_bus()
    incoming = np.tile(np.array([20., -20.])[:, None], (1, 5))
    owned = replace(dispatch, injections_mw=incoming)
    first = reference_flows(grid, owned, time).input_sha256
    incoming[0] += 1.
    assert reference_flows(grid, owned, time).input_sha256 == first
    with pytest.raises(ValueError):
        owned.injections_mw.setflags(write=True)


def test_phy_r02_original_lossless_string_false_rejected():
    with pytest.raises(DataContractError, match="bool"):
        HVDCTerminals("malformed", "left", "right", lossless="False")


@pytest.mark.parametrize("value", ["True", 0, 1, None, [], np.bool_(True), 0.0])
def test_phy_r02_adversarial_nonboolean_lossless_flags_fail_closed(value):
    with pytest.raises(DataContractError, match="bool"):
        HVDCTerminals("malformed", "left", "right", lossless=value)


def test_phy_r02_actual_false_is_explicitly_unsupported_loss_model():
    with pytest.raises(RejectedComponent, match="loss"):
        HVDCTerminals("lossy", "left", "right", lossless=False)


def test_phy_r03_original_in_service_string_false_rejected():
    with pytest.raises(DataContractError, match="bool"):
        ACBranch("malformed", "left", "right", .1, 400, in_service="False")


@pytest.mark.parametrize("value", ["True", 0, 1, None, [], np.bool_(False), 0.0])
def test_phy_r03_related_flags_require_actual_bool(value):
    with pytest.raises(DataContractError, match="bool"):
        ACBranch("bad", "left", "right", .1, 400, in_service=value)
    grid, _, _ = two_bus()
    with pytest.raises(DataContractError, match="bool"):
        replace(grid, incomplete_110kv_ties=value)
    with pytest.raises(DataContractError, match="bool"):
        replace(grid.provenance, synthetic=value)


def test_phy_r03_real_false_excludes_AC_line_without_island_conflation():
    grid, _, _ = two_bus()
    off = replace(grid, ac_branches=(
        ACBranch("disabled", "left", "right", .1, 400, in_service=False),))
    _, _, islands, count = ac_topology(off)
    assert off.active_branches == ()
    assert count == 2
    assert len(set(islands)) == 2


@pytest.mark.parametrize("invalid", [
    float("inf"), float("-inf"), float("nan"), 1.0, 1e99,
    1e-5, 0., -1e-7, True, "1e-7", None,
])
def test_phy_r04_bad_tolerance_never_accepted(invalid):
    grid, dispatch, time = two_bus()
    with pytest.raises(DataContractError, match="atol_mw"):
        reference_flows(grid, dispatch, time, atol_mw=invalid)


def test_phy_r04_original_plus20_minus19_hard_rejection_even_at_ceiling():
    grid, dispatch, time = two_bus()
    unbalanced = replace(dispatch, injections_mw=np.array([[20.] * 5, [-19.] * 5]))
    for tol in (1e-7, 1e-6):
        with pytest.raises(DataContractError, match="island"):
            reference_flows(grid, unbalanced, time, atol_mw=tol)
    assert abs(unbalanced.injections_mw[:, 0].sum()) == 1.0


def test_phy_r04_valid_positive_bounded_tolerances_still_solve():
    grid, dispatch, time = two_bus()
    assert np.allclose(reference_flows(grid, dispatch, time, atol_mw=1e-7).flow_mw, 20.)
    assert np.allclose(reference_flows(grid, dispatch, time, atol_mw=1e-6).flow_mw, 20.)


# === Independent physical topology and dense cycle-space oracle ===

def new_three_island_case():
    bus = ("a0", "a1", "a2", "a3", "a4", "b0", "b1", "b2", "c0", "c1")
    branches = (
        ACBranch("x02", "a0", "a2", .09, 400),
        ACBranch("x24", "a2", "a4", .17, 225, kind="transformer",
                 phase_shift_rad=.014),
        ACBranch("x41", "a4", "a1", .11, 400),
        ACBranch("x13", "a1", "a3", .13, 225, kind="pst"),
        ACBranch("x30", "a3", "a0", .08, 400),
        ACBranch("x04", "a0", "a4", .21, 400),
        ACBranch("x23", "a2", "a3", .19, 225),
        ACBranch("x12", "a1", "a2", .25, 400),
        ACBranch("y02", "b0", "b2", .14, 225),
        ACBranch("y21", "b2", "b1", .12, 400, kind="pst"),
        ACBranch("y10", "b1", "b0", .16, 400),
        ACBranch("z10", "c1", "c0", .10, 225, kind="transformer"),
    )
    grid = DetailedGridSnapshot(
        bus, ("DE", "FR", "DE", "FR", "DE", "FR", "FR", "DE", "NI", "NI"),
        branches, (HVDCTerminals("dc_ab", "a1", "b0"),
                   HVDCTerminals("dc_ca", "c1", "a3")),
        137., source("new-grid"),
    )
    ids = tuple(f"202{k}-01-01T00:00:00Z" for k in range(5))
    years = tuple(f"EXTERNAL-Y{k}" for k in range(5))
    time = TimeSet(ids, years, years, np.array([1, 2, 1, 1, 3.]),
                   ("winter", "summer", "winter", "summer", "winter"),
                   source("new-time"))
    target = np.array([30., -13., 8., -11., -14., 12., -5., -7., 4., -4.])
    scale = np.array([.85, 1., 1.15, .92, 1.08])
    net = target[:, None] * scale[None, :]
    transfers = {"dc_ab": np.array([5., 7., 9., -3., 4.]),
                 "dc_ca": np.array([-6., -4., 2., 5., -1.])}
    terminal = np.zeros_like(net)
    for link in grid.hvdc:
        terminal[bus.index(link.bus0)] -= transfers[link.identifier]
        terminal[bus.index(link.bus1)] += transfers[link.identifier]
    phases = {"x13": np.array([.02, -.01, .017, 0., .009]),
              "y21": np.array([-.015, .019, 0., .01, -.009])}
    dispatch = ReferenceDispatchSet(
        bus, ids, net - terminal, transfers, phases, source("new-dispatch"))
    ratings = NormalContingencyRatings(
        ids, {b.identifier: np.full(5, 800.) for b in branches},
        {b.identifier: np.full(5, 900.) for b in branches},
        source("new-ratings"),
    )
    return grid, dispatch, time, ratings, net


def dense_cycle_witness():
    grid, dispatch, time, ratings, expected_net = new_three_island_case()
    sparse_incidence, susceptances, labels, island_count = ac_topology(grid)
    assert issparse(sparse_incidence) and island_count == 3
    assert sparse_incidence.shape == (10, 12) and sparse_incidence.nnz == 24
    assert len(grid.hvdc) == 2 and sum(b.kind == "pst" for b in grid.ac_branches) == 2
    a = np.zeros((len(grid.bus_ids), len(grid.active_branches)))
    for j, branch in enumerate(grid.active_branches):
        a[grid.bus_ids.index(branch.bus0), j] = 1.
        a[grid.bus_ids.index(branch.bus1), j] = -1.
    cycles = null_space(a)
    assert cycles.shape == (12, 5)  # L - N + number of AC islands
    x_over_base = np.array([b.x_pu / grid.base_mva for b in grid.active_branches])
    matrix = np.vstack((a, cycles.T @ np.diag(x_over_base)))
    solution = reference_flows(grid, dispatch, time)
    assert np.array_equal(np.unique(labels, return_counts=True)[1], [5, 3, 2])
    assert preflight(grid, dispatch, time, ratings, country_label_map={
        "DE": "Germany", "FR": "France", "NI": "Northern Ireland",
    }).status == "PASS"
    flow_error = kcl = kvl = balance = 0.
    for t in range(5):
        phase = np.array([
            dispatch.pst_phase_rad[b.identifier][t] if b.kind == "pst"
            else b.phase_shift_rad for b in grid.active_branches
        ])
        desired = np.r_[expected_net[:, t], -(cycles.T @ phase)]
        dense, *_ = np.linalg.lstsq(matrix, desired, rcond=None)
        flow_error = max(flow_error, float(np.max(np.abs(solution.flow_mw[:, t] - dense))))
        kcl = max(kcl, float(np.max(np.abs(a @ solution.flow_mw[:, t] - expected_net[:, t]))))
        kvl = max(kvl, float(np.max(np.abs(cycles.T @ (
            x_over_base * solution.flow_mw[:, t] + phase)))))
        for island in range(island_count):
            balance = max(balance, abs(float(expected_net[labels == island, t].sum())))
        assert np.max(np.abs(matrix @ dense - desired)) < 3e-9
        assert np.max(np.abs(solution.nodal_net_mw[:, t] - expected_net[:, t])) < 3e-12
    return {
        "case": "RR1-PHY-new-10bus-3island-12AC-5cycle-2HVDC-2PST",
        "buses": 10, "ac_branches": 12, "islands": 3, "cycles": 5,
        "hvdc": 2, "pst": 2, "snapshots": 5,
        "max_oracle_flow_abs_mw": flow_error,
        "max_kcl_abs_mw": kcl,
        "max_affine_kvl_abs_rad": kvl,
        "max_island_balance_abs_mw": balance,
        "reference_input_sha256": solution.input_sha256,
        "real_network_qualified": False,
    }


def test_new_10bus_hvdc_pst_fixed_shift_cycle_space_oracle():
    numbers = dense_cycle_witness()
    assert numbers["max_oracle_flow_abs_mw"] < 3e-8
    assert numbers["max_kcl_abs_mw"] < 3e-9
    assert numbers["max_affine_kvl_abs_rad"] < 1e-11
    assert numbers["max_island_balance_abs_mw"] < 1e-10


def test_reversing_new_pst_and_hvdc_directions_is_physically_invariant():
    grid, dispatch, time, _, _ = new_three_island_case()
    baseline = reference_flows(grid, dispatch, time)
    edges = list(grid.ac_branches)
    i = next(i for i, e in enumerate(edges) if e.identifier == "x13")
    edges[i] = replace(edges[i], bus0="a3", bus1="a1")
    links = list(grid.hvdc)
    links[0] = replace(links[0], bus0="b0", bus1="a1")
    changed_grid = replace(grid, ac_branches=edges, hvdc=links)
    phases = dict(dispatch.pst_phase_rad)
    phases["x13"] = -phases["x13"]
    trans = dict(dispatch.hvdc_transfer_mw)
    trans["dc_ab"] = -trans["dc_ab"]
    changed_dispatch = replace(dispatch, pst_phase_rad=phases, hvdc_transfer_mw=trans)
    transformed = reference_flows(changed_grid, changed_dispatch, time)
    expected = baseline.flow_mw.copy()
    expected[i] *= -1.
    np.testing.assert_allclose(transformed.flow_mw, expected, rtol=0., atol=2e-8)
    np.testing.assert_allclose(transformed.nodal_net_mw, baseline.nodal_net_mw, atol=1e-11)


def test_hvdc_transfer_change_without_redispatch_cannot_hide_island_balance():
    grid, dispatch, time, _, _ = new_three_island_case()
    changed = dict(dispatch.hvdc_transfer_mw)
    changed["dc_ab"] = changed["dc_ab"] + 1.0
    with pytest.raises(DataContractError, match="island"):
        reference_flows(grid, replace(dispatch, hvdc_transfer_mw=changed), time)


def test_1001_bus_sparse_nonuniform_dispatch_analytic_chain_oracle():
    n = 1001
    buses = tuple("s" + str(i) for i in range(n))
    grid = DetailedGridSnapshot(
        buses, ("DE",) * n,
        tuple(ACBranch(f"e{i}", buses[i], buses[i+1], .04 + (i % 7) * .013,
                       400 if i % 2 else 225) for i in range(n-1)),
        (), 117., source("sparse-1001"))
    ids = tuple(f"202{k}-01-01T00:00:00Z" for k in range(5))
    years = tuple(f"TEST-{k}" for k in range(5))
    time = TimeSet(ids, years, years, np.ones(5), ("winter",) * 5, source("sparse-time"))
    scale = np.array([1., .7, 1.3, 1.1, .85])
    injections = np.zeros((n, 5))
    injections[0] = +10 * scale
    injections[300] = -3 * scale
    injections[700] = -4 * scale
    injections[-1] = -3 * scale
    dispatch = ReferenceDispatchSet(buses, ids, injections, {}, {}, source("sparse-dispatch"))
    a, _, islands, count = ac_topology(grid)
    assert count == 1 and issparse(a) and a.nnz == 2 * (n-1)
    result = reference_flows(grid, dispatch, time)
    expected = np.array([10.] * 300 + [7.] * 400 + [3.] * 300)[:, None] * scale
    assert expected.shape == (1000, 5)
    np.testing.assert_allclose(result.flow_mw, expected, rtol=0, atol=3e-8)
    np.testing.assert_allclose(a @ result.flow_mw, injections, rtol=0, atol=3e-8)


# === Fail-closed data/time/raters, source hash and 15-file synthetic witness ===

def test_source_time_rating_rejections_and_changed_injection_hash():
    grid, dispatch, time, ratings, _ = new_three_island_case()
    with pytest.raises(DataContractError, match="SHA-256"):
        replace(grid.provenance, source_sha256="0"*63)
    with pytest.raises(DataContractError, match="UTC-aware"):
        replace(time, snapshot_ids=tuple(x[:-1] for x in time.snapshot_ids))
    with pytest.raises(DataContractError, match="chronological"):
        replace(time, snapshot_ids=tuple(reversed(time.snapshot_ids)),
                year_for_snapshot=tuple(reversed(time.year_for_snapshot)))
    with pytest.raises(DataContractError, match="MW"):
        replace(ratings, unit="MVA")
    with pytest.raises(DataContractError, match="110-kV"):
        reference_flows(replace(grid, incomplete_110kv_ties=True), dispatch, time)
    with pytest.raises(DataContractError, match="PST"):
        reference_flows(grid, replace(dispatch, pst_phase_rad={}), time)
    with pytest.raises(DataContractError, match="HVDC"):
        reference_flows(grid, replace(dispatch, hvdc_transfer_mw={}), time)
    bad_rating = replace(ratings, contingency_mw={"x02": np.full(5, 900.)})
    assert preflight(grid, dispatch, time, bad_rating, country_label_map={
        "DE": "Germany", "FR": "France", "NI": "Northern Ireland",
    }).status == "BLOCKED_DATA"
    baseline = reference_flows(grid, dispatch, time).input_sha256
    injections = dispatch.injections_mw.copy()
    injections[0] += 2.
    injections[1] -= 2.
    assert reference_flows(grid, replace(dispatch, injections_mw=injections),
                           time).input_sha256 != baseline


def test_fifteen_file_fixture_sha_manifest_and_operator_consistency(tmp_path):
    args = build_synthetic_fixture()
    result = execute_ma1(*args, protected_line_ids=("d12",))
    assert result.preflight.status == "PASS"
    assert len(result.preflight.ac_islands) == 2
    assert result.seed.quota_counts == {
        "Germany": 2, "France": 1, "Northern Ireland": 1,
    }
    assert result.gate_statuses["G11_part_devices"] == "PASS_LOSSLESS_DC_EQUIVALENT_ONLY"
    output = tmp_path / "independent-fixture"
    manifest = result.export(output, code_commit=REPAIR_SHA)
    assert manifest["code_commit"] == REPAIR_SHA
    assert manifest["independent_reviewer_release"] is False
    assert manifest["real_network_qualified"] is False
    assert manifest["budget_page_evidence"] == "NOT_APPLICABLE_SYNTHETIC"
    assert manifest["protected_line_ids"] == ["d12"]
    assert len(manifest["ratings_content_sha256"]) == 64
    assert len(manifest["budget_source_sha256"]) == 64
    assert len(manifest["output_sha256"]) == 14
    assert len([p for p in output.iterdir() if p.is_file()]) == 15
    for filename, digest in manifest["output_sha256"].items():
        assert sha256((output / filename).read_bytes()).hexdigest() == digest, filename
    matrices = {n: load_npz(output / f"operator_{n}.npz") for n in ("P", "Gamma", "A_z", "A_d")}
    lhs = matrices["A_z"] @ matrices["Gamma"] - matrices["P"] @ matrices["A_d"]
    assert lhs.nnz == 0 or np.max(np.abs(lhs.data)) < 1e-11
    # Explicit negative: tampering is detectable by independent SHA recomputation.
    path = output / "busmap.csv"
    path.write_bytes(path.read_bytes() + b"tamper\n")
    assert sha256(path.read_bytes()).hexdigest() != manifest["output_sha256"]["busmap.csv"]


if __name__ == "__main__":
    metrics = dense_cycle_witness()
    path = Path(sys.argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metrics, sort_keys=True))
