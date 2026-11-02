# IoSN Modul 1 — Unabhängige PECD-Import- und Anlagen-Zeitreihenarchitektur

**Datum:** 2026-11-02  
**Autorität:** INDEPENDENT_UPSTREAM_AND_PRIMARY_SOURCE_RESEARCH / RECOMMENDATION_FOR_OWNER_DECISION  
**Status:** ARCHITECTURE_RESEARCH_ONLY; keine PECD-Originalbytes verarbeitet, keine produktiven PyPSA-Komponenten verändert, keine reale Netz-/Zeitreihen-Integration qualifiziert.  
**Ausgang:** neue, eigenständige Prüfung der Upstream-Fähigkeiten; ältere IoSN-M1-Produkte **nicht** als Architektur-/Implementierungsvoraussetzung verwendet. Dokument separat auf einem Branch vom unabhängigen Projekt-\`main\`-Commit \`1595d6d38e77804760612621657721b3699d2fea\`.

## 1. Exakte Auftragsgrenze

**Alleiniger Gegenstand ist Modul 1**: Native PECD-v4.2-Daten beschaffen/einlesen und daraus zeitabhängige Verfügbarkeiten beziehungsweise definierte PECD-Energiezeitreihen an den Komponenten eines **bereits vorhandenen** hochaufgelösten \`pypsa.Network\` bereitstellen. Netzformat-/CGMES-Import, Netzerzeugung, Kraftwerks-Neuanlage, Netztopologie, Clustering/Netzreduktion, Optimierung und Solverentwicklung sind **ausgeschlossen**. Nachfrage-/DFT-Prognose ist ebenfalls außerhalb des PECD-Energy-Import-Basisscopes; PECD-Temperatur allein erzeugt keine verbindliche Stromlast.

Der Netzinput ist ein **beliebiges qualifiziertes PyPSA-Netz** mit bereits vorhandenen Generator-/Speicher-IDs, \`bus\`, \`carrier\`, \`p_nom\` und (wo vorhanden) geografischen/technischen Metadaten. Die für Profilmatching notwendigen **physikalischen Anlagenstandorte** dürfen über ein **separates** Inputregister in M1 bereitgestellt werden; diese Standortzuordnung ist nicht dem Netzimport anzulasten. M1 ändert keine statischen Komponenten und enthält keine Arbeit an M0/M2.

Die bereits extern festgelegten fünf Wetterdatensätze bleiben unverändert und werden als **Inputidentitäten** behandelt; keine neue Auswahl/Reduktion oder Gleichsetzung mit den drei TYNDP-2026-Standard-WS je Planungshorizont.

## 2. Verifizierter Upstream-Stand

| Komponente | Ist-Fähigkeit | Nicht als Lösung voraussetzen | Source |
|---|---|---|---|
| **PyPSA-Core** | \`Network.generators\`, \`generators_t.p_max_pu\`, \`storage_units_t.inflow\`, \`set_snapshots\`, NetCDF, Asset-IDs, Geohilfen | kein dedizierter PECD-Importer oder generischer \`PECD grid/region → existing_generator_id\`-Dienst nachgewiesen | [Core @ 23650353](https://github.com/PyPSA/PyPSA/tree/23650353eb1d059acfec28f4915ad3e068c085bf), [Time-Series Design](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/docs/user-guide/design.md), [I/O](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/io.py) |
| **PyPSA-Eur** | ERA5/SARAH→Atlite-CF→Region-Bin-Profile, \`build_powerplants.py\` GeoPandas-Plant→Netzregion via \`sjoin\`, nearest bis 10 km, \`add_electricity\` für RES/Last/Hydro, Snakemake | Plant→Cluster-Bus ist **nicht** Profile→**Original-Generator**; standardmäßiger \`compose_network\` beginnt bei \`networks/clustered.nc\` und **erzeugt** neue Generatoren/Loads | [pypsa-eur @ 1526bb82](https://github.com/PyPSA/pypsa-eur/tree/1526bb820e25a9faa61f32b00bfc77dd05db6b2e), [build_renewable_profiles.py](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_renewable_profiles.py), [build_powerplants.py](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/scripts/build_powerplants.py), [compose.smk](https://github.com/PyPSA/pypsa-eur/blob/1526bb820e25a9faa61f32b00bfc77dd05db6b2e/rules/compose.smk) |
| **Atlite** | Geometrische Raster-/Polygon-Indikatormatrix und geeignete Flächenmatrix, Cutouts und Ressourcen-Leistungsmodell | \`availabilitymatrix\` = **flächenbezogene Landnutzungs-Eignung**, NICHT die stündliche \`p_max_pu\`-Zeitreihe; für native bereits berechnete PECD-CF ist keine neue Atlite-Konversion erforderlich | [Atlite @ 0d4ff8](https://github.com/PyPSA/atlite/tree/0d4ff8f703a99566b475b8d775aa2e74309123ee), [Cutout / GIS](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py) |
| **Open-TYNDP tyndp-2026** | PECD-v4.2-CSV-/TYNDP-Prebuilt-Reader, Wetterspalten \`WS###\`, \`clean_tyndp_pecd_data.py\`→\`build_renewable_profiles_pecd.py\`→regional \`profile(time,bus,bin=0,year)\`; Hydro/TYNDP-Reader | Reader verwendet \`buses_tyndp\`/TYNDP-Knoten, nicht beliebige Originalgeneratoren; griddiertes ORIG-PV-NetCDF wird im untersuchten regionalen Reader nicht verarbeitet; Standard-\`fill_gaps_method: zero\`/Horizon-Fallback für die hier erforderliche Quellentreue unzulässig | [tyndp-2026 @ 71a3a9](https://github.com/open-energy-transition/open-tyndp/tree/71a3a9a15b77114cd79458bceabc98e1a64dd58a), [PECD reader](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py), [profiles](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_renewable_profiles_pecd.py) |
| **Copernicus CDS** | Offizielle PECD4.2 als CSV (regionale Energieindikatoren) und NetCDF-4 (griddierte Produkte); \`cdsapi\` für freigegebene Downloads, "Weights and masks" für offizielle 3D-Regionmasken | Originaldateien, tatsächliche Dimensionen/Calendar/Header, fünf Projekt-IDs und Verfügbarkeit des ausgewählten Produkts müssen mit **realen Dateibytes** bestätigt werden | [CDS-Datensatz](https://cds.climate.copernicus.eu/datasets/sis-energy-pecd?tab=overview), [API](https://cds.climate.copernicus.eu/en/how-to-api), [PECD4.2 PUG](https://confluence.ecmwf.int/spaces/CKB/pages/540941752/Climate+and+energy+related+variables+from+the+Pan-European+Climate+Database+derived+from+reanalysis+and+climate+projections+v4.2+Product+user+guide+PUG) |

### 2.1 PECD native räumliche Energieauflösung ist technologiespezifisch

**Primärdokument:** ECMWF [PECD4.2 PUG, Tabelle 2.12/3.6 und 4.2/4.3](https://confluence.ecmwf.int/spaces/CKB/pages/540941752/Climate+and+energy+related+variables+from+the+Pan-European+Climate+Database+derived+from+reanalysis+and+climate+projections+v4.2+Product+user+guide+PUG), zuletzt aktualisiert 2026-08-05.

| Energievariable | Tatsächlich geliefertes Ergebnis | Einheit | Konsequenz |
|---|---|---|---|
| Wind onshore WON | stündliche **regionale** \`PEON/P2ON\` CF, unterschiedliche Existing/Future SP-HH- und \`ReGrA/ReGrB\`-Typologien | MW/MW | Anlagen→offizielle Wind-Profilregion plus technologische Variante; nicht unzulässig einen nativen 0,25°-WON-CF behaupten |
| Wind offshore WOF | stündliche **regionale** \`PEOF/P2OF\` CF, Existing/Future-Varianten | MW/MW | Offshore-Parkstandort/Quellregion; Landfall-Anschlussbus ist nicht der Parkstandort |
| Solar photovoltaics SPV | stündliches **\`ORIG\`-Raster 0,25°×0,25°** **und** \`NUT0/NUT2/SZON/PEON/P2ON\`-Region-CF, vier technische PV-Typologien | MW/MWp | genuine native Rasterzelle vorzeitigem Regionsmittel vorziehen, falls das ORIG-Produkt im tatsächlich gelieferten Input vorhanden ist; PV DC/AC normieren |
| Hydro HRI/HRR/HPI/HOL | **regionale \`SZON\`-Wochenergiemengen** | MWh | eigenständiger energie-/hydrologisch belegter Flächen-/Basin→bestehendes Hydroasset-Port, nicht analog zum Wind-CF-Point-Join |
| Wettervariablen (WS10/WS100/GHI/TA/TP) | griddiert \`0.25°\`, ggf. regional | Quellgröße | getrenntes **optionales** meteorologisches Leistungsmodell, **nicht** die native WON/WOF-Energie-CF |

**Wichtige Präzisierung:** Die globale PECD-Klimabasis hat 0,25°-Grid, **nicht alle abgeleiteten Energietime-Series**. Vorhandene native Energie-CF werden **nicht** aus Wetterdaten neu simuliert. Wer unbedingt **standortbezogene griddierte Wind-CF** braucht, muss ein eigenes qualifiziertes Wind-Conversionsmodell aus griddierten Windgeschwindigkeiten/Alphas/Power-Curves ableiten (separate, bewusst genehmigte Modellklasse).

**PECD Versions-/Zeitevidenz:** Original-Szenario, GCM, SSP, Technologievarianten, \`file_version\` inklusive ggf. reprocessed \`fv2\`, Start-/Endzeit und Timelabel aus der *tatsächlichen Datei* kontrollieren; PUG beschreibt bekannte korrigierte Wind-/Klima-Datenfehler, deshalb \`PECD4.2\` allein nicht hinreichender Versionsschlüssel.

## 3. Minimalarchitektur von Grund auf

\`\`\`text
          PECD 4.2 OFFIZIELLE DATEN
    CDS-CSV (PEON/PEOF/P2ON/P2OF)    CDS-ORIG SPV-NetCDF + native Masken
               │                               │
               └─────[1. PECD native IO + canonical metadata]────┘
                                     │
                Canonical source records:
                (weather_id, source/version, product, tech,
                 region/cell, UTC time, source units, source hash)
                                     │
         NETWORK INPUT               │          PLANT LOCATION INPUT
       vorhandenes                   │       unabhängiges Anlagenregister,
       PyPSA.Network                 │       falls Netz nur Buspositionen hat
              │                      │                   │
              └──────────────────────┼───────────────────┘
                                     ▼
                    [2. Asset→source spatial join]
                  point→PECD-zone / point→PV grid
                  technology and capacity-basis gate
                  emits original_generator_id→profile_id
                                     │
                                     ▼
                   [3. Apply/Export using PyPSA Core]
                 only existing generators_t.p_max_pu
            optional Hydro → existing storage_units_t.inflow
                     no n.add, no static mutations
                                     │
                                     ▼
              time × existing_component_id time series
                   + optional attached copy of network
                   + concise data/source/mapping QA
\`\`\`

### Minimaler Programmumfang

**Zwingend neue projektspezifische Funktion 1: \`pecd_native_io\`**

- Exakte CDS-Quellselektion: Version, GCM/SSP bzw. historisch, Energievariable, Technologie, Zielregionen, Zeitschritte und fünf **vordefinierte** Weather-IDs, ohne automatische Wahl.
- Regionale PECD-CSV je \`profile_id/region_id, time\` lesen; alle tatsächlichen Source-Spalten/Metadata-Header/Zeitzonen validieren. Open-TYNDP-Parser als wiederverwendbares Muster, TYNDP-Knotenbinding **entfernen**.
- \`SPV ORIG\`-NetCDF gezielt mit \`xarray.open_dataset\` lesen; native Latitude/Longitude, CF-Dimensionen, Technik-/Szenariometadaten/Calendar erst anhand realer Samples spezifizieren. **Lazy selection nur der tatsächlich benötigten Standorte/Zellen**, nicht das gesamte Europa-Raster für alle fünf Jahre eager materialisieren.
- Offizielle \`mask(region,latitude,longitude)\`-NetCDF für PEON/PEOF/P2ON/P2OF je tatsächlicher Source-Version einlesen. Maskenanteile sind **Flächenüberdeckung**, nicht Anlagenkapazitätsanteile. Offizielle Vektor-Shapefiles sind teils nicht öffentlich; keine frei erfundene GeoJSON-Autorität.
- Einheitlicher kleiner Sourcekatalog und \`xarray/pandas\`-Profile, QA Source-Hash/Revision/Calendar/Missing/Coverage.

**Zwingend neue projektspezifische Funktion 2: \`pecd_asset_mapper\`**

- Input: nur **bestehende** \`n.generators\`-IDs, \`carrier\`, \`bus\`, \`p_nom\` und **qualifizierte** Generator-/Park-Koordinaten oder explizit freigegebene externe Region-ID. \`n.buses.x/y\` kann ein Proxy sein, **nicht** automatisch Standortbeweis; Ersatz durch \`plant_location_catalog\` zulässig.
- Wind: \`Generator location/region → PEON/P2ON/PEOF/P2OF → technology/grade → native regional source_profile_id\`. Viele verschiedene elektrische Originalgeneratoren dürfen denselben **regionalen** Wind-CF verwenden. Keine räumliche Interpolation von Wind-CF.
- PV: \`Generator location → native ORIG grid cell\` mit Latitude-/Longitude-Richtung, Zellgrenzen, Technologieklasse, Units \`MW/MWp\` und AC-\`p_nom\`; falls Produkt nur regional vorhanden ist, explizite regionale Zuordnung statt vorgetäuschter Gridauflösung.
- Grenzzellen: Offizielle \`mask\` enthält **fraktionale Zellfläche**, kann bei angrenzenden Regionen **keine exakte Punktposition** innerhalb der Zelle entscheiden. Bei mehrdeutiger Maske zusätzliche offizielle Standort-/Gebietsinformation oder dokumentierte externe Zuordnung; für Real-PASS keine stille Mehrheits-/Nearest-Heuristik.
- Park-/Sammelgeneratoren: Nur wenn es ein bereits bestehender zusammengesetzter Generator ist und tatsächliche einzelne Teilkapazitäten/Standorte vorliegen, mehrere Sourceprofile mit nachgewiesenen MW-/MWp-Anteilen gewichten; andernfalls kein arbiträrer Gewichtungsmix.
- Ausgabe \`generator_id, source_profile_id, weather_scope, carrier_variant, mapping_evidence, confidence/quality\` inklusive \`unmatched\`. Keine neue Bus-/Generatoranlage.

**Keine neue Modellierungsengine – kleine Apply-Funktion:** Prüft \`time × generator_id\`/Snapshots, Quell-/Target-Coverage, \`0≤CF≤1\`, technologieabhängige DC/AC-Semantik, vorhandene Dynamic-Werte/Overwrite-Policy. Schreibt mit PyPSA-Pandas-API ausschließlich \`n.generators_t.p_max_pu\` **an unveränderte bestehende IDs**, optional als getrenntes Zeitreihenfile statt neuer Netzdatei. Kein Upstream-PyPSA- oder PyPSA-Eur-Code ändern und **kein voller PyPSA-Eur-\`compose_network\`**.

**Optionale Spezialschicht \`pecd_hydro\`:** Nur wenn Hydro-M1-Pflichtscope. \`SZON, WEEK, MWh\` benötigt **separate** Sourceintervall-, Hydrologiebereich→Asset-/Speicherport- und Energiebilanzlogik. Nicht in allgemeinen Wind/PV-Spatial Join pressen. Nicht neue Hydro-Komponenten erzeugen. Ein vorhandener fachlich gültiger Hydro-Adapter kann dafür wiederverwendet werden, wird aber nicht zum Architekturfundament des Wind/PV-Matchings.

## 4. Größte technischen und wissenschaftlichen Risiken

| Rang | Herausforderung | Warum problematisch | Minimal erforderliche Gegenmaßnahme |
|---|---|---|---|
| **1** | **Reale Anlagenstandorte fehlen/Bus-Koordinaten sind nicht Anlagenkoordinaten** | Netzknoten liegt elektrisch korrekt, aber meteorologisch oft nicht am Kraftwerksstandort; Offshore-Landfall, Sammelanschluss, synthetische Busse | unabhängiges Anlagen-/Park-Georegister oder autoritative PECD-Region-ID; Bus nur mit dokumentierter Standortvertretbarkeit |
| **2** | **Offizielle Energieindikatoren sind unterschiedlich räumlich aufgelöst** | 0,25° Wind-Wetter ist **nicht** 0,25° Wind-CF; erzwungene Griddierung erzeugt Scheingenauigkeit | direkt native WON/WOF Region-CF; SPV-ORIG-CF wenn vorhanden; alternativ eigener Wind-Power-Model-Scope nur nach gesondertem Entscheid |
| **3** | **Offizielle Regionsmasken/Label und Grenzzellen** | PECD-Masken fraktional, Shapefiles teilweise nicht verfügbar; region IDs TYNDP-Bus≠CGMES-Bus | Native NetCDF-Masken, Source-Region-Registry, grenz-/offshore-spezifische Qualitätssicherung, keine unmarkierte Nearest-Heuristik |
| **4** | **PV MW/MWp vs. vorhandenes \`p_nom\` MW_AC** | \`p_max_pu\` muss in der AC-Basis normiert sein; implizite DC/AC-Konversion oder Clipping kann falsche verfügbare Leistung liefern | belegte PV DC-Peak-/AC-Nennleistung, Wechselrichter-/Loss-/Clip-Semantik oder Quelle mit explizit gleicher AC-Basis; sonst BLOCK |
| **5** | **Technologie- und Klimaszenarioauswahl** | Wind Existing/Future, SP-HH, ReGrA/B, PV rooftop/fixed/tracking, GCM/SSP, PECD-file version; Verwechslung von Planungsjahr und Weatherjahr | kleine explizite Technologie-/Weather-/Source-Selektor-Tabelle, kein Fallback auf andere Jahre/Spalten |
| **6** | **Zeitachse und Granularität** | UTC/DST, Monats-/Stundenindex, Leaptage, mögliche Intervall-Ende-Konvention, Hydro WEEK MWh vs. Hour MW | originaler NetCDF-/CSV-Time-Metadata-Witness, explizite Snapshots, keine stille Füllung; Hydro gesondert bilanzieren |
| **7** | **Datenvolumen/RAM** | volljähriges pan-europäisches \`time × lat × lon\` plus fünf Fälle sehr groß | \`xarray\` lazy/chunked, benötigte Geo-Zellen zuerst auswählen, Parquet/NetCDF-Streaming, gerätebezogene Ausgabe |
| **8** | **Unbeabsichtigte Netz-/Zeitreihenänderung** | voller PyPSA-Eur-Composer legt Komponenten an, PyPSA-\`set_snapshots\`/Import kann fehlende Zeitwerte mit Default auffüllen | nur bestehende Generator-IDs/Attribute schreiben; vorher Vollständigkeits- und Overwrite-Prüfung; statische Tabellen vor/nach unverändert |
| **9** | **Echte Quelldateien nicht qualifiziert** | PUG/CSV-Schema theoretisch; reale ORIG-Var/Dims/CRS, Windprovenienz, PECD \`fv2\` und tatsächliche fünf Fall-IDs unbekannt | für jeden Produkttyp **eine echte Datei** plus offizielle Maske prüfen, bevor ein starrer generischer Reader implementiert wird |

## 5. Minimaler Workflow und Datenvertrag

### Eingänge

1. **PECD source_manifest** pro Produkt: \`source_id, version/file_version, climate_model, SSP, weather_id, time_extent, product=WON|WOF|SPV|HRI|HRR|HPI|HOL, spatial_level, technology_variant, native_unit, path/sha256, license\`. Keine Weltmetadaten aus einem TYNDP-Busnamen inferieren.
2. **Network target table** als schmale, read-only \`Generator(ID,bus,carrier,p_nom)\`-Sicht des existierenden PyPSA-Netzes; optional unabhängiges Anlagenstandortregister mit Koordinaten/CRS und \`location_evidence\`.
3. **Offizielle Regionmasken** oder autoritativ identische PECD-Zonencodes; bei NetCDF Grid die Originalgrid-Zellkoordinaten und Extents.

### Zwischenprodukt

\`asset_profile_map\` schmal und jederzeit neu aus Inputs reproduzierbar: \`generator_id, source_id, spatial_id, technology_variant, mapping_rule, evidence_ref, weight\` (bei Single-Region \`weight=1\`).

Für vorhandenen Generator \`g\`, unterstellten Quelldatenstand \`s\`, Zeit \`t\` und freigegebene Teilprofile \`r\`:

\`CF[g,s,t] = Σ_r w[g,r] CF_PECD[r,s,t]\`, \`Σ_r w[g,r]=1\` wenn Composite mit belegter technischer Kapazität. Sonst direktes Single-Profile-Mapping. Das elektrische \`p_nom\` und \`bus\` bleiben **unverändert**.

### Ausgabe

**Primär:** \`generator_cf(time,existing_generator_id)\` je externer Weather-ID; optionale \`hydro_inflow(time,existing_storage_id)\` nach Hydro-Physik. **Sekundär:** an eine Kopie des unveränderten PyPSA-Netzes angelegte dynamische Attribute und NetCDF-Roundtrip. QA nur als kleiner Source-/Mapping-/Coverage-/Static-Fingerprint-Begleitbericht.

**Wichtig:** \`p_max_pu\` ist ein **Verfügbarkeitslimit**, kein tatsächlicher Dispatch und kein automatisch bilanziertes AC-PF-Betriebsszenario.

### Einzige notwendige Snakemake-Erweiterung (konzeptionell)

\`\`\`
existing_network.nc ---------------+
                                   |
PECD source files -> pecd_read ----+-> pecd_map -> apply_to_existing_ids -> generator_cf / optional annotated-network
official masks -----> /            |
asset locations -------------------+
\`\`\`

Option \`source_format=PECD_CSV_REGIONAL|PECD_NETCDF_ORIG\`, **kein** fiktiver Upstream-Schalter. Keine \`build_cutout\`-Regel, sofern das PECD-Produkt bereits Energie-Kapazitätsfaktoren enthält. GeoPandas/Atlite nur als GIS-Bibliotheken einsetzen, wo nötig. Hydro, falls Pflicht, mit separatem Vorverarbeitungspfad an derselben Apply-Grenze.

## 6. Minimaler Arbeits- und Qualifikationsplan (keine Makroflut)

**A – PHYSICAL SOURCE SAMPLE FIRST:** Exakte fünf bereits festgelegte User-Weather-IDs und Zugangswege beibehalten; **nur** je Produktfamilie einen repräsentativen echten Datensatz und offizielle Maske byte-/header-/CRS-/Dim-/Time-/Unit-spezifisch prüfen: WON regional CSV, WOF regional CSV, SPV ORIG NetCDF falls gewünscht; Hydro original-weekly nur falls obligatorisch. Getrennt davon vorhandenes PyPSA-Netz-/Generator-/Anlagenstandort-Sample (kann synthetisch zum ersten Softwaretest sein). Ergebnis: realer minimaler Schema-Contract. M0-/Netzimport nicht beauftragen.

**B – EIN SMALL IMPLEMENTATION + REGRESSION:** 1–2 kleine Reader/Mapper-Funktionsmodule + dünner Writer auf dem vorhandenen PyPSA-Objekt; Geo/Technology/Time/Units-Negativtests, mehrere Generatoren je Windregion, PV-Pixel, Cross-border, Offshore-Landfall, Park ohne Standort, PV DC/AC, Missing-Year, statische Netz-Invarianz. **Kein** neuer Generator-, Clustering-, Optimierungs- oder Gesamt-Composer-Framework.

**C – REAL SOURCE QUALIFICATION:** Erst bei tatsächlichen Quellbytes und qualifiziertem Netz/Standortregister: vollständige fünf gewählte Wetterfälle, alle erforderlichen Generatoren, echte Geo/Tech/MW-Basen, Stundenindex, NetCDF-Export (falls benötigt) und unabhängiger begrenzter Review. Reale Zulassung strikt von synthetischem Test-PASS trennen.

## 7. Klare Architekturentscheidung

**M1 = PECD source reader + profile-to-existing-generator mapper + thin PyPSA time-series attachment.** Die ersten beiden sind die eigentliche PECD-Spezialisierung; die dritte ist vorhandene PyPSA-Core-Funktionalität mit einer kleinen konfliktfreien Zuweisungsroutine. Keine neue PyPSA-Core-Erweiterung, kein eigener Solver, keine volle PyPSA-Eur-Pipeline, kein TYNDP-Knotenmodell und keine Netzproduktion.

**Bewusst offen bis echte Dateien vorliegen:** Welcher PECD-Wind-Regionmaskenstand vorliegt, welches PV-Produkt tatsächlich geliefert wird, ob Originalanlage-Geo verfügbar ist, welche Technologie-/DC-/AC-Parameter gelten und wie fünf fixierte Klimafälle in die echten CDS-/TYNDP-Metadaten kodiert sind. Diese Faktoren bestimmen die benötigte konkrete Reader-/Spatial-Mapping-Implementation, nicht weitere abstrakte Architekturmakros.
