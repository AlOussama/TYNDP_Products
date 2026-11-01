# IOSN / TYNDP — Modul 1: Nächste Makroaufträge nach MA-1

**Datum:** 2026-11-01  
**Status:** GOVERNANCE MACRO ASSIGNMENTS READY FOR OWNER DISPATCH — kein Codeauftrag allein durch dieses Dokument  
**Repository:** `AlOussama/TYNDP_Products`  
**Fachliche Basis:** 
- [MA-1 geprüfter Source-/Branch-/Geokontrakt](IOSN_M1_MA1_CONSOLIDATED_SOURCE_SPATIAL_CONTRACT_AUDIT_2026_11_01.md)
- [MA-1 logischer Datenvertrag](IOSN_M1_MA1_LOGICAL_DATA_CONTRACT_2026_11_01.yaml)
- [M1 Basisarchitektur](IOSN_M1_PECD_PYPSA_REFERENCE_TIMESERIES_ARCHITECTURE_2026_10_30.md)
- [M1 räumlicher Makroplan](IOSN_M1_SPATIAL_RESOLUTION_AND_MACRO_EXECUTION_PLAN_2026_11_01.md)
- **M0 normative DetailedNetworkReference v1:** `AlOussama/TYNDP_Products`, Commit `0275f48231a0794bea324b9cab34700bb0de8f5b`, `docs/current/IOSN_Modul0_CGMES/{30,40,60,70}`.

**Zentrale Entscheidung:** MA-1 ist **statisch abgeschlossen**, aber kein Real-Data-Freeze: `MA1_STATIC_PASS__DATA_FREEZE_CONDITIONAL`. Vier nachfolgende, **gebündelte** Aufträge — davon drei parallel startbare Arbeitsstränge mit unterschiedlichem Gatesystem — und eine nachgelagerte Gesamtqualifikation. **M0, M1 und M2 sind unterschiedliche Projektmodule;** das M0-Architektur-M2 darf nicht mit der IoSN-Netzaggregation (Projekt-Modul 2) verwechselt werden.

## 1. Entscheidung: Zeitliche Reihenfolge und Gates

| Auftrag | Parallelstart | Produktiver REAL-Data-PASS erst wenn | Abschlussstatus |
|---|---|---|---|
| **M1-MA1C SOURCE-WITNESS** | **sofort**, parallel zu M0-Eigentümerprozess | Tatsächliche 5-Set-Dateien, Version/Hashes/Geo/Hydro-Semantik und M0-Referenzartefakt nachgewiesen | `M1_SOURCE_CONTRACT_WITNESSED` oder konsolidiert `BLOCKED` |
| **M1-MA2 RES PECD** | **sofort für Fixtures/Adaptercode**, parallel zu MA1C/MA3 | MA1C PECD-Evidenz, mindestens repräsentative reale M0-IDs, alle fünf Quelldatensätze | `M1_RES_REAL_DATA_QUALIFIED`, andernfalls `IMPLEMENTED_FIXTURE_ONLY` |
| **M1-MA3 HYDRO** | **sofort für Fixtures/Adaptercode**, parallel zu MA1C/MA2 | MA1C Hydro-Evidenz, M0 Hydrotypen/Zielkomponenten, nachgewiesene regionale Wasseranteile, alle fünf Quellsets | `M1_HYDRO_REAL_DATA_QUALIFIED`, andernfalls `IMPLEMENTED_FIXTURE_ONLY` |
| **M1-MA4 E2E** | Nach Code-/Source-Gates der drei Vorläufer | M0 reales qualifiziertes Paket + MA2 und MA3 REAL qualifiziert; DFT-/Last-Daten gemäß Scope | `M1_DETAILED_REFERENCE_READY_FOR_M2` oder `BLOCKED_WITH_FINDINGS` |

