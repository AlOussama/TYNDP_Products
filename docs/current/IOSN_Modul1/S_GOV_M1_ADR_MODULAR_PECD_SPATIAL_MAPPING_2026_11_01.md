# S-GOV-M1 ADR — Netzimport strikt von PECD-zu-Netz-Raumzuordnung trennen

**Datum:** 2026-11-01  
**Status:** OWNER_SCOPE_CLARIFICATION / M1 ARCHITECTURAL AMENDMENT  
**Betroffene Makros:** MD-1 (Source Witness), MA-4F (Integration), MA-4R (Real-data Acceptance)  
**Verbindlicher Nutzerhinweis:** M0 importiert **ausschließlich Netzdaten aus einem bestimmten Format**. Wetter- und PECD-Profile sind eigenständige regionale/rasterbezogene Daten, deren Zuordnung zum importierten Netz ein **separater Vorgang innerhalb von M1** ist. Netzaggregation gehört in das separate Folgemodul 2.

## Entscheidung

1. **M0 ist formatbezogener Netzimport / elektrisches Preprocessing.** M0 liest CGMES oder ein jeweils vereinbartes Quellnetzformat, erzeugt ein elektrisches PyPSA-`Network` mit vorhandenen Bus-/Generator-/Last-/Speicherelementen, elektrischer Topologie, technischen Stammdaten und vorhandenen Geokoordinaten; es erhält seine eigenen Quellen-/Identitäts-/Qualitätsdaten gemäß seinem M0-Owner-Vertrag. **M0 ist nicht PECD-, Hydro-, DFT- oder Wetter-Zuordnungsdienst.**
2. **M1 ist formatunabhängiger Time-Series-/Spatial-Join-Consumer.** Es liest ein bereits vorhandenes hochaufgelöstes PyPSA-Netz (aus M0 oder grundsätzlich einer beliebigen qualifizierten Importquelle) und separate autoritative PECD-/Hydro-/ggf. Lastzeitreihen. M1 bestimmt selbst das Profil→Anlage/Bus-Mapping mit Geo-/Quellmetadaten und schreibt nur genehmigte zeitvariable PyPSA-Attribute.
3. **M2 allein ist Netzaggregation.** M1 erzeugt keine reduzierten Netzbereiche, Ersatzknoten, Ersatzimpedanzen oder neue Anlagen. Die Zuordnung eines regionalen PECD-Profils zu vielen getrennten elektrischen Generatoren ist **keine Netzaggregation**, weil alle elektrischen Anschlussknoten bestehen bleiben.
4. **M0-Sidecar-Verhältnis:** Das derzeit dokumentierte `DetailedNetworkReference`-/Sidecar-Paket ist eine **M0-spezifische Provenienz-/Qualitätsausgabe**, nicht ein zur PECD-Datenverarbeitung neu von M0 zu erstellendes Feature. Für das minimale M1-Funktionsinterface reichen `PyPSA.Network` + stabile Komponenten-IDs/`bus`/`carrier`/`p_nom` + nachgewiesener Koordinatenbezug + Input-/Revisionsmetadaten. *Wenn* M0-Quelle und M0-Normvertrag ein Sidecar verbindlich vorsehen, übernimmt M1 es zur Identity-/Geoqualitätsprüfung; M1 verlangt von M0 **keine** PECD-/Hydro-Region-ID oder Basin-Allokation. Ein späteres echtes M0-Paket bleibt für die konkrete IoSN-Realdatenintegration nötig, aber nicht für den synthetischen M1-Integrationstest.
5. **Geo-Herkunft:** Buskoordinaten können aus dem Netz gelesen werden; ihre Eignung als *physischer Generatorstandort* ist eine M1-Prüfung. Ein landseitiger Offshore-Bus oder synthetischer Trafo-Sternbus ist kein belegter Windstandort. M1 darf hierzu die vorhandene M0-Geo-Provenienz verwenden und gegebenenfalls **separate** PECD-/Anlagengeometriedaten einlesen, ohne M0 auf Wetterdaten zu erweitern.

## Ergebnis der tatsächlichen PyPSA-Softwareinspektion

| Bibliothek | Tatsächlich verfügbar | Konsequenz |
|---|---|---|
| PyPSA-Core `pypsa/geo.py` | `haversine`, `haversine_pts`, `compute_bbox`, CRS-/Projektionshilfen | Geometrische Hilfsmittel, **keine** generische regionale `PECD CF → existing Generator`-API nachgewiesen |
| PyPSA-Core `Network` | Bus-Koordinaten, Generator/Load/Storage-Komponenten; `generators_t.p_max_pu`, `storage_units_t.inflow`, `loads_t.p_set`, `set_snapshots`, NetCDF | Zielnetz und Zeitreihen **direkt nutzbar**, kein Core-Fork benötigt |
| Atlite `Cutout.indicatormatrix` und `atlite.gis.compute_indicatormatrix` | Geometrische Sparse-Überlappungsmatrix von Polygonen und Rasterflächen | Wiederverwendung für geeignete Raster-/Regionsschnitte möglich; Area-share ist **nicht** automatisch installierte MW-Share |
| Atlite `compute_availabilitymatrix` | Anteil **landnutzungsseitig zulässiger Flächen** je Rasterzelle und Polygon mit Exclusions | **Nicht** verwechseln mit zeitabhängiger Erzeugungs-`p_max_pu`! |
| PyPSA-Eur `determine_availability_matrix`, `build_renewable_profiles` | Landnutzung/Atlite-Wetter nach PyPSA-Eur-Netzregion und Resource-Bin | Konzept-/Geohilfsreuse; Standard-Voronoi-/Clusterregionen nicht für Original-CGMES als verbindliche Zuordnung |
| Open-TYNDP `tyndp-2026` | PECD v4.2 CSV/NetCDF und Hydro/TYNDP-Quellparser | Eingabeadapter wiederverwenden, deren TYNDP-Zonenknoten von Original-PyPSA-Buskennungen strikt trennen |

