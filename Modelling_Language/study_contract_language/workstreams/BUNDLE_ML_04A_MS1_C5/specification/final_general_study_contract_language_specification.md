# General Study Contract Language — consolidated C5-R1 research candidate 0.2

**NON-NORMATIVE / RESEARCH ONLY; OWNER_TBD. Not a v1.0 release.**

## 1. Purpose and scope
Study contracts describe what must be specified and observed independently of model formulation. The research profile admits finite named support only. No CBA-specific primitive.

## 2. Conformance and governance
Overall contract conformance remains NOT_PROVED. OWNER_TBD; NON-NORMATIVE / RESEARCH ONLY. PASS belongs to a particular test and declared scope.

## 3. Architecture and native authority
M3-Hybrid; C4 semantics at pinned commit and mathspec public Program. C5-R1 supplies outer typed trace, test and evidence records; no competing AST, solver or evaluator.

## 4. Inherited specification and precedence
The pinned C4 final_study_contract_language_specification.md, formal_semantics.md, canonical_normal_form_specification.md, supported_mathspec_subset.json, normalization_rules.md and extension_and_composition_policy.md define inherited constructs. This supplement extends only the outer C5 records. Native semantics take precedence for math.

## 5. Abstract syntax and version identity
D=(schema,base,requirements,metrics,tests); I=(schema,definition_ref,base,requested_tests,run_id,claims,attestations) for 0.2; 0.1 has no attestations. Package=(schema,D,I,receipt). Wire tags c5-vmodel-definition/instance/package-0.1 and -0.2 are distinct.

## 6. Concrete authoring
C3 structural A/B unchanged; A study_contract quoted-version { definition Object instance Object }; Object ::= { (Key : Value ;)* }; Value ::= Object | List | QuotedString | Integer | true | false | null; B strict JSON. Exact pins required. Native mathspec leaf authoring separate.

## 7. Metamodel and structural schema
final_metamodel.json and final_schema.json. Both version branches exact; schema admission is necessary, not sufficient. vmodel.check_design is semantic admission. Independent schema controls include valid 0.1, valid 0.2 and omitted required field.

## 8. Study frame, domains and subjects
C4 ContractFrame, qualified subject identities, declared finite axes, scenario/time support and study purpose. No implicit geographic or functional boundary.

## 9. Native mathematical subset
Unchanged pinned C4 supported_mathspec_subset.json. Static quantity/type checks and bounded finite evaluation; new native operator requires separate C4 extension, not outer record changes.

## 10. Physical and economic types
C4 unit, dimension, carrier, sign, conversion and price-year/basis semantics. Native incompatible comparisons rejected. No implicit monetary normalization or physical equivalence.

## 11. Components, ports and external behaviour
C4 component/port/link/observable references and scoped assertions; internal variables, equations, solver and topology abstractions remain model freedom subject to declared external obligations.

## 12. Assumptions, guarantees and guards
Inherited C4 Bool3 and A/G; no assumption silently established by a request. Explicit false/unknown semantics preserved.

## 13. Data and context contracts
C4 pinned snapshot, provenance, source/license/access references, complete support or native quality assertion. R1 quality target reuses actual data-contract identity and receipt, including context data, not a new predicate.

## 14. Chronology, information and states
C4 temporal order, endpoints, scenario information and nonanticipativity; native policy checks consume actual receipts; state check reads endpoint/cycle assertion truth, not binding alone.

## 15. Variation, pairing and comparison
Reference/project pairing and authorized variation inherited from C4. Native comparison validates exogeneity and change policy; full declared context coverage and actual identities required.

## 16. Study requirements
Versioned qualified IDs, nonempty statement, explicit source_kind/source_ref/authority_ref and scope. STUDY roots; required STUDY metrics and validation linkage; no regulatory claim inferred.

## 17. System requirements and derivation
SYSTEM descendants and external target references. Parents form DAG; equal axis sets and child subjects contained in parent. COMPLETE_SUBJECT_COVERAGE checks union of required direct child subjects. No logical entailment solver.

## 18. Requirement dependencies and normativity
Separate depends_on prerequisites must PASS; reject cycles across child/dependency assessment edges. Normativity RESEARCH_ASSUMPTION, INFORMATIVE, NORMATIVE_REQUIREMENT_PENDING_OWNER; informative cannot be required.

## 19. Metric roles and references
STUDY points to output, VERIFICATION to native assertion/comparison/output/policy/state/data-quality/report, VALIDATION to report. No orphan metric. Every mandatory verification/validation metric covered per requirement; every mandatory study metric output is an explicit validation input.

## 20. Native acceptance criteria
Native criterion linked to actual output dependency across typed UPSTREAM edges; no duplicate formula parser. Binary/typed native assertions and comparisons retain native conditions/tolerances. A syntactic dependency is not a sensitivity/entailment proof.

## 21. System Test Specification
id, version, kind, objective, requirements, metric, criterion, scope, oracle_ref, method, coverage, evidence, input_refs, preconditions, procedure_ref, reviewer_refs, applicability. All referential and role/scope checks are fail-closed.

