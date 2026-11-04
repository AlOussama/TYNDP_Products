# 02 — IoSN process analysis and Process Specification Matrix

## Evidence and classification
Source: [O26] 2026 consultation version, 25 Feb 2026, [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf). The steps **reconstruct** the published process, not an assertion that ENTSO-E uses exactly this software workflow. P04 and P12 include derived engineering tasks. Absent thresholds are marked OPEN rather than invented. Scenario-method source [OS] is linked in the README.

## Data and process dependencies

~~~mermaid
flowchart TD
  S[O26 / scenario methodology] --> P01[Study context P01]
  PECD[PECD weather] --> P02[Weather preparation P02]
  P01 --> P02 --> P03[Representative years P03] --> P04[Aligned time inputs P04]
  GRID[Detailed electrical grid] --> P05[Zoning and network reduction P05] --> P06[Zonal input mapping P06]
  P04 --> P06
  H2[Hydrogen scenario data] --> P07[Coupled system P07]
  P06 --> P07
  ECON[Candidates and costs] --> P08[Candidate/economics P08]
  P07 --> P09[Weighted 2-stage LP P09]
  P08 --> P09
  P09 --> P10[Internal constraint studies P10]
  P09 --> P11[Needs outputs P11]
  P10 --> P11
  P11 --> P12[Method evidence and acceptance P12]
~~~

## Process Specification Matrix

|Process ID / purpose|Method source|Inputs / mandatory properties|Rules and method constraints|Permissible implementation freedom|Outputs / output properties|Failure conditions|Acceptance / unresolved decisions|
|---|---|---|---|---|---|---|---|
|**P01** Study context, planning horizons and scenarios|[O26 §§2,3.2,4.1]|scenarios / target periods; 2035,2040,2050; scenario identity and database version|choose study slices and validate identity|2026 scenario assumptions are externally provided; choice of import technology free|study manifest; unique ids, target-year mapping, provenance|missing/unlicensed/version-mismatched assumptions|SR-001, SR-002; **OPEN:** unverified scenario dataset version|
|**P02** Weather source data preparation|[O26 §§3.7,4.2, Annex 6.3]|PECD weather and geo/time series; scenario, clock and spatial references; adequate candidate-year pool|assemble comparable source profiles; follow referenced scenario-method documents|storage/serialization and parallelization free|weather feature dataset; traceable PECD scenario codes / units / chronology|misaligned leap years, missing climate metadata|SR-003; **OPEN:** exact preparation parameter closure|
|**P03** Weather-year selection|[O26 §3.7, Annex 6.3]|prepared weather features; candidate scenario set, weights and target year|PCA, k-means and representative-year choices described; final 2026 IDs/weights explicit|choice of libraries free where methodology permits|three weighted scenarios per horizon; IDs and numerical weights as published; full algorithm evidence when requested|unmapped or duplicated scenario, weights invalid|SR-004, SR-005; **OPEN:** random seed, PCA rank, tie rules|
|**P04** Temporal preparation / disaggregation|[O26 §§3.1.1,3.7,4.1–4.4]|selected profiles, market inputs; consistent hourly index, units, scenario alignment|make weighted market/flow input profiles consistent across datasets|file layout and transport free; no invented aggregation method|time-dependent inputs; no silent time shifts, documented transformations|gaps, inconsistent units/time resolution|SR-006; **OPEN:** method mandates exact temporal aggregation? OPEN|
|**P05** Spatial zoning and network reduction|[O26 §3.8, Annex 6.1]|detailed grid, LF, overload results; busmap, line impedances, branch ratings, weather hours|identify critical lines, zone boundaries, equivalent impedances, seasonal directional capacities and N-1 considerations|implementation technique free within method bounds|zonal grid + mapping; provenance, physical/balance validation evidence|unmapped bus, invalid equivalence, violation of method rules|SR-007, SR-008; **OPEN:** termination and numeric convergence thresholds|
|**P06** Zonal input mapping|[O26 §3.8.4]|busmap, PEMMDB/PECD assets; source/target zones, technology and capacity|reconcile detailed-grid capacities and PECD profiles at zonal resolution|data tools free|zonal technology and demand dataset; preserved referenced quantities and units|lossy unapproved mapping|SR-009; **OPEN:** normalisation/rounding thresholds|
|**P07** Coupled system topology|[O26 §§3.3,3.6]|zonal electricity, H2 scenario data; electricity/H2 commodity semantics and ports|represent cross-sector conversion and H2 system dispatch, but no H2 network expansion in described case|model element types and internal topology free if obligations met|model manifest and balance definitions; carrier balance and permitted conversions|H2 expansion wrongly admitted; omitted conversion|SR-010, SR-011; **OPEN:** full H2 dispatch constraints not all prescribed|
|**P08** Investment candidates and economics|[O26 §§3.10,4.5–4.6]|real/conceptual/offshore and storage candidates; candidate class, units, caps, time horizon, CAPEX, O&M|separate admissible investments and constraints, storage timing restrictions|internal variable encoding free|candidate register and cost parameters; unique candidates, allowed horizon/type, bounded capacities|illegal candidate or missing bound|SR-012, SR-013; **OPEN:** ambiguous partial-candidate and cost defaults|
|**P09** Investment and operation LP|[O26 §§3.1.1,3.9–3.10]|P07/P08 model, three weighted weather sets; same investments over weather scenarios; power balance; model flow constraints|two-stage LP, LF setting for primary expansion, operating-cost objective weighted by weather|solver/variable layout free; equation class where prescribed not free|expansion solution, primal/dual or certificates; solve status, objective decomposition, constraint/equality residuals|infeasible run, scenario-dependent x, omitted restrictions|SR-014, SR-015, SR-016; **OPEN:** numerical tolerances & calibration conventions|
|**P10** Supplementary internal-constraint studies|[O26 §3.9]|expansion portfolio and detailed capacities; LF portfolio and internal grid study setup|dispatch with/without portfolio; optional OPF assessment distinguished explicitly|additional methods only as described|sensitivity dispatch outputs; result and mode provenance; no conflation with LF baseline|mode mislabeled|SR-017; **OPEN:** what optional studies become mandatory per study|
|**P11** Postprocess needs and outputs|[O26 §§2.2,3.1.2,3.10]|solutions and candidate investments; scenario and horizon lineage, investment category, units|filter/aggregate need opportunities as specified; produce system-needs evidence|rendering and internal ETL free|infrastructure needs register and KPI tables; definitions reproducible and lineage complete|missing indicators or invalid aggregation|SR-018, SR-019; **OPEN:** exact external report data schema not fully specified|
|**P12** Quality control / method sign-off|[O26 §5.1; D derived systems-engineering gate]|all manifests and runs; run versions and evidence artifacts|check implementation sanity, review unresolved obligations and approve publication|choice of CI/reporting platforms free|acceptance report and findings; structural, semantic and implementation conformance clearly separated|failed/unresolved normative requirement|SR-020, SR-021; **OPEN:** formal ENTSO-E acceptance procedure not in source|

