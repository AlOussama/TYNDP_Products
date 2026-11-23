# ML-C20/01 – Scope and requirements
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

## Required preservation
Every C1–C9 role and I01–I10 invariant must remain expressible, either as named classes or explicitly discriminated records. Independent identities for source/owner/evidence, variation freedom and external component behaviour are mandatory. A typed AST maps every SLR01–42 to one or more CSNF roles; see `data/slr_expressibility.csv`. This matrix is **design coverage**, not a validation pass or a resolved owner requirement.

## Design non-goals
Not a GEMS algebraic modelling-language implementation; no solver IR, no mandated SOC variable/constraint, no full SysML2 metamodel import, no default energy-to-H2 conversion, no N2E authority fabrication. Study/Process/Observable profiles should remain implementable for nonoptimising workflows. Avoid freezing JSON or compact notation as the winner merely because parsing looks simpler.

## Acceptance categories
Designed representation -> parser-tested -> AST type-checked -> semantically lowered -> audit roundtripped -> independently author-tested. Current state **DESIGNED**, all later evidence NOT_EXECUTED. B1 interface is a typed schema *proposal* version 0.1, subject to versioned compatibility review with C21/C22/C23.
