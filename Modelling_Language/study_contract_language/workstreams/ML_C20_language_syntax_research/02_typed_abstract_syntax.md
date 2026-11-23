# ML-C20/02 – Typed Abstract Syntax v0.1 (implementation-neutral)
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

```text
Contract = { frame:ContractFrame, referents:Ref[], relations:Relation[],
 predicates:Predicate[], assertions:Assertion[], observables:Observable[],
 variations:VariationPolicy[], evidences:Evidence[], authorities:Authority[],
 sidecar:SourceLedger }.
ContractFrame = (id:QualifiedID, schema:Version, rules:Version, registry:Version,
 question:Text?, boundary:QualifiedID?, time:TimeAxis?, scenario:ScenarioTree?,
 counterfactual:QualifiedID?, study_kind:StudyKind).
Ref = (id:QualifiedID, kind:Enum, type:QualifiedID, role:Enum?,
 quantity:QuantityType?, port:PortType?, scope:Scope?).
Relation = (id:QualifiedID, kind:Enum, from:QualifiedID, to:QualifiedID,
 cardinality:(min,max)?, authority:QualifiedID*).
Predicate = {id:QualifiedID, expr:Expr<T>, quantifier?:Quantifier}.
Assertion = (id, modality:Modality, semantic_role:AssumptionKind|GuaranteeKind,
 predicate_ref, scope:Scope, guard:Expr<Bool3>, authority_refs:QualifiedID+,
 decision_state:DecisionState, proof_duty?:QualifiedID).
Observable = (id, subject:QualifiedID, projection:Expr<Measure>, quantity:QuantityType,
 time_aggregation, spatial_aggregation, scenario_aggregation, basis, tolerance, selection).
VariationPolicy = (id, subject, alternatives:TypedChoice+, disclosure:Bool,
 extra_assumptions:QualifiedID*, proof_duty:QualifiedID?, source_refs:QualifiedID+).
Evidence = (id, role:REQUEST|RESULT, subject_ref, oracle, level, run_id?,
 status:NOT_EXECUTED|PASS|FAIL|INCONCLUSIVE|NOT_APPLICABLE|BLOCKED, source_refs).
Authority = (id, role:SOURCE|OWNER|DECISION|PROVENANCE, immutable_ref,
 revision, decision_state:APPROVED|PROPOSED|OWNER_TBD|REJECTED|SUPERSEDED|UNKNOWN).
```

## Value types and constraints
QualifiedID: namespace-qualified stable URI or declared unambiguous alias, never inferred from local name. Scope=(space_set,time_intervals,scenario_set,subjects,guard_ref) with explicit overlap test or UNKNOWN. Quantity=(physical_kind, dimension_vector, carrier, unit, reference_basis, sign_reference, direction, temporal_support), no automatic mass-energy conversion. Temporal support distinguishes instantaneous power from interval energy, sampling from integration, timezone/DST and weights. ScenarioTree defines root, stages, probabilities and nonanticipativity information partitions; *no* implicit future signal. Bool3 TRUE/FALSE/UNKNOWN; strict Kleene AND/OR/NOT under an explicitly versioned registry; UNKNOWN never satisfies GUARANTEE. Cardinalities are checked on typed relations; orders must be declared SEQUENCE or SET. SourceSpan=(document_uri,revision,range,source_id) exists in audit sidecar, not inside the comparison key as free text.

## Invariants
Unique IDs across namespace; every ref resolves to exactly one declared kind; source refs to Authority; assertions always have guard and valid source; no evidence result PASS without run/evidence/proof metadata; owner state never erased. Syntax candidates may reorganize nodes but may not remove semantic discriminators. This is a designed AST signature, not proof of semantic completeness or a concrete parser ABI.
