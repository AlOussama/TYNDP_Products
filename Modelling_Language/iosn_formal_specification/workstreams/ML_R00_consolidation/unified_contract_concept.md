# ML-R00 — Unified IoSN Scientific Requirements Contract Concept

**Integration Research v0.1 — 11 November 2026**  
**State:** NONNORMATIVE_CONCEPT / NO_DSL_CHOICE / NO_ARCHITECTURE_ADR / NO_SOLVER_MANDATE / G1_BLOCKED.  
**Original authoring baselines preserved:** ML-R01/PR26, ML-R02/PR27, ML-R03/PR28, ML-R04/PR29, common BUNDLE-01R PR25 HEAD \`5c13d4d63f18d30c308997cd7a01f2977fcc6b7b\`. This is a semantic *integration proposal* only.

## 1. Purpose: one method contract, multiple independent models

The IoSN Requirements Contract is an **authoritative interface candidate between the methodology, accepted input and output expectations, and each energy modelling tool implementation**. The eventual contract shall be tool-neutral, typed, verifiable and provenance-preserving. Different tool teams independently construct the corresponding network, market, storage, H2, hydro and optimisation models. A shared object model or a GEMS/INES/CESM exchange format is **not**, by itself, the method contract and does not prove correctness after translation.

The contract needs to articulate, at a minimum:
1. **what is being requested** (source clause, SR, research profile, conditional applicability),
2. **on what data** (source release, time/space/carrier/scope, transformation graph and integrity),
3. **how mathematical behavior is constrained** (objective, decision/scenario indices, physics, process modes, stages, permitted formulations),
4. **what is observed** (raw outputs, derived needs/KPIs, meanings, aggregation and assumptions),
5. **how it is verified** (test case, accepted oracle, independent evidence, severity, conditional status, reviewer),
6. **who may authorise it** (source authority, domain/requirements owners, independent reviewer and Gate G1; **not** a generated schema).

**Scope:** IoSN process P00–P17 (not CBA interoperation), no weather-year selection/reconstruction, no additional generic robustness criteria, no implementation of a full productive optimisation, no approval now.

## 2. Conceptual layers and typed links

~~~mermaid
flowchart TB
  S["SOURCE / GOVERNANCE<br/>O26 draft; older context; D1-D6; MD/CL TBD"] --> R["REQUIREMENTS<br/>48 MA01-SR + applicability + version"]
  R --> M["SCIENTIFIC SEMANTICS<br/>18 process steps; M01-M18 invariants"]
  R --> L["LANGUAGE CAPABILITIES<br/>LR01-LR20; A/B/C architecture alternatives"]
  M --> D["DATA & TRANSFORMATIONS<br/>87 B01-D objects; 38 MLR03-T specs"]
  L --> D
  D --> I["TOOL-SPECIFIC IMPLEMENTATION<br/>independent Tool A / Tool B / others"]
  M --> I
  I --> E["EVIDENCE<br/>E01-E08 exports, V1-V6, D0-D4"]
  R --> V["VERIFICATION CASES<br/>48 MA01-VN / R04-T-SR + C01-C10"]
  V --> E
  D --> E
  E --> O["OUTPUTS<br/>raw results, versioned KPI definitions, system needs"]
  O --> G["SCOPED REVIEW & GATE<br/>separate Owner approval, independent review, G1"]
  S -. "approval authority, not inferred" .-> G
~~~

**Read the diagram as conceptual dependencies, NOT a prescribed software stack or mandatory runtime order.** P00 and P17 are governance/review boundaries, P15 is a **conditional** analysis, and every model/tool can use native internal data layouts if it exports a semantically complete evidence surface.

### 2.1 Namespaces and reference rules

| Existing namespace / source | Stable identity | Proposal for unified cross-reference | No silent promotion |
|---|---|---|---|
| O26 / H24 / CBA4 and D1–D6 | \`source_clause\`, \`source_version\`, \`source_kind\`, \`authority_status\` | every obligation has a source and scope/override type | O26-DRAFT ≠ owner-approved; H24 ≠ default 2026 |
| MA01-SR | \`MA01-SR-NNN\`, 48 active IDs | **master obligation ID**, with original text and optional trigger | no new SR-012/-049; MA01 stays unchanged |
| MA01-MR | 50 method claims, two out-of-scope weather selection claims | retained as source references | no weather selection implementation |
| R01 | \`P00…P17\`; \`M01…M18\` | process and mathematical obligations | illustrative equations ≠ approved numeric formula |
| R02 | \`LR01…LR20\`, ReqIF/LinkML/etc. references | language **capability**, not second method owner | no architecture/DSL decision |
| R03 | \`B01-D001…B01-D087\`, \`B01-Txxx\` trace links, \`MLR03-Txx-yy\` | data object / original trace edge / proposed transform | producer and 93 links not yet domain approved |
| R04 | \`MA01-VN-NNN\`, \`R04-T-SR-NNN\`, \`C01…C10\` | verification need, test proposal and synthetic fixture | ten synthetic oracle PASS ≠ native model test PASS |
| R04 | \`E01…E08\`, \`V1…V6\`, \`D0…D4\` | evidence exports, **verification layers** and **test-depth** dimensions | D4 here = deep equivalence **test depth**; do not confuse with **project decision D4=UTC/units** |

**Namespace collision rule:** Always write \`project_decision:D4\` when referring to UTC/unit decision and \`test_depth:D4\` when referring to deep equivalence checks. They are distinct namespaces. Likewise \`R04-C01\` is a synthetic fixture, not an official contractual KPI.

### 2.2 Typed relation vocabulary (proposed, not released)

\`DERIVED_FROM_SOURCE\` (methodology claim → source clause), \`REFINES\` (SR → mathematical/process obligation), \`REQUIRES_CAPABILITY\` (SR → LR), \`CONSUMES\`/\`PRODUCES\` (P/transform ↔ data instances), \`USES_PROVENANCE\`, \`IMPLEMENTS\` (tool realization → SR), \`TESTS\` (VN/test → invariant), \`HAS_ORACLE\`, \`HAS_EVIDENCE\`, \`APPLICABLE_IF\`, \`BLOCKED_BY_DECISION\`, \`REVIEWED_BY\`, \`PUBLISHES_AS\`. A relation carries **source/head SHA + semantic revision + proof status**. A missing link or a link to a placeholder cannot become \`VERIFIED\` solely because both endpoints exist.

## 3. Science and model semantics, reconciled from R01→R04

### 3.1 Scenario and temporal contract

For three **separate** study years \(Y=\{2035,2040,2050\}\) receive externally selected \(C=\{CY1,\ldots,CY5\}\). Project D2 means

\[
\pi_{2035,c}=\pi_{2040,c}=\pi_{2050,c}=\pi_c,\quad
\pi_c\ge0,\quad \sum_{c\in C}\pi_c=1,\quad \pi_c\text{ numeric value }=\mathrm{TBD}.
\]

**Crucial:** \(\pi_{CY1},\ldots,\pi_{CY5}\) are **not necessarily equal to each other**. Synthetic value 0.2 in R02/R03/R04 is never a productive parameter. Project decision D4 demands canonical UTC-indexed intervals with explicit duration \(\Delta t\) and unit/dimensional lineage; DST/leap/missing-hour rules still MD-12-TBD. O26 §3.7 instead describes three other year-specific weather cases, which are **preserved as source facts**, not silently treated as a 5-case approved method.

### 3.2 Stochastic optimisation and physical network

For each independent horizon \(y\):

\[
\min_{x_y,\{u_{y,c}\}_{c\in C}}
\ C_y^\mathrm{inv}(x_y) + \sum_{c\in C}\pi_c C_{y,c}^\mathrm{op}(x_y,u_{y,c}),
\]

where the *same* \(x_y\) participates in all five CY, and \(u_{y,c}\) may differ. Costs include the methodically described investment and weather-dependent operational/VoLL/ENS classes, but price-year/discount operators and stage accounting are **MD-02/07 TBD**. Do not invent a cost formula or use robust min-max/CVaR without a source requirement.

Electric injections obey conservation in MW with explicit MW×h→MWh, while existing/reduced physical network branches obey DC-KCL/KVL/mesh physics including calibrated impedance/no-load/PST/HVDC effects. By contrast, **all transmission-expansion candidates** are modelled as **controllable DC market links with directional NTC effects**, even if their candidate physical technology is AC (O26 §4.5.2). This distinction is a *method-level invariant*, not a tool-format option.

Stages: S1 LP over eligible **real** on-/offshore transmission, S2 LP over residual real + conceptual onshore + theoretical offshore with correct S1 carry-forward **TBD_OWNER**, S3 separate endogenous storage only in 2040/2050. LF primary expansion retains DC-mesh while internal transfer ratings are not binding; internal-network dispatch with/without LF portfolio is separate; OPF expansion **only optional**, capped by LF portfolio if enabled. H2 network investment is exogenous, whereas coupled electric/H2 operations, hydro, DSR, storage and frozen pre-expansion H2-load sensitivity carry their own verified constraints/lineage.

### 3.3 Network reduction vs mere aggregation

P05 clustering must have traceable, connected zone partitions and congestion/flow rationale; P06 must provide six method classes: (1) no-load/reference flows; (2) mesh relations; (3) HVDC impacts; (4) capacities (four seasonal/directional values per relevant link); (5) equivalent impedances; (6) PST impacts. Preserve detailed-grid reference, PTDF/LODF/N-1 behavior and quality evidence. **An exact sum of injection/cut flows is necessary but insufficient** for electric equivalence. Actual detailed 2025 grid, formal contingency cases and RMSE acceptance TBD; O26's 102 zones are version-specific source facts, not an all-time hard-coded rule.

### 3.4 Data and output contract

The R03 \`SourceRelease → SourceArtifact → DataObjectDefinition → DataInstance → TransformationExecution → ModelInputBundle → ModelRunResult → OutputDefinition/PublishedNeed\` chain supplies the **verifiable lifecycle**. It must distinguish external artifacts, preprocessed data, model inputs, raw solver outputs, postprocessed metrics and genuine **identified needs**. Every real instance requires actual data freeze/version, provenance, units, study/CY/UTC/zone/carrier keys and a real original-file hash where file integrity is claimed. Project-, corridor-, node- and market-zone IDs must be related by **controlled spatial crosswalks**, not assumed interchangeable.

No unapproved KPI formula, tiny-investment cutoff, offshore routing factor, discount period or output mapping may be replaced by a tool default. A need is not an officially authorised construction/project decision. In multiple-optimum cases, objective equivalence and physical/KPI invariants must be distinguished from exact per-candidate portfolio identity.

## 4. Unified evidence semantics — independent of a specific tool

**Six orthogonal V-dimensions** from R04:
- \`V1 DATA\`: schema, original source manifest/release, axes and units.
- \`V2 SEMANTIC\`: identity, asset meaning, transformations, conserved quantities, optional/mandatory applicability.
- \`V3 MATHEMATICAL\`: source-grounded generated objective, constraints, variable domains, nonanticipativity, KCL/KVL, stages and transformations.
- \`V4 NUMERICAL\`: independent primal/dual/optimality/feasibility and objective residual reconstruction on an instance.
- \`V5 RESULTS\`: raw outputs, KPI formula/aggregation/version and reproducible metric recomputation.
- \`V6 EVIDENCE\`: actual execution, artifact hashes, scope, test outcome, independent review, decision/provenance.

**D0–D4** from R04 are *risk-proportionate test depths*, not the same thing as V1–V6. E01–E08 are *evidence ports*, not layers, and R02 A/B are *contract architecture prototypes*, not two tools.

Exactly six scoped **test** statuses proposed by R04: \`PASS | FAIL | BLOCKED | UNSUPPORTED | NOT_EXECUTED | NOT_APPLICABLE\`, always with a \`fixture_kind\` and provenance. \`NOT_APPLICABLE\` requires a proven false conditional antecedent (e.g. P15 OPF not selected) and cannot hide missing mandatory capabilities. Source/data qualification status, semantic review status, overall conformance claim and G1 are **separate fields**; do not flatten them into a successful test status.

A defensible **FULL** conformance claim (future, not now) requires all applicable mandatory SR/contract obligations to be validated with acknowledged oracles, release-specific inputs, independently checkable native model/solver and KPI evidence, and qualified reviewers. Agreement between two tools alone does not prove soundness, especially if they share the same misconstrued assumption.

### 4.1 Proposed evidence record: logical example, **not a schema or execution report**

~~~text
ResearchObligation:
  requirement_ref: MA01-SR-029
  source_ref: O26 §3.1.1 [CONSULTATION_DRAFT] + project_decision:D2 [RESEARCH]
  scenario_scope: y∈{2035,2040,2050}; CY1..CY5; shared symbolic w_c
  scientific_semantics: M01 (one x_y; weighted recourse and cost once)
  language_capabilities: crosswalk LR IDs from ML-R02
  data_dependencies: B01-Dxxx from integrated requirement crosswalk
  transform_dependencies: MLR03-Txx-yy (proposed, not owner confirmed)
  verification_need: MA01-VN-029
  test_id: R04-T-SR-029
  evidence: E04 generated constraints; E05 numerical witness; E08 ledger
  test_status: NOT_EXECUTED
  source_authority: AUTHORITY_UNCONFIRMED
  numerical_oracle: TBD_OWNER
  independent_signoff: NOT_OBTAINED
  gate_G1: BLOCKED
~~~

This is deliberately **not** a normative JSON/YAML/ReqIF/SysML schema. It is a capability-independent representation of what later formal syntax must carry.

## 5. Language/architecture disposition — retain a controlled experiment

**No winner declared.** R02 evaluated 15 candidate approaches × 12 generic criteria and built (A) a modular registry with five profiles and (B) an integrated typed semantic metamodel; a federated view C remains conceptual. A and B both structurally handled synthetic constraints and fail-closed mutations, but neither is a complete IoSN semantic executable model or certified standard parser.

- **A:** favorable research hypothesis if Input/Process/Math/Output/Verification have different owner/version cycles and a verified cross-profile closure can be maintained; cost is registry governance and version-tuple consistency.
- **B:** favorable research hypothesis if a coherent typed semantic core and fewer cross-profile invalid mappings dominate; cost is semantic evolution and complex schema migrations.
- **C:** standard/federated views may be useful for cross-tool interoperability, but introduce round-trip/mapping-loss risks and a second source-of-truth unless a single semantic authority is preserved.

The *core contract role* must be agreed before selecting any of SysML v2, ReqIF, LinkML, JSON Schema, SHACL, GEMS, CESM, INES, SiennaSchemas, mathspec or JSON/YAML. GEMS etc. may help represent an energy model; they do **not** automatically enforce method input transformations, numerical oracles, version authority and outputs. Neither full model translation nor 1:1 algebraic form is a general requirement.

## 6. Normative/non-normative and truth-status firewall

| Layer | Can be prepared under G1=BLOCKED? | Can be claimed as approved today? |
|---|---|---|
| Requirements/process/equation **research** specification | **Yes** | **No** |
| Language capability criteria, A/B/C and synthetic grammar/schema prototypes | **Yes** | **No** |
| Data/transform/output **research** contracts, mock oracles | **Yes** | **No** |
| Synthetic fixture arithmetic and negative mutation suites | **Yes**, with scope label | **No** to IoSN tool conformance |
| Actual original source-data qualification / owner method release | **No**, deferred by project decision | **No** |
| Two independent production tool implementations and benchmark certification | **Not performed here**; future readiness design only | **No** |
| Normative requirements language / binding architecture ADR | **Not decided here** | **No** |
| Gate G1 approval | Not part of ML-R00 | **No; BLOCKED** |

## 7. Integrated research acceptance criteria (not G1)

A subsequent **research** consolidation may be considered structurally ready when:
- 48 MA01-SR IDs and all 18 P IDs have exact cross-workstream joins, including M, LR, data and test bindings;
- 20 process-only data objects are explicitly preserved as unmapped-to-SR exceptions, **not dropped**;
- five CY profile and UTC/units decisions are correctly classified under D2/D4 with numerically undefined real weights;
- historical sources and draft-vs-project deviations remain tagged and never falsely elevated;
- all 21 MD/CL retain unchanged open status;
- all synthetic tests and any executions carry separate scope and authority statuses;
- architectural options A/B/C remain exploratory until an evidence-backed controlled decision.

These are **documentary/research checks**, **not** a reason to change Gate G1.

## 8. Trace and source anchors

Primary artifacts in this combined research snapshot:

- R01: [scientific_methodology_specification.md](../ML_R01_methodology/scientific_methodology_specification.md), [mathematical_obligations.md](../ML_R01_methodology/mathematical_obligations.md), [source_and_assumption_traceability.csv](../ML_R01_methodology/source_and_assumption_traceability.csv).
- R02: [language_requirements_specification.md](../ML_R02_language_architecture/language_requirements_specification.md), [contract_architecture_alternatives.md](../ML_R02_language_architecture/contract_architecture_alternatives.md), [comparative_evaluation.md](../ML_R02_language_architecture/comparative_evaluation.md).
- R03: [iosn_data_semantic_model.md](../ML_R03_data_process_contracts/iosn_data_semantic_model.md), [input_contract_catalogue.csv](../ML_R03_data_process_contracts/input_contract_catalogue.csv), [process_transformation_matrix.csv](../ML_R03_data_process_contracts/process_transformation_matrix.csv).
- R04: [verification_architecture.md](../ML_R04_verification/verification_architecture.md), [requirements_verification_matrix.csv](../ML_R04_verification/requirements_verification_matrix.csv), [test_catalogue.csv](../ML_R04_verification/test_catalogue.csv), [future_multi_tool_pilot_requirements.md](../ML_R04_verification/future_multi_tool_pilot_requirements.md).

**Status at handoff:** scientific integration **documented, not approved**; D2/D4 terminology reconciled **at the integration layer only**; no method/owner/data/tool certificate. \`G1=BLOCKED\`.
