# M2-MA1-RR1-PHY — Independent Physical Repair Re-Review

**Review date:** 2026-11-12  
**Reviewer:** Independent scientific physical/sparse-numerics review, separate test and evidence branch; not W-PHY/W-INT  
**Verdict:** **ACCEPT_SYNTHETIC** — **only for the reviewed lossless-DC physical MA1 synthetic scope**, without an Owner release.  
**Repository:** AlOussama/TYNDP_Products  
**Exact repaired code SHA:** [fb201ef5f120f64696dea9aa99f77ece77546f9a](https://github.com/AlOussama/TYNDP_Products/commit/fb201ef5f120f64696dea9aa99f77ece77546f9a)  
**Reviewer test/CI SHA:** [fa097c23a71510ad1feb0ed327b76b4ed95955ca](https://github.com/AlOussama/TYNDP_Products/commit/fa097c23a71510ad1feb0ed327b76b4ed95955ca)  
**Review branch:** [review/iosn-m2-ma1-rr1-phy-20261112](https://github.com/AlOussama/TYNDP_Products/tree/review/iosn-m2-ma1-rr1-phy-20261112)  
**Issue:** [#14](https://github.com/AlOussama/TYNDP_Products/issues/14)

## 1. Immutable input, review independence and pinned code

Read and reconciled the [original R-PHY report 87](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md), its [original findings ledger](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/R_M2_MA1_PHY_FINDINGS_20261111.json), the [original strict-XFAIL test commit c0dd75de](https://github.com/AlOussama/TYNDP_Products/blob/c0dd75de1285296da420fd0eb77d29f60efd7d92/tests/iosn_official/test_r_phy_independent_20261111.py), the [RP1 report 101](https://github.com/AlOussama/TYNDP_Products/blob/fb201ef5f120f64696dea9aa99f77ece77546f9a/docs/current/IOSN_Modul2_Netzaggregation/101_M2_MA1_RP1_INTEGRATION_AND_RR1_HANDOFF_20261111.md), the original [RR1 contract 99](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/99_M2_MA1_RR1_INDEPENDENT_REREVIEW_AND_GATE_20261111.md) and [handoff 103](https://github.com/AlOussama/TYNDP_Products/blob/37ee7734049d4cbe3480bb263ca68615d9140809/docs/current/IOSN_Modul2_Netzaggregation/103_M2_RR1_AND_OWNER_G2_COLD_START_HANDOFFS_20261112.md).

The independent test implementation was written anew in [test_rr1_phy_re_20261112.py](https://github.com/AlOussama/TYNDP_Products/blob/fa097c23a71510ad1feb0ed327b76b4ed95955ca/tests/iosn_official/test_rr1_phy_re_20261112.py) with a separate [GitHub Actions verification workflow](https://github.com/AlOussama/TYNDP_Products/blob/fa097c23a71510ad1feb0ed327b76b4ed95955ca/.github/workflows/m2-ma1-rr1-phy-independent.yml). No original strict-XFAIL witnesses were changed or incorporated as passing tests. The 10-bus graph and its five snapshots are newly constructed, not reused from W-INT's fixture. This is an algorithmically independent test development and separate immutable review branch; it is **not** a claim that a second human or external institution has separately authenticated its identity (the GitHub publishing account is the repository owner's connected account).

The reviewer branch was created from **exact fb201ef5**, with no production-code modifications. The CI confirms the repair is an ancestor, and both its source tree and the review checkout's source tree have identical Git tree SHA:

**e9202091d4ac79b5bd8fbe83646d3ba11f1367b3**.

The independent GitHub compare before publication showed precisely two added files compared to the repair commit: independent tests and independent CI workflow. Subsequent changes are report/ledger documentation only. No edits to M0, M1, weather-year selection, legacy m2 implementation, or frozen historical review sources.

## 2. Independently executed CI: all required suites green

- [Push run #43165364424 — SUCCESS](https://github.com/AlOussama/TYNDP_Products/actions/runs/43165364424)
- [Job #131005866264 — SUCCESS](https://github.com/AlOussama/TYNDP_Products/actions/runs/43165364424/job/131005866264)
- [Artifact #13919657133 — JUnit, metrics, source SHA and 15-file fixture](https://github.com/AlOussama/TYNDP_Products/actions/runs/43165364424/artifacts/13919657133)
- ZIP artifact SHA-256: **fc6ef9ac072c0c9cda7be38993a1cba9203ee02eb9a534a789124b2829f756ed**
- Exact tested review checkout: **fa097c23a71510ad1feb0ed327b76b4ed95955ca**; exact immutable repaired production code: **fb201ef5f120f64696dea9aa99f77ece77546f9a**.
- Runtime: Ubuntu 24.04, Python 3.11.18, pytest 9.2.0, NumPy 2.4.6, SciPy 1.17.1, pandas 3.1.1; the full pip freeze is in the evidence artifact.

| Suite | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| New independent ordinary-PASS PHY tests | **40** | 0 | 0 | 0 |
| Entire MA1 tests/iosn_official including new tests | **106** | 0 | 0 | 0 |
| Entire repository Python test suite including new tests | **132** | 0 | 0 | 0 |

The evidence artifact includes three independent JUnit XML files and their SHA-256 hashes, complete pytest logs, exact source Git-tree identities, physical_metrics.json, the fixture manifest and all 14 manifest-hashed outputs, plus rr1_ci_attestation.json. Historical 4 strict XFAIL cases are not counted as passing: the original attack inputs are recreated with **new ordinary assertions**.

## 3. PHY-R01 through PHY-R04, independent failure-reproducer replay

| Original finding | New independently executed attacks and required behavior | Disposition |
|---|---|---|
| **PHY-R01** — mutable input list / TOCTOU fingerprint | Caller mutates grid AC branch list, bus/country lists, HVDC, unsupported list **after construction**: active topology, validated fingerprints, physical reference remain unchanged. Further tests exercise time/dispatch/rating/cache caller lists and NumPy buffer ownership. | **CLOSED_VERIFIED** |
| **PHY-R02** — lossless="False" admitted | Exact string "False" rejected; also other nonboolean strings, integers, None, list, numpy.bool and float rejected. Actual bool False deliberately raises RejectedComponent because losses are out of the declared DC kernel. | **CLOSED_VERIFIED** |
| **PHY-R03** — in_service="False" admitted and changes connectivity | Exact string "False" and seven nonboolean variants rejected. Related incomplete_110kv_ties and Provenance.synthetic are strict bool. True bool False removes the AC tie, yielding two separate electrical islands. | **CLOSED_VERIFIED** |
| **PHY-R04** — unbounded atol_mw permits hidden MW slack | nan, +/-inf, huge finite, out-of-bounds 1e-5, zero, negative, string, bool, None rejected. Exact original two-bus [+20,-19] MW island rejected even at maximum admissible tolerance. Balanced two-bus case succeeds at the lower/default and upper legal tolerances. | **CLOSED_VERIFIED** |

These are independent tests without xfail or skipped branches. **Open synthetic physical P0 = 0; open synthetic physical P1 = 0** within the tests' explicit input domain.

## 4. Newly derived sparse-vs-dense KCL and affine KVL oracle

**New case:** 10 buses, 12 AC branches, three AC islands (5+3+2 buses), five independent AC cycle constraints, two HVDC links crossing AC islands, two independent PST schedules, a fixed-phase transformer, five synthetic snapshots and a cross-country AC mesh. HVDC controls include positive and negative transfers. AC graph connectivity is calculated globally; country labels do not break the power-flow graph, and HVDC does not connect synchronous AC islands.

The production reference computes sparse islandwise nodal Laplacian flows. The independent check constructs a fresh **dense oriented incidence A** and a dense **cycle-space basis C** from the nullspace of A. It solves KCL **A f = p** together with **C-transpose (diag(x_pu/S_base) f + phi) = 0** by least squares, not by copying the production Laplacian or any W-INT flow vector. Phase phi contains fixed transformer and time-varying PST phase shifts with the production orientation sign.

| Independent maximum, five snapshots | Numeric result |
|---|---:|
| Nodal KCL max abs residual | **8.881784197001252e-15 MW** |
| Affine cycle-space KVL max abs residual | **8.673617379884035e-18 rad** |
| Sparse vs independent dense flow max difference | **3.3640645824561943e-11 MW** |
| AC-island net injection max abs residual | **5.329070518200751e-15 MW** |

Input SHA-256: **43f23103be31edd9bd5d38199daa579eb5958f24869a1e871eb8a73b21621cb4**.

Orientation reversals of a PST and HVDC with correspondingly reversed control signs preserve physical node injections and all unreversed branch flows. A changed HVDC schedule without balancing redispatch fails closed; a missing PST schedule or HVDC schedule also fails closed. There is no hidden balancing MW slack.

**Sparse stress:** new 1001-bus/1000-line nonuniform-reactance case with five nonidentical snapshots, injections at buses 0, 300, 700 and 1000, analytic branch flows of 10, 7 and 3 MW times the snapshot scale on successive stretches; sparse incidence has 2000 nonzeros and agrees with the analytic oracle. This demonstrates sparse-functional correctness, **not** a 37-country or European-scale resource qualification.

## 5. Finite tolerance, fail-closed inputs, file hashes

The repaired public tolerance contract accepts only **0 < atol_mw <= 1e-6 MW**, finite real and nonboolean. **1e-6 MW equals 1 W**; at a 100-MVA base this is order 1e-8 of base power. Callers can tighten but not relax this absolute physical balance/KCL gate. The chosen ceiling is an internal **I implementation choice**, not an official ENTSO-E numerical standard. Other real-grid scales/conditioning require a separate scientifically documented numerical admission; no automatically enlarged proportional tolerance is certified.

New negative cases check invalid source hash length, naive UTC timestamps, reversed chronology, wrong ratings units (MVA rather than declared MW proxy), incomplete flagged 110-kV ties, missing PST/HVDC controls and incomplete contingency ratings. A numerical balanced redispatch changes the flow input fingerprint even if declared source hashes do not change.

**15-file SHA-bound fixture:** independently regenerated the synthetic MA1 fixture on the pinned production code and rehashed all **14 manifest-listed output files** plus verified the manifest itself. **14/14 match, 0 mismatches**. It retains two AC islands, three country labels and five mock weather years; the operator invariant **A_z Gamma = P A_d** is checked independently to sparse rounding accuracy. The fixture exporter is not itself a verified Git checkout witness: the CI asserts repair ancestry, identical Git source tree and correct pinned code_commit. The reviewer test deliberately tampers with one exported CSV and verifies a hash mismatch is detected.

- Fixture input digest: **a378e22fde234cdf9275bcb5685f1034c1e41eeb442b81a8cfe06ed988882661**
- Fixture manifest SHA-256: **876f91423e2bb2493f6121d681a5443794cc7a4c47a7cbcc37321fe42df92621**
- The fixture explicitly retains **real_network_qualified = false**, **independent_reviewer_release = false**, and **NOT_APPLICABLE_SYNTHETIC** budget page evidence.

## 6. Residual findings and scoped gates

The new machine-readable [RR1 PHY findings ledger](M2_MA1_RR1_PHY_INDEPENDENT_FINDINGS_20261112.json) records all original PHY-R01..04 as **independently closed**, while retaining separate P2 dispositions:

- **PHY-P2-SOURCE — OPEN_DATA_SCOPE:** an upstream declared source SHA field is not an independent attestation of the original ENTSO-E/TSO source bytes. No real dataset was validated.
- **PHY-P2-COMMIT — MITIGATED_BY_CI_NOT_API_FIXED:** exported code_commit is caller-supplied; the external CI's actual Git SHA, identical source tree, JUnit and evidence artifact are necessary to bind this physical review. The exporter API alone still does not prove its own source SHA.

**G01:** synthetic temporal/hash/balance contracts pass; real provenance not admitted.  
**G03:** synthetic global AC multi-island, PST/HVDC terminal and physical solver behavior pass.  
**G05:** synthetic Kirchhoff, affine cycle laws and oriented-operator consistency pass.  
**G11:** **PARTIAL_LOSSLESS_DC_ONLY**. Lossy HVDC, full transformer/tap semantics, real device adapters, original PyPSA parity and AC load flow not qualified.  
**G02/G04:** existing regression green, but the separate independent **R-CLU-RR1** is not replaced by this review.  
**37-country / 102-zone real grid:** **BLOCKED_DATA**; original source licensing, external dispatch/weather-year input, network topology, ratings, contingencies and ENTSO-E method authority remain outside this admission.

## 7. Final decision and handoff

**R-PHY-RR1 = ACCEPT_SYNTHETIC**, limited to the physical lossless-DC synthetic contract tested against the exact integrated repair commit. There are **no remaining reproduced PHY P0/P1** in this scoped review. This decision does **not** independently authorize the overall **MA1_SYNTHETIC_QUALIFIED** system gate; that requires the separate R-CLU-RR1 on the same SHA and the project governance/Owner decision.

Maintain **Issue #14 OPEN** as a governance/status record until explicit Owner disposition. **No main/PR merge, no MA2/MA3 runtime authorization, no real-network qualification, no interpretation as complete G11 or officially adopted ENTSO-E method**. Original historical review tests, report and findings remain unchanged.

### Reproduction

Use the immutable reviewer test/CI SHA **fa097c23a71510ad1feb0ed327b76b4ed95955ca**. In a Python >=3.11 environment, install dependencies via python -m pip install -e ".[test]" and run python -m pytest -q tests/iosn_official/test_rr1_phy_re_20261112.py, python -m pytest -q tests/iosn_official and python -m pytest -q. The committed CI workflow runs these commands, independently derives the numerical metrics, regenerates the 15 fixture files and retains SHA-bound JUnit, source identity and file digests at the linked GitHub run.
