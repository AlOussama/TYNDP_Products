---
title: "IoSN 2026 – Auswahl und Gewichtung repräsentativer Wetterjahre"
subtitle: "Konsolidierte wissenschaftliche Methodik mit ergänzender Auswertung der ENTSO-E-Fassungen 2024 und 2022"
date: "19. Oktober 2026"
lang: de-DE
---

# Geltungsbereich und Entscheidung

**Entscheidung.** Die Auswahl repräsentativer Klima-Jahr-Kombinationen erfolgt primär nach der **TYNDP-2026-IoSN-Methodik** und dem ergänzenden offiziellen **TYNDP-2026-Scenarios-Methodology-Report, Anhang III**. Die Dokumentationen **IoSN 2024** und **IoSN 2022** werden ausschließlich für begriffliche Präzisierung, unabhängige Repräsentativitätsdiagnostik und begründete Qualitätsprüfungen herangezogen. Das historische Auswahlverfahren mit kombinatorischer Dreijahressuche und K-Medoids **ersetzt nicht** die aktuelle PCA-/K-Means-Selektion. [Q26-I, §3.7, Anhang 6.3; Q26-S, Kapitel 6, Anhang III; Q24, §8.2; Q22, §6.3]

**Untersuchungsobjekt:** Auswahl von drei *vollständigen*, regional konsistenten Klima-Jahr-Kombinationen aus je 30 Kandidaten sowie die Ableitung und Nutzung ihrer Szenariowahrscheinlichkeiten. **Außerhalb des Geltungsbereichs:** Auswahl von Wochen, repräsentativen Tagen, Stunden, Zeitschritten und zusätzliche temporale Aggregation. Weder die Zahl der Zeitpunkte innerhalb eines ausgewählten Wetterjahres noch die zeitliche Speicherzustandskopplung wird in diesem Dokument geändert.

Die Bezeichnungen und mathematischen Modelle werden nach vier Evidenztypen kenntlich gemacht: **[D26]** ausdrücklich durch eine offizielle 2026er Quelle dokumentiert; **[H24/22]** historisch bei ENTSO-E dokumentiert; **[R]** mathematische Rekonstruktion der dokumentierten Verfahrenslogik; **[E]** vorgeschlagene zusätzliche Validierung oder Implementierungsentscheidung; **[O]** offen, widersprüchlich oder nicht vollständig numerisch festgelegt. Historische Ergänzungen und Rekonstruktionen sind **keine** ENTSO-E-Originalalgorithmen für 2026.

# 1. Quellenhierarchie und Anwendungsregel

| Rang | Offizielle Veröffentlichung | Maßgebliche Inhalte |
|:--|:--|:--|
| 1A | **[Q26-I]** ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, Konsultationsfassung vom 25.02.2026, §3.7, S. 18–21, Anhang 6.3, S. 57–62 | Ziele, Kandidaten, meteorologische Größen, PCA-/K-Means-Prozess, publizierte IoSN-Gewichte |
| 1B | **[Q26-S]** ENTSO-E/ENTSOG, *TYNDP 2026 Scenarios Methodology Report* (Juni 2026), Kapitel 6 und Anhang III | Präzisierungen: 53 Zonen, neun Makroregionen, zwölf Merkmale, getrennte PCA, zehn K-Means-Initialisierungen, Clustergrößen und Gewichtungsregel |
| 2 | **[Q24]** ENTSO-E, *TYNDP 2024 Identification of System Needs – Implementation Guidelines*, §8.2, S. 62–69 | Frühere Bewertung der Übereinstimmung von Jahresmittel und Jahresstreuung; separate Repräsentativitätsdiagnostik mit gewichteter Distanz und K-Medoids |
| 3 | **[Q22]** ENTSO-E, *TYNDP 2022 IoSN Implementation Guidelines*, §6.3, S. 44–49 | Historische Ausgangsmethodik, regionale Residuallastverteilungen, Delta-Indikatoren und Erfordernis regionaler Repräsentativität |

**Konfliktregel:** Stimmen Q26-I und Q26-S in einer konkreten Angabe überein, gilt diese als vorrangige 2026er Rekonstruktion. Präzisiert Q26-S eine in Q26-I offen gelassene Operation, wird die Präzisierung übernommen und mit Quellenangabe gekennzeichnet. Bei verbleibendem Widerspruch wird die Differenz offengelegt und nicht durch Rückgriff auf die ältere Methode verdeckt. Q24/Q22 dienen ausschließlich als zweite Evidenzlinie. Diese Priorisierung ist **unsere Dokumentationsentscheidung [E]**, keine behauptete ENTSO-E-Normenhierarchie.

# 2. Kandidatenmenge und Klimadaten

## 2.1 Studienzieljahr und Klima-Jahr

Für jedes Studienzieljahr $Y$ liegt ein Ensemble projizierter meteorologischer Realisierungen vor. Ein Kandidat $i=(m,y)$ verbindet ein Klimamodell $m$ mit einem Klima-Jahr $y$. [D26]

$$
\mathcal M=\{\mathrm{CMR5},\mathrm{ECE3},\mathrm{MEHR}\},\qquad
\mathcal I_Y=\mathcal M\times\mathcal W_Y,\qquad
|\mathcal I_Y|=3\cdot10=30.
$$

