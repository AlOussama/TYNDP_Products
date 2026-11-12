# M2-MA2-PRE / W-ITER-SPEC — Coupled-country search, immutable splits and comparable RMSE

**Status:** PROPOSED_DESIGN_ONLY, v0.1 / 2026-11-12. This is **not** a run result and provides no permission to implement or operate MA2. The underlying MA1 API is provisional pending independent repair/re-review and an explicit Owner canonical-API decision.

## 1. Search domain and the invariant frontier

The physical search domain is a **single global AC network**. Country labels only restrict membership of each zone. For every source-country label c, the exact integer k_c of nonempty zones is invariant. In the full published consultation-profile geography this is **37 separate labels / 102 zones**, with Northern Ireland and United Kingdom distinct. All small tests require visibly synthetic quotas. HVDC edges never create AC adjacency or permit AC-connectedness. Every preserved original active cross-border AC branch participates in the shared electrical calculation.

Let z: original bus ID -> zone ID. A candidate is admissible iff:

1. Every original bus assigned exactly once; country labels unchanged and every zone is country-pure.
2. For each c, number of nonempty zones = k_c; each induced original-AC zone subgraph connected; cross-island zones forbidden; no country-local hidden power balancing.
3. Frozen protected_line_ids remain interzonal, all required critical-line classifications and ratings are source-qualified. Missing/unaudited protection = **BLOCKED_PROTECTION_POLICY** (never silently default empty for a real run).
4. Original grid/reference/time/split/source bytes fixed. An eligible move may not add/drop AC branches, adjust dispatch, alter ratings, change five external years, or modify protected line membership.
5. Candidate SHA includes **canonical partition membership** independent of arbitrary renaming, reference SHA, protected policy ID, and move-plan ID. IDs for the new zonepairs are regenerated and may not be joined to previous candidates by index.

## 2. Deterministic multi-country candidate generator

Construct a *country interaction graph* K: vertices are source country labels; an undirected edge exists iff at least one **active original AC intercountry branch** joins the countries. HVDC-only adjacency is excluded. Enumerate bundles on induced connected K-subgraphs with 2 or 3 countries, plus 1-country control candidates; original 37-country breadth is an input, not a loop selecting countries in isolation. The full European physics is always refitted, even when a bundle touches only 2/3 countries. Deterministic order: country-label tuple, move type, original bus IDs, canonical resulting partition SHA.

Candidate operators (all moves **within** one country):
- **BOUNDARY_MOVE:** transfer a boundary bus from zone U to adjacent same-country zone V; U remains nonempty and connected, V remains connected; k_c unchanged.
- **BALANCED_SWAP:** exchange boundary buses u in U and v in V (or connected small subsets), such that both resulting zones remain AC-connected and nonempty. Here 'balanced' means **zone-count preserving**; it does not require equal zone size or fabricated MW balance.
- **COUPLED_BUNDLE_2/3:** synchronous tuple of independently legal same-country boundary moves/swaps in 2 or 3 AC-coupled countries; candidate validated **after applying the entire bundle atomically**. Intermediate invalid maps are never fed to the fitter.
- **PROTECTED_REJECT:** explicit negative class when a change internalizes a protected original branch; **DISCONNECTED_REJECT**, **QUOTA_REJECT**, **CROSS_COUNTRY_REJECT** and **ISLAND_REJECT** likewise pre-fit.
- **DUPLICATE_MAP:** no-op or already attempted canonical partition; skip expensive refit, but write a ledger record.

The generator must not rely on MA1's known false-infeasibility greedy behavior (R-CLU-001) as a proof of candidate infeasibility. Use complete independent validate_busmap, additional exact-small-graph oracle for feasibility claims and status **HEURISTIC_STUCK** rather than 'mathematically impossible' when no proof exists. The 'protected' set must be derived from an auditable policy including annual 225/400-class screening, not the currently unsafe 400kV class-0 opt-out (R-CLU-002). Input-mutation, truthy booleans and unsafe tolerances (PHY-R01..04) remain pre-run blockers until independently repaired.

