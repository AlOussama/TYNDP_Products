# IoSN 2026 – verbindliche Methodik-zu-Code-Traceability für die Netzreduktion

**Status:** Wissenschaftlich-technischer Implementierungs-Audit / reproduzierbare Spezifikation, **keine** Behauptung einer vollständigen ENTSO-E-Reimplementierung und **keine** Freigabe eines Realnetz-End-to-End-Laufs.  
**Datum:** 26.10.2026  
**Repository-Basis:** `AlOussama/TYNDP_Products`, `main` bei Commit `1595d6d38e77804760612621657721b3699d2fea`.  
**Scope:** ausschließlich **Netzreduktion** (Zonierung, europaweite physikalische Abbildung, Ersatzreaktanzen/Zero-Balance-Flows, RMSE, N-1-Ersatzkapazitäten, Ausgabe- und Zuordnungsschnittstellen). Die **fünf bereits festgelegten Wetterjahre sind unveränderte Eingangsdaten**. Wetterjahrauswahl, Wetterjahre-Clustering, Methode B und FBMC gehören **nicht** zur offiziellen Reimplementierungs-Baseline.

## 0. Verbindliche Primärquelle und Erkenntnisstatus

**Alleinige normative Referenz:** ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology — Version for Public Consultation, 25 February 2026*, insbesondere **§ 3.8, Druckseiten 21–29**, **§ 3.9, S. 29**, **Anhang 6.1, S. 45–51**.  
PDF: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf  
Wichtig: Es handelt sich ausdrücklich um eine **Konsultationsfassung**. Dieses Dokument behauptet weder, dass sie final ist, noch dass ein interner ENTSO-E-Quellcode vorliegt. PyPSA und die Repository-Dateien sind **Implementierungswerkzeuge**, keine normative Quelle.

- **D** — direkt dokumentierte fachliche Festlegung (verbindlich übernehmen).
- **T** — rein technische/physikalische Formalisierung von D, ohne neue Zielfunktion als angeblich offiziell auszugeben.
- **U** — öffentlich **unterbestimmte algorithmische Einzelheit**; benötigt eine explizit als eigene Festlegung gekennzeichnete Entscheidung.
- **I** — minimale, **eigene** und überprüfbare Implementierungsentscheidung zur Schließung einer U-Lücke.
- **B** — Daten-/Werkzeug-/Integrationsblocker: auch mit beschriebener Methodik noch nicht ausführbar.
- **X** — bewusst nicht im offiziellen Baseline-Scope.

Diese Kategorien gelten pro **Einzelregel**; ein Kapitel kann D- und U-Anteile zugleich enthalten.

## 1. Wissenschaftlicher Kern und unveränderliche Invarianten

### 1.1 Ein europäisches elektrisches Modell, nationale Zonenrestriktionen

Die detaillierte Referenz umfasst die grenzüberschreitenden AC-Verbindungen **durchgehend**. Nationale Grenzen sind **nur Restriktionen der Clusterzuordnung**, nicht Trennstellen im Lastflussmodell. ENTSO-E berichtet, dass Iterationen Änderungen in **mehreren voneinander abhängigen Ländern gemeinsam** untersuchen (Anhang 6.1, S. 46), während geografische Landesgrenzen **nicht verschoben** werden (S. 47). Die optimierte Flussqualität ist europaweit auszuwerten.

Für die Knotenmenge \(\mathcal N\), die Landeszuordnung \(c:\mathcal N\to\mathcal C\) und Busmap \(z:\mathcal N\to\mathcal Z\) gilt:

\[
z(i)=z(j)\;\Rightarrow\;c(i)=c(j).
\]

Zugleich müssen die interzonal wirkenden **grenzüberschreitenden Leitungen** im Detailnetz, der PTDF und der Aggregationsmatrix enthalten bleiben. **Niemals** nationale Teilnetze mit unabhängigen Slacks als Ersatz für das gemeinsame physikalische Referenznetz auswerten.

### 1.2 Länderbudget aus Tabelle 3 — keine Neukalibrierung

Die offizielle Studie nutzt **102 Zonen** mit publizierter Landesaufteilung (S. 26–27). Exakte Abschrift in  
[IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv](IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv).

Prüfinvarianten:

\[
\sum_{c\in\mathcal C} k_c=102,\qquad
\#\{z(i):c(i)=c\}=k_c,\qquad
\forall Z_j:\; c(Z_j)\text{ eindeutig}.
\]

Die CSV verwendet **Original-Länderbezeichnungen** aus Tabelle 3, darunter gesondert „Northern Ireland“ und „United Kingdom“. Der Datensatzadapter muss die exakte Zuordnung zu den tatsächlichen Netzmetadaten explizit klären; **keine stillschweigende ISO-Code-Normalisierung oder Zusammenlegung**. Komponenteninseln, deren physischer Graph die vorgegebene Anzahl zusammenhängender Zonen nicht zulässt, sind als Daten-/Topologie-Konflikt zu melden, nicht durch künstliche AC-Leitungen zu „reparieren“.

### 1.3 Netzinvarianten

Für jede zulässige Busmap:

- Genau **eine** Zone je AC-Knoten; **jede Zone topologisch zusammenhängend** auf dem vereinbarten AC-Graphen (§ 3.8.1, S. 24).
- Orientierungskonsistente Knoten-/Schnittoperatoren \(P,\Gamma\) und zonale Inzidenz \(A_z\):

\[
p_{z,t}=P p_{d,t},\quad f_{z,t}^{\mathrm{target}}=\Gamma f_{d,t},
\quad A_z\Gamma=P A_d,\quad A_zf_{z,t}^{\mathrm{target}}=p_{z,t}.
\]

