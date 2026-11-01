# M2 — 60 ARCHITECTURE DECISION RECORD
## Integrations- und Governanceentscheidungen für Modul 0: CGMES ↔ PyPSA

**Stand:** 2026-11-01. **Historische M2-Disposition:** `M2_DESIGN_DECISIONS_ADOPTED_PENDING_M3_STATIC_REVIEW`. **Korrigierte normative Fassung:** [85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md), CAN/2.0.0, nach M3-REPAIRS_REQUIRED (P1=7); der frühere M3-Bericht wird nicht rückwirkend verändert. Entscheidet Design und Umsetzungsscope, **nicht** Konformität, Test-PASS oder Produktionsfreigabe.
**Entscheidungsbasis:** [00 S-GOV](00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md), [10 Requirements](10_REQUIREMENTS.md), [20 Backend](20_BACKEND_ASSESSMENT.md), [30 Canonical](30_CANONICAL_DATA_CONTRACT.md), [40 Architecture](40_SOFTWARE_ARCHITECTURE.md), [50 Validation](50_VALIDATION_CONTRACT.md).

## 1. Autorität, Evidenz und verbindliche Auslegung

Der Backend-Fachrücklauf wurde unter Commit `d3ab97e170eb6eeb5064dc3058b497f5c954af58` und die Anforderungs-/Datenvertrags-/Validierungsspezifikation unter `f2705338e3d79e12a46ae44a8d7a008a81c04b3b` abgeschlossen und unverändert im S-GOV-Ausgangsbranch übernommen (`e595335d511af6f8c9c05c88276553363ed37045`). Die beiden Berichte sind wissenschaftliche Fakten-/Designvorlagen; für **explizite K-01…K-07-Konflikte** gelten dieses ADR und die präzisierten Schnittstellen in `40`/`70`. **Für die sieben M3-P1-Designwidersprüche gilt zwingend 85 (CAN/2.0.0)**, einschließlich neuem Originaltabellenregister, TopologyKind, ProjectionQuality, ExportRoute, REQ-009/T-06, atomarem Publish und DNR/1.0.0. Die REQ-/T-IDs sowie die nicht widersprüchlichen physikalischen Definitionen aus `10`/`30`/`50` bleiben erhalten.

**Evidenzklassen:** `D` dokumentierte Upstream-Funktion; `C` im Quellcode gefunden; `T` Testinventar vorhanden (nicht ausgeführt); `M` datierte fachliche Pflege; `P` hier getroffene Designentscheidung; `U` ungeklärt. Kein `D/C/T` ist für sich ein ausgeführter numerischer Nachweis. Ein neues internes `PASS` setzt Test-/Versions-/Fixture-/Capability-bezogene Ausführungsevidenz voraus. Kein interner PASS ersetzt eine ENTSO-E-/IEC-Zertifizierung.

## 2. ADR-001 — Externes Backend statt eigener CIM-/RDF-Engine

**Entscheidung:** `PowSyBl/powsybl-core` über `PyPowSyBl` als **primärer** produktseitig angestrebter Format-Backend-Pfad; `VeraGrid` als **zweiter Adapterkandidat**, nicht automatisch parallel zu implementierende zweite Runtime. Eigene Codebasis beginnt bei Paket-/Provenienzverwaltung, Backend-Port, kanonischer Normalisierung, elektrischer Projektion und kontrolliertem Export. Extern gepflegte Formatreleases erhalten Upstream-Verantwortung für RDF/XML, CGMES-Versionsprofile und Grundserialisierung.

**Begründung:** PowSyBl dokumentiert importierbare und exportierbare CGMES-Kernprofile EQ/TP/SSH/SV, zweistufiges RDF/SPARQL-Importverfahren, Node-Breaker/Bus-Branch-Interpretation, CGM-Subnetwork/IGM, Profile-Metadata- und gezielten CGM-SSH/SV-Update-Export. PyPowSyBl hat Pandas/Netz-API; fachliche CGMES-Pflege im Oktober 2026 ist im Fachbericht belegt. VeraGrid bietet native Python-CGMES-Klassen beider Versionen, Import und Export, allerdings weniger belegte echte CGM-Delta-Exportsemantik. Die neue Architektur vermeidet, dieselben CGMES-Schemaregeln selbst zu warten.

