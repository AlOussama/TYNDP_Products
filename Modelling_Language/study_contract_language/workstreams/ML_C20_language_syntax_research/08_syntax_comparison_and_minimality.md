# ML-C20/08 – Syntax candidates and semantic minimality
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

| Criterion | A compact text | B structured document | status |
|---|---|---|---|
| C1–C9 conceptual capacity | named declarations and typed calls | discriminated objects and typed arrays | DESIGNED |
| Semantic references | QID+resolver | JSON IDs+resolver | DESIGNED |
| External component freedom | VariationPolicy, not solver variables | same AST fields | DESIGNED |
| Source/Owner/Evidence identity | audit-linked QIDs | role arrays and audit links | DESIGNED |
| Normalisation | shared typed AST | shared typed AST | NOT_EXECUTED |
| Parser reuse | custom EBNF implementation | standard JSON parser | POTENTIAL |
| Schema enforcement | custom typechecker | JSON Schema envelope + same typechecker | NOT_EXECUTED |
| Authoring simplicity | compact but unfamiliar | verbose but widespread tooling | NOT_EVALUATED |
| Tool interchange | depends on typed lowering | depends on typed lowering | NOT_EXECUTED |
| SysML H0 | C22 controlled profile | C22 controlled profile | UNDER_INVESTIGATION |

Do not interpret nine distinct *functions* as nine minimum classes. Ablate C4 embedded into assertion, C6/C8/C9 typed Referents and C7 assertion-discriminator; assess burden moved to validators, not just reduced node count. No weights or final syntax selection.
