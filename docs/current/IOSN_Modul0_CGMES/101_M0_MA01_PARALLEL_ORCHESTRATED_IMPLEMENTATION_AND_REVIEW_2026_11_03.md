# M0-MA-01 — Orchestrated CGMES ↔ PyPSA Implementation, Export and Independent Qualification

**Datum:** 2026-11-03  
**Projekt:** IoSN / TYNDP / PyPSA — **ausschließlich Modul 0**  
**Repository:** https://github.com/AlOussama/TYNDP_Products  
**Auftragstyp:** EIN gesamthafter Makro-Ausführungsauftrag mit intern parallelisierbaren Arbeitspaketen, Subagenten, lokalen Codierungsworkern und unabhängigen Review-Workern.  
**Owner:** Project Owner (einmalige Scope-/Ausführungsfreigabe); **Ausführungsverantwortung:** M0-ORCH-01 (Lead-Orchestrator / S-GOV-Ausführungskoordination).  
**Technische gefrorene Basis:** 8d3bdbf19656a66ba342b223d0ca30613e07a80c (M4-0-Endstand).  
**Normativer Architektur-Freeze:** b1e284996fa69f81651daf9150b829e6a42e4ce3 (M3-Reparatur-/Freeze-Baseline).
**Übergeordneter Makrostatus bei Erstellung:** PREPARED_NOT_STARTED. Veröffentlichung dieses Handoffs ist keine Ausführung.

## 0. Verbindliche Entscheidung: EIN Makro, mehrere interne Worker

**Alle bislang getrennten M5A/M5B/M6/M7A/M7B/M8 werden in EINEN Auftrag M0-MA-01 integriert.** Der Project Owner muss nicht jeden Unterauftrag separat in einem neuen Chat starten. Der ausführende M0-ORCH-01 darf intern mehrere lokale Agenten, parallele Arbeits-Chats, Subagenten, Worktrees, Testprozesse und Review-Agenten einsetzen. Der Orchestrator ist für die vollständige Umsetzung, technische Integration, Resultattransparenz und einen konsolidierten Endbericht verantwortlich.

**Wesentliche Unterscheidung:** Ein einziger User-Handoff bedeutet **nicht**, dass nur ein Agent den gesamten Code erstellt und sich selbst als unabhängigen Reviewer ausgibt. Reviewer und Implementierungspfade müssen nachprüfbar getrennt sein. Insbesondere REQ-009/T-06 erfordert einen **tatsächlich unabhängigen zweiten Parser auf denselben rohen Originaldateien** und nicht lediglich eine andere Chat-Instanz.

**Normalfall:** Ein Startauftrag, internal autonomous task decomposition und begrenzte Defektkorrekturen, eine abschließende Status-/Merge-/Releaseentscheidung. **Ausnahme:** Fehlende Datenrechte, Sicherheits-/Native-G0-Verstöße oder eine neue Scope-/Architekturentscheidung dürfen nicht stillschweigend übergangen werden; diese Capabilities bleiben BLOCKED oder benötigen ausdrückliche neue Owner-Freigabe. Keine zusätzlichen Nutzerfreigaben für bereits im Normscope enthaltene interne Teilaufträge.

## 1. Harte Scopegrenze und technische Autorität

**Enthalten:**
- CGMES 2.4.15/3.0 (nur echt qualifizierte und erlaubte Profil-/Boundary-Varianten): Import der Netztopologie, Netzelemente und Zustände.
- Unveränderliches Originalquellen-/RDF-/FullModel-/Authority-/Profile-Archiv; verlustbewusste Identität, SourceOccurrences, Geo-/Country-/Terminal-/Topology-Origin.
- CAN/2.0.0 als versionierter Backend-neutraler Datenvertrag mit SOURCE/DERIVED/DEFAULT/MISSING, Revisionen und M0-PUBLISH/1.0.0.
- Detaillierte elektrische PyPSA-Projektion, DNR/1.0.0, Projektionsverlust- und SourceQuality-Witness, AC-Power-Flow/Linear-Power-Flow, soweit fachlich testbar.
- Zwei **getrennt qualifizierte** UPDATE_IMPORTED-Exportpfade: MANUAL_IGM_SSH und CGM_QUICK_SSH_SV.
- Runtime-/Sicherheits-/Rechte-/Identitäts-/Backend-Paritäts-/Numerik-/Roundtrip-/CAS-/Crash- und unabhängige E2E-Nachweise.

**Ausgeschlossen, ohne Auswirkungen auf M0-Release:**
- Modul 1 einschließlich PECD/PACD, Wetter-/Wind-/PV-/Hydro-/Last-Zeitreihen und deren räumliches Matching.
- PyPSA-Netzreduktion, Clustering, Regionalisierung und andere IoSN-Module.
- CREATE_FROM_PYPSA (vollständiger CGMES-Neuaufbau) und unqualifizierte große reale europäische CGM-Datensätze; dies sind separate optionale Scope-Entscheidungen.
- Pauschale IEC-/ENTSO-E-Konformitätszertifizierung.

