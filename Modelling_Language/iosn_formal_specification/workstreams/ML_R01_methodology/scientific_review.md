# ML-R01 — Wissenschaftliche Gegenprüfung / Adversarial Methodology Review

**Reviewstand:** 2026-11-11 · **Status:** SELF-CONDUCTED_CRITICAL_REVIEW / INDEPENDENT_PERSON_REVIEW_NOT_OBTAINED / G1_BLOCKED.  
**Erstellt und kritisch geprüft im selben KI-Arbeitsprozess.** Dies ist **weder** ein organisatorisch unabhängig durchgeführter Peer Review **noch** ein ENTSO-E-/Methodology-Owner-Signoff. Ein fachlicher Prüfer außerhalb der Erstellung wurde nicht mandatiert. Alle festgestellten Quellen-, Daten- und mathematischen Lücken bleiben ausdrücklich offen.

## 1. Kontrollierte Prüfgrundlage

- Repository-Ausgangscommit **5c13d4d63f18d30c308997cd7a01f2977fcc6b7b**, BUNDLE-01R PR #25 Draft; neue Änderungen ausschließlich im ML-R01-Unterordner auf separatem Forschungsbranch.
- Aktive Baseline: 48 einzigartige IDs MA01-SR-001…050 mit Lücken **012 und 049**; 18 Prozessschritte P00–P17; 50 MA01-MR, darunter MR-012 und MR-049 als **upstream-externe Wetterselektion**.
- Primärquelle: **O26**, ENTSO-E *TYNDP 2026 Identification of System Needs Methodology*, *Version for Public Consultation*, 25 February 2026, §§2–5 + 6.1–6.3. **Veröffentlicht und konsultiert; Adoption und Wirksamkeit nicht verifiziert.**
- Historische Quelle H24 *TYNDP 2024 Identification of the System Needs Study Methodology*, *Version for ACER, European Commission and EU Member States Opinion*, 9 April 2025: §7.3.2 gedruckte S.42 zu LF ohne internen Kapazitätsdeckel; §7.3.1 S.36–38 als **rein historischer** Eligibilitätsvergleich. Nicht zur Schließung von MD-08/-14 verwendet.
- CBA4 §2.5.1 als extern referenzierte, eigenständig genehmigte Methodik; CBA4-Zulassung **nicht** auf IoSN übertragen.
- Projektvorgaben D1…D6, insbesondere **fünf CY1–CY5**, im Widerspruch zu O26s **drei anderen Wetterfällen pro Jahr**; D2 als **Forschungsprofil**, nicht als offizielle Quellenänderung.

## 2. Abdeckung — belegte Struktur, keine Modelllaufkonformität

| Prüfobjekt | Soll | Befund der dokumentenbasierten Gegenprüfung | Evidenzklasse |
|---|---:|---|---|
| Prozess-IDs P00–P17 | 18 | **18** einzeln mit neun Analysefeldern, Input/Output/Abhängigkeit und Forschungs-TBD in process_semantics_P00_P17.md | REPOSITORY_SOURCE_STRUCTURE / NO_EXECUTION |
| Aktive MA01-SR | 48 | **48** eindeutige SR in source_and_assumption_traceability.csv, referenziert in Prozess-/Methodiksemantik | REPOSITORY_SOURCE_STRUCTURE |
| MA01-MR | 50 | 48 aktive MR→SR-Paare, MR-012/049 als upstream-externe Wetterselektion, ohne neue aktive SR | SOURCE_SCOPE_CHECK |
| Mathematische Verpflichtungen | 18 | M01–M18 mit Quelle/Abstraktionsklasse und Verifikationsdesign | DESIGNED_NOT_RUN |
| Prozess-zu-Mathematik | P00–P17 | Je Schritt wissenschaftliche Zuordnung; P00 ist Research-/Governance-Gate ohne neue LP-Pflicht | TRACEABILITY_STRUCTURE |
| Bekannte Ownerentscheidungen | 21 | MD-01…MD-20 + MA02-CL-001 vollständig ins Register übernommen, **21/21 OPEN** | OWNER_STATUS_NOT_APPROVED |
| Projektentscheidungen | 6 | D1–D6 als Forschungsprofil von O26-Klauseln unterschieden | USER_DECISION_SCOPE |
| Historische Ergänzungen | 2 | H24 §§7.3.1/7.3.2 mit Version, Druckseiten, Ergänzungsgrund und unbestätigter 2026-Gültigkeit | HISTORICAL_CONTEXT_ONLY |
| Neue wissenschaftliche Forschungslücken | 12 | FR-01…FR-12 als TBD, **nicht** als neue verbindliche Ownerbeschlüsse | RESEARCH_TBD |
| Native IoSN-Modell-/Daten-/Netzläufe | – | **0** durch ML-R01 durchgeführte vollständige LP-/Netzreduktion-/Hydro-/H2-/KPI-Rechnungen | NOT_EXECUTED |
| Personell unabhängiger Review | – | **Keiner**; Prüfung im selben KI-Erstellungsprozess | NOT_OBTAINED |

