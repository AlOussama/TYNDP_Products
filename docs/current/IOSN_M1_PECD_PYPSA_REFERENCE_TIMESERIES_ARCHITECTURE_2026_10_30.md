# IoSN / TYNDP — M1 Softwarearchitektur: PECD- und Hydro-Zeitreihen für das detaillierte PyPSA-Referenznetz

**Datum:** 30.10.2026  
**Status:** ARCHITECTURE_PROPOSAL — statische Quellcode-/Dokumentationsprüfung; **keine Implementierung, keine Datenausführung, keine numerische Qualifikation**  
**Repository:** AlOussama/TYNDP_Products  
**Baseline dieses Repositories:** 1595d6d38e77804760612621657721b3699d2fea  
**Open-TYNDP Referenz:** open-energy-transition/open-tyndp @ 5b25904496150b889b321dd8d76f393ef09a0f2e  
**PyPSA-Eur Referenz:** PyPSA/pypsa-eur @ 1526bb820e25a9faa61f32b00bfc77dd05db6b2e

## 1. Executive decision

M1 ist ein eigenständiges **PECD-/TYNDP-to-PyPSA Time-Series Integration Module**. Es verwendet ein von M0 geliefertes, bereits CGMES-konvertiertes, elektrisch qualifiziertes **hochaufgelöstes PyPSA-Netz** einschließlich der bestehenden Generatoren, Lasten, Speicher, ihrer Anschlussknoten, technischen Eigenschaften und verfügbaren Geokoordinaten. M1 **erzeugt keine Topologie, keine Kraftwerke und keine Netzaggregation**. Es ergänzt ausschließlich zeitvariable Eingaben an existierenden PyPSA-Komponenten, dokumentiert die Profile-to-Asset-Zuordnung und qualifiziert die Integrität.

**Beschlussvorschlag:** Kein Fork/Change von PyPSA-Core; keine Ausführung der Standard-PyPSA-Eur-Pipeline von base über simplified/clustered zu composed für M1. Stattdessen schlanker, eigenständiger Snakemake-DAG, der vorhandene Reader/Normalisierungslogik aus Open-TYNDP soweit kompatibel wiederverwendet und einen **neuen M0-Asset-ID-zu-PECD-Profile-ID-Mapper** und einen **invarianten PyPSA Time-Series Composer** hinzufügt.

Die fünf Wetterdatensätze sind **extern festgelegt** und bleiben unverändert. M1 wählt oder reduziert keine Wetterjahre und keine Stunden. M2 (Netzaggregation) ist ein vollständig separater Folgeprozess.

## 2. Verbindliche Modulgrenzen

| Modul | Owner/Verantwortung | Verbindliche Grenze |
|---|---|---|
| **M0 CGMES Preprocessing** | separater Architektur-/Implementierungsprozess | Liefert validiertes statisches Netz, dauerhafte Original-/PyPSA-IDs, vorhandene Generator- und Speicherkomponenten, Bus-Geometrie, Anschlusszuordnung |
| **M1 Zeitreihenintegration (dieses Dokument)** | PECD/TYNDP-Datenparser, Profile-to-Asset-Zuordnung, Hydro-Inflow-Mapping, kontrollierte Zeitreihen-Injektion, QA | Darf die elektrische Topologie, Anschlussknoten und technischen Stammdaten nicht verändern |
| **M2 Netzaggregation** | separater Chat/Owner | Liest nur den qualifizierten M1-Output, wendet eigenständige Aggregationsmethodik an; M1 implementiert **keine** Clustering-Regel |

Voraussetzung: Die fachlich maßgeblichen Anlagen-/Knoteninformationen aus M0 sind korrekt. Bei abweichenden PECD-/TYNDP-Anlagen-IDs wird eine explizite Zuordnungsdatei erforderlich; die technischen Stammdaten werden nicht aufgrund der Zeitreihenquelle überschrieben.

**Nicht Gegenstand von M1:** Erzeugung des CGMES-Netzes, CGMES-Komponenten-Mapping, Bus-Vereinfachung, Zuordnung zukünftiger nicht existierender Anlagen, PTDF-/LODF-Clustering, elektrische Ersatzimpedanzen, N-1-Ersatzkapazitäten, Wetterjahrauswahl und vollständige Marktdispatch-Optimierung.

## 3. Verifizierter Softwarebestand und Reuse-Assessment

### 3.1 PyPSA-Core und PyPSA-Eur

