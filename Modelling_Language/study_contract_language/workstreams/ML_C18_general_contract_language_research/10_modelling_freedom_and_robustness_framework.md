# ML-C18 / 10 – Preservation of Modelling Freedom & Multi-Model Robustness Framework

**Status:** versioned non-normative research protocol, K02–K09 gate-critical; 2026-11-20, ML-C18 baseline research-r1. No claim of robust scientific results or validated multi-tool conformance.

## 1 Definitions and formal separation
A `StudyContract C` fixes a *scientific question*, valid datasets/scenarios and source-controlled boundary. Its `component contracts` define external ports (carrier, sign, unit, time), environment assumptions A, guarantees G and required capabilities/services. Implementations `M_i` may choose different internal mathematics. `C` defines obligations and allowed variation policies, not a single optimal model.

For fixed data `D`, scope `S`, and observation map `π_i`, a safety conformance condition is `∀h ∈ Traces(M_i,D,A,S): π_i(h) ∈ Allowed(C,D,S)`. Capability obligations additionally require existence of feasible witnesses that deliver contracted services under specified demands; otherwise the trivial never-operate model would pass. A feasible set need not equal another feasible set unless the contract *requires* equivalence. Scientific validity (right model of reality) is separately evaluated using independent empirical evidence; it does not follow from syntax, feasibility, optimality or inter-model agreement.

**Implementation freedom partition:**
- `REQUIRED`/ `PROHIBITED`: must satisfy or reject.
- `PERMITTED`: explicitly permitted choices (e.g. distinct energy-state coordinates, alternative loss methods *if* corresponding guarantee still passes).
- `IMPLEMENTATION_DEFINED`: choice not prescribed but disclosed with reason/impact, for instance solver/algorithm and chosen abstraction.
- `CONDITIONAL`: guard on obligation, with TRUE/FALSE/UNKNOWN semantics; unknown can block conformance judgement.
- `OWNER_TBD`: genuinely unresolved contractual value; its absence is not consent or a default.
Alternative minimal abstract syntax `Rule(effect,guard,scope)` + `VariationPolicy(choice/disclosure)` + `DecisionStatus`. Test semantics by mutation, not merely by counting constructs.

## 2 Distinguish R1–R4 and the appropriate oracles
| Layer | What changes | What is held fixed | Legitimate checks | False claim to avoid |
|---|---|---|---|---|
| R1 Numerical / Solver | solver, tolerances, algorithms, floating point | identical model data and mathematical formulation | primal/dual residuals, objective tolerance, feasibility, degeneracy and integrality | equal objective implies identical primal solution |
| R2 Independent Implementation | code path and optionally algebraically equivalent formulation | same feasible set/objective under proven mapping; study data | algebraic equivalence assumptions + mapped feasible set + objective, residuals, optima set | identical samples prove mathematical equivalence |
| R3 Structural Model | degree of aggregation, physics, cost model, temporal granularity | common **outer contract**, allowed variation set and comparison frame | individually required A/G, trace witnesses, outputs' distributions/rankings, attribution | different outcomes mean nonconformance |
| R4 Study Conclusion | cross-model, cross-scenario, data, alternate assumptions | explicit decision question, reported domain of variation, KPI definitions | ranking stability, threshold crossings, sign and decision-set robustness, model-family sensitivity | low spread proves truth / scientific accuracy |

**Mathematical equivalence evidence** can be algebraic derivation, independent formulation mapping, bijective feasible-set/projection proof under stated assumptions, relaxation-bound analysis, or case-specific analytical invariants. In RC05 lossless, connected fixed-topology DC network, angles/cycle/PTDF can produce identical physical line flows when susceptance/slack/phase-shift/base mapping match; this is not an AC or N-1 equivalence claim. **Permitted non-equivalence** means both independently fulfill C but differ in modeling outcomes, with design-difference declaration; it is **not** evidence of same feasible set. **Unproven equivalence** receives `UNPROVEN`, not `EQUIVALENT`.

