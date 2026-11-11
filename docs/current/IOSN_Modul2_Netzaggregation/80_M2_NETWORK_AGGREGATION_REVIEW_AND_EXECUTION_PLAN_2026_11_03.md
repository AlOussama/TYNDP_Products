# IoSN Modul 2 – Netzaggregation und Netzreduktion: unabhängiger Code-Review und Ausführungsleitfaden

**Dokument-ID:** M2-R0-REVIEW-20261103  
**Datum:** 03.11.2026  
**Repository:** AlOussama/TYNDP_Products  
**Geprüfter Code:** main @ 1595d6d38e77804760612621657721b3699d2fea (19.10.2026)  
**Übernommene methodische Vorarbeit:** docs/iosn-official-network-reduction-code-audit-2026-10-26 @ 3dc719a35f57bd9516bef8486bf262b75509d6b1 (26.10.2026)  
**Status:** statischer Review und Ausführungsplanung; keine neue Laufzeit-/Realnetzausführung; keine ENTSO-E-Konformitätsfreigabe.

## 0. Entscheidung und strikte Modulgrenze

Die kanonische Implementierung unter src/tyndp_reduce ist ein funktionsfähiger, mathematisch getesteter **wissenschaftlicher Demonstrator**; sie ist noch **keine vollständig geschlossene, mit einem europaweiten Netz validierte IoSN-2026-Netzreduktionspipeline**.

Dieses **Modul 2** ist eigenständig:
- **Input:** versioniertes, bereits aufgebautes physikalisches Referenznetz; externe stündliche nodale Nettopositionen/Dispatch-Zustände; Länder-/Gebietszuordnung; physische Limits/Kontingenzen; extern festgelegte Wetterjahre.
- **Output:** Busmap, Zonen, physikalische Ersatzlinks mit Ersatzreaktanzen, strukturellen Flusskorrekturen/affiner Maschenformulierung, vier saisonalen/richtungsbezogenen N-1-Kapazitäten, Steuergerätewirkungen sowie Validierungsprotokoll.
- **Nicht Bestandteil:** CGMES-Import/-Export (Modul 0), PECD-Quellenreader und Asset-Profilmapping (Modul 1), Auswahl/Clustering der Wetterjahre, Marktinvestitionsoptimierung, FBMC-Forschungsverfahren. Netz- und Zeitreihendaten sind Schnittstelleneingänge, keine Entwicklungsabhängigkeit zu M0/M1.
- **Fünf bestehende Wetterjahre** werden unverändert als externer Projektdatensatz behandelt. ENTSO-E beschreibt in der Konsultationsfassung drei repräsentative Wetterfälle für ihre gesonderte Optimierung. Das hier verwendete Fünf-Jahre-Protokoll darf deshalb nicht als offizielle IoSN-Szenarioanzahl etikettiert werden.

## 1. Verbindliche Evidenz und Versionshierarchie

### Primärquellen
1. ENTSO-E: *TYNDP 2026 Identification of System Needs Methodology*, Version for Public Consultation, **25.02.2026**: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf  
   Relevanz: §3.8 S.21–29; §3.9 S.29; Annex 6.1 S.45–51; Tabelle 3 S.26–27; Abbildung 4 S.23; Abbildung 13 S.46. Die PDF ist eine **Konsultationsfassung**, kein nachgewiesener endgültiger Algorithmus.
2. Bereits durchgeführter 18-Punkte-Methodik-Audit: [IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md).
3. Originalgetreue Budgetabschrift: [IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv](../IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv): **37 Einträge, Summe 102**. „Northern Ireland“ und „United Kingdom“ sind separat bezeichnet; keine stillschweigende Zusammenlegung.
4. Wissenschaftlicher Bestandsbericht: [Band I](../IOSN_2026_Band_I_Wissenschaftliche_Methodik.md); [Band II](../IOSN_2026_Band_II_PyPSA_Implementierung.md).
5. GitHub-CI: https://github.com/AlOussama/TYNDP_Products/actions/runs/39284613687 – erfolgreich am 19.10.2026 für den genannten main-Commit.

