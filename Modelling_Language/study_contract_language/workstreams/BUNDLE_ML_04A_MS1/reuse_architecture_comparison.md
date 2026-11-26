# reuse architecture comparison

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

| Architecture | Language reuse | Implementation reuse | Own responsibilities | Evidence / risk |
|---|---|---|---|---|
| M0 | Existing A/B + CSNF | Existing R1 parser/validator, original C21 | Full expression/typing/normalization + contract | Historical baseline, unchanged original regressions; full-chain gaps inherited |
| M1 | native expression grammar/concepts | none at runtime | independent parser/typing/normalization + contract | design only; duplicates parser; independent grammar drift; no native reuse benefit |
| M2 | restricted native syntax | to_spec, Program, canonical export | AST adapter to original CSNF, physical type, contract/evidence | 9 native fragments executed; bounded static feasibility; dual graph mapping not complete |
| M3 | native mathematical leaf + outer contract | same native public APIs plus finite typed consumer | contract roles, scope, quantity, evidence, method orchestration; no solver generator | finite native consumer + four method leaf swaps; no complete CSNF integration |
| M4 | M3 with extra native language capability if proven necessary | possible adapter/upstream contributions, then fork | compatibility and extension maintenance | deferred; no native operator extension justified by observed cases |

M2 and M3 share upstream code but differ in architectural source of truth: M2 lowers native expressions into the existing mathematical CSNF; M3 stores validated versioned native mathematical leaf as its source of mathematical identity and leaves contract CSNF as outer authority. The experiment does not migrate the R1 CSNF to M3 and does not implement M1/M4. It tests public API feasibility (M2) and a bounded M3-like mathematical consumer; no apples-to-apples full architecture execution. M0 is fallback, M1 preserves control if API instability outweighs reuse, M4 only after M1-M3 demonstrably fail required expressiveness. No fork. No numerical rank.
