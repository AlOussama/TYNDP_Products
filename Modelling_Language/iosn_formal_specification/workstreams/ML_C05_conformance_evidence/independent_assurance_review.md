# ML-C05 — Adversarial Assurance Review and Open Findings

**2026-11-12 · NONNORMATIVE RESEARCH REVIEW · Baseline: ML-R00 commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Independence qualification — important limitation

This is an **adversarial desk review by the same AI-based authoring process** that generated the ML-C05 research package. It deliberately challenges the proposed semantics and traces known cross-workstream contradictions. It is **not** a professionally independent human or institutional review; no external reviewer identity, separate approval chain or independent signoff exists. The filename denotes the *intended assurance function and review criteria*, not an achieved independent certification.

**Review classification:** AUTHORING_SELF_REVIEW_ADVERSARIAL; INDEPENDENT_ASSURANCE_NOT_OBTAINED. No official IoSN methodology release, owner acceptance, original data qualification, mathematical two-tool evaluation, native solver run or Gate G1 approval was conducted.

## 2. Reviewed baseline and attack model

**Baseline sources inspected:** ML-R00 cross_workstream_consistency_review.md and integration_verification_report.md; ML-R02 contract_architecture_alternatives.md; ML-R03 data_provenance_and_quality_rules.md; ML-R04 verification_architecture.md, failure_and_evidence_semantics.md, tool_conformance_evidence_specification.md, risk_based_conformance_policy.md, mathematical_verification_rules.md, future_multi_tool_pilot_requirements.md, and requirements_verification_matrix.csv at the exact referenced ML-R00 commit.

**ML-C05 subjects:** unified_conformance_semantics.md, verification_layers_and_depths.md, evidence_information_model.md, applicability_and_failure_state_machine.md, conformance_claim_rules.md, tool_evidence_interface_requirements.md, verification_status_test_cases.md and future pilot handoff design. Static and conceptual review only. New status cases were **not executed** against real implementations; a cross-document consistency assertion is not a formal proof of mathematical correctness.

The threat model is an **incorrect but convincing conformance dossier**: a tool presents plausible optimal values, hides a mandatory unsupported feature, substitutes synthetic source weights, bypasses missing acceptance criteria, reclassifies optional P15, produces self-certified evidence, or merges independent status dimensions into one attractive PASS.

## 3. Findings and dispositions

