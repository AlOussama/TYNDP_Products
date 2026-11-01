# MA1C — Hydro Source, Interval, Technology & Allocation Ledger

**Status:** `HYDRO_REAL_DATA_NOT_PROVIDED` · **Keine echten hydro-spezifischen Quellzeitreihen, CSV-Header, Originalintervalle, Basin- oder Asset-Anteilsschlüssel gelesen.** Das folgende Ledger ist die geprüfte **Semantik-/Validierungsmatrix**, kein erfundener Hydro-Datensatz.

## 1. Getrennte Technologiefamilien

| PECD / TYNDP Code | Physikalische Größe und Produktklasse | Erwartete PyPSA-Klasse nur nach M0-Freigabe | Source-/Mappingstatus |
|---|---|---|---|
| `HRR` | Run-of-river **inflow energy**, typischerweise weekly `MWh` im PECD-v4.2-SZON-Produkt | bestehender RoR-`Generator` mit freigegebener Leistungs-/CF-Interpretation oder freigegebenes Zuflussmodell | `NOT_PROVIDED` |
| `HRI` | Reservoir **inflow energy**, nicht erzeugte Elektrizität | M0-`StorageUnit` oder genehmigter `Store+Link`-Zuflussport | `NOT_PROVIDED` |
| `HPI` | Pondage/run-of-river with pondage **inflow energy** | bestehender Speicher-/Generator-Port nach Typ | `NOT_PROVIDED` |
| `HOL` | Open-loop pumped-storage **natural inflow energy** | genehmigter offener PHS-Zuflussport, getrennt von Pumpenergie | `NOT_PROVIDED` |
| `HCL` | Closed-loop/pure pumped-storage **Technologieklasse** im TYNDP-Crosswalk; **nicht** ohne Beleg eine PECD natürliche Inflow-Zeitreihe | PHS-Speicher/Pumpe/Turbine gemäß M0; kein fiktiver natürlicher Zufluss | `NOT_PROVIDED/NOT_AUTOMATIC_INFLOW` |
| `HRO` | Run-of-river **generation energy** `MWh`; **kein** Inflow | kein generischer `storage_units_t.inflow`-Import | `GENERATION_NOT_INFLOW` |
| `HPO` | Pondage **generation energy** `MWh`; **kein** Inflow | kein generischer Inflow-Import | `GENERATION_NOT_INFLOW` |
| `HRG` | Reservoir/hydro **generation energy** `MWh`; **kein** Inflow | kein generischer Inflow-Import | `GENERATION_NOT_INFLOW` |

**Beleg:** `data/tyndp_technology_map.csv` des fixierten Open-TYNDP-Commits kodiert `HRR/HRI/HPI/HOL/HCL` nach PEMMDB-Turbinen/Pumpen/Reservoir-Typen; ECMWF-PECD-v4.2-Produkthandbuch beschreibt `SZON` mit **wöchentlichen MWh-Hydrowerten** und unterscheidet Inflow von Generation. Ob der tatsächliche **TYNDP-2026-Hydro-Inflow-ZIP** andere Intervall-/Zeitauflösung oder andere Typkombinationen enthält, muss an den Bytes geprüft werden, nicht aus der PUG geraten.

## 2. Open-TYNDP-Reader: tatsächlich belegte Semantik und Gegenbefund

`scripts/sb/clean_tyndp_hydro_inflows.py` @ `a50c3dc5d1cf4004ea28c499052829ae4a5eb8f2`:
- sucht Dateien `Hydro Inflows/{planning_horizon}/{node}_Hydro_Inflows_{hydro_tech}_{planning_horizon}.csv`; `node.replace("GB","UK")`;
- liest `WS###`; erkennt `WEEK` oder daily anhand Indexname;
- erzeugt für Wochen 53 Anker `Jan01 + 7 Tage`; Tagesindex teils mit entfernten Schaltjahrtagen;
- `.reindex(hourly).ffill().div(168 bzw. 24)`; fehlende Node-Dateien/Regionen mit `.fillna(0)`;
- Ergebnisse bleiben **regional** `bus` bzw. `TYNDP_NODE`, nicht Original-Hydro-Anlage.