- Grenzüberschreitende Detailzweige werden für interzonale Flüsse **nicht entfernt**. Parallele physische Grenzzweige können zu einem Ersatzlink addiert werden, ihre gegenläufigen Flüsse müssen aber eigens diagnostiziert werden (§ 3.8.1, S. 23–24).
- AC-Inseln sind getrennt zu bilanzieren. HVDC ist keine passive AC-Leitung. PST und nicht neutrale Transformatorphasen erzeugen gesonderte Effekte. Ein rein passives Ein-Insel-DC-Modell gilt **nicht** als Gesamteuropa-Nachweis.
- Die im offiziellen § 3.8.2 verwendete Kupferplattenannahme beseitigt intrazonale Engpässe **im reduzierten Modell**, nicht nachweislich im detaillierten physikalischen Netz.

## 2. Vollständige Primärquellen-zu-Code-Matrix

| ID | Verbindliche Fundstelle | Was ENTSO-E beschreibt | Übersetzung / vorhandene Code-Basis | Status und genuine Lücke |
|:--|:--|:--|:--|:--|
| NR-01 | § 3.8, S. 21–23; Abb. 4 | Klassische Market Study (NTC), Dispatch-Sample, detaillierter PTDF/Lastfluss, gemeinsamer Weg zu Clustering und Ersatzparametern | Für jede Referenzstunde vollständige nodale Nettoeinspeisung und synchronen Detailfluss speichern; `dc.py`, `screening.py` | **D/T+B**: realistischer Market-Dispatch-/Netzdatensatz und AC-Komponentenadapter fehlen |
| NR-02 | Anhang 6.1, S. 45 | 225-/400-kV-Leitungen stündlich prüfen; **jährliche Überlastungsenergie in MWh** als Kritikalitätsranking | \(S_{\ell,y}=\sum_{t\in y}\Delta t\,\max(0,|f_{\ell,t}|-\bar F_{\ell,t})\); `screening.method_a` | **D/T**: Kern vorhanden; Spannungsfilter, zeitabhängige Limits, Jahresselektion, MW-Grenzkonvention und Szenarioaggregation offen |
| NR-03 | § 3.8.1, S. 23–24; Abb. 5 | Möglichst kritische/sensitive Leitungen als Interzonenverbindungen; flusssynchrone Grenzleitungen, geringe Zonenanzahl, Konnektivität, balancierte Zonengröße | Edge-Ranking und Schutzkandidaten, Konnektivitäts-Checks; `clustering.py` | **D+U**: keine vollständige veröffentlichte kombinierte Clustering-Zielfunktion oder harte Schutz-Top-K-Vorgabe |
| NR-04 | § 3.8.1, S. 25–27; Tab. 3; Anhang 6.1, S. 47 | Verwendete **102 Zonen pro festgelegter Landesverteilung**, geografische Grenzen unveränderlich | CSV-Budget; Länderreinheit und per-country counts als strikte Busmap-Assertions | **D/T**: `greedy_busmap` hat derzeit nur **globale** Zonenanzahl, keine Länderquoten |
| NR-05 | § 3.8.1, S. 23–27 | Detaillierte Zuordnung von Knoten zu initialen Zonen; topology-connected clusters | Deterministische zulässige Start-Busmap aus Land, Graph, Kritikalitätsranking und Budget | **U/I**: vollständiger veröffentlichter Initialisierungsalgorithmus fehlt |
| NR-06 | Anhang 6.1, S. 45–47 | Kritische Lücken finden, Clustering anpassen, Karte/Indikatoren beurteilen, Änderungen behalten/verwerfen; mehrere gekoppelte Länder gemeinsam | Europäische iterative Kandidatensuche; Kandidaten können Änderungen in mehreren Ländern **simultan** enthalten | **D+U/I**: Nachbarschaftsoperator, Suchreihenfolge, Maximalrunden, Plateau-Toleranz nicht publiziert |
| NR-07 | § 3.8.2, S. 27 | Interzonen-Verbindungen nach Knotenzusammenfassung, KCL und KVL | `aggregation.build_aggregation` erzeugt \(P,\Gamma,A_z\), prüft \(A_z\Gamma=P A_d\) | **T**, synthetischer Kern vorhanden, Realnetzkomponenten offen |
| NR-08 | Anhang 6.1, S. 48–49 | Synchrone Marktszenario-Flüsse; parameterbezogene **DC-Lastfluss-Sensitivitäten** um Referenzzustand, stündliche Rekonstruktion | \(f(t)=f^{ref}+\sum_p h_p[m_p(t)-m_p^{ref}]\); nodale PTDF nur bei gesicherter Äquivalenz der Parameterabbildung einsetzen | **D+U/B**: Auswahl der sensitiven Marktdatenparameter, Störungsschritte, Stützstunden und Datenprovenienz nicht voll publiziert |
| NR-09 | Anhang 6.1, S. 49 | Zur **Impedanzkalibrierung** HVDC-Setpoints im AC-Gitter auf null, PST auf neutral | Getrennte Kalibrierungskonfiguration; Änderungen der NTC-Referenzflüsse und aktiven Geräte konsistent behandeln | **D+B**: `pypsa_adapter.py` verwirft Links/Transformatoren/PST statt sie vollständig einzubinden |
| NR-10 | § 3.8.2, S. 27; Anhang 6.1, S. 48–49 | Optimierung der Ersatzimpedanzen **und** Zero-Balance-Flow-Korrekturen gegen Detail-Zielflüsse | Positiv beschränkte \(x\), zonal bilanzneutraler Offset \(c^0\), RMSE-Fit über europaweite Referenzstunden; `equivalent.fit_equivalent` | **D+U/I**: Solver, Gewichte, Regularisierung, Eichung, Stichproben, globale Optimalität nicht publiziert |
| NR-11 | Anhang 6.1, S. 49 | Kirchhoff-Maschenbedingung \(\sum_{i\in m}X_iF_i=0\) im DC-Ersatznetz; gleichzeitig strukturelle Flusskorrekturen | Physikalisch konsistente **affine** Modellform bei nichtverschwindendem \(c^0\) definieren und im Marktsolver implementieren | **D+U/B**: genaue Verbindung der offiziellen homogenen KVL-Darstellung mit additivem \(c^0\) nicht vollständig angegeben |
| NR-12 | Anhang 6.1, S. 46–47; Abb. 13 | **RMSE** als primäre Übernahmeentscheidung; nach Plateau Kapazitätsqualität als weiteres Kriterium; farbliche Kennzahlen | RMSE je Link und globale Kennzahl; Kandidatenvergleich nach jeweils erneutem Ersatznetz-Fit | **D+U/I**: Mittelungs-/Normierungsvorschrift und Umgang mit unterschiedlichen Linkmengen nicht vollständig angegeben |
| NR-13 | § 3.8.2, S. 27; Anhang 6.1, S. 50 | N-1-sichere Ersatzkapazität auf Basis physischer Grenzzweige und **LODF**; höchste N-1-Auslastung je Grenzschnitt | Detail-PTDF/LODF, N-0/N-1-Ladungen, netzphysikalische Sicherheitsdiagnostik; `security.py` | **D/T+B**: verbindliche Kontingenzliste, saisonale Notfallgrenzen, TSO-Maßnahmen fehlen |
| NR-14 | § 3.8.3, S. 28; Anhang 6.1, S. 50–51 | **Vier** gerichtete/saisonale Kapazitäten je Ersatzlink; Punktwolke „Gesamtaustausch vs höchste Auslastung“, Schnitt mit 100 % | Vier getrennte Datensätze pro Schnitt und zulässige, qualitätsmarkierte Fits | **D+U/I**: Fitfunktion, Repräsentativitätsfenster, Stichprobengröße, Auswahl/Interpolation nicht vollständig publiziert |
| NR-15 | Anhang 6.1, S. 51 | Sonderfälle: >99,5 % nur eine Richtung → andere Richtung spiegeln; >1 % Mindestbelastung; >99,5 % Punkte oberhalb 130 % → Ursprung-durch-Mittelpunkt-Extrapolation; diffuse Punktwolke → Warnung/neu clustern | Explizite Statuscodes und deterministische Sonderfallzweige | **D/T** für Grenzwerte; **U/I** für „genügend“ Stützpunkte und diffuse Punkte |
| NR-16 | § 3.8.3, S. 28 | Ausgaben: No-Load-Flows, Maschengleichungen, HVDC-Einfluss auf No-Load-Flows, vier Kapazitäten, Ersatzimpedanzen, PST-MW-Wirkungsbereich | Getrennte benannte Outputobjekte mit Gültigkeitsflag | **D+B**: HVDC-/PST-Integration im aktuellen Adapter fehlt |
| NR-17 | § 3.8.4, S. 28–29 | PEMMDB-Anlagen am Detailknoten, Nachfrage (fix/flexibel), TSO-Lastsplits, RES-PECD-Profilabgleich, konsistente thermische Stückzahlen/Kapazitäten | Zonenaggregation **nach** der finalen Busmap mit technologie- und variablenspezifischen Schlüsseln | **D+B**: vollständige TSO-/PEMMDB-/PECD-Eingangstabellen nicht vorhanden/verifiziert |
| NR-18 | § 3.9, S. 29 | Unterscheidung Netzphysik im LF-Investitionsmodus und nachgelagerter Bewertung interner Kapazitätsrestriktionen | Separate Modus- und Constraint-Flags; keine Vermischung mit Reduktions-Kalibrierung | **D+U**: sprachlich heikle Aussage „only cross-border capacities activated“ vs. „interzone capacities ... infinity“; modusspezifisch zu interpretieren und testen |

