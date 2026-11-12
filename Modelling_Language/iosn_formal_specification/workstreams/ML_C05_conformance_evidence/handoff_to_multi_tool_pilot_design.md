# ML-C05 — Handoff to Future Multi-Tool Pilot Design

**2026-11-12 · DESIGN HANDOFF ONLY · Pinned ML-R00 baseline: PR #32, SHA 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Mission and strict boundary

This is a **handoff for designing a later two-tool IoSN scientific pilot**, not authorisation to run one. Both future teams independently realise the **same frozen tool-neutral IoSN Requirements Contract** and use the same declared input profiles. One tool's native model, solver output or converted DSL must **not** be used as the other team's definition of truth. ML-C05 does not choose a tool, language, architecture, schema, solver, transport format or implementing organisation.

Pilot objective: produce an independently inspectable **chain of evidence** from E01 source/contract and E02 inputs through E03 transformations, E04 generated mathematical obligations, E05 numerical solutions, E06 raw results, E07 independent KPI replay and E08 status/review decisions, while accurately stating which properties are and are not established.

**Do not confuse:** research prototype tests, a scientific two-tool pilot, productive IoSN implementation acceptance, vendor/tool certification, Methodology Owner approval and Gate G1. They are separate events and require different evidence/authority.

## 2. Prerequisite release gates (present state)

| Gate | Minimal owner-supplied future input | Current state / cannot infer |
|---|---|---|
| **G-P0 Method authority** | Authorised effective IoSN release with original bytes/identity, exact scope and clause→48-SR reconciliation; D1–D6 record and O26 versus D2 research overlay resolved | **BLOCKED**: MD-01/18/19/20; O26 consultation is a draft |
| **G-P1 Data freeze** | Qualified actually consumed data releases with actual original byte hashes, provenance, external CY1–CY5 for each target year, cross-year weight vector, UTC intervals/Δt and unit/zone mappings | **BLOCKED**: original data unqualified; MD-11/12/18 |
| **G-P2 Domain oracles** | Approved physical and economic parameters, P05/P06 network reduction quality oracle and PTDF/LODF/N−1 cases, stage carry-forward, storage/H2/DSR, LF/conditional OPF and KPI definitions | **BLOCKED**: MD-02/03/04/06/07/08/09/10/13/15/16/17 |
| **G-P3 Verification policy** | Approved applicability rules, V/D/risk allocation, numerical acceptance tolerances, claim/reviewer protocol and negative-oracle validation | **NOT_OBTAINED**: ML-C05 is only research design |
| **G-P4 Independent teams/review** | Independently built Tool A and Tool B models, qualified oracle/reviewer roles, frozen reproducible builds, conflicts of interest/role separation | **NOT_EXECUTED** |
| **G-P5 Formal project gate** | Explicit later Gate G1 decision by authorised actors based on all necessary evidence | **G1 = BLOCKED**, unchanged |

**Allowed before the above gates:** model-independent synthetic fixture design, proof-of-concept evidence schema experiments, independent oracle design and negative mutations, format evaluations and reviewer planning. **Not allowed to claim:** officially approved model, source-qualified datasets, productive IoSN tool conformance, or an executed two-tool pilot.

## 3. Future pilot architecture as roles, not products

~~~text
                                    Frozen semantic Requirements Contract
                                   (source/revision/48 SR/guards/oracles)
                                        │                      │
                                  Frozen input profile     Independent oracle suite
                                        │                      │
                            ┌───────────┴───────────┐          │
                            │                       │          │
                 Independent Team A       Independent Team B   │
                 Tool/model generator A   Tool/model generator B
                            │                       │          │
                       E02-E06 A                E02-E06 B       │
                            └───────────┬───────────┘          │
                                        │                      │
                              Evidence collector / verifier ←──┘
                                        │
                              E07 independent KPI replay
                                        │
                           E08 per-SR status, cause and claims
                                        │
                          Qualified independent reviewer
                                        │
                        Separate Methodology/Data/Gate Owners
                                (no automatic approval)
~~~

Permissible shared components are the **contract definition, approved source releases, input fixture identities, oracle specifications and evidence semantics**. Implementing teams must independently create model formulations and generator code; common copied implementation artefacts must be disclosed and treated as a dependency threatening independence. An independent oracle may be reused when its authoring, versioning and review are demonstrably separated from both implementations.

## 4. Pilot design phases and falsifiable exit artifacts

