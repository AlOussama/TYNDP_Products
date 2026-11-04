# M2-MA2 – Global x/c0 Equivalent + Coupled-Country Re-Clustering: vollständiger Cold-Start-Handoff

**Dokument-ID:** M2-MA2-COLD-START-20261104
**Projekt:** AlOussama/TYNDP_Products
**Verbindliche technische Startbasis:** M2-MA1 Code-Freeze 0254d867a34b66ec7b56c90225605d29ea328916
**Berichts-/Review-Startbasis:** M2-MA1-Dokumentations-Commit 1089874c1cf4980fc8e6527297a6ed6123d7c709
**Arbeitsbranch für MA2:** neu von feature/iosn-m2-ma1-integration-20261104, **nicht** aus main oder dem alternativen m2-Branch, solange kein gemeinsamer Contract-Freeze beschlossen ist.
**Freigabestatus Start:** SYNTHETIC_TESTS_PASS; unabhängige MA1-R-PHY/R-CLU-Reviews PENDING; Realnetz BLOCKED_DATA; kein MA2-Runtime-Go durch diese Übergabe.

## 0. Copy-ready kurzer Ausführungsauftrag

> Führe M2-MA2 für AlOussama/TYNDP_Products als ein konsolidiertes Implementierungs- und Qualifikationsmakro aus. Verifiziere zuerst den technischen MA1-Code-Freeze 0254d867a34b66ec7b56c90225605d29ea328916 und Dokumentations-Commit 1089874c1cf4980fc8e6527297a6ed6123d7c709. Lies vollständig docs/current/IOSN_Modul2_Netzaggregation/80, 81, 82, 83, 84 und diesen Handoff 85. Verwende MA1-API tyndp_reduce.iosn_official.ma1.execute_ma1 und deren versionierte Referenz-/P/Gamma/Az-Artefakte. Entwickle zwei **inhaltlich getrennte** Worker W-EQ und W-ITER mit unabhängiger numerischer Revision R-NUM: globale positive Ersatzreaktanzen mit Gauge und strukturelles c0 inklusive affiner KVL im Zielmodell; länderquoten-konforme gekoppelte Kandidaten/Swaps über mehrere Länder, nach jedem Kandidaten vollständiger globaler Refit und RMSE-Accept/Rollback auf verschlossenen Splits. Führe Tests/Reparaturen/Re-Review durch, veröffentliche Branch/Commits/G05–G08-Witness/Entscheidungsledger und einen MA3-Handoff. M0/CGMES, M1/PECD, Wetterjahrauswahl, Legacy-Prototypen und die alternative MA1-Linie nicht ändern. Keine automatische Realnetzfreigabe ohne unabhängige Prüfer und reale Daten.

## 1. Normative Grundlage und niemals überschreibbare Grenzen

- Primärquelle ENTSO-E Identification of System Needs Methodology, **Konsultationsfassung 25.02.2026**, §3.8.1–3.8.4, Annex 6.1 S.45–51; eine exakte Veröffentlichung der proprietären Optimierung wird nicht unterstellt.
- Verbindliche lokale Nachweise: [MA1-Ausführung 82](82_M2_MA1_EXECUTION_REPORT_2026_11_04.md), [R-PHY-Status 83](83_M2_MA1_R_PHY_REVIEW_STATUS_2026_11_04.md), [R-CLU-Status 84](84_M2_MA1_R_CLU_REVIEW_STATUS_2026_11_04.md), [Gate-Ledger 86](86_M2_MA1_GATE_EVIDENCE_2026_11_04.json) und [18-Punkte-Methodik-Mapping](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md).
- Die vollständige Geografie bleibt aus **37 separaten Country-Labels, Quoten-Summe 102**; Northern Ireland und United Kingdom niemals stillschweigend zusammenlegen. Bei künstlichen kleineren Netzen **ausschließlich als SYNTHETIC_BUDGET** gekennzeichnete Testquoten.
- Die AC-Physik ist ein europaweit gekoppelter Graph, auch wenn echte elektrische AC-Islands getrennt bilanziert werden. Ländergrenzen sind **nur Clusterrestriktionen**, keine Lastfluss-Slacks. HVDC ist kein passiver AC-Zweig.
- MA1 wählt **keine** Wetterjahre, MA2 ebenso nicht. Die extern festgelegten fünf IDs und deren Snapshots bleiben unveränderlich und gehasht. Die fünf Projektjahre sind nicht als offizielle Zahl der ENTSO-E-Marktstudien-Szenarien zu beschriften.
- M2/MA2 erzeugt keine CGMES- oder PECD-Reader, editiert keine M0/M1-Dateien und ersetzt nicht die nachfolgende N-1-Vierfachkapazität aus MA3.

