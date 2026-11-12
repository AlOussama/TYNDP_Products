# ML-C04 — Handoff to Contract Architecture and Conformance Design

**Research handoff, NOT an architecture decision, NOT an IoSN production schema.** Baseline is ML-R00 PR #32 SHA 9162def2. Independent of ML-C01/C02/C03/C05; no consumer should assume their findings already exist or were accepted.

## 1. Minimal tool-neutral evidence interface (conceptual)

A later contract representation, whether registry, typed metamodel or another approach, must be able to refer to these logical objects *without mandating YAML, JSON, SysML, PyPSA, Antares, Sienna or any other implementation*:

|Logical object|Required conceptual fields / relation|Why it matters|
|---|---|---|
|BenchmarkCase|stable ID Bxx, version, claim type, synthetic vs source-backed, applicable Y/CY/time, feature condition|prevent wrong source/profile promotion|
|FixtureParameter|ID, typed unit and carrier basis, value or symbolic constraint, provenance=ILLUSTRATIVE, declared parameter domain|prevent hidden price/weight/η defaults|
|ExpectedOracle|expression, assumption, projection coordinates, analytical/symbolic proof or reference values, oracle authority, result range|compare meaning rather than solver algebra|
|NegativeMutation|MUT-xx, fault category, affected generated property, witness, expected detection layer, mutation execution status|verify test sensitivity, not just positive passes|
|RequirementLink|existing MA01-SR ID + M01–M18 ID, DIRECT or CONTEXT/PARTIAL, source clause, MD/CL blockers|preserve approved-ID boundary|
|GeneratedModelEvidence|tool and generator version, native variable/type/constraint inventories, coefficients/units/index crosswalk and graph orientation|D3 evidence independent of native naming|
|ResultEvidence|native run/source hash, primal solution, objective reconstruction, optional dual/certificate, feasibility residual scale, selected projection/KPI rule ID|separate V3 semantic from V4 optimality|
|ApplicabilityCapability|mandatory/conditional, feature supported?, OPF flag, justified not-applicable status, skip reason|unsupportable mandatory cannot silently pass|
|ReviewAndAuthority|independent reviewer, owner oracle status, source-method authority, data qualification, test state, gate state|synthetic PASS must not escalate G1|

These are **logical fields**, not an adopted file format or new MA01-SR. They should reference ML-R00's unified contract concept and crosswalk, not replace them.

## 2. Required conformance algorithm (research pseudocode)

~~~text
for each applicable existing MA01-SR:
    bind versioned methodology profile, source dataset, CY vector and UTC grid
    resolve synthetic / owner-authorised oracle; retain explicit absence
    determine feature mandatory vs conditional (record why OPF off)
    if required feature missing: status = UNSUPPORTED; continue
    if a required oracle or source approval is absent: status = BLOCKED; continue
    run D0/D1 semantic and provenance checks; record independent evidence
    for math obligations: generate tool-native LP and inspect D3 index/row/bound/cost families
    if risk trigger requires D4:
        prove projected E-FEAS / E-OPT scope or find falsifying witness
    run applicable D2 micro-references including at least one targeted mutant
    run native optimisation only if data/case meaningful; check V4 primal+dual+gap
    derive V5 outputs only for explicitly defined KPI formula revision
    attach V6 evidence and reviewer sign-off
do not collapse BLOCKED/FAIL/UNSUPPORTED/NOT_EXECUTED/NOT_APPLICABLE into PASS
do not promote any synthetic result to a source/model/tool-level PASS
~~~

## 3. Suggested future two-tool pilot (D6-A; planning only)

- Independently develop two native representations for *the same semantic contract inputs*; **not** one tool converting the other's LP. Candidate implementations (e.g. PyPSA/linopy and an independent Antares or Sienna implementation) are examples, **not selected tools**.
- Pilot sequence: B01/B02 (nonanticipativity/heterogeneous weights), B04/B05 (marketlink vs physical mesh; real-network Oracle later), B06 (stage transition **after** MD-07), B07/B08/B09 (storage/H2/DSR), B10 (LF/OPF conditional), B11/B12 (E-FEAS/E-OPT and degeneracy), B13/B14 (outputs/unsupported features). B15 only with owner-authorised offshore geometry/cost basis.
- Snapshot for every native tool: fixture hash, independent model builder version, generated constraint matrices or semantic IR with variable and row units, source-to-model identity mapping, solver status and V4 certificates. Use a *shared semantic test definition*, not a shared generated mathematical model.
- Retain negative cases: an end-result agreement without generated-row inspection is insufficient; different portfolios with same objective may be mathematically valid. External accepted absolute/scaled tolerances and ε-optimum policies are MD-15/TBD.

## 4. Unresolved owner/evidence dependencies (no premature release)

|Dependency|Blocked parts|Required later evidence|
|---|---|---|
|MD-01 / source authority|all source-based acceptance claims|approved methodology release and explicit O26 delta|
|MD-02, MD-04, MD-17|objective periodisation, KPI/system-need aggregation and degeneracy reporting|discount/price basis, formula and denominators, output selection/aggregation policy|
|MD-03, MD-13, MD-15|electrical equivalence, PTDF/LODF N−1, network tolerance|qualified detailed grid, mapping, calibration method, accepted numerical oracle|
|MD-06, MD-16|storage/hydro/DSR|technology and boundary/source constraints, allowable shift/inflow windows|
|MD-07, MD-09|stage transitions, marketlink and indirect NTC|source-backed transition and cost reconciliation, NTC effect mapping|
|MD-08|LF/OPF scope|accepted internal-branch eligibility, mode mapping and optional cap rule|
|MD-10|H2 coupling/frozen sensitivity|frozen preexpansion hourly source profiles and exogenous H2 capacity rules|
|MD-11, MD-12, MD-18, MD-19|input/UTC/weather|source releases, per-CY IDs, real weights, calendar/DST intervals|
|MD-05, MD-14 / MA02-CL-001|Offshore/eligibility|geography and source-factor choice, eligible base-grid project rules|

**Gate rule:** G1 remains BLOCKED. No new weather-year selection, robustness budget, official formula, accepted numerical epsilon, DSL choice, implementation architecture or productive data certification is authorised by this handoff.
