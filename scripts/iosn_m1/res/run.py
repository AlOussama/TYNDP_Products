# SPDX-License-Identifier: MIT
"""Scenario-specific, fail-closed MA2 CLI; emits no edited M0 network."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from scripts.iosn_m1.res.adapter import (
    ContractError, compile_scenario, digest, read_catalog, require,
    validate_assignment, validate_crosswalk, validate_m0, validate_manifest,
)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("weather_manifest", "source_catalog", "m0_assets", "m0_reference_manifest",
                 "technology_crosswalk", "assignment_map", "output_cf", "output_source_ledger",
                 "output_assignment_ledger", "output_profile_catalog", "output_qa"):
        p.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    p.add_argument("--geometry-registry", type=Path)
    p.add_argument("--horizon", required=True)
    p.add_argument("--weather-id", required=True)
    return p.parse_args(argv)


def atomic_write_csv(df: pd.DataFrame, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".csv",
                                     dir=target.parent, delete=False) as tmp:
        staging = Path(tmp.name)
    try:
        df.to_csv(staging, index=False)
        os.replace(staging, target)
    finally:
        staging.unlink(missing_ok=True)


def atomic_write_json(payload: dict, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json",
                                     dir=target.parent, delete=False) as tmp:
        staging = Path(tmp.name)
    try:
        staging.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(staging, target)
    finally:
        staging.unlink(missing_ok=True)


def execute(args):
    weather_manifest = json.loads(args.weather_manifest.read_text(encoding="utf-8"))
    horizon, weather_id = str(args.horizon), str(args.weather_id)
    validate_manifest(weather_manifest, weather_id, horizon)
    assets, m0 = validate_m0(args.m0_assets, args.m0_reference_manifest)
    assets = validate_crosswalk(assets, args.technology_crosswalk)
    catalog = read_catalog(args.source_catalog, weather_manifest, horizon)
    assignments, geo_audit = validate_assignment(assets, catalog, args.assignment_map,
                                                  horizon, args.geometry_registry)
    ds, source_ledger, qa = compile_scenario(assets, catalog, assignments, args.source_catalog,
                                              horizon, weather_id,
                                              weather_manifest["evidence_class"] != "FIXTURE",
                                              m0, geo_audit)
    qa["evidence_class"] = weather_manifest["evidence_class"]
    qa["m0_reference_manifest_sha256"] = digest(args.m0_reference_manifest)
    qa["m0_asset_registry_sha256"] = digest(args.m0_assets)
    qa["weather_manifest_sha256"] = digest(args.weather_manifest)
    qa["assignment_map_sha256"] = digest(args.assignment_map)
    qa["source_catalog_sha256"] = digest(args.source_catalog)
    qa["real_data_qualified"] = False  # Requires MA1C witness and M0 independently qualified input.
    qa["source_qualification_gate"] = "MA1C_AND_REAL_M0_REQUIRED"
    # Stage, roundtrip, then publish. Never touch M0 network, asset table, p_nom or bus.
    args.output_cf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".nc", dir=args.output_cf.parent, delete=False) as tmp:
        nc_stage = Path(tmp.name)
    try:
        ds.to_netcdf(nc_stage, engine="scipy")
        with xr.open_dataset(nc_stage) as rt:
            require(rt.sizes == ds.sizes and
                    np.array_equal(rt["existing_generator_id"].values,
                                   ds["existing_generator_id"].values) and
                    np.array_equal(rt["time"].values, ds["time"].values) and
                    np.array_equal(rt["renewable_cf"].values, ds["renewable_cf"].values),
                    "NETCDF_ROUNDTRIP_MISMATCH")
        qa["netcdf_roundtrip"] = "PASS"
        qa["netcdf_sha256"] = digest(nc_stage)
        # All validations completed before publishing deliverables.
        os.replace(nc_stage, args.output_cf)
    finally:
        nc_stage.unlink(missing_ok=True)
    mapping_ledger = assignments.copy()
    mapping_ledger["m0_source_set_hash"] = m0["source_set_hash"]
    mapping_ledger["m0_mapping_policy_hash"] = m0["mapping_policy_hash"]
    mapping_ledger["weather_id"] = weather_id
    mapping_ledger["p_nom_mw_read_only"] = mapping_ledger["existing_generator_id"].map(
        assets.set_index("existing_generator_id")["p_nom_mw"])
    mapping_ledger["source_sha256"] = mapping_ledger["source_profile_id"].map(
        catalog[catalog["weather_id"].eq(weather_id)].set_index("source_profile_id")["source_sha256"])
    atomic_write_csv(source_ledger, args.output_source_ledger)
    atomic_write_csv(mapping_ledger, args.output_assignment_ledger)
    atomic_write_csv(catalog[catalog["weather_id"].eq(weather_id)], args.output_profile_catalog)
    qa["result_files"] = {"renewable_cf": str(args.output_cf),
                          "source_ledger": str(args.output_source_ledger),
                          "assignment_ledger": str(args.output_assignment_ledger),
                          "profile_catalog": str(args.output_profile_catalog)}
    atomic_write_json(qa, args.output_qa)
    return qa


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        execute(args)
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError) as e:
        atomic_write_json({"status": "BLOCKED", "reason": str(e), "real_data_qualified": False},
                          args.output_qa)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
