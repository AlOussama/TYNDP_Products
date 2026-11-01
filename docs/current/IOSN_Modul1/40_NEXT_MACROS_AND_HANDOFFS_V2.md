# S-GOV-M1 V2 — Nächste konsolidierte Makro-Aufträge / copy-ready Worker-Handoffs

**Datum:** 2026-11-01  
**Status:** `MACRO_HANDOFFS_PREPARED / OWNER_DISPATCH_PENDING`  
**Vorrang:** [00 kanonische Architektur](00_CANONICAL_ARCHITECTURE_V2.md) → [10 Reuse-Ledger](10_UPSTREAM_REUSE_LEDGER_V2.md) → [20 Interfaces](20_SOURCE_SPATIAL_COMPONENT_CONTRACT_V2.md) → [30 QA/Gates](30_WORKFLOW_AND_QUALIFICATION_V2.md). Die älteren MA-1-/MA-2-/MA-3-/MA4F-Handoffs bleiben historische **Abschluss-/Evidenzdokumente**, kein Neubeauftragungsbedarf.

## 1. Ausgangsstand und Entscheidungen

**Bereits geliefert, nicht erneut entwickeln:**
- MA2 `11700baa8df8cafc6bd71b96998f8b2bca647ca0` (regional CSV PECD reader, geografische Mapping-Validierung, 20 lokale synthetische Tests);
- MA3 `b3b9bf133d1b5c968323a31f8ac76090f1f2e182` (Hydro energy adapter, 62 Gesamttests im CI-Scope);
- MA4F `1ab3eb1aed54975e69586cc3d958a24d97a6288f` (getesteter SHA `cd71f36ddf07fb3ecc1cb4be5701a2586b9950c8`; **92 Tests, 16 Snakemake-Jobs, fünf synthetische NetCDF, 16 statische Netztabellen gleich**); [MA4F-Handoff](https://github.com/AlOussama/TYNDP_Products/blob/1ab3eb1aed54975e69586cc3d958a24d97a6288f/docs/current/IOSN_Modul1/MA4F/HANDOFF_MA4R.md).
- MD1 `5c68198984b6f2f430a49ff3e23d17c0b27320e1`: unabhängiger Source-/M0-/Join-Vertrag, **physische PECD/Hydro/M0-Daten blockiert**, 0/5 reale Projekt-IDs bestätigt. [MD1-Releaseentscheid](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/MA4R_RELEASE_DECISION.md).
- M0 Owner: Netzimport-CAN/2.0.0/DNR/1.0.0 als **eigene** separate Workstream; bis jetzt dokumentarische Architektur, kein physischer qualifizierter Detailnetzimport. M0 **darf nicht** mit PECD-Reader/Mask-/Demand- oder Basin-Mapping beauftragt werden.

**Fehlende Funktionen (gegenüber hochaufgelöstem nativen PECD-Standard):** (1) native griddierte PECD-SPV-`ORIG`-NetCDF; (2) native ECMWF fraktionale Regionsmasken-NetCDF; (3) **automatisch** generiertes Source-zu-bestehender-Generator Spatial Mapping statt ausschließlich MA2-Mappingtabellenvalidierung; (4) optional verpflichtender DFT/Load-zu-bestehenden-Load-ID-Adapter; (5) echte unveränderte fünf Weather-IDs und physische Sources/M0-Package fehlen.

## 2. Freigabe- und Parallelisierungsentscheidung

| Makro | Verantwortlichkeit | Start | Gate / Ergebnis |
|---|---|---|---|
| **M1-MA5N** Native PECD + Auto Spatial Matching + bestehender Composer | eigener **M1 Python-/Spatial-/PyPSA-Implementierungschat** | **SOFORT**, auf getestetem MA4F-Code-Branch | \`M1_NATIVE_PECD_AUTOJOIN_FIXTURE_QUALIFIED\` oder ein konsolidierter FIX-/BLOCKED-Bericht, kein Real-PASS |
| **M1-MA5D** DFT Demand→bestehende Load-IDs | eigener **Demand-/PyPSA-Eur-Expertenchat**, unabhängig von MA5N | **PARALLEL**, falls Lastzuordnung von M1 erforderlich; mit synthetischen Demandfixtures ohne echte DFT-Daten | \`M1_DEMAND_EXISTING_LOAD_FIXTURE_QUALIFIED\` oder begrenzter BLOCK |
| **M1-MD2** Physische native PECD-/Hydro-/DFT-Source-Beschaffung und Qualifikation | **Data Owner / Source-Auditor**, getrennt vom M0-Owner | **PARALLEL zu MA5N und MA5D** | getrennte Source-Gates \`S-PECD\`, \`S-HYDRO\`, \`S-DEMAND\`, klare 5-WS-Ledger; **keine** Netzabhängigkeit |
| **M0-owner** Originalnetz/PyPSA-Import | **separater M0-Entwicklungs-/Governancechat**, nicht M1 | unabhängig | \`N-M0-PHYSICAL\` plus eigenes Original-IDs-/Geo-/Portpaket |
| **M1-MA6** gesamte reale M1-Integration | eigener Integrations-/Ausführungschat, startend von MA5N+MA5D | **NACH** echten Source-/Netz-Gates und Fixture-PASS | \`M1_REAL_REFERENCE_READY_FOR_INDEPENDENT_REVIEW\` |
| **R-M1-MA6** unabhängiger Review / S-GOV Release | unabhängiger Reviewer, danach **dieser Governancechat** | nach MA6 realem Ergebnis | \`M1_DETAILED_REFERENCE_READY_FOR_M2\` oder fundierter Blocker |

**Keine unnötigen Mikroschleifen:** MA5N ist **ein einziges** umfassendes Implementierungs- und Regressionstestmakro; MA5D ein kompletter optionaler Adapter samt Tests; MD2 **ein** tatsächlicher Quellenbeschaffungs-/Qualifikationsauftrag. Erst nach ihnen ein kombinierter MA6-Real-Lauf und ein unabhängiger Reviewer. Die bereits qualifizierten MA4F-Fixtures werden **nicht** als ungültig erklärt, sie sind die Baseline.

## 3. M1-MA5N — Native PECD-ORIG & Fractional-Mask Reader + Automatic Spatial Profile Mapping (SOFORT)

**Rolle:** erfahrener Python/xarray/Dask/GeoPandas/Atlite/PyPSA-Eur-Softwarearchitekt und Implementierer für PECD v4.2 und original-asset spatial joins.

**Verbindliche erste Handlung:** GitHub-Ausgangscommits `MA4F 1ab3eb1aed54975e69586cc3d958a24d97a6288f`, `MA2 11700baa8df8cafc6bd71b96998f8b2bca647ca0`, `MA3 b3b9bf133d1b5c968323a31f8ac76090f1f2e182` und [vorhandenes MA4F-Ausführungsreport](https://github.com/AlOussama/TYNDP_Products/blob/1ab3eb1aed54975e69586cc3d958a24d97a6288f/docs/current/IOSN_Modul1/MA4F/EXECUTION_REPORT.md) vollständig verifizieren. Die V2-Architektur `00/10/20/30` vollständig lesen. Externes PyPSA-Eur `1526bb82`, Atlite `0d4ff8`, Open-TYNDP `71a3a9a` und offizielles PECD4.2-PUG Tab. 3.6/4.2/4.3 als Source-Pins prüfen.

**Arbeitsbranch:** `impl/iosn-m1-ma5n-native-pecd-spatial-20261101` **vom getesteten MA4F-Branch-HEAD**; die V2-Docs als immutable externe Autorität referenzieren statt ungeprüft Worker-/S-GOV-Branchhistorien zusammenzufügen. MA4F-Originalcode, MA2/MA3-Parser, Hydro und 16-statischer-Tabellen-Gate möglichst unverändert lassen.

**Kompletter Makro-Scope:**
1. Echte PECD-Produktvarianten differenzieren: WON/WOF **regionale** CF `PEON/P2ON/PEOF/P2OF` (Wind-Technologie/ReGrA/B) und SPV **ORIG 0,25° griddierte NetCDF-Kapazitätsfaktoren** (MW/MWp, vier PV-Typologien), plus optionale regionale PV-CF. Das meteorologische Raster darf **nicht** als offiziell griddierte Wind-CF ausgeben werden.
2. **Native xarray-NetCDF Source-Reader** für SPV `ORIG` inkl. echter Header-/Dimension-/CRS-/Vartype-/Szenario-/Timing-Schema-Ableitung, Lazy-Grid-Windowing und Source-Byte-/SHA256-/License-Gates; im Source-abwesenden Modus testbarer Reader mit **synthetischen** PECD-PUG-konformen NetCDF-Fixtures und eindeutiger \`FIXTURE\`-Klassifikation.
3. **Native fractional NetCDF Mask-Reader** für PEON/P2ON/PEOF/P2OF/SZON (und bei Bedarf NUT2), offizielle `mask(region,latitude,longitude)`, Region- und Versionregister, Grenzzellen-/Mehrdeutigkeits-Policy, CRS/Lat-Lon-Flip. **Keine** unbelegte Shapefile-/GeoJSON-Zertifizierung und keine Gleichsetzung von Flächenanteil und Kraftwerks-MWp.
4. **Automatische originale Asset-Zuordnung** aus `existing_generator_id / carrier / technology / bus / approved plant_location / optional qualified bus proxy` und Source Grid/Zones. Hier generierte `asset_profile_map_v2` an den bereits existierenden **MA2-Validator** geben; zusätzliche Geo-/Negative-Tests für mehrere Generatoren mit einem regionalen Wind-CF, verschiedene PV-Rasterzellen, Offshore-Landfall, synthetische Sternbusse, Multi-Region-Capacity-Weights, technische Unterschiede und PV-MWp↔MW_AC.
5. Quellgestreute, explizite `weather_id` über fünf vorgesehene IDs; Source-Datei-/Masken-/Planjahr-/Version-Gates und keine stillen 3→5-/0-/mean-/nearest-centroid-Fallbacks.
6. **Nur vorhandenen MA4F-Composer erweitern**, keine zweite Output-Pipeline. Neue nativen Parser-/Mapper-Outputs in `rules/iosn_m1_res.smk` oder ergänzende Rule-Datei einhängen; Snakemake-NetCDF, genaue Original-IDs, unveränderte elektrische Netzstatik (16/16), Hydro-Regression, PV-/Wind-/Zeitzonenchecks, 5× synthetische NetCDF-Roundtrips und unabhängiger QA-Report. MA2/MA3 und bislang 92 PASS müssen im kombinierten Test weiterhin bestehen.
7. Der neue Reader muss bestehende regionale Sourceformate weiterhin unterstützen. Kein Upstream-PyPSA-Core-/PyPSA-Eur-Patch, kein neues Netzmodell, keine Wetterneuwahl, keine neue Wind-Simulation, keine Netzaggregation. Echte Sourcequalifikation gesondert MD2.

**Abgabe:** neuer `scripts/iosn_m1/res/native_grid.py`, `native_masks.py`, `auto_spatial_mapping.py` (Namen durch Projektkonvention anpassbar), aktualisierte Source-/GIS-Schemas, neue/erweiterte Snakemake-Regeln, Tests mit NetCDF/Masken-/Boundary-/Offshore-/Grid-Negativfällen, vollständiger kombinierten CI-Lauf, `docs/current/IOSN_Modul1/MA5N/EXECUTION_REPORT.md`, `SOURCE_PRODUCT_COVERAGE.md`, `INTEGRATION_DELTA_LEDGER.md`, `HANDOFF_MA6.md`; Commit/PR.

**PASS nur Fixture:** `M1_NATIVE_PECD_AUTOJOIN_FIXTURE_QUALIFIED` mit tatsächlichem kombinierten Testwitness und unveränderten Baseline-Pflichten. Ohne originale ORIG-Datei/-Masken **kein** `NATIVE_ORIG_REAL_DATA_PASS`.

## 4. M1-MA5D — Demand / DFT Source-to-Existing-Load Adapter (PARALLEL, WENN LAST-SCOPE PFLICHT)

**Rolle:** Demand Forecast/ENTSO-E TYNDP/DFT, PyPSA-Eur Demand Spatial Disaggregation, Python xarray/Snakemake.

**Auftrag:** In **einem** Makro vorhandene PyPSA-Eur-Quelle `scripts/build_electricity_demand_base.py` und Open-TYNDP `scripts/sb/build_tyndp_demand.py` lesen; tatsächliche Quellversion des verbindlichen Demand-/DFT-Produkts dokumentieren. Entwickle **nur bei erforderlicher Lastzeitreihenverteilung** einen eigenständigen Datenadapter `regional/country MW(time,weather,horizon) → existing Load IDs`. Verwende geprüfte Source-/TSO-/POP-/GDP-/Zählerinformationen als qualifizierte, versionierte Verteilgewichte; `sum_load p_set_MW(t)=source_region_demand_MW(t)` und doppelte Lastzählung/fehlenden \`weather_id\` blockieren.

**Unveränderlich:** `n.loads.index`, `n.loads.bus`, elektrische Anschluss-/Stammdaten, regionale Quelle, 5 Weather IDs. Wenn M0 ein bereits fachlich akzeptiertes `loads_t.p_set` mitgibt, dessen Werte **nicht** ohne Source-/Owner-Genehmigung überschreiben. Keine Last aus bloßem PECD-Wind/PV rekonstruieren; DFT unabhängige Source. Kein Clustering und keine eigene Netzsimulation.

**Integrationsvertrag:** `load_p_set(time,existing_load_id)` + Source-/Distribution-/Time-/Overwrite-Ledger mit erlaubtem Writer `MA4F.compose`; **MA5D ändert nicht gleichzeitig Composer-/MA5N-Dateien**, um Race-/Mergekonflikte zu vermeiden. Nur eigene `scripts/iosn_m1/demand/`, `rules/iosn_m1_demand.smk`, Schema und Tests mit synthetischen positiven/negativen echten Lastprofilformat-Beispielen.

**Abgabe:** vollständiger Code, autonomes Fixture-QA, \`M1_DEMAND_EXISTING_LOAD_FIXTURE_QUALIFIED\` oder bedingter \`NOT_NEEDED_EXISTING_LOADS_ALREADY_QUALIFIED\`-Review mit Original-/Quellbelegen, `HANDOFF_MA6.md`; keine Real-WS-PASS-Behauptung.

## 5. M1-MD2 — Physical Native PECD / Hydro / DFT Source Evidence (PARALLEL OHNE NETZABHÄNGIGKEIT)

**Rolle:** Data Owner/CDS- und ENTSO-E-TYNDP-Daten-/Source-Auditor, mit gesichertem Zugang zu Originaldateien. **Nicht erneut** allgemeinen MD1-Bericht umformulieren.

**Ausgangsbasis:** [MD1 @ 5c681989](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/EXECUTION_REPORT.md), [MD1 Blockerregister](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/BLOCKER_REGISTER.csv), 00/10/20/30 V2.

**Einmaliger konsolidierter physischer Auftrag:**
1. Die **bereits festgelegten fünf** \`weather_id\`, Klima-/Horizon-/Source-References **aus der autoritativen Nutzer-/Data-Owner-Quelle** beibringen, ohne neue Auswahl. Alle erforderlichen Originärfiles, Release/Korrektur, Lizenzen und SHA256 sowie Full-Year-Stunden prüfen.
2. Physische PECD-v4.2-WON/WOF-regionalen CF und **falls ausgewählt/erforderlich griddiertes SPV-ORIG-NetCDF** plus offizielle `ANCI_PEON/P2ON/PEOF/P2OF`-/SZON-Masken-Bytes, File-/Variable-/Dimension-/Coord-/Tech-/Unit-/Grid-Witness sichern. Externe ZIP-/CDS-Datensätze nur bei belegter Zugangs-/Verwendungsberechtigung nutzen.
3. Physische Hydro-SZON-/DAY-/WEEK-Intervall-/MWh-/Technologie- und TSO-/Basin-Herkunft; jeweils natürliche Energie/Erzeugungsenergie unterscheiden. DFT-Lastsource nur wenn Pflichtumfang, auch dort fünf WS und regionales MW.
4. Für das spätere reale Join-Paket getrennt aufzubewahren: offizielle PECD-Georegionen/CRS, ggf. Anlagendatenbank-Standorte, Offshore-Parkkoordinaten, PV-DC/AC-Einheiten, Hydro-Basin-zu-Kraftwerk-Witness und TSO-/Load-Anteile; **keine M0-PECD-Implementierungsaufgabe** ableiten.
5. Maschinell lesbarer Source-PASS/BLOCKED je \`(weather_id,horizon,technology,source_file)\`, inklusive echte Header, SHA/Release und Nutzerrechte. Kein \`TYNDP-WS03\` als Ersatz einer unbekannten Projekt-ID.

**Trennung von M0:** Dieser Auftrag kann `S-PECD-PHYSICAL / S-HYDRO-PHYSICAL / S-DEMAND-PHYSICAL` **unabhängig** freigeben, ohne M0-Netz. **M0-Owner** liefert eigenes späteres `N-M0-PHYSICAL`. Join-/AC-PF-/NetCDF-Gesamt-PASS liegt **nicht** bei MD2.

**Abgabe:** \`SOURCE_BYTES_AND_SCHEMA_WITNESS.md\`, \`FIVE_IDS_RELEASE.csv\`, \`PECD_NATIVE_NETCDF_AND_MASK_LEDGER.csv\`, \`HYDRO_SOURCE_LEDGER.csv\`, \`DEMAND_SOURCE_LEDGER.csv\`, \`LICENSE_SHA256_MANIFEST.csv\`, \`GATE_DECISION.md\`, \`HANDOFF_MA6.md\`; kontrollierte Raw-Datenablage außerhalb des öffentlichen Repositories falls Datenrechte dies verlangen.

## 6. M1-MA6 — Complete Real Five-Weather Reference Composer and Qualification (NACH GATES)

**Owner:** eigenständiger PyPSA-/Snakemake-M1-Integrationschat. Keine Startfreigabe mit nur fiktiven Wetterdaten. Eingang: geprüfter MA5N-Commit + ggf. MA5D + MD2 echter Source-Byte-PASS + **separat qualifizierter Netzimport** (vom M0 Owner oder zulässiger alternativer Netzquelle).

**Ausführung als EIN Makro:**
- ggf. geprüften Demand-Adapter integrieren; bestehende Source- und Hydrologiedateien mit fixen M0-Original-IDs durch den nun nativen auto spatial join auf die **vorhandenen** Generatoren/Loads/Hydroports übertragen.
- Für alle fünf festgelegten Weather IDs und erforderlichen Horizonte exakte stündliche Zeitreihen exportieren; tatsächlich native PECD-Raster-/Regionenauflösung auslesen, nicht überhöhtes Weather-Detail behaupten.
- Source-/Anlagenverfügbarkeit pro MW/Technik/Region, PV-MWp→MW_AC, Offshore, Source-NetCDF/mask geometry, hydro source-to-model-MWh, Demand-MW, 16-statische-PyPSA-Tabellen, ursprüngliche Komponenten, NetCDF reimport und gezielte negative Fälle prüfen; Speicher-/Laufzeit-/Dateigrößen mit echten Daten berichten.
- Exakte Qualifikationsklasse \`M1_REAL_REFERENCE_READY_FOR_INDEPENDENT_REVIEW\` nur bei positivem physischem Source-, Netz-, Join- und Output-PASS; ansonsten \`BLOCKED_WITH_CONSOLIDATED_FINDINGS\` ohne neue Wetterwahl oder nachträglich erfundene Source-IDs.
- Ein abschließender **unabhängiger R-M1-MA6-Reviewer** erhält den gefrorenen MA6-Commit, Source-/QA-Reports und Originalnetzwitness. Erst S-GOV kann nach Reviewer-PASS die M2-Übergabe freigeben.

**Pflichtabgabe:** komplett reproduzierbarer volljähriger Source-/Netz-Workflow, \`detailed_reference_{horizon}_{weather_id}.nc\` für alle tatsächlich vorgeschriebenen Kombinationen, Source-/Spatial-/Hydro-/Demand-/Static-/Target-Ownership-Reports, QA JSON/JUnit, \`M1_TO_M2_HANDOFF.md\` nur bei erreichten Gates, Reviewer-Handoff/Abnahme.

## 7. Kurztexte zum Copy/Paste an die jeweiligen Arbeiter

**MA5N (SOFORT):**  
> Übernimm den gesamten Auftrag `M1-MA5N` aus §3 dieses Dokuments. Verifiziere die S-GOV-V2-Architektur und den bereits erfolgreichen MA4F-Implementierungscommit; ergänze **in einem einzigen Makro** native PECD-SPV-ORIG-NetCDF-Leseunterstützung, native offizielle PECD-Regionsmasken-NetCDF, **automatisches** Profil-zu-bestehender-Generator-Mapping und die minimale bestehende MA4F-Snakemake-Integration. Reuse statt Neuschreibung, keine PyPSA-Core-/M0-Codeänderung. Führe die Gesamt- und Negativtestkampagne aus, veröffentliche isolierten Branch + Commit + PR + Bericht. Bei fehlenden realen Daten ein ehrlicher Fixture-PASS, nie Real-Daten-PASS.

**MA5D (PARALLEL, falls regionale Lasten zu verteilen):**  
> Übernimm den gesamten Auftrag `M1-MA5D` aus §4. Verifiziere PyPSA-Eur Demand Disaggregation und Open-TYNDP DFT/TYNDP-Reader. Entwickle einen eigenständigen Input-/Mappingadapter, der echte/regional definierte Load-MW nur auf **bestehende** PyPSA-Load-IDs verteilt, mit kompletter MW-Bilanz und 5-WS-Gates. Arbeite auf eigenem Branch und **ändere nicht** den MA5N-/MA4F-Composer. Liefere Code, Fixture-Tests und MA6-Handoff in einem Makro. Real-Daten nur mit echten Sources deklarieren.

**MD2 (PARALLEL):**  
> Übernimm den gesamten physischen Source-Witness-Auftrag `M1-MD2` aus §5. Beschaffe/verifiziere die **fünf bereits fixierten** Weather IDs, echte PECD-4.2-CSV/ORIG-PV-NetCDF/Regionmasken-Dateien, Hydro-MWh-/Intervalldaten und ggf. DFT-Dateien, mit Hash/Release/Lizenz/Schlüsseln/Grids. **PECD-Source-QA ist unabhängig von M0/CGMES.** Keine M0- oder Mapperimplementierung, keine neue Wetterjahresauswahl. Ein konsolidiertes Source-Gates-/Blocker-Paket und MA6-Handoff auf eigenem Branch.

**MA6 (SPÄTER NACH GATES):**  
> Führe §6 als **ein** reales Integration-/Abnahmemakro aus, ausschließlich nach MA5N/MA5D Fixture-Gates, MD2 physisch qualifizierten echten Quellen und separater qualifizierter Netzimportlieferung. Erzeuge die realen fünf PyPSA-Detailreferenznetze, verifiziere Source-/Spatial-/Hydro-/Demand-/Originalnetz-Invarianz und gib einen gefrorenen Producer-Commit an unabhängigen Reviewer. Kein vorgezogener M2-Release.

## 8. Konflikt- und Governance-Regeln

- Jedes Makro startet mit vollständigem Lesen der unveränderlichen V2-Architecture/Contracts und der für seine Rolle maßgeblichen originalen MA4F/MD1-Belege.
- **Inkompatible Parallelwrites vermeiden:** MA5N führt MA4F-Code, MA5D schreibt ausschließlich seinen Demand-Adapter, MD2 nur Source-Evidence; Integration allein MA6. Keine Änderungen an M0-/M2-Code durch M1-Worker.
- **Kein Markieren eines Realdaten-Gates als PASS** anhand synthetischer Dateien, statischer README/CSV-Header oder netzunabhängiger Quellkataloge. Ausnahme-/N/A-Fälle explizit quellenbezogen benennen.
- Neue S-GOV-Entscheidung nach den drei parallelen Rückläufen; **kein** wiederholter allgemeiner Architekturvergleich und **keine** Mikro-Aufträge je Weather-ID/Tech/Knoten.
