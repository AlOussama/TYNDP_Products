# ML-C05 — Applicability and Failure State Machine

**2026-11-12 · NONNORMATIVE RESEARCH PROPOSAL · ML-R00 SHA 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Object whose state is evaluated

Exactly one **atomic assertion in an identified target scope** receives one of six dispositions:

**PASS | FAIL | BLOCKED | UNSUPPORTED | NOT_EXECUTED | NOT_APPLICABLE.**

The six values are *not* a lifecycle sequence (FAIL does not naturally progress to PASS), and cannot be used as substitutes for Methodology Authority, data qualification, independent signoff, risk tier or governance approval. Record separate applicability, feature-support, execution, evidence-quality, oracle-state, scope-class and cause-code fields. A requirement with multiple assertions keeps several records; an aggregate summary must not discard them.

### 1.1 Necessary distinctions

| State | Necessary evidence | Disallowed shortcut |
|---|---|---|
| **PASS** | Applicability established; relevant test actually executed with complete witness; assertion evaluated against independently trusted oracle/tolerance **for the declared scope**; evaluated property holds | Test specification exists, syntax validated or tool self-reports PASS |
| **FAIL** | Applicable executed check or independently admissible counterexample **demonstrates** violation of that assertion, with reproducible evidence and identified conditions | Missing oracle or transient execution error asserted to be a mathematical counterexample |
| **BLOCKED** | A necessary input/source/condition/authority/oracle/tolerance/inspection artifact is unresolved, or an unclassifiable external failure makes a warranted assessment impossible | Calling missing data 'NOT_APPLICABLE', or fabricating an acceptance value |
| **UNSUPPORTED** | Applicable obligation and capability absence proven by explicit declaration + probe or equivalent reliable evidence; missing capability is required for that scope | 'Not supported, therefore not tested'; applying N/A to mandatory model physics |
| **NOT_EXECUTED** | Validly scoped test planned but no completed assertion execution, and not already more specifically classified as BLOCKED or UNSUPPORTED; null actual run/witness | Unexecuted check counted as PASS; synthetic case called native tool execution |
| **NOT_APPLICABLE** | Applicable conditional antecedent is **proven false** for exact version/run; evidence of active configuration/absence where relevant; excludes only that atomic conditional obligation | No OPF result file, unknown flag, insufficient skill/tool support, or low risk tier |

An executed negative fixture that fails *the intended wrong-model mutant* supports the **test's detection power**; it is not a FAIL of the conforming target. Use test_target_role = NEGATIVE_MUTANT vs IMPLEMENTATION_UNDER_TEST to prevent reversal.

## 2. Precedence: make eligibility, capability and proof explicit

### 2.1 Three-valued applicability

Let predicate A(q, profile, run) be an authorised conditional applicability predicate.

- **TRUE:** direct mandatory obligation, or conditional predicate with proven true antecedent.
- **FALSE_PROVEN:** only if the condition is explicitly part of the released/research-profile obligation, the condition evaluated false, and a verifiable witness exists.
- **UNKNOWN:** predicate missing, variant unclear, config hash unavailable, stage conditionality disputed or contradictory execution signals; classification BLOCKED.

Mandatory obligations do not have a FALSE_PROVEN branch by mere tool choice. An inactive optional sub-branch **never** deactivates mandatory obligations upstream.

### 2.2 State decision algorithm (conceptual, no wire format)

~~~text
evaluate(assertion q, target t, contract c, evidence e):

  require exact tuple (q revision, t identity, c profile, evaluation policy)

  a := evaluate_condition(q, c, t, e.condition_witness)
  if a == FALSE_PROVEN:
      return NOT_APPLICABLE + witness + excluded_scope
  if a == UNKNOWN:
      return BLOCKED + APPLICABILITY_UNRESOLVED

  if has_independently_validated_counterexample(q, t, e):
      return FAIL + failing_property + counterexample
      # Only against a sufficiently established invariant and actual target.

  capability := assess_required_capability(q, t, e.capability_probe)
  if capability == UNSUPPORTED_EVIDENCED:
      return UNSUPPORTED + missing_feature + version
  if capability == UNKNOWN and capability_evidence_is_required(q):
      return BLOCKED + CAPABILITY_UNKNOWN

  prerequisites := resolve_required_source_data_oracle_tolerance(q, c, t, e)
  if prerequisites == REQUIRED_UNRESOLVED:
      return BLOCKED + list_of_unresolved_dependencies

  if e.execution == NONE or e.assertion_not_completed:
      return NOT_EXECUTED + precise_nonexecution_reason

  if e.execution_witness_missing or not independently_evaluable(e):
      return BLOCKED + EVIDENCE_INCOMPLETE_OR_UNTRUSTED

  result := verify_property_using_accepted_scope_oracle(q, t, e)
  if result == VIOLATED:
      return FAIL + counterexample
  if result == HOLDS:
      return PASS + scope + evidence_refs
  return BLOCKED + UNKNOWN_RESULT
