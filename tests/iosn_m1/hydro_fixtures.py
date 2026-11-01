# SPDX-License-Identifier: MIT
"""Synthetic-only hydro sources. Not evidence of PECD or real M0 input."""
import hashlib
from pathlib import Path

import pandas as pd

from scripts.iosn_m1.hydro.adapter import CONTRACT, read_snapshots


def fixture_case(tmp_path: Path, *, tech="HRI", semantics="STORAGE_ENERGY_EQUIVALENT_MWH",
                 zone="UTC", native_intervals=None, two_assets=False):
    if native_intervals is None:
        native_intervals = [
            ("2026-01-01T00:00:00+00:00", "2026-01-03T00:00:00+00:00", 96.0)
        ]
    native_start = pd.Timestamp(native_intervals[0][0]).tz_convert("UTC")
    native_end = pd.Timestamp(native_intervals[-1][1]).tz_convert("UTC")
    timestamps = pd.date_range(native_start, native_end, freq="h", inclusive="left")
    snap_path = tmp_path / "snapshots.csv"
    pd.DataFrame({"timestamp": [x.isoformat() for x in timestamps],
                  "duration_hours": [1] * len(timestamps)}).to_csv(snap_path, index=False)
    weather_ids = ["FIXTURE-WS-01", "FIXTURE-WS-02", "FIXTURE-WS-03",
                   "FIXTURE-WS-04", "FIXTURE-WS-05"]
    sources = []
    for i, weather_id in enumerate(weather_ids):
        name = f"input_{i + 1}.csv"
        path = tmp_path / name
        pd.DataFrame(native_intervals, columns=["start", "end", "energy_mwh"]).to_csv(
            path, index=False)
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        sources.append({
            "planning_horizon": "2030", "weather_id": weather_id,
            "source_id": f"fixture-H-{i+1}", "source_dataset_id": "SYNTHETIC_ONLY",
            "source_dataset_version": "test-1", "corrected_dataset_revision": "FIXTURE",
            "source_uri": "fixture://ma3", "license": "fixture-only",
            "source_evidence_ref": "FIXTURE_ONLY",
            "hydro_area_id": "FIXTURE-BASIN-A", "hydro_tech": tech,
            "semantics": semantics, "unit": "MWh",
            "resolution": "WEEK" if (native_end - native_start).days > 1 else "DAY",
            "timezone": zone, "path": name, "sha256": sha,
        })
    manifest = {
        "contract": CONTRACT, "source_mode": "FIXTURE",
        "network_revision_id": "FIXTURE-M0-REV-1", "source_set_hash": "FIXTURE-M0-SHASH",
        "mapping_policy_hash": "FIXTURE-M0-PHASH",
        "selected_weather_ids": weather_ids, "sources": sources,
        "closed_loop_no_natural_inflow": [],
    }
    ids = ["existing-su-101", "existing-su-102"] if two_assets else ["existing-su-101"]
    weights = [0.6, 0.4] if two_assets else [1.0]
    assets = []
    allocations = []
    for idx, (component_id, weight) in enumerate(zip(ids, weights)):
        asset_id = f"original-hydro-{idx+1}"
        assets.append({
            "asset_id": asset_id, "existing_component_id": component_id,
            "component_class": "StorageUnit", "hydro_tech": tech, "bus_id": "original-bus",
            "network_revision_id": "FIXTURE-M0-REV-1", "role": "HYDRO_ASSET",
            "p_nom_mw": "10", "max_hours": "48",
            "efficiency_dispatch": "0.9", "e_nom_mwh": "",
        })
        allocations.append({
            "planning_horizon": "2030", "network_revision_id": "FIXTURE-M0-REV-1",
            "hydro_area_id": "FIXTURE-BASIN-A", "hydro_tech": tech,
            "asset_id": asset_id, "share": str(weight),
            "mapping_basis": "HYDROLOGICAL_BASIN", "evidence_ref": "FIXTURE_SHARE_ONLY",
            "conversion_factor": "1", "conversion_evidence_ref": "IDENTITY",
            "port_generator_id": "", "port_approval_ref": "", "allowlist_approved": "NO",
        })
    return {
        "manifest": manifest, "allocations": pd.DataFrame(allocations),
        "assets": pd.DataFrame(assets), "snapshots": read_snapshots(snap_path),
        "root": tmp_path, "planning_horizon": "2030", "weather_id": weather_ids[0],
    }
