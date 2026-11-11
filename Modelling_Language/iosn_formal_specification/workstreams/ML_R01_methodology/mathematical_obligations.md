# ML-R01 — Mathematische Verpflichtungen und Äquivalenzbedingungen

**Status:** nichtnormative, toolunabhängige Forschungsformalisierung · 11.11.2026 · **G1 BLOCKED**.  
**Primärquelle O26:** ENTSO-E, *TYNDP 2026 Identification of System Needs Methodology*, **Version for Public Consultation, 25 February 2026**; insbesondere §§3.1.1, 3.3–3.11, 4.1–4.6, Anhang 6.1. **Nicht genehmigte Entwurfsreferenz.**  
**Ergänzung H24:** ENTSO-E, *Identification of the System Needs Study Methodology – TYNDP 2024*, **Version for ACER, European Commission and EU Member States Opinion, 9 April 2025**, §7.3.2, gedruckte S.42, als historischer LF-Vergleich. Gültigkeit für 2026 **TBD**, keine Normersetzung. CBA4 §2.5.1 nur über Verweis aus O26 §3.4.

**Legende:** [O] direkt beschriebene Entwurfsanforderung; [D] Projektentscheidung D1–D6; [S] wissenschaftliche Ausformulierung mit angegebenen Voraussetzungen; [E] äquivalente Formulierung *nur unter nachzuweisenden Voraussetzungen*; [I] ausschließlich illustrative Gleichung; [TBD] offene Methodik, Daten oder Verifikationsparameter. Eine [S]- oder [I]-Formel ist nicht automatisch wörtlich in O26 enthalten; ihre Geltung als Konformitätsprüfung ist wissenschaftlich vorgeschlagen, nicht genehmigt.

## A. Indizes, Dimensionen, Modellgrenzen

| Zeichen | Definition | Dimension und Konvention | Grundlage |
|---|---|---|---|
| \(y\in Y=\{2035,2040,2050\}\) | Studienjahr, separat optimiert | Jahr-ID, **keine endogene y→y+1-Kopplung** | [O] §3.2; SR-002/-003 |
| \(c\in C=\{CY1,\ldots,CY5\}\) | exogen ausgewählte Wetterfälle | gemeinsame Identitäten, Zeitreihen je y,c | **[D] D2**, **Abweichung von O26 §3.7: drei andere Fälle je y** |
| \(\pi_c\) | Fallwahrscheinlichkeit | \(\pi_c\ge0,\ \sum_c\pi_c=1\), **identisch für alle y**, Zahlen **TBD** | [D] D2; [S] normierte Wahrscheinlichkeit |
| \(t\in T_{y,c}\) | Betriebsintervall | kanonischer UTC-Start/Ende; \(\Delta t_{yct}>0\) in h | [D] D4; MD-12 |
| \(n\in N^E\), \(h\in N^H\) | Strom- bzw. H2-Zone | stabile Identität, Bilanzen getrennt | [O] §§3.3, 3.8 |
| \(\ell\in L^E\), \(a\in L^H\) | reduzierter physischer elektrischer Zweig / exogener H2-Link | MW bzw. definierte H2-Transportrate | [O] §§3.6,3.8 |
| \(k\in K_y\) | wählbarer Stromübertragungskandidat | Asset-ID, Richtung, MW und Kosten | [O] §§3.10,4.5.2 |
| \(x_{y,k}\) | gemeinsam beschlossener Ausbauumfang | MW oder separate technologiespezifische Kapazitätsdimension | [O] §3.1.1 |
| \(p^g,p^d,p^{shed},p^{ch},p^{dis},q^{E2H},q^{H2E}\) | Betriebs- und Kopplungsgrößen | konsequent MW\(_e\), MW\(_{H2}\) oder MWh pro Schritt | [S] auf O26 §§3.1.1,3.3,4.3–4.4 |
| \(C^{inv},Q^{op}\) | Investitions- und Betriebskosten | *gleiche* Bewertungs-/Währungs- und Preisjahrbasis | [O] §3.1.1; [TBD] MD-02 |

**Drei voneinander getrennte Achsen:** Studienjahr \(y\), Wetterfall \(c\) und UTC-Zeit \(t\); Szenariowahrscheinlichkeit ist **kein** Zeitschrittgewicht. Wetterfallauswahl, Gewichtsermittlung, PCA und K-Means sind upstream/out of scope (MA01-MR-012/-049). **Die O26-Angaben zu drei Wetterfällen werden nicht in das D2-Forschungsprofil hineinvererbt.**

### M01 [O+D+S] — Nichtantizipative, erwartungswertgewichtete Zielfunktionsstruktur

Für **ein** festes \(y\) gilt als allgemeine wissenschaftliche Normalform:

\[
\begin{aligned}
\min_{x_y,\{u_{yc}\}_{c\in C}}\quad &
C^{\mathrm{inv}}_y(x_y;\eta_y)
 + \sum_{c\in C}\pi_c\, C^{\mathrm{op}}_{yc}(x_y,u_{yc};\eta_y)\\
\text{s.t.}\quad &
x_y\in\mathcal X_y,\qquad
u_{yc}\in\mathcal U_{yc}(x_y),\qquad \forall c\in C.
\end{aligned}
\tag{M01}
\]

