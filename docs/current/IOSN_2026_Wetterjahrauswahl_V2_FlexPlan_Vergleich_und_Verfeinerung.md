---
title: "IoSN 2026 – Wetterjahrauswahl V2: FlexPlan-Vergleich und methodische Verfeinerung"
subtitle: "Vergleich der offiziellen Methoden, mathematische Hybridvarianten und Validierungsprotokoll"
date: "2026-10-19"
lang: de-DE
status: "Wissenschaftliche Methodenspezifikation – vorgeschlagene Weiterentwicklung, noch nicht numerisch validiert"
scope: "Nur Auswahl und Gewichtung vollständiger repräsentativer Wetterjahre"
---

# IoSN 2026 – Wetterjahrauswahl V2: FlexPlan-Vergleich und methodische Verfeinerung

**Dokumentstatus.** Eigenständige Version 2 / Ergänzung zur [IoSN-2026-Wetterjahrauswahl V1](IOSN_2026_Wetterjahrauswahl_konsolidierte_Methodik_2024_2022.md). Die veröffentlichte ENTSO-E-Methode von 2026 bleibt unverändert als **Baseline B0** erhalten; FlexPlan D1.1 (2020) liefert eine **alternative, offiziell dokumentierte Methode** zur jahresweisen Szenarioreduktion. Die in diesem Dokument abgeleiteten Verfahren H1 und H2 sind **neue, zu prüfende Forschungsvorschläge**, keine vorgeblichen ENTSO-E-Originalalgorithmen und keine bereits experimentell bestätigten Verbesserungen.

**Geltungsbereich.** Auswahl und Gewichtung kompletter, räumlich konsistenter Klimamodell-Wetterjahre für Zieljahre 2030/2035/2040/2050. **Ausgeschlossen:** Auswahl repräsentativer Wochen, Tage oder Stunden, zeitliche Reduktion der Ausgabedaten, synthetische Mischjahre und Neuentwicklung eines Markt- oder Lastflussoptimierers. Stündliche Werte dürfen für die *Merkmalsberechnung eines vollständigen Jahres* analysiert werden; die ausgewählten Originalstunden werden nicht entfernt.

**Hauptschlussfolgerung.** FlexPlan ergänzt IoSN 2026 substanziell auf der Ebene des **Jahresdeskriptors**: Statt nur relativ grober meteorologischer Jahresmerkmale können synchronisierte, physikalisch interpretierbare Profile von Nachfrage, Wind und PV, deren räumliche Kovarianz, Last-/RES-Spitzen sowie die Dauer ungünstiger Wetterlagen berücksichtigt werden. Das Clustering und die Auswahl der Vertreter können danach entweder **konservativ innerhalb der offiziellen IoSN-Cluster (H1)** oder **neu mittels einer globalen Optimierung über drei reale Medoide (H2)** erfolgen. Die offizielle Wahrscheinlichkeitsschätzung aus **Clusterhäufigkeiten** bleibt zunächst erhalten. Eine eigenständige Kalibrierung dieser Gewichte ist optional und nicht mehr als reine Häufigkeitswahrscheinlichkeit zu interpretieren.

## 1. Offizielle Quellen, Quellenhierarchie und Anspruchsniveau

| Kürzel | Primärquelle | Für diese Untersuchung relevante Inhalte | Autorität |
|---|---|---|---|
| **I26** | ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, Konsultationsfassung vom 25.02.2026; §3.7, Anhang 6.3 | 30 Klima-Jahr-Kandidaten, PCA/K-Means, 3 Wetterjahre, Szenariogewichte | Primäre IoSN-Referenz |
| **S26** | ENTSO-E/ENTSOG, *TYNDP 2026 Scenarios Methodology Report*, Juni 2026, Anhang III *Weather Year Selection Methodology* | Operative Präzisierungen: PECD 4.2, neun Makroregionen, zwei PC1, K-Means, 10 Initialisierungen, Clustergrößen | Aktuelle ergänzende Primärquelle zur 2026er Auswahl |
| **C26** | ENTSO-E/ENTSOG, *TYNDP 2026 Scenarios Consultations Summary Report*, Januar 2026, Anhang I, S. 36–40 | Diskutierte Weiterentwicklung durch granularere Eingaben, Extremereignisse, K-Medoids, bessere Begründung | **Verbesserungsvorschläge**, nicht als produktiver Standard nachgewiesen |
| **F20** | FlexPlan Consortium, *D1.1 Monte Carlo Scenario Generation and Reduction*, 10.12.2020, Version 1.0; §§5.1–5.3, 6.2.1 | Jahresprofile, Korrelationsbewahrung, Merkmalsreduktion, K-Means, reale Vertreter, Clusterwahrscheinlichkeiten | Primärquelle für den konkurrierenden Ansatz |
| **H24** | ENTSO-E, *IoSN Implementation Guidelines* 2024, §8.2, nur Wetterjahrauswahl | Historische Residuallast-Momentenkriterien | Ergänzende historische Prüfung |
| **H22** | ENTSO-E, *IoSN Implementation Guidelines* 2022, §6.3, nur Wetterjahrauswahl | Historische Repräsentativitätsprüfung und K-Medoids | Ergänzende historische Prüfung |

**Aussagestatus:** **[D26]** ausdrücklich I26/S26; **[DF]** ausdrücklich F20; **[DC]** lediglich als Möglichkeit in C26 diskutiert; **[DH]** historische IoSN-Vorgabe; **[R]** nachvollziehbare mathematische Rekonstruktion, nicht Originalformel; **[P]** eigener Forschungsvorschlag; **[O]** offen oder numerisch nicht verifiziert.

Weder FlexPlan D1.1 noch die Verbesserungsvorschläge C26 dürfen als neu beschlossener IoSN-2026-Standard bezeichnet werden. Frühere IoSN-Jahresauswahlmethoden sind **Vergleichs-/Validierungsquellen**, kein automatischer Ersatz der Juni-2026-Methode.

## 2. Einheitlicher mathematischer Vergleichsrahmen

Für ein Zieljahr \(Y\) sei die **vollständige Grundgesamtheit**

\[
\mathcal I_Y=\mathcal M\times\mathcal W_Y,\qquad
\mathcal M=\{\mathrm{CMR5},\mathrm{ECE3},\mathrm{MEHR}\},\qquad
|\mathcal W_Y|=10,\quad N=30.
\tag{1}
\]

Jeder Kandidat \(i\in\mathcal I_Y\) besteht aus einer **einzigen, vollständigen Klima-Jahr-Realisierung** über sämtliche Regionen \(r\), Technologien \(v\) und Originalzeitindizes \(t\):

\[
X_i=\{x_{i,v,r,t}:v\in\mathcal V,\ r\in\mathcal R_v,\ t\in\mathcal T_{i,v}\}.
\tag{2}
\]

Die Variablen besitzen unterschiedliche Originalraster (Wind/PV stündlich, HDD/CDD täglich, bestimmte Wasserkraftangaben wöchentlich). Diese Raster dürfen **nicht** ohne definierte Einheiten-/Aggregationsregeln als gleichartige numerische Daten behandelt werden.

Gesucht sind **drei tatsächlich vorhandene, ganze Wetterjahre**

\[
\mathcal S_Y=\{s_1,s_2,s_3\}\subset\mathcal I_Y,
\quad s_k\ne s_\ell\;(k\ne\ell),
\quad\boldsymbol\pi\in\Delta_3
:=\{\pi\in\mathbb R_{\ge0}^3:\sum_k\pi_k=1\}.
\tag{3}
\]

Drei verschiedene Gewichtsbegriffe werden strikt getrennt:

- \(\beta_{v,r,Y}\): **räumliche Relevanz** einer Region/Technologie bei der Merkmalskonstruktion;
- \(q_i\): **Gewicht eines ursprünglichen Kandidaten**; für den 2026er Standardfall \(q_i=1/30\);
- \(\pi_k\): **Szenariomasse des ausgewählten Jahres** als Proxy für seinen Cluster.

Die \(\pi_k\) sind keine CO₂-, Energie- oder Strompreise und auch **keine unmittelbare Häufigkeit extremer Ereignisse**. FlexPlan-Anwendungsbeispiele mit 35 oder 40 anderen Jahresszenarien sind **nicht** mit der statistischen PECD-2026-Grundgesamtheit zu vermischen. Für alle methodischen Vergleiche gilt derselbe 30er-PECD-Datensatz und \(K=3\) Repräsentanten.

