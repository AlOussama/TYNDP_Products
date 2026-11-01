# S-GOV M2/M3 — Konsolidierter normativer Reparaturvertrag

**Projekt:** IoSN / TYNDP / PyPSA, Modul 0 CGMES ↔ Canonical ↔ PyPSA.
**Datum:** 2026-11-01. **Status:** NORMATIVE_DESIGN_REPAIRS_SPECIFIED_NOT_EXECUTED.
**Basis:** M2 0275f48231a0794bea324b9cab34700bb0de8f5b; unabhängiger M3-Bericht [80_INDEPENDENT_ARCHITECTURE_REVIEW.md](80_INDEPENDENT_ARCHITECTURE_REVIEW.md), ea62050a867c27036552af28d3e0102a8689f4ec.
**Versionsentscheidungen:** IOSN-M0-CAN/2.0.0 als Breaking-Korrektur der noch nicht produktiv implementierten CAN/1.0.0; DetailedNetworkReference/1.0.0; M0-PUBLISH/1.0.0; M0-EXPORT-ROUTES/1.0.0.
**Nicht Teil dieser Korrektur:** produktive Implementierung, Testausführung, CGMES-/PyPSA-/Lastfluss-/Export-Qualifikation oder Merge nach main.

## 0. Vorrang und Nachvollziehbarkeit

Dieses Dokument ist die **einzige normative Sollfassung der sieben M3-P1-Korrekturen**. Es ergänzt und präzisiert 40/60/70 und überschreibt *nur die explizit hier widersprechenden Regeln* der historischen Originaldokumente 30/50 sowie die unpräzisen Stellen in 40/60/70. Die Quellenberichte 00/10/20/30/50 und der unabhängige Bericht 80 bleiben unverändert. Die physikalischen Formeln, 48 REQs mit 39 MUSS, K1–K7, ADR-001…009 sowie die T-01…T-24-Test-IDs bleiben vollständig erhalten. Ein Verweis auf das frühere Canonical-v1-Tabellenregister ist nun als **30 plus dieses CAN/2.0.0-Delta** zu lesen. Für den externen CGMES-Austausch gelten jeweils die zutreffenden IEC-/ENTSO-E-Profile und Exchange-Policies; dieser interne Vertrag ist kein externer Konformitätsnachweis.

Sämtliche unten angegebenen Methoden/Porttypen sind **neue Implementierungsspezifikationen des Modul 0**, keine nachgewiesenen Funktionen des externen Backends. Die M3-Evidenzklassifikation D/C/T/P/U bleibt verbindlich.

## 1. M3-P1-01: Source-Identität und Occurrences, CAN/2.0.0

**source_entity_key** = (qualified_identity_namespace, identity_kind, identity_value). identity_kind ∈ {MRID, RDF_SUBJECT}. qualified_identity_namespace dokumentiert Authority/Exchange/CIM-Familie und benötigten Modellkontext, **nicht den Profilnamen EQ/SSH/TP/SV**. Über Profile wiederkehrende logisch identische Quellobjekte haben genau eine source_entity, aber mehrere source_occurrences. Widersprüchliche Klassen-/Authority-/Identity-Kollisionen werden BLOCK, niemals last-file-wins.

**Identitätsräume und deterministische IDs:**
- source_entity_id = versionierter Hash des qualifizierten source_entity_key; asset_id = stabiler fachlicher Source-Equipment-Key, soweit belegt.
- source_object_id = Hash(source_revision_id,source_entity_id), unveränderlicher Datensatz einer bestimmten Originalrevision.
- source_occurrence_id = Hash(source_object_id,source_model_id,profile_uri,source_file_sha256,graph_scope_id,rdf_subject,subject_ordinal). Profile/File/Graph sind **Occurrence-**, nicht logische Entity-Dimensionen.
- source_mrid darf NULL sein. Für Objekte ohne mRID bleibt original rdf_subject verpflichtend. Kein historisches mRID aus Hash, Backend-ID, Name oder synthetischem PyPSA-Objekt erzeugen.
- RDF-BlankNodes werden mit Originallexem, Graph-/File-Hash und lokalem bnode-Scope verankert; die Identität gilt nur innerhalb dieser unveränderlichen Graph-/Revisionssphäre. Ohne nachgewiesene RDF-Kanonisierung wird keine stabil idempotente Cross-Serialization-BlankNode-Identität behauptet; eine nicht eindeutig inverse Änderung ist BLOCK.
- Backend-ID, Original-mRID, RDF-subject, source_object_id, canonical asset_id, synthetic view_id und exportseitig *neu generierte* CGMES-mRID sind strikt getrennte Identitäten. Aliase und Ähnlichkeiten sind kein Joinbeweis.

**Verbindliches Tabellen-/Constraint-Delta; S=nonempty String, U=UUID/StringID, H=SHA-256, E=versioniertes Enum, J=validiertes JSON, B=bool, F=endlicher float64, TS=UTC-Zeitstempel. NULL ist kein Nullwert; absence_reason ist verpflichtend.**

