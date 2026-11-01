# MD1 — M0 CAN/2.0.0 / DNR/1.0.0 real network and identity witness

**Dieses M0-Paket ist eine unabhängig von PECD entstehende Eingabe.** M0 erzeugt Busse, Generatoren, Lasten, Speicher, Anschlüsse, technische Stammdaten und Original-CGMES-Provenienz. Keine PECD-Regions-/Wetter-IDs sind Felder der M0-Netzreferenz.

## 1. Dokumentierte, noch nicht real ausgeführte M0-Version

- [CAN/2.0.0 und DNR/1.0.0](https://github.com/AlOussama/TYNDP_Products/blob/b1e284996fa69f81651daf9150b829e6a42e4ce3/docs/current/IOSN_Modul0_CGMES/85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md), [S-GOV Freeze](https://github.com/AlOussama/TYNDP_Products/blob/b1e284996fa69f81651daf9150b829e6a42e4ce3/docs/current/IOSN_Modul0_CGMES/90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md): **`ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING`**, kein echter CGMES-/PyPSA-/NetCDF-/Sidecar-Run.
- [M4-0 Quelle/Backend/Runtime](https://github.com/AlOussama/TYNDP_Products/blob/ba55e4a12819a88605474606888ca23ee2108584/docs/current/IOSN_Modul0_CGMES/95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md) und [RunRelease-Gates](https://github.com/AlOussama/TYNDP_Products/blob/ba55e4a12819a88605474606888ca23ee2108584/docs/current/IOSN_Modul0_CGMES/96_M4_0_RUNRELEASE_POLICY_AND_GATES.md): **`M4_0_STATIC_PREFLIGHT_COMPLETE`**, keine installierte/ausgeführte Referenz, Source/Importrechte und T-06 noch offen.
- Tatsächliche M0-Projektreferenz-NetCDF-/Sidecar-/DNR-Manifeste unter den geprüften Governance-/M0-Git-Bäumen nicht sichtbar. GitHub-Textdokumente sind keine erzeugten Netze. Ein realer M0-Owner-RunRelease fehlt.

## 2. Normativer M0-Identity-/Revisionsraum (nur M0)

| Feld | Eindeutige Bedeutung nach `85` | MD1-Realwitness |
|---|---|---|
| `source_entity_id` | stabile, qualifizierte Source-Identität (MRID oder RDF_SUBJECT nach Authority/Namespace) | `NOT_PROVIDED` |
| `source_revision_id` | originale Source-Model-Set-/Graphrevision | `NOT_PROVIDED` |
| `operating_state_id` | elektrischer SSH-/SV-Zustand, **kein** Wetter-ID | `NOT_PROVIDED` |
| `canonical_revision_id` | CAN/2.0.0-Normalisierung + State/Policy | `NOT_PROVIDED` |
| `projection_id` | versionierte elektrische PyPSA-Projektion auf CAN/State | `NOT_PROVIDED` |
| `reference_id` | identifizierte DNR/1.0.0-Ausgabe mit Hash-/Policy-/Component-Manifest | `NOT_PROVIDED` |
| `m0_sidecar` | Source-/Terminal-/Equipment-/Geo-/Loss-/Country-/Support-/Port-/FK-Nachweise | `NOT_PROVIDED` |
| `view_source_map` | n:m Source-Entity→PyPSA-View, synthetische 3W/Star-IDs separiert | `NOT_PROVIDED` |

Der Legacy-`network_revision_id`-Name in MA2/MA3 darf nicht automatisch zu `source_revision_id`, `projection_id` oder `reference_id` umgedeutet werden. DNR-Contract nennt `network_revision_id` veralteten Alias von `canonical_revision_id` **im Altvertrag**, jedoch ist ein realer Join zusätzlich an `projection_id` und `reference_id` zu binden. Die neue DNR-Schemaversion und konkrete Hash-/Feld-Handshake-Vollständigkeit muss vom M0-Owner bestätigt werden.

## 3. Geografische Qualität und Modellgrenzen gehören M0

**Reale Busse** tragen geprüfte Country-/Terminalzuordnung, ggf. nur abgeleitetes Station-Centroid-x/y. Diese Koordinaten sind kein gesicherter Standort eines Windparks oder Solar-Assets. **Synthetische 3W-Sternbusse** haben `bus_role=SYNTHETIC_3W_STAR`, `country_code=NULL`, keine physische Geokoordinate und keine ursprüngliche Anlagenrolle. **Offshore** braucht getrennte Anlagen-/Landfall-Koordinaten. Cross-border-Branches tragen Original-Country je Terminal; elektrische Leitungen bleiben intakt.

**Hydro-Porttypen:** tatsächlich vorhandene `Generator`, `StorageUnit` oder `Store+Link`-Architektur einschließlich Energiebus, `p_nom`, `max_hours`, `efficiency_dispatch`, erlaubtem natürlichen Zuflussport, Capability-/Quality-Flag. Die Architekturdokumentation beweist **keine** echte hydroelektrische M0-Komponentenabdeckung. Ein `Store` hat keinen universellen `inflow`-Port.

## 4. Benötigter realer M0-Package-Witness (M0-Owner)

`DetailedNetworkReference/1.0.0` mit realer, bereits eingefrorener CGMES-Eingangsrevision, ausführbar generierter PyPSA-Netzdatei; SHA256-verifizierten Originalgraph-/DNR-/Sidecar-/QA-/Capability-/Identity-Manifests; `source_revision_id`, `operating_state_id`, `canonical_revision_id`, `projection_id`, `reference_id`; tatsächlichen `Generator/Load/StorageUnit/Store/Link/Transformer`-IDs/Ports, `carrier/p_nom/bus`, wirklicher Geo-/CRS-/Country-/Offshore-/Synthetic-Bus-Qualität und pro Gerät `EXACT/APPROX/UNSUPPORTED` mit ausgeführtem Witness. Rechte/Versionpin und komponentenspezifische M0-Akzeptanz sind vor M1-Join erforderlich.

**Realresultat:** Kein DNR-Byte-/Sidecar-/Identity-Package und keine echte Source-Generator-/Hydro-ID-Probe verfügbar; `N-M0-CONTRACT=PASS_DESIGN_ONLY`, `N-M0-PHYSICAL=BLOCKED_NOT_PROVIDED`. Diese Einschränkung ist **unabhängig vom PECD-Native-Source-Status**.