Ein erfolgreicher Abdeckungstest belegt nicht, dass die 48 Anforderungen **vollständig realisiert oder mathematisch nachgewiesen** sind. Die Matrix enthält für einzelne SR bewusst nur Struktur- oder Symbolprüfungen, weil notwendige numerische Akzeptanzorakel fehlen. Ein Nichtvorliegen des Orakels bleibt **BLOCKED_ORACLE**, kein positiver und nicht automatisch ein negativer Modelltest.

## 3. Kritische Findings ML-R01 (Forschungsreview, nicht bestehende BUNDLE-01-Findings schließen)

| ID | Schwere | Adversarial-Befund | Wissenschaftliche Gefahr / Gegenprobe | Verfügung |
|---|---|---|---|---|
| R01-F01 | CRITICAL | **O26-D2 Wetterprofil divergiert**: O26 je drei jahresspezifische Wetterfälle/Gewichte, D2 fünf CY-IDs und identisches \(\pi\) über 2035/2040/2050 | Unbemerktes Vermischen verfälscht Erwartungswerte und Vertragsumfang; expliziter Source-Profile-Delta-Test | OPEN_PROFILE_DIVERGENCE; **nicht** O26 oder MA01 umschreiben |
| R01-F02 | CRITICAL | O26 ist ein **Konsultationsentwurf** ohne verifizierte Adoption/Original-SHA256 | Jede als „offizielle verbindliche IoSN-Methode“ betitelte Anforderung wäre voreilig | OPEN_MD-01; späterer Norm-Delta-Abgleich nötig |
| R01-F03 | CRITICAL | Diskont-/Blockjahreskonvention unbestimmt, beschädigter O26 §4.6-Verweis | Mehrere plausible Barwertoperatoren ergeben verschiedene Ausbauvektoren | OPEN_MD-02; \(C^{inv}=\mathcal V(\cdot)\) statt erfundene Formel |
| R01-F04 | CRITICAL | Physischer DC-LF und DC-Marktlink sind semantisch verschieden | Drei-Bus-Ring mit freiem Kandidatenmarktlink vs Kirchhoff-Kandidat zeigt unterschiedlichen Feasible Set | OPEN_MD-09; M05 vs M07 separat |
| R01-F05 | CRITICAL | Stufe 1/2: genaue Teilübernahme, neue Kostenbasis, Kandidatenreste unklar | Joint-Optimierung ohne Priorität oder Stage1 doppelt angerechnet ändert Zielfunktion/Feasible Set | OPEN_MD-07; keine fiktive Fixierungsregel |
| R01-F06 | HIGH | Netzreduktion: keine originalen Detailnetze, PTDF-/LODF-/N-1-Oracle und akzeptierten RMSE-Grenzen | 102 Zonen oder Flusssumme ist kein elektrischer Gütenachweis | OPEN_MD-03/-13/-15 |
| R01-F07 | HIGH | LF-Kapazitätsfreiheit darf keine Kirchhoff-Freiheit bedeuten | Physischer Maschenfluss muss bei deaktivierten internen Caps weiterhin KVL erfüllen | M05/M06 unterscheiden; H24 nur historischer Beleg |
| R01-F08 | HIGH | Zeit-/Dimensionsachsen: Kalender, DST, Schaltjahr, Zeitgewicht und ENERGY vs POWER teilweise offen | Test MW × h ↔ MWh, VoLL × ENS ↔ EUR, stündliche Datengleichheit | OPEN_MD-12; UTC D4 ist fest, kein ETL-Default |
| R01-F09 | HIGH | H2-Netzausbau exogen; Preis-/Konversionseffekt und Präexpansionsfreeze offen | Versehentliche H2-Netz-Entscheidungsvariable oder nur kumulative statt stündliche Elektrolyse-Fixierung | OPEN_MD-10; M15/M18 |
| R01-F10 | HIGH | Speicher-/Hydro-/DSR-Verlust-/Zeitkonventionen und Energieendzustände offen | Energy balance trotz formal korrektem LP bei unzulässiger „freier Energie“ verletzt | OPEN_MD-06/-16; Beispielgleichungen als I markieren |
| R01-F11 | HIGH | Offshore-Seeumweg 10–15 % ist **Spanne** und Ziel-/Routen-/Kosten-Abgrenzung nicht abschließend | 12.5 % oder pauschale Route wäre unbelegte Annahme | OPEN_MD-05/-14; M17 symbolisch |
| R01-F12 | HIGH | Ergebnisidentität: LP-Mehrfachoptima, Reporting-KPI und Kleinmengenfilter ohne Oracle | gleiche Zielfunktion ≠ gleiche zulässige Menge; verschiedene Optima ≠ automatisch falsch | OPEN_MD-04/-17; separate Ergebnisbeobachtungen |
| R01-F13 | HIGH | Statische Vollständigkeitsprüfung kann als methodischer PASS fehlinterpretiert werden | Traceability-CSV ersetzt nicht Originaldaten-/Runvalidierung oder personelle Unabhängigkeit | D3 fail-closed, D5-A1 risikobasierte Orakel |
| R01-F14 | MEDIUM | Historisches H24 §7.3.1 mit CBA4 §2.5.1 könnte scheinbar 2035-Projektreife a/b/c entscheiden | Unterschiedliche Study-Year-Regeln nicht ohne zuständigen Methodology-/Starting-Grid-Owner vereinigen | OPEN_MD-14/MA02-CL-001 |
| R01-F15 | MEDIUM | Beispielgleichung M05 kann No-load-/PST-/HVDC-Terms **doppelt** erfassen, wenn Quellenkalibrierung gemeinsame Effekte enthält | Kalibrierter Parametervektor muss eindeutig festlegen, welche Effekte bereits in \(f^0\) stecken | ILLUSTRATIVE_ONLY; Referenzrechnung MD-03 |
| R01-F16 | MEDIUM | N-1-LODF-Formel nicht ohne Weiteres gültig bei Inselbildung oder singulärer PTDF-Basis | Insel-/Ausfalltest als Negativfall; ggf. eigener Oracle-Pfad | ILLUSTRATIVE_CONDITIONAL; MD-03/-15 |