## 3. Immutable split contract

A SplitManifestV1 is created **once before the first candidate**:
- time_axis_sha256, original five **external** year IDs, full ordered immutable snapshot IDs, durations (hours), season, dispatch/source hashes, partitions TRAIN, SELECTION, FINAL_HOLDOUT, optional EMBARGO, split_algorithm_version, deterministic seed, list SHA and owner;
- three nonempty disjoint index sets with strict union equal to admitted snapshots **minus explicitly documented embargo**; no duplicates, hidden leakage, sorting, reweighting or replacement of year IDs;
- stratify/block within each of the five **already delivered** years and both supplied seasons when sufficiently covered, preserving chronologically contiguous blocks and an embargo between temporally correlated blocks. If coverage per year/season is inadequate, **INSUFFICIENT_SPLIT_COVERAGE** rather than silent extrapolation. Splitting hours **does not select weather years**.
- Neutral and operational training/replay align on snapshot keys (a separately balanced neutral dispatch may differ physically); keep their hashes distinct. Any new split/source/input byte => a **new experiment/run identity**, never mutate a trial mid-search.
- Fit of x/c0, weights, source-provider mapping calibration, numerical rank, x priors and early stopping may see **TRAIN only**. Candidate choice and plateau use **SELECTION only**. FINAL_HOLDOUT is sealed; only final post-selection independent replay can open it. If final holdout fails, report failure and stop; reusing it to tune is leakage.

Proposed fixture split only (project I): five synthetic IDs MOCK-CY1…MOCK-CY5, six UTC snapshots per ID. For each year ordinal 0/1/2 => TRAIN; ordinal 3 => EMBARGO; ordinal 4 => SELECTION; ordinal 5 => HOLDOUT. Counts: 15/5/5 with five embargoed. These are **synthetic fixture clocks**, not original five years or official ENTSO-E split instructions. Real block lengths/coverage must be separately approved.

## 4. Full pan-European re-projection and x/c0 refit per candidate

For **every feasible nonduplicate candidate**, rebuild from the immutable *original* grid (not incumbent reduced network):
- original global A_d, candidate P(z), Gamma(z), A_z(z), full candidate sorted zonepairs and memberships; verify A_z Gamma = P A_d exactly;
- for **all identical source hours** derive candidate p_z = P p_detail, target f_z = Gamma f_detail separately for operational and separately balanced neutral reference. Do not recompute original dispatch/physical reference differently per candidate;
- regenerate reduced AC-island/cycle basis and source provider for that candidate; check source semantics; fit **all** reduced AC-islands (not only altered countries) using TRAIN and the W-EQ contract. An island can have a new number of cycles or become unidentifiable; report not-ready, not an invented result;
- fit with documented gauge per actual reduced AC-island, source SHA and split SHA unchanged. Warm starts from incumbent are permissible only as optimizer **initial guesses**, never accepted as a refit or rank proof; no cached incumbent calibrated x/c0 is authoritative for the new map.
- replay TRAIN/SELECTION through the actual affine reduced simulator, not f_eq = oldH p + fitted plotting offset. If operational HVDC/PST cannot be represented, report DEVICE_SOURCE_UNQUALIFIED; do not fall back to a fabricated device-neutral operational score.

'Global' means **all European AC-islands considered under one run/gate and uniform source/time identity**; island sparsity remains structurally block-diagonal. Do not invert a dense Europe-wide matrix or introduce per-country slacks. A source-flag change, missing fixed-transformer phase, unsupported loss/tap/3-winding device, or silently excluded 110kV tie forces FAIL_CLOSED.

## 5. Fixed, topology-comparable monitor contract (G08)

A raw RMSE averaged over the *candidate-specific* list of E zonepairs is **not** directly comparable when E or the physical cut membership changes. Keep raw link metrics as **diagnostics only** and report link_count, pair IDs, per-link RMSE/MAE/quantiles and captured critical branches separately.

