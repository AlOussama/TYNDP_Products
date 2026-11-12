# ML-C01 — Independent Semantic Review (adversarial research role)

**Reviewed:** 12 November 2026. **Baseline:** ML-R00 Draft PR #32, commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2. **Author/reviewer independence limit:** this is a *role-separated adversarial review by the same AI authoring process*, NOT independent human/organizational review, NO source/model/G1 approval. **G1=BLOCKED.**

## 1. Review scope, method and verdict

**Source set actually read:** original [MA01 catalogue](../../iosn_requirements_catalogue.csv), [ML-R00 integrated 48-SR crosswalk](../ML_R00_consolidation/integrated_requirement_traceability.csv), [R00 INT-01…15](../ML_R00_consolidation/cross_workstream_consistency_review.md), original R01 scientific specification and math/MD register, R02 language capability/crosswalk and reviewer findings, R03 semantic model/input catalogue/transform matrix, R04 verification rules/test matrix/test catalogue. Re-fetched the original CSVs from the exact supplied commit; the C01 conflict register from the new research branch. Reviewed each MA01-SR's *original wording* against the canonical D1–D6, source/content scope, typed physical/data/output vocabulary and proposed test semantics.

**Review outcome:** RESEARCH_SEMANTIC_PROFILE_REVIEWED_WITH_OPEN_DISAGREEMENTS. Core definitions are coherent when **qualified by version and scope**. The O26↔D2 method gap, upstream R04 terminology, numerical owner oracles, data release and all 21 MD/CL are **not closed**. No native tool execution, no external original-payload qualification, no human independent review and no G1 release.

### Structural source integrity checked anew in this review

| Check | Observed outcome and its limit |
|---|---|
| MA01 active L2 set | **48 unique IDs**, 001–050 excluding 012 and 049; no new SR |
| Crosswalks at exact baseline | R00 **48/48**, R02 **48/48**, R04 **48/48** by exact SR key |
| Verification references | Exact **48/48** MA01-VN-NNN and R04-T-SR-NNN pairs |
| R04 test designs | **48** native-model test entries, all **NOT_EXECUTED**, not 48 passes |
| R03 data object types | **87**: **67** with direct proposed MA01-SR links, **20** process-only, **93** direct proposed pairs |
| Proposed R03 operations | **38**, separate from actual execution |
| R04 proposed risk tiers | **33 A / 12 B / 3 C**: a research allocation, not approved assessment |
| Integration finding IDs | Exactly **INT-01…INT-15**, all accounted for with separate owner-open status |
| Genuine source/data/mathematical approval | Not established by any of the above structural checks; G1 remains BLOCKED |

The review computations only inspect **research CSV membership and value consistency**. They do not rerun R02/R03 JS fixtures, R04 arithmetic harness, a power-system model or original ENTSO-E release checks.

## 2. All 48 MA01-SR: terminological and decision compatibility audit

**Table interpretation:** A row labelled with an established meaning means **semantically interpretable at research level**, NOT a passed model test. Each row has at least one domain-specific semantic note and linked decision/owner dependency. The exact original SR statement, constraints, process and proposed verification acceptance remain in the unchanged MA01 catalogue and R00 crosswalk; R04 status stays NOT_EXECUTED.

