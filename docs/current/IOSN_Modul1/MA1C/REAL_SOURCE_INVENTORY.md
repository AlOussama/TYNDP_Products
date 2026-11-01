# MA1C — Real Source Inventory und Provenienzprüfung

**Prüfdatum:** 2026-11-01 · **Status:** `PHYSICAL_SOURCE_WITNESS_BLOCKED`. Textuell verifizierte Quellen sind **keine** realen Wetter-/Hydro-Samples. Maschinenlesbare Einzelstände in [SOURCE_STATUS_LEDGER.csv](SOURCE_STATUS_LEDGER.csv).

## 1. Inventarisierte Quellen, nicht nur Source-Code

| Familie / Autorität | Tatsächlicher Zugriff / Nachweis | Benötigte fehlende Realdatei-Information |
|---|---|---|
| M1-Projekt Gitbaum `2c0b482...` | 127 Dateien im vollständigen rekursiven Baum verzeichnet; `results/synthetic` und bestehende Methodenberichte, **keine direkt sichtbaren PECD-/Hydro-/M0-Netzdateien** | Pfade zu originalen PECD-/Hydro-Sets, fünf WS-IDs, Netzdaten-Paket mit SHA256 |
| Projekt-ZIP `artifacts/bundles/IOSN_TYNDP2026_Revidierte_Berichte_und_PyPSA_Code.zip` (1,351,541 B) | Git-Blob `55100619175eda90303adca08ba1e934de4602ef`, **Binärinhalt nicht lesbar** | gegebenenfalls auspackbare Dateiliste/Hashes und Quellenklassifikation; **nicht als leer behauptet** |
| Projekt-ZIP `TYNDP_PyPSA_Methodenvergleich_Code_und_Implementierung.zip` (211,482 B) | Git-Blob `8d3990c3523acb345a58c7e05e18d7d6532e4167`; **nicht entpackt** | Inhaltsinventur optional, kann Real-Source-Gate nicht ohne Datenmanifest ersetzen |
| Projekt-ZIP `TYNDP_PyPSA_Methodenvergleich_FBMC_Codepaket.zip` (636,736 B) | Git-Blob `7d64ca104ee9c4fd7ccdec0302b3fca8b90feb3a`; **nicht entpackt** | Inhaltsinventur optional; Methoden-Codepaket nicht als Wetterzeitreihe akzeptieren |
| Offizieller [TYNDP-2026 Input-Katalog](https://2026.entsos-tyndp-scenarios.eu/download/) | Dokumentiert getrennte Downloads für **PECD**, **Hydro Inflow** und **Demand**; CC BY 4.0 für die dort veröffentlichten Daten mit Attribution „TYNDP 2026 Scenarios“ | angeforderte/erworbene Bytes, pro Datei SHA256, Release-Datum, Lizenz-/Nutzungsnachweis |
| Offizieller [PECD-Datensatz](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/PECD.zip) | URL publiziert, ZIP-Inhalt/Headers **nicht** ausgelesen | Wetter-ID-/Horizon-Spalten, Tech/Region, Anlage zugeordnet, QC, Datei-SHA256 |
| Offizieller [Hydro-Inflow-Datensatz](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/Hydro-Inflow.zip) | URL publiziert, ZIP-Inhalt/Headers **nicht** ausgelesen | HRR/HRI/HPI/HOL/HCL nach Datei, Intervallgrenzen/MWh, region→plant |
| Offizieller [Demand-Datensatz](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/Demand.zip) | URL publiziert, ZIP-Inhalt/Headers **nicht** ausgelesen | WS-Abdeckung je Horizont; nicht automatisch fünf volle WS |
| [Copernicus PECD v4.2](https://cds.climate.copernicus.eu/datasets/sis-energy-pecd?tab=documentation) | Dokumentierter Produkttyp und CDS-Zugang; **kein** tatsächlicher ORIG-/Regionmasken-Datensatz geladen | genaue Datenklasse/Version `fv`, Maskenmatrix, CRS, Zellindizes, SHA256, Lizenz der gelieferten Datei |
| Open-TYNDP `tyndp-2026` (fixierter SHA) | Quellcode und CSV-Datenledger **tatsächlich gelesen**, nicht dessen externe PECD-/Hydro-Archives | Sourcefiles und Records der benötigten fünf Projektdatensätze |
| M0-Produzent `0275f482...` + jüngerer Repair | Normative M0-DNR-/Sidecar-Spezifikation und Qualitätsregeln **gelesen** | reales `DetailedNetworkReference` inklusive NetCDF/Sidecar/Original-AssetIDs/Geoqualität und Hydromodell |

**Integritätsstatus:** Git-Objekt-Hashes bei lesbaren Quellcode- und ZIP-Blobs sind **SHA-1-Gitobjektkennungen**; sie dürfen nicht als SHA-256 der externen PECD-/Hydro-/M0-Eingangsdateien deklariert werden. Alle `source_sha256` in realen Pflichtprofilen sind aktuell `NOT_PROVIDED`.

## 2. Upstream Open-TYNDP / Versionsledger

| Textartefakt (fixierter Commit `71a3a9a...`) | Git-Blob | Beobachtung |
|---|---|---|
| `data/tyndp_versions.csv` | `2ef1578543952e631c0376d9ba95b4772dac991b` | `tyndp_2026` archiviert 2026-08-21 und 2026-10-07, `tyndp_pecd` 4.2 und Prebuilt 4.2+pre-built.0.1 (2026-08-13) |
| `data/tyndp_technology_map.csv` | `8a13a2f19bda72e5994a9b5873760253e5149754` | RES- und Hydro-Typvokabular; **nicht** auf echte M0-Generator-`carrier` geprüft |
| `rules/sb.smk` | `11312c3edbfc84b3b9a11b2510617eda3e4874ef` | `buses_tyndp`/`busmap_base_s_all.csv` ≠ CGMES-Originalbus; `get_wscenario_tyndp(...)[0]` unerlaubter Fünf-WS-Fallback |
| `scripts/sb/prepare_tyndp_pecd_release.py` | `f6da188247e00caf669d56eedc189caf1b52313e` | filtert CSV nach 10 Kopfzeilen `Date,Hour,WS###`, ungültige WS werden durch Intersektion still verworfen |
| `scripts/sb/clean_tyndp_pecd_data.py` | `f03149bbe88854b41f58464dae7fe1b31e1578bc` | TYNDP Node/Tech-Dateinamen, `Hour-1`, `GB↔UK`, `fill_gaps_method=zero/mean` möglich |
| `scripts/sb/build_renewable_profiles_pecd.py` | `eced56cd50ba42570570476b82429d4f658269cf` | `profile(time,bus,bin,year)`, horizon-fallback; `bus` ≠ M0 ID |
| `scripts/sb/clean_tyndp_hydro_inflows.py` | `a50c3dc5d1cf4004ea28c499052829ae4a5eb8f2` | `Hydro Inflows/{horizon}/...WS###`, `WEEK`/Tag, `ffill`, `/168`/`/24`, `fillna(0)` |
| `scripts/sb/build_tyndp_hydro_profile.py` | `1fe24515831db44df3dcff8debb7311a294a3282` | `inflow(time,bus,year,hydro_tech)`, hydro-`bus` ist TYNDP-Gebietskennung |
| `scripts/sb/build_tyndp_demand.py` | `42dc4a61728724cab75ce01aec9b4e6111f0f926` | je horizon 30 WS-Spalten, laut Kommentar nur **3** nicht-null-belegt |

**Releasestriktheit:** `2026-08-21` wurde laut Versionsledger zur Korrektur von Nachfrage, Hydro-Inflow, Wasserstoff, Leitungen und PEMMDB benutzt; `2026-10-07` wird dort als späteres vorläufiges Datenpaket geführt; `PECD 4.2+pre-built.0.1` ist ein separater vorbereiteter Auguststand. **Nicht automatisch zusammenführen oder als identisch zertifizieren.** Ein späterer Header-/Bytevergleich muss den tatsächlich eingesetzten Stand und Korrekturpfad entscheiden.

## 3. Weather-/Horizon-Metadaten ≠ externer 5-ID-Beleg

| TYNDP-2026-Zielhorizont | laut festem Reader belegte reguläre WS-Spalten | Status als fünf Projekt-Wetter-IDs |
|---|---|---|
| 2030 | `WS003 / WS021 / WS029` | `NOT_PROJECT_WITNESS` |
| 2035 | `WS032 / WS037 / WS059` | `NOT_PROJECT_WITNESS` |
| 2040 | `WS065 / WS071 / WS077` | `NOT_PROJECT_WITNESS` |
| 2050 | `WS091 / WS092 / WS106` | `NOT_PROJECT_WITNESS` |

Die vorhandene methodische IoSN-Wetterjahrauswahldokumentation behandelt ebenfalls die offiziellen Szenarien, **nicht** die vom Owner bereits separat festgelegte Fünferlieferung. Keine Neuauswahl oder implizite Zuordnung erlaubt.

## 4. Herkunfts-/Dateigates (pro echtem Eingangsfile)

Ein File-Witness muss `source_dataset_id; provider; product/version; original_filename+URI; byte_size; source_sha256; correction/release; license/access; planning_horizon; exact_weather_id; technology/variable; native_region_id+level; region_mask_file+mask_version; original unit/normalisation; timestamp/tz; interval_start/end; actual QC/missing` nachweisen. Zeitreihenwerte, zeitliche Vollständigkeit und Geometrie müssen **aus lesbaren Bytes** stammen. Geplante Dateinamenskonventionen und README-Header sind nicht gleich physischem Sample.

**Verdikt:** `GIT_TEXT_WITNESSED` für Upstream-Code und Versionsdatei, `PUBLIC_CATALOG_LOCATED` für offizielle Downloadseiten, `NOT_PROVIDED` für originäre reale Projektdateien und `BINARY_UNINSPECTED` für historische Projekt-ZIPs. Der Real-Data-Source-Witness bleibt `BLOCKED`.
