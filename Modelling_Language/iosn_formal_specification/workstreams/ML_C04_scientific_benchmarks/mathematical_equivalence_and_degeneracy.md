# ML-C04 — Mathematical Equivalence, Observability and Degeneracy

**Non-normative formal research | D5-A1 risk-based | E ≠ string equality | G1 BLOCKED.**

## 1. Typed domains and three *nonidentical* claims

Fix source/model configuration d, parameter mapping φ and contract-relevant projection π. Let F_A(d)⊆X_A, F_B(φ(d))⊆X_B; objective functions J_A,J_B and observation maps h_A,h_B (defined *with* versioned KPI definitions). Define mapped projected feasible sets F̂_A=π_A(F_A(d)), F̂_B=π_B(F_B(φ(d))).

- **E-FEAS(d,π):** F̂_A=F̂_B. Quantifies over **all feasible points** for the stated d, not only solutions. If economic costs depend on hidden variables, their reduced value functions must additionally be preserved to infer objective equivalence.
- **E-OPT(d,π,J):** min J_A = min J_B (same validated cost basis) **and** π_A(argmin_F_A J_A)=π_B(argmin_F_B J_B). Requires equality of **sets** of optimum projected decisions, not equality of one arbitrarily selected optimum.
- **E-OBS(d,h,protocol):** equality of specifically declared *observations*, for a specified population of inputs and solver/selection protocol. Could mean one matched run, expected KPI, a full set of attainable KPI values, or distributions; without this scope its truth value is undefined.

Additional scope axes: source authority, Y/CY/time, orientation/reference conventions, line offsets, objective price basis, initial storage energy, boundary conditions, stage state, optional OPF activation, and ownership of reporting formulas.

## 2. Implications: constructive counterexamples

|Claim known|Does **not** automatically imply|Minimal counterexample|
|---|---|---|
|E-FEAS|E-OPT|A,B both F=[0,1], but J_A=x and J_B=−x; same feasible set, optimum x=0 vs x=1 and 0 vs −1 objective value|
|E-OPT|E-FEAS|A: F=[0,1], B: F=[0,2], both J=x; same optimum 0 at x=0, but B admits x=1.5|
|E-OBS for one scalar on one input|E-FEAS or E-OPT|A: F=[0,1], J=x; B: F=[0,2], J=x. Reporting just min objective 0 matches but feasible sets differ. With A: F=[0,1], J=x and B: F=[0,1], J=1−x, the reported constant KPI k≡1 matches (E-OBS for that KPI), while optimal solutions x=0 vs x=1 differ (not E-OPT)|
|E-OPT|observed same per-run portfolio/KPI|A=B={x,y≥0, x+y=1}, J=x+y. Solver A selects (1,0); Solver B selects (0,1); observed x differs|
|E-FEAS plus equal objective on every mapped feasible point|E-OPT failure **not possible** if the mapping preserves optimum attainment and hidden-variable costs|This is a sufficient condition for E-OPT, not an independent assumption|
|E-OPT plus identical set-valued output map over **all** optima|set-valued E-OBS failure **not possible**, provided same KPI definition and complete optimal-set map|Per-run deterministic E-OBS still depends on tie-break/selection|

Thus **E-FEAS alone, E-OPT alone and finite E-OBS each have narrower implications** than informal "same model" claims. A structural/parametric proof is required where conformance risk warrants D4. At fixed d, E-FEAS is weaker than equality for *all possible* input data d'.

## 3. Equivalent positive constructions and exact preconditions

### 3.1 Slack / row scaling (B11, P: symbolic)
A: x+y≥4, x,y≥0, J=2x+3y. B: 2x+2y−2s=8, s≥0, x,y≥0. Maps T:(x,y)↦(x,y,s=x+y−4) and projection π:(x,y,s)↦(x,y) are mutual inverses on feasible sets; row scaling by +2 preserves equality and sign of slack. Projected feasible sets identical (E-FEAS) and identical J on matched points means E-OPT. Unique optimum x=4,y=0, J=8. Mutation **remove s≥0** ⇒ (0,0,−4) feasible in B, J=0. The semantic check sees this despite unchanged names.

### 3.2 DC angle, PTDF and cycle formulations (P: conditional linear algebra)
For a connected physical graph, oriented node-edge incidence A∈R^{n×m}, strictly positive B=diag(b_ℓ), physical flow f, offsets f0 (which must incorporate the owner-defined PST/no-load convention), and net injection p with 1ᵀp=0:

(A) **Angle:** f=B Aᵀθ+f0, A f=p, one reference angle fixed.
(B) **PTDF:** solve Lθ=p−A f0, L=A B Aᵀ, θ_ref=0. Then f=B Aᵀ L^+ (p−A f0)+f0, with a consistent connected-component generalised inverse.
(C) **Cycle:** A f=p and Cᵀ B^(−1)(f−f0)=0 for a basis C of ker(A); Cᵀ Aᵀ=0. The second condition states B^(-1)(f−f0)∈im(Aᵀ) because im(Aᵀ)=ker(A)⊥.

