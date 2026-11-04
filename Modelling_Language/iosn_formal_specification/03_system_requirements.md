# 03 — IoSN System Requirements Specification (SyRS)

**Status:** Proposed engineering derivation, **not** approved ENTSO-E SyRS. Source [O26] [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf). The **MR** statements are faithful *paraphrases* of O26 obligations, not copied quotations; **SR** statements are independently derived *system-level* requirements. All `SHALL` clauses are contractual candidates only after source approval. Conformance is unknown until testing.

## Levels / modelling doctrine
- **L1 — MR:** direct methodology-level obligations with section trace.
- **L2 — SR:** implementation-neutral, verifiable system requirements derived from MR and source.
- **L3 — FS:** machine-interpretable schema and behavioral/mathematical method profile; see 04, 08 and `poc/`.
- **L4 — VC:** verification cases and evidence; see 09.

### Requirements Catalogue
#### MR-001 — Use 2035, 2040 and 2050 as separate studied planning horizons.
|Attribute|Value|
|---|---|
|Requirement ID|MR-001|
|Methodology Source|O26 §3.1.1, §3.2|
|Requirement Level|Stakeholder|
|Requirement Type|Constraint|
|Requirement Statement|Use 2035, 2040 and 2050 as separate studied planning horizons.|
|Rationale|Planning results are horizon-specific.|
|Inputs|scenario inputs|
|Outputs|year-specific need outputs|
|Mandatory / Optional|mandatory|
|Implementation Freedom|Internal storage/solvers|
|Verification Method|inspection|
|Acceptance Criteria|Study manifest uses exactly the study horizons applicable to the declared report|
|Formalisation Feasibility|full|
|Open Issues|MD-01|

#### MR-002 — The published 2026 study uses the three selected weighted weather scenarios per horizon.
|Attribute|Value|
|---|---|
|Requirement ID|MR-002|
|Methodology Source|O26 §3.7|
|Requirement Level|Stakeholder|
|Requirement Type|Method|
|Requirement Statement|The published 2026 study uses the three selected weighted weather scenarios per horizon.|
|Rationale|Weather probabilities enter expansion study.|
|Inputs|PECD weather set|
|Outputs|weighted scenario profile|
|Mandatory / Optional|mandatory|
|Implementation Freedom|Operational export representation|
|Verification Method|test|
|Acceptance Criteria|Exact published ID/weight tuples for stated study version|
|Formalisation Feasibility|full for fixed output; partial for selection algorithm|
|Open Issues|MD-02|

#### MR-003 — Expansion investment variables are common to all weather scenarios in one horizon.
|Attribute|Value|
|---|---|
|Requirement ID|MR-003|
|Methodology Source|O26 §3.1.1 pp.12–13|
|Requirement Level|Stakeholder|
|Requirement Type|Method|
|Requirement Statement|Expansion investment variables are common to all weather scenarios in one horizon.|
|Rationale|Non-anticipativity prevents weather-specific builds.|
|Inputs|weighted scenarios|
|Outputs|investment portfolio|
|Mandatory / Optional|mandatory|
|Implementation Freedom|Variable implementation|
|Verification Method|analysis + test|
|Acceptance Criteria|For each candidate and horizon x has no weather-specific values / values equal|
|Formalisation Feasibility|partial|
|Open Issues|objective/solver evidence|

#### MR-004 — The investment model has two LP stages with distinct candidate sets.
|Attribute|Value|
|---|---|
|Requirement ID|MR-004|
|Methodology Source|O26 §§3.1.1,3.10|
|Requirement Level|Stakeholder|
|Requirement Type|Method|
|Requirement Statement|The investment model has two LP stages with distinct candidate sets.|
|Rationale|Candidate admissibility is staged.|
|Inputs|candidate classes|
|Outputs|stage-specific expansion|
|Mandatory / Optional|mandatory|
|Implementation Freedom|LP encoding|
|Verification Method|inspection + test|
|Acceptance Criteria|Stage 1 admits real candidates; stage 2 permitted residual and conceptual/offshore classes|
|Formalisation Feasibility|partial|
|Open Issues|MD-04|

