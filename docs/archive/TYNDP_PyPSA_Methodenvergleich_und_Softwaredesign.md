---
title: "Vergleich und Softwaredesign TYNDP-naher Netzreduktionsmethoden mit PyPSA"
subtitle: "Clustering A/B, technologiespezifische PTDFs, Merit-Order-Referenzen, elektrische Äquivalenz und N-1"
author: "Wissenschaftlicher Architektur- und Prototypbericht"
date: "16. Oktober 2026"
lang: de-DE
fontsize: 10pt
geometry: "margin=23mm"
colorlinks: true
urlcolor: blue
linkcolor: blue
numbersections: true
toc: true
toc-depth: 2
---

# Executive Summary

Der Bericht konsolidiert die in diesem Gespräch entwickelten Ansätze zur räumlichen Netzreduktion im Rahmen von **PyPSA / ENTSO-E TYNDP 2026**. Sein Ergebnis ist **kein Beleg einer vollumfänglichen ENTSO-E-Implementierung**, sondern eine explizite, mathematisch überprüfbare Architektur mit einem ausführbaren synthetischen Kernprototypen, einem gekapselten PyPSA-Adapter und klar definierten Validierungsgrenzen.

Die empfohlenen Hauptstufen sind:

1. **Zwei getrennte Clusterbildungen** auf derselben detaillierten physischen Topologie: A mit stündlichen Flüssen aus vollständigem Marktdispatch und Überlastungsenergie; B mit erneuerbarer Verfügbarkeit und Last, transparenter Bilanzierung und allgemeiner Leitungsbeanspruchung.
2. **Einheitliche elektrische Identifikation** je Busmap: Aggregationsoperatoren $P_m,\Gamma_m$, Referenzverteilung $R$, effektive technologiespezifische PTDFs, positive Ersatzreaktanzen, strukturelle Flusskorrektur $F_0$, N-1-bezogene saisonale, gerichtete Kapazitäten und unabhängige Validierung.

Über beide Stufen laufen drei **Referenzvarianten**: Gleichverteilung, Verteilung nach installierter konventioneller Leistung sowie eine aus festen Grenzkosten und Kapazitäten generierte **Merit-Order-Verteilung**. Repräsentativknoten werden optional durch Annäherung an die zugehörige gewichtete PTDF-Spalte ausgewählt, nicht allein anhand der installierten Leistung.

Im neuen synthetischen 9-Bus-Test (120 Stunden, fünf Zonen) ist die korrigierte Merit-Order-Referenz bei Clustering A am genauesten (RMSE **0,845 MW**), bei Clustering B dagegen schlechter als Gleichverteilung (RMSE **1,337 MW** gegenüber **0,638 MW**). Die Studie belegt damit die **Problemabhängigkeit** der Wahl von $R$, nicht eine generelle Hierarchie. Die Werte stammen ausschließlich aus frei generierten Modellzahlen und **nicht** aus TYNDP-/ENTSO-E-/PyPSA-Eur-Netzen.

**Begriffsvorbehalt:** Die im Auftrag genannte *„MCOE-Formulierung“* ist weder in den vorliegenden Gesprächsunterlagen noch in den bisherigen Berichtsentwürfen als eigenständige mathematische Normform definiert. Für die folgende Distanzbewertung wird daher transparent die **marginalkostenbasierte, kapazitätsbeschränkte Merit-Order-Referenz** als *Arbeitsinterpretation MCOE* verwendet. MCOE wird hier **nicht** als etablierte oder durch ENTSO-E vorgeschriebene Abkürzung behauptet. Falls eine andere exakte MCOE-Gleichung gemeint war, muss die Distanzbewertung dagegen ersetzt werden.

# 1. Dokumenten- und Geltungsbereich

## 1.1 Methodische Autorität

Normative Ausgangsbasis für die ENTSO-E-Beurteilung ist allein die Konsultationsfassung **„TYNDP 2026 – Identification of System Needs Methodology“**, vom 25. Februar 2026, Kapitel 3.8 und Anhang 6.1. Die relevante Methode beschreibt kritische Leitungen, räumliche Zonengrenzen, PTDF-gestützte stündliche physikalische Flüsse, Ersatzimpedanzen, strukturelle Nullbilanzflüsse sowie richtungs- und saisonabhängige, N-1-bezogene Ersatzkapazitäten. Die ENTSO-E veröffentlicht dabei **nicht** sämtliche Regressions- oder Optimierungsdetails. [E1]

Andere Quellen werden nur für vorhandene **Softwarefunktionen** ([P1]–[P3]) oder als **frühere interne Gesprächsartefakte** ([I1]–[I3]) herangezogen. Der neue quantitative Beispielversuch ist [S1].

## 1.2 Statuskennzeichnung

- **[D] Dokumentiert:** vom ENTSO-E-Text ausdrücklich gedeckt.
- **[R] Rekonstruktion:** mathematisch konsistente Interpretation, nicht als Originalalgorithmus ausgewiesen.
- **[E] Entwurf:** konkrete Software- oder Forschungsentscheidung.
- **[S] Synthetischer Befund:** aus künstlichen Eingangsdaten berechnet.
- **[O] Offen:** zusätzliche Daten, Methodenspezifikation oder Realnetzqualifikation erforderlich.

Nicht betrachtet: vollständige AC-Spannungsäquivalenz, Schutz-/Kurzschlussäquivalente, harmonische Modelle, dynamische Äquivalenz sowie der gesamte TYNDP-Markt- und Investitionsplanungsprozess.

# 2. Gemeinsame mathematische Grundlagen

Sei $G_d=(\mathcal N,\mathcal L)$ der detaillierte passive AC-Graph in verlustloser DC-Näherung mit $N$ Knoten, $L$ Zweigen, orientierter Knoten-Zweig-Inzidenz $A_d\in\mathbb R^{N\times L}$ und positiver Reaktanz $x_\ell>0$. Es sei $B_d=\operatorname{diag}(1/x_\ell)$.

