# MAKRO-AUFTRAG ML-C10
## Native Scientific Micro-Models, Generated Equations & E04/E05 Witness Verification

### 1. Rolle
Agiere als Expertenteam aus Optimisation/LP Verification Expert, Sector-Coupled Model Developer, Generated-Model Inspection Engineer, Mathematical Equivalence Specialist, Adversarial Benchmark Reviewer und Reproducibility Engineer.

### 2. Ziel
Überschreite die bisherige Ebene synthetischer Ergebnisarithmetik: **erzeuge und löse tatsächlich kleine, vollständig synthetische LP-/DC-/Sektorkopplungsmodelle**, exportiere ihre **E04 Variablen, Nebenbedingungen und Koeffizienten** und überprüfe auf entsprechend kleinen Fällen E05-Zeugen mit unabhängig rekonstruierten Residuen und Zielfunktionswerten. Keinen vollständigen IoSN-Solver implementieren.

### 3. Forschungsinputs
ML-C08 integrated_mathematical_obligations.md, verification_and_evidence_reference.md; ML-C04 B01–B15, 26 katalogisierte Mutationen und dokumentierter korrigierter B05-LODF-Fall; ML-C05 Conformance- und Äquivalenzsemantik. Bei offenen Methodikparametern **konkurrierende illustrative Varianten** mit klarer Fallidentität statt scheinbar verbindlicher Formeln.

### 4. Untersuchung
1. Modellfamilien M01 (ein x über CY mit unterschiedlichen, über 2035/2040/2050 identischen synthetischen Gewichtswerten), M02/03 (dimensionsrichtige Kosten), M04/M05 (KCL/KVL), M07 (NTC-Marktlinks), M08 (P10/P11 Stufen), M13 (Speicher), M15 (H2) und M18 (optional OPF/Frozen H2) als kleine unabhängige Modellexperimente.
2. Exportiere pro tatsächlich erzeugtem Modell Zeilen-/Spaltenregister, quantifizierte Indizes, Units, Koeffizienten, Affin-Offsets, Bounds, Stage- und CY-Bindung, Zielfunktionskomponenten und Eingabehash.
3. Führe einen tatsächlich verfügbaren kleinen LP-Solver **nur als Forschungswerkzeug** aus; reproduziere Zielfunktionswert und Primalresiduen unabhängig vom Solver. Fehlen Dual-/Optimalitätszertifikate, beschränke die Behauptung auf wirklich geprüfte Eigenschaften.
4. Injiziere möglichst die 26 C04-Mutationen in **erzeugte Modellgleichungen** und zeige gezielte, testbare Fehlerdetektion; genau angeben, wie viele tatsächlich ausgeführt werden.
5. Untersuche E-FEAS, E-OPT-SET/-VALUE und E-OBS mit echten Kleinstmodellen und mehreren Optima. Gleiche Outputzahlen sind kein Feasible-Set-Beweis.
6. Behandle F_y-Stufenübergabe, Discount/VoLL/H2-Parameter als Owner-TBD. Nur klar gekennzeichnete illustrative Alternativen testen, kein Default für IoSN.

### 5. Liefergegenstände
Im Ordner .../ML_C10_native_mathematical_micro_models/:
- native_math_experiment_protocol.md
- small_models/ mit Quellcode, Fixtures und Reproduktionsbefehlen
- generated_equation_inventory.csv
- e04_constraint_witnesses/ und e05_solution_witnesses/
- mutation_execution_matrix.csv
- feasible_set_and_multi_optima_review.md
- actual_execution_report.md
- adversarial_mathematical_review.md
- handoff_to_conformance_runner.md

### 6. Forschungsabnahme
Mindestens ein **nachweisbar ausgeführtes** synthetisches Modell je kritischer modellierbarer Pflichtklasse mit Rohzeilenexport; pro getesteter Eigenschaft Positiv-/Negativkontrolle und dokumentierter Ausführung. Unerfüllbare Klassen/TBD sind explizit zu begrenzen, kein pauschaler „48 SR PASS“. Tool-/Solverwahl ist ausschließlich experimentell; kein produktives Modell, keine akzeptierten realen Toleranzen.

**Welle 1: sofort unabhängig startbar.**

### Gemeinsame wissenschaftliche und Governance-Grenzen
- D1: 48 aktive vorläufige MA01-SR, keine erfundenen SR-012/049; P00–P17 vollständig.
- D2: extern ausgewählte CY1–CY5; für jede CY-ID ist das symbolische Gewicht in 2035/2040/2050 identisch, aber nicht zwangsläufig zwischen CYs gleich; Zahlenwerte TBD; keine Wetterjahrselektion.
- D3: Fail-Closed für anwendbare Pflichtnachweise; BLOCKED, UNSUPPORTED, NOT_EXECUTED und NOT_APPLICABLE nicht vermischen.
- D4: kanonische UTC-Intervalle und Einheitendimensionen, offene Kalender-/DST-/Leap-Toleranzen TBD. project_decision:D4 ist nicht test_depth:D4.
- D5-A1: risikobasierte Verifikation, keine generelle Gleichheit der Algebra; D6-A: ein gemeinsamer wissenschaftlicher Contract, unabhängig entwickelte Implementierungen.
- O26 bleibt als konsultierter 2026-Methodikstand gekennzeichnet; offizielle Adoption und Originalbytes nicht nachgewiesen. H24 und CBA4 nur in dokumentiertem Quellenrang.
- Keine neuen allgemeinen Robustheitsanforderungen, kein vollständiges IoSN-Produktivmodell, keine normative DSL-/Architektur-/Solverwahl, keine echte Originaldatenfreigabe, keine automatische SR- oder MD/CL-Änderung.
- Trenne synthetische Testresultate, echte Modell-/Generatorzeugnisse, fachlich akzeptierte Orakel und personell unabhängigen Audit. 21 MD/CL bleiben offen und G1 bleibt BLOCKED.

### Repository- und Review-Protokoll
Repository: AlOussama/TYNDP_Products. Gemeinsamer Ausgangsstand: ML-C08, Draft-PR #51, Commit 8470add62fcbc7f39b1d90c0d5afdcee50ab811e. ML-C01 bis ML-C07 sind separat gepinnte Forschungsinputs gemäß ML-C08; verifiziere beim Start ihre tatsächlichen Head-SHAs. Jede Arbeit erstellt ihren eigenen Forschungsbranch **vom ML-C08-Commit**, ändert ausschließlich den eigenen Workstream-Ordner und öffnet einen separaten Draft-PR gegen den ML-C08-Forschungsbranch. Keine Merge-/Ready-/Freigabeaktion. Ein KI-interner adversarieller Review darf nicht als personell unabhängiger Audit erscheinen.

Status am Ende muss getrennt ausweisen: Struktur, synthetische Tests (mit tatsächlichem Ausführungsnachweis), native Mathematik falls ausgeführt, externe Quelldaten, Owner-Orakel, unabhängige Review und Gate. Fehlende Evidenz bleibt offen.