\(\eta_y\) fasst **quellbelegte oder TBD** Parameter zusammen. Der gleiche Vektor \(x_y\) geht in **alle fünf** wetterfallspezifischen Betriebsprobleme ein; es gibt keinen frei entscheidbaren \(x_{yc}\). In einer äquivalenten Szenario-Replikation mit \(x_{yc}\) sind **explizite** Kopplungsgleichungen \(x_{yc}=x_y\) obligatorisch. Investition wird nur einmal und **außerhalb** der Wetterfall-Erwartung angerechnet; keine per Wetterfall verfünffachte CAPEX. [O] O26 §3.1.1 S.12–14, MA01-MR/SR-027/-029; [D] D2 fünf und gleiche Gewichte; [S] explizite Mengenstruktur. **Keine** Annahme von minimax, CVaR, robustem Budget, neuem Sicherheitsstandard oder jahresübergreifender Endogeninvestition. [TBD] Zielfunktions-Kostengruppen und Periodisierung MD-02.

### M02 [O+S] — Operative Energiekosten und ENS korrekt bewerten

Eine **dimensionsrichtige illustrative Entfaltung** der O26-Kostenklasse ist:

\[
C^{\mathrm{op}}_{yc}
=\sum_{t\in T_{yc}}\Delta t_{yct}
\left(
\sum_g c^{\mathrm{var}}_{gyct}p^{g}_{gyct}
+\sum_{n} \mathrm{VoLL}_{nyct}\,p^{\mathrm{shed}}_{nyct}
+\sum_{j} c^{\mathrm{other}}_{jyct}\,u^{j}_{yct}
\right).
\tag{M02-I}
\]

[O] O26 §3.1.1 fordert wetterfallgewichtete Kosten und VoLL×nichtversorgte Energie; [S] MW\(\times\)h \(\to\)MWh und EUR/MWh\(\times\)MWh \(\to\)EUR; [I] Aufschlüsselung der sonstigen Kosten ist **keine O26-KPI- oder verbindliche Kontendefinition**. Falls die Upstream-Kosten bereits **EUR/Intervall** statt **EUR/MWh** tragen, darf \(\Delta t\) nicht erneut multipliziert werden. Für Szenariorepräsentativität oder Zeitblockgewichtung sind **keine** zusätzlichen Koeffizienten ohne ein freigegebenes Kalender-/Samplingprofil zulässig (MD-12). Lastabwurf \(p^{shed}\) [MW] und nichtversorgte Energie \(E^{ENS}=\sum_t p^{shed}\Delta t\) [MWh] sind unterschiedliche Datentypen.

### M03 [O+S+TBD] — Investitionskosten und Diskontierung

\[
C^{\mathrm{inv}}_y(x_y;\eta_y)
=\mathcal V_y\Bigl(\{\,\mathrm{Cashflow}_{k,\tau}(x_{y,k})\,\}_{k,\tau};
\text{Preisjahr, Referenzjahr, WACC, Lebensdauer, Blockdefinition}\Bigr).
\tag{M03}
\]

\(\mathcal V_y\) ist ein **TBD-Bewertungsoperator**, keine freigegebene Formel. [O] O26 §4.6 S.39–40 nennt für benannte Transmission-/Batteriekandidaten WACC 4 %, Transmission-Lebensdauer 25 Jahre und Diskontierung zum Bezugsjahr 2026; die Diskont-Blockreferenz ist sichtbar **beschädigt**. [S] Alle verglichenen Kosten benötigen kompatible Bezugsjahre, Quellenpreisstände, Lifetime-/CAPEX-/OPEX-Abgrenzung, Rundungs- und Zeitblöcke. [TBD] MD-02, MD-06: konkreter jährlicher Cashflow, Annuität vs Kapitalwert, Kosten je Kandidatenklasse, block-year-Regel. **Kein** erfundener Annuitätenfaktor oder pauschales 4%-Profil für fremde Technologien.

### M04 [O+S] — Elektrische Knotengleichung und Lastabwurf

Bei orientierter physischer Zweig-Inzidenz \(A^E_{n\ell}\) und Kandidatenlink-Inzidenz \(A^K_{nk}\) liefert eine **illustrative sign-konsistente** nodale Leistungsbilanz:

\[
\sum_{g\in G(n)}p^g_{gyct}
+p^{dis}_{nyct}-p^{ch}_{nyct}
-p^{E2H}_{nyct}+p^{H2E}_{nyct}
+p^{shed}_{nyct}
-d_{nyct}
-\sum_{\ell}A^E_{n\ell}f_{\ell yct}
-\sum_k A^K_{nk}m_{kyct}=0.
\tag{M04-I}
\]

