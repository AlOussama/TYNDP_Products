# ML-C02 — Mathematical expression capabilities and scientific equivalence

**Scope:** logical expression power needed by the future Contract. Mathematical families M01–M18 are retained from ML-R01 as research obligations, with [O] source claim, [D] research decision, [S] derived scientific requirement, [E] equivalence subject to proof and [I] illustration. **No requirement to use an identical algebraic form** and no solver or mathematical DSL selection.

## 1. Required mathematical semantic primitives

- Typed **sets and indexes**: study year Y, external weather C, intervals T(Y,C), electrical/hydrogen nodes and zones, carrier, asset roles, candidate class, stage, season, direction, contingency; explicit products and subsets.
- **Variables/parameters** distinct from inputs and outputs: control timing (before/after scenario), domain (continuous/integer if approved), bounds, unit, carrier basis, signs, stage ownership and optional/conditional guards. No unapproved integrality constraint in LP stages.
- **Algebraic obligations:** conservation equalities, signed flows, conditional linear inequalities, affine incidence/sensitivity relations, intertemporal updates, objective aggregation operators, source-referenced nonlinear/algorithmic verification properties. The logical model represents intended semantics even when implementation form differs.
- **Network constructs:** physical DC branch, nodal balance, angle/cycle/PTDF equivalence, reference flows, PST/HVDC shifts, contingency-derived limits, directional NTC market links and expansion effect matrices; route/cluster/topology mappings.
- **Process constructs:** mode selection (LF/internal dispatch/optional OPF), eligible candidate sets, staged transfer, fixed-portfolio controls, frozen sensitivity inputs, study-specific feasibility and observed raw outputs.
- **Equivalence claim:** reference formulation, alternate formulation, assumed domains, projection from native states to contract observables, source semantic revision, proof class (analytic / transformation certificate / metamorphic / bounded numerical), tolerance and counterexample checks.

## 2. M01–M18 coverage table

| Family | Model-neutral capability | Minimal scientific witness and alternative/equivalence limit |
|---|---|---|
| **M01** | scenario-coupled first-stage investment, expected operational recourse | one x(y) shared across CY; replicated x(y,c) valid only with equality couplings; do not cross-couple study years |
| **M02** | weighted operating costs, ENS and Δt dimensionality | cost units: (EUR/MWh)×MW×h; no duplicate Δt if already EUR/interval |
| **M03** | cashflow/discount operators with price basis | formula and time blocks explicit; numeric factor cannot be fabricated MD-02 |
| **M04** | electric nodal/zonally projected KCL, shedding, conversion injections | MW_e balance and signed incidence; independently reproducible residual |
| **M05** | physical existing/reduced DC mesh | angle-vs-cycle/PTDF admissible under consistent topology, no-load offsets and islands; no free-link substitution |
| **M06** | LF vs OPF physical transfer-limit guard | LF removes binding internal transfer ratings, **not** branch impedance; OPF scope owner-TBD MD-08 |
| **M07** | controllable DC market links for candidate investments | directional NTC bounds, possibly indirect effects, distinct from physical AC branch KVL |
| **M08** | S1 real, S2 residual/conceptual/theoretical, S3 storage | distinct eligibility and stage carry rule, cost reconciliation; MD-07 still open |
| **M09** | connected nonoverlapping geographic partition | exactly one zone per detailed bus and induced subgraph connected |
| **M10** | calibratable reduced-grid equivalence | six outputs/no-load, mesh, HVDC, capacity, impedance, PST; fit objective/tolerance not invented |
| **M11** | PTDF/LODF, N−1 network rating consequences | four seasonal/directional values where applicable, source topology/contingency witness |
| **M12** | conservation-aware zonal disaggregation/reaggregation | additive quantities sum correctly; intensive ratios weighted/recomputed |
| **M13** | storage MW/MWh, SOC evolution, horizon condition | time-indexed energy balance with Δt; boundary/efficiencies only if sourced |
| **M14** | differentiated five hydro classes and reservoir balance | flow/volume/energy basis and inflow/spillage; not one reservoir model for all |
| **M15** | electrical-H2 conversion and exogenous H2 network | declared LHV/HHV or mass-energy basis, no endogenous H2 pipe investment by default |
| **M16** | implicit vs explicit DSR semantics | prevent double counting; energy neutrality only if product requires it |
| **M17** | fixed offshore RES target vs routed theoretical projects | route geometry, capital-cost basis, class; 10–15% O26 source range not fixed chosen value |
| **M18** | paired dispatch, hourly H2 freeze, optional capped OPF, reporting | controls and raw/derived KPI logic; oracle/aggregation MD-04/-10/-17 |

## 3. Scientific normal forms, not mandated implementation syntax

For each **independent** y∈{2035,2040,2050} with C={CY1,…,CY5}:

