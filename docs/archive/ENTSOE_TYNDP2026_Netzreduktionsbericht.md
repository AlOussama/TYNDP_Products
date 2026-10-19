---
title: "Netzreduktion im ENTSO-E TYNDP 2026"
subtitle: "Wissenschaftlicher Methodikbericht mit mathematischer Rekonstruktion, Spezifikationsprüfung und Anforderungen an Reproduzierbarkeit"
date: "16. Oktober 2026"
lang: de-DE
abstract: |
  Dieser Bericht analysiert die im Entwurf der ENTSO-E-Methodik zur Identification of System Needs (IoSN) für den TYNDP 2026 veröffentlichte zonale Netzreduktion. Ausschließliche Primärquelle ist die Konsultationsfassung vom 25. Februar 2026. Die drei methodisch verschiedenen Schritte der Knotenzonierung, elektrischen Ersatznetzkalibrierung und N-1-orientierten Kapazitätsäquivalenz werden systematisch rekonstruiert. Eine Graphen- und Matrizenformulierung macht die Bilanz- und Maschengleichungen, die Verwendung stündlicher Leistungsflüsse, die strukturellen Nullbilanzflüsse und die Grenzen der Parameteridentifikation präzise nachvollziehbar. Die mathematischen Ergänzungen sind ausdrücklich **keine** von ENTSO-E veröffentlichten Implementierungsgleichungen. Bewertet werden Reproduzierbarkeit, zeitliche Repräsentativität, betriebliche Sicherheitsäquivalenz und Konsequenzen für die europäische Ausbauoptimierung.
keywords:
  - ENTSO-E
  - TYNDP 2026
  - IoSN
  - Zonal Clustering
  - Netzreduktion
  - PTDF
  - LODF
  - N-1
  - DC-Lastfluss
---

\newpage

# Zusammenfassung und zentrale Ergebnisse

Die ENTSO-E definiert für die TYNDP-2026-*Identification of System Needs* (IoSN) ein mehrstufiges zonales Verfahren, in dem das detaillierte europäische Übertragungsnetz zu **102 aggregierten Zonen** verdichtet wird. Netzengpässe und die räumliche Verteilung der Wirkflüsse beeinflussen die Zonengrenzen; die Verbindungen zwischen den Zonen werden anschließend mit optimierten Ersatzimpedanzen, strukturellen Flusskorrekturen und richtungs- sowie jahreszeitspezifischen N-1-Transferkapazitäten ausgestattet. Das resultierende Modell nutzt elektrische Maschengleichungen, nicht bloß voneinander unabhängige Net Transfer Capacities (NTC). [Q1, S. 21–29, 45–51]

**Zentrale Befunde:**

1. **Das Verfahren ist topologisch und zeitlich informiert.** Stundenbasierte detaillierte Leitungsflüsse werden für die Priorisierung überlasteter Betriebsmittel, für eine Stichprobe synchroner Zielflüsse zur Impedanzkalibrierung und für die Schätzung äquivalenter Transferkapazitäten verwendet. Welche Stunden mit welchem Gewicht in die Impedanzoptimierung eingehen, bleibt im Text unbestimmt. [Q1, S. 45, 49–51]
2. **Das reduzierte Netz bildet vor allem Wirkleistungsflüsse in DC-Näherung ab.** Die Quelle bezeichnet das Ergebnis zwar als vereinfachtes AC-Netz, beschreibt die Netzgleichungen aber ausdrücklich in DC-Approximation. Daraus folgt **keine** verifizierte Erhaltung der AC-Spannungs-, Blindleistungs-, Verlust- oder dynamischen Eigenschaften. [Q1, S. 27, 49]
3. **Knotenbilanz und Aggregationsflüsse lassen sich mathematisch exakt erhalten**, wenn die Zuordnung der Originalknoten zu Zonen und die Summation physikalischer Grenzleitungen konsistent gewählt sind. Die Maschengleichungen können dagegen nach räumlicher Aggregation nur angenähert erfüllt werden; dafür werden Ersatzreaktanzen und Nullbilanz-Flusskorrekturen kalibriert. Abschnitt 5 gibt die entsprechende Herleitung.
4. **Die Impedanzidentifikation ist nicht eindeutig.** Selbst in einem reinen linearen DC-Netz lässt sich aus Wirkleistungsflüssen allein der gemeinsame Skalierungsfaktor aller Ersatzreaktanzen nicht bestimmen. Dieser formale Nachweis ergänzt die von ENTSO-E ausdrücklich festgestellte Nicht-Eindeutigkeit infolge interner räumlicher Informationen. Eine Parameternormierung oder zusätzliche Referenz ist nicht veröffentlicht. [Q1, S. 48–49]
5. **Die vier äquivalenten Kapazitäten je Interzonenverbindung sind statistisch aus Betriebszuständen erschlossene N-1-Surrogate**, keine allgemeine Garantie, dass jede beliebige gleichzeitige Zoneneinspeisung und jeder relevante Ausfall sicher bleibt. Ausfallauswahl, Flusskorrelation, verwendete Zeitstichprobe und die Behandlung operativer Gegenmaßnahmen bestimmen die Güte. [Q1, S. 27–28, 47, 50–51]
6. **Die Veröffentlichung ist konzeptionell substanziell, aber kein ausführbares Referenzmodell.** Nicht offengelegt sind unter anderem die vollständige Knoten-Zonen-Matrix, der Kalibrierungsstundenindex, die Zielfunktion und Nebenbedingungen der Impedanzoptimierung, die allgemeine Kapazitäts-Fitfunktion, die Auswahl aller CBCOs und ein unabhängiges Validierungsprotokoll.

**Gesamturteil.** Die Methodik ist als fachliches Rahmenkonzept einer langfristigen zonalen Netzausbauanalyse nachvollziehbar. Ihre Beschreibung reicht jedoch nicht aus, um ein **eindeutig reproduzierbares** mathematisches Netzreduktionsverfahren herzuleiten. Die Gleichungen dieses Berichts liefern eine **konsistente wissenschaftliche Rekonstruktion**, aber keine behauptete Offenlegung des ENTSO-E-internen Algorithmus.

# 1. Untersuchungsgegenstand und Quellenbindung

## 1.1 Einzige Primärquelle

Analysiert wird ausschließlich:

**[Q1]** ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, Version for Public Consultation, **25 February 2026**, 65 Seiten, insbesondere **§ 3.7 (S. 18–21), § 3.8 (S. 21–29), § 3.9 (S. 29), Anhang 6.1 (S. 45–51), Anhang 6.3 (S. 57–62)**. Offizielles Dokument: <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf>.

Die Fassung ist als **öffentlicher Konsultationsentwurf** gekennzeichnet. Dieser Bericht trifft deshalb keine Aussagen über spätere verbindliche Fassungen, interne Quellcodes, reale Kalibrierungsdateien oder nicht im Dokument beschriebene operative Verfahren. Der Anwenderbegriff „AUSN“ wird im Folgenden durch die im Dokument verwendete Bezeichnung **IoSN** präzisiert. Literatur anderer Autoren oder Implementierungsdetails fremder Software werden nicht zur Begründung herangezogen.

## 1.2 Kennzeichnung des epistemischen Status

Die folgende Kennzeichnung verhindert, dass eine plausible mathematische Ergänzung als veröffentlichte ENTSO-E-Regel missverstanden wird:

| Kennzeichnung | Bedeutung |
|:--|:--|
| **[D] Dokumentiert** | Aussage oder Rechenschritt wird in [Q1] ausdrücklich angegeben. |
| **[R] Rekonstruktion** | Mathematisch konsistente Formalisierung eines dokumentierten Prinzips; nicht notwendigerweise die intern verwendete Form. |
| **[A] Analytische Folgerung** | Aus [D]/[R] logisch oder mathematisch hergeleitete Eigenschaft bzw. Grenze. |
| **[E] Ergänzung** | Für eine reproduzierbare oder belastbar validierte Implementierung vorgeschlagene Festlegung; keine ENTSO-E-Vorgabe. |
| **[U] Unbestimmt** | Nicht eindeutig oder nicht vollständig aus [Q1] ableitbar. |

Diese Statusangaben gelten auch für Formeln. **[R] und [E] dürfen nicht als zitierfähige Originalgleichungen der ENTSO-E bezeichnet werden.**

## 1.3 Abgrenzung

Gegenstand sind: (i) Auswahl und Abgrenzung der Zonen, (ii) Ableitung der physikalischen Leistungsflüsse aus Markt- und Netzsimulation, (iii) Reduktion der AC-Übertragungsnetztopologie auf äquivalente Wirkleistungs-Verbindungen, (iv) Parameteridentifikation für Ersatzimpedanzen und Nullbilanzflüsse, (v) Berechnung der äquivalenten N-1-Kapazitäten, (vi) zonale Zuordnung der Erzeugungs-, Last- und Speicherzeitreihen sowie (vii) Verwendung des reduzierten Modells bei der Ausbauplanung. Nicht untersucht werden andere TYNDP-Verfahren außer ihrer unmittelbaren Schnittstelle zur Netzreduktion.

# 2. Daten, Graphen, Indizes und Modellannahmen

## 2.1 Notation

| Symbol | Bedeutung und Dimension |
|:--|:--|
| $G^{\mathrm d}=(V^{\mathrm d},E^{\mathrm d})$ | Detaillierter AC-Netzgraph, $n$ Knoten, $m$ Zweige |
| $A_{\mathrm d}\in\{-1,0,1\}^{n\times m}$ | Orientierte Knoten-Zweig-Inzidenzmatrix |
| $x_{\ell}$, $b_{\ell}=1/x_{\ell}$ | Zweigreaktanz und DC-Suszeptanzparameter in konsistentem p.u.-System |
| $p_t^{\mathrm d}\in\mathbb R^n$ | Nettoeinspeisung der detaillierten AC-Knoten in Stunde $t$ |
| $f_t^{\mathrm d}\in\mathbb R^m$ | Physikalischer Wirkleistungsfluss der detaillierten AC-Zweige |
| $V^{\mathrm z}$, $E^{\mathrm z}$ | Menge der reduzierten Zonen und äquivalenten AC-Verbindungen, $k$ bzw. $r$ Elemente |
| $g:V^{\mathrm d}\to V^{\mathrm z}$ | Abbildung jedes ursprünglichen Knotens auf genau eine Zone |
| $P\in\{0,1\}^{k\times n}$ | Knotenzonen-Zuordnung, $P_{zi}=1\Leftrightarrow g(i)=z$ |
| $\Gamma\in\{-1,0,1\}^{r\times m}$ | Aggregation der physikalischen Grenzleitungsflüsse auf Interzonenverbindungen |
| $A_{\mathrm z}\in\{-1,0,1\}^{k\times r}$ | Inzidenzmatrix des reduzierten Graphen |
| $X=\mathrm{diag}(x_1^{\mathrm{eq}},\ldots,x_r^{\mathrm{eq}})$ | Diagonalmatrix positiver Ersatzreaktanzen |
| $C\in\mathbb R^{r\times(r-k+c)}$ | Zyklenmatrix des reduzierten Graphen mit $c$ Zusammenhangskomponenten |
| $f_t^\star=\Gamma f_t^{\mathrm d}$ | Aus dem Originalnetz aggregierter Zielfluss der Interzonenverbindungen |
| $\widehat f_t$ | Im Ersatznetz berechneter Interzonenfluss |
| $c^0\in\mathbb R^r$ | Struktureller Nullbilanz-Flusskorrekturvektor (Rekonstruktion) |
| $\mathcal S_y$ | Menge der betrachteten Wetter-/Betriebsszenarien für Zieljahr $y$ |
| $\mathcal T_s$, $\mathcal T_s^{\mathrm{cal}}$ | Verfügbare bzw. zur Kalibrierung verwendete Zeitpunkte im Szenario $s$ |
| $\mathcal O$, $\operatorname{LODF}_{\ell o}$ | Betrachtete Ausfälle und Lastflussverteilungsfaktoren infolge Ausfall $o$ |
| $\overline F_{\ell}$ | Thermische oder anderweitig vorgegebene Belastungsgrenze der physikalischen Leitung |
| $K_{e,\sigma,d}$ | Ersatzkapazität der Interzonenverbindung $e$ für Jahreszeit $\sigma$ und Richtung $d$ |