$$
A_d B_d A_d^{\mathsf T}\theta_t=p_{d,t},\qquad
f_{d,t}=B_d A_d^{\mathsf T}\theta_t,\qquad A_df_{d,t}=p_{d,t}.
\tag{1}
$$

Für die nodale PTDF $H_d$ (gewählte Slack-Referenz) gilt bei **explizit ausgeglichenem** $p_{d,t}$:

$$
\mathbf 1^{\mathsf T}p_{d,t}=0,\qquad f_{d,t}=H_dp_{d,t}.
\tag{2}
$$

Ein von null verschiedener physikalischer Phasenschieber-/PST-Offset müsste als zusätzlicher Term geführt werden. Mehrere AC-Inseln benötigen eigene Bilanzen und Block-PTDFs. HVDC ist als zweipolige nodale Ein-/Ausspeisung abzubilden; Leistung am AC-Terminal, Verluste und Link-Vorzeichen müssen konsistent sein.

## 2.1 Exakte Matrixaggregation

Die Busmap $z_m:\mathcal N\to\{1,\ldots,Z\}$ erzeugt für Clustering $m\in\{A,B\}$ die boolesche Matrix $P_m\in\{0,1\}^{Z\times N}$ sowie den orientierten physikalischen Schnittoperator $\Gamma_m\in\{-1,0,1\}^{E_m\times L}$. $A_{z,m}$ ist die Inzidenz des reduzierten Schnittgraphen. Dann:

$$
p_{z,t}^{(m)}=P_mp_{d,t},\qquad
f_{z,t}^{(m)}=\Gamma_mf_{d,t},\qquad
\boxed{A_{z,m}\Gamma_m=P_mA_d}.
\tag{3}
$$

Folglich gilt exakt (im selben lossless-DC-Modell):

$$
\boxed{A_{z,m}f_{z,t}^{(m)}=p_{z,t}^{(m)}}.
\tag{4}
$$

**Wichtig:** Diese Bilanzidentität ist keine Aussage, dass die äquivalenten Zweigimpedanzen bereits richtig sind. Sie sagt ausschließlich, dass ursprüngliche Grenzflüsse und die zugehörigen eingespeisten Zonenbilanzen konsistent aggregiert wurden. $P_m$ und $\Gamma_m$ sind **busmap-spezifisch**; ihre Werte sind im Allgemeinen für A und B verschieden.

## 2.2 Basisfluss, Nullbilanzfluss und zwei verschiedene F0-Begriffe

Ein Referenzfluss $f_{\mathrm{ref}}=H_dp_{\mathrm{ref}}$ ist nicht dasselbe wie ein **struktureller zonaler Nullbilanzfluss**. Letzterer wird aus Einspeisungsunterschieden innerhalb der Zonen erzeugt, deren zonale Summe null ist. Für eine Disaggregation $R\in\mathbb R^{N\times Z}$, $P_mR=I_Z$, gilt:

$$
p_{d,t}=RP_mp_{d,t}+u_t,\qquad P_mu_t=0.
\tag{5}
$$

Somit:

$$
f_{z,t}^{(m)}=\underbrace{\Gamma_mH_dR\,p_{z,t}^{(m)}}_{\text{referenzbasierter Zoneneinfluss}}
+\underbrace{\Gamma_mH_du_t}_{f_{{\mathrm{struct}},t}}
\tag{6}
$$

und $A_{z,m}f_{{\mathrm{struct}},t}=0$. Der Strukturfluss ist typischerweise **zeitabhängig** und **referenzabhängig**. Ein kalibrierter konstanter $c^0$ ist dagegen ein Modellparameter, der diese stündlich schwankenden Wirkungen nur innerhalb seiner Gültigkeitsbedingungen approximiert. Die Rechnung setzt hier neutrale PST-Offsets voraus.

# 3. Methode A: Dispatch-basierte Überlastungsenergie

**Ziel [D/R]:** Die Überlastungen aus physikalischen Flüssen eines vollständig bilanzierten Marktergebnisses markieren die kritischen Übertragungsleitungen, die als Zonengrenze bevorzugt erhalten bleiben sollen.

$$
p_{d,t}^{A}=p_{\mathrm{RES,dispatch,t}}+p_{\mathrm{conv,t}}+p_{\mathrm{storage,t}}-p_{\mathrm{load,t}}+p_{\mathrm{HVDC,t}}.
\tag{7}
$$

Im verlustlosen Netz ist $\mathbf1^\mathsf Tp_{d,t}^A=0$. Die stündlichen physikalischen Flüsse sind $f_{d,t}^A=H_dp_{d,t}^A$. Der Leitungsindikator wird als aufgelaufene Überlastungsenergie definiert:

$$
\boxed{S^A_\ell=\sum_t\Delta t_t\max(0,|f^A_{\ell,t}|-\overline F_{\ell,t})}.
\tag{8}
$$

Ein Entwurf für die Clusterbildung minimiert dann über zulässige verbundene Partitionen bei vorgegebenem Zonenbudget die „verlorene Wichtigkeit“:

$$
\min_{z_A\in\mathcal Z_{\mathrm{valid}}}\sum_{\ell=(i,j)}S^A_\ell\,\mathbb{1}\{z_A(i)=z_A(j)\}.
\tag{9}
$$

Das Optimierungsproblem (9) ist ein **eigener Entwurf**. Das vorhandene Programm implementiert nur ein **greedy connected contraction screening**, kein garantiertes globales Minimum.

