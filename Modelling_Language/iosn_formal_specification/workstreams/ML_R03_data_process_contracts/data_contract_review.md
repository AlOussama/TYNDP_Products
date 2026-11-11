# ML-R03 — Data Contract Research Review
**Review version:** 0.1.0 · **Date:** 2026-11-11 · **Status:** RESEARCH_CONTRACT_PROPOSAL_WITH_OPEN_DOMAIN_BLOCKERS
**Baseline:** BUNDLE-01R PR #25, commit `5c13d4d63f18d30c308997cd7a01f2977fcc6b7b`.

## 1. Rolle und Unabhängigkeitsgrenze
Reviewperspektive: adversarielle Prüfung durch einen **separaten Analyse-/Prüfdurchgang** auf den von diesem Workstream erzeugten Datenobjekt-, Transformations-, Modellinput/-output- und Postprocessing-Verträgen. Dies ist **kein personell oder organisatorisch unabhängiger externer Audit**, keine ENTSO-E-Freigabe und kein Sign-off. Der Projektstand `G1_REMAINS_BLOCKED` wird dadurch nicht verändert.

**Prüfkriterien:** (A) Vollständigkeit 87/18/93, (B) referenzielle Integrität und Graph-Azyklizität, (C) Fachneutralität und Scope, (D) Daten-vs.-Methodik-vs.-Governance-Trennung, (E) synthetische Prüfungen mit Negativfällen, (F) belegte statt angenommene Freigaben, (G) technische Reproduzierbarkeit.

## 2. Erzielte, eng abgegrenzte Evidenz
| Review-ID | Prüfung | Ergebnis und Grenze |
|---|---|---|
| `R03-REV-01` | Vollständigkeit Inventar | **87/87** IDs `B01-D001`–`B01-D087`; **keine** Quellinventur geändert |
| `R03-REV-02` | Baseline-Klassen | 42 externe, 35 interne, 6 Governance, 1 Studienreferenz, 1 externe Release-Referenz, 2 Review/Verification |
| `R03-REV-03` | Ursprungstraceability | **93/93** ursprüngliche `B01-Txxx`-IDs erhalten, alle SR-FKs gegen 48 aktive MA01-SR gültig; 67 direkt SR-linked, 20 nur Prozess-linked |
| `R03-REV-04` | Prozess-/Transformationsabdeckung | **38** vorgeschlagene Transforms über **18/18** Prozessschritte P00–P17; eindeutige Transformations-IDs |
| `R03-REV-05` | Transformationsreferenzen | alle B01-/neuen MLR03-I-Referenzen gegen Katalog/Produzenten aufgelöst |
| `R03-REV-06` | Interne Producer-Deckung | **35/35** interne Typen mit mindestens einem vorgeschlagenen Transforms-Output; **keine Behauptung tatsächlicher Ausführung** |
| `R03-REV-07` | Statischer Transformationsgraph | **47** abgeleitete Producer/Consumer-Kanten, **0** Graphzyklen |
| `R03-REV-08` | Synthetic fixtures | **1 positiver** + **14 negative** Fälle, **15/15 in-memory Assertions erwartungsgemäß**; Node.js-Script beigefügt, kein Repo-CI-Ergebnis behauptet |
| `R03-REV-09` | Änderungsumfang | GitHub-Vergleich gegen Baseline nur neue/geänderte Dateien **unter** `ML_R03_data_process_contracts/`; Original-MA03/BUNDLE01/R unverändert |
| `R03-REV-10` | Wissenschaftlicher/normativer Status | sämtliche Ergebnisse markiert `NON_NORMATIVE`; externe Originaldateien, Owner-Signaturen, mathematische Orakel **nicht** qualifiziert |

Die Prüfungen `REV-01` bis `REV-07` und `REV-09` sind **Strukturprüfungen**. `REV-08` ist nur technische Syntax-/Referenz-/Zeit-/Einheitentestung synthetischer Daten. Keine der zehn Prüfungen beweist einen methodischen Energiesystemmodell-Constraint oder ein tatsächliches 2026-IoSN-Source-Dataset.