## 3. B0 – präzise Rekonstruktion der IoSN-2026-Referenz

### 3.1 Eingangsdaten und regionale Abbildung [D26]

Nach S26 werden pro Kandidat sechs Merkmalsfamilien ausgewertet: (i) Onshore-Wind, (ii) Offshore-Wind, (iii) Solar-PV, (iv) Laufwasserkraft, (v) Reservoirwasserkraft und (vi) Heiz-/Kühlgradtage (HDD/CDD). 53 Bidding Zones werden neun Makroregionen (Baltic, CE, CW1, CW2, Nordic, SC, SE, SW, UK) zugeordnet. Wind- und PV-Kapazitätsfaktoren werden mit installierten Kapazitäten des Studienjahrs skaliert; Hydro-Eingaben entstammen PECD; HDD/CDD berücksichtigen regionsspezifische Temperaturschwellen.

Die **zwei** Indikatoren je Familie messen (a) relatives Jahresniveau und (b) intraannuelle Variabilität. S26 präzisiert: Makroregionale Deltas werden zunächst technologieabhängig gewichtet und **vor** einer Z-Standardisierung auf eine Größe je Jahr und Familie zusammengefasst. Die Relevanzgewichte basieren bei Erzeugung auf dem Kapazitätsanteil, bei HDD/CDD auf der anteiligen Last:

\[
\beta_{v,r,Y} = \frac{K_{v,r,Y}}{\sum_{r'}K_{v,r',Y}}
\quad(v\in\mathrm{RES/Hydro});\qquad
\beta_{L,r,Y}=\frac{L_{r,Y}^{\mathrm{ref}}}{\sum_{r'}L_{r',Y}^{\mathrm{ref}}}.
\tag{4}
\]

Die exakte regional relevante Größe \(K\) bzw. \(L^{\rm ref}\), der Ausschluss von Nullkapazitäten und die konkrete Hydro-Einheit sind als Datenvertrag festzuhalten. **Normalisierung und physikalische Relevanzgewichtung dürfen nicht verwechselt werden**.

### 3.2 Jahresmerkmale und bekannte definitorische Unschärfe [D26/R/O]

Für Familie \(v\), Region \(r\), Jahr \(i\) kann der Niveaumerkmalsanteil konsistent formuliert werden als

\[
\mu_{i,v,r}=T_v^{-1}\sum_t x_{i,v,r,t},\quad
\bar\mu_{v,r}=\sum_iq_i\mu_{i,v,r},\quad
\delta^{\mu}_{i,v,r}=\mu_{i,v,r}-\bar\mu_{v,r}.
\tag{5}
\]

Die **Variabilitätsanomalie** ist in I26/S26 nicht in einer durchgängig eindeutigen numerischen Vorschrift festgelegt. Der S26-Text verknüpft eine *kumulative Anomalie* mit einer Streuungsreferenz; eine mögliche, aber ausdrücklich **nicht originalverifizierte** Rekonstruktion ist

\[
\sigma_{i,v,r}=\operatorname{sd}_t(x_{i,v,r,t}),\qquad
\delta^{\sigma}_{i,v,r}=\sigma_{i,v,r}-\sum_jq_j\sigma_{j,v,r}.
\tag{6}
\]

Die empirisch eingesetzte Originaldefinition und ihre Kalenderkonvention müssen aus Originaldaten-/Quellcodeprovenienz aufgeklärt werden. Ferner ist eine rein kumulative Abweichung \(\sum_t(x_{i,t}-\bar x_t)\) bei gemeinsamem Zeitindex mathematisch eine affine Funktion des Jahresmittels und damit **kein unabhängiges Maß für Volatilität** [R]. Der Widerspruch ist keine Lizenz, die tatsächliche ENTSO-E-Implementierung ungekennzeichnet zu korrigieren.

Zunächst werden regionale Deltas mit \(\beta\) aufsummiert:

\[
d^{\mu}_{i,v}=\sum_r\beta_{v,r,Y}\delta^{\mu}_{i,v,r},\qquad
 d^{\sigma}_{i,v}=\sum_r\beta_{v,r,Y}\delta^{\sigma}_{i,v,r}.
\tag{7}
\]

Danach wird **jede** der sechs Jahresmerkmalsreihen standardisiert:

\[
 A_{i,v}=\frac{d^{\mu}_{i,v}-\overline{d^{\mu}}_v}{\operatorname{sd}_i(d^{\mu}_{i,v})},\quad
 S_{i,v}=\frac{d^{\sigma}_{i,v}-\overline{d^{\sigma}}_v}{\operatorname{sd}_i(d^{\sigma}_{i,v})},\qquad
 A,S\in\mathbb R^{30\times6}.
\tag{8}
\]

**Wichtig:** Hätte man eine einzelne regionale Spalte zuerst mit einem festen positiven Gewicht multipliziert und anschließend dieselbe Spalte separat z-standardisiert, würde sich das Gewicht exakt herauskürzen. Die in S26 beschriebene **Aggregation vor Standardisierung** vermeidet diesen spezifischen Fehler grundsätzlich.

### 3.3 Zwei PCA-Achsen, K-Means und Wahrscheinlichkeiten [D26/R]

Die zwei Blöcke \(A,S\) erhalten **je eine eigene PCA**. Jeweils PC1 wird behalten:

\[
\mathbf z_i^{I}=\begin{bmatrix}(Au_A)_i\\(Su_S)_i\end{bmatrix},\quad
u_A=\arg\max_{\|u\|_2=1}\|Au\|_2^2,\quad
u_S=\arg\max_{\|u\|_2=1}\|Su\|_2^2.
\tag{9}
\]

In Gleichung (9) sind \(u_A,u_S\) die Einheits-Eigenvektoren zu den jeweils größten Eigenwerten der beiden Kovarianzmatrizen. Anschließend wird K-Means mit \(K=3\) angewandt:

\[
\min_{\mathcal C_1,\mathcal C_2,\mathcal C_3,\,\mathbf c_k}
\sum_{k=1}^{3}\sum_{i\in\mathcal C_k}\|\mathbf z_i^{I}-\mathbf c_k\|_2^2,
\quad \mathbf c_k=\frac1{|\mathcal C_k|}\sum_{i\in\mathcal C_k}\mathbf z_i^{I}.
\tag{10}
\]

S26 nennt **zehn zufällige Initialisierungen** und einen festen Seed (dessen numerischen Wert das Dokument nicht nennt). Als Vertreter wird das **reale** Clusterjahr gewählt, das dem Zentrum im 2D-Raum am nächsten liegt. Die 2026er Gewichte sind **exakt**

\[
\boxed{\pi_k^{I}=|\mathcal C_k|/30.}
\tag{11}
\]

| Zieljahr | Offizielle ausgewählte WS-IDs | Clustergrößen in dieser Reihenfolge | Genaue rationale Gewichte |
|---|---|---|---|
| 2035 | WS032 / WS037 / WS059 | 7 / 13 / 10 | 7/30 / 13/30 / 10/30 |
| 2040 | WS065 / WS071 / WS077 | 6 / 12 / 12 | 6/30 / 12/30 / 12/30 |
| 2050 | WS091 / WS092 / WS106 | 7 / 17 / 6 | 7/30 / 17/30 / 6/30 |

Die veröffentlichten gerundeten Gewichte lauten 2035 **0,24 / 0,43 / 0,33**, 2040 **0,20 / 0,40 / 0,40**, 2050 **0,23 / 0,57 / 0,20**. Die Zuordnung 2035 **WS032 = 0,24 bei Clustergröße 7** stimmt mit normalem Zwei-Dezimal-Runden von 7/30 (=0,23) nicht überein. Ein Summen-Rundungsausgleich ist plausibel, aber ohne Originalvorgabe nicht als sicherer Schritt zu behaupten [O]. Für Rechnungen die **exakten Brüche**, für publizierte Tabellen die **publizierten Werte samt Hinweis** verwenden.

### 3.4 Grenzen von B0

Mit nur zwei PC1-Scores können wichtige Unterschiede in Quantilen, räumlichen Kovarianzen, Dauer von Windflauten oder zeitgleichen Lastspitzen verloren gehen. Das ist **keine nachgewiesene Schwäche der konkreten neun ausgewählten Wetterjahre**, sondern eine fehlende mathematische Garantie des statistischen Verfahrens. B0 bleibt die bindende wissenschaftliche Vergleichsbasis der Methodenuntersuchung.

