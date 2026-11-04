"""PHY worker: fixed numeric cases and fail-closed acceptance fixtures, no PyPSA."""
from hashlib import sha256
from dataclasses import replace
import numpy as np
import pytest

from tyndp_reduce.iosn_official.contracts import (
    ACBranch, HVDCTerminals, DetailedGridSnapshot, ReferenceDispatchSet,
    TimeSet, NormalContingencyRatings, Provenance,
    DataContractError, RejectedComponent,
)
from tyndp_reduce.iosn_official.physical import ac_topology, reference_flows
from tyndp_reduce.iosn_official.preflight import preflight


def source(name="ma1_fixture"):
    return Provenance(name, "synthetic://ma1/" + name, "1",
                      sha256(name.encode("utf-8")).hexdigest(), synthetic=True)


def fixture(phase=0.0):
    grid = DetailedGridSnapshot(
        bus_ids=("a0", "a1", "a2", "b0", "b1"),
        raw_country_ids=("DE", "DE", "DE", "FR", "FR"),
        ac_branches=(
            ACBranch("pst", "a0", "a1", 0.1, 400, "pst"),
            ACBranch("a12", "a1", "a2", 0.1, 400),
            ACBranch("a20", "a2", "a0", 0.1, 400),
            ACBranch("trafo", "b0", "b1", 0.1, 225, "transformer"),
        ),
        hvdc=(HVDCTerminals("dcbridge", "a2", "b0"),),
        base_mva=100, provenance=source("grid"),
    )
    ids = tuple(f"20{18+i}-01-01T00:00:00Z" for i in range(5))
    times = TimeSet(ids, tuple(f"Y{i+1}" for i in range(5)),
                    tuple(f"Y{i+1}" for i in range(5)),
                    np.array([1, 2, 1, 1, 1]),
                    ("winter", "summer", "winter", "summer", "winter"),
                    source("time"))
    disp = ReferenceDispatchSet(grid.bus_ids, ids,
                                np.tile(np.array([20., -10., 0., -5., -5.])[:, None], (1, 5)),
                                {"dcbridge": np.full(5, 10.)},
                                {"pst": np.full(5, phase)},
                                source("dispatch"))
    ratings = NormalContingencyRatings(ids, {x.identifier: np.full(5, 200.) for x in grid.active_branches},
                                       {x.identifier: np.full(5, 240.) for x in grid.active_branches},
                                       source("rating"))
    return grid, disp, times, ratings


def test_two_ac_islands_hvdc_transformer_orientation():
    grid, dispatch, time, ratings = fixture()
    A, susceptance, labels, count = ac_topology(grid)
    assert count == 2
    assert A.shape == (5, 4)
    assert A.nnz == 8
    np.testing.assert_array_equal(labels, [0, 0, 0, 1, 1])
    actual = reference_flows(grid, dispatch, time)
    np.testing.assert_allclose(actual.flow_mw[:, 0], [10., 0., -10., 5.], atol=1e-9)
    np.testing.assert_allclose(actual.nodal_net_mw[:, 0], [20., -10., -10., 5., -5.])
    np.testing.assert_allclose(A @ actual.flow_mw, actual.nodal_net_mw, atol=1e-8)
    assert actual.flow_mw.flags.writeable is False
    with pytest.raises(ValueError):
        actual.flow_mw[0, 0] = 100
    with pytest.raises(ValueError):
        actual.flow_mw.setflags(write=True)
    assert reference_flows(grid, dispatch, time).input_sha256 == actual.input_sha256
    assert preflight(grid, dispatch, time, ratings,
                     country_label_map={"DE": "Germany", "FR": "France"}).status == "PASS"


def test_pst_affine_circulation_and_independent_dense_reference():
    grid, dispatch, time, _ = fixture(phase=0.03)
    solved = reference_flows(grid, dispatch, time)
    np.testing.assert_allclose(solved.flow_mw[:, 0], [0., -10., -20., 5.], atol=1e-8)
    A, b, labels, _ = ac_topology(grid)
    phase = np.array([0.03, 0., 0., 0.])
    B = (A.multiply(b) @ A.T).toarray()
    net = solved.nodal_net_mw[:, 0]
    theta = np.zeros(5)
    for member in ([0, 1, 2], [3, 4]):
        keep = member[1:]
        rhs = net - A @ (-b * phase)
        theta[keep] = np.linalg.solve(B[np.ix_(keep, keep)], rhs[keep])
    independent = b * (A.T @ theta - phase)
    np.testing.assert_allclose(solved.flow_mw[:, 0], independent, atol=1e-9)
    assert solved.input_sha256 != reference_flows(*fixture()[:3]).input_sha256


