# ML-C02 — Handoff to nonnormative contract architecture experiments

**Research deliverable, not an Architecture Decision Record.** Starting snapshot: ML-R00 9162def25d22c37b1fbc38f7d80fe929425cc8d2; ML-C02 logical artefacts. A/B/C experiments must not mutate MA01-SR, owner decisions, ML-R00 workstreams or the official methodology. Gate G1 remains BLOCKED.

## 1. Test the shared semantic contract, not the software fashion

Baseline nodes and relations are defined in contract_entities_and_types.md, typed_relationship_vocabulary.md and the **generated NODE/EDGE trace view** contract_traceability_model.csv. The same logical object/identity semantics must survive independent implementations:

- **A — modular registry** with linked source, requirement, data/process, math, output/verification profiles and a closure checker.
- **B — integrated typed model** with explicit discriminated types and integrated graph validation.
- **C — federated governed views** with immutable canonical identity ledger and proof-of-mapping/round-trip loss register.

The experiment must not prejudge A/B/C; A's cross-profile consistency risk, B's schema coupling/evolution risk and C's multi-authority/mapping-loss risk require measured evidence. A/B custom R02 JS prototypes are **not** two independent energy system models; C is a design option without equivalent native pilot evidence.

## 2. Required identical test corpus for all three variants

| Experiment | Positive contract | Controlled negative mutation | Required observable |
|---|---|---|---|
| **EXP-01 IDs** | 48 MA01-SR, 18 P, 18 M, 20 LR, 87 B01-D, 38 T, 48 R04 | remove one process-only B01-D | same IDs/edges survive or blocked import with deterministic reason |
| **EXP-02 authority** | O26 draft + D2 research overlay with source claims intact | mark O26 approved by schema pass | reject authority promotion, preserve claims and conflict |
| **EXP-03 D2** | 3 study years, five external CY each, same symbolic unequal vector | change year-specific weight or allow CY-specific first-stage x | invariant violation; no real numeric fallback |
| **EXP-04 D4 units** | UTC [start,end), explicit 0.5 h and MW→MWh | remove Δt, overlap intervals, mix LHV/HHV | typed failure with exact affected instance |
| **EXP-05 topology** | physical branch mesh + controllable market-link candidate | swap role semantics while preserving endpoint string | reject with M05/M07 semantic reason |
| **EXP-06 reduction** | six reduced-grid output roles with provenance | drop PST or four-directional-seasonal capacity | fail structured completeness, numerical oracle still BLOCKED |
| **EXP-07 process** | P10/P11/P12 and P15 conditionality preserved | force P12 for 2035; mark disabled P15 PASS | reject applicability and unproven execution |
| **EXP-08 verification** | 48 test declarations, no actual Evidence; 6-status enum | attach EvidenceRequest as HAS_EVIDENCE, assert tool PASS | reject type, keep NOT_EXECUTED and G1 BLOCKED |
| **EXP-09 equivalent maths** | shared x ↔ linked scenario copies; DC theta ↔ consistent cycles | unlinked scenario x or omit mesh | proof strength recorded; negative witness rejected |
| **EXP-10 multiple optima** | two feasible equal-objective portfolios on bounded synthetic LP | compare raw x elementwise only, or objective only | report appropriate contract projection and missing KPI tie-break |
| **EXP-11 evolution** | pin semantic revisions and O26/owner scope | change unit/asset role meaning without major change marker | incompatible mapping/migration BLOCKED |
| **EXP-12 intermediate lineage** | distinguish 87 original R03 data definitions from MLR03-I types | count MLR03-I types as new B01-D or treat T spec as execution | detect count/status/identity false claim |

Positive cases may only receive **PASS_STRUCTURAL or PASS_SYNTHETIC** claims qualified by type, not productive tool conformance. Negative cases must include recorded errors, affected IDs and reproducibility.

## 3. Common observation and scorecard (no winner predetermined)

Measure for each experiment and architecture: (i) lossless identity/reference round-trip, (ii) semantic invariant coverage, (iii) distinct blocker/status preservation, (iv) negative-mutation rejection accuracy, (v) version/migration discipline, (vi) owner change blast radius, (vii) ability to export inspectable mathematical generator witnesses, (viii) operational governance burden and reproducibility. Compare **qualitatively and quantitatively** where feasible, with fixed baseline/data/test corpus and recorded parser/validator versions.

**Stop conditions:** an architecture loses branch/market-link role, source authority, P00/20 process-only data, time/unit basis, shared CY investment, evidence status or requirement revision. A structurally successful custom validator is **not** an official conformant SysML/ReqIF/LinkML implementation, nor is a schema pass evidence of scientific soundness.

## 4. Two-tool scientific pilot is a different, later experiment

For native implementations (e.g. PyPSA vs Antares/Sienna, **only if selected later**), require two independently constructed models, the same frozen source release, applicable owner-approved contract profile, explicit data transformations and units, generated-equation/constraint witnesses, solver primal/dual/optimality evidence, raw outputs and KPI independent recomputation. Compare projection of feasible sets and relevant output semantics, rather than native variable names or particular portfolio vectors in a degenerate LP.

Separate (a) architecture contract-representation conformance, (b) native mathematical model fidelity, (c) numerical result fidelity and (d) approval authority. Agreement between tools is insufficient if both encode the same mistaken source interpretation. Original ML-R04 C01–C10 are **synthetic reference sketches**, not accepted production ground truth.

## 5. Suggested artifact contract for experiment runners

~~~text
input: pinned_baseline_sha + canonical_node_edge_manifest + research_profile_revision
       + synthetic_case_revision + mutation_id + expectation
output: representation_id / validator_version / fixture_hash
        + resolved_node_count / edge_count / closure_report
        + rule_id / verdict / precise scope / witness_ref / lossiness
        + source_authority_state / test_scope / test_status / evidence_hash_if_actual
        + owner_approval_state / independent_review_state / G1_state
~~~

Never auto-fill actual source file hashes, signatures, CY weights, accepted numerical tolerances or independent reviewer IDs. For every architecture experiment, provide the same evidence ledger and produce **FAIL / BLOCKED / UNSUPPORTED / NOT_EXECUTED / NOT_APPLICABLE** as genuinely distinguished causes, not a universal boolean.

## 6. Formal handoff acceptance

Can proceed without owner approval to compare structure and semantics **in research scope** once all three candidate representations can ingest all 48 SR, 18 P, M01–M18, LR01–LR20, 87 data incl. 20 process-only, 38 transforms, 48 tests, and all D1–D6 research overlays, maintaining zero fabricated Evidence and explicit TBDs. If any variant cannot preserve all required semantic distinctions, record the limitation; do not revise the baseline to make it pass.

**Deferred:** official methodology authority, real source data/weights, approved cost/network/KPI/hydro/H2/stage oracles, actual native-tool scientific comparison, independent institutional audit, and G1 release. Current status: **NONNORMATIVE_RESEARCH / NO_ARCHITECTURE_CHOICE / G1_BLOCKED**.