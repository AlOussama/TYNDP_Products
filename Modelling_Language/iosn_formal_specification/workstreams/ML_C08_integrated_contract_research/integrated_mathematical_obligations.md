# ML-C08 — Integrated Mathematical Obligations M01–M18

**NONNORMATIVE RESEARCH.** ML-R00 Draft-PR #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2; C01–C07 exact source heads in integrated_scientific_contract_reference.md. No adopted IoSN methodology, original data qualification, model/solver execution, human-independent audit or normative contract release. G1 BLOCKED.

## 1. Scientific mathematical reference, not a required syntax

Study years Y={2035,2040,2050} are separately optimized. Five CY1–CY5 are selected **externally** for each year. Weights w(y,c)=w(c) are identical across the three years **by case identity** but are permitted to be nonuniform across cases; numerical weights and accepted normalization remain TBD. Time is canonical UTC with positive Δt in hours. Electricity and H2 quantities use explicit dimensions and conversion bases, and investment x(y) is a first-stage decision shared across CY within one study year. This imposes no cross-year endogenous investment coupling and no additional general robustness/minimax requirement.

Schematic research objective only (where operating cost is per hour rather than already integrated per interval):

    min   C_inv,y(x_y) + Σ_c w(c) Σ_t Δt(y,c,t) C_op(y,c,t)
    subject to a common x_y across weather cases,
               relevant electric/H2 balances, physical DC constraints,
               eligible stages, storage/intertemporal dynamics,
               and applicable conditional modes.

Cost source/price-year, CAPEX payment timing, VoLL, discounts, H2 units and all real values remain Owner/source TBD. Do not double count Δt or investment CAPEX. R01 symbols and their [O]/[D]/[S]/[E]/[I]/[TBD] classification remain definitive research source, not an adopted single LP.

## 2. Family-by-family contract and falsifying controls

| M | Obligation | Scoped invariant | Toy benchmark | Native/Owner oracle |
| --- | --- | --- | --- | --- |
| M01 | Nonanticipative expected cost | One x(y) shared across CY; replicate x(y,c) only with coupling and CAPEX once | B01 B02 B06 | E04 indices/coupling; real weight values TBD |
| M02 | Operating costs and ENS | Weighted energy: MW × Δt h × EUR/MWh; avoid second Δt if already interval cost | B02 B03 | E04/E05 objective terms; VoLL and period source TBD |
| M03 | CAPEX, discount | Correct investment payment frequency, price-year, discount and stage attribution | B02 B06 | E04 objective decomposition; MD-02/MD-07 TBD |
| M04 | Electrical nodal KCL | Generation, demand, losses as sourced, converters, shedding and signed network injections | B04 B08 | E04 KCL rows and native residual; source mapping TBD |
| M05 | Physical DC mesh | Angle or PTDF/cycle with consistent branch impedance, topology, PST/offset, island references | B04 B05 B11 | E04 generated KVL and projection; calibrated grid TBD |
| M06 | LF vs OPF limits | LF preserves physical network impedances; P15 ON cap needs genuine LF reference | B10 | E04 guards/bounds and E05 LF reference; MD-08 TBD |
| M07 | Candidate controllable market link | NTC/directional and investment bounds distinct from physical KVL branch | B04 B06 | E04 asset-role and candidate rows; owner source TBD |
| M08 | Staged candidate expansion | P10 real, P11 residual/conceptual, P12 storage; preserve stage eligibility and cost | B06 | E04 stage transfer F_y, allow lists; MD-07 TBD |
| M09 | Zonal partition | Disjoint connected bus groups and stable topology/zone mapping | B05 | E03 topology/crosswalk; detailed source grid TBD |
| M10 | Reduced network equivalence | Six classes and relevant PTDF/flow response; conservation is not complete physical proof | B05 B11 | E04/equivalence and source-calibrated oracle TBD |
| M11 | Contingency network ratings | Consistent LODF/PTDF, seasonal and directional N−1 capacity calculations | B05 | E04/E05 independent outage topology/limits; owner oracle TBD |
| M12 | Zonal data allocation | Extensive quantities conserved; intensive ratios weighted/recomputed, UTC/units explicit | B03 B13 | E02/E03 source and preservation witness; MD-11/12 |
| M13 | Storage dynamics | MW power versus MWh capacity, time-indexed SoC, efficiencies and boundary states | B07 B11 | E04 state/bound rows; initial/terminal conditions TBD |
| M14 | Hydro physical classes | Five hydro classes distinct; inflow, reservoir, spillage and energy/water dimensions | B09 | E04 water/energy balances; class parameters TBD |
| M15 | Hydrogen coupling | H2 and electric units, η and LHV/HHV basis explicit, exogenous hydrogen links | B08 | E04 conversion/balance; MD-10 basis TBD |
| M16 | DSR distinction | Implicit and explicit DSR identity; avoid double-count or invented universal rebound | B09 | E03 and E04 DSR-specific rows, owner semantics TBD |
| M17 | Offshore exogenous targets | Fixed targets distinct from elective routes, class and cost traceable to source | B15 | E02/E04 project identities, route/parameter authority TBD |
| M18 | P13/P14/P15/P16 semantics | Paired dispatch, frozen pre-expansion H2, conditional OPF, raw/KPI/SystemNeed separation | B08 B10 B12 B13 B14 | E03–E08, B01-D072/B01-D081 and reporting Owner TBD |

