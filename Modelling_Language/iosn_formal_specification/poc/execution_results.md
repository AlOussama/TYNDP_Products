# Recorded local PoC execution — 2026-11-04

**Runtime:** Python 3.13.5; jsonschema 4.26.0. **Executables:** `python poc/run_tests.py` and `python -m unittest discover -s poc/tests -v`.

~~~text
Test cases: 11; valid accepted: 4; invalid rejected: 7; all match: True

test_exact_registered_horizons_and_weights ... ok
test_generated_report_schema_and_expected_rejections ... ok
test_independent_adapter_formats_normalize_to_same_scenarios ... ok
test_input_accept_reject_fixture_suite ... ok

Ran 4 tests in 0.014s
OK
~~~

|Fixture|Observed|Falsified rules on rejected fixtures|
|---|---|---|
|valid_2035_rows.json|PASS|none|
|valid_2035_map.json|PASS|none|
|valid_2040_rows.json|PASS|none|
|valid_2050_rows.json|PASS|none|
|invalid_wrong_weight_rows.json|FAIL|R03_EXACT_WEIGHTS, R04_SUM|
|invalid_duplicate_rows.json|FAIL|R02_IDS, R03_EXACT_WEIGHTS|
|invalid_missing_weather_map.json|FAIL|R02_IDS, R03_EXACT_WEIGHTS, R04_SUM|
|invalid_negative_rows.json|FAIL|R03_EXACT_WEIGHTS, R04_SUM, R05_FINITE_NONNEGATIVE|
|invalid_bad_year_rows.json|FAIL|R01_YEAR|
|invalid_bad_source_rows.json|FAIL|R06_SOURCE|
|invalid_missing_provenance_rows.json|FAIL|R00_INPUT_SCHEMA|

`verification_report.json` is a **compact reconstruction of the observed checks** from that execution, to keep an auditable machine-readable summary in GitHub. Running `python poc/run_tests.py` regenerates the **full detailed report** with runtime messages. This is not a CI attestations/signature and does not imply that code was executed **inside GitHub**; it was executed in the analysis environment. No energy optimisation model, external adapter or weather-year selection algorithm was executed.

**Known result limitations:** synthetic inputs; 2026 consultation source; no real weather-feature preprocessing; no PyPSA, Antares, Sienna execution; acceptance threshold `1e-12` X engineer-chosen.