Zur Vermeidung von Einheitenfehlern sind Winkeldifferenzen in Radiant, Flüsse und Einspeisungen in einheitlichen p.u.-Leistungsgrößen oder nach einheitlicher Skalierung in MW zu verwenden. Falls $x$ als Reaktanz in Ohm gegeben ist, müssen Spannungsebene und Leistungsbasis vor der Verwendung in DC-Flussgleichungen festgelegt werden. [E]

## 2.2 Datenherkunft und Zeitskalen [D]

Das Ablaufdiagramm in [Q1, Abb. 4, S. 23] verbindet ein zusammengeführtes physikalisches Netzmodell (*merged grid model*), eine klassische NTC-Marktsimulation, die darauf gestützte PTDF-/Lastflussberechnung, das Clustering, die zwei Parameterverfahren sowie anschließend die zonale Marktsimulation. Die Pan-European Market Modelling Database (PEMMDB) stellt insbesondere Anlagen- und Marktdaten bereit, während die Pan-European Climate Database (PECD) wetterabhängige Profile liefert. Die Datensätze der Wetterauswahl enthalten stündliche Nachfrageschwankungen, Wind- und PV-Kapazitätsfaktoren; Zuflüsse der Wasserkraft liegen laut § 3.7 auf Wochenbasis vor. [Q1, S. 19, 23, 28–29, 33–35]

**Wichtig:** Die Datenebene des Wetter-Szenario-Clusterings (PCA/K-Means im Anhang 6.3) und das **elektrische Knoten-Clustering** nach § 3.8 sind zwei verschiedene Operationen mit anderen Grundgesamtheiten und anderen Zielgrößen.

## 2.3 Detaillierte Leistungsflussgleichungen [R]

Unter einer verlustlosen DC-Lastflussannahme mit konstanten Spannungbeträgen, kleinen Phasenwinkeldifferenzen und nicht verschwindenden Reaktanzen gilt, sofern nicht gesondert modellierte HVDC-/PST-Beiträge als Einspeisungen bzw. Offsets behandelt werden:

$$
A_{\mathrm d}f_t^{\mathrm d}=p_t^{\mathrm d},\qquad
f_t^{\mathrm d}=D_{\mathrm d}A_{\mathrm d}^{\mathsf T}\theta_t^{\mathrm d},
\qquad D_{\mathrm d}=\operatorname{diag}(1/x_{\ell}). \tag{1}
$$

Daraus folgt die Laplace- bzw. Suszeptanzmatrix

$$
L_{\mathrm d}=A_{\mathrm d}D_{\mathrm d}A_{\mathrm d}^{\mathsf T},
\qquad L_{\mathrm d}\theta_t^{\mathrm d}=p_t^{\mathrm d}. \tag{2}
$$

Die Referenzwinkelwahl und die Behandlung mehrerer Zusammenhangskomponenten sind bei einer tatsächlichen Implementation festzulegen. Das Dokument stellt für den Reduktionsschritt explizit die **DC-Approximation** und später die Maschenbedingung dar, schreibt aber keine vollständige nodale Matrixform wie (1)–(2) aus. Deshalb sind (1)–(2) Standardrekonstruktionen der beschriebenen physikalischen Modellklasse, keine wörtlichen ENTSO-E-Gleichungen. [Q1, S. 49]

# 3. Rekonstruierte Prozesskette und Schnittstellen

## 3.1 Methodische Reihenfolge [D]

Abbildung 4 von [Q1] ergibt folgende, teilweise rückgekoppelte Verarbeitung:

1. Ausgangsszenario, PEMMDB, klassisches NTC-Marktmodell und detaillierter zusammengeführter Netzgraph.
2. Marktsimulations-Dispatch und Umrechnung in synchronisierte physikalische Flüsse über PTDF oder ein anderes Lastflusswerkzeug.
3. Kandidaten einer Knoten-Zonen-Partition unter Berücksichtigung der kritischen Leitungen, Flusssynchronität und Zonenanzahl.
4. Kalibrierung der Ersatzimpedanzen und strukturellen Nullbilanzflüsse anhand der Zielflüsse.
5. Bestimmung der äquivalenten Übertragungskapazitäten anhand der physikalischen Leitungen und ihrer N-1-Belastung.
6. Qualitätskontrolle und gegebenenfalls erneute Änderung der Zonengrenzen.
7. Bildung der zonalen Marktdaten, Ergänzung steuerbarer Betriebsmittel und Integration in das physikalisch gekoppelte zonale Markt-/Ausbaumodell.

Die Parameterberechnung wird in Abb. 4 **„für jedes Szenario“** dargestellt. Offen bleibt, welcher Szenariobegriff für alle Teilprozesse verbindlich gilt und ob die **Topologie** ebenfalls neu erzeugt oder nur die **Parameter** pro Szenario neu kalibriert werden. Die Grafik allein definiert keine eindeutige Versions- und Vererbungsregel. [Q1, S. 23]

## 3.2 Zu unterscheidende Ergebnisse

**Strukturelle Ergebnisse:** Zonenzahl, eindeutige Knotenzuordnung, relevante Grenzleitungsbündel und äquivalenter Zonen-Graph.

**Elektrische Parameter:** Pro Verbindung Ersatzimpedanz und struktureller Nullbilanzfluss, resultierende Maschenbeziehungen, HVDC-Einfluss und PST-Wirkbereich.

**Sicherheitsparameter:** N-1-äquivalente Kapazitäten, je Sommer/Winter und positiver/negativer Flussrichtung.

**Datenparameter:** Räumliche Zuordnung der Anlagen, Lasten und Wetterprofile zu den Zonen.

Die sechs explizit benannten Reduktions-Outputs sind: No-Load Flows, Reduced Network Loop Flows, HVDC-Einfluss auf No-Load Flows, Reduced Link Capacities, Reduced Link Impedances und PST-Wirkung in MW. [Q1, § 3.8.3, S. 28]

# 4. Engpassbewertung und Knotenzonierung

## 4.1 Zeitabhängige Priorisierung überlasteter Leitungen [D/R]

ENTSO-E beschreibt für die im Verfahren betrachteten Wetterfälle **stündliche** Flussberechnungen sämtlicher betrachteter 225-kV- und 400-kV-Leitungen. Kritisch ist eine überlastete Leitung. Als Prioritätskriterium dient die *jährliche Überlastungsenergie*: Sie verknüpft Häufigkeit und Überlastungsstärke, statt nur die stärkste Einzelüberlastung oder deren Häufigkeit zu verwenden. [Q1, Anhang 6.1, S. 45]

Eine mathematisch naheliegende Formalisierung [R] lautet für eine Leitung $\ell$ und ein Wetterjahr $s$:

$$
\varepsilon_{\ell,t,s}
  =\max\{0,|f_{\ell,t,s}^{\mathrm d}|-\overline F_{\ell,t,s}\},
\qquad
E_{\ell,s}^{\mathrm{ov}}
  =\sum_{t\in\mathcal T_s}\varepsilon_{\ell,t,s}\,\Delta t_t .\tag{3}
$$

Bei $\Delta t=1\,\mathrm h$ besitzt $E_{\ell,s}^{\mathrm{ov}}$ die Einheit MWh. Für unterschiedliche Wetterjahre ist eine zusätzliche Aggregation möglich, **aber ihre Definition für die Engpassrangfolge ist nicht veröffentlicht**; insbesondere folgt aus den statistischen Wettergewichten der Ausbauoptimierung nicht automatisch, dass dieselben Gewichte in (3) verwendet werden. [U]

**Analytischer Befund [A].** Die Rangfolge nach (3) kann sich von derjenigen nach der stündlichen Maximallast oder der Überlastungshäufigkeit unterscheiden. Tabelle 5 in [Q1, S. 45] illustriert genau diesen Unterschied. Der veröffentlichte Text enthält jedoch keinen absoluten Aufnahmeschwellenwert, kein festes Top-$N$ und keine mathematisch spezifizierte Mehrwetterjahr-Aggregation. [U]

## 4.2 Partitionierung der Originalknoten [R]

Eine zonale Partition lässt sich durch die binäre Matrix $P$ beschreiben:

$$
P_{zi}\in\{0,1\},\qquad
\sum_{z\in V^{\mathrm z}}P_{zi}=1
\quad\forall i\in V^{\mathrm d}.\tag{4}
$$

Zusätzlich fordert die dokumentierte Methodik eine innerhalb jeder Zone **zusammenhängende Netztopologie** und strebt ungefähr ausgewogene Zonengrößen an. Dies ist wichtig: Eine rein geografische Nachbarschaft oder ein gemeinsames Bietzonenetikett genügt nicht, wenn im elektrischen Graphen keine Verbindung innerhalb der Zone besteht. [Q1, S. 24]

Die publizierten Clustering-Ziele lauten [D]:

- kritische oder grenzüberschreitend sensitive Betriebsmittel möglichst als Interzonenverbindungen sichtbar halten;
- Leitungen mit ähnlichem Verhalten bzw. **synchronen, gleichgerichteten Flüssen** gemeinsam aggregieren;
- Zahl der Zonen begrenzen und ein rechnerisch handhabbares Modell erhalten;
- elektrische Zusammenhängigkeit, angemessene Zonengröße und, soweit möglich, Übereinstimmung mit PECD-Räumen berücksichtigen.

Für den betrachteten Studienansatz nennt [Q1, Tabelle 3, S. 26–27] **102 Zonen**, darunter **Deutschland 11**, **Frankreich 16**, **Spanien 10**, **Italien 7** und **Niederlande 5**. Diese veröffentlichte Zonenzahl ist eine Erfahrungskalibrierung beziehungsweise ein Kompromiss; es wird **kein** vollständiges kombinatorisches Optimierungsmodell veröffentlicht, das exakt diese Partition erzeugt.

## 4.3 Flusssynchronität und Vorzeichenkompensation [A]

Seien zwei physikalische Grenzleitungen $\ell_1,\ell_2$ zu einer einzigen äquivalenten Verbindung zusammengefasst. Für gemeinsam gewählte Orientierung gilt

$$
f_{e,t}^{\star}=f_{\ell_1,t}^{\mathrm d}+f_{\ell_2,t}^{\mathrm d}.\tag{5}
$$

**Rein hypothetisches Beispiel:** $f_{\ell_1,t}^{\mathrm d}=250\,\mathrm{MW}$ und $f_{\ell_2,t}^{\mathrm d}=-240\,\mathrm{MW}$ führen zu nur $10\,\mathrm{MW}$ Netto-Grenzfluss, obwohl beide Leitungen sehr hoch belastet sein können. Weder eine sehr kleine äquivalente thermische Grenze noch eine robuste Ersatzimpedanz folgt daraus. Die Gefahr einer solchen künstlichen Kompensation wird in [Q1, S. 23–24] ausdrücklich genannt.

**Wissenschaftliche Folgerung:** Eine Flusskorrelation ist hier kein nebensächlicher Statistikindikator, sondern kann die strukturelle Identifizierbarkeit und die Qualität der gesamten äquivalenten Verbindung bestimmen. Ein eindeutiger Korrelationskoeffizient, Schwellenwert oder Optimierungsgewicht ist jedoch nicht angegeben. [U]

## 4.4 Als Vorschlag formulierte Multikriterien-Spezifikation [E]

Zur systematischen Reproduktion könnte eine Partition $P$ beispielsweise als Lösung eines Problems der Art

