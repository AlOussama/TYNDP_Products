---
title: "Netzreduktion im ENTSO-E TYNDP 2026: Wissenschaftlicher Methodenvergleich"
subtitle: "IoSN-Baseline, PTDF-Aggregation, technologiespezifische Verteilungen, elektrische Äquivalenz, N-1-Sicherheit und Flow-Based Market Coupling"
author: "Wissenschaftlicher Konsolidierungsbericht — Revision 1"
date: "16. Oktober 2026"
lang: de-DE
fontsize: 10pt
geometry: "top=22mm,bottom=23mm,left=23mm,right=22mm"
colorlinks: true
urlcolor: blue
numbersections: false
toc: true
toc-depth: 2
toc-title: "Inhaltsverzeichnis"
header-includes:
  - '\usepackage{booktabs}'
  - '\usepackage{longtable}'
  - '\usepackage{array}'
  - '\setlength{\emergencystretch}{2em}'
---

# Zusammenfassung und Kernaussagen

Diese Revision ersetzt die bisher getrennt geführten wissenschaftlichen Aussagen zum ENTSO-E-Netzreduktionsverfahren, zu zwei Clustering-Ansätzen (A und B), zu technologiespezifischen PTDFs, zu Referenzverteilungen (gleichmäßig, leistungsgewichtet und Merit Order), zur elektrischen Ersatznetzkalibrierung, zu N-1-sicheren Kapazitäten, zur dualen LODF-Theorie und zu Flow-Based Market Coupling (FBMC). Ihr Ziel ist eine **wissenschaftlich überprüfbare, intern konsistente Gesamtdarstellung**. Der korrespondierende Band II definiert die PyPSA-Implementierung und die Verifikationsstufen.

**Zentrale Ergebnisse:**

1. Die **IoSN-Referenzmethodik** gemäß ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, Konsultationsfassung vom 25. Februar 2026, Kap. 3.8.1–3.8.4 und Anhang 6.1, priorisiert kritische Leitungen über aufgelaufene Überlastungsenergie aus Marktsimulationen und detaillierten stündlichen Leistungsflüssen. Nach der Zonierung werden Ersatzimpedanzen und Nullbilanzflusskorrekturen kalibriert und saisonale, richtungsabhängige N-1-Ersatzkapazitäten geschätzt. Die Veröffentlichung liefert nicht den vollständigen deterministischen Optimierungsalgorithmus [E1].
2. **Methode A** reproduziert diese Auswahlidee so eng wie öffentlich möglich; **Methode B** ersetzt den Überlastungsindikator durch die allgemeine RES-/Last-induzierte Leitungsbeanspruchung. B ist eine begründete Forschungsalternative, **keine** von ENTSO-E definierte Originalmethode.
3. Eine Busmap induziert zwei algebraische Operatoren: Knotenaggregation $P$ und Zweigflussaggregation $\Gamma$. Die Identität $A_z\Gamma=P A_d$ beweist die **exakte Erhaltung der zonalen Wirkleistungsbilanz**; die elektrischen Maschengleichungen des Ersatznetzes folgen daraus ausdrücklich **nicht**.
4. Technologiespezifische effektive PTDFs $H_z^{(k)}=\Gamma H_dR_k$ werden aus **einer einzigen physikalischen nodalen PTDF** und technologieabhängigen räumlichen Gewichten abgeleitet. Eine zeitabhängige strukturelle Flusskorrektur lässt sich exakt gegenüber einer gewählten Referenzzerlegung formulieren; ein für das Ersatznetz konstanter $F_0$ ist dagegen ein identifizierter Modellparameter.
5. Die **N-1-Sicherheitsregion** kann bei fixierter intrazonaler Verteilung direkt aus der detaillierten PTDF, der LODF und den Leitungsgrenzen als gekoppeltes Polyeder konstruiert werden. Einzelne zonale Link-Kapazitäten, auch wenn sie als exakte bilaterale Grenzwerte berechnet wurden, ersetzen dieses Polyeder nicht.
6. Die Woodbury-Identität und die duale Kreisflusstheorie sind alternative effiziente **Berechnungswege der Kontingenzsensitivitäten**, keine zusätzlichen physikalischen Sicherheitsmodelle. Die leitungsspezifischen/robusten Derating-Ideen nach Gazafroudi–Neumann–Brown sind wissenschaftliche Vergleichsmethoden [N1, N2].
7. FBMC und IoSN-Zonenreduktion verwenden dieselbe nodale Physik, aber verschiedene Operatoren, Zonenbegriffe und Sicherheitssemantiken. Die Analogie zwischen $\Gamma H_dR$ und $K H_dG$ ist exakt auf der Ebene linearer Sensitivitäten, **nicht** auf der Ebene der Kapazitätsbegriffe (IoSN-Ersatzkapazität vs. operativer RAM).

**Erkenntnisstatus:** [D] direkt im IoSN-Dokument beschrieben; [R] explizite mathematische Rekonstruktion; [E] eigener Entwurf; [L] aus externer wissenschaftlicher Literatur begründbar; [S] synthetisch getestet; [O] nicht spezifiziert bzw. noch nicht realnetzvalidiert. Jede Gleichung wird im Folgenden einer dieser Kategorien zugeordnet. Wissenschaftliche Literatur und PyPSA-Dokumentation werden **nicht** als Quelle für eine vermeintlich offizielle IoSN-Definition verwendet.

# 1. Untersuchungsgegenstand, Quellenhierarchie und Grenzen

## 1.1 Verbindliche IoSN-Referenz

**[D]** Die alleinige methodische Autorität für den *Abgleich mit der ENTSO-E-Netzreduktion* ist [E1], Abschnitt 3.8 (Zonal Clustering, Network Reduction, Outputs und Market Data Split), Abschnitt 3.9 (interne Restriktionen) und Anhang 6.1 (Clustering, Impedanzoptimierung und N-1-Ersatzkapazitäten). Kapitel 3.7 (Wetterfälle) und Kapitel 3.1 (Planungsmodell) liefern den Kontext. [E1] trägt ausdrücklich den Status *Version for Public Consultation*, datiert 25.02.2026. Die im Folgenden formulierten alternativen mathematischen Verfahren sind daher **nicht als ENTSO-E-Vorgaben** zu lesen.

**[D]** Die dokumentierte Zonierung dient einer physikalisch sinnvollen, rechenbaren Näherung des pan-europäischen Verbundnetzes. ENTSO-E berichtet **102 Zonen**, darunter 11 für Deutschland und 16 für Frankreich; es sind Planungszonen, nicht identisch mit den Core-Gebotszonen. Die Zonen sollen wesentlich über Engpässe, synchrone Flussmuster und Begrenzung der Zonenanzahl bestimmt werden. Weitere Kriterien sind Konnektivität, sinnvolle Zonengrößen und PECD-Bezug [E1, S. 23–27].

## 1.2 Getrennte wissenschaftliche Bezüge

Die Theorie zu Kreisfluss-LODFs und zu Woodbury wird in [N1], der Vergleich der N-1-Approximationen in [N2] verankert. PyPSA-Funktionen werden in [P1]–[P3] zitiert. Operative FBMC-Begriffe werden als **eigener Anwendungsbereich** betrachtet; das IoSN-Dokument definiert keinen vollständigen Core-Day-Ahead-Capacity-Calculation-Prozess.

## 1.3 Abgrenzung des Nachweises

Die Herleitungen beziehen sich auf verlustlose, stationäre Wirkleistungsflüsse in DC-Näherung. Wirk- und Blindleistung sind nicht synonym; thermische AC-Grenzen in MVA/A sind für ein DC-Modell auf explizite MW-Proxys abzubilden. Nicht eingeschlossen sind AC-Spannungsgüte, Blindleistung, nichtlineare Verlustmodelle, Kurzschluss- und Stabilitätsäquivalenz. HVDC-Terminalverluste, Trafo-Taps, PSTs und Netzinseln müssen als Sonderfälle ausdrücklich behandelt werden. Ein niedriger Fluss-RMSE belegt weder dynamische Äquivalenz noch N-1-Sicherheit.

# 2. Einheitliche Notation und detaillierte elektrische Physik

## 2.1 Netzgraph und DC-Flussmodell

Sei $G_d=(\mathcal N,\mathcal L)$ ein zusammenhängender passiver AC-Teilgraph mit $N$ Knoten, $L$ Zweigen, orientierter Inzidenz $A_d\in\mathbb R^{N\times L}$, Zweigreaktanzen $x_\ell>0$ und $B_d=\mathrm{diag}(1/x_\ell)$. Ein Zweig $i\to j$ hat in $A_d$ am Abgang $+1$ und am Zugang $-1$. Der nodale Laplace-Operator lautet $L_d=A_dB_dA_d^{\mathsf T}$.

