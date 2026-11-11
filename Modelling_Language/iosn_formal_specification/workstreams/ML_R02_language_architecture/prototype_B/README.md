# Forschungsprototyp B — integriertes typisiertes Metamodell

**Nichtnormativ.** `IoSN-TinyMeta` ist eine **eigene** synthetische JSON-AST-Repräsentation; keine offizielle SysML-v2-/LinkML-/GEMS-/CESM-/INES-Implementierung. Ein einziges Modell enthält Requirements-IDs, typisierte Entitäten, gerichtete Kanten, Profileigenschaften, numerische Mikrofixtures und Verification-Links. Anders als A existieren keine fünf separat versionierten Profile; Schema-, Semantik- und Workflowsicht teilen ein einziges Metamodell und seinen Versionsvertrag.

`schemas/metamodel.schema.json` ist ein Draft-2020-12-**Subset**; `run_tests.mjs` prüft darüber hinaus Rollen-, Referenz-, Zeit- und Mikroinvarianten mit Node >=18 ohne externe Abhängigkeiten. Gleiche 22 Szenarien wie A, gleiche erwartete PASS-/FAIL-CLOSED-Ausgänge. Keine validierte allgemeine Ausdruckssemantik, keine Tool-Adapter, kein mathematischer Konformitätsbeweis. Gewichte im Modell symbolisch, nur Fixture numerisch-illustrativ.