Original R01 M01–M18 and all original MA01-SR are retained by reference and cross-linked in [end_to_end_requirements_traceability.csv](end_to_end_requirements_traceability.csv). The benchmarks in the table are illustrative associations, not complete compliance proofs.

## 3. DC network equivalence and its limits

For an oriented physical graph with incidence A, susceptances B positive and consistent flow offsets f0, an angle formulation f=B Aᵀθ+f0 with A f=p may be projected to PTDF or cycle space under connected-component reference and net injection consistency. For cycle basis C spanning ker(A), Cᵀ B⁻¹(f−f0)=0 enforces KVL. Equality of these projections requires consistent topology, signs/offsets, islands and all bounds. A controllable DC **market link** participates through injection balance but is not placed in the physical cycle basis as a KVL-branch. A reduced-grid conservation check alone does not prove six-category equivalence, LODF/N−1 behavior or calibration. Numerically qualified detailed/reduced grid source and Owner oracle are missing.

Storage example: E_(t+1)=E_t+η_ch P_ch Δt−P_dis Δt/η_dis, subject to sourced initial/final energy and bounds. A normalized SoC E/Emax is equivalent only if Emax>0 and all bounds and trajectories are mapped. Real hydrology and H2 LHV/HHV conventions remain source dependent.

## 4. Mathematical equivalence and degeneracy

Let mapped projected feasible sets be Fhat_A=π_A(F_A(d)) and Fhat_B=π_B(F_B(φ(d))) at the same frozen input d. **E-FEAS** requires equality of the projected feasible *sets*, not merely identical sample optima. **E-OPT** requires justified objective values and equality of complete projected **optimal sets**. **E-OBS** requires separately declared observations (per-run KPI, set-valued KPI or distribution) and corresponding protocol. A source objective can match while feasible sets differ; an equal feasible set can have different objective and optimal set. For x,y≥0 and x+y=1, both (1,0) and (0,1) minimize x+y, so exact portfolio-vector equality is not a universal tool conformance test.

D5-A1 risk-guided future deep equivalence D4 research candidates include SR-017/-018/-019/-027/-029/-035. A formal/projection proof may be warranted where high risk, but universal algebra text identity is not required for independent tools.

## 5. Existing evidence taxonomy and unresolved quantitative science

C04 EX-02 logged **15/15** positive and **15/15** negative *local synthetic arithmetic/metadata predicates*, following a detected incorrect B05 triangle LODF 0.5 corrected to (90−30)/60=1.0. Twenty-six designed mutants were not run against native model generators; the written Python candidate harness was not executed in C04. C06 135/135 shared mock classifications do not construct LP constraints. An actual native E04 variable/constraint/term/offset/bound witness, E05 solver objective/primal/dual/bound witness and independent oracles have not been produced in any of these inputs. All 48 native R04 tests remain NOT_EXECUTED.

Open: source-adopted method, CY source/weights, MD-12 UTC details, costs/discount MD-02, MD-07 stage transfer F_y, real topology reduction PTDF/LODF/N−1 threshold, storage/hydro/DSR technical rules, MD-10 H2 unit basis, pre-expansion B01-D072 reference solve, P15 activation/LF cap, B01-D081 reporting-owner filter and all productive tolerance/oracle values.