$$
\min_{P\in\mathcal P_{\mathrm{conn}}}
\ \lambda_1 J_{\mathrm{flow}}(P)
+\lambda_2 J_{\mathrm{hidden\ bottlenecks}}(P)
+\lambda_3 J_{\mathrm{size}}(P)
+\lambda_4 |V^{\mathrm z}|,\tag{6}
$$

mit zulässigen elektrisch zusammenhängenden Partitionen $\mathcal P_{\mathrm{conn}}$ beschrieben werden. Dies ist **ausdrücklich nicht** das von ENTSO-E offengelegte Clustering-Modell: Weder die Funktionen $J_\cdot$ noch die Gewichte $\lambda_\cdot$ werden in der Quelle vollständig spezifiziert. Gleichung (6) dient ausschließlich dazu, die mathematisch zu schließenden Entscheidungsfreiheiten sichtbar zu machen.

# 5. Exakte Bilanzaggregation und Verlust elektrischer Detailinformation

## 5.1 Aggregationsmatrix für Grenzleitungsflüsse [R]

Jedem Element $e\in E^{\mathrm z}$ wird eine feste Richtung $z_a\to z_b$ zugewiesen. Jede Originalleitung $\ell=(i,j)$ wird für $g(i)\neq g(j)$ der entsprechenden Zonengrenze zugeordnet; innerhalb einer Zone liegende Leitungen tragen in $\Gamma$ keine Einträge. Für physikalisch zueinander passende Richtungen gilt $\Gamma_{e\ell}=+1$, im Gegenfall $-1$.

Damit ist der **Zielfluss** des reduzierten Netzes

$$
f_t^\star=\Gamma f_t^{\mathrm d}.\tag{7}
$$

Physikalisch bedeutet dies die vorzeichenrichtige **Summe** der Detailflüsse aller Leitungen zwischen demselben Zonenpaar. Die Summe von **Nettoflüssen** in (7) ist nicht zu verwechseln mit der **Addition thermischer Grenzen**, die ausdrücklich keine allgemein gültige Ersatzkapazität ergibt. [Q1, S. 27, 50]

## 5.2 Satz zur Bilanztreue der topologischen Aggregation [A]

Unter der Annahme, dass sämtliche betrachteten AC-Grenzleitungen in $\Gamma$ enthalten sind und jeder Originalknoten genau einer Zone angehört, gilt die strukturelle Matrixidentität

$$
\boxed{A_{\mathrm z}\Gamma=P A_{\mathrm d}.}\tag{8}
$$

**Beweis.** Für jede innerhalb einer Zone liegende Originalleitung besitzen deren zwei Inzidenzeinträge nach Multiplikation mit $P$ dieselbe Zonenzeile und heben sich auf; zugleich ist die zugehörige Spalte von $\Gamma$ null. Für eine zonenüberschreitende Originalleitung ergibt $P A_{\mathrm d}$ genau einen positiven und einen negativen Eintrag in den durchlaufenen Zonen. Die Orientierung von $\Gamma$ reproduziert dieselben beiden Einträge in $A_{\mathrm z}\Gamma$. Da dies spaltenweise gilt, folgt (8). $\square$

Mit (1), (7) und (8) folgt

$$
\boxed{A_{\mathrm z}f_t^\star
=A_{\mathrm z}\Gamma f_t^{\mathrm d}
=P A_{\mathrm d}f_t^{\mathrm d}
=Pp_t^{\mathrm d}=:p_t^{\mathrm z}.}\tag{9}
$$

**Interpretation:** Wenn Verluste und separat modellierte Betriebsmittel konsistent behandelt werden, kann die **summierte Knotenbilanz** exakt erhalten bleiben. Daraus folgt jedoch **nicht**, dass die zonalen Flüsse $f_t^\star$ unter irgendeinem einzigen Satz positiver Ersatzreaktanzen die Maschengleichungen erfüllen. Genau dieser zweite Teil ist das Gegenstück zur parametrischen Netzreduktion.

## 5.3 Konsequenz für die Modellidentität [A]

Die topologische Aggregation ist somit eine **konservative Projektion der Knotenbilanzen**, aber keine allgemeine verlustfreie Projektion der elektrischen Zustandsbeziehungen. Die Originalzustände $\theta_t^{\mathrm d}$ enthalten räumliche Winkelunterschiede innerhalb einer Zone, die im Modell mit nur einem Zonenwinkel verschwinden.

Die Aussage [Q1, S. 27], mit dem zonalen Kupferplattenmodell träten *keine intrazonalen Engpässe auf*, ist eine Aussage über **nicht vorhandene explizite interne Beschränkungen im reduzierten Modell**; sie beweist nicht, dass diese Engpässe im ursprünglichen Netz physikalisch verschwinden.

# 6. PTDF-Verfahren und Verwendung stündlicher Zeitreihen

## 6.1 Herkunft der Synchronfluss-Stichprobe [D]

Im Anhang [Q1, S. 49] wird die Referenzdatenbildung wie folgt beschrieben: Eine klassische Marktsimulation mit NTC-Austauschbedingungen liefert zeitliche Ergebnisse. Für wichtige ausgewählte Marktparameter werden finite Änderungen vorgenommen und neue **DC-Lastflussrechnungen** durchgeführt. Aus den Differenzen entstehen Empfindlichkeiten; mit ihnen werden für jede Stunde die Leitungsflüsse des detaillierten Netzes approximiert.

Die im Quelltext ausdrücklich abgedruckte Gleichung besitzt die Struktur

$$
f_{\ell,t}^{\mathrm d}
=f_{\ell,\mathrm{ref}}^{\mathrm d}
+\sum_{q\in\mathcal Q}
\mathrm{PTDF}_{q\ell}
\left(u_{q,t}-u_{q,\mathrm{ref}}\right),\tag{10}
$$

wobei $u_{q,t}$ ausgewählte Marktparameter und $\mathcal Q$ ihre Menge bezeichnet. Die genaue Bedeutung sämtlicher $q$ wird im Dokument nicht vollständig definiert. Deshalb wird hier bewusst **nicht** unterstellt, die Spalten seien zwingend einzelne Knotenleistungsinjektionen.

## 6.2 Finite-Differenzen-Interpretation [R]

Eine konsistente Interpretation der beschriebenen Sensitivitätsbildung ist

$$
H_{\ell q}
\approx\frac{f_\ell(u^{\mathrm{ref}}+\delta_q e_q)
-f_\ell(u^{\mathrm{ref}})}{\delta_q},\qquad
f_{\ell,t}^{\mathrm d}
\approx f_{\ell,\mathrm{ref}}^{\mathrm d}
+\sum_q H_{\ell q}(u_{q,t}-u_{q,\mathrm{ref}}).\tag{11}
$$

Die Größe $\delta_q$ und die jeweils erforderliche Rebalancierung der Einspeisungen im Lastfluss sind **nicht** spezifiziert. Werden nodale Ein- und Ausspeisungen verwendet, kann im konventionellen DC-Modell die lineare Flussabbildung als

$$
f_t^{\mathrm d}=D_{\mathrm d}A_{\mathrm d}^{\mathsf T}
L_{\mathrm d}^{+}p_t^{\mathrm d},\tag{12}
$$

geschrieben werden, wobei $L_{\mathrm d}^{+}$ die Moore-Penrose-Pseudoinverse auf dem zulässigen bilanzierten Einspeisungsraum bezeichnet. Gleichung (12) ist eine **mathematische Rekonstruktion** und weder die allein mögliche PTDF-Definition noch eine als ENTSO-E-intern belegte Implementierung. Sie setzt bilanzierten Dispatch und ein konsistentes Referenzsystem voraus.

## 6.3 Wann und wo werden Zeitreihen benötigt?

| Verfahrensstufe | Zeitliche Datenverwendung | Spezifikationslage |
|:--|:--|:--|
| Engpasspriorisierung | Stündliche Leitungsflüsse und jährliche Summe der Überlastungsenergie | **[D]** Stundenweise Auswertung; Szenarioaggregation **[U]** |
| Impedanzkalibrierung | Stichprobe *synchroner* physikalischer Flussvektoren $f_t^\star$ | **[D]** Datenart; Stundenauswahl, Gewichtung und Umfang **[U]** |
| N-1-Kapazitätsschätzung | Stündliche Paare aus Grenzfluss und maximalem N-1-Belastungsgrad | **[D]** Prinzip; allgemeiner Fit **[U]** |
| Marktmodell nach Reduktion | Zeitreihen für Nachfrage, Wind, PV, Wasserkraft und Anlagen-Dispatch auf zonaler Ebene | **[D]** Grundprozess; exakte Allokationsschlüssel **[U]** |
| Wetter-Szenarioauswahl | Repräsentative Klima-Jahr-Kombinationen aus 30 Kandidaten je Studienzieljahr | **[D]**; keine automatisch belegte Gleichheit mit Kalibrierungsstunden |

Die Formulierung *synchronous flows* ist entscheidend: Die Zielvektoren müssen denselben Zeitpunkt und dieselbe simultane räumliche Einspeisesituation repräsentieren. Würden die Zielflüsse für jede Interzonenverbindung aus unterschiedlichen Stunden zusammengesetzt, könnten sie die nach (9) notwendigen Knotenbilanzen im Allgemeinen verletzen. [A]

## 6.4 Wetterjahre, Gewichte und Gültigkeit [D/U]

Für die **übergeordnete** IoSN-Ausbauoptimierung werden je Zieljahr drei repräsentative Wetterszenarien mit folgenden Gewichten veröffentlicht [Q1, § 3.7, S. 20]:

| Zieljahr | Repräsentative Szenarien | Wahrscheinlichkeits-/Szenariogewichte |
|:--|:--|:--|
| 2035 | WS032, WS037, WS059 | 0,24; 0,43; 0,33 |
| 2040 | WS065, WS071, WS077 | 0,20; 0,40; 0,40 |
| 2050 | WS091, WS092, WS106 | 0,23; 0,57; 0,20 |

Die Auswahl wird mithilfe statistischer Normalisierung, Hauptkomponentenanalyse (PCA) und K-Means-Clustering beschrieben [Q1, Anhang 6.3]. **Unzulässiger Kurzschluss:** Aus der Rolle dieser Gewichte in der stochastisch/robust formulierten Ausbauoptimierung folgt **nicht**, dass exakt diese Gewichte auch die Kalibrierungszielfunktion der Ersatzimpedanzen definieren. Das müsste separat spezifiziert sein. [U]

Ein konkreter redaktioneller Widerspruch betrifft die Wetterjahr-Fenster: § 3.7 nennt etwa für das Zieljahr 2035 **2030–2039**, während Anhang 6.3.1 **2031–2040** festhält. Entsprechende Verschiebungen finden sich auch für 2040 und 2050 [Q1, S. 19 und 58]. Ohne eine Entscheidung über den maßgeblichen Zeitindex ist der exakte Auswahlpool aus dem Dokument nicht widerspruchsfrei rekonstruierbar.

## 6.5 Hypothetische Gewichtung einer Impedanzkalibrierung [E]

Für eine reproduzierbare Umsetzung könnte man einen bekannten Index $\mathcal S$, stündliche Mengen $\mathcal T_s^{\mathrm{cal}}$ und normierte positive Gewichte $\omega_{s,t}$ verwenden:

$$
\omega_{s,t}\ge0,\qquad
\sum_s\sum_{t\in\mathcal T_s^{\mathrm{cal}}}\omega_{s,t}=1.\tag{13}
$$

Damit lässt sich festlegen, ob typische Stunden, Extremstunden und Szenarien gleichmäßig oder zielbezogen gewichtet werden. **Die konkreten $\omega_{s,t}$ gehören nicht zur veröffentlichten ENTSO-E-Spezifikation.** Derartige zusätzliche Festlegungen können die gewonnenen Ersatzreaktanzen und Flusskorrekturen materiell verändern.

# 7. Elektrische Reduktion: Ersatzreaktanzen und strukturelle Flusskorrekturen

## 7.1 Von der Impedanz zur Ersatznetz-Admittanz [D/R]

