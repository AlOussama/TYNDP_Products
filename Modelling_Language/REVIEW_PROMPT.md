# Reviewauftrag: Modelling Languages & Interoperabilität für TYNDP und NEP

**Status:** Arbeitsauftrag / Review-Prompt (keine vorweggenommene Architekturentscheidung)  
**Repository:** AlOussama/TYNDP_Products  
**Zielordner:** Modelling_Language/  
**Sprache der Ergebnisse:** Deutsch; fachliche Begriffe und Quellen in Originalsprache  
**Review-Stichtag:** Ausführungsdatum des Reviews; Versionen und Veröffentlichungsstände explizit dokumentieren

## 1. Rolle und Ziel

Agiere als unabhängiges Review-Team aus (a) Senior Energy System Modelling Expert für gekoppelte Strom-, Wasserstoff- und Wärmesysteme, (b) TYNDP-/IoSN-/CBA-/NEP-Methodikexperte, (c) Software-/Datenarchitekt für Modellierungssprachen, Compiler, Interoperabilität und Data Governance sowie (d) kritischem wissenschaftlichem Reviewer.

Führe ein evidenzbasiertes, nach Möglichkeit reproduzierbares Review der vorhandenen Analysen, Berichte, Folien, Codebeispiele und Architekturhypothesen zu formalen Energiesystem-Modellierungssprachen durch. Reproduziere die bisherige Empfehlung nicht unkritisch. Identifiziere Fehler, Begriffsunschärfen, Auslassungen, unbewiesene Behauptungen, Implementierungsrisiken und alternative Architekturentscheidungen.

**Leitfrage:** Welche minimale gemeinsame, technisch durchsetzbare Spezifikation benötigt ein TYNDP-/NEP-Planungsprozess, um Daten und Modelle zwischen heterogenen Tools interoperabel und vergleichbar zu machen, ohne die methodisch wertvolle Unabhängigkeit der Tools zu verlieren?

Unterscheide strikt:
1. Requirements Clarification: Was muss ein Planungsprozess normativ/fachlich leisten?
2. 1:1 Translation: Bleibt die mathematische und semantische Bedeutung bei der Konvertierung erhalten?
3. Interoperation: Können heterogene Tools und Transformationsketten die Planungsfrage bearbeiten und die Ergebnisse belastbar vergleichen?
4. Conformance: Interpretieren unabhängige Engines dieselbe freigegebene Formulierung korrekt?
5. Robustness: Bleibt eine Planungsentscheidung bei plausiblen Methoden-, Modell-, numerischen und Zukunftsvarianten stabil?

## 2. Ausgangshypothesen – ausdrücklich zu falsifizieren

Behandle folgende Aussagen aus den bisherigen Diskussionen nur als Hypothesen:

- H1: Architektur A+ (minimales gemeinsames semantisches Daten-/Komponentenmodell + Methodenbeschreibungen + Planning/Comparison Contract + eigenständige Modellierungstools) ist für methodische Robustheit im TYNDP/NEP grundsätzlich besser geeignet als eine einzige verpflichtende Mathematik.
- H2: Architektur B (eine gemeinsame vollständige mathematische Referenz, z. B. GEMS, mehrere Interpreter/Solver) maximiert die Prüfung der Implementierungskonformität, aber kann gemeinsame fachliche Modellfehler nicht selbst aufdecken.
- H3: B+ kombiniert die formale Referenz aus B mit ausdrücklich zugelassenen Alternativmethoden; sie könnte in bestimmten regulatorischen oder standardisierten Prozessen auch A+ überlegen sein.
- H4: GEMS ist als verpflichtende Austausch-Normalform möglicherweise über-spezifiziert, als ausführbare LP/MILP-Modellierungssprache aber nicht notwendigerweise. Gleichzeitig könnten Planungsprozessanforderungen und Transformationssemantik unter-spezifiziert sein.
- H5: Eine reduzierte Normalform der Komponenten (Bus/Balance, Load, Generator/Source, Storage, Line, Link, Converter) ist ausreichend. Prüfe, ob dieses Set wirklich minimal, eindeutig, erweiterbar und für sektorübergreifende Anwendungen sinnvoll ist. Prüfe insbesondere Generalisierungen auf Balance, Node, Port, Process, Connection, Storage und externe Netzprofile.
- H6: Ein direkter Modellsprache-zu-Solver-Compiler kann den mathematischen Modellgenerator von PyPSA, Antares, Sienna oder PLEXOS teilweise ersetzen, nicht aber zwangsläufig ein vollständiges Simulations- und Planungswerkzeug.
- H7: Eine fehlerhafte gemeinsame Referenzmathematik kann denselben Fehler in alle Interpreter propagieren; umgekehrt kann ein datenorientierter Austausch stillschweigend mathematische Unterschiede erzeugen.
- H8: Vergleichbare Ergebnisse erfordern mehr als identische CSV/YAML/JSON-Daten oder gleich benannte KPI: Systemgrenzen, Formeln, Einheiten, Szenariogewichte, Referenzfälle, Aggregationen und Provenienz müssen passen.

Formuliere pro Hypothese: stärkstes Argument dafür, stärkstes Gegenargument, notwendige Evidenz, Urteil (bestätigt / eingeschränkt / widerlegt / offen), Sicherheitsgrad.

## 3. Repository- und Quelleninventur

Prüfe vor inhaltlicher Bewertung alle verfügbaren Inputs. Das Repository besitzt auf dem geprüften Stand einen kanonischen IoSN-Forschungsstrang:
- README.md und docs/REPOSITORY_AUDIT.md
- docs/current/ mit IoSN-Band I (wissenschaftliche Methodik), Band II (PyPSA-Implementierung), Wetterjahrauswahl und weiterem Bericht
- src/tyndp_reduce/, tests/, examples/, tools/
- provenance/README.md, docs/archive/, artifacts/, results/synthetic/

Wichtige Einschränkung der vorhandenen Forschung: IoSN-Nachbildung ist als Forschungsprototyp / IoSN-near gekennzeichnet; synthetische Ergebnisse sind keine unabhängige ENTSO-E-Verifikation. Eine reale PyPSA-End-to-End-Integration wurde im bestehenden Audit als offen bezeichnet. Prüfe die jeweils aktuellen Dateien und den HEAD-Commit, bevor Du den Status bestätigst.

Zusätzliche primäre Review-Inputs sind die bisherigen ChatGPT-Analysen zu GEMS, CESM, INES, SiennaSchemas, mathspec/MSML, CIM/CGMES, IAMC und OEO sowie die Präsentation „Interoperabilitaet_TYNDP_NEP_Architekturen_Aplus_B_Bplus.pptx“. Diese Inputs liegen nicht zwangsläufig im Repository. Wenn sie nicht zugänglich sind, kennzeichne sie als nicht vorliegend und arbeite mit den verfügbaren Hypothesen weiter; erfinde keine Folieninhalte oder Zitate.

Erstelle ein Input-Inventar mit Datei/URL, Rolle (normativ, dokumentativ, experimentell, abgeleitet), Version/Commit, Datum, Zugriffsstatus und Vertrauenswürdigkeit. Unterscheide aktuelle kanonische und archivierte/duplizierte Repository-Dateien.

Nutze möglichst Originalquellen: ENTSO-E/TYNDP (Scenario Building, IoSN, CBA, Projektbewertung), deutsche NEP-/BNetzA-Dokumente und Primärdokumentation/Repositories von GEMS, G-PST CESM, INES, SiennaSchemas, mathspec, BlockScience MSML, CIM/CGMES, IAMC/pyam und OEO. Prüfe den aktuellen Veröffentlichungsstand; kennzeichne Konsultationsentwürfe ausdrücklich und verwechsle diese nicht mit finalen verbindlichen Methoden. Quellen mit konkreter Version, Datum, URL und möglichst Dokumentabschnitt nachweisen.

