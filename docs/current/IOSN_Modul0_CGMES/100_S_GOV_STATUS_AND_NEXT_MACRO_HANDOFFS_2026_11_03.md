# S-GOV-M0 — Gesamtstatus und konsolidierte Folge-Handoffs

**Datum:** 2026-11-03  
**Projekt:** IoSN / TYNDP / PyPSA — ausschließlich Modul 0 (CGMES zu PyPSA und CGMES-Rückexport)  
**Repository:** https://github.com/AlOussama/TYNDP_Products  
**Verbindlicher M4-0-Eingangscommit:** 8d3bdbf19656a66ba342b223d0ca30613e07a80c  
**Normativer Architektur-Freeze:** b1e284996fa69f81651daf9150b829e6a42e4ce3  
**Status dieses Dokuments:** Plan und kopierfähige Implementierungs-/Prüfaufträge; kein selbstständiger Runtime-RunRelease, keine Ausführung, kein main-Merge.

## 1. Scope und Dokumentenautorität

Modul 0: CGMES → Originalgraph-/Provenienzarchiv → CAN/2.0.0 (kanonische Daten) → detailliertes PyPSA-Netz (DNR/1.0.0). Als eigenständiger M0-Funktionszweig folgt der auf dem Originalgraphen beruhende Update-Export importierter CGMES-Modelle. CREATE_FROM_PYPSA (vollständige Neugenerierung eines CGMES-Modells aus einer PyPSA-Quelle) und Real-CGM-Performance sind gesondert zu entscheiden.

**Strikt ausgeschlossen:** PECD/PACD, Wetterjahre, Erzeugungs-/Lastzeitreihen, Hydro, räumliche Profile, Modul-1-Adapter, Netzreduktion/Clustering. Diese Arbeiten dürfen weder M0-Architektur noch die Validierung der M0-Netzdaten blockieren.

**Verbindliche Referenzen:**

- [50 – Test- und Exportvertrag](50_VALIDATION_CONTRACT.md)
- [70 – Requirements und PoC-Plan](70_IMPLEMENTATION_READINESS.md)
- [85 – Normative CAN/2.0.0-/DNR/1.0.0-Reparatur](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md) (hat Vorrang bei früheren M3-Konflikten)
- [90 – Dokumentarischer Architektur-Freeze](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md)
- [95 – M4-0 Toolchain/Source Witness](95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md)
- [96 – G0, Security, Rechte, RunRelease](96_M4_0_RUNRELEASE_POLICY_AND_GATES.md)
- [97 – Zwei bereits vollständige Cold-Start-Handoffs](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md)
- [99 – M4-0-Abschlussbericht](99_S_GOV_M4_0_FINAL_EXECUTION_REPORT.md)

**Python-first:** PyPowSyBl als Primärinterface zu PowSyBl; kein eigener Java-Service, keine eigene universelle RDF/XML-Engine. VeraGrid ausschließlich als unabhängige read-only zweite CGMES-Parsing-/T-06-Qualifikation (nicht zweites komplettes Produktionsbackend). Eine konkrete, reproduzierte fehlende Python-API-Funktion erfordert eine neue begrenzte Ownerentscheidung, bevor ein Sonderweg zulässig ist.

## 2. Iststand und fehlende Evidenz

| Stufe | Gegenstand | Tatsächlicher Status |
|---|---|---|
| M0/M1 | Backend-/Anforderungs-/Daten-/Testverträge | dokumentarisch abgeschlossen; 48 REQ (39 MUSS), T-01…T-24 spezifiziert |
| M2 | Softwarearchitektur/ADR | dokumentarisch abgeschlossen |
| M3 | unabhängiger Review | REPAIRS_REQUIRED, 0 P0, 7 P1, 4 P2; Originalurteil bleibt historisch gültig |
| M3-Reparatur | normativer CAN/2.0.0-/DNR/1.0.0-Freeze | 7 P1 dokumentarisch geschlossen; 4 P2 disponiert; ausschließlich Freeze für Implementierungsplanung |
| M4-0 | Toolchain, APIs, CGMES 2.4.15/3.0 Testquellen, Runtime-/Sicherheitsgates, Handoffs | M4_0_STATIC_PREFLIGHT_COMPLETE_WITH_NAMED_RUNRELEASE_HOLDS |
| Ausführbare M0-Capabilities | Runtime, SourceGraph, CGMES-Import, PyPSA-LF, unabhängiges T-06, Export, Recovery, Großnetz | NOT_EXECUTED/NOT_ASSESSED, keine READY-Aussage |