Der Anhang bezeichnet die Konstruktion einer **Admittanzmatrix für das reduzierte System** als Basis der Bestimmung äquivalenter Impedanzen. Dabei werden die äquivalenten Reaktanzen **und** initiale bzw. strukturelle Flusskorrekturen so angepasst, dass prognostizierte Interzonenflüsse möglichst gut mit den aus dem detaillierten Netz gewonnenen Zielflüssen übereinstimmen. [Q1, S. 27, 48–49]

Mit $X=\operatorname{diag}(x_1^{\mathrm{eq}},\dots,x_r^{\mathrm{eq}})$ und $B=X^{-1}$ lautet die reduzierte gewichtete Laplace-Matrix [R]

$$
L_{\mathrm z}(X)=A_{\mathrm z}B A_{\mathrm z}^{\mathsf T}.\tag{14}
$$

Für einen nicht zusammenhängenden reduzierten Graphen erfolgt die Referenzwinkel- und Bilanzbehandlung getrennt je Zusammenhangskomponente. Positive Ersatzreaktanzen halten die (rein induktive) DC-Admittanz interpretierbar. Welche Vorzeichen- oder Wertebereiche die ENTSO-E-Optimierung tatsächlich erzwingt, wird im untersuchten Dokument **nicht** vollständig offengelegt. [U]

## 7.2 Knoten- und Maschenbedingungen [D/R]

Ohne zusätzliche Flusskorrekturen wäre eine übliche Netzbeschreibung

$$
A_{\mathrm z}\widehat f_t=p_t^{\mathrm z},\qquad
\widehat f_t=B A_{\mathrm z}^{\mathsf T}\widehat\theta_t.\tag{15}
$$

Sei $C$ eine Basis des Zyklenraums $\ker A_{\mathrm z}$. Bei einem zusammenhängenden reduzierten Graphen besitzt der Zyklenraum die Dimension $r-k+1$. Aus $X\widehat f_t=A_{\mathrm z}^{\mathsf T}\widehat\theta_t$ folgt die Maschengleichung

$$
\boxed{C^{\mathsf T}X\widehat f_t=0.}\tag{16}
$$

ENTSO-E druckt ausdrücklich die entsprechende Regel „Summe aus Impedanz mal Fluss je Masche gleich null“ als lineare Nebenbedingung in der DC-Approximation ab [Q1, S. 49]. Die Matrixschreibweise (16) ergänzt nur die Wahl einer konsistenten Maschenorientierung und eines unabhängigen Zyklensatzes. Das Kirchhoffsche Knotenstrom-/Leistungsbilanzgesetz wird in der Quelle als bereits respektiert bezeichnet. [Q1, S. 27]

## 7.3 Nullbilanz-Flusskorrekturen: präzise Interpretation [D/R]

Der Anhang verlangt pro äquivalenter Verbindung einen **Initial- bzw. Strukturflusskorrekturparameter**. Begründung: Nach der Aggregation kann eine Zone netto ausgeglichen sein, obwohl räumlich getrennte Erzeuger und Lasten zu physikalischen Austausch- oder Kreisflüssen beitragen. Ferner werden im Output „No-Load Flows“ bei **null Austausch zwischen Zonen** ausgewiesen. [Q1, S. 28 und 48]

Eine in sich konsistente Rekonstruktion ist der additive Ansatz

$$
\boxed{\widehat f_t
   = B A_{\mathrm z}^{\mathsf T}\widehat\theta_t+c^0,}
\qquad A_{\mathrm z}c^0=0.\tag{17}
$$

Die Zusatzbedingung $A_{\mathrm z}c^0=0$ ist keine wörtlich publizierte ENTSO-E-Gleichung, sondern die notwendige **Bilanzbedingung**, wenn $c^0$ bei null Zonen-Nettoeinspeisung als stationärer Nullbilanzfluss auftreten und die zonale Knotenbilanz unverändert bleiben soll. In einem zusammenhängenden System kann $c^0$ daher als $c^0=C\eta$ für geeignete Kreisflusskoeffizienten $\eta$ parametrisiert werden. [R]

Für (17) folgt

$$
A_{\mathrm z}\widehat f_t=p_t^{\mathrm z}
\quad\Longleftrightarrow\quad
L_{\mathrm z}\widehat\theta_t=p_t^{\mathrm z}
\quad\text{(unter }A_{\mathrm z}c^0=0\text{)},\tag{18}
$$

und die zugehörige modifizierte Maschenbeziehung lautet

$$
\boxed{C^{\mathsf T}X(\widehat f_t-c^0)=0.}\tag{19}
$$

**Wichtige Spezifikationslücke [U].** Die Quelle stellt einerseits die unmodifizierte Maschengleichung (16), andererseits strukturelle Flusskorrekturen und Nullbilanz-Flüsse dar. Sie führt keine gemeinsame, vollständige Gleichung für **beide** Elemente auf. (17)–(19) sind eine fachlich konsistente Modellvariante, jedoch keine belegte Implementierungsentscheidung. Alternativ könnte eine interne Software Offsets auf anderen Variablenebenen realisieren.

**Konsequenz:** Für einen reduzierten **Baumgraphen** ohne Zyklus und ohne gesonderte äußere Einspeisungen ist $\ker A_{\mathrm z}=\{0\}$; daher muss ein bilanzerhaltender Nullbilanzfluss $c^0$ in (17) verschwinden. Nur bei vorhandenen Zyklen können nichttriviale stationäre Kreisflusskorrekturen auftreten. [A]

## 7.4 Mathematisch mögliche Flussabbildung mit Nullbilanz-Offset [R]

Unter dem Modell (17) und der bilanzierten Einspeisung $p_t^{\mathrm z}$ ergibt sich

$$
\widehat f_t(X,c^0)
=B A_{\mathrm z}^{\mathsf T}
\bigl(A_{\mathrm z}BA_{\mathrm z}^{\mathsf T}\bigr)^{+}
 p_t^{\mathrm z}+c^0.\tag{20}
$$

Die Pseudoinverse in (20) ist mit der Wahl von Referenzwinkeln sowie der Behandlung möglicherweise getrennter Netzkomponenten konsistent zu verwenden. Alternativ lässt sich das lineare Gleichungssystem ohne explizite Pseudoinversen durch Fixieren eines Referenzwinkels je Zusammenhangskomponente lösen.

Der veröffentlichte Wortlaut legt nicht fest, ob $c^0$ über Wetterjahre unverändert ist, ob mehrere Szenario-Offsets $c_s^0$ identifiziert werden oder ob interne Anlagenverteilungen in den zeitlichen Offsets variieren dürfen. Abbildung 4 nennt Ergebnisse je Szenario, spezifiziert diese Indexierung aber nicht. [U]

## 7.5 Rekonstruierbare Zielfunktion der Parameteridentifikation [R/E]

Eine zu der beschriebenen Minimierung des Flussfehlers passende **mögliche** Optimierungsaufgabe ist

$$
\begin{aligned}
\underset{X,c^0,\{\widehat\theta_t\}}{\operatorname{minimize}}
\quad &\sum_{s\in\mathcal S}\sum_{t\in\mathcal T_s^{\mathrm{cal}}}
\omega_{s,t}
\left\|W_{s,t}^{1/2}
(\widehat f_{s,t}-f_{s,t}^\star)\right\|_2^2,\\
\text{unter}\quad
&\widehat f_{s,t}=X^{-1}A_{\mathrm z}^{\mathsf T}\widehat\theta_{s,t}+c^0,\\
&A_{\mathrm z}\widehat f_{s,t}=Pp_{s,t}^{\mathrm d},\\
&A_{\mathrm z}c^0=0,\qquad x_e^{\mathrm{eq}}>0\quad\forall e.
\end{aligned}\tag{21}
$$

$W_{s,t}$ ist eine positive semidefinite Gewichtungsmatrix der Interzonenverbindungen. Gleichung (21) erläutert, welche Bestandteile eine Implementierung haben *könnte*. Sie ist **nicht** die von ENTSO-E veröffentlichte Zielfunktion; in [Q1] fehlen gerade die Entscheidung über den Fehlerterm (Quadrat-/Absolutfehler oder andere Form), $W_{s,t}$, $\omega_{s,t}$, die Parametergrenzen und die methodische Behandlung von Mehrdeutigkeiten. [Q1, S. 27 und 48–49]

Eine weitere optionale Stabilisierung [E] wäre

$$
J_{\mathrm{reg}}(X,c^0)
=\lambda_x\|\log x-\log x^{\mathrm{ref}}\|_2^2
+\lambda_c\|c^0\|_2^2.\tag{22}
$$

Diese Form fordert eine externe Referenz $x^{\mathrm{ref}}$ und eigene Hyperparameter; **keines** dieser Elemente wird im Methodikdokument als verbindlich angegeben.

## 7.6 Formale Nichtidentifizierbarkeit aller Impedanz-Skalierungen [A]

**Satz.** Unter dem DC-Modell (15) bleibt die Abbildung von bilanzierten Einspeisungen zu Leitungsflüssen unverändert, wenn **sämtliche** Reaktanzen einer zusammenhängenden reduzierten AC-Komponente durch denselben positiven Faktor $\alpha$ multipliziert werden.

**Beweis.** Setze $X'=\alpha X$, somit $B'=X'^{-1}=B/\alpha$ und

$$
L_{\mathrm z}'=A_{\mathrm z}B'A_{\mathrm z}^{\mathsf T}
=\frac{1}{\alpha}L_{\mathrm z}.\tag{23}
$$

Für ein gegebenes bilanziertes $p$ kann der zu $X$ gehörige Winkelvektor $\widehat\theta$ durch $\widehat\theta'=\alpha\widehat\theta$ ersetzt werden. Dann gilt

$$
B'A_{\mathrm z}^{\mathsf T}\widehat\theta'
=\frac{B}{\alpha}A_{\mathrm z}^{\mathsf T}
 (\alpha\widehat\theta)
=BA_{\mathrm z}^{\mathsf T}\widehat\theta
=\widehat f.\tag{24}
$$

Damit sind sämtliche Wirkleistungsflüsse und ihre quadratischen Fitfehler identisch. $\square$

**Bedeutung:** Selbst eine vollständige stündliche Zeitreihe fehlerfreier Fluss- und Einspeisungsdaten identifiziert den *absoluten gemeinsamen Maßstab* der Reaktanzen nicht. Zusätzliche Nicht-Eindeutigkeiten können aus den Zone-internen Freiheitsgraden und den Korrekturoffsets entstehen. Ohne Fixierung einer Referenzreaktanz, einer Normierung oder einer physikalisch begründeten Regularisierung ist das Parameterset deshalb nicht eindeutig. Aus [Q1, S. 48–49] lässt sich keine solche Normalisierungsregel entnehmen. [U]

Dies ist kein bloß numerisches Solversymptom, sondern eine **strukturelle Symmetrie** der zugrunde gelegten Flussgleichungen. Sie berührt die Reproduzierbarkeit der numerischen Impedanzwerte, nicht unmittelbar die Möglichkeit einer guten Flussapproximation.

## 7.7 Einfluss von HVDC und PST [D/U]

Zur robusteren Ermittlung des passiven AC-Impedanznetzes sollen die Sollwerte interner HVDC-Verbindungen auf **null** und die Phasenschiebertransformatoren (PST) in **Neutralstellung** gesetzt werden. [Q1, S. 49]

Die Reduktions-Outputs nennen anschließend explizit (i) den **Einfluss von HVDC-Systemen auf Nullbilanzflüsse** und (ii) die durch PST erreichbaren **Wirkleistungsanpassungen in MW**. [Q1, S. 28] Das Dokument formuliert aber keine vollständigen HVDC-/PST-Sensitivitätsmatrizen oder die Kopplung ihrer Stellgrößen an (17)–(19).

Eine mögliche, noch zu qualifizierende Erweiterung wäre [E]

