"""Conformance tests: execution on illustrative input fixtures only."""
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
from validator import load, validate  # noqa: E402
from run_tests import EXPECTED, run  # noqa: E402


class WeatherManifestContractTests(unittest.TestCase):
    def test_input_accept_reject_fixture_suite(self):
        for case, expected in EXPECTED.items():
            with self.subTest(case=case):
                self.assertEqual(validate(load("examples/" + case))["status"], expected)

    def test_independent_adapter_formats_normalize_to_same_scenarios(self):
        a = validate(load("examples/valid_2035_rows.json"))
        b = validate(load("examples/valid_2035_map.json"))
        self.assertEqual(a["status"], "PASS")
        self.assertEqual(b["status"], "PASS")
        self.assertEqual(a["canonical"]["study_year"], b["canonical"]["study_year"])
        def by_id(data):
            return {row["id"]: row["weight"] for row in data["canonical"]["scenarios"]}
        self.assertEqual(by_id(a), by_id(b))

    def test_generated_report_schema_and_expected_rejections(self):
        report = run()
        Draft202012Validator(load("report.schema.json")).validate(report)
        self.assertTrue(report["all_expected_results_observed"])
        self.assertEqual(report["test_count"], 11)
        self.assertEqual(report["pass_count"], 4)
        self.assertEqual(report["reject_count"], 7)

    def test_exact_registered_horizons_and_weights(self):
        c = load("contract.json")
        self.assertEqual(set(c["target_years"]), {"2035", "2040", "2050"})
        for year, rows in c["target_years"].items():
            with self.subTest(year=year):
                self.assertEqual(len(rows), 3)
                self.assertAlmostEqual(sum(r["weight"] for r in rows), 1.0)


if __name__ == "__main__":
    unittest.main()

