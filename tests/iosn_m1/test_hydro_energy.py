# SPDX-License-Identifier: MIT
import math

import pandas as pd
import pytest

from scripts.iosn_m1.hydro.adapter import execute, write_outputs
from hydro_fixtures import fixture_case


def run(case):
    return execute(**case)


def test_two_original_storage_units_preserve_native_mwh_and_bus(tmp_path):
    c = fixture_case(tmp_path, two_assets=True)
    result = run(c)
    inflow = result["hydro_inflow"]
    assert len(inflow) == 48 * 2
    energy = inflow.groupby("asset_id").value.sum()
    assert energy["original-hydro-1"] == pytest.approx(57.6)
    assert energy["original-hydro-2"] == pytest.approx(38.4)
    assert math.fsum(energy) == pytest.approx(96.0)
    native = result["interval_energy_ledger"]
    assert native.source_energy_mwh.iloc[0] == pytest.approx(96)
    assert native.source_energy_residual_mwh.abs().max() < 1e-9
    assert result["qa"]["selected_weather_count"] == 5
    assert result["qa"]["source_status"] == "FIXTURE_ONLY"
    assert result["qa"]["network_mutation_count"] == 0
    assert list(c["assets_frame"].bus_id) == ["original-bus", "original-bus"]
    assert inflow.utc_naive_timestamp.dt.tz is None
    output = tmp_path / "out"
    write_outputs(result, output)
    assert (output / "interval_energy_ledger.csv").is_file()
    assert (output / "hydro_allocation_ledger.csv").is_file()
    assert (output / "qa.json").is_file()


def test_53_native_weeks_with_partial_last_interval_in_leap_year(tmp_path):
    start = pd.Timestamp("2024-01-01T00:00:00+00:00")
    end = pd.Timestamp("2025-01-01T00:00:00+00:00")
    intervals = []
    now = start
    while now < end:
        nxt = min(now + pd.Timedelta(days=7), end)
        hours = (nxt - now).total_seconds() / 3600
        intervals.append((now.isoformat(), nxt.isoformat(), 2.0 * hours))
        now = nxt
    assert len(intervals) == 53
    assert (pd.Timestamp(intervals[-1][1]) - pd.Timestamp(intervals[-1][0])).total_seconds() == 48 * 3600
    c = fixture_case(tmp_path, native_intervals=intervals)
    result = run(c)
    native = result["interval_energy_ledger"]
    assert len(native) == 53
    assert native.native_duration_h.iloc[-1] == 48
    assert len(result["hydro_inflow"]) == 8784
    assert result["hydro_inflow"].value.sum() == pytest.approx(8784 * 2.0)
    assert native.source_energy_mwh.sum() == pytest.approx(8784 * 2.0)


@pytest.mark.parametrize("start,end,energy,hours", [
    ("2026-03-29T00:00:00+01:00", "2026-03-30T00:00:00+02:00", 46, 23),
    ("2026-10-25T00:00:00+02:00", "2026-10-26T00:00:00+01:00", 50, 25),
])
def test_dst_day_intervals_use_actual_elapsed_hours(tmp_path, start, end, energy, hours):
    c = fixture_case(tmp_path, zone="Europe/Berlin",
                     native_intervals=[(start, end, energy)])
    result = run(c)
    assert result["interval_energy_ledger"].native_duration_h.iloc[0] == hours
    assert len(result["hydro_inflow"]) == hours
    assert all(result["hydro_inflow"].value == 2.0)
    assert result["hydro_inflow"].value.sum() == pytest.approx(energy)


@pytest.mark.parametrize("tech", ["HPI", "HOL"])
def test_pondage_and_open_loop_pumped_storage_are_not_closed_loop(tmp_path, tech):
    c = fixture_case(tmp_path, tech=tech)
    result = run(c)
    assert result["hydro_inflow"].value.sum() == pytest.approx(96.0)
    assert result["closed_loop_policy_ledger"].empty


def test_qualified_ror_generator_availability_is_not_dispatch(tmp_path):
    c = fixture_case(tmp_path, tech="HRR", semantics="AVAILABLE_GENERATION_ENERGY_MWH")
    c["assets_frame"].loc[0, "component_class"] = "Generator"
    c["assets_frame"].loc[0, "existing_component_id"] = "original-ror-generator"
    c["assets_frame"].loc[0, "max_hours"] = ""
    result = run(c)
    cf = result["ror_availability"]
    assert len(cf) == 48
    assert set(cf.target_attribute) == {"generators_t.p_max_pu"}
    assert (cf.value.sub(0.2).abs() < 1e-10).all()
    assert result["hydro_inflow"].empty


def test_closed_loop_without_natural_inflow_is_recorded_not_zero_filled(tmp_path):
    c = fixture_case(tmp_path)
    extra = c["assets_frame"].iloc[0].copy()
    extra["asset_id"] = "original-HCL"
    extra["hydro_tech"] = "HCL"
    extra["existing_component_id"] = "original-HCL-storage"
    c["assets_frame"] = pd.concat([c["assets_frame"], extra.to_frame().T], ignore_index=True)
    c["manifest"]["closed_loop_no_natural_inflow"] = [{
        "asset_id": "original-HCL",
        "policy": "NO_NATURAL_INFLOW_BY_DESIGN",
        "evidence_ref": "FIXTURE_APPROVED_CLASSIFICATION",
    }]
    result = run(c)
    assert "original-HCL" not in set(result["hydro_inflow"].asset_id)
    assert len(result["closed_loop_policy_ledger"]) == 1
    assert result["closed_loop_policy_ledger"].value.iloc[0] == "NOT_APPLICABLE_NO_NATURAL_INFLOW"
    assert result["qa"]["existing_hydro_assets_covered"] == 2


def test_preexisting_approved_store_link_inflow_port_staged_separately(tmp_path):
    c = fixture_case(tmp_path)
    c["assets_frame"].loc[0, "component_class"] = "Store"
    c["assets_frame"].loc[0, "existing_component_id"] = "original-store-23"
    c["assets_frame"].loc[0, "e_nom_mwh"] = "100"
    port = c["assets_frame"].iloc[0].copy()
    port["asset_id"] = "internal-approved-port"
    port["component_class"] = "Generator"
    port["existing_component_id"] = "original-inflow-port"
    port["role"] = "INFLOW_PORT"
    c["assets_frame"] = pd.concat([c["assets_frame"], port.to_frame().T], ignore_index=True)
    c["allocations"].loc[0, "port_generator_id"] = "original-inflow-port"
    c["allocations"].loc[0, "port_approval_ref"] = "FIXTURE_APPROVED_M0_PORT"
    c["allocations"].loc[0, "allowlist_approved"] = "YES"
    result = run(c)
    assert result["hydro_inflow"].empty
    assert len(result["store_link_staged"]) == 48
    assert result["store_link_staged"].value.sum() == pytest.approx(96)
    assert set(result["store_link_staged"].target_attribute) == {"generators_t.p_set"}
    assert result["qa"]["non_default_store_link_ports_staged"]


def test_true_sourced_zero_remains_zero_with_provenance(tmp_path):
    c = fixture_case(tmp_path, native_intervals=[
        ("2026-01-01T00:00:00+00:00", "2026-01-02T00:00:00+00:00", 0.0)
    ])
    result = run(c)
    assert all(result["hydro_inflow"].value == 0)
    assert len(result["interval_energy_ledger"]) == 1
    assert result["interval_energy_ledger"].source_sha256.iloc[0] == c["manifest"]["sources"][0]["sha256"]
    assert result["qa"]["zero_fallback_count"] == 0
