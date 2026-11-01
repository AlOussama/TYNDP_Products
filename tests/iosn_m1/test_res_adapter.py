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


def test_full_fixture_cf_original_ids_and_no_static_edits(tmp_path):
    args = make_fixture(tmp_path)
    before = {str(p): digest(p) for p in (args.m0_assets, args.m0_reference_manifest)}
    qa = execute(args)
    assert qa["real_data_qualified"] is False
    assert qa["mapped_mw"] == pytest.approx(580.0)
    assert qa["m0_total_generator_count"] == 6
    assert qa["netcdf_roundtrip"] == "PASS"
    with xr.open_dataset(args.output_cf) as ds:
        assert ds.sizes == {"time": 2, "existing_generator_id": 5}
        assert list(ds.existing_generator_id.values) == [
            "G-CGMES-ON1", "G-CGMES-ON2", "G-CGMES-OFF", "G-CGMES-PVU", "G-CGMES-PVR"]
        assert np.allclose(ds.renewable_cf.values[:, 0], [0.2, 0.6])
        assert np.allclose(ds.renewable_cf.values[:, 1], [0.2, 0.6])  # same region, different buses
        assert np.allclose(ds.renewable_cf.values[:, 2], [0.75, 0.85])
        assert np.allclose(ds.renewable_cf.values[:, 3], [1, 1])  # explicit MWp -> MW_AC clipping
        assert np.allclose(ds.renewable_cf.values[:, 4], [0.48, 0.6])
        assert ds.attrs["semantics"] == "CAPACITY_FACTOR_NOT_DISPATCH"
    assert all(digest(p) == before[str(p)] for p in (args.m0_assets, args.m0_reference_manifest))
    assert len(pd.read_csv(args.output_source_ledger)) == 4
    assert len(pd.read_csv(args.output_assignment_ledger)) == 5


def test_five_separate_weather_sets(tmp_path):
    args = make_fixture(tmp_path)
    for idx, wid in enumerate(WEATHERS):
        args.weather_id = wid
        args.output_cf = tmp_path / f"out_{wid}.nc"
        result = execute(args)
        assert result["weather_id"] == wid
        with xr.open_dataset(args.output_cf) as ds:
            assert ds.renewable_cf.values[0, 0] == pytest.approx(0.2 + idx * 0.001)
    assert len(list(tmp_path.glob("out_FIXTURE_WS_*.nc"))) == 5


def test_incomplete_five_sets_is_blocked(tmp_path):
    args = make_fixture(tmp_path)
    edit_csv(args.source_catalog, lambda d: d.drop(index=d.index[-1], inplace=True))
    with pytest.raises(ContractError, match="INCOMPLETE_FIVE_SET_SOURCE"):
        execute(args)


def test_invalid_weather_id_never_falls_back(tmp_path):
    args = make_fixture(tmp_path)
    args.weather_id = "WS003"
    with pytest.raises(ContractError, match="UNSELECTED_WEATHER_ID"):
        execute(args)


def test_source_hash_and_missing_file_are_fatal(tmp_path):
    args = make_fixture(tmp_path)
    file = tmp_path / f"{WEATHERS[0]}_ON-PEON-1.csv"
    file.write_text("corruption")
    with pytest.raises(ContractError, match="SOURCE_SHA256_MISMATCH"):
        execute(args)
    file.unlink()
    with pytest.raises(ContractError, match="SOURCE_FILE_NOT_FOUND"):
        execute(args)


def test_synthetic_three_winding_star_is_forbidden(tmp_path):
    args = make_fixture(tmp_path)
    edit_csv(args.m0_assets, lambda d: d.__setitem__("bus_role", d["bus_role"].mask(d.index == 0, "SYNTHETIC_3W_STAR")))
    m0 = json.loads(args.m0_reference_manifest.read_text())
    m0["asset_registry_sha256"] = digest(args.m0_assets)
    args.m0_reference_manifest.write_text(json.dumps(m0))
    with pytest.raises(ContractError, match="SYNTHETIC_GENERATOR_BUS"):
        execute(args)


def test_offshore_landfall_not_used_as_weather_location(tmp_path):
    args = make_fixture(tmp_path)
    edit_csv(args.assignment_map, lambda d: d.__setitem__("spatial_assignment_method",
             d["spatial_assignment_method"].mask(d["existing_generator_id"] == "G-CGMES-OFF",
             "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE")))
    with pytest.raises(ContractError, match="OFFSHORE_LANDFALL_PROXY|MASK_PROFILE_MISSING_OR_DUPLICATE"):
        execute(args)


