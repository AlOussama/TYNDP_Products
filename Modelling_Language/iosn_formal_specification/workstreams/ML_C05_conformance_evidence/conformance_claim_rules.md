# ML-C05 — Bounded Conformance Claim Rules and Mathematical Equivalence

**2026-11-12 · NONNORMATIVE SCIENTIFIC RESEARCH · ML-R00 commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Claims are typed propositions with explicit scope

An assertion's **PASS** is not automatically a conformance claim. Every proposed claim must carry:

1. **claim type and strength** (e.g. structure, data, semantics, mathematics, numerical, KPI, evidence, equivalence or full profile);
2. **target identity** (tool implementation/build/model generator, model instance/run, solver version and any candidate mapping);
3. **normative/research basis** (contract/source release ID, clause/48-SR baseline revision, D1–D6 research profile, authorisation state, open MD/CL);
4. **quantifiers and applicability** (which y, CY, UTC intervals, carriers, assets, process/stages and optional P15 branch; *one fixture* versus *all parameters* must not be conflated);
5. **required assertions** (explicit SR/Test IDs, V-layers, D-depths, risk tier, oracle and tolerance profile, accepted exclusions with proof);
6. **proof boundary** (executed evidence E01–E08, direct counterexamples, completeness/quality, expected numerical error, qualified review);
7. **status and caveats** (record the six-state test vector plus independent source/data/model/review/gate states, current/stale condition);
8. **negative statements** (what the claim specifically does *not* establish).

A claim is inadmissible if any mandatory relevant item is silently omitted, if a tool's own claims are substituted for evidence, or if actual original source data are labelled qualified without original-byte verification.

## 2. Claim taxonomy and preconditions

| Proposed claim label | Minimum logical basis | Proper conclusion | Cannot conclude |
|---|---|---|---|
| **C-STRUCT** | Scoped D0 schema/ID assertions actually run, E01/E02/E08 | Specific structural properties on specified artifacts | Adopted methodology, correct maths or source qualification |
| **C-DATA** | V1 + applicable V2/E02–E03 checks, original data access/identity, actual qualification policy, V6 | Named consumed inputs qualified for exact scope **if owner actually authorises them** | Generated LP or KPI correctness |
| **C-SEMANTIC** | V2, selected V3 plus authoritative contract interpretation and applicable D1–D3 observations, V6 | Specific domain/process semantics implemented | All mathematical feasible sets equal |
| **C-MATH-PROPERTY** | V3 + applicable D2/D3, triggered D4 if material, accepted oracle E04, V6 | Named generated mathematical invariant/formulation obligations satisfied under assumptions | Global equivalence or solver optimality |
| **C-NUMERIC-INSTANCE** | V4/E05, identified generated model, independent primal/dual/objective/bound checks with accepted tolerance, V6 | Feasibility and/or optimality for **one instance**, with precise certificate strength | Valid semantic LP, convergence for all other runs |
| **C-RESULT-KPI** | V5/E06–E07, approved versioned KPI, full raw lineage, independent replay and V6 | Exact specified observable correct for declared run/portfolio | Same KPI for every alternate optimum or tool |
| **C-EVIDENCE** | V6 graph closure, authenticity, integrity, independence and review qualified *for this claim* | Dossier satisfies specified evidence criteria | Correct mathematics merely because documentation is complete |
| **C-EQUIV-FEAS/OPT/OBS** | Scoped equivalence proof or approved bounded empirical observations (see §3) | Precise mathematical/result relation, with quantifiers | Unrestricted general equality beyond projection/input domain |
| **C-FULL-PROFILE** | All applicable mandatory SR obligations proved at needed depths, required authority/data/oracles, independent review + explicit owner decision | A later **scoped, governed** conformance conclusion only if genuinely authorised | Automatic tool certification or automatic G1 approval |

A single C-NUMERIC-INSTANCE may specify PRIMAL_FEASIBLE without claiming OPTIMAL. A synthetic fixture with independent arithmetic can yield a **C-STRUCT-RESEARCH** or **C-MATH-PROPERTY-RESEARCH** *only within the explicitly declared synthetic scope* and without claiming a productive contract result. No productive C-FULL-PROFILE is presently reachable.

### Evidence-backed claim rule

