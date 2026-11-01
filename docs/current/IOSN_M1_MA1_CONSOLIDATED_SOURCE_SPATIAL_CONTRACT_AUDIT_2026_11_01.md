# IoSN Modul 1 — MA-1 konsolidierte Source-, Branch-, Raumauflösungs- und Datenvertragsprüfung

**Erstellungsdatum:** 2026-11-01  
**Kennung:** \`IOSN-M1-MA1-2026-11-01\`  
**Qualifikation:** \`STATIC_ARCHITECTURE_REVIEW_COMPLETED / CONTRACT_DESIGNED / DATA-WITNESS_NOT_ASSESSED\`  
**Freeze-Gesamtentscheidung:** \`M1_MA1_CONDITIONAL_ARCHITECTURE_BASELINE__SOURCE_AND_M0_WITNESS_BLOCKED\`  
**Ausführung:** GitHub-Repositoryquellen, Branchvergleich und veröffentlichte PECD-Dokumentation **statisch** geprüft. **Keine tatsächlichen Projekt-PECD-Rohdateien, Hydro-Zeitreihen, fünf finalen WS-IDs oder produziertes M0-PyPSA-Netz vorgelegen; keine numerischen Tests / Snakemake-Runs / Produktionscodeänderungen.**

**Verknüpfte Architekturdokumente:** [M1 Basisarchitektur](IOSN_M1_PECD_PYPSA_REFERENCE_TIMESERIES_ARCHITECTURE_2026_10_30.md), [M1 Raumauflösungs-/Makroplan](IOSN_M1_SPATIAL_RESOLUTION_AND_MACRO_EXECUTION_PLAN_2026_11_01.md).

## 0. Executive Decision & Scope

MA-1 ist **als quellcodebasierte, versionierte Architektur- und Schnittstellenuntersuchung ausgeführt**. Die wiederverwendbaren Implementierungen wurden über den alten Open-TYNDP-\`master\` hinaus bis zum **TYNDP-2026-Featurebranch** geprüft. Es ist keine Neuimplementierung von PECD-Meteorologie erforderlich, wenn autoritative vorgefertigte Kapazitätsfaktoren geliefert werden.

**Ziel:** Zu bereits existierenden M0-Komponenten (\`Generator\`, \`Load\`, \`StorageUnit\`/Hydro-Store-Modell) **alle vorgegebenen meteorologischen und wasserwirtschaftlichen Zeitreihen** auf Original-IDs binden; kein erneutes Plant-Matching, keine Netzrekonstruktion, kein Clustering, keine Neuauswahl von Wetterjahren.

**Verbindliche Trennung:** M0 liefert CGMES→Canonical→elektrische PyPSA-Detailansicht samt Sidecar; M1 ist \`PECD / Hydro / DFT -> vorhandene PyPSA Component ID\`; M2 ist der getrennt verantwortete Netzreduktions-/Aggregationsprozess. Das in M0-Dokumenten verwendete interne Kürzel „M2 Architektur“ und dortige historische „Modul-1-Netzreduktion“ sind **nicht** die vorliegende projektweite Modulnummerierung. Für diese M1-Spezifikation gilt ausschließlich M0/M1-Zeitreihe/M2-Netzaggregation.

**Unbedingter Source-Gate-Vorbehalt:** Die fünf bereits extern ausgewählten Wetterdatensätze werden **unverändert** übernommen. Ihre exakten fünf Quellkennungen sind im zugänglichen M1-Projektkontext **nicht ausgewiesen**. Die veröffentlichte IoSN-Wetterjahrauswahl-Dokumentation enthält **drei** ENTSO-E-Szenarien je Zielhorizont; sie ist **kein Beleg** für die Existenz der fünf tatsächlich gewählten Projekt-Datensätze. Die Auswahl wird nicht wiederholt.

## 1. Reproduzierbare Repository-/Branch-Evidenz

GitHub-SHAs am 2026-11-01 aus den Repository-Refs gelesen; Stichprobe auf funktions- und zeitlich relevante Branches, **keine Behauptung, sämtliche historischen Branches oder Forks der Welt erfasst zu haben**.

| Software/Ref | Geprüfter Commit | Befund | M1-Reuse |
|---|---|---|---|
| **PyPSA/PyPSA** \`master\` | \`23650353eb1d059acfec28f4915ad3e068c085bf\` (2026-10-30) | \`Network.set_snapshots\`, zeitabhängige DataFrames, NetCDF, \`Network.set_scenarios\`; zuletzt #2063 Fix für Custom Time-Varying Attributes | **Core unverändert**, konkrete API-Version vor Codepin |
| **PyPSA v1.4.0** (2026-10-09) | Release-Notes aus obiger Quelle | schnellere NetCDF-Importe; definierte Stochastik- und LPF/AC-PF-Grenzen | stabile Version prüfen; nicht blind \`master\` installieren |
| **PyPSA/pypsa-eur** \`master\` | \`1526bb820e25a9faa61f32b00bfc77dd05db6b2e\` (2026-10-28) | \`build_renewable_profiles\` = Atlite-Cutout/Regionen und \`build_hydro_profile\` = Länder-Runoff/EIA; komponiert i.d.R. über \`clustered.nc\` | nur Snakemake-/xarray-Konventionen; **kein Standardkomponieren auf M0** |
| **Open-TYNDP** \`master\` | \`5b25904496150b889b321dd8d76f393ef09a0f2e\` (2026-10-28) | PECD-/PEMMDB-/Hydro-Reader, ursprünglich TYNDP-2024-Knotenzuordnung | historischer Quellanker |
| **Open-TYNDP** \`tyndp-2026\` | \`71a3a9a15b77114cd79458bceabc98e1a64dd58a\` (2026-10-29) | **PECD v4.2 + vorbereiteter Datenbestand; erneuerte Hydro-, Demand- und PEMMDB-Rules**; 47 Commits vor und 52 hinter \`master\` (divergent) | **primärer Reuse-Kandidat**, code- und datenseitig nicht unverändert übernehmbar |
| **Open-TYNDP** \`feat/sres-profiles\` | \`9967567d962c90de67a4317d3f95a75b5dc85f0f\` | weitere SRES-/Technologie-Profilentwürfe, ungemergt, divergiert | punktuell Technologieabgleich; **kein produktiver Default** |
| **Open-TYNDP** \`feat/nuclear-profiles\` | \`41781279c97fe7a24c749373bec91e2f79bf3632\` | nukleare Profile, nicht PECD-Wetter | optional für separate thermische Verfügbarkeiten |
| **PyPSA-Eur** \`custom_profiles\` | \`c39effd9abee26f14b135478d0b0ea7d8c51bca2\` (2019!) | historischer Spezialpfad; ca. 5535 Commits hinter \`master\` | **nicht portieren** |
| **PyPSA** \`fixed-profile\` | \`ef4c23edc421ab76e4174cd84843b6e9aeeb40e7\` (2024) | historischer, überholter Branch | **nicht portieren** |
| **OET pypsa-eur** \`master\` | \`ddb66caf3efefb661b03d4689279b9b54cc6cca7\` | Soft-Fork mit PyPSA-Eur-Funktionalität | allein kein eigener PECD-Detailnetzwriter |
| **OET pypsa-eur** \`feature/hydropower-modelblock\` | \`4818980473df70fdcd0e9ca1a88773eacc95e141\` (2026-09-26) | Snakemake-Modul für auf Kraftwerke bezogene HydroBASINS/Atlite-Runoff-Profile | **optionale Hydro-Vergleichsquelle**, nicht stillschweigend PECD-Ersatz |
| **modelblocks-org/module_hydropower** \`main\` | \`1daecde3e653d53da3f1ae740cc70d5d14d480eb\` (2026-10-19) | HydroBASINS-Basins, Standorte, Atlite, EIA-Nationalnormierung; plant-level inflow_mwh und zonal PU, warnt vor heuristischer nationaler Kalibrierung/subnationalen Gültigkeitsgrenzen | für räumliche Hydrozuordnung **konzeptionell wertvoll**, anderes hydrologisches Eingangssignal |
| **PyPSA/atlite** \`master\` | \`0d4ff8f703a99566b475b8d775aa2e74309123ee\` (2026-10-15) | Wetterraster, räumliche Matrix/Ressourcenkonversion | **nur für fehlende originäre CF-Produkte**, nicht wenn PECD CF verbindlich |
| **PyPSA-Earth** \`main\` | \`d64c3d9be1e75b1b0b2a347a0772b72a444a67ce\` (2026-10-28) | großräumige Datenpipeline; \`Fix_scripts_for_custom_data\` arbeitet an Custom-Daten/Potenzialen | keine vorrangige M1-Komponente identifiziert |
| **PyPSA-USA** \`master\` | \`3d67e2061e02a5b983ed9807a1b2668e7fdf6fd4\` (2026-10-26) | US-spezifische Modelle/Regeln | keine einschlägige PECD-/CGMES-Kopplung |
| **AlOussama/TYNDP_Products** \`main\` | \`1595d6d38e77804760612621657721b3699d2fea\` | Projekt-Baseline, Wetterauswahl-Methodik (nicht fünf tatsächliche Dateien) | Projektkontext |
| **M0 Architekturbranch** | \`0275f48231a0794bea324b9cab34700bb0de8f5b\` (2026-11-01) | M0-\`DetailedNetworkReference v1\` plus \`m0_sidecar\`, **DESIGNED_NOT_EXECUTED** | **M1 Input-Contract maßgeblich**, noch kein realer Import-Run |

Nachvollziehbare Quellen:
- [Open-TYNDP 2026 Rules](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/rules/sb.smk)
- [Open-TYNDP PECD v4.2 Datenledger](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/data/tyndp_versions.csv)
- [Open-TYNDP Technology Crosswalk](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/data/tyndp_technology_map.csv)
- [PyPSA-Core zeitliche Indizes](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/pypsa/network/index.py)
- [PyPSA v1.4.0 Release Notes](https://github.com/PyPSA/PyPSA/blob/23650353eb1d059acfec28f4915ad3e068c085bf/docs/release-notes.md)
- [modelblocks hydro README](https://github.com/modelblocks-org/module_hydropower/blob/1daecde3e653d53da3f1ae740cc70d5d14d480eb/README.md)
- [M0 \`DetailedNetworkReference\` Contract](https://github.com/AlOussama/TYNDP_Products/blob/0275f48231a0794bea324b9cab34700bb0de8f5b/docs/current/IOSN_Modul0_CGMES/30_CANONICAL_DATA_CONTRACT.md)

**BOM-/Lizenzregel:** Externe Code-Reuse-Patches müssen vor Übernahme SPDX/Lizenz (insb. MIT/CC0/CC-BY je Datei und Datensatz) sowie commitbezogene Provenienz prüfen; das Verlinken im Bericht stellt noch keine lizenzrechtliche oder Runtime-Freigabe dar. Unmerged Branches sind nicht installierte/pinned Production Releases.

## 2. Tatsächlich geprüfte Open-TYNDP-2026-Quellpfade und harte Findings

| Datei am \`tyndp-2026\`-SHA | Funktion | Evidenzbasierte Disposition |
|---|---|---|
| \`rules/sb.smk\` | \`retrieve_tyndp_pecd\`, \`prepare_pecd_release\`, \`clean_tyndp_pecd_data\`, \`build_renewable_profiles_pecd\`, \`clean_tyndp_hydro_inflows\`, \`build_tyndp_hydro_profile\` | **REUSE rule structure**, aber statt TYNDP-Node-SUBSTATION/busmap M0-\`asset_id\` |
| \`scripts/sb/prepare_tyndp_pecd_release.py\` | filtert \`WS###\`-Spalten aus Quelldateien; CSV \`skiprows=10\`, \`Date\`/\`Hour\` | **ADAPT**: exakt fünf extern definierte Source-IDs, Hash und Kalender; nicht out-of-range \`warn+intersect\` |
| \`scripts/sb/clean_tyndp_pecd_data.py\` | \`node.replace("GB","UK")\`, TYNDP-Node-Filenames, \`Hour-1\`; \`fill_gaps_method: zero\`/Mittelwert | **ADAPT parser only**; Name \`node\` als TYNDP-ID, **nicht** CGMES-Bus; fehlende Profile \`FAIL\` |
| \`scripts/sb/build_renewable_profiles_pecd.py\` | \`profile(time,bus,bin,year)\`, \`bin=0\`; \`safe_planning_horizon\` | **ADAPT** to \`profile_id\` and \`existing_generator_id\`; no \`safe_planning_horizon\` fallback |
| \`scripts/sb/clean_tyndp_hydro_inflows.py\` | \`WEEK\`-/Tag-Energiedaten in \`MW\` umgerechnet, \`.ffill()\`, Division durch 168/24; fehlende Regionen \`.fillna(0)\` | **ADAPT with source-interval ledger**; keine synthetischen Null-Inflow-Werte; echte Datumslänge/Teilintervalle prüfen |
| \`scripts/sb/build_tyndp_hydro_profile.py\` | \`inflow(time,bus,year,hydro_tech)\` | **ADAPT**, \`bus\` ist Zone, kein Hydro-Asset; Quellmedium \`SZON\`/TYNDP-Node |
| \`scripts/sb/_helpers.py\` | \`AVAILABLE_WSCENARIOS\` und \`safe_planning_horizon\` fallback | **DON'T REUSE** für meteorologische Source-Freeze-Semantik |
| \`scripts/sb/build_tyndp_demand.py\` | DFT/2026 Demand, wscenarios \`WS001...WS120\`; aktuell pro Horizont erster befüllter WS | optionaler Last-Reader, aber kein belegter 5-WS-Generator |
| \`data/tyndp_technology_map.csv\` | PEMMDB↔PECD↔PyPSA carrier inkl. HRR, HPI, HRI, HOL, HCL und PV rooftop/utility | **REUSE crosswalk** nach Abgleich vorhandener M0-Carrier und PyPSA-Komponententypen |
| \`data/tyndp_versions.csv\` | TYNDP 2026 und \`tyndp_pecd,4.2\` plus \`4.2+pre-built.0.1\`; Aug.-Korrekturen an Szenarioinputs | **VERSION+SHA REQUIRED**; 2026-08-21 korrigierte Inputs nicht ungeprüft mit prelim. Prebuilt vom 2026-08-13 mischen |

Quellcode-URLs:
- [PECD CSV-Filter](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/prepare_tyndp_pecd_release.py)
- [PECD Clean Reader](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_pecd_data.py)
- [PECD NetCDF Converter](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_renewable_profiles_pecd.py)
- [Hydro TYNDP 2026 Inflows](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_hydro_inflows.py)
- [TYNDP Demand Reader](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_demand.py)

**Neu gegenüber bisherigem M1-Dokument:** Die Behauptung „Open-TYNDP hat nur TYNDP-2024 PECD v3.1“ ist für den untersuchten **\`master\`** ein historischer Befund, jedoch für \`tyndp-2026\` **nicht mehr gültig**. Für M1 ist der v4.2-Branch die primäre Basis. Die Quellpipeline bleibt **zonal**, selbst wenn das elektrische Zielnetz knotenscharf ist.

### 2.1 Fünf feste Projektwetterdatensätze vs. drei befüllte TYNDP-2026-WS pro Horizont

In \`scripts/sb/_helpers.py\` sind tatsächlich befüllte TYNDP-2026-Wetter-WS je Planungshorizont definiert:

| Planungshorizont | Im geprüften Open-TYNDP-Bundle dokumentierte WS |
|---|---|
| 2030 | WS003 / WS021 / WS029 |
| 2035 | WS032 / WS037 / WS059 |
| 2040 | WS065 / WS071 / WS077 |
| 2050 | WS091 / WS092 / WS106 |

Die TYNDP-Demand-Excel-Quelldatei hat 30 Klimaszenario-Spalten je Horizont, davon sind nach Codekommentar **drei befüllt**, übrige sind Nullplatzhalter. \`get_wscenario_tyndp\` wählt aktuell per \`[0]\` das erste. Das ist **nicht** die verlangte fünf-Jahres-Integration. Die im Repository dokumentierte offizielle IoSN-Wetterjahrauswahl beschreibt ebenfalls drei offizielle Szenarien pro Zielhorizont und stellt **nicht** den unbekannten Fünferprojekt-Satz dar.

**BLOCKER SW-01 (Datenebene):** Für jedes vom Owner vorgegebenen \`(planning_horizon, weather_id)\` muss ein tatsächlich existierender vollständiger Wind-, Solar-, Hydro- und soweit benötigt Last-Datensatz nachgewiesen werden. Fünf schon gewählte Jahres-IDs **nicht ersetzen oder auswählen**. Falls offizielle TYNDP-2026-Exceldateien nur drei gebundene WS enthalten, werden **nicht** zwei aus Nullen, Mitteln oder anderen Jahren erzeugt. Für diese zwei muss die verbindliche Quelle (z. B. vollständiger CDS-PECD-Produktzugriff) und Konsistenz zu Nachfrage und Hydro vertraglich geklärt werden; andernfalls liegt \`BLOCKED_SOURCE_AVAILABILITY\` vor.

### 2.2 Version / Datenkorrektur

\`tyndp_versions.csv\` enthält eine nach 2026-08-12 korrigierte TYNDP-2026-Datenlieferung mit Versionskennzeichnung 2026-08-21 und eine vorbereitete, als *preliminary* bezeichnete PECD-4.2-Version 2026-08-13. **Keine implizite Kompatibilitätsannahme!** Für jede Datei: \`source_dataset_id\`, release/revision, SHA256, ursprüngliche Datei, Klimaindex, Gebiet, Einheit, Zeitindex, Lizenz/zugelassene Nutzung; bekannte Korrekturhinweise gesondert.

## 3. Normativer M0→M1-Contract; M0 nicht als erledigt behaupten

M0 \`IOSN-M0-CAN/1.0.0\` (Branch \`0275f482...\`) definiert \`DetailedNetworkReference v1\`, mindestens:
- \`pypsa_network\` und **\`m0_sidecar\`** (Original-CIM-Identity/Quelle, Geometrie mit CRS und Qualitätsflag, Geräte-/Portzuordnung, Synthetic-Component-Ledger und Lost-Information/Capabilities).
- \`network_revision_id\`, \`source_set_hash\`, \`mapping_policy_hash\`, ggf. \`operating_state_id\` und qualifiziertes \`PYPSA_ACPF_READY\`/LPF-Flag.
- \`asset_id\` ist kanonische, revisionierbare Geräteidentität; \`view_id\` ist die PyPSA-Projektionszeile. M1 muss \`source_asset_id ↔ pypsa_component_id\` explizit referenzieren; **keine Gleichsetzung mit raw mRID ohne Ledger**.
- Reale Busse mit nur abgeleiteten Station-Centroid-Koordinaten sind **nicht automatisch echte Erzeugungsstandorte**. 3W-Stern-Synthesebusse haben absichtlich keine reale Standortssemantik. Keine Wetterzuordnung zu synthetischen Bussen über \`x/y\`.

**M0-Status:** \`DESIGNED_NOT_EXECUTED\`, M3-Architekturreview läuft/steht aus; weder vollständige reale PyPSA-NetCDF-Datei noch sidecar/Fixture mit getesteter CGMES-Quelle ist hier belegt. \`PYPSA_ACPF_READY\`, \`REDUCTION_ADAPTER_READY\` sind **nicht** als positiv getestet behauptet. Modul 2 Netzreduktion ist nicht M1-Arbeit.

**M1 Input ist Paket statt nacktes .nc:** \`M0_ReferencePackage = (network, sidecar, identity_mapping, revision, capabilities, provenance)\`; bitte Dokumentation mit M0-Owner spiegeln. Bei fehlender Quell-ID/Geometrie gibt es nicht automatisch einen „Geokoordinaten“-PASS.

**Invarianz:** M1 verändert keine \`buses\`, \`lines\`, \`transformers\`, \`links\`, \`shunt_impedances\`, \`generators\`, \`loads\`, \`storage_units\`/Stores/Links Stammtabellen sowie Anschlüsse. Der einzige erlaubte Write-Bereich ist eine explicit versionierte **Time-series Attribute Allowlist**, primär \`generators_t.p_max_pu\`, \`loads_t.p_set\`, \`storage_units_t.inflow\`; andere Attribute nur mit eigener M1-Freigabe. Auch bereits in M0 vorliegende zeitabhängige Daten dürfen nicht stumm überschrieben werden.

## 4. Raumauflösungs- und Profilsemantik: Bindender Designvertrag

### 4.1 Physikalische Auflösungen im selben Modell

| Quellfamilie | Geografische Quelle | Profilwerte / Zeit | Zulässige M1-Zuordnung | Präzisionsgrenze |
|---|---|---|---|---|
| CGMES-M0 | Original-Topologieknoten, reale Substations und Geräte; ggf. abgeleitete Koordinaten | keine neuen Wetterwerte | unveränderte \`Generator.bus\`, Original-Asset-/PyPSA-ID | elektrisch knotenscharf ≠ wettermessstellen-scharf |
| PECD meteorologische Raster | ERA5/PECD typ. 0,25° x 0,25° | meteorologische stündliche Variablen | nur wenn daraus genehmigte Ressourcenmodelle laufen | Rohwetter ist kein CF |
| PECD Wind Onshore | PEON / P2ON und spezifische Technologie-/Ressourcenvarianten | stündliche Kapazitätsfaktoren MW/MW | Source-Region + Tech -> vorhandene Generator-ID | dasselbe regionale CF an vielen elektrischen Knoten legitim |
| PECD Wind Offshore | PEOF / P2OF | stündliche CF | **Offshore-Anlagenkoordinate** oder validierte Offshore-Zone | Bus kann landseitiger Kabelanschluss sein |
| PECD Photovoltaik | \`ORIG\` PV-CF 0,25° Raster **wenn tatsächlich bezogen**; alternativ PEON/P2ON/NUT2/SZON | stündliche CF **MW/MWp** | korrekte Rasterzelle oder Region + PV-Technologietyp + DC/AC-Mapping | keine unbewiesene lokale Auflösung; regional ≠ Originalraster |
| PECD-/TYNDP-Hydro | Source-TYNDP/SZON-Hydroregion, oft Wochen- oder Tagesenergie in MWh | nicht primär stündliche Anlagen-MW | Hydrologisches Gebiet -> existierendes Hydro-Asset nach expliziten Anteilen | elektrische Knotengeografie **bestimmt kein hydrologisches Einzugsgebiet** |
| DFT/TYNDP Load | definierte TYNDP-Gebiete, WS, Horizon | Stunden-MW | vorhandene \`Load\`-ID falls Quell-/TSO-Mapping vorhanden | regionaler Lastwert ≠ nachgewiesene Knotennachfrage |

**CDS/PECD-Regiomaske:** Für PECD v4.2 ist eine Rastermasken-/Fractional-Region-Mask-Repräsentation dokumentiert; konkret bezogene Produktmasken dürfen als Geometriequelle für Point-in-Region/intersection verwendet werden. Fractional **Flächengewichte** sind aber nicht automatisch die **Leistungsgewichte** eines über mehrere Regionen verteilten Generators. Quellkoordinaten/CRS und Randfälle separat prüfen. PECD-Produktgenauigkeit muss als Metadatum am Generatorprofil geführt werden.

Bei Offshore-Anlagen sind ggf. \`plant_location\`, \`landing_bus_location\` und \`pecd_offshore_region\` explizit verschiedene Felder.

### 4.2 Rangfolge der Zuordnung

1. **\`EXPLICIT_SOURCE_ID\`**: amtliche PECD-Profil-/Anlagenregionskennung zur bestehenden M0-Anlage.
2. **\`VERIFIED_PLANT_LOCATION\`**: mit Herkunft belegte reale Anlagenposition zu **im gleichen Quellprodukt** dokumentierter PECD-Region/Rasterzelle.
3. **\`VERIFIED_BUS_PROXY\`**: nur wenn nachweisbar repräsentativ für Generatorstandort; für große Sammelanschlüsse/offshore meist nicht pauschal gültig.
4. **\`CAPACITY_WEIGHTED_COMPOSITE\`**: aggregierte, schon in M0 bestehende Generatorgruppen mit **belegter** Erzeugungskapazität pro PECD-Profil; Summe der Gewichte 1.
5. **\`UNRESOLVED\`**: nichtzuordenbare oder mehrdeutige IDs/Geografie → **BLOCK**, kein unprotokollierter Nearest-Node.

Formale Mappingmatrix: \`A[g,p,h]\` über vorhandene Generator-ID \`g\`, Quellprofil-ID \`p\`, Zielhorizont \`h\`; nichtnegative, nachgewiesene Gewichte und \`sum_p A[g,p,h]=1\`. Für WS \`s\`, Stunde \`t\`:
\`CF[g,h,s,t] = sum_p A[g,p,h] * CF[p,h,s,t]\`;
\`P_avail[g,h,s,t] = p_nom[g] * CF[g,h,s,t]\`.
Bei einteiligen Anlagen ist genau ein Profil zugeordnet. Vorhandene M0 Generator-\`p_nom\` und \`bus\` werden nicht angepasst. \`p_max_pu\` ist **verfügbare Erzeugung, nicht Dispatch**.

**PV Normierungspflicht:** PECD \`MW/MWp\` vs. M0 \`p_nom\` meist \`MW_AC\`: Gate prüft, ob \`MWp\` DC-Leistung, \`MW\` AC-Ausgang, Standort/Wechselrichter, DC/AC-Verhältnis/Clipping/Ausrichtung bereits in PECD oder M0 enthalten sind. Ohne kompatible Basis **kein direktes p_max_pu-Writing** und keine unbelegte 1:1-Umrechnung.

### 4.3 Hydro, keine künstliche Stundenpräzision

- \`HRR\` = RoR; \`HPI\` = Pondage; \`HRI\` = Reservoir; \`HOL\` = offene Pumpspeicher; \`HCL\` = geschlossene Pumpspeicher (jeweilige Quellbedeutung im realen Datensatz prüfen). Vorhandene PyPSA-\`Generator\`, \`StorageUnit\` oder \`Store/Link\`-Modelle bestimmen erlaubten Zeitreihenzielpfad, nicht die freie Wahl des Adapters.
- Nur \`HRI/HPI/HOL\` entsprechend **als natürlicher Zufluss** belegte Quellprodukte an Speicherinflow. Ein geschlossener PS-Hydro-CF-/Betriebswert ist **nicht** ein natürliches Wasserzufluss-Signal.
- Quellwert \`E[zone,tech,interval,weather,horizon]\` MWh/Energieäquivalent. Energie-gewichteter Asset-Faktor \`B[asset,zone,tech]\` **belegt**; bei gleichmäßig im Intervall angesetztem Profil \`inflowMW(asset,t) = B*E / Δh_interval\`; danach \`Σ_t inflowMW*Δt = B*E\` für jeden ursprünglichen Quellinterval.
- Bei Teilwochen, Schaltjahr oder abweichender Quellintervalllänge die tatsächlichen Zeitintervallgrenzen verwenden; keine pauschal 53 vollständigen Wochen pro Jahr. Eine Annahme „konstante stündliche Leistung aus Wochenenergie“ ist eine **klar zu dokumentierende Disaggregation** und keine eigenständige meteorologische Stundenbeobachtung. Check Hydro-Konversion der Quellgröße in PyPSA \`inflow\`-Energie- und Wirkungsgradsemantik. Keine stillschweigende \`fillna(0)\`.
- Kein Nachbau von HydroBASINS/Runoff durch \`module_hydropower\` als **vermeintliche Original-PECD-Zeitreihe**; nur explizit genehmigte optionale Zusatzvalidierung.

### 4.4 Lasten / thermische Verfügbarkeit

Nur bei dokumentierter Source und M0-\`Load\`-/Generator-ID-Verbindung \`loads_t.p_set\` und thermische \`generators_t.p_max_pu\` hinzufügen. TYNDP-Demand-Zonenprofil an einen elektrischen Originalbus weiterzuschreiben ohne explizite Lastanteile ist genauso unbegründet wie beim Wind. Da vorhandene Lasten elektrisch angeschlossen sind, muss die zeitliche Skalierung aus Lastmengen/TSO-Splits hervorgehen. DFT ist eine separate Sourcefamilie, keine automatische Kopie eines Meteorologie-CF.

## 5. Zeitverträge und Core-Kompatibilität

**Pro \`(planning_horizon, weather_id)\` ein unvermischtes Zeitreihenpaket mit eigenem \`time\`-Index**, sowie ein vollständiges PyPSA-NetCDF-Netz pro benötigter Kombination als Übergabe. Gemeinsame unveränderte M0-Topologie kann zur Speicheroptimierung intern geteilt werden; der Endabgabe-Export bleibt vollständig.

\`time\` wird als absolute, exakt stündliche **UTC**-Zeitachse interpretiert; **PyPSA \`Network.set_snapshots\` weist timezone-aware \`DatetimeIndex\` derzeit ausdrücklich zurück**. Daher UTC vorab konvertieren, anschließend **timezone-naive UTC-stempel** an PyPSA übergeben, \`time_zone=UTC\` im Metadatenmanifest sichern. \`Date/Hour\` in PECD-CSV wird nur mit dokumentierter Stundenkonvention (\`Hour\` 1–24/0–23), DST-Handling und korrektem physikalischen Zeitraum übernommen. Nach \`set_snapshots\` vollständige Pflichtzeitreihen erneut prüfen; PyPSA kann beim Reindexing Defaultwerte ergänzen.

**Fünf Jahre nicht mit PyPSA-Stochastik verwechseln:** Core hat \`n.set_scenarios()\` und mehrstufige Indexmöglichkeiten, doch PyPSA v1.4.0/kommende Release Notes weisen auf **nicht unterstütztes LPF/AC-PF für stochastische Netze** hin. Für M1 ist die **separate Netzdatei je WS** deshalb eine bewusst robuste Anschlusslösung; spätere Investitionsstochastik ist nicht M1.

**Bewusst verboten:** Klimajahr-/Planungshorizont-Fallbacks, \`fill_gaps_method=zero\`/mean ohne genehmigten Sourceentscheid, Wechsel auf \`[0]\` erstes TYNDP-Wetterszenario, reduzierte repräsentative Stunden, stilles Abschneiden von PV-CF, Änderungen an bereits vorhandenen Betriebspunkt-\`p_set\`-Werten.

## 6. Verbindliche logische Datenverträge

### 6.1 M0_ReferencePackage v1 (externer Eingang, nicht in M1 neu erzeugt)

| Feld / Artefakt | Bindend | M1-Nutzung |
|---|---|---|
| \`network_revision_id\`, \`source_set_hash\`, \`mapping_policy_hash\` | Ja | unveränderliche Revisionsanker |
| \`pypsa_network\` | Ja | exakte Original-Bus-/Branch-/Generator-/Load-/Storage-IDs und statische Felder |
| \`m0_sidecar\` + \`identity_map\` | Ja | SourceAsset/Terminal/Location -> PyPSA-Komponente und Herkunft |
| \`location\`/\`CRS\`/\`quality_flag\` | wenn vorhanden | nur validierte reale Anlagenkoordinate oder explizit als Proxy qualifizierte Busgeometrie |
| \`component_support_matrix\` | Ja | unterstützt/approximiert/nicht unterstützt; Hydro-Modelldefinition |
| \`capability_report\` | Ja | \`PYPSA_ACPF/LPF\` und Studiensicht; kein abgeleiteter M2-Qualitäts-PASS |

**Hinweis:** Ein M0-Interface kann dokumentarisch existieren und gleichzeitig im Code fehlen. In diesem Audit sind M0-\`DetailedNetworkReference\`-Realdateien nicht gezeigt. Ein \`STATIC PASS\` beweist keinen CGMES-Importer.

### 6.2 PECD_SourceManifest v1 (quellenspezifisch)

\`source_dataset_id, provider, product_version, source_revision_date, file_sha256, license/access, planning_horizon, weather_id, climate_model_year, native_area_level, native_area_id, region_mask_id/CRS, technology_variant, variable_semantics, unit, timestamp_basis, interval_bounds, missing_policy\`.

\`native_area_level\` ist enumeriert: \`PEON/P2ON/PEOF/P2OF/ORIG/NUT2/SZON/TYNDP_NODE/OTHER_EXPLICIT\`; **keine automatische Austauschbarkeit**. \`TYNDP_NODE\` in Open-TYNDP-Dateien ist nicht \`CGMES_BUS\`.

### 6.3 Canonical M1 artefacts (versionierte, typisierte Schemas)

| Schema | Schlüssel | Pflichtfelder / Bedeutung |
|---|---|---|
| \`profile_catalog\` | \`(source_dataset_id, horizon, weather_id, profile_id, technology_variant)\` | \`native_area_level, native_area_id, unit, time_resolution, source_sha256\` |
| \`asset_profile_map\` | \`(network_revision_id, horizon, asset_id, profile_id)\` | \`pypsa_component_id, component_class, source_asset_id, bus_id, A_weight, assignment_method, geo_source, geo_quality, approval_ref\` |
| \`asset_hydro_map\` | \`(network_revision_id, horizon, hydro_asset_id, hydro_region, tech)\` | \`hydro_source_id, B_fraction, basin_evidence, destination_component, dimension_convention, loss/efficiency_policy\` |
| \`renewable_cf\` | \`(horizon, weather_id, time, generator_id)\` | normierte \`CF\` mit korrekter Nennleistungsbasis |
| \`hydro_inflow\` | \`(horizon, weather_id, time, destination_id)\` | \`inflow_MW\` nach nachvollziehbarer Energieumrechnung; Quellintervall-Ledger |
| \`load_p_set\` | \`(horizon, weather_id, time, existing_load_id)\` | nur bei autoritativer, vollständig gemappter Quelle |
| \`source_coverage_audit\` | \`(source_id, horizon, weather_id, technology, region)\` | Anzahl+MW der zugeordneten/ungeklärten Pflichtanlagen und Energievergleich |
| \`static_fingerprint\` | \`(network_revision_id, pypsa_version, m0_policy_hash)\` | sha256/canonical serialized static tables + IDs/Busverbindung; vor/nach M1 identisch |
| \`QA_EVIDENCE\` | \`(run_id, gate_id)\` | \`PASS/FAIL/BLOCKED/NOT_ASSESSED\`, source refs, tolerances, exception refs |

**Im PyPSA-Schreibadapter**: nur bekannte Attribute, e.g. \`generators_t.p_max_pu\`, \`storage_units_t.inflow\`, \`loads_t.p_set\`. Bei Store/Link-basiertem Hydro-Modell ist vor der Schreiboperation die exakte zuflusskompatible Schnittstelle mit M0 festzulegen; nicht jede \`Store\`-Komponente besitzt ein direktes \`inflow\`-Attribut.

**Dateiformate:** xarray/NetCDF oder Zarr für große time×asset Arrays; Parquet/CSV für IDs und Tabellen; feste Namen pro \`(horizon,weather_id)\`; keine in der Architektur versteckte Komponentenneuanlage. Runtimeseitige Memory-/Skalierbarkeit bleibt ungetestet.

## 7. Gates und Akzeptanzentscheidung für MA-1

| Gate | Prüfobjekt | Ergebnis dieser Ausführung |
|---|---|---|
| **G1-A UPSTREAM STATIC REUSE** | Nachweis der relevanten Master-/Feature-Branches, konkreter PECD-4.2-Reader, Hydro-Skripte, Grenzen | **PASS (STATIC)** |
| **G1-B SOFTWARE ARCH CONTRACT** | Projektgrenzen, M0/M1/M2, Schreib-Whitelist, Profil- und Quellidentität, Zeit-/Räumlichkeitssemantik | **PASS (DESIGN)** |
| **G1-C M0 REAL FILE CONTRACT** | echte \`DetailedNetworkReference v1\` inklusive Sidecar, Quell-/Bus-/Geo-IDs, Klassen, Version und Fingerprints | **NOT_ASSESSED / BLOCKED: M0 noch Design** |
| **G1-D PECD REAL SOURCE CONTRACT** | physische PECD-v4.2-Dateien, reale fünf WS-IDs, region masks, source hashes & genaue Spalten/Dimensions/Zeiten | **NOT_ASSESSED / BLOCKED: reale Quelldateien/WS-IDs fehlen** |
| **G1-E HYDRO REAL SOURCE CONTRACT** | Hydro-Rohwerte, Source-Intervallgrenzen, SZON/Nodes, Anlagentyp und belegbare regionale Verteilfaktoren | **NOT_ASSESSED / BLOCKED** |
| **G1-F PYPSA RUN COMPATIBILITY** | tatsächlich importierte Daten, \`set_snapshots\`, 5 WS, nicht-mutierender Composer, NetCDF-roundtrip | **NOT_EXECUTED** |

**Governance-Ergebnis:** \`M1-MA1-STATIC-COMPLETE_CONTRACT-CONDITIONALLY-FROZEN_DATA-WITNESSES-BLOCKED\`. Die **Kernarchitektur ist als Baseline eingefroren**, aber kein vollständiges \`M1-SPATIAL-SOURCE-CONTRACT-FROZEN\`/Implementierungsgate. MA-2/MA-3 dürfen **nur vorbereitende Fixture-/Quellcodeadapter-Entwicklung** ohne Produktivdaten-PASS beginnen, bis G1-C/D/E anhand realer Dateien und M0-Revision erfüllt sind. Kein micro-loop: Owner liefert **ein gebündeltes Datenpaket**.

### 7.1 Minimaler gebündelter Data-Witness zur harten Freigabe

1. **M0-Package-Witness:** ein revisionsgebundenes \`DetailedNetworkReference v1\` mit \`pypsa_network\`, \`m0_sidecar\`, \`identity_map\`, repräsentativem onshore-/offshore-PV/Wind-/Hydro-/Load-Asset, Beispiel-CRS und tatsächlich unterstütztem Hydro-PyPSA-Modell; bei späterer voller Real-Netzlieferung kompletter Check.
2. **Fünf-WS-Witness:** die **bereits beschlossenen fünf Quellkennungen**, ihre Zielhorizonte und je ein File Header/Manifest (inkl. Wetter, hydro, optional DFT) pro erforderlicher Source-/Technologieklasse, inklusive Source-Dateihash. Keine Neuauswahl erforderlich.
3. **Räumlicher Witness:** offizielle Regionsmasken/Polygone/Rastermetadaten und Quell-PECD-Profilschlüssel; eine stichprobenartige reale \`source_asset ↔ profile\`-Zuordnung pro Raumfall (Onshore, Offshore, PV Raster/Region, Grenzfall).
4. **Hydro-Witness:** mindestens je ein originärer Hydro-Zuflussdatensatz mit Einheit/Intervall und eine nachvollziehbare Verteilung zu den realen Hydro-Assets (Basin/TSO/Quellallocation); Einheiten und Zustand geprüft.
5. **Versionsledger:** PECD pre-built vs korrigierte Szenarioinputs eindeutig und lizenziert, PyPSA/Python/Snakemake-Versionpin; keine gemischten Releases ohne belegte Kompatibilität.

Bis zum Eingang dieser Zeugen ist keine Aussage zulässig, alle fünf Datensätze ließen sich schon knotenscharf und vollständig aus dem genannten Open-TYNDP-Bundle abbilden.

## 8. Fixierte Negativ-/Positive Testmatrix zur späteren Ausführung

- Gültige onshore-Anlage: M0-Generator-ID, belegtes PEON/P2ON-Profil; statisches \`p_nom\` und \`bus\` unverändert.
- Zwei Generatoren in einer PEON-Zone: gleiche CF-Zeitreihe, **zwei elektrische Anschlüsse**.
- PV-ORIG-raster vs regionales PV: als unterschiedliche Quellauflösung gekennzeichnet; keine künstliche Interpolation zur Verfeinerung.
- PV-DC-MWp vs AC-MW: ohne freigegebene Transformation **BLOCK**.
- Offshore-Asset mit landseitigem Bus: validierter Offshore-Orts-/Region-Identifier, sonst BLOCK.
- Synthetischer 3W-Star-Bus aus M0: nie als Erzeugungsstandort, kein weather matching.
- Kombinierter Generator über Regionengrenze: belegte Kapazitätsanteile, Summe A=1; andernfalls BLOCK.
- Hydro HRR/HRI/HPI/HOL/HCL: Typ-/Zielkomponentenmatrix; eigenständige Intervallenergie-Prüfung inkl. Teilintervalle.
- DFT 3 gefüllte vs 5 verlangte WS: keine künstliche Ergänzung; **fail closed**.
- Fehlen von Quelle/Region/Wetterjahr: keine Null-/Mean-/Fallback-Profile, Block mit Ledger.
- UTC und Leap/DST: vollständige Zeitausdehnung; Profilkonsistenz nach PyPSA-Reindex.
- Grenzüberschreitende physische Netzzweige und alle M0-Originalkomponenten statisch identisch; keine Clusterung.
- Roundtrip/Hash- und Memory-Test über fünf real gelieferte Sets; Status derzeit **NOT_EXECUTED**.
- Optional physikalischer LPF/AC-PF nur bei **separat bilanziertem** Betriebspunkt; PECD-CF alleine ist kein gültiger Lastflussdispatch.

**Keine Erfundenen Grenzwerte:** Für floats Prüftoleranzen nach source-precision und Netto-Speicherung als gesonderten numerischen QA-Contract pinnen; Identität von Asset-IDs/Knoten/Zeitschritten ist strikt.

## 9. Präziser Übergang zu konsolidierten Implementierungsmakros

**Makro MA-1 (hier):** Vollständige statische Branch-/Source-Architekturprüfung, Baseline-/Contractvorschlag und gebündeltes Data-Witness-Gate. **Abgeschlossen mit qualifizierter Sperre**, nicht als Real-Daten-PASS.

**Makro MA-2: PECD RES Adapter + spatial mapping (ein Auftrag)**  
Nach harten G1-C/D: Source-PECD v4.2 Reader basierend auf \`tyndp-2026\` adaptieren; 5-WS-Quelle explicit, exakte Profil-/Tech-ID, Punkt-/Masken- bzw. verifiziertes Composite-Mapping an existierende Generator-IDs, Normierung, Fixtures, Integritätsledger; inklusive G2 in einer Lieferung. Ohne reale Daten nur Fixture-Scaffold, kein Produktions-PASS.

**Makro MA-3: Hydro Source + Basin Inflow (parallel ein Auftrag)**  
Nach harten G1-C/E: PECD-v4.2-/TYNDP-Hydro-Reader adaptieren, Source-Region->hydro asset/Speichermodell, Intervallmengen, Tages-/Wochentemporalität, Wirkungsgrad-/Einheitenvertrag, 5-WS-Quellen, Fixtures; inklusive G3 in einer Lieferung. Modellblocks als nur genehmigte zusätzliche Diagnose, nicht Ersatz.

**Makro MA-4: Non-mutating PyPSA Composer + E2E unabhängiger Qualifikation (ein Auftrag)**  
Nach G2/G3: gemeinsamer statischer Fingerprint, Generation/Load/Hydro-Profile, pro Szenario vollständiges PyPSA-NetCDF, Source-Mapping-/Energy-Coverage, alle 5 WS, NetCDF-roundtrip, unabhängiger QA, M2-Handoff. Keine M2-PTDF-/Clustering-Aufgaben.

**Parallelisierung:** MA-2/MA-3 nach denselben physisch qualifizierten MA1-Schemas parallel; M0-Implementierung unter eigenem Owner. MA4 erst nach beiden. Diese vier Makros sind vollständig, keine separate Mikroiteration nach Anlagentyp/Wetterdatensatz.

## 10. Revisionssichere Schlussentscheidung

- **Statisch nachgewiesen:** PyPSA-Core benötigt keinen neuen Wetterparameter; Open-TYNDP 2026 bietet PECD-v4.2-Parser/Snakemake/Hydro/Tech-Mapping; die volle Stochastik ist **nicht** Voraussetzung der knotenscharfen Zeitreihenintegration.
- **Nicht nachgewiesen:** exakte PECD-Profilabdeckung für das **externe Fünfer-Wetterset**; M0-Originalnetz/Geometrie tatsächlich produziert; Einheiten-/Anlagenmappings an realen Daten; Hydro-Basin-Anteile; End-to-End-Integration/Performance.
- **Hard-Freeze-Empfehlung:** Reuse- und Architektur-Baseline **jetzt freigegeben zur weiteren Entwicklung**; eine **vollständige Quellen-/Datenschemafreigabe für produktive Umsetzung** bleibt **BLOCKED** bis die Witnesses aus Abschnitt 7.1 zusammen vorliegen. Kein Wechsel der fünf Datenjahre und keine unprotokollierte Approximation.

**Dokumentstatus:** \`MA1_STATIC_PASS__DATA_FREEZE_CONDITIONAL\`, strikt unterschieden von \`MA1_FULL_DATA_PASS\`. Das bestehende [M1 Raumauflösungsdokument](IOSN_M1_SPATIAL_RESOLUTION_AND_MACRO_EXECUTION_PLAN_2026_11_01.md) wird inhaltlich mit dieser MA1-Entscheidung **präzisiert** (insb. Open-TYNDP-2026, M0-Sidecar, 3-vs.-5-WS, PyPSA-Szenario-/Zeitachse); keine alten Quellen verändert.