**Einordnung der übrigen Kandidaten:** CIMpy/CIMgen und PyCGMES sind rohe CIM-/Schema-/Klassenbausteine und würden erhebliche eigene Topologie-/Transformer-/Limit-/Exportlogik erfordern; SOPTIM `cgmes2pgm_converter` mit `cgmes2pgm_suite` bleibt Referenz für SPARQL, YAML, State Estimation und partiellen SV-Export, aber kein allgemeines CGMES-System-of-Record; PowerGridModel-IO ist ein gutes Mapping-/Unit-Designvorbild, kein vollständiger CGMES-Serializer; pandapower und dessen PyPowSyBl-Konverter sind Vergleichs-/Testreferenzen; Sparlectra.jl ist ein unabhängiges Julia-Referenzprojekt, kein vorrangiger Python-Backendvertrag; SiennaSchemas hilft bei Typisierung, ist **kein** CIM/CGMES-Parser. Das zusätzlich vom Nutzer genannte unbekannte Julia-Projekt bleibt offen und ist **nicht** zur Voraussetzung des Architekturabschlusses erklärt.

**Konkretisierung M3-P1-05:** Eine produktive VeraGrid-Runtime bleibt optional; REQ-009/T-06 verlangt vor CANONICAL_IMPORT_READY trotzdem einen zweiten **unabhängig erzeugten** BackendSnapshot (minimaler read-only VeraGrid-Fixture-Prüfadapter genügt), siehe 85 §6. Ohne T-06 nur CANONICAL_IMPORT_PROVISIONAL/REQ-009 NOT_ASSESSED, nicht READY. **Konsequenz:** Keine direkte CGMES-Abhängigkeit im PyPSA-Adapter. Späterer Versions-Pin und API-Witness über PowSyBl/PyPowSyBl zwingend; die breite DataFrame-API alleine beweist keinen vollständigen Originalgraph-Zugriff.

## 3. ADR-002 / K-01 — Versions-/Anwendungsfallgebundene Profilpolicy

**Entscheidung:** Keine globale Pflicht, bei **jedem** Import EQ+TP+SSH+SV+EQBD+TPBD+GL zu verlangen. Profilvorgaben sind eine Funktion von (`CGMES-Familie`, `Exchange-/Boundary-Policy`, `Single-IGM/CGM`, `Input-/Export-Operation`, `geforderte Capability`). Profilmetadaten, URI und FullModel-Abhängigkeiten sind verbindlicher als Dateinamen.

| Operation / Ziel | CGMES 2.4.15 | CGMES 3.0 | M0-Regel |
|---|---|---|---|
| Stationärer unsolved Import | `EQ`, `SSH`; `TP` bei NODE_BREAKER optional bzw. für BUS_BRANCH zwingend; `SV` darf fehlen | analog; versionsrichtige URIs | NODE_BREAKER: TP-Abgleich oder nachgewiesene EQ/SSH-Switch-Ableitung. BUS_BRANCH: **TP zwingend**, sonst BLOCK; keine erfundenen ConnectivityNodes. Originalterminal-/SourceStations-Provenienz in 85 §2 |
| Solved AC-SV-Validierung | EQ/SSH/zuverlässige TP-Basis + passendes SV | analog | Ohne geeignete SV-Referenz `NOT_APPLICABLE_NO_SV` statt fingiertem PASS |
| Single-/Multi-IGM, Boundary | benötigte EQBD/TPBD-Referenzen des tatsächlichen Austauschvertrags | referenzierte Core-EQ-/Boundary-Objekte, ggf. zulässiger EQBD-Übergang; **kein 3.0-TPBD als Pflicht** | Fehlende benötigte Cross-Model-Referenz BLOCK, länderübergreifende Kanten bleiben erhalten |
| GL/Geo | optionales GL importieren, wenn geliefert | analog | Ohne GL: Koordinaten MISSING, Länder- und Verbindungszuordnung nicht erfinden |
| Update-Export | belegtes SSH (pro IGM) / SV (CGM), ggf. qualifiziertes TP | versionsbedingt analog | Keine pauschale GL/EQBD/TPBD-Neuschreibung; unveränderte Originalpakete/Refs behalten |
| Neuaufbau | EQ/TP/SSH aus expliziter Konstruktionsspezifikation, SV nur solved | analog | Separate CREATE-Capability und neue Authority/IDs; kein historischer IGM-Anspruch |

CGMES-3.0-Boundary-Details müssen dem tatsächlichen vereinbarten Austauschprofil folgen. Unkontrollierte Vermischung verschiedener CGMES-Familien, unpassende FullModel-Dependencies oder unbelegte Querverweise führen zu `BLOCK`. Der Backendbericht-Gate "G1 Vollprofil" ist daher ein **Fixture-Stresstest**, **keine** universelle Importscope-Anforderung.

