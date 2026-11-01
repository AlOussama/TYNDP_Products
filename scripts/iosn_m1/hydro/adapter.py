# SPDX-License-Identifier: MIT
"""MA3 hydro adapter: immutable asset binding and source-interval energy conservation.

No electrical network is constructed or mutated here. This code is original;
Open-TYNDP tyndp-2026 @ 71a3a9a was reviewed, not copied.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

CONTRACT = "IOSN-M1-MA3/1.0.0"
TYPES = {"HRR", "HRI", "HPI", "HOL", "HCL"}
SEMANTICS = {
    "STORAGE_ENERGY_EQUIVALENT_MWH",
    "AVAILABLE_GENERATION_ENERGY_MWH",
    "HYDRAULIC_ENERGY_MWH",
}
ATTRIBUTES = {
    "StorageUnit": "storage_units_t.inflow",
    "Generator": "generators_t.p_max_pu",
    "Store": "generators_t.p_set",  # approved EXISTING port, STAGED only
}
EPS = 1e-8


class HydroContractError(ValueError):
    """Fail-closed contract violation."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise HydroContractError(message)


def nonempty(value: object, field: str) -> str:
    require(value is not None and str(value).strip() not in ("", "nan", "None"),
            "Missing required " + field)
    return str(value).strip()


def numeric(value: object, label: str, *, zero_ok: bool = True) -> float:
    try:
        result = float(value)
    except (ValueError, TypeError) as exc:
        raise HydroContractError("Non-numeric " + label) from exc
    require(math.isfinite(result) and (result >= 0 if zero_ok else result > 0),
            "Invalid nonnegative value: " + label)
    return result


def aware_utc(value: object, zone: str, label: str) -> pd.Timestamp:
    """Accept only explicit UTC offsets; validate against the declared IANA zone."""
    raw = nonempty(value, label)
    try:
        instant = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        require(instant.tzinfo is not None and instant.utcoffset() is not None,
                "Timezone offset missing in " + label)
        in_zone = instant.astimezone(ZoneInfo(zone))
        require(in_zone.replace(tzinfo=None) == instant.replace(tzinfo=None)
                and in_zone.utcoffset() == instant.utcoffset(),
                "Offset/zone inconsistency in " + label)
        return pd.Timestamp(instant).tz_convert("UTC")
    except (ValueError, KeyError) as exc:
        if isinstance(exc, HydroContractError):
            raise
        raise HydroContractError("Invalid timezone/timestamp in " + label + ": " + raw) from exc


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_snapshots(path: Path) -> pd.DataFrame:
    rows = pd.read_csv(path, keep_default_na=False)
    require({"timestamp", "duration_hours"} <= set(rows.columns),
            "Snapshot file must provide timestamp and duration_hours")
    require(len(rows) > 0, "No snapshots")
    timestamps = [aware_utc(t, "UTC", "snapshot timestamp")
                  for t in rows["timestamp"]]
    durations = [numeric(v, "snapshot duration", zero_ok=False)
                 for v in rows["duration_hours"]]
    require(all(abs(h - 1.0) < EPS for h in durations),
            "Only complete hourly UTC snapshots are accepted")
    result = pd.DataFrame({"time": timestamps, "hours": durations})
    require(result.time.is_unique and result.time.is_monotonic_increasing,
            "Unsorted or duplicate UTC snapshots")
    result["end"] = result.time + pd.to_timedelta(result.hours, unit="h")
    require(all(result.time.iloc[i + 1] == result.end.iloc[i]
                for i in range(len(result) - 1)),
            "Missing or overlapping hourly snapshots")
    return result