| Tabelle | PK / Unique | FK und Pflichtfelder | Nullable / Hard Constraints |
|---|---|---|---|
| source_model_sets | PK source_model_set_id:U | cgmes_family:E, exchange_policy_id:S, equipment_boundary_manifest_hash:H, authority_set:J | Nur Original-EQ-/Boundary-Hierarchie; kein SSH-/Mappingwechsel allein |
| source_revisions | PK source_revision_id:U | FK source_model_set_id, source_graph_hash:H, model_header_hashes:J | parent_source_revision_id:U? nur bei neuer struktureller Quelle |
| source_entities | PK source_entity_id:U; UNIQUE (qualified_identity_namespace,identity_kind,identity_value) | source_class_uri:S, identity_rule_version:S | source_mrid:S? **nur bei real geliefertem MRID**; Klasse/Authority-Kollision BLOCK |
| source_objects | PK (source_revision_id,source_object_id); UNIQUE (source_revision_id,source_entity_id) | FK source_revisions/source_entities, source_class_uri:S, is_boundary:B | source_mrid:S? nullable; NULL bei RDF_SUBJECT/BlankNode |
| source_occurrences | PK source_occurrence_id:U; UNIQUE (source_object_id,source_model_id,profile_uri,source_file_id,graph_scope_id,rdf_subject,subject_ordinal) | FK source_objects/source_files/model_headers; source_model_id:S, profile_uri:S, graph_scope_id:S, rdf_subject:S, subject_ordinal:I | is_blank_node:B, bnode_local_id:S?, original_rdf_lexeme:S?; doppelt widersprüchlicher Subject-Record BLOCK |
| source_relations/raw_attributes | bestehende Quell-PKs und **FK source_occurrence_id** | RDF-Prädikat, Objektwert/-URI, Source-Referenz, File-/Profilautorität | unresolved target nur ausdrücklich als externe Boundary-Referenz mit bekanntem Scope |
| source_hierarchy | PK (source_revision_id,source_entity_id,relation_kind,parent_source_entity_id) | originärer RDF-Relationenbeleg und FK Source-Entities; relation_kind ∈ {EQUIPMENT_CONTAINER,VOLTAGE_LEVEL,SUBSTATION,REGION,COUNTRY,TERMINAL_SOURCE} | fehlende/mehrdeutige Country-/Substation-Beziehung ⇒ Quality-Event, kein Vertreter-IIDM-Fallback |
| terminal_source_origin | PK (source_revision_id,source_terminal_entity_id) | FK Originalterminal, original_equipment_id:U, original_terminal_order:I, original_relation_refs:J | source_connectivity_node_id:U?, source_topological_node_id:U?, source_substation_id:U?, source_voltage_level_id:U?, source_country_code:S? **nur mit Quellenbeleg** |
| buses | PK (projection_id,bus_id); FK projection_id | bus_role:E={REAL,SYNTHETIC_3W_STAR}, v_nom_kv:F, island_id:U, origin_refs:J, country_resolution_status:E | REAL: original_topological_node_ref:U und Country-FK bei M1-/Country-READY; SYNTHETIC_3W_STAR: source_transformer_id:U, country_code=NULL, source_geo=NULL, excluded_from_country_clustering=TRUE |
| projection_bus_source_map | PK (projection_id,bus_id,source_terminal_entity_id,origin_relation_kind) | FK bus/source-terminal, RDF-Provenienzreferenz | synthetischer Sternbus braucht **kein** erfundenes Originalterminal; eigener SourceTransformer-Parentanker |

Die bisherige source_objects.source_mrid-Pflicht und der profilhaltige source_key aus 30/1.0.0 sind **explizit aufgehoben**. Der bisherige unbedingte Country-FK für alle Busse ist nach **bus_role und beanspruchter Capability** eingeschränkt. Reale, für Landes-/Reduktionsanalyse freigegebene Busse haben genau einen verifizierten country_code aus versioniertem Register; bei Multi-Country-/Mehrdeutigkeitszuordnung wird country_code=NULL, origin_country_codes bleiben pro Terminal erhalten und COUNTRY-/REDUCTION-READY bleibt BLOCKED. Sterne bleiben country_code=NULL und besitzen keine erfundene Geometrie. Ein länderübergreifender Zweig wird physikalisch nicht aufgetrennt; seine beiden Endport-Länder sind im Source- und View-Mapping erhalten. 

**T-04:** gleiche mRID across EQ/SSH, RDF-only/SV ohne mRID, BlankNodes in verschiedenen Graphen, gleiche RDF-Lexeme unterschiedlicher Authorities, Klassenkollision und unbekannte Attribute. **T-10:** realer Country-Konflikt und synthetischer 3W-Stern ohne Country. Das Schema ist vor erster physischer Umsetzung als CAN/2.0.0 anzulegen; keine unbemerkte Migration aus einem später implementierten CAN/1.

## 2. M3-P1-02: NODE_BREAKER und BUS_BRANCH mit Source-Hierarchie

**topology_domains:** PK (source_revision_id,topology_domain_id), topology_kind:E={NODE_BREAKER,BUS_BRANCH}, source_model_id, voltage_level/authority scope, supplied_tp_profile_ref?, derivation_policy_id?, integrity_status. Mehrere Domains in einem CGM sind zulässig, Grenzübergänge nur über originale Equipment/Terminal-/Boundary-Beziehungen.

**terminal_connections:** PK (canonical_revision_id,operating_state_id,source_terminal_entity_id), FKs topology_domain/terminal/source, connected:B, resolved_topological_node_id:U, resolved_bus_id:U, connection_origin:E={EQ_CN_DERIVED,EQ_CN_TP_VERIFIED,TP_DIRECT}, original_connectivity_node_id:U?, original_tp_node_id:U?, original_relation_ref:S. Ein aktives Terminal hat genau einen aktuellen, belegten Bus. Anschluss-FKs sind je OperatingState zu prüfen, kein globales stilles Remapping.

