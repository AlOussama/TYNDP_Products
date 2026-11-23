# ML-C19/10 – CSNF-Architekturen A/B/C und Nullhypothese H0
Status NON-NORMATIVE, Stand 2026-11-23. Gleiche SLR01–42, NFR01–18, RC01–10 und K01–17 als Bewertungseinheit. Kein bindender Architekturentscheid.

## Varianten
**A Eigenständiger Kern:** C1–C9 getypte semantische Rollen, RuleSet CSNF-R0, optionale Profile und Adapter. Plus: kleiner unabhängiger Sprachumfang, klare A/G-/Status- und Observable-Logik, bewahrt externe Modelling Freedom. Minus: neues Governance-/Typesystem und Versionierung müssen erst implementiert/bewiesen werden.
**B KerML/SysML-basierte CSNF:** SysML Part/Port, Requirement/Constraint, VerificationCase, KerML Type/Feature/Relationship/Namespace; spezialisierte Energy Contract Library + Profile. Plus: formell definierte Mechanismen, Austauschstandard und tooling. Minus: großer semantischer Surface, Autorenschulung, unerforschte Normalform-, Unit-/Governance-/Ablationsregeln, mögliche ungewollte interne Structure-Präsuppositionen.
**C Föderierte Kernreferenz + standardbezogene Views:** native Source GEMS/mathspec/SysML bleibt, gemeinsame minimale Contract-Semantik mit Mapping und verzugsfreien Roundtrip-Verlustdiagnosen. Plus: Wiederverwendung vorhandener Modelle, fachliche Unabhängigkeit, flexible Views. Minus: Mapping-/Versionierungs- und Cross-tool-Regressionen; ohne irgendeinen minimalen Kern kein stabiles gemeinsames Vergleichskriterium.
**H0 Bestehender Standard mit sehr kleinem Profil:** insbesondere SysML/KerML; prüfe, ob ein kleiner Profile-Footprint alle externen Pflichtdaten und Status/Variation/Evidence verlustfrei abdeckt, ohne komplementäres kanonisches Modell. Nullhypothese ist **nicht widerlegt**; dazu fehlt ein ausgeführtes E2-audit/Unit-/Port-/KPI-Roundtrip und kontrollierte Authoring Studie.

## Kriterienvergleich: qualitative, evidenzgetrennte Vorprüfung
| K | A Core | B KerML/SysML | C Federated | Evidenz-/Validierungsgrenze |
|---|---|---|---|---|
| K01 Study expressiveness | designed | profile-needed | core-needed | RC08–10 noch nicht nativ |
| K02 External behaviour | designed explicit | standards+profile | profile mapping | keine A/G-E2E-Tests |
| K03 Modelling Freedom | protected by spec | needs external-only discipline | protected if core audited | forced choice count zunächst design-level |
| K04 Tool agnosticism | semantic IR independent | OMG model/platform independent notion | adapters needed | zweiter Interpreter nicht ausgeführt |
| K05 Formulation independence | outside impl | possible by Profile | naturally variant adapters | E4 nur extern |
| K06 Model diversity | variation registry | profile for variation | cross-native sources | keine Modelle ausgeführt |
| K07 Robustness | ComparisonContract fields | profile | canonical views | keine R1-R4-Studie |
| K08 Precision | scoped typed predicates | formal type semantics | mapping risk | Formalisierung Lücken |
| K09 Formal checks | proposed validators | Metamodel constraints | mapping plus core checks | kein CSNF-Paket |
| K10 Domain semantics | profile-driven | library/profile | GEMS data + profiles | H2/EV native nicht belegt |
| K11 Data/process/output | typed relations | SysML trace/views | source adapters | fehlende Realdata |
| K12 Simplicity | small candidate, not measured | largest inherited graph | core+adapters complex | Autorenaufwand unbekannt |
| K13 Reuse | new core/API | strong standard reuse | strong source reuse | keine Cross-UC runs |
| K14 Interoperability | new adapters | standards alignment | central requirement | roundtrips nicht durchgeführt |
| K15 Governance | explicit authority | controlled metadata profile | cross-source ledger | Owner-Autorität offen |
| K16 Tooling maturity | none for new core | pilot implementations present | multiple existing tools | kein nativer C19 Run |
| K17 Authoring effort | UNKNOWN | UNKNOWN | UNKNOWN | human blind trial REQUIRED |

## CSNF-spezifische Metriken und vorläufiger Status
M01 Kernrollen = 9 Forschungsfamilien (05), nicht minimal bewiesen. M02 normalisierbare SLR-Anteile = NOT_MEASURED. M03 Pflicht-/Source-Erhaltung = DESIGNED, NOT_VERIFIED. M04 Zusatztypen/-operatoren = nach ML-C20 Profilfreeze zählen. M05 negative Mutations-Erkennungsquote = erst mit ausführbarem Validator. M06 Export-/Import-Verlust = NOT_TESTED. M07 Nfr Idempotenz = theoretische Invarianten, formal engine nicht implementiert. M08 gezwungene interne Entscheidungen = 0 **Design-Intent** im C1–C9-Entwurf, nicht empirisch. M09 Syntax-/Autorenzahl = NOT_MEASURED. M10 Performance/Terminationsbeweis = nur bedingt, siehe 07. Keine numerischen Gesamtscores ohne Testbasis; K02–K09 als nicht kompensierbare Gates (ML-C18/13).

## Forschungsentscheidung (bedingt)
Bevorzugte **nächste Experimentreihenfolge**, keine Wahl einer DSL: minimalen A-Kern als Referenz-Hypothese nutzen; B (KerML/SysML Profil) als ernsthafte H0-Konkurrenz auf identischen Fällen prototypisieren; C über Import/Export experimentell testen. Die Existenz von A als *semantischer Referenz* ist logisch mit C vereinbar, aber C ist ohne gemeinsamen Source-/Status-/Observable-Nenner nicht sinnvoll prüfbar. Definitive Komplexitäts-Rangfolge A<B<C **nicht belegt**. Vergleich nach gemessener Ausdrucksstärke, Audit-Roundtrip, Forced-Decision-Count, Autorenaufwand und Code-/Rule-Surface erneut öffnen.

## Architektur-Entscheidungsbedingungen für ML-C20/C21
A nur akzeptieren falls NFR01–18 und RC negative witnesses bestehen; B bevorzugen falls CSNF-Pflichten im klaren KerML-Profil und kleineren implementierten + kognitiven Kosten abbildbar; C nur wählen falls kontrollierte Adapter Mappings semantische Verluste erkennen und unverlierbare AuthorityRecords liefern. Unnötige neue Sprache vermeiden; kein Solver-/Python-/GEMS-Ausführungspflichtkern.
