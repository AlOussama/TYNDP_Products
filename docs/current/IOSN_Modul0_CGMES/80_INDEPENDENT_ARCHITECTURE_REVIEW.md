# R-M0-CGMES-ARCH-REVIEW-1 — Independent Static Architecture Review

**Projekt:** IoSN / TYNDP / PyPSA — Modul 0 (CGMES ↔ Canonical ↔ PyPSA)  
**Prüfdatum:** 2026-11-01  
**Prüfrolle:** unabhängiger wissenschaftlich-technischer Architektur-Reviewer  
**Verbindliches Repository:** AlOussama/TYNDP_Products  
**M2-Ausgangsbranch:** research/iosn-m0-cgmes-m2-architecture-20261031  
**Unveränderlicher M2-Prüfcommit:** 0275f48231a0794bea324b9cab34700bb0de8f5b  
**M3-Reviewbranch:** review/iosn-m0-cgmes-m3-static-20261101  
**Reviewmodus:** ausschließlich statische Dokumenten-, Quelltext- und Upstream-Dokumentationsprüfung; keine Python-/CGMES-/PyPSA-Ausführung, keine numerischen Tests, keine Änderung an M2- oder Produktivdateien.

## 0. Entscheidung

**Abschlussentscheidung: REPAIRS_REQUIRED.**

- **P0 (unmittelbar fundamentaler Architekturfehler): 0.**
- **P1 (vor einem vorbehaltlosen dokumentarischen Architektur-Freeze zu korrigieren): 7.**
- **P2 (präzise vor bzw. innerhalb des jeweiligen später autorisierten Implementierungsmakros zu schließen): 4.**
- **Formale Traceability:** 48/48 REQ-Einträge inklusive **39/39 MUSS**, 6/6 SOLL und 3/3 OPTIONAL mit Owner und geplantem T-Nachweis; sämtliche **T-01…T-24** vorhanden; **K-01…K-07 und ADR-001…ADR-009** enthalten. Diese Vollständigkeit ist dokumentarisch und kein Test-PASS.

**Begründung:** Die Schichtenarchitektur, die Wahl von PowSyBl als bedingtem Primärbackend, die alternative VeraGrid-Route und die Trennung von Originalgraph, Canonical, elektrischer PyPSA-Projektion und Export sind fachlich tragfähig. Die M2-Entscheidungen beheben die meisten konzeptionellen Widersprüche der beiden Vorberichte. Allerdings bestehen sieben spezifische, noch nicht durch einen eindeutig implementierbaren normativen Vertrag geschlossene Lücken: korrigiertes Identitäts-/Country-Schema, Bus/Branch-Topologie und Origin-Hierarchie, eigener Projektionsverlustnachweis, tatsächliches SSH-only-Routing, zwingende Backend-Parität, dateisystemübergreifende atomare Publikation und maschinenlesbarer DetailedNetworkReference-v1-Vertrag.

**ARCH-STATIC: REPAIRS_REQUIRED.** Ein endgültiges **ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING** wird hier nicht erteilt. Alle Runtime-Gates **QUAL-FORMAT, QUAL-IDENTITY, QUAL-TOPO-GEO, QUAL-ELECTRICAL, QUAL-PYPSA, QUAL-UPDATE-EXPORT, QUAL-CREATE-EXPORT, QUAL-SV-REF, QUAL-OPS-PERF und QUAL-M1-INTEGRATION** bleiben **DESIGNED_NOT_EXECUTED / NOT_ASSESSED**; keine Import-, Elektro-, CGMES-Export- oder IoSN-Realnetzkonformität ist bestätigt. Die P1-Befunde sind in **einer** konsolidierten, vom Owner/S-GOV autorisierten M2-Vertragskorrektur zu behandeln. Dieser unabhängige Reviewer verändert die Ausgangsdokumente nicht.

## 1. Prüfbasis, Provenienz und Evidenzklassen

### 1.1 Verifizierte Repository-Basis

