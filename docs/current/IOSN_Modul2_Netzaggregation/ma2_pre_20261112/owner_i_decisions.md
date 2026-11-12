# M2-MA2-PRE — Proposed Owner / project-I decisions and outstanding gates

**Classification:** PROPOSED / OWNER_PENDING throughout. Version 2026-11-12. This document **records recommendations only**, not acts of approval. It does not make a canonical-API choice, change MA1 or authorize M2 runtime, MA3, a PR merge, or REAL_QUALIFIED.

## 1. Authority and immutable higher-level decisions

**Known:** [Task 98](../98_M2_MA2_PRE_DOCUMENT_FIXTURE_MACRO_20261111.md) permits only isolated document/fixture design; [conditional macro 100](../100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md) requires a repaired independently reviewed MA1 SHA, an explicit Owner API choice, and new scoped MA2-SYNTHETIC-IMPLEMENTATION authorization. MA1 [handoff 85](../85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) remains a prior technical source, not an active code instruction under this gate.

**Review status inherited, not re-adjudicated:**
- R-PHY SHA c004e5330df2a018e567c8ef955ef2fc9d71e0ea: **4 open P1** input immutability, HVDC Boolean, in_service Boolean, unsafe numerical tolerance.
- R-CLU SHA 7d7d07d7af5966ddc26d0be1100a69013763d2e8: **2 open P1 + 3 P2** including false-infeasible four-bus greedy search and silent 400-kV screening exclusion.
- R-API SHA 075c50903b7d51ec19befb4a4b8db1322ae33b2a: **option C recommended**, *not selected*: A (iosn_official) canonical with limited typed B (m2) adapter, strict lossless v1.
- D-REAL SHA 6a8262f128ae3dd7e108afe2ade09028ea4f651f: **BLOCKED_DATA**, no real Europe/source/neutral set qualified.
- R-METH SHA 754a79e11370dca2c25f1102d83ced5beb251522: **AUTHORITY_UNCONFIRMED**, ENTSO-E 25.02.2026 consultation is *scientific working source only*, not verified adopted/effective methodology.

The five externally chosen project weather-year IDs are frozen inputs, **not** an official number of ENTSO-E weather cases. Complete European consultation-profile quotas are exactly 37 distinct labels/102 zones, Northern Ireland and United Kingdom separate. No M0/CGMES, M1/PECD, year selection, external source adapter or MA3 capacity code is within the present task.

## 2. Decision register, all PROPOSED

