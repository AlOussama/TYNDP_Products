# R-M2-MA1-CLU — Independent Country-Quota Clustering and Aggregation Review

**Date:** 2026-11-11  
**Repository:** AlOussama/TYNDP_Products  
**Original immutable code freeze:** 0254d867a34b66ec7b56c90225605d29ea328916  
**Independent review branch:** review/iosn-m2-ma1-r-clu-20261111  
**Scope:** Module 2 / src/tyndp_reduce/iosn_official; W-CLU code was not modified.  
**Final independent decision: REPAIRS_REQUIRED**  
**Finding count: P0 = 0, P1 = 2, P2 = 3; separate BLOCKED_DATA real-input gate.**

## 1. Evidence, independence and limits

Sources read at fixed refs:
- GitHub Issue #15, Draft PR #13, reviewer brief 84 at commit 70e92ba9e62a320e58227ce9c2f03fad266f44bf.
- Official method/code mapping NR-01..NR-18 at commit 3dc719a35f57bd9516bef8486bf262b75509d6b1.
- Original ENTSO-E TYNDP 2026 *Identification of System Needs Methodology*, version for public consultation, 25 February 2026: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf (Table 3 printed pages 26-27; clustering printed pages 23-27; Annex 6.1 printed pages 45-51).
- All ten Python modules under src/tyndp_reduce/iosn_official, country budget CSV, existing test_ma1_clustering.py, test_ma1_integration.py and test_ma1_fixture_evidence.py, plus workflows.

Independent evidence:
- New test source: tests/iosn_official/test_r_clu_independent_frozen.py, distinct from all W-CLU tests.
- Clean GitHub Actions Python 3.11 invocation: https://github.com/AlOussama/TYNDP_Products/actions/runs/43078445311
- Earlier complete successful run of the 10-test independent addition: https://github.com/AlOussama/TYNDP_Products/actions/runs/43078137235 (36/36 tests including the 26 pre-existing MA1 tests).
- CI JUnit XML, raw pytest transcript and tested commit are uploaded as a versioned workflow artifact.
- Local, separately written search_greedy_failure.py and enumerate_n4.py were also used to discover and independently confirm the small-graph counterexample before writing the repository review tests.

No externally sourced, fully mapped 37-country European detailed grid; no five-year real dispatch/load-flow provenance; no whole-Europe 102-zone validation was supplied. The review therefore does not attest real-data qualification, algorithmic equivalence to ENTSO-E's unpublished software, MA2 calibration, or MA3 N-1 capacities.

**Interpretation of CI:** The independent negative tests intentionally assert the observed defects, including errors raised by the frozen code. Their PASS means the defects were reproduced, *not* that the defects were repaired. Production implementation remains at the frozen commit.

## 2. Contract, scientific and numerical matrix

