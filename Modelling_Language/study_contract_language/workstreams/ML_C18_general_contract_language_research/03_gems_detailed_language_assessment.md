# ML-C18 / 03 – GEMS: detaillierte Language- und Component-Contract-Analyse
**Stand:** AntaresSimulatorTeam/GEMS @ `9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a`, 2026-11-20. Vergleichsmethodik: ML-C18/01–02 research-r1. Qualität der GEMS-Sprache in ihrer primären Aufgabe ist von ihrer Eignung als *allgemeine Study Contract Language* zu trennen.

## Quellen- und Implementierungsverzeichnis
| Evidenz | Konkreter Source-Pin | Art |
|---|---|---|
| Library/Ports/Models | [library.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/library.md) | D_DOC |
| System/Instanzen/Connections | [system.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/system.md) | D_DOC |
| Expressions/Bind-Constraints | [syntax.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/syntax.md) | D_DOC |
| Taxonomy/Views | [taxonomy.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/taxonomy.md) | D_DOC |
| Output-Katalog | [catalog.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/catalog.md) | D_DOC |
| Zeit-/Szenariokonfiguration | [optimization-configuration.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/optimization-configuration.md), [scenario-builder.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/scenario-builder.md), [calendar.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/doc/user-guide/input-files/calendar.md) | D_DOC |
| Interpreterkompatibilität | [COMPATIBILITY.md](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/COMPATIBILITY.md), [pyproject.toml](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/pyproject.toml) | D_DOC + I dependency |
| Implementierte Anwendungsbeispiele | [basic_models_library.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/libraries/basic_models_library.yml), [pypsa_models.yml](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/libraries/pypsa_models.yml) | I example input |
| Vorhandene Tests | [test_pypsa_eur_tutorial.py](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/tests/e2e_tests/test_pypsa_eur_tutorial.py), [test_objective_parsing.py](https://github.com/AntaresSimulatorTeam/GEMS/blob/9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a/tests/unit_tests/test_objective_parsing.py) | T_EXISTING |
| GitHub Actions auf diesem SHA | [Actions-Lauf 43884814876](https://github.com/AntaresSimulatorTeam/GEMS/actions/runs/43884814876) | T_CI: update-check success; E2E **skipped** |

Aktueller main-SHA wurde per GitHub REST branch endpoint gegen vorherige Baseline geprüft: unverändert. Aktuell sichtbare Releases (zum Abrufzeitpunkt): v0.6.0 (28.10.2026), v0.5.0 etc.; Kompatibilitätsdokument nennt bereits Docs v0.6.1. **Versionierter Entwicklungsstand ist nicht automatisch veröffentlichtes Release.** Das GEMS-Repository ist hauptsächlich Sprache/Dokumentation/Studien/Bibliotheken/Tests, während Engines u.a. Antares-Simulator und GemsPy separat bestehen. `pyproject.toml` listet `gemspy==0.3.0` für Tests; das belegt eine Abhängigkeit, keinen in diesem ML-C18-Lauf installierten Interpreter.

## 1 Spracharchitektur: tatsächlich deklarierte Konzepte
- `library.yml`: `port-types` (fields), `models` (parameters, variables, ports, port-field-definitions, constraints, binding-constraints, objective-contributions, extra-outputs) und Version; die **Model Library formuliert Mathematik**, nicht nur fachliches Verhalten.
- `system.yml`: konkrete `components`, `model`-Referenzen, Parameterwerte/Datenquellen, `connections`. Ein Graph aus Instanzen und getypten Verbindungen entsteht aus Systemdatei plus Libraries.
- **Portsemantik:** Ports übertragen *lineare mathematische Ausdrücke* in Portfeldern. Ein empfangender Bus kann `sum_connections(p_balance_port.power) = 0` verlangen. Bindings können so algebraische Terme zusammenstellen. Dies ist eine starke Kompositionsschnittstelle, aber keine automatisch fachlich vollständige Energiefluss- oder Contract-Semantik. Gleich benannte Felder garantieren weder Einheiten noch identische physikalische Definitionen.
- `taxonomy` spezifiziert erwartete Parameter, Variablen, Ports, Constraints, extra outputs usw. einer Kategorie; zusätzliche Merkmale sind erlaubt. Das kann bei einer nur auf Port-/Output-Semantik eingeschränkten Taxonomie alternative innere Modelle erleichtern; **fordert die Taxonomy identische interne Variable-IDs, reduziert sie Freiheiten**. Die Dokumentation bezeichnet Inheritance als work in progress. Verknüpfung zu Views ist implementierungs-/dokumentationsbezogen und kein universeller Konformitätsprüfer.
- Gleichungsgrammatik: `= <= >=` für lineare Constraints; variable×variable ist in den dokumentierten Ausdrücken nicht zulässig; Zeitabhängigkeit führt zur Entfaltung pro Zeitindex, `sum` aggregiert, `expec` Szenarien; `dual` und solverbezogene Werte für Outputs. Nichtlinearität benötigt Reformulierung; das ist eine Einschränkung **einer GEMS Model-Library-Spezifikation**, nicht notwendig einer übergeordneten Study Contract Language.
- `optim-config.yml` enthält `time-scope`, `scenario-scope`, Solver-/Resolutionwahl, Decomposition etc. Sprachdokumentation warnt selbst: nicht alle dokumentierten Optionen werden von allen Interpretern unterstützt. `system.yml` enthält beispielsweise eine `integer-strategy`, die Antares-Simulator laut Dokumentation ignorieren kann.

## 2 Externe Komponentenverträge / Substitute
Forschungsfrage: Modell `battery_a` und `battery_b` mit verschiedener interner Speicherzustandsformulierung. **Konzeptionell** können beide gleiche Port-Typen und beobachtbare Feldnamen exportieren und in `system.yml` alternativ eingesetzt werden. Die Kompatibilität erfordert aber zusätzlich:
1. gleiche Vorzeichen/Einheit/Zeiteinheit/Standortbedeutung;
2. gleiche extern garantierte Energie-/Leistungsgrenzen und Verlustannahmen;
3. kompatible zeitliche Randbedingungen und Aggregation;
4. nachweisbares Witness-/Prüfverhalten für beide.
Ein bloßes `port-type: flow` plus `field: power` garantiert dies **nicht**. Im GEMS-Original würde jede Variante ihre *eigene* Variablen-/Constraint-Spezifikation tragen; wenn alle Modellierer dieselbe Library benutzen müssen, ist die Formulierung wesentlich festgeschrieben. Die Lösungshypothese ist **oberer fachlicher Contract + mehrere separat versionierte GEMS-Libraries + gemeinsame Observable-Projektion**. Das ist bislang keine native GEMS-Garantie und nicht im ML-C18-Pilot ausgeführt.

**Konkrete Quellenevidenz:** `libraries/pypsa_models.yml` enthält `storage_unit` mit `state_of_charge` und bilanzierender zeitindizierter Constraint sowie `store` mit `e` als alternativer interner Zustand und `p` als Portinjektion. Dies sind zwei *bestehende* Modellarten, **kein Nachweis semantischer Austauschbarkeit**, weil ihre Leistungs- und Kapazitätsannahmen unterschiedlich sein können.

## 3 Unnötige Bindungen für den generischen Contract
- Zwang zur selben `variables`-/`constraints`-Deklaration, `objective-contributions`, linearen Gleichungsform, zeit-/szenarioindizierten GEMS-Modelldefinition oder `integer-strategy`.
- Taxonomy-Pflicht zur Benennung konkreter Variablen/Constraints statt nur Observable-Semantik.
- Fehlende nachgewiesene allgemeine Built-ins für `REQUIRED/PROHIBITED/PERMITTED/IMPLEMENTATION_DEFINED/OWNER_TBD` und echte Assume-Guarantee-Verifikationssemantik.
- Studienfragen, CBA-Wertehorizonte, Datenfreigaben, Robustheitsprotokolle sind **nicht als allgemeiner Study Contract dokumentiert**. Ein GEMS Output Catalog ist nicht identisch mit einem wissenschaftlichen modellübergreifenden Ergebnisvertrag.

## 4 K01–K17: quellenbasierte Befundmatrix (qualitativ vor Scores)
| K | GEMS-Befund für Study Contract | Evidenzgrenze |
|---|---|---|
| K01 | Modellstudienkonfiguration vorhanden, umfassender Studienzweck/Governance nicht nativ | D_DOC |
| K02 | Port-Typen, Field-Definitions und binding-constraints stark; garantierte Außenbehavior nicht als eigener Kontrakt | D_DOC + Beispiel |
| K03 | Libraries erlauben verschiedene konkrete Modelle; gemeinsame *Library* normiert deren Algebra | D_DOC + I example |
| K04 | Syntax-/Library-Konzept von GemsPy vs Antares unterscheidbar; konkrete GEMS-Semantik/Interpreterabhängigkeit bleibt | COMPATIBILITY |
| K05 | Alternative Libraries möglich; einzelne Library definiert Variablen/Constraints | D_DOC |
| K06 | Graph/Model Libraries fördern Austauschbarkeit; semantische Substituierbarkeit unbewiesen | H_TEST |
| K07 | Szenarien, Output Views verfügbar; R3/R4 zwischen unabhängigen Modellen nicht als Contract | D_DOC |
| K08 | Algebra und Indexregeln dokumentiert; physikalische Port-/Carrier-Semantik profilabhängig | D_DOC |
| K09 | Syntax und strukturelle Taxonomy-Regeln dokumentiert; separate Engines nötig; kein eigenes unit checker proof | D_DOC |
| K10 | Electricity/Storage/PyPSA-Beispiele; H2-/EV-Outercase nicht mit gleicher Tiefenprüfung | I example |
| K11 | Input config, data series, catalog/view und outputs; Study Provenance/Evidence ergänzen | D_DOC |
| K12 | Port-/Librarymodell konsistent; fachlicher Contract würde unnötig mathematische Felder tragen | D_DOC |
| K13 | Versionsfähige Libraries/Taxonomy und zusätzliche Modelleigenschaften vorhanden | D_DOC |
| K14 | GEMS-kompatible Interpreterschnittstellen; universeller semantic roundtrip nicht bewiesen | COMPATIBILITY |
| K15 | Library-Versionen, Sprach-/Interpretercompat; methodische Governance extern | COMPATIBILITY |
| K16 | Reale Beispiele/Testdateien und Interpreter-Dependencies; CI am SHA beweist **keinen** E2E-Lauf | T_EXISTING / T_CI skipped |
| K17 | Lesbare YAML, aber keine kontrollierte Autoren-/Interpretationsstudie | NOT_EVALUATED |

## 5 Technische Unsicherheiten und negative Gegenproben
- **Units:** Aus benannten, inspizierten Source-Dateien ist keine durchgängig statisch durchgesetzte dimensionsphysikalische Port-/Energieträgerprüfung nachgewiesen. `NOT_VERIFIED`, nicht "GEMS kann keine Einheiten".
- **Gegenbeispiel:** `flow.power` bedeutet einmal MW-Injektion, anderswo Stromverbrauch in kW mit umgekehrtem Vorzeichen. Gleicher Port-Typ ohne fachlichen Zusatzvertrag ist nicht austauschbar.
- **Gegenbeispiel:** Taxonomy verlangt `state_of_charge`, alternative Implementierung besitzt nur integrierte Zwischenenergie `e` und würde trotz gleicher Außenleistung abgewiesen. Das ist eine Fehlkonfiguration des *gewählten Taxonomy Contracts*, kein prinzipielles GEMS-Verbot.
- **Positiv-Hypothese:** Taxonomy fordert nur Port-/Observable-Felder und nicht innere `variables`; mehrere Libraries mit verschiedenen Zuständen können demselben Energieport genügen. Parser-/Interpreternachweis: `NOT_EXECUTED`.
- **CI-Grenze:** Ein am Commit erfolgreicher "Check Antares Simulator Update" löste **keine** E2E-Ausführung aus (jobs skipped). Andere bestehende Tests sind Quellenevidenz, keine ML-C18-Laufergebnisse.

## 6 Wiederverwendung
Empfehlung nur als **Forschungshypothese**: Port-/Graph-/Library-Mechanismus und klare Instanz/Typtrennung als optionales Implementierungsprofil oder Adapter übernehmen, nicht das vollständige Model-Library-Schema zum generischen Contract erklären. GEMS Model Library bleibt wertvoll für konkrete Optimierungsumsetzung; ihr Zweck soll nicht abgewertet werden.

## 7 Nicht durchgeführte Prüfungen
Keine GemsPy-/Antares-Installation, kein Parserlauf von RC01–RC10, kein Solverbenchmark, kein dynamischer Equivalence Proof, kein unabhängiger Audit. `T_EXECUTED = NONE` innerhalb dieses Forschungsauftrags.