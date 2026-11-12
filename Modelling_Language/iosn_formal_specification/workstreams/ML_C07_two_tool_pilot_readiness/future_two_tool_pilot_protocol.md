# ML-C07 — Future Two-Tool Pilot Protocol (Scientific Research Reference)

**State:** NONNORMATIVE / DESIGN_ONLY / NO_TWO_TOOL_RUN / NO_TOOL_SELECTION / NO_PRODUCTIVE_CONFORMANCE / G1_BLOCKED.  
**Created:** 2026-11-12. **Baseline:** ML-R00 Draft PR #32, exact commit **9162def25d22c37b1fbc38f7d80fe929425cc8d2**.  
**Repository:** AlOussama/TYNDP_Products. The ML-C07 branch starts exactly at the R00 commit; the three subsequent workstreams below are **pinned external research inputs**, not silently merged dependencies.

## 1. Verifiable research provenance

| Input | Draft PR / head SHA verified at preparation | Relevant evidence (relative to workstreams/) |
|---|---|---|
| ML-R00 | #32 / 9162def25d22c37b1fbc38f7d80fe929425cc8d2 | ML_R00_consolidation/integrated_requirement_traceability.csv; unified_contract_concept.md |
| ML-C03 | #46 / 212bad6811877f9b974b20a1047913c18b1ba756 | ML_C03_process_contract_closure/{end_to_end_process_contract.md,process_data_math_dependency_matrix.csv,handoff_to_contract_integration.md} |
| ML-C04 | #45 / 256541e763147dcb118a3a9d24ca2f52035c672e | ML_C04_scientific_benchmarks/{scientific_benchmark_catalogue.md,analytical_reference_oracles.md,benchmark_requirement_traceability.csv,mathematical_equivalence_and_degeneracy.md} |
| ML-C05 | #44 / 1d1bfd18e92d457b415bbad54450bd5aec10963a | ML_C05_conformance_evidence/{applicability_and_failure_state_machine.md,evidence_information_model.md,conformance_claim_rules.md,handoff_to_multi_tool_pilot_design.md} |
| ML-R04 | inherited in ML-R00 at #32 | ML_R04_verification/future_multi_tool_pilot_requirements.md; tool_conformance_evidence_specification.md; risk_based_conformance_policy.md |

**Trust status:** C03/C04/C05 documents are draft research findings and designs; none is normative or an executed native two-tool trial. The ML-C04 arithmetic self-check and mutation predicates are not evidence about actual tool generators. Source O26 (25 February 2026) is a consultation draft; no methodology adoption, qualified original data, approved oracle, independent institutional review or Gate G1 approval is inferred.

## 2. Objective and unit of scientific comparison

The future experiment tests whether two **independent implementations** of one frozen semantic IoSN Requirements Contract satisfy the same *scoped scientific obligations*, despite different modelling frameworks, variable layouts, formulations and solvers. A two-tool run on the same converted mathematical file is a translation experiment, **not** an independent-implementation trial.

The unit of comparison is:
- **contract profile**: methodology authority, exact 48 MA01-SR revisions and MA01-VN/R04 tests, decisions D1–D6, unresolved MD/CL, variant and guards;
- **input instance**: original bytes and authoritative provenance, identity mappings, transformation versions, study year, externally selected CY cases, UTC intervals/durations, carriers and units;
- **target implementation**: tool/model-generator/build/source commit, generated model instance and solve attempt;
- **assertion**: one SR-linked predicate in a declared input/variant scope, with V1–V6 layer, test_depth:D0–D4, accepted oracle, evidence and explicit six-state result;
- **claim**: a bounded reviewed proposition with enumeration of applicable obligations and documented exclusions; never a tool-wide badge.

For each y in {2035,2040,2050}, use a **separate** study. Five CY1–CY5 are selected externally, not by the pilot. Under the D2 research overlay the case-specific weights are shared *across* the three study years but need not be uniform *within* the five CY; their productive numeric values are TBD. Project decision D4 is UTC and units; **test_depth:D4** means deep mathematical equivalence. No new generic robustness, minimax or CVaR obligation is introduced.

## 3. Parties, independence and permitted sharing

