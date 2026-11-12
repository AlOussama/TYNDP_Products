# ML-C01 — Canonical Semantic Vocabulary

**Version:** research-0.1, 12 November 2026. **Baseline:** ML-R00 PR #32, commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2. **Status:** NONNORMATIVE; AUTHORITY_UNCONFIRMED; G1=BLOCKED.

## 1. Canonical objects: meaning and anti-conflation

| Canonical type | Identity and scientific meaning | Must not be conflated with |
|---|---|---|
| SourceClause | Exact versioned source text, clause and source-kind label | Adopted authority; merely citing O26 does not grant approval |
| SourceAuthorityAssertion | Evidence of issuer, effective date, scope, original source release and official decision | Source availability, date, checksum or a CBA4 approval for another scope |
| ResearchProfile | Version tuple of source snapshot + project decisions + derived assertions + open MD/CL | Released methodology or productive model specification |
| GovernanceDecision | Versioned decision ID, competent issuer, scope, evidence, state and effective interval | Proposed interpretation or AI closure of a pending MD/CL |
| Requirement | One of exactly 48 unchanged active provisional MA01-SR L2 obligations | M01–M18, LR01–LR20, process, data objects or a new active SR |
| Process | P00–P17 scientific activity with triggers, inputs, outputs and dependencies | ETL-only transformation or mandated execution scheduler |
| DataObjectDefinition | One of B01-D001…B01-D087 data catalogue types | Actual original source-file payload, source release or instance |
| DataInstance | Versioned run- or source-specific realization of a DataObjectDefinition | Object type, hashless fixture or approved source |
| TransformationSpec | One of 38 MLR03-T proposed operations/edges; typed as DATA_TRANSFORM, MODEL_OPERATION, ANALYSIS, GOVERNANCE or VERIFICATION | Proven actual execution, mandatory ETL product or arbitrary new SR |
| TransformationExecution | Actual recorded execution of a versioned spec with referenced input/output instances | Proposal for producer/consumer mapping |
| MathematicalObligation | M01–M18 scientific invariant/formulation family with assumptions, scope, units and counterexamples | Adopted numeric threshold, an algebraically unique formula or a second L2 baseline |
| LanguageCapability | LR01–LR20 research-level expression/verification need | Normative language feature or decided A/B/C architecture |
| VerificationCase | MA01-VN test need, R04-T-SR test proposal, or separately identified C01–C10 fixture | Executed native tool verification or approved oracle |
| Evidence | Immutable claim-scoped execution/source/oracle/observation/reviewer record | Solver status alone, synthetic PASS, method adoption or Gate G1 |
| SystemNeed | Versioned, derived need/opportunity with geography, carrier, direction, year, KPI/formula and provenance | ApprovedProject, permitting, funding or construction approval |
| ApprovedProject | Separately authorised project lifecycle state evidenced by competent owner | Any positive optimized need |
| ModelMode | Explicit LF expansion, internal-constrained dispatch comparison, frozen-H2 sensitivity or selected optional OPF | Interchangeable procedures with the same physics |
| PhysicalDCBranch | Existing/reduced *physical* line with DC power-flow approximation, network mesh/KVL and KCL | Free-flowing controllable NTC transport link |
| ControllableDCMarketLink | Candidate expansion decision modeled as steerable market link with directional NTC effect, independent of candidate AC/DC physical technology | New meshed physical branch just because candidate technology is AC |
| ExternalWeatherCase | Externally selected CY1–CY5 and source-specific profile mappings | Weather-year selection algorithm, source calendar hour, constant weight |

## 2. Namespaces and identity invariant

Canonical references retain their **original ID and source namespace**:

