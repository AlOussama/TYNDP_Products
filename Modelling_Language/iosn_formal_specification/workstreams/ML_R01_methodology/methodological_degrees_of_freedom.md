# ML-R01 — Methodologische Freiheitsgrade und Formulierungsäquivalenz

**Stand:** 2026-11-11 · **RESEARCH ONLY**, O26 Consultation Draft 25.02.2026; Entscheidungen D1–D6 nur als Projekt-Forschungsprofil; keine Tool-/Sprach-/Solverbindung. **G1 BLOCKED**.

## 1. Freiheit ist nicht Unterbestimmtheit

Eine Implementierung ist gegenüber der Methodik **frei**, wenn die vom wissenschaftlichen Profil geforderte Eingabe-/Ausgabe- und Restriktionssemantik erhalten bleibt. Eine unbelegte Annahme, die Menge zulässiger Investitionen/Dispatches, deren Zielkosten oder berichtete Needs verändert, ist **keine nachgewiesene Implementierungsfreiheit**. Unterscheide:

- **I – Invariante:** aus O26-Entwurfsinhalt oder D1–D6 definiert; ihre Missachtung wäre ein Verstoß gegen das jeweilige *Forschungsprofil*, nicht bereits automatisch gegen eine freigegebene offizielle 2026-Methodik.
- **E – Wissenschaftlich äquivalente Formulierung:** beobachtbar gleiche zulässige Menge und Zielfunktionswerte bei identischen Eingaben; Voraussetzungen, Abbildung und numerischer Vergleich nachzuweisen.
- **F – Toolinterne Freiheit:** Speicher-, Ausführungs-, Datenstruktur-, Model-Builder-, Constraint-Generation-, Dekompositions- oder Solverentscheidung ohne methodische Verhaltensänderung.
- **T – Nicht geklärte fachliche Option:** verändert methodisch relevante Semantik, bis Owner, Quelle oder Referenzfall sie legitimiert; **TBD**, nicht Default.
- **X – Ausgeschlossen:** widerspricht O26-/D-Profil oder führt neue Anforderungen/Verfahren ein.
- **Z – Illustrativ:** hilfreich als mathematischer Repräsentant, aber nicht aus dem Methodenstand eindeutig vorgeschrieben.

## 2. Freiheitsgradmatrix (wissenschaftliche Systematik)

