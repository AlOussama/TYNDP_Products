# ML-C07 — Failure Classification and Pilot Stop Conditions

**DESIGN ONLY · NONNORMATIVE · 2026-11-12 · G1 BLOCKED.** Rules adapt the six-state ML-C05 applicability_and_failure_state_machine.md (PR #44, head 1d1bfd18e92d457b415bbad54450bd5aec10963a) to a *future* independently implemented two-arm experiment. No actual Tool A/B failure, test PASS, review approval or source qualification is reported by this document.

## 1. Separate four different outcome planes

1. **Atomic assertion outcome**: exactly one of PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_EXECUTED, NOT_APPLICABLE *for a scoped test*, determined with evidence, applicability, capacity and oracle status. No additional status is invented.
2. **Tool feature capability**: SUPPORTED, EQUIVALENT_WITH_EVIDENCE, UNSUPPORTED, NOT_ASSESSED plus named semantic loss; assessed on tool/build/implementation scope.
3. **Pilot execution control**: CONTINUE, HOLD_AFFECTED_SCOPE, STOP_PHASE, REBASE_AND_RERUN, or INVALID_COMPARISON; these are coordinator process actions, **not** six-state test verdicts or governance approval.
4. **Source/data/authority/claim readiness**: independent release/oracle/reviewer/MD/CL gates and G1 state; an atomic PASS cannot make G1 GO.

Retain root cause, scope class, target role (IMPLEMENTATION_UNDER_TEST vs NEGATIVE_MUTANT), actual attempted execution, evidence digests, reviewer, mutable-current pointer and immutable historical attempts. An invalid or missing attempt must never be silently represented as PASS.

## 2. C05 atomic status decision semantics

| Test status | Preconditions and required witness | Misclassification forbidden |
|---|---|---|
| **PASS** | Applicability established; check actually executed with complete scope-compatible evidence and independent accepted oracle; property holds | Test designed; syntax validated; matching second tool objective; arbitrary threshold |
| **FAIL** | Applicable established invariant with reproducible actual-target counterexample or executed independent violation | Solver crash without scientific evidence; missing authority that determines rule |
| **BLOCKED** | Unknown conditional antecedent, required source/data/oracle/tolerance/certificate/inspection/authority or trust is unresolved; no warranted property assessment | Missing original bytes labelled N/A; guessed numeric epsilon |
| **UNSUPPORTED** | Applicable required feature or required inspection representation is demonstrably absent for precise tool/build/variant, evidenced by declaration and discriminating probe or equivalent reliable observation | Tool unable ⇒ NOT_APPLICABLE, or “skipped” |
| **NOT_EXECUTED** | Test planned but no completed assertion run, and there is not a more specific known BLOCKED/UNSUPPORTED cause at evaluation time | Invented attempt ID, synthetic self-check used as productive run |
| **NOT_APPLICABLE** | Exact genuinely conditional antecedent is proven false with active configuration/source variant and invocation witness | Unavailable optional output, absent file, undisclosed flag, low risk tier |

Conditionality is three-valued: TRUE, FALSE_PROVEN, UNKNOWN. Every mandatory obligation outside a legitimate optional guard remains applicable. In P15-OFF, SR-026 may be N/A with proof of explicit OFF *and* no invocation; in P15-ON, cap becomes mandatory; P15-UNKNOWN ⇒ BLOCKED. Mandatory LF physics is unaffected by P15-OFF.

If an independently established invariant is violated, FAIL can be recorded for that *specific assertion* even while other downstream claims remain BLOCKED by missing authority. Never replace concurrent blockers with a single headline.

## 3. Stop and hold conditions — decision table

| Control ID | Trigger / detectable condition | Test status or governance context | Required pilot control |
|---|---|---|---|
| **STOP-01** | Arm B actually generated from Arm A's model/matrix/translated native solution or shared generator; independence not demonstrable | Independent implementation evidence invalid; per-assertion technical truth not inferred | **STOP_PHASE / INVALID_COMPARISON**; disclose dependency, rebuild independent arm and re-review |
| **STOP-02** | Contract, 48 SR or signed/research-profile revision differs without controlled semantic migration | E01 profile/identity mismatch; BLOCKED comparisons | **HOLD_AFFECTED_SCOPE**; re-freeze or classify as separate experiment |
| **STOP-03** | Real source bytes/release/qualification absent or hash differs; restricted reviewer cannot inspect original | E02 data qualification BLOCKED; V1 can FAIL if mismatched actual data demonstrated | **STOP P2/P3**; no synthetic replacement of owner data |
| **STOP-04** | External CY selection/weights, UTC/Δt, zone/carrier/candidate crosswalk incompatible | Applicable V1/V2 FAIL when proven, otherwise BLOCKED | **HOLD comparison** until common semantic instance verified |
| **STOP-05** | Unresolved source authority or methodology-vs-D2 overlay, or MD decision materially defines proposed rule | Owner gate BLOCKED | **STOP P2/P3**, continue only explicitly scoped research |
| **STOP-06** | Unknown P15 activation or contradictory run flag/history | SR-026 applicability BLOCKED | **HOLD P15 comparison**; cannot declare N/A |
| **STOP-07** | P15 enabled but required OPF cap feature demonstrably not supported | SR-026 UNSUPPORTED | **STOP affected mandatory P15-ON claim**; no waiver by successful LF |
| **STOP-08** | Generated model lacks mandatory row/equality/variable or exhibits incorrect physical KVL/market candidate, valid counterexample | V3 FAIL (or UNSUPPORTED when capability truly absent) | **STOP affected model/feature assessment**, record native E04 and reproduce |
| **STOP-09** | E04 missing, semantic row map not bound to solved native model or critical row inventory unverifiable | Required evidence BLOCKED or evidenced inspection UNSUPPORTED | **HOLD mathematical claim**; no proxy row count |
| **STOP-10** | Solver returns infeasible/unbounded/error/termination without independently valid proof of the asserted property | V4 BLOCKED/NOT_EXECUTED/FAIL depending on exact tested property and witness | **HOLD numeric claim**, keep logs and distinguish generator from solver failure |
| **STOP-11** | A nominal optimum has violated bounds/rows or objectively invalid independently verified primal/certificate | V4 FAIL if established accepted bound/invariant | **STOP specific numerical claim**, preserve unrounded evidence |
| **STOP-12** | Required productive tolerance/discount/network-quality/KPI threshold is TBD | Scoped numeric/physical/KPI BLOCKED | **STOP P2/P3 acceptance**; never use native solver epsilon as method oracle |
| **STOP-13** | P14 uses post-expansion load as pre-expansion H2 baseline, or source B01-D072 lacks named legitimate run | V2/V3 FAIL if demonstrably wrong; otherwise BLOCKED | **STOP affected H2 sensitivity claim**, require referenced baseline |
| **STOP-14** | P16 filter/metric formula B01-D081 missing owner authority; published need treated as approved project | E07 formula BLOCKED or semantic FAIL for proven mislabelling | **HOLD KPI/need claim**; preserve E06 raw decisions |
| **STOP-15** | Positive C04 oracle inconsistent, negative mutation undetected, or two implementations use same faulty verifier | Test-framework sensitivity defect; does not alone establish target FAIL | **STOP affected benchmark verdict**, repair and separately rerun controls |
| **STOP-16** | Different portfolios with independently established equal optimal values | Not in itself a failure | **CONTINUE** with E-OPT-SET/E-OBS analysis; do not force identity |
| **STOP-17** | Meaningful formulation change or semantic-loss risk not yet supported by D4 equivalence | Scoped equivalence proof unresolved; BLOCKED if mandatory | **HOLD equivalence claim**, seek bidirectional mapping/counterexample |
| **STOP-18** | E01–E08 stale, unverifiable digest, missing evidence ancestor or tampered run | Evidence quality BLOCKED; potentially separately confirmed integrity FAIL | **REBASE_AND_RERUN** impacted tests; retain original attempts |
| **STOP-19** | Same authors perform “independent qualified reviewer” attestation or model tool asserts G1 | Reviewer/owner gate BLOCKED | **STOP reviewed/full claim**, do not upgrade AI self-review to external approval |
| **STOP-20** | Any applicable mandatory FAIL, UNSUPPORTED, BLOCKED or NOT_EXECUTED while a full-profile claim is proposed | Claim ineligible; exact six-state vector retained | **WITHHOLD full claim**, log remaining scope/owner blockers |
| **STOP-21** | Actual implemented tool behaviour or oracle differs from frozen profile after release | Existing evidence stale; new independent attempt required | **REBASE_AND_RERUN**, never edit old PASS |
| **STOP-22** | New generic robustness criterion or unapproved downstream methodology/parameters silently inserted | Scope contamination / false normative authority | **STOP affected claim**, preserve original scope and obtain later explicit owner change |

**STOP or HOLD are protocol actions and do not by themselves prove model failure.** For example, a solver crash may be a numerical run event without any accepted V3 counterexample. Contrastingly, a missing required nonanticipativity equality established on an actual generated model can FAIL a specific V3 obligation even if no solver was invoked.

## 4. Technical fault-domain routing

| Fault domain | First evidence to inspect | Propagation |
|---|---|---|
| SOURCE / METHOD | E01 source release, D1–D6 ledger, clause→SR source and authority | Blocks dependent profile/claims; does not erase synthetic derivation |
| INPUT / TIME / UNIT | E02 original-byte source, CY/year mapping, UTC/Δt, unit conversion | V1 and all downstream assertions dependent on affected data may BLOCK |
| PREPROCESS / LINEAGE | E03 38 transform proposals, conservation, data axes, missing B01-D072/B01-D081 | V2 and derived model/KPI claims affected |
| MATHEMATICAL GENERATOR | E04 variables, bounds, rows, objective, indexed omissions, physical and candidate roles | V3 FAIL if invariant counterexample; may invalidate numerical meaning despite successful solve |
| SOLVER / NUMERICS | E05 exact model, primal, bounds/duals, residuals, status/versions | V4 claim blocked/fails per actual cause; do not substitute solver messages for certificates |
| RESULT / REPORTING | E06 unfiltered raw and E07 formula/filter authority | V5 may fail or block while E04/E05 remains intact |
| EVIDENCE / INDEPENDENCE | E08 graph closure, actual attempt, review role, provenance integrity | V6 or claim blocked; all synthetic/native statuses remain separately scoped |

A conformance display may use FAIL > UNSUPPORTED > BLOCKED > NOT_EXECUTED > PASS for **different applicable assertions**, while preserving the full vector and all separate blockers. If all candidate assertions are legitimately excluded, report NOT_APPLICABLE with empty-applicable-scope, never “all mandatory PASS”.

## 5. Incident and re-entry dossier

Every paused future scope should retain a canonical *incident record*: STOP-ID, phase and tool arm, contract and input versions, SR/assertion IDs, explicit P15 guard and scope class, witness, test status (if evaluated), factual root cause versus hypothesis, owner/verification decision required, E01–E08 hashes, negative mutation context, change and new attempt revision, qualified review and restart decision. A human coordinator determines restart of a phase; a scientific PASS cannot authorise G1.

**Re-entry checks:** cause specifically corrected; replacement source/oracle/tolerance authorized where relevant; native generator rebuilt independently; source/model digests changed and dependent evidence marked STALE; actual rerun and fresh attempts performed; independent verification re-evaluated; old FAIL/UNSUPPORTED/BLOCKED evidence retained. A new reviewer must not be the original implementation author when an external independent review is claimed.

## 6. Current boundaries

No actual incident, capability absence, solver failure, two-tool comparison or qualified release is established in ML-C07. The STOP IDs are **planned research controls**, not observed runtime results. Productive P2/P3 are presently blocked by real-data authority, quantitative acceptance oracles and external review. P0/P1 are likewise unexecuted. **G1 remains BLOCKED.**
