# M2-MA2-PRE — Global equivalent and coupled iteration: design package

**Project:** AlOussama/TYNDP_Products  
**Date:** 2026-11-12  
**Branch:** docs/m2-ma2-pre-design-20261112  
**Frozen task-base commit:** 27dfd810b39e17e6b616a2b0aeb813eb8948d8a0  
**Scope:** DOCUMENTATION + FUTURE TEST FIXTURE SPECIFICATIONS **ONLY**  
**Design handoff:** **MA2_PREP_READY_FOR_GATE** (*document-only readiness*, **not** MA2_IMPLEMENTED / MA2_AUTHORIZED / a qualified numerical test run). No source/runtime changes and no merge.

## 1. Deliverables

| File | Exact content |
|---|---|
| [ma2_equivalent_network_contract.md](ma2_equivalent_network_contract.md) | Proposed typed MA1→MA2 inputs; original-graph P/Gamma/A_z; global positive x/gauge, structural c0 in cycle space; correct source-free and phase-source affine KVL in **actual reduced solver**; identifiability, objective and pseudocode |
| [ma2_iteration_spec.md](ma2_iteration_spec.md) | Hard country/AC connectivity and critical-line gates; 2-/3-country coupled candidates; full Europe-wide refit; frozen train/selection/holdout; exact fixed monitors, strict RMSE acceptance/rollback, plateau, budgets, ledger and pseudocode |
| [ma2_analytic_oracle_cases.md](ma2_analytic_oracle_cases.md) | Independent dense cycle/KCL numerical solution method; exact triangle, square+diagonal, tree, multi-island, neutral HVDC, operational PST, rank/scale and three-country accepted/rejected mock decision cases |
| [ma2_test_and_gate_matrix.json](ma2_test_and_gate_matrix.json) | Machine-readable G05–G08, R-NUM, G12 and Owner gate predicates; **45 designed-only** test IDs with mathematical expected outcomes, source SHAs and future commands |
| [test_matrix.csv](test_matrix.csv) | Same 45 test IDs, gate, fixture, oracle and expected outcome; no simulated execution results |
| [owner_i_decisions.md](owner_i_decisions.md) | All proposed, **not selected**, numerical/project I decisions and signatures required before code or real use |

## 2. Inputs independently reconciled for this design

| Source | Pinned ref | Finding / design consequence |
|---|---|---|
| [Verbindlicher Auftrag 98](../98_M2_MA2_PRE_DOCUMENT_FIXTURE_MACRO_20261111.md) | 27dfd810b39e17e6b616a2b0aeb813eb8948d8a0 | Document-only, G06–G08 specification and fixtures, no MA2 production |
| [MA2 handoff 85](../85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) | 70e92ba9e62a320e58227ce9c2f03fad266f44bf | Common Europe-wide AC reference, x/c0 and coupled iteration, three splits, G05–G08 |
| [Review consolidation 93](../93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md) | task-base 27df | Five independent evidence refs and explicit no-go |
| [R-PHY independent report](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md) | c004e5330df2a018e567c8ef955ef2fc9d71e0ea | 4 P1 open; PHY-R01–04 need repair + different reviewer |
| [R-CLU independent report](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md) | 7d7d07d7af5966ddc26d0be1100a69013763d2e8 | 2 P1 + 3 P2; protected feasibility and 400-kV screen |
| [R-API comparison](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md) | 075c50903b7d51ec19befb4a4b8db1322ae33b2a | Option C **recommended**, not Owner-chosen; A API provisional |
| [D-REAL readiness](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/89_M2_D_REAL_GAP_GATES_AND_WITNESS_2026_11_11.md) | 6a8262f128ae3dd7e108afe2ade09028ea4f651f | BLOCKED_DATA, particularly real balanced neutral source |
| [R-METH authority review](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_INDEPENDENT_METHODOLOGY_AUTHORITY_DELTA_REVIEW_2026_11_11.md) | 754a79e11370dca2c25f1102d83ced5beb251522 | AUTHORITY_UNCONFIRMED, consultation O26 only |
| [Conditional MA2 code macro 100](../100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md) | 27df | **Prepared, not authorized** until independent repairs + Owner contract + scoped code GO |

### Current original MA1 API used *only for design compatibility*