## 4. ADR-003 / K-03 — Identität: mRID, RDF-Subject und Profil-Occurrence trennen

**Entscheidung:** Das logische Quellobjekt wird unabhängig von Profil/Datei identifiziert. Normativ:

~~~text
source_entity_key = (qualified_identity_namespace, identity_kind, identity_value)
identity_kind ∈ {MRID, RDF_SUBJECT}
source_occurrence_key = (source_entity_key, source_model_id, profile_uri, source_file_sha256, rdf_subject)
asset_id = canonical logical electrical asset identity
view_id = deterministic derived PyPSA/Star/Projection identity
~~~

- `qualified_identity_namespace` enthält einschlägige Authority-/Exchange-/CIM-Familien-Information, jedoch **nicht** unbesehen Profilkürzel EQ/TP/SSH/SV: ein Objekt mit gleichem qualifiziertem mRID wird nicht viermal angelegt.
- Ein mRID-loses Objekt (z. B. bestimmte State-Variables-RDF-Ressourcen) wird mittels RDF-Subject/URI + maßgeblichem Namespace/Grafkontext und dessen Occurrences referenziert; kein erfundenes historisches mRID.
- Kollidierende mRIDs/Klassen/Authorities werden nicht per "last file wins" zusammengeführt; Konflikt-Ledger und `BLOCK`.
- Die source occurrence dokumentiert pro Profil die Originalrepräsentation; `ModelHeader`, `DependsOn`, `Supersedes`, Aliases und RDF-Beziehungen bleiben gesondert erhalten.
- Original-ID, IIDM-ID, Canonical-ID, PyPSA-ID und synthetischer Starbus dürfen nicht ohne explizites Mapping gleichgesetzt werden.

**Normative CAN/2.0.0-Tabelle in 85 §1 löst M3-P1-01 vollständig auf:** source_entities/source_objects/source_occurrences mit vollständigen PKs/FKs und identity_kind, nullable mRID und Original-BlankNode-/Graphscopes, deterministischen Revisionen; 30 bleibt unveränderte historische Eingabeevidenz. **Explizite Normpräzisierung gegenüber `30`:** Das dortige konzeptuelle `source_key=(model_authority_id,cgmes_profile_family,source_mrid)` darf nicht zu einer profilspezifischen Mehrfachidentität führen; `source_mrid` ist bei RDF-Objekten ohne mRID nullable. Das Tabellenregister wird im ersten physischen Schema-Migrations-/Implementierungsmakro mit dieser normativen Regel umgesetzt, nicht rückwirkend im unmodifizierten Arbeitsdokument überschrieben. M3 prüft, ob der Vorrang eindeutig ist.

## 5. ADR-004 / K-04 — Länder- und Geoprovenienz bei synthetischen Netzknoten

**Entscheidung:** Originale, für nachfolgende Netzreduktion freigegebene AC-Busse benötigen prüfbaren `country_code` (versioniertes ISO-Registry-/Sondercodeverfahren); eindeutige Landesidentität darf nicht aus geographischer Nähe allein abgeleitet werden. Cross-border-Geräte besitzen endportbezogene Länder-/Authority-Zuordnung. Ein 3W-Sternersatz erhält `bus_role=SYNTHETIC_3W_STAR`, `source_transformer_id`, `country_code=NULL` und keine geographische Koordinate, sofern nicht als synthetisches Layout gesondert markiert. **Konditionale FK-Regel:** reale Busse `country_code NOT NULL` für REDUCTION_CAPABILITY, synthetische Busse `country_code IS NULL` erlaubt/erwünscht; Letztere niemals als reale nationale Knoten in Land-Clustering oder Cross-border-Statistik zählen.

85 §§1–2 führt dies als bedingtes Country-FK-Schema inklusive source_hierarchy, terminal_source_origin und Country-Konflikten aus; ein IIDM-Vertreter-Substation-Attribut ist keine Quelle für das originale Land. Damit wird die pauschale Länder-NOT-NULL-Spalte in `30` für **abgeleitete synthetische Busse** präzisiert. Fehlen echter Country-Information ist kein Anlass, ein Land zu erfinden. Beim reinen Canonical-Import kann Country noch MISSING sein; REDUCTION_ADAPTER_READY bleibt dann BLOCKED.

## 6. ADR-005 / K-02 — Update-Export beruht auf originalem Modell, nicht auf PyPSA-Rekonstruktion

