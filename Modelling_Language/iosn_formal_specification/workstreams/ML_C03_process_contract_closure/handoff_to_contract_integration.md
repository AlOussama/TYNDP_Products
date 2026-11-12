# ML-C03 — Handoff to IoSN Contract Integration

**Research baseline:** ML-R00 consolidation PR #32, commit `9162def25d22c37b1fbc38f7d80fe929425cc8d2`. **Workstream:** ML-C03 process / data / mathematical contract closure. **State:** `RESEARCH_TRACEABILITY_RECONCILED_WITH_EXPLICIT_OPEN_DEPENDENCIES`. **No normative language, serialization, architecture or methodology choice. No real-data/source release. No native energy-model implementation. G1 BLOCKED.**

## 1. Integrationsgegenstand und gesicherte Bestandszahlen

| Artifact / provenance type | Scope and observed coverage | Meaning / status |
|---|---|---|
| R01 process semantics | P00–P17 **18/18** | Original research process obligations; not executed |
| R01 mathematics | M01–M18 **18** | Scientific mathematical families and open oracles, not complete native equation witnesses |
| MA01 system requirements | **48 active** SR IDs; SR-012 and SR-049 excluded from implementation | Provisional L2 source, unchanged |
| R03 B01 data objects | **87**, of which **67** direct-SR-linked and **20** process-only | Original analyst inventory and trace relations, not Owner approved |
| B01 source trace relationships | **93** distinct `B01-T` linked to 93 individual B01-D/SR pairs | Preserved; these links are original relative to R03 but not normative |
| Internal data types | **35** proposed producer mappings | Structural coverage only, two serious authority exceptions B01-D072 / B01-D081 |
| R03 transformation/workflow proposals | **38** T IDs over 18 P | Not all ETL; includes math/solve, governance and postprocess |
| R03 transform DAG | **47** distinct T→T edges, acyclic | Exact structural graph, not the full R01 controlling workflow |
| ML-C03 matrix | **204** typed rows = 93 direct + 20 process-only + 35 producer + 38 transformation + 18 process anchors | New nonnormative cross-layer reconciliation |
| ML-C03 exception register | **108** rows = 87 B01-D + 21 process/exception rows | All unresolved/not executed; includes 8 new cross-layer link gaps |
| R04 verification | 48 SR tests, V1–V6, E01–E08, synthetic C01–C10 | Tests designed; native solver/data execution NOT_EXECUTED |

## 2. Neun abzugebende ML-C03-Artefakte

1. [End-to-End Process Contract](end_to_end_process_contract.md) — alle 18 Prozessverträge mit neun Analysefeldern, SR/M-R04-Zuordnung, Parametrierungs-/Verifikationsblockern.
2. [Process/Data/Math Matrix](process_data_math_dependency_matrix.csv) — 204 typisierte Quell-/Vorschlags-/Process-Ankerzeilen; originale 93 B01-T-Beziehungen nicht überschrieben.
3. [Transformation Semantic Obligations](transformation_semantic_obligations.md) — 38 einzelne Transformations-/Modell-/Governance-Obligationen, Invarianten nur nach dimensionsgültiger Semantik.
4. [Data Lineage and Process DAG](data_lineage_and_process_dag.md) — 47 Kanten, azyklischer T-Graph, separater R01-Prozess- und Owner-Kontrollgraph.
5. [Data Allocation and Exception Register](data_allocation_and_exception_register.csv) — vollständige 87 B01-D plus 21 Ausnahmen/Reviewfragen, keine neue SR.
6. [Model Input / Output Boundary](model_input_output_boundary.md) — Original/Derivat/Parameter/Variable/Raw/KPI/Need + Kontroll- und Evidenzobjekte.
7. [Data/Transformation Verification Cases](data_transformation_verification_cases.md) — 18 prozessbezogene, 20 kritische falsifizierbare Testdesigns, strukturelle Prüfungen und Stop-Regeln.
8. [Independent-Role Process Review](independent_process_contract_review.md) — kritischer adversarial Self-Review **ohne** unabhängige institutionelle Freigabe.
9. Diese Übergabe — Verantwortung, Übernahmebedingungen, Nichtentscheidungen und nachgelagerte Integrationsfragen.

## 3. Contract-element vocabulary für die spätere Zusammenführung (neutral, nicht als DSL)