[O] O26 §3.1.1 verlangt elektrische Bilanz, Netz-/Erzeugungsgrenzen und Politikrestriktionen; [S] gleiche Einheit MW\(_e\), keine Einspeiseverluste ohne explizite Modellregel. [I] Vorzeichen von \(A\), \(p^{E2H}\), \(p^{H2E}\), Aggregationsorte und Form einzelner Konversionen sind **Darstellung**, kein aus O26 wortwörtlich entnommenes Knotenrezept. [TBD] Abregelung, Ausfälle, Reserve und sektorale Doppelverbuchungsregeln MD-10/-16.

### M05 [O+S+E] — Vermaschtes Bestandsnetz: DC-Physik

Für einen physischen reduzierten AC-Ersatzzweig \(\ell=(i,j)\):

\[
f_{\ell yct}=b_\ell(\theta_{iyct}-\theta_{jyct})+f^{0}_{\ell yct}
+\phi^{\mathrm{PST/HVDC}}_{\ell yct},\quad
b_\ell=1/x_\ell^{eq},
\tag{M05-I}
\]

wobei die Darstellung von No-load-/PST-/HVDC-Effekten **nur** eine mögliche, korrekt kalibrierte Äquivalenzform ist. [O] §§3.8.2–3.8.3/Anhang 6.1 erfordern die ermittelten Äquivalenzimpedanzen, Nullbilanzflüsse, Maschenrestriktionen und PST/HVDC-Einwirkungen; §3.1.1 DC-Lastfluss. [S] \(A f=\) nodale physische Netzeinspeisung; auf **jeder** geschlossenen Masche erfüllt der Fluss die entsprechende Kirchhoff-Spannungswinkelsumme; ein Slackwinkel je zusammenhängender Komponente ändert keine Flüsse. [E] Winkel- und Zyklusflussdarstellung sind äquivalent, wenn dieselben PTDF-/No-load- und Inzidenzkonventionen und konsistente Netzkomponenten verwendet werden. **Nicht** äquivalent: Ersatz aller Bestandsleitungen durch frei disponierbare zonale Links ohne Maschengesetz. [TBD] kalibrierte Parameter und Vorzeichenkonvention, MD-03/-15.

### M06 [O+S] — Physische Interzonen-Kapazität im LF und OPF

Definiere **eine** Modussemantik \(R_{\ell,s,d}^{mode}\), mit Saison \(s\in\{Sommer,Winter\}\) und Richtung \(d\in\{+,-\}\). Im LF-**Investitions**modus werden *interne Interzonen-Transferkapazitätsrestriktionen* nicht bindend angesetzt, während M05 und die übrigen technisch/politisch geltenden Grenzen erhalten bleiben:

\[
\mathcal U_{yc}^{LF}
=\{u:\mathrm{Balance},\mathrm{DCMesh},\mathrm{UnitConstraints},\mathrm{PolicyConstraints}\};
\quad
\mathcal U_{yc}^{OPF}
=\mathcal U_{yc}^{LF}
\cap\{u:-R^-_{\ell,s}\le f_{\ell yct}\le R^+_{\ell,s}\}.
\tag{M06-S}
\]

Die Mengenform ist ein **vereinfachtes Struktur-Schema**, kein Beweis, dass ein reales OPF ausschließlich diese Restriktionen ergänzt. [O] O26 §3.9 S.29, MA01-SR-024/-025/-026; [H24] älterer Vergleich §7.3.2 gedruckte S.42 bestätigt als Kontrollbeispiel den Erhalt der Impedanzen trotz unbegrenzter interner Übertragungslimits. **H24-Autorisierung für 2026 offen.** [TBD] MD-08: genauer Scope „interner“ Links, Saison-/Richtungsabbildung, Ausnahmen, Vergleichsfahrplan. Nicht ein tatsächlich unendlicher numerischer Big-M-Wert als willkürliche Eingabe.

### M07 [O+S] — Ausbaukandidaten sind steuerbare DC-*Marktlinks*

\[
0\le x_{y,k}\le\overline x_{y,k},\quad
-\mathrm{NTC}_{k}^{-}(x_{y,k})\ \le\ m_{kyct}\ \le\ \mathrm{NTC}_{k}^{+}(x_{y,k}).
\tag{M07-I}
\]

[O] O26 §4.5.2 S.37–38 definiert Kandidaten als **controllable DC market links** trotz möglicher physischer AC-Technologie, und benennt direkte/indirekte NTC-Wirkungen. §3.1.1 beschränkt LP-Investitionsgrößen linear. [S] Marktlinkfluss \(m\) ist steuerbare Entscheidungsvariable; er geht in die **Knotenbilanzen** ein, wird **nicht** durch neue Winkel-/Impedanzgleichung des bestehenden AC-Äquivalentnetzes fixiert. [I] Das einfache bilaterale \(\mathrm{NTC}^{\pm}(x)\) ist **kein Nachweis**, dass alle Projektwirkungen nur auf einer Grenzverbindung liegen. Für mehrere direkte/indirekte NTC-Grenzbeiträge kann eine **source-basierte** Matrix \(H_{bk}^{\pm}\) erforderlich sein; Richtung und Vorzeichen bleiben [TBD] MD-09. Rein physisch ähnliche Onshore-Kandidaten sind nicht automatisch „gleichwertige“ Kirchhoff-Zweige.

