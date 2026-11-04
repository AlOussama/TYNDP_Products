"""End-to-end synthetic Module-2 MA1 with immutable upstream contracts.

This is NOT an ENTSO-E real-data or full IoSN 102-zone qualification.
"""
from dataclasses import replace
from hashlib import sha256
import json
import numpy as np
import pytest
from scipy.sparse import load_npz

from tyndp_reduce.iosn_official.contracts import (
    ACBranch, HVDCTerminals, DetailedGridSnapshot, ReferenceDispatchSet,
    TimeSet, NormalContingencyRatings, Provenance, DataContractError,
)
from tyndp_reduce.iosn_official.country import CountryZoneBudget
from tyndp_reduce.iosn_official.ma1 import execute_ma1


def provenance(name):
    return Provenance(
        name, "synthetic://ma1/" + name, "1",
        sha256(name.encode()).hexdigest(), synthetic=True,
    )


def complete_fixture():
    edges = (
        ACBranch("d01", "d0", "d1", .1, 225),
        ACBranch("d12", "d1", "d2", .1, 400),
        ACBranch("d20", "d2", "d0", .1, 110),
        ACBranch("cross1", "d1", "f0", .2, 400),
        ACBranch("f01", "f0", "f1", .1, 400),
        ACBranch("cross2", "f1", "d0", .2, 400),
        ACBranch("phase", "d0", "d2", .2, 400, "pst"),
    )
    grid = DetailedGridSnapshot(
        bus_ids=("d0", "d1", "d2", "f0", "f1"),
        raw_country_ids=("DE", "DE", "DE", "FR", "FR"),
        ac_branches=edges, hvdc=(HVDCTerminals("dc", "d2", "f1"),),
        base_mva=100., provenance=provenance("grid"),
    )
    snapshot_ids = tuple(f"202{i}-01-01T00:00:00Z" for i in range(5))
    years = tuple(f"W{i}" for i in range(5))
    time = TimeSet(
        snapshot_ids, years, years, np.array([1., 2., 3., 1., 1.]),
        ("winter", "summer", "winter", "summer", "winter"),
        provenance("times"),
    )
    p = np.tile(np.array([20., -12., -5., -1., -2.])[:, None], (1, 5))
    dispatch = ReferenceDispatchSet(
        grid.bus_ids, time.snapshot_ids, p,
        {"dc": np.full(5, 1.)},
        {"phase": np.array([0., .01, 0., .01, 0.])},
        provenance("dispatch"),
    )
    ratings = NormalContingencyRatings(
        snapshot_ids,
        {edge.identifier: np.full(5, 10.) for edge in edges},
        {edge.identifier: np.full(5, 15.) for edge in edges},
        provenance("rating"),
    )
    budget = CountryZoneBudget.synthetic({"Germany": 2, "France": 1})
    mapping = {"DE": "Germany", "FR": "France"}
    weights = {year: 1. for year in years}
    return grid, dispatch, time, ratings, budget, mapping, weights


def test_ma1_complete_synthetic_flow_country_quotas_and_crossborder():
    grid, dispatch, time, ratings, budget, mapping, weights = complete_fixture()
    obj = execute_ma1(
        grid, dispatch, time, ratings, budget, mapping, weights,
        protected_line_ids=("d12",),
    )
    assert obj.preflight.status == "PASS"
    assert obj.preflight.model_sizes["hvdc_links"] == 1
    assert obj.preflight.model_sizes["weather_year_count"] == 5
    assert obj.preflight.model_sizes["active_ac_branches"] == 7
    assert obj.reference.flow_mw.shape == (7, 5)
    assert obj.seed.quota_counts == {"Germany": 2, "France": 1}
    assert len(set(obj.seed.zone_of_bus)) == 3
    assert {"cross1", "cross2"}.issubset(set(obj.seed.retained_cross_country_branch_ids))
    assert obj.screen.year_ids == time.weather_year_ids
    assert "d20" not in obj.screen.screened_line_ids
    assert "phase" not in obj.screen.screened_line_ids
    assert obj.projection.verify(obj.reference)
    pzone, flowcut = obj.projection.aggregate(obj.reference)
    np.testing.assert_allclose(obj.projection.A_z @ flowcut, pzone, atol=1e-7)
    assert obj.gate_statuses["real_input_and_independent_review"] == "BLOCKED_DATA_AND_REVIEW"
    assert obj.input_manifest_sha256 == execute_ma1(
        grid, dispatch, time, ratings, budget, mapping, weights,
        protected_line_ids=("d12",)).input_manifest_sha256


def test_ma1_export_provenance_hashed_global_cache_and_projection(tmp_path):
    inputs = complete_fixture()
    obj = execute_ma1(*inputs, protected_line_ids=("d12",))
    path = tmp_path / "ma1"
    manifest = obj.export(path, code_commit="test-commit-pinned")
    assert manifest["real_network_qualified"] is False
    assert manifest["independent_reviewer_release"] is False
    assert manifest["calibration_equivalent_x_c0"] == "NOT_IN_MA1"
    assert manifest["input_manifest_sha256"] == obj.input_manifest_sha256
    for filename, expected_hash in manifest["output_sha256"].items():
        assert (path / filename).is_file()
        assert sha256((path / filename).read_bytes()).hexdigest() == expected_hash
    assert json.loads((path / "manifest.json").read_text())["code_commit"] == "test-commit-pinned"
    with np.load(path / "global_reference_flows.npz", allow_pickle=False) as frozen:
        np.testing.assert_allclose(frozen["flow_mw"], obj.reference.flow_mw)
        np.testing.assert_allclose(frozen["nodal_net_mw"], obj.reference.nodal_net_mw)
        assert list(frozen["snapshot_ids"]) == list(inputs[2].snapshot_ids)
    A_d = load_npz(path / "operator_A_d.npz")
    A_z = load_npz(path / "operator_A_z.npz")
    P = load_npz(path / "operator_P.npz")
    Gamma = load_npz(path / "operator_Gamma.npz")
    residual = A_z @ Gamma - P @ A_d
    assert residual.nnz == 0 or np.max(np.abs(residual.data)) <= 1e-12
    busmap_rows = (path / "busmap.csv").read_text().splitlines()
    assert len(busmap_rows) == len(inputs[0].bus_ids) + 1
    assert "Germany" in "\n".join(busmap_rows)
    assert len((path / "annual_criticality.csv").read_text().splitlines()) > 5
    with pytest.raises(FileExistsError):
        obj.export(path, code_commit="second")


def test_ma1_fail_closed_missing_hvdc_dispatch_and_rating_or_country():
    grid, dispatch, time, ratings, budget, mapping, weights = complete_fixture()
    with pytest.raises(DataContractError, match="HVDC"):
        execute_ma1(grid, replace(dispatch, hvdc_transfer_mw={}),
                    time, ratings, budget, mapping, weights)
    with pytest.raises(DataContractError, match="ratings"):
        execute_ma1(grid, dispatch, time,
                    replace(ratings, normal_mw={"d01": np.full(5, 10.)}),
                    budget, mapping, weights)
    with pytest.raises(DataContractError, match="unresolved"):
        execute_ma1(grid, dispatch, time, ratings, budget,
                    {"DE": "Germany"}, weights)


def test_ma1_comparative_year_weights_are_explicit_not_silent():
    grid, dispatch, time, ratings, budget, mapping, weights = complete_fixture()
    from tyndp_reduce.iosn_official.screen import ScreeningError
    with pytest.raises(ScreeningError, match="weights"):
        execute_ma1(grid, dispatch, time, ratings, budget, mapping,
                    {"W0": 1.})
