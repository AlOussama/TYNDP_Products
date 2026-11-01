# S-GOV — M4-0: nächste ausführbare Makroaufträge und unabhängige Handoffs

**Datum:** 2026-11-01  
**Projekt/Repository:** IoSN / TYNDP / PyPSA — `AlOussama/TYNDP_Products`  
**Verbindliche Architektur:** S-GOV-Freeze-Commit `b1e284996fa69f81651daf9150b829e6a42e4ce3`.  
**M4-0-Referenzen:** [98 maschinenlesbarer Preflight](98_M4_0_PREPARED_EXECUTION_CONTRACT.json), [95 Upstream/Daten](95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md), [96 RunRelease-Gates](96_M4_0_RUNRELEASE_POLICY_AND_GATES.md), [85 CAN/2.0.0 + DNR/1.0.0](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md), [70 Testplanung](70_IMPLEMENTATION_READINESS.md), [50 Tests](50_VALIDATION_CONTRACT.md).  
**M4-0-Governance:** `M4_0_STATIC_PREFLIGHT_COMPLETE_WITH_NAMED_RUNRELEASE_HOLDS` — die **Vorbereitung** dieser Worker-Handoffs autorisiert **nicht automatisch** Implementierung/Testausführung. Der Nutzer/Owner startet jeden gewählten Worker durch gesonderten ausdrücklichen Ausführungsauftrag. Alle weiteren Arbeiten sind auf getrennten Branches, ohne Merge nach main.

## 1. Makrofolge und Parallelstrategie

| Makro | Verbindlicher Scope | Termin / Abhängigkeit | Ergebnisstatus |
|---|---|---|---|
| `R-M0-POC1-IMPL-1` | Primärer PowSyBl→CAN/2.0.0→PyPSA-Kernpfad, sichere Source-Raw-Archive, Typ-/Identity/Revision/Topologie/Quality, M0-PUBLISH, Testharness | Start nach ausdrücklicher PoC-Freigabe, G0-Prüfung als erster Arbeitsteil | zunächst `CANONICAL_IMPORT_PROVISIONAL` möglich; READY nur mit tatsächlich unabhängiger T-06 |
| `R-M0-T06-INDEPENDENT-1` | **Unabhängiger** read-only CGMES-Zweitbackend-Snapshot und differenzierter T-06-Witness zu REQ-009; VeraGridEngine nach G0-Check | Parallel zu PoC1, gleiche immutable Quellfixtures/Definitionen, eigener Branch | `T06_WITNESS_VALID_FOR_NAMED_SCOPE` oder `BLOCKED/INCONCLUSIVE` |
| `S-GOV-M0-POC1-INTEGRATE` | Einmalige konsolidierte Prüfung von Implementation-/T06-Rückläufern, basierte Diff-/Fixture-/BOM-/QA-Berichte und getrennte Capability-Entscheidungen | nach Vorliegen beider Rückläufer, kein zusätzlicher Microreview | bezogener SCOPED PASS oder BLOCK/CONDITIONAL |
| `R-M0-POC2-ELECTRICAL-1` | 3W/PST/HVDC/Shunt/Limits/Multi-IGM mit elektrischen Witnesses | nach stabiler PoC1 Source/Canonical/Projection API; parallel zu POC3 | unabhängige Geräte-/ACPF-/LPF-Capabilities |
| `R-M0-POC3-UPDATE-EXPORT-1` | originalgraphgestützter MANUAL_IGM_SSH/CGM_QUICK_SSH_SV-Export, Inversen, Dependency-Graph-Diff, CAS/Reimport | nach stabiler PoC1 Raw-/Identity-/Publish-Basis, parallel zu POC2 | getrennte SSH-only-/SSH+SV-Exportgates |
| `R-M0-POC4-CREATE-OPS-1` | synthetische CREATE_FROM_PYPSA-Profile und große lizensierte CGM-Skalierung | nur bei eigener späterer Owner-Freigabe | CREATE und PERFORMANCE separat |
| `R-M1-DNR-ADAPTER-1` | bestehender `tyndp_reduce.pypsa_adapter` auf DNR v1 qualifizieren/erweitern | anderer Modul-/Owner-Scope, nach PoC1/PoC2 Eingangsvertrag | REDUCTION_ADAPTER_READY nur nach eigenem E2E, nicht M0-Automatik |

