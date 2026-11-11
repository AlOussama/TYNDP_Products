# 89 — M2-D-REAL: Gap Analysis, Real Witness and Qualification Gates

**Date:** 2026-11-11. **Independent decision:** **BLOCKED_DATA**.
**Scope:** solely Module 2 input readiness; upstream M0/M1 and weather selection are read-only suppliers.

## 1. Contracts actually implemented versus required

| Contract | Present in pinned MA1 code? | Real payload available? | Required real fields and remaining gaps |
|---|---|---|---|
| DetailedGridSnapshot | YES, contracts.py | NO | Stable bus IDs, raw country IDs for every bus, ACBranch(id,bus0,bus1,x_pu,voltage_kv,kind,line/transformer/PST), HVDCTerminals, base_mva, complete AC connectivity, source SHA. Equipment loss/tap/3-winding/110-kV handling not silently approximated. Need country resolver and separate source/device capability sidecar. |
| ReferenceDispatchSet | YES | NO | Exact bus × UTC snapshot nodal net MW; distinct HVDC MW schedules and PST rad schedules; signed convention; generation/load/storage and network-vintage joins, dispatch origin and independent reference flow. Market outputs alone are not nodal source. |
| TimeSet | YES | NO | Exactly 5 already selected external IDs, real non-duplicated UTC snapshots, year_id for every snapshot, positive duration_hours and explicit summer/winter season; source hash. No year IDs delivered to audit. |
| CountryZoneBudget | YES, official CSV | QUOTA ONLY | Exact 37 labels, sum 102, NI and UK distinct; fail closed on unresolved country/source bus IDs; AC connectedness/quotas feasible only on full reference. |
| NormalContingencyRatings | YES | NO | Complete per-branch time-matched normal_mw and contingency_mw (thermal MW proxies); source conversion from MVA/A and approved assumptions. **These arrays are not a contingency list or an N-1 proof.** |
| SecurityData | NOT a standalone pinned MA1 implementation contract | NO | Proposed MA3 handoff: outage IDs, monitored elements, branch/outage topology, islanding classification, PTDF/LODF applicability, seasonal emergency ratings, 4 directed×seasonal capacity witnesses and signed TSO exceptions. |

Three separate object types must not be conflated: **market dispatch**, physically balanced **nodal dispatch**, and independently checked **branch reference flows**. The software can compute flows from a declared balanced nodal dispatch, but model-computed values are not independent TSO reference-flow evidence.

## 2. MA1 / MA2 / MA3 gaps

| Stage | Input prerequisites | Current evidence | Real-data conclusion |
|---|---|---|---|
| MA1-G01/G03 | Entire active AC grid, original country map, balanced nodal real MW and HVDC/PST schedules; fully resolved 110-kV ties, component capability map | synthetic 7-bus/2-island + methods | BLOCKED_DATA |
| MA1-G02 | Official 37/102 quotas plus a bus for every mapped land and enough connected components | CSV available, no full bus mapping | PARTIAL_SCHEMA_ONLY |
| MA1-G04 | 225/400-kV designated branches; time-varying normal limits and each of 5 complete real year calendars; stated rating class for 220/380 kV | synthetic only, MOCK years | BLOCKED_DATA; one hour/year cannot validate annual MWh |
| MA1-G05 | Independent original reference flows and topology for sparse projection & KCL | mathematical synthetic checks | NO_REAL_WITNESS |
| MA2-G06 | Same frozen real grid and flows, separate *physically balanced* neutral calibration dispatch (HVDC=0, PST neutral), multiple operating conditions, identifiable meshed equivalent | specification only | BLOCKED_DATA |
| MA2-G07/G08 | Immutable multi-year training/selection/holdout split, sufficient independent snapshots per link/direction/region, detailed flow oracle | specification only | BLOCKED_DATA |
| MA3-G09/G10 | Explicit outage/contingency list, N-1 branch/transformer limits, seasonal/directional classification, exception ledger and 4 capacity outputs | no real security dataset | BLOCKED_DATA |
| Real Gate G11/G12 | Qualified special equipment semantics and independent comparison against real physical data | partial lossless-DC synthetic semantics | BLOCKED_DATA |