**Referenzen (vor Start zwingend lesen und exakt versionieren):**
1. Normativ: [85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md) (CAN/2.0.0, DNR/1.0.0, Topologie, Qualität, T-06, Export, CAS).
2. Requirements/Testmatrix: [10_REQUIREMENTS.md](10_REQUIREMENTS.md), [50_VALIDATION_CONTRACT.md](50_VALIDATION_CONTRACT.md), [70_IMPLEMENTATION_READINESS.md](70_IMPLEMENTATION_READINESS.md).
3. Architektur/ADR: [30_CANONICAL_DATA_CONTRACT.md](30_CANONICAL_DATA_CONTRACT.md), [40_SOFTWARE_ARCHITECTURE.md](40_SOFTWARE_ARCHITECTURE.md), [60_ARCHITECTURE_DECISION.md](60_ARCHITECTURE_DECISION.md), [90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md).
4. M4-0-RunRelease und Python-API: [95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md](95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md), [96_M4_0_RUNRELEASE_POLICY_AND_GATES.md](96_M4_0_RUNRELEASE_POLICY_AND_GATES.md), [98_M4_0_PREPARED_EXECUTION_CONTRACT.json](98_M4_0_PREPARED_EXECUTION_CONTRACT.json), [99_S_GOV_M4_0_FINAL_EXECUTION_REPORT.md](99_S_GOV_M4_0_FINAL_EXECUTION_REPORT.md).
5. Historical work orders, superseded as **user-facing execution structure**, retained as technical detail: [97_M4_0_NEXT_MACRO_ASSIGNMENTS.md](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md), [100_S_GOV_STATUS_AND_NEXT_MACRO_HANDOFFS_2026_11_03.md](100_S_GOV_STATUS_AND_NEXT_MACRO_HANDOFFS_2026_11_03.md), [80_INDEPENDENT_ARCHITECTURE_REVIEW.md](80_INDEPENDENT_ARCHITECTURE_REVIEW.md).

**Normvorrang:** 85 / CAN/2.0.0 / DNR/1.0.0 schlägt konfliktbehaftete ältere Tabellen in 30/40/60/70; 96 ist bindender G0-RunRelease-Vertrag. Bestehende Source/Tests/Adapter außerhalb M0 nur kompatibel, nicht mutierend, nutzen.

## 2. Runtime-/Daten-G0 als erster interner Subtask

**Orchestrator + Worker W0 (Runtime/Source Qualification)** führen vor untrusted CGMES-Parsing und qualifikationsrelevanten Tests das G0-Paket aus.

- Verifiziere Remote-Basis SHA, Architekturdateien, Git-Blob-Hashes, echte Arbeitsumgebung und Reproduzierbarkeit.
- Prüfe OS, Python-/ABI-Versionen, installierbare Kandidaten **pypowsybl==1.16.1, pypsa==1.4.0, VeraGridEngine==6.7.20**, aufgelöste Wheels/SDists und transitive Abhängigkeiten, tatsächliche Native-Core-/Backend-Buildidentitäten. Kandidatenpins dürfen nur mit begründetem, dokumentiertem Kompatibilitäts-Witness geändert werden, nicht still.
- Nutze zunächst **offizielle PyPowSyBl-Python-API**, nicht eigene Java-Anwendung. Nachgewiesene Python-Methoden sind noch kein Runtime-PASS.
- Erwerbe/prüfe tatsächlichen physischen Source-Fileset (CGMES-Profil-URIs statt Dateinamen), Originaldatei-SHA-256, FullModel/Authority, Boundary und Rights-/Redistribution-Gates. Private lizenzierte Netzdaten nicht öffentlich committen. Nur rechtmäßig verfügbare Quellen oder explizit synthetische Fixtures einsetzen.
- Erzwinge die in 96 spezifizierten ZIP/XML-/Path-/DTD-/externe-Entity-/Dateisystem-/CPU-/RSS-/Timeout-/Sicherheitslimits und versieh sie mit negativen Tests vor Verarbeitung nichtvertrauenswürdiger Quellen.
- Erzeuge eine **read-only, immutable Fixture-Registry** mit Source-ID, bytes SHA-256, Profilfamilie, Profile-URIs, Rechten, Scope und Ausführungskonfiguration, die alle Worker teilen. Keine Änderung oder nachträgliche automatische Sanitization/Hashersetzung.

**G0-Gate:** PASS_SCOPED oder blockiert nach Ursache. Ein blockiertes reales Dataset erlaubt einen gekennzeichneten synthetischen/öffentlichen Teilpfad, jedoch nie REAL_CGM_READY. Ein nicht verfügbares natives Backend wird nicht als PASS simuliert. Keine unautorisierten Netzwerk-/Daten-/Artefaktoperationen.

