# ML-C07 — Tool Capability Assessment Framework

**Research design only · 2026-11-12 · NO PRODUCT/TOOL CONFORMANCE ASSESSED · G1 BLOCKED.** Frameworks such as PyPSA, Antares, Sienna and other systems are **illustrative future candidates**, not selected, ranked, tested, endorsed or certified here. Native capabilities vary by version, extension, modelling formulation, generator and access mode; do not infer support from a product name.

## 1. Assessment question and scope

For a **specific tool version + generator implementation + solver/export stack + contract profile + workload**, can an independent team represent **and make inspectable** each required IoSN semantic property with adequate E01–E08 evidence? Two tool systems may use different internal algebra and files. No prescribed DSL, exchange schema, solver, architecture or converter follows from this framework.

Assess four dimensions independently:
1. **Functional expressivity:** can the native model encode the exact obligation (including conditionality, bounds and indices)?
2. **Semantic equivalence:** if formulated differently, is the common observable/projection semantics valid under explicit assumptions? Does any information disappear?
3. **Inspection/evidence export:** can a verifier reconstruct actual solved row/column/objective/bounds, input transform, primal/dual or suitable certificate, raw results and KPI provenance?
4. **Reproducibility and independence:** can a fixed build/source/input reproduce the evidence without importing the other arm's model or relying on solver self-attestation?

Tool capability is **not** an executed test verdict. A capability assessment with positive evidence cannot become PASS of an MA01-SR unless the scoped property was actually tested against an accepted oracle.

## 2. Proposed feature-support dispositions

| Feature support | Necessary basis | What it does *not* establish |
|---|---|---|
| **SUPPORTED** | Exact scoped function natively represented, required evidence extractable and one or more discriminating probes of the actual generator/export performed; no material unexplained semantic loss | Full IoSN conformance, accepted productive oracle or solver optimality |
| **EQUIVALENT_WITH_EVIDENCE** | Different formulation or data representation; explicit native↔semantic mappings; adequate D2/D3 and triggered D4 proof/validated bounded witness, preserved feasibility/objective/selected observables for declared domain | Universal equivalence beyond proven inputs, mapping or assumptions |
| **UNSUPPORTED** | Required scoped function **or mandatory inspection capability** demonstrably absent, with specific version/build, limitation and negative probe or independently reliable evidence | NOT_APPLICABLE; a way to omit a mandatory requirement |
| **NOT_ASSESSED / UNKNOWN** | No sufficient versioned probe or exported witness; or unknown product behaviour | Never claim support; if such capability evidence is mandatory at assessment time, scoped test becomes BLOCKED |

These are **capability descriptors**, not a seventh C05 test status. For an actual applicable assertion: an established required capability absence leads to UNSUPPORTED; missing mandatory evidence/oracle leads to BLOCKED; planned but unexecuted test remains NOT_EXECUTED if prerequisites are otherwise in order. Legitimate conditional antecedent false with witness leads to NOT_APPLICABLE regardless of irrelevant capability limitations.

**Semantic-loss sidecar, always recorded:** NONE_DEMONSTRATED, REPRESENTATIONAL_ONLY_WITH_PROOF, LOSS_DETECTED (state dropped invariant, indices, chronology, carrier, topology or output), LOSS_RISK_UNRESOLVED, and NOT_INSPECTED. Material semantic loss means SUPPORTED is disallowed for the affected requirement; EQUIVALENT_WITH_EVIDENCE is permitted only if *no relevant loss remains after proven mapping*. A declared known loss that changes required physics/decision degrees of freedom cannot be called equivalent.

## 3. Capability catalogue (research probes, not product claims)

| CAP ID | Required property / evidence distinction | Discriminating future probe |
|---|---|---|
| CAP-01 | Distinct study-year models; five externally supplied CY/case axes and nonuniform weight vector common across years | B01: inspect shared x, per-CY u, coefficients and absence of cross-year investment equalities |
| CAP-02 | UTC interval and explicit Δt, MW/MWh and dual-carrier mappings | B03: spring/fall UTC and non-hourly integral, negative DST/energy mutant |
| CAP-03 | One investment per year across CY or proven equality-coupled replicas | C02/B01/B11: inspect equality rows or shared index, objective CAPEX once |
| CAP-04 | LP variable/constraint family and linear bounds extraction | Export actual generated row matrix/variable map, omitted/zero rows, bound and objective coefficient metadata |
| CAP-05 | Physical DC meshed network KCL and KVL/angle/PTDF/cycle with offsets and slack reference | B04: cycle-flow mutant and physically equivalent angle/PTDF mapping |
| CAP-06 | Controllable candidate market links, directional NTC, no erroneous physical KVL constraint | B04/B10: KCL presence plus inspectable *absence* of candidate in physical cycle space |
| CAP-07 | Detailed-grid clustering and reduced-grid PTDF/LODF/N−1 criteria when qualified | B05: connected partition and contingency witness; original reference/threshold TBD |
| CAP-08 | Stage P10/P11 candidate policies and state carry-forward | B06: allowlist, frozen stage state and cost mapping; method F_y MD-07 TBD |
| CAP-09 | Storage stage P12 for 2040/2050 and operational SoC dynamics | B07: energy/power bounds, efficiencies, boundary indices, no 2035 storage expansion |
| CAP-10 | Electricity/H2 energy conversion; H2 investment exogeneity | B08: carrier balance and inspectable absence of H2 investment decision |
| CAP-11 | P14 frozen prior H2 baseline reference and scenario-sensitive electrical operations | B08: named independent pre-expansion run ID, B01-D072 owner evidence |
| CAP-12 | Hydro class-specific restrictions and DSR without double use | B09: shared resource identity and conservation mutants |
| CAP-13 | LF modelling baseline and paired P13 dispatch | B10: active LF constraint families and two dispatch result lineage chains |
| CAP-14 | P15 conditional OPF with LF-cap linkage only when enabled | B10/C10: OFF false-antecedent proof; ON generated cap rows and output |
| CAP-15 | Objective, costs, weighted ENS, VoLL, price-year/discount trace | B02/B11: independent coefficient and unit replay, no invented economics |
| CAP-16 | Raw unfiltered portfolios, time/case flows, ENS and solver provenance | E05→E06: raw decision vector and native-to-semantic mapping |
| CAP-17 | Owner-defined postprocessing/KPI and undefined/blocked formula state | B13: E07 independent replay from E06; B01-D081 filter authority TBD |
| CAP-18 | Solver primal/bound/certificate export and independently reconstructible residuals | Known LP positive/negative, model-hash match, status vs justified optimality |
| CAP-19 | Source/transform integrity, original-byte SHA-256 and 87-object lineage | Verify exact consumed original bytes and 38 transform specs where relevant; prohibit guessed release |
| CAP-20 | Six-state per-assertion ledger, applicability witnesses and review independence | C05 ST-01–ST-32 invalid state transitions, stale result, P15 UNKNOWN |
| CAP-21 | Multiple-optimum handling and projected equivalence reasoning | B11/B12: two distinct valid optima with optimality proof, KPI range/invariance |
| CAP-22 | E01–E08 evidence closure, audit custody and licensed reviewer access | Verify original-to-claim directed graph, no missing E04/E05 or self-review-as-independent |

