# ML-C08 — Integration Validation Report

**NONNORMATIVE_RESEARCH** — No methodology, dataset, architecture, tool, mathematical model or KPI approved; owner MD/CL pending; native IoSN R04 tests NOT_EXECUTED; no external independent review; **G1 BLOCKED**.

## 1. Actual checks during this ML-C08 session

Pinned GitHub file reads at source commits, exact Git-blob comparisons and deterministic RFC4180-compatible CSV/typed graph joins were actually executed **in this session**; unlike upstream descriptions this is a new independent *computation* but not a person-independent scientific audit or external model execution.

| Executed in ML-C08 integration | Actual check outcome | Scope |
| --- | --- | --- |
| Exact MA01-SR universe | PASS_STRUCTURAL | 48 distinct original IDs; no SR-012/049 |
| R00/C07 requirement and test joins | PASS_STRUCTURAL | 48/48 identical primary tests |
| Original R03 definitions | PASS_STRUCTURAL | 87/87 unique B01-D |
| C03 classifications | PASS_STRUCTURAL | 93 direct +20 process-only +35 producers +38 T +18 P |
| Source data-SR link pairs | PASS_STRUCTURAL | 93 source pairs retained without new SR |
| Process-only classification | PASS_STRUCTURAL | 20 process-only without invented SR |
| P00–P17 and 38 transforms | PASS_STRUCTURAL | 18 process anchors, 38 distinct T |
| C02 typed graph | PASS_STRUCTURAL | 528 NODE, 1323 EDGE |
| C02 graph edges resolve | PASS_STRUCTURAL | all edges have existing typed NODE endpoints |
| C04 direct vs contextual | PASS_STRUCTURAL | 74=35 direct+39 context, all 48 SR |
| Native tests not executed | PASS_STRUCTURAL | 48/48 not run in R00 or either tool arm |
| C07 source SHA and G1 | PASS_STRUCTURAL | all 48 source refs correct, G1 blocked |
| Research risk tier | PASS_STRUCTURAL | 33 A, 12 B, 3 C proposed |
| No invented source approval | PASS_STRUCTURAL | 15 reconciled C01 conflicts still Owner-open |
| C07 data and assurance | PASS_STRUCTURAL | no qualified actual data/review |
| Direct T graph acyclic | PASS_STRUCTURAL | 47 unique direct T edges; topological traversal visits 38/38 |

Additional direct-graph test: reconstructed all **47** unique R03 transformation-to-transformation edges from intersecting declared output/input object IDs and verified topological traversal of all **38** nodes (no cycle). Verified exact expected active SR-ID set, R00–C03 data/SR joins, 20 process-only types, 48 C07 test and source pins, C02 528/1323 typed graph endpoint validity, 74 C04 SR associations and their strengths, C07 no actual tool runs and G1 BLOCKED.

C08 generated [end_to_end_requirements_traceability.csv](end_to_end_requirements_traceability.csv) with 48 SR rows, 20 process-only, 18 process anchors. Each SR row carries source clause/MR, P, R03 data and original B01-T IDs, T IDs/declared output objects, M/LR, primary R04 test/verification layers/depth and proposed risk tier, C04 direct/context benchmark associations, Owner/MD/CL/evidence status and **eight exact source branch SHA identifiers**. 86 rows, not 86 approved independent SRs.

## 2. Source provenance

| Source path relative to workstreams/ | Revision | Source Git blob SHA |
| --- | --- | --- |
| ML_R00_consolidation/integrated_requirement_traceability.csv | R00 #32 | a594580bd876a02613963afdfa351e47482e4289 |
| ML_C01_semantic_harmonization/semantic_conflict_register.csv | C01 #43 | 7095d1c5ebd4eabe756c4ce479b8b4bd23e0beb4 |
| ML_C02_contract_metamodel/contract_traceability_model.csv | C02 #42 | d10e19103aa44bcaac6df692ee3b7dbb64fd77c3 |
| ML_C03_process_contract_closure/process_data_math_dependency_matrix.csv | C03 #46 | 27f8eeaebc3fd581c5446428f9befaf512e07ae6 |
| ML_C04_scientific_benchmarks/benchmark_requirement_traceability.csv | C04 #45 | 26db4a147993dc65af97c3340d144edc01191565 |
| ML_C07_two_tool_pilot_readiness/pilot_execution_readiness_matrix.csv | C07 #49 | 3be9502846dc26b98362df60f30536b293f8db5e |
| ML_R03_data_process_contracts/input_contract_catalogue.csv | R00 #32 | 0ad7cde7b51a2e4aea229e6ac75c5dc7eda175ab |
| ML_R03_data_process_contracts/process_transformation_matrix.csv | R00 #32 | b664dcc134e3d31e25f0c710ac2beb855d2e2ff8 |

All original 81 C01–C07 files remain on seven separate Draft branches: no cherry-pick or modification of their original workstreams was required. Git commit/blob SHA proves **repository identity**, not authenticity/adoption or original external-data SHA-256 and Owner qualification.

## 3. What was *not* executed or approved

| Candidate claim | Actual evidence status |
|---|---|
| 48 R04 tool-native requirement checks | NOT_EXECUTED (source records only) |
| Original IoSN input bytes, effective source methodology | NOT_QUALIFIED / AUTHORITY_UNCONFIRMED |
| Generated E04 equations and E05 solver certificates | NOT_EXECUTED |
| Native two-tool C07 P0–P3 pilot | NOT_EXECUTED (design only) |
| C04 B01–B15 micro-oracles | Previously reported 15+15 local self-checks; **NOT reexecuted in ML-C08** |
| C04 26 native mutants | DESIGN_ONLY |
| C06 custom A/B/C benchmark (135 + 24) | Previously reported shared-harness local results; **NOT reexecuted in ML-C08** |
| Native SysML/ReqIF/SHACL/GEMS etc parser | NOT_TESTED |
| Actual independendent external reviewer/Owner signoff | NOT_OBTAINED |
| G1 | BLOCKED |

**Mathematical warning:** E-FEAS projected feasible-set equivalence, E-OPT optimal-face equivalence and E-OBS selected observations are *not* proven by structural joins or matching toy KPIs. No extra general robustness requirement added.

## 4. Critical integration review and disposition

This integration produces **31** sourced findings (15 inherited C01 INT crossworkstream conflicts plus 16 newly classified C08 critical checks), with explicit severity, impact, closure evidence, and retained Owner/TBD gates. See [cross_workstream_findings_register.csv](cross_workstream_findings_register.csv). Review is AI-assisted, not a human-independent assurance.

**Outcome:** PASS_STRUCTURAL_WITH_EXPLICIT_OPEN_RESEARCH_SCIENTIFIC_AND_GOVERNANCE_GAPS; REAL_MODEL_NOT_EXECUTED; OWNER_ORACLES_TBD; G1 BLOCKED. Later post-write Git compare must establish only 12 C08 added files and PR Draft status.
