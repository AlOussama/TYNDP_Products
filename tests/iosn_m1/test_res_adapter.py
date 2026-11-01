# SPDX-License-Identifier: MIT
"""MA2 synthetic data only: no generated fixture is a real PECD/M0 witness."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from scripts.iosn_m1.res.adapter import (
    ContractError, _utc_index, digest, read_catalog, read_profile, validate_assignment,
    validate_crosswalk, validate_m0, validate_manifest,
)
from scripts.iosn_m1.res.run import parse_args, execute, main

WEATHERS = [f"FIXTURE_WS_{i}" for i in range(1, 6)]
HORIZON = "2030"
UPSTREAM = "open-tyndp@71a3a9a15b77114cd79458bceabc98e1a64dd58a"
ROOT = Path(__file__).resolve().parents[2]


def make_fixture(tmp_path):
    base = tmp_path
    assets = pd.DataFrame([
        dict(network_revision_id="M0-FIXTURE-REV", asset_id="A-ON-1", existing_generator_id="G-CGMES-ON1",
             existing_bus_id="B-A", carrier="onwind", technology_variant="Wind_Onshore", p_nom_mw=100,
             bus_role="ORIGINAL", geo_quality="PLANT_GEO_WITNESSED", plant_lon=9.25, plant_lat=48.75,
             plant_crs="EPSG:4326"),
        dict(network_revision_id="M0-FIXTURE-REV", asset_id="A-ON-2", existing_generator_id="G-CGMES-ON2",
             existing_bus_id="B-B", carrier="onwind", technology_variant="Wind_Onshore", p_nom_mw=120,
             bus_role="ORIGINAL", geo_quality="PLANT_GEO_WITNESSED", plant_lon=9.26, plant_lat=48.75,
             plant_crs="EPSG:4326"),
        dict(network_revision_id="M0-FIXTURE-REV", asset_id="A-OFF", existing_generator_id="G-CGMES-OFF",
             existing_bus_id="B-LANDFALL", carrier="offwind-r", technology_variant="Wind_Offshore", p_nom_mw=300,
             bus_role="ORIGINAL", geo_quality="OFFSHORE_PLANT_LOCATION", plant_lon=5, plant_lat=55,
             plant_crs="EPSG:4326", bus_lon=8.0, bus_lat=54.0, bus_crs="EPSG:4326"),
        dict(network_revision_id="M0-FIXTURE-REV", asset_id="A-PVU", existing_generator_id="G-CGMES-PVU",
             existing_bus_id="B-PVU", carrier="solar", technology_variant="Solar PV Utility", p_nom_mw=50,
             bus_role="ORIGINAL", geo_quality="PLANT_GEO_WITNESSED", plant_lon=9.25, plant_lat=48.75,
             plant_crs="EPSG:4326", pv_dc_mwp=65, pv_ac_mw=50,
             pv_clipping_policy="CLIP_AC_AT_P_NOM_WITH_APPROVED_EVIDENCE",
             pv_conversion_evidence_ref="fixture://inverter-study",
             pv_source_ac_semantics="UNCLIPPED_DC_NORMALIZED"),
        dict(network_revision_id="M0-FIXTURE-REV", asset_id="A-PVR", existing_generator_id="G-CGMES-PVR",
             existing_bus_id="B-PVR", carrier="solar", technology_variant="Solar PV Rooftop", p_nom_mw=10,
             bus_role="ORIGINAL", geo_quality="REGIONAL_SOURCE", plant_lon=9.25, plant_lat=48.75,
             plant_crs="EPSG:4326", pv_dc_mwp=12, pv_ac_mw=10,
             pv_clipping_policy="CLIP_AC_AT_P_NOM_WITH_APPROVED_EVIDENCE",
             pv_conversion_evidence_ref="fixture://inverter-study-rooftop",
             pv_source_ac_semantics="UNCLIPPED_DC_NORMALIZED"),
    ])
    thermal = dict(network_revision_id="M0-FIXTURE-REV", asset_id="A-THERMAL",
                   existing_generator_id="G-CGMES-THERMAL", existing_bus_id="B-C", carrier="gas",
                   technology_variant="", p_nom_mw=1000, bus_role="ORIGINAL", geo_quality="NONE")
    assets = pd.concat([assets, pd.DataFrame([thermal])], ignore_index=True)
    assets["res_profile_required"] = ["true"] * 5 + ["false"]
    assets_path = base / "m0_assets.csv"
    assets.to_csv(assets_path, index=False)
    m0 = {"reference_type": "DetailedNetworkReference_v1", "network_revision_id": "M0-FIXTURE-REV",
          "source_set_hash": "fixture-only-source-set", "mapping_policy_hash": "fixture-only-policy",
          "identity_ledger_ref": "fixture://identity-map", "sidecar_ref": "fixture://m0-sidecar",
          "asset_registry_sha256": digest(assets_path), "generator_count": 6}
    m0_path = base / "m0.json"
    m0_path.write_text(json.dumps(m0))
    manifest = {"selected_weather_ids": WEATHERS, "planning_horizons": [HORIZON],
                "evidence_class": "FIXTURE", "time_semantics": "HOURLY_UTC_NAIVE_OUTPUT",
                "full_native_year_required": False}
    weather_path = base / "weather.json"
    weather_path.write_text(json.dumps(manifest))
    profiles = [
        ("ON-PEON-1", "Wind_Onshore", "PEON", "DE_PEON", "MW_per_MW"),
        ("OFF-PEOF-1", "Wind_Offshore", "PEOF", "NSEA", "MW_per_MW"),
        ("PV-ORIG-1", "Solar PV Utility", "ORIG", "GRID-01", "MW_per_MWp"),
        ("PV-P2ON-1", "Solar PV Rooftop", "P2ON", "DE_P2ON", "MW_per_MWp"),
    ]
    values = {"ON-PEON-1": [0.2, 0.6], "OFF-PEOF-1": [0.75, 0.85],
              "PV-ORIG-1": [0.8, 0.9], "PV-P2ON-1": [0.4, 0.5]}
    catalog_rows = []
    for wi, weather in enumerate(WEATHERS):
        for pid, tech, level, region, unit in profiles:
            filename = f"{weather}_{pid}.csv"
            f = base / filename
            pd.DataFrame({"Date": ["01.01.", "01.01."], "Hour": [1, 2],
                          "WS001": [v + wi * 0.001 for v in values[pid]]}).to_csv(f, index=False)
            catalog_rows.append(dict(planning_horizon=HORIZON, weather_id=weather,
                source_profile_id=pid, technology_variant=tech, spatial_level=level, region_id=region,
                source_format="TYNDP_DATE_HOUR", file_path=filename, source_sha256=digest(f),
                source_dataset_id="FIXTURE-PECD-42", source_dataset_version="4.2-fixture",
                corrected_dataset_revision="fixture-2026-08-21", license="FIXTURE-MIT",
                source_evidence_ref="fixture://source", source_time_basis="UTC", calendar_year="2020",
                weather_column="WS001", source_unit=unit, geometry_ref="fixture://geometry",
                spatial_source_crs="EPSG:4326"))
    catalog_path = base / "source_catalog.csv"
    pd.DataFrame(catalog_rows).to_csv(catalog_path, index=False)
    rows = []
    for a, p, method, level in [
        (0, 0, "EXPLICIT_SOURCE_ID", "PEON"), (1, 0, "EXPLICIT_SOURCE_ID", "PEON"),
        (2, 1, "EXPLICIT_SOURCE_ID", "PEOF"),
        (3, 2, "VERIFIED_PLANT_LOCATION_WITH_OFFICIAL_PECD_MASK", "ORIG"),
        (4, 3, "EXPLICIT_SOURCE_ID", "P2ON"),
    ]:
        asset = assets.iloc[a]
        rows.append(dict(network_revision_id="M0-FIXTURE-REV", planning_horizon=HORIZON,
                         asset_id=asset.asset_id, existing_generator_id=asset.existing_generator_id,
                         existing_bus_id=asset.existing_bus_id,
                         source_profile_id=profiles[p][0], technology_variant=asset.technology_variant,
                         spatial_level=level, spatial_assignment_method=method,
                         geo_quality=asset.geo_quality, mapping_weight=1,
                         segment_capacity=asset.p_nom_mw, capacity_basis="AC_MW",
                         source_evidence_ref="fixture://assignment"))
    map_path = base / "asset_map.csv"
    pd.DataFrame(rows).to_csv(map_path, index=False)
    geo = {"type": "FeatureCollection", "features": [{
        "type": "Feature", "properties": {"source_profile_id": "PV-ORIG-1", "technology_variant": "Solar PV Utility",
        "spatial_level": "ORIG", "source_evidence_ref": "fixture://mask", "crs": "EPSG:4326"},
        "geometry": {"type": "Polygon", "coordinates": [[[9, 48], [10, 48], [10, 49], [9, 49], [9, 48]]]}}]}
    geo_path = base / "geo.json"
    geo_path.write_text(json.dumps(geo))
    crosswalk = ROOT / "data/iosn_m1/technology_crosswalk_v1.csv"
    args = parse_args(["--weather-manifest", str(weather_path), "--source-catalog", str(catalog_path),
        "--m0-assets", str(assets_path), "--m0-reference-manifest", str(m0_path),
        "--technology-crosswalk", str(crosswalk), "--assignment-map", str(map_path),
        "--geometry-registry", str(geo_path), "--horizon", HORIZON,
        "--weather-id", WEATHERS[0], "--output-cf", str(base / "out.nc"),
        "--output-source-ledger", str(base / "sources.csv"),
        "--output-assignment-ledger", str(base / "assignment_ledger.csv"),
        "--output-profile-catalog", str(base / "profile_catalog.csv"),
        "--output-qa", str(base / "qa.json")])
    return args


def edit_csv(path, function):
    df = pd.read_csv(path, dtype="string", keep_default_na=False)
    function(df)
    df.to_csv(path, index=False)