Die Datenbasis ist PECD 4.2 / CMIP6 unter SSP2-4.5. Die Klimamodelle sind CMCC-CM2-SR5 (CMR5), EC-Earth3 (ECE3) und MPI-ESM1-2-HR (MEHR). $Y$ bezeichnet das wirtschaftliche Studienzieljahr; $y$ bezeichnet das meteorologische Jahr innerhalb des Klimamodells. [Q26-I, §3.7; Q26-S, Anhang III]

| Studienzieljahr $Y$ | Zehnjähriges Kandidatenfenster $\mathcal W_Y$ | Verwendung |
|:--|:--|:--|
| 2030 | 2025–2034 | 2026er Szenarienbildung; nicht eines der drei IoSN-Ausbauzieljahre |
| 2035 | 2030–2039 | IoSN-Ausbauoptimierung |
| 2040 | 2035–2044 | IoSN-Ausbauoptimierung |
| 2050 | 2045–2054 | IoSN-Ausbauoptimierung |

**Quellenabgleich [O]:** Q26-I §3.7 und Q26-S Anhang III, Tabelle 34, stimmen für diese Fenster überein. Q26-I Anhang 6.3.1 verschiebt die Fenster dagegen jeweils um ein Jahr (für 2035 beispielsweise 2031–2040). Die hier gewählten Fenster sind somit quellenübergreifend am stärksten gestützt und mit den veröffentlichten Vertreterjahren vereinbar. Der redaktionelle Widerspruch im IoSN-Anhang bleibt dennoch dokumentiert; eine ausdrückliche Erratum-Entscheidung ist daraus nicht ableitbar.

## 2.2 Klimasensitive Eingangsgrößen

Die aktuelle Auswahl beruht auf sechs Merkmalsfamilien: Wind an Land, Wind auf See, Photovoltaik, Laufwasser, Reservoirwasserkraft und kombinierte Heiz-/Kühlgradtage. [D26]

| Gruppe $v$ | Daten und Auflösung | Energiesystembezug |
|:--|:--|:--|
| ON | Onshore-Wind-Kapazitätsfaktoren, stündlich | Erzeugungsverfügbarkeit an Land |
| OF | Offshore-Wind-Kapazitätsfaktoren, stündlich | Erzeugungsverfügbarkeit auf See |
| PV | Photovoltaik-Kapazitätsfaktoren, stündlich | Solare Erzeugungsverfügbarkeit |
| ROR | Laufwasser-Zuflüsse/-Profile, wöchentlich | Wasserkraftverfügbarkeit |
| RES | Reservoir-Zuflüsse/-Profile, wöchentlich | Speicherwasserkraftverfügbarkeit |
| T | Heiz- und Kühlgradtage, täglich | Temperaturabhängige Nachfrage |

Q26-I bezeichnet die hydrologischen Inputs als **Zuflüsse**; Q26-S Anhang III spricht bei der statistischen Aufbereitung teilweise von **Erzeugungsprofilen** bzw. -energie. Die exakte physikalische Ausprägung, Skalierung und Umrechnung ist für eine Reimplementierung zu fixieren **[O]**. Die Primärquelle Q26-S verknüpft Wind-/PV-Kapazitätsfaktoren mit den zieljahrspezifischen installierten Leistungen aus PEMMDB; HDD/CDD beruhen auf Temperaturgrenzwerten und Nachfragedaten. Die originalen Zeitreihen werden ausschließlich zur Ableitung von **Jahresmerkmalen** genutzt; ihre Stunden bzw. Wochen werden hier nicht ausgewählt oder reduziert.

## 2.3 Räumliche Zuordnung

Q26-S Anhang III dokumentiert **53 Bidding Zones**, die zu **neun europäischen Makroregionen** aggregiert werden: Baltic, CE, CW1, CW2, Nordic, SC, SE, SW und UK. Die historische IoSN-Methode von 2022/2024 betont ebenfalls, dass eine rein gesamteuropäische Zusammenfassung die räumliche Variabilität statistisch glätten würde. [D26; H24/22]

Die Methode verwendet pro Klima-Jahr $i$, Variable $v$, Zone $z$ und Zeitpunkt $t$ eine realitätskonsistente Zeitreihe $x_{v,z,i}(t)$. Eine rekonstruktive Makroregionsbildung ist [R]

$$
x_{v,r,i}(t)=\sum_{z\in\mathcal Z_r}x_{v,z,i}(t),
$$

wobei die tatsächliche Datenumwandlung von der Einheit abhängt: Kapazitätsfaktoren können nicht ohne Kapazitätsskalierung sinnvoll wie erzeugte MW summiert werden. **[D26]** Für Wind/PV wird zunächst eine anlagenkapazitätsbasierte Umrechnung vorgenommen; **[O]** die vollständigen zonalen Referenzkapazitäten und Variablenkonventionen müssen als Eingabe archiviert werden.

# 3. Primärer 2026-Auswahlalgorithmus

## 3.1 Stufe A: Jahresstatistik je Kandidat, Technologie und Makroregion

Seien $N=30$ Kandidaten und $T_{v,i}$ die Zahl der Beobachtungen in einem Wetterjahr für Technologie $v$. **[D26/R]** Der jährliche Mittelwert lautet