**Stärken:** nahe an der in [E1] beschriebenen Engpassidee; tatsächliche flexible Einspeisungen, Importe und Lasten werden erfasst; direkt auf langfristige Ausbauengpässe interpretierbar. **Schwächen:** vom Marktszenario, bereits vollzogenen Redispatch und Speichereinsatz abhängig; unter ausschließlich N-1-optimalem Dispatch können bestimmte präventiv beseitigte Engpässe verdeckt sein; wenige Extremstunden können Rangfolgen bestimmen. Unterschiedliche Marktannahmen müssen daher als Szenarien getrennt geprüft werden.

# 4. Methode B: RES-Last-getriebenes allgemeines Belastungsclustering

**Ziel [E]:** Die räumlich und zeitlich exogenen Profile von erneuerbarer Verfügbarkeit und unflexibler Nachfrage sollen dominante strukturelle Transportkorridore bestimmen, ohne einen optimierten konventionellen Dispatch zur Clusterbildung vorzugeben.

$$
q_t=p^{\mathrm{RES,avail}}_{d,t}-p^{\mathrm{load}}_{d,t}.
\tag{10}
$$

Im Allgemeinen ist $\mathbf1^\mathsf Tq_t\ne0$. Daher ist die unkommentierte Multiplikation $H_dq_t$ **keine eindeutige physikalische Flussrekonstruktion**. Eine explizite Ausgleichskonvention ist erforderlich, z. B.:

$$
\widetilde q_t=q_t-w\,\mathbf1^{\mathsf T}q_t,\qquad w_i\ge0,\quad\mathbf1^{\mathsf T}w=1.
\tag{11}
$$

Die entstandenen $f^B_{d,t}=H_d\widetilde q_t$ sind **Screening-Flüsse** unter der angenommenen Verteilung $w$, nicht implizit ein vollständiges Marktergebnis. Alternativ lässt sich nur der intrazonale, per Konstruktion balancierte Strukturanteil auswerten; auch dann benötigt man $R$ und eine feste Busmap.

Die Gesamtbeanspruchung einer Leitung kann als transportierte Wirkleistungsenergie und relative Belastung beschrieben werden:

$$
E_{\ell}^{\mathrm{flow}}=\sum_t\Delta t_t|f_{\ell,t}^B|,\qquad
S^B_\ell=\frac{\sum_t\omega_t|f_{\ell,t}^B|/\overline F_{\ell,t}}{\sum_t\omega_t}.
\tag{12}
$$

Optional: P95 der stündlichen relativen Auslastung, zeitliche Korrelationsgruppen, Mindestkonnektivität und Schutz wichtiger Leitungen. $S_\ell^B$ wird **auch unterhalb der thermischen Grenze** berücksichtigt.

**Stärken:** sehr gut zur strukturellen Langfristorientierung, RES-Integration und stabilen räumlichen Leistungsbilanz-Mustern; geringere Abhängigkeit von ökonomisch optimierter Steuerung. **Schwächen:** Ausgleichsschlüssel kann Leitungsrangfolgen deutlich beeinflussen; ignoriert Import-, Kernkraft-, Gas-, Speicher- und konventionelle Transitsituationen; ist bewusst keine ENTSO-E-Überlastungsreplik. Sensitivität gegenüber $w$ muss quantitativ gemessen werden.

# 5. Technologiespezifische PTDFs als gemeinsamer mathematischer Unterbau

Seien $k\in\mathcal K$ die Komponenten Wind, Photovoltaik, Wasser, Last, konventionelle Erzeugung und Speicher; ihre zonalen Einspeisungen sind *vorzeichenbehaftet* $p_{z,t}^{(k)}$. Für die räumliche Disaggregation pro Technologie $R_k(t)$ gelten:

$$
P_mR_k(t)=I_Z,\qquad H_z^{(k,m)}(t)=\Gamma_mH_dR_k(t).
\tag{13}
$$

**Wesentliche physikalische Erkenntnis:** Die Technologie verändert nicht die physikalische Matrix $H_d$; die Unterschiede entstehen vollständig durch $R_k(t)$. Beispielsweise ist die Wind-PTDF anders als die Kernkraft-PTDF, weil diese innerhalb derselben Zone andere Anschlussknoten gewichten.

Mit gemeinsamer Referenz $R_0$ ist der technologiespezifische strukturelle Flussbeitrag:

$$
\boxed{f_{{\mathrm{struct}},t}^{(k)}=\Gamma_mH_d\big(R_k(t)-R_0\big)p_{z,t}^{(k)}}.
\tag{14}
$$

Er besitzt null Zonendivergenz, da $P_m(R_k-R_0)=0$. Die Aggregation der Beiträge von RES und Last benötigt **keinen neuen AC- oder DC-Netzsolver** und kann im Python-Code als Sparse-Matrixprodukt ausgeführt werden. Für bei null verfügbarer RES auftretende undefinierte Quotienten ist ein expliziter Ersatzschlüssel zu definieren, ohne Leistung zu erzeugen.

Eine bedeutende Grenze ist, dass $H_z^{(k,m)}$ **keine automatisch durch passive Ersatzreaktanzen realisierbare PTDF** ist. Außerdem sind $f_{\mathrm{struct}}$ und der Fit-Residualfehler $f_z-H_{\mathrm{eq}}p_z$ nicht identisch.

# 6. Die drei nicht erneuerbaren Referenzverteilungen

## 6.1 Gleichverteilung $R_{\mathrm{uni}}$

Jeder ursprüngliche Knoten einer Zone erhält den gleichen Anteil $1/n_z$. Das Verfahren ist robust, datensparsam und als neutrale Baseline nützlich; physikalisch große Einspeisungen und Anlagenschwerpunkte werden jedoch ignoriert.

## 6.2 Kapazitätsverteilung $R_{\mathrm{cap}}$

Für nicht erneuerbare Referenzkapazität $C_i$ innerhalb der Zone $z$:

$$
[R_{\mathrm{cap}}]_{iz}=\frac{C_i}{\sum_{j\in\mathcal N_z}C_j}.
\tag{15}
$$