**Wichtig:** Der veröffentlichte Text spezifiziert **keine** multidimensionale Knotenmetrik aus elektrischer Distanz, PTDF-Spalten, Wind/PV und Last als normative Clustering-Zielfunktion. Ein solches Verfahren ist deshalb **nicht Teil dieser Baseline**. Gleiches gilt für die im Repository separat vorhandene RES-/Last-Screening-Methode B und FBMC-Experimente.

## 3. Ausführbarer Baseline-Prozess

### 3.1 Datenvertrag

**Eingaben:**
1. `detailed_grid`: eindeutige Knotennamen, veröffentlichte Landes-/Gebietsidentitäten, orientierte AC-Zweige, Transformatoren, HVDC-Endpunkte, PST, Reaktanzen, Spannungsebenen, Leitungs-/Saisonlimits, Betriebszustände und AC-Inselzugehörigkeit.
2. `market_reference`: NTC-basierter vollständiger klassischer Marktdispatch; Knoten-Einspeisezuordnung nach Technologie, alle Lasten, Speicher, HVDC-Endpunktbilanzen, synchroner Zeitstempel; je AC-Insel bilanziert.
3. `time_set`: die **fünf extern festgelegten Wetterjahre** plus verbindliche Stundenmaske, Stundenlänge und Ziel-/Szenariobezeichnung; **keine** interne Auswahl oder Optimierung der Jahre.
4. `country_budget`: offizielle 102-Zonen-Tabelle.
5. `contingencies`: freigegebene CNEC-/Ausfallliste samt Normal-/Notfallgrenzen, TSO-seitig begründeten Ausnahmen und Inselbildungsbehandlung.
6. `asset_allocation`: PEMMDB-Anlagenknoten, TSO-Lastsplits, PECD-Zuordnung sowie ggf. PST-/HVDC-Fähigkeitsdaten.

Fehlt eine notwendige Quelle, muss der betreffende Schritt als **BLOCKED_DATA** ausgeben. Synthetische oder ersetzte Inputs dürfen in einer separaten Demonstration verwendet werden, jedoch **nicht** unter demselben Freigabestatus.

### 3.2 Ref-PTDF und Engpassranking

Bei einem vollständigen bilanzierten Einspeisevektor \(p_d(t)\) (je AC-Insel) gilt für das passende DC-Modell:

\[
f_d(t)=H_d\,p_d(t)+b^\phi_d(t).
\]

Die offizielle Sensitivitätsbeschreibung (S. 49) bildet insbesondere die Änderung von **Marktparametern** relativ zu einem Referenzfall ab. Wenn direkt nodale PTDF verwendet werden, muss die identische Parameter-zu-Injektions-Abbildung nachgewiesen werden; die beiden Matrizen dürfen **nicht** stillschweigend gleichgesetzt werden.

Nur für die beschriebenen 225-/400-kV-Leitungen:

\[
S_{\ell,y}=\sum_{t\in y}\Delta t_t \max(0, |f_{\ell,t}|-\bar F_{\ell,t}).
\]

- Die **Einzeljahres-Scores** werden unverändert gespeichert; eine zusätzliche Aggregation über fünf feststehende Jahre wäre **eigene** Gewichtungsentscheidung, solange ENTSO-E sie für diese Fünfer-Eingabe nicht spezifiziert.
- Die detaillierte europäische Topologie und **alle** Leitungsflüsse bleiben für die nachfolgenden Schritte erhalten — der 225-/400-kV-Filter begrenzt **nur das dokumentierte Clustering-Screening**.
- Die Wahl der thermischen MW-Äquivalente, seasonal ratings und eines konsistenten Market-Dispatch wird als Datenvertrag dokumentiert.

### 3.3 Start-Busmap (einzige zwingende Suchheuristik)

**Eigenentscheidung I-01:** deterministische topologisch beschränkte Kantenkontraktion/Region-Growing auf der **vollständigen** Netzgraph-Datenbasis, aber ausschließlich mit Merge-Operationen zwischen Knoten **desselben Landes**. Länderquoten \(k_c\) werden **je Land** eingehalten. Das ist eine **Initialisierung**, ausdrücklich nicht die publizierte ENTSO-E-Originalsoftware.

- Kritikalitätsranking und sensible Grenzleitungen steuern nur die Kandidatenpriorität.
- „Protected“ Kanten sind nur dann ein **hartes** Verbot, wenn eine explizite Schutzliste vorliegt und die 102-Zonen-Realisierbarkeit erhalten bleibt. ENTSO-E schreibt „when possible“ für das Erfassen kritischer Leitungen; eine automatische harte Sperre der Top-N-Leitungen wäre eine zusätzliche Methode.
- Zu jeder Start-Busmap werden Verletzung des Kritikalitätsschutzes, gegenläufige Grenzflüsse, topologische Qualität und Größenunterschiede dokumentiert.

### 3.4 Einheitliche europaweite Zielgrößen

Für **jede** Kandidaten-Busmap dieselben gespeicherten, synchronisierten Detailflüsse aus dem gesamteuropäischen Netz verwenden:

\[
f^{target}_z(t)=\Gamma(z)f_d(t),\quad
p_z(t)=P(z)p_d(t).
\]

Die physische Wirkung aus **anderen Ländern** bleibt im Referenzfluss enthalten. Der gewünschte europäische Schnittfluss wird aus der orientierten Summe der Originalzweige berechnet, auch bei grenzüberschreitenden Zonenpaaren. Knoten-/Länderzuordnung ist davon unabhängig.

### 3.5 Ersatzreaktanzen und strukturelle Flusskorrektur

Minimal ausführbare eigene mathematische Rekonstruktion der dokumentierten Impedanzoptimierung:

\[
\min_{x>0,\;c^0}\;
 \sum_{t\in T_{cal}}\sum_{e\in E_z}
 w_{e,t}\left(
 [H_{eq}(x)p_z(t)]_e+c^0_e-f^{target}_{z,e}(t)
 \right)^2+
 \lambda_x R_x(x)+\lambda_cR_c(c^0)
\]
\[
A_z c^0=0.
\]

- \(H_{eq}(x)\) muss aus dem **gesamten europäischen äquivalenten AC-Netz** und seinen Maschen berechnet werden, nicht länderweise.
- Positive \(x\); Skaleneichung **pro AC-Insel**, geeignete Schranken und dokumentierte Regularisierung. Ein baumförmiges Ersatznetz identifiziert aus Flüssen **keine** einzelnen Reaktanzen; Rank-/Konditionsdiagnostik Pflicht.
- Im **Kalibrierungsfall** HVDC-Setpoints im AC-Netz auf 0 und PST neutral setzen (offizielle S. 49); die späteren operationalen HVDC-/PST-Einflüsse müssen gesondert ausgegeben und modelliert werden (S. 28).
- Die Datenstichprobe \(\mathcal T_{cal}\), Gewichte, Solver und Regularisierung sind **nicht offiziell publiziert**. Minimaloption: deterministisch versionierte repräsentative synchrone Zeitpunkte; unabhängige Teststunden zurückhalten und die Sensitivität gegen Stichprobengröße dokumentieren.

**Kritischer Modellkonsistenz-Gate:** Die offiziell auf S. 49 angegebene homogene KVL-Maschengleichung \(\sum_{i\in m}X_iF_i=0\) und ein nicht verschwindender additiver Loop-Offset \(c^0\) können **nicht** gleichzeitig für den **gesamten** Fluss auf einem rein passiven AC-Ersatznetz gelten. Bei einem Modell \(f=H_{eq}(x)p+c^0\) ist eine konsistente **affine** Maschenformulierung beispielsweise:

\[
A_z f=p_z,\qquad
C_z^\top\mathrm{diag}(x)(f-c^0)=0,\qquad
A_zc^0=0,
\]

mit Zyklusmatrix \(C_z\) (\(A_zC_z=0\)). **Dies ist eine eigene technische Implementierungsform, keine als solche veröffentlichte ENTSO-E-Gleichung.** Sie muss im eigentlichen Simulations-/Marktmodell durchgängig gelten. Der vorhandene reine Fit `equivalent.py` genügt **nicht**, solange der Offset nur im Postprocessing addiert und nicht in die Netzgleichungen eingebunden wird.

