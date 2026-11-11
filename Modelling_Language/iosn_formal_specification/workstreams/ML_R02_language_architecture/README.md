# ML-R02 — Formal Language & Contract Architecture Research
**Branch:** `research/iosn-ml-r02-language-architecture-2026-11-11` · **Basis:** `5c13d4d63f18d30c308997cd7a01f2977fcc6b7b` · **NONNORMATIVE / DRAFT ONLY**

## Lieferobjekte
1. `language_requirements_specification.md` — 20 untersuchende LR-Cluster mit **48/48 MA01-SR Traceability**, L3-/L4- und P00–P17-Bezug.
2. `standards_and_languages_comparison.md` — MBSE, RM, GEMS/CESM/INES/Sienna, mathspec, JSON Schema/LinkML/SHACL, Hybride.
3. `language_capability_matrix.csv` — **15 Ansätze × 12 Kriterien = 180 Einzelzellen**, belegbare Primitive von Erweiterungen und Nichtnachweis getrennt.
4. `contract_architecture_alternatives.md` — alternative Architekturen und Systemverträge.
5. `prototype_A/` — fünf separate Profile und zentrale Registry.
6. `prototype_B/` — integriertes typisiertes Metamodell.
7. `comparative_evaluation.md` — 22+22 synthetische Testresultate, gleiche Mutationen, Limits.
8. `architecture_decision_proposal.md` — nur bedingter Forschungsbeschlussvorschlag, **keine ADR**.
9. `independent_architecture_review.md` — eigenständiger Adversarial-Review-Pass nach Erstellung.
Zusätzlich `requirements_language_crosswalk.csv`, `research_sources.md` zur Auditierbarkeit.

## Reproduktion
```bash
node prototype_A/run_tests.mjs
node prototype_B/run_tests.mjs
```
Keine zusätzlichen Node-Dependencies (Node >=18). Schemadateien sind nur strukturelle Untersets; der JS-Runner wertet sie nicht als JSON Schema aus. Ausgangsprotokolle unter `test_results.json` pro Prototyp sind **nur synthetische Tests**.

## Governance und Grenzen
MA-01 einzige aktive vorläufige SR-Baseline, kein Fremd-Workstream als Quelle. O26 = 25.02.2026 Consultation; D2 = fünf CY1–CY5 als Forschungsoverride (quellmethodischer Konflikt sichtbar). Die D1–D6-Grundsätze sind konstruktive Constraints, **nicht** Eigentümer- oder Datenfreigaben. `G1_REMAINS_BLOCKED`; kein BUNDLE-02- oder Produktionsstart und kein Merge/Ready-Status.
