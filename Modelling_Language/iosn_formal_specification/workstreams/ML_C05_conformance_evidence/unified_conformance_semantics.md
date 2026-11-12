# ML-C05 — Unified Conformance Semantics

**Research release:** ML-C05 v0.1, 2026-11-12. **Status:** NONNORMATIVE_RESEARCH_PROPOSAL. **Baseline:** ML-R00 PR #32, commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2. **Governance:** AUTHORITY_UNCONFIRMED; NOT_DATA_QUALIFIED; NO_TOOL_CONFORMANCE_ASSESSED; G1 = BLOCKED.

## 1. Purpose, scope and binding distinctions

The IoSN Requirements Contract is a versioned, tool-independent *set of scientific obligations*, not an assertion that a particular implementation, source release, dataset or result has been approved. Verification observes a **specific assertion**, against a specified scope, using identified evidence and an identified oracle. Conformance is a bounded claim derived from many such observations and independent review, never a global boolean obtained from a parser, solver or synthetic benchmark.

This note reconciles ML-R02 (architecture and draft progression), ML-R03 (data/source qualification) and ML-R04 (V1–V6, six test statuses). The ML-R00 integration findings INT-01/02/03/10/12/15 are explicitly retained. The original R01–R04 artifacts and the 48 provisional MA01-SR are not rewritten.

**Eight orthogonal dimensions** are required for any conformance dossier:

| Dimension / proposed namespace | Question and permissible statement | Evidence anchor | Explicit non-implication |
|---|---|---|---|
| **A — Source/method authority** | Which exact methodology release/clauses and project decisions are in force, and who authorised them? | E01, signed authoritative release when available | An accessible O26 draft is not adopted methodology |
| **Q — Input data qualification** | Are the actually consumed source bytes, releases, calendar, units and data transformations qualified? | E02/E03, independent data audit | Schema validity or a file hash is not data approval |
| **S — Semantic fulfilment** | Does the tool represent the required physical, process, optionality and economic meanings? | E01/E03/E04, V2 | Matching names or row counts do not prove semantic coverage |
| **M — Mathematical model conformance** | Does the generated mathematical programme satisfy applicable obligations, including feasible-space meaning? | E04, V3, D2–D4 | Same optimum on one fixture is not equal formulation |
| **N — Numerical solver conformance** | For an identified generated instance, are feasibility and the claimed optimality supported? | E05, V4 | Solver text OPTIMAL alone is not an independently verified certificate |
| **R — Raw result and KPI conformance** | Can output lineage and each approved, in-scope KPI be independently reconstructed? | E06/E07, V5 | Same KPI in two tools may reflect the same error |
| **E — Evidence quality / independence** | Are evidence objects complete, immutable, authentic, reproducible and reviewed with real independence? | E08 and references to E01–E07, V6 | A self-review does not constitute independent assurance |
| **G — Governance / gate decision** | Has a duly authorised human governance process approved a specified release or gate? | External decision record linked through E01/E08 | No test-suite, evidence collector or tool may auto-approve G1 |

Technical shape validation is an **observation within Q/S/E**, not a ninth source of authoritative approval. D0 technical passes may coexist with A=AUTHORITY_UNCONFIRMED, Q=NOT_DATA_QUALIFIED and G=BLOCKED. Every dimension carries its *own* status family, scope and unresolved dependencies; never force all eight into the six test outcomes.

## 2. Minimal evaluation identity

An atomic test-result identity is a logical tuple:

- **contract snapshot** = exact SR/MA01-VN/L4 reference set, methodological source version, applicable D1–D6 research decisions and profile digests;
- **obligation** = requirement ID, asserted property ID and revision, relevant P00–P17 process, variant and conditional antecedent;
- **target** = tool-independent model/run/instance or synthetic fixture, study year, CY set, date/time and carrier/space axes as applicable;
- **verification configuration** = V-level, D-depth, oracle revision and authority, accepted tolerance profile or explicit TBD, test implementation revision;
- **attempt** = distinct execution ID, timestamp, evidence content identities, capability evidence, disposition, review references and causal defects.

