# ML-C08 — Integrated Data, Process and Output Contracts

**NONNORMATIVE RESEARCH.** ML-R00 Draft-PR #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2; C01–C07 exact source heads in integrated_scientific_contract_reference.md. No adopted IoSN methodology, original data qualification, model/solver execution, human-independent audit or normative contract release. G1 BLOCKED.

## 1. Distinguish logical definitions and observed instances

A SourceArtifact requires exact source release and actual inspected original-byte digest if qualified. A DataDefinition is a B01-D original research requirement for grain, attributes, time/space/scenario, unit and source lineage; a DataInstance is an actually consumed qualified payload. The 87 B01-D items are definitions, **not** 87 qualified file instances. A TransformationSpec is a versioned process/algorithm declaration, distinct from actual TransformExecution with code, input/output instance hashes, run ID and conservation/error witness. Not all 38 process operations are ETL; P00 governance, P10–P12 mathematical solve and P17 review have distinct kinds. A ModelInput/Parameter is not an endogenous variable; a generated constraint is not an analytic assertion; RawResult is not KPI; SystemNeed is not an ApprovedProject.

## 2. Reconciled inventories

- 87 original R03 B01-D data definitions; 67 directly SR-associated and **20 process-only**, covering P00 even though P00 has no active direct SR.
- 93 distinct original B01-T data–SR research links, which remain analyst mapping rather than Owner approved.
- C03 typed matrix of 204 records: **93** direct data/SR + **20** process-only + **35** proposed internal producer + **38** transformation/workflow definitions + **18** process anchors P00–P17.
- 38 R03 transformation specs and **47** distinct acyclic inferred producer-output→consumer-input T graph edges. These are not the full R01 process-control dependencies and do not establish execution. Eight conceptual/control gaps from C03 remain open.
- C03 exception register contains 108 rows (87 objects +21 exceptions); P14 B01-D072 and P16 B01-D081 are severe owner/producer authority gaps.

## 3. Original R03 transformation declarations (all 38)

This table preserves R03 source identifiers, declared input and output IDs and associated decision references at source blob b664dcc134e3d31e25f0c710ac2beb855d2e2ff8. No entry is claimed executed, qualified or owner approved.

