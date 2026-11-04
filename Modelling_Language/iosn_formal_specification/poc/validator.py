"""Executable fixture-only IoSN weather-manifest validation; NOT production ENTSO-E certification."""
from __future__ import annotations

import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent


def load(filename: str):
    with (ROOT / filename).open(encoding="utf-8") as handle:
        return json.load(handle)


def normalize(payload):
    """Different upstream layouts, same canonical method-signature data."""
    if payload["adapter_type"] == "rows_v1":
        records = [{"id": row["weather_id"], "weight": row["weight"]}
                   for row in payload["records"]]
        return {"study_year": payload["study_year"],
                "source_ref": payload["source_ref"],
                "run_id": payload["run_id"], "dataset_id": payload["dataset_id"],
                "adapter_type": "rows_v1", "scenarios": records}
    if payload["adapter_type"] == "map_v1":
        records = [{"id": ident, "weight": weight}
                   for ident, weight in payload["weight_map"].items()]
        return {"study_year": payload["horizon"],
                "source_ref": payload["methodology"],
                "run_id": payload["run"], "dataset_id": payload["dataset"],
                "adapter_type": "map_v1", "scenarios": records}
    raise ValueError("Unsupported adapter type; no implicit default")


def validate(payload):
    contract = load("contract.json")
    checks = []

    def check(rule_id, condition, detail):
        checks.append({"id": rule_id, "status": "PASS" if bool(condition) else "FAIL",
                       "detail": detail})

    errors = sorted(Draft202012Validator(load("input.schema.json")).iter_errors(payload),
                    key=lambda e: str(e.path))
    if errors:
        check("R00_INPUT_SCHEMA", False, " / ".join(e.message for e in errors))
        return {"status": "FAIL", "checks": checks, "canonical": None}
    check("R00_INPUT_SCHEMA", True, "Input data matches one declared adapter profile")

    canonical = normalize(payload)
    errors = sorted(Draft202012Validator(load("canonical.schema.json")).iter_errors(canonical),
                    key=lambda e: str(e.path))
    check("R00_CANONICAL_SCHEMA", not errors,
          "Canonical shape valid" if not errors else " / ".join(e.message for e in errors))
    if errors:
        return {"status": "FAIL", "checks": checks, "canonical": canonical}

    year = str(canonical["study_year"])
    expected = contract["target_years"].get(year)
    check("R01_YEAR", expected is not None, "Selected target year belongs to O26 section 3.7")
    if expected is None:
        return {"status": "FAIL", "checks": checks, "canonical": canonical}

    observed = canonical["scenarios"]
    expected_ids = {row["id"] for row in expected}
    observed_ids = [row["id"] for row in observed]
    check("R02_IDS", len(observed_ids) == len(expected) and
          len(set(observed_ids)) == len(observed_ids) and set(observed_ids) == expected_ids,
          "Exact unique published weather scenario ID set")

    tol = contract["tolerance"]
    expected_weights = {row["id"]: row["weight"] for row in expected}
    check("R03_EXACT_WEIGHTS", len(observed) == len(expected) and all(
          row["id"] in expected_weights and
          math.isfinite(row["weight"]) and
          abs(row["weight"] - expected_weights[row["id"]]) <= tol for row in observed),
          "Each ID has the published probability within demonstrator-only tolerance")

    numeric = all(math.isfinite(row["weight"]) for row in observed)
    check("R04_SUM", numeric and abs(sum(row["weight"] for row in observed)-1.0) <= tol,
          "Weather probabilities sum to 1 within demonstrator tolerance")
    check("R05_FINITE_NONNEGATIVE", numeric and all(row["weight"] >= 0 for row in observed),
          "Weather probabilities are finite and nonnegative")
    check("R06_SOURCE", canonical["source_ref"] == contract["authority"]["source_ref"],
          "Source reference matches consultation text O26 section 3.7")
    check("R07_PROVENANCE", all(
          isinstance(canonical[k], str) and bool(canonical[k].strip())
          for k in ("run_id", "dataset_id")),
          "Source dataset and run lineage supplied")

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    return {"status": status, "checks": checks, "canonical": canonical}