The same SR may have several independent assertion IDs, test attempts, tools, study years or conditional branches. An assertion's PASS cannot satisfy a different assertion by changing the join key; a new contract revision or changed input invalidates previous scope and requires impact analysis/re-execution.

### Namespaces are not interchangeable

| Namespace | Example | Interpretation |
|---|---|---|
| project decision | D2 | Five externally selected CY1–CY5; same potentially **nonuniform** weight vector across 2035, 2040, 2050 |
| project decision | D4 | Canonical UTC/time interval and unit semantics; detailed MD-12 still TBD |
| verification depth | depth:D4 | Triggered deep mathematical equivalence or projection proof, **not** project decision D4 |
| project decision | D3 | Fail-closed requirement/evidence treatment |
| project decision | D5-A1 | Risk-based verification: not identical algebra for every tool |
| project decision | D6-A | Same semantic contract, independently built tool models, not model-to-model conversion |
| technical verification layer | V1–V6 | Data, semantics, math, solver, KPI and continuous evidence respectively |
| evidence surface | E01–E08 | Logical information supplied for inspection, not a mandated wire format |

**Weather correction (INT-01/02):** w(2035,c) = w(2040,c) = w(2050,c) = w(c) for corresponding CY labels. There is **no** assumed equality between w(CY1) … w(CY5), nor a real default of 0.2. Even a normalised symbolic probability vector is subject to the source profile and final acceptance rules. The historic three-versus-five MA01-SR-010/source difference is a versioned *research overlay conflict*, not silently approved amendment.

## 3. Three non-interchangeable status domains

### 3.1 Assertion outcome: exactly six values

**PASS**, **FAIL**, **BLOCKED**, **UNSUPPORTED**, **NOT_EXECUTED**, **NOT_APPLICABLE** are exclusively per-test or per-scoped-requirement dispositions. Definitions and priority rules are specified in applicability_and_failure_state_machine.md. Store cause codes, applicability and test-scope flags separately; do not coin a seventh substitute such as SKIPPED or PASS_SYNTHETIC. A research synthetic test may have status PASS *only for its fixture-level assertion*, plus scope = SYNTHETIC_FIXTURE; its productive tool-run assertion remains NOT_EXECUTED.

### 3.2 Independent lifecycle/status families (illustrative, not owner-adopted)

| Subject | Illustrative statuses / values | Ownership boundary |
|---|---|---|
| Methodology/source | AUTHORITY_UNCONFIRMED; SOURCE_IDENTIFIED_DRAFT; AUTHORITY_CONFIRMED | Methodology Owner |
| Source data | NOT_QUALIFIED; SOURCE_UNVERIFIED; QUALIFIED_FOR_SCOPE | Data Owner; original bytes needed |
| Contract structure | DECLARED; STRUCTURE_CHECKED; SEMANTICS_REVIEWED | Technical evaluator; never SOURCE_APPROVED by implication |
| Model evidence | NOT_ASSESSED; EVIDENCE_INCOMPLETE; SCOPED_PROPERTY_EVALUATED | Verification procedure, claim-scoped |
| KPI definition | FORMULA_TBD; FORMULA_VERSIONED; ORACLE_APPROVED | KPI/Reporting Owner |
| Review independence | NOT_OBTAINED; SELF_REVIEW_ONLY; INDEPENDENT_REVIEWED_FOR_SCOPE | Qualified reviewer |
| Gate | BLOCKED; EXPLICIT_OWNER_DECISION_RECORDED | Gate/Project Owner only |

These labels are **proposed descriptors**, not unobserved approvals. R02's DECLARED → SCHEMA_CHECKED → … → APPROVED is recast as a **candidate evidence-readiness sequence**, not an automatic status machine; its final APPROVED cannot be inferred from completed parser stages. R03's T0–T5 are different assurance *subjects*, not a single progression that repairs missing original data. R04's six statuses are per-assertion outcomes.

### 3.3 Additional orthogonal fields

