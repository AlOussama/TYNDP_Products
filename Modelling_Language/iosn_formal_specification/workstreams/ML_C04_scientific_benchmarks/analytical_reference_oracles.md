# ML-C04 — Analytical Reference Oracles and Proof Boundaries

**RESEARCH ONLY; all values illustrative; no sanctioned numeric source oracle or numerical acceptance tolerance.** Catalogue: scientific_benchmark_catalogue.md. Machine-readable fixtures: synthetic_cases/cases.json. Distinguish carefully (P) proved on stated assumptions; (A) hand-derivation; (T) self-check if specifically executed; (N) no native model/tool execution.

## A. Reproducible numeric derivations (P/A only unless execution record says otherwise)

|Case|Mathematical oracle|Positive expectation|Targeted counterexample|Proof boundary|
|---|---|---|---|---|
|B01|F(x)=3x+10Σw_c max(d_c−x,0), 0≤x≤4|x*=3, F*=11.5, expected ENS=.25 MWh|uncoupled x_c: 6.75; uniform synthetic weights at x=3: 11|fixed-cost fictional one-hour LP only|
|B02|E=Σ_c w_c Σ_t u_c Δt_t; J=7+100E|E=5.1 MWh; penalty=510 EUR; J=517 EUR|uniform CY:4.8 MWh, J=487; CAPEX repeated|no genuine economic periodisation|
|B03|E=2×.5+4×1.5|7 MWh|unweighted MW sum=6; 1h each=6|UTC source calendar unresolved|
|B04|b=1; f_AB=θA−θB, f_AC=θA−θC, f_CB=θC−θB|f=(60,30,30) MW|physical f=(90,0,0) KCL only, KVL violation=90 MW|no offsets/PST/HVDC|
|B05|triangle PTDF=(2/3,1/3,1/3), outage AB yields LODF=.5 each|before=(60,30,30), after=(0,90,90); cut=50 MW|LODF=0 predicts 30 instead of 90; missing 10 MW cut|only necessary network sanity checks|
|B06|stage1 min(2x1+10u1) need1, then fixed x1 and min(x2+10u2) need2|x1=1,x2=1, final cost3 EUR|joint x1=0,x2=2 cost2; duplicate charge cost5|**hypothetical** fixed carry-over only|
|B07|e1=e0+η_ch p_ch Δt_ch; e2=e1−p_dis Δt_dis/η_dis|2→2.8→1.8 MWh; s=0.5→0.7→0.45|omit Δt: e2=1.6 MWh|boundary conditions unapproved|
|B08|E_H2=η_EL p_EL Δt, E_used=p_H2E Δt/η_H2E|3.5=1.75+1.75 MWh_H2; frozen energy=12 MWh_e|[6,6] MW vs frozen [3,7] MW with same 12 MWh|no approved H2 baseline|
|B09|e1=e0+(inflow−turbine)Δt; load_implicit+δ|e1=4 MWh_water_eq; net load=(3,7) MW|omit inflow e1=2; same DSR resource in two ledgers|DSR shift conditional|
|B10|LF KCL and θ-difference; separate OPF bound|f_LF=5 MW possible; OPF x=1≤x_LF=2|LF forced to obey R=3; OPF x=3>2|LF scope MD-08|
|B11|s=x+y−4≥0 and row scaling 2x+2y−2s=8|projection feasible-set equality; optimal (4,0), 8|s negative gives x=y=0 feasible|symbolic proof on toy LP only|
|B12|optimal face x+y=1; min x+y|all (1,0),(0,1),(.5,.5) optimal; obj=1|comparator flags component differences|noninvariant per-asset KPI|
|B13|same E as B02, no formula authority|raw E=5.1, raw ENS value=510, official KPI=BLOCKED|unweighted 24 MWh or invented KPI|no official KPI/threshold|
|B14|applicability / capability predicate|missing mandatory ⇒ UNSUPPORTED; optional off ⇒ NOT_APPLICABLE|claim PASS after skip|tool ability not tested|
|B15|L=100 km×(1+.12); offshore RES exogenous|112 km only illustrative; productive value BLOCKED|12% treated as approved; 100 MW made investment|route/owner data absent|

### Derivation B01 — unequal synthetic scenario probabilities
For d=(0,1,2,3,4), w=(.10,.20,.30,.15,.25), the slopes of F away from kink points x=0,1,2,3,4 are: x∈(0,1):3−10(.90)=−6; (1,2):3−10(.70)=−4; (2,3):3−10(.40)=−1; (3,4):3−10(.25)=+.5. Hence unique minimiser x=3; F(0..4)=(22.5,16.5,12.5,11.5,12.0). Expected ENS=sum w_c max(d_c−3,0)=.25 MWh. Unlinked scenario-specific investment picks x_c=d_c at weighted cost Σw_c 3d_c=6.75 EUR. This is a different optimisation problem; lower cost proves *relaxation*, not better tool quality.