Source code freeze [0254d867](https://github.com/AlOussama/TYNDP_Products/tree/0254d867a34b66ec7b56c90225605d29ea328916/src/tyndp_reduce/iosn_official): A.execute_ma1(grid, dispatch, time, ratings, budget, explicit_country_map, explicit_year_weights, protected_line_ids=...) -> MA1Result; A.ReferenceFlowCache; A.build_oriented_projection(grid, zone_of_bus) -> P/Gamma/A_z/A_d, zonepairs. Its frozen input manifest/output arrays are **not yet independently repaired/released**; proposed MA2InputV1 wrapper adds separate neutral source, frozen split/monitor policies and byte-attested provenance. No real code is changed or chosen canonical by this documentation.

## 3. Scientific decision trace (D / T / I / U / B)

- **D — consultation documented, not enacted authority:** 37 labels/102 country quotas; European AC coupling; reduction x/zero-balance correction, iterative comparison; device-neutral calibration; later N-1 four capacities (not delivered here).
- **T — mathematical invariants:** oriented A_z Gamma=P A_d; per-AC-island KCL; A_z c0=0 and source-free affine KVL on (f-c0). Known phase sources require explicit generalized KVL. Tree x unidentifiable; one gauge/meshed island; country quotas and no hidden MW slacks.
- **I — project-only proposal:** explicit gauge and x_ref; optimizer and regularization; unregularized data-rank test; frozen block split; fixed country-corridor monitors; strict selection delta/fairness rules; plateau and compute budgets; exact tolerances in fixture tests. All require Owner authority for product decisions.
- **U — not published/settled:** ENTSO-E exact solver, x and c0 weights, uniquely correct country-search neighborhood, topology-comparable official RMSE norm and thresholds, fixed PST/transformer reduced source map, adopted/effective later methodology.
- **B — hard blockers:** six MA1 P1 awaiting repair+independent reviews, canonical API Owner-pending, absent complete Europe/neutral/operational original data and source-byte proof, no R-NUM, no MA2 runtime/real approval.

## 4. Future **executable** test and review plan (NOT performed by this documentation macro)

**Prerequisite:** explicitly authorized separate MA2 code macro, a single independently repaired MA1 SHA, Owner-selected canonical API and a future distinct R-NUM. Test module paths below are **planned interfaces**, not existing files.

1. Create exactly the synthetic fixture objects and independent dense cycle/KCL reference arrays specified in the oracle document. Write signed source/input/split manifests and add stable 45 IDs to regression markers; do not invent original grid/weather/TSO bytes.
2. Implement W-EQ only on authorized source branch; perform unit tests and independent dense oracle replay; characterize rank and sparsity plus negative fail-closed paths.
3. Implement W-ITER only on authorized separate worker branch; compare source SHA/partition invariants and record **every** candidate; use injected deterministic evaluator for accept/rollback and independent true physics test for fit.
4. Integrate on authorized SHA, run physical/monitor/full package regressions, capture JUnit and diagnostic JSON, compare outputs against the test matrix. Suggested commands *after those tests are actually written*:

~~~bash
python -m pip install -e ".[test]"
python -m pytest -q tests/iosn_official/test_ma2_equivalent_oracles.py
python -m pytest -q tests/iosn_official/test_ma2_coupled_iteration.py
python -m pytest -q tests/iosn_official/test_ma2_split_monitor_gate.py
python -m pytest -q tests/iosn_official
python -m pytest -q
~~~

5. On a **frozen integration SHA**, independent R-NUM reproduces dense cycle oracle, actual affine reduced solver including phi, exact/global candidate refits and stable-source/monitor split, reviews negatives and published residuals. If P0/P1 found, workers patch, **new SHA and R-NUM re-review**. Independent R-PHY/R-CLU must also pass against the **same repaired MA1 SHA**.
6. R-NUM opens FINAL_HOLDOUT only after search and configuration freeze; report one final replay. Failure blocks qualification and cannot be repaired by tuning on the same revealed holdout. Any real qualification then requires separate original-byte and D4/data witness plus G12; MA3 is a later code macro.

**Document verification commands**, available immediately without MA2 code:

~~~bash
git diff --name-only 27dfd810b39e17e6b616a2b0aeb813eb8948d8a0..docs/m2-ma2-pre-design-20261112
git diff --check 27dfd810b39e17e6b616a2b0aeb813eb8948d8a0..docs/m2-ma2-pre-design-20261112
python -m json.tool docs/current/IOSN_Modul2_Netzaggregation/ma2_pre_20261112/ma2_test_and_gate_matrix.json >/dev/null
~~~

Verify test_matrix.csv contains the **same** 45 unique IDs in the same order as JSON. These checks validate document integrity only, **not** the absence of a future defect or mathematical solver runtime. Documentation-only work cannot truthfully claim R-NUM replay or numerical CI PASS.

## 5. Release ledger / next gate

| Object | Current permissible declaration |
|---|---|
| M2-MA2-PRE deliverables | **MA2_PREP_READY_FOR_GATE (DESIGN ONLY)** |
| MA1 repairs / independent replay | **REPAIRS_REQUIRED / RR1_PENDING** |
| Canonical API | **OWNER_PENDING**, option C recommended but not chosen |
| Methodology authority | **AUTHORITY_UNCONFIRMED** |
| Qualified real/neutral grid input | **BLOCKED_DATA** |
| MA2 actual production source + tests | **NOT_IMPLEMENTED / NOT_AUTHORIZED_FOR_RUNTIME** |
| MA2 R-NUM independent run | **NOT_RUN** |
| MA3 / G12 real network | **NOT_IMPLEMENTED / BLOCKED_DATA** |
| PR merge / main edits | **NONE / NOT_AUTHORIZED** |

No main/M0/M1/weather-year edits, code implementation, test execution claim, review signoff or Owner decision is created by this branch. The only successor for actual code is [conditional macro 100](../100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md) after its entry gate is met.