## 4. F20 – originale FlexPlan-D1.1-Methode für **vollständige Jahre**

### 4.1 Grundobjekt: korrelierter Nachfrage-/Erzeugungs-Jahrespfad [DF]

Der FlexPlan-Bericht D1.1, insbesondere §5.2–5.3, behandelt Szenarien aus **simultanen Jahresreihen** von Nachfrage und wetterabhängiger Erzeugung an Netzknoten. Anders als IoSN B0 wird nicht notwendigerweise zuerst ein kleiner meteorologischer Mittelwert-/Variabilitätsvektor berechnet. Die Jahrespfade können als sehr hochdimensionale Vektoren aufgefasst werden:

\[
\mathbf x_i^{F}
=\operatorname{vec}\left(
P^{L}_{i,n,t},\ P^{PV}_{i,n,t},\ P^{W}_{i,n,t}
\right)_{n\in\mathcal N,\;t=1,\ldots,T}.
\tag{12}
\]

Die zeitliche **und** räumliche Korrelation liegt innerhalb der einen Jahresrealisation. D1.1 beschreibt in der Szenariogenerierung bis zu **40** Jahresvarianten; in der Jahresreduktions-Demonstration werden ausdrücklich **35 korrelierte komplette Jahresrealisationen** mit gemeinsam vorhandenen Last-, PV- und Windwerten verwendet. Andere Text-/Abbildungsstellen referenzieren erneut 40. Der Unterschied ist als Provenienz-/Beispielumfangsgrenze zu dokumentieren. Die im Beispiel verwendeten **fünf Cluster** sind nicht als universell optimale Anzahl hergeleitet. Für den direkten Vergleich mit IoSN muss deshalb **N=30 und K=3** gelten; das ist die neue Transferentscheidung, nicht der originale FlexPlan-Demonstrationsumfang.

### 4.2 Kapazitätsnormalisierung und euklidische Distanz [DF/R]

FlexPlan empfiehlt eine Normierung der Last- und Erzeugungsprofile durch die entsprechenden nominalen Last-/Erzeugungskapazitäten, um eine allein von großen Anlagen geprägte euklidische Distanz zu vermeiden:

\[
\widetilde P^L_{i,n,t}=P^L_{i,n,t}/K_n^L,\qquad
\widetilde P^v_{i,n,t}=P^v_{i,n,t}/K_n^v
\quad (v\in\{PV,W\}).
\tag{13}
\]

Dies setzt \(K_n^v>0\) voraus und verlangt ein explizites Verfahren für Nullkapazitäten und fehlende Daten. Eine direkte Distanz ohne weitere Projektion wäre

\[
 d_F^2(i,j)=\sum_{n,t,v}\eta_{n,v}
\bigl(\widetilde P^v_{i,n,t}-\widetilde P^v_{j,n,t}\bigr)^2
\tag{14}
\]

mit \(\eta_{n,v}=1\) als einfachem Rohprofilvergleich. Die zusätzlichen \(\eta\)-Gewichte sind ein **eigener Verfeinerungsvorschlag [P]**, nicht als ursprünglicher FlexPlan-Parameter verifiziert. Die Rohdistanz kann schon durch eine Verschiebung eines meteorologischen Ereignisses um einige Tage anwachsen, obwohl beide Jahre ähnliche Energie- und Knappheitsverteilungen besitzen. Diese Eigenschaft ist bei **Jahresauswahl** zu prüfen und motiviert interpretierbare Jahresdeskriptoren.

### 4.3 Drei Dimensionierungs-/Merkmalsvarianten [DF]

FlexPlan D1.1 diskutiert für die hochdimensionale Clustermatrix drei Wege:

1. **PCA** direkt auf Leistungszeitreihen; im numerischen Fall werden beispielhaft 30 Komponenten mit **mehr als 95 % erklärter Varianz** verwendet. Nur 35 Szenarien bei sehr vielen Ursprungsmerkmalen können jedoch empfindliche, schlecht generalisierbare Hauptkomponenten erzeugen. Eine PCA per SVD ist auch bei \(N<p\) rechnerisch möglich, besitzt dann aber höchstens \(N-1\) nichttriviale zentrierte Komponenten. Die oft zitierte Forderung, viel mehr Beobachtungen als Features zu haben, ist eine **statistische Empfehlung**, keine algebraische Notwendigkeit.
2. **Bedeutsame physikalische Kennwerte** statt aller Rohstunden; in der FlexPlan-Jahresdemonstration werden **zwölf Merkmale** verwendet. Die exakten zwölf Originaldefinitionen werden hier mangels einer vollständig verifizierten Formeltabelle **nicht erfunden oder als sichere Übernahme ausgegeben**. Alle unten verwendeten Zusatzfeatures sind ausdrücklich **[P]**.
3. **Verringerung der Knoten-/Featurezahl** mittels räumlichen Clusterings. Das ist eine Reduktion der *Featuredimension vor Jahresauswahl*, nicht der Stunden des später ausgewählten Wetterjahres; im Demonstrationskontext werden 30 Cluster von Netz-Zuständen/Knotenfeatures erwähnt.

Keiner dieser Wege allein beweist, dass relevante europäische Stromsystem-Extremereignisse erhalten bleiben. Die Auswahl von PCA-Komponenten mit hoher erklärter Rohprofilvarianz kann beispielsweise ökonomisch kritische, aber seltene Stresszustände vernachlässigen.

### 4.4 K-Means, Repräsentant und Clusterwahrscheinlichkeiten [DF]

Die FlexPlan-Algorithmuskette in §5.3 lässt sich für vollständige Jahre abstrahieren als:

\[
\widetilde{\mathbf X}
\ \longrightarrow\ \Phi_F(\widetilde{\mathbf X})
\ \longrightarrow\ K\text{-Means}
\ \longrightarrow\ \text{Repräsentanten und Clustergewichte}.
\tag{15}
\]

Dabei kann \(\Phi_F\) die Identität, PCA oder eine kompakte Merkmalstransformation sein. Nach K-Means wird ein Vertreter gewählt. Ein **Zentroid** in Rohprofilkoordinaten ist ein künstlich gemittelter Jahrespfad; bei starker Feature-Projektion besitzt das Zentroid nicht einmal die ursprüngliche Profil-Dimension. D1.1 sieht hierfür die Wahl eines **echten** Jahres aus dem Cluster vor und beschreibt als generelle Möglichkeit eine zufällige Cluster-Mitgliedswahl. Für die wissenschaftliche Vergleichbarkeit wird diese Zufälligkeit in F3 **durch deterministische nächste-Zentrum-/Medoidwahl ersetzt [P]**. Die Zufälligkeit der ursprünglichen Repräsentantenwahl darf nicht stillschweigend als IoSN-2026-Regel übernommen werden.

Unter gleichgewichteten Eingangsrealisationen ist der FlexPlan-Gewichtsansatz analog zu IoSN:

\[
\boxed{\pi_k^F=|\mathcal C_k^F|/N_F.}
\tag{16}
\]

Die **Unterschiede der Gewichte** nach einer FlexPlan-basierten Neuauswahl entstehen primär aus der **veränderten Clusterpartition**, nicht aus einer grundsätzlich anderen stochastischen Gewichtungsformel.

## 5. Direkter detaillierter Methodenvergleich IoSN B0 – FlexPlan F3

**Definition F3:** Transfer der originalen FlexPlan-Jahresclusterungs-Idee auf **dieselben 30 PECD-4.2-Kandidaten**, \(K=3\), vollständige Jahresrealisationen und deterministische reale Vertreter. Diese Transferkonfiguration ist **[P]**, während die grundlegenden Schritte aus D1.1 stammen.