$$
\mu_{v,r,i}=\frac{1}{T_{v,i}}\sum_{t=1}^{T_{v,i}}x_{v,r,i}(t),\qquad
\bar\mu_{v,r}=\frac{1}{N}\sum_{i=1}^N\mu_{v,r,i}.
$$

Daraus folgt der Mittelwert-Anomalieindikator

$$
\delta^{\mu}_{v,r,i}=\mu_{v,r,i}-\bar\mu_{v,r}.
$$

Für eine zweite Merkmalsfamilie verwendet Q26-S Anhang III die Bezeichnung *variability-anomaly* und zielt auf die **innerjährliche Streuung**; Q26-I Anhang 6.3 nennt neben jährlichen Standardabweichungen eine kumulative Anomalie gegenüber einem Multimodell-Mittel. Die Quellen liefern jedoch **keine widerspruchsfreie, eindeutig ausführbare Formel** für diese zweite Merkmalsfamilie. Q26-I stellt eine Standardabweichung der Jahresmittel einer Jahresstandardabweichung gegenüber. Q26-S beschreibt den Variabilitätsindikator sprachlich mit kumulativen Anomalien und der Streuung von Szenario-Standardabweichungen. **[O: wissenschaftlich kritischer Definitionsbedarf]**

Eine mögliche, mit dem Zweck des Indikators vereinbare Rekonstruktion — **nicht als ENTSO-E-Formel auszugeben [R]** — ist

$$
\sigma_{v,r,i}=\operatorname{std}_{t}\bigl(x_{v,r,i}(t)\bigr),\qquad
\delta^{\sigma}_{v,r,i}=\sigma_{v,r,i}-\frac{1}{N}\sum_{j=1}^N\sigma_{v,r,j}.
$$

Diese Formel beschreibt die Abweichung der intraannuellen Streuung eines Kandidaten von der mittleren intraannuellen Streuung. Vor einer produktiven Reimplementierung ist die genaue ENTSO-E-Definition oder eine begründete eigene Festlegung erforderlich.

**Prüfung der kumulativen Anomalie [R]:** Falls $CA_{v,r,i}=\sum_t[x_{v,r,i}(t)-\bar x_{v,r}(t)]$ mit einheitlichem Zeitraster gebildet wird, dann gilt $CA_{v,r,i}=T(\mu_{v,r,i}-\overline{\bar x}_{v,r})$. Als einzelne Jahressumme liefert sie dann keine eigenständige Information über die zeitliche Reihenfolge; die im neuen Anhang genannte Variabilitätsrolle lässt sich damit nicht allein begründen. Diese Beobachtung ist keine Aussage über einen nicht veröffentlichten Softwarealgorithmus.

## 3.2 Stufe B: Technologiebasierte räumliche Gewichtung

**[D26, Q26-S Anhang III]** Die Regionsgewichte hängen vom betrachteten Merkmal ab. Für Wind, PV und Wasserkraft wird der Anteil der regional installierten Leistung der betreffenden Technologie verwendet; für HDD/CDD der Anteil der regionalen Stromnachfrage. Die Gewichte sind zieljahrspezifisch.

$$
\beta_{v,r,Y}=\begin{cases}
\displaystyle \frac{K_{v,r,Y}}{\sum_{r'\in\mathcal R}K_{v,r',Y}}, & v\in\{\mathrm{ON,OF,PV,ROR,RES}\},\\[6pt]
\displaystyle \frac{L_{r,Y}}{\sum_{r'\in\mathcal R}L_{r',Y}}, & v=\mathrm{T},
\end{cases}
\qquad \sum_r\beta_{v,r,Y}=1.
$$

$K$ ist die je Technologie maßgebliche installierte Leistung; $L$ ist die verwendete Nachfragereferenz. **[O]** Die konkreten Anlagen-/Zonenwerte, die besondere Behandlung sehr kleiner oder nullwertiger Kapazitäten sowie einheitliche historische/monatliche Lastnormalisierungen sind nicht als vollständige maschinenlesbare Eingangsmatrix in Q26-I vorgegeben.

**Wesentliche Präzisierung aus Q26-S [D26]:** Die gewichteten regionalen Delta-Indikatoren werden **zunächst zu genau einem Szenariowert je Merkmalsfamilie aggregiert**. Formal [R]:

$$
D^{\mu}_{v,i}=\sum_{r\in\mathcal R}\beta_{v,r,Y}\delta^{\mu}_{v,r,i},\qquad
D^{\sigma}_{v,i}=\sum_{r\in\mathcal R}\beta_{v,r,Y}\delta^{\sigma}_{v,r,i}.
$$

Erst **nach dieser räumlichen Aggregation** wird standardisiert. Damit wird verhindert, dass feste Regionalgewichte bei einer vorherigen spaltenweisen Z-Transformation automatisch verschwinden. Bei positivem konstantem $\beta$ würde für eine einzelne regionale Spalte $\operatorname{zscore}_i(\beta\delta_i)=\operatorname{zscore}_i(\delta_i)$ gelten. Für $\operatorname{zscore}_i(\sum_r\beta_r\delta_{r,i})$ gilt diese Aufhebung im Allgemeinen nicht. Diese Reihenfolge ist deshalb eine **methodisch substantielle Klärung** gegenüber der knappen IoSN-Beschreibung.

## 3.3 Stufe C: Normalisierung