**Direkt parallel arbeitsfähig** bedeutet ausdrücklich **nicht**, dass sich mit fehlenden Rohdateien ein produktives PASS herbeiführen lässt. Die Adapter können ihre kontraktgebundenen positiven und negativen synthetischen Fixtures jetzt schreiben. Das reale Quellengate wird nicht durch generierte Mockdateien ersetzt.

**Gemeinsame Arbeitspolitik:** pro Auftrag ein vollständiges Makro inklusive source study, Implementation (wenn beauftragt), Fixtures, statischen Checks, gezielten Testläufen und zusammenfassendem Report. Keine weiteren Mikro-Chats je Technologie, Branch, Wetterjahr oder Fehler. M0 bleibt eigener Produzent; M2-Netzaggregation bleibt fremd.

## 2. Unveränderliche gemeinsame Verträge

1. **M0-Input** ist `DetailedNetworkReference v1 = (pypsa_network, m0_sidecar, source/identity ledger, revision keys, geo-quality, component support/capabilities)`; **nicht** nur ein nacktes `.nc`. Das echte M0-System wurde zum MA1-Zeitpunkt noch nicht ausgeführt (`DESIGNED_NOT_EXECUTED`).
2. **Statische M0-Invarianz:** keine Änderung / Erzeugung / Aggregation von Bus, Line, Transformer, Link, Generator, Load, StorageUnit, Store, Sondergeräte-Topologie, ID, `bus` oder `p_nom`. M1 schreibt ausschließlich deklarierte Zeitreihen an vorhandene IDs.
3. **Wetterdatensätze:** genau fünf **extern festgelegte**, bislang im verfügbaren Quellpaket nicht identifizierte IDs. Keine Auswahl/Reduktion/Ersetzung. Open-TYNDP 2026 kennt je Zielhorizont nur drei regulär gefüllte `WS`-Spalten; diese sind **kein Ersatznachweis** für fünf externe Wetterdatensätze.
4. **Räumliche Präzision:** elektrische Originalknoten ≠ tatsächliche Anlagenstandorte ≠ PECD-Raster ≠ PEON/P2ON/PEOF/P2OF/SZON. Identische regionale Wind-CF dürfen an verschiedenen elektrischen Originalknoten verwendet werden, sofern die Asset-Profilzuordnung validiert ist. Bus-Koordinate für Offshore und synthetische 3W-Sternknoten nicht als Anlagenort verwenden.
5. **Quellsemantik:** `Generator.p_max_pu` ist ein **Kapazitätsfaktor/Verfügbarkeitslimit, kein Dispatch**; PECD Solar ggf. MW/MWp statt AC-MW; Hydro `inflow` darf nicht mit Generation verwechselt werden. Zeitindex standardisiert UTC ohne timezone-aware Snapshots in PyPSA (UTC-Provenienz erhalten).
6. **Fail closed:** kein `fill_gaps_method=zero/mean`, kein `safe_planning_horizon`, kein `get_wscenario_tyndp(...)[0]` als implizite Fünf-WS-Ersetzung. Source-Version/Korrekturdatum/Hash je Datei.
7. **Upstream-Vorzug:** Open-TYNDP `tyndp-2026` @ `71a3a9a15b77114cd79458bceabc98e1a64dd58a` für PECD-v4.2-/Hydro-/Tech-Reader; PyPSA-Eur @ `1526bb820e25a9faa61f32b00bfc77dd05db6b2e`, PyPSA-Core @ `23650353eb1d059acfec28f4915ad3e068c085bf`. Kein blindes Kopieren alter Master-/Custom-Branches.
8. **GitHub-Branchisolation:** je Auftrag separater Arbeitsbranch vom selben geprüften M1-Vertragsbaseline-Commit; keine Änderung in den Arbeiterbranches der anderen. Ein zentraler Integration Owner cherry-pickt/führt erst nach Gates zusammen. Quellübernahme = SPDX/Lizenz-/Datenzugang prüfen.

## 3. M1-MA1C — Consolidated Physical Source & M0 Interface Witness

