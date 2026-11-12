# ML-C01 — Source Authority & Applicability Semantics

**Research draft 0.1 · 2026-11-12 · ML-R00 #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2.** No newly adopted methodology, owner decision, data approval or normative contract. **G1=BLOCKED**.

## 1. Principle: truth of a citation ≠ authority of a rule

Keep three distinct assertions per source: (1) *provenance* — which document revision and clause was inspected or cited; (2) *source-content truth* — what that version explicitly says; (3) *normative applicability* — whether a qualified authority adopted that wording for this particular IoSN target/version/run. The first two do **not** prove the third. A source may be authentic as a public consultation document while its normative authority remains unverified.

| Canonical source kind | Concrete research baseline | Applicable research use | Explicitly prohibited promotion |
|---|---|---|---|
| **O26_DRAFT** | ENTSO-E *TYNDP 2026 Identification of System Needs Methodology*, **Version for Public Consultation, 25.02.2026**, §§2–5/Annexes | Primary documented 2026 methodological research reference; cite exact clause and revision | **No** claim of adopted/effective IoSN method; no original IoSN-run dataset or signed approval inferred |
| **H24_CONTEXT** | ENTSO-E *TYNDP 2024 Identification of System Needs Study Methodology*, *Version for Opinion*, **09.04.2025**, §7.3.1/7.3.2 | Explicit historical fill-in/control *only where O26 is silent and consistent*, with the historical scope retained | Not the 2026 governing text or owner-approved default; never override O26 |
| **CBA4_REFERENCED_EXTERNAL** | Final European Commission-approved fourth CBA Guideline (2024), §2.5.1, referenced by O26 §3.4 | Reference within *its own approved CBA domain* for identified 2035 project-eligibility interpretation, subject to later IoSN applicability decision | CBA4 approval ≠ O26 adoption, automatic starting-grid eligibility or acceptance of an unverified project list |
| **PROJECT_DECISION** | Confirmed D1–D6 in the project record | Governs ML-C01 **non-normative research profile** and related scoping | Cannot alter O26 document text, decide MD/CL or grant ENTSO-E normative approval |
| **SCI_DERIVED** | Traceable physical/mathematical implication of a source/decision with explicit assumptions | Potential research invariant and falsifiable micro-oracle | Not a released numeric value or universal equation requirement |
| **ILLUSTRATIVE** | Synthetic fixture constants, examples, proposed schema/prototype/algorithms | Explicitly sandboxed scientific examples only | Not run defaults, authoritative data, threshold, official test oracle or source norm |
| **TBD_OWNER** | Unresolved methodology owner choice MD-01…MD-20, MA02-CL-001 | Preserved dependency with scope, owner and required later evidence | Not assumed true, false, approved or cured by an AI interpretation |
| **FUTURE_ADOPTED** | No positively verified record in this research snapshot | Reserved separate future source-authority assertion after genuine release verification | Must not be populated from an expected future publication or absence of search results |

**Known authority facts:** The R01/ML-R00 research has positively identified O26 as a consultation, and specifically **has not verified an adopted later IoSN release**. Historical H24 and CBA4 are source facts in narrower contexts. The underlying source PDFs, their release hashes and any signed effective-version record are not themselves qualified in ML-C01; no negative search is proof no successor exists.

## 2. Version-specific precedence is not a silent merging algorithm

1. At future normative acceptance, a genuinely adopted applicable method takes precedence **for that defined scope**, after its original version/issuer/effective date/clauses are verified.
2. Until then, O26 is the **primary research source** rather than a falsely approved norm.
3. If O26 lacks a needed detail, clearly mark historical H24 context, exact prior clause and the explicit **authority gap**. An older document supplements interpretation but not operative approval.
4. D1–D6 control the **project research configuration**. When a project choice conflicts with O26 content, keep both statements and a named versioned conflict; do not issue an implicit “project supersedes ENTSO-E” claim.
5. SCI_DERIVED propositions require declared premises and domain constraints. A premise change invalidates or limits a derived claim rather than silently updating its proof.
6. ILLUSTRATIVE data and unclosed TBD_OWNER have no authority to fill blank productive parameters.

**Example:** O26 §3.7 has **three** weather cases per year; D2 research profile has **five** externally selected CY. Required state is O26_3_CASES_VS_D2_5_CASES = OPEN_SOURCE_PROFILE_RECONCILIATION, not “O26 has five cases” and not “D2 cancelled”. Source case names/profile dates are kept source-specific and do not magically map to CY1–CY5.

## 3. Applicable assertions and profile scopes

Every MethodologyAssertion/SourceClauseLink should retain a structured tuple (logical contract only):

