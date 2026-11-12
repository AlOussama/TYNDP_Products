# ML-C01 — Handoff to a Tool-Independent IoSN Requirements Contract Model

**Non-normative semantic handoff v0.1 · 12 November 2026.** Research source: ML-R00 PR #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2. **No architecture/DSL/solver selection, no authorized method, no data release, no owner signoff; G1=BLOCKED.**

## 1. What ML-C01 hands over

A consistent semantic **interpretation interface** for five separate later investigations: requirements/contract metamodel, process/data graph, mathematical micro-oracles, language/architecture alternatives and conformance/evidence handling. The interface must not add or rewrite the 48 active MA01-SR. The original R00 crosswalk is the frozen structural linking baseline, and all 15 INT findings remain tracked with explicit research/owner dispositions.

**Deliverable components:**
1. [canonical_semantic_vocabulary.md](canonical_semantic_vocabulary.md): original namespaces, typed objects, relationships, physical/network distinction, results.
2. [decision_semantics_D1_D6.md](decision_semantics_D1_D6.md): canonical D1–D6, explicit project D2 and D4, R04 test_depth:D4, no uniform CY default.
3. [semantic_conflict_register.csv](semantic_conflict_register.csv): each INT-01…INT-15 plus additional local conflicts, with open owner conditions.
4. [source_authority_and_applicability_semantics.md](source_authority_and_applicability_semantics.md): O26/H24/CBA4/research/illustration/TBD source meanings.
5. [status_and_applicability_ontology.md](status_and_applicability_ontology.md): product status, six tests, three-valued guard, mandatory and optional profiles.
6. [semantic_invariants_and_counterexamples.md](semantic_invariants_and_counterexamples.md): falsifiable scientific obligations without approved numerical defaults.
7. [independent_semantic_review.md](independent_semantic_review.md): adversarial **same-AI** check, explicit review of 48 SR and all 15 INT findings; never a qualified independent human audit.
8. This handoff: future schema-neutral interfaces, acceptance checks, open work.

## 2. Minimum common semantic kernel (language independent)

| Semantic class | Required fields / references | Scientific property |
|---|---|---|
| MethodologyProfile | profile_id, source_version, source_class, project_decision_refs, disputed_clause_refs, MD/CL set | Explicit O26 3 vs D2 5 conflict; source adoption separate |
| GovernanceDecision | original decision_id/namespace, issuer, effective_scope, current_status, signed_evidence_ref-or-missing | D1–D6 confirmed as project research constraints; 21 MD/CL open |
| Requirement | MA01-SR ID, exact MA01 source ref/text, conditional_kind, applicability, source links and revision | Only existing 48 active SR; not relabelled LR/M/T |
| Process | P00–P17, operation kind, trigger/mode/stage, inputs/outputs, pre/postconditions | P00 governance, P17 review, P15 optional conditional; scheduler independent |
| DataObjectDefinition / DataInstance | B01-D ID, source/producer, instance/axes/units/release/checksum-state, spatial and time crosswalk | 87 original object IDs, 67 direct and 20 process-only; true payload not assumed |
| TransformationSpec/Execution | original MLR03-T ID, type, mapping, pre/postcondition, conservation, version, actual execution ref | 38 specs but zero production execution implied |
| MathematicalObligation | M01–M18 reference, variables/sets/units, mode, exact observable property, exceptions/allowed formulations | Original physical DC mesh vs controllable NTC market link, common investment, stages |
| LanguageCapability | LR01–LR20 and alternative technical representation bindings | No normative DSL or architecture chosen |
| VerificationCase/Oracle | MA01-VN, R04-T-SR and synthetic fixture IDs (separate), V level, D depth, applicability guard, oracle-ref/status | Correct claim scope and ability to reject negative mutations |
| Evidence/Claim | assertion/fixture/tool/model/source/input/run/solver/oracle identifiers, hash-status, observations, test state, reviewer and gate | No test status escalation to source/data/math/owner/G1 approval |
| OutputDefinition/SystemNeed | formula/ref, source/version, zone/carrier/year/direction, raw-to-derived lineage and project-status type | A reported system need is not an approved project |

**Typed link closure:** each active SR may refer to one or more P/M/LR/B01-D/MLR03-T/VN/test, but different types never share a namespace or become new baseline SR. A direct data↔SR relation is semantically different from a process-mediated dependency. P00 and B01-D process-only data can be correctly present without a direct SR mapping. A future contract encoding must support unresolved/blocked references explicitly.

### 2.1 Suggested logical record, **not syntax or adopted schema**

~~~text
obligation_ref = requirement:MA01-SR-029
provisional_baseline = MA01 (unchanged; L2)
source_claim = source:O26:2026-02-25:§3.1.1 [CONSULTATION_ONLY]
project_overlay = project_decision:D2 [RESEARCH_SCOPE]
case_set = CY1..CY5, externally selected
weights = w[CY1..CY5]; same per c across Y={2035,2040,2050};
numeric_values = TBD_OWNER; no 1/5 default
scientific_obligation = math:M01 [COMMON_INVESTMENT_PER_YEAR]
process_ref = process:P10 / process:P11 / process:P12
test_design = verification_test:R04-T-SR-029
verification_axes = V3 mathematical; V4 numerical; V6 evidence
fixture_result = SYNTHETIC_ONLY (where a local fixture was checked)
native_tool_test_status = NOT_EXECUTED
source_authority = AUTHORITY_UNCONFIRMED
owner_open = MD-01/12/15/18 and any requirement-specific unresolved references
independent_signoff = NOT_OBTAINED
G1 = BLOCKED
~~~

