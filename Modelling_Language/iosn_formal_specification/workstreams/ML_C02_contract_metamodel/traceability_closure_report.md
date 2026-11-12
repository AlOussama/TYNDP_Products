# ML-C02 — Traceability closure and minimality verification

**Executed at research-design layer on 2026-11-12; exact source ref:** ML-R00 commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2. **Result:** PASS_STRUCTURAL_WITH_UNRESOLVED_DOMAIN_AUTHORITY. **No actual native energy model was executed.** Gate G1 remains BLOCKED.

## 1. Sources parsed and checking procedure

Input CSVs fetched at exact baseline: ML_R00_consolidation/integrated_requirement_traceability.csv, ML_R03_data_process_contracts/input_contract_catalogue.csv, ML_R03_data_process_contracts/process_transformation_matrix.csv, ML_R04_verification/requirements_verification_matrix.csv, ML_R04_verification/test_catalogue.csv. The graph generator parses CSV with quote/newline handling and generates both explicit NODE records and typed EDGE records in contract_traceability_model.csv. It rejects duplicate incompatible node types, unresolved endpoint IDs, unknown R03 transforms/data, duplicates in direct SR-data pairs, absent R04 tests and non-NOT_EXECUTED native test source statuses.

This report describes deterministic checks performed on that **source snapshot and generated graph**, not just intended checks. Original external ENTSO-E PDF hashes, data file releases, mathematical coefficients and tool execution were **not** checked or approved.

## 2. Exact structural closure

| Baseline/control | Observed | Interpretation |
|---|---:|---|
| Unique active MA01-SR | **48/48** | only provisional L2 requirement baseline, unchanged |
| Distinct process IDs in process/transformation graph | **18/18** | P00 included despite zero direct SR mapping |
| M families referenced by at least one SR | **18/18** | mathematical linkage only; not source-authorized equations |
| LR families referenced by at least one SR | **20/20** | language-capability research linkage |
| R03 data object definitions | **87/87** | original B01-D identities preserved |
| Directly linked R03 objects | **67/67** | research owner confirmation pending |
| Direct SR–data pairs | **93/93** | exact cross-check R03 catalogue vs R00 crosswalk: **0 deltas** |
| Process-only data objects | **20/20** | no new SR introduced |
| R03 transformation definitions | **38/38** | proposed, not executed; all P00–P17 covered |
| Proposed R04 native tests | **48/48** | one mapped test per SR; no orphans |
| Native tests with status NOT_EXECUTED | **48/48** | no productive conformance |
| Proposed risk tiers | **33 A / 12 B / 3 C** | risk proposal, not approved risk policy |
| SR with missing mandatory structural reference path | **0** | requires source, profile, process, LR, R04 VN and native test |
| Missing graph edge endpoints | **0** | all edges resolve to a registered NODE |
| Missing M or LR from active crosswalk references | **0** | all 18 M and 20 LR represented |

**Graph materialization size:** 528 NODE records, 1323 EDGE records. **Types:** {"DataObject":87,"EvidenceRequest":48,"GovernanceDecision":27,"IntermediateDataType":20,"LanguageCapability":20,"MathematicalObligation":18,"MethodologyProfile":1,"Oracle":48,"ProcessStep":18,"Requirement":48,"ReviewStatus":1,"SourceClause":48,"SyntheticFixture":10,"Transformation":38,"VerificationCase":96}. An EvidenceRequest and an Oracle(OWNER_TBD) are typed *planned obligations* only; **no actual Evidence object was fabricated**, and no HAS_EVIDENCE edge asserts a nonexistent productive run.

## 3. Process coverage including the P00 exception

Counts below are *incidence counts* and therefore overlap: one SR/DataObject may appear in more than one process. “Data” is based on declared_process_link, not inferred raw consumption, and “Transform” counts proposed MLR03-T specs.

| Process | Linked SR | R03 data definitions | Proposed transformations |
|---|---:|---:|---:|
| P00 | 0 | 2 | 1 |
| P01 | 3 | 3 | 2 |
| P02 | 4 | 3 | 1 |
| P03 | 4 | 5 | 2 |
| P04 | 3 | 5 | 2 |
| P05 | 5 | 4 | 2 |
| P06 | 6 | 10 | 3 |
| P07 | 1 | 4 | 2 |
| P08 | 6 | 10 | 2 |
| P09 | 10 | 12 | 3 |
| P10 | 8 | 4 | 2 |
| P11 | 8 | 3 | 2 |
| P12 | 8 | 4 | 2 |
| P13 | 1 | 4 | 2 |
| P14 | 1 | 3 | 3 |
| P15 | 1 | 3 | 2 |
| P16 | 4 | 5 | 4 |
| P17 | 1 | 3 | 1 |