## 22. Native test library
NATIVE_ASSERTION, NATIVE_COMPARISON, NATIVE_POLICY, NATIVE_STATE, NATIVE_DATA_QUALITY. Actual C4 receipts required. DATA_QUALITY explicitly includes dependent quality assertion slot inputs/observables and conversion source when required. Finite target scope and quality assertion scope must be covered.

## 23. External test library
EXTERNAL_PROCEDURE and EXTERNAL_REVIEW reference pinned typed report and procedure source; external tool/human produces attestation, DSL does not run arbitrary code. All declared reviewers must attest exact test and inputs. Missing reviewer blocks, conflicting signed results inconclusive.

## 24. Applicability and preconditions
Existing C4 guard with explicit slot or constant; true/false/unknown. False whole-test applicability gives NOT_EXECUTED with FALSE applicability; unknown/mixed gives INCONCLUSIVE. False/unknown precondition blocks an otherwise applicable test. No N/A-based validation.

## 25. Coverage and traceability
Requirement linked test scopes cover declared subjects; mandatory targets and metrics covered for every requirement. Native inputs are exact declared slot support including precondition, guard, comparison and quality dependencies. Universal safety/prohibition points can be replayed up to 10000; larger support conservatively inconclusive. Service request/witness folds inherited; no universal proof.

## 26. Execution and assessment
Separate execution/applicability/verdict/diagnostic. Requirement local and derived statuses: FAIL, INCONCLUSIVE, BLOCKED, NOT_EXECUTED, NOT_APPLICABLE, PASS. Required child failures dominate; N/A parent plus applicable required child cannot become PASS. A computed study metric gets pinned-validation status only with passing linked actual validation evidence and all applicable mandatory study assessments PASS.

## 27. Evidence, attestation and provenance
Unsigned claims cannot establish PASS. Native counterexamples retained. Ed25519 over canonical id/version/payload; exact definition and base instance roots, run/test/criterion/version, method/data identities, coverage, observed value and artifact SHA-256. Unique qualified evidence IDs, distinct reviewer key fingerprints and source roles. Pinned key possession is not independent reviewer identity.

## 28. Canonical Semantic Normal Form
C4 CSNF unchanged. Outer semantic identity from C4 native identity plus admitted sorted registries and reference sets. Exact definition/instance/source digests distinct. Export canonical bytes; reimport recomputes identical receipt. A/B preserves different source audit identity. No unrestricted E2–E5 equivalence.

## 29. Method composition and authorized changes
C4 compose_method requires exact request/authorization pins, allowed changed expressions and protected outer trace. revise_requirements requires exact old/new pins, full change set, scoped authority and version bump on changed existing record; protected C4 base. New independent authoring is not an authorized transition. Research authorization only.

## 30. Migration and compatibility
migrate_r1 explicitly adds reviewer sources, new tags, new roots, required normativity mapping for original-source requirements and new test bindings. Discards old claims; reexecute. Legacy 0.1 behavior retained and checked using 45 exact hashes.

## 31. Diagnostics, evidence limits and evaluation
Structural rejection, native receipt, expected negative result, unknown and internal failure are distinct. Tests are finite synthetic evidence; signed artifacts may be scientifically wrong; no real auditor, no broad solver/model equivalence, no actual human authoring measurement. See C5_R1 evidence, historical coverage and residual risk register.

## 32. Release, extension policy and 04B handoff
No release solely from green tests. Original C5-G0–G12 reviewed without scope waiver. New mathematical constructs require separate native evaluation; new outer constructs require demonstrated missing semantics and compatibility. Use pinned candidate only within recorded status. No automatic 04B; C5_R1/gate_status.json and handoff/BUNDLE_ML_04B_HANDOFF.md control.

## Detailed technical supplement
**NON-NORMATIVE / RESEARCH ONLY; OWNER_TBD.** Release designation depends on the actual C5-R1 gates, not this document.

## Scope and inheritance
C4 normative-for-this-research-candidate syntax, type and domain semantics are inherited exactly from commit 6920aade2f6b7517a49e8c9c3a21843c9e71fd9b. C4 native mathspec commit 5f1464c334c1012cdee2947d4d55b4d1d6bef40a is the sole mathematical authority. M3-Hybrid; no optimizer, new mathematical AST, or CBA-specific primitive. The existing 0.1 definition/instance/package remains accepted by vmodel.py, and C5-R1 introduces explicit 0.2 wire tags.

## Abstract syntax and identities
D=(schema,base,requirements,metrics,tests). I=(schema,definition_ref,base,requested_tests,run_id,claims,attestations) for 0.2; 0.1 omits attestations. Package=(schema,D,I,receipt). final_schema.json has two exact structural branches; final_metamodel.json describes the 0.2 records. C3 structural authoring A/B remains unchanged. C4 canonical mathspec packages are not replaced. Definition semantic identity includes native C4 semantic identity and sorted registries/reference sets. Exact definition/instance/source hashes are separate. Signed payload uses exact canonical JSON of id, version and payload. Reimport recomputes and compares the entire canonical package; source audit identity preserves A/B differences. No equality claim for arbitrary mathematical formulations.

