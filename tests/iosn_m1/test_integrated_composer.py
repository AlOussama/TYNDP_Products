# SPDX-License-Identifier: MIT
"""Integrated MA4F synthetic-only source -> PyPSA NetCDF validation.

All inputs are explicitly generated here. They are not actual CGMES, PECD,
Hydro, DFT or externally selected weather datasets.
"""
from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import pypsa
import pytest

from fixture_ma4f import build, WEATHERS, HORIZON
from scripts.iosn_m1.res.adapter import digest
from scripts.iosn_m1.res.run import execute as res_execute
from scripts.iosn_m1.hydro.adapter import execute as hydro_execute, write_outputs
from scripts.iosn_m1.compose import (
    compose, IntegrationError, static_fingerprints,
)


@pytest.fixture(scope="module")
def integrated(tmp_path_factory):
    root = tmp_path_factory.mktemp("ma4f")
    fixture = build(root)
    res = fixture["res_args"]
    for weather in WEATHERS:
        res.weather_id = weather
        resdir = root / "res" / weather
        resdir.mkdir(parents=True)
        res.output_cf = resdir / "renewable_cf.nc"
        res.output_source_ledger = resdir / "source_ledger.csv"
        res.output_assignment_ledger = resdir / "assignment_ledger.csv"
        res.output_profile_catalog = resdir / "profile_catalog.csv"
        res.output_qa = resdir / "qa.json"
        res_execute(res)
        h = fixture["hydro_case"]
        result = hydro_execute(
            h["manifest"], h["allocations"], h["assets_frame"],
            h["snapshots"], h["root"], h["planning_horizon"], weather)
        write_outputs(result, root / "hydro" / weather)
    return fixture


def params(fixture, weather, *, output_network=None):
    root = fixture["root"]
    return dict(
        m0_network=fixture["m0_network"],
        m0_sidecar=fixture["sidecar"],
        m0_reference_manifest=fixture["m0_reference_manifest"],
        bridge_path=fixture["bridge"],
        master_path=fixture["master"],
        res_manifest_path=fixture["res_manifest"],
        res_catalog=fixture["res_catalog"],
        hydro_manifest_path=fixture["hydro_manifest"],
        hydro_assets=fixture["hydro_assets"],
        hydro_allocations=fixture["hydro_allocations"],
        res_cf=root / "res" / weather / "renewable_cf.nc",
        hydro_dir=root / "hydro" / weather,
        res_qa=root / "res" / weather / "qa.json",
        hydro_qa=root / "hydro" / weather / "qa.json",
        horizon=HORIZON,
        weather_id=weather,
        output_network=output_network or root / "combined" / weather /
                       f"detailed_reference_{HORIZON}_{weather}.nc",
    )


def edit_json(path, fn):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    fn(payload)
    Path(path).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8")


def cloned_file(path, tmp_path):
    target = tmp_path / Path(path).name
    shutil.copyfile(path, target)
    return target


def test_five_weather_compositions_and_all_static_component_invariance(integrated):
    f = integrated
    original_hash = digest(f["m0_network"])
    base = pypsa.Network(str(f["m0_network"]))
    original = static_fingerprints(base)
    assert "Bus" in original and "Generator" in original
    assert "Transformer" in original and "Store" in original
    assert "Link" in original and "Load" in original
    assert "StorageUnit" in original
    assert len(f["weather_ids"]) == 5
    outputs = []
    for weather in WEATHERS:
        p = params(f, weather)
        qa = compose(**p)
        assert qa["status"] == "M1_MA4F_FIXTURE_INTEGRATION_QUALIFIED"
        assert qa["real_data_qualified"] is False and qa["m2_release"] is False
        assert qa["static_invariance"] == "PASS_ALL_COMPONENT_TABLES"
        assert qa["m0_static_fingerprints_before"] == original
        assert qa["m0_static_fingerprints_after"] == original
        assert qa["loads_t_p_set_preserved"]
        assert qa["staged_store_link_written"] == 0
        assert qa["weather_id_count"] == 5 and qa["snapshot_count"] == 2
        assert qa["dynamic_targets"] == 8  # 5 RES + 1 RoR + 2 StorageUnits
        assert len(qa["target_ownership"]) == 8
        composed = pypsa.Network(str(p["output_network"]))
        assert static_fingerprints(composed) == original
        assert composed.loads_t.p_set.equals(base.loads_t.p_set)
        expected_generators = {
            "G-CGMES-ON1", "G-CGMES-ON2", "G-CGMES-OFF",
            "G-CGMES-PVU", "G-CGMES-PVR", "G-CGMES-ROR"}
        assert set(composed.generators_t.p_max_pu) <= expected_generators
        for identifier in expected_generators:
            if identifier in composed.generators_t.p_max_pu:
                assert len(composed.generators_t.p_max_pu[identifier]) == 2
            else:
                # PyPSA intentionally elides time-series which exactly equal
                # the physical default; their meaning survives via static.
                assert any(e["target_id"] == identifier
                           for e in qa["pypsa_default_elision_ledger"])
                assert composed.generators.at[identifier, "p_max_pu"] == 1.0
        assert set(composed.storage_units_t.inflow) == {
            "existing-su-101", "existing-su-102"}
        assert np.allclose(composed.storage_units_t.inflow["existing-su-101"], 1.2)
        assert np.allclose(composed.storage_units_t.inflow["existing-su-102"], .8)
        assert np.allclose(composed.generators_t.p_max_pu["G-CGMES-ROR"], .2)
        assert "HCL-FX" not in composed.storage_units_t.inflow.columns
        assert composed.links.index.equals(base.links.index)
        assert composed.transformers.index.equals(base.transformers.index)
        assert composed.buses.index.equals(base.buses.index)
        assert "B-STAR" in composed.buses.index
        outputs.append(digest(p["output_network"]))
    assert len(outputs) == len(WEATHERS)
    assert len(set(outputs)) == len(outputs), "Five fixture weather profiles must differ"
    assert digest(f["m0_network"]) == original_hash