## Critical process semantics
1. **Branch separation** [O26 §§3.9–3.10]: LF expansion is the required baseline; internal-constraint assessments must be labeled supplementary. An optional OPF analysis must not silently replace the LF investment portfolio.
2. **Non-anticipativity** [O26 §3.1.1]: investment `x_i` has no weather index for one study year; operation/dispatch does. Weather probability impacts objective, not independent investment decisions.
3. **Two-stage LP** [O26 §§3.1.1, 3.10]: candidate eligibility changes between stage 1 and stage 2. A generic one-stage optimising tool is not proven conformant just because its objective has the same name.
4. **Spatial modelling** [O26 §§3.8–3.8.4, Annex 6.1]: busmap conservation is only one necessary condition, not proof that the equivalent impedance/rating representation is adequate.
5. **Report ownership** [D]: publication/acceptance authorization is a proposed governance process, **not an ENTSO-E clause**.

## 2026 scenario manifest [O26 §3.7, pp.19–20]
|Horizon|Weather IDs|Weights|
|---|---|---|
|2035|WS032, WS037, WS059|0.24, 0.43, 0.33|
|2040|WS065, WS071, WS077|0.20, 0.40, 0.40|
|2050|WS091, WS092, WS106|0.23, 0.57, 0.20|

These are the **published selection outcomes**, not the entire selection algorithm.

## Method-ambiguity register
|Issue|Source|Why it matters|Resolution criterion|
|---|---|---|---|
|MD-01 Approved version unknown|O26 cover/status|Cannot assert normative 2026 acceptance|Method owner identifies approved or current effective version|
|MD-02 PCA/k-means deterministic options|O26 Annex 6.3; OS Annex III|Independent selection algorithms may produce different outputs|Publish feature set, scaling, eigenvectors, random seed, tie rules, effective code/profile|
|MD-03 Zonal calibration convergence|O26 §3.8/Annex 6.1|Equivalent networks differ numerically|Publish invariant/tolerance/validation datasets|
|MD-04 Partial candidate handling|O26 §§3.1.1, 3.10|Two-stage eligibility ambiguous at implementation detail|Method owner signs candidate state machine and sample test|
|MD-05 Broken PDF reference|O26 §4.6 around p.40|Source contains an unresolved cross-reference|Publish erratum/clarification|
|MD-06 Report KPI schema|O26 §§2.2,3.1.2|Needed for strict system acceptance|Authoritative field definitions, aggregation rules and required artifacts|
|MD-07 Hydrogen constraint closure|O26 §§3.3,3.6|Semantics underconstrained for independent implementers|Approved H2 model/assumption profile|
