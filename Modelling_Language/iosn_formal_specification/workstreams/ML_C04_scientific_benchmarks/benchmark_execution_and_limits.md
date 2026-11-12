# ML-C04 — Benchmark Execution, Evidential Scope and Limits

**Status: PARTIAL_SYNTHETIC_ORACLE_SELF_CHECK | no native model/tool execution | G1 BLOCKED.**
Input identity: ML-R00 baseline 9162def25d22c37b1fbc38f7d80fe929425cc8d2, Draft PR #32; synthetic fixture blob at final rerun: 3ce73355e7c5ad228cbe29db045223ca1adea571. Date: 2026-11-12 (Europe/Berlin). All numbers deliberately illustrative.

## 1. What was actually executed

**Execution environment:** ChatGPT Code Mode JavaScript runtime (deterministic direct arithmetic/metadata checks using data fetched from the research GitHub branch), not a native energy-system modeller and not a production numerical solver. No external packages, input data source qualification, or tool conversion was involved. Code explicitly checked 15 fixture-positive statements and 15 targeted negative *predicates* (at least one mutation signature per B01–B15). The negative predicates inspect deliberately incorrect alternative arithmetic, structural-condition or status values; they do **not** constitute executing 15 corrupted model generators.

|Run|Git fixture blob SHA|Executed method|Result|Meaning|
|---|---|---|---|---|
|EX-01 initial|fb8c557fbbbbfa650278de7e2879bf14e0c085a6|15 positive + 15 negative JavaScript mini-checks|**14/15 positive, 15/15 negative conditions; B05 positive FAIL**|A deliberate independent cross-check caught a wrong LODF parameter; first run is **not** a suite PASS|
|COR-01 correction|3ce73355e7c5ad228cbe29db045223ca1adea571|Correct B05 LODF values from .5 to 1.0 and expose separate path topology for connectivity-mutant|Corrected source fixture and math docs committed|On triangle, (90−30)/60=1, not .5|
|EX-02 rerun|3ce73355e7c5ad228cbe29db045223ca1adea571|15 positive + 15 negative JavaScript mini-checks|**15/15 positive, 15/15 negative predicates; 0 failed**|Local synthetic arithmetic and stated toy-fixture predicates only|

**B05 diagnostic:** With base f_AB=60 MW, f_AC=f_CB=30 MW, setting LODF_AC,AB=LODF_CB,AB=.5 erroneously predicts 60 MW on each remaining line. Removing AB forces the entire A→B injection 90 MW through the A→C→B path, hence valid post-contingency flows (0,90,90) and factor (90−30)/60=1. A separate path-only graph (A1–A2–B) is now explicitly identified for the disconnected-cluster negative witness. The cut-conservation example with three branches is algebraic KCL only; it is **not asserted to be an electrically calibrated DC mesh case**.

### EX-02 results by family

|Case|Positive synthetic oracle|Target negative signature|Claim scope|
|---|---|---|---|
|B01|PASS_LOCAL|DETECTED|piecewise objective / unequal synthetic CY weights|
|B02|PASS_LOCAL|DETECTED|ENS/VoLL scalar arithmetic|
|B03|PASS_LOCAL|DETECTED|UTC durations and MW→MWh|
|B04|PASS_LOCAL|DETECTED|triangle KCL/KVL|
|B05|PASS_LOCAL|DETECTED|cut, PTDF/LODF, path-connectivity witness|
|B06|PASS_LOCAL|DETECTED|conditional fixed stage and CAPEX arithmetic|
|B07|PASS_LOCAL|DETECTED|2-step storage recursion|
|B08|PASS_LOCAL|DETECTED|H2 conversion and energy-only frozen mutation|
|B09|PASS_LOCAL|DETECTED|reservoir and DSR asset separation|
|B10|PASS_LOCAL|DETECTED|LF/OPF bounds as conditions|
|B11|PASS_LOCAL|DETECTED|slack constraint algebra on sampled points|
|B12|PASS_LOCAL|DETECTED|degenerate portfolio samples|
|B13|PASS_LOCAL|DETECTED|raw aggregation and undefined KPI status|
|B14|PASS_LOCAL|DETECTED|UNSUPPORTED vs conditional N/A|
|B15|PASS_LOCAL|DETECTED|illustrative route and lack of approval|

