---
title: "Wissenschaftliches Addendum: Flow-Based Market Coupling und TYNDP-nahe Netzreduktion"
subtitle: "Technologiespezifische PTDFs, GSK, CNEC, RAM, No-Load-Flows und PyPSA-Implementierung"
author: "Mathematische Methoden- und Softwarearchitektur"
date: "16. Oktober 2026"
lang: de-DE
fontsize: 10pt
geometry: "margin=24mm"
colorlinks: true
urlcolor: blue
linkcolor: blue
numbersections: true
toc: true
toc-depth: 2
---

# Executive Summary

**Kernergebnis.** Die bisher entwickelte TYNDP-nahe, technologieabhängige Netzreduktion und das europäische Flow-Based Market Coupling (FBMC) verwenden denselben **detaillierten linearen physikalischen Sensitivitätsoperator**, verfolgen aber unterschiedliche Modellziele. Die Reduktion bildet Originalleitungsflüsse auf Interzonenflüsse ab. FBMC prüft ausgewählte **kritische Leitungen unter ausgewählten Kontingenzen** (CNEC). Die mathematische Verwandtschaft lautet

$$
H^{(k)}_{\\mathrm{red}}=\Gamma H_dR_k,\qquad
H_{\\mathrm{FB}}=K H_dG.
\tag{1}
$$

Hierbei ist $R_k$ die räumliche, technologieabhängige Verteilungsabbildung; $G$ ist der Generation/Load Shift Key, der **Änderungen der Handelsnettopositionen** in nodale Einspeisungsänderungen übersetzt. Die Unterscheidung ist physikalisch und ökonomisch bedeutend: Eine durchschnittliche Erzeugungsverteilung ist nicht zwingend die marginale Antwort auf eine grenzüberschreitende Transaktion.

**Hauptschlussfolgerungen:** (i) bestehende Technologienverteilungen sind **Kandidaten für GSKs**, keine automatisch gültigen operativen GLSKs; (ii) der von einer Referenzverteilung abhängige strukturelle TYNDP-Offset und der FBMC-Nullpositionsfluss sind algebraisch verwandt, aber über **andere Zweigoperatoren und Marktdefinitionen** gebildet; (iii) vier saisonale/richtungsabhängige Ersatzleitungsgrenzen sind **keine** FBMC-RAM-Werte; (iv) die wirtschaftlich begründete Merit-Order-Gewichtung kann die FB-Domäne substantiell verändern, ist aber nicht per se sicherer oder realistischer.

Der beigefügte **Python-Erweiterungsbaustein** erzeugt einen vereinfachten vorregulatorischen, N-1-basierten FB-Polyeder aus einem detaillierten DC-Netz und drei statischen GSK-Hypothesen. Er arbeitet ohne PyPSA-Abhängigkeit im mathematischen Kern. Offizielle RAM-Schritte (minRAM/AMR, NRAO, IVAs, LTA/Long-Term-Nominations usw.) sind **nicht implementiert**. Die Ergebnisse sind **synthetisch** und keine Core-/JAO-Kapazitätsberechnung.

# 1. Normativer und wissenschaftlicher Geltungsbereich

Für die **TYNDP-Netzreduktion** ist weiterhin ausschließlich das ENTSO-E-Dokument *TYNDP 2026 – Identification of System Needs Methodology*, Konsultationsfassung 25.02.2026, Kap. 3.8 und Anhang 6.1 maßgeblich [T]. Dieses Dokument beschreibt Clustering, stündliche PTDF-Flüsse, äquivalente Reaktanzen, Zero-Balance-Korrekturen und N-1-bezogene äquivalente saisonale/richtungsabhängige Transfergrenzen.

