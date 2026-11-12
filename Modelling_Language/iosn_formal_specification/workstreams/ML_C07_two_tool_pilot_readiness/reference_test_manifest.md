# ML-C07 — Scientific Reference Test Manifest

**DESIGN_ONLY · NONNORMATIVE · 2026-11-12 · G1 BLOCKED.** This document defines a *logical manifest* and case-selection protocol. It is **not** a released fixture archive, input-data licence, executable harness, adapter API, or record of two executed tool runs.

**Pinned sources:** ML-R00 #32 9162def25d22c37b1fbc38f7d80fe929425cc8d2 (48-SR integrated traceability), ML-C03 #46 212bad6811877f9b974b20a1047913c18b1ba756 (P00–P17, 38 transforms), ML-C04 #45 256541e763147dcb118a3a9d24ca2f52035c672e (B01–B15/analytic oracles), ML-C05 #44 1d1bfd18e92d457b415bbad54450bd5aec10963a (six statuses, E01–E08), inherited ML-R04/C01–C10.

## 1. Reference manifest — minimum logical fields, **not a wire format**

| Logical record | Required values / identity | Rule |
|---|---|---|
| ExperimentIdentity | pilot_id, phase, manifest_revision, freeze_timestamp_UTC, scope_class, responsible actor | Synthetic and owner-qualified real are different immutable scopes |
| ContractLock | R00 commit, source_release identity + approval state, D1–D6 decision ledger, active MA01-SR revision and test-plan digest | Preserve draft-vs-approved distinctions; 48 active SR, no SR-012 or SR-049 |
| ResearchDependencies | C03/C04/C05 exact commit hashes and relative artifact paths, oracle and mapping revision | Never replace a pinned source with latest without a reviewed update |
| StudyProfile | one study_year in {2035,2040,2050}; external_weather_cases CY1–CY5, each case's upstream source ID, case_weights vector and authority | Same **case-indexed weight vector across three years** under D2 overlay, not necessarily equal 1/5 |
| TimeProfile | ordered UTC half-open intervals [start,end), duration_h, source time key, missing/DST/leap mapping and decision state | No implicit hourly spacing or MW=MWh identity |
| DataInstance | real original-byte hash or explicit UNKNOWN, release/owner/qualification, geometry/carrier/unit and crosswalk revisions; synthetic provenance when applicable | A descriptor or Git commit hash is not verification of original energy-data bytes |
| TransformationLock | C03 P/MLR03-T ID, input/output IDs, code/hash/config, invariant, loss/exception, lineage and replay policy | Process-control and physical input/output dependencies typed separately |
| ModeAndStage | stage P10/P11/P12, P13 paired run, P14 baseline link, P15 OPF condition+invocation witness, LF baseline, candidate allowlist, H2/storage switches | Unknown P15 flag does not justify N/A |
| ToolArm | arm=A/B, independently authored generator revision/build/dependencies, native solver/version/seed/thread/settings, reuse declaration | Neither may consume the other's generated model as its specification |
| TestAssertion | stable test_id, MA01-SR, case_id, positive/negative role, invariant, V-layer, D-depth, guard, mathematical assumptions, expected witness, oracle revision and status | Absence of actual execution remains NOT_EXECUTED; conditions unknown can BLOCK evaluation |
| OracleProfile | type ANALYTICAL / SYNTHETIC / OWNER_APPROVED_REAL / UNRESOLVED, independent author/reviewer, exact validity domain, input and acceptance tolerance ref | No guessed productive epsilon, weights, economics or grid-quality threshold |
| EvidenceIndex | E01–E08 refs, hash method and computed source, native-to-semantic row/column/candidate maps, run/attempt IDs, time and access restrictions | Export labels without native solved model linkage are not evidence |
| Adjudication | per-arm six-state test status with applicability witness/reason; unresolved blockers and incident; source/data/reviewer/gate states separately | A cross-tool objective match is not a test result by itself |

**Suggested key relation:** (contract_revision, study_year, CY_id, variant, P_stage, fixture_id, assertion_id, tool_arm, model_instance, test_attempt). All comparisons require an explicit map between *native* IDs and this canonical semantic index. This is an identifier plan, **not** an imposed schema or serialization.

A fixture must also declare expected **good** behaviour and a targeted **faulty mutation**. Record an oracle derivation, exactly what change was introduced, the predicted violation and the independent check that detects it. A planned negative mutant is not an executed negative-control result.

