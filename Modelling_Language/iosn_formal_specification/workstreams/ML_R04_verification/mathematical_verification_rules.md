# ML-R04 — Mathematical Verification Rules v0.1

**Non-normative mathematical obligation templates.** Explicit unknowns remain **TBD**. Mathematical properties must hold independent of an implementation's variable names, algebraic ordering or solver package.

## 1. Index spaces and quantification

- Y={2035,2040,2050}, with separate study run and economic context per y. No unstated investment linkage between target years.
- W_y={CY1,CY2,CY3,CY4,CY5}, **externally selected** for each y; w_{y,c} positive/finite and equal as directed by D4. Their numerical owner values and accepted sum-tolerance are **TBD**.
- T_{y,c} represents a UTC-normalised sequence of instants with explicit interval durations Δt_{y,c,t} in hours; no assumption that all time steps have duration 1 h.
- N, branches B, controllable links K, candidate investments I, carriers E/H2, storage classes and stages carry persistent IDs. All model-to-data joins must preserve each axis.

**Conditional mathematical observation:** If *and only if* equality of the five weights and exact probability normalisation ∑_c w_{y,c}=1 are both approved, algebra gives w_{y,c}=1/5. This implication does not create a real weight release, source claim, tolerance, or approval. C01/C08 use a synthetic 0.2, which must never be copied into an actual input contract.

## 2. Investment and two-stage objective

Illustrative semantic skeleton for each y, subject to final MD-02/07/15 authority:

~~~text
min_x,p,u  ∑_{i∈I} CAPEX_i,y × x_i,y
         + ∑_{c∈W_y} w_y,c × ∑_{t∈T_y,c} Δt_y,c,t
              × [∑_g OPEX_g,y,c,t × p_g,y,c,t + VoLL_y × ENS_y,c,t]
~~~

Any discount/annualisation factor, vintage allocation, block sum, offshore cost and additional sanctioned objective terms are not determined by this skeleton: explicit **TBD (MD-02/43/44)**. Do not claim that this is a complete adopted IoSN objective.