| Phase | Activity and evidence | Future exit criteria | Scientific limitation |
|---|---|---|---|
| **P0 — Contract freeze / capability** | E01, E02, E08; exact 48 SR and status guards, feature-and-inspection capability probes, source versions | No unknown or silently skipped mandatory assertion; all exceptions listed | Structural completion not model conformance |
| **P1 — Negative control / synthetic cases** | Original R04-C01–C10 extended by C05 ST-01–ST-32, ML-C04 microbenchmarks if later available; independent analytic oracles | Each targeted wrong formulation detected under actual execution; good controls do not yield false FAIL | No real IoSN source/data verification |
| **P2 — Native generated models** | Each team separately builds declared year/CY/stage/variant LP model, exports E03/E04; targeted D3 and triggered D4 review | Required row/variable/index/objective invariants independently reconstructed; model differences explained by mapping | Generator inspection alone not solution validity |
| **P3 — Native solver runs** | Each team exports E05/E06 on the exact frozen instance(s) | Independently checked primal feasibility, admissible optimality evidence and accepted tolerances; not just OPTIMAL text | One instance not entire feasible space |
| **P4 — KPI and equivalence assessment** | E07 independent replay; E-FEAS, E-OPT-VALUE/SET, E-OBS statements selected by proof strength, multiple-optima analysis | Invariants proven in scope; portfolio-specific differences retained and explained | Equal KPI does not prove identical equations |
| **P5 — Assurance and controlled claim** | E08 status vector, exception registry, full trace and qualified reviewer report | Claims only where mandatory assertions/evidence/oracles fully discharged; actual owner/gate signoff separate | Qualified technical review does not automatically set G1 |

These are **design phases**, not a project schedule, milestone commitment or evidence that a pilot has been run.

## 5. Mandatory test population and variant matrix

The source verification baseline contains **48 provisional MA01-SR** and corresponding primary R04-T-SR-NNN assertions. Keep all 48 in the pilot planning matrix, not merely the six deepest cases.

| Test cohort (illustrative) | Mandatory science target | Planned depth / special check |
|---|---|---|
| 001–011 (excluding absent 012), 039–040, 047–048 | Scope, study years, external data/time, weather, offshore baseline, source and tool-neutrality | V1/V2/V6; D0/D1, D2 as per matrix |
| 013–023 | Zonal reduction, six output classes, detailed network comparison and disaggregation | V1–V5 as applicable; SR-017 and 019 D4 when triggered |
| 024–026 | Mandatory LF, dispatch comparison, optional P15 OPF guard and LF candidate cap | SR-024 remains mandatory; SR-026 N/A only under documented OPF false |
| 027–036 | Objective, physical network, shared investment, bounds, stages, storage, controllable candidates, NTC | D3 generated models and targeted D4 for 027/029/035 and 018 |
| 037–038, 043–046 | Offshore cost, detours, discount/price-year, filter and output KPI | Source/parameter owner TBD; explicit raw versus derived output |
| 007–009, 033–034, 041–042, 050 | H2, pre-expansion freeze, storage, hydro, DSR and sector coupling | Carrier/unit conservation and typed generator inspection |

Cohorts overlap by design; the **canonical exact SR list** and each row's complete minimum D-level remain the inherited R04 matrix and the explicit 48-row C05 verification_status_test_cases.md. Cohort grouping does **not** exclude low-risk mandatory items or create new SRs.

### Per-case input and result contract

For each independent Tool A and B test run, pin:

- **input**: source and input manifest digests; study y, CY1–CY5 and same *possibly nonuniform* weight vector across years; UTC interval/Δt, zone/carrier/technology and source units; conditional OPF guard; stage/candidate allowlists;
- **model**: semantic-to-native mapping, original row/variable identities, generated constraints/objective, bounds, freeze/transform provenance, model digest;
- **solver**: version/build/configuration/seed/threads, primal solution, objective decomposition, numerics/dual or bound certificate and error state;
- **output**: raw portfolio and operation, weighted results, independently recomputed KPI; alternative optimum characterisation where relevant;
- **verification**: asserted SR/Test ID, V/D/risk and applicable condition, accepted oracle/tolerance, actual attempt and evidence hashes, six-status disposition, reviewer identity/null and open cause;
- **governance**: explicit method/data/owner status and separate gate record.

## 6. Specific safeguards before calling two implementations comparable

