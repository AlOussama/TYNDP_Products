# 107 — S-GOV-M2-G2 | Next admissible macro handoffs and hold points

**Date:** 2026-11-12. **State:** `G2_PREPARED_NO_RELEASE`.
**Use:** Copy-ready task boundaries, not permission to run deferred MA2 code. Starting another G2 or an RR1 review is not needed if an equivalent signed independent execution is already active; reconcile its evidence rather than count it twice.

## M2-G2-OWNER-ACT — Now executable as an Owner decision request (documentation only)

**Role:** competent repository Project Owner (not S-GOV acting as the Owner).
**Input:** [document 104](104_M2_G2_OWNER_DECISION_REGISTER_20261112.md), [105](105_M2_G2_MA1_SYNTHETIC_GATE_EVIDENCE_20261112.md), [106](106_M2_G2_MA2_SYNTHETIC_IMPLEMENTATION_DECISION_PROPOSAL_20261112.md), API G1 `ed42d051a7234f7f062d94d06291f66e56657bbc`, Method G1 `c980bbd341b1051257bcf31b0a904dd7937f7241` and MA2-PRE `b73bb3c595bff515aeca052f02fc83f72289b5f0`.

Ask the Owner to issue a signed, explicit choice for `OD-M2-API-01..05`, `OD-M2-METH-01`, `OD-M2-SCOPE-11`, `OD-M2-MA2-PRE`, `OD-M2-MA2-CODE` and `OD-M2-MERGE-12`. Strong recommendation: API option C, A (`iosn_official`) sole canonical, optional one-way type-checked B converter; strict lossless v1; separate measured-flow QA; audited screening/protection, O26 provisional scientific baseline, no merge, and MA2 code **DEFER** until independent RR1 plus accepted I-contract. Require precise scope, owner authority, timestamp, issue URL, commit SHA and all testable I-values before an implementation decision can become effective.

The Owner may decide **project** API/method working baseline/I values; the Owner cannot declare ENTSO-E's 25 February 2026 consultation draft adopted/effective. Preserve E2 `ENTSOE_AUTHORITY_UNCONFIRMED`. If no explicit Owner act, return `OWNER_PENDING`, not presumed assent.

**Output:** separate traceable Owner act and signed register revision. **No Worker/MA2 code, main merge or REAL release under this macro.**

## M2-MA1-RR1-R-PHY — Independently continue/complete now

**Role:** reviewer independent of W-PHY/W-CLU/W-INT and R-CLU-RE. **Exact repair implementation:** `fb201ef5f120f64696dea9aa99f77ece77546f9a`. Read original R-PHY review `c004e5330df2a018e567c8ef955ef2fc9d71e0ea`, report 101 and RR1 contract 99; honor Handoff 103.

