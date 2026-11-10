# BUNDLE-01R B — Data Qualification Blockers and Owner Action Requests

**Status:** `NOT_DATA_QUALIFIED`. The inventory still expresses mandatory **requested data properties**, not inspected source values. **87 objects = GOVERNANCE_OR_CONFIGURATION_INPUT:6, STUDY_CONFIGURATION_REFERENCE:1, EXTERNAL_DATA_RELEASE_REFERENCE:1, EXTERNAL_UPSTREAM_DATA:42, IN_SCOPE_INTERMEDIATE_OR_PRIOR_STEP_OUTPUT:35, VERIFICATION_REFERENCE_OR_APPROVAL_INPUT:2.** All 87 lack verified per-object original file bytes, SHA256 and consumed study-specific frozen release; 28/28 planned validations remain blocked.

## Itemized owner requests

|Scope/Source owner|Exact evidence to supply|Impact if unresolved|
|---|---|---|
|ENTSO-E Scenario/PEMMDB Owner|Source release IDs and original PEMMDB CommonData/2.X files, schema and exact modelled scenario/country/zone/year extraction; original SHA256 and IoSN freeze manifest|P01/P07–P10 no market source conformity|
|PECD/Upstream Weather Owner|Exact PECD v4.2 vs posted package release, selected WS IDs/weights and source profile IDs including hour & spatial maps, SHA256|P02–P03/P07 weather manifest and profiles blocked; no selection algorithm|
|DFT/EV/Heat Data Owner|Demand.zip versus actual DFT export mapping, units/time axis/weather and zones; file checksums|Hourly load, EV/HP and DSR semantics not verifiable|
|Hydro Owner|Hydro-Inflow archive version, 5 hydro classes/constraints, inflow periods, reservoir states and checksums|P03/P08 hydro constraint input blocked|
|H2/P2G Owner|Hydrogen.zip/P2G.zip vs actually consumed H2 infra and conversion data; GW/MW, LHV/HHV, H2 freeze series|P08/P14 coupled energy and sensitivity blocked|
|TSO Network Owner|Exact synchronized 2025 detailed AC/DC grid, seasonal/directional ratings, critical line flows, PTDF/LODF, network reduction reference and signed accuracy criteria|Scenario 2026 Line-data/Nodes links **cannot be substituted** for P04–P06 detailed IoSN grid|
|Starting Grid / Project Owner|Signed 2035 initial projects, RDFIDs and maturity a/b/c crosswalk, original frozen project submission versus Sept project updates, adopted offshore fixed targets|P04 starting grid eligibility unresolved|
|Candidates/Offshore Owner|Real/conceptual/theoretical candidate lists, region geometry, market-link NTC+/− and route factor, canonical IDs, costs|P09–P12 investment feasible sets blocked|
|Economics/Storage Owner|Fuel/CO2 actual input data, CAPEX/OPEX, price year, discount blocks, WACC scope and storage 2040/2050 country trajectories|P09/P12/P16 objective and KPI references blocked|
|Verification/Results Owner|Approved KPI formulas, investment filter, internal grid dispatch pair cases, physical LP/H2/OPF (if run) fixtures, numeric acceptance thresholds|P13–P17 no source/model/data validation PASS|
|ENTSO-E Methodology/Governance Owner|Approved exact IoSN methodology PDF/release bytes/hash and signed source/per-file data authority for IoSN 2026|Entire input contract cannot be normative|

## Traceability issues

- Existing **93** proposed data→MR/SR links pass reference integrity but remain analyst-to-owner allocations, **0 domain-approved** and **0 with qualified source artifact**.
- **67/87** objects are directly linked to ≥1 SR; **20/87** remain process-only; this is not inherently an error, but it requires explicit Requirements/Process Owner decision for each object before release.
- Explicit source-class distinctions appear in `qualified_input_inventory.csv`; prior step outputs cannot be counted as public external files or independently present before runs.

**Access failure ≠ proof of data nonexistence**. The next action is owner-provided frozen original artifact release and signed test oracles, not inventing a substitute dataset.
