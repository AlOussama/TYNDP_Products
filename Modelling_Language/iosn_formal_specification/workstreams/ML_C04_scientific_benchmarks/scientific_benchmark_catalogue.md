# ML-C04 — Scientific Micro-Benchmark Catalogue v0.1

**Stand 2026-11-12 | NONNORMATIVE RESEARCH | G1 BLOCKED | AUTHORITY_UNCONFIRMED.**
Versionierte Eingangsbaseline: ML-R00-Commit 9162def25d22c37b1fbc38f7d80fe929425cc8d2, Draft-PR #32. Quellen dieses Katalogs: ML-R01 M01–M18, ML-R04 mathematical_verification_rules.md / synthetic_reference_cases C01–C10 / risk_based_conformance_policy.md sowie ML-R00 cross_workstream_consistency_review.md. O26 ist ein Konsultationsentwurf vom 25.02.2026, keine autorisierte 2026-Norm. Der Katalog ergänzt die R04-Kleinstfälle; er ersetzt sie nicht und ändert keine ursprünglichen SR, Methodikentscheidungen oder Orakel.

## 0. Testvertrag und Anwendungsgrenzen

- **D2 – Wetter:** Y={2035,2040,2050} als getrennte Studien; CY={CY1,...,CY5} exogen gegeben. Für jedes CY gilt w_{2035,c}=w_{2040,c}=w_{2050,c}=w_c; daraus folgt *keine* Gleichheit w_CY1=...=w_CY5. Normierung und reale Zahlen bleiben Owner-/Quellenfrage. B01/B02 nutzen **ausdrücklich künstliche ungleiche** Gewichte (0.10,0.20,0.30,0.15,0.25).
- **D4 – UTC/Einheiten:** Intervalle als eindeutige UTC-Halbintervalle [start,end), Δt in h. Leistung MW, Energie MWh; H2 mit expliziter eigener Energiebasis. EUR, EUR/MW und EUR/MWh in Beispielen sind *synthetische Testwährung*, nicht freigegebene CAPEX-/VoLL-/Diskontparameter.
- **D3/D5-A1:** fehlende verpflichtende wissenschaftliche Evidenz bleibt FAIL, BLOCKED, UNSUPPORTED oder NOT_EXECUTED je Ursache; keine universelle algebraische Identität. Testtiefe D0 Struktur, D1 Semantik, D2 analytisches/synthetisches Oracle, D3 generierte Variablen/Rows/Koeffizienten, D4 parametrische/projizierte Äquivalenz.
- **Status je Aussage:** S=SYMBOLIC_PROOF, A=ANALYTICAL_DERIVATION, X=EXECUTED_SYNTHETIC_LOCAL (nur explizit im Ausführungsprotokoll), N=NOT_EXECUTED_NATIVE. Ein erwarteter Wert in cases.json ist **kein** ausgeführter Lauf; ein lokaler Oracle-Selbsttest verifiziert weder einen Generator noch ein Optimierungsmodell.
- **Geltungsbereich:** B01–B15 sind bewusst winzig und fiktiv. Alle namentlich geforderten 14 Familien sind abgedeckt; B15 ergänzt die durch M17 implizierte Offshore-Quellenregel. Fehlende MD/CL, geprüfte Daten, akzeptierte Toleranzen, Kostenperiodisierung und reale Netzkalibrierung werden nicht ersetzt.

Notation: x [MW] Investition, u [MW] ENS-Leistung, w_c [1] CY-Gewicht, Δt [h], c_op und VoLL [EUR/MWh], C_inv [EUR für den fiktiven Fixturehorizont], f [MW] Branchfluss, θ [rad bzw. rein illustrativer Winkelmaßstab], b [MW/Winkeleinheit], E [MWh], η [1]. Bei B05 sind PTDF/LODF dimensionslos; geometrische Strecken km. Jede ausdrücklich genannte Zahl einschließlich Konstanten ist ILLUSTRATIVE.

## 1. Benchmark-Index und Traceability

