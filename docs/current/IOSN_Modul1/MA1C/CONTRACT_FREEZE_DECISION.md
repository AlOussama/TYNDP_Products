# MA1C — Binding Contract Freeze Decision

**Entscheidungszeitpunkt:** 2026-11-01  
**Status:** **`M1_SOURCE_CONTRACT_BLOCKED`**  
**Statischer Altentscheid:** `MA1_STATIC_PASS__DATA_FREEZE_CONDITIONAL` bleibt unverändert gültig, aber **kein Real-Data-Freeze**.  
**Autorität:** M1 `NEXT_MACROS §3` am Commit `2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994`, MA-1-YAML; M0 Architektur bei `0275f482...` und nachgelagerter **noch nicht live qualifizierter** DNR-Reparaturvorschlag `85`.

## Entscheidungsmatrix

| Gegenstand | Statische Freigabe | Real-Data-Freigabe |
|---|---|---|
| M0/M1/M2 Modulgrenze und statische Netzinvarianz | `PASS_DESIGN` | `NOT_EXECUTED` |
| PECD/Hydro Open-TYNDP-Code und Methodenkatalog | `PASS_STATIC_REUSE_WITH_ADAPTATION` | `BLOCKED_MISSING_BYTE_SAMPLES` |
| fünf extern fixierte Weather-IDs/Horizonte | `COUNT_AND_NO_RESELECTION_FROZEN` | `BLOCKED_5_IDENTIFIERS_NOT_PROVIDED` |
| PECD 4.2 source/mask/version/geo | `CONTRACT_SPECIFIED` | `BLOCKED_NO_REAL_MASKS_OR_PROFILE_BYTES` |
| PV MWp↔M0 MW_AC | `FAIL_CLOSED_POLICY_FROZEN` | `BLOCKED_NO_BASE_EVIDENCE` |
| Hydro `HRR/HRI/HPI/HOL/HCL` + intervals | `CONTRACT_SPECIFIED` | `BLOCKED_NO_NATIVE_INTERVAL_OR_BASIN_EVIDENCE` |
| M0 DNR + sidecar and versioned crosswalk | `DESIGN_SPECIFIED_WITH_M0_OWNER_ALIGNMENT` | `BLOCKED_NO_REAL_M0_PACKAGE` |
| Runtime/NetCDF/PF/M2 integration | `OUTSIDE_SCOPE` | `NOT_EXECUTED` |

## Vorläufig festgehaltene Schnittstelleninvarianten

- M1 schreibt ausschließlich explizit erlaubte zeitabhängige Werte an bereits vorhandene `Generator`-/`Load`-/Hydro-IDs; statische M0-`Bus/Line/Transformer/Link/Generator/Load/StorageUnit/Store/Shunt`-Tabellen, `bus`, `p_nom`, Endpoint/Country/Source-IDs **unverändert**.
- `Generator.p_max_pu` bedeutet zeitabhängige **Verfügbarkeit/CF**, nicht Dispatch. Zeitachsen pro `(planning_horizon,weather_id)`, Quelle mit Originaltimezone und eindeutigen Intervallgrenzen, PyPSA zeitstempelkonform UTC-naive.
- Keine fünf WS aus TYNDP-2026-Dreierszenarien ergänzen; kein `get_wscenario_tyndp(...)[0]`, `safe_planning_horizon`, `fill_gaps_method=zero/mean`, nicht nachgewiesene geo-nearest oder wetterseitig erfundene Kapazität.
- PECD-Quelle und meteorologische Auflösung bleiben unabhängig von elektrischer Knotenauflösung; Wind-PEON/P2ON/PEOF/P2OF, PV-ORIG nur wenn geliefert, PV-MWp/DC-AC-Gate, hydrologische Herkunft getrennt.
- M0-`m0_sidecar` mit Revisions-/View-/Source-/Terminalmapping und `bus_role,geo_quality,component_support` ist Pflicht. Älteres `network_revision_id`-Feld erst nach M0-Owner-Bestätigung mit CAN/2.0.0 und `projection_id` harmonisieren. Ein späterer M0-Schemastand darf ohne versionierte M1-Vertragsentscheidung nicht still einfließen.

## Harte Exit-Bedingungen, kein Partial-PASS-Trick

`M1_SOURCE_CONTRACT_WITNESSED` setzt **alle** gleichzeitig voraus:

1. Fünf echte bereits festgelegte Projekt-Weather-IDs/Horizonte, verifizierter File- und Stunden-/Coverage-Witness je obligatorischer RES-/Hydro-/optional bindender Demand-Familie (pro erforderlicher Kombination).
2. Tatsächliche PECD v4.2 Input-/Header-/Masken- oder offiziell zulässige Georeferenzdateien mit Version/CRS/Hash/Sample, expliziter Source→Profile→Original-Generatorzuordnung inklusive Offshore, PV und Grenz-/Composite-Fällen.
3. Tatsächliches M0-DNR-v1-Paket, `m0_sidecar`, ID-Crosswalk, Geo-/Country-/Synthetic-Bus-Qualität, ComponentSupportMatrix, Hydro-Port, Revisions- und Manifesthash-Prüfung; **M0-Owner-Handshake**.
4. Tatsächliche Hydro-`MWh`-/`MW`-Intervalle und hydrologisch begründete Region→Existing-Hydro-Asset-Anteile; pro Originärintervall prüfbare Energiebilanz und Wirkungsgradpolitik.
5. Version-/Korrekturdaten und Lizenz-/Zugangsrechte für **jede** Datei, kein Null-/Fallback-Ersatz fehlender Datensätze.

`M1_SOURCE_CONTRACT_CONDITIONAL` wäre nur bei geliefertem realem, klar abgrenzbarem Teilsource-Witness und expliziter reduzierter Capability zulässig, **nicht** wenn zugleich M0-Paket, fünf Projekt-IDs und Hydro-Realbelege fehlen. Deshalb gemäß §3 zwingend `M1_SOURCE_CONTRACT_BLOCKED`.

## Freigaben und Verbote für Parallel-Makros

**MA2:** mit Reader-/Spatial-/Time-Fixtures und Tests in getrenntem Branch sofort startbar; `M1_RES_REAL_DATA_QUALIFIED` **gesperrt**, solange G1-C/D fehlen.  
**MA3:** Hydro-Type-/Interval-/Store-Port-Fixtures und Tests sofort startbar; `M1_HYDRO_REAL_DATA_QUALIFIED` **gesperrt**, solange G1-C/E fehlen.  
**MA4:** reale Integration/E2E/M2-Handoff nicht freigeben.  
**M0:** Eigentümerprozess für DNR/Sidecar bleibt eigenständig; keine M0-Quellfiles durch diesen Audit verändert.

**Konsolidierter nächster Nachweis:** genau die eine gebündelte Inputliste [OPEN_INPUTS_AND_EXIT_CRITERIA.md](OPEN_INPUTS_AND_EXIT_CRITERIA.md), nicht mehrere Detailfragen oder Mini-Iteration.
