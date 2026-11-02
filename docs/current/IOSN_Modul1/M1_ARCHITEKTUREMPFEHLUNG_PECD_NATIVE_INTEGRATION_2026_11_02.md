# IoSN Modul 1 — Architektur-Empfehlung zur Integration hochaufgelöster PECD-v4.2-Zeitreihen in PyPSA

**Datum:** 2. November 2026  
**Dokumenttyp:** unabhängige, quellengestützte Softwarearchitektur-Empfehlung  
**Status:** `RECOMMENDATION / SOURCE-CODE-REVIEW` – keine Implementierungs- oder Real-Data-Freigabe  
**Verantwortungsbereich:** ausschließlich **Modul 1: PECD-Import, Zuordnung der Profile zu vorhandenen Netzkomponenten und Bereitstellung der Zeitreihen**  
**Repository:** [AlOussama/TYNDP_Products](https://github.com/AlOussama/TYNDP_Products)

> **Architekturentscheidung:** Bestehende PyPSA-Core-, PyPSA-Eur-, GeoPandas-/Atlite- und Open-TYNDP-Funktionalität wiederverwenden. Für IoSN-M1 werden **kein neues Netzmodell, keine neue Wettermodellierung, kein neuer allgemeiner räumlicher Matchingalgorithmus und keine parallele PyPSA-Eur-Pipeline** benötigt. Es verbleiben eine schmale **PECD-Quellnormalisierung**, ein **quellenagnostischer Geometrie-/Technologie-Crosswalk** auf bestehende Generator-IDs und eine sehr kleine **Zeitreihenanbindung** an PyPSA. Der native PECD-ORIG-NetCDF-Eingang ist nur für tatsächlich verwendete griddierte Produkte zu ergänzen.

---

## 1. Geltungsbereich und überprüfbare Annahmen

### 1.1 Eingang und Ziel

Die Anwendung erhält **zwei unabhängige Eingangsströme**:

1. **Vorhandenes hochaufgelöstes Netz:** ein bereits konstruiertes `pypsa.Network` mit sämtlichen elektrischen Knoten, Generatoren, Lasten, Speichern, Anschlussbeziehungen, `carrier` und `p_nom`. Wo notwendig, ist ein eigenständiges, qualifiziertes **Anlagenstandortregister** mit Koordinaten und Herkunft beizustellen. Ein Generator kann an einem elektrischen Bus angeschlossen sein, dessen Koordinaten **nicht** dem tatsächlichen Erzeugungsstandort entsprechen.
2. **PECD v4.2:** räumlich definierte stündliche Erzeugungsverfügbarkeiten und – bei entsprechender Umfangsentscheidung – hydrologische Energie-/Zuflussdaten. PECD-Regionen und Rasterzellen kennen **keine** elektrischen PyPSA-Bus- oder Generator-IDs.

Die Anwendung erzeugt **Zeitreihen mit den IDs der bereits vorhandenen Komponenten**. Sie verändert weder `n.generators.bus` noch `n.generators.p_nom` oder andere statische elektrische Eigenschaften. Allein eine Kopie des bereits vorhandenen Netzobjekts darf ausgewählte dynamische Attribute erhalten.

**Nicht Bestandteil von M1:** CGMES-/anderer Netzformatimport, Netzerzeugung, Bus-/Leitungserzeugung, Netztopologieänderungen, Netzreduktion/Clustering, Leistungsfluss-/OPF-Algorithmen, neue Wetterjahresauswahl und die Entwicklung eines meteorologischen Wind-/PV-Leistungsmodells. Die Lastprognose/DFT ist eine **eigene externe Datenquelle** und nicht automatisch Teil des PECD-Wind-/PV-Imports.

Die im Projekt bereits **fünf ausgewählten Wetterdatensätze** sind reine Konfigurations-/Quellenidentitäten. Ihre konkreten IDs und die zugehörigen Originaldateien wurden in der hier geprüften Quellenlage **nicht physisch verifiziert**. Diese fünf sind nicht ohne Nachweis identisch mit den drei regulären Open-TYNDP-2026-`WS###` je Planungshorizont; sie werden nicht neu gewählt.

### 1.2 Was hier überprüft wurde

Die Bewertung stützt sich auf die **tatsächlichen Quellcodedateien** von PyPSA, PyPSA-Eur, Atlite und Open-TYNDP sowie die **offiziellen PECD-v4.2-Produktdefinitionen**. Sie leitet Architekturentscheidungen aus diesen Belegen ab. Ein generischer API-Name, den die Upstream-Pakete **nicht** besitzen, wird nicht als bestehende Funktion dargestellt. Exakte Commit-Stände und die Links zu den maßgeblichen Stellen stehen in Abschnitt 12.

---

## 2. Kurzbefund: Was bereits vorhanden ist

| Aufgabe | Vorhandene Funktion / nachgeprüfter Quellcode | Ergebnis für M1 |
|---|---|---|
| Dynamische Generator-Zeitreihen | PyPSA-Core `n.generators_t.p_max_pu`; zeitabhängige Komponentenattribute, `set_snapshots`, NetCDF [Q01], [Q02], [Q03] | **Unverändert verwenden.** Kein Core-Fork. |
| Vorhandene Generatoren und Anschlussknoten | `n.generators.index`, `n.generators.bus`, `n.generators.carrier`, `n.generators.p_nom`, `n.buses.x/y` [Q01] | Read-only Input für M1; nicht neue Generatoren erzeugen. |
| Räumliches Punkt→Polygon-Matching | GeoPandas `GeoDataFrame.sjoin` und Prädikate `within`, `covers` etc. [Q04] | **Bestehenden GIS-Algorithmus benutzen.** |
| Beispiel für räumliches Kraftwerksmatching in einem PyPSA-Workflow | PyPSA-Eur `map_to_country_bus()` in `scripts/build_powerplants.py`: Plant-Standort→Netzregion, per Country und ggf. nearest-neighbor [Q05] | **Verfahren übernehmen**, aber Ziel ist bei uns **PECD-Profilregion**, nicht ein neuer Netzbus. Unqualifizierten Nearest-Fallback nicht übernehmen. |
| Raster-/Polygon-Überlappungsmatrix | Atlite `Cutout.indicatormatrix`, `atlite.gis.compute_indicatormatrix` [Q06] | Verwenden, **sofern** Raster-/Polygonverarbeitung erforderlich; keine zweite GIS-Engine. |
| ERA5/SARAH→Kapazitätsfaktoren / Regionsprofile | PyPSA-Eur `build_renewable_profiles.py`, `determine_availability_matrix` [Q07], [Q08] | Für **fertig gelieferte PECD-CF** weder Wind-/PV-Leistungsmodell noch Landnutzungs-Potenzialanalyse wiederholen. |
| PECD-Regional-CSV und Wetterspalten | Open-TYNDP `prepare_tyndp_pecd_release.py`, `clean_tyndp_pecd_data.py` [Q09], [Q10] | **Vorhandenen Reader wiederverwenden/adaptieren**, seine TYNDP-Knotenbindung aus dem neutralen Importpfad heraushalten. |
| PECD-Regionalprofil→PyPSA-Eur-Profil-Datei | Open-TYNDP `build_renewable_profiles_pecd.py`, `profile(time,bus,bin=0,year)` [Q11] | Als bestehende Ausgabe-/Formatkonvention nutzbar; `bus` dort bezeichnet TYNDP-Node, **nicht** automatisch unsere Generator-ID. |
| Native PECD-SPV-ORIG-NetCDF | PECD-Datensatz liefert griddierte SPV-CF, xarray kann NetCDF lesen [Q12], [Q13] | **Kleine PECD-spezifische Variable-/Koordinatenauswahl** ergänzen, *falls* native ORIG-SPV-Profile genutzt werden. |
| PECD-Regionsmasken | Offizielle float-NetCDF-Masken `mask(region,latitude,longitude)` für `PEON/PEOF/P2ON/P2OF/SZON` [Q14] | Eingabemasken verwenden; **Flächenanteile nicht als Anlagen-MW-Gewichte interpretieren.** |
| Daten an ein Netz anfügen | PyPSA-Zeitreihen/DataFrame-API [Q01–Q03] | Dünner `attach_existing_profiles`-Schritt mit Index- und Überschreibprüfung, **keine zusätzliche Modellierungsengine**. |

**Kritische begriffliche Trennung:** Die in PyPSA-Core verfügbare **elektrische Clusterung** ist nicht der geografische Wetter-Profil-Join. Der generische geografische Join wird von **GeoPandas/Atlite** implementiert und in **PyPSA-Eur** fachlich verwendet. Unser M1 muss ihn nur auf einen **anderen Ziel-Namensraum** (PECD-Profile statt Netzbusse) anwenden. [Q04–Q07]

---

## 3. PECD-v4.2-Produkte: Welche „hohe Auflösung“ ist wirklich verfügbar?

Aus den offiziellen Tabellen **2.12** (historisch) und **3.6** (Projektionen) des PECD-v4.2-Product-User-Guides folgt eine zwingende Unterscheidung zwischen **meteorologischer Rasterauflösung** und **Auflösung der fertig berechneten Energieindikatoren**. **Nur SPV wird bei den hier relevanten Energieindikatoren sowohl als griddiertes ORIG-Produkt als auch regional aggregiert geliefert.** [Q12], [Q14], [Q15]

| PECD-Energieindikator | Native Energieprofil-Auflösung | Zeit / Einheit | Relevanz für bereits existierende Originalgeneratoren |
|---|---|---|---|
| Wind Onshore (`WON`) | **`PEON`, `P2ON`** (regionale Kapazitätsfaktoren) | stündlich, **MW/MW** | Generator/Standort bzw. belegte PECD-Region → regionales Windprofil. Mehrere elektrische Knoten dürfen denselben CF nutzen. |
| Wind Offshore (`WOF`) | **`PEOF`, `P2OF`** (regionale Kapazitätsfaktoren) | stündlich, **MW/MW** | Windpark-/Offshore-Region verwenden; landseitiger Anschlussbus ist kein Windparkstandort. |
| Solar PV (`SPV`) | **`ORIG` 0,25°×0,25°-Raster** als NetCDF; außerdem `NUT0`, `NUT2`, `SZON`, `PEON`, `P2ON` regional als CSV | stündlich, **MW/MWp** | Standort→ORIG-Rasterzelle, falls genau dieses Produkt vorliegt, sonst qualifizierte regionale Zuordnung. PV-Technologietyp und DC/AC-Basis beachten. |
| Hydro (`HRI`, `HRR`, `HPI`, `HOL`) | **`SZON`** regionale Energie-/Zuflussindikatoren | **wöchentlich, MWh** | Eigenständiger hydrologischer Allokations- und Einheitenvertrag; **kein** gewöhnlicher Wind-/PV-Point-Join. |
| Meteorologische Daten (`WS10`, `WS100`, `GHI`, Temperatur usw.) | teilweise **0,25°-Raster** | je Variable stündlich oder täglich | Keine bereits vorgefertigten `WON/WOF`-Kapazitätsfaktoren. Ableitung eigener Wind-CF würde ein **zusätzliches Leistungsmodell** erfordern. |

**Nicht zulässige Schlussfolgerung:** „PECD liefert Wetterdaten mit 0,25°“ bedeutet **nicht**, dass das veröffentlichte `WON`-/`WOF`-CF-Produkt in 0,25° verfügbar wäre. Diese CF sind nach den offiziellen Produkttabellen regional. Für ihre Verknüpfung mit dem elektrischen Netz reicht daher eine Regionszuordnung; meteorologische Interpolation oder eigenes Windmodell sind nicht Teil des minimalen Scopes. [Q12]

### 3.1 Offizielle Regionenmasken

Die von ECMWF veröffentlichten Regionsmasken haben die Form `mask(region, latitude, longitude)` und enthalten in Grenzzellen **Flächenüberdeckungsanteile zwischen 0 und 1**. Die zugrunde liegenden ENTSO-E-Shapefiles sind nach PUG für zahlreiche Regionen **nicht öffentlich**, die NetCDF-Masken dagegen im CDS unter „Weights and masks“ abrufbar. [Q14], [Q15]

**Daraus folgt eine wichtige technische Grenze:** Die Maske sagt, welcher **Anteil einer Rasterzelle** zu einer Region gehört – nicht, in welchem Teil dieser Zelle ein beliebiger Anlagenpunkt liegt. Ein Punkt in einer Grenzzelle kann daher anhand der Maske allein **mehrdeutig** sein.

Bevorzugte Reihenfolge der Regionsermittlung:

1. **Autoritative PECD-Region-ID pro Anlage vorhanden:** direkt nutzen, gegen Quellregionenkatalog prüfen; kein GIS notwendig.
2. **Rechte-/versioniert vorliegende Regionspolygone und reale Anlagenposition:** GeoPandas `sjoin` mit nachgewiesenem CRS verwenden.
3. **Nur offizielle fractional NetCDF-Maske:** Zelle und alle Regionanteile ermitteln; bei eindeutiger Zelle zulässige Region zuordnen. **Bei mehreren möglichen Regionen** zusätzliche Standort-/Regionsinformation verlangen, keine unmarkierte Mehrheits-/Nearest-Entscheidung.
4. **Nur elektrischer Busstandort:** nur verwenden, wenn dessen Repräsentativität für den Anlagenstandort ausdrücklich belegt ist; im Zweifel `UNRESOLVED_LOCATION`.

**Nie** aus `mask_fraction=0.6` schließen, dass 60 % der Leistung einer Kraftwerksanlage dieser Region zuzuweisen seien. **Installierte MW/MWp-Anteile** müssen aus echten Anlagen-/Portfolioinformationen stammen.

---

## 4. Der bestehende PyPSA-Eur-Workflow und der kleinste PECD-Eingriff

PyPSA-Eur ist kein gleichbedeutendes Synonym für PyPSA-Core: Es ist ein **Snakemake-Modellaufbau-Workflow** mit zusätzlichen Quell- und Raumannahmen. Nach geprüfter Implementierung wird der klassische Pfad wie folgt durchlaufen: [Q07], [Q08], [Q16], [Q17]

```text
PyPSA-Eur Standardfall:
ERA5/SARAH → Atlite cutout → Land-Eligibility → CF/Potenzial je Netzregion
                                                       |
                      Regionalisiertes/clustered Network
                                                       |
                        add_electricity / compose_network
                        (fügt Generatoren/Loads/Hydro hinzu)
                                                       |
                                PyPSA.Network mit Profilen
```

**Warum kein reiner NetCDF-Dateiaustausch genügt:** `attach_wind_and_solar()` in `scripts/add_electricity.py` erwartet neben `profile` je nach Technologie die Daten `p_nom_max` und bei Offshore `average_distance`. Es **erzeugt Generatoren** via `n.add("Generator", ...)`. Auch `attach_load()` erzeugt neue `Load`-Komponenten. Der Standard-`compose_network` liest `networks/clustered.nc`. Das passt fachlich **nicht** zu einem bereits vollständigen detaillierten Netz mit vorhandenen Originalgeneratoren. [Q16], [Q17]

Für IoSN-M1 bleibt das **wissenschaftliche Datenflussprinzip** von PyPSA-Eur erhalten:

```text
Datenquelle → Zeitreihen normalisieren → räumlich/technologisch zuordnen
           → mit vorhandener PyPSA-API an bestehende Komponenten binden
```

**Nicht** übernommen werden die im Standardfall nötigen Schritte zur **Erzeugung neuer Kraftwerke**, zur Berechnung von **Neubaupotenzialen** oder zur **Netzaggregation**. Das ist ein zusätzlicher **Input-/Attach-Modus**, keine neue PyPSA-Engine und kein Core-Eingriff.

### 4.1 Was sich bei einem Wechsel ERA5 → PECD fachlich ändert

| Verarbeitungsschritt | ERA5/Atlite-Pfad | PECD-Energieindikator-Pfad | Änderungsaufwand |
|---|---|---|---|
| Daten beschaffen und lesen | ERA5/SARAH-Wetterdaten | CDS-/TYNDP-PECD-CSV/NetCDF | Source-Auswahl-/Formatadapter |
| Wetter → CF berechnen | Atlite Wind-/PV-Modell | fertige PECD-WON/WOF/SPV-CF | **entfällt** im Native-CF-Modus |
| Regionen-/Rastergeometrie | Atlite-Cutout/Netzregionen | offizielle PECD-Region/ORIG-Raster | Geometrie-Input wechseln, **Matchingalgorithmus bleibt GeoPandas** |
| Generatorzuordnung | neue Generatoren je Netzregion | **vorhandene Generator-ID** anhand Standort/Technologie → Quellprofil | kleiner ID-/Metadaten-Crosswalk |
| Profilanwendung | `n.add(Generator, p_max_pu=...)` | nur `n.generators_t.p_max_pu` bestehender IDs | dünne Attach-Routine |
| PyPSA Core / Solver | bestehend | **identisch** | **keine** |

---

## 5. Empfohlene Zielarchitektur: nur zwei eigentliche Adapterfunktionen

```text
     OFFIZIELLE PECD-DATENQUELLE                    BEREITS EXISTIERENDES PYPSA-NETZ
     Region-CF CSV / SPV-ORIG NetCDF                n.generators / n.buses / n.stores etc.
                   |                                            |
      [A] vorhandener Open-TYNDP-Reader +          optionale reale Anlagenstandorte
          schmaler PECD-Format-/Metadatenadapter                  |
                   |                                            |
       Source profile data (time, region/cell,       Plant data (generator_id,
               technology, weather_id)                    x/y, carrier)
                   |                                            |
                   +------------------------+-------------------+
                                            |
                               [B] GeoPandas/Atlite
                            Spatial + Technology Join
                         Region-/Pixel-ID → Generator-ID
                                            |
                              generator_cf(time, gen_id)
                                            |
                              [C] PyPSA-Core DataFrame
                              attach: generators_t.p_max_pu
                                            |
                          ORIGINALNETZ + VERFÜGBARKEITSZEITREIHEN
```

**A – Source Adapter:** Adapter über die vorhandenen Open-TYNDP-Reader für **regionale** PECD-CSV. Das Open-TYNDP-Skript `prepare_tyndp_pecd_release.py` liest PECD-Dateien mit den zehn Metadatenzeilen und `Date`/`Hour`/`WS###`-Spalten. `clean_tyndp_pecd_data.py` bindet die Dateisuche jedoch an `buses_tyndp` und deren Knotennamen. **Diese Bindung wird für den quellenagnostischen Reader entfernt bzw. durch echte Quell-Region-/Profil-IDs ersetzt.** Keine Neuimplementierung der CSV-Parsing-Grundfunktion. [Q09], [Q10], [Q11]

**Nur wenn griddiertes `SPV ORIG` gefordert und physisch verfügbar ist:** ergänzend `xarray.open_dataset` mit echter Variablen-/Dimensions-/Koordinaten-/Technologie- und Zeitselektion; Lazy/Chunked Zugriff auf **nur benötigte PV-Zellen**. Die genauen PECD-Variablennamen werden erst anhand einer Originaldatei festgelegt. **Ein neuer allgemeiner NetCDF-Framework-Parser ist nicht nötig.** [Q13]

**B – Generic Spatial Profile Assignment:** Verwende denselben technischen Algorithmus wie PyPSA-Eur für GeoPandas Punkt/Polygon-Join, ergänzt um **eine andere Zuordnungstabelle**:

`existing_generator_id → PECD_source_profile_id (+ technology_variant, evidence, optional weight)`.

Die Geometriequelle kann ebenso von ERA5-, PECD- oder anderen Wetterprodukten stammen; Geometrieprädikate bleiben unverändert. Unterschiede entstehen in **Quellmetadaten, räumlicher Auflösung, Technologie und Einheit**, nicht in der grundlegenden GIS-Operation. Das Mapping wird **einmal pro Netz-/Anlagen-/Quellgeometriestand** erzeugt und für alle fünf Wetterdatensätze **wiederverwendet**, soweit die Regionsdefinition identisch bleibt. [Q04–Q07]

**C – Dynamic Attribute Attachment:** Das ist **kein neues Subsystem**. Ein kleiner, überprüfbarer Python-Schritt formatiert `DataFrame(index=n.snapshots, columns=existing_generator_ids)`, prüft vorher vollständige Sourceabdeckung, Zielkomponenten, vorhandene Profile, `0≤p_max_pu≤1`, Einheiten und schreibt ausschließlich die freigegebenen Spalten des bestehenden PyPSA-Netzes. Keine `n.add()`-Aufrufe, kein Netzumbau. [Q01–Q03]

### 5.1 Minimale technische Dateistruktur (Vorschlag, **keine** Ist-Implementierung)

```text
m1_pecd/
    source.py       # Open-TYNDP regionalen Reader adaptieren;
                    # optional nativer ORIG-SPV-xarray-Slice
    mapping.py      # GeoPandas/Atlite auf PECD-Geometrien und
                    # bestehende Generator-IDs anwenden
    attach.py       # dünner PyPSA-DataFrame-Writer, Zeit-/Overwrite-Gates
rules/
    pecd_profiles.smk  # kleine optionale Snakemake-Regel
tests/
    test_pecd_source.py
    test_pecd_mapping.py
    test_pecd_attach.py
```

`attach.py` ist lediglich eine **kleine Integrationsroutine**, keine dritte Fachengine. Ein bereits verlässlicher Writer aus dem vorhandenen Projekt kann unverändert genutzt werden; in diesem Dokument ist keine frühere IoSN-Implementierung Voraussetzung.

### 5.2 Schnittstellen, bewusst klein gehalten

| Schnittstelle | Eingabe-/Ausgabeformat | Pflichtfelder |
|---|---|---|
| `SourceSelection` | Konfiguration / kleines Manifest | PECD-Version + `file_version`, Produkt (`WON/WOF/SPV`), spatial level, Technologieklasse, Klima-/Weather-ID, Pfad, Zeitbasis, Sourcehash |
| `ProfileSource` | `xarray` oder `pandas` | `time`, `profile_id` **oder** native `latitude/longitude`, `capacity_factor` bzw. `source_unit`; unveränderte Originalidentitäten |
| `GeneratorLocations` | Read-only Tabelle, bei Bedarf externe Geotabelle | `existing_generator_id`, `bus`, `carrier`, `p_nom`, Standortkoordinate + CRS oder belegte PECD-Region-ID; Standortqualität |
| `ProfileAssignment` | kleine `CSV/Parquet` | `generator_id`, `source_profile_id`, `technology_variant`, `method`, `evidence`; optional belegter MW-/MWp-Anteil |
| `GeneratorAvailability` | `pandas.DataFrame` oder `xarray.DataArray` | `time × existing_generator_id`, normierter `p_max_pu`, Weather-ID |
| `PyPSA Output` | `pypsa.Network`/optionales `.nc` | ursprüngliche statische Tabellen/IDs unverändert; ausschließlich erlaubte dynamische Serien hinzugefügt |

**Keine Verpflichtung zur Übernahme** eines speziellen M0-`DetailedNetworkReference`-/CGMES-Sidecar-Schemas als PECD-Eingabevertrag. Für **jedes** vorhandene, qualifizierte PyPSA-Netz genügen die genannten Standardattribute und – wo für das Matching nötig – ein **separater** Standortdatensatz. Die Herkunft des Netzformats ist fachlich unabhängig.

---

## 6. Matchingregeln nach Technologie

### 6.1 Wind – bereits regional gelieferter PECD-CF

Für einen vorhandenen Windgenerator `g` mit zugeordneter Quellregion `r(g)`, technischer PECD-Klasse `k(g)` und Wetterfall `w`:

`p_max_pu[g,t,w] = CF_PECD[r(g),k(g),t,w]`.

**Mehrere Generatoren** dürfen denselben CF erhalten, während `n.generators.bus`, `n.generators.p_nom` und sämtliche Leitungs-/Transformatordaten unverändert bleiben. Das ist **kein Netzclustering** und keine neue Berechnung eines feineren Wind-CF. Für echte Windparks ist der Parkstandort oder eine belegte Quell-Regions-ID vorzuziehen; landseitiger Offshore-Netzanschluss darf keine Turbinenkoordinate ersetzen. [Q12], [Q05]

**Resource Grades und Technologiemodelle:** Der PUG unterscheidet bestehende Windtechnologien, unterschiedliche Specific-Power-/Hub-Height-Auslegungen und – bei zukünftigen Anlagen – `ReGrA`/`ReGrB`. Ein rein geometrischer Join genügt daher **nicht**, solange die richtige Profilvariante nicht anhand einer belegten technischen/planerischen Regel ausgewählt ist. [Q12]

### 6.2 PV – native Rasterzelle oder offizielle Regional-CF

Für `SPV ORIG`: tatsächlicher PV-Anlagenstandort → Rasterzelle des **physisch bezogenen** 0,25°-Produkts; Technologieklasse `industrial rooftop`, `residential rooftop`, `utility fixed` oder `utility 1-axis tracking` passend zur Modellanlage auswählen. **Keine künstliche Aggregation in eine TYNDP-Region vor der Zuordnung**, wenn das native Raster tatsächlich verfügbar ist. [Q12], [Q13]

**Einheitenentscheidung:** PECD-`SPV` ist in **MW/MWp** normiert; PyPSA-`p_nom` repräsentiert häufig die elektrische AC-MW-Nennleistung. Liegen `P_DC_MWp`, `P_AC_MW` sowie eine freigegebene Wechselrichter-/Clipping-/Verlustannahme vor, kann eine geeignete `p_max_pu`-Umrechnung definiert werden; **ohne diese Angaben nicht** ohne Weiteres das PECD-`MW/MWp`-Profil als AC-`p_max_pu` zertifizieren. [Q12]

### 6.3 Bereits vorhandene mehrteilige Generatoren

Nur wenn ein **einzelner vorhandener Generator** nachgewiesen Anlagenanteile in mehreren PECD-Profilregionen zusammenfasst, ist ein belegtes kapazitätsgewichtetes Mapping zulässig:

```text
CF_g(t) = Σ_r a_(g,r) · CF_r(t) ;  a_(g,r) ≥ 0, Σ_r a_(g,r) = 1
```

Die `a_(g,r)` sind Anteile der tatsächlich vertretenen MW bzw. PV-MWp. **Die fraktionalen geografischen Regionsmasken sind nicht automatisch diese Gewichte.** Ohne Teilanlagen- und Kapazitätsdaten keine frei erfundene Mischzuordnung.

### 6.4 Hydro – eigener optionaler fachlicher Pfad

Wenn M1 neben Wind/PV auch **PECD-Hydro-Zuflussenergie** importieren soll, wird die vorhandene Datenlese- und Speichersemantik von Open-TYNDP/PyPSA-Eur wiederverwendet, **nicht** dieselbe Point-in-Polygon-Regel wie für Wind. Die PECD-Quelle liefert vielfach **`SZON`-Wochenenergie in MWh**; sie ist weder eine stündliche reale Wasserzuflussmessung noch unmittelbar eine `StorageUnit.inflow`-Zeitreihe. [Q12], [Q18], [Q19]

Nur mit dokumentiertem `SZON/TSO/Hydrologie→existing_hydro_asset`-Anteil und zur Netzkomponente passender physikalischer Konvention gilt:

```text
Σ_(Stunden im Originalintervall) inflow_MW(t) · Δt_h
   = dokumentiert dem Asset zugeteilte Modell-Energie_MWh.
```

Stundenverteilung aus Wochenwerten ist eine **explizite zeitliche Modellannahme**. Generation `HRG/HRO/HPO` darf nicht als natürlicher Zufluss `HRI/HRR/HPI/HOL` interpretiert werden. Hydro ist ein **optionales fachliches Erweiterungsprofil** des minimalistischen PECD-Wind-/PV-Moduls, nicht ein Grund, einen allgemeinen neuen Matching-Kern zu entwickeln.

### 6.5 Elektrische Last / DFT

Die stündliche `Load.p_set`-Belegung ist in PyPSA vorhanden, aber **PECD-Wind-/PV-CF** enthalten keine direkt auf einzelne Lasten übertragbaren Nachfrageprofile. Falls M1 auch DFT-/TSO-Lastprofile verteilen soll, ist eine **separat beschlossene Lastquellen-/Verteilungsregel** nötig. PyPSA-Eur besitzt regionales Demand-Upsampling, aber dessen Bevölkerung/GDP-Schlüssel sind nicht automatisch die richtigen lokalen Lastgewichte eines bereits existierenden Detailnetzes. [Q20], [Q01]

**Empfehlung:** Das PECD-Wind-/PV-MVP nicht vom DFT-/Load-Scope abhängig machen; vorhandene bereits qualifizierte `n.loads_t.p_set` nicht überschreiben.

---

## 7. Größte fachlich-technische Herausforderungen und Minimalmaßnahmen

| Priorität | Tatsächlicher Konflikt | Kein unnötiger Neubau; erforderliche Maßnahme |
|---|---|---|
| **P0** | Bus-Koordinate ist nicht zwingend Anlagenposition (Offshore, Sammelparks, synthetische Busse) | Unabhängige Anlagenort-/Region-ID-Tabelle; bestehender GeoPandas-`sjoin` erst mit qualifizierten Geometrien. |
| **P0** | Regionaler Wind-CF vs. griddierte PV-CF; meteorologisches `ORIG` ist nicht automatisch CF | Produktkatalog genau nach PUG; keine 0,25°-Wind-CF behaupten. |
| **P0** | Unklare echte Source-Version/-Dateien/-Weather-IDs | **Ein reales Sample je bezogenem Produkttyp**, Metadaten/Bytes/Variablen/CRS prüfen; fünf fixe Weather-IDs aus vorhandenem Datenentscheid übernehmen. |
| **P1** | PECD float-NetCDF-Masken liefern Flächenanteile, kein eindeutig exakt lokalisierbares Grenzpolygon | Direkte belegte Regions-ID oder Polygon bevorzugen; mehrdeutige Grenz-Zellen ablehnen und markieren. |
| **P1** | PV: `MW/MWp` vs. bestehendes `MW_AC` | DC/AC-Konvention + technische Quelle klären, dann erst normalisieren. |
| **P1** | Unzulässige PECD-Default-/Wetterjahr-Fallbacks | `fill_gaps_method=zero/mean`, automatische `safe_planning_horizon`-Ersetzung und nicht verfügbare `WS###` **nicht** für Pflichtprofile akzeptieren. |
| **P1** | PyPSA `set_snapshots` und Serienimport können fehlende Zeitwerte mit Defaults ergänzen | **VOR** Import vollständige Zeitachsen-/NaN-/Coverage-Validierung; UTC- und Kalenderkonvention aus Originaldaten nachweisen. [Q02], [Q03] |
| **P2** | Pan-europäisches 0,25°-Raster × 5 Wetterfälle kann groß werden | xarray selektiert relevante Zellen, ggf. chunked/Dask; kein europäischer Full-Grid-Eager-Load. [Q13] |
| **P2** | Falscher Write-Pfad erzeugt zweite Komponenten | PyPSA-Eur-`compose_network` für diesen Scope nicht auf bestehende Anlagen anwenden; nur dynamische Attribute an vorhandene IDs schreiben. [Q16], [Q17] |

**Zusätzliche PUG-Korrekturhinweise:** PECD-Datei-`version/fv1/fv2` und etwaige reprozessierte Wind-/Klimaszenarien sind laut „Known issues“ ausdrücklich relevant. `PECD v4.2` allein ist **kein** vollständiger Source-Fingerprint. [Q12]

---

## 8. Minimaler Ausführungsworkflow und Umsetzungsschnittstelle

### 8.1 Snakemake (ein optionaler Datenzweig statt neuer Workflow)

```text
get_pecd_inputs     [reused Open-TYNDP/CDS, source-pinned]
       |
normalize_pecd      [thin regional CSV + optional native PV ORIG]
       |
match_existing_ids  [GeoPandas/Atlite with PECD source geometry]
       |                                existing_pypsa_network.nc (read only)
       +----------------------------------------------------|
                              |
                       attach_timeseries
                              |
                     generator_cf(time, generator_id)
                              |
                 optional copy of PyPSA.Network + p_max_pu
```

Die Matchingtabelle wird **nicht für jedes Wetterjahr neu berechnet**, solange Netz-/Generatorinventar, Anlagenstandorte, Regionengeometrie und Technologieklassifizierung unverändert bleiben. Wetter-/Planungsjahre beeinflussen die **Profilwerte**, nicht den geografischen Algorithmus.

Für diese Anwendung **nicht** erforderlich: `build_cutout`, `determine_availability_matrix`, `build_renewable_profiles` zur erneuten meteorologischen CF-Erzeugung, `cluster_network`, vollständiges `compose_network`, neuer AC-Lastfluss oder Solver.

### 8.2 Ein präziser kleiner Programmvertrag

```python
# Architekturskizze; keine behauptete vorhandene Upstream-API.
profiles = read_pecd_native(source_selection)          # time × PECD profile
assignments = match_to_existing_generators(             # generator_id → profile_id
    network.generators,
    qualified_generator_locations,
    pecd_geometry,
    technology_crosswalk,
)
generator_cf = select_and_normalize(profiles, assignments, weather_id)
network_with_profiles = attach_availability_to_existing_ids(
    network, generator_cf, overwrite_policy="reject"
)
```

`read_pecd_native` und `match_to_existing_generators` sind nur **schmale projektspezifische Adapter über bestehende Bibliotheken**, keine Forderung zur Neuimplementierung von `pandas`, `xarray`, GeoPandas oder Atlite. `attach_availability_to_existing_ids` verwendet normale PyPSA-DataFrames.

**Primärprodukt kann `generator_cf` sein**, sodass Modul 1 nicht verpflichtet ist, neue physische Netzdateien herzustellen. Die optional exportierte Netzdatei ist eine **Kopie desselben Netzes mit zusätzlichen erlaubten dynamischen Attributen**, nicht ein neuer Netzerzeugungsprozess.

---

## 9. Tests, messbare Abnahme und korrekte Evidenzklassen

### 9.1 Source-only, ohne ein reales Netz erforderlich

- Echte PECD-Regional-CSV und ggf. SPV-ORIG-NetCDF mindestens **je ein Formatbeispiel** gelesen; Felder, `lat/lon`/Regionen, Zeitkodierung, Units, Produkt-/Szenario-/Dateiversionen und Source-Hashes identifiziert.
- Offizielle `PEON/PEOF/P2ON/P2OF`-Maske korrekt geöffnet und ihre fraktionalen Grenzzellen nachgewiesen; keine erfundene Shapefile-Genauigkeit.
- Kein stilles Ersetzen fehlender `WS`-/Klima-/Zeithorizonte; fünf vorhandene Weather-ID-Entscheidungen werden **als gegeben** behandelt.
- Wenn `ORIG` physisch nicht gewählt/zugänglich ist: **kein** Pflicht-ORIG-Reader implementieren oder PASS behaupten.

### 9.2 Mapper-Fixtures, mit kleinem künstlichem Netz möglich

- Zwei Originalgeneratoren an verschiedenen Bussen, jedoch in derselben `PEON`-Region erhalten dasselbe regionale CF; Bus und `p_nom` bleiben identisch.
- PV-Anlagen in zwei verschiedenen ORIG-Zellen erhalten unterschiedliche CF aus dem tatsächlich ausgewählten Quellgrid; ein regionales SPV-Produkt wird nicht als `ORIG` etikettiert.
- Offshore-Parkstandort und Küsten-Anschlussbus werden unterschiedlich behandelt; synthetischer/ungeprüfter Bus darf nicht still als Parkstandort gelten.
- Eindeutige Region, Grenz-Zelle mit zwei positiven Maskenwerten, fehlender Anlagenstandort, veraltete Region-ID, falsche Technologie, fehlerhafte Quellzeitachse und vorhandenes `p_max_pu` werden positiv/negativ getestet.
- PV-MWp/AC-MW; Composite nur mit echten MW-Anteilen; kein unzulässiger `nearest`-Fallback.

### 9.3 Echte fünf Wetterdatensätze, nur nach verfügbarer Quelle

- Pro `weather_id` und benötigtem Horizont stündliche Index-/Coverage-Konsistenz, **genau vorhandene Generator-IDs**, keine fremden IDs und keine ungeschriebenen Pflichtprofile.
- Quellwerte und Daten nach dem Spatial-/Technologie-/Einheitenmapping stimmen; Wind-`p_max_pu` innerhalb physikalisch zulässiger Werte.
- Vor-/Nachher-Fingerprint **aller statischen PyPSA-Komponententabellen** unverändert; bereits bestehende unbeteiligte Last-/Erzeugungszeitreihen unverändert.
- PyPSA-NetCDF-Roundtrip, Versions-/Quellprovenienz und ein begrenzter unabhängiger Integrationstest dokumentiert.

**Stufen:** `STATIC_SOURCE_VERIFIED` ≠ `FIXTURE_PASS` ≠ `REAL_PECD_INPUT_PASS` ≠ `REAL_EXISTING_NETWORK_JOIN_PASS`. Ein grüner CSV-/Fixture-Test ist **kein** Nachweis für korrektes geografisches Matching mit echten PECD-Regionen.

---

## 10. Der tatsächlich minimale nächste Arbeitsauftrag

**Empfehlung: ein einziges kleines, zusammenhängendes M1-Implementierungsmakro**, dessen erste Pflichtoperation **physische Source-Samples** sind. Keine Wiederholung separater generischer Reader-/Mapper-/Composer-Architekturarbeiten:

1. **Reale Produktsamples prüfen**: Offizielle PECD-v4.2-Kapazitätsfaktor-Dateien `WON/WOF/SPV` in der gewünschten Auflösung (regional CSV / ggf. SPV ORIG NetCDF), offizielle Regionmasken und die fünf bereits gewählten Weather-IDs. Bestehendes Generator-/Anlagenort-Schema als kleines anonymisierbares Read-only-Sample; *keine Netzimport-/Netzproduktionsarbeiten*.
2. **Nur den tatsächlich fehlenden Delta-Code ergänzen:** Open-TYNDP regionaler Reader ohne TYNDP-Bus-Abhängigkeit; ggf. `ORIG`-SPV-xarray-Selektion; GeoPandas-Matcher mit **PECD-Profil-ID-Ausgang**; kleine PyPSA-Zeitreihenanbindung.
3. **In einem Lauf testen und berichten:** Source-/Geo-/Technik-/Time-/MW-Normierung, Netzinvarianz, kleine Snakemake-/PyPSA-Fixtures; realer PASS nur wenn tatsächlich echte Dateien und ein geeignetes bereits existierendes Netz-/Standortpaket zugänglich sind.

**Kein genereller PyPSA-Core-Änderungsauftrag.** Keine vollständige alternative PyPSA-Eur-Pipeline. Hydro nur in den Auftrag aufnehmen, wenn wirklich eine M1-Hydro-Zuflussintegration benötigt wird und die dazugehörigen Anlagen-/Einheiteninformationen vorliegen. DFT-Lastintegration separat behandeln.

---

## 11. Entscheidungsregister

| ID | Entscheidung | Begründung / Prüfnachweis |
|---|---|---|
| **ADR-M1-01** | PyPSA-Core bleibt unverändert. | Dynamic Series und Netz-I/O existieren [Q01–Q03]. |
| **ADR-M1-02** | Generisches Geomatching wird **wiederverwendet**, nicht neu erfunden. | GeoPandas + PyPSA-Eur `map_to_country_bus` als algorithmisches Vorbild [Q04–Q07]. |
| **ADR-M1-03** | Open-TYNDP-`PECD`-Regional-Reader wiederverwenden, aber TYNDP-Knotenbindung von PECD-Quellidentitäten lösen. | PECD-Code filtert aktuell über `buses_tyndp` [Q09–Q11]. |
| **ADR-M1-04** | ORIG-SPV-NetCDF nur bei echter Produktanforderung ergänzen; native Wind-CF bleiben regional. | PECD-PUG Tabellen 2.12/3.6 [Q12]. |
| **ADR-M1-05** | Vorhandene Generatoren werden ausschließlich durch dynamische Attribute ergänzt. | Standard-PyPSA-Eur-Composer legt andernfalls Komponenten an [Q16], [Q17]. |
| **ADR-M1-06** | Standortmetadaten dürfen separat geliefert werden; Netzimportformat ist für M1 irrelevant. | Elektrischer Anschlussbus ≠ zwingend Anlagenort; M1 ist datenformatagnostisch. |
| **ADR-M1-07** | Fünf bereits entschiedene Wetterfälle bleiben Pflichtinput, ohne automatische Ersetzung. | Open-TYNDP-2026-Standard-`WS` und `fill_gaps_method` sind keine unbedingte Zusicherung der fünf Projektquellen [Q10], [Q21]. |
| **ADR-M1-08** | Source-/Geo-/Netz-Gates werden getrennt nach Evidenzklasse abgenommen, ohne neue Governance-Plattform. | Reale Quellbytes/Anlagenstandorte müssen getrennt belegbar bleiben. |

**Offen und erst durch Originaldaten entscheidbar:** konkrete PECD-Dateivarianten und NetCDF-Variablennamen; P2ON- versus PEON-Regionsversion; Grenz-Zellen-Auflösung; Standortqualität der relevanten Anlagen; Windtechnologie-/Resource-Grade-Wahl; PV `MWp/DC` vs. `p_nom/AC`; tatsächliche Weather-ID-/Horizon-Abdeckung. Das sind **Eingangsdaten- und Modellsemantikfragen**, keine Gründe für einen neuen generischen Mapper.

---

## 12. Quellennachweise – offizielle Dokumentation und Source Code

Alle GitHub-Quellen sind auf **unveränderliche Commit-SHAs** gepinnt. Die Stände wurden am **02.11.2026** überprüft; der PECD-Produktkatalog ist die offizielle CDS/PUG-Quelle. Aussagen in Abschnitt 3 sind **Produktdokumentationsbefunde**; Aussagen über Funktionen in Abschnitt 2 sind **direkt aus Quellcode geprüfte Befunde**; vorgeschlagene Interfaces und Risikopolitiken sind **Architekturentscheidungen**, keine behaupteten Upstream-APIs.

### PyPSA-Core

[Q01]: https://docs.pypsa.org/latest/user-guide/design/ "PyPSA – Design, Snapshots und zeitveränderliche Komponentenattribute"
[Q02]: https://github.com/PyPSA/PyPSA/blob/d21e028d3198490b6d5d310ccb199a76393775a2/pypsa/network/index.py#L48-L145 "PyPSA-Core – set_snapshots, Zeitzonen und Default-Fill bei Reindex"
[Q03]: https://github.com/PyPSA/PyPSA/blob/d21e028d3198490b6d5d310ccb199a76393775a2/pypsa/network/io.py#L2107-L2205 "PyPSA-Core – DataFrame Time-Series Import, Default-Fill und bestehende Komponentennamen"

- **[Q01]** [PyPSA: Design, Snapshots, Component Time Series](https://docs.pypsa.org/latest/user-guide/design/) – Nutzer- und API-Dokumentation, `n.generators_t.p_max_pu`.
- **[Q02]** [PyPSA `network/index.py` – `set_snapshots`](https://github.com/PyPSA/PyPSA/blob/d21e028d3198490b6d5d310ccb199a76393775a2/pypsa/network/index.py#L48-L145) – exakter Quellcode.
- **[Q03]** [PyPSA `network/io.py` – zeitabhängige DataFrames](https://github.com/PyPSA/PyPSA/blob/d21e028d3198490b6d5d310ccb199a76393775a2/pypsa/network/io.py#L2107-L2205) – exakter Quellcode, interne Importmethode als Beleg, **nicht** als empfohlene private Projekt-API.

### Geomatching / PyPSA-Eur / Atlite

[Q04]: https://geopandas.org/en/stable/docs/reference/api/geopandas.sjoin.html "GeoPandas – sjoin und topologische Prädikate"
[Q05]: https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/build_powerplants.py#L129-L173 "PyPSA-Eur – map_to_country_bus"
[Q06]: https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py#L150-L208 "Atlite – compute_indicatormatrix"
[Q07]: https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/build_renewable_profiles.py#L1-L43 "PyPSA-Eur – erneuerbare Profilmodellierung und Raumauflösungen"
[Q08]: https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/rules/build_electricity.smk#L328-L421 "PyPSA-Eur – Availability/RES-Snakemake-Rules"
[Q16]: https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/add_electricity.py#L389-L569 "PyPSA-Eur – attach_load und attach_wind_and_solar, n.add"
[Q17]: https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/rules/compose.smk#L15-L70 "PyPSA-Eur – clustered network als Composer-Input"
[Q20]: https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/build_electricity_demand_base.py#L139-L232 "PyPSA-Eur – nationale/regional verteilte Lasten"
[Q22]: https://docs.xarray.dev/en/stable/generated/xarray.open_dataset.html "xarray – NetCDF, lazy und chunked selection"

- **[Q04]** [GeoPandas `sjoin`: Punkt/Polygon-Join](https://geopandas.org/en/stable/docs/reference/api/geopandas.sjoin.html).
- **[Q05]** [PyPSA-Eur `map_to_country_bus` im Originalcode](https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/build_powerplants.py#L129-L173).
- **[Q06]** [Atlite `compute_indicatormatrix`](https://github.com/PyPSA/atlite/blob/0d4ff8f703a99566b475b8d775aa2e74309123ee/atlite/gis.py#L150-L208).
- **[Q07]** [PyPSA-Eur `build_renewable_profiles.py`](https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/build_renewable_profiles.py).
- **[Q08]** [PyPSA-Eur `build_electricity.smk`](https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/rules/build_electricity.smk).
- **[Q16]** [PyPSA-Eur `attach_wind_and_solar` / `attach_load`](https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/add_electricity.py#L389-L569).
- **[Q17]** [PyPSA-Eur `compose.smk`](https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/rules/compose.smk#L15-L70).
- **[Q20]** [PyPSA-Eur `build_electricity_demand_base.py`](https://github.com/PyPSA/pypsa-eur/blob/8d4b7d3073e027f52aabcd4675afcb47b767cdc5/scripts/build_electricity_demand_base.py).
- **[Q22]** [xarray `open_dataset` und Lazy/Chunked NetCDF](https://docs.xarray.dev/en/stable/generated/xarray.open_dataset.html).

### Open-TYNDP – bereits implementierter PECD-Reader

[Q09]: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/prepare_tyndp_pecd_release.py#L20-L113 "Open-TYNDP – PECD-CSV-Parser, WS-Spalten und prebuilt"
[Q10]: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py#L34-L154 "Open-TYNDP – region-knotenbasiertes PECD-CSV-Laden"
[Q11]: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_renewable_profiles_pecd.py#L1-L74 "Open-TYNDP – profile(time,bus,bin,year)"
[Q18]: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_hydro_inflows.py "Open-TYNDP – Hydro-Source-Aufbereitung"
[Q19]: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_hydro_profile.py "Open-TYNDP – zonale Hydro-Profile"
[Q21]: https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/config/config.tyndp.yaml#L1-L40 "Open-TYNDP 2026 – konfigurierte Standard-WS"

- **[Q09]** [Open-TYNDP `prepare_tyndp_pecd_release.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/prepare_tyndp_pecd_release.py).
- **[Q10]** [Open-TYNDP `clean_tyndp_pecd_data.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py).
- **[Q11]** [Open-TYNDP `build_renewable_profiles_pecd.py`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_renewable_profiles_pecd.py).
- **[Q18]** [Open-TYNDP Hydro-Dateileser](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_hydro_inflows.py).
- **[Q19]** [Open-TYNDP Hydro-Profilaufbereitung](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_hydro_profile.py).
- **[Q21]** [Open-TYNDP `config.tyndp.yaml`](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/config/config.tyndp.yaml).

### Copernicus CDS / PECD v4.2 – normative Datenquelle

[Q12]: https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752 "PECD v4.2 Product User Guide, Tab. 2.12 / 3.6"
[Q13]: https://cds.climate.copernicus.eu/datasets/sis-energy-pecd?tab=overview "Copernicus CDS – PECD Energy Dataset, gridded / regional forms"
[Q14]: https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752 "PECD PUG Tab. 4.2 / 4.3 und Gewichte/Regionmasken"
[Q15]: https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752 "PECD PUG Kap. 2.5: räumliche Aggregation und Bruchteil-Masken"

- **[Q12]** [PECD-v4.2 Product User Guide](https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752) – **Tabellen 2.12 und 3.6**, Produktauflösung, Technologie, Zeitschritte, Einheiten; Abschnitt „Known issues“ für reprozessierte `fv2`-Daten.
- **[Q13]** [Copernicus CDS – Pan-European Climate Database (PECD)](https://cds.climate.copernicus.eu/datasets/sis-energy-pecd?tab=overview) – offizielle Produktfamilien, Raster-/Regionsdaten, Abruf.
- **[Q14]** [PECD-v4.2 Product User Guide, Tabellen 4.2 und 4.3](https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752) – offizielle Dateien `ANCI_PEON-mask`, `ANCI_P2ON-mask`, `ANCI_PEOF-mask`, `ANCI_P2OF-mask`, `ANCI_SZON-mask`.
- **[Q15]** [PECD-v4.2 Product User Guide, Kapitel 2.5](https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=540941752) – Polygon-/Fraktionsraster, Aggregationsdefinitionen und Einschränkungen.

**Versionspins für Reproduzierbarkeit (02.11.2026):**
- PyPSA-Core `master@d21e028d3198490b6d5d310ccb199a76393775a2`;
- PyPSA-Eur `master@8d4b7d3073e027f52aabcd4675afcb47b767cdc5`;
- Atlite `master@0d4ff8f703a99566b475b8d775aa2e74309123ee`;
- Open-TYNDP `tyndp-2026@71a3a9a15b77114cd79458bceabc98e1a64dd58a`.

---

## 13. Kompakte Schlussentscheidung

**Keine neue allgemeine Matching-Engine. Kein neuer allgemeiner PECD-Regional-Reader. Kein neues PyPSA-Netz- oder Solver-Modul.**

**Die einzige fachlich eigenständige M1-Erweiterung** ist die **quell-/technologie-/standortbewusste Verbindung** der PECD-Quellprofile mit den **bestehenden** PyPSA-Generator-IDs. Sie wird mit bereits vorhandenen GeoPandas-/Atlite-Funktionen umgesetzt. Das Lesen nativer `ORIG`-PV-NetCDF ist eine kleine zusätzliche Eingabefunktion, **nur wenn dieses Datenprodukt tatsächlich verwendet wird**. Die anschließende Zeitreihenanbindung übernimmt PyPSA-Core ohne API-Änderung.

Erst echte PECD-Originaldateien und belegte Kraftwerkspositionen können den letzten, entscheidenden Unterschied zwischen einer sauber spezifizierten Architektur und einer real qualifizierten Zuordnung schließen.