| Property / basis | Independent evidence | Qualification |
|---|---|---|
| Table 3: 37 separate source labels, 102 zones | Compared CSV row-by-row with original ENTSO-E PDF, pages 26-27; test_01 | PASS_SYNTHETIC_CONTRACT |
| Northern Ireland and United Kingdom distinct, one zone each | Original PDF, literal independent expected table, test_01/test_05 | PASS |
| Exact quota per country; no mixed-country zone | country.py lines 142-182, test_03/test_05 | PASS for returned solutions |
| Every zone AC-connected | Test_03 enumerated feasible partitions and validates every returned busmap | PASS for returned solutions |
| Separate same-country AC components | test_04: underbudget reject; quota=2 for two islands succeeds | PASS |
| Incomplete 110-kV tie flag | test_04: raises fail-closed CountryContractError | PASS on correctly flagged inputs; actual coverage BLOCKED_DATA |
| Explicitly protected branches remain interzonal | test_03 checks every successful result against protected endpoints | PASS for returned solutions |
| Protected constraints are decided feasible/infeasible correctly | test_02/test_03: feasible input raises Cannot meet exact quotas | FAIL P1 R-CLU-001 |
| Greedy deterministic contraction / declared I-01 | Fixed costs and canonical ordering in seed.py; tests repeat results | Implemented heuristic; NOT official method or optimum |
| Criticality 225/400 kV annual overload MWh | test_07: duration weighting, signed flow, variable MW limits, years separated | PASS for admitted classes; exception FAIL P1 R-CLU-002 |
| 220/380 nominal kV require explicit 225/400 class | test_07: classified examples pass; unclassified 220 rejected | PASS conditional on honest external classification |
| Explicit screening class 0 on a genuine 400-kV line | test_08: silently excluded despite physical overload | FAIL P1 R-CLU-002 |
| Explicit weather year IDs and weighting | test_07, screen.py lines 61-99, TimeSet five-year contract | PASS_SYNTHETIC; no real-year provenance checked |
| Cross-border AC ties left in shared network | test_05 covers three countries and all three inter-country tie pairs | PASS |
| Oriented P, Gamma, A_z, A_d | test_06 independently asserts signed matrices and A_z Gamma = P A_d | PASS_SYNTHETIC |
| Opposed parallel corridor flows | test_06: +32 MW, -30 MW, net +2 MW, cancellation 60 MW | PASS diagnostic; no N-1 quality claim |
| Input-protected-ID fingerprint stability | test_09: tuple vs generator same protection and busmap, different hash | FAIL P2 R-CLU-003 |
| Source page attribution | test_10: UK official page can change 27 to 26 undetected as false attribution | FAIL P2 R-CLU-004 |
| Country raw aliases to official labels | country.py injectivity restriction; test_05 negative alias | P2 contractual limitation R-CLU-005; upfront normalization required |
| Complete real 102-zone geography and operational scenarios | No verified original source/dispatch available | BLOCKED_DATA |

## 3. Exhaustive oracle and failure certificate

The independent exhaustive oracle enumerates all canonical set partitions of four labelled vertices. Its admissibility predicate uses only: exactly k nonempty groups; group connectivity in the undirected active AC graph; protected endpoints in different groups. It does not reuse quota_seed, country.py's validator or W-CLU's merge logic to decide feasibility.

All **3^6 = 729** edge-state configurations are covered for four possible vertex pairs? More precisely: four vertices have **six** possible undirected edges; each edge is absent, ordinary, or protected, hence 729 configurations. The review tests all quotas k = 1,2,3,4. **1,804** graph/quota instances have at least one feasible partition. The frozen greedy seed succeeds on **1,794**, rejects **10** despite a valid partition, and produces **zero** invalid partitions among successful instances. This is a complete, bounded enumeration of this finite test family, not a claim about larger grids.

Minimal independent reproduction:
- Bus IDs: v0, v1, v2, v3; one synthetic country X; quota X = 2.
- Active AC lines (ID: endpoints; merge cost; protected):
  - e01: v0-v1; 7; YES
  - e02: v0-v2; 4; YES
  - e03: v0-v3; 0; NO
  - e13: v1-v3; 7; NO
  - e23: v2-v3; 0; NO
- Expected feasible assignment: {v0} and {v1,v2,v3}, the latter connected via v3. Both protected endpoints are separated.
- Observed: greedy merges v0-v3 at zero cost, thereby locking both interfaces from the merged component to v1/v2. It subsequently raises CountryContractError("Cannot meet exact quotas ...").
- Source: seed.py lines 61-135, especially 87-104. Trigger: test_02; broad certificate: test_03.

The error is not that a greedy heuristic is nonoptimal. It is that a feasible input is labelled impossible when a different merge order would succeed. The error can obstruct valid 102-zone processing when protected cuts are active.

## 4. Screening bypass certificate

Source: contracts.py lines 60-85 and screen.py lines 41-79. The API explicitly permits screening_class_kv = 0, and screen.py excludes such a line without an exception reason or source certificate.