**(G1) Kirchhoff-Gleichungen [R/L].**

$$
L_d\theta_t=p_{d,t},\qquad f_{d,t}=B_dA_d^{\mathsf T}\theta_t,\qquad A_df_{d,t}=p_{d,t}.
$$

Voraussetzung ist $\mathbf1^{\mathsf T}p_{d,t}=0$ innerhalb jeder AC-Insel. Mit reduzierter Faktorisierung oder Pseudoinverser $L_d^{\dagger}$ folgt die nodale PTDF $H_d=B_dA_d^{\mathsf T}L_d^{\dagger}$ und

**(G2) Detaillierte Flussabbildung [R/L].**

$$
f_{d,t}=H_dp_{d,t}+b_t^{\phi},\qquad \mathbf1^{\mathsf T}p_{d,t}=0.
$$

$b_t^{\phi}$ ist ein **vorher berechneter physikalischer Offset** aus festgehaltenen Phasenschieber-/Transformatorzuständen, kein frei wählbarer Ersatznetz-Nullbilanzfluss. Die mathematischen Identitäten im Folgenden werden zunächst für $b_t^{\phi}=0$ hergeleitet und bei Bedarf um diesen Term erweitert. Die konkrete PTDF-Darstellung ist für balancierte Einspeisungen unabhängig von der Slack-Konvention; für unbalancierte Vektoren ist die Slack-Wahl dagegen entscheidend.

## 2.2 Zeit- und Zustandsindizes

$t\in\mathcal T$ bezeichnet synchron erfasste Stunden; $s\in\mathcal S$ Wetter-/Marktszenarien und $\Delta t_t$ ihre Dauer. Im IoSN-Ausgangsverfahren werden stündliche physikalische Flüsse aus einer Marktsimulation abgeleitet; die Impedanzoptimierung verwendet laut [E1] eine Stichprobe synchroner Flüsse. Die exakte Auswahl und Gewichtung dieser Stichprobe ist öffentlich nicht vollständig spezifiziert. Die im Text gegebenen Gewichtungen $w_t$ sind **eigene Entwurfsparameter** und müssen versioniert werden.

# 3. Die IoSN-Baseline als verbindlicher methodischer Referenzprozess

## 3.1 Dokumentierte Schritte [D]

1. NTC-basierte Marktsimulation und Gewinnung repräsentativer Last-/Erzeugungssituationen;
2. DC-/PTDF-basierte Berechnung detaillierter stündlicher Leitungsflüsse;
3. Priorisierung überlasteter Leitungen (225- und 400-kV-Bereiche werden im Anhang ausdrücklich genannt) durch jährliche Überlastungsenergie;
4. Zonierung: kritische Leitungen und relevante Austausch-Sensitivitäten sollen als Interzonenverbindungen möglichst sichtbar bleiben; Flussverhalten, Zonengröße und Konnektivität sind zusätzliche Kriterien;
5. für eine vorgegebene Busmap: Optimierung äquivalenter Impedanzen **und** struktureller Nullbilanzflusskorrekturen anhand synchroner Ziel-Flüsse;
6. Ableitung von vier Kapazitäten je Interzonenverbindung (Sommer/Winter, beide Richtungen) aus stündlichen physikalischen Leitungsflüssen und LODF-basierter N-1-Belastung;
7. iterative Anpassung der Busmap nach Fluss-RMSE und Kapazitätsqualität; Aufteilung der Markt-, Last-, Erzeugungs- und Speicherdaten auf Zonen.

**Quellen:** [E1, S. 21–29, 45–51]. Weder die vollständige Clustering-Zielfunktion noch die Optimierer-/Solverkonfiguration der Impedanzkalibrierung noch das allgemeine Kapazitätsregressionsmodell werden veröffentlicht. Gleichungen in den nächsten Abschnitten sind deshalb rekonstruiert oder zusätzlich vorgeschlagen.

## 3.2 Normative Bewertungsperspektive

Die zentrale Frage ist nicht, ob ein Verfahren ähnliche mathematische Begriffe verwendet, sondern **welche konkreten IoSN-Anforderungen** nachweisbar erfüllt werden. In jedem Methodenkapitel werden daher vier Kategorien ausgewiesen: (i) IoSN-Nähe, (ii) explizite Abweichungen, (iii) offene Daten-/Numerikannahmen, (iv) prüfbare Entscheidungskriterien.

# 4. Zwei eigenständige Clustering-Methoden

## 4.1 Methode A: vollständiger Dispatch und Überlastungsenergie

**[D/R]** Aus einem vollständig bilanzierten Dispatch, der konventionelle Erzeugung, Erneuerbare nach Abregelung, Speicher, HVDC-Terminale und Lasten einschließt, folgt für jede Stunde

$$
p_{d,t}^{A}=p_{\mathrm{RES},t}^{\mathrm{actual}}+p_{\mathrm{conv},t}+p_{\mathrm{storage},t}+p_{\mathrm{HVDC},t}-p_{\mathrm{load},t};\quad
f_{d,t}^{A}=H_dp_{d,t}^{A}+b_t^{\phi}.
$$

Hier sind alle Terme **Nettoeinspeisungen am AC-Knoten** und ihre Vorzeichen im Datenvertrag festgelegt. Die in [E1, Anhang 6.1] berichtete jährliche Überlastungsenergie kann als

**(C1) Überlastungsscore [D/R].**

$$
S_{\ell,s}^{A}=\sum_{t\in\mathcal T_s}\Delta t_t\,\max\{0,\lvert f_{\ell,t}^{A}\rvert-\overline F_{\ell,t}\}
$$

geschrieben werden. Mehrere Szenarien werden zunächst **getrennt** betrachtet; eine gewichtete Aggregation über Szenarien ist eine weitere, nicht normativ bestimmte Entscheidung.

**Optionale Optimierungsformulierung [E]:** Für eine zulässige Busmap $z$ mit $Z$ verbundenen Zonen minimiere man

$$
J_A(z)=\sum_{\ell=(i,j)}w^A_\ell\,\mathbb1\{z(i)=z(j)\},\qquad w^A_\ell\propto S_\ell^A,
$$

unter Konnektivitäts-, Zonenbudget- und Länderrestriktionen. Diese Formel ist eine **Forschungsrekonstruktion**, nicht der veröffentlichte Clustering-Code von ENTSO-E. Nicht jede kritische Leitung kann bei festem $Z$ zwangsläufig eine Zonengrenze werden.

**Stärken:** direkter Bezug zu potenziellen physikalischen Engpässen; Erfassung von Transit-, Import- und flexiblem Dispatch; gute IoSN-Treue. **Schwächen:** endogen gegenüber Marktergebnis, Brennstoffpreisen, Speicherstrategie und ggf. präventivem Redispatch; Extremstundengewichtung und Netzgrenzen beeinflussen die Rangfolge.

**IoSN-Abgleich:** *konzeptionell direkt* für Überlastungsenergie und Engpassschutz; *eigener Entwurf* für das konkrete gewichtete Clustering-Optimierungsproblem und die Wahl der Szenariogewichte.

## 4.2 Methode B: allgemeine RES-/Last-induzierte Leitungsbeanspruchung

**[E]** Um marktoptimierten konventionellen Dispatch im ersten Schritt zu vermeiden, werden die exogenen nodalen Größen

$$
q_t=p^{\mathrm{RES,avail}}_t-p^{\mathrm{load}}_t
$$

verwendet. Da $\mathbf1^{\mathsf T}q_t\ne0$ auftreten kann, ist $H_dq_t$ **ohne definierte Balancekonvention keine eindeutige physikalische Flusslösung**. Mit einem festen, nichtnegativen Ausgleichsvektor $w$ mit $\mathbf1^{\mathsf T}w=1$ wird

**(C2) Balanciertes Screening [E].**

$$
\widetilde q_t=q_t-w\,\mathbf1^{\mathsf T}q_t,\qquad
f^B_{d,t}=H_d\widetilde q_t.
$$

Bei mehreren Netzinseln gilt diese Bedingung **getrennt je Insel**. $w$ ist ein Screening-Proxy (etwa nach vorgegebener fixer Kapazität) und darf nicht als tatsächlich realisierter Marktdispatch bezeichnet werden. Die Sensitivität der Ergebnisse gegenüber mehreren $w$ ist explizit zu messen.

Ein sinnvoller Vergleich nutzt parallele Lastindikatoren:

**(C3) Gesamtbelastung [E].**

$$
E_\ell^B=\sum_t \Delta t_t\lvert f^B_{\ell,t}\rvert,\qquad
\rho_\ell^B=\frac{\sum_t\omega_t\lvert f^B_{\ell,t}\rvert/\overline F_{\ell,t}}{\sum_t\omega_t},
$$