An open European grid built from OSM is valuable for testing the *implementation*, but is not authoritative evidence of officially selected ENTSO-E 2025→2035 starting-grid projects, actual dispatch, TSO contingency sets or final IoSN capacities.

## 3. Required reproducible checks: M2-DR-01…DR-17

1. **DR-01 Source bytes:** obtain originals with immutable release ID, source license/access, SHA-256 and byte length. Resolve hashes against original bytes, never Git blob SHA, URL, ETag or self-declared SHA only.
2. **DR-02 Asset identity:** unique nonempty stable buses, AC branches, transformer/PST and HVDC IDs; all terminal foreign keys; original→canonical IDs/versions; no dropped/duplicated elements.
3. **DR-03 Geography:** explicit reversible country-source mapping to published labels; full 37/102 only for whole-Europe input; separate NI/UK; no silent many-to-one normalization.
4. **DR-04 Electrical topology:** AC incidence for all in-service branches, connected components and island count; HVDC not considered AC connection; explicit status for incomplete 110-kV cross-zone ties; no orphan/dangling elements.
5. **DR-05 Equipment:** AC lines, transformers, PST, HVDC, 3W/converted stars, DC systems and unsupported devices enumerated; exact/approx/rejected policy; no implicit omission.
6. **DR-06 Electrical units:** documented S_base and per-bus/transformer V_base; x_ohm→x_pu= x_ohm*S_base/V_base² (consistent 3-phase base convention); transformer tap/phase signs; x_pu>0; voltage screen class explicit.
7. **DR-07 Ratings:** line and transformer thermal/emergency values by branch, snapshot and case; original A/MVA/MW with conversion/proxy policy; finite positive limits, units, seasonal cases, no unmarked fallbacks.
8. **DR-08 Time:** UTC ISO-8601 strictly increasing unique hours; time zone, DST folds, leap day and durations; exact identical bus/branch/year/time keys across all operating states and limits.
9. **DR-09 Weather contract:** exactly 5 immutable externally selected year IDs as actually provided, every ID represented by real snapshots; check fixed manifest and original hashes, never run selection.
10. **DR-10 Asset-to-node joins:** generation, demand, storage, embedded energy sources and HVDC/PST controls map to live grid nodes; MW injections reconcile to signed asset/substation sums.
11. **DR-11 Island power balance:** for each real hour and AC island, sum(nodal MW incl. explicit HVDC terminal actions)=0 within declared tolerance; no hidden country slack, losses/imbalance accounted explicitly in source policy.
12. **DR-12 Reference physics:** sparse DC AC flows satisfy A f=p, mesh equations and consistent branch orientation; compare independently computed/tested original branch flows with source witness, residuals and error tolerances owner-defined.
13. **DR-13 Screenability:** for every screened 225/400 kV branch complete real normal MW limit on every selected hour; all 220/380 nominal levels must have owner-approved screening_class_kv=225/400 or documented 0 exclusion. Complete yearly hours for annual overload-energy claims.
14. **DR-14 Neutral calibration:** separate balanced physical nodal injections (not merely toggling a flag) for HVDC=0 and PST neutral; independent solver replay and source-state identity.
15. **DR-15 Security completeness:** every eligible outage and monitoring branch identified; topology islanding flagged and separately processed; no silently skipped undefined LODF; N-1 emergency and seasonal constraints complete.
16. **DR-16 TSO exceptions:** documented source, justification, scope, expiry, approving TSO and exact outage/branch/hour/season; separate from published algorithmic sparse-sample fallback heuristics.
17. **DR-17 Reproducible witness:** immutable input/output hashes, dataset and parser versions, executable commit, environment lock, solver and tolerances, objective/dataset split metadata and independent reviewer replay. Nonzero missing/unsupported fields -> FAIL_CLOSED, not nominal PASS.

