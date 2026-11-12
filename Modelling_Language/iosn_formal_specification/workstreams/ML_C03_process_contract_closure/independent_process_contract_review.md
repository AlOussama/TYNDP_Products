# ML-C03 — Independent-Role Process Contract Review (Research Self-Review)

**Date:** 2026-11-12. **Baseline:** ML-R00 Draft PR #32 / `9162def25d22c37b1fbc38f7d80fe929425cc8d2`. **Disposition:** `STRUCTURALLY_COMPLETE_WITH_CRITICAL_OPEN_SEMANTIC_GAPS` (research only); `REAL_DATA_UNQUALIFIED`; `NATIVE_MODEL_NOT_EXECUTED`; `OWNER_APPROVAL_NOT_OBTAINED`; `G1 BLOCKED`.

## 1. Review independence and conflict-of-interest statement

This document applies an **adversarial reviewer role** to the ML-C03 outputs and checks their claims against ML-R00/R01/R03/R04 source artefacts. The same AI authoring environment created and reviewed these files. It is **not a human or organizationally independent audit, not a signed domain-owner decision, and not independent tool validation**. Reviewer's *role-based* independence is a logical separation of criteria only; mandatory later independent signoff (B01-D084 / MD-20) is still absent.

### Reviewed deliverables

- `end_to_end_process_contract.md`: each P00–P17 with inputs, identity/version, preconditions, transformation, math properties, evidence, failure, dependencies.
- `process_data_math_dependency_matrix.csv`: 93 original data–SR pair records, 20 original process-only records, 35 proposed producer records, 38 proposed T records and 18 process anchors, **204** in total.
- `transformation_semantic_obligations.md`: all 38 original R03 T proposals, with research operation type, dimensional restrictions and open oracles.
- `data_lineage_and_process_dag.md`: 47 original R03-derived proposal-graph edges, recorded provenance/controls and missing relationship types.
- `data_allocation_and_exception_register.csv`: 87 data object rows plus **21** explicit process/exception rows = **108** records.
- `model_input_output_boundary.md`: seven differentiated numerical object classes, evidence/approval control and run-type contracts.
- `data_transformation_verification_cases.md`: 18 P-specific and 20 critical falsifiable design tests plus static coverage checks.
- The present review and the integration handoff; no upstream edits permitted.

## 2. Audit objectives, method and limits

| Review axis | Question and method | Observed disposition | What it does **not** imply |
|---|---|---|---|
| Baseline identity | Check repository/commit/ML-R00 PR/branch and source paths | SOURCE_REF_CONFIRMED | Normative methodology authority |
| Inventory cardinality | Parse B01-D rows, B01-T trace count, T proposals, process IDs, 48 active SR | 87/87; 93/93; 38/38; 18/18; 48/48 | Domain owner endorsed SR allocation |
| Object link coverage | 67 directly SR-linked and 20 process-only, each source trace ID paired with same-row SR | STRUCTURAL_JOIN_PASS | All links scientifically/legally correct |
| Proposed internal producer coverage | 35 original in-scope intermediate types have at least one proposed R03 T output | PROPOSAL_COVERAGE_PASS | Producer executable or validated |
| Directed-acyclic graph | Build unique T→T edges from declared outputs/inputs and Kahn topological sort | 47/47; no syntactic cycle | Full R01 process control flow or H2 run dependencies |
| Process-vs-data dependency | Compare R01 conceptual arrows to R03 direct artifact refs | **PARTIAL / 8 gaps below** | Permission to invent new source references |
| Math/data consistency | Inspect M01–M18, P06/P09/P14/P16 obligations against the proposed lineage | SEMANTIC_RESEARCH_RECONCILIATION_ONLY | Valid generated LP or qualified network reduction |
| Test and evidence | Map R04 test IDs, V1–V6 and structural/synthetic/native claims | TEST_DESIGN_AVAILABLE; NATIVE_NOT_EXECUTED | Certification or result conformity |
| Governance | Check source release, original dataset hashes, owner approvals and reviewer signoffs | AUTHORITY_UNCONFIRMED; G1 BLOCKED | Any gate can be passed by structural PASS |

**Reproduction limit:** The structural joins and 47-edge acyclicity checks were performed in-memory on the given baseline files during drafting. No CI/workflow execution, independent manual inspection of original energy data, signed methodology release, actual LP/OPF solve, reference PTDF/LODF computation or KPI oracle execution was performed for ML-C03. Reproduction instructions are provided in the verification-cases document; this self-review is not a substituted immutable test log.