| Fully qualified reference | Meaning |
|---|---|
| project_decision:D2 | Five externally selected CY1–CY5; same case-indexed weight vector in 2035, 2040, 2050; no numeric weights |
| project_decision:D4 | UTC and units |
| test_depth:D4 | Deep equivalence verification (ML-R04), *not* project_decision:D4 |
| project_decision:D5-A1 | Risk-based verification decision; not proposed risk tier A |
| project_decision:D6-A | Independent tool implementations under shared semantics; not architecture A |
| source:O26:2026-02-25:§3.7 | 2026 consultation method weather clause, CONSULTATION_ONLY |
| requirement:MA01-SR-029 | Active provisional SR on scenario-independent investment |
| process:P10 | Stage-1 transmission LP process |
| math:M01; language:LR03 | Scientific obligation vs language capability |
| data_object:B01-D072 | Data-object definition; source/producer status retained separately |
| verification_need:MA01-VN-029 | Original verification need |
| verification_test:R04-T-SR-029 | R04 planned test |
| fixture:R04-C01 | Bounded synthetic example; never native IoSN evidence |
| md:MD-12; clarification:MA02-CL-001 | Unresolved owner decision/clarification |

A semantic ID is unique only inside its namespace and revision/scope. Distinguish detailed bus, physical node, electrical zone, H2 zone, market area, offshore hub, asset, candidate, corridor, project, source file, release and run. Many-to-many identity crosswalks require an explicit rule, provenance, mapping revision, applicable geography, carrier, aggregation direction and treatment of unmapped identities. Equal strings do not establish equal entities.

**Baseline set:** 48 active MA01-SR (001–050 excluding 012 and 049); the corresponding excluded MR-012/MR-049 describe upstream weather selection, which must not be reintroduced. R03 has 87 original data types, of which 67 have proposed direct SR links (93 proposed pairs), and 20 are *process-only*. No process-only object may be silently promoted to a new SR or deleted.

## 3. Typed relations (non-normative interface)

| Relation | Source → target | Semantic constraint |
|---|---|---|
| DERIVED_FROM | Requirement/MathematicalObligation → SourceClause or GovernanceDecision | Provenance and validity scope carried; reference ≠ approval |
| REFINES | MathematicalObligation → Requirement | Does not mutate source SR statement; SCI_DERIVED or ILLUSTRATIVE explicit |
| SCOPES | ResearchProfile → Requirement/Process/Decision | One declared profile version, open conflicts retained |
| REQUIRES_CAPABILITY | Requirement → LanguageCapability | Research hypothesis, not newly authorized L2 |
| PARTICIPATES_IN | Requirement → Process | Many-to-many; P00 can legitimately lack a directly mapped active SR |
| DEFINES | DataObjectDefinition → DataInstance | Each instance has exactly one definition; potentially multiple instances per object |
| CONSUMES / PRODUCES | Process/TransformationSpec → DataObjectDefinition | Intended dependency, not a run |
| REALIZED_BY | TransformationSpec → TransformationExecution | 0..n executions; 0 means not executed |
| DERIVED_FROM_INPUT | DataInstance → SourceArtifact/DataInstance | Exact source release, transformation and version, no fabricated original hash |
| IMPLEMENTS | ToolRealization → Requirement/MathObligation | Intended implementation mapping, not conformance |
| TESTS / HAS_ORACLE | VerificationCase → Requirement/MathObligation / Oracle | Independent accepted oracle state explicitly recorded |
| EVIDENCES | Evidence → TestAssertion + Run + Scope | Specific observation, validation class, hash and reviewer |
| BLOCKED_BY | Requirement/Metric/Claim → pending MD/CL | 21 owner items stay open until real competent decision |
| PUBLISHES_AS | OutputDefinition → SystemNeed | Derivation and KPI defined; never imply ApprovedProject |
| APPROVED_BY | Source/Decision/Data/Claim → signed governance record | No approval edge from schema validator or AI-generated draft |

**Reference completeness != scientific verification.** A fully resolved 48-row crosswalk is structural evidence only; original B01-D→SR producer assignments, the 20 process-only dispositions and 38 transformations remain proposals until appropriately reviewed.

## 4. Physical, temporal and output semantics

