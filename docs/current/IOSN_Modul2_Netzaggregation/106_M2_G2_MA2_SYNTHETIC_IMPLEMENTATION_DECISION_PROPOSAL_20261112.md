# 106 — M2-G2 | MA2 synthetic-only conditional implementation decision proposal

**Date:** 2026-11-12. **Status:** `PREPARED_NOT_AUTHORIZED`. **Not a runtime instruction.**
Source hierarchy: original technical Handoff **85** @ `70e92ba9e62a320e58227ce9c2f03fad266f44bf`; conditional implementation macro **100** @ `27dfd810b39e17e6b616a2b0aeb813eb8948d8a0`; MA2-PRE `ma2_pre_20261112` @ `b73bb3c595bff515aeca052f02fc83f72289b5f0`; A–E consolidation 102 / G2 handoff 103 @ `37ee7734049d4cbe3480bb263ca68615d9140809`. **Do not confuse the conditional MA2 file 100 with the D-SOURCE1 document 100 on its separate branch.**

## 1. Three independent, non-substitutable entry gates

| Entry gate | Required positive evidence | Present |
|---|---|---|
| **G2-S1: MA1 science** | Both genuinely independent RR1 R-PHY/R-CLU with zero open P0/P1 on exact identical integrated implementation `fb201ef5f120f64696dea9aa99f77ece77546f9a`, independent code/tree, test and CI proof; explicit P2 treatment; a separate `MA1_SYNTHETIC_QUALIFIED` release record | **NO — RR1 pending** |
| **G2-S2: Project Owner/API/I contract** | Signed Owner selection A/B/C (C proposed), strict lossless v1 devices, observed-real QA separate, screen/protected policy audited, approved `M2.MA2Input.v1` with exact 15 MA1 files and all open API/MD/I discrepancies dispositioned, numeric/config/split/monitor freeze | **NO — OWNER_PENDING / CONTRACT_DRAFT** |
| **G2-S3: Independent scoped code decision** | New explicit Owner act `SCOPED_SYNTHETIC_IMPLEMENTATION_ONLY` listing implementation SHA, named W-EQ, W-ITER, W-INT scopes, no real data or merge, source/test boundaries, report/review obligations | **NO — MA2_CODE_NOT_AUTHORIZED** |

**Conjunction rule:** `MA2_CODE_GO = G2_S1 AND G2_S2 AND G2_S3`. No implicit auto-activation when a future reviewer report arrives. The present file does **not** approve G2-S3.

## 2. Contract for future W-EQ (when and only when authorized)

Define original AC incidence `A_d (N×L)`, country-pure candidate assignment `P (Z×N)`, oriented cut projector `Gamma (E×L)` and reduced incidence `A_z (Z×E)`. Enforce source conservation for each candidate:

- `A_z Gamma = P A_d` exactly; `p_z(t)=P p_d(t)`; `f_target(t)=Gamma f_detail(t)` with frozen **original global** detailed flows and per-true-AC-island balances. HVDC is signed terminal injection, not an AC graph edge.
- For each reduced meshed AC island, `B(x)=diag(S_base / x_e)`, `x_e > 0` and sparse reduced Laplacian `L=A_z B A_z^T`. Cycle basis `C` satisfies `A_z C=0` and structural `c0=C alpha`, so `A_z c0=0` identically.
- The **actual source-free reduced solver**, not plotting postprocess, has `f=B A_z^T theta + c0` and `L theta=p_z`; thus `A_z f=p_z` and `C^T diag(x)(f-c0)=0`. Nonzero structurally calibrated `c0` must not be projected away by an ordinary DC post-hoc estimator.
- With a validated fixed or operational reduced phase source `phi(t)` in radians: `f=B(A_z^T theta-phi)+c0` and `L theta=p_z+A_z B phi`. Required cycle residual is `C^T[(diag(x)/S_base)(f-c0)+phi]=0`. If the reduced phase-source provider cannot map original transformer/PST physics, reject that operational comparison as `DEVICE_SOURCE_UNQUALIFIED`; do not absorb time-varying PST into fixed `c0`.
- Use positive `x_ref`, bounded `u=log(x/x_ref)` with a fixed scale gauge in every meshed **physical AC island**, and test the **unregularized data Jacobian** on TRAIN for effective rank. A tree or insufficiently excited island is `UNIDENTIFIABLE`, not a fit PASS. An absolute x value is not identifiable from DC-flow observations alone merely by imposing a gauge. Sparse island solves only; no dense full-Europe inverse.
- Use independently balanced *neutral* calibration dispatch (HVDC=0/PST=0 and all other source terms supported), with immutable **distinct source and content hashes** from operational data. Switching device flags in the operational dispatch without rebalancing is forbidden. Separate real measured AC-flow discrepancy QA must not be forced equal to DC approximation.

**G06 evidence:** numerical / analytic dense oracles, source/provider manifest, rank/gauge report, strictly positive x, per-island KCL, cycle residuals for source-free and source-dependent affine KVL, convergence ledger, immutable input/source/solver SHA. E's proposed fixture tolerances are *test proposals only*; final scale-aware numerical accept limits remain Owner/reviewer choices.

## 3. Contract for future W-ITER (when and only when authorized)