### M08 [O+S+TBD] — Kandidatenmengen und Stufenübernahme

Für jedes \(y\) werden drei methodische Zustände unterschieden:

\[
\begin{aligned}
S^1_y &:= \mathrm{LP}\bigl(K^{real,onshore}_y\cup K^{real,offshore}_y;\ \mathcal U^{LF}_{yc}\bigr),\\
S^2_y &:= \mathrm{LP}\bigl(K^{residual,real}_y\cup K^{conceptual,onshore}_y
\cup K^{theoretical,offshore}_y;\ S^1_y,\mathcal U^{LF}_{yc}\bigr),\\
S^3_y &:= \mathrm{StorageLP}\bigl(S^2_y;\ y\in\{2040,2050\}\bigr).
\end{aligned}
\tag{M08-S}
\]

[O] O26 §3.10 S.30. Diese notationale Semantik ist **keine Festlegung**, ob Stage1-Investitionen fixiert, unter Restlimits reoptimiert oder anders in Stage2 übernommen werden. **TBD MD-07.** Zulässig ist nur eine kontrollierte Übergabefunktion \(F_y:\mathrm{Result}(S^1)\mapsto\mathrm{FeasibleInput}(S^2)\) mit ausdrücklicher Kosten-/Kapazitätsreconciliation ohne Doppelzählung. [S] \(C^{final}\) umfasst alle angewendeten Stufen im freizugebenden Kostenbezug; Stufe1-Ergebnis nicht per bloßem erneuten Summieren zweifach bepreisen. **Keine** automatische Zusammenfassung der zwei LPs in eine einzelne Optimierung, weil dadurch zulässige Investitionsprioritäten geändert werden können. **Keine** modellendogene Speicherexpansion 2035.

### M09 [O+S] — Netzpartition und geographische Zuordnung

Eine diskrete Zuordnung \(z:V^{detail}\rightarrow Z\) ist eine Partition:

\[
\forall v\in V^{detail}:\ \sum_{a\in Z}{\bf1}[z(v)=a]=1,\qquad
G^{detail}[z^{-1}(a)]\text{ ist verbunden}\quad\forall a\in Z_{\mathrm{occupied}}.
\tag{M09-S}
\]

[O] O26 §3.8.1 S.23–27/Anhang 6.1: Clustering nach Überlastungs- und Austauschcharakteristik, zusammenhängende Zonen, 102 Zonen als **O26-spezifische** Geographie; [S] vollständige Partition, Konnektivitätscheck. Überlastungsenergie **illustrativ** \(E_\ell^{over}=\sum_t\Delta t\max(0,\lvert f_{\ell t}\rvert-R_{\ell t})\) (M09-I), nur falls \(\Delta t\), Saisonrating und betrachtete Lastflussszenarien so definiert sind; keine neu erfundene Qualifikationsschwelle. [TBD] MD-03/-13, konkretes detailliertes Netz, normativer Clustering-Score und Ausnahmen.

### M10 [O+S+I+TBD] — Kalibrierung reduzierter Äquivalenz

Aus detailnetzbasierten Referenzflüssen \(f^{detail}_{r}\), Studienfällen \(r\) und einem methodisch zulässigen Parameterraum \(E\) kann die **illustrative** Flussanpassung als

\[
\min_{\xi\in E}\ \sum_{r\in \mathcal R}\omega_r
\left\|\mathcal P f^{detail}_{r}-f^{reduced}_{r}(\xi)\right\|_2^2
\tag{M10-I}
\]

geschrieben werden. [O] O26 §§3.8.2–3.8.3/Anhang 6.1 nennt Optimierung von Äquivalenzimpedanzen und No-load-Korrekturen, Übertragung physikalischer Meshbeziehungen, PTDF/LODF-/N-1-basierte Kapazitäten sowie Qualitätsprüfung inklusive RMSE. [S] \(\mathcal P\) ist eine quellenbelegte Detail→Zonenprojektion; Parameter \(\xi\) enthalten ausschließlich methodisch zulässige Komponenten. [I] \(L_2\)-Norm, Gewichte \(\omega_r\), Nebenbedingungen und Testfälle **nicht** als endgültig freigegebene O26-Optimierungsfunktion deklarieren.

**Sechs P06-Ausgabeklassen** sind gesondert zu referenzieren: (1) No-load-/Nullbilanz-Flüsse, (2) Mesh-/Maschenbeziehungen, (3) HVDC-Wirkung, (4) Kapazitäten, (5) Äquivalenzimpedanzen, (6) PST-Wirkung; saisonal/richtungsbezogen vier Kapazitätsvarianten. Fehlende Klassen sind unabhängig von numerischer Qualität erkennbar. [TBD] MD-03/-13/-15/MD-11: Detail-Oracle, Ranking, numerische Fehlergrenzen.

### M11 [O+S] — N-1/LODF als physikalische Kapazitätsableitung

Für einen Ausgangsflussvektor \(f^{(0)}\) und Leitungs-Ausfallfall \(k\) gilt bei vorhandener, methodisch gültiger LODF-Kalibrierung **als schematische Linearisierung**

