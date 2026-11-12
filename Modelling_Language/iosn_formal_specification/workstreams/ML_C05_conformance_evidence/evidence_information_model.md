# ML-C05 — Logical Evidence Information Model (E01–E08)

**2026-11-12 · NONNORMATIVE, FORMAT-NEUTRAL · Based on ML-R00 commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Model objective and trust boundary

Represent **what is claimed, on which exact basis, demonstrated by which observations, and reviewed by whom**, without prescribing JSON, YAML, ReqIF, MPS, LP, Arrow, database tables, a particular DSL or a vendor API. The evidence model is a **logical contract for inspection and provenance**, not a mandate that every tool store or transmit objects in a common syntax.

Three producer/reviewer roles must remain distinguishable:

1. **Contract/source and data stewards** identify source and owner status, controlled version, original bytes/availability, configuration, claims and declared open decisions. Documentation of the state is possible without approving it.
2. **Implementing model/tool and evidence exporter** produce native/preprocessed model, raw solution and generated-obligation traces. A supplied hash or a self-reported solver status proves neither authenticity nor correctness.
3. **Verifier/oracle and independent qualified reviewer** independently recompute relevant assertions and adjudicate scoped claims. Same-author AI adversarial review is explicitly not an independent qualified review.

Records carry a **role and independence relation**, not merely a human-readable name. Tool A's result reused by Tool B does not become two independent oracles.

## 2. Eight evidence surfaces

| Surface | Logical entity family | Required identity / minimally inspectable payload | Independent verification action | Not proven by presence |
|---|---|---|---|---|
| **E01** Contract and authority | ContractSnapshot, RequirementRef, SourceRelease, DecisionRef, VariantProfile | Snapshot/version/hash; 48 SR IDs and MA01-VN/L4 refs; clause provenance; source class; decisions D1–D6 with project-decision namespace; effective scope; authority state; unresolved MD/CL | Detect incompatible source/profile tuples and unsupported approval assertions | O26 draft adopted; signed owner approval |
| **E02** Consumed inputs | InputManifest, SourceArtifact, DataInstance, AxisDefinition, Crosswalk, QualityObservation | Original file identity/release, *computed original-byte* SHA-256 or explicit unknown; selected 2035/2040/2050 and CY1–CY5 per year, vector w(c), UTC start/end/Δt, zone/carrier/units, actual consumed data instance IDs | Re-open/qualify authorised originals and recompute temporal/unit/integrity checks | A valid filename or source URL proves actual payload |
| **E03** Preprocessing | TransformSpecification, TransformExecution, SourceTargetLink, ConservationWitness | Input/output instance IDs + hashes, transformation/mapping/code versions, parameter status, filters and losses, execution time, provenance and test result | Replay applicable transformations or independently check conserved integrals and mappings | A conserved aggregate proves physical reduction equivalence |
| **E04** Mathematical generation | ModelInstance, EquationFamily, VariableFamily, IndexDomain, CoefficientExport, ObjectiveTerm, OmissionRecord | Model hash, generation configuration, semantic constraint/variable IDs, SR and process links, coefficient/sign/offset and units, row/column bounds, stage, CY/year/asset indices | Reconstruct mathematical obligations or falsifying counterexamples on generated matrix | Equal text/row count or claimed labels prove semantics |
| **E05** Solver and certificate | SolveAttempt, PrimalWitness, DualOrBoundWitness, ResidualReport | Solver/build/config, generation-model ref, status, raw values, objective decomposition, primal/dual bounds, gap, native and independently computed residuals, seeded/nondeterministic context | Independent primal, dual and objective computation with separate tolerances | OPTIMAL string proves optimality or correct model |
| **E06** Unfiltered raw results | RawResultBundle, ResultAxis, NativeToCanonicalMap | Instance/solve IDs, native and normalised sign/unit convention, original asset IDs, investments, dispatch, flows, ENS, relevant prices, CY/time/stage/country/carrier, digest | Compare to E05 primal and source axes; preserve all multiple-optimum solutions provided | A final aggregate KPI replaces raw decisions |
| **E07** Independent derived results | MetricDefinition, MetricEvaluation, ReconstructionWitness, FilterDecision | Formula ID/revision and authority, exact raw refs, weights/Δt, price-year/discount units and parameter versions, independent execution/provenance, output and uncertainty/invariance scope | Independently recalculate or mark FORMULA_TBD; compare only justified observables | Agreement of two dashboards proves valid KPI |
| **E08** Tests, capability, claims and review | AssertionSpec, TestAttempt, CapabilityAssessment, StatusRecord, ClaimRecord, ReviewRecord, ExceptionRecord | Exact SR/test/attempt IDs, applicability witness, six status, cause, oracle/tolerance refs, evidence graph closure, tool export support, actor independence, current/stale state, review decision | Check fail-closed rules, reject false NA/PASS, preserve immutable attempt history and gate | A suite summary can approve or certify |

