# ML-C01 — Semantic Invariants and Falsifying Counterexamples

**Research-only, v0.1; baseline ML-R00 #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2.** All numerical examples below are **SYNTHETIC**, not original IoSN inputs, owner-approved KPIs or solver results. The equations and negative cases describe falsifiable semantic requirements, not a chosen model or released tolerance. **G1=BLOCKED.**

## 1. Contract-level invariants

| ID | Type / anchor | Research invariant and scope | Explicit invalid counterexample | Decision/oracle gap |
|---|---|---|---|---|
| INV-01 | Identity, D1 | Exactly 48 current active MA01-SR, 001–050 excluding 012/049; related objects carry distinct IDs | R03 producer trace automatically creates SR-049 or a new mandatory SR | MD-20; controlled baseline change only |
| INV-02 | Source, O26/D2 | O26 §3.7 states **three** cases per y (consultation); research D2 has **five** externally selected CY; both facts coexist | Mark O26's draft clause as “official 5-case adopted method” | MD-01/18/19 |
| INV-03 | Weather, D2; SR-010 | Same **indexed** weight w[c] in 2035, 2040, 2050; values not assumed uniform across c | Conformance checker rejects nonuniform [0.05,0.10,0.20,0.25,0.40] even when casewise shared across years | Weights numeric TBD, MD-12/18 |
| INV-04 | M01; SR-029 | One investment x[y,k] shared by all five CY, operational recourse u[y,c,t] may differ | Five unlinked investments x[y,CY1,k]…x[y,CY5,k] with separate optimums | Generated V3 + synthetic V2/4; no real run |
| INV-05 | M01/M02/M03; SR-027 | Investment cost appears **once** per horizon decision; weather weights applied to operational scenario costs at proper time granularity | Investment CAPEX repeated five times under expectation summation or worst-case substituted | MD-02/12, source cost definitions |
| INV-06 | D4/M02; SR-011/042 | Interval-mean MW integrated with exact Δt[h] yields MWh; UTC source mapping and semantic value type explicit | Two half-hour readings at 2 MW summed as 4 MWh, rather than 2 MWh | Calendar gaps/leap/DST/aggregation MD-12 |
| INV-07 | M04; SR-028 | Electricity node balance conserves MW for each relevant y,c,t and explicit loss/curtailment/ENS terms | Zero-injection node with net unmatched generation, hidden balancing slack | Sign/loss policy and V3/V4 tolerance MD-15 |
| INV-08 | M05; SR-018 | Existing/reduced physical branches obey DC mesh/Kirchhoff constraints, adjusted by allowed reference/PST/HVDC terms | Three equal-reactance triangle branches each carry +1 around same oriented cycle with zero nodal injection; KCL passes but KVL fails | Detailed equivalent grid and reference/PST MD-03/15 |
| INV-09 | M07; SR-035/036 | All expansion transmission candidates are **controllable directional NTC market links**, regardless of stated AC physical technology | Interpret physical AC technology as a new Kirchhoff branch, coupling candidate flow to phase angles; or use one unsigned NTC | Candidate source mapping/directional NTC MD-09 |
| INV-10 | M06; SR-024/025 | Primary LF expansion preserves DC mesh but disables relevant **binding internal interzonal ratings**; P13 tests internal-constrained dispatch separately | Remove mesh equations or use P13 constrained dispatch as base LF expansion | Mode and cap semantics MD-08 |
| INV-11 | M08; SR-003/031/032 | S1 real on/offshore LP; S2 residual real + conceptual/theoretical categories, with explicit S1 carry-forward | Joint LP for both stages; reset S1 investment to zero at S2; double-count CAPEX | **TRANSFER_OPERATOR_TBD_OWNER MD-07**, no unique S2 formula |
| INV-12 | M13; SR-033/034 | Storage state conserves energy, separate power/energy bounds; endogenous storage expansion only for y=2040/2050 | Endogenous storage build in 2035, or 1 MW of charge credited as 1 MWh without Δt or efficiency | Durations/SoC boundary MD-06/12 |
| INV-13 | M14; SR-041 | Five hydro classes retain distinct operating/resource constraints: run-of-river, pondage, reservoir, open-loop pumped, closed-loop pumped | All hydro modes converted into an unconstrained generator | Hydrology, levels and end conditions MD-16 |
| INV-14 | M15; SR-007/008/050 | P2G and H2→power balances respect energy basis/efficiency; **H2 transmission investment remains exogenous** | Optimizer chooses additional H2 pipeline size as free electric expansion candidate | H2 efficiency/profile, LHV/HHV MD-10 |
| INV-15 | M16; SR-042 | Implicit DSR already reflected in input demand must not be counted again as market-controlled flexible dispatch; explicit DSR separately modeled | Demand reduced twice by the same assumed elasticity | DFT categories/units MD-16 |
| INV-16 | M18; SR-009 | P14 frozen H2 sensitivity refers to exact **pre-expansion** temporally/zonal resolved H2/electrolysis series, not post-expansion current profile | Freeze the optimized post-expansion annual H2 total and claim pre-expansion time-series identity | Upstream pre-expansion lineage B01-D072/MD-10 |
| INV-17 | M18; SR-026 | P15 is *optional to select*; if selected, any OPF expansion is limited by LF portfolio and reported separately | OPF build=4 with LF cap=3 accepted as “optional” | Cap mapping MD-08; guard-evidence required |
| INV-18 | M09/M10/M11; SR-013–022 | P05 zones connected and complete; P06 six output categories; physical equivalent preserves accepted PTDF/LODF/N−1 behavior and four seasonal/directional ratings | Perfect zonal injection conservation but broken PTDF, wrong contingency capacity or missing PST/HVDC effects | Actual detailed grid, RMSE, LODF/N−1 acceptance MD-03/13/15 |
| INV-19 | M12; SR-023 | Zonal allocation declares conserved extensive measures, source/target spatial crosswalk and exceptions; intensity measures have special operators | Normalize a demand MW series by price €/MWh aggregation rule, or duplicate national loads for two zones | Mapping/tolerance MD-11/13 |
| INV-20 | M17; SR-006/037/038/043/044/048 | Fixed offshore RES targets and theoretical candidate route/cost parameters retain correct distinct source-vintage roles | Select arbitrary 12.5% sea detour or 4%/25yr default as approved economics for all candidates | Offshore factor MD-05, economics MD-02, eligibility MD-14/CL-001 |
| INV-21 | M18; SR-001/045/046 | SystemNeed vs ApprovedProject types and raw result→KPI formula→reported need lineage are explicit; no unapproved filtering formula | A positive expansion flagged “construction approved”, or discard tiny investment at arbitrary threshold | KPI/filter/ONDP MD-04/17 |
| INV-22 | M18; SR-025/046 | Different valid optimal portfolios are not automatically a failure when objective and required invariants/observables match for an accepted comparison scope | Compare candidate vector IDs element-wise and fail when two degenerate optima allocate differently | Approved observables/equivalence MD-17 |
| INV-23 | V axes, D3/D5 | Every technical outcome carries fixture kind, test ID, oracle, model/run scope and evidence; none implies source or gate approval | All R02/R03 synthetic PASS ⇒ G1=GO | Owner acceptance MD-15/17, review not obtained |
| INV-24 | Optionality, SR-026 | An unknown optional guard is BLOCKED; proven OPF=false gives N/A only SR-026; mandatory LF/P13 remain | Missing OPF output is taken as proof of false guard and all downstream tests marked N/A | Configuration-evidence contract |
| INV-25 | IDs/status; INT-02/03 | project_decision:D4 UTC/units differs from test_depth:D4 math; test PASS differs from data/source qualification | Interpret R04 “D4 weather overlay” as UTC approval or synthetic PASS as complete science | Corrections live in C01 overlay only |

