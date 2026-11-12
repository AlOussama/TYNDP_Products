# 109 — S-GOV-M2-G2 Project-Owner decision register after both RR1 results

Date: 2026-11-12. Classification: DECISION-READY PROPOSAL / UNSIGNED / OWNER_PENDING. This is the post-RR1 supplement to immutable draft 104, not a Project Owner act or retroactive amendment to Method-G1.

## 1. What has changed since the initial G2 proposal

Document 108 verifies two independent RR1 decisions ACCEPT_SYNTHETIC against identical repaired production SHA fb201ef5f120f64696dea9aa99f77ece77546f9a, each with zero synthetic P0/P1. Therefore the strictly scientific MA1 synthetic-lossless-DC RR1 condition is met. The original six MA1 PHY/CLU P1s were independently closed within scope; this does not close separate R-API-P1-01..09 interface-semantic contract items, source-byte dependencies, bounded search completeness, or actual Project Owner choices. The distinction between science gate and Owner authorization is mandatory.

Project Owner decisions may now be made, but they do not self-activate a code worker. No Owner signature/selection was found in the checked record; the selected column below stays PENDING. The review reports are published under commits 7a7de151fcf7e4bd2cda0530c2438dcfc95b5df1 (PHY) and bb7cabeb25f092e4ab68732e17903e7be1413c55 (CLU).

## 2. Specific Project Owner choices — all unsigned

| Decision identifier | Scientific / engineering recommendation | Actual selection |
|---|---|---|
| OD-M2-API-01 / OD-M2-API-09 | Option C: one canonical production API tyndp_reduce.iosn_official; B=tyndp_reduce.m2 only as independent parity comparison or optional audited, typed, versioned one-way B→A adapter; no fusion and no required dependency | PENDING |
| OD-M2-API-02 | STRICT_LOSSLESS for MA2 v1: HVDC power terminals balanced p0=-p1 with declared sign; unknown/lossy HVDC, unsupported taps/transformer/PST phases or source-device semantics FAIL_CLOSED | PENDING |
| OD-M2-API-03 | SEPARATE_MODEL_DISCREPANCY_QA: observed real signed AC flows are separately hashed measured-flow QA, never force observed AC equals synthetic DC result within 1e-6 MW | PENDING |
| OD-M2-API-04 | AUDITED_CLASS_AND_PROTECTION: prove 225/400 nominal-voltage class; source-backed 220/380 translations; screen/class0/critical and protected exceptions explicit, signed and auditable | PENDING |
| OD-M2-API-05 | DOC_GATE_ONLY_NO_MERGE, with separate future code release | PENDING |
| OD-M2-METH-01 | O26, ENTSO-E public consultation dated 2026-02-25, as PROJECT provisional scientific baseline only; no official adopted/effective claim | PENDING |
| OD-M2-CLUSTER-02 | Hard country purity, exact regional quotas, actual AC-connected zones, protected cuts, global electrical AC topology; 37/102 only for complete sourced consultation-profile dataset | PENDING |
| OD-M2-EQV-03 | Positive global equivalent x, fixed source-correct gauge per true meshed island, structurally divergence-free c0, actual affine KVL with validated phase sources and island balance | PENDING |
| OD-M2-RMSE-04 | Frozen weighted train/selection/final holdout; topology-comparable original network corridor monitors, mandatory protected coverage, country fairness acceptance limits, no unverifiable normative threshold | PENDING |
| OD-M2-N1-05 | All real summer/winter × forward/reverse N-1 MA3 security/capacity claims delayed to sourced TSO contingencies and independent data/physics/numeric gates | PENDING |
| OD-M2-DATA-06 | Original-byte/source-owner/licenses and exact full grid, fixed 5 project-year external IDs, synchronized nodal dispatch, distinct physically balanced neutral source, device/rating/border witnesses; D4 after input freeze | PENDING |
| OD-M2-DEVICE-07 | Strict supported/unsupported per-device source capability contract; lossless synthetic subset only now; all approximations separately qualified and reviewed | PENDING |
| OD-M2-LF-08 | Distinguish network reduction and future expansion/dispatch/OPF, no infinite-limit shortcut as N-1 certificate | PENDING |
| OD-M2-I-10 | Versioned PROJECT I-rules (bounded search, gauge/rank, split/monitors, full global refit and solver/QA numeric policies), never mislabeled official ENTSO-E prescriptions | PENDING |
| OD-M2-SCOPE-11 | Documentation, reviewer reconciliation, source acquisition and independent MA2 design review may proceed without code GO | PENDING |
| OD-M2-MA2-PRE | ACCEPT_DOCUMENT_AND_FIXTURE_DESIGN_ONLY for all 45 planned cases; no MA2 code or numeric review PASS | PENDING |
| OD-M2-MA2-CODE | DEFER while API/I/input contract unapproved. Later possible separate signed SCOPED_SYNTHETIC_IMPLEMENTATION_ONLY release after all MA2 prerequisites | PENDING |
| OD-M2-MERGE-12 | NO_MERGE_NOW: draft PRs stay draft; main remains unaltered | PENDING |

The API-01 choice and Method-G1 API-09 concern the same proposed architecture and must be one consistent, cross-referenced Owner act, not two contradictory approvals. All others in the canonical 12-case Method-G1 register at c980bbd341b1051257bcf31b0a904dd7937f7241 continue to apply.