Für **FBMC** sind andere Quellen erforderlich, da der TYNDP-Text keine operative Core-Kapazitätsberechnung normiert. Herangezogen wurden die Core-Day-Ahead-Prozessdarstellung der ENTSO-E [F1], das JAO-Publication-Tool-Handbuch [F2], die ACER-Übersicht der Core-Kapazitätsmethodiken [F3] sowie zwei aktuelle PyPSA-Dokumentationsbeispiele zur Berechnung und Verwendung von Flow-Based-Domänen [P1, P2]. Insbesondere die 2026 veröffentlichten Änderungen an der Core-Kapazitätsmethodik zeigen, weshalb das vorliegende Research-Prototype **keinen** Anspruch auf die rechtlich aktuelle operative CCM erhebt.

# 2. Gemeinsame nodale Netzphysik und verschiedene Projektionsoperatoren

Sei $A_d\in\mathbb R^{N\times L}$ die Knoten-Zweig-Inzidenz und $X=\operatorname{diag}(x_l)$ die Reaktanzmatrix eines zusammenhängenden, verlustlosen AC-Teilnetzes in DC-Approximation. Die nodale PTDF $H_d\in\mathbb R^{L\times N}$ bildet *balancierte* Einspeisungsänderungen auf Zweigflussänderungen ab:

$$
\Delta f_d=H_d\Delta p_d,\qquad
\mathbf{1}^{\mathsf T}\Delta p_d=0.
\tag{2}
$$

## 2.1 TYNDP-Reduktion: Flussaggregation

Die Planungsknoten-Zonen-Matrix $P_T\in\{0,1\}^{Z_T\times N}$ und der Leitungs-Schnittoperator $\Gamma_T\in\{-1,0,1\}^{E_T\times L}$ sind aus der **gewählten Busmap** abgeleitet:

$$
p_T=P_Tp_d,\qquad f_T=\Gamma_T f_d,\qquad
A_T\Gamma_T=P_TA_d.
\tag{3}
$$

Für eine Referenzdisaggregation $R_T$ mit $P_TR_T=I$ gilt

$$
H_T=\Gamma_T H_d R_T.
\tag{4}
$$

Der Operator $\Gamma_T$ **summiert** die Flüsse aller physischen Leitungen zwischen je zwei Planungszonen. Interne Leitungen erhalten keine eigene Zeile im reduzierten Schnittnetz.

## 2.2 FBMC: kritische Zweige und Ausfälle

Ein CNEC ist ein **Critical Network Element** in Kombination mit einer relevanten **Contingency**, also üblicherweise eine überwachte Leitung/Transformator unter Ausfall eines anderen Elements. Für einen überwachten Zweig $\ell$ und Ausfall $k$ folgt linearisiert:

$$
f_{\ell}^{(k)}=f_\ell+\mathrm{LODF}_{\ell k}f_k.
\tag{5}
$$

Eine Zeile des CNEC-Operators $K\in\mathbb R^{C\times L}$ besitzt damit in den Spalten $\ell$ und $k$ die Faktoren $1$ und $\mathrm{LODF}_{\ell k}$. Ohne Ausfall ist die Zeile nur ein Selektor $e_\ell^{\mathsf T}$. Für mehrere CNECs:

$$
f_C=K f_d,\qquad H_C=K H_d.
\tag{6}
$$

Der kritische Unterschied: $K$ **bewahrt physische kritische Flussrestriktionen**, statt die einzelnen Leitungsflüsse zu einem Zonenschnitt zu summieren. Eine thermisch kritische Leitung, die innerhalb einer Marktzone liegt, kann im FBMC weiterhin einen grenzüberschreitenden Handel begrenzen. Inselbildende Ausfälle oder Netztopologieänderungen benötigen eine gesonderte Modellierung, da das LODF-Standardverfahren dann nicht gilt.

# 3. Technologiespezifische PTDFs und Generation Shift Keys

## 3.1 Warum dieselbe Matrixstruktur nicht dieselbe Bedeutung hat

Sei $P_B\in\{0,1\}^{Z_B\times N}$ die **offizielle Marktgebotszonenpartition** und $G\in\mathbb R^{N\times Z_B}$ die GLSK-/GSK-Verteilung mit

