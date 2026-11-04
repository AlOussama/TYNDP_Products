# ADR-IOSN-ML-001 — Contract-first tool-neutral IoSN specification

- **Status:** **PROPOSED / CONDITIONAL** — not approved as a normative standard.
- **Date:** 2026-11-04.
- **Methodology authority:** O26 ENTSO-E TYNDP 2026 IoSN public consultation (25 Feb 2026); source final status unresolved.
- **Scope:** IoSN methodology to system-model contract; **not** CBA interoperability and **not** implementation of a production solver.
- **Decision owner:** To be appointed: ENTSO-E methodology authority, method domain lead, data steward, modelling-tool leads, independent verification lead.
- **Evidence used:** 02 process matrix, 03 SyRS, 04 LRC, 05/06 capability comparison, 07 architecture comparison, 08 examples, 09 testing architecture, 10 fixture PoC, 11 independent review.

## Context
O26 has both **solution-neutral outcome obligations** (data identities, outputs) and **method-specific classes** (two-stage LP; weather-weighted objective; non-anticipative investments; DC flow; zonal network reduction; LF/OPF separation). The contract must not reduce a binding class to a vague "behavior" statement nor force one product's native classes.

## Options reviewed
**L1 SysML v2:** integrated requirements/verification semantics; domain work and operational tooling burden. **L2 full custom DSL:** coherent human representation; high ownership/reimplementation risk. **L3 adapt CESM/INES/GEMS:** good tool/domain data/maths; not a complete process-method contract. **L4 single canonical registry + modular profiles:** balances source-derived requirements and specialised technology; primary risk is semantic fragmentation.

## Proposed decision
Pilot **L4 with one canonical normative IoSN contract registry** and profile modules:
1. `method_source` + `obligations`: stable requirement IDs, authority, status, applicability, derivation and change control. SysML v2/ReqIF are *interfaces/views* if warranted, not alternative normative truth.
2. `data_semantics`: typed schemas (JSON Schema 2020-12 / LinkML as candidate), units/carriers/scenario/time/space and vetted energy vocabulary; evaluate CESM reuse.
3. `process_methods`: input/preprocess/processing/postprocess signatures, parameters, mandatory method rules, state transitions and prohibited substitutions.
4. `model_obligations`: tool-neutral energy commodity semantics, and **binding math profile** for those O26 clauses that genuinely prescribe LP/DC/non-anticipativity/formulation class. Pilot GEMS and mathspec representation, but do not require them as engine architecture.
5. `output_and_kpi`: canonical need records with approved formulas and lineage.
6. `verification_and_evidence`: versioned tests, input/reference oracles, statuses and signed acceptance.

The **only normative implementer-facing interface** is a **published, signed, semantically closed version of that registry and its referenced profiles**, not a collection of mutually competing documents. Methodology PDF remains the method authority and release interpretation source; approval resolves the apparent tension between "one interface" and "many standards." No tool reads the PDF as its integration contract after formal adoption.

## Decision consequences
- **Positive:** independently constructed model internals; reuse standards; strict coverage of mandatory mathematics where needed; machine-testable requirements and output, traceable evidence.
- **Negative:** modular profiles and cross-references need validation and governance; first version needs new domain-specific extensions, even without an invented general optimisation DSL; automatic tests are necessarily partial for physics/algorithms and opaque solvers.
- **Stop condition:** cannot freeze the final normative contract while O26 source status and MD-01–MD-07 are unresolved; cannot certify two real tools from synthetic adapter fixtures.

## Requirements-specification language vs mathematical modelling language
A method/requirements/data/output/testing specification is **sufficient only for behavioral or structurally testable statements**. O26 explicitly specifies **LP model classes and mathematical constraints** [§§3.1.1,3.9–3.10], so a **bounded formal mathematical obligation profile** is also required. That does *not* mean every implementation must use an identical set of PyPSA/Antares objects, identical LP matrix scaling or the same full canonical solver formulation. Where equivalence is rigorously demonstrated and freedom allowed, different internal formulations remain permissible.

## F1–F10 explicit answers
|Question|Answer and evidence / limit|
|---|---|
|F1 Formal tool-neutral IoSN?|**Partially feasible, yes technically** for source-closed rules; complete normative source-accurate coverage **not yet demonstrated** (02, 11 R1).|
|F2 SR/constraints/tests?|All P01–P12 processes produce proposed SR-001–021; applicable mathematical constraints and tests VC-01–14 separated (03,09).|
|F3 Blueprint for multiple tools?|**As design**, if single registry, capability gates and independent model verification; not proven end-to-end (08,09).|
|F4 PyPSA, Antares, Sienna?|Plausible mapping for portions, especially PyPSA and GEMS/Antares; feature parity and actual conformance **unverified**, Sienna profile TBD (08 UC-02, 11 R3).|
|F5 Pre/model/post together?|One versioned DAG of method/data/model/output profiles and trace IDs, not a single universal equation or component library (02,04,07).|
|F6 Automatic acceptance?|Yes for schema, scenario tuple, unit and specific invariants; model implementation/physical network acceptance additionally needs execution evidence and manual checks (09,10).|
|F7 Existing technologies?|No demonstrated complete single solution; SysML v2 requirement semantics, ReqIF exchange, CESM/LinkML energy data, JSON Schema/SHACL checks, BPMN/DMN process rules, mathspec/GEMS algebra each contribute (05,06).|
|F8 New DSL required?|**Full custom DSL not justified at this stage.** A small IoSN-specific semantic profile/registry is likely necessary; falsify this with L1/L3 pilot before finalizing (07).|
|F9 Minimum shared semantics?|Identity/source, units/axes, data+transformation, carriers/ports/balance, allowed candidate classes, method/math profiles, weather probabilities, KPI meaning, verification oracles/evidence (04).|
|F10 First implementation?|UC-01 fixed published scenario manifest → independently validate two representations, then advance to signed Annex 6.3 selection reference and UC-02 real two-engine micro-LP with non-anticipativity (10,13).|

## Architectural exit criteria
A final `ACCEPTED` ADR requires all: source/version authority resolution; signed normative method decisions including MD-02/03/06; trace completeness to all applicable source obligations; formal semantics published; two **real** tool implementations with independent generated-model and result tests; source-change impact tests; cost/adoption comparison L1/L2/L3/L4; authorized independent review. Before then the decision remains `PROPOSED`.