Bei null Kapazität ist eine dokumentierte Alternativverteilung notwendig. Vorteil: Anschluss- und Größenstruktur werden erhalten; Nachteil: verfügbare Leistung, marginale Kosten und tatsächlicher Einsatz fehlen.

## 6.3 Feste marginalkostenbasierte Merit-Order-Verteilung $R_{\mathrm{MO}}$

Es seien die installierten Leistungen $C_g$ und **zeitlich unveränderliche Grenzkosten** $c_g$ der nicht erneuerbaren Generatoren bekannt. Für fest definierte Referenz-Residuallastniveaus $D_s$ und Gewichte $\pi_s$, $\sum_s\pi_s=1$, ergibt sich ein einfacher, **zonaler** Restmarkt:

$$
\min_{0\le p_{g,s}\le C_g}\sum_g c_gp_{g,s}
\quad\mathrm{s.t.}\quad\sum_{g\in\mathcal G_z}p_{g,s}=D_{z,s}.
\tag{16}
$$

Die gewichtete Einsatzneigung ist

$$
\bar p_g=\sum_s\pi_s p_{g,s}^{*},\qquad
[R_{\mathrm{MO}}]_{iz}=\frac{\sum_{g\to i}\bar p_g}{\sum_{j\in\mathcal N_z}\sum_{g\to j}\bar p_g}.
\tag{17}
$$

Im Prototyp werden $D_{z,s}$ als 35 %, 60 % und 85 % der zonalen konventionellen Kapazität mit Gewichten 0,30, 0,45 und 0,25 verwendet. Das ist **ein demonstrativer Parameterentscheid**, keine ENTSO-E-Anforderung und keine kalibrierte Prognose. Der vereinfachte zonale Markt berücksichtigt weder Netzrestriktionen noch Anfahrkosten, Rampen, Mindestlast, Reservehaltung, CO$_2$-Unsicherheit oder länderübergreifenden Austausch.

**Die Grenzkosten beeinflussen die effektive PTDF ausschließlich über die Disaggregation $R_{\mathrm{MO}}$.** Die elektrische PTDF $H_d$ und physikalische Impedanzen sind weiterhin unabhängig von den Kosten.

## 6.4 Arbeitsinterpretation „MCOE“ und methodische Distanz

Eine MCOE-Normgleichung ist nicht belegt. Als **Arbeitsproxy** gilt (16)–(17), also kostenminimaler Restdispatch an ausgewählten Residuallaststützstellen. Die folgenden „Abstände“ sind **konzeptionell** und keine metrisch normierten Zahlenwerte.

| Ansatz | Nähe zum Kostenproxy (16)–(17) | Begründung |
|:--|:--|:--|
| $R_{\mathrm{MO}}$ | Direkt | Enthält Kapazitäten, Grenzkosten, Merit Order, Stützstellen |
| $R_{\mathrm{cap}}$ | Mittel | Enthält Kapazitäten, aber keine Kosten oder Aktivierungsordnung |
| $R_{\mathrm{uni}}$ | Gering | Keine Anlagen- oder Kostendaten |
| Methode A: voller Markt | Betriebswirtschaftlich realitätsnäher möglich; andere Ebene | Tatsächlicher Dispatch kann weitere Restriktionen berücksichtigen, ist keine feste Referenz |
| Methode B: RES/Last | Bewusst weit entfernt | Exogene Struktur statt konventioneller Kostenoptimierung |
| Technologie-PTDF | Orthogonal | Rein räumlicher Operator, mit jedem $R$ kombinierbar |
| Ersatzimpedanz-Fit | Orthogonal | Projektion von Flusssensitivitäten auf ein passives Netz, unabhängig vom Kostenmodell |

Daraus folgt **nicht**, dass die dem Kostenproxy nächste Variante die beste elektrische Ersatznetzgenauigkeit haben muss. Ökonomische Plausibilität und Flussrekonstruktionsgüte sind unterschiedliche Zielkriterien.

# 7. Auswahl eines realen Ersatzknotens pro Zone

Zusätzlich zu einer verteilten Referenz $R$ kann je Zone ein repräsentativer Originalknoten $i_z\in\mathcal N_z$ bestimmt werden. Auf dem detaillierten Netz vergleicht man die aggregierten Sensitivitätsspalten gegen die gewichtete Referenzspalte:

$$
i_z^{*}=\arg\min_{i\in\mathcal N_z}
\left\|W\big(\Gamma_mH_de_i-\Gamma_mH_dR_{:,z}\big)\right\|_2^2.
\tag{18}
$$

Dies ist eine transparente **lokale heuristische Knotenwahl**. Eine slackunabhängige **globale** Bewertung muss ausgeglichene Einspeisungskombinationen der ausgewählten Kandidaten verwenden. Die Existenz eines repräsentativen Knotens impliziert keine exakte physikalische Reduktion des restlichen Graphen. Der Prototyp berechnet Kandidaten, führt aber noch **keine automatische graphphysikalische Kron-Reduktion** durch.

# 8. Ersatzimpedanzen: Realisierbarkeit, Skalierung, Zielfunktionen

Für die vorgegebene reduzierte Inzidenz $A_z\in\mathbb R^{Z\times E}$ und positive Ersatzreaktanzen $x_e$ ist

$$
H_{\mathrm{eq}}(x)=\operatorname{diag}(1/x)A_z^{\mathsf T}
\Big(A_z\operatorname{diag}(1/x)A_z^{\mathsf T}\Big)^{+},
\tag{19}
$$

wobei die Pseudoinverse nur auf dem balancierten Unterraum wirkt und in der Software durch die Eliminierung eines Slackwinkels berechnet wird.

Es bestehen **zwei getrennte Kalibrierungsziele**:

**Operatorprojektion der technologiespezifischen Referenz:**

