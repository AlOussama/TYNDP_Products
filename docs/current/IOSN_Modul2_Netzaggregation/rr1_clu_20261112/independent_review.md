# M2-MA1-RR1-R-CLU — Independent Clustering Repair Re-Review

**Review date:** 2026-11-12
**Repository:** AlOussama/TYNDP_Products
**Immutable production integration under review:** fb201ef5f120f64696dea9aa99f77ece77546f9a
**Independent review branch:** review/iosn-m2-ma1-rr1-clu-20261112
**First independently tested review commit:** 00e50ecca685b5379171f5f3ac1bb304a812c9c0
**Independent GitHub CI run:** https://github.com/AlOussama/TYNDP_Products/actions/runs/43165924354
**CI artifact:** m2-ma1-rr1-clu-independent-20261112 (ID 13919364098, ZIP digest sha256:e54a1cc66f41d0bc16cea64645bf6b19dde0988e8a528a39d560128869fbb622)
**Independent test implementation:** tests/iosn_official/test_rr1_clu_independent_20261112.py
**Gate decision:** ACCEPT_SYNTHETIC — R-CLU SUBGATE ONLY. P0=0 and P1=0 demonstrated in the explicit finite/synthetic contract scope. Overall MA1 gate remains PENDING_R_PHY_RE_AND_OWNER; REAL_QUALIFIED=false; MA2/MA3 and merge remain NOT_AUTHORIZED.

## 1. Frozen provenance and reviewer separation

Read fully: original 87 R-CLU independent review, original 88 R-CLU findings ledger R-CLU-001..005 on immutable 7d7d07d7af5966ddc26d0be1100a69013763d2e8; RP1 101 integrator report; RP1 worker ledger; RR1 contract 99; owner handoff 103; integrated code under fb201ef5 (seed, country, screen, ma1, operators, contracts); original worker regression tests; and GitHub Issue #15. No production, M0, M1, weather selector, or historical independent reviewer test was edited.

The new independent oracle enumerates set partitions as canonical bit-subsets, tests connectedness by a separate bitset reachability routine and checks output quotas/cuts without calling the implementation's busmap validator. It is not a copy of W-CLU's restricted-growth-string oracle and does not cite worker green CI as independent proof.

GitHub Actions explicitly checked integration SHA ancestry and an empty diff from fb201ef5 to the independently tested checkout over src/tyndp_reduce/iosn_official. The review commit only added an independent test and a separate CI workflow. CI checked Python 3.11.18, pytest 9.2.0 and installed scientific dependencies.

Official consultation methodology was inspected against printed PDF pages 26 and 27, Table 3 (37 country rows / 102 zones, Northern Ireland and United Kingdom distinct), and printed page 45, Annex 6.1 (225/400 kV annual overload-energy screening). Source: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf. This is the 25 February 2026 PUBLIC CONSULTATION text, not a certification of final ENTSO-E adoption.

## 2. Full independent four-node graph oracle

Six labelled undirected candidate edges, each absent/ordinary/protected, yield 3^6 = 729 graphs. Quotas k=1..4 and 15 canonical set partitions were enumerated independently. The oracle tests only: exactly k nonempty AC-connected blocks and no protected edge wholly within a block.

| Quota k | Feasible pairs, including empty graph |
|---|---:|
| 1 | 38 |
| 2 | 373 |
| 3 | 665 |
| 4 | 729 |
| Total | 1,805 |

The original worker tests exclude the graph with ZERO active edges before iterating quotas. Exactly one mathematically feasible case is thereby omitted: the empty graph with quota k=4, where every node forms its own connected singleton zone. Hence the original nonempty-edge domain contains **1,804** feasible graph/quota pairs, whereas the complete mathematical domain contains **1,805**. This is a test-scope qualification, NOT a repair regression. The independent review explicitly executes the previously omitted case against production; it succeeds.