### Evidenzkategorien
- **D:** explizit in der ENTSO-E-Veröffentlichung beschrieben;
- **T:** aus D abgeleitete, zwingende physikalische/technische Formalisierung;
- **I:** eigene, offen deklarierte Festlegung, weil Veröffentlichungen keinen vollständigen Algorithmus liefern;
- **B:** Daten-/Integrationsblocker;
- **X:** Forschungsalternative, ausdrücklich nicht IoSN-Baseline.
Jeder Implementierungsentscheidung, Konfigurationsvorgabe, numerischen Schwelle und jedem Gate ist eine Kategorie zuzuordnen. Bei späterer verbindlicher offizieller Methodik zuerst Versionsvergleich durchführen.

## 2. Tatsächlicher Repo- und Teststand (statischer Audit)

Verifiziert: src/tyndp_reduce mit 13 Python-Modulen; tests mit fünf Dateien; Demo und synthetische CSV/JSON. Die historische main-CI-Ausführung ist erfolgreich. Die 24 Tests wurden **hier nicht erneut ausgeführt**; ihre Pass-Aussage stammt aus der vorliegenden Vorarbeit/CI. Die synthetische Referenz in results/synthetic/manifest.json ist ein erfundenes **9-Bus-, 120-Snapshot-DC-Netz**, ausdrücklich ohne PyPSA-Ausführung.

| Status | Datei/Funktion | Existierende Evidenz | Konkrete Lücke / Risiko |
|---|---|---|---|
| PARTIAL | dc.py / DetailedDC | DC-Inzidenz, PTDF, exakte Bilanz, Erkennung eines nicht-zusammenhängenden Graphen | dichte Rangtests, explizite Inversion, ein AC-Island, keine PST-/HVDC-/Trafo-Wirkungen; nicht auf europäische Knotenzahlen skalierbar |
| PARTIAL | screening.py / method_a | jährliche Überlastungsenergie aus Flüssen und statischen Grenzwerten | kein 225-/400-kV-Filter; kein explizites Jahr-/Szenarioledger; keine saisonalen Grenzen oder Limit-Einheitenbehandlung |
| PARTIAL | clustering.py / greedy_busmap | deterministische verbundene Kantenkontraktion, optionales regions und locked_edges | Länderrestriktion optional, nur globale Zonenanzahl; 37 Einzelquoten/102 Zonen, geloggte Multi-Country-Nachbarschaft und Iteration fehlen |
| PASS_SYNTHETIC | aggregation.py | P, Gamma, A_z und A_z Gamma = P A_d | Identität sagt nichts über elektrische Ersatzimpedanzen, PST/HVDC oder Sicherheitskapazitäten; Quotenlandkarte fehlt |
| PARTIAL | equivalent.py / fit_equivalent | positive x; konstantes divergence-freies c0; nichtlineare kleinste Quadrate | reine Ein-Island-Inversion, erste x-Referenz fixiert, keine vollständige robuste Identifizierbarkeit; c0 nicht als affine Loop-Gleichung in einem realen Zielsolver bewiesen |
| PROXY | security.py | LODF und N-1-Stress; lineare Kapazitätsregression | invalid/islanding wird in worst-loading-Schleife übersprungen, Sonderfälle 99,5 % / 1 % / 130 % unvollständig, empirische Standardparameter sind **nicht offiziell** |
| REJECTING_ADAPTER | pypsa_adapter.py | einfacher Leitung-only-Import; Blocker statt stilles Verwerfen | transformer, link, storage_unit, store, phase shift nicht zugelassen; AC-Mehrinseln und operativer HVDC/PST-Kontext offen |
| OUT_OF_BASELINE | security_projection.py, fbmc_bridge.py, method_b | unabhängige Sicherheits-/Marktforschungsmodelle | nicht als Ersatz für IoSN-Annex-6.1-Kapazität oder offizielle Clustering-Regel benutzen |
| DEMO_ONLY | demo.py, examples/pypsa_real_network.py | synthetische Vergleichsrechnungen, einfacher Realnetz-Preflight | Demo hat keine exakte Länderzahl, keine globale Re-Clustering-Schleife; Realnetzbeispiel schreibt ausdrücklich unqualifiziertes Netz ohne x/c0/N-1 |