## 3. Kritische Findings / offene fachliche Autorität
| Finding | Priorität für spätere Freigabe | Feststellung | Erforderliche spätere Evidenz |
|---|---|---|---|
| `R03-F01` | P0 | Neueste maßgebliche Methodik-/Quellenautorität nicht nachgewiesen; O26 ist Konsultationsstand, kein eingefrorener freigegebener Vertrag | Methodology-Owner: Release/Date/Version/Originalbytes |
| `R03-F02` | P0 | **87** Objekte besitzen keine qualifizierten IoSN-Originalpayloads oder tatsächlich berechneten Original-SHA-256; 28 Originaldatenchecks nicht ausgeführt | Data Owner: Run-Freeze, originale Dateien, Checksums, Testläufe |
| `R03-F03` | P0 | 93 fachliche Data-SR-Zuordnungen sind Analystenvorschläge, nicht vom Domain Owner bestätigt | Requirements-/Domain Owner: zeilenweise Traceability-Abnahme |
| `R03-F04` | P0 | 5×3 CY-Fälle gemäß Projektprämisse stehen zum älteren O26-Draft mit je 3 konkreten Wetterfällen im Konflikt; gemeinsame Gewichte numerisch **TBD** | Methoden-/Wetter-Owner: genehmigtes Override, Quellen, w-Vektor |
| `R03-F05` | P0 | Verifizierte numerische Netzreduktions-, N−1-/RMSE-/LODF- und Clustering-Orakel fehlen; bestehende detaillierte 2025-Netzdaten nicht qualifiziert | TSO/Reduction Owner: Referenzfälle, Schwellen, Messmethode |
| `R03-F06` | P0 | LP-Stufenübergabe, Kosten-/Discount/Basis und fachliche Zielfunktion nicht vollständig bestätigt | Expansion-/Economics Owner: Stufenkontrakt und numerisches Oracle |
| `R03-F07` | P0 | KPI-Formeln, ENS-/Kostenvorteil, Kleinmengenfilter und ONDP-Allokation unbestätigt | Reporting Owner: Definition-ID, Formel, Achsen, Referenzbasis, Filter |
| `R03-F08` | P1 | UTC-Intervalle formalisierbar, aber DST-/Leap-/Kalender-Detailkonversion und Qualitäts-Toleranzen (MD-12) offen | Time/Data Owner: technische Konversionsrichtlinie |
| `R03-F09` | P1 | B01-D072 vor Expansion erzeugte H2-Last erfordert benannten präexpansiven Referenzlauf; T14-00 ist eine **Forschungsskizze**, kein verifizierter Lauf | H2-/Model Owner: exakt benanntes Baseline-Resultat |
| `R03-F10` | P1 | B01-D081 wurde in der Originalinventur als interner Zwischenobjekttyp klassifiziert; fachlich benötigt es eine externe Owner-Regel. T16-00 stellt nur die fehlende Steuerungsautorität dar | Reporting Owner: Autorität/Status/Einheit der Filterregel |
| `R03-F11` | P1 | Synthetische Schema-/Validator-Beispiele sind klein, kein objektklassenspezifisches 87er Payload-Schema und keine fachliche vollständige Solver-Verifikation | spätere contract compiler, reale Testfixtures, unabhängiges mathematisches Review |
| `R03-F12` | P1 | D1–D6 wurden aus dem expliziten Projektauftrag technisch berücksichtigt; vollständiger formaler Einzelentscheidungswortlaut und Signaturen fehlen hier | Decision Log/Owner: beabsichtigter Beschlusswortlaut, unterschriebene Regelstände |
| `R03-F13` | P1 | P15 ist optional; ungeprüfte automatische OPF-Aktivierung/Ersetzung von LF widerspricht Scope | Model/Method Owner: Bedingung und LF-Kappungsnachweis |
| `R03-F14` | P1 | Original-QA/Evidence-Owner-Signoff und unabhängiger Organisationsreview fehlen weiterhin | Independent Auditor/Approver: signierte Freigabe und Review-Evidence |

Alle Findings bleiben `OPEN_FOR_FUTURE_QUALIFICATION`; sie sind **keine Blockade dieses nichtnormativen Forschungs-Branches**, verhindern jedoch ausdrücklich den Übergang zu einem realen produktiven IoSN-Daten-/Methodikvertrag.

## 4. Technische Reviewdetails

### 4.1 Abdeckungs- und Modellgrenzen
Die `input_contract_catalogue.csv` spiegelt für jedes Objekt Baseline-Properties und MA01-SR-Verknüpfung. Die neuen `expected_attributes_proposed`, `producer_step_proposed`, `consumer_steps_proposed` sind **zusätzliche Forschungszuordnungen**, deren Feindimensionierung/Mehrfachverwendung noch Ownervalidierung benötigt. **35/35 Producer-Abdeckung** beweist nur die Existenz einer vorgeschlagenen Erzeuger-Operation; `P14_PRE_EXPANSION_BASELINE_EXTRACTION_PROPOSED` und `P16_OWNER_RULE_RESOLUTION_PROPOSED` sind explizit nicht als tatsächlich verfügbar eingestuft.