**P00:** no active SR directly claims P00 in the integrated SR process column; P00 is a governance/process step with data and transformation references. This is an intentional zero-SR exception, **not** a coverage failure or reason to create SR-012/049.

## 4. The twenty R03 objects without direct SR membership

| Original data ID | Declared process |
|---|---|
| B01-D001 | P00 |
| B01-D012 | P03 |
| B01-D013 | P03 |
| B01-D019 | P05 |
| B01-D023 | P06 |
| B01-D025 | P06 |
| B01-D032 | P07 |
| B01-D036 | P08 |
| B01-D037 | P08 |
| B01-D045 | P09 |
| B01-D046 | P09 |
| B01-D060 | P10 |
| B01-D062 | P11 |
| B01-D066 | P12 |
| B01-D068 | P13 |
| B01-D070 | P13 |
| B01-D074 | P14 |
| B01-D077 | P15 |
| B01-D080 | P16 |
| B01-D085 | P17 |

These 20 remain DataObject nodes with at least one **LINKED_TO_PROCESS** edge. Their direct-SR cardinality is 0; they are not assigned to a newly minted requirement. Their producer/consumer roles remain research proposals pending domain review.

## 5. Typed edge materialization summary

| Predicate | Edge count |
|---|---:|
| APPLIES_TO | 74 |
| BLOCKED_BY | 156 |
| CONSUMES | 123 |
| DEPENDS_ON | 371 |
| DERIVED_FROM | 48 |
| HAS_ORACLE | 48 |
| INCLUDES | 38 |
| LINKED_TO_PROCESS | 87 |
| PRODUCES | 55 |
| REFINES | 63 |
| REQUIRES_CAPABILITY | 68 |
| REQUIRES_EVIDENCE | 48 |
| SCOPED_BY | 48 |
| VERIFIES | 96 |

The CSV includes source-backed, proposed and unexecuted *state labels*. A valid key reference **does not** prove a valid scientific relation. **DEPENDS_ON** SR→Transformation is recorded as **PROCESS_RELEVANCE_ONLY_NOT_DIRECT_IMPLEMENTATION** where the R00 crosswalk supplies a process-level relevant transformation list. Direct R03 SR–DataObject pairs are marked **DIRECT_SR_DATA_LINK_UNCONFIRMED**.

## 6. Closure levels deliberately NOT satisfied

| Layer | State and reason |
|---|---|
| ID / typed edge closure | **PASS_STRUCTURAL** in generated research graph |
| Scientific agreement of every SR→M/LR/Data/T mapping | **UNCONFIRMED**; crosswalk research hypotheses, no independent domain owner |
| O26 authority and D2 deviation release | **AUTHORITY_UNCONFIRMED**; historical and consultation claims do not grant adoption |
| Real D2 numeric weights and UTC full calendar policy | **TBD_OWNER**; no productive default 0.2 |
| Actual source datasets/hashes/transform executions | **NOT_QUALIFIED / NOT_EXECUTED** |
| Native generated constraint and numerical solver checks | **NOT_EXECUTED** for 48 R04 tests |
| Actual independent KPI/oracle and two-tool equivalence | **NOT_OBTAINED**; multiple-optimum handling proposed |
| Human-independent qualified audit, method/data owner approval | **NOT_OBTAINED** |
| G1 release | **BLOCKED** |

## 7. Minimality assessment

**Core candidate:** a small set of semantic roles with typed identity, applicability, quantity axes, source/revision, data+transform lineage, mathematical obligations, raw/derived outputs and evidence/status provenance. **Full view:** additional intermediate type nodes, 38 transformation specs, 48 oracle requests, specific network/hydro/H2 features and detailed V/depth/risk annotations.

Removing SourceClause/version destroys source-authority firewall; removing Axis/Quantity collapses MW/MWh and D2 weather semantics; collapsing branch and market-link destroys M05/M07; merging DataObject/DataInstance destroys provenance; omitting ProcessStep loses 20 process-only objects; merging EvidenceRequest/Evidence creates false PASS; merging governance and test state risks false G1 GO. Hence minimality is **role-based**, not a claim that this specific graph/node count is a mathematically proven minimum.

## 8. QA limit and reproducibility

Validation is on the exact fetched source CSVs and generated logical NODE/EDGE closure. **No source PDF screenshot/manual PDF authority check, owner-signed clause adoption, original physical data-file hash, data quality execution or native tool replay** was performed. A qualified independent reviewer must rerun source-grounded arithmetic, assess edge meanings, review open decisions and sign off separately. The baseline Git snapshots and all 48 planned R04 tests remain unchanged.

**Verdict:** ML-C02 logical traceability graph structurally closed for research, scientifically nonnormative and owner-dependent; **G1=BLOCKED**.