### Neu hervorgehobene P0-Auditfunde
- **M2-P0-01: 102/37-Quoten nicht erzwungen.** Ein Parameter n_zones und optionale regions sind kein Ersatz für zwingende Quoten pro Land/Gebiet, Country-ID-Abbildung und Connectedness.
- **M2-P0-02: fehlende geschlossene europaweite Feedbackschleife.** Nach jeder Änderung der Busmap müssen die europaweiten Ersatzreaktanzen und der Offset neu geschätzt, der Zielfluss neu aggregiert und auf denselben Referenzstunden bewertet werden.
- **M2-P0-03: Realnetz-Physik nicht qualifiziert.** Das DC-Demo unterstützt ein einziges passives AC-Netz und dichte Matrizen; HVDC, Transformatoren, PSTs, getrennte synchrone Gebiete und zeitabhängige Zustände sind Daten- und Solververträge.
- **M2-P0-04: N-1-Qualifikation fehlt.** Die 4-Wege-Kapazitätsschätzung und veröffentlichten Sonderfälle sind nicht vollständig; Ausfälle mit undefinierten LODF dürfen nicht ohne transparenten TSO-Nachweis ignoriert werden.
- **M2-P0-05: struktureller Flow-Offset in physischer Maschenbedingung.** Ein bilanzneutraler c0 als Postprocessing ist nur dann einsatzfähig, wenn die affine KVL-Formulierung des tatsächlich verwendeten reduzierten Simulators implementiert und unabhängig geprüft ist.
- **M2-P0-06: kein reales synchrones Referenzdatenset.** Keine End-to-End-Qualifikation ohne reproduzierbare Netztopologie, Limits, dispatch/injections und Kontingenzen.

### Nachweisgrenzen
Keine neue CI-Ausführung, kein realer PyPSA-Lauf und keine numerisch gemessene europäische RMSE in diesem Review. Die Farbbänder in Abb. 13 (200/350/500 MW bzw. 10/20/30 %) sind **indikative Diagnoseklassen, kein vollständiger normativer PASS-Grenzwert**. Methodik-Konformität und empirische Qualität müssen getrennt beurteilt werden.

## 3. Daten-, Modell- und Schnittstellenvertrag

Verbindliche externe Inputobjekte; jedes besitzt Quellpfad, Version/Commit, Hash, Einheiten, Netzvariante, Zieljahr, Wetterjahr, Zeitstempelindex und Validierungsstatus.

1. **DetailedGridSnapshot**: Bus-IDs, Land/Gebiet laut Tabelle 3, Spannungsebene, geographische und elektrische Topologie, orientierte AC-Zweige, alle Transformatoräquivalente, PST, HVDC-Terminals und controllable devices, AC-Inseln, x, branch ratings, seasonal/emergency ratings, Einheitentransformation.
2. **ReferenceDispatchSet**: vollständige und je AC-Island ausgeglichene nodale Wirkleistungsinjektionen und Detailflüsse pro synchronem Zeitpunkt. Market/NTC-Dispatch und tatsächliche Terminalsignale unterscheiden. Der physikalische Referenzlauf ist europaweit gemeinsam zu berechnen; niemals mit separat pro Land balancierten PTDFs ersetzen.
3. **TimeSet**: fünf bereits festgelegte externe Wetterjahres-IDs, Stunden-/Dauergewicht, Sommer/Winter-Konvention, feste Trainings-, Auswahl- und Holdout-Splits (ohne Neuauswahl der Jahre). Keine Umdeutung als offizielle drei ENTSO-E-Szenarien.
4. **CountryZoneBudget**: Tabelle-3-Einträge und pro Label k_c; Summe 102 bei vollständig abgedeckter offizieller Geographie. Unbekannte oder nicht abgedeckte Landestopologie als BLOCKED_DATA; bei kleinen Fixtures separate ausdrücklich **nicht offizielle** Testquoten.
5. **SecurityData**: Kontingenzliste, Monitore, N-0/N-1-Limits, saisonale/Notfallgrenzen, TSO-begründete Ausnahme, Inselbildungsledger.
6. **OptionalAssetAllocation**: standortbezogene oder zonal zuordenbare Anlagen und Lasten für §3.8.4; Modul 2 konsumiert fertige Assets/Verteilungsschlüssel. Kein PECD-Reading, kein CGMES-Parsen.