| Logical entity | Minimum typed relationship / property needed | Why relevant |
|---|---|---|
| `SourceRelease` / `MethodologyProfile` | `source_id/version/authority_status/effective_scope/approved_override_ref` | O26 DRAFT versus D1–D6 research overlay, source gate |
| `DataDefinition` / `DataInstance` | `has_definition / originates_from / belongs_to_study_year / belongs_to_CY / has_spatial_and_temporal_grain / has_unit` | Original and 87 derived/source data types remain resolvable |
| `ProcessStep` | `P_id, applicability, pre/postconditions, upstream_control_dependencies` | All 18 P; optionality and governance not collapsed into ETL |
| `TransformationSpec` / `Execution` | `input_refs, output_refs, kind, invariant_scope, transform_version, evidence, exception_status` | 38 proposals, 47 structural edges and model/solve operation types |
| `ModelParameter` / `DecisionVariable` / `Constraint` | `physical_quantity, unit, carrier, indices, exogenous_or_endogenous, stage, source_ref, witness_ref` | Match R01 M01–M18 without prescribing a tool's internal formulation |
| `ModelRun` / `SolverWitness` | `run_type, model_snapshot, input_freeze, candidate_set, status, primal/dual/residual_if_applicable` | Prevent synthetic proof passing as real LP/OPF execution |
| `RawResult` / `DerivedIndicator` / `SystemNeed` | `is_derived_from / uses_metric_definition / is_reported_as / has_project_approval_status` | KPI definition, filter, comparison and no system-need→project approval |
| `Requirement` / `MathematicalObligation` / `Test` / `Evidence` | `traces_to / verifies_claim / witness_type / per_test_status` | Preserve R00 48-SR and R04 V/D/E evidence graph |
| `OwnerDecision` / `Exception` | `decision_id, authority, open_reason, affected_entities, blocker_scope, resolution_evidence` | Process gaps and unknown methodological rules never silently filled |

**Typed relation authority flag:** `ORIGINAL_B01_ANALYST_LINK`, `MLR03_TRANSFORMATION_PROPOSAL`, `MLC03_RESEARCH_CROSSWALK`, `OWNER_AUTHORIZED` (future only), `EXECUTED_AND_VERIFIED` (future only). Avoid merging these meanings into one boolean `approved`. A graph link may exist without physical correctness, execution or authority.

## 4. Scientific semantics that must survive any future contract representation

- **Horizon:** 2035, 2040 and 2050 as distinct study contexts; no generic cross-horizon investment linking.
- **CY/weights (D2):** five externally selected CY1–CY5 with the *same case-specific weight vector across years*, not equal weight over CY, with numeric weights and upstream selection evidence TBD. O26 three-case weather profile remains a source-difference, not an implicit rewrite.
- **UTC/units (D4):** canonical UTC/interval/duration and native conversion provenance; DST/leap and quality tolerance TBD, no indiscriminate MW/MWh or electricity/H2 conversions.
- **Physical vs candidate links:** reduced existing electrical graph obeys DC/mesh/contingency semantics; new transfer candidates are controllable directional DC market links with NTC and bounds.
- **LP and expansion:** shared per-year x across CY, stages P10 (real) → P11 (remaining/conceptual/theoretical) with **unresolved F_y** → P12 storage only 2040/2050; no duplicate costs.
- **Coupled assets:** electricity and H2 distinct carriers, exogenous H2 infrastructure, P2G/H2-to-power efficiencies, five hydro classes, explicit storage energy and DSR types.
- **P13–P15:** controlled with/without paired dispatch, P14 preexpansion H2 freeze sourced to validated baseline, P15 optional with LF cap and separate result stream.
- **P16/17:** RawResult is not a KPI or SystemNeed; B01-D081 filter and monetary KPIs need external owner rule; reported system needs do not approve projects. Test PASS requires actual evidence and correct scope; different valid optimal portfolios must be compared semantically.

## 5. Integration-blocking questions, not automatic design decisions