**NOT executed:** The checked-in Python file synthetic_cases/check_micro_oracles.py was **authored but was not executed** in this GitHub/Code Mode session. Its reproducible use is described in synthetic_cases/README.md; its results cannot be asserted from this record. The external 26-row adversarial mutation catalogue is a *design catalogue*, not an executed 26-mutant suite. EX-02 checks 15 representative *predicates*, not every mutation.

## 2. Reproduction and fixture discipline

1. Check out branch research/iosn-ml-c04-scientific-microbenchmarks-2026-11-12 at the recorded final head SHA in this workstream's README.
2. Inspect synthetic_cases/cases.json (blob 3ce73355e7c5ad228cbe29db045223ca1adea571) and verify declared synthetic-only provenance; no downstream source should silently substitute real CY weights.
3. Optional independent local smoke-check: run python3 synthetic_cases/check_micro_oracles.py from this folder (requires only Python standard library), record actual process exit, stdout, interpreter version and Git hash. This was NOT run by EX-01/02.
4. For future *native tool* testing: generate the actual LP/graph/constraint data for each independently implemented tool, capture emitted rows/bounds/coefficients and per-case outputs, compare using the oracles and their expressly limited proof conditions. Attach native tool and solver version, input hashes and independent reviewer evidence.

**Numeric comparison note:** Direct JavaScript synthetic arithmetic spot-checks use ordinary floating-point arithmetic and a narrow **local implementation comparison** (absolute error below 1e-9 in those specific toy values). The Python illustrative harness uses its own internal float-comparison guard. Neither value is an IoSN numerical acceptance threshold or policy. Productive scaling and acceptance rules remain MD-15/TBD.

## 3. Evidence taxonomy and prohibited conclusions

|Level|Current evidence|Status|
|---|---|---|
|S — symbolic proof on explicitly constrained models|slack/projection bijection, fixed-E SoC mapping, DC angle/PTDF/cycle conditional identity, nonanticipativity replication|RESEARCH_PROOF_WITH_ASSUMPTIONS; not proof on native tools|
|A — analytical numerical derivation|B01–B15 equations and expected values|DERIVED_SYNTHETIC, cross-checked only in shown scope|
|X — executed local synthetic check|EX-01 failed B05 then EX-02 15/15 + 15/15|PASS_LOCAL_FIXTURE_SELF_CHECK **only**|
|D3 — generated native objective and constraint inventory|no tool builder invoked|NOT_EXECUTED|
|V4 — actual native LP optimality evidence (primal, dual, gap)|no LP solver invoked|NOT_EXECUTED|
|D4 — complete parametrised real-tool equivalence|no pair of tools/real grid|NOT_EXECUTED; owner oracle BLOCKED|
|V5 — approved KPI system-needs aggregation|only raw synthetic sums; rules not released|BLOCKED (MD-04/17)|
|V6 — native provenance/independent external review|not present|NOT_EXECUTED / BLOCKED|
|Full IoSN conformance / G1|no authority, qualified data or approved oracles|**BLOCKED**|

**Failure triage:** A mathematically witnessed discrepancy of a defined synthetic invariant is FAIL in that fixture (EX-01/B05); unknown method/Oracle means BLOCKED, unavailable mandatory feature means UNSUPPORTED, an unrun eligible test is NOT_EXECUTED. It is incorrect to convert PASS_LOCAL_FIXTURE_SELF_CHECK into PASS for any MA01-SR, for any concrete tool, or for G1.

No official source records, real CY weights, model runs, product licence acceptance, production tolerances, welfare/discount/KPI formulas, 102-zone model, full H2 LP, weather selection, generic robustness constraints or tool certification were created.
