# ML-C22/05 – Pinned mathspec expression semantics / canonicalization
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

**Source read:** https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_canonical.py; support in ML-C19/02 code-analysis and existing test source. mathspec `Spec.to_yaml(canonical=True)` uses `canonical_dict(spec)` and parse->normalise->print of a subset of arithmetic/boolean expression ASTs, then serializes. It sorts known pure commutative sums/products and AND/OR, keyword args, certain collections; it preserves order of position arguments and piecewise links, division/exponent order and comparison-side semantics. It does not make two arbitrary optimization models E4-equivalent or carry a complete external authority/port/Owner model.

## Reuse-by-layer
- Parse/typed operator trees: reuse strategy and proof obligation, not a direct parser import for all CSNF expressions.
- Stable expression printer: useful after binding quantity and scope; do not reorder floating-point reductions unless exact semantics permit.
- Existing canonical roundtrip/property tests: templates for R02–R05 and regressions; a copied test is not new native execution.
- Spec assumptions/given/constraints/objective: represent mathematical formulation *inside an implementation model*, not automatically a Study Contract guarantee or mandatory CSNF field.
- Provenance, Owner and Evidence: external audit ledger or controlled metadata mapping needed; `to_yaml(canonical=True)` is not E2_audit or E4 proof.

### RC05 counterexample
Expression AST for KCL can canonicalize in both angle and KCL-only formulations, while KVL obligation is absent in one. Normalized mathspec source alone must not infer equality of physical feasible projection sets. E1 only within exact typed CSNF/R0 fragment; E2–E5 require separate scope-specific evidence.

**Native mathspec execution in ML-C22:** NOT_EXECUTED. Source-inspection supports partial language-mechanism reuse, not full CSNF interoperability.