\[
\min_{x_y,\{u_{yc}\}} C_y^{inv}(x_y;\eta_y)+\sum_{c\in C}w_c\,C_{yc}^{op}(x_y,u_{yc};\eta_y)
\]
subject to \(x_y\in X_y\), \(u_{yc}\in U_{yc}(x_y)\), where \(w_{y,c}=w_c\) for the **same c** in every y. Numerical weights and some \(\eta_y\) are **TBD**; probability interpretation/norm constraints are declared assumptions to be owner-checked. A tool may clone x into scenarios **if** it provides explicit \(x_{yc}=x_y\), or use common x directly; both can represent the same feasible set under projection.

Electricity KCL (generic oriented form): \(p^{gen}+p^{dis}-p^{ch}-p^{E2H}+p^{H2E}+p^{shed}-d-A^{phys}f-A^{market}m=0\) in MW_e. Existing/reduced physical branch: \(f_\ell=b_\ell(\theta_i-\theta_j)+f_\ell^{offset}\) **as a possible calibrated representation**; the correct offset/PST/HVDC topology is source-dependent. A candidate market link has bounded control flow \(-NTC^-_k(x)\le m_k\le NTC^+_k(x)\) and nodal-balance incidence, **without physical AC branch KVL**; indirect NTC mapping may require a sourced H-matrix.

Storage example: \(E_{t+1}=E_t+\eta_c P^c_t\Delta t-P^d_t\Delta t/\eta_d\) with explicit assumptions and MW/MWh bounds; the equation is illustrative, not an approved leakage, loss, terminal-SOC or energy-to-power policy. Network reduction is a **transformation + quality claim** between a detailed grid and six reduced-equivalent output classes, not simply a nodal aggregation. Net conservation can be necessary while PTDF, mesh and N−1 behavior differ.

## 4. Equivalence versus non-equivalence

A **scientifically acceptable** equivalence claim declares the source scope and a projection \(\pi:\mathcal X_{\rm tool}\to\mathcal X_{\rm contract}\). Check (i) all admissible native solutions project to contract-feasible observations; (ii) all required contract alternatives are represented (surjectivity/completeness when relevant); (iii) objective and KPI observable values preserved under accepted units/tolerances; (iv) control timing and stages unchanged; (v) feasible set under projection and optimum semantics preserved to claimed strength. Proof strength is **explicit**: structural only, symbolic/analytic, bounded numeric fixture, or run-specific feasible/optimal certificate. No unqualified universal equivalence claim from matching a few cases.

**Acceptable under conditions:** theta-angle ↔ cycle-flow DC mesh, LP reparametrisation, signed-incidence orientation reversals with consistent signs, scenario-variable replication with nonanticipativity equations, storage energy ↔ normalized SOC when \(E^{cap}>0\) and endogenous product semantics handled.

**Not acceptable by default:** physical AC-equivalent branch ↔ controllable candidate NTC market link; independent weather-specific investments; LF mode disabling physical mesh; merging stage1+stage2 without preserving eligibility/priority and owner-defined transfer; H2 LHV↔HHV without basis; hourly H2 freeze ↔ fixed annual sum; replacing original KPI with convenient tool-default formula.

## 5. Degeneracy, multiple optima and verification

Two different portfolios \(x^A\neq x^B\) may both satisfy the **same** contract with equal optimal objective. A comparison must evaluate feasibility, objective optimality with accepted numerical evidence, contract-relevant aggregations and **invariant outputs** before candidate-level equality. Where a KPI genuinely depends on which optimum is selected, the contract must specify a tie-break/tie-handling rule or report **RESULT_EQUIVALENCE_TBD**. Matching optimal objectives does **not** prove identical constraint sets or method fidelity.

Per R04, distinguish V1 data, V2 semantic, V3 mathematical generation/projection, V4 numerical witness, V5 result/KPI recomputation and V6 evidence/review. D0–D4 here are **test depth**, distinct from **project_decision:D4**. The 33 A / 12 B / 3 C test risk-tier grouping remains a **proposal**, and the 48 native tests are **NOT_EXECUTED**.

## 6. Open scientific oracles

The logical model has slots for acceptance of: LP objective valuation/discount and cost blocks; real CY weights; complete original UTC calendars; detailed grid/PTDF/LODF/N−1 and reduction RMSE/reference tolerances; NTC effect matrices; stage carry-forward; storage boundary and country trajectories; H2 conversion/dispatch basis; hydro/DSR products; optional OPF cap mapping; KPI formula/small investment filters; qualified independent verification. These slots are explicit **TBD_OWNER** values, never hardcoded examples.

**Excluded:** new generic robustness/min-max/CVaR obligation, in-scope weather-year selection, mandated 1:1 tool algebra, solution-equality-for-degenerate-optima, production model/tool conformance or architecture recommendation.