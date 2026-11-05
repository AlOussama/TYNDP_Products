> **MA-01 LEGACY / HISTORICAL ONLY — NOT AN ACTIVE REQUIREMENTS CATALOGUE (2026-11-05).** This research artifact predates MA-01. Sole active provisional source-derived system requirements: [iosn_requirements_catalogue.csv](iosn_requirements_catalogue.csv), with [source baseline](methodology_source_baseline.md), [process specification](iosn_process_specification.md), [scope change impact](scope_and_change_impact.md). Weather-year selection/PCA/K-Means/reproduction is **EXTERNAL / OUT OF SCOPE**, only already-selected weather inputs and consistency checks are in scope. Any old MR/SR/UC/VC/LRC/test/architecture recommendation is superseded and **not normative**. Das bestehende synthetische Wetter-Manifest-PoC wurde NICHT für MA-01 erweitert und ist kein Konformitätsnachweis für Wetterauswahl, LP, Netzreduktion oder ein echtes Tool.

---

# 10 — Minimal Executable IoSN Contract PoC

## Decision and methodological scope
**Use case:** UC-01, validation of **published weather scenario selections** and weights for target years 2035/2040/2050, [O26 §3.7, printed pp.19–20]. The producer may be any tool or preprocessing implementation, but its result must meet **one canonical externally testable artifact contract**. **Excluded:** deriving selections from PECD features via PCA/k-means [O26 Annex 6.3], running/validating an energy-system optimisation, and certification of real PyPSA/Antares/Sienna adapters.

**Contract status:** `X/NON_NORMATIVE_DEMONSTRATOR`. O26 is a consultation version. Fixture exact IDs/weights reflect O26; additional schema/provenance fields and tolerances are implementation assumptions **X** pending governance.

## Reproduction
Project root below is `Modelling_Language/iosn_formal_specification/`:

~~~bash
python -m pip install "jsonschema>=4.20,<5"
python poc/run_tests.py
python -m unittest discover -s poc/tests -v
~~~

Generated evidence: `poc/verification_report.json`. The *committed* report is from an actual execution only if its `execution_status` says `EXECUTED`, otherwise it is a declared example. Each test has a Boolean expected-vs-observed assertion. No production model is solved.

## Files and contract layers
|Artifact|Role|
|---|---|
|`poc/contract.json`|2026 target years, fixed weather IDs/weights, tolerance, method authority and metadata|
|`poc/input.schema.json`|Structure of two supported example exporter variants|
|`poc/canonical.schema.json`|Tool-independent output manifest structure|
|`poc/report.schema.json`|Verification report shape|
|`poc/validator.py`|Parser/adapters plus structural and semantic rules|
|`poc/run_tests.py`|Positive/negative cases and report generation|
|`poc/tests/test_contract.py`|unittest assertions for acceptance and rejection|
|`poc/examples/`|two mock adapter formats + targeted negative fixtures|
|`poc/verification_report.json`|actual run evidence when executed|

## Required minimum elements (explicit)
1. **Input definition:** either `rows_v1` records (list of ID/weight pairs) or `map_v1` object (keyed weights); provenance and source must be present.
2. **System Requirement:** SR-004, directly derived from O26 §3.7, with SR-001/SR-003 provenance.
3. **Process rule:** normalize export → validate schema → enforce exact year-specific IDs/weights → report evidence.
4. **Output definition:** canonical manifest with `study_year`, `scenarios`, `source_ref`, `dataset_id`, `run_id`, adapter identity.
5. **At least three rules:** R01 approved year; R02 exact unique selected IDs; R03 exact weights within X tolerance; R04 sum-to-1; R05 nonnegative/finite; R06 correct source; R07 provenance.
6. **Positive fixture:** `valid_2035_rows.json`, also `valid_2035_map.json`, `valid_2040_rows.json`, `valid_2050_rows.json`.
7. **Invalid fixtures:** wrong ID count, duplicate, wrong weights, wrong year, negative value, bad source, missing provenance.
8. **Expected results:** 4 accepted; remaining invalid fixtures rejected; runner must fail if not.
9. **Report schema:** `report.schema.json`, validated as part of the test execution.
10. **Tool independence on specification level:** both adapter formats yield the **same normalized year, scenario IDs and weights**, without using a native PyPSA, Antares or Sienna data class.

## What PoC proves and does not
- **Proves when executed:** reproducible interpretation of *this* output contract and deliberate failure of invalid fixtures; two different example exporter formats tested against one method-semantic oracle.
- **Does not prove:** the Annex 6.3 selection algorithm, upstream PECD raw data quality, adequacy of scenarios, solver/model correctness, external tool capability or official ENTSO-E acceptance.
- **No magic implicit defaults:** missing source/provenance or unsupported adapter fails.
- **Numerical tolerance of 1e-12 is X**, selected solely to test numeric JSON representation; not an O26 acceptance threshold.

## Extension to a real IoSN method validation
Sign a complete Annex 6.3 method profile with input data hashes, scaling, PCA/k-means design choices, expected intermediate features and independent oracle, followed by a second tool's actual execution and evidence. Only then could this become evidence for **selection algorithm** rather than **fixed output manifest** conformance.