## 3 Independent Implementation / Variations Register
Minimal per model:
`implementation_id, repository_commit, team, author_lineage, code_dependency_graph, parent_model, language_engine_solver_version, data_hash, parameter_hash, study_contract_sha, method_profile, mathematical_profile, scenario_set, boundaries, discretization, aggregation, loss_model, available_output_observables, known_limitations, exceptions, solver_config, results_hash, evidence_uri`.

**Independence levels:** I0 same executable, I1 copied/translated shared model/library, I2 independently coded from shared mathspec/Library (R2 more plausible than R3), I3 independently designed internal math but same external contract, I4 external group audit of assumptions/provenance (not automatically full scientific independence). These are research labels, not quality verdicts. Two different engines consuming the same formulation do **not** establish independent model assumptions. Shared upstream loads, costs, data preprocessing, topology reduction, libraries and tests create correlated failure modes; register them.

## 4 Common results contract
Every comparable observation must declare:
- `observable_id`, meaning/quantity, `unit`, carrier, sign, geographic entity, base/nominal/year currency, and source definition; *reference role* base/project and `variant_id`.
- Time domain, `Δt`, calendar and timezone if relevant, sampling and missing-data policy, aggregation operator and weights `w_s`, whether annualization or representative-day scaling applied.
- Fixed vs endogenous decisions, information availability and nonanticipativity; reserve / N-1 / adequacy assumption if KPI relies on it.
- Economic boundaries: whether objective vs total-system-cost KPI, CAPEX annualization, residual value, discount/base year, fuel/CO2 tax and transfer conventions. Avoid comparing incomparable objective values.
- Observable projection `π_i` from native output to shared KPI and its validation/oracle; `COMPLETE/PARTIAL/UNAVAILABLE` reporting; no fabricated zero.
- Conformance outcome with `PASS/FAIL/BLOCKED/UNSUPPORTED/NOT_EXECUTED/NOT_APPLICABLE` plus level E0–E5; no arbitrary tolerance after seeing results.
- Loss of semantics on export: `source_property_id -> target_fields -> reconstruction -> equality predicate`. If unmatched, `LOSSY` and precisely list what is dropped.

## 5 Operational comparison design and metrics
**Pre-registration is mandatory for a defensible robustness experiment**: case IDs, variants, model inclusion/exclusion, input identities, common units/outputs, acceptance thresholds, missing/failed runs, tolerance sensitivity, and decision rule fixed before inspecting results.

For model `i` and scenario `s`, `y_{i,s}` is comparable only after eligibility/conformance. If `n_s` eligible models:
- Numeric **range** `R_s=max_i(y_{i,s})-min_i(y_{i,s})`; use only alongside scale/relative spread and eligibility count, not as an accuracy score.
- **Relative dispersion** `R_s / max(ε, |median_i(y_{i,s})|)` with report of ε/unit; for zero-crossing signed indicators prefer absolute physically meaningful tolerance.
- **Rank concordance:** Kendall tau_b (tie-aware) or pairwise rank violation probability for measure ordering; report ambiguous near-tie alternatives and metric-specific thresholds.
- **Sign/threshold robustness:** fraction of eligible models agreeing on `Δ benefit > 0` or safety threshold, with n and model family; highlight decision reversal and robust-dominance sets.
- **Structure sensitivity:** grouped contrasts between policy-allowed model families under same common data; report within-family spread and between-family shifts. Do not misinterpret as unbiased variance component with n=2 or correlated implementations.
- **Data/assumption sensitivity:** factorial or controlled one-factor perturbations, distinct from R3 structure variation; record interactions and explain effects.
- **Component compliance:** numerator eligible case/obligation combinations passing conformance against denominator applicable tests; unexecuted and blocked are kept separate, not counted as pass/fail by omission.
- **Unexplained divergences:** proportion of material output differences without traced assumptions/structure/data/execution explanation, with hard 'unexplained' register.
- **Multi-optimum selection:** record objective gap and primal solution variability; compare invariant decision properties or the set of optimal possible outcomes, not just one arbitrary solver-selected optimum.

