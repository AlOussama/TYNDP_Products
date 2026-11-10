# BUNDLE-01 B — Input Data and Provenance Baseline

**Stichtag 2026-11-10.** `PROVISIONAL_REQUIREMENT_DISCOVERY_ONLY`; **kein Data Release, kein normativer IoSN-Contract, keine Daten- oder Modellreproduktion.**

## Umfang, Status und konkrete Befunde

- **85 fachliche Eingabeobjekte** über **18/18 Prozesse P00–P17**. Ein Eingabeobjekt kann ein echter externer Payload, ein freizugebender Steuer-/Parameterdatensatz oder ein Output eines früheren IoSN-Schritts als Input für einen späteren Schritt sein. Dieses Typfeld verhindert, dass abgeleitete Resultate als externe Quellen ausgegeben werden.
- **17 Source-/Owner-Kategorien** in `source_registry.csv`; Originaldatei-ID, Hash und tatsächlich eingefrorene IoSN-Revisionskennung sind für **keine** Kategorie positiv geprüft. Die offiziell sichtbaren 2026-Szenario-Downloadkategorien wurden als **Index nachgewiesen**, nicht als validierter IoSN-Payload.
- Alle fachlichen Key-Grains, Einheiten, Zeit, räumlichen Auflösungen, Szenario-Achsen, Versions- und Qualitätsbedingungen sind **Anforderungen an künftige Datenlieferungen**, nicht eine Behauptung, dass diese Dateien existieren oder Datenprüfung bestanden hätten.
- Methodische Aussagen zu 102 IoSN-Zonen, drei Wetterfällen je Studienjahr und Wetter-ID-Gewichten sowie 4% WACC sind Eigenschaften der **Konsultationsfassung O26**, keine unangetastet verbindlichen Bestandsdaten.
- **Wetterselektion ist vollständig upstream**. Kein Rohkandidaten-Pool, keine PCA- oder K-Means-Reimplementation, kein Selektionsalgorithmustest. Der IoSN-Input enthält ausschließlich bereits ausgewählte Wetter-IDs, Gewichte, Studie+Profilreferenzen, Zeitreihen und Provenienz.

## Referenz des O26-Entwurfs für bereits ausgewählte Wetterfälle (nur Soll-Prüftabelle)

|Studienjahr|Wetterfälle (ID:Gegenwahrscheinlichkeit)|
|---|---|
|2035|WS032:0.24; WS037:0.43; WS059:0.33|
|2040|WS065:0.20; WS071:0.40; WS077:0.40|
|2050|WS091:0.23; WS092:0.57; WS106:0.20|

*O26 §3.7 S.19–20, Draft: Ein künftig freigegebenes Run-Manifest kann abweichen. Die Summentoleranz ist nicht festgesetzt. „Gegenwahrscheinlichkeit“ in der Überschrift bedeutet **Wetterfallgewicht / Wahrscheinlichkeit** und nicht Komplementärwahrscheinlichkeit.*

## Datenstatus — präzise Interpretation

1. `PUBLIC_DOWNLOAD_INDEX`: https://2026.entsos-tyndp-scenarios.eu/download/ führt PEMMDB, PECD, Hydro Inflow, Demand, EV, Heat, Hydrogen, P2G, Line Data, Nodes, Prices und Varianten; der Downloadbereich nennt Draft Scenarios June 2026 und für öffentlich publizierte Inhalte CC BY 4.0. **Dateien, Checksummen, konkrete IoSN-Konsumversion und Nutzbarkeit nicht geprüft.**
2. `DRAFT_RULES`: O26 beschreibt Datenklassen und teils Tabellen in §4 und Annex 6.2, bestätigt aber weder eine endgültige Quelle noch eine übergreifende Datenübergabe.
3. `OWNER_EXPORT_REQUIRED`: vertrauliche oder studienspezifische Netz-, Projekt-, Sensitivitäts- und Test-Inputs sind nicht als konkrete Dateien verifiziert.
4. `DERIVED_UNEXECUTED`: Zwischenergebnisse P05–P16 sind erwartete Inputs nachgelagerter Schritte, nicht vorhandene Simulationsergebnisse.
5. `GOVERNANCE_NOT_SIGNED`: Genehmigungsakte, Provenienz- und Vergleichsorakel fehlen.

## Mindestmanifest für **jedes** reale Datenartefakt

`dataset_id`; `object_slug`; `authority/source_id`; `canonical_origin_url`; `filename`; `file_sha256`; `release/version`; `publication_timestamp`; `frozen_at`; `data_owner`; `license/access`; `study_year`; `scenario_id`; `weather_case_id`; `time_axis_timezone/calendar`; `units_base/currency_price_year`; `spatial_reference`; `transformation_lineage`; `quality_tests`; `approval/signoff`.

Eindeutigkeit und referenzielle Integrität der aufgelisteten Key-Grains sind zu validieren; ein HTTP-Download allein erfüllt **keine** Freigabekriterien. Für alle semantischen Transformationen zusätzlich Mapping, Quell-/Ziel-Grain, Aggregationsoperator, Massenerhaltung, Ausnahmen und Prüftoleranz protokollieren.

## Fachliche Schwerpunkte/Risiken

- **Startnetz (P04–P06):** 2025-Snapshot, Projekt-Eligibility a/b/c (MA02-CL-001), Richtungs- und Saisonkapazität, PTDF/LODF, Netzreduktionsorakel; Detailexporte und Zuständigkeiten offen.
- **Markt und Zeit (P02–P03/P07–P08):** PECD v4.2 im Draft, PEMMDB, DFT/EV/Heat/Hydro, Crosswalks zwischen PECD/Markt-/IoSN-Zonen und Zeitstunden; autoritative eingefrorene Releases und DQ-Toleranzen offen.
- **Strom↔H2 und DSR (P08/P14):** exogene H2-Netzstruktur und Elektrolyse-Profile; LHV/HHV-Basis, implizite/explizite DSR-Abgrenzung und Freeze-Baseline offen.
- **Kandidaten/Ökonomie (P09–P12):** NTC+/NTC−, reale/konzeptionelle/theoretische Projektkategorien und rechenstufenbezogene Verfügbarkeit; korrekter Marktlink unabhängig von physischem AC/DC; Routenfaktor, Speicherparameter und Diskontierung offen.
- **Ergebnisse und Abnahme (P13–P17):** Output-Gleichwertigkeit, KPI-Spezifikation, Kleinmengenfilter, Testorakel und unabhängige Sign-offs fehlen; sie bleiben abhängige Kontrollinputs, keine vermeintlichen externen Marktdateien.

**Verweise:** O26 §§3.2–4.6 und Annexes 6.1–6.3; bestehende MA01-Quellen-, Systemanforderungs- und Prozessmatrizen (PR #17); MA02 Authority (PR #18). Daten wurden nicht geöffnet/ausgeführt, keine Verfügbarkeitszusage.