def test_geometry_ambiguity_blocks_instead_of_nearest(tmp_path):
    args = make_fixture(tmp_path)
    geo = json.loads(args.geometry_registry.read_text())
    dup = json.loads(json.dumps(geo["features"][0]))
    dup["properties"]["source_profile_id"] = "PV-ORIG-2"
    geo["features"].append(dup)
    args.geometry_registry.write_text(json.dumps(geo))
    with pytest.raises(ContractError, match="AMBIGUOUS_OR_WRONG_REGION"):
        execute(args)


def test_pv_dc_ac_ratio_and_clipping_must_be_qualified(tmp_path):
    args = make_fixture(tmp_path)
    edit_csv(args.m0_assets, lambda d: d.__setitem__("pv_conversion_evidence_ref",
             d["pv_conversion_evidence_ref"].mask(d["existing_generator_id"] == "G-CGMES-PVU", "")))
    m0 = json.loads(args.m0_reference_manifest.read_text())
    m0["asset_registry_sha256"] = digest(args.m0_assets)
    args.m0_reference_manifest.write_text(json.dumps(m0))
    with pytest.raises(ContractError, match="PV_AC_DC_EVIDENCE_MISSING"):
        execute(args)


def test_mw_weighted_composite_and_wrong_weights(tmp_path):
    args = make_fixture(tmp_path)
    catalog = pd.read_csv(args.source_catalog, dtype="string", keep_default_na=False)
    extras = catalog[catalog["source_profile_id"].eq("ON-PEON-1")].copy()
    extras["source_profile_id"] = "ON-PEON-2"
    extras["region_id"] = "DE2_PEON"
    catalog = pd.concat([catalog, extras], ignore_index=True)
    catalog.to_csv(args.source_catalog, index=False)
    amap = pd.read_csv(args.assignment_map, dtype="string", keep_default_na=False)
    old = amap.loc[amap["existing_generator_id"].eq("G-CGMES-ON1")].iloc[0].copy()
    first = old.copy()
    first["spatial_assignment_method"] = "CAPACITY_WEIGHTED_COMPOSITE_WITH_DOCUMENTED_MW_SHARES"
    first["mapping_weight"] = ".4"
    first["segment_capacity"] = "40"
    other = first.copy()
    other["source_profile_id"] = "ON-PEON-2"
    other["mapping_weight"] = ".6"
    other["segment_capacity"] = "60"
    amap = pd.concat([amap.loc[~amap["existing_generator_id"].eq("G-CGMES-ON1")],
                      pd.DataFrame([first, other])], ignore_index=True)
    amap.to_csv(args.assignment_map, index=False)
    qa = execute(args)
    assert qa["assignment_audit"]["geo_methods"]["CAPACITY_WEIGHTED_COMPOSITE_WITH_DOCUMENTED_MW_SHARES"] == 2
    with xr.open_dataset(args.output_cf) as ds:
        assert ds.renewable_cf.sel(existing_generator_id="G-CGMES-ON1").values[0] == pytest.approx(.2)
    edit_csv(args.assignment_map, lambda d: d.__setitem__("mapping_weight",
             d["mapping_weight"].mask(d["source_profile_id"].eq("ON-PEON-2"), "0.5")))
    with pytest.raises(ContractError, match="MW_WEIGHT_SUM_NOT_ONE"):
        execute(args)


def test_missing_hour_is_not_automatically_zero_filled(tmp_path):
    args = make_fixture(tmp_path)
    f = tmp_path / f"{WEATHERS[0]}_ON-PEON-1.csv"
    pd.DataFrame({"Date": ["01.01.", "01.01."], "Hour": [1, 3], "WS001": [0.2, 0.6]}).to_csv(f, index=False)
    edit_csv(args.source_catalog, lambda d: d.__setitem__("source_sha256",
             d["source_sha256"].mask((d["weather_id"] == WEATHERS[0]) &
                                       (d["source_profile_id"] == "ON-PEON-1"), digest(f))))
    with pytest.raises(ContractError, match="TIME_GAP_OR_NONHOURLY"):
        execute(args)