## Requirements, scope and trace
Requirement holds id, version, level, statement, source kind/reference, authority, scope, required, parents, targets and metric_refs; 0.2 adds normativity, refinement_policy and depends_on. Normativity is RESEARCH_ASSUMPTION, INFORMATIVE or NORMATIVE_REQUIREMENT_PENDING_OWNER; informative cannot be required. Study roots, system descendants; DAG and all references validated. Scope contains another iff their named axis sets coincide and child subjects are contained in parent subjects. Axis projection is not a refinement. DIRECT_AND_CHILDREN aggregates local and required descendant outcomes. COMPLETE_SUBJECT_COVERAGE additionally requires the union of required direct child subjects to equal parent subjects. This establishes declared subject coverage, not logical entailment. Requirement scope is covered by its linked tests, mandatory criteria by their linked tests, and every mandatory verification/validation metric by a test for that requirement (not merely somewhere in the study). Mandatory study metric outputs must be explicitly present in validation test input references. No orphan metric. Independent depends_on links identify prerequisites (must PASS), and cycles across required-child and dependency assessment edges are rejected. No implicit requirement satisfaction from study metric values.

## Metrics, methods, tests
Metrics keep roles STUDY, VERIFICATION, VALIDATION and typed target references. Native output metric may be linked to an assertion in another slot only by actual native public-Program expression/parameter references and transitive typed UPSTREAM edges. Target type, units and economic basis remain C4 responsibilities. Test definition gives id/version/objective, requirements, metric/criterion, scope, oracle source, method, coverage, evidence role, explicit input_refs, preconditions, procedure_ref, reviewer_refs and explicit applicability. Applicability reuses C4 guard evaluation: a true/false/unknown constant or a guard bound to an existing native slot; mixed point truth is inconclusive at whole-test level. A false applicability is reasoned N/A; a false precondition blocks an otherwise applicable test. Native input coverage equals actual criterion and precondition slot dependencies. The precondition's scope must contain the test scope; unknown or false precondition blocks execution assessment. The native adapters are NATIVE_ASSERTION, NATIVE_COMPARISON, NATIVE_POLICY, NATIVE_STATE and NATIVE_DATA_QUALITY. State binding itself is not a test result; actual endpoint/cycle assertion truth is required. Native data-quality targets cover any existing typed data contract, including shared and contextual inputs; scope is checked against its declared axes and subject. EXTERNAL_PROCEDURE and EXTERNAL_REVIEW reference a typed report and pinned procedure source. External evaluation is not run by this DSL. All declared reviewers must attest the exact same test scope, version and input roots; missing reviewers block and conflicting signed outcomes are inconclusive.

## Finite coverage and evidence
Native comparison verifies full declared support and actual data identities. Universal safety/prohibition assertion point replay reuses existing C4 evaluation; explicit restrictions are recorded as exclusions and unknown points remain inconclusive. The finite replay resource limit is explicit. Other native assertion kinds retain the C4 quantified/request/witness fold. External coverage is a signed declaration over exact domains and subjects, not an automatically validated external experiment. Signed evidence is verified using Ed25519 against distinct pinned PROVENANCE public keys. Test/criterion/version, definition and base instance roots, method identities, run id, data identities, expected scope, observed result and inline report SHA-256 are signed. A signer may not be the same registered source as the oracle, procedure, slot or model source; duplicate key fingerprints are rejected. This proves possession of a definition-pinned key and integrity of bytes, not real reviewer independence, owner authority or scientific truth. No arbitrary executable is accepted; no private key stored. Unverified claims cannot create a pass, and a known native counterexample is not erased by an opposing unverified claim. Local and derived requirement status are separate. Overall contract conformance remains NOT_PROVED. Missing/incomplete evidence is not satisfaction.

## Change and migration
compose_method uses C4 explicit versioned research-only authorized composition; stable requirement and test IDs, new definition/method roots and fresh evidence required. migrate_r1 converts 0.1 to 0.2 explicitly with caller-supplied reviewer key sources; records old roots and discards unverified old claims; reauthor normative/refinement policy if applicable. Original-source requirements require an explicit normativity mapping during migration. It does not infer regulatory requirements. revise_requirements binds exact prior/proposed roots and the complete changed record set to a separately pinned research authorization, requires version changes for changed existing records, and protects C4 base content. Direct authoring of a new root is not an authorized transition. Evidence must be renewed after any changed root. Structural schema validity alone is not semantic admission.

## Limits
No general logical implication solver, arbitrary scope-axis refinement, unbounded/continuous verification proof, automatic external procedure execution, real independent auditor credentials, real model-tool integration, or normative method release. Generic external procedure source can declare further test classes, but procedure semantics and real correctness are outside this interpreter. Finite tests, same-design A/B and synthetic signers are technical evidence only. No global language minimum, empirical authoring or independent human review claimed. Current release decision is recorded separately in C5_R1/gate_status.json.
