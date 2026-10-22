# Modelling Languages & Interoperability — Review-Arbeitsstand

**Stichtag:** 23.10.2026 · **Status:** unabhängiger *Desktop-/Quellenreview*, vorläufig; kein vollständiger Konformitätsnachweis.  
**Gegenstand:** übergreifende Interoperabilität von TYNDP-/NEP-Energiesystemmodellen und CBA-Szenarien; nicht die IoSN-Implementierung.

## Kernaussage

Die vorläufig sinnvollste **allgemeine** Architektur ist ein normativer, toolneutraler **A+-Kern** (Semantik, Methoden- und Transformationsdeklarationen, Planning/Comparison Contract) mit **optionalen B-/B+-Profilen** für mathematische 1:1-Konformität oder freigegebene Alternativmethoden. Dies ist eine **zu testende Architekturhypothese**, kein durch Multi-Tool-Experimente nachgewiesener Sieger. Unter strikter regulatorischer Mathematik-Konformität können B oder B+ vorzugswürdig sein.

**Vier unterschiedliche Fragen:** (1) Requirements Clarification, (2) mathematisch-semantische 1:1-Übersetzung, (3) Interoperation über heterogene Tools, (4) Conformance unabhängiger Implementierungen, (5) methodische und entscheidungsbezogene Robustheit. Ein gültiges Schema beantwortet nicht automatisch die Fragen (2) bis (5).

## Dokumente

| Datei | Zweck | Status |
|---|---|---|
| [REVIEW_PROMPT.md](REVIEW_PROMPT.md) | Verbindlicher vollständiger Reviewauftrag, 14 Abschnitte | Unverändert |
| [review/architecture_review.md](review/architecture_review.md) | Executive Summary, Hypothesen H1–H8, Review-Runden, Einordnung von GEMS | Quellenreview; kein Experiment |
| [review/findings.md](review/findings.md) | Priorisierte kritische Befunde mit Korrekturen, Unsicherheiten und Prüfgates | Vorläufig |
| [review/claim_evidence_matrix.csv](review/claim_evidence_matrix.csv) | Maschinenlesbare Claim–Source–Status-Zuordnung | Vorläufig |
| [review/review_status.md](review/review_status.md) | Input-Inventur, 14-Abschnitte-Fortschritt, noch fehlende Nachweise | Verbindliche Abgrenzung |
| [analysis/architectures.md](analysis/architectures.md) | A/A+/B/B+ und Metamodellvergleich mit Mermaid-Diagrammen | Designreview |
| [analysis/cba_interoperation_scenarios.md](analysis/cba_interoperation_scenarios.md) | CBA-Use-Cases: Modellfehler, M1→M2, Robustheit, Übersetzung | **Nächster fachlicher Schwerpunkt** |
| [analysis/cba_contracts_and_tests.md](analysis/cba_contracts_and_tests.md) | Normative CBA-Contracts, Akzeptanzkriterien, Verlustklassen und Testfälle | Pilot-Spezifikation |
| [analysis/cba_pilot_plan.md](analysis/cba_pilot_plan.md) | Geordneter Validierungspilot und Stop-/Go | Geplant, noch nicht durchgeführt |
| [analysis/recommendation_adr.md](analysis/recommendation_adr.md) | Bedingte Architekturentscheidung (ADR) mit Falsifikationskriterien | Proposed |
| [sources/bibliography.md](sources/bibliography.md) | Primärquellen, Fassungen und Grenzen | Überprüft am Stichtag |

## Fachliche Trennung von IoSN

IoSN ist **nicht** Gegenstand dieses Architektur-Reviews und nicht die Quelle eines universellen Metamodells. Der im Stammrepository vorhandene IoSN-Forschungsstrang wird weder verändert noch als Beweis für CBA-Interoperabilität verwendet. Hier werden nur eigenständige, allgemeine CBA-/TYNDP-/NEP-Anforderungen behandelt.

## Evidenz- und Reifegrenzen

- **Belastbare Quellen:** 4th ENTSO-E CBA Guideline (EC-approved, 2024); TYNDP 2026 CBA Implementation Guidelines **Konsultationsentwurf 16.12.2025**, nicht als finaler Stand zitiert; Primär-READMEs und Konverter-Kompatibilitätslisten (siehe Bibliographie).
- **Nicht nachgewiesen:** Multi-Tool-Konformität, verlustfreie GEMS-/CESM-/INES-Round-Trips, vollständige Abdeckung aller Modellklassen, realistische CBA-Entscheidungsrobustheit, abschließende Freigabe der 2026er Implementation Guidelines.
- **Rechenzahlen** in den Beispielen sind ausschließlich illustrativ. Keine tatsächlichen TYNDP-Projektergebnisse.
- Der vollständige 14-teilige Auftrag ist **noch nicht abgeschlossen**; der Bearbeitungsstand ist ausdrücklich dokumentiert.

Alle hier angelegten Dateien befinden sich ausschließlich unter `Modelling_Language/`. Kanonische IoSN-Dateien bleiben unverändert.
