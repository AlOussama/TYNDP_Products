# ML-C05 — Tool-Neutral Evidence Interface Requirements

**2026-11-12 · NONNORMATIVE LOGICAL REQUIREMENTS · ML-R00 SHA 9162def25d22c37b1fbc38f7d80fe929425cc8d2 · G1 = BLOCKED.**

## 1. Interface purpose, not a software/API decision

Future independently developed IoSN models (e.g. in PyPSA, Antares, Sienna or another framework) need a **common inspection meaning**, not identical code, native variable labels, model algebra, data transport, solver or a mandatory model translator. This document defines **logical information requirements** for evidence exports E01–E08 and independent conformance assessment; it does not select JSON/YAML, MPS/LP, a schema/DSL, an API, an adapter architecture or a vendor.

For a future scoped implementation evaluation, each logical requirement is classified as REQUIRED_IF_APPLICABLE, CONDITIONAL or INFORMATIONAL. A demonstrably missing mandatory functionality is **UNSUPPORTED**; unknown/uncollected evidence is **BLOCKED** or **NOT_EXECUTED** based on the actual cause. A producer's claim 'supported' without an operational export/probe is not sufficient.

## 2. Information surfaces and interface obligations

| Requirement ID | Surface / logical producer | Required inspection capability (conditional on evaluated profile) | Independent verifier action | Violation class |
|---|---|---|---|---|
| **TI-01** | E01 / Contract custodian | Contract snapshot, 48 SR→MA01-VN/L4 links, source clauses, methodology class, decisions and active variant | Verify immutable exact profile and no unknown SR omission | E01 incomplete ⇒ BLOCKED or D0 FAIL |
| **TI-02** | E01 / Source custodian | Source authority is explicit, draft vs released distinguished, MD/CL and scope reconciliation visible | Refuse to infer adoption from availability | Missing authority ⇒ claim BLOCKED |
| **TI-03** | E02 / Data steward | Actually consumed source release, original file metadata, true SHA-256 or unknown, licence/access, data lineage, frozen input manifest | Check original bytes under authorised access; compare manifest to run | Unqualified source ⇒ C-DATA blocked |
| **TI-04** | E02 / Input exporter | Calendar interval [start,end) UTC, Δt, zones/carriers, dimensional units, y=2035/2040/2050, CY1–CY5 and w(c) across years | Recompute time/energy and equality by corresponding CY; test nonuniform w(c) | V1 applicable failure or BLOCKED if source rule undecided |
| **TI-05** | E03 / Preprocessor | Execution ID, input/output hashes, source→target mapping, parameter and transform versions | Replay or independently balance quantities intended to be conserved | Untraceable mandatory transform ⇒ BLOCKED |
| **TI-06** | E03 / Domain transformation | Explicit transform kind, exceptions, residuals, quality oracle and provenance of interpolation/aggregation | Compare original/aggregated figures at correct axes | Conservation not sufficient for grid equivalence |
| **TI-07** | E04 / Model generator | Stable semantic variable/row family ID linked to SR/process/source/variant plus actual variable/row mappings | Verify role, presence and intended omission | Wrong/missing relevant family ⇒ FAIL; no required support ⇒ UNSUPPORTED |
| **TI-08** | E04 / Model generator | Export variable domains, bounds, stage/year/CY/time/asset indices, units and generated objective coefficients | Recompute common first-stage x, x_max, storage bounds and cost blocks | D3 counterexample ⇒ FAIL |
| **TI-09** | E04 / Model generator | Reconstructible matrix rows with sign/sense, affine term, coefficient, variable key, offsets and scaling | Independently check KCL/KVL/PTDF/NTC/SoC/H2 and omission | Labels alone insufficient; absent mandated inspectability ⇒ UNSUPPORTED or BLOCKED per evidence |
| **TI-10** | E04 / Model generator | Negative obligations: absence of forbidden row/decision couplings and row-coverage counts per index predicate | Ensure market candidates not in physical KVL; no CY-specific free investment | Incorrect coupling/omission ⇒ FAIL |
| **TI-11** | E04 / Stage/variant exporter | P10/P11 stage allowlists, documented carry-forward, P12 storage-year scope, P15 enabled/disabled flag | Compare stages and explicit variant guards | Unknown carry-forward ⇒ BLOCKED; forbidden candidate ⇒ FAIL |
| **TI-12** | E05 / Solver | Exact model instance, solver build/options/seed/threads, termination, primal values and primal objective | Replay every constraint/bound and objective from E04/E05 | OPTIMAL string insufficient |
| **TI-13** | E05 / Solver | A valid optimality witness (dual/lower bound or justified alternative) **if optimality claimed**; native residuals and gap | Independently calculate gaps/bounds after normalisation | Without certificate, only lesser claim or BLOCKED |
| **TI-14** | E05 / Verifier | Independently recomputed primal, dual/optimality diagnostics using accepted tolerance references, plus raw unrounded values | Separate solver defaults from owner acceptance thresholds | Threshold TBD ⇒ accepted numeric PASS BLOCKED |
| **TI-15** | E06 / Result exporter | Unfiltered investment/dispatch/ENS/flows/prices where relevant, axes, original IDs, units, signs and solve-attempt linkage | Compare raw exported variables with solution witness | Only filtered output ⇒ evidence incomplete |
| **TI-16** | E07 / KPI provider | KPI definition/formula version, owner state, input lineage, weights, Δt, price year, discount/filter refs | Independently recompute named KPI; no hidden interpolation/default | Formula TBD ⇒ metric undefined + BLOCKED test |
| **TI-17** | E07 / Comparative observer | Mark KPI as invariant/portfolio-specific with proof or certified interval for multiple optima | Check result differences not falsely classified as model FAIL | Candidate ID mismatch alone cannot FAIL |
| **TI-18** | E08 / Capability reporter | Feature-specific supported/unsupported/unknown state, tool/build and export support, probe evidence | Attempt unsupported or negative capability tests | Mandatory missing ⇒ UNSUPPORTED |
| **TI-19** | E08 / Test runner | Each assertion/revision/attempt, actual execution, six-status classification, conditions and E01–E07 links | Reclassify invalid PASS/N/A/UNSUPPORTED causes | No execution ⇒ NOT_EXECUTED, no silent skip |
| **TI-20** | E08 / Evidence repository | Immutable digests, provenance graph and staleness/change effects; reproducibility inputs and access | Verify critical hash chains and scope/version closure | A schema-valid file is not authentic proof |
| **TI-21** | E08 / Review steward | Distinguish self-review, independent qualified review, owner approval and G1 decision | Validate reviewer independence and authority | Tool/AI cannot sign G1 or source adoption |
| **TI-22** | E08 / Claim producer | Enumerate all applicable mandatory SR, justified N/A, status vector and claim-specific prerequisites | Fail-closed aggregate, no numerical conformance score hiding blockers | False C-FULL claim ⇒ reject claim |
| **TI-23** | All surfaces / Interface owner | Typed units, identity crosswalk and definitions; explicit unknown/TBD and alternative representation mappings | Reconstruct common observable projection across tools | Data loss without disclosure invalidates comparison |
| **TI-24** | All surfaces / Security/data owner | Licence, access restrictions, trusted reviewer ability to inspect original restricted evidence | Approved environment/reproducible access without forced public exposure | Hash-only metadata cannot qualify unavailable original bytes |

