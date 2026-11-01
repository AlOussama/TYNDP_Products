# MD1 — PECD-native Profile, Raummasken und unabhängige Source-Evidenz

**Wichtig:** Dieser Katalog hat **absichtlich keine** `m0_asset_id`, `generator_id`, `bus_id` oder CGMES-Netzreferenz. PECD ist eine eigenständige raum-/zeitbezogene Datenquelle. Der elektrische Join wird separat in `M1_JOIN_READINESS.csv` qualifiziert.

**Offizielle Quellen:** [ECMWF PECD 4.2 PUG](https://confluence.ecmwf.int/spaces/CKB/pages/540941752/Climate+and+energy+related+variables+from+the+Pan-European+Climate+Database+derived+from+reanalysis+and+climate+projections+v4.2+Product+user+guide+PUG); [CDS-Produkt](https://cds.climate.copernicus.eu/datasets/sis-energy-pecd); [TYNDP-2026-Download](https://2026.entsos-tyndp-scenarios.eu/download/); [Open-TYNDP 2026 Versionstabellen](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/data/tyndp_versions.csv) und [Tech-Map](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/data/tyndp_technology_map.csv).

## 1. Produktklassen (keine tatsächlichen Projektdateien)

| PECD Variable | Native Zeit-/Wertsemantik | Regionengröße und Dateityp | Reiner PECD-Source-Gate |
|---|---|---|---|
| `WON` Onshore | stündliche Wind-Generation-CF, `MW/MW` | `PEON`, `P2ON`, Region/Tech, regionales CSV | tatsächliche Dateien/WS/Horizon/Regionen und Techvariante belegen |
| `WOF` Offshore | stündliche Wind-CF `MW/MW` | `PEOF`, `P2OF`, regionales CSV | tatsächliche Offshore-Regioncodes/Maskenversion/Quellvarianten, keine Landbus-Info nötig |
| `SPV` Solar | stündliche CF `MW/MWp` | `ORIG` gridded NetCDF ca. 0.25°; `NUT0/NUT2/SZON/PEON/P2ON` regional CSV | echte Quelle: Raster oder Region, Technologievarianten, PV-Wertbasis/Einheit |
| `HRR/HRI/HPI/HOL` | native hydrologische Source-Energie, typischerweise Wochen-`MWh`; Quellgebiet `SZON` | PECD-Produkt vs TYNDP-2026-Hydro-Input **separat** versionieren | echter Source-Typ/Intervalle im Hydro-Ledger, nicht elektrische Anlagen |
| `HCL` | closed-loop/pure pumped-storage als TYNDP-Technologieklasse | nicht automatisch ein natürliches PECD-Inflow-Produkt | `NOT_APPLICABLE_BY_DESIGN` erst nach anlagen-/quellenbezogener Begründung, keine Null-Datei erzeugen |

Die PECD-Klimadatenbasis besteht aus historischen ERA5- und projizierten CMIP6-Streams. `planning_horizon`, `climate_model`, `climate_year`, `emission_scenario` und `weather_id` sind voneinander zu unterscheiden. Der externe fünf-ID-Entscheid wird **nicht** durch die im Open-TYNDP-Code dokumentierten drei TYNDP-2026-Standard-WS je Horizont ersetzt.

**Horizon-WS in Open-TYNDP 2026 (nur Reader-Hinweis):** 2030 `WS003/WS021/WS029`; 2035 `WS032/WS037/WS059`; 2040 `WS065/WS071/WS077`; 2050 `WS091/WS092/WS106`. Diese zwölf Bezeichner über mehrere Horizonte sind **keine vom Owner belegten fünf Projekt-IDs**.

## 2. Masken und räumliche Auflösung

Die PECDv4.2-PUG beschreibt offizielle **floating-point NetCDF-Regionmasken** mit `mask(region,latitude,longitude)` auf dem zugrunde liegenden 0.25°-Gitter, Werte 0–1 als Flächenfraktionen. `PEON` und `P2ON` sowie `PEOF` und `P2OF` sind **verschiedene** Regionssysteme, nicht alternative IDs derselben Geometrie. Die offiziellen, zur Herstellung benutzten Shapefiles sind teilweise nicht öffentlich; der CDS bietet die dokumentierten Masken als Downloadprodukt. GeoJSON in MA2 ist **nicht** automatisch identisch mit diesen fractional masks.

**Quellnative Validierung ohne CGMES:** Masken-Bytehash + PECD-Dateiversion `fv` + Koordinaten-/Regionachsen + CRS/Koordinatenkonvention + Null-/Überlappungen + Regioncode-Registry + produktbezogene Version/Revisionshistorie. Ein Regionmasken-Pixelanteil ist **nicht** der Installationsleistungsanteil eines späteren M0-Generators; diese MW-Gewichte gehören erst in den Asset-Join.

**PECD 4.2 Data Corrections:** Offizielle PUG dokumentiert u.a. `fv2`-Reprozessierungen für betroffene projizierte Winddaten (`WON/WOF`) und weitere Variablen. Deshalb `PECD4.2` als alleiniger Versionsstring **nicht ausreichend**: je tatsächlich gelieferten Datensatz `fv1/fv2`, Model/Scenario, Korrekturdatum und Datei-SHA256 bestimmen. Der Open-TYNDP-Prebuilt `4.2+pre-built.0.1` (2026-08-13) ist nicht automatisch inhaltlich gleich mit später korrigierten TYNDP-2026-Files (2026-08-21/2026-10-07) oder CDS fv2.

## 3. Quellnative Zeit-/Unit-/Dateiwitnesses

- PUG: Gridded `ORIG`/ggf. `BIAS` NetCDF; aggregierte Regionprodukte CSV. Stündlicher Wind/PV-CF ist **Verfügbarkeitsprofil**, kein Netzeinspeise-Dispatch. PECD enthält keine aus M0 abgeleiteten Generatoren oder elektrischen Anschlussknoten.
- TYNDP-2026 ZIP-/Prebuilt-Reader: `Date`, `Hour` 1–24 und `WS###` in regionalen Dateien. `TYNDP_NODE` ist eine externe Zonenkennung, kein PyPSA Bus, kein direkter `WON/WOF/SPV`-Profil-Beweis für jedes Projektasset.
- Genauer Quellzeitstempel: Zeitzone, Kalender, Stundenorigin, native Leap/DST-Behandlung, exakter Dateibereich, Missing und Korrekturversion an tatsächlich gelesenen Bytes belegen; kein `fillna(0)`, `ffill`, `safe_planning_horizon` oder `get_wscenario_tyndp(...)[0]` als Ersatz.
- Solar `MW/MWp` ≠ `MW/MW_AC`. Die **Quellsemantik** wird hier unabhängig geprüft; erst der spätere Anlagen-Join prüft die M0-`p_nom`-Basis und ggf. genehmigten Inverter-/Clipping-Contract.
- Keine künstliche meteorologische Verfeinerung aus PEON/P2ON nach originalem Bus. `ORIG`-Solar-CF gibt nur die tatsächlich vorhandene Rasterauflösung an, nicht eine daraus abgeleitete Anlagensimulationsgenauigkeit.

## 4. Ergebnis

`S-PECD-CATALOG=PASS_STATIC_CATALOG_ONLY`, `S-PECD-PHYSICAL=BLOCKED_NOT_WITNESSED`. Tatsächliche vorselektierte Projektwetter-IDs=0/5; originale Wind/PV-Dateien=0; Regionenmasken-NetCDF mit SHA256=0. Diese Einstufung gilt **unabhängig** von der M0-Referenzentwicklung.