**[D26]** Für jede der sechs Merkmalsfamilien werden die beiden aggregierten Delta-Indikatorvektoren über alle 30 Kandidaten standardisiert:

$$
A_{i,v}=\frac{D^{\mu}_{v,i}-\overline D^{\mu}_{v}}{s^{\mu}_v},\qquad
S_{i,v}=\frac{D^{\sigma}_{v,i}-\overline D^{\sigma}_{v}}{s^{\sigma}_v},
$$

mit $\overline D^{\mu}_v=N^{-1}\sum_iD^{\mu}_{v,i}$ und $s^{\mu}_v=\operatorname{std}_{i}(D^{\mu}_{v,i})$ sowie analogen Größen für $\sigma$.

Damit entstehen **zwei standardisierte Matrizen**

$$
A\in\mathbb R^{30\times6},\qquad S\in\mathbb R^{30\times6}.
$$

Q26-I Anhang 6.3.2 nennt irrtümlich eine Minimum-Subtraktion; Q26-I Anhang 6.3.3 und Q26-S Anhang III nennen ausdrücklich die Subtraktion des Mittelwerts und die Division durch die Standardabweichung. Die hier dargestellte Z-Standardisierung ist damit durch **zwei 2026er Originalstellen** gestützt. [O] Nicht explizit geregelt bleiben die Wahl zwischen Populations- und Stichproben-Standardabweichung und der Umgang mit Spalten ohne Varianz.

## 3.4 Stufe D: Zwei getrennte Hauptkomponentenanalysen

**[D26, Q26-S Anhang III]** Die 12 Indikatoren werden **nicht** durch eine einzige zwölfdimensionale PCA reduziert. Stattdessen erfolgt je eine separate PCA der sechs Mittelwert- und sechs Variabilitätsindikatoren. Von beiden wird **nur die erste Hauptkomponente (PC1)** übernommen.

Eine entsprechende mathematische Rekonstruktion ist

$$
\begin{aligned}
C_A&=\frac{1}{N-1}A^\top A,& u_A&=\operatorname{eigvec}_{\max}(C_A),\\
C_S&=\frac{1}{N-1}S^\top S,& u_S&=\operatorname{eigvec}_{\max}(C_S),\\
p_i&=\begin{bmatrix}(Au_A)_i\\(Su_S)_i\end{bmatrix}\in\mathbb R^2.
\end{aligned}
$$

Die PCA-Scores $p_i$ bilden das zweidimensionale Merkmalssystem, in dem anschließend drei meteorologische Regime geclustert werden. Die willkürliche Vorzeichenkonvention einer Hauptkomponente ändert euklidische Distanzen nicht, muss für gespeicherte Komponenten aber reproduzierbar behandelt werden. **[O]** Numerische Ladungen, erklärter Varianzanteil, PCA-Referenzimplementierung und die tatsächlichen Eingabematrizen werden nicht vollständig als ausführbare Konfiguration veröffentlicht.

## 3.5 Stufe E: K-Means-Selektion mit $k=3$

**[D26]** Die 30 Punkte $p_i\in\mathbb R^2$ werden in drei nichtleere Cluster partitioniert. Die K-Means-Zielfunktion lautet [R]

$$
\boxed{
\min_{\{\mathcal C_k,c_k\}_{k=1}^3}
\sum_{k=1}^{3}\sum_{i\in\mathcal C_k}\|p_i-c_k\|_2^2,
\quad c_k=\frac{1}{|\mathcal C_k|}\sum_{i\in\mathcal C_k}p_i.}
$$

Q26-S Anhang III präzisiert **zehn zufällige Initialisierungen**; die Clusterlösung mit der kleinsten gesamten Intra-Cluster-Streuung wird gewählt. Ein fester Zufalls-Seed wird für Reproduzierbarkeit verwendet, der **numerische Seed ist jedoch nicht angegeben [O]**.

Pro Cluster wird ein **existierendes** Klima-Jahr, kein synthetischer Zentroid, als Vertreter gewählt:

$$
\boxed{i_k^\star=\arg\min_{i\in\mathcal C_k}\|p_i-c_k\|_2.}
$$

Die Einschränkung auf das eigene Cluster folgt ausdrücklich aus der Vertreterbeschreibung von Q26-S Anhang III. Q26-I Anhang 6.3.3 verwendet an einer Stelle eine weiter gefasste Formulierung (Abstände zu allen Reihen). Bei gleich großen Abständen und mehrfach auswählbaren Indizes wäre eine nachvollziehbare Tie-Break-Regel erforderlich [O].

## 3.6 Stufe F: Wahrscheinlichkeit aus Clustergrößen

**[D26]** Die Wahrscheinlichkeiten werden **nicht** aus den regionalen Gewichtungsfaktoren, PCA-Eigenwerten, K-Means-Distanzen oder historischen K-Medoids-Scores berechnet. Der aktuelle Scenarios-Methodology-Report dokumentiert direkt:

$$
\boxed{\pi_{Y,k}=\frac{n_{Y,k}}{N},\quad n_{Y,k}=|\mathcal C_{Y,k}|,\quad N=30,\quad\sum_{k=1}^{3}\pi_{Y,k}=1.}
$$