$$
A_{\mathrm z}\widehat f_t=p_t^{\mathrm z}+D_{\mathrm{dc}}h_t,
\qquad
\widehat f_t=B(A_{\mathrm z}^{\mathsf T}\widehat\theta_t-\psi_t)+c^0,
\tag{25}
$$

mit HVDC-Terminal-Injektionen $D_{\mathrm{dc}}h_t$ und PST-Phasenverschiebungen $\psi_t$. Dies darf **nicht** als Originalimplementierung interpretiert werden; insbesondere ist die von ENTSO-E ausgegebene PST-Leistungsfähigkeit keine eindeutig spezifizierte Umrechnung zu $\psi_t$.

# 8. Äquivalente Übertragungskapazitäten unter N-1

## 8.1 Begriff und physikalische Bedeutung [D]

Die Ersatzkapazität einer reduzierten Verbindung wird nicht aus der Summe ursprünglicher Leitungskapazitäten gebildet. Die physikalischen Leitungen zwischen zwei Zonen, deren synchronisierte Flüsse sowie **LODF**-basierte Lastflussänderungen unter Leitungsausfällen bestimmen, welcher Gesamtfluss noch mit dem N-1-Sicherheitskriterium vereinbar ist. [Q1, S. 27 und 50]

Pro Verbindung werden vier Werte berichtet:

$$
\bigl(K_{e,\sigma,d}\bigr)_{\sigma\in\{\mathrm{Sommer},\mathrm{Winter}\},\;d\in\{+,-\}}.\tag{26}
$$

Der Text verwendet „direct“ und „indirect“ beziehungsweise beide Transport-Richtungen; das Vorzeichen in (26) ist lediglich eine formal festgelegte Orientierung. Die saisonalen Definitionen und die Details physikalischer thermischer Grenzwerte sind nicht in einer vollständigen Datenschnittstelle spezifiziert. [U]

## 8.2 LODF-Abbildung eines Einzelausfalls [R]

Für eine intakte Leitung $\ell\ne o$ und den Ausfall $o$ lautet die übliche lineare Abbildung [R]:

$$
f_{\ell,t}^{(o)}
\approx f_{\ell,t}^{\mathrm d}
+\operatorname{LODF}_{\ell o}f_{o,t}^{\mathrm d}.
\tag{27}
$$

Der Ausfallzweig $o$ selbst wird nach dem Ausfall nicht als verbleibender Strompfad bewertet. Die Berechnung von $\operatorname{LODF}_{\ell o}$ setzt eine definierte Referenztopologie voraus; sogenannte Inselungsfälle benötigen eine Sonderbehandlung. [E] Die ENTSO-E-Quelle nennt LODFs als Methode, spezifiziert aber weder alle Kontingenzen noch deren numerische Auswahlregeln. [U]

Für ein physikalisches Leitungsbündel $E_e\subset E^{\mathrm d}$ der reduzierten Verbindung $e$ lässt sich die maximale verbleibende N-1-Auslastung schematisch darstellen als

$$
\rho_{e,t}^{N-1}
=\max_{\substack{\ell\in E_e,\;o\in\mathcal O_e\\\ell\neq o}}
\frac{|f_{\ell,t}^{(o)}|}{\overline F_{\ell,\sigma(t)}}.
\tag{28}
$$

Diese mathematische Konstruktion entspricht dem beschriebenen Konzept „höchste Belastung eines betroffenen Stromkreises unter N-1“, ist aber **keine** veröffentlichte vollständige Festlegung der Menge $\mathcal O_e$. Genau diese Menge kann auch sogenannte *critical branch–critical outage*-Paare (CBCO) und betriebliche Ausschlüsse reflektieren. [Q1, S. 47]

## 8.3 Zusammenhang zwischen Zonengrenzfluss und Sicherheitsauslastung [D/R]

Für jede Stunde wird der physikalisch aggregierte Grenzfluss

$$
q_{e,t}=\left|\sum_{\ell\in E_e}
\gamma_{e\ell} f_{\ell,t}^{\mathrm d}\right|
=|f_{e,t}^\star|\tag{29}
$$

mit der höchsten N-1-Belastung aus (28) gekoppelt. Die resultierenden Datenpaare $(q_{e,t},\rho_{e,t}^{N-1})$ werden nach **Sommer/Winter** und **Flussrichtung** getrennt und auf ausreichende Datendichte **um 100 %** geprüft. Die äquivalente Kapazität ist der Gesamtfluss am Schnittpunkt mit der Belastung $\rho=1$. [Q1, S. 50]

Ohne eine nicht veröffentlichte Vorschrift zu erfinden, lässt sich die Datenkalibrierung allgemein als Schätzfunktion $\widehat h_{e,\sigma,d}(q)$ notieren:

$$
\boxed{\widehat h_{e,\sigma,d}
(K_{e,\sigma,d})=1.}\tag{30}
$$

**[U] Entscheidend:** Die Quelle gibt **keine allgemeine eindeutige Form von $\widehat h$** an (Regressionstyp, Gewichtung, Intervall um 100 %, Umgang mit Ausreißern oder Gütemaß). Sie erwähnt lediglich, dass in einem **besonderen** Extremfall eine Gerade durch den Ursprung und den Mittelwert der Daten gelegt und bei 100 % geschnitten wird. Diese Sonderregel darf nicht auf alle Fälle verallgemeinert werden. [Q1, S. 51]

## 8.4 Veröffentlichte Sonderregeln [D]

| Beobachtung | In [Q1, S. 51] beschriebene Behandlung | Interpretation |
|:--|:--|:--|
| In mehr als **99,5 %** der Stunden Fluss nur in einer Richtung | Für die unbeobachtete Gegenrichtung wird die Kapazität der dominanten Richtung übernommen. | Ersatzannahme, kein separat validierter Richtungswert |
| Zu wenige Datenpunkte mit Auslastung **> 1 %** | Es wird **kein** Kapazitätswert berechnet. | Unzureichende Informationslage |
| Mehr als **99,5 %** der Datenpunkte über **130 %** Auslastung | Gerade durch Ursprung und Datenmittelwert; Schnitt mit **100 %**. | Nur expliziter Spezialfall |
| Starke Streuung, kein klarer Zusammenhang zwischen Gesamtfluss und kritischer Auslastung | Kapazität kann berechnet werden; Vorsicht bei Nutzung, ggf. Zonen neu zuschneiden oder zusätzliche Zonen bilden. | Schwache statistische Äquivalenz |

Zudem erklärt der Anhang, dass bestimmte kritische Ausfälle, etwa 225-kV-Ausfälle oder durch netzbetreiberseitige topologische Maßnahmen beherrschte CBCOs, in Abhängigkeit von der betrachteten Qualität und Modellierbarkeit **nicht berücksichtigt** werden können. Dies ist eine dokumentierte methodische Freiheitsstelle; eine einheitliche veröffentlichte normative Ausschlussliste existiert im untersuchten Text nicht. [Q1, S. 47]

## 8.5 Warum eine einzige Ersatzkapazität keine vollständige N-1-Sicherheitsregion ist [A]

In einem vermaschten Netz hängt die Post-Contingency-Belastung nicht nur vom **einen** Grenzfluss $q_e$ ab, sondern von den gleichzeitigen Einspeisungen, Lasten und den Flüssen anderer Netzelemente. Mathematisch hat eine detaillierte Menge linearer N-1-Anforderungen unter festem Netz typischerweise die Form

$$
\mathcal F_{\mathrm{secure}}
=\left\{p:\ \left|H_o p\right|
\le \overline f_o,\ \forall o\in\mathcal O\right\},\tag{31}
$$

also eine (gegebenenfalls umfangreiche) **mehrdimensionale** Menge von Ungleichungen. Eine reduzierte Ersatzkapazität auf einer einzelnen Verbindung entspricht hingegen einer Projektion der Form

$$
-K_{e,\sigma,-}\le\widehat f_e\le K_{e,\sigma,+}.\tag{32}
$$

Die Mengen (31) und (32) können ohne zusätzliche Voraussetzungen **nicht** allgemein äquivalent sein. Die Kapazitätskalibrierung nach dem veröffentlichten Verfahren approximiert die Sicherheit daher über die **beobachtete** Betriebszustandsverteilung. Eine universelle N-1-Garantie für beliebige, nicht untersuchte simultane Einspeiseverschiebungen wird durch [Q1] nicht bewiesen.

Das ist eine Aussage über die Informationsreduktion und die mathematische Reichweite der dokumentierten Methode, **keine** Behauptung über tatsächlich beobachtete Sicherheitsverletzungen in ENTSO-E-Rechenläufen.

# 9. Daten-Disaggregation und Erhaltung zeitlicher Bilanzen

## 9.1 Zuordnungslogik [D]

Nach § 3.8.4 werden die Zonen der detaillierten Netzknoten über die Clusterdefinition gebildet. Die PEMMDB verknüpft Erzeuger, Speicher und weitere Anlagen mit ihren Anschlussknoten. Für variable Lasten liefern Netzbetreiber Aufteilungsschlüssel; industrielle Lasten werden anhand ihrer Anschlussstellen verortet. Bei erneuerbaren Anlagen sind der **elektrische Anschlussort** und die **meteorologische PECD-Region** voneinander zu unterscheiden und konsistent zusammenzuführen. Für thermische Erzeugung sollen Anzahl und installierte Kapazität der Anlagen konsistent bleiben. [Q1, S. 28–29]

## 9.2 Mathematische Bilanzbedingungen der zonalen Abbildung [R/E]

Sei $d_{n,t}$ die Nachfrage und $g_{a,t}$ die Erzeugung einer Anlage $a$ am ursprünglichen Anschlussknoten $n(a)$. Eine elektrisch anschlusstreue Aggregation liefert

$$
G_{z,t}=\sum_{a:\ g(n(a))=z}g_{a,t},
\quad
D_{z,t}=\sum_{n:\ g(n)=z}d_{n,t},
\quad
p_{z,t}=G_{z,t}-D_{z,t}+p_{z,t}^{\mathrm{other}}.\tag{33}
$$

Damit gelten unter konsistenter Komponentenabgrenzung die elementaren Erhaltungsbeziehungen

$$
\sum_zG_{z,t}=\sum_a g_{a,t},
\qquad
\sum_zD_{z,t}=\sum_n d_{n,t}.\tag{34}
$$

Wenn nur übergeordnete nationale Zeitreihen $D_{c,t}$ vorliegen, kann die unbekannte Aufteilung schematisch durch zonale Schlüssel $\alpha_{z|c,t}$ beschrieben werden:

$$
D_{z,t}=\alpha_{z|c,t}D_{c,t},\qquad
\alpha_{z|c,t}\ge0,\qquad
\sum_{z\subset c}\alpha_{z|c,t}=1.\tag{35}
$$

ENTSO-E nennt das Prinzip der vom TSO gelieferten Aufteilungsschlüssel, schreibt aber nicht fest, ob diese zeitlich konstant sind, technologiespezifisch variieren oder wie sie bei Änderungen der Laststruktur fortgeschrieben werden. [U] (35) ist eine **bilanzwahrende mögliche Formalisierung**.

## 9.3 Technologie- und Wetterzuordnung [R/E]

Für eine Wind- oder PV-Anlage $a$ mit installierter Leistung $\overline G_a$ und meteorologischer Profilregion $r(a)$ bietet sich formal

$$
g_{a,t}^{\mathrm{avail}}
=\overline G_a\,\mathrm{CF}_{r(a),t},\qquad
0\le g_{a,t}\le g_{a,t}^{\mathrm{avail}}\tag{36}
$$

an. Die Anlage wird für elektrische Bilanzen in die Zone $g(n(a))$ eingetragen, während ihr meteorologisches Profil aus $r(a)$ stammt. Damit bleiben **Netzanschluss** und **Wetterraum** explizit getrennt. Der dokumentierte Text verlangt eine derartige Konsistenz, definiert aber keine eindeutige Regel für fehlende oder mehrdeutige Anlagenpositionen. [Q1, S. 29]