Keine automatische Parallel-Worker-Startpflicht. **Zwei** unmittelbar sinnvoll vorbereitete unabhängige Fachchats (POC1 und T06) reichen aus. POC2 und POC3 werden erst nach dem konsolidierten PoC1-Interface-Witness gestartet; nicht gleichzeitig auf einem ungetesteten Datenvertrag arbeiten.

---

## 2. Vollständiger Cold-Start-Handoff A — R-M0-POC1-IMPL-1

### Rolle / Autorität

Du bist `R-M0-POC1-IMPL-1`, primärer ausführender Software- und Netzmodellierungsworker für IoSN Modul 0. Dieses Handoff ist **ein vollständiger Implementierungsauftrag nach separater Nutzerfreigabe**, kein Auftrag, einen weiteren Plan zu erstellen. Du darfst in deinem eigenen Branch Quellcode, Tests und reproduzierbare Daten-Schemata implementieren und die ausdrücklich benötigten isolierten Backend-/PyPSA-Testläufe durchführen, **nur nachdem** du die verpflichtende G0-Host-/Rights-/Safetyprüfung bestanden hast. Kein Merge nach main, keine Änderungen an historischen Architekturberichten.

**Verpflichtende erste Handlung:** Den **exakten finalen M4-0-Commit aus dem S-GOV-Ausführungsbericht** im Remote-Repository verifizieren; dann 10/20/30/40/50/60/70/80/85/90/95/96/97 vollständig und das Projekt-`pyproject.toml` sowie den bestehenden `src/tyndp_reduce/pypsa_adapter.py` lesen. Verwende nicht ein unbestimmtes moving HEAD. Verstehe: CAN/2.0.0 aus 85 hat im Widerspruch Vorrang vor den unveränderten historischen CAN/1.0.0-Tabellen.

**Implementierungsbranch:** `implementation/iosn-m0-poc-m1-core-20261101` aus dem verifizierten **M4-0-Endcommit**. Keine direkten Änderungen an `main`, kein Merge. Es ist zulässig, die neue Modul-0-Paketstruktur getrennt von `tyndp_reduce` zu implementieren; die bestehenden Reduktionsalgorithmen bleiben unverändert.

### Ein einziges konsolidiertes PoC1-Lieferpaket

