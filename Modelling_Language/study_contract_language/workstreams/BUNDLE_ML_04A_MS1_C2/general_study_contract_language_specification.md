# General Study Contract Language — M3 Hybrid (C2 partial research specification)
Status: NON-NORMATIVE / RESEARCH ONLY. No executing energy system model, solver, productive code generator or study-specific rule embedded in the generic language. ADR-C1-COMP-01 remains selected. Native mathspec canonical YAML and public Program are the sole mathematical authority; legacy CSNF/M0 and bounded M2 are reference/migration only.

## 1. Scope and abstract syntax
A StudyContract specifies required external observations/behaviors, not internal formulation. The full intended concept comprises StudyFrame, scoped component/port/referent and observable declarations, typed native mathematical specification, assumptions/guarantees, methods and studies, verification, governance, provenance and evidence. The executable C2 subset is described by integrated_language_metamodel.json and canonical_study_contract_schema.json; full component/port/frame adaptation and multiple methods are explicitly open.

## 2. Concrete syntax and binding
Strict outer JSON, see WS_A/contract_concrete_syntax.md and WS_B method/study schemas. The mathematical payload is an admitted versioned package with exact native canonical YAML, typed signatures, source bytes and binding context. Author mathematics in native mathspec syntax. No raw AST, arbitrary extension or separate math parser. The shared interface resolves qualified predicate/symbol/domain/method identities, exact axis order and scope. Data support must cover every required coordinate with compatible type, carrier, basis and convention. Cross-layer domain kinds must agree.

## 3. Formal semantics and modeling freedom
See formal_semantics_specification.md and WS_A detailed semantics. Quantifier order, complete nonempty domains, Bool3, data assumption holds/where and finite guard applicability are implemented in a bounded setting. Mathematical data assumptions do not establish technical behavioral guarantees. Internal state/SoC, aggregation, alternative conversion or grid formulations remain allowed subject to independently evidenced projected external obligations; finite equality is not equivalence of formulations or feasible sets. Real model conformance is NOT_PROVED.

## 4. Physical, temporal and information typing
Reuse C1 checked quantity algebra, carrier/basis and conversion registry; explicit duration, chronology, relations and time policy. MW vs MWh, kg vs kg/h, electric vs heat, LHV vs HHV and real vs nominal price types must not be conflated. The complete original R1 validations are preserved; adapter to qualified component/port, information partition and process metadata is not complete. Static admission of time/condition nodes is not proof of finite evaluator support.

## 5. Methods, data, outputs
MethodProfile binds mathematical identity, exact source, typed inputs/parameters, explicit role and ranges, probability and time weight rules, counterfactual pair context, output identity and optional ledger policy. StudyProfile pins one profile and data/case context; full multiple-profile DAG open. Generic validator is independent of study labels. Native expression intermediate vs external output partition is explicit if declared. N7 contribution table reused; finite native lineage only on supported same-support affine expressions. No implied project change authorization or external source authenticity. Legacy N2R/Engine are retained as independent reference.

## 6. Canonical and evidence
See canonical_study_contract_specification.md, canonical.py, mathematical_integration_interface.json. Strict version dispatch and fail-closed fields. Recompute native source/canonical identity, typed binding, contract reference, profile and study context; reimport recomputes receipts and rejects modifications. Verification requests are not conformance; each explicit obligation has a finite request in current integrated subset. OWNER_TBD and RESEARCH_ASSUMPTION are not promoted. Four identities separated. Documentation-only projection limited to native top-level description.

## 7. Extension and versioning
Only a demonstrated requirement may justify change; ICR-001..004 record additions. Preserve prior package behavior, pin upstream, replay original tests. controlled_mathspec_subset.yaml separates native static admission, finite execution and external extensions. No fork or redundant deletion. Historical A/B syntax and all original tests remain unchanged.

## 8. Scientific limits and readiness
See remaining_blockers.json and gate_status.json. Formal language specification is not complete; the bounded implementation and native CI are material evidence only for their declared scope. C3 full 58/116 materialization may start only after fundamental C2 blockers are closed, not by accepting this snapshot as completion.