This representation must preserve **unapproved source, open numeric parameter, execution and test status as distinct facts**. A compiler/validator is not allowed to create guessed numeric weights, fallback method clauses, new owner decisions or a fictitious signed source document.

## 3. Required invariants for any later contract syntax

**Structural acceptance (research only):**
- Exactly the original 48 active MA01-SR IDs (no SR-012/SR-049) and 48 L4 MA01-VN links; full exact crosswalk to their R04-T IDs; process IDs drawn from P00–P17.
- 18 M and 20 LR families remain identifiable; 87 B01-D types, 93 *proposed* direct pairs, 20 process-only with their non-SR disposition, and 38 versioned operations remain traceable without creating new SR.
- Every reference carries type/namespace/source revision; project_decision:D4, test_depth:D4 and D2 distinct.
- Source status can express O26 draft three-case vs D2 five-case coexistence, H24 historical context, CBA4 external scope, SCI_DERIVED, ILLUSTRATIVE and TBD.
- Applicability guards use evidenced T/F/U, and P15 NOT_APPLICABLE only with proved disabled mode; unknown never coerced to false.
- Test outcomes remain exactly six, with separate fixture, data, method, math, numerical, KPI, independent review and G1 axes.
- No hard-coded 0.2 weights, official KPI, discount rule, reduction tolerance, H2 profile or Stage-1→2 carry-forward.

**Scientific falsifiability (designed, not yet executed):** a model violating common investment, KCL/KVL, controllable market-link boundaries, stage transfer, UTC energy balance, H2 conservation, optional OPF cap or system-need-vs-project identity should produce a counterexample under an appropriate accepted oracle. Merely comparing final objectives or syntactically matching JSON is insufficient. Several tests necessarily remain BLOCKED where oracle/owner conditions are unknown.

## 4. Interface requirements for parallel research packages

| Later work | Consume from ML-C01 | Produce without making normative decisions |
|---|---|---|
| Contract/metamodel research (e.g., ML-C02) | Typed class/edge registry, namespaces, source profile, applicability and status product | Alternative representations (modular A, typed B, federated C or language-independent core) with the **same semantic instances** and loss audit |
| Process/data dependency closure | P00–P17 semantics and R03 producer classifications, 20 process-only, object→instance distinction | Typed DAG with explicit data / model / governance / verification ops, unresolved mappings and provenance |
| Math-oracle research | M01–M18, negative cases INV-01…25, current MD/CL | Reproducible *synthetic* micro-oracles, explicit intended projection/equivalence and failure mutants; no real values |
| Evidence/conformance research | Six test states, V1–V6, test_depth:D0–D4, gate/authority firewall | Independent verification record spec, status algebra and evidence bundles for a later pilot |
| Architecture A/B/C comparison | Same 48 SR, 18 P, 87 B01-D, 38 ops, 48 VN/test and status/authority cases | Measured semantic loss, native or custom parser limits, change-impact and migration results; **no winner by declaration** |

**Cross-tool boundary:** independently built models share **intent and evidence semantics**. This does not mandate a translation chain or identical solver/library. If Tool A and Tool B give different portfolios, test scientific projection, constraints, acceptable objective/other observables and multiple-optimum policy before failing. Under D5-A1, deep mathematical equivalence is triggered by risk rather than globally requiring AST identity.

## 5. Open decisions / future gates — no fictional closure

All 21 existing pending items **MD-01…20 and MA02-CL-001 stay open**. Key dependencies: authority/scope (01/20), economics (02), network reduction (03/13/15), KPI and multi-optima (04/17), offshore factor (05), storage (06), stage transfer (07), LF/OPF (08), NTC/candidates (09), H2 profile (10), real input releases (11), UTC calendaring (12), 2035 project eligibility (14 and CL-001), hydro/DSR (16), weather source and weights (18/19).

Deferred real sources, signed data manifests, accepted numerical oracles, independent human reviewer and G1 decision are **prerequisites to future productive claims**, **not** prerequisites to nonnormative research. ML-C01 has not executed native energy-tool models, original dataset qualification or a two-tool pilot. No merge or Ready-for-Review change is authorized.

## 6. Independent handoff acceptance checklist

A successor research package should reject a proposal if it (a) changes original MA01-SR content, (b) equates R04 D4 with project D4, (c) hardcodes uniform weights as official, (d) silently claims 5 CY adopted by ENTSO-E, (e) conflates physical DC with controllable NTC, (f) makes OPF unconditional or N/A without proof, (g) derives a project approval from a system need, (h) flattens source/data/model/G1 into PASS, or (i) treats AI adversarial review as an independent institutional signoff.

**Handoff status:** SEMANTIC_PROFILE_DOCUMENTED_WITH_OPEN_ISSUES; 48-SR and 15-INT research audit trace required in companion review; numeric and owner unknowns preserved; **G1=BLOCKED**.
