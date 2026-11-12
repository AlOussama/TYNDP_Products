# ML-C01 — Multidimensional Status & Applicability Ontology

**Research ontology, v0.1 (12 November 2026).** Derived from ML-R02 progression, ML-R03 source/data semantics and ML-R04 six test statuses. **No status in this file grants source adoption, model certification, independent human approval or Gate G1. G1=BLOCKED.**

## 1. State vector rather than single PASS

An object or claim carries a **product state** whose dimensions are **not mutually substitutable**:

~~~text
SemanticStatusVector {
  record_id, record_type, profile_revision, scope, applicable_guard,
  research_maturity,                   // conceptual drafting maturity
  source_authority,                    // exact method revision and normative validity
  decision_authority,                  // project D1–D6 vs open MD/CL
  original_data_qualification,        // actual source payload qualification
  structural_integrity,               // keys/types/FKs/units on a named artifact
  semantic_validation,                // domain meaning and transformation preservation
  mathematical_verification,          // generated physics/objective/candidate obligations
  numerical_verification,             // solver/analytic witness and residuals
  output_kpi_verification,            // formula/aggregation/replay
  evidence_integrity,                 // hashes, scope, oracle and execution provenance
  independent_review,                 // actual person/organization signoff
  gate_g1,                            // governing gate state, kept separate
  tests: [{test_id, assertion_id, fixture_kind, V_dimension,
           test_depth, applicability, test_status, cause_code, evidence_refs}]
}
~~~

This is **logical pseudostructure**, not a selected JSON Schema or DSL. The type constraints prohibit casting one field's favorable value into another field.

| Axis | Canonical research-facing values/examples | Source origin and separation |
|---|---|---|
| Research maturity | DRAFT, STRUCTURALLY_REVIEWED, RESEARCH_SEMANTICS_DOCUMENTED, OPEN_OWNER_DETAIL | R02 lifecycle: SCHEMA_CHECKED is structural only; a later APPROVED would require an actual owner act |
| Source authority | CONSULTATION_DOCUMENTED, HISTORICAL_CONTEXT, REFERENCED_EXTERNAL_ONLY, AUTHORITY_UNCONFIRMED, ADOPTED_WITH_EVIDENCE (future only) | R01/O26 and ML-R00; source authenticated != adopted |
| Governance decision | PROJECT_DECISION_CONFIRMED_RESEARCH_SCOPE, OPEN_NOT_OWNER_APPROVED, OWNER_APPROVED_WITH_RECORD (future only) | D1–D6 separate from 21 MD/CL |
| Original data qualification | NOT_QUALIFIED, SOURCE_UNVERIFIED, QUALIFIED_WITH_ORIGINAL_BYTES (future), NOT_APPLICABLE_TO_SYNTHETIC | R03: 87 objects defined != 87 released datasets; 0/28 real BUNDLE validation tests |
| Structural integrity | NOT_CHECKED, STRUCTURALLY_VALID, STRUCTURALLY_INVALID | A schema pass does not resolve source or mathematical correctness |
| Domain/semantic validation | NOT_ASSESSED, PROPOSED_WITH_TBD, VALIDATED_FOR_SPECIFIED_SCOPE, COUNTEREXAMPLE_FOUND | Requires distinct domain evidence; not a free extension of structural PASS |
| Mathematical verification | NOT_EXECUTED, BLOCKED_ORACLE, ASSERTION_VALIDATED_SCOPE, ASSERTION_VIOLATED_SCOPE | R01 M01–M18, R04 V3; no native model execution at baseline |
| Numerical verification | NOT_EXECUTED, BLOCKED_TOLERANCE, FEASIBLE_OPTIMAL_WITH_EVIDENCE, COUNTEREXAMPLE_FOUND | R04 V4; solver OPTIMAL alone insufficient |
| Output/KPI | METRIC_UNDEFINED_TBD_OWNER, NOT_EXECUTED, RECOMPUTED_SCOPED, MISMATCH_CONFIRMED | Definition/formula separate from computed value (MD-04/17) |
| Evidence integrity | NOT_CAPTURED, SYNTHETIC_ONLY, STRUCTURAL_TRACE_ONLY, EXECUTED_VERIFIABLE, ORACLE_UNAPPROVED | R04 E01–E08 and V6; self-review ≠ independent signoff |
| Independent review | NOT_OBTAINED, INTERNAL_ADVERSARIAL_ONLY, INDEPENDENT_REVIEWED_WITH_RECORD (future) | Same-AI critical review never accepted as independent qualified approval |
| Gate | G1_BLOCKED, G1_APPROVED_WITH_RECORD (future) | **Only** responsible governance owner may set gate outcome |

