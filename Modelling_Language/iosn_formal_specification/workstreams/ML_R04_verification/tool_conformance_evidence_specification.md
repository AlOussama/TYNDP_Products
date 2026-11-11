# ML-R04 — Tool-neutral Conformance Evidence Specification v0.1

**Purpose:** Define future *export and inspection interfaces* for independently developed modelling tools. **No** implementation, connector, translator, certification, or approval performed.

## 1. Evidence roles / trust boundary

Three independent actors may later contribute: (A) **implementing tool + model generator** providing native traces, (B) **evidence collector / verifier** computing contract-level assertions from raw exports, and (C) **independent qualified reviewer** adjudicating exceptions and conformance scope. The same implementing package may calculate diagnostics, but self-reported diagnostics alone are not proof. An accepted test oracle is independent of each implementation's solver and output writer.

**Evidence classes and minimum interfaces:**

|Port|Minimum evidence|Independent verifier action|Not sufficient|
|---|---|---|---|
|E01 contract + authority|Contract revision, MA01-SR/VN, decisions, variant and methodology release identity|Check approved profile IDs, applicability and MD closures|Draft SR ID alone|
|E02 input manifest|Native source file names/versions, SHA-256, owner, studies, external CY IDs/weights, UTC/Δt, units, axes|Validate referential integrity, independent unit-/time-audit|Public download URL as proof of data used|
|E03 preprocessing|Source→output ID/provenance, transformations, loss/conservation/counterfactual checks, hash per output|Repeat critical conservation checks and inspect mapping|Output CSV without lineage|
|E04 model generator|Variable/row families, stable semantic labels, index domains, bounds, coefficients/affine offsets, objective terms, tech semantics, inspection export|Reconstruct key obligations, test Nonanticipativity, KCL/KVL, stage bounds and candidates|Model text hash or constraint COUNT only|
|E05 solver execution|Solver version/build/config, termination and primal/dual status, raw values, feasible primal/dual bounds, basis or alternative optimality certificate, objective decomposition|Independently recalc primal/dual residuals, objective and admissible gap|OPTIMAL status string alone|
|E06 raw output|Unfiltered portfolio x, operations, ENS, flows, prices when applicable, dimensioned time/CY/zone keys|Reconcile to E05 and formula lineage|Only final dashboard KPI|
|E07 independent KPI|KPI formula IDs/revisions, raw inputs, Δt, weather weights, costs and filter rules, recomputed KPI|Cross-check each scoped KPI and report non-invariants under multiple optima|Identical KPI from two tools using same buggy formula|
|E08 conformance/test ledger|Feature support, each test ID, actual attempt, 6-status result, oracle/tolerance IDs, evidence hash, reviewer identity or null|Compute dimension-specific and global status with fail-closed rules|Skipped tests counted as PASS|

Physical format is not prescribed; JSON/CSV/columnar/LP/MPS/matrix-triplet exports may be used when semantically complete. For privacy, hashes/metadata may be published while original input bytes remain inside an approved secure environment—but the independent verifier must have authorised access to test those original data. Hashes are integrity evidence, not provenance or correctness on their own.

## 2. Semantic equation and variable manifest (E04)

Each emitted row family should expose:
- stable **semantic_constraint_id** (e.g. electricity_KCL; physical_branch_KVL; cap_bound; investment_shared; H2_carrier_balance; SOC_recursion; LF_candidate_allowlist; OPF_conditional_cap);
- relation to MA01-SR IDs and stage, y, CY/UTC/zone/asset index predicates, dimensional unit and sign orientation;
- row sense (=, ≤, ≥), affine term, coefficients or a directly reconstructible row-export and variable mapping;
- number of instantiated rows, omitted cases with reason, structural zero assumptions, bound provenance and any transformation from source;
- method of extracting primal values and computing residuals without using hidden native conventions.

**Not required:** identical internal variable labels, equal matrix row order, direct source-language translation or an exactly identical algebraic expression. **Required:** the contract-relevant mathematical properties must be reconstructible. A semantic label that claims KVL but points to a free market-link row is **not** sufficient.

## 3. Solver and numerical evidence (E05)

Capture model hash and dimension, objective sense, primal objective from raw output, independently reconstructed objective decomposition, solver's reported objective, normalized primal residuals by family, dual feasibility/residual if a dual certificate is used, reduced costs, complementarity, primal/dual bounds and certified relative/absolute gaps where available.

The solver may implement alternative canonicalisations; the verifier must map equality and inequality signs, variable units and objective signs before comparing. Infeasible/unbounded status without validation witness is a statement of tool execution, not necessarily a mathematically accepted proof. A failure to extract **required** evidence is reported BLOCKED or NOT_EXECUTED with reason; a specifically unsupported mandatory feature is UNSUPPORTED. Tolerance profiles are reference IDs: **numeric real tolerances TBD (MD-12/15)**. Store both native solver tolerance settings *and* independently approved acceptance thresholds; never substitute one for the other silently.

## 4. Raw results and independent KPIs (E06-E07)

All rows must have (where applicable) target_year, weather_case_id, UTC time key, duration_h, geographic ID, carrier, unit, source-object-ID, asset-ID, stage and variant. Preserve native sign conventions via an explicit transform manifest. A raw-output checksum and independent KPI execution report must allow re-running **without** entering the original model generator. Aggregation must use true weights and Δt. Investment-vector comparison is not a global conformance oracle when alternatives are optimal; expose objective, invariant KPI and portfolio-specific values separately (C07).

## 5. Execution trace and capability declarations (E08)

Capability state is separate from test status; a feature is supported only if implementation and required inspection export are operational under the exact version/feature scope. A feature list without an execution trace is neither PASS nor a legitimate N/A. For each test, record:
- source-assertion ID and actual execution date/time (UTC), attempt ID and framework revision;
- applicable + antecedent witness, capability declaration and precise lack-of-support explanation if any;
- test-level six-status, failure counterexample or blocking dependency, evidence pointers;
- oracle authority, tolerance profile/ref and reviewer identity (null if absent);
- an explicit **SYNTHETIC_FIXTURE** vs **PRODUCTIVE_RUN** scope flag.

The nonnormative machine-readable schema is in evidence.schema.json and an honestly unexecuted example in example_evidence_not_executed.json. They are **candidate transport shapes**, not accepted industry exchange standards.

## 6. Data governance, immutability and reproducibility

Evidence bundle includes all content-addressed referenced files (SHA-256 of raw bytes), deterministic manifests, endianness/locale/decimal parsing notes when relevant, reproducible transform/code versions, solver thread/seed/config and runtime/container/dependency lock, licence/access constraints, and UTC timestamp of execution. Re-run should identify intentional nondeterminism and available ranges (not false deterministic sameness). An owner-approved oracle, signoff or exception must state approval authority and date; null is mandatory until obtained.

## 7. Quality controls / non-authority

A schema-valid JSON bundle proves only shape, not truth of coefficients, solved runs, or mathematical soundness. Cross-tool agreement is a possible diagnostic, not a replacement for the source contract or independent proof. The required inspection surfaces are **future adapter interfaces**, not a demand to modify existing GenzOE, PyPSA, Antares or Sienna tools in this workstream. **G1 remains BLOCKED.**