def read_native_intervals(source: dict, root: Path) -> pd.DataFrame:
    relative = nonempty(source.get("path"), "source.path")
    source_path = Path(relative)
    require(not source_path.is_absolute() and ".." not in source_path.parts,
            "Source path must be relative and contained in the source root")
    source_path = (root / source_path).resolve()
    require(source_path.is_relative_to(root.resolve()), "Source path escape")
    require(source_path.is_file(), "Physical source missing: " + relative)
    expected = nonempty(source.get("sha256"), "source.sha256").lower()
    require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected),
            "Invalid source SHA256")
    actual = file_sha256(source_path)
    require(actual == expected, "Source SHA256 mismatch: " + relative)
    table = pd.read_csv(source_path, keep_default_na=False)
    require({"start", "end", "energy_mwh"} <= set(table.columns) and len(table) > 0,
            "Missing native source intervals: " + relative)
    zone = nonempty(source.get("timezone"), "source.timezone")
    try:
        ZoneInfo(zone)
    except (KeyError, ValueError) as exc:
        raise HydroContractError("Unknown IANA timezone: " + zone) from exc
    start = [aware_utc(v, zone, "native start") for v in table["start"]]
    end = [aware_utc(v, zone, "native end") for v in table["end"]]
    energy = [numeric(v, "native interval energy") for v in table["energy_mwh"]]
    require(all(a < b for a, b in zip(start, end)), "Nonpositive native interval")
    for k in range(len(start) - 1):
        require(end[k] == start[k + 1], "Native interval gap, overlap or disorder")
    hours = [(b - a).total_seconds() / 3600 for a, b in zip(start, end)]
    resolution = nonempty(source.get("resolution"), "source.resolution")
    require(resolution in {"DAY", "WEEK"}, "Unsupported native resolution")
    max_hours = 25.0 if resolution == "DAY" else 169.0
    require(all(EPS < h <= max_hours + EPS for h in hours),
            "Native interval duration inconsistent with DAY/WEEK")
    return pd.DataFrame({"start": start, "end": end,
                         "energy_mwh": energy, "hours": hours})


def validate_manifest(manifest: dict, root: Path, horizon: str) -> dict:
    require(manifest.get("contract") == CONTRACT, "Hydro contract mismatch")
    for field in ("network_revision_id", "source_set_hash", "mapping_policy_hash"):
        nonempty(manifest.get(field), field)
    mode = manifest.get("source_mode")
    require(mode in {"FIXTURE", "REAL"}, "source_mode must be FIXTURE or REAL")
    weather_ids = manifest.get("selected_weather_ids")
    require(isinstance(weather_ids, list) and len(weather_ids) == 5
            and len(set(weather_ids)) == 5
            and all(isinstance(w, str) and w.strip() for w in weather_ids),
            "Five distinct, externally selected weather IDs are mandatory")
    sources = [s for s in manifest.get("sources", [])
               if str(s.get("planning_horizon")) == horizon]
    require(sources, "No sources for requested planning horizon")
    catalog = {}
    areas_by_weather = {}
    for source in sources:
        for field in ("source_id", "source_dataset_id", "source_dataset_version",
                      "corrected_dataset_revision", "source_uri", "license",
                      "source_evidence_ref", "hydro_area_id"):
            nonempty(source.get(field), field)
        weather = nonempty(source.get("weather_id"), "weather_id")
        tech = nonempty(source.get("hydro_tech"), "hydro_tech")
        require(weather in weather_ids, "Unselected weather ID in source")
        require(tech in TYPES - {"HCL"}, "HCL cannot be assigned natural inflow")
        require(source.get("unit") == "MWh", "Native source energy must be MWh")
        require(source.get("semantics") in SEMANTICS,
                "Source must distinguish energy-equivalent, hydraulic and generation")
        require(source.get("temporal_distribution_policy") == "UNIFORM_WITHIN_NATIVE_INTERVAL",
                "Explicit uniform native-interval temporal policy required")
        nonempty(source.get("temporal_policy_evidence_ref"), "temporal policy evidence")
        key = (weather, source["hydro_area_id"], tech)
        require(key not in catalog, "Duplicate source per weather/area/type: " + str(key))
        catalog[key] = (source, read_native_intervals(source, root))
        areas_by_weather.setdefault(weather, set()).add(key[1:])
    required_areas = areas_by_weather[weather_ids[0]]
    require(required_areas, "No required hydro source-area/type pairs")
    require(all(areas_by_weather.get(w) == required_areas for w in weather_ids),
            "Five weather sets do not cover identical hydro area/type pairs")
    return catalog


