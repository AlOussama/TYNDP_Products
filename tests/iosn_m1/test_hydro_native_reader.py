# SPDX-License-Identifier: MIT
"""Physically shaped Open-TYNDP WEEK files, but synthetic values/evidence."""
import pandas as pd
import pytest

from scripts.iosn_m1.hydro.adapter import HydroContractError, file_sha256
from scripts.iosn_m1.hydro.normalize_tyndp2026 import normalize_tyndp2026


def prepared(tmp_path):
    raw = tmp_path / "DE_FIXTURE_Hydro_Inflows_HRI_2030.csv"
    bounds = tmp_path / "WEEK_BOUNDS_ORIGINAL_EVIDENCE_FIXTURE.csv"
    target = tmp_path / "normalized.csv"
    pd.DataFrame({"WEEK": [1, 2], "WS003": [168, 48],
                  "WS021": [336, 96]}).to_csv(raw, index=False)
    pd.DataFrame({
        "period_key": ["1", "2"],
        "start": ["2026-01-01T00:00:00+00:00", "2026-01-08T00:00:00+00:00"],
        "end": ["2026-01-08T00:00:00+00:00", "2026-01-10T00:00:00+00:00"],
    }).to_csv(bounds, index=False)
    kwargs = dict(
        source_column="WS003", selected_weather_id="FIXTURE-WS-01",
        timezone="UTC", expected_raw_sha256=file_sha256(raw),
        expected_bounds_sha256=file_sha256(bounds),
        native_unit="MWh", source_version="FIXTURE-not-actual-2026-release",
        bounds_evidence_ref="FIXTURE-bounds",
    )
    return raw, bounds, target, kwargs


def test_exact_ws_column_and_original_partial_week_boundaries(tmp_path):
    raw, bounds, target, kw = prepared(tmp_path)
    evidence = normalize_tyndp2026(raw, bounds, target, **kw)
    result = pd.read_csv(target)
    assert result.energy_mwh.tolist() == [168, 48]
    assert result.end.iloc[-1] == "2026-01-10T00:00:00+00:00"
    assert evidence["source_column"] == "WS003"
    assert evidence["zero_fallback_count"] == 0
    assert evidence["normalized_file_sha256"] == file_sha256(target)
    assert evidence["native_interval_count"] == 2


def test_unavailable_ws_is_never_replaced_by_first_filled_ws(tmp_path):
    raw, bounds, target, kw = prepared(tmp_path)
    kw["source_column"] = "WS029"
    with pytest.raises(HydroContractError, match="WS column absent"):
        normalize_tyndp2026(raw, bounds, target, **kw)
    assert not target.exists()


def test_invented_168h_for_partial_week_rejected_by_bijection(tmp_path):
    raw, bounds, target, kw = prepared(tmp_path)
    df = pd.read_csv(bounds).iloc[:1]
    df.to_csv(bounds, index=False)
    kw["expected_bounds_sha256"] = file_sha256(bounds)
    with pytest.raises(HydroContractError, match="bounds missing"):
        normalize_tyndp2026(raw, bounds, target, **kw)


def test_unverified_raw_file_is_rejected_before_normalization(tmp_path):
    raw, bounds, target, kw = prepared(tmp_path)
    kw["expected_raw_sha256"] = "0" * 64
    with pytest.raises(HydroContractError, match="SHA256 mismatch"):
        normalize_tyndp2026(raw, bounds, target, **kw)


def test_incoherent_native_intervals_cannot_be_upsampled(tmp_path):
    raw, bounds, target, kw = prepared(tmp_path)
    df = pd.read_csv(bounds)
    df.loc[1, "start"] = "2026-01-08T01:00:00+00:00"
    df.to_csv(bounds, index=False)
    kw["expected_bounds_sha256"] = file_sha256(bounds)
    with pytest.raises(HydroContractError, match="contiguous"):
        normalize_tyndp2026(raw, bounds, target, **kw)