**Referenzen (Immutable):**
- PyPSA-Core: https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/geo.py
- PyPSA-Core Index/API: https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/index.py
- Atlite `indicatormatrix`: https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/cutout.py
- Atlite `availabilitymatrix`: https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py
- PyPSA-Eur source: https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_renewable_profiles.py
- Open-TYNDP 2026: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py

## Sollschichten in M1

```
                 M0 / NETZFORMAT-IMPORT                 PECD / HYDRO / DFT
                  PyPSA detailed Network                externe Quellen
                         |                                    |
                         |                           normalize_source_profiles
                         |                                    |
                         +------> M1 spatial profile join <---+
                                    |   
                       Asset-to-PECD association table
                           (ID + geo/region + tech)
                                    |
                    Renewable / Hydro / Load time series
                                    |
                         PyPSA dynamic attribute writer
                                    |
                         full-resolution PyPSA Network
                                    |
                     M2 separate network aggregation
```

### Identitäts- und Raumvertrag

`n.generators.index` und `n.generators.bus` sind die elektrischen **Target-IDs**. `n.buses.x/y` kann als geometrischer Input dienen; sofern vorhandene Anlagenkoordinaten/Quellzuordnungen verlässlicher sind, gehen diese vor. `source_profile_id` ist eine PECD-Raster-/Regions-/Technologie-ID, **nicht** ein elektrischer Bus. Der Spatial Join ist eine **separate M1-Transformation** mit expliziter Assignment-Ledger.

Bei regionalen Profilen gilt zum Beispiel `p_max_pu[g,t] = CF[region(g), technology(g), weather_id, t]`, auch wenn mehrere Generatoren über verschiedene Busse auf dieselbe PECD-Region zeigen. PV-DC/AC-Normierung und hydroenergetische Gebietsanteile sind M1-Quell-/Modellsemantik, nicht Netzdatenimport.

**Nicht verwechseln:** Netzknoten sind immer elektrisch fein aufgelöst, auch wenn Windverfügbarkeit nur regional zur Verfügung steht. Keine scheinbare `0.25°`-Wind-CF-Auflösung aus dem meteorologischen Raster ableiten, wenn das bezogene CF-Produkt nur zonal vorliegt.

## Auswirkungen auf aktuelle Makros

- **MD-1:** liefert physische PECD-/Hydro-Quell-/Region-/Wetterdatensatz-Nachweise und den tatsächlichen Netzimport-Output aus M0 als **zwei voneinander unabhängige Input-Pakete**. MD-1 beauftragt M0 nicht mit einem PECD-Mapper. Die eigentliche Zuordnung erfolgt in M1.
- **MA-4F:** baut den M1 Spatial Join / Composer **an jeder geprüften hochaufgelösten PyPSA-Netz-Fixture**. Er darf sein Fixture-PASS nicht davon abhängig machen, dass der M0-CGMES-Importer bereits produktiv existiert; ein realistisches synthetisches PyPSA-Netz genügt ausdrücklich **nur für das Fixture-Gate**. Production-IoSN-E2E bleibt an echte Daten und qualifizierte M0-Ausgabe gebunden.
- **MA-4R:** liest die beiden Pakete unabhängig und führt den PECD-/Hydro-zu-Netz-Join ausschließlich in M1 aus; ein M0-Sidecar kann bei Herkunft/Identity helfen, aber M0 produziert weder PECD-Profile noch Mapping-Annahmen.
- **Governance:** Bestehende frühere M1-Gate-Texte sind so auszulegen, dass sie M0 nicht zur Entwicklung von Wetter-Profilgeometrie, Hydro-Basin-Quoten oder DFT-Zeitreihen verpflichten. Dass der reale Originalnetz-Import noch nicht abgeschlossen ist, blockiert nur **Real-E2E**, nicht den formatunabhängigen M1-Fixture-Composer.

**ADR-Entscheid:** `M0_NETWORK_IMPORT_ONLY__M1_SPATIAL_TIMESERIES_MAPPING_ONLY__M2_AGGREGATION_ONLY`. Kein PyPSA-Core-Change-Request, bevor ein eigenständiger generischer Mapping-Baustein mit Source-/Geo-/Physiksemantik wirklich nachgewiesen als allgemein wiederverwendbar spezifiziert ist.
