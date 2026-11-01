# IoSN Modul 1 V2 — Upstream-Reuse-/Delta-Ledger (PyPSA, PyPSA-Eur, Atlite, Open-TYNDP)

**Datum:** 2026-11-01  
**Status:** `SOURCE_VERIFIED_STATIC / NO_UPSTREAM_CORE_CHANGES`  
**Normativer Architekturanker:** [00_CANONICAL_ARCHITECTURE_V2.md](00_CANONICAL_ARCHITECTURE_V2.md)  
**Richtlinie:** Wiederverwendung existierender Algorithmen/Schnittstellen **vor** neuer Implementierung; kein erneuter Ansatz für PyPSA-Core, keine Doppelimplementierung des MA4F-Composers und keine Übernahme des Open-TYNDP-Regionalnetzes als CGMES-Netz.

## 1. Eingefrorene Source-Pins / Beweisumfang

| Repository | Geprüfter Commit/Branch | Rolle und tatsächliche Einschränkung |
|---|---|---|
| [PyPSA/PyPSA](https://github.com/PyPSA/PyPSA/tree/23650353eb1d059acfec28f4915ad3e068c085bf) | `master@23650353eb1d059acfec28f4915ad3e068c085bf` (2026-10-30) | Komponenten, Snapshots, dynamische Serien, NetCDF, Optimierung/AC-PF. **Kein PECD-Importer und kein nativer PECD-zu-Anlagen-Mapping-Service nachgewiesen.** |
| [PyPSA/pypsa-eur](https://github.com/PyPSA/pypsa-eur/tree/1526bb820e25a9faa61f32b00bfc77dd05db6b2e) | `master@1526bb820e25a9faa61f32b00bfc77dd05db6b2e` (2026-10-28) | Energie-Datenpipeline, Atlite/ERA5-/SARAH-Konversion, Lastaufschlüsselung, Geo-/Regionenverarbeitung, Profil-NetCDF, Snakemake |
| [PyPSA/atlite](https://github.com/PyPSA/atlite/tree/0d4ff8f703a99566b475b8d775aa2e74309123ee) | `master@0d4ff8f703a99566b475b8d775aa2e74309123ee` (2026-10-15) | Raster-/Polygon-/Sparse-Geografie, optional meteorologische Energie-Konversion; **Land-Eligibility ist nicht PECD-Zeitreihenverfügbarkeit** |
| [open-energy-transition/open-tyndp](https://github.com/open-energy-transition/open-tyndp/tree/71a3a9a15b77114cd79458bceabc98e1a64dd58a) | `tyndp-2026@71a3a9a15b77114cd79458bceabc98e1a64dd58a` (2026-10-29) | PECD-v4.2-/TYNDP-2026-Datenreader, regionale CF-, Hydro-/Demand-/PEMMDB-Schemas und Dateien; **TYNDP-Knoten statt CGMES-Generator-IDs** |
| Open-TYNDP `master` | `5b25904496150b889b321dd8d76f393ef09a0f2e` | ältere PECD-/TYNDP-2024-Reader als historische Referenz; **nicht** Hauptimplementierungsanker |
| [IoSN MA-2](https://github.com/AlOussama/TYNDP_Products/blob/11700baa8df8cafc6bd71b96998f8b2bca647ca0/scripts/iosn_m1/res/adapter.py) | `11700baa8df8cafc6bd71b96998f8b2bca647ca0` | **existierender** regionaler CSV-/ISO-Source-Reader + manuelles Mapping-Validator, 20 lokale Fixture-Tests |
| [IoSN MA-3](https://github.com/AlOussama/TYNDP_Products/blob/b3b9bf133d1b5c968323a31f8ac76090f1f2e182/scripts/iosn_m1/hydro/adapter.py) | `b3b9bf133d1b5c968323a31f8ac76090f1f2e182` | **existierender** Hydro-Native-Intervall-Reader, Energieallokation/Storage-Port-Zuordnung, Fixture-Tests |
| [IoSN MA-4F](https://github.com/AlOussama/TYNDP_Products/blob/1ab3eb1aed54975e69586cc3d958a24d97a6288f/scripts/iosn_m1/compose.py) | `1ab3eb1aed54975e69586cc3d958a24d97a6288f`; getesteter Code SHA `cd71f36ddf07fb3ecc1cb4be5701a2586b9950c8` | **vorhandener integrierter Composer** mit 92 Pytest-PASS, 16 Snakemake-Fixture-Jobs und fünf synthetischen NetCDF-Roundtrips. Nicht neu schreiben. |
| [IoSN MD-1](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/EXECUTION_REPORT.md) | `5c68198984b6f2f430a49ff3e23d17c0b27320e1` | native Source-Kataloge; physische PECD-/Hydro-/M0-Pakete nicht geliefert |

## 2. PyPSA-Core: nutzen, nicht verändern

| Datei/öffentliches Objekt | Vorhandene Funktion | M1-Verwendung |
|---|---|---|
| [`pypsa/network/index.py`](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/index.py) — `set_snapshots` | Zeitindex und dynamische DataFrames; PyPSA erwartet timezone-naive DatetimeIndex | pro Wetter-ID auf eine geprüfte **UTC-naive** Stundenachse; **vorher** Source-Vollständigkeit prüfen, da Reindex Defaultwerte auffüllen kann |
| [`pypsa/network/transform.py`](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/transform.py) — `Network.add` | Generator/Load/Storage mit Zeitreihen erzeugbar | für **Tests/Fixtures**, nicht zur erneuten Anlage vorhandener M0-Generatoren in M1 |
| [`pypsa/network/io.py`](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/io.py) — `_import_series_from_df`, NetCDF IO | DataFrames mit `snapshots × component names`; Import kann fehlende Serien auf Default auffüllen; `export_to_netcdf` | ausschließlich der MA4F-Writer mutiert dynamische Attribute; Real-Witness und Roundtrip |
| [`docs/user-guide/design.md`](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/docs/user-guide/design.md) | `generators_t.p_max_pu` als Availability, Vorrang gegenüber statischem Wert | Wind/PV und RoR Zielattribut; keine eigene Core-Klasse |
| PyPSA `n.loads_t.p_set`, `n.storage_units_t.inflow` | Last-/Speicherzufluss als reguläre Zeitserien | DFT/TSO-Load-/Hydro-Ausgabe |
| [`pypsa/geo.py`](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/geo.py) | `haversine`, `haversine_pts`, `compute_bbox`, CRS-/Projection-Hilfen | geografische Basishilfen, **nicht** vollwertiger Source-Product→Original-Asset-Mapper |

**Core-Fazit:** Es gibt **keinen Bedarf** für einen neuen PyPSA-Core-Wetteradapter oder eine Änderung an `n.optimize()`/`n.lpf()`/`n.pf()`. PyPSA-NetCDF-Default-Elision ist im vorhandenen MA4F-Composer bereits semantisch geprüft; niemals künstlich nicht-default Werte einfügen, nur damit Dateien Spalten enthalten.

## 3. PyPSA-Eur: genaue Wiederverwendungs- und Ausschlussentscheidung

| Upstream Modul/Regel | Datenrolle | Entscheidung für native PECD, vorhandene Netzkomponenten |
|---|---|---|
| [`rules/build_electricity.smk`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/rules/build_electricity.smk): `build_cutout` | ERA5-/SARAH-Atlite-Wetterfelder | **SKIP wenn native fertige CF**; optional für separate meteorologische Neuberechnung |
| [`scripts/determine_availability_matrix.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/determine_availability_matrix.py) | Anteil der **für Neuinstallationen geeigneten Landfläche** in Rasterzellen | **NICHT** als stündliche CF oder bereits vorhandene Anlagenverteilung interpretieren; für bestehende Generatoren meistens SKIP |
| [`scripts/build_renewable_profiles.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_renewable_profiles.py) | `profile(year,bus,bin,time)` + `p_nom_max(bus,bin)` + `average_distance(bus,bin)`; Atlite erzeugt CF je Cutout-Pixel und gewichtetes Regionsprofil | **Format/Orchestrierung/technische Zuordnungsidee REUSE**; native PECD-CF **nicht erneut** in Atlite nachrechnen, standardmäßige regionalisierte `bus,bin`-Ausgabe **nicht** ungeprüft als Original-Generator-ID interpretieren |
| [`scripts/build_electricity_demand.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_electricity_demand.py) | nationale Lastzeitleisten, Quellen-/Lückenbehandlung | selektiv Reader-/Metadatenprinzipien; automatische Gap-Fills nur bei explizit genehmigter Source-Policy |
| [`scripts/build_electricity_demand_base.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_electricity_demand_base.py) | Verteilung von National-/NUTS3-Last auf Netzregionen (GDP, Bevölkerung, andere Faktoren) | **wiederverwendbares Verfahren** für gesonderten Demand→vorhandene Load-IDs-Adapter; Quell-/Lastanteile und vollständige MW-Summe prüfen |
| [`scripts/cluster_electricity_demand.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/cluster_electricity_demand.py) | nachträgliche Summierung auf geclusterte Busse | **NICHT** vor vollständiger M1-Zuordnung; gehört in M2 |
| [`scripts/build_hydro_profile.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_hydro_profile.py) | ERA5 Runoff × Länderformen, normiert mit EIA-Statistik | Modellbeispiel/Format, aber **nicht** PECD/SZON-Wochen-Inflow als unveränderte Quelle; **MA3 native Hydro-Reader nutzen** |
| [`scripts/add_electricity.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/add_electricity.py) — `attach_wind_and_solar`, `attach_load`, `attach_hydro` | legt `Generator`, `Load`, `StorageUnit` neu an und füllt dynamische Werte | **nicht unverändert ausführen**, weil M0 bereits sämtliche Originalanlagen besitzt; **nur Attribute-/Semantikprinzip** |
| [`rules/compose.smk`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/rules/compose.smk) / [`scripts/compose_network.py`](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/compose_network.py) | `networks/clustered.nc` → neue Komponenten, Kosten, Sektoren, Brownfield, Vorbereitung zur Lösung | **nicht** auf ein fertig bestehendes detailliertes M0-Netz anwenden; eigener **kleiner** M1-Zeitreihen-Composer MA4F bereits vorhanden |
| `simplify_network` / `cluster_network` | Vereinfachung/Netzaggregation | **M2 only**; nicht für M1 |

**Unterschied zweier Modi:** Für einen **gewöhnlichen**, von PyPSA-Eur neu aufgebauten Energieträger-/Planungsnetzlauf könnte man ein kompatibles `profile_{tech}.nc` mit `p_nom_max` und `average_distance` vorab bereitstellen und `add_electricity` weiterlaufen lassen. Das **verändert die Generatorstruktur** und ist **nicht** unser M1-Default auf einem bereits detaillierten Netz. Die Kategorie „PyPSA-Eur-Kompatibilitätsmodus für neue Kraftwerke“ bleibt optional und gesondert zu beauftragen.

## 4. Atlite und Geospatial Dependencies

| Modul/API | Technische Bedeutung | Reuse-Policy |
|---|---|---|
| [`atlite.Cutout.indicatormatrix`](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/cutout.py), [`atlite.gis.compute_indicatormatrix`](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py) | Polygon-Schnittmatrix, **Flächenanteil** der Quelle innerhalb der Zielregion | verwenden, **wenn** reales Grid/Polygon vorliegt und Schnitt-Definition fachlich passt; Matrix nicht automatisch für MW-Kapazitätsanteile benutzen |
| [`atlite.gis.compute_availabilitymatrix`](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py) | Fläche, die nach Exklusionen für Bau neuer Energieanlagen geeignet ist | nicht mit PECD-`p_max_pu` verwechseln, für vorhandene Generatoren i.d.R. unnötig |
| `xarray.open_dataset`, `open_mfdataset`, `sel/isel`, Dask-Zeitchunks | native NetCDF-Variable `time × latitude × longitude × technology/model`; Datenformat je echtem PUG-File zu prüfen | **neuer kleiner native `ORIG` Reader**, nicht als Atlite-Cutout-Typ missbrauchen |
| `geopandas.GeoDataFrame.sjoin`, `shapely`, `pyproj.Transformer` | reale Anlagenteile mit PECD-Region-/Pixelgeometrie joinen | **automatischen** Mapper erzeugen; Quellqualität, CRS, Boundary/Overlap/Offshore-Tests |
| `numpy`/`scipy.sparse` | sparsame Zuordnungsgewichte `A[g,profile]`, Kapazitätsverteilungs- und Aggregationswitness | optionale Sparse-Implementierung für größere Portfolios |

Atlite ist eine **methodisch geeignete Geo-Bibliothek**, aber zum Lesen des griddierten PECD-PV-`ORIG`-Produkts genügt oft xarray mit sauberem Rasterindex. Atlite-Wind-/Solar-Konverter nur dann einschalten, wenn die offizielle, bereits berechnete CF **nicht** verwendet werden soll und ein eigener physikalischer Modellvertrag genehmigt wurde.

## 5. Open-TYNDP 2026: native Quellparser wiederverwenden, TYNDP-Busannahmen verwerfen

| Datei am [`tyndp-2026`-Commit](https://github.com/open-energy-transition/open-tyndp/tree/71a3a9a15b77114cd79458bceabc98e1a64dd58a) | Verifizierte Funktion | Entscheidung |
|---|---|---|
| [`rules/sb.smk`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/rules/sb.smk) | `retrieve_tyndp_pecd`, `prepare_pecd_release`, `clean_tyndp_pecd_data`, `build_renewable_profiles_pecd`, Hydro-/Demand-/PEMMDB-Regeln | **Reuse DAG-Idee**, selektiv, aber M1-Native-CF-Produktart/-Auflösung separat konfigurieren |
| [`scripts/sb/prepare_tyndp_pecd_release.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/prepare_tyndp_pecd_release.py) | PECD prebuilt/WS-Spalten und native Source-Namen | CSV-Metadaten-/Szenario-Parser reuse, nicht 3→5 oder Re-Selection |
| [`scripts/sb/clean_tyndp_pecd_data.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py) | `Date`/`Hour` + `WS###` aus node-indexierten regionalen CF-Dateien | **regionaler CSV-Pfad**, aber `buses_tyndp`/TYNDP-Nodes **nicht** mit Original-CGMES-Assets gleichsetzen; keine automatische `fill_gaps_method=zero` |
| [`scripts/sb/build_renewable_profiles_pecd.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_renewable_profiles_pecd.py) | Ergebnis `profile(year,bus,bin=0,time)` | reine Datensatzstruktur/NetCDF-Konvention; keine native `ORIG`-PV-Pixel-Zuordnung implementiert |
| [`scripts/sb/clean_tyndp_hydro_inflows.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_hydro_inflows.py), [`build_tyndp_hydro_profile.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_hydro_profile.py) | hydro TYNDP-Zone, Tages-/Wocheneinheiten, NetCDF | **MA3** übernimmt Schema-/Methodikideen; keine impliziten `/168`-/`ffill`-/Nullwerte ohne echte Intervall- und Quellsemantik |
| [`scripts/sb/build_tyndp_demand.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_demand.py) | TYNDP Demand-/WS-Excel-Reader | optional als DFT-Quellparser, **nicht** komplette Last-zu-Original-Load-ID-Mappingimplementierung |
| [`scripts/sb/build_tyndp_pemmdb_data.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_pemmdb_data.py) | Kapazitäten und thermische Verfügbarkeiten | nur optionaler zusätzlicher Source-Bereich, keine statischen M0-PNom-Änderungen |
| [`data/tyndp_technology_map.csv`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/data/tyndp_technology_map.csv) | Quell-/TYNDP-/PyPSA-Carrier-Crosswalk | Reuse als **Startpunkt**, gegen M0-Carrier und reale PECD-Technologien anpassen |
| [`config/config.tyndp.yaml`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/config/config.tyndp.yaml) | PECD-v4.2-Konfig, TYNDP-Node-Grid, drei TYNDP-WS je Horizon und `fill_gaps_method: zero` | **nicht** als gültige Fünf-Szenario-/Daten-Fidelity-Policy kopieren |
| [`scripts/build_tyndp_network.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/build_tyndp_network.py) | TYNDP-Knoten/NTC-Netz, bewusst leere detaillierte AC-Line/Transformer-Tabellen | **NICHT** als M0-/CGMES-/detailliertes elektrisches Referenznetz |
| [`scripts/prepare_sector_network.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/prepare_sector_network.py) | erstellt Anlagen und koppelt TYNDP-Kapazitäten an TYNDP-Regionen | für M1 auf **vorhandenen** CGMES-Generatoren nicht direkt benutzen |

**Kernsatz:** Open-TYNDP hat **PECD v4.2**, aber **nutzt die Source-Daten bereits TYNDP-knoten-/regionenbezogen**. Das ist nicht dasselbe wie „native PECD-ORIG-PV-NetCDF auf ein hochaufgelöstes Netz mappen“. Für regionale Wind-CF ist die regionalisierte Produktauflösung hingegen bereits die offiziell verfügbare Quellauflösung.

## 6. Nicht wiederverwenden oder neu bauen?

| Funktion | Existiert | Noch neuer Code? | Disposition |
|---|---|---|---|
| Core-Objekte und dynamische Zeitreihen | PyPSA | **NEIN** | 1:1 nutzen |
| PECD regionale Wind-/PV-CSV | Open-TYNDP + MA2 | **NEIN**, nur reale Source-Schemas validieren | vorhandenen MA2 Reader weiterverwenden |
| PECD griddiertes `ORIG`-PV-NetCDF | xarray Bibliotheks-IO, **kein fertiger Projektquellparser** | **JA**: Dataset-Header-/Source-Variant-Reader inkl. Chunk/CF-Normierung | MA5-Native |
| Offizielle regionale fractional Masken als native NetCDF | xarray; Geo-Methoden in Atlite/GeoPandas | **JA**: PECD-Mask-Reader/Region-Registry + Ambiguitäts-/Boundary-Policy | MA5-Native |
| Auto `Asset→ORIG-Pixel/PECD-Zone` | GIS primitives + MA2 kann Mappingtabellen **prüfen**, nicht erzeugen | **JA**: deterministic original-asset Spatial Mapper + belegter Kapazitätsmix | MA5-Native |
| Hydro-Intervalle, Energie und Asset-Ziel | MA3 | **NEIN**, sofern reale Source-Semantik passt | Realsource-Qualifikation |
| Demand/DFT auf vorhandene `Load`-IDs | PyPSA-Eur Verteilungsfunktionen, aber kein kompletter IoSN-Load-Mapper | **JA falls M1-Pflicht**: minimale `Load`-ID-Allokation und regionaler MW-Witness | MA5-Demand parallel |
| PyPSA-Composer, 5 Szenarien, Datengates | MA4F | **NEIN**, nur neuen Reader/Mapper/ggf. Demand-Adapter ankoppeln | MA5-Integrations-Upgrade |
| Netzimport CGMES | M0 eigener Owner | **NICHT M1** | M0 unabhängig |
| Netzreduktion, Clustering, CF-Reaggregation | M2 eigener Owner | **NICHT M1** | erst nach Abnahme |
| Eigenes stochastisches PyPSA-Modell/optimieren | PyPSA, ggf. später | **NEIN** | nicht Teil von M1 |