$$
P_BG=I_{Z_B}.
\tag{7}
$$

Bei einer Nettohandelsänderung $\Delta NP$ mit $\mathbf1^\mathsf T\Delta NP=0$ gilt

$$
\Delta p_d\approx G\Delta NP,\qquad
\Delta f_C=K H_dG\Delta NP.
\tag{8}
$$

Entsprechend lautet die zonale, CNEC-bezogene Markt-PTDF

$$
\boxed{Z_{\\mathrm{FB}}=K H_dG.}
\tag{9}
$$

Die frühere technologiespezifische PTDF $H_T^{(k)}=\Gamma_TH_dR_k$ ist deshalb eng verwandt. Das $R_k$ beschreibt aber normalerweise **Niveauanteile** (wo RES-Verfügbarkeit, Last oder installierte konventionelle Leistung räumlich liegen); ein operatives GSK beschreibt **marginale Einspeisungs- und Nachfrageänderungen** zur Änderung einer **Bidding-Zone-Net-Position**. Eine statische technologie-/kostenbasierte Verteilung kann als *hypothetisches GSK* ausprobiert werden, darf aber nicht ohne Datenqualifikation als tatsächlich verwendetes Core-GLSK bezeichnet werden. ENTSO-E weist ausdrücklich darauf hin, dass GLSKs von den TSOs erzeugt werden und stündlich variieren können [F1].

## 3.2 Drei aus unserer Studie unmittelbar verfügbare GSK-Kandidaten

Für die Knoten $i$ einer Marktzone $z$ können Vergleichsoperatoren gebildet werden:

$$
G^{\\mathrm{uni}}_{iz}=\frac{1}{|\mathcal N_z|},\qquad
G^{\\mathrm{cap}}_{iz}=\frac{C_i}{\sum_{j\in\mathcal N_z}C_j}.
\tag{10}
$$

Ein *explizit als Research-Proxy deklarierter* Merit-Order-Schlüssel könnte etwa

$$
G^{\\mathrm{MO}}_{iz}=
\frac{C_i\,\psi(c_i)}{\sum_{j\in\mathcal N_z}C_j\,\psi(c_j)},
\qquad \psi(c_i)>0,\quad \psi'(c_i)<0,
\tag{11}
$$

mit festen marginalen Grenzkosten $c_i$ benutzen. Das im Code getestete Beispiel setzt $\psi(c)=1/(1+c/50)$ und ist **keine physikalische oder europäische regulatorische Formel**. Gleichung (11) ist ferner kein tatsächlicher Merit-Order-Clearingalgorithmus mit Begrenzungen und Residualbedarf; sie ist eine glatte, positive Kostenpräferenz.

**Vorteil:** Die GSK-Hypothese kann ohne stündlich optimierten Dispatch als stabiler Sensitivitätsoperator verwendet werden. **Nachteil:** Die Kostenannahme sagt nicht zwingend voraus, an welchen Knoten sich der Betrieb bei einer Nettohandelsänderung tatsächlich anpasst. Eine feste Kernkraft- oder Gasreferenz kann ihren Einfluss überschätzen, falls Anlagen nicht flexibel sind oder nicht am marginalen Handel reagieren.

# 4. F0 im TYNDP-Netzmodell und F0/RAM im FBMC

Die im bisherigen Projekt diskutierte strukturelle TYNDP-Korrektur und die operative FBMC-Nullpositionskomponente sind **nicht identisch**, teilen aber eine exakte algebraische Zerlegung.

## 4.1 Gemeinsame algebraische Identität

Sei $p_d^{\\mathrm{ref}}$ ein balancierter nodaler Referenzzustand. Seine Marktpositionsprognose lautet $NP^{\\mathrm{ref}}=P_Bp_d^{\\mathrm{ref}}$. Mit einem festen detaillierten Offset $b_d$, z. B. bei vorgegebenem Phasenschieberzustand, ergibt sich:

$$
f_C^{\\mathrm{ref}}=K(H_dp_d^{\\mathrm{ref}}+b_d),
\qquad Z_{\\mathrm{FB}}=KH_dG.
\tag{12}
$$

Der Fluss bei **Nullstellung der modellierten Markt-Nettopositionen**, jedoch bei unveränderter intrazonaler Referenzstruktur, ist

$$
\begin{aligned}
f_{0,\\mathrm{FB}}
&=f_C^{\\mathrm{ref}}-Z_{\\mathrm{FB}}NP^{\\mathrm{ref}}\\
&=KH_d(I-GP_B)p_d^{\\mathrm{ref}}+Kb_d.
\end{aligned}
\tag{13}
$$

Der TYNDP-Strukturfluss für seine **eigene** Busmap lautet dagegen

$$
f_{0,T}=\Gamma_TH_d(I-R_TP_T)p_d^{\\mathrm{ref}}
\quad\text{(plus ggf. physikalische Offsets).}
\tag{14}
$$

Die Formeln unterscheiden sich in (i) der Zonenpartition $P_T$ gegen $P_B$, (ii) dem Zuordnungsoperator $R_T$ gegen dem marginalen GSK $G$, (iii) der Flussprojektion $\Gamma_T$ gegen dem CNEC-Operator $K$ sowie (iv) dem zeitlichen Referenzzustand.

**Wichtige Warnung zur Terminologie:** In operativen Veröffentlichungssystemen können mehrere Nullpositions- und Referenzflussgrößen existieren; das JAO-Handbuch unterscheidet unter anderem $F0core$, $F0all$, $F_{ref,init}$ und $F_{uaf}$. Ein mit (13) konstruierter Forschungswert darf **nicht ohne Anpassung des Bilanzraums** als einer dieser veröffentlichten Werte ausgegeben werden [F2].

## 4.2 Herleitung der Flow-Based Domain

Die affine CNEC-Flussprognose lässt sich für absolute Nettohandelspositionen $NP$ darstellen als

$$
\widehat f_C(NP)=f_{0,\\mathrm{FB}}+Z_{\\mathrm{FB}}NP.
\tag{15}
$$

Bei oberer thermischer Zweiggrenze $F_C^{\max}$ und einer noch zu bestimmenden positiven Sicherheitsmarge $FRM_C$ ergibt sich schematisch die gerichtete Beschränkung

$$
Z_{\\mathrm{FB}}NP\le F_C^{\max}-FRM_C-f_{0,\\mathrm{FB}}.
\tag{16}
$$

Die Gegenrichtung erhält die gespiegelte Form

$$
-Z_{\\mathrm{FB}}NP\le F_C^{\max}-FRM_C+f_{0,\\mathrm{FB}}.
\tag{17}
$$

Die rechten Seiten sind in einer einfachen DC-Modellstudie **vorläufige Restkapazitäten**. Sie sind weder die im Core-Prozess publizierten finalen RAMs noch eine valide Nachbildung aktueller Methoden für die regulatorische Mindestkapazität. In der Praxis werden z. B. Außenhandelsbeiträge, Remedial Actions, Reliability Margins, minRAM-Anpassungen und Validierungskorrekturen in einem koordinierten Kapazitätsberechnungsprozess verarbeitet [F1, F2].

Für einen gesamten Satz orientierter CNECs ist der vereinfachte, konvexe Marktbereich

$$
\boxed{D_{\\mathrm{FB}}=\{NP\mid\mathbf1^\mathsf T NP=0,\;MNP\le RAM\}}.
\tag{18}
$$

Dieser Polyeder ist **nicht** identisch mit unabhängigen bilateralen Leitungskapazitäten zwischen Planungszonen. Die zulässige A-B-Übertragung hängt von gleichzeitigen anderen Handelspositionen ab.

# 5. Engpasskriterien der beiden Clustering-Methoden und FBMC