sowie ein hohes Quantil $Q_{0.95}(|f_{\ell,t}^B|/\overline F_{\ell,t})$. Das erste Maß bewertet absolute Transferbeanspruchung, das zweite die Nutzung relativer zur verfügbaren Grenze; beide beantworten unterschiedliche Fragen. Als Busmap-Ziel können die nach Normierung gewichteten Scores den Verlust wichtiger Linien durch Verschmelzung bestrafen.

**Stärken:** exogenes, langfristiges Strukturmerkmal; Leitungen auch ohne Überlastung berücksichtigt; weniger direkte Abhängigkeit vom Marktclearing. **Schwächen:** schwache beziehungsweise falsche Flüsse bei ungeeignetem $w$; Abregelungen und niedrige RES-Stunden nicht repräsentiert; Transitflüsse und thermische Erzeugung fehlen als operative Treiber. Niedrige Grenzkosten der Erneuerbaren beweisen nicht, dass flexible Erzeugung elektrisch unwichtig ist.

**IoSN-Abgleich:** *explizite methodische Abweichung*: die IoSN priorisiert nicht den durchschnittlichen RES-/Last-induzierten Belastungsgrad als Ersatz für jährliche Überlastungsenergie. Methode B ist daher als **vergleichende Forschungsalternative** zu klassifizieren, nicht als ENTSO-E-konforme Rekonstruktion.

## 4.3 Gemeinsame Kriterien und fairer Vergleich

Bei A und B müssen Netztopologie, Zahl der Zonen $Z$, angeschlossene Komponenten, Spannungsregime, zulässige Ländergrenzen, Wetter-/Zeithorizonte, Konnektivität und nachgelagerte Identifikationsalgorithmen vergleichbar sein. Zusätzliche Qualitätsmerkmale sind (i) Schutz kritischer Schnittlinien, (ii) synchrone Flussrichtung/Korrelation, (iii) geringe Vorzeichenkompensation, (iv) zonale Größenbalance und (v) stabile Busmap über Wetterjahre. Die beiden Methoden können unterschiedliche $P_A,\Gamma_A$ und $P_B,\Gamma_B$ liefern.

**IoSN-Abgleich:** Flusssynchronität, zonale Konnektivität und begrenzte Clusterzahl sind in [E1, S. 23–25] ausdrücklich vorgesehen. Unsere Scores und Schutz-Penalties werden zusätzlich eingeführt.

# 5. Exakte Matrixaggregation und ihre Grenzen

## 5.1 Konstruktion von $P$ und $\Gamma$

Sei $P\in\{0,1\}^{Z\times N}$ die Busmap-Matrix mit genau einer Eins je Originalknoten. $\Gamma\in\{-1,0,1\}^{E\times L}$ summiert alle detaillierten Zweige, welche dieselben Zonen in derselben gewählten Orientierung verbinden; intrazonale Zweige erhalten ausschließlich Nullen. $A_z\in\mathbb R^{Z\times E}$ ist die Inzidenz des Zonengraphen.

**(A1) Algebraische Netzaggregation [R].**

$$
p_{z,t}=Pp_{d,t},\qquad f_{z,t}=\Gamma f_{d,t}.
$$

**(A2) Strukturelle Identität und Bilanzsatz [R].**

$$
\boxed{A_z\Gamma=PA_d}\quad\Longrightarrow\quad
\boxed{A_zf_{z,t}=p_{z,t}}.
$$

*Beweis:* Jede zwischen verschiedenen Zonen verlaufende Originalleitung hat auf beiden Seiten derselben Identität dieselben Vorzeichen; intrazonale Zweige heben sich in $PA_d$ auf und besitzen eine Nullspalte in $\Gamma$. Multiplikation mit $f_d$ und $A_df_d=p_d$ ergibt den Folgesatz. Bei HVDC gilt eine gesonderte Injektionskonvention, bei Verlusten eine bilanzrichtige Verlustallokation.

## 5.2 Was der Satz nicht impliziert

Diese Identität bewahrt Knotenbilanz, aber **nicht** die KVL-/Maschengleichungen, Einzelleitungsbelastungen, AC-Verluste oder N-1-Sicherheit. Insbesondere können gegengerichtete physikalische Grenzleitungen einen kleinen Schnittfluss $\Gamma f_d$ liefern, obwohl beide thermisch stark beansprucht sind. Die IoSN warnt ausdrücklich vor dieser Auslöschung [E1, S. 23].

Ein ergänzender Diagnoseindikator ist

$$
\chi_{e,t}=\frac{|(\Gamma f_d)_{e,t}|}{\sum_{\ell\in\mathcal L_e}|f_{\ell,t}|},
$$

für Stunden mit positivem Nenner. $\chi$ nahe null zeigt starke gerichtete Kompensation, nicht zwingend einen Modellfehler, aber ein Risiko für eine einzelne Ersatzkapazität.

**IoSN-Abgleich:** Die Matrixidentität ist unsere formale Rekonstruktion einer in [E1] impliziten Flussaggregation; die IoSN publiziert diesen Matrixsatz nicht als eigene Gleichung.

# 6. Technologiespezifische PTDFs und räumliche Verschiebungsfaktoren

## 6.1 Physik und Technologie strikt trennen

Für eine Technologieklasse $k$ (Wind, PV, Last, Kernkraft, Gas, Speicher usw.) definiere $p_{z,t}^{(k)}$ ihre zonale Einspeisung (Last negativ). Eine technologie- und ggf. zeitabhängige Matrix $R_k(t)\in\mathbb R^{N\times Z}$ beschreibt die räumliche Verteilung innerhalb der Zonen. Wo die Klasse vertreten ist, gilt $PR_k(t)=I_Z$; bei null installierter/aktiver Leistung ist ein dokumentierter Fallback nötig.

**(T1) Effektive technologiespezifische PTDF [R/E].**

$$
\boxed{H_z^{(k)}(t)=\Gamma H_dR_k(t)},\qquad
f_{z,t}=\sum_k H_z^{(k)}(t)\,p_{z,t}^{(k)}+\Gamma b_t^\phi.
$$

**Kein technologiespezifisches Netzgesetz:** $H_d$ bleibt dieselbe elektrische Matrix. Technologien verändern die Gewichtung, mit der zonale Leistung auf detaillierte Knoten verteilt wird. Entsprechend können Wind-, PV- und Lastbeiträge verschieden große beziehungsweise entgegengesetzte Grenzflüsse hervorrufen.

Eine positive Gewichtsregel für disponible/nicht disponible Erzeugung ist etwa

$$
(R_k(t))_{iz}=\frac{\sum_{g\in\mathcal G_{i,k}} P_g^{\mathrm{nom}}a_g(t)}{\sum_{j\in\mathcal N_z}\sum_{g\in\mathcal G_{j,k}}P_g^{\mathrm{nom}}a_g(t)},\qquad i\in\mathcal N_z.
$$

Für PV/Wind ist $a_g(t)$ die wetterabhängige Verfügbarkeit; für feste Leistungsshares kann $a_g\equiv1$ gelten. Lastgewichte beruhen auf nodalen Nachfrageprofilen; die Vorzeichen stehen in $p_{z,t}^{(\mathrm{load})}$, **nicht** in $R_{\mathrm{load}}$.

## 6.2 Exakte relative No-Load-Flusszerlegung

Wähle eine Referenzverteilung $R_0$ mit $PR_0=I$. Für den detaillierten gesamten Einspeisevektor $p_{d,t}$ gilt

$$
p_{d,t}=R_0p_{z,t}+u_t,\qquad u_t=(I-R_0P)p_{d,t},\qquad Pu_t=0.
$$

**(T2) Strukturfluss unter Nulländerung der Zonenbilanz [R].**

$$
\boxed{f_{z,t}=\Gamma H_dR_0p_{z,t}+c_{\mathrm{struct}}(t)+\Gamma b_t^\phi},\qquad
c_{\mathrm{struct}}(t)=\Gamma H_d(I-R_0P)p_{d,t}.
$$

Es gilt $A_zc_{\mathrm{struct}}(t)=0$. Der Strukturfluss ist **referenzabhängig** und kann zeitabhängig sein. Für eine Technologienzerlegung folgt

$$
c_{\mathrm{struct}}(t)=\sum_k\Gamma H_d\,[R_k(t)-R_0]p_{z,t}^{(k)}.
$$

Der aus RES und Last isolierte Anteil folgt identisch, indem statt $p_d$ nur $q=p_{\mathrm{RES},avail}-p_{\mathrm{load}}$ in $(I-R_0P)q$ eingesetzt wird. Dieser intrazonale Strukturvektor ist **per Konstruktion bilanziert**, selbst wenn $q$ insgesamt keine ausgeglichene Einspeisung ist. Er kann somit schon für eine feste Busmap ohne Markt-Dispatch ausgewertet werden. Er ist allerdings nur ein **Teil** der vollständigen strukturellen Korrektur.