|ID|Hypothese / fachliche Pflicht|MA01-SR (wichtigste)|M01–M18|vorrangiger Falsifikationsweg|
|---|---|---|---|---|
|B01|Ein x über CY, ungleiche synthetische Gewichte über CY aber gleiche Vektoren über Y|002,010,027,029,030,040|M01,M02,M07,M08|D2+D3, Nonanticipativity-D4|
|B02|CAPEX einmal; gewichtete ENS-/VoLL-Energie über Zeit|010,011,027,043,044|M01,M02,M03|D2+D3, Kostenbuchung|
|B03|UTC, echte Δt und MW→MWh|004,011,040|M02,M12|D0+D2, Zeitintegral|
|B04|physische DC-Masche hat KVL, controllable market link nicht|018,024,028,035,036|M04,M05,M06,M07|D2+D3+D4|
|B05|zusammenhängende Partition, Cut-Erhaltung, PTDF-/LODF-/N−1-Notwendigkeiten|013–023|M05,M09,M10,M11,M12|D2+D3; Detail-Oracle offen|
|B06|Stage-Inventar, Übergabe und CAPEX ohne Doppelzählung|003,027,030–033|M01,M03,M07,M08|D3 + Szenariovergleich|
|B07|Speicherleistung/Energie, intertemporale SoC-Erhaltung|033,034|M13|D2+D3+D4|
|B08|getrennte Strom-/H2-Einheiten und stündlich eingefrorenes Elektrolyseprofil|007,008,009,039,050|M04,M15,M18|D2+D3|
|B09|Hydro-Klassen, Erhaltung und DSR-Ressourcenidentität|041,042|M14,M16|D1+D2+D3|
|B10|LF mit DC-Mesh ≠ OPF; OPF-Deckel nur bei Aktivierung|024,025,026,028|M05,M06,M18|D3 konditional|
|B11|Formulierungsäquivalenz ohne algebraische Textgleichheit|018,027,029,043,044,047|M01,M03,M05,M13|D4 Projektion/Beweis|
|B12|mehrere optimale, aber unterschiedliche Portfolio-Vektoren|001,025,046,047|M01,M18|D2+D4 optimal face|
|B13|Postprocessing-Erwartungswert und nicht definierte KPIs|001,023,025,045,046|M02,M12,M18|V5-Rekalkulation + D3|
|B14|Pflicht-Toolfähigkeit nicht überspringen; optionale OPF separat|003,026,029,035,047|M07,M08,M18|V6-D0/D3 Status|
|B15|Offshore-Ziele exogen, theoretische Routen/Quellfaktoren offen|005,006,037,038,048|M09,M17|D1+D3 Source-Provenienz|

In der begleitenden benchmark_requirement_traceability.csv werden alle zugeordneten *existierenden* MA01-SR-IDs einzeln geführt. CONTEXT und PARTIAL sind **keine** positive Prüfabdeckung. Für jede Familie sind positive und negative Orakel nur für genau den genannten Mini-Scope spezifiziert.

## 2. Einzelne Benchmarkfamilien

### B01 — Gemeinsame Investition mit nichtuniformen CY-Gewichten
**Hypothese:** Zu einem Studienjahr y existiert nur ein x_y, nicht x_{y,c}; derselbe **CY-Gewichtsvektor** gilt symbolisch über die drei unabhängig optimierten Studienjahre. Indexe C={CY1,...,CY5}; Eingaben d_c=[0,1,2,3,4] MW, w=[.10,.20,.30,.15,.25], Δt=1 h, 0≤x≤4 MW, CAPEX=3 EUR/MW, VoLL=10 EUR/MWh (alle fiktiv). u_c=max(0,d_c−x) MW. Positiv: min_x 3x+10 Σ_c w_c u_c hat eindeutiges x=3 MW, ENS-Erwartung .25 MWh und Zielfunktion 11.50 EUR. Negativ N1: separat x_c=min(d_c,4) mit gewichteter CAPEX erbringt 6.75 EUR, ist nichtantizipativ **verboten**. N2: versehentlich w_c=.2 ergibt bei x=3 Wert 11.00 EUR; N3: je CY ungewichtete CAPEX verfünffacht 9 EUR zu 45 EUR. **Nachweis A/S:** stückweise Steigungen in analytical_reference_oracles.md, Var-Indizes und Kopplung müssen zusätzlich D3 belegen. **Entdeckt:** Fehlkopplung, falsche w-Achse, falsche Kostenanzahl. **Nicht:** reales CY-Manifest, Stufenkosten MD-02, tatsächliche Optimierer/gleichwertige Modellimplementierungen.