$$
\min_{x>0}\left\|\Big(H_{\mathrm{eq}}(x)-\Gamma_mH_dR_{\mathrm{ref}}\Big)T\right\|_F^2
+\lambda\mathcal R(x),\quad \mathbf1^{\mathsf T}T=0.
\tag{20}
$$

**Snapshotbasierte elektrische Kalibrierung mit konstantem Offset:**

$$
\min_{x>0,\,A_zc^0=0}\sum_{t\in\mathcal T_{\mathrm{train}}}w_t
\left\|W\big(H_{\mathrm{eq}}(x)p_{z,t}+c^0+f_{{\mathrm{struct}},t}^{\mathrm{known}}-f_{z,t}^{\mathrm{target}}\big)\right\|_2^2.
\tag{21}
$$

Für (20) wird im Paket die erste Reaktanz skalenfixiert. Für (21) wird der Offset über eine Nullraum-Basis von $A_z$ parametrisiert. Die Zusatzgröße $f_{{\mathrm{struct}},t}^{\mathrm{known}}$ darf nur verwendet werden, wenn dieselbe räumliche Auflösung **auch im späteren Betrieb** tatsächlich verfügbar ist.

**Nicht-Eindeutigkeit:** Wenn alle Reaktanzen desselben zusammenhängenden Netzes mit demselben positiven Faktor skaliert werden, bleibt die verlustlose DC-Flussverteilung unter gegebenen Einspeisungen identisch. Für einen **Baumgraphen** sind die Grenzflüsse durch die zonale Bilanz bereits eindeutig bestimmt; Reaktanzen sind dann aus reinen Wirkleistungsflüssen nicht identifizierbar. Deshalb meldet die Software den Zyklus-Rang $E-Z+1$ als wesentlichen Identifizierbarkeitsindikator. Auch bei positivem Rang können spezifische Parameter unbeobachtbar bleiben.

**Realisierbarkeit:** Die Matrix $\Gamma_mH_dR$ muss nicht im Raum der durch positive $x$ und feste reduzierte Topologie realisierbaren PTDFs liegen. (20) ist darum ein Projektionsproblem, keine algebraisch garantierte Gleichheit.

# 9. No-Load-Flows und spätere zonale Betriebssemantik

Aus bekannten hochaufgelösten Profilen ergibt sich bei Referenz $R$ für jedes $t$:

$$
\boxed{f_{{\mathrm{struct}},t}=\Gamma_mH_d(I-RP_m)p_{d,t}}.
\tag{22}
$$

Diese Größe ist im DC-Modell und bei vollständigen nodalen Daten exakt und hat null Zonendivergenz. Für den nur RES-Last-basierten Anteil benutzt man $q_t$ statt $p_{d,t}$; dieser **intern bilanzierte Differenzvektor** benötigt keine separate globale Restmarktlösung, liefert jedoch nicht die vollständigen Betriebsflüsse.

Der bestimmbare residuale Offset zum konkreten Ersatznetz ist

$$
r_{0,t}=f_{z,t}^{\mathrm{target}}-H_{\mathrm{eq}}(x)p_{z,t}.
\tag{23}
$$

Er besteht im Allgemeinen aus einem strukturbedingten Anteil und dem eigentlichen **Ersatzimpedanz-Abbildungsfehler**. Einen unveränderlichen $c^0$ zu verwenden heißt also, eine zusätzliche stationaritätsähnliche Näherung zu treffen. In dem neuen Paket wird $c^0$ ausdrücklich als kalibrierter, zeitunabhängiger Nullraumvektor interpretiert.

Ein gewöhnlicher PyPSA-`Line`-Lastfluss erzeugt die zusätzliche freie Nullbilanz-Zirkulation nicht allein durch Setzen von `x`. **Für den produktiven Einsatz muss die affine Flussgleichung tatsächlich in die Optimierungsrestriktionen integriert werden**, beispielsweise als verifizierte zusätzliche Linopy-Formulierung; das Paket liefert dafür die Parameter und Rechenkerne, noch keinen produktiv qualifizierten Override des PyPSA-Optimierungsmodells.

# 10. N-1 und saisonale gerichtete Kapazitäten

Für die detaillierten ungestörten Flüsse $f_t$ und einen nicht inselbildenden Ausfall $k$ gilt:

$$
f_{\ell,t}^{(k)}=f_{\ell,t}+\operatorname{BODF}_{\ell k}f_{k,t}.
\tag{24}
$$

Der Prototyp berechnet die BODF aus der nodalen PTDF und Zweiginzidenz, erkennt Nenner nahe null (häufig Inselbildungsfälle) und meldet diese **nicht abgedeckten Kontingenzen**. Die Belastung einer ursprünglichen Leitung berücksichtigt N-0 und die gültigen N-1-Ausfälle:

$$
\rho_{\ell,t}=\max\left\{\frac{|f_{\ell,t}|}{\overline F_\ell},
\max_{k\in\mathcal C}\frac{|f_{\ell,t}^{(k)}|}{\overline F_\ell}\right\}.
\tag{25}
$$

Je Interzonenschnitt $e$ werden stündlicher aggregierter Austausch $F_{e,t}$ und die stärkste dort überwachte N-1-Leitungsauslastung gepaart. Daraus werden getrennt für **Sommer/Winter** und **beide Flussrichtungen** vier empirische Grenzeinstellungen bei $\rho=1$ geschätzt.

**Sicherheitsgrenze:** Die im Code angebotene lineare Punktwolken-Regression mit Intercept ist nur ein **gekennzeichneter Vorentwurf**. Schwache Korrelation, fehlende Daten, unzureichende Belastungsbereiche oder inselbildende Ausfälle führen zu Qualitätsflags beziehungsweise `NaN`. Ein numerisch geschätzter MW-Wert ist **kein universell N-1-sicherer Transfergrenzwert**; dafür braucht es explizite CBCO-Listen, geeignete Zeitbereiche, Maßnahmenannahmen und unabhängige Security-Berechnungen. Auch MW-Grenzen aus AC-Scheinleistungslimits sind lediglich Näherungen.