**IoSN-Abgleich:** [E1, S. 48] beschreibt die „zero balance flow corrections“ wegen räumlicher Last-/Erzeugungsasymmetrien, veröffentlicht aber keine Technologienzerlegung. (T2) ist eine eigene mathematische Erklärung und ein möglicher Verbesserungsansatz, nicht die publizierte IoSN-Parameteridentifikation.

# 7. Referenzverteilungen, Merit Order und Ersatzknoten

## 7.1 Drei Verteilungsoperatoren [E]

Für eine Zone $z$ und den Knoten $i\in z$ werden drei Kandidaten definiert:

- **Gleichverteilung:** $R_{{\mathrm{uni}},iz}=1/|\mathcal N_z|$.
- **Kapazitätsgewichtung:** $R_{{\mathrm{cap}},iz}=C_i/\sum_{j\in z}C_j$ mit installierter geeigneter Leistung $C_i\ge0$.
- **Kostenbasierte Präferenz:** $R_{{\mathrm{cost}},iz}=C_i\psi(c_i)/\sum_{j\in z}C_j\psi(c_j)$ mit vorab definierter monoton fallender positiver $\psi$ und festen Grenzkosten $c_i$.

Die dritte Variante ist ein **glatter Kostenproxy**, keine strenge Merit Order. Eine echte stufenweise Merit-Order-Allokation löst für einen gegebenen zonalen Residualbedarf $D_z$ etwa

$$
\min_g\sum_{i\in z}c_i g_i\quad\text{unter}\quad \sum_{i\in z}g_i=D_z,\quad0\le g_i\le C_i.
$$

Fixe Preise implizieren **nicht** fixe Gewichte: Die Lösung ändert sich mit dem Bedarf $D_z$. Für eine zeitlich konstante Referenz kann ein definiertes Ensemble repräsentativer Residualbedarfsniveaus $D_z^{(r)}$ verwendet und $g_i^{(r)}$ mit veröffentlichten Gewichten gemittelt werden. Bei nicht flexiblen Kernkraftwerken müssen Verfügbarkeit, Mindestlast und Betriebsrestriktionen gesondert beachtet werden.

## 7.2 Gemeinsame Referenz-PTDF und einzelner Ersatzknoten

Für eine gewählte Referenz $R$ folgt $H_z^{\mathrm{ref}}=\Gamma H_dR$. Alternativ kann eine Spalte $r_z$ durch einen einzelnen Originalknoten $i_z\in\mathcal N_z$ ersetzt werden. Ein elektrisch sinnvoller Kandidat löst

$$
 i_z^*\in\arg\min_{i\in\mathcal N_z}
 \left\|W\Gamma H_d(e_i-R_{:,z})\right\|_2.
$$

Die Ein-Knoten-Näherung erhöht die Interpretierbarkeit, kann aber die Genauigkeit erheblich verschlechtern. Die Referenzknotenwahl bestimmt auch nicht allein die Ersatzreaktanz; dazu ist anschließend eine elektrisch realisierbare zonale Netzmatrix zu identifizieren.

**IoSN-Abgleich:** [E1] verlangt die Kalibrierung äquivalenter Reaktanzen und Flusskorrekturen, aber keine kostenbasierte Referenz-PTDF oder Auswahl eines einzigen physikalischen Ersatzknotens. Diese drei Varianten sind ausdrücklich **eigene Forschungshypothesen**.

## 7.3 Begriffsklärung „MCOE“

In den vorliegenden Ausgangsdokumenten ist *MCOE* nicht als verifizierte eigenständige mathematische Normform definiert. Eine „Distanz zur MCOE-Formulierung“ kann nur gegenüber einer **offengelegten** Gleichung belastbar beurteilt werden. Hier wird daher ausschließlich der klar definierte marginalkostenbasierte Merit-Order-Proxy bzw. die kapazitätsbeschränkte Kostenminimierung verglichen; eine weitergehende normative Äquivalenz wird nicht behauptet.

# 8. Ersatznetzimpedanzen und struktureller Flussoffset $F_0$

## 8.1 Vom detaillierten Schnittfluss zum realisierbaren Ersatznetz

Aus $\Gamma H_dR_0$ folgt eine *aggregierte Sensitivitätsmatrix*, aber nicht notwendigerweise eine PTDF, die durch positive Reaktanzen auf der gewählten reduzierten Topologie realisierbar ist. Für den Zonengraphen seien $A_z\in\mathbb R^{Z\times E}$ und $X_z=\mathrm{diag}(x_e^{\mathrm{eq}})$, $x_e^{\mathrm{eq}}>0$. Dann ergibt sich die passive zonale PTDF

$$
H_{\mathrm{eq}}(x)=X_z^{-1}A_z^{\mathsf T}
(A_zX_z^{-1}A_z^{\mathsf T})^{\dagger}.
$$

Für eine zulässige Zoneneinspeisung $p_z$ ist der DC-Fluss $H_{\mathrm{eq}}(x)p_z$. Um intrazonal ausgelöste Loop-Flows abzubilden, kann man einen über die Kalibrierungsperiode konstanten Nullbilanzfluss $c^0$ ergänzen:

**(E1) Affines Ersatznetzmodell [R/E].**

$$
\boxed{\widehat f_{z,t}=H_{\mathrm{eq}}(x)p_{z,t}+c^0},\qquad A_zc^0=0.
$$

Die Knotenbilanz bleibt $A_z\widehat f_{z,t}=p_{z,t}$. Mit einer beliebigen Zyklenbasis $C_z$ des reduzierten Netzes gilt die **modifizierte** Maschenbeziehung

$$
\boxed{C_z^{\mathsf T}X_z(\widehat f_{z,t}-c^0)=0}.
$$

Der Offset ist somit ein **explizit modellierter affiner KVL-Beitrag**. Ein gewöhnlicher passiver PyPSA-Lastfluss ohne zusätzliche Gleichungen reproduziert im Allgemeinen **keine** von null verschiedenen Flüsse bei $p_z=0$; sie dürfen nicht bloß nachträglich in einem Ergebnisfeld addiert und dann als physikalisch bindend bezeichnet werden. Für einen festgesetzten $c^0$ ist eine algebraische Emulation über äquivalente Branch-Source-Terme möglich; diese sind aber keine Aussage über reale PSTs.

## 8.2 Kalibrierungsproblem und Zerlegung des Fehlers

**(E2) Explizit vorgeschlagene, nicht normativ vorgegebene Identifikation [E].**

$$
\begin{aligned}
\min_{x,c^0}\quad&
 \sum_{t\in\mathcal T_{\mathrm{cal}}}\omega_t
 \left\|W_f\left[H_{\mathrm{eq}}(x)p_{z,t}+c^0-\Gamma f_{d,t}\right]\right\|_2^2
 +\lambda_x\|\log(x/x^{\mathrm{prior}})\|_2^2
 +\lambda_c\|c^0\|_2^2,\\
\text{unter}\quad &x_{\min}\le x\le x_{\max},\qquad A_zc^0=0,
\end{aligned}
$$

wobei $W_f$ z. B. nach kritischen Verbindungen oder Referenzflüssen gewichtet. Die genaue Gewichtung, Regularisierung und der Solver sind **eigene Entscheidungen**. ENTSO-E nennt als Aufgabe die gemeinsame Minimierung des Flussfehlers durch Impedanzen und strukturelle Korrekturen, nicht das vollständige mathematische Programm [E1, S. 27, 48–49].

Bei vorgegebenem $R_0$ folgt die fehlerdiagnostische, exakte Zerlegung

$$
\Gamma f_{d,t}-H_{\mathrm{eq}}(x)p_{z,t}
=\underbrace{\Gamma H_d(I-R_0P)p_{d,t}}_{\text{Verlust intrazonaler Verteilung}}
+\underbrace{(\Gamma H_dR_0-H_{\mathrm{eq}}(x))p_{z,t}}_{\text{elektrische Ersatznetzabweichung}}
+\Gamma b_t^\phi.
$$

**Wissenschaftlicher Nutzen:** Die technologiespezifische Zerlegung erklärt den *räumlichen* Beitrag, während die Impedanzidentifikation den *netzstrukturellen* Beitrag approximiert. Ein frei optimiertes $c^0$ kann beide Anteile überlagern; Attribution und Identifikationsparameter müssen deshalb auseinandergehalten werden.

## 8.3 Identifizierbarkeit

Wenn alle positiven zonalen Reaktanzen eines zusammenhängenden AC-Zonennetzes mit demselben Faktor $\eta>0$ skaliert werden, bleiben die DC-Flüsse bei vorgegebenen Einspeisungen unverändert:

$$
H_{\mathrm{eq}}(\eta x)=H_{\mathrm{eq}}(x).
$$