**D2 / probability:** For separate study years Y={2035,2040,2050} and C={CY1,…,CY5}, use one symbolic weight w[c] per c, identical across Y: w[y,c]=w[c]. D2 does **not** require w[CY1]=…=w[CY5]. Nonnegativity and sum_c w[c]=1 are scientific conventions for probability-weighted expectation subject to later source/normalization confirmation; numeric values, original case identities and tolerances remain TBD. An equal 0.2 vector is only a marked synthetic fixture. Selection and reconstruction of weather years are upstream.

**Optimization:** In each year y, x[y,k] is common to all five cases, whereas operation u[y,c,t] varies; investment cost is counted once in a scoped objective I[y](x)+sum_c w[c] Q[y,c](x,u). No automatic cross-year endogenous coupling, maximin/CVaR or fivefold investment CAPEX. Cost/discount, the Stage-1→2 residual mapping and real hourly weighting need owner evidence.

**Network:** Reduced/existing branches obey physical DC mesh relations including equivalent impedance, no-load/reference flows, HVDC/PST effects and KCL/KVL. Candidate expansion uses *controllable market-link* dispatch and directional NTC effects, even for physically AC candidates. Six P06 network reduction categories: reference/no-load flows; mesh relations; HVDC effects; transfer capacities including four season×direction ratings; equivalent impedances; PST effects. Mere conservation is not PTDF/LODF/N−1 fidelity. The detailed network/quality oracle remains open.

**Process modes:** P10 first real-candidate transmission LP; P11 residual/conceptual/theoretical second LP with unresolved S1→S2 transfer (MD-07); P12 storage investment only 2040/2050. LF retains physical mesh relations but removes relevant binding *internal interzonal ratings*. P13 network-constrained dispatch comparison is separate; P14 freezes the *pre-expansion, time- and zone-resolved* H2 profile; P15 OPF is optional but its LF-portfolio cap becomes mandatory **if selected**. H2 transmission expansion is exogenous.

**D4:** Canonical half-open UTC intervals [start_utc,end_utc) and actual duration Δt; MW times Δt[h] produces MWh, not MW; hydrogen energy basis (LHV/HHV), directional sign, currency, price year and discount basis are explicit. Ambiguous DST, leap/missing-hour, time aggregation, numerical tolerance and calendar decisions are **MD-12 TBD**; mere UTC string format does not prove correct conversion. Original source provenance and transformation history are mandatory *when claiming* authentic release/production input.

**Results:** Raw solver records, postprocessed KPI objects, published SystemNeeds and externally authorized projects have distinct types and lifecycles. A missing KPI formula or small-expansion filter threshold is METRIC_UNDEFINED / OWNER_TBD, not a value computed using a preferred software default.

## 5. Obligation polarity and evidence

- REQUIRED: cannot be disabled for an applicable run; no complete PASS if capability missing, reference absent or required check unexecuted.
- CONDITIONAL: mandatory property when a *versioned, evidenced antecedent* is true. An unknown antecedent is BLOCKED.
- OPTIONAL: only choosing to execute the extension is optional. When OPF_SELECTED=true, SR-026's cap and mode restrictions are obligatory.
- NOT_APPLICABLE: per-test outcome requires proof the specific guard is false; disabling P15 never disables mandatory LF, P13 or P14.
- PASS: only an actually executed, scope-identified assertion with suitable oracle/evidence. Structure and fixture successes are separate technical facts and never general source/model/G1 PASS.

See [status ontology](status_and_applicability_ontology.md), [source applicability](source_authority_and_applicability_semantics.md), [D1–D6](decision_semantics_D1_D6.md), and [the original R00 crosswalk](../ML_R00_consolidation/integrated_requirement_traceability.csv).

**Research-only conclusion:** these terms and relations provide a consistent vocabulary for later contract representation; none chooses syntax, architecture A/B/C, solver, thresholds, owner approval or Gate G1.