Create the **fixed original-graph monitor catalogue before any candidate**. Primary exact monitor family:
- each eligible intercountry physical **country-pair corridor** (c1,c2) defined by the fixed set of original active branch IDs crossing c1/c2, signed in canonical country order. Every zone remains country-pure, so for any candidate the reduced estimate of this monitor equals the signed sum of the **reduced zonepair flows** whose endpoint country labels are (c1,c2). The reference is the signed original detailed sum over the same fixed original branch IDs. The monitor index, physical inclusion, orientation, hourly target and base weight never change when zonepair counts change;
- exact **protected corridor bundles** defined as an immutable union of complete original zonepair cut memberships **for each admitted candidate** may be added if the exact same original branch set can be represented, without double-counting. If a protected original branch is mixed into an aggregate link containing unmonitored original branches, **individual-branch reconstructed flows are not observable from f_eq alone**. Mark monitor UNREPRESENTABLE and reject if coverage is mandatory. Never assume proportional branch allocation or infer hidden counterflow as physical truth;
- predeclared country-level fairness groups and border regions are stable IDs. For a country with no observed eligible monitor, declare NO_MONITOR and fail the mandatory coverage gate; do not impute zero error.

For each candidate and fixed monitor m construct **linear** M_z from its reduced ordered links, and immutable target y_m,t from original operational source. Do not form M_z from an incumbent or Selection/Holdout regression. Both target and prediction use identical source hours, durations and orientations. Verify monitor physics independently against Gamma. Monitor algebra is exact only for representable fixed sets. Any physical branch internalization that prevents an obligatory monitor is a hard rejection, not a metric omission.

For a fixed index set \(\mathcal M\) and SELECTION times \(\mathcal S\), with fixed predeclared dimensionless weights \(w_m>0\) and durations d_t>0, primary proposed project-I objective (MW) is:

\[
 J_{\mathcal S}(z)=
 \sqrt{\frac{\sum_{m\in\mathcal M,t\in\mathcal S} w_m d_t(\widehat y_{m,t}(z)-y_{m,t})^2}
 {\sum_{m\in\mathcal M,t\in\mathcal S} w_m d_t}}.
\]

**Same** monitor IDs, reference y, d, w and selection indices for every candidate. Report secondary MAE, P95/P99 absolute error, per-country max RMSE, critical-line capture fraction, protected-line preserved fraction, country-pair fairness, internal/cancelled parallel counterflow flags, raw zone-link RMSE and link_count. Source-derived small reference flows should not cause unbounded relative ratios: normalized error requires a declared fixed denominator and zero-flow policy. Neither the 200/350/500-MW figure colors nor 10/20/30% consultation legend imply official acceptance thresholds.

**Caution:** even exact country-pair sums may be insensitive to some changes (e.g. a radial country graph with no alternative paths); that is an **insufficient monitor discrimination** gate, not evidence of optimal aggregation. Choose predeclared genuinely sensitive and observable monitors with independently tested rank/variation; no tuning the monitor catalogue after seeing Selection.

## 6. Accept/rollback, plateau, budgets and immutable audit

Each candidate gets a **decision**, including pre-fit rejects. Proposed decision order:

1. Structural/source/split/protection validations -> explicit pre-fit status and zero fit calls on failure.
2. If feasible, **complete new global** x/c0 fit and independent KCL/KVL/rank gate -> G06_PASS_SYNTHETIC only if future implemented tests prove it; otherwise reject with numerical/status reason.
3. Require 100% predefined mandatory monitor coverage with same IDs/hours/reference; missing comparison => REJECT_UNCOMPARABLE, not an artificially lower J.
4. Compute J_SEL and strict improvement vs incumbent \(J_{\rm inc}-J_{\rm cand} > \max(\delta_{\rm abs},\delta_{\rm rel}\max(J_{\rm inc},J_{\rm floor}))\). The tolerances are **project I, OWNER_PENDING**; equality never accepts. Additional fairness/protection hard guards may veto an otherwise smaller J. No Select-derived model tuning.
5. Among *improving admissible* candidates in a fixed round choose minimum J_SEL, then minimum max-country RMSE, then minimum counterflow/coverage-risk diagnostic, then lexical canonical candidate SHA. Commit **one** fully validated map/result pair atomically; leave other candidates recorded as REJECT_NOT_BEST.
6. If none improves, keep the entire immutable incumbent bundle (map, operators, x/c0, monitors, hashes). Failed/timeout candidates cannot partially overwrite it. Log REJECT_NO_IMPROVEMENT / ROLLBACK and the exact δ.
7. Plateau after P consecutive completed no-improvement rounds; EXHAUSTED if deterministic neighborhood empty; MAX_EVALUATIONS_STOP when configured evaluation count exhausted; CPU/WALLTIME_BUDGET_INTERRUPTED is **not convergence**. Holdout remains unopened. No automatic permission to start MA3 or report capacities.

For every attempted move, write CandidateLedgerV1: trial_id, parent/incumbent SHA, sorted touched countries/bus moves, candidate partition/operator hashes, original source/time/split hashes, protection and quota results, topology/zonepair/link counts, all pre-fit statuses, attempted full-refit flag, **all reduced island IDs**, optimization diagnostics (or explicit 'not run'), x/c0 gauge/rank/KCL/KVL residuals, fixed monitor IDs+weights+coverage, TRAIN/SELECTION score, per-country and border diagnostics, reason code, acceptance/rollback, tie-break decision, CPU/evaluation counts and terminal state. No ledger entry may include FINAL_HOLDOUT values until a separate final replay artifact is appended by independent reviewer.

Recommended statuses: GENERATED, REJECT_COUNTRY, REJECT_QUOTA, REJECT_CONNECTIVITY, REJECT_PROTECTION, REJECT_ISLAND, REJECT_BAD_SOURCE, REJECT_DUPLICATE, REFIT_FAILED, UNIDENTIFIABLE, REJECT_UNCOMPARABLE, REJECT_FAIRNESS, REJECT_NO_IMPROVEMENT, REJECT_NOT_BEST, ACCEPT, ROLLBACK, PLATEAU, BUDGET_STOP, FINAL_HOLDOUT_REPLAYED. Keep invariant reasons from exceptions, not generic 'solver failed' only.

## 7. Read-only algorithm pseudocode

~~~text
freeze original MA1 input artifacts, source bytes, operational reference,
       separate balanced neutral reference, 5 external years, ratings,
       protection policy, fixed monitor catalogue, split manifest
assert all frozen SHA and independent preflight gates
incumbent = validated seed; fit/incumbent selection via GLOBAL fit once
for round in 1..MAX_ROUNDS:
    trial_pool = sorted(enumerate_within_country_moves_and_coupled_bundles(
                            original_AC_country_interaction_graph, incumbent))
    best = none
    for candidate in trial_pool:
        entry = start_immutable_ledger(candidate, frozen_SHA)
        if duplicate or invalid quota/purity/connectedness/critical lines:
            ledger.reject_before_fit(entry, precise_reason); continue
        P,Gamma,A_z,A_d = rebuild_from_original_grid(candidate)
        assert A_z*Gamma == P*A_d and same hours and source SHA
        project FULL original operational+neutral MW to new map
        eq = fit_global_equivalent_for_ALL_AC_ISLANDS_on_TRAIN(...)
        if eq fails physical/sensitivity/device-source gate:
            ledger.reject(entry, eq.status); continue
        if any mandatory fixed monitor cannot be represented:
            ledger.reject(entry, REJECT_UNCOMPARABLE); continue
        score = evaluate_only_predeclared_SELECTION_monitors(...)
        record score and fairness and candidate-specific link diagnostics
        if strict improvement and hard guards satisfied:
            best = deterministic_rank_min(best,candidate,score)
        else: ledger.reject(entry, REJECT_NO_IMPROVEMENT/REJECT_FAIRNESS)
    if best exists: atomically_replace_incumbent(best); reset plateau
    else: preserve incumbent unmodified; increment plateau
    if plateau reached: terminate PLATEAU
    if evaluation or time budget reached: terminate appropriate BUDGET status
