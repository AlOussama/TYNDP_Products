# ML-C21/12 – Executed B1 cross-workstream schema compatibility negative probe
Research-r0.1 | 2026-11-23 | NON-NORMATIVE. Common immutable B0 base `2f0297b754e3a96a2523a34d3af98782b26181f3`. G1 BLOCKED.

## Direct evidence / limitations
Executed locally with Python 3.13.5 and the pinned ML-C21 `tools/csnf_validator.py`. Input is a transcription of the illustrative **RC01 Candidate-B JSON sketch** in ML-C20/07, preserving all fields and values (but reformatted), saved under `data/b1_c20_candidate_b_rc01.json`. Command from this workstream's `tools/` directory: `python b1_fixture_check.py` (the script is runnable there, loads `../data/`). This is **NOT** a parsed ML-C20 full syntax specimen or full positive adapter, and C20 has no executable parser.

Observed B1 outcome: `INCOMPATIBLE_EXPECTED`, with `VERSION_MISMATCH` ERROR at `$.frame.schema`, `VERSION_MISMATCH` ERROR at `$.frame.registry`, `OWNER_STATE` ERROR at `$.authorities[0].decision`, plus `OWNER_UNRESOLVED` BLOCKED at `$.assertions[0].decision`. `normalize` rejects the input. This is a **successful detection of cross-interface incompatibility**, not a successful B1 integration, not a test of energy-model conformance.

## Design incompatibilities and potential silent losses
| Mismatch | Evidence from interfaces | Required B1 resolution |
|---|---|---|
| Schema/registry version | C20 example `C20-research-0.1 / energy-r0` vs C21 `CSNF-C21-0.1 / energy-c21-0.1` | versioned adapter; no one-off hidden override |
| Authority decision discriminator | C20 `authorities[].decision_state` vs C21 expects `authorities[].decision` | typed mapping preserving separate C9 source/owner statuses |
| Port kind | C20 `kind: external_port` vs C21 only runs quantity checks on `kind: port` | reject unknown discriminators and verify port carrier/unit/sign rather than skipping |
| Observable payload | C20 uses untyped explanatory `semantics` text; C21 cannot validate price/time/quantity projection | typed C6 observable/projector, loss test |
| Predicate payload | C20 `contractPredicate` placeholder; C21 does not typecheck operators/quantifiers | explicit typed operator registry with A/G, time and scenario domain semantics |
| Independent oracle | C23 `data/golden_cases.json` is descriptive preregistered oracle, not executable typed fixture | deterministic case-to-typed-fragment test fixture with separate oracle version |
| Standard maps | C22 `data/mapping_registry.json` is conceptual, no native SysML/GEMS/mathspec output | perform native parse/type/export/import and audit roundtrip before acceptance |

`OWNER_UNRESOLVED` correctly remains BLOCKED regardless of schema fixes; the design must not normalize it to APPROVED. No E1/E2/E3/E4/E5 conformance statement follows from this failed handshake.

## Gate decision
**B1 = NOT_MET (one executed negative compatibility probe, zero successful integrated adapters).** B2 = NOT_MET (incomplete proof/case matrix, no native roundtrips, missing human study). B3 = NOT_STARTED; ML-C24 must remain gated until versioned interoperable inputs and comparable executed outcomes exist. Re-run exactly these negative witnesses after any schema revision and add complete positive and negative RC01–10 fixtures before a B1-ready label.

Source: [ML-C20/07](https://github.com/AlOussama/TYNDP_Products/blob/research/ml-c20-study-contract-language-2026-11-23/Modelling_Language/study_contract_language/workstreams/ML_C20_language_syntax_research/07_reference_case_syntax_examples.md) and ML-C21/02-06. AI-internal critical review only; independent human audit NOT_EXECUTED.