#### MR-005 — The LF expansion and optional additional internal-constraint studies have distinct roles.
|Attribute|Value|
|---|---|
|Requirement ID|MR-005|
|Methodology Source|O26 §3.9|
|Requirement Level|Stakeholder|
|Requirement Type|Method|
|Requirement Statement|The LF expansion and optional additional internal-constraint studies have distinct roles.|
|Rationale|Avoid replacing baseline silently.|
|Inputs|network constraints|
|Outputs|LF portfolio and optional studies|
|Mandatory / Optional|mandatory distinction|
|Implementation Freedom|OPF algorithms in optional path|
|Verification Method|inspection|
|Acceptance Criteria|Baseline run marked LF and never substituted by an optional OPF run|
|Formalisation Feasibility|full at manifest level|
|Open Issues|MD-07|

#### MR-006 — The described IoSN expansion includes electricity/H2 coupling; H2 network investment is not part of the stated expansion decisions.
|Attribute|Value|
|---|---|
|Requirement ID|MR-006|
|Methodology Source|O26 §§3.3,3.6|
|Requirement Level|Stakeholder|
|Requirement Type|Scope|
|Requirement Statement|The described IoSN expansion includes electricity/H2 coupling; H2 network investment is not part of the stated expansion decisions.|
|Rationale|Respect sector and investment scope.|
|Inputs|H2 topology/conversions|
|Outputs|joint operation and investments|
|Mandatory / Optional|mandatory within scope|
|Implementation Freedom|internal commodity/port schema|
|Verification Method|analysis|
|Acceptance Criteria|Evidence of conversion and H2 dispatch; no illegal H2 network expansion|
|Formalisation Feasibility|partial|
|Open Issues|hydrogen constraint details|

#### SR-001 — The implementation shall identify study horizons, scenarios and authoritative source versions by stable identifiers.
|Attribute|Value|
|---|---|
|Requirement ID|SR-001|
|Methodology Source|O26 §§3.2,4.1; D|
|Requirement Level|System|
|Requirement Type|Data|
|Requirement Statement|The implementation shall identify study horizons, scenarios and authoritative source versions by stable identifiers.|
|Rationale|Prevent mixing studies and databases.|
|Inputs|PEMMDB, scenario metadata|
|Outputs|study_manifest|
|Mandatory / Optional|mandatory|
|Implementation Freedom|identifier encoding free|
|Verification Method|schema + inspection|
|Acceptance Criteria|all study/run/source IDs supplied and unique|
|Formalisation Feasibility|full|
|Open Issues|MD-01|

#### SR-002 — The system shall keep distinct model and result identities for each target horizon.
|Attribute|Value|
|---|---|
|Requirement ID|SR-002|
|Methodology Source|O26 §3.1.1, §3.2; D|
|Requirement Level|System|
|Requirement Type|Constraint|
|Requirement Statement|The system shall keep distinct model and result identities for each target horizon.|
|Rationale|Separate optimisations.|
|Inputs|study_manifest|
|Outputs|horizon-scoped outputs|
|Mandatory / Optional|mandatory|
|Implementation Freedom|pipeline layout free|
|Verification Method|structure test|
|Acceptance Criteria|no output with unbound target year|
|Formalisation Feasibility|full|
|Open Issues|none|

#### SR-003 — The system shall preserve unit, time-index, weather-source and spatial reference information for imported series.
|Attribute|Value|
|---|---|
|Requirement ID|SR-003|
|Methodology Source|O26 §§3.7,4.1–4.4; D|
|Requirement Level|System|
|Requirement Type|Data|
|Requirement Statement|The system shall preserve unit, time-index, weather-source and spatial reference information for imported series.|
|Rationale|Comparability and transformations.|
|Inputs|PECD, PEMMDB|
|Outputs|time_series_manifest|
|Mandatory / Optional|mandatory|
|Implementation Freedom|storage encoding free|
|Verification Method|schema + cross-reference|
|Acceptance Criteria|all series have unit, clock/calendar, source and spatial mapping|
|Formalisation Feasibility|partial|
|Open Issues|MD-02|