Across all 729 graphs and all four quotas, including infeasible instances, independent production-oracle comparison found:
- 1,805/1,805 mathematically feasible cases returned a valid solution;
- FALSE_REJECTED_FEASIBLE = 0;
- FALSE_PROVEN_INFEASIBLE = 0;
- FALSE_ACCEPTED_INFEASIBLE = 0;
- each accepted output obeyed exact quota, protected cuts and AC-connectedness;
- reversed protected iterable and reversed cost-map insertion order did not change output;
- elapsed graph-oracle test time in CI: 0.201 s.

The original 4-node protected-cut witness was recovered, and a distinct 5-node protected-cut trap with another pendant vertex was solved with the exact deterministic fallback.

## 3. Independent larger, multi-country and search-budget attacks

A 14-vertex / 3-country synthetic graph (X:7, Y:4, Z:3) was constructed independently. It includes a six-vertex protected-cut trap in country X, a seventh X-bus that belongs to a separate global AC island, cross-country X–Y, Y–Z and Z–X lines, two oppositely oriented parallel X–Y ties, an internal 110-kV line, and protected cross/interior line IDs. Quotas X=3, Y=2, Z=2 were met; every returned zone was AC-connected and country-pure; all protected endpoints remained interzonal; all cross-country branches remained in the global AC network. Setting the 110-kV incompleteness flag raised the expected hard error. The connected global component excluding the isolated X-bus was independently established.

The matrices P, Gamma, A_z and A_d were built a second time as dense integer matrices from bus/branch orientations and output zone memberships. Each matched its production sparse equivalent element-by-element, and A_z Gamma = P A_d exactly. Independent detailed and zonal KCL held for two snapshots. Explicit +32 MW and opposite 30 MW parallel flows gave 2 MW net corridor transfer and 60 MW cancelled absolute flow, correctly flagged in two counterflow events. No MA2 impedance-fit or MA3 N-1 capacity claim follows.

An independently proved infeasible three-vertex case with fully protected spanning edges and quota 1 returned PROVEN_INFEASIBLE after exhausting states. Conversely a constructively feasible 17-vertex extension of the original greedy trap, whose valid solution is singleton b0 versus the connected remaining 16 buses, returned HEURISTIC_STUCK (visited=0), NOT PROVEN_INFEASIBLE, because the published implementation has a max_nodes=16 exact-search budget. The 17-vertex case is a **known search-completeness limitation**, not a false impossibility certificate. A complete search is not guaranteed on networks exceeding the node/state caps; do not claim that all feasible real-grid graphs are solved.

## 4. Original five independent findings, re-adjudicated

| Finding | Previous priority | RR1 observed result | RR1 disposition |
|---|---|---|---|
| R-CLU-001 | P1 | 1,804/1,804 nonempty feasible solutions recovered, plus empty graph; 4-/5-/6-node protected traps; no invalid accepted outputs | CLOSED_SYNTHETIC_SCOPE |
| R-CLU-002 | P1 | True nominal 400-kV and 225-kV line cannot silently opt out via declared class 0; rejection is explicit; eligible 400-kV line yields 90 MWh per year | CLOSED_SYNTHETIC_SCOPE |
| R-CLU-003 | P2 | Identical tuple versus generator of protected IDs: same busmap, same protected tuple, same input-manifest SHA; duplicate IDs rejected | CLOSED_SYNTHETIC_SCOPE |
| R-CLU-004 | P2 | Original Table-3 UK source-page 27 enforced; altered row claiming page 26 rejected; original CSV SHA equals budget source SHA | CLOSED_SYNTHETIC_SCOPE |
| R-CLU-005 | P2/contract | Opt-in many-to-one alias normalization accepts two independent DE raw IDs; pinned NIR/GBR cannot merge NI/UK; declared source-URI/SHA changes alter the normalization digest | PARTIAL_EXTERNAL_SOURCE_BYTES_PENDING |

The annual overload test uses two samples per external year, durations 0.25 and 0.75 hours, signed +100/-100 MW, normal limit 10 MW: sum(max(0,abs(f)-10)*dt) = 90 MWh/year for each of five declared years. False explicit class=0 raises for nominal 225/400 and for 220/380. The latter values can only enter the correct voltage screening class through explicit 220->225 and 380->400 declarations. The test establishes contract behaviour, NOT the external proof that a particular 220/380-kV asset's class was source-certified. Transformer exclusion and 110-kV exclusion were also checked.

