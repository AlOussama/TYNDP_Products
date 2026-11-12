# ML-C02 — Critical metamodel review (independent role, not institutional independent audit)

**Date:** 2026-11-12. **Review stance:** adversarial cross-check against ML-R00 source records and the stated ML-C02 objective. This critical review is authored in the **same AI work context as the design**. It is **not** a qualified external/independent-person verification and does not authorise G1, methodology or data.

## 1. Evidence considered and tested

- Checked the exact ML-R00 baseline Git SHA and source artifacts at it, including unchanged research ML-R01–R04.
- Compared R00 integrated crosswalk to independent R03 direct SR memberships: **93/93 links match**, no missing or extra direct SR-data pair.
- Recomputed 48 unique SR, 18 M, 20 LR, 87 R03 objects, 38 proposed transforms, 48 native R04 tests, 33/12/3 risk tiers and 20 process-only objects.
- Built typed graph with explicit NODE declarations, typed EDGE references and no unresolved endpoint, and checked source native tool statuses: **48 NOT_EXECUTED**.
- No native solver run, actual original datasets, owner oracle, formal semantic proof engine or human audit was performed.

## 2. Critical findings

| Finding | Severity | Review challenge | Disposition |
|---|---|---|---|
| **MC02-F01** | P0 | Same “D4” label means UTC/units in project decisions but deep equivalence test depth in R04. Without namespaces a parser may apply the wrong rule. | **Addressed in research schema:** project_decision:D4 vs test_depth:D4; upstream R04 documents not edited |
| **MC02-F02** | P0 | D2 shared weights across years can be misread as uniform equal CY weights, or O26 three cases silently overwritten. | **Addressed in concept:** no equal-CY assertion; source-vs-overlay split; numerical source still owner-TBD |
| **MC02-F03** | P0 | R03 20 process-only objects are structurally required but have zero SR edges. A naive SR-centric schema would lose them. | **Addressed structurally:** DataObject→P LINKED_TO_PROCESS; no new SR; owner allocation open |
| **MC02-F04** | P0 | “Oracle” object can exist as a placeholder and then erroneously count as accepted oracle/evidence. | **Addressed conceptually:** OWNER_ORACLE_TBD vs approved; EvidenceRequest distinct from actual Evidence; native tests remain NOT_EXECUTED |
| **MC02-F05** | P0 | Algebraic shape identity cannot be required without excluding sound, different DC/LP formulations. Equivalence may be asserted too cheaply by matching objective alone. | **Conditionally addressed:** projection, feasible-set, objective and observable checks with proof strength; actual oracle/threshold TBD |
| **MC02-F06** | P1 | Entity catalogue is large; “minimal” could be falsely equated with schema/table count, or excessive ontology roles mandated. | **Addressed by role minimality:** core and extensions; implementable as values/registry/integrated/federated views; no schema choice |
| **MC02-F07** | P1 | S1→S2 carry forward and LF/OPF internal capacity semantics are unresolved; a single mode flag can hide these. | **Explicitly open:** stage transition/eligibility and conditional guards, MD-07/08 |
| **MC02-F08** | P1 | DataObject→P declared link does not prove a consumed **instance** nor an executed transform; conflation would grant false provenance. | **Addressed:** LINKED_TO_PROCESS and research TRANSFORM nodes distinct from execution/evidence |
| **MC02-F09** | P1 | Network reduction conservation alone can pass while DC mesh/PTDF/LODF/N−1 equivalence fails. | **Addressed as research invariant:** six output families and required oracles; numerical physical benchmark remains open |
| **MC02-F10** | P1 | Multi-optimum portfolios may differ; a strict equal-x cross-tool comparison is over-restrictive, whereas “same objective” is under-restrictive. | **Addressed conditionally:** compare feasibility, projected admissible results and owner KPI semantics; portfolio-selection policy unresolved |
| **MC02-F11** | P1 | Source and approval status must not be a single phase with PASS/FAIL/NOT_APPLICABLE; draft/real-data/test/G1 states are orthogonal. | **Addressed:** explicit status dimensions, six R04 test values, G1 still BLOCKED |
| **MC02-F12** | P1 | Graph synthesis from source CSV could conceal incorrect research allocations despite perfect FK checks. | **Open for domain review:** source pair equality verified, meaning not independently adjudicated |
| **MC02-F13** | P1 | Full transform graph includes intermediate MLR03-I types that are not part of 87 B01-D definitions; silently counting them as original inventory would distort scope. | **Addressed structurally:** separate IntermediateDataType, counted outside 87 |
| **MC02-F14** | P1 | Scientific completeness must include P00 despite no active SR claim and P15 conditionality without forced PASS. | **Addressed:** P00 0 SR declared exception; conditional applicability tri-state |
| **MC02-F15** | P1 | Native-tool conformance and “two independent models” cannot be inferred from R02 A/B schema prototypes. | **Open:** future two-tool scientific pilot; architecture experiment is separate |
| **MC02-F16** | P2 | A flattened graph CSV is not itself a guaranteed formally complete ontology, theorem prover or source-policy system. | **Accepted limitation:** portability and full semantic validation are future experiments |

No design finding is closed by an external owner or qualified independent person; “addressed” means the **draft research design documents or demonstrates the distinction**, not that approved conformance has been established.

## 3. Independence, traceability and evidence critique

The materialized graph demonstrates **structural** closure. It does not establish (a) source authority, (b) full source clause interpretation, (c) generated mathematical constraint equivalence, (d) original data quality, (e) numerical tolerances, (f) produced KPI correctness or (g) organizational independent review. An accepted evidence framework must record separate scope and independence at the point of actual execution; no trusted reviewer identity is fabricated here.

**Review of falsifiability:** reference_instances_and_counterexamples.md contains targeted failures for year/CY indexing, units, time, market links, physical mesh, storage stages, conditional OPF, data provenance, planned-versus-actual evidence and multiple optimums. These are useful discriminators but are **not** a complete scientific benchmark. A model may pass every fixture while breaking an untested network or stage detail.

## 4. Verdict and handoff conditions

**RESEARCH_DESIGN_STRUCTURALLY_CLOSED_WITH_OPEN_SCIENTIFIC_ISSUES.** No second MA01-SR baseline, no new generic robustness requirement, no DSL/architecture decision, no method/data release. Essential next steps: independent domain judgement of all research crosswalk meanings; agreed source/owner status; detailed mathematical and KPI oracles; explicit versioned proofs of projection/equivalence; original data/test evidence in the later gated phase.

Preserve **G1 BLOCKED**, all 48 native R04 tests NOT_EXECUTED and ML-R00 original files/IDs unchanged.