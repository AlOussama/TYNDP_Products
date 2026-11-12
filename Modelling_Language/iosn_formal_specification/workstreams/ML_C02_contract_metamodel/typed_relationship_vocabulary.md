# ML-C02 — Typed relationship vocabulary and graph contracts

**Status:** semantic relation vocabulary only, not RDF vocabulary, ontology commitment, property-graph API or schema syntax. **Notation:** A→B means source/target type; min..max cardinalities apply to an active contract snapshot and are conditional on the specified scope.

## 1. Relationships

| Predicate | Domain → range | Cardinality / semantics | Inadmissible interpretation |
|---|---|---|---|
| **DERIVED_FROM** | Requirement or obligation → SourceClause / provenance claim | SR ≥1 clause; every link source-versioned, authority distinguished | A draft clause is approved because the edge exists |
| **REFINES** | MathematicalObligation / ConstraintFamily / derived assertion → Requirement / broader obligation | M family ≥1 trace; many:many, edge carries justification | Refines means silently replacing original SR wording |
| **APPLIES_TO** | Requirement / obligation / Applicability → ProcessStep, StudyCase or scoped role | 0..n; guarded by profile predicate | All instances always applicable |
| **REQUIRES_CAPABILITY** | Requirement → LR family / capability role | ≥1 LR per active SR in ML-R00 crosswalk | LR becomes a new source of methodology |
| **CONSUMES** | ProcessStep or Transformation → DataObject, DataInstance or intermediate type | 0..n P; ≥1 T; exact type & grain required | Generic object ID implies same instance/release |
| **PRODUCES** | ProcessStep or Transformation → DataObject, DataInstance or intermediate type | 0..n P; ≥1 T | Hypothesized producer proves executed transform |
| **LINKED_TO_PROCESS** | DataObject → ProcessStep | ≥1 per R03 object by declared process link; can coexist with 0 SR links | Process link automatically creates new SR |
| **INCLUDES** | ProcessStep → Transformation | each MLR03-T spec exactly 1 P | Claiming every proposed T was executed |
| **DEPENDS_ON** | ProcessStep, Transformation, output or claim → applicable upstream entity | 0..n; scoped DAG for execution-only links | Circular execution graph is acceptable |
| **IMPLEMENTS** | ToolModelRealization / adapter mapping → Requirement, obligation, capability | 0..n; implementation ID + scope/version/proof | Translation syntax alone establishes equivalence |
| **CONSTRAINS** | MathematicalObligation / ConstraintFamily → ModelInput or semantic variable role | 0..n; guard and objective/feasible-set mapping | All tools must emit same algebra |
| **VERIFIES** | VerificationCase → Requirement / MathematicalObligation / data invariant | ≥1 assertion target; 48 native SR tests remain NOT_EXECUTED | Test is successfully run because it was authored |
| **HAS_ORACLE** | VerificationCase → Oracle | ≥1 declared oracle request; accepted oracle optional in research; status explicit | An Oracle(TBD) is an accepted oracle |
| **HAS_EVIDENCE** | VerificationCase, assertion or tool claim → **actual** Evidence | 0..n; requires immutable artifact/fixture scope/run hash | Proposed evidence text or planned port is actual evidence |
| **REQUIRES_EVIDENCE** | VerificationCase → EvidenceRequest/Port | 0..n; planned evidence, separate type | REQUIRES_EVIDENCE entails HAS_EVIDENCE |
| **BLOCKED_BY** | Requirement, test, contract readiness or gate → GovernanceDecision / unresolved parameter / Oracle | 0..n; preserves root cause and effective scope | Open MD is an observed mathematical FAIL |
| **USES_RELEASE** | DataInstance / ModelInput → SourceRelease | exactly 1 external release for externally supplied instance; not for generated internal artifact | Unknown release may be assigned fictitious checksum |
| **TRANSFORMED_FROM** | DataInstance / derived output → DataInstance or SourceArtifact | ≥1 for derived instances, with transformation execution reference | An untyped transformation chain is evidence |
| **PUBLISHES_AS** | DerivedMetric → SystemNeed / output product | 0..n; formula, category, status controlled | System need automatically creates approved project |
| **REVIEWED_BY** | Evidence / decision / claim → ReviewRecord / reviewer role | 0..n, independence recorded; review can remain absent | AI self-review is institutional independent audit |
| **SCOPED_BY** | any scoped entity → profile/study/axis/stage/variant | ≥1 effective profile; axis links per type | Join across Y/C without explicit mapping |
| **EQUIVALENT_UNDER** | implementation/formulation → EquivalenceClaim | 0..n; assumptions, projection, target observations, comparison proof | Identical objective value alone proves equal feasible sets |