def test_neutral_calibration_is_distinct_and_rejects_imbalanced_islands():
    grid, dispatch, time, _ = fixture(phase=0.03)
    with pytest.raises(DataContractError, match="island"):
        reference_flows(grid, dispatch, time, neutral_calibration=True)
    neutral_dispatch = replace(
        dispatch, injections_mw=np.tile(np.array([10., -10., 0., 5., -5.])[:, None], (1, 5)))
    neutral = reference_flows(grid, neutral_dispatch, time, neutral_calibration=True)
    np.testing.assert_allclose(neutral.nodal_net_mw[:, 0], [10., -10., 0., 5., -5.])
    assert neutral.neutral_calibration
    assert neutral.input_sha256 != reference_flows(grid, dispatch, time).input_sha256


def test_no_hidden_island_slack_and_missing_terminal_schedule():
    grid, dispatch, time, _ = fixture()
    with pytest.raises(DataContractError, match="island"):
        reference_flows(grid, replace(dispatch, injections_mw=dispatch.injections_mw + 1.0), time)
    with pytest.raises(DataContractError, match="HVDC"):
        reference_flows(grid, replace(dispatch, hvdc_transfer_mw={}), time)


def test_orientation_reversal_flips_branch_flow():
    grid, dispatch, time, _ = fixture()
    branches = list(grid.ac_branches)
    branches[-1] = replace(branches[-1], bus0="b1", bus1="b0")
    altered = replace(grid, ac_branches=tuple(branches))
    original_f = reference_flows(grid, dispatch, time).flow_mw
    reversed_f = reference_flows(altered, dispatch, time).flow_mw
    np.testing.assert_allclose(reversed_f[-1], -original_f[-1])


def test_preflight_contracts_and_rejected_component():
    grid, dispatch, time, ratings = fixture()
    missing = preflight(grid, dispatch, time, ratings, country_label_map={"DE": "Germany"})
    assert missing.status == "BLOCKED_DATA"
    assert "unresolved" in missing.to_json()
    bad_110 = preflight(replace(grid, incomplete_110kv_ties=True),
                        dispatch, time, ratings,
                        country_label_map={"DE": "Germany", "FR": "France"})
    assert bad_110.status == "BLOCKED_DATA"
    blocked = preflight(replace(grid, unsupported_components=("unknown_svc",)),
                        dispatch, time, ratings,
                        country_label_map={"DE": "Germany", "FR": "France"})
    assert blocked.status == "REJECTED_COMPONENT"
    with pytest.raises(DataContractError):
        blocked.require_pass()
    with pytest.raises(RejectedComponent):
        reference_flows(replace(grid, unsupported_components=("unknown_svc",)), dispatch, time)


def test_ratings_units_and_year_contract_are_hard():
    grid, dispatch, time, ratings = fixture()
    with pytest.raises(DataContractError, match="MW"):
        replace(ratings, unit="MVA")
    with pytest.raises(DataContractError, match="Five"):
        replace(time, weather_year_ids=("Y1",))
    incomplete = replace(ratings, normal_mw={"pst": np.full(5, 100.)})
    ledger = preflight(grid, dispatch, time, incomplete,
                       country_label_map={"DE": "Germany", "FR": "France"})
    assert ledger.status == "BLOCKED_DATA"


def test_provenance_missing_hash_rejected():
    with pytest.raises(DataContractError):
        Provenance("x", "synthetic://x", "v1", "")


def test_invalid_chronology_or_non_utc_snapshots_rejected():
    grid, dispatch, time, _ = fixture()
    with pytest.raises(DataContractError, match="chronological"):
        replace(time, snapshot_ids=tuple(reversed(time.snapshot_ids)),
                year_for_snapshot=tuple(reversed(time.year_for_snapshot)))
    with pytest.raises(DataContractError, match="UTC-aware"):
        replace(time, snapshot_ids=tuple(x.removesuffix("Z") for x in time.snapshot_ids))
    with pytest.raises(DataContractError, match="ISO-8601"):
        replace(time, snapshot_ids=("not-a-time",) + time.snapshot_ids[1:])