Reproduction: a physical 400-kV line, screening_class_kv = 0, flow = 100 MW, time-dependent normal limit = 10 MW, one hour per each of five external years. The declared IoSN screening scope would yield **90 MWh for each year** if this 400-kV line is in scope. Observed output is **no screened line and no score row**. Test_08 asserts this actual behavior.

This should be treated as an unaudited opt-out, not a valid zero-overload result. Any genuinely approved exclusion must be explicit and attributable to a documented upstream line-class/TSO decision. It must not be an unconstrained flag accepted by the final screening gate. For the ordinary nominal-225/400 line, test should reject class 0 without an authorized reason.

## 5. Additional reproducible P2 findings

**R-CLU-003, consumed iterable / unstable input identity.** execute_ma1 passes protected_line_ids to quota_seed, which consumes it as a frozenset, then later hashes sorted(protected_line_ids). A one-shot generator is empty at the latter point. A tuple and a generator with the *same* sole protected ID d12 yield the *same* resulting busmap and protected IDs but **different input_manifest_sha256**. Fix: canonicalize/validate the IDs into an immutable sorted tuple once at the API boundary; use it for seed, result, and all hashing. Source ma1.py lines 128-180; test_09.

**R-CLU-004, inaccurate official source-page attribution accepted.** The CSV row United Kingdom,1,27 may be mutated to United Kingdom,1,26. The reader checks that the page is 26 or 27 but not that the correct row belongs to the official page; quota validation still passes. Source country.py lines 58-80; test_10. Fix: pin exact expected page per label or omit page-level authenticity claim without matching proof. This does not change the correct 37/102 counts.

**R-CLU-005, raw-country identifier normalization requires upstream action.** resolve_country_ids deliberately rejects many-to-one normalization for two raw aliases belonging to one official country. This is a fail-closed design to avoid mistakenly combining Northern Ireland and United Kingdom, *not* a defect in quota partitioning. Document and test a provenance-preserving upstream canonicalization of legitimate same-country aliases, without touching Module 0/1. Source country.py lines 84-96; baseline brief 84 CLU-INT-04.

## 6. Comparison with official IoSN method NR-01...NR-18

Codes D = publicly documented requirement, I = repository-owned implementation choice, U = unpublished details, T = synthetic verification, B = data or later-module blocker.

| Mapping | Official method | Current MA1 appraisal |
|---|---|---|
| NR-01 | Synchronised European market dispatch and detailed AC flows | Synthetic global physical flow available; real dispatch BLOCKED_DATA |
| NR-02 | 225/400-kV annual overload energy | MWh formula T; uncontrolled class-0 exclusion P1 |
| NR-03 | Sensitive/critical boundaries, coherent parallel flows, limited zone count | Protected/cost heuristic I-01; diagnostics T, quality optimization absent |
| NR-04 | Exact country-level Table 3 / 102 zones | Table and contract T verified; full Europe B |
| NR-05 | Connected initial country-pure clustering | T for returned results; I-01 greedy false infeasibility P1 |
| NR-06 | Iterative, coupled, multiple-country reclustering | Not in MA1; deferred MA2, U search rules |
| NR-07 | AC-oriented cut aggregation; Kirchhoff conservation | Sparse P/Gamma/Az/Ad algebra T verified |
| NR-08 | Synced market-parameter sensitivity reconstruction | Not part of MA1; full realistic input B, further work MA2 |
| NR-09 | Neutral HVDC/PST for impedance calibration | Physical kernel supports distinct neutral mode; MA1 uses operational mode; calibration MA2 |
| NR-10 | Fit equivalent reactances and flow corrections | Deliberately MA2, not delivered by seed |
| NR-11 | KVL and structural/affine loop corrections | MA2, not certified here |
| NR-12 | Global RMSE iterative decision, capacity as secondary | MA2/MA3; present cost heuristic not interchangeable |
| NR-13 | LODF-based N-1 equivalent capacity | MA3, not certified here |
| NR-14 | Four seasonal/directional capacities | MA3 |
| NR-15 | Annex 6.1 capacity special cases | MA3 |
| NR-16 | No-load flow, PST/HVDC influence and equivalent data | Final later product, not MA1 complete |
| NR-17 | Technology/assets/load market split to final zones | Downstream data adapters, out of MA1 scope |
| NR-18 | LF investment vs internal constraint modes | Downstream model contract, out of MA1 scope |