Das ist die **empirische Häufigkeit** eines meteorologischen Regimes im jeweils gleichgewichtet betrachteten Pool von 30 Klima-Jahr-Kandidaten. Der Anhang bezeichnet die dahinterstehende Interpretation als nichtparametrische Schätzung unter einer Ergodizitätsannahme. Diese Werte sind kein Schweregradindex und keine separat geschätzten Ausfallwahrscheinlichkeiten. Insbesondere werden drei Projektionsmodelle und zehn Klima-Jahre innerhalb des Fensters als gleich große Eingangseinheiten gezählt, ohne dass damit eine unabhängige physikalische Eintrittswahrscheinlichkeit jeder Klimamodellfamilie bewiesen wäre.

### 3.6.1 Offizielle IoSN-Ergebnisse für 2035, 2040 und 2050

| Zieljahr | WS-ID | Modell / Klima-Jahr | Cluster $n_k$ | Exakt $n_k/30$ | Gewicht (Q26-I) |
|:--|:--|:--|--:|--:|--:|
| 2035 | WS032 | CMR5 / 2031 | 7 | 0,2333 | 0,24 |
| 2035 | WS037 | CMR5 / 2036 | 13 | 0,4333 | 0,43 |
| 2035 | WS059 | MEHR / 2038 | 10 | 0,3333 | 0,33 |
| 2040 | WS065 | CMR5 / 2039 | 6 | 0,2000 | 0,20 |
| 2040 | WS071 | ECE3 / 2035 | 12 | 0,4000 | 0,40 |
| 2040 | WS077 | ECE3 / 2041 | 12 | 0,4000 | 0,40 |
| 2050 | WS091 | CMR5 / 2045 | 7 | 0,2333 | 0,23 |
| 2050 | WS092 | CMR5 / 2046 | 17 | 0,5667 | 0,57 |
| 2050 | WS106 | ECE3 / 2050 | 6 | 0,2000 | 0,20 |

Quellen: Szenariokennungen und veröffentlichte Gewichte aus Q26-I §3.7; Clustergrößen aus Q26-S Anhang III, Tabelle 36.

**[O] Präziser Rundungshinweis:** Für 2035 entspricht die offizielle Kombination $n_{WS032}=7$ und $N=30$ exakt $0{,}2333\ldots$ und würde bei unabhängiger konventioneller Rundung auf zwei Nachkommastellen $0{,}23$ ergeben, **nicht $0{,}24$**. Die drei unabhängig gerundeten Werte wären $0{,}23+0{,}43+0{,}33=0{,}99$. Die publizierte Kombination $0{,}24+0{,}43+0{,}33=1{,}00$ kann durch einen möglichen Rundungsausgleich erklärt werden; eine solche Regel wird jedoch nicht explizit dokumentiert. Für wissenschaftliche Nachrechnungen sind die **exakten Brüche $n_k/30$** eindeutig; für eine exakte Nachbildung veröffentlichter Modellläufe muss gesondert dokumentiert werden, ob die intern eingesetzten Szenariogewichte gerundet waren. Beides darf nicht unbemerkt vermischt werden.

Für 2030 liefert Q26-S Anhang III ergänzend WS029 (9/30, 0,30), WS003 (19/30, 0,63) und WS021 (2/30, 0,07). Diese 2030er Werte dienen der Szenarienbildung, nicht als zusätzliches IoSN-Ausbauzieljahr in Q26-I.

## 3.7 Weiterverwendung der Gewichte

**[D26]** Die IoSN-Ausbauoptimierung verwendet die Gewichte als Szenariowahrscheinlichkeiten. Eine abstrakte Erwartungswertdarstellung ist [R]

$$
\min_{x\in X}\left\{ C^{\mathrm{inv}}(x)+\sum_{k=1}^{3}\pi_{Y,k}Q_Y(x,i_k^\star)\right\},
$$

wobei $x$ szenarioübergreifende Investitionsentscheidungen und $Q_Y$ die wetterabhängigen optimalen Betriebskosten für festes $x$ bezeichnet. Die Formel verdeutlicht nur die Rolle der Jahresgewichte: Die drei Wetterjahre teilen dieselbe Ausbauentscheidung, Betriebsentscheidungen können sich unterscheiden. Diese Wahrscheinlichkeit darf **nicht** mit dem regionalen Merkmalsgewicht $\beta_{v,r,Y}$ verwechselt werden.

# 4. Zulässige Ergänzungen aus IoSN 2024 und IoSN 2022

## 4.1 Historischer Kern: Repräsentativität der Gesamtheit prüfen

**[H24/22]** Die älteren IoSN-Leitfäden bilden stündliche regionale Residuallastdaten und bewerten dreijährige Kandidatenkombinationen gegenüber dem 30-Jahres-Ensemble anhand der **Abweichungen von Mittelwert und Standardabweichung**. Die insgesamt $\binom{30}{3}=4060$ möglichen Dreierkombinationen werden anhand einer gewichteten Distanz bewertet. Die besten Kandidaten werden anschließend mittels K-Medoids auf eine gute Abdeckung des gesamten Klima-Jahresraums geprüft. Das Verfahren wird in Q24 §8.2 und Q22 §6.3 als eigenständiges historisches Auswahlverfahren beschrieben.

Eine historische schematische Formel lautet [H24/22]