The exact numeric thresholds for residuals, admissible real-flow errors, dispatch gaps and N-1 acceptance are *proposed owner-approval items*, not official values invented here.

## 4. Security and TSO-special-case source fidelity

ENTSO-E consultation §3.8.3 identifies **four N-1 capacity values per interzone connection**: summer/winter × direct/reverse. Annex 6.1 describes branch flows, LODFs and scarcity of representative near-100% loading samples. Its published fallback descriptions include: a flow direction absent >99.5% of the year may copy the opposite capacity; too few points above 1% load produces no value; >99.5% of points above 130% leads to a line-through-origin fit; diffuse point clouds trigger quality warnings/possible re-clustering. These are documented **methodological conditions**, not evidence that individual TSO exemptions exist or apply. A real release must include availability flags and provenance for every fallback; if physical N-1 truth is unverified, the result cannot become REAL_QUALIFIED. [Primary PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf), Annex 6.1, pp.49–51.

## 5. Minimal scientifically admissible real witness, staged

**Priority A (least external preparation, topology-only):** Acquire immutable source records for the OSM-based PyPSA-Eur prebuilt high-voltage network v0.6 (or another explicitly pinned release) and select a **small, electrically connected two-country subset with at least one true AC cross-border tie and a meshed interior**. Prefer adjacent countries with actual data coverage, rather than claiming a fixed pair before inspecting the bytes. Preserve original bus/line IDs, include all induced required transformer/HVDC branches or fail with excluded-component ledger, add x (validated ohm→pu), voltage classes and full source manifest. Run topology, ID, country and KCL **as a limited real-world topology/parameter witness**, not as a real IoSN operating-state or TSO-valid N-1 witness. Heuristically inferred electrical parameters remain labelled APPROX_OPEN_DATA.

**Priority B (first M2/MA1 real-flow smoke):** Provide physically balanced nodal injections, explicit HVDC/PST schedules, source-side branch-flow oracle and time-matched normal ratings for several real hours. If the five existing weather IDs are delivered, use only actually corresponding times; avoid artificial duplication to fill absent years. The pinned TimeSet requires 5 IDs, hence fewer real years support a **separate component-level check only**, not a literal MA1 G01/G04 run. A real full-calendar dataset is mandatory before reporting annual overload MWh/criticality.

**Priority C (MA2 calibration):** Add a *separately balanced* neutral reference set, diverse real dispatch hours and frozen train/selection/holdout partitions sufficient for numerical identifiability; replay real detailed flows and validate x>0, c0 and affine KVL.

**Priority D (MA3):** Add complete and authorized TSO contingency definitions, per-case emergency limits, seasonal/hourly applicability and exceptions; verify 4 directed-seasonal capacity values independently.

**Full pan-Europe qualification:** official/authorized synchronized reference-grid vintage with 2025 base and adopted 2035 starting-grid project changes; all 37 country labels and exact 102 quotas; all AC islands/border ties, HVDC, transformer, PST, 225/400-class lines; five fixed year inputs with real calibrated dispatch/reference flows; source-derived normal/emergency constraints; N-1 case list/TSO exceptions; real splits and independent reviewer. No source-independent substitution silently promoted.

## 6. Stop rules and qualification decision

- **REAL_DATA_READY:** every compulsory source payload and original SHA inspected, coherent 37/102 pan-Europe data and full temporal/security coverage, preflight+real replay+independent validation PASS.
- **PARTIALLY_READY:** at least one real inspected, qualified and reproducible input bundle satisfying an explicit limited gate (e.g. a real two-country topology witness), with missing higher-scope attributes transparently blocked.
- **BLOCKED_DATA (current):** no committed, admitted original real M2 grid+dispatch input bundle and no execution of real M2 flow/security gate evidenced; all available evidence is schema, synthetic, historical or prospective.

**Decision 2026-11-11: BLOCKED_DATA.** Documentation and synthetic tests are ready for acquisition planning, **not** a real network release. Independent R-PHY/R-CLU/R-NUM and interface reconciliation remain separate from data qualifications. No merge or M0/M1/selection change is authorized by this report.