| Source-TopologyKind | Normative Resolver-Regel | Pflicht-/Negativbedingung |
|---|---|---|
| NODE_BREAKER | Terminal→ConnectivityNode aus EQ; eigene Switch.open, normalOpen, Equipment.inService, Terminal.connected aus aktuellem Zustand; ConnectivityNodes nur über geschlossene leitfähige Switches verbinden. Leitungen und Transformatoren bleiben Impedanzzweige. | TP, falls geliefert, gegen berechnete Topologie abgleichen. TP fehlt: deterministische nachgewiesene EQ/SSH-Ableitung erlaubt; andernfalls BLOCK. |
| BUS_BRANCH | Originalterminal→TopologicalNode über geliefertes TP und Original-RDF-Referenzen. **Keine künstlichen ConnectivityNodes.** | TP ist zwingend; fehlt TP: BLOCK_TOPOLOGY_MISSING_TP. Keine fiktive EQ/SSH-Topologieableitung aus nicht vorhandenen ConnectivityNodes. |
| MIXED_DELIVERY | Domains separat resolven, dann referenziell per Originalequipment-/Boundary-Port zusammenführen; AC-Islands ermitteln. | unklare Cross-Domain-/Boundary-FKs ⇒ BLOCK; HVDC verschmilzt keine AC-Islands. |

**Originalhierarchie:** PowSyBl kann ursprüngliche CGMES-Substations und VoltageLevels in IIDM zusammenfassen. Daher sind repräsentative IIDM-Station-/Level-Namen/Zuordnungen **nicht** autoritativ für Source-Station, Landeszuordnung oder Original-Authority. Country und Substation je realem Endport stammen aus source_hierarchy/terminal_source_origin mit RDF-Relationswitness. Fehlt diese Herkunft, kann ein eng begrenzter Import-Preview existieren, jedoch kein auf Landes-/Originalhierarchie angewiesenes READY, kein identitätstreuer Update-Export. Mehrdeutige Cross-Border-Knoten bleiben als ungelöster Country-Konflikt sichtbar und werden nicht nach Koordinate/Alphabet aufgelöst.

**Tests/Fälle:** F-02/T-07/T-08 mit BB+TP, BB ohne TP, NB mit offenem/geschlossenem Switch und Konflikt-TP; F-04/T-03/T-10 mit Multi-IGM, Authority und zusammengeführten IIDM-Stationen über verschiedene ursprüngliche Country-Endports.

## 3. M3-P2-02: Getrennte Revisionsidentitäten

| Logischer Schlüssel | Eingangs-Hash und Bedeutung | Änderung |
|---|---|---|
| source_model_set_id | Equipment-/Boundary-Datei-/Exchange-Metadatenhash, sortiert | anderes ursprüngliches Netz-/Boundary-Modell |
| source_revision_id | source_model_set_id + Original-EQ-/Boundary-Graph-/Headerhash | andere Quellstruktur/Herkunft, **nicht** bloß SSH oder andere PyPSA-Projektion |
| operating_state_id | source_revision_id + SSH-/SV-Stategraphhash + Scenario/Time/State-Policy | geänderter betrieblicher Zustand |
| canonical_revision_id | source_revision_id + operating_state_id + CAN/2.0.0 + Normalisierungs-/Identity-/Topology-Policy + resultierender Tabellenhash | neue Canonical-Normalisierung, nicht neue originale EQ-Quelle |
| projection_id / electrical_view_id | canonical_revision_id + FunctionRegistry-/Mapping-Hash + gewähltes elektrisches Modell/Target-Version | andere elektrische Darstellung; Source/State bleiben unverändert |

Die frühere **network_revision_id** aus 30/40 ist ausschließlich ein deprecated Alias des neuen **canonical_revision_id**, niemals ein Hash über unveränderte Originalquelle *und* willkürlich geänderte Projektionsfunktion. source_entity_id/asset_id sind source-key-stabil; view_id ist projection_id-/Port-/Funktions-gebunden. Deterministischer Hash: versioniertes kanonisches UTF-8-/JSON-Encoding mit Schlüsselsortierung, typisierter NULL-/Einheiten-/Zahlenrepräsentation, keine Importzeitstempel/Backend-Reihenfolgen, keine NaN/Inf. Encoding und Testvektoren müssen vor der Implementierung gepinnt werden.

## 4. M3-P1-03: Eigenständiges, exportunabhängiges Projection-Loss-Ledger

| Tabelle | Schlüssel und FK | Pflichtangaben / Bedingungen |
|---|---|---|
| electrical_projections (append-only) | PK projection_id; FK canonical_revision_id, operating_state_id | mapping_policy_hash, function_registry_hash, target_model_kind, target_pypsa_pin, status |
| projection_witnesses (append-only) | PK witness_id; FK projection_id | witness_kind:E={UNIT,TOPOLOGY,YBUS,KCL,PQ_SIGN,HVDC_LOSS,TAP_SHIFT,LIMIT,ORIGIN,OTHER}, function_id/version, input_hashes, test_or_derivation_id, tolerance_policy_id, evidence_origin:E={DECLARED,STATIC,EXECUTED}, result_status:E, measurement_ref? |
| projection_quality (append-only) | PK (projection_id,quality_item_id); FKs projection_id, source_object_id?, view_id?, witness_id? | component_type, field_or_relation, capability_scope, function_id/version, mapping_policy_hash, exactness_class:E={EXACT,APPROX,UNSUPPORTED}, quality_status, reason, witness_id? oder missing_witness_reason, approximation_domain?, physical_effect?, approval_policy_id? |
| export loss_manifest (bestehende Tabelle) | PK (transaction_id,loss_item_id); FK export_transaction; optionale Referenz (projection_id,quality_item_id) | Export-eigene Feld-/Profilverluste; existiert nur bei Export, **nicht** als Parent des ProjectionQuality-Ledgers |

Eine **ElectricalView besitzt immer** ein eigenes revisionsgebundenes Quality-/Loss-Manifest, selbst ohne Export. Jede gemappte elektrisch relevante Feld-/Relationen-Wirkung wird nach Policy erfasst. EXACT ist nur für eine **bezeichnete** physikalische Eigenschaft mit gültigem passendem Witness zulässig; STATIC/DECLARED belegen keine ausgeführten Zahlen. Bis zum tatsächlichen qualifizierten Witness lautet die ausführbare Freigabe NOT_ASSESSED/BLOCKED, die Designabsicht kann EXPECTED_EXACT heißen. APPROX erfordert benannte Domain, physikalische Wirkung und genehmigte Policy; unbekannte Wirkung ⇒ UNSUPPORTED. UNSUPPORTED sperrt die jeweilige betroffene Capability, nicht zwingend den verlustbewahrenden Raw-Import. T-12…T-20 prüfen die Loss/Witness-Coverage **ohne Export**, T-21/22 getrennte Exportmanifeste, T-24 die Reproduzierbarkeit. Das Sidecar exponiert dieses Ledger an Modul 1.