| Eigenschaft | B0: IoSN 2026 | F3: FlexPlan-basiert | Relevanz für die Weiterentwicklung |
|---|---|---|---|
| Original-Datenpool | 30 CMIP6/PECD-Klima-Jahr-Kombinationen, SSP2-4.5 | FlexPlan-Demonstration mit 35 gemeinsam kompletten bzw. bis zu 40 generierten historischen Jahresvarianten | Für fairen Vergleich Datenbasis und \(N=30\) angleichen |
| Zieljährige Anlagenstruktur | Kapazitäts-/Lastdaten aus PEMMDB/ETM in Auswahl | Kapazitätsnormierung von Leistungskurven | Referenzanlagen und Nachfrageannahmen fixieren |
| Primärobjekt | 12 statistische Jahreswerte (6 Niveau, 6 Variabilität) | Hochdimensionale simultane nodale Last-/RES-Jahrespfade | FlexPlan ist unmittelbarer am Betriebszustand |
| Variablen | Wind on/off, PV, Hydro RoR/Reservoir, HDD/CDD | Nachfrage, PV, Wind im Jahresdemobeispiel | Für einen gemeinsamen Test Hydro/Temperatur transparent ergänzen |
| Räumlichkeit | 53 Zonen → 9 Makroregionen → ein Wert je Technologie | Knoten-/Anlagenprofiles, ggf. Knotencluster | IoSN ist schlank, FlexPlan kann Netzlokalität erhalten |
| Gleichzeitigkeit | Innerhalb **eines ausgewählten Jahres** intakt, in Merkmalen stark verdichtet | Gemeinsamer Profilvektor über Zeit und Knoten | Für Netzprobleme Koinzidenzprüfungen ergänzen |
| Zeitliche Repräsentation der Features | Jahresmittel, Jahresvariabilität | Ganze Stundenpfade oder ihre interpretierbaren Kennwerte | Dauer, Rampen und Extremwerte ergänzbar |
| Normierung | Technologiebezogene Aggregation + Z-Score | Nominalleistungs- bzw. Lastbezugsgrößen je Profil | Nie ungeprüft Gewichte durch Standardisierung aufheben |
| Regionsrelevanz | Anlagenkapazität bzw. Lastanteile | Normierung durch Kapazität; nicht identisch zu IoSN-Gewichten | Zwei gesonderte Operationen nötig |
| Dimensionsreduktion | Zwei getrennte PC1, zusammen 2D | Rohfeatures oder PCA/12 Features/Knotenreduktion | Profil-PCA mit kleinem \(N\) kritisch |
| Hauptproblem der Merkmalswahl | Unterrepräsentation von Dauer/Stress/weiteren PCs | Extrem hohe Merkmalszahl und Kalendertag-Verschiebungseffekte | Physikalisch lesbare, robuste Jahresfeatures bevorzugen |
| Clustering | K-Means | K-Means | Identisches \(K=3\) für Vergleich |
| Initialisierung | 10 Starts, fester Seed (Wert offen) | Implementierungsabhängige Wiederholungen | Alles protokollieren; Medoids als Alternative |
| Vertreter | Tatsächliches Jahr nächst PCA-Zentrum | Zentroid oder Cluster-Mitglied, je Featurestrategie | Nur echte vollständige Jahre zulassen |
| Clustergewichte | \(n_k/30\) | \(n_k/N_F\) | Formal gleicher Frequenzansatz |
| Extremereignisse | Kein formaler Schutz | Kein formaler Schutz; vollere Informationen potentiell verfügbar | Spezielle Stressfeatures + unabhängige Validierung nötig |
| Speicher-/Hydro-Grenzen | Hydro/Temperatureingaben repräsentiert | Demonstration ersetzt keine Hydro-Speicherdynamik | Hydro-Zufluss nicht als stündliche Dispatchleistung interpretieren |
| Dokumentierte Resultate | Konkrete WS-IDs, Clustergrößen und Gewichte | Nur exemplarische Jahresclusterung, keine PECD-2026-WS-IDs | Keine neuen WS-Jahre ohne reale Berechnung behaupten |
| Methodische Reproduzierbarkeit | Exakter Code/Seed/Variabilitätsindikator teilweise offen | Konkrete Demonstrationsfeatures/Seeds nicht durchgängig verfügbar | Vergleich nur mit veröffentlichter Konfiguration + offengelegten Ergänzungen |
| Optimierungsziel | Näherung meteorologischer Hauptvariationsmuster | Näherung normierter Leistungsprofil-Features | Keiner garantiert minimalen Netzausbau-Fehler |
| Rechenaufwand | Sehr gering nach Jahresmerkmalen | Hochdimensional ohne Merkmalsreduktion | 30 Kandidaten erlauben erschöpfendes K-Medoids-Auswahlproblem |

### 5.1 Methodischer Trade-off

IoSN B0 ist **einfacher und eng an die veröffentlichte Governance gebunden**, reduziert aber viel operative Information schon *vor* dem Clustering. FlexPlan-Featuremethoden können die Last-/RES-Realisationen deutlich realitätsnäher an die operativen Belastungen koppeln, haben aber ein Risiko für **Dominanz großer Anlagen, Curse of Dimensionality, Tagesverschiebungssensitivität und eine willkürliche Featurewahl**. **Es ist noch nicht gezeigt, welche Auswahl das eigentliche Netzausbauziel besser approximiert.** Dafür wird Abschnitt 10 als verbindlicher Vergleichsrahmen eingeführt.

## 6. Wo die IoSN-2026-Methode konkret angepasst werden kann

| Originaler Schritt | Mögliche Schwäche/fehlende Information | Beitrag FlexPlan | Präzise Anpassung [P] | Keine Änderung an ... |
|---|---|---|---|---|
| Kandidatenpool | 30 wetterbasierte Jahrkombinationen | Auch operativer Jahresvektor aus Last und RES | Last-/Wind-/PV-Werte für jeden der **gleichen** 30 Kandidaten konsistent erzeugen | Zahl und Herkunft der 30 Kandidaten |
| Makroregionen | Lokale Koinzidenzen gehen im Jahresmerkmal verloren | Nodale/regionale Features | Zusätzliche Teilregions-/Kovarianzfeatures, niemals künstliche Jahreskombination | Original-53-Zonen-/9-Regionen-Zuordnung |
| Jahresmittel/Volatilität | Keine Ereignisdauer, Rampen, Peakstress | Kennwert-/Profilreduktion | Quantile, Residuallast, Rampen, längste Wind-/Lastknappheit | Vollständige Wetterzeitreihen |
| Kapazitätsgewichtung | Meteorologische Verfügbarkeit ≠ elektrische Einsatzrelevanz | Leistungsprofile und Nominalwert-Normierung | Last/RES-Normalisierung **plus separat** \(\beta_{v,r,Y}\) | Quelle und Interpretation originaler IoSN-Gewichte |
| PCA | Nur zwei PC1 | Alternativen zur hochdimensionalen PCA | Originale PC1 als eigener Block, physikalische Zusatzfeatures eigener Block | B0 vollständig reproduzierbar |
| K-Means | Zentroidnähe nur im IoSN-2D-Raum | Clusterrepräsentanten in anderem Merkmalsraum | H1: Cluster fix, physikalischer Medoid; H2: komplette 3-Medoids-Auswahl | \(K=3\), reale Jahre |
| Jahresgewichtung | Nur Häufigkeiten des B0-Feature-Raums | Häufigkeiten auch in FlexPlan | Neue Clusterhäufigkeiten; optionale Momente-Kalibrierung als eigene Variante | Keine automatische stärkere Gewichtung extremer Jahre |
| Prüfung/Begründung | PCA-Inertia ist nicht Planungsfehler | Jahrprofile ermöglichen physikalische Checks | Erhalt von Mittelwert, Varianz, Koinzidenz, Extremdauer, Ausbaukosten | Getrennte Berichterstattung Original vs. Vorschlag |

**Zusätzliche offizielle Unterstützung [DC]:** Der TYNDP-2026-Konsultationsbericht vom Januar 2026 diskutiert genau die Richtungen *höhere Granularität, klarere Auswahlbegründung, Extremfälle sowie K-Medoids/hierarchische Clusterung*. Diese Passage darf nur als **Motivation für Alternativversuche**, nicht als Nachweis des späteren offiziellen Einsatzes, zitiert werden.

## 7. Physikalisch interpretierbare Deskriptoren für vollständige Jahre [P]

### 7.1 Exogene Jahresprofile statt unbilanzierter Netzflüsse

Für \(i,r,t\) seien \(L_{i,r,t}\) die stündliche zieljahrspezifische Last, \(CF^{v}_{i,r,t}\) die PECD-Verfügbarkeit und \(K^{v}_{r,Y}\) die installierte Wind-/PV-Kapazität. Definiere

\[
A^v_{i,r,t}=K^v_{r,Y}CF^v_{i,r,t},\qquad
R_{i,r,t}=L_{i,r,t}-\sum_{v\in\{PV,ON,OF\}}A^v_{i,r,t}.
\tag{17}
\]