This is a **proposed requirement catalogue**, not 24 new MA01 system requirements. TI IDs describe future *evidence exchange capability* and do not modify the active 48-SR universe.

## 3. Semantic export contract for mathematical inspection

A future verifier must be able to form a **tool-independent observation graph**:

~~~text
MA01-SR-029 ──obligates──> shared_investment(year,candidate)
                                  │
                         implemented_by (tool-specific)
                                  │
                         variable IDs + equality rows
                                  │
                      reconstructed projection onto x(year,candidate)

MA01-SR-018 ──obligates──> physical_DC_mesh
                                  │
                       branch/angle/PTDF/cycle mappings
                                  │
                      inspected balance + cycle constraints

MA01-SR-035 ──obligates──> candidate_market_link
                                  │
                      controllable flow + directional NTC
                                  │
                   evidence: not in physical AC KVL family
~~~

It is acceptable for Tool A to use one shared x and Tool B to create scenario-indexed copies with equality rows, provided a justified mapping and projected feasible-space proof are supplied at appropriate D-level. It is **not** sufficient to export only the semantic family name or an MPS file without a mapping from row/column IDs to meaning. A generic sparse-matrix export is an **option** for numerical reconstruction, not a prescribed official transport format.

A model may use algebraically equivalent inequalities, matrix scaling, auxiliary variables and different sign conventions. The exporter must disclose corresponding mappings and objective bases; solver residuals need reconstruction on **one normalised physical/unit basis**. Where a separate native model is inaccessible, the claim must state this inspection limitation explicitly.