Each proposed probe must include **both** (a) tool model functional behaviour and (b) native evidence extraction when relevant. A manually authored sample equation list unrelated to the solved native model is insufficient to prove CAP-04/05/06/18.

## 4. Repeatable assessment record

For each (tool, build, model generator, CAP, contract snapshot, mode and scoped fixture), record:

| Field | Description |
|---|---|
| Identity | tool_name, tool_version/commit, extension versions, generator source revision/hash, solver version, runtime/dependency lock, experiment/arm ID |
| Target | required MA01-SR and semantic family; 2035/2040/2050, CY1–CY5 and stage/optional P15 applicability |
| Native mechanism | model primitives, formulation, constraints/variables exposed and omitted, exact native→contract mapping |
| Evidence | probe/attempt ID, E01–E08 links, generated constraint/variable/cost exports, mutated negative-control output |
| Disposition | SUPPORTED / EQUIVALENT_WITH_EVIDENCE / UNSUPPORTED / NOT_ASSESSED; functional and inspectability ratings **separately** |
| Loss assessment | loss classification, lost dimension/guard, consequence, proof or counterexample; planned mitigation *without asserting success* |
| Equivalence | E-FEAS, E-OPT-VALUE, E-OPT-SET, E-OBS if relevant; quantified domain and D4 review; not one undifferentiated flag |
| Unresolved dependencies | source/data/oracle/tolerance/owner, hidden native model or incomplete export, independent reviewer status |
| Review / change | assessor role, external reviewer if later appointed, timestamp, result version, invalidating upstream changes |

Suggested document structure for any future evaluation: **capability declaration → independent probe → raw and generated evidence → counterexample/equivalence analysis → scoped disposition and limitations**. A tool list without actual probes is only a candidate inventory.

## 5. Worked classification patterns (hypothetical, no real tool findings)

| Scenario | Correct capability conclusion | Assessment/claim consequence |
|---|---|---|
| Shared investment x versus scenario copies linked by all equality rows | EQUIVALENT_WITH_EVIDENCE only after projection/cost proof | Matching objective alone does not establish the relation |
| Physical branch rows include KCL but omit required KVL | UNSUPPORTED or flawed implementation, depending on demonstrated mechanism | Applicable mathematics may FAIL with valid counterexample; no full claim |
| Correct operational model but native E04 row and variable mapping cannot be exported or independently reconstructed | UNSUPPORTED **for required inspection** once proven; otherwise NOT_ASSESSED | Running solver successfully cannot replace D3 evidence |
| P15 disabled with valid contract-specific OFF and non-invocation witness | Feature support need not be used for that scoped branch | SR-026 may be NOT_APPLICABLE; mandatory LF tests remain active |
| P15 enabled, cap not representable | UNSUPPORTED | Cannot be N/A |
| Optimisers return distinct portfolios with same independently certified optimum | Do not mark feature unsupported based on vector difference | Evaluate B12 and objective/KPI invariants separately |
| Real CY weights, network RMSE threshold, discount policy unknown | NOT_ASSESSED for relevant unresolved authority, or capability may remain supported **as a feature** | Scoped productive verdict BLOCKED, not PASS |

## 6. Evaluation policy and non-decisions

No score-weighting, product ranking or mandatory tool pair is defined. Any future trade-off table must not convert UNSUPPORTED into a positive weighted percentage. Test depth D0–D4, E01–E08 and all 48 SR obligations remain requirements of the *scope*, not negotiable product features. A future tool may need a separately verified adapter, but the adapter is an **implementation artifact** and never a substitute for independently constructed mathematical models. No commitments about the capabilities of PyPSA, Antares, Sienna or other software are made.

**Current disposition:** no candidate stack version selected, no capability probes executed, every candidate-specific capability NOT_ASSESSED, all potential losses not inspected, G1 BLOCKED.