## 2. Unveränderlicher Eingangsvertrag und gefrorene MA1-Artefakte

Konsumiert werden:
1. DetailedGridSnapshot mit ACBranch/HVDCTerminals und Source-SHA; ReferenceDispatchSet inklusive sämtlicher expliziter Terminal- und PST-Schedules; TimeSet mit fünf Jahren und Dauer/Season; NormalContingencyRatings in MW; CountryZoneBudget; explizites Country-Label-Mapping.
2. MA1Result aus execute_ma1(...) mit **nur operationalem** ReferenceFlowCache (MW-Ströme im gemeinsamen AC-Detailgraphen), AnnualScreen und SeedResult, dessen Quoten/Connectedness/Gamma mit G01–G05 geprüft wurden. Seine input_manifest_sha256 ist Run-Anker. Der Referenzfluss darf nicht anlässlich einzelner Country-Kandidaten verändert oder über neue Jahresauswahl ersetzt werden.
3. Export aus ma1.py (15 manifestierte Dateien): global_reference_flows.npz, operator_P/Gamma/A_z/A_d.npz, busmap.csv, annual_criticality.csv, country_quotas.csv, zone_cuts.csv, preflight_ledger.json, gate_ledger.json, reference_flow_manifest.json, merge_ledger.json, counterflow_ledger.json, manifest.json.
4. **Separat** ein explizites neutrales Kalibrierungs-ReferenceDispatchSet mit HVDC-Setpoints null/PST neutral, dessen AC-Inseln trotzdem physikalisch bilanziert sind. Keinesfalls active dispatch einfach auf Null schalten und fehlende MW-Slacks verstecken; bei fehlendem qualifizierten neutralen Dispatch BLOCKED_DATA.

Alle Inputhashes und Split-Zuordnungen sind vor L2/L3 zu frieren; verändert sich ein Byte, beginnt eine neue Version, niemals derselbe Output-Run-ID.

## 3. W-EQ – positiver globaler x/c0-Fit und affine KVL

Implementiere vorzugsweise unter src/tyndp_reduce/iosn_official/equivalent_network.py und ergänzenden numerischen Helfern:

**Physischer Vertrag:**
- Für jeden zulässigen vollständigen Busmap-Kandidaten aus dem ORIGINAL Detailnetz P(z), Gamma(z), A_z(z) und p_z=P p_detail, f_target=Gamma f_detail **auf derselben pan-europäischen Referenzstundentabelle** neu bilden.
- Reduced DC: f_eq(t)=H_eq(x) p_z(t)+c0, mit allen x_e>0, mindestens einer dokumentierten Skaleneichung je tatsächlich zusammenhängendem AC-Zonennetz, und **A_z c0=0**.
- Im tatsächlich verwendeten reduzierten Netz muss die affine Maschenbedingung gelten: C^T diag(x)(f_eq(t)-c0)=0, wobei C die unabhängige Maschenbasis bezeichnet. Nicht c0 als reines nachgelagertes Plot-Offset akzeptieren; niemals unqualifiziert die homogene KVL auf den korrigierten Gesamtfluss anwenden.
- Ein Baumgraph besitzt keine frei identifizierbaren x-Werte aus KCL-Flüssen. Rang-/Konditions-/Loop-Anregungscheck vor jedem Fit, andernfalls UNIDENTIFIABLE statt erfundener Parameterqualität.
- Globaler Sparse-Solver, keine dichte europäische Inverse. Getrennte Winkel-Referenz pro tatsächlicher AC-Insel, **keine** pro-Country-Leistungsausgleichsvariable.
- Trainingsstunden, Gewichtung, Regularisierung, Solver, Bounds, Startwerte, Gauge und numerische Toleranzen explizit als **I-Entscheidungen** ausweisen. Literatur-/Source-Belege pro Entscheidung. Der ENTSO-E-Originalsolver ist nicht veröffentlicht.
- Solver-Exception, Nicht-Konvergenz, neg. x, singularer Loop-Block oder identifikationsbedingt beliebige x sind **FAIL/GATE_FAIL**, kein Return eines „plausiblen“ Netzes.