$$
E_g=\sqrt{\sum_{r\in\mathcal R}w_r^{\mathrm{hist}}
\bigl(I_{\mu,r,g}^2+I_{\sigma,r,g}^2\bigr)},\quad
w_r^{\mathrm{hist}}=\frac{\overline{L}_r}{\sum_{r'}\overline{L}_{r'}}.
$$

Dabei sind $I_{\mu,r,g}$ und $I_{\sigma,r,g}$ normierte Differenzen der drei Jahre zur 30-Jahre-Referenz. In dieser alten Methode werden die Regionsgewichte **nach** der Indikatorstandardisierung innerhalb der Distanzfunktion angewendet. Die dokumentierte kombinatorische Zahl 4060 ist mathematisch korrekt; beide älteren Texte nennen an anderer Stelle irrtümlich 4600. Diese historische Formel wird **nicht** zum neuen 2026er Primärscore erklärt.

**Zulässiger methodischer Transfer [E]:** Die 2026 ausgewählten drei Wetterjahre zusätzlich auf die Erhaltung von Mittelwert, Streuung und räumlicher Diversität testen, ohne die drei K-Means-Vertreter bei der Primärauswahl zu verändern. Die Prüfgrößen dürfen bei Bedarf sowohl für die meteorologischen Merkmale als auch für eine eigens aus 2026-Nachfrage-/Erzeugungsdaten abgeleitete Residuallast berechnet werden. Letzteres setzt explizit kompatible Daten voraus und gehört dann zur **Validierung**, nicht zur ursprünglichen Merkmalsdefinition.

## 4.2 Gewichtete Momentenprüfung für den 2026er Dreiersatz

Seien $\mu_{v,r,i}$ und $\sigma_{v,r,i}$ Mittelwert und innerjährliche Standardabweichung jedes der 30 Kandidaten. Die vollständige Referenz und das reduzierte Ensemble können [E/R] verglichen werden:

$$
\mu_{v,r}^{\mathrm{full}}=\frac{1}{30}\sum_{i=1}^{30}\mu_{v,r,i},\qquad
\widehat\mu_{v,r}=\sum_{k=1}^{3}\pi_{Y,k}\mu_{v,r,i_k^\star}.
$$

Die korrekte Gesamtvarianz einer Mischung aus Jahresverteilungen enthält **sowohl** die mittlere innere Varianz **als auch** die Varianz der Jahresmittel (Satz der totalen Varianz). Für gleichartige vollständige Jahresreihen ergibt sich [R]

$$
\begin{aligned}
V_{v,r}^{\mathrm{full}}&=\frac{1}{30}\sum_{i=1}^{30}
\left[\sigma_{v,r,i}^2+(\mu_{v,r,i}-\mu_{v,r}^{\mathrm{full}})^2\right],\\
\widehat V_{v,r}&=\sum_{k=1}^{3}\pi_{Y,k}
\left[\sigma_{v,r,i_k^\star}^2+(\mu_{v,r,i_k^\star}-\widehat\mu_{v,r})^2\right].
\end{aligned}
$$

Die Formeln setzen eine einheitliche **Populationsvarianzkonvention** pro Jahr voraus; bei Stichprobenvarianzen, unterschiedlich langen Jahren oder verschieden langen Datengittern sind Korrekturen notwendig. Die einfache gewichtete Summe von Jahresstandardabweichungen wäre **nicht** dieselbe Größe wie die Standardabweichung des zusammengemischten Wetterensembles.

Ein zulässiger, ausdrücklich **zusätzlicher** Qualitätsnachweis besteht darin, die normierten Differenzen $|\widehat\mu-\mu^{\mathrm{full}}|$ und $|\sqrt{\widehat V}-\sqrt{V^{\mathrm{full}}}|$ pro Technologie und Makroregion zu protokollieren. Schwellenwerte dafür sind in Q26-I/Q26-S **nicht normativ festgelegt**.

## 4.3 Repräsentation des Szenarienraums als zweite Diagnose

**[H24/22]** Die älteren Methoden begründen die K-Medoids-Stufe damit, dass eine Dreijahreskombination zwar statistisch im Mittel richtig liegen, den Variationsraum aber dennoch schlecht abdecken kann. Dieser Gedanke ist für 2026 als Qualitätsprüfung nutzbar.

Für die primär ermittelten Vertreter $p_{i_k^\star}$ kann ergänzend [E] die Distanz

$$
J_{\mathrm{repr}}=\sum_{i=1}^{30}\min_{k=1,2,3}\|p_i-p_{i_k^\star}\|_2^2
$$

berechnet und mit alternativen Dreijahreskombinationen **nur diagnostisch** verglichen werden. Diese Distanz ist **nicht identisch** mit dem primären K-Means-Zielwert, weil dort die Zentroiden $c_k$ statt der ausgewählten realen Jahre verwendet werden. Eine solche Diagnose lässt den Primäralgorithmus unverändert und kann helfen, die Auswahl und Clusterabdeckung zu auditieren.

## 4.4 Nicht übertragbare Elemente

**Nicht** übernommen werden: (a) die historische Residuallast als Ersatz für die sechs 2026er Merkmalsfamilien; (b) der alte kombinatorische 4060-Kandidaten-Filter als verbindlicher 2026er Zwischenschritt; (c) K-Medoids als Ersatz für das 2026er K-Means; (d) die historischen reinen Lastanteile als gemeinsame Regionsgewichte für alle Technologien; (e) historische tatsächliche Wetterjahr-IDs und deren Wahrscheinlichkeiten als 2026er Kandidaten; (f) jede Art von Wochen- oder Stundenwahl. Der Grund ist nicht fehlende wissenschaftliche Plausibilität, sondern die klare Primärquellenbindung an den methodisch geänderten 2026er Ablauf.

