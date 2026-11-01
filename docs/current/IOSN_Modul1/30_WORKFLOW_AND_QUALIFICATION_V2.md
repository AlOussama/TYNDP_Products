# IoSN Modul 1 V2 — Snakemake-/PyPSA-Workflow und Qualifikationsvertrag

**Datum:** 2026-11-01  
**Status:** `WORKFLOW_SPECIFIED / NATIVE_GRID_IMPLEMENTATION_PENDING / REAL_SOURCE_BLOCKED`  
**Grundlagen:** [00 Architektur](00_CANONICAL_ARCHITECTURE_V2.md) · [10 Upstream-Reuse](10_UPSTREAM_REUSE_LEDGER_V2.md) · [20 Daten-/Spatial-Vertrag](20_SOURCE_SPATIAL_COMPONENT_CONTRACT_V2.md).

## 1. Leitlinie

**Keine neue PyPSA-Core- oder PyPSA-Eur-Rechenpipeline.** Die einzigen neuen fachlichen Operationen sind die **Auswahl der Quelle**, ein nativer PECD-NetCDF-/Masken-Leser, ein automatisch generierter Profil-zu-Originalanlage-Spatial-Join und — falls regionale Lastdaten verteilt werden müssen — ein Demand-zu-bestehende-Load-IDs-Join. Der **bereits ausgeführte MA4F-Composer** bleibt die einzige PyPSA-Netz-Schreibinstanz. M0 liefert nur Netz, M2 aggregiert später.

```text
M0 (or another format import)     PECD regional CSV | SPV ORIG NetCDF | Hydro | DFT
    detailed PyPSA.Network                            |
          |                                 normalize independent sources
          |                                   |                |
          |                             native CF      native masks/geometry
          |                                   |                |
          +-----------------------> automatic original-asset spatial join
                                              |
                         existing MA2 RES / MA3 Hydro / optional DFT load
                                              |
                                 existing MA4F dynamic composer
                                              |
                         QA + existing topology + 5 per-weather output nets
                                              |
                                     M2 network reduction
```

## 2. Inkrementeller Snakemake-Schnitt

