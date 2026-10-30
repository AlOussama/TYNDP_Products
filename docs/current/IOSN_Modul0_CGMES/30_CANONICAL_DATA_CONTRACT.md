# R-M0-CGMES-CONTRACTS-1 — 30 Canonical Data Contract and Electrical Mapping

**Contract-ID:** IOSN-M0-CAN/1.0.0 · **Datum:** 2026-10-30 · **Status:** verbindliche interne fachliche Spezifikation, weder Parser- noch Ausführungstest  
**Basis:** `1595d6d38e77804760612621657721b3699d2fea` · **Referenzen:** [10 Requirements](10_REQUIREMENTS.md), [50 Validation](50_VALIDATION_CONTRACT.md).  
Dieser Vertrag legt **logische** Tabellen, Beziehungen, semantische Invarianten, elektrische Transformationen sowie deklarative Konfigurationsfelder fest. Er wählt **kein** CGMES-Backend und kein physisches Tabellenformat.

## 1. Architekturschichten und Datenprodukte

`CGMES 2.4.15 / CGMES 3.0 Modellset` → **externes versionsbewusstes RDF/CIM-Backend** (XML/ZIP, RDF-Referenzen, Klassen, Header, Profile) → **Source Graph + Raw Ledger** → **Canonical Network v1 (verlustbewusster Graph in Tabellen)** → **Electrical Projection v1** (vereinfachtes symmetrisches AC+HVDC-Übertragungsnetz) → **PyPSA Detailed View** und `m0_sidecar` → Modul 1. Exportmodus 1 verwendet Source Graph+Canonical+Delta; Exportmodus 2 benötigt PyPSA+Konstruktions-Metadaten+Explizitregeln, siehe [50](50_VALIDATION_CONTRACT.md).

**Unveränderlich:** Der Quellgraph, Originalwerte, Originalbeziehungen, Source-Profile, Original-mRIDs, P/Q-/Tap-Referenzzustand, Identitätszuordnung und die originale detaillierte Netzversion. Änderungen erfolgen als neue Canonical-Revisions/Delta-Events, nicht als Überschreiben des Originals. Die zeitlich hochaufgelösten RES-/Last-/Dispatchdaten, PACD und die Reduktion sind keine Tabellen dieses Modul-0-Vertrags.

**Drei klar getrennte Artefakte:**

1. `canonical_source`: alle relevanten Originalobjekte, Endports, Zustände, Grenzwerte, Historie, ungelöste Unbekannte und Rohbeziehungen.
2. `electrical_projection`: validierter positiver Sequenznetz-Schnitt mit aktiven Bussen, Zweigen, Ersatzsternen, Shunts, Erzeugung/Last und einfacher HVDC-Steuerportdarstellung; Quelle unverändert.
3. `pypsa_network` + `m0_sidecar`: PyPSA-Standardtabellen nur mit nachweisbar repräsentierbaren Attributen; Sidecar bewahrt Identitäten, Boundary, granularen Limits, Tap-Originaldaten, Geo, Rohattributen und qualifizierten Verlusten.

## 2. Konventionen, Identifier und Versionierung

### 2.1 Datentypen, Nulls, Schlüssel

- Typen: `S` UTF-8 String, `U` UUID/URN-String, `I` int32/64, `F` float64 endlich, `B` bool, `TS` ISO-8601 Timestamp mit Zeitzone/UTC, `J` streng validiertes JSON (kein undeklariertes Objekt-Pickling), `E` versioniertes Enum, `BIN` Datei-/Graph-Blob-Referenz. `DEC` Dezimal-Lexem als String zusätzlich zu F, falls präziser originaler RDF-Wert relevant ist. Winkel in `deg` oder `rad` **ausschließlich bei Felddeklaration**; keine stille Mischung.
- `PK` bezeichnet Primärschlüssel, `FK` referenzielle Pflicht. **Null ist NIE Null als Zahl:** `null` = fehlend/nicht geliefert, `0` = tatsächlich gelieferter/abgeleiteter Nullwert. Unbekannt, nicht anwendbar und nicht unterstützt unterscheiden sich über `absence_reason`.
- Einheitensystem (kanonisch): P **MW**, Q **Mvar**, S **MVA**, Netzspannung **kV** Leiter–Leiter (RMS), Betriebsstrom **A**, R/X **Ω**, G/B **S**, Länge **km**, Winkel **deg**, Frequenz **Hz**, Dauer **s**, p.u. **1** mit expliziter Basis; Latitude/Longitude nur mit CRS, keine automatische Annahme WGS84. Positionen können auch projizierte Ost-/Nordwerte tragen.
- Identität: `source_key = (model_authority_id, cgmes_profile_family, source_mrid)` als kanonischer namespacespezifischer Quell-Identifier; überlappende mRIDs in mehreren Profilen desselben logischen Source-Modells ergeben **ein Objekt** mit mehreren Source-Occurrences. Ein abweichendes mRID-/Klassen-/Authority-Paar wird nie stillschweigend gleichgesetzt. `asset_id`: deterministisch erzeugte interne stabile ID aus kanonisch gewählter Quellidentität; `source_object_id` bezeichnet dagegen eine revisionsgebundene Original-Occurrence (`source_set_hash` plus `source_key`), damit geänderte Rohquellen als neue unveränderliche Datensätze koexistieren können; `view_id`: deterministischer ID-Namespace für abgeleitete PyPSA-Zeilen/Sternäste, niemals als CGMES-mRID ausgeben. Für echten Export-2-Generator gelten gesonderte neue IDs.
- Wertprovenienz: jedes elektrisch relevante Feld ist über `value_provenance` mit `value_origin ∈ {SOURCE, DERIVED, DEFAULT, MISSING}`, `source_ref` (falls SOURCE), `function_id`/Input-IDs (DERIVED), `policy_id` (DEFAULT), `absence_reason` (MISSING), `confidence` und `quality_flag` verknüpft. „0 aus PyPSA-Default“ ist **DEFAULT**, niemals SOURCE.
- Konflikte der Profile/EQ/SSH/SV werden nicht durch „last file wins“ gelöst; eine verbindliche referenzierte Auswahlpolicy und Konflikt-Ledger sind Pflicht.

### 2.2 Revisionsregeln (für **jede** Tabelle in Register 3)

**Spalte V:** `I` = append-only Quelle mit `import_id` und Hash, nie editieren; `N` = versionierter Netzbestand (PK enthält `network_revision_id`); `O` = zustands-/szenarioabhängig (`operating_state_id` + Quellzeit, aus SSH/SV); `D` = abgeleitet aus `network_revision_id, mapping_contract_version, mapping_policy_hash`, bei Änderung **rebuild**; `X` = Export-/Audit-Transaction. Alle Tabellen besitzen `contract_version`, `record_origin` und `created_at` als gemeinsame Pflicht-Metadaten (in V=I zusätzlich `source_file_id`/`source_object_ref` oder `source_graph_ref`; V=N/O/D über `network_revision_id`; V=X über `transaction_id`). **Keine In-place-Änderung** einer veröffentlichten Revision, keine Wiederverwendung einer abgeleiteten ID mit geänderter Bedeutung. Schema-Major-Bump für geänderte Feldsemantik/PK-/Einheitenregeln, Minor für additive nullable Felder, Patch nur Dokumentationskorrekturen. Versionen einer CGMES-Familie werden durch profilgebundene Adapter normalisiert, nicht durch Änderung der kanonischen Feldbedeutung.

