# ML-C08 — Integrated IoSN Scientific Contract Reference

**NONNORMATIVE_RESEARCH** — No methodology, dataset, architecture, tool, mathematical model or KPI approved; owner MD/CL pending; native IoSN R04 tests NOT_EXECUTED; no external independent review; **G1 BLOCKED**.

## 1. Frozen research inputs

**Repository:** AlOussama/TYNDP_Products. Base: ML-R00 Draft PR #32 commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2. C01–C07 sources were read by exact PR-head ref and their blob IDs compared; all seven open Draft research PRs were previously verified to contain new files exclusively in their own source workstream versus R00. No source branch or original MA01-SR is changed by this integration.

| Workstream | PR | Head SHA | Purpose |
| --- | --- | --- | --- |
| R00 | #32 | 9162def25d22c37b1fbc38f7d80fe929425cc8d2 | immutable common base |
| C01 | #43 | 160774b05fee0c1b342ed139cc5d56ed6e7079fc | pinned Draft research head |
| C02 | #42 | 136b35e9dc2206b38c95b1e9a68b7d9598a5f86c | pinned Draft research head |
| C03 | #46 | 212bad6811877f9b974b20a1047913c18b1ba756 | pinned Draft research head |
| C04 | #45 | 256541e763147dcb118a3a9d24ca2f52035c672e | pinned Draft research head |
| C05 | #44 | 1d1bfd18e92d457b415bbad54450bd5aec10963a | pinned Draft research head |
| C06 | #50 | 2d306845a2855a9956e7dc685df423e304ebbb52 | pinned Draft research head |
| C07 | #49 | 4c6f33f37820feb91fc99e9229d7d164ea38283e | pinned Draft research head |

## 2. Common requirements/process/data/mathematics reference

**48 unchanged MA01-SR identities**, no active SR-012/-049; R01 M01–M18; process P00–P17 (18 stages); R03 **87** unique original B01 data definitions, **67** directly SR-linked and **20** process-only, **93** distinct direct original B01-T data→SR research edges, **35** proposed internal producer references, **38** R03 process/transform specs with **47** directed acyclic direct output→input T graph edges. C02 materializes 528 typed NODE /1323 EDGE rows. None certifies real source data, generated LP, tooling or method authority.

## 3. Full typed methodological lineage

Methodology SourceClause(version,authority,scope) → Requirement(MA01-SR immutable) → ProcessStep(P00–P17) → DataDefinition / DataInstance and TransformationSpec / TransformExecution → MathematicalObligation(M01–M18) → Model/solver RawResult → DerivedMetric/SystemNeed → VerificationCase(R04-T-SR-NNN) → EvidenceRequest versus actual Evidence(E01–E08) → IndependentReview → separately authorized governance/G1.

This is a semantic dependency **graph**, not one mandatory execution pipeline. P00 has no directly linked active SR; its gate, data and T00 still require trace records. The companion [end_to_end_requirements_traceability.csv](end_to_end_requirements_traceability.csv) contains **48 requirement rows, 20 process-only data rows, 18 process anchor rows = 86 typed rows**; no process-only reference has been promoted to a new system requirement. Data and transformation links are research analyst mappings, not Owner accepted. A declared producer does not produce an actual payload until executed.

## 4. All process steps — incidence and boundaries

