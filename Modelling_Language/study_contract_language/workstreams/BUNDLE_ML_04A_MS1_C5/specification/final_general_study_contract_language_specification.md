# General Study Contract Language – C5 research candidate 0.1
NON-NORMATIVE / RESEARCH ONLY; OWNER_TBD. Not v1.0.
## 1 Scope and inheritance
C4 normative-for-this-research-candidate syntax, type and domain semantics are inherited exactly from the pinned C4 specification (commit 6920aade2f6b7517a49e8c9c3a21843c9e71fd9b, sibling BUNDLE_ML_04A_MS1_C4). All existing contract collections, quantity typing, chronology, information, data and method composition remain under C4. No replacement mathematics or CBA-specific primitives.
## 2 Architecture
M3-Hybrid; pinned mathspec public Program is sole mathematical authority. C5 is a generic research composition profile above C4 Definition/Instance. It does not modify frozen historical branches or C4 wire schemas.
## 3 Abstract syntax
D5=(schema,base,requirements,metrics,tests). I5=(schema,definition_ref,base,requested_tests,run_id,claims). P5=(schema,definition,instance,receipt); here P5 denotes C5 package, not the historical CBA P5 corpus. Exact fields and roles in final_schema.json and final_metamodel.json.
## 4 Semantics
Requirement records version level, source, authority, scope, required flag, parents, targets and metrics. STUDY roots; SYSTEM descendants in the same exact scope. Explicit acyclic trace and mandatory target coverage, not decomposition entailment.
Metrics classify STUDY, VERIFICATION, VALIDATION and reference C4 typed targets. Criteria are native assertions, comparisons, or external reports; no duplicated math. Tests specify objective, requirements, metric, criterion, scope, oracle source, method, coverage and evidence role. Test inputs, assumptions and guards are inherited from bound C4 targets and instances. See workstream documents.
## 5 Execution and evidence
admit checks exact pin and static semantics. instantiate calls actual C4 native instantiation and derives bounded receipts. Computed evidence binds versions, roots, methods, actual data and diagnostics. Declared claims are unverified and cannot supply missing execution. Conflicting claims prevent automatic positive satisfaction. Assessment states and aggregation in verification/assessment_state_semantics.md. No overall conformance claim.
## 6 Canonical representation
Use C3 A/B structural authoring envelope and existing native canonical package. Semantic D identity includes C4 semantic identity and sorted registries and set-valued references. Exact source, D and I roots are separate from semantic identity. Export canonical JSON and reimport by recomputation and exact match. A/B byte differences remain audit differences. No mathematical AST or second normal form.
## 7 Method exchange and version migration
compose_method uses C4 approved composition and preserves outer test/requirement records. New roots invalidate old evidence; re-admit and re-execute. C4-to-C5 is explicit authoring of requirement/metric/test records around preserved C4 payload, not automatic inference of stakeholder requirements. Old C4 packages remain valid at original wire schema.
## 8 Authoring and limitations
The same C3 grammar represents nested C5 records. Candidate schema is structural only; run semantic validation. No solver integration, authenticated external reviews, universal equivalence or validation completeness. Equal-scope refinement and limited finite coverage; proof that the declared support matches the intended study remains external. Missing empirical and scientific evidence recorded separately. C5 release status governed by gate_status.json.
