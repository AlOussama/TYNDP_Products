# Executed independent CBA synthetic micro-oracles

## Run status (not grammar)
- Run: `P5-CBA-SYNTHETIC-V8-20261124-r0.1`, isolated V8 JavaScript execution.
- Source: `tools/cba_stress_oracle.js`, runner `tools/test_cba_stress_oracle.js`.
- **36/36 checks PASS:** six positive witness/property checks plus thirty targeted negative mutations. The full response is preserved in `data/executed_v8_micro_oracle_results.json`; oracle expectations in code and fixture IDs in `data/negative_case_manifest.json`.
- Test environment engine version was not exposed; repository Node.js CLI is provided but a pinned Node.js CI run **NOT_EXECUTED**. No source code from C20/C21 was invoked in P5.

## Positive samples actually checked
1. Base research fixture is internally consistent with `OWNER_TBD` still a blocker.
2. Two model-labelled results have different NPV proxy signs.
3. E3/E4/E5 are explicitly **not** inferred from those numbers.
4. Reversing sample order leaves computed synthetic result unchanged.
5. Model result divergence is treated as sensitivity rather than an automatic static defect.
6. Not-executed indicators are not converted to numeric zero.

## Negative tests (independent domain-oracle only)
| ID | Expected diagnostic |
|---|---|
| M01 | `PAIR_INCOMPLETE` |
| M02 | `EXOGENOUS_SNAPSHOT_DRIFT` |
| M03 | `SCENARIO_WEIGHT_INVALID` |
| M04 | `SCENARIO_WEIGHT_SUM` |
| M05 | `OUTPUT_BASIS_MISMATCH` |
| M06 | `OUTPUT_BASIS_MISMATCH` |
| M07 | `BENEFIT_SIGN_CONVENTION` |
| M08 | `COST_PROXY_MISLABELED_AS_SEW` |
| M09 | `UNSUPPORTED_OWNER_APPROVAL` |
| M10 | `EVIDENCE_PROMOTION_UNSUPPORTED` |
| M11 | `SOURCE_LEDGER_LOSS` |
| M12 | `MODEL_VARIATION_NOT_DISCLOSED` |
| M13 | `PROJECT_SCOPE_DRIFT` |
| M14 | `PROJECT_DELTA_MISASSIGNED` |
| M15 | `CROSS_MODEL_PAIRING_FORBIDDEN` |
| M16 | `TIME_SUPPORT_INVALID` |
| M17 | `UNKNOWN_COERCED_TO_NUMBER` |
| M18 | `CARRIER_UNIT_TYPE_MISMATCH` |
| M19 | `PROJECT_DELTA_MISASSIGNED` |
| M20 | `DISCOUNT_POLICY_INVALID` |
| M21 | `INDEPENDENCE_IDENTITY_COLLISION` |
| M22 | `DISCOUNT_CURRENCY_BASIS` |
| M23 | `WEIGHT_ROLE_CONFLATION` |
| M24 | `OBSERVABLE_SELECTION_UNDEFINED` |
| M25 | `UNKNOWN_SAMPLE_REFERENCE` |
| M26 | `CONSULTATION_SOURCE_PROMOTION` |
| M27 | `METHOD_PROFILE_UNVERSIONED_OR_PREMATURE` |
| M28 | `KPI_DOUBLE_COUNTING_POLICY` |
| M29 | `STAGE1_INFORMATION_LEAKAGE` |
| M30 | `E4_UNSUPPORTED` |

Detection is only for *predefined* mutations in a finite independent evaluator. This is useful as a **future language-implementation test oracle**, not proof that the language parser or static validator currently recognizes them. Do not label `REFERENCE_CASE_EXECUTION=30` for CSNF; it is `CBA_SYNTHETIC_MICRO_ORACLE=36/36`, `CBA_LANGUAGE_FULL_RUNS=0`.
