# P5 → actual pinned P1 bridge: controlled negative operator probes

**Execution:** isolated V8 JS, `P5-P1-NEGATIVE-CBA-OPERATORS-V8-20261124-r0.1`. The original P1 `tools/candidate_b_bridge.js` was fetched from immutable commit `506be1607e1e8a6eb50db2f1317961d5bbaffcce`, blob `34f280487ec03e9de7c097b6351d9e147211af30`, and executed in memory (no modifications to P1).

- Control: unchanged supported typed RC01 fixture via `makeRc01()` yields `BLOCKED` because Owner decision remains `OWNER_TBD`. It is *not* a full CBA.
- Four controlled probes replaced **one expression/projection** in that otherwise supported fragment with candidate generic CBA-semantic operations. All four returned `FAIL_STATIC` and `UNKNOWN_PREDICATE_OPERATOR`.
- Expressions tested: `sameExogenousSnapshot`, `pairedDelta`, `weightedAggregate`, `discountedValue`.
- **Observed 4/4 expected negative rejections**. This proves only that the currently pinned P1 bridge does not recognize these four proposed operators. It does **not** prove that a new primitive syntax is necessary: some may be composed from other typed operations or expressed by a reusable standards profile. A full CBA source/parser/AST/CSNF/Validator chain remains NOT_EXECUTED. The pinned C21 **Python validator was not invoked**.

| Probe | Outcome |
|---|---|
| P5_X01_COUNTERFACTUAL_SAME_EXOGENOUS | `FAIL_STATIC`, `UNKNOWN_PREDICATE_OPERATOR, PREDICATE_NOT_BOOL3, OWNER_UNRESOLVED, OWNER_UNRESOLVED` |
| P5_X02_PAIRED_DELTA | `FAIL_STATIC`, `UNKNOWN_PREDICATE_OPERATOR, PREDICATE_NOT_BOOL3, OWNER_UNRESOLVED, OWNER_UNRESOLVED` |
| P5_X03_WEIGHTED_AGGREGATION | `FAIL_STATIC`, `UNKNOWN_PREDICATE_OPERATOR, PREDICATE_NOT_BOOL3, OWNER_UNRESOLVED, OWNER_UNRESOLVED` |
| P5_X04_DISCOUNTED_OBSERVABLE | `FAIL_STATIC`, `OWNER_UNRESOLVED, OWNER_UNRESOLVED, UNKNOWN_PREDICATE_OPERATOR, OBSERVABLE_PROJECTION_TYPE` |

Raw record: `data/p1_operator_negative_execution.json`. These tests are **additional** to the 36 independent P5 domain oracle checks and must not be aggregated into a misleading conformance percentage. Gate B1 remains `B1_PARTIAL`, not met.
