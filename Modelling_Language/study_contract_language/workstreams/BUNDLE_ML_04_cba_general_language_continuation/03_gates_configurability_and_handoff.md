# BUNDLE-ML-04 — Gate, dependency and method-configuration acceptance matrix

**Date:** 2026-11-24. **Status:** PRE-REGISTERED RESEARCH PLAN ONLY. No new execution evidence in this bundle.

## Phase order and non-deceptive gating

| Workstream | When | Depends on | Minimum deliverable | Correct gate/limit |
|---|---|---|---|---|
| ML-C24-N1 | NOW P0 | immutable B0/C20/C21/P1 | Real A/B parser/decoder -> typed AST -> CSNF -> pinned C21 Python with positive and negative RC01 plus CBA fragment | B1 cannot become MET from JS microtests or only Candidate B |
| ML-C24-N2 | Design NOW P0, execute after N1 interface freeze | N1 typed schema, P5 CBA gaps | General typed operator semantics, external MethodProfile schema and executable two-profile swap | Method swap is mandatory independent subgate |
| ML-C24-N4 | Parallel P1 | C22/P3, later common N1 canonical case | Native SysML/KerML/GEMS/mathspec evidence/loss matrix | H0 UNRESOLVED if runtimes unavailable |
| ML-C24-N5 | Parallel P1 | C23 controls, N2 semantic signatures | Non-CBA component/service/temporal/physical controls; modelling freedom evidence | Generality NOT proved by CBA alone |
| ML-C24-N3 | After N1/N2 B1 verifiable handoff | N1/N2, P2/P5 frozen oracles | Language-based CBA complete study; RC01–10; original 18 C23 + 30 P5 mutations; profile swap | B2_PARTIAL if any required path/coverage missing |
| ML-C24-N6 | After comparable N3 and native/control tracks | N3/N4/N5 & comparable builds | A/B/C/H0 independent minimality, loss, usability, K/NFR/SLR comparison | B3_NOT_READY until adequate comparative evidence |
| Integrated ML-C24 | Conditional ONLY | B1_MET and adequate B2 evidence plus comparable evaluation | Integrated research architecture vote and limits | Never claim owner G1; blocked means do not open integrated PR |

The starting gate is not a claim that the final gate is already achieved. Where full B1 is unreachable, publish an honest B1_PARTIAL blocker and allow explicitly labelled preliminary B2 preparation without promoting B2_MET.

## MethodProfile interchangeability: mandatory executable acceptance test

1. Create two **research-only** method profiles, A and B, differing in a substantive CBA-relevant assumption or a typed aggregation/discount rule, with an explicitly registered method identity and independent version/digest. Both must use a defined supported operator set. They are illustrative and must not be passed off as ENTSO-E-approved values.
2. Define input scenarios, study contract, external data snapshots, expectation oracle, currency/units/price-year rules, and the model/run variation policy. Keep the general language core, parser and validator binaries identical for A and B; record source-code revision/commit, executable checksum, container/runtime fingerprint where available.
3. Execute the same synthetic CBA contract (with resolved external method reference) under A and then B. The only intended change is the profile and its resolved parameter snapshot. No modifications to the core, parser, validator, or arbitrary code. Verify that the measured output delta agrees with an independent numerical oracle and its sign/magnitude are reproducible.
4. Validate that the output and canonical audit ledger contain the correct profile ID/version/digest, source document/status, study-specific assumptions, resolved parameters, provenance and evidence identity. A/B must not be conflated in normalization or cache identity.
5. Mutate profile version, digest, missing rule, invalid dimensional unit, incompatible price year/currency, zero/negative/out-of-range weights, broken counterfactual pairing, overlapping monetisation ledger, missing authority or unsupported rule/operator. Expect explicit typed errors/BLOCKED, never silent defaults or owner-state promotion.
6. Differentiate (a) replacing PARAMETERS, (b) replacing supported DECLARATIVE RULES, and (c) needing NEW EXECUTABLE OPERATORS. Only (a)/(b) must work without source-code changes. (c) must fail safely and be documented as optional future language/runtime extension, assessed generically against non-CBA use cases.
7. Test configuration roundtrip and migration/version compatibility. A method upgrade must never silently modify previously frozen study evidence; version pinning and prior run reproducibility are mandatory.

**Failure conditions:** hardcoded discount/KPI/weighting/owner rules; untyped formula strings or eval; defaulting unknown fields; missing source or method digest; false PASS for unexecuted computation; successful run with mismatched/unknown method version; only changing one constant while method-selection semantics are not expressed. Classify these failures explicitly.

## Minimal evidence/reporting contract

Each workstream's Draft PR should include:
- README with objective, source pins, dependencies and explicit NON-NORMATIVE status.
- Machine-readable manifest: case ID, original source refs, declared expected result, invocation, runner versions, actual result, exact status, evidence path/digest, shortcomings.
- Reproducible command(s) and environment/lockfile. Do not claim an execution solely because test source exists.
- Semantics-vs-Audit comparison matrices; separate responsibility/authority evidence.
- Negative mutation manifest and non-passing cases, including expected vs observed detection.
- SLR01–42, NFR01–18, K01–17, RC01–10 and E1–E5 scope / actual evidence matrix; no changing denominators after results.
- Independent critical review with open defects and explicit gate votes.
- Structured handoff to the next bundle with source SHAs and clearly flagged unresolved items.

## Result vocabulary (normative for this research reporting, not owner methodology)

- EXECUTED_PASS / EXECUTED_FAIL: actually run with recorded command and result.
- SYNTHETIC_ONLY: synthetic data/domain micro-oracle; not a claim for whole language or real solver.
- DESIGN_ONLY: conceptual mapping/specification, not execution.
- NOT_EXECUTED: missing runtime, no invocation or not yet attempted.
- BLOCKED: unmet dependency/authority; no bypass or implicit default.
- NOT_PROVED: insufficient for formal equivalence or conformance theorem.
- B1_MET / B2_MET: only if declared gate criteria, coverage and evidence pass; otherwise PARTIAL.
- B3_NOT_READY / EVIDENCE_INSUFFICIENT: default until supported comparative architecture vote.
- G1_BLOCKED: production/normative owner authorization separate from research evidence.

## Existing baseline limitations to preserve

- P1 15/15 restricted V8 adapter microchecks; original C21 Python not invoked there.
- P2 28/28 independent domain microchecks; no full typed RC language execution.
- P3 native SysML/GEMS/mathspec NOT_EXECUTED, H0 UNRESOLVED.
- P4 synthetic minimality/variation examples; no independent human authoring.
- P5 36/36 independent CBA microchecks including 30 negative mutations; no full language run.
- No ML-C24 integrated architecture implementation authorized by these results.
