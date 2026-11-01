# MA1C — PECD v4.2 Spatial Product / M0 Mapping Matrix

**Evidenzstatus:** Produkttypen und Maßeinheiten aus PECD-v4.2-PUG, MA-1 und Open-TYNDP-Quellcode; **keine gelieferten Pixel-/Masken-/Point-Samples**. Keine räumliche Genauigkeit höher behaupten als die tatsächlich bereitgestellte PECD-Quelle.

| Quellprodukt | Native Auflösung und Semantik | Zulässiger elektrischer M0-Zieltyp | Reales Mapping-Gate / Disposition |
|---|---|---|---|
| Wind Onshore `PEON` | stündlicher regionaler `MW/MW`-CF | vorhandener `Generator`, Carrier `onwind`/freigegebenes Äquivalent | explizite Profilregion+Technologie oder geprüfter Standort/Maskenmatch; fehlend `BLOCK` |
| Wind Onshore `P2ON` | andere regionale Partition als PEON, `MW/MW` | vorhandener `Generator` | eigene Regioncode-Registry/Mask; kein PEON-Code als P2ON interpretieren |
| Wind Offshore `PEOF` | Offshore-Regio-CF, `MW/MW` | bestehender Offshore-`Generator` | echte Windpark-/Seekoordinate bzw. offiziell belegter Offshore-Profile-Link; landseitige Bus-x/y **nicht** verwenden |
| Wind Offshore `P2OF` | zweite Offshore-Regionenklasse, `MW/MW` | bestehender Offshore-`Generator` | PEOF/P2OF weder namengleich noch austauschbar annehmen |
| Solar PV `ORIG` | **nur wenn geliefert** ursprüngliches 0,25°×0,25°-Raster, `MW/MWp` | `Generator` Solar PV Utility/Rooftop | prüfbarer echter Anlagenpunkt, WGS84/Quell-CRS, Zellenkante, PV-Technik und MWp→MW_AC-Vertrag |
| Solar PV `PEON/P2ON` | stündlicher regionaler PV-CF `MW/MWp` | vorhandener Solar-`Generator` | korrekte PV-Region und Technologietyp; nicht als originale Raster-CF deklarieren |
| Solar PV `NUT2` | administrative NUTS-2-Gebietsklasse (aus tatsächlich geliefertem Versionsstand) | vorhandener Solar-`Generator` | Region-Registry samt gültigem NUTS-Stand und Grenzflag; keine Nearest-Centroid-Heuristik |
| Solar PV `SZON` | zonal/bidding-zone, `MW/MWp` | vorhandener Solar-`Generator` | nur bei belegtem PV-Zonenlookup; geringe räumliche Auflösung im Catalog dokumentieren |
| PECD Meteorologie `ORIG` | ca. 0,25°-Raster-Wettergrößen, **nicht** direkt CF | kein direkter Generator-`p_max_pu`-Port | erst genehmigtes Ressourcenkonversionsmodell; nicht Meteorologie = CF |
| Offizielle Regionmasken | fractional NetCDF masks je Produktsystem/Version; teils keine öffentlichen Shapefiles | ausschließlich geografischer Mappingbeleg | exakte `mask_id`, Sourceversion `fv`, `CRS`, Raster/Zellenachsen prüfen; Fractional-Flächengewicht ≠ Anteil an installierten MW |
| Hydropower `SZON` | native Wochen-`MWh`-Hydrologie (Quelle prüfen) | `Generator` RoR, `StorageUnit` oder M0-genehmigter `Store+Link`-Port | hydrologische basin/TSO-Asset-Anteile, nicht Generatorbus-Polygon; siehe Hydro-Ledger |
| Open-TYNDP `TYNDP_NODE` | aus TYNDP-System und PEMMDB abgeleitete Quellregion, kein CGMES-Bus | kein ungeprüfter direkter Join | getrennte Namespace-Registry; `buses_tyndp`/`busmap_base_s_all.csv` **nicht** ins M0-Originalnetz importieren |

## Invarianten für die realen Assignments

`network_revision_id` (M1 Altvertrag) bzw. autoritativ nach M0-Repair `canonical_revision_id + projection_id`, `existing_generator_id`, `source_asset_id`, `existing_bus_id`, `source_profile_id`, `planning_horizon`, `weather_id`, `technology_variant`, `native_area_level`, `geo_source`, `geo_quality`, `assignment_method`, `mask_version`, `A_weight`, `approval_ref` sind getrennte Felder. Es gibt aktuell **null** real verifizierte Assignmentzeilen ([SPATIAL_ASSIGNMENT_LEDGER.csv](SPATIAL_ASSIGNMENT_LEDGER.csv)). Der Ledger zeigt Prüfpflichtfälle ohne fiktive Asset-IDs.

**Präferenz:** `EXPLICIT_SOURCE_ID` → `VERIFIED_PLANT_LOCATION` → belegter `VERIFIED_BUS_PROXY` → `CAPACITY_WEIGHTED_COMPOSITE` → sonst `UNRESOLVED/BLOCK`.

Für jeden existierenden Generator `g` und `horizon h` gilt eine qualifizierte Profilmatrix `A[g,p,h]>=0` und `sum_p A[g,p,h]=1`. Nur reale dokumentierte MW-Anteile, nicht geographische Pixel-/Maskenflächen, dürfen ein über mehrere Regionen zusammengesetztes Profil gewichten. Identische `PEON`-Zeitreihen dürfen mehreren getrennten Originalbus-Generatoren zugewiesen werden, solange die Anlagenzuordnung belegt ist; `Generator.bus`/`p_nom` unverändert.

## Negativwitnesses, die MA2 implementieren und später real belegen muss

1. Offshore-Windpark mit landseitigem Netzknoten: Standort = offshore Anlage, nicht Landfall.
2. M0 `bus_role=SYNTHETIC_3W_STAR`: Land und physische Geometrie fehlen berechtigt; ausgeschlossen aus geografischem Generator-Matching, keine pseudo-WGS84-Geometrie.
3. Grenznähe und zwei Masken/unklare Topologie: Disambiguierung durch reale Quelle, keine willkürliche Region nach Distanz.
4. Aggregierter bereits existierender Generator mit zwei Regionen: dokumentierte MW-Aggregation und Quellwerte, `sum A=1`.
5. Solar DC-Nennleistung `MWp` vs M0 `p_nom[MW_AC]`: keine direkte `p_max_pu`-Befüllung ohne explizite Basis/Clipping-Transformation.
6. Quelle `ORIG` nicht geliefert, nur `SZON`: `ORIG`-Sampling muss mit `NOT_PROVIDED` blockieren, keine scheinbare Feinauflösung.
7. Zeit-/Profilindex ohne fünf Wetter-IDs, fehlende Dateien oder Verwechslung TYNDP_NODE/CGMES_BUS: fail closed.

**Output erst nach tatsächlichem Source-PASS:** `renewable_cf[planning_horizon,weather_id,UTC_naive_time,existing_generator_id]`; Wert ist `Generator.p_max_pu` und **niemals Dispatch**. Native Geometrieauflösung und Zuweisungsqualität bleiben im `profile_catalog` dokumentiert.