### 3.6 RMSE und europaweite gekoppelte Re-Clustering-Schleife

Je Ersatzlink auf den **gleichen** synchronen Referenzstunden:

\[
\mathrm{RMSE}_e=
\sqrt{\frac{1}{|T|}\sum_{t\in T}
(\widehat f_{e,t}-f^{target}_{e,t})^2},
\quad
\mathrm{RMSE}_{global}=
\sqrt{\frac{1}{|E_z||T|}\sum_{e,t}
(\widehat f_{e,t}-f^{target}_{e,t})^2}.
\]

**Eigene Minimalentscheidung I-02:** Diese ungewichtete globale Größe zunächst als deterministischen Optimierungsindikator verwenden, **zusätzlich** Link-RMSE, absolute Fehler-Quantile und Grenzleitungs-Kritikalität ausgeben. Die Normierung in „RMSE/flow“ sowie eine voll vergleichbare Metrik für *geänderte Linkmengen* sind nicht publiziert; daher die globale Kennzahl **nicht als exakte interne ENTSO-E-Formel** ausgeben.

Abb. 13 (S. 46) enthält **indikative Klassen**:
- grün: annual RMSE ≤ **200 MW** **oder** RMSE/flow ≤ **10 %**;
- gelb: ≤ **350 MW** oder ≤ **20 %**;
- rot: ≤ **500 MW** oder ≤ **30 %**;
- schwarz: RMSE > **500 MW** **und** RMSE/flow > **30 %**.

Die genaue relative Nennerdefinition, Aggregationsvorschrift und Farbvorrangregel sind nicht publiziert. **Keine fiktive normative PASS-Schwelle** aus dieser Grafik ableiten.

Für die Kandidatensuche **I-03**:
1. Frühestens nach vollständig ausgeführter europaweiter Ersatznetzkalibrierung einen Ist-Kandidaten bewerten.
2. Eine kleine Menge gültiger **zusammenhängender** Grenzknoten-/Teilgebietsverschiebungen oder gebündelter Änderungen in **mehreren elektrisch gekoppelten Ländern** vorschlagen; keine Landesgrenze übertreten, Quoten nicht verändern.
3. Für jeden Kandidaten \(P,\Gamma\) aktualisieren, dann europaweit \(x,c^0\) **neu** schätzen und RMSE **neu** berechnen.
4. Nur tatsächlich gemessene Verbesserungen annehmen. Bei numerischem Plateau zusätzlich die **Kapazitätsqualität** beurteilen; diese hat laut S. 47 nachrangigen Stellenwert.
5. Suchreihenfolge, Budget, Plateau-Toleranz, Tie-Breaker, Kalibrierungs-/Validierungssplit und alle verworfenen Kandidaten protokollieren. Die genaue Suchheuristik ist nicht veröffentlicht.
6. Bei unterschiedlichen Ersatzlinkmengen ist ein reiner Vergleich der Mittel-RMSE verzerrbar; deshalb zugleich erhaltene kritische Grenzleitungen, Linkzahl, Verschiebungen und linkübergreifende Qualitätsverteilung dokumentieren. Ein offizieller einheitlicher Matching-Operator ist nicht publiziert.

### 3.7 N-1-Ersatzkapazitäten — erst nach finalisierter Busmap

Anhang 6.1 S. 50–51 spezifiziert:

1. Original-Grenzleitungsflüsse und LODF-basierte N-1-Auslastungen aus **derselben** detaillierten physikalischen Referenz berechnen.
2. Stundenpunkte für **Sommer/Winter** und **beide Richtungen** getrennt bearbeiten — **vier** Resultate je Ersatzlink.
3. Pro Zeitpunkt den (orientiert aufsummierten) Ersatzschnittfluss der **maximalen N-1-Grenzleitungsbelastung** gegenüberstellen.
4. Ersatzkapazität ist der äquivalente Austausch bei **100 %** maximaler Grenzbelastung.
5. Prüfen, ob ausreichend Stützpunkte um 100 % vorliegen; die genaue Fensterbreite und Mindestzahl sind **U**.
6. Wenn >**99,5 %** der Jahresstunden nur eine Flussrichtung zeigen, die **Gegenrichtung** mit demselben Kapazitätswert belegen (dokumentierter Sonderfall).
7. Bei zu wenigen Punkten mit Auslastung >**1 %**: **kein Wert** (offizieller Sonderfall); kein stillschweigendes Default.
8. Wenn >**99,5 %** aller Punkte über **130 %** liegen: Ausgleichsgerade vom Ursprung durch den Punkt der mittleren Datenwerte, Auswertung bei 100 % (dokumentierter Sonderfall).
9. Bei „cloud of data points“ Warn-/Unsicherheitsstatus; ggf. **Re-Clustering** statt scheinpräzisem Limit.

**Eigene Minimalentscheidung I-04:** Für den generischen, nicht publizierten Fitfall eine transparente, explizit als **Proxy** gekennzeichnete Regression \( \rho=\beta_0+\beta_1|F_z| \) verwenden und \( \rho=1\) schneiden. Fitfenster, minimale Stützmenge, slope/correlation gates und Extrapolationsbereich sind Konfigurationsparameter, deren Wert **nicht** als offizielle ENTSO-E-Vorgabe auszugeben ist. Bei nicht identifizierbarer Beziehung `UNQUALIFIED` oder `NO_VALUE` statt impliziter Sicherheitsbescheinigung.

Die bestehende Funktion `seasonal_directional_limits` besitzt Defaults (`minimum=12`, `min_correlation=.75`, `minimum_observed_rho=.25`) **ohne normative Herkunft** aus dem IoSN-Text und bildet die offiziellen 99,5-/1-/130-%-Sonderfälle nicht vollständig ab. Sie ist ein Forschungsschätzer, **kein fertiger IoSN-Kapazitätsalgorithmus**.