| Role | Proposed obligation | Conflict-of-interest control |
|---|---|---|
| Methodology / Requirements Owner | Later approve the effective source release, reconciled SR and variant decisions | No automatic adoption from repository drafts |
| Data / Domain Owners | Later qualify actually consumed source bytes, original hashes, CY/time/weight rules, network, cost, H2/stage/KPI oracles | Dataset metadata is not an approval |
| Coordinator / input custodian | Publish the same immutable semantic contract, clean-room input bundle, test manifest and change-control log to both teams | Does not send A's implementation to B |
| Implementation Team A | Independently derive mathematical model and build/export E02–E06 from Tool A | Own code/generator commit and signed independence declaration |
| Implementation Team B | Independently derive mathematical model and build/export E02–E06 from Tool B | No translation, code generation, copied constraint matrix or shared implementation code from A |
| Independent oracle maintainer | Independently derive/store analytical, physical and KPI checks including negative controls | Separate provenance and reviewer; not solver or A/B output as truth |
| Evidence verifier | Reconstruct relevant invariants, residuals and KPI from raw exports; classify each assertion | Cannot equate exporter self-reports with proof |
| Qualified external reviewer / gate authority | Later review evidence, independence, deviations and limited claims; gate actor separately decides G1 | This ML-C07 author/reviewer-role self-audit is **not** an external attestation |

**Independence design:** Before implementations begin, freeze a jointly accessible specification and record each team's independently authored design, generator source digest, dependency lock, model build provenance, modelling choices and signed reuse disclosures. Shared test harness interfaces, reference semantics and data are permissible; shared executable model construction, copied equations from the other implementation, A→B translation as B's source, or a common generator invalidates the independent-arm inference. A translation experiment can be logged in a *separate* supplementary arm and must never be counted as Team B.

**Blinding:** Candidate identities and expected positive/negative outcomes may be published as contracted semantics; where feasible, reserve independent holdout mutations, metamorphic probes and outcome adjudication for the oracle/reviewer. Disclose unavoidable leakage and avoid claiming statistical independence where it is not demonstrable.

## 4. Contract and frozen fixture package

A future run is reproducible only with immutable identifiers for: ContractSnapshot, method/source and scope; active SR/test universe; process P00–P17 / M01–M18; E01–E08 specifications; original (not placeholder) source releases; transform and input hashes; 2035/2040/2050 and CY1–CY5 IDs; vector of real externally authorised CY weights; UTC start/end/interval duration in hours; dimensioned MW/MWh/H2 and monetary conventions; zone/bus/corridor/candidate crosswalks; stage and model/solver configuration; OPF flag/invocation evidence; oracle version, mathematical assumptions, allowed numeric tolerances and reviewer authority; executable environment and licence/access policy.

Scientific synthetic fixtures use their own scope_class=SYNTHETIC_FIXTURE, synthetic weights and synthetic costs; they are **not** surrogate originals. A productive run needs source_class=OWNER_QUALIFIED and exact original-byte SHA-256 computed on an observed payload. Declared hashes, filenames or URLs without original-byte inspection do not qualify data. Where sensitive data cannot leave a controlled environment, the independent reviewer must still have authorised reproducible access.

### Scientific obligations not reducible to output equality

1. **Source and transformations:** distinguish 87 R03 B01-D objects (67 directly SR-linked, 20 process-only), 38 proposed transformations over P00–P17, 47 direct transform-DAG edges and C03's 204 research typed links. Preserve procedural-versus-data dependencies and typed exceptions instead of inventing edges.
2. **Nonanticipativity and economics:** one investment portfolio per study-year across its CY, or scenario copies with demonstrably binding equalities; correct CAPEX frequency, scenario weight and time duration, objective provenance and accounting. P10→P11 carry-forward is MD-07/TBD; P12 storage only 2040/2050.
3. **Network and market:** physically retained/reduced AC branches obey DC-KCL and appropriate KVL/angle/PTDF/cycle relations, conditional PTDF/LODF/N−1 quality; controllable market-link candidates participate in nodal balance and directional NTC but are not forced into the physical mesh cycle equations. P05/P06 source-quality oracles remain open.
4. **Sector coupling:** distinct carrier units and H2 network investment exogeneity; valid storage energy/SoC; hydro and DSR non-double counting. P14 requires a named **pre-expansion H2 baseline solve** (B01-D072), not back-derived from final expansion.
5. **Modes/results:** primary LF, independently mapped P13 paired dispatch; optional P15 OPF cap only when invoked; raw E06 preserved before owner-defined P16 filtering/KPI (B01-D081 owner rule pending); a published need is not a project authorisation.
6. **Verification:** V1–V6 evidence, D0–D3 and triggered D4; separate mathematical legality, instance feasibility, proof of optimality, KPI replay and independent review.

