# 08 — Methodology → Contract → Verification: three use cases

**Source:** [O26] ENTSO-E TYNDP 2026 IoSN methodology, *Version for Public Consultation*, 25 Feb 2026. Link and status in README. **Key:** O = documented official rule; D = derived technical obligation; X = illustrative domain-specific configuration, not source normative. Test/oracle values below are **X unless explicitly O**.

## UC-01: Weather-year selection / preprocessing

**Representation 1 — Methodology evidence [O]:** [O26 §3.7, printed pp.19–20] lists exactly 3 weather IDs and their weights for each horizon: **2035** WS032:0.24, WS037:0.43, WS059:0.33; **2040** WS065:0.20, WS071:0.40, WS077:0.40; **2050** WS091:0.23, WS092:0.57, WS106:0.20. [O26 Annex 6.3] describes meteorological feature selection, statistical reduction and clustering; the full executable algorithm requires stronger parameter closure.

**Representation 2 — System Requirements [D]:** SR-003/004/005: the system must identify PECD/weather provenance, output the selected scenario manifest for the target horizon, retain weights and distinguish validation of published IDs from verification of the selection algorithm.

**Representation 3 — machine-readable specification [D/X]:**
~~~json
{
  "contract_id": "IOSN-WEATHER-MANIFEST-DEMO-0.1",
  "source_ref": "O26-3.7",
  "study_year": 2035,
  "expected_scenarios": [
    {"id":"WS032","weight":0.24},
    {"id":"WS037","weight":0.43},
    {"id":"WS059","weight":0.33}
  ],
  "preconditions": {"requires_peCD_provenance":true},
  "method_profile": "fixed_published_2026_selection_output",
  "selection_algorithm": "NOT_IMPLEMENTED_OR_CERTIFIED"
}
~~~
Actual interpretation, precise schema, adapters and executed fixtures: `poc/contract.json`, `poc/input.schema.json`, `poc/canonical.schema.json`, `poc/validator.py`.

**Representation 4 — verification:** VC-01 validates typed input/canonical output; VC-02 exact ID set/unique and selected weight values; VC-03 weighted sum and nonnegative finite weights; VC-04 provenance/ref/year; at least one invalid fixture deliberately rejected. **Method status:** these validate final *manifest compliance only*. A true UC-01 **selection-algorithm conformance** test additionally needs signed Annex 6.3 feature dataset, feature scaling, PCA component count, k-means initialisation/ties, weather classes and independent oracle; **OPEN MD-02**.

**Two configurations:** `rows_v1` and `map_v1` adapters normalize differing hypothetical tool exports into the same canonical contract. **Not** proof that PyPSA/Antares produced either result.

## UC-02: Electricity–hydrogen coupling, investment model

**Representation 1 — Methodology evidence [O]:** [O26 §§3.3,3.6] includes electricity and hydrogen with interconnections via electrolysers and H2-to-electricity conversion, while hydrogen network investment is outside described expansion choices. [O26 §§3.1.1,3.10] specifies LP investment planning, physical power balance and common investment decision across weather cases. Storage candidate availability differs by horizon. The source does **not** require the exact illustrative efficiencies below.

**Representation 2 — System Requirements [D]:** SR-010/011/012/013/014/015/016: declare electricity/H2 conversion ports, energy balances and candidate eligibility, enforce LP class, investment bounds, weather-nonanticipativity, stage-specific candidate sets and cost weights.

**Representation 3 — machine-readable specification [X illustrative, not O26 equation]:**
~~~yaml
profile_id: UC02-ELEC-H2-LP-DEMO
status: NON_NORMATIVE_EXAMPLE
sources: [O26-3.1.1, O26-3.3, O26-3.6, O26-3.10]
indexes:
  year: [2035, 2040, 2050]
  weather: published_weather_set_for_year
  hour: supplied_hourly_domain
carriers: [electricity, hydrogen]
components:
  electrolyser:
    input_port: {carrier: electricity, unit: MWh}
    output_port: {carrier: hydrogen, unit: MWh}
    conversion: hydrogen_out_MWh == 0.70 * electricity_in_MWh
    provenance: ASSUMED_EXAMPLE_EFFICIENCY_NOT_ENTSOE_NORM
  hydrogen_storage:
    state_unit: MWh_H2
    state_transition: H2_state_next == H2_state_now + H2_charge - H2_discharge
    provenance: ILLUSTRATIVE_NO_LOSSES
  hydrogen_turbine:
    input: hydrogen
    output: electricity
    conversion: electricity_out_MWh == 0.55 * hydrogen_in_MWh
    provenance: ASSUMED_EXAMPLE_EFFICIENCY_NOT_ENTSOE_NORM
investments:
  electricity_interconnection:
    decision: x_candidate_year
    weather_index: forbidden_for_investment
    bound: 0 <= x_candidate_year <= Xmax_candidate
  hydrogen_grid_extension: forbidden_in_this_expansion_profile
requirements:
  - electricity_balance_for_each_zone_weather_hour
  - hydrogen_balance_for_each_zone_weather_hour
  - weighted_cost_objective_by_published_weather_probabilities
  - first_stage_real_candidates_only
  - second_stage_remaining_real_plus_conceptual_offshore
  - primary_mode_load_flow
