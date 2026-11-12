# 105 — S-GOV-M2-G2 | MA1 synthetic qualification and RR1 evidence register

**Date:** 2026-11-12. **Frozen repair code:** `fb201ef5f120f64696dea9aa99f77ece77546f9a`.
**Gate result at initial publication:** `MA1_RR1_PENDING` / `MA1_SYNTHETIC_QUALIFIED=false`.
**Evidence type:** reconciliation of available worker artifacts, not a new independent runtime re-review or Owner approval.

## 1. Verified A–E integration status

| Source | Immutable SHA | Evidentiary class | Gate consequence |
|---|---|---|---|
| RP1 W-INT | `fb201ef5f120f64696dea9aa99f77ece77546f9a` | Worker+integrator; Draft PR 41 | Repair source pinned, **not** independently qualified |
| API G1 | `ed42d051a7234f7f062d94d06291f66e56657bbc` | Read-only API/option comparison | C recommended, no chosen API |
| D SOURCE1 | `05dd0db3fc15fd6e091b8dd96d854adcedf8302c` | Metadata/37–102 table checked, no actual real grid | `BLOCKED_DATA` |
| METHOD G1 | `c980bbd341b1051257bcf31b0a904dd7937f7241` | Method authority review and Owner proposals | `OWNER_PENDING` / `ENTSOE_AUTHORITY_UNCONFIRMED` |
| MA2 PRE | `b73bb3c595bff515aeca052f02fc83f72289b5f0` | Formal design and 45 **planned** G05–G08 cases | `DESIGN_READY_ONLY` / MA2 R-NUM `NOT_RUN` |

Frozen input docs: 102/103 @ `37ee7734049d4cbe3480bb263ca68615d9140809`; RP1 report 101 @ repair SHA; RR1 contract 99 @ `27dfd810b39e17e6b616a2b0aeb813eb8948d8a0`.

## 2. Exact-worker SHA provenance (NOT reviewer release)

- Repair code `fb201ef5...`, parent `70e92ba9e62a320e58227ce9c2f03fad266f44bf`; only M2 source, tests, review workflow and RP1 documentation changed.
- SHA-specific **push** CI `https://github.com/AlOussama/TYNDP_Products/actions/runs/43113044448`: 66 focused PASS + 92 full PASS, zero failed/error/skipped, as reported in 101 and issue #14/#15 worker handoff. Artifact `https://github.com/AlOussama/TYNDP_Products/actions/runs/43113044448/artifacts/13897013086` stores JUnit and synthetic witness.
- One 15-file MA1 export: **14 hashed payloads + manifest**, with source/code/check-out and output binding in evidence. The passing PR event's temporary merge SHA is **not** a substitute for the pinned push checkout SHA.
- PHY-R01: caller-owned sequence mutation/fingerprint; PHY-R02: `lossless="False"`; PHY-R03: `in_service="False"`; PHY-R04: `atol_mw=inf/nan/huge` or [+20,-19] MW per island: `FIXED_BY_WORKER_TEST`, independent closed status **NOT ESTABLISHED**.
- CLU-001 protected seed bounded exact recovery / `HEURISTIC_STUCK` versus complete `PROVEN_INFEASIBLE`; CLU-002 unaudited class0 on true 400 kV; worker enumeration 729 labeled 4-vertex 3-state edge graphs, k=1..4, 1804 feasible, 0 worker false infeasibility. CLU-003/004 fingerprint/page fixes; CLU-005 opt-in country alias normalization and declared metadata provenance. All **worker** outcomes, never independent RR1 certification.
- Known bounded algorithmic limits: exact merge-state DFS capped at up to **16 vertices / 100000 distinct states**; depletion yields `HEURISTIC_STUCK` not mathematical infeasibility. Greedy success not a global optimum proof.
- Screening test: nominal 400 kV, flow 100 MW, normal limit 10 MW, duration 1 h = **90 MWh/year**; source-qualified 220→225 and 380→400 mapping still required. `screening_class_kv=0` cannot silently exempt a true 225/400 line.

## 3. Independent RR1 acceptance matrix

The following are required **separate results**. At initial G2 evidence publication, neither complete RR1 decision / reviewer CI evidence has been admitted. No inference from an empty open issue or a newly created review branch.