The method publicly requires keeping critical grid lines as boundaries **when possible**, respecting connected zones, promoting same-direction parallel corridors and comparing global RMSE when iteratively adjusting coupled countries. It does not publish a unique exhaustive graph-search algorithm or mandate this particular sum-of-merge-cost greedy strategy. The latter is unequivocally **I-01, an in-house initialization heuristic**, not the ENTSO-E original algorithm. Likewise the user's explicit five-year weights are an input convention, not an ENTSO-E proprietary priority formula.

## 7. Findings and priority gates

| ID | Priority | Status | Gate |
|---|---|---|---|
| R-CLU-001 | P1 | CONFIRMED, OPEN | Correct feasibility handling / no false impossible |
| R-CLU-002 | P1 | CONFIRMED, OPEN | Correct audited 225/400 scope |
| R-CLU-003 | P2 | CONFIRMED, OPEN | Stable protected-ID fingerprint |
| R-CLU-004 | P2 | CONFIRMED, OPEN | Correct original source-page verification |
| R-CLU-005 | P2 | CONTRACT LIMIT, OPEN_DATA | Canonical source country mapping |

- P0: no new directly demonstrated violation of quota, country-purity, connectedness or zonal KCL in an accepted synthetic output.
- P1: two independent blockers before ACCEPT_SYNTHETIC.
- Data gate: official fully matched bus-level 37-territory, 102-zone, cross-Europe real-grid and synchronized market-flow witness not available. Full 102-zone gate stays BLOCKED_DATA irrespective of synthetic repair.
- Method gate: MA2 impedance/RMSE and MA3 N-1/seasonal capacity claims are not supported by MA1 outputs, nor required to clear this *narrow MA1* review.

## 8. Required repair / independent re-review handoff

**R-CLU-PATCH-1 (W-CLU or a distinct repair worker; separate branch from reviewed implementation, no merge):**
1. Repair R-CLU-001. Do not claim feasibility impossibility merely because the current greedy choice dead-ends. Add deterministic alternative-merge search/feasibility guard, bounded exact oracle when tractable, and distinct HEURISTIC_STUCK / INFEASIBLE statuses with valid proof requirements. Demonstrate zero false-infeasible instances over the 729 four-node graph set and expanded five/six-node and multi-country cases, while preserving exact quotas, country purity, connectivity, and protected branches.
2. Repair R-CLU-002. Enforce audited physical-voltage-class admission: exact nominal 225/400 cannot silently disappear via 0; any accepted explicit exclusion requires a mandatory provenance record, reason and method-scope check. Preserve 220→225, 380→400 explicit source-qualified mappings and transformer/PST/110-kV exclusions.
3. Repair R-CLU-003 and R-CLU-004. Make iterable canonicalization and official original-page verification exact. Reconcile documented R-CLU-005 upstream normalization without merging NI/UK.
4. Keep all ten independent R-CLU tests as frozen behavior reproductions in a separate review path. New requirements tests for the repairs must assert the **corrected** outputs rather than merely the previous exceptions.
5. Produce immutable repair commit, isolated CI JUnit/log artifact and a fresh independent R-CLU re-review against that commit. No worker may self-attest the independent approval.

**Decision is REPAIRS_REQUIRED.** Do not merge PR #13. Do not label the synthetic pipeline ACCEPT_SYNTHETIC until the above P1 repairs are independently verified. Full 102-zone real-grid qualification remains separately **BLOCKED_DATA**. Do not change M0/CGMES, M1/PECD or weather-year selection.

This file is the independent frozen-commit review record; reviewer production changes: **NONE**.