## 2. Three discriminating mathematical micro-counterexamples

### CE-A: common versus independent weather investments

For any y, a model with only one x[y] and five separate u[y,c] can be a valid representation of nonanticipativity. Five variables x[y,c] linked by equality constraints to a common x[y] can also be equivalent. Five **unlinked** x[y,c] are not equivalent, regardless of identical objective in a particular accidental data instance. A useful synthetic counterexample varies case-specific load/operating penalties and asks whether the model can invest differently by c; the *feasible set under projection* changes if equality constraints are absent. No permitted real numeric weights are inferred from the fixture.

**Test design:** inspect native generated variable indices, equality constraints and scenario-specific perturbation; output comparison alone insufficient. Source M01 and R04 C01/C02, SR-029.

### CE-B: KCL is not sufficient for a physical meshed network

In a three-node directed triangle with equal positive reactances and zero net injections, a circular flow (1,1,1) satisfies KCL at each node but violates DC cycle consistency: the signed reactance-weighted sum of branch flows around an unshifted, zero-reference closed cycle must be zero. A model using only nodal balance and freely chosen flows accepts this false physical state. Physical branch DC/KVL **must not** be imposed on a controllable market link (it is dispatchable subject to its directional NTC).

**Test design:** small triangle, two distinct representations (angle and cycle/PTDF), same physical feasible projection; deliberately remove one cycle condition and require detection. PST/no-load effects must be part of the accepted reference when present. Source M05/M07 and R04 C04, SR-018/035.

