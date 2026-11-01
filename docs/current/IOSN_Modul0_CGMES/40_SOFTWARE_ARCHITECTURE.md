# M2 — 40 SOFTWARE ARCHITECTURE
## Modul 0: CGMES ↔ kanonischer Netzvertrag ↔ detaillierte PyPSA-Ansicht

**Status:** `M2_ARCHITECTURE_DESIGNED_PENDING_INDEPENDENT_REVIEW` (2026-11-01). **Keine Implementierung, keine ausgeführten Tests, keine ENTSO-E-Konformitätsbehauptung.**
**Autorität:** `00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md`; fachliche Inputs `10_REQUIREMENTS.md`, `20_BACKEND_ASSESSMENT.md`, `30_CANONICAL_DATA_CONTRACT.md` und `50_VALIDATION_CONTRACT.md` am Ausgangscommit `e595335d511af6f8c9c05c88276553363ed37045`. Architekturentscheidungen in `60_ARCHITECTURE_DECISION.md` sind für ausdrücklich behandelte Kollisionen präzisierend, die Arbeiterdokumente bleiben unverändert.

## 1. Ziele, Anforderungen und Nichtziele

**Ziel:** Ein zweckgebundenes Modul für die Interpretation und den qualifizierten Import stationärer symmetrischer AC-/HVDC-Übertragungsnetze aus CGMES 2.4.15 und 3.0, für eine nachvollziehbare elektrische Projektion nach PyPSA und für einen kontrollierten CGMES-Export. Eingänge können Single-IGM oder CGM mit mehreren IGMs/Boundary-Modellen sein. Ländergrenzen sind **keine elektrische Trennbedingung**: grenzüberschreitende Zweige und Flüsse bleiben über terminalbezogene Referenzen erhalten. Modul 1 verarbeitet später Clustering/Netzreduktion separat.

**Qualitätsattribute:** Korrektheit und Evidenz > Reproduzierbarkeit > Provenienz/Verlusttransparenz > Austauschbarkeit des Backends > Betriebsvereinfachung > Performanz. Keine stillen Originaldatenergänzungen, keine unmarkierte Änderung der elektrischen Semantik. Vorhandene Verteilungskomponenten dürfen im Quellgraph liegen; Modellierung unsymmetrischer Netze, Schutz-/Kurzschluss-/Dynamikrechnung, Wetter-, Demand-, PACD- oder Optimierungs-/Dispatchaufgaben sind kein Teil von M0.

**Anforderungsvorrang:** 39 MUSS, sechs SOLL, drei OPTIONAL aus `10`; alle MUSS bleiben als spätere, capability-bezogene Akzeptanzpflicht bestehen. Ein Design darf technische Unmöglichkeit als `BLOCK/UNSUPPORTED` und zulässige, markierte Approximation als `CONDITIONAL` ausweisen, aber keinen unbelegten PASS.

## 2. Architekturblick und Komponenten

~~~mermaid
flowchart TD
 A["CGMES 2.4.15 / 3.0\nIGM / CGM + Boundary"] --> B["DeliveryArchive\nImmutable XML/ZIP, hashes, headers"]
 B --> C["BackendPort\nPowSyBl primary / VeraGrid alternative"]
 C --> D["CanonicalStore\nsource graph anchors, typed tables, identity & revisions"]
 D --> E["ProjectionService\nTopologie + elektrisch geprüfte Mappingfunktionen"]
 E --> F["PyPSA detailed Network + sidecar\nDetailedNetworkReference v1"]
 F --> G["Modul 1 / IoSN\nnur nach eigener Capability-Freigabe"]
 D --> H["ChangeSet / inverse-mapping gate"]
 F -. "nur explizit freigegebene edits" .-> H
 H --> I["ExportCoordinator\nUPDATE_IMPORTED / CREATE_FROM_PYPSA"]
 B --> I
 C <--> I
 I --> J["Staged delivery + semantic diff\nprofiles, refs, audit & atomic publish"]
 K["ValidationEngine\nREQ, capability, T-01...T-24"] -.-> C
 K -.-> D
 K -.-> E
 K -.-> I
~~~

**Invariante Zwei-Sichten-Modell:** `canonical_source` ist der (mit Raw-Graph-Referenzen) originaltreue Netzbestand; `electrical_projection` ist ein abgeleitetes positives Sequenznetz; `pypsa_network` ist ein konkretes, ggf. verlustbehaftetes Berechnungsmodell. `m0_sidecar` verknüpft die drei, ersetzt aber kein vollständig unveränderliches Roharchiv. Ein `pypsa_network` darf nie allein zur Wiederherstellung historischer CGMES-Metadaten verwendet werden.

