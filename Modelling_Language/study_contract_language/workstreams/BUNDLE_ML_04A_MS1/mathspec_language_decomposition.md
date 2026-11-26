# mathspec language decomposition

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

## Evidence basis
[Exact upstream source] (https://github.com/energy-models/mathspec/tree/5f1464c334c1012cdee2947d4d55b4d1d6bef40a); see source_manifest.json for blob hashes, dependency map, native logs and locked runtime. API findings are from this commit rather than assuming later releases preserve them. Source code MIT; documentation attribution CC-BY-4.0 where marked. No upstream code vendored.

| Layer | Actual implementation | Reuse classification | Boundary |
|---|---|---|---|
| Surface | YAML/mapping schema; arithmetic and condition strings | LANGUAGE_REUSE / PUBLIC_API_REUSE | to_spec; schema/validation, not arbitrary extension |
| Abstract syntax | _expression_parser, _condition_parser | INTERNAL_IMPLEMENTATION_REUSE through public API only | parser node API private; no direct import |
| Type/index semantics | _expression_resolver, _condition_resolver, _dimensions, _operators | PUBLIC_API_REUSE through to_spec | index sets, domains, operator signatures; no physical quantity algebra |
| Program | Spec.program, public mathspec.program node classes | PUBLIC_API_REUSE | named expression tree with dims; solver-facing variables remain decisions |
| Canonical | Spec.to_yaml(canonical=True), _canonical.py | PUBLIC_API_REUSE | parsed source normalization, not semantic theorem proving |
| Composition | fragments, given, macros; merge/override/rename | LANGUAGE_REUSE / ADAPTER_REQUIRED | not versioned authority/contract ports; defer native join and macro execution proof |
| Validation | to_spec, LanguageError, Spec construction | PUBLIC_API_REUSE / EXTENSION_REQUIRED | no attached data, scientific proof or owner decision |
| Presentation | upstream typesetting helpers | CONCEPT_REUSE / NOT_ASSESSED | optional authoring layer; no impact on contract verdict |
| Execution | Program consumed by clients; no model solver in MS1 | ADAPTER_REQUIRED | finite observation evaluator, not generator |

The native Program can be constructed without an objective or decision variables. Parameters are constants relative to the mathematical formulation; an external observable can be bound as a parameter **only in an observation-checking context**. The binding is explicitly typed, scoped and identified in the contract. In a model-specification context a variable is a decision; given:variables does not change that. Native assumptions describe data requirements; using an assumption as a technical encoding of a predicate on attached observations does not make it a contract assumption or prove a guarantee. 

The public API is sufficient for parsing, lowering, typed access and canonical export. The public Program nodes are usable as a visitor interface. Raw parsed trees, operator registries and lowerer internals are implementation details. Program.roots/footprint need not include unused/reported expressions; validate the entire permitted fragment, including expressions and conditions. The pinned project is alpha: no forward API stability claim. A package pin, locked dependency environment, public-API compatibility tests and an explicit adapter boundary are mandatory. Upgrade only via reviewed replay.

### Dependency risk
A native consumer receives a closed union of node classes. Unknown node types fail closed; do not monkey-patch native registries. Use composition before additions. Source and docs are separately attributed. Upstream updates may change canonical output even when mathematical meanings are unchanged; version canonical hash namespaces. Direct private imports, fork, and broad dependency on optimizer tooling not required by the observed experiment. Native test coverage applies to upstream semantics, not contract conformance.
