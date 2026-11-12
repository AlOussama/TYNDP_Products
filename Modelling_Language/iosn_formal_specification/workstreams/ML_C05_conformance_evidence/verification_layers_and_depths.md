# ML-C05 — Verification Layers V1–V6 and Risk-Based Depths D0–D4

**2026-11-12 · NONNORMATIVE RESEARCH DESIGN · ML-R00 baseline 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Orthogonal coordinates, not one verification ladder

Each proposed check is assigned a **verification subject** V1–V6, a **verification method/depth** D0–D4 and a **risk tier** A/B/C. None implies the others. V6 provenance accompanies each tested assertion; a V3 math check can depend on V1/V2 referential inputs, while V1 success is not a V3 result. A qualified reviewer must evaluate those dependencies before accepting a claim.

| Layer | Subject / principal obligation | Minimal independently inspectable evidence | Negative control and limitation |
|---|---|---|---|
| **V1 Data/schema** | Release and input manifest; IDs, units, time, axes, external five CY IDs and cross-year weights | E01/E02; original source-release references, file-byte hash, manifest, dimension audit, UTC intervals/Δt | Bad ID/unit/calendar fixture; passing a schema does not qualify actual source bytes |
| **V2 Domain semantics / preprocessing** | Required versus optional process flow; exogenous vs endogenous; physical branch vs market link; source→zone and frozen-profile transformation | E03/E04; mapping and balance, process/variant witness, producer identity | Candidate wrongly inserted as mesh branch or duplicated demand; necessary conservation not sufficient reduction fidelity |
| **V3 Generated mathematical problem** | Exact contract-relevant index sets, variable domains/bounds, objective components, coupling, Kirchhoff constraints and LP-stage rules | E04; typed row/variable/term exports, source/row crosswalk, rank/projection/omission evidence | Missing nonanticipativity, wrong objective weight, free KVL cycle; no uniform textual equation requirement |
| **V4 Numerical solution** | Primal constraints, dual/optimality evidence when claimed, gap, objective reconstruction and termination | E05; independent residuals and qualified bound/certificate | OPTIMAL label but nonzero KCL residual; feasibility of one solution not mathematical equivalence |
| **V5 Raw outputs / KPI** | Complete raw result preservation, output axes, independent Δt/weight aggregation, KPI formula revisions, needs versus projects | E06/E07; replayable raw results and independent formula computation | ENS unweighted, hidden filter, non-invariant portfolio KPI; matching totals not proof of correct LP |
| **V6 Evidence / review** | Version pinning, immutable traces, capability/support, six-state test ledger, independent review and exceptional decisions | E01–E08 and review register | Missing original-hash/reviewer; hash checks integrity only, review cannot be self-certified |

**Note on V3/V4:** A solver may return a feasible or optimal solution to a model that encodes the wrong feasible set. V4 PASS never compensates for V3 FAIL/BLOCKED. Conversely V3 structural PASS does not certify V4 numerical behaviour. V5 depends on **both** the raw output and an independently established KPI/oracle, not on the tool's own dashboard.

## 2. Verification depths and discriminating power

| Depth | What is examined | Example positive proof | False model it is able to catch | What it cannot justify |
|---|---|---|---|---|
| **D0 — Structure** | Registry completeness, IDs, syntactic type/schema, declared units and manifest references | All 48 SR and matching test/requirement references join | Missing mandatory SR, duplicate CY/key, absent E04 export | Correct coefficient signs, actual temporal physics |
| **D1 — Semantic** | Meaning, carrier/asset role, stage, optionality, scope and conservation domain | Candidate market link classified separately from physical branch | AC candidate added to KVL despite market-link obligation | Constraint generator really enforces declared semantics |
| **D2 — Synthetic/analytical** | Exact small numerical oracle, metamorphic or negative-mutation test; dimensions and scaling | Two-node KCL, weighted ENS arithmetic, energy conservation with Δt | Omitted weight, wrong unit, altered cut flow on chosen fixture | General feasible-set identity; actual grid/owner cutoff |
| **D3 — Generated obligation inspection** | Independently reconstruct variable indices, bounds, rows, offsets, objective coefficients and absence/presence of required families | Shared x over CY or copies with enforced equalities; inspected coupling rows | Hidden CY-specific free investment, missing KVL, erroneous OPF cap, wrong stage allowlist | Full all-parameter mathematical equivalence without additional proof |
| **D4 — Deep equivalence / projection** | Symbolic algebra, elimination, rank/nullspace, bidirectional projection, exhaustive finite test *only for finite domains*, counterexample search and perturbation study | Prove angle and PTDF DC feasible projections equal under stated rank/reference conditions | Relaxations or restrictions with same sampled optimum, wrong formulation under other data | Universal proof from finite samples; release without source-specific assumptions |