| Objekt / Prozess | Invariante I | E/F: zulässige Spielräume **unter Gleichwertigkeitsnachweis** | Fachlich offen T (nicht frei) | Unzulässige Annahme X / Beispiel Z | Beleg |
|---|---|---|---|---|---|
| Quellenprofil P00 | Methodikstatus erkennbar: O26 **Draft**, Adoption nicht bestätigt | Manifestformat, Archiv- und Provenienzlösung (F) | Version/Wirksamkeit MD-01 | Draft als „freigegeben“ kennzeichnen (X) | O26 Cover, D1/D3 |
| Zieljahre P01 | 2035, 2040, 2050 **getrennt** rechnen | Unabhängige Parallelisierung und Ergebnisablage (F) | Studienversion und Szenariozuordnung MD-11 | Endogene 2035→2040→2050 Portfoliovererbung (X) | §3.2, §3.10 |
| Wetteraufnahme P02 | D2: CY1–CY5, gleiche symbolische \(\pi_c\) je Zieljahr, nichtnegativ/normiert | beliebige Eingabeform und Schlüsselcodierung mit reversibler Zuordnung (F) | tatsächliche Gewichte, Freeze, Zeitreferenzen MD-12/-18/-19 | O26s 3 Wetterfälle als D2-Profil ersetzen (X); Wetterselektion rechnen (X) | O26 §3.7 **vs D2** |
| Zeitachsen P03 | UTC-Intervallidentität, Dimensionen/Provenienz D4 | verlustlose UTC-Timeseries-/Datenbankkodierung, äquivalentes Voraggregieren nach Freigabe (F/E) | Leap/DST, Fehlstellen, Zeitgewichte und Toleranzen MD-12 | fehlende Stunde ohne Beleg auffüllen, implizit mit 8760 multiplizieren (X) | D4, §§3.7/4.2 |
| Startnetz P04 | qualifizierter 2035-Grenznetzstand, fixe Offshore-Ziele | graphische/netzinterne Darstellung (F) | Eligibility/CBA4-Maturity MD-14/MA02-CL-001 | ungeprüfte Projektkategorie als qualifiziert (X) | §§3.4–3.5, Anh.6.2 |
| Cluster P05 | dokumentierte kritische Leitungen, **zusammenhängende** vollständige Zone-/Knotenpartition, O26-Studienprofil 102 Zonen | Graphpartitionierung/Suche/Knoten-ID-Technik (F), soweit akzeptierte Partition/Qualität resultiert | Gewichtung Engpass/Austausch, Ausnahmefälle und numerische Zielgrenzen MD-03/-13 | beliebige 102-Zonen-Partition ohne Qualitätsbeleg (X) | §3.8.1; Anh.6.1 |
| Netzäquivalent P06 | sechs Outputklassen, DC-Mesh, Zonen-/PST-/HVDC-Einflüsse, N-1-Kapazitäten | alternative numerische Äquivalenzoptimierung nur nach gleicher Physik/Oracle (E/F) | Referenznetz, RMSE-/LODF-/N-1-Toleranzen MD-03/-15 | beliebige Leitungsratings addieren (X) | §3.8.2–3.8.3; Anh.6.1 |
| Datenallokation P07 | Source→Zone-Mapping und Kapazitäts-/Energieerhaltung relevanter additiver Größen | ETL, Vektorisierung, Batch/Stream (F) | Konflikte PECD vs Netz, Resampling MD-11/-12 | Kapazitätsfaktoren wie Leistungen summieren (X) | §3.8.4 |
| Strombilanz P08 | elektrische Knotenleistung in MW, Lastabwurf und Lade-/Wandlungsnetto in konsistenter Bilanz | unterschiedliche Inzidenz-/Vorzeichenwahl bei reversibler Gleichheit (E/F) | Policy-Details, Abregelung/Reserve MD-10/-16 | Energie und Leistung in derselben Gleichung addieren (X) | §3.1.1 |
| Vermaschte elektrische Bestandsleitung P06/P08 | Kirchhoff/DC-Flow mit methodischer Äquivalenzimpedanz und Nullfluss-/PST-Korrektur | Winkelansatz, PTDF oder Zyklusformulierungen mit gleicher Projektion (E) | Kalibrierung, Slack-/Referenzfallkonvention MD-03/-15 | No-load-/PST-Effekt weglassen (X), wenn physisch relevant | §§3.1.1,3.8 |
| Ausbaukandidaten P09 | **steuerbare DC-Marktlinks**, selbst bei physisch AC-Projekt | gerichtete signed-Variable vs. positive/negative Variablen mit exakt gleicher Link-/Kostenregel (E) | direkte/indirekte NTC-Wirkung, Kostenträger/RDFID MD-09 | Kandidaten unbemerkt zu Kirchhoff-AC-Zweigen machen (X) | §4.5.2 |
| Kandidatenbounds P09–P11 | \(0\le x\le\overline x\), lineare LP-Kandidaten | Presolve, aktive-Set-Variableneinführung, statische Bounds (E/F) | individuelle Obergrenzen, Restcapacity MD-07/-11 | unbegrenzter Ausbau ohne Quelle (X) | §3.1.1 |
| Kosten und Zielfunktion P09–P12 | Investition **einmal** + \(\sum_c\pi_c Q_c\), VoLL/ENS in konsistenter Energieeinheit | analytische lineare äquivalente Terms, extensive Form/Zerlegung (E) | Preisjahr/Annuität/Discount, Blockjahre MD-02 | minimax/CVaR als Ersatz (X); konkrete Barwertformel ohne Owner (Z) | §§3.1.1/4.6, D2 |
| Investitionsnichtantizipativität P10–P12 | genau ein Investitionsvektor je Jahr über Wetterfälle | Replikation mit Gleichheitslinks (E), ein geteilter Vektor (E) | Verknüpfung der Stage-Zustände MD-07 | pro Fall separate investments \(x_c\) (X) | §3.1.1 |
| Stufe 1 P10 | reales On-/Offshore-Kandidaten-LP, LF-Physik ohne bindende interne Interzonencaps | LP-Numerik/Runengine (F) | Kandidaten- und LF-Abgrenzung MD-07/-08 | konzeptionelle Kandidaten in Stage1 (X) | §§3.9–3.10 |
| Stufe 2 P11 | verbliebene reale, konzeptionelle Onshore und theoretische Offshore-Kandidaten, Stage1 angerechnet | Solver-/Betriebsdarstellung (F); wissenschaftlich gleichwertige Übergabe bei Beweis (E) | Teilinvestitionen, Fixierung/Reoptimierung MD-07 | Stage1 ganz ignorieren oder CAPEX doppelt (X) | §3.10 |
| Stufe 3 P12 | endogene Speicherexpansion nur 2040/2050; 2035 exogen | Batterieproxy-Variablenrepräsentation, wenn Klassen und Kosten erhalten bleiben (E/F) | Speicherdauern, Ländertrajektorien, CAPEX, End-SOC MD-06 | beliebiges 2035 storage build (X) | §3.10/4.5.1 |
| Stromspeicher P08/P12 | Lade-/Entlade- und Energiezustand mit intertemporaler Bilanz | direkte Energievariable vs korrekt normierter SoC (E) | Verluste, Initial-/Endzustand, Zyklusannahmen MD-06 | SoC ohne Zeitfortschreibung, nicht gedeckte negative Energie (X) | §4.5.1, wissenschaftliche Erhaltung |
| Hydro P08 | fünf Hydroklassen mit Ressourcen-/Zuflussdifferenzierung | spezialisierte Erzeuger/Reservoir-Komponenten (F/E) | Inflow, Pumpverluste, Energiegrenzen, Endzustände MD-16 | jedes Hydroasset als identisches unbeschränktes Thermal-Asset (X) | §4.3 |
| DSR P03/P08 | explizite Markt-DSR und implizite außerhalb Markt getrennt | unterschiedliche Zustandsformulierungen bei gleicher Lastsemantik (E) | Curtail-/Shiftfenster, Rebound, EV-/HP-Zugehörigkeit MD-16 | doppelte Anrechnung impliziter verschobener Last (X) | §4.4 |
| Strom-/H2-Kopplung P08 | getrennte Zonen-/Carrierbilanzen, P2G und Rückstrom, H2-Netzausbau exogen | Port-/Netz-/Transferdarstellungen mit dimensionsgleicher Wirkung (E/F) | exogene H2-Kapazitäten, Wirkungsgrade, Betriebsregeln MD-10 | neue H2-Pipelineinvestmentvariable im Strom-LP (X) | §§3.3/3.6 |
| Frozen H2 P14 | präexpansives stündliches elektrolytisches Betriebslastprofil einfrieren, separate Sensitivität | Fixvariablen vs exogenes Profil, numerisch identische Stundengleichheit (E) | Umfang weiterer eingefrorener H2-Größen MD-10 | nur Jahresenergie fix, Stundenprofil frei (X) | §3.6 |
| LF/Dispatch P10–P13 | LF-Expansion und gesonderter *restriktiver* Dispatchvergleich unterscheiden | verschiedene OPF/ED-Löser bei gleichen Bedingungen (F/E) | interne Netzlimits und KPI-/Delta-Konvention MD-08/-17 | LF-Porfolio mit OPF-Zusatzstudie gleichsetzen (X) | §3.9 |
| Optionale OPF P15 | separat, nicht Pflicht; Ausbau durch LF-Portfoliokapazitäten limitiert | äquivalente gesonderte OPF-Formulierungen (E) | Mapping des Caps und Portfolio-Identität MD-08 | neue OPF-Kandidaten jenseits LF-Deckel (X) | §3.9 |
| Offshore P04/P09/P16 | fixe Länderziele und source-spezifischer theoretischer Übertragungs-/Routenansatz | GIS/Geometrie-/Kostenrechner frei bei gleichem Eingabe-/Formelbezug (F/E) | exakter Umwegfaktor 10–15%, Routengeometrie/Kosten MD-05/-14 | \(12.5\%\) als verbindlich ausgeben (X/Z) | §§3.5,3.11,4.5.3 |
| Needs/Outputs P16 | Systembedarf, **kein** genehmigtes Projekt, Quelle/Zieljahr/Run identifizierbar | Berichtsdarstellung und Datencontainer (F) | KPIs, Aggregation, Kleinmengenschwellen MD-04/-17 | vage Prosa als numerisch verifiziertes KPI ausgeben (X) | §§2.1–2.2,3.10 |
| Review/Acceptance P17 | D3 fail-closed; D5-A1 risk-based; D6-A unabhängige Implementierungen | Testimplementierung, Evidenzcontainer, Vergleicher (F) | Schwellen, Referenzorakel, unabhängiger Personensignoff MD-15/-17/-20 | Strukturtests als Modellfreigabe oder KI-Selbstreview als Unabhängigkeit (X) | D3/D5/D6, §5.1 |

