# SPDX-License-Identifier: MIT
"""End-to-end CLI fixture smoke, deliberately not real M0/PECD evidence."""
import json
import subprocess
import sys

from hydro_fixtures import fixture_case


def test_cli_five_file_manifest_and_original_id_outputs(tmp_path):
    case = fixture_case(tmp_path)
    manifest_file = tmp_path / "manifest.json"
    allocations_file = tmp_path / "hydro_allocations.csv"
    inventory_file = tmp_path / "m0_original_asset_inventory.csv"
    out = tmp_path / "cli-output"
    manifest_file.write_text(json.dumps(case["manifest"]), encoding="utf-8")
    case["allocations"].to_csv(allocations_file, index=False)
    case["assets_frame"].to_csv(inventory_file, index=False)
    command = [
        sys.executable, "-m", "scripts.iosn_m1.hydro.cli",
        "--manifest", str(manifest_file),
        "--allocations", str(allocations_file),
        "--assets", str(inventory_file),
        "--snapshots", str(tmp_path / "snapshots.csv"),
        "--source-root", str(tmp_path),
        "--planning-horizon", "2030",
        "--weather-id", "FIXTURE-WS-01",
        "--output-dir", str(out),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    qa = json.loads((out / "qa.json").read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert qa["selected_weather_count"] == 5
    assert qa["source_status"] == "FIXTURE_ONLY"
    assert qa["native_intervals_checked"] == 1
    assert (out / "hydro_inflow.csv").exists()
    assert (out / "closed_loop_policy_ledger.csv").exists()
    assert "original-hydro-1" in (out / "hydro_inflow.csv").read_text(encoding="utf-8")