Diese globale Skalierungsfreiheit muss etwa durch eine feste Referenzreaktanz oder eine physikalische Priorinformation gebrochen werden. Bei einem **baumförmigen Zonennetz** ist die gesamte Flussverteilung bereits durch KCL eindeutig; die Reaktanzen sind aus Flussdaten **überhaupt nicht identifizierbar**. Ein kleiner RMSE in diesem Fall ist kein Nachweis der elektrischen Qualität. Auch in vermaschten Netzen sind Rang der Anregung über die Stunden und Parameterkorrelationen zu prüfen.

**IoSN-Abgleich:** [E1, S. 48] benennt ausdrücklich die fehlende Eindeutigkeit und den Kompromiss zwischen Robustheit und Genauigkeit. Unsere analytische Identifizierbarkeitsprüfung konkretisiert diese Aussage.

# 9. N-1-Sicherheitsabbildung: detaillierte PTDF und LODF

## 9.1 Leitungsausfälle und vollständiger Kontingenzoperator

Für den Ausfall von Zweig $k$ sei $d_k=A_{d,:,k}$ die zugehörige nodale Transaktion. Mit $T=H_dA_d$ und einem **nicht inselbildenden** Einzelausfall gilt

**(N1) Line Outage Distribution Factors [L/R].**

$$
D_{\ell k}=\frac{T_{\ell k}}{1-T_{kk}}\quad(\ell\ne k),\qquad D_{kk}=-1,
$$

und somit $f_\ell^{(k)}=f_\ell+D_{\ell k}f_k$. Für Brücken/Ausfälle, die das AC-Netz separieren, ist der Nenner null oder numerisch unbrauchbar; solche Fälle dürfen **nicht** stillschweigend als sicher gelten. Andere Topologieänderungen oder Gegenmaßnahmen benötigen separate Modelle.

Sei $K\in\mathbb R^{C\times L}$ eine Matrix aus Zeilen $e_\ell^{\mathsf T}$ (N-0) und $e_\ell^{\mathsf T}+D_{\ell k}e_k^{\mathsf T}$ (überwachter Zweig $\ell\ne k$ unter Ausfall $k$). Dann

**(N2) Gekoppelte N-1-Sicherheitsregion [L/R].**

$$
\boxed{-\overline f_C\le K(H_dp_d+b^\phi)\le\overline f_C}.
$$

Jedem Überwachungsfall wird die zugehörige zulässige (ggf. saisonale) MW-Grenze zugeordnet. $K$ ist ein **CNEC-Selektions-/Transformationsoperator**, kein Aggregationsoperator $\Gamma$.

## 9.2 Direkte zonale N-1-Projektion bei festem räumlichem Schlüssel

Für $p_d=Rp_z+u$, $PR=I$ und $Pu=0$ gilt

**(N3) N-1-Sicherheitsabbildung in zonale Nettopositionen [R/E].**

$$
\boxed{-\overline f_C\le H_{C,z}p_z+f_{0,C}\le\overline f_C},
$$

mit $H_{C,z}=KH_dR$ und $f_{0,C}=K(H_du+b^\phi)$. Diese Formulierung ist in der linearen Netzapproximation **exakt konditional** auf $R$, $u$, Topologie, fixierte PST-/HVDC-Einwirkungen und die betrachteten Kontingenzen.

Die Wahl des intra-zonalen Betriebs ist hierbei entscheidend:

- **Feste intrazonale Struktur:** $u=u^{\mathrm{ref}}$ ergibt ein einzelnes gekoppeltes Zonensicherheits-Polyeder.
- **Existenzielle Projektion:** $p_z$ gilt als zulässig, wenn ein $u\in\mathcal U$ existiert, das sämtliche Restriktionen erfüllt; dies bildet die erlaubte Re-Dispatch-Flexibilität ab, benötigt aber ihre technische Beschreibung.
- **Robuste Projektion:** $p_z$ gilt nur als zulässig, wenn die Restriktionen für **jedes** $u\in\mathcal U$ gelten; dieses Polyeder ist meist konservativer.

Die letzte Unterscheidung ist für die langfristige Planung wesentlich: Eine feste GSK-Verteilung ist weder automatisch eine vollständige noch eine robuste Projektion aller operativen Freiheitsgrade.

## 9.3 Sichere bilaterale Handelsänderung

Für einen **N-1-sicheren Referenzzustand** $p_z^{\mathrm{ref}}$ und den Transfervektor $d_{ab}=e_a-e_b$ gilt $p_z(\tau)=p_z^{\mathrm{ref}}+\tau d_{ab}$ mit $\tau\ge0$. Definiere $b=H_{C,z}p_z^{\mathrm{ref}}+f_{0,C}$ und $g=H_{C,z}d_{ab}$.

**(N4) Maximale sichere Transfererhöhung [R].**

$$
\boxed{\tau_{\max}^{a\to b}=\min_{r:\,g_r\ne0}
\frac{\overline f_{C,r}-\operatorname{sgn}(g_r)b_r}{|g_r|}}
$$

unter den Nebenbedingungen, dass alle $g_r=0$ bereits zulässig sind, die Basis $|b_r|\le\overline f_{C,r}$ ist und alle N-0-/N-1-Restriktionen enthalten sind. Für eine Gegenrichtung wird $d_{ab}$ negiert. Ist die Menge der einschränkenden Zeilen leer, ist $\tau$ hinsichtlich **dieser** Restriktionen unbeschränkt; weitere Markt-/Erzeugungsgrenzen fehlen dann noch.

Der Wert ist **keine universelle Ersatzkapazität der Verbindung $e=(a,b)$**: Eine bilaterale Nettopositionsänderung verteilt sich über sämtliche parallelen und vermaschten Pfade. Der zulässige Wert hängt von $p_z^{\mathrm{ref}}$, $R$ und anderen Transaktionen ab.

## 9.4 Unterschied zwischen Sicherheits-Polyeder und vier Grenzwerten

Die durch (N3) definierte Region enthält gekoppelte Restriktionen. Unabhängig je Ersatzverbindung maximierte Schnittflüsse $\max\{(\Gamma f_d)_e\}$ bilden in der Regel nur ein **achsparalleles äußeres Begrenzungsrechteck**; die gleichzeitige Ausschöpfung aller Maxima kann unzulässig sein. Eine garantiert sichere innere Approximation benötigt zusätzliche robuste Restriktionen oder eine explizite Inklusionsprüfung.

**IoSN-Abgleich:** [E1, S. 50–51] bestimmt vier saisonale, gerichtete Ersatzkapazitäten aus stündlichen Grenzflüssen und N-1-Maximalbelastungen sowie Sonderregeln für einseitigen Fluss und unzureichend identifizierbare Daten. (N3) und (N4) sind **alternative analytische Referenzmethoden**, nicht dieselbe Kapazitätsschätzung. Ein direkter zahlenmäßiger Vergleich ohne identischen Referenzzustand und identische Sicherheitsmengen ist methodisch unzulässig.

## 9.5 Analytische Dreiknotenillustration [A/S]

Ein Dreiecksnetz mit identischen Zweigreaktanzen besitzt drei Leitungen A–B (100 MW), B–C (100 MW) und C–A (80 MW). Bei einer A-zu-B-Transaktion $\tau$ fließen im Normalzustand $2\tau/3$ über A–B und jeweils $\tau/3$ über den alternativen Weg. Die N-0-Grenze beträgt daher 150 MW. Nach Ausfall von A–B fließt die gesamte Transaktion über den alternativen Weg; C–A wird bereits bei 80 MW bindend. Unter Berücksichtigung aller drei möglichen Einfachausfälle ergibt die N-1-Transfergrenze **80 MW**. Dies zeigt unmittelbar, warum eine Addition der thermischen Leitungsgrenzen weder eine korrekte N-0- noch eine N-1-Kapazität liefert.

Der begleitende Python-Test `test_triangle_transfer_n0_150_n1_80` prüft diese Aussage als analytischen Referenzfall. Es handelt sich ausdrücklich um **synthetische Daten** und nicht um eine TYNDP-Topologie.

# 10. Drei Kapazitätsmethoden und ihre Aussagekraft

## 10.1 K1: IoSN-nahe stündliche Ersatzkapazität [D/R]

Für jede reduzierte Verbindung $e$ werden stündliche Schnittflüsse $F_{e,t}=(\Gamma f_{d,t})_e$ und die maximalen N-1-Belastungen beteiligter kritischer physikalischer Zweige ausgewertet:

$$
\rho_{e,t}^{N-1}=\max_{(\ell,k)\in\mathcal C_e}\frac{|f_{\ell,t}+D_{\ell k}f_{k,t}|}{\overline f_{\ell,t}}.
$$