| Active MA01-SR | Source P-step | Original class | Semantic review classification | Domain/decision compatibility assessment | Open or confirmed D-reference / owner blocker | Native test ID / status |
|---|---|---|---|---|---|---|
| MA01-SR-001 | P16 | FUNC | SYSTEM_NEED_NOT_PROJECT | SystemNeed with separate approval state; KPI and reporting formula remain unresolved | D1;D3;D6-A / MD-04;MD-17 | R04-T-SR-001 / NOT_EXECUTED |
| MA01-SR-002 | P01 | SCOPE | RESEARCH_HORIZON_DEFINED | Separate runs for 2035 2040 2050; no cross-year investment coupling inferred | D1;D2 / MD-01;MD-20 | R04-T-SR-002 / NOT_EXECUTED |
| MA01-SR-003 | P10–P12 | PROCESS | STAGE_TRANSITION_TBD | Per-year expansion stages distinct; carry-forward is not a joint LP or invented transfer rule | D2;D3 / MD-07 | R04-T-SR-003 / NOT_EXECUTED |
| MA01-SR-004 | P01–P03 | DATA | SOURCE_DATA_TBD | Source releases and technoeconomic axes versioned, not assumed qualified | D3;D4 / MD-11 | R04-T-SR-004 / NOT_EXECUTED |
| MA01-SR-005 | P04 | DATA | PROJECT_ELIGIBILITY_TBD | 2025 detailed grid and eligible 2035 projects require separate eligibility crosswalk | D3 / MD-14;MA02-CL-001 | R04-T-SR-005 / NOT_EXECUTED |
| MA01-SR-006 | P04 | MODEL | FIXED_TARGET_WITH_SOURCE_TBD | National offshore RES targets fixed within chosen profile, not synthetic optimization decisions | D3 / MD-14 | R04-T-SR-006 / NOT_EXECUTED |
| MA01-SR-007 | P08 | MODEL | CARRIER_BALANCE_TBD | H2 electricity conversion with separate physical units and efficiency/energy bases | D3;D4 / MD-10 | R04-T-SR-007 / NOT_EXECUTED |
| MA01-SR-008 | P08 | SCOPE | EXOGENOUS_H2_NETWORK | Hydrogen transmission expansion not an endogenous electric candidate | D3 / MD-10 | R04-T-SR-008 / NOT_EXECUTED |
| MA01-SR-009 | P14 | PROCESS | FROZEN_H2_LINEAGE_TBD | Pre-expansion zonal and time-resolved H2 load profile; not post-expansion total | D3;D4 / MD-10 | R04-T-SR-009 / NOT_EXECUTED |
| MA01-SR-010 | P02 | DATA | O26_D2_SOURCE_CONFLICT | Intake only of five external CY; O26 three-case draft source difference retained; no uniform weights | D2;D4 / MD-01;MD-12;MD-18;MD-19 | R04-T-SR-010 / NOT_EXECUTED |
| MA01-SR-011 | P02–P03 | DATA | UTC_CALENDAR_TBD | UTC intervals and distinct power/energy units; missing-hour and leap policies unresolved | D2;D4 / MD-12 | R04-T-SR-011 / NOT_EXECUTED |
| MA01-SR-013 | P05 | NETWORK | ZONE_SOURCE_VINTAGE_TBD | Zone identities and O26 102-zone example version-scoped; not universal constant | D3 / MD-03;MD-13 | R04-T-SR-013 / NOT_EXECUTED |
| MA01-SR-014 | P05 | NETWORK | CLUSTER_CRITERIA_TBD | Clustering rationale is traceable; numeric importance threshold owner-dependent | D3 / MD-13 | R04-T-SR-014 / NOT_EXECUTED |
| MA01-SR-015 | P05 | NETWORK | OVERLOAD_METRICS_TBD | Hourly overload MW vs annual overload MWh distinguished and referenced | D4 / MD-13 | R04-T-SR-015 / NOT_EXECUTED |
| MA01-SR-016 | P05 | NETWORK | CONNECTED_PARTITION | Every relevant node assigned to connected cluster or documented exception | D3 / MD-13 | R04-T-SR-016 / NOT_EXECUTED |
| MA01-SR-017 | P06 | NETWORK | NETWORK_EQUIVALENCE_ORACLE_TBD | Equivalent impedances and no-load corrections require detailed-grid numeric witness | D5-A1 / MD-03;MD-15 | R04-T-SR-017 / NOT_EXECUTED |
| MA01-SR-018 | P06/P09 | MODEL | PHYSICAL_DC_MESH | Physical DC KCL/KVL branch physics; not controllable NTC candidate | D3;D5-A1 / MD-15 | R04-T-SR-018 / NOT_EXECUTED |
| MA01-SR-019 | P06 | NETWORK | N1_LODF_ORACLE_TBD | Physical N-1/LODF-derived capacity, not plain aggregate NTC | D5-A1 / MD-03;MD-15 | R04-T-SR-019 / NOT_EXECUTED |
| MA01-SR-020 | P06 | DATA | FOUR_CAPACITY_AXES | Summer/winter × forward/reverse rating dimensions, no scalar collapse | D4 / MD-03 | R04-T-SR-020 / NOT_EXECUTED |
| MA01-SR-021 | P06 | DATA | SIX_NETWORK_CLASSES | Six method classes typed; mere existence of labels not oracle conformance | D3 / MD-03 | R04-T-SR-021 / NOT_EXECUTED |
| MA01-SR-022 | P05–P06 | VERIFICATION | QUALITY_THRESHOLDS_TBD | Reduction quality reports RMSE and capacity; no implied quality approval | D3;D5-A1 / MD-03;MD-13;MD-15 | R04-T-SR-022 / NOT_EXECUTED |
| MA01-SR-023 | P07 | DATA | SPATIAL_ALLOCATION_TBD | Explicit PEMMDB PECD DFT source→zone identity and conservation/crosswalk | D4 / MD-11;MD-13 | R04-T-SR-023 / NOT_EXECUTED |
| MA01-SR-024 | P09–P12 | MODEL | LF_MODE_SEPARATION | Retain physical mesh while relevant internal ratings nonbinding in LF mode | D3;D5-A1 / MD-08 | R04-T-SR-024 / NOT_EXECUTED |
| MA01-SR-025 | P13 | PROCESS | INTERNAL_DISPATCH_DISTINCT | Internal constrained dispatch with and without LF portfolio distinct from primary LF | D3 / MD-08;MD-17 | R04-T-SR-025 / NOT_EXECUTED |
| MA01-SR-026 | P15 | PROCESS | OPTIONAL_OPF_GUARD | OPF selected guard required; if selected LF-portfolio cap mandatory, if provably false N/A only this SR | D3;D5-A1 / MD-08 | R04-T-SR-026 / NOT_EXECUTED |
| MA01-SR-027 | P10–P12 | MODEL | WEIGHTED_COST_PROFILE_TBD | Weather weighting per case with investment once; nonuniform D2 weights allowed; finance TBD | D2;D4;D5-A1 / MD-02;MD-12;MD-18 | R04-T-SR-027 / NOT_EXECUTED |
| MA01-SR-028 | P09–P12 | MODEL | BALANCES_AND_LIMITS | Electric balance, physical DC flow and operational/policy conditions need source-scoped oracles | D3;D5-A1 / MD-15 | R04-T-SR-028 / NOT_EXECUTED |
| MA01-SR-029 | P10–P12 | MODEL | NONANTICIPATIVITY | One x[y,k] over five CY; operating recourse can vary; no weather-specific investments | D2;D5-A1 / MD-15 | R04-T-SR-029 / NOT_EXECUTED |
| MA01-SR-030 | P10–P12 | MODEL | LINEAR_BOUNDS | Candidate-specific x in [0,xmax] and correct dimensions; no forced integral build | D5-A1 / MD-15 | R04-T-SR-030 / NOT_EXECUTED |
| MA01-SR-031 | P10 | PROCESS | STAGE1_ELIGIBILITY | Stage-1 LP real on/offshore only; not theoretical/other candidates | D3 / MD-07 | R04-T-SR-031 / NOT_EXECUTED |
| MA01-SR-032 | P11 | PROCESS | STAGE2_CARRYOVER_TBD | Stage-2 residual real/conceptual/theoretical with unresolved S1 carry-forward | D3 / MD-07;MD-09 | R04-T-SR-032 / NOT_EXECUTED |
| MA01-SR-033 | P12 | SCOPE | STORAGE_HORIZON | Endogenous storage 2040 and 2050 only; 2035 exogenous stock | D2;D3 / MD-06 | R04-T-SR-033 / NOT_EXECUTED |
| MA01-SR-034 | P09/P12 | MODEL | STORAGE_CLASSES_TBD | At least two classes and explicit power/energy durations; actual proxy TBD | D4 / MD-06 | R04-T-SR-034 / NOT_EXECUTED |
| MA01-SR-035 | P09–P11 | MODEL | CANDIDATE_MARKET_LINK | Candidate asset physical AC technology distinct from controllable DC market link NTC semantics | D3;D5-A1 / MD-09 | R04-T-SR-035 / NOT_EXECUTED |
| MA01-SR-036 | P09 | DATA | DIRECTIONAL_NTC_IDS | NTC forward/reverse, endpoints and project cost identities must map explicitly | D4 / MD-09 | R04-T-SR-036 / NOT_EXECUTED |
| MA01-SR-037 | P09 | DATA | OFFSHORE_TECH_COST_TBD | Theoretical VSC technology/costs revision-specific not general hardcoded facts | D3 / MD-05 | R04-T-SR-037 / NOT_EXECUTED |
| MA01-SR-038 | P09 | METHOD | OFFSHORE_FACTOR_TBD | 10–15 percent is source-described range, not an adopted value or formula | D3 / MD-05 | R04-T-SR-038 / NOT_EXECUTED |
| MA01-SR-039 | P01/P08 | DATA | MARKET_DATA_VINTAGE | PEMMDB and DSR/P2X/net market data releases and scenario scope unqualified | D3;D4 / MD-11 | R04-T-SR-039 / NOT_EXECUTED |
| MA01-SR-040 | P02–P03 | DATA | EXTERNAL_WEATHER_SOURCE | PECD versions/profiles are external; retain three-case O26 versus five-case D2 delta | D2;D4 / MD-11;MD-18;MD-19 | R04-T-SR-040 / NOT_EXECUTED |
| MA01-SR-041 | P08 | MODEL | HYDRO_CLASS_PROFILE_TBD | Five distinct hydro operational classes and time/capacity semantics; constraints incomplete | D4;D5-A1 / MD-16 | R04-T-SR-041 / NOT_EXECUTED |
| MA01-SR-042 | P03/P08 | DATA | EXPLICIT_IMPLICIT_DSR | DFT EV/HP hourly series and no double-counting implicit versus explicit DSR | D4 / MD-12;MD-16 | R04-T-SR-042 / NOT_EXECUTED |
| MA01-SR-043 | P09 | METHOD | ECONOMIC_VERSION_TBD | WACC/lifetime per O26 §4.6 source and cost category; no timeless financial default | D3;D4 / MD-02 | R04-T-SR-043 / NOT_EXECUTED |
| MA01-SR-044 | P09/P16 | METHOD | DISCOUNT_FORMULA_TBD | 2026 cost base and broken crossrefs recorded; no fabricated NPV operator | D3;D4 / MD-02 | R04-T-SR-044 / NOT_EXECUTED |
| MA01-SR-045 | P16 | OUTPUT | FILTER_POLICY_TBD | Very-small investments require owner approved threshold and raw-to-derived provenance | D3 / MD-04 | R04-T-SR-045 / NOT_EXECUTED |
| MA01-SR-046 | P16 | OUTPUT | NEEDS_AND_ONDP_TBD | Infrastructure gap and ONDP formula/lineage; no approved project conflation | D3;D6-A / MD-04;MD-17 | R04-T-SR-046 / NOT_EXECUTED |
| MA01-SR-047 | P17 | VERIFICATION | TOOL_NEUTRAL_CONFORMANCE | Plexos/Antares are examples, not mandatory; independently implemented contract/evidence | D5-A1;D6-A / MD-15 | R04-T-SR-047 / NOT_EXECUTED |
| MA01-SR-048 | P04 | DATA | START_GRID_PROJECT_IDS | Appendix project IDs/status and separate adopted eligibility rule; CBA4 not O26 approval | D3 / MD-14;MA02-CL-001 | R04-T-SR-048 / NOT_EXECUTED |
| MA01-SR-050 | P08 | MODEL | MULTIZONE_COUPLING_TBD | Power/H2 zones, prices/hubs and flows semantically distinct; link actual carrier units | D3;D4 / MD-10 | R04-T-SR-050 / NOT_EXECUTED |

