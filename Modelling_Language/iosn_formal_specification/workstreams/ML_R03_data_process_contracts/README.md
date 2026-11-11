# ML-R03 — IoSN Data, Preprocessing & Output Contract Research

**Research baseline:** BUNDLE-01R PR #25 / `5c13d4d63f18d30c308997cd7a01f2977fcc6b7b`. **Status:** nonnormativer, toolunabhängiger Entwurf; G1/Originaldatenfreigabe weiterhin blockiert.

## Artefakte
1. [`iosn_data_semantic_model.md`](iosn_data_semantic_model.md) — logisches Daten-/Provenienz-Metamodell, Zeit/Ort/Einheiten und Wetterfallachsen.
2. [`input_contract_catalogue.csv`](input_contract_catalogue.csv) — **87** Objektverträge einschließlich **93** ursprünglicher Trace-Link-IDs und offener Parameter.
3. [`preprocessing_contracts.md`](preprocessing_contracts.md) — P00–P17 fachlich erläutert.
4. [`process_transformation_matrix.csv`](process_transformation_matrix.csv) — **38** vorgeschlagene Transformationen/Workflow-Kontrakte.
5. [`model_input_output_contracts.md`](model_input_output_contracts.md) — Modellinput, Solver-Rohoutput, systembedarfsfähige Typen, toolneutrale Semantik.
6. [`postprocessing_contracts.md`](postprocessing_contracts.md) — P16-KPI-Abhängigkeiten, Aggregationsdimensionen, Definition-/Statuspflichten.
7. [`data_provenance_and_quality_rules.md`](data_provenance_and_quality_rules.md) — Fail-Closed, Provenienz, Qualitätsebenen, Gate-Status.
8. [`synthetic_contract_examples/`](synthetic_contract_examples/) — JSON-Schema-Prototyp, synthetische Fixtures, Node-Validator, technische Negativtests.
9. [`data_contract_review.md`](data_contract_review.md) — adversarielle Reviewgrenzen, Abdeckung, offene Findings und Evidenz.

Die ursprünglichen Baseline-Dateien bleiben unberührt. **Keine reale Datensatzversion, kein originaler Datei-Hash und keine KPI-Formel wurde fingiert.** Die einzigen numerischen CY-Gewichte sind als `SYNTHETIC_TEST_ONLY` beschriftet und haben keinen fachlichen Geltungsanspruch.

## Nutzung
Lies zuerst das semantische Modell und das Input-Katalogblatt, danach die Prozessmatrix und die Modell-/Postprocessing-Verträge. Prüfe anschließend `data_contract_review.md`; bei nicht genehmigter Source/Methodik nur Research-Draft-Freigabe, **keine Produktion**.

Für technische Beispielvalidierung: `cd synthetic_contract_examples && node validate_examples.mjs`. Der Validator testet **nur synthetische** technische Integritätsinvarianten. Eine überprüfte Original-IoSN-Instanz oder wissenschaftlich qualifizierter Modellergebnisvergleich ist **nicht** Teil der Suite.
