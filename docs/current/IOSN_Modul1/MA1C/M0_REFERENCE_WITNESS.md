# MA1C — M0 DetailedNetworkReference / Sidecar / Geographic Quality Witness

**Prüfbasis:** M0 `0275f48231a0794bea324b9cab34700bb0de8f5b`, Docs 30/40/60/70; unabhängiger Review `ea62050a867c27036552af28d3e0102a8689f4ec`; jüngerer normativer M3-Repair `85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md` (Blob `209416fd687d5ab700993684ca64a998241a4cad`), **noch keine hier nachgewiesene Owner-Akzeptanz/Ausführung**.

**Witness-Entscheid:** `M0_REFERENCE_REAL_PACKAGE_NOT_PROVIDED`. Dokumente wurden geprüft; kein tatsächlich produziertes `DetailedNetworkReference v1`, `pypsa_network`, `m0_sidecar`, geomantisches Asset-Sample, Store/Link-Portschema oder Revisionsmanifest vorgelegt.

## 1. Die verbindliche Grenze ist ein Paket, kein isoliertes NetCDF

| Vertragsobjekt | M0 Soll laut Architektur/Repair | Real-Witness |
|---|---|---|
| `DetailedNetworkReference/1.0.0`-Manifest | typisiert, `schema_version=1.0.0`, `reference_id`, Source-/State-/Projection-Refs, SHA256-Manifeste | `DESIGN_ONLY` |
| Elektrische PyPSA-Detailansicht | `Bus,Line,Transformer,Generator,Load,Link,StorageUnit,Store,ShuntImpedance` je Capability | `NOT_PROVIDED` |
| `m0_sidecar` | originaler RDF-/CIM-Graphanker, Identity, Geography, Boundary, Equipment-/Terminal-Trace, Limits, 3W/Single-/Multi-Island, Projektion Loss/Quality | `DESIGN_ONLY; FILE_NOT_PROVIDED` |
| Identitätsketten | `source_entity_id` / `source_object_id` / `asset_id` / `view_id` / tatsächlicher PyPSA-Komponentenname getrennt | `NOT_PROVIDED` |
| Revisionen | `source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id`, `source_set_hash`, `mapping_policy_hash` | `DESIGN_ONLY` |
| Geografiequalität | `country_code`, originale GL/CRS-Quelle, `geo_quality`, originale Plant-/Substation-/Bus-Rolle, bewiesener Datenursprung | `NOT_PROVIDED` |
| Komponenten-/Portklasse | `component_support_matrix`, `capabilities`, zielkompatibles Hydro-`Generator`/`StorageUnit`/`Store+Link`-Schema | `DESIGN_ONLY` |
| Fingerprints | statische PyPSA-Tabellen, IDs, Verbindungen, NetCDF Roundtrip und SHA256 des Sourcegraphen | `NOT_EXECUTED` |

## 2. Revisions- und ID-Korrektur aus M0-M3

Der ältere MA-1-Vertrag referenziert `network_revision_id`. Der neuere M0-Korrekturentwurf hebt den bisherigen unpräzisen Alias auf: `network_revision_id` wird als veralteter Alias von **`canonical_revision_id`** interpretiert, während `projection_id`, `source_revision_id` und `operating_state_id` **getrennte** Revisionsachsen sind. **M0-Owner muss den tatsächlichen DNR/1.0.0-Release- und SemVer-Handshake bestätigen**, bevor MA2/MA3 reale Mappingtabellen pinnen.

**Verbotene Gleichsetzungen:** `raw CGMES mRID = canonical asset_id = PyPSA view_id = Generator.index`; `CGMES SSH/SV scenario_time = weather_id`; `TYNDP_NODE = CGMES_BUS`; `PV plant_location = station centroid`. Ein Original-Equipment kann in mehreren PyPSA-Zeilen abgebildet werden, insbesondere 3W/Links; `view_source_map` ist n:m, nicht ohne Quelle bijektiv.

Erwarteter Referenz-Crosswalk: siehe [M0_INTERFACE_CROSSWALK.csv](M0_INTERFACE_CROSSWALK.csv). Keine reale Zeile mit einer erfundenen Source-/View-ID.

## 3. Real-Geo-Witness und Fehlerpolitik

