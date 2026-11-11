# ML-R03 synthetische Vertragsbeispiele
**NICHT REAL, NICHT PRODUKTIV UND NICHT NORMATIV.** Keine Originaldatei-Version, echter SHA-256, reale Wetterjahrgewichtung oder IoSN-Datenfreigabe ist hier enthalten. Die 0,2 Gewichte sind ausschließlich ein synthetischer **Gleichheits-/Referenzfixture** für CY1–CY5 über 2035, 2040 und 2050; **reale Werte TBD**. O26-Draft-Identitäten wurden nicht übernommen.

## Inhalt
- `synthetic_contract.schema.json`: optionales maschinenlesbares JSON Schema 2020-12 für grundlegende Struktur; nicht die ganze Methodik.
- `valid_synthetic_fixture.json`: eine hypothetische Demand-Quelle, deren UTC-Intervall und ein abgeleitetes Alignment-Objekt mit durchgängigen Instanz-/Release-/Transformations-/Run-FKs. `RELEASE_BLOCKED` ist absichtlich.
- `invalid_*.json`: negative Testfälle zu Gewichtskonsistenz, CY-Vollständigkeit, UTC, Überlappung, Dimension, Quelldatenref, Provenienz, Definitions-FK, Transform-FK, Dopplung und Verbot einer behaupteten Freigabe.
- `validate_examples.mjs`: ausführbare technische Checks mit Node.js 18+ ohne Drittabhängigkeiten.
- `synthetic_validation_results.json`: beim Erstellen in-memory ausgeführte Assertions; kein produktiver CI-/Owner-Test.

## Reproduktion
```bash
cd Modelling_Language/iosn_formal_specification/workstreams/ML_R03_data_process_contracts/synthetic_contract_examples
node validate_examples.mjs
```
Erwartung: **1 synthetischer Positivfall gültig, 14 synthetische Negativfälle zurückgewiesen**. Das optionale JSON Schema kann gesondert mit einem JSON-Schema-2020-12-Validator geprüft werden. Der CLI-Test verwendet eigene semantische Integritätschecks statt eine automatische Methodik- oder originale Datenqualifikation zu behaupten.

**Geltung:** `validate_examples.mjs` validiert nur ein *kleines* generisches Fixtureformat, nicht alle 87 Objekt-Fachschemas und nicht die 38 Transformationen mit physikalischer/mathematischer Vollständigkeit. Eine erfolgreiche Prüfung ist höchstens `SYNTHETIC_TECHNICAL_PASS`. Für echte IoSN-Daten braucht es signierte Quellen, fachliche Orakel, reale Datenobjekte und unabhängige Reviews.
