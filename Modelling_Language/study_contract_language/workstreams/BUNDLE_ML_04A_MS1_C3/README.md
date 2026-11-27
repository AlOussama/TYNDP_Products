# BUNDLE-ML-04A-MS1-C3 — partial research integration

**NON-NORMATIVE / RESEARCH ONLY. No completion or C4 entry claim.**

Parent is exact PR #96 HEAD e8a0ee3b7057a1e93afebb1f83b79fd19620446b, not the older tested commit. C2 native code, original frozen catalogues, oracles and native mathspec remain unchanged. See source_baseline.json and the original C2 closure_v1/C3_handoff.md.

## Targeted seam

C2 admits a strict JSON Definition/Instance/Package but does not provide a full M3-native outer syntax A. R1 syntax A embeds an older predicate AST. authoring.py reuses only the pinned R1 lexical and structural parser to define a versioned declaration form over the exact C2 objects. Native package strings are passed unchanged to the C2 validator; no new mathematical parser, AST, evaluator or solver. The authoring envelope requires explicit independently supplied source, definition and instance pins. The synthetic ledger roundtrip control is not original A/B authoring. Structural type/duplicate/trailing checks and source tamper controls are separate from semantic admission. Representation hashes remain distinct while admitted semantic projection must match.

The P5 discount projection extends the narrow CL24 annual amount calculation using the existing C2 affine integer power boundary; independent original oracle expected numbers are read only for comparison after native evaluation. This does not materialize full P5 mutations, contribution/decision context or original A/B sources. Original RC and C23/P5 diagnostics are not reclassified.

## Evidence and gate status

- original_path_coverage.json: all 58 frozen identities / 116 target paths, original expected records, original rule and oracle contracts unchanged. No full paths materialized or run by this initial increment.
- requirement_coverage.csv: all 105 + 20 rows, inherited evidence retained, C3 full evidence explicitly open.
- audit_originals.py: checks exact original coverage, pin and requirement identity preservation; --require-complete deliberately refuses C3 completion.
- test_authoring.py and p5_native_discount_projection.py: actual execution scheduled by the stacked draft PR native workflow; results must be captured from real CI, not inferred from code.
- gate_status.json / critical_review.md / C4_handoff.md: fail-closed decision. C4 not started.

The C3 branch is stacked on the C2 final branch to preserve isolation of the research delta. No main merge or history rewriting.
