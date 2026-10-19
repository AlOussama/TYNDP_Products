# Merit-Order-gewichtete PTDF als Grundlage der Netzreduktion

**Stand:** 16. Oktober 2026  
**Status:** analytische Prüfung und synthetische Machbarkeitsstudie; **keine ENTSO-E-/TYNDP-Validierung**.

## Forschungsfrage
Kann die Kombination aus installierter konventioneller Erzeugungsleistung und festen Grenzkosten eine stabile, ökonomisch repräsentative PTDF-Referenz für Ersatzknoten und Ersatzimpedanzen liefern, während RES/Last-Verteilungen gesonderte strukturelle Flusskorrekturen erzeugen?

## Methode
Seien P die Zonen-Knoten-Inzidenz (Z×N), Γ der orientierte Interzonen-Cut-Operator (E×L) und Hd die DC-PTDF des detaillierten Netzes. Für eine Disaggregation R mit PR=I gilt die effektive Zonensensitivität Href=ΓHdR. Die PTDF wird stets nur auf ausgeglichene zonale Injektionen angewendet; die in einem PTDF-Formalismus gewählte Slack-Konvention muss konsistent sein.

Die Referenzvarianten sind (i) gleichmäßige Gewichte innerhalb jeder Zone, (ii) Verteilung nach installierter Leistung, (iii) kostenbasierte Merit Order unter festgelegten Residuallast-Stützstellen und Szenariogewichten. In der dritten Variante werden die Einsatzleistungen pro Stützstelle in aufsteigender Reihenfolge fester Grenzkosten aufgefüllt und danach über die Stützstellen gewichtet. Die Merit-Order-Gewichte bleiben im Ersatznetzmodell fest, obwohl der reale Betrieb variabel sein kann.

Die Ersatzreaktanzen xeq werden im synthetischen Pilot durch min_x ||Heq(x)T − Href T||² bestimmt, wobei T unabhängige ausgeglichene Zoneninjektionen abbildet. Die Flusskorrektur ist f_struct=ΓHd Σk(Rk−Rref)pzk mit *vorzeichenbehafteten* pzk für Wind, Solar und Last. Der Residualfehler beinhaltet die nicht explizit korrigierte konventionelle Injektionsverteilung sowie gegebenenfalls die Impedanzapproximation. Der sogenannte strukturelle Korrekturfluss ist referenzabhängig und nicht ohne Zusatzbedingungen mit dem kalibrierten No-Load-Flow identisch.

## Synthetisches Testsystem
6 Knoten, 3 Zonen zu je 2 Knoten, 9 AC-Leitungen in DC-Näherung und 3 reduzierte Interzonen-Zweige. Konventionelle Kapazitäten [90, 140, 120, 90, 100, 130] MW und **frei erfundene** Grenzkosten [30, 100, 45, 95, 32, 110] €/MWh. Drei Residuallast-Stützstellen (35 %, 60 %, 85 % der konventionellen Kapazität), mit Gewichten (0,30; 0,45; 0,25). 1000 synthetische, bilanziert erzeugte Injektionssituationen, mit merit-order-nahem, aber nicht idealem konventionellem Dispatch und unterschiedlichen RES- und Lastprofilen; fixe Zufallszahl 20261016. Dieselben Szenarien für alle drei Referenzmodelle.

## Ergebnisse

| Referenz | RMSE ohne Strukturkorrektur [MW] | RMSE mit RES-/Last-Korrektur [MW] | Reaktanzen (AB, BC, AC), Modellparameter |
|---|---:|---:|---|
| Gleichmäßig | 0,507 | 0,448 | 0,255; 0,264; 0,379 |
| Kapazität | 0,471 | **0,276** | 0,257; 0,266; 0,378 |
| Merit Order | 0,653 | 0,460 | 0,252; 0,267; 0,386 |

Gemeinsame RMS-Größe der tatsächlichen Interzonenflüsse: 24,683 MW. Alle drei Referenz-PTDFs waren **in diesem speziellen Dreizonen-Dreieck** bis auf Rundungsfehler durch positive Ersatzreaktanzen reproduzierbar. Dies gilt nicht allgemein für reduzierte Netztopologien.

Die Merit-Order-Referenz ist nicht die beste Variante im Pilot. Die Kapazitätsreferenz senkt den korrigierten RMSE gegenüber der Merit Order um etwa 39,9 %. Der Pilot isoliert und belegt damit die **Machbarkeit**, nicht einen generellen Genauigkeitsvorteil ökonomischer Gewichte.

## Wissenschaftliche Schlussfolgerungen
1. Feste Grenzkosten plus installierte Kapazitäten liefern über definierte Residualniveaus eine feste merit-order-gewichtete Disaggregation. Eine feste Merit Order alleine definiert jedoch noch keine eindeutige Einsatzverteilung; Stützstellen und Nachfragegewichtung sind erforderlich.
2. Die Größe Href ist eine Referenz-Sensitivität, nicht zwangsläufig eine realisierbare physikalische PTDF. Ihre physikalische Projektion kann von Topologie, Zonenbildung und Ausgleichsregel abhängen.
3. Für die Wahl eines **real existierenden** Repräsentativknotens pro Zone sollte die Kandidatensensitivität gegen die jeweilige Zielspalte von ΓHdRref auf dem bilanzierten Unterraum verglichen werden; die gekoppelte Eignung aller ausgewählten Knoten und die Ersatzleitungsparametrisierung sind anschließend gemeinsam zu prüfen.
4. Eine PTDF-basierte Knotenwahl ist nicht identisch mit der Wahl der ENTSO-E-TYNDP-Zonengrenzen. Clustering A (Dispatch/Überlastungsenergie) und B (RES/Last) sollten als vorgeschaltete getrennte Varianten bestehen bleiben.
5. Für eine faire Bewertung braucht es *out-of-sample*-Snapshots, mehrere Topologien, vollständige Flussvektoren, Richtung und Grenzwertverletzungen, N-1 und Kalibrierungsaufwand. Die hier berichtete Pilot-Korrektur beruht auf bekannten nodalen RES-/Lastverteilungen und ist daher kein Nachweis, dass ein zonales Produktionsmodell ohne diese Daten dieselbe Genauigkeit erreichen wird.

## Konkreter nächster Projektversuch
Aus dem tatsächlichen ENTSO-E-/PyPSA-Fall: Netz + Netzzonen P und Γ, Anlagenstandorte/Kapazitäten/Grenzkosten, Wind/PV/Last-Standorte und Verfügbarkeiten, Referenzsnapshots. Danach (1) drei fixe Rref, (2) rein elektrischer Repräsentativknoten pro Zone, (3) Kalibrierung mit identischer reduzierter Topologie, (4) feste RES-/Last-Strukturkorrektur bzw. zulässige kalibrierte Offset-Modelle, (5) unabhängige Testflüsse sowie N-1-Qualitätsvergleich. Zusätzliche Szenarien zur Robustheit gegenüber Merit-Order-Misspezifikation.

**Reproduzierbarkeit:** `merit_order_ptdf_pilot.py` erstellt `merit_order_ptdf_results.csv` (Python + NumPy + SciPy).