## 5. M3-P1-04 und P2-01: Qualifizierte Update-Exportstrategie statt implizitem Quick-CGM

### 5.1 ExportPlan, Strategie und tatsächliche Profile

| Route-ID | Nach Upstream-Dokumentation erwartete Ausgabe | Benötigte Preconditions | Releasebedingung |
|---|---|---|---|
| CGM_QUICK_SSH_SV | PowSyBl-CGM-Quick-Export erzeugt **SSH je IGM und ein gemeinsames CGM-SV**, ignoriert Profilselektion | qualifizierter neuer gelöster SV-Snapshot, SSH-/IGM-/CGM-/Authority-/Boundary- und Header-/Dependency-Nachweise | ausschließlich bei richtigem Profilset, qualifiziertem SV und erfolgreichem T-21/T-23/T-24-Graph-/Reimport-Witness |
| MANUAL_IGM_SSH | PowSyBl dokumentiert manuelle IGM-/Subnetwork-Profile-Exportfähigkeit; konkrete Python-Bridge, FullModel-/MAS-/Metadata-Weitergabe **nicht qualifiziert** | SSH-only gewünscht, vollständige IGM-Assembly, originaler EQ/TP/Boundary-Graph und geprüfte neue SSH-/DependsOn-/Supersedes-Header | vor Runtime-Witness: NOT_ASSESSED/BLOCK_EXPORT_UNPROVEN; erst nach belegter Python/Java-Bridge und T-21/T-24-Fidelity PASS |
| OTHER_QUALIFIED_ROUTE | ausschließlich später separat nachgewiesene äquivalente Backend-Operation | explizite neue Versions-/Profil-/Operations-ADR und Witnesses | niemals automatische Fallbackroute |
| NO_ROUTE | keine passende Upstream-Operation/Profilkombination verfügbar | beliebig | BLOCK, keine gekürzte/umbenannte oder scheinbar gelöste Ausgabe |

**ExportPlan/1.0.0** verlangt: route_id; backend_name/version; actual_upstream_operation; requested_profile_set; **known_producible_profile_set**; target_cgmes_family; source_revision_id; base_graph_hash; operating_state_id; changed_attributes; mutation_class; source-ID/inverse witness; per-IGM MAS/FullModel/DependsOn/Supersedes; produced_header_plan; semantic_graph_diff_scope; revision/CAS-token; exact export_loss_manifest; idempotency_key. Ein Unterschied von angefragten zu tatsächlich erzeugbaren Pflichtprofilen ⇒ BLOCK. Ein YAML-Parameter allow_profiles:[SSH] ist **kein Beleg**, dass PowSyBls Quick-CGM-Export nur SSH schreibt. Nicht automatisch den SV-Teil eines ungeeigneten Quick-Ergebnisses entfernen oder SV aus SSH/p_set fingieren.

**Änderungs- und Inverseprüfung:**

| mutation_class | Beispiele | M0 v1 Regel |
|---|---|---|
| STATE_NON_TOPOLOGY | ausgewählte P/Q-Setpoints und sonstige belegte SSH-Felder; Tap nur nach Ybus-/Portqualifikation | pro CGMES-Familie/Backend/Feld freigegebene Write-Allowlist, eindeutige Source-Inverse, Delta-/Graph-Witness |
| STATE_TOPOLOGY_AFFECTING | Switch.open, Terminal.connected, Equipment.inService, wenn Anschluss-/Inselverhalten betroffen | Default **BLOCK**; Freigabe erst mit separatem TP-Rebuild, Boundary-/Header-/Dependency- und Test-Witness |
| STRUCTURAL_EQ_TP | neue/gelöschte originale Terminals, Equipment, Connectivity, EQ-/TP-Struktur, ursprüngliche Authority | UPDATE_IMPORTED v1 **BLOCK**, nie stiller Originalnetz-Umbau |
| SYNTHETIC_CREATE | explizit neues künstliches CGMES-Equipment/Terminal-/FullModel-/Authority-Paket | nur CREATE_FROM_PYPSA, eigene Capability |

Ein bloßes Namenslabel darf keine Änderungswirkung verschleiern: ob eine STATE_NON_TOPOLOGY-Änderung effektiv topologieprägend wird, ist durch den betroffenen Source-Terminal-/TP-/Equipment-Kontext zu prüfen. Original EQ/TP/Boundary/GL/unknown-Tripel bleiben unverändert und werden gültig weiterreferenziert. Jede nicht eindeutige Star-/Link-/View-Inverse wird vor Backend-Write blockiert.

**Negativ T-21:** SSH-only-Delta ohne tatsächlich neu gelösten SV-Snapshot darf nicht über QUICK_CGM_SSH_SV als erfolgreiches SSH-only geliefert werden. MANUAL_IGM_SSH darf ausschließlich bei dokumentiertem Header-/MAs-/Reimport-/Graph-Witness ausliefern, andernfalls expliziter BLOCK. Neuer SV benötigt einen tatsächlich berechneten konsistenten Referenzzustand und T-23-Eligibility.

## 6. M3-P1-05: REQ-009/T-06 verbindlich ohne zweites Produktionsbackend

