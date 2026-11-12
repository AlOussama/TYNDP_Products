# ML-C02 — Canonical IoSN Contract: conceptual metamodel (research v0.1)

**Research snapshot:** 2026-11-12; ML-R00 commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2, Draft PR #32. **State:** NONNORMATIVE / AUTHORITY_UNCONFIRMED / G1_BLOCKED. No DSL, serialization, tool stack, architecture or source approval is chosen.

## 1. Contract boundary and intended semantics

The conceptual contract is the **single semantic interface** from source methodology and owner-governed research profile to independent tool implementations, input/transform lifecycle, model behaviour, outputs and checkable evidence. It **does not** encode or prescribe a particular tool's internal asset classes, native optimisation expressions or converter. The existing **48 active MA01-SR are the only active provisional L2 requirements baseline**; P00–P17, M01–M18, LR01–LR20, R03 data/transforms and R04 verification records are typed elaborations and trace nodes, not replacement L2 requirements.

D1: 48 active SR (not SR-012/SR-049). D2: external CY1–CY5, same symbolic weight **vector across 2035/2040/2050**, not necessarily uniform across CY; numerical values TBD. D3: mandatory fail-closed. D4: UTC interval/unit semantics (MD-12 details TBD). D5-A1: risk-proportionate mathematical proof, not universal syntactic identity. D6-A: shared contract, independent model construction. O26 is the **25 February 2026 consultation draft**, with three cases per target year as a separate source claim: its authority and D2 reconciliation remain open.

The core is a **typed, versioned semantic graph plus explicitly-scoped assertions**. A graph can be persisted as a registry, a typed integrated model, or federated governed views. None is selected here.

## 2. Conceptual graph

~~~mermaid
flowchart LR
  S["MethodologyProfile / SourceClause"] -->|DERIVED_FROM| R["Requirement + Applicability"]
  G["GovernanceDecision + ReviewStatus"] -->|BLOCKED_BY / governs| R
  R -->|APPLIES_TO| P["ProcessStep + Transformation"]
  R -->|REFINED_BY| M["MathematicalObligation / ConstraintFamily"]
  R -->|REQUIRES_CAPABILITY| L["LR01–LR20"]
  D["SourceRelease / DataObject / DataInstance"] -->|CONSUMES / PRODUCES| P
  P -->|ASSEMBLES| I["ModelInput"]
  M -->|CONSTRAINS| I
  I -->|independent IMPLEMENTS| U["Tool-specific realization"]
  U --> O["ModelOutput / DerivedMetric"]
  V["VerificationCase / Oracle"] -->|VERIFIES| R
  V -->|observes| U
  V -->|requires / HAS_EVIDENCE when actual| E["Evidence"]
  O -->|HAS_LINEAGE| D
  E -->|reviewed under| G
~~~

The diagram is a **semantic relationship diagram** rather than a prescribed runtime pipeline. Repeated time, carrier, topology and study scopes are value-types referenced by the graph; they need not each be independently stored objects. Each arrow is typed and carries a profile/version scope and research/approval status. **An absent Evidence object cannot be replaced by a prospective evidence request.**

## 3. Logical layers and irreducible distinction

| Layer | Contract meaning | Cannot be collapsed into |
|---|---|---|
| Source/authority | versioned methodology clause, provenance, override reason, effective scope | locally checked schema, a source draft marked approved |
| Obligation | stable L2 requirement, trigger, fulfilment condition, uncertainty | equation or test ID alone |
| Case/axis/topology | independent study run, external CY, time intervals, scenario, spatial/carrier identity | untyped string or tool-bus identifier |
| Data | a definition distinct from a particular immutable instance/release | a CSV path/column name alone |
| Process | step, precondition, transformation, producer/consumer and transformation execution lineage | one undifferentiated solver run |
| Scientific model | objective/feasible-set semantics, decisions, restrictions, observable projection, modes/stages | fixed equation AST or tool syntax |
| Outputs | raw computed result versus definition/recomputation of system needs/KPI | approval of a physical investment project |
| Verification | independently falsifiable case, approved-or-TBD oracle, actual evidence, scoped verdict | PASS of a synthetic fixture or a document review |
| Governance | owner decision state, reviewer independence, G1 gate | a test-state field |

Definitions of core/extension attributes and multiplicities are in **contract_entities_and_types.md**; domain/range semantics are in **typed_relationship_vocabulary.md**. Invariants are IDs **INV-01…INV-30**, not new MA01-SR.