verification: [VC-05, VC-06, VC-07, VC-08, VC-09]
~~~
The conversion equations are an **example feasibility model**; the O26 source defines binding model formulation categories, not these numbers. Real storage uses unit-consistent time steps and method-authorized charging losses/self-discharge, none implicit. Scenario-consistent investment `x_{i,y}` has no `s` index; operational dispatch `p_{g,t,s,y}` does. The actual documented LP's objective and network constraints must be preserved; this YAML is intentionally not a complete LP specification.

**Representation 4 — verification:** VC-05 port-carrier/unit checks; VC-06 electric/H2 balance with residuals and a negative wrong-sign test; VC-07 common `x` across weather cases with a negative scenario-dependent-variable test; VC-08 candidate eligibility by stage and storage horizon; VC-09 objective weight/linear-constraint reference comparison. **Proposed and NOT executed**.

**Independent implementation mapping (design, not executed):**
|Contract element|PyPSA representation candidate|Antares/GEMS representation candidate|Evidence and capability gate|
|---|---|---|---|
|Electric and H2 nodes|Buses with carrier labels, balance via connected components|Commodity/balance nodes or GEMS model entities|Demonstrate both carrier conservation and correct energy unit|
|Electrolyser / H2 turbine|Link conversion or equivalent custom Linopy equations|GEMS conversion/process equations interpreted by target tool|Whether exact model profile is supported by *installed Antares version* **NOT VERIFIED**|
|H2 storage|Store or StorageUnit with eligible domain parameterization|Storage state and flow expressions in GEMS / verified Antares adapter|No claim of equivalent cyclic/terminal states without test|
|Cross-weather investment|PyPSA multi-investment/stochastic functionality with explicit shared decision / custom Linopy|GEMS indexed investment decision supported by suitable interpreter|Verify non-anticipativity *after model generation*, not inferred from syntax|
|Network and candidates|Lines/links and defined investment limits or custom LP constraints|GEMS line/network equations and bounded decision structures|Compare generated LP on a signed microfixture|
|Two-stage LP|Two explicitly orchestrated PyPSA/Linopy runs with candidate filtering|Two independent model builds/solves, if capabilities permit|Neither tool is declared conformant without tests|

PyPSA stochastic investment modelling is documented at https://docs.pypsa.org/latest/user-guide/optimization/stochastic/ . GEMS repository https://github.com/AntaresSimulatorTeam/GEMS describes explicit energy equations and Antares integration; **full UC02 capability across these products has not been experimentally validated**. Do not substitute a tool component identity for O26 methodology.

## UC-03: Postprocessing — infrastructure needs

**Representation 1 — Methodology evidence [O]:** [O26 §§2.2,3.1.2,3.10] describes identifying beneficial infrastructure expansions and presenting system-needs results; it distinguishes opportunities from a mandatory project recommendation. The reviewed source does **not** furnish an independently identified, complete machine-readable reporting schema covering all required aggregation rules.

**Representation 2 — System Requirements [D]:** SR-018/019/020: output units, horizon, zone and technology/candidate identities, model stages and traceable definition of each infrastructure-need measure; independently reproducible aggregation and evidence.

**Representation 3 — machine-readable proposed profile [X, requires business sign-off]:**
~~~yaml
profile_id: UC03-NEEDS-OUTPUT-DEMO
status: NON_NORMATIVE_EXAMPLE
source: O26-2.2_and_3.1.2
inputs:
  - scenario_weighted_expansion_results
  - candidate_metadata
  - baseline_capacity
output:
  record_type: infrastructure_need
  unique_key: [study_year, candidate_id, model_stage, method_profile]
  properties:
    added_capacity: {type: number, unit: MW, nonnegative: true}
    source_run_id: {type: string}
    source_result_digest: {type: string}
    study_year: {enum: [2035, 2040, 2050]}
    capacity_semantics: incremental_or_total_explicit
illustrative_rule:
  added_capacity_MW: max(0, optimized_total_capacity_MW - reference_capacity_MW)
  status: REQUIRES_OWNER_APPROVAL_NOT_NORMATIVE
verification: [VC-11, VC-12]
~~~
**Representation 4 — verification:** VC-11 structure, unit, uniqueness, no unresolved source references; VC-12 independently recompute the *signed/approved* KPI/aggregation and check raw-to-final lineage. The illustrative subtraction is *not* presented as O26's binding reporting formula.

**Two implementations:** PyPSA and Antares/GEMS (or any other verified engine) export tool-specific raw investment values to separate adapters, both producing the canonical infrastructure-need record. Independence is assessed at the **output meaning and approved KPI oracle**, not at identical native result tables. **Status: unexecuted design; tool capability gap remains OPEN**.

## Boundary: what is not established by three examples
No production weather selection; no fully generated 2035/2040/2050 LP; no actual grid reduction; no official KPI acceptance; no real PyPSA-vs-Antares end-to-end equivalence; no approved source version. These are explicit stop conditions for a final IoSN contract certification.