\[
f_{\ell}^{(k)}=f_{\ell}^{(0)}+\mathrm{LODF}_{\ell k}f_k^{(0)}
\quad(\ell\ne k),\qquad
-R_{\ell,s}^{-}\le f_{\ell}^{(k)}\le R_{\ell,s}^{+}.
\tag{M11-S}
\]

[O] O26 §3.8.2/Anhang 6.1 S.49–51: aus detaillierten Netzflüssen und N-1/LODF abgeleitete äquivalente Übertragungskapazitäten. [S] Voraussetzung: linearisierter gültiger Referenzzustand, definierter Kontingenzsatz, keine Inselbildung oder Sonderfall ohne geeignetes Ersatzverfahren. \(\mathrm{LODF}_{\ell k}\) ist eine **netzabhängige Sensitivität**, nicht eine willkürliche Konstante. Vier Werte pro interzonaler Verbindung: Sommer/Winter mal beide Flussrichtungen. Die Kapazitätszuordnung benötigt einen **verifizierbaren detaillierten Vergleichsfall**, nicht einfache Summation von Thermallimits. [TBD] MD-03/-15: Oracle, Sicherheitsabstände, Islanding, Ausnahmekontingenzen.

### M12 [O+S] — Zonale Datenallokation und Reaggregation

Für eine **additive** Originalgröße \(d_v\) mit genau einem Zielraum \(z(v)\) ist

\[
d_a^{zone}=\sum_{v:z(v)=a} d_v,\qquad
\sum_a d_a^{zone}=\sum_v d_v.
\tag{M12-S}
\]

[O] O26 §3.8.4 S.28–29: Zuordnung von PEMMDB-/PECD-/DFT-Marktdaten zu Zonen, Kapazitäts-/Profilreconciliation. [S] Last und Kapazität dürfen nur summiert werden, wenn Einheiten, Bezugszeiten und Bilanzgrenzen identisch sind; RES-Verfügbarkeitsfaktoren \([0,1]\) sind **keine additiven Leistungen**. [TBD] MD-11/-12: Feedervintage, Knotenmap, Mappings, zulässige Differenzen. Beispiel: Ein auf 50 % und eines auf 80 % laufendes RES-Aggregat ist nicht durch Summieren der zwei Prozentzahlen beschrieben. Bei Quelländerungen ggf. indirekte Reconciliation via referenzierter disaggregierter Kraftwerks-/PECD-Zuordnung.

### M13 [O+S+I] — Speicherenergie und Leistungstrennung

Für eine Speicherklasse \(s\) und Betriebsschritt \(t\):

\[
e_{s,t+1}=e_{s,t}
+\eta^{ch}_s p^{ch}_{s,t}\Delta t
-\frac{p^{dis}_{s,t}\Delta t}{\eta^{dis}_s}
-\lambda_{s,t}\Delta t,\qquad
0\le e_{s,t}\le \overline E_s,\quad
0\le p^{ch/dis}_{s,t}\le\overline P^{ch/dis}_s.
\tag{M13-I}
\]

[O] O26 §§3.10,4.5.1: Speicherleistung/-energiedauer und mindestens zwei Speicherklassen, standardisierte Batterie als Modellproxy, Landestrajektorien, endogen 2040/2050. [S] intertemporale Energieerhaltung und dimensionsrichtige MW/MWh-Entkopplung; Betriebszustand hängt nicht von getrennten Wetterfällen ab **nur wenn** Methodik ein solches Boundary-Profil vorgibt — Standard ist je Fall eigener Verlauf. [I] \(\eta^{ch},\eta^{dis},\lambda\), End-SOC, Zyklengrenzen, zeitabhängige Kapazitätsabbauten und Verhältnis \(\overline E=d\overline P\) sind **illustrative Modellparameter**, keine erfundenen O26-Werte. [E] Normalisierter SoC \(s=e/\overline E\) ist bei korrekt behandeltem \(E>0\), Einheit und bilinearitätsfreier Fallunterscheidung äquivalent; Vorsicht beim endogenen Energievolumen. [TBD] MD-06/-16/-15.

### M14 [O+S] — Wasserkraftklassen und hydrologische Erhaltung

[O] O26 §4.3 S.35 unterscheidet (1) Laufwasser, (2) Pondage/kurzfristige Speicherung, (3) Reservoir/Speicherkraftwerk, (4) offenes Pumpspeicherwerk, (5) geschlossenes Pumpspeicherwerk. Ein Reservoirbedarf benötigt ggf. Zustandsbilanz

\[
V_{t+1}=V_t+I_t\Delta t+P^{pump}_t\Delta t
-R^{turb}_t\Delta t-S^{spill}_t\Delta t,
\tag{M14-I}
\]

in **konsistenten volumetrischen/energetischen Wasseräquivalenten**. [S] Masse-/Energieerhaltung und technische Grenzen sind keine Solverwahl. [I] Exakte Inflow-/Spillage-/Pumprepräsentation je Hydroklasse und Kopplung von Energie zur Wassermenge sind **quell- und fallabhängig** (MD-16); keine pauschale Gleichung für alle fünf Hydroklassen, insbesondere Laufwasser nicht automatisch als Jahresreservoir behandeln. PECD/Hydroprofile referenzieren CY1–CY5 nur im D2-Forschungsprofil.