Daher ist der Algorithmus **nur Parser-/Format-Vorlage**, kein MA3-freigegebener Konverter. Das pauschale `168 h` oder `24 h` ist **nur dann** physikalisch zulässig, wenn das reale Quellintervall nach UTC-Konversion exakt diese Länge hat; die 53. Woche kann ein Restintervall sein, DST/Leap/teilweise Kalenderwochen sind gesondert zu behandeln. Wöchentliche `MWh` sind nicht stündliche tatsächliche Erzeugungsmessungen.

## 3. Obligatorischer realer Source-Intervalldatensatz

| Spalte | Erforderliche Bedeutung | Aktueller Inhalt |
|---|---|---|
| `source_dataset_id, source_file_sha256, correction_date, license` | byteverifizierter eindeutiger Hydrobestand | `NOT_PROVIDED` |
| `planning_horizon, exact_weather_id, technology_code` | keine 3→5 Substitution | `NOT_PROVIDED` |
| `source_hydro_region, region_type, basin_or_tso_ref` | SZON-/Basin-/Allokationsregister | `NOT_PROVIDED` |
| `native_interval_start_utc, native_interval_end_utc` | echte Intervallgrenzen, notierte Zeitkonvention | `NOT_PROVIDED` |
| `native_value, native_unit, physical_semantics` | `MWh_inflow` oder `MWh_generation` getrennt | `NOT_PROVIDED` |
| `destination_m0_asset_id, pypsa_component_id, port, B_fraction` | realer bestehender Asset-Port mit hydrologischem/TSO-Anteilsbeleg | `NOT_PROVIDED` |
| `assigned_MWh, hourly_MW, reconstructed_MWh, residual_MWh` | numerischer Energie-Closure je Source und Anlage | `NOT_EXECUTED` |

## 4. Physikalische Regeln für MA3

Für jedes reale Quellintervall `k=[t0,t1)` und Hydrosource `z` gilt `Δh_k=(t1-t0)/3600` mit tatsächlich gegebener UTC-Zeitbasis; `E_zk[MWh]` wird nur mit belegten Anteilen `B[a,z,k]≥0` zugeordnet. Für nicht absichtlich ausgeschlossene vollständig abzubildende Teilmengen: `sum_a B[a,z,k]=1`. Ein echtes, vorab definiertes Aggregations-/Coverage-Regime kann Teilzuordnungen zulassen, **muss** den nicht zugeordneten Rest als `unallocated_MWh` mit `BLOCK`/Scope-Freigabe ausweisen.

`E_azk=B[a,z,k] E_zk`, `P_azk=E_azk / Δh_k`, `sum_{t in k} P_a(t) Δt = sum_z E_azk`. Intervallbreite, UTC-Umstellung, 53. oder nur teilweise letzte Woche, leap/DST und Up-/Downsampling-Lücken unabhängig kontrollieren. Gleichheit mit `storage_units_t.inflow`-Portenergie nur nach eindeutigem M0-Wirkungsgrad-/SOC-Vertrag; PV/MW- und Wasser-/Elektrizitätsenergieeffizienz nicht verwechseln.

**Allokationsnachweis:** hydrologische Becken-/Flussgebietszugehörigkeit, behördliche/TSO-Anlagentabelle oder andere genehmigte physikalisch nachvollziehbare Zuordnung. Nur elektrischer Generator-`bus.x/y` reicht nicht. Pro Region, Asset, Tech und Intervall eine Quelle und ein dokumentierter Anteil; Mehrfachzählungen und Pumpstrombezug separat.

**Fehlende Daten sind nicht `0 MWh`**: unbekannte Quelldatei `BLOCK`, ausdrücklich dokumentierter, technologisch geschlossener natürlicher Zufluss `NOT_APPLICABLE_BY_DESIGN` (nicht ein ausgefüllter fehlender Datensatz). `fillna(0)`, `ffill`, Gleichsetzen mit Generation und erzwungene Jahressubstitution verboten.

## 5. Abnahme und Next Owner

Die tatsächlichen `WEEK`-/Daily-Header, `WS###`-Spalten, Zone/Basin, Intervalldaten, fünf WS-Verknüpfungen, Anlagensplittings und StoragePorts fehlen. `G1-E=BLOCKED_NOT_PROVIDED`; kein realer MWh→MW-Zahlenwert, keine ausgeführte Energiebilanz, keine Hydro-Real-Data-Freigabe. **MA3** darf mit typisierten synthetischen Intervallen, partieller 53.-Woche und negativen Quellenfällen implementieren; nach echten Files fünf Sets mit positivem, quellengebundenem Energieclosure qualifizieren.