**Entscheidung:** Zwei Exportoperationen mit ausdrücklich getrennten Verträgen:

- `UPDATE_IMPORTED`: originale Input-Dateien, Modell-/Profil-/Boundary-Kontext und ID-/Mapping-Ledger bleiben Autorität. Nur pro Backend/CIM-Version nachweisbar **freigegebene** Schreibfelder, insbesondere SSH-Sollwerte/Tap-/Statusfelder soweit belegbar, und SV **nur aus nachgewiesen geeignetem gelösten Snapshot**. PowSyBl kann CGM-IGM-SSH/CGM-SV und optional TP ausgeben, aber **keine allgemeine verlustfreie 1:1-RDF-Patch-API** ist belegt. Zur Lieferung gehören originale unveränderte referenzierte Profile und neue geprüfte Zustandsprofile; Source-Graph-/Semantic-Diff/Headers/Dependencies müssen korrekt sein. Für unbekannte CIM-Extensions darf der Patch keine versteckte Löschung verursachen. Falls die Identity-/Graph-Provenienz nicht tatsächlich zugänglich ist: `BLOCK_EXPORT_UNPROVEN`, statt stillen 1:1-Round-Trip zu behaupten.
- `CREATE_FROM_PYPSA`: neues explizites, synthetisches CGMES-Equipment- und Profilmodell mit neuem Authority-Kontext/IDs; nur bei vollständigen Konstruktionsvorgaben und eigenen Konformitätsprüfungen. Kein Versprechen, historische TSO-Schaltanlagen, mRIDs oder Boundary-Modelle aus Bus-Branch-PyPSA zu restaurieren.

**M3-P1-04-Freeze der Exportoperationen (85 §5):** CGM_QUICK_SSH_SV erzeugt dokumentiert **immer** SSH je IGM und gemeinsam ein SV (Profilauswahl ignoriert); nur bei gültigem neu gelöstem SV. MANUAL_IGM_SSH ist eine **gesondert** zu qualifizierende Python-/Metadaten-/FullModel-/Dependencies-/Graph-Diff-/Reimport-Route für SSH-only; ohne Witness BLOCK_EXPORT_UNPROVEN. Erforderliche Mutationsklassen: STATE_NON_TOPOLOGY, STATE_TOPOLOGY_AFFECTING (v1 default BLOCK), STRUCTURAL_EQ_TP (UPDATE v1 BLOCK), SYNTHETIC_CREATE (nur CREATE). **Strukturelle Änderungen** an EQ/TP, Änderung von Source-Terminals, Originalschaltern oder reduzieren/aggregieren des Netzes sind im **ersten Update-Exportumfang nicht erlaubt**. Ein neuer CGMES-EQ-/TP-Export oder CGM-Strukturumbau erfordert gesonderte Qualifikation. `Update-from-file` der Python-API ist ein **Import-Update**, nicht automatisch die Freigabe für sämtliche exportseitige Änderungen.

**Nicht akzeptierte Alternative:** einen eigenen generischen RDF-XML-Serializer/Patcher zur Rettung beliebiger Metadaten bauen, ohne den Upstream zu nutzen. Diese Alternative würde dem Wartbarkeitsziel widersprechen und wird nur bei explizitem späterem Scopeentscheid neu bewertet.

## 7. ADR-006 / K-07 — Elektrische Projektion ist zweck- und wirkungsgebunden

**Entscheidung:** `canonical_source` erhält Originalparameter, Anschlüsse, Richtungen, Limits und Klassen. `electrical_projection` und `PyPSA detailed view` erhalten eine ausdrücklich deklarierte Exaktheitsklasse; nicht mit CGMES-Original-Identität verwechseln. Referenzprüfung anhand komplexer Zwei-/Dreiport-Admittanz und richtiger Leistungsverlustbilanz hat Vorrang vor bloßer Parameter-/Zeilenanzahl.