| Finding | Criticality | Adversarial question or counterexample | Research handling / remaining gap | State |
|---|---|---|---|---|
| **AR-01** | P0 | Can 'D4' mean both project time/units and deep verification? R04 contains erroneous 'D4 weather' wording. | Explicit namespaced project_decision:D2 weather; project_decision:D4 time/units; test_depth:D4. Legacy R04 remains unchanged; upstream correction still needed. | MITIGATED_IN_C05, UPSTREAM_OPEN |
| **AR-02** | P0 | Does 'equal CY weights' quietly mean 0.2 per case? | Nonuniform synthetic vector and cross-year equality tests ST-19–21. Actual numeric weights and source reconciliation TBD. | MITIGATED_IN_C05, OWNER_OPEN |
| **AR-03** | P0 | Can schema PASS become evidence of adopted source authority or qualified actual data? | Eight orthogonal dimensions, E01/E02 real source-bytes + owner state. Missing actual original data remains. | BLOCKED_EXTERNAL |
| **AR-04** | P0 | Can a single PASS in a 48-test table hide mandatory failures/nonexecution? | Exact six outcomes per assertion and full vector aggregation; excluded optional scope explicit, no global single PASS. | MITIGATED_IN_C05 |
| **AR-05** | P0 | Is UNSUPPORTED incorrectly relabelled NOT_APPLICABLE? | Capability and conditional antecedent separated; ST-01/11–15/25/26. Mandatory unsupported remains visible. | MITIGATED_IN_C05 |
| **AR-06** | P0 | Can optional OPF P15 absence make LF and all network checks N/A? | Only SR-026 conditional; P15-off requires config and noninvocation evidence; SR-024 unconditional. | MITIGATED_IN_C05 |
| **AR-07** | P0 | Are missing oracle/threshold and a proven model violation given identical status? | BLOCKED for owner oracle; FAIL only for established applicable counterexample. Outstanding numeric tolerance/authority TBD. | MITIGATED_IN_C05, OWNER_OPEN |
| **AR-08** | P0 | Can solver OPTIMAL bypass independent primal/dual/objective checks? | E04/E05 reconstructible model + numeric certificate; solver-native tolerances separated. No actual solver executed. | DESIGN_ONLY |
| **AR-09** | P0 | Does a correct aggregate cut flow certify reduced electrical PTDF/LODF/N−1 equivalence? | Explicit necessary-vs-sufficient split, D4 triggers SR-017/019, detailed original grid/oracle still missing. | BLOCKED_EXTERNAL |
| **AR-10** | P0 | Can two different optimal candidate IDs be called inconsistent without mapping? | E-FEAS, E-OPT-VALUE, E-OPT-SET, E-OBS differentiated; multiple optimum fixture rejects vector identity oracle. | MITIGATED_IN_C05, UNTESTED |
| **AR-11** | P1 | Is R02 'APPROVED' an automatic next parser stage? | Lifecycle recast as technical readiness only; owner approval external and orthogonal. | MITIGATED_IN_C05 |
| **AR-12** | P0 | Does a file hash imply source authenticity, identity or qualification? | E02 original-byte evidence, E08 integrity separate from authenticity, authorised source access. No original source files qualified. | BLOCKED_EXTERNAL |
| **AR-13** | P1 | Can a status rerun silently overwrite earlier FAIL or use stale PASS after changed data? | Immutable TestAttempt history and STALE_UNTIL_RECOMPUTED; impact graph specified but no implementation. | DESIGN_ONLY |
| **AR-14** | P1 | Can two representations of a single generator masquerade as independent implementations? | Pilot requires independent teams/models, same shared semantic contract; native E04 + negative mutants per implementation. | FUTURE_PILOT |
| **AR-15** | P0 | Can self-review become qualified independent assurance by metadata? | Independent actor/credential/authority separate; current document explicitly SAME_AI_SELF_REVIEW. | REVIEW_NOT_OBTAINED |
| **AR-16** | P1 | Can missing definition of KPI/filter/discount be replaced with a plausible number? | FORMULA_TBD and BLOCKED acceptance, preserve raw E06; owner MD-02/04/17. | BLOCKED_EXTERNAL |
| **AR-17** | P1 | Does any A/B/C risk tier excuse a mandatory obligation? | Risk affects depth only; all 48 still mandatory when applicable. Tier 33/12/3 labelled PROPOSED, D4 six triggers. | MITIGATED_IN_C05 |
| **AR-18** | P1 | Does one nominal claim of 'mathematical equivalence' conceal a weaker E-OBS on one fixture? | Separate quantified E-FEAS/E-OPT-VALUE/E-OPT-SET/E-OBS, reference scope and counterclaims. Formal proofs not produced. | DESIGN_ONLY |
| **AR-19** | P0 | Can a gate transition be triggered by all technical passes with owner authority absent? | GateDecision independent, explicit rejection ST-32 and G1 remains BLOCKED. | MITIGATED_IN_C05 |
| **AR-20** | P1 | Does the 48-SR sparse numbering create orphan or invented IDs? | Matrix parsed at exact commit; 48 unique IDs, no SR-012/049, tests one-to-one, 33/12/3 verified in document-generation check. | STATIC_CHECK_PERFORMED |

The states **MITIGATED_IN_C05** and **DESIGN_ONLY** mean *the documentation contains a countermeasure*, **not** that a real tool passed an assurance test. BLOCKED_EXTERNAL and OWNER_OPEN have not been closed.

## 4. Structured negative review of the principal claims