| Decision | Alternatives and proposal | Rationale / consequence |
|---|---|---|
| **OD-M2-API-01** (contract authority) | A only / B only / **C proposed: A as provisional MA2 core, B through *versioned* one-way constrained adapter** | R-API favors C, but no Owner signature. Implementation blocks on OWNER_PENDING. No fusion/merge. |
| **I-EQ-01** (x gauge) | Absolute physical x without angle witness **reject** / **propose** one log-geometric-mean normalization of x/x_ref per actual meshed AC island | Only x ratios identifiable from DC flows. x_ref must be frozen, positive and source-labeled. A numerical gauge is not an absolute x measurement. |
| **I-EQ-02** (bounds/regularization) | **Propose** optimize u=log(x/x_ref) under finite bounds with data-only Jacobian rank checked before/after optimization; regularizer=0 for exact analytic oracles | Nonzero prior allowed as engineering stabilization only if it cannot conceal rank deficiency. Concrete production u bounds, prior and lambda remain owner approval items. |
| **I-EQ-03** (identification) | **Propose** rank-revealing gauge-restricted sensitivity, per-island report; tree/collinear cases UNIDENTIFIABLE; rank-undetermined fail closed | Cannot assign x from KCL-only tree flows. Threshold/scaling must be signed by numeric Owner. |
| **I-EQ-04** (structural correction) | **Propose** c0=C alpha, globally selected on TRAIN only, constant over snapshots, A_z c0=0 and actual affine-KVL solver | A post-hoc offset without equivalent-model equation is no pass. No time-varying ad-hoc c0 for PST. |
| **I-EQ-05** (device sources) | **Propose** known fixed transformer/PST phases as explicit \(\phi\), HVDC as terminals, strict lossless MA2-v1; unknown mapping -> DEVICE_SOURCE_UNQUALIFIED | Neutral HVDC=0/PST=0 must be **independently balanced**; fixed phase remains explicit unless a validated convention absorbs it. Lossy HVDC and tap≠1 require separate gate. |
| **I-EQ-06** (numerical solver) | **Propose** log-x bounded sparse nonlinear least squares, sparse island Laplacian, analytic/JVP sensitivities, independent small dense cycle oracle; no dense European inverse | W-EQ may use starting guesses, but certify full unregularized data rank and source/KCL/KVL residuals. Production memory/CPU and convergence tolerances OWNER_PENDING. |
| **I-ITER-01** (neighborhood) | **Propose** country-local boundary moves, quota-preserving swaps and 2/3-country coupled atomic bundles over original active-AC country graph | Country quotas and country purity hard; connectedness, protection and island rules checked **before** fit; no HVDC-defined coupling. |
| **I-ITER-02** (global refit) | **Require** every feasible nonduplicate candidate to rebuild original P/Gamma/A_z, both source targets and x/c0 for **all** reduced European AC islands | Reusing incumbent fit/zonepair IDs or adjusting only one country invalidates global optimization. Warm start only initial guess. |
| **I-SPLIT-01** (split) | **Propose** frozen temporally blocked TRAIN/SELECTION/FINAL_HOLDOUT + optional EMBARGO *within each of five unchanged years* | No new year selection or hidden resampling; one split SHA; Holdout sealed until final independent replay; leakage invalidates experiment. |
| **I-MON-01** (topology-comparable metrics) | **Propose** primary fixed exact original intercountry AC corridor sums plus prequalified *exactly representable* protected corridor monitors; raw zone-link RMSE diagnostic only | Candidate link set changes: comparing E-dimensional averages would bias the search. Do not fabricate branch flow from a many-branch aggregated link. Source monitor IDs/weights frozen before search. |
| **I-SEL-01** (selection objective) | **Propose** duration/weight-normalized RMSE J on the *same* SELECTION monitor index, orientation and samples, strict \(J_{inc}-J_{cand}>\max(\delta_{abs},\delta_{rel}\max(J_{inc},J_{floor}))\) | Absolute/relative δ and J_floor require Owner; for IT-01 test choose δ<1 MW (not a real threshold). Exact equality **reject**; rollback state atomic. |
| **I-FAIR-01** (fairness and criticality) | **Propose** hard mandatory monitor coverage/protected retention; country-maximum RMSE/fairness constraints owner-specified, plus MAE/P95/P99/link-count/counterflow diagnostics | Lower global RMSE alone may hide regional deterioration or swallowed critical branches. A specific fairness cap is **not yet adopted**. |
| **I-STOP-01** (termination) | **Propose** deterministic eval-count limit, MAX_ROUNDS, P no-improvement rounds -> PLATEAU; CPU/walltime interruption separately status BUDGET_STOP_NOT_CONVERGED | Search exhaustion/budget stop ≠ scientific convergence. Selection reused adaptively, so holdout required once; no tuning after holdout failure. |
| **I-AUDIT-01** (ledger/publishing) | **Propose** SHA-bound candidate ledger for accepted/rejected moves, projection/operator/solver/replay, staging write-once+atomic READY manifest | No arbitrary result overwriting, input mutation, partially written 'success' or faked run SHA. |
| **I-TEST-01** (synthetic residuals) | **Propose only for numeric design fixtures** KCL ≤1e−8 MW, generalized cycle ≤1e−10 rad, dense/sparse diff ≤1e−8 MW | Pending independent calibration for scale/condition and real data; tolerance must be finite/bounded and cannot bypass an unbalanced island (PHY-R04). |
| **I-REAL-01** (real acceptance) | **Propose** no real MA2 until original bytes, source-owner/license, full 37/102 grid, synchronized five-year operations and *separate* neutral dispatch, 225/400 ratings, device semantics and D4 witness admitted | D-REAL BLOCKED_DATA is a hard gate; OSM/PyPSA open topology smoke does not establish official IoSN Real. |
| **I-METH-01** (method validity) | **Propose** O26 consultation working baseline, tag all private solver choices I; actual adopted/effective document version MD-01 remains external-authority unresolved | MD-03 x/c0/RMSE, MD-13 cluster/criticality, MD-11 source, MD-12 times, MD-08 LF/OPF and MD-18 external year input remain traceable; no 'official method PASS'. |
| **I-REVIEW-01** (independence) | **Require** independent R-PHY and R-CLU replay on the same repaired MA1 SHA; independent R-NUM on future MA2 implementation SHA | Internal fixture computations and green CI do not constitute R-NUM signoff. No automatic PR merge. |

## 3. Owner choices needed before a production implementation specification becomes authorized

The following are **not** answered by preparing documentation: (a) exact repaired-and-reviewed MA1 code SHA; (b) A/B/C canonical API and adapter scope; (c) whether the task M2-MA2-CODE may start and what 'synthetic-only' explicitly means; (d) design profile acceptance for gauge, rank threshold, bounds, lambda, phase provider, fixed monitor catalogue and split; (e) origin and admissibility of separately balanced neutral dispatch; (f) interpretation of adopted/effective IoSN methodology and official quality oracles.

**Recommended staged gate decision, for consideration only:**
1. OD-M2-MA2-PRE = **ACCEPT_DOCUMENT_AND_FIXTURE_DESIGN_ONLY** after checking this documentation and machine-readable matrix. This authorizes no code.
2. OD-M2-API-01 = C *if and only if Owner explicitly selects it*, with strict lossless v1; no implied branch reconciliation or merge.
3. OD-M2-MA2-CODE = **DEFER** until positive post-repair R-PHY/R-CLU reviews on one integrated SHA and a new scoped authorization.
4. REAL_G12 = **BLOCKED_DATA** until full source-attested input and independent physical/numeric qualification; N-1 capacities deferred to MA3.

## 4. Gate decision record template (empty by design)

~~~text
Decision ID: ___________________
Selected option (not merely recommendation): ___________________
Owner / authority: ___________________
Approval timestamp / issue / commit: ___________________
Evidence SHA(s) and scope: ___________________
Effective start / expiration: ___________________
Explicit exclusions: MA1 unresolved findings / MA2 runtime / real / main merge / M0 / M1 / year selection
Independent re-review requirement: ___________________
~~~

**Do not populate or publish a selected option from a recommendation.** The present outcome can be **MA2_PREP_READY_FOR_GATE — DESIGN STATUS ONLY**, with implementation/runtime/review/real/merge flags all false.