## 4. Process-First Analyse

Rekonstruiere die fachlichen Prozessketten:
A. TYNDP Scenario Building: Narrative → techno-ökonomische Annahmen → Regionalisierung → Wetter-/Last-/RES-Profile → sektorübergreifende Szenariodaten.
B. Identification of System Needs (IoSN): Eingangsdaten → Markt-/Energiesystemrechnung → Wetterauswahl → Netz-/Zonenaggregation → Investitions-/Bedarfsoptimierung → kritische Systembedarfe.
C. TYNDP Cost-Benefit Analysis: Referenzsystem, Projektfall und Szenarien → Markt-/Netz-/Redispatchmodelle → Indikatoren (mindestens B1 und B6) → Bewertung.
D. Deutscher NEP: Szenariorahmen → Regionalisierung/Marktmodell → Netzanalyse/N-1 → Maßnahmenidentifikation und -prüfung.
E. Optional OSM: Kläre erst die Bedeutung (OpenStreetMap, Operational Scenario Modelling oder anderer Kontext), bevor konkrete Anforderungen behauptet werden.

Erfasse jede Tool-/Datenübergabe in einer Matrix: Quelle, Ziel, Modellgranularität, Semantik, Transformation, verantwortliche Methodik, zulässiger Informationsverlust, Validierung, Auswirkung auf CBA/Investitionsentscheidung. Markiere Prozessschritte, deren Verhalten keine der betrachteten Modellierungssprachen vollständig abdeckt.

## 5. Normativer und technischer Anforderungskatalog

Prüfe die früheren 14 Requirements R01–R14 und die verdichteten K01–K12 auf Redundanz, Messbarkeit, Vollständigkeit und Widersprüche. Erstelle eine neue konsolidierte Liste mit:
ID, präziser Muss-/Soll-Aussage, Begründung, betroffene Prozessschritte, Pflicht/Option, Akzeptanzkriterium, überprüfbarem Test, Eigentümer, unterstützendem Standard, Implementierungslücke und Priorität.

Pflichtdimensionen:
- komponentenübergreifende Identitäten, Ports, Commodities, physikalische Bilanzgrenzen und Einheiten;
- räumliche/zeitliche Auflösung, Zeitdauern, repräsentative Perioden, Wetterjahre, Szenariowahrscheinlichkeiten;
- mathematische Semantik von Variablen, Gleichungen, Nebenbedingungen, Zielfunktionen;
- explizite Modellmethoden inkl. Defaults, unterstützte Modellklassen und Solverfähigkeiten;
- Transformationen/Mapping und Erhaltungs-/Qualitätskriterien (Netzreduktion, Zeitaggregation, CGMES → Marktmodell);
- bidirektionale Konvertierung, Capability/Gap Reports und Verlustklassifikation;
- Ergebnis-/KPI-Semantik (Systemkosten, Preise, Emissionen, Curtailment, Redispatch, SEW und Versorgungszuverlässigkeit);
- Vergleichbarkeit, Konformität, Unsicherheits-/Robustheitsauswertung;
- Anforderungen an Prozessabläufe, Referenz-/Projektfälle, Methodenfreigabe und Auditierbarkeit.

Trenne „gleiche Daten“, „gleiche Mathematik“, „gleichwertiges Verhalten“ und „vergleichbare Planungsfrage“. Ein gültiges Schema ist kein mathematischer Äquivalenznachweis.

## 6. Tiefenreview der Kandidaten

Untersuche einzeln: GEMS, G-PST Common Energy System Model (CESM), INES/ines-spec und deren Konverter, SiennaSchemas, energy-models/mathspec, BlockScience MSML, CIM/CGMES, IAMC/pyam und Open Energy Ontology. Ergänze andere gut begründete Kandidaten, ohne Datenstandard, Ontologie, DSL, Simulator und Solver unkritisch als gleichartige Produkte zu bewerten.

