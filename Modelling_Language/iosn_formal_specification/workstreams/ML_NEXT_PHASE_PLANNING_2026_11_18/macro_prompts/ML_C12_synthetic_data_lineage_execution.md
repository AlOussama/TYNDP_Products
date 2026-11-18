# MAKRO-AUFTRAG ML-C12
## Executable Synthetic Data, Transformation, Process-Control & Output Lineage Research

### 1. Rolle
Agiere als Expertenteam aus Energy Data/ETL Architect, Process-Modelling Expert, Temporal/Spatial Data Engineer, Data Governance/Provenance Expert, Sectors-Coupled Input Architect und Adversarial Data Quality Reviewer.

### 2. Ziel
Demonstriere in einem **synthetischen, tatsächlich ausgeführten** Forschungs-Labor, wie IoSN-Daten von Quellen über P00–P17-Teiltransformationen bis zu Modellinput, RawResult, abgeleiteten Kennzahlen und SystemNeed typisiert und mit wirklicher Lineage geführt werden können. **Keine reale PECD-/PEMMDB-/H2-Dateiqualifizierung.**

### 3. Forschungsinputs
ML-C08 integrated_data_process_output_contracts.md, end_to_end_requirements_traceability.csv, C03 204-Row Trace-Matrix, 108-Row-Ausnahmeregister, 38 TransformationSpec und 47 direkter T-DAG-Kanten, acht explizite Kontroll-/Graphlücken, C05 E01–E08. B01-D072 und B01-D081 sind **nicht** freigegebene Quellen oder Ergebnisse.

### 4. Untersuchung
1. Definiere synthetische SourceArtifact-Bytes mit **wirklich berechneten SHA-256 der synthetischen Dateien**, Quelle/Fixture-Kennzeichnung, Dateninstanz und Transformationsausführung. Ein Git-SHA ist kein realer SourceData-SHA.
2. Implementiere repräsentative, klar markierte Teilketten: P00/P02/P03 Wetter-/UTC-Manifest, P04–P07 Netzzonen/Reaggregation, P08 Modellinput, P13/P14 pre-expansive H2-Identität, P16 Raw→Metric→SystemNeed, P17 EvidenceRequest/ActualEvidence. Alle 87 B01-D-Definitionen und 20 process-only bleiben im Katalog referenziert, auch wenn nicht für alle reale Transformationen ausgeführt werden.
3. Trenne R01-Konzeptprozess, **38 Spec-/47 Data-DAG** und Governance-/Owner-Kontrollgraph. Reproduziere und klassifiziere die acht C03-Kontrollkantenlücken als OpenEdge/Guard, niemals frei als produktive Kante ergänzen.
4. Belege UTC-Intervall- und Δt-Energieerhaltung, DST-/Leap-Ambiguität als NegativeCase; source↔model räumliche Zuordnung, dimensional H2 Basis, nonuniform CY-Gewichtsvektor mit gleicher Fallidentität über Y.
5. Demonstriere B01-D072 als **separat erstelltes, synthetisches präexpansives Referenzlaufartefakt**, nicht aus P12 rekonstruiert; fehlende echte Quelle bleibt BLOCKED.
6. B01-D081: Unbekannte KPI-Formel/Filterschwelle erzeugt METRIC_UNDEFINED, nicht Null. Führe optionale **explizit illustrative** KPI-Formeln ausschließlich für Testmutationen aus.
7. Erfasse Fehlerfälle: dangling FK, fehlender Originalhash, unqualifizierter Release, fehlende Quellzeit, doppelte Einheit, falscher Carrier, stale Output, ausgelassener optionaler OPF-Guard.

### 5. Liefergegenstände
Im Ordner .../ML_C12_synthetic_data_lineage_execution/:
- synthetic_data_and_transform_contract.md
- synthetic_fixtures/ und executable_transformations/
- typed_process_control_dag.md
- actual_instance_lineage.csv
- provenance_hash_and_replay_results.json
- undefined_metric_and_h2_preexpansion_cases.md
- cross_layer_gap_disposition.csv
- executed_data_quality_mutations.md
- independent_data_lineage_review.md
- handoff_to_evidence_engine.md

### 6. Abnahme
Reproduzierbare tatsächliche Teilketten und Negativtests, korrekt getrennte Originaltypen/Instanzen/ausgeführte Transformationen. Zeit-/Energieinvarianten werden nur bei geeigneten Größen behauptet. **87/87 Definitionen** abgebildet, aber „87/87 reale Originaldaten validiert“ ausdrücklich nicht behauptet. Nicht benannte Ownerparameter bleiben TBD.

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