Ausgabe **ReducedGridProduct**: eindeutig versionierte busmap und Schnittoperatoren; per-country quotas; interzonale orientierte Ersatzlinks; x_eq; strukturelle c0 und affine Mesh-Constraints; vollständige flussbezogene Vergleichsmetrik; vier N-1-Kapazitäten je Link samt Qualitätsstatus; No-Load-, HVDC- und PST-Wirkungen; zonale Asset-Zuordnung und Masse-/Energieerhaltung; Maschinenlesbares Provenance-/Evaluation-/Decision-Ledger.

### Absolute Invarianten
- Genau eine Zone je Knoten; innerhalb jeder Zone exakt ein Länder-/Gebietslabel; jede Zone AC-topologisch zusammenhängend.
- Für vollständige Geographie: Summe k_c=102 **und** Anzahl Zonen pro Country-Budget-Eintrag exakt k_c.
- Landesgrenzen werden nicht als Lastfluss-Schnittstelle modelliert. Physische grenzüberschreitende Zweige bleiben im europäischen Referenzsystem.
- Zonal algebraisch: p_z=P p_d, f_cut=Gamma f_d, A_z Gamma=P A_d, A_z f_cut=p_z.
- KCL pro AC-Island, für zulässigen Offset A_z c0=0. Affine KVL muss im reduzierten Zielmodell gelten; eine eigene technische Form ist C^T diag(x)(f-c0)=0, nicht ohne Nachweis die offiziell veröffentlichte homogene Gleichung für den Gesamtfluss.
- N-1-Werte sind vier echte, richtungs-/saisonspezifische qualitätsmarkierte Ergebnisse. Ein undefinierter Ausfall erzeugt FAIL/UNQUALIFIED, keine stille Freigabe.

## 4. IoSN-Baseline: algorithmischer Ablauf und verschachtelte Iterationen

### L0 – Eingangsdaten und Physik (BLOCKING PRE-FLIGHT)
Prüfe Vollständigkeit, Identitäten, Landestaxonomie, AC-Inseln, realen Betrieb, MW/MVA/A-Konvention, Dispatch-/Fluss-Konsistenz, zeitliche Synchronität, fünf Jahres-IDs und zulässige Kontingenzen. Erzeuge eine versionierte Referenzflusstabelle aus dem **gemeinsamen europäischen Modell**, bevor Clusterkandidaten optimiert werden. Bei fehlenden aktiven Betriebsmitteln keine künstliche Ersatzdatenfreigabe.

### L1 – Primärer Engpass- und Clusterstart (D + I-01)
- Berechne über alle repräsentierten Stunden getrennt je Jahr die Lastflussüberlastungen auf dokumentierten 225-/400-kV-Leitungen; S_(l,y)=sum_t delta_t max(0,abs(f_(l,t))-F_lim_(l,t)) [MWh].
- Speichere die fünf Jahresscores getrennt; eine gemeinsame Jahresgewichtung ist eigene Entscheidung, nicht unbemerkt verbindliche IoSN-Definition.
- Wähle eine deterministische feasible Start-Busmap mit verankerter Landesreinheit, exakt k_c Zonen je Country-Label, topologischer Verbindung und nach Möglichkeit Erhalt der kritischen Zweige als Interzonen-Grenzen.
- Beurteile gegenläufige Flüsse in zu einem Ersatzlink zusammengefassten Korridoren, schutzwürdige Engpässe, unvollständige 110-kV-Tie-Daten und dreifache Ländergrenzsituationen.
- Das Ziel ist **nicht** eine neue, frei erfundene gewichtete RES/elektrische-Distanz/Last-KMeans-Funktion. Eine solche Erweiterung kann separat als X-Benchmark laufen.

### L2 – Elektrische Parameterkalibrierung je Busmap (D + I-02)
Für Kandidat z: p_z(t)=P(z)p_d(t) und f_target,z(t)=Gamma(z)f_d(t). Auf demselben paneuropäischen reduzierten Graphen positive x und einen zeitlich konstanten strukturellen Offset c0 fitten, so dass KCL und affine KVL gelten.

Beispiel **eigener** offengelegter Fit (nicht der ENTSO-E-Originalalgorithmus):

  min_(x>0,c0) sum_(e,t in Ttrain) w_(e,t) [ (H_eq(x)p_z(t))_e + c0_e - f_target_(e,t) ]^2 + Regularisierung

  unter A_z c0=0 und dokumentierter Skaleneichung/Identifizierbarkeit je AC-Island.

