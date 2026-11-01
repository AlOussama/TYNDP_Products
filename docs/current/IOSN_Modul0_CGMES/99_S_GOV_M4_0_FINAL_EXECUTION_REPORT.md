# S-GOV-M0 — M4-0: konsolidierter Abschluss- und Ausführungshandoff

**Projekt:** IoSN / TYNDP / PyPSA, Modul 0 CGMES ↔ Canonical ↔ PyPSA  
**Ausführungsdatum:** 2026-11-01  
**Auftrag:** M4-0 Toolchain, Data Source Inventory, Preflight/RunRelease-Gates und Handoffs für die nächsten konsolidierten Implementierungsmakros  
**Git-Authority:** Basis-Commit `b1e284996fa69f81651daf9150b829e6a42e4ce3`  
**Branch:** `research/iosn-m0-cgmes-m4-0-preflight-20261101`  
**Endentscheidung:** `M4_0_STATIC_PREFLIGHT_COMPLETE_WITH_NAMED_RUNRELEASE_HOLDS`  
**Kein** Produktivcode, kein Merge, keine ausgeführten Import-/Export-/PyPSA-/Native-/T-06-/Lastfluss-/Recoverytests.

## A. Vollständige M4-0-Dokumentenlieferung

| Dokument | Implementierungs-/Governancefunktion |
|---|---|
| [95 — Toolchain/Quellenwitness](95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md) | tatsächliche Upstream-Datei-/Gitblob-Verifikation für 2.4.15 und 3.0; Release-/Wheel-Kandidaten, konkrete PyPowSyBl-APIs und ihre Evidenzgrenzen |
| [96 — RunRelease und Security](96_M4_0_RUNRELEASE_POLICY_AND_GATES.md) | G0-BOM/API/Dataset/Rights/Safety/Publish/QUAL, versionierte quantitative kleine Security- und Ressourcenbudgets, Stop-/Recovery-Regeln |
| [97 — nächste Makroaufträge](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md) | komplette Cold-Start-Handoffs für PoC-M1 und unabhängigen T-06-Witness, Branch- und Akzeptanz-/Parallelisierungsregeln |
| [98 — Machine-readable Preflight](98_M4_0_PREPARED_EXECUTION_CONTRACT.json) | strukturierte Kandidaten-Paket-/Ressourcenhashes, Originalquellen, Grenzen, Python-API-Belege, Worker- und RunRelease-Holds |
| [README](README.md) | konsolidierter Dokumentenindex und Governance-Vorrang |

Historische Originalberichte `00/10/20/30/50/80` sowie eingefrorene Architektur `40/60/70/85/90` werden nicht modifiziert. Die normative CAN/2.0.0-/DNR/1.0.0-Spezifikation bleibt im Freeze gültig.

## B. Ausgeführte Verifikationen (statisch, keine Laufzeit)

1. Der S-GOV-Freeze-Basiscommit ist über den GitHub-Connector verifiziert; der Projekt-Buildvertrag gibt Python >=3.11, `pypsa>=1.4,<2` optional und einen separaten eingeschränkten Modul-1-PyPSA-Adapter vor.
2. Konkrete Pakete und Distributionskandidaten sind verzeichnet: `pypsa==1.4.0`, `pypowsybl==1.16.1` und `VeraGridEngine==6.7.20`. Diese Pins sind **Kandidaten**; die transitive BOM, native Core-Version und Host-Installation wurden nicht ausgeführt.
3. Am unveränderlichen `powsybl/powsybl-core@f6749ad368fba8dd3776099c040fed07023a1ba3` wurden tatsächlich einzelne Original-RDF/XML-Beispieldateien für CGMES 2.4.15 und CGMES 3.0 nachgewiesen: EQ, SSH, TP, SV, GL, Boundary und Multi-IGM-Assembly-Ressourcen. Die Gitblob-SHAs sind keine Byte-SHA-256 und ersetzen keine Rechte-/Datasetprüfung.
4. **Wichtige Python-API-Präzisierung:** PyPowSyBl ist der primäre **Python-basierte Zugriff** auf die Java-basierten PowSyBl-Funktionen. Am Tag `v1.16.1` sind u. a. `Network.get_sub_networks`, `get_sub_network`, `save`, `update_from_file`, `pypowsybl.network.get_export_parameters('CGMES')` sowie `get_extensions/create_extensions('cgmesMetadataModels')` statisch belegt, einschließlich Profilsatz, Authority, DependsOn und Supersedes in DataFrame-Adaptern. Damit ist eine **eigene Java-Serviceentwicklung nicht erforderlich und nicht beauftragt**. Noch nicht bewiesen ist die sichere Python-seitige Mutation bereits importierter CGMES-Header und der voll gültige manuelle SSH-only-CGM-Reimport.
5. Für kleine F-01…F-07-Fixtures wurden restriktive, nicht als Benchmarkergebnisse auszugebende Schutzbudgets und eine prüfbare Stop-/Recovery-Policy beschlossen. Für F-08 (lizenziertes reales Groß-CGM) ist keine pauschale Startfreigabe erteilt.