### B02 — Erwartungswert und einmalige CAPEX-/VoLL-Bewertung
**Hypothese:** Für feste, ausdrücklich gewählte Intervallgewichte erfolgt ENS-Kostenrechnung als Σ_c w_c Σ_t VoLL·u_ct·Δt_t; Investitionswert außerhalb der Summe. C=5, T=2, Δt=(.5,1.5) h, u_c=(1,0,2,4,5) MW, VoLL=100 EUR/MWh und C_inv=7 EUR (fiktiv). Positiv E_ENS=5.1 MWh, ENS-Wert 510 EUR, Gesamt 517 EUR. Negativ gleiche Wettergewichte (4.8 MWh), fehlende Δt oder fünfmal CAPEX. **Nachweis A/D3:** Zielfunktionskoeffizienten mit Einheiten und synthetischer Rekonstruktion. **Entdeckt:** systematische Rechen-/Skalierungsfehler. **Nicht:** Quelle/Preisjahr/WACC/Discount-/Blockformel; M03 bleibt MD-02-BLOCKED.

### B03 — UTC und Leistung/Energie
**Hypothese:** Kanonische UTC-Intervallidentität ist von lokaler DST-Uhrzeit unabhängig, MW wird nur mit Δt zu MWh. T: [2026-03-29 00:00Z,00:30Z) und [00:30Z,02:00Z); P=(2,4) MW. Positiv Δt=(.5,1.5) h ⇒ 7 MWh. Negativ Summe=6 (MW fälschlich als MWh), beide Δt=1 oder Zeitintervall-Duplikat. **Nachweis A/D0/D2:** Datums-/Intervall- und Einheitsaudit. **Entdeckt:** Schritt-/Zeitzonenfehler und doppelte Intervalle. **Nicht:** vollständiges Kalender-/Leap-/missing-hour-Ownerprofil MD-12.

### B04 — KCL/KVL gegenüber marktbasierten DC-Links
**Hypothese:** Für physische AC-Ersatzzweige (DC-Näherung) erzwingt KVL f_AB=f_AC+f_CB; ein neuer steuerbarer DC-Marktlink darf dagegen seine Flüsse innerhalb NTC wählen. N={A,B,C}, B_phys={AB,AC,CB}, b=1 MW/Winkel, p=(+90,−90,0) MW, θ=(60,0,30). Positiv f=(60,30,30) MW. Als Marktlink AB ist (90,0,0) bei zulässiger NTC möglich. Negativ: physischer AB als freier Link akzeptiert (90,0,0), erfüllt KCL aber verletzt KVL; neue Kandidaten als AC-Winkelzweig auf das physische Dreieck zurückzwingen entfernt zulässige Markträume. **Nachweis S/A, D3/D4:** KCL-Zeilen, physisches Cycle-Subspace, Branch-Typ, Link-NTC. **Nicht:** kalibrierte PST/HVDC/no-load-Regeln, indirektes NTC-Mapping MD-09.