## 3. Strengere Äquivalenzprüfung als Vergleich von Gleichungstexten

Für zwei Modellimplementierungen \(M_A,M_B\) und **identisches freigegebenes Eingabeprofil** \(d\) mit offenen Parametern erst nach deren Freigabe gilt:

\[
\mathrm{Proj}_{\mathcal O}\bigl(\mathrm{Feasible}(M_A,d)\bigr)
=
\mathrm{Proj}_{\mathcal O}\bigl(\mathrm{Feasible}(M_B,d)\bigr),\qquad
\mathrm{OptCost}(M_A,d)=\mathrm{OptCost}(M_B,d).
\]

Hier ist \(\mathcal O\) die **methodisch beobachtbare** Menge von Kostenkomponenten, physikalischen und Marktlinkflüssen, Investitions-/Stufenstatus, Dispatch- und Need-Größen. **\(\mathcal O\) ist noch teilweise TBD** (MD-04/-17). Diese Mengenbedingung ist ein **wissenschaftliches Prüfkriterium, nicht eine bereits autorisierte Akzeptanzregel**. Praktische numerische Gleichheit braucht freigegebene Toleranzen (MD-15).

Eine reine Gleichheit von Zielfunktionswerten garantiert weder identische Feasible Sets noch physikalisch zulässige Flüsse. Umgekehrt kann bei degenerierten LPs **mehr als ein optimales Portfolio** existieren. Gleiches Kostenminimum mit unterschiedlichen Kandidaten-IDs kann daher äquivalent sein, solange die methodisch beobachteten Größen kompatibel bleiben; die tatsächliche Entscheidungs-/Tie-Break-Regel bleibt MD-17 offen.