# 11. Wissenschaftlicher Methodenvergleich

| Methodik | Hauptinformation | Stärken | Schwächen | Status im Paket |
|:--|:--|:--|:--|:--|
| Clustering A: Überlastungsenergie | Gesamter Dispatch, Ratings | ENTSO-E-nahe Sicht auf bestehende Engpässe | Markt-/Szenarioabhängigkeit, „fehlende“ flexible Fälle | Ausführbarer numerischer Kern, greedy Partition |
| Clustering B: gesamte Belastung | RES-Verfügbarkeit, Last, Bilanzausgleich | Strukturelle Transportmuster ohne Marktopti-mierung | Ausgleichsabhängigkeit, kein vollständiger Betrieb | Ausführbarer numerischer Kern, greedy Partition |
| Explizite $P_m,\Gamma_m$ | Busmap, Originaltopologie | Exakte Bilanz, Sparse-Matrizen, Audits | Keine Ersatzimpedanzen | Ausführbar und getestet |
| Technologiespezifische PTDF | $H_d$, $R_k(t)$ | Erklärt Strukturfluss, speichert räumliche Informationen | Referenzabhängig, $R_k$ nicht immer definiert | Ausführbar und getestet |
| Gleichgewichtung | Alle Knoten | Einfach, stabil, keine Kraftwerksdaten | Ignoriert reale Erzeugungsstruktur | Ausführbar |
| Kapazitätsgewichtung | Nameplate-MW | Räumliche Kraftwerksstruktur | Ignoriert Grenzkosten | Ausführbar |
| Merit-Order-Referenz | Kapazitäten, feste Grenzkosten, Laststützstellen | Ökonomisch interpretierbar | Kein echter Markt; potenzieller Bias | Ausführbar |
| PTDF-Ersatzknoten | Sensitivitätsspalten | Erhält existierenden Knoten als Kandidat | Nur lokale, nicht globale Repräsentation | Heuristik ausführbar |
| Operator-Fit $H_{\mathrm{eq}}$ | Referenz-PTDF | Realisierbare positive Reaktanzen | Nicht-Eindeutigkeit; kann nicht exakt passen | Ausführbar und getestet |
| Snapshot-Fit $x,c^0$ | Vollständige Kalibrierungsflüsse | Betriebszustandsgetriebene Fehlerreduktion | Overfitting/Referenzzeitraum; Integration erforderlich | Ausführbar und getestet |
| N-1-Grenzen | Originalnetz-Ausfälle | Physikalischer Sicherheitsbezug | Datenabhängige Proxy-Schätzung | Diagnoseprototyp, nicht freigabefähig |

# 12. Implementierungsdesign und PyPSA-Wiederverwendung

## 12.1 Kernarchitektur

```text
PyPSA detailliertes Network  -> pypsa_adapter.py (Preflight, x_pu, IDs)
       |                                |
       +-- vollständige p_d^A ----------+--> screening.py: A, Überlastungsenergie
       |                                |
       +-- RES/Last + Bilanzierung -----+--> screening.py: B, allgemeine Belastung
                                          |
                                 clustering.py: zwei Busmaps
                                          |
                         aggregation.py: P_A/Gamma_A, P_B/Gamma_B
                                          |
                   PyPSA get_clustering_from_busmap (optional initial topology)
                                          |
            distribution.py: uniform/capacity/merit-order/tech-R/rep-node
                                          |
          equivalent.py + offsets.py: Href, xeq, c0 und Strukturkorrekturen
                                          |
                  security.py: BODF, N-1 und Diagnosekapazitäten
                                          |
             outputs/: CSV/JSON + wissenschaftliche Tests und Gate-Status
```

`pypsa.Network.cluster.spatial.busmap_by_hac()` und `get_clustering_from_busmap()` gehören zu den vorhandenen PyPSA-Schnittstellen. `n.lpf()` und `SubNetwork.calculate_PTDF()` beziehungsweise `calculate_BODF()` stehen ebenfalls zur Verfügung. Die **globale** Beurteilung von Engpassschutz oder Kostengewichtung wird dadurch jedoch nicht automatisch gelöst. [P1–P3]

## 12.2 Modulvertrag

| Datei | Verantwortung | Verwendungsstatus |
|:--|:--|:--|
| `dc.py` | Explizite lossless-DC-PTDF, Balanzprüfung | Numerisch getestet |
| `screening.py` | Methode A und B, Leitungsscores | Numerisch getestet |
| `clustering.py` | Verbundene Greedy-Kontraktionen mit Score | Numerisch getestet, keine globale Optimalität |
| `aggregation.py` | $P,\Gamma,A_z$, Identität $A_z\Gamma=PA_d$ | Numerisch getestet |
| `distribution.py` | $R_0,R_{cap},R_{MO},R_k(t)$ und Ersatzknoten | Numerisch getestet |
| `offsets.py` | Exakte Strukturflüsse relativ zu $R$ | Numerisch getestet |
| `equivalent.py` | PTDF-Projektion und Fit positiver $x$, konstantem $c^0$ | Numerisch getestet |
| `security.py` | BODF und unsichere/markierte Grenzschätzungen | Numerisch getestet, keine Sicherheitsfreigabe |
| `pypsa_adapter.py` | PyPSA-Netze lesen, aggregieren, Export | **Nicht zur Laufzeit getestet** |
| `run_demo.py` | Gleichartige A/B-Tests und Referenzvergleich | Ausgeführt |