**Nicht zulässige Vereinfachung:** Die PECD-Geometrie darf nicht ohne weitere Prüfung als elektrische Clusterpartition behandelt werden; umgekehrt folgt aus der elektrischen Knotenzuordnung nicht automatisch das passende Erzeugungsprofil.

## 9.4 Folgen für die Parameterkalibrierung [A]

Eine Änderung der zonalen Last- oder Erzeugungsallokation verändert $p_t^{\mathrm z}$ und damit potenziell $\widehat f_t$. Bei unveränderten physikalischen Ausgangsdaten könnte eine andere Allokation deshalb andere Ersatzimpedanzen und Korrekturflüsse als optimal erscheinen lassen. Die Daten-Disaggregation und die elektrische Netzreduktion sind wissenschaftlich **nicht voneinander unabhängige** Schritte. Abbildung 4 berücksichtigt diese Kopplung über die Rückkopplung zwischen Clustering und Kalibrierung, liefert aber kein vollständig geschlossenes simultanes Optimierungsmodell. [Q1, S. 23]

# 10. Einbindung in die TYNDP-Ausbauoptimierung

## 10.1 Unterschied zum NTC-Marktmodell [D]

Im konventionellen NTC-Modell werden Länder beziehungsweise bestehende Bietzonen durch Kupferplatten und grenzüberschreitende, im Wesentlichen unabhängig begrenzte Transfermöglichkeiten repräsentiert. Kommerzielle Marktaustausche entsprechen deshalb nicht zwingend den realen physikalischen Flüssen; insbesondere können Maschen- und Transitflüsse nicht vollständig dargestellt werden. Der zonale Ansatz führt demgegenüber die **Maschengleichungen des physischen AC-Verbundnetzes in DC-Näherung** in das Marktmodell ein und erlaubt interne zonale Verbindungen. [Q1, S. 21–23]

In einer geeigneten linearen Marktrepräsentation treten daher neben den bilanzierten Einspeisungen $p_t^{\mathrm z}$ Bedingungen der Art

$$
A_{\mathrm z}\widehat f_t=p_t^{\mathrm z},
\qquad C^{\mathsf T}X(\widehat f_t-c^0)=0,
\tag{37}
$$

und – soweit im betreffenden Modus aktiviert – Kapazitätsrestriktionen

$$
-K_{e,\sigma,-}\le\widehat f_{e,t}
\le K_{e,\sigma,+}.\tag{38}
$$

Die Kombination aus (37)–(38) beschreibt lediglich die **elektrische Teilstruktur** und ersetzt weder die Marktbilanz- und Einsatzbedingungen noch das vollständige stochastische Ausbauoptimierungsmodell aus § 3.1. [R]

## 10.2 LF-Ausbauoptimierung und ergänzender OPF-Modus [D]

§ 3.9 beschreibt zwei verschiedene Einsatzweisen des zonalen Netzes.

**LF-Modus – eigentliche IoSN-Ausbauoptimierung.** Die physikalische Verteilung über das vermaschte reduzierte Netz bleibt erhalten, bestehende **interne** Netzeinschränkungen sollen die Wahl neuer grenzüberschreitender Investitionen aber nicht vorbestimmen. Der Text bezeichnet dies als Aktivierung ausschließlich grenzüberschreitender Kapazitäten und als Deaktivierung der internen Interzonen-Kapazitätsgrenzen. [Q1, S. 29]

**OPF-Modus – ergänzende Bewertung.** Zusätzliche Dispatchanalysen mit aktiven internen Netzgrenzen sollen Redispatchänderungen, mögliche interne Verstärkungsbedarfe und die Wirtschaftlichkeit des im LF-Modus gefundenen Portfolios unter tatsächlichen internen Restriktionen untersuchen. Eine ergänzende OPF-Ausbauoptimierung wird dabei auf das LF-Portfolio begrenzt, um einen Ausbau bloß zur Umgehung bereits bestehender interner Engpässe zu vermeiden. [Q1, S. 29]

Für eine formale Variantenimplementierung könnte man eine Menge $E^{\mathrm{cross}}$ grenzüberschreitender AC-Verbindungen und eine Menge $E^{\mathrm{internal}}$ interner Interzonenverbindungen definieren und dann schreiben [R]:

$$
\begin{array}{ll}
\text{LF:} & |\widehat f_e|\ \text{begrenzt, falls }e\in E^{\mathrm{cross}};
\quad \overline f_e=+\infty,\ e\in E^{\mathrm{internal}},\\[3pt]
\text{OPF:} & \widehat f_e\ \text{mit aktiven internen und externen Grenzen.}
\end{array}\tag{39}
$$

**Dokumentarischer Widerspruch [U]:** Derselbe § 3.9 spricht gleichzeitig von „only cross-border capacities are activated“ und pauschal davon, dass „interzone capacities are set to infinity“. Weil auch grenzüberschreitende Verbindungen Interzonenverbindungen sein können, ist die Passage terminologisch nicht vollständig eindeutig. Gleichung (39) stellt die sachlogisch naheliegende Lesart der erklärten Zielsetzung dar, nicht eine aus dem Text zweifelsfrei ableitbare formale Zuordnungsregel.

## 10.3 Konsequenzen für Netzausbauentscheidungen [A]

Ein physikalisch kalibriertes zonales Modell kann räumliche Übertragungswege und Kreisflüsse besser berücksichtigen als eine unabhängige NTC-Transferstruktur. Zugleich entscheidet die LF-/OPF-Moduswahl darüber, **welche** Engpässe tatsächlich die Investitionsentscheidung beschränken. Die Genauigkeit der Ersatzkapazitäten wirkt im LF-Modus auf aktivierte Grenzen anders als in der späteren OPF-Bewertung. Deshalb ist die Unterscheidung zwischen *Qualität der Netzreduktion* und *Restriktionsaktivierung im Investitionsproblem* zentral: Ein gut kalibrierter Interzonenfluss impliziert noch nicht, dass im betreffenden Studienmodus auch seine Kapazitätsgrenze bindend ist.

# 11. Numerische Illustrationen und Grenzfälle

Die folgenden Beispiele sind **eigene synthetische Beispiele**. Sie stammen nicht aus TYNDP-Datensätzen und dienen ausschließlich zur mathematischen Plausibilisierung der veröffentlichten Prinzipien.

## 11.1 Bilanz ohne Maschengleichungsäquivalenz

Betrachte drei reduzierte Zonen mit einer ringförmigen AC-Verbindung, den gleichgerichteten Kanten $1\to2$, $2\to3$, $3\to1$. Die Inzidenzmatrix ist

$$
A_{\mathrm z}=
\begin{pmatrix}
1&0&-1\\
-1&1&0\\
0&-1&1
\end{pmatrix}.
\tag{40}
$$

Für den reinen Kreisfluss $c^0=(20,20,20)^{\mathsf T}\,\mathrm{MW}$ ist $A_{\mathrm z}c^0=0$. Der Fluss verletzt daher **keine** zonale Leistungsbilanz, obwohl jede Interzonenverbindung 20 MW führt. Ohne strukturellen Offset erzwingt das DC-Modell mit identischen positiven Reaktanzen und $p=0$ jedoch $f=0$, weil $C^{\mathsf T}Xf=3x\cdot20\ne0$. Mit der Korrekturformulierung (19) wird $C^{\mathsf T}X(f-c^0)=0$ erfüllt.

Das Beispiel illustriert den mathematischen Bedarf nach einer **gemeinsamen Definition** von Nullbilanzfluss und Maschenbedingungen. Es besagt **nicht**, dass dieser Wert 20 MW in einem tatsächlichen ENTSO-E-Modell vorkommt.

## 11.2 Fehlinterpretation einer aggregierten Grenzkapazität

Zwei physikalische Grenzleitungen haben angenommene thermische Grenzen von jeweils 300 MW. Eine naive Summation ergäbe $600\,\mathrm{MW}$. Unter einer betrachteten N-1-Kontingenz kann sich der Fluss beider Leitungen jedoch auf einen verbleibenden Kreis konzentrieren; im Allgemeinen folgt daraus **nicht**, dass $600\,\mathrm{MW}$ sicher übertragbar wären. Die tatsächliche Ersatzgrenze hängt vom Ausfall, von den LODFs und von den simultanen Grundflüssen ab. Genau deshalb werden die Ersatzkapazitäten im Dokument **nicht** als reine Summen thermischer Leitungsgrenzen definiert. [Q1, S. 27 und 50]

## 11.3 Flussgüte gegen Engpassgüte

Sei ein reduziertes Netz in 100 fiktiven Kalibrierungsstunden auf 99 Stunden mit einem Fehler von null und in einer seltenen extremen Engpassstunde auf einen Fehler von 500 MW kalibriert. Dann ist sein globaler ungewichteter Fehler

$$
\operatorname{RMSE}=\sqrt{\frac{99\cdot0^2+1\cdot500^2}{100}}
=50\,\mathrm{MW}.\tag{41}
$$

Ein relativ kleiner Jahres-RMSE kann folglich gleichzeitig mit einem sehr hohen **einzelstündlichen** Engpassfehler auftreten. Diese arithmetische Aussage motiviert zusätzliche Tail- oder Stressstundenkriterien und widerlegt keine tatsächlich veröffentlichten numerischen ENTSO-E-Ergebnisse.

# 12. Qualitätsmaße, Validierung und Unsicherheitsbewertung

## 12.1 In der Quelle angegebene Qualitätslogik [D]

Der Clustering-Prozess wird laut Anhang iterativ verbessert: Entdeckte Engpässe werden an Zonengrenzen gebracht, eine neue Partition wird getestet, die resultierende Netzreduktion optimiert, die Fehlerqualität und Kapazitätsgüte geprüft, und Änderungen werden bei Verbesserung übernommen. Dabei besitzt der **RMSE Vorrang** vor der nachgelagerten Kapazitätsqualität. [Q1, S. 45–47]

Abbildung 13 [Q1, S. 46] illustriert folgende **fehlerklassifizierende Grenzen**:

| Farbkategorie | In der Abbildung gezeigte Bedingung |
|:--|:--|
| Grün | RMSE $\le200\,\mathrm{MW}$ **oder** relativer RMSE/Fluss $\le10\%$ |
| Gelb | RMSE $\le350\,\mathrm{MW}$ **oder** relativer RMSE/Fluss $\le20\%$ |
| Rot | RMSE $\le500\,\mathrm{MW}$ **oder** relativer RMSE/Fluss $\le30\%$ |
| Schwarz | RMSE $>500\,\mathrm{MW}$ **und** relativer RMSE/Fluss $>30\%$ |

**Vorsicht:** Diese abgebildeten Kriterien sind verschachtelt und keine vollständig disjunkten mathematischen Klassen. Zudem definiert der Text den Bezugsnenner „RMSE/flow“ nicht eindeutig. Eine deterministische Klassifizierung benötigt eine **Priorität der Kategorien** und eine genaue relative Fehlerdefinition, die dem untersuchten Methodikdokument nicht vollständig zu entnehmen sind. [U]

## 12.2 Konventioneller RMSE als Rekonstruktion [R]

Für eine reduzierte Verbindung $e$ und eine definierte, identische Stundenmenge $\mathcal T$ kann man den Fehler als

$$
\operatorname{RMSE}_e
=\sqrt{\frac{1}{|\mathcal T|}
\sum_{t\in\mathcal T}
\bigl(\widehat f_{e,t}-f_{e,t}^\star\bigr)^2}
\tag{42}
$$

und für die Gesamtheit der reduzierten Verbindungen als

$$
\operatorname{RMSE}_{\mathrm{global}}
=\sqrt{\frac{1}{r|\mathcal T|}
\sum_{e=1}^r\sum_{t\in\mathcal T}
\bigl(\widehat f_{e,t}-f_{e,t}^\star\bigr)^2}
\tag{43}
$$

