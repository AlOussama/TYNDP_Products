# ML-R04 — Failure, applicability and evidence semantics v0.1

**Scope:** status definitions for individual tests, requirement scopes and aggregate conformance claims; research proposals, not productive certification.

## 1. Exactly six per-test / per-requirement status values

|Status|Exakte Bedeutung|Mandatory requirement and total claim|
|---|---|---|
|**PASS**|Test was actually executed; preconditions, accepted oracle and tolerance reference fixed; asserted property satisfied; evidence traceable|Only that particular assertion/scoped requirement passed; does **not** grant full conformance|
|**FAIL**|Executed test produces independently checked, applicable counterexample to a required property / certified bound|Global claim prohibited; source of concrete violation recorded|
|**BLOCKED**|A required assertion cannot be evaluated because authoritative source, agreed oracle, data release, rights or tolerances are unresolved|Global claim prohibited; no speculative default oracle|
|**UNSUPPORTED**|Implementation lacks a **required and applicable** capability; manifest or failed capability probe demonstrates absence|Global claim prohibited; a capability absence is not NOT_APPLICABLE|
|**NOT_EXECUTED**|Test was not run, whether by planning, incomplete tooling or unavailable resources not already recorded as missing mandatory capability|Global claim prohibited until execution/evidence; distinguishes intentional omission from FAILED execution|
|**NOT_APPLICABLE**|Formal condition for a conditional requirement is provably false in this run, e.g. OPF variant=false with evidence|Only this *conditional* test excluded from denominator; its unconditional parent tests remain mandatory|

**Clarification:** test PASS on synthetic oracle arithmetic may be recorded **only under class SYNTHETIC_FIXTURE**, never as PASS of tool model conformance. Future tool-run conformance field remains NOT_EXECUTED. No other implicit statuses such as SKIPPED/PENDING/UNKNOWN as substitutes for the six are allowed; operational fields may use separate detailed cause codes.

## 2. Evaluation order (preserve vector, do not silently aggregate away)

1. Resolve requirement obligation and proven antecedent from the versioned contract. For conditional false: NOT_APPLICABLE with condition/branch/absence evidence; if the antecedent is itself unknown, BLOCKED rather than N/A.
2. Check capability: applicable mandatory unsupported ⇒ UNSUPPORTED, including a test not runnable by design.
3. Check method/data/reference-oracle availability; missing released, necessary oracle ⇒ BLOCKED (subject to item 2).
4. Check explicit execution and complete evidence; no attempt ⇒ NOT_EXECUTED. An attempted tool error is FAIL only if it violates required behavior; otherwise record ERROR_CAUSE and BLOCKED/NOT_EXECUTED depending on the independently justified failure mode.
5. Evaluate assertions, negative/mutation controls and numerical criteria against approved evidence ⇒ PASS or FAIL.
6. Every per-layer conformance view retains all constituent statuses and root causes, especially when the summary carries the most severe state.

For **display-only aggregate summary**, deterministic precedence is FAIL > UNSUPPORTED > BLOCKED > NOT_EXECUTED > PASS, after separately excluding justified NOT_APPLICABLE. This is **not** a scientific equivalence between these causes: show the status vector and affected IDs. If every applicable test PASS **and** owner/authority evidence valid, a scoped PASS may be considered by qualified reviewer; not automatically by software. If none applicable, do **not** assign universal PASS: summary NOT_APPLICABLE with explicit empty-scope flag.

## 3. Orthogonal conformance dimensions

Maintain six independently reasoned dimensions:
- **Data validity:** native source release, physical files, schema, keys and UTC/units.
- **Semantic conformance:** intended physical/economic meaning and transformation preservation.
- **Mathematical conformance:** generated problem and required invariants under an explicit projection.
- **Numerical conformance:** solution feasibility and accepted optimality evidence on instance.
- **Result conformance:** raw outputs and independently reproduced KPIs.
- **Evidence quality:** coverage, authenticity, reproducibility, completeness, independence and provenance.

A requirement may be V1=PASS_SYNTHETIC, V3=NOT_EXECUTED, V4=NOT_EXECUTED, source_authority=BLOCKED; **never** flatten this into a general PASS. In machine-readable test files, stick to the six core status labels and put synthetic scope in an orthogonal class field. Review quality can be a scored dimension but an unattributed favorable score never substitutes for independent human signoff.

## 4. Required record and provenance

~~~json
{
  "test_id": "R04-T-SR-029",
  "requirement_id": "MA01-SR-029",
  "scope": "SYNTHETIC_FIXTURE | PRODUCTIVE_RUN",
  "applicable": true,
  "condition_evidence_ref": "run-config-hash-or-null",
  "status": "NOT_EXECUTED",
  "cause_code": "NO_TOOL_RUN",
  "assertion_revision": "draft-v0.1",
  "methodology_ref": "BUNDLE01R-O26-DRAFT-AUTHORITY-UNCONFIRMED",
  "oracle_ref": null,
  "oracle_approval": "NOT_OBTAINED",
  "tolerance_profile_ref": null,
  "attempted_at_utc": null,
  "raw_evidence_sha256": null,
  "tool_version": null,
  "independent_reviewer": null
}
~~~

The example fields are placeholders and should never be interpreted as acquired hashes, signoffs or executions. Real evidence must be immutable with SHA-256, timestamp UTC, provenance, tool/model/solver identifiers and a reproducible assertion algorithm.

## 5. Illustrative status transitions and anti-patterns

|Situation|Permitted outcome|Explicitly prohibited|
|---|---|---|
|C09: tool cannot couple investment across CY, obligation mandatory|UNSUPPORTED|PASS, NOT_APPLICABLE, silently dropped|
|C10: OPF disabled with reliable configuration/absence of OPF run|NOT_APPLICABLE (SR-026 only)|Unconditional LF tests N/A|
|C10: OPF enabled; y=4 > LF cap 3 and model ran|FAIL|Reclassify as optional hence PASS|
|C05: incorrect cut 40 vs injection 50|FAIL on synthetic conservation check|Declare electrical network equivalent based on just one equality|
|No accepted network RMSE threshold, no counterexample known|BLOCKED for approved numerical cutoff|Auto-PASS or fabricated threshold|
|Solver reports OPTIMAL but no exportable solution/metadata to recompute|BLOCKED evidence or NOT_EXECUTED check, cause-specific|Trust solver status as proof|
|Two valid but different optimal portfolios (C07)|Potential PASS on objective/constraints/invariants|FAIL solely due to differing investment vectors|
|Only synthetic self-check has been run|SYNTHETIC_FIXTURE local result; tool-run NOT_EXECUTED|Global model or G1 PASS|

## 6. Open case management

Defects link to exact SR, test, layer, proof artifact, reproducibility steps, severity, affected method/target years, owner for resolution, evidence to close and new test run. A missing owner decision is an **open decision dependency**, not automatically evidence that the implementation is mathematically wrong. Only approved owner closure plus genuinely rerun assertions can change blocked states.

G1 and normative approval remain independent gated records; BUNDLE-01R still BLOCKED, findings do not disappear when a synthetic test passes.

**External reasoning:** NIST notes that a passing suite cannot establish universal conformance outside tested behavior, and certification requires agreed criteria/process: https://www.nist.gov/itl/ai/applied-ai-research-group/conformance-testing