Nicht definierte/inselbildende LODF-Ausfälle dürfen **nicht stillschweigend übersprungen** werden. Die Dokumentation erlaubt TSO-seitig begründete Modellierungsentscheidungen/Ausnahmen (S. 47); für jede Ausnahme einen expliziten CBCO-/TSO-Quellennachweis führen. Analytische K2/K3-/CNEC-/FBMC-Alternativen im Repository dürfen nicht unbemerkt die offizielle S. 50–51 beschriebene Punktwolkenroute ersetzen.

### 3.8 Finales Datenprodukt

Für einen qualifizierten Kandidaten mindestens:
- versionierte `busmap`, Landesbudget, Länderreinheits- und Konnektivitätsnachweis;
- europäische detaillierte und aggregierte Flussreferenzstunden, \(P,\Gamma,A_z\);
- geometrisch/topologisch eindeutige AC-Ersatzlinks, \(x_{eq}\), \(c^0\), **wirksame** affine Maschengleichungen;
- No-Load-/Loop-Flows, HVDC-Einfluss und PST-MW-Bereiche (§ 3.8.3);
- **vier** N-1-Kapazitätsfelder samt `QUALIFIED / PROXY / UNQUALIFIED / NO_VALUE`, Dokumentation möglicher TSO-Ausnahmen;
- RMSE je Link und gesamteuropäisches Validierungsledger;
- PEMMDB-/PECD-/TSO-basierte zonale Marktzuordnung aus § 3.8.4 (getrennte Behandlung fixer/flexibler Nachfrage, EE und thermischer Anlagen);
- gesonderte Kennzeichnung, welche Kapazitäten in der **LF-Investitionsrechnung** und welche erst in den nachgelagerten Dispatchprüfungen wirken (§ 3.9).

## 4. Normativer Minimal-Codeablauf (Pseudocode)

~~~python
def iosn_reduction_official_baseline(inputs):
    check_provenance_and_balances(inputs)       # 5 vorgegebene Jahre; keine Neuauswahl
    k_country = read_official_table3_budget()   # 37 publizierte Einträge, Summe 102
    detail = build_pan_european_ac_network(inputs)    # Ländergrenzen NICHT entfernen
    f_detail = reconstruct_synchronous_detail_flows(detail, inputs.market_reference)
    annual_scores = screen_225_400_kv_annual_overload(f_detail, inputs)
    z = deterministic_feasible_initial_busmap(detail, k_country, annual_scores)  # I-01

    fit = full_europe_calibration(detail, z, f_detail, inputs.calibration_hours)
    validate_busmap_and_affine_network(detail, z, fit)
    ledger = [audit_candidate(z, fit)]

    while search_budget_not_exhausted(ledger):       # I-03; deterministic geloggt
        options = propose_joint_changes_in_coupled_countries(z, ledger)
        options = [q for q in options if country_and_connectivity_and_quotas_valid(q)]
        if not options:
            break
        scored = []
        for q in options:
            fit_q = full_europe_calibration(detail, q, f_detail, inputs.calibration_hours)
            scored.append(audit_candidate(q, fit_q))
        z, fit, decision = accept_only_measured_improvement(z, fit, scored)   # I-02
        ledger.append(decision)
        if decision.plateau:
            break

    # Erst nach Stabilisierung: Kapazitätsqualität als weiteres Kriterium.
    n1 = physical_n1_lodf_reference(detail, f_detail, inputs.contingencies)
    capacities = fit_four_equivalent_limits(z, f_detail, n1, inputs.seasons) # I-04
    capacities = apply_published_995_1_130_percent_rules(capacities)
    output = export_reduced_network_and_market_allocation(z, fit, capacities, inputs)
    final_independent_validation(output, inputs)
    return output
~~~

Dies ist eine **implementierbare Prozessrekonstruktion**, nicht der proprietäre ENTSO-E-Quellcode. Für einen produktiven Lauf müssen alle **B**-Eingänge und die mit **I** gekennzeichneten Entscheidungen tatsächlich materialisiert und getestet werden.

## 5. Tatsächlicher Code-Gap-Audit am gepinnten Repository

| Ist-Modul | Vorhandene Funktion | Konkretes Delta für offizielle Referenzimplementation |
|:--|:--|:--|
| `dc.py` | Physikalisch konsistente DC-PTDF und Bilanz im **einzigen verbundenen AC-Graphen** | Europa mit AC-Inseln und HVDC-Kopplungen, Trafo/PST/HVDC-Operation, realen Lastflussreferenzen; keine per-country Slack-Inseln |
| `screening.py` | A-Überlastungsenergie aus vollständiger bilanzierten Einspeisung | 225-/400-kV-Filter, verschiedene Jahres-/Zeitfenster, saisonale Grenzwerte, echte Marktszenario-Provenienz |
| `clustering.py` | Deterministische Greedy-Kantenkontraktion, optionales `regions`, `locked_edges`, Konnektivitätsprüfung | `regions` **verbindlich**, **exakte Zonenquote je Land**, gekoppelte europaweite Move-Suche mit Kalibrierung/RMSE-Schleife |
| `aggregation.py` | \(P,\Gamma,A_z\) und \(A_z\Gamma=P A_d\) als prüfbare Identität | Vollständige AC-/HVDC-/PST-Topologie und Sonderfallbehandlung in der Projektion |
| `equivalent.py` | \(x>0\), Fit von konstantem \(c^0\), Eichung am ersten Ersatzlink | Mehrere AC-Inseln, explizite Stichprobe/Quelle, Solver-/Identifizierbarkeitsdiagnostik, **Einbindung** \(c^0\) in affine Netzgleichungen, gekoppelte Re-Clustering-Iteration |
| `security.py` | LODF und empirische Sommer-/Winter-, Richtungsfits | Offizielle 99,5/1/130-%-Sonderfälle; dokumentierte CNEC-Ausnahmen; bekannte historische Regressions-Defaults als **I**, nicht D; kein stilles Übergehen ungültiger Ausfälle |
| `security_projection.py` | Forschungsbenchmark für CNEC, LODF, Woodbury, bilaterale Grenzen | **nicht** anstelle des beschriebenen IoSN-Punktwolkenverfahrens als „Original“ verwenden |
| `pypsa_adapter.py` | Eingeschränkter PyPSA-Adapter für Leitung-only, ohne Links/Transformatoren/Speicher/PST | Aktuelle Realnetz-E2E-**Blockade**: korrekte Terminal-Injektionen, mehrere AC-Komponenten und aktive Geräte integrieren |
| `distribution.py` / Dokumentation Band II | Forschungsreferenzen zur zonalen Verteilung | Assetbezogene PEMMDB-/PECD-/TSO-Schlüssel und Bilanz-/Kapazitätserhaltung nach § 3.8.4 nachweisen |