\(R\) ist eine **exogene Residuallast für Merkmalszwecke**, *kein* eindeutiger physikalisch bilanzierter PTDF-Einspeisungsvektor. Flexibler Dispatch, Importsaldo, Speicherung, konventionelle Erzeugung und Slack-Regel sind darin nicht bestimmt. Für Netzflussmerkmale wären zusätzliche Dispatch-/Bilanzierungsannahmen erforderlich, die dieses Dokument **nicht erfindet**.

Hydro-Daten werden separat und **einheitentreu** behandelt: Ein wöchentlicher Reservoirzufluss ist keine ohne Weiteres bekannte stündliche Turbinenleistung; falls originale PECD-Energieprofile vorliegen, sind deren Originaldefinition und Auflösung einzuhalten. Temperaturmerkmale verbleiben eigenständig, wenn die vollen stündlichen Lastprofile für *alle* 30 Jahre nicht verfügbar sind. Die DFT erzeugt nach 2026er Standard häufig Lastprofile erst für ausgewählte Jahre; F3/H1/H2 benötigen zur fairen Neubewertung **alle 30** konsistent wetterabhängigen Lastjahre [O]. Dies ist ein bedeutender zusätzlicher Daten-/Rechenbedarf.

### 7.2 Merkmalskatalog [P, keine originalen zwölf FlexPlan-Features]

Die folgenden **neu spezifizierten** Kennwerte werden aus **vollständigen Jahren** berechnet. Quantile sind einheitlich als empirische Quantile mit festgelegter Interpolationsregel zu bestimmen; die zeitliche Referenz einer Dauerangabe ist Stunden, wenn stündliche Daten vorliegen.