| Komponente | Akzeptierte v1-View | Einschränkung und Capability |
|---|---|---|
| Positive-sequence AC Line | `Line` mit r/x Ω, g/b S, gültiger Portreihenfolge | `EXACT` nur bei PI-/Ybus-Prüfung |
| 2W / PhaseTap / RatioTap | `Transformer` mit geprüften pu-Basen/Tap-Seite/φ | Tabellen-/Nichtlinear-Steps und Remote Controller ggf. `APPROX`/`UNSUPPORTED` |
| 3W | drei 2W-Staráste plus synthetischer Bus, 3W-Original im Ledger | `EXACT` nur elektrisch nach 3-Port-Kron-Y-Äquivalenz; historische Semantik im PyPSA-Core nicht exakt |
| Generator/Load/ExternalInjection | positive Gen-injection / positive Load-demand, deklarierte PQ/PV/Slack | Quellenzeichen, Q-/Regel-/Szenariodaten müssen separat erhalten werden |
| Shunt | effektive positive-sequence G/B | Stufen-/spannungsabhängige Controls nur `APPROX` oder `UNSUPPORTED` |
| HVDC | port-/verlustqualifizierter PTP-Link oder stationäre AC-Port-Injektion | Ein einfacher verlustbehafteter reversibler Link bildet Rückwärtsverluste regelmäßig falsch; MTDC nicht generisch freigegeben |
| Limits | qualifizierter Study-Proxy in PyPSA + original mehrdimensionaler Limit-Contract | Duration/Direction/Season/N-1 nicht zu einem unbelegten `s_nom` reduzieren |

**K-07 — Verbindliche objektbezogene Capability-Matrix.** Die Stufen sind *bedingte Zielklassifikationen* des Entwurfs, **keine aktuell bestandenen Qualifikationen**. Jede tatsächlich gewählte Stufe wird pro Gerät/Feld/Port, Netzwerkrevision, CGMES-/PyPSA-Version und Projektionsfunktion durch die Tests T-07…T-20 belegt; `EXACT` bezieht sich nur auf eine benannte elektrische oder informationssemantische Eigenschaft, nicht pauschal auf CIM↔PyPSA-Identität.

| Gegenstand | `EXACT` nur falls | `APPROX` zulässiger, dokumentierter Downscope | `UNSUPPORTED` / harte Sperre |
|---|---|---|---|
| ACLineSegment / PI | Orientierung, OHM/S, Shunt-Aufteilung und Zweitor-Y übereinstimmen | nur explizit geprüfter Ersatz- oder reduzierter Modellzweck | singuläre aktive Impedanz, unklare Ports/Basen |
| EquivalentBranch | ursprüngliche Ersatz-Identität im Canonical/Sidecar und passende elektrische Zweitorwirkung | als `Line` elektrisch reproduzierbar, aber nicht als physische Leitung umetikettiert | unbekannte Steuer-/Quellwirkung oder unklare Endports |
| 2W-Transformer | EndNumber, ratedU/ratedS, Modell T/PI, Tap-Seite, Ratio/Phase und Zweitor-Y nachgewiesen | Regelungsprioritäten, ferne Sollwerte oder Step-Kennlinien nur als dokumentierte Arbeitspunktannäherung | unbekannte Tap-Tabelle/-Seite oder inkompatible Admittanz |
| 3W-Transformer | 3W-Original mit drei Ports/Ends erhalten und Kron-reduziertes Dreiport-Y inklusive Shunts/Taps äquivalent | drei 2W-Sternäste sind strukturell nur PyPSA-Sicht; historische 3W-CIM-Struktur im Sidecar | singuläre Sternzweige, fehlendes Endmapping, nicht darstellbare Taps |
| PST / Phase-Tap | physikalischer Shift, Vorzeichen und affine Flusswirkung je Port qualifiziert | fixierter Shift ohne vollständige Remote-/Automatikregelung | unqualifizierte variable PST-Regelung, falsche Richtung oder unbekannter Shift |
| Generator/Load/ExternalInjection | stationäre P/Q-Kernwerte, Service, Bus und Quellzeichen eindeutig sind | ZIP/PV/Slack-/Q-Curve-/Remote-Control-Einschränkungen ausdrücklich sichtbar | nicht rückführbare Quelle, widersprüchlicher Betriebszustand |
| Shunt | konstante wirksame G/B bei geprüftem Schaltzustand und Vorzeichen | nichtlineare Stufenregelung nur am dokumentierten Operating Point | fehlende Stufendaten mit erforderlicher variabler Wirkung |
| HVDC PTP | AC-/DC-Quellports, P- und Verlustbilanz bei bestimmtem Flussregime geprüft sind | fester gerichteter Link, verlustfrei reversibler Link oder explizite AC-Port-Ersatzinjektion mit begrenztem Zweck | ungeprüft verlustbehaftet *reversibler* Einzel-Link, MTDC als simpler PTP-Link, fehlende DC-/Konverterdaten |
| Operative Limits | komplettes Original-`OperationalLimitSet` mit Dauer, Richtung, Terminal, Saison, Zustand im Canonical/Sidecar erhalten bleibt | ausgewähltes PyPSA-`s_nom` als gekennzeichneter Study-Proxy auf deklarierter Spannungsbasis | unzulässige A→MVA-Umrechnung, implizite Notfall-/N-1-Grenze |
| Country/GL/Boundary | reale Länder-/Authority-/Terminalreferenzen und originales GL/CRS erhalten | Buskoordinate aus belegtem Station-Zentroid, ausdrücklich `DERIVED`; 3W-Stern ohne reales Land | erfundene Geo-/Landesdaten, unauflösbare Cross-Model-Referenzen |

