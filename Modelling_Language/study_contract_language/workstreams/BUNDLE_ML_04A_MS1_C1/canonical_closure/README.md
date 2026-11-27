# C1 Canonical-First Closure — v0.2
NON-NORMATIVE / RESEARCH ONLY

Baseline: PR #87 7953830daf56aa8a79405e791ed7fc02458af60b; canonicalizer and runtime pinned to mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a. Targeted direct public Program visitor, no temporary legacy math bridge and no independent stored mathematical AST. Existing C1 quantity registry and rational domain checks reused.

The scope admits bounded native arithmetic, named conditions, data assumptions, dense relations/at/group sums, explicit shift/window policies and cases. Closed lexical preflight prevents float rounding before native load and rejects Bool literals inside author conditions because native Mask folding may erase branches. Native numeric constants cannot carry physical units: typed parameter binding is required. Dense data support, relation key/group coverage and exact values checked, not evaluated. Native default missing=refused is a fixed versioned admission policy. Unknown never becomes false/zero in this boundary. Explicit physical conversion factors have research provenance references (not proof of authenticity). Quantifier/behaviour semantics, general Bool3 and method evaluation remain C2. Existing A/B and M0/M2 regression requirements unchanged.

No upstream changes. No general equivalence proof or production approval. This experiment is not the full C1-A4 gate: compare with old gate criteria and record remaining blockers after actual CI. C2 can consume the candidate only for research prototyping unless gate is independently closed or owner approves a revised gate.
