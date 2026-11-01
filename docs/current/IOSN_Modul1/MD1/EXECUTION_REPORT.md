# M1-MD1 — Consolidated Real Source & M0 Reference Witness

**Datum:** 2026-11-01  
**Verbindliche Eingabe:** [M1 S-GOV MD1 §2](https://github.com/AlOussama/TYNDP_Products/blob/03fa261850da8c940283668741bb7a17c46bd769/docs/current/IOSN_Modul1/S_GOV_M1_NEXT_MACROS_AND_MA4_HANDOFFS_2026_11_01.md), Commit `03fa261850da8c940283668741bb7a17c46bd769`, verifiziert.  
**Isolierter Branch:** `research/iosn-m1-md1-real-source-m0-witness-20261101`.  
**Abschlussstatus:** **`M1_SOURCE_CONTRACT_BLOCKED`**.  
**Evidenzgrenze:** qualifizierte Quellenkataloge und statische Software-/Schnittstellenverträge; **keine** physisch lesbaren fünf Projekt-PECD-Sourcefiles, keine echte Hydro-Datei, keine CDS-NetCDF-Masken-Datei und kein ausgeführtes M0-DNR-Referenznetz. Keine produktive Implementation/Simulation/Netzänderung.

## 1. Wichtige fachliche Präzisierung: Zwei unabhängige Datenströme

**PECD/TYNDP und CGMES sind vollständig unabhängige Eingangsquellen.** PECD kennt **Regionen, Raster, meteorologische und hydrologische Variablen, Technologieprofile und Zeitindizes**, aber *nicht* die späteren elektrischen CGMES-Bus-/Generator-IDs. M0/CGMES kennt die **elektrische Topologie und vorhandene Anlagen**, aber erzeugt keine regionalen PECD-Ressourcendaten. Beide werden erst an einer separaten M1-Join-Grenze zum PyPSA-Referenznetz verbunden.

**Vier getrennt bewertete Gate-Linien:** `S-PECD` = unabhängige PECD-v4.2-Source-Bytes/Geometrie/Version/Zeiten; `S-HYDRO` = Hydro-Source-Bytes/Intervall-/Semantikprüfung unabhängig von Netzdaten; `N-M0` = separat produziertes qualifiziertes CGMES→M0-DNR-Referenzpaket; `J-M1` = späterer Source-Region/Profile→bereits vorhandene M0-Asset-/Port-ID-Join. Ein M0-Blocker kann ein real bestandenes PECD-Native-Source-Gate **nicht** aufheben; er blockiert nur den Join/Real-MA4R. Umgekehrt ist ein korrektes M0-Netz kein Wetter-/Hydro-Source-PASS.

Dieses MD1-Audit führt ausdrücklich **keinen** CGMES-/Netz-Match als angeblich PECD-eigenes Datenfeld. Regioncode, Profil-ID, Weather-ID, Dimensionen, Einheiten, Kalender, Source-Hash und source-native Geometrie gehören in den eigenständigen Source-Katalog. Erst im getrennten M1-Join-Ledger erscheinen M0-Asset-/Bus-/Port-ID, Anlagenpunkt-/Geoqualität und Gewichtungs-/Zuteilungsbelege.

## 2. Unveränderliche Evidenz und tatsächlich ausgeführte Prüfung

| Autorität | Fixierter Stand und Auditgegenstand | Qualifikation |
|---|---|---|
| S-GOV-Auftrag und Review | `03fa261850da8c940283668741bb7a17c46bd769`, Dateien `S_GOV_M1_NEXT_MACROS_AND_MA4_HANDOFFS_2026_11_01.md` Blob `3dbd1362a8bb81e5fbf0297b3823c94c343b815c`; `S_GOV_M1_CONSOLIDATED_MA1C_MA2_MA3_REVIEW_2026_11_01.md` Blob `c4dcc2d6f90ff4092bb25f08ea2e275e81bea263` | `GIT_TEXT_WITNESSED`; Review `M1_PARALLEL_DELIVERIES_COMPLETE__FIXTURE_QUALIFIED__REAL_DATA_BLOCKED` |
| MA1C | `f366f8162e1023ff959721d5fed14ad80dcba890`, Abschlussbericht + `OPEN_INPUTS_AND_EXIT_CRITERIA.md` (`IN-01…IN-10`) + Source-Status | `GIT_TEXT_WITNESSED`; fünf Slots `NOT_PROVIDED` |
| MA2 | `11700baa8df8cafc6bd71b96998f8b2bca647ca0`, Source-Validator/CSV-/Geo-Schemas, Report, QA | `IMPLEMENTED_FIXTURE_ONLY`, Producer nennt 20/20 lokale Tests, **nicht hier erneut ausgeführt** |
| MA3 | `b3b9bf133d1b5c968323a31f8ac76090f1f2e182`, Hydro-Reader/Normalizer/CSV-/JSON-Schemas, Report, QA | `IMPLEMENTED_FIXTURE_ONLY`; CI 62 Tests *inkl. vorhandener Tests*, **kein realer Inflow** |
| M0 CAN/DNR | `b1e284996fa69f81651daf9150b829e6a42e4ce3`, `85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md`, `90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md` | `ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING`, **kein Runtime-/DNR-PASS** |
| M0 M4-0 | `ba55e4a12819a88605474606888ca23ee2108584`, `95` Toolchain-/Source-Witness, `96` RunRelease, `97/98` Preflight | `M4_0_STATIC_PREFLIGHT_COMPLETE`; kein produziertes reales PyPSA-DNR |
| Open-TYNDP 2026 | [`tyndp-2026` @ `71a3a9a15b77114cd79458bceabc98e1a64dd58a`](https://github.com/open-energy-transition/open-tyndp/tree/71a3a9a15b77114cd79458bceabc98e1a64dd58a), `tyndp_versions.csv`, `tyndp_technology_map.csv`, PECD/Hydro/DFT-Skripte und Snakemake | echte Git-Text- und Versionsdaten, **keine Projekt-PECD-/Hydro-Bytes** |
| ECMWF PECD-v4.2 | [PUG](https://confluence.ecmwf.int/spaces/CKB/pages/540941752/Climate+and+energy+related+variables+from+the+Pan-European+Climate+Database+derived+from+reanalysis+and+climate+projections+v4.2+Product+user+guide+PUG) und [CDS](https://cds.climate.copernicus.eu/datasets/sis-energy-pecd) | Produktsemantik, Masken-/Variablenspezifikation und Korrekturhinweise öffentlich, **kein heruntergeladener Quellbestand** |
| ENTSO-E/ENTSOG TYNDP-2026 | [Downloadportal](https://2026.entsos-tyndp-scenarios.eu/download/), dort PECD, Hydro Inflow, Demand sowie Daten-Lizenz | Downloadlinks und öffentliche CC-BY-4.0-Erklärung bestätigt; direkter ZIP-Inhalt in dieser Prüfung nicht lesbar |

**Repositories:** Vollständige Git-Baum-Inventur am S-GOV-SHA (129 Blobs, Git-Antwort nicht gekürzt), MA2-SHA (144 Blobs), MA3-SHA (147 Blobs), M0-M4-0-SHA (138 Blobs, nur M0-Dokumentation statt produziertem Netz). Verfügbare PECD-/Hydro-Programm-/Datenmanifest-Beispiele sind Fixtures/Code, keine Original-RES- oder Hydro-Klimadatensätze. Projekt-/Library-Dateisuche und Suche nach dem früheren fünf-Wetter-Entscheid lieferten **nur Methodik und Platzhalter**, nicht die fünf konkret beschlossenen IDs.

**Zugriffsgrenze:** TYNDP-offizielle ZIP-Links sind erreichbar und als ZIP referenziert, eine textorientierte Webschnittstelle kann `application/zip` jedoch nicht auslesen. Direkter externer Download/DNS aus der aktuellen Containerlaufzeit ist nicht verfügbar. Deshalb wurden ZIP-Header/Member/CSV-Werte/Hydrointervallgrenzen/Masken-Pixel **nicht** gelesen oder gehasht. Das betrifft auch drei vorhandene alte Projekt-ZIP-Blobs, deren Inneninhalt nicht qualifiziert ist. Das ist ein **konkret benanntes Prüfdefizit** und kein Beweis, dass offizielle Dateien überhaupt fehlen.

## 3. Vier getrennte Gate-Entscheidungen

| Gate | Normativer Input | Tatsächlicher Stand | Ergebnisklasse |
|---|---|---|---|
| `S-PECD-CATALOG` | offizielle Produktspezifikation, Technologie-/Raum-/Releasekatalog | öffentlich plus Reader geprüft | **`PASS_STATIC_CATALOG_ONLY`** |
| `S-PECD-PHYSICAL` | echte source-native Wind/PV-Dateien + fünf IDs, Byte-SHA256, Zeit/Unit/Region + offizielle Masken | 0 originale Datendateien geprüft; 0 Maskenbytes, 0/5 Projekt-IDs | **`BLOCKED_NOT_WITNESSED`** |
| `S-HYDRO-CATALOG` | Technologie-/Intervall-/Regionsemantik | PUG und TYNDP-Reader verifiziert | **`PASS_STATIC_CATALOG_ONLY`** |
| `S-HYDRO-PHYSICAL` | echte Hydro-Energie-/Intervallfiles für fünf IDs + SHA256/Intervallgrenzen | 0 reale Inflow-Bytes/Originärintervalle | **`BLOCKED_NOT_WITNESSED`** |
| `N-M0-CONTRACT` | CAN/2.0.0, DNR/1.0.0 und Eigentümer-Freeze | Dokumentarischer Freeze geprüft | **`PASS_DESIGN_ONLY`** |
| `N-M0-PHYSICAL` | reales ausgeführtes PyPSA-Netz + Sidecar + Identity/Capability/Geo-Manifest | 0 echte ausgeführte M0-Referenzpakete | **`BLOCKED_NOT_PROVIDED`** |
| `J-M1-SPATIAL_AND_HYDRO_JOIN` | vorab unabhängig qualifizierte Sourceprodukte UND echtes M0; unveränderliche IDs; Region→Asset/Wasserbeckenanteile | 0 reale Source→Asset- oder Basin→Asset-Zuordnungen | **`BLOCKED_PREREQUISITES`** |
| `J-M1-CAN_DNR_BRIDGE` | `canonical_revision_id`, `projection_id`, `reference_id` und Legacy-Producer-`network_revision_id` | statische Kontraktabweichung nachgewiesen, keine reale M0-DNR-Probe | **`STATIC_MISMATCH_RUNTIME_BLOCKED`** |
| `MD1-MA4R-RELEASE` | alle Pflichtquellen, physisches M0, Mapping, Rechte/Hashes, später MA4F-Fixture-Gate | mehrere harte Voraussetzungen offen | **`NOT_RELEASED`** |

**Logische Konsequenz:** Die native PECD-/Hydro-Qualifikation darf auf eigenem Dataset unabhängig von M0 stattfinden. Der gesamte Status `M1_SOURCE_CONTRACT_WITNESSED` verlangt nach dem verbindlichen S-GOV-MD1-Auftrag zusätzlich `N-M0` und `J-M1`. Da diese und die Quell-Bytegates fehlen, heißt das **Gesamturteil** `M1_SOURCE_CONTRACT_BLOCKED`, nicht `CONDITIONAL`.

## 4. Präzise zusätzliche Interoperabilitätsbeobachtungen

- MA2 `MA2_SCHEMA_V1.json`/Code unterstützt für Einzelprofile `TYNDP_RAW10_DATE_HOUR`, `TYNDP_DATE_HOUR`, `ISO_CSV`. Das native **PECD-ORIG-PV-NetCDF** (wenn als Quellprodukt gewählt) ist damit *nicht unmittelbar* als NetCDF-Quellparser abgedeckt. Ein verifizierter, unverfälschender vorgeschalteter Formatadapter wäre gegebenenfalls vom Integrationsowner zu spezifizieren, **nicht MD1**. Ein behaupteter ORIG-PASS allein aus synthetischem CSV ist nicht zulässig.
- MA2 räumlicher Matchingpfad liest **GeoJSON-Polygone**; ECMWF bietet für PEON/PEOF/P2ON/P2OF offizielle **fractional NetCDF-Masken**, Original-Shapefiles teils nicht öffentlich. Ein GeoJSON-`official mask` benötigt eine dokumentierte, versionierte und geometrisch konsistente Ableitung bzw. separate genehmigte offizielle Polygone. Nicht `mask-area fraction` mit Anlagen-MW-Anteilen verwechseln. Die native PECD-Quellqualifikation benötigt keinen M0-Generator.
- MA3 Hydro-Source-/Native-Interval-Reader kann real erst mit `WS###`-Datei und tatsächlich belegten `WEEK`-/Tag-Intervallgrenzen laufen. Dessen `network_revision_id`/Asset-/Portbezug ist *nur* die nachgelagerte Join-Stufe; Hydroquellen selbst enthalten keinen CGMES-Bus.
- MA2 und MA3 verwenden altvertraglich `network_revision_id`. Die verbindliche M0-Reparatur CAN/2.0.0/DNR/1.0.0 trennt `source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id` und `reference_id`. Ein Ersatz `network_revision_id=source_revision_id` oder `=projection_id` ist **falsch**. Nur eine versionierte M0-Owner-autorisiert akzeptierte DNR-Bridge darf das Legacy-Feld in einer expliziten M1-Join-Sicht auflösen.
- Die MA2-Quell- und MA3-Hydro-Producer sind fixture-funktional, aber weder echte M0-Anlagen-Geoqualität noch M0-Hydro-Ports noch unabhängige reale Datenabnahme belegt. MA4F ist eigenständiger Integrator und zuständig für Composer/Target-Ownership/Runtime; MD1 ändert keinen Code.
- Keine Ausgabe `Generator.p_max_pu` als Dispatch; MA3 HRR kann ebenfalls das Attribut schreiben, daher nur MA4F-Target-Ownership-Ledger verhindert die Kollisionsklasse RES vs RoR, wenn tatsächlich zusammengeführt.

## 5. Publizierte Artefakte

Die Source-native Daten werden in **separaten** Katalogen geführt: [PECD_NATIVE_PROFILE_CATALOG.md](PECD_NATIVE_PROFILE_CATALOG.md), [PECD_SOURCE_PRODUCT_LEDGER.csv](PECD_SOURCE_PRODUCT_LEDGER.csv), [HYDRO_NATIVE_SOURCE_INTERVAL_LEDGER.md](HYDRO_NATIVE_SOURCE_INTERVAL_LEDGER.md), [HYDRO_SOURCE_WITNESS.csv](HYDRO_SOURCE_WITNESS.csv), [FIVE_WEATHER_IDS.csv](FIVE_WEATHER_IDS.csv).

M0 ist separat: [M0_DNR_IDENTITY_WITNESS.md](M0_DNR_IDENTITY_WITNESS.md), [M0_DNR_FIELD_COMPATIBILITY.csv](M0_DNR_FIELD_COMPATIBILITY.csv). Erst für die Join-Grenze: [M1_SOURCE_TO_ASSET_JOIN_CONTRACT.md](M1_SOURCE_TO_ASSET_JOIN_CONTRACT.md), [M1_JOIN_READINESS.csv](M1_JOIN_READINESS.csv).

Governance- und Machine-Ledgers: [SOURCE_RELEASE_LICENSE_SHA256_LEDGER.csv](SOURCE_RELEASE_LICENSE_SHA256_LEDGER.csv), [QUALIFICATION_REPORT.json](QUALIFICATION_REPORT.json), [BLOCKER_REGISTER.csv](BLOCKER_REGISTER.csv), [MA4R_RELEASE_DECISION.md](MA4R_RELEASE_DECISION.md), [S_GOV_M1_HANDOFF.md](S_GOV_M1_HANDOFF.md).

**Ausführungsumfang:** Realdatei-Tests/Runtime nicht ausführbar ohne zugängliche Bytes. Repo-/Code-/Schema-/Dokumentationswitness abgeschlossen. Keine Wetterjahreswahl, keine hydroelektrische Pseudomessung, keine physische Netzdatenmutation, keine MA2/MA3-Produktivänderung, kein Merge in `main`, keine M2-Aggregation.