#### SR-004 — The system shall produce the selected weather-scenario manifest per target year with the O26 §3.7 weather IDs and weights.
|Attribute|Value|
|---|---|
|Requirement ID|SR-004|
|Methodology Source|O26 §3.7; D|
|Requirement Level|System|
|Requirement Type|Functional|
|Requirement Statement|The system shall produce the selected weather-scenario manifest per target year with the O26 §3.7 weather IDs and weights.|
|Rationale|Published fixed outcome.|
|Inputs|PECD scenario register|
|Outputs|selected_weather_manifest|
|Mandatory / Optional|mandatory for O26 version|
|Implementation Freedom|selection-library implementation free|
|Verification Method|data+semantic test|
|Acceptance Criteria|exact IDs with [0.24,0.43,0.33] etc|
|Formalisation Feasibility|full for manifest|
|Open Issues|MD-01|

#### SR-005 — If claiming to implement weather-year selection, the system shall provide reproducible selection evidence, including normative preprocessing and clustering decisions.
|Attribute|Value|
|---|---|
|Requirement ID|SR-005|
|Methodology Source|O26 Annex 6.3; D|
|Requirement Level|System|
|Requirement Type|Verification|
|Requirement Statement|If claiming to implement weather-year selection, the system shall provide reproducible selection evidence, including normative preprocessing and clustering decisions.|
|Rationale|Distinguish chosen outcome from algorithm.|
|Inputs|candidate weather features|
|Outputs|selection_evidence|
|Mandatory / Optional|conditional on algorithm-conformance claim|
|Implementation Freedom|library free within signed method profile|
|Verification Method|analysis and reference reproduction|
|Acceptance Criteria|independent reference fixture yields expected candidates/weights once approved|
|Formalisation Feasibility|partial|
|Open Issues|MD-02|

#### SR-006 — The system shall align scenario-indexed time series before use and shall report time transformations and missing-data handling.
|Attribute|Value|
|---|---|
|Requirement ID|SR-006|
|Methodology Source|O26 §§3.7,4.1–4.4; D|
|Requirement Level|System|
|Requirement Type|Data|
|Requirement Statement|The system shall align scenario-indexed time series before use and shall report time transformations and missing-data handling.|
|Rationale|Avoid silent time drift.|
|Inputs|time-series inputs|
|Outputs|aligned input set + mapping log|
|Mandatory / Optional|mandatory|
|Implementation Freedom|ETL language free|
|Verification Method|invariant/schema test|
|Acceptance Criteria|consistent timestamps/scenario keys and declared transformations|
|Formalisation Feasibility|partial|
|Open Issues|hourly convention and allowed gaps|

#### SR-007 — The system shall represent published zonal network reduction outputs and their mapping to the detailed electricity network.
|Attribute|Value|
|---|---|
|Requirement ID|SR-007|
|Methodology Source|O26 §§3.8.1–3.8.4; D|
|Requirement Level|System|
|Requirement Type|Functional|
|Requirement Statement|The system shall represent published zonal network reduction outputs and their mapping to the detailed electricity network.|
|Rationale|Spatial model reproducibility.|
|Inputs|detailed grid, flows|
|Outputs|zonal_grid, busmap|
|Mandatory / Optional|mandatory|
|Implementation Freedom|graph and algorithm storage free|
|Verification Method|schema + analysis|
|Acceptance Criteria|every required detailed bus maps to a defined zone|
|Formalisation Feasibility|partial|
|Open Issues|MD-03|

#### SR-008 — The system shall preserve the required network-reduction properties, including equivalent electrical behaviour and seasonal directional transfer limits as specified by the chosen method profile.
|Attribute|Value|
|---|---|
|Requirement ID|SR-008|
|Methodology Source|O26 §3.8, Annex 6.1; D|
|Requirement Level|System|
|Requirement Type|Constraint|
|Requirement Statement|The system shall preserve the required network-reduction properties, including equivalent electrical behaviour and seasonal directional transfer limits as specified by the chosen method profile.|
|Rationale|Method-quality conditions.|
|Inputs|detailed and zonal grids|
|Outputs|network reduction evidence|
|Mandatory / Optional|mandatory for scope|
|Implementation Freedom|solver/technique free|
|Verification Method|math + reference tests|
|Acceptance Criteria|approved profile invariants and thresholds pass, else fail/unresolved|
|Formalisation Feasibility|partial|
|Open Issues|MD-03|

