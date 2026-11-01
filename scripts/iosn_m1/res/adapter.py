# SPDX-License-Identifier: MIT
"""IoSN M1 MA2: strict PECD source -> original M0 generator ID adapter.

The TYNDP 2026 Date/Hour (1..24), WSxxx and technology conventions are
adapted from Open-TYNDP at 71a3a9a15b77114cd79458bceabc98e1a64dd58a
(MIT). No TYNDP busmap, weather fallback, or upstream gap filling is used.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

RENEWABLES = {"Wind_Onshore", "Wind_Offshore", "Solar PV Utility", "Solar PV Rooftop"}
METHODS = {"EXPLICIT_SOURCE_ID", "VERIFIED_PLANT_LOCATION_WITH_OFFICIAL_PECD_MASK",
           "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE",
           "CAPACITY_WEIGHTED_COMPOSITE_WITH_DOCUMENTED_MW_SHARES"}
SPATIAL = {"ORIG", "PEON", "P2ON", "PEOF", "P2OF", "NUT2", "SZON", "TYNDP_NODE", "OTHER_EXPLICIT"}
SHA = re.compile(r"^[0-9a-fA-F]{64}$")


class ContractError(ValueError):
    """A reproducible fail-closed contract violation, not a recoverable gap."""


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise ContractError(f"{code}: {detail}")


def digest(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def csv_table(path: str | Path, fields: set[str], label: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype="string", keep_default_na=False)
    require(fields <= set(df.columns), "SCHEMA_FIELDS", f"{label}: {sorted(fields - set(df.columns))}")
    require(not df.empty, "EMPTY_TABLE", label)
    return df


def text_value(v) -> str:
    return "" if pd.isna(v) else str(v).strip()


def positive(v, name: str) -> float:
    try:
        number = float(v)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"INVALID_NUMBER: {name}={v}") from exc
    require(np.isfinite(number) and number > 0, "NONPOSITIVE_CAPACITY", name)
    return number


def validate_manifest(manifest: dict, weather_id: str, horizon: str) -> None:
    ids = manifest.get("selected_weather_ids")
    require(isinstance(ids, list) and len(ids) == 5 and all(isinstance(x, str) and x for x in ids)
            and len(set(ids)) == 5, "FIVE_WEATHER_IDS_REQUIRED")
    require(weather_id in ids, "UNSELECTED_WEATHER_ID", weather_id)
    require(horizon in [str(x) for x in manifest.get("planning_horizons", [])],
            "UNDECLARED_HORIZON", horizon)
    require(manifest.get("evidence_class") in {"FIXTURE", "REAL_SOURCE_CANDIDATE"},
            "EVIDENCE_CLASS_UNDECLARED")
    require(manifest.get("time_semantics") == "HOURLY_UTC_NAIVE_OUTPUT",
            "TIME_POLICY_UNQUALIFIED")
    if manifest["evidence_class"] != "FIXTURE":
        require(manifest.get("full_native_year_required") is True,
                "REAL_YEAR_INTEGRITY_REQUIRED")


def validate_m0(assets_path: Path, reference_manifest_path: Path) -> tuple[pd.DataFrame, dict]:
    m0 = json.loads(reference_manifest_path.read_text(encoding="utf-8"))
    required = {"reference_type", "network_revision_id", "source_set_hash",
                "mapping_policy_hash", "asset_registry_sha256", "identity_ledger_ref", "sidecar_ref"}
    require(required <= set(m0), "M0_REFERENCE_INCOMPLETE", str(required - set(m0)))
    require(m0["reference_type"] == "DetailedNetworkReference_v1", "M0_REFERENCE_TYPE")
    require(SHA.fullmatch(m0["asset_registry_sha256"]) is not None and
            m0["asset_registry_sha256"].lower() == digest(assets_path), "M0_ASSET_HASH")
    for key in ("network_revision_id", "source_set_hash", "mapping_policy_hash",
                "identity_ledger_ref", "sidecar_ref"):
        require(bool(text_value(m0[key])), "M0_MISSING_PROVENANCE", key)
    fields = {"network_revision_id", "asset_id", "existing_generator_id", "existing_bus_id",
              "carrier", "p_nom_mw", "bus_role", "geo_quality", "technology_variant",
              "res_profile_required"}
    df = csv_table(assets_path, fields, "m0_asset_registry")
    require(df["network_revision_id"].eq(m0["network_revision_id"]).all(), "M0_REVISION_MISMATCH")
    for key in ("asset_id", "existing_generator_id"):
        require(df[key].str.len().gt(0).all() and df[key].is_unique, "M0_DUPLICATE_OR_EMPTY_ID", key)
    require(df["existing_bus_id"].str.len().gt(0).all(), "M0_EMPTY_BUS")
    require(df["res_profile_required"].isin(["true", "false"]).all(),
            "M0_RES_SCOPE_FLAG_REQUIRED")
    require(int(m0.get("generator_count", -1)) == len(df), "M0_GENERATOR_LEDGER_INCOMPLETE")
    m0["total_generator_count"] = len(df)
    df = df[df["res_profile_required"].eq("true")].copy()
    require(not df.empty, "M0_RES_TARGETS_EMPTY")
    df["p_nom_mw"] = [positive(v, "p_nom_mw") for v in df["p_nom_mw"]]
    require(~df["bus_role"].eq("SYNTHETIC_3W_STAR").any(), "SYNTHETIC_GENERATOR_BUS")
    return df, m0


def validate_crosswalk(assets: pd.DataFrame, path: Path) -> pd.DataFrame:
    cross = csv_table(path, {"m0_carrier", "technology_variant", "pecd_carrier", "upstream_ref"},
                      "technology_crosswalk")
    require(not cross.duplicated(["m0_carrier", "technology_variant"]).any(), "DUPLICATE_TECH_CROSSWALK")
    require(cross["technology_variant"].isin(RENEWABLES).all(), "CROSSWALK_TECH_UNSUPPORTED")
    for a in assets.to_dict("records"):
        rows = cross[cross["m0_carrier"].eq(a["carrier"])]
        require(not rows.empty, "UNKNOWN_M0_CARRIER", a["existing_generator_id"])
        variant = text_value(a["technology_variant"])
        if not variant:
            require(len(rows) == 1, "AMBIGUOUS_GENERATOR_TECH", a["existing_generator_id"])
            variant = str(rows.iloc[0]["technology_variant"])
            assets.loc[assets["existing_generator_id"].eq(a["existing_generator_id"]),
                       "technology_variant"] = variant
        require(((rows["technology_variant"] == variant) &
                 (rows["pecd_carrier"] == variant)).any(), "CARRIER_TECH_MISMATCH", a["existing_generator_id"])
    return assets


def read_catalog(path: Path, manifest: dict, horizon: str) -> pd.DataFrame:
    fields = {"planning_horizon", "weather_id", "source_profile_id", "technology_variant",
              "spatial_level", "region_id", "source_format", "file_path", "source_sha256",
              "source_dataset_id", "source_dataset_version", "corrected_dataset_revision",
              "license", "source_evidence_ref", "source_time_basis", "calendar_year",
              "weather_column", "source_unit", "geometry_ref", "spatial_source_crs"}
    df = csv_table(path, fields, "source_catalog")
    df = df.loc[df["planning_horizon"].eq(horizon)].copy()
    require(not df.empty, "HORIZON_SOURCES_NOT_PROVIDED", horizon)
    require(df["technology_variant"].isin(RENEWABLES).all() and
            df["spatial_level"].isin(SPATIAL).all(), "UNKNOWN_SOURCE_TECH_OR_LEVEL")
    require(not df.duplicated(["planning_horizon", "weather_id", "source_profile_id"]).any(),
            "DUPLICATE_SOURCE_KEY")
    require(df["weather_id"].isin(manifest["selected_weather_ids"]).all(), "UNKNOWN_WEATHER_IN_CATALOG")
    ids = set(manifest["selected_weather_ids"])
    profiles = df.groupby("source_profile_id", sort=True)
    for name, group in profiles:
        require(set(group["weather_id"]) == ids, "INCOMPLETE_FIVE_SET_SOURCE", str(name))
        for column in ("technology_variant", "spatial_level", "region_id", "source_unit", "geometry_ref"):
            require(group[column].nunique() == 1, "CHANGING_PROFILE_DEFINITION", f"{name}: {column}")
    for r in df.to_dict("records"):
        require(all(text_value(r[k]) for k in ("source_profile_id", "region_id", "source_dataset_id",
                "source_dataset_version", "corrected_dataset_revision", "license", "source_evidence_ref",
                "source_time_basis", "file_path")), "MISSING_SOURCE_PROVENANCE", str(r["source_profile_id"]))
        if manifest["evidence_class"] != "FIXTURE":
            for field in ("license", "source_evidence_ref", "corrected_dataset_revision"):
                require(not text_value(r[field]).upper().startswith(("UNKNOWN", "NOT_PROVIDED", "FIXTURE")),
                        "REAL_SOURCE_PROVENANCE_UNQUALIFIED", field)
        require(SHA.fullmatch(text_value(r["source_sha256"])) is not None,
                "SOURCE_HASH_UNDECLARED", str(r["source_profile_id"]))
        require(r["source_dataset_version"].startswith("4.2"), "NOT_PECD_V42", str(r["source_profile_id"]))
        if r["technology_variant"].startswith("Wind"):
            require(r["source_unit"] == "MW_per_MW", "WIND_UNIT_INVALID")
        else:
            require(r["source_unit"] in {"MW_per_MWp", "MW_per_MW_AC"}, "PV_UNIT_INVALID")
        if r["spatial_level"] in {"PEOF", "P2OF"}:
            require(r["technology_variant"] == "Wind_Offshore", "OFFSHORE_PRODUCT_TECH_MISMATCH")
        if r["technology_variant"] == "Wind_Offshore":
            require(r["spatial_level"] in {"PEOF", "P2OF", "OTHER_EXPLICIT", "TYNDP_NODE"},
                    "OFFSHORE_SPATIAL_LEVEL_INVALID")
    return df


def _utc_index(dates: pd.Series, source_time_basis: str) -> pd.DatetimeIndex:
    # Never silently resolve DST ambiguous or nonexistent times. Offset-bearing ISO is authoritative.
    s = dates.astype(str)
    aware = s.str.contains(r"(?:Z|[+-]\d{2}:?\d{2})$", regex=True)
    require(aware.all() or (~aware).all(), "MIXED_TIMEZONE_AWARENESS")
    if aware.all():
        idx = pd.DatetimeIndex(pd.to_datetime(s, utc=True, errors="raise"))
    else:
        naive = pd.DatetimeIndex(pd.to_datetime(s, errors="raise"))
        require(naive.tz is None, "TIME_FORMAT_MIXED")
        require(bool(source_time_basis), "SOURCE_TIMEZONE_MISSING")
        idx = naive.tz_localize(source_time_basis, ambiguous="raise", nonexistent="raise").tz_convert("UTC")
    return idx.tz_localize(None)


def read_profile(row: dict, catalog_path: Path, enforce_full_year: bool) -> pd.Series:
    f = Path(str(row["file_path"]))
    if not f.is_absolute():
        f = catalog_path.parent / f
    require(f.is_file(), "SOURCE_FILE_NOT_FOUND", str(f))
    require(digest(f).lower() == str(row["source_sha256"]).lower(), "SOURCE_SHA256_MISMATCH", str(f))
    source_format = str(row["source_format"])
    skiprows = 10 if source_format == "TYNDP_RAW10_DATE_HOUR" else 0
    raw = pd.read_csv(f, dtype={"Date": str}, skiprows=skiprows)
    basis = text_value(row["source_time_basis"])
    require(basis in {"UTC", "Europe/Berlin"}, "SOURCE_TIMEZONE_UNSUPPORTED", basis)
    if source_format in {"TYNDP_DATE_HOUR", "TYNDP_RAW10_DATE_HOUR"}:
        require({"Date", "Hour", str(row["weather_column"])} <= set(raw.columns),
                "PECD_DATE_HOUR_WS_MISSING", str(f))
        parts = raw["Date"].str.extract(r"^\s*(\d{1,2})\.(\d{1,2})\.?\s*$")
        require(parts.notna().all().all(), "DATE_HOUR_DATE_FORMAT", str(f))
        hour = pd.to_numeric(raw["Hour"], errors="raise")
        require(hour.notna().all() and hour.between(1, 24).all() and (hour % 1 == 0).all(),
                "DATE_HOUR_RANGE", str(f))
        yr = int(row["calendar_year"])
        naive = pd.to_datetime({"year": yr, "month": parts[1].astype(int),
                                "day": parts[0].astype(int), "hour": hour.astype(int) - 1}, errors="raise")
        idx = _utc_index(naive.astype(str), basis)
        value_col = str(row["weather_column"])
        require(re.fullmatch(r"WS\d{3}", value_col) is not None,
                "INVALID_WS_COLUMN", value_col)
    elif source_format == "ISO_CSV":
        require({"time", "cf"} <= set(raw.columns), "ISO_SOURCE_FIELDS", str(f))
        idx = _utc_index(raw["time"], basis)
        value_col = "cf"
    else:
        raise ContractError(f"UNKNOWN_SOURCE_FORMAT: {source_format}")
    values = pd.to_numeric(raw[value_col], errors="raise").astype(float).to_numpy()
    require(len(idx) > 0 and len(idx) == len(values), "EMPTY_OR_BAD_TIME_SERIES")
    require(np.isfinite(values).all(), "SOURCE_NA_OR_INFINITY", str(f))
    require((values >= -1e-12).all() and (values <= 1 + 1e-12).all(),
            "SOURCE_CF_OUT_OF_DOMAIN", str(f))
    # No silent clipping, even for machine-rounding excursions.
    require((values >= 0).all() and (values <= 1).all(), "SOURCE_CF_OUT_OF_RANGE", str(f))
    require(idx.is_monotonic_increasing and idx.is_unique, "TIME_DUPLICATE_OR_UNSORTED", str(f))
    require(len(idx) == 1 or (idx[1:] - idx[:-1] == pd.Timedelta(hours=1)).all(),
            "TIME_GAP_OR_NONHOURLY", str(f))
    if enforce_full_year:
        year = int(row["calendar_year"])
        start = pd.Timestamp(year=year, month=1, day=1)
        expected = pd.date_range(start, pd.Timestamp(year=year + 1, month=1, day=1),
                                 freq="h", inclusive="left")
        require(idx.equals(expected), "INCOMPLETE_NATIVE_YEAR", str(f))
    return pd.Series(values, index=idx, name=str(row["source_profile_id"]))


def _spatial_match(asset: pd.Series, entry: pd.Series, method: str, geometry: dict | None) -> None:
    if method == "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE":
        require(asset["technology_variant"] != "Wind_Offshore", "OFFSHORE_LANDFALL_PROXY")
    require(geometry is not None, "OFFICIAL_REGION_MASK_REQUIRED")
    from shapely.geometry import Point, shape
    from pyproj import Transformer
    source = geometry.get("features", [])
    profile = str(entry.name)
    matches = [feat for feat in source if feat.get("properties", {}).get("source_profile_id") == profile]
    require(len(matches) == 1, "MASK_PROFILE_MISSING_OR_DUPLICATE", profile)
    feat = matches[0]
    props = feat.get("properties", {})
    require(props.get("spatial_level") == entry["spatial_level"] and
            props.get("technology_variant") == entry["technology_variant"] and
            props.get("source_evidence_ref"), "MASK_METADATA_MISMATCH", profile)
    require(props.get("crs") == "EPSG:4326" and entry["spatial_source_crs"] == "EPSG:4326",
            "MASK_CRS_NOT_WITNESSED", profile)
    if method == "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE":
        require(asset["technology_variant"] != "Wind_Offshore", "OFFSHORE_LANDFALL_PROXY")
        require(asset["bus_role"] == "ORIGINAL" and
                str(asset.get("bus_location_verified_for_plant", "")).lower() == "true",
                "UNVERIFIED_BUS_PROXY", str(asset.name))
        prefix = "bus"
    else:
        prefix = "plant"
    for col in (f"{prefix}_lon", f"{prefix}_lat", f"{prefix}_crs"):
        require(col in asset and text_value(asset[col]), "ASSET_LOCATION_MISSING", col)
    crs = text_value(asset[f"{prefix}_crs"])
    require(crs.startswith("EPSG:"), "ASSET_CRS_UNQUALIFIED", crs)
    x, y = float(asset[f"{prefix}_lon"]), float(asset[f"{prefix}_lat"])
    require(np.isfinite([x, y]).all(), "ASSET_COORD_INVALID")
    lon, lat = Transformer.from_crs(crs, "EPSG:4326", always_xy=True).transform(x, y)
    require(-180 <= lon <= 180 and -90 <= lat <= 90, "COORD_OUT_OF_BOUNDS")
    point = Point(lon, lat)
    covering = [f for f in source if f.get("properties", {}).get("technology_variant") == entry["technology_variant"]
                and f.get("properties", {}).get("spatial_level") == entry["spatial_level"]
                and shape(f["geometry"]).covers(point)]
    require(len(covering) == 1 and covering[0]["properties"]["source_profile_id"] == profile,
            "AMBIGUOUS_OR_WRONG_REGION", str(asset.name))


def validate_assignment(assets: pd.DataFrame, catalog: pd.DataFrame, assignment_path: Path,
                        horizon: str, geometry_path: Path | None) -> tuple[pd.DataFrame, dict]:
    fields = {"network_revision_id", "planning_horizon", "asset_id", "existing_generator_id",
              "existing_bus_id", "source_profile_id", "technology_variant", "spatial_level",
              "spatial_assignment_method", "geo_quality", "mapping_weight", "segment_capacity",
              "capacity_basis", "source_evidence_ref"}
    assignments = csv_table(assignment_path, fields, "asset_profile_map")
    assignments = assignments.loc[assignments["planning_horizon"].eq(horizon)].copy()
    require(not assignments.empty, "HORIZON_ASSIGNMENTS_NOT_PROVIDED", horizon)
    require(not assignments.duplicated(["existing_generator_id", "source_profile_id"]).any(),
            "DUPLICATE_PROFILE_ASSIGNMENT")
    require(assignments["spatial_assignment_method"].isin(METHODS).all(), "ASSIGNMENT_METHOD_INVALID")
    require(assignments["geo_quality"].str.len().gt(0).all() and
            assignments["source_evidence_ref"].str.len().gt(0).all(), "ASSIGNMENT_EVIDENCE_MISSING")
    require(set(assignments["existing_generator_id"]) == set(assets["existing_generator_id"]),
            "UNMAPPED_OR_FOREIGN_M0_GENERATOR")
    source = catalog.drop_duplicates("source_profile_id").set_index("source_profile_id")
    require(set(assignments["source_profile_id"]) <= set(source.index), "UNKNOWN_SOURCE_PROFILE")
    geometry = json.loads(geometry_path.read_text(encoding="utf-8")) if geometry_path else None
    if geometry is not None:
        require(geometry.get("type") == "FeatureCollection", "MASK_GEOJSON_INVALID")
    assets_by_id = assets.set_index("existing_generator_id")
    assignments["mapping_weight"] = pd.to_numeric(assignments["mapping_weight"], errors="raise")
    assignments["segment_capacity"] = pd.to_numeric(assignments["segment_capacity"], errors="raise")
    require(np.isfinite(assignments[["mapping_weight", "segment_capacity"]].to_numpy(dtype=float)).all(),
            "ASSIGNMENT_NONFINITE")
    audit = {"geo_methods": {}, "offshore_landing_proxy_rejected_by_contract": True}
    for gid, group in assignments.groupby("existing_generator_id", sort=True):
        asset = assets_by_id.loc[gid]
        require(group["asset_id"].eq(asset["asset_id"]).all() and
                group["existing_bus_id"].eq(asset["existing_bus_id"]).all() and
                group["network_revision_id"].eq(asset["network_revision_id"]).all(),
                "M0_ID_OR_BUS_MISMATCH", str(gid))
        require(group["technology_variant"].eq(asset["technology_variant"]).all(),
                "ASSIGNMENT_TECH_MISMATCH", str(gid))
        weights = group["mapping_weight"].astype(float)
        require((weights > 0).all() and np.isclose(weights.sum(), 1, atol=1e-10, rtol=0),
                "MW_WEIGHT_SUM_NOT_ONE", str(gid))
        if len(group) > 1:
            require(group["spatial_assignment_method"].eq(
                "CAPACITY_WEIGHTED_COMPOSITE_WITH_DOCUMENTED_MW_SHARES").all(),
                "UNVERIFIED_MULTI_REGION_GROUP", str(gid))
        for _, row in group.iterrows():
            entry = source.loc[row["source_profile_id"]]
            require(row["spatial_level"] == entry["spatial_level"] and
                    row["technology_variant"] == entry["technology_variant"],
                    "ASSIGNMENT_SOURCE_METADATA_MISMATCH", str(gid))
            method = str(row["spatial_assignment_method"])
            audit["geo_methods"][method] = audit["geo_methods"].get(method, 0) + 1
            if method in {"VERIFIED_PLANT_LOCATION_WITH_OFFICIAL_PECD_MASK",
                          "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE"}:
                _spatial_match(asset, entry, method, geometry)
            elif method == "CAPACITY_WEIGHTED_COMPOSITE_WITH_DOCUMENTED_MW_SHARES":
                require(row["segment_capacity"] > 0 and row["capacity_basis"] in {"AC_MW", "DC_MWp"},
                        "MW_SHARE_EVIDENCE_MISSING", str(gid))
            # Any single explicit source ID requires an evidence reference; supplied above.
            if asset["technology_variant"] == "Wind_Offshore":
                require(method != "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE", "OFFSHORE_LANDFALL_PROXY")
        if group["spatial_assignment_method"].eq(
                "CAPACITY_WEIGHTED_COMPOSITE_WITH_DOCUMENTED_MW_SHARES").any():
            basis = "DC_MWp" if str(asset["technology_variant"]).startswith("Solar") else "AC_MW"
            cap = (positive(asset["pv_dc_mwp"], "pv_dc_mwp") if basis == "DC_MWp"
                   else float(asset["p_nom_mw"]))
            require(group["capacity_basis"].eq(basis).all() and
                    np.isclose(group["segment_capacity"].sum(), cap, rtol=1e-6, atol=1e-7) and
                    np.allclose(group["segment_capacity"] / cap, weights, atol=1e-9, rtol=0),
                    "MW_SHARE_CAPACITY_MISMATCH", str(gid))
    return assignments, audit


def compile_scenario(assets: pd.DataFrame, catalog: pd.DataFrame, assignments: pd.DataFrame,
                     catalog_path: Path, horizon: str, weather_id: str, full_year: bool,
                     m0: dict, geo_audit: dict) -> tuple[xr.Dataset, pd.DataFrame, dict]:
    subset = catalog[catalog["weather_id"].eq(weather_id)]
    sources = {}
    records = []
    source_index = None
    for row in subset.to_dict("records"):
        series = read_profile(row, catalog_path, full_year)
        if source_index is None:
            source_index = series.index
        require(series.index.equals(source_index), "SOURCE_TIME_AXIS_MISMATCH", str(row["source_profile_id"]))
        sources[row["source_profile_id"]] = series
        records.append({"source_profile_id": row["source_profile_id"], "weather_id": weather_id,
                        "planning_horizon": horizon, "source_file": row["file_path"],
                        "source_sha256": row["source_sha256"], "source_dataset_id": row["source_dataset_id"],
                        "dataset_version": row["source_dataset_version"], "correction": row["corrected_dataset_revision"],
                        "license": row["license"], "unit": row["source_unit"],
                        "spatial_level": row["spatial_level"], "first_utc": series.index[0].isoformat(),
                        "last_utc": series.index[-1].isoformat(), "count": len(series)})
    require(bool(sources), "NO_SOURCE_PROFILES")
    asset_order = list(assets["existing_generator_id"])
    matrix = np.empty((len(source_index), len(asset_order)), dtype=float)
    lookup = catalog.drop_duplicates("source_profile_id").set_index("source_profile_id")
    clipped = {}
    for j, gid in enumerate(asset_order):
        asset = assets[assets["existing_generator_id"].eq(gid)].iloc[0]
        group = assignments[assignments["existing_generator_id"].eq(gid)]
        source_units = {lookup.loc[pid, "source_unit"] for pid in group["source_profile_id"]}
        require(len(source_units) == 1, "MIXED_PROFILE_UNIT_BASE", str(gid))
        unit = next(iter(source_units))
        cf = sum(float(row["mapping_weight"]) * sources[row["source_profile_id"]].to_numpy()
                 for row in group.to_dict("records"))
        count = 0
        if str(asset["technology_variant"]).startswith("Solar"):
            if unit == "MW_per_MWp":
                for field in ("pv_dc_mwp", "pv_ac_mw", "pv_clipping_policy",
                              "pv_conversion_evidence_ref", "pv_source_ac_semantics"):
                    require(field in asset and text_value(asset[field]), "PV_AC_DC_EVIDENCE_MISSING", field)
                require(np.isclose(positive(asset["pv_ac_mw"], "pv_ac_mw"),
                                   float(asset["p_nom_mw"]), rtol=1e-7, atol=1e-8),
                        "PV_AC_M0_CAPACITY_MISMATCH", str(gid))
                require(asset["pv_clipping_policy"] == "CLIP_AC_AT_P_NOM_WITH_APPROVED_EVIDENCE" and
                        asset["pv_source_ac_semantics"] == "UNCLIPPED_DC_NORMALIZED",
                        "PV_CLIPPING_NOT_QUALIFIED", str(gid))
                cf = cf * positive(asset["pv_dc_mwp"], "pv_dc_mwp") / float(asset["p_nom_mw"])
                count = int((cf > 1).sum())
                cf = np.minimum(cf, 1.0)
            else:
                require(unit == "MW_per_MW_AC" and text_value(asset.get("pv_conversion_evidence_ref")),
                        "PV_AC_SOURCE_SEMANTICS_UNPROVEN", str(gid))
        else:
            require(unit == "MW_per_MW", "WIND_BASE_MISMATCH", str(gid))
        require(np.isfinite(cf).all() and (cf >= 0).all() and (cf <= 1).all(),
                "OUTPUT_CF_OUT_OF_BOUNDS", str(gid))
        matrix[:, j] = cf
        clipped[str(gid)] = count
    ds = xr.Dataset({"renewable_cf": (("time", "existing_generator_id"), matrix)},
                    coords={"time": source_index, "existing_generator_id": asset_order})
    ds.attrs.update({"contract_id": "IOSN-M1-MA2-1.0.0", "network_revision_id": m0["network_revision_id"],
                     "source_set_hash": m0["source_set_hash"], "mapping_policy_hash": m0["mapping_policy_hash"],
                     "planning_horizon": str(horizon), "weather_id": weather_id,
                     "time_basis": "UTC_NAIVE_PROVENANCE_UTC", "semantics": "CAPACITY_FACTOR_NOT_DISPATCH",
                     "source_resolution": "NATIVE_PECD_NO_SPATIAL_INTERPOLATION"})
    covered_mw = float(assets["p_nom_mw"].sum())
    qa = {"status": "FIXTURE_PASS_OR_REAL_SOURCE_CANDIDATE_NOT_FINAL_GATE", "network_revision_id": m0["network_revision_id"],
          "planning_horizon": horizon, "weather_id": weather_id, "existing_generator_count": len(asset_order), "m0_total_generator_count": m0["total_generator_count"],
          "mapped_generator_count": len(asset_order), "mapped_mw": covered_mw,
          "unmapped_mw": 0.0, "source_profile_count": len(sources), "hours": len(source_index),
          "utc_start": source_index[0].isoformat(), "utc_last": source_index[-1].isoformat(),
          "pv_explicit_clipped_hours": clipped, "assignment_audit": geo_audit,
          "m0_static_tables_written": [], "target_attribute": "generators_t.p_max_pu"}
    return ds, pd.DataFrame.from_records(records), qa
