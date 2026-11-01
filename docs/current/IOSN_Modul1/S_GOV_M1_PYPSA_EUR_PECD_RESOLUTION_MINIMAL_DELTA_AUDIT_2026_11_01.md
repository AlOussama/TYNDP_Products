# S-GOV-M1 — PyPSA-Core/PyPSA-Eur: PECD-4.2-Auflösung und minimal erforderliche Datenquellenanpassung

**Datum:** 2026-11-01  
**Status:** SOURCE-CODE-VERIFIED_STATIC_ARCHITECTURE_DECISION — keine produktive Implementierung, keine echte PECD-Byte-/PyPSA-Netzqualifikation  
**Ausgangsfrage:** Können die bestehenden PyPSA-/PyPSA-Eur-Schritte beibehalten und lediglich die ERA5/SARAH-Quellprofile durch PECD v4.2 ersetzt werden? Was passiert bei unterschiedlichen PECD-Raumauflösungen?  
**Verbindliche Scopeentscheidung:** M0 importiert Netzformat/ein detailliertes PyPSA-Netz; M1 bereitet PECD-/Hydro-/Lastdaten und ihre räumliche Verknüpfung mit **bestehenden** Netzkomponenten auf; M2 aggregiert das Netz separat. Wetterjahre bereits extern festgelegt (fünf), keine neue Auswahl.

## 1. Prüfanker (immutable)