Wichtig: Die offizielle Primärquelle neutralisiert während der beschriebenen Kalibrierung die PSTs und setzt HVDC-Setpoints innerhalb des AC-Netzes auf null; deren operationale Wirkung muss später als getrennter Output erscheinen. Fitstunden, Regularisierung, Solver, Startwerte und Fehlerbehandlung sind offengelegte I-Entscheidungen. Unidentifizierbare Maschen, sehr schlecht konditionierte Systeme und nicht konvergierte Solver sind explizite GATE_FAIL.

### L3 – Europaweite gekoppelte Re-Clustering-Iteration (D + I-03)
Pro Versuch:
1. Erzeuge gültige lokale Grenzknotenbewegungen oder ausgeglichene Swap-/mehrteilige Moves **innerhalb** der jeweiligen Landesgrenzen. Optional bündle Änderungen in **mehreren elektrisch gekoppelten Ländern gleichzeitig**; niemals Ländergrenzen verändern.
2. Verwerfe Kandidaten vor dem teuren Fit, wenn Quoten, Country-Purity, Connectedness, kritische Branch-Erhaltung oder AC-Inselkonsistenz verletzt werden.
3. Berechne neue P, Gamma und europäischen Ziel-Schnittfluss aus **denselben** eingefrorenen Detailstunden.
4. Starte L2 **vollständig neu** für den gesamten europäischen Ersatzgraphen und neutralen Kalibrierungskontext.
5. Vergleiche Fluss-RMSE je Ersatzlink und global auf fixen Auswahlstunden: RMSE_e = sqrt(mean_t((f_pred,e(t)-f_target,e(t))^2)). Speichere MW-Quantile, relative Fehler nur bei explizitem Nenner, Linkzahl, kritische Branch Capture, Anti-Korrelations-/Flussrichtungsdiagnosen und länderspezifische sowie Grenzqualitätsindikatoren.
6. **Achtung wechselnde Topologie:** Linklisten ändern sich. Ein einziges arithmetisches Mittel über jeweils andere Links ist nicht unmittelbar äquivalent. Benutze ergänzend feste Monitorgruppen, Kritikalitätsabdeckung, Linkzahl- und Länder-/Grenz-Fairness-Diagnosen. Tie-Breaker, Normalisierung und Nichtvergleichbarkeit offen kennzeichnen.
7. Akzeptiere einen Kandidaten nur, wenn die vorab festgelegte vergleichbare Fehler-/Qualitätsentscheidung ihn tatsächlich verbessert, und protokolliere alle verworfenen Moves, Solverresiduen und Gründe; sonst Rollback.
8. Nach dokumentiertem RMSE-Plateau starte L4, nicht unendlich weiteroptimieren. Suchbudget, stabile Seed-Führung, tolerierte Plateau-Änderung und Abbruchordnung sind **I**, keine erfundenen ENTSO-E-Pflichten.

Trenne strikt (a) Trainingsstunden für Ersatzimpedanzfit, (b) Auswahlstunden für Re-Clustering-Entscheidungen, (c) finale verschlossene Holdout-Stunden. Die fünf vorgegebenen Jahre werden nicht im Prozess ausgetauscht; Zeitfenster und Jahre dürfen über Block-Splits geprüft werden.

### L4 – Kapazitätsqualitäts- und Sicherheitsrückkopplung (D + I-04)
Erst nach Stabilisierung der Flussqualität:
- Verwende die Detailnetz-Grenzzweige und validierte LODF/physische N-1-Flüsse. Für jede Grenze die maximal N-1-belastete relevante physische Leitung pro Stunde ermitteln.
- Bilde vier getrennte Punktwolken je Ersatzlink: Sommer/Hin, Sommer/Rück, Winter/Hin, Winter/Rück. Vergleiche je Gruppe orientierte Summe physischer Schnittflüsse mit maximaler Auslastung. Kapazitätsdefinition: Austausch bei 100 % N-1-Auslastung.
- Verwende nur als **I-PROXY** bezeichnete generische Fits, sofern die ENTSO-E-Spezifikation die konkrete Regression nicht offenlegt. Dokumentiere sample count, Fitbereich, Korrelation, R², Unsicherheit und Inter-/Extrapolation.
- Offizielle Sonderfälle aus Anhang S.51: >99,5 % in nur einer Richtung -> Gegenseitenwert gleichsetzen; zu wenige Datenpunkte über 1 % Beanspruchung -> NO_VALUE; >99,5 % oberhalb 130 % -> Gerade Ursprung/Mittelwert zu 100 %; diffuse Punktwolke -> Unsicherheitsflag, gegebenenfalls erneutes Clustering.
- Für jedes Inselbildungs-/ungültige LODF-Ereignis BLOCKED/EXCEPTION_WITH_TSO_EVIDENCE, nie stillschweigend skippen.
- Wenn die Kapazitätsqualität schlecht bleibt, erzeuge gezielte Änderungsanforderungen und springe zurück zu **L3** mit neuer Kandidatengrenze, unverändertem Quotenbudget und erneutem globalem Fit. ENTSO-E priorisiert RMSE über Kapazitätsqualität; diese Reihenfolge beibehalten.