**Übernahme in `LossLedger`:** `source_object_id`, `component_type`, `field_or_relation`, `projection_id`, `exaktheitsklasse`, `mathematical_witness_id?`, `approximation_domain?`, `physical_effect?`, `capability_scope`, `policy_hash` werden je Zeile geführt. Ist ein erforderlicher `EXACT`-Witness nicht vorhanden, bleibt die beantragte elektrische Capability `NOT_ASSESSED`/`BLOCKED`; nicht nur eine verbale EXACT-Behauptung.

**M3-P1-03-Ergänzung:** Ein append-only, revisionsgebundenes **projection_quality**-Register und separate projection_witnesses nach 85 §4 sind bei jeder ElectricalView unabhängig von Exporttransaktionen verpflichtend; das exportgebundene loss_manifest bleibt eigenständig und kann Projektionswitnesses referenzieren. Ein unbekannter Parameter wird nicht auf PyPSA-Defaults (z. B. `r=0`, `tap_ratio=1`, `s_nom=∞`) als angebliches Quellattribut gesetzt. Jede Approximation ist feld-, objekt-, policy- und capability-bezogen im `loss_manifest` verzeichnet.

## 8. ADR-007 / K-05 — Capability-Gates statt konkurrierender G-Nummern

**Entscheidung:** Die alte Backend-G0…G6- und Contracts-G0…G5-Nomenklatur bleibt als **historische Unterabschnittsbezeichnung** erhalten. Kanonische neue Gate-Schlüssel sind:

| Neuer Gate-Schlüssel | Inhalt | Notwendiger späterer Testpfad |
|---|---|---|
| `ARCH-STATIC` | Dokumenten-, Schnittstellen- und REQ-Abdeckung | M3, rein statisch |
| `QUAL-FORMAT` | Familien-/Profile-/Header-/Dependencies-/Boundary-Handling | T-01–T-03 |
| `QUAL-IDENTITY` | Source IDs/RDF/Occurrences/FKs, Revisions-/Raw-Graph-Integrität | T-04–T-06 |
| `QUAL-TOPO-GEO` | Switch/TP/Islands, Länder-/Geo-Referenzen | T-07–T-11 |
| `QUAL-ELECTRICAL` | Geräte, pu/Ybus/Vorzeichen/HVDC/Limits | T-12–T-19 |
| `QUAL-PYPSA` | Projektion in AC-PF/LPF-Berechnungsmodell | T-20 plus relevante elektrische Tests |
| `QUAL-UPDATE-EXPORT` | originalgraphgestützter SSH/SV-Delta-Export, Ref-/Identity-Diff | T-21, T-24 |
| `QUAL-CREATE-EXPORT` | neuer CGMES-Graph, eigenständige synthetische Konformität | T-22, T-24 |
| `QUAL-SV-REF` | qualifizierter stationärer SV/AC-PF-Vergleich | T-23; N/A ohne gültige SV |
| `QUAL-OPS-PERF` | skalierte Multi-IGM-Memory-/Runtime-/Ressourcen- und Sicherheitsqualifikation | T-24 plus eigens definierte Leistungsfixture |
| `QUAL-M1-INTEGRATION` | echter bestehender Folgeadapter erfüllt DetailedNetworkReference | T-20 plus Adapter-End-to-End |

**M3-P1-05-Gate:** QUAL-IDENTITY/CANONICAL_IMPORT_READY verlangt REQ-009/T-06 mit tatsächlich unabhängigen Backendsnapshots; Single-Backend-Samples sind nur PROVISIONAL, bis T-06 PASS für den konkret bezeichneten Scope vorliegt. **Eine Zahl allein bezeichnet keinen Gate-Namen.** Ein `ARCH-STATIC PASS` setzt kein `QUAL-* PASS` und kein `REDUCTION_ADAPTER_READY` voraus. Status je Capability = `PASS`, `CONDITIONAL_WITH_NAMED_GAPS`, `BLOCKED`, `NOT_ASSESSED`, zusätzlich Vorbereitungszustand `DESIGNED_NOT_EXECUTED`.