~~~text
candidate_claim(C):
  enumerate applicable obligation universe U(C), validated optional exclusions X(C)
  require full trace E01..E08 as relevant, and all per-assertion statuses visible
  reject/w ithhold if unexecuted, failed, unsupported or blocked mandatory assertion
  reject if required oracle, data authority, reviewer independence or tolerance unresolved
  if every property proven:
      issue only the named scope-limited proposition with proof/review provenance
  never issue owner approval, methodology adoption, certification or G1 GO automatically
~~~

(The 'reject/withhold' phrase is a claim eligibility decision, **not** an invented seventh test status.)

## 3. Mathematical equivalence relations: do not collapse them

Let implementations A and B, for the **same frozen and semantically mapped input instance** d, have feasible sets F_A(d) and F_B(d) in potentially different native variable spaces. Let pi_A, pi_B project onto the *declared common observable decision space* X (physical flows, valid investments, operation or selected balance variables). Let J_A, J_B be objective functions mapped to a declared common monetary/unit basis, and K a chosen KPI function.

| Relation | Formal meaning | Adequate research proof | Insufficient evidence |
|---|---|---|---|
| **E-FEAS** | pi_A(F_A(d)) = pi_B(F_B(d)) under explicit model/data maps | Bidirectional feasible lifting/elimination, rank/cycle argument, complete symbolic reduction or a sound finite-domain proof under stated assumptions | Same optimal objective; same solver solution; sampled dispatch |
| **E-OPT-VALUE** *(weak)* | min J_A(d) and min J_B(d) agree within an **approved** tolerance/basis | Independently certified optimal values/bounds for identified instance d | Equality of optimizer sets, feasible sets, or KPI |
| **E-OPT-SET** *(stronger)* | Mapped optimal-solution projections are equal and objective scale/basis is reconciled | Prove objective-preserving mapping plus optimality correspondence; investigate degeneracy | One matching optimizer pair or one equal reported cost |
| **E-OBS** | Selected observable/KPI K has equal value or certified range under stated runs/solution selections | Independent KPI replay; projection and mapping; invariance proof if claiming equality for all optima | Same feasible set, equal portfolios, exact mathematical equivalence |
| **E-MULTI-INPUT** | A preceding equivalence relation holds over a precisely bounded parameter family D | Symbolic quantified proof or justified verified exhaustive finite family | Ten synthetic cases generalised to all IoSN scenarios |

**Strict logic:** E-FEAS does not alone imply E-OPT-SET without objective mapping. E-OPT-VALUE does not imply E-FEAS, nor equal optimizer sets. E-OBS is a chosen observable relation and can coexist with inconsistent constraints. Different native indexing or candidate IDs do not invalidate a valid mapping, while identical ID strings do not prove the same meaning.

### Feasible-set example: shared investment across weather cases

A model with a single first-stage x_i and a model with copies x_i,c constrained by x_i,c = x_i,CY1 for all c can have the same projected investment feasible set and objective, **if** all relevant bounds, scenario costs and links are mapped. Eliminating equality-constrained copies supports E-FEAS. Removing the equalities makes an inadmissible relaxation even if one synthetic optimum happens to choose equal investments. D3 requires the equality rows or shared-index proof; D4 can establish the projection.

### DC network example: angles versus PTDF

Angle-flow, PTDF-flow and cycle-based models may be equivalent **only under** compatible connectedness/reference, susceptance/rank, phase-shifter/offset, orientation and treatment of physical branches. A market-link transmission candidate is not silently placed in the AC KVL subspace: it participates in KCL and controllable directional NTC but need not obey physical cycle equations. Identical KCL objective values on one network fixture do not prove E-FEAS. Original detailed-grid PTDF/LODF/N−1 reduction oracles and acceptance cutoffs remain TBD.

### Objective example: positive affine transforms

A positive rescaling J_B=a J_A+b with a>0 and decision-independent b preserves argmin *for identical feasible set*, but not equal **objective values** or monetary accounting unless conversion back to the same cost basis is demonstrated. Scenario weights, Δt, VoLL and price-year/discount cannot be silently dropped as common constants. Productive economic oracles remain MD-02/15/TBD.

## 4. Multiple optima — portfolio and KPI semantics