| Merkmal \(g_{i,r}\) | Mathematische Definition | Zweck |
|---|---|---|
| Mittlere Residuallast | \(\bar R_{i,r}=T^{-1}\sum_tR_{i,r,t}\) | Mittlerer nichtfluktuierender Deckungsbedarf |
| Residuallast-Streuung | \(\sqrt{T^{-1}\sum_t(R_{i,r,t}-\bar R_{i,r})^2}\) | Innerjährliche Schwankungsstärke |
| Hoher Quantilwert | \(Q_{0.95}(\{R_{i,r,t}\}_t)\) | Häufiges hohes Deckungsdefizit |
| Maximale Residuallast | \(\max_t R_{i,r,t}\) | Jahresspitze |
| Niedriger Quantilwert | \(Q_{0.05}(\{R_{i,r,t}\}_t)\) | Überschuss-/Negativresiduallastregime |
| Hohe Rampen | \(Q_{0.95}(\{|R_{i,r,t}-R_{i,r,t-1}|\}_t)\) | Kurzfristige Flexibilitätsbeanspruchung |
| Persistenter Defizitblock | \(\ell^{R,+}_{i,r}(\tau_R)\): längster konsekutiver Block mit \(R_{i,r,t}>\tau_R\) | Mehrtägige Knappheit |
| Persistente Windflaute | \(\ell^{W,-}_{i,r}(\tau_W)\): längster Block mit \(CF^{W}_{i,r,t}<\tau_W\) | Windknappheit/Dunkelflauteproxy |
| Saisonmittel | \(\bar R_{i,r}^{\rm winter}\), \(\bar R_{i,r}^{\rm summer}\) | Saisonale Last-/Erzeugungsmuster |
| Koinzidenz | \(\operatorname{corr}_t(R_{i,r,t},R_{i,r',t})\) | Räumlich gemeinsame Stresslagen |
| Hydro-Jahresenergie | Einheitentreue Summe wöchentlicher PECD-Energieangaben | Wasserkraftverfügbarkeitsregime |
| Temperaturlast | Jahres-/Saison-HDD/CDD und extreme Tagesfolgen | Lasttreibende Wetterextreme |

**Alle Schwellen \(\tau_R,\tau_W\), regionalen Indizes, Quantilalgorithmen, Saisonabgrenzungen und Gewichtungen müssen vor der Auswertung festgelegt werden.** Keine nachträgliche Schwellenwahl zur Erzwingung eines bestimmten Wetterjahres. Die Einzelmerkmale sind statistische Deskriptoren, nicht jeweils eine zusätzliche Eintrittswahrscheinlichkeit.

**Regionale Kohärenz:** Ein Wetterjahr wird als **ganze gekoppelte Realisation** aus einem Modelllauf behalten. Deutsche Winddaten aus Jahr A und italienische Lastdaten aus Jahr B dürfen nicht zu einem vermeintlichen gemeinsamen Jahr „vermischt“ werden.

### 7.3 Normalisierung, dimensionierte Merkmalsblöcke und Skalenschutz

Definiere Lastreferenz \(L_{r,Y}^{\rm ref}>0\) sowie Kapazitäten \(K^v_{r,Y}>0\) für vorhandene Technologien; bei \(K=0\) wird die Größe als **nicht anwendbar** behandelt, nicht durch Null dividiert. Normierte Leistungsprofile sind \(L/L^{\rm ref}\) und \(A^v/K^v\). Nach der regionalen Aggregation werden numerisch dimensionslose Jahresfeatures über die **30 Kandidaten** z-standardisiert. Dabei Nullvarianzspalten ausschließen. Zieljährliche Regionenrelevanz \(\beta_{v,r,Y}\) nicht mit der p.u.-Normierung gleichsetzen.

### 7.4 Eigenständiger PCA-/Profil-Kontrolldiagnostikblock

Zur Erkennung des Verlusts an zeitlicher Struktur kann ergänzend eine Rohprofildistanz ermittelt werden:

\[
 d_{\rm profile}(i,j)^2=
\frac1T\sum_{t=1}^{T}\sum_{v,r}\omega_{v,r}
\left(\widetilde x_{i,v,r,t}-\widetilde x_{j,v,r,t}\right)^2.
\tag{18}
\]

Diese Distanz ist stark davon abhängig, **an welchem Kalendertag** ein Ereignis im Jahr liegt. Für die globale Jahresauswahl daher nicht ohne Sensitivität als alleinige Zielfunktion verwenden. Bei quantil-/dauerkurvenbasierten Features wird die Kalendertagausrichtung zwischen verschiedenen Jahren dagegen weniger stark gewichtet, während innerhalb jedes realen Repräsentanten die ursprüngliche Chronologie erhalten bleibt.

## 8. Hybridmethode: zwei alternative Eingriffstiefen [P]

### 8.1 Definition eines kombinierten Jahresabstands

Für jeden Kandidaten stehen zur Verfügung:

- \(z_i^I\in\mathbb R^2\), der **unveränderte** offizielle IoSN-PCA-Score (wenn reproduziert);
- \(f_i\in\mathbb R^{p_F}\), z-standardisierte physikalische Last-/Erzeugungsjahresmerkmale;
- \(h_i\in\mathbb R^{p_H}\), z-standardisierte Dauer-/Stressmerkmale.

Eine **explizite neue** Distanz lautet

\[
\boxed{
 d(i,j)^2=\alpha\frac{\|z_i^I-z_j^I\|_2^2}{s_I^2}
+\beta\frac{(f_i-f_j)^\top W_F(f_i-f_j)}{s_F^2}
+\gamma\frac{(h_i-h_j)^\top W_H(h_i-h_j)}{s_H^2}}
\tag{19}
\]

unter \(\alpha,\beta,\gamma\ge0\), \(\alpha+\beta+\gamma=1\), \(W_F,W_H\succeq0\). Die positiven Distanzskalen \(s_I^2,s_F^2,s_H^2\) werden je Block *vorab*, beispielsweise als Mittelwert nichtverschwindender paarweiser quadrierter Distanzen über den 30er-Pool, festgelegt. Null-Distanz-Blöcke ausschließen; Doppelzählungen (etwa identische Mittelwerte im IoSN- und Lastblock) vermeiden oder begründen. Hier werden **keine erfundenen numerischen \(\alpha,\beta,\gamma\)** als FlexPlan-Vorgaben ausgegeben. Verschiedene Voreinstellungen sind als Sensitivität zu dokumentieren.

### 8.2 H1: Offizielle Cluster und Gewichte bleiben fest

Die Partition \(\mathcal C_k^I\) aus B0 bleibt unverändert. Nur der Vertreter wird als **clusterinterner Medoid** der neuen, physikalisch erweiterten Distanz bestimmt:

\[
\boxed{s_k^{H1}=\underset{j\in\mathcal C_k^I}{\arg\min}
\sum_{i\in\mathcal C_k^I}q_i\,d(i,j)^2,\qquad
\pi_k^{H1}=|\mathcal C_k^I|/30.}
\tag{20}
\]

**Vorteile:** Direkte Vergleichbarkeit; exakt dieselben drei Regime und Gewichte wie IoSN; nur der meteorologische Vertreter je Regime wird möglicherweise ausgetauscht. Keine K-Means-Neuclusterung nötig. **Grenze:** Eine suboptimale Regimegrenze im IoSN-2D-Raum wird bewusst nicht geändert. Die Konstruktion verbessert höchstens die Summe der **clusterinternen Abstände nach Gleichung (19)**; bessere Investitionsresultate sind erst nachzuweisen.

### 8.3 H2: Global exakt optimierte Drei-Medoids-Auswahl

Der zweite Vorschlag optimiert **sowohl** Zuordnung als auch drei reale Wetterjahre im Distanzraum (19):

\[
\boxed{\mathcal S^{H2}=\underset{\mathcal S\subset\mathcal I_Y,\ |\mathcal S|=3}{\arg\min}
\sum_{i=1}^{30}q_i\min_{s\in\mathcal S}d(i,s)^2.}
\tag{21}
\]

Der Ausdruck ist eine gewichtete **K-Medoids-/p-Median-Formulierung** mit drei Medoiden. Er ist *nicht* dasselbe wie K-Means, weil die Zentren auf reale Kandidaten beschränkt bleiben. Bei nur 30 Kandidaten gilt

\[
\binom{30}{3}=4060.
\tag{22}
\]

Alle 4.060 Kombinationen lassen sich anhand einer einmal berechneten 30×30-Distanzmatrix **exhaustiv** durchprüfen; damit wird das globale Optimum **dieser** exakt angegebenen Diskret-Zielfunktion gefunden. Dies bedeutet keineswegs das globale Optimum des nachgelagerten Netzausbauproblems. Bei Gleichstand wird über lexikografische WS-ID-Reihenfolge entschieden. Die Zuordnung ist

\[
 a(i)=\underset{k\in\{1,2,3\}}{\arg\min}\ d(i,s_k)^2,
\quad\mathcal C_k^{H2}=\{i:a(i)=k\},
\quad\boxed{\pi_k^{H2}=\sum_{i\in\mathcal C_k^{H2}}q_i
=|\mathcal C_k^{H2}|/30.}
\tag{23}
\]

Bei Distanzgleichstand werden ausgewählte Medoide zuerst sich selbst zugeordnet; danach kleinste WS-ID. Dadurch enthalten alle drei Cluster ihre jeweiligen Repräsentanten. Die Wahrscheinlichkeit bleibt eine **empirische Clusterhäufigkeit**, ihre Zahlenwerte dürfen gegenüber IoSN B0 abweichen.

### 8.4 Optional: Extrem-Abdeckung als Nebenbedingung

Soll ein vordefinierter, besonders schwerer Zustand unter den drei Repräsentanten vorkommen, kann eine getrennte [P]-Variante verlangen:

\[
\exists s\in\mathcal S:\quad g_s^{\rm stress}\ge\tau_{\rm stress}.
\tag{24}
\]

Die Stressfunktion, räumliche Aggregation und Schwelle sind **vorab** zu definieren. Diese Forderung kann bei mehreren räumlich widersprüchlichen Extremen unvereinbar mit genau drei Repräsentanten sein. Eine künstlich erhöhte \(\pi_k\) für ein Extremjahr wäre **keine** sachlich begründete Eintrittswahrscheinlichkeit. Ein externes viertes Stressjahr, falls später erforderlich, ist **separater Stresstest ohne stillschweigende Wahrscheinlichkeitsmasse** und nicht Bestandteil des 30→3-Hauptvergleichs.

## 9. Gewichtung: Originalregel bewahren, neue Kalibrierung klar abtrennen

### 9.1 Häufigkeitswahrscheinlichkeiten von IoSN und FlexPlan [D26/DF]

Sowohl IoSN 2026 als auch FlexPlan beschreiben Clustergewichte im Sinne einer **Anteilshäufigkeit**. Bei gleichgewichteten Ausgangsszenarien ist

\[
\boxed{\pi_k^{\rm freq}=n_k/30,\qquad n_k=|\mathcal C_k|,\quad\sum_kn_k=30.}
\tag{25}
\]

Unter der in S26 genannten Ergodizitätsannahme gelten Clusteranteile als Schätzer der Wahrscheinlichkeit eines Wetterregimes. Bei nur drei Klimamodellen und zehn Projektionsjahren ist diese Interpretation **modellabhängig** und kein formaler Beweis, dass die Klimamodelle unabhängige, gleichwahrscheinliche Ziehungen der realen Zukunft sind. Insbesondere ist \(\pi_k\) nicht proportional zu Residuallastmaxima oder dem volkswirtschaftlichen Schaden einzelner ausgewählter Jahre.

**H1:** \(\pi^{H1}=\pi^I\) (exakt gleich). **H2:** \(\pi^{H2}\) aus neuem Cluster. Exakte Brüche und veröffentlichte Rundungen getrennt exportieren.

### 9.2 H2-W: optionale Momenten-Kalibrierung [P]

Wenn die drei ausgewählten Jahre die aggregierten Statistikmomente des 30er-Ensembles schlecht treffen, ist eine **neue, getrennte** Gewichts-Kalibrierung denkbar. Für vorab gewählte Testmerkmale \(m_i\in\mathbb R^p\):

\[
\bar m=\sum_{i=1}^{30}q_im_i,\quad
M_{\mathcal S}=[m_{s_1}\ m_{s_2}\ m_{s_3}],
\]
\[
\boxed{
\min_{\pi}\ \|M_{\mathcal S}\pi-\bar m\|_W^2
+\rho\|\pi-\pi^{\rm freq}\|_2^2,
\quad \boldsymbol1^\top\pi=1,\quad\pi_k\ge\epsilon.
}
\tag{26}
\]

Dabei sind \(W\succeq0\), \(\rho>0\), \(0\le\epsilon\le 1/3\) **freie, zu begründende wissenschaftliche Designgrößen**. Ein \(\rho\) nahe Null kann die Häufigkeitsgewichte stark verbiegen; bei hohem \(\rho\) bleibt die Lösung näher am empirischen Clusteranteil. Der Momenten-Fit hat lediglich **zwei freie Wahrscheinlichkeitsdimensionen**. Eine beliebig große Zahl statistisch unabhängiger Momente lässt sich deshalb mit drei Gewichten im Allgemeinen **nicht exakt** erhalten.

Die Lösung \(\pi^{\rm cal}\) ist dann ein **Repräsentationsgewicht** und nicht mehr zwingend eine echte geschätzte Wetterwahrscheinlichkeit. Deshalb beide Fälle separat führen: **H2 mit \(\pi^{\rm freq}\)** als Hauptfall und **H2-W mit \(\pi^{\rm cal}\)** nur als sensitivitätsgeprüfte Variante. Kein Umschreiben des veröffentlichten ENTSO-E-Gewichtssatzes.

### 9.3 Identifizierbarkeit und Datenanforderungen

Die Clustergröße allein ist bei gleicher Eingangsmasse definiert. Für alternative probabilistische Ausgangsgewichte \(q_i\) benötigte man **externe Evidenz** über Modellwahrscheinlichkeiten, Abhängigkeiten und Klimaeintrittshäufigkeiten; weder D1.1 noch die hier betrachtete IoSN-Methode liefern hierfür automatisch eine eindeutig bessere Verteilung. Für die Momente-Kalibrierung fehlen zudem a priori \(W\), \(\rho\), \(\epsilon\), der Zielmomentraum und die Validierungsdaten. Diese Unbekannten als Methodenparameter und nicht als bekannte Daten deklarieren.

## 10. Vergleichs-, Abnahme- und Validierungsprotokoll

### 10.1 Fünf Vergleichsarme, gleicher Informationsstand

| Arm | Kandidaten/Jahre | Merkmalsraum | Auswahlverfahren | Jahresgewichte |
|---|---|---|---|---|
| **B0** | 30 → 3 | Original-IoSN 2 PC1 | Original-IoSN K-Means und nächstes Clusterjahr | Offizielle Clusteranteile |
| **F3** | dieselben 30 → 3 | FlexPlan-typische gemeinsame normierte Last-/RES-Jahresmerkmale | K-Means, **deterministische** reale Vertreter | Neue Clusteranteile |
| **H1** | dieselben 30 → 3 | Original-IoSN + physikalische Zusatzmerkmale | Offizielle Cluster fest, physikalische Medoide | **Unveränderte** B0-Gewichte |
| **H2** | dieselben 30 → 3 | kombinierter physikalischer Distanzraum | Exakte 4.060-Kombinationen-Medoids-Auswahl | Neue Clusteranteile |
| **H2-W** | dieselben 30 → 3 | **identische** H2-Jahre | Keine neue Jahreswahl | Zusätzlich kalibrierte Gewichte [P] |

**Keine Scheinkomparabilität:** Ein originales FlexPlan-Fünferclusterexperiment und ein IoSN-Dreierclusterexperiment haben *unterschiedliches Szenariobudget* und dürfen nicht ohne Budgetkorrektur als Algorithmenvergleich gelesen werden. Gleiches gilt für unterschiedliche historische vs. projizierte Klimadatensätze, unterschiedliche installierte Leistungen oder unterschiedliche Lastprofile.

### 10.2 Mittelwerte und **totale** Varianz korrekt ausweisen

Für Variable \(X_i(t)\), innerhalbjährlichen Mittelwert \(\mu_i\), Populationsvarianz \(V_i\) und Jahresgewichte \(q_i\) gilt

\[
\mu_{\rm full}=\sum_iq_i\mu_i,\qquad
V_{\rm full}=\sum_iq_i\bigl[V_i+(\mu_i-\mu_{\rm full})^2\bigr].
\tag{27}
\]

Für die Auswahl entsprechend

\[
\widehat\mu=\sum_{k=1}^{3}\pi_k\mu_{s_k},\quad
\widehat V=\sum_{k=1}^{3}\pi_k\bigl[V_{s_k}+(\mu_{s_k}-\widehat\mu)^2\bigr].
\tag{28}
\]

**Nicht** die gewichteten Standardabweichungen addieren, als wären sie die Gesamtstreuung. Für die räumliche Kovarianz von \(X,Z\) gilt analog

\[
\operatorname{Cov}_{\rm full}(X,Z)=\sum_iq_i\left[
\operatorname{Cov}_t(X_i,Z_i)
+(\mu_{X,i}-\mu_X)(\mu_{Z,i}-\mu_Z)
\right].
\tag{29}
\]

Daraus folgt eine wichtige wissenschaftliche Prüfforderung: Nicht allein regionale Mittelwerte, sondern auch **räumliche gemeinsame Extrembelastungen** und ihre Kovarianz sind gegen alle 30 Jahre zu vergleichen.

### 10.3 Ergänzende statistische Qualitätskennzahlen

Pro Technologie, Region und Zieljahr ausgeben: relativer Mittelwertfehler, Fehler der totalen Standardabweichung, Quantilfehler (5/50/95/99 %), Energiedifferenzen, stärkste Residuallastspitze, Länge des längsten über dem Schwellenwert liegenden Defizitblocks, Länge zusammenhängender niedriger Windverfügbarkeit, saisonale Hydro-Kennzahlen und Fehler regionaler Korrelation. Außerdem die Auswahlverzerrung im *eigenen* Distanzraum sowie **in einem vollständig unabhängigen, nicht zur Auswahl verwendeten Validierungsraum** messen.

Eine minimale normierte Fehlermetrik etwa für Moment \(m\) ist

\[
E_m=\frac{|\widehat m-m_{\rm full}|}{\max(|m_{\rm full}|,s_{\rm phys})},
\tag{30}
\]

wobei \(s_{\rm phys}>0\) ein sinnvoller, **vorab dokumentierter Skalierungsanker** mit derselben Einheit wie \(m\) ist. Ohne Anker führen nahezu verschwindende Referenzwerte zu irreführend großen Prozentfehlern. Ein alleiniger K-Means-Inertia-Vergleich zwischen verschiedenen Feature-/Distanzräumen ist **nicht** aussagekräftig: dessen Zahlen werden durch Skalierung und Dimension verändert.

### 10.4 Energiesystem- und Ausbaukosten als letzte Qualitätsstufe

Eine reduzierte Wetterjahrauswahl wirkt auf das stochastische Investitionsproblem abstrakt durch

\[
x_{\rm red}^*\in\arg\min_x\left[C_{\rm inv}(x)
+\sum_{k=1}^{3}\pi_k Q_Y(x,s_k)\right].
\tag{31}
\]

Mit **fixem** reduzierten Investitionsportfolio kann seine ex-post-Eignung über sämtliche 30 Originaljahre bewertet werden:

\[
J_{30}(x^*_{\rm red})=C_{\rm inv}(x^*_{\rm red})
+\sum_{i=1}^{30}q_iQ_Y(x^*_{\rm red},i).
\tag{32}
\]

Nur wenn zusätzlich das identische 30-Szenarien-Investitionsproblem gelöst ist, ist ein echter Optimierungs-Regret zulässig:

\[
\operatorname{Regret}(\mathcal S)
=J_{30}(x^*_{\rm red})-J_{30}(x^*_{30})\ge0
\tag{33}
\]

bei gleichen zulässigen Entscheidungen und nachweislich optimalen Lösungen. Fehlt \(x^*_{30}\), darf ein anderes Ergebnis **nicht** als exakter Regret bezeichnet werden. Ex-post-Fixed-Investment-Betriebsläufe für alle 30 Jahre sind dann die pragmatische erste Stufe.

Zu untersuchen sind Gesamtinvestitionen, technologiespezifische Erzeugung, Speicherbedarf, Nichtdeckung/ENS, RES-Abregelung, zonale Preisunterschiede und Grenzleitungsbelastung **nur soweit das nachgelagerte Modell sie tatsächlich berechnet**. **Strompreise sind keine FlexPlan-/IoSN-Wetterjahr-Eingangswerte.** Für Preis- oder Kostenprognosen werden gesondert Brennstoffpreise, CO₂-Preise, Wirkungsgrade, OPEX/CAPEX, Lastelastizitäten, Speicherrestriktionen, VoLL und Netz-/Dispatchdaten benötigt. Weder Originaldokument liefert universelle numerische „Preise des Wetterjahres“. Keine Kostenvorteile vor Durchführung dieser Experimente behaupten.

### 10.5 Akzeptanzgrenzen vor der Rechnung festlegen

Vor Ergebnissichtung verbindlich dokumentieren: Welche Größen sind **Primärkriterien**, welche Diagnose? Welche Mindestgüte darf sich gegenüber B0 nicht verschlechtern? Welche Extremregionen und Schwellen \(\tau\) gelten? Welche Fehlernormalisierung, Bootstrap- oder Modelljahr-Sensitivität wird verwendet? Wie werden wechselseitige Zielkonflikte zusammengefasst? **ENTSO-E und FlexPlan schreiben hierfür keinen universellen Akzeptanzschwellenvektor für H1/H2 vor**. Solche Grenzwerte sind ausdrücklich Projektentscheidungen [P].

## 11. Provenienz-/Reproduzierbarkeitsvertrag

### 11.1 Kritische offene Informationen

| ID | Priorität | Fehlende/zu entscheidende Information | Auswirkung |
|---|---|---|---|
| O01 | kritisch | Exakte IoSN-Variabilitäts-/kumulative-Anomalie-Implementierung | B0-PCA, Cluster, alle Hybride |
| O02 | kritisch | Vollständig abrufbare PECD-4.2-Profile **aller 30** Kandidaten für jedes Zieljahr | Alle Methoden |
| O03 | kritisch | **Konsistente jahres- und temperaturabhängige Nachfrage** für alle 30 Kandidaten | Fairer FlexPlan-F3- und H1/H2-Vergleich |
| O04 | hoch | Konkrete IoSN-Merkmalswerte/Regionen/Kapazitäten/Seed/PCA-Loading und 30→3-Zuordnung | B0-Reproduktion und H1 |
| O05 | hoch | Hydro-Eingabeeinheiten, wöchentliche Zeitachsen und Anwendungs-/Umrechnungsregeln | Hydro-Merkmale und statistische Aggregation |
| O06 | hoch | Jahresfenster-Widerspruch zwischen I26 §3.7 und Anhang 6.3 | Kandidatensatz |
| O07 | hoch | Schwellen/Regionen/Features für Extremstress und räumliche Kohärenz | H1/H2 |
| O08 | hoch | Blockgewichte, Distanzskalen, \(W_F,W_H\), Merkmalsdoppelzählungen | Auswahlobjektiv H1/H2 |
| O09 | hoch | Ein vollständiger, konsistenter Netzausbau-/Dispatch-Validierungslauf und Preis-/Kostenparameter | Ökonomische Auswahlgüte |
| O10 | mittel | Konkrete originale 12 FlexPlan-Demo-Merkmale, 35/40-Beispielzuordnung, Daten und Seeds | Historische FlexPlan-Demo-Nachbildung |
| O11 | mittel | Veröffentlichte WS032-Rundung 0,24 trotz 7/30 | Exakte Wahrscheinlichkeitsdarstellung |
| O12 | mittel | Quantilinterpolation, fehlende Werte, Kalender-/Schaltjahrbehandlung, Lastreferenzen | Reproduzierbarkeit |
| O13 | mittel | \(W,\rho,\epsilon\) und Trennung von Auswahl- und Prüfmerkmalen bei H2-W | Gewichtskalibrierung ohne Überanpassung |

### 11.2 Konkrete Gate-Reihenfolge

1. **G0 Provenienz:** Originalquellen, Datenhashes, vollständige Jahre, offizielle WS-/Klimamodell-/Jahr-Zuordnung, Installationsdaten, Einheit und regionaler Mapping-Code gesichert.
2. **G1 Original-B0:** Publizierte 2026-Auswahl numerisch reproduziert **oder** Abweichungen durch konkret belegte Daten-/Definitionslücken markiert. Niemals WS-IDs durch nachträgliches Tuning erzwingen.
3. **G2 Faire Datenbasis:** Identische 30 Kandidaten, volle zeit-/raumkonsistente Last-/Wind-/PV-/Hydro-Inputs und gleiche Zieljahrkapazitäten; keine Residuallast-als-physischer-PTDF-Trick.
4. **G3 F3:** FlexPlan-basierte Verfahren mit \(K=3\), deterministischen realen Jahren und klaren Feature-/Normalisierungsregeln.
5. **G4 H1/H2:** H1 verändert nur Medoide bei fixen B0-Clustern/\(\pi\); H2 prüft alle 4060 Kombinationen bei fixierter Distanz; exakte Wahrscheinlichkeiten, Tie-breaks, Nichtleere.
6. **G5 Statistik:** Unabhängige 30er-Benchmark-Metriken zu Mittelwert, totaler Varianz, Kovarianz, Ereignishöhe/-dauer und regionaler Gleichzeitigkeit.
7. **G6 Ökonomie:** 30er-Fixed-Investment-Test; Vollproblem-Regret nur bei vollständiger Optimierung.
8. **G7 Entscheidung:** Ersetze B0 als Produktionsauswahl **erst nach** festgelegter, numerisch belegter Überlegenheit hinsichtlich der relevanten Kriterien; dokumentiere Verschlechterungen und Grenzen genauso.

### 11.3 Minimal zu exportierende Tabellen

- `input_manifest.csv`: \(Y\), WS-ID, Klimamodell, Klima-Jahr, SSP, PECD-Version, Zonenkonvention, Datum/Hash.
- `features.csv`: genau definierte, Einheit tragende IoSN- und Zusatzmerkmale je Kandidat, Raum, Technologie.
- `feature_transform.json`: Regions-/Kapazitätsgewichte, Z-Score-Parameter, PCA-Ladungen, Seed, \(\alpha,\beta,\gamma\), Distanzskalen, Stressschwellen.
- `distances.csv`: 30×30-Distanzmatrix; unterschiedliche Blöcke getrennt prüfbar.
- `clusters_and_weights.csv`: \(Y\), Methode, WS-ID, Cluster, Repräsentant, \(q_i\), \(n_k\), exaktes \(\pi_k\), gerundetes \(\pi_k\), optional \(\pi_k^{\rm cal}\).
- `year_selection_ranking.csv`: für H2 **alle 4060 Dreiermengen** und Zielwert oder vollständiger, reproduzierbarer Prüfsummenbeleg.
- `validation_metrics.csv` und `validation_review.md`: unabhängige Güte, offene Punkte, statistische und ökonomische Befunde, PASS/FAIL, Entscheidung.

## 12. Fazit und Empfehlung

Die wesentliche zusätzliche FlexPlan-Information ist **nicht** eine andere Formel zur Gewichtung, sondern ein **physikalisch gehaltvollerer Merkmalsraum für ganze korrelierte Jahresprofile**. Die publizierte IoSN-2026-Auswahl sollte deshalb **zunächst als B0 erhalten und exakt als Referenz dokumentiert** bleiben.

- **F3** kontrolliert, ob die FlexPlan-basierte Profil-/Merkmalsrepräsentation bei identischem Dreijahresbudget andere Jahre/Cluster auswählt.
- **H1** ist die **konservative erste Verfeinerung**, denn Cluster und Häufigkeitsgewichte aus IoSN 2026 bleiben unverändert; nur das reale Repräsentantenjahr wird anhand zusätzlicher physikalischer Kennwerte gewählt.
- **H2** ist die **weitreichendere, aber numerisch kleine** Alternativoptimierung: Unter definierten Features und Gewichten ist die Suche über 4060 Dreierkombinationen exakt lösbar und ergibt neue Clusterhäufigkeiten.
- **H2-W** ist lediglich ein optionaler, klar getrennter Test, weil kalibrierte Gewichte keine ursprünglichen empirischen Szenariowahrscheinlichkeiten mehr darstellen.

**Verbindliche wissenschaftliche Feststellung:** Ohne vollständige PECD-/Nachfragedaten und Ergebnisvergleich können keine neuen WS-IDs, keine optimalen H1/H2-Gewichte und keine nachgewiesene Überlegenheit gegenüber IoSN 2026 angegeben werden. Der Bericht liefert eine mathematisch ausführbare **Methodenspezifikation mit offen ausgewiesenen Annahmen**, kein numerisch ausgeführtes Selection-Ranking.

## Quellenverzeichnis – ausschließlich offizielle Projekt-/ENTSO-E-Unterlagen

**[I26]** ENTSO-E (2026), *TYNDP 2026 Identification of System Needs Methodology*, Konsultationsfassung 25.02.2026, §3.7 und Anhang 6.3.  
https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf

**[S26]** ENTSO-E/ENTSOG (2026), *TYNDP 2026 Scenarios Methodology Report*, Juni 2026, Annex III, *Weather Year Selection Methodology*, insbes. Tabellen 33–36 und Prozessstufen 1–5.  
https://2026.entsos-tyndp-scenarios.eu/scenarios-methodology-report/annex-iii-weather-year-selection-methodology/

**[C26]** ENTSO-E/ENTSOG (2026), *TYNDP 2026 Scenarios Consultations Summary Report*, Januar 2026, Annex I, *Possible Improvements to Weather Scenario Selection Methodology*, S. 36–40. **Diskussionsstatus.**  
https://2026-data.entsos-tyndp-scenarios.eu/consultation/entsos_TYNDP2026_Scenarios_Public_consultations_Summary_Report_260108.pdf

**[F20]** FlexPlan Consortium (2020), *D1.1 Monte Carlo Scenario Generation and Reduction*, V1.0, 10.12.2020, §§5.1–5.3 und 6.2.1. Vom Nutzer vorgegebene Primärquelle.  
https://flexplan-project.eu/wp-content/uploads/2020/12/D1.1_20201210_V1.0.pdf

**[H24]** ENTSO-E (2024), *Identification of System Needs Implementation Guidelines*, §8.2 (nur Auswahl ganzer Wetterjahre).  
https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2024/foropinion/SystemNeedsMethodology.pdf

**[H22]** ENTSO-E (2022), *TYNDP 2022 IoSN Implementation Guidelines*, §6.3 (nur Auswahl ganzer Wetterjahre).  
https://eepublicdownloads.blob.core.windows.net/public-cdn-container/tyndp-documents/TYNDP2022/public/IoSN-IG.pdf

**Quellenbeschränkung und Prüfvorgehen:** FlexPlan D1.1 wurde über öffentlich indexierte Textabschnitte des Original-PDFs, insbesondere Seiten 46–53 und 57–62, ausgewertet. Der direkte Komplettdownload der großen Original-PDF war in dieser Sitzung nicht zugänglich. Einzelheiten, die daraus nicht sicher rekonstruiert werden können – insbesondere die präzisen zwölf Demo-Kennwerte –, sind folglich als **[O] offen** ausgewiesen. Das gilt nicht für die ausdrücklich dokumentierte Kernmethode und ihre allgemeinen Auswahl-/Gewichtungsschritte.
