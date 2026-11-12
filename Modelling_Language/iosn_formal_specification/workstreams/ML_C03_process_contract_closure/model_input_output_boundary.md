# ML-C03 — Model Input / Output Boundary Contract

**Research reference:** ML-R00 PR #32, commit `9162def25d22c37b1fbc38f7d80fe929425cc8d2`; [R03 Input/Output Contracts](../ML_R03_data_process_contracts/model_input_output_contracts.md), [R01 mathematical obligations](../ML_R01_methodology/mathematical_obligations.md), [R04 evidence design](../ML_R04_verification/tool_conformance_evidence_specification.md). **NON_NORMATIVE / NO_ORIGINAL_DATA_QUALIFICATION / NO_NATIVE_MODEL_RUN / G1 BLOCKED.** The following are logical types and obligations, not a JSON, YAML, DSL or tool schema.

## 1. Seven intentionally non-interchangeable object classes

| Boundary type | Identity / minimum semantics | Authoritative producer | Examples / linked process | Permissible next step |
|---|---|---|---|---|
| **Original external data** `SourcePayload` | `source_id, source_release_ref, exact_file_version, content_sha256_if_verified, native_grain, native_units, location/time/CY/year/scope` | Named upstream data or governance owner; original bytes | PECD profiles B01-D008/011, grid B01-D014, economic reference B01-D055, H2 B01-D040 | Validate provenance, not silently redefine the source |
| **Derived or reference data** `DerivedDataInstance` | `definition_ref, producer_transform_ref, ordered_input_instance_refs, transform_version, params_ref, output_grain, provenance` | Explicit P03–P09 transformation *when actually run* | UTC axis, bus→zone mapping B01-D021, reduced N-1 B01-D029, zonal data B01-D034 | Model input only after structural/semantic data checks and source-qualification gate |
| **Fixed model parameter** `ModelParameter` | `model_version, parameter_role, source_or_derivation_ref, unit, index_set, carrier, bounds, fixed_or_exogenous` | Model compiler/adapter from qualified data and declared method | exogenous H2 network, NTC, storage cap, electrolysis efficiency, cost coefficients | Instantiate variables/constraints; keep origin and scenario axes |
| **Endogenous decision variable** `DecisionVariable` | `model_ref, symbol_role, index_set, domain, physical_unit, bounds, stage_id, nonanticipativity_partition` | Independent energy modelling tool, according to scientific contract | shared investment `x_{k,y}`; dispatch `p_{g,y,c,t}`; flows, SOC | Formulate mathematical programme and solve; not an import data field |
| **Raw solver result** `RawResult` | `result_id, model_run_id, solver_status, stage, object_ref, index_tuple, quantity_type, unit, value_or_missing_status, witness_ref` | Model solver/export adapter with native witness | `candidate_units`, `link_flow_MW`, `soc_MWh`, `unserved_power_MW` | Independently normalize/check feasibility before KPI derivation |
| **Derived metric** `DerivedIndicator` | `metric_definition_ref+version, raw_result_refs, comparator_ref, weights_ref, temporal/spatial aggregation, filter_rule_ref, units, approval_state` | Authorized postprocessing computation | ENS volume, system cost, CO2, curtailment, P13 delta, offshore route/cost | Publish only when formula, inputs, scope and owner rule are resolved |
| **Published system need** `SystemNeed` | `need_id, need_class, study_year, corridor/zone/country, direction, units, method/status, metric_ref, provenance, project_approval_status` | Authorized reporting pathway P16 after review/clearance | TransmissionNeed, StoragePowerAndEnergyNeed, OffshoreNeed | **Never** automatically imply construction/project approval |

**Separate control/evidence entities:** `SourceRelease`, `MethodologyProfile`, `OwnerDecision`, `RunManifest`, `EvidenceRecord`, `VerificationClaim` and `ReviewDisposition` are not an eighth numerical payload type. They constrain the lifecycle and claims of all seven classes.

## 2. Typed boundary and admissible transformations

```text
External source identity & release (owner-controlled)
   |  ingest + quality/axis/source checks, metadata no default promotion
   v
Original DataInstance -- P03..P09 transforms with explicit grain/units --> Derived DataInstance
   |                                                                  |
   +--------------- semantically qualified model-import ----------------+
                                  v
                          Fixed ModelParameters
                                  |         +-- Endogenous DecisionVariables
                                  +-------> |-- Generated constraints & objective
                                            +-- ModelRun & solver witness
                                                     |
                                                     v
                                             RawResultRecords
                                                     |
                   authorized formula + comparison + aggregation + weight + filter
                                                     v
                                              DerivedIndicators
                                                     |
                                     verification and publication authority
                                                     v
                                        SystemNeeds (not project approval)
```