## 3. Arbeitspakete: intern, nicht als sechs separate User-Handoffs

### W0 — Orchestrierung, Verträge, G0, Merge-Owner

Owner: M0-ORCH-01 (Lead). Darf Unteragenten/Werkzeuge beauftragen, behält Integrations- und Berechtigungsverantwortung.

**Ergebnis:** eingefrorenes Fixture-/Runtime-/Normmanifest; offengelegte Arbeitspaketgrenzen; getrennte Branch-/Worktree-IDs; explizite Completion-/Testgates; laufende Issue-/Defekt- und Abhängigkeitsregister.

**Nicht delegierbar:** G0-Entscheidungsregister, Konflikterkennung, finale Konsolidierung, Freigabeempfehlung. M0-ORCH ist **nicht** unabhängiger Reviewer seiner eigenen Implementierung.

### W1 — Originalgraph, Python-CGMES-Backend und Importsource

Owner: CGMES-Backend-/DataProvenance-Implementierungsagent. Vorzugsweise auf eigenem Worktree.

**Teilaufgaben:**
- Python-first CGMES-Formatport mit pypowsybl.network.load, realen get_*-DataFrames, update_from_file nur in qualifizierten isolierten Situationen, tatsächliche CGMES-Parameter-/Extensions-Inspektion.
- Original-RDF/XML-, ZIP-/Profil-/FullModel-/MAS-/Authority-/Boundary-Archiv unveränderlich und content-addressed; sichere Originaldatei-Hashes und Import-/SourceModelSet-/SourceRevision-/OperatingState-Manifeste.
- Original SourceObjects/SourceOccurrences: mRID vs. RDF subject, RDF-only, Blank Nodes, Graph- und Authority-Namespace, SourceHierarchy, Country/Geo/Terminals/Connectivity/TP; NODE_BREAKER und BUS_BRANCH (ohne TP kein erfundenes Netz).
- Fehler-/Provenienz-/Missing-Ledger. Unbekannte Rohrelationen nicht still verwerfen.

**Output:** BackendPort, OriginalSourceStore, SourceFactsV1, Fixtures/Contract-Tests und Implementierungsbericht. **Keine** Repräsentation der eigenen Rohdaten als unabhängiger T-06-Witness.

### W2 — CAN/2.0.0, elementare PyPSA-Projektion, Publisher

Owner: Canonical-/Python-/PyPSA-Implementierungsagent, eigener Worktree. Darf **parallel zu W1** starten, sobald der von 85/40 festgelegte Inputvertrag für SourceFactsV1 abgestimmt ist (kein W1-Code als zwingende Startvoraussetzung).

**Teilaufgaben:**
- Typed CAN/2.0.0-Schema (z. B. SQLite) mit PK/FK/Unique, SourceObject vs SourceOccurrence, Original-/Canonical-/OperatingState-/Projection-Revisionsräumen und SOURCE/DERIVED/DEFAULT/MISSING.
- Basis ACLines/EquivalentBranches, Loads/Generators/ExternalInjections, einfache 2W-Transformatoren, geschaltete Topologie, AC-Inseln, P/Q-/Units-/Sign-/Base-Referenzen, sichere PyPSA-Kernansicht.
- DNR/1.0.0-typed Output samt Sidecars/Qualitätsflags, auch wenn Sondergeräte noch UNSUPPORTED sind.
- M0-PUBLISH/1.0.0: immutable blobs/Manifest **durabel vor** SQLite-CAS-Commit als einzigem Sichtbarkeitspunkt, Idempotenz und überprüfbare Recoveryfälle.
- Testharness für T-01…T-12/T-15/T-18/T-20 im eigenen tatsächlich abgedeckten PoC-Scope; Pflichtnegative ohne übertriebene Generalisierung.

**Output:** CanonicalStore, Publisher, PyPSACoreAdapter, DNR v1, unit-/schema-/failure-injection-Tests, verständliche Statusmatrix.

### W3 — unabhängiger T-06-Backend- und Source-Facts-Witness

Owner: **anderer unabhängiger Review-/Implementierungsagent**, eigener Worktree und eigene Parserabhängigkeit. Kein gemeinsamer Source/ParsedSource/Canonical-Codepfad mit W1/W2.

**Parallelstart:** direkt nach read-only Fixture-Registry; wartet **nicht** auf W1. Paritätsrunner kann später die unveränderlichen W1-SourceFacts abholen.