| Quellstand | Code und eindeutiger Befund |
|---|---|
| [PyPSA-Core @ 23650353](https://github.com/PyPSA/PyPSA/tree/23650353eb1d059acfec28f4915ad3e068c085bf) | [docs/user-guide/design.md](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/docs/user-guide/design.md) mit n.generators_t.p_max_pu; [pypsa/network/io.py](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/io.py) mit _import_series_from_df, [pypsa/network/index.py](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/index.py) und set_snapshots; Core benötigt keine PECD-Erweiterung |
| [PyPSA-Eur @ 1526bb82](https://github.com/PyPSA/pypsa-eur/tree/1526bb820e25a9faa61f32b00bfc77dd05db6b2e) | [rules/build_electricity.smk](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/rules/build_electricity.smk), [scripts/build_renewable_profiles.py](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_renewable_profiles.py), [scripts/build_hydro_profile.py](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_hydro_profile.py), [scripts/add_electricity.py](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/add_electricity.py), [rules/compose.smk](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/rules/compose.smk) |
| [Open-TYNDP tyndp-2026 @ 71a3a9a](https://github.com/open-energy-transition/open-tyndp/tree/71a3a9a15b77114cd79458bceabc98e1a64dd58a) | [rules/sb.smk](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/rules/sb.smk), [clean_tyndp_pecd_data.py](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py), [build_renewable_profiles_pecd.py](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_renewable_profiles_pecd.py), [config/config.tyndp.yaml](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/config/config.tyndp.yaml); **PECD v4.2 bereits importiert**, aber nach TYNDP-Knoten vorgefiltert; \`bin=0\`, nicht das originale PV-Raster |
| [Atlite @ 0d4ff8](https://github.com/PyPSA/atlite/tree/0d4ff8f703a99566b475b8d775aa2e74309123ee) | [atlite/cutout.py](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/cutout.py) und [atlite/gis.py](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py); Sparse-Schnitt-/Indikatormatrix und Atlite-Cutouts, **keine** universelle PECD-Asset-Mapping-Einheit im PyPSA-Core |
| [PECD-v4.2 PUG](https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752) | Energieprodukte Tabelle 2.12 und 3.6: Wind-WON/WOF CF regional; PV-SPV CF auch ORIG 0,25° griddiert; Hydro SZON/Woche |
| [TYNDP-2026 IoSN Methodik, 25.02.2026](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) | §4.2 „high-resolution spatial and temporal weather scenarios“ beschreibt *PECD-Wetterinput allgemein*, **nicht** die Behauptung, alle Wind-CF lägen als 0,25°-Raster-Output vor; §3.8.4 unterscheidet elektrischen Anlagenanschluss und zugehörige PECD-Zone |

## 2. Originaler PyPSA-Eur-Workflow: Datenübergabe

| Schritt | Eingabe | Implementierte Funktion | Ausgabe | PECD-Delta |
|---|---|---|---|---|
| \`build_cutout\` | meteorologische ERA5/SARAH-Daten | Atlite-Wetter-Cutout | Cutout NetCDF | **nicht nötig**, wenn fertige PECD-CF vorliegen |
| \`determine_availability_matrix\` | Landnutzungs-/Ausschlussmasken, Cutout, Netzregion | potenziell **geeignete Flächen**, keine stündlichen RES-CF | \`availability_matrix_{technology}.nc\` | **nicht nötig** für fest vorhandene Generatoren mit vorgegebener Leistung; wird nur gebraucht, wenn Standortpotenziale gebaut werden |
| \`build_renewable_profiles\` | Cutout, geeignete Flächen, Resource-Klassen und Netzregionen | \`capacity_factor\` je Wetterpixel, dann Kapazitäts-/Eignungs-gewichtete Aggregation in Busregion/Bin | \`profile_{technology}.nc\`: \`profile(year,bus,bin,time)\`, \`p_nom_max(bus,bin)\`, \`average_distance(bus,bin)\` | **hier** PECD native CF/Region/Profile Reader einschleusen, nicht Klimadaten mit unverändertem ERA5-Schema vortäuschen |
| \`build_hydro_profile\` | ERA5-Runoff, Länderflächen, EIA-Statistik | Runoff→Länderzufluss in MW | \`profile_hydro.nc\` mit \`inflow(countries,time)\` | durch expliziten PECD-/TYNDP-Hydro-Quell- und Intervalladapter ersetzen |
| \`build_electricity_demand\`, \`build_electricity_demand_base\` | national/DFT-Last | gesonderte zeitliche/regionale Lastverteilung (z.B. Bevölkerung/GDP) | Nachfrage \`(time,bus)\` | bei bereits vorhandenen Original-\`Load\`-IDs und verbindlichem DFT ggf. nur separate \`Load\`-ID-Zuordnung |
| \`cluster_electricity_demand\` | vereinfachte Busnachfrage und busmap | Nachfrage auf geclusterte Netzbusse umverteilen | \`electricity_demand.nc\` | **nicht** für unverändertes hochaufgelöstes Referenznetz laufen lassen |
| \`compose_network\` / \`add_electricity\` | \`networks/clustered.nc\`, Profile, Kraftwerks-/Kostendaten | legt **neue** Load/Generator/StorageUnit an; setzt \`p_max_pu\`/\`inflow\`; zusätzliche Modell-/Temporalschritte | \`networks/composed_{horizon}.nc\` | **nicht unverändert** auf vollständiges M0-Netz mit bereits existierenden Anlagen ausführen; sonst Doppelanlage/Änderung technischer Stammdaten |

**Zentrale Einschränkung für blindes „Datei tauschen“:** Der Standard-\`attach_wind_and_solar\` setzt \`p_nom_max\`, für Offshore auch \`average_distance\`, voraus und legt aus \`bus,bin\` Generator-IDs an. Der Open-TYNDP-2026-Generator liefert \`profile(time,bus,bin,year)\` mit \`bin=0\`, **ohne** automatisch alle Standard-Attributfelder. Standard-Datenersatz ist deshalb nicht in allen Fällen ein austauschbares NetCDF unter gleichem Dateinamen.

## 3. Wo Open-TYNDP 2026 räumliche PECD-Auflösung verliert

1. \`rules/sb.smk\` übergibt \`buses_tyndp = rules.build_tyndp_network.output.substations\` an \`clean_tyndp_pecd_data\`.
2. \`clean_tyndp_pecd_data.py\` liest für die TYNDP-Nodes Dateien \`<node>_CapacityFactors_<technology>_<horizon>.csv\` oder \`<technology> <node>.csv\`. Es wählt **pro Knoten** eine \`WS###\`-Spalte und schreibt \`(time,TYNDP_node)\`.
3. \`build_renewable_profiles_pecd.py\` transformiert zu \`profile(time,bus,bin=0,year)\`. **Keine native \`ORIG\`-PV-Pixel-/Technologie-zu-einzelner-CGMES-Generator-Zuordnung** in diesem Pfad belegt.

**Präzise Bewertung:** Open-TYNDP **nutzt PECD v4.2** bereits, aber im untersuchten Workflow **TYNDP-knoten-/regionenbezogene vorberechnete Daten**, nicht die gesamte räumliche Produktbreite des ursprünglichen CDS-Datensatzes. Ob die einzelnen TYNDP-Knoten genau PEON-/PEOF-Regionsgrenzen wiedergeben und ob die regionale CF-Quelle bereits vor dem Reader aggregiert wurde, ist **ohne reale TYNDP-CSV-Header/-Regionsmasken nicht vollständig beweisbar**. Eine numerische Differenz „Auflösung X statt Y“ darf nicht erfunden werden.

## 4. PECD-4.2-Produktauflösungen: entscheidend für minimalen Delta

| Produkt | Wetter-/Climatemodell-Grundauflösung | Offiziell veröffentlichter stündlicher CF / hydrologischer Output | Empfohlene Verarbeitung |
|---|---|---|---|
| Wind Onshore (WON) | meteorologische Rasterdaten 0,25° | **PEON / P2ON** regionale CF (MW/MW), mit Technologie-/HubHeight/ResourceGrade | Original-PyPSA-Generatorstandort → PECD-Region, deren bestehender CF als \`p_max_pu\`; **keine fingierte 0,25°-Wind-CF** |
| Wind Offshore (WOF) | meteorologische Rasterdaten 0,25° | **PEOF / P2OF** regionale CF (MW/MW) | Windpark-Geografie/Quell-ID, **nicht** landseitiger Anschlussbus |
| Photovoltaik (SPV) | Raster 0,25° | **ORIG-Raster NetCDF** (0,25°) sowie regionale CF \`NUT0/NUT2/SZON/PEON/P2ON\`, PV-Varianten (MW/MWp) | Griddiertes \`ORIG\` bei real belegter PV-/Anlagenposition; ordentliche PV-DC-MWp-vs.-AC-MW-Semantik; regionale PV nur als qualifizierter Fallback mit Herkunft, **nicht** stillschweigend |
| Hydro (HRI, HRR, HPI, HOL) | hydrologische Eingangsdaten aus Klimamodell | überwiegend **SZON** mit **wöchentlicher MWh-Energie**, nicht native stündliche Asset-Zuflüsse | native Quelle/Intervall → Wasserkraftgebiet→existierendes Hydro-Asset mit belegten Anteilen und Energieerhaltung |
| Temperatur/Last | nach Variable regional/griddiert | Temperatur/DFT sind von fixen Lastzeitreihen zu trennen | Lastzeitreihen nur aus der tatsächlich verbindlichen DFT-/TSO-Quelle für vorhandene \`Load\`-IDs; nicht automatisiert aus Wind-/PV-CF ableiten |

**Wichtiger methodischer Schluss:** Die IoSN-Publikation nennt die **Wetterdatenbasis** räumlich/zeitlich hochaufgelöst. Die tatsächlichen *bereits modellierten Energieindikatoren* sind je Technologie verschieden aufgelöst. Die Unterscheidung ist verbindlich. Eine behauptete feinere Wind-CF-Quelle muss durch Dateien nachgewiesen oder über ein separat qualifiziertes meteorologisches Windmodell abgeleitet werden.

## 5. Kleinste fachlich richtige Softwareänderung

### Pfad A – Projektfall (M0 hat fertiges elektrisches Netz + alle Generatoren/Loads/Hydro bereits)

**Minimal-Datenfluss:**  
\`M0 network (unchanged) + PECD native products -> PECD normalized profiles -> geospatial profile-to-existing-asset join -> PyPSA dynamic attrs -> same network + time-series -> M2 downstream\`.

Konkret:
1. **Snakemake Source Switch**: \`profile_source = {atlite|pecd_v4_2}\` als *neue projektseitige Konfiguration*, nicht vorbestehende Upstream-Option. Bei PECD-CF: nur neue \`retrieve/normalize_pecd_profiles\` und für Hydro \`normalize_pecd_hydro\`; keine \`build_cutout\`-/Eignungsflächen-Regel im aktiven Pfad. PECD-Metadaten und Source-Hashes Pflicht.
2. **Räumlicher Crosswalk**: vorhandene \`n.generators\`, \`n.buses.x/y\` (nur qualifiziert als tatsächlicher Anlagenstandort), ggf. externe Anlagenkoordinate, PECD-Polygon-/Region-/Rastermaske, \`carrier\`/Technologievariante → \`asset_profile_map\`. Das ist **die eigentliche neue Funktion**, wiederverwendbar und quellenunabhängig. Regionale Wind-CF werden nicht künstlich interpoliert. Auflösung auf der meteorologischen Seite bleibt Quelleigenschaft.
3. **Ein dynamischer Attribute Writer**: \`n.generators_t.p_max_pu\` (Wind/PV und entsprechend qualifiziert RoR), \`n.storage_units_t.inflow\` (nur existierendes StorageUnit-Modell), \`n.loads_t.p_set\` nur mit geprüfter DFT-Last-ID-Quelle. Keine \`n.add("Generator"...)\`, keine \`n.add("Load"...)\`, keine Änderung an Leitungen/Bus/Buszuordnung/\`p_nom\`. Kollisions-/Overwrite-Gates für bereits bestehende Zeitreihen.
4. **Netz-Daten-Lifecycle**: \`pypsa.Network(reference.nc)\` und \`export_to_netcdf\` wie bisher; strikte Zeitindizes/UTC-Provenienz, Source-Coverage, statische Fingerprint- und Hydro-MWh-Checks. Ein full-resolution-Netz je \`(planning_horizon,weather_id)\`, keine vorherige Netz- oder Stundenaggregation.
5. **Rechner**: PyPSA-Core, LPF/AC-PF/OPF/Optimierungscode unverändert. Verfügbarkeit ist noch kein Dispatch; AC/LPF nur mit bilanziertem Betriebspunkt.

**Keine Änderung an:** PyPSA-Core, Lastflussformulierung, Netzwerkobjekten, Atlite-Algorithmen, Clustering (liegt später in M2), Wetterjahrauswahl.

### Pfad B – Standard PyPSA-Eur berechnet zusätzlich selbst Wind-/PV-Kapazitäten und legt Generatoren an

Wenn der vollständige **Standard-PyPSA-Eur-Workflow** weiterlaufen soll, muss der PECD-Adapter zusätzlich eine kompatible \`profile_{technology}.nc\`-Schnittstelle mit \`bus,bin,time,year\` und ggf. \`p_nom_max\`/\`average_distance\` bereitstellen oder die Stellen in \`attach_wind_and_solar\` explizit für EXOGENE Profile anpassen. Dieses Modell nutzt ggf. eigene geklusterte \`networks/clustered.nc\` und erstellt Generatoren; **es ist nicht gleichbedeutend mit der unveränderten M0-Originalnetzkomponentenstruktur**. Ein Dateinamen-Tausch allein garantiert weder die korrekte Erzeugungsauflösung noch korrekte Anlagenidentitäten.

**Empfehlung:** Für den aktuellen IoSN-M1-Zweck **Pfad A**, mit Wiederverwendung der PyPSA-Eur-/Open-TYNDP-Reader-Snippets. Für allgemeine PyPSA-Eur-Konfigurierbarkeit künftig Pfad B als separaten optionalen Integrationslayer planen, **keine Rückänderung des Upstream-Kernworkflows**.

## 6. Formale Mapping-/Zeitreihenverträge

- Für Generator \`g\` aus dem vorhandenen Netz \`n.generators\`, zugelassene PECD-Quellprofile \`r\`, Gewichte \`A[g,r]\`:
  \`CF_g(t)=Σ_r A[g,r] CF_{r,technology(g),weather_id}(t)\`; \`Σ_r A[g,r]=1\` bei nachgewiesener Multi-Region-Kapazitätsverteilung; single-profile default Gewicht 1.
  \`n.generators_t.p_max_pu[t,g]=CF_g(t)\`. Der elektrische \`Generator.bus\` und \`Generator.p_nom\` bleiben identisch. Wind-Region 1 kann viele elektrische Busse bedienen.
- PV aus \`MW/MWp\` bedarf dokumentierter DC→AC-Basis; ein AC-Clip ist eine qualifizierte Modellannahme, kein genereller PECD-fester Umrechnungsfaktor.
- Hydro: \`inflow_{asset,t}\` nur für das tatsächlich vorhandene Wasser-Speichermodell; \`Σ_t P_{inflow,t} Δh=E^{model}_{asset,sourceinterval}\`, source-native Energie bilanziert getrennt. RoR als qualifizierte Erzeugungsverfügbarkeit und nicht als tatsächliche Einspeisung.
- Last/DFT: Regio-Last nur mit belegter Lastkapazitäts-/elektrischer Verteilung auf vorhandene \`n.loads\`, nicht aus Wetterkoordinaten allein.
- Genau fünf **vorher festgelegte** Wetterdatensätze; keine neue Auswahl, keine Zeitreduktion, kein automatischer \`fillna(0)\`-/Planning-Horizon-Fallback. Der Open-TYNDP-2026-Standard nennt bislang drei regulär befüllte Wetter-WS je Horizont; kein Nachweis über das externe Fünfer-Set.
- Originale PECD-/Hydro-Dateien und versionierte technische Relationen als getrennte Input-Pakete; M0 hat nur Netzimport-/Stammdatenverantwortung.

## 7. Abnahmetests und organisatorische Konsequenz

| Test | Minimaler PASS |
|---|---|
| Source/Mode | Bei \`source=pecd_v4_2\` keine ERA5-Cutout-Neuberechnung von bereits verfügbaren offiziellen CF; Source manifest/hash und Produktauflösung vollständig |
| Wind | PEON/P2ON/PEOF/P2OF und Technologievariante korrekt; keine Behauptung nativer 0,25°-Wind-CF |
| PV | \`ORIG\`-Grid, Standort-/CRS-/Zellzuordnung und MWp/AC; regionales Produkt nur dokumentiert verwendet |
| Hydro | Original-SZON-/Intervallenergie, Basin-/Anlagenanteile, MWh→MW und existierende Speicherports korrekt |
| Static | Identische vorher/nachher M0-Komponententabellen, \`bus\`, \`p_nom\`, Leitungen, Trafos, Links, Store/Generator/Loads |
| Time | Exakte Snapshotabdeckung je extern vorgegebenem WS und korrekter Zeitbasis, keine stumme Füllung mit PyPSA-Defaults |
| Integration | NetCDF roundtrip, keine Erzeugung von doppelt vorhandenen Generatoren/Loads, kein unzulässiger Attribut-Overwrite, kein M2-Clustering |

**MA-4F Focus Update:** Zuerst prüfen, ob die schon gelieferten MA-2-/MA-3-Adapter direkt als alternative **PyPSA-Eur-Profilquelle** mit bestehendem M1 Composer genutzt werden können. Baue nur die minimale notwendige Source-Switch-/Manifest-/Spatial-Join-/Dynamic-Writer-Schicht. Die bereits getesteten Parser nicht duplizieren. Die Unterschiede von Pfad A zu Pfad B in einer Versionsmatrix dokumentieren.

**MD-1 Focus Update:** Unterscheiden ob tatsächliche Projektinputdateien (A) TYNDP-node/prebuilt, (B) PECD-4.2-native Zonenprodukte oder (C) \`ORIG\`-Raster-Photovoltaik sind. Die „hochauflösende Variante“ nicht aus dem generischen IoSN-Wording annehmen. Reale Dateien und ihren Raumbezug/Quellvarianten müssen vor Real-PASS belegt sein.

**Governance-Verdikt:** \`PYPSA_CORE_UNCHANGED__PYPSA_EUR_INPUT_PIPELINE_PECD_SWITCH__M1_NATIVE_SPATIAL_PROFILE_MAPPING\`. **Kein** genereller Workflow-Neubau; allerdings **konkrete** Daten-/Schema-Anpassung zwingend, da das Standard-PyPSA-Eur-Profilformat und das Open-TYNDP-Knotenformat keine 1:1-Garantie haben.
