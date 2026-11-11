# ML-R01 — Wissenschaftliche IoSN-Methodikreferenz (nichtnormativ)

**Arbeitsstand:** 2026-11-11 · **Status:** RESEARCH_SPECIFICATION / NOT_APPROVED / G1_BLOCKED · **Basis:** BUNDLE-01R PR #25, Commit 5c13d4d63f18d30c308997cd7a01f2977fcc6b7b.  
**Aufgabe:** Methodology-to-Scientific Specification; weder Sprach-/Softwarearchitektur noch ausführbare Optimierung. Die MA-01-Baseline bleibt unverändert. Diese Beschreibung ist ein Vorschlag für überprüfbare, von einer konkreten Implementierung unabhängige wissenschaftliche Semantik.

## 1. Quellen, Geltungsraum und Evidenzklassen

| Kürzel | Exakt identifizierter Gegenstand | Fundstelle | Verwendung / Autorität |
|---|---|---|---|
| O26 | ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, **Version for Public Consultation, 25 February 2026**, 65 Druckseiten | §§2–5 und Anhänge 6.1–6.3; [Original-PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) | Neueste in der Untersuchung bis 11.11.2026 positiv verifizierte fachlich einschlägige **2026er Forschungsreferenz**, **keine nachgewiesene Adoption** |
| P26 | ENTSO-E, *TYNDP 2026 Identification of System Needs methodology: Public Consultation*, 26.02.–03.04.2026 | [Konsultationsseite](https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/) | Bestätigung der Konsultation, keine Freigabe |
| H24 | ENTSO-E, *Identification of the System Needs Study Methodology – TYNDP 2024*, **Version for ACER, European Commission and EU Member States Opinion, 9 April 2025**, 97 PDF-Seiten | §7.3.2, **Druckseite 42**, [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2024/foropinion/SystemNeedsMethodology.pdf) | **Historischer Kontrollbeleg**: LF-Referenzsimulation mit unbegrenzten internen Interzonen-Kapazitäten bei unveränderten Impedanzen; ergänzt nur die Interpretation von O26 §3.9, **nicht normativ** |
| H24-B | Dasselbe H24-Dokument | §7.3.1, **Druckseiten 36–38** | Historischer Entscheidungs-/Datenkontext zur Projektreife a/b/c; **kein Ersatz** für einen 2035-Eligibility-Crosswalk unter O26/CBA4, MD-14 und MA02-CL-001 bleiben offen |
| CBA4 | ENTSO-E, *4th ENTSO-E CBA Guideline for Grid Development Projects*, finale von der EC genehmigte Fassung, 2024 | §2.5.1, [PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf) | Fremdmethodik **nur** über Verweis O26 §3.4 auf Startnetz-Projektreife relevant; genehmigte CBA4 ist **keine** Genehmigung von O26 |

**Begründung der historischen Ergänzung:** O26 §3.9 nennt das Abschalten interzonaler Kapazitätsbeschränkungen im primären LF-Lauf, aber keine vollständig testbare technische Konvention. H24 §7.3.2 bestätigt als älterer Ablaufbeleg, dass die Impedanzbeziehungen grundsätzlich erhalten bleiben. Der aktuelle O26-Text hat Vorrang; identische Formulierungen sind kein Nachweis gleicher Projektprofile. Für die O26-Lücke der 2035-Projektreife dienen H24 §7.3.1 und CBA4 nur als *Fragestellen*, nicht als zusätzliche gültige Kriterien. **Autorisierung beider historischer Übernahmen für 2026: TBD.** Kein älterer Zahlenwert wird für O26 verbindlich gemacht.

Die SDC-Minuten Februar 2026 erwähnen eine erst vorgesehene schriftliche Genehmigung; eine wirksam freigegebene spätere IoSN-Fassung wurde nicht positiv belegt. Original-PDF-Byte-Hashes, Adoption und eine mögliche tatsächliche Nachfolgeversion sind **NOT_VERIFIED**. Ein negativer Webtreffer beweist keine Nichtexistenz (MD-01). Bezugsquellen und Klassifikation werden im CSV je Ableitung fortgeführt.

### Belegsemantik