**Rolle:** Unabhängiger Data & Spatial Contract Auditor (keine produktive Python-Code-Implementation).  
**Start:** Sofort; parallel zu M0-Architektur/Implementierungsowner.  
**Branchvorschlag:** `research/iosn-m1-ma1c-source-witness-20261101`.  
**Autorität:** MA-1-Bericht + YAML oben; M0 Canonical/Architecture/Decision/Readiness at immutable `0275f482...`.

### Pflichtausführung als EIN Makro

- Repository- und sofern tatsächlich zugängliche Projekt-/Datenquelle nach den bereits festgelegten **fünf** Weather-IDs/Horizonten durchsuchen. Keine neue Auswahl, keine Rückfrage nach schon veröffentlichtem Kontext. Wenn nicht verfügbar: `NOT_PROVIDED`, nicht raten.
- Verfügbare **physische** PECD-v4.2- und Hydro-/DFT-Rohdaten oder präparierte Dateien inventarisieren: Herkunft, korrigierte Freigabe (TYNDP 2026: 2026-08-21 vs. vorläufiges PECD prebuilt 2026-08-13), Hash, Lizenz, verfügbares WScode, Technologie, Zeitindex, räumliche Produktklasse, PECD region masks.
- Verfügbares echtes M0-`DetailedNetworkReference v1`, `m0_sidecar`, Anlagen-/PyPSA-ID, Standortqualität, Hydro-`StorageUnit`/Store-/Link-Modell prüfen; getrennt markieren, was nur dokumentarischer Schemaentwurf ist.
- **Spatial mapping witness**: Onshore Wind PEON/P2ON, Offshore PEOF/P2OF, PV `ORIG` vs. Regional, synthetische M0-3W-Busse/Busproxy, Grenzlage und ggf. Multi-Region-Generator. Ohne reale Quelle sind synthetische Beispiele **nur Fixtures**, nicht Evidenz.
- **Hydro witness**: Herkunft und Bedeutung `HRR/HRI/HPI/HOL/HCL`, echte Tages-/Wochenintervallgrenzen, hydrologisches Gebiet und anlagenbezogene Anteilsschlüssel.
- Festen M0→M1-Inputcontract und ID-Crosswalk einschließlich Sidecar-Revision mit M0-Owner abgleichen. Nicht frühere CGMES-EQs/SV mit Wetterjahr vermischen.
- Gesamte **offene Inputliste EINMAL** konsolidieren, klare verifizierbare Exit-Kriterien und maschinenlesbare Source-Statusliste. Keine Mini-Iterationspings.

### Pflichtabgabe

Unter `docs/current/IOSN_Modul1/MA1C/`:
`REAL_SOURCE_INVENTORY.md`, `FIVE_WEATHER_ID_LEDGER.csv` (mit `NOT_PROVIDED` statt erfundenen IDs), `PECD_SPATIAL_PRODUCT_MATRIX.md`, `M0_REFERENCE_WITNESS.md`, `HYDRO_SOURCE_INTERVAL_LEDGER.md`, `CONTRACT_FREEZE_DECISION.md`, `HANDOFF_MA2_MA3.md`.

### Akzeptanz

- `M1_SOURCE_CONTRACT_WITNESSED` nur bei echten Datei-/Geometrie-/Anlagen-ID-Proben und fünf realen Weather-IDs/Komponentenquellen.
- `M1_SOURCE_CONTRACT_CONDITIONAL` bei explizit eingrenzbaren partiellen Quellen;
- `M1_SOURCE_CONTRACT_BLOCKED` bei nicht gelieferten M0-Package/5-Sets/Hydro-Mapping-Evidenzen.
- Status nie allein durch Quellcode- oder synthetische Fixture-PASS erklären.

## 4. M1-MA2 — PECD v4.2 Renewable Profiles & Original-Asset Spatial Mapping