M4-0-Paketkandidaten: PyPSA 1.4.0, PyPowSyBl 1.16.1, VeraGridEngine 6.7.20; tatsächlich installierte transitive BOM und Native-Core-Version noch unbestätigt. CGMES-Testressourcen sind im Upstream katalogisiert, aber der Rechte-/Raw-SHA-256-/FullModel-/Boundary-Fidelity-Witness ist noch auszuführen.

## 3. Makrofolge, Verantwortlichkeiten und Abhängigkeiten

| ID | Makro | Zuständigkeit | Start |
|---|---|---|---|
| **M5A** | R-M0-POC1-IMPL-1: Import/Canonical/elementare PyPSA-Sicht/Publisher | Primärer Implementierungsworker; kann im **bestehenden Hauptchat** erfolgen | Jetzt nach expliziter Freigabe, G0 ist erster Teil |
| **M5B** | R-M0-T06-INDEPENDENT-1: wirklich unabhängiger read-only VeraGrid-Snapshot/Parität | **Separater unabhängiger Fachchat** | Parallel zu M5A, gleiche Originalfixture-Hashes |
| **M6** | S-GOV-M0-POC1-INTEGRATE: Abnahme und Schnittstellenfreeze nach beiden Rückläufern | S-GOV / bestehender Hauptchat | Nach M5A/M5B |
| **M7A** | R-M0-POC2-ELECTRICAL-1: 3W/PST/HVDC/Shunt/Limits/Multi-IGM/ACPF | Elektrotechnik-/PyPSA-Implementierungsworker | Nach M6; parallel zu M7B |
| **M7B** | R-M0-POC3-UPDATE-EXPORT-1: manueller IGM-SSH-/CGM-Quick-SSH+SV-Export | CGMES-/Originalgraph-/Exportworker | Nach M6; parallel zu M7A, getrenntes Branch |
| **M8** | R-M0-INDEPENDENT-E2E-1: komplette unabhängige M0-Capability-Qualifikation | Unabhängiger dritter Reviewer; S-GOV für Release | Nach M7A und M7B |
| **M9 optional** | R-M0-POC4-CREATE-OPS-1: CREATE_FROM_PYPSA und/oder lizenziertes Real-CGM-Performance-Gate | separater Owner-/Workerauftrag | Nur bei ausdrücklichem Scopebeschluss |

**Zielabgrenzung:** Für einen geprüften *CGMES→PyPSA*-Konverter werden M5A/M5B/M6/M7A und ein passender unabhängiger M8-Importscope benötigt. Für Update-Rückexport zusätzlich M7B/M8-Exportabnahme. CREATE_FROM_PYPSA und großskaliges Real-CGM sind keine impliziten Voraussetzungen des Import-PASS.

Jeder Worker arbeitet auf einem isolierten Branch, mit exakten Remote-SHAs. Nur die vom S-GOV nach M6 akzeptierte **unveränderliche Integrationsbasis** darf für M7A und M7B gemeinsam verwendet werden. Kein automatischer main-Merge. Unabhängige T-06- und Endreview-Rollen nicht mit dem primären Implementierungsworker zusammenlegen.

## 4. Copy-ready: M5A – primärer Kernpfad (sofort)

**Vollständiger Handoff:** [97 §2, Cold-Start-Handoff A](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md). Der bereits ausgearbeitete Vollauftrag hat Vorrang vor diesem Kurzstart.

> Du bist R-M0-POC1-IMPL-1. Verifiziere zuerst Remote-Commit 8d3bdbf19656a66ba342b223d0ca30613e07a80c und lies 10/20/30/40/50/60/70/80/85/90/95/96/97/98/99 vollständig. Ich beauftrage die **vollständige tatsächliche Ausführung** von 97 Abschnitt 2 auf dem dort bestimmten Implementierungsbranch, nicht die erneute Planung. Führe zuerst G0: Host, Runtime/Native-BOM, Quellenprofile, rechtmäßig nutzbare Fixtures und sichere ZIP-/XML-Verarbeitung. Implementiere SourceRaw-Archiv/Originalgraph, CAN/2.0.0 mit IDs/Occurrences/Origin/Revisionsräumen, PyPowSyBl-Python-Port, elementare Komponenten/Topologie/PyPSA, DNR/1.0.0, M0-PUBLISH/SQLite-CAS/Recovery, Tests/Negative-Cases und reproduzierbare Reports. CANONICAL_IMPORT_READY bleibt ohne unabhängiges T-06 gesperrt. Bei Blocker präzise beschränkte Teilergebnisse/BLOCKED; keine eigene RDF/XML-Engine, keine Java-App, kein main-Merge und kein Modul 1.