### M15 [O+S+I] — Wasserstoffnetz, P2G und Rückverstromung

Für Hydrogen-Zone \(h\), Zeit \(t\), Wetterfall \(c\) **als illustrative erhaltene Stoff-/Energiebilanz**:

\[
\sum_{e\in EL(h)} \eta_e^{E2H}p^{EL}_{ect}
+ q^{H,source}_{hct}
+ q^{H,dis}_{hct}
+ q^{H,in}_{hct}
= d^{H}_{hct}
+q^{H,chg}_{hct}
+q^{H,out}_{hct}
+ \sum_{r\in H2P(h)}\frac{p^{H2P}_{rct}}{\eta_r^{H2E}}.
\tag{M15-I}
\]

Alle Summanden müssen in einer **einheitlichen H2-Energie- oder Massenflussdimension** geführt werden; bei Massenflüssen bedarf es expliziter Heizwert-/Einheitenumrechnung. [O] O26 §§3.3/3.6 S.15/18: zonale Strom-H2-Kopplung via Elektrolyse, H2-Rückverstromung, vorgegebene (exogene) Entwicklung der H2-Infrastruktur; [S] keine H2-Ausbauentscheidung unbemerkt im Strom-Expansionsvektor, aber betrieblicher H2-Dispatch ist zulässig. [I] dieser konkrete Knotenabschluss ist nur eine Möglichkeit; Boil-off, Druck, Kompressoren und Mindestlasten wären zusätzliche Modellannahmen, nicht aus der O26-Zusammenfassung als bindend ableitbar. [TBD] MD-10: H2-Topologie/Capacities, Konversionswirkungsgrade, Preis-/Nachfragemodelle und Freeze-Präprozess.

### M16 [O+S+TBD] — Demand-Side Response ist nicht ein einziges flexibles Lastprofil

[O] O26 §4.4 S.35–36: DFT-Stundenlast einschließlich EV/Wärmepumpe; **implizite DSR** verändert Lastprofile außerhalb der Markträumung; **explizite industrielle DSR** wird als market-responsive Flexibilität modelliert. [S] Keine doppelte Flexibilitätsanrechnung, indem eine implizit verschobene MW-Menge zusätzlich als angebotene DSR-Variable angesetzt wird. **Nur falls** ein explizites DSR-Produkt als reines Lastverschieben mit Energieerhaltung definiert ist, könnte \(\sum_{t\in W}\Delta t\delta d_t=0\) als [I]-Nebenbedingung gelten; O26 lässt **W** und produktspezifische Wiederholung/Verluste offen. [TBD] MD-16.

### M17 [O+S] — Offshorerouten, fixe Ziele und theoretische Kandidaten

[O] O26 §3.5 S.18: Offshore-RES-Ziele der Länder als exogene Vorgaben; qualifizierte Hybridprojekte im Startnetz. §§3.11/4.5.3 S.30–31,38–39: geographische Prüfung, theoretische VSC-Offshoreverbindungen; Quellstandard 525-kV-VSC-HVDC/2 GW für benannte Klasse; einheitlicher Seeumwegfaktor in einer Spanne **10–15 %**, exakter Wert offen. [S] Räumliche Streckenlänge und daraus abgeleiteter Kostenansatz sind mit einer **nachweisbaren** Geoquelle/Projekt-ID zu verbinden; fixe Offshore-RES-Kapazität ist nicht frei als Stromausbaukandidat auswählbar. **Illustrativ** \(L_{route,k}=L_{geometric,k}(1+\alpha)\) [I], **nur** falls „\(\alpha\) ist ein relativer Streckenaufschlag“ mit Bezugsgeometrie so freigegeben ist; \(\alpha\in[0.10,0.15]\) ist eine **Quellenspanne**, keine gültige Endwahl. [TBD] MD-05/-14, einheitlicher exakter Routenfaktor, Korridor-/Kostenverteilung und eventuelle Ausnahmen.

### M18 [O+S+TBD] — P13, P14, optionale P15 und P16

**P13:** Gleiche Szenario-/UTC-/Last-/Erzeugungsdaten, internes Netz mit methodisch festgelegten Ratings; vergleichen \(\mathcal D_y^{0}\) (ohne LF-IoSN-Portfolio) vs. \(\mathcal D_y^{1}\) (mit LF-IoSN-Portfolio). Die **deskriptive** Differenz \(\Delta Q_{yc}=Q_{yc}^{1}-Q_{yc}^{0}\) darf berechnet werden; **keine** fiktive offiziell anzuwendende Welfare-/KPI-Formel. [O] §3.9; [TBD] MD-04/-08/-17.

