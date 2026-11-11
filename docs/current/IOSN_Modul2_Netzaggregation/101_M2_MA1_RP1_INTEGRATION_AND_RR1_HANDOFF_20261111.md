# M2-MA1-RP1 — W-INT integrated worker repair and independent RR1 handoff

**Scope:** Module 2 `iosn_official` only. W-PHY and W-CLU were committed
separately, sharing immutable parent `70e92ba9e62a320e58227ce9c2f03fad266f44bf`.
This single integrator commit includes both code lines, additional numerical
reference tests, a full-package CI workflow, evidence-binding manifest fields,
and this worker findings ledger. No changes to M0, M1, legacy m2 or weather selection.

## 1. Worker commits and independently sourced findings

- **W-PHY:** [`4f235dc90b1e5ad9119a811ff1d96ff97c9d29b7`](https://github.com/AlOussama/TYNDP_Products/commit/4f235dc90b1e5ad9119a811ff1d96ff97c9d29b7).
  Dedicated [MA1 CI 43112239447](https://github.com/AlOussama/TYNDP_Products/actions/runs/43112239447):
  54 passed; [full CI 43112240030](https://github.com/AlOussama/TYNDP_Products/actions/runs/43112240030):
  80 passed. Four PHY P1 tests now pass without xfail.
- **W-CLU:** [`763f90039cf4ac3b49e8e0f68c1b8b8f890c2689`](https://github.com/AlOussama/TYNDP_Products/commit/763f90039cf4ac3b49e8e0f68c1b8b8f890c2689).
  Dedicated [MA1 CI 43112243743](https://github.com/AlOussama/TYNDP_Products/actions/runs/43112243743):
  34 passed; [full CI 43112243718](https://github.com/AlOussama/TYNDP_Products/actions/runs/43112243718):
  60 passed. The worker test includes the independent-oracle-style complete
  729 labelled four-node graph cases, k=1..4, 1804 feasible cases and zero
  false-infeasible results. These are worker tests, not an independent R-CLU result.

Original **unmodified** reviewer witnesses:
[R-PHY report & findings](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md);
[R-CLU report & findings](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md).
Their original strict-XFAIL or defect-asserting tests must not be edited by implementers.

## 2. Implemented repair contracts and explicit limits

- **PHY-R01/R02/R03/R04:** tuple-owned frozen contract sequences,
  genuine bool for lossless/service/gap/provenance, no caller mutation of
  topology/fingerprint, and owner-choice numerical tolerance `0 < atol_mw <= 1e-6`
  with finite-only physical acceptance. The numerical bound is an
  implementation I-choice, **not** attributed to ENTSO-E.
- **CLU-001:** existing deterministic cost greedy preserved on success.
  On stuck countries, restart from singleton buses with deterministic bounded
  exact merge-state DFS (up to 16 vertices/100000 distinct states).
  Only a fully exhausted within-budget state-space may return
  `PROVEN_INFEASIBLE`; resource/time limit yields `HEURISTIC_STUCK`.
  Neither this nor the heuristic proves optimality of European cluster quality.
- **CLU-002:** unqualified class=0 cannot opt an eligible 225/400 nominal
  line out of screening. The chosen policy **rejects** unaudited exclusion;
  no unpublished protected-policy or method B is invented.
  220/380 declarations still depend on upstream source-class verification;
  device-/source-qualified exemptions require a separate versioned contract.
- **CLU-003/004:** protected IDs canonicalized/validated exactly once;
  Table 3 row-specific printed pages verified, including UK on page 27.
- **CLU-005:** opt-in M2-only `canonicalize_country_aliases` records original
  labels, declared source URI/SHA and a manifest digest; NI and UK are pinned
  distinct. This is not an original-byte attestation or a blanket raw-alias
  permission. Existing fail-closed `resolve_country_ids` remains in place;
  adapter callers must explicitly construct a new M2 snapshot with fresh
  normalization provenance.

## 3. W-INT execution and SHA-bound evidence contract

CI workflow `.github/workflows/m2-ma1-rp1-verify.yml` runs **focused**
G01–G05/G11 regression, the complete 729*4/1804 feasible enumeration,
W-INT 10-bus/3-AC-island/2-HVDC/2-PST independent dense KCL and affine-cycle
oracle, 1001-bus sparse chain, the full Python test suite, and
`fixture_evidence --commit "$(git rev-parse HEAD)"`.
Its JUnit outputs, 15-file synthetic fixture (14 hashed output files plus
manifest), tested checkout SHA and content digests are uploaded as one
retained GitHub artifact.

`MA1Result.export` now additionally records:
`ratings_content_sha256`, sorted `protected_line_ids`,
`budget_source_sha256`, `budget_source_page_by_country` (only for
official budget), and a non-claiming synthetic page-evidence flag.
The actual Git checkout SHA must be corroborated by CI, not trusted from
the caller-provided `code_commit` alone.

The machine-readable per-finding status and blocks are in
`M2_MA1_RP1_WORKER_FINDINGS_20261111.json` adjacent to this document.
`FIXED_BY_WORKER_TEST` means worker tests passed, **not independently
verified or release-qualified**.

## 4. Exactly two independent RR1 requests (same W-INT SHA)

**R-PHY-RE (new independent reviewer):** use the integrated repair-branch
**exact final GitHub commit** (not either worker SHA) and
[RR1 handoff 99](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/99_M2_MA1_RR1_INDEPENDENT_REREVIEW_AND_GATE_20261111.md).
Replay original four strict-XFAIL attack inputs as ordinary, independently
authored PASS assertions on a new review branch, without modifying original
witnesses. Repeat fresh 10-bus cycle/KCL/KVL, 1001-bus sparse and 15-file SHA
fixture. Document any P1/P2 and independent CI.

**R-CLU-RE (different reviewer):** same integrated SHA, independently verify
zero false infeasible among **1804** feasible inputs across 729 graphs,
correct separation of `PROVEN_INFEASIBLE` and `HEURISTIC_STUCK`,
90 MWh/year 400-kV minimal case, generator fingerprints, UK source page,
and NI/UK protection, plus larger multi-country cases. Record elapsed resource
counts and SHA-bound CI. No worker self-review.

Only after *both* distinct reviews may S-GOV decide a narrowly scoped
MA1 synthetic gate. **NO_MERGE, NO_MA2_RUNTIME_GO, REAL_QUALIFIED=false,
G11_PARTIAL_LOSSLESS_DC_ONLY and 37/102 BLOCKED_DATA** remain in force.
