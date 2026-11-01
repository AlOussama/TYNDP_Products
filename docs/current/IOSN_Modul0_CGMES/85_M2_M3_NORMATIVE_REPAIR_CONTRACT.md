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

