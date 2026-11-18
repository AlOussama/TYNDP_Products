# MAKRO-AUFTRAG ML-C14
## Executable Evidence Ledger, Scoped Conformance Engine & Mutation Detection Research

### 1. Rolle
Agiere als V&V Architect, Formal Conformance Expert, Independent Test-oracle Engineer, Data Provenance Architect, Energy Optimization Verification Specialist und adversarial Evidence Reviewer.

### 2. Ziel
Erstelle einen tatsächlich ausführbaren **Forschungsprototyp eines Conformance- und Evidenzprüfers** für die sechs atomaren Teststatus und die voneinander unabhängigen V1–V6-, D0–D4- und E01–E08-Ebenen. Reale wissenschaftliche Konformität und G1 bleiben gesperrt. Der Prüfer muss mit erhaltener Quellenautorität unterscheiden, welche Aussagen **bereits getestet** und welche nur geplant sind.

### 3. Fachliche Voraussetzungen
ML-C08 verification_and_evidence_reference.md, C05 Conformance/Event-Status, C07 future pilot protocol, C04 26 Mutanten. **Abhängigkeiten:** Verwende die versionierten, tatsächlich vorliegenden Forschungsoutputs von ML-C09 (semantische Guards/Trace), ML-C10 (E04/E05 synthetische Modellzeugen) und ML-C12 (E01–E03/E06–E08 synthetische Lineage) nach deren Fertigstellung. Diese Inputs sind nicht Owner-approved und dürfen nicht stillschweigend als echte Daten freigegeben werden.

### 4. Untersuchung
1. Definiere die sechs atomaren Ergebnisse PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_EXECUTED, NOT_APPLICABLE plus getrennte EvidenceClass, SourceAuthority, InputQualification, IndependentReview und G1-Felder.
2. Implementiere Condition TRUE/FALSE/UNKNOWN und P15/SR-026: OFF nur mit konkretem Nichtaufrufbeleg ⇒ N/A; UNKNOWN ⇒ BLOCKED; ON ⇒ LF-Portfolio-Cap und E04/E05 verlangt; verpflichtende LF-Tests bleiben erhalten.
3. Verwende EvidenceRequest als Planungsobjekt und actual Evidence mit UUID/Digest/Run/Oracle/Scope als getrennte Objekte; keine automatische Erstellung tatsächlicher Zeugnisse aus Absichtserklärungen.
4. Entwickle E01–E08-Manifest- und Beweisprüfer für Source/Hash-Zustände, Original- vs. SYNTHETIC-BYTES, UTC/Units, transformierte Daten, generierte Rows, Solver-Residuen, Rohresultat/Metric und qualifizierte Review-Identität.
5. Führe gezielte Negativfälle aus: erfundener Hash, veraltete Evidenz nach Versionwechsel, Missing Mandatory, UNSUPPORTED fälschlich N/A, gleiche Solverwerte bei falscher KVL, fehlendes E04, KPI ohne gültige Formel, fehlendes unabhängiges Review.
6. Wenn ML-C10 tatsächliche Mutanten bereitstellt, prüfe konkrete D3-Fehlerdetektion. Die 26 C04-Designs sind nicht 26 ausgeführte Tests, solange Code- und Log-Evidenz fehlen.
7. Implementiere **scoped claims**, keine pauschale Zertifizierung; alle ungetesteten MA01-SR-Ebenen bleiben NOT_EXECUTED/ BLOCKED.

### 5. Liefergegenstände
Im Ordner .../ML_C14_executable_conformance_engine/:
- conformance_state_and_evidence_spec.md
- executable_evidence_verifier/
- source_and_fixture_scope_cases/
- status_and_optional_guard_mutation_tests.md
- actually_executed_checks.csv
- 48_sr_coverage_and_claims.csv
- evidence_integrity_and_staleness_review.md
- independent_assurance_critique.md
- handoff_to_synthetic_cross_implementation.md

### 6. Abnahme
Mindestens 30 explizite Status-/Evidenztests werden nachweislich ausgeführt, einschließlich aller sechs Status und E01–E08-Anwendungsfälle oder klar begründeter Nichtanwendbarkeit. Ein PASS eines synthetischen Validators darf nie eine reale Tool-/Methodik-/Owner-/Gatefreigabe auslösen. Keine Zahl der tatsächlich geprüften **native mathematical** SR darf größer ausgewiesen werden als belegte E04/E05-Zeugen.

**Welle 2: Start nach ML-C09, ML-C10 und ML-C12; unabhängig von ML-C13.**

### Gemeinsame Quellen-, Scope- und Governance-Bedingungen
- D1: Einzige aktive vorläufige Baseline sind 48 unveränderte MA01-SR ohne SR-012/SR-049; P00–P17 bleiben 18 fachliche Schritte.
- D2: Fünf extern gewählte CY1–CY5; identischer CY-indizierter symbolischer Gewichtsvektor über 2035,2040,2050, aber nicht notwendig gleiche Gewichte zwischen CY. Reale Zahlen und Originale TBD. Keine Wetterjahrselektion.
- D3 Fail-Closed; D4 UTC/Zeitskala/Einheit und nicht die D4-Prüftiefe; D5-A1 risikobasierte Mathematik; D6-A ein toolneutraler Vertrag mit unabhängig entwickelten Toolrealisierungen.
- O26 IoSN-Konsultationsentwurf 25.02.2026 ist nicht automatisch adoptiert. Die 21 Owner-MD/CL und die 31 ML-C08-Integrationsbefunde bleiben nach ihrem Evidenzstatus offen. G1=BLOCKED.
- Keine allgemeine Robustheitsanforderung, keine produktive Datennutzung oder Inputfreigabe, keine erfundenen KPI-/Diskont-/NTC-/Stage-F_y-Formeln, keine verbindliche DSL/ADR/Tool-/Solverwahl und keine normative Konformitäts- oder unabhängige Reviewbehauptung.
- PRs/Artefakte sind versionsgepinnt zu lesen; Ergebnisse eigener Programme nur mit belegtem Ausführungsprotokoll als tatsächlich getestet ausweisen. KI-interne Gegenprüfung ist nicht personell unabhängige Begutachtung.

### Reproduzierbares Repository-Protokoll
Repository AlOussama/TYNDP_Products. Ausgangspunkt ML-C08 Draft PR #51 HEAD 8470add62fcbc7f39b1d90c0d5afdcee50ab811e. Prüfe die tatsächlichen git-HEADs aller erforderlichen ML-C01–ML-C07 und späteren Forschungsinputs; referenziere sie als **unveränderliche** Quellen. Neuer eigener Branch **vom ML-C08-Commit**, keine Änderungen außerhalb des angegebenen neuen Workstream-Ordners; eigener Draft-PR gegen ML-C08, kein Merge/Ready. Verifiziere Source-Diff-Scope und Code-/Fixture-Ausführung, sofern im Auftrag verlangt. Abschlüsse trennen Forschung/strukturelle Tests, echte synthetische Ausführung, native Mathematik, Quelle/Originaldaten, Owner/Orakel, Unabhängigkeit und G1.