N-0-Überwachungsfälle gehören ebenfalls in die Sicherheitsprüfung. Nach Sommer/Winter und Vorzeichen von $F_{e,t}$ werden vier bedingte Transfergrenzen nahe der 100-%-Belastung identifiziert. Die ENTSO-E erläutert Sonderfälle: über 99,5 % einseitige Flüsse, unzureichende Stützstellen nahe 100 %, Schwellen von 1 % bzw. 130 % und diffuse Punktwolken [E1, S. 50–51]. Das konkrete statistische Schätzverfahren ist nicht vollständig offengelegt; eine lineare Regression mit Intercept ist **nur ein Forschungsproxy**, kein verifizierter Originalalgorithmus.

**Stärke:** betriebszustandsbezogene, praxisnahe Kapazität je Ersatzlink. **Schwäche:** daten- und stichprobenabhängig, mögliche Scheinkorrelation und nicht garantierte gleichzeitige Sicherheit.

## 10.2 K2: analytische N-1-Polyederprojektion [R/E]

K2 bewahrt die einzelnen N-0-/N-1-Restriktionen (N3); Transfergrenzen sind (N4), oder für die äquivalente Schnittflussgröße kann über die gesamte zulässige Domäne ein lineares Programm gelöst werden:

$$
\max_{p_z\in\mathcal P}\ \pm e_e^{\mathsf T}\Gamma H_d(Rp_z+u^{\mathrm{ref}})
\quad\text{unter}\quad
-\overline f_C\le H_{C,z}p_z+f_{0,C}\le\overline f_C.
$$

Die Menge $\mathcal P$ umfasst Balanz, Grenzen verfügbarer Technologien und ggf. vertragliche Austauschlimits. Ohne diese zusätzlichen Schranken können einzelne Optimierungen unbeschränkt sein. Ein positiver LP-Optimalwert ist eine **Stützfunktion** einer zulässigen Flussmenge, nicht automatisch ein zulässiger gemeinsamer Link-Kapazitätsvektor.

**Stärke:** mathematisch klarer Sicherheitsbezug; direkt für FBMC-artige Nebenbedingungen. **Schwäche:** größere Restriktionszahl; Modell muss räumliche Flexibilität und N-1-Sonderfälle korrekt behandeln; kapazitätsorientiertes IoSN-Format muss zusätzlich approximiert werden.

## 10.3 K3: robuste Derating-Approximation [L/E]

Eine konservative Alternative beschränkt bereits die N-0-Flüsse auf $|f_\ell|\le\alpha_\ell\overline f_\ell$. Aus

$$
|f_\ell^{(k)}|\le |f_\ell|+|D_{\ell k}|\,|f_k|
$$

folgt die **hinreichende** Sicherheitsbedingung

**(N5) Konservativer leitungsspezifischer Sicherheitsfaktor [E].**

$$
\alpha_\ell\overline f_\ell+
|D_{\ell k}|\alpha_k\overline f_k\le\overline f_\ell
\qquad(\ell\ne k),\quad 0\le\alpha\le1.
$$

Bei einem gemeinsamen Faktor ist

$$
\boxed{\alpha_{\mathrm{common}}=\min\left\{1,\ \min_{\ell\ne k}
\frac{\overline f_\ell}{\overline f_\ell+|D_{\ell k}|\overline f_k}\right\}}.
$$

Diese explizit **hier abgeleiteten** Schranken sind konservativ, da sie mögliche Korrelationen physikalischer Flüsse ignorieren. Sie setzen voraus, dass der angewandte N-0-Boxbereich tatsächlich die vollständigen modellierten Flüsse beschränkt; feste Offsets dürfen nicht fehlen. [N2] untersucht verwandte robuste, approximative und leitungsspezifische Verfahren, verwendet aber nicht notwendig dieselben Formeln.

**IoSN-Abgleich:** K3 ist **kein Ersatz für die dokumentierten IoSN-Kapazitäten**, sondern ein kostengünstiger Vergleichs-/Sicherheitsbenchmark. Gute konservative K3-Werte müssen nicht dieselben Transfermöglichkeiten wie K1 oder K2 liefern.

## 10.4 Qualität der Sicherheitsregion

Die drei Methoden sollten unter identischem detailliertem N-1-Prüfsatz anhand folgender Kennzahlen verglichen werden: (i) Anteil fehlerhaft zugelassener Einspeisungen (false feasible), (ii) Anteil unnötig ausgeschlossener, detailliert sicherer Einspeisungen (false infeasible), (iii) Verletzungshöhe und -dauer, (iv) zulässige Transferenergie in repräsentativen Stunden, (v) rechnerischer Aufwand und (vi) Sensitivität auf Wetterjahre, GSK/Verteilung, Outage-Sets und Sondergeräte. K1 ist nicht per Konstruktion N-1-garantiert, K2 unter klaren Bedingungen schon, K3 ist konservativ.

# 11. Woodbury-Identität und duale LODF-Theorie

## 11.1 Sherman–Morrison–Woodbury für Einzelkontingenzen

Schneidet man zur Lösung des balancierten AC-Teilnetzes den Referenzknoten aus, ist der reduzierte nodale Laplace-Operator $L_r$ regulär. Ein nicht inselbildender Ausfall von Zweig $k$ mit Suszeptanz $b_k=1/x_k$ verändert ihn mit Rang eins:

$$
L_r^{(k)}=L_r-b_ka_ka_k^{\mathsf T}.
$$

**(W1) Woodbury-Rang-eins-Update [L].**

$$
\boxed{(L_r^{(k)})^{-1}=L_r^{-1}+
\frac{b_kL_r^{-1}a_ka_k^{\mathsf T}L_r^{-1}}
{1-b_ka_k^{\mathsf T}L_r^{-1}a_k}.}
$$

Bei singulärem Nenner ist das Netz nach dem Ausfall nicht mit derselben regulären Teilnetz-Faktorisierung behandelbar. Im produktiven numerischen Verfahren sollten **faktorisierte lineare Systeme statt expliziter inverser Matrizen** verwendet werden. Woodbury beschleunigt die Kontingenzberechnung, bestimmt aber nicht selbst die zonalen Sicherheitsgrenzen.

## 11.2 Duale Zyklendarstellung

Sei $C_d\in\mathbb R^{L\times(L-N+1)}$ eine Basis von $\ker A_d$ und $X_d=\mathrm{diag}(x)$. Definiere

$$
M=C_d(C_d^{\mathsf T}X_dC_d)^{-1}C_d^{\mathsf T}.
$$

Für nicht inselbildende Zweige gilt die duale Darstellung [N1]:

**(W2) Kreisraum-basierte LODF [L].**

$$
\boxed{D_{\ell k}=-M_{\ell k}/M_{kk}\quad(\ell\ne k)},\qquad D_{kk}=-1.
$$

Auch diese Darstellung scheitert im Grenzfall einer Brücke: Eine Brücke liegt in keinem Kreis und hat $M_{kk}=0$. Für **schwach vermaschte Netze** mit wenigen unabhängigen Zyklen kann die Kreisraumformulierung attraktiv sein. Welcher Ansatz schneller ist, hängt von Sparse-Faktorisierung, Zahl der Kontingenzen und Netzstruktur ab und muss empirisch benchmarkiert werden.

**IoSN-Abgleich:** Das IoSN-Dokument nennt LODF-basierte N-1-Bewertung, aber weder Woodbury noch die duale Kreisformel als verpflichtenden Rechenkern. Beide sind technisch austauschbare Beschleunigungsoptionen, keine normative Weiterentwicklung des Clustering-Prinzips.

# 12. Verbindung zu Flow-Based Market Coupling (FBMC)

## 12.1 Planungsknoten sind keine Marktgebotszonen

Die IoSN-Busmap $P_T$ erzeugt Planungszonen und der Schnittoperator $\Gamma_T$ aggregiert Leitungstransfers. Im FBMC wird dagegen eine **Gebotszonenmatrix** $P_B$ verwendet; sie ist im Allgemeinen nicht identisch mit $P_T$. Ein GSK/GLSK $G_B$ verteilt **marginale Änderungen** zonaler Nettohandelspositionen auf detaillierte elektrische Knoten. Typischerweise soll $P_BG_B=I$ gelten, wenn jede Spalte nur innerhalb ihrer Gebotszone wirkt.

Für die kritischen Elemente und Kontingenzen verwendet FBMC den Sicherheitsoperator $K$, nicht $\Gamma_T$:

**(F1) Zonale sensitivitätsbasierte FBMC-PTDF [R/L].**

$$
\boxed{Z_{\mathrm{FB}}=KH_dG_B}.
$$

Demgegenüber beschreibt $H_T^{(k)}=\Gamma_TH_dR_k$ die Wirkung einer *räumlichen Einspeisungsverteilung* auf *summierte Interzonenflüsse*. Beide sind Sonderfälle der gleichen Kette „nodale PTDF mal Disaggregationsoperator, anschließend Beobachtungsoperator“, aber ihre physikalischen **Outputs unterscheiden sich**.

