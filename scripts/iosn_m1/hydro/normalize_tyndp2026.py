# SPDX-License-Identifier: MIT
"""Strict Open-TYNDP-2026 hydro CSV normalization with externally witnessed period bounds.

The reviewed upstream reader reindexes WEEK/DAY rows using synthetic calendar
labels and ffill / 168 or 24. This module deliberately requires actual
period start/end evidence and an exact WS column. It does NOT invent dates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from .adapter import HydroContractError, aware_utc, file_sha256, nonempty, numeric, require


def normalize_tyndp2026(
    raw_file: Path,
    bounds_file: Path,
    output_file: Path,
    *,
    source_column: str,
    selected_weather_id: str,
    timezone: str,
    expected_raw_sha256: str,
    expected_bounds_sha256: str,
    native_unit: str,
    source_version: str,
    bounds_evidence_ref: str,
) -> dict:
    """Convert an exact selected WS column to original [start,end) MWh records.

    The caller must supply independently established period bounds; 168/24 h,
    week-start inference, default dates, source substitution are prohibited.
    """
    nonempty(selected_weather_id, "selected external weather_id")
    nonempty(source_version, "TYNDP source revision")
    nonempty(bounds_evidence_ref, "original interval bounds evidence")
    require(native_unit == "MWh", "Only source intervals expressed in MWh supported")
    require(source_column.startswith("WS") and len(source_column) == 5
            and source_column[2:].isdigit(), "Explicit original WS### column required")
    for path, expected in ((raw_file, expected_raw_sha256),
                           (bounds_file, expected_bounds_sha256)):
        require(path.is_file(), "Missing raw data or bounds file: " + str(path))
        actual = file_sha256(path)
        require(len(expected) == 64 and actual == expected.lower(),
                "Native source/bounds SHA256 mismatch: " + str(path))
    require(not output_file.exists(), "Refuse overwrite of normalized hydro source")
    raw = pd.read_csv(raw_file, keep_default_na=False, dtype=str)
    require(len(raw) > 0 and raw.columns[0] in ("WEEK", "DAY"),
            "Raw Open-TYNDP hydro CSV requires explicit WEEK or DAY first column")
    period_col = raw.columns[0]
    require(source_column in raw.columns, "Requested WS column absent: " + source_column)
    require(raw[period_col].is_unique and raw[period_col].str.strip().ne("").all(),
            "Duplicate/blank native period keys")
    bounds = pd.read_csv(bounds_file, keep_default_na=False, dtype=str)
    require({"period_key", "start", "end"} <= set(bounds.columns)
            and len(bounds) == len(raw) and bounds.period_key.is_unique,
            "Original interval bounds missing, duplicated or wrong count")
    native_keys = list(raw[period_col].str.strip())
    bound_keys = set(bounds.period_key.str.strip())
    require(set(native_keys) == bound_keys,
            "Original period-key to bounds mapping is not a bijection")
    keyed = bounds.assign(period_key=bounds.period_key.str.strip()).set_index("period_key")
    records = []
    for key, value in zip(native_keys, raw[source_column]):
        start = nonempty(keyed.loc[key, "start"], "native period start")
        end = nonempty(keyed.loc[key, "end"], "native period end")
        a = aware_utc(start, timezone, "native period start")
        b = aware_utc(end, timezone, "native period end")
        hours = (b - a).total_seconds() / 3600
        require(hours > 0, "Nonpositive witnessed source period")
        require(hours <= (169 if period_col == "WEEK" else 25),
                "Witnessed period exceeds declared native WEEK/DAY maximum")
        records.append({"start": start, "end": end,
                        "energy_mwh": numeric(value, "physical native MWh")})
    for previous, current in zip(records[:-1], records[1:]):
        require(aware_utc(previous["end"], timezone, "end") ==
                aware_utc(current["start"], timezone, "start"),
                "Original source bounds must be contiguous in file order")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(output_file, index=False)
    return {
        "normalization_contract": "IOSN-M1-MA3-NATIVE-1.0.0",
        "selected_weather_id": selected_weather_id,
        "source_column": source_column, "source_version": source_version,
        "native_resolution": period_col,
        "native_unit": native_unit, "timezone": timezone,
        "raw_source_sha256": file_sha256(raw_file),
        "period_bounds_sha256": file_sha256(bounds_file),
        "period_bounds_evidence_ref": bounds_evidence_ref,
        "normalized_file_sha256": file_sha256(output_file),
        "native_interval_count": len(records), "zero_fallback_count": 0,
        "hourly_inference": "NONE_NATIVE_BOUNDS_REQUIRED",
        "raw_reader_reuse": "INSPECTED_NO_EXTERNAL_CODE_COPIED",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--raw", required=True, type=Path)
    p.add_argument("--bounds", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--source-column", required=True)
    p.add_argument("--weather-id", required=True)
    p.add_argument("--timezone", required=True)
    p.add_argument("--raw-sha256", required=True)
    p.add_argument("--bounds-sha256", required=True)
    p.add_argument("--native-unit", required=True)
    p.add_argument("--source-version", required=True)
    p.add_argument("--bounds-evidence-ref", required=True)
    a = p.parse_args()
    report = normalize_tyndp2026(
        a.raw, a.bounds, a.output, source_column=a.source_column,
        selected_weather_id=a.weather_id, timezone=a.timezone,
        expected_raw_sha256=a.raw_sha256, expected_bounds_sha256=a.bounds_sha256,
        native_unit=a.native_unit, source_version=a.source_version,
        bounds_evidence_ref=a.bounds_evidence_ref,
    )
    provenance = a.output.with_suffix(".provenance.json")
    provenance.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