**Teilaufgaben:**
- Eigenständige CGMES-2.4.15-/3.0-Fixture-Einlesung mit VeraGridEngine als unabhängiger Parserpfad, nicht PowSyBl und nicht PoC1-Rückexport als scheinbares Original.
- SourceFacts-/BackendSnapshotV1 des **gleichen Originaldatei-SHA-256-Sets** einschließlich mRID/RDF-Subject/Occurrences, Terminal-/Equipment-FKs, Provenienz/Authority, TP, Country/Substation/SourceOrigin, Units/Signs/Status.
- Eigenes Normalisierungs-/Differenzverfahren mit per-Feld-Deltas, klarer Missing/Unsupported-/Tolerance-Policy, Negativfixtures (BlankNode, RDF-only, ID-/Authority-Kollision, BB ohne TP, Country-Merge, Sign/Units).
- Paritätsvergleich erst wenn W1-Snapshot vorliegt. Ohne zweiten echten Parser oder identische Rohfile-Hashes: T06_BLOCKED, kein CANONICAL_IMPORT_READY.

**Output:** T06_INDEPENDENT_EVIDENCE_REPORT, eigener Code/Runner/Testlogs, SnapshotSHA und Paritätsledger. Ein separater Chat ist **nicht zwingend**, sofern wirkliche Code-/Parser-/Agententrennung nachweisbar ist.

### W7 — QA-Fixtures, CI, Negativtests und Buildreproduzierbarkeit

Owner: separater Test-/Infra-Agent. Früh mit W1/W2/W3 parallel einsetzbar, schreibt **nicht** dieselben produktiven Implementierungsdateien.

**Teilaufgaben:** SourceFixtures F-01…F-07 nach 95 qualifizieren/aus rechtmäßig erlaubten Originalquellen erstellen, zusätzlich als SYNTHETIC getrennt benennen; Testmatrix REQ-001…048/T-01…24, CI-Suites, Fixture-/Software-Lock-/BOM-/Hash-Erfassung, Negativtests für Zip-Bombs, Path Traversal, XML entities, Missing IDs, Topology, Units, Crash/2-Writer-CAS, Export-/Loss-Verletzung. Testresultate niemals vortäuschen und fehlende Testumgebung als BLOCKED/NOT_EXECUTED melden.

**Output:** versionierter Fixtures-Index, CI-Runner und reproduzierbares Testevidenzpaket.

### W4 — elektrische Vollprojektion und PyPSA-Qualifizierung

Owner: qualifizierter PyPSA-/Elektrotechnik-Implementierungsagent. **Nach G1-Interfacefreeze**, dann **parallel mit W5**.

**Teilaufgaben:** 3W-Transformator mit korrekt qualifizierter Y-/Kron-/Ersatznetz-Semantik, RatioTap/PST (Richtung/Regeln/Limits), linearer/nichtlinearer Shunt, Current/Operational Limits, HVDC und mehrportige Insel-/Port-/Loss-Semantik, Multi-IGM/Boundary, GL/CRS-Missing-Herkunft. DNR-Typen erweitern, exportunabhängiges append-only projection_quality/projection_witnesses-Ledger verwenden. **Nichts still ignorieren:** EXACT nur mit Witness, APPROX mit Gültigkeitsdomäne und Fehlerkorridor, UNSUPPORTED mit begrenztem Scope.

**Elektrische Belege:** Ybus/Zweitor/Trafo-/Tap-/Phase-Shift-Referenzen, KCL-/P/Q-/Base-/Sign-Invarianten, AC-Islands/Slacks, PyPSA ACPF/LPF, T-03/T-07…20/T-23 nur soweit echte Daten und vereinbarte Toleranzen vorliegen.

**Output:** elektrische Adapter/Tests, qualifizierte scoped PYPSA_ACPF-/LPF-Evidenz. Kein Exportcode und kein M1.

### W5 — originalgraphbasierter Update-Export

Owner: eigenständiger CGMES-Export-/Originalgraph-Implementierungsagent. **Nach G1**, **parallel zu W4**. Getrennter Branch vom selben G1-Integrationscommit.

**Teilaufgaben:**
- UPDATE_IMPORTED mit SourceBackmapping, Originalgraph als Autorität, MutableState-/Revision-/Conflict-/Idempotency-/Dependency-/FullModel-/MAS-/Authority- und OriginalID-Fidelity, Originaltripel-/SemanticDiff und M0-PUBLISH-/CAS-Recovery.
- STATE_NON_TOPOLOGY als erster zu qualifizierender Update-Scope. STATE_TOPOLOGY_AFFECTING, STRUCTURAL_EQ_TP und SYNTHETIC_CREATE bleiben ohne eigene normative Qualifikation gesperrt.
- **MANUAL_IGM_SSH** (SSH-only je IGM) getrennt von **CGM_QUICK_SSH_SV** (SSH je IGM + tatsächlich qualifiziertes gemeinsames SV).
- Python-first gezielter API-Witness: get_sub_networks/get_sub_network; get_extensions('cgmesMetadataModels'); get_export_parameters('CGMES'); create_extensions in isolierten Kopien; Network.save(..., format='CGMES'); echte importierte Header-Mutation und qualifizierten Reimport **nachweisen**. Die Existenz einer Methode allein ist kein funktionierender Export.
- Originalgraph-Delta/WhitelistedChanges, gegen Originalset eingefrorene EQ/TP/Boundary-Pakete, FullModel/Dependencies/Supersedes, unabhängiger CGMES-Reimport, T-05/T-21/T-22/T-24, fehlerhafte SV-/Profile-/CAS-/Conflict-Negativfälle.