### B05 — Zonen, PTDF/LODF und N−1
**Hypothese:** Eine Clusterzuordnung ist disjunkt und vollständig, jede Zone in der definierten Detailtopologie zusammenhängend; Cut-Flüsse und additive Injektionen konservieren. Pfad A1–A2–B: {A1,A2}→X ist verbunden; {A1,B}→X wäre es nicht. Separater Detail-Cut-Test mit p=(30,20,−50) MW und f=(-10,40,10) MW liefert p_X=50 MW, f_XY=50 MW; Weglassen des 10-MW-Cuts ergibt 40 MW (FAIL). Ergänzend DC-Dreieck wie B04: PTDF_AB/AC/CB=(2/3,1/3,1/3), bei p_A=+90,p_B=−90 ergibt f=(60,30,30). Für *genau diesen* störungsfreien Dreiecksfall führt Ausfall AB zu (0,90,90) MW und LODF_AC,AB=LODF_CB,AB=1.0. Falsches LODF=0 liefert 30 statt 90 MW. Vier saison-/richtungsabhängige Ratingfelder und sechs P06-Ausgabeklassen sind strukturell nachzuweisen; 100 MW Restbranchrating ist ausschließlich illustrativ. **Nachweis A/S:** PTDF- und Re-Dispatch-Kontingenzgleichungen; D2/D3. **Nicht:** reale 102-Zonen-Partition, LODF bei islanding, Netzkalibrierung, RMSE/Owner-Toleranz MD-03/13/15. Cut-Erhaltung ist nur notwendig.

### B06 — LP-Stufen und Übergabemechanismen
**Hypothese:** Pflicht sind unterscheidbare Stufen, Kandidatenmenge, Übernahmeevidenz und einmalige ökonomische Verbuchung; *die konkrete* Stage-1-Fixierung ist **nicht autorisiert (MD-07)**. Ausschließlich konditionaler Test: Stufe 1 erlaubt real x1∈[0,2] MW mit Kosten 2 EUR/MW und Bedarf 1 MW (ENS-Penalty 10 EUR/MWh), ⇒ x1=1. Stufe 2 mit **hypothetisch fixiertem** x1 erlaubt konzeptionell x2∈[0,2], Bedarf 2 MW, Preis 1 EUR/MW ⇒ x2=1, Endportfolio (1,1), Kosten 3 EUR. Negativ: Stage-1-Resultat ignorieren und beide Variablen neu optimieren ⇒ (0,2), Kosten 2 EUR; oder x1-Kosten doppelt zählen ⇒ 5 EUR. **Nachweis A/D3:** Stufenmanifest, aktive Kandidatenindices, bounds, Übergabefunktion, Kostenledger. **Nicht:** endgültige zulässige Übergabe, Annuität, Jahr-zu-Jahr-Kopplung oder Stufe-3-Regeln. Kein stiller Ersatz der zwei Stufen durch ein einziges Joint-LP.

### B07 — Speicher und SoC
**Hypothese:** Energie e_t [MWh] und Leistung p [MW] sind getrennte Dimensionen; bei festem E_max>0 ist s=e/E_max eine bijektive Zustandsrepräsentation. Beispiel E_max=4 MWh, e0=2 MWh, Ladung 2 MW×.5h mit η_ch=.8, danach Entladung 1 MW×.5h mit η_dis=.5. Positiv e1=2.8, e2=1.8 MWh, s=(.5,.7,.45). Negativ Δt vergessen ⇒ e2=1.6 MWh; keine intertemporale Zeile ⇒ unphysikalische Entladung. **Nachweis A/S, D3:** zwei State-transition-Zeilen und Kapazitätsgrenzen. **Nicht:** echtes End-SoC, Verluste, Dauerklassen, exogene 2035-Speicher oder endogene E_max-Normalisierung ohne Nichtlinearität (MD-06).

### B08 — Strom/H2 und eingefrorene Elektrolyselast
**Hypothese:** Elektrische MW und H2-MWh werden nur über η und Δt gekoppelt; der P14-Freeze ist zeitschritt-, CY- und zonengenau. Beispiel P_EL=10 MW_e, η_E2H=.7, Δt=.5h ⇒ 3.5 MWh_H2. P_H2E=1.4 MW_e, η_H2E=.4 verbraucht 1.75 MWh_H2, weitere H2-Nachfrage 1.75 MWh_H2 schließt die Bilanz. Frozen-Vektor [3,7] MW_e bei [.5,1.5]h enthält 12 MWh_e. Negativ [6,6] enthält ebenfalls 12 MWh, verletzt aber **jede** Intervall-Identität; η=1 statt .7 erzeugt falsche H2-Energie. **Nachweis A/D3:** getrennte Carrierbilanzen, Zeitindex, vor-expansiver Profil-Hash, H2-Netzkapazität exogen. **Nicht:** tatsächliches frozen-preexpansion-H2-Profil, alle H2-Netzregeln und Scope weiterer Frozen-Variablen MD-10.