**Rolle:** Python, xarray/pandas, Snakemake, PECD, geodetic CRS/region masks und PyPSA RES-Datenarchitektur.  
**Start:** Sofort parallel zu MA1C/MA3; solange Datenwitness offen: nur Code und synthetisch verifizierbare Tests, kein Real-Data-PASS.  
**Branchvorschlag:** `impl/iosn-m1-ma2-pecd-res-20261101`.  
**Arbeitsscope:** Wind Onshore, Wind Offshore, PV Utility/Rooftop und technologieabhängige PECD-CF. Hydro und Last nicht implementieren.

### Pflichtausführung als EIN Makro

- Open-TYNDP-`tyndp-2026`-Reader `prepare_tyndp_pecd_release.py`, `clean_tyndp_pecd_data.py`, `build_renewable_profiles_pecd.py`, `rules/sb.smk` reviewen und passende **Parser-/IO-Funktionen** adaptieren. Nicht das `TYNDP_NODE`-`busmap_base_s_all.csv` oder `buses_tyndp` in den CGMES-Busnamensraum kopieren.
- Technologie-Crosswalk aus `data/tyndp_technology_map.csv` auf die tatsächlich vorhandenen M0-`Generator.carrier`-Werte abgleichen. Regioncode-/Geometrie-ID-Registry, `asset_profile_map`, Zuordnungsqualität, Quelle/CRS und GPS-Proxy-Evidenz aufbauen.
- Multi-Region-Gruppen nur mit **MW-gewichteter** und dokumentierter Profilkombination; keine künstliche räumliche Interpolation der Wind-CF; Offshore/landseitigen Bus und 3W-Stern negativ testen.
- Korrekte PV-MWp-vs.-MW_AC-Basis, Puffer/Umwandlung und eventuelles Clipping als Vertragsgate; bei unbestimmter Konversion `BLOCK`.
- Alle extern vorgegebenen fünf Datensätze getrennt per `(horizon, weather_id)` einlesen; PECD-2026-Szenarien mit nur drei gefüllten Spalten dürfen nicht still auf fünf ergänzt werden.
- Output `renewable_cf[time, existing_generator_id]` + Katalog + Source-/Assignment-Ledger. **Kein** neues `Generator`-Objekt, keine Änderung `p_nom`, `bus`, `Line`, `Transformer`; keine komplette `compose_network`-Ausführung.
- Testfixtures zusammenhängend: ein/multiple Generatoren in PEON, PV-ORIG, regionale PV, Offshore/Landfall, synthetischer Bus, Mehrfachprofil, Mismatch/DC-AC, Leap/DST, 5-Sets-Quelle, Missing/Zero-Fallback.
- Gezielte automatisierte Tests und ein konsolidierter Implementierungsbericht in derselben Lieferung.

### Pflichtabgabe

`scripts/iosn_m1/res/`, `rules/iosn_m1_res.smk` (oder gleicher logisch isolierter Name), `tests/iosn_m1/test_res*.py`, versionierte konfigurierte Mapping-/Source-Catalog-Schemas, `docs/current/IOSN_Modul1/MA2/EXECUTION_REPORT.md`, `HANDOFF_MA4.md`.

### Akzeptanz

- `M1_RES_FIXTURE_QUALIFIED` bei synthetischen Source-/Mapping-/Zeitreihenfixtures und statisch unveränderten M0-IDs.
- `M1_RES_REAL_DATA_QUALIFIED` zusätzlich erst wenn **wirkliche** M0-Anlagen, offizielle PECD-Profile und fünf Wetterdatensätze vollständig geprüft, inklusive MW-Coverage und Source-Roundtrip.
- Sonst `M1_RES_BLOCKED_MISSING_SOURCE` oder `M1_RES_NUMERIC_OR_MAPPING_INCONCLUSIVE`, präzise Fehlerliste, keine erfundenen Profile.

## 5. M1-MA3 — Hydro Source Inflows, Basin Allocation & Original-Asset Mapping