### Investment nonanticipativity (SR-029)
For each y and candidate i, investment x_{i,y} is common to *all* c∈W_y. Either one shared variable x_{i,y} or scenario-indexed copies with enforced equalities x_{i,y,c}=x_{i,y,c'} is acceptable. The decision-space projection must be identical. Excluding costs in some weather cases or using scenario-specific capital decisions is a mathematically distinct model: C01 versus C02. For candidate bounds (SR-030): 0≤x_{i,y}≤Xmax_{i,y}; continuous LP feasibility with source-specific upper limits.

### Stage semantics (SR-003, SR-031–033)
The semantic stage graph must record:
- Stage 1: only eligible real transmission candidates.
- Stage 2: eligible remaining real, conceptual and theoretical candidates, with correct Stage-1 carry-forward, capacity, and cost accounting.
- Storage expansion: if in the profile, allowed only for 2040/2050; 2035 uses exogenous scenario storage.
The precise carry-forward mapping and Stage-3 rules remain MD-07/TBD. Test model generator's variable and upper-bound inventories for each stage; a final portfolio alone is insufficient.

## 3. Electric and coupled-carrier balances

For each electric node n, y,c,t:

~~~text
∑ generator MW + imports MW + discharge MW + H2_to_electric MW
  − demand MW − charging MW − electrolysis MW − exports MW
  − ENS_balance_convention = 0
~~~

ENS sign/location is fixed by the *approved* source definition; the test harness normalises to a declared injection orientation. For each H2 node separately: production (from electrolysis × conversion efficiency), H2 imports, H2 supply/withdrawal, storage and consumption must close on a declared H2 energy/mass basis, with conversions dimensionally correct. No automatic identification of 1 MWh_e with 1 MWh_H2. Input/output portfolio energies are related by explicit efficiencies; illustrative η values in fixtures may be used but never inherited as real defaults.

A generic storage example (not a methodically final formula): SOC_{t+1}=SOC_t + η_ch p_ch Δt − p_dis Δt/η_dis − losses_t; SOC and energy-basis units are MWh, power MW, Δt hours. Boundary/cyclic conditions, efficiencies and proxy-class definitions are MD-06/TBD. Hydro class constraints and DSR double-counting must be separately inspected (SR-041/042).

## 4. DC physical network versus transport link

For a fixed physical AC branch in a *linearised DC power-flow approximation*, choose a consistent orientation and reference convention:

~~~text
f_b = b_b × (θ_from − θ_to − φ_b) + f_b^0
KCL: A × f + net consumption − net generation = 0
KVL: equivalent cycle/angle/PTDF representation on physical branch subspace
~~~

Equivalent cycle, PTDF, nodal-angle, reduced-space or scaled formulations can be valid **if** the feasible projected flows/balances and phase/offset semantics are preserved. With reference offsets and modified impedance, the exact branch equation must be source-specific (MD-03/15). No blanket constraint-by-constraint identity required.

Candidate transmission reinforcement under SR-035 is a controllable **DC market link**, including where the physical future technology is AC; it participates in KCL and directional NTC/capacity bounds but is **not** a physical AC cycle relation. C04 analytically distinguishes the models: a correct KCL alone cannot prove KVL and the type of object matters. Seasonal and directional NTC+/- entries are independently mapped (SR-020/036). Exogenous H2 network expansion and fixed offshore baselines are not accidentally made electrical investment variables.

For LF primary expansion (SR-024) retain mandated mesh equations while applying the LF rule for unbounded transfer capacity of the relevant grid class. An optional OPF expansion is **not** the mandatory LF baseline; candidate capacity must be capped by LF portfolio (SR-026, C10). Do not equate LF with a physically unlimited *market link*, nor silently turn LF into OPF.

## 5. Network reduction and necessary preservation properties

**Necessary, not sufficient**:
1. Every detailed node maps to exactly one accepted cluster; each cluster connected in the required underlying graph (SR-016).
2. Aggregate injection P_cluster = ∑ native-node injections for conserved carriers/times and cut flow = algebraic sum of crossing physical flows (C05).
3. Branch rating, directional seasonal capacity, impendances, reference/no-load flow offsets, HVDC and PST impacts, mesh relations and six output categories are explicitly traceable (SR-017–022).
4. Independent detailed/reduced tests report flow RMSE, N−1/LODF-capacity behavior and the numerical acceptance rule **only once an owner oracle is approved**. Equality of aggregate injections alone is not electrical equivalence.

C05 deliberately cannot validate actual impedances, N−1 topology, PTDF, contingency behavior or network-reduction quality. No source or tolerance shall be fabricated.

## 6. V4 numerical feasibility / optimality

For an LP in canonical normalised form min cᵀx s.t. Ax=b, x≥0 with dual y and reduced costs s=c−Aᵀy, check:
- Primal feasibility: Ax−b residual, x≥0 and all native rows/bounds, with absolute **and scaled** residual views.
- Dual feasibility: s≥0, Aᵀy+s−c residual (after reformulation to the canonical equivalent and correct objective sign).
- Complementarity: xᵀs approximately zero; primal-dual gap cᵀx−bᵀy and declared feasible upper/lower objective bounds.
- Solver reported OPTIMAL/FEASIBLE/INFEASIBLE/ERROR status **plus** independently reconstructed objective and constraints from exported model and solution.
- Availability of dual/basis certificates or an alternate bounded-optimality proof; a primal incumbent with no admissible lower bound **cannot** establish optimality by assertion.

For constraints scaled very differently, compare absolute and dimensionless residuals explicitly with per-quantity scales. All tolerance values and comparison units (MW, MWh, EUR, €/MWh, relative gap) remain **TBD (MD-12/15)**. Avoid hard-coded 1e-6 as a released criterion; a solver's defaults are not an external methodology standard. A failed numerical solution does not prove the model's semantic equation family incorrect – report V3 and V4 separately.

**Reference:** HiGHS KKT documentation distinguishes primal/dual feasibility, equation residual and optimality tolerances: https://github.com/ERGO-Code/HiGHS/blob/master/docs/src/guide/kkt.md

## 7. Equivalent formulations and multiple optima

Three noninterchangeable equivalence claims:
- **E-FEAS:** same feasible *projection* on contract-relevant physical decisions, after a proven data/parameter mapping.
- **E-OPT:** same optimal objective value and mapped optimal-solution set for fixed inputs; weaker than E-FEAS, not enough for generality.
- **E-OBS:** same explicitly selected observables/KPIs on tested inputs; weaker, may mask wrong constraints.

C06 supplies a constructive proof for E-FEAS (slack elimination and row scaling). A finite sample cannot prove all-input equivalence; use D4 when a decision- or criticality-trigger justifies symbolic or parametric analysis. C07 demonstrates that identical valid objectives and invariant aggregate capacity may correspond to distinct optimal investment vectors. Report objective interval, primal feasibility and requirement-relevant invariants; project-specific non-invariant KPI vectors and alternative portfolios are **not** artificially forced equal. If a tool returns an ɛ-optimal solution, the ɛ and proof method are explicit and **TBD** for production.

## 8. V5 outputs and KPI mathematics

Expected energy in MWh is ∑_c w_c ∑_t Δt_t × P_c,t, not ∑_c∑_t P_c,t. ENS penalty in EUR is VoLL [EUR/MWh] times ENS energy [MWh], with correct temporal, scenario and discount basis. C03 and C08 include analytic examples plus intentionally wrong aggregations. Keep raw unfiltered outputs; publish source/KPI lineage, formula version, denominators and explicit "Systembedarf" semantics. Filtering small investment quantities requires MD-04 approved threshold; no silent drop.

**Research completion does not imply approved mathematical verification:** the listed equations are property templates conditioned on final owner methodology, and no real solver/model tests were executed.