### Critical groups across the 48 requirements

**External five-CY intake:** SR-010 and SR-040 require preserving the O26 three-case statement as a **consulted source fact** and D2 five-case shared-vector overlay as a **project profile**, without a weather selection algorithm. SR-011, 027 and 029 propagate time/weight/investment semantics. Nonuniform per-CY weights must not be rejected as inconsistent with D2. A real released manifest and weights are not yet available.

**Physical semantics:** SR-018 and SR-035 describe *different* assets and formulations: a DC-approximated physical branch versus an independent controllable market link. SR-017/019–022 demand reduced-network evidence, not merely a conservation assertion. The modeling language must express type-safe relation to candidates and final needs.

**Modes and conditional applicability:** SR-024 (LF), SR-025 (separate dispatch comparison) remain applicable; SR-026 (optional OPF) becomes REQUIRED conditional on a provably selected OPF mode. A missing config cannot be coerced to N/A.

**Outputs and economics:** SR-001/045/046 demand need-reporting semantics, but MD-04/17 leave formulas and filtering open. SR-027/043/044 require correct cost dimensions and year-vintage operators, not a silently selected 4%/25y result; missing approved economics is a BLOCKED oracle, not executed scientific FAIL.

**Non-equivalence:** SR-029 nonanticipative investment can be expressed with shared variables or explicitly linked scenario variables; exact AST identity is unnecessary. SR-046 multiple optimal portfolios can differ; equal objectives alone are insufficient. SR-047 mandates **tool independence**, not Plexos/Antares usage or full tool-to-tool translation.