With degeneracy, let X*(d) denote the set of feasible optimal projected outcomes. Two independent solvers may return x_A* ≠ x_B* even if both have valid optimality certificates and fulfil the same semantic constraints. **Do not FAIL merely because candidate IDs or portfolio vectors differ.**

Valid scoped checks are:

1. independently establish primal feasibility for each returned portfolio and compatible certified optimality **within approved tolerances**;
2. verify identical input/data/profile and compatible projection of physical quantities, not textual candidate labels;
3. compare an **objective value or interval** after correct cost/annualisation normalisation;
4. compare **invariant** KPI properties only if established constant across X*(d); otherwise evaluate portfolio-specific KPI values independently and report a *range over optimal solutions* only if that range has actually been bounded/proven;
5. use additional tie-breaking only if the contract explicitly includes such a rule. No artificial ID ordering or lexicographic preference may be invented by the verifier.

**Illustrative synthetic fixture:** Two equivalent zero-cost reinforcement options A and B each cover a need of one capacity unit; an objective minimises x_A+x_B subject to x_A+x_B≥1 and bounds [0,1]. Both (1,0) and (0,1) have objective 1. If a later (approved) KPI measures 'MW on project A', its value is not invariant (0 vs 1) despite identical optimum. A project-ID mismatch here is not an error; a claim of equality of *this KPI* would be invalid. This illustrates mathematical degeneracy only and is **not** an IoSN investment specification.

## 5. Result and KPI claim rules

- **Raw versus derived:** E06 stores original unfiltred decisions, E07 records named formula, version, accepted owner/oracle, exact raw parent and independent evaluation.
- **Weighted outputs:** energy expectation must use real declared w(c) and Δt. Never assume uniform CY weights or a one-hour step absent source evidence.
- **Metric undefined:** formula/status FORMULA_TBD is separate from a test's BLOCKED outcome; return a null/undefined value and preserved raw lineage, not a manufactured zero.
- **Filtering and system need:** small-investment threshold, ONDP/offshore, candidate route cost and approved project status must be separately sourced; a system-need opportunity cannot be relabelled as construction approval.
- **Numerics:** if a test depends on unresolved feasibility, objective-gap or RMSE thresholds, withhold its accepted PASS while retaining unrounded diagnostic evidence; solver-native tolerances are not owner thresholds.
- **Non-invariants:** different feasible optimum portfolios may have different congestion, investment and project-specific KPIs; report exactly which observables are invariant and how verified.

## 6. Counterclaims and falsifiers

| Incorrect conformance statement | Counterexample / missing proof |
|---|---|
| 'Tool A and B returned the same objective, so both models conform.' | B lacks KVL or scenario investment coupling; same sampled optimum is possible |
| 'No missing required feature since OPF is optional.' | P15 invoked ⇒ SR-026 cap mandatory; unsupported means UNSUPPORTED |
| 'Both are optimal, therefore individual investment rows must match.' | Alternative optima with nonunique portfolios |
| 'Passing structural JSON plus E04 label proves model mathematics.' | Semantic label can point to wrong/missing row/variable; inspect coefficients/domains |
| 'The negative mutant was rejected, therefore the productive model conforms.' | Test sensitivity is not execution against productive model/input |
| 'Successful R04-C05 proves network-reduction equivalence.' | Cut conservation alone does not verify PTDF/LODF/N−1 or original grid |
| 'All 48 planned test entries are PASS.' | Inherited 48 tool-run statuses are NOT_EXECUTED; no actual model run |
| 'Independently computed dashboard KPI establishes G1 GO.' | Methodology/data/oracle/reviewer and formal gate authority absent |

## 7. Claim maturity and governance

Current ML-C05 work can publish **hypotheses and rules for future claims**. A future qualified independent reviewer may approve a scoped scientific claim only on complete, authoritative evidence; separate Methodology/Data/Gate Owners retain their decisions. A research author may report a structural coverage check but cannot convert it into independent assurance. **G1 stays BLOCKED.**

**Sources:** ML-R04 mathematical_verification_rules.md (E-FEAS, E-OPT, E-OBS), risk_based_conformance_policy.md, failure_and_evidence_semantics.md; ML-R00 INT-01/03/06/10/12; ML-R02 architecture alternatives.
