# ESM-A – European & National Planning Process Requirements

**Status:** fachliche Übergabe zur unabhängigen ESM-Vergleichsstudie, Version 0.1, 27. November 2026  
**Adressaten:** zentraler Architektur- und Vergleichschat; unabhängige Tool-Reviewer  
**Scope:** Antares/GEMS, PyPSA, PyPSA-Eur, Open-TYNDP und open_eGo/eGon; ergänzende Referenzwerkzeuge. Keine Bewertung ihrer aktuellen Implementierung als Ersatz für die hier abgeleiteten Anforderungen.  
**Repository-Ablage:** separater Dokumentationsbranch, keine Änderung an der IoSN-Implementierung, keine Solver-Ausführung.  
**Evidence cutoff:** 27.11.2026. Dokumentstände mit ausdrücklich ausgewiesenem Draft-Status werden nicht als final genehmigte Methode behandelt.

## 0. Executive Summary

Die europäischen und nationalen Planungsprozesse benötigen **kein einziges universelles Optimierungsmodell**, sondern eine interoperable Kette aus mindestens sechs unterscheidbaren Modellklassen:

1. Szenario- und Transformationsmodell: konsistente Nachfrage, Technologie-, Bestands- und Kapazitätsentwicklung, Emissions- und Politikrestriktionen.
2. Chronologisches Markt-/Betriebsmodell: zonaler oder nodaler Dispatch, Speicher, sektorale Flexibilität; bei entsprechender Fragestellung diskrete Betriebsentscheidungen und Flow-Based Market Coupling (FBMC).
3. Infrastruktur-Bedarfsoptimierung: endogene Kapazitätserweiterung bei exogen vorgegebenen oder gekoppelten Erzeugungs-/Nachfrageszenarien; Brownfield und mehrere Wetterlagen.
4. Projektbewertung: inkrementelle, referenznetz- und gegenfaktualgebundene CBA (PINT/TOOT), keine Substitution durch bloße Ausbauoptimierung.
5. Probabilistische Versorgungssicherheit: Economic Viability Assessment (EVA), Wetter-/Ausfallstichproben, LOLE/EENS und statistische Konvergenz; getrennt von deterministischer N-1-Netzsicherheit.
6. Physische Netz- und regionale Infrastrukturprüfung: AC/DC-Lastfluss, Redispatch, Sicherheits- und Stabilitätsprüfung, Gas-/H2-Hydraulik nach Bedarf, Verteilnetz- und Wärmenetzrestriktionen.

Die entscheidenden Vergleichsdimensionen sind daher **Entscheidungsumfang, Informationsstruktur, Netzphysik, Zeitkopplung, sektorale Modellgrenzen, Gegenfaktualsemantik und Evidenz**. Ein Tool, das ein Ergebnis per Datenimport oder externem Modul abbilden kann, erfüllt eine Anforderung nicht automatisch nativ. Ebenso ist ein guter Lastfluss kein Nachweis einer korrekten CBA oder ERAA.

**Empfehlung:** ein modularer Workflow mit einheitlichen Daten- und Ergebnisverträgen und prozessspezifischen mathematischen Modellen. Keine Verpflichtung auf einen Solver, keine automatische Bevorzugung eines der fünf Vergleichskandidaten. Die folgenden IDs sind die gemeinsame Referenz für spätere Capability-/Gap-Matrizen.

**Wesentliche Befunde zur Quellenlage:**

- TYNDP 2024: veröffentlichte Szenarien und Methodikberichte; IoSN/CBA-Implementierungsberichte in der Fassung für Stellungnahmen vom April 2025; übergeordnete vierte Strom-CBA-Leitlinie durch die Kommission 2024 genehmigt. Stellungnahme, Bericht und Genehmigung sind unterschiedliche Rechts-/Evidenzkategorien.
- TYNDP 2026: Strom-IoSN-Konsultationsmethodik vom Februar 2026, CBA-Konsultationsentwurf vom Dezember 2025, Szenarienentwurf 2026; ENTSOG-Methodiken Oktober 2026 nach Konsultation weiterhin als Entwürfe bezeichnet. Keine Behauptung, alle finalen Fassungen oder Resultate seien bereits bestätigt.
- ERAA 2025: amended edition nach ACER-Entscheidung 06-2026; überarbeitete ERAA-Methodik 2026 separat durch ACER-Entscheidung 04-2026. Anwendungszeitpunkt einzelner neuer Regeln nach Implementierungsplan prüfen; nicht rückwirkend dem ERAA-2025-Lauf zuschreiben.
- Deutschland: gemeinsam genehmigte Szenariorahmen Strom/Gas-H2 2025; NEP-Entwürfe 2026 und nächster Szenariorahmen 2027–2040/45 getrennt behandeln. Der nationale Netzausbau ist kein freies Greenfield-Transformationsmodell.
- PLEXOS, Antares und diverse Netzwerkzeuge sind in offiziellen Dokumenten konkret genannt; daraus folgt keine regulatorische Pflicht zu diesen Produkten. Eine vollständige versionsgebundene Reproduktion ihrer Produktionskonfigurationen ist anhand der öffentlichen Berichte nicht möglich.

## 1. Methodik, Evidenz und Geltung

### 1.1 Klassifikation

| Code | Bedeutung |
|---|---|
| L | geltendes Gesetz bzw. EU-Verordnung |
| A | genehmigte Methodik/Entscheidung bzw. verbindlicher genehmigter Rahmen in ihrem jeweiligen Anwendungsbereich |
| D | Konsultations-/Arbeitsentwurf, nicht automatisch bindend |
| B | offizieller Bericht, dokumentierte Anwendung oder behördliche Stellungnahme |
| E | offizielle Empfehlung, Strategie oder wissenschaftliche Modellbeschreibung |
| P | daraus abgeleitete Pflicht für den jeweiligen Vergleichsprozess; keine eigenständige Rechtsnorm |
| O | optionale Erweiterung, sofern für den Prozess nicht zwingend |
| F | Forschungsanforderung, methodisch interessant, noch nicht als allgemeine Produktionspflicht belegt |
| U | ungeklärt, nicht ausreichend öffentlich dokumentiert oder im vorliegenden Audit nicht abschließend verifiziert |

Ein offizielles Dokument kann mehrere Rollen haben, z. B. B hinsichtlich dokumentierter Implementierung und A hinsichtlich genehmigter Teile. Die nachfolgenden Formeln sind **eigene toolneutrale Referenzformulierungen**, nicht wörtliche Rekonstruktionen proprietärer Solver oder eine Autorisierung, die Originalmethodik zu ersetzen. Für einen konkreten TYNDP-Zyklus gelten dessen Szenarien, Referenznetz, Kandidatensätze, Parameter, Indikatoren und Übergangsregeln.

### 1.2 Abgrenzung von Aussagen

- DOCUMENTED: Quelle beschreibt Vorgehen/Funktion.
- IMPLEMENTED: konkreter Code-/Versionsnachweis vorhanden.
- REPRODUCED: unabhängiger numerischer Lauf unter gepinnten Bedingungen.
- PHYSICALLY_VALIDATED: separate physikalische Prüfung.
- OWNER_ACCEPTED: explizite Entscheidung des Projektowners.

Dieser Bericht enthält DOCUMENTED-Evidenz, abgeleitete Requirements und analytische Sollwerte; **keine reproduzierten Solverläufe, keine Produktionszertifizierung und keine Owner-Freigabe**. Angaben zu Drafts sind auf den überprüften Dokumentstand beschränkt. Keine Aussage über unveröffentlichte oder nicht verifizierte Modellkonfigurationen.

## 2. Prozess- und Quellenmatrix

### 2.1 Autoritative und operative Quellen (Europa)

Links sind Primärquellen bzw. offizielle Publikationsseiten. Versionsangaben beziehen sich auf Dokumenttitel, Datum und erkennbaren Verfahrensstatus, nicht auf den Website-Zeitstempel. Vor einem formalen Konformitätslauf sind PDF-Versionen und Hashes einzufrieren.

