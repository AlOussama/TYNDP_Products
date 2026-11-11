# R-M2-MA1-PHY — Independent Physical Foundation Review

**Review-ID:** R-M2-MA1-PHY-20261111  
**Date (UTC):** 2026-11-11  
**Repository:** `AlOussama/TYNDP_Products`  
**Role:** independent scientific-technical reviewer, **not** W-PHY or W-INT  
**Decision:** **REPAIRS_REQUIRED** — four independently reproduced **open P1** findings; zero demonstrated P0.  
**Release boundary:** neither `ACCEPT_SYNTHETIC` nor `REAL_QUALIFIED` is authorized by this review. No merge, no MA2 runtime admission, no M0/M1/weather-year changes.

## 1. Frozen sources, verification and independence

| Object | Verified reference / role |
|---|---|
| W-PHY/integrated **code freeze** | [`0254d867a34b66ec7b56c90225605d29ea328916`](https://github.com/AlOussama/TYNDP_Products/commit/0254d867a34b66ec7b56c90225605d29ea328916) |
| Documented MA1 completion/head | [`70e92ba9e62a320e58227ce9c2f03fad266f44bf`](https://github.com/AlOussama/TYNDP_Products/commit/70e92ba9e62a320e58227ce9c2f03fad266f44bf) |
| Baseline pre-MA1 | `2d0b830375c71f3e727d303cdd2ca037da1c67f4` |
| Parent of this review branch | `70e92ba9e62a320e58227ce9c2f03fad266f44bf` |
| Independent test/workflow commit | [`c0dd75de1285296da420fd0eb77d29f60efd7d92`](https://github.com/AlOussama/TYNDP_Products/commit/c0dd75de1285296da420fd0eb77d29f60efd7d92) |
| Review branch | [`review/iosn-m2-ma1-r-phy-independent-20261111`](https://github.com/AlOussama/TYNDP_Products/tree/review/iosn-m2-ma1-r-phy-independent-20261111) |
| Original implementation | [Draft PR #13](https://github.com/AlOussama/TYNDP_Products/pull/13) |
| Reviewer gate | [Issue #14](https://github.com/AlOussama/TYNDP_Products/issues/14) |
| Input documents | [81](81_M2_MA1_COLD_START_HANDOFF_2026_11_03.md) · [82](82_M2_MA1_EXECUTION_REPORT_2026_11_04.md) · [83](83_M2_MA1_R_PHY_REVIEW_STATUS_2026_11_04.md) · [80](80_M2_NETWORK_AGGREGATION_REVIEW_AND_EXECUTION_PLAN_2026_11_03.md) |

The GitHub API resolves both complete commits. `0254d...` is eight commits ahead of the stated input baseline, and `70e...` is exactly three further **documentation-only** commits after that code freeze. The file-level change comparison from baseline to code freeze contains only `src/tyndp_reduce/iosn_official/**`, `tests/iosn_official/**` and the MA1 CI workflow. This R-PHY review branch adds **only independent tests, numeric witness scripts, CI and review documentation**; it does not modify production source, the separate W-PHY worktree, M0/CGMES, M1/PECD or weather selection.

The review did **not** reuse W-PHY's dense oracle as an acceptance criterion. The new test constructs an independent KCL plus **cycle-space KVL** solution with `scipy.linalg.null_space` and a direct least-squares system, while the production solver uses sparse per-island Laplacian `splu`. This is algorithmic independence within the present reviewer context, not a claim of a separate human signature or real-network qualification.

## 2. Independently executed evidence

- [GitHub Actions run #43077807614](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077807614), event `push`, tested SHA `c0dd75de1285296da420fd0eb77d29f60efd7d92`, conclusion **success**.
- [Job #130722144343](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077807614/job/130722144343) includes exact commands, timestamps, test summaries and independent numerical residuals.
- [Artifact #13881368283](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077807614/artifacts/13881368283) includes JUnit XML, two pytest logs, `numerical_metrics.json`, fixture summary, source checkout SHA, recomputed output SHA list and synthetic fixture output.
- `python -m pytest -q -rx tests/iosn_official`: **31 passed, 4 xfailed**. `python -m pytest -q -rx`: **57 passed, 4 xfailed**. All four are strict, intentional XFAIL reproductions of *open* defects. The CI job being green does **not** mean the four cases passed. The pre-existing MA1 and full package regressions otherwise passed.
- Independently executed 10-bus network: **12** AC branches (including one fixed-angle transformer and two PST), **3 electrical AC islands**, **5 independent cycle constraints**, **2** lossless HVDC corridors (one with a negative transfer schedule), **5** explicit synthetic year-snapshots, mixed country labels within one AC mesh. The original grid is solved globally, not per country. An independently built dense cycle-space reference produces:

| Independent numeric quantity | Maximum absolute measured residual |
|---|---:|
| Detailed nodal KCL, `||A f-p||∞` | `1.4210854715202004e-14 MW` |
| Sum of net terminal-adjusted injections per island | `5.329070518200751e-15 MW` |
| Sparse solver vs independent cycle-space least-squares reference | `2.7107205369247822e-12 MW` |
| Cycle-space affine KVL, `||Cᵀ(diag(x/Sbase)f+φ)||∞` | `6.071532165918825e-18 rad` |

Further positive checks: reversing PST orientation and HVDC terminal direction together with their signed controls preserves physical node injections and other flows; changing an inter-island HVDC control without matched redispatch is rejected; missing PST control, lossy-HVDC declaration, unknown SVC, missing 110-kV ties, invalid MW/MVA rating units, non-UTC and unsorted timestamps fail closed. A **1001-bus/1000-line** chain was solved using the sparse graph path without construction of a dense production PTDF matrix. This checks functional sparse behavior, **not** full European scale/memory performance.

The published implementation fixture was independently regenerated under the same review CI: two islands, three countries, five MOCK years, `preflight_status=PASS`, **14** manifest-hashed output files, input digest `a378e22fde234cdf9275bcb5685f1034c1e41eeb442b81a8cfe06ed988882661`. Its two release flags remain **false**.

**Numerical scope:** `physical.py` provides a sparse islandwise DC-flow calculation, not a public explicit PTDF tensor. This satisfies the MA1 option “sparse PTDF/Lastfluss-Ansatz oder geeigneter Solver”; no sparse PTDF API or general PyPSA parity is certified.

## 3. Independent findings ledger

### PHY-R01 — P1 / OPEN — Mutable sequence fields violate the immutable contract

**Affected:** [contracts.py L103–L141](https://github.com/AlOussama/TYNDP_Products/blob/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official/contracts.py#L103-L141); similarly `TimeSet`, `ReferenceDispatchSet` and cache tuple annotations.  
**Reproducer:** `test_known_repro_mutable_grid_branch_list_must_not_mutate_after_validation`. Supply `ac_branches` as a Python `list` to a frozen `DetailedGridSnapshot`, then append a new branch to the caller-owned list after validation.  
**Expected:** Type rejection at construction or owned canonical immutable tuple; fingerprint and physical topology cannot change through external list mutation.  
**Actual:** The frozen dataclass retains the same live list and the supposedly immutable `grid.fingerprint()` changes without a replacement object or validation. This allows time-of-check/time-of-use inconsistencies between preflight and reference/manifest stages.  
**Worker repair:** Reject mutable sequence inputs or defensively convert/copy all tuple-like contract fields before validation; test post-construction mutations and hashes. No source code was changed by R-PHY.

### PHY-R02 — P1 / OPEN — HVDC `lossless` accepts truthy nonboolean flags

**Affected:** [contracts.py L89–L99](https://github.com/AlOussama/TYNDP_Products/blob/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official/contracts.py#L89-L99).  
**Reproducer:** `test_known_repro_lossless_string_flag_must_fail_closed`; construct `HVDCTerminals("bad", "a0", "a1", lossless="False")`.  
**Expected:** `DataContractError` or explicit type rejection of a nonboolean/unqualified loss model.  
**Actual:** The truthy string `"False"` bypasses `if not self.lossless` and is admitted as a lossless HVDC link. This can hide a lossy/asymmetric terminal model under a lossless calculation.  
**Worker repair:** Enforce `type(lossless) is bool`, then reject `False`; test string, integer and other invalid states.

### PHY-R03 — P1 / OPEN — AC `in_service` accepts truthy nonboolean flags

**Affected:** [contracts.py L60–L85](https://github.com/AlOussama/TYNDP_Products/blob/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official/contracts.py#L60-L85) and [L129–L131](https://github.com/AlOussama/TYNDP_Products/blob/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official/contracts.py#L129-L131).  
**Reproducer:** `test_known_repro_branch_service_status_string_must_fail_closed` with `in_service="False"`.  
**Expected:** Malformed service status is rejected before topology construction.  
**Actual:** Constructor admits the string and `active_branches` includes the branch because `"False"` is truthy. The resulting solver can fabricate AC connectivity across an out-of-service corridor.  
**Worker repair:** Enforce true `bool` values for service and related safety flags (`incomplete_110kv_ties`, `Provenance.synthetic`) and add explicit nonboolean negative tests.

### PHY-R04 — P1 / OPEN — Public numerical tolerance can bypass island balance and KCL

**Affected:** [physical.py L44–L51](https://github.com/AlOussama/TYNDP_Products/blob/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official/physical.py#L44-L51) and [L92–L113](https://github.com/AlOussama/TYNDP_Products/blob/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official/physical.py#L92-L113).  
**Reproducer:** `test_known_repro_infinite_tolerance_must_not_bypass_island_kcl`; a two-bus/one-line island with injections `[+20, -19] MW`, and `atol_mw=float("inf")`.  
**Expected:** Nonfinite/unsafe tolerance is invalid; a 1-MW unbalanced island must never produce a physically accepted reference flow.  
**Actual:** `abs(imbalance) <= inf` passes and `abs(residual) > inf` is false; the routine returns a cache although the implied slack/reference node leaves a 1-MW KCL residual. Excessively large *finite* tolerances pose the same issue.  
**Worker repair:** Require a scientifically bounded finite tolerance (or make physical acceptance tolerance internal and non-overridable) plus a separate hard residual/balance gate; test infinity, NaN, huge finite values and unbalanced islands.

**P0:** no P0 reproduced within the tested synthetic input classes. **P1:** four open physical/contract findings. **P2 / evidence limitations:** declared source SHA-256 values are syntactically validated, but original source **bytes** are not rehashed or independently attested; the exported `code_commit` is a caller-provided string and must be matched externally to the actual checkout (the review workflow does this by using `$GITHUB_SHA`). Those limitations must not be misreported as verified real-data provenance.

The machine-readable ledger is published separately in [`R_M2_MA1_PHY_FINDINGS_20261111.json`](R_M2_MA1_PHY_FINDINGS_20261111.json).

## 4. Reproduction procedure

On the **review** branch at `c0dd75de1285296da420fd0eb77d29f60efd7d92` (not the production code-freeze alone):

```bash
git checkout c0dd75de1285296da420fd0eb77d29f60efd7d92
python -m pip install -e ".[test]"
python -m pytest -q -rx tests/iosn_official
python -m pytest -q -rx
python tests/iosn_official/r_phy_numerical_metrics_20261111.py /tmp/rphy-metrics.json
python -m tyndp_reduce.iosn_official.fixture_evidence \
  --output /tmp/rphy-evidence-new --commit "$(git rev-parse HEAD)"
```

The fixture output directory must not exist beforehand. Strict XFAILs document **confirmed open bugs**, not evidence for an acceptance decision. A worker repair should convert all four to actual PASS results; strict XPASS triggers a new red gate until reviewed/reclassified.

## 5. Residual blockers (not silently repaired in Module 2)

- **B-DATA-01 / P1 admission blocker:** no independently verified byte-for-byte source provenance for a complete European network, 37 country labels/102 zones, actual physical grid/tie topology, synchronized real dispatch, original five weather-year series, MW limits, emergency ratings, N-1 inputs and TSO assumptions. A syntactic SHA field is not a source witness.
- **B-DEVICE-02 / P1 integration blocker:** nontrivial transformer tap ratios, HVDC conversion/loss models, PST operating semantics, storage/control assets and their original PyPSA/TSO equipment mapping lack a validated real adapter and independent n.lpf or equivalent parity witness; only the explicitly supported lossless-DC subset has passed synthetic checks.
- **B-GOV-03:** R-CLU Issue #15 remains a separate independent gate. Completion of this R-PHY review does not satisfy R-CLU, complete G11, G12, N-1, or MA2/MA3 runtime gates.
- **B-ARCH-04:** the alternative `src/tyndp_reduce/m2/` line must be reconciled before choosing a canonical production contract; do not silently merge branches.

## 6. Required repair / re-review sequence and final decision

1. **W-PHY (separate implementer)** fixes PHY-R01 through R04 on a new worker repair commit, without editing the independent reviewer tests to suppress failures.
2. **R-PHY (different reviewer)** rechecks the pinned repair SHA, runs the four strict repros as regular PASS, repeats the ten-bus independent oracle, 1001-bus sparse test, full regression, and source/status hashes. Publish repaired/new findings, numeric residuals and run/job URL.
3. **S-GOV / Owner** may revisit `ACCEPT_SYNTHETIC` *only* after no open P0/P1 gates, R-CLU's own review and full independent evidence reconciliation. Actual real-network approval remains blocked until source and model witnesses exist.

**R-PHY verdict on 2026-11-11: `REPAIRS_REQUIRED`.** The demonstrated lossless-DC arithmetic is accurate on independently constructed synthetic multi-island cases; fail-closed input integrity is not yet sufficient for synthetic release. This report does not assert completed repairs, an independent re-review of a future worker SHA, real-network qualification, merge or runtime release.