- **scope_class:** SYNTHETIC_FIXTURE | RESEARCH_PROFILE | PRODUCTIVE_RUN | REVIEW_ONLY.
- **applicability:** TRUE | FALSE_PROVEN | UNKNOWN; false requires a witness.
- **capability:** SUPPORTED_AND_INSPECTABLE | UNSUPPORTED_EVIDENCED | UNKNOWN; support is scoped to function and version.
- **oracle_state:** AUTHORIZED_FOR_SCOPE | RESEARCH_ONLY | UNRESOLVED_TBD | INVALID.
- **evidence_quality:** traced completeness, integrity, authenticity, reproducibility, independence, and reviewer identity *independently*; quality is not a single magic score.
- **decision_provenance:** owner identity, version, effectivity, scope, effective date and explicit decision reference, null until obtained.
- **staleness:** CURRENT | STALE_UNTIL_RECOMPUTED, based on dependencies and source/input/model/oracle revisions.

Do not encode these subjects in a single 'PASS' result field or misread a JSON/CSV validation result as scientific acceptance.

## 4. Applicability and per-layer assurance rules

1. Establish the versioned requirement and its **mandatory or conditional** predicate before test classification.
2. For proven inactive optional P15 (OPF disabled, configuration and no invocation attested), only P15-specific SR-026 assertions are NOT_APPLICABLE. The LF baseline SR-024 and other unconditional obligations remain applicable.
3. For an applicable mandatory feature missing from the tool, outcome UNSUPPORTED; absence cannot be hidden under NOT_APPLICABLE or omitted from scope.
4. A missing authoritative input, owner formula, necessary tolerance or accepted oracle means a corresponding acceptance assertion is BLOCKED rather than a manufactured PASS.
5. An unexecuted test with prerequisites ready is NOT_EXECUTED. A verified counterexample under sufficient, applicable evidence is FAIL.
6. A PASS is local to the exact assertion, scope, reference data, oracle and accepted tolerances actually evaluated. Earlier failures do not vanish when rerun; retain immutable attempt history and an explicitly selected current attempt.
7. The overall profile is **not** a single test; dimension-specific claims must retain all constituent tests and dependency states. A display priority may be calculated but cannot replace the vector.

Example: V1 structure = PASS on a synthetic manifest; V3 = NOT_EXECUTED; input qualification = NOT_QUALIFIED; authority = AUTHORITY_UNCONFIRMED; review = NOT_OBTAINED; G1 = BLOCKED. No conformance claim beyond the narrow executed V1 structural fixture assertion follows.

## 5. Conformance boundaries and failure of false equivalences

The following implications are **invalid**:

- E02 schema PASS ⇒ qualified original source data.
- E04 coefficient list present ⇒ intended mathematical constraints correct.
- V4 primal feasible on one instance ⇒ correct V3 semantics.
- Equal solution objective ⇒ equal feasible set, equal optimal set or identical full model.
- Two different optimal portfolios ⇒ at least one model FAIL (false with degeneracy/multiple optima).
- Matching KPI ⇒ correct KPI formula or correct physical constraints.
- Many local PASS results ⇒ scientific certification, source authority or G1 GO.
- An existing unchanged output ID ⇒ evidence current after a changed input hash (stale).

Use scoped claims defined in conformance_claim_rules.md. They may state verified properties, numerical outcomes and conditional equivalence under precise assumptions; they cannot assert official methodology adoption or tool certification without external approval.

## 6. Current ML-C05 research disposition

The inherited matrix contains **48 unique provisional SR IDs**, **48 test IDs**, **33 proposed A / 12 B / 3 C** risk tiers. All **48 productive tool-run statuses remain NOT_EXECUTED**; original IoSN inputs are not qualified; owner oracles/tolerances remain TBD. No independent qualified human assurance or native two-tool pilot has been carried out. The present deliverable harmonises evidence semantics only.

**Decision:** G1 = BLOCKED, unchanged. Owner authority, data qualification and technical conformity must be reported on separate axes and cannot be released by this research note.

## 7. Source crosswalk

- ML-R00 cross_workstream_consistency_review.md (INT-01, INT-02, INT-03, INT-10, INT-12, INT-15).
- ML-R02 contract_architecture_alternatives.md (A/B/C and technical progression).
- ML-R03 data_provenance_and_quality_rules.md (T0–T5, DQ-001–020).
- ML-R04 verification_architecture.md, failure_and_evidence_semantics.md, tool_conformance_evidence_specification.md, requirements_verification_matrix.csv.