## 9. ADR-008 / K-06 — Modul 1 und Detailnetzevidenz bleiben getrennt

**M3-P1-07:** M0 liefert das **verbindliche typisierte** DetailedNetworkReference/1.0.0 aus 85 §8 mit expliziten Source-/OperatingState-/Canonical-/Projection-IDs, Busrollen, gerichteten Branch-/Port-FKs, Units/Bases, PST-/HVDC-Wirkungen, Limits, Original-Source-Mappings, Quality-/Capability-Manifests und einem separaten M1-Handshake. **Historische Kurzbeschreibung:** M0 liefert `DetailedNetworkReference v1` plus original-/topology-/geographic-/constraint sidecar. Wetter-/Last-/RES-/Dispatchzeitreihen, Kostenoptimierung und IoSN-Busmaps bleiben außerhalb von M0 und dürfen die eingefrorene Detailnetzrevision nicht mutieren. Aktuelles `src/tyndp_reduce/pypsa_adapter.py` ist ein absichtlich eingeschränkter, eininselig-leitungsbasierter DC-/PTDF-Eingang; Transformer/Links/Storage/PST/multi-island werden dort noch nicht qualifiziert. 

**Folge:** `CANONICAL_IMPORT_READY`, `PYPSA_ACPF_READY` und `PYPSA_LPF_READY` führen **nicht** zu `REDUCTION_ADAPTER_READY`. M1-Adaptererweiterung (PST/HVDC/3W/mehrere Inseln, zeitlich bilanziertes Gesamtmodell) erfordert späteren eigenen Implementierungsauftrag. Die richtige Source-/Endpoint-Country-Zuordnung bleibt im M0-Sidecar; Ländergrenzen dürfen Netzflüsse nicht unterbrechen.

## 10. ADR-009 — Persistenz, Mapping, Change-Sicherheit

**Entscheidung:**
- Erste physische Umsetzung: unveränderliches content-addressed Raw-Delivery-Archiv + JSON-Manifest + SQLite-Canonical-/Provenienz-Store (Python-`sqlite3`), weil dies bei einem Netz von mehreren Tausend Busknoten relational überprüfbar und ohne zusätzlich zu betreibende Infrastruktur auskommt.
- DataFrames werden als PyPSA-View erzeugt; Parquet/Arrow als **optionaler** abgeleiteter Cache erst nach Leistungs-/Fidelity-Qualifikation. Persistenzentscheidung darf den **logischen** Datenvertrag nicht verändern.
- Konfigurierbare YAML-Mappingdateien (Schema-/Rule-/Policy-Version) dürfen **nur** registrierte, deterministische, geprüfte elektrische Transformationsfunktionen auswählen. Kein untrusted `eval` und kein frei importierbarer Python-Funktionsstring.
- **M3-P1-06-Publish-Protokoll:** verifizierte durable immutable Blobs → vollständiges durable Manifest → *einzige* SQLite-CAS-COMMITTED-Pointertransaktion als Publikationszeitpunkt. Crash vor Commit ⇒ alter Stand; nach Commit ⇒ vollständiger neuer Stand; idempotente Retries, orphan-GC und Fehlbestand-FATAL nach 85 §7. SQLite alleine ist keine atomare FS-Transaktion. Keine ungeprüften Teil-Exporte.
- PyPowSyBl/Java/RDF-Speicher wird über BackendSession isoliert und nach Auftragsende geschlossen; kein langfristiger Live-Handle als Ersatz eines Originalarchivs.

**Nicht festgelegt:** eine produktive DB-/Cloud-Architektur, verteilter Triplestore oder paralleler bidirektionaler VeraGrid-Implementierungszwang. Änderungen an diesem PoC-Profil erfordern einen begründeten Folge-ADR.

## 11. Noch offene, nicht als M2-Befunde 'geheilte' Qualifikationsrisiken

