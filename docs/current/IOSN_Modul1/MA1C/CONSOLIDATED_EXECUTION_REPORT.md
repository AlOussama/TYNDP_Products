# M1-MA1C — Consolidated Physical Source & M0 Interface Witness

**Datum:** 2026-11-01  
**Rolle:** Independent Data & Spatial Contract Auditor  
**Ergebnis:** `M1_SOURCE_CONTRACT_BLOCKED` — statische Quelle/Schnittstelle dokumentiert, physisches Real-Data-Gate nicht bestanden.  
**Scope:** eine zusammenhängende statische Prüfung; keine Wetterjahresauswahl, keine produktive Software, keine meteorologischen/elektrischen Simulationen, keine synthetischen Daten als Realevidenz.

## 1. Unveränderlicher Prüfstand

| Referenz | Festgehaltener Stand | Prüfergebnis |
|---|---|---|
| M1-Auftrag | [NEXT_MACROS §3](https://github.com/AlOussama/TYNDP_Products/blob/2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994/docs/current/IOSN_M1_NEXT_MACRO_ASSIGNMENTS_AND_HANDOFFS_2026_11_01.md), Commit `2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994` | Commit und Inhalt verifiziert |
| M1 MA-1 | `IOSN_M1_MA1_CONSOLIDATED_SOURCE_SPATIAL_CONTRACT_AUDIT_2026_11_01.md`, Blob `1032def05eaa09eef33ece80bf952df385ee745e` | vollständig eingesehen |
| M1 logischer Contract | `IOSN_M1_MA1_LOGICAL_DATA_CONTRACT_2026_11_01.yaml`, Blob `f19ed696fdfde0211f991ac8bc0e37103799d167` | `selected_weather_ids: null`, `required_count: 5` |
| M1 Basisarchitektur/Spatial | `IOSN_M1_PECD_PYPSA_REFERENCE_TIMESERIES_ARCHITECTURE_2026_10_30.md` und `IOSN_M1_SPATIAL_RESOLUTION_AND_MACRO_EXECUTION_PLAN_2026_11_01.md` | eingesehen; ältere MA-3/MA-4-Aufteilung nur historisch, NEXT_MACROS maßgeblich |
| M0 Architektur | [Commit `0275f482...`](https://github.com/AlOussama/TYNDP_Products/commit/0275f48231a0794bea324b9cab34700bb0de8f5b), Docs `30`, `40`, `60`, `70` | getypter Leistungs-/Identity-/Geo-Entwurf, `DESIGNED_NOT_EXECUTED` |
| M0 unabhängiger Review | [`80_INDEPENDENT_ARCHITECTURE_REVIEW.md`](https://github.com/AlOussama/TYNDP_Products/blob/ea62050a867c27036552af28d3e0102a8689f4ec/docs/current/IOSN_Modul0_CGMES/80_INDEPENDENT_ARCHITECTURE_REVIEW.md), Commit `ea62050...` | `REPAIRS_REQUIRED`, 7 P1 / 4 P2; kein Runtime-PASS |
| M0 jüngerer Repair-Entwurf | [`85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md`](https://github.com/AlOussama/TYNDP_Products/blob/research/iosn-m0-cgmes-m2-m3-repair-20261101/docs/current/IOSN_Modul0_CGMES/85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md), Blob `209416fd687d5ab700993684ca64a998241a4cad` | CAN/2.0.0 und DNR/1.0.0 spezifischer; `SPECIFIED_FOR_STATIC_CHECK`, **nicht** M0-Owner-PASS |
| PECD-/Hydro-Reader | [Open-TYNDP `tyndp-2026`](https://github.com/open-energy-transition/open-tyndp/tree/71a3a9a15b77114cd79458bceabc98e1a64dd58a), Commit `71a3a9a15b77114cd79458bceabc98e1a64dd58a` | Versionstabellen, Technologie-Crosswalk und Quellcode gelesen |
| Offizieller Downloadkatalog | [TYNDP 2026 Inputdaten](https://2026.entsos-tyndp-scenarios.eu/download/); [CDS PECD](https://cds.climate.copernicus.eu/datasets/sis-energy-pecd?tab=documentation) | Downloadverweise/Produktdokumentation gefunden; **keine heruntergeladenen Prüfbytes** |

## 2. Ausgeführte Prüfschritte und Reichweite

1. GitHub-Commit, M1-Auftrag, MA-1-Audit/YAML, M1-Basisarchitektur und Spatial-Makroplan gelesen; normative M0-Architektur mit getrennten Revisions-/Geo-/ID-/Capability-Feldern abgeglichen.
2. Am fixierten M1-Ausgangscommit rekursive GitHub-Dateibaum-Inventur **127 Blobs, keine gekürzte Baumantwort**, einschließlich `artifacts`, `docs`, `provenance`, `results`, `src`, `tests`. Ergebnis: keine eigenständigen namentlich erkennbaren realen PECD-/Hydro-Zeitreihendateien, fünf Wetter-ID-Manifeste, M0-PyPSA-`.nc` oder M0-`m0_sidecar` im Dateibaum. Die `results/synthetic`-Dateien sind ausdrücklich nicht physische Evidenz.
3. Drei ZIP-Archive unter `artifacts/bundles/` wurden als Git-Blobs inventarisiert. Die aktive GitHub-Textschnittstelle konnte sie nicht als UTF-8 lesen (`UnicodeDecodeError`); **ZIP-Inneninhalte nicht kontrolliert**, daher kein Beweis ihrer Inhaltsfreiheit.
4. GitHub-M0-Architekturstand und unabhängigen M3-Review sowie nachgelagerte Spezifikationskorrektur eingesehen. Kein reales M0-Paket, reale Plant-ID-/Sidecar-Tabelle oder mit Originaldaten geprüfte Hydro-Speicherklasse verfügbar gemacht.
5. Open-TYNDP: `data/tyndp_versions.csv`, `data/tyndp_technology_map.csv`, `rules/sb.smk`, PECD-Filter/Reader/NetCDF-Builder, Hydro-Reader/Builder, Demand-Reader auf referenziertem Commit geprüft. Upstream-Git-Baum umfasst 524 Blobs; vorhandene Text- und Hilfsdaten sind **nicht** die benötigten Projekt-PECD/Hydro-Rohprofile.
6. Offizielle PECD-, Hydro-Inflow- und Demand-Verweise nachgeschlagen. ZIP-Download konnte im Auditwerkzeug nicht als Byteinhalt geprüft werden. Keine gemessene SHA-256, kein reales CSV-Header-/Zeitstempel-/Geometrie-Sample, kein Regionsmasken-Raster-Sample, keine Genehmigung der fünf Projekt-Wetter-IDs.
7. Projekt-/Library-Dateisuche nach fünf IDs, Hydro-/PECD-Rohdaten und M0-Referenz ergab lediglich methodische Wetterauswahl-Dokumentation; **nicht** fünf Projektwetterdatensatz-Manifeste. Diese Suche begründet nur den aktuellen Evidenzstand, nicht die Nichtexistenz beliebiger externer Datenablagen.

**Evidenzklassen:** `GIT_TEXT_WITNESSED` = echter Textinhalt vom SHA; `PUBLIC_CATALOG_LOCATED` = reale Downloadreferenz, ohne Bytes; `DESIGN_ONLY` = Normdokument ohne erzeugtes Datenprodukt; `BINARY_UNINSPECTED` = Blob vorhanden, Inhalt nicht geprüft; `NOT_PROVIDED` = benötigter Pflichtnachweis nicht im zugänglichen Paket; `NOT_EXECUTED` = keine Laufzeit-/Mengenprüfung.

## 3. Zentrale Daten-/Source-Feststellungen

- **Wetter-Fünfer-Set:** fünf extern festgelegte IDs, aber keine einzige explizit identifizierte Projektreihe. Der Open-TYNDP-2026-Code nennt je Horizont drei gefüllte reguläre WS: 2030 = `WS003,WS021,WS029`; 2035 = `WS032,WS037,WS059`; 2040 = `WS065,WS071,WS077`; 2050 = `WS091,WS092,WS106`. Diese Werte sind **Quellcode-Metadaten, nicht die fünf Projektentscheidungen**.
- **Releasekonflikt:** Open-TYNDP-Versionstabelle führt `tyndp_2026` 2026-08-21 (korrigierte Demand/Hydro/Line/PEMMDB-Sätze), 2026-10-07 (neuerer preliminary-Stand), `tyndp_pecd` 4.2 und den `4.2+pre-built.0.1`-Stand 2026-08-13. Keine garantierte releaseübergreifende Gleichheit, Dateirevisions- und SHA256-Abgleich erforderlich. Git-Blob-SHAs sind kein Dateiquellen-SHA256.
- **Spatial:** PEON/P2ON-Onshore, PEOF/P2OF-Offshore, ORIG-PV nur mit tatsächlich bezogenem Grid; NUT2/SZON/PEON/P2ON regionale PV bleiben regional. CGMES-Originalbus oder synthetischer Sternbus impliziert **keinen** Anlagenort. Formale `asset_profile_map`-/MW-Anteilsnachweise fehlen real.
- **PV:** `MW/MWp` der PECD-PV-Quelle darf ohne Beleg der M0-Nennleistungsbasis `MW_AC` nicht direkt `Generator.p_max_pu` befüllen.
- **Hydro:** `HRR,HRI,HPI,HOL` Quelle/Einzugsgebiet/Zeitintervall; `HCL` closed-loop ist gesonderte Modellklasse, kein bewiesener natürlicher PECD-Zufluss. `HRO/HPO/HRG` kennzeichnen Erzeugung statt Inflow. Die TYNDP-Reader verwenden heuristische `/168`, `/24`, `ffill` und `fillna(0)`, für MA-3 bei unbewiesenen Intervallen/fehlender Quelle unzulässig.
- **M0:** Normvertrag mit `m0_sidecar`, Source-/View-/Asset-ID und Geoqualität ist dokumentiert. Aktuelle korrigierte Variante CAN/2.0.0/DNR/1.0.0 trennt `source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id`. Ein faktischer Paket-/Version-/Qualifikations-Handshake mit dem M0-Owner fand nicht statt.

## 4. Ergebnisse der MA-1C-Akzeptanzgates

| Gate | Beurteilung | Evidenz-/Negativfeststellung |
|---|---|---|
| G1-A — Upstream static reuse | `PASS_STATIC` (MA-1 übernommener Befund; erneut Quellcode-Stichproben) | Open-TYNDP Reader und Technologie-/Versionsdateien vorhanden |
| G1-B — Logical architecture contract | `PASS_DESIGN_WITH_M0_ALIGNMENT_HOLD` | M1-Design vorhanden; M0-DNR-Schemaversion vom Owner offen |
| G1-C — Real M0 DNR and sidecar | **`BLOCKED_NOT_PROVIDED`** | kein echtes M0-Netz/Sidecar/View-Source-Map/Geo-Asset |
| G1-D — Real five PECD sources & masks | **`BLOCKED_NOT_PROVIDED`** | fünf IDs und gehashte Profil-/Masken-Samples fehlen |
| G1-E — Real Hydro intervals & allocation | **`BLOCKED_NOT_PROVIDED`** | Originär-Intervalle, Basin-/TSO-Anteile und Speicherport fehlen |
| G1-F — PyPSA runtime, roundtrip | `NOT_EXECUTED` | bewusst außerhalb MA1C; keine Testläufe |
| MA1C Gesamtentscheid | **`M1_SOURCE_CONTRACT_BLOCKED`** | reale G1-C/D/E Pflichtnachweise fehlen |

## 5. Lieferumfang und offene Gesamtinputliste

Dieser Branch enthält den exakten Fünf-Slot-CSV, maschinenlesbaren Source-Status, räumliche Produktmatrix, Spatial-Assignment-Ledger, Hydro-Quellintervall-Ledger, M0-Referenzwitness/Interface-Crosswalk, datengebundene Freezeentscheidung, einmalige konsolidierte Inputliste und vollständige MA-2-/MA-3-Handoffs. Details: [OPEN_INPUTS_AND_EXIT_CRITERIA.md](OPEN_INPUTS_AND_EXIT_CRITERIA.md).

**Keine Zertifikate:** Null reale CF/Inflows, null M0-Netze, null hydrologische Zuordnung, null validierte WS-ID und null erfolgreiche Laufzeittests wurden aus Dokumentation in einen behaupteten PASS umgedeutet. Keine produktive Python-, Snakemake- oder Netzdatei geändert.

**Abschlussentscheidung:** Statischer Vorbereitungsstand nutzbar; **physischer Inputcontract nicht gefroren**. MA-2/MA-3 dürfen parallel Quellparser-Adapter und rein synthetische Fixtures entwickeln; Real-Data-PASS erst nach Erfüllung der referenzierten M0-, PECD- und Hydro-Gates. Modul 2 Netzaggregation ist vollständig außerhalb des Auftrags.
