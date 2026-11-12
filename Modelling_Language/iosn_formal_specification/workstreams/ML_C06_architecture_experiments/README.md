# ML-C06 — Comparative Formal Contract Architecture Experiment

**Status: NONNORMATIVE_RESEARCH / NO_ARCHITECTURE_DECISION / G1_BLOCKED.**

This research workstream is branched from the exact ML-R00 commit `9162def25d22c37b1fbc38f7d80fe929425cc8d2`. ML-C02 (#42; head `136b35e9dc2206b38c95b1e9a68b7d9598a5f86c`) and ML-C04 (#45; head `256541e763147dcb118a3a9d24ca2f52035c672e`) are treated as immutable, pinned research inputs. The `frozen_sources/` files are the original, byte-identical Git blobs and do not update any source PR.

A is a modular registry+profiles; B is a typed integrated model; C is a federated view with semantic ID ledger. All compare the same 528 nodes, 1323 typed edges, B01–B15 synthetic cases, research semantics, and controlled mutations. Only dedicated local JavaScript validators are in scope; no native energy model, external SysML/ReqIF/GEMS/LinkML/SHACL parser, LP-solver, original data qualification, or certification is implied.

Run `node run_experiments.mjs` using Node >=18. See `architecture_benchmark_results.csv` for local test observations; tests are not independent full-scale IoSN conformance. Standalone standards support remains NOT_TESTED unless separately evidenced.