| ID | Prozess / Herausgeber | Version, Status | Relevanz und Quelle |
|---|---|---|---|
| S01 | EU TEN-E, gemeinsame Szenarien, Netzentwicklungspläne, CBA | Verordnung (EU) 2022/869, geltende Fassung; L | Art. 11–13 und einschlägige Anhänge; [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/869/oj?locale=de). |
| S02 | ACER – Szenarioleitlinien / Stellungnahme | Framework Guidelines 25.01.2023, ACER Opinion 05/2024; A/B getrennt | Anforderungen an gemeinsame Szenarien; [ACER-Stellungnahme](https://www.acer.europa.eu/sites/default/files/documents/Official_documents/Acts_of_the_Agency/Opinions/Opinions/ACER_Opinion_05-2024_ENTSOs_Scenarios_TYNDP_Guidelines.pdf). Leitlinienversion hier über Stellungnahme belegt, nicht separat volltextgeprüft. |
| S03 | ENTSO-E/ENTSOG Scenario Building 2024 | Final Scenario Methodology Report, Januar 2025; B | NT bottom-up, DE/GA top-down, Nachfrage- und Angebotsmodellierung; [Methodik](https://2024.entsos-tyndp-scenarios.eu/wp-content/uploads/2025/01/TYNDP_2024_Scenarios_Methodology_Report_Final_Version_250128.pdf), [Downloads](https://2024.entsos-tyndp-scenarios.eu/download/). |
| S04 | ENTSO-E/ENTSOG Scenario Building 2026 | veröffentlichter Szenarienentwurf Juni 2026; D/B | NT+ und HEV/LEV-Sensitivitäten, 2030/35/40/50; [Framework](https://2026.entsos-tyndp-scenarios.eu/tyndp-2026-scenario-framework/), [Downloads](https://2026.entsos-tyndp-scenarios.eu/download/), [Toolchain §§3.1–3.9](https://2026.entsos-tyndp-scenarios.eu/scenarios-methodology-report/toolchain/). |
| S05 | ENTSO-E TYNDP 2024 / IoSN | System Needs Methodology, 09.04.2025, Fassung für Stellungnahmen; B | Referenznetz, Marktmodelle, Zeithorizonte, Kandidaten; [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2024/foropinion/SystemNeedsMethodology.pdf), [TYNDP 2024](https://www.entsoe.eu/outlooks/tyndp/2024/). |
| S06 | ACER TYNDP 2024 | Opinion 04-2025; B | Unabhängige Beurteilung und Verbesserungspunkte, keine Gleichsetzung mit Genehmigung sämtlicher Modelle; [PDF](https://www.acer.europa.eu/sites/default/files/documents/Official_documents/Acts_of_the_Agency/Opinions/Opinions/ACER-Opinion-04-2025-ENTSO-E-TYNDP-2024-and-Infrastructure-Gaps-report-2024.pdf). |
| S07 | ENTSO-E IoSN 2026 | 25.02.2026, Konsultation bis 03.04.2026; D | Mehrzonenmodell, gemeinsame Kapazitätsentscheidung über gewichtete Wetterfälle, gekoppelte H2-/Offshore-Modellierung, Ausbau-/Filterlogik; [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf), [Konsultation](https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/). |
| S08 | ENTSO-E Strom-CBA | 4th CBA Guideline, EC-Genehmigung 26.03.2024, publiziert 09.04.2024; A | Projektindikatoren, Wohlfahrt, externe Effekte, Bewertungshorizonte; [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf). |
| S09 | ENTSO-E CBA-Implementierung TYNDP 2024 | Implementation Guidelines, 09.04.2025, Stellungnahmenfassung; B | §3.4/3.5 Referenznetze, PINT/TOOT, SoS-Kalibrierung, Markt- und Netzstudien, Annex G/H; [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2024/foropinion/CBA_Implementation_Guidelines.pdf). |
| S10 | ENTSO-E CBA-Implementierung TYNDP 2026 | Draft 16.12.2025, Konsultation bis 06.02.2026; D | §3.5 zeit-/reifeabhängige Referenznetze, projektbezogene Methodik, hybride Projekte, aktualisierte Indikatoren; [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2026/Draft_TYNDP_2026_CBA_ImpG_for_PC.pdf), [Konsultation](https://consultations.entsoe.eu/tyndp/tyndp-2026-cba-imp-public-consultation/). |
| S11 | ENTSOG TYNDP 2024 | Veröffentlichte Annex-D1/D2/D3-Unterlagen; B | H2-CBA, Infrastruktur-Gap- und Systembewertung; Methan-Systembewertung nicht mit projektspezifischer H2-CBA verwechseln; [Downloads](https://tyndp2024.entsog.eu/downloads/). |
| S12 | ENTSOG H2-CBA | CBA Methodology Report, 2024, veröffentlichte Fassung Februar 2025 nach Genehmigung; A/B | H2-Projektbewertung, Infrastruktur, Interlinkage; [PDF](https://www.entsog.eu/sites/default/files/2025-10/entsog_CBA_methodology_report_250225.pdf), [Methodologies and modelling](https://www.entsog.eu/methodologies-and-modelling). Interlinked-Modellbericht 28.04.2026 separat vom Genehmigungsstatus behandeln. |
| S13 | ENTSOG TYNDP 2026 | Annex D1, Draft post-consultation, Oktober 2026; D | H2-CBA-Implementierung, Referenz- und Projektgruppen, Stress-/Kosteneffekte; [D1](https://www.entsog.eu/sites/default/files/2026-10/TYNDP%202026%20Annex%20D1%20-%20Implementation%20Guidelines%20-%20draft%20post-consultation.pdf). |
| S14 | ENTSOG TYNDP 2026 | Annex D2, Draft post-consultation, Oktober 2026; D | H2 Infrastructure Gap Identification, Kapazitäts-/Import-/Speichersensitivitäten; [D2](https://www.entsog.eu/sites/default/files/2026-10/TYNDP%202026%20Annex%20D2%20-%20H2%20IGI%20Methodology%20-%20draft%20post-consultation.pdf). |
| S15 | ENTSOG TYNDP 2026 | Annex D3, Draft post-consultation, Oktober 2026; D | System Assessment, Gas/H2, Stressfälle, Versorgung und Infrastruktur; [D3](https://www.entsog.eu/sites/default/files/2026-10/TYNDP%202026%20Annex%20D3%20-%20System%20Assessment%20Methodology%20-%20draft%20post-consultation.pdf), [Downloads](https://tyndp2026.entsog.eu/downloads/). |
| S16 | EU Strommarkt / ERAA | Verordnung (EU) 2019/943, geändert 2024, Art. 23–25; L | Europäische und nationale Resource Adequacy, Zuverlässigkeitsstandard; [EUR-Lex konsolidiert](https://eur-lex.europa.eu/eli/reg/2019/943/2024-07-16/eng). |
| S17 | ACER/ENTSO-E ERAA | ACER Decision 04-2026 vom 17.03.2026; A; Implementierungsplan 31.07.2026; B | Methodenrevision und zeitliche Umsetzung; [ENTSO-E Revision](https://www.entsoe.eu/eraa/methodology-revision/), [ACER Entscheidungen](https://www.acer.europa.eu/documents/official-documents/individual-decisions). |
| S18 | ENTSO-E ERAA 2025 | Amended edition nach ACER Decision 06-2026, 29.04.2026; B/A hinsichtlich Entscheidung | Annex 2, EVA und probabilistische Adequacy; [Publikationen](https://www.entsoe.eu/eraa/2025/reports%26results/), [Annex 2](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/sdc-documents/ERAA/ERAA_2025/ERAA%202025%20Annex%202_Amended%20edition%20following%20ACER%27s%20decision.pdf). |

### 2.2 Nationale und regionale Quellen (Deutschland)

| ID | Prozess / Herausgeber | Version, Status | Relevanz und Quelle |
|---|---|---|---|
| S19 | EnWG | geltende Fassung; L | §12a ff. Strom, §15a ff. Gas/H2, §12i Stabilität, §14d/e Verteilnetz, §51 Monitoring; [EnWG](https://www.gesetze-im-internet.de/enwg_2005/). |
| S20 | BNetzA Szenariorahmen Strom und Gas/H2 | Genehmigung 30.04.2025; A | 2037 und 2045, abgestimmte Strom-/Gas-/H2-Annahmen; [Genehmigung/Pressemitteilung](https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2025/20250430_Szenariorahmen.html). |
| S21 | ÜNB/BNetzA NEP Strom 2037/2045 (2025) | zweiter Entwurf 2026 und Konsultation; D | Marktmodell, Regionalisierung, physische Netzplanung; [BNetzA](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/NEP/Strom/start.html), [ÜNB NEP](https://www.netzentwicklungsplan.de/nep-aktuell/netzentwicklungsplan-20372045-2025). |
| S22 | FNB/H2-Netzbetreiber/BNetzA NEP Gas und Wasserstoff | zweiter Entwurf 01.06.2026, weitere Konsultation 2026; D | Methan- und H2-Netze, Umstellungen und Transportbedarf; [BNetzA](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/NEP/Gas/start.html). |
| S23 | BNetzA Szenariorahmen 2027–2040/45 | Entwürfe Juni 2026, Konsultation ab August 2026; D | neuer Planungshorizont und sektorübergreifende Abstimmung; [Szenariorahmen](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/NEP/SR_2040/start.html). Nicht mit S20 vermischen; spätere Genehmigung hier nicht abschließend belegt. |
| S24 | BMWE Systementwicklungsstrategie (SES) | Strategie November 2024, begleitende Arbeiten 2025; E/B | gemeinsame Leitplanken, Resilienz und sektorübergreifende Transformationspfade; [SES-Dossier](https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Dossier/ses.html). |
| S25 | BMWE Langfristszenarien / Enertile | O45-Szenarien und Modellbeschreibung; B/E | kostenminimierende intertemporale Transformation, räumliche/zeitliche Auflösung und Verteilnetzapproximation; [Szenario-Explorer](https://langfristszenarien.de/enertile-explorer-de/szenario-explorer/angebot.php). Konkrete Auflösungen und Wetterbasis sind studienspezifisch. |
| S26 | BNetzA Versorgungssicherheitsmonitoring Strom | Bericht 2025, veröffentlicht 03.09.2025; B | nationales Monitoring, Zielpfad und verzögerte Energiewende, Adequacy; [Monitoring](https://bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Versorgungssicherheit/Monitoring_Strom/start.html). |
| S27 | BNetzA/ÜNB Netzreserve / Systemanalyse | 22.05.2026, Betrachtungen 2026/27 und 2028/29; B | räumlich erforderlicher Redispatch und Netzreserve, nicht identisch mit nationalem Kapazitätsmangel; [Netzreserve](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/Versorgungssicherheit/Netzreserve/start.html). |
| S28 | BNetzA/ÜNB Systemstabilitätsbericht | Bericht 2025 und BNetzA-Bewertung Juli 2025, Horizont 2027–2037; B/L (§12i) | Stabilitätsbedarf, Maßnahmen und technische Nachweise; [Systemstabilität](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/NEP/Strom/Systemstabilitaet/start.html). |
| S29 | Verteilnetzausbauplanung | §14d EnWG, aktuelle Fassung; L | regionale Szenarien, Netzausbaupläne, Flexibilität, Abstimmung; [§14d](https://www.gesetze-im-internet.de/enwg_2005/__14d.html), [§14e](https://www.gesetze-im-internet.de/enwg_2005/__14e.html), [BNetzA Verteilnetze](https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/VerteilerNetz/start.html). |
| S30 | Kommunale Wärmeplanung | WPG, geltende Fassung; L | Eignungsprüfung, Bestands-/Potenzialanalyse, Zielszenario, Wärmeversorgungsgebiete und Umsetzungsstrategie §§13–20; [WPG](https://www.gesetze-im-internet.de/wpg/BJNR18A0B0023.html). |

### 2.3 Prozessprofile: Ziel, Entscheidung und Auflösung

Notation: GF = Greenfield; BF = Brownfield; PF = Perfect Foresight über den definierten Horizont; MY = Myopic/receding horizon; E = exogen; I = endogen. PF der Jahresdispatch-Simulation ist nicht gleich intertemporaler PF über die gesamte Transformation. Simulationsmodelle können eine exogene Infrastruktur bewerten, ohne dass sie selbst deren Ausbau optimieren.

| Prozess-ID | Zielfunktion / Ergebnis | E/I und zeitlicher Entscheidungsmodus | Raum, Zeit, Unsicherheit / Netz | Quellen |
|---|---|---|---|---|
| PR01 EU-Szenarien 2024/26 | kohärente Nachfrage-/Angebots-/Emissionsentwicklung; Betriebsmodell auf Kostenminimum; Szenarioerzeugung nicht notwendig ein einziges mathematisches Optimierungsproblem | TSO-Daten, Politik und Technologietrends E; bestimmte Nachfrageflexibilitäten, Umwandlungsbetrieb I; Top-down/Bottom-up; BF/PF je Teilmodell | Länder/Marktzonen, Energiesektoren, jährliche Bestände und stündliche Profile; Wetterkonsistenz, keine allgemeine stochastische Investitionspflicht | S01–04 |
| PR02 Strom-IoSN 2024 | wirtschaftlicher zusätzlicher Austausch-/Speicher-/Infrastrukturbedarf gegenüber Startnetz | Erzeugung und Nachfrage szenariogebunden E, ausgewählte Ausbaukandidaten I; BF; horizon-/szenariospezifisch | 2030/2040/2050 je modellierter Szenariokombination; zonales Marktmodell, NTC/Transfer-Kandidaten, wetterbezogene Chronologie | S05–06 |
| PR03 Strom-IoSN 2026 | gewichtete Gesamtkosten der Ausbau- und Betriebsentscheidungen; identifizierte Bedarfe, nicht individuelle Projektgenehmigung | gemeinsamer Ausbau über Wetterfälle je Horizont, Szenariokapazitäten teilweise E, Kandidaten I; BF; mehrstufiges Screening | 2035/40/50 in der Konsultationsmethodik; mehrere Modellzonen pro Marktzone; drei gewichtete Wetterfälle, H2, Offshore-/Hybrid-Kandidaten; physische Zusatzprüfung getrennt | S07 |
| PR04 Strom-CBA 2024/26 | inkrementelle Wohlfahrt und weitere monetäre/nichtmonetäre Indikatoren; projektbezogener Vergleich | Projektstatus in den beiden Gegenfaktualen E; Betrieb I; Referenzkapazität und System-Sicherheit nach methodischer Vorgabe; BF | Markt-/Netzmodelle, Stunden/Wetterfälle und projekt-/indikatorspezifische Zusatzsimulationen; PINT/TOOT und Referenz-/Projektgruppen | S08–10 |
| PR05 H2-CBA / IGI / Gas-H2-Systembewertung | Projektmehrwert, Infrastruktur- oder Angebotslücke, Stressversorgung; getrennte Zielgrößen | Szenarien E; Projektkonfiguration E bei CBA, Kapazitätsfreigaben/Sensitivitäten bei IGI; Betrieb I; BF | zonale/regionale Gas-/H2-Netze, Strom-H2-Stundenmodell und Gas-Monatsmodell, Stressfälle, technische Transport- und Umstellungsrestriktionen | S11–15 |
| PR06 ERAA | EVA: wirtschaftliche Tragfähigkeit von Ressourcen; anschließend probabilistische Versorgungssicherheit | Bestand/Szenario E plus EVA-Eintritt/-Austritt/-Mothballing nach Methode I; MC-Stichproben mit wetter-/ausfallabhängigem Betrieb | europäische Marktzonen, stündliche Chronologie, wetter- und ausfallbedingte Verfügbarkeit, Austausch; LOLE/EENS | S16–18 |
| PR07 DE Szenariorahmen | genehmigungsfähige plausible gemeinsame Entwicklung, Regionalisierung und Konsistenz | Szenarien und Politik E für nachfolgende NEP; keine Pflicht zu freier Expansion aller Technologien im NEP | Bundesgebiet/Regionen und europäisches Umfeld, Zieljahre, Nachfrage- und Leistungsspitzen | S19–23 |
| PR08 DE NEP Strom | notwendige bedarfsgerechte Netzinfrastruktur und Netzsicherheit, ggf. Vergleich von Maßnahmen | genehmigter Rahmen E; Redispatch/Betrieb und Netzmaßnahmen I bzw. iterativ bestimmt, BF/NOVA-Prinzip | europäischer Markt → detailliertes deutsches Übertragungsnetz; Stunden/ausgewählte Netzfälle; AC/DC und N-1 je Planungsstufe | S19–21 |
| PR09 DE NEP Gas/H2 | bedarfsgerechte Transportfähigkeit, Umstellung, Versorgung und wirtschaftliche Maßnahmen | Szenariorahmen E; Infrastrukturmaßnahmen/Umstellungen I bzw. iterativ; BF | Fernleitungs-/H2-Netze, Spitzen-, Last- und Stressfälle, Druck/Transporttechnik bei physischer Prüfung | S19–20, S22–23 |
| PR10 SES / Langfristszenarien | volkswirtschaftlich günstige Transformationspfade, Robustheit und Infrastrukturinteraktionen | Nachfrage/Politik teilweise E, sektorgekoppelte Erzeugungs-/Speicher-/Transportkapazitäten I; BF/PF im Enertile-Referenzfall; MY als Vergleich | Europa/nationale Regionen, mehrere Jahre, stündliche Operation und ausgewählte DSO-Näherung; Szenariosensitivitäten | S24–25 |
| PR11 Nationales Adequacy-Monitoring | Risiko ausreichender Leistung und Versorgung unter Varianten | Kapazitätsannahmen und Szenarioentwicklung E/ggf. Marktreaktionen gemäß Studie; Betrieb I | europäische Kopplung, probabilistische wetter-/ausfallabhängige Lastdeckung; nicht nur deutsche Jahresenergiebilanz | S26, S16–18 |
| PR12 Netzreserve/Bedarfsanalyse | ausreichende, am Standort wirksame Redispatch-/Reserveleistung | Marktergebnis und Netztopologie E, netzwirksamer Redispatch/Reserve I; BF | kritische Stunden/Stressfälle, nodale Netzphysik, Kontingenzen, zulässige Maßnahmen | S27 |
| PR13 Systemstabilität | Frequenz-, Spannungs-, Kurzschluss- und dynamische Stabilität; Bedarf an Systemdienstleistungen | Betriebspunkte/Topologie E, Maßnahmen-/Dienstleistungsbedarf iterativ bzw. I; kein allgemeines einziges Kostenziel | dynamische Sekunden-/Subsekundenebene plus repräsentative Jahresbetriebspunkte, AC-Netz und Gerätemodelle | S28 |
| PR14 DSO-/integrierte TSO-DSO-Planung | regionaler bedarfsgerechter Ausbau und Flexibilitätsvergleich | regionale Entwicklung E; lokale Maßnahmen/Flexibilität I; BF, sequenziell/integriert | Region, Umspannwerk, MS/NS-Netz nach Bedarf; chronologische Last-/Einspeiseprofile und Spitzen; Spannung/Thermik, Netzzustände | S19, S29 |
| PR15 Kommunale Wärmeplanung | geeignete Versorgungsoptionen und Gebiete, Transformationsstrategie; Kosten/Emissionen/Risiken | Gebäude- und Nachfragebestand E, Wärmeoptionen/Netze/Umstellung I bzw. planerisch bestimmt; BF | Gemeinde/Gebäudecluster/Wärmenetzgebiet; Jahreswärme und saisonale/stündliche Last, lokale Potenziale, EE/Abwärme | S30 |

### 2.4 Ausgewählte methodische Unterschiede, die nicht verloren gehen dürfen

**Scenario Building.** Die gemeinsame 2026-Toolchain koppelt jährliche Eingangsdaten, Nachfrageprofile, Flexibilitäts- und Angebotsmodule sowie das Strom-H2-Marktmodell. Das ETM, Nachfrageprofilierung und PLEXOS übernehmen unterschiedliche Aufgaben. PLEXOS berechnet in der dokumentierten Toolchain insbesondere den stündlichen Strom-/H2-Betrieb; nicht jede fossile Nachfrage wird dort endogen optimiert. NT+ mit HEV/LEV ist anders zu verstehen als die 2024er DE/GA-Narrative. Nicht aus der Toolchain eine einzige durchgängige stochastische Dreisektor-Expansion ableiten. [S03–04]

**IoSN.** Für 2024 sind die Horizonte und Startnetze getrennt zu behandeln. Für den 2026-Entwurf sind interne Engpässe durch mehrere Modellzonen, ein gemeinsamer Ausbau über gewichtete Klimafälle, Offshore-Kopplung und die Auswahl-/Filterstufen wesentlich. Das gewichtete Erwartungskostenproblem ist nicht allein durch das Wort robust zu einem Minimax-Modell geworden. Die Kandidatengrenzen und die exakten Wettergewichte aus dem zyklusgebundenen Input übernehmen; nicht aus späteren Modellversionen ergänzen. [S05, S07]

**CBA.** Die zu prüfende Maßnahme und die übrige Infrastruktur müssen in zwei korrespondierenden Modellzuständen explizit dokumentiert sein. PINT (Put IN one at a Time) und TOOT (Take Out One at a Time) sind nicht austauschbar bei Projektinteraktion. Die CBA-Referenz ist auch nicht einfach das IoSN-optimale Netz. Reife, Inbetriebnahme und Zieljahr beeinflussen die Referenzzugehörigkeit; indikatorspezifische Anpassungen, etwa Security-of-Supply-Kalibrierung, müssen vor der eigentlichen Delta-Auswertung eindeutig definiert werden. [S08–10]

**Gas/H2.** Die ENTSOG-Entwürfe unterscheiden CBA, Infrastructure Gap Identification und System Assessment. Eine Sensitivität mit gelockerten Transport-, Import- oder Speichergrenzen zeigt eine Infrastruktur-/Angebotsrestriktion, liefert aber ohne Kosten und Investitionsvariablen keine ökonomisch optimale Dimensionierung. Stündliche duale Strom-H2-Modellierung und monatliche Gasmodellierung sind unterschiedliche Auflösungen; eine Kopplung über Schnittstellen ist kein Beweis vollständiger simultaner physischer Co-Optimierung. [S11–15]

**ERAA.** Erst die wirtschaftliche Ressourcenentwicklung, dann die probabilistische Risikoermittlung auf dem resultierenden System. Risiko- und Konvergenzanforderungen nicht aus einer einzelnen perfekten Wetterchronologie ableiten. Die 2026 revidierte Methodik und ihr Rollout müssen je Bewertungsjahr separat gepinnt werden. [S16–18]

**Nationale Planung.** Genehmigte Szenariorahmen sind für die zugehörigen NEP Eingangsdaten; sie sind nicht das Ergebnis einer nachträglichen kostenoptimalen Neuberechnung durch den NEP-Solver. SES und Langfristszenarien unterstützen die konsistente Transformation, haben aber andere Entscheidungsaufgaben und Autorität als die einzelnen NEP. Im NEP und der Netzreserve können marktbasierte Austauschrestriktionen die detaillierte Netzprüfung nicht ersetzen. [S19–28]

**Verteilnetz und Wärme.** §14d EnWG verlangt die regionale Abstimmung und Berücksichtigung von Entwicklung/Flexibilität; das WPG verlangt räumliche Analyse und Zielszenarien. Beide legen nicht pauschal einen einheitlichen Optimierungssolver oder die explizite Modellierung jedes einzelnen NS-Strangs für jede nationale Studie fest. Für eine konkrete lokale Ausbauentscheidung kann eine Aggregation ohne Spannung, thermische Grenzen und Anschlussbedingungen unzureichend sein. [S29–30]

## 3. Prozessübergreifende Requirements-Matrix

### 3.1 Anwendung

P = Pflicht **für die genannten Prozessprofile**, nicht für jeden einzelnen Solver und nicht automatisch gesetzliche Pflicht. O = optionale methodische Erweiterung. F = Forschung. Für eine integrierte Architektur gelten alle P-Anforderungen im jeweils relevanten Profil; einzelne Komponenten dürfen außerhalb ihres deklarierten Profils N/A sein. Spätere Reviewer sollen zusätzlich unterscheiden: native Unterstützung / Konfiguration / validierter Adapter / externe Modellkette / nicht unterstützt / unbekannt. Die Nummern sind dauerhaft; Änderungen über Version und Traceability, keine Umnummerierung.

| Requirement-ID | Klasse | Profile | Anforderung und prüfbares Akzeptanzkriterium | Quelle / Referenz |
|---|---|---|---|---|
| ESM-A-R001 | P | alle | Szenario-ID, Zieljahr, Dokumentstatus, Parameter-/Datenversion und Herkunft je Datensatz; reproduzierbarer Snapshot ohne stille Defaults | S01–30; M0 |
| ESM-A-R002 | P | PR01/02/03/06/07/10 | exogene Bestands-/Kapazitätsentwicklung mit expliziter Fixierung; exogenes Asset nicht versehentlich optimierbar | S03–07, S18, S20, S25; B04/B11 |
| ESM-A-R003 | P | PR02/03/05/10/14 | endogener Ausbau mit Kandidaten, bounds, Kosten, Lebensdauer und Inbetriebnahme; Investitionsvariablen getrennt von Dispatch | S05, S07, S14, S25, S29; B04/B11 |
| ESM-A-R004 | P | PR02/03/04/05/07–10/14/15 | Brownfield mit vorhandenem, geplanten und stilllegbarem Bestand; getrennte Zuordnung von sunk und incremental costs | S05–15, S20–25, S29–30; B05/B11 |
| ESM-A-R005 | O | PR01/10 | GF-Variante nur mit klarer Ausschluss-/Restbestandsdefinition; GF als Sensitivität, nicht Standard-NEP | M1, B11 |
| ESM-A-R006 | P | PR01–06/10/11 | PF-Informationsumfang und Terminalbedingungen offenlegen; Wetter-/Ausfallkenntnis und Investitionskenntnis getrennt | S03–07, S18, S25; B03/B04 |
| ESM-A-R007 | O | PR01/10/14 | myopic/rolling Planung: Freeze bereits getroffener Investitionen, konsistente Zustandsübergabe und Endwert | M1; B11 |
| ESM-A-R008 | P | PR01–06/08/10–12/14 | stündliche oder quellenkonform feinere Chronologie, Kalender/DST/UTC, Zeitschritt und statistische Gewichte separat | S03–10, S18, S21, S25–27; B03 |
| ESM-A-R009 | P | PR01–06/10/11 | korrelierte meteorologische Zeitreihen für Last, Wind, PV, Wasserkraft und Temperatur; keine unabhängige Neusortierung | S03–07, S09, S18; B04/B06 |
| ESM-A-R010 | P | PR03 | gemeinsamer Investitionsvektor über gewichtete Wetterfälle, Jahresbetrieb je Fall; Gewichte normiert | S07; B04 |
| ESM-A-R011 | P | PR06/11 | stochastische Ausfälle, Wetter, LOLE/EENS, Stichprobengewichte, Seed und Konvergenz; analytische Referenz reproduzierbar | S16–18, S26; B06 |
| ESM-A-R012 | O | PR03/10 | alternative Risiko-Ziele (CVaR/Minimax), nach Vergleich mit Erwartungswert und unverändertem Kandidatenset | M1; B04 |
| ESM-A-R013 | P | PR01–06/08/10–12 | Marktclearing mit Angebot, Nachfrage, Import/Export, Spill und ENS; Bilanz und Kostenzerlegung | S03–10, S18, S21, S25–27; B01 |
| ESM-A-R014 | P* | PR04/06/08/12 | Unit Commitment bei nachweislich benötigter Anlagendiskretheit: min P, Start/Stop, Rampen, Up/Down, Reserve, Initialzustand; sonst explizite Relaxation und Impact | M2; B09; Pflicht im UC-Benchmark, keine universelle gesetzliche UC-Pflicht |
| ESM-A-R015 | P | PR01–06/08/10/11 | Speicherleistung/-energie separat, SOC, Wirkungsgrade, Verluste, Inflow, Spill und Zeitkopplung; korrekte Endbedingungen | M2; B03 |
| ESM-A-R016 | P | PR02/04/06/08/10/11 | NTC-/Transportnetz: Richtung, Verluste, Kapazitäten und Austauschbilanz; nicht mit DC-Netz gleichsetzen | S05, S09, S18, S21; B01 |
| ESM-A-R017 | P | PR03/08/12 | nodales DC-Netz mit KCL/KVL, Referenzwinkel je Insel, PST/HVDC als unterschiedliche Komponenten | S07, S21, S27; B02 |
| ESM-A-R018 | P* | PR03/04/06/08/12 | zonale PTDF/GSK/FBMC-Option mit CNEC, RAM, Referenzflüssen, Nettoexporten und geprüfter Zeit-/Netzversion; verpflichtend für Vergleichsprofil FB, nicht für jedes Zieljahr der Originalprozesse | S07, S09–10, S18; B02 |
| ESM-A-R019 | P | PR03/08/12/14 | Aggregationsmapping unter Erhalt von Injektion, Leitungsverbindung, Inseln, Technologie-/Anlagenzuordnung; Flussfehler gegen Originalnetz | M3; B02/B08 |
| ESM-A-R020 | P | PR08/12/13/14 | AC-Lastfluss bzw. AC-OPF als eigenes Modell mit Q, V, Verlusten, Trafo, Shunt, Grenzen und validierter Slack-Semantik | S21, S27–29; B10 |
| ESM-A-R021 | P | PR08/12/13; PR14 falls erforderlich | N-1-Kontingenzen, zulässige preventive/corrective Maßnahmen, Insel-/Ausfallsemantik; kein Pseudo-PASS bei nicht versorgter Insel | S21, S27–29; B02/B10 |
| ESM-A-R022 | P | PR08/12 | Markt→Redispatch als getrennter Prozess, Ausgangsdispatch, positive/negative Kosten, Grenzen, Erzeugungs-/Speicherzustände und Netzverluste | S21, S27; B02 |
| ESM-A-R023 | P | PR12/13 | Reservekapazität, Aktivierbarkeit, Standort und Einsatzdauer; keine Mehrfachanrechnung derselben Flexibilität | S27–28; B09/B10 |
| ESM-A-R024 | P | PR04/05 | Referenznetz je Zieljahr, Projektstatus, Reife, Baseline und PINT/TOOT; paarige Eingaben mit dokumentierten zulässigen Abweichungen | S08–13; B05 |
| ESM-A-R025 | P | PR04/05 | inkrementelle CBA-Kennzahlen getrennt nach monetär/nichtmonetär, Investition/Betrieb, Wohlfahrt, Verluste, externe Effekte, Versorgung; keine Doppelzählung | S08–13; B05 |
| ESM-A-R026 | P | PR04/05 | projektbezogene Stress-/SoS-Kalibrierung getrennt von Bewertung; identische Seeds/Wetter und dokumentiertes Projektinteraktionsrisiko | S09–10, S13; B05/B06 |
| ESM-A-R027 | P | PR05/09 | Gas/H2 als getrennte Carrier, getrennte Kapazitäten und Verluste; Leitungsumstellung mit gegenseitigem Ausschluss und Zeitverzug | S11–15, S22; B07/B11 |
| ESM-A-R028 | P | PR09 | Druck, Transportgrenzen, Verdichtung und ggf. Linepack in physischer Gas-/H2-Prüfung; vereinfachtes Transportmodell klar kennzeichnen | S22; M6/B07 |
| ESM-A-R029 | P | PR01/03/05/10/14 | Elektrolyse, H2-Speicher, Rückverstromung und Import; Energie-/Massen-/Wirkungsgradbasis eindeutig (LHV/HHV) | S04, S07, S11–15, S25; B07 |
| ESM-A-R030 | P | PR01/10/14 | EV-Mobilitätsnachfrage, Ladeanschluss/-verfügbarkeit, SOC und Abfahrtsbedarf; unflexible und V1G-Variante | S04, S25, S29; B03 |
| ESM-A-R031 | O | PR01/10/14 | V2G inkl. bidirektionaler Grenze, Wirkungsgrad, Degradation und Nutzerrestriktionen, keine kostenlose Doppelverwendung | M7; B03 |
| ESM-A-R032 | P | PR01/10/14/15 | Wärmebedarf, Wärmepumpe, temperaturabhängiger COP, Wärmespeicher, Fernwärme/Abwärme und Wärmeversorgung; dieselbe Wärmelast nicht zweimal | S03–04, S25, S29–30; B07/B08 |
| ESM-A-R033 | O | PR01/10/14/15 | Kälte/Kühlung mit temperatur-/zeitabhängiger EER bzw. COP und thermischer Speicherung; bei relevanter Nachfrage P | M7; B07 |
| ESM-A-R034 | P* | PR01/06/10/14 | industrielle Flexibilität mit Energie-/Produktionsrestriktion, Zeitfenster, Rebound, Opportunitätskosten; P wenn als gesicherte Flexibilität angenommen | S04, S18, S25, S29; B03/B09 |
| ESM-A-R035 | P | PR14 | explizite DSO-Netze für lokale Ausbauentscheidung: Spannung, Thermik, Trafo, Anschluss, Topologie und bidirektionale Flüsse | S29; B08/B10 |
| ESM-A-R036 | P | PR08/10/14 | aggregierte DSO-Flexibilitäts-/Netzrestriktion als Alternative auf übergeordneter Ebene; disaggregierbar und validiert, gemeinsame Schnittstelle | S25, S29; B08 |
| ESM-A-R037 | P | PR14/15 | räumliche Zuordnung von Wärme-/EV-/H2-Last, Netzanschlussleistung, zeitliche Profile und Kosten zwischen Planungsebenen; keine Doppelzählung | S29–30; B08 |
| ESM-A-R038 | P | PR13 | Stabilität separat prüfen: Frequenz/RoCoF/Nadir, Spannung, Kurzschlussleistung, dynamische Modelle, relevante Betriebs- und Fehlerfälle; Scope dokumentiert | S28; B10 |
| ESM-A-R039 | F | PR08/10/13/14 | endogene Stabilitätsrestriktionen als validierte approximative Schnitte; Fehlklassifikation und Topologieabhängigkeit nachweisen | M4; B10 |
| ESM-A-R040 | F | PR03/10/14 | mehrstufige stochastische Expansion mit Nichtantizipativität, Information Sets, ggf. Dekomposition und Out-of-sample-Prüfung | M1; B04/B11 |
| ESM-A-R041 | O | PR01–05/08/10 | Repräsentativtage/-wochen mit Extremereignissen, Erhaltung saisonaler SOC-Kopplung, Fehler gegen Volljahr; bei offizieller Volljahrpflicht nur Screening | M0/M2; B03 |
| ESM-A-R042 | P | alle | deterministische Benchmarks mit unabhängiger Referenz, Residuen, Solverstatus, Toleranzen, reproduzierbaren Eingaben; kein Bestehen bei fehlender Evidenz | B01–B11 |
| ESM-A-R043 | P | PR01/07/10 | Szenariokohärenz: CO2, Energie, Bestandsentwicklung und politische Constraints, eindeutige regionale Summen | S03–04, S20, S24–25; B11 |
| ESM-A-R044 | P | PR04/05/10/15 | einheitliche Preisbasis, Währung, Diskontierung, Annuitäten/Lebensdauer, Restwert und Projektkosten; keine doppelte Diskontierung | S08–13, S25, S30; B05/B11 |
| ESM-A-R045 | P | PR06/11 | wirtschaftliche Ressourcenentwicklung (EVA sofern gemäß Profil) separat vom probabilistischen Risiko; Eintritt/Austritt/Verbleib und Investitionslogik nachvollziehbar | S16–18, S26; M5 |
| ESM-A-R046 | P | alle | Modellgrenzen und Missing/Unknown explizit: keine stillen Nullen für Zeitreihen, Netze, Ausfälle, Kosten oder SOC; Datenvertrag und Adapteraudit | M0, §7 |
| ESM-A-R047 | P | PR01/03/05/07/09/10/14/15 | Schnittstellen zwischen Strom/Gas/H2/Wärme und Ebenen mit gemeinsamen räumlich-zeitlichen Schlüsseln, Kapazitäts- und Energieerhaltung | S04, S07, S12–15, S20, S25, S29–30; B07/B08 |
| ESM-A-R048 | F | PR01/06/10 | ML-/Surrogatmodelle nur mit OOD- und Residuenprüfung, konservativer Fehlerabschätzung und unabhängiger physikalischer Validierung | §8; B10 |
| ESM-A-R049 | P | PR04/05/06/11 | Unsicherheits- und Sensitivitätsauswertung, gemeinsame Referenzannahmen, Stichproben-/Szenariostatistik; kein Scheingenauigkeits-Ranking | S08–18, S26; B05/B06 |
| ESM-A-R050 | P | PR14/15 | Wärmeversorgungsgebiet/Eignung, lokales Potenzial, Lebenszykluskosten, Emissionen, Versorgung und Umsetzungsrestriktionen getrennt ausweisen | S30; M7/B08 |

P* bedeutet konditionale Pflicht: aktiviert durch den expliziten Modell-/Prozess-Scope. Insbesondere UC, FBMC und Industrie-Flexibilität dürfen nicht aufgrund bloßer Nennung im Modellkatalog für jedes offizielle Verfahren als verpflichtend behauptet werden.

## 4. Mathematische Referenzformulierungen

### M0 – Indizes, Einheiten, Zeit und Informationsstruktur

Mengen: K Carrier (Strom, Methan, H2, Wärme, Kälte ...), N Knoten/Regionen, A Anlagen/Umwandler, L Leitungen/Korridore, Y Investitions-/Zieljahre, T_y chronologische Zeitschritte, W Wetterfälle, Ω probabilistische Ausfall-/Wetterzustände, C Kontingenzen. Positive Injektion ins Netz; Flüsse orientiert. Leistungsgrößen in MW (bei Carrier festgelegter Energiebezug), Energie in MWh, Gas-/H2-Masse separat in kg oder t, Druck absolut in bar bzw. Pa; Währung EUR eines dokumentierten Preisjahres.

Physische Zeitschrittdauer Δt in h; statistisches Repräsentationsgewicht ν_t dimensionslos; Jahresstundengewicht h_t = ν_t Δt. Für volle Chronologie ν_t=1. Wetter-/Szenariogewicht π_w mit Summe 1. Keine Multiplikation der SOC-Dynamik mit einer Stichprobengewichtung, die keine echte Zeitdauer darstellt. Reserve, Leistung, Energie, Emissionsmasse und monetäre Werte nicht vermischen.

Investition erfolgt vor Realisierung des jeweiligen Betriebsfalls, sofern eine gemeinsame Entscheidung verlangt wird. Eine einzelne Wetterjahresoptimierung mit vollständiger Voraussicht innerhalb dieses Jahres ist ein idealisiertes Dispatch-Modell; sie ist weder eine mehrstufig stochastische Politik noch eine reale Marktprognose.

### M1 – Kapazitäts-/Transformationsoptimierung (LP/MILP)

Für Anlagen i, Jahr y und Wetterfall w: Bestand K_iy, Zubau x_iy, Stilllegung r_iy, Dispatch p_iytw. Beispiel eines diskontierten Systemkostenminimums:

$$
\min_{x,r,p,\ldots}\;\sum_{y\in Y} d_y\left[I_y(x,r)+a_y\left(F_y(K)+\sum_w\pi_w\sum_t h_t C_{ytw}(p,q,\ell)\right)\right].
$$

d_y=(1+r)^(−(y−y0)), a_y Anzahl repräsentierter Kalenderjahre (präziser: Summe der jahrweisen Diskontfaktoren relativ zu d_y). I_y einmalige CAPEX; F_y jährliche Fixkosten; C variable Kosten in EUR/h, z. B. Brennstoff, CO2, variable O&M, Lastabwurf und ggf. gesonderte Startkosten pro Ereignis. CAPEX alternativ annualisieren, dann in F_y einfügen und I_y entsprechend entfernen. Keine doppelte Kapitalbelastung. Je nach Horizont Restwert explizit.

Kapazität aus dokumentiertem Bestand und aktiven Investitionskohorten:

$$
K_{iy}=K^{legacy}_{iy}+\sum_{\tau\le y:\;\tau+b_i\le y<\tau+b_i+L_i}x_{i\tau}-R_{iy}.
$$

b_i Bauzeit, L_i Lebensdauer, R freiwillige kumulierte Stilllegung der sonst noch verfügbaren Kapazität. Im implementierbaren Modell kohortenscharfe Retirement-/Lifetime-Buchung verwenden; R darf nie dieselbe Kapazität zweimal abziehen. Diskrete Projekte mit x_i=Kbar_i z_i, z_i∈{0,1}; kontinuierliche Technologien mit 0≤x_i≤xmax_i. Exogener Bestand wird fixiert, nicht als kostenloser Ausbau modelliert. GF entspricht einem ausdrücklich definierten Klegacy=0 für die GF-Assets, BF nicht.

Allgemeine Carrier-Knoten-Bilanz (bei Verlusten portweise Eingang/Ausgang):

$$
\sum_{a}S_{nka}q_{aytw} + \sum_l B_{nkl}f_{lytw}
+ p^{import}_{nky tw} - p^{export}_{nky tw}
+\ell_{nky tw}=D_{nky tw}.
$$

S signed conversion-port matrix, z. B. Elektrolyse −1 MW_el und +η MW_H2 je MW_el Input. B Inzidenz bzw. verlustbehaftete Portabbildung. 0≤ℓ≤D; Abregelung ausschließlich auf verfügbares Angebot, nicht als zusätzliche Lastdeckung. Emissionslimit:

$$
\sum_{w,t,a}\pi_w h_t e_{a}q_{aytw}\le E_y^{max}.
$$

Bei wetterfallspezifischer statt erwarteter Zielvorgabe pro w anwenden. Politische Mindest-/Maximalbestände, EE-Anteile und Standortrestriktionen explizit.

- PF: simultane Lösung für alle Y unter gegebenem Szenario.
- MY: Lösung des aktuellen Fensters, Realisierung nur erster Entscheidungen, Weitergabe des Bestands/SOC; Diskont-/Terminalwerte dokumentieren.
- Zweistufig stochastisch: gemeinsame x über w; recourse p_w. Mehrstufig: x_{yω}=x_{yω'} für ω,ω' mit identischem Informationsverlauf vor y.
- Risikovariante: Erwartungswert plus λ CVaR_α(C), wobei CVaR=ζ+1/(1−α)Σπ_w max(0,C_w−ζ), oder minimax über w. Diese Alternativen nicht als gleichwertig ausweisen.

### M2 – Chronologischer Dispatch, UC, Reserve, Speicher (LP/MILP)

Gegeben K und Netzwerk, min Σ h_t Σ_i c_i p_it + Kosten für ENS, ggf. Reserve, und Σ Ereigniskosten. Für diskrete Einheiten (oder ganzzahlige Aggregate mit geeigneter Flottenformulierung):

$$
\underline P_i u_{it}\le p_{it}\le \bar P_{it}u_{it},\quad
u_{it}-u_{i,t-1}=v_{it}-z_{it},
$$

$$
\sum_{\tau=t-U_i+1}^{t}v_{i\tau}\le u_{it},\qquad
\sum_{\tau=t-D_i+1}^{t}z_{i\tau}\le1-u_{it}.
$$

u on/off, v Start, z Stop (binär). Initiale Restlauf-/Stillstandsdauer separat. Rampen z. B.
p_t−p_{t−1}≤RU Δt u_{t−1}+SU v_t,
p_{t−1}−p_t≤RD Δt u_t+SD z_t; Grenzwerte an Anlagentyp und Start-/Stop-Rampe binden. Bei kontinuierlichem Dispatch u entfallen; Relaxation hinsichtlich Kosten, Lastdeckung und Reserve kennzeichnen. Produkt aus kontinuierlicher Investitionsgröße und binärem UC ist nicht automatisch linear; feste Anlagenblöcke oder saubere Linearisierung verwenden.

Aufwärtsreserve 0≤r^+≤Pmax u−p, r^+≤RU τ_act und Σr^+≥R_t; analog abwärts und gegebenenfalls Netzlieferbarkeit, Aktivierungsdauer, Speicher-SOC. Reserve-Energie und Marktenergie nicht doppelt belegen. Für Speicher:

$$
s_t=(1-\rho)^{\Delta t}s_{t-1}+\eta_c p^c_t\Delta t-p^d_t\Delta t/\eta_d+I_t-S_t,
\quad 0\le s_t\le E,\quad 0\le p^c_t\le K_c,\;0\le p^d_t\le K_d.
$$

I/S als Energiemenge pro Schritt, oder bei Leistung zusätzlich Δt. Gleichzeitiges Laden/Entladen nur zulassen, wenn das gewählte Relaxationsmodell dies physikalisch/ökonomisch rechtfertigt; bei negativen Preisen, gekoppelten Produkten oder Anlagenmodi explizite Modusrestriktion. Ein-/Ausspeicherung, PHS, Flusskraft und Reservoir nicht ohne Semantikprüfung zusammenfassen. Für repräsentative Perioden eine chronologisch konsistente interperiodische Speicherzustandskopplung oder nachgewiesene Approximation.

Marktpreise: Dual der Energiebilanz im konvexen Dispatch; bei MILP keine eindeutigen Marktpreise aus beliebigen Relaxations-Dualen, Preisbildung (z. B. fixed commitment dispatch) separat deklarieren. Nachfrage kann fix oder elastisch über Nutzenkurven modelliert sein. Wohlfahrtsmaximum mit elastischer Nachfrage ist nicht stets dasselbe wie reines Kostenminimum.

### M3 – Netzrepräsentationen, FBMC und Aggregation

**NTC:** f_AB∈[−NTC_BA,NTC_AB]; keine implizite KVL. Grenzwerte zeit-/richtungsspezifisch, gegebenenfalls verlustbehaftete Portbilanz. Eine Marktkopplungsgrenze ist keine physische Leitungsampazität.

**DC load flow:** für AC-Leitung l=(i,j), orientierter Fluss f_l=(θ_i−θ_j−φ_l)/x_l in konsistenter pu-/MW-Basis, |f_l|≤F_l; KCL A f=p; θ_ref=0 je verbundenem AC-Teilnetz. HVDC ist steuerbarer Transfer mit eigener Wirkungsgrad-/Kapazitätsbilanz; nicht als passiver AC-Zweig in KVL einsetzen. PST Phasenverschiebung φ_l; Referenzwinkel und Vorzeichen festschreiben. PTDF H=B_f B_bus^+ auf der balancierten Injektionsuntermenge, f=H p+f_φ. Bei Inselbildung neue Netzmatrix und Inselbilanzen.

**Zonales Flow-Based Domain:** zonale Nettoexporte n, Σ_z n_z=0 (bei separater Verlust-/HVDC-Semantik entsprechend ergänzen), GSK-Matrix G mit kolonnenweisen Summen 1 innerhalb der zugeordneten Zone, p=p_ref+G(n−n_ref). Für CNEC k:

$$
f_k=f^{ref}_k+H_k G(n-n^{ref}),\quad
-F_k^{min,dir}+m_k^-\le f_k\le F_k^{max,dir}-m_k^+.
$$

Äquivalent richtungsbezogen A_FB n≤RAM, wobei die Referenz-/Sicherheitskomponenten genau einmal enthalten sind. RAM enthält nach konkreter Marktmethodik u. a. Referenzfluss, Margen und remedial actions; Vorzeichen, minRAM/Validierungskorrekturen und HVDC-Repräsentation nicht pauschal aus dieser Formel ableiten. CNEC = monitored element × contingency; PTDF je Fall oder LODF-Transformation, soweit zulässig. Keine Behauptung, vollständige europäische Day-Ahead-Auktionslogik (Orders, Blockgebote, Preis-/Volumenregeln) werde allein durch PTDF-Ungleichungen abgebildet. Separates erweitertes Marktprofil bei Bedarf.

**Aggregation:** P bildet detaillierte Knoten auf Zonen, Γ bildet orientierte detail-Leitungsflüsse auf Aggregatkorridore, R verteilt zonale Injektionen. Notwendige Konsistenz:

$$
p_z=Pp,\quad PR=I,\quad f_z=\Gamma f,\quad A_z\Gamma=PA_d,\quad H_z=\Gamma H_dR.
$$

Technologie-/zeitabhängige R/GSK bei Bedarf. Interne Zyklen, affine PST-/Grundflüsse und Netzreaktanzen bleiben zu qualifizieren. Eine aggregierte PTDF-Matrix impliziert nicht automatisch ein passendes passives Ersatznetz mit exakt gleichen Reaktanzen; Ersatzparameter, KVL-Residuen, Fehler in relevanten CNECs und mehrere Topologien separat bewerten. Ländergrenzen begrenzen gegebenenfalls Clusterbildung, nicht automatisch physische AC-Verbindungen.

**AC network:** komplexe Spannung V_i=|V_i|e^{jθ_i}, admittance Y. Knotenleistung:

$$
P_i+jQ_i=V_i\left(\sum_jY_{ij}V_j\right)^*,\quad
\underline V_i\le |V_i|\le\bar V_i,\quad |S_{ij}|,|S_{ji}|\le S_{ij}^{max}.
$$

Generator-P/Q- oder capability-curve, Trafo/Taps, Shunts, Leitungsverluste, Lastmodell und Slack explizit; AC-PF prüft einen Betriebspunkt, AC-OPF optimiert zulässige Variablen. Beides ersetzt nicht die Mehrperioden-UC-Bedingungen oder die Stabilität.

### M4 – Redispatch, N-1 und Stabilitätsmodelle

Marktergebnis p^M_i ist Referenz, p_i=p_i^M+δ_i^+−δ_i^−. Redispatch minimiert beispielsweise

$$
\sum_{i,t}h_t(c_i^+\delta_{it}^+ + c_i^-\delta_{it}^-)+C_{ENS}+C_{other}.
$$

Kostenkonvention (Entschädigung, Opportunitätskosten oder inkrementelle Systemkosten) ausdrücklich angeben; keine implizite Belohnung für gegenläufige Maßnahmen. Nettowirkleistung, Rampen, SOC, Commitment, Q-Grenzen, HVDC/PST und Reserven aus dem Ausgangsfall. AC-Verluste führen gegebenenfalls zu nicht exakt ausgeglichenem reinen Wirkleistungsredispatch ohne Slack-/Reservekorrektur.

N-1: für c∈C Netzzustand nach Ausfall, gemeinsame präventive Entscheidung p, zulässige korrektive Variable Δp_c mit Reaktionszeit/-grenze, Kontingenzgleichungen und Notfallgrenzen:

$$
g_c(p+\Delta p_c,V_c,\theta_c)=0,\quad
h_c(p+\Delta p_c,V_c,\theta_c)\le0.
$$

Bei nicht-isolierendem Einzelausfall kann DC-Screening f_l^c=f_l+LODF_lc f_c verwenden. LODF singular bei Inselbildung: nicht mit Null, NaN oder ausgelassenem Fall als sicher werten. Zulässige Korrekturmaßnahmen, Load Shedding und Wiederversorgung explizit. N-1-Ausfälle sind keine Zufallsstichproben der ERAA; deterministische Sicherheitsgrenzen und probabilistische Risikoaggregation auseinanderhalten.

Stabilität: Frequenzbeispiel für einen kohärenten initialen Bereich mit synchroner kinetischer Energie E_kin=Σ H_i S_i in MWs und plötzlichem Leistungsdefizit ΔP:

$$
\left.\frac{df}{dt}\right|_{0^+}=-\frac{f_0\Delta P}{2E_{kin}}.
$$

Nur unter den Modellannahmen (keine unmittelbare Regelantwort/Dämpfungswirkung, geeignete aggregierte Frequenz). Nadir hängt zusätzlich von dynamischer Antwort, Verzögerung, Sättigung und Reserven ab. Spannungs-/Winkel-/Konverterstabilität und Kurzschlussfestigkeit erfordern separate Nachweise, z. B. DAE mit ẋ=F(x,z,u), 0=G(x,z,u) samt konsistentem Initialzustand. Statische SCR/gSCR, Impedanz- oder RoCoF-Surrogate sind keine universelle dynamische Sicherheitsgarantie. Optimierungs-Cuts müssen für jeweilige Topologie, Gerätemodelle und Betriebsbereich qualifiziert werden.

### M5 – IoSN, CBA und ERAA

**IoSN:** Spezialfall M1 mit festen szenariogebundenen Erzeugungs-/Lastdaten, BF-Startnetz L0 und zulässigen Kandidaten, z. B. x Austausch, Speicher oder hybride Infrastruktur. Für die 2026-Konsultationsstruktur:

$$
\min_{x}\left[C^{annual}_{inv}(x)+\sum_{w=1}^3\pi_w Q_w(x;L_0,K,D_w)\right].
$$

Q_w ist optimaler Betrieb unter denselben x. Die Anzahl drei stammt aus S07, die Gewichte, Jahreswahl, Kandidaten- und Filterlogik müssen aus der gültigen Fassung übernommen werden. Vergleich mit einem exogenen Ausbau-/No-build-Referenzfall getrennt von Projekt-CBA. Bedarf und baulich realisierbares Projekt nicht gleichsetzen.

**CBA:** R_y ist Referenzinfrastruktur für Zieljahr y, j Projekt oder definierte Projektgruppe. PINT: L^-_y=R_y, L^+_y=R_y∪{j}, wenn j nicht in R_y. TOOT: L^-_y=R_y\{j}, L^+_y=R_y, wenn j enthalten. Bei Projektgruppen analog. Alle anderen Eingaben gleich, außer dokumentierten methodischen Anpassungen.

Für inelastische identische Nachfrage und geeignetes Betriebskostenmodell:

$$
B^{op}_{jy}=\sum_w\pi_w\left[C^{op}(L^-_y,w)-C^{op}(L^+_y,w)\right].
$$

Für elastische Nachfrage SEW-Differenz = Δ(Nutzen−Ressourcenkosten); Konsumenten-/Produzentenrente und Congestion Rent als konsistente alternative Zerlegung. Transfers nicht erneut als gesellschaftlicher Nutzen addieren. Lastabwurf monetär nur gemäß definierter VoLL/ENS-Semantik. CO2-Kosten im Dispatch und monetarisierte Emissionsnutzen abgleichen; Verluste nicht doppelt erfassen.

$$
NPV_j=\sum_y d_y\left[B^{mon}_{jy}-\Delta OPEX_{jy}-CAPEX_{jy}\right]+RV_j,\quad
BCR_j=PV(B)/PV(C).
$$

Hier muss B^mon betriebliche Kosten, externe Effekte und weitere Indikatoren ohne Doppelzählung enthalten; wenn OPEX bereits in B^op enthalten, nicht erneut abziehen. PV(C)>0, Kosten-/Nutzenkonvention und Restwertbasis fixieren. Nichtmonetäre Indikatoren (z. B. Emissionen in t, RES-Integration in MWh, Resilienzindikatoren) separat berichten. Nicht-additive Projektinteraktionen durch Gruppen-/Reihenfolgesensitivität prüfen. ENTSOG-H2-Indikatoren in ihren Originaleinheiten und separater H2-Methodik auswerten, nicht elektrische CBA-Labels blind übertragen.

**ERAA/EVA:** wirtschaftlicher Ressourcenzustand über Investition, Austritt oder Erhalt gemäß jeweiliger Methode bestimmen. Ein Profitabilitätsindikator für Ressource i:

$$
\Pi_i=\mathbb E_\omega\!\left[\sum_t h_t(\lambda_{nt}p_{it}+Rev^{other}_{it}-C^{var}_{it})\right]-C^{fixed}_i-C^{capital}_i.
$$

EVA-Entscheidungen hängen von definierten Markt-/Vergütungsannahmen, Unsicherheit, Technologie, Kosten und Eintritts-/Austrittsregeln ab. Diese Formel ist eine konzeptionelle Referenz, nicht vollständige Rekonstruktion des ERAA-EVA-Algorithmus. Reines Systemkostenminimum ohne EVA-Semantik ist nicht automatisch gleichwertig.

Anschließend probabilistisches Betriebsmodell mit gezogenen Verfügbarkeiten und korrelierten Wetterlasten, szenariogebundenem Austausch und SOC. Für Zone z und ENS-Leistung ℓ:

$$
LOLE_z=\sum_\omega \pi_\omega\sum_t \Delta t\,1[\ell_{z,t,\omega}>\epsilon],\quad
EENS_z=\sum_\omega \pi_\omega\sum_t \Delta t\,\ell_{z,t,\omega}.
$$

ε explizite numerische Schwelle. System-LOLE basiert auf mindestens einer betroffenen Zone, nicht Summe der zonalen LOLE. EENS kann bei eindeutigen disjunkten Zonen addiert werden. Für MC mit N gleichgewichteten unabhängigen Jahrespfaden, Mittelwert und Standardfehler s/√N; bei gewichteten/abhängigen Pfaden passende Stichprobenstatistik. Konvergenz je kritischer Zone, Konfidenzintervalle, seltene Ereignisse und Sensitivitäten, nicht nur Gesamt-Europa. VoLL×EENS kann erwartete Kosten ausdrücken, ersetzt aber keinen normativen Reliability Standard (LOLE etc.).

### M6 – Gas/H2 und sektorale Energienetze

Transportmodell: getrennte Carrier-Bilanzen, gerichtete Kapazitätsgrenzen, Umwandlungseffizienz, Speicher-/Importverfügbarkeit. Bei physischer Gas-/H2-Planung zusätzlich Druckgrenzen und geeignete Strömungsrelation, z. B. stationäre vereinfachte Weymouth-Form

$$
q_{ij}|q_{ij}|=K_{ij}(p_i^2-p_j^2)
$$

für festgelegte Einheit, Gasparameter und Modellannahmen; bei Verdichtern Druckverhältnis und Energieverbrauch separat. Linepack-Zustand L_t=L_{t−1}+Δt(q_in−q_out), konsistente Druck-/Inventarbeziehung und thermodynamische Annahmen. H2 hat andere Dichte, Heizwert und hydraulische Parameter; nicht einfach dieselben MW-Kapazitäten aus Methan übernehmen. Modelle nach Fragestellung linear approximieren oder nichtlinear validieren.

Umrüstung einer Leitung: z^CH4_{ly}+z^H2_{ly}≤1, plus Umstellungszeit, Status, technische Eignung, zulässige Teilabschnitte; keine doppelte Zählung derselben Leitung. Elektrolyse p_H2=η_el p_el auf definierter Energie-/Massenbasis; Kompression, Transportverlust und Speicher als separate Ports. Bei sektorübergreifender Iteration unterschiedliche Zeitskalen durch Energieerhaltung und Peak-Information koppeln, nicht nur Monatsmittel.

### M7 – Nachfrageflexibilität, Wärme/Kälte und regionale Netze

EV-Batterie: s_t=s_{t−1}+η_c p^c_tΔt−p^d_tΔt/η_d−E_trip,t; 0≤p^c_t≤a_t K_c, 0≤p^d_t≤a_t K_d, s_depart≥E_req. V1G setzt p^d=0, V2G erlaubt Rückspeisung mit Nutzer-/Degradationskosten, Modusgrenzen und Reserveanforderung. Aggregation der Flotte muss verfügbare Fahrzeuge und Abfahrtsbedingungen erhalten; Jahresenergie allein nicht ausreichend.

Wärmepumpe p_heat=COP(T_ambient,T_supply)p_el; Kältemaschine q_cool=EER(T) p_el. Gebäudespeicher z. B. C_th(T_{t+1}−T_t)=Δt[UA(T_amb−T_t)+q_heat−q_cool+q_gains]; Komfortgrenzen, Warmwasser und saisonale Speicher. Industrielle Lastverschiebung: d_t=d^base_t+δ^+_t−δ^-_t, Grenzen, Σ_{t∈window}Δt(δ^+−δ^-)=0 für reine Verschiebung; Prozesse mit Produkt-/Materiallager oder nicht energetischem Rebound gesondert. Abschaltbare Last mit Kosten und Dauerrestriktion statt fiktiver Energieerhaltung.

DSO-Schnittstelle am Umspannwerk k: F_k = Menge der zeitgekoppelten zulässigen P/Q-Trajektorien, für die lokale Zustände, Flexibilität und AC/DistFlow-Restriktionen existieren. Nationaler Optimierer kann konservative inner approximation Fhat_k⊆F_k verwenden. Für radialen AC-DistFlow (pu, orientiert vom Slack):

$$
P_{ij}=\sum_{m:j\to m}P_{jm}+p_j+r_{ij}l_{ij},\;
Q_{ij}=\sum_mQ_{jm}+q_j+x_{ij}l_{ij},\;
v_j=v_i-2(r_{ij}P_{ij}+x_{ij}Q_{ij})+(r_{ij}^2+x_{ij}^2)l_{ij},
$$

$$
v_il_{ij}=P_{ij}^2+Q_{ij}^2.
$$

v=|V|², l=|I|²; Anschluss- und thermische Grenzen, Schaltzustand und bei Bedarf Unsymmetrie separat. Lineare/SOCP-Näherung gegen unabhängigen Lastfluss validieren. Einzelstunden-Polytop reicht bei SOC, EV und Wärme nicht für den vollen zeitgekoppelten Austausch. Aufteilung aggregierter TSO-Dispatches auf DSO-Einzelanlagen über machbare Disaggregation; Rückmeldung von Unzulässigkeiten und Grenzverletzungen.

Kommunale Wärmeplanung: Vergleich von Versorgungsgebieten (z. B. dezentrale WP, Fernwärme, Hybrid/andere zulässige Optionen), Anschlussquoten, Gebäudelast, lokale Wärmequellen, Wärmenetz-/Stromnetz-Infrastruktur, Temperatur-/Leistungsspitzen, Lebenszykluskosten, Emissionen und Versorgung. M1/M7 sind mögliche quantitative Unterstützung, keine vom WPG allgemein vorgeschriebene Zielfunktion.

## 5. Tatsächlich dokumentierte Werkzeuge und methodische Referenzen

Diese Tabelle ist ausdrücklich **keine vollständige Capability-Bewertung der fünf Vergleichskandidaten**. Offizielle Verwendung in einer Studienphase, dokumentierte Softwarefähigkeit und reproduzierter Produktionslauf sind drei verschiedene Ebenen. Es werden nur belegte Rollen oder ausdrücklich als Kandidaten gekennzeichnete Referenzen eingetragen.

| Tool / Modell | Nachgewiesene Rolle bzw. beschriebene Fähigkeit | Grenzen der Evidenz / Verwendung für Vergleich |
|---|---|---|
| PLEXOS | S04 Toolchain Strom/H2-Marktmodell; S05 IoSN Markt-/Long-Term-Planning; S07 Vergleich/Qualifikation; S09 dokumentierte SoS-Iterations-/Marktmodellrolle | Lizenz, konkrete Version, Eingabedateien, Solveroptionen, UC-Details und Produktionskonfiguration nicht vollständig öffentlich verifiziert. Referenzfunktion M1/M2/M5, kein Produktzwang. |
| Antares Simulator | S05 und S07 dokumentierte Eignungs-/Vergleichsarbeit für Marktmodellierung, u. a. Testsysteme | Antares und Antares/GEMS-Workflow nicht ohne Versions-/Komponentennachweis gleichsetzen. Cross-Tool-Qualifikation ist keine universelle Gleichheit aller Kosten, Preise oder Bilanzsemantiken. Aktueller ERAA-Produktionssolver nicht abschließend verifiziert. |
| PowSyBl | S09 Netzwerkzeuge für CBA-Netzstudien; [offizielles Projekt](https://github.com/powsybl) für Netzmodelle/Analysen | AC/DC-PF, Sicherheits- und Sensitivitätsanalysen als geeignete Referenz; konkrete Implementierungsdetails und Eingabeformat je Version prüfen. Kein Beweis einer alleinigen vollständigen Markt-/CBA-Kette. |
| Weitere CBA-Netzwerkzeuge | S09 dokumentiert unter anderem GridSuite, Integral, PSS/E, PowerFactory sowie RTE-Kontext | technische Rollen unterscheiden; keine ungesicherte Zuordnung sämtlicher Indikatoren zu einem Tool. |
| ETM / Nachfrage- und Angebotsmodule | S04 gemeinsame Toolchain: Energy Transition Model, Nachfrage-/Flexprofilierung, stündliches Marktmodell und weitere Supply-Module | sektorale Schnittstellen, Exogenität und zeitliche Auflösung transparent machen; kein pauschaler simultaner Drei-Carrier-Optimierer. |
| Enertile | S25 Langfristszenarien; lineare, kostenminimierende Transformation mit mehreren Investitionsjahren, sektoraler Kopplung, hochaufgelöstem Betrieb | O45: studienspezifische räumliche Aggregation (Europa 23 Regionen, Deutschland 11), Stundenmodellierung, DSO-Näherung und Wetterbasis 2010 gemäß Modellbeschreibung; keine allgemeine gesetzliche Vorgabe. |
| REMix (DLR) | Open-Source-Energiesystemoptimierung, sektorale Ressourcen-/Technologieflüsse, räumlich-zeitliche Auflösung; [DLR](https://www.dlr.de/de/ve/forschung-und-transfer/infrastruktur/modelle/remix), [Publikation](https://elib.dlr.de/206649/) | Referenz für M1 und Sektorkopplung; hier kein Versions-/Runtime-Nachweis für alle Einzelanforderungen und keine behauptete verpflichtende offizielle Verwendung. |
| TIMES (IEA ETSAP) | intertemporales Technologie-/Ressourcenmodell mit Szenarien, Systemkosten und Lebensdauern; [offizielle Dokumentation](https://iea-etsap.org/the-official-documentation/) | Referenz für langfristige Multi-Period-Planung und Kohorten; räumlich-zeitliche Detaillierung je Instanz, nicht automatisch AC-/FB-/ERAA-Modell. |
| FINE (Forschungszentrum Jülich) | sektorgekoppelte Energiesystemoptimierung, Investition/Betrieb und Zeitaggregation; [offizielle Modellseite](https://www.fz-juelich.de/de/ice/ice-2/ice2-forschung/open-source/fine) | Referenz für M1/M2/M7 und Aggregation; exakte MILP-/Zeitkopplungsoptionen später an konkretem Release testen. |
| Egret, pandapower, OpenDSS, FlexPlan/PowerModels | mögliche unabhängige UC-/AC-/DSO-/Ausbaureferenzen für gemeinsame Benchmarks; siehe §8 | nicht als offiziell eingesetzte TYNDP-/NEP-Produktionswerkzeuge belegt. Prüfen statt voraussetzen, keine Installation oder Lauf in diesem Auftrag. |

Für Antares/GEMS, PyPSA, PyPSA-Eur, Open-TYNDP und open_eGo/eGon ist im nächsten Review jeweils **Produkt-/Repo-/Releasegrenze** zu bestimmen: Kernsolver, Modellgenerator, Datenpipeline, Workflow, zusätzliche Optimierung, Nachverarbeitung. Beispiel: native Fähigkeit einer Bibliothek kann im darauf aufbauenden Modellworkflow fehlen; umgekehrt kann ein Workflow durch ein externes Netztool ein integriertes Profil erfüllen. Keine Gleichsetzung anhand des Namens.

## 6. Gemeinsame, toolneutrale Benchmarks (Spezifikation, keine Solverläufe)

Alle Fälle sind synthetisch und methodenunabhängig. Analytische Sollwerte wurden aus den nachstehenden Definitionen abgeleitet; keine offiziellen ENTSO-E-Ergebnisse. Vor späteren Läufen sind Fixtures mit expliziten Defaults, Einheiten, Toleranzen und Datendateihashes zu erzeugen. Jede Toolantwort wird gegen denselben mathematischen Vertrag bewertet. Benchmarks sind klein genug für manuelle oder unabhängige Referenzrechnung; realistische Skalierungsfälle sind danach gesondert zu definieren.

| ID | Name, Inputs und Profil | Analytisches Orakel / Prüfungen | Requirements |
|---|---|---|---|
| B01 | Zwei-Zonen-Dispatch, 1 h: A Erzeugung 100 MW zu 10 EUR/MWh; B Last 80 MW, lokale Erzeugung 100 MW zu 50; A→B NTC 30 MW, keine Verluste/anderen Kosten. | f=30 MW, pA=30, pB=50, C=2800 EUR. Ohne Grenze C=800, ohne Transfer C=4000. Bilanz und Grenzkosten bei kontinuierlichem LP. | R013,016,042 |
| B02 | Dreiknoten-Dreieck A-B-C-A, x gleich, A +90 MW, C −90 MW, B=0; Orientierung A→B, B→C, A→C. AC-Direktzweig Fmax=50 MW, andere 100. | DC-Flüsse 30,30,60; zulässiger maximaler Transfer 75 bei unveränderter Injektionsverteilung. Ausfall A-C: 90 auf beiden anderen Zweigen. Zusätzliche Inselvariante durch radialen Zweig mit Last; als unversorgt erkennen. FB-Variante mit GSK/PTDF aus demselben Netz, RAM=50 ohne Referenzoffset: 75 MW. | R017–022 |
| B03 | Speicher 2×1 h, Preise 10/100, η=1, initial/terminal SOC=0, E=1 MWh, P=1 MW; ausreichend Kauf-/Verkaufsmöglichkeit, keine Fixkosten. EV-Variante: a=[1,0], Abfahrt am Ende der ersten Stunde SOC≥1, Fahrt in Stunde 2 verbraucht 1. | Speicher lädt 1, entlädt 1, Gewinn 90 EUR. EV-V1G lädt 1 bei Kosten 10, keine Rückspeisung; V2G darf Abfahrts-/Anschlussgrenzen nicht verletzen. Variante ηc=ηd=0,9: SOC-/Energieverluste explizit; kein gleichzeitiger Betrieb durch unbeabsichtigte Relaxation. | R006,008,015,030–034,041 |
| B04 | Gemeinsame Investition über zwei Wetterfälle π=0,5: W1 Last 100 MW für 1 h, W2 Last 0; keine Altanlage; x∈[0,100], CAPEX 60 EUR/MW für Modellhorizont, variable Kosten 0, VoLL=100 EUR/MWh. | Erwartungsziel C(x)=60x+50(100−x); x=0, C=5000. Minimax: x=100, C=6000; PF nach Wetterrealisierung wäre x_W1=100, x_W2=0, erwartete Kosten 3000, aber nicht zulässig für gemeinsame Planung. | R002,003,006,009,010,012,040 |
| B05 | CBA, zwei Kandidaten J1/J2 à 40 MW, parallel zwischen A (billig 10) und B (teuer 50); B Last 60 MW, 1 h, alle anderen Kapazitäten groß, keine Projektkosten im Betriebsindikator. | ohne Projekt C=3000; eines C=1400; beide C=600. PINT Einzelprojekt 1600 EUR; TOOT Einzelprojekt aus Vollnetz 800 EUR; Gruppe 2400 EUR. Summe einzelner PINT=3200 überschätzt Gruppenbenefit. Gleiche Wetter-/Last-/Kosteninputs nachweisen, CAPEX getrennt. | R004,024–026,044,049 |
| B06 | ERAA exakter Wahrscheinlichkeitsfall: 1 h, Last 100 MW, 100 MW verfügbar mit p=0,9, 70 MW mit p=0,1. Kein Import oder Speicher. | LOLE=0,1 h, EENS=3 MWh. 2-Zonen-Variante mit identischem perfekt korreliertem Defizit: System-LOLE=0,1 statt 0,2 h, EENS=6 MWh. MC-Variante mehrere Seeds, Konfidenz und Stichprobenfehler gegen exaktes Orakel. | R009,011,026,045,049 |
| B07 | H2-Last 10 MWh in 1 h; Elektrolyse η=0,5, Strompreis 10 EUR/MWh, alternative H2-Quelle 30 EUR/MWh, genügend Leistung; H2-Energie LHV. Variante 6 MW H2-Transportlimit der Elektrolyse. | freie Elektrolyse 20 MWh_el→10 MWh_H2, Kosten 200. Limit: 12 MWh_el→6 MWh_H2, 4 MWh Alternative, Kosten 240. Übertragbare Leitung entweder CH4 oder H2; kein doppelter Asset-Bestand. Druck-/Linepack-Negativfall später explizit parametrisieren. | R027–029,032,033,047 |
| B08 | Zwei DSO-Teilflexibilitäten je bis 3 MW, gemeinsame Umspanngrenze 5 MW; 1 h, alle Verluste 0. Zusatz: Wärmepumpe COP=3, 6 MW Wärmebedarf erzeugt 2 MW Stromlast im selben Knoten, keine Speicherung. | Summe Flex ≤5, nicht 6; bei 2 MW gleichzeitig beanspruchter Trafoleistung verbleibt in gleichgerichteter Richtung maximal 3 MW. Gegengerichtete Flüsse mit signierter Bilanz. Lokale Disaggregation und Spannungs-/Thermik-Nachweis als zweite Stufe. | R019,035–037,047,050 |
| B09 | UC: 3×1 h, Nachfrage [10,0,10] MW; Einheit 10 MW, Pmin=10, c=10, Startup=50, MinUp=2 h, anfangs aus und genügend lange aus. Notwendige Abregelung/Spill bei Überschuss zum Preis 0 erlaubt; keine Mindeststillstandsdauer über eine Stunde. Terminalstatus erlaubt weiteres On-sein nach Ende, Start in letzter Stunde erfordert explizite Terminalregel. | On über alle 3 h: Kosten 350 EUR, Spill 10 MWh in Mitte. Unzulässiges On-Off-On hätte 300 EUR (zwei Starts, zwei Betriebsstunden), verletzt MinUp. Mit geeigneter Alternative prüfen, dass UC-Relaxation nicht als exaktes Optimum ausgegeben wird. Reservevariant Pmax=10: bei p=10 kein Up-Headroom. | R014,023,034 |
| B10 | AC-Referenz: zwei Busse, V1=V2=1 pu, rein induktiver Zweig x=0,1 pu, Transfer P=0,5 pu. Frequenztest separat: f0=50 Hz, Ekin=500 MWs, plötzliches Defizit 10 MW. | θ1−θ2=arcsin(0,05)≈0,05002086 rad, Q-Einspeisung je Ende (1−cos θ)/0,1≈0,01250782 pu, P-Verluste 0. RoCoF initial −0,5 Hz/s unter M4-Annahmen. Kein Rückschluss auf Nadir/dynamische Stabilität; Inselkontingenz und Grenzverletzung gesondert. | R020,021,023,028*,038,039,048 |
| B11 | Kohorten: 2030 Bestand 20 MW, technisch auslaufend Ende 2034; 2035 exogene Last 30, keine Alternativen, Ausbau ohne Bauverzug, x30/x35 frei, L≥10 Jahre, positiver CAPEX, keine 2030-Last. | 2035 müssen mindestens 30 MW aktive neue Kapazität verfügbar sein, nicht 10 MW unter unzulässiger Altbestandsfortschreibung. Bei ausschließlich positivem späterem diskontiertem Kostenunterschied und gleichen nominalen CAPEX bevorzugt PF den spätesten zulässigen Zubau. Bei Bauzeit >0 verschiebt sich Entscheidung; MY mit zu kurzem Fenster kann infeasible werden. | R002–007,027,040,043,044 |

R028* in B10 betrifft nur die allgemeine Trennung zwischen Netzmodell und physischer Validierung; Gas-Hydraulik muss mit einem eigenen Druck-/Massen-Orakel ergänzt werden. B07 enthält dafür zunächst den Transport-/Conversion-Test, nicht vollständige Hydraulik. B09 erlaubt Spill explizit; ohne Spill oder alternative Last wäre der Fall unter der genannten Einheit unlösbar. Diese Modellgrenzen sind Teil des Testvertrags.

### 6.1 Bewertung und Datencontract der Benchmarks

- Stufe A: analytisches Orakel (obige Werte), exakte diskrete Logik.
- Stufe B: unabhängige zweite Implementierung bzw. Standard-Netztool, je nach Modellklasse. Gleiche Formulierung, keine impliziten Defaults.
- Stufe C: reale oder anonymisierte größere Instanz mit Datenrechten, Referenzmetrik, Skalierung, Ressourcenbudget; noch nicht im Auftrag geliefert. Keine synthetischen Testresultate als reale ENTSO-E-Daten ausgeben.
- Numerische vorgeschlagene Baseline-Toleranz für kleine LP-Fälle: max(10^-6 in nativen Einheiten, 10^-6 relative Abweichung), AC-PF-Residual 10^-6 pu, MILP Zielgap und Feasibility separat protokollieren. Toleranzen vor Läufen je Algorithmus/Einheit einfrieren; diese sind **keine offiziellen Grenzwerte**. Bei Alternativoptima Objektiv und Zulässigkeit, nicht zwingend identische Einzelvariablen.
- Statistik: MC-Toleranzen anhand Fehlerbudget/CI, keine deterministische 10^-6-Regel für Stichproben.
- Negative Tests: fehlende Parameter, Null-/Negativgewicht, DST-Duplikat, unbalancierte Insel, unzulässiges Projekt im Baseline, H2/CH4-Doppelbelegung, Relaxation vs UC, unphysikalische SOC-/COP-/Q-Zustände.
- Ausgabefelder: benchmark_id, requirement_ids, fixture_hash, tool/release/commit, adapter_version, solver/settings/gap, walltime/RAM, objective und Zerlegung, residuals, solution_status, oracle_error, PASS/FAIL/UNQUALIFIED/NOT_APPLICABLE mit Begründung.
- Laufzeit und Skalierbarkeit erst nach korrekter Semantik vergleichen. Kein TOOL-PASS aus bloßer Datei- oder Solverstatus-Existenz.

## 7. Anforderungen an eine integrierte Modellarchitektur

### 7.1 Empfohlene funktionale Kette

    Gemeinsame Szenario-/Datenbasis (EU, nationale Rahmen, regionale Inputs)
      |-- Transformation/Capacity Expansion (Carrier, Y, Wetterfälle)
      |-- Chronologisches Marktmodell / UC / Flexibilität (Zonen)
      |-- Infrastruktur-Bedarf (IoSN-/IGI-Kandidaten, gemeinsame x)
      |-- Referenz- und Gegenfaktualgenerator -> CBA-Indikatoren
      |-- EVA -> probabilistische Adequacy (ERAA/national)
      |-- Markt-zu-Netz-Allokation -> DC/AC/Redispatch/N-1
      |       |-- Stabilitätsprüfung / Systemdienstleistungen
      |       |-- TSO-DSO-Schnittstellen / lokale AC-Feasibility
      |-- Gas/H2-Transport und physische Prüfung
      |-- Regionale Wärme-/Industrie-/EV-Planung
      +-- iterative Rückkopplung / Evidence Store / Vergleich

Szenario, Markt, CBA und Adequacy sind getrennte Studien mit eigenen Run-IDs. Kein Zirkelschluss: z. B. eine mit Projekt j optimierte Referenz nicht ohne methodische Genehmigung als angeblich projektfreie Baseline wiederverwenden. Kopplung erfolgt über explizite Eingabe-/Ausgabeverträge, nicht über unkontrolliertes Überschreiben des gemeinsamen Bestands.

### 7.2 Daten- und Schnittstellenverträge

| Vertrag | Mindestfelder / Semantik |
|---|---|
| Scenario | scenario_id, narrative, source, status, target_year, policy assumptions, carrier demand, capacities, CO2, fuel prices, geographical definition, assumptions ownership |
| Weather/Chronology | weather_id, source years, UTC timestamps, Δt, ν_t, π_w, missing flags; korrelierte Last/RES/Hydro/Temperatur |
| Asset | immutable asset_id, carrier ports, owner/location/region, status, existing/planned/candidate, capacity power/energy, efficiency basis, lifetime, build/retire year, cost/currency/price year |
| Network | node_id, branch_id, orientation, type AC/HVDC/PST/pipe/heat/transformer, electrical/hydraulic bases, topology version, limits/ratings, contingency set, mappings P/Γ/R |
| MarketDomain | zone IDs, NTC or CNEC/PTDF/GSK/RAM, reference dispatch/flows, loss convention, HVDC, date/time, method version |
| Dispatch | p/q/net position, cost/price definition, UC/status, reserve, storage SOC, ENS, curtailment, duals (if meaningful), solver/evidence |
| ProjectCase | project_id/group, commissioning, maturity, reference grid ID, PINT/TOOT, pair_id, inclusion/exclusion, changed input allowlist, indicator definitions |
| AdequacyCase | scenario/asset/economic viability result, weather/outage seed/probabilities, duration/ENS rule, correlated failure model, MC convergence/CI |
| InterfaceEnvelope | TSO-DSO connection ID, time-coupled P/Q bounds/polytope, baseline and reserve, local disaggregation feasibility, validity domain, residuals and provenance |
| StudyResult | model_class, requirement IDs, mathematical variant, objective decomposition, data hash, tool/release, run status, validity scope, independent oracle evidence |

Missing-data handling: UNKNOWN/MISSING/UNQUALIFIED statt Nullfüllung. Numerische Konventionen (MW/pu, MWh/HHV/LHV, positive Injektion, UTC) beim Import testen. Proprietäre oder vertrauliche Netzdaten nicht ohne Rechteprüfung weitergeben; anonymisierte und synthetische Fixtures strikt markieren.

### 7.3 Geographische und zeitliche Integration

- Europa: länder-/zonenübergreifende Energiebilanzen, gemeinsames Wetter und Austausch, interne Subzonen bei Bedarf; Landesquoten beschränken Aggregation gegebenenfalls, nicht die physischen grenzüberschreitenden Verbindungen.
- Deutschland: nationale genehmigte Kapazitäten, standortscharfe Regionalisierung, konsistentes EU-Randmodell. Detailnetz, Umspannwerke, HVDC, PST, Gas/H2-Korridore und Planungsmaßnahmen.
- Regionen/DSO: räumliche Verteilung der Lasten, dezentrale Anlagen, Anschluss-/Flexibilitätsrestriktionen; Top-down-Zielwerte mit Bottom-up-Potenzial, Netzen und kommunaler Wärmeplanung abgleichen.
- Übersetzung: Jahresenergien und Kapazitäten in Stundenprofile mit identischen Summen, Spitzen und Wetterkorrelation. Aggregation mit Erhaltung kritischer räumlicher und zeitlicher Merkmale. Vermeide zeitliche Glättung von Reserve-/Extremereignissen.
- Rückkopplung: nationaler Markt-/Ausbauplan → lokale Netzprüfung → zulässige Flex-/Kapazitätsgrenzen, Zusatzkosten oder validierte Feasibility-Cuts → erneute übergeordnete Lösung. Stop: definierte Konvergenz für Energiebilanzen, Schnittstellenflüsse, Kapazität/Kosten und keine ungelösten Verletzungen. Oscillation/Non-convergence melden, nicht stillschweigend accept.
- Strom-H2-Wärme-Gas: Umwandler und gemeinsam genutzte Assets besitzen eindeutige IDs; Stromverbrauch Elektrolyse/WP nur einmal, H2/Wärmeoutput separat; Strom-/Gasnetz CAPEX und externe Kosten nicht doppelt in regionaler und nationaler Zielfunktion.
- Daten-/Modellhierarchie erlaubt mehrere Solver. Ein Monolith ist nur dann sinnvoll, wenn alle Zeit-/Raum-/Physikannahmen und Lösbarkeit tatsächlich qualifiziert sind; ansonsten lose gekoppelte oder dekomponierte Module.

### 7.4 Vergleichslogik für nachfolgende Arbeiten

Je Requirement und Tool folgende Felder: Scope, Capability status (NATIVE_CONFIGURED / NATIVE_EXTENSION / WRAPPER_VALIDATED / EXTERNAL_TOOLCHAIN / UNSUPPORTED / UNKNOWN / N/A), mathematische Äquivalenz, Source URL und Pin, Datenvertrag, Benchmark-ID, Run-Evidenz, Gap/mitigation, Lizenz/Deployment. Nicht verfügbare Fähigkeiten nicht als Nullpunkt gegen einen spezialisierten Solver interpretieren, wenn sie außerhalb seines vereinbarten Profils liegen. Architekturvergleich auf Ebene von Toolchains zusätzlich zur Kernbibliothek. Getrennte Scorecards für Markt, Ausbau, CBA, ERAA, Netzphysik, DSO, Sektorkopplung und Reproduzierbarkeit; kein willkürlich gewichtetes Gesamtranking vor Owner-Entscheidung.

## 8. Power-Agent Reuse, Skills und Workflows

Die projektweiten Reuse- und Evidence-Regeln werden berücksichtigt (interne Architektur-/Projektanweisungen und relevante Abschnitte der Power-Agent-Wissensbasis konsultiert). Sie begründen den Workflow, **keine offizielle Planungsmethode**. Öffentliche Repositories am 27.11.2026 per GitHub-Metadaten/Commit-Abfrage und ausgewählten Quellen read-only geprüft. Branch jeweils main. Nachfolgende Pins dienen der Nachvollziehbarkeit der Inspektion, nicht als Integrationsfreigabe. Lizenz-/Security-/Dependencies-Review steht vor tatsächlicher Übernahme aus; keine Ausführung, kein Setup.

| Reuse-ID | Upstream / geprüfter Pin | Relevante Pfade / Entscheidung |
|---|---|---|
| PA01 | [PowerSkills](https://github.com/Power-Agent/PowerSkills/tree/636102954ff9522e7b161cbb2e3863746afa78cc) | powerskills-tool/skills/pypsa/SKILL.md, egret/SKILL.md, opendss/SKILL.md sowie powerskills-engineering/skills/operations-planning-mitigation/SKILL.md und contingency-mitigation/SKILL.md: ADAPT. Netz-/Input-Inspektion vor Solve, DC→AC/UC, Base Case, Kontingenz/Fehlerdiagnose. Keine Übernahme beispielhafter Sicherheitsgrenzen als Norm. Weitere Voltage/Thermal/Dynamics-Skills bei Folgereview suchen/prüfen. |
| PA02 | [PowerWF](https://github.com/Power-Agent/PowerWF/tree/a3c437146e7263a45db940edc5e4c66a4cd170cf) | cross_engine_validation/README.md: ADAPT. gemeinsamer StudySpec, Adapter, Comparator, Units/Time/Tolerances und unabhängige Resultate. Anwendbar auf Benchmarks, aber kein Nachweis bereits ausgeführter ESM-Vergleichsläufe. |
| PA03 | [PowerMCP](https://github.com/Power-Agent/PowerMCP/tree/10dbd9a8ef81bbf0e1c790ba4faca25e7f1af336) | PyPSA/README.md und pandapower/security_assessment.py: WRAP/ADAPT nach Prüfung. Dokumentierte PyPSA-Adapteroperationen (PF/Optimierung/Investition/N-1) sind nicht gleich der gesamten nativen PyPSA-Funktionalität. Commit 23.11.2026 mit topologiebewusster N-1/N-2-Prüfung, Inselbehandlung in ausgewähltem Code erkennbar; vollständige Korrektheit/Runtime nicht verifiziert. Für B02/B10 als Kandidat, fehlende Werte und Slack-Semantik prüfen. PowerIO/Interchange nur mit Roundtrip-Orakel. |
| PA04 | [PowerAgentBench](https://github.com/Power-Agent/PowerAgentBench/tree/77fe638482af94dd20ce28bfa4301658660d283d) | benchmarks/steady/level_1/README.md: ADAPT. IEEE39-basierter gestresster Basisfall, definierte Kontingenzen, Aktionen und Kosten-/Bewertungslogik als Vorbild für B02/B10; kein Ersatz für CBA-/ERAA-/Transformationsbenchmarks. |
| PA05 | [PowerFM](https://github.com/Power-Agent/PowerFM/tree/4c6e9b3dd1e035d7abf8c526b2947380b6667fa3) | README.md: RESEARCH / nicht als Produktionspflicht. Surrogate nur nach Fehler-/OOD-/Physikprüfung, R048. |
| PA06 | [Power-Agent Website](https://github.com/Power-Agent/power-agent.github.io/tree/9e47948d155278c5dc7ccb059ff8ac887b2ab7a8) | README.md: Discovery/Information, NOT_APPLICABLE als physikalischer Solver oder offizielle Planungsmethodik. |

Reuse-Entscheidung: bevorzugt bestehende mathematische Engines und Adapter, neue dünne Daten-/Orakelverträge nur für fehlende prozessübergreifende Semantik. Kein ungeprüfter Fork, keine Neuimplementierung komplexer Netzphysik, kein Ersatz der offiziellen Originalquellen durch Agent Skills. Die einzelnen Repositories wurden nicht vollständig dateiweise auditiert; ausgewählte Dokumentation/Codeausschnitte sind belegt. Insbesondere API-/Lizenzkompatibilität und numerische Tests sind noch HOLD.

### 8.1 Gates für den zentralen Vergleich

| Gate | Inhalt | ESM-A Status |
|---|---|---|
| G0 | Aufgaben- und Scope-Freeze, Authority, Originalquellen | abgeschlossen für diesen Bericht; einzelne aktuell gültige Fassungen U |
| G1 | toolneutrale mathematische Anforderungen / Prozessprofile | DRAFT_READY, Review erforderlich |
| G2 | Reuse Discovery, gepinnte Quellen, Capability- und License-Audit | Discovery/ausgewählte Inspektion abgeschlossen; vollständige Tool-/Lizenzprüfung HOLD |
| G3 | Architekturvarianten und Datenverträge | vorgeschlagen, keine Owner-Entscheidung |
| G4 | Benchmark-Spezifikation und Akzeptanz | analytische Fälle B01–B11 vorgeschlagen; Fixture-Freeze und unabhängige Prüfung HOLD |
| G5 | Implementierung/Adapter | NOT_AUTHORIZED |
| G6 | Solver-/Benchmarkkampagne und physikalische Validierung | NOT_AUTHORIZED |
| G7 | unabhängige Bewertung der fünf Kandidaten | nachgelagerter Auftrag |
| G8 | zentrale Konsolidierung und Owner-Entscheidung | HOLD |

## 9. Offene Fragen, methodische Risiken und Entscheidungen

| Risiko-ID | Offene Frage / Risiko | Priorität und Abhilfe |
|---|---|---|
| O01 | Sind die TYNDP-2026-IoSN-, CBA- und ENTSOG-Entwürfe inzwischen durch final gültige, abweichende Dokumente ersetzt? | Hoch. Vor Konformitätsbewertung finalen Status, Datum, Änderungen und Hash verbindlich nachziehen; Draft hier nicht als A. |
| O02 | Vollständiger Satz öffentlicher Eingangsdatensätze, Kandidaten, Wetterjahre/-gewichte, Netzaggregation, CNEC/GSK/RAM, Projektmaturity und Inbetriebnahme? | Hoch. Official-method fixture vs real data getrennt; bei fehlender Datenautorität UNQUALIFIED. |
| O03 | Exakter Referenz-/Counterfactual-Generator je Projektart, Horizont und Indikator, inkl. SoS-Kalibrierung und hybrider Projekte? | Hoch. PINT/TOOT und Projektgruppen im Datencontract; pair allowlist und Audit; Referenzen nicht aus IoSN ersetzen. |
| O04 | Welche ERAA-Methodik gilt für welchen Jahrgang einschließlich Übergangsplan 2026; EVA-Algorithmus, Preise/Entry-/Exit-Regeln und reale Stichprobenkonfiguration? | Hoch. S17/S18 getrennt pinnen; nicht aus allgemeinem Kostenminimum approximativ als offizielles ERAA ausweisen. |
| O05 | Welche nationalen NEP- und Szenariorahmenstände sind nach Konsultation tatsächlich bestätigt? | Hoch. S20 genehmigt, S21–23 als hier identifizierte Entwürfe behandelt; Nachtrag bei finaler Entscheidung. |
| O06 | Marktdesign: NTC vs FB, CNEC/RAM/minRAM, UC, Regelleistung, Day-Ahead/Intraday/Balancing? | Hoch. Separate Benchmark-/Marktprofile; keine Verwechslung von physical DC OPF und zonalem Clearing. |
| O07 | GF/PF/MY: Ist Vergleichshorizont derselbe, werden Asset-Lebensdauern, Bauzeiten, Preisbasis, Terminalwert und Unsicherheiten gleich modelliert? | Hoch. M1 und B04/B11 fixieren. |
| O08 | Auflösungsverlust bei Aggregation und repräsentativen Zeiträumen; Extremereignisse, saisonale Speicher und simultane DSO-Grenzen? | Hoch. Validierung gegen detaillierten Netz-/Zeitfall, systematische Fehlermetriken und Rückkopplung. |
| O09 | Proprietäre Produktionsmodelle und Solvereinstellungen (PLEXOS u. a.), konkrete GEMS-Rolle, Softwareversionen der offiziellen Produktionsläufe? | Mittel/hoch. Dokumentierte Rollen allein nicht als Laufnachweis. Lizenz-/Datenzugriff vor Reproduktion. |
| O10 | Gas/H2-Physik, Umrüstung, Linepack, hydraulische und Lastspitzenrestriktionen; zeitliche Kopplung mit Strom? | Hoch. Transport- vs Hydraulikmodelle trennen; zusätzliche analytische Druck-/Kompressor-/Massenbilanz-Fixtures definieren. |
| O11 | Welche technischen Stabilitätsgrenzen und Betriebsfälle gelten; welche Surrogate sind konservativ? | Hoch. Separates dynamisches Orakel, kein universeller SCR/RoCoF-Threshold und keine Gleichsetzung AC-PF mit Stabilität. |
| O12 | Integrierte DSO-/Wärmedaten, Anschlussinformationen und lokale Flexibilitätsverträge verfügbar? | Hoch. Datenschutz, Datenrechte, Feasibility-Envelopes und Machbarkeitsbelege. |
| O13 | Doppelzählung von CO2, Verlusten, Markttransfers, Flexibilität, Projektbenefits, Asset-Kosten? | Hoch. Kosten-/Indikatorledger, eindeutig identifizierte Assets, gemeinsame paarige Fälle, B05. |
| O14 | Toolvergleich: ein Tool oder integrierte Toolchain, welche Profile wie gewichtet? | Owner-Entscheidung. Zunächst getrennte Profil-Scorecards; keine universelle Rangliste. |
| O15 | Benchmarks: vollständige Maschinenfixtures, unabhängige Orakelprüfung, reale Netzfälle, Solverressourcen? | HOLD. B01–B11 sind Spezifikationen, keine Läufe; R042 verlangt nachgelagerte Freeze-/QA-Phase. |

**Explizite Scope-Entscheidungen dieses Berichts:** Deutschland als nationale Konkretisierung; europäische und regionale Modellierung über gemeinsam definierte Verträge; Prioritätsklasse P pro Prozess statt globaler Tool-Pflicht; analytische synthetische Benchmarks statt nicht autorisierter Solverläufe; eigenständiger Dokumentationsbranch und neuer Unterordner im Zielrepository. Kein formales Zertifikat über regulatorische Vollständigkeit. Keine Behauptung, alle Quellen oder alle Tool-Repositories vollständig zeilenweise auditiert zu haben. Quellenlinks sollen in der nachgelagerten Freeze-Phase mit Dateihashes, ggf. genauerer Absatz-/Seitenreferenz und finalem Status archiviert werden.

## 10. Übergabe an den zentralen Architektur- und Vergleichschat

Verwende ESM-A-R001 bis ESM-A-R050 als stabile Requirements und PR01–PR15 als Prozessprofile. Ordne nachfolgende Tool-Reviews und Benchmarkentwürfe darauf ab. Behalte S01–S30 als Quellenregister; neue offizielle Quellen mit neuer ID und dokumentierter Änderung ergänzen, nicht stillschweigend umdefinieren. Prüfe Benchmark B01–B11 vor Freeze auf mathematische Konsistenz und ergänze fehlende Gas-Hydraulik-, Stabilitäts- und skalierbare Realnetz-Fixtures.

Nächste Schritte **nur nach Freigabe**:

1. Aktuellen Status der maßgeblichen 2026er Methodiken und der deutschen NEP/Szenariorahmen verbindlich verifizieren; offizielle Eingangsdaten, Versions-/Hash-Manifest.
2. Unabhängige Review-Matrix je Tool/Release mit Requirements, nativer/gekoppelter Fähigkeit, Beleg und Gap.
3. Benchmark-Fixtures, unabhängige Orakel und Toleranzen einfrieren; Code-/Solverkampagne separat autorisieren.
4. Architekturvarianten anhand der prozessspezifischen Profile, nicht einer unqualifizierten Gesamtnote, bewerten; Owner-Entscheidung zur integrierten Toolchain.

**Abschlussstatus:** DOCUMENTATION_HANDOFF_READY / SCIENTIFIC_REQUIREMENTS_REVIEW_PENDING / NO_SOLVER_RUN / NO_CODE_CHANGE / NO_MERGE.