### 2.3 Relationaler Grundsatz und Beispiel

Ein `terminal` verweist auf `equipment` und `connectivity_node`; eine zustandsabhängige `topology_membership` ordnet diesen Anschluss einer `topological_node`/einem `bus` zu. Die Ableitung ist bijektiv **nur innerhalb des für diesen Zustand aktiven Topologienetzes**; mehrere ConnectivityNodes dürfen auf einen Bus fallen, und ein Equipment kann mehrere Terminals haben. `pypsa_mapping` bildet 1:n auf abgeleitete Zeilen, etwa 3W → drei `Transformer` plus virtueller Bus; inverse Exportlogik verwendet ursprüngliche Source-Typen, **nicht** die synthetischen Zeilen als neue Geräte.

## 3. Tabellenschema-Register (logisch, bindend)

**Tabellenkonvention:** In jeder Zeile sind **PK**, **FK**, **Pflichtfelder** (zusätzlich zu PK/FK und `contract_version`), **optionale Felder**, Einheiten und **V** angegeben. `id:S` kennzeichnet Name und Typ; `name:F[Einheit]` Einheiten. `?` bedeutet nullable. ``` ist nirgends physikalische Einheit. Für Domain-Enums gelten zentral die angegebenen Werte; weitere Enum-Werte sind additive kontrollierte Schemaänderungen, nicht frei interpretierbare Strings.

### 3.1 Quellpakete, Profil- und Identitätsherkunft

| Tabelle | PK; FK | Pflichtfelder (Typ/[Einheit]) | Optional / Bedeutung | V |
|---|---|---|---|---|
| `import_runs` | `import_id:U` | `started_at:TS, backend_name:S, backend_version:S, contract_version:S, input_manifest_sha256:S, status:E` | `finished_at:TS?, configuration_sha256:S?, warnings:J?` | I |
| `network_revisions` | `network_revision_id:U`; FK `import_id` | `network_id:S, revision_index:I, cgmes_family:E, source_set_hash:S, authority_set:J, reference_state_id:S?` | `study_case:S?, description:S?, parent_revision_id:U?` | N |
| `source_files` | `source_file_id:U`; FK `import_id` | `uri:S, sha256:S, byte_size:I, format:E, profile_code:E, declared_version:S` | `zip_member:S?, producer:S?, parsed_at:TS?, provenance_license:S?` | I |
| `model_headers` | `model_header_id:U`; FK `source_file_id` | `model_id:S, profile_uri:S, version_label:S, authority_id:S, header_raw:J` | `created:TS?, scenario_time:TS?, dependent_on:J?, supersedes:J?, description:S?` | I |
| `source_objects` | `source_object_id:U`; FK `network_revision_id` | `source_mrid:S, source_class_uri:S, source_authority_id:S, is_boundary:B` | `name:S?, alias:S?, equipment_scope:E?` | I |
| `source_occurrences` | `(source_object_id, source_file_id, profile_uri)`; FKs `source_objects/source_files` | `rdf_subject:S, occurrence_hash:S` | `graph_name:S?, source_lexical_id:S?` | I |
| `source_relations` | `source_relation_id:U`; FK `source_object_id`, optional FK `target_source_object_id` | `predicate_uri:S, source_object_id:U, target_rdf_uri:S, relation_status:E` | `target_source_object_id:U?, profile_uri:S?, graph_name:S?, ordinal:I?` | I |
| `raw_attributes` | `raw_attribute_id:U`; FK `source_object_id/source_file_id` | `predicate_uri:S, rdf_lexical_value:S, rdf_datatype_uri:S, original_profile_uri:S` | `unit_symbol:S?, unit_multiplier:S?, language:S?, parsed_value:J?, cardinality_index:I?` | I |
| `value_provenance` | `value_id:U`; FK `network_revision_id` | `table_name:S, row_key:S, field_name:S, value_origin:E, quality_flag:E` | `source_object_id:U?, source_file_id:U?, raw_attribute_id:U?, input_value_ids:J?, function_id:S?, policy_id:S?, absence_reason:E?, uncertainty:J?` | D |
| `mapping_identity` | `mapping_id:U`; FK `source_object_id/network_revision_id` | `target_layer:E, target_table:S, target_id:S, relation_type:E, mapping_policy_version:S` | `ordinal:I?, synthetic:B?, parent_mapping_id:U?` | D |
| `assumption_events` | `assumption_id:U`; FK `network_revision_id` | `affected_table:S, affected_id:S, field:S, assumption_type:E, policy_id:S, severity:E` | `input_value_ids:J?, numerical_effect:J?, approver:S?, approval_timestamp:TS?` | D |

***Quellgraph-Sicherung:*** `source_files` plus externe/archivierte `raw_graph_blob_ref` im Importmanifest sind für den semantisch vollständigen Modus-1-Export **obligatorisch**. `raw_attributes` allein kann beliebige RDF-Graphstrukturen, leere Blanks, Profilregeln, XML-Header oder ursprüngliche Profilpartitionierung nicht zuverlässig reproduzieren. Backend muss unveränderten Graph oder äquivalentes verlustfreies Subjekt-Prädikat-Objekt-Modell mitsamt Namespaces, Profilzugehörigkeit, Headern und Graphgrenzen bereitstellen. Eine Byte-für-Byte-Identität neu serialisierter XML-Dateien ist **nicht** versprochen.

### 3.2 Netzhierarchie, Geografie, Ports und elektrische Topologie

| Tabelle | PK; FK | Pflichtfelder | Optional / Bedeutung | V |
|---|---|---|---|---|
| `countries` | `country_code:S` | `name:S, country_registry_version:S` | `iso3166_1_alpha2:S?, region_code:S?, non_iso_extension_reason:S?` | N |
| `substations` | `(revision_id, substation_id)`; FK `source_objects/countries` | `substation_id:U, country_code:S, name:S` | `source_object_id:U?, location_id:U?, tso_id:S?` | N |
| `voltage_levels` | `(revision_id, voltage_level_id)`; FK `substations` | `substation_id:U, base_voltage_kv:F[kV], voltage_level_id:U` | `source_object_id:U?, nominal_name:S?` | N |
| `locations` | `(revision_id, location_id)`; FK `source_objects` | `location_id:U, coordinate_system:S, location_type:E` | `source_object_id:U?, geometry_source:E?, route_geometry_type:E?` | N |
| `position_points` | `(revision_id, location_id, sequence_number)`; FK `locations` | `sequence_number:I, x:F, y:F, coordinate_system:S` | `z:F?, raw_x_lexeme:S?, raw_y_lexeme:S?, point_type:E?` | N |
| `connectivity_nodes` | `(revision_id, connectivity_node_id)`; FK `voltage_levels?` | `connectivity_node_id:U, source_object_id:U, container_id:U` | `voltage_level_id:U?, country_code:S?` | N |
| `equipment` | `(revision_id, equipment_id)`; FK `source_objects` | `equipment_id:U, cim_class:E, source_object_id:U, terminal_count:I` | `container_id:U?, station_id:U?, owner_tso:S?` | N |
| `equipment_states` | `(revision_id, operating_state_id, equipment_id)`; FK `equipment` | `in_service:B, equipment_id:U, availability_state:E` | `outage_reason:S?, source_ssh_object_id:U?` | O |
| `terminals` | `(revision_id, operating_state_id, terminal_id)`; FK `equipment/connectivity_nodes` | `terminal_id:U, equipment_id:U, sequence_number:I, is_connected:B, source_object_id:U` | `connectivity_node_id:U?, source_topological_node_id:U?, phases:S?, regulation_target:B?` | O |
| `switches` | `(revision_id, equipment_id, operating_state_id)`; FK `equipment/terminals` | `switch_kind:E, is_open:B, normal_open:B, is_in_service:B` | `rated_current_a:F[A]?, switching_restrictions:J?` | O |
| `topological_nodes` | `(revision_id, operating_state_id, topological_node_id)`; FK `voltage_levels?` | `topological_node_id:U, source_or_derived:E, base_voltage_kv:F[kV]` | `source_object_id:U?, voltage_level_id:U?, island_id:U?` | O |
| `topology_membership` | `(revision_id, operating_state_id, connectivity_node_id)`; FK `connectivity_nodes/topological_nodes` | `topological_node_id:U, derive_rule_id:S` | `source_tp_node_id:U?, conflict_ref:U?` | O |
| `buses` | `(revision_id, operating_state_id, bus_id)`; FK `topological_nodes/countries` | `bus_id:U, topological_node_id:U, v_nom_kv:F[kV], carrier:E, country_code:S, island_id:U` | `substation_id:U?, voltage_level_id:U?, x:F?, y:F?, crs:S?, geo_quality:E?, v_set_pu:F[pu]?` | D |
| `ac_islands` | `(revision_id, operating_state_id, island_id)` | `island_id:U, bus_count:I, active_branch_count:I, connectivity_status:E` | `slack_source_id:U?, boundary_touch_count:I?, solvability_status:E?` | D |

**Konsequenz:** Der aktive Geräte-Status wird aus `equipment_states` **und** dem maßgeblichen Terminal-/Switch-Zustand gewonnen, nicht aus einem unveränderlichen `in_service`-Feld der Leitungs- oder Transformer-Stammtabelle. `country_code` verweist auf ein **versioniertes Länderregister** (ISO-3166-Werte, wo vorhanden; projektweit genehmigte Sondercodes wie `XK` nur explizit). Der Ländercode kommt aus fachlich überprüften Substation-/Region-/Territory-Zuordnungen, nicht aus Koordinaten-Heuristik ohne Kennzeichnung. Ein auf zwei Länder verteiltes Asset hat **länderspezifische Endport-Zuordnungen**; seine Leitung selbst muss nicht eine einzige „physische Länder“-Wahrheit haben. `location_id` und alle Originalpositionen bleiben unverändert; zu `buses` projizierte x/y sind ausdrücklich DERIVED. `island_id` ist ein AC-Synchronisierungsverbund; HVDC-Links verschmelzen solche Inseln nicht.

### 3.3 Passive Betriebsmittel, Transformatoren, Generatoren und Last

| Tabelle | PK; FK | Pflichtfelder | Optional / Bedeutung | V |
|---|---|---|---|---|
| `ac_lines` | `(revision_id, equipment_id)`; FK `equipment/terminal0/terminal1` | `terminal0_id:U, terminal1_id:U, r_ohm:F[Ω], x_ohm:F[Ω], g_total_s:F[S], b_total_s:F[S]` | `length_km:F[km]?, is_underground:B?, r0_ohm:F?, x0_ohm:F?, asset_owner:S?` | N |
| `equivalent_branches` | `(revision_id, equipment_id)`; FK `equipment/terminals` | `terminal0_id:U, terminal1_id:U, branch_kind:E, r_ohm:F[Ω], x_ohm:F[Ω]` | `g_total_s:F[S]?, b_total_s:F[S]?, equivalent_source:E?, control_offset_deg:F?` | N |
| `transformers` | `(revision_id, equipment_id)`; FK `equipment` | `winding_count:I{2,3}, source_mrid:S` | `s_rated_mva:F[MVA]?, vector_group:S?, model_preference:E?, magnetizing_loss_kw:F[kW]?` | N |
| `transformer_ends` | `(revision_id, equipment_id, end_number)`; FK `transformers/terminals` | `terminal_id:U, rated_u_kv:F[kV], end_number:I, r_ohm:F[Ω], x_ohm:F[Ω], g_s:F[S], b_s:F[S]` | `rated_s_mva:F[MVA]?, connection_kind:E?, ground_impedance:J?, end_source_object_id:U?` | N |
| `tap_changers` | `(revision_id, tap_changer_id, operating_state_id)`; FK `transformer_ends` | `tap_kind:E{RATIO,PHASE,OTHER}, transformer_id:U, end_number:I, low_step:I, high_step:I, neutral_step:I, current_step:I, regulating_enabled:B` | `step_voltage_increment_pct:F[%]?, x_step_parameters:J?, phase_step_table:J?, ratio_step_table:J?, control_target_id:U?, target_value:F?, target_unit:S?, ltc_flag:B?, phase_shift_deg:F[deg]?` | O |
| `generating_units` | `(revision_id, generating_unit_id)`; FK `source_objects` | `technology:E, source_object_id:U, is_in_service:B` | `min_operating_p_mw:F[MW]?, max_operating_p_mw:F[MW]?, fuel:S?, energy_source:E?, unit_count:I?` | N |
| `generators` | `(revision_id, equipment_id, operating_state_id)`; FK `equipment/terminals` | `terminal_id:U, injection_p_mw:F[MW], injection_q_mvar:F[Mvar], control_mode:E{PQ,PV,SLACK,UNKNOWN}, in_service:B` | `generating_unit_id:U?, rated_s_mva:F[MVA]?, p_min_mw:F?, p_max_mw:F?, q_min_mvar:F?, q_max_mvar:F?, voltage_target_kv:F?, regulating_control_id:U?, capability_curve_ref:U?, technology:E?` | O |
| `external_injections` | `(revision_id, equipment_id, operating_state_id)`; FK `equipment/terminal` | `terminal_id:U, injection_p_mw:F[MW], injection_q_mvar:F[Mvar], is_in_service:B, control_mode:E` | `p_min_mw:F?, p_max_mw:F?, q_min_mvar:F?, q_max_mvar:F?, voltage_target_kv:F?, boundary_authority_id:S?` | O |
| `loads` | `(revision_id, equipment_id, operating_state_id)`; FK `equipment/terminal` | `terminal_id:U, demand_p_mw:F[MW], demand_q_mvar:F[Mvar], in_service:B` | `pfixed_mw:F?, qfixed_mvar:F?, load_response_ref:U?, constant_power_fraction:F?, motor_or_equipment_type:E?` | O |
| `shunts` | `(revision_id, equipment_id, operating_state_id)`; FK `equipment/terminal` | `terminal_id:U, model_kind:E{LINEAR,NONLINEAR}, g_equiv_s:F[S], b_equiv_s:F[S], sections_in_service:I, in_service:B` | `g_per_section_s:F?, b_per_section_s:F?, max_sections:I?, voltage_dependency:J?, control_target_id:U?` | O |
| `regulating_controls` | `(revision_id, regulating_control_id, operating_state_id)`; FK `source_objects` | `mode:E, enabled:B, controlled_equipment_ids:J, target_terminal_id:U` | `target_value:F?, target_unit:S?, deadband:F?, discrete:B?, monitored_remote_bus_id:U?` | O |
| `operating_states` | `operating_state_id:U`; FK `network_revision_id` | `state_kind:E{SSH,SV,DERIVED}, source_model_id:S, consistency_hash:S` | `scenario_time:TS?, pf_iteration:S?, loadflow_reference_id:U?, precedence_policy_id:S?` | O |

***Zustandsabhängigkeit:*** `equipment.inService` liegt in `equipment_states` und `Terminal.connected`/`Switch.open` in zustandsgebundenen Tabellen. Die in `switches` und `equipment_states` wiedergegebenen Service-Flags müssen widerspruchsfrei sein. Original-Parameter, technische P/Q-Grenzen und Unit-Associations sind von `operating_state_id` zu trennen, wo sie zeitinvariant sind. Die Tabellen kodieren den Snapshot-Schlüssel explizit, selbst wenn ein Input nur einen Snapshot enthält. Bei Import einer „unsolved“ Lieferung darf `SV` nicht mit synthetischen Nullen ersetzt werden.

### 3.4 HVDC, Boundary, Limits, State Variables und Export-Audit

| Tabelle | PK; FK | Pflichtfelder | Optional / Bedeutung | V |
|---|---|---|---|---|
| `hvdc_systems` | `(revision_id, hvdc_system_id)`; FK `equipment?` | `topology_kind:E{POINT_TO_POINT,MULTITERMINAL,UNKNOWN}, source_authority_id:S, converter_count:I` | `technology:E{LCC,VSC,UNKNOWN}?, power_nom_mw:F?, loss_model_ref:U?, control_mode:E?` | N |
| `hvdc_converters` | `(revision_id, converter_id, operating_state_id)`; FK `hvdc_systems/equipment/terminals` | `ac_terminal_id:U, converter_kind:E, is_in_service:B` | `dc_terminal_id:U?, p_ac_inj_mw:F[MW]?, q_ac_inj_mvar:F[Mvar]?, voltage_dc_kv:F?, current_dc_a:F?, loss_coefficients:J?, p_min_mw:F?, p_max_mw:F?, control_mode:E?` | O |
| `dc_branches` | `(revision_id, dc_branch_id)`; FK `hvdc_systems/dc_terminal_ids` | `dc_terminal0_id:U, dc_terminal1_id:U, branch_kind:E` | `r_ohm:F[Ω]?, current_limit_a:F[A]?, dc_voltage_kv:F[kV]?` | N |
| `boundary_connections` | `(revision_id, boundary_id)`; FK `source_objects/terminals?` | `boundary_authority_id:S, model_a_id:S, model_b_id:S, join_kind:E, status:E` | `shared_source_mrid:S?, external_terminal_id:U?, equivalence_group:S?, original_cross_refs:J?` | N |
| `operational_limit_sets` | `(revision_id, limit_set_id)`; FK `equipment/terminal?` | `equipment_id:U, limit_set_id:U, limiting_context:E` | `terminal_id:U?, authority_id:S?, applicability:J?, overload_management:J?` | N |
| `operational_limits` | `(revision_id, limit_id)`; FK `operational_limit_sets` | `limit_kind:E{CURRENT,APPARENT_POWER,ACTIVE_POWER,VOLTAGE,OTHER}, quantity_value:F, unit:S, direction:E{POSITIVE,NEGATIVE,ABSOLUTE,UNSPECIFIED}, limit_type:E, valid_state:E` | `terminal_id:U?, acceptable_duration_s:F[s]?, season:E?, valid_from:TS?, valid_to:TS?, source_object_id:U?, contingency_context:E?, normal_or_emergency:E?` | N |
| `sv_voltages` | `(revision_id, operating_state_id, topological_node_id)`; FK `topological_nodes` | `v_kv:F[kV], angle_deg:F[deg], source_sv_id:U` | `validation_eligible:B?, reference_error_code:E?` | O |
| `sv_power_flows` | `(revision_id, operating_state_id, terminal_id)`; FK `terminals` | `p_from_bus_mw:F[MW], q_from_bus_mvar:F[Mvar], source_sv_id:U` | `flow_direction_quality:E?, source_sign_convention:E?` | O |
| `pypsa_mapping` | `(revision_id, pypsa_view_id, component_type, component_name)`; FK `mapping_identity` | `component_type:E, component_name:S, mapping_role:E, source_equipment_ids:J, terminal_orientation:J` | `synthetic_bus_id:U?, approximation_class:E?, model_constraint_ids:J?, mapping_errors:J?` | D |
| `quality_events` | `quality_event_id:U`; FK `network_revision_id` | `rule_id:S, severity:E, event_status:E, object_type:S, object_id:S, message:S` | `observed_value:J?, expected_value:J?, tolerance:J?, remediation:S?, waived_by:S?` | D |
| `export_transactions` | `transaction_id:U`; FK `network_revision_id` | `export_mode:E{UPDATE_IMPORTED,CREATE_FROM_PYPSA}, target_cgmes_family:E, status:E, loss_manifest_hash:S, delta_hash:S` | `base_graph_sha256:S?, profile_set:J?, new_authority_id:S?, mapping_policy_hash:S?, exported_file_hashes:J?` | X |
| `loss_manifest` | `(transaction_id, loss_item_id)`; FK `export_transactions` | `source_object_or_component:S, field_or_relation:S, loss_class:E{EXACT,APPROX,NONRECONSTRUCTIBLE}, reason:S, severity:E` | `source_value_ref:U?, target_value:J?, policy_id:S?, acknowledged_by:S?, physical_effect:J?` | X |

**Normative relationelle Nebenbedingungen:** alle gemappten `source_object_id` und `terminal_id` sind gültig; ein Terminal gehört genau einem Equipment und einer eindeutigen Reihenfolge, keine duplizierten `end_number`; 2W besitzt zwei, 3W drei Ports; Limits dürfen *mehrere* Limits pro Equipment/Terminal/Dauer/Richtung besitzen; Quell-Identität und View-Identität sind nicht austauschbar. `network_revision_id` erscheint in Tabellen als `revision_id` (identischer FK-Typ). Wenn die CGMES-Quelle eine als Pflicht erklärte Größe **nicht liefert**, wird ein `MISSING`-Eintrag mit Hard-/Soft-Gate erzeugt; „Pflichtfeld“ bezeichnet die Anforderung einer **freigegebenen elektrischen Projektion**, nicht die Behauptung, jede Eingabedatei müsse dieses Feld in jedem Profil enthalten.

## 4. Elektrische Abbildung CGMES → Canonical → PyPSA

### 4.1 Allgemeines: Basen, Orientation, Leistungszeichen

**Dreiphasige symmetrische Basen:** Für Leiter-Leiter-Spannung `U_base` [kV], dreiphasige `S_base` [MVA] gilt

`Z_base = U_base² / S_base` [Ω], `Y_base = S_base / U_base²` [S],
`z_pu = Z_Ω · S_base / U_base²`, `y_pu = Y_S · U_base² / S_base`.

Umrechnung einer Zweigimpedanz von Basis 1 nach 2: `z_pu,2 = z_pu,1 · (S_base,2/S_base,1) · (U_base,1/U_base,2)²`. Bei Transformatoren besitzt **jede Wicklung** eine Nennspannung als Ausgangsbasis; Sternzweige sind auf eine **einheitliche Systemleistungsbasis und kompatible Wicklungs-/Spannungsbasen** zu referenzieren. `s_nom` des PyPSA-Transformers ist keine universelle Netzbasis; die PyPSA-Transformer-`r/x/g/b` sind per-unit auf `s_nom` und Nennspannung, die PyPSA-Line-`r/x/g/b` hingegen Ω/S [P1–P3]. Keine blinde Division durch globale 100 MVA.

**Orientierung:** Source-Terminal `sequence_number`/EndNumber bestimmt die stabile Portreihenfolge; PyPSA `bus0`/`bus1` folgen einer versionierten Richtungsregel. Eine Vertauschung muss Phase Shift, unsymmetrische Tap-Seite, End-SV-Flüsse, Limits und HVDC-Richtungsgrößen **physikalisch äquivalent** transformieren, sonst BLOCK.

**Leistung:** CGMES nutzt bei EnergyConsumer und RotatingMachine/PowerElectronicsConnection/ExternalNetworkInjection häufig die **Load-Sign-Convention**: positive `p/q` heißt Strom-/Leistungsbezug *aus dem Netzknoten in das Equipment*. Deshalb Source-`RotatingMachine.p = -100 MW` → Canonical `injection_p_mw = +100` → PyPSA `Generator.p_set = +100`. Source-`EnergyConsumer.p = +40 MW` → `demand_p_mw = +40` → `Load.p_set = +40`. Negative Last ist nicht automatisch invalid; als Rückspeisung anhand Konfiguration und Provenienz markieren. ***Nie*** ein globales Minus auf alles anwenden; Terminal-`SvPowerFlow` wird mit Orientierung **positiv aus dem Bus ins Equipment** separat abgeglichen. KCL: `sum(injections) - sum(loads) - sum(shunt withdrawals) - sum(branch withdrawals) = 0`, unter Berücksichtigung von Verlusten/Slack. Siehe [ENTSO-E Quality Guidance](https://www.entsoe.eu/Documents/Network%20codes%20documents/Implementation/cacm/cgmm/Quality_of_CGMES_Datasets_and_Calculations.pdf), [CIM RotatingMachine](https://docs.rs/cim-rs/latest/cim_rs/cgmes3/views/struct.RotatingMachine.html), [CIM EnergyConsumer](https://acs.pages.rwth-aachen.de/public/cim/cimpy/cimpy.cgmes_v2_4_15.EnergyConsumer.html).

### 4.2 ACLineSegment und EquivalentBranch

| CGMES | Canonical | PyPSA | Gate |
|---|---|---|---|
| `ACLineSegment` `r,x` [Ω], `gch,bch` [S] als **gesamte** Serien-/Ladeparameter; End-Terminals | `ac_lines` `r_ohm,x_ohm,g_total_s,b_total_s`, echte Orientation | `Line(bus0,bus1,r,x,g,b,s_nom)` (Leitungs-Nennspannung kommt aus dem Anschluss-`Bus.v_nom`), Parameter direkt, kein `Line.type`-Override | `z ≠ 0`, positive sinnvolle Basis, 2 aktive Endports, Gleichspannungsniveau ohne expliziten Transformator |
| `EquivalentBranch` `r,x` etc. | `equivalent_branches`, `branch_kind` und Herkunft | `Line` **nur** als gekennzeichnetes Ersatzmodell (nicht echte Leitung) oder dedizierter passiver Sonderadapter | Ersatzcharakter sichtbar, Steuereffekte nur bei nachgewiesener Äquivalenz |
| `ACLineSegment` gesperrt/ausgeschaltet | Rohobjekt bleibt; aktiver Teilgraph ohne leitenden Zweig | `Line.active=False` oder keine aktive View-Zeile, abhängig von geprüfter PyPSA-Version | keine Neuanbindung über geöffnetes Switch-Objekt |

**PI-Ersatz:** `z=r+jx`, `y=1/z`, `y_sh=g+j b`. Ohne Tap gilt `Y_00=Y_11=y+y_sh/2` und `Y_01=Y_10=-y`. Das *gesamte* `gch/bch` wird hälftig den beiden Leitungsenden zugewiesen. `bch` ist **Suszeptanz** in S, kein MVAr-Wert; die reaktive Strom-/Leistungsbilanz wird über `S_k=V_k·conj(I_k)` geprüft. Wenn Parameter pro km vorliegen, wird Länge genau **einmal** angewandt und die Provenienz dokumentiert; CGMES-`ACLineSegment`-Gesamtparameter dürfen nicht erneut mit `length` multipliziert werden. `r0/x0/g0ch/b0ch` gehören außerhalb der positiven Sequenz, bleiben aber roh erhalten.

### 4.3 Zweiwicklungstransformatoren mit Tap/Phase

CGMES `PowerTransformer` + zwei `PowerTransformerEnd` + `RatioTapChanger`/`PhaseTapChanger` + `TapChangerControl`/SSH (`step`) → `transformers, transformer_ends, tap_changers, regulating_controls`. Die CGMES-2W-Konvention platziert die positive Sequenzimpedanz im Normalfall an End 1; die Regeln des konkreten Profils und die übermittelten Werte sind zu prüfen, **nicht** alle Wicklungsimpedanzen blind zu summieren [C3, C5]. Im Canonical ist jedes `end_number` mit `Terminal` verbunden.

**Transformer-Projection:** ein aktiver PyPSA `Transformer(bus0,bus1,r_pu,x_pu,g_pu,b_pu,s_nom,tap_side,tap_ratio,phase_shift,model)`. Die Parameter werden für ein deklariertes T- oder PI-Modell auf PyPSA-`s_nom` und geeignete Wicklungsbasis umgerechnet. Ein gesetztes `Transformer.type` kann in PyPSA explizite Werte überschreiben; standardmäßig `type=""` und `model` aus dokumentierter Gleichwertigkeitsprüfung. RatedU-Verhältnis und tatsächliche Bus-Nennspannungen sind getrennte Daten. Kein `tap_ratio=1` bei unbekanntem Tap.

Für das PI-Modell mit Off-Nominal-Tap `t = τ·exp(jφ)` auf **Port 0** ist die physikalische Solladmittanz (bei standardisierter Portorientierung)

`Y_00 = (y+y_sh,0)/|t|²`; `Y_01 = -y/conj(t)`; `Y_10 = -y/t`; `Y_11=y+y_sh,1`.

Die konventionelle Symmetrie von Kreuzgliedern gilt bei `φ=0`, sonst komplex-konjugiert passend. Diese Form ist **Referenz eines auf Port 0 angesetzten idealen Taps**, nicht die stillschweigende Behauptung, PyPSA speichere intern dieselbe Portkonvention. Für `tap_side=1` ist die Solladmittanz durch eindeutige Porttransformation abzuleiten. **Gate:** Zweiport-`Y` (und ±φ/PST-Flussrichtung) der berechneten PyPSA-Daten müssen in einem isolierten Test dieselbe physikalische Kennlinie liefern. PyPSA dokumentiert die eigene `tap_side`/`phase_shift`-Konvention; bei linearer Näherung `P_0→1 ≈ (θ_0 − θ_1 − φ)/x_eff` [P2, P3]. RatioTapChanger-Schrittspannung kann nicht generell mit `1+(step-neutral)*increment` auf alle CGMES-Phase-/Tap-Typen übertragen werden: bei nichtlinearen, tabellierten oder asymmetrischen Changers nur geprüfte Feature-Funktion oder BLOCK.

**PV/Slack:** voltage control wird am **geregelten Bus** geführt, nicht einfach aus Maschinentyp erraten; Q-Grenzen, RegulatingControl, Remote-Sensing und Prioritäten bleiben im Sidecar. Die reinen PyPSA-`pf`-Regeln/Slack-Behandlungen bilden CGMES-Regelungsprioritäten nicht generell vollständig ab.

### 4.4 Dreiwicklungstransformatoren

`PowerTransformerEnd` Nr. 1/2/3 liefert gemäß CGMES eine **Stern-Ersatzdarstellung** der positiven Sequenz-Serienwerte und zugehöriger Shunts [C5]. Kanonisches Original: ein `transformers`-Objekt mit drei `transformer_ends` und ggf. getrennten Tap-Changers, Shunts und Limits.

Für die PyPSA-View wird ein **synthetischer, eindeutig benannter Sternbus** `virtual_bus_id = deterministic_id(transformer_mrid,"star")` eingeführt; drei `Transformer`-Äste verbinden Originalport i mit Sternbus. Alle `z_i` werden auf dieselbe Systemleistungsbasis und intern konsistente Spannungsbasen konvertiert; `g_i,b_i` werden dem korrekten Wicklungs-/Sternport zugewiesen. Die resultierende 3-Port-Kron-reduzierte Admittanz muss dem CGMES-Sternnetz **einschließlich aller aktiven Tap-/Phasenstellungen** entsprechen. *Annahme:* virtuelle Sternbusspannung wird durch explizite Normierungswahl erzeugt; wird keine physikalisch konsistente T-/PI-Portdarstellung gefunden oder sind Sternzweige singular, ist die PyPSA-View **nicht freigabefähig**. Scheinbare Zahlenerhaltung von 3 Zweigen genügt nicht. Der synthetische Bus besitzt kein CGMES-mRID und keine automatische Länderzuordnung.

### 4.5 Schalter, Inseln und Boundary-Netz

**Zustandsreihenfolge:** (1) Roh-Gültigkeit EQ/MAS/Boundary und Equipment/Terminal-FKs; (2) `inService`/`Terminal.connected`/`Switch.open` für den konkreten SSH-State; (3) Vereinigung der ConnectivityNodes **nur** über elektrisch geschlossene, leitende Switches; (4) Abgleich gegen geliefertes TP; (5) Erzeugung TopologicalNodes/Buses; (6) aktiver Zweiggraph und AC-Inseln; (7) Terminal-/Asset-Anschlussauflösung. `Switch.normalOpen` ist ein nominaler Hinweis, **kein** Ersatz des aktuellen `open`. Leitungen und Transformatoren verbinden Busse als **Impedanzzweige**, verschmelzen keine Knoten zu einem Bus. Geschlossene Schalter müssen nicht als Nullimpedanz-PyPSA-Leitung erzeugt werden. Offene Schalter dürfen nicht als Bus-Kurzschluss gelten.

Boundary-Assemblierung nach Authority und Originalreferenz (CGMES 2.4.15 EQ_BD/TP_BD vs CGMES 3.0 Core-EQ/Boundary-Regeln mit ggf. zugelassenem EQBD-Übergangspfad). Gemeinsame Objekte werden **referenziell**, nicht geometrisch, vereinigt. Mehrdeutige X-/Boundary-Nodes, abweichende BaseVoltage oder ungültige Cross-Model-Refs → BLOCK. Eine unsolved Importlieferung ohne TP ist nur zugelassen, wenn der dokumentierte topology-processor die Äquivalenz schlüssig ableiten kann.

### 4.6 Erzeugung, Verbraucher, Shunts, Limits

- `SynchronousMachine`, `PowerElectronicsConnection`, `GeneratingUnit` und Technologieattribute → `generating_units`/`generators`: PyPSA `Generator(bus,carrier,p_nom,p_set,q_set,control)`, soweit geeignet. **Injektionszeichen** standardisieren, `RegulatingControl.enabled/mode`, Q-Limits und Q-Kennlinie separat sichern; PV-/Slack-Zuweisung muss je AC-Insel konsistent sein. `Generator.p_nom` ist Kapazität, `p_set` ist Betriebspunkt; nicht aus einander erraten.
- `EnergyConsumer` → `loads` → PyPSA `Load(bus,p_set,q_set)`; spannungsabhängige Lastmodelle und ZIP-Lastcharakteristika sind **nicht** exakt durch konstante P/Q modelliert. Vereinfachung ⇒ `APPROX` mit Modell-/Spannungsbereich. Stationärer P/Q-Sollwert stammt aus richtigem Zustand, nicht aus SV-Endlastfluss über geschriebenes SSH.
- `ExternalNetworkInjection` → `external_injections` → PyPSA `Generator`/`Load`/Netzäquivalent nur gemäß ausgewähltem PQ/PV/Slack/Equivalent-Injection-Policy. Boundary-Objekt bleibt erhalten; externe Einspeisung darf nicht zur unsichtbaren Bilanzkorrektur werden.
- `LinearShuntCompensator`/`NonlinearShuntCompensator` + Abschnitte → `shunts` mit aktuell wirksamem `g_equiv,b_equiv` → PyPSA `ShuntImpedance(bus,g,b)` [S]; die Spannungsabhängigkeit der reinen Admittanz wird bei konstantem `Y` dargestellt, stufenweise/tabel­lierte Nichtlinearität und Regeldynamik nicht. Für `b>0` liefert eine passive Suszeptanz am Bus bei üblichem `S=V I*` einen **kapazitiven Q-Einspeisebeitrag**; Vorzeichen anhand Endportleistung prüfen.
- `OperationalLimitSet`/`OperationalLimit` und `OperationalLimitType` → `operational_limit_sets/operational_limits`, **nicht** automatisch ein einziges `s_nom`. Stromgrenze `I_limit` [A] entspricht bei angenommener Spannung `U_ll` [kV] `S_limit=√3·U_ll·I_limit/1000` [MVA]. Eine Strombegrenzung ist spannungsabhängig; als **statischer konservativer Proxy** darf sie nur unter deklariertem Minimalspannungswert und Zweckkontext übertragen werden. Gegenläufige Terminal-/Richtungs-/Dauer-/Notfallgrenzen bleiben im Sidecar und müssen bei N-1-Analysen in Modul 1 separat ausgewertet werden.

### 4.7 HVDC- und PST-spezifische Grenzen

**CGMES HVDC:** AC/DC Converter und DC-Equipment/Ports werden im Originalgraph erhalten. Für ein festes Point-to-Point-Gerät mit nachweisbaren terminalgebundenen P-Sollwerten und Verlustannahmen kann ein steuerbarer PyPSA `Link` zwischen AC-Bussen die **aktive Wirkleistungsübertragung** approximieren: `p0>0` entnimmt `bus0` Energie; `p1=-η p0` speist `bus1` ein, `0<η≤1`. **Rückwärtsfluss bei η<1:** `p0<0` im selben verlustbehafteten Link modelliert im Allgemeinen die Verluste **falsch**. Daher nur (a) verlustfreier reversibler Link, (b) zwei **gerichtete**, gegenläufige Links mit harter exklusiver Aktivierung (falls späteres Modell diese tatsächlich erzwingt), oder (c) gesonderte symmetrische bidirektionale Verlustfunktion. Ohne realisierte Exklusivitäts-/Verlustbedingungen ist eine Bidirektionalität nicht als physikalisch exakt freigebbar. Blind aus einem Konverterpaar ein verlustfreies „AC-Line“-Element zu erzeugen ist verboten. HVDC-Kontroll-, DC-Spannungs-, Q-Fähigkeits- und Mehrterminal-Constraints bleiben getrennt; komplexe MTDC-Systeme bekommen `UNSUPPORTED_FOR_PYPSA_SIMPLE_LINK` statt erfundener Netzstruktur.
**PST:** Tap-Phase, Tap-Bounds, mechanischer Ratioschritt, Remote Control bleiben eigenständige Felder; linearer PyPSA-Offset ist keine freie optimierbare PST-Regelung, solange nicht gesondert implementiert. Im späteren DC/PTDF-Modell sind aktive Phasenschieber als **affine Flussoffsets** zu erhalten, sonst ist die Projektion nicht für unqualifizierte PTDF-/F0-Rechnungen geeignet.

## 5. Versionierbare YAML-Mapping-Spezifikation (nicht ausführbar)

### 5.1 Was deklarativ ist und was zwingend mathematisch implementiert wird

**YAML erlaubt:** Quell-CIM-Klasse, Profil-/Familien-Match, Quellfeld, Zieltyp/Spalte, Einheiten-/Enum-Vokabular, Identitäts-/FK-Pfade, Property-Priorität EQ/SSH/SV, Status-/Missing-/Default-Policy, Terminalorientierung *als Auswahlregel*, Feature-Gates, Name und Version einer **vorgeprüften** Funktion sowie Zielprojektion/Qualitätsgrenze.  
**YAML darf nicht als unbegrenzte Script-Engine gelten:** per-unit-Basis-/Wicklungsumrechnungen, AC/Transformer/3W-Ybus, Ring-/Netztopologie, PST-Off-Nominal-Taps, Q-Regel-/P/Q-Sign-Konsistenz, HVDC-Verlustmodell und thermische Strom→Leistungsgrenzen benötigen separate, mathematisch und numerisch geprüfte Funktionen. Jedem Funktionsnamen ist eine `function_version` und ein Testvektor zugeordnet.

### 5.2 Beispiel: CGMES-2.4.15-AC-Anschluss und Topologie

```yaml
contract_version: "1.0.0"
mapping_policy_id: "cgmes24-ac-stationary-v1"
cgmes_family: "2.4.15"
profile_uri_policy: "require_header_and_known_profile_uris"
properties:
  terminal_connectivity:
    source_class: "Terminal"
    target_table: "terminals"
    source_identity: ["mRID", "model_authority"]
    foreign_keys:
      equipment_id: "Terminal.ConductingEquipment"
      connectivity_node_id: "Terminal.ConnectivityNode"
    missing_reference: "BLOCK"
  switches:
    source_classes: ["Breaker", "Disconnector", "LoadBreakSwitch", "Switch"]
    state_precedence:
      actual_open: "SSH.Switch.open"
      fallback_normal_open: "PROHIBITED_FOR_ACCEPTED_STATE"
      service_status: "SSH.Equipment.inService"
    topology_function:
      function_id: "switch_union_find_positive_sequence"
      function_version: "1.0"
    tp_consistency: "BLOCK_ON_CONFLICT"
  ac_line:
    source_class: "ACLineSegment"
    target_table: "ac_lines"
    fields:
      r_ohm: {from: "ACLineSegment.r", unit: "ohm", missing: "BLOCK"}
      x_ohm: {from: "ACLineSegment.x", unit: "ohm", missing: "BLOCK"}
      g_total_s: {from: "ACLineSegment.gch", unit: "siemens", missing: "BLOCK"}
      b_total_s: {from: "ACLineSegment.bch", unit: "siemens", missing: "BLOCK"}
      length_km: {from: "Conductor.length", unit: "km", missing: "NULL_WITH_REPORT"}
    electrical_function:
      function_id: "ac_line_pi_admittance"
      function_version: "1.0"
    pypsa_target: "Line"
    pypsa_type_override: "FORBIDDEN"