### Gegenbeispiele zur Freiheit

1. **Nichtantizipativität:** \(\min\sum_c \pi_c Q_c(x_c)\) mit je Wetterfall frei gewähltem \(x_c\) ist ein relaxiertes, anderes Investitionsproblem und hat im Allgemeinen ein zu optimistisches Ergebnis.
2. **DC-Begriffsverwechslung:** Eine physisch AC-geplante Ausbaumaßnahme als neue Kirchhoff-Branch statt als steuerbarer Marktlink kann Flüsse und Schattenpreise verändern, selbst wenn die nominelle MW-Kapazität identisch ist.
3. **Stage-Merging:** Das gemeinsame Lösen aller Kandidaten in einem einzigen LP kann andere reale-vor-konzeptionelle Ausbauentscheidungen liefern als eine zweistufige Sequenz.
4. **NTC-Mapping:** Gleiche neu gebaute MW bedeuten nicht zwingend gleiche *direkte/indirekte* richtungsbezogene Transferfähigkeit und daher nicht gleiche Wirkung.
5. **Physikalische Reduktion:** Gleiche Zahl 102 Zonen garantiert keine elektrische Äquivalenz und keinen N-1-Sicherheitsnachweis.
6. **Kalender:** Zwei Datenreihen mit nominell 8760 Zeilen können 8760 unterschiedliche/verschobene UTC-Stunden repräsentieren.
7. **Kosten:** \(\sum_c \pi_c C^{inv}\) ist nur *algebraisch* gleich \(C^{inv}\), wenn \(\sum_c\pi_c=1\) und jede Investition einheitlich bilanziert wird; **Kosten fünfmal separat** addieren ist dagegen falsch. Diskont-/Währungsmischung ändert das Optimum.
8. **Storage:** Zwei Modelle mit gleichem MW-Kandidat aber unterschiedlicher Dauer/MWh-Kapazität sind im Allgemeinen nicht operational äquivalent.