Für **jeden** Kandidaten:
1. Zweck, Architektur, formales Ausdrucksvermögen, Serialisierung und Validierung;
2. welche Requirements nativ, über Erweiterung oder gar nicht gedeckt sind;
3. Unterschiede zwischen Schema-Gültigkeit, Semantik, ausführbarer Formulierung und End-to-End-Prozess;
4. Zeit-/Szenariobehandlung und Sektorkopplung;
5. Erweiterbarkeit, Versions-/Governancekonzept, Reife, Tooladapter und konkrete Grenzen;
6. welche Änderungen für A+, B und B+ nötig wären – mit Machbarkeit, Aufwand und Risiken;
7. Primärquellen mit Release/Commit und Gegenbeispielen.

Verifiziere explizit: Reichweite von GEMS-Taxonomien, Views, Metriken und Workflows; reale Interpreterabdeckung (Antares/GemsPy); GEMS-Ausdrucks-/Einheiten- und Cross-Szenario-Funktionen; CESM-Referenzintegrität und Methodenattribute; INES-Konvertierungsverluste; SiennaSchemas-Versionierung; Unterschied zwischen energy-models/mathspec und BlockScience MSML. Sage nie „unterstützt“ aufgrund eines angekündigten Roadmap-Features.

Liefere eine Requirements-×-Kandidaten-Matrix mit Kategorien „nativ/nachgewiesen“, „teilweise“, „nur mit Erweiterung“, „nicht vorgesehen“, „unbekannt“. Jede starke Bewertung braucht eine Fundstelle. Ergänze mindestens zwei Gewichtungsszenarien (robuste CBA/IoSN-Interoperation vs. mathematische 1:1-Konformität), Sensitivitätsanalyse und Warnung vor Scheingenauigkeit einer Summenpunktzahl.

## 7. Kritisches Designreview: „GEMS ist über-spezifiziert“

Zerlege die These:
- Über-Spezifikation relativ zu **welchem** Vertrag: Datenaustausch, Referenzmathematik oder gesamter TYNDP-Prozess?
- Welche Mathematik darf für einen minimalen gemeinsamen Austausch entfallen, ohne implizite Modellierungsentscheidungen in Adapter/Compiler zurückzuverlagern?
- Wann ist ein Core Component Model sinnvoll, wann eine ausführbare Mathematical Normal Form?
- Was ist die minimale **semantisch ausreichende** Menge an Komponenten, Ports und Größen? Ist „Line“ eigenständig nötig oder CGMES-Spezialisierung eines Link?
- Wie werden Modellidentität, Methodenidentität und Capability des Tools getrennt?
- Kann eine Taxonomie zu einem normativen Method Contract ausgebaut werden, ohne GEMS zu überladen?
- Welche Verweise auf externe Daten-/Netzprofile sind erforderlich?
- Welche Planungsanforderungen sollten in einem separaten, versionierten Planning Requirements & Methodology Contract stehen und welche unmittelbar in GEMS?
- Welche Vor- und Nachteile hat ein GEMS-zu-Solver-Compiler für die Existenzberechtigung von PyPSA, Antares, Sienna und PLEXOS?
- Welche systematischen Common-Mode-Fehler entstehen, wenn alle Tools dieselbe fehlerhafte Mathematik nutzen?
- Wie wird die Unabhängigkeit alternativer Modellierungsansätze tatsächlich nachgewiesen?

Entwerfe mindestens zwei alternative minimale Metamodelle (z. B. sieben benannte Komponenten vs. generische Port/Balance/Process/Storage/Connection-Klassen). Vergleiche Ausdrucksstärke, Erweiterbarkeit, Verlustgefahr, Implementierungskosten und Prüfverfahren. Verwechsle syntaktische Kanonisierung nicht mit bewiesener mathematischer Gleichwertigkeit.