**Disposition:** Alle 16 Forschungsreview-Findings sind **OPEN bzw. RESEARCH-QUALIFICATION-PENDING**. Das bedeutet nicht, dass 16 zusätzliche formale BUNDLE-01-Findings eröffnet oder bestehende 23 Findings ersetzt wurden. Kein Owner-/Methodikentscheid erfolgt.

## 4. Mathematische Plausibilitäts- und Gegenbeispieltests — Bewertung des Teststatus

### 4.1 Kostendimensionen

- **Einheitentest auf Papier:** EUR/MWh × MW × h = EUR. VoLL in EUR/MWh muss mit ENS in MWh und nicht als nacktes Produkt mit Lastabwurfleistung MW verrechnet werden.
- **Doppelzählungstest als Entwurf:** \(\sum_c\pi_c=1\) macht die Wetterwahrscheinlichkeiten zu normierten Fällen, aber nicht zu fünf unabhängig getroffenen Investitionsentscheidungen. Jede bilanzierte Investition ist genau einmal im \(I(x)\)-Teil abzubilden.
- **Ergebnis:** dimensionsanalytische Argumentation **durchgeführt**, jedoch keine Source-Input-Kostenreproduktion, kein Solverfall, keine Währungs-/Barwertfreigabe. Status **SCI_REASONING_ONLY**.

### 4.2 Elektrische Physik

- **Dreiknotentest als Design:** Eine Netzschleife aus drei linearen Zweigen mit begrenzten Impedanzen und einem frei steuerbaren Kandidatenlink unterscheidet die Feasible Sets „KVL-Bestandsnetz + NTC-link“ vs „KVL-Bestandsnetz + AC-Kandidatenbranch“. Ohne Winkel-/Zyklustests ist ihre Gleichsetzung wissenschaftlich nicht gedeckt.
- **LF-Verwechslungsprüfung:** Kein internes Interzonen-Thermallimit ist **keine** Freistellung von KVL/DC-Netzequivalenz, Energiebilanz oder anderen technischen/Policy-Restriktionen.
- **Ergebnis:** Modellkriterium **entworfen**, physikalische Originalnetze, N-1-/PTDF-/LODF-Abgleich und numerische Residuen **nicht ausgeführt**.