**Directional conventions:** for example Requirement DERIVED_FROM SourceClause; MathematicalObligation REFINES Requirement; VerificationCase VERIFIES Requirement; Transformation CONSUMES and PRODUCES DataObject. A storage engine may materialize reverse navigation, but not reverse semantic meaning.

## 2. Contract graph tuple and identity

Typed edge = (edge_id, subject Ref, predicate, object Ref, source_assertion_ref, authority_state, semantic_revision, scope_predicate, lifecycle_state). Edge ID is stable under re-export; semantic revision changes if meaning changes. Only relations compatible with the declared domain/range are admitted. The graph holds **both confirmed structure and unresolved semantics**; a VALID_REFERENCE flag is not an APPROVED_MEANING flag.

Node = (Ref, entity_type, label/source_record, profile_scope, state, revision). In the CSV materialization, **NODE** rows declare references and **EDGE** rows declare relationships. The CSV is a research traceability view, not the selected canonical serialization.

## 3. Integrity rules and impact analysis

- **FK closure:** all edge subjects/objects must resolve to unique NODE identities in the same pinned snapshot; no wildcard target and no duplicate NODE ID. Unknown external artifact IDs require an explicitly declared UNQUALIFIED placeholder with precise reason, not a made-up release.
- **Version closure:** join only compatible source profile, requirement baseline, semantic-vocabulary version and axes. A semantically incompatible revision either migrates under review or becomes BLOCKED; unchanged strings with changed meaning are not identical.
- **Scoped completeness:** every active SR has a source clause, verified process mapping or documented zero-process governance exception, ≥1 language capability, a VN/test and a planned oracle/evidence path. M families and R03-only object links need not create an SR edge.
- **Execution DAG:** no circular dependency among actual transformation execution events. A broad methodological “DEPENDS_ON” may describe conceptual iteration; such a cycle is **not** an execution DAG and must be labeled separately.
- **Transformation closure:** every consumed/produced intermediate type is registered. For an executed transform, input instance/release, output instance, parameter revision, execution ID and check results must be traceable.
- **Crosswalk correctness:** an n:m spatial crosswalk needs from/to namespace, topology version, effective region, factors and conservation/exception checks. Ambiguous mapping is blocked; type compatibility is necessary but not sufficient.
- **Change impact:** update to source clause or decision affects reachable refinements/SR, applicable process/T specs, model inputs, mathematical obligations, test oracles, raw outputs, derived KPIs and affected evidence. A prior PASS must not survive changed premises without a compatibility/replay decision.
- **Contradictions:** two claims with same intended scope but divergent meaning produce an explicit conflict record; one is not silently overwritten by an edge precedence inferred from chronology.

## 4. Example of a valid relationship path

Research path for SR-029: source-clause claim → **MA01-SR-029** → relevant P and M01, LR capabilities and B01-D data definitions → **MA01-VN-029** and **R04-T-SR-029** → proposed oracle request. If real execution evidence is absent, this chain has **REQUIRES_EVIDENCE**, not HAS_EVIDENCE; test remains **NOT_EXECUTED**. No project G1 approval may be inferred.

## 5. Anti-patterns

A “generic TESTED” relation without distinct oracle/evidence cannot represent six statuses. A bare same-name dataset link cannot establish a source release. A transfer edge from physical AC branch to an expansion market link without a physical-vs-controllable discriminant loses M05/M07 semantics. A direct SR→new invented data-source SR edge for all 20 process-only objects violates D1.