Unsere **Methode A** wählt kritische Leitungen auf Basis jährlicher (synthetisch gemessener) Überlastungsenergie unter vollständigem Dispatch. Sie ist der ENTSO-E-TYNDP-Methode näher als Methode B. Ihre tatsächlichen Überlastungsscores hängen jedoch von Marktergebnissen und Annahmen ab. Ein FBMC-CNEC muss deshalb **nicht** zu den am häufigsten überlasteten Leitungen gehören: Auch thermisch weitgehend freie Elemente können große *marginale Handels-Sensitivitäten* besitzen.

Unsere **Methode B** gewichtet den gesamten RES-Last-verursachten Leitungsfluss, auch ohne Überlastung. Sie ist hilfreich, um strukturell wichtige Flusskorridore zu erfassen. Sie kann aber interne CNECs mit starkem grenzüberschreitendem Einfluss übersehen, wenn diese in den RES-Last-Screeningfällen wenig belastet sind.

Der ergänzende **FBMC-nahe Screening-Indikator** sollte sich daher aus den *Handelssensitivitäten* ableiten, etwa

$$
S_c^{\\mathrm{FB}}=\max_{a\ne b}\big|(Z_{\\mathrm{FB}})_{c,a}-(Z_{\\mathrm{FB}})_{c,b}\big|.
\tag{19}
$$

Dies misst, wie stark eine 1-MW-Transaktion zwischen zwei Marktgebotszonen den CNEC beeinflusst. Für die Core-CCM wird von ENTSO-E ein 5%-Filter auf maximaler Zone-zu-Zone-Sensitivität für die frühe CNEC-Selektion beschrieben [F1]. Gleichung (19) ist ein **Screening-Proxy** und ersetzt nicht die vollständigen Auswahl-, Rechen- und Betriebsregeln.

| Kriterium | A: Überlastung | B: RES/Last-Belastung | FBMC: CNEC-/GSK-Sensitivität |
|:--|:--|:--|:--|
| Analysiertes Signal | MW oberhalb thermischer Grenze | MW-Transport oder relative Last | $\partial f_{CNEC}/\partial NP$ |
| Dispatchbezug | hoch | gering, expliziter Bilanzausgleich | prognostizierter CGM/GLSK |
| Schützt interne kritische Marktleitungen? | nur bei expliziter Partitionserhaltung | nicht garantiert | ja, bei Auswahl als CNEC |
| Modellziel | langfristige Engpassrepräsentation | strukturelle RES-Last-Korridore | Marktzulässigkeitsbereich |
| Hauptrisiko | markt- und szenarioabhängig | Ausgleichskonvention | falsches GSK/CNEC/FRM/Referenzniveau |

**Empfehlung:** A und B bleiben die zwei primären Clusterverfahren. $S^{\\mathrm{FB}}$ wird als **unabhängiger dritter Evaluationsindikator** verwendet, nicht automatisch als dritte Busmap-Zielfunktion. Besonders kritisch ist der Anteil relevanter CNECs, der im Planungsnetz intrazonal verschwindet.

# 6. Räumlicher Grenzfall: Planungszonen sind keine Marktgebotszonen

Die ENTSO-E-TYNDP-Methodik sieht intern erheblich mehr zonale Planungsknoten als offiziell gehandelte Bidding Zones vor. Deshalb dürfen Spalten einer Planungs-PTDF nicht unmittelbar als operative Markt-PTDF interpretiert werden.

Wenn alle Planungszonen vollständig jeweils innerhalb einer Marktgebotszone liegen, kann es einen zusätzlichen Aggregationsoperator $Q$ geben:

$$
P_B=Q P_T.
\tag{20}
$$

Falls eine Planungszone eine Bidding-Zone-Grenze schneidet, gilt (20) für eine einfache one-hot Zuordnung **nicht**. Dann sind die beiden Partitionen getrennt im hochaufgelösten Originalnetz zu verwalten. Selbst bei existierendem $Q$ ist der entsprechende GSK und CNEC-Operator nicht automatisch aus den TYNDP-Impedanzen oder der Zonenschnitt-PTDF rekonstruierbar.