## 3. Critical adversarial findings

| Finding | Priority | Counterargument / observed evidence | Scope-preserving disposition | Owner / later evidence |
|---|---|---|---|---|
| **C03-F01** | P0 | 2026 O26 source is a consultation draft, D1–D6 research overlay. Structural formalization could mistakenly suggest adoption. | Keep `O26_DRAFT`, MethodologyProfile, SourceRelease and authority as separate fields. | Methodology Owner MD-01; later release/approval |
| **C03-F02** | P0 | 93 B01-T original Analyst research links are not 93 Owner-certified Data-SR obligations. | Tag `ORIGINAL_B01_DATA_SR_PAIR` distinct from `MLR03_...`; no new SR-012/-049. | Domain/Requirements Owner |
| **C03-F03** | P1 | P00 legitimately no direct active SR and 20 B01-D process-only; inventing SR to close a graph would alter baseline. | Keep process-only, add controlled research governance contracts only. | Scope owner / later allocation |
| **C03-F04** | P0 | P14's B01-D072 source is marked `P14_PRE_EXPANSION_BASELINE_EXTRACTION_PROPOSED`; T14-00 is not a validated baseline optimization run. | `MISSING_EXTERNAL_BASELINE_RUN_WITNESS`; block freeze claim; no P12 result substituted. | H2/Model Owner MD-10 |
| **C03-F05** | P0 | B01-D081 was treated as in-scope intermediate; scientifically it is an owner-issued filter policy. | T16-00 resolves reference only; no auto threshold or filtering. | Reporting Owner MD-04/17 |
| **C03-F06** | P0 | Stage 1/2 functional transition and cost accounting not determined; T11-01's pointers alone do not define `F_y`. | Explicitly label `STAGE_CARRY_RULE_TBD`; cannot certify second-stage numerical output. | Expansion Owner MD-07 |
| **C03-F07** | P0 | Net reduction six outputs and PTDF/LODF/N−1 are described; detailed reference, outage set and tolerances unqualified. | Graph/schema validation ≠ electrical equivalence; claim BLOCKED for numeric oracle. | Reduction/TSO Owner MD-03/13/15 |
| **C03-F08** | P0 | Candidate market links and existing physical grid have different constraint semantics. | Model type/port direction, DC controlled market-link and LF existing mesh separately. | Model/Expansion Owner MD-08/09 |
| **C03-F09** | P0 | D2 means same CY weight **vector** across three years, not equal weights for all cases; O26 profile differs. | No 0.2 defaults; all five numeric weights owner-TBD; no weather selection. | Weather Owner MD-12/18/19 |
| **C03-F10** | P1 | Physical loss, power-vs-energy, intensive spatial means and WACC cannot obey a universal sum conservation claim. | Preservation predicates depend on dimension, carrier, source/target grain and approved mapping. | Data/Economics Owners |
| **C03-F11** | P0 | P16 needs and KPI definitions/filters have no Owner-authorized formulas; raw solver objective may be mistaken for KPI. | Separate RawResult, DerivedIndicator, SystemNeed and project status; block KPI publication. | KPI/Reporting Owner MD-04/05/17 |
| **C03-F12** | P1 | P15 optional branch could be enforced by a generic transformer or used as a replacement for LF. | Explicit trigger, proof of inactive antecedent, LF capacity cap, separate output branch. | Method/Model Owner MD-08 |
| **C03-F13** | P0 | Valid solver optimum or synthetic PASS alone does not show feasible-set conformance or independent tool evidence; different optimal portfolios may be valid. | R04 V1–V6 and E01–E08 retained, numerical witnesses and independent review TBD. | Verification Owner MD-15/20 |

### 3.1 Eight specifically detected cross-layer link gaps

The following are **differences between the R01 conceptual dependency claims and the *direct* R03 T-output→T-input graph**. A missing direct graph edge need not mean a missing scientific requirement: it may be a control/precondition, an implicit subassembly, or an unmodeled data dependency. ML-C03 must not silently choose which.