- Country interaction graph uses **active original AC** cross-border ties only. Hard quotas for each country, country-pure/nonempty AC-connected zones, exact source/asset protection and true AC-island integrity. In full profile 37 labels, 102 zones, NI/UK separate; synthetic tests use marked synthetic quotas.
- Deterministic **boundary moves**, quota-preserving **swaps** and atomic connected 2- or 3-country bundles; no cross-country zone formation. Every candidate is validated as a whole **before** fitting. Invalid candidates are recorded with reason and **zero fit calls**.
- Every feasible nonduplicate candidate rebuilds **whole-Europe** original `P, Gamma, A_z`, zonepair IDs, aggregated operational AND separate neutral targets from the same immutable original snapshot set, new phase-source mapping, sparse cycle basis and **complete global x/c0 refit** on TRAIN. Only initial optimizer guesses may be warm-started; no reuse of incumbent fit or zonepair index ordering as authority.
- Create one immutable blocked `TRAIN / SELECTION / FINAL_HOLDOUT` (optional EMBARGO) split **inside** each of five already fixed external project years, with source/time/season/duration/unit hashes. No input year re-selection, leakage, tuning on final holdout or per-candidate split changes.
- Fix an original-graph **topology-comparable** monitor set before search (primary complete intercountry corridor sums in canonical direction, optionally exact reconstructible protected corridor bundles). A raw mean RMSE over a different number of candidate zonepairs is **not a comparable selection objective**. Branch flows hidden inside aggregate links cannot be invented. Mandatory monitor/protected coverage failures reject the candidate.
- Evaluate candidate `J` on exactly the same SELECTION snapshot/monitor/hour weights as incumbent; accept only strict improvement `J_inc - J_cand > max(delta_abs, delta_rel * max(J_inc, J_floor))` with Owner-frozen finite nonnegative thresholds. Fairness/country-worst constraints mandatory when chosen. Equal score, source inconsistency, solver failure or critical-branch loss ⇒ atomic rollback.
- Record all accepted, rejected, duplicate and budget-stopped candidates in deterministic ledger with canonical partition SHA, changed countries/zonepairs, full global-refit proof, evaluator config, source/split/monitor hashes and monitor metrics. Label `PLATEAU` distinctly from `BUDGET_STOP_NOT_CONVERGED`; a stop cannot claim global optimum.

**G07/G08 evidence:** owner-approved fixed monitor index, signed direction, country fairness and protected policy, complete candidate/evaluation ledger, deterministic replay, sealed FINAL_HOLDOUT followed by **one** independent final replay. No arbitrary threshold chosen from the consultation draft.

## 4. Test/review scope and artifacts for the *future* MA2 implementation

E's matrix contains **45 designs**, each `DESIGNED_NOT_EXECUTED`. Conditional code work must implement all applicable IDs, with explicit not-applicable reasons tied to the selected device/physical scope, plus fresh adversarial tests for tree/gauge, multi-island, nonzero fixed phases, operational PST provider failure, unbalanced neutral, protected 400-kV Class-0 exception, changed zonepair monitor bias, leakage, multi-country rollback and resource stops.

Worker split once separately authorized:

| Worker | Allowed objective | No-go |
|---|---|---|
| W-EQ | new M2 global equivalent x/c0 and sparse affine-KVL implementation with independent analytic fixtures, source-aware fail-closed modes | no real-grid claim, no unsupported devices, no dense-Europe inverse |
| W-ITER | quota/AC protection candidate generator, 2–3-country bundles, full global refit integration interface, fixed monitor/selection/holdout and ledger | no M0/M1/weather changes, no reuse of incumbent fit |
| W-INT | reconcile on one immutable integration SHA, re-run full MA1/MA2 synthetic suite and export write-once SHA-bound artifacts | no unilateral approval, no main merge |
| R-NUM | **different** reviewer independently repeats physical/optimization/selection oracles at integrated MA2 SHA and independently opens final holdout | worker green CI is not R-NUM signoff |

Required target evidence names from conditional macro 100: `fit.json`, `equivalent_network.json`, `rmse_per_link.csv`, `candidate_ledger.csv`, `input_split_manifest.json`, `holdout_report.json` and independent review report/JUnit/artifact/source-manifest. Staging/READY must be atomic; partial directories never PASS.

## 5. Decision that remains to be made

A permissible *future* Owner statement, **only after G2-S1 and G2-S2 are actually satisfied**, is:

> Approve M2-MA2-W-EQ/W-ITER/W-INT **SYNTHETIC IMPLEMENTATION ONLY**, on the explicitly identified repaired and independently RR1-qualified MA1 implementation and frozen A v1 contract, subject to planned 45-case matrix plus new negative oracles, independent future R-NUM, no real source admission, no production operation, no MA3, no M0/M1/weather modification and no GitHub merge. No operational release from this authorization alone.

This quotation is **draft wording**, not an Owner act; it requires a named competent owner, selected options, timestamps, issue/commit signature and testable I-values. Alternatively select `DEFER` without activating any worker.

**Actual current outcome:** `NOT_AUTHORIZED`. Start only nonruntime follow-ups listed in document 107; G06–G08/R-NUM remain `NOT_IMPLEMENTED / NOT_RUN`, `G12=BLOCKED_DATA`.
