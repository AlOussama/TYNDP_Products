# ML-C07 — Pilot Entry and Exit Criteria

**DESIGN_ONLY · 2026-11-12 · nonnormative · G1 BLOCKED.** The phases below are **future conditions**, not phase completion or authorisation. Based on ML-R00 #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2; C03 #46 @ 212bad6811877f9b974b20a1047913c18b1ba756; C04 #45 @ 256541e763147dcb118a3a9d24ca2f52035c672e; C05 #44 @ 1d1bfd18e92d457b415bbad54450bd5aec10963a.

## 1. Phase notation and separation of authority

For consistency with ML-R04 future_multi_tool_pilot_requirements.md, four future phases are denoted **P0–P3** below; these are *pilot phases*, not IoSN process nodes P00–P17. Qualification for a later owner-approved real subset or complete profile is **not** granted by scientific synthetic tests. Each phase needs an independent GO/NO-GO record with a dated responsible role, exact evidence refs and unresolved blocker list; this protocol does not appoint those actors.

| Gate | Nature | Present research status | May proceed now? |
|---|---|---|---|
| R-DESIGN | Design-only ML-C07 artifacts, internal structural audit, no implementation arms | Under preparation; no independent human approval claimed | Yes, as nonnormative research |
| P0 | Synthetic scientific contract/capability dry-run, optional independently built proof-of-concept later | NOT_EXECUTED | Only after its own research-scope authorisation; never label as productive pilot |
| P1 | Native analytic/synthetic cases against two independently built tool implementations | NOT_EXECUTED | Later separate research execution decision required |
| P2 | Owner-qualified, frozen real IoSN data subset | BLOCKED | No: source/data/owner/review prerequisites unresolved |
| P3 | Full candidate-scope scientific conformance / independent judgement | BLOCKED | No: all P2 gates plus full evidence and independent review outstanding |

R-DESIGN and P0/P1 are not proxies for G1. **G1 remains BLOCKED for every phase.**

## 2. Cross-phase entry gates (future)

- **G-01 Contract and methodology:** versioned contract covers exactly 48 provisional MA01-SR (SR-012/-049 excluded), R04-T-SR-NNN tests, P00–P17, conditional P15; methodology effective-release identity, source-claim provenance, D1–D6 decision and MD/CL authority. O26 consultation draft is not approved methodology. **R-DESIGN may document open G-01; P2/P3 require actual closure.**
- **G-02 Input and transformation:** two-arm identical *meaning* of 2035/2040/2050, externally selected CY1–CY5, shared cross-year case-weight vector (not necessarily uniform across CY), UTC intervals/Δt, units, asset/zone/candidate mapping, 87 data objects, 38 transformations and C03 exceptions. **P2/P3 require released original-byte SHA-256 and real owner qualification.**
- **G-03 Domain oracles:** approved economic/discount, starting-grid, P05/P06 physical reduction/PTDF/LODF/N−1, stages P10–P12, B01-D072 pre-expansion H2 baseline, storage/hydro/DSR, conditional P15 cap, B01-D081 KPI/filter and P16/P17 claim definitions. A research-only oracle is allowed in P0/P1 with exact scope_class.
- **G-04 Verification policy:** accepted scope-specific test-depth schedule D0–D4, all V1–V6 and E01–E08 exports, negative controls, immutable status ledger and original-vs-synthetic differentiation. **P2/P3 require owner-qualified numeric, feasibility, optimality, KPI and network acceptance oracles/tolerances; tool-native solver tolerance is not acceptance.**
- **G-05 Tool independence:** two separate teams, independently authored model-generating implementations, build manifests/code/reuse declarations, no A→B model conversion as B, no shared model generator, separated oracle and qualified external review.
- **G-06 Reproducibility/access:** frozen manifests and hashed actually observed artifacts, interpretable source/transform/model/solve/metric DAG, environment and solver settings, licence-compliant reviewer access and change/staleness controls.
- **G-07 Governance:** real Methodology/Data/Domain/Verification Owner decisions and later qualified independent review, then an explicit Gate G1 decision by its authorised authority. No automated status-to-G1 promotion.

## 3. P0 — Synthetic research dry-run / contract & capability

**Entry:** R-DESIGN materials frozen by research authors; synthetic provenance marks every input and oracle as illustrative; 48/48 SR accounted for in proposed test ledger; no missing SR, invented SR, or silent replacement of TBD; P15 predicate encoded as ternary TRUE/FALSE_PROVEN/UNKNOWN; ability to record all six statuses and explicit unsupported features. No original source release, productive thresholds or model implementation is assumed.

**Future actions:** validate contract/test/manifest identity, deliberate broken keys and source conflicts, UTC/unit/weight examples, status machine ST-01–ST-32, evidence completeness and deterministic generation of capability requests. Optionally evaluate mock evidence adapters in a *separate* research experiment; record exactly what ran.

**Exit artifacts:** one frozen synthetic manifest; 48-row obligation audit; P00–P17/process exception register; E01/E02/E08 mock or plan records; test-run log with real attempt IDs **only if executed**, classification and rejected invalid statuses; unresolved owners/guards, semantic-loss ledger; independent design review findings. If no tests are run, report NOT_EXECUTED, never a synthetic PASS.

**Stop:** nonreconcilable SR cardinality; fictitious owner approval; all-0.2 assumption asserted as real CY; missing UTC/Δt; unknown P15 condition silently marked N/A; status ledger fabricates execution, or A→B conversion presented as independent implementation.

