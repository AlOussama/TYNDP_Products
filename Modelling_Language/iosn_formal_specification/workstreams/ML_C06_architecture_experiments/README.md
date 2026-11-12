# ML-C06 — Comparative Formal Contract Architecture Experiment

**Status: NONNORMATIVE_RESEARCH / NO_ARCHITECTURE_DECISION / G1_BLOCKED.**

This research workstream is branched from the exact ML-R00 commit `9162def25d22c37b1fbc38f7d80fe929425cc8d2`. ML-C02 (#42; head `136b35e9dc2206b38c95b1e9a68b7d9598a5f86c`) and ML-C04 (#45; head `256541e763147dcb118a3a9d24ca2f52035c672e`) are treated as immutable, pinned research inputs. The `frozen_sources/` files are the original, byte-identical Git blobs and do not update any source PR.

A is a modular registry+profiles; B is a typed integrated model; C is a federated view with semantic ID ledger. All compare the same 528 nodes, 1323 typed edges, B01–B15 synthetic cases, research semantics, and controlled mutations. Only dedicated local JavaScript validators are in scope; no native energy model, external SysML/ReqIF/GEMS/LinkML/SHACL parser, LP-solver, original data qualification, or certification is implied.

Run `node run_experiments.mjs` using Node >=18. See `architecture_benchmark_results.csv` for local test observations; tests are not independent full-scale IoSN conformance. Standalone standards support remains NOT_TESTED unless separately evidenced.

## Reproduction and evidential limits

From this directory, use Node >=18 with **no external dependencies**:
```bash
node run_experiments.mjs
node run_change_experiments.mjs
```
The scripts compare their recomputed rows to committed CSVs and throw on drift. Use `--write` only for an intentional, reviewed fixture/regression update. Frozen source cases/trace graph are not regenerated.

On 2026-11-12 the equivalent JavaScript validation functions were **executed in an isolated V8 Code-Mode session**, producing **135/135** expected classifications for the principal A/B/C comparison and **24/24** fail-closed classifications for eight change scenarios repeated per architecture. No separately captured Node CLI process exit or independent reviewer sign-off exists. The outcomes are research-local structural/analytic *checks*; no native model generators, optimisers, standard parsers, semantic migration engines, real datasets or approved tolerance rules were executed.

## Ten requested deliverables

1. `architecture_comparison_framework.md`
2. `comparative_architecture_evaluation.md`
3. `standards_and_extension_gap_matrix.csv`
4. `prototype_A_experiments/`
5. `prototype_B_experiments/`
6. `prototype_C_concept_and_experiments/`
7. `architecture_benchmark_results.csv`
8. `semantic_change_and_migration_analysis.md` (supplement: `semantic_change_test_results.csv`)
9. `independent_architecture_review.md` (separated adversarial research perspective, **not an external signed review**)
10. `conditional_architecture_recommendation.md`

**No architecture, contract language, native energy system tool, or data/model release is selected. G1 remains BLOCKED.**
