# ML-R00 — Integrated Research Backlog, Dependencies and Deferred Gates

**Version:** 0.1, 2026-11-11 · **Purpose:** Turn ML-R01–ML-R04 into a coordinated, tool-neutral scientific research roadmap **without** reopening deferred approvals. **G1 REMAINS BLOCKED**. This backlog is not a newly approved release plan, normative architecture choice, implementation authorization or BUNDLE-02 entry.

## 1. Explicit separation of what can start now

**Track R — Research preparation, no owner or G1 dependency for design-only work.** Can use O26 consultation and D1–D6 as provenance-labelled *working assumptions*, synthetic examples and open \`TBD\` parameters.

**Track A — Later controlled authority/data/acceptance decisions.** Methodology Owner, Data/Network/Economics/H2/Reporting Owners, qualified independent reviewer and Gate G1 must separately approve original sources, original data releases, numerical oracles and official change decisions. **Do not perform these approvals now.**

This respects the existing project choice to defer normative and data release decisions while advancing formal contract design research. A missing approval remains visible in downstream test applicability/status.

## 2. Prioritized, independently startable research packages

| ID | Recommended research package | Exact input from R01–R04 | Deliverable / falsifiable completion evidence | Dependencies | Boundary |
|---|---|---|---|---|---|
| **RC-01** | **Semantic overlay correction and typed status alignment** | R01 D1–D6; R03 WeatherManifest; R04 six statuses and D0–D4 labels; INT-01/02/03 | Common *research* decision/type registry: \`project_decision:D2\` for same CY-weight vector across years, \`project_decision:D4\` UTC/units, \`test_depth:D4\` equivalence; no 1/5 assumption | none; can begin now | Cannot amend MA01-SR or approve O26 |
| **RC-02** | **Canonical scientific concept/ID reference model** | R01 P/M, R02 LR/A/B/C, R03 B01-D/MLR03-T, R04 VN/Tests/Es/Vs | Stable typed edges, source profile/authority, reference semantics, applicability, version tuples and reversible crosswalk of all 48 SR | RC-01 useful but design may run in parallel | No DSL/AST/architecture winner |
| **RC-03** | **P00–P17 data-to-math-to-evidence dependency closure** | R03 87 data and 38 transforms/47 DAG edges, 20 process-only; R01 M; R04 tests | Per P data producer/consumer, transformation invariants, optionality, source/oracle/evidence edges; explicit **20 process-only dispositions proposed**, not new SRs | can begin now | Producer mapping remains Research Proposal until owner confirmation |
| **RC-04** | **Risikobasierte mathematische Micro-Oracles** | R01 M01–M18 and degrees of freedom; R04 C01–C10, 48 test designs, D5-A1 | Independent synthetic reference cases with negative mutants for *shared x* vs separate x, DC mesh vs NTC market link, reduced-grid PTDF/LODF and N-1, stage carry-forward **alternative TBD models**, storage/H2/hydro/DSR, optional OPF, ENS/KPI dimensionality and multiple optima | independent of RC-02/03 until interface binding | No fabricated real data/tolerances; stage/discount unknown flagged |
| **RC-05** | **Evidence and conformance ontology** | R04 E01–E08/V1–V6/D0–D4, R03 source/provenance, R02 A/B version pins | Consistent scope-separated test status, \`NOT_APPLICABLE\` proof, \`UNSUPPORTED\` vs \`BLOCKED\` vs \`NOT_EXECUTED\`, evidence and hashes/ref policy; preserve ORACLE/TBD and independent-review flags | may begin now; later use RC-01 naming | No automatic approval or trust in self-reported solver results |
| **RC-06** | **A/B/C architecture capability comparison on common semantics** | R02 registry/profile A + typed B + C; unified concept, RC-04 microfixtures | Apply same 48 SR mapping, 18-P process/87-data references, conditional guards, outputs/evidence and negative tests; native standards parsers only when feasible. Record extension burden, semantic loss, trace closure, change impact, native data size and migration effort | RC-02 and RC-04 as benchmark fixture interface | **No premature ADR/DSL/solver commitment** |
| **RC-07** | **Scientific external adversarial review preparation** | R01/R02/R03/R04 internal self-reviews; this integration INT-01–15; original 23 BUNDLE-01R findings | Independent-review package with reproducible provenance and scoped research claims, reviewer checklist, acceptance gap inventory | can prepare now; external human review depends on assignment | A research peer review is **not** Methodology Owner approval or G1 |
| **RC-08** | **Test-catalogue / future two-tool pilot readiness design** | R04 E01–E08, 48 R04 tests/10 C fixtures; R03 model IO | Write *future* input and oracle bundles, proposed evidence export specification, capabilities and out-of-scope handling, tool independence protocol | RC-02/04/05 for coherent design; can prepare partially | No actual production tool-pilot start under G1 BLOCKED |

**Recommended coordination:** RC-01, RC-03, RC-04, RC-05 and RC-07 can begin independently. RC-02 may begin concurrently but should adopt RC-01 labels before publishing a single research profile. RC-06 evaluation requires at least the shared semantics/fixtures from RC-02/04; RC-08 should consume RC-05 evidence state definitions. None requires parallel ML-R01/02/03/04 runs, since all research artifacts are now snapshot-integrated.

## 3. Deferred owner/G1 work — **not** executable as an implied side effect

| Gate or later task | Required genuine evidence | Existing open IDs | Status |
|---|---|---|---|
| Methodology Authority | Original adopted/effective IoSN release, signed method scope/version, original PDF bytes/hash, controlled delta against O26 | MD-01/20 | **NOT_VERIFIED / DEFERRED** |
| Research D2 vs published O26 reconciliation | Explicit authorised 3-vs-5 interpretation for an eventual normative profile, original external CY selection, five numerical source weights, study-year matching | MD-18/19, MD-12 and MD-01 | **DECISION_OPEN / DEFERRED** |
| Frozen source data qualification | Actually consumed PEMMDB/PECD/DFT/H2/network/reference files incl. licenses, versions, original checksums, calendar and 28 true BUNDLE-01R source-data checks | MD-11/12/18/19 | **0/28 ORIGINAL TESTS / DEFERRED** |
| Starting-grid project eligibility | Owner-approved 2035 starting-grid list, O26 §3.4 versus CBA4 §2.5.1 crosswalk and offshore targets | MD-14, MA02-CL-001 | **OPEN / DEFERRED** |
| Network physics and aggregation oracle | Detailed physical grid, connected zones, reduced-grid parameters, flow PTDF/LODF/N-1 seasonal/directional reference and tolerance | MD-03/13/15 | **OPEN / DEFERRED** |
| Economics and stage governance | Discount/vintage/price-year/VoLL, stages, candidate NTC direction and cap, storage proxy, optional OPF applicability | MD-02/06/07/08/09/15 | **OPEN / DEFERRED** |
| Sector details | Exogenous H2 infrastructure and pre-expansion time series, hydro and DSR detail, hourly UTC conversion | MD-10/12/16 | **OPEN / DEFERRED** |
| Needs/KPI and multiple-optima | Exact KPI equations, filter rules, route/cost factor, outcome comparability and multi-optima policy | MD-04/05/17 | **OPEN / DEFERRED** |
| Independent confirmation | Qualified person/organisation review with signed source/Oracle/test findings; separate Gate G1 decision | MD-15/17/20 and G1 | **NOT_OBTAINED / BLOCKED** |

Track A remains **pending and later**. Source facts may be documented in Track R, but signing a new owner rule, approving a data release or taking a G1 GO decision is outside this consolidation and not justified by structural research PASS.

## 4. A staged future readiness model (does not override Gate G1)

| Research checkpoint | Observable exit artifact | What it **does not** mean |
|---|---|---|
| **R0 — Consolidated research snapshot** | All 89 original files preserved, 48-SR crosswalk and integration findings visible | no official methodology approval or real tool PASS |
| **R1 — Semantic baseline for research** | Reconciled D2/D4 labels, typed ID/decision/status namespaces, all 18 P and 48 SR referenced, explicit TBDs | does not change MA01-SR |
| **R2 — Tool-neutral executable micro-oracle design** | independently testable synthetic property fixtures and mutation coverage with source/pseudocode version | no IoSN datasets or certified optimizer |
| **R3 — Architecture comparison** | A/B/C capability/extension/migration/traceability comparison under same fixtures | no normative architecture choice |
| **Later Gate G1** | actual method/data/owner/sign-off evidence, approved conformance oracles | not declared complete by R0–R3 |
| **Later independent two-tool pilot** | approved shared contract + frozen data, two separate energy-model implementations, native E01–E08 artifacts and independent review | NOT STARTED now |

**Result status:** R0 can be closed as documentary work when integration validation succeeds. R1–R3 are research next steps. G1 **does not change** from BLOCKED just because R0–R3 succeed.

## 5. Minimum acceptance for a future cross-tool comparison

A successful *future* pilot will need two independently developed tool models, not two representations of the same unverified implementation and not a M1→M2 translation as the source of truth. Test equivalent **projected feasible spaces or justified reference invariants**, proper common investments over CY, carrier/time/space/units, generator-supplied equation evidence, native solver primal/dual residuals, independently computed output KPIs, and explicitly scoped multiple-optimum interpretation. No production thresholds are set by ML-R00.

**Mandatory missing feature ⇒ UNSUPPORTED**, unresolved owner oracle ⇒ **BLOCKED**, unexecuted test ⇒ **NOT_EXECUTED**, P15 disabled and proven ⇒ **NOT_APPLICABLE for P15 only**, actual applicable counterexample ⇒ **FAIL**. A scoped PASS requires real execution and proper evidence. All must be reported separately per requirement, test layer and approved source profile.

## 6. Change control for the new research snapshot

- Original R01–R04 Git blob SHAs and their Draft PR identities remain intact. **Research integration is a separate PR**; it should not silently back-merge into workstreams.
- All integration-specific labels/finding IDs live under \`ML_R00_consolidation/\`. Mark corrections as **proposals for later harmonisation**, not as post-hoc changes to source statements.
- Any adopted future methodology document requires original bytes/hash, dated authority, clause-level delta, controlled 48-SR impact review and new semantically scoped test oracles.
- The shared snapshot must retain \`AUTHORITY_UNCONFIRMED\`, \`G1_REMAINS_BLOCKED\`, \`NOT_EXECUTED\` and lack of independent signoff in its publication metadata until actually resolved.

**Conclusion:** The scientifically meaningful preparation tasks can proceed in parallel with explicit uncertainties. Methodology/data/owner approvals, a live two-tool pilot and normative contract adoption remain **deliberately deferred**.
