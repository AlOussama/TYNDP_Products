# MA-01 — IoSN Requirements Baseline & Scope Consolidation

> **STATUS: PROVISIONAL / NOT APPROVED — stand 2026-11-05.** Als Dokumentenbaseline gegen die offizielle ENTSO-E **TYNDP 2026 Identification of System Needs Methodology, Version for Public Consultation, 25 February 2026** geprüft. Eine **final genehmigte effektive Methodikversion ist nicht bestätigt**; insbesondere werden fehlende Kosten-/Qualitäts-/KPI-Parameter als BLOCKED dokumentiert. Dies ist **keine** ENTSO-E-Methodikfreigabe und **keine** durchgeführte Modellkonformitätsprüfung.

## Scope und einzig aktiver Requirements-Stand

Die IoSN-Prozessumsetzung **übernimmt extern bereits ausgewählte Wetterjahre**: Anzahl, Jahr-IDs, Studienjahrzuordnung, veröffentlichte bzw. freigegebene Gewichte, referenzierte Zeitreihen, Zeitachsen, Einheiten und Provenienz. Nur **Input-Konsistenz- und Datenqualitätsprüfungen** sind in Scope. PCA, K-Means, Wetterjahrauswahl, Auswahlentscheidungsreproduktion und deren Verifikation sind **explizit OUT OF SCOPE**.

**Alle früheren Requirements-IDs MR-*, SR-*, LRC-*, VC-*, UC-01 aus PR #16 sind LEGACY/HISTORICAL und NICHT aktiv.** Sie sind für Audit/Provenienz archiviert, einschließlich des dortigen Wetterauswahl-Use-Cases und PoC. **Das einzige aktive (noch vorläufige) SyRS-Verzeichnis** lautet iosn_requirements_catalogue.csv mit 48 MA01-SR-IDs, abgeleitet von 50 quellenbezogenen MA01-MR-IDs, wobei MA01-MR-012 und MA01-MR-049 ausschließlich auf einen externen Prozess verweisen und **keine** aktiven MA01-SR erzeugen.

## MA-01-Deliverables (rev 0.1.0, 2026-11-05)

|Datei|Inhalt|Verbindlichkeitsgrad|
|---|---|---|
|methodology_source_baseline.md|Offizielle Konsultationsfassung, Quellen-/Statuskontrolle, Fundstellen 50 MA01-MR, Fehler/Annahmen|Vorläufige methodische Evidence|
|iosn_process_specification.md|18 Schritte P00–P17, Quellen, Ein-/Ausgänge, LF/OPF/Stage-H2-Varianten, Prozessdiagramm|Vorläufige Prozessinterpretation|
|iosn_process_matrix.csv|Strukturiertes Prozessregister mit Regeln, Freiheitsgraden und Prüfbarkeit|Vorläufig|
|iosn_system_requirements.md|L1–L4 und vollständige 48 MA01-SR in toolneutraler Form|Einzige aktive Draft-SyRS|
|iosn_requirements_catalogue.csv|48 MA01-SR mit Implementierungsfreiheit, Akzeptanz-/Nachweisspalten|Einziger aktiver Requirements-Katalog (PROPOSED)|
|iosn_methodology_traceability.csv|50 Quellen-Items, 48 L1→L2→L3→L4 Ketten und 2 upstream-only|Vorläufiges Traceability-Register|
|methodology_ambiguity_register.md|20 offen priorisierte Methodikentscheidungen MD-01–20|OPEN / owner approval required|
|requirements_review.md|R1–R5 unabhängige methodische Review-Findings|Review dokumentiert, kein Sign-off|
|scope_and_change_impact.md|Wetterauswahl ausgeschlossen; alte Reports/PoC-Audit und Ablösung|Kontrollierte Scope-Korrektur|
|handoff_to_language_architecture.md|Verwendbare/gesperrte Inputs, Gate-Abhängigkeiten, unabhängige Folgeoptionen|Nur Handoff, kein Folgeauftrag|

**Methodikquelle:** [ENTSO-E O26 consultation PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf). [Offizieller Konsultationseintrag](https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/). Externe Datenquellen, Quelle/Anhang/PDF-Status und unbestätigte Folgeversion im Baseline-Dokument.

## Governance und L1–L4

L1 Methodology → L2 tool-neutrale System Requirements → L3 Required Formalisation (keine konkrete DSL) → L4 Verification Needs (kein Test ausgeführt). Jede Pflicht zu Mathematik (LP-Stufen, nichtantizipative Investments, wettergewichtete Kosten, Stromnetz-DC-Flüsse) bleibt quellengebunden. Alle Übertragungsausbaukandidaten sind nach O26 §4.5.2 als kontrollierbare DC-**Market**-Links, auch wenn physisch AC, zu beschreiben; das unterscheidet sich von vermaschten elektrischen DC-Lastflüssen. **Keine** Festlegung auf SysML v2, CESM/GEMS/INES, eigene DSL, PyPSA, Antares oder Sienna.

**Freigabestatus:** offizielle effektive Quelle OPEN; MD-01–20 fachlich offen; L4-Systemnachweise zu allen 48 MA01-SR **NOT_EXECUTED**; keine volle mathematische/KPI-Systemakzeptanz.

## Historische Forschungsartefakte — ausdrücklich superseded

Die folgenden alten Dokumente haben direkt im Kopf den Hinweis **MA-01 LEGACY / NOT ACTIVE**: 01_executive_summary.md, 02_iosn_process_analysis.md, 03_system_requirements.md, 04_language_requirements.md, 05_existing_languages_review.md, 06_matrix_interpretation.md, 07_architecture_options.md, 08_formalisation_use_cases.md, 09_verification_traceability.md, 10_poc_specification.md, 11_critical_review.md, 12_architecture_decision.md, 13_implementation_roadmap.md.

Auch die früheren Tabellen source_clause_coverage.csv, sources_inventory.csv und 06_language_capability_matrix.csv sind **HISTORICAL ONLY**. Der alte Ordner poc/** inklusive Validator, synthetischer Fixture-Daten, Tests und Ausführungsnachweis bleibt vollständig **unverändert** und ist ein historischer Demonstrator des **bereits ausgewählten** Wetter-Inputs, keine operative Wetterauswahl oder neue MA-01-Validierung. **Bestehende IoSN-Implementierungen sind nicht verändert worden.**

## Nutzung durch nachfolgende Teams

Das MA-01-Paket darf zur Quellen-/Requirements-Prüfung verwendet werden. **Nicht** als verbindlicher endgültiger Vertrag ohne offizielle Methodik- und Owner-Freigaben verwenden. Folge-Makroaufträge, neue PoC-Implementierungen, Adapter oder Sprach-/Architekturauswahl wurden **nicht** gestartet. Für Sequenz, Unabhängigkeiten und Blocker siehe handoff_to_language_architecture.md.