~~~

The early *counterexample check* is permitted **only** where an independent, applicable, scope-valid invariant is already established; it cannot bypass an unresolved authority that changes the content of the obligation. For example, a proven MW/MWh dimensional inconsistency can fail a scoped dimensional-identity check even if a later KPI discount oracle is TBD. The dependent full KPI claim remains BLOCKED. Report concurrent unresolved dependencies separately instead of losing them to precedence.

R04's useful display order (FAIL > UNSUPPORTED > BLOCKED > NOT_EXECUTED > PASS) applies to **different applicable assertion records** after individual determinations; it is not a license to relabel the primary cause of a single test.

## 3. Event-sourced lifecycle (never overwrite evidence)

A practical lifecycle distinguishes **plan states** from **verdicts**:

~~~text
PLANNED → APPLICABILITY_EVALUATED
                │
                ├─ false + proof ────────────────> NOT_APPLICABLE [closed for this scope]
                ├─ unknown ──────────────────────> BLOCKED [dependency open]
                └─ true → CAPABILITY_EVALUATED
                             ├─ absent → UNSUPPORTED [feature defect]
                             ├─ unknown → BLOCKED [inspection dependency]
                             └─ available → PRECONDITIONS_EVALUATED
                                               ├─ unresolved → BLOCKED
                                               └─ satisfied → ATTEMPT_RECORDED
                                                                  ├─ not completed → NOT_EXECUTED
                                                                  ├─ incomplete proof → BLOCKED
                                                                  ├─ valid counterexample → FAIL
                                                                  └─ established property → PASS

Any observed upstream change → new evaluation revision / new immutable TestAttempt
                              (historical evidence retained, affected claims STALE)
~~~

Re-evaluation may replace the **currently selected** attempt pointer after real resolution, but not mutate/erase earlier verdicts, contradictory evidence, defects or the source of the originally chosen oracle. Resolving BLOCKED requires the missing authoritative dependency; fixing UNSUPPORTED requires proven implemented/exportable capability; fixing FAIL requires correction and rerun; NOT_EXECUTED requires actual execution; N/A→applicable requires changed variant/config and new evaluated scope.

## 4. Special-case rules

### 4.1 P15 optional OPF versus mandatory LF

- **Case P15-OFF:** A versioned configuration sets optional_OPF = false, no P15 invocation exists in the complete run manifest, and the condition is consistent with source/variant profile. P15-specific conditional SR-026 ⇒ **NOT_APPLICABLE**. Mandatory LF SR-024, SR-028, SR-029, SR-035 etc. retain separate mandatory tests.
- **P15-UNKNOWN:** no signed/integrity-checked config, no reliable invocation history, or contradictory status ⇒ **BLOCKED** (not N/A).
- **P15-ON, feature missing:** conditional predicate true, tool cannot represent mandatory OPF candidate cap ⇒ **UNSUPPORTED**.
- **P15-ON, cap violated:** applicable run/valid witness of x_OPF > x_LF ⇒ **FAIL** (if the bound is an established obligation).
- **P15-ON, no model/test run:** feature is available and prerequisites supplied but check was omitted ⇒ **NOT_EXECUTED**.

### 4.2 Missing evidence vs failed technical behaviour

A V1 check on invalid source data may be FAIL as a **data-integrity assertion**, while V3 cannot be meaningfully performed on those same invalid inputs and is BLOCKED due to the upstream defect. An E04 mathematical counterexample is a V3 FAIL even if V4 solve is NOT_EXECUTED. A V4 solver crash is not automatically V3 mathematical FAIL; establish whether it violated a declared solver requirement, is a capability absence, or is simply an incomplete attempt.

