# ML-C06 — Architecture Comparison Framework

**Nichtnormative Forschung, Stand 2026-11-12. Kein Architekturentscheid, keine offizielle IoSN-Contract-Sprache. G1=BLOCKED.**

## 1. Identität und reproduzierbarer Versuchsraum

|Quelle|PIN / Status|Verwendung|
|---|---|---|
|ML-R00 PR #32|`9162def25d22c37b1fbc38f7d80fe929425cc8d2`|Gemeinsamer Baseline-Commit und PR-Ziel|
|ML-R02 PR #27|`16d58381bfc6d7ded9f0eb5004699ce718f037f7`|A/B-Prototypen und Standardsvergleich, **nicht** als bestätigte Architektur|
|ML-C02 PR #42|`136b35e9dc2206b38c95b1e9a68b7d9598a5f86c`|Logisches Metamodell und versionierter 528-NODE/1323-EDGE-Graph|
|ML-C04 PR #45|`256541e763147dcb118a3a9d24ca2f52035c672e`|Die identischen 15 Fälle B01–B15, synthetische Referenzorakel|

`frozen_sources/c02_traceability_model.csv` ist **byteidentisch** mit Git-Blob `d10e19103aa44bcaac6df692ee3b7dbb64fd77c3`; `frozen_sources/c04_cases.json` ist **byteidentisch** mit `3ce73355e7c5ad228cbe29db045223ca1adea571`. Es werden keine fremden Research-PRs geändert. Originale 12 CSV-Spalten (einschließlich Herkunft und Lifecycle) bleiben bei der Hin-/Rückabbildung erhalten. Forschungsentscheid D1–D6 und 20 Owner-TBD werden **nicht** als Freigabe interpretiert.

## 2. Architekturdefinitionen ohne Strohmann

- **A, Registry/Profiles:** zentrale ID-Registry; getrennte Requirements-, Input-, Process-, Math-, Output-, Verification- und Governance-Scopes; referenzielle Cross-Profile-Prüfung; mindestens sieben versionierte fachliche Verträge. Der Output-Scope darf in der C02-Grafik ohne vorgetäuschte zusätzliche Nodes bleiben.
- **B, Typed Meta:** ein integrierter typisierter Contract-AST (hier absichtlich JavaScript-Objekte); gemeinsame Identitäten, Variablen/Relationen und expliziter Anwendungsbereich. Keine Behauptung, dass das bereits SysML v2 ist.
- **C, Federation:** getrennte konzeptionelle Fach-Views und ein kanonisches Identitätsledger als einzige semantische Referenz. Verlustfreie Rückführung ist testbare Bedingung, aber kein Anspruch auf tatsächlich parsbare ReqIF-/SysML-/SHACL-/GEMS-Dateien.

Für **jede** Variante ist derselbe Graph, derselbe semantische Zustand, dieselbe B01–B15-C04-Fixture-Version und dieselbe Mutationsliste maßgeblich. Ein Common-Oracle-Kernel minimiert Bewertungsbias, macht die synthetischen Orakelergebnisse aber **nicht unabhängig**.

## 3. Vergleichskriterien (keine frei erfundenen Gewichte)

|ID|Kriterium|Prüfobservable|
|---|---|---|
|C01|Requirements traceability|canonical MA01-SR source test and block references|
|C02|Types and formal semantics|typed index role obligation and forbidden-state predicates|
|C03|Time spatial carrier scenario axes|UTC and Δt with independent year/CY/scenario/carrier units|
|C04|Mathematical expression power|nonanticipativity DC mesh market NTC storage objective and E-FEAS claims|
|C05|Preprocessing transformations|typed producer consumer preservation laws and execution lineage|
|C06|Conditional process variants|P12 eligibility P15 optionality stage and LF/OPF guard|
|C07|Data and output provenance|immutable releases instance hashes KPI formula and raw-derived split|
|C08|Scientific verification|native generated rows numeric oracle V1–V6 and actual Evidence|
|C09|Extensibility|versioned IoSN domain-specific operator or profile customization|
|C10|Semantic migration|incompatible revision detection mapping and change impact|
|C11|Standard interoperability|independently tested standard parser and loss accounting|
|C12|Complexity maintenance|governance responsibilities adapter code and operational costs|