## 8. Architekturen A, A+, B, B+ – ohne vorgegebene Siegerarchitektur

Definiere die Architekturen unabhängig voneinander und widerspruchsfrei:
- A: gemeinsamer Datenaustausch, toolinterne Mathematik, nur begrenzte verbindliche Semantik;
- A+: gemeinsamer **normativer semantischer Kern**, Methoden-/Transformationsdeklaration, Planning & Comparison Contract, unabhängige Toolmathematik;
- B: vollständige freigegebene Referenzmathematik, mehrere unabhängige Interpreter/Compiler/Solver und Konformitätstests;
- B+: gemeinsame Referenzmathematik plus explizite, zugelassene unabhängige Modellvarianten, Conformance- und Robustness-Mode.

Prüfe, ob A+ und B+ tatsächlich Alternativen, komplementäre Profile oder unterschiedliche Governance-Stufen sind. Vergleiche:
Tool-/Vendor-Neutralität; mathematische Eindeutigkeit; Semantik; Datenverlust; Zeit- und Raumaggregation; Migrationsaufwand; Programmier- und Integrationsaufwand; Governance; Prüfbarkeit; unabhängige Modellrisiken; CBA-/IoSN-Robustheit und Schutz vor versteckten Defaults.

Erstelle für jede Architektur ein High-Level-Diagramm sowie „was wird verpflichtend gleich gehalten / was darf variieren / was wird dadurch überhaupt getestet“. Trenne Solverdiversität, Implementierungsdiversität, mathematische Methodendiversität und Szenariodiversität.

Bewerte den möglichen Fehler „gleiche Ergebnisse = robuste Planung“ kritisch. Ein gleiches LP mit verschiedenen Solvern prüft keine Modellstrukturunsicherheit; verschiedene Methoden sind nicht automatisch vergleichbar. Erkläre Unterschiede zwischen robustness, reproducibility, mathematical equivalence, numerical stability und decision robustness.

## 9. Verpflichtende High-Level-Use-Cases und Gegenbeispiele

Für jeden Use Case: Planungsfrage, Input/Output Contract, Gemeinsamkeiten, zugelassene Variationen, Transformationen, KPI, Fehlermöglichkeiten, erwartete Architektur-Eignung und Prüfplan.

UC1 – TYNDP-CBA eines Interkonnektors, mit/ohne Projekt, B1/SEW: Vergleich mehrerer Marktmodelle und klare Behandlung von Methodendifferenzen; Daten- und Referenzfallharmonisierung. Quellendefinitionen der B1-Methodik verifizieren.
UC2 – B6/Versorgungssicherheit: geeignete Wetter-/Monte-Carlo- und Adequacy-Auswertung versus repräsentative Wetterjahre; exakte TYNDP-Methodik und Gültigkeitsstand prüfen.
UC3 – IoSN: unterschiedliche Wetterjahrauswahl, räumliches Clustering und Aggregation, Investitionsoptimierung; Erhalt kritischer Engpässe, Knotenbilanz und Systembedarfsrangfolge. Nutze die Repository-Forschungsprototypen nur mit eindeutiger Kennzeichnung „synthetisch / IoSN-near“.
UC4 – Deutscher NEP: Szenario → Markt → nodale Einspeisungen → CGMES/AC-Netz → N-1 → Netzausbauoptionen; prüfe, welche Teilmodelle überhaupt mathematisch 1:1 übertragbar sind.
UC5 – Speicher: zyklischer vs. freier terminaler Ladezustand, identische Komponentenparameter. Zeige, dass Dateninteroperabilität mathematische Vergleichbarkeit nicht garantiert.
UC6 – Leitung/Link: Transport, DC/PTDF und lineare Verluste; teste 1:1-Konvertierung, stillschweigenden Informationsverlust und unterschiedliche methodische Gültigkeitsbereiche.