**Output:** Update-Exportport, zwei getrennte Exportmanifeste/Capabilities, Roundtrip-/Graph-Diff- und Recovery-Logs. Bei nachgewiesen unzureichender Python-API: **BLOCK_EXPORT_UNPROVEN**, keine eigenmächtige Java-App oder generische XML-Patcher-Freigabe.

### W6 — unabhängige integrierte System-/Elektrik-/RDF-Endabnahme

Owner: **von W1/W2/W4/W5 verschiedener unabhängiger Agent** mit eigener Testmethodik, eigenen Prüfwerkzeugen und eigenem Review-Branch. Darf Testskripte erstellen und Tests ausführen, aber nicht seine zu reviewenden Produktivänderungen selbst als alleiniger Autor begutachten.

**Start:** nach W0-Zusammenführung aller W1/W2/W3/W4/W5/W7-Änderungen in einen **separaten Integrationstest-Branch**, niemals nach main.

**Teilaufgaben:**
- Verifikation jedes Commits, Diff/Code-/Abhängigkeits-/Fixture-/Runtime-/Security-/Rights-/QA-Nachweises.
- Eigene End-to-End-Proben: Original-CGMES 2.4.15/3.0 → PyPowSyBl → Origin-/CAN/2.0.0 → PyPSA DNR/1.0.0 → elektrische AC/LPF-Evidenz → jeder separat unterstützte UPDATE_IMPORTED-Export → Graph-Diff und unabhängiger Reimport.
- Elektrische Gegenoracle (Ybus, PowerFlow, Sign/KCL/Islands), T-06 muss wirklich zwei unabhängige Rohparser enthalten, Negativfälle für Source IDs/Country/Boundary/TP/SV, CAS-Race/Crash/Resume, Versions-/Native-/Data Rights.
- REQ-001…048 und T-01…24 auf **per Fixtur, Profilfamilie und Capability** genau PASS/FAIL/BLOCKED/NOT_EXECUTED prüfen; Defect-Ledger mit Severity, Reproduktion, Owner, tatsächlicher Fix-Provenienz.
- Keine bloße Übereinstimmung mit dem produktiven Code als unabhängige Referenz ausgeben.

**Output:** INDEPENDENT_E2E_REVIEW.md, Test-/Defect-/Matrix-/Scope-Evidenz, differenzierte Releaseempfehlung an W0.

## 4. Geplante parallele Ausführung und Gates

### Phase P0 — gemeinsamer Start / G0

**W0** verifiziert Source und Repo, erstellt Worktrees, identifiziert Host/Runtime/Entitlement/Fixture-Hashes, aktiviert Security-Policy und erzeugt ein unveränderliches gemeinsames Inputmanifest. W7 darf Test-/CI-Bereitschaft bereits parallel dokumentieren; Parserausführungen erst nach dem jeweiligen G0. Keine Wartepflicht auf neue Nutzerantworten für im Scope autorisierte interne Arbeit.

**G0 Ergebnis:** PASSED_FOR_NAMED_FIXTURES oder BLOCKED_SCOPED; keine simulierten Importe.

### Phase P1 — paralleler Kern und unabhängige Parität

**W1 || W2 || W3 || W7** bearbeiten ihre disjunkten Dateien/Worktrees parallel. W0 richtet zuerst die bekannten 85/40-Port-/CAN-/DNR-Interfaces als unveränderliche Input-/Output-Kontrakte aus. Falls Unklarheit, in kleinem Cross-Team Interface-Vorschlag dokumentieren und 85 respektieren; keine stille Umdefinition.

W0 führt W1+W2+W7 auf einen dedizierten G1-Integrationsbranch zusammen und prüft Schema-/Publisher-/Fixture-/Coretests. **W3 läuft unabhängig weiter** und veröffentlicht originären Snapshot; die T-06-Vergleichsstufe läuft nach Vorliegen von W1-Snapshot. Ein relevanter Unterschied kann defect/fix bedeuten; W0 darf ihn nicht wegstandardisieren.

**G1 Ergebnis:** stabile immutable SourceArchive/SourceFacts/CAN/Projection/DNR/Publish-API; Status PROVISIONAL oder scoped PASSED. **T-06 zwingend vor finalem CANONICAL_IMPORT_READY**. W4/W5 dürfen Codeentwicklung nach qualifiziertem stabilem G1-Vertrag parallel beginnen, selbst wenn ein Scope noch PROVISIONAL ist; finale Freigabe bleibt gesperrt.