## 4. Reference and identity semantics

- Reference key: (**namespace, stable_id, semantic_revision**). Distinguish object identity from content-hash, tool-internal handle, source clause locator and run instance. Never assume equivalence between network bus, IoSN zone, market zone, corridor, technology and candidate ID.
- A ResearchContractSnapshot binds immutable **baseline commit**, a MethodologyProfile revision, source authority state, D1–D6 research overlays, catalog revisions, graph vocabulary revision and selected data/solver run references. Snapshots are append-only; revisions to a requirement text are controlled changes to the upstream baseline, **not** permitted under ML-C02.
- Source assertions record **source_class** (draft, historic, owner decision, derived-scientific, illustrative), provenance and validity/applicability. Draft O26 does not turn into an effective adopted source because a derived invariant is demonstrable.
- The graph supports both mandatory and conditional obligations. Applicability evaluates to **TRUE, FALSE or UNKNOWN** from an explicit witnessed predicate. UNKNOWN is BLOCKED when it governs mandatory assessment; FALSE only permits a documented conditional NOT_APPLICABLE.
- Relationship evidence can be **RESEARCH_MAPPING_UNCONFIRMED** even when its referential integrity passes.

## 5. Minimal-core versus full coverage

**Minimal irreducible semantic core** (roles, not mandatory implementation classes): identity/revision/authority; Requirement + Applicability; Case and typed axes; Spatial/Carrier/Asset role; Data definition/instance/release; ProcessStep + Transformation; mathematical obligation with variable/constraint semantics; raw result + derived metric; VerificationCase + Oracle + Evidence; governance/status; typed relationships.

**Full catalogue view** extends the core with source-document clauses, detailed circuit sensitivities, identity crosswalks, transformation executions, solver witnesses, risk policies, stage-specific decision scopes, detailed validation depths, source artifacts, formula versions, provenance and all P00–P17 instances. Lossless mappings from extension to semantic roles are required.

A proposal is **not minimal** merely because it has few boxes. A collapsed generic “Asset”, “Constraint”, “Value” or “Status” is only permissible if it still preserves (a) physical branch versus controllable expansion market link, (b) D2 nonanticipativity, (c) MW vs MWh / UTC/Δt, (d) release-vs-instance lineage, (e) output-vs-need and (f) six separate test outcomes plus owner/G1 state. Conversely separate database tables for every subtype are not obligatory.

## 6. Closed-world traceability, open-world science

**Structural closed world:** all 48 MA01-SR IDs, P00–P17, M01–M18, LR01–LR20, B01-D001…D087 and 48 R04 test IDs are explicitly represented, with valid typed references. R03's 20 process-only data objects are linked to a process without creating any SR. In the materialized **contract_traceability_model.csv**, NODE and EDGE records share a manifest, allowing a referential-closure audit.

**Scientific open world:** a structurally complete graph may still have unknown source authority, original release/hash, weight values, network and KPI oracles, stage transfer, or independent tool evidence. The metamodel **must permit these unknowns without fabricating values** and must block productive full conformance. Unknowns can be described in research, but cannot silently count as implemented.

## 7. Architecture-independent realization test

Equivalent semantic exports must reconstruct the same **typed nodes, referential closure, scope predicates, decision/constraint families, stage modes and evidence claims**, preserving source/version IDs and unresolved-owner markers. A modular registry (R02 A), integrated metamodel (R02 B) and federated governed views (R02 C) are alternative realizations of **the same conceptual graph**, not competing L2 baselines and not alternative energy models.

A valid round-trip must preserve identity, applicability, dimensional typing, directionality, optionality, nonanticipativity and source authority. Where information is lost, export **LOSSY_BLOCKED** with an explicit loss witness. Such a round-trip is a research experiment, not an architectural decision. See **handoff_to_architecture_experiments.md**.

## 8. Research limitations and source anchors

Research anchors at ML-R00 HEAD: unified_contract_concept.md and integrated_requirement_traceability.csv; ML-R01 mathematical_obligations.md and process_semantics_P00_P17.md; ML-R02 language_requirements_specification.md; ML-R03 input_contract_catalogue.csv / process_transformation_matrix.csv; ML-R04 requirements_verification_matrix.csv / test_catalogue.csv.

No normative source authority, original data qualification, production solver test, human-independent sign-off or G1 approval has occurred here. All supplied R04 native test states remain **NOT_EXECUTED**.