~~~mermaid
flowchart LR
 subgraph "Externe gepflegte Bibliotheken"
 P["PyPowSyBl / PowSyBl Core"] 
 V["VeraGrid (Alternative)"]
 end
 subgraph "M0: eigene sieben Verantwortungspakete"
 BA["backend"]
 AR["archive_provenance"]
 CS["canonical"]
 PR["projection"]
 PP["pypsa_port"]
 EX["export"]
 QA["validation"]
 end
 P --> BA
 V -. "nur aktivierter Fallback" .-> BA
 BA --> AR
 BA --> CS
 AR --> CS
 CS --> PR
 PR --> PP
 CS --> EX
 AR --> EX
 BA --> EX
 QA -. "gates" .-> BA
 QA -.-> CS
 QA -.-> PR
 QA -.-> PP
 QA -.-> EX
 end
~~~

**Fachliche Modul-API, nicht neue Framework-Klassen:** Die dreizehn Einzelverantwortungen aus dem M2-Auftrag werden in sieben Paketen umgesetzt, um doppelte Services zu vermeiden. Die Schnittstellen bleiben trotzdem gesondert dokumentiert.

| Paket | Komponenten / Besitz | Eingang → Ausgang | Nicht verantwortlich |
|---|---|---|---|
| `backend` | `BackendPort` + `PowSyBlBackend`; später `VeraGridBackend` | CGMES-Delivery + Profiloptionen → BackendSession, normierte SourceTables, Capabilities | Eigenes CIM-Regelwerk oder PyPSA-Elektrik |
| `archive_provenance` | `DeliveryArchive` + `ProvenanceStore` + `ChangeTracker` | Rohbytes/Metadaten/Delta → Raw-Graph-Anker, ID-/Change-Ledger | Erfindung von CGMES-Information |
| `canonical` | `CanonicalNetwork`, Revisions-/Tabellen-Speicher, Semantikvalidator | normierte SourceTables → CanonicalRevision | Auflösen komplexer Elektrik in XML-Parser |
| `projection` | `TopologyAdapter`, `MappingEngine`, `ElectricalProjection` | Revision+State+Policy → gerichteter elektrischer Detailgraph, Quality/Loss | Veränderung des Originalgraphen |
| `pypsa_port` | `PyPSAAdapter`, `DetailedNetworkReference` | elektrischer Detailgraph → PyPSA Network + Sidecar | Clustering, Zeitreihen, N-1-Grenzen |
| `export` | `ExportCoordinator` und Transaktionssteuerung | Originalstate + erlaubte Deltas oder synthetischer Konstruktionsvertrag → staged CGMES-Profile | Universelle, selbst implementierte XML-Serialisierung |
| `validation` | `ValidationEngine` + Capability-Reports | beliebiger Schnittstatus/Export → PASS/BLOCK/CONDITIONAL/NOT_ASSESSED mit Belegen | Zertifizierung ohne unabhängige Konformitätsprüfung |

**Abhängigkeitsregel:** Kein Import von `pypowsybl` oder `VeraGrid` außerhalb `backend` und minimaler Export-Bridge. Keine CIM-spezifischen Klassen im Tabellen-/PyPSA-Adapter. Keine Fremdmodule dürfen mutable globale Originalobjekte halten. Elektrische Formeln sind unabhängig von Backendnamen testbar.

## 3. Backend-Port: Vertrag und Lebenszyklus

