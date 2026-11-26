# migration plan

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

**Conditional plan only — no migration authorized.**
1. Freeze M0 and source pins; build public-API compatibility harness against exact mathspec lock. Retain original C21 and both A/B syntax parsers.
2. Define versioned leaf schema, strict qualification/role/physical-unit binding, ordered scope and Unknown semantics. Reuse CSNF C1–C9; use native parse and normalization only for admissible mathematical leaves. R1 physical types, trust, ledger, profile data contracts remain reference implementations, not replaced by the prototype.
3. Implement actual CSNF/leaf roundtrip and validated extension boundary. Prove native static and independent finite checks; support nonvacuous A/G, temporal and information domains, data/output binding. Generalize exact evaluator where required; do not duplicate parser.
4. Bind method AST and output observable in real A/B chain, preserve counterfactual-context flag until resolved, preserve source and authority, signed contributions, independent proof/evidence. Use both frozen R1 profiles and two non-CBA profiles with unchanged code hashes and independent reference oracles.
5. Execute all 58 original identities through both syntaxes (116 paths), original 57 R1 tests, versioned canonical/audit roundtrip, original mutation diagnostics and independent oracles. Revisit B1 only against original criteria.
6. Compare M0/M2/M3 common scope; measure operator/production, parser, adapter and canonical rewrite burden with reproducible denominators and migration cost; independent human authoring/usability and review.
7. If sufficient evidence, request owner authorization for MS2 and selective replacement; otherwise resume T1–T3 gaps. Rollback: M0 preserved, no data/schema changes to old PRs. T1 static semantic boundary, T2 integrated method/output/evidence, T3 independent full original regressions remain acceptance milestones. BUNDLE-ML-04B still gated; SysML H0 OPEN.