### Phase P2 — elektrische und Export-Erweiterung parallel

**W4 || W5 || W7** auf getrennten Branches vom *identischen* durch W0 veröffentlichten G1-Integrationscommit. Keine gegenseitigen Produktivdateiänderungen, kein gegenseitiger abhängiger unkontrollierter Rebase; W0 verantwortet gezieltes Cherry-Pick/Merge auf Integrationsbranch und dokumentierte Konfliktresolution. Separate Tests für elektrische und Export-Capabilities. W3 liefert T-06-Delta-/Failure-Witness und darf bei Rohparser-Fehlern weiter getrennt testen.

**G2 Ergebnis:** reproduzierbarer integrierter Candidate mit eingefrorenen SHA/ABI/Fixture-Hashes, RunLogs, per-Capability-Entscheidungen; **kein** impliziter PASS bei fehlendem SV, Headern oder T-06.

### Phase P3 — unabhängiger Review, gezielte Korrektur, Abschluss

**W6** erhält nur den Candidate-Commit, normativen Vertrag und Rohfixtures, erstellt eigene unabhängige Gegenproben. W0 verteilt echte Defekte an W1/W2/W4/W5, vereinigt Fixes kontrolliert und gibt W6 eine neue explizit benannte Candidate-SHA. Keine endlose Mikroschleife: höchstens ein konsolidiertes reguläres Defect-Fix-Bündel, sofern sachlich möglich; danach verbleibende Defekte als BLOCKED/FAIL und klarer Folgebedarf im Abschluss. Sicherheits- oder Datenrechte-Stopregeln haben Vorrang.

**G3 Ergebnis:** eine finale, überprüfbare Integration-SHA und **ein** vollständiger unabhängiger Review sowie ein S-GOV-Orchestrator-Abschlussbericht. W0 entscheidet nur anhand tatsächlich unabhängiger Evidenz, keine Peer-Review-Selbstauskunft.

### Abhängigkeitsgraph (Pfeile)

G0 → (W1 || W2 || W3 || W7) → G1-Source/Canonical-Interfacefreeze → (W4 || W5 || W7) → G2 Integration → W6 E2E → G3 ReleaseDecision.

W3 beginnt in P1 und darf auf P2/P3 fortlaufen; Parität und Release hängen von identischen Rohdaten und unabhängigen Parsern ab, **nicht** davon, in wie vielen Chats die Arbeit stattfand.

## 5. Branch-/Agent-Isolation und Dateienownership

**Gemeinsame technische Ausgangsbasis für neue Worktrees:** exakter M4-0-Endcommit 8d3bdbf19656a66ba342b223d0ca30613e07a80c; dieser Makroauftrag wird separat unter einem unveränderlichen Dokumentcommit referenziert. Branches und tatsächliche Base-SHAs ins Worker-Manifest schreiben; keine moving-HEAD-Basis oder unbewiesene Fork-Gleichheit.

**Vorgeschlagenes Namensschema (nicht zwingende Dateipfade):**
- orchestrator/integration/iosn-m0-ma01-20261103;
- implementation/iosn-m0-ma01-backend-20261103 (W1);
- implementation/iosn-m0-ma01-canonical-20261103 (W2);
- validation/iosn-m0-ma01-t06-20261103 (W3);
- implementation/iosn-m0-ma01-electrical-20261103 (W4, Basis = G1);
- implementation/iosn-m0-ma01-update-export-20261103 (W5, Basis = G1);
- validation/iosn-m0-ma01-e2e-20261103 (W6);
- testing/iosn-m0-ma01-fixtures-ci-20261103 (W7).

**Physische Isolation:** getrennte git worktrees/Branches oder äquivalente isolierte Arbeitsverzeichnisse. W1 Source/Backend/Originalgraph; W2 CAN/Publish/Core Projection; W4 special electrical; W5 export; W3/W6 validation; W7 tests/fixtures/CI. Gemeinsame Dateien/Schema-/API-Verträge nur via dokumentierte Review-/Integrationsteile bearbeiten. W6 hat einen eigenen Prüfbranch, darf keine produktiven Ergebnisse der Implementierer als unabhängige Testoracle wiederverwenden. Keine gegenseitige ungeprüfte Übernahme von Testfixtures, die denselben Codefehler maskieren.

**Rollenunabhängigkeit:** W3 und W6 dürfen interne Subagenten/andere Working-Chats sein, falls deren separate Quellen-/Implementierungs-/Reviewprovenienz sich nachweisen lässt. Unterschiedliche Chatnamen allein erfüllen keine unabhängige T-06-Prüfung. Falls das Laufzeitsystem keine echten parallelen Subagenten/Worktrees bereitstellt: sequentielle Ausführung der disjunkten Pakete zulässig, unabhängiger Parser und Gegenprüfung bleiben zwingend. Niemals behaupten, nicht gestartete Worker hätten gearbeitet.