With **identical** topology, offsets, physical branches, sign/units, and injection mapping, (A)⇔(B)⇔(C) under projection to (f,p). The arbitrary slack angle changes θ by a constant but not f. If singular/islanded or b≤0, or if PTDF computed using a different base/offset, this proof does not apply. A *controllable DC-market link* m appears in A_K m in KCL and changes p injected into the physical network, but it is **not** included in the physical cycle space C or B; mixing spaces destroys the equivalence. With multiple connected components: enforce componentwise injection balance and reference or develop a separate qualified island model. PTDF/LODF for contingencies must be recalculated/validated, not mechanically reused.

### 3.3 Scenario replication / nonanticipativity (P: finite-dimensional isomorphism)
Shared formulation S uses x with U_c(x) and J(x,u)=C_inv(x)+Σw_c C_op,c(x,u_c). Replicated formulation R uses x_c with x_c=x_ref for each c and **exactly one** investment-cost term C_inv(x_ref) (or mathematically equivalent weighting with normalised w). Mapping T(x,u)=(x_c≡x,u) is a bijection between feasible sets after projection to x,u and preserves J. If any equality is omitted, replicated R contains infeasible-to-S decisions; it is generally a relaxation (B01). D2 invariance between years does **not** add equalities x_2035=x_2040=x_2050.

### 3.4 Storage state representations (P only for fixed E>0)
With fixed nonzero E, energy e_t∈[0,E] and normalised s_t=e_t/E∈[0,1] are bijective by e_t=E s_t; transition s_{t+1}=s_t+(η_ch p_ch Δt−p_dis Δt/η_dis−loss_t)/E preserves feasible physical dispatch. Mapping includes initial/end conditions and all time/case indices. When E=0 or E is endogenous, s=e/E may be undefined or induce bilinearity e=E s; naïvely using the same linear rows is not generally LP-equivalent. A power-only storage approximation without an energy state is a strict relaxation unless additional conditions are proven.

### 3.5 Stage transition (not proved; counterexample)
The three IoSN LP stages are not interchangeable with a joint model by default. B06 explicitly contrasts one **hypothetical** fixed Stage1 carry-forward with joint reoptimisation. Which transition mapping F is methodologically correct remains MD-07/TBD. This is a scientific **non-equivalence witness**, not a ruling that Stage1 must be fixed.

## 4. Multiple optima and robust comparison against false fails (B12)

Let P={ (x,y):0≤x,y≤1, x+y=1}, J=x+y. Every point in P is globally optimal, J*=1. The optimal *face* has a one-dimensional continuum. Projected total MW is fixed at 1, but x can range [0,1]. Hence:

1. Comparing scalar objective + feasibility + properly defined invariant total capacity can PASS in this exact fixture even when raw vectors differ.
2. Comparing x asset by asset and requiring exact identity would falsely FAIL two equally valid optimal portfolios.
3. If a genuinely approved reporting KPI distinguishes asset x from asset y, equality **cannot** be inferred from objective equality; report the attainable range [0,1], a declared tie-break, or a set-valued comparison.
4. If tools expose primal/dual solutions, reconstruct objective and bounds; a solver-reported "OPTIMAL" alone is not a certificate. Production absolute/scaled residual tolerances and ε-optimum definitions are MD-15/TBD.

Degeneracy may be detected analytically from a proven optimal face for the synthetic model; in a native LP, a bounded LP or sensitivity range at the verified optimum plus valid optimality evidence is a possible method. Sampling several solutions is **not** an exhaustive proof of the optimal set.

## 5. Epistemic classification / forbidden inference

|Evidence|Can support|Cannot support|
|---|---|---|
|Algebraic proof at explicit parameter assumptions|all-input equality over the *declared* domain|actual IoSN data eligibility, authority, unproved parameter mappings|
|Analytical scalar benchmark|check a narrowly stated mathematical oracle|all generated rows or general model equivalence|
|Synthetic script self-check|self-consistency and mutant sensitivity for a fixture|native tool implementation, numerical LP solver or G1 approval|
|One or more matching tool outputs|E-OBS for **tested** inputs and declared observations|E-FEAS and E-OPT over all decisions/inputs|
|Identical objective with distinct portfolios|possible degeneracy; further solution-set inspection|automatic inconsistency or automatic per-asset KPI equivalence|
|Generated constraints and validated bidirectional projection|E-FEAS for stated input/model families under proof conditions|an authorised methodology release, real network-quality tolerance|

**Open:** MD-02/-03/-04/-06/-07/-08/-09/-10/-12/-13/-15/-16/-17/-18/-19 (among others); O26 adoption AUTHORITY_UNCONFIRMED; G1 BLOCKED. No formal DSL, tool library, solver or approved acceptance epsilon has been chosen.