**Normative Entscheidung:** REQ-009 bleibt **MUSS**, T-06 bleibt ein zwingender Nachweis für unqualifiziertes CANONICAL_IMPORT_READY. T-06 benötigt zwei **unabhängig durch verschiedene CGMES-Parser-/Backendpfade erzeugte** Daten-Snapshots desselben semantisch identischen Fixtures, auf eine versionierte gemeinsame Canonical-Referenz normalisiert. Beispiel: primär PowSyBl und als reiner Prüfadapter eine minimal notwendige **read-only** VeraGrid-Quelle. Dieser zweite T-06-Feld-/Relationen-Prüfadapter muss **nicht** als vollständiger, dauerhaft gepflegter Fallback-Produktionsdienst implementiert werden.

Zwei Ansichten derselben PowSyBl-IIDM-Instanz, ein Mock, bereits kopierte Canonical-Tabellen oder zwei Abläufe über denselben Parser gelten **nicht** als unabhängige Parität. Identitäten/Einheiten/Relationships und deklarierte zulässige numerische Rundungen werden verglichen; die Prüfmenge und die Unterschiede werden als Hashes und per-field Diff geliefert. Der Nachweis gilt nur für konkret geprüfte Familien/Profile/Geräte-/Fixture-Scope.

| Phase | Ohne unabhängig ausgeführtes T-06 | Nach T-06 und allen sonst relevanten Gates |
|---|---|---|
| PoC-M1 PowSyBl-Import | CANONICAL_IMPORT_PROVISIONAL; REQ-009=NOT_ASSESSED; **kein** CANONICAL_IMPORT_READY-PASS | CANONICAL_IMPORT_READY ist scoped und kann PASS erhalten |
| CANONICAL_BACKEND_PARITY | NOT_ASSESSED | PASS nur für geprüfte Gerät-/Versions-/Profil-Scope |
| VeraGrid Runtime-Fallback | nicht qualifiziert | weiterhin separate Adapter-/Full-Workload-Qualifikation, **kein** Produktions-PASS durch T-06 |

Ein PoC-M1 mit beanspruchtem Import-READY hat daher einen verpflichtenden unabhängigen **minimalen read-only T-06-Snapshot-/Adapter-Witness**. Ist er technisch noch nicht realisierbar, bleibt der Import nur PROVISIONAL; die bestehende REQ-MUSS-Klasse wird **nicht** heruntergestuft. Eine Änderung der Anforderung braucht gesonderte ausdrückliche Owner-Entscheidung, geänderten REQ-Vertrag und entsprechend versionierte Test-/Capability-Definition.

## 7. M3-P1-06: Ein autoritativer Commitpunkt und Crash-Recovery

**Storage-Profil M0-PUBLISH/1.0.0:** Unveränderliches content-addressed Original-/Export-/Manifest-Archiv und SQLite als **einzige Autorität der Veröffentlichung**. SQLite-FK-Transaktionen allein machen **keine** Dateien oder ZIP-Archive atomar; das folgende Write-Ordering ist verpflichtend. Für die erste Umsetzung wird ein qualifiziertes lokales FS mit nachgewiesenem durable write/rename und SQLite-WAL plus geeigneter synchronous-Policy vorausgesetzt. Cross-filesystem/network-/Cloud-Writes benötigen eigenständig überprüftes Storage-Profil. Öffentliche Konsumenten dürfen **nur** per SQLite-COMMITTED-Pointer lesen, nie direkt aus dem Stage-Verzeichnis.

**Sechs Schritte:**

1. **PREPARE:** Schreibe eine unter SQLite eindeutig identifizierte Transaktion mit request_payload_sha256, idempotency_key, expected_active_revision und expected_pointer_version. Gleicher Key + identischer Payload liefert dasselbe Ergebnis; gleicher Key + anderer Payload ⇒ BLOCK_IDEMPOTENCY_COLLISION.
2. **STAGE:** Baue unveröffentlichte Original-/Canonical-/Projection-/Exportdateien; validiere Profil-/Header-/Loss-/Identity-/Graph-/Quality-Gates auf den tatsächlich gestagten Bytes. Eingabe-Archive nur mit sicheren Größen-/Traversal-/XML-Entity-Policies entpacken.
3. **DURABLE BLOBS:** Schreibe SHA-256-adressierte Blobs in eingeschränktem finalen Blobroot; verifiziere Länge/Hash und sichere Datei/Parent-Durability (file- und wo verfügbar directory-fsync). Nur verifizierte Same-Filesystem-Atomic-Renames zulassen; unbewiesene Betriebs- oder Plattformsemantik ⇒ QUAL-OPS nicht freigegeben.
4. **DURABLE MANIFEST:** Manifest enthält **alle** notwendigen Blobhashes, source/reference IDs, Versions-/Backend-/Profile- und QA-/Diff-/Loss-Witnesses; Manifest vollständig schreiben, hashverifizieren und durabel abschließen **vor** Pointeränderung.
5. **COMMIT:** SQLite BEGIN IMMEDIATE und transaktionale Compare-and-Swap-Prüfung (expected base revision + Pointerversion); validiere Blob-/Manifest-Präsenz; schreibe COMMITTED-Record und schalte **als letzte sichtbare Operation in derselben DB-Transaktion** den einzigen aktiven Revisions-/Delivery-Pointer; danach SQLite COMMIT. CAS-Verlierer => BLOCK_CONCURRENT_REVISION ohne Pointerwechsel. **Der erfolgreiche SQLite-COMMIT dieses Pointers ist der einzige Publikationszeitpunkt.**
6. **READ/RECOVER:** Leser akzeptieren ausschließlich COMMITTED-Pointer und verifizieren Manifest/Blob-Verfügbarkeit. Crash **vor** DB-COMMIT: alter Pointer gültig, unreferenzierte stage/finale Blobs werden erst nach Recovery-/Lease-/Grace-Prüfung gesammelt. Crash **nach** DB-COMMIT: vollständiger neuer Manifeststand gültig, Retry mit gleichem Idempotenzschlüssel findet denselben Commit. Fehlender/hashdefekter Blob unter COMMITTED ⇒ CORRUPT_COMMIT/FATAL (kein stiller Rückfall).