**Rolle:** Hydro/PyPSA-Speichermodellierung, Zeit- und Energieerhaltung, xarray/pandas, Snakemake.  
**Start:** Sofort parallel zu MA1C/MA2, Datenwitness-Grenze wie oben.  
**Branchvorschlag:** `impl/iosn-m1-ma3-hydro-20261101`.  
**Arbeitsscope:** Hydro-Inflow-Quellen und Speicherzeitreihen; kein Wind/PV/DFT-Adapter, keine Netzaggregation.

### Pflichtausführung als EIN Makro

- TYNDP-2026-`clean_tyndp_hydro_inflows.py` und `build_tyndp_hydro_profile.py` sowie `tyndp_technology_map.csv` vollständig reviewen. Ihre `bus`-Dimension ist TYNDP-Gebiet, **nicht** Originalanlage.
- Hydro-Source-Semantik nach Typ und Produkt **zwingend** unterscheiden: `HRR` RoR, `HRI` Reservoir, `HPI` Pondage, `HOL` offenes PHS, `HCL` geschlossenes PHS; Quelle `inflow` vs. tatsächlich erzeugte Energie; bestehende `Generator`/`StorageUnit`/`Store+Link`-Modellklasse.
- `hydro_region_to_existing_asset_map` nur mit dokumentiertem hydrologischem/TSO-Anteil. Nicht elektrische Bus-Koordinate als Wasser-Einzugsgebiet deklarieren.
- Physikalische Energie- und Einheitenbilanz: `MWh per native week/day` → `MW` über **Originalintervallgrenzen** (incl. 53-Wochen/teilweise letzte Woche, Leap-/DST-/UTC-Fälle), Summe `MW × h` = Quellenergiemenge, getrennte Source-/Plant-Bilanzen; Wirkungsgradsemantik prüfen.
- `module_hydropower` bei Bedarf als methodischen Vergleich für echte Becken-/Standortzuordnung untersuchen, dessen Atlite/EIA-synthetischen Inflow aber **nicht als original PECD** ausgeben.
- Geschlossene PHS ohne externen natürlichen Zufluss ≠ mit 0 ausgefüllte unbekannte Quelldatei. Fehlende Hydroquellen blockieren ihre Pflichtkomponente, keine automatische `fillna(0)`.
- `hydro_inflow[time, existing_storage_or_hydro_id]` und ggf. genehmigtes RoR-`p_max_pu` erzeugen; Input-/Output-Semantik und erlaubte Zielattribute maschinenlesbar dokumentieren.
- In einem Rutsch Fixtures und Tests einschließlich kapazitäts-, energie-, technik- und Quellennegativfällen.

### Pflichtabgabe

`scripts/iosn_m1/hydro/`, `rules/iosn_m1_hydro.smk`, `tests/iosn_m1/test_hydro*.py`, `hydro_allocation_schema`, `interval_energy_ledger`, `docs/current/IOSN_Modul1/MA3/EXECUTION_REPORT.md`, `HANDOFF_MA4.md`.

### Akzeptanz

- `M1_HYDRO_FIXTURE_QUALIFIED` bei sämtlichen synthetischen Energie-/Mapping-/Typprüfungen.
- `M1_HYDRO_REAL_DATA_QUALIFIED` bei echten regionalen Inflows, hydrologischen Asset-Anteilen, 5-Sets-Abdeckung und qualifiziertem Speicherportmodell;
- andernfalls klar begrenzter `BLOCKED`-Status mit fehlender Source-Evidenz, niemals fictive MWh→MW oder Basin-Mapping.

## 6. M1-MA4 — Non-Mutating PyPSA Composition + Demand/Availability Integration + Independent Qualification

**Rolle:** verantwortlicher PyPSA-Integrator, begleitet durch **unabhängigen Akzeptanzreviewer** (separate Rolle, keine Selbstzertifizierung).  
**Start:** Erst nach tatsächlichem Output von MA2 und MA3 und einem qualifizierten M0-Netz; ein konsolidiertes Integrations- und Prüfmakro.  
**Branchvorschlag:** `impl/iosn-m1-ma4-integration-20261101`.