| Required fact | R-PHY-RE | R-CLU-RE | Current G2 status |
|---|---|---|---|
| Independent reviewer different from W-PHY/W-CLU/W-INT and other RR1 reviewer | Identity + independent authorship attest | Identity + independent authorship attest | **NOT_VERIFIED** |
| Exactly same repaired **implementation code** SHA or byte-for-byte source tree compared to `fb201ef5...` | actual `git rev-parse`, code diff and source hashes | actual `git rev-parse`, code diff and source hashes | **NOT_VERIFIED** |
| Own source-control review branch and immutable report/findings/JUnit/CI run+job+artifact SHA | required | required | **NOT_PRESENT_AT_GATE** |
| Repeat originally failed cases without weakening original reviewer tests | PHY-R01..04 as ordinary PASS | CLU-001..005 explicitly dispositioned | **PENDING** |
| New, independently derived numerical/graph attacks | 10 bus / 3 AC islands / 2 HVDC / PST KCL KVL, 1001 sparse, 15-file witness and failure/clock/rating/source tests | complete 729-state enumeration / all 1804 feasible, zero false-infeasible/false rejection, 90-MWh 400kV, larger multi-country/protected attacks | **PENDING** |
| No reproducible open P0/P1 at tested integrated code; P2 separately accepted with scope/owner | required | required | **NOT_DETERMINABLE** |
| Positive independently reasoned reviewer decision | `ACCEPT_SYNTHETIC` | `ACCEPT_SYNTHETIC` | **PENDING** |

*Same code* means a reviewer branch with additional independent tests may have a different commit SHA, but its audited `src/tyndp_reduce/iosn_official` implementation must be byte-identical to the integrated repair code at `fb201ef5...`. A new worker modification or different implementation SHA invalidates reconciliation and requires new pairwise re-reviews.

**Issue inputs / update points:** `https://github.com/AlOussama/TYNDP_Products/issues/14` (R-PHY), `https://github.com/AlOussama/TYNDP_Products/issues/15` (R-CLU). Do not close issue using Worker confirmation alone.

## 4. Final MA1 synthetic release predicate — all TRUE before status change

1. Frozen integrated code SHA `fb201ef5...`, checked in both independent replays; reviewer reports include exact commit/code tree and independent run provenance. Reviewers not the RP1 implementation workers.
2. PHY-R01..04 demonstrably PASS on original attacks plus new numerical tests, with numerical tolerance finite and `0 < atol_mw <= 1e-6 MW` as implementation preflight, not an official universal physical tolerance; verify scale-aware KCL/cycle/oracle with independent checks.
3. CLU enumeration 729 states / 1804 feasible cases / 0 false `PROVEN_INFEASIBLE` or false feasible rejection; all country quotas, AC-connectedness, protected cuts and cross-border original graph preserved, 90 MWh/year true 400-kV fixture, generator/tuple stable SHA, exact UK page 27, NI/UK separated.
4. All independent report P0/P1 closed as a **reviewer finding**, not just `FIXED_BY_WORKER_TEST`. Every P2 has explicit scope and disposition. Country alias metadata does **not** certify original source bytes; no real-data claim.
5. G01–G05 invariants reproduced, including actual AC-island balance, finite flags/tolerances, screening and `A_z Gamma=P A_d`, signed border flow preservation, source/time/order alignment, exact 15-file verified export. G11 retains `PARTIAL_LOSSLESS_DC_ONLY` with strict device/transformer exclusions.
6. Optional distinct Owner API/contract choice may follow or precede reviewer results, but a positive **code-only MA1 synthetic scientific qualification** must not be represented as Owner release if that choice is pending. No MA2 code until explicit API/I freeze and a separate Owner code authorization.

If all reviewer scientific conditions are met, S-GOV may document **MA1_SYNTHETIC_QUALIFIED within the explicitly frozen lossless-DC synthetic fixture scope**, keeping `OWNER_PENDING` as a separate possible state. If any independently reproducible P0/P1 remains, choose `REPAIRS_REQUIRED`, new implementation SHA and **both** new independent reconciled re-reviews as applicable. If source/contract provenance cannot be shown, `BLOCKED_CONTRACT` rather than an optimistic PASS.

## 5. Current gate ledger and prohibited inferences

| Gate | Initial evidence-backed classification |
|---|---|
| G01–G05 / worker | `PASS_SYNTHETIC_WORKER_TESTS` (not RR1 qualified) |
| G11 | `PARTIAL_LOSSLESS_DC_ONLY` (no general AC device qualification) |
| MA1_RR1_PHY / MA1_RR1_CLU | `PENDING` / `PENDING` |
| MA1_SYNTHETIC_QUALIFIED | `false` |
| Project-Owner API and MA2 authorization | `OWNER_PENDING` / `MA2_CODE_NOT_AUTHORIZED` |
| G06–G08 / future R-NUM | `NOT_IMPLEMENTED` / `NOT_RUN` |
| G12 / real grid, real dispatch/neutral, TSO N-1 | `BLOCKED_DATA`; `REAL_QUALIFIED=false` |
| ENTSO-E adopted/effective version and authority | `ENTSOE_AUTHORITY_UNCONFIRMED` |
| Main / PR #13 / PR #41 release | `NO_MERGE_NOW` recommendation; both PRs remain Draft/open/unmerged in latest available source checks |

**Gate act now:** `G2_PREPARED_NO_RELEASE`. It is neither an adverse review finding nor a positive scientific/Owner approval. Update this file only through a new evidence-specific gate revision with named reviewer report commits and CI, never retroactively declare these initial fields passed.