### L5 – Unabhängige Out-of-Sample-Validierung und Publikation
Auf verschlossenen Holdout-Stunden, den fünf unverändert externen Wetterjahren, mehreren Netzsituationen und vollständigem Kontingenzsatz prüfen:
- Bilanz-/Topologieinvarianten (harte Tests).
- Detail-gegen-Ersatz-Schnittfluss-MW-RMSE, Perzentile, Vorzeichen, globale und länderspezifische Fairness, kritische Leitungen, grenzüberschreitende Flüsse.
- Parametergüte, Sensitivität auf Kalibrierstunden, initiale x-Skalierung, Solverstabilität und numerische Identifizierbarkeit.
- Vier N-1-Kapazitätsqualitäten einschließlich Sonderfälle und Ausfälle.
- No-Load-Flows, operative HVDC-/PST-Wirkungen, Loop Constraints im **tatsächlich genutzten** Ersatznetzmodell.
- Eingangsasset- und zeitliche Zonenaggregation mit Summenerhaltung; keine eigene PECD-Datenbeschaffung.
Bei einer fehlenden realen Eingabe lautet die Freigabe **BLOCKED_DATA**, nicht PASS. Bei Fehlern wird zum frühesten ursächlichen Loop L0/L1/L2/L3/L4 zurückgegangen; jede Revision ist versioniert und gegenüber der vorherigen Kandidatenkonfiguration vergleichbar.

### Prozessübersicht
~~~text
externe Referenzdaten -> L0 physikalischer Preflight -> L1 Engpassranking und Start-Busmap
                                           |                           |
                                           +-- BLOCKED_DATA             v
                               L3 Kandidaten <-> L2 globaler x/c0-Fit
                                   |                   |
                                   |     RMSE-Gate, Accept/Rollback
                                   v
                            RMSE-Plateau -> L4 vier N-1-Kapazitäten
                                                |
                                          schlechte Qualität?
                                                | ja -> L3
                                                v
                                   L5 unabhängiger Holdout-Review
                                                |
                                   FAIL -> ursächliche Schleife
                                   PASS -> versioniertes Ersatznetz
~~~

## 5. Bewertungsmatrix und konkrete Tests

| Gate | Testfälle | Erwarteter Abnahmestatus |
|---|---|---|
| G01 Herkunft | Provenance/Hash, Einheit und fünf Wetter-IDs, Synchronität | harte Validierung oder BLOCKED_DATA |
| G02 Country-Budget | 37 Original-Labels, Summe 102; je Land die offizielle Anzahl; NI/UK bewusst getrennt | keine Überschreitung/Unterdeckung; FAIL bei Konflikt |
| G03 Connectedness | jedes Cluster zusammenhängend; Inseln, 110-kV-Kanten, Grenzknotenfälle; keine Landesmischung | FAIL bei Verstoß |
| G04 Dispatch/Screening | bilanzierte AC-Inseln, grenzüberschreitende PTDF, 225/400-MWh-Muster, Stundenlängen und variable Limits | analytisch/Fixture PASS |
| G05 Aggregation | A_z Gamma=P A_d; A_z f_target=p_z und Knoten-/Technologiesummen | numerisch nahe Maschinenpräzision |
| G06 Ersatznetz | x>0, rank, Skalenfixierung, A_z c0=0, affine KVL im operativen Netz | FAIL bei fehlender Netzgleichungsintegration |
| G07 Loop | je accepted/rejected candidate dieselben Zeitfenster, globaler Refit, reproduzierbares Ledger; mehrere abhängige Länder | keine Übernahme ohne gemessene Verbesserung |
| G08 RMSE | pro Link/global auf fixen Zeitfenstern, Topologie-Vergleichsdiagnose, Holdout, Warnfarben | dokumentiert; keine erfundene harte offizielle Farb-PASS-Schwelle |
| G09 N-1 | LODF gegen Direktausfall, Inselbildner, saisonale Limits, TSO-Ausnahmen | fail-closed |
| G10 Kapazitäten | 4 Richtungs-/Saisonwerte; 99,5-/1-/130-%-Sonderfälle; diffuse Wolken | QUALIFIED / PROXY / UNQUALIFIED / NO_VALUE |
| G11 HVDC/PST | Null-/Neutral-Kalibrierungsfall getrennt von aktiven Operationen; No-Load und Mesh | exakte, geprüfte Adapterfunktion |
| G12 Realnetz | unabhängiger offener/regulatorisch zulässiger Referenzdatensatz, festes Manifest, fünf Wetterjahre, reproduzierbare P/F-Metriken | nur nach realer Ausführung REAL_QUALIFIED |