## 3. Project I parameter acceptance worksheet — NOT YET FROZEN

For approval of M2.MA2Input.v1 and a later MA2 code task, the competent Project Owner must populate and version a single testable I-profile, with actual values, units, constraints and independent oracles:

| Section | Mandatory fields to decide; do not infer numeric values |
|---|---|
| Source / MA1 payload | Exact 15-artifact names, 14 SHA-256 payload hashes, immutable source/checkout manifest, ordered N/L/T IDs, units, A_z Gamma=P A_d, class/protection and signed terminal definitions |
| I-EQ gauge and bounds | x_ref source and units, x>0, per-true-meshed-island log-x normalization weights, finite log-x bounds, gauge strategy; no physical absolute x identifiability without external anchor |
| I-EQ identifiability and solver | Source-aware fixed and operational phase provider, structural c0=C alpha, full unregularized data Jacobian rank/scaling/threshold, sparse solver configuration, regularization prior/lambda, resource ceiling, convergence and physical residual caps |
| I-DATA operational / neutral | Immutable original operational and independently balanced neutral dispatch per AC island; supported HVDC/PST/fixed phase device schedule; independent source hash and dispatch/time ratings |
| I-SPLIT / I-MON | Frozen per-year blocked TRAIN, SELECTION and sealed FINAL_HOLDOUT (embargo if chosen); exactly same year inputs; fixed exact original-corridor monitor IDs, orientation, weights, representability and mandatory coverage |
| I-ITER / I-FAIR | Country interaction adjacency from true original AC ties; allowed single/two/three-country atomic swaps, deterministic candidate/rollback policy, full-global re-projection and x/c0 refit; delta_abs, delta_rel, J_floor, regional fairness bound |
| I-STOP / I-AUDIT | MAX_ROUNDS, candidate and state budgets, plateau patience, time/memory policy, deterministic seed and canonical tie-breaks, failure labels, write-once SHA-ledger, atomic publish / final holdout one-time opening |
| I-SCREEN | Actual 225/400 overload-energy thresholds and weights by year, protection union and explicit exceptions; signed 220/380 source mappings; mandatory devices reject unsupported source semantics |
| I-TEST | Every applicable EQ/IT/SH ID in E's planned 45-case matrix with executable oracles; finite physical tolerances independently calibrated for synthetic fixture and no hardcoded adoption of a real-grid or ENTSO-E tolerance |
| R-API contract | Each R-API-P1-01..09 and P2 compatibility item mapped to enforceable guard/negative test or documented unsupported adapter; OWNER_REVIEWED_DISPOSITION required |

E's 1e-8 MW KCL, 1e-10 rad generalized cycle KVL and 1e-8 MW dense/oracle difference are proposed synthetic-case tests, not active Owner-approved parameters. MA1 physical atol_mw <= 1e-6 MW is an implementation hard cap and not a measured-real-flow RMSE acceptance.

Until every mandatory field is selected and verified, status stays M2.MA2Input.v1_DRAFT / OWNER_I_FREEZE_PENDING and MA2_CODE_NOT_AUTHORIZED, even with RR1 scientific success.

## 4. Three separate authority lanes

**E1 — Project authority:** A competent Project Owner can approve A-vs-B-vs-C canonical architecture, synthetic I parameters, provisional research baseline and scoped MA2 code. None has been approved by this S-GOV document.

**E2 — ENTSO-E method authority:** A Project Owner cannot certify adoption/effectiveness of a public-consultation draft. ENTSOE_AUTHORITY_UNCONFIRMED until an externally competent adopted/effective text, exact version/bytes, date/approval and clause-by-clause NR-01..NR-18 comparison are demonstrated. The draft's three illustrative weather cases and the project's five externally selected year inputs must not be conflated.

**E3 — Original data and security authority:** D0 official TSO/IoSN complete network grants, D1 open REAL_TOPOLOGY_ONLY pilot source bytes, D2 time/dispatch/neutral files, D3 actual TSO N-1 scenarios and independent D4 replay remain BLOCKED_DATA. A table with 37 country labels and 102 zone quotas is not a qualified European electrical dataset.

## 5. Required explicit approval record, blank by design

- Owner competent identity and documented delegation: NOT_PROVIDED
- Accepted/rejected choice for every requested OD: NOT_PROVIDED
- Accepted I-parameter profile hash, version, ranges and units: NOT_PROVIDED
- Exact approved code/input SHA(s) and permitted roles: NOT_PROVIDED
- Owner-approval timestamp, issue URL, immutable quote and effective interval: NOT_PROVIDED
- Explicit exemptions / source and reviewer identity attestations: NOT_PROVIDED
- Separate SCOPED_SYNTHETIC_IMPLEMENTATION_ONLY MA2 code decision: NOT_PROVIDED
- Merge, Real and official ENTSO-E authority: NOT_APPROVED

A mere owner discussion, a draft-PR review or this published register is not a signature. A later actual signed act must be recorded in a new immutable decision file with the chosen value and audit reference. At this G2 milestone: MA1 scientific RR1 evidence PASS scoped; OWNER_PENDING; MA2_CODE_NOT_AUTHORIZED; REAL_QUALIFIED=false; NO_MERGE.