Depths are **cumulative in evidence intent**, not necessarily chronological or implemented as the same programme. A D4 mathematical proof may use earlier independently documented mappings, and an algebraic derivation may replace brute-force enumeration. If a D2 test is incapable of detecting a targeted mutant, its detection coverage is **open**, not PASS on the property.

### Why D5-A1 matters

**Project decision D5-A1** requires risk-based scientific verification. A blanket one-to-one syntax comparison across PyPSA, Antares, Sienna or other tools is neither necessary nor sufficient. Equivalent formulations may eliminate slack variables, scale rows, introduce auxiliaries, or use angles versus PTDF while preserving the declared observable feasible projection. Deep D4 is triggered by relevant semantic risk; it is not mandated for each of 48 requirements.

**Notation collision prevention:** Project decision **D4 = UTC/time and units**. Test depth **D4 = deep equivalence**. These identifiers must be typed and never compared or mapped using the naked string D4.

## 3. Research risk tiers and 48-SR coverage

ML-R04's **proposed**, not approved, tiering is preserved verbatim as a risk assignment: **A=33, B=12, C=3**. The source is requirements_verification_matrix.csv, with all **48** active provisional SR IDs, sparse numbering (there is no SR-012 or SR-049), and a test for each SR. Neither tier nor priority implies a passing test.

| Tier | Minimum science programme when applicable | Escalation |
|---|---|---|
| **A — critical** | D0 + D1, applicable D2 analytic/mutation, D3 where a generated mathematical obligation exists, V6 all along | D4 on triggered high-consequence equivalence uncertainty; model generator evidence required for equation claims |
| **B — significant** | D0 + D1, D2 if numerical evidence is needed, D3 if an actual generator obligation applies; V6 | Raise to A/D3/D4 if the observed failure could evade output comparisons |
| **C — controlled** | D0 + D1 + V6 and negative structural checks | Still mandatory where applicable; low risk is not NOT_APPLICABLE |

The per-SR minimum depths/levels in the original 48-row matrix remain the controlling **research proposals**; the table above is guidance, not a substitute. SR-036 and SR-038, for example, have specific D3 obligations despite B tier. In each case, declare the check's exact assertion, no broad 'tier A PASS' statement.

### Proposed D4 triggers, not six automatic full-model proofs

| SR | Specific equivalence question | Minimum D4 strategy (research candidate) | Missing actual reference |
|---|---|---|---|
| **017** | Reduced impedance/reference flow retains intended interzonal electrical response | Establish boundary injections, reduce/eliminate internal nodes and compare projected flows over stated reference set | Original detailed network, reduction method/oracle, MD-03/15 |
| **018** | Angle, PTDF and cycle DC representations encode same physical mesh | Choose slack/reference, map offsets, derive both directions or exhibit rank/cycle witness | Accepted DC conventions and tolerance MD-15 |
| **019** | LODF/N−1 reduced-grid bounds represent prescribed contingencies | Case-indexed outage/cut projection plus security-capacity comparisons | Outage set, detailed grid, rating oracle MD-03 |
| **027** | Objective transformations preserve investment/operation cost semantics | Expand scenario/time/discount terms by unit, check affine/positive scaling and argmin implications | Final economic/discount policy MD-02/15 |
| **029** | Shared x versus scenario copies + equalities have identical investment projection | Eliminate copies, prove bidirectional feasible lifting and objective weight mapping | Scope-specific variable/candidate maps; MD-15 |
| **035** | Market-link candidate not incorrectly coupled to physical KVL mesh | Counterexample to AC-cycle model, show KCL and directional NTC projection with link role | Candidate/physical mapping MD-09/15 |

**Additional evidence-triggering events:** unexplained KPI divergence, changed candidate mapping, arbitrary relaxation, altered row family or indexing, unknown sign/offset convention, numerical agreement despite failed negative mutation, model conversion with unproven semantic loss, or divergent predictions on perturbed inputs. The escalation requires a written trigger record, hypothesis, proof object/counterexample and review, and may be unresolved/TBD.