def validate_assets(assets: pd.DataFrame, revision: str) -> dict:
    fields = {"asset_id", "existing_component_id", "component_class",
              "hydro_tech", "bus_id", "network_revision_id", "role",
              "p_nom_mw", "max_hours", "efficiency_dispatch", "e_nom_mwh"}
    require(fields <= set(assets.columns), "Incomplete M0 identity/asset inventory")
    result = {}
    require(assets.asset_id.is_unique, "Duplicate M0 asset_id")
    require(not assets.duplicated(["component_class", "existing_component_id"]).any(),
            "Duplicate existing PyPSA component")
    for row in assets.to_dict("records"):
        require(row["network_revision_id"] == revision, "M0 revision mismatch")
        require(row["component_class"] in {"Generator", "StorageUnit", "Store"},
                "Unsupported M0 component class")
        require(row["hydro_tech"] in TYPES, "Unknown M0 hydro type")
        require(row["role"] in {"HYDRO_ASSET", "INFLOW_PORT"}, "Unknown asset role")
        for field in ("asset_id", "existing_component_id", "bus_id"):
            nonempty(row[field], "M0 " + field)
        if row["component_class"] in {"Generator", "StorageUnit"}:
            numeric(row["p_nom_mw"], "existing p_nom", zero_ok=False)
        if row["component_class"] == "StorageUnit":
            numeric(row["max_hours"], "existing max_hours", zero_ok=False)
            eff = numeric(row["efficiency_dispatch"], "existing discharge efficiency", zero_ok=False)
            require(eff <= 1, "Invalid efficiency_dispatch")
        if row["component_class"] == "Store":
            numeric(row["e_nom_mwh"], "existing e_nom_mwh", zero_ok=False)
        result[row["asset_id"]] = row
    return result


def validate_allocations(alloc: pd.DataFrame, assets: dict, catalog: dict,
                         horizon: str, revision: str) -> dict:
    fields = {"planning_horizon", "network_revision_id", "hydro_area_id", "hydro_tech",
              "asset_id", "share", "mapping_basis", "evidence_ref",
              "conversion_factor", "conversion_evidence_ref",
              "port_generator_id", "port_approval_ref", "allowlist_approved"}
    require(fields <= set(alloc.columns), "Incomplete hydro allocation schema")
    alloc = alloc.loc[alloc.planning_horizon.astype(str) == horizon]
    require(len(alloc) > 0, "No hydro allocations")
    coverage = {(zone, tech) for _, zone, tech in catalog}
    mapping = {}
    for row in alloc.to_dict("records"):
        area = nonempty(row["hydro_area_id"], "allocation area")
        tech = nonempty(row["hydro_tech"], "allocation technology")
        require((area, tech) in coverage, "Allocation not in hydro source catalog")
        require(row["network_revision_id"] == revision, "Allocation M0 revision mismatch")
        asset_id = nonempty(row["asset_id"], "allocation asset_id")
        require(asset_id in assets, "Mapping must use existing M0 asset_id")
        asset = assets[asset_id]
        require(asset["role"] == "HYDRO_ASSET" and asset["hydro_tech"] == tech,
                "Hydro technology or role mismatch")
        require(row["mapping_basis"] in {"HYDROLOGICAL_BASIN", "TSO_APPROVED_SHARE"},
                "Bus coordinates are not a hydrological basin mapping")
        nonempty(row["evidence_ref"], "hydrological evidence")
        share = numeric(row["share"], "hydro allocation share", zero_ok=False)
        require(share <= 1 + EPS, "Share exceeds one")
        factor = numeric(row["conversion_factor"], "energy conversion", zero_ok=False)
        require(factor <= 1 + EPS, "Energy conversion gain requires separate physics")
        nonempty(row["conversion_evidence_ref"], "conversion evidence")
        if asset["component_class"] == "Generator":
            require(tech == "HRR", "Only qualified RoR may use Generator availability")
        elif asset["component_class"] == "Store":
            require(row["allowlist_approved"] == "YES"
                    and nonempty(row["port_approval_ref"], "Store/Link port approval"),
                    "Store/Link requires explicit additional attribute permission")
            port = nonempty(row["port_generator_id"], "Store/Link inflow Generator port")
            matches = [a for a in assets.values()
                       if a["existing_component_id"] == port
                       and a["component_class"] == "Generator"
                       and a["role"] == "INFLOW_PORT"]
            require(len(matches) == 1 and matches[0]["bus_id"] == asset["bus_id"],
                    "Approved inflow Generator port absent or on a different store bus")
        else:
            require(tech in {"HRR", "HRI", "HPI", "HOL"},
                    "StorageUnit inflow technology mismatch")
        mapping.setdefault((area, tech), []).append((row, asset))
    require(set(mapping) == coverage, "Missing hydro basin allocation(s)")
    for key, items in mapping.items():
        shares = [float(row["share"]) for row, _ in items]
        require(abs(math.fsum(shares) - 1) < EPS,
                "Source allocation shares must sum to 1: " + str(key))
        require(len({asset["asset_id"] for _, asset in items}) == len(items),
                "Duplicate basin-to-asset allocation")
    return mapping