## 3. All 15 ML-R00 integration findings: explicit semantic action

All findings below were individually assessed for semantic need. “Harmonized” means wording/typing in the **ML-C01 research layer only**; no original R01–R04 file, old finding state, MA01 content or owner register has been modified.

| INT finding | Priority | Semantic field | ML-C01 interpretation | Open owner dependency | Result |
|---|---|---|---|---|---|
| INT-01 | P0 | WEATHER_WEIGHTS | For each c across 2035/2040/2050 same symbolic w[c]; case weights may differ; 0.2 synthetic only | MD-12;MD-18;MD-19 | RESEARCH_MEANING_HARMONIZED_OWNER_OPEN |
| INT-02 | P0 | DECISION_ID_COLLISION | Namespaced project_decision:D2 weather; project_decision:D4 UTC units; test_depth:D4 deep equivalence; leave original text unchanged | MD-20 | RESEARCH_MEANING_HARMONIZED_OWNER_OPEN |
| INT-03 | P0 | STATUS_AXIS_CONFLATION | Orthogonal source,data,structure,semantics,math,numeric,output,evidence,review,gate tuple; six statuses scoped to tests | MD-15;MD-17 | RESEARCH_ONTOLOGY_PROPOSED_OWNER_OPEN |
| INT-04 | P1 | IDENTITY_CROSSWALK | Retain original IDs and 48 exact structural joins; crosswalk is research only | MD-20 | RESEARCH_HARMONIZED_MAPPING_UNAPPROVED |
| INT-05 | P0 | STAGE_STATE | S1 and S2 remain distinct; transfer F_y is unresolved rather than joint LP or arbitrary fixed mapping | MD-02;MD-07;MD-09 | OPEN_OWNER_FORMULA |
| INT-06 | P0 | PHYSICAL_NETWORK_EQUIVALENCE | Typed six classes plus detailed-grid and numerical-oracle dependencies; no physics equivalence claim | MD-03;MD-11;MD-13;MD-15 | OPEN_OWNER_ORACLE |
| INT-07 | P0 | SOURCE_AUTHORITY | Separate O26_DRAFT H24_CONTEXT CBA4_REFERENCED_EXTERNAL PROJECT_DECISION SCI_DERIVED ILLUSTRATIVE TBD; source version plus applicability | MD-01;MD-14;MA02-CL-001 | RESEARCH_CLASSIFIED_AUTHORITY_UNCONFIRMED |
| INT-08 | P0 | DIRECT_VS_PROCESS_DATA | Maintain 87 types, 93 research direct pairs, 20 process-only as distinct relation kind; no new SR | MD-11;MD-20 | OPEN_DOMAIN_ALLOCATION |
| INT-09 | P1 | PROCESS_VS_ETL | Allow types DATA_TRANSFORM MODEL_OPERATION ANALYSIS GOVERNANCE VERIFICATION; no scheduler mandate | MD-20 | RESEARCH_TYPING_PROPOSED |
| INT-10 | P0 | OUTPUT_SEMANTICS | Separate raw, OutputDefinition (METRIC_UNDEFINED), SystemNeed and ApprovedProject; formula/owner needed | MD-02;MD-04;MD-05;MD-17 | OPEN_OWNER_KPI_ORACLE |
| INT-11 | P1 | ARCHITECTURE_CHOICE | Keep A B C competing research hypotheses under common semantic kernel; no DSL or conversion mandate | D6-A;future technical evaluation | RESEARCH_OPTIONS_OPEN |
| INT-12 | P1 | EVIDENCE_SCOPE | Evidence must carry fixture_kind input_hash_state oracle_origin execution target and claim_scope; no native PASS inference | MD-11;MD-15 | EVIDENCE_BOUNDARY_EXPLICIT |
| INT-13 | P1 | VERSIONED_NUMERIC_FACT | Preserve exact source revision/units/context; no production defaults without authorization | MD-01;MD-02;MD-03 | OPEN_OWNER_PARAMETERS |
| INT-14 | P1 | PRE_EXPANSION_H2_AND_FILTER | REQUIRES_UPSTREAM_EVIDENCE for freeze series and KPI filter; not an executed run or approved threshold | MD-04;MD-10 | OPEN_UPSTREAM_EVIDENCE |
| INT-15 | P1 | RISK_AND_OPTIONALITY | 33/12/3 risk proposal only; proven OPF disabled => SR-026 N/A but mandatory LF still applicable | MD-15;MD-17 | RESEARCH_POLICY_ONLY |