**Achtung:** Dieser Kurzstart wird erst durch das tatsächliche gesonderte Nutzerkommando zum Ausführungsauftrag.

## 5. Copy-ready: M5B – unabhängiger zweiter Parsingpfad (sofort, eigener Chat)

**Vollständiger Handoff:** [97 §3, Cold-Start-Handoff B](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md).

> Du bist R-M0-T06-INDEPENDENT-1. Verifiziere Remote-Commit 8d3bdbf19656a66ba342b223d0ca30613e07a80c und lies den vollständigen Auftrag aus Dokument 97 §3 sowie 50/70/85/95/96/98/99. Führe das komplette T-06-Makro auf eigenem Branch validation/iosn-m0-t06-independent-20261101 aus. Verarbeite die identischen originalgehashten rechtmäßig verfügbaren CGMES-Fixtures, aber **durch einen eigenständigen VeraGrid-Parserpfad** – keine PowSyBl-/PoC1-ParsedSources als vermeintlich unabhängige Daten. Liefere BackendSnapshot/SourceFacts, Herkunft, FKs/IDs/Terminal/Topology/Country, Unit- und Sign-Vergleiche, Negativfälle, per-Feld-Paritätsledger und gesicherte Testlogs. Solange der PoC1-Snapshot fehlt: WAITING_FOR_PRIMARY_SNAPSHOT, keine erfundene Parität. Keine produktive zweite Komplettimplementierung, kein Modul 1, kein main-Merge.

## 6. Copy-ready: M6 – S-GOV-Integrationsreview (nach beiden Rückläufern)

> **Auftrag S-GOV-M0-POC1-INTEGRATE.** Rolle: Governance-/Integrationsverantwortung; kein selbstständiger Neuimplementierungsauftrag. Basis AlOussama/TYNDP_Products, M4-0-Commit 8d3bdbf19656a66ba342b223d0ca30613e07a80c. Verifiziere zuerst die **exakten Remote-Abschlusscommits** von M5A und M5B. Lies 50/70/85/90/95/96/97/99/100 und die vollständigen beiden Execution-Reports samt Diffs, Testartefakten und Fixture-Manifesten.
>
> Führe in einem Makro die vollständige Source-/Version-/Host-/Rights-/CAN-/DNR-/Quality-/Persistence-/Security-Konformitätsprüfung und die **tatsächlich unabhängige** T-06-Parität durch: identische Originaldatei-SHA-256; Profile/FullModel/Authority; SourceModelSet, mRID/RDF-Subject/BlankNodes/Occurrences, Terminal-/Equipment-FKs, Country-/Substation-Herkunft, NODE_BREAKER/BUS_BRANCH/TP, SourceQuality, Units/Basen/Vorzeichen und tolerierte numerische Deltas. Jede Abweichung hat Feld- und Source-Referenz; keine Normalisierung, die Unterschiede unbewiesen wegfiltert.
>
> Kontrolliere Negativfixtures, M0-PUBLISH-Atomizität/Idempotenz/Recovery, Requirements REQ-001…048 und T-01…T-24 als **scopegebundene** PASS/FAIL/BLOCKED/NOT_EXECUTED-Matrix. Ein nicht ausgeführtes T-06 darf kein CANONICAL_IMPORT_READY ergeben. Erstelle **einen** konsolidierten Integrations-/Entscheidungsbericht mit exakten SHAs, berechtigten Fixtures, Diffs, Quality-/Loss-Matrix, technischen Blockern, Entscheidung SCOPED_PASS/CONDITIONAL/BLOCKED und – nur soweit zulässig – einem Integrationsbranch mit einer **konkreten unveränderlichen Start-SHA** für M7A/M7B. Kein main-Merge, keine Modul-1-Arbeiten, kein neuer allgemeiner Architekturreview.

## 7. Copy-ready: M7A – elektrische Projektion (nach M6; parallel zu M7B)