**Bewusste Schranke des Adapters:** In seiner ersten Version werden vorhandene Transformatoren, Mehrpol-Links, Stores, StorageUnits und nichtneutrale Phase-Shifts **nicht stillschweigend ignoriert**, sondern lösen einen Fehler aus. Das ist für ein reales europäisches Netz noch nicht ausreichend, schützt aber vor wissenschaftlich falschen Flüssen. Ein echter Transformator-/HVDC-/PST-Adapter ist ein blockierender Integrationsschritt.

## 12.3 Minimale Benutzung

```bash
python -m pip install -e '.[test]'
pytest -q
python run_demo.py --output outputs
```

Für die echte PyPSA-Anbindung:

```bash
python -m pip install -e '.[pypsa,test]'
python examples/pypsa_real_network.py /pfad/detailed_network.nc
```

`examples/pypsa_real_network.py` ist ein **Integrationsskelet** mit strikten Hard-Stops. Es liefert bei geeigneten Netzen eine nicht kalibrierte PyPSA-Basistopologie; die mathematischen Ersatznetzparameter werden **nicht** schon automatisch als fertiges Linopy-Netzmodell eingetragen.

# 13. Neue synthetische Gegenüberstellung [S1]

## 13.1 Versuchsprotokoll

Neun ursprüngliche Knoten, 15 passive AC-Leitungen, 120 stündliche Profile, fünf resultierende Zonen, random seed `20261016`; frei erfundene, feste Grenzkosten und installierte Kapazitäten. Derselbe vollständige, stündlich bilanzierte Betrieb wird für die **elektrische Validierung beider Busmaps** verwendet. Die Clusterbildung A nutzt Überlastungsenergie, B nutzt RES/Last-Screening mit kapazitätsgewichtetem Bilanzausgleich. Kalibrierungsperiode sind die ersten 80 Stunden, unabhängige Testperiode die letzten 40.

Die PTDF-Operatorprojektion wird **je Referenz** neu berechnet. Für den Vergleich „mit Strukturkorrektur“ sind die **hochaufgelösten** Wind-, PV- und Lastbeiträge auch in der Validierung bekannt; das ist eine bewusst **datenintensive Obergrenze**, keine Aussage über spätere Verfügbarkeit dieser nodalen Daten im Produktionsnetz.

## 13.2 Ergebnisse

| Clustering | Referenz | Test-RMSE ohne Struktur [MW] | Test-RMSE mit RES/Last-Struktur [MW] | Zyklusrang |
|:--|:--|--:|--:|--:|
| A | Gleichmäßig | 2,225 | 1,951 | 3 |
| A | Kapazitätsgewichtet | 3,149 | 1,534 | 3 |
| A | Merit-Order-gewichtet | 5,158 | **0,845** | 3 |
| B | Gleichmäßig | 1,100 | **0,638** | 2 |
| B | Kapazitätsgewichtet | 1,028 | 0,730 | 2 |
| B | Merit-Order-gewichtet | 1,670 | 1,337 | 2 |

Die gemeinsame snapshotbasierte Anpassung von $x,c^0$ erreichte in diesem Test unabhängig von der nachträglich daneben betrachteten Referenzverteilung einen Test-RMSE von **1,024 MW** für Busmap A und **0,551 MW** für Busmap B. Das liegt daran, dass dieses Fit-Ziel nur die vollständigen Zielzeitreihen, nicht $R_{\mathrm{ref}}$ verwendet. Die drei Wiederholungen dürfen daher nicht als drei unterschiedliche wirtschaftliche Fits missverstanden werden.

- **A** bewahrt im synthetischen Fall 100 % der positiven Überlastungsenergie als Originalleitungen auf Interzonenschnitten; das ist **kein** Nachweis, dass der aggregierte Ersatz dieselben Überlastungen prognostiziert.
- **B** bewahrt 92,4 % des definierten relativen Belastungsscores auf Schnittleitungen auf.
- **Die Clustering-Busmaps unterscheiden sich**, und auch die Fehlerstruktur unterscheidet sich. Ein Vergleich allein von zwei RMSE-Zahlen ist ohne gleiches Zonenbudget, Kalibrierungsfenster und Testset unzulässig.
- Die demonstrative N-1-Punktwolkenschätzung liefert vielfach **„insufficient_data“** oder **„weak_relationship“**. Diese Fälle bleiben ausdrücklich offen; die Software füllt sie nicht mit erdachten MW-Kapazitäten.

Die Zahlen sind *nicht* direkt mit dem früheren 6-Bus-/3-Zonen-Pilot [I3] vergleichbar; dort lag nach RES/Last-Korrektur die Kapazitätsreferenz vorn. Die geänderten Netztopologien und Einspeisungsannahmen unterstreichen, dass keine Variante universal dominant ist.

# 14. Reproduzierbarkeit, Validierungsgates und Grenzen

**Gate G0 – Eingang:** vollständige, versionierte Ausgangsnetze und synchronisierte Zeitreihen; eindeutig definierte technologiebasierte Erzeugungsklassen und Vorzeichen. Bei fehlenden Originaleingängen kein Anspruch auf echte Netzreduktion.

**Gate G1 – vollständige Balance:** nodale Einspeisungsbilanz je Insel (A); explizite Sensitivität gegenüber Ausgleichsschlüsseln (B). Bei verletzter Bilanz kein PTDF-Fluss.

**Gate G2 – Partition:** gleiche Zonenzahl, nur zusammenhängende Zonen, vollständige Komponentenabdeckung, getrennte Busmaps A/B, dokumentierte kritische Schnitte.

**Gate G3 – algebraische Identität:** $A_z\Gamma=PA_d$, $A_zf_z=p_z$, $PR_k=I$ und Nullbilanz des Strukturflusses.

**Gate G4 – elektrische Identifikation:** positive Ersatzreaktanzen; Hinweis auf Skalengauge und Zyklusrang; keine Behauptung exakter Realisierbarkeit von $\Gamma H_dR$; Test mit zurückgehaltenen Stunden.