| Register ref | Process-level gap | Direct artifact-graph observation | Reviewer decision |
|---|---|---|---|
| **ML-C03-E14** | R01 P01 → P02 | T02-01 reads external B01-D003 but not `P01 study_manifest`. | Mark missing explicit profile handoff; no invented P01 data link |
| **ML-C03-E15** | R01 P06 → P08 | T08-01/02 lack direct reduced-grid B01-D026–029 or reduction bundle inputs; only P07 zonal bundle arrives. | Require clarification whether network model semantics are complete and where reduced-grid params enter |
| **ML-C03-E16** | R01 P12 → P13 | T13-01 reads LF portfolio B01-D068 (P11) and direct detailed/internal-grid data, not P12 storage need. | Clarify whether P12 state is control prerequisite or should be imported; no automatic new P12→P13 feed |
| **ML-C03-E17** | R01 P12 → P14 | No direct P12 T-output; P14 needs independently generated **preexpansive H2** data. | Distinguish execution ordering from input provenance; P12 cannot become source B01-D072 |
| **ML-C03-E18** | R01 P12 → P15 | T15-01 only takes opt-in and B01-D068 from P11, no P12 contract. | Decide scope/antecedent/carry, preserving conditional P15 status |
| **ML-C03-E19** | R01 P13 → P15 | T15-01 does not read P13 internal-grid comparison/control, though P15 OPF needs internal constraints. | Explicit grid model/cap reference after Owner definition |
| **ML-C03-E20** | P17 all-in-claim versus R03 inputs | T17-01 references B01-D082, B01-D078 and review objects, not every native E04/E05/math proof as direct input. | Add typed evidence relations in later integration, not fictitious executed links |
| **ML-C03-E21** | Optional P15 → P16 | T16-01 lists B01-D077 OPF result together with mandatory raw inputs. | Condition input under opt-in=false; no automatic P16 blockage from omitted optional OPF |

**Review conclusion on these gaps:** Structural DAG `47 edges / 0 cycles` is accurate for R03, but not a valid claim that the scientific end-to-end contract is executable or fully mapped. The 8 links are not new SR, not approved corrections to R01/R03 and not replacements of existing 47 edges. All retained in exception register.

## 4. Dimension-specific scientific counterexamples

1. **Network equivalence:** A network reduction that preserves total zonal injection but produces incorrect N−1 flow after a contingency is *not* conformant; no universal full-flow equality or rating summation can be postulated without a reference oracle.
2. **Temporal:** A 1 MW interval lasting 30 minutes has 0.5 MWh energy on that interval. Using the numerical value 1 as hourly energy is dimensionally invalid. A source local DST timestamp cannot be converted by simply removing its zone tag.
3. **Spatial:** The sum of 40 EUR/MWh and 60 EUR/MWh regional prices is not a meaningful zonal price; an intensity needs an authorized aggregation denominator and underlying commodity flow/weight.
4. **Multi-CY:** Separate per-CY investment decisions can lower the objective and appear feasible but violate shared-investment nonanticipativity; forcing all 5 weights to exactly 1/5 violates D2 semantics even though the resulting vector sums to one.
5. **Market links:** A candidate new transfer with independently controllable flow must not automatically inherit Kirchhoff cycles of the existing physical AC network solely because its technology is AC.
6. **H2:** An electrical electrolyte input is not one-to-one equal to hydrogen chemical energy without an efficiency and LHV/HHV basis. A post-expansion dispatch cannot be the baseline for frozen *pre*-expansion H2.
7. **Postprocess:** Two optima with distinct candidate choices and equal validated objective can both be mathematically valid; the reporting formula must document which need interpretation and aggregated portfolio class is actually authorized.

These examples illustrate required negative oracles, not results of a qualified IoSN instance.

## 5. Approval, scope and evidence stop conditions

| Claim | Permitted ML-C03 status | Reason |
|---|---|---|
| Documentation of source counts, crosswalk structure and T graph | `PASS_RESEARCH_STRUCTURE_SELF_CHECK` | Narrow, in-memory static verification only |
| Correctness of B01 analyst-to-SR scientific meaning | `DOMAIN_CONFIRMATION_OPEN` | 93 original traces preserved, not Owner-endorsed |
| Physical reduced-grid, LP stage and coupled-model correctness | `BLOCKED_ORACLE / NOT_EXECUTED` | No qualified PTDF/LODF/solver/optimality/Owner parameters |
| Original data contract qualification | `NOT_QUALIFIED` | No real payload/hash validation |
| KPI, filter and system-needs publication | `OWNER_RULE_BLOCKED` | No finalized filter/KPI/ONDP formula authority |
| Signed independent review | `NOT_OBTAINED` | This adversarial same-AI review is explicitly not independent certification |
| Methodology/G1 acceptance | **`G1 BLOCKED`** | Owner release and independent evidence deferred by project decision |

No reviewed artefact modifies R00/R01/R02/R03/R04. Numeric tolerance, real data, SourceRelease and review signatures remain **TBD**. This is sufficient for **handoff as a nonnormative integration research input**, not for productive model validation.