Bewertung pro Kriterium: **OBSERVED_CUSTOM** nur bei tatsächlich ausgeführtem eigenem Prüfer; **REPRESENTABLE_PARTIAL** bei explizit darstellbaren, aber unbewiesenen Domänenkonstrukten; **DOCUMENTED_STANDARD** nur bei nachvollziehbarer öffentlicher Dokumentation; **NOT_TESTED** ohne nativen Parser/Modelllauf; **BLOCKED_OWNER** bei fehlender Autorität, echten Daten oder numerischen Orakeln. Diese Kategorien sind **nicht additiv**, und es gibt keinen Gesamtscore, der mathematische Fehler durch Software-Wartbarkeit kompensieren könnte.

## 4. Testdesign, Tiefe und Ergebnissemantik

Der ausführbare `run_experiments.mjs` reproduziert mit Node >=18 und ohne Abhängigkeiten pro Architektur **45** Klassifikationen: eine vollständige Struktur-/Round-trip-Prüfung, eine Profilsemantik-Prüfung, 15 positive synthetische C04-Arithmetikprüfungen, 15 kontrollierte Fixture-Mutationen, 12 semantische Mutationen und einen erzwungenen Verlust eines Lifecycle-Feldes. `node run_experiments.mjs` prüft Ergebnisdrift; `node run_experiments.mjs --write` schreibt nach expliziter Neuprüfung die CSV.

**Abgrenzung der Teststärken:** (i) D0/D1 Struktur, IDs, Typen, Status; (ii) D2 synthetisches numerisches Oracle; (iii) D3 generierte native LP-Variablen/Gleichungen/Beschränkungen **NOT_TESTED**; (iv) D4 vollständiger äquivalenter Lösungsraum **NOT_TESTED**; (v) native Solver/Tool-/Daten-/Provenienz-/Review-Beweise **NOT_TESTED/BLOCKED**. Fehlende Quellenreleases, reale CY-Gewichte, P06-Kalibrierung, Stage-MD-07 und KPIs werden nicht synthetisch freigegeben.

Die 48 MA01-SR, P00–P17 (einschließlich P00 ohne SR), 18 M, 20 LR, 87 B01-D mit 20 process-only, 38 Transformationen und 48 R04-Tests müssen vollständig erhalten bleiben. Die 48 R04-native-Test-Status bleiben `NOT_EXECUTED`. Bei C02-Quellkonflikt O26/D2 wird keine semantische Autorität „aus Syntax“ abgeleitet. Alle sechs Ergebnisstatus PASS/FAIL/BLOCKED/UNSUPPORTED/NOT_EXECUTED/NOT_APPLICABLE bleiben unterscheidbar; `PASS` wird in diesem Experiment nicht für Toolkonformität vergeben.

## 5. Abbruchbedingungen und spätere Falsifikation

Ein Ansatz ist für den **wissenschaftlichen Contract** disqualifiziert, wenn er nach Anwendung seiner zulässigen semantischen Erweiterungen SourceClause-Status, verlässliche IDs, ungleiche symbolische CY-Gewichte über Y, gemeinsame Investmententscheidung, MW×h, KCL/KVL-Branches versus NTC-Links, P12/P15, Daten-/Transformationsprovenienz, unbelegte KPI-Definitionen oder sechs Teststatus nicht ausdrücken kann. Ein testweise auftretender Loss wird nicht als Produktivversagen gewertet, wenn die Architektur über **nachweislich kontrollierte** semantische Extension schließbar ist. Für endgültige Architektur-Eignung bleiben Parser, echte Operatoren, robuste Versionstupel, native Generatorwitnesses und zwei unabhängig implementierte Modelle erforderlich.

**Forschungseinordnung:** Alle Implementierungen sind minimale, projektspezifische Mockups, bewusst keiner Sprache untergeordnet. Keine gemeinsame Model-to-Model-Translation und kein identischer Solver-Quellcode vorgeschrieben.