These are **suggested canonical interpretations**, not a modification of source R02/R03/R04 status enum fields. Preserve original upstream values and use an explicit mapping into this tuple with origin and version.

## 2. Strict scoped six-state test outcome

The **only** R04 *individual assertion execution* statuses are:

| test_status | Preconditions/meaning | Effect on applicable mandatory claim |
|---|---|---|
| **PASS** | Test actually executed for explicitly stated fixture_kind, tool/version, inputs, assertion, **accepted** oracle/tolerance where needed; complete evidence and applicable preconditions; property holds | Supports *only that property and scope*, not other axes or G1 |
| **FAIL** | Applicable executed test has an independently reproducible violation of a required property (e.g., positive KVL residual beyond approved tolerance) | Inhibits required scoped conformance |
| **BLOCKED** | Cannot evaluate because necessary authority, domain meaning, original data, oracle, right, tolerance or antecedent is unresolved | Inhibits required scoped conformance; not scientific falsification |
| **UNSUPPORTED** | Applicable required capability cannot be implemented by the tool; absence evidenced by capability manifest/probe | Inhibits required scoped conformance; cannot be relabelled N/A |
| **NOT_EXECUTED** | Test has not been run on the claimed target, though no known unsupported capability is asserted; planned/self-check only | Inhibits required scoped conformance |
| **NOT_APPLICABLE** | Specific conditional antecedent **demonstrably false**, with configuration or domain evidence and no execution of that mode | Excludes **only** that test from applicable denominator; no general PASS |

Fixture kind is a **separate mandatory field** for test claims: SYNTHETIC_FIXTURE, RESEARCH_STRUCTURE, NATIVE_TOOL_RUN, ORIGINAL_DATA_VALIDATION or further explicitly named research types. Test result PASS for a synthetic case is valid only for **that fixture**, while native model conformance remains NOT_EXECUTED. Do not add PASS_SYNTHETIC as a seventh core status; store scope separately.

## 3. Applicability logic: mandatory, conditional and optional

Use guard truth values T (evidenced true), F (evidenced false), U (unresolved) and obligation kind REQUIRED, CONDITIONAL, OPTIONAL. **An absent guard value is U, not F.**

| Obligation | Guard | Target applicability | Test consequence before execution |
|---|---|---|---|
| REQUIRED | N/A | APPLICABLE | capability/source/oracle/execution check required |
| CONDITIONAL | T | APPLICABLE_REQUIRED | source/oracle/capability/execution check required |
| CONDITIONAL | F and evidence | NON_APPLICABLE | NOT_APPLICABLE with exact guard/ref |
| CONDITIONAL | U | UNDETERMINED | BLOCKED (guard unknown); **not** NOT_APPLICABLE |
| OPTIONAL feature selection | T | feature enabled ⇒ its conditional rules REQUIRED | check all feature-specific obligations |
| OPTIONAL feature selection | F with proven disabled configuration | feature-specific rules NON_APPLICABLE | NOT_APPLICABLE only for the optional extension |
| OPTIONAL feature selection | U / omitted ambiguous config | UNDETERMINED | BLOCKED on feature-specific applicability |

**P15 case (SR-026):** guard OPF_SELECTED. If false *and documented*, P15/R04-T-SR-026=N/A. If true, LF portfolio capping is mandatory; violating the cap after an executed test is FAIL. If the tool does not support required OPF while the selected profile requires it, UNSUPPORTED. If flag or run manifest is ambiguous, BLOCKED. **Other mandatory LF, P13 and H2/scope tests do not become N/A.**

**Optional vs condition:** It is the decision to invoke OPF that is optional, *not* the conformance of an OPF experiment once chosen. Neither a missing OPF output file nor a successful LF test is evidence of OPF_SELECTED=false. An evidence-backed feature flag plus run manifest is required.

## 4. Evaluation and aggregation (D3 fail-closed)

Evaluation order is a **research policy**, retained from R04 where possible:

1. Validate identity, source profile, applicable assertions and evidence of the guard.
2. If guard is proven F for a conditional obligation, record NOT_APPLICABLE only for that test.
3. If required capability absent, record UNSUPPORTED.
4. If authoritative interpretation/inputs/accepted oracle/tolerance/guard unresolved, record BLOCKED.
5. If test not actually executed on the asserted target, record NOT_EXECUTED.
6. For executed, fully evidenced, applicable assertion record PASS or FAIL against the correct oracle.

