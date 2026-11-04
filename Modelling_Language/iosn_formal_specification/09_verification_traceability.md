# 09 — Traceability, evidence and system acceptance architecture

## Canonical graph
~~~mermaid
flowchart LR
  O[Method statement O26] --> MR[MR stakeholder obligation]
  MR --> SR[SR system requirement]
  SR --> FS[FS formal semantic element]
  FS --> AD[Implementation adapter]
  AD --> VC[Verification case / oracle]
  VC --> EV[Execution evidence]
  EV --> AR[Acceptance report]
~~~
All edges must be typed: `derives_from`, `formalizes`, `implemented_by`, `verified_by`, `evidenced_by`, `supersedes`. Their endpoints must reference immutable versions/hashes; links must be validated for referential integrity and no dangling normative obligation.

## Explicit trace examples
|Statement [O26]|Requirement|Formal element|Tool side|Verification|Evidence/status|
|---|---|---|---|---|---|
|§3.7 published weather tuples|MR-002 → SR-004|poc/contract.json years[2035] and schemas|rows_v1/map_v1 *mock adapters*|VC-01–VC-04|poc/verification_report.json, **executed on fixtures only**|
|Annex 6.3 weather selection method|SR-005|UC-01 selection algorithm profile OPEN|unimplemented|VC-13 selection reproduction|EV-13 **NOT EXECUTED**|
|§3.1.1 common investment across weather|MR-003 → SR-015|UC-02 indexed x(i,year) invariant|PyPSA / GEMS adapter **design**|VC-07|EV-07 **NOT EXECUTED**|
|§3.1.1 LP and objective|SR-016|UC-02 mathematical profile|unimplemented model oracle|VC-09|EV-09 **NOT EXECUTED**|
|§3.8 network reduction|SR-007/008|busmap/equivalent network profile OPEN|unimplemented|VC-10|EV-10 **NOT EXECUTED**|
|§3.9 LF and internal constraints|SR-017|processing state profile|unimplemented|VC-14|EV-14 **NOT EXECUTED**|
|§§2.2,3.1.2 output|SR-018/019|UC-03 output profile X|unimplemented|VC-11/12|EV-11/12 **NOT EXECUTED**|

## Three distinct conformance classes
1. **Structural conformance:** schema, required fields, JSON/LinkML/SHACL shapes, reference and unit metadata. Independent testable, insufficient to prove physics/method validity.
2. **Semantic/methodology conformance:** scenario weights, method version, transformation invariants, correct reference KPI and mathematical obligations. Requires domain-specific interpreters and sometimes independent model/algorithm oracles.
3. **Implementation/system conformance:** tool configuration, generated model, runtime result, solver state and test-suite evidence, plus human review for ambiguous/physical criteria. Cannot be inferred from a correctly formatted file.

## Verification methods and confidence
|Type|Automatable|What is established|What is not established|
|---|---|---|---|
|Static schema|Yes|Types, presence, range|Correct solver behavior or physics|
|Referential/unit consistency|Usually with semantics|Dimensional, source/target coherence|Adequacy of modelling assumptions|
|Known-answer reference fixture|Yes with an approved oracle|One discrete method/example|Global correctness|
|Constraint residual / objective recomputation|Partially; needs solver evidence|Feasibility for a returned candidate solution|Proof of model generator completeness unless algebra inspected|
|LP structure and non-anticipativity inspection|Partially; model introspection needed|Presence of required variable equivalences|Correctness of every hidden constraint in uninspectable solver|
|Physical network reduction quality|Mixed automated + expert|Bounded residual on agreed cases|Unspecified general equivalence|
|Independent technical acceptance|Human sign-off required|Authorized release for defined scope|Automatically guaranteed fitness beyond tested scope|

