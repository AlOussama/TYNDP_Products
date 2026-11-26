# canonical specification csnf mapping

**NON-NORMATIVE / RESEARCH ONLY — MS1 — 2026-11-26**

## Three integration hypotheses
1. **Nested mathematical normal form**: candidate M3. Use native canonical YAML in the mathematical leaf, attach explicit version/source/role/scope/units/identity metadata in CSNF. Native identity never substitutes for contract identity.
2. Extend upstream canonical format to full CSNF: defer. Different scope and approval/evidence semantics would force native schema/operator changes without demonstrated benefit.
3. Keep CSNF mathematical representation and reuse selected native normalization mechanisms: M2 migration fallback. Prefer public API and mapping, not copying private code.

| Axis | mathspec pinned | CSNF requirement / boundary |
|---|---|---|
| Scope / abstraction | mathematical specification incl solver model; parsed source normalization | external study obligations + semantic and audit graph |
| Typed meaning | Program named dims, expression nodes | physical quantity, modality, role, referent, data contract |
| Order | normalizes commutative additions/products, set-like names, dimension declaration/list ordering; noncommutative operand order retained | ordered binders and information/stage order protected; do not sort lists indiscriminately |
| Guards | parsed conditions, mask semantics, AND/OR normalization | Bool3, scope, non-vacuity; preserve original applicability |
| Binding | dimension names / relations / variable names | qualified IDs, alpha-equivalence only proven capture avoidance, role binding |
| Serialization | YAML canonical=True, removes defaults | versioned semantic identity with explicit missing/default semantics and canonical provenance sidecar |
| Units/carrier | not physical type checked | exact conversion basis and carrier typed |
| Authority / source | model metadata/source text only | separate source pin, approval, owner, applicability and trust |
| Evidence / method | no scientific proof identity | independent receipts, profile IDs/hashes, contributions, evidence strength |

Tests: first native run exercises 9 fragments with canonical idempotence and reimport, deterministic repeated rendering within same process, commutative a+b vs b+a, ordered a-b and a/b, unknown operator/name/section rejection, physical-unit gap. Adapter evaluates reimported native Program with exact rational observations. Cross-process/platform determinism, full native composition/typed semantic preservation, full R1/R2 dual audit roundtrip and ordered binder export/reimport not executed. Keep ML-C21 frozen. Source bytes and semantic graph must both be retained; canonical YAML alone cannot preserve audit.

Counterexamples: (a) same native p+m tree with p MW and m kg/h vs both MW, (b) same native guard but missing data coerced false vs blocked Unknown, (c) identical expression under ∀scenario∃decision vs ∃policy∀scenario, (d) equal monetary values in real EUR:2024 vs nominal EUR:2024, (e) same expression with different applicability, source/approval, contribution or method identity, (f) associative floating-point reduction versus exact arithmetic, (g) unsafe divisor zero and omitted row. Therefore mathematical hash equality is not E2/E4; contract graph hash includes leaf language version, binding/scope/units/role, audit hash separately includes original bytes, method/source/evidence identity. Ordered binder preservation is designed, not demonstrated by native normalization. No arbitrary AST nodes accepted.