| Issue / register ref | Required integration action (research) | Later Owner evidence (not in current wave) |
|---|---|---|
| **ML-C03-E14** P01→P02 | Distinguish StudyManifest procedural applicability from actual data input relation | Study/Weather owner release |
| **ML-C03-E15** P06→P08 | Ensure reduced physical-grid inputs and evidence are represented at model boundary, not inferred from P07 zoning | Network-model owner + equivalence oracle |
| **ML-C03-E16** P12→P13 | Clarify if storage stage state materially conditions paired dispatch or only acts as a methodological predecessor | Dispatch/Storage owner |
| **ML-C03-E17** P12→P14 | Explicitly distinguish process ordering from *pre-expansion* H2 baseline producer; never source baseline from postexpansion P12 | H2 baseline model owner / named run |
| **ML-C03-E18/E19** P12/P13→P15 | Define optional OPF internal capacity/basis, LF cap and applicable dependency type | Method/OPF owner |
| **ML-C03-E20** P17 evidence | Integrate all R04 mathematical/solver/KPI source evidence ports as typed relations not all as unstructured data payloads | Independent verification owner |
| **ML-C03-E21** P15→P16 | Make optional output a conditional input, and prove NOT_APPLICABLE only on P15 branch | Model/report owner |
| **B01-D072/T14-00** | Add `pre_expansion_baseline_run_ref` as an explicit unresolved *required* precondition | MD-10 named source/model/run, validity witness |
| **B01-D081/T16-00** | Reclassify authority need without rewriting original R03 object class; reference owner-issued filtering definition | MD-04/17 policy/version/threshold/grain |
| **B01-D063** | Model `F_y` as unresolved typed StageCarry transition, not as a data default | MD-07 investment and cost rule |
| **B01-D024–D030/D086–D087** | Keep PTDF/LODF/N−1 and equivalent mapping separate from generic power conservation | MD-03/13/15 reference data/thresholds |
| **B01-D078–D080** | Treat KPI/ONDP aggregation and publication as owner-formula-dependent gates | MD-04/05/17 versioned formulas and signatures |

These issues may be reconciled by the parallel semantic (ML-C01) and metamodel (ML-C02) research streams, but **nothing in ML-C03 imports their unreviewed findings, settles their design choices, or changes either workstream**.

## 6. Handoff acceptance criteria for the next integration research stage

1. **Graph/identity:** every typed data, process, transformation, SR, M, test and evidence record has a stable namespace and source-resolution rule; test the 204 matrix rows, 108 exceptions and 47-edge DAG against immutable R00 source.
2. **Authority:** distinguish source-adoption, Owner decisions, analytic original-B01 links, research proposals and executed evidence independently.
3. **Semantic crosswalk:** classify each R01/R03 discrepancy as `PROCEDURAL_DEPENDENCY`, `DATA_PRODUCER_CONSUMER`, `MODEL_STATE_DEPENDENCY`, `CONDITIONAL_APPLICABILITY` or `OWNER_POLICY_REFERENCE`; **do not add a producer edge without source basis**.
4. **Math/test:** preserve M01–M18 carrier/dimension/phase conditions and R04 V1–V6, D0–D4 (test depth) and E01–E08; avoid literal solver-variable identity as cross-tool proof.
5. **Two-tool readiness (future):** portable original/frozen inputs plus acceptance oracles, stage/marketlink physics, baseline H2 witness, KPI definition, and independently run solver outputs are required before pilot or conformance claims.
6. **Validation limit:** the static self-audit can establish source-cardinality/graph coverage only; it cannot qualify data, approve mathematical tolerances or decide G1.
7. **Change protection:** future work writes outside R01–R04 only, preferably new workstream, and records source mapping as nonnormative until appropriate Owner decisions. No mass rewriting of the 93 B01-T references.

## 7. Explicit non-decisions and closure statement

No selection of DSL, YAML/JSON/SysML/ReqIF, runtime orchestrator, data exchange standard, native solver, tool architecture, automated cross-tool conversion or constraint code generator. No robustness requirement added. No productive OriginalSource/data release, no numeric WACC/WEATHER weights, no accepted network RMSE/N−1/LODF or KPI threshold, no baseline H2 solver invention, no independent certification, no actual IoSN model implemented.

**Research traceability: STRUCTURALLY_RECONCILED_WITH_EXPLICIT_OPEN_DEPENDENCIES. Scientific production contract: NOT_COMPLETE. Methodology authority: UNCONFIRMED. Original data qualification: NOT_PERFORMED. Independent signoff: NOT_OBTAINED. G1: BLOCKED.**