## C. Fünf harte RunRelease-Vorbehalte

| Gate | Momentaner Status | Präzise spätere Erledigung |
|---|---|---|
| Laufzeit/Native | `NOT_ASSESSED` | Host-CPython/OS/ABI und native Bundle-/Paketversions-Messung, reproduzierbare Lockdatei und SHA-256 |
| Dataset/Usage rights | `RIGHTS_UNVERIFIED` | tatsächliche Quellprofile/Dateibytes SHA-256, vollständige Lizenz-/Nutzungs-/Weitergabeberechtigung, ausdrücklich kein ungeklärtes Real-CGM im öffentlichen Repo |
| Exakte Source-/Country-/TP-/ID-Fidelity | `NOT_EXECUTED` | vollständiger ursprünglicher RDF-/FullModel-/Authority-Graph, NODE_BREAKER/BUS_BRANCH, SourceHierarchy, Failure-Fixtures |
| T-06 / unabhängiger zweiter Parser | `NOT_EXECUTED` | derselbe originalgehashte Datensatz unabhängig über VeraGrid gelesen; objekt-/attributgenaue Parität mit PowSyBl, sonst CANONICAL_IMPORT_PROVISIONAL |
| Export-/Publikationsgates | `NOT_EXECUTED` | API-/Header-/Graph- und Reimport-Witness sowie Blob-/SQLite-CAS-/Crash-/Recoverytests; Quick-CGM-SV nicht mit SSH-only verwechseln |

## D. Unmittelbar vorbereitete Aufträge

**1. PoC-M1, primärer Import/Canonical/PyPSA-Worker:** `R-M0-POC1-IMPL-1`, Branch `implementation/iosn-m0-poc-m1-core-20261101`. Umfasst geprüfte Runtime/Fixtures, SourceGraph-Provenienz, CAN/2.0.0, Original/State/Projection-Revisionsräume, beide Topologiearten, SQLite CAS, einfache Geräte/PyPSA und DNR/1.0.0. Ohne T-06 nur PROVISIONAL.

**2. Unabhängiger T-06-Worker:** `R-M0-T06-INDEPENDENT-1`, Branch `validation/iosn-m0-t06-independent-20261101`. Erstellt mit VeraGrid einen **wirklich eigenständig** geparsten read-only Source/BackendSnapshot samt detaillierter Paritäts-/Abweichungsevidenz auf identischen Originaldatei-SHA-256.

Beide sind als **einzelne große, separat vom Nutzer zu autorisierende** Implementierungs-/Qualifikationsaufträge vollständig in [97](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md) beschrieben und können nach ihrer jeweiligen Freigabe parallel laufen. Ein vorzeitiges Starten wurde durch die Erstellung des Handoffs nicht ausgelöst.

**3. Anschließend:** Ein konsolidierter S-GOV-Rücklauf auf exakten Remote-Commits. Nach stabiler PoC-M1-Schnittstelle können **PoC-M2 elektrische Sondergeräte** und **PoC-M3 originalgraphbasierter CGMES-Update-Export** parallel auf getrennten Branches beginnen. PoC-M3 verwendet ausdrücklich zuerst die offiziell belegte PyPowSyBl-Python-/Extension-/Subnetwork-API für `MANUAL_IGM_SSH`; Java-Eigencode ist keine Defaultlösung. CREATE_FROM_PYPSA, große reale CGMs und Änderung des Modul-1-Adapters werden separat entschieden.

## E. Schlussentscheidung

**M4-0 als dokumentarisches und quellenorientiertes Vorbereitungsmakro abgeschlossen:** `M4_0_STATIC_PREFLIGHT_COMPLETE_WITH_NAMED_RUNRELEASE_HOLDS`. Der Architektur-Freeze bleibt unverändert; keine neuen Anforderungen, keine zusätzlichen Mikroreviews, kein produktiver Commit.

**Nicht freigegeben:** `CANONICAL_IMPORT_READY`, `PYPSA_ACPF_READY`, `UPDATE_EXPORT_READY`, `CREATE_EXPORT_READY`, `REDUCTION_ADAPTER_READY`, `PERFORMANCE_QUALIFIED` sowie jede ENTSO-E-/IEC-Konformitätsbehauptung.