def verify_m0_real_network(network_path: str | None, sidecar_path: str | None,
                           assets: dict, manifest: dict) -> None:
    require(network_path and sidecar_path, "REAL mode requires M0 network and sidecar")
    sidecar = json.loads(Path(sidecar_path).read_text(encoding="utf-8"))
    for field in ("network_revision_id", "source_set_hash", "mapping_policy_hash"):
        require(sidecar.get(field) == manifest[field], "REAL M0 sidecar " + field + " mismatch")
    require(bool(sidecar.get("identity_mapping")) and
            bool(sidecar.get("component_support_matrix")),
            "REAL M0 sidecar identity/capability witness missing")
    try:
        import pypsa
    except ImportError as exc:
        raise HydroContractError("REAL M0 verification requires PyPSA") from exc
    network = pypsa.Network(network_path)
    tables = {"Generator": network.generators, "StorageUnit": network.storage_units,
              "Store": network.stores}
    for asset in assets.values():
        table = tables[asset["component_class"]]
        name = asset["existing_component_id"]
        require(name in table.index, "M0 PyPSA component missing: " + name)
        require(str(table.loc[name, "bus"]) == asset["bus_id"],
                "M0 electrical connection mismatch: " + name)
        if asset["component_class"] in {"Generator", "StorageUnit"}:
            require(math.isclose(float(table.loc[name, "p_nom"]),
                                 float(asset["p_nom_mw"]), abs_tol=EPS),
                    "M0 rated MW mismatch: " + name)
        if asset["component_class"] == "Store":
            require(math.isclose(float(table.loc[name, "e_nom"]),
                                 float(asset["e_nom_mwh"]), abs_tol=EPS),
                    "M0 Store energy capacity mismatch")
    witness = manifest.get("real_witness", {})
    require(witness.get("ma1c_status") == "M1_SOURCE_CONTRACT_WITNESSED"
            and witness.get("m0_status") == "M0_REFERENCE_QUALIFIED"
            and bool(witness.get("evidence_commit")),
            "Independent MA1C/M0 source witness missing in REAL mode")