### 4.3 Synthetic and productive scopes

For each SR keep a pair of independently identifiable records if needed:

| Scope | Typical research state | Permissible claim |
|---|---|---|
| SYNTHETIC_FIXTURE arithmetic oracle | PASS/FAIL possible only after actual fixture execution and review record | Exact fixture identity or mutation detection |
| NATIVE_TOOL_RUN, PRODUCTIVE_RUN | **48/48 NOT_EXECUTED** at ML-R00/C05 research baseline | None beyond declared plan |
| Original source-data qualification | NOT_QUALIFIED/UNVERIFIED | Cannot be repaired by fixture PASS |
| Official methodology and G1 | AUTHORITY_UNCONFIRMED / G1 BLOCKED | Cannot be set by test-run status |

Do not invent PASS_SYNTHETIC as a seventh test-status label; keep **PASS + scope_class=SYNTHETIC_FIXTURE**, and never aggregate it into a PRODUCTIVE_RUN PASS.

## 5. Correct aggregation preserving causality

For a **specified claim** C, construct its complete required applicable atomic assertion universe U(C), including conditional assertions whose antecedents are true. Exclusions X(C) are exactly assertions with status NOT_APPLICABLE and **proof for a false optional antecedent**. U and X together must account for every potentially relevant assertion; no silent omission.

Report:

- vector of six status counts **and exact IDs**; source/data/authority/reviewer dimensions separately;
- completeness ratio only with **denominator and exclusions shown**; never a compliance percentage from number of planned tests;
- **display headline** = FAIL if any applicable FAIL; else UNSUPPORTED if any; else BLOCKED; else NOT_EXECUTED; else PASS *only for all applicable tests with accepted scope-specific proof*;
- if **U empty** after proven conditional exclusions, headline = NOT_APPLICABLE with EMPTY_APPLICABLE_SCOPE=true, never universal PASS;
- if source authority/qualified data/independent review are required by the higher-level claim but missing, its claim-readiness is **BLOCKED** regardless of a display-level technical PASS;
- a six-valued individual test and a dimension-specific **conformance claim decision** are different record types.

Example 1: 47 applicable checks PASS, one mandatory SR-029 UNSUPPORTED ⇒ headline UNSUPPORTED; full conformance withheld. Example 2: 47 PASS plus P15-OFF proven N/A ⇒ all *applicable* checks pass in a synthetic scoped suite only; methodological/data review remain open. Example 3: 1 executed FAIL and 1 missing source oracle BLOCKED ⇒ display FAIL, vector keeps both causes, never report merely FAIL with no open blocker.

## 6. State-transition controls and audit tests

| Transition attempt | Expected handling |
|---|---|
| NOT_EXECUTED → PASS with no attempt ID | Reject, stay NOT_EXECUTED; record invalid status update |
| BLOCKED → PASS after assigning arbitrary threshold | Reject, stay BLOCKED pending accepted threshold |
| UNSUPPORTED → NOT_APPLICABLE because tool lacks a branch | Reject unless a *legitimate conditional predicate* is demonstrably false for the new scope |
| FAIL → PASS after code change but without rerun | Reject; original FAIL immutable and new test still NOT_EXECUTED |
| P15-OFF N/A → OPF-ON with reused old evidence | New evaluation needed; prior N/A valid only for old run |
| PASS on changed data hash / formula revision | Historical PASS remains, current claim STALE/NOT_EXECUTED pending new check |
| SELF_REVIEW_ONLY → INDEPENDENT_REVIEWED by same author | Reject independence assertion, review status unchanged |
| All tests technically PASS → G1 APPROVED automatically | Reject; G1 controlled externally |

## 7. Unresolved research design questions

Future governance must decide how to prioritise contradictory evidence, classify genuinely unresolvable mixed failures, freeze scope-compatible oracle and numerical tolerance revisions, and attest independent reviewers. The conservative default for a claim without complete necessary proof is **withheld/BLOCKED**, not a new invented sixth-state exception. These are **design issues**, not new owner decisions.

**Sources:** ML-R04 failure_and_evidence_semantics.md, risk_based_conformance_policy.md; ML-R03 data_provenance_and_quality_rules.md; ML-R00 INT-03/10/15. Full scenario suite in verification_status_test_cases.md.