#### SR-009 — The system shall reconcile zonal technology capacities and time series with network and climate source mappings.
|Attribute|Value|
|---|---|
|Requirement ID|SR-009|
|Methodology Source|O26 §3.8.4; D|
|Requirement Level|System|
|Requirement Type|Data|
|Requirement Statement|The system shall reconcile zonal technology capacities and time series with network and climate source mappings.|
|Rationale|Consistent asset placement.|
|Inputs|network and PECD data|
|Outputs|zonal asset map|
|Mandatory / Optional|mandatory|
|Implementation Freedom|ETL technology free|
|Verification Method|aggregation test|
|Acceptance Criteria|approved capacity conservation and source lineage tests|
|Formalisation Feasibility|partial|
|Open Issues|mapping unit thresholds|

#### SR-010 — The system shall express electricity, hydrogen, coupled conversion and required energy balances as domain semantics independent of tool object names.
|Attribute|Value|
|---|---|
|Requirement ID|SR-010|
|Methodology Source|O26 §§3.3,3.6; D|
|Requirement Level|System|
|Requirement Type|Functional|
|Requirement Statement|The system shall express electricity, hydrogen, coupled conversion and required energy balances as domain semantics independent of tool object names.|
|Rationale|Sector-coupled feasibility.|
|Inputs|zonal electricity/H2|
|Outputs|model_semantics_manifest|
|Mandatory / Optional|mandatory within study|
|Implementation Freedom|component decomposition free|
|Verification Method|static + residual test|
|Acceptance Criteria|ports, carriers, balances and conversion declared and testable|
|Formalisation Feasibility|partial|
|Open Issues|MD-07|

#### SR-011 — The system shall restrict expansion decisions to the methodologically eligible investment asset classes, excluding hydrogen network capacity expansion.
|Attribute|Value|
|---|---|
|Requirement ID|SR-011|
|Methodology Source|O26 §§3.6,3.10,4.5; D|
|Requirement Level|System|
|Requirement Type|Constraint|
|Requirement Statement|The system shall restrict expansion decisions to the methodologically eligible investment asset classes, excluding hydrogen network capacity expansion.|
|Rationale|Avoid expanded scope.|
|Inputs|eligible candidate register|
|Outputs|candidate bounds/portfolio|
|Mandatory / Optional|mandatory|
|Implementation Freedom|internal variable naming free|
|Verification Method|structure + model test|
|Acceptance Criteria|no prohibited capacity variable contributes to expansion decision|
|Formalisation Feasibility|partial|
|Open Issues|MD-04|

#### SR-012 — The system shall register candidate identities, class, location, maximum capacity, and required economic parameters with units and vintage.
|Attribute|Value|
|---|---|
|Requirement ID|SR-012|
|Methodology Source|O26 §§4.5–4.6; D|
|Requirement Level|System|
|Requirement Type|Data|
|Requirement Statement|The system shall register candidate identities, class, location, maximum capacity, and required economic parameters with units and vintage.|
|Rationale|Well-defined investments.|
|Inputs|candidate/cost database|
|Outputs|candidate manifest|
|Mandatory / Optional|mandatory|
|Implementation Freedom|schema implementation free|
|Verification Method|schema + semantic test|
|Acceptance Criteria|required fields present, finite caps, dimensions checked|
|Formalisation Feasibility|partial|
|Open Issues|broken reference MD-05|

#### SR-013 — The system shall enforce storage expansion horizon restrictions and other published candidate eligibility rules.
|Attribute|Value|
|---|---|
|Requirement ID|SR-013|
|Methodology Source|O26 §§3.10,4.5.1; D|
|Requirement Level|System|
|Requirement Type|Constraint|
|Requirement Statement|The system shall enforce storage expansion horizon restrictions and other published candidate eligibility rules.|
|Rationale|Avoid unapproved builds.|
|Inputs|storage candidates|
|Outputs|allowed investment variables|
|Mandatory / Optional|mandatory|
|Implementation Freedom|constraint encoding free|
|Verification Method|LP microtests|
|Acceptance Criteria|storage expansion excluded for 2035 when the source rule applies|
|Formalisation Feasibility|partial|
|Open Issues|candidate state machine|

