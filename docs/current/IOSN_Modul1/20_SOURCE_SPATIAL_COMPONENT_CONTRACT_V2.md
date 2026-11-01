# IoSN Modul 1 V2 — Quell-, Raster-/Regionen-, Asset- und Zeitreihenverträge

**Datum:** 2026-11-01  
**Status:** `CONTRACT_V2_DESIGNED / NATIVE_SOURCE_BYTES_NOT_QUALIFIED`  
**Autorität:** [00 kanonische Architektur](00_CANONICAL_ARCHITECTURE_V2.md) · [10 Wiederverwendung](10_UPSTREAM_REUSE_LEDGER_V2.md). Dies ist ein **logischer Sollvertrag**, keine Behauptung, reale Dateien lägen bereits vor.

## 1. Zwei unabhängige Inputfamilien; der Join gehört ausschließlich M1

| Netzinput (M0 oder anderer Provider) | Profile/Sources (PECD/Hydro/DFT) | Erst in M1 |
|---|---|---|
| `Network.buses`, `generators`, `loads`, `storage_units`, `stores`, `links`, Trafo-/Branch-Daten | Source-Profile mit \`time\`, \`weather_id\`, \`horizon\`, \`technology\`, \`region/pixel\`, Rohwert und Einheit | Source-/Profile-ID → **existierende** Generator-/Load-/Hydroport-ID |
| elektrische `Generator.bus`-/`Load.bus`-Anschlüsse, `p_nom` und `carrier` | PEON/P2ON/PEOF/P2OF/SZON/ORIG-Raster und offizieller Geo-/Ancillary-Masken-Katalog | qualifizierte Geografie-/Technology-/Kapazitätszuordnung, nicht neue Topologie |
| Bus-/ggf. Anlagen-Geokoordinate und Geoprovenienz/Quelle | PECD-Quellgeometrie mit CRS, Rasterlat/lon, fraktionalen Masken und Produktrelease | versionierter, auditiert räumlicher Crosswalk |
| Revision/Source-/ID-Provenienz oder M0-DNR-Sidecar | Dateihashes/Versions-/Rechte-/Szenario-/Intervallnachweis | gemeinsame Join- und Output-Provenienz, eigene Freigabegates |

**M0 MUSS NICHT:** PECD-, Hydro-, DFT-Regionen, PV-DC/AC-Verfügbarkeit, hydrologische Allokationsmatrix, WS-spezifische Zeitreihen oder landwirtschaftliche Exklusionsmasken produzieren. Wenn es Anlagenkoordinaten **nicht** liefert, ist das eine reale Geolokationslücke, die M1 aus einer extern qualifizierten Anlagendatenquelle beheben kann. Eine Elektro-Buskoordinate ist nur bei geprüfter physischer Repräsentativität zulässig.

Für eine konkrete M0-Lieferung mit CAN/2.0.0/DNR/1.0.0 können Felder `source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id`, `reference_id` und `source→view mapping` vorhanden sein. Das MA4F-Bridge-Schema bildet Legacy-`network_revision_id` **nur nach ausdrücklich genehmigter Semantik** auf `canonical_revision_id` ab, niemals still auf `projection_id` oder `source_revision_id`. Das ist M1-Schnittstellenqualifikation, nicht eine PECD-Pflicht von M0.

## 2. Source-Katalog als eigener Eingangsvertrag

**\`NativeSourceFile\` Pflichtmetadaten:**

- \`source_dataset_id\`, \`provider\`, \`product_version\`, \`file_revision\`, \`file_sha256\`, \`license/access_policy\`, \`source_path\`/kontrollierte URI;
- \`stream\` = `historical` / `projection`; \`climate_model\`, \`emission_scenario\`, \`energy_scenario\` und \`weather_id\` nur mit Originaldatenbezug;
- \`planning_horizon\` und \`source_climate_year\` sind **nicht austauschbare** Indizes; die fünf zuvor festgelegten IDs und ihre Horizonte sind in einem getrennten, extern freigegebenen Manifest aufzulösen;
- \`source_product\` = WON/WOF/SPV/CSP/HRR/HRI/HPI/HOL/DFT/other; \`technology_variant\` = spezifizierte Turbine/Hubhöhe/ResourceGrade oder PV-Typ/Tracking, ggf. Hydro-Porttyp;
- \`spatial_level\` = PEON/P2ON/PEOF/P2OF/ORIG/NUT0/NUT2/SZON/… **aus Quelldatei**, \`native_geometry_ref\`, \`crs\`, \`region_registry_version\` bzw. Rastertransformation;
- \`value_semantics\` = capacity_factor / generation_energy / natural_inflow_energy / load_power / meteorological; \`units\` = MW/MW, MW/MWp, MWh, MW usw.;
- \`source_time_axis\`, \`timezone\`, \`time_interval_bounds\`, \`native_resolution\`, \`missing_value_policy\`.

**Statische Quelle vs. echte Daten:** Ein Open-TYNDP-Skript, ein ECMWF-PUG, eine downloadbare ZIP-URL oder eine Schema-CSV ist **kein** Nachweis der verwendeten Originaldatenbytes. Quellen müssen separat nach Datei-/Mengen-/Metadatenprüfung als \`PHYSICAL_WITNESSED\` gelten. Die Stand-2026-11-01 MD1-Gates für tatsächliche Sourcebytes sind weiterhin `BLOCKED`.

**Unzulässige stillschweigende Fallbacks:** Open-TYNDP-Defaults `fill_gaps_method=zero`, Ersatz-Wetterszenario `[0]`, `safe_planning_horizon`, unbelegte Klimajahr-/Forecast-Substitution, normative Ersetzung fehlender Hydroquelle durch Null und Format-/Zeittyp-Casting ohne Protokoll. Ein echter gemessener Nullwert ist von einer fehlenden Datei zu unterscheiden.

## 3. Native Reader: regionales CSV und griddiertes PV-NetCDF sind zwei verschiedene Pfade

### 3.1 REGIONAL: PECD-WON/WOF und regionale PV

- Reuse MA2 `scripts/iosn_m1/res/adapter.py` für `TYNDP_RAW10_DATE_HOUR`, `TYNDP_DATE_HOUR` und `ISO_CSV`, erweitert nur um tatsächlich neue CSV-Header/Technologievarianten aus echten Dateien.
- Native Indexierung der Quelle: `(weather_id,horizon,source_profile_id,technology_variant,time)`.
- Pro Datei exakte `WS###`-Spalte und Code auf Quelldatum; alle stündlichen Werte finite und vor Source-Policy im Wertebereich, kein stilles `clip`.
- Bei Projektionen Wind `PEON/P2ON` bzw. `PEOF/P2OF`; **kein** impliziter ORIG-Wind-CF im Produktkatalog. Ein bereits regionaler CF bleibt meteorologisch regional, auch wenn er auf 1.000 Generatoren verteilt wird.

