# ML-R04 — Future Multi-Tool Pilot Requirements v0.1

**State:** DESIGN_ONLY; not authorised, not started. This is independent of ML-R01/02/03 results and does not select any modelling language, adapter or tool.

## 1. Research objective and two-tool isolation

After an approved contract release and independent review gate, two implementation teams shall **independently** encode the *same* semantic source contract in Tool A and Tool B. No pipeline may compile or translate Model A to Model B as the common source of truth. The only shared specification must be the tool-neutral accepted contract, data input release and agreed test/evidence requirements. Shared code for an independent test oracle may be used only if it is independently versioned and reviewed; it must not be embedded as an unchecked implementation assumption.

Neither GenzOE, PyPSA, Antares nor Sienna is chosen or implemented by ML-R04. Candidate tools require ability to export the E01–E08 evidence surfaces; otherwise any mandatory unavailable feature is UNSUPPORTED and cannot be hidden by a favorable final number.

## 2. Pilot entry prerequisites (future gate, currently open)

|Entry criterion|Evidence owner|Current status|
|---|---|---|
|Applicable officially adopted IoSN source, effective scope, SHA256 and requirements reconciliation|Methodology / requirements owner|BLOCKED: MD-01, G1|
|D1–D6 project decisions in controlled signed ledger; resolve SR-010 three-versus-five discrepancy|Project/requirements owner|BLOCKED for normative release; ML-R04 uses declared D4 research overlay|
|Frozen external CY1–CY5 selection **per** 2035, 2040 and 2050, equal source weights, provenance|Weather/time-series data owner|BLOCKED: no actual source manifest, numerical weight policy open|
|UTC calendar/profile, Δt, units, interpolation and gaps; original data hashes|Data owner|BLOCKED: MD-11/12/18, 0/28 real input checks|
|Economics, starting grid, network reduction, stages, KPI/ONDP and storage/H2 parameter oracles|Domain owners|BLOCKED: MD-02/03/04/06/07/08/09/10/14/15/17|
|Two independent teams and separate build/release pipelines|Pilot coordinator|NOT_EXECUTED|
|Qualified, independent reviewer and versioned acceptance tolerances|Verification owner|NOT_OBTAINED|

Synthetic fixtures **may be developed and self-checked before these prerequisites**, but their success never closes the owner or G1 gates.

## 3. Required runs and evidence pipeline

### Phase P0 — Dry contract / capability verification
Identify each of 48 MA01-SR including sparse source IDs, application to stages and conditional OPF; D4 weather overlay; declare support, exact tool/build, projected test level and dependency. Run schema-/status checks on intentionally broken inputs. Deliver E01, E02, E08 and exceptions.

### Phase P1 — Small analytic fixtures (C01–C10)
Use *identical* synthetic data/manifests but **separate** model builds. For each case:
1. Tool A and B produce E03 preprocessing manifest, E04 generator projection/obligations, E05 solver outputs where applicable, E06 raw observations and E07 recomputed KPIs.
2. Independent verifier runs property assertions with a separately implemented check, not just inter-tool diff.
3. Negative mutations (e.g. CY-specific investments, KVL-free AC network, missing cut-edge, wrong ENS aggregation) **must** be detected by the designated tests; absence of detection is a test-framework finding.
4. Tests that do not involve solver calls (C09) still need capability and applicability evidence; optional OPF (C10) requires true/false conditional branches.

### Phase P2 — Owner-qualified real-data subset (not currently available)
After controlled release, choose a minimal frozen IoSN subset with all needed IDs and truly used source bytes/hashes, including distinct target-year runs, five upstream-selected CY per year and appropriate stage/variant flags. Restore exact preprocessing, comparison to domain-approved baseline, numerical tolerance profile and official output definitions. No invented RMSE/N−1/LF/OPF thresholds.

### Phase P3 — Full candidate scope / independent judgement
For each mandatory requirement compute conformance state on V1..V6, collect unavailable evidence and deviations, perform peer review and issue scoped recommendation. **No automatic certification** or G1 change from test runner success.

## 4. Comparison protocol

|Comparison unit|Mandatory invariant|Permissible difference|Escalation|
|---|---|---|---|
|Input/time mapping|Same controlled source provenance, units, CY and Δt semantics|Storage format, internal index order|Reject data claim if hash/source differs without a controlled mapping|
|Generated mathematics|Required projected feasible set, costs, nonanticipativity, KCL/KVL, storage/candidate/stage invariants|Angles vs cycle vs PTDF; slack variables; row scaling; MPS order|Trigger D4 when equivalent semantics cannot be established|
|LP numerical|Admissible primal and dual/optimality evidence, objective within approved profile|Solver algorithm, degeneracy, basis, row ordering|Rebuild equation/objective residuals independently|
|Investment portfolio|Correct candidate bounds, shared CY decisions and objective; report solution-set scope|Different *equally optimal feasible* vectors|Check invariant KPIs, portfolio-dependent ranges and optional tie-break report|
|KPIs/output|Same accepted formulas and dimensions, independently reconciled to raw results|Non-invariant, portfolio-specific quantities explicitly reported as alternatives|Investigate weighted ENS/discount and filter versions|
|Optional OPF|If executed, LF-portfolio capacity cap and separate run|OPF absent with documented false antecedent|Fail-closed when actually requested but unsupported|

Numerical comparison uses source-approved absolute/relative tolerances per unit; never a single undifferentiated relative %. For exact synthetic integers/rationals, compare against declared mathematical expected values while still recording solver floating-point residuals. If objective values agree but equations differ, do **not** declare equivalence.

## 5. Operationally testable acceptance criteria for the pilot

- All 48 SR have implemented applicability rules, owner-released oracle (if required), at least one relevant positive and targeted negative/mutation check, and a row in the final evidence ledger.
- For mandatory mathematical A-tier properties, generated constraints and independent numeric/semantic oracles are inspectable, not inferred from success of another tool.
- All applicable mandatory tests are executed; NONE remain FAIL, UNSUPPORTED, BLOCKED or NOT_EXECUTED for a full claimed scope.
- A tool may yield an explicit **partial claim** with named limitations and fail-closed status; no vague “substantially conformant” label.
- Independently calculated outputs include versioned KPI lineage, raw data and documented multiple-optimum uncertainty; no forced equality of investment vectors.
- Independent qualified review, review findings and owner approvals are actual attested records, not self-review statements or synthetic PASS.

## 6. Pilot deliverables, not produced now

Proposed future structure: frozen_contract/, released_inputs/, team_A_evidence/, team_B_evidence/, independent_oracles/, comparisons/, exceptions_and_closure/, review_and_approval/. Evidence transport follows tool_conformance_evidence_specification.md and evidence.schema.json with separate source and tool checksums.

**Non-goals:** direct M1→M2 translation, general CBA tool interoperability, production tool certification, weather-selection modelling, and modifying current pipelines. **Present decision:** NO PILOT EXECUTED, NO NORMATIVE FREIGABE, G1 BLOCKED.