## 4. Adversarial attempts to falsify the proposed ontology

| Adversarial mutation | Expected rejection or outcome | Current execution evidence |
|---|---|---|
| Rename project_decision:D2 to project_decision:D4 for weather cases | Reject decision-namespace mismatch; D4 remains UTC/units | Reasoned manually from source texts; no new native test |
| Require 0.2 across every CY as a D2 invariant | Reject as unauthorized uniform-case restriction; synthetic illustration only | Counterexample documented, not productive test |
| Label O26 consultation as ADOPTED without signed source | Reject authority escalation despite stable URL/date | Document review only; signed adopted source absent |
| Equate approved CBA4 with approved O26 | Reject cross-method authority inference | Document review only |
| Convert B01-D process-only object to new MA01-SR | Reject D1 baseline mutation | Deterministic 48 and 87 membership checks |
| Record a valid synthetic arithmetic result as productive native-model PASS | Reject fixture_kind/scope escalation | Baseline R04 native tests all NOT_EXECUTED |
| Reclassify market link (physically AC candidate) as meshed physical DC branch | Reject asset semantics and feasible-set change | Scientific counterexample designed; owner mapping TBD |
| Give LF mode full N/A because OPF not selected | Reject guard scope; only SR-026 can be N/A | Semantically reasoned; future run manifests needed |
| Publish optimized SystemNeed with ApprovedProject=true automatically | Reject result type and independent approval edge | Semantically reasoned; KPI source unresolved |
| Treat matching objectives or differing portfolios alone as equivalent/failing | Reject both false implication and false negative without feasible-set/observable proof | Synthetic LP example; approved observables TBD |
| Treat same-AI adversarial review as independent institutional signoff | Reject reviewer independence claim | Explicit NOT_OBTAINED |
| Use a source-unapproved network RMSE cutoff to convert BLOCKED to PASS | Reject absent oracle and fabricated tolerance | MD-03/15 still open |