Across study years the synthetic profile is e.g. (w_2035, w_2040, w_2050)=(w,w,w) with w *nonconstant over c*. Perturb only 2040 by (+.01,−.01,0,0,0): sum stays one but D2 year-identity fails. Neither w=.2 nor any particular vector follows from D2.

### Derivation B04–B05 — KCL does not imply KVL; LODF not arbitrary
Triangle edges A→B, A→C, C→B and b=1. p_A=+90,p_B=−90,p_C=0. With θ_B=0, nodal KCL implies θ_A=60, θ_C=30; f_AB=60, f_AC=f_CB=30. Independent free transport links can carry (90,0,0) with identical KCL, but it violates physical KVL f_AB−f_AC−f_CB=0 by 90 MW. For an outage AB, the remaining path A→C→B carries 90 MW per edge. Thus LODF_AC,AB=LODF_CB,AB=(90−30)/60=1/2 (on THIS triangle); values are computed from the network, not configurable defaults. Islanding, offsets and real contingency sets require their own rules.

### Derivation B06 — different transition mappings are not equivalent by assumption
Stage1 feasible x1∈[0,2], u1≥max(0,1−x1), cost 2x1+10u1 ⇒ x1=1. Stage2 **assuming F means fixed committed x1**: x2∈[0,2], u2≥max(0,2−1−x2), incremental cost x2+10u2 ⇒ x2=1. Total x1 cost 2 plus new x2 cost 1 = 3. A joint reoptimisation instead permits (x1,x2)=(0,2) and cost 2; this is a counterexample to silently merging stages, **not** a claim that fixed carry-over is the approved methodology. If Stage2 charges x1 again: 2+3=5 and the cost ledger is wrong. Need MD-07/02 before accepting one interpretation.

### Derivation B07–B08 — state and carrier dimensions
B07: e1=2+.8·2·.5=2.8; e2=2.8−1·.5/.5=1.8 MWh. For fixed Emax=4 MWh, s=e/4 maps both bounds and recurrence bijectively; if Emax is an endogenous LP decision, an unqualified division by Emax is nonlinear/undefined when Emax=0 and is **not** a blanket LP equivalence.

B08: hydrogen production 10 MW_e×.5 h×.7=3.5 MWh_H2; return-to-power demand 1.4 MW_e×.5h/.4=1.75 MWh_H2; remaining H2 load 1.75 MWh_H2. Independently the frozen preexpansion profile [3,7] MW over [.5,1.5] h gives 12 MWh_e. Mutated [6,6] MW also gives 12 MWh_e. This establishes explicitly why total energy equality is inadequate to prove **hourly** equality.

### Derivation B09–B10 — conditional versus universal invariants
Hydro uses a declared **energy-equivalent water basis**, not automatically volumetric m³. A pure DSR shift with net energy preservation is an *illustration conditional on product semantics*, whereas disjoint resource IDs for implicit-versus-explicit accounting are relevant independent of the toy energy total. LF f=5 MW retains KCL/KVL even if its defined internal transport rating would be R=3 MW in a subsequent OPF. Enforcing R at the wrong stage changes its feasible set; omitting DC-Mesh equations from LF also changes it, despite apparent relaxation.

## B. Required future evidence by verification layer

- **V1 input:** original source release, multi-axis CY profile/weights, UTC interval bounds, units/price-year, candidate eligibility, data hashes and one-to-one IDs.
- **V2 process/physics:** carrier balance, connected partition, cut reconciliation, six network output categories, DSR/Hydro class, freeze-profile identity.
- **V3 generated mathematics:** scenario indices and nonanticipativity rows or a common x, exact objective coefficient inventory, network cycles/no-load/PST, market-link type and NTC, stage carryover/cost terms, storage transition, optional OPF bounds; compare *semantics*, not text.
- **V4 numerical optimality (not run):** primal and scaled residuals, dual feasibility, complementarity and gap/certificate or equivalent verified bounds, solver statuses and independent recomputation; owner-specified numerical tolerances are TBD.
- **V5 outputs:** raw vs derived vs published lineage, meaningful denominators, formula ID and input units, degeneracy treatment; undefined KPI blocked.
- **V6 audit:** trace IDs, case hashes, condition/applicability, failure evidence, reviewer independence, approval/gate status.

**No generated model, native solver, real DFT/PECD/PEMMDB input, PTDF calibration, official KPI, discount calculation or two-tool comparison has been run.** No productive numerical threshold is introduced by this document.