**Scientific limit:** P0 checks representation/test protocol, not true model equations, solver optimality, network quality or actual data.

## 4. P1 — Analytic and synthetic native two-implementation tests

**Entry:** P0 structural/semantic defects addressed for P1 scope; a *separate future* research execution decision; both arms and an oracle independently frozen and buildable; exactly identical synthetic semantic input definitions; source-independent C01–C10 and C04 B01–B15 oracles selected, with analytical assumptions, mutation hypotheses and per-obligation minimum evidence; no invented productive tolerances.

**Future actions:** independent Team A and Team B model generation and execution on applicable fixtures; E03–E06 native exports; verifier-created E07; E04 row/column/coefficients/bounds review for high-risk obligations; positive plus negative/mutant sensitivity; E05 primal/objective/certificate reconstruction when solved. D4 triggered where required; distinguish proof from observations. Test status per *tool × fixture × assertion × attempt*; optional OPF both OFF and ON synthetic controls **only where scientifically meaningful**.

**Exit artifacts:** two reproducible separate generator+solve+evidence chains, deterministic/controlled environment record, C04/R04 oracle results and counterexample records, explicit mutant-detection matrix, six-status vectors, cross-tool E-FEAS/OPT/OBS claim boundaries and independence audit, non-invariant portfolio/KPI report; open findings not suppressed.

**Stop:** a mandatory synthetic invariant is demonstrably violated; native evidence cannot be traced to solved model; shared model-source dependence; incorrect positive oracle / undetected negative mutation affecting an intended assertion; unsupported compulsory feature; incoherent objective or missing coefficients; solver failure without diagnostic record. These stops *constrain the affected scope* and do not force every unrelated check to FAIL.

**Scientific limit:** P1 PASS (if actually run) supports the declared fixtures only; nothing establishes productive data qualification or full-parametric equivalence.

## 5. P2 — Owner-qualified real-data subset (later, presently BLOCKED)

**Entry (all mandatory):** G-01–G-06 actually satisfied for the selected subset; owner-approved effective IoSN source; original payload byte hashes verified; licensed reviewer access; source-to-SR reconciliation; external CY selection and real weights/UTC/units; method-specific network/stage/H2/asset parameters; approved solver and KPI tolerances; named qualified reviewer and explicit P2 gate decision. Maintain three separate study-year contexts even if the chosen minimal subset uses restricted topology/candidate sets; any excluded source scope must be explicit and authorised.

**Future actions:** two independent native preprocessing/generation/solve paths on the same frozen *original* subset; E01–E08 verified from actual observations; individual V1–V6/D0–D4 obligations; independent acceptable reference, residuals, certified optimality where claimed, raw-to-reported KPI lineage. Record all conditional modes. A subset lacking P15 does **not** establish P15-ON support.

**Exit artifacts:** qualified input manifest and owner signatures, two native evidence dossiers, approved oracles/tolerance revisions, source/process/model/solver/result ledger, deviations, scoped technical claims plus all open blockers, qualified external review, reproducible rerun instructions and explicit **nonclaims**.

**Stop:** missing or changed source bytes, approvals, oracle revision or threshold; incompatible spatial/UTC/CY axes; invalid H2 pre-expansion baseline or stage transfer assumptions; unreconstructible native model; unreviewed divergence; unapproved loss; any claim that P2 proves complete-profile compliance.

## 6. P3 — Potential full-profile conformance assessment (later, presently BLOCKED)

**Entry:** P2 gates plus all official method/data/owner decisions and full production scope enumerated; every mandatory or conditional SR applicability and oracle qualified; all required scenario/year/variant instances, all required E01–E08 inspection and D4 escalations implemented; two complete independent build chains, external reviewer eligibility, and an explicit P3 approval to attempt assessment.

**Future actions:** evaluate all applicable assertions at their required depth for both arms; independently corroborate physical/mathematical and numerical correctness and output integrity; test mutants and regression/change control; analyse multiple optimal solutions without forced candidate-vector equality; review all exceptions and claim limitations. A full-profile claim is considered only with zero applicable FAIL/UNSUPPORTED/BLOCKED/NOT_EXECUTED **and** sufficient positive evidence and all external approvals.

**Exit artifacts:** qualified reviewer disposition with exact assertion universe U, every N/A with false-antecedent witness, six-status count vector, original/evidence proof graph, objective/KPI sensitivity and uncertainty, reproducibility package, future Owner/Gate decision recorded **separately**. A reviewer may reject or withhold a claim despite all technical checks appearing satisfactory.

**Stop:** any applicable mandatory defect or absent evidence; unanswered material authority/data/oracle question; unbounded equivalence assertion; independence or provenance breach; improper implication from successful checks to tool certification or G1 GO.

## 7. Transition and change rules

Phase completion cannot be inferred from plans or output file presence. An upstream input, contract, generator, mapping, oracle, threshold or KPI change creates a **new** versioned evaluation with stale dependent evidence; no historical PASS is rewritten. A failed arm cannot be bypassed by running only the other. Any optional branch N/A must have a named false-antecedent witness for that exact scope. For a technical headline preserve FAIL > UNSUPPORTED > BLOCKED > NOT_EXECUTED > PASS **only across applicable assertion records**, retain each original reason; an entirely excluded conditional scope reports NOT_APPLICABLE, not universal PASS.

The current **ML-C07 exit criterion** is limited to producing and structurally reviewing the ten requested *design artifacts*, correctly citing input SHAs and open dependencies, with **no actual scientific two-tool pilot run, no owner approval and G1 BLOCKED**.
