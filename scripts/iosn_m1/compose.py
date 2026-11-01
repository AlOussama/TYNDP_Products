# SPDX-License-Identifier: MIT
"""MA4F: single, fail-closed PyPSA time-series composer for immutable M0 DNR.

Only synthetic FIXTURE evidence is admissible in this implementation macro.
MA2 and MA3 remain independent source compilers; only this module writes PyPSA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pypsa
import xarray as xr

SCHEMA = "IOSN-M1-MA4F-MASTER/1.0.0"
BRIDGE = "IOSN-M1-DNR-BRIDGE/1.0.0"
DNR = "iosn-m0-detailed-network-reference/1.0.0"
ALLOW = {("Generator", "p_max_pu"): "generators_t.p_max_pu",
         ("StorageUnit", "inflow"): "storage_units_t.inflow"}
HYDRO_PORTS = {"hydro_inflow": ("StorageUnit", "inflow"),
               "ror_availability": ("Generator", "p_max_pu")}
HASH_KEYS = {"m0_network", "m0_sidecar", "m0_reference_manifest",
             "res_manifest", "res_catalog", "hydro_manifest",
             "hydro_assets", "hydro_allocations", "bridge"}


class IntegrationError(ValueError):
    """Explicit rejected input, never a silently repaired gap."""


def guard(test, reason):
    if not test:
        raise IntegrationError(str(reason))


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def static_fingerprints(network):
    """Every PyPSA static component table, including empty and standard tables."""
    hashes = {}
    for name in sorted(network.all_components):
        frame = network.components[name].static
        data = {"columns": [str(c) for c in frame.columns],
                "index": [str(c) for c in frame.index],
                "dtypes": [str(t) for t in frame.dtypes],
                "values": pd.DataFrame(frame).to_json(orient="split", date_format="iso",
                                        date_unit="ns", double_precision=15)}
        hashes[name] = hashlib.sha256(
            json.dumps(data, sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()
    return hashes


def dynamic_copy(network):
    return {(comp, field): data.copy(deep=True)
            for comp in network.all_components
            for field, data in network.components[comp].dynamic.items()}


def validate_untouched_dynamics(before, network, written):
    after = dynamic_copy(network)
    for key in set(before) | set(after):
        if key in written:
            continue
        old, new = before.get(key), after.get(key)
        guard(old is not None and new is not None and old.equals(new),
              "UNAUTHORIZED_DYNAMIC_MUTATION: " + ".".join(key))


def snapshots(network, master):
    grid = network.snapshots
    guard(isinstance(grid, pd.DatetimeIndex) and grid.tz is None,
          "M0_SNAPSHOTS_MUST_BE_UTC_NAIVE_DATETIME")
    guard(grid.is_unique and grid.is_monotonic_increasing and len(grid) > 0,
          "M0_SNAPSHOT_ORDER_INVALID")
    guard(len(grid) == 1 or (grid[1:] - grid[:-1] == pd.Timedelta(hours=1)).all(),
          "M0_SNAPSHOT_HOURLY_GAP")
    axis = master["time_axis"]
    guard(axis["timezone"] == "UTC" and axis["interpretation"] == "UTC_NAIVE",
          "MASTER_TIME_AXIS_NOT_UTC")
    guard(int(axis["snapshot_count"]) == len(grid) and
          pd.Timestamp(axis["start_utc"]) == grid[0] and
          pd.Timestamp(axis["end_utc_inclusive"]) == grid[-1],
          "MASTER_M0_TIME_AXIS_MISMATCH")
    guard((network.snapshot_weightings["objective"] > 0).all(),
          "M0_SNAPSHOT_WEIGHT_INVALID")
    return grid


def verify_manifest(master, bridge, sidecar, m0, res_manifest, hydro_manifest,
                    paths, horizon, weather_id):
    guard(master.get("schema") == SCHEMA, "MASTER_SCHEMA_VERSION")
    guard(bridge.get("schema") == BRIDGE and
          bridge.get("m0_schema") == DNR, "DNR_BRIDGE_SCHEMA")
    guard(sidecar.get("schema") == DNR and
          sidecar.get("evidence_class") == "SYNTHETIC_FIXTURE",
          "M0_SIDECAR_UNQUALIFIED")
    guard(master.get("evidence_class") == "FIXTURE" and
          master.get("real_data_qualified") is False,
          "REAL_SOURCE_NOT_QUALIFIED_MA4F")
    ids = master.get("selected_weather_ids")
    guard(isinstance(ids, list) and len(ids) == 5 and len(set(ids)) == 5
          and all(isinstance(x, str) and x for x in ids),
          "MASTER_EXACT_FIVE_WEATHER_IDS")
    horizons = master.get("planning_horizons")
    guard(isinstance(horizons, list) and horizons and len(set(horizons)) == len(horizons),
          "MASTER_HORIZON_SET")
    guard(horizon in horizons and weather_id in ids,
          "UNSELECTED_SCENARIO_FORBIDDEN")
    guard(res_manifest.get("selected_weather_ids") == ids and
          hydro_manifest.get("selected_weather_ids") == ids and
          [str(x) for x in res_manifest.get("planning_horizons", [])] == horizons,
          "PRODUCER_WEATHER_OWNERSHIP_MISMATCH")
    guard(res_manifest.get("evidence_class") == "FIXTURE" and
          hydro_manifest.get("source_mode") == "FIXTURE",
          "PRODUCER_QUALITY_CLASS_MISMATCH")
    guard(bridge.get("legacy_network_revision_semantics") ==
          "EXACT_CANONICAL_REVISION_ID" and
          bridge.get("legacy_network_revision_id") ==
          bridge.get("canonical_revision_id"),
          "UNAUTHORIZED_NETWORK_REVISION_ALIAS")
    for field in ("source_revision_id", "operating_state_id",
                  "canonical_revision_id", "projection_id", "reference_id",
                  "source_set_hash", "mapping_policy_hash"):
        value = bridge.get(field)
        guard(isinstance(value, str) and bool(value), "MISSING_BRIDGE_FIELD: " + field)
        guard(sidecar.get(field) == value, "SIDECAR_BRIDGE_CONFLICT: " + field)
    for field in ("network_revision_id", "source_set_hash", "mapping_policy_hash"):
        expected = bridge["canonical_revision_id"] if field == "network_revision_id" else bridge[field]
        guard(m0.get(field) == expected and hydro_manifest.get(field) == expected,
              "PRODUCER_M0_REVISION_OR_HASH_CONFLICT: " + field)
    guard(m0.get("reference_type") == "DetailedNetworkReference_v1",
          "M0_REFERENCE_TYPE")
    guard(master.get("m0_reference_id") == bridge["reference_id"],
          "MASTER_DNR_IDENTITY_CONFLICT")
    guards = master.get("input_sha256", {})
    guard(set(guards) == HASH_KEYS, "MASTER_INPUT_HASH_COVERAGE")
    for key in sorted(HASH_KEYS):
        guard(guards[key] == sha256(paths[key]), "MASTER_SOURCE_SHA256_MISMATCH: " + key)
    guard(isinstance(sidecar.get("view_source_map"), list)
          and len(sidecar["view_source_map"]) > 0,
          "M0_SOURCE_VIEW_IDENTITY_MAP_MISSING")
    guard(isinstance(sidecar.get("bus_roles"), dict) and
          isinstance(sidecar.get("synthetic_three_winding"), dict),
          "M0_BUS_AND_THREE_WINDING_SIDECAR_MISSING")
    return ids


def validate_qa(qa_res, qa_hydro, bridge, horizon, weather_id, res_cf, hydro_manifest):
    guard(qa_res.get("netcdf_roundtrip") == "PASS" and
          qa_res.get("real_data_qualified") is False and
          qa_res.get("evidence_class") == "FIXTURE",
          "RES_QA_FIXTURE_GATE")
    guard(qa_hydro.get("source_status") == "FIXTURE_ONLY" and
          qa_hydro.get("source_mode") == "FIXTURE" and
          qa_hydro.get("network_mutation_count") == 0 and
          qa_hydro.get("zero_fallback_count") == 0,
          "HYDRO_QA_FIXTURE_GATE")
    for qa in (qa_res, qa_hydro):
        guard(qa["planning_horizon"] == horizon and
              qa["weather_id"] == weather_id and
              qa["network_revision_id"] == bridge["canonical_revision_id"],
              "PRODUCER_OUTPUT_SCENARIO_OR_REVISION_CONFLICT")
    guard(qa_res["netcdf_sha256"] == sha256(res_cf),
          "RES_OUTPUT_SHA256_MISMATCH")
    calculated = hashlib.sha256(json.dumps(
        hydro_manifest, sort_keys=True).encode("utf-8")).hexdigest()
    guard(qa_hydro["manifest_sha256"] == calculated,
          "HYDRO_OUTPUT_MANIFEST_HASH_MISMATCH")


def _validate_identity(sidecar, network):
    ids = {}
    for row in sidecar["view_source_map"]:
        key = (row["component_class"], row["view_id"])
        guard(key not in ids and row.get("source_entity_id") and row.get("asset_id"),
              "M0_SOURCE_VIEW_ID_DUPLICATE_OR_UNPROVEN")
        table = network.components[row["component_class"]].static
        guard(row["view_id"] in table.index,
              "M0_SOURCE_VIEW_TARGET_NOT_IN_NETWORK: " + str(key))
        ids[key] = row
    for name in ("Generator", "StorageUnit", "Store", "Load"):
        for target in network.components[name].static.index:
            guard((name, target) in ids, "M0_IDENTITY_LEDGER_INCOMPLETE: " + name + ":" + target)
    roles = sidecar["bus_roles"]
    guard(set(network.buses.index) == set(roles), "M0_BUS_ROLE_COVERAGE")
    for bus, role in roles.items():
        guard(role in {"REAL", "SYNTHETIC_3W_STAR"}, "M0_UNSUPPORTED_BUS_ROLE")
        if role == "SYNTHETIC_3W_STAR":
            x, y = network.buses.at[bus, "x"], network.buses.at[bus, "y"]
            # PyPSA 1.4 NetCDF import materializes missing geometry as 0,0
            # defaults. These are SERIALIZATION PLACEHOLDERS, never geo evidence.
            guard((pd.isna(x) and pd.isna(y)) or
                  (float(x) == 0.0 and float(y) == 0.0),
                  "M0_SYNTHETIC_STAR_HAS_NONPLACEHOLDER_GEOGRAPHY")
    star = sidecar["synthetic_three_winding"]
    guard(star.get("bus") in roles and roles[star["bus"]] == "SYNTHETIC_3W_STAR",
          "M0_3W_STAR_NOT_DECLARED")
    guard(star.get("source_geo") is None and star.get("country_code") is None,
          "M0_STAR_SIDECAR_FABRICATED_ORIGIN")
    guard(len(star.get("arms", [])) == 3 and
          set(star["arms"]) <= set(network.transformers.index),
          "M0_3W_ORIGINAL_ARMS_NOT_WITNESSED")
    for arm in star["arms"]:
        guard(star["bus"] in {network.transformers.at[arm, "bus0"],
                             network.transformers.at[arm, "bus1"]},
              "M0_3W_TRANSFORMER_ARM_NOT_AT_STAR")
    return ids, roles


def _checked_frame(path, name):
    guard(Path(path).is_file(), "MISSING_PRODUCER_OUTPUT: " + name)
    return pd.read_csv(path, keep_default_na=False)


def collect_targets(res_cf, hydro_dir, grid, bridge, horizon, weather_id):
    targets = []
    with xr.open_dataset(res_cf) as ds:
        guard(ds.attrs.get("contract_id") == "IOSN-M1-MA2-1.0.0" and
              ds.attrs.get("network_revision_id") == bridge["canonical_revision_id"] and
              ds.attrs.get("source_set_hash") == bridge["source_set_hash"] and
              ds.attrs.get("mapping_policy_hash") == bridge["mapping_policy_hash"] and
              ds.attrs.get("planning_horizon") == horizon and
              ds.attrs.get("weather_id") == weather_id and
              ds.attrs.get("time_basis") == "UTC_NAIVE_PROVENANCE_UTC",
              "RES_PROFILE_HEADER_IDENTITY_OR_TIME")
        guard(set(ds.data_vars) == {"renewable_cf"} and
              set(ds["renewable_cf"].dims) == {"time", "existing_generator_id"},
              "RES_NETCDF_TARGET_SCHEMA")
        times = pd.DatetimeIndex(ds.time.values)
        guard(times.equals(grid), "RES_SNAPSHOT_AXIS_MISMATCH")
        ids = [str(a) for a in ds.existing_generator_id.values]
        guard(len(ids) > 0 and len(ids) == len(set(ids)),
              "RES_GENERATOR_ID_DUPLICATE_OR_EMPTY")
        values = ds["renewable_cf"].transpose("time", "existing_generator_id").values
        guard(np.isfinite(values).all() and
              (values >= 0).all() and (values <= 1).all(), "RES_CF_INVALID")
        for j, target in enumerate(ids):
            targets.append(("Generator", "p_max_pu", target,
                            values[:, j].astype(float), "MA2_RES"))
    for fname, expected in HYDRO_PORTS.items():
        df = _checked_frame(Path(hydro_dir) / (fname + ".csv"), fname)
        if df.empty:
            continue
        guard({"utc_naive_timestamp", "existing_hydro_id",
               "target_attribute", "value"} <= set(df.columns),
              "HYDRO_OUTPUT_SCHEMA: " + fname)
        component, attribute = expected
        guard(df["target_attribute"].eq(ALLOW[expected]).all(),
              "HYDRO_WRONG_TARGET_ATTRIBUTE")
        guard(not df.duplicated(["utc_naive_timestamp", "existing_hydro_id"]).any(),
              "HYDRO_DUPLICATE_TARGET_TIME")
        for target, part in df.groupby("existing_hydro_id"):
            dates = pd.DatetimeIndex(pd.to_datetime(part.utc_naive_timestamp))
            guard(dates.tz is None and dates.is_unique and set(dates) == set(grid),
                  "HYDRO_UTC_SNAPSHOT_COVERAGE")
            values = pd.to_numeric(part.value, errors="raise").to_numpy(dtype=float)
            order = dates.argsort()
            guard(dates[order].equals(grid) and np.isfinite(values).all() and
                  (values >= 0).all(), "HYDRO_SNAPSHOT_OR_VALUE_INVALID")
            if component == "Generator":
                guard((values <= 1).all(), "ROR_AVAILABILITY_NOT_PU")
            targets.append((component, attribute, str(target),
                            values[order], "MA3_HYDRO"))
    staged = _checked_frame(Path(hydro_dir) / "store_link_staged.csv", "store_link_staged")
    guard(staged.empty, "STORE_LINK_STAGED_REQUIRES_SEPARATE_M0_OWNER_CONSENT_NO_WRITE")
    guard(len(targets) > 0, "NO_SOURCE_TARGETS")
    return targets


def apply_targets(network, identity, roles, targets):
    written, ownership = set(), []
    occupied = set()
    for comp, attr, target, values, producer in targets:
        key = (comp, attr, target)
        guard(key not in occupied, "PRODUCER_TARGET_COLLISION: " + str(key))
        occupied.add(key)
        guard((comp, attr) in ALLOW and (comp, target) in identity,
              "TARGET_NOT_IN_ALLOWLIST_OR_M0_IDENTITY: " + str(key))
        table = network.components[comp].static
        guard(target in table.index, "PYPSA_ORIGINAL_ID_NOT_FOUND: " + str(key))
        bus = str(table.at[target, "bus"])
        guard(roles.get(bus) == "REAL", "SOURCE_ASSIGNED_TO_SYNTHETIC_3W_BUS")
        existing = network.components[comp].dynamic[attr]
        guard(target not in existing.columns,
              "EXISTING_PROFILE_OVERWRITE_FORBIDDEN: " + str(key))
        guard(len(values) == len(network.snapshots),
              "TARGET_SNAPSHOT_LENGTH")
        ownership.append({"component": comp, "attribute": attr,
                          "target_id": target, "owner": producer,
                          "source_entity_id": identity[(comp, target)]["source_entity_id"],
                          "source_asset_id": identity[(comp, target)]["asset_id"]})
    # No writes until *all* scenarios, IDs, conflicts and overwrites pass.
    for comp, attr, target, values, _ in targets:
        component = network.components[comp]
        frame = component.dynamic[attr].copy()
        if frame.empty and len(frame.index) == 0:
            frame = pd.DataFrame(index=network.snapshots)
        guard(frame.index.equals(network.snapshots), "EXISTING_DYNAMIC_INDEX_MISMATCH")
        frame[target] = values
        component.dynamic[attr] = frame
        written.add((comp, attr))
    return written, ownership


def _roundtrip(network, original_fingerprint, original_weights,
               target_values, outfile, before_load):
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".nc", dir=outfile.parent, delete=False) as tmp:
        staged = Path(tmp.name)
    try:
        network.export_to_netcdf(str(staged))
        copied = pypsa.Network(str(staged))
        guard(pd.DatetimeIndex(copied.snapshots).equals(network.snapshots),
              "PYPSA_NETCDF_SNAPSHOT_ROUNDTRIP")
        guard(copied.snapshot_weightings.equals(original_weights),
              "PYPSA_NETCDF_SNAPSHOT_WEIGHTS_CHANGED")
        # Each static table is compared by its complete, canonical fingerprint.
        # The serializer may otherwise mask source topology changes by reordering.
        rt_fingerprint = static_fingerprints(copied)
        guard(rt_fingerprint == original_fingerprint,
              "PYPSA_NETCDF_STATIC_COMPONENT_ROUNDTRIP_MISMATCH")
        guard(copied.loads_t.p_set.equals(before_load),
              "PYPSA_NETCDF_LOAD_PROFILE_ROUNDTRIP_MISMATCH")
        for comp, attr, target, values, _ in target_values:
            out = copied.components[comp].dynamic[attr]
            guard(target in out.columns and out.index.equals(copied.snapshots),
                  "PYPSA_NETCDF_DYNAMIC_TARGET_MISSING")
            np.testing.assert_allclose(out[target].to_numpy(dtype=float), values,
                                       rtol=0, atol=1e-12)
        guard(not outfile.exists(), "REFUSE_EXISTING_OUTPUT_NETCDF")
        os.replace(staged, outfile)
    finally:
        staged.unlink(missing_ok=True)


def compose(*, m0_network, m0_sidecar, m0_reference_manifest,
            bridge_path, master_path, res_manifest_path, res_catalog,
            hydro_manifest_path, hydro_assets, hydro_allocations,
            res_cf, hydro_dir, res_qa, hydro_qa,
            horizon, weather_id, output_network):
    paths = {"m0_network": Path(m0_network), "m0_sidecar": Path(m0_sidecar),
             "m0_reference_manifest": Path(m0_reference_manifest),
             "res_manifest": Path(res_manifest_path), "res_catalog": Path(res_catalog),
             "hydro_manifest": Path(hydro_manifest_path),
             "hydro_assets": Path(hydro_assets), "hydro_allocations": Path(hydro_allocations),
             "bridge": Path(bridge_path)}
    master, bridge = load_json(master_path), load_json(bridge_path)
    sidecar, m0 = load_json(m0_sidecar), load_json(m0_reference_manifest)
    res_manifest, hydro_manifest = load_json(res_manifest_path), load_json(hydro_manifest_path)
    verify_manifest(master, bridge, sidecar, m0, res_manifest,
                    hydro_manifest, paths, horizon, weather_id)
    validate_qa(load_json(res_qa), load_json(hydro_qa), bridge,
                horizon, weather_id, res_cf, hydro_manifest)
    network = pypsa.Network(str(m0_network))
    grid = snapshots(network, master)
    identity, roles = _validate_identity(sidecar, network)
    static_before = static_fingerprints(network)
    dynamic_before = dynamic_copy(network)
    weights = network.snapshot_weightings.copy(deep=True)
    loads_before = network.loads_t.p_set.copy(deep=True)
    targets = collect_targets(res_cf, hydro_dir, grid, bridge, horizon, weather_id)
    written, ledger = apply_targets(network, identity, roles, targets)
    guard(static_fingerprints(network) == static_before, "M0_STATIC_INVARIANCE_VIOLATED")
    guard(network.snapshot_weightings.equals(weights), "SNAPSHOT_WEIGHTING_MUTATED")
    guard(network.loads_t.p_set.equals(loads_before), "M0_EXISTING_LOADS_OVERWRITTEN")
    validate_untouched_dynamics(dynamic_before, network, written)
    guard(static_fingerprints(network) == static_before, "M0_STATIC_CHANGED_AFTER_QA")
    _roundtrip(network, static_before, weights, targets, Path(output_network),
               loads_before)
    return {
        "status": "M1_MA4F_FIXTURE_INTEGRATION_QUALIFIED",
        "evidence_class": "SYNTHETIC_FIXTURE",
        "real_data_qualified": False,
        "m2_release": False, "planning_horizon": horizon,
        "weather_id": weather_id, "weather_id_count": 5,
        "m0_reference_id": bridge["reference_id"],
        "canonical_revision_id": bridge["canonical_revision_id"],
        "projection_id": bridge["projection_id"],
        "m0_static_component_count": len(static_before),
        "m0_static_fingerprints_before": static_before,
        "m0_static_fingerprints_after": static_fingerprints(network),
        "static_invariance": "PASS_ALL_COMPONENT_TABLES",
        "loads_t_p_set_preserved": True,
        "snapshot_count": len(grid), "dynamic_targets": len(targets),
        "target_ownership": ledger, "staged_store_link_written": 0,
        "output_netcdf_sha256": sha256(output_network),
        "producer_inputs_sha256": {"res_cf": sha256(res_cf),
                                   "hydro_qa": sha256(hydro_qa)},
        "python_version": platform.python_version(),
        "pypsa_version": pypsa.__version__,
        "pandas_version": pd.__version__,
        "xarray_version": xr.__version__,
    }


def parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ("m0-network", "m0-sidecar", "m0-reference-manifest",
                 "bridge-path", "master-path", "res-manifest-path", "res-catalog",
                 "hydro-manifest-path", "hydro-assets", "hydro-allocations",
                 "res-cf", "hydro-dir", "res-qa", "hydro-qa", "horizon",
                 "weather-id", "output-network", "output-qa"):
        p.add_argument("--" + flag, required=True)
    return p.parse_args(argv)


def main(argv=None):
    args = vars(parse(argv))
    output_qa = Path(args.pop("output_qa"))
    output_network = args.pop("output_network")
    try:
        report = compose(**args, output_network=output_network)
    except Exception as exc:
        output_qa.parent.mkdir(parents=True, exist_ok=True)
        output_qa.write_text(json.dumps({
            "status": "M1_MA4F_REPAIRS_REQUIRED", "real_data_qualified": False,
            "m2_release": False, "reason": type(exc).__name__ + ": " + str(exc)},
            indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise
    output_qa.parent.mkdir(parents=True, exist_ok=True)
    output_qa.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