**Einordnung:** Bestehende synthetische mathematische Tests sind kein Nachweis einer offiziellen europaweiten IoSN-Reproduktion. Dieser Audit hat **keine** reale PyPSA-/ENTSO-E-End-to-End-Ausführung durchgeführt und keine neue numerische Genauigkeit behauptet.

## 6. Eng begrenztes Entscheidungsregister

### A. Offiziell festgelegt — **keine** Nutzerentscheidung nötig
- **F-01:** europäische physikalische Referenz und gekoppelte internationale Re-Clustering-Bewertung;
- **F-02:** keine länderübergreifenden Cluster; Tabelle 3 mit insgesamt 102 Zonen;
- **F-03:** Engpassranking als jährliche Überlastungsenergie auf 225-/400-kV-Leitungen;
- **F-04:** kritische/sensitive interzonale Leitungen, flusssynchrones Zusammenfassen, verbundenes Zonennetz;
- **F-05:** iterative *RMSE zuerst, Kapazitätsqualität danach*-Bewertung;
- **F-06:** gemeinsame Ersatzimpedanz-/Strukturflussoptimierung mit KCL/KVL;
- **F-07:** HVDC null/PST neutral **im bezeichneten Kalibrierungskontext**;
- **F-08:** LODF-N-1, 4 saisonale/richtungsbezogene Ersatzkapazitäten und Sonderfälle 99,5/1/130 %;
- **F-09:** Ausgabe von No-Load-, Loop-, PST-, HVDC- und Marktzuordnungskomponenten.

### B. Minimale eigene Entscheidungen — **I**, vorerst verbindlich als transparente Implementierungsdefaults
| ID | Entscheidung | Warum exakt nötig | Abnahme bzw. Rückfall |
|:--|:--|:--|:--|
| I-01 | Deterministische länderquoten-konforme Graph-Initialisierung statt eigener elektrischer/RES-Multimetrik | Offizieller Seed-Algorithmus unveröffentlicht | 102, Länderreinheit, Konnektivität, reproduzierbarer Seed, Schutzstatistik |
| I-02 | Auf festen synchronen Stunden RMSE je Link und global über alle Ersatzlinks berechnen; diagnostisch Fehlerquantile und Linkzahl berichten | Exakte Durchschnitts-/relative Normierung nicht veröffentlicht | Ungewichtete MW-RMSE ausdrücklich **eigene** Referenz; Vergleich bei unterschiedlicher Topologie kennzeichnen |
| I-03 | Begrenzte deterministische Single-/Multi-Land-Boundary-Moves, pro Kandidat globaler Neu-Fit; Verbesserung vor Plateau, dann Kapazitätsqualität | ENTSO-E beschreibt Iteration, nicht Move-Generator/Suchbudget/Plateautest | Alle Kandidaten und Entscheidungen auditierbar; keine geografischen Grenzverletzungen |
| I-04 | Nachvollziehbarer parametrischer generischer Punktwolken-Fit mit Statusflags und offiziellen Sonderfallzweigen | ENTSO-E nennt 100-%-Kriterium, aber nicht vollständig das Fit-/Stichprobenverfahren | Niemals „vollständig reproduziertes ENTSO-E-Verfahren“ nennen, ohne zusätzliche Quellen |
| I-05 | Positive \(x\), Eichung/Bounds pro AC-Insel und bilanzneutraler \(c^0\); affine Netzgleichung explizit | Öffentliches Modell gibt keine durchgängige Offset-/KVL-Solver-Spezifikation | Physikalische KCL- und affine-KVL-Tests vor Freigabe |
| I-06 | Keine stille Mittelung der 5 vorgegebenen Jahre; getrennte Jahresnachweise, deterministische Zeitstichprobe für Kalibrierung/Validierung | Szenario- und Stichprobengewichte nicht für diese feste 5-Jahre-Eingabe spezifiziert | Versionierte Stundenindizes und reproduzierbare getrennte Reports |

### C. Tatsächliche Daten-/Implementierungsblocker — **nicht** mit willkürlichen Heuristiken überbrücken
- **B-01 (P0):** europaweiter synchroner Detailnetz-/Market-Dispatch-Datensatz, beiderseitige Knoten-/Leitungszuordnung, vollständige AC-Netzkomponenten, Limits und Zeitstempel.
- **B-02 (P0):** Landestaxonomie „United Kingdom“ vs. „Northern Ireland“ sowie AC-Inseln/HVDC-Brücken und landesspezifische Zonenquoten auf reale Knoten abbilden.
- **B-03 (P0):** offizielle N-1-/CBCO-/Notfallgrenzen und belegbare TSO-Sondermaßnahmen, keine erfundenen Ausfall-Ausschlüsse.
- **B-04 (P1):** PyPSA-Adapter akzeptiert aktuell keine reale Transformator-/HVDC-/PST-/Speicherstruktur.
- **B-05 (P1):** nachgewiesene Integration von \(c^0\) und Maschengleichungen in den tatsächlich verwendeten zonalen Simulator.
- **B-06 (P2):** eindeutige Markt-Anlagen-/TSO-Last-/PECD-Profilzuordnungen für § 3.8.4.
- **B-07 (wissenschaftlich):** einige interne numerische ENTSO-E-Parameter und die proprietäre Suchstrategie sind **öffentlich nicht erhältlich**; dokumentierte Proxy-Verfahren bleiben notwendig.