```

### 5.3 Beispiel: 3W, Schaltstufen, Erzeugung und HVDC

```yaml
contract_version: "1.0.0"
mapping_policy_id: "ac-equipment-v1"
cgmes_family: "3.0"
transforms:
  three_winding:
    source_class: "PowerTransformer"
    when_end_count: 3
    preserve_original_equipment: true
    function_id: "three_winding_star_to_pypsa_transformers"
    function_version: "1.0"
    synthetic_bus_id_rule: "hash(network_revision_id, source_mrid, 'star')"
    acceptance: "KRON_REDUCED_YBUS_EQUIVALENCE"
  taps:
    source_classes: ["RatioTapChanger", "PhaseTapChanger"]
    position_source: "SSH.TapChanger.step"
    ratio_function_id: "ratio_tap_model_for_cgmes_profile"
    phase_function_id: "phase_tap_model_for_cgmes_profile"
    unknown_table_or_step: "BLOCK"
    pypsa_override_type: ""
  machine:
    source_class: "SynchronousMachine"
    p_source: "RotatingMachine.p"
    p_sign_policy: "LOAD_SIGN_TO_INJECTION"
    q_source: "RotatingMachine.q"
    regulation_source: "RegulatingControl.enabled/mode/targetValue"
    output_class: "Generator"
    missing_q_bounds: "REPORT_NO_INVENTED_BOUNDS"
  hvdc:
    source_classes: ["CsConverter", "VsConverter", "DCLineSegment"]
    canonical_target: "hvdc_systems+hvdc_converters+dc_branches"
    pypsa_simple_link:
      allowed_for: "QUALIFIED_POINT_TO_POINT_ONLY"
      reverse_lossy_flow: "BLOCK_WITHOUT_EXPLICIT_BIDIRECTIONAL_MODEL"
      reactive_control: "SIDECAR_ONLY"