| Tag | Bedeutung | Darf als verbindliches O26-Erfordernis ausgegeben werden? |
|---|---|---|
| **O26-EXPLICIT** | In der konsultierten 2026-Fassung ausdrücklich beschrieben | Nur als **Entwurfsreferenz**, nicht als freigegebene Methodik |
| **O26-DESCRIPTIVE** | Methodischer Kontext/Ziel, ohne vollständig bestimmten Algorithmus | Nein; zusätzliche Regeln als Ableitung markieren |
| **H24-CONTEXT** | Ältere Ergänzung/Kontrolle mit benannter Seite | Nein; nie bei Widerspruch Vorrang vor O26 |
| **D1–D6** | Vom Projektauftrag vorgegebene Design-/Governanceentscheidungen | Nur innerhalb dieses Forschungsprofils, **nicht** ENTSO-E-Autorität |
| **SCI-DERIVED** | Wissenschaftliche Invariante aus Methodenbeschreibung und dimensionsrichtiger Formulierung | Als überprüfbarer wissenschaftlicher Vorschlag |
| **EQUIVALENT** | Mathematisch gleichwertige Darstellungen unter expliziten Voraussetzungen | Ja, sofern dieselben Ein-/Ausgabe- und Nebenbedingungssemantiken |
| **ILLUSTRATIVE** | Beispielgleichung, die nicht eindeutig durch Methode determiniert ist | Nein; keine verdeckte Defaultregel |
| **TBD** | Fehlender Parameter, Referenzwert, Ownerentscheid oder Orakel | Muss offen bleiben |

## 2. Konfliktfreie Arbeitsprofilierung D1–D6

1. **D1:** einzige aktive vorläufige SR-Baseline sind die **48 MA01-SR** (IDs mit Lücken, insbesondere kein SR-012 oder SR-049). Die 50 MA01-MR enthalten die beiden ausgenommenen Wetterselektions-MR-012/-049.
2. **D2:** fünf **extern ausgewählte** Wetterfall-IDs **CY1–CY5** für jedes Studienjahr 2035, 2040 und 2050. Gewichte \(\pi_c\) sind für alle drei Studienjahre *identisch*, Werte **TBD**; keine Berechnung/Selektion von Wetterjahren. **Explizite Quellenabweichung:** O26 §3.7, S.19–20, nutzt **jeweils drei andere, jahresspezifische** Wetterfälle und Wahrscheinlichkeiten. D2 ist ein **Forschungsprofil**, keine behauptete Textänderung oder Freigabe der O26.
3. **D3:** **Fail-Closed** für verpflichtende wissenschaftlich bestimmte Anforderungen: ohne erforderlichen Nachweis kein PASS; offene Ownerinhalte bleiben **BLOCKED/TBD**, weder erfundene Fehler noch Erfolge.
4. **D4:** **Kanonische UTC-basierte Zeit- und Einheitensemantik:** eindeutige Intervalle \([t,t+\Delta t)\), dimensionaler Bezug (MW, MWh, H2-Einheiten, EUR/Preisjahr) und explizite Quellzeitabbildung. DST-, Schaltjahr-, Fehlstunden-, Zeitaggregation- und Gewichtstoleranz bleiben MD-12-TBD.
5. **D5-A1:** risikobasierte mathematische Verifikation: Hochrisikopflichten zuerst mit strukturellem, analytischem und kleinformatigem Referenzorakel; keine fiktiven numerischen Toleranzen und keine Gleichsetzung statischer Tests mit modellbasierter Konformität.
6. **D6-A:** gemeinsamer wissenschaftlicher Requirements-Contract, **unabhängige Toolimplementierungen**. Diese Referenz definiert Beobachtungssemantik, nicht API/DSL, Komponentenarchitektur, Modellierungsbibliothek oder Solver.

**Abgrenzung:** Vorbereitende Forschung kann fortgeführt werden; **G1 bleibt BLOCKED**, normative Methoden- und Datenfreigabe sind nachgelagert. Verifikation der Auswahl von CY1–CY5 ist außerhalb dieses Auftrags.

## 3. Fachliche Objekte und kanonische Semantik

