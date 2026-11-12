# 108 — S-GOV-M2-G2: RR1 closure and scoped MA1 scientific synthetic gate

Date: 2026-11-12. Classification: EVIDENCE-BASED SCIENTIFIC GATE REVISION / UNSIGNED OWNER DECISIONS. This is an additive update to the frozen, historically correct G2-preparation record 105 and gate ledger v1. It neither retroactively changes the original records nor grants project Owner authority.

## 1. Frozen inputs and exact A–E closure

All five reported A–E completion commits exist in GitHub and were inspected at immutable SHAs:

| Macro | Git commit | Verified status |
|---|---|---|
| A — MA1 RP1 | fb201ef5f120f64696dea9aa99f77ece77546f9a | 12 changed M2-only files, worker CI 43113044448 SUCCESS (66 focused and 92 full); worker repair is not independent reviewer evidence |
| B — API G1 | ed42d051a7234f7f062d94d06291f66e56657bbc | Option C recommended, not Owner-selected; canonical A = tyndp_reduce.iosn_official, optional strict B→A adapter |
| C — D SOURCE1 | 05dd0db3fc15fd6e091b8dd96d854adcedf8302c | Country quota CSV 37 labels/102 zones source-table only; D0–D3 blocked; D4 not admitted |
| D — METHOD G1 | c980bbd341b1051257bcf31b0a904dd7937f7241 | Project decision proposals only; ENTSO-E adopted/effective authority unconfirmed |
| E — MA2 PRE | b73bb3c595bff515aeca052f02fc83f72289b5f0 | x/c0, affine-KVL, coupled-country and fixed-monitor designs; 45 cases DESIGNED_NOT_EXECUTED; R-NUM NOT_RUN |

Primary authorization boundary: consolidation 102 and handoff 103 at 37ee7734049d4cbe3480bb263ca68615d9140809; conditional MA2 implementation macro 100 at 27dfd810b39e17e6b616a2b0aeb813eb8948d8a0. The separate D-SOURCE1 report also carries document number 100 on another branch; never identify these by number alone.

## 2. Independent RR1 evidence admission

Both review artifacts explicitly name and test exactly the same immutable production repair commit: fb201ef5f120f64696dea9aa99f77ece77546f9a. Independent reviewer test branches add only test/workflow files relative to the repair SHA; inspected GitHub compares contain no changed file in src/tyndp_reduce/iosn_official. The repaired source subtree Git SHA reported by PHY is e9202091d4ac79b5bd8fbe83646d3ba11f1367b3.

| Required proof | RR1-R-PHY | RR1-R-CLU |
|---|---|---|
| Published review report commit | 7a7de151fcf7e4bd2cda0530c2438dcfc95b5df1 | bb7cabeb25f092e4ab68732e17903e7be1413c55 |
| Independent tested checkout | fa097c23a71510ad1feb0ed327b76b4ed95955ca | 00e50ecca685b5379171f5f3ac1bb304a812c9c0 |
| Independent CI / job | 43165364424 / 131005866264 | 43165924354 / 131007649350 |
| Independent new PASS | 40/40 | 7/7 |
| MA1 suite PASS | 106/106 | 73/73 |
| Full repository suite PASS | 132/132 | 99/99 |
| Failure / error / skip | 0 / 0 / 0 | 0 / 0 / 0 |
| Independent findings conclusion | ACCEPT_SYNTHETIC — PHY subset | ACCEPT_SYNTHETIC — CLU subset |
| Open P0/P1 in reviewed synthetic scope | 0 / 0 | 0 / 0 |

Exact sources:
- PHY report: https://github.com/AlOussama/TYNDP_Products/blob/7a7de151fcf7e4bd2cda0530c2438dcfc95b5df1/docs/current/IOSN_Modul2_Netzaggregation/M2_MA1_RR1_PHY_INDEPENDENT_REPORT_20261112.md
- PHY ledger: https://github.com/AlOussama/TYNDP_Products/blob/7a7de151fcf7e4bd2cda0530c2438dcfc95b5df1/docs/current/IOSN_Modul2_Netzaggregation/M2_MA1_RR1_PHY_INDEPENDENT_FINDINGS_20261112.json
- PHY CI: https://github.com/AlOussama/TYNDP_Products/actions/runs/43165364424 (GitHub status completed/success; head fa097c23...)
- CLU report: https://github.com/AlOussama/TYNDP_Products/blob/bb7cabeb25f092e4ab68732e17903e7be1413c55/docs/current/IOSN_Modul2_Netzaggregation/rr1_clu_20261112/independent_review.md
- CLU ledger: https://github.com/AlOussama/TYNDP_Products/blob/bb7cabeb25f092e4ab68732e17903e7be1413c55/docs/current/IOSN_Modul2_Netzaggregation/rr1_clu_20261112/findings_and_gate.json
- CLU CI: https://github.com/AlOussama/TYNDP_Products/actions/runs/43165924354 (GitHub status completed/success; head 00e50ecc...)

Reviewer independence qualification: there are separate reviewer-authored test files, distinct workflows, evidence artifacts, commits and independently described oracles, rather than worker self-tests. The GitHub publisher is the repository account; a distinct human or institutional reviewer identity is NOT independently authenticated. If the Project Owner requires person-level separation rather than independently executed work products, add a separately signed reviewer-identity attestation as an Owner control; do not invent it.

## 3. Attack replays, physical and graph oracles

