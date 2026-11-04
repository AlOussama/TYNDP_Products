# 13 — Implementation roadmap and controlled development tasks

**Principle:** Each stage ends in a falsifiable **gate**. No task changes existing IoSN implementation code or expands into CBA or generic robustness. This is a **proposed work order**, not a commitment of future delivery.

## Gate 0 — Normative source release and governance
**Owner:** IoSN methodology authority + requirements lead.
- Confirm current effective 2026 IoSN document; record source URL, file hash, release status and supersession relations.
- Review O26 §4.6 broken reference, Annex 6.3 parameterization and §3.8 network reduction acceptance tolerances.
- Approve output vocabulary/report scope and which §3.9 studies are mandatory versus optional for each study.
- Provide signed source decision register `MD-01–MD-07` with authoritative clarifications.
**Deliverable:** approved source registry and method ambiguity resolution. **Gate:** no unresolved **normative** ambiguity in the pilot profile; otherwise work remains exploratory.

## Gate 1 — Reference semantics and versioned registry
**Owner:** Systems architect + domain/data stewards.
- Stable identifiers and semantic type dictionary (carrier, unit, time, scenario, node, investment candidate, KPI).
- Implement `requirement`, `method_constraint`, `transformation`, `model_obligation`, `test_case`, `evidence`, `source_statement`, `open_issue`.
- Publish JSON Schema / LinkML prototypes with explicit schema-version compatibility and forward/backward policy.
- Negotiate representation of strict math obligations vs allowed formulation freedom.
**Deliverable:** `iosn-contract-v0.x` profiles with machine-checked cross-reference links.
**Gate:** contradiction injection and dangling-reference tests fail closed; process IDs MR→SR→LRC→VC traverse.

## Gate 2 — UC-01 extend executable weather process
**Owner:** Climate modelling lead + verification engineer.
- Retain **already executed** fixed-scenario/weight output PoC.
- Use actual PECD version and approved Annex 6.3 selection dataset with timestamps, location mapping and hashes.
- Encode feature calculation, standardization, PCA, clustering, representative selection and weighting, with signed seed/ties.
- Build independent reference code and algorithm-specific negative tests.
**Deliverable:** published selected-year dataset and full selection-method conformance evidence.
**Gate:** two implementations reproduce intermediate outputs or explain authorized numerical degrees of freedom; no mismatch masked by passing fixed outputs.

## Gate 3 — UC-02 real coupled micro-model
**Owner:** Two **independent** modelling teams (e.g. PyPSA and Antares/GEMS) + math reviewer.
- Define signed electricity/H2 microfixture: carrier balances, conversion, storage, candidate eligibility and two weighted weather scenarios.
- Express mandatory O26 math profile (two-stage LP, weighted objective, DC flow, same investment across weather).
- Each team builds model natively without copying the other team's generated LP. Capture LP matrix/symbol map or equivalent trustworthy evidence, objective, feasibility residuals and investment decision.
- Compare the approved invariants and diagnose differences; unsupported features emit `UNSUPPORTED`.
**Deliverable:** two real adapters, signed two-engine test case, model evidence and capability-gap list.
**Gate:** both pass independently on identical contract obligations, or conditional architecture selection is rejected/revised. **No claim of actual support until tested.**

## Gate 4 — Network reduction and needs KPIs
**Owner:** Grid planning lead + reporting method owner.
- Formalize §3.8/Annex 6.1 spatial clustering/impedance/rating method; test on small detailed vs zonal systems.
- Sign system-needs data contract, units and KPI equations, aggregation keys and LF vs supplementary study distinction.
- Implement independent aggregation oracle and negative input/result checks.
**Deliverable:** validated network/needs profiles plus independent raw-to-report reconciliation.
**Gate:** conservation and approved electrical equivalence tests; no KPI without definition or lineage.

## Gate 5 — Tool/standards architecture comparison
**Owner:** Enterprise architect + independent review lead.
- Prototype L1 (SysML v2), L2 (minimal DSL), L3 (CESM/GEMS/INES), L4 (modular).
- Reuse the **same three UC reference fixtures and same VC obligations** across candidates; compare ambiguity, functional coverage, conformance effort, readability and ownership cost.
- Check licence/release status and pin tested versions; put failures into the capability matrix.
**Deliverable:** comparative reproducibility pack and updated ADR.
**Gate:** independent reviewers agree evidence supports one option; otherwise maintain PROPOSED.

## Gate 6 — Controlled release of normative interface
**Owner:** IoSN Methodology Change Control Board (to be appointed).
- Freeze released contract bundle (signed source, registry, schema, method/math/output/verification profile).
- Publish tool-agnostic validator and compliance kit, adapter certification guide, migration tests and governance rules.
- Report required/optional scope and waivers; certify only evidence-covered combinations of tool version and method profile.
**Deliverable:** immutable versioned IoSN model blueprint and system acceptance report.
**Gate:** all mandatory tests PASS with evidence, expert approval obtained and no unresolved high-severity normative issues.

## First implementable development task (concrete)
**Ticket:** `IOSN-CONTRACT-001`.
**Scope:** From O26 §3.7 build an externally testable selection-output manifest, JSON Schema and runtime rule interpreter; two adapter shapes, positive/negative fixtures, evidence report.
**Acceptance:** all three horizon tuples and probabilities validated; wrong IDs, weight sum, source/year and provenance rejected; report schema itself verified; simple rerun commands documented; source remains `CONSULTATION`.
**Current completion:** local PoC **11/11 expected outcomes**, 4/4 unit tests passed on synthetic inputs. **Remaining:** real tool adapter and Annex 6.3 full selection algorithm separate tickets.
**Non-goals:** optimization engine, private IoSN code changes, official model certification.

## Recommended next ticket after successful Gate 0
**Ticket:** `IOSN-CONTRACT-002`: encode O26 §3.1.1 `x` non-anticipativity and weighted objective in a signed mathematical obligation profile; independent two-tool micro-fixtures; test case with deliberate scenario-dependent investments must be rejected. Requires approved solver/LP evidence and units. **Status:** NOT IMPLEMENTED.

## Mandatory additions to Gate 3/4 based on detailed O26 clauses
- **Starting grid fixture:** construct 2025 grid + eligible existing/planned project registry to get 2035 reference grid, comparing source project IDs and conditions (VC-15).
- **Candidate abstraction fixture:** include physical AC project that must be represented as a controllable zonal **DC market link with NTC**; reject a generated mathematical model that incorrectly constrains this candidate with the existing meshed DC power-flow equations (VC-20).
- **Hydro and DSR fixture:** distinguish five hydro classes and implicit/explicit DSR, with time-unit checks (VC-19).
- **Offshore environmental/economic fixture:** apply method-authorized uniform sea-use factor, published 525-kV/2-GW VSC technology reference and source-vintage cost factors; require approval for the exact factor (VC-18/21).
- **Reporting fixture:** storage flexibility expansion must be presented as **storage needs**, not misleadingly as battery-only needs; ONDP corridors include distance/cost lineage (VC-11/12).
- **Economic-blocking issue:** O26 §4.6 contains a broken internal cross-reference for discount-block handling; do not certify complete objective/economics until an authoritative clarification is available.