**Thresholds are not defaulted.** Per-KPI tolerance and decision margin are source-/Owner-bound or transparent nonnormative research assumptions. With tiny biased model portfolios, spread is descriptive, not a frequentist CI on true uncertainty.

## 6 Suggested independent research protocol for RC10
1. Freeze `C`, SLR/K baseline, profile, canonical scenarios/input hashes, comparison observable schema, intended model families; check no owner-dependent missing rule is silently filled.
2. Model A and B independently map external ports, guarantees and observables. Document variable/state representation and assumption delta, plus team/shared-dependency graph.
3. Execute formal semantic/static checks (units, carrier, sign, timing, source identity) separately from native parser, feasibility, scientific model evidence. Mark `NOT_EXECUTED` where absent.
4. Pair R1 (same mathematical model different solver) and R2 (independent equivalent) runs; compare residuals and output within preregistered tolerances. Where proof absent, call R2 `hypothesized`, not established.
5. R3 compare different structures only if both individually conform. Record systematic tradeoffs (e.g. individual EV vs justified fleet envelope, H2 efficiency alternative).
6. R4 compare policy alternatives against predeclared decision threshold across model families + scenarios; identify flips, dominance and tradeoffs. Test common-error sensitivity with an independently sourced challenge dataset/assumption.
7. Publish input/data/solver/implementation metadata and all failed/missing runs; assess whether contract conclusions are stable **within the declared scope**. Never certify model truth from agreement.

## 7 Specific failure classes and negative checks
| Error | Conformance classification | Robustness disposition |
|---|---|---|
| Battery creates net MWh in required energy ledger | FAILED_OBLIGATION | exclude from legitimate R3 sample; report separate failure |
| V2G exported but `PROHIBITED` | FAILED_POLICY | exclude or mark distinct nonconformant stratum |
| Model has allowed efficiency approximation, emits different costs | PERMITTED_NON_EQUIVALENCE if witness confirms | retain R3, explain through structural choice |
| Same math, different solver picks another equally optimal unit | CONFORMANT, MULTIPLE_OPTIMA | compare optimal set / interval / decision stability |
| Wrong currency-year or demand scenario | INCOMPARABLE | harmonize/re-run; cannot count as structural uncertainty |
| Assumption owner TBD | BLOCKED / UNKNOWN | no positive conformance claim |
| All models share one wrong constraint assumption | MAY_PASS_INTERNAL_CONFORMANCE; SCIENTIFIC_VALIDITY_OPEN | adversarial external data/method review required |

## 8 Reuse boundary by candidate
- GEMS: Port graphs, modular libraries and Views help *build and observe* runs; if requiring identical libraries, R3 diversity collapses. A separate outer Contract can classify and validate two different libraries.
- mathspec: Formal operator/name/dimension semantics and deterministic Program reduce implementation ambiguity for **one mathspec formulation**, facilitate R1/R2; R3 requires multiple mathspec Specs plus shared outer Contract.
- ML-C17: Source/Requirement/Scope/Data/Process/Result/Evidence/Unknown are foundations for the outer contract, but native multi-model comparison, precise typed behaviour and validation remain absent.
Each capability needs a version-pinned adaptor and tested negative witness before reuse can be called implementation-level.

## 9 Power-Agent / QA traceability
PowerSkills `pypsa` and `operations-planning-mitigation` at Power-Agent/PowerSkills main SHA `636102954ff9522e7b161cbb2e3863746afa78cc` support the research sequencing: inspect network and data, DC screening before AC, do not declare infeasible before checking inputs, distinguish OPF from AC voltage/reactive validation. These are *engineering playbooks*, not a substitute for native model tests or a normative Contract. The separately referenced Power QA Question Answers knowledge base could not be identified by an accessible versioned file/repository in this session; its contents are **NOT_EVALUATED**, not silently reproduced.

## 10 Non-goals / evidence
No independent multi-model run or actual study-result distribution has been computed in ML-C18. Numerical microchecks for ten RCs are documented separately as **synthetic** and cannot establish R1–R4 empirical robustness. `G1=BLOCKED`; decisions D1–D6 unchanged.