## 7. Tests und harte Freigabegates

| Gate | Automatischer Nachweis | Freigabe |
|:--|:--|:--|
| G-01 | Zonenbudget CSV: 37 Einträge, Summe 102; jede reale Knotenlandeszuordnung eindeutig | **BLOCK** bei Mismatch |
| G-02 | Kein Cluster mit Knoten verschiedener Länder, Topologie jedes Clusters zusammenhängend | **BLOCK** |
| G-03 | Gleiche vollständige AC-Referenz und Bilanz je AC-Insel in allen Kandidaten; grenzüberschreitende Leitungen physisch erhalten | **BLOCK** |
| G-04 | Überlastungsenergie 225/400 und Jahres-/Stunden-MW/MWh-Einheiten per Referenzbeispiel | **BLOCK** |
| G-05 | \(A_z\Gamma=P A_d\), \(\sum p=0\), \(A_z f_z=p_z\) | **BLOCK** |
| G-06 | Positive identifizierbare \(x\), \(A_zc^0=0\), affine KVL **im verwendeten Marktmodell** | **BLOCK** |
| G-07 | Gleiche Trainings-/Teststunden je Kandidat; RMSE-Ledger je Link, europaweiter Report, dokumentierter Move | **BLOCK** |
| G-08 | LODF-Abgleich gegen ausführbare N-1-Testfälle, Ausfall-/Islanding-Ledger, keine unbelegte Ausnahme | **BLOCK** |
| G-09 | Vier Kapazitätsfelder, 100-%-Schnitt, alle 99,5/1/130-%-Sonderfälle und UNCERTAIN/NO_VALUE-Status | **BLOCK** |
| G-10 | Operationale HVDC-/PST-Wirkung getrennt von neutraler Impedanzkalibrierung nachvollziehbar | **BLOCK** für vollständige IoSN-Abnahme |
| G-11 | Asset-/Lastverteilung nach Zonen erhält Länder-/Technologiesummen und thermische Anzahl/Kapazität | **BLOCK** |
| G-12 | Unabhängige Stunden, Szenarien, Ausfälle; physikalische und Sicherheitsgüte auf Realnetz | **BLOCK** für Realnetzqualifikation |

**Erlaubter unmittelbarer Folgeschritt:** P0/P1-Spezifikation und deterministische Länder-/Graph-Assertions aufbauen; anschließend reale AC-Datenadapter und Implementierung der vollständigen **europaweiten** RMSE-Schleife. **Nicht erlaubt:** eine neue multidimensionale Clustering-Zielfunktion oder RES-/Last-Methode B in die offizielle Referenzimplementierung einschleusen.

## 8. Minimale Implementierungsreihenfolge / Coding-Handoff

1. **P0 — Vertrags- und Topologieprüfung:** Tabelle-3-CSV lesen, Landes-/Insel-Mapping auflösen, Bilanz/Parameter/225-400-Screening-/Szenariomanifest festlegen. Ausgabe: deterministische Preflight-Reports.
2. **P1 — IoSN-konforme initiale Busmap:** bisherige Graphkontraktion nur mit verpflichtender Länderreinheit, Quoten und Konnektivität; gesamteuropäische \(P,\Gamma\)- und Flussreferenz. Ausgang: `busmap_initial` plus Schutz-/Schnittstatistik.
3. **P2 — Ersatznetz-Fit:** globales \(x,c^0\)-Problem, dokumentierte synchrone Referenzstunden, Eichung/Identifizierbarkeit, wirksame affine Maschenmodellierung und unabhängiger RMSE. Ausgang: `reduction_fit`.
4. **P3 — Offizielle Clustering-Feedbacklogik:** Kandidatenänderungen in gekoppelten Ländern, globaler Re-Fit, RMSE-Entscheidungsledger, nach Plateau Qualitätsbeurteilung. Ausgang: `busmap_qualified`.
5. **P4 — N-1-Ersatzkapazitäten:** physische Grenzzweige, LODF, vier Fitgruppen, offizielle Ausnahmeregeln, Statuskennzeichnung und Validierung. Ausgang: `capacity_4way`.
6. **P5 — Komplette Outputs und Zuordnung:** No-Load/PST/HVDC/Loop, § 3.8.4 Asset-Verteilung und LF-/Dispatch-Modusgrenzen. Ausgang: vollständig qualifizierte zonale Netzkopie.

**Durchführungsstand dieser Makroarbeit (26.10.2026):** Primärquellenanalyse + statischer Repository-Abgleich + Entscheidungsmatrix + ausführbare Spezifikation **durchgeführt**. Keine geänderten bestehenden Algorithmen, keine realen Netzsimulationen, keine neu durchgeführten PyPSA-Integrationstests und keine Behauptung einer qualifizierten Gesamtimplementierung.

## 9. Herkunft/prüfbare Dateien

- Offizielle PDF: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf
- Quellenstelle § 3.8.1: PDF S. 23–27; § 3.8.2: S. 27; § 3.8.3–4: S. 28–29; Anhang 6.1: S. 45–51.
- Repo-Originalwissenschaft: [Band I](IOSN_2026_Band_I_Wissenschaftliche_Methodik.md).
- Repo-Implementierungsarchitektur: [Band II](IOSN_2026_Band_II_PyPSA_Implementierung.md).
- Getrennt zu behandeln: vorbestehende A/B-Tutorials, Wetterjahrdokumentation und FBMC-Forschungszweig.