E01–E08 are **information surfaces**; one logical artifact may serve several if its provenance and semantics are explicit. An E08 ledger cannot replace missing E04/E05 raw evidence by repeating a PASS field.

## 3. Logical object types and relationships

~~~text
SourceRelease ──supports_clause──> RequirementRef ──defines──> AssertionSpec
      │                                │                      │
      │                                └──constrains──> Process/VariantProfile
      └──declared_in──> ContractSnapshot ───contains─────────┘
                                  │             │
                              pins_inputs   pins_oracles
                                  │             │
SourceArtifact → DataInstance → TransformExecution → ModelInstance → SolveAttempt
                          │              │                │            │
                   ConservationWitness   EquationFamily  RawResultBundle
                                           │                  │
                                       VariableFamily     MetricEvaluation ← MetricDefinition
                                           │                  │
                      TestAttempt ──inspects/evaluates────────┘
                           │       │         │
                     EvidenceRef  OracleRef  StatusRecord
                           │
                         ClaimRecord ──reviewed_by──> ReviewRecord
                           │
                       GateDecision (EXTERNAL, not inferred from ClaimRecord)
~~~

The diagram denotes **typed links**, not single-parent ownership. E.g. a TestAttempt can inspect E02, E03, E04 and E05 together; a transform can consume many inputs and produce many outputs. No model result is permitted without a trace to its actual model instance and frozen input manifest.

### Required cardinality / closure conditions (logical proposals)

- Every **AssertionSpec** references at least one declared SR and its exact revision; every one of the 48 provisional SR has at least one test-plan link (the inherited R04 matrix has exactly one primary R04-T-SR-NNN each). Multiple further test cases may be added without minting extra SR IDs.
- Every **TestAttempt** belongs to exactly one assertion revision, target scope, execution record and evaluation configuration; it may link to many EvidenceRef records. Nonexecuted plans are represented as *planned checks* or a status record with null execution, never a fabricated run.
- Every **ModelInstance** links to a frozen InputManifest and a generation configuration. A **SolveAttempt** links to exactly one model instance; several solver attempts may target it. E06 must identify its originating attempt, not a generic tool.
- Every **MetricEvaluation** links to exactly one formula revision, its parameter/profile status and the raw-input lineage. If the formula is TBD, preserve a MetricDefinition placeholder and **no approved value**.
- Every **StatusRecord** contains one of the six outcomes and cause/evidence. NOT_APPLICABLE requires a proven antecedent false witness; PASS requires applicable scope, performed check and scoped oracle.
- Every **ClaimRecord** enumerates the universe of in-scope assertions, their current selected attempts, missing and excluded obligations, scope and non-implications; no unenumerated exclusion is allowed.
- A ReviewRecord may link to many claims; only an actually qualified external reviewer may attest independence. GateDecision is externally authored and separate from every automatic aggregate.

Missing mandatory edges are reported as **evidence closure failures**, not erased from the relationship graph.

## 4. Five noninterchangeable identity classes

| Identity class | Stability and required fields | Collision/error to prevent |
|---|---|---|
| **Semantic ID** | SR, MA01-VN/L4, process P, math obligation, source clause and typed roles; stable across implementation variants where meaning preserved | Tool-specific variable name equals a shared semantic ID without mapping |
| **Content identity** | Algorithm + digest of actual canonical/byte-level artifact; for native source files SHA-256 of actual original bytes; unknown remains null | Declared checksum of an unobserved file treated as verified data |
| **Revision identity** | Immutable contract/profile/formula/oracle/generator/test-spec/review revisions and compatible version tuple | Latest version silently substituted into an earlier result |
| **Execution identity** | Run, transform invocation, model-generation, solve attempt, KPI recalculation and test attempt with timestamps and environment | One run ID reused across multiple differing inputs or solvers |
| **Authority identity** | Verifiable source owner, independent evaluator, authorised decision actor, credential and dated scope | The tool producer marked independent merely because it signed itself |

A digest is an integrity fingerprint **conditional on verified acquisition**; it is not a certificate of document authority or method validity. Stronger authentication, signature and safe evidence custody are future owner policy decisions. A Git blob SHA for text files is distinct from SHA-256 of original third-party dataset bytes.

## 5. E04 equation-inspection information model

To avoid superficial equivalence, EquationFamily records must include at least:

- **semantic family and obligation:** e.g. electricity_KCL, physical_branch_KVL, market_link_NTC, shared_investment, H2_balance, SOC_recursion, stage_allowlist, LF_capacity_policy, optional_OPF_cap; related SRs and source clauses.
- **domain and guards:** quantified index predicates for study year/CY/time/asset/node/carrier/stage; branch mode and omitted rows/variables *with reasons*; zero-row declarations.
- **mathematics:** row orientation/sense, units, coefficients with variable mapping, affine offsets, variable bounds and objective contribution, linearisation assumptions and ref slack/angle conventions.
- **provenance:** generator build/hash, input instance and transformations feeding each coefficient and bound, relevant approved/TBD parameters.
- **inspectability:** native or reconstructible sparse matrix entries, complete index sets and ability to compute residuals independently. Identical row/column ordering is not required.

For physical AC branches, a KVL/angle/PTDF obligation must be independently reconstructible. For market candidates, **absence** of forbidden physical KVL coupling is an explicit negative obligation; exporting only active rows can miss this defect without a typed variable and cross-row trace. For nonanticipativity, both a single shared x and scenario copies constrained to equality can be valid after projection.

## 6. E05/E06/E07 replay and uncertainty

A numerical record keeps reported termination, actual primal witness, feasible bound, dual certificate or alternative justified optimality evidence **separately**. Required residuals include all native constraints/bounds, primal–dual gap when a proper certificate exists, numerical scales and native solver tolerances *distinct from* external acceptance thresholds. With no approved threshold, numeric acceptance remains BLOCKED/TBD while raw diagnostic values may still be recorded.

Raw investments, scenario×UTC dispatch and flows, ENS and source currency conventions are preserved prior to filtering. A KPI evaluator shall identify: its own executable formula revision, exact input digests, lineages, CY weights that are **not assumed uniform**, Δt, all unit conversions, formula authority and any multiple-optimum invariance claim. If the KPI is portfolio-sensitive, return a scope-dependent value or certified range rather than assert equality across alternative optima.

## 7. Evidence quality and selective disclosure

Quality dimensions are evaluated independently:

| Dimension | Proposed verifiable question |
|---|---|
| Identity/traceability | Are all references dereferenceable to a frozen artifact/version? |
| Integrity | Can the verifier recalculate the declared byte-level digests? |
| Authenticity/authority | Is source/reviewer authority externally established, not just self-asserted? |
| Completeness | Are all mandatory applicable assertions/evidence families covered? |
| Reproducibility | Can an authorised reviewer rerun or independently calculate witnesses? |
| Independence | Is the oracle/review separated from the implementation under test? |
| Relevance | Does the proof test the actual semantic property rather than a proxy only? |
| Currency | Have changed sources, mappings, formulas or thresholds invalidated old results? |

Native files may remain in a controlled environment subject to rights and access; the logical interface must still supply secure review access to an authorised verifier. Publishing hashes without disclosing bytes does not amount to independent data qualification.

## 8. Version/change impact and staleness rules

Given a changed SourceArtifact, Crosswalk, TimeProfile, FormulaDefinition, Generator or Oracle, traverse downstream dependencies. Mark affected TestAttempts/Claims **STALE_UNTIL_RECOMPUTED**, preserve previous historical claims with their original scope, and create fresh attempts for a new snapshot. A later owner approval cannot retroactively make an old unqualified source execution approved unless the exact consumed bytes, version and applicability are independently shown to match and the governing policy permits retrospective validation.

Examples requiring dependency invalidation: CY-vector change for all three years; revised time/Δt; altered KVL orientation; stage carry-forward; candidate NTC direction; KPI filter; threshold; or source methodology adoption. A formatting-only version change still needs a recorded compatibility decision, not an automatic digest substitution.

## 9. Scope of evidence exchange

A future adapter may serialise each E-surface independently, send an immutable bundle or expose a governed query view. The **logical semantics and inspectability** are required for a claim, not a particular encoding or endpoint. No technology choice among ML-R02 A/B/C, GEMS/mathspec, LinkML, SysML, JSON/YAML, MPS/LP, PyPSA, Antares or Sienna follows from this model.

This is a **design of evidence information**, not a new repository of qualified IoSN datasets, an implemented verifier or a tool certification. Source authority and source-file bytes remain unverified; G1 remains BLOCKED.

**Sources:** ML-R02 contract_architecture_alternatives.md; ML-R03 data_provenance_and_quality_rules.md (DQ-001–020); ML-R04 tool_conformance_evidence_specification.md, verification_architecture.md; ML-R00 cross_workstream_consistency_review.md.