Ein *direkter* Import von saisonalen, gerichteten TYNDP-Ersatzleitungsgrenzen als FBMC-RAM scheitert daher mehrfach:

1. Die Grenzen gelten für reduzierte **Interzonenschnitte**, nicht für einzelne kritische Leitungen unter Kontingenzen.
2. FBMC-RAM ist um Prognosebasisflüsse, Sicherheitsmargen und weitere operative Parameter angepasst.
3. Mehrere CNECs koppeln die Handelsergebnisse aller Marktgebotszonen **gleichzeitig**; nicht unabhängige NTC-ähnliche Box-Grenzen.
4. Der Referenzhorizont (2035/2040/2050-Planungswetterjahre versus kurzfristige D-2-Vorhersage) ist grundsätzlich unterschiedlich.

# 7. Wissenschaftlich bevorzugte Kopplungsarchitektur in PyPSA

Die robuste Lösung ist **keine Verschmelzung** von TYNDP-Ersatzleitungskapazitäten mit dem Core-Marktbereich, sondern ein *dualer Ergebniszweig* aus demselben hochaufgelösten Referenznetz:

**Planungszweig:** $H_d, p_d(t) \to$ Cluster A/B $\to (P_T,\Gamma_T)$ $\to$ Ersatzimpedanzen, $F_0$, saisonale Interzonengrenzen.

**FBMC-Zweig:** $H_d, p_d^{ref}(t),P_B,G_t \to$ CNEC/LODF-Operator $K_t$ $\to Z_{FB,t},f_{0,FB,t},RAM_t$ $\to$ experimenteller FB-Polyeder und Marktsimulation.

Die Datenbasis kann dieselbe sein; die **Operatoren und Gültigkeitsbedingungen bleiben unabhängig**. In einer langfristigen Planung können hypothetische zukünftige FB-Domänen unter Szenarioannahmen berechnet werden, dürfen jedoch nicht mit publizierten Day-Ahead-RAM-Werten gleichgesetzt werden.

## 7.1 Vergleichsmetriken

Ein belastbarer Test sollte vier getrennte Fehlerfamilien liefern:

- **Flussäquivalenz**: RMSE von $\Gamma_Tf_d$ gegen das reduzierte Ersatzmodell, auf nicht verwendeten Stunden.
- **GSK-Modellfehler**: $KH_d\Delta p^{\\mathrm{actual}}$ gegen $KH_dG\Delta NP$ auf beobachteten plausiblen Handelsverschiebungen.
- **CNEC-Sicherheitsfehler**: Anteil der vom experimentellen FB-Polyeder erlaubten Handelspositionen, die im detaillierten N-1-Modell Überlastungen verursachen (bei identischer Basis und zulässigen RAs).
- **Marktwirkung**: Kosten-/Wohlfahrts- und Preisunterschiede eines FBMC-Marktlaufs zu einem durch denselben Datenstand qualifizierten Referenzfall.

Eine reine RMS-Flussmetrik genügt für FBMC nicht: Kleine Fehler auf stark begrenzenden CNECs können große Wirkungen auf den Marktbereich besitzen.

# 8. Reproduzierbarer synthetischer Vergleich

Die neu implementierte Erweiterung verwendet das **gleiche frei konstruierte 9-Knoten-/15-Leitungs-Netz** wie der bisherige Methodenbericht. Die Marktpartition besteht für dieses Zusatzexperiment aus **drei** Bidding Zones, unabhängig von den A/B-Planungsbusmaps mit fünf Zonen. Der Referenzzustand besteht aus skalierten mittleren synthetischen Einspeisungen; der Netzparameterstand ist fest. Alle N-0-Zweige und die für die BODF gültigen geordneten N-1-Zweigpaare werden überwacht. Die vorläufige Marge ist pauschal 10% der Demonstrations-Zweiggrenze. Ein ausdrücklich vereinfachter Handelssensitivitätsfilter nutzt die Schwelle 5%.