1. **G0 direkt zuerst ausführbar prüfen:** host/CPython/ABI, tatsächlich installierbare `pypowsybl==1.16.1`/`pypsa==1.4.0` und transitive Lock-/Wheel-/Native-BOM; keine Core-7.4.2-Kompatibilitätsannahme. Die sichere ZIP/XML-/Memory-/Timeout-Policy aus 96 anwenden. Tatsächliche Profil-URIs und FullModel-/Boundary-/Authority-Referenzen der gewählten originalen Fixtures prüfen; Rechte/Redistribution belegen, andernfalls nur nachweislich zulässige synthetische/anders lizenzierte Tests verwenden und Capability begrenzen.
2. **Datenarchitektur implementieren:** immutable Content-Addressed Originalablage, Dataset-/Source-/Profile-/Header-/Graph-Manifest, `source_entities/source_objects/source_occurrences` mit nullable mRID und Original-RDF-Subject, QualifiedIdentityNamespace, Originalhierarchie der Stationen/Länder/Terminals und robustes `CAN/2.0.0`-SQLite-Schema mit PK/FK/Unique. Revisionsraum source_model_set/source_revision/operating_state/canonical_revision/projection_id. SOURCE/DERIVED/DEFAULT/MISSING und Fehlerledger.
3. **PowSyBl BackendPort implementieren:** versionskorrekt `pypowsybl.network.load(...)`/DataFrame-/Terminals-/Switch-/Transformer-Adapter nur bei tatsächlich nachgewiesenen APIs, Profile/EQ/SSH/TP/SV/Boundary/GL nach Scope. `NODE_BREAKER`-Switch-/Terminal-Faltung und `BUS_BRANCH` direkte TP-Terminal-Zuordnung; BB ohne TP BLOCK. Keine erdachten Country-/Source-Substation-Werte aus repräsentativer IIDM-Station.
4. **Elektrischer Kern und PyPSA-View:** mindestens ACLineSegment/EquivalentBranch, Generator/Load/ExternalInjection, einfacher 2W-Transformer, Basen/Units/Signs/AC-Islands/Status sowie qualifizierte Basis-PyPSA-Abbildung. Exportunabhängiges append-only `projection_quality` und Witness; DNR/1.0.0 mit typed Source-/State-/Projection-/Basis-/Port-/Limit-/Sidecar-Referenzen, auch bei nicht unterstützten Geräten. Nicht abgebildete 3W/PST/HVDC etc. nicht still löschen: benannter UNSUPPORTED-Status bis POC2.
5. **M0-PUBLISH/1.0.0:** immutable Blobs+Manifest vor SQLite-CAS-Pointer, Idempotency/Crash-Recovery/Hash-/Source-Witness nach 85 §7; T-05-/T-24-Kernnegative als automatisierte Tests.
6. **QA/Tests als Teil desselben Makros:** vorhandene T-01…T-12, T-15, T-18, T-20 **soweit im PoC1-Gerätescope relevant** mit positiven und negativen F-01/F-02/F-04/F-06-/kleinen PyPSA-Fällen; vertraglich gewünschte, nicht abgedeckte T-Zellen als NOT_EXECUTED ausweisen. API-Interface für den unabhängigen T-06-Worker (CanonicalSnapshot/SourceFacts, Normalisierungsregel und Fixturehash) ohne Daten aus seinem Parser vorwegzunehmen. `CANONICAL_IMPORT_READY` **bis zum echten unabhängigen T-06-PASS nicht** erteilen.

### Nachweise / akzeptierte Status

Publiziere ein vollständiges `EXECUTION_REPORT.md` mit:
- exaktem finalem Remote-Commit, Branch, Diff, Codepfaden, schema/port/API-Versionen;
- Windows/Linux/CPython und nativer Bundle-/Wheel-/Dependency-Fingerprint, tatsächlich ausgeführtem G0;
- CGMES-Version/Familie/Profil-URIs, Datensatzberechtigung, alle verwendeten SHA-256-Fixtures;
- Requirements T-01…T-24 scoped Testmatrix: PASS/FAIL/BLOCKED/NOT_EXECUTED pro Fixture/Version, negative Fälle, kein fiktives Ergebnis;
- Details zu Identity-/SourceHierarchy-/Country-/TP-/Units-/Port-/ProjectionQuality-/Publish-Witness;
- Provisorische/Ready-Flags getrennt: `CANONICAL_IMPORT_PROVISIONAL` möglich; `CANONICAL_IMPORT_READY` ausschließlich nach Integration des separaten T-06-Witness durch S-GOV;
- bekannte exakt benannte Blocker, nächste von PoC2/PoC3 benötigte Interface- und Fixture-Verträge.

**Stopregeln:** fehlende Nutzungsberechtigung, inkompatible native Runtime, Original-ID-/TP-/Country-Unentscheidbarkeit, unkontrollierte ZIP/XML-Verarbeitung, nicht beweisbare SQLite/FS-Atomizität oder ungeeignetes elektrisches Modell ⇒ betroffene Capability BLOCKED. Keine automatische eigene RDF/XML-Universalengine, keine komplette VeraGrid-Production-Runtime als Ersatz, keine POC2-/POC3-Mikroentwicklung. Partieller, präzise qualifizierter PoC ist zulässig; eine falsche READY-Freigabe nicht.

---

## 3. Vollständiger Cold-Start-Handoff B — R-M0-T06-INDEPENDENT-1

### Rolle / Autorität