## Test catalogue / inputs and conditions
|VC|Requirement|Precondition & stimulus|Expected oracle / pass criteria|Status|
|---|---|---|---|---|
|VC-01|SR-004|well-formed and malformed weather export|valid shape accepted; invalid rejected per input/canonical JSON schemas|PoC executed|
|VC-02|SR-004|correct and wrong/duplicate weather IDs|exact selected IDs, no duplicate|PoC executed|
|VC-03|SR-004|correct and perturbed weather weights|exact published weights and sum near 1 using **X tolerance 1e-12**|PoC executed|
|VC-04|SR-001,004|wrong year/source/missing provenance|year recognized, source reference correct, nonempty source lineage|PoC executed|
|VC-05|SR-010|cross-carrier unit and port fixture|units and carriers match signed definitions|NOT EXECUTED|
|VC-06|SR-010|known H2 conversion/balance data|feasible case within approved residual tolerance, wrong sign fails|NOT EXECUTED|
|VC-07|SR-015|two-weather investment fixture|one common x; duplicated scenario-specific x fails|NOT EXECUTED|
|VC-08|SR-011–014|candidate stages and storage period fixture|eligible candidate classes only, no prohibited H2 grid expansion|NOT EXECUTED|
|VC-09|SR-016|small LP expected objective and constraints|reference LP and independent extracted engine results align within signed tolerance|NOT EXECUTED|
|VC-10|SR-007/008|small-grid zoning and reduction fixture|approved mass/electrical equivalence checks pass|NOT EXECUTED|
|VC-11|SR-018/019|needs output fixture|typed fields, identities and provenance complete|NOT EXECUTED|
|VC-12|SR-019|raw and aggregated outputs|signed KPI recomputation equals report values|NOT EXECUTED|
|VC-13|SR-005|climate feature dataset + approved random seed|independent Annex 6.3 selection returns agreed results|NOT EXECUTED|
|VC-14|SR-017|LF portfolio + supplementary OPF artifact|LF baseline preserved; optional outputs never replace it|NOT EXECUTED|

## Version and impact rules
- `source_document_id`, `source_version`, `section`, `requirement_id`, `profile_id`, `schema_version`, `test_version`, `adapter_version`, `run_id` and `artifact_digest` are separately tracked.
- A source change invalidates linked derived requirements and every dependent downstream test/evidence until impact analysis is accepted. Old results remain immutable with historical label, never rewritten as conformant to a new source.
- Contradictory obligations or unspecified normative behavior → `UNRESOLVED` (blocks certified conformance). Executed negative tests are recorded as successful *rejections*, not successful implementations.
- A tool may publish `UNSUPPORTED` and fail closed for an obligation. Silently dropping it is non-conformant.
- Approval report template: source version/status, contractual profile hashes, obligations/test coverage, pass/fail/blocked counts, responsible method authority, independent reviewer, waivers (if any), formal scope, signature/release date.

## Distinction between design and execution
`poc/verification_report.json` records executed fixture checks only, not generated from an actual energy model. VC-05–VC-14 require their own independently run suites. A test definition is not a test generator, a generated test is not an executed test, and an executed test does not by itself prove untested model behavior.

## Extended verification cases from additional O26 obligations

|VC|Source + SR|Input/stimulus|Expected oracle and status|
|---|---|---|---|
|VC-15|O26 §3.4 / SR-022,029|2025 baseline + qualifying project set|2035 reference grid inclusion/exclusion backed by qualifying evidence and identities; **NOT EXECUTED**|
|VC-16|O26 §3.5 / SR-023|national offshore RES targets and hybrid reference projects|fixed-target consistency and source vintage; **NOT EXECUTED**|
|VC-17|O26 §3.9 / SR-031|candidate OPF variant after LF expansion|OPF candidate expansion capped by LF portfolio, run modes different; **NOT EXECUTED**|
|VC-18|O26 §3.11 / SR-024|theoretical offshore candidate source length and routing coefficient|uniform increase factor within 10–15%, exact factor governed by signed method decision; **NOT EXECUTED**|
|VC-19|O26 §§4.1,4.3–4.4 / SR-025,026,033,034|hydro five-type and DFT/DSR synthetic series|resource class, chronology, units and market participation semantics preserved; **NOT EXECUTED**|
|VC-20|O26 §4.5.2 / SR-027,029,035|investment candidate with directional NTC and AC physical label|controllable DC *market-link* model abstraction, no accidental electrical-mesh reinterpretation; post-filter documented; **NOT EXECUTED**|
|VC-21|O26 §§4.5.3,4.6 / SR-028,030|standard offshore candidate and cost vintage|VSC reference, investment lifetime and unit-consistent economic rules checked against approved costs; **NOT EXECUTED**|

## New traceability dependency
`O26-4.5.2 → MR-011 → SR-027 → LRC-20 → UC-02.NTC_candidate → real_adapter_generated_model → VC-20 → EV-20`. The two occurrences of the word `DC` (DC power flow in source §3.1.1 vs controllable DC market link for all transmission investment candidates in §4.5.2) are **different semantics** and must not be merged.
