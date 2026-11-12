# 104 — S-GOV-M2-G2 | Project-Owner decision register (UNSIGNED PROPOSAL)

**Date:** 2026-11-12. **Repository:** AlOussama/TYNDP_Products.
**Classification:** PROJECT_DECISION_PREPARATION_ONLY / OWNER_PENDING.
**Approval status:** No option in this file is an actual Owner selection, release, signature or delegation. No code, PR merge, real data run or MA2 implementation authorized.

## 1. Immutable input and hierarchy

- Governance input: `102_M2_A_E_CONSOLIDATION_AND_G2_READINESS_20261112.md` and `103_M2_RR1_AND_OWNER_G2_COLD_START_HANDOFFS_20261112.md` at `37ee7734049d4cbe3480bb263ca68615d9140809`.
- A RP1 integrated repair: `fb201ef5f120f64696dea9aa99f77ece77546f9a` (Draft PR 41, report 101); Worker evidence, not reviewer signoff.
- B API G1: `ed42d051a7234f7f062d94d06291f66e56657bbc`; recommendation C and draft `M2.API.v1` / `M2.MA2Input.v1`.
- C D-SOURCE1: `05dd0db3fc15fd6e091b8dd96d854adcedf8302c`; D0–D3 blocked, original source payloads not qualified.
- D METHOD G1: `c980bbd341b1051257bcf31b0a904dd7937f7241`; proposed decisions, ENTSO-E authority unresolved.
- E MA2-PRE: `b73bb3c595bff515aeca052f02fc83f72289b5f0`; designs and 45 planned, not executed, tests.
- Conditional MA2 source: `100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md` at `27dfd810b39e17e6b616a2b0aeb813eb8948d8a0`. This is *not* the separate D-SOURCE1 report number 100.

**Scope:** Only Modul 2. No modifications to M0/CGMES, M1/PECD, weather-year selection, legacy `tyndp_reduce.m2` or main.

## 2. Decision cards for the competent Project Owner

All values in the **Selected value** column are intentionally **PENDING**, independently of the recommendation. An explicit, attributable Owner act must fill each value. Merely approving this draft or opening a PR is insufficient.

| ID | Proposed value (not selected) | Alternatives / exact effect | Selected value |
|---|---|---|---|
| OD-M2-API-01 | **C**: `tyndp_reduce.iosn_official` as sole canonical A API; B as independent parity oracle; optional typed, source-attested one-way B→A adapter only on demonstrably lossless subset | A-only is feasible; B-only requires a new contract. Never fuse A and B; no B prerequisite for MA2. | **PENDING** |
| OD-M2-API-02 | **STRICT_LOSSLESS** | HVDC terminals satisfy `p0=-p1`, explicit sign convention and each T. Lossy/asymmetric transfers, unresolved taps, phase and source devices fail closed; later separate device gate for extensions. | **PENDING** |
| OD-M2-API-03 | **SEPARATE_MODEL_DISCREPANCY_QA** | Real observed signed AC flows are separately hashed quality observations; never assert measured AC = DC reference to ≤1e-6 MW. | **PENDING** |
| OD-M2-API-04 | **AUDITED_CLASS_AND_PROTECTION** | 225/400-kV screen mandatory on qualified lines; 220→225/380→400 only with source proof; no class0 opt-out on genuine 225/400 without approved exception; freeze auditable protection policy, threshold/year weights/source SHA. | **PENDING** |
| OD-M2-API-05 | **DOC_GATE_ONLY_NO_MERGE** | Current G2 is documentary; does not approve adapter porting, runtime, merge or production. | **PENDING** |
| OD-M2-METH-01 | **O26_PROVISIONAL_SCIENTIFIC_BASELINE** | ENTSO-E consultation text dated 2026-02-25 is a scientific reference for project design, not a declaration of adopted/effective ENTSO-E authority. | **PENDING** |
| OD-M2-SCOPE-11 | **DOCUMENT_FIXTURE_AND_SOURCE_ACTIONS_NOW** | Independent RR1, doc/fixture design, source intake and formal reviews only; later actual MA2 code requires new scoped release. | **PENDING** |
| OD-M2-MA2-PRE | **ACCEPT_DOCUMENT_AND_FIXTURE_DESIGN_ONLY** | Acknowledge E's design package without claiming 45 tests passed or authorizing execution. | **PENDING** |
| OD-M2-MA2-CODE | **DEFER_UNTIL_RR1_AND_OWNER_API_I_FREEZE** | Alternative after all gates: explicit `SCOPED_SYNTHETIC_IMPLEMENTATION_ONLY` act naming version and worker scope. No self-activating conditional authorization. | **PENDING** |
| OD-M2-MERGE-12 | **NO_MERGE_NOW** | This proposed project policy covers main and existing PRs; no implicit release or automatic transition to READY. | **PENDING** |

`OD-M2-MERGE` in older shorthand refers to `OD-M2-MERGE-12`; do not create two conflicting acts. These decisions require a new signed Owner record, not a retroactive reclassification of the Method-G1 proposals.

## 3. Mandatory M2.MA2Input.v1 project contract for later decision