| Crash-/Konfliktfenster | Sichtbarkeit und Failure-Injection-Nachweis |
|---|---|
| Vor/during Staging | alter Pointer; T-05/T-24 |
| Nach Blob-Schreiben, vor Manifest | alter Pointer; orphaned Blobs erlaubt; T-05/T-21 |
| Nach Manifest, vor DB-COMMIT | alter Pointer; Manifest nicht öffentlich; T-05/T-22 |
| Zwei konkurrierende Writer gleicher Base | höchstens einer committed; CAS-Verlierer BLOCK; T-05/T-21 |
| Nach Commit, vor Client-Antwort | neuer vollständiger Pointer; gleicher Retry ⇒ gleiche Delivery; T-21/T-22/T-24 |
| Gleicher Idempotenzschlüssel, anderer Payload | BLOCK; T-05/T-24 |
| Hashdefekt beim committed Manifest/Blob | FATAL, kein als READY berichtetes Teilpaket; T-24 |

Die Operationen publish_import_revision, publish_projection und publish_export verwenden **dasselbe** transaktionale Protokoll und erhalten unterschiedliche Capability-Freigaben; sie dürfen kein gemeinsam unkontrolliert mutierbares globales Netz halten. Nicht referenzierte Blobs werden erst nach Haltbarkeits- und Writer-Lease-Check gelöscht. Storage-/Filesystem-Garantie und Idempotenzalgorithmus sind im M4-Setup zu testen; **keine** ausgeführte Atomicity-Evidenz wird hier behauptet.

## 8. M3-P1-07: DetailedNetworkReferenceV1 — getypter M0→M1-Vertrag

**Schema-ID:** iosn-m0-detailed-network-reference/1.0.0. S=String, U=UUID/StringID, H=SHA-256, F=finite float64, B=bool, E=versioniertes Enum, J=validiertes JSON, TS=UTC-ISO-8601, NULL ausschließlich mit absence_reason. Das Modell ist eine **unveränderliche stationäre Netz-/Snapshot-Referenz**, nicht Zeitreihen-/Wetter-/Dispatchdaten und nicht eine Reduktions-Busmap. DNR v1 ist getrennt von CAN/2.0.0 versioniert.

### 8.1 Metadaten und Einheiten

| Tabelle | Pflichtfelder mit Typ | Nullable/FK/Regel |
|---|---|---|
| metadata (ein Datensatz) | schema_version:S="1.0.0"; reference_id:U; source_model_set_id:U; source_revision_id:U; operating_state_id:U; canonical_revision_id:U; projection_id:U; source_set_hash:H; mapping_policy_hash:H; function_registry_hash:H; backend_name_version:S; pypsa_version_pin:S; unit_schema_id:S; source_graph_manifest_sha256:H; sidecar_manifest_sha256:H; qa_manifest_sha256:H; capability_manifest_sha256:H; snapshot_kind:E | scenario_time:TS? nur wenn Quelle vorhanden; alle IDs referenzieren *dieselbe* Source-/State-/Projection-Hierarchie |
| system_bases | basis_id:U; s_base_mva:F>0; frequency_hz:F>0; voltage_convention:E=LINE_TO_LINE_RMS; phase_unit:E=DEG; p_unit=MW; q_unit=MVAR; branch_impedance_unit=OHM; shunt_admittance_unit=SIEMENS | Keine stillschweigende globale 100-MVA-Annahme |
| per_device_bases | PK basis_id:U; FK equipment_or_view_id:U; purpose:E={LINE_EFFECTIVE_X,TRANSFORMER_RATING,AC_LF,DC_LPF}; u_base_kv:F>0, s_base_mva:F>0, z_base_ohm:F>0, rule_version:S | transformer winding_end_number:I?, rated_u_kv:F?, rated_s_mva:F?; ohne belegte Base kein LPF-READY |
| capabilities | PK capability_code:E; status:E={PASS,CONDITIONAL_WITH_NAMED_GAPS,BLOCKED,NOT_ASSESSED}; evidence_manifest_sha256:H; limitations:J | ein STATIC_ONLY-Dokumentationsbefund darf nicht Runtime-PASS werden |

### 8.2 Elektrische Komponenten und Sidecar