| T ID | P | Operation classification | Declared inputs | Declared outputs | MD/Owner |
| --- | --- | --- | --- | --- | --- |
| MLR03-T00-01 | P00 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D001;B01-D002 | MLR03-I-P00-source_manifest | MD-01;MD-11 |
| MLR03-T01-01 | P01 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D003;B01-D005 | MLR03-I-P01-study_manifest | MD-01;MD-20 |
| MLR03-T01-02 | P01 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D004;MLR03-I-P00-source_manifest | MLR03-I-P01-extraction_index | MD-11 |
| MLR03-T02-01 | P02 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D006;B01-D007;B01-D008;B01-D003 | MLR03-I-P02-weather_manifest | MD-12;MD-18;MD-19 |
| MLR03-T03-01 | P03 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D013;B01-D009;B01-D010;B01-D011;B01-D012 | MLR03-I-P03-utc_time_axis | MD-12;MD-16 |
| MLR03-T03-02 | P03 | DATA_OR_SEMANTIC_TRANSFORMATION | MLR03-I-P02-weather_manifest;MLR03-I-P03-utc_time_axis;B01-D009;B01-D011;B01-D012 | MLR03-I-P03-aligned_timeseries | MD-11;MD-12 |
| MLR03-T04-01 | P04 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D014;B01-D015;B01-D016 | MLR03-I-P04-start_grid | MD-14;MA02-CL-001 |
| MLR03-T04-02 | P04 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D017;B01-D018;MLR03-I-P04-start_grid | MLR03-I-P04-offshore_reference | MD-14 |
| MLR03-T05-01 | P05 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D019;B01-D020;MLR03-I-P04-start_grid | B01-D021 | MD-13 |
| MLR03-T05-02 | P05 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D020;B01-D021 | B01-D022 | MD-13 |
| MLR03-T06-01 | P06 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D021;B01-D023;B01-D024;B01-D025 | B01-D026;B01-D027;B01-D028;B01-D086;B01-D087 | MD-03;MD-08 |
| MLR03-T06-02 | P06 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D024;B01-D026;B01-D027;B01-D028 | B01-D029 | MD-03 |
| MLR03-T06-03 | P06 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D023;B01-D024;B01-D026;B01-D027;B01-D029 | B01-D030 | MD-03;MD-13 |
| MLR03-T07-01 | P07 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D031;B01-D032;B01-D021 | B01-D033 | MD-11 |
| MLR03-T07-02 | P07 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D033;MLR03-I-P03-aligned_timeseries | B01-D034;MLR03-I-P07-zonal_market_bundle | MD-11;MD-12 |
| MLR03-T08-01 | P08 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D035;B01-D036;B01-D038;B01-D039;B01-D040;B01-D041;B01-D042;MLR03-I-P07-zonal_market_bundle | B01-D057 | MD-10;MD-16 |
| MLR03-T08-02 | P08 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D037;B01-D043;B01-D044;B01-D057 | MLR03-I-P08-storage_hydro_constraints;B01-D067 | MD-16 |
| MLR03-T09-01 | P09 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D045;B01-D046;B01-D047;B01-D048;B01-D049;B01-D050 | B01-D059;B01-D061 | MD-07;MD-09 |
| MLR03-T09-02 | P09 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D051;B01-D052;B01-D050 | MLR03-I-P09-offshore_routing | MD-05 |
| MLR03-T09-03 | P09 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D053;B01-D054;B01-D055;B01-D056 | MLR03-I-P09-economic_bundle | MD-02;MD-06 |
| MLR03-T10-01 | P10 | MODEL_WORKFLOW_OR_SOLVE | B01-D057;B01-D028;B01-D059;MLR03-I-P09-economic_bundle;MLR03-I-P02-weather_manifest | B01-D058;MLR03-I-P10-stage1_model_input | MD-07;MD-15 |
| MLR03-T10-02 | P10 | MODEL_WORKFLOW_OR_SOLVE | MLR03-I-P10-stage1_model_input | B01-D060 | MD-15 |
| MLR03-T11-01 | P11 | MODEL_WORKFLOW_OR_SOLVE | B01-D060;B01-D061 | B01-D063;MLR03-I-P11-stage2_model_input | MD-07 |
| MLR03-T11-02 | P11 | MODEL_WORKFLOW_OR_SOLVE | MLR03-I-P11-stage2_model_input;B01-D063 | B01-D062;B01-D068 | MD-07;MD-15 |
| MLR03-T12-01 | P12 | MODEL_WORKFLOW_OR_SOLVE | B01-D064;B01-D067;B01-D062;B01-D056 | B01-D065;MLR03-I-P12-storage_model_input | MD-06;MD-07 |
| MLR03-T12-02 | P12 | MODEL_WORKFLOW_OR_SOLVE | MLR03-I-P12-storage_model_input | B01-D066 | MD-06 |
| MLR03-T13-01 | P13 | MODEL_WORKFLOW_OR_SOLVE | B01-D068;B01-D014;B01-D029 | B01-D069;B01-D070;MLR03-I-P13-paired_dispatch_inputs | MD-08 |
| MLR03-T13-02 | P13 | MODEL_WORKFLOW_OR_SOLVE | MLR03-I-P13-paired_dispatch_inputs | B01-D071 | MD-04;MD-17 |
| MLR03-T14-00 | P14 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D057;B01-D040;B01-D042 | B01-D072 | MD-10 |
| MLR03-T14-01 | P14 | MODEL_WORKFLOW_OR_SOLVE | B01-D072;B01-D040;B01-D042 | B01-D073 | MD-10 |
| MLR03-T14-02 | P14 | MODEL_WORKFLOW_OR_SOLVE | B01-D073;B01-D057 | B01-D074 | MD-10 |
| MLR03-T15-01 | P15 | MODEL_WORKFLOW_OR_SOLVE | B01-D075;B01-D068 | B01-D076;MLR03-I-P15-opf_model_input | MD-08 |
| MLR03-T15-02 | P15 | MODEL_WORKFLOW_OR_SOLVE | MLR03-I-P15-opf_model_input | B01-D077 | MD-08 |
| MLR03-T16-00 | P16 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D001;B01-D002 | B01-D081 | MD-04;MD-17 |
| MLR03-T16-01 | P16 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D060;B01-D062;B01-D066;B01-D071;B01-D074;B01-D077 | MLR03-I-P16-raw_result_index;B01-D082 | MD-04;MD-17 |
| MLR03-T16-02 | P16 | DATA_OR_SEMANTIC_TRANSFORMATION | MLR03-I-P16-raw_result_index;B01-D081 | B01-D079;B01-D078 | MD-04;MD-17 |
| MLR03-T16-03 | P16 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D050;B01-D051;B01-D052;MLR03-I-P16-raw_result_index | B01-D080;MLR03-I-P16-offshore_report | MD-05;MD-04 |
| MLR03-T17-01 | P17 | DATA_OR_SEMANTIC_TRANSFORMATION | B01-D083;B01-D084;B01-D085;B01-D082;B01-D078 | MLR03-I-P17-review_evidence | MD-01;MD-15 |