## 6. Qualität und harte Stopregeln

**Keine Aufweichung der bestehenden M0-Verträge:**
- SOURCE vs DERIVED vs DEFAULT vs MISSING mit nachvollziehbarem Origin- und ProjectionQuality-Ledger, auch ohne Export.
- NODE_BREAKER/BUS_BRANCH physisch richtig trennen; BUS_BRANCH ohne gültiges TP blockieren.
- Originalgraph/Identity/Authority/FullModel/Boundary erhalten, keine IIDM-Land- oder MAS-Fiktion.
- Aktualisierte CGMES-Header und MANUAL_IGM_SSH nicht lediglich wegen methodischer API-Verfügbarkeit als erfolgreich behandeln.
- CGM_QUICK_SSH_SV benötigt tatsächlich gelöstes qualifiziertes SV; sein Export ist **nicht** SSH-only.
- M0-PUBLISH blobrelease/fsync/Manifest vor SQLite-CAS-Pointer und umfangreiche Crash-/Duplicate-/ConcurrentWriter-Tests.
- Unbekannte Geräte, Mapping-Lücken, fehlende Rechte, native Runtime-Fehler, Source-Loss und nichtbestehende unabhängige Parität als BLOCKED/UNSUPPORTED dokumentieren.
- CGMES-2.4.15/3.0-Familie anhand tatsächlicher Profile-URIs/FullModel identifizieren, nicht Dateinamen oder vermutete Dummy-Profile.
- Keine produktive Implementierung oder Merge in main; keine Daten mit ungeklärten Redistribution-Rechten ins öffentliche Repository.
- Kein PyPSA-/CGMES-/RDF-/Native-/Performance-PASS ohne tatsächlich durchgeführte Messung, reproduzierbare Logs und unabhängige Referenz im jeweils erforderlichen Testscope.

## 7. Abnahme, Scope-Vektoren und Ergebnis

**M0-MA-01 gilt als administrativ abgeschlossen**, sobald W0 alle autorisierten Unterpakete bearbeitet, G0–G3 dokumentiert, den tatsächlich erreichbaren scoped Code-/Teststand veröffentlicht und einen einzigen konsolidierten Report vorgelegt hat. **Administrative Makrofertigstellung ist nicht gleich vollständiger technischer PASS.**

**Getrennte Fähigkeitsklassen (niemals zusammenfassen):**
1. CANONICAL_IMPORT_PROVISIONAL; CANONICAL_IMPORT_READY nur mit qualifiziertem echtem T-06 und benannten T-01…11.
2. PYPSA_ACPF_READY und ggf. LPF gesondert, nur für die belegten elektrischen Geräte, Inseln, Profilfamilien und die relevanten T-12…20/23.
3. UPDATE_EXPORT_READY_MANUAL_IGM_SSH nur nach qualifiziertem Originalgraph-/ModelHeader-/SSH-only-/Reimport-Witness.
4. UPDATE_EXPORT_READY_CGM_QUICK_SSH_SV nur nach richtigem SSH je IGM und qualifiziertem gemeinschaftlichem SV.
5. CREATE_EXPORT_READY = **OUT_OF_SCOPE/NOT_EXECUTED**, es sei denn ein separater späterer Ownerbeschluss autorisiert diese Funktion.
6. PERFORMANCE_QUALIFIED/REAL_CGM_READY = **OUT_OF_SCOPE/BLOCKED**, soweit Datensatzrechte/Budget/Bearbeitung fehlen.
7. MODULE_1_READY/PECD_INTEGRATION = **OUT_OF_SCOPE**, kein M0-Gate.

**Finale Lieferobjekte:** 
- ein ausführbarer Paket-/Code-/Schema-/Config-/Teststand auf separatem Integrationsbranch mit exakter Commit-SHA und für jedes Subteam belegter Base-/Head-SHA;
- vollständiger Runtime-/Native-/SBOM-/Daten-/Lizenz-/Fixture-/Hash-/Profilkatalog und versionsgerechte Sicherheits-/Ressourcenlimits;
- Originalgraph-/Canonical-/DNR-v1-/SourceFacts-/Quality-/Export-/Crash-/Reimport-/Diff-Evidenz;
- T-06-Bericht aus unabhängigem Zweitbackend; unabhängiger E2E-Reviewerbericht und Fehlerledger;
- Requirements REQ-001…48 sowie Test T-01…24 als per Profile/Fixture/Capability PASS/FAIL/BLOCKED/NOT_EXECUTED;
- EIN S-GOV-orchestrierter FINAL_EXECUTION_REPORT mit Matrix W0–W7, Gate-Entscheidungen, fehlenden Rechte-/Native-/Fixture-/API-Fakten, konkreten Defects, reproduzierbarer Run-Anleitung und eng abgegrenzter Releaseempfehlung;
- keinerlei main-Merge, außer ein zusätzlicher späterer, expliziter Ownerentscheid ordnet ihn an.