### CE-C: the same optimal value need not mean the same portfolio

Synthetic LP: minimize x1+x2 subject to x1+x2 ≥ 1, x1,x2 ≥ 0. Both (1,0) and (0,1) are optimal with objective 1. Their candidate vectors differ, so an *equality of candidate IDs* requirement is too strict without an agreed tie-break. However, a pair of models with equal optimum but different *feasible projections* is not thereby mathematically equivalent. Compare objective, accepted physical invariants, relevant costs/needs and alternative optimality sets under an agreed observation relation; MD-17 remains open. Source R04 C07 and SR-046.

## 3. Synthetic unit and option counterexamples

- **UTC/time:** 2 MW held for 30 minutes transfers exactly 1 MWh, not 2 MWh. This says nothing about the approved method's calendar leap/DST policy, which remains MD-12.
- **Weights:** The synthetic vector [0.05,0.10,0.20,0.25,0.40] is nonuniform, nonnegative, normalized, and may be the same per CY across years. A checker requiring 0.2 for every CY would reject a valid *D2 structural profile*, and is semantically over-constraining.
- **OPF cap:** If a synthetic LF portfolio upper bound is 3 MW and selected OPF builds 4 MW, SR-026 has a falsifying numerical counterexample **if** the cap mapping is defined for this fixture. If OPF is explicitly not selected, its specific test is N/A; basic LF cannot be bypassed.
- **Network reduction:** Aggregating injection at two buses to the correct zone may conserve total MW while changing PTDF and transfer response; structural conservation PASS must not be cast as validated network equivalence.
- **KPI:** Exactly reconstructed formula arithmetic does not imply the source approved that formula. OutputDefinition can remain METRIC_UNDEFINED and a numerical candidate value can remain a raw **unpublished** result.

## 4. Planned verification relationship and trace

For each INV-ID record the linked MA01-SR (source L2), R01 M family, R03 data/transformation dependency, applicable V1–V6 and D0–D4 test depth, oracle origin, negative mutation, expected evidence and MD/CL blocker. The **exact requirement-wise ID join is inherited**, not regenerated, from [ML-R00 integrated_requirement_traceability.csv](../ML_R00_consolidation/integrated_requirement_traceability.csv); the [ML-R04 test catalogue](../ML_R04_verification/test_catalogue.csv) contains the associated R04-T-SR cases.

R04 C01–C10 are **synthetic-only** reference designs. These counterexamples are a *critique of invalid semantics*, not reports of new executed test runs. A discriminating test must not be credited until independently implemented and checked. D5-A1 permits different mathematical formulations only when their intended physical/decision projection and evidence are justified. Never require literal equation names, identical tool ASTs or a specific solver.

**Reviewer warning:** Necessary invariants are not sufficient for full IoSN conformance: especially accepted network reduction, stage accounting, economic cost formula, original input qualification, emissions/policies, H2 profiles and KPI definition remain blocked by later owner evidence. No real-IoSN counterexample or two-tool execution was produced in ML-C01.

**Sources:** [R01 M01–M18 obligations](../ML_R01_methodology/mathematical_obligations.md), [R04 verification rules](../ML_R04_verification/mathematical_verification_rules.md), [R04 synthetic cases](../ML_R04_verification/synthetic_reference_cases/README.md), [ML-R00 findings](../ML_R00_consolidation/cross_workstream_consistency_review.md).
