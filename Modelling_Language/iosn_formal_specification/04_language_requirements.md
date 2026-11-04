# 04 — Language Requirements Catalogue (LRC)

**Method:** each LRC item below is **derived from the previously identified SR**, not from A+/B+ concepts. LRC items describe capabilities of a specification language or composition of languages. They are **not** claims that these capabilities are already implemented.

|LRC ID|Language capability|Derived SR|Formalizable statement / capability|Verification of language feature|Caveat|
|---|---|---|---|---|---|
|LRC-01|Source and status registry|SR-001, SR-021|Official authority, version, section/paragraph and effective status are mandatory first-class references.|schema+governance review|A spec without signed source version cannot assert normativity|
|LRC-02|Typed temporal weather/scenario data|SR-003, SR-004|IDs, timezone/calendar, scenario, year, weight, source, time/space metadata and units.|schema + referential checks|Coordinate/alignment semantics need governed vocabulary|
|LRC-03|Fixed scenario-selection contract|SR-004, SR-005|Declare selected IDs, probabilities and their target horizon with exact reference source.|schema + numeric invariants|PCA/k-means algorithm needs separate annex profile|
|LRC-04|Spatial geometry / network reduction|SR-007, SR-008, SR-009|Busmap, zone, source/target topology, direction, seasonal rating, equivalent impedance and provenance.|graph / algebraic validator|Not fully reducible to type declarations|
|LRC-05|Transformation/method signatures|SR-005, SR-006, SR-009|Input/output contracts, parameters, required algorithm identity, version and allowed freedoms.|data fixtures + trace|Appropriate PCA reference needs sign-off|
|LRC-06|Tool-independent multi-carrier semantics|SR-010, SR-011|Commodities, balances, conversion efficiency, storage and connectivity with signed unit conventions.|semantic invariant tests|No automatic solver representation inferred|
|LRC-07|Mathematical obligation profiles|SR-013, SR-014, SR-015, SR-016|Conditional binding for LP class, DC-flow constraint, objective weights and non-anticipativity.|algebraic reference/microtests|Only method-prescribed equations become normative|
|LRC-08|Candidate eligibility / stage state machine|SR-011, SR-012, SR-013, SR-014|Asset class, stage, date and capacities as guarded constraints.|state tests + model audit|Partial investment ambiguity MD-04|
|LRC-09|Canonical KPI / result semantics|SR-018, SR-019|Definitions, units, horizon/location/carrier keys, provenance, aggregation expressions.|recompute reference fixtures|Precise system-needs KPI rules MD-06|
|LRC-10|Verification and acceptance objects|SR-004, SR-005, SR-019, SR-020|VC ID, preconditions, stimulus, invariant, oracle, tolerances, execution status and linked evidence.|schema + machine checks + manual review|Do not conflate executable with truly proved|
|LRC-11|Provenance / immutability|SR-001, SR-003, SR-006, SR-020|Method source revision, transformation versions, input hashes, tool build, result hash.|hash + signature/audit|External trust and authentication necessary|
|LRC-12|Process/state orchestration|SR-014, SR-017|Preconditions, outputs, ordering and separation of LF, dispatch, optional OPF.|workflow tests|BPMN represents flow, not LP math|
|LRC-13|Reference integrity and ontology|SR-001, SR-007, SR-010, SR-018|Typed references, URIs, allowed carriers and units with scope.|SHACL/LinkML validation + custom rules|Names alone are not semantically unambiguous|
|LRC-14|Alternative tool adapter capabilities|SR-010, SR-014, SR-016, SR-020|Capability declarations, obligation coverage, explicit unsupported/loss statuses.|capability gates + test|Declared support not actual proof|
|LRC-15|Change-impact dependency graph|SR-001, SR-020, SR-021|Edges from statement to requirement, semantic rule, adapter and evidence with version.|graph reachability tests|Approval lifecycle organizational|
|LRC-16|Formalization limits & manual obligations|SR-005, SR-008, SR-019, SR-021|Required human decision, reference-benchmark limit and untestable status expressed explicitly.|review + negative acceptance|No invented acceptance metrics|
|LRC-17|Configuration interoperability and profiles|SR-010, SR-016, SR-017|Versioned modules: data, method, math, output, test; validity scoped by horizon and source version.|compatibility + conformance suite|Global language version alone insufficient|