seal selected map and source/split/fit/score SHA
R-NUM separately opens FINAL_HOLDOUT **once**, never reoptimizes from it
if replay shows failure: FINAL_HOLDOUT_FAIL; do not retune on same holdout
~~~

## 8. Concrete three-country search oracle and expected decisions

Fixture topology: three synthetic AC-coupled countries A, B, C; each has four buses a1..a4, b1..b4, c1..c4, an interior square (1-2-3-4-1) **plus a protected 1-3 diagonal**; exactly **two zones per country**. Baseline for each c: c1,c2 in zone 1; c3,c4 in zone 2. AC intercountry ties a2-b1, b2-c1, c2-a1 form a country triangle (not HVDC). Each zone is AC-connected; protected diagonal c1-c3 is interzonal both before and after the valid swaps c2↔c4. The A+B paired swap and A+B+C triple swap each preserves three hard quotas and country purity. Require independent validation of the global AC reduced mesh and full new refit in either case.

To isolate the **decision engine** from fit arithmetic, inject a **test-only deterministic evaluator** that returns fixed three-country-pair monitor vectors at a selection snapshot, all conserving country net injections p=(−4,+2,+2) MW under oriented A→B, B→C, C→A. Target (2,4,6); baseline predicted (6,8,10) => J=4 MW; 2-country A+B swap predicted (3,5,7) => J=1 MW => ACCEPT (for proposed δ<1 MW); subsequent A+B+C candidate predicted (5,7,9) => J=3 MW => REJECT_NO_IMPROVEMENT and bitwise ROLLBACK to incumbent. **These numbers are a mocked evaluator/decision oracle only**, not a claimed solution of the calibrated nonlinear x/c0 network or real reference data. An independent end-to-end electrical fit test must separately construct source-consistent snapshots with known x/c0 (see oracle document). The test must prove evaluator called only after full refit for feasible candidates; it may not use these mock scores to certify physics.

Negative paired candidate: change c2↔c3 in a country so that protected diagonal c1-c3 would become internal (and remaining zone disconnected on square-only branches) => REJECT_PROTECTION or REJECT_CONNECTIVITY before fit. A country-bus transfer to another country must be REJECT_COUNTRY regardless of score. Verify country interaction graph and deterministic two-/three-country enumeration. Finally change one zonepair count while keeping the three **fixed** country-pair monitors; verify changed raw zone-link RMSE is flagged NOT_COMPARABLE_RAW, but fixed J can still be compared when representability holds.

## 9. Future outputs and gates

Documentation-only design schemas for future candidate_ledger.csv/json, equivalent_network.json, fit.json, fixed_monitor_manifest.json, rmse_per_link.csv, selection_scores.json, input_split_manifest.json, exception_ledger.json, final_holdout_report.json, independent_review.md. Write-once staging plus atomic manifest/READY publication is proposed; a partially written run is NOT_READY. Report all source/time/split SHA across every candidate and include versioned monitor catalogue and zonepair shape. No output called REAL_QUALIFIED without data/provenance/G12; no MD-03 or MD-13 official oracle until owner evidence.

G05: quotas/connectedness/protected cuts/projection; G06: x/c0, affine KVL, rank/physical replay; G07: global refit per feasible trial, immutable split and ledger; G08: fixed monitors and comparable selection metric, sealed holdout, fairness/critical-line diagnostics. Actual PASS requires later implemented independent tests and R-NUM, not this specification.