| Asserted claim to challenge | Minimum evidence that would refute false assurance | Current observation |
|---|---|---|
| 'All 48 requirements covered' | Exact 48-ID and test crosswalk, including nonconsecutive IDs and conditional SR-026 | **STRUCTURE CHECK ONLY**: source matrix has 48 unique SR/test joins |
| 'All mandatory tests passed' | Actual attempts, scoped oracle, E04/E05/E07 and full status vector | **NOT SHOWN**: 48 actual tool tests NOT_EXECUTED |
| 'Original IoSN data verified' | Original releases/files, retrieval and measured byte SHA-256, qualified DQ tests | **NOT SHOWN**: unqualified source bytes/data |
| 'Mathematics equivalent across tools' | Both independently generated formulations, projection map and sound D4 property proof when triggered | **NOT SHOWN**: no two-tool pilot or native model |
| 'Numerically optimal' | Acceptable primal/dual/bounds and gap at approved tolerance on exact instance | **NOT SHOWN**: no solver certificates |
| 'Outputs conform to IoSN KPI' | Authorised KPI revision and independent replay on frozen raw results | **NOT SHOWN**: KPI/filter oracles unresolved |
| 'Independent assurance completed' | Qualified reviewer different from author/test implementation, dated scope and signed findings | **NOT SHOWN**: same AI authoring context |
| 'G1 ready' | Separate formal Methodology/Data/Verification/Gate decisions and closed blockers | **NOT SHOWN**: G1 BLOCKED |

A technical source-document consistency review cannot validate an assumed methodological clause. Claims must state their quantifiers and failure cases; failure to do so is a *claim eligibility defect*, not evidence that all native energy-model equations are wrong.

## 5. Audit criteria for a future independent assurance team

An independent future reviewer should:

1. **Freeze provenance:** read both pinned ML-R00 sources and final C05 Git blob IDs; compare table and references with actual 48 SR and R04 test catalogue. Confirm no upstream file changed.
2. **Review typed semantics:** verify D2 weight identity without 1/5 default; D4 namespaces; R02/R03/R04 state separation; source/authority distinction.
3. **Execute classification test suite:** ST-01–ST-32 with concrete records and malicious changes; verify all six statuses, precedence, mixed aggregation and N/A only for a proven optional antecedent.
4. **Execute negative mathematical mutants:** nonanticipativity, DC mesh/market separation, stage transition, storage/H2, energy weighting, KPI/source-time faults.
5. **Verify E04 inspectability:** check generator-produced rows/bounds against actual solver model, not illustrative row names; inspect signed coefficients and absent forbidden constraints.
6. **Verify E05 certification method:** independent residual/objective/bound reconstruction with accepted tolerance sources, distinguish unbounded/infeasible/error witness claims.
7. **Recalculate E07:** raw-preserving, independently implemented KPI formulas and multiple-optimum comparisons; reject non-invariant KPI equality claims.
8. **Test source and access:** ensure original source artifacts are exactly those consumed and that approvals are authentic; never substitute a transport schema.
9. **Check organisation independence:** implementation teams, oracle developers and reviewer must have documented separation of responsibility; self-attestation must remain visibly self-attested.
10. **Guard governance:** no algorithm may issue G1 GO or change MD/CL owner status from an evidence score or favorable synthetic benchmark.

Until real execution and external authorisation occur, each of the above is a **future review requirement**, not a completed independent audit.

## 6. Residual research risks and nondecisions

The package does **not** resolve: authoritative O26 successor and O26 3-weather versus D2 5-weather reconciliation (MD-01/18/19); original source-data releases and UTC/Δt numerical tolerances (MD-11/12); network reduction/PTDF/LODF/N−1 oracle (MD-03/13/15); economic discount and stage transfer (MD-02/07/09); H2/hydro/storage parameters (MD-06/10/16); output KPI/filter (MD-04/05/17); accepted independent reviewer and exact quantitative acceptance policy. The 21 original MD/CL are not closed or altered. ML-C05 adds only research recommendations.

**Review outcome:** CONDITIONAL_RESEARCH_SEMANTICS_COHERENT_WITH_OPEN_FINDINGS (conceptual, not scientific validation). **Independent assurance: NOT_OBTAINED. Production conformance: NOT_ASSESSED. G1: BLOCKED.**

**Reference:** ML-R00 cross_workstream_consistency_review.md INT-01–15; ML-R04 independent_verification_review.md and source verification architecture.