### 4.3 Stufenoptimierung und Mehrfachoptima

- **Kontraindikator:** Stage1 erhält nur reale Transmissionkandidaten; ein aggregiertes LP mit gleichzeitig verfügbaren konzeptionellen Alternativen kann ein anderes Portfolio wählen. Die genaue Stufe1/2-Übergabe ist deshalb methodisch relevant.
- **Mehrfachoptima:** Unterschiedliche optimale \(x\) können dieselbe Zielfunktion haben; Portfolio-IDs ohne zulässiges Bewertungsverfahren nicht als alleinigen Konformitätsprüfer verwenden.
- **Ergebnis:** fachliche Nichtäquivalenz plausibilisiert, keine Berechnung eines echten IoSN-Stufenfalls; **MD-07/-17 offen**.

### 4.4 Storage, Hydro und H2

- **Erhaltungscheck:** Batterie \(e_{t+1}\) muss MWh-Mengen fortschreiben, Hydrovolumen benötigt Wasser-/Energieäquivalenz, Elektrolyse/Rückstrom getrennte H2/Strom-Knotenbilanzen.
- **H2-Freeze:** Bei fixierter *stündlicher* Elektrolyselast müssen entsprechende \(\widehat p^{EL,pre}_{y,c,t,h}\) für alle relevanten Indizes wiedergefunden werden; identische Jahresenergiemenge ist nicht äquivalent.
- **Ergebnis:** Einheiten-/Strukturkritik, **keine qualifizierten Parameter oder Operating-Model-Orakel**, keine mathematische Abnahme.

### 4.5 Historische Ergänzungen

H24 §7.3.2 wird als **nichtnormativer Kontrollvergleich** für M06 geführt, weil O26 §3.9 die genaue technische „unbegrenzte Kapazität“ nicht vollständig prüfbar spezifiziert. H24 §7.3.1/alte maturity-Kategorien sind ausschließlich **fehlertolerante Quellenkommentare**, keine 2035-Projektentscheidung. Sollte eine neuere genehmigte IoSN-2026-Fassung später anders lauten, gilt diese bei nachgewiesener Autorisierung vorrangig. **Kein** als „no change verified“ gekennzeichneter Delta-Befund ohne beide Originaldokumente.

## 5. Qualitäts- und Abschlussentscheidung dieser Forschungsprüfung

| Entscheidungsdimension | Prüfergebnis | Konsequenz |
|---|---|---|
| Wissenschaftliche **Beschreibbarkeit** | ACHIEVED_WITH_LIMITS | Wesentliche Verfahrens-/Bilanz-/Physik-/Stufeninvarianten als Referenzentwurf vorhanden |
| P00–P17 Dokumentationsabdeckung | DOCUMENTED_18_OF_18 | Keine Behauptung, jeden Schritt ausgeführt zu haben |
| MA01-SR-Traceability | DOCUMENTED_48_OF_48 | D1-Baseline bleibt einzig aktiv |
| O26-Methodikgenehmigung und originaler Filehash | NOT_VERIFIED | MD-01 offen |
| Datenfreigabe/Originalmodell- und Laufdaten | NOT_VERIFIED | Kein numerischer Vollkonformitätsnachweis |
| Mathematische Modellläufe, N-1, KPI, LP-Optimumszeugnis | NOT_EXECUTED | Wissenschaftlicher Prüfentwurf, keine positive Implementierungsbewertung |
| Qualifiziert unabhängiger Review | NOT_OBTAINED | Dieser Text ersetzt keinen unabhängigen Reviewer |
| G1 | **BLOCKED** | Keine Freigabe für normative Contract-/Sprach- oder Datenumsetzung |

**Kritische Schlussfolgerung:** Unter dem definierten O26-Entwurfs-/D1–D6-Forschungsprofil sind invariantenbasierte, toolunabhängige wissenschaftliche Anforderungen gut formulierbar. Eine vollständige normative, daten- und numerisch beweisbare IoSN-Spezifikation ist mit diesem Stand **nicht** möglich; deshalb bleiben Methodikversion, Ownerparameter, Datenstände und Akzeptanzorakel kontrolliert offen. **Keine neuen allgemeinen Robustheitsanforderungen, keine Wetterjahrselektion, keine Architekturentscheidung, keine Freigabe.**