> **Auftrag R-M0-POC2-ELECTRICAL-1.** Rolle: unabhängiger ausführender PyPSA-/CGMES-Netzmodellierungsingenieur. Verifiziere zuerst den **genau von S-GOV-M6 freigegebenen Integrationscommit**, lies 30/40/50/60/70/85/90/95/96/97/99/100 und PoC1-/M6-Reports sowie bestehende Source-/Canonical-/PyPSA-API vollständig. Führe einen konsolidierten Implementierungs- und Elektrowitness auf einem **eigenen Branch von diesem Commit** durch.
>
> Implementiere die für das detaillierte Netz fehlenden Spezialfälle: Dreiwicklungstransformatoren samt qualifizierter Ersatz-/Kron-/Ybus-Abbildung; RatioTap/PhaseTap/PST mit Lage, Richtung und Limits; lineare/nichtlineare Shunts; Grenzwerte und Equipmentstatus; HVDC mit korrekten Insel-/Port-/Sign- und Verlustregeln; CGM-Multi-IGM/Boundary/SourceCountry; GL/CRS und Missing-/Derived-Provenienz. Behalte Original-mRID/RDF-/Terminal-/SourceHierarchy-/Revisionsreferenzen und CAN/2.0.0 bei. Bei fehlender PyPSA-Äquivalenz: explizite APPROX-/UNSUPPORTED- und Qualitäts-/Loss-Klassifizierung statt stillem Drop.
>
> Ergänze die DNR/1.0.0-Typen/Port-/Limit-Sidecars und das von Export **unabhängige** append-only projection_quality-/projection_witnesses-Ledger. Erzeuge reproduzierbare positive/negative F-03/F-04/F-05/F-06-Fixtures, soweit Datenfamilie, vollständige Originalprofile und Nutzungsrechte tatsächlich belegt sind. Verifiziere Ybus/Zweitor/Transformator-/Tap-Referenzen, KCL, Bases/Sign, AC-Islands/Slack, PyPSA ACPF und LPF, relevante T-03/T-07…T-20/T-23 mit **explizit normierten** elektrischen Toleranzen; dokumentiere Geräte und Varianten getrennt für CGMES 2.4.15/3.0.
>
> Liefere Code-/Test-Diff, exakten Remote-Commit, Fixture-SHA-256, Runner/Version/Host, Vollreport, Requirement-/Test-/Quality-/Loss-Witness und scoped Capability-PASS/BLOCKED. PYPSA_ACPF_READY ausschließlich im geprüften Bereich. Keine CGMES-Exportentwicklung, keine erneute Parserengine, kein Modul 1 oder Netzreduktion, kein main-Merge.

## 8. Copy-ready: M7B – graphbasierter Update-Export (nach M6; parallel zu M7A)

> **Auftrag R-M0-POC3-UPDATE-EXPORT-1.** Rolle: eigenständiger CGMES-/CIM-Export- und Provenienzingenieur. Verifiziere den **identischen von S-GOV M6 freigegebenen Integrationscommit** wie M7A, lies 40/50/60/70/85/90/95/96/97/99/100 sowie PoC1-SourceGraph-/Identity-/State-/M0-PUBLISH-Implementierung und ihre Nachweise vollständig. Arbeite in separatem Branch; keine Änderungen an M7A-Branch oder main.
>
> Implementiere UPDATE_IMPORTED mit Originalgraph als Autorität, attributgenauem Backmapping/Change-Ledger, vollständigen Original-IDs und ungemappten Tripeln, Revisions-/Betriebszustands- und Modellheader-/Authority-/FullModel-/DependsOn-/Supersedes-Semantik, Transaktions-/CAS-/Recovery-Policy. STATE_NON_TOPOLOGY ist eigens zu qualifizieren; STATE_TOPOLOGY_AFFECTING/STRUCTURAL_EQ_TP/SYNTHETIC_CREATE ohne expliziten belegten Vertrag BLOCKED.
>
> Qualifiziere **zwei streng getrennte Routen:** MANUAL_IGM_SSH (SSH-only je IGM, originalgetreue EQ/TP/Boundary-Referenzen) und CGM_QUICK_SSH_SV (SSH je IGM und **wirklich gelöstes** gemeinsames SV, ggf. qualifizierter TP-Pfad). Der Quick-Profilefilter liefert kein SSH-only. Prüfe **Python-first** get_sub_networks/get_sub_network, get_extensions('cgmesMetadataModels'), get_export_parameters('CGMES'), isolierte create_extensions-API-Proben sowie Network.save(..., format='CGMES'). Vorhandene importierte Header-/Metadata-Extension sicher mutieren/erhalten und unabhängig reimportieren **tatsächlich beweisen**, nicht aus Methodennamen erschließen. Ist das nicht möglich: BLOCK_EXPORT_UNPROVEN und präziser Negativbefund; keine selbstgebaute Java-App oder generischer XML-Patcher als Default.
>
> Für jede Route separater Bundle-/Source-/Originaldatei-/Output-SHA-256, semantischer RDF-Graph-Diff, zulässige Attributwhitelist, Profil-/Authority-/Dependency-/Versionscheck, unabhängiger Reimport, Idempotenz, Konflikt-/Crash-/Retry- und T-05/T-21/T-22/T-24-Negativtest. Veröffentliche exakten Remote-Commit, Code, Report und getrennte scoped UPDATE_EXPORT_READY-Entscheidungen je Route. CREATE_FROM_PYPSA, Modul 1 und Netzreduktion sind verboten; kein main-Merge.