**Endklassen des Makros:** FULL_SCOPED_PASS (alle für den vorher benannten M0-Pflichtscope auf tatsächlich vorhandenen zulässigen Quellen qualifiziert), PARTIAL_SCOPED_PASS_WITH_BLOCKERS oder BLOCKED; zusätzlich technische Fähigkeitsvektoren je Familie/Profil/Fixture, keine pauschale ENTSO-E-Konformitätsbehauptung.

## 8. Einziger Copy-ready Startprompt

**Ein Auftrag im Hauptchat oder an einen lokalen Orchestrator genügt:**

> **Rolle: M0-ORCH-01, Lead Orchestrator für IoSN Modul 0 CGMES ↔ PyPSA.** Repository AlOussama/TYNDP_Products. Ausgangsbasis Commit 8d3bdbf19656a66ba342b223d0ca30613e07a80c, Architektur-Freeze b1e284996fa69f81651daf9150b829e6a42e4ce3.
>
> Ich beauftrage die **vollständige Ausführung des EINEN Makros M0-MA-01** nach diesem Dokument 101: Orchestrated CGMES ↔ PyPSA Implementation, Export and Independent Qualification. Dies ist ein echter **Implementierungs-, Integrations- und Prüfauftrag**, keine erneute Planung. Verifiziere zuerst den exakt verlinkten Dokumentcommit und die technischen Git-Commits, lies vollständig die normativen Quellen 10/30/40/50/60/70/80/85/90/95/96/97/98/99/100/101.
>
> Setze ohne zusätzliche Nutzer-Chat-Handoffs selbstständig interne Subtasks W0–W7 auf. Nutze soweit verfügbar mehrere lokale Subagenten, Code-Worker, Worktrees und Working-Chats **parallel**: W1 Backend/Quellgraph, W2 CAN/PyPSA-Kern, W3 wahrhaft unabhängiger VeraGrid-T-06-Parser, W7 Fixture/Test/CI; nach G1 W4 elektrische Sondermodelle und W5 Python-first Originalgraph-/CGMES-Update-Export parallel. Führe alles auf einem separaten Integrationsbranch zusammen, beauftrage W6 als von Implementierungsworkern getrennten unabhängigen E2E-/Numerik-/Semantik-Reviewer und schließe die qualifizierten Defekte kontrolliert.
>
> Beginne zwingend mit G0 Host/Native/FixtureSHA/Datenrechten/Security; beachte alle Stopregeln und normative CAN/2.0.0-/DNR/1.0.0-Verträge, die beiden strikt getrennten Update-Exportrouten und scoped Test-/Capability-Gates. Führe sämtliche zulässigen Tests tatsächlich aus; nie fiktive PASS-/READY-Claims.
>
> Liefere EINEN konsolidierten Abschluss mit exakten Git-Commits/Branches, Quellcode und Tests, unabhängigen T-06-/E2E-Prüfberichten, vollständiger REQ-/T-/Capability-Matrix, Belegen für Original- und Exporttreue, runtime-/datei-/rights-/securitygebundenen Einschränkungen und klarer scoped Releaseempfehlung. Keine Änderung an main, keine Modul-1-/PECD-/Hydro-/Zeitreihen-/Netzreduktionsarbeit, kein CREATE_FROM_PYPSA oder unfreigegebener Real-CGM-Großlauf.
>
> Kein weiterer allgemeiner Planungsdurchlauf. Beende den autorisierten Makroauftrag bestmöglich mit realen Artefakten oder genau benannten BLOCKED-Befunden. **Keine Behauptung automatischer lokaler Ausführung, wenn dir die erforderlichen Subagenten-/Laufzeittools tatsächlich nicht zur Verfügung stehen.**

## 9. Späterer optionaler Makroauftrag M0-MA-02

**Nicht Bestandteil von M0-MA-01 und nicht als Blocker für dessen Abnahme:** Vollständiger CGMES-Neuaufbau CREATE_FROM_PYPSA, lizenzierte europäische Groß-CGM-Skalierung und belastbare Realnetzbetriebs-/Performance-Benchmarks. Nur nach eigener konkreter Owner-Entscheidung, eigenem Rechte-/Daten-/Ressourcenprofil und eigener unabhängiger QA. Optional kann M0-MA-02 ebenfalls intern parallelisiert werden.

**Governance-Abschluss:** Mit M0-MA-01 ersetzen wir die vielen separaten Nutzer-Handoffs durch EINEN auf interne Worker heruntergebrochenen Makroauftrag. Unabhängige Prüfung bleibt harte Abnahmevoraussetzung statt eine optionale Chatfolge.