### Review objections and residual limitations

1. **Authority remains a blocking semantic dependency.** Describing a draft accurately does not make it legally/operatively effective. The later effective method might modify obligation classes. C01 cannot resolve MD-01.
2. **Weight normalization as a modeling probability convention is not numerical owner acceptance.** The project only fixed cross-year equality and the case set. Numeric values and tolerances remain MD-12/18/19 open. C01 explicitly permits *nonuniform* weights.
3. **Typed scientific obligations do not prove full mathematical correctness.** KCL may pass while KVL fails; reduced-grid class labels can exist without an accepted detailed-grid oracle; same objective does not prove equivalent feasible set.
4. **Status transition is not globally monotone.** A later owner decision may alter effective scope; a previously successful fixture cannot be promoted across profile revisions or evidence types.
5. **Decision and namespace normalization is a mapping layer.** ML-R04 wrong D4/equal-weights wording remains in original artifacts and must not be silently rewritten in a separate PR.
6. **No truly independent reviewer.** This file documents adversarial reasoning but cannot provide institutional independence or a qualified external scientific approval.

## 5. Final disposition / completeness boundaries

**Research acceptance:** all eight ML-C01 files provide a coherent proposal for typed semantics, source applicability, status/test dimensions, 25 scientific counterexample families and precise D1–D6 meanings; **15/15 INT mapped; 48/48 SR individually assessed**. Research-level ID membership checks were re-run at exact ML-R00 source commit and this branch. There is **no** approved model correctness, no qualified original dataset, no accepted numerical/KPI oracle, no resolved owner MD/CL and no authorized source version.

**Open flags retained:** AUTHORITY_UNCONFIRMED; METHODOLOGY_CONFLICT_O26_3_VS_D2_5; MD_CL_OPEN_21_OF_21; NATIVE_TOOL_TESTS_NOT_EXECUTED_48_OF_48; INDEPENDENT_PERSON_SIGNOFF_NOT_OBTAINED; G1=BLOCKED.

**Release constraints:** Workstream ML-C01 must alter **only** its dedicated folder. PR must remain Draft against ML-R00 branch; no merge/Ready-for-Review, no BUNDLE-02 or G1 progression. The research semantics can be used as an interface hypothesis for later independently executed work packages.

**References:** [ML-R00 integration review](../ML_R00_consolidation/cross_workstream_consistency_review.md), [original crosswalk](../ML_R00_consolidation/integrated_requirement_traceability.csv), [R01 math](../ML_R01_methodology/mathematical_obligations.md), [R03 input catalogue](../ML_R03_data_process_contracts/input_contract_catalogue.csv), [R04 verification matrix](../ML_R04_verification/requirements_verification_matrix.csv), [R04 tests](../ML_R04_verification/test_catalogue.csv), [C01 conflict register](semantic_conflict_register.csv).
