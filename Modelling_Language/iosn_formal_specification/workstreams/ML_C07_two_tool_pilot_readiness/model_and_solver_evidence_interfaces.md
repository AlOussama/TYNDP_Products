# ML-C07 — Model, Solver and Evidence Interfaces (Logical Contract)

**DESIGN_ONLY / transport-neutral / 2026-11-12 / G1 BLOCKED.** This specifies inspectable *information and provenance* required for a future two-arm pilot. It does **not** prescribe a new API, JSON schema, LP/MPS format, DSL, network adapter, storage technology or solver. Upstream basis: ML-R04 tool_conformance_evidence_specification.md; ML-C05 #44 @ 1d1bfd18e92d457b415bbad54450bd5aec10963a and ML-C03 #46 @ 212bad6811877f9b974b20a1047913c18b1ba756, pinned against ML-R00 #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2.

## 1. Evidence surfaces and producer / reviewer boundaries

| Surface | Logical exports a future arm must make available | Independent verifier must be able to do |
|---|---|---|
| **E01 Contract & authority** | Contract revision and immutable digest, 48 MA01-SR and R04 test refs, source release type and authority, D1–D6 decisions, MD/CL blocks, scope/conditional guards | Reject two runs with different or unapproved semantics; distinguish draft source from adopted methodology |
| **E02 Consumed input & source** | Actually consumed input IDs and original-byte SHA-256 when inspected; source release, case/year/time/space/carrier/unit maps, externally supplied CY weights, qualification state | Independently verify digest of readable original, UTC durations, units, spatial/asset identities, provenance; unknown original bytes remain UNKNOWN |
| **E03 Transform execution** | Process and MLR03-T identity, input/output instance IDs and observed digests, code/config revisions, parameters, split/join/aggregation/exceptions, conservation witnesses | Replay or independently check transformations; confirm input→model binding and that process-control edges are not invented data edges |
| **E04 Generated mathematics** | Actual solved model identity, native variable & equation families, index-domain predicates, coefficients, senses, offsets, bounds, objective terms, semantic trace and omissions | Reconstruct all material generated obligations, verify shared investment, stage eligibility, KCL/KVL and market links, identify missing/extra rows |
| **E05 Solver & numerical** | Solver/build/settings, model hash, status, primal vector/objective, feasible bounds, dual/certificate if claimed, raw diagnostics and residuals | Independently compute primal feasibility and objective, bound/duality evidence; separate native solver tolerances from authorised acceptance |
| **E06 Unfiltered raw result** | Model/solve attempt, per-year/CY/UTC/asset/carrier dispatch, flows, ENS, investments, prices as applicable, source signs/units, full portfolio before filtering | Reconcile E05→E06 and preserve differences between multiple valid optima |
| **E07 KPI and derived output** | Formula revision and authority, raw parent IDs, parameters (Δt, CY weight, discount, cost basis, filters), independently recomputed metric, invariance claim/proof | Recalculate only defined outputs; distinguish undefined owner KPI from numeric zero; trace published system need without implying project approval |
| **E08 Test, capability, review** | Assertion/test/attempt IDs, six statuses, applicability witness, feature probes, oracle and tolerance refs, failure cause, reviewer role, claim scope and evidence closure | Recheck complete U/X obligation universe, false N/A, missing mandatory proof, stale artifacts and unqualified signoff |

**E01–E08 are logical information surfaces.** A physical file may cover more than one surface if identities and trustworthy access remain explicit. Every surface must support an inspection path to *the model actually solved*; a manually drafted demonstration of equations or a status flag in an E08 summary is not sufficient.

## 2. Minimum common identity and typed-reference graph

Required links (cardinality logical, not a database schema):

~~~text
ContractSnapshot → RequirementRef → AssertionRevision → TestAttempt
      │                   │                           │
      ├→ SourceRelease    ├→ Process(P00..P17)/Math(M01..M18)
      ├→ DataManifest → TransformExecution → ModelInstance
      │                                            │
      └→ OracleRef ──────────────────────────────┐  └→ SolveAttempt → RawResult
                                                │                         │
TestAttempt → evidence(E01..E08) → independent verification    MetricEvaluation
      │                                                     /
      └→ StatusRecord → ClaimRecord → qualified ReviewerRecord
                                        │
                               GateDecision (separate owner)
~~~