Zusätzliche **Negativtests**: Bus ohne Land, Grenzcluster, ungeeignete Länderquote, unbalanced Dispatch, asymmetrische s_nom-/MW-Grenzen, entgegengesetzte Parallelflüsse, schwach belastete N-1-Wolke, kein Richtungssample, LODF-Islanding, PST/HVDC ohne explizite Semantik, Non-Convergence, Re-Clustering mit geänderter Linkzahl, und mehr als eine AC-Insel. Bestehende Tests allein belegen diese Pfade nicht.

**Unabhängiger Benchmark:** synthetisch 3- bis 50-Bus mit mindestens drei gekoppelten Ländern; anschließend mittleres realistisches Netz; erst dann paneuropäisches Netz. Auf keiner Stufe eine Jahres-/Länderteilnetz-Fitqualität als Beweis für eine voll gekoppelte Europaqualität ausgeben.

## 6. Konkrete Makroaufträge und Zuständigkeiten

| Auftrag | Priorität | Zuständige Rolle | Umfasst | Abnahme / Folge |
|---|---|---|---|---|
| **M2-MA0** – Methodenreview & Contract Freeze | **hier statisch vorbereitet** | S-GOV-M2 + unabhängiger Methodikreviewer | dieses Dokument; 18er-Matrix; Input-/Output-Verträge; eindeutige D/T/I/B/X-Liste | Owner bestätigt nur eigene I-Entscheidungen; bestehende offizielle D nicht neu verhandeln |
| **M2-MA1** – Physical Foundation + Quota Clustering | P0 | 2 parallele Worker: W-PHY (AC-Physik/Adapter), W-CLU (Land/Graph/102); differente Reviewer R-PHY und R-CLU | Multi-AC-Subnetwork-Verträge, HVDC/PST/Trafo-Semantik, sparse Solver; country-aware seed, 225/400-Screening, Conformance/Edge-Fixtures | G01–G05, G11; Status abhängig von externen Realinputs |
| **M2-MA2** – x/c0 & gekoppelte Iterations-Engine | P0 | W-EQ + W-ITER; unabhängiger R-NUM | globale fit/affine-Mesh Integration, Kandidatensuche inkl. Coupled-Country-Moves, 3-fach Zeit-Split, RMSE und Ledger, Plateau/Rollback | G05–G08; Regression Initial-vs-Iterated auf identischer Fixture |
| **M2-MA3** – N-1-Kapazität & Output Contract | P0/P1 | W-SEC und W-EXPORT, unabhängiger R-SEC | 4-Wege-Kapazitäten, 99,5-/1-/130-Regeln, invalid LODF-Ausfälle, PST/HVDC-/No-Load-Ausgaben, reduzierte Netzexporte; optionale Asset-Join-Rezeption ohne PECD-Reader | G09–G11 + integrierte End-to-End-Fixtures |
| **M2-MR1** – Independent Numeric/Method Reviewer | P0-Gate | anderer Reviewer, nicht MA1–3 implementierend | Codeaudit; Gate-Replay; Referenznetz und Out-of-Sample; Fehlerszenarien; Quellenbelege; Entscheidung REPAIRS_REQUIRED / SYNTHETIC_QUALIFIED / REAL_QUALIFIED | keine Owner-Realnetzfreigabe ohne echten Referenznachweis |