**W-EQ-Tests:** 3-Bus-Dreieck exakt mit c0=0, positives x; Loops mit nichtzero bilanzneutralem c0, unabhängige affine-Mesh-Replay-Instanz; mehrere AC-Islands; ungeeigneter Baum und rangschwacher Fall (fail-closed); PST/HVDC-neutral vs operational getrennt; bei absoluter x-Skalenmultiplikation demonstrierte Gauge-Notwendigkeit; unabhängiger Sparse-/Dense-Vergleich auf kleinen Netzen.

## 4. W-ITER – verschachtelter grenzrein gekoppelter Suchprozess

Implementiere vorzugsweise unter src/tyndp_reduce/iosn_official/iterate.py, evaluate.py:

- Starte mit einer **nachgewiesen gültigen** MA1-Busmap; erzeuge Single-Boundary-Moves, balancierte Swaps und gebündelte Moves in **mehreren elektrisch gekoppelten Ländern** gleichzeitig. Alle Zonen bleiben ausschließlich innerhalb ihres Country-Labels; **k_c ist hart und darf sich nie ändern**.
- Vor jedem teuren Fit strikt Country-Purity, vollständige Originalknotenzuordnung, AC-Connectedness jeder Zone, AC-Island-Semantik, kritische geschützte Zweige und Daten-/Ratingverfügbarkeit prüfen. Rejected Moves ins unveränderliche Candidate-Ledger aufnehmen.
- **Pro Kandidat** P/Gamma/A_z, gesamte europäische Schnittliste und Ziel-MW-Flüsse neu berechnen und **W-EQ auf dem gesamten europäischen reduzierten Netz erneut ausführen**, nicht nur auf dem Land des Moves.
- Auf einem eingefrorenen **Train/Selection/Holdout**-Split mit fünf festen Jahren operieren: Fit ausschließlich TRAIN, Accept/Rollback ausschließlich SELECTION, HOLDOUT bis abschließendem unabhängigen Replay verschlossen. Der genaue Blocksplit ist I; die Jahre werden nicht erneut ausgewählt.
- Per Link MW-RMSE, globale Norm, MAE, P95/P99, Vorzeichen-/Gegenflussdiag, kritische Branch-Capture und Land-/Grenzfairness loggen. Wenn Linkmenge mit der Busmap wechselt, sind einfach gemittelte Link-RMSE nicht unmittelbar vergleichbar: vorab feste Monitorgruppen, kritische Leitungsabdeckung, Linkzahl, Referenzmonitor-Vektor und eindeutiger Tie-Breaker.
- Nur echte, auf exakt demselben frozen SELECTION-Split gemessene Verbesserung übernehmen; sonst Rollback. Detaillierte Entscheidung und alle Solverresiduen in candidate_ledger.csv/json. Deterministische Seeds, Max-Runden, Plateau-Abbruch und tolerierte Verbesserung als **I**, keine erfundene „offizielle“ Formel.
- Bei stabilem Plateau Handoff an MA3 für N-1-Vierfachkapazitäten; MA2 selbst darf aus Proxykapazitäten keine REAL_QUALIFIED-Entscheidung ableiten. Eine spätere Kapazitätsbeanstandung erfordert gezieltes Feedback zu L3, nicht unsichtbare Revision der Landesbudgets.

**W-ITER-Tests:** drei gekoppelte Länder mit AC-Grenzties, deterministische 2- und 3-Land-Moves, identische Quoten vor/nach; mindestens ein nachweislich akzeptierter und ein verworfener Kandidat; manipulierte Train/Select/Holdout-Splits lösen Fail aus; nach Kandidat stets europäischer Refit, immutable reference checksum identisch; geänderte Zonepaarliste/Linkzahl erzeugt methodische Vergleichsflag; bad/unterbudgeted/mixed/abgetrennte Zonen scheitern *vor* Fit.