### B09 — Hydroklassen und DSR ohne Doppelverwendung
**Hypothese:** Die fünf Hydrotypen run-of-river, pondage, reservoir, offenes und geschlossenes Pumpspeicherwerk bleiben klassifiziert; für einen definierten Reservoirtest gilt Ressourcenerhaltung. Beispiel e0=4 MWh_water_eq, Zufluss=1 MW_water_eq und Turbine=1 MW_water_eq über 2h ⇒ e1=4; Wegfall des Zuflusses ergibt e1=2 (FAIL). Separat als **nur illustratives reines Shiftprodukt**: Basislast (6,4) MW, außerhalb des Marktes implizit auf (4,6) verschoben, unabhängiges explizites Asset δ=(−1,+1) MW ⇒ (3,7) MW; Summe bei 1h je Schritt bleibt 10 MWh. Negativ: dieselbe Asset-ID sowohl als implizite und explizite DSR führen; die Energie kann sogar korrekt bleiben, weshalb eine Ressourcen-/Eligibility-Prüfung erforderlich ist. **Nicht:** universelle Shiftfenster-, Rebound-, Hydro-Inflow-/Endzustandsregeln MD-16.

### B10 — LF-Baseline und optionale OPF-Erweiterung
**Hypothese:** LF bewahrt DC-Physik, lässt aber die methodisch betroffenen internen Kapazitätsbounds unbindend; eine separat aktivierte OPF-Expansion wird durch das freigegebene LF-Portfolio begrenzt. Zweiknotennetz mit 5-MW-KCL-Fluss, physisch b=1, illustrativer Betriebsrating=3 MW: LF erlaubt den 5-MW-Fluss mit gültiger θ-Differenz, OPF mit 3-MW-Bound **nicht** ohne weitere Dispatchanpassung. Bei LF-Kandidatenlimit 2 MW ist x_OPF=1 MW zulässig und 3 MW unzulässig. Negativ R=3 bereits auf LF erzwingen oder x_OPF>2 zulassen. OPF=false ⇒ nur bedingter OPF-Test NOT_APPLICABLE, **nicht** LF-Tests. **Nachweis A/D3** über Modus-Provenienz und Kandidatencaps. **Nicht:** tatsächliche LF-Ausnahmeleitungsmenge, OPF-Dispatchvergleich, MD-08.

### B11 — Formulierungsäquivalenz
**Hypothese:** Projektionsgleichheit gilt für Contract-Variablen, nicht für Text/Variablenanzahl. A: x+y≥4, x,y≥0; min 2x+3y. B: 2x+2y−2s=8, s≥0 und x,y≥0 mit s=x+y−4. E-FEAS und bei gleicher Zielfunktion E-OPT sind **symbolisch** bewiesen; Optimum (4,0), Wert 8. Negativ s≥0 entfernen erlaubt (x,y,s)=(0,0,−4), Wert 0. Ergänzend Gegenbeispiele gegen E-FEAS⇒E-OPT, E-OPT⇒E-FEAS und E-OBS⇒andere Aussagen im Äquivalenzbericht. Winkel/PTDF/Zyklus, Nonanticipativity-Replikation und SoC-Normalisierung werden dort mit exakten Annahmen behandelt. **Nicht:** globale Gleichwertigkeit reeller IoSN-Toolmodelle ohne D4-Annahmen.

### B12 — Mehrfach optimale Portfolios
**Hypothese:** E-OPT verlangt gleiche optimale Lösungsmenge *nach Projektion*, aber keine identischen vom Solver zufällig ausgewählten Vektoren. 0≤x,y≤1 MW, x+y=1 MW, min x+y. Positiv (1,0), (0,1), (.5,.5) mit Wert 1 und Summe 1 MW. Negativ ein Comparator verwirft (1,0) vs (0,1) wegen Feldungleichheit trotz korrekter Feasibility-/Objective-Zertifikate. **Nachweis S/A:** gesamte optimale Streckenmenge; gegensätzliche, aber zulässige per-Asset-KPI-Ausgaben sind möglich. **Nicht:** tatsächliche IoSN-Portfoliokosten, freie Toleranz oder bereits definierte KPI-Äquivalenz.