**Parallelisierung:** Nach dem MA0-Contract-Freeze können in MA1 W-PHY und W-CLU auf getrennten Branches/Worktrees parallel arbeiten; W-SEC kann die offiziellen Spezialfälle bereits fixturebasiert vorbereiten, solange der N-1-Schnittstellenvertrag eingefroren ist. MA2 darf erst den integrierten physikalischen/Topologie-Contract voraussetzen; W-EQ und W-ITER können getrennt entwickeln, aber erst nach gemeinsamer Refit-Integration abnehmen. W-EXPORT kann parallel zu W-SEC arbeiten. Reviewer sollen **andere** Agenten sein als implementierende Worker; Merge nur nach überprüfbarem Commit und Reviewer-Handoff.

**Kritischer Pfad:** Quoten-/Country-Mapping + physikalische Eingangssemantik -> globale Kalibrierung -> Re-Clustering-Iteration -> 4-fach N-1 -> unabhängige Qualifikation. Dateninputs und Ausfallregeln sind echte Blocker, die kein CI-Sieg auf synthetischen Netzen entfernt.

## 7. Repository-Handhabung und maschinenlesbare Artefakte

Empfohlener neuer Produktpfad (nach Review-Freigabe):
- src/tyndp_reduce/iosn_official/contracts.py
- src/tyndp_reduce/iosn_official/screen.py
- src/tyndp_reduce/iosn_official/seed.py
- src/tyndp_reduce/iosn_official/equivalent_network.py
- src/tyndp_reduce/iosn_official/iterate.py
- src/tyndp_reduce/iosn_official/n1_capacity.py
- src/tyndp_reduce/iosn_official/evaluate.py
- tests/iosn_official/ (Fixtures für jedes Gate)
- results/iosn_official/<run_id>/manifest.json; country_quotas.csv; branch_criticality.csv; busmap.csv; fit.json; rmse_per_link.csv; candidate_ledger.csv; four_way_capacity.csv; exception_ledger.csv; independent_review.md.

Dies ist ein **empfohlener** Namensraum, kein Anlass zur unnötigen Neuschreibung stabiler src/tyndp_reduce-Bausteine. Möglichst bestehende Funktionen via geprüfte Adapter wiederverwenden. Unverifizierte Daten niemals als „offiziell reproduziert“ beschriften. Die offiziellen Anforderungen aus [der 18-Punkte-Matrix](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md) bleiben das detaillierte source-of-truth-Register.

### Freigabestatus
- **AUDIT_ONLY:** dieser Review, keine neue Laufzeitevidenz.
- **SYNTHETIC_QUALIFIED:** alle belegbaren formalen/fixture G01–G11 erfüllt, aber keine realen Eingangsdaten; keine REAL_QUALIFIED-Freigabe.
- **BLOCKED_DATA:** notwendige Netze/Zeiten/Limit-/Kontingenzwerte fehlen.
- **REPAIRS_REQUIRED:** reproduzierbare implementierungs- oder methodenrelevante Gate-Verstöße.
- **REAL_QUALIFIED:** unabhängige, vollständig dokumentierte Referenznetz-Qualifikation mit G01–G12 bestanden. Keine pauschale Behauptung, proprietäre ENTSO-E-Software exakt nachgebildet zu haben.

## 8. Nächste Aktion

M2-MA1 als **ein** konsolidiertes Ausführungsmakro starten: zwei implementierende lokale Worker/Subagenten plus zwei unabhängige Reviews, gegenseitige Review-Handoffs, verbindlicher Evidence-/Commit-Freeze. Danach M2-MA2, M2-MA3 und M2-MR1. Der separate Copy-ready-Auftrag steht in **81_M2_MA1_COLD_START_HANDOFF_2026_11_03.md**.

**Bedingungen:** keine Änderungen an M0- oder M1-Implementierungen; keine per-country unabhängigen Lastflussmodelle; keine Wahl neuer Wetterjahre; keine eigenentwickelte multikriterielle Clustering-Zielfunktion als angeblich offiziell; keine verdeckten N-1-Ausfallausnahmen; keine Realnetz-PASS-Behauptung ohne reale Referenz.
