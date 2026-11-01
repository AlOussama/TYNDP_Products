# SPDX-License-Identifier: MIT
"""Build five explicit SYNTHETIC-only MA4F M0/PECD/Hydro fixtures.

This is a test factory, NOT a reader or generator of real M0, PECD, TYNDP or
weather years. It deliberately reuses the MA2 and MA3 producer fixture makers.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pypsa
import yaml

from test_res_adapter import make_fixture, WEATHERS, HORIZON
from hydro_fixtures import fixture_case
from scripts.iosn_m1.res.adapter import digest


REVISION = "M0-FIXTURE-REV"


def save_json(path, payload):
    Path(path).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8")


def build(root):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    res = make_fixture(root)
    catalog = pd.read_csv(res.m0_assets, dtype=str, keep_default_na=False)
    ror_registry = {
        "network_revision_id": REVISION, "asset_id": "A-ROR",
        "existing_generator_id": "G-CGMES-ROR", "existing_bus_id": "original-bus",
        "carrier": "ror", "technology_variant": "", "p_nom_mw": "10",
        "bus_role": "ORIGINAL", "geo_quality": "FIXTURE",
        "res_profile_required": "false",
    }
    catalog = pd.concat([catalog, pd.DataFrame([ror_registry])], ignore_index=True)
    catalog.to_csv(res.m0_assets, index=False)
    m0 = json.loads(res.m0_reference_manifest.read_text())
    m0["asset_registry_sha256"] = digest(res.m0_assets)
    m0["generator_count"] = len(catalog)
    save_json(res.m0_reference_manifest, m0)

    # Two source-native hours, five distinct synthetic source files for both producers.
    native = [("2020-01-01T00:00:00+00:00", "2020-01-01T02:00:00+00:00", 4.0)]
    hydro = fixture_case(root, two_assets=True, native_intervals=native)
    hydro["manifest"]["selected_weather_ids"] = WEATHERS
    hydro["manifest"]["network_revision_id"] = REVISION
    hydro["manifest"]["source_set_hash"] = m0["source_set_hash"]
    hydro["manifest"]["mapping_policy_hash"] = m0["mapping_policy_hash"]
    for i, s in enumerate(hydro["manifest"]["sources"]):
        s["weather_id"] = WEATHERS[i]
    hydro["assets_frame"]["network_revision_id"] = REVISION
    hydro["allocations"]["network_revision_id"] = REVISION

    ror = {"asset_id": "A-ROR", "existing_component_id": "G-CGMES-ROR",
           "component_class": "Generator", "hydro_tech": "HRR",
           "bus_id": "original-bus", "network_revision_id": REVISION,
           "role": "HYDRO_ASSET", "p_nom_mw": "10",
           "max_hours": "", "efficiency_dispatch": "", "e_nom_mwh": ""}
    hcl = {"asset_id": "A-HCL", "existing_component_id": "HCL-FX",
           "component_class": "StorageUnit", "hydro_tech": "HCL",
           "bus_id": "original-bus", "network_revision_id": REVISION,
           "role": "HYDRO_ASSET", "p_nom_mw": "12",
           "max_hours": "24", "efficiency_dispatch": ".9", "e_nom_mwh": ""}
    hydro["assets_frame"] = pd.concat([
        hydro["assets_frame"], pd.DataFrame([ror, hcl])], ignore_index=True)
    hydro["manifest"]["closed_loop_no_natural_inflow"] = [{
        "asset_id": "A-HCL", "policy": "NO_NATURAL_INFLOW_BY_DESIGN",
        "evidence_ref": "FIXTURE_ONLY_HCL_CLASSIFICATION"}]
    for i, weather in enumerate(WEATHERS):
        src = copy.deepcopy(hydro["manifest"]["sources"][i])
        src["weather_id"] = weather
        src["source_id"] = "FIXTURE-ROR-" + str(i + 1)
        src["path"] = "ror_" + str(i + 1) + ".csv"
        src["hydro_area_id"] = "FIXTURE-ROR-BASIN"
        src["hydro_tech"] = "HRR"
        src["semantics"] = "AVAILABLE_GENERATION_ENERGY_MWH"
        pd.DataFrame(native, columns=["start", "end", "energy_mwh"]).to_csv(
            root / src["path"], index=False)
        src["sha256"] = digest(root / src["path"])
        hydro["manifest"]["sources"].append(src)
    hydro["allocations"] = pd.concat([
        hydro["allocations"],
        pd.DataFrame([{"planning_horizon": HORIZON,
            "network_revision_id": REVISION, "hydro_area_id": "FIXTURE-ROR-BASIN",
            "hydro_tech": "HRR", "asset_id": "A-ROR", "share": "1",
            "mapping_basis": "HYDROLOGICAL_BASIN", "evidence_ref": "FIXTURE_ONLY",
            "conversion_factor": "1", "conversion_evidence_ref": "FIXTURE_EQUAL_ENERGY",
            "port_generator_id": "", "port_approval_ref": "",
            "allowlist_approved": "NO"}])], ignore_index=True)
    hydro_manifest_path = root / "hydro_manifest.json"
    hydro_assets_path = root / "hydro_assets.csv"
    hydro_alloc_path = root / "hydro_allocations.csv"
    save_json(hydro_manifest_path, hydro["manifest"])
    hydro["assets_frame"].to_csv(hydro_assets_path, index=False)
    hydro["allocations"].to_csv(hydro_alloc_path, index=False)

    network = pypsa.Network()
    network.set_snapshots(pd.date_range("2020-01-01T00:00:00", periods=2, freq="h"))
    buses = sorted(set(catalog["existing_bus_id"]) |
                   {"B-STAR", "B-STORE", "original-bus"})
    for i, bus in enumerate(buses):
        network.add("Bus", bus, v_nom=220,
                    x=float("nan") if bus == "B-STAR" else float(4 + i),
                    y=float("nan") if bus == "B-STAR" else float(50 + i))
    for carrier in sorted(set(catalog.carrier)):
        network.add("Carrier", carrier)
    for row in catalog.to_dict("records"):
        network.add("Generator", row["existing_generator_id"],
                    bus=row["existing_bus_id"],
                    p_nom=float(row["p_nom_mw"]), carrier=row["carrier"])
    network.add("Line", "LINE-ORIGINAL-AB", bus0="B-A", bus1="B-B",
                r=.05, x=.2, s_nom=250)
    for i, bus in enumerate(["B-A", "B-B", "B-C"], start=1):
        network.add("Transformer", f"3W-ARM-{i}", bus0="B-STAR",
                    bus1=bus, s_nom=100, x=.04, r=.005)
    network.add("Transformer", "2W-ORIGINAL", bus0="B-A", bus1="B-PVU",
                s_nom=200, x=.05, r=.006)
    network.add("Load", "LOAD-CGMES-1", bus="B-A", p_set=5.0)
    network.loads_t.p_set = pd.DataFrame(
        {"LOAD-CGMES-1": [5.0, 5.5]}, index=network.snapshots)
    for row in hydro["assets_frame"].to_dict("records"):
        if row["component_class"] == "StorageUnit":
            network.add("StorageUnit", row["existing_component_id"],
                        bus=row["bus_id"], p_nom=float(row["p_nom_mw"]),
                        max_hours=float(row["max_hours"]),
                        efficiency_dispatch=float(row["efficiency_dispatch"]))
    network.add("Store", "STORE-CGMES-1", bus="B-STORE", e_nom=100)
    network.add("Link", "LINK-EXISTING-STORE", bus0="original-bus",
                bus1="B-STORE", p_nom=25, efficiency=.9)
    network_path = root / "m0_synthetic_dnr.nc"
    network.export_to_netcdf(str(network_path))

    bridge = {
        "schema": "IOSN-M1-DNR-BRIDGE/1.0.0",
        "m0_schema": "iosn-m0-detailed-network-reference/1.0.0",
        "reference_id": "FIXTURE-DNR-REFERENCE-01",
        "source_revision_id": "FIXTURE-SRC-REV-01",
        "operating_state_id": "FIXTURE-OPERATING-STATE-01",
        "canonical_revision_id": REVISION,
        "projection_id": "FIXTURE-PROJECTION-01",
        "source_set_hash": m0["source_set_hash"],
        "mapping_policy_hash": m0["mapping_policy_hash"],
        "legacy_network_revision_semantics": "EXACT_CANONICAL_REVISION_ID",
        "legacy_network_revision_id": REVISION,
    }
    bridge_path = root / "m0_identity_bridge.json"
    save_json(bridge_path, bridge)
    source_map = []
    for component, table in [
        ("Generator", network.generators), ("Load", network.loads),
        ("StorageUnit", network.storage_units), ("Store", network.stores)]:
        for id_ in table.index:
            source_map.append({
                "component_class": component, "view_id": str(id_),
                "asset_id": "FIXTURE-ASSET-" + str(id_),
                "source_entity_id": "FIXTURE-SOURCE-" + str(id_),
                "source_role": "SYNTHETIC_ONLY_SOURCE_KEY",
            })
    sidecar = {
        "schema": "iosn-m0-detailed-network-reference/1.0.0",
        "evidence_class": "SYNTHETIC_FIXTURE",
        **{key: bridge[key] for key in ("reference_id", "source_revision_id",
            "operating_state_id", "canonical_revision_id", "projection_id",
            "source_set_hash", "mapping_policy_hash")},
        "view_source_map": source_map,
        "bus_roles": {bus: "SYNTHETIC_3W_STAR" if bus == "B-STAR"
                      else "REAL" for bus in network.buses.index},
        "synthetic_three_winding": {
            "bus": "B-STAR", "source_transformer_id": "FIXTURE-ORIGINAL-3W",
            "arms": ["3W-ARM-1", "3W-ARM-2", "3W-ARM-3"],
            "country_code": None, "source_geo": None,
        },
        "m0_real_runtime_qualified": False,
    }
    sidecar_path = root / "m0_synthetic_sidecar.json"
    save_json(sidecar_path, sidecar)
    master = {
        "schema": "IOSN-M1-MA4F-MASTER/1.0.0",
        "evidence_class": "FIXTURE", "real_data_qualified": False,
        "selected_weather_ids": WEATHERS,
        "planning_horizons": [HORIZON],
        "m0_reference_id": bridge["reference_id"],
        "time_axis": {"timezone": "UTC", "interpretation": "UTC_NAIVE",
                      "snapshot_count": 2,
                      "start_utc": "2020-01-01T00:00:00",
                      "end_utc_inclusive": "2020-01-01T01:00:00"},
        "input_sha256": {},
    }
    inputpaths = {"m0_network": network_path, "m0_sidecar": sidecar_path,
                  "m0_reference_manifest": res.m0_reference_manifest,
                  "res_manifest": res.weather_manifest, "res_catalog": res.source_catalog,
                  "hydro_manifest": hydro_manifest_path, "hydro_assets": hydro_assets_path,
                  "hydro_allocations": hydro_alloc_path, "bridge": bridge_path}
    master["input_sha256"] = {key: digest(path) for key, path in inputpaths.items()}
    master_path = root / "master_manifest.json"
    save_json(master_path, master)
    config = {
        "iosn_m1_res": {
            "weather_manifest": str(res.weather_manifest),
            "source_catalog": str(res.source_catalog),
            "m0_res_registry": str(res.m0_assets),
            "m0_reference_manifest": str(res.m0_reference_manifest),
            "technology_crosswalk": str(res.technology_crosswalk),
            "asset_profile_map": str(res.assignment_map),
            "geometry_registry": str(res.geometry_registry),
            "output_dir": "results/iosn_m1/res"},
        "iosn_m1_hydro": {
            "manifest": str(hydro_manifest_path),
            "allocations": str(hydro_alloc_path),
            "assets": str(hydro_assets_path),
            "snapshots": {HORIZON: {w: str(root / "snapshots.csv")
                                   for w in WEATHERS}},
            "source_root": str(root),
        },
        "iosn_m1_compose": {
            "master_manifest": str(master_path),
            "identity_bridge": str(bridge_path),
            "m0_network": str(network_path), "m0_sidecar": str(sidecar_path),
            "m0_reference_manifest": str(res.m0_reference_manifest),
            "output_dir": "results/iosn_m1/detailed",
        },
    }
    config_path = root / "snakemake_fixture_config.yaml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")
    return {
        "root": root, "res_args": res, "hydro_case": hydro,
        "hydro_manifest": hydro_manifest_path, "hydro_assets": hydro_assets_path,
        "hydro_allocations": hydro_alloc_path, "m0_network": network_path,
        "bridge": bridge_path, "sidecar": sidecar_path, "master": master_path,
        "m0_reference_manifest": res.m0_reference_manifest,
        "res_manifest": res.weather_manifest, "res_catalog": res.source_catalog,
        "config": config_path, "weather_ids": WEATHERS, "horizon": HORIZON,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    result = build(args.out)
    print(json.dumps({k: str(v) for k, v in result.items()
                      if k not in {"hydro_case", "res_args"}},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