#### SR-014 — The system shall solve the indicated two-stage linear expansion process separately for each studied horizon.
|Attribute|Value|
|---|---|
|Requirement ID|SR-014|
|Methodology Source|O26 §§3.1.1,3.10; D|
|Requirement Level|System|
|Requirement Type|Method|
|Requirement Statement|The system shall solve the indicated two-stage linear expansion process separately for each studied horizon.|
|Rationale|Process compliance.|
|Inputs|stage candidates, market inputs|
|Outputs|stage results|
|Mandatory / Optional|mandatory|
|Implementation Freedom|tool, solver and numerical formulation free within LP requirement|
|Verification Method|stage test + evidence|
|Acceptance Criteria|both stages recorded with eligible sets and valid terminal statuses|
|Formalisation Feasibility|partial|
|Open Issues|MD-04|

#### SR-015 — The system shall constrain each candidate investment decision to one weather-independent value per target horizon.
|Attribute|Value|
|---|---|
|Requirement ID|SR-015|
|Methodology Source|O26 §3.1.1; D|
|Requirement Level|System|
|Requirement Type|Constraint|
|Requirement Statement|The system shall constrain each candidate investment decision to one weather-independent value per target horizon.|
|Rationale|Non-anticipativity.|
|Inputs|weather scenarios|
|Outputs|investment decisions|
|Mandatory / Optional|mandatory|
|Implementation Freedom|variable indexing free|
|Verification Method|algebraic + model test|
|Acceptance Criteria|x_i equal/one instance across all represented weather scenarios|
|Formalisation Feasibility|partial|
|Open Issues|engine proof mechanism|

#### SR-016 — The expansion objective and physical operating constraints shall implement published cost weighting, nodal power balance, admissible DC-flow and investment bounds.
|Attribute|Value|
|---|---|
|Requirement ID|SR-016|
|Methodology Source|O26 §3.1.1; D|
|Requirement Level|System|
|Requirement Type|Constraint|
|Requirement Statement|The expansion objective and physical operating constraints shall implement published cost weighting, nodal power balance, admissible DC-flow and investment bounds.|
|Rationale|Constrained minimum cost.|
|Inputs|network, demand, costs, scenarios|
|Outputs|primal model and results|
|Mandatory / Optional|mandatory|
|Implementation Freedom|constraint generation and solver free; math class prescribed|
|Verification Method|symbolic inspection + reference test|
|Acceptance Criteria|zero unconstrained omissions; objective and residuals meet approved tolerances|
|Formalisation Feasibility|partial|
|Open Issues|method profile, numerical thresholds|

#### SR-017 — The implementation shall distinguish mandatory LF portfolio runs from subsequent internal-constraint dispatch and optional OPF expansion studies.
|Attribute|Value|
|---|---|
|Requirement ID|SR-017|
|Methodology Source|O26 §3.9; D|
|Requirement Level|System|
|Requirement Type|Processing|
|Requirement Statement|The implementation shall distinguish mandatory LF portfolio runs from subsequent internal-constraint dispatch and optional OPF expansion studies.|
|Rationale|Prevent methodological substitution.|
|Inputs|LF portfolio|
|Outputs|differentiated runs|
|Mandatory / Optional|mandatory separation; optional OPF|
|Implementation Freedom|tools and storage free|
|Verification Method|workflow state test|
|Acceptance Criteria|each result tagged mode and LF baseline protected|
|Formalisation Feasibility|full at metadata level|
|Open Issues|study-specific optionality|

#### SR-018 — The system shall output investment/need indicators with defined location, carrier, scenario/horizon, unit, meaning and calculation provenance.
|Attribute|Value|
|---|---|
|Requirement ID|SR-018|
|Methodology Source|O26 §§2.2,3.1.2,3.10; D|
|Requirement Level|System|
|Requirement Type|Output|
|Requirement Statement|The system shall output investment/need indicators with defined location, carrier, scenario/horizon, unit, meaning and calculation provenance.|
|Rationale|Interpretation and acceptance.|
|Inputs|validated model results|
|Outputs|needs results|
|Mandatory / Optional|mandatory|
|Implementation Freedom|report renderer free|
|Verification Method|schema + aggregation test|
|Acceptance Criteria|complete context and lineage; KPI equations declared|
|Formalisation Feasibility|partial|
|Open Issues|MD-06|