## 4. Formulierungsklassen mit Voraussetzungen

| Klasse | Mathematische Transformation | Nachweisverpflichtung | Quellenabgrenzung |
|---|---|---|---|
| Winkel-DC ↔ PTDF/Zyklus-DC | eliminiere Potenzialvariablen bei gleichen Inzidenz-/Referenzfällen | gleicher Netzinjektionsraum und Zweigflüsse, inkl. äquivalenter No-load-/PST-Effekte | O26 physikalische Netzpflicht, formaler Beweis [S] |
| Extensivform ↔ Dekomposition | gemeinsame Investition mit Szenario-Recourse, ggf. Benders | keine gelockerten Nichtantizipativitäts-/Schnittbedingungen, gleiches Optimum | O26 §3.1.1, D2, [S/E] |
| Ein Link ↔ positive/negative Links | \(m=m^+-m^-\) | Richtungsgrenzen, Kosten, keine zusätzliche Simultanfluss-Arbitrage | O26 §4.5.2, NTC-Mapping TBD |
| \(e_t\) ↔ \(SOC_t\) | \(SOC=e/E\) | gleiche Zustands- und Endbedingungen, Vorsicht bei endogenem \(E\) | O26 Speicherklasse, [S/E] |
| Vorverarbeitung ↔ Integration | qualifiziertes Netzäquivalent aus P06 als Input statt Berechnung im selben Programm | vollständige sechs Outputklassen plus referenzierte Detailed-Grid-Evidenz | O26 §3.8; keine Architekturentscheidung |

## 5. Grenze der D5-A1-Verifikation

Die Forschungsprüfung darf (i) Text-/Strukturkonformität, (ii) symbolische Gleichungs-/Einheitentestfälle, (iii) kleine unabhängige Orakelentwürfe und (iv) dokumentierte Fehlerszenarien vorab erarbeiten. **Sie darf nicht** durch solche Prüfungen fehlende Detailnetze, Wetterprofile, Freigaben, solverbasierte Laufresultate oder numerische Akzeptanzentscheidungen ersetzen. Für unbekannte Parameter/Freigabedaten: **TBD / BLOCKED_ORACLE**, nicht fiktiv numerisch komplett.

Die Übergabe an die spätere Requirements-Sprache soll Invariante, Annahme, Äquivalenzvoraussetzung, Ownerparameter und Verifikationsnachweis **separat** behandeln. Sie darf weder konkrete YAML-Schemas noch GEMS, PyPSA-Eur, Sienna, Antares oder einen Solver normativ festlegen.

**Querverweise:** mathematical_obligations.md M01–M18; process_semantics_P00_P17.md; source_and_assumption_traceability.csv; unresolved_methodology_parameters.md. **Status: G1 BLOCKED.**