**PyPSA-Core direkt nutzbar:** Die vorhandenen Komponenten und Attribute **Generator.bus**, **Generator.p_nom**, **Generator.p_max_pu / generators_t.p_max_pu**, **Load.p_set / loads_t.p_set**, **StorageUnit.inflow / storage_units_t.inflow** sowie entsprechende zeitabhängige Werte für thermische Verfügbarkeit. Ein NetCDF-Import/Export des kompletten Netzes ist vorhanden. Keine Core-Änderung für die beschriebene Aufgabe erkennbar.

**PyPSA-Eur:** Snakemake trennt Datenbeschaffung, Profilkonstruktion und Network Composition. In der aktuellen Generation folgt der reguläre Workflow jedoch base -> simplified -> clustered -> composed -> solved. Die nativen Regeln **build_cutout**, **determine_availability_matrix**, **build_renewable_profiles** und **build_hydro_profile** nutzen Atlite- und PyPSA-Eur-Regionen. **add_electricity/compose_network** erzeugt oder verändert Anlagen und startet vom geclusterten Netz. Dieser Hauptpfad ist für das bereits fertige M0-Netz nicht geeignet. Datenformatkonventionen und Python-Hilfsfunktionen sind dennoch teilweise wiederverwendbar.

Quellen:
- [PyPSA-Eur Workflow/Regeln](https://pypsa-eur.readthedocs.io/en/latest/rules/electricity/)
- [PyPSA-Eur Changelog v2026.09.0](https://pypsa-eur.readthedocs.io/en/stable/release_notes/)
- [Upstream compose.smk](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/rules/compose.smk)
- [Upstream add_electricity.py](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/add_electricity.py)

### 3.2 Open-TYNDP — tatsächlich vorhandene PECD-Integration

Open-TYNDP enthält bereits folgende produktive Quellcodebausteine für TYNDP **2024**:

| Quelle (alle am oben fixierten Open-TYNDP-Commit) | Nachgewiesener Funktionsumfang | M1-Disposition |
|---|---|---|
| [rules/sb.smk](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/rules/sb.smk) | Rules retrieve_tyndp_pecd, prepare_pecd_release, clean_pecd_data, build_renewable_profiles_pecd, clean_tyndp_hydro_inflows, build_tyndp_hydro_profile | Snakemake- und Abhängigkeitsmuster **übernehmen/adaptieren** |
| [scripts/sb/prepare_pecd_release.py](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb/prepare_pecd_release.py) | Filtert PECD-Dateien nach vorgegebenen Klimajahren und Planungshorizonten | Reuse nach Prüfung von Eingabeformat und Version |
| [scripts/sb/clean_pecd_data.py](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb/clean_pecd_data.py) | PECD-CSV, Technologie-/Klima-/Planungsjahr, TYNDP-Knoten als Spalten, Ergebnis CSV | **Parser wiederverwenden**, TYNDP-Knoten-/Busmap-Abhängigkeit ersetzen |
| [scripts/sb/build_renewable_profiles_pecd.py](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb/build_renewable_profiles_pecd.py) | NetCDF-Profile mit Dimensionen time, bus, bin, year | Transformation zum **profile_id**-basierten M1-Vertrag adaptieren |
| [scripts/sb/clean_tyndp_hydro_inflows.py](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb/clean_tyndp_hydro_inflows.py) | TYNDP-/PEMMDB-Hydro-Inflow: Tages-/Wochenenergie, zeitliche Hochrechnung auf MW, Knotenbezug | Nur **Einheiten-/Zeitlogik als Vorlage**; neue Asset-Zuordnung/QA |
| [scripts/sb/build_tyndp_hydro_profile.py](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb/build_tyndp_hydro_profile.py) | NetCDF mit time, bus, year, hydro_tech | Normalisierungsidee übernehmen, M1-Output direkt pro existierender Asset-ID |
| [config/config.tyndp.yaml](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/config/config.tyndp.yaml) | Schalter pecd_renewable_profiles und pemmdb_hydro_profiles, Technologie- und Datenjahrvorgaben | Konfigurationsprinzip übernehmen, nicht blind Defaults übernehmen |
| [scripts/sb/build_pemmdb_data.py](https://github.com/open-energy-transition/open-tyndp/blob/5b25904496150b889b321dd8d76f393ef09a0f2e/scripts/sb/build_pemmdb_data.py) | PEMMDB-Kapazität, p_min_pu und p_max_pu auf TYNDP-Knoten/Technologien | Nur bei begründetem Zusatzbedarf; M0-Stammdaten sind maßgeblich |

**Entscheidende Einschränkungen:**
1. Das Feld **bus** in den Open-TYNDP-PECD-Profilen bezeichnet **TYNDP-Knoten/Regionen, nicht die Original-CGMES-Bus-ID**. In clean_pecd_data wird insbesondere **busmap_cluster_network.csv** verwendet. Deshalb ist ein neuer Mapping-Layer zwingend.
2. Die betrachtete Open-TYNDP-Datenpipeline ist an **PECD v3.1 / TYNDP 2024** gebunden, mit dateinamen- und technologieabhängigem Reader; für die tatsächlichen IoSN-/PECD-Produkte darf Format-/Versionskompatibilität nicht unterstellt werden.
3. **Hydro kommt dort ausdrücklich aus den TYNDP-2024-PEMMDB-Hydro-Inflows**, nicht aus derselben PECD-CF-Reihe wie Wind und PV. Für unsere Datenquelle muss das separat spezifiziert werden.
4. clean_pecd_data kann nicht vorhandene Daten nach Konfiguration mit **zero** bzw. einem Aggregatwert auffüllen; für fehlende Klimajahre existiert eine **Fallback-Logik**. Solche stillen Ersatzmechanismen sind im Referenzmodell nicht zulässig.
5. Ein vollständiges, direkt verfügbares CGMES-Originalbus-zu-PECD-Mapping ist im geprüften Open-TYNDP-Workflow **nicht nachgewiesen**. Ebenso ist keine Ausführung dieser externen Regeln in unserem Projekt erfolgt.
6. Das Script build_renewable_profiles_pecd enthält ausdrücklich einen noch nicht implementierten Hinweis auf PECD-Hydro; dieser Hinweis darf nicht als Hydro-Implementierungsnachweis gewertet werden.

Quellen: [Open-TYNDP TYNDP-2024-Dateninventar](https://open-tyndp.readthedocs.io/en/latest/tyndp_2024/), [Open-TYNDP Rules](https://open-tyndp.readthedocs.io/en/latest/sb_rules/), [Open-TYNDP Configuration](https://open-tyndp.readthedocs.io/en/latest/configuration/).

### 3.3 Reuse-vs.-Build-Entscheidung

- **Direkt nutzen:** PyPSA-Netzcontainer, Generator-/StorageUnit-/Load-Zeitreihen, pandas/xarray, Snakemake, NetCDF-Export; Open-TYNDP-Methoden für Parsen/Umformen nach Prüfung.
- **Gezielt adaptieren:** Open-TYNDP PECD-Dateileser (Versions- und Zeitachsen-Adapter), Technologie-Mapping, TYNDP-Hydro-Einheiten und ggf. Wochen-/Tages-Zeitauflösung.
- **Neu definieren/entwickeln:** Profile-ID-Registry unabhängig von TYNDP-Knoten, Zuordnung existierende Generator-ID -> PECD-Profil, hydrologische Zuordnung an bereits existierende PyPSA-Assets, statisch unverändernder Time-Series Composer, Gate-basierte Datenvalidierung.
- **Bewusst nicht verwenden:** Wiederholte Leistungsschätzung über powerplantmatching, Erzeugen neuer Wind-/PV-Generatoren in add_electricity, Wiederaufbau per build_tyndp_network, standardmäßige Vorvereinfachung/Clustering, land-use-Potenzialberechnung bei bereits vorhandenen Anlagen, automatische Null- oder Fallback-Profile.
- **Lizenz/Provenienz:** Wiederverwendeten Quellcode vor Übernahme gegen die geltenden Lizenz- und Datenzugangsvorgaben prüfen, Herkunft und Originalcommit nachführen; Dokumentieren/Verlinken ist nicht gleich Codeübernahme.

## 4. Fachliches Zielmodell und mathematische Zuordnung

### 4.1 Elektrische und meteorologische Auflösung strikt trennen

- Elektrische Auflösung: **jede vorhandene M0-Generator-, Last- und Speicher-ID** mit festem Anschlussbus.
- Meteorologische Auflösung: durch das **tatsächlich gelieferte** PECD-Produkt (Raster, PECD-Region, TYNDP-Knoten oder anderes Datengebiet) bestimmt.
- Gleiche Profilkurven für Anlagen in derselben Wetterregion sind zulässig; daraus folgt **keine elektrische Zusammenlegung**.
- Eine Bus-Geokoordinate kann zur Zuordnung eines PECD-Polygons dienen, **aber nur, falls diese Koordinate den Anlagenstandort repräsentiert**. Für Offshore-Anlagen, Kabel-Anlandepunkte und dezentrale Sammelanschlüsse kann ein anderer geografischer Standort maßgeblich sein.
- Bei vorliegenden expliziten Zuordnungskennungen haben diese Vorrang vor Point-in-Polygon; eine willkürliche Nearest-Centroid-Zuordnung ist nicht der Default.

### 4.2 Renewable profile mapping

Eingaben: Menge bestehender Generatoren G, Menge verfügbarer PECD-Profile R, Technologiemapping K, festgelegte Wetterdatensätze S, Zeitindex T.

- A(g,r,k): validierte gewichtete Zuordnung eines bestehenden Generators g zu Profil r der Technologie k. In der Regel genau ein Profil je Generator und Datensatz. Mehrfachgewichte nur mit expliziter Quelle und nachvollziehbarer Begründung.
- CF(r,k,s,t): Quellkapazitätsfaktor, dimensionslos.
- CF(g,s,t) = Summe über (r,k) von A(g,r,k) * CF(r,k,s,t).
- P_avail(g,s,t) = p_nom(g) * CF(g,s,t).

PyPSA-Ziel: **n.generators_t.p_max_pu.loc[t,g] = CF(g,s,t)**. **n.generators.p_nom, .bus und übrige statische Anlagenparameter bleiben erhalten**. Tatsächlicher Dispatch ist **nicht** gleich Verfügbarkeit. Eigenständige vorgegebene Dispatchwerte dürfen nicht versehentlich überschrieben werden.

Für mehrere technische Profile am selben Anschluss (z. B. PV-Rooftop vs. Utility) muss die bestehende Anlagen-/Trägerdifferenzierung korrekt sein. Fehlt sie, ist keine beliebige Profilzuordnung zulässig; es braucht einen gekennzeichneten fachlichen Entscheidungsfall.

### 4.3 Hydro ist kein Wind-/PV-CF-Import

Unterscheide:
- **Run-of-river:** abhängige Einspeisefähigkeit; abhängig vom vorhandenen Modell als Generator-p_max_pu oder speicherkompatibler Zufluss.
- **Reservoir, Pondage, offene Pumpspeicher:** natürlicher Zufluss an bestehendem Speicher-/Store-Modell; bestehende Energie-/Wirkungsgradparameter bleiben erhalten.
- **Geschlossene Pumpspeicher:** kein künstlicher natürlicher Zufluss.
- **PECD-Kapazitätsfaktor vs. TYNDP/PEMMDB-Hydro Inflow:** fachlich verschiedene Eingangstypen; Hydro-Quelle und Metadaten separat versionieren.

Bei Energie E(region,technology,period) in MWh und begründeten Anteilen alpha(asset,region,technology) erfolgt eine energieerhaltende Abbildung in die jeweils richtige PyPSA-Energie-/Leistungseinheit; bei konstantem Profil über ein Intervall mit Dauer delta_h (Stunden):
P_inflow(asset,t) = alpha * E / delta_h.
Prüfung für jedes Originalintervall: Summe_t P_inflow(asset,t) * delta_t = alpha * E.
Eine aus Wochen-/Tagesenergie erzeugte Stundenzeitreihe ist **eine ausdrücklich dokumentierte Annahme**, keine gemessene Stundenauflösung. Keine unkontrollierte Füllung fehlender Regionen mit 0.

**Kritische Source-Frage vor Implementierung:** Welche Hydro-Quelle liegt tatsächlich vor: TYNDP-2024 PEMMDB Hydro Inflows mit Tages-/Wochenenergien, ein neuerer Hydro-Datensatz oder bereits anlagenscharfe Zeitreihen? Diese Entscheidung ändert den Parser, nicht die M1-Modulgrenze.

### 4.4 Zeitszenarien

Fünf extern eingefrorene Wetterdatensätze W01–W05 (nur Platzhalter-IDs). Keine Neuauswahl, kein Ranking, keine Reduktion. Eigenständiger Index für **Wetterdatensatz**, **Klimajahr**, **Planungshorizont** und **Zeitstempel**. Ursprungszeitachse, Zeitzonenannahme, Schaltjahr und Zeitintervalldauer als Metadaten speichern. Fehlende Klima-/Planungsjahre: **fail closed**, außer es existiert eine explizite, durch Owner freigegebene Zuordnung. Open-TYNDP-2009-Fallback nicht übernehmen.

Nicht alle PECD-CF sind ohne Prüfung auf [0,1] zu begrenzen: Sonderformen wie CSP mit thermischer Speicherung können in TYNDP-Daten CF > 1 aufweisen. Für gewöhnliche Wind-/PV-Profile gilt ein fachlich definierter Wertebereich; jede Abweichung wird vor dem Mapping geprüft.

## 5. Schnittstellen / Datenverträge

### 5.1 M0 -> M1: Eingang

| Eingang | Erwarteter Mindestinhalt | Prüfstatus |
|---|---|---|
| reference_network.nc | Validiertes PyPSA-Netz mit statischer Topologie, bestehenden Generatoren/Loads/StorageUnits und aktuellen technischen Parametern | M0-Liefergegenstand; **noch nicht hier verifiziert** |
| asset_registry.parquet | Eindeutige bestehende Asset-IDs, Carrier/Subtyp, Bus-ID, ggf. Standort (vorhandene Bus- und Anlagenkoordinaten) | Contract; wo möglich aus Netz ableitbar |
| identity_map.parquet | CGMES-mRID -> PyPSA-ID, stabile Referenz für Vergleich mit Quelle | M0-Vertrag |
| m0_manifest.yaml | Netzstand, Revision, Modellierungsgrenzen, elektrische Qualifikation | M0-Vertrag |

Das genaue Dateischema ist mit M0 zu harmonisieren. M1 benötigt **kein CGMES-RDF/XML** und darf Module-0-Rohdaten nicht als eigene Topologie parsen.

### 5.2 Quellinput -> M1

- source_manifest.yaml: Anbieter/Produkt/Version, ggf. Lizenz, Quelle/Hash, Zielhorizont, die fünf vorgegebenen Wetterdatensätze, ursprüngliche regionale Auflösung, Zeitindexkonvention.
- pecd_profiles: Profil-ID x Technologie x Planungshorizont x Wetterdatensatz x Zeit; Datenwert als normierter CF.
- pecd_geometry_or_region_mapping: Polygone/Regionencodes/Rasterzellen bzw. offizielle Verbindung zwischen Inputregionen und Anlagen. Wenn nicht vorhanden, als offener Datenvertrag markieren.
- hydro_inflows: Quelle x hydro_tech x Region/Asset x Zeitintervall x Energie/Leistung.
- Optional: vorgegebene DFT-Lastzeitreihen und thermische Verfügbarkeiten, soweit zum M1-Abgabeumfang gehörig; deren Quellen werden nicht aus Wetter-Rohdaten nachsynthetisiert.

### 5.3 M1-interne kanonische Zwischenartefakte

| Artefakt | Eindeutige Dimensionen / Schlüssel | Bedingung |
|---|---|---|
| profile_catalog.parquet | profile_id, source_version, technology, region_id, planning_horizon, weather_id, unit | Profil-ID unabhängig von PyPSA-Bus-ID |
| asset_profile_map.parquet | asset_id, profile_id, assignment_method, spatial_source, source_ref, mapping_quality | keine verdeckten Nächstpunkt-Annahmen |
| renewable_cf_{weather_id}.parquet oder .zarr | time x **existing generator_id** | 1:1 mit Zielgeneratoren; Werte geprüft |
| hydro_inflow_{weather_id}.parquet oder .zarr | time x **existing storage/hydro asset_id** | korrektes Energie-/Leistungsmodell |
| mapping_audit.parquet | unmapped/ambiguous/assumed mappings, Quellen und Begründungen | keine verlorenen Datensätze |
| qa_report.json | Gates, Abweichungen, Source-Hashes, Lücken, PASS/FAIL | maschinenlesbar |

Die konkrete physische Datei-/Arraytechnologie (NetCDF/xarray, Parquet, Zarr) wird anhand Datenvolumen/Performance in Makro 2 entschieden; **die logischen Datenverträge werden hier eingefroren**.

### 5.4 M1 -> M2: Ausgabe

- reference_grid_full_{planning_horizon}_{weather_id}.nc mit allen Original-M0-Komponenten und den zugeordneten Zeitreihen.
- profile_catalog, asset_profile_map, weather_manifest, Hydro-Methodik-Parameter und Validierungsreport.
- optional unveränderte statische M0-Basis als dedupliziertes Artefakt plus referenzierte Zeitreihenpakete; Export eines vollständigen PyPSA-Netzes als Pflicht.
- Keine Busmap, kein reduziertes Netz, keine Ersatzimpedanz im M1-Output.

## 6. Sollarchitektur: getrennte Snakemake-Pipeline

### 6.1 Abhängigkeitsgraph

    [M0: detailed_reference.nc + Asset IDs] ---+
                                                |
    [PECD source manifest + fünf feste Sets] -> [normalize_pecd_profiles]
                                                |
                                                +--> [map_profiles_to_assets] --+
                                                                                 |
    [TYNDP/PEMMDB Hydro Inflows] ----------> [prepare_hydro_inflows] ------------+
                                                                                 |
    [optionale DFT-/Thermal-Zeitreihen] ----------------------------------------+
                                                                                 v
                                             [compose_full_reference_timeseries]
                                                                                 |
                                             [validate_m1_reference] ------------+
                                                                                 |
                                                                                 v
                                             [full_reference_*.nc + QA + Ledger]
                                                                                 |
                                                                                 v
                                             [M2 separate Owner/Chat]

### 6.2 Kandidatenregeln (sind noch keine vorhandenen Snakemake-Rules)

| M1 Rule | Input | Output | Reuse |
|---|---|---|---|
| normalize_pecd_profiles | PECD-Dateien, Version/Technology/Time Contract | versionierte CF-Arrays + Profilkatalog | Open-TYNDP clean_pecd_data / build_renewable_profiles_pecd nach Formatprüfung |
| map_profiles_to_assets | M0-Assetliste, PECD-Regionen/Zuordnungen, Technologiecrosswalk | geprüfte asset_profile_map | **neu** |
| prepare_hydro_inflows | Hydro-Quellwerte, hydro_model_type, M0-Assetliste | Hydro-Inflow-Arrays, Energieledger | Open-TYNDP clean_tyndp_hydro_inflows / build_tyndp_hydro_profile adaptiert |
| compose_full_reference_timeseries | unverändertes M0-Netz, CF-Arrays, Hydro-Arrays, optionale Last-/Thermal-Profile | vollständiges PyPSA-Referenznetz für gegebenes Szenario | **neu**, nutzt direkte PyPSA APIs |
| validate_m1_reference | M0- und M1-Netz, Kataloge, Mapping, Quellaggregate | Gate-Bericht + Fehlerliste | **neu** |

Ein optionaler Download-/Cache-Rule kann vorgeschaltet werden. M1 bindet **nicht** den upstream compose_network-DAG, kein build_tyndp_network, kein build_cutout, kein determine_availability_matrix, kein cluster_network.

### 6.3 Python-Komponentenschichten

1. **Data adapters:** Eingabeprodukte lesen und nach gemeinsamen Zeit-/Technologie-/Regionendimensionen normalisieren.
2. **Domain mapping:** Explizite Profile-zu-Asset-Zuordnung, getrennte Geografie- und Typauflösung, Audit.
3. **Time-series compiler:** Arrays für existierende Generator-/Hydro-/Load-IDs in PyPSA-kompatibler Form.
4. **Non-mutating composer:** M0-Netz laden, ausschließlich freigegebene *time-varying* Attribute schreiben, statische Fingerprints vergleichen, exportieren.
5. **Validation & provenance:** unabhängige Grenzwerte, Nullstellen, Conservation, Kalender- und Source-Traceability.

**Kein produktiver Code in diesem Makro.** Die obigen Namen sind Schnittstellenvorschläge.

## 7. Pflichtgates zur Abnahme

| Gate | Harte PASS-Bedingung |
|---|---|
| M1-G0 Source Traceability | Wetterdatensätze, Produktversion, Lizenz, Einheiten, Regionencodes und Zielhorizonte vollständig dokumentiert; fehlende Daten als FAIL |
| M1-G1 Static invariance | Vorher/nachher identische geordnete IDs und statische Attribute von Buses, Lines, Transformers, Links, Generators, Loads und Speicherkomponenten; getrennte Whitelist für bewusst schreibbare Zeitreihen |
| M1-G2 Profile Mapping | Jeder wetterabhängige Generator hat genau die fachlich korrekte Profil-/Technologiezuordnung, kein stiller Nearest-Node und keine fehlenden IDs |
| M1-G3 Renewable semantics | p_max_pu-Profil, Zeitachse, Einheiten, Quellprofilwerte und p_nom unverändert; P_avail = p_nom * CF |
| M1-G4 Hydro energy | Hydro-Typen und Zielkomponenten korrekt, Energieintegral pro ursprünglicher Quelle/Intervall erhalten, keine Inflow-Erfindung bei closed-loop PHS |
| M1-G5 Scenario/time | Exakt die fünf **vorgegebenen** Szenario-IDs, keine heimliche Wetterjahrersetzung, keine unautorisierte Zeitaggregation, DST/Leap/UTC geklärt |
| M1-G6 Reproducibility | Quelle + Mapping + Rules + Config liefern identische Datenhashes/Netzgrößen, NetCDF roundtrip und validierte PyPSA-Netzkonsistenz |
| M1-G7 Optional physical qualification | Bei vorgegebenen bilanzierten Dispatch-/Load-Snapshots separate DC-/AC-Lastfluss-Plausibilisierung; **nicht** als Vorbedingung für reine Profilintegration missverstehen |

Ein bestandener Import belegt **nicht** automatisch, dass eine vollständige Marktoptimierung durchgeführt wurde oder die PECD-Windprofile eine Anlage-auf-den-Meter-genaue Meteorologie enthalten.

## 8. Datenrisiken und erforderliche Owner-Entscheidungen

| Risiko / Frage | Behandlung in M1 | Status |
|---|---|---|
| PECD v3.1 (Open-TYNDP 2024) vs. tatsächlich gelieferte PECD-/TYNDP-Produkte | Quellversion und Dateischema vor Adapterreusage abgleichen | OFFEN: Dateiexemplare fehlen |
| PECD-Region/Node-Name vs. CGMES-mRID | offizielles Mapping oder Georeferenzpolygon; eigenständige ID-Tabelle | OFFEN: Zuordnung im gelieferten M0-/PECD-Datensatz |
| Offshore-Landanschluss-Koordinate vs. Offshore-Wetterregion | tatsächlichen Erzeugungsstandort/Offshore-Region nutzen; nicht nur bus.x/y | OFFEN/bedingte Ausnahme |
| Hydro-Quelle: PEMMDB-Hydro-Inflows vs. PECD-Rohprodukt | Quelltyp, zeitliche Auflösung, hydrologische Topologie und Ziel-PyPSA-Klasse deklarieren | OFFEN: Quelldaten |
| Profile fehlen für vorhandenen Generator | FAIL + Audit; kein ungeprüftes fillna(0), Mittelwert oder anderes Jahr | FESTGELEGT |
| Stromerzeugung und Dispatch | Verfügbarkeit von tatsächlicher Einspeisung trennen | FESTGELEGT |
| Pflichtwetterdatensätze | Genau die fünf extern bestimmten IDs ohne Neuauswahl/-reduktion | FESTGELEGT |
| Änderungen an statischen Netzkomponenten | verbieten, Fingerprint-Vergleich | FESTGELEGT |

## 9. Konsolidierter Makroplan — keine Mikroschleifen

Nur **vier Makros** mit einem klaren Gate pro Makro. Keine selbständigen Mikroaufträge je Technologie oder Jahr.

### MA-1 — Architektur und Source-Contract Freeze (**dieses Dokument als Ausgangsbasis**)

**Einmalige Arbeit:** Verifizierte Open-TYNDP-/PyPSA-Eur-Wiederverwendung dokumentieren; M0- und PECD-/Hydro-Dateischemata auf Realbeispiele abgleichen; festes Technologie- und Mapping-Ledger inklusive fünf vorgegebener Szenariokennungen; freigegebene Fallback-/Fehlerpolitik. Kein produktiver Code.

**Exit:** M1-ARCH-CONTRACT-FROZEN (nur wenn reale Datenbeispiele, M0-Vertrag und Zielattribute bestätigt sind). Status aktuell: **PROPOSAL, noch nicht gefroren**.

### MA-2 — PECD-Reader und Profile-to-Asset Engine (**ein Implementierungsmakro**)

**Einmalige Arbeit:** vorhandenen Open-TYNDP-Reader nach Prüfung an Quellprodukt anpassen, kanonische Profil-IDs/Technologiecrosswalks erstellen, bestehende Generatoren über explizite oder georeferenzierte Zuordnung anbinden, alle fünf Datensätze als normierte CF-Arrays ausgeben. Umfassende Testfixtures/QA in derselben Lieferung.

**Exit:** M1-PECD-MAPPING-QUALIFIED; keine unzugeordneten Pflichteinheiten, keine Year-Fallbacks, nachgewiesene Referenzprofilwerte.

### MA-3 — Hydro + Non-mutating PyPSA Composer (**ein Integrationsmakro**)

**Einmalige Arbeit:** Hydro-Reader und Zeit-/Energieumrechnung an tatsächliche Quelle anpassen; Speichermodellkompatibilität prüfen; wetterabhängige CF-/Hydro-/ggf. weitere Zeitreihen an die **bestehenden** Generator-/StorageUnit-/Load-IDs binden; statische M0-Fingerprints unverändert; NetCDF-Export pro fixiertem Szenario; Tests in derselben Lieferung.

**Exit:** M1-DETAILED-NETWORK-WITH-TIMESERIES-CANDIDATE; reproduzierbarer PyPSA-Import/Export und technische Einheitenprüfungen.

### MA-4 — Unabhängige End-to-End-Qualifikation und M2-Handoff (**ein Akzeptanzmakro**)

**Einmalige Arbeit:** Gates M1-G0..G6 inklusive Quellaggregatvergleich, Energieerhaltung, alle fünf Szenarios, Originaltopologieinvarianz, unabhängiger QA-Bericht; optional G7 bei echten Betriebspunkten. Restfehler als konsolidierte Befundliste, nicht viele Einzelfix-Schleifen.

**Exit:** M1-REFERENCE-TIMESERIES-ACCEPTED-FOR-M2 oder M1-CONDITIONAL/BLOCKED mit abschließender Korrekturliste.

**Parallelisierungsregel:** Nach MA-1 können in MA-2/MA-3 **PECD-Reader** und **Hydro-Reader** parallel entwickelt werden, sofern derselbe eingefrorene Input-/Output-Vertrag gilt. Der Composer startet mit stabilen Schnittstellen; die vollständige Endabnahme MA-4 bleibt sequenziell. M0 und M2 haben getrennte Verantwortliche. Kein neuer Chat je Mikroaufgabe erforderlich.

## 10. M1/M0/M2-Handoff und Reproduzierbarkeit

- **An M0:** Benötigt statisches PyPSA-NetCDF, Original-ID-Ledger, Asset-/Bus-/Geokoordinaten und eindeutige hydroelektrische Komponentenklassifikation. M1 verlangt keine neuen CGMES-Feature-Wünsche, solange diese Informationen vorhanden sind.
- **An M2:** Liefert unverändertes hochaufgelöstes Netz mit allen stündlichen Zeitreihen, Profil- und Zuordnungstabellen, technischen Annahmen, Source Manifest und Gate-Bericht. Keine vorweggenommenen Zonen/Busmaps.
- **Im Repository:** Die Architektur ist bewusst ein eigenständiges Dokument unter docs/current/; das bestehende Aggregationspaket src/tyndp_reduce/ und die Bände I/II werden nicht verändert.
- **Versionierung:** Jeder externe Reuse-Anspruch muss auf einen konkreten externen Commit und eine konkrete Datei verweisen. Vor Implementierungsbeginn Open-TYNDP-Version, Ziel-PECD-Version und Datensatzlizenz nochmal verifizieren.

## 11. Entscheidungslage und nächster Freigabepunkt

**Bestätigt aus Quellcode:** Open-TYNDP besitzt PECD-/PEMMDB-Parser, Snakemake-Rules und Hydro-Aufbereitung; der vorhandene Pfad ist TYNDP-2024-knotenbezogen und bereits teilweise zonal. PyPSA-Core unterstützt die benötigten Zeitreihen.

**Architekturvorschlag:** Neuer profil-ID-basierter Layer und Topologie-erhaltender Composer, ohne Core-Patch und ohne Aggregationsmodul.

**Noch nicht bestätigt:** Die tatsächlichen Inputdateien (PECD-/Hydro-Versionen, exakte Profile-/Regionencodes), M0-Artefaktschema und die räumlichen Zuordnungen in den konkreten Projektdateien. Daher **keine Aussage über vollständige Ausführbarkeit mit den fünf vorgegebenen Datensätzen** und keine Freigabe von MA-2 ohne MA-1-Datencontract-Gate.

Das nächste sinnvolle Arbeitspaket ist **ein konsolidiertes MA-1-Contract Freeze anhand von wenigen repräsentativen realen Eingabedateien**. Danach können die Implementierungsmakros ohne weitere Architektur-Grundsatzschleifen beginnen.
