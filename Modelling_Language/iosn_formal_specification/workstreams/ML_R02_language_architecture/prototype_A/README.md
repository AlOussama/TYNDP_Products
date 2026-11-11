# Forschungsprototyp A — Registry und fünf Profile

**Nichtnormativ, isoliert, synthetisch.** Registry mit allen 48 MA01-SR-IDs als unveränderte externe Referenzen; neun lokale Requirement-Test-Kanten; expliziter O26/D2-Widerspruch. Profile: Input, Process, Math, Output, Verification. Die mathematischen und semantischen Regeln sind hier bewusst **nur partiell** operationalisiert.

`schemas/registry.schema.json` ist ein **JSON-Schema-2020-12-Subset**; der dependency-freie Node-Validator `run_tests.mjs` ergänzt semantische Assertions, wertet aber **nicht selbst JSON Schema** aus. Alle fünf Gewichte sind im Contract symbolisch. Nur das synthetische Test-Fixture enthält numerische Gewichte. Das Beispiel ist keine Original-ENTSO-E-Datenprüfung und kein Solver.

Ausführen (Node >=18): `node run_tests.mjs`. Die 22 Cases umfassen 1 gültige synthetische Struktur und 21 absichtlich ungültige Varianten; sämtliche Mutationen werden fail-closed abgewiesen. `test_results.json` dokumentiert den isolierten JS-Testlauf. Ein bestandener lokaler Test bedeutet weder Netzreduktionsgüte noch KPI- oder mathematische IoSN-Konformität. Offene Oracles: Netzkongruenz, KPI-Berechnung, Autorität, Datenrelease. Profilversionen sind exakt angeheftet; unbekannte Versionswechsel werden abgewiesen.