- One canonical A `execute_ma1`/`MA1Result` and exactly one SHA-verified 15-file MA1 export (14 data files plus manifest); frozen ID/row/column orientation, country map, `P`, `Gamma`, `A_z`, `A_d`, `A_z Gamma=P A_d`, source/CI SHA. The adapter from B may be used only if strict semantics and all required source data survive unchanged.
- Strict lossless HVDC, never an AC branch; operational transfers and neutral zero-HVDC/zero-PST calibration physically balanced independently for every true AC island; source / tap / transformer / fixed phase and PST semantics either verified by an explicit provider or `UNSUPPORTED_SEMANTICS` / `DEVICE_SOURCE_UNQUALIFIED`.
- Screens, critical lines and protected cuts source-qualified, immutable; audited explicit empty protection is possible, silent unexamined empty protection is not. Countries restrict clustering, **not** pan-European power flow; preserve actual AC islands, all intercountry AC ties and exact quota.
- Five externally supplied *project* weather-year IDs remain unchanged. They are not proof that ENTSO-E prescribed five weather cases. Full O26 country-budget table: 37 published labels, 102 zones, Northern Ireland and United Kingdom distinct **only in the full profile**; a synthetic fixture must be tagged `SYNTHETIC_BUDGET`.
- Real observed AC-flow discrepancy is a **separate QA metric**, not the DC KCL/KVL acceptance equality. All sources need immutable byte SHA for real admission; a declared metadata source hash is not an original-byte attestation.
- No M2.MA2Input v1 final release until source/device/protection/split/monitor policy and all R-API-P1 dispositions are adopted and tested; API-G1 is presently a **draft contract**.

## 4. Explicit project-I choices requiring further freeze before *any* MA2 code

| I-decision | Proposed scientific invariant | Unresolved Owner parameter |
|---|---|---|
| I-EQ-01/02 | Positive `x=x_ref exp(u)`, fixed source-tagged `x_ref`; one gauge per **meshed actual reduced AC island**; solver bounds finite | Gauge weights, log-x lower/upper bounds, prior/regularization λ, physical source mapping |
| I-EQ-03/06 | Check unregularized gauge-restricted Jacobian rank and conditioning; trees/insufficient excitation ⇒ `UNIDENTIFIABLE`; sparse island solver and independent dense small oracle | Rank threshold/scaling, limits, convergence, CPU/memory budgets |
| I-EQ-04/05 | Structural `c0=C alpha` with `A_z c0=0`; actual reduced solver includes affine KVL; fixed-phase/PST source provider or fail closed | Phase/source provider contract and qualification scope |
| I-ITER-01/02 | Country-pure quota-preserving 1-, 2-, 3-country atomic moves on true AC-coupled country graph; full-Europe reprojection and full x/c0 refit for every feasible nondeduplicated candidate | Neighborhood/version, determinism, candidate limits |
| I-SPLIT-01 / I-MON-01 | Frozen blocked TRAIN / SELECTION / sealed FINAL_HOLDOUT (optional embargo); fixed topologically comparable original intercountry corridor monitor catalogue and auditable protected monitors | Exact block windows, coverage policy, weights, source identity |
| I-SEL-01 / I-FAIR-01 / I-STOP-01 | Strict selection improvement; mandatory protection and monitor coverage; fairness constraint; rollback/plateau/limits with distinct `BUDGET_STOP_NOT_CONVERGED` | `delta_abs`, `delta_rel`, `J_floor`, fair RMSE limits, budget, patience |
| I-AUDIT-01 / I-TEST-01 | Write-once candidate/source/solver ledger, SHA-bound artifact manifest; fixture-oriented physical residual tests only | Effective tolerances after numeric review; E's proposal KCL 1e-8 MW, affine KVL 1e-10 rad, dense diff 1e-8 MW is **not approved** |

MA1-RP1's numerical input policy `0 < atol_mw <= 1e-6 MW` is an implementation choice, not an ENTSO-E numerical standard. No invented production RMSE, x or fairness acceptance threshold.

## 5. External ENTSO-E authority is **not** a Project-Owner decision

**E1 – Internal research authority:** the Project Owner may explicitly elect O26 as a provisional working source and own all project-I design decisions.

**E2 – External normative authority:** the Project Owner cannot certify that the 25 February 2026 consultation draft has been adopted or is effective. Mark `ENTSOE_AUTHORITY_UNCONFIRMED` pending the exact competent ENTSO-E/approval-source version, original bytes, approval/entry-into-force statement, and old/new clause delta to NR-01..NR-18. Do not confuse the consultation's three weather scenarios per target year with the five fixed *project* weather years.

**E3 – Real-source authority:** separate D0/TSO grants, source files, rights, original SHA, D1 topical-only open pilot, synchronized D2 operations/neutral and D3 security plus independent D4; current `BLOCKED_DATA`.

E1 does **not** imply E2 or E3, scientific synthetic gate success does **not** imply real or formal ENTSO-E compliance.

## 6. Auditable Owner signing block (EMPTY)

- Owner identity / documented competence / delegation: **NOT_PROVIDED**.
- Selection values for all requested decision IDs: **NOT_PROVIDED**.
- Exact Owner statement and source issue/comment URL: **NOT_PROVIDED**.
- Timestamp, version/commit(s), project scope, effective date and expiry: **NOT_PROVIDED**.
- Explicit denied scope, fixed I-values with units and limits: **NOT_PROVIDED**.
- Independent reviewer assessment and new Owner record SHA: **NOT_PROVIDED**.

A future Owner act must explicitly say whether selected options are **APPROVED, REJECTED, or RETURN_FOR_REVISION**. All unfilled options remain `OWNER_PENDING`. For an MA2 code GO, even a signed *conditional* vote becomes effective only after both independent RR1 reviews on exactly the same repaired code and all additional contract/I gates; there is no automatic transition.

**Disposition of this file: UNSIGNED_DECISION_PACK / NO_OWNER_RELEASE / NO_MERGE / NO_MA2_CODE_GO / NO_REAL_GO.**