- **Semantic identity**: MA01-SR, R04-T-SR, P, M, B01-D/MLR03-T, physical asset/line/candidate role, and common observable mapping; must survive native name changes.
- **Content identity**: digest *algorithm, observed byte stream, computed value, verifier and timestamp*; SHA-256 of original external files when qualification is claimed. Git source commit SHA is distinct from source-file SHA-256.
- **Revision identity**: source/contract, profiles, transforms, generator code, oracle, tolerance, test spec, formula, model and reviewer disposition. New versions invalidate dependent current claims, not historical records.
- **Execution identity**: preprocessing invocation, generator call, actual solver attempt, independent KPI recomputation and test attempt, all distinct; no one generic run ID for changed artifacts.
- **Authority identity**: named/verified source owner, data qualifier, independent verifier/reviewer and Gate actor. Absence is explicit null/UNKNOWN.

For two arms, the frozen semantic contract and approved/common input may be identical, but generated models, generator source, execution identities, native row/column labels, solvers and independent proof chains are intentionally distinct.

## 3. E02/E03 — source, preprocessing and time interface

Minimum E02 mapping fields: study_year (2035/2040/2050 as separate studies), external_CY_ID (CY1–CY5), source weather-selection release ID or UNKNOWN, case-indexed weight and its *authority*, UTC interval start/end and duration_hours, zone/bus/corridor/candidate source ID, network/carrier, dimensioned value, original provenance, quality/exception state. The D2 profile requires case-specific weights equal *across* study years, not equal across CY. All productive values are open; synthetic fixtures must state that their own numbers are illustrative.

E03 must preserve input/output object identity and transformation kind (extract, temporal/spatial aggregate, network reduction, energy conversion, stage mapping, solve-related, postprocess or governance). For each transformation: applied version, source-object/target mapping, coefficients where relevant, unit operation, exclusions and lost detail, uncertainty and independently testable conservation or correspondence. **Graph validity alone does not prove semantic or physical correctness.** C03's P14 B01-D072 requires a named valid independent **pre-expansion H2 baseline solve**, and P16 B01-D081 requires externally owned filtering definition; do not fill these from a downstream final portfolio or arbitrary constants.

For a time integral E = sum_t P_t × Δt_t, each P_t is in power and Δt_t in time; energy/carrier and currency conversions must be typed. If no real gap/duplicate-hour rule has been owner qualified, data claim is BLOCKED and the invalid gap is not silently interpolated.

## 4. E04 — native generated mathematical model inspection

### 4.1 Minimum row/column export

| Entity | Required attributes |
|---|---|
| ModelInstance | model digest, generation inputs digest, generator/build rev, study/CY/variant/stage scopes, solver target hash, objective sense |
| VariableFamily | stable semantic role, native column IDs, domains/indices (y, CY, t, node, line, carrier, asset, stage), endogenous/exogenous status, units, lower/upper bounds, solution reference |
| EquationFamily | semantic obligation ID, MA01-SR and M/P links, native row IDs, row count and expected index-domain predicate, omissions/zero-row evidence, sense (=, ≤, ≥), affine right-hand side, units and orientation |
| CoefficientExport | immutable native row/column references, coefficient value/unit and source transformation, sparsity, scaling, offset handling |
| ObjectiveTerm | term semantic class, associated columns/weights/Δt/discount/price basis, frequency (CAPEX once vs operational expectation), affine constant, sign and unit |
| ProjectionMap | native→canonical physical variable/index map and reverse lift where necessary; topology orientation, candidate identity, row/column elimination or scaling, proof limits |

A linear model may export MPS/LP plus a **complete** semantic map, canonical triplets plus bounds, or another inspectable representation. A stand-alone LP file without semantic row/column mapping cannot prove the correct IoSN obligation. A semantic label without coefficients/domains and a model-instance binding also cannot.

### 4.2 Critical generated obligations

- **SR-029 / nonanticipativity:** shared investment x_y across CY or scenario x_yc copies with binding equalities; capacity bounds and once-per-study investment objective; **do not** add x_2035=x_2040=x_2050.
- **SR-018 / physics:** physical AC-branch KCL and KVL via angles, PTDF or cycle, with connected graph, reference/slack, no-load/PST offset, susceptance and orientation assumptions. A KCL-only network can admit invalid cycle flow.
- **SR-035 / market links:** candidates have controllable flow and directional capacity/NTC and KCL involvement, *without* being placed in the physical KVL/cycle subspace, even if candidate technology is AC.
- **SR-019 / reduction:** contingency cases and quality references require the original detailed network; conserving a cut integral is insufficient for LODF/PTDF/N−1 acceptance.
- **SR-031/032/033:** stage candidate allowlist, valid owner-approved carry-forward policy (MD-07 pending), optional 2040/2050 storage generation; raw model code may implement a hypothetical F_y but cannot call it approved.
- **SR-007/009/034/041/042/050:** H2/electric carrier balance, pre-expansion reference H2 demand, storage SoC and hydro/DSR limitations.
- **SR-026 / P15:** if activated, generated OPF capacity constraints must be linked to LF portfolio. If OFF proven, no conditional row is mandatory for that scope. UNKNOWN guard ⇒ BLOCKED applicability on actual evaluation.