**P14:** Erhalte präexpansives Elektrolyseprofil \(\widehat p^{EL,pre}_{yct,h}\) als extern identifizierte Quellgröße und erzwinge in der **dafür vorgesehenen** Sensitivität \(p^{EL,sens}_{yct,h}=\widehat p^{EL,pre}_{yct,h}\) [S] für jedes relevante Intervall/Zone/CY; welche weiteren H2-Variablen „frozen“ sind, bleibt **TBD MD-10**. [O] §3.6. Ein nur gleicher Jahreswert ist **nicht** gleichbedeutend mit einem stündlichen Freeze.

**P15 (optional):** Falls eine gesonderte OPF-Expansion stattfindet, muss das als LF-Ergebnis zugelassene Kandidatenportfolio die OPF-Ausbauentscheidung begrenzen. Schematisch \(0\le x^{OPF}_{y,k}\le \widehat x^{LF}_{y,k}\) [I], **nur falls** \(\widehat x^{LF}\) dieselbe Richtung, Kategorie, Kapazität und den vom Owner festgelegten Deckel bezeichnet; anderenfalls ist ein äquivalentes, freigegebenes Portfoliomapping erforderlich. [O] §3.9; [TBD] MD-08.

**P16:** Zu jedem Systembedarf gehören Provenienz, Zieljahr, Geographie, Kandidaten-/Speicherklasse, dimensionsrichtiger Ausbau-/Kostenbezug, Quellen-/Runversion, Ausgangsportfolio, Status und Interpretation **Bedarf, keine Bauentscheidung**. [O] §§2.1–2.2/3.1.2/3.10–3.11; Kleinmengenfilter-Schwelle, Need→Korridor-Aggregation, KPI-/Welfare-/Offshorekostenformeln bleiben **MD-04/-05/-17-TBD**. Ohne freigegebene Formel keine numerische KPI-Bestehensbehauptung.

## B. Wissenschaftlich äquivalente vs. unterschiedliche Formulierungen

| Thema | Äquivalente Klasse unter Voraussetzungen [E] | Nicht äquivalente Abweichung |
|---|---|---|
| Erwartung / Investition | extensive Form mit einem \(x_y\) oder replizierte Investitionen mit \(x_{yc}=x_y\) | wetterfallabhängig variable \(x_{yc}\), Worst-Case/minimax, CAPEX-fünffach |
| LF-Physik | Winkel-DC, PTDF, Zyklusfluss mit gleichen No-load-/PST-Konventionen und Referenzknoten | beliebige Interzonen-NTC-Freiflussnetze ohne Maschenzwang |
| Marktlink | direktionale Variable, aufgespaltene positive/negative Links, sofern gegenseitige Semantik und Kosten abgebildet sind | Kandidat als Kirchhoff-AC-Leitung oder gerichteter Capacity-Zuwachs ohne Quellmapping |
| Speicher | Energiezustand oder normierter SoC, sofern zulässige Mengen und Initial-/Endwerte äquivalent sind | unbeschränkte Arbitrage oder fehlende Energiebilanz |
| Stufen | Austausch der *LP-Solvertechnik* oder exakt bewiesene äquivalente Stage-Probleme | Stufen 1+2+3 in ein Joint-Optimum zusammenziehen |
| Zeitskalen | UTC-konforme Intervalle mit belegter \(\Delta t\)/Aggregation und Erhalt relevanter Größen | stiller DST-Shift, fehlende Leap-Stunde, frei angenommener Repräsentativitätsfaktor |
| Output | gleiche optimale Kosten und beobachtbare Grenzgrößen in identischem Datenprofil, ggf. verschiedene degenerierte Optima | Identität aller Kandidaten-IDs als universelle Gleichwertigkeitspflicht |

**Präziser Äquivalenzbegriff:** Für dasselbe versionierte Eingabeprofil \(d\) und dieselben **freigegebenen** methodischen Parameter müssen die *Projektionen der zulässigen Mengen auf vertraglich beobachtete Größen* sowie die optimalen Zielfunktionswerte übereinstimmen. Solverinterne Variablen müssen nicht identisch sein. Ohne Ownerbestimmung der beobachteten Größen, der Degeneracy-Regel und numerischer Toleranzen (**MD-15/-17**) darf keine allgemeine Tool-Äquivalenz zertifiziert werden. Reine Rechenzeit- oder Variablenzahlunterschiede sind keine Methodikverletzung.

## C. Pseudocode — Forschungsreferenz, **nicht** ausführbares Modell

~~~text
given: O26 consultation methodology reference + D1..D6 research profile
require: external manifest CY1..CY5, same symbolic weight vector for y=2035,2040,2050
for y in [2035, 2040, 2050]:
    verify source identity, scenario identity, time/units/zone provenance
    construct qualified baseline grid and offshore reference (eligibility TBD)
    derive zonal partition and equivalent physical network (oracle TBD)
    map upstream data to zones, preserve energy/capacity balances
    construct electricity + H2 + hydro + DSR feasible operation
    register real, conceptual, theoretical candidates as controllable NTC market links
    S1 = solve separate LF LP over real onshore/offshore links
    S2 = solve separate LF LP over remaining/conceptual/theoretical links,
         using owner-specified non-double-counting stage transition (TBD)
    if y in [2040,2050]:
         S3 = solve separate storage stage with approved trajectories (TBD)
    else:
         S3 = exogenous storage only
    pairwise compare network-constrained dispatch without/with LF portfolio
    evaluate frozen pre-expansion hydrogen sensitivity with hourly value identity
    if optional OPF explicitly authorized:
         solve separately with LF portfolio ceiling under specified mapping
    derive reportable needs; apply threshold/KPI only if defined (otherwise BLOCKED)
    record solver-input identities, formula provenance and per-obligation evidence status