def test_master_rejects_missing_fifth_weather(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    manifest = cloned_file(p["master_path"], tmp_path)
    edit_json(manifest, lambda d: d["selected_weather_ids"].pop())
    p["master_path"] = manifest
    with pytest.raises(IntegrationError, match="MASTER_EXACT_FIVE_WEATHER_IDS"):
        compose(**p)
    assert not p["output_network"].exists()


def test_m0_canonical_revision_cannot_be_silently_aliased_to_projection(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    bridge = cloned_file(p["bridge_path"], tmp_path)
    edit_json(bridge, lambda d: d.update({
        "legacy_network_revision_id": d["projection_id"]}))
    p["bridge_path"] = bridge
    with pytest.raises(IntegrationError, match="UNAUTHORIZED_NETWORK_REVISION_ALIAS"):
        compose(**p)


def test_source_hash_change_is_fatal_before_pypsa_write(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    sidecar = cloned_file(p["m0_sidecar"], tmp_path)
    with sidecar.open("a") as stream:
        stream.write("\n")
    p["m0_sidecar"] = sidecar
    with pytest.raises(IntegrationError, match="MASTER_SOURCE_SHA256_MISMATCH"):
        compose(**p)
    assert not p["output_network"].exists()


def test_ror_and_res_same_generator_target_collision_blocked(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    hydro_dir = tmp_path / "hydro"
    shutil.copytree(p["hydro_dir"], hydro_dir)
    ror = hydro_dir / "ror_availability.csv"
    df = pd.read_csv(ror)
    df["existing_hydro_id"] = "G-CGMES-ON1"
    df.to_csv(ror, index=False)
    p["hydro_dir"] = hydro_dir
    p["hydro_qa"] = hydro_dir / "qa.json"
    with pytest.raises(IntegrationError, match="PRODUCER_TARGET_COLLISION"):
        compose(**p)


def test_missing_required_hydro_source_output_is_not_zero_filled(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    hydro_dir = tmp_path / "hydro"
    shutil.copytree(p["hydro_dir"], hydro_dir)
    (hydro_dir / "hydro_inflow.csv").unlink()
    p["hydro_dir"], p["hydro_qa"] = hydro_dir, hydro_dir / "qa.json"
    with pytest.raises(IntegrationError, match="MISSING_PRODUCER_OUTPUT"):
        compose(**p)


def test_store_link_port_is_explicitly_staged_not_auto_written(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    hydro_dir = tmp_path / "hydro"
    shutil.copytree(p["hydro_dir"], hydro_dir)
    staged = hydro_dir / "store_link_staged.csv"
    pd.DataFrame([{"utc_naive_timestamp": "2020-01-01T00:00:00",
                   "existing_hydro_id": "STORE-CGMES-1",
                   "target_attribute": "generators_t.p_set", "value": 5}]).to_csv(
                       staged, index=False)
    p["hydro_dir"], p["hydro_qa"] = hydro_dir, hydro_dir / "qa.json"
    with pytest.raises(IntegrationError, match="STORE_LINK_STAGED_REQUIRES"):
        compose(**p)


def test_utc_hourly_snapshot_axis_mismatch_is_rejected(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    master = cloned_file(p["master_path"], tmp_path)
    edit_json(master, lambda d: d["time_axis"].update({
        "end_utc_inclusive": "2020-01-01T02:00:00"}))
    p["master_path"] = master
    with pytest.raises(IntegrationError, match="MASTER_M0_TIME_AXIS_MISMATCH"):
        compose(**p)


def test_preexisting_res_profile_cannot_be_overwritten(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    n = pypsa.Network(str(p["m0_network"]))
    n.generators_t.p_max_pu = pd.DataFrame({
        "G-CGMES-ON1": [.4, .5]}, index=n.snapshots)
    new_network = tmp_path / "m0_with_existing_profile.nc"
    n.export_to_netcdf(str(new_network))
    master = cloned_file(p["master_path"], tmp_path)
    edit_json(master, lambda d: d["input_sha256"].update({
        "m0_network": digest(new_network)}))
    p["m0_network"], p["master_path"] = new_network, master
    with pytest.raises(IntegrationError, match="EXISTING_PROFILE_OVERWRITE_FORBIDDEN"):
        compose(**p)


def test_real_evidence_flags_never_promote_fixture_to_m2(integrated, tmp_path):
    p = params(integrated, WEATHERS[0], output_network=tmp_path/"out.nc")
    master = cloned_file(p["master_path"], tmp_path)
    edit_json(master, lambda d: d.update({
        "evidence_class": "REAL_SOURCE_CANDIDATE", "real_data_qualified": True}))
    p["master_path"] = master
    with pytest.raises(IntegrationError, match="REAL_SOURCE_NOT_QUALIFIED_MA4F"):
        compose(**p)