| Risiko | Ursache | Regel in M2 | Nachweis vor Freigabe |
|---|---|---|---|
| `R1-ORIG-ID` | Original-RDF-/Modellheader-/Alias-/mRID-Graph nicht automatisch vollständig durch Python zugänglich | Immutable Archive, IdentityEvidence mit UNKNOWN- und BLOCK-Semantik | Pinned Backend + T-04/T-21/Graph-Diff-Witness |
| `R2-BOUNDARY-GL` | Export unterstützt nicht allgemein das Neubilden sämtlicher Boundary-/GL-Profile | Original unverändert, kein unsupported rewrite | Multi-IGM 2.4/3.0 F04/F08, Version-/Profile-Gates |
| `R3-DEVICE-YBUS` | 3W, PST, Tap-/Shunt-/HVDC-Semantik nicht 1:1 durch PyPSA | Exact/Approx/Unsupported, Sidecar | T-12…T-20; AC-/LPF-/SV falls geeignet |
| `R4-M1-GAP` | existing reduktionsadapter rejects complex components | Separate REDUCTION_ADAPTER_READY | echtes M1-End-to-End |
| `R5-VERSION-SCALE` | Java/Python/CGMES Versionen, Lizenz für Testdaten, RAM, Laufzeit | Version pins, Lizenzmanifest, separated capability | T-01…T-24 + qualifizierte 6k+ Bus/CGM-Skalierung |

**Technischer Stop-/Fallback-Punkt:** Scheitert ein zwingender PowSyBl-Nachweis zur Quelle/Identity/Exportinversen, darf nicht durch ein unsichtbares Feldmapping "gerettet" werden. Entweder wird nur die belegte **Import-/PyPSA-Capability** freigegeben, oder ein VeraGrid-Adapter nach denselben Canonical-/Graph-Gates als getrennte Variante geprüft. Eine erzwungene Totalfähigkeit von Backend B ist nicht vorausgesetzt.

## 12. Entscheidungen, Geltung und Reifegrad

| ADR | Resultat | Status |
|---|---|---|
| 001 Backend | PowSyBl primär, VeraGrid Alternative | `ADOPTED_DESIGN`; Backend-Eignung noch bedingt |
| 002 CGMES-Profilmatrix | Version-/Capability-bedingt; kein pauschales TPBD für 3.0 | `ADOPTED_DESIGN` |
| 003 ID-Semantik | profilübergreifender Quellschlüssel, mRID nullable, RDF-Subject-Identität | `ADOPTED_DESIGN` |
| 004 Länder | real-Country hart bei M1; künstlicher Sternbus NULL erlaubt | `ADOPTED_DESIGN` |
| 005 Export | Originalmodell + erlaubte Delta-Updates; Create separat | `ADOPTED_DESIGN`, Full-Fidelity offen |
| 006 Komponenten | zweckgebundene elektrische Äquivalenz und Loss-Manifest | `ADOPTED_DESIGN`, numerisch offen |
| 007 Quality-Gates | `ARCH-*` / `QUAL-*` statt G-Nummern-Konflikt | `ADOPTED_DESIGN` |
| 008 Modul 1 | getrennte Capability; keine stille Reduction-Integration | `ADOPTED_DESIGN` |
| 009 Mapping/Persistenz | versionierte YAML/Functions; Raw+SQLite; klare Transaktionen | `ADOPTED_DESIGN` |

**Historische S-GOV-Disposition vor M3:** `M2_DESIGN_DECISIONS_ADOPTED_PENDING_M3_STATIC_REVIEW`. **Reparatur-Normstand:** 85 spezifiziert alle sieben P1 als SPECIFIED_FOR_STATIC_CHECK. Die abschließende S-GOV-Entscheidung ist in [90](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md) festgelegt: **ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING**, ausschließlich dokumentarisch, nicht als Änderung des unabhängigen M3-REPAIRS_REQUIRED-Befunds und nicht als Runtime-PASS. Der Abschluss eines unabhängigen M3-Reviews kann einen **dokumentarischen Architektur-Freeze** begründen, aber nicht eine ausführbare CGMES-/PyPSA-/Exportfreigabe. Die spätere M4-Implementierung wird ausschließlich bei gesonderter Nutzer-/Ownerfreigabe gestartet.

**Quellen:** ursprüngliche [Backend-Auswertung](20_BACKEND_ASSESSMENT.md) mit datierten Code-/Release-Belegen; [PowSyBl-CGMES-Import](https://github.com/powsybl/powsybl-core/blob/main/docs/grid_exchange_formats/cgmes/import.md), [PowSyBl-CGMES-Export](https://github.com/powsybl/powsybl-core/blob/main/docs/grid_exchange_formats/cgmes/export.md), [PyPowSyBl Python Network API](https://github.com/powsybl/pypowsybl/blob/main/docs/user_guide/network.rst), [ENTSO-E CIM/CGMES](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/).