Re-run four original P1 attack inputs as true ordinary PASS without weakening original historic strict-XFAIL tests. Derive a separate 10-bus/3-AC-island/2-HVDC/PST dense cycle/KCL/KVL test, 1001 sparse, finite/bounded tolerance, UTC and source/rating/15-file fingerprint. Independently publish code source tree hash, JUnit, run/job/artifact IDs, new independent P0/P1/P2 ledger and `ACCEPT_SYNTHETIC` vs `REPAIRS_REQUIRED` on own branch; update [Issue #14](https://github.com/AlOussama/TYNDP_Products/issues/14). A reviewer branch that adds tests may differ in SHA but must prove `iosn_official` code identical to repair SHA.

**Do not perform Owner signature, main merge, MA2 code or real qualification.** Do not reassign if already running.

## M2-MA1-RR1-R-CLU — Independently continue/complete now

**Role:** different reviewer, not W-PHY/W-CLU/W-INT or R-PHY-RE. **Exact repair implementation:** same `fb201ef5f120f64696dea9aa99f77ece77546f9a`. Read original R-CLU report/ledger `7d7d07d7af5966ddc26d0be1100a69013763d2e8`, report 101 and RR1 contract 99; honor Handoff 103.

Independently enumerate 729 labelled 4-node edge-state graphs and k=1..4, all 1804 feasible graph/quota cases; require 0 false infeasible and 0 false feasible rejection. Distinguish `HEURISTIC_STUCK` from `PROVEN_INFEASIBLE` and report resource bounds. Verify nominal 400-kV 100MW/10MW/1h = 90 MWh per year, fail-closed unknown 380/220 mapping and class0 exclusion. Audit generator versus tuple SHA, source page UK 27, NI/UK distinct, opt-in alias metadata versus original bytes; devise larger multi-country protected/corridor/AC island attacks and source/15-file hashes. Publish independent code source tree identity, findings/JUnit/CI, P0/P1/P2 and `ACCEPT_SYNTHETIC` vs `REPAIRS_REQUIRED`; update [Issue #15](https://github.com/AlOussama/TYNDP_Products/issues/15).

**No worker self-signoff, Owner code approval, merge or real qualification.** Do not reassign if already running.

## M2-D-SOURCE-OWNER — Parallel, external source only

**D0 / [Issue 35](https://github.com/AlOussama/TYNDP_Products/issues/35):** institutional owner requests genuine European/TSO 2025 grid and 2035 changes, licensed source/permission/NDA scope, voltage, 110kV ties, transformer/HVDC/PST/protection and original SHA. Do not post confidential bytes/identity tokens.

**D1 / [Issue 36](https://github.com/AlOussama/TYNDP_Products/issues/36):** acquire original bytes of PyPSA-Eur OSM Zenodo 14144752 v0.6 named five CSV files; verify published MD5, independently compute SHA256, licenses, two-country genuine AC cycle with complete induced equipment. Label result `REAL_TOPOLOGY_ONLY`, not official 37/102/grid dispatch/neutral or N-1 proof.

**D2 / [Issue 37](https://github.com/AlOussama/TYNDP_Products/issues/37):** obtain exact five externally determined project weather-year IDs, synchronized original-bus nodal MW, UTC/season/duration, signed HVDC/PST, separately balanced physically qualified neutral reference and independent real flow oracle. No re-selection.

**D3 / [Issue 38](https://github.com/AlOussama/TYNDP_Products/issues/38):** authentic TSO outage lists, normal/emergency/seasonal ratings, monitored assets, exceptions and 4 directional×seasonal security cases; no synthetic contingency or rating masquerading as a real TSO certificate.

**D4 / [Issue 39](https://github.com/AlOussama/TYNDP_Products/issues/39)** may start only after exact raw bytes/manifests and source rights have been frozen. Without external access label `BLOCKED_SOURCE_ACCESS`; never invent credentials or witness.

## M2-MA2-PRE-R — Optional immediately: independent formal *document-only* review

**Role:** mathematically independent numeric optimization/power systems reviewer. **Input:** E design `b73bb3c595bff515aeca052f02fc83f72289b5f0`, original Handoff 85 and conditional 100. Check gauge and rank per true meshed AC island, affine KVL including fixed phases, structural c0, separate real versus neutral sources, 2/3-country admissibility, global refit per candidate, fixed corridor monitors, selection/holdout, fairness and leakage. Audit all **45 planned** oracle cases, proposed tolerances and owner-I parameters. Publish P0/P1/P2 **design** findings only. Do not claim `MA2_IMPLEMENTED` or `R_NUM_PASS`, run production code or open holdout.

## S-GOV-M2-G2-RR1-CLOSE — Only after both independent RR1 reports exist

**Role:** S-GOV Governance coordinator; read-only evidence reconciliation. Fetch both *published* reviewer reports, their exact tested implementation and own CI SHA, independent authors and issue comments. Verify both source trees reproduce `fb201ef5...`, both decisions positive, all scientific P0/P1 = 0, P2 explicitly scoped, all G01–G05 and G11 constraints. A repair changing implementation code forces new evidence. Publish revision of [105](105_M2_G2_MA1_SYNTHETIC_GATE_EVIDENCE_20261112.md) and machine ledger with both immutable independent URLs. Emit one of `MA1_SYNTHETIC_QUALIFIED` (narrow lossless DC fixtures), `REPAIRS_REQUIRED`, `BLOCKED_CONTRACT` or `RR1_PENDING`. Preserve `OWNER_PENDING` if no Owner signature, `BLOCKED_DATA` and `ENTSOE_AUTHORITY_UNCONFIRMED`.

**No inferred MA2 GO, merge, or real qualification even after synthetic PASS.**

## M2-MA2-CODE — NOT STARTABLE until new explicit Owner release

**Gate:** the strict conjunction in [106](106_M2_G2_MA2_SYNTHETIC_IMPLEMENTATION_DECISION_PROPOSAL_20261112.md). After actual RR1 and Owner API/strict device/split/monitor/I acceptance, require separate expressly signed `SCOPED_SYNTHETIC_IMPLEMENTATION_ONLY` instruction. Only then issue W-EQ/W-ITER/W-INT and later independent R-NUM on an entirely separate implementation/review SHA, following conditional Handoff 100 and the 45 designed tests; no changes to M0/M1/weather or main. No synthetic acceptance can substitute for real-source D4 or ENTSO-E authority, and MA3 remains downstream separately gated.

**Current next action classification:** RR1 + Owner choices + source-owner requests + optional PRE-design review `STARTABLE_NOW`; RR1 close `WAIT_FOR_TWO_REPORTS`; MA2 code `BLOCKED_BY_RR1_AND_OWNER`; REAL/MA3 `BLOCKED_DATA_AND_SEPARATE_AUTHORIZATION`.