## 12.2 Struktureller Nullbilanzfluss versus FBMC-Nullpositionsfluss

Für einen vollständig bilanzierten nodalen Referenzzustand $p_d^{\mathrm{ref}}$ ist $NP^{\mathrm{ref}}=P_Bp_d^{\mathrm{ref}}$. Die zugehörige CNEC-Flussprognose und ihr theoretischer Nullpositionsintercept lauten

**(F2) Affine Flow-Based Domain [R/E].**

$$
\begin{aligned}
f_C^{\mathrm{ref}}&=K(H_dp_d^{\mathrm{ref}}+b^\phi),\\
f_{0,\mathrm{FB}}&=f_C^{\mathrm{ref}}-KH_dG_BNP^{\mathrm{ref}}\\
&=KH_d(I-G_BP_B)p_d^{\mathrm{ref}}+Kb^\phi,\\
f_C(NP)&\approx Z_{\mathrm{FB}}NP+f_{0,\mathrm{FB}}.
\end{aligned}
$$

Der IoSN-Strukturfluss ist hingegen $\Gamma_TH_d(I-R_TP_T)p_d$, also mit **anderer Partition, anderem Shift-Key und anderem beobachteten Fluss**. Darüber hinaus sind operative Größen wie *F0core/F0all*, *FRM*, *RAM* und *Remedial Actions* pro Kapazitätsberechnungsregion methodisch zusätzlich spezifiziert. Der theoretische $f_{0,\mathrm{FB}}$ darf deshalb nicht einfach mit einem operativ veröffentlichten RAM-Input gleichgesetzt werden.

Für eine symmetrische vereinfachte thermische Grenze (keine weiteren regulatorischen Anpassungen) erhält man

$$
-\overline f_C\le Z_{\mathrm{FB}}NP+f_{0,\mathrm{FB}}\le\overline f_C,
\qquad \mathbf1^{\mathsf T}NP=0.
$$

Nach Berücksichtigung eines separat definierten Reliability Margins $FRM$ entsteht je Richtung ein vereinfachter RAM-Proxy, z. B. $RAM_C^+=\overline f_C-FRM_C-f_{0,\mathrm{FB}}$. Operatives FBMC enthält weitere regionale Vorgaben und braucht eine eigene Daten-/Regulierungsqualifikation [P3].

## 12.3 Wozu die Verbindung wissenschaftlich dient

Die bisherige Netzreduktion prüft den Fehler im **summierten Flussraum**. FBMC ergänzt einen Test der **kritischen Leitungs- und Kontingenzsensitivitäten**. Ein Zonennetz kann kleine Schnittflussfehler aufweisen und dennoch wichtige interne CNEC-Sensitivitäten ungenau abbilden. Deshalb sind für die Validierung beide Metrikfamilien erforderlich:

$$
\varepsilon_{\mathrm{cut}}=\|\widehat f_z-\Gamma f_d\|,
\qquad
\varepsilon_{\mathrm{CNEC}}=\|\widehat H_C-H_C\|,
$$

wobei die zweite Norm nur bei kompatiblen Zonen, identischen GSK-Hypothesen und demselben CNEC-Satz sinnvoll ist. Die Marktregion wird **zusätzlich** durch falsch sichere/zu restriktive Nettohandelspositionen bewertet. Eine einzelne IoSN-Ersatzkapazität ist **nicht** automatisch RAM und kann nicht anstelle des vollständigen CNEC-Polyeders in den Core-Marktprozess eingebaut werden.

**IoSN-Abgleich:** In [E1, S. 22] wird das zonale Modell als näher an flow-based physikalischem Verhalten als ein reines NTC-Modell charakterisiert. Die hier behandelte CNEC-/GSK-Mathematik ist eine **theoretische Querbeziehung**, keine Aussage, dass die IoSN denselben Algorithmus wie Core-FBMC verwendet.

# 13. Rolle der reduzierten Netze im IoSN-Ausbauproblem

**[D]** Abschnitt 3.9 unterscheidet die ursprüngliche IoSN-Ausbauoptimierung im **Load-Flow-Modus** (physikalische Maschengleichungen, aber spezifisch behandelte interne Kapazitätsgrenzen) von nachgelagerten Dispatch-/OPF-Untersuchungen mit expliziten inneren Beschränkungen. Der Originaltext ist in einem Detail terminologisch unscharf: Er nennt einerseits aktivierte grenzüberschreitende Kapazitäten, andererseits unendliche „interzone capacities“ im LF-Modus. Eine reproduzierbare Umsetzung muss daher **für jede Ersatzverbindung** festlegen, ob ihre Grenze im LF-Ausbauschritt, in der OPF-Validierung oder in beiden aktiv ist [E1, S. 29].

Die IoSN-Ersatzkapazitäten sind damit **Modellparameter**, deren Verwendung vom Ausbauschritt abhängt. Ein verbesserter N-1-Kapazitätsschätzer erhöht nicht automatisch die Qualität der LF-Ausbauentscheidung, wenn dessen interne Restriktionen bewusst nicht bindend gesetzt werden. Deshalb müssen Netzreduktionsfehler auch anhand ihrer Auswirkungen auf Netzausbau-, Redispatch- und Wohlfahrtsindikatoren geprüft werden.

# 14. Durchgehender wissenschaftlicher Methodenvergleich

## 14.1 Clustering und räumliche Aggregation

| Ansatz | Stärken | Schwächen | Nähe zur IoSN |
|:--|:--|:--|:--|
| A: Dispatch/Überlastung | Relevanz für reale Engpässe; vollständiger Betriebszustand | Marktdispatch- und Redispatchabhängigkeit | **Hoch** für Kriterium; Algorithmus nur rekonstruiert |
| B: RES/Last-Belastung | Exogene strukturelle Korridore; schließt nicht überlastete Leitungen ein | Bilanzkonvention, ausgelassene Transit-/Flexflüsse | **Abweichende Alternative** |
| $P,\Gamma$-Aggregation | Exakte zonale Bilanz; lineare Sparse-Operatoren | Keine KVL-/N-1-Garantie | **Kompatible Formalisierung** |
| Technologie-$R_k$ | Explizite räumliche PV-/Wind-/Lastinformation | Zeitvariable, nicht eindeutig bei Nullverfügbarkeit | **Erweiterung** der strukturellen Korrektur |
| Kosten-/Kapazitäts-$R$ | Transparente, testbare Referenzen | Kostenproxy nicht gleich marginalem Einsatz | **Nicht vorgeschrieben** |
| Ersatzknoten | Interpretierbar, reduziert Modellkomplexität | Zusätzlicher PTDF-Fehler | **Nicht vorgeschrieben** |

## 14.2 Elektrische Reduktion und Sicherheit

| Ansatz | Stärken | Schwächen | Nähe zur IoSN |
|:--|:--|:--|:--|
| Ersatz-$x$ und $c^0$ | Vermaschtes, kompaktes Wirkflussmodell | Nicht eindeutige Identifikation; affine Semantik | **Direkt angelegt** |
| K1: stündliche N-1-Ersatzkapazität | Vier markt-/wetterbezogene Linkgrenzen | Stützstellen- und Korrelationsabhängigkeit | **Direkt dokumentiert** |
| K2: vollständige CNEC-Polyederprojektion | Konditional exakte Sicherheit im DC-Modell | Viele Restriktionen; $R,u$ erforderlich | **Erweiterung** |
| K3: robuste Derating-Box | Geringe Rechenlast; konservativ sicher | Häufig restriktiver als notwendig | **Alternative** |
| Woodbury/duale LODF | Potenziell schnellere Sensitivitätsberechnung | Insel-/Sparse-/Benchmarkbedarf | **Rechentechnik**, nicht IoSN-Vorgabe |
| FBMC-GSK/CNEC | Handelsrelevante Sensitivitäten und Sicherheit | Andere Zonen und operative RAM-Semantik | **Benachbarte Anwendung** |

## 14.3 Wesentliche Nicht-Äquivalenzen

1. **Bilanztreue $\not\Rightarrow$ elektrische Ersatznetzäquivalenz.**
2. **Effektive Technologie-PTDF $\not\Rightarrow$ neue physikalische PTDF.**
3. **Fester Grenzkostenvektor $\not\Rightarrow$ zeitlich konstante Merit-Order-Einspeisung.**
4. **Zeitabhängiger Strukturanteil $c_{\mathrm{struct}}(t)\not\Rightarrow$ konstanter kalibrierter $c^0$.**
5. **Bilaterale N-1-Transfergrenze $\not\Rightarrow$ unabhängige simultane Ersatzlink-Kapazität.**
6. **IoSN-Ersatzkapazität $\not\Rightarrow$ operativer FBMC-RAM.**
7. **Ein niedriger Fluss-RMSE $\not\Rightarrow$ identifizierte Reaktanzen oder N-1-Sicherheit.**