### B13 — Postprocessing, Aggregation und undefinierte KPIs
**Hypothese:** Raw-Ausgaben bleiben unverändert; erwartete ENS-MWh werden als ΣwΣΔt·u und Kosten über explizite VoLL errechnet, nicht als MW-Summe. B02-Input liefert 5.1 MWh und 510 künstliche EUR, ungefilterte ungewichtete CY-Gesamtenergie dagegen 24 MWh. Negativ Summe aller CY ohne Gewichte als offiziellen KPI publizieren oder bei fehlender Formel-ID/Filtergrenze PASS melden. **Nachweis A/V5** nur für diese rechenbaren Rohgrößen; OWNER_DEFINED-KPI=BLOCKED und Threshold=TBD. **Nicht:** Welfare, Systembedarfsfilter, Discount- oder offiziell zu veröffentlichende Aggregationsregeln MD-04/17.

### B14 — Fehlende Toolfähigkeit und übersprungene Tests
**Hypothese:** Eine nicht unterstützte verpflichtende Market-Link-Fähigkeit ist UNSUPPORTED, kein PASS und kein NOT_APPLICABLE. Ein optionaler OPF-Test ist nur bei nachweislichem OPF=false NOT_APPLICABLE; bei true und fehlender Fähigkeit UNSUPPORTED. Positiv: korrektes Fail-Closed-Metadatenorakel verweigert den Gesamtclaim. Negativ: stiller Testskip und pauschales Gesamt-PASS. **Nachweis D0/V6** über Feature-/Anwendbarkeitsmanifest, D3 über Generatorinventar, wenn Tool verfügbar ist. **Nicht:** Fähigkeit eines konkreten Tools (kein echtes Tool getestet).

### B15 — Exogenes Offshore-Ziel und Route (zusätzliche Familie)
**Hypothese:** Für eine versionsbelegte Offshore-RES-Zielgröße entsteht keine frei optimierte RES-Ausbauvariable; theoretische Verbindungen benötigen Geometrie-/Kosten-Provenienz. Beispiel exogen 100 MW, Rohdistanz 100 km und **synthetischer** Faktor α=.12 ⇒ 112 km *nur bei ausdrücklich angenommener relativer Aufschlagsdefinition*. O26 nennt für benannte Klasse eine Spanne 10–15 %, keine freigegebene finale Wahl. Negativ: 12 % als verbindlichen Wert deklarieren oder 100-MW-Ziel zur endogenen Investition machen. **Nachweis D1/D3** über Manifest, Referenzquellen und Variableninventar. **Nicht:** tatsächliche Trasse, GIS-Oracle, autorisierte Kostenkurve oder Eligibility MD-05/14.

## 3. Evidenzanforderung statt Algebra-Pflicht

Ein positives rein analytisches Oracle darf mit einem abweichend formulierten Tool-LP vereinbar sein. Bei mathematischen A-Risiken muss zusätzlich geprüft werden, ob die *generierten* Gleichungen, Indizes, Bounds, Zyklusbeziehungen und Objektarten das entsprechende invariant definierte Entscheidungsproblem darstellen. Ein übereinstimmender Zielfunktionswert kann eine falsche zulässige Menge oder zufällige Gleichheit überdecken. Eine fehlende Orakelfreigabe ist nicht durch geringe Solverresiduen heilbar.

**Nicht durch diese Arbeit beschlossen:** produktive Akzeptanztoleranzen, echte Wettergewichte, Defektpriorisierung, KPI-/Discountformeln, robustes Optimierungsziel, Wetterjahrselektion, reale 102-Zonen-/N−1-Qualitätsgrenzen, Stage-Fixierung, konkrete Toolarchitektur oder irgendeine Zertifizierung. D6-A meint weiterhin **zwei unabhängig implementierte Tools**, nicht zwei Übersetzungen desselben Modells.