| Symbol/Objekt | Bedeutung | Identität/Einheit | Beleg |
|---|---|---|---|
| \(Y\) | Separat gerechnete Horizonte | \(\{2035,2040,2050\}\) | O26 §3.2; MA01-SR-002 |
| \(C\) | Exogene Wetterfallmenge | \(\{CY1,\ldots,CY5\}\), identisch je \(Y\) | D2; O26-Abweichung dokumentiert |
| \(\pi_c\) | Szenariowahrscheinlichkeit | \(\pi_c\ge0,\ \sum_c\pi_c=1\), gleiche Werte je \(Y\), Zahlen TBD | D2; SCI-DERIVED aus O26 §3.1.1 |
| \(T_{yc}\) | Zeitschritte einer Eingabereihe | UTC-Intervall samt Dauer \(\Delta t\), Repräsentativitätsgewicht nur falls freigegeben | D3; MD-12 |
| \(N^E,N^H\) | Elektrische und Wasserstoffzonen | Stabile Zonen-/Sektoridentität | O26 §§3.3,3.8 |
| \(G,L^E,L^H,K,S\) | Erzeuger, reduzierte Stromleitungen, exogene H2-Leitungen, Kandidaten, Speicher | Asset-ID, Port-/Zonenbezug, Einheit, Status | O26 §§3.4,3.8,4.1,4.5 |
| \(x_{y,k}\) | Investitionsumfang im Jahr \(y\) für Kandidat \(k\) | MW bzw. durch Kandidatentyp definierte Dimension | O26 §3.1.1 |
| \(u_{y,c,t}\) | Wetterabhängiger zulässiger Betrieb | MW, MWh, H2-Einheiten nach dokumentierter Dimension | O26 §§3.1.1,3.3–3.6 |
| \(R_y\) | Ergebnis-/Nachweis-Paket | Szenario, Input-Release, Modellklasse, Stage, Portfolio, Zielfunktionsteile, Prüfstatus | SCI-DERIVED, D5/D6 |

**Wetterfall-Identität ist kein Zeitindex.** Die Bezeichnung CY1–CY5 kann bei mehreren Studienhorizonten dieselbe Fallidentität tragen, jedoch können Profile und Stundenanzahlen je \(y,c\) verschieden sein. Eine globale Gewichtung *über* 2035, 2040 und 2050 wird durch D2 nicht eingeführt. **MW \(\times\) h = MWh**; Kapazitäten, Energie, Kostenströme und diskontierte Barwerte dürfen nie ohne Einheitentransformation summiert werden. \(\pi_c\) ist dimensionslos.

## 4. Wissenschaftliches Prozessbild (keine Orchestrierungsarchitektur)