**Implementierungsbaseline:** [MA4F getesteter Branch](https://github.com/AlOussama/TYNDP_Products/tree/1ab3eb1aed54975e69586cc3d958a24d97a6288f) enthält `Snakefile.iosn_m1_ma4f`, `rules/iosn_m1_res.smk`, `rules/iosn_m1_hydro.smk`, `rules/iosn_m1_compose.smk`, `scripts/iosn_m1/compose.py`.

| Stufe | Vorhanden / neu | Input | Output |
|---|---|---|---|
| `source_catalog` | bestehende MD1-/MA2-Contracts **adaptieren** | fixierte 5 WS, Source-Version, Datei-Hashes, Produkte, Rechte | katalogisierte Source-Identity/Quality |
| `regional_pecd_cf` | **MA2** | On-/Offshore-Regional-CSV, ggf. PV regional | stündliche `native_cf(time,profile_id)` |
| `native_pv_orig_cf` | **NEU** | echtes SPV-ORIG-CF-NetCDF + Technologie-/Klima-Metadaten | stündliche `CF(time,grid_cell_id,PV_variant)` |
| `native_pecd_masks` | **NEU** | offizielle NetCDF fractional Masken; Geo-Region-Registry | fraktionale PEON/P2ON/PEOF/P2OF/SZON-Regionmasken |
| `auto_asset_profile_map` | **NEU** | reale PlantGeo bzw. autorisierter Busproxy, CF-Katalog und Masken | `asset_profile_map` für vorhandene Generatoren; Error-Ledger |
| `compile_res` | bestehende **MA2**-Schnittstelle | native CF + Map + PV AC/DC Policy | `renewable_cf(time,existing_generator_id)` |
| `compile_hydro` | bestehende **MA3**-Schnittstelle | native SZON-MWh/Intervall/Basin-Anteile | `hydro_inflow` / `ror_availability` / Energie-Ledger |
| `compile_demand` | **NEU, optional bei Last-Pflichtscope** | DFT/TSO MW + Regionen/Lastanteile | `load_p_set(time,existing_load_id)` |
| `compose_reference` | bestehende **MA4F** | Read-Only M0-Netz/Sidecar, RES/Hydro/Load, QA/Owner | ein `.nc` je `(horizon,weather_id)` |
| `qualify_reference` | MA4F erweitert | Source/Netz/Mapping-/Statik-/Hydro-Evidenz | PASS/NOT_ASSESSED/BLOCKED + unabhängige Reviewbasis |

Die hier neu eingeführten Rules sind **Namen eines Soll-Workflows**, nicht behauptete bereits implementierte Snakemake-Regeln.

### Source Switch

`m1.profile_source=pecd_native_cf` ist eine **neue projektseitige Option**, keine nachgewiesene upstream-PyPSA-Eur-Option. Sie setzt vorausberechnete PECD-Region-Wind-/PV-CF und, wenn bezogen, ORIG-PV-CF ein. `m1.profile_source=atlite_meteorological` bezeichnet einen *gesondert zu beauftragenden* alternativen Energieumwandlungsmodus und darf im Standardpfad keine offiziell vorhandenen PECD-Kapazitätsfaktoren neu modellieren.

## 3. Getrennte Evidenzgates

| Gate | Definition | Stand 01.11.2026 |
|---|---|---|
| `S-PECD-CATALOG` | offizieller PUG-Produkt-, Technologie-, Versions- und Auflösungsnachweis | `PASS_STATIC_CATALOG_ONLY` laut MD1 |
| `S-PECD-PHYSICAL` | originale reale PECD-Source-/ORIG-PV-/Maskenbytes inkl. Hash, 5 WS, Zeit-/Produkt-/Unit-Witness | `BLOCKED_NOT_WITNESSED` |
| `S-HYDRO-PHYSICAL` | originale Hydro-Dateien, SZON-/WEEK-/MWh-/Intervallsemantik, 5 WS | `BLOCKED_NOT_WITNESSED` |
| `S-DEMAND-PHYSICAL` | bei Lastpflicht: tatsächliche DFT/TSO-Stundenwerte und WS-Verknüpfung | `NOT_QUALIFIED` |
| `N-M0-PHYSICAL` | qualifiziertes, tatsächlich erzeugtes Netz unabhängig vom PECD-Service | `BLOCKED_NOT_PROVIDED` |
| `J-M1-SPATIAL_JOIN` | echte Quelle + echte Anlagen / geo+tech+capacity+ports korrekt verknüpft | `BLOCKED_PREREQUISITES` |
| `FIXTURE-E2E-MA4F` | 92 Pytest, 16 Snakemake, 5 synthetische NetCDF, 16 statische Tabellen gleich | `PASS_FIXTURE` |
| `REAL-E2E` | komplette originale fünf Wetterdaten und echtes Referenznetz, native Masken, Hydro/Load etc. | `NOT_EXECUTED` |
| `INDEPENDENT-M1` | unabhängiger Reviewer am Real-Producer-SHA | `NOT_EXECUTED` |

**Wichtig:** Native PECD-Source-Dateien können vor einem realen M0-Netz eigenständig `S-PECD-PHYSICAL=PASS` erreichen. Umgekehrt erzeugt ein M0-Import keinerlei PECD-Quellpass. Der reale M1-Join verlangt beide.

## 4. Pflichtmatrix für neue positive/negative Fixtures

### 4.1 Native PV/Regionmasken
- Lesen realitätsnaher synthetischer NetCDF-CF mit `time,latitude,longitude,technology`; die tatsächlichen Dimensionen müssen **aus den echten Dateien** erkannt werden. Lat-Achse auf-/abwärts, Koordinaten-CRS, Halbzelle und Source-Grid-Index verifizieren.
- ORIG-PV im Raster `0.25°×0.25°`, mindestens zwei PV-Anlagen in unterschiedlichen Rasterzellen bei identischem elektrischem Bus sowie zwei PV-Anlagen an unterschiedlichen Bussen innerhalb derselben Zelle. Das gewählte CF-Produkt, nicht der Bus, bestimmt die wetterseitige Genauigkeit.
- NetCDF-Masken `mask(region,latitude,longitude)`, fraktionale Grenz-/Küstenzellen, zwei teilweise belegte benachbarte Regionen, Masken-GeoJSON-Interoperabilität nur mit nachgewiesener Konversionsgeometrie. Nie Regionmaskenflächenanteile automatisch als Generator-MWp-Anteile setzen.
- Test der tatsächlichen PV-Technologievarianten (Rooftop industrial/residential, utility fixed/tracking), Grid NaN/exclusion, Source-Mismatch und Datei-SHA.

### 4.2 Wind und Assetzuordnung
- Onshore PEON/P2ON und Offshore PEOF/P2OF mit realitätsnahen Regional-CSV, gleicher Wind-CF auf mehreren **getrennten** elektrischen Originalknoten.
- Offshore-Profil anhand Parkstandort statt Landfall-Bus; 3W-Synthetic-Bus und unqualifizierter Bus-Proxy strikt ablehnen.
- Echte vorher bestehende zusammengesetzte Generatorgruppe mit nachgewiesenen MW-Anteilen, alternative Regionen/Technologien bei abweichender Source-Version blockieren.
- Keine angebliche offizielle native 0.25°-Wind-CF, wenn die Quelle nur regionales WON/WOF bereitstellt.

### 4.3 Hydro/Demand
- Hydro-Originärintervall-MWh gegen \`∑P_MW×Δh\` und separate Model-/Hydraulik-Konversion, Leap-/DST-/Wochenrand, HCL no-natural-inflow, unautorisierter Store-/Link-Port verweigert.
- DFT bei aktiviertem Demand Source: mehrere vorhandene Load-IDs in einer Source-Region, \`∑Loads MW = Source MW\`, keine Lastdoppelzählung, keine ungenehmigten vorherigen Profile überschreiben.
- fehlendes fünftes WS und fehlende Sourcehours: **FAIL**, keine automatische Null-/Mean-/Planjahr-/Profilsubstitution.

## 5. Gemeinsame PyPSA-Fixture-Regression

**Ist-Nachweis:** MA4F [EXECUTION_REPORT](https://github.com/AlOussama/TYNDP_Products/blob/1ab3eb1aed54975e69586cc3d958a24d97a6288f/docs/current/IOSN_Modul1/MA4F/EXECUTION_REPORT.md), getesteter SHA `cd71f36ddf07fb3ecc1cb4be5701a2586b9950c8`, [CI 41315496732](https://github.com/AlOussama/TYNDP_Products/actions/runs/41315496732). `92/92` Pytest, `16/16` Jobs, `5/5` SYNTHETISCHE 2-Stunden-WS und `16/16` statische Netztabellen im Input/Output/NetCDF-Importer identisch.

**Muss nach nativen Erweiterungen erneut laufen:** bestehende MA2/MA3/MA4F-Tests plus eigene ORIG-/Masken-/Auto-Join-/Demand-Suite, full Snakemake DAG und Writer Collision/Overwrite-/NetCDF-Default-Elision-Tests. Die bisherigen **zwei Stunden** pro Fixture sind nicht die Volljahreszeit-/RAM-Qualifikation der realen fünf Wetterjahre.

**Writer-Whitelist:** `generators_t.p_max_pu` für RES und disjunkte RoR-Generatoren, `storage_units_t.inflow` für erlaubte Hydrotypen, `loads_t.p_set` ausschließlich aus zulässiger Demandquelle. Store/Link-Spezialport bleibt gestaged ohne ausdrückliche Owner-Freigabe.

**Static:** Alle Source-Netz-Komponenten, IDs, Busanschlüsse, \`p_nom\`, Transformatoren, Links, Stores und elektrischen Eigenschaften unverändert. PyPSA 1.4 may omit all-default dynamic NetCDF column: semantischer Gleichheitsbeweis statt Wertänderung/Trick.

## 6. Volle reale Validierung und M2-Gate

- Genau fünf extern festgelegte **wirklich existierende** Weather-IDs und ihre Horizonte; die bisher nur drei bei Open-TYNDP gelisteten TYNDP-Szenarien sind **nicht** automatisch diese fünf.
- Jede Quelle/Asset/Technologie/Region: \`source_profile_id, actual_spatial_level, source_SHA256, component_id, position_quality, mapping_method, weight, time-range, native-unit\`; 100% der verpflichtenden betroffenen installierten MW/Anzahl erklärt oder geblockt. PV \`MW/MWp\` auf AC-Rating nur mit belegter DC-/Inverter-/Clippingkonvention.
- Native Hydro Energieintervall/Lastregionenbilanz und vollständige NetCDF-Originalnetz-Invarianz, CPU/RSS/File-Volumen der realen Systemgröße; Source/Version/Datennutzungsrechte dokumentiert, keine unlizenzierte Originalfile-Publikation.
- Die **physische** Quellprüfung, das importierte Netz und deren **M1-Join** sind eigenständige CAPABILITY-Gates. Ein bestandener realer Source-Download ist noch kein M2-Referenznetz.
- **Separater unabhängiger Reviewer** auf finalem realen Producer-SHA und danach S-GOV-Freigabe vor M2. Nicht einfach \`pytest PASS\` oder ein CAD-/CGMES-Schema als Real-PASS umetikettieren.

**Nächste Makros:** [40_NEXT_MACROS_AND_HANDOFFS_V2.md](40_NEXT_MACROS_AND_HANDOFFS_V2.md).