### Pflichtausführung als EIN Makro

- `M0_ReferencePackage` in *definierter Revision* laden; statische Fingerprints/IDs über alle elektrischen Komponenten und Links/Stores vor der Dateninjektion erfassen.
- Kanonische CF-Arrays von MA2, Hydro-Inflow-Arrays von MA3 und **nur bei belegter M0-Load-ID-/DFT-Zuordnung** Lastzeitreihen hinzufügen. Bereits vorhandene M0-`loads_t.p_set` oder Dispatchzeitreihen nicht still überschreiben; Quelle/Policy vergleichen. Thermische Verfügbarkeit nur bei autoritativer Quelle.
- Für jedes tatsächlich externe `(horizon, weather_id)` exakte Zeitachsen aufbauen, NA-Leerstellen vor PyPSA-Reindex erkennen; PyPSA verlangt timezone-naive Snapshots, UTC-Herkunft dokumentieren; PyPSA-`Network.set_scenarios` **nicht** als PF-kompatible Alternative zu separaten vollen Netzen voraussetzen.
- Ausschließlich dynamische Attribute auf Whitelist setzen; statische M0-Komponenten nach Export/NetCDF-Reimport bit-/schema-/toleranzgerecht vergleichen.
- Vollständigen Trace: PECD source→profile→asset→bus→time→`p_max_pu`; Hydro source→Basin/Region→asset→`inflow`; DFT source→bestehende Load-ID→`p_set`.
- Ohne Last-/Dispatchdaten werden keine angeblich gelösten Lastflüsse erzeugt. AC/DC-PF nur wenn ein tatsächlicher, physikalisch bilanziertes Betriebsfallset vorliegt; separate Qualifikation, nicht künstliches `p_set = p_max_pu`.
- Gemeinsames Validierungsgate über alle fünf Quellen, Regionencoverage/MW/Technologien, Hydroenergie, PV-Normierung, Geoqualitätsmatrix, ursprüngliche Topologie und Reproduzierbarkeit. Speicher-/RAM-Kosten prüfen.
- **Unabhängiger Reviewer** liest den finalen Producer-Commit, die echten Output-/Gate-Dateien und testet gegen die M0-Originalreferenz. Abschlussbericht unterscheidet `STATIC`, `FIXTURE`, `REAL_DATA`, `PF`-Capability ausdrücklich.

### Pflichtabgabe

`scripts/iosn_m1/compose/`, `rules/iosn_m1_compose.smk`, `tests/iosn_m1/test_e2e*.py`, qualifizierte `detailed_reference_{horizon}_{weather_id}.nc` für **alle gelieferten fünf Datensätze**, `M1_HANDOFF_TO_M2.md`, `QA_ACCEPTANCE_REPORT.md`, maschinenlesbare Quell-/Asset-/Netz-/Zeitreihenledger und unabhängiger Reviewer-Findings.

### Akzeptanz

`M1_DETAILED_REFERENCE_READY_FOR_M2` nur wenn vollständiges reales M0-Package, echte fünf Szenarios, RES/Hydro und (soweit als Pflicht im konkreten Zielmodell) Lasten vollständig qualifiziert sind, keine Änderung der statischen M0-Kernparameter, NetCDF roundtrip/Source/Capacity/Hydro-Energy Checks bestehen und der unabhängige Reviewer einen begrenzten PASS veröffentlicht. Sonst `M1_CONDITIONAL_OR_BLOCKED_WITH_CONSOLIDATED_FINDINGS`, ohne M2-Handoff-Freigabe.

## 7. Governance: konsolidierte Kommunikationsstruktur