notieren. Beide Formeln sind übliche Varianten, jedoch spezifiziert [Q1] nicht eindeutig, welche absolute oder relative Aggregation seinen Qualitätsindikatoren zugrunde liegt. Ein relativer RMSE könnte beispielsweise durch mittleren Absolutfluss, Bemessungsleistung, Nennkapazität oder einen anderen Wert dividiert werden; jede Wahl verändert die qualitative Einstufung. [U]

## 12.3 Wissenschaftlich erforderliche Validierungsebenen [E]

Ein fachlich belastbares Prüfprotokoll sollte **mindestens** zwischen den folgenden Ebenen unterscheiden:

**V1 – Daten- und Bilanzvalidität.** Eindeutigkeit der Knoten-Zonen-Zuordnung, graphische Konnektivität jeder Zone, Erhalt der aggregierten Einspeise-/Lastbilanzen (9) und (34), korrekte Orientierung und verlustkonsistente Behandlung der Grenzflüsse.

**V2 – Elektrische Struktur.** Rang und Dimension der Inzidenz- und Zyklenmatrizen, zulässige Ersatzreaktanzen, Restfehler in Knotenbilanz und Maschenbeziehungen (einschließlich definierter Nullbilanzfluss-Offets), nachvollziehbarer Referenzwinkel und Modellkomponenten.

**V3 – Interzonen-Flussabbildung.** Fehler je Verbindung und je Wetterjahr, mediane und hohe Fehlerquantile, Maximum über kritische Stunden, systematische Vorzeichenfehler, Cross-Validation zwischen Kalibrierungs- und Teststunden.

**V4 – N-1-Surrogatgüte.** Fehler der Ersatzkapazitäten, Datenzahl nahe 100-%-Belastung, Unsicherheit des Schnittpunkts, Sensitivität gegenüber CBCO-Ausschlüssen, die Häufigkeit von sicherheitskritischen Fehlklassifikationen bei gehaltenen, unabhängigen Stunden.

**V5 – Planungsrelevanz.** Stabilität der im LF-Modus identifizierten Investitionsportfolios gegenüber plausiblem Zonen-Reclustering und unterschiedlichen Parametersätzen sowie Vergleich von LF- und OPF-Ergebnissen.

Für jede Ebene sind Eingangsdateien, Topologiestände, Stundenindizes, Solveroptionen, Zwischenresultate und akzeptierte Schwellenwerte versioniert zu dokumentieren. Diese Anforderungen ergänzen [Q1]; sie sind nicht als bereits implementierte ENTSO-E-Gates zu interpretieren.

## 12.4 Gefahr der Kalibrierung auf dieselben Stunden [A]

Wenn die Parameter $X$ und $c^0$ anhand der stündlichen Zielflüsse optimiert und anschließend **nur auf denselben Stunden** beurteilt werden, ist ein niedriger Fehler lediglich ein Maß für die Anpassung an den Kalibrierungsdatensatz. Er beweist keine Generalisierung auf abweichende Wetterjahre, neue Anlagenverteilungen oder zukünftige Netztopologien.

Ein zusätzliches Testset $\mathcal T^{\mathrm{test}}\cap\mathcal T^{\mathrm{cal}}=\varnothing$ ist daher eine wissenschaftlich notwendige Ergänzung, wenn eine **out-of-sample**-Aussage zur Modellrobustheit getroffen werden soll. Das Dokument spezifiziert eine solche saubere Trennung nicht. [U/E]

# 13. Spezifikationsaudit und priorisierte Anforderungen

## 13.1 Reifegradmatrix

Der Reifegrad bezieht sich **ausschließlich auf den veröffentlichten Informationsgehalt** der konsultierten Quelle. Er ist keine Bewertung der Qualität der internen ENTSO-E-Arbeit.

| Gegenstand | Dokumentationsstatus | Erforderliche Präzisierung |
|:--|:--|:--|
| Ziel einer vermaschten zonalen Wirkleistungsabbildung | **Klar [D]** | Keine für die Grundidee |
| Unterscheidung NTC und AC-äquivalente Zone | **Klar [D]** | Genaue Marktintegration als Modellgleichungen |
| 102 Zonen und Länderzahlen | **Klar [D]** | Vollständige Knotenzonen- und Link-Zuordnung |
| Verwendung 225-/400-kV-Engpassflüsse | **Klar/teilweise [D/U]** | Grenzwerte, Auswahl betroffener Leitungen, Wetteraggregation |
| Zielflussberechnung über PTDF | **Teilweise [D/U]** | Parameterliste, Störungsschritte, Slack-/Referenzfälle |
| Clustering-Algorithmus | **Teilweise [D/U]** | Zulässige Änderungen, Zielfunktion, Stopp- und Gleichstandregeln |
| Ersatznetz-Admittanz und Impedanzoptimum | **Teilweise [D/U]** | Vollständige Zielfunktion, Nebenbedingungen, Normierung |
| Strukturelle Nullbilanzflüsse | **Teilweise [D/U]** | Einbindung in Bilanz/Maschenregeln und Szenarioindex |
| Auswirkung HVDC und PST | **Teilweise [D/U]** | Exakte Steuer-/Offsetabbildung |
| Vier N-1-Kapazitäten je Verbindung | **Klar [D]** | Allgemeine Fit-/Kontingenz- und Sicherheitslogik |
| Fehlende/CBCO-Ausfalldaten | **Teilweise [D/U]** | Explizite Ausschlusslisten und Auswirkungsanalysen |
| Zeitreihen-Disaggregation | **Teilweise [D/U]** | Allokationsschlüssel je Technologie, Zeit und Szenario |
| LF-/OPF-Modellgrenzen | **Teilweise [D/U]** | Verbindungstypen eindeutig definieren |
| Qualitätsvalidierung | **Teilweise [D/U]** | RMSE-Normierung und Auswertung unabhängiger Stunden |
| End-to-end-Reproduzierbarkeit | **Nicht spezifiziert [U]** | Daten-/Parameter-/Code-/Versionsmanifest |

## 13.2 Erforderliche Entscheidungen nach Priorität

| ID | Priorität | Wissenschaftlich zu schließende Anforderung | Konsequenz bei Offenbleiben |
|:--|:--|:--|:--|
| NR-01 | **Kritisch** | Detaillierten Netzdatenstand und Knotenzonen-Matrix $P$ fixieren | Reduzierte Topologie nicht reproduzierbar |
| NR-02 | **Kritisch** | Originalleitung–Interzonen-Abbildung $\Gamma$ einschließlich Richtungen festlegen | Zielflüsse und Bilanzen nicht deterministisch |
| NR-03 | **Kritisch** | Kalibrierungswetterjahre, Stunden und Gewichte fixieren | Impedanz-/Offset-Parameter nicht reproduzierbar |
| NR-04 | **Kritisch** | Zielfunktion, Parameterbereiche und Normierung der Impedanzkalibrierung veröffentlichen | Skalierungsmehrdeutigkeit und Solverabhängigkeit |
| NR-05 | **Kritisch** | Gleichungsintegration der Nullbilanzflüsse mit Maschen- und Knotenbedingungen festlegen | Physikalische Konsistenz nicht verifizierbar |
| NR-06 | **Kritisch** | CBCO- und Ausfallmenge samt Ausschlussgründen dokumentieren | N-1-Äquivalenz nicht unabhängig überprüfbar |
| NR-07 | **Kritisch** | Allgemeine statistische Schätzung der 100-%-Schnittpunkte und Gütequalifizierung definieren | Ersatzkapazitäten nicht reproduzierbar |
| NR-08 | **Hoch** | Zeit-, Szenario- und Zieljahr-Indizes der Ersatzparameter klarstellen | Übertragbarkeit und Vergleichbarkeit unklar |
| NR-09 | **Hoch** | PTDF-Ausgangsfall, variierte Marktparameter, Schrittweiten und Rebalancierung festlegen | Referenzflüsse nicht reproduzierbar |
| NR-10 | **Hoch** | Behandlung von HVDC, PST und getrennten Stromnetzteilen beschreiben | Regelbarer Flussanteil nicht eindeutig |
| NR-11 | **Hoch** | Klare Sommer-/Winterdefinition sowie physikalische Leitungsgrenzen hinterlegen | Saisonkapazitäten nicht nachbildbar |
| NR-12 | **Hoch** | Verbindliche interne und grenzüberschreitende Kantenklassen für LF/OPF festlegen | Aktivierte Netzrestriktionen interpretationsabhängig |
| NR-13 | **Hoch** | TSO-Allokationsschlüssel, PECD-Kopplung und Bilanztests definieren | Zonale Zeitreihen können Inkonsistenzen erzeugen |
| NR-14 | **Hoch** | unabhängige Teststunden/-szenarien samt kritischen Fehlerkennzahlen festlegen | Generalisierung nicht nachgewiesen |
| NR-15 | **Mittel** | RMSE-Definition und Farbklassifikations-Priorität formal ergänzen | Bewertungsfarben nicht deterministisch |
| NR-16 | **Mittel** | Kriterien für Clustering-Abbruch, stabile Verbesserung und Zonenwechsel dokumentieren | Re-Cluster-Prozess nicht nachvollziehbar |
| NR-17 | **Mittel** | Datenqualitätsregeln für 110-kV-Lücken und parallele Grenzleitungen definieren | Lokale Cluster-Güte abhängig von Datenlücken |
| NR-18 | **Mittel** | Dokumentationskonflikt zu Wetterjahr-Fenstern auflösen | Unklare Wetterstichprobe |

## 13.3 Minimal ausreichender Reproduzierbarkeitsdatensatz [E]

Ein Dritter benötigt mindestens ein versioniertes **Topologiepaket** (Originalgraph, AC-Zweigparameter, Knoten-Zonen-Mapping, Grenzleitungsgruppen), ein **Betriebsstundenpaket** (NTC-Marktoutputs, nodale bzw. zonale Einspeisungen, Referenz-PTDF und Zielgrenzflüsse), ein **Kalibrierungspaket** (aktuelle Partition, Optimierungsaufgabe und -parameter, gefundene Reaktanzen und Korrekturflüsse), ein **Kontingenzpaket** (LODF- und CBCO-Listen, physikalische Grenzen, Stunden- und Saisondatenpunkte) sowie ein **Validierungspaket** (Fehler je Verbindung und Stunde, Sicherheitsvergleiche, ausgewiesene Ausnahmefälle und Solver-/Softwareversionen).

Die Existenz oder Veröffentlichung solcher Pakete wird durch [Q1] nicht behauptet. Es handelt sich um einen methodischen Mindeststandard für den Zweck einer unabhängigen Nachrechnung.

# 14. Konsistente Referenzarchitektur für eine wissenschaftliche Reimplementation

## 14.1 Input-/Output-Verträge [E]

Die hier skizzierte Architektur beschreibt **nicht** ein in [Q1] veröffentlichtes Softwaredesign. Sie operationalisiert die aus der Dokumentation ableitbaren Anforderungen unter expliziter Kennzeichnung noch offener Entscheidungen.

| Schritt | Erforderlicher Input | Prüfbarer Output |
|:--|:--|:--|
| A. Data preflight | Versioniertes Originalnetz, PEMMDB-/PECD-Zeitreihen, Markt-Dispatch | Topologie-, Mengen- und Zeitkonsistenzbericht |
| B. Detailed-flow synthesis | Referenzfall, ausgewählte Marktparameter, PTDF-Sensitivitäten, Stunden | $f_{\ell,t}^{\mathrm d}$ und kontrollierte Knotenbilanzen |
| C. Criticality scoring | Leitungsflüsse, Grenzwerte, Wetter-/Stundenindex | $E_{\ell,s}^{\mathrm{ov}}$ und Engpassrangfolge |
| D. Partition candidate | Netzgraph, kritische Leitungen, Konnektivitätsanforderung | $P$, $A_{\mathrm z}$, $\Gamma$, zonale Zuordnungsbilanz |
| E. Equivalent-flow calibration | $f_t^\star$, $p_t^{\mathrm z}$, Kalibrierungsdefinition | $X$, $c^0$, stündliche $\widehat f_t$, Residuen |
| F. Equivalent-capacity fitting | N-1-LODF, CBCOs, Leitungsgrenzen, Stunden/Saison | Vier $K_{e,\sigma,d}$ mit Unsicherheit/Status |
| G. Model acceptance | unabhängige Teststunden, Qualitätsschwellen | Annahme/Ablehnung oder Cluster-Rückkopplung |
| H. IoSN integration | freigegebenes Netz, zonale Zeitreihen, Stellgeräte | konsistente LF-/OPF-Modellvarianten |