## 5. Protocol workflow — DESIGN, NOT EXECUTION

1. **Qualify scientific design:** inventory 48/48 existing SR (never invent SR-012/-049), map all to R04-T-SR-NNN, C04 benchmark families, C03 process edges and C05 evidence surfaces. Log unresolved MD/CL, guard semantics and oracle maturity.
2. **Freeze scope:** assign immutable contract/profile, fixture, test-plan, candidate-map and acceptance-policy revision. Record owner states; for an unapproved real-data gate use STOP rather than hidden defaults.
3. **Assess capability separately:** for each proposed tool/build/feature establish functional representability and inspectability, each with probe evidence. Classify SUPPORTED, EQUIVALENT_WITH_EVIDENCE, UNSUPPORTED or NOT_ASSESSED; retain semantic loss and required equivalence proof.
4. **Build separately:** teams derive their models from the shared semantic contract, independently document interpretation and build paths. An independence audit precedes comparative inference.
5. **Generate native evidence:** E02/E03 inputs and transformations; E04 semantic row/column/bound/objective maps; E05 solver status and primal/dual/certificate data where meaningful; E06 unfiltered raw decisions; E07 independent KPI replays; E08 assertion, applicability, capability, evidence and review ledger. E01 anchors all.
6. **Verify within each arm first:** rerun dimensional/conservation checks, validate negative mutants and small analytical cases, reconstruct mathematical constraints and solver residuals **independently**; do not take Tool A as the oracle for Tool B.
7. **Compare across arms:** only after semantic input reconciliation. Evaluate E-FEAS, E-OPT-VALUE, E-OPT-SET and E-OBS as different propositions; stage/branch, time, source, candidate and objective maps must be explicit.
8. **Escalate:** D4 if network reduction, cycle/PTDF substitution, scenario replication, objective scaling, market-link physics or unexplained KPI/portfolio differences change the feasible/optimal projection. Unproved equivalence is an unresolved claim, never an assumed PASS.
9. **Classify and review:** each atomic assertion gets exactly one C05 test status with scope and cause. Aggregate only a fully enumerated universe; evidence quality, review independence, source/data authority and G1 remain orthogonal.
10. **Publish a reproducibility dossier** with both independent E01–E08 graphs, negative-control detections, failures, open issues, comparisons and limited claims, plus *explicit nonclaims*. No G1 state transition without external decision.

The future phases, applicable entry/exit conditions and stop rules are defined in pilot_entry_and_exit_criteria.md and failure_and_stop_conditions.md. This document neither starts those phases nor implies readiness to run on real data.

## 6. Hypothesis, falsification and acceptance boundary

- **H1:** both arms can implement the shared scientific obligations with native generation. Falsifier: missing mandatory equations/capabilities or insufficient inspectability.
- **H2:** accepted mathematical invariants agree despite different algebraic representations. Falsifier: a valid counterexample in projected feasible space or an unaccounted constraint/cost.
- **H3:** accepted instance-level numerical and KPI outputs can be independently reproduced. Falsifier: reconstructed row/bound/objective/certificate/metric violation under a defined oracle and authorised tolerance.
- **H4:** deviations are attributable to input, transform, semantics, optimisation, solver, degeneracy or reporting, with scope-specific test statuses. Falsifier: evidence gaps or status conflation; a legitimate research outcome may be BLOCKED.
- **H5:** independence can be audited. Falsifier: model reuse or opaque cross-tool conversion.

**Prohibited conclusion:** matching objectives or dashboards implies equivalent mathematics, or different equally optimal investment portfolios imply a failure. No tool, solver, transport, contractual syntax or architecture is selected.

## 7. Companion deliverables and current disposition

See reference_test_manifest.md, tool_capability_assessment_framework.md, model_and_solver_evidence_interfaces.md, cross_tool_comparison_rules.md, multiple_optima_and_equivalence_policy.md, pilot_execution_readiness_matrix.csv and independent_pilot_design_review.md. **Current status: protocol designed; 0 native Tool A runs, 0 native Tool B runs, 0 qualified real-source releases, 0 accepted productive tolerances, 0 independent institutional approvals; G1 BLOCKED.**