**Gate G5 – Security:** N-0/N-1 auf Originalleitungen; inselbildende Ausfälle separat; CBCO-Regeln, Ratingdefinitionen, Sommer/Winter und beide Richtungen; keine Kapazität ohne identifizierbare Daten.

**Gate G6 – Produktionsintegration:** affine $F_0$-Semantik in Linopy/PyPSA restriktionswirksam, Transformatoren/HVDC/PST modelliert, unabhängige Prüfszenarien, Reproduzierbarkeit mit gepinnter PyPSA-Version.

Status zum Zeitpunkt dieses Berichts: **G1–G4 für den begrenzten synthetischen DC-Kern teilweise testgestützt; G0/G5/G6 für ein reales ENTSO-E-Netz nicht erreicht.** Der PyPSA-Adapter konnte in dieser Containerumgebung nicht ausgeführt werden, da PyPSA nicht installiert war und der Paketindex nicht erreichbar war. Getestet sind NumPy/SciPy-Kernfunktionen mit sieben `pytest`-Tests. Ein Produktionsfreigabestatus wird nicht behauptet.

# 15. Priorisierte Implementierungsschritte

1. **Echte Dateneingänge binden (verpflichtend):** Originalnetz, Profil- und Dispatchdaten, AC-Zweige einschließlich Transformatoren, Ratings, HVDC und PST sowie eindeutige Trägerinformationen. Validierung der PyPSA-Version **1.4.0** oder bewusst gepinnter Folgeversion.
2. **A/B unter gleicher Topologie ausführen:** über die tatsächlichen Snapshots Scores bilden, alternative Bilanzausgleichsschlüssel für B testen, beide Busmaps ausgeben und algebraisch prüfen. Bei großem Netz die PTDF nicht zwingend dicht materialisieren, sondern Flüsse mit Sparse-DC-Lösungen berechnen.
3. **Drei Referenzen und Ersatzknoten vergleichen:** gleiche Zonen, gleicher Validierungsdatensatz; kein Auswahlentscheid aufgrund von Marginalkosten allein. Auswahl mittels unabhängiger Flussgüte und Stabilität.
4. **Realisierbaren Ersatznetz-Fit produktionsfähig machen:** Projektions- und Snapshotfit getrennt dokumentieren, Offset in mathematische Netzrestriktionen integrieren, saisonale Parameterstrategie festlegen.
5. **Security qualifizieren:** N-1 und CBCO-Definitionssatz, korrekte MVA-/MW-Konversion, Richtung, Saison, statistische Identifizierbarkeit, unabhängige Kontingenzprüfungen. Erst danach exportierte Zonenkapazitäten als qualifiziert bewerten.

# 16. Schlussfolgerung

Die frühere technologieabhängige PTDF-Idee und die ENTSO-E-nahe Netzreduktion konkurrieren **nicht**: Die erstere macht räumliche Einspeiseverteilungen und ihren Einfluss auf **No-Load-/Strukturflüsse** sichtbar, die zweite bestimmt die **Topologie und physikalischen Ersatzparameter**. Als mathematischer Kern genügen die Operatoren $H_d,P_m,\Gamma_m,R_k(t)$; weder ein neuer AC-Solver noch separate elektrische Gleichungen pro Technologie sind erforderlich.

Eine Merit-Order-gewichtete Referenz ist eine **testbare ökonomische Hypothese**, keine physikalisch notwendige oder generell genauere PTDF. Positive Ersatzreaktanzen müssen als **Projektion auf ein physikalisch zulässiges reduziertes Netz** identifiziert werden. Der konstante Struktur-Offset muss als Näherung und nicht als automatisch aus der detaillierten Laststruktur exakte Konstante behandelt werden. Schließlich liefern aus zeitlichen Punktwolken geschätzte N-1-Kapazitäten nur mit nachgelagerter Security-Qualifikation belastbare Grenzen.

Für die weitere Forschung ist die direkte Paarung von **A: dispatchgetriebene Überlastungsinformation** und **B: RES-Last-basierte strukturelle Belastung** bei gemeinsamer Elektrik, Kalibrierung und *out-of-sample*-Validierung die methodisch klarste und am besten falsifizierbare Studiendesignentscheidung.

# Referenzen und Provenienz

- **[E1]** ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, Konsultationsfassung vom 25. Februar 2026, Kapitel 3.8 und Anhang 6.1: <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf>
- **[P1]** PyPSA, *Clustering API*, <https://docs.pypsa.org/latest/api/networks/cluster/>.
- **[P2]** PyPSA, *SubNetwork API*, PTDF/BODF, <https://docs.pypsa.org/latest/api/networks/subnetwork/>.
- **[P3]** PyPSA, *Installation*, <https://docs.pypsa.org/latest/home/installation/>. PyPI Stand Oktober 2026: `pypsa==1.4.0`.
- **[I1]** Früheres Chat-Artefakt: *ENTSOE_TYNDP2026_Netzreduktionsbericht.md*, Oktober 2026. Methodische Interpretation, keine Primärquelle.
- **[I2]** Früheres Chat-Artefakt: *TYNDP_PyPSA_Netzreduktion_Implementierungsbericht.md*, Oktober 2026. Softwarekonzept.
- **[I3]** Früheres Chat-Artefakt: *merit_order_ptdf_bericht.md* und *merit_order_ptdf_pilot.py*, synthetischer 6-Bus-Pilot mit 1.000 Fällen und fixem Saatwert. Nicht gegen realen TYNDP-Datensatz validiert.
- **[S1]** Dieses Paket: `tyndp_reduce/demo.py`, `outputs/comparison.csv`, `outputs/manifest.json`, `tests/test_core.py`; künstlicher 9-Bus-Modellfall mit Saatwert 20261016.
