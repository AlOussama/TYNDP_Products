"""Run positive and negative fixtures and write a schema-validated evidence report."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from validator import ROOT, load, validate

EXPECTED = {
    "valid_2035_rows.json": "PASS",
    "valid_2035_map.json": "PASS",
    "valid_2040_rows.json": "PASS",
    "valid_2050_rows.json": "PASS",
    "invalid_wrong_weight_rows.json": "FAIL",
    "invalid_duplicate_rows.json": "FAIL",
    "invalid_missing_weather_map.json": "FAIL",
    "invalid_negative_rows.json": "FAIL",
    "invalid_bad_year_rows.json": "FAIL",
    "invalid_bad_source_rows.json": "FAIL",
    "invalid_missing_provenance_rows.json": "FAIL",
}


def run():
    cases = []
    for name, expected in EXPECTED.items():
        observed = validate(load("examples/" + name))
        cases.append({"case_id": name, "expected": expected, "observed": observed["status"],
                      "matches_expected": observed["status"] == expected,
                      "checks": observed["checks"]})

    report = {
        "contract_id": load("contract.json")["contract_id"],
        "execution_status": "EXECUTED",
        "test_count": len(cases),
        "pass_count": sum(c["observed"] == "PASS" for c in cases),
        "reject_count": sum(c["observed"] == "FAIL" for c in cases),
        "all_expected_results_observed": all(c["matches_expected"] for c in cases),
        "cases": cases,
        "limitations": [
            "Inputs are synthetic export fixtures; no PyPSA/Antares/Sienna run was executed.",
            "Only published weather-year manifest checked, not PCA/K-Means selection algorithm.",
            "Source O26 is the 25-Feb-2026 consultation version, not verified as final.",
            "Numeric tolerance 1e-12 is a demonstrator choice, not ENTSO-E policy."
        ]
    }
    Draft202012Validator(load("report.schema.json")).validate(report)
    with (ROOT / "verification_report.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return report


if __name__ == "__main__":
    result = run()
    print("Test cases: %s; valid accepted: %s; invalid rejected: %s; all match: %s" %
          (result["test_count"], result["pass_count"], result["reject_count"],
           result["all_expected_results_observed"]))
    raise SystemExit(0 if result["all_expected_results_observed"] else 1)