#### SR-019 — The implementation shall provide verifiable postprocessing definitions, filters and aggregation records for the published infrastructure-needs findings.
|Attribute|Value|
|---|---|
|Requirement ID|SR-019|
|Methodology Source|O26 §§2.2,3.1.2; D|
|Requirement Level|System|
|Requirement Type|Verification|
|Requirement Statement|The implementation shall provide verifiable postprocessing definitions, filters and aggregation records for the published infrastructure-needs findings.|
|Rationale|Reproducibility.|
|Inputs|raw model results|
|Outputs|needs table + lineage|
|Mandatory / Optional|mandatory as derived requirement|
|Implementation Freedom|ETL implementation free|
|Verification Method|independent recomputation|
|Acceptance Criteria|reference fixture reproduces reported KPI under approved formula|
|Formalisation Feasibility|partial|
|Open Issues|MD-06|

#### SR-020 — The system shall publish a typed evidence manifest for static, semantic and implemented-model verification statuses.
|Attribute|Value|
|---|---|
|Requirement ID|SR-020|
|Methodology Source|O26 §5.1; D|
|Requirement Level|System|
|Requirement Type|Verification|
|Requirement Statement|The system shall publish a typed evidence manifest for static, semantic and implemented-model verification statuses.|
|Rationale|Comparable sanity controls.|
|Inputs|all artifacts|
|Outputs|verification report|
|Mandatory / Optional|proposed mandatory for future contract|
|Implementation Freedom|CI product free|
|Verification Method|schema + negative tests|
|Acceptance Criteria|no requirement marked PASS without linked observed evidence|
|Formalisation Feasibility|full for reporting|
|Open Issues|governance sign-off|

#### SR-021 — Unresolved or ambiguous methodological clauses shall have an explicit issue ID and may not be silently converted to proprietary tool defaults.
|Attribute|Value|
|---|---|
|Requirement ID|SR-021|
|Methodology Source|O26 draft/§4.6; D|
|Requirement Level|System|
|Requirement Type|Governance|
|Requirement Statement|Unresolved or ambiguous methodological clauses shall have an explicit issue ID and may not be silently converted to proprietary tool defaults.|
|Rationale|Prevent divergent readings.|
|Inputs|source issues|
|Outputs|open-issues decisions|
|Mandatory / Optional|proposed mandatory|
|Implementation Freedom|issue tracker free|
|Verification Method|audit|
|Acceptance Criteria|unresolved normative requirement blocks full conformance claim|
|Formalisation Feasibility|full|
|Open Issues|MD-01–MD-07|

## Trace map and source boundaries
- [O26 §3.7] → MR-002 → SR-003/004/005 → LRC-02/03/05/10 → `poc/contract.json` → VC-01–VC-04 → `poc/verification_report.json`.
- [O26 §§3.1.1,3.10] → MR-003/004 → SR-012–016 → LRC-06/07/08/12 → UC-02 → VC-05–VC-08 (**proposed, not executed**).
- [O26 §§3.8–3.9] → MR-005 → SR-007/008/017 → LRC-04/06/07 → VC-09/10 (**proposed, not executed**).
- [O26 §§2.2,3.1.2] → SR-018/019 → LRC-09/10 → UC-03 → VC-11/12 (**proposed, not executed**).

## Contractual acceptance gate
Proposed requirements MUST **not** become official conformance claims until: version locked; methodological ambiguity resolved; applicable mandatory/conditional obligations signed; executable artifacts versioned; tool implementation evidence assessed; and independent test reports linked. A syntactically well-formed requirements database is not that proof.

## Notes on precise semantics
- If an obligation prescribes **behavior only**, require observable invariant/tests rather than component names.
- If the methodology prescribes an **optimization formulation class** (two-stage LP, DC flow, non-anticipativity), the formal method profile must constrain that class even if the engine representations differ.
- If an obligation prescribes an **explicit equation**, preserve its quantified indices, units, sign conventions and scenario probabilities; a prose approximation alone is insufficient.
- Numeric tolerances in independent test harnesses are **X engineering choices**, until formally adopted.