# 15. Validierung, Ergebnisse und wissenschaftlicher Erkenntnisstatus

## 15.1 Physik- und Daten-Gates

- **V1:** Balancierte AC-Inseln je Snapshot; Topologie-, Einheiten- und Vorzeichenkonsistenz.
- **V2:** Exakte Identität $A_z\Gamma=P A_d$ für jede Busmap; Gleichheit der zonalen Bilanzen.
- **V3:** Konnektivität der Zonen, kritische Leitungen an Grenzen und überprüftes Flussrichtungsverhalten.
- **V4:** Technologiespezifische Referenzmatrizen mit $PR_k=I$; deklarierte Nullverfügbarkeitsregeln.
- **V5:** Train/Test-Trennung, RMSE/Quantile und Identifizierbarkeit positiver Reaktanzen.
- **V6:** Vollständige Offset-Wirkung in **Modellgleichungen**, nicht nur in Ergebnisdateien.
- **V7:** N-0-/N-1-Rekonstruktion gegen detailliertes Netz, Ausschluss/Behandlung von Inselkontingenzen, dokumentierte Outage-Liste.
- **V8:** K1/K2/K3-Grenzwerte, falsche Zulässigkeit und robuste Konservativität.
- **V9:** FBMC-GSK-Test nur in kompatiblen Gebotszonen und mit eindeutigem Referenzzustand.
- **V10:** Bewertung ausgewählter Ausbau-/Redispatchentscheidungen unter der originalen IoSN-Moduslogik.

## 15.2 Vorliegende Prototypergebnisse [S]

Der früher erstellte 9-Knoten-Demonstrator enthält zwei unterschiedliche Clustering-Busmaps und drei Referenzverteilungen. Der daraus übernommene, **nicht neu an echten Netzdaten qualifizierte** Vergleich nach Strukturkorrektur ergibt als RMSE (MW):

| Referenz | Busmap A | Busmap B |
|:--|--:|--:|
| Gleichmäßig | 1,951 | 0,638 |
| Kapazitätsgewichtet | 1,534 | 0,730 |
| Kosten-/Merit-Order-Proxy | 0,845 | 1,337 |

Die Werte demonstrieren eine Interaktion zwischen Busmap und Referenzverteilung; sie erlauben **keine** allgemeine Rangfolge, keinen Schluss auf reale TYNDP-Parameter und keinen Nachweis vollständiger IoSN-Konformität. Der ältere synthetische FBMC-Versuch zeigt analog, dass die Wahl eines GSK den berechneten Handelsbereich verändert; dessen Zahlen sind **keine** realen Core-RAMs. Eine reproduzierte Ausführung und die neu ergänzten mathematischen N-1-Kerntests werden in Band II getrennt dokumentiert.

# 16. Priorisierter wissenschaftlicher Fahrplan

**Stufe 1 — Normkonformes Referenzscreening.** Detailliertes AC-Teilnetz und exakte Wetter-/Marktzeitreihen fixieren; A als IoSN-nahe Baseline bauen. B als bewusst unabhängigen RES-/Last-Benchmark auf identischer Topologie erstellen; Ausgleichsannahmen sensitivieren. Busmaps $P_A,\Gamma_A$ und $P_B,\Gamma_B$ validieren.

**Stufe 2 — Reproduzierbares Ersatznetz.** Für jede Busmap drei räumliche Referenzen und technologiespezifische Strukturflüsse berechnen; reale Ersatzreaktanzen und $c^0$ unter identischen Train/Test-Protokollen kalibrieren; identifizierbare vermaschte Netze sicherstellen.

**Stufe 3 — Drei N-1-Wege.** IoSN-nahe K1-Schätzung; analytische K2-CNEC-Projektion als **bedingte** Sicherheitsreferenz; robuste K3-Derating-Approximation als konservative Kontrolle. Untereinander nur bei gleichen Temperatur-/Saisonlimits, Outage-Sets und Einspeisungsannahmen vergleichen.

**Stufe 4 — FBMC-Sensitivität und End-to-End-Bewertung.** Auf offiziellen Gebotszonen separat GSK-/CNEC-Sensitivitäten prüfen und die Zonennetzqualität anhand von Dispatch, Grenzverletzungen und repräsentativen Netzausbauentscheidungen beurteilen. PyPSA-Integrationsprüfung ist ein gesondertes Software-Gate.

Die zentrale wissenschaftliche Hypothese lautet: **Technologieabhängige räumliche Disaggregationsoperatoren verringern den auf einen konstanten $F_0$ projizierten Strukturfehler, während eine explizite PTDF-/LODF-Sicherheitsprojektion die versteckte N-1-Fehlabbildung durch einzelne Ersatzlink-Kapazitäten sichtbar macht.** Diese Hypothese ist testbar, aber derzeit noch nicht an realen TYNDP-Netzen bestätigt.

# Anhang A: Normative Rückverfolgbarkeit zur IoSN 2026

| IoSN-Abschnitt | Dokumentierter Inhalt | Unsere mathematische Zuordnung | Status |
|:--|:--|:--|:--|
| §3.8.1, S. 23–25 | Kritische Linien, Flusskorrelation, Zonenbudget, Konnektivität | C1, A-/B-Busmaps | A nah; B alternativ |
| §3.8.2, S. 27 | Impedanzen und Flusskorrekturen aus Optimierung | E1/E2 | Rekonstruktion |
| §3.8.3, S. 28 | No-Load, Loop-Flows, HVDC/PST, vier N-1-Grenzen | E1, T2, K1 | Direkte Zielgrößen |
| §3.8.4, S. 28–29 | Zonale Last-, RES-, konventionelle Asset-Verteilung | T1 und Eingangsvertrag | Konkrete Formalisierung |
| §3.9, S. 29–30 | LF-/OPF-Modi und interne Grenzen | Modus-Validierung | Kontextgebundene Umsetzung |
| Anhang 6.1, S. 45–48 | Jahresüberlastung; iterativer RMSE | C1, V3/V5 | Dokumentierter Bewertungsfokus |
| Anhang 6.1, S. 48–49 | PTDF-Sample, Impedanzen, Nullbilanzfluss, neutrale HVDC/PST | G2, T2, E2 | Teilweise rekonstruierbar |
| Anhang 6.1, S. 50–51 | LODF, vier Kapazitäten und Sonderfallbehandlung | N1, K1 | Prinzip dokumentiert |
| Kein IoSN-Abschnitt | B, Merit Order, Woodbury, K2, K3, FBMC | C2/C3, W1/W2, N3–N5, F1/F2 | Eigene Forschung/Technik |

# Anhang B: Quellen und Evidenzstatus

**[E1] ENTSO-E (2026).** *TYNDP 2026 Identification of System Needs Methodology: Version for Public Consultation*, 25 February 2026, §§3.7–3.9, Annex 6.1. Einzige methodische Normquelle für den IoSN-Abgleich. URL: <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf>.

**[N1] Ronellenfitsch, H.; Manik, D.; Hörsch, J.; Brown, T.; Witthaut, D.** *Dual Theory of Transmission Line Outages*. arXiv:1606.07276, wissenschaftliche Theorie zu Kreisflüssen, LODF und niedrig-rangigen Netzupdates. <https://arxiv.org/abs/1606.07276>.

**[N2] Gazafroudi, A. S.; Neumann, F.; Brown, T.** *Topology-based Approximations for N-1 Contingency Constraints in Power Transmission Networks*. International Journal of Electrical Power & Energy Systems, DOI:10.1016/j.ijepes.2021.107702; arXiv:2211.00970. Vergleich robuster, approximativer und leitungsspezifischer Kapazitätsfaktoren. <https://arxiv.org/abs/2211.00970>.

**[P1] PyPSA Developers.** *Network Clustering*, offizielle Dokumentation, Busmap, Clustering-Objekt und Aggregation. <https://docs.pypsa.org/stable/user-guide/clustering/>.

**[P2] PyPSA Developers.** *SubNetwork API*, `calculate_PTDF()` und `calculate_BODF()`. <https://docs.pypsa.org/latest/api/networks/subnetwork/>.

**[P3] PyPSA Developers.** *Flow-Based Market Coupling: Example*, Domänenrestriktionen und Linopy-Marktformulierung. <https://docs.pypsa.org/stable/examples/fbmc-simple-example/>.

**[S0] Frühere Projektartefakte (16.10.2026).** Vorheriger synthetischer Methodenvergleich und FBMC-Prototyp, einschließlich CSV-Dateien und Python-Testpaket aus diesem Gespräch. Interne Demonstrationsdaten, **keine** ENTSO-E-Netzevidenz.