## 9. Copy-ready: M8 – unabhängige integrierte Endabnahme (nach M7A/M7B)

> **Auftrag R-M0-INDEPENDENT-E2E-1.** Rolle: vom M5-/M7-Implementierer verschiedener unabhängiger System-/Numerik-/Datenreviewer. Nach Benennung des gemeinsamen S-GOV-Integrationscommits Remote-Baseline und alle M4-/M5-/M6-/M7-Abschlusscommits verifizieren, Diffs und sämtliche 10/30/40/50/60/70/85/90/95/96/97/99/100-Verträge sowie Ausführungsreports lesen. Kein Produktivcode-Merge.
>
> Führe **eigene** Testläufe und nachvollziehbare Gegenproben für die tatsächlich rechtmäßig vorhandenen CGMES-2.4.15-/3.0-Quellen aus: Rohprofile → unabhängige Originalgraph-Fakten → PyPowSyBl → CAN/2.0.0/SourceQuality → detaillierte PyPSA-DNR/1.0.0-Projektion mit Ybus/ACPF/LPF → jede unterstützte originalgraphbasierte CGMES-Update-Exportroute → RDF-Semantikdiff und unabhängigen Reimport. T-06 darf nur mit zwei wirklich unabhängig geparsten Original-Rohdatensätzen PASS heißen.
>
> Prüfe Source-/Country-/mRID-/RDF-/BlankNode-/TP-/Boundary-/Multi-IGM-Semantik, Sondergeräte, Units/Sign/Islands, ProjectionQuality/Loss, Header/Authority/Dependencies/SV und erzwungene negative Sicherheits-/CAS-/Crash-/Konfliktfälle. Erzeuge REQ-001…048 und T-01…24 pro Familie/Fixture/Capability als PASS/FAIL/BLOCKED/NOT_EXECUTED, mit konkreten Artefakten. Ungeprüfte Real-CGMs, nicht vorhandene Datenrechte oder isolierte PyPowSyBl-/Native-Funktionen lassen sich nicht durch synthetischen Erfolg ersetzen.
>
> Gib **getrennte** Empfehlungen für CANONICAL_IMPORT_READY, PYPSA_ACPF_READY, UPDATE_EXPORT_READY_MANUAL_IGM_SSH, UPDATE_EXPORT_READY_CGM_QUICK_SSH_SV, CREATE_EXPORT_READY und PERFORMANCE_QUALIFIED; auch nach PASS keine pauschale IEC-/ENTSO-E-Konformitätszertifizierung. Liefere unabhängigen Reviewbericht, Fehlerledger, Hash-/Commit-/Runtime-Matrix, reproduzierbare Gegenproben und Empfehlung an S-GOV. S-GOV trifft finalen Merge-/Releaseentscheid; keine M1/PECD/Reduktionsaufgaben.

## 10. Optionaler Scope M9 und Schlussentscheidung

Nur bei expliziter Ownerentscheidung: CREATE_FROM_PYPSA als vollständig eigenständiger Exportmodus mit selbst generiertem CIM-Quellgraph/Original-mRID-/FullModel-/Authority-/Dependency-/Loss-Vertrag und neuem Test-/Roundtrip-Gate. Für reales großes europäisches CGM sind separate Nutzungsrechte, konkrete Datenbytes/SHA-256, lizenzierte Multiarea-Testbasis sowie ein neu begrenztes Ressourcen-/Benchmark-Profil erforderlich. Synthetische Testnetze ersetzen keinen REAL-CGM-/PERFORMANCE-PASS.

**Unmittelbarer nächster Schritt:** Nutzer autorisiert M5A und M5B separat. M5A kann im jetzigen Hauptchat implementiert werden; M5B wegen T-06-Unabhängigkeit in einem neuen Fachchat. M6 erfolgt sinnvollerweise wieder im Hauptchat. Es besteht kein Bedarf für eine weitere breite M0-Architektur- oder Backend-Recherchekampagne vor diesen Implementierungswitnesses.