## 5. Unabhängiger numerischer Reviewer R-NUM

R-NUM darf weder von W-EQ noch von W-ITER als implementierender Agent übernommen werden. Ein anderer Prüfer erhält **einen eingefrorenen SHA** mit sämtlichen Source- und Gate-Protokollen, rechnet neu nach und veröffentlicht Findings P0/P1/P2 mit konkretem Repro sowie Re-Review der Reparatur-Commits. Ohne einen **tatsächlich getrennten** Prüfer und nachweisbare Runs gilt der Status INDEPENDENT_REVIEW_PENDING. CI-Grün ersetzt R-NUM nicht.

Explizite Reviewer-Fragen: ist c0 gleichzeitig bilanzneutral UND als affine KVL tatsächlich im reduzierten Simulator repräsentiert? Werden Referenzstunden, Jahre, Ranges und Ländergrenzen durch Kandidatenbewegungen unverändert behalten? Sind x identifizierbar? Wird jeder Candidate global neu gefittet und verworfen, wenn seine Auswahlmetrik nicht verbessert ist? Stimmen KCL/KVL/Direct Dense bei kleinen Testfällen? Welche echte Realquelle belegt europaweite Parameterqualität?

## 6. Verbindliche MA2-Gates, Iteration und Publikation

| Gate | Muss-Bedingung / Output | Entscheidung |
|---|---|---|
| G05 | P/Gamma/A_z und Land/Island invariants pro Kandidat | PASS / FAIL |
| G06 | x>0, richtige Gauge, Rang, A_z c0=0, affine KVL im Zielnetz | PASS_SYNTHETIC / FAIL |
| G07 | Invarianten vor dem Fit, kompletter globaler Refit pro Candidate, 3 Splits, Ledger, Accept/Rollback und Plateau | PASS_SYNTHETIC / FAIL |
| G08 | Vergleichbarkeit nach topology changes, identische selection hours, RMSE und Link-/Country-Fairness, verschlossener Holdout | PASS_SYNTHETIC / UNQUALIFIED |
| R-NUM | Unabhängiger Reviewer mit neuem Run/Re-Review | INDEPENDENT_REVIEW_PENDING bis belegter Re-Run |
| Real | Vollständige offizielle Referenzstunden, 37-Länder-Country-Map, echte Limit-/Device-Inputs | BLOCKED_DATA bis vorhanden |

**Publikationspfad:** neuer Modul2-Work-Branch + Worker-Branches + PR (Draft bis unabhängige Reviews); src/tyndp_reduce/iosn_official/equivalent_network.py, iterate.py, evaluate.py; tests/iosn_official/test_ma2_*.py; results/iosn_official/<versionierter_run>/fit.json, equivalent_network.json, rmse_per_link.csv, candidate_ledger.csv, input_split_manifest.json, exception_ledger.json, holdout_report.json, independent_review.md; docs/current/IOSN_Modul2_Netzaggregation/87_M2_MA2_EXECUTION_REPORT.md und MA3-Handoff.

**Schlussentscheidungen:** "SYNTHETIC_TESTS_PASS" ist zulässig bei belegtem numerischem CI; "SYNTHETIC_QUALIFIED" erst nach den fälligen unabhängigen MA1-/MA2-Reviews; "REAL_QUALIFIED" nur nach G12, vollständiger externer Referenzprovenienz und unabhängiger Realnetz-Numeric-Qualifikation. **Keine automatische runtime/multimodul/methodische Freigabe.**

## 7. Integrationskonflikt nicht verdecken

Neben dieser Linie ist der eigenständige Branch restructure/iosn-m2-ma1-integration-20261103 @ 88374dd38792146ca55fa3fe2d4b35dac842c0b9 mit alternativer API tyndp_reduce.m2 vorhanden. Er ist ein **separates nicht gemergtes Implementierungsergebnis**, nicht stillschweigend mit tyndp_reduce.iosn_official kompatibel. MA2 wendet sich **an genau diese dokumentierte iosn_official-Linie**; soll der andere Branch kanonisch werden, ist vorher eine ausdrücklich versionierte Contract-Reconciliation durch den Owner erforderlich. Die parallele Alternative wird weder gelöscht noch ohne Freigabe überschrieben.
