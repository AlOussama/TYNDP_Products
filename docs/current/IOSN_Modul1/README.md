# IoSN Modul 1 — reduzierte Architektur V3

**Datum:** 2026-11-01  
**Aktueller Architekturvorschlag:** `M1_V3_REUSE_MA2_MA3_MA4F__MINIMAL_PECD_SOURCE_AND_SPATIAL_DELTA`  
**Umsetzungsstatus:** bestehender MA4F-Composer **synthetisch getestet**, reale Quellen-/Netzverknüpfung und optionale native PECD-Rasterdaten **noch nicht** qualifiziert.

## Vorrangiger Architekturtext

**[50_REDUCED_ARCHITECTURE_V3.md](50_REDUCED_ARCHITECTURE_V3.md)** — ein einziger, schlanker Sollvertrag:

1. Bestehende **MA-2-/MA-3-Reader** nutzen; native PV-ORIG-/Masken-Funktionen nur entwickeln, wenn die realen Source-Dateien dies verlangen.
2. PECD-Profil/Region/Raster auf **vorhandene** Generator-/Hydro-/Load-IDs abbilden; bewährte GIS-Bibliotheken und MA-2-Mappingvalidator wiederverwenden.
3. Bestehenden **MA-4F-Composer** als einzigen PyPSA-Writer verwenden; dessen M0-spezifische Pflichtmanifeste für generische PyPSA-Netze und echten Real-Mode minimal entkoppeln, alle Invarianz-/Test-Gates erhalten.

**M0:** Netzimport und elektrische Stammdaten. **M1:** unabhängiger PECD-/Hydro-/optional Demand-Zeitreihen-Join. **M2:** spätere Netzzusammenfassung. PyPSA-Core und Solver unverändert. Kein neuer Wetterjahresentscheid.

**Nur zwei verbleibende Phasen:** zunächst tatsächlich verfügbares PECD-Produktformat und minimale Code-Deltas belegen/ergänzen, danach bei echten Quellen und qualifiziertem Netz eine gesamte Real-Datenkampagne mit unabhängiger Abnahme. Frühere V2-Handoffs starten **nicht automatisch** als getrennte Makros.

## V2-Dokumente als technische Referenzen (keine neue Ausführungspflicht)

| Dokument | Weiterhin gültiger Wert |
|---|---|
| [00_CANONICAL_ARCHITECTURE_V2.md](00_CANONICAL_ARCHITECTURE_V2.md) | Frühere umfassendere Sollarchitektur, durch V3-Vereinfachung überholt, historische Evidenz bleibt |
| [10_UPSTREAM_REUSE_LEDGER_V2.md](10_UPSTREAM_REUSE_LEDGER_V2.md) | Verifizierte PyPSA-Core/PyPSA-Eur/Atlite/Open-TYNDP-Schnittstellen |
| [20_SOURCE_SPATIAL_COMPONENT_CONTRACT_V2.md](20_SOURCE_SPATIAL_COMPONENT_CONTRACT_V2.md) | Nachschlagewerk für detaillierte Source-/Geo-/Hydro-/Zeitsemantik |
| [30_WORKFLOW_AND_QUALIFICATION_V2.md](30_WORKFLOW_AND_QUALIFICATION_V2.md) | Bestehende Fixture-/Source-/QA-Gates |
| [40_NEXT_MACROS_AND_HANDOFFS_V2.md](40_NEXT_MACROS_AND_HANDOFFS_V2.md) | Historischer Mehr-Makro-Plan; V3 bündelt den nachweislich notwendigen Restumfang |

## Tatsächliche Umsetzungsevidenz

- **MA-2** [`11700baa`](https://github.com/AlOussama/TYNDP_Products/tree/11700baa8df8cafc6bd71b96998f8b2bca647ca0/scripts/iosn_m1/res) — PECD-CSV/ISO-Parser, Geometrieprüfung, 20 lokale synthetische Tests laut Producerbericht.
- **MA-3** [`b3b9bf13`](https://github.com/AlOussama/TYNDP_Products/tree/b3b9bf133d1b5c968323a31f8ac76090f1f2e182/scripts/iosn_m1/hydro) — hydrologische Intervall- und Energietreue, Fixturetests/CI.
- **MA-4F** [`1ab3eb1a`](https://github.com/AlOussama/TYNDP_Products/blob/1ab3eb1aed54975e69586cc3d958a24d97a6288f/docs/current/IOSN_Modul1/MA4F/EXECUTION_REPORT.md) — erfolgreicher CI-Lauf mit **92/92 Pytest**, 16 Snakemake-Jobs und fünf synthetischen NetCDF-Ausgaben; kein Real-PASS.
- **MD-1** [`5c681989`](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/EXECUTION_REPORT.md) — physische PECD-/Hydro-/M0-Quellen **nicht** geliefert/qualifiziert.

**Aktuelle Grenze:** Die V3-Datei ist eine Architekturentscheidung auf einem eigenen Dokumentationsbranch, **keine** zusätzliche Softwareimplementierung oder Real-Data-Zertifizierung.