## 4. Mathematical criticality and minimum evidence combinations

| Obligation family | Relevant SR | Why a sole final-KPI check is inadequate | Proposed independent check |
|---|---|---|---|
| Multi-CY investment | 027, 029, 030 | Scenario-dependent investment can achieve plausible/lower cost | D2 wrong mutant + D3 index/bounds/constraint witness, D4 when formulation substitution |
| DC physical/market separation | 018, 024, 028, 035, 036 | KCL can pass with free physical cycle; KVL can be wrongly added to market link | D2 network cycle + D3 typed KCL/KVL/NTC rows, D4 projection when needed |
| Expansion stages/conditional OPF | 003, 026, 031, 032, 033 | Final portfolio can hide forbidden candidates or carry-forward errors | D1 variant/stage trace + D3 candidate and capacity/cost crosswalk |
| Reduction and contingencies | 015–023 | Cut-flow preservation is only necessary | D2 balance + D3 parameter provenance + triggered D4 and detailed-network reference |
| Sectors and flexibility | 007–009, 034, 041, 042, 050 | A common objective may conceal H2 basis, SOC or double-count errors | D2 analytic carrier/time fixture + D3 equations and source version |
| Economics and reporting | 001, 022, 025, 027, 043–046 | Same total can mask wrong discount, weights, threshold or KPI definition | D2 dimensional arithmetic + D3 objective terms + V5 independent KPI replay |
| Time/weather/source | 002, 004, 010, 011, 039, 040 | Undocumented input mismatch can invalidate otherwise correct solver result | V1 source manifest; D0/D1 axes and nonuniform cross-year weight vector; MD-12 open |

The remaining specific SR-005/006, 013/014, 020/021, 037/038, 047/048 all have independent matrix assertions (see verification_status_test_cases.md); no SR is excused by not appearing in this thematic overview.

## 5. Oracle and tolerance discipline

An evidence object must distinguish: **(a)** known arithmetic/physical identity under declared assumptions, **(b)** research fixture with synthetic numbers, **(c)** unapproved draft source formula, **(d)** accepted authoritative method- and data-specific oracle. Numerical cutoffs for RMSE/LODF, gap/feasibility, conversion/weight normalisation, discount, filtering and calendar acceptance remain **TBD** (not implicit default 1e-6). Record native solver tolerances as observations separately from independently approved acceptance thresholds.

For a primal candidate, evaluate original native bounds and signed rows with explicit units and normalised residuals. For an optimality claim, obtain a sound dual/lower-bound certificate or other justified method; neither zero-looking primal residual nor solver status string establishes optimality. Retain solver infeasible/unbounded/error diagnostics and source/equation uncertainty as different failure causes.

## 6. Layer-by-depth assessment matrix

Each cell is an admissible *method*, not a mandatory test count.

| | D0 | D1 | D2 | D3 | D4 |
|---|---|---|---|---|---|
| V1 | Keys, provenance fields | source/time/unit interpretation | synthetic Δt/CY negative check | generated data index checks if material | formal alignment only if axis mapping is contested |
| V2 | typed semantic identifiers | branch/role/process | conserved transform examples | source→row family tracing | transform preservation/projection |
| V3 | variable/row inventory | constraint-role semantics | analytic LP mutants | coefficients/bounds/omissions | feasible/optimal projection proof |
| V4 | statuses/fields present | solver termination meaning | residual analytic fixture | matrix–solution residual reconstruction | model-proof/dual-certificate scrutiny as needed |
| V5 | raw/derived distinct | KPI formula and unit meaning | independent weighted replay | source→generated objective/output bridge | invariance bounds over multiple optimal solutions |
| V6 | identity and schema | trust/authority/independence | tamper and stale-evidence mutants | generator trace completeness | proof provenance and qualified review |

## 7. Acceptance limits

This work defines **proposed acceptance evidence**, not an approved acceptance policy. With unqualified original data, an unauthorised source profile or TBD numerical oracles, scoped scientific/profile acceptance remains BLOCKED even if bounded synthetic checks succeed. Inherited tool-run status for all 48 SR is **NOT_EXECUTED**; this document reports no actual D3 model inspection or D4 proof for a production IoSN implementation.

**Cross-references:** ML-R04 verification_architecture.md, risk_based_conformance_policy.md, mathematical_verification_rules.md; ML-R00 cross_workstream_consistency_review.md (INT-01/02/06/10/15).
