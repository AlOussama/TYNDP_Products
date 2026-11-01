# IoSN Modul 1 — kanonische Architektur V2 und Integrationsdokumente

**Datum:** 2026-11-01  
**Status:** `M1_V2_ARCHITECTURE_PREPARED_FOR_GOVERNANCE_REVIEW` — Dokumentation, keine neuen Produktivcode- oder Real-Source-Testläufe in diesem Branch.

## Kanonischer Dokumentenindex

| Datei | Inhalt und Autorität |
|---|---|
| [00_CANONICAL_ARCHITECTURE_V2.md](00_CANONICAL_ARCHITECTURE_V2.md) | **Verbindlicher aktueller Architekturentwurf V2**: M0-Netzimport unabhängig, M1 PECD-native Quellen/Spatial Join/Time Series, M2 Netzreduktion danach |
| [10_UPSTREAM_REUSE_LEDGER_V2.md](10_UPSTREAM_REUSE_LEDGER_V2.md) | **Exakte PyPSA-Core, PyPSA-Eur, Atlite, Open-TYNDP Module/Commits**, vorhandene IoSN-MA2-/MA3-/MA4F-Bausteine, Was-wiederverwenden-vs.-neu |
| [20_SOURCE_SPATIAL_COMPONENT_CONTRACT_V2.md](20_SOURCE_SPATIAL_COMPONENT_CONTRACT_V2.md) | Quell-/Anlagen-/Zeit-/Masken-/Hydro-/DFT-Verträge; native NetCDF `ORIG`-PV; offizielle fractional mask NetCDF; auto Spatial Mapping |
| [30_WORKFLOW_AND_QUALIFICATION_V2.md](30_WORKFLOW_AND_QUALIFICATION_V2.md) | Snakemake-DAG, Source-/Netz-/Join-Gates, positive/negative Tests, Fixture-vs.-Real-Qualifikationspolitik |
| [40_NEXT_MACROS_AND_HANDOFFS_V2.md](40_NEXT_MACROS_AND_HANDOFFS_V2.md) | **Alle nächsten konsolidierten Makros und Copy/Paste-Worker-Handoffs**: MA5N, MA5D, MD2, MA6, unabhängige Endabnahme |

## Normative Modultrennung

- **M0**: importiert ausschließlich das elektrische Netzformat (z. B. CGMES) nach PyPSA und liefert gegebenenfalls Identitäts-/Geo-/DNR-Sidecar. **Keine PECD-/Hydro-/DFT-Datenverarbeitung und keine Wetter-/Basin-Profilzuordnung.**
- **M1**: liest unabhängig davon PECD-4.2-WON/WOF-Regional-CF und SPV-`ORIG`-griddierte CF/Region-CF, Hydro und ggf. Demand; verbindet diese Profile räumlich/technologisch mit den bereits existierenden PyPSA-Komponenten und schreibt ausschließlich genehmigte Zeitreihen.
- **M2**: aggregiert erst anschließend das elektrisch detaillierte Netzwerk mit den qualifizierten Daten; keine vorzeitige Aggregation in M1.

## Aktualität und Historie

Der ältere Dokumentationsstand [IOSN_M1_PECD_PYPSA_REFERENCE_TIMESERIES_ARCHITECTURE_2026_10_30.md](../IOSN_M1_PECD_PYPSA_REFERENCE_TIMESERIES_ARCHITECTURE_2026_10_30.md) und die damaligen MA-1- bis MA4-F-/MD1-Abschlussberichte bleiben **historisch**. V2 ersetzt ihre vorläufige Sollarchitektur, **nicht** ihre damaligen Test- und Datengates.

- **MA2:** `11700baa8df8cafc6bd71b96998f8b2bca647ca0` — regionale PECD-CSV, Mapping-Validator, Fixture-Level.
- **MA3:** `b3b9bf133d1b5c968323a31f8ac76090f1f2e182` — Hydro/Interval/Energy, Fixture-Level.
- **MA4F:** `1ab3eb1aed54975e69586cc3d958a24d97a6288f` — **92/92 Tests** im erfolgreichen CI, 16 Snakemake-Jobs und fünf **synthetische** Netz-Outputs.
- **MD1:** `5c68198984b6f2f430a49ff3e23d17c0b27320e1` — `M1_SOURCE_CONTRACT_BLOCKED`; keine fünf realen Projekt-WS-IDs/PECD-/Hydro-/M0-Evidenzen.

**Nicht implementiert und nicht behauptet:** nativer PV-ORIG-NetCDF-Quellparser, native fraktionale PECD-Masken-Dateiunterstützung und automatische Erzeugung des Profil-zu-bestehender-Anlage-Mappings, echter DFT-Lastadapter (nur soweit benötigt), fünf reale Source-Integration, unabhängige real-datenbasierte MA6-Abnahme. **Keine Änderung an PyPSA-Core, PyPSA-Eur oder dem M0-Code in diesem Dokumentationsmakro.**

**Offizielle Primärdokumentation:** [PECD v4.2 PUG, aktualisiert 05.08.2026](https://confluence.ecmwf.int/spaces/CKB/pages/540941752/Climate+and+energy+related+variables+from+the+Pan-European+Climate+Database+derived+from+reanalysis+and+climate+projections+v4.2+Product+user+guide+PUG), Tabellen 2.12/3.6/4.2/4.3; source-code-based Prüfpins in [10](10_UPSTREAM_REUSE_LEDGER_V2.md).