| Tabelle | PK/FK/Pflicht | Nullable- und physikalische Regeln |
|---|---|---|
| buses | PK bus_id:U; bus_role:E={REAL,SYNTHETIC_3W_STAR}; v_nom_kv:F>0; FK island_id→ac_islands; is_active:B; source_origin_refs:J; country_resolution_status:E | REAL: source_topological_node_id:U, source_substation_refs:J, country_code:S für M1 COUNTRY_READY, sonst NULL/Block. STAR: source_transformer_id:U, country_code=NULL, source_topological_node_id=NULL, geo=NULL, excluded_from_country_clustering=TRUE |
| ac_islands | PK island_id:U; active_bus_refs:J; slack_policy_id:S; topology_quality:E | HVDC verbindet AC-Islands nicht synchron; LF/LPF-Slackfähigkeit separat qualifiziert |
| ac_branches | PK view_branch_id:U; FK bus0/bus1→buses; branch_kind:E={LINE,EQUIVALENT_BRANCH,TRANSFORMER_2W,THREE_WINDING_ARM}; is_active:B; source_equipment_id:U; terminal_port_map:J; orientation_rule_id:S; electrical_model_id:S | terminal_port_map enthält originale Source-Terminals und bei Sternarm eindeutigen SYNTHETIC_PORT, nie gefälschtes Source-Terminal. LPF: x_pu_eff:F endlich und nonzero, basis_id:U, function_id/version Pflicht; AC: Ybus/r/x/g/b/Tap-Witness im Sidecar. Keine Datenelemente ohne qualified basis |
| transformer_effects | PK (view_branch_id,end_or_port_id); FK ac_branches; winding_end_number:I?; tap_side:E; tap_ratio:F>0; phase_shift_deg:F; control_status:E; effect_model_id:S | Portkonvention und Ratio-/Phasenrichtung bei jeder Transposition explizit. Unbekannter Step ⇒ UNSUPPORTED |
| pst_offsets | PK view_branch_id; FK ac_branches; p_offset_mw:F; oriented_from_bus_id:U; oriented_to_bus_id:U; signed_phase_shift_deg:F; offset_function_version:S; basis_id:U | Offset an richtiger bus0→bus1-Orientierung; kein stiller Null-Offset |
| injections | PK injection_view_id:U; FK bus_id→buses; source_equipment_id:U; kind:E={GENERATOR,LOAD,EXTERNAL,SHUNT,DC_TERMINAL}; p_inj_mw:F; q_inj_mvar:F?; is_active:B | p_inj_mw **positiv ins AC-Netz**. Positive Canonical-Load-Demand wird negatives p_inj; source_terminal_id:U? nur bei vorhandenem Originalport |
| hvdc_ports | PK (hvdc_system_id,converter_id,port_id); FK ac_bus_id→buses; source_terminal_id:U; p_ac_inj_mw:F; q_ac_inj_mvar:F?; loss_model_id:S; transfer_direction:E; model_class:E={PTP_LOSSLESS,PTP_DIRECTIONAL_LOSS,PORT_INJECTION,UNSUPPORTED}; quality_ref:S | Endport-/Converter-/DC-Herkunft belegt; P/Q/Verluste und Reverse-Flow je Modell/Witness. Keine AC-Island-Fusion |
| operational_limits | PK limit_id:U; FK source_equipment_id/source_terminal_id; quantity_value:F; unit:E; limit_kind:E; direction:E; terminal_port_id:U?; limit_type:E; normal_or_emergency:E; applicability:J; source_ref:S | acceptable_duration_s:F?, season:S?, valid_from/to:TS?, contingency_context:S?. Kein impliziter CurrentLimit→s_nom-Proxi ohne Spannungsbasis |
| view_source_map | PK (view_type,view_id,source_entity_id,source_role); FK source_entities; inverse_export_allowed:B; source_terminal_map:J | n:m-Abbildung transparent, synthetische Star-Ports als solche gekennzeichnet |
| projection_quality_refs | PK (projection_id,quality_item_id); FK projection_quality | Exportunabhängiges EXACT/APPROX/UNSUPPORTED + Witness; keine Implizit-PASS |
| sidecar_reference | PK sidecar_manifest_sha256:H; reference_id:U; source_archive_ref:S; canonical_tables_ref:S; hierarchy_ref:S; boundary_ref:S; rdf_identity_ref:S; operational_limits_ref:S; projection_quality_ref:S | alle Artefakte immutable/hashverifiziert; PyPSA ohne Sidecar ist **kein** volles DNR v1 |

**Snapshot-/Port-/FK-Invarianten:** Alle Referenzen gehören zur selben (source_revision_id, operating_state_id, canonical_revision_id, projection_id). Jeder aktive reale Port hat belegte Terminal-/Busbeziehung, ein 3W-Original genau drei qualifizierte Star-Arms bei einem synthetischen Bus, HVDC-Ports behalten original AC-Endpunktländer und Verlustbilanz; Limits bleiben mehrfach je Richtung/Dauer/Terminal. Fehlende Originaldaten werden NULL/MISSING, nie als 0, unendlich oder Default-Quelle ausgegeben. Die referenzierte Quell-/Betriebssituation ist vollständig eingefroren, während zukünftige Modul-1-Zeitreihen separat dieselbe Revision referenzieren.

**SemVer/Fingerprint:** Major für andere Pflichten, Units, Vorzeichen-/Portkonvention, Minor für additive optionale nullable Felder, Patch für redaktionelle Änderung. reference_id ist der deterministische Hash über schema_version, Source-/State-/Canonical-/Projection-ID, geordnete Tabellen- und Sidecar-Manifesthashes, Unit-/Function-/Mapping-/Backend-BOM und Capabilitypolicy; kanonische Hashencoding-Version in metadata. Änderungen der Projektionspolicy verändern reference_id, aber nicht den ursprünglichen Source-Key.

**M0→M1 Handshake:** M0 liefert DNR-v1-Manifest, PyPSA Detailed View, die komplette Sidecar-/Source-Map, gewünschte Capabilities und ComponentSupportMatrix. M1 prüft Schema-Major, alle Manifesthashes, Snapshot-/ID-/FK-, Origin-, Unit-/Port-/Basis- und Quality-Konsistenz sowie seine **tatsächlich** akzeptierten Gerätetypen. Nicht erkannte Transformer/3W/PST/HVDC/Storage/Mehrinseln dürfen niemals still gedroppt oder in ungetestete Proxies verwandelt werden; bei fehlender Fähigkeit explizit UNSUPPORTED_FOR_REDUCTION_ADAPTER/BLOCK mit Komponentenliste. Ein M0-DNR-v1-Export ist **nicht** REDUCTION_ADAPTER_READY; dieses Gate erfordert gesondert einen M1-End-to-End-Test, ohne M1-Quellcodeänderung innerhalb dieses Architekturmakros.

**T-20:** positiver line-only/single-island-Handshake mit x_pu_eff-/Rating-Basis, Bus-/Line-/State-ID; negative 2W, 3W, PST, HVDC, Storage, Multi-Island, fehlendes Country, unaufgelöste Limits, falsche Schema-/Snapshotversion und fehlende Source-/Basisprovenienz. Alle negativen Testfälle müssen REJECT statt silent Drop erzeugen.