def test_leap_year_utc_2020_and_dst_ambiguity():
    leap = _utc_index(pd.Series(["2020-02-29 00:00:00", "2020-02-29 01:00:00"]), "UTC")
    assert leap[0].day == 29 and leap[0].month == 2
    with pytest.raises(Exception, match="ambiguous|Ambiguous|Cannot infer"):
        _utc_index(pd.Series(["2026-10-25 02:00:00"]), "Europe/Berlin")
    with pytest.raises(Exception):
        _utc_index(pd.Series(["2026-03-29 02:30:00"]), "Europe/Berlin")
    aware = _utc_index(pd.Series(["2026-10-25T02:30:00+02:00", "2026-10-25T02:30:00+01:00"]), "Europe/Berlin")
    assert (aware[1] - aware[0]) == pd.Timedelta(hours=1)


def test_cli_blocked_report_on_contract_failure(tmp_path):
    args = make_fixture(tmp_path)
    args.weather_id = "BAD-ID"
    from unittest.mock import patch
    with patch("scripts.iosn_m1.res.run.parse_args", return_value=args):
        assert main() == 2
    status = json.loads(args.output_qa.read_text())
    assert status["status"] == "BLOCKED" and "UNSELECTED_WEATHER_ID" in status["reason"]
    assert not args.output_cf.exists()


def test_original_raw_tyndp_skip10_header_and_ws_column(tmp_path):
    args = make_fixture(tmp_path)
    filename = tmp_path / f"{WEATHERS[0]}_ON-PEON-1.csv"
    raw = filename.read_text()
    filename.write_text("\n".join(["# fixture source metadata"] * 10) + "\n" + raw)
    edit_csv(args.source_catalog, lambda d: (
        d.__setitem__("source_sha256", d["source_sha256"].mask(
            (d["weather_id"] == WEATHERS[0]) & (d["source_profile_id"] == "ON-PEON-1"), digest(filename))),
        d.__setitem__("source_format", d["source_format"].mask(
            (d["weather_id"] == WEATHERS[0]) & (d["source_profile_id"] == "ON-PEON-1"),
            "TYNDP_RAW10_DATE_HOUR"))
    ))
    result = execute(args)
    assert result["source_profile_count"] == 4


def test_iso_utc_with_explicit_timezone_offsets(tmp_path):
    args = make_fixture(tmp_path)
    f = tmp_path / f"{WEATHERS[0]}_ON-PEON-1.csv"
    pd.DataFrame({"time": ["2020-01-01T01:00:00+01:00", "2020-01-01T02:00:00+01:00"],
                  "cf": [0.2, 0.6]}).to_csv(f, index=False)
    edit_csv(args.source_catalog, lambda d: (
        d.__setitem__("source_sha256", d["source_sha256"].mask(
            (d["weather_id"] == WEATHERS[0]) & (d["source_profile_id"] == "ON-PEON-1"), digest(f))),
        d.__setitem__("source_format", d["source_format"].mask(
            (d["weather_id"] == WEATHERS[0]) & (d["source_profile_id"] == "ON-PEON-1"), "ISO_CSV"))
    ))
    assert execute(args)["utc_start"] == "2020-01-01T00:00:00"


def test_real_candidate_partial_year_must_fail(tmp_path):
    args = make_fixture(tmp_path)
    manifest = json.loads(args.weather_manifest.read_text())
    manifest["evidence_class"] = "REAL_SOURCE_CANDIDATE"
    manifest["full_native_year_required"] = True
    args.weather_manifest.write_text(json.dumps(manifest))
    with pytest.raises(ContractError, match="REAL_SOURCE_PROVENANCE_UNQUALIFIED"):
        execute(args)


def test_bus_proxy_with_unverified_location_is_blocked(tmp_path):
    args = make_fixture(tmp_path)
    edit_csv(args.assignment_map, lambda d: d.__setitem__("spatial_assignment_method",
             d["spatial_assignment_method"].mask(d["existing_generator_id"] == "G-CGMES-PVU",
             "VERIFIED_BUS_PROXY_WITH_SPATIAL_EVIDENCE")))
    with pytest.raises(ContractError, match="UNVERIFIED_BUS_PROXY"):
        execute(args)


def test_unknown_carrier_declared_res_is_blocked(tmp_path):
    args = make_fixture(tmp_path)
    edit_csv(args.m0_assets, lambda d: d.__setitem__("carrier",
             d["carrier"].mask(d["existing_generator_id"] == "G-CGMES-ON1", "unknown-res")))
    m0 = json.loads(args.m0_reference_manifest.read_text())
    m0["asset_registry_sha256"] = digest(args.m0_assets)
    args.m0_reference_manifest.write_text(json.dumps(m0))
    with pytest.raises(ContractError, match="UNKNOWN_M0_CARRIER"):
        execute(args)
