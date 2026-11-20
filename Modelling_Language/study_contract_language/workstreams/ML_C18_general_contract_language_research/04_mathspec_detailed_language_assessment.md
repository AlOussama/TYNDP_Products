# ML-C18 / 04 – mathspec: detaillierte Language-/Engine- und Formulierungsanalyse
**Stand:** energy-models/mathspec @ `5f1464c334c1012cdee2947d4d55b4d1d6bef40a`, 2026-11-20. Metrikversion ML-C18/01–02 research-r1. Bewertung betrifft die zusätzliche Aufgabe als übergeordneter Study Contract, nicht pauschal die Qualität von mathspec als mathematischer Spezifikationssprache.

## Quellen- und Implementierungsverzeichnis
| Source | Nachweis | Status |
|---|---|---|
| [Language vs Tool](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/about/what-counts-as-language.md) | Sprachsemantik für alle Tools; Engine darf ablehnen | D_DOC |
| [Limits](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/about/limits.md) | geschlossene Operatoren, Makros, Formulations | D_DOC |
| [Versions](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/about/versions.md), [File shape](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/file.md) | Sprache vs Paket, 13 Sections, version 0 instabil | D_DOC |
| [Assumptions](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/assumptions.md) | Datenprädikate, load-time geprüft ohne Daten | D_DOC |
| [Dimensions](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/dimensions.md), [Relations](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/relations.md) | formale Indizes, Relationstabellen | D_DOC |
| [Absence](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/absence.md) | missing absent/0/refused, where | D_DOC |
| [Variables/Constraints](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/parameters-variables-constraints.md), [Named](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/language/named.md) | Variablen, Objectives, Conditions, macros | D_DOC |
| [Composition](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/docs/reference/composition.md) | merge, override, rename, given | D_DOC |
| [Spec](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/spec.py), [Validation](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/_validation.py), [Program](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/src/mathspec/program.py) | wirkliche Python-Implementierung | I_IMPL |
| [Parser Tests](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/tests/test_parser.py), [Validation Tests](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/tests/test_validation.py), [Composition Tests](https://github.com/energy-models/mathspec/blob/5f1464c334c1012cdee2947d4d55b4d1d6bef40a/tests/test_composition.py) | negative/positive Sprachtasten | T_EXISTING |
| [CI, SHA 5f1464c](https://github.com/energy-models/mathspec/actions/runs/44263210102) | Erfolgreiche Schritte `Run pytest`, lint, docs, LaTeX compiles am 18.11.2026 | T_CI_EXISTING |

Repositories main unverändert gegen angegebene Vorbaseline. Bei Abfrage war v0.4.0 der neueste sichtbare Release (22.10.2026). Paketreleases und Dateisprachversion sind separat; `version: 0` ist dokumentiert instabil. Aus erfolgreicher CI schließen wir **nur**, dass vorhandene Tests in diesem Workflow erfolgreich liefen, nicht dass RC01–RC10 oder Study Contracts experimentell bestätigt sind.

## 1 Exakt implementierte formale Sprachfunktion
`to_spec` in `src/mathspec/_validation.py` führt YAML/Mapping-Validierung durch und validiert die `Spec`-Datenstruktur. `src/mathspec/spec.py` nutzt eingefrorene Pydantic-Typen (`extra='forbid'`) für Sections/entries; Namen, Referenzen, Operatoren, Typen/Dimensionen und Gradbedingungen werden weiter aufgelöst. Eigenständige Expression- und Condition-Parser erzeugen Programmnodes; lesbare negative Tests existieren in `test_parser.py`/`test_validation.py`. Fehlbenannte Schlüssel wie `boundz` führen zu präzisen Fehlern statt stillen Defaults.
Die 13 Sections: `given`, `dimensions`, `relations`, `parameters`, `conditions`, `variables`, `expressions`, `objective`, `constraints`, `sos`, `piecewise`, `assumptions`, `macros`. `Program` bildet bedeutungsbehaftete AST-/Semantik-Einträge. `merge` und `override` ermöglichen Teil-Spec- und Variantenkomposition. `typeset` rendert Mathedokumentation.

## 2 Language-defined vs Engine-defined: ausdrücklich dokumentiert
**Language-defined:** eindeutige Referenzbedeutung, geschlossene Operatorsprache, Indizierung und Dimensionsergebnis, Expression degree, Expansions von Formulations (piecewise/SOS), Bedingungen, `where`, Absence-Semantik. Damit können verschiedene Tools **dieselbe mathematische Spec** lesen und konsistent interpretieren.
**Engine-defined:** konkrete Solver-APIs, Datenobjekte, Modellgenerierung, Lösungsverfahren, Implementierungsrestriktionen; einzelne Engines dürfen inkompatible Sprachenlemente ablehnen, dürfen deren Bedeutung aber nicht verändern.

**Entscheidender Unterschied:** "andere Engine implementiert dieselbe mathspec" ist nicht dasselbe wie "anderer Modellierer darf eine alternative Mathematik wählen". Eine gemeinsame `variables/constraints/objective`-Spec legt bereits fachlich oft unnötige Repräsentation und Nebenbedingungen fest, selbst wenn jede Engine anders kompiliert. Verschiedene mathspec-Dateien können unterschiedliche Mathematik darstellen; ihre gemeinsame **fachliche** Substituierbarkeit wird durch mathspec alleine nicht formal nachgewiesen. Ein externer übergeordneter Contract wäre hierfür zu testen.

## 3 Fehlinterpretationen vermeiden
- `assumptions:` bedeutet dokumentiert Bedingungen **für Inputdaten**, bei Laden typ-/dimensionsprüfbar, bei tatsächlichen Daten prüfen muss der Konsument. Sie sind **nicht** automatisch Assume-Guarantee *Systembehaviour contracts*.
- `relations:` sind tabellarische Indexzuordnungen wie `line -> bus0,bus1`. Das kann eine Topologie *kodieren*, ist aber nicht dasselbe wie vordefinierte Porttypen mit physikalischen Garantien.
- `where:` bedeutet bedingtes Vorhandensein einer Variablen/einer Restriktion, nicht eine freie Behauptung, das System garantiere ein externes Verhalten.
- `given:` deklariert Namen aus anderen Spec-Fragmenten; hilfreich für die Komposition, kein generisches Owner-TBD.
- `absent` versus 0 ist präzise für Daten/Variablentabellen, kein Synonym für `NOT_EVALUATED` bei Forschungsevidenz.
- `mathspec` erlaubt nach den Testquellen quadratische Constraints und Objectives unter den dokumentierten Gradgrenzen; es ist **nicht** einfach eine LP-only-Sprache.
- `version: 0` hat keine Stabilitätsgarantie; Auswertung per präzisem SHA ist notwendig.

## 4 Ist unabhängige Mathematik formulierbar?
**Ja, im Sinne verschiedener mathspec-Dateien mit unterschiedlichen Variablen-/Constraint-Familien.** Eine einzige `mathspec`-Datei mit konkret benannten `variables/constraints/objective` stellt jedoch eine bestimmte Mathematik dar. Dass zwei unterschiedliche Spec-Dateien denselben Battery-/EV-/H2-Contract erfüllen, muss mittels zusätzlichen semantischen Mappings und externen Prüforakeln gezeigt werden. Keine native `PERMITTED_IMPLEMENTATION_VARIANT`-, komponentenbezogene `Assume-Guarantee`-, `StudyPurpose`- oder Multi-Model-Robustness-Semantik aus den inspizierten top-level-Sections nachgewiesen. Das ist eine **Abstraktionsgrenze**, kein Qualitätseinwand gegen mathspec.

**Gegenprobe 1:** H2-Emission in kg/h und elektrische Einspeisung in MW auf derselben mathematischen Relation ohne Umwandlungsgrundlage. Statische dimensionale *Index*korrektheit garantiert nicht physikalische *Einheiten*korrektheit. Eine native physikalische Unit-Check-Funktion ist in den geprüften Quellen nicht nachgewiesen.
**Gegenprobe 2:** Zwei `storage`-Specs nutzen `e(t)` versus kumulative Energie. Beide können gültig sein; eine identische gemeinsame mathematische Spec erzwingt eine spezifische Repräsentation. Ein äußerer Verhaltenscontract kann beide zulassen.
**Positive Konstruktion:** `given` + Relations + benannte Conditions + formale Output-Expressions könnten als *optionales* mathematisches Profil unter fachlichem Contract dienen.

## 5 K01–K17 qualitative Befundmatrix
| K | mathspec-Befund für Study Contract | Evidenz |
|---|---|---|
| K01 | Optimierungsspezifikation detailliert; Study Purpose/vergleichende Methodik fehlen als Kernkonstrukte | D_DOC + schema |
| K02 | Relations/Conditions ermöglichen Modellcodierung, nicht nativ typisierte Behaviour Ports | D_DOC |
| K03 | Engines frei in Implementierung; gemeinsame mathspec bindet math variables/constraints | D_DOC |
| K04 | strenge Trennung Language/Engine; semantische Bindung an mathspec selbst bleibt | D_DOC + I_IMPL |
| K05 | Engines können lösen/builden, aber nicht unterschiedlich interpretieren; zwei Specs möglich | D_DOC |
| K06 | Merge/override unterstützt Varianten, keine native externe semantische Konformität | I_IMPL + tests |
| K07 | Vergleichbare Specs/Outputs formbar; R3/R4 auf Contractebene fehlt | D_DOC |
| K08 | Namens-, Referenz-, Operator- und Indexsemantik sehr präzise | I_IMPL + tests |
| K09 | Datenfreie Validation, Parser, negative Cases, CI erfolgreich | I_IMPL + T_CI_EXISTING |
| K10 | PyPSA-/Storage-/Network-Beispiele vorhanden; allgemeine physikalische Carrier/Portsemantik nicht nativ | examples |
| K11 | `parameters`, `relations`, `expressions`, `assumptions`; Study Process/Data Governance nur ergänzbar | D_DOC |
| K12 | Klarer formaler Optimierungskern; für nichtmathematische Study Contracts zu umfangreich | File shape |
| K13 | Given/merge/override/rename/macro leistungsfähig | D_DOC + tests |
| K14 | Program ist neutrale, definierte mathematische Bedeutung für Engines; kein universeller fachlicher Roundtrip | I_IMPL |
| K15 | Dateisprachversion/Package klar getrennt; Owner-/Quellenprozess extern | Versions |
| K16 | Quellcode/Tests/CI-Pytest erfolgreich auf geprüftem SHA; RC-Experimente nicht ausgeführt | T_CI_EXISTING |
| K17 | Präzise Docs, Typesetting; keine kontrollierte Autorenaufwandsmessung | NOT_EVALUATED |

## 6 Reuse-Potenzial / Designfallen
**Direkte konzeptionelle Übernahme**: "Language-defined meaning vs Engine-defined implementation"; eindeutige Referenzauflösung, deterministische AST/Validierungsfehler; deklarative Conditions/Dimensions/Relations, `given`-basierte Modularisierung und nachvollziehbare Komposition, Typesetting zur Dokumentation. **Adaptation**: statische Einheitentypen/Carrier, Availability/Behaviour/Owner-TBD, Ergebnisprojektionen, echte Verhaltens-Assume-Guarantee-Contracts. **Nicht in generischen Pflichtkern übernehmen**: vorgegebene Variablen, `objective`, vollständige Constraint-Familien, SOS-/piecewise-Engineprofile und geschlossenes Algebra-Operatorinventar, sofern eine Studie sie fachlich nicht zwingend benötigt.

## 7 Validierung und Grenze
Die GitHub-CI auf exakt diesem Commit meldet `Run pytest` success; unabhängige zusätzliche Parserläufe auf RC01–RC10 **NICHT_EXECUTED** (Paket nicht im Arbeitscontainer installiert; externer Repository-Klon nicht erreichbar). Vorhandene Tests sind **kein** unabhängig durchgeführter Konformitäts- oder fachlicher Study Contract Audit.