### 3.2 GRIDDED: offizielles PECD-SPV-`ORIG` (NEUER projektspezifischer Adapter)

**Einlesen:** `xarray.open_dataset` / `open_mfdataset` für tatsächlich gelieferte originale NetCDF-Dateien; aus Datei-Header und PUG:

- real vorgefundene Dimensionen und Variablennamen mappen (\`latitude/longitude/time\`, Technologie-/Modell-/Stream-/Szenario-/Level-Dimensionen nur soweit tatsächlich vorhanden); **nicht** ohne echten Datei-Header synthetische Dimensionsnamen als verbindlichen Iststand ausgeben;
- Gridzentren, Koordinatenorientierung, Zellbreite, Antimeridian, Domain/Maskierung, Fillvalue, CRS, CF units, PV-Technologie; Ziel \`NativePVGrid(time, grid_cell_id, technology_variant, weather_id,horizon)\`;
- gezieltes windowing/Chunking per vorhandene Anlagen-/Gebiets-Bounding-Box, Test gegen vertauschte lat-Achsen; bei mehreren NetCDF-Sources source-native Identität erhalten, keine unerklärte Doppelfüllung;
- PV-`ORIG` im offiziellen PECD v4.2 PUG 0,25°×0,25° ist **bereits CF MW/MWp**, nicht nur meteorologische Strahlung. Eine eigenständige Wiederberechnung mittels Atlite ist im Standardmodus unerwünscht.
- Originalwerte/Zeitachse/Maskenpässe über einen kleinen Source-Roundtrip verifizieren; kein ungeprüftes Mittel über vier benachbarte Pixel, keine glättende Wetterinterpolation.

**Source-Ausgabevertrag:** `native_cf_catalog` und `native_cf(time,source_profile_id,technology_variant)`. Für ORIG ist `source_profile_id` eine deterministische **grid_cell_id mit originalem Raster/CRS/Dateiversion-Anker**; für REGION eine versionsgebundene PECD-Regions-ID.

## 4. Offizielle PECD-Regionmasken (NEUER kleiner Reader)

Das PECD-PUG Kap. 4.2/4.3 beschreibt NetCDF-`mask(region,latitude,longitude)` mit **fraktionalem Flächenanteil** je Zelle, beispielsweise `ANCI_PEON-mask_PECD4.2_fv1.nc`, `ANCI_P2ON-mask_PECD4.2_fv1.nc`, analog PEOF/P2OF, SZON, NUT2. Manche originale Shapefiles sind nicht öffentlich; GeoJSON ist daher **kein garantierter nativer Eingabestandard**.

- Native Masken-NetCDF und originale \`region\`-IDs, Rasterbasis, Orientation, Maskenwerte in [0,1], Küsten-/Grenzzellen, Version und Hash lesen; metadata zur vorher erzeugten Energy-Source-Regions-ID abgleichen.
- Bevorzugte deterministische Zonenwahl: **explizite Source-Zonen-ID**, danach genau eine belegte Anlagenort→Produktregion-Zuordnung. Bei einer Zelle mit zwei fraktionalen Regionsmasken ist der Anteil **kein** gesicherter Point→Region-Beweis; maschinenlesbar \`AMBIGUOUS\` markieren oder ergänzende echte Geometrie-/TSO-Regionzuordnung verlangen.
- Wenn qualifizierte Polygone verfügbar sind, `geopandas.sjoin` bzw. `shapely.covers` verwenden. Originalregionmasken dürfen in GeoJSON/polygons **nur** per dokumentierter Geometrieableitung mit eigenem Accuracy-Witness gewandelt werden; nicht als verlustfreie Authentizität behaupten.
- Eine Zellenüberlappung aus Atlite `indicatormatrix` oder ein PECD-fraktionales Landflächen-Gewicht ist **nicht** automatisch Kapazitätsgewicht einer in mehreren Wetterregionen bestehenden Generatorgruppe.

## 5. Automatischer Profile→bestehende Anlage Spatial Join (NEUES deterministisches Modul)

### 5.1 Eingangsstruktur

**\`ExistingAsset\`:** \`existing_component_id\`, \`source_asset_id\` (falls vorhanden), \`component_class\`, \`bus_id\`, \`carrier\`, \`technology_variant\`, \`p_nom_mw\`, \`source_grid_revision\`, optional \`real_plant_lon/lat/crs\`, \`bus_lon/lat/crs\`, \`geo_quality\`, \`is_synthetic_bus\`, \`offshore_park_location/landing_bus\`, \`pv_dc_mwp\`/AC-Basis, \`composite_subplant_capacity_mw\`.

**\`Profile\`:** \`source_profile_id\`, \`source_dataset_version\`, \`spatial_level\`, \`region_id\` oder \`grid_cell_id\`, \`technology_variant\`, \`time_index\`, \`units\`, \`source_hash\`.

### 5.2 Methodenrangfolge und Abnahme

| Methode | Fall | PASS-Bedingung |
|---|---|---|
| \`DIRECT_VERIFIED_PROFILE_LINK\` | Reale Anlagen-ID hat autoritativ zugeordnete PECD-Profil-ID | gleiche Quellversion/Technologie/Horizon, source evidence vorhanden |
| \`PLANT_POINT_TO_ORIG_CELL\` | PV-ORIG-Grid und reale Anlagenposition | Koordinate im gültigen Rasterpixel, passende PV-Typologie/Einheit/Maskstatus und eindeutiger Zellindex |
| \`PLANT_POINT_TO_PECD_REGION\` | On-/Offshore-Windregionalprofil oder regionale PV | amtliche Regionsmaske/Polygon/eindeutige TSO-Zuordnung, realer Anlagenstandort |
| \`VERIFIED_BUS_COORDINATE_PROXY\` | kein Plant-Point; Netzbus ist nachweislich repräsentativ | dokumentierter Proxy, kein Offshore-Landfall und kein synthetischer Sternbus |
| \`CAPACITY_WEIGHTED_MULTIREGION\` | ein *bereits bestehendes* Sammel-Generatorobjekt deckt echte Anlagen in verschiedenen Regionen ab | belegte \`MW/MWp\` je Unteranlage, Gewichte summieren 1, entsprechend Normierungsbasis |
| \`UNRESOLVED\` | keine verlässliche Eindeutigkeit, fehlende Geo-/Technologie-/DC/AC-Evidenz | BLOCK, Eintrag im Source-/Spatial-Error-Ledger; kein unkontrollierter nearest-centroid |

**Ausgabe:** deterministischer `asset_profile_map_v2.parquet/csv`, Schlüssel `(grid_revision,horizon,component_id,source_profile_id)`, \`assignment_method\`, \`spatial_level\`, \`source_resolution\`, \`weight\`, \`source_bytes_hash\`, \`region_mask_hash\`, \`geo_evidence\`, \`quality\`, \`error_code\`. MA2-V1-Mappingtabellen im Schemaadapter weiterlesbar; ihre **Validierungsfunktion** bleibt als nachgelagerte Prüfung erhalten.

### 5.3 Mathematik, Normalisierung

Für bestehenden Generator `g` und Quellenprofile `p` wird ohne Erzeugeraggregation definiert:

\[
a_{gp}\ge0,\quad \sum_{p}a_{gp}=1,\qquad CF_g(t)=\sum_pa_{gp}CF_p(t).
\]

Bei PV MW/MWp muss die verwendete \`a\`-Gewichtung auf PV-\`DC_MWp\`-Anteile statt ungeprüft auf AC-MW bezogen sein. Anschließend `P^{avail}_{g}(t)=p^{nom,AC}_g\,CF^{AC}_g(t)` nur nach dokumentierter Wechselrichter-/Clipping-Policy. Bei Wind ist CF normalerweise `MW/MW` und keine weitere erfundene Standortauflösung zu behaupten.

**Kerninvariante:** `original_generator_id`, `n.generators.bus`, `n.generators.p_nom` unverändert. Wenn 100 elektrische Anlagen dasselbe regionale Windprofil erhalten, bleiben sie 100 Anlagen. Die Source-Distanz-/Korrelationsauflösung bleibt regional.

## 6. Hydro: Native Source und hydraulischer Join strikt getrennt

**Quellinput ohne Netz:** `(source_region SZON,hydro_tech,weather_id,horizon,interval[t0,t1),E_MWh,unit,source_file_sha)`. Typen `HRR` RoR, `HRI` Reservoir, `HPI` Pondage, `HOL` open-loop pumped; `HCL` als tatsächlich vorhandene closed-loop Speicherklasse **nicht** automatisch natürliche Quelle. `HRG/HRO/HPO` Generation nicht mit Inflow verwechseln.

**Join:** hydrologisch belegte Zuordnung `B[existing_hydro_asset,source_region,tech]` aus Basin-/TSO-/realem Wasserfluss-/Anlagenschlüssel, nie aus alleiniger Distanz zum Elektro-Bus. Bestehendes `StorageUnit` erhält `storage_units_t.inflow`; vorhandener RoR-`Generator` ggf. `generators_t.p_max_pu` mit nachgewiesener Normierung; `Store/Link`-Spezialport nur mit M0-Owner-Schnittstellen-/Source-Policy.

**Erhaltung:** erst \`source MWh\`→zugeordnete **native** Quellenergie pro Originalintervall, dann mit belegtem \`c[hydro_asset]\` Modell-Energie und \`∑_t inflow_MW(t) Δt\` prüfen. Native Wochen-/Tagesgrenzen, Schaltjahr, Teilwoche, Zeitzone exakt. Uniforme Stundenwerte sind dokumentierte Intervallsynthese, keine meteorologische Stundenmessung.

**Reuse:** MA3 `scripts/iosn_m1/hydro/adapter.py`, `normalize_tyndp2026.py`, `rules/iosn_m1_hydro.smk` unverändert, sofern Tests und echte Datenpassung vorliegen; keine komplette neue Hydro-Pipeline.

## 7. Nachfrage/DFT: separater Datenstrom, gleicher vorhandener Load-Target-Vertrag

Falls es nur PECD-Wind/PV und Hydro zu ergänzen gilt und reale `loads_t.p_set` schon unabhängig zulässig geladen wurden: **keinen neuen Last-Adapter aktivieren**. Wenn die regionalen TYNDP-/DFT-Stundenlasten noch auf die **bestehenden** elektrischen Lasten verteilt werden müssen:

- \`demand_source_catalog\` mit \`weather_id,horizon,time,source_region,MW,source_hash,license\`;
- \`load_distribution_map\` mit \`existing_load_id,source_region,documented_fraction,evidence\` und je Quelle komplette Anteilssumme =1;
- `n.loads_t.p_set` nur in einem klar autorisierten dynamischen Komponiermodul belegen; keine neuen Lasten erzeugen oder Originalbusse verlagern;
- regionale/räumliche und stündliche Summen erhalten und national/gebietsübergreifende Doppelzählungen verhindern;
- TYNDP/DFT kann Lasten mit PECD-Wetterjahr korrelieren, aber ist **nicht** automatisch aus PECD-Solar-/Wind-CF berechenbar.

Reuse PyPSA-Eur `scripts/build_electricity_demand_base.py` (regionale Disaggregation über Population/GDP) und Open-TYNDP `scripts/sb/build_tyndp_demand.py` (Quellreader), **nicht** `cluster_electricity_demand` vor M2.

## 8. Gemeinsamer Writer / Export-Vertrag (MA4F statt neuer Composer)

**MA4F ist die einzige autorisierte Target-Write-Stelle.** Existierende Funktion `scripts/iosn_m1/compose.py` bindet `renewable_cf` und Hydrooutputs auf exakte M0-/PyPSA-IDs. Nach V2-Erweiterung erhält sie den automatisch erzeugten Join und optional Demand-Zeitreihen.

| Vorhandene Komponente | Dynamischer Zielwert | Zulässiger Writer |
|---|---|---|
| `Generator` mit Wind/PV | `generators_t.p_max_pu` | RES-Mapping-Ergebnis |
| `Generator` mit RoR | `generators_t.p_max_pu` | Hydro-Ergebnis, **disjunkt** zu Wind/PV |
| `StorageUnit` mit Reservoir/Teich/PHS mit natürlichem Zufluss | `storage_units_t.inflow` | Hydro-Ergebnis |
| `Load` | `loads_t.p_set` | DFT/TSO, nur wenn aktiviert und Source-/Overwritepolicy qualifiziert |
| `Store + Link` | **kein** natives Store-inflow-Attribut | nur vorhandener genehmigter Zusatzport und explizite dynamische Whitelist |
| Andere/Conventional | keine Übernahme ohne zusätzlichen Quellvertrag | Default = unverändert |

**Statisch:** alle 16 PyPSA-Static-Komponententabellen inklusive Netztopologie und Original-Assetparameter vor, während und nach PyPSA-NetCDF-Export/Reimport nach bestehendem MA4F-Fingerprint prüfen. PyPSA 1.4 kann reine Default-valued Dynamic Columns beim Export weglassen; semantischer Gleichheitswitness nur bei exaktem Default und unveränderter Statik zulässig.

**Zeit:** exakte fünf fixierte \`weather_id\`, stündlich in UTC; vor PyPSA `timezone-naive UTC`, UTC im Manifest; kein \`set_snapshots\`-Default-Fill ohne vorgängigen vollständigen Source-Coverage-Check.

**Outputs:** vollständiges `detailed_reference_{horizon}_{weather_id}.nc` + `source_manifest` + `native_cf_catalog` + `asset_profile_map` + `hydro_allocation` + `load_distribution_map` (falls aktiv) + `target_ownership` + `static_fingerprints` + `qa_evidence`. Technische Abschnitte unabhängig von CGMES-Importer-Dateiformaten.

## 9. Praktische Folgen für die Makroausführung

- **Native PECD + automatische spatial association** ist **eine** konsolidierte Weiterentwicklung von MA2/MA4F, keine Änderung an M0 und kein eigener PyPSA-Core-Branch.
- **Regionale Wind-CF** mit dem vorhandenen CSV-Reader und Source-Region-Mapper; **ORIG-PV** mit neuem xarray-NetCDF-Reader plus grid-cell mapping; offizielle fraktionale Masken als NetCDF lesen, nicht nur aus vorgefertigtem GeoJSON.
- **MD1 / echte Quellen**: Quelle selbst kann unabhängig vom M0-Netz verifiziert werden. Ein physisch bestehendes PECD-ORIG-PV-NetCDF belegt aber erst nach realem Join und Writer-Gates das komplette M1-Referenzmodell.
- **MA4R Realbetrieb** erst nach getrenntem `S-PECD`, `S-HYDRO`, `N-M0`, `J-M1` PASS und unabhängiger Abnahme. Sonst Fixture-PASS klar getrennt erhalten.

**Qualifikationspolitik und Makroübergaben:** [30_WORKFLOW_AND_QUALIFICATION_V2.md](30_WORKFLOW_AND_QUALIFICATION_V2.md), [40_NEXT_MACROS_AND_HANDOFFS_V2.md](40_NEXT_MACROS_AND_HANDOFFS_V2.md).