1. **Common input identity:** identical semantic input instances—not merely same filenames. Original source qualification, UTC/calendar and unit alignment must be checked independently.
2. **Semantic model identity:** physical branches, market links, stage-transition semantics and H2/SoC carrier constraints must map correctly; a model-to-model conversion is not an independent implementation.
3. **Mathematical obligation proof:** compare projected feasible sets where justified, otherwise state weaker per-property evidence. Require meaningful D3 generation and D4 on documented triggers.
4. **Numerical certificate:** independently reconstruct primal feasibility and justified optimality, not compare tool logs alone. Identical solver numerical setting is neither necessary nor sufficient for equivalent mathematics.
5. **Observables and multiple optima:** compare KPI formula revisions and invariants; two different feasible optimal portfolios do not fail solely on IDs. Where a KPI is not invariant, report independently reconstructed portfolio-specific values and, if proven, ranges.
6. **Independence of oracle:** compare against controlled external/analytical reference, not only Tool A versus Tool B. Shared implementation bugs can produce identical outputs.
7. **Full fail-closed scope:** capability absence UNSUPPORTED; unresolved oracle BLOCKED; omitted run NOT_EXECUTED; actual contradiction FAIL; P15 disabled with evidence only SR-026 NOT_APPLICABLE.
8. **No false release:** all favorable scientific pilot results remain **scoped evidence**, requiring later separate source/owner/G1 decisions.

## 7. Minimum expected outputs from the *future* pilot

| Future deliverable | Required content | Responsible role (proposed) |
|---|---|---|
| Frozen contract pack | SR/VN/L4/profiles, source authority, explicit open MD and effective variants | Contract/Methodology Owner |
| Frozen input/lineage pack | E02/E03 with original data byte hashes and transformation witnesses | Data Owner and each tool team |
| Two native model packs | Separate E04 generator row/variable/term exports and semantic crosswalks | Team A, Team B independently |
| Two solver/result packs | E05/E06 complete raw attempts, logs and model mappings | Team A, Team B |
| Independent oracle pack | Analytical/negative fixtures, model projection checks, accepted numeric thresholds | Independent verification team |
| KPI replay & comparison pack | E07 formula-authorised replay and non-invariant multiple-optima notes | KPI/verification team |
| Test and exception ledger | E08 all SR/tests, six statuses + cause, excluded branches and staleness | Conformance coordinator |
| Qualified assurance and decision records | Reviewer report and separate explicit owner/gate decisions | Independent reviewer / authorised owners |

Suggested logical directory grouping for later review (not prescribed file transport): frozen_contract / released_inputs / tool_A / tool_B / independent_oracles / comparisons / exceptions_and_closure / qualified_review. Stable identities and proof obligations matter more than filenames or exchange syntax.

## 8. Stop conditions and future go/no-go protocol

**Stop a C-FULL claim**, but keep research and issue diagnosis possible, on: unknown method authority; unqualified original data; missing owner oracle/tolerances; an applicable mandatory test FAIL/UNSUPPORTED/BLOCKED/NOT_EXECUTED; unproven P15 N/A; missing E04 model inspectability; missing numerical certificate for a claimed optimum; unreconstructable KPI; unqualified reviewer; or active dependent stale evidence.

Escalate **D4 deep equivalence** on documented high-risk mathematical model differences, not automatically for every implementation and not merely because code differs. Open a finding with SR, root cause, counterexample or missing evidence, proposed resolution owner, old/new versions and rerun plan. A later formal go/no-go must be an explicit authorised human action, never the output of an algorithmic score.

## 9. Handoff questions that remain to be resolved later

- Which officially adopted methodological source revision controls all 48 provisional SR and the D2 3-versus-5 weather conflict?
- Which original files, data rights, input versions and accepted calendar/time/units are actually frozen?
- Which detailed-network reference and tolerance evaluate reduction, PTDF/LODF/N−1, directional capacity, RMSE?
- What are the approved stage-1→stage-2 investment/cost transfer, H2 baseline freeze and storage/hydro rules?
- Which cost, discount, price-year, VoLL, filter, KPI and result-equivalence conventions are signed?
- Which model-generator export and solver certificate methods are sufficient to make V3/V4 inspectable?
- Which external persons/organisations can qualify oracles, review independently and separately decide G1?

These are **deferred Owner/verification decisions**, not blockers to completing the present research design. No invented values or premature tool/DSL selection are allowed.

**Current handoff status: DESIGN_READY_FOR_FURTHER_RESEARCH_ONLY. Pilot: NOT_EXECUTED. Source/Data/Oracle: NOT_QUALIFIED. Independent assurance: NOT_OBTAINED. G1 = BLOCKED.**

**Primary sources:** ML-R04 future_multi_tool_pilot_requirements.md, tool_conformance_evidence_specification.md and requirements_verification_matrix.csv; ML-R00 research_backlog_and_gate_plan.md (RC-05/08); ML-R02 A/B/C architecture alternatives; ML-R03 provenance rules.
