# minimality ablation report

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

### Defined measurement population
Count construct *families* in minimal_mathspec_subset.yaml (20), not grammar productions; classification counts derived from that file. Executed native AST node kinds allowlist in adapter.py: 9 (Constant, ParameterReference, ExpressionReference, Negate, Add, Multiply, Divide, Power, Sum). Native API reused: to_spec, Spec.program, Spec.to_yaml(canonical=True); no own expression parser in the prototype, no private import, no new native operators, no own mathematical canonical rewrite rules. The adapter compiles 10 R1 profile AST operator labels (literal,param,input,rule,select_case,add,sub,mul,div,pow,weighted_sum = 11 labels), checks finite values/signatures, evaluates a closed AST subset and creates receipts. No deletion from M0. Code size is not language minimality; measure nonblank LOC/function counts for selected files in source_manifest or reproduction command; compare only same scope. Native upstream tests are not an M0-M3 savings denominator.

### Ablation witnesses
1. Remove quantity check: same-axis p + m accepted by mathspec, but p MW plus m kg/h invalid; executed rejection by finite adapter.
2. Remove complete support/known value rule: missing row or Unknown may be treated as absent (native missing rules permit other modes); finite adapter explicitly rejects incomplete support and unknown.
3. Remove nonvacuity: an all-false guard can give a trivially true universal; adapter rejects empty active support.
4. Remove individual service projection: aggregate total equals requirement while [0,2] fails first individual request (RC02).
5. Remove KVL: cyclic circulation meets KCL but fails loop obligation (RC05).
6. Remove owner/evidence boundary: native validity says nothing about source approval; original P5 oracle detects false promotion. No fully integrated removal experiment for authority/ledger.
7. Removing own parser is demonstrated for restricted native leaf authoring, not for A/B surface grammar. Native index typing and normalization replace parallel implementation in this prototype, not physical typing or contract normalization.

Ablation here means bounded counterexample comparison, not a systematic executable deletion of all CSNF concepts. Retain C1-C9. C4 arithmetic substructure and parts of R00/R02/R04 are replacement candidates; C5/C6/authority not redundant. No percentage savings, no quantified migration benefit. Full minimality proof pending traceable independent deletion tests on all originals.