Kennzeichne alle konstruierten Zahlen sichtbar als illustrative Rechenbeispiele. Behaupte keine tatsächlichen ENTSO-E/TSO-Ergebnisse ohne Datenbeleg. Untersuche insbesondere die Umkehr einer Projektentscheidung unter alternativen, zulässigen Modellannahmen.

## 10. Review-Runden und Fehlerkatalog

Führe mindestens fünf Review-Runden durch:
1. Requirements Clarification: Lücken, Konflikte, Nichtprüfbarkeit, Quelle/Fassung/Geltungsbereich.
2. 1:1 Translation: Verlustfreie Übertragung von Daten und Mathematik; Round Trip, nicht unterstützte Funktionen, implizite Defaults.
3. Interoperation: Mehrstufige Markt-Netz-CBA-Ketten, Mapping, Provenienz, referenzierte Methoden.
4. Independent Validation/Robustness: Conformance Mode gegen Robustness Mode, Ausreißeranalysen, Common-Mode-Risiken.
5. Red Team: Suche aktiv nach Szenarien, in denen die bevorzugte Architektur ungeeignet, überkomplex oder regulativ unzulässig wäre.

Nutze ein Finding-Register mit ID, Schweregrad (Critical/High/Medium/Low), Kategorie, präziser Behauptung, Beleg, Gegenbeleg, Konsequenz für die Planung, empfohlener Korrektur, offener Frage und Vertrauensniveau. Kritische Findings müssen in Entscheidung und Roadmap nachvollziehbar auftauchen.

## 11. Optionaler technischer Proof of Concept

Erstelle Code nur, wenn er die Reviewaussagen überprüfbar verbessert, z. B.:
- maschinenlesbares Minimal-Schema für Komponenten, Ports, Einheiten, Zeit/Szenarien;
- Method Profile für zwei Speicherformulierungen;
- Planning/Comparison Contract mit Referenz-/Projektfall und KPI-Definition;
- Validierungsbeispiel mit erlaubter, verlustbehafteter und abgelehnter Konvertierung;
- Testfälle für Schema- und Konsistenzprüfung (ggf. JSON Schema, LinkML, Python).

Lege Quellcode ausschließlich unter Modelling_Language/prototypes/ und zugehörige Tests unter Modelling_Language/tests/ ab. Nutze möglichst wenige Abhängigkeiten, führe Tests wirklich aus, dokumentiere Environment und Resultate. Keine angeblichen Multi-Tool-Validierungen, falls Antares/GemsPy/PLEXOS oder reale Netzdatensätze nicht verfügbar sind. Keine komplexe produktive Implementierung nur um ein Diagramm zu illustrieren.

## 12. Deliverables und Repository-Organisation

Arbeite in einem eigenen Branch, idealerweise review/modelling-language-<Datum>, und öffne einen **Draft Pull Request** zur Prüfung. Verändere keine vorhandenen kanonischen IoSN-Methodiken oder Python-Module außerhalb des neuen Ordners. Keine stillen Überschreibungen, keine Duplikation ganzer Altberichte ohne Notwendigkeit.

Vorgeschlagener Zielbaum (nur tatsächlich erzeugte Artefakte anlegen):