**No automatic PASS propagation:** For a mandatory test set A, scoped success can be considered *only when each applicable mandatory test is PASS with sufficient scope*, and each separate source, data, mathematical, output and independent-review/gate predicate needed for that claim is satisfied. If any is FAILED/BLOCKED/UNSUPPORTED/NOT_EXECUTED, scoped full conformance is not established. The research snapshot has **zero native-tool executed tests**; its structural join and synthetic cases cannot change this.

For a *display-only test summary*, R04 proposes FAIL > UNSUPPORTED > BLOCKED > NOT_EXECUTED > PASS; exclude evidenced N/A first and retain the complete vector and cause. This is **not** a single order or lattice allowing cross-axis success; if all tests are N/A, set empty-scope/N/A, never universal PASS. If owner authority or review is still absent, even “all tests PASS on a fixture” cannot be promoted into full conformance.

## 5. Explicit non-implications / monotonicity firewall

A test status is indexed by (test_id, requirement_id, assertion_revision, source_profile, tool/model_version, input_set, weather case set, study_year, stage/mode, fixture_kind, oracle_revision, tolerance_revision). A PASS at one tuple **does not imply** a PASS at another tuple.

| Premise | Not logically entailed |
|---|---|
| R02 A/B validator PASS | mathematical obligation satisfied, native tool supported or architecture chosen |
| R03 fixture schema PASS | original source data qualified or correct source provenance |
| R04 arithmetic oracle PASS | any native energy model executed or independent reviewer agreed |
| MA01 48/48 cross-reference integrity | source authority, approved content, SR coverage *semantics*, or 48/48 model tests |
| Model solver returns OPTIMAL | formulation correct, model feasible in intended physics, KPI definition valid |
| Two tools produce equal objective | identical feasible set, project needs, physics or valid published method |
| Output KPI recomputed | KPI formula approved, data source released or system need a construction project |
| All applicable synthetic tests PASS | SOURCE_APPROVED, DATA_QUALIFIED, C_FULL, independent review, G1_APPROVED |

A later successful test provides new evidence on its **own axis** but cannot erase prior source history or owner dependencies without a controlled decision. Even future owner approval is scoped by effective dates and versions; it does not rewrite history.

## 6. Per-test examples and countercases

| Event | Correct tuple facts |
|---|---|
| Nonanticipativity constraint absent; tool incapable of shared x | applicability=T, capability=UNSUPPORTED; mathematical claim not established |
| Actual witness violates KCL/KVL in required model, with accepted tolerance | executed=true, test=FAIL, retained counterexample |
| Network reduction RMSE threshold unresolved | owner oracle TBD, test=BLOCKED; **not FAIL** without an executed violation |
| Optional P15 not selected, proven by signed config and no OPF run | SR-026=NOT_APPLICABLE; SR-024/025 remain applicable |
| OPF selected, candidate expansion greater than LF portfolio | SR-026=FAIL if executed and independently evidenced; optionality does not waive constraints |
| R04 C01 synthetic expected value matches | fixture_kind=SYNTHETIC_FIXTURE + test=PASS locally; NATIVE_TOOL_RUN=NOT_EXECUTED |
| Same-AI critical review of all docs | independent_review=INTERNAL_ADVERSARIAL_ONLY; actual signoff NOT_OBTAINED |
| Missing original O26 adopted authority | source_authority=AUTHORITY_UNCONFIRMED; G1_BLOCKED independent of schema results |

## 7. Audit and mapping obligations

Maintain **original source status strings** as source payloads plus the canonical mapped value. Every mapped status has source workstream, source file/revision, scope, decision rationale and conflict reference. An unrecognized source status is mapping=UNRESOLVED rather than implicitly PASS/APPROVED. Capture eight R04 E-ports (E01–E08), V1–V6 axes and D0–D4 test-depth labels separately; none is a status itself. Tier A/B/C are **proposed risk priorities** and cannot be converted into stronger scientific confidence in the absence of additional proof.

The stable record of independent review contains reviewer identity/affiliation, independence declaration, exact artifact versions, methods, findings, evidence, decision and signature; ML-C01 supplies **none** of these official attestations. G1 remains **BLOCKED** until the real later gate action.

## 8. References

[R04 failure/evidence semantics](../ML_R04_verification/failure_and_evidence_semantics.md); [R04 risk policy](../ML_R04_verification/risk_based_conformance_policy.md); [R02 language status](../ML_R02_language_architecture/language_requirements_specification.md); [R03 source/data state model](../ML_R03_data_process_contracts/iosn_data_semantic_model.md); [R00 INT-03 and INT-15](../ML_R00_consolidation/cross_workstream_consistency_review.md).