PHY-R01 (TOCTOU/caller-owned mutation), PHY-R02 (string lossless="False"), PHY-R03 (string in_service="False") and PHY-R04 (nonfinite/unbounded atol or unbalanced [+20,-19] MW island) are all independently CLOSED_VERIFIED as ordinary passing assertions. The historical strict-XFAIL review evidence was not modified.

PHY's independent five-snapshot case covers 10 buses, 12 AC lines, 3 true AC islands, 5 cycles, 2 HVDC links and 2 PSTs. Max observed residuals: KCL 8.881784197001252e-15 MW; affine cycle KVL 8.673617379884035e-18 rad; sparse-vs-dense flow discrepancy 3.3640645824561943e-11 MW. A 1001-bus sparse chain passed its analytic oracle. Its synthetic exporter regenerated 15 total files and checked 14/14 manifest-listed output SHA-256 digests (zero mismatch). The MA1 finite input tolerance 0 < atol_mw <= 1e-6 MW is a PROJECT IMPLEMENTATION bound, not a published ENTSO-E accuracy norm.

CLU independently enumerated all 729 four-node edge-state graphs and all quotas k=1..4. The worker's original nonempty-edge domain contains 1804 feasible graph/quota pairs. The mathematically exhaustive domain additionally includes the empty graph with quota k=4: 1805/1805 feasible instances accepted; zero false infeasible, false rejected feasible or false accepted infeasible. Thus 1804 is a documented restricted-domain count, not the unrestricted mathematical count. Independent 5-node and 14-vertex/3-country cases check protected cuts, country purity, all actual AC islands, four cross-country AC ties and exact A_z Gamma = P A_d. A feasible 17-vertex case returns HEURISTIC_STUCK, not PROVEN_INFEASIBLE, because the exact-search limit is 16 vertices (or 100000 states); completeness or optimum at larger scale is NOT certified.

CLU independently closes R-CLU-001/002 (P1) and R-CLU-003/004 (synthetic P2). The nominal 400-kV screened line at |flow|=100 MW, limit 10 MW for one hour yields 90 MWh/year; class0 for genuine 225/400-kV lines is explicit reject, and 220→225 / 380→400 needs sourced declarations. Protection hashes of generator and tuple agree; UK Table-3 printed source page 27 and separate Northern Ireland versus UK are enforced. R-CLU-005 remains partial because declared source-URI/SHA and aliases do not independently authenticate remote original bytes.

## 4. Residual issues — scoped treatment

- PHY source original-byte attestation: OPEN_DATA_SCOPE P2; a caller-populated code_commit exporter field requires external actual Git checkout CI checking; MITIGATED_BY_CI_NOT_API_FIXED.
- CLU R-CLU-005: PARTIAL_EXTERNAL_SOURCE_BYTES_PENDING P2; source alias and voltage-class provenance is not verified against original remote asset bytes.
- RR1-NOTE-001: bounded-exact-search incompleteness for >16 vertices / 100000 states is a KNOWN_P2, not proof of real-network feasibility or global optimality; any HEURISTIC_STUCK must remain non-certifying.
- R-API-P1-01..09 are independent semantic/API integration risk items from API G1, not the six repaired MA1 physical/clustering P1. They require explicit versioned MA2 contract guards, Owner disposition and applicable independent tests before MA2 code approval; they have NOT been declared closed by either RR1.
- G11 is PARTIAL_LOSSLESS_DC_ONLY: no generic lossy HVDC, 3W/tap/phase physical adapter parity, full AC or production security validation. The full real D0/D1/D2/D3/D4 source chain and 37-country/102-zone replay remain BLOCKED_DATA.

## 5. Final scoped gate ruling

| Field | Post-RR1 status | Meaning |
|---|---|---|
| MA1_RR1_PHY / MA1_RR1_CLU | ACCEPT_SYNTHETIC / ACCEPT_SYNTHETIC | Two independent evidence suites, identical repaired code; each with P0=0/P1=0 |
| MA1_RR1_SAME_CODE | VERIFIED | Both compared to frozen fb201ef5; no implementation source change |
| MA1_SCIENTIFIC_SYNTHETIC_QUALIFIED | TRUE_SCOPED | G01–G05 physical/clustering synthetic lossless-DC subset only |
| G11 | PARTIAL_LOSSLESS_DC_ONLY | Unsupported device classes remain out-of-scope |
| OWNER_API_DECISION / OWNER_CODE_RELEASE | PENDING / FALSE | No signed Project Owner act; neither canonical API nor MA2 permission follows automatically |
| MA2_G06–G08 / R-NUM | NOT_IMPLEMENTED / NOT_RUN | 45 E-design tests still only planned |
| REAL_QUALIFIED / G12 | FALSE / BLOCKED_DATA | No authentic 37/102 European source, synchronized neutral/operational data or D4 review |
| ENTSOE_METHOD_AUTHORITY | UNCONFIRMED | Consultation draft only; Project Owner cannot approve official adopted/effective status |
| MAIN / PR / MA3 | NO_MERGE / NOT_AUTHORIZED | Existing Draft PRs stay unmerged; no downstream implementation authorization |

This scientific evidence ruling is NOT an Owner vote or release, does not modify any API choice and does not authorize MA2 code. Project I-parameters, fixed monitors, full 15-file v1 intake, neutral data, review-person attestation policy and the explicit signed scoped MA2 code instruction remain separate controls.

Next: read the additive Owner register 109, next-macros 110 and machine ledger m2_g2_gate_ledger_rr1_closed_20261112.json. Keep historical document 105 and v1 machine ledger as the valid initial pre-RR1 snapshot.