## 4. Scientific interface obligations

| Boundary | Required semantics | Outstanding evidence |
|---|---|---|
| P00→P01 | Exact source authority, methodological profile/version and input freeze manifest | O26 still consultation; MD-01 and original-byte data qualification |
| P01→P02 | Separate 2035/2040/2050 study scope and five exogenously supplied CY per year, shared case-wise w(c) | Real identities/weights and external source authority TBD |
| P02→P03/P07 | UTC [start,end), Δt>0, unit/quantity semantics, carrier-specific units, conserved additive quantities; intensive recomputation | Calendar/DST, source regridding and MD-12 TBD |
| P04→P05→P06 | Starting grid identity, connected partition, physical meshed DC equations, reduction and contingency constraints | Detailed grid, PTDF/LODF/N−1 and tolerance Owner oracle TBD |
| P07→P08/P09 | Electricity/H2 coupling, hydro/DSR and asset roles, candidate lists, discount/cost basis | Sources and MD-02/MD-10 etc TBD |
| P10→P11→P12 | Stage 1 vs stage 2 candidate eligibility, once-only CAPEX, year-specific shared investment across CY, storage power/energy | MD-07 transfer F_y and stage finance TBD |
| P12→P14 | H2 series frozen from **pre-expansion** independent reference model/run (B01-D072) | Actual prior H2 solve and data/solver/E04/E06 witness absent |
| P15 | Optional ON needs LF-referenced OPF cap, OFF+non-invocation must be proven, UNKNOWN blocked | P15 activation/control and LF evidence TBD |
| P13/P16→P17 | Paired raw, independently derived formula/weights/Δt, reporting category SystemNeed versus project approval | KPI/filter B01-D081 and reporting Owner, external reviewer TBD |

## 5. Output and quality trace

A testable full path records SourceRelease→DataInstance→TransformExecution→ModelInstance→SolveAttempt→unfiltered RawResult E06→approved MetricDefinition and independently recomputed MetricEvaluation E07→SystemNeed and E08 claim/reviewer. Preserve source/hash/revision, Y/CY/UTC/space/carrier/asset identities and explicit missing reason at each boundary. No missing output is to be replaced by a fabricated numeric zero or a claimed PASS. Data QA includes exact ID/axis resolution, finite and type-valid quantities, dimensionally correct units, source-vintage equality, time coverage, versioned crosswalks and stated exceptions. Real original data remains NOT_QUALIFIED, and no productive output was generated.