No direct edge from `SourcePayload` to approved KPI, no direct edge from solver objective to approved welfare result, no automatic source-to-variable inference, and no direct conversion of `SystemNeed` to a build-ready project. `MODEL_WORKFLOW_OR_SOLVE` is a mathematically stateful process, not a generic ETL node.

## 3. Dimension, axis and conservation semantics

| Axis or quantity | Contractual obligation | Blocker / warning |
|---|---|---|
| Study year | Exact `2035, 2040, 2050` as separate optimization contexts; no implicit common intertemporal investment state | Methodology/profile release TBD; no 2030 substitution |
| External CY cases | `CY1,CY2,CY3,CY4,CY5` are externally selected with source and data releases; no internal selection | Numeric weights TBD; O26 §3.7 contains different draft profile |
| CY weights | For each case `c`: `w_(2035,c)=w_(2040,c)=w_(2050,c)=w_c`, `w_c>=0`, `sum_c w_c=1` on authorized numeric inputs; never force `w_c=w_d` | Missing weights block productive expected-value objective/KPIs; no `0.2` default |
| UTC time | Canonical half-open UTC interval `[start_utc,end_utc)`, interval duration, offset provenance, unique chronological key and explicit calendar conversion | DST/leap, gap fill, resampling, accepted tolerance MD-12 TBD |
| Electricity power vs energy | `E[MWh]=sum_t P[MW] × duration_h[t]` under matching time/area/carrier and proper sign; energy used for an indicator only after approved aggregation basis | Do not sum MW series and label the result MWh |
| Hydrogen carrier | Declare quantity in `kg_H2`, `MWh_H2(LHV)` or `MWh_H2(HHV)` with explicit conversion basis and efficiencies; preserve separate electrical/H2 balance equations | No equality `MWh_e=MWh_H2` without a documented conversion |
| Storage & hydro | Storage power `MW` and energy `MWh` distinct; SOC update includes efficiencies, inflow/outflow and interval duration; hydro five classes keep individual constraints | Terminal-state and hydrological source rules TBD; not a generic additive source energy |
| Network location | Physical detailed buses, reduced zones, H2 hubs, market/corridor endpoints and countries have explicit typed crosswalks; only additive quantities can be safely reaggregated with valid exhaustive mapping | NTC, PTDF, LODF, price, ratio, efficiency, mean and network flows are *not* universally additive |
| Physical electrical network | Kirchhoff/mesh/DC equivalence on existing branches with impedance, offsets, PST/HVDC and contingency context; directional seasonal N−1 ratings kept | Reduction requires approved comparison oracle, not total transfer-energy identity |
| New candidate links | Expansion transmission = controllable DC **market link** with directional NTC, even if asset implementation is AC; no automatic application of physical mesh relation to the new candidate | Candidate technology vs optimization representation explicitly separate |
| Economics | Currency, price year, real/nominal, CAPEX/OPEX, annuity/WACC/discount basis, cost decomposition and project stage/candidate IDs separate | Numeric WACC/discount rules and benefit formula unresolved |

**Invariant formulation rule:** every proposed preservation claim specifies `quantity_type, carrier, source_grain, destination_grain, mapping_type, dimensions, allowed losses, reference_conditions, oracle_ref`. If the property is not applicable to a particular quantity, use `NOT_APPLICABLE` with factual grounds, not a fabricated equality.

## 4. Model-side invariant contracts

- **M01/M02 / investments versus operational recourse:** for a fixed study year, one nonanticipative investment decision `x_{k,y}` across five CY cases and case-indexed operations `u_{y,c,t}`; objective structure `I_y(x_y)+sum_c w_c Q_yc(x_y,u_yc)` is an illustrative scientific shape, **not** permission to choose owner-unknown discount/ENS/weight coefficients. Distinct but equivalent native variable factorizations are permitted under a verifiable projection.
- **M04/M05/M06/M07 / network:** nodal/coupled balances and legal flow orientation, existing mesh DC constraints, LF internal-interzone-rating removal **only on relevant limits** (not the mesh itself), candidate market-link caps and OPF special conditions. PTDF/LODF/N−1 belong to reference/calibration evidence.
- **M08 / LP stages:** `P10_STAGE1_REAL_LP` gives real-candidate portfolio; `P11_STAGE2_LP` permits residual-real/conceptual/theoretical classes under **TBD owner transition F_y**. A cross-tool model cannot invent carry-over or count Stage-1 CAPEX twice.
- **M13/M14/M15/M16 / coupled assets:** electricity, hydrogen, storage, hydro and DSR impose typed balance and resource constraints; five hydro classes and explicit-vs-implicit DSR not conflated; H2 transmission expansion exogenous.
- **M18 / branches:** P13 paired dispatch A/B, P14 fixed pre-expansion H2 reference vector, P15 conditionally enabled OPF with expansion capped by LF; all branch results have separate `run_id/parent_refs` and never replace core LF results implicitly.

