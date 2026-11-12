# ML-C04 — IoSN Scientific Micro-Benchmark & Mathematical Equivalence Research

**Status:** NONNORMATIVE / SCIENTIFIC_REFERENCE_ONLY / AUTHORITY_UNCONFIRMED / **G1=BLOCKED**  
**Date:** 2026-11-12  
**Baseline:** AlOussama/TYNDP_Products, ML-R00 draft PR #32, commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2  
**Research branch:** research/iosn-ml-c04-scientific-microbenchmarks-2026-11-12  
**Scope:** exclusively this ML_C04_scientific_benchmarks/ directory. ML-C01/C02/C03/C05 and prior workstreams remain unchanged.

## Deliverables (read in order)

1. scientific_benchmark_catalogue.md — 15 tool-neutral families, including all 14 requested topics and additional offshore case; for each hypothesis, typed dimensions, SR/M trace, positive/negative, detection limits.
2. benchmark_requirement_traceability.csv — 74 existing SR-family edges over 48/48 active MA01-SR (35 DIRECT_MICRO_INVARIANT, 39 CONTEXT_OR_PARTIAL); **not** blanket test coverage.
3. analytical_reference_oracles.md — derived numeric toy oracles, explicit symbolic and model-generator boundaries.
4. mathematical_equivalence_and_degeneracy.md — E-FEAS, E-OPT, E-OBS; conditional DC angle/PTDF/cycle, nonanticipativity replication, storage, degeneracy.
5. adversarial_mutation_catalogue.csv — 26 deliberately faulty variants with detection target; *designs, not 26 executed mutated tool models*.
6. synthetic_cases/ — cases.json, Python standard-library **candidate** check_micro_oracles.py, README with 15 positive/negative datasets; all values *illustrative*.
7. benchmark_execution_and_limits.md — actual failed first EX-01 (B05 wrong LODF), correction, passing EX-02 **15/15 local arithmetic positives and 15/15 targeted negative predicates** in independent JavaScript; native tests NOT_EXECUTED. Python candidate harness NOT_EXECUTED.
8. independent_mathematical_review.md — adversarial role review, 16 findings; explicitly **not** an independent human/institutional audit.
9. handoff_to_architecture_and_conformance.md — later evidence/model-conformance interface and open owner gates; no architecture or DSL decision.

## Critical corrections and source guardrails

- D2 identical CY-weight *vector across study years* does **not** imply uniform weights across the five CY. B01/B02 deliberately use synthetic, nonuniform w=(.10,.20,.30,.15,.25), which are not IoSN profile numbers.
- D4 is UTC/time/units; *test_depth:D4* is a separate verification depth, not project decision D4.
- EX-01 caught a newly created LODF=.5 error; for the declared triangle AB-outage it is **1.0**. The correction is in the exact research files with an honest failure/rerun record.
- The network cut-conservation example is **KCL-only** and cannot demonstrate full electrical equivalence; stage-1 carryover, hydro DSR shift and route factor use clearly conditional illustrative assumptions.
- 74 mapped links do **not** mean 48 conformant tests. All MA01 native/tool tests remain NOT_EXECUTED, source authority is unconfirmed, and 21 MD/CL need Owner decisions in the wider research.
- No production discount/KPI, numerical tolerances, real CY weights, robustness requirement or weather-year selection was created; no full IoSN solver or tool certificate.

## Reproducibility

The synthetic fixtures are versioned by Git blob SHA in benchmark_execution_and_limits.md. The committed Python standard-library script is provided as a *future local smoke-check*; this session only executed an independent JavaScript arithmetic check. To run the Python candidate locally:

~~~sh
python3 synthetic_cases/check_micro_oracles.py
~~~

A future independent evaluation must log actual run hash/stdout, generated mathematical row inventories, tool and solver versions, and owner-authorised oracles. **Do not use synthetic checks as G1 or production PASS.**
