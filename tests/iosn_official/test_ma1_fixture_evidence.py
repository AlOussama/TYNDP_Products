"""Check end-to-end two-island, cross-border artifact emission."""
from hashlib import sha256
import json
import numpy as np
from scipy.sparse import load_npz
from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture
from tyndp_reduce.iosn_official.ma1 import execute_ma1


def test_synthetic_fixture_two_islands_three_countries_five_years(tmp_path):
    args = build_synthetic_fixture()
    result = execute_ma1(*args, protected_line_ids=("d12",))
    ledger = result.preflight
    assert ledger.status == "PASS"
    assert ledger.model_sizes["buses"] == 7
    assert ledger.model_sizes["active_ac_branches"] == 8
    assert ledger.model_sizes["hvdc_links"] == 1
    assert ledger.model_sizes["weather_year_count"] == 5
    assert len(ledger.ac_islands) == 2
    assert result.seed.quota_counts == {
        "Germany": 2, "France": 1, "Northern Ireland": 1}
    assert "United Kingdom" not in result.resolved_country_of_bus
    assert len(set(result.seed.zone_of_bus)) == 4
    assert set(result.seed.retained_cross_country_branch_ids) == {
        "cross_de_fr_1", "cross_fr_de_2"}
    assert result.projection.verify(result.reference)
    pz, cut = result.projection.aggregate(result.reference)
    np.testing.assert_allclose(result.projection.A_z @ cut, pz, atol=1e-7)
    manifest = result.export(tmp_path / "evidence", code_commit="test-commit-pinned")
    assert manifest["real_network_qualified"] is False
    assert manifest["independent_reviewer_release"] is False
    assert manifest["status"] == "MA1_SYNTHETIC_CONTRACT_PASS_ONLY"
    assert result.screen.year_ids == args[2].weather_year_ids
    folder = tmp_path / "evidence"
    preflight = json.loads((folder / "preflight_ledger.json").read_text())
    assert len(preflight["ac_islands"]) == 2
    assert preflight["country_ids"]["NI"]["resolved"] == "Northern Ireland"
    for filename, digest in manifest["output_sha256"].items():
        assert sha256((folder / filename).read_bytes()).hexdigest() == digest
    az, gm, p, ad = [load_npz(folder / ("operator_" + name + ".npz"))
                     for name in ("A_z", "Gamma", "P", "A_d")]
    diff = az @ gm - p @ ad
    assert diff.nnz == 0 or np.max(np.abs(diff.data)) <= 1e-12