## 9. M3-P2-03/P2-04: Negative Fixtures und spätere operative RunRelease

Die ursprünglichen 24 Tests T-01…T-24 bleiben **unverändert nummeriert**. Nachfolgende Unterfälle sind ausdrücklich Teil derselben künftigen Tests:

- F-02 / T-03,T-07,T-08: BUS_BRANCH mit/ohne TP; NODE_BREAKER offen/geschlossen; Mixed-Domain-/TP-Konflikte.
- F-04 / T-04: mRID-los RDF-only/SV, lokale BlankNodes, Multi-Occurrence, Authority-Kollision, originale Substation-/VoltageLevel-Mappings.
- F-04/F-06 / T-10: Merging von IIDM-Stationen trotz divergierender ursprünglicher Länder-Endports; synthetic-star NULL-country.
- F-07 / T-21,T-23: QUICK_CGM ohne passenden neu berechneten SV ⇒ BLOCK; MANUAL_IGM_SSH ohne validierte Headers/Dependencies/Bridge ⇒ BLOCK.
- F-07 / T-05,T-21,T-22,T-24: Stage-/Post-Blob-/Pre-Commit-/Post-Commit-Crash, Konkurrenz/CAS, Idempotenz, orphan-GC, Hashdefekt.
- T-12…T-20 ohne Export: Projection-Loss-Ledger/Witness-Coverage; EXACT ohne executed witness oder APPROX ohne geprüfte Domäne ⇒ kein READY.

Vor einer tatsächlich autorisierten M4-/PoC-Ausführung ist eine **versionierte operative Policy** zu veröffentlichen und zu pinnen: ZIP-/XML-Eingangsgröße, dekomprimiertes Größen-/Ratio-/Entrycount-Limit, Traversal-/Entity-/DoS-Schutz; CPU/Wallclock/Java-/Native-/RDF-Speichergrenzen und Prozessisolation; Timeouts/Cancel/BackendSession-Close; Filesystem-Durability, Restart/Recovery; Nutzungs-/Weitergaberechte der Netzdaten, insbesondere echte IGM/CGM; messbare Runtime-/Peak-RAM-/Multi-IGM-/6k+-Bus-Skalierungsziele. **Fehlt ein verbindliches Budget, das geprüfte Rechte-/Lizenzmanifest oder die verifizierbare Betriebsumgebung, bleibt das betreffende QUAL-OPS-PERF/SECURITY/DATASET-Gate NOT_ASSESSED/BLOCKED.** Keine Schwellenwerte aus bislang nicht ausgeführten Tests erfinden.

## 10. Closure-Matrix, Status und Governance-Grenzen

| Finding | Korrektur | Dokumentationsstatus |
|---|---|---|
| M3-P1-01 | §1 CAN/2.0.0 SourceObjects/Occurrences/Country-FK | SPECIFIED_FOR_STATIC_CHECK |
| M3-P1-02 | §2 duale TopologyKinds, Bus/Branch-TP, SourceHierarchy | SPECIFIED_FOR_STATIC_CHECK |
| M3-P1-03 | §4 eigenständiges revisionsgebundenes ProjectionQuality-Ledger | SPECIFIED_FOR_STATIC_CHECK |
| M3-P1-04 | §5 CGM_QUICK_SSH_SV versus MANUAL_IGM_SSH | SPECIFIED_FOR_STATIC_CHECK |
| M3-P1-05 | §6 REQ-009/T-06 zwingend, minimaler zweiter unabhängiger Testadapter | SPECIFIED_FOR_STATIC_CHECK |
| M3-P1-06 | §7 Filesystem/Blob/Manifest vor SQLite-CAS-Pointer, Recovery/Retry | SPECIFIED_FOR_STATIC_CHECK |
| M3-P1-07 | §8 vollständig typisierter DNR-v1-/Sidecar-/Handshake-Vertrag | SPECIFIED_FOR_STATIC_CHECK |
| M3-P2-01 | §5 Mutationsklassen | SPECIFIED_FOR_STATIC_CHECK |
| M3-P2-02 | §3 Revisions-/ID-Entflechtung | SPECIFIED_FOR_STATIC_CHECK |
| M3-P2-03 | §9 explizite Negativfixtures | SPECIFIED_FOR_STATIC_CHECK |
| M3-P2-04 | §9 operative, vor M4-RunRelease zu pinnende Policies | DEFERRED_WITH_OWNER_AND_BLOCK_GATE |

**S-GOV-Prüfpflicht vor dokumentarischem Architektur-Freeze:** sieben P1 in *einem* konsistenten normativen Vertrag, nachvollziehbar in 40/60/70 verankert; 48/48 REQ, 39/39 MUSS, T-01…T-24 und K1–K7/ADR-001…009 bleiben unverändert erhalten; kein P0 und keine unaufgelösten P1-Widersprüche; GitHub-Änderungen auf Dokumentation begrenzt. Der unveränderte unabhängige M3-Bericht mit REPAIRS_REQUIRED ist historische Evidenz; sein Befund wird nicht rückwirkend auf PASS umgeschrieben.

**Nicht impliziert:** ENTSO-E-/IEC-Konformität, CGMES 2.4.15/3.0 Imports, Round-Trip-Fidelity, Ybus-/ACPF-/LPF-Numerik, Write-API-Verfügbarkeit, Performance, Datei-Atomizitäts-Test-PASS oder REDUCTION_ADAPTER_READY. Diese bleiben auf zukünftige ausdrücklich zu autorisierende PoC-/M4-Ausführung bezogen und dürfen niemals durch eine bloße ARCH-STATIC-Entscheidung ersetzt werden.