Du bist `R-M0-T06-INDEPENDENT-1`, **unabhängiger Implementierungs- und Datenwitness-Worker** für REQ-009/T-06. Dein Ergebnis darf **nicht** aus einem vom PoC1-Worker erzeugten Parser-/IIDM-/Canonical-Snapshot rückabgeleitet werden; die physische CGMES-Datei muss **durch einen zweiten unabhängig betriebenen Backend-/Parserpfad** eingelesen werden. Du bist kein Reviewer der ganzen Architektur und implementierst **keinen** alternativen vollständigen produktiven VeraGrid-Konverter.

**Verpflichtende erste Handlung:** Remote verifizieren: finaler M4-0-S-GOV-Commit (aus S-GOV-Handoff), denselben eingefrorenen CAN/2.0.0-/T-06-Vertrag, 50 §4 T-06, 70, 85 §§1–3/6, 95/96 sowie 97 vollständig lesen. Die gleichen Source-Git-Commit-/Datensatz- und Versionpins wie PoC1 zugrunde legen, aber eigenes unabhängiges Laufzeit-/ParsedSource-Protokoll verwenden.

**Branch:** `validation/iosn-m0-t06-independent-20261101`, von demselben finalen M4-0-Commit. Keine Änderungen an PoC1-Produktivdateien, kein Merge. Minimaler read-only Testadapter darf auf eigenem Branch in `tests/` oder eigenem Prüfverzeichnis leben.

### Ein einziges konsolidiertes T-06-Arbeitspaket

1. Unabhängig `VeraGridEngine==6.7.20` und die tatsächlich verwendeten v2.4.15/v3.0 CGMES-Parserklassen/API-Pfade mit eigenem Lock-/Native-/Python-Manifest qualifizieren. Wenn eine relevante Version/Fixture nicht importierbar ist, den Blocker und verfügbare alternative **wirklich unabhängige** Quelle benennen, nicht PoC1-Mapping als „zweites Backend“ verwenden.
2. Für genau bezeichnete, zulässig nutzbare, unveränderte identische Rohdateien derselben Fixturehashes den Originalgraph/Profile/FullModel-/Authority-/RDF-/Terminal-/Equipment-Bestand **selbst** einlesen. Erzeuge eigenständige read-only normierte `BackendSnapshotV1`-/`SourceFacts`-Tabellen nach CAN/2.0.0 für den **gemeinsamen Mindestabdeckungsscope**: SourceEntity/Occurrences, Equipment-/Terminal-FKs, Status, reale Country-/Substation-Herkunft soweit Source nachweislich, BusBranch TP, AC-Line/Gen/Load/2W-Units und Sign. Ausdrücklich reporten, wenn die unabhängige Parser-API eine erforderliche Rohrelation nicht liefert.
3. Ein separater **Paritätsrunner** vergleicht später die beiden unabhängig erzeugten Snapshot-Manifeste: gleiche Originaldatei-SHA-256, CGMES-Familie/Profil-URIs und Input-Policies; normalisierte PKs, Equipment/Terminals, FK, Unit-Werte, SourceOrigin-Provenienz; numerische Delta-Metriken nach dokumentierter Einheiten-/Toleranz-/Absence-Policy. Keine Parität durch gefilterte Werte oder unbewiesene Null-Defaults erzwingen.
4. Negative Fälle: gleiche mRID in EQ/SSH ohne Doppel-Entity; RDF-only ohne MRID; BLANK_NODE innerhalb/außerhalb Original-Graph-Scope; Authority-Kollision; BB ohne TP; SourceCountry-Fehlschluss nach IIDM-Merge; absichtlich verdrehte elektrische Vorzeichen/Basen; fehlendes Feld als UNSUPPORTED statt stiller Gleichheit.
5. Zeige formal, welche Datensätze/Felder tatsächlich **beide** Backends qualifiziert haben, wo `PASS`, `FAIL`, `NOT_ASSESSED` oder `UNSUPPORTED` entstanden sind. Ohne PoC1-Ergebnis kann die unabhängige Erzeugung PASS erhalten, die **vergleichende** T-06-Parität aber bleibt WAITING_FOR_PRIMARY_SNAPSHOT; keine falsche unabhängige Doppelprobe behaupten.