Modelling_Language/
  README.md                                  # Navigation, Status, wichtigste Entscheidungen
  REVIEW_PROMPT.md                           # dieser Arbeitsauftrag
  review/
    inventory.md                             # analysierte Inputs und Versionen
    findings.md                              # priorisierte Feststellungen und Korrekturen
    claim_evidence_matrix.csv                # Behauptung → Quelle → Verifikationsstatus
    review_report.md                         # zusammenfassendes Fach- und Architekturreview
  analysis/
    process_interoperability.md              # TYNDP/IoSN/CBA/NEP-Prozessketten
    requirements.md                          # konsolidierte, prüfbare Requirements
    candidates.md                            # vergleichende Technologiebewertung
    architectures.md                         # A/A+/B/B+ inkl. Gegenargumenten
    gems_normal_form.md                      # vertiefte kritische Analyse der These
    use_cases.md                             # mindestens UC1–UC6
    recommendation_adr.md                    # Entscheidung und nachvollziehbare Alternativen
    roadmap.md                               # realistische priorisierte Umsetzung
  sources/
    bibliography.md                          # Quellen und geprüfte Versionsstände
  prototypes/                                # optional, nur funktionsfähige Prototypen
  tests/                                     # optional
  presentations/
    architecture_review.pptx                 # nach Review überarbeitete Präsentation
  reports/
    architecture_review.pdf                  # optional aus kanonischem Markdown generiert

Markdown ist die führende, diff-freundliche Quelle. PDF/PPTX sind darauf abgestimmte Veröffentlichungsartefakte; Quellmaterial muss rekonstruierbar sein. Präsentation: klare Storyline Prozesse → Interoperationsbedarf → Requirements → Kandidaten → Architekturvergleich → Use Cases → offene Probleme → Empfehlung; gut lesbar, kein überladener Tabellenkleindruck, deutliche Quellen-/Evidenzangaben. Bei fehlenden Export-/Renderfunktionen keine Artefakte vortäuschen.

## 13. Qualitätsgates und Abnahmekriterien

Ein Review ist erst abgeschlossen, wenn:
- alle zugänglichen Input-Artefakte inventarisiert und wichtige nicht zugängliche Inputs transparent aufgeführt sind;
- alle zentralen Tatsachen-/Produkt-/Methodenbehauptungen an nachvollziehbare Primärquellen gebunden oder als unbestätigt ausgewiesen sind;
- normative, veröffentlichte und entworfene Methoden ausdrücklich unterschieden sind;
- die Requirements und Bewertungsmatrizen intern widerspruchsfrei und nachprüfbar sind;
- mindestens eine Gegenhypothese zur favorisierten Architektur substantiell untersucht wurde;
- die Minimalkomponenten-These gegen alternative Metamodelle geprüft wurde;
- Vergleichbarkeit und Robustheit nicht mit identischer Mathematik oder identischen Daten verwechselt werden;
- IoSN-Prototyp und synthetische Ergebnisse nicht als offizielle TYNDP-Verifikation bezeichnet werden;
- jeder priorisierte Kritikpunkt einer konkreten Korrektur/Entscheidung zugeordnet ist;
- Codebeispiele, falls erzeugt, getestet und als Prototyp gekennzeichnet sind;
- Markdown-Berichte, Quellenmatrix und Folien konsistent sind.

Bewerte die empfohlene Architektur nur so stark, wie die Evidenz es zulässt. Wo Information nicht verfügbar ist, formuliere eine überprüfbare offene Frage und eine praktikable nächste Validierungsmaßnahme.

## 14. Abschließendes Ergebnisformat

Beginne mit einer Executive Summary (maximal zwei Seiten) mit:
- wichtigsten bestätigten und widerlegten bisherigen Aussagen,
- drei bis fünf architektonisch entscheidenden Findings,
- Empfehlung A+, B, B+ oder alternative Lösung samt expliziten Voraussetzungen,
- priorisierter Roadmap (Quick Wins, mittel- und langfristige Entwicklung),
- klaren Stop-/Go-Kriterien für einen kleinen TYNDP-/IoSN-/CBA-Piloten.

Lege ausführliche Evidenz und Vergleiche in die Anhänge/Einzelberichte. Beende mit einer expliziten Aussage: **Was sollte in einem gemeinsamen Standard zwingend festgelegt werden, was gehört in ein optionales mathematisches Referenzprofil, und was muss für Robustheitsanalysen bewusst unabhängig bleiben?**
