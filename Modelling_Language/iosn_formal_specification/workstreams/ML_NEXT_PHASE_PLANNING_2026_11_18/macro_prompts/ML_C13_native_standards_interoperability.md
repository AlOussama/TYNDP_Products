# MAKRO-AUFTRAG ML-C13
## Native Standards Parsing, Semantic Round-Trip & A/B/C Interoperability Experiment

### 1. Rolle
Agiere als Team aus Formal Language/Schema Expert, SysML/ReqIF/LinkML/SHACL Architect, Energy Model Interoperability Expert, Versioning/Migration Specialist, Software Test Engineer und adversarial Architectural Reviewer.

### 2. Ziel
Prüfe mit **tatsächlich ausgeführten nativen Parser-/Serializeraufrufen** das Erweiterungs- und Verlustverhalten der A/B/C-Forschungsarchitekturen. C06 hat bisher nur drei Darstellungen unter **gemeinsamem eigenem Prüfkern** klassifiziert; es gab keinen nativen Standardparser- oder Energietool-Nachweis. Keine endgültige Architekturwahl.

### 3. Quellen und Hypothesen
Verwende ML-C08 architecture_experiment_decision_brief.md, C06 A/B/C Prototypen und 135/135+24/24 lokale Ergebnisse, C02 528/1323 Typgraph, C01 Source-/Statussemantik und C04 B01–B15. Standardskandidaten: LinkML, JSON Schema, SHACL/RDF, ReqIF, SysML v2/KerML, GEMS, mathspec, INES/CESM, Sienna. Dokumentierte Standardsfähigkeit ≠ getestete Fachsemantik.

### 4. Experimente
1. Wähle **mindestens zwei technisch ausführbare unterschiedliche Standardparser/Validatoren**, etwa JSON Schema und LinkML/SHACL oder ReqIF; eine Eigenimplementation derselben Strukturprüfung zählt nicht als nativer Standardparser.
2. Repräsentiere *dieselbe begrenzte* Contract-Slice (Quelle/Authority, D2/CY, D4/UTC, SR/P/Data/T/Math/Evidence IDs, PhysicalBranch vs MarketLink, optionale P15, process-only Daten) in den gewählten Standards, dokumentiere tatsächliche Konformitätslücken.
3. Führe Parser-/Serializer-Roundtrips, absichtlich falsche Referenzen, Verlust von SourceStatus, Branch/MarketLink, P15-Guard, Gewichtscase-IDs und 20 process-only durch.
4. Vergleiche A, B und C mit denselben In-/Out-Semantiken, einschließlich Authorität/Source-of-Truth, typisiertem Mapping und round-trip loss certificate.
5. Miss reproduzierbar Aufwand für Versionswechsel: Quellclauses, Math-Operatoren, Profilversionen, Migrationspfade, erneute Testpflichten. Echte Aufwandsschätzungen und Messwerte trennen.
6. Wenn Parserinstallation nicht verfügbar ist, **NOT_EXECUTED** mit Ursache und dennoch Teilergebnis liefern; keinen Standard-PASS fingieren.
7. Keine Pflicht, dass jeder der 48 SR in jedem Standard vollständig mathematisch ausdrückbar ist; dokumentiere repräsentierte und nicht repräsentierte Bereiche und Verbindung zu einem gemeinsamen logischen Semantikkern.

### 5. Liefergegenstände
Im Ordner .../ML_C13_native_standards_interoperability/:
- selected_native_standards_and_capabilities.md
- native_slices_and_parsers/
- executed_parser_roundtrip_report.md
- shared_semantic_contract_slices.md
- mapping_loss_and_coverage_matrix.csv
- source_version_migration_experiment.md
- architecture_A_B_C_comparative_evidence.md
- independent_architecture_review.md
- conditional_handoff_to_future_ADR.md

### 6. Forschungsabnahme
Mindestens zwei native Standard-Engines mit konkretem Invocation-/Versions-/Fixture-/Ergebnisprotokoll **oder** explizit begrenzte Teilreife. Alle A/B/C Bewertungen müssen ihre tatsächliche parserbasierte Evidenztiefe angeben. Kein echter E04-Generatorbeweis oder ADR aus reinem Roundtrip.

**Welle 1: sofort unabhängig startbar.**

### Gemeinsame Quellen-, Scope- und Governance-Bedingungen
- D1: Einzige aktive vorläufige Baseline sind 48 unveränderte MA01-SR ohne SR-012/SR-049; P00–P17 bleiben 18 fachliche Schritte.
- D2: Fünf extern gewählte CY1–CY5; identischer CY-indizierter symbolischer Gewichtsvektor über 2035,2040,2050, aber nicht notwendig gleiche Gewichte zwischen CY. Reale Zahlen und Originale TBD. Keine Wetterjahrselektion.
- D3 Fail-Closed; D4 UTC/Zeitskala/Einheit und nicht die D4-Prüftiefe; D5-A1 risikobasierte Mathematik; D6-A ein toolneutraler Vertrag mit unabhängig entwickelten Toolrealisierungen.
- O26 IoSN-Konsultationsentwurf 25.02.2026 ist nicht automatisch adoptiert. Die 21 Owner-MD/CL und die 31 ML-C08-Integrationsbefunde bleiben nach ihrem Evidenzstatus offen. G1=BLOCKED.
- Keine allgemeine Robustheitsanforderung, keine produktive Datennutzung oder Inputfreigabe, keine erfundenen KPI-/Diskont-/NTC-/Stage-F_y-Formeln, keine verbindliche DSL/ADR/Tool-/Solverwahl und keine normative Konformitäts- oder unabhängige Reviewbehauptung.
- PRs/Artefakte sind versionsgepinnt zu lesen; Ergebnisse eigener Programme nur mit belegtem Ausführungsprotokoll als tatsächlich getestet ausweisen. KI-interne Gegenprüfung ist nicht personell unabhängige Begutachtung.

### Reproduzierbares Repository-Protokoll
Repository AlOussama/TYNDP_Products. Ausgangspunkt ML-C08 Draft PR #51 HEAD 8470add62fcbc7f39b1d90c0d5afdcee50ab811e. Prüfe die tatsächlichen git-HEADs aller erforderlichen ML-C01–ML-C07 und späteren Forschungsinputs; referenziere sie als **unveränderliche** Quellen. Neuer eigener Branch **vom ML-C08-Commit**, keine Änderungen außerhalb des angegebenen neuen Workstream-Ordners; eigener Draft-PR gegen ML-C08, kein Merge/Ready. Verifiziere Source-Diff-Scope und Code-/Fixture-Ausführung, sofern im Auftrag verlangt. Abschlüsse trennen Forschung/strukturelle Tests, echte synthetische Ausführung, native Mathematik, Quelle/Originaldaten, Owner/Orakel, Unabhängigkeit und G1.