def execute(manifest: dict, allocations: pd.DataFrame, assets_frame: pd.DataFrame,
            snapshots: pd.DataFrame, root: Path, planning_horizon: str,
            weather_id: str, *, network_path: str | None = None,
            sidecar_path: str | None = None) -> dict[str, pd.DataFrame | dict]:
    """Produce dynamic attributes and audit ledgers, without mutating M0."""
    catalog = validate_manifest(manifest, root, planning_horizon)
    require(weather_id in manifest["selected_weather_ids"], "Unselected weather ID")
    revision = manifest["network_revision_id"]
    assets = validate_assets(assets_frame, revision)
    mapping = validate_allocations(allocations, assets, catalog, planning_horizon, revision)
    if manifest["source_mode"] == "REAL":
        verify_m0_real_network(network_path, sidecar_path, assets, manifest)
    closed = {v["asset_id"] for v in assets.values()
              if v["hydro_tech"] == "HCL" and v["role"] == "HYDRO_ASSET"}
    declarations = manifest.get("closed_loop_no_natural_inflow", [])
    declared = {d.get("asset_id") for d in declarations
                if d.get("policy") == "NO_NATURAL_INFLOW_BY_DESIGN"
                and d.get("evidence_ref")}
    require(closed == declared, "HCL requires complete evidenced no-inflow declarations")
    mapped_assets = {asset["asset_id"] for items in mapping.values() for _, asset in items}
    required_assets = {v["asset_id"] for v in assets.values()
                       if v["role"] == "HYDRO_ASSET" and v["hydro_tech"] != "HCL"}
    require(required_assets == mapped_assets,
            "Unmapped non-HCL hydro asset(s) or extraneous asset")

    grid = snapshots
    require(len(grid) > 0, "No target snapshots")
    records = []
    native_ledger = []
    allocated_ledger = []
    for (ws, area, tech), (source, intervals) in catalog.items():
        if ws != weather_id:
            continue
        shares = mapping[(area, tech)]
        for ordinal, native in enumerate(intervals.to_dict("records"), start=1):
            begin, finish = native["start"], native["end"]
            selected = grid.loc[(grid.time >= begin) & (grid.end <= finish)]
            require(len(selected) > 0, "Source interval has no corresponding target snapshots")
            duration = math.fsum(selected.hours)
            require(abs(duration - native["hours"]) < EPS,
                    "Native source interval not exactly covered by hourly UTC snapshots")
            source_energy = native["energy_mwh"]
            allocated_source = math.fsum(source_energy * float(r["share"]) for r, _ in shares)
            require(math.isclose(allocated_source, source_energy,
                                 rel_tol=1e-10, abs_tol=EPS),
                    "Native source allocation energy is not conserved")
            native_ledger.append({
                "planning_horizon": planning_horizon, "weather_id": weather_id,
                "source_id": source["source_id"], "source_sha256": source["sha256"],
                "hydro_area_id": area, "hydro_tech": tech,
                "native_interval_ordinal": ordinal,
                "native_start_utc": begin.isoformat(), "native_end_utc": finish.isoformat(),
                "native_duration_h": native["hours"], "source_energy_mwh": source_energy,
                "allocated_native_mwh": allocated_source, "snapshot_count": len(selected),
                "snapshot_coverage_hours": duration,
                "source_energy_residual_mwh": allocated_source - source_energy,
                "temporal_distribution_policy": source["temporal_distribution_policy"],
                "temporal_policy_evidence_ref": source["temporal_policy_evidence_ref"],
                "hourly_values_are_observations": False,
            })
            for row, asset in shares:
                share = float(row["share"])
                factor = float(row["conversion_factor"])
                semantics = source["semantics"]
                cls = asset["component_class"]
                if cls == "Generator":
                    require(semantics == "AVAILABLE_GENERATION_ENERGY_MWH"
                            or semantics == "HYDRAULIC_ENERGY_MWH",
                            "RoR Generator requires available generation energy, not raw reservoir inflow")
                else:
                    require(semantics == "STORAGE_ENERGY_EQUIVALENT_MWH"
                            or semantics == "HYDRAULIC_ENERGY_MWH",
                            "Stored natural inflow cannot be generation output")
                if semantics == "HYDRAULIC_ENERGY_MWH":
                    require(row["conversion_evidence_ref"] != "IDENTITY",
                            "Hydraulic->model energy requires documented conversion")
                else:
                    require(abs(factor - 1) < EPS,
                            "Do not apply hidden conversion to already modeled energy")
                incoming = source_energy * share
                modeled = incoming * factor
                power = modeled / native["hours"]
                if cls == "Store":
                    target_id = row["port_generator_id"]
                    attr = ATTRIBUTES["Store"]
                    require(power <= float(next(a["p_nom_mw"] for a in assets.values()
                                 if a["existing_component_id"] == target_id
                                 and a["role"] == "INFLOW_PORT")) + EPS,
                            "Store/Link inflow port capacity exceeded")
                else:
                    target_id = asset["existing_component_id"]
                    attr = ATTRIBUTES[cls]
                if cls == "Generator":
                    require(power <= float(asset["p_nom_mw"]) + EPS,
                            "Available RoR power exceeds unchanged Generator.p_nom")
                for time in selected.time:
                    records.append({
                        "time": time, "asset_id": asset["asset_id"],
                        "component_class": cls, "existing_hydro_id": target_id,
                        "target_attribute": attr, "inflow_mw": power,
                        "source_id": source["source_id"], "source_interval_ordinal": ordinal,
                    })
                integrated = math.fsum(power * h for h in selected.hours)
                require(math.isclose(integrated, modeled, rel_tol=1e-10, abs_tol=EPS),
                        "Plant energy integral mismatch")
                allocated_ledger.append({
                    "planning_horizon": planning_horizon, "weather_id": weather_id,
                    "source_id": source["source_id"], "hydro_area_id": area,
                    "hydro_tech": tech, "native_interval_ordinal": ordinal,
                    "asset_id": asset["asset_id"], "existing_hydro_id": target_id,
                    "component_class": cls, "target_attribute": attr,
                    "mapping_basis": row["mapping_basis"], "evidence_ref": row["evidence_ref"],
                    "allocation_share": share, "source_energy_mwh": source_energy,
                    "allocated_native_mwh": incoming,
                    "conversion_factor": factor, "conversion_evidence_ref": row["conversion_evidence_ref"],
                    "model_energy_mwh": modeled, "integrated_model_mwh": integrated,
                    "energy_balance_residual_mwh": integrated - modeled,
                    "native_start_utc": begin.isoformat(), "native_end_utc": finish.isoformat(),
                })
    require(records, "No hydro output for requested weather")
    frame = pd.DataFrame(records)
    grouped = (frame.groupby(["time", "asset_id", "component_class", "existing_hydro_id",
                               "target_attribute"], as_index=False, sort=True)
                    .inflow_mw.sum())
    require((grouped.inflow_mw >= 0).all(), "Negative computed inflow")
    all_times = set(grid.time)
    for asset_id in required_assets:
        require(set(grouped.loc[grouped.asset_id == asset_id, "time"]) == all_times,
                "Hourly asset inflow incomplete: " + asset_id)
    frame = grouped.rename(columns={"inflow_mw": "value"})
    frame["utc_naive_timestamp"] = frame.time.dt.tz_convert("UTC").dt.tz_localize(None)
    su = frame.loc[frame.component_class == "StorageUnit"].copy()
    sl = frame.loc[frame.component_class == "Store"].copy()
    ror = frame.loc[frame.component_class == "Generator"].copy()
    if len(ror):
        pnom = {a["asset_id"]: float(a["p_nom_mw"]) for a in assets.values()}
        ror["value"] = [v / pnom[a] for a, v in zip(ror.asset_id, ror.value)]
        require((ror.value <= 1 + EPS).all(), "RoR p_max_pu > 1")
    su, sl, ror = [
        f.drop(columns=["time"]).sort_values(
            ["utc_naive_timestamp", "existing_hydro_id"]
        ).reset_index(drop=True)
        for f in (su, sl, ror)
    ]
    closed_rows = [{"asset_id": d["asset_id"], "policy": d["policy"],
                    "evidence_ref": d["evidence_ref"], "value": "NOT_APPLICABLE_NO_NATURAL_INFLOW"}
                   for d in declarations]
    qa = {
        "contract": CONTRACT, "planning_horizon": planning_horizon,
        "weather_id": weather_id, "network_revision_id": revision,
        "source_mode": manifest["source_mode"],
        "source_status": ("FIXTURE_ONLY" if manifest["source_mode"] == "FIXTURE"
                          else "REAL_WITNESSED_CANDIDATE_REQUIRES_MA4_REVIEW"),
        "selected_weather_count": len(manifest["selected_weather_ids"]),
        "source_files_in_full_catalog": len(catalog),
        "native_intervals_checked": len(native_ledger),
        "allocated_plant_intervals_checked": len(allocated_ledger),
        "existing_hydro_assets_covered": len(required_assets) + len(closed),
        "zero_fallback_count": 0, "network_mutation_count": 0,
        "temporal_accuracy": "UNIFORM_ALLOCATED_ENERGY_NOT_OBSERVED_HOURLY",
        "manifest_sha256": hashlib.sha256(
            json.dumps(manifest, sort_keys=True).encode("utf-8")).hexdigest(),
        "pypsa_utc_timezone": "UTC_NAIVE", "non_default_store_link_ports_staged": len(sl) > 0,
    }
    return {
        "hydro_inflow": su, "ror_availability": ror, "store_link_staged": sl,
        "interval_energy_ledger": pd.DataFrame(native_ledger),
        "hydro_allocation_ledger": pd.DataFrame(allocated_ledger),
        "closed_loop_policy_ledger": pd.DataFrame(closed_rows,
            columns=["asset_id", "policy", "evidence_ref", "value"]),
        "qa": qa,
    }


def write_outputs(result: dict, output_dir: Path) -> None:
    require(not output_dir.exists() or not any(output_dir.iterdir()),
            "Output directory must be absent or empty to avoid stale data")
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, value in result.items():
        if key == "qa":
            (output_dir / "qa.json").write_text(
                json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        else:
            value.to_csv(output_dir / (key + ".csv"), index=False)