# 5. Spezifikationslücken und Konfliktregister

| ID | Status und Priorität | Betreff | Dokumentationsentscheidung bzw. fehlende Information |
|:--|:--|:--|:--|
| W01 | [D26/O], hoch | Kandidatenfenster | Q26-I §3.7 und Q26-S Tabelle 34 stützen 2030: 2025–34; 2035: 2030–39; 2040: 2035–44; 2050: 2045–54. Q26-I Anhang 6.3.1 weicht um +1 Jahr ab. Dokumentierte Präferenz, keine behauptete offizielle Erratum. |
| W02 | [O], kritisch | Variabilitätsindikator | Die exakte Formel zwischen jährlicher Standardabweichung, kumulativer Anomalie und Vergleichsreferenz ist nicht konsistent ausgeschrieben. Umsetzung benötigt Fachentscheidung bzw. Bestätigung. |
| W03 | [D26/O], mittel | Normierung | Mittelwertsubtraktion wird durch Q26-I Detailformel und Q26-S gestützt; IoSN-Überblick nennt dagegen „Minimum“. Umgang mit Nullvarianz und genaue std-Konvention fehlen. |
| W04 | [D26], geklärt | Regionale Gewichtungsreihenfolge | Q26-S beschreibt: nach Technologie gewichtete regionale Deltas zusammenfassen, erst dann Technologie-Spalten z-standardisieren. Damit ist die frühere Gefahr einer vollständigen Gewichtsaufhebung eingegrenzt. |
| W05 | [O], hoch | Anlagen-/Lastgewichte | Vollständige versionierte Werte von $K_{v,r,Y}$ und $L_{r,Y}$, Abgrenzung bei Wasser und Datenstand müssen gespeichert werden. |
| W06 | [D26/O], mittel | Räumlicher Scope | Neun Makroregionen und 53 Zonen sind angegeben; die exakte interne mapping-/Technologieaggregation und Inputdatei-Versionen müssen für Reproduktion archiviert werden. |
| W07 | [D26], geklärt | PCA-Struktur | Zwei getrennte PCAs über 30×6 Mittelwert- und 30×6 Variabilitätsindizes; jeweils PC1; damit 30×2 Clusterpunkte. |
| W08 | [O], mittel | PCA-Werte | Tatsächliche Komponenten, Varianzanteile und die 30×12 Matrix sind nicht als komplette numerische Benchmarktabelle dokumentiert. |
| W09 | [D26/O], mittel | K-Means | $k=3$, zehn zufällige Starts und ein fester Seed dokumentiert; konkreter Seed, Softwareversion, Abbruch- und Gleichstandsregeln nicht vollständig veröffentlicht. |
| W10 | [D26], geklärt | Empirische Szenariogewichtung | $\pi_k=n_k/30$, Clustergrößen je Zieljahr in Q26-S Tabelle 36; nicht aus der älteren K-Medoids-Methode zu übernehmen. |
| W11 | [O], hoch | Rundung 2035 | $7/30=0{,}2333\ldots$, gedruckt WS032 mit 0,24; fehlende Regel der Gewichtsquantisierung und Anwendung exakter oder gedruckter Gewichte in Optimierung. |
| W12 | [O], mittel | Hydrologische Features | Q26-I bezeichnet wöchentliche Zuflüsse; Q26-S beschreibt teilweise generation-/energiebasierte Hydroprofile. Exakte Variable und Skalierung müssen eindeutig fixiert werden. |
| W13 | [D26/E], mittel | Daten-/Wahrscheinlichkeitsinterpretation | Empirische Clusterhäufigkeiten setzen den Pool aus drei Modellen × zehn Klima-Jahren als gleichgewichtige Kandidatenbasis voraus; sie sind keine explizit kalibrierten Klimamodellwahrscheinlichkeiten. |
| W14 | [E], offen | Repräsentativitätsgüte | Optionale 2024/2022-inspirierte Momenten- und Abdeckungsdiagnose. Keine offiziell festgelegten 2026er Akzeptanzschwellen. |

# 6. Konkrete Spezifikation für eine Reimplementation

**Primärpipeline [D26/R]:**