The official country table source pages were checked from the source PDF as well as from the pinned code: printed page 26 ends at Sweden; printed page 27 starts Switzerland and contains Turkey and United Kingdom; Northern Ireland remains separate. R-CLU-005 stores declared source SHA/URI, not an independent digest of the original remote input bytes. This is an explicit source-provenance dependency, not a disguised P2 clearance for real data.

## 5. GitHub CI evidence and artifact integrity

Run: https://github.com/AlOussama/TYNDP_Products/actions/runs/43165924354
Review test/CI checkout SHA: 00e50ecca685b5379171f5f3ac1bb304a812c9c0
Unmodified production repair SHA: fb201ef5f120f64696dea9aa99f77ece77546f9a
Job: rr1-clu-independent, ID 131007649350, SUCCESS.

| Test tier | Cases | Passed | Failed/errors/skipped |
|---|---:|---:|---:|
| New reviewer-authored adversarial tests | 7 | 7 | 0/0/0 |
| Full Module-2 iosn_official suite including new tests | 73 | 73 | 0/0/0 |
| Complete repository Python test suite including new tests | 99 | 99 | 0/0/0 |

The retained artifact (ID 13919364098) contains independent.log, MA1 and all-suite logs, three JUnit XMLs, environment/pytest versions, pip freeze, SHA-bound CI manifest and a reproduced fifteen-file synthetic export: fourteen output objects with explicit content SHA-256 plus manifest.json. The artifact ZIP digest is recorded above. For exact source checkout vs reviewer commit, use the CI ancestry and source-diff checks; do not confuse a caller-provided code_commit string with the Git checkout SHA.

An earlier successful worker run on pinned fb201ef5 was verified separately (run 43113098354, artifact 13896943305). Its success was not counted as an independent reviewer test.

## 6. Final decision and residual gates

**Independent R-CLU subgate: ACCEPT_SYNTHETIC (SCOPED).** No open P0/P1 was reproduced across the stated finite/synthetic reviewer tests. This validates the repaired country-quota seed, audited nominal-voltage screening decisions, immutable protected-ID fingerprinting, row-exact source-page checks, AC-connected/country-pure output and oriented sparse aggregation **in the tested synthetic contract**. It does not certify heuristic completeness for arbitrary large graphs or optimality of a European clustering solution.

**Residual explicitly recorded limitations:**
1. R-CLU-005 remains P2/EXTERNAL_SOURCE_ATTESTATION_PENDING; raw original source bytes, country aliases and 220/380-voltage mapping must be independently proven for real input.
2. Independent RR1-NOTE-001 (P2/KNOWN_BOUNDED_SEARCH): constructively feasible 17-node case returns HEURISTIC_STUCK correctly; no completeness or runtime/quality guarantee for >16 vertices or >100,000 exact states.
3. Independent RR1-NOTE-002 (scope correction): exhaustive oracle has 1,805 mathematical feasible pairs, of which the worker's nonempty graph domain contains 1,804.
4. Full original 37-country/102-zone real-network replay, five externally sourced synchronized weather-year flows, topology/rating/source SHA attestation: BLOCKED_DATA.
5. A separate R-PHY-RE sign-off on the same fb201ef5 and explicit Owner-G2 decision are prerequisites for a project-wide MA1_SYNTHETIC_QUALIFIED gate.

**G02-G05:** independently PASS_SYNTHETIC for demonstrated clustering/screening/projection contracts. **G01/G03 physical kernel outside this review:** R-PHY-RE PENDING. **G11:** PARTIAL_LOSSLESS_DC_ONLY. **REAL_QUALIFIED:** false. **ENTSOE_AUTHORITY:** CONSULTATION_ONLY / NOT_CONFIRMED_ADOPTED. **MERGE:** NO. **MA2/MA3:** NOT_AUTHORIZED. No change in M0, M1, weather-year selector or main.

The project owner / S-GOV must not convert this R-CLU-only acceptance to an overall integration approval without the separate R-PHY re-review and source/Owner gate.