~~~mermaid
flowchart TD
  P00[\"P00 Quellen-/Forschungsprofil\"] --> P01[\"P01 Horizonte + Szenario\"]
  U[\"Externes CY1–CY5-Manifest\"] --> P02[\"P02 Wetterfallannahme\"]
  P01 --> P02 --> P03[\"P03 Zeit- und Marktdatausrichtung\"]
  B[\"2025-Netz / Projekt- und Offshorequellen\"] --> P04[\"P04 Startnetz 2035\"]
  P04 --> P05[\"P05 Clustering\"] --> P06[\"P06 Netzreduktion\"]
  P06 --> P07[\"P07 Zonale Datenallokation\"]
  P03 --> P07
  P07 --> P08[\"P08 Strom/H2/Hydro/DSR\"]
  P01 --> P08
  K[\"Exogene Kandidaten und Kosten\"] --> P09[\"P09 Kandidaten-/Kostenregister\"]
  P08 --> P10[\"P10 reale Kandidaten LF-LP\"]
  P09 --> P10
  P10 --> P11[\"P11 Rest/konzeptionell/offshore LF-LP\"] --> P12[\"P12 Speicher 2040/2050\"]
  P12 --> P13[\"P13 Vergleich intern beschränkter Dispatch\"]
  P12 --> P14[\"P14 Frozen-H2-Sensitivität\"]
  P12 -. \"optional\" .-> P15[\"P15 OPF-Zusatzanalyse, LF-Deckel\"]
  P13 --> P16[\"P16 Systembedarf und Reporting\"]
  P14 --> P16
  P15 -. \"optional\" .-> P16
  P16 --> P17[\"P17 Forschungsreview\"]
~~~

Reihenfolge und Zwischenstände sind fachliche **Abhängigkeitssemantik**; Datenfluss- oder Workflow-Implementierung bleibt frei. Separate Zieljahre und Stufen werden nicht zu einer frei erfundenen dynamischen Mehrjahresinvestitionsrechnung zusammengezogen. Die vollständige, zeilenweise Analyse P00–P17 findet sich in **process_semantics_P00_P17.md**.

## 5. Kern des wissenschaftlichen Optimierungsvertrags

Für jedes \(y\in Y\) sind Investitionen \(x_y\) über alle fünf Wetterfälle gemeinsam und Betriebsentscheidungen \(u_{y,c}\) wetterabhängig. Die **Struktur** aus O26 §3.1.1 (S.12–14) lautet:

\[
\min_{x_y,\{u_{y,c}\}_{c\in C}}
\quad I_y(x_y)+\sum_{c\in C}\pi_c\,Q_{y,c}(x_y,u_{y,c}),\qquad
x_y\in X_y,\quad u_{y,c}\in \mathcal U_{y,c}(x_y).
\]

Hier ist \(I_y\) eine **einmal** angerechnete, konsistent bewertete Investitionskomponente, \(Q_{y,c}\) ein operationales Kostengefüge inkl. gegebenenfalls nicht versorgter Energie. Die Menge \(\mathcal U\) umfasst Nodalbilanzen, physische reduzierte AC-Äquivalente **unter DC-Lastflussapproximation**, technische Einheitenlimits, sektorale Kopplungen, exogene Klimareihen und Planungsrestriktionen. Operative Kosten können aus Dispatch, Brennstoff, Emissionen, Speicherbetrieb und ENSE bestehen, soweit die jeweilige Quelldaten- und Kostenabgrenzung sie vorsieht. **Offen** sind beispielsweise Abschreibungs-/Barwertlogik, Blockjahre und die genaue Abgrenzung aller Kostenterme (MD-02).

**Invariante M01 — Nichtantizipativität:** Ein Investitionsvektor \(x_{y}\) pro Zieljahr, nicht ein nach Wetterfall auswählbarer \(x_{y,c}\). Die Korrelation/Abhängigkeit zwischen verschiedenen Wetterfall-Dispatches ergibt sich allein über den gemeinsamen Investitionsraum und explizit gekoppelte methodische Variablen. Ein Worst-Case-/CVaR-/Minimax-Ansatz ist **nicht** durch die bloße Bezeichnung „robust“ in O26 gedeckt.

**Invariante M02 — Wettergewichtung:** \(\pi_c\) multipliziert nur die **je Wetterfall** entstehenden erwarteten Größen; keine fünffache Investitionskostenbelastung und keine doppelte Energie-/Zeitgewichtung. Ein Multiplikator \(\Delta t\) ist erforderlich, wenn Betrieb in MW und Kosten in EUR/MWh vorliegen. Tatsächliche Stichproben-/Repräsentativitätsgewichte und Stundenkalender sind **TBD**.

**Invariante M03 — Elektrische Bilanz:** Für jeden Stromknoten, jedes relevante UTC-Intervall und jeden Wetterfall gilt vorzeichenkonsistente Nettoerzeugung + Entladung + Importe + Lastabwurf = Nachfrage + Ladung + Exporte + Umwandlungslast, jeweils in MW. Nicht bediente Energie ist ein **integrierter** Wert MWh, nicht unbesehen dieselbe Größe wie Lastabwurfsleistung MW.

**Invariante M04 — zwei DC-Begriffe:** Die bestehenden/reduzierten elektrisch vermaschten Interzonenleitungen respektieren DC-Lastfluss, Kirchhoff und die aus P06 hergeleiteten physikalischen Äquivalentparameter. **Ausbaukandidaten** in P09–P11 sind dagegen steuerbare **DC-Marktlinks mit NTC-Wirkung**, sogar wenn die vorgeschlagene physische Technologie AC ist (O26 §4.5.2, S.37). Ihr Transport ist eine Handelsübertragungsvariable und darf nicht stillschweigend als neue Kirchhoff-AC-Leitung behandelt werden.

**Invariante M05 — LF/OPF:** Bei der **primären LF-Expansion** bleiben physikalische Maschenbeziehungen erhalten, jedoch werden die *internen Interzonen-Kapazitätsgrenzen* nicht als bindende Limits angesetzt (O26 §3.9, S.29). P13 vergleicht mit/ohne Portfolio in gesonderten Dispatchrechnungen **mit** internen Grenzen. Eine optionale OPF-Expansion P15 ist separat auszuweisen und durch das LF-Portfolio gedeckelt; die exakte Obergrenzenabbildung ist MD-08-TBD.

**Invariante M06 — Kandidaten/Stufen:** Stufe 1 reale On-/Offshore-Transmission als LP; Stufe 2 verbleibende reale + konzeptionelle Onshore + theoretische Offshore-Korridore als LP unter korrekter Anrechnung von Stufe 1; Speicherentscheidung getrennt, endogen erst 2040/2050. Für LP-Kandidaten \(0\le x_{y,k}\le X^{\max}_{y,k}\). Regeln zur Übernahme teilweise ausgewählter Kandidaten sind **MD-07-TBD** und dürfen nicht als mathematisches Faktum vorgegeben werden.

**Invariante M07 — Netzreduktion:** Zonenpartition, relevante Engpässe, Äquivalenzimpedanzen, Nullbilanz-Flüsse, Meshregeln, HVDC-/PST-Effekte und vier saisonal/richtungsabhängige N-1-Transferkapazitäten werden aus der detaillierten elektrischen Referenz abgeleitet (O26 §§3.8.1–3.8.3 und Anhang 6.1). Unberechtigtes Aufsummieren von physikalischen Leitungsratings ist kein Ersatz für LODF/N-1-Kapazitätsableitung. Qualitätsgrenzen sind **MD-03/-13/-15-TBD**.

**Invariante M08 — sektorale Betriebsfähigkeit:** Strom- und H2-Bilanzen mit verlust-/wirkungsgradkonsistenten P2G- und H2-zu-Strom-Prozessen; H2-**Netzausbau** ist exogen und darf nicht in die elektrischen Expansionsvariablen überführt werden (O26 §§3.3,3.6). P14 verwendet ein nachweisbar eingefrorenes *präexpansives* zeitlich/zonal aufgelöstes Elektrolyseprofil; konkrete Freeze-Semantik MD-10-TBD.

**Invariante M09 — intertemporale Physik:** Speicherladestand und gegebenenfalls Hydro-Reservoire respektieren Energieerhaltung, Lade-/Entladegrenzen und zeitliche Zustandsfortschreibung. Hydrotypen aus O26 §4.3: Run-of-River, Pondage, Reservoir, Open-Loop-Pump, Closed-Loop-Pump. DFT §4.4 unterscheidet implizite außerhalb und explizite innerhalb des Markts angebotene DSR. Endbedingungen, Kosten, Restriktionen und DSR-Intertemporalkopplung **MD-06/-16-TBD**.

**Invariante M10 — Berichtssinn:** O26 §§2.1–2.2 fordert identifizierte Systembedarfe/opportunities, **keine** genehmigten Projekte. Postprocessing (inkl. Kleinmengenfilter), Offshore-Routen/Kosten, Infrastructure-Gaps-/ONDP-Abgrenzung und Ergebnisvergleich brauchen festgelegte Berichtssemantik. **MD-04/-05/-17-TBD**; es gibt **keine erfundene KPI-Formel**.

Die genauen mathematischen Pflichten, möglichen Formulierungsklassen, testbaren Gegenbeispiele und Grenzen dokumentiert **mathematical_obligations.md**.

## 6. Freiheiten, Äquivalenz und Beobachtbarkeit

Wissenschaftlich äquivalent sind Formulierungen, wenn sie bei **identischen versionierten Eingaben**, denselben berücksichtigten Kosten-/Einheiten-/Stundenkonventionen und denselben zulässigen Nebenbedingungen **dieselbe zulässige Menge der nach außen beobachteten Entscheidungsgrößen** und denselben optimalen Zielfunktionswert erzeugen (unter festzulegender numerischer Akzeptanz). Äquivalente Beispiele *unter Voraussetzungen*: Winkel- versus Zyklusflussdarstellung des DC-Netzes; kompakte extensive Form vs. analytisch identische zweistufige Zerlegung; storage energy variable vs. normierte State-of-Charge mit korrekt eingebundener Energiegröße.

**Nicht äquivalent:** Zwei unabhängige Wetterfallinvestitionen; nur NTC-Fernübertragung statt physikalisch vermaschter Bestandsleitungen; Kandidaten als AC-Leitungen statt steuerbare Marktlinks; verknüpfte Endogeninvestitionen 2035→2040→2050; willkürliches Sum-Worst-Case oder festgewählte fehlende Daten. Verschiedene optimale Portfolios können aufgrund degenerierter LPs denselben Zielfunktionswert haben. **Kandidaten-ID-Gleichheit ist deshalb ohne Auswahl-/Tie-Break-Regel kein notwendiges Äquivalenzkriterium** (MD-17).

Die interne Softwarewahl (LP-Bibliothek, Variablennamensgebung, Datenhaltung, Genauigkeitsstrategie, Parallelisierung, Netzwerkcontainer) ist **frei**, soweit Identitäten, Belege und Semantik erhalten bleiben. Keine neue allgemeine Robustheitsanforderung. Siehe **methodological_degrees_of_freedom.md**.

## 7. Wissenschaftliche Prüfbarkeit nach D5-A1

| Risikoklasse | Obligationen | Vorgesehener wissenschaftlicher Nachweis | Verfügbarkeit |
|---|---|---|---|
| Kritisch: Ergebnissemantik | gemeinsame Investitionen, erwarteter Zielfunktionswert, Stage-Übergang, DC-Marktlink vs physikalischer LF | symbolischer Aufbau, kleine analytische LPs, Constraint-/Dualwitness und Gegenbeispiele | **DESIGNED_ONLY**; MD-02/-07/-09/-15 |
| Kritisch: Netz | P05/P06 Topologie, Äquivalenzfluss, N-1-/LODF-Ableitung | detailliertes Referenznetz, korrespondierender reduzierte Testfall, Fehlervergleich | **BLOCKED_ORACLE**; MD-03/-13/-15 |
| Hoch: Sektoren | H2-Kopplung/Freeze, Speicher/Hydro/DSR, Zeitschritte | dimensionsgeprüfte Einzelfälle, Energierestfehler, Freeze-Identität | **DESIGNED_ONLY**; MD-06/-10/-12/-16 |
| Hoch: Output | Kosten, Offshore, Bedürfnisse und Baseline-/Portfoliovergleich | Kostenkomponentenreproduktion, Portfolio-Linien, KPI-Referenzdaten | **BLOCKED_ORACLE**; MD-02/-04/-05/-17 |
| Governance | Quelle, 48 SR, P00–P17, Datenmanifest, unabhängige Review | statische Traceprüfung + eigenständige fachliche und später personelle Auditentscheidung | **STRUCTURAL_ONLY**; G1 BLOCKED |

Ein „wissenschaftlich formuliert“ bedeutet **nicht** „mathematisch mit echtem Modell getestet“. Es wurden keine echten Optimierungs-, N-1- oder IoSN-Datenrechnungen ausgeführt und keine numerischen Toleranzen genehmigt. Das Review-Dokument trennt dabei die vom selben Erstellungsprozess vorgenommene adversarielle Gegenprüfung von einer tatsächlich unabhängigen Freigabe.

## 8. Nachweisführung und spätere Contract-Gestaltung

- **Prozess:** process_semantics_P00_P17.md enthält alle neun geforderten Analysefelder je P00–P17, je Schritt exakte ursprüngliche Prozessquelle und MA01-SR-Zuordnung.
- **Mathematische Verpflichtungen:** mathematical_obligations.md dokumentiert Formeln, Klassen, Einheiten, strukturelle Invarianten, Gegenproben und offene Orakel.
- **Freiheiten:** methodological_degrees_of_freedom.md.
- **Lücken:** unresolved_methodology_parameters.md enthält alle MD-01–MD-20, MA02-CL-001 und weitere Forschungs-TBD ohne Owner-Entscheidungsfiktion.
- **Zeilenregister:** source_and_assumption_traceability.csv verbindet Quellen, Entscheidungen, alle 18 P und **alle 48 MA01-SR** mit wissenschaftlichen Ableitungen.
- **Review/Handoff:** scientific_review.md und handoff_to_contract_design.md.

**Abschlussstatus:** Wissenschaftliches Referenzprofil **nichtnormativ; Forschungsformalisation möglich**. Kein normativer Go/No-Go-Entscheid, keine Datenfreigabe, keine aktive MA-01-Änderung, keine implementierte Wetterjahrselektion und keine Solver-/Sprach-/Architekturentscheidung. **G1 = BLOCKED**.