**Externe belegte Beispiele** (nur Quellreferenzen, noch nicht ausgeführt): PyPowSyBl stellt `pypowsybl.network.load`, `get_buses`, `get_lines`, `get_2_windings_transformers`, `get_generators`, `get_loads`, `get_ratio_tap_changer_steps`, einzelne `update_*`, `Network.update_from_file`, `Network.save` und Import-/Exportparameter-Discovery bereit. Der PowSyBl-CGMES-Export dokumentiert EQ, TP, SSH, SV, CGM-SSH/SV-Update und optionale TP-Ausgabe. **Nicht belegt** ist eine automatische Python-API für jede Original-RDF-Aussage, GL-/Boundary-Neuschreiben oder beliebige Inverse aus PyPSA. Beleg: [pypowsybl network user guide](https://github.com/powsybl/pypowsybl/blob/main/docs/user_guide/network.rst), [PowSyBl import](https://github.com/powsybl/powsybl-core/blob/main/docs/grid_exchange_formats/cgmes/import.md), [PowSyBl export](https://github.com/powsybl/powsybl-core/blob/main/docs/grid_exchange_formats/cgmes/export.md).

Der folgende **eigene Adapter-Port ist Entwurf**, keine behauptete API der Fremdbibliotheken:

~~~python
class FormatBackend(Protocol):
    def capabilities(self, profile_set, requested_operation) -> CapabilityReport: ...
    def open_delivery(self, immutable_manifest, import_options) -> BackendSession: ...
    def extract_tables(self, session, canonical_contract_version) -> BackendSnapshot: ...
    def extract_identity_metadata(self, session) -> IdentityEvidence: ...
    def create_update_plan(self, session, validated_delta, export_policy) -> ExportPlan: ...
    def stage_export(self, session_or_build_spec, export_plan, staging_uri) -> ExportArtifacts: ...
    def close(self, session) -> None: ...
~~~

- `BackendSession`: nicht serialisierbarer, versionierter Laufzeit-Handle zur geladenen IIDM-/CGMES-Instanz; muss geschlossen/entsorgt werden. Zustand, Version und Ursprungshash werden im Manifest nachgewiesen. **Das Archiv bleibt unabhängig vom flüchtigen Handle**; Update-Export kann nach wiederholter Backend-Ladung aus unveränderten Originaldateien plus validiertem Delta rekonstruierbar geplant werden.
- `BackendSnapshot`: Tabellen für Busse, Leitungen, 2W-/3W-Transformatoren, Terminals/Topologie, Generatoren, Lasten, Shunts, HVDC, Limits/Geo (falls API liefert), Quellfeldsignaturen und source-backend IDs. Jedes Feld besitzt `SOURCE/DERIVED/DEFAULT/MISSING` plus Beleg.
- `IdentityEvidence`: Original-IDs und Beziehungen **nur** aus nachweislich verfügbarer backend-/quellgraphischer Sicht; Lücken werden als `UNKNOWN` behandelt. Alias oder Name ist kein Ersatz für originalen RDF-Subject bzw. mRID. Falls für den angefragten Export unverzichtbare Provenienz nicht zugänglich ist: `BLOCK_EXPORT_UNPROVEN`.
- `CapabilityReport`: pro Backend-Version, CGMES-Familie, Profilgruppe und Operation `SUPPORTED_VERIFIED`, `SUPPORTED_STATIC_ONLY`, `UNSUPPORTED` oder `UNKNOWN` mit Evidenz. `SUPPORTED_STATIC_ONLY` bedeutet ausschließlich Quellcode-/Dokumentationsbefund, **keine produktive Freigabe**.
- `ExportPlan`: explizite `changed_attributes`, `supported_write_fields`, Ziel-Profile, Header-/Dependency-Plan, Modellautoritäts-/Versionierungsstrategie und `expected_semantic_diff`; unklare Änderungen sind nicht exportierbar.
- `ExportArtifacts`: temporär erzeugte Dateien, Hashes, Profil-/Objektliste, Backend-Log, QA-Ergebnis. Atomare Publikation erst nach grünen Gates.

**Backendwechsel:** Backendname und Paketversion gepinnt; die Normalisierungsgrenze (`BackendSnapshot`) ist die einzige Austauschstelle. Unterschiedliche Backend-Reihenfolgen dürfen kanonische Primärschlüssel nicht verändern. Gleichheit wird anhand typisierter Werte, Objektbeziehungen und tolerierter, explizit gekennzeichneter mathematischer Rundung beurteilt, **nicht** allein anhand gleicher Anzahl von DataFrame-Zeilen. Der Wechsel ist eine neue Backend-/Mapping-Revisionsqualifikation; keine Live-Heißumschaltung innerhalb einer offenen Exporttransaktion.

**Staged Freigabe:** In M4 zuerst PowSyBl-Adapter. VeraGrid-Portvertrag ist M2-Design, kein Auftrag, zwei vollständige Implementierungen parallel zu schreiben. Optionale Ergänzung durch SOPTIM-Tests ist keine Backend-Abhängigkeit der Primärpipeline.

## 4. Canonical-v1-Datenobjekte, Identität und Revisionen

Der ausführliche **logische** Datenvertrag aus `30_CANONICAL_DATA_CONTRACT.md` bleibt Grundlage. Dieses Dokument konkretisiert nur die widerspruchsrelevanten Regeln K-03/K-04 und die API-Grenze.

| Datenprodukt | Beispieltabelle/Funktion | Fachliche Rolle |
|---|---|---|
| Source+Manifest | `source_files`, `model_headers`, `source_objects`, `source_occurrences`, `source_relations`, `raw_attributes` | Unveränderliche Wahrheit über Input, RDF-Subjects, Profile, Header, Provenienz, unmapped attributes |
| State+Topology | `operating_states`, `equipment_states`, `terminals`, `switches`, `topology_membership`, `buses`, `ac_islands` | Zustandsabhängiges Bus-/Terminal-/Inselmodell, kein impliziter globaler Slack |
| Equipment+Constraints | `ac_lines`, `transformer_ends`, `tap_changers`, `generators`, `loads`, `shunts`, `hvdc_converters`, `operational_limits` | Parameter, Endorientierung, aktive Grenzen samt Einheiten und Herkunft |
| Projektion | `mapping_identity`, `pypsa_mapping`, `value_provenance`, `assumption_events` | Backend- und Canonical-unabhängige deterministische PyPSA-View |
| Export/Audit | `change_ledger` (in `archive_provenance` ergänzt), `export_transactions`, `loss_manifest`, `quality_events` | Inversibilität, kontrollierter Delta, Nachweise und Verbote |

**Normativer K-03-Präzisierungsvertrag** (überschreibt bei Widerspruch die informelle `source_key`-Definition aus `30`): Identität bezieht sich **nicht** auf ein einzelnes Profil. `source_entity_key` = (`identity_namespace`, `identity_kind`, `identity_value`). Zulässige `identity_kind`: `MRID`, `RDF_SUBJECT`; `identity_namespace` ist der eindeutig qualifizierte Modell-/Authority-/Exchange-Kontext des Objekts, nicht beliebig der EQ-/SSH-/TP-/SV-Name. Wo derselbe logisch identifizierte Gegenstand in mehreren Profilen oder Dateien wiederkehrt, entsteht **ein** `source_object` plus mehrere `source_occurrences`. Profil, Datei, Header und Graph werden auf Occurrence-/Relationsebene gespeichert. Ein mRID-loses CIM-/SV-Objekt erhält niemals ein behauptetes historisches mRID; es wird über sein vollständiges RDF-Subject/URI samt Quellenkontext identifiziert. Blank nodes erhalten eine graph- und kanonisierungsspezifische, nur im Input-Revisionsraum gültige Identität; über neue Serialisierungen ist keine globale Blank-Node-ID-Stabilität behauptet. Unklare oder kollidierende Authorities/IDs ⇒ `BLOCK`.

**Determinismus:** `source_object_id` = stabiler projektinterner Hash/UUID über qualifizierten `source_entity_key` **und** eingehende Originalrevision, falls ein immutable occurrence-identifier benötigt wird. `asset_id` = logisch identifizierter Primärschlüssel innerhalb einer Netzfamilie. `view_id` = deterministic ID aus `network_revision_id`, originalem asset, Projektionsfunktion, Portrolle und Namespace; nicht als mRID exponieren. `network_revision_id` = versionierter Zustand aus Modellset-, Betriebszustands- und Mappingpolicies mit Hashes; identische Archive + identische Konfiguration ⇒ identische fachliche IDs, ungeachtet Zeitstempel eines erneuten Importlaufs. Neuer Quellstand oder geänderte Mappingpolitik ⇒ neue Revision; publizierte Revision wird niemals in-place geändert.

**Source-Graph-Treue:** `raw_attributes` allein garantiert kein semantisch vollständiges RDF; Originaldateien, ZIP-Mitglieder, Modelheader, Graphpartitionierung und nicht abgebildete RDF-Aussagen bleiben über immutable `raw_graph_ref`/Manifest verfügbar. Normative Export-1-Garantie bezieht sich auf **unveränderte semantische Objekte/Referenzen innerhalb eines definierten Modellsatzes**, nicht byteidentische XML-Formatierung und nicht nicht-veröffentlichbare, technisch verlorene Originalgraphinformation.

**K-04 Country-Regel:** Ein **realer**, für Modul 1 akzeptierter originaler AC-Bus muss eine verifizierte Länder-FK besitzen; ein synthetischer interner 3W-Sternbus besitzt `bus_role=SYNTHETIC_3W_STAR`, `country_code=NULL`, `source_transformer_id` und `excluded_from_country_clustering=True`. Das ursprünglich in `30` als allgemein verpflichtend formulierte `buses.country_code` ist **konditional nach bus_role**. Synthetische Busse dürfen nicht mit einem künstlichen ISO-Ländercode in die reale Netzhierarchie geschrieben werden. Cross-border Line/PST/HVDC hat getrennte landesbezogene Endports, nicht ein erzwungenes 'Leitungsland'.

**Null-/Unit-Regel:** `NULL != 0`, `missing != default`. Internes Bezugssystem für P/Q/S = MW/Mvar/MVA, U = kV (LL), Leitungs-Z = Ω, Shunt-Y = S, Winkel = deg mit expliziter Deklaration, Transformator-pu mit wirklicher Rating-/Voltage-Base; alle abgeleiteten Werte referenzieren `function_id`, Input-IDs und Policy-Version. Kein PyPSA-Default ist CGMES-Quelle.

## 5. Projektion und elektrische Konsistenz

**Allgemeiner Pfad:** Versionierte Mappingregeln wählen Quellen, Feld-/Vorzeichen-/Einheitenfunktionen sowie Status-/Error-Policy. `TopologyAdapter` liefert die gültigen bus/terminal mappings pro `operating_state_id`. `ElectricalProjection` berechnet eine elektrische View und ein `loss_manifest`. `PyPSAAdapter` erzeugt nur die aus dem ausgewählten Capability-Set zulässigen Standardkomponenten; fehlende Sondermodelle blockieren die angeforderte Berechnungsfähigkeit, ohne Originaldaten zu löschen.

| Quellklasse / Problem | PyPSA-Projektion | Gate / Evidenz |
|---|---|---|
| `TopologicalNode`/`ConnectivityNode`/Switch | `Bus` nach TP oder nach zulässig abgeleitetem EQ/SSH-Graph | Vorhandenes TP vs abgeleitete Topologie prüfen; open/connected/inService getrennt |
| `ACLineSegment` | `Line` mit expliziten Ω-Serienwerten und gesamten S-Shunts | Zweitor-PI-Admittanz, Orientierung, Spannungsebene, Ports |
| `EquivalentBranch` | gekennzeichnete Ersatz-`Line`/äquivalenter Branch | niemals als historische physische AC-Leitung umetikettieren |
| `PowerTransformer` 2W | `Transformer`, per unit, Tap-Seite/Shift, T/PI-Policy | Zweitor-Y, ratedU/ratedS, Shunts, Tap-Richtungen; `Transformer.type=""` falls explizite Werte |
| `PowerTransformer` 3W | drei geprüfte 2W-Sternäste + synthetischer Bus | 3-Port-Kron-Y-Gleichheit, Ursprungs-3W im Sidecar |
| `SynchronousMachine`, `EnergyConsumer`, `ExternalNetworkInjection` | `Generator`/`Load` nach zugelassenem PQ/PV/Slack-Regime | P/Q-Load-Sign, Q-Limits, VoltageControl, p_nom != p_set |
| `Linear/NonlinearShuntCompensator` | `ShuntImpedance` mit Arbeitspunkt-/Sections-Ableitung | fixes g/b eventuell EXACT, Steps/Voltage-Control APPROX |
| HVDC AC/DC Converter & DC Line | geeignete Punkt-zu-Punkt-`Link`-View oder festes Terminal-P-Q-Modell | portseitige Verlust-/Statusbilanz; verlustbehaftete bidirektionale Link-Einheit **nicht** als exakt behandeln; MTDC unsupported |
| `CurrentLimit`/`OperationalLimitSet` | Selected study `s_nom`/`s_max_pu` plus voll granulare Limits im Sidecar | keine undokumentierte Umrechnung A→MVA, keine N-1-/Dauergrenze als Normallimit |
| GL/DL, Boundary/EQBD/TPBD | Geo, IDs und Raw-Sidecar; nicht im üblichen PyPSA-Core | GL optional, CRS explizit; fehlende Boundary FK blockt Netzassembly |

**Unit-Gate:** Für dreiphasige Basis mit Leiter-Leiter-`U_base` [kV], `S_base` [MVA] gilt `Z_base=U_base²/S_base` [Ω], `z_pu=Z_Ω/Z_base`, `Y_base=1/Z_base` [S]. Bei Transformatormodellen die konkrete Wicklungsbasis (nicht blind 100 MVA) anwenden. Leitungsschaltadmittanz (Gesamtwert `gch+j bch`) wird im symmetrischen PI-Modell hälftig auf beide Ports verteilt, sofern das Zielmodell genau diese Konvention besitzt; sonst mittels Zweitor-Y überprüfen. Tap als `t=τ exp(jφ)` ist eine mathematische Portkonvention, nicht ohne Test identisch mit backend-/PyPSA-Side-Semantik. Für einen positiven linearen PST-Flussbeitrag `P_0→1≈(θ0-θ1-φ)/x_eff` sind Porttausch und Winkelvorzeichen zu validieren. Bei HVDC darf `p0<0` in einem einzelnen verlustbehafteten Link nicht automatisch die physikalisch richtige Rückwärtsverlustfunktion erhalten.

**Capability-Regel:** `EXACT` bezeichnet nur die im gewählten Anwendungsmodell nachgewiesene Information oder mathematische Größe, nicht historische CIM-Objektidentität. `APPROX` nennt Gültigkeitsbereich und numerische Wirkung; `UNSUPPORTED` blockiert die entsprechende View/Exportoperation. Der Canonical-/Raw-Import darf auch bei noch nicht abbildbarer PyPSA-Elektrik als eigenständige Capability bestehen bleiben.

## 6. Import-, Reimport- und Exportabläufe

### 6.1 Erstimport

~~~mermaid
sequenceDiagram
 participant U as Caller
 participant A as Archive
 participant B as CGMES Backend
 participant C as Canonical
 participant Q as QA
 participant P as Projection/PyPSA
 U->>A: stage immutable delivery + hash profiles/headers
 A->>Q: profile/version/boundary inventory
 Q-->>U: BLOCK if critical references/version mismatch
 A->>B: open delivery + version-aware options
 B->>C: extract tables + provenance (UNKNOWN allowed for noncritical fields)
 C->>Q: identity/FK/topology/state gates
 Q-->>C: eligible capability set
 C->>P: chosen operating_state + mapping policy
 P->>Q: electrical mapping and loss manifest
 Q-->>U: per-capability decision
 P-->>U: DetailedNetworkReference v1 + sidecar if eligible
~~~

**Profilpolicy K-01:** EQ/SSH sind Kern für einen unsolved stationären Input. TP wird übernommen/gegengeleitet, sofern vorhanden; bei Fehlen nur nach verifizierbarer, backendgestützter Ableitung aus EQ/SSH, andernfalls `BLOCK_TOPOLOGY`. SV darf bei unsolved fehlen; bei solved/SV-Referenzprüfung ist es erforderlich. 2.4.15-Boundary kann EQBD/TPBD benötigen. 3.0 erfordert kein künstliches TPBD; tatsächliche Core-EQ-/Boundary-Exchange-Policy je deklarierter Modellversion anwenden. GL optional; wenn geliefert, CRS/Position- und Herkunftsvalidierung. Keine globale Annahme, dass alle Profile bei jedem einzelnen Import vorhanden sein müssen. Bei Multi-IGM referenzielle Assembly und Authority-Zuordnung, keine geometrischen Cross-border-Merges.

### 6.2 Reimport und Zustandsaktualisierung

~~~mermaid
sequenceDiagram
 participant U as Caller
 participant A as Archive
 participant C as Canonical
 participant B as Backend
 participant Q as QA
 U->>A: new delivery set / SSH update + hashes
 A->>C: compare source model/version/profile dependencies
 C->>B: load base + version-qualified update
 B->>C: new BackendSnapshot (not overwrite previous)
 C->>Q: compare identities/refs/operating states
 Q-->>C: publish next immutable revision if accepted
 C-->>U: new revision_id + changed objects + capabilities
~~~

Getrennte `source_set_hash`, `operating_state_id` und `network_revision_id`; keine impliziten Löschungen. Nur explizite supported Update-Familien und ‑Modelldependenzen zulassen. `update_from_file` der PyPowSyBl-Python-API ist kein Nachweis, dass jede EQ-/TP-/Boundary-Mutation als partieller Update-Import zulässig wäre. Konkurrierende Revisionen ⇒ optimistic hash conflict und BLOCK.

### 6.3 Update-Export `UPDATE_IMPORTED`

~~~mermaid
sequenceDiagram
 participant U as Caller
 participant X as ChangeTracker
 participant A as Original Archive
 participant B as Backend
 participant Q as Validation
 participant E as ExportCoordinator
 U->>X: request approved detail-network field edits
 X->>Q: policy/identity/inverse/affected-profile gate
 Q-->>U: BLOCK if noninvertible, unsupported or structural
 A->>B: reload original + metadata/model variants
 X->>B: apply only allowlisted backend edits
 B->>E: stage CGMES SSH/SV; optional TP only with qualification
 E->>Q: dependencies, model headers, semantic diff, unknown fields
 Q-->>E: PASS or BLOCK (never silent drop)
 E-->>U: atomic delivery + loss/audit manifest only on PASS
~~~

**Wichtig K-02:** PowSyBl Quick-CGM-Export kann mehrere IGM-SSH und ein CGM-SV (optional TP) schreiben; das garantiert **nicht** frei erfundene oder unveränderte originalfremde RDF-Tripel, GL oder EQBD/TPBD im Ausgabeprofil. **Exportstrategie v1:** Original-EQ/TP-/Boundary- und andere unverändert erhaltene Profile verbleiben im referenzierten, unveränderlichen Archive/Delivery-Set; für geänderte Zustandsattribute schreibt das Backend **nur die belegten unterstützten Profile** und korrekte `FullModel/DependsOn/Supersedes`-Beziehungen. Eine streng semantisch unchanged-graph-Policy wird an den original erhaltenen oder unverändert gereichten Objekten geprüft. Unbekannte XML-Header und Extension-Felder dürfen beim Neuschreiben nicht unbemerkt als gleichwertig ausgegeben werden. Wenn die erforderliche Python-Original-ID/Graph-Rückbindung nicht nachgewiesen werden kann, wird `UPDATE_EXPORT_READY` nicht vergeben; ein zusätzliches, nicht bereits beauftragtes universelles RDF-Patcher-Subsystem ist **keine** implizite M2-Entscheidung.

**SV-Export:** Ein neues SV muss aus einem nachweislich geeigneten, konsistenten *berechneten* Betriebspunkt stammen; bloßes Setzen der SSH-P/Q-Werte oder Verwenden ungeprüfter Startwerte ist keine neue State-Variables-Lösung. Ohne solver-/snapshot-/version-/sign-konformen Nachweis keinen neuen `SV`-PASS behaupten. Für reinen SSH-Update-Export darf die Vertragsklasse dies getrennt von der Fähigkeit zum SV-Neuschreiben ausweisen.

### 6.4 Create-Export `CREATE_FROM_PYPSA`

~~~mermaid
sequenceDiagram
 participant U as Caller
 participant K as CGMES Construction Contract
 participant B as Backend
 participant Q as Validation
 U->>K: PyPSA detailed view + authority/equipment/topology metadata
 K->>Q: required class/port/base/identity/profile/limits
 Q-->>U: BLOCK if incomplete
 K->>B: construct new explicit CGMES equipment model
 B->>Q: stage EQ/TP/SSH; SV only from qualified solved state
 Q-->>U: independent synthetic-network qualification + loss report
~~~

Kein Versprechen, alte Node-Breaker-Schaltanlagen, historische mRIDs, gl-/boundary-Strukturen oder alte Modellautoritäten aus bloßen PyPSA-Tabellen wiederherzustellen. Neue IDs müssen mit einer dokumentierten neuen Modellautorität und deterministischer Regel erzeugt werden. `CREATE_EXPORT_READY` hat eigene Tests/Scope und ist **nicht** Voraussetzung für den priorisierten v1-Update-Export.

### 6.5 Fehlerschwere, Transaktionen

- `FATAL`: fehlerhafte Datei/Header/Identitätskollision; keine vertrauenswürdige Canonical-Revision.
- `BLOCK`: harte Capability-Vorbedingung verletzt (fehlender Port, ungültige Basis, fehlende Boundary, nicht invertierbarer Delta, unzulässiger Graph-Diff).
- `WARN`: genehmigungsfähige, ausdrücklich benannte Approximation im gewählten Modellkontext, mit betroffenem Feld und elektrischer Auswirkung.
- `INFO`: nachvollziehbare Transformation ohne Informationsdefizit.
- `NOT_APPLICABLE`: z. B. SV-PF-Vergleich für unsolved Input ohne SV; kein PASS.

**Transaktion:** Staging → Profil-/Daten-/Referenz-/elektrische Prüfungen → Manifest mit Hashes/Policy/Version/Proof → atomare Publikation einer abgeschlossenen Revision bzw. Delivery. Bei FATAL/BLOCK kein teilweiser "fertiger" Export; Zwischenartefakte bleiben optional in isolierter Diagnosequarantäne, nie als freigegebene Datei.

## 7. YAML-Konfiguration, Rechenfunktionen und SemVer

Deklarative Regeln: versioniertes Schema, `backend`, Profilpolicy, Feldumbenennung, Quell-/Zieltyp, Einheit, Vorzeichen, referenzierte Funktions-ID, Fallback-/Blockpolitik, resultierende Capability und Verlusttyp. Keine beliebig ausführbaren Expressions, dynamischen Python-Imports oder `eval` im Mapping; nur registrierte, versionierte pure Transformationsfunktionen.

**Schemaskizze, ausdrücklich NICHT ausführbar:**

~~~yaml
contract_version: "1.0.0"
backend:
  preferred: "pypowsybl"
  fallback: "veragrid"
  allow_implicit_fallback: false
  require_pinned_version: true
delivery:
  cgmes_family: "2.4.15"     # or "3.0"
  mode: "UNSOLVED_IMPORT"    # or "SOLVED_IMPORT"/"CGM_UPDATE"
  profiles: ["EQ", "SSH"]
  if_tp_absent: "DERIVE_ONLY_IF_PROVEN"
  if_sv_absent: "NO_REFERENCE_PASS"
  boundary_policy: "EXCHANGE_VERSION_AWARE"
canonical:
  schema: "iosn-m0-can/1.0.0"
  store: "sqlite-v1"
projection:
  target: "PYPSA_DETAILED"
  operating_state_id: "<explicit-state-id>"
  mapping_policy_id: "transmission-positive-sequence/v1"
  components:
    ACLineSegment:
      target: "Line"
      transform: "line_total_ohm_s_to_pypsa/v1"
      on_missing_critical: "BLOCK"
    PowerTransformer:
      target: "Transformer"
      transform: "transformer_end_and_tap_to_2port/v1"
      on_nonrepresentable: "UNSUPPORTED"
    ThreeWindingTransformer:
      target: "ThreeBranchStar"
      transform: "three_winding_kron_equivalence/v1"
      synthetic_country_code: null
export:
  mode: "UPDATE_IMPORTED"
  allow_profiles: ["SSH"]     # SV separately if eligible
  allowed_write_rule: "pinned-backend-qualified-allowlist/v1"
  require_source_graph: true
  require_semantic_graph_diff: true
quality:
  unauthorized_default: "BLOCK"
  log_attribute_provenance: true
~~~

**Schemaänderung:** Canonical Major bei PK-/FK-/Einheiten-/Semantikänderung; Minor bei additiven optionalen Feldern; Patch für redaktionelle Korrekturen. Regel- und Funktionsversionshash gehen in `mapping_policy_hash` ein; Pinning von Backend/Core/Python/PyPSA/CIM-Profile und Unit-/CRS-Verträgen im Reproduktionsmanifest. Beim Backendupgrade wird ein neues Qualifikationsprotokoll mit T-01…T-24 je betroffener Capability erzeugt.

## 8. Persistenz, Reproduzierbarkeit und Skalierung

**Entscheidung für den ersten PoC:** `sqlite3` (Python-Standardbibliothek) als normiertes, referenzintegritätsprüfbares Canonical-/Provenienz- und Revisionsregister; originale RDF/XML/ZIP-Bytes im **content-addressed, immutable** Dateispeicher (SHA-256), mit separatem Manifest (JSON). Für die PyPSA-Ansicht werden DataFrames beim Abruf erzeugt; optionaler Cache als Parquet/Arrow erst nach Datenmengen-/Kompatibilitätsnachweis, **nicht** zweite fachliche Quelle. Keine zusätzliche dauerhaft betriebene Fuseki-Instanz allein wegen dieser Architektur. SQLite ist ein **PoC-Persistenzprofil**, nicht die Festlegung eines endgültigen verteilten Datenbankprodukts.

**Wichtig:** die SQLite-Verwendung und ein mögliches Parquet-Cacheformat sind neue Modul-0-Entscheidungen, keine Behauptung einer extern vorhandenen Datenbank. Speicherschemas müssen referenzielle Beziehungen/PKs, nullable Pflichtfeldregeln, Versionen und Opaque-Graph-Referenzen des logischen `30`-Vertrags validieren; unaufgelöste Quellkonflikte bleiben Blocker. Jede Dataset-/Variant-Datei und der Exportbericht werden gehasht. Modelle mit realen Netzrechten werden nicht ins öffentliche Repository eingecheckt.

**Snapshot/Persistenz-Lebenszyklus:** Backup der unveränderten Rohdateien → importer/BackendSession → staging CanonicalRevision → QA → Commit/Manifest-Pointer atomar veröffentlichen. Eine im M2 benannte zukünftige ACPF-/LPF-/Reduction-View ist keine automatisch wiederherstellbare Original-Topologie. Cache-Dateien sind jederzeit aus Archive, Dataset- und Mappingversion reproduzierbar.

**Skalierungsrichtlinie:** Ein Referenz-CGM um mehrere Tausend Busse und Multi-IGM-Grenzen ist für spätere Benchmarks vorgesehen; Leistungszeit und RAM sind **noch unbekannt**. Bei M4 messen: Parse/Backend-RAM, PyPowSyBl-/Java-Native-Ressourcen, Canonical-Write und Join-Kosten, PyPSA-Projektion, Export-Staging, peak RAM; lange RDF-Graph-Zeitreihen und CFD dürfen nicht in der Kern-PyPSA-Tabelle dupliziert werden. Dateneingaben müssen Größe/Zip-Bomb-/Pfad-/XML-Entity-Limits und sichere temporäre Verzeichnisse beachten; XML-Parsing übernimmt die geprüfte externe Bibliothek, ihr Verhalten ist durch Fixture-/Fuzz-Gates zu prüfen.

## 9. Vertrag zum vorhandenen Modul 1

**Pflichtartefakt:** `DetailedNetworkReference v1` enthält `network_revision_id`, `source_set_hash`, `mapping_policy_hash`, ggf. `operating_state_id`, aktive orientierte Bus-/Branch-Mengen, effective `x_pu` mit Grundlage, 3W-Source-Mapping, PST-Offset, HVDC-Terminalmodell/Flows, normal-/temporär-/direktionale Grenzwerte, Country/Boundary-IDs und `m0_sidecar`. Zeitreihen/Dispatch/Wetter/Busmaps sind keine M0-Daten. Reale grenzüberschreitende Zweige müssen in der Detailtopologie bleiben, auch wenn später Länder separat geclustert werden.

**Aktueller Codebefund:** Der bestehende `src/tyndp_reduce/pypsa_adapter.py` verwirft Transformatoren, Links, Storage und mehrdimensionale/mehrinselige Sonderfälle. Somit folgt aus `PYPSA_ACPF_READY` oder `PYPSA_LPF_READY` keinesfalls `REDUCTION_ADAPTER_READY`. Die Erweiterung des bestehenden Reduktionsadapters ist **späteres Modul-1-Implementierungsmakro**, nicht ein versteckter Teil des CGMES-Format-Backends.

## 10. Abnahme für M2 und Referenzverzeichnis

**M2 ist statisch komplett**, wenn `40`, `60` und `70` dieselben Begriffe verwenden, K-01…K-07 eindeutig behandeln, allen 39 MUSS-Anforderungen eine Modulverantwortung zuordnen, die 24 Tests referenzieren und sämtliche unqualifizierten Upstream-Annahmen als PoC-Gates kennzeichnen. **Nicht** Teil des M2-Abschlusses: lauffähige Parserintegration, PyPSA-Netzpfad, exportierte konforme RDF/XML-Lieferung oder bestandenes AC-PF-/Round-Trip-Experiment.

**Verbindliche Inputs:** [10 Requirements](10_REQUIREMENTS.md), [20 Backend](20_BACKEND_ASSESSMENT.md), [30 Canonical](30_CANONICAL_DATA_CONTRACT.md), [50 Validation](50_VALIDATION_CONTRACT.md), [00 S-GOV](00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md).

**Externe geprüfte öffentliche Referenzen:** [PyPowSyBl Netzwerk-API](https://github.com/powsybl/pypowsybl/blob/main/docs/user_guide/network.rst), [PowSyBl CGMES Import](https://github.com/powsybl/powsybl-core/blob/main/docs/grid_exchange_formats/cgmes/import.md), [PowSyBl CGMES Export](https://github.com/powsybl/powsybl-core/blob/main/docs/grid_exchange_formats/cgmes/export.md), [PyPSA-Komponentenattribute](https://github.com/PyPSA/PyPSA/tree/master/pypsa/data/component_attrs), [VeraGrid CGMES](https://github.com/SanPen/VeraGrid/tree/master/src/VeraGridEngine/IO/cim/cgmes). Diese beweglichen öffentlichen URLs werden **nicht** als unveränderliches Implementierungs-Version-Pin interpretiert: der spätere PoC pinnt installierbare Releases/Commit-SHAs und dokumentiert deren API-/Betriebsverhalten.