- **Echte AC-Busse:** der `country_code` muss von Originalhierarchie/Endport und versioniertem Registry-Beleg stammen. Ein aus Substation-Centroid berechnetes Bus-x/y bleibt ein **`DERIVED`-Proxy**, keine automatisch gesicherte Generator-Plant-Koordinate.
- **3W-Ersatz:** `bus_role=SYNTHETIC_3W_STAR`, `source_transformer_id`, `country_code=NULL`, keine echte Geometrie, Ausschluss aus Länderstatistik und Anlagenpunkt-Matching. Ein synthetischer Bus darf keine Wetterprofilregion nur durch x/y erhalten.
- **Grenzüberschreitende Leitungen/PST/HVDC:** originaler Land-/Authority-Bezug **pro Terminal**, nicht ein frei erfundener Geräte-Ländercode. Ihre elektrischen Verbindungen bleiben in M0 und damit auch M1 bestehen.
- **Offshore:** `plant_location`, `offshore_region`, `landing_bus` getrennte Quellmerkmale; fehlender Plant-Ort = `UNRESOLVED`.
- **Geoqualität:** `SOURCE_PLANT`, `VERIFIED_STATION_PROXY`, `DERIVED_BUS`, `SYNTHETIC`, `MISSING/AMBIGUOUS` dürfen nur nach M0-kontrolliertem Enum/Provenienzbeleg in produktive Mappingmethoden überführt werden; diese Bezeichnungen sind hier Prüfklassen, kein vorgefundenes reales M0-Enum.

## 4. Hydro-Port/Komponentenwitness

| Bestehende M0-Klasse | Zulässiger Quellport nach expliziter M0-Supportentscheidung | Was noch nachgewiesen werden muss |
|---|---|---|
| `Generator` / HRR RoR | bei genehmigtem Modell `generators_t.p_max_pu` aus hydrologisch korrekt bestimmter Verfügbarkeit | Source-Kapazität, Energie vs P und Portsemantik, bestehender Generator-/Busname |
| `StorageUnit` / HRI HPI HOL | `storage_units_t.inflow`, **wenn** M0 `StorageUnit` real erstellt, sign-/Wirkungsgradmodell klar | realer Bestand, Anlagentyp, `p_nom/max_hours`, interner Energieport, Quelle als Inflow |
| `Store + Link`-System | kein allgemeiner `Store.inflow`-PyPSA-Default; projektspezifischer **genehmigter** Einspeise-/Zeitreihenport | tatsächliches Link-/Store-Modell, Vorzeichen/Energieerhaltung, Quelle→Port-Referenz |
| `HCL` closed-loop pumped hydro | kein unterstellter natürlicher Inflow | Evidenz, ob unabhängige natürliche Zuflüsse vorhanden sind; sonst keine erzeugte Quellnull als fehlender Datei-Ersatz |

Unveränderliche M0-`p_nom`, `bus`, Topologie, Storage- und Portkonfiguration. `component_support_matrix` muss reale `EXACT/APPROX/UNSUPPORTED`-Deklaration und testbare Capability am betreffenden Gerät führen; nur Designabsicht reicht nicht.

## 5. Capability und dynamische Attribute

Default-Write-Allowlist aus M1: `generators_t.p_max_pu`, `storage_units_t.inflow`, `loads_t.p_set`; alle anderen dynamischen Ports nur mit freigegebenem Vertrag. Keine vorhandenen M0-Zeitreihen still überschreiben, keine statischen IDs/`p_nom`/`bus` ändern. Zeitachse M1: nach geprüfter UTC-Normalisierung **timezone-naive** PyPSA-Snapshots, ursprünglicher Zeitzonen-/Intervallbeleg im Source-Manifest. Netzmodell-Capabilities `CANONICAL_READY`, `PYPSA_ACPF_READY`, `PYPSA_LPF_READY`, `REDUCTION_ADAPTER_READY` sind **nicht austauschbar**. Dieser Witness nimmt keinen dieser Runtime-PASSes vorweg.

## 6. Bindender M0-Owner-Handshake

Ein einziges revisionsgebundenes M0-Paket mit: `DetailedNetworkReference` manifest.json + referenziertem PyPSA-Netz + `m0_sidecar` + Source-/ID-/View-/Terminalmap + geo-quality, CRS, `bus_role`, Country-/Crossborder-Validierungen + hydro component support/port + statischen Fingerprints + QA-/Capability-Report und allen SHA256. Repräsentative reale Fälle: Onshore, Offshore, Solar, HRR und HRI/HPI/HOL/HCL soweit existierend, Load sowie synthetischer 3W und grenzüberschreitender Port. Fehlende reale Klassen ausdrücklich `NOT_PRESENT` mit Coverage, **nicht** erfunden.

**Schluss:** `G1-C=BLOCKED_NOT_PROVIDED`; typisierte DNR-Feldliste fachlich vorbereitet, keine materielle Schnittstellenakzeptanz durch M0-Owner nachgewiesen.
