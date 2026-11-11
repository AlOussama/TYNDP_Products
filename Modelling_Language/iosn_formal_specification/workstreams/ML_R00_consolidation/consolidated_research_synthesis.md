# ML-R00 — Consolidated IoSN Scientific Research: ML-R01–ML-R04

**11 November 2026. Status: RESEARCH_CONSOLIDATION_COMPLETE_WITH_OPEN_ISSUES; G1=BLOCKED; AUTHORITY_UNCONFIRMED.** All four completed research branches share BUNDLE-01R base commit \`5c13d4d63f18d30c308997cd7a01f2977fcc6b7b\`. Their **89 Git blob artifacts have been carried unchanged** into this combined research branch; original PRs #26–#29 and MA01/BUNDLE baselines remain untouched. This is *not* official methodology, data or tool certification.

## Executive synthesis

The four tasks form a logically connected, **tool-independent IoSN Requirements Contract** research framework:
- **ML-R01 / WHAT**: source-grounded methodological requirements, **18 P00–P17** process steps, **18 M01–M18** mathematical obligations, tool freedom versus scientific invariants, and 21 open owner MD/CL.
- **ML-R02 / FORMAL EXPRESSION**: **20 LR** language capabilities and comparison of **15 alternatives × 12 criteria**, modular registry and five profiles **A**, integrated typed metamodel **B**, federated-view hypothesis **C**; no architecture or formal-language decision.
- **ML-R03 / DATA & TRANSFORMATION**: **87** B01-D data objects, **93** original data/SR trace links, **38** transformation-/workflow-contract proposals on 18 processes, provenance and UTC/unit/space semantics, model inputs and raw→derived outputs. **20/87** original objects are process-only, not directly SR-linked.
- **ML-R04 / INDEPENDENT EVIDENCE DESIGN**: **48** requirement-specific verification-test proposals, V1–V6 verification axes, D0–D4 test depths, E01–E08 evidence ports, **10 synthetic reference cases** and a future *two-tool* pilot design. **No independent energy-tool model runs** performed.

The new [integrated_requirement_traceability.csv](integrated_requirement_traceability.csv) performs an exact **48-of-48** join of active MA01-SR with R01 M, R02 LR/L3/L4, R03 direct data/process transforms and R04 V/D/evidence/test IDs. The original SR-012 and SR-049 remain **absent**: weather selection was upstream, not a new algorithm requirement.

**Research evidence is not implementation evidence.** R02's 22 classified synthetic mutations per A and B, R03's 15 synthetic input tests and R04's 10 fractional-arithmetic oracles cannot establish that an IoSN optimisation model, real source payload or two independent tools satisfy the method. R01's symbolic equations likewise are not full executed formal proofs.

## Quantified integration

| Area | Coverage / result | Caveat |
|---|---:|---|
| Active provisional MA01-SR | **48/48** | single active L2 baseline; unchanged |
| MA01-MR source references | **50** | two upstream-weather-selection items excluded from implementation |
| IoSN process steps P00–P17 | **18/18** | conceptual obligations; P15 conditional |
| Mathematical families M01–M18 | **18** | some equations illustrative and parameters TBD |
| Language capability families LR01–LR20 | **20** | not a normative DSL |
| R02 capability comparison | **180 cells** | mostly generic/qualitative, not tested scientific conformance |
| R03 data contract types | **87**, 67 directly linked, 20 process-only | no real input qualification |
| R03 direct object→SR relations | **93 pairs** | not 93 approved scientific relationships |
| R03 operations | **38**, all 18 process IDs | proposals, not executed |
| R04 tests | **48**, same MA01-VN identifiers | all native tool tests NOT_EXECUTED |
| R04 risk strata | **33 A / 12 B / 3 C** | proposed scientific priority, not owner-approved |
| Original dataset validation | **0/28** | no frozen IoSN run source hashes |
| Pending MD/CL | **21/21 OPEN** | no Owner approval |
| Institutional independent review | **NOT_OBTAINED** | source reviews are same-AI adversarial passes |

Do not sum M, LR, transformations and tests into new requirements: they are **different types of traceable obligations**.

## P00–P17 cross-layer coverage

The following table is generated from the new SR join and the 38 R03 transformation proposals. *An SR may apply to multiple process steps, so per-P SR counts cannot be summed*. P00 legitimately has no directly allocated active SR even though governance is essential.

| Step | Process function | MA01-SR linked | R03 process operations | R01 M families via mapped SR |
|---|---|---:|---:|---|

| P00 | Source authority | 0 | 1 | – |
| P01 | Study-year/scenario intake | 3 | 2 | M01, M08, M12, M15 |
| P02 | External weather intake | 4 | 1 | M01, M02, M12 |
| P03 | UTC/market data alignment | 4 | 2 | M02, M12, M16 |
| P04 | 2035 starting grid/offshore | 3 | 2 | M09, M17 |
| P05 | Network clustering | 5 | 2 | M09, M10, M11 |
| P06 | Equivalent physical grid | 6 | 3 | M05, M10, M11 |
| P07 | Zonal data allocation | 1 | 2 | M12 |
| P08 | Sector-coupled system | 6 | 2 | M12, M14, M15, M16 |
| P09 | Candidates and costs | 10 | 3 | M03, M04, M05, M06, M07, M13, M17 |
| P10 | Stage-1 real-candidate LP | 8 | 2 | M01, M02, M03, M04, M05, M06, M07, M08 |
| P11 | Stage-2 residual/conceptual LP | 8 | 2 | M01, M02, M03, M04, M05, M06, M07, M08 |
| P12 | Storage expansion 2040/2050 | 8 | 2 | M01, M02, M03, M04, M05, M06, M07, M08, M13 |
| P13 | Internal-grid dispatch comparison | 1 | 2 | M18 |
| P14 | Frozen-H2 sensitivity | 1 | 3 | M18 |
| P15 | Optional OPF | 1 | 2 | M06, M18 |
| P16 | Needs and KPI postprocessing | 4 | 4 | M03, M18 |
| P17 | Independent verification | 1 | 1 | M18 |

The full nine-field assessments remain in [R01's process semantics](../ML_R01_methodology/process_semantics_P00_P17.md); data lineage is in [R03's process transformation matrix](../ML_R03_data_process_contracts/process_transformation_matrix.csv). The table is structural trace evidence, **not an execution log**.

## Shared mathematical findings

For each **separate** horizon \(y\in\{2035,2040,2050\}\), model a **single nonanticipative investment decision** \(x_y\) across five externally selected cases \(C=\{CY1,\ldots,CY5\}\) and case-specific operation \(u_{yc}\):

\[
\min_{x_y,\{u_{yc}\}}\ C_y^\mathrm{inv}(x_y)+\sum_{c\in C}w_c Q_{yc}(x_y,u_{yc}),
\quad w_c\ge0,\quad \sum_{c\in C}w_c=1.
\]

**D2 means \(w_{2035,c}=w_{2040,c}=w_{2050,c}=w_c\) for each CY, not \(w_{CY1}=\cdots=w_{CY5}\). Real numeric weights remain TBD.** O26 §3.7 instead publishes three distinct weather cases per year with year-specific weights. D2 is a **research-profile variation**, not an adopted change to the consultation methodology. No weather selection, worst-case risk objective or extra generic robustness obligation is introduced.

Existing/reduced electrical branches obey **DC physical Kirchhoff network equations**, including appropriate impedance/no-load/mesh/PST/HVDC effects and later detailed-grid equivalence review. **Expansion candidates are controllable DC *market links* with directional NTC**, even if the physical technology is AC. Candidate stages are S1 real on-/offshore LP, S2 residual-real/conceptual/theoretical LP with **unresolved stage carry-forward** and S3 storage expansion only 2040/2050. The primary LF expansion retains physical mesh laws while disabling relevant binding internal interzonal ratings; network-constrained dispatch is compared separately; an OPF expansion is **optional and LF-portfolio-capped**.

Storage, hydro, H2 and DSR require energy/carrier balances and temporal conservation. H2 transmission infrastructure is exogenous. Offshore fixed RES targets, generic theoretical route/cost inputs, and P16 needs reporting are separate. A *system need is not an approved construction project*. KPI formulas, 2035 eligibility, original detailed-grid quality/LODF/N-1, LP economics and H2/Storage parameter details remain MD/CL-TBD. Multiple optimal investment portfolios may be scientifically valid, so equal candidate vectors are not automatically the correctness criterion.

## Architecture and verification decision boundaries

R02 architecture **A (modular source registry + Input/Process/Math/Output/Verification profiles)** is a **conditional research preference** under differing lifecycle/governance assumptions, not an accepted architecture. **B (integrated typed metamodel)** and **C (federated views)** remain open. SysML v2, ReqIF, JSON/YAML/LinkML/SHACL, GEMS, CESM, INES, SiennaSchemas, mathspec and programming frameworks can cover different roles but **none is proven by this research to be a complete, normative method-to-evidence contract**. No general model-to-model translation is required: independently developed tools use the same semantic contract and must expose comparable evidence.

R04 risk-based tiers determine *proposed test depth*, not capability approval. Maintain:
- **V1 Data**, **V2 semantic**, **V3 generated mathematical**, **V4 numerical**, **V5 KPI/result**, **V6 immutable evidence/independent review** as orthogonal assessment axes;
- **D0–D4** as *test-depth labels* distinct from **project decision D4** (UTC/unit semantics);
- E01–E08 as future export surfaces;
- six scoped test outcomes: PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_EXECUTED, NOT_APPLICABLE, with optional P15 N/A only when antecedent is evidenced false.

A structural/synthetic PASS is **not** promoted into model, data-release, KPI, owner or Gate PASS. Mandatory unsupported functions and unexecuted tests prevent a scoped complete conformance claim. Different feasible optima need independently accepted observation/optimality rules, not a mandatory matching project list.

## Findings requiring explicit integration, not automatic correction

See [cross_workstream_consistency_review.md](cross_workstream_consistency_review.md) for **15 integration findings** and proposed research-level dispositions. Highest consequence:

1. **R04 weather wording**: „equal weights“ is ambiguous and sometimes suggests uniform weights across CY; **the project only decided an identical CY-weight vector across the study years**. R04's \`1/5\` and \`0.2\` illustrations cannot become productive defaults.
2. **Decision-ID drift**: Some R04 documents call five-CY weather case selection „D4“, whereas the project decision is **D2**; **D4 = UTC/units**. Distinguish \`project_decision:D4\` from \`test_depth:D4\`.
3. **Status ontology mismatch**: R02's process maturity, R03's source/data/method states and R04's per-test statuses must be combined as *separate dimensions*, not flattened to one PASS/APPROVED flag.
4. **Cross-namespace linking**: SR ↔ M ↔ LR ↔ B01-D ↔ MLR03-T ↔ VN/test now joined for 48 SR; 20 process-only data objects remain explicitly unapproved rather than fabricated as new SR.
5. **Evidence limits**: no approved detailed-grid/oracle, marketlink NTC mapping, stage-1/2 transfer, H2 baseline, weather weights, Discount or KPIs, original dataset hashes, human independent review or native two-tool model results.
6. **Historical method references**: R01's H24 §7.3.1–7.3.2 supplementation is explicitly historical, not a valid 2026-method replacement; CBA4 is approved in its **own** scope only.

The original workstream research findings overlap. Their counts should **not** be added as unique defects. Nor may drafting the integration close any of the **21** established BUNDLE-01R owner decisions or **23** original open findings.

## Readiness and next research stage

| Layer | Research status | Why not an authoritative/implementation PASS? |
|---|---|---|
| Scientific process and mathematics | **DOCUMENTED_WITH_TBD** | O26 latest research consultation, not verified adopted version; owner and numerical details remain |
| Language/contract alternatives | **EXPERIMENTS_AVAILABLE** | only custom synthetic A/B validators; no native standards parser or mathematical tool pilot |
| Data/transformation contracts | **STRUCTURALLY_TRACEABLE** | 87 original IoSN payloads/release hashes unqualified; 0/28 original tests |
| Mathematical conformance policy | **DESIGNED_NOT_EXECUTED** | no native solver equation witnesses, independent reference tool results or approved tolerances |
| Independent review / Gate G1 | **BLOCKED** | no actual independent person/organisation, owner decision or normative source acceptance |

**Recommended research continuation, not a release request:** harmonise D2/D4 labels and multi-axis status model, define a minimal semantic core covering 48 SR and all process/data/test links, harden independent synthetic micro-oracles (including counterexamples), test R02 architecture A/B/C under identical comprehensive criteria, and prepare future evidence ports for an eventual two-tool pilot. Defer normative methodology/data approvals and real pilot entry as already decided.

See [unified_contract_concept.md](unified_contract_concept.md), [research_backlog_and_gate_plan.md](research_backlog_and_gate_plan.md) and [integration_verification_report.md](integration_verification_report.md).

**Integration conclusion:** the four research streams can now be reviewed together as one **tool-neutral scientific Contract research baseline**, but not yet accepted as an official IoSN Requirements Contract. **G1 REMAINS BLOCKED.**
