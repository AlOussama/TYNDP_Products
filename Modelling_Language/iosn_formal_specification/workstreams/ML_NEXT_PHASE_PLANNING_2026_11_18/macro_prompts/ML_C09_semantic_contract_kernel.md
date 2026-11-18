# MAKRO-AUFTRAG ML-C09
## Executable Scientific Contract Semantics & Traceability Kernel

### 1. Rolle
Agiere als Expertenteam aus Formal Semantics/Requirements Architect, MBSE-Metamodellierer, Energy System Domain Expert, Data/Provenance Architect, Formal Verification Engineer und kritischem unabhängigen Prüfrollenträger.

### 2. Ziel
Untersuche mit einem **ausführbaren, toolneutralen Forschungsprototyp**, ob die in ML-C01, ML-C02, ML-C05 und ML-C08 vereinbarten fachlichen Identitäten, Typbeziehungen, Gültigkeitsregeln, Statusachsen und Traceability-Invarianten maschinell prüfbar sind. Kein neues L2-SR-System und keine verbindliche DSL entwickeln.

### 3. Relevante Ausgangsevidenz
ML-C08: canonical_contract_semantics.md, end_to_end_requirements_traceability.csv, cross_workstream_findings_register.csv und integration_validation_report.md. ML-C01: source/decision/status ontology; ML-C02: 528 NODE / 1323 EDGE graph; ML-C03: 87 Datenobjekte, 20 process-only, 38 T, acht offene Kontrollabhängigkeiten; ML-C05: scoped sechs Teststatus und EvidenceRequest vs Evidence.

### 4. Untersuchung
1. Definiere einen minimalen semantischen Kern mit **SourceClause, Requirement, P00–P17, DataDefinition/Instance, TransformationSpec/Execution, MathematicalObligation, EvidenceRequest/ActualEvidence, Condition, Oracle und ReviewDecision**; typisiere Beziehungen und Kardinalitäten.
2. Implementiere nur eine **Forschungs-Validierungsfunktion** für alle 48 SR, 18 P, 87 B01-D, 20 prozessgebundene Objekte, 38 Transformationen und 48 Testreferenzen. 528/1323 ist eine Regressionskontrolle, keine Pflicht zu identischer interner Datenstruktur.
3. Unterscheide Quellautorität, Forschungsstatus, Datengüte, semantische Gültigkeit, Math-/Numerikprüfung, Teststatus, personelle Unabhängigkeit und Gate. Beweise mit Mutationen, dass ein synthetischer PASS nie eine Freigabe auslöst.
4. Implementiere die dreiwertige P15-Guard-Logik (TRUE/FALSE/UNKNOWN) und kontrolliere Voraussetzung, Toolfähigkeit und Begründung von NOT_APPLICABLE.
5. Prüfe D2/D4/UTC/CY-Kollisionen, physikalische Branch vs MarketLink, SystemNeed vs ApprovedProject, Verlust von P00 und process-only B01-D, fehlende Quelltypen, stale evidence nach Profilwechsel.
6. Analysiere Ausdrucksfähigkeit vs. mathematische Korrektheit ausdrücklich getrennt. Kein Symbolgraph-Validator darf als Generator-/Solverbeweis gelten.

### 5. Liefergegenstände
Im Ordner Modelling_Language/iosn_formal_specification/workstreams/ML_C09_semantic_contract_kernel/:
- scientific_semantic_kernel.md
- typed_relations_and_invariants.md
- scope_and_applicability_semantics.md
- executable_traceability_checks/ (reproduzierbare Miniimplementierung mit Negativbeispielen)
- identity_and_status_mutation_catalogue.csv
- machine_check_results.json (ausgeführte Tests von bloßen Plänen getrennt)
- completeness_and_limitations_review.md
- handoff_to_native_model_and_conformance.md

### 6. Abnahme innerhalb der Forschung
48/48 SR, 18/18 P, 87/87 B01-D, 20 process-only, 38 T und P15-Guard mit referenziellen Negative-Tests nachprüfbar. Jede geprüfte Invariante hat ID, Quellbezug, begrenzten Scope und tatsächlich ausgeführte oder NOT_EXECUTED Testevidenz. Fehlende Owner-Parameter bleiben TBD; keine Aussage, dass M01–M18 numerisch korrekt implementiert wurden.

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