end
verify: not all fields are approved; missing oracle => BLOCKED, not PASS
~~~

**Pseudocode-Präzedenz:** Es handelt sich um ein fachliches Abhängigkeitsbild; keine Vorgabe von Skriptlaufzeit, Programmiersprache, API oder Architektur. P04/P05/P06 könnten als vorab berechnete, qualifizierte Inputs übergeben werden, wenn ihre wissenschaftliche Referenz und Verifikation erhalten bleiben; der vorgeschriebene Nachweis geht dadurch nicht verloren.

## D. D5-A1 — Verifikationsbedarf und Gegenbeispielklassen

| Risiko / Verpflichtung | Analytisches Kleinsttest-Orakel (zu entwickeln, **nicht ausgeführt**) | Blocker und Status |
|---|---|---|
| Nonanticipativity M01 | Zwei Wetterfälle mit entgegenwirkendem Dispatch-Optimum, ein gemeinsames \(x\); Szenario-spezifische \(x_c\) als Negativfall | Gewichtswerte/Validierungs-Toleranzen TBD; **DESIGN_ONLY** |
| Bewertungsdimension M02–03 | EUR/MWh × MW × h = EUR; Jahreskosten vs Kapitalwert isolieren | MD-02/12; **ORACLE_BLOCKED** |
| Bilanz/Physik M04–06 | Dreiknotennetz, Maschenzwang vs handelssteuerbarer Kandidatenlink; Slack-Neutralität | MD-03/08/15; **DESIGN_ONLY** |
| Kandidaten/Stufe M07–08 | Teilausbau Stufe1 und Restoption Stufe2, keine Doppelzahlung | MD-07/-09; **ORACLE_BLOCKED** |
| Aggregation M09–12 | Nicht zusammenhängendes Zonenpaar als Negativfall, PTDF/LODF N-1 und vier Ratings, Reaggregation von MW | MD-03/13/15; **ORACLE_BLOCKED** |
| Speicher/Hydro M13–14 | Ein-Zeitschritt-Energieerhaltung, Dauerklassen, Residuen/Endzustand | MD-06/16; **DESIGN_ONLY** |
| H2/DSR M15–16 | Elektrolyse/Rückstrom in gemeinsamen Einheiten, explizite und implizite DSR nicht doppelt | MD-10/16; **DESIGN_ONLY** |
| Offshore/Analyse M17–18 | Referenzgeometrie mit symbolischem Faktor, LF→OPF-Deckel, stündliche Frozen-H2-Identität | MD-04/05/08/10/17; **ORACLE_BLOCKED** |

**Fail-Closed D3:** Wo mathematische Eigenschaften feststehen, dürfen bereits symbolische/strukturelle Gegenbeispiele Verletzungen nachweisen. Ohne echte Datensätze, Freigabe des Orakels, numerische Grenzwerte oder native Läufe wird aber **kein erfolgreiches IoSN-Konformitätsurteil** erteilt. Die in O26 §5.1 erwähnte Plexos/Antares-Dreiknotenprüfung ist ein *wissenschaftliches Vergleichsbeispiel*, **keine Pflicht, diese Tools zu verwenden**. Ein identischer Optimalwert allein verifiziert nicht sämtliche verborgenen Nebenbedingungen; ein anderer optimaler Portfolio-Vektor allein beweist nicht die Nichtäquivalenz.

## E. Lückenstatus und semantisches Traceability-Minimum

Alle M01–M18 sind an O26-Klauseln und/oder Entscheidungen D1–D6 gebunden; illustrative Passagen sind gekennzeichnet. Wesentliche **noch nicht bestimmbar verbindliche Größen**: MD-01 Methodikrelease, MD-02 Finanzperiodisierung, MD-03/13 Netzreduktion, MD-04 KPI/Filter, MD-05 Offshorefaktor, MD-06 Speicherparameter, MD-07 Stufenlogik, MD-08 LF/OPF, MD-09 NTC-Mapping, MD-10 H2, MD-11 Inputfreeze, MD-12 UTC-Detailprofil, MD-14/MA02-CL-001 Eligibility, MD-15 numerische Orakel, MD-16 Hydro/DSR, MD-17 Degeneracy/Output, MD-18/19 Wetterdateneingang, MD-20 Baselineabgrenzung.

**Schluss:** Die wissenschaftlichen Invarianten lassen sich beschreiben, aber ihre vollständige parametrisierte Konformitätsprüfung nicht ohne Owner-/Data-/Oracle-Nachweise. **Keine allgemeine Robustheitsanforderung, kein vollständiges Optimierungsmodell, keine mathematische Konformitätsfreigabe. G1 = BLOCKED.**