Der Transformationskatalog erfasst auch nicht-ETL-Aufgaben wie LP-Stufen, Vergleichsdesign und unabhängigen Review. Das ist notwendig, damit kein modellinternes Resultat als direkt verfügbarer externer Datensatz fehlklassifiziert wird. Alle referenzierten `MLR03-I-...`-IDs sind nur zusätzliche logische Handover-Typen und verletzen die ursprüngliche Anzahl von 87 nicht.

### 4.2 Konkrete Negativtests
`invalid_weight_mismatch`: `WEIGHT_SHARED`/Normierung; `invalid_missing_weather_case`: CY-Vollständigkeit; `invalid_non_utc_offset`: UTC-String; `invalid_overlap`: Intervallüberschneidung; `invalid_missing_source_release`: FK; `invalid_unit_dimension`: MW≠Energie; `invalid_missing_provenance`: fehlendes Lineage-Feld; `invalid_production_unqualified`: reale Release-Assertion bei fehlenden Originalhashes; `invalid_data_definition`: Definitions-FK; `invalid_duplicate_instance_id`: PK; `invalid_missing_derived_run`: Run-FK; `invalid_transform_reference`: Spec-FK; `invalid_missing_numeric_weight`: unbekanntes synthetisches Gewicht; `invalid_synthetic_release_claim`: verbotene Freigabe des synthetischen Fixtures. 14 Negativfälle wurden durch die im Erstellungsprozess ausgeführten In-Memory-Assertions jeweils erkannt, der Positivfall passierte dieselben Checks.

**Nicht getestet:** echte PECD/PEMMDB-/DFT-/H2-Dateien; UTC-/DST-Konvertierung aus Source Files; PTDF/LODF-Kalibration; Solverfeasibility und bilaterale Modelläquivalenz; produktive Wirtschafts-/KPI-Formeln. Für diese Klassen ist `TEST_NOT_EXECUTED`, nicht `PASS`, zu protokollieren.

### 4.3 Reproduzierbarkeit
Die logischen Datenverträge sind jeweils in Markdown/CSV textbasiert reproduzierbar und Git-versioniert. `synthetic_contract_examples/validate_examples.mjs` benötigt nur Node.js 18+. `synthetic_validation_results.json` kennzeichnet seinen tatsächlichen in-memory-Ausführungsumfang. Kein CI-Workflow oder originaler Datenlauf wurde von diesem Forschungspaket ausgeführt.

## 5. Disposition
**Research deliverables:** `COMPLETE_AS_NON_NORMATIVE_CONTRACT_PROTOTYPE` – alle geforderten Dokument-/Katalog-/Beispieltypen und alle Baseline-IDs vorhanden; 18/18 Schritte durch Vertragsentwürfe abgedeckt.

**Fachliche Implementierungsreife:** `BLOCKED_PENDING_METHOD_OWNER_DATA_RELEASE_ORACLES` – keine normative Sprache, kein freigegebener Data Standard, keine Originaldatenqualifikation und keine methodische Endabnahme. Historische O26-Parameter wurden nicht zu einem Produktionsprofil befördert.

**Abschluss ohne Merge:** Separater Research Branch und Draft PR zur nachvollziehbaren Konsultation. Originale BUNDLE-/MA-Daten und andere ML-Workstreams werden nicht verändert; ML-R01, ML-R02 und ML-R04 werden weder vorausgesetzt noch entschieden.

## 6. Empfohlene spätere Review-Stufen (nicht in diesem Auftrag ausführen)
1. Methodology-/Data-Owner liefern echte Freigabe- und Dateievidenz einschließlich CY-Gewichten, 2035-Netzbasis, Herkunfts-/Versionstabelle.
2. Fachowner präzisieren Transformationsorakel, KPI-Definitionen, zulässige Freiheitsgrade und ursprüngliche SR-Traceability.
3. Kompatibilitäts-/Solvergruppen führen reale, dimensions-/netz-/mathebasierte Positiv- und Negativkonformitätstests je Modellsystem aus.
4. Externer unabhängiger Reviewer prüft Ergebnisse **und** Input-/Run-Evidence, danach getrennte Gate-Entscheidung.

**Keine dieser Stufen gilt durch dieses Forschungsdokument als gestartet oder bestanden.**
