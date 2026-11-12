# ML-C07 — Multiple Optima and Mathematical Equivalence Policy

**NONNORMATIVE SCIENTIFIC POLICY · 2026-11-12 · NO TWO-TOOL PROOF PERFORMED · G1 BLOCKED.** This research protocol aligns ML-C04 mathematical_equivalence_and_degeneracy.md (PR #45 head 256541e763147dcb118a3a9d24ca2f52035c672e), ML-C05 conformance_claim_rules.md (PR #44 head 1d1bfd18e92d457b415bbad54450bd5aec10963a) and ML-R04 mathematical_verification_rules.md inherited from R00 #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2.

## 1. Formal scope and vocabulary

For **the same frozen semantic input** d and variant s, let independently built tools A and B generate feasible sets F_A(d,s) and F_B(d,s) in possibly different native variable spaces. Let π_A and π_B be explicitly documented projections onto a shared, dimensionally consistent physical decision/observable space X (which may include year-specific investment, operations, flows and selected metrics). Let J_A and J_B be each model's objective after an **explicit source-approved conversion** to the same economic basis, and K the versioned defined KPI map.

Do not claim equivalence without declaring:
- exact input instance versus parameter family D and source/authority status;
- study year, CY/weather weights, UTC intervals, units and variable/candidate/corridor map;
- allowed technology/asset/stage and physical vs controllable-market-link roles;
- reference/slack angle, topology, offsets, conversion/discount and boundary-condition conventions;
- optional P15 predicate and whether comparison includes OPF;
- existence and attainability of optima, dual/primal and tolerance profile and map/proof validity domain.

A numerically equal reported cost on two different datasets is not E-OPT. The source release O26 draft and research D2 five-CY overlay must not be confused as authorised alternatives without an explicit owner decision.

## 2. Four distinct equivalence/observation propositions

| Relation | Exact scope-specific definition | Strong evidence | Common false inference |
|---|---|---|---|
| **E-FEAS** | π_A(F_A(d,s)) = π_B(F_B(d,s)) | Construct two-sided feasible lifting/elimination or sound proof of both inclusions, including bounds, stage/conditional guards and all relevant rows | Same solved optimum or row count proves identical feasible sets |
| **E-OPT-VALUE** | Correctly normalized minimum objective *values* agree for d,s to accepted accuracy | Independent feasible and sound bound/certificate checks with compatible monetary basis and optimality tolerances | Same solver status string or scalar KPI proves optimality |
| **E-OPT-SET** | Projected sets of globally optimal decisions coincide after objective-preserving mapping | E-FEAS plus objective correspondence (or direct solution-set proof) and correctly established optimum | One chosen optimizer pair proves optimal set equality |
| **E-OBS** | Precisely declared observation relation (same selected K, same set of attainable K over optima, or same certified range) | Independently replay K from E06/E07, verify formula and invariance/domain with stated solution selection | Identical dashboard means E-FEAS, or equal optimum forces identical KPI |
| **E-MULTI-INPUT** | Any above relation holds for every input in a *specified* parameter domain D | Quantified symbolic proof or sound exhaustive bounded discrete domain evaluation | Ten or fifteen synthetic fixtures generalize to all real IoSN cases |

E-FEAS alone does **not** prove E-OPT-SET without objective alignment. E-OPT-VALUE does **not** imply E-FEAS. Equality of one KPI value is usually much weaker than mathematical model equivalence. A report may state which of these relations is established, falsified or **unresolved**; no unqualified umbrella status “models equivalent” is permitted.

### 2.1 Valid change of objective basis

If both models have the same projected feasible set and J_B(x)=a J_A(x)+b for every corresponding feasible x, with a>0 and decision-independent b, they have the same minimiser set. They do **not** have equal raw objective values; E-OPT-VALUE requires reverse mapping to the authorised original currency/price-year/discount/Δt/CY basis and valid bounds. No discount rule, VoLL, price-year or tolerance is inferred from synthetic arithmetic.

### 2.2 Equal solutions by accident

A model missing a coupling or KVL row can return the *same* chosen optimizer as a correct model in a benign instance. Positive output agreement is therefore at most a bounded E-OBS observation. D3 native row/column inspection and targeted adversarial input are required, and D4 proof may be necessary to rule out an enlarged feasible set.

## 3. Equivalent formulation patterns and mandatory conditions

### 3.1 Shared investment across externally selected CY

A shared year-specific investment x_y with CY-specific operation u_yc may be represented as scenario-indexed x_yc plus equality constraints x_yc = x_y,CY1 for every c. A bidirectional feasible map exists if all copies have compatible bounds/candidate membership, operation couples to the correct copy, and CAPEX/operational scenario weights are mapped without duplication. Eliminating the equality constraints demonstrates projected E-FEAS for the declared linear model. **Omitting any necessary equality is generally a relaxation.** D2 says the weather weight *vector* is reused across 2035/2040/2050, **not** x_2035=x_2040=x_2050.

### 3.2 Physical DC mesh vs angle/PTDF/cycle

For an appropriately connected physical network with oriented incidence matrix A, nonzero correctly signed susceptance B, physical branch flows f, reference offset f0 and injection p, a conventional angle model has f = B Aᵀ θ + f0 and A f = p. Equivalent PTDF or cycle representations can be derived with a consistent reference, graph rank and offsets: the cycle representation satisfies A f = p and Cᵀ B⁻¹(f−f0)=0 for a valid basis C of ker(A). Proof assumptions must include component balances, sign/orientation, slack, no-load/PST and other offsets, topology and allowed network assets.

**Market-link candidates are separate:** their controllable flow affects KCL injection and directional NTC but is not inserted into the physical AC cycle-basis rows. If one tool incorrectly couples them to KVL, similar outputs on one instance cannot establish E-FEAS. Actual detailed-grid PTDF/LODF/N−1 equivalence also needs owner-qualified physical reference and cutoffs (MD-03/13/15 TBD).

### 3.3 Storage, sector coupling and stages

Fixed nonzero energy capacity E permits a mathematically valid mapping between state of charge in MWh and normalized SoC, but **E=0 or endogenous E** can invalidate naive division or introduce bilinearity. Correct SoC time boundaries, efficiency, case and carrier constraints are mandatory. P14 H2-load baseline must originate in its *pre-expansion* reference solve (B01-D072) and is not equivalent to the final portfolio dispatch. P10→P11 stage carry-forward F_y is open MD-07; no assumed joint optimization equivalence. P15 OPF is a conditional analysis, never a mandatory extension to all variants.

## 4. Multiple optimal portfolios — avoid false FAIL

Let F be a feasible decision set, J the approved objective, and X* = argmin_{x in F} J(x) the **set of all optimizers** (possibly an optimal face). If two independently solved models return x_A* and x_B* that are distinct but both map to feasible globally optimal decisions, difference of portfolio coordinates **alone** is not an error.

**Analytical illustrative example (B12/C07):** 0≤x_1,x_2≤1; x_1+x_2≥1; J=x_1+x_2. Optimal value is 1; both (1,0) and (0,1) are optimal and physically distinct alternatives. Total reinforcement x_1+x_2 is invariant (1), but an asset-specific K=x_1 spans [0,1]. Forcing the two tools to choose identical project IDs or K values would create a false FAIL. This is a synthetic example, **not** an adopted IoSN investment/priority rule.

### Valid handling of alternate optima

1. **Independently establish feasibility** of each native portfolio against its model and the accepted common scientific obligations; preserve unrounded E04/E05/E06.
2. **Independently establish optimality** of each specific instance using admissible primal/dual/bound reasoning; a solver status string alone is inadequate.
3. **Reconcile objective basis**, candidate IDs, investment quantity units, CY/year/stage and source lineage; compare correct objective values/intervals, not native row labels.
4. **Distinguish invariants**: an observable is invariant on X* only with a proof. For a linear KPI on a verified LP optimal face, one may (later) bound min/max K over that face with valid solver/certificates and accepted tolerances. Sampling a few optima is not a proof of the range.
5. **Report portfolio-specific KPI values** even if the objective is invariant; include a mathematically established range only if certified. Do not suppress a real KPI definition merely because it varies across optima.
6. **Tie-break only by contract**: no alphabetical, lexicographic, minimum-ID or arbitrary preference introduced by the verifier. A solver's internal implicit tie-break cannot be declared official.
7. **Classification**: a genuinely violated investment bound or nonanticipativity property can FAIL; a distinct valid optimum cannot FAIL solely on its difference; unresolved oracle/certificate yields BLOCKED, missing required feature UNSUPPORTED.

Near-optimal solutions under numerical tolerances are **not automatically mathematically optimal**. Any approved approximate-optimality policy must specify an objective interval, sound bounds and associated feasible portfolio/KPI uncertainty. Productive gap and feasibility thresholds remain TBD.

## 5. Triggered D4 and proof strategy

| Candidate SR / scope | Trigger | Minimum meaningful deep evidence |
|---|---|---|
| **SR-017** reduced electric network | Detailed-to-reduced physics/equivalent substitutions | Valid domain projection or source-qualified oracle; cut conservation insufficient |
| **SR-018** physical DC model | Angle vs PTDF vs cycle or changed slack/reference | Bidirectional graph-based projection with rank/offset assumptions and counterexample controls |
| **SR-019** N−1/reduction | LODF/PTDF/contingency mapping or material network simplification | Original-grid outage set and independent contingency feasibility/quality oracle |
| **SR-027** objective alternatives | Scaling, discount or weighted expected operating cost transformation | Term-by-term cost/units reconciliation, valid optimizer/optimum mapping |
| **SR-029** scenario investment | Single x versus equality-coupled replicated x_c | Two-sided feasible-set mapping, objective once and missing-equality negative mutant |
| **SR-035** candidate market-link | Candidate/physical classification, controllability, NTC versus physical KVL | KCL and directional bound mapping; proof of excluded physical KVL coupling |

Additional D4 escalations: material semantic loss in a converter, a mysterious KPI difference, unproved relaxation, changed candidate map, failed negative control, inconsistent physical/units projection and identical outputs despite a detected missing constraint. A D4-trigger candidate is **not** an assertion that the proof was performed.

**Hierarchy of possible evidence:** (A) logical counterexample directly falsifies a scoped proposition; (B) finite analytical synthetic oracle validates a limited fixture; (C) generated-model inspection validates named constraints of an actual instance; (D) bidirectional mathematical proof justifies a projection for a declared domain. Do not promote A/B/C to a universal result without an argument covering the missing quantifiers.

## 6. Cross-tool equivalence report fields

Each comparison record requires: A/B implementation/build/model IDs and **independence**, frozen contract and original/synthetic data tuple, study/CY/stage/mode, applicable source and open-owner state, model and objective/candidate map, equivalence proposition and quantified domain, proof/counterexample ID, native E04/E05/E06 observations, E07 formula authority and raw lineage, accepted numerical tolerance revision (or TBD), result as PROVED / FALSIFIED / OBSERVED_ONLY / UNRESOLVED **for this proposition**, reviewer and non-implications. These **equivalence report outcomes** are distinct from the six C05 atomic test statuses.

## 7. Non-goals and current status

No general robustness requirement, common solver, identical algebra, global simulator translation, lexicographic portfolio rule, official economic weights or full formal equivalence certification is introduced. ML-C07 provides a policy and reference hypotheses; **no native model, proof across two tools, optimality certificate, certified KPI range or productive tolerance was executed/accepted. G1 BLOCKED.**