Evidence must also demonstrate **absence of forbidden coupling** (e.g. physical cycle rows containing controllable market candidates; weather-dependent investment freedom). This requires typed variable × row inspection, not only a positive list of expected row families.

## 5. E05 — solver witness versus scientific judgement

For each solver attempt, export all named inputs and model digests, native termination/primal/dual status, full primal values, reported objective, objective coefficients + offset, raw row activity and violation diagnostics, signed bound violations, duals/reduced costs if used, primal/dual objective bounds and gaps if meaningful, feasibility scaling, solver version/parameters/threads/seed and numerical condition notes. A solver's OPTIMAL label is only a claim by a program.

For a canonical LP **when an applicable primal/dual certificate exists**, the independent verifier should:
1. reconstruct Ax (or the exact mapped native row form), compare to all row senses and explicit bounds;
2. compute objective cᵀx + constant from exported coefficients independently; reconcile component cost basis and units;
3. verify dual feasibility and bound relationship under the transformed signs/senses with correct objective orientation; compute absolute/relative gap on *approved* scales;
4. record unexplained infeasibility, unboundedness, solver errors or discrepancies without conflating a failed solve with invalid formulation.

If only a primal witness exists, an instance-feasibility claim *may* be possible, but **not** global optimality. Feasibility/optimality and network reduction acceptance tolerances are pending MD-15 and relevant domain owners. Native solver tolerance settings are recorded as diagnostic observations, never auto-adopted acceptance values. Zero residual from rounded output alone is inadequate; use unrounded exports.

## 6. E06/E07 — output reconciliation

E06 keeps the full unfiltered x, dispatch, carrier flows, ENS and relevant raw values with y/CY/time/asset/candidate/stage/variant keys and sign/unit mapping. It must reconcile to an exact E05 model/solve attempt. Tool-native reporting filters must be logged separately and **cannot erase E06**.

E07 carries independent computation identity, exact formula and status, authorisation reference, real/synthetic w(c), Δt, unit basis, price year/discount/threshold versions, raw parent IDs, intermediate components and calculated value or **UNDEFINED (FORMULA_TBD)**. KPI disagreements can be:
- true arithmetic/formula/aggregation violations,
- portfolio-specific differences between alternate optima,
- unmatched source/region/candidate mappings,
- missing or inapplicable oracle, or
- numerical uncertainty requiring approved tolerance.

Do not treat any portfolio-sensitive KPI as invariant merely because optimal objective values agree. A system-need record must not be interpreted as a project-construction approval.

## 7. E08 — status and proof-chain interface

Every atomic assertion has: SR/revision, R04 test ID, target arm/build/model/input/phase, guard and false-antecedent witness if applicable, feature-support and semantic-loss record, actual attempt ID (null if unexecuted), V-layer/D-depth, oracle and tolerance revision/authority, direct evidence links, observed residual or counterexample, exact C05 disposition **PASS/FAIL/BLOCKED/UNSUPPORTED/NOT_EXECUTED/NOT_APPLICABLE**, reason and qualified review status. Preserve immutable historical TestAttempts. Research fixture successes and productive runs must never share an undifferentiated result.

A ClaimRecord enumerates the full potentially applicable universe, excluded N/A assertions with proof, current selected attempt, six-state vector, unresolved blockers, mathematical equivalence proposition with quantifiers, explicit limitations and external review/gate state. **Claim readiness BLOCKED** if necessary authority, data, oracle, review or evidence is absent, even with many structural successes.

## 8. Export sufficiency and validation

A future pilot must demonstrate: complete source→data→transform→generated model→solve→raw output→independent KPI→assertion→claim linkage; original/native and mapped data **both** inspectable; no unsupported row/constraint hidden by abstraction; actual solver instance linkage; independent source/certificate checking; versioned reproducibility; appropriate restricted original-data access.

**Current status:** logical export interfaces specified; no adapter, tool output, actual equation/solver export, original energy data, productive KPI, owner acceptance tolerance or qualified external reviewer has been validated by ML-C07. G1 BLOCKED.