1. Je Zieljahr $Y$ die 30 Kombinationen aus PECD-4.2-Klimamodell und dem zehnjährigen Fenster laden und mit einem unveränderlichen Szenarioindex versehen.
2. Die sechs Merkmalsfamilien mit den vom aktuellen 2026er Szenariobericht beschriebenen Kapazitäts-/Nachfragebezügen auf neun Makroregionen zusammenführen.
3. Je Szenario/Merkmal/Makroregion die zwei Jahreskennzahlen ermitteln; den bislang nicht eindeutigen Variabilitätsindikator als **explizite offene Spezifikation** behandeln und jede gewählte mathematische Variante deklarieren.
4. Je Technologie die Makroregionsgewichte bestimmen und die regionalen Deltas auf genau einen Mittelwert- und einen Variabilitätswert aggregieren.
5. Über die 30 Kandidaten merkmalsweise z-standardisieren und die Matrizen $A,S\in\mathbb R^{30\times6}$ bilden.
6. $\operatorname{PCA}(A)$ und $\operatorname{PCA}(S)$ getrennt berechnen; je eine PC1 übernehmen; $P\in\mathbb R^{30\times2}$ erzeugen.
7. K-Means mit $k=3$ und zehn zufälligen Initialisierungen ausführen; bestes Inertia-Ergebnis auswählen; Seed und Softwareumgebung protokollieren.
8. Je Cluster das reale, dem Zentrum nächstgelegene Wetterjahr wählen; Clustergröße $n_k$ bestimmen und $\pi_k=n_k/30$ berechnen.
9. Reproduzierbare Outputtabelle mit Zieljahr, Klima-Modell, Klima-Jahr, WS-ID, Cluster-ID, Clustergröße, exaktem Gewicht, publiziertem Vergleichsgewicht, PCA-Scores und Quellenstand ausgeben.

**Sekundäre, strikt nichtselektierende Prüfungen [E; historisch motiviert durch H24/22]:**

- Übereinstimmung der mit $\pi_k$ gewichteten Jahresmittel und Gesamtvarianzen mit dem ursprünglichen Ensemble untersuchen.
- Verteilung der realen Vertreter im PCA-Raum und ihre Abdeckungsdistanzen zum Ensemble prüfen.
- Bei verfügbaren, zum Studienzieljahr konsistenten Leistungsdaten ergänzend die **regionale Residuallaststatistik** prüfen, jedoch nicht als Primärmerkmal oder Ersatz für K-Means einführen.
- Die 2026er veröffentlichten WS-Kennungen und die exakten Clustergrößen vergleichen; Abweichungen als Validierungsbefund und nicht als stillschweigende Eingabekorrektur dokumentieren.

**Minimal erforderliche Qualitätsinvarianten:** $|\mathcal I_Y|=30$; $|\mathcal C_k|\ge1$; $\sum_kn_k=30$; drei verschiedene Repräsentanten $i_k^\star\in\mathcal C_k$; $\pi_k\ge0$; $\sum_k\pi_k=1$; beiden PCA-Matrizen 30×6; gemeinsamer räumlicher Inputstand aller Kandidaten; identischer Zeitraum je Zieljahr und Klimamodell. Für die exakte Vergleichbarkeit müssen ferner Input-Provenienz, normalisierte Merkmalsmatrix, regionale Gewichte und Zufalls-/Softwareparameter versioniert gespeichert werden.

# 7. Ergebnis und Einordnung

**Die Integration ist möglich und fachlich sinnvoll, aber mit klaren Rollen:** Die aktuelle 2026er Methode definiert den Auswahlalgorithmus und die empirische Szenariowahrscheinlichkeit. Sie wird durch den später veröffentlichten 2026er Scenarios-Methodology-Report entscheidend konkretisiert: neun Makroregionen, zwölf aggregierte Kennzahlen, zwei getrennte PC1-Projektionen, zehn K-Means-Neustarts sowie die Clustergrößen $n_k$ und Gewichte $n_k/30$. Die älteren IoSN-Versionen liefern **kein fehlendes Glied für die Gewichtungsformel**, weil dieses bereits offiziell in 2026 spezifiziert ist. Ihr wissenschaftlich nutzbarer Beitrag liegt in der **unabhängigen Prüfung von Mittelwert, Streuung und räumlicher Abdeckung**.

Die größte verbliebene fachliche Lücke ist die **uneindeutige exakte Definition des Variabilitäts-Anomalieindikators**. Daneben bestehen Reproduktionsfragen bei konkreten Inputdaten, Seed und der publizierten Rundung eines Gewichts für 2035. Es wäre methodisch unzulässig, diese Unterschiede als bereits durch Q24/Q22 verbindlich entschieden auszugeben. Sie sind als offener Spezifikationsbedarf und — soweit nötig — ausdrücklich als eigene methodische Festlegung zu behandeln.

# Quellenverzeichnis (ausschließlich offizielle Dokumente)

**[Q26-I]** ENTSO-E (2026): *TYNDP 2026 Identification of System Needs Methodology*, Version for Public Consultation, 25.02.2026, §3.7, Anhang 6.3. <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf>

**[Q26-S]** ENTSO-E / ENTSOG (2026): *TYNDP 2026 Scenarios Methodology Report*, Juni 2026; Kap. 6 und Anhang III *Weather Year Selection Methodology*, besonders Tabellen 34 und 36. <https://2026.entsos-tyndp-scenarios.eu/scenarios-methodology-report/weather-year-selection/> und <https://2026.entsos-tyndp-scenarios.eu/scenarios-methodology-report/annex-iii-weather-year-selection-methodology/>

**[Q24]** ENTSO-E (2024): *Identification of System Needs – Implementation Guidelines*, §8.2 *Methodology for the definition of representative climate years and weeks*, insbesondere §8.2.1–8.2.3. <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2024/foropinion/SystemNeedsMethodology.pdf>

**[Q22]** ENTSO-E (2022): *TYNDP 2022 IoSN Implementation Guidelines*, §6.3 *Methodology for the selection of representative climate years and weeks* (Jahresauswahl). <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2022/public/IoSN-IG.pdf>