## 2. Primary reference families inherited from ML-R04

| R04 case | Study purpose | What a future verifier should distinguish |
|---|---|---|
| C01 | Five CY with shared investment | Correct annual investment decision, vector w(c) and operating scenario separation |
| C02 | Deliberately broken nonanticipativity | Missing equalities may preserve one result but change feasible set |
| C03 | Time resolution and units | UTC intervals, Δt and proper MW→MWh/dual-carrier conversion |
| C04 | DC physical flow versus market link | KCL plus physical KVL, controllable candidate not in physical KVL mesh |
| C05 | Aggregation/conservation | Conserved cuts alone do not prove PTDF/LODF/N−1 equivalence |
| C06 | Equivalent LP representations | Different rows/slack variables may preserve projected feasibility/optimality |
| C07 | Multiple optimal portfolios | Same optimal objective with distinct valid portfolios; KPI may depend on portfolio |
| C08 | Deliberately wrong KPI aggregation | Independent replay with correct case weights, Δt and formula version |
| C09 | Missing mandatory tool feature | UNSUPPORTED must not be presented as N/A or PASS |
| C10 | Optional P15 OPF | P15-OFF false-guard N/A only with witness; P15-ON cap and LF reference enforced |

The inherited ML-R04 synthetic_reference_cases/ folder and its oracles.json are **research artefacts**. Any verification of an actual tool must inspect the *tool-generated* model and independent evidence, not only reproduce those expectations.

## 3. Expanded ML-C04 benchmark families and oracle selection

| C04 family | Focus and primary MA01-SR examples | Positive/negative comparison and minimum export |
|---|---|---|
| B01 | Shared investment and nonuniform illustrative CY weights; 002,010,027,029,030,040 | Shared x or scenario copies + equality rows; reject independently optimised x_c, wrong weights; E04/E05 |
| B02 | CAPEX exactly once, ENS/VoLL temporal expectation; 010,011,027,043,044 | Objective term reconstruction; reject multiplied CAPEX, missing Δt; E04/E07 |
| B03 | UTC duration and MW/MWh; 004,011,040 | Time-axis and integral oracle; reject local-time duplicates; E02/E03 |
| B04 | Physical DC mesh and controllable market links; 018,024,028,035,036 | KCL/KVL/NTC typed row inspection; reject market-link KVL or free physical circulation; E04 |
| B05 | Connected zones, PTDF/LODF, seasonal/directional N−1; 013–023 | Necessary conservation plus source-qualified quality oracle when available; reject disconnected graph or wrong outage transfer; E03/E04 |
| B06 | P10→P11→P12 stages and correct cost transfer; 003,027,030–033 | Stage variable allowlist and carry-forward condition; leave method F_y **TBD**, do not approve guessed transition; E03/E04 |
| B07 | Storage power/energy and SoC; 033,034 | Correct initial/end/Δt/efficiency, zero-energy caveat; reject energy-creation and free power-only approximation; E04/E05 |
| B08 | Electricity/H2 coupling and frozen pre-expansion H2 sensitivity; 007,008,009,039,050 | Carrier balances and B01-D072 original run identity; reject final-expansion-derived baseline; E03/E04 |
| B09 | Hydro classifications and DSR conservation; 041,042 | Original resource identity and capacity/energy limits; reject double accounting; E03/E04 |
| B10 | LF baseline and only conditional P15 OPF cap; 024,025,026,028 | Keep LF physics, if OPF active enforce cap, if inactive prove N/A; E04/E08 |
| B11 | Equivalent LP, PTDF/cycle, scenario-copy representations; 018,027,029,043,044,047 | Bidirectional feasible projection/objective map; reject missing slack sign or equality; D4 |
| B12 | Multiple optimum portfolios; 001,025,046,047 | Optimal face and proof of invariants versus portfolio-dependent KPIs; E05/E06/E07 |
| B13 | Raw versus postprocessed outputs; 001,023,025,045,046 | Replay accepted formula only, otherwise FORMULA_TBD and blocked metric; E06/E07 |
| B14 | Missing mandatory capability and skipped checks; 003,026,029,035,047 | Capabilities, six-state transitions, missing rows/evidence; E08 |
| B15 | Offshore exogenous targets and routes; 005,006,037,038,048 | Provenance, exogeneity and separate cost-source mapping; reject unsourced default parameters; E02/E04 |