| P | Process | Linked SR (incidence) | Data objects | T proposals | Critical dependency |
| --- | --- | --- | --- | --- | --- |
| P00 | Source/profile release gate | 0 | 2 | 1 | MD-01 authority; no active direct SR |
| P01 | Study horizon and scenarios | 3 | 3 | 2 | 2035/2040/2050 distinct run identifiers |
| P02 | Previously selected weather-case intake | 4 | 3 | 1 | CY1–CY5 externally supplied, cross-year shared per-case w(c) |
| P03 | Temporal and market input preparation | 4 | 5 | 2 | UTC, durations Δt, conversion, MD-12 |
| P04 | 2035 starting grid/offshore | 3 | 5 | 2 | Qualified starting grid and offshore source |
| P05 | Zonal clustering | 5 | 4 | 2 | Connected, nonoverlapping partition |
| P06 | Network reduction | 6 | 10 | 3 | PTDF/LODF, N−1, KVL and reduction oracle |
| P07 | Zonal data allocation | 1 | 4 | 2 | Extensive conservation and intensive recomputation |
| P08 | Sector-coupled model construction | 6 | 10 | 2 | Typed electricity/H2, hydro, DSR roles |
| P09 | Candidate/economic preparation | 10 | 12 | 3 | Cost, discount, candidate source MD-02 |
| P10 | Real-candidate LP expansion | 8 | 4 | 2 | Nonanticipative x across CY; stage 1 |
| P11 | Residual/theoretical LP expansion | 8 | 3 | 2 | Stage 2 F_y/candidate carry MD-07 |
| P12 | Storage expansion 2040/2050 | 8 | 4 | 2 | Storage power/energy, boundary conditions |
| P13 | Paired internal dispatch | 1 | 4 | 2 | Paired frozen dispatch and source controls |
| P14 | Frozen pre-expansion H2 sensitivity | 1 | 3 | 3 | Independent pre-expansion H2 solve B01-D072 |
| P15 | Optional OPF | 1 | 3 | 2 | Three-valued guard and LF cap |
| P16 | Postprocess and needs | 4 | 5 | 4 | KPI B01-D081 formula and threshold owner |
| P17 | Independent verification/acceptance | 1 | 3 | 1 | E01–E08 actual evidence and independent reviewer |

The transform-level 47-edge DAG differs from R01 conceptual process control/dependency DAG and the separate Owner-approval graph. Eight conceptual-to-artifact gaps identified in C03 remain open; do not invent edges to fill them. P14 B01-D072 requires an independently identified **pre-expansion** H2 reference solve; P16 B01-D081 needs a Reporting Owner-approved formula/filter/threshold; P10/P11 stage carry and cost F_y remain MD-07 TBD.

## 5. Canonical scientific semantics and incompatibilities

- D1: 48 active MA01-SR and their original text/IDs only.
- D2: five **externally selected** CY1–CY5 for each Y={2035,2040,2050}; per-case weight equality **across years** w(2035,c)=w(2040,c)=w(2050,c)=w(c). No equality between distinct c is required; numeric weights and their authority are TBD. O26 25-Feb-2026 **consultation draft** described three weather cases, so retain both source claims with explicit conflicting methodology profiles; no upstream selection algorithm in scope.
- D3: fail closed for applicable mandatory obligations, with six individual-test statuses; missing evidence is not automatically demonstrated FAIL.
- D4: canonical UTC instants, [start,end) and Δt>0, dimensional MW/MWh/electricity/H2/carrier cost conversions; calendar, daylight saving and tolerance details remain MD-12 TBD. **project_decision:D4 ≠ test_depth:D4**.
- D5-A1: risk-based mathematical V1–V6/D0–D4 verification. A33/B12/C3 is research-tier proposal, not Owner risk approval. Mathematically equivalent projections may have different native algebra, and multiple optimal portfolios require set-valued or qualified observation policies.
- D6-A: one tool-independent scientific Contract and **independently developed** tool implementations; a direct A-to-B model translation is not independent implementation. Contract architecture A/B/C remains undecided.
- P15 optional OPF: unknown activation ⇒ BLOCKED; proven OFF plus non-invocation ⇒ scoped NOT_APPLICABLE; ON ⇒ LF-referenced capacity bound and actual evidence. Mandatory LF duties remain active even when P15 is OFF.

## 6. Verification and research-only evidence

C04 B01–B15 has 74 SR-family associations of which 35 DIRECT_MICRO_INVARIANT and 39 CONTEXT/PARTIAL. C04 EX-02 recorded 15/15 local positive and 15/15 local negative arithmetic/metadata checks after correcting B05 triangle LODF from 0.5 to 1.0; the 26 catalogued mutations were designed but not executed as native model mutants. C06 recorded 135/135 custom shared-harness classifications and 24/24 targeted changes across A/B/C; these are **not** native standards parsers or generated-model equivalence. All 48 R04 native test obligations remain NOT_EXECUTED, actual E04/E05 absent, no original data qualification, no two-arm C07 pilot or qualified independent human review.

## 7. Outcome and readiness

**Research-semantic structural closure is reproducible at pinned source snapshots. Scientific mathematical completeness and productive conformance are not established.** Open methodology/data/owner/physical network/oracle/KPI/architecture/independence decisions are enumerated in [cross_workstream_findings_register.csv](cross_workstream_findings_register.csv). G1 **BLOCKED**. No normative release or mandatory architecture/DSL decision.

## 8. Exact input blob provenance audited during creation

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