- **Governance/Lead in bestehendem Modul-1-Chat:** MA1C Source-Gate, konsistente Interpretation der Baseline, konfliktfreie Zusammenführung, M0/M2-Schnittstellen.
- **Drei parallel startende Arbeitschats:** MA1C (Source/Data), MA2 (RES), MA3 (Hydro). MA2/MA3 dürfen Fixtures/Code parallel vorbereiten; der Real-Data-Gate wird bei ihnen **nicht** eigenmächtig freigegeben.
- **Ein nachgelagerter integrativer Arbeitschat**: MA4 Producer; **ein unabhängiger Reviewer** innerhalb der konsolidierten Endabnahme mit getrennt dokumentierter Autorität/Reports. Keine Mikro-Chats für jede Technologie/WS.
- **Arbeitsbranch pro Rolle**; jede Rückgabe enthält Commit SHA, geänderte Dateien, Tests/Reports, Quellenlücken und eindeutigen Status. Producer darf fremde Module nicht verändern.
- M0-Owner arbeitet unabhängig; M2-Netzaggregation darf die M1-Arbeit nicht verdrängen oder vorwegnehmen.

## 8. Kurzform aller Copy/Paste-Handoffs

Jeder neue Worker-Chat erhält zusätzlich die folgende verbindliche Eingangsformel: *„Vollständig ausführen, nicht nur planen. Lies zuerst die bei GitHub veröffentlichte MA1-Architektur, den logischen Datenvertrag und diesen NEXT-MACROS-Handoff am angegebenen unveränderlichen Commit. Prüfe den jeweiligen Upstream-Commit, arbeite nur in deinem isolierten Branch und veröffentliche einen einzigen konsolidierten Rücklauf. Keine Wetterjahrauswahl/Netzaggregation. Wo echte Source-Dateien fehlen, liefere alles mit Fixtures Belegbare, kennzeichne Blocker und beanspruche keinen Real-Data-PASS.“*

**MA1C Chat-Handoff:** „Übernimm Auftrag `M1-MA1C Physical Source & M0 Interface Witness`, Abschnitt 3 dieses Dokuments. Führe den gesamten Daten-/M0-/PECD-/Hydro-Audit als ein Makro durch, ohne produktive Python-Codeänderungen. Liefere die sechs definierten Ledger/Reports einschließlich eindeutiger fünf Weather-IDs oder markiertem NOT_PROVIDED und hartem Freezeentscheid.“

**MA2 Chat-Handoff:** „Übernimm Auftrag `M1-MA2 PECD v4.2 Renewable & Spatial Mapping`, Abschnitt 4. Implementiere in einem einzigen Makro wiederverwendete, jedoch vom TYNDP-Zonenmapping entkoppelte PECD-Reader; zugeordnet wird ausschließlich auf bereits vorhandene M0-Generator-IDs. Liefere den vollständigen Satz aus Code, Fixtures, Tests, QA und S-GOV-Handoff. Real-Data-PASS nur mit G1C/D.“

**MA3 Chat-Handoff:** „Übernimm Auftrag `M1-MA3 Hydro Source Inflow & Basin Mapping`, Abschnitt 5. Entwickle in einem Makro den quellentreuen, energieerhaltenden Hydro-Adapter an vorhandene M0-Generator-/Storage-/Store-IDs mit positiven und negativen Tests. Kein heimliches Null-Inflow, keine Scheinpräzision wöchentlicher Daten. Real-Data-PASS nur mit G1C/E.“

**MA4 Chat-Handoff (nach G2/G3):** „Übernimm Auftrag `M1-MA4 Full Reference Time Series Composition & Independent Acceptance`, Abschnitt 6. Integriere die Outputs aus MA2/MA3 und geprüfte DFT-/Load-Quellen in das unveränderte M0-Paket; liefere fünf vollständige Netze, Revisions-/Sourceledger, NetCDF roundtrip, E2E-QA, unabhängigen Review und den M2-Handoff nur bei echtem qualifizierten PASS.“

**Materialisierungsstatus:** Dieses Dokument gibt verbindliche Auftragstexte zur Freigabe durch den Owner vor. Durch die Dokumentation selbst ist weder die Implementierung gestartet noch ein Datenwitness erbracht.