## Language partitions / what must be expressed
1. **Input:** LRC-01/02/03/11/13; structure, unit, study scenario, time/space, provenance, validity and referential integrity.
2. **Preprocessing:** LRC-04/05/12; typed transform, method/parameter closure, input/output mapping, conservation evidence and validation gates.
3. **Energy-system semantics:** LRC-06/07/08/13; electricity/H2 conversion, balance, time- and scenario-indexed decisions, non-anticipativity and eligibility; do **not** require a named PyPSA/Antares component.
4. **Processing:** LRC-07/08/12; two-stage LP and mode/stage state machine, solver evidence without insisting on a solver supplied by the language.
5. **Postprocessing:** LRC-09/11/13; canonical results, meaning, aggregation, policy scope, reconciliation.
6. **Verification:** LRC-10/14/15/16/17; structural, semantic and implementation checks with explicit uncertainty/evidence type.

## Minimum semantic core
Stable identifiers; authority and normative source pointers; units/dimensions; quantities and periods; carrier/port/balance; type-safe transformation inputs and outputs; scenario and weather weights; method profile IDs and applicability; required/optional obligation with condition; verification oracle and evidence status; version and trace graph. Other model-specific details may live in versioned extension profiles.

## Separate layers rather than conflated file formats
- **YAML/JSON:** serialization, not complete semantics.
- **JSON Schema/LinkML:** structure, type constraints, some references; not proof of optimized behavior.
- **SHACL:** RDF graph constraints; only after well-defined graph mapping.
- **BPMN/DMN:** process/decision representation; not replacement for actual optimization obligations.
- **SysML v2/ReqIF:** systems engineering requirement/trace modelling vs ReqIF exchange.
- **GEMS/mathspec:** option for explicit math if and only if source obligation requires it.
- **Tool adapters:** interpret the spec into real model types and return testable evidence.

## Acceptance of the language itself
For any mandatory requirement, publish (i) a well-defined syntax, (ii) semantic interpretation rules including constraints/units, (iii) static and runtime validators with negative tests, (iv) a mapping from O26 section to test and evidence, and (v) a tool-independent conformance interpretation. Mark non-verifiable/partial elements rather than pretending universal automation.

## Additional LRC requirements from newly extracted O26 clauses
These requirements were added following explicit review of starting grid, offshore, marine environment, hydro/DSR and cost modeling; they are **not extrapolated from prior CBA architectures**.

|LRC ID|Capability|Derived SR|Required expression|Test|Qualification|
|---|---|---|---|---|---|
|LRC-18|Detailed resource class profiles|SR-025, SR-026, SR-033, SR-034|Hydro inflow types, storage reservoir state, hourly DFT load, explicit/implicit DSR and PEMMDB resource limits|schema + representative physical tests|External source and units need pinning|
|LRC-19|Economic and vintage-aware parameter semantics|SR-028, SR-030, SR-035|CAPEX/OPEX currency-year, WACC/discount rate, economic lifetime, staged annualization and small-expansion filtering|reference formula and dimensional tests|Broken discount reference; thresholds OPEN|
|LRC-20|Baseline and directional capacity impact semantics|SR-022, SR-027, SR-029|Distinct baseline/option identity, bidding-zone node pairs, NTC forward/backward impact, controlled market-link abstraction|project registry cross-check + LP fixture|Physical AC/DC must not be confused with market DC-link|
|LRC-21|Offshore policy and spatial cost constraints|SR-023, SR-024, SR-028, SR-036|Fixed offshore RES target, theoretical candidate technology reference, maritime routing factor, corridor distance and cost|bound checks, cost/unit tests, report provenance|10–15 percent range exact profile factor pending|

These refine all six original language domains: **Input** hydro/DFT/PEMMDB and source/period identities; **preprocessing** reference-grid eligibility and environmental length factors; **model** directional NTC market-link abstraction; **processing** stage/optional portfolio caps; **postprocessing** generic storage needs/ONDP corridors; **verification** cost and network invariants. Schema alone is insufficient for LP-level proof.