| GSK-Proxy | Kandidaten-CNECs N-0/N-1 | $S_c^{FB}\ge5\%$ | RMSE Nullpositionsfluss [MW] | Bilateral A→B [MW] | Bilateral A→C [MW] |
|:--|--:|--:|--:|--:|--:|
| Gleichmäßig | 225 | 166 | 5,380 | 88,770 | 74,140 |
| Kapazitätsgewichtet | 225 | 198 | 5,092 | 84,184 | 76,605 |
| Merit-Order-Proxy | 225 | 211 | 4,874 | 69,359 | 65,475 |

Die bilateralen Zahlen sind **eindimensionale Schnitte** des *vereinfachten* FB-Polyeders für einen Handel zwischen jeweils zwei Zonen und alle anderen Nettohandelspositionen gleich null. Sie dürfen nicht gleichzeitig ausgeschöpft oder mit echten veröffentlichen Core-Kapazitäten verglichen werden. $S_c^{FB}\ge5\%$ ist nur ein Forschungsindikator. Der Nullpositionsfluss-RMSE misst die Größe des Offsets, **nicht** dessen Vorhersagefehler oder die Qualität des GSK. Dass Merit Order hier die kleinere Offset-Norm hat, ist deshalb **keine Güteaussage** für das operative Market Coupling.

Die Beispielrechnung zeigt jedoch etwas Grundsätzliches: **Dieselbe Netztopologie und derselbe nodale Referenzzustand können durch Änderung der GSKs merklich andere Marktbereiche ergeben.** Das ist der wichtigste operationelle Testfall für unsere wirtschaftlich gewichtete PTDF-Hypothese.

# 9. Softwaredesign und reproduzierbare Ausführung

Die bestehende Architektur `tyndp_reduce` bleibt erhalten und erhält die pure-NumPy/SciPy-Erweiterung `fbmc_bridge.py`. Sie enthält:

- `market_partition`: getrennte Bidding-Zone-Knotenzuordnung $P_B$;
- `gsk_uniform`, `gsk_from_positive_weights`, `validate_gsk`: GSK-Kandidaten und strenge $P_BG=I$-Prüfung;
- `cnec_operator`: N-0/N-1-Zweigoperator $K$ über die bestehende BODF-Routine; inselbildende Ausfälle werden abgewiesen;
- `build_domain`: Berechnung von $KH_dG$, exakter Referenzflussidentität, Nullpositionsfluss und gerichteten, **nicht regulatorisch qualifizierten** RAM-Proxy-Grenzen;
- `select_sensitive_cnecs`: maximale Zone-zu-Zone-Sensitivität (slack-invariant) als Vorselektion;
- `bilateral_capacity`: einseitige Marktbereich-Schnittgröße bei festem Außenhandel;
- `maximise_net_position`: grundlegendes LP über den vollständigen Forschungs-Polyeder.

Beispielaufruf im erweiterten Projektordner:

```bash
python -m pip install -e '.[test]'
pytest -q
python examples/run_fbmc_bridge.py
```

Der Beispielcode schreibt `outputs/fbmc/fbmc_gsk_comparison.csv` und für alle drei GSK-Proxys einen gerichteten Zeilenexport `outputs/fbmc/fbmc_domain_<gsk>.csv`. **Teststand: 16 kombinierte mathematische Kerntests bestanden; PyPSA selbst ist in der hiesigen Ausführungsumgebung nicht installiert.**