Der Remote-Commit [0275f48231a0794bea324b9cab34700bb0de8f5b](https://github.com/AlOussama/TYNDP_Products/commit/0275f48231a0794bea324b9cab34700bb0de8f5b) wurde über das verbundene GitHub-Repository aufgelöst. Der Vergleich des Commit mit dem angegebenen M2-Branch ergab **identical / ahead_by=0 / behind_by=0**. Damit beziehen sich sämtliche nachstehenden Befunde auf denselben eingefrorenen Dokumentstand.

| Prüfdokument | Geprüfter Git-Blob-SHA | Funktion |
|---|---|---|
| [00 S-GOV](00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md) | 5631f43ca750c688408b8bb6238d080f5f0919c6 | K-01…K-07, M2-/M3-/M4-Autorität |
| [10 Requirements](10_REQUIREMENTS.md) | 71c9da068e2e7c814e6ebe60cc1a4a02a19ef578 | REQ-001…048 und REQ-X01…X08 |
| [20 Backend](20_BACKEND_ASSESSMENT.md) | 6d5ac0af95ae2efbd94bdbd791c3e008b8c4e830 | Upstream-Evidenz und Backendrisiken |
| [30 Canonical](30_CANONICAL_DATA_CONTRACT.md) | 17c23531786759d9841905b9427069637963922e | Tabellen, PK/FK, Einheiten, elektrische Formeln |
| [40 Architecture](40_SOFTWARE_ARCHITECTURE.md) | 408444a1ef17a7caf4031b3f34502fa17f3bc939 | sieben Pakete, Ports, Datenflüsse, Publikation |
| [50 Validation](50_VALIDATION_CONTRACT.md) | de300923e63668b48334ed3321c8c82fad019c63 | Invarianten, T-01…T-24, F-01…F-08 |
| [60 ADR](60_ARCHITECTURE_DECISION.md) | db33ec93ca7b72716b56b43f62cedeef987b2376 | ADR-001…009; verbindliche Korrekturpriorität |
| [70 Readiness](70_IMPLEMENTATION_READINESS.md) | 1d5754adbc3bae6372ecee06f27fca8e8c722177 | Workstreams, Owner, Traceability, Makrogates |

**Ergänzend vollständig gelesen:** [README](../../../README.md) (Blob 8eb4a16b92d63ef9513b7f664d799055d61dc8ec), [Repository-Audit](../../REPOSITORY_AUDIT.md) (1b091e156f0df5d65c15580cc847b43fc09f2e9), [IoSN Band II](../IOSN_2026_Band_II_PyPSA_Implementierung.md) (6412d1e776ae0e8646c429250a439aadae2496b5) und [bestehender M1-PyPSA-Adapter](../../../src/tyndp_reduce/pypsa_adapter.py) (62c54669f5413598f9f5d231c6ebea7e9b4ca914). Ergänzende Einsicht in den vorhandenen DC-Referenzkernel bestätigte die **Single-Island- und Line-only-Beschränkung**. Repository-README und Audit beanspruchen ausdrücklich **keine** qualifizierte reale TYNDP-PyPSA-Integration.

### 1.2 Unabhängiger Upstream-Quercheck

Die relevante PowSyBl-CGMES-Dokumentation wurde zusätzlich am **festen Upstream-Commit f6749ad368fba8dd3776099c040fed07023a1ba3** gelesen:

- [CGMES-Format und Topologien](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/index.md): **Bus/Branch-EQ ohne ConnectivityNodes**, mit notwendiger TP-Zuordnung.
- [CGMES-Import](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/import.md): Original-Terminalidentitäten als IIDM-Aliase; Transformator-/Switch-bedingte Zusammenfassung von VoltageLevels/Substations; State-Updates für SSH/TP/SV, nicht EQ.
- [CGMES-Export](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/export.md): **CGM-Quick-Export erzeugt stets SSH je IGM und ein gemeinsames SV; Profile-Auswahl wird dabei ignoriert**. Der dokumentierte **manuelle CGM-Export** kann einzelne Subnetze mit gezielten Profilen/Metadaten exportieren, ist aber als M0-Workflow und speziell über die Python-Bridge noch zu qualifizieren.

Die unter [20 Backend](20_BACKEND_ASSESSMENT.md) aufgeführten weiteren Versions-, Code-, Release- und Testinventarbelege werden nicht zu Runtime-PASS hochgestuft. Hier erfolgten weder Installationen noch tatsächlich ausgeführte Quellcode-Tests. Evidenzklassen: **D** dokumentiert, **C** statisch im Quellcode, **T** Test vorhanden/nicht ausgeführt, **P** eigene M0-Designvorgabe, **U** nicht nachgewiesen.

### 1.3 Einstufung

**P0:** Entscheidungsgrundlage strukturell unbrauchbar oder Verletzung der grundlegenden Scope-/Sicherheitsinvarianten ohne zulässigen Pfad.  
**P1:** relevante Widersprüche/fehlende Entscheidungen im normativen Integrationsvertrag; **ARCH-STATIC-Freeze-Blocker**, keine Behauptung eines bereits beobachteten Runtime-Fehlers.  
**P2:** begrenzte Spezifikationsschärfung, Negativfall-/Betriebs-/Dokumentationspräzisierung; ohne automatischen Architektur-Neuentwurf lösbar.

Die Kennungen **P0/P1/P2 der Befunde** sind **nicht** identisch mit den in Dokument 70 so bezeichneten **Implementierungspaketen P0…P6**.

## 2. Positivbefunde: begründete Architekturteile

**B-01 — Grundstruktur konsistent.** Der Immutable-Delivery-/Raw-Graph-Ansatz hält Historie, Source-Identitäten, Profile, Header, Boundary und Opaque-Information getrennt von kanonischen Netzobjekten und der elektrischen PyPSA-View; ein PyPSA-Netz wird nicht zur vollständigen CIM-Datenbank erklärt. Diese Trennung erfüllt die fachliche Zielrichtung von REQ-005, REQ-007, REQ-010, REQ-039 und REQ-040.

**B-02 — Bedingte Backend-Wahl sachgerecht.** ADR-001 zieht den dokumentierten PowSyBl-CGMES-Import-/Exportkern über PyPowSyBl heran und verwirft eine eigene allgemeine RDF/XML-Engine. VeraGrid bleibt Alternativkandidat, kein automatischer zweiter Produktionsbackend. Die Unterschiede **externe belegte API versus neu vorgeschlagener FormatBackend-Port** sind in 40 §3 und §3.1 deutlich gekennzeichnet; Originalgraph-Zugriff und vollständige semantische Exportinverse bleiben U, nicht D.

**B-03 — Elektrische Loss-/Capability-Policy grundsätzlich richtig.** Für ACLineSegment und EquivalentBranch, 2W/3W einschließlich sternförmiger 3-Port-Kron-Reduktion, RatioTapChanger/PST, lineare/nichtlineare Shunts, Generator/Load/ExternalInjection, AC/DC-Konverter/HVDC und granulare Current-/OperationalLimits ist eine **zweckgebundene** EXACT/APPROX/UNSUPPORTED-Trennung formuliert (30 §4; 40 §5; ADR-006). Es wird keine pauschale Gleichwertigkeit einer reversiblen verlustbehafteten Link-Abbildung versprochen. Fehlende Ybus-/P/Q-/Basis-Nachweise sollen blockieren, nicht verborgen werden.

**B-04 — Exportmodi trennscharf.** ADR-005 und 40 §§6.3–6.4 verbieten die Gleichsetzung eines originalmodellgebundenen SSH-/SV-Updates mit dem synthetischen CGMES-Neuaufbau aus PyPSA. Kein struktureller EQ-/TP-Round-Trip aus einer reduzierten Netztabelle wird behauptet. Ein gesetztes qualifiziertes Source-Graph-/Semantic-Diff-Gate schützt unbekannte Attribute und Boundary-Referenzen; die konkrete SSH-only-Route bleibt allerdings Befund P1-04.

**B-05 — Modul-1-Grenze richtig gesetzt.** Band II benötigt die unveränderliche detaillierte elektrische Referenz und trennt eigene Zeitreihen, Dispatch, Busmaps sowie Reduktion. Der reale vorhandene M1-Adapter lehnt Transformer, Links/HVDC, Stores/StorageUnits und nicht qualifizierte Phase Shifts ab; der DC-Kern verlangt eine einzelne zusammenhängende AC-Insel. 40/60/70 setzen **REDUCTION_ADAPTER_READY** ausdrücklich **nicht** mit CANONICAL_IMPORT_READY oder PYPSA_LPF_READY gleich. Keine geforderte Änderung des M1-Codes in M3.

**B-06 — Reife- und Gate-Semantik konservativ.** ADR-007 priorisiert eindeutige ARCH-/QUAL-Gate-Namen statt kollidierender G-Nummern, einschließlich eigener Security/Performance-, Export- und M1-Qualifikation. Keiner der 24 geplanten Tests wird als ausgeführt ausgegeben. Fehlen von Referenz-SV führt zu NOT_APPLICABLE_NO_SV statt zu einem Scheinerfolg.

## 3. P1-Befunde — vor statischem Architektur-Freeze zu schließen

### M3-P1-01 — Verbindliche Identitäts-/Occurrence- und Synthetic-Country-Regel noch nicht in einem eindeutigen logischen Tabellenregister konsolidiert

**Quellen:** [30 §2.1, §3.1 Tabellen source_objects/source_occurrences, §3.2 Tabelle buses](30_CANONICAL_DATA_CONTRACT.md); [40 §3.1 Port A/B, §4](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-003/ADR-004](60_ARCHITECTURE_DECISION.md); [70 REQ-006/017](70_IMPLEMENTATION_READINESS.md). **Betroffen:** K-03/K-04; REQ-005/006/007/008/013/017/036; T-04/T-05/T-10/T-21.

**Befund:** Die **inhaltliche Normpräzisierung** in ADR-003 ist eindeutig und zu begrüßen: profilübergreifender Schlüssel (qualified_identity_namespace, identity_kind, identity_value), identity_kind ∈ {MRID, RDF_SUBJECT}, und separate Occurrences. Der weiterhin als bindend bezeichnete Tabellenvertrag 30 schreibt jedoch **source_objects.source_mrid:S verpflichtend** vor, hat keine Felder identity_kind/identity_namespace und definiert einen source_occurrences-PK **ohne source_model_id und rdf_subject**, obwohl die normative Occurrence-Identität nach 60 gerade diese Informationen enthält. Somit ist ein mRID-loses RDF-/SV-Objekt oder eine gleichqualifizierte Mehrfach-Occurrence nicht eindeutig in den Tabellen abbildbar. Ferner erklärt 30 **buses.country_code:S** einschließlich Country-FK verpflichtend, während ADR-004 korrekterweise bei SYNTHETIC_3W_STAR **country_code=NULL** vorsieht; 30 enthält weder bus_role noch source_transformer_id oder die explizite Clustering-Ausschlussinformation. Das spätere Versprechen einer physischen Migration ersetzt noch **keine eindeutige, versionierbare logische Schema-Sollfassung**.

**Korrektur:** Ein einziges, normatives **Canonical-v1-Tabellen-/Constraint-Delta** als M2-Ergänzung beschließen (ohne historische Arbeitsberichte rückwirkend umzuschreiben): nullable source_mrid; identity_kind, qualifizierter Namespace und versionierte Identitätsregel; logisch exakter source_entity_key und source_occurrence_key einschließlich Modelheader/Graph/File/RDF-Subject; eine belastbare Auflösung für Blank Nodes nur innerhalb des Graph-/Revisionskontextes; eindeutige FK-/Unique-Regeln. bus_role={REAL, SYNTHETIC_3W_STAR,...}, source_transformer_id, konditionaler Country-FK, originäre Terminal-Country-Zuordnung und Ausschluss synthetischer Binnenknoten aus nationalen Statistiken. Den Vertrag mit neuen Tabellen/Keys durch **Schema-Major-Version oder klaren Korrekturstand vor erster physischer Einführung** versionieren. Präzisierte negative T-04/T-10-Fälle: mRID-los, gleiche mRID in mehreren Profilen, Authority-Kollision, identischer RDF-Subject in unterschiedlichem zulässigem Kontext, 3W-Stern NULL-Country.

**Abnahmekriterium:** Eine einzige widerspruchsfreie logische PK/FK-Definition kann sämtliche gültigen Quellobjekte einschließlich RDF-only-Identitäten und 3W-Sternbusse ohne erfundene mRIDs oder Länder darstellen.

### M3-P1-02 — Bus/Branch-Topologiepfad und Erhaltung der ursprünglichen Station-/Landes-Hierarchie nicht durchgängig kontrahiert

**Quellen:** [30 §3.2 terminals/topology_membership/topological_nodes, §4.5](30_CANONICAL_DATA_CONTRACT.md); [40 §§3.1/5/6.1](40_SOFTWARE_ARCHITECTURE.md); [50 T-07/T-08/T-10](50_VALIDATION_CONTRACT.md); [60 ADR-002/004](60_ARCHITECTURE_DECISION.md); [PowSyBl Format](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/index.md) und [PowSyBl Import](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/import.md). **Betroffen:** K-01/K-04; REQ-002/003/004/013/015/016/017; T-03/T-07/T-08/T-10.

**Befund:** Der kanonische Topologiekern und die Fixtures sind primär als **ConnectivityNode → Switch-Zusammenfassung → TopologicalNode** formuliert. Das unabhängige PowSyBl-Formatdokument beschreibt jedoch ausdrücklich gültiges **Bus/Branch-CGMES-EQ ohne ConnectivityNodes**, bei dem die Terminal-zu-Bus-Zuordnung zwingend aus **TP** erfolgt. 30 lässt an terminals zwar nullable connectivity_node_id und source_topological_node_id zu, spezifiziert aber keinen vollständigen alternativen Membership-/FK-/Fehlerpfad. Zusätzlich dokumentiert PowSyBl-Import eine **Zusammenfassung von CGMES-Substations/VoltageLevels** in IIDM, wenn die dort strengeren Hierarchiebedingungen es erfordern; als Vertreter wird die alphabetisch erste Station/Ebene gewählt. Daraus darf weder Source-Station noch Origin-Country eines Endports zuverlässig rekonstruierbar angenommen werden. Das betrifft grenzüberschreitende Anlagen, auch wenn physikalische AC-Grenzflüsse im Graphen bleiben.

**Korrektur:** TopologyKind NODE_BREAKER/BUS_BRANCH am Input und pro relevantem Bereich explizit einführen. **Node/Breaker:** Connectivity-/Switch-Faltung, TP-Abgleich. **Bus/Branch:** direkte, originalreferenzierte Terminal→TP-TopologicalNode-Abbildung ohne künstliche ConnectivityNodes; **TP fehlt ⇒ BLOCK**, nicht fiktive EQ/SSH-Ableitung. Canonical-Originalhierarchie über SourceGraph/Relationen rekonstruieren bzw. bei fehlendem Provenienzbeleg blockieren; ein IIDM-Vertreter-Substationwert ist nie automatische Original-Authority-/Country-Zuordnung. In F-02/F-04 und T-03/T-07/T-08/T-10 gezielte Bus/Branch- und Cross-substation-/Country-Gegenfälle aufnehmen.

**Abnahmekriterium:** Beide legalen Topologieformen erhalten eine eindeutige Terminal-/Bus-/Country-Herkunft; ohne unverzichtbares TP oder nicht rekonstruierbare Originalhierarchie bleibt die angefragte Capability BLOCKED.

### M3-P1-03 — Projektionsbezogenes Loss-/Exactness-Ledger besitzt keinen exportunabhängigen Persistenzvertrag

**Quellen:** [30 §3.1 value_provenance, §3.4 export_transactions/loss_manifest](30_CANONICAL_DATA_CONTRACT.md); [40 §3.1 ElectricalView/Port C, §5](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-006](60_ARCHITECTURE_DECISION.md); [50 §3.3](50_VALIDATION_CONTRACT.md). **Betroffen:** K-07, ADR-006; REQ-007/009/035/036/037/042/043; T-12…T-20, T-21/T-22.

**Befund:** ADR-006 schreibt einen **geräte-/feld-/projektionsbezogenen LossLedger** einschließlich Exaktheitsklasse, mathematischem Witness, Gültigkeitsbereich, Policy und Capability vor. Die konkrete Tabelle **loss_manifest** aus 30 ist aber **an export_transactions.transaction_id gebunden**. Eine lediglich importierte oder als PyPSA bereitgestellte ElectricalView hat gerade **keine** Exporttransaktion. value_provenance/assumption_events allein repräsentieren nicht das gleiche Wirkungs-/Approximation-/EXACT-Witness-Urteil. Die Architektur benennt das Ledger, ohne seinen eigenständigen Revisions- und FK-Vertrag festzulegen.

**Korrektur:** Eigenes append-only **projection_quality/loss_ledger** mit PK/FK aus network_revision_id, operating_state_id, projection_id, component/source object, field_or_relation, function_id@version, policy_hash, capability_scope, exactness_class, witness_id bzw. missing_witness, approximation_domain, physical_effect und Status spezifizieren; exportbezogenes loss_manifest bleibt **gesondert** und darf auf Projektionswitnesses verweisen. Regeln für EXACT=kein freigegebener Wert ohne erforderlichen Witness, APPROX=begrenzter Domain-/Effect-Nachweis, UNSUPPORTED=Capability-BLOCK; Reporting auch ohne Export.

**Abnahmekriterium:** Für jede ElectricalView sind originäre Loss-/Quality-Berichte unabhängig von einem Export vorhanden und anhand einer konkreten Netz-/Mappingrevision reproduzierbar.

### M3-P1-04 — Der geplante SSH-only-Updatepfad ist nicht mit dem dokumentierten PowSyBl-CGM-Quick-Export identisch

**Quellen:** [40 §6.3, §7 YAML allow_profiles SSH](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-005](60_ARCHITECTURE_DECISION.md); [70 §6 PoC-M3](70_IMPLEMENTATION_READINESS.md); [PowSyBl Export, CGM quick/manual](https://github.com/powsybl/powsybl-core/blob/f6749ad368fba8dd3776099c040fed07023a1ba3/docs/grid_exchange_formats/cgmes/export.md). **Betroffen:** K-02, ADR-005; REQ-010/040/041/042/043/044; T-21/T-23/T-24.

**Befund:** 40 und 70 lassen **SSH-only ohne neuen gelösten SV** als eigenständig freigebbare Update-Capability zu. Das ist wissenschaftlich sinnvoll, denn neu zu serialisierende SV-Werte verlangen einen geeigneten tatsächlich berechneten Zustand. Aber laut fest gepinnter PowSyBl-Dokumentation schreibt der **CGM-Quick-Export immer** SSH je IGM **plus ein CGM-SV**; die Profile-Auswahl wird dort **ignoriert**. Eine YAML-Policy allow_profiles: [SSH] schränkt den Quick-CGM-Export also **nicht** auf SSH ein. Die Quelle dokumentiert jedoch auch einen **manuellen Subnetwork-/IGM-Export**, der Profile und Metadaten gezielt adressiert. Es handelt sich folglich um eine **fehlende/unklare Backend-Routenwahl**, nicht um den Beweis, dass SSH-only generell unmöglich wäre.

**Korrektur:** Im ExportPlan separate, version-/capability-gebundene Strategien definieren: **CGM_QUICK_SSH_SV** nur bei qualifiziertem neuem SV; **MANUAL_IGM_SSH** (oder später belegte äquivalente Bridge) für SSH-only nach gesonderter Prüfung von Python-Zugriff/Metadata/Header/MAS/Dependencies/Supersedes, vollständiger IGM-Assembly, Semantic Diff und re-importierbarer Lieferung; andernfalls BLOCK_EXPORT_UNPROVEN. Keinen unbelegten SV aus Quick-Output still entfernen oder aus p_set/SSH erzeugen. Negative T-21-Fixture: SSH-Änderung ohne validierten SV-Snapshot muss ausschließlich zulässige SSH-Lieferung erzeugen **oder explizit blockieren**, niemals scheinbar korrekten SV mitliefern.

**Abnahmekriterium:** Jeder freigegebene Exportmodus besitzt eine tatsächlich passende Backend-Operation/Profilmenge und ein geprüftes Header-/Graph-Protokoll; SSH-only ist nicht mehr implizit Quick-CGM.

### M3-P1-05 — REQ-009/T-06-Zweitbackend-Parität ist MUSS, die zweite tatsächliche Backend-Abbildung im PoC aber optional formuliert

**Quellen:** [10 REQ-009](10_REQUIREMENTS.md); [50 T-06 und §4.4](50_VALIDATION_CONTRACT.md); [70 REQ-009, §5 T-06 und §6 PoC-M1](70_IMPLEMENTATION_READINESS.md); [60 ADR-001/007](60_ARCHITECTURE_DECISION.md). **Betroffen:** K-05, ADR-001/007; REQ-009/034/035/043/045; T-06/T-24.

**Befund:** REQ-009 (MUSS) fordert fachliche Canonical-Gleichheit aus **zwei Backend-Abbildungen**; T-06 verlangt zwei backend-spezifische Parse-Adapter/Snapshots. 70 spricht dagegen von einem **optional zweiten Adapter** und plant PoC-M1 mit nur dem PowSyBl-Pfad. Ein zweiter produktiver Runtime-Backend ist zu Recht nicht generell nötig; gleichwohl darf die verbindliche REQ-/T-Prüfpflicht dadurch nicht unbemerkt **PASS** erhalten.

**Korrektur:** Die **Qualifikationsstrategie** normativ auflösen: entweder T-06 mit zwei tatsächlich unabhängig erzeugten und verifizierten BackendSnapshots erfüllen, bevor die dadurch betroffene Backendneutralitäts-/Canonical-Paritäts-Capability PASS bekommt; oder durch ausdrückliche Owner-Governance und versionierte REQ-Änderung eine primäre Single-Backend-Importfähigkeit von einer **separaten verpflichtenden Paritäts-/Backendwechsel-Capability** trennen. Zwei künstlich identische Mock-Snapshots oder ein einziges Backend mit zwei Views sind **kein** Beleg unabhängiger Parserparität. Bis dahin REQ-009=NOT_ASSESSED; keine pauschale Erfüllungsbehauptung.

**Abnahmekriterium:** Ein dokumentierter eindeutiger Status und Pflichttermin für REQ-009/T-06 ohne normativen Widerspruch zur optionalen VeraGrid-Produktivimplementierung.

### M3-P1-06 — Atomarität zwischen SQLite, unveränderlichem Dateiarchiv und Exportpaket ist als Commit-/Recovery-Protokoll unterbestimmt

**Quellen:** [40 §3.1 Ports B/E, §6.5, §8](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-009](60_ARCHITECTURE_DECISION.md); [30 §2.2, §3.4 export_transactions](30_CANONICAL_DATA_CONTRACT.md); [50 T-05/T-21/T-22/T-24](50_VALIDATION_CONTRACT.md). **Betroffen:** ADR-009; REQ-008/010/039/040/044; T-05/T-21/T-22/T-24.

**Befund:** Staging → QA → atomarer Manifest-/Revisionspointer, SQLite-FKs und optimistic base hash sind richtige Elemente. Eine gewöhnliche **SQLite-Transaktion garantiert aber nicht die Atomarität gleichzeitiger Dateisystem-/ZIP-/JSON-Publikation**. Nicht normativ geklärt sind der einzige autoritative Commitpunkt, bereits durabel gespeicherte Blob-Inhalte vor Sichtbarkeit, CAS/Locking für konkurrierende Writer, Crash-/Restart-Recovery, Behandlung orphaned staging files und idempotente Wiederholung. Das sind konkrete Vertragsrisiken für die explizite Anforderung atomarer Exportlieferungen, keine gemessenen Fehler.

**Korrektur:** Ein eindeutiges **Publish-Protokoll** für PoC-v1 spezifizieren: immutable Blobs und Manifest vollständig schreiben, SHA-256 verifizieren und vor Veröffentlichung dauerhaft abschließen; **ein** autoritativer, transaktionaler Revisions-/Delivery-Pointer (bevorzugt SQLite mit CAS/base-hash) wird **zuletzt** sichtbar gemacht; nur dieser Pointer definiert COMMITTED. Staging-Artefakte sind extern nie als gültige Lieferung zu behandeln. Nach Crash: committed-only Wiederherstellung, GC für unreferenzierte Blobs, Retry via idempotency key, CAS-Konflikt führt BLOCK und Audit. Dateisystemgrenzen und atomare Umbenennungen ausdrücklich definieren; keine magische Cross-DB-/FS-Transaktion behaupten. T-05/T-21/T-22/T-24 um definierte Failure-Injection-/Concurrency-Szenarien als spätere Testspezifikation ergänzen.

**Abnahmekriterium:** Für jeden Absturzpunkt und konkurrierenden Export ist eindeutig festgelegt, welche Revision/Dateimenge sichtbar ist und wie eine Wiederholung ohne Teil-Commit funktioniert.

### M3-P1-07 — DetailedNetworkReference v1 ist semantisch beschrieben, aber nicht als vollständiger typisierter Übergabe-/Versionierungsvertrag eingefroren

**Quellen:** [30 §7](30_CANONICAL_DATA_CONTRACT.md); [40 §3.1 Port D und §9](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-008](60_ARCHITECTURE_DECISION.md); [70 P6 und Capability-Matrix](70_IMPLEMENTATION_READINESS.md); [Band II §2.2](../IOSN_2026_Band_II_PyPSA_Implementierung.md); [M1-Adapter](../../../src/tyndp_reduce/pypsa_adapter.py). **Betroffen:** K-06, ADR-008; REQ-017/027/029/037/038/039; T-09/T-14/T-17/T-19/T-20.

**Befund:** Die Grenze M0→M1 und das **getrennte REDUCTION_ADAPTER_READY-Gate** sind eindeutig. Dagegen fehlen für das als Version **v1** bezeichnete Übergabeartefakt eine verbindliche Feld-/Typ-/Null-/FK-/Unit- und Kompatibilitätstabelle sowie ein expliziter Status-/Versionierungs-Handshake: insbesondere Netz-/State-/Projektionsreferenz, Original- versus Sternbusrolle, Kanten-/Portrichtung, System- und Transformer-PU-Basen, x_pu_eff, PST-Offset/Orientierung, HVDC-Terminal-Injektionen und Verlustklasse, mehrdimensionale Limits, State-/Active-Semantik und Sidecar-Referenz. In 30/40 sind diese nur verteilt in Fließtext und beispielhaften Signaturen genannt. Ein implementierender M1-Adapter müsste damit wichtige API-/Einheitenentscheidungen selbst erfinden.

**Korrektur:** Normatives **DetailedNetworkReferenceV1-Schema** mit Feldtypen, erlaubten NULLs, FK-/Orientierungs- und Snapshot-Invarianten sowie verpflichtenden unit/base/source-map/quality/capability-Feldern und einer festen SemVer-/Fingerprint-Regel einfügen. Unveränderlichen Input von späteren Zeitreihen/Dispatch/Reduktions-Busmaps explizit trennen. M0 darf das Artefakt ausgeben, aber **nur ein separater M1-End-to-End-Test** kann REDUCTION_ADAPTER_READY erteilen. T-20 enthält erfolgreichen Line-only- sowie negative 2W/3W/PST/HVDC/mehrinselige Handshake-Fälle; keine stillen Drops.

**Abnahmekriterium:** Ein fremder Modul-1-Entwickler kann die detaillierte Netzrevision einschließlich Sonderkomponenten **ohne implizite Feld-/Einheitenannahmen** konsumieren oder mit nachvollziehbarem Unsupported-Status ablehnen.

## 4. P2-Befunde — konkretisieren, ohne die Grundarchitektur erneut zu öffnen

### M3-P2-01 — Topologieändernde State-Writes und strukturelle EQ-/TP-Mutationen ausdrücklich disjunkt klassifizieren

**Quellen:** [50 §3.1](50_VALIDATION_CONTRACT.md); [40 §6.3](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-005](60_ARCHITECTURE_DECISION.md). **Problem:** Beispielhafte SSH-Status-/Tap-Writefelder könnten als generelle Erlaubnis zur Änderung von Switch.open, Terminal.connected oder Equipment.inService verstanden werden, obwohl ADR-005 strukturelle Originalschalter-/Terminal-/EQ-/TP-Änderungen zunächst sperrt und topologieändernde Zustände TP-Neuqualifikation benötigen. **Vorgabe:** Mutationsklassen STATE_NON_TOPOLOGY, STATE_TOPOLOGY_AFFECTING, STRUCTURAL_EQ_TP und SYNTHETIC_CREATE samt backend-/profile-spezifischer Allowlist definieren. Für v1 STATE_TOPOLOGY_AFFECTING nur nach eigener TP-/Reference-/Graph-Gate-Zulassung, ansonsten BLOCK. Negative T-21-Erwartung ergänzen.

### M3-P2-02 — Source-, Betriebszustands-, Canonical- und View-Revisionsidentitäten eindeutig entflechten

**Quellen:** [30 §2.2/3.1](30_CANONICAL_DATA_CONTRACT.md); [40 §3.1 RevisionRef und §4](40_SOFTWARE_ARCHITECTURE.md). **Problem:** network_revision_id wird teils als unveränderliche Quellnetzrevision, teils als Hash aus Source-Set **plus Operating State plus Mapping-Policy** beschrieben. Bei unverändertem Originalgraph, aber geänderter Projektionspolicy würde so die Original-Referenz-Identität wechseln. **Vorgabe:** source_model_set_id/source_revision_id, operating_state_id, canonical_revision_id und electrical_view/projection_id mit klarer Hash-/Parent-Policy sowie unveränderlichen referenzierten Originaldaten getrennt definieren; asset_id stabil und view_id policygebunden. Für v1 nicht zwingend vier physische Tabellen, aber eindeutige logische Semantik.

### M3-P2-03 — Testfixtures gezielt um die erst hier belegten Negativfälle erweitern

**Quellen:** [50 §4/T-01…T-24](50_VALIDATION_CONTRACT.md); [70 §5](70_IMPLEMENTATION_READINESS.md); Upstream-Import-/Exporttexte in §1.2. **Problem:** F-02 ist überwiegend Node/Breaker, T-06 benötigt echte Zweitbackend-Evidenz; bisher fehlt eine explizit benannte SSH-only-CGM-Negativfixture. **Vorgabe:** für T-03/07/08 Bus/Branch mit/ohne TP, für T-04 RDF-only/BlankNode-Multi-Occurrence, für T-10 aus IIDM zusammengefasste Source-Substations mit abweichenden Länderendpunkten, für T-21 QUICK_CGM mit ungeeignetem SV und manueller SSH-Routenprüfung ergänzen. Testumfang bleibt **T-01…T-24**; keine Ausführung oder synthetischen Testresultate in M3.

### M3-P2-04 — Laufzeit-, Sicherheits-, Lizenz- und Performanzfreigaben als operative Policies abschließen

**Quellen:** [20 §9/10](20_BACKEND_ASSESSMENT.md); [40 §8](40_SOFTWARE_ARCHITECTURE.md); [60 ADR-009](60_ARCHITECTURE_DECISION.md); [70 §8](70_IMPLEMENTATION_READINESS.md). **Problem:** Größe/Zip-Bomb/XML-Entity-Grenzen, Java-/RDF-Speicherlebenszyklus, Lizenzierung echter IGMs und 6k+-Bus-Benchmarks sind korrekt als spätere Gates benannt, besitzen aber noch keine gepinnten Limits/Budgets/Thresholds. **Vorgabe:** vor der jeweiligen PoC-Freigabe Inputbudget, Speicher-/CPU-/Timeoutpolicy, Prozessisolierung, JVM/Backend-Session-Schließung, Abbruch-/Recovery-Gates, Nutzungs-/Redistributionsberechtigung und messbare Performanceziele versionieren. Kein externer Testdatensatz ohne belegte Berechtigung; keine Performance-/Sicherheits-/CGMES-Konformitätsaussage aus einem 2-Bus-Test.

## 5. K-01…K-07 und ADR-001…ADR-009 — vollständiger Crosscheck

### 5.1 Auflösung der sieben K-Konflikte

| K | Entscheidung im M2 | Statisches Review |
|---|---|---|
| K-01 Profile/Boundary | 2.4.15 und 3.0 versions-/exchange-/capabilityabhängig; kein fiktives 3.0-TPBD; GL optional | **Grundsatz korrekt.** Für Bus/Branch muss TP ausdrücklich zwingend sein; P1-02 |
| K-02 Update-Export | Originalmodell/RawGraph, beschränkter Delta, keine 1:1-Behauptung; CREATE separat | **Grundsatz korrekt.** SSH-only muss von Quick-CGM getrennt geroutet werden; P1-04 |
| K-03 Source-ID/Occurrence | MRID oder RDF_SUBJECT profilübergreifend; Source/Occurrence/View verschieden | **Vorrang eindeutig**, aber korrigiertes tabellarisches Sollschema fehlt; P1-01 |
| K-04 Länder/Sternbus | reales Country bei M1-Freigabe; 3W-Star NULL und nicht geographisch | **Fachlich korrekt**, Tabellen-FK/Role noch inkonsistent; P1-01/02 |
| K-05 Gates | ARCH-STATIC und benannte QUAL-* statt zweier G-Nummernbereiche | **Korrekt**, REQ-009/T-06-Nachweispflicht gegen optionalen Adapter klären; P1-05 |
| K-06 M0/M1 | DetailedNetworkReference v1, M1-Adapter separat zu qualifizieren | **Grenze korrekt**, Typ-/Snapshotvertrag ergänzen; P1-07 |
| K-07 elektrische Sondergeräte | objekt-/wirkungsbezogen EXACT/APPROX/UNSUPPORTED, Ybus/Power/Limits-Witness | **Fachlich korrekt**, persistentes exportunabhängiges LossLedger ergänzen; P1-03 |

### 5.2 Neun Architekturentscheidungen

| ADR | Statische Disposition | Verbleibendes, präzise begrenztes Risiko |
|---|---|---|
| ADR-001 Externes Backend | **ACCEPTED_DESIGN** | API-/Graph-Fidelity per Runtime noch UNKNOWN; keine Eigenengine |
| ADR-002 Profilpolicy | **ACCEPTED_WITH_P1-02** | Bus/Branch-TP-Pflicht explizit |
| ADR-003 Identität | **ACCEPTED_PRINCIPLE_WITH_P1-01** | Implementierbares normatives Tabellenschema |
| ADR-004 Länder | **ACCEPTED_PRINCIPLE_WITH_P1-01/02** | synthetische FK und originaler Stations-/Endport-Ursprung |
| ADR-005 Export | **ACCEPTED_PRINCIPLE_WITH_P1-04** | Quick-CGM/Manual-IGM und SSH/SV-Trennung |
| ADR-006 elektrische Projektion | **ACCEPTED_PRINCIPLE_WITH_P1-03** | eigenes Projection-Loss-Witness-Register |
| ADR-007 Gates | **ACCEPTED_WITH_P1-05** | REQ-009/T-06-Nachweis nicht optional |
| ADR-008 M1-Grenze | **ACCEPTED_WITH_P1-07** | typisierter DetailedNetworkReference-v1-Handshake |
| ADR-009 Persistenz/Sicherheit | **ACCEPTED_WITH_P1-06** | revisionssicheres DB-/Datei-Commit-/Recovery-Protokoll |

**Keine alternative Backendgesamtarchitektur empfohlen.** Die Befunde verlangen einen begrenzten dokumentarischen Vertragsabgleich und später gezielte Witnesses, nicht die Rückkehr zu einem selbst implementierten universellen CGMES-Parser.

## 6. Verantwortlichkeiten der sieben M0-Pakete und Implementierungsworkstreams

### 6.1 Tatsächliche M0-Codepakete in 40

| Fachpaket | Abgegrenzte Eigentümerschaft und Ports | Reviewstatus / Zuordnung |
|---|---|---|
| **backend** | FormatBackend, PowSyBlBackend, später VeraGridBackend; BackendSession/BackendSnapshot/IdentityEvidence, Backend-Exportbridge | **Definiert**; P1-02/04/05 sind API-/Routenpräzisierungen, nicht Upstream-Zusagen |
| **archive_provenance** | DeliveryArchive, source facts/identity index, immutable blobs, ChangeTracker | **Definiert**; P1-01/06, P2-02 |
| **canonical** | Revisions-/SQLite-/PK/FK-Schema, typed SourceFacts, identity/relationship checks | **Definiert**; P1-01/02/06 |
| **projection** | TopologyAdapter, MappingEngine, prüfbare elektrische Funktionen, ElectricalView | **Definiert**; P1-02/03, P2-03 |
| **pypsa_port** | detailliertes PyPSA Network und Sidecar, DetailedNetworkReferenceV1, inverse Edit-Grenze | **Definiert**; P1-03/07, keine M1-Codefreigabe |
| **export** | Update-/Create-Pläne, staged serializer, Graph-Diff, atomare Publikation | **Definiert**; P1-04/06, P2-01 |
| **validation** | REQ-/Capability-Gates, Prüfberichte, QA-/Loss-Witnesses, Tests/Negative-Fixtures | **Definiert**; P1-03/05/06, P2-03/04 |

**Review der Portgrenzen:** Die sieben Pakete besitzen fachlich nachvollziehbare Eingänge, Ausgänge, Fehlersemantik, Version-/Policybezug und Zuständigkeit. Die benannten Ports unter 40 §3.1 sind **eigene Architekturentwürfe**, keine als bestätigt ausgegebenen PyPowSyBl-/VeraGrid-Methoden. Ein BackendSession-Handle darf nie als dauerhaftes Originalarchiv oder globale mutable Quelle fungieren. Alle potenziell fehlenden Quell-IDs/Originalrelationen müssen UNKNOWN/BLOCK bleiben.

**Abgrenzung zu 70:** Dort sind **sieben Umsetzungsworkstreams P0–P6** aufgeführt; sie sind nicht identisch mit den sieben M0-Codepaketen. P0 BACKEND-IN, P1 CANONICAL, P2 ELECTRICAL, P3 EXPORT-UPDATE, P4 EXPORT-CREATE und P5 QA-OPS verteilen Arbeiten **innerhalb M0**. **P6 M1-ADAPTER** liegt explizit **außerhalb M0** und bedarf eigener Owner-Freigabe. Diese Differenzierung ist konsistent und darf bei weiterer Planung nicht verloren gehen.

### 6.2 Owner-/REQ-/T-Traceability

Ein statischer Zeilenabgleich der Dateien 10 und 70 ergab:

| Gegenstand | Soll | Ist | Urteil |
|---|---:|---:|---|
| REQ-001…REQ-048 | 48 | 48 | vollständig, keine doppelte/fehlende ID |
| Klasse MUSS | 39 | 39 | alle mit Owner und Test-ID |
| Klasse SOLL | 6 | 6 | alle erhalten |
| Klasse OPTIONAL | 3 | 3 | alle erhalten |
| REQ-X01…X08 Scope-Ausschlüsse | 8 | 8 | weiterhin ausgeschlossen |
| K-01…K-07 | 7 | 7 | vollständig adressiert |
| ADR-001…009 | 9 | 9 | vollständig enthalten |
| T-01…T-24 | 24 | 24 | jeder Test einmal als Testfall in 50 spezifiziert |
| F-01…F-08 | 8 | 8 | Fixture-Plan, keine ausgeführten Fixtures |

**Unterscheidung:** Eintrag vorhanden ≠ durch tatsächlichen Code erfüllt. Die REQ-Zeilen mit **M3-P1-Abnahmeabhängigkeit** sind insbesondere **REQ-005/006/008/009/010/013/017/036/037/038/040/042/043/044/045**. Sie bleiben in der Traceability erhalten und dürfen bei der späteren Implementierung weder still gestrichen noch durch pauschal grüne Tests ersetzt werden.

Alle Testfälle wurden ihrem Fachziel statisch zugeordnet; keiner wurde ausgeführt:

| Test-ID | Geplanter Nachweis | Statischer Status |
|---|---|---|
| T-01 | 2.4.15/3.0 Profil-/Header-/URI-Versionen | DESIGNED_NOT_EXECUTED |
| T-02 | unsolved/solved SSH/SV-States | DESIGNED_NOT_EXECUTED |
| T-03 | Single-/Multi-IGM/CGM, Boundary | DESIGNED_NOT_EXECUTED; Bus/Branch ergänzen |
| T-04 | mRID/RDF/Occurrence/Unknowns | DESIGNED_NOT_EXECUTED; P1-01 |
| T-05 | deterministischer Reimport/CAS | DESIGNED_NOT_EXECUTED; P1-06 |
| T-06 | unabhängige Backend-Normalisierungsparität/YAML | DESIGNED_NOT_EXECUTED; P1-05 |
| T-07 | Switch/Connectivity/Terminal-Topologie | DESIGNED_NOT_EXECUTED; Bus/Branch ergänzen |
| T-08 | TP-gegen-EQ/SSH-Abgleich | DESIGNED_NOT_EXECUTED; P1-02 |
| T-09 | AC-Inseln/HVDC/Slack | DESIGNED_NOT_EXECUTED |
| T-10 | Country/Endport/Synthetic-Bus | DESIGNED_NOT_EXECUTED; P1-01/02 |
| T-11 | GL/CRS/Missing/Geometrie | DESIGNED_NOT_EXECUTED |
| T-12 | Line/EquivalentBranch/PI/Ybus | DESIGNED_NOT_EXECUTED |
| T-13 | 2W/3W-Basen und Kron-Y | DESIGNED_NOT_EXECUTED |
| T-14 | RatioTap/PST/Remote Control | DESIGNED_NOT_EXECUTED |
| T-15 | Generator/Load/PQ/PV/Slack | DESIGNED_NOT_EXECUTED |
| T-16 | Shunts/Abschnitte/ZIP | DESIGNED_NOT_EXECUTED |
| T-17 | AC/DC-Ports/Reverse-Loss/MTDC | DESIGNED_NOT_EXECUTED |
| T-18 | Units/Zero/NaN/Singularität/Origin | DESIGNED_NOT_EXECUTED |
| T-19 | Limits terminal-/zeit-/richtungsgebunden | DESIGNED_NOT_EXECUTED |
| T-20 | PyPSA-Projektion plus M1-Negativfälle | DESIGNED_NOT_EXECUTED; P1-07 |
| T-21 | UPDATE-Round-trip/Diff/Unknowns | DESIGNED_NOT_EXECUTED; P1-04/06 |
| T-22 | synthetisches CREATE/Reimport | DESIGNED_NOT_EXECUTED; P1-06 |
| T-23 | qualifizierter SV-/AC-PF-Vergleich | DESIGNED_NOT_EXECUTED; bei fehlendem SV N/A |
| T-24 | QA/BOM/Report/Regression/OPS | DESIGNED_NOT_EXECUTED |

Damit ist die **Zähl- und Plan-Traceability formal vollständig**. Eine numerische Toleranz aus 50 ist noch kein bestandenes mathematisches Äquivalenzkriterium; echte CGMES-Versionen/Datasetlizenzen, PyPSA-/Java-Versionen, Fixturehashes, Ergebnisbelege und negative Testfälle sind Pflicht bei späterem QUAL-PASS.

## 7. Weitere Pflichtprüffelder und differenzierte Freigaben

### 7.1 Daten-, RDF-, Authority- und Boundary-Verträge

**Positiv:** Raw-Delivery einschließlich ZIP-Mitgliedern, Dateihash, FullModel-IDs, Profile URI, Authority/MAS, DependsOn/Supersedes, Opaque-Tripeln, originalen Source-Terminals und Boundarybeziehungen wird als unveränderliche Autorität verlangt. Reimport darf keine impliziten Deletes, Profile keine Last-file-wins-Priorität und synthetische View-IDs keine historischen mRIDs erzeugen. Import und Revisionspublikation sind getrennte Vorgänge.

**Einschränkungen:** Die tatsächliche Exponierung der Original-RDF-Subjects, Class-/Alias-/Terminal- und Boundary-Details über PyPowSyBl ist **nicht belegt**. Auch die dokumentierten IIDM-Substation-Zusammenfassungen belegen, dass eine reine DataFrame-Rückabbildung Originalhierarchie verlieren kann. **REQ-006/007/010/017/040** verlangen deshalb den originalgraphgestützten Witness/Backmapping-Pfad; fehlender Zugriff ist **BLOCK_EXPORT_UNPROVEN** beziehungsweise Country-/Canonical-Blocker für die relevante Fähigkeit. EQBD/TPBD/GL dürfen nicht durch synthetische Re-Serialisierung ersetzt werden; insbesondere kein 3.0-TPBD als globale Voraussetzung.

### 7.2 Elektrische Semantik

| Objekt | Erforderlicher Invariant, keine implizite Freigabe |
|---|---|
| ACLineSegment/EquivalentBranch | physikalisch differenzierte Sourceklasse, echte Endorientierung, Ohm/Siemens, vollständiges PI-Zweitor-Y, Shunts korrekt aufgeteilt |
| 2W-Trafo | ratedU/ratedS je Wicklung; T-/PI-Modell und Tap-Seite; ±φ/ratio in zweitoriger komplexer Y-Matrix; kein stiller TransformerType-Override |
| 3W-Trafo | ursprüngliche drei Endports im Canonical, drei synthetische Sternäste nur als abgeleitete View; 3-Port-Kron-Y samt aktiven Taps/Shunts |
| PST/RatioTap | Schritt/Neutral/EndNumber/Controller/Remote-Status behalten; affine DC-Offset-Richtung und AC-Phase qualifizieren |
| Shunt | Vorzeichen der G/B-Wirkung; fixe Admittanz gegebenenfalls EXACT, nichtlineare Sections/Steuerung eingeschränkt |
| Generator/Load/External | korrekt konvertierte Load-Sign-P/Q-Bilanz, PQ/PV/Slack und Grenzen nicht erraten |
| HVDC | separate AC-/DC-Port-/Converterbeziehungen; Verluste; keine falsche Rückwärts-Effizienz im einzelnen lossy reversiblen PyPSA-Link; MTDC explizit außerhalb Simple-Link-Capability |
| Grenzwerte | Original-LimitSet/Terminal/Direction/Duration/Season/Contingency unverändert; CurrentLimit→MVA nur mit deklarierter Spannung; s_nom höchstens gekennzeichneter Proxy |

Die Definitionen und initialen vorgeschlagenen NUM-01…NUM-09-Grenzen sind **statisch fachlich nachvollziehbar**; ein mathematisches PASS oder ein konkreter Ybus-Fidelity-Nachweis ist daraus nicht abzuleiten.

### 7.3 Export- und Revisionsmatrix

| Operation | Vertrag | M3-Beurteilung |
|---|---|---|
| CANONICAL/Import | Originalgraph, referenzielles Canonical, Version-/Header-/Boundary-Policy | entworfener Weg, keine Importqualifikation; P1-01/02 |
| PYPSA_ACPF/LPF | versionierte elektrische Projektion mit Verlust-/Witness- und Grenzenbericht | entworfener Weg, keine elektrische Qualifikation; P1-03/07 |
| UPDATE_IMPORTED | originale unveränderte EQ/TP/Boundary weiterreferenzieren, freigegebene SSH-/ggf. SV-Delta-Profile, Modellheader/Graphdiff, atomische Lieferung | strikt getrennt von CREATE; SSH-only-Routing und Commit-Protokoll P1-04/06 |
| CREATE_FROM_PYPSA | neue synthetische Equipment-/Terminal-/Authority-/Profil-Identitäten, eigene Konformitätsprüfung | strikter eigener Vertrag; noch nicht implementiert/qualifiziert; P1-06 |
| REDUCTION_ADAPTER_READY | tatsächliche Unterstützung durch bestehenden M1-Adapter und eigene E2E-Snapshot-/Zeitreihenqualifikation | **explizit NICHT gegeben**, korrekter isolierter Folgescope; P1-07 nur M0-Übergabevertrag |

**Insbesondere:** Ein erfolgreiches Import-/Projektions-QUAL würde keinen Export-PASS, einen originalgraphisch unveränderten Reimport und keine M1-Reduktion bestätigen. Eine reine SSH-Änderung rechtfertigt kein neu behauptetes gelöstes SV. Das Import-/Export-Graph-Diff ist semantisch, nicht XML-byteidentisch; unqualifizierte Änderungen an Source-Equipment oder Boundary bleiben verboten.

## 8. Konsolidierte Korrektur- und Governance-Freigabekriterien

**Ein einziger begrenzter M2-Nachtrag** statt neuer paralleler Architektur- oder Testschleifen. Änderungen nur durch hierzu autorisierten S-GOV-/M2-Producer, nicht durch diesen unabhängigen M3-Review.

| Priorität | Korrekturlieferung | Zugeordnet |
|---|---|---|
| P1 | normatives korrigiertes Identity/Occurrence/Country-Schema mit Major-/Versionsregel | M3-P1-01 |
| P1 | beide TopologyKinds und Source-Substation-/Country-Provenienzroute einschließlich Negativfall | M3-P1-02 |
| P1 | unabhängiges, revisionsgebundenes Projection-LossLedger-Schema | M3-P1-03 |
| P1 | backendpassende QUICK_CGM vs MANUAL_IGM SSH-only/SV-Exportstrategie | M3-P1-04 |
| P1 | REQ-009/T-06-Bindung auf verpflichtende Paritäts-Qualifikation bzw. genehmigte Scope-Revision | M3-P1-05 |
| P1 | autoritativer Commitpunkt, CAS-/Crash-/Recovery-/Idempotenz-Vertrag für DB/FS | M3-P1-06 |
| P1 | typisierter unveränderlicher DetailedNetworkReferenceV1 und M0/M1 Capability-Handshake | M3-P1-07 |
| P2 | Änderungs-Klassifikation, Revision-IDs und zusätzliche Negativfixtures | M3-P2-01/02/03 |
| P2 | versionierte Security/Runtime/License/Performance-PoC-Policies | M3-P2-04 |

**Kriterien für eine spätere dokumentarische ARCH-STATIC-Freigabe:** (i) alle sieben P1 geschlossen und eindeutig auf den korrigierten normativen Vertrag bezogen; (ii) keine aufgehobene REQ- oder T-Traceability; (iii) weiterhin keine behauptete Runtime-/Konformitäts-Evidenz; (iv) alle P2 mit expliziter verantwortlicher späterer Freigabestufe und BLOCK-Fallback versehen; (v) ein nachvollziehbarer S-GOV-Abschlussentscheid über den Architektur-Freeze. Eine erneute breit angelegte Backend-Literaturrecherche ist für diese Korrektur nicht erforderlich.

**Spätere PoC-/M4-Implementierung:** Erst nach gesonderter ausdrücklicher Ownerfreigabe. PowSyBl/PyPowSyBl- und PyPSA-Pins, reale Profile/Fixturedaten, Versions-/Java-ABI, Testlizenzen, Rohgraph-/ID-/Boundary-Belege sowie T-01…T-24 werden dann tatsächlich überprüft. Auch nach einem statischen PASS sind **CANONICAL_IMPORT_READY, PYPSA_ACPF_READY, PYPSA_LPF_READY, UPDATE_EXPORT_READY, CREATE_EXPORT_READY und REDUCTION_ADAPTER_READY** weiterhin getrennte qualifikationspflichtige Aussagen.

## 9. Review-Abschluss

**Disposition:** **R-M0-CGMES-ARCH-REVIEW-1 = REPAIRS_REQUIRED**.  
**P0:** 0. **P1:** 7. **P2:** 4.  
**Stärken:** bedingte externe Format-Backendwahl, korrekte Originalgraph-/PyPSA-Trennung, beide Exportmodi, solide elektrische Invarianten, 39/39 MUSS plus 24/24 T in Plan-Traceability, explizite M1-Grenze.  
**Keine Freigabe:** weder CGMES-2.4.15-/3.0-Konformität noch verlustfreier Round-Trip, Ybus-/PF-/Exportnachweis, Performance, Sicherheitstest, reale TYNDP-Netzintegration oder ENTSO-E-/IEC-Zertifizierung.

**Repository-Operation dieses M3-Makros:** ausschließlich dieses neue, unabhängige Reviewdokument auf dem separaten Review-Branch. **Keine** Änderung von 00/10/20/30/40/50/60/70, **keine** Änderung unter src/ oder tests/, **kein Merge** nach main.