~~~text
assertion_id; exact_source_document_id; revision; clause_span;
source_kind; content_statement; effective_scope; authority_claim_state;
project_profile_id; project_decision_overlay; conflict_id;
derivation_class; assumptions; applicability_guard; blocking_MD_CL_ids;
original_file_hash_state; owner_record_ref; evidence_ref
~~~

**Applicable scope is multi-key:** target year; scenario/pathway/variant; weather identity; source release; region/zone/network revision; carrier; process stage; model mode (LF, internal dispatch, H2 sensitivity, OPF); time interval; output category; requirement revision. Applicability cannot be inferred just from a bare year or an arbitrary tool configuration string.

**Source-gate decision matrix:**

| Statement/evidence condition | Research disposition | Productive authorization |
|---|---|---|
| O26 clause present, exact revision known, adoption not verified | SOURCE_CONTENT_DOCUMENTED + AUTHORITY_UNCONFIRMED | BLOCKED |
| H24 clause clarifies O26 technical context but no 2026 owner adoption | HISTORICAL_CONTEXT_WITH_LIMITED_SCOPE | BLOCKED |
| D1–D6 signed/project confirmed as previously recorded | PROJECT_RESEARCH_PROFILE_CONFIRMED | **not** ENTSO-E adoption |
| R02/R03 synthetic example schema-valid | PASS_STRUCTURAL_SYNTHETIC (scoped event) | none |
| A method parameter or KPI formula remains TBD | SCIENTIFIC_SPEC_PARTIAL + ORACLE_TBD | BLOCKED for relevant required claim |
| Genuine future method approval and owner reconciliation (not present now) | New release/version assertion, future controlled review | Requires **separate** signed claim, not inferred here |

## 4. Conditions and optionality

Use three-valued applicability truth **TRUE / FALSE / UNKNOWN** plus a separate obligation kind REQUIRED / CONDITIONAL / OPTIONAL. Treat UNKNOWN as **BLOCKED** on the scoped test/claim; it cannot be coerced into FALSE to obtain N/A. A conditional rule, when TRUE, is mandatory; when FALSE with evidence it is NOT_APPLICABLE for that exact test. For optional P15, the **selection of OPF** is optional, but if the run declares OPF_SELECTED=TRUE then SR-026's method-specific constraints (LF cap, separation and candidate accounting) are mandatory. A false/absent OPF flag needs credible signed configuration/absence evidence; absent proof means UNKNOWN.

**Cross-scope non-interference:** P15=N/A never implies SR-024 LF expansion, SR-025 internal constrained dispatch, SR-027 objective or SR-029 shared investments are N/A. An approved project-list element at P04 similarly cannot inherit a SystemNeed category at P16; separate record types and sources control them.

## 5. Provenance and change impact

A source link is a reference, not a hash. Hash status for source PDF/real data can be VERIFIED_FROM_ORIGINAL_BYTES, NOT_VERIFIED or SYNTHETIC; **never generate a plausible checksum for a file not inspected**. Store original version, not only current revision pointers. A source update requires new identity, clause-level delta, impact links for all 48 MA01-SR, M01–M18, data objects, transforms, VN tests, outputs/claims, and explicit owner resolutions; previous research snapshot must remain immutable.

**Change control trigger examples:** future adopted IoSN method; official five-CY mapping and weights; official starting-grid eligibility; LF/OPF formulas; native verified reduction oracle; KPI formula; time calendar policy. Any such update is a new profile version + impact report, not an edit of the underlying original workstreams or a retrospective PASS.

## 6. Open authority/owner dependencies

- **MD-01**: adopted source/effective revision; **MD-20**: scope/requirements governance.
- **MD-18/19 and MD-12**: case mappings, externally supplied numerical weights/profile chronology and time/unit conventions.
- **MD-14 + MA02-CL-001**: 2035 starting-grid project eligibility from O26 versus CBA4/historical H24.
- **MD-02/03/04/05/06/07/08/09/10/11/13/15/16/17**: scientific formulas, model parameters, original-data provenance, numerical and result oracles.

All 21 established MD/CL remain OPEN_NOT_OWNER_APPROVED; their ultimate resolution is explicitly deferred. ML-C01 records no new source authority. **G1 remains BLOCKED.**

## 7. Anchors

[R01 scientific source and provenance comparison](../ML_R01_methodology/scientific_methodology_specification.md); [ML-R00 synthesis](../ML_R00_consolidation/consolidated_research_synthesis.md); [R03 semantic data model](../ML_R03_data_process_contracts/iosn_data_semantic_model.md); [R00 consistency findings INT-07/13](../ML_R00_consolidation/cross_workstream_consistency_review.md); [MA01 catalogue](../../iosn_requirements_catalogue.csv).