## 5. Run-type boundary ledger

| Run-type (R03) | Inputs and model assumptions | Expected **raw** outputs | Additional evidence / warning |
|---|---|---|---|
| `P10_STAGE1_REAL_LP` | P08 model, qualified real candidates and cost data, five external CY, LF mode | `x_stage1`, dispatch/flow/ENS, solver objective decomposition, status | LP generated equations and shared x; raw objective not a KPI |
| `P11_STAGE2_LP` | P10 result, remaining candidate set, owner-defined `F_y` | incremental/final investment/flow/cost, duals **if available**, status | Carry-over/de-duplication requires source and mathematical witness |
| `P12_STORAGE_LP` | 2040/2050, prior portfolio, storage country caps and technology profiles | storage power/energy, country/technology, solver status, need flag | No endogenous 2035 storage expansion; MW ≠ MWh |
| `P13_INTERNAL_DISPATCH_PAIR` | Same baseline/conditions except specified portfolio intervention, internal grid capacity | paired ENS, dispatch, costs, flows; raw differences | Pair identity/difference sign documented; KPI formula still TBD |
| `P14_H2_FROZEN_SENSITIVITY` | Explicit pre-expansion hourly zonal CY H2 load (B01-D072), freeze control | frozen-H2 electrical response, `freeze_witness`, solver status | No validated H2 pre-expansion reference-run currently; BLOCKED |
| `P15_OPTIONAL_OPF` | Explicit OPF opt-in, network constraints, LF capacity ceiling | OPF investment/flows, LF-cap evidence, separate branch status | Conditional; LF must not be overwritten; false antecedent allows supported N/A |

## 6. Raw, derived and published boundaries

Minimum `RawResultRecord`: `result_id, run_id, model_id, stage_id, study_year, CY_id_if_applicable, utc_interval_if_applicable, object_id, zone/corridor_ref, carrier, quantity_type, unit, value_or_explicit_missing_status, solver_status, solver_witness_ref, source_snapshot_ref, model_version, lineage_refs`. A not-exported dual is not automatically an error unless authoritative method makes it mandatory. Solver-status `OPTIMAL` does not by itself validate exported variable values, residuals or costs.

Minimum `MetricDefinition`: `metric_id, formula_ref, formula_version, raw_input_type_set, baseline/comparator, carrier/unit, space/time/CY reduction, weighting_ref, null_handling, filter_rule_ref, source_method_authority, owner_approval_ref`. `DerivedIndicator` must link to actual raw-result IDs and formula version; `BLOCKED_ORACLE` when essential definition is missing. Technical calculations such as multiplying a MW observation by interval hours may be checked dimensionally but are not, by themselves, adopted IoSN KPIs.

Minimum `SystemNeed`: `need_id, need_type, need_quantity, corridor/country/zone, study_year, CY_aggregation_rule, direction, provenance_to_source_run_and_raw, metric_ref, need_status, approval_status=NOT_PROJECT_APPROVAL`. Filtering needs by insignificance requires an externally authorized, versioned B01-D081 rule; unknown filter → **no filtering** and clearly blocked publication claim. Duplicate candidates/corridors and parallel links require explicit aggregation rules; unlike extensive quantities directional NTC is not arbitrarily sum-safe.

## 7. Integration interface and no-inference contract

For each boundary crossing, the receiving energy tool must either implement the semantically required behavior and provide traceable generated-model + numerical evidence, or declare `UNSUPPORTED` for mandatory capability. Structural importer acceptance is insufficient. The future multi-tool pilot compares **feasible-set projection, objective/constraints/residuals and defensible numerical results** rather than candidate-vector identity (multiple optimal portfolios may exist). Contract representation/serializer and native model decomposition remain tool-independent.

**Unresolved Owner/Method issues:** MD-01 release; MD-03/13/15 reduction; MD-02/05/06/07/09 economics/stages/candidates; MD-10 H2 reference; MD-12 UTC detail; MD-16 hydro/DSR; MD-04/17 KPI/filter; MD-08 conditional OPF; MD-11 data freeze; MD-20 evidence/approval. Data and numeric acceptance **TBD**. **G1 remains BLOCKED.**
