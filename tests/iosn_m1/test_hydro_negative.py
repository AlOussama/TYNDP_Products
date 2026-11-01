# SPDX-License-Identifier: MIT
import copy

import pandas as pd
import pytest

from scripts.iosn_m1.hydro.adapter import (
    HydroContractError,
    execute,
    read_snapshots,
    write_outputs,
)
from hydro_fixtures import fixture_case


def invalid(case, contains=None):
    with pytest.raises(HydroContractError) as err:
        execute(**case)
    if contains:
        assert contains.lower() in str(err.value).lower()


def test_absent_weather_dataset_never_substituted(tmp_path):
    c = fixture_case(tmp_path)
    c["manifest"]["sources"] = c["manifest"]["sources"][:-1]
    invalid(c, "Five weather")


def test_exact_five_selected_weather_ids_required(tmp_path):
    c = fixture_case(tmp_path)
    c["manifest"]["selected_weather_ids"] = ["FIXTURE-WS-01"] * 5
    invalid(c, "Five distinct")


def test_missing_file_or_hash_mismatch_blocks_entire_5set_campaign(tmp_path):
    c = fixture_case(tmp_path)
    c["manifest"]["sources"][3]["sha256"] = "f" * 64
    invalid(c, "sha256 mismatch")
    c = fixture_case(tmp_path)
    (tmp_path / "input_5.csv").unlink()
    invalid(c, "Physical source missing")


def test_no_implicit_bus_geographic_basin_mapping(tmp_path):
    c = fixture_case(tmp_path)
    c["allocations"].loc[0, "mapping_basis"] = "NEAREST_ELECTRICAL_BUS"
    invalid(c, "Bus coordinates")


def test_unqualified_allocation_and_unknown_asset_are_blocked(tmp_path):
    c = fixture_case(tmp_path, two_assets=True)
    c["allocations"].loc[1, "share"] = "0.3"
    invalid(c, "sum to 1")
    c = fixture_case(tmp_path)
    c["allocations"].loc[0, "asset_id"] = "asset-not-in-m0"
    invalid(c, "existing M0")


def test_missing_evidence_and_unapproved_energy_gain(tmp_path):
    c = fixture_case(tmp_path)
    c["allocations"].loc[0, "evidence_ref"] = ""
    invalid(c, "hydrological evidence")
    c = fixture_case(tmp_path)
    c["allocations"].loc[0, "conversion_factor"] = "1.2"
    invalid(c, "conversion gain")


def test_hydraulic_energy_needs_explicit_conversion_evidence(tmp_path):
    c = fixture_case(tmp_path, semantics="HYDRAULIC_ENERGY_MWH")
    invalid(c, "documented conversion")
    c["allocations"].loc[0, "conversion_factor"] = "0.8"
    c["allocations"].loc[0, "conversion_evidence_ref"] = "FIXTURE_HYDRAULIC_CONVERTER"
    result = execute(**c)
    assert result["hydro_inflow"].value.sum() == pytest.approx(96 * .8)
    assert result["interval_energy_ledger"].allocated_native_mwh.sum() == pytest.approx(96)


def test_ror_must_not_disguise_reservoir_inflow_as_availability(tmp_path):
    c = fixture_case(tmp_path, tech="HRR")
    c["assets_frame"].loc[0, "component_class"] = "Generator"
    c["assets_frame"].loc[0, "max_hours"] = ""
    invalid(c, "RoR Generator requires available generation energy")


def test_ror_exceeding_generator_pnom_cannot_be_silently_clipped(tmp_path):
    c = fixture_case(tmp_path, tech="HRR", semantics="AVAILABLE_GENERATION_ENERGY_MWH")
    c["assets_frame"].loc[0, "component_class"] = "Generator"
    c["assets_frame"].loc[0, "max_hours"] = ""
    c["assets_frame"].loc[0, "p_nom_mw"] = "1"
    invalid(c, "exceeds unchanged")


def test_existing_storage_capacity_and_efficiency_checked(tmp_path):
    c = fixture_case(tmp_path)
    c["assets_frame"].loc[0, "max_hours"] = "0"
    invalid(c, "max_hours")
    c = fixture_case(tmp_path)
    c["assets_frame"].loc[0, "efficiency_dispatch"] = "1.1"
    invalid(c, "efficiency")


def test_closed_loop_zero_is_never_invented(tmp_path):
    c = fixture_case(tmp_path, tech="HCL")
    invalid(c, "HCL cannot be assigned")
    c = fixture_case(tmp_path)
    c["assets_frame"].loc[0, "hydro_tech"] = "HCL"
    invalid(c, "Hydro technology or role mismatch")


def test_store_link_requires_approved_existing_port(tmp_path):
    c = fixture_case(tmp_path)
    c["assets_frame"].loc[0, "component_class"] = "Store"
    c["assets_frame"].loc[0, "e_nom_mwh"] = "100"
    invalid(c, "Store/Link requires explicit")


def test_native_intervals_must_be_gap_free(tmp_path):
    intervals = [
        ("2026-01-01T00:00:00+00:00", "2026-01-02T00:00:00+00:00", 24),
        ("2026-01-02T01:00:00+00:00", "2026-01-03T00:00:00+00:00", 23),
    ]
    c = fixture_case(tmp_path, native_intervals=intervals)
    invalid(c, "interval gap")


def test_missing_hour_in_hourly_snapshots_is_detected(tmp_path):
    c = fixture_case(tmp_path)
    file = tmp_path / "snapshots.csv"
    snapshots = pd.read_csv(file)
    snapshots = snapshots.drop(index=5)
    snapshots.to_csv(file, index=False)
    with pytest.raises(HydroContractError, match="Missing or overlapping"):
        read_snapshots(file)


def test_utc_offset_must_agree_with_declared_DST_zone(tmp_path):
    c = fixture_case(tmp_path, zone="Europe/Berlin", native_intervals=[
        ("2026-03-29T02:00:00+01:00", "2026-03-29T04:00:00+02:00", 2)
    ])
    invalid(c, "Offset/zone inconsistency")


def test_real_data_pass_cannot_be_claimed_from_fixture_only(tmp_path):
    c = fixture_case(tmp_path)
    c["manifest"]["source_mode"] = "REAL"
    invalid(c, "M0 network and sidecar")


def test_write_outputs_refuses_nonempty_directory_and_stale_results(tmp_path):
    c = fixture_case(tmp_path)
    out = tmp_path / "published"
    out.mkdir()
    (out / "old-result.txt").write_text("stale", encoding="utf-8")
    with pytest.raises(HydroContractError, match="absent or empty"):
        write_outputs(execute(**c), out)


def test_unknown_native_energy_or_nan_cannot_be_filled_with_zero(tmp_path):
    c = fixture_case(tmp_path)
    c["manifest"]["sources"][0]["unit"] = "MW"
    invalid(c, "must be MWh")