```

### 5.4 Beispiel: Limits und Export-Vorbedingungen

```yaml
contract_version: "1.0.0"
mapping_policy_id: "limits-export-v1"
limits:
  current_to_apparent_power:
    function_id: "three_phase_i_to_s_at_declared_voltage"
    function_version: "1.0"
    required_inputs: ["current_limit_a", "voltage_assumption_kv", "context"]
  unknown_duration: "NO_EMERGENCY_CLASS_INFERENCE"
  direction: "PRESERVE_TERMINAL_AND_POSITIVE_NEGATIVE"
exports:
  update_imported:
    require: ["raw_graph_blob", "original_mrids", "profile_headers",
              "mapping_identity", "loss_manifest", "validated_delta"]
    reject_change_outside_supported_fields: true
  create_from_pypsa:
    require: ["new_authority_namespace", "equipped_terminals", "base_voltage",
              "profile_set", "explicit_ssh_state", "loss_manifest"]
    missing_required_cim_entity: "BLOCK"
quality:
  no_implicit_zero: true
  default_mode: "BLOCK_ON_ELECTRICAL_DEFAULT_UNLESS_APPROVED"
  missing_country_for_active_bus: "BLOCK_MODULE1_HANDOFF"
```

***Schema-Anmerkung:*** Die YAML-Blöcke definieren eine **fachliche Zielsprache**. Bezeichner wie `RatioTapChanger.step` sind logische Pfade; die gültige tatsächliche Klassen-/Profilassoziation wird je CGMES-Familie und Schema geprüft. Die Blöcke sind **keine** lauffähige Konfiguration und keine Aussage, dass sämtliche genannten Attribute in beiden Releases identisch existieren.

## 6. Vorbildanalyse: keine ungeprüfte Schemaübernahme

| Vorlage | Wertvoll für Modul 0 | Nicht übernehmen / Grenze |
|---|---|---|
| **PyPSA-Komponentenattribute** [P1–P3] | klarer terminalbasierter `Bus, Line, Transformer, Generator, Load, ShuntImpedance, Link`-Export; Status-/Parameterkonvention und per-unit-Dokumentation | PyPSA besitzt keine vollständige CGMES-Origin-/Terminal-/Boundary-/Tap-/Duration-Limit-Rückexportsemantik; Link ist kein vollständiger DC-Konverter |
| **SiennaSchemas** [S1] | zentrale, eindeutig typisierte Schema-/Einheitenquelle, Sprach-/DB-Schema-Generierung, maschinenprüfbare Units | Schemafamilie ist kein 1:1-CGMES-/PyPSA-Zielvertrag; fachliche CIM-Relationen und Originalgraphen nicht aus Typkatalog allein ableitbar |
| **Power Grid Model IO** [G1] | deklarative Mapping-Dateien, Units, Substitutions-/Auto-ID-Policies, Converter-Grenzen, nachvollziehbare Tabellentransformation | orientiert sich an PGM und dokumentiert Vision-/pandapower-Konverter; **kein Beleg** für volle CGMES-Round-trip- oder Europa-Übertragungsnetzunterstützung |
| **cgmes2pgm_suite / cgmes2pgm_converter** [G2] | relevante Vergleichsperspektive für Version 2.4/CIM16 und 3.0/CIM100, Graph-/Conversion-/State-Estimation-Prozesse | nach eigenem Projektziel SPARQL/PGM- und Zustandsschätzungsweg; kein direkter Nachweis eines vollständigen, identitätserhaltenden CGMES↔PyPSA-Exports. Backendentscheidung bleibt offen |

**Übernahmeentscheidung:** übernehmen **Designprinzipien** (units-as-schema, Mapping-/ID-Konfiguration, Konverter-Gates), **keine** externe Tabellenstruktur ungeprüft als Canonical v1. Der externe Backendadapter muss sich an dieses Schema anpassen, nicht umgekehrt.

## 7. Vertragsausgabe an Modul 1

**Pflichtoutput `DetailedNetworkReference v1`:** `network_revision_id` + Graphhash + Mapping-Policy-Hash; Tabellen/IDs für `buses`, AC-Inseln, aktive orientierte `lines` und `transformers`, synthetische Sternäste, effektive `x_pu` (mit Basis), limitierender Grenzwert **mit Typ und Gültigkeit**, `in_service`, Land je Originalbus, `pst_offset`, HVDC-Ports/Nettoeinspeisungen und Equipment→PyPSA-Mapping. Zusatz `sidecar`: Original-CIM-Graphanker, alle Originalgrenzen, Boundary, Terminal-/Topology-Trace, Geo und lossy approximations.

**Capability Matrix:**

- `CANONICAL_READY` = Datensatz mit referenziell konsistenten Originalobjekten, auch falls PyPSA-Sonderabbildung noch nicht qualifiziert ist.
- `PYPSA_ACPF_READY` = alle aktiven Sonderkomponenten im AC-positiven Sequenzmodell darstellbar, LF-Regeln/Slack qualifiziert.
- `PYPSA_LPF_READY` = wirksame PST-/Tap-/HVDC-Offsets und Inselbalancen dokumentiert und korrekt einsetzbar.
- `REDUCTION_ADAPTER_READY` = *zusätzlich* vorhandener `tyndp_reduce.pypsa_adapter` akzeptiert Komponenten **tatsächlich**; am Basiscommit bestehen harte Einschränkungen. Sonst `UNSUPPORTED_FOR_REDUCTION_ADAPTER`.
- `EXPORT_UPDATE_READY` und `EXPORT_CREATE_READY` stehen **unabhängig** zu den anderen Freigaben (Details in 50).

Für Modul 1 wird die gefrorene Detailansicht **nicht** mit Dispatch-/Wetterzeitreihen aufgefüllt. Spätere Zeitreihen referenzieren deterministisch die `bus_id`/`equipment_id` und dieselbe `network_revision_id`; ihre Zeitbasis und Provenienz werden im Modul 1 gesondert geprüft. **Keine Reaggregation** oder Austausch von Originaltopologie während der Kalibrierung.

## 8. Offene Implementierungsverifikationen und Quellen

Diese Spezifikation ist **solver-free**; noch nicht belegt sind die tatsächlichen Backend-Klassen-/Profilabdeckungen, versionierte CGMES-3.0-Attributpfade, die exakte PyPSA-3W-/PST-Ybus-Projektion auf einem Realnetz, realistische Boundary-Assemblerfälle und das aktualisierte Modul-1-Gate. Sie sind **Testspezifikation**, keine Ergebnisse.

- **[C1]** ENTSO-E, [CGMES Library v2.4/v3.0](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/).
- **[C2]** IEC, [61970-600-2:2021 Exchange Profiles](https://webstore.iec.ch/en/publication/63867) und 61970-600-1:2021 (via C1).
- **[C3]** ENTSO-E, [CGMES 2.4.15 profiles](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140807_ENTSOE_CGMES_v2.4.15.pdf), [CGMES Implementation Guide](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/160315_ImplementationGuide_CGMES_2_4_15.pdf).
- **[C6]** ENTSO-E, [Boundary and Reference Data Exchange v1.0](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/Boundary_and_reference_data_exchange_specification_v1.0.pdf), insbesondere CGMES-3.0-Übergang von EQBD zu Core-EQ.
- **[C5]** [CGMES PowerTransformerEnd interpretation / 3-winding star](https://modellen.netbeheernederland.nl/cgmes/Short%20Circuit/PowerTransformerEnd/); am jeweiligen Profil zu verifizieren.
- **[P1]** PyPSA, [Design & Components](https://docs.pypsa.org/latest/user-guide/design/).
- **[P2]** PyPSA, [AC Power Flow: line/transformer admittance, signs and controls](https://docs.pypsa.org/latest/user-guide/power-flow/).
- **[P3]** PyPSA, [Lines](https://docs.pypsa.org/latest/user-guide/components/lines/), [Transformers](https://docs.pypsa.org/latest/user-guide/components/transformers/), [Generators](https://docs.pypsa.org/latest/user-guide/components/generators/), [Links](https://docs.pypsa.org/latest/user-guide/components/links/).
- **[S1]** [SiennaSchemas pipeline](https://github.com/Sienna-Platform/SiennaSchemas/blob/main/docs/PIPELINE.md).
- **[G1]** [Power Grid Model IO: converters, mapping, units and IDs](https://power-grid-model-io.readthedocs.io/en/stable/).
- **[G2]** [SOPTIM CGMES2PGM Converter und Suite (Beschreibung)](https://github.com/SOPTIM/cgmes2pgm_converter).
- **[R1]** [IoSN Band II](../IOSN_2026_Band_II_PyPSA_Implementierung.md) und [Repository Audit](../../REPOSITORY_AUDIT.md) am verbindlichen Basiscommit.

**Status dieser Datei:** `DESIGNED_NOT_EXECUTED`. Die Freigabe erfolgt allein als **Implementierungsgrundlage**; Datensätze/Backends müssen gegen [50_VALIDATION_CONTRACT.md](50_VALIDATION_CONTRACT.md) später nachweislich geprüft werden.