## 4. Feature support vs inspection support

Record both:

| Concept | Possible observation | Why separate |
|---|---|---|
| Functional implementation | Tool model can represent the intended KCL, investment, storage or OPF rule | A model may appear to run yet not export rows |
| Evidence extraction | Generator and solver expose enough information to verify required assertions | A hidden equation may be scientifically uninspectable |
| Oracle availability | Accepted reference rule, original data, tolerance and capability-independent verification | Export alone cannot establish truth |
| Execution/replay | Actual complete run on pinned model/input with accessible witness | Declarative support is not executed PASS |

An implementer may generate a separate audit-only representation **if** it is proven identical in relevant semantics to the actual solved model. A manually prepared 'illustrative constraint list' that cannot be tied to the solver's model is insufficient. Absence of required inspection functionality proven by probe is UNSUPPORTED *for a conformance scope requiring that inspection*, even if the modeller asserts the internal model can solve the problem.

## 5. Required comparison and acceptance behaviour

For two independent implementations A/B:

1. agree on **frozen semantic profile and common original/research input identity** before any comparison; compare independently obtained raw inputs to the manifest;
2. map physical source objects, units, study year and CY/UTC into a common observable space;
3. independently check each E04 model's obligations at planned depths (not A→B model translation);
4. check E05 numerical feasibility/certificate **for each generated model separately**, with accepted thresholds;
5. independently recompute E07 KPI and compare **only legitimate invariants or bounded relation**; different valid portfolios need not be equal;
6. record all failing, blocked, unsupported, missing, not-executed and nonapplicable assertions with cause/status and reviewer decisions;
7. issue only scoped claims with source/data/review gates separately controlled.

A mutation that removes KVL, nonanticipativity, cost weights, OPF LF cap or correct UTC duration must be detected by some specifically identified test. A missing effective negative control is a **coverage gap**; favorable positive-case totals do not repair it.

## 6. Performance, reproducibility and governance constraints

Performance and implementation overhead of E04/E05 extraction should be measured in a later pilot. They must not be used to waive critical inspection without a risk/owner decision. Environment/build and source revisions, timezone UTC, locale/decimal conversion, solver seeds and reproducibility notes belong to the evidence. Non-deterministic optimal solutions are assessed by objective/constraints/invariant KPI semantics rather than a false expectation of bitwise identity.

A future logically complete bundle may be realised in a registry, typed metamodel or federated view (ML-R02 A/B/C); this document expressly does **not** choose one. Real source releases, qualified datasets and thresholds are still missing, all native tool conformance checks remain NOT_EXECUTED, and independent sign-off was not obtained. **G1 remains BLOCKED.**

**Sources:** ML-R04 tool_conformance_evidence_specification.md and verification_architecture.md; ML-R02 contract_architecture_alternatives.md; ML-R03 data_provenance_and_quality_rules.md; ML-R00 cross_workstream_consistency_review.md.