## 14.2 Kontrollierte Iteration [E]

Eine methodisch konsistente Iteration könnte wie folgt definiert werden:

1. Ausgangspartition $P^{(0)}$ aus der geprüften, zusammenhängenden Zonenstruktur initialisieren.
2. Kritische Leitungen anhand von (3) priorisieren; eine begründete geographisch-elektrische Änderung $P^{(k+1)}$ erzeugen.
3. $\Gamma^{(k+1)}$, $A_{\mathrm z}^{(k+1)}$ und die synchronen Zielflüsse nach (7) bestimmen; (8) numerisch testen.
4. Ersatzparameter auf einem **festgelegten** Kalibrierungsindex fitten, die Skalierungsnormierung prüfen und die ergänzte Maschenbeziehung testen.
5. Die vier N-1-Transfergrenzen mit einem **versionierten** Kontingenz- und Regressionsdatensatz berechnen; Ausnahmefälle gesondert markieren.
6. Fluss-/Kapazitätsqualität **auf unabhängigen Teststunden** messen und Änderungen nur bei vorher festgelegten Akzeptanzregeln übernehmen.
7. Falls nicht akzeptiert, zum Clustering zurückgehen; andernfalls das reduzierte Netz mit Zeitreihen und Moduskennzeichen publizieren.

Anders als eine unkontrollierte Reoptimierung aller Größen auf wechselnden Stunden erhält diese Architektur die Vergleichbarkeit unterschiedlicher Partitionen. Die Verfahrensidee der iterativen Partitionsverbesserung ist dokumentiert [Q1, S. 45–47], **nicht** jedoch diese konkrete Reihenfolge einschließlich Testdatentrennung und Akzeptanzregeln.

# 15. Schlussfolgerungen

Die Netzreduktion im TYNDP 2026 ist sachgerecht als **zeitreihenbasiert kalibrierte, topologisch informierte und sicherheitsorientiert parametrierte zonale Wirkleistungsnetzapproximation** einzuordnen. Der Begriff „Netzreduktion“ darf dabei weder auf das Clustering der Knoten noch auf die elektrische Zusammenfassung von parallelen Leitungen verkürzt werden.

Der dokumentierte Verfahrenskern besteht aus (i) der engpass- und flussorientierten Knotenzonierung, (ii) der Rekonstruktion synchroner detaillierter AC-Netz-Wirkflüsse durch DC-/PTDF-Rechnungen, (iii) der Flussfehlerkalibrierung äquivalenter Impedanzen und Nullbilanzkorrekturen, (iv) der datenbasierten Ermittlung von N-1-Ersatzkapazitäten und (v) der rückgekoppelten Verbesserung der Partition. Dieser Kern ist fachlich nachvollziehbar und für großräumige langfristige Studien plausibel. [Q1, § 3.8 und Anhang 6.1]

**Das entscheidende wissenschaftliche Defizit liegt nicht im Fehlen einer allgemeinen physikalischen Idee, sondern in fehlenden eindeutigen Definitionen an den Kopplungsstellen.** Die veröffentlichte Quelle lässt offen, wie Kalibrierungsstunden ausgewählt werden, wie Nullbilanzflüsse exakt mit Maschengleichungen kombiniert werden, welche Normierung der Ersatzreaktanzen gilt, wie die allgemeine N-1-Kapazitätskurve geschätzt wird und mit welchen Testdaten die Qualität unabhängig nachgewiesen wird.

Die mathematische Herleitung macht zudem zwei prinzipielle Grenzen sichtbar:

- **Bilanzäquivalenz ist nicht elektrische Zustandsäquivalenz.** Die räumliche Aggregation kann Leistungsbilanzen exakt erhalten, ohne die originalen Winkel- und Zweigflussbeziehungen exakt reproduzieren zu können.
- **Statistische N-1-Transferäquivalenz ist keine universelle N-1-Sicherheitsgarantie.** Vier richtungs- und saisonabhängige Skalargrenzen bilden nur einen Teil des mehrdimensionalen sicherheitskritischen Betriebsraums ab.

**Endurteil:** Auf Grundlage der allein untersuchten ENTSO-E-Konsultationsfassung ist eine formal konsistente wissenschaftliche Rekonstruktion möglich; eine **eindeutige, numerisch und algorithmisch reproduzierbare Implementierung** erfordert die Schließung insbesondere der kritischen Anforderungen **NR-01 bis NR-07**. Eine weitergehende Behauptung zur konkreten internen ENTSO-E-Berechnung wäre ohne zusätzliche Originaldaten und Spezifikation nicht belegt.

# Anhang A. Mathematische Beweise und Prüfinvarianten

## A.1 Flusserhaltung durch Graphaggregation

Der Beweis von (8) gilt unabhängig davon, wie die Zonen geografisch zugeschnitten sind, **sofern** die Zuordnung jedes Originalknotens eindeutig und der Interzonen-Kantenaggregator konsistent ist. Eine mögliche Validierungsinvariante lautet daher

$$
\epsilon_{\mathrm{inc}}=
\|A_{\mathrm z}\Gamma-PA_{\mathrm d}\|_{\max}=0,\qquad
\epsilon_{\mathrm{KCL},t}=
\|A_{\mathrm z}f_t^\star-Pp_t^{\mathrm d}\|_\infty\approx0.\tag{A1}
$$

Wenn Teilnetze (etwa HVDC-Betriebsmittel) als externe Einspeisung statt als AC-Zweig in $A_{\mathrm d}$ geführt werden, müssen beide Seiten von (A1) dieselbe AC-Bilanzkonvention verwenden. Modellbedingt verbleibende Wirkverluste verletzen die verlustlose DC-Gleichung und sind nicht ohne weitere Festlegung durch (A1) kompensierbar.

## A.2 Äquivalenz von Winkelmodell und Zyklusgleichung

Für positive $X$ gilt $\widehat f=BA^{\mathsf T}\theta$ genau dann, wenn $X\widehat f\in\mathrm{im}(A^{\mathsf T})$. Nach dem Fundamentalsatz der linearen Algebra ist $\mathrm{im}(A^{\mathsf T})=(\ker A)^\perp$, sodass

$$
X\widehat f\in\mathrm{im}(A^{\mathsf T})
\quad\Longleftrightarrow\quad
C^{\mathsf T}X\widehat f=0.\tag{A2}
$$

Mit strukturellem Nullbilanzoffset $c^0$ wird dieselbe Aussage auf $\widehat f-c^0$ angewendet. Für ein verbundenes Netzwerk mit $r$ Kanten und $k$ Zonen gibt es $r-k+1$ unabhängige Maschenbedingungen. Wenn $c$ Zusammenhangskomponenten existieren, erhöht sich die Zahl auf $r-k+c$.

## A.3 Genauigkeit und Identifizierbarkeit sind getrennte Kriterien

Aus (24) folgt unmittelbar

$$
J(\alpha X,c^0)=J(X,c^0)
\qquad \forall\,\alpha>0\tag{A3}
$$

für jede Zielfunktion $J$, die ausschließlich auf vorhergesagten Flüssen im Modell (20) beruht, solange sich die übrigen Größen nicht verändern. Damit können **verschiedene numerische Reaktanzsätze exakt denselben RMSE** besitzen. Ein Report, der nur den RMSE dokumentiert, validiert noch nicht die Eindeutigkeit oder physikalische Skalierung der Reaktanzen.

## A.4 Alternative zur reinen Normierung: externe physikalische Referenz

Eine mögliche Identifikationsergänzung wäre, mindestens eine repräsentative Reaktanz je zusammenhängender Netzkomponente festzulegen oder die Parameter auf eine vorab dokumentierte Skalierungsbedingung einzuschränken, beispielsweise

$$
\sum_{e=1}^{r}\log x_e^{\mathrm{eq}}=\kappa\tag{A4}
$$

für eine **extern begründete** Referenzkonstante $\kappa$. Die konkrete Bedingung (A4) ist eine eigene methodische Empfehlung [E] und lässt sich nicht [Q1] als gültige ENTSO-E-Festlegung zuschreiben.

# Anhang B. Auflösung der wichtigsten offenen Spezifikationsfragen

| Frage | In der Quelle eindeutig beantwortet? | Zulässige Aussage in einem wissenschaftlichen Manuskript |
|:--|:--|:--|
| Werden 8.760 Stunden für die Engpassidentifikation verwendet? | **Grundsätzlich ja**, stündliche jährliche Bewertung; Umfang verschiedener Szenarien muss spezifiziert sein | „Stündliche Überlastungswerte über ein Jahr werden aggregiert.“ |
| Werden **alle** Stunden zur Impedanzidentifikation verwendet? | **Nein, nicht festgelegt** | „Es wird eine Stichprobe synchroner physikalischer Flüsse verwendet.“ |
| Werden Klimaszenario-Gewichte als Impedanz-Fitgewichte verwendet? | **Nicht belegt** | „Die IoSN-Ausbauoptimierung nutzt die ausgewiesenen Wettergewichte; ein Transfer auf den Impedanz-Fit ist offen.“ |
| Ist das Ersatznetz ein vollständiges AC-Lastflussäquivalent? | **Nein, nicht nachgewiesen** | „Die expliziten elektrischen Nebenbedingungen sind in DC-Näherung formuliert.“ |
| Sind elektrische Nettoflüsse über Zonen konservativ aggregierbar? | **Ja, unter konsistenten DC-/Bilanzannahmen** | „Die Knotenbilanz kann durch $A_z\Gamma=PA_d$ erhalten werden.“ |
| Ist die absolute Skala äquivalenter Reaktanzen aus DC-Flussdaten bestimmbar? | **Nein** | „Globales Reaktanz-Scaling ist ohne zusätzliche Referenz nicht identifizierbar.“ |
| Gibt es je Zonenlink vier N-1-Kapazitäten? | **Ja** | „Sommer/Winter und beide Flussrichtungen.“ |
| Ist eine allgemeine Kapazitätsregression veröffentlicht? | **Nein** | „Die Kapazität ergibt sich aus dem Schnitt geschätzter Belastungsdaten mit 100 %; Details sind offen.“ |
| Sind alle N-1-Kontingenzen zwingend enthalten? | **Nein** | „LODF und ausgewählte CBCO; bestimmte Fälle können ausgeschlossen werden.“ |
| Werden interne Engpässe in der primären LF-Ausbauoptimierung aktiv begrenzt? | **Nein, gemäß Zielsetzung nicht** | „Interne Kapazitätsgrenzen werden für die primäre LF-Optimierung deaktiviert.“ |
| Können die Ergebnisse ohne Originaltopologie und Ein-/Ausgangsdaten vollständig nachgerechnet werden? | **Nein** | „Die Methodik ist konzeptionell rekonstruierbar, aber nicht numerisch vollständig replizierbar.“ |

# Quellenverzeichnis

**[Q1]** ENTSO-E Planning Study Team / System Development Committee (2026). *TYNDP 2026 Identification of System Needs Methodology.* **Version for Public Consultation**, 25 February 2026, 65 S. Ausschließlich verwendete fachliche Primärquelle. Zuordnung der wichtigsten Fundstellen: § 3.7, S. 18–21; § 3.8.1, S. 23–27; § 3.8.2, S. 27; § 3.8.3–3.8.4, S. 28–29; § 3.9, S. 29; Anhang 6.1, S. 45–51; Anhang 6.3, S. 57–62. <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf>