### Nachweise / Ergebnis

Publiziere nur auf eigenem Branch einen `T06_INDEPENDENT_EVIDENCE_REPORT.md` mit:
- exaktem Remote-Commit, eigenem Code-/Konfigdiff, Backendversionen und ggf. fehlenden APIs;
- Origin-SHA-256 aller verwendeten Originaldateien, Rechte-/Lizenzstatus, tatsächlichen Profil-URIs/States;
- Hashes/Schema einer **originär durch VeraGrid geparsten** read-only Snapshotdatei;
- Vergleichsreports gegen PoC1 nur nach tatsächlicher Übergabe von dessen Snapshot, inklusive pro-Feld-Deltas und abweichender Source-/Country-/Terminal-Semantik;
- Anforderungen/Tests REQ-009/T-06/T-24 mit scoped Status und exakten Grenzen;
- Schlussklasse `T06_INDEPENDENT_PARITY_PASS_SCOPED`, `T06_INDEPENDENT_SNAPSHOT_READY_AWAITING_PRIMARY` oder `T06_BLOCKED_OR_INCONCLUSIVE`.

**Untersagt:** Nutzung der PowSyBl-ParsedSource als eigenen Parser, künstliche identische Mocks, ungeprüftes Klassengleichsetzen von VeraGrid und PyPowSyBl, stilles Ignorieren fehlender Source-Felder, Mutation des produktiven M0-Pakets und Behauptung vollständigen VeraGrid-Produktionsimports.

---

## 4. Konsolidierungs- und späterer Parallelstartvertrag

**S-GOV-POC1-Gate:** PoC1-Implementierungsbranch und T06-Branch müssen denselben Source-/Fixture-/CAN-/DNR-Vertrag verwenden, auch wenn sie unabhängig parsen. S-GOV prüft die genauen **Remote-Commits**, Testdateien, Fixturehashes, Status und die tatsächlichen Implementierungsdiffs; danach genau ein konsolidierter Return, keine Mikroreview-Schleifen.

**Folgemakros erst danach:**
- `PoC-M2`: Sondergeräte, Multi-IGM, qualifizierte Kron-Y-/Tap-/HVDC-/PST-/Limit-/Country-/GL-Funktionen, exportunabhängige ProjectionQuality, NUM-Guards, PyPSA ACPF/LPF. Eigener Branch aus von S-GOV akzeptiertem PoC1-Integrationscommit; Test T-03/T-07…T-20/T-23 (wenn SV geeignet).
- `PoC-M3`: SSH/SV-Update-Export, originalgraphgestütztes SourceBackmapping, manueller SSH-only-Witness vs CGM-Quick-SSH/SV mit passendem berechneten SV, semantische Originaltripel-/FullModel-Diff, T-05/T-21/T-24-Crash-/Recovery. Eigener Branch aus **demselben** akzeptierten PoC1-Integrationscommit; parallel zu PoC-M2.
- **Keine** automatische CREATE_FROM_PYPSA- oder M1-Adapterfreigabe; beide sind getrennte spätere Ownerentscheidungen.

## 5. S-GOV-Autorisierungsvorlage für die Userentscheidung

Die beiden Handoffs sind jetzt vollständig vorbereitet und referenzieren die eingefrorene M4-0-Architektur. Eine künftige Freigabe kann lauten:

> Ich autorisiere PoC-M1 und den unabhängigen T-06-Witness als zwei parallele konsolidierte Implementierungs- und Testmakros auf getrennten Branches entsprechend M4-0-Dokument 97 am angegebenen unveränderlichen Commit. Jeder Worker führt zuerst die im Dokument 96 definierten G0-Host-, Datensatzrechte- und Sicherheitsprüfungen durch; bei Blockern werden betroffene Capabilities ausdrücklich BLOCKED, ohne fiktiven PASS. Keine eigenmächtige Änderung an main, keine POC2-/POC3-/CREATE-Ausführung.

Bis diese Autorisierung in den jeweiligen Chats tatsächlich vorliegt, bleibt der Ausführungsstatus **PREPARED_NOT_STARTED**.