**Coverage warning:** This is a catalogue of *families*, not proof that each of 48 SR has a direct benchmark oracle. ML-C04 benchmark_requirement_traceability.csv marks DIRECT versus CONTEXT/PARTIAL; **CONTEXT/PARTIAL cannot be promoted to PASS**. The ML-C07 readiness CSV enumerates each of 48 original SRs and the relevant families only as planned probes.

## 4. Required cross-cutting suites and condition branches

- **SR universe:** exactly 48 source IDs from pinned ML-R00, each with primary R04-T-SR-NNN, retained V/depth/risk/owner dependencies and one status ledger row **per arm and scoped attempt** in any future trial. No blanket inferencing from one benchmark to all SRs.
- **C03 traceability:** process P00–P17, R01 M01–M18, 87 B01-D, 38 proposed MLR03-T, 47 structural direct T→T edges and C03's 21 additional process exceptions must be mapped to tests where they constrain an implemented path. An additional conceptual process dependency does not automatically become a producer/consumer edge.
- **C05 state scenarios:** ST-01–ST-32 should be instantiated as independent assertion-status and dependency tests; match expected conditions, not a hard-coded tool result. Include invalid PASS without run, false N/A, missing oracle, stale evidence, unsupported mandatory, failed mutant, reviewer conflict and aggregate fallacy.
- **ML-C04 adversarial mutation list:** 26 designed faulty formulations/transform variants; select and pin those relevant to the tested capability and report *detected / not detected / not run / oracle invalid*. Do **not** confuse this sensitivity descriptor with the six production assertion statuses.
- **Deep-equivalence candidates:** SR-017, -018, -019, -027, -029, -035. D4 is triggered by material formulation/projection risks, not automatically completed by including these IDs in a manifest.
- **P15:** SR-026 has optional antecedent; P15-OFF must be proven from both configuration and invocation history for NOT_APPLICABLE. If ON, generator capacity limits and correct LF portfolio reference are mandatory; missing capability is UNSUPPORTED. UNKNOWN means BLOCKED upon evaluation.
- **Negative controls:** run both conforming and deliberately defective synthetic instances where available; record false positives, false negatives, oracle defects and independent diagnostic. A good mutant discriminator is not a native conformance proof.

## 5. Proposed evidence and acceptance oracle matrix

| Assertion family | Minimum independent reference | Export surfaces | If missing |
|---|---|---|---|
| Source/time/unit/weights | Exact source/UTC/Δt & dimension assertions, synthetic analytical identities or qualified originals | E01–E03/E08 | BLOCKED for required original/authority; synthetic tests remain separately scoped |
| Data transforms and spatial mapping | Typed before/after lineage, conservation, graph and exception checks | E02/E03/E08 | BLOCKED, or FAIL for independently demonstrated wrong transform |
| Mathematics/objective/capabilities | Analytic or source-approved invariant plus actual native row/variable/coefficient proof | E04/E08 | UNSUPPORTED if required export capability is shown absent; otherwise BLOCKED |
| Numerical LP/OPF | Feasible primal, objective recomputation, sound optimality/dual or bounds where claimed | E04/E05/E08 | BLOCKED without certificate/oracle; solver crash alone not mathematical FAIL |
| Raw and derived outputs | E05→E06 raw linkage, independently executed authorised E07 formula | E05–E08 | Undefined KPI if owner formula TBD; never invent a zero or threshold |
| Review and claim | Complete status vector, applicability evidence, role-separated review and approval states | E08 plus referenced chain | Claim WITHHELD when mandatory proof missing; Gate G1 independent |

## 6. Comparison procedure and current state

For each case and each arm: freeze exact fixture; inspect semantic mapping; independently apply oracle; retain raw generated/solver evidence; classify the *individual* assertion, then compare corresponding projected physical variables/obj/bounds. Different native formulations are permitted, unproven projection is not. Use **no productive numeric acceptance threshold until approved**. Solver settings may be recorded for diagnostics but are not owner acceptance.

**Status at ML-C07 authoring:** manifest and oracle selection **DESIGNED**; external real releases, official economic/network/solver/KPI oracle parameters **TBD/BLOCKED**; no Team A or B models/runs, no native D3/D4 evidence, no executed status verdicts created by this workstream. **G1 BLOCKED.**