**Produktionsintegration:** Die offizielle PyPSA-Dokumentation bietet bereits Beispiele für (a) nodale und zonale PTDF/GSK-Transformation inklusive CNEC, RAM und N-1 [P1] und (b) Markt-Clearing mit einem zusätzlichen `pool`-Bus, Zone-zu-Pool-Links sowie `linopy`-Constraints $Z_{FB}NP\le RAM$ [P2]. Dieses Muster sollte verwendet werden, statt Marktnettopositionen als passive Leitungen des TYNDP-Ersatznetzes zu missdeuten. Der bereitgestellte Kern berechnet die Matrizen; eine aktuelle und reale PyPSA-Linopy-Integration muss vor einer Produktionsfreigabe eigens in einer gepinnten Umgebung geprüft werden.

# 10. Grenzen, Bewertung und Arbeitsprogramm

**Sehr hohe konzeptionelle Kompatibilität:** Die GSK-Abbildung ist algebraisch der früheren technologieabhängigen PTDF-Abbildung ähnlich; der Differenzterm der detaillierten Referenzverteilung liefert einen sauber definierbaren Nullpositionsfluss.

**Keine automatische physikalische Äquivalenz:** Eine technologiespezifische Referenz-PTDF muss keine positive-Reaktanzen-PTDF einer festen reduzierten Topologie sein. Ein vermaschtes Ersatznetz kann die CNEC-Sensitivitäten des detaillierten Netzes zudem nicht ohne weitere Informationen vollständig bewahren.

**Keine direkte RAM-Übertragbarkeit:** TYNDP-Kapazitäten sind Planungsersatzparameter. FBMC-RAM ist das Ergebnis eines spezifischen operativen Kapazitätsberechnungs- und Validierungsprozesses. Die beiden dürfen nicht stillschweigend ineinander umgerechnet werden.

**Priorisierte, kurze nächste Route:** (1) Beide Busmaps A/B beibehalten; (2) Marktgebotszonenpartition unabhängig hinzufügen; (3) für reale CNEC-Daten sowie beobachtete NP-Änderungen technologie-/kapazitäts-/kostenbasierte GSKs benchmarken; (4) die von $KH_dG$ induzierten zulässigen Domänen gegen eine detaillierte Security-Prüfung validieren; (5) anschließend ein kleines PyPSA/Linopy-Zonal-Clearing aufbauen, ohne den TYNDP-Planungszweig zu verändern.

**Status:** Mathematischer Zusammenhang **hergeleitet**, prototypische FBMC-Kernoperatoren **implementiert und synthetisch getestet**. **Keine** regulatorisch exakte Core-Replikation, kein TSO-CGM, kein reales CNEC-/GLSK-/JAO-Dataset und kein produktives PyPSA-FBMC-Clearing in dieser Umgebung.

# 11. Dokumentierte Quellen

- **[T] ENTSO-E (2026):** *TYNDP 2026 Identification of System Needs Methodology*, Konsultationsfassung, Kapitel 3.8 und Anhang 6.1. <https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf>
- **[F1] ENTSO-E:** *Core CCR: Day-ahead capacity calculation process explained*. <https://www.entsoe.eu/bites/ccr-core/day-ahead/>
- **[F2] JAO:** *CORE – Publication Tool for DA CCM*, Handbuch, insbesondere Referenzfluss-, F0- und RAM-Felder. <https://www.jao.eu/sites/default/files/news/mail/Core_PublicationTool_Handbook.pdf>
- **[F3] ACER:** *Capacity Allocation and Congestion Management: Regional Methodologies, Core Day-ahead*. <https://www.acer.europa.eu/electricity/implementation-monitoring/cacm>
- **[P1] PyPSA-Dokumentation:** *Determining Flow-Based Domains*. <https://docs.pypsa.org/latest/examples/fbmc-building-domain/>
- **[P2] PyPSA-Dokumentation:** *Flow-Based Market Coupling*. <https://docs.pypsa.org/stable/examples/fbmc-simple-example/>
- **[I] Vorheriger interner Projektbericht:** *Vergleich und Softwaredesign TYNDP-naher Netzreduktionsmethoden mit PyPSA*, 16.10.2026; die Untersuchungen des aktuellen Gesprächs und das beigefügte Projekt `tyndp_reduce`.
