# IoSN Modul 0 – CGMES ↔ kanonische Netztabellen ↔ PyPSA

**Stand: 2026-11-01.** Die fachlichen Berichte und die **dokumentarische M2-Architektur-Synthese** sind vorhanden. **M3 am 01.11.2026 unabhängig statisch abgeschlossen: REPAIRS_REQUIRED (P0=0, P1=7, P2=4). Ein konsolidierter dokumentarischer M2-Reparaturvertrag (85) behandelt alle P1 und disponiert P2; S-GOV hat den **dokumentarischen Architektur-Freeze für Implementierungsplanung** in 90 ausgesprochen. Keine produktive Implementierung, keine Netzsimulation, kein CGMES-/PyPSA-/Export-Test, keine externe Konformitätszertifizierung.** **M4-0 ist als konsolidierter statischer Toolchain-/Quell-/RunRelease-Preflight abgeschlossen.** Der spätere Runtime-/Implementierungs-RunRelease bleibt bei den in 96 benannten G0-Host-/Datenrechte-/Sicherheitsgates gesperrt. Die Änderungen des M4-0-Branches betreffen ausschließlich Dokumentation und Preflight-Metadaten.

## Autorität und Dokumentenindex

| Datei | Status | Gegenstand |
|---|---|---|
| [00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md](00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md) | S-GOV-Fachkonsolidierung | Ursprungsbelege, K-01…K-07, Governance |
| [10_REQUIREMENTS.md](10_REQUIREMENTS.md) | unveränderter Fachrücklauf | REQ-001…REQ-048 und REQ-X01…X08 |
| [20_BACKEND_ASSESSMENT.md](20_BACKEND_ASSESSMENT.md) | unveränderter Fachrücklauf | PowSyBl/PyPowSyBl, VeraGrid, CIMpy, SOPTIM usw. |
| [30_CANONICAL_DATA_CONTRACT.md](30_CANONICAL_DATA_CONTRACT.md) | unveränderter Fachrücklauf | logische Tabellen, elektrische Transformationsgrundlagen |
| [40_SOFTWARE_ARCHITECTURE.md](40_SOFTWARE_ARCHITECTURE.md) | **M2-Entwurf** | sieben Verantwortungspakete, BackendPort, Datenfluss, Identity, Import/Export, Persistenz |
| [50_VALIDATION_CONTRACT.md](50_VALIDATION_CONTRACT.md) | unveränderter Fachrücklauf | T-01…T-24, Capabilities, Verlustvertrag |
| [60_ARCHITECTURE_DECISION.md](60_ARCHITECTURE_DECISION.md) | **M2-Entscheidungen** | ADR-001…009; K-01…K-07 explizit aufgelöst |
| [70_IMPLEMENTATION_READINESS.md](70_IMPLEMENTATION_READINESS.md) | **M2-Planung, M3-korrigiert** | 48 REQ-Mappings, 39 MUSS, 24 Tests, unabhängiges T-06, PoC-/Capability-Gates |
| [80_INDEPENDENT_ARCHITECTURE_REVIEW.md](80_INDEPENDENT_ARCHITECTURE_REVIEW.md) | **unveränderter M3-Review** | sieben P1-Freeze-Blocker, vier P2 und REPAIRS_REQUIRED |
| [85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md) | **normativer Reparaturvertrag CAN/2.0.0** | präzise PK/FK, beide Topologieformen, projektionseigenes QualityLedger, Quick-vs-SSH-Export, T-06, SQLite-FS-Commit/Recovery, typisiertes DNR/1.0.0 |
| [90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md](90_S_GOV_M3_REPAIR_CLOSURE_AND_FREEZE.md) | **S-GOV Abschluss** | sieben P1 dokumentarisch geschlossen; P2 disponiert; ARCHITECTURE_FROZEN_FOR_IMPLEMENTATION_PLANNING, alle QUAL-* NOT_ASSESSED |
| [95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md](95_M4_0_TOOLCHAIN_AND_SOURCE_WITNESS.md) | **M4-0 Upstream/API-/Datenwitness** | fest identifizierte CGMES 2.4.15/3.0-Dateien, Paketkandidaten und nachgewiesene PyPowSyBl-Subnetz-/CGMES-Metadaten-Python-API |
| [96_M4_0_RUNRELEASE_POLICY_AND_GATES.md](96_M4_0_RUNRELEASE_POLICY_AND_GATES.md) | **M4-0 Ausführungsrichtlinie** | G0-Prüfbedingungen, kleine Security/RAM/CPU/ZIP/XML-Budgets, Runtime-/Lizenz-/Recovery-Stopregeln |
| [97_M4_0_NEXT_MACRO_ASSIGNMENTS.md](97_M4_0_NEXT_MACRO_ASSIGNMENTS.md) | **Folgeaufträge / zwei Handoffs** | PoC-M1-Primärworker und unabhängiger T-06-Read-Only-Worker; spätere PoC-M2/M3-Trennung |
| [98_M4_0_PREPARED_EXECUTION_CONTRACT.json](98_M4_0_PREPARED_EXECUTION_CONTRACT.json) | **maschinenlesbare Preflight-Evidenz** | Softwarekandidaten, Paket-/Quellanker, initiale Schutzbudgets und API-/RunRelease-Holds |
| [99_S_GOV_M4_0_FINAL_EXECUTION_REPORT.md](99_S_GOV_M4_0_FINAL_EXECUTION_REPORT.md) | **M4-0-Abschluss und Handoff** | verifizierte statische Fakten, Python-first PowSyBl, offene Runtime-/Datenrechte-Gates und zwei vorbereitete Folgeaufträge |

**Auslegungspriorität:** Der Original-REQ- und T-Katalog bleibt maßgeblich. **CAN/2.0.0 aus [85](85_M2_M3_NORMATIVE_REPAIR_CONTRACT.md) hat bei den sieben identifizierten M3-P1-Konflikten Vorrang** gegenüber dem früheren 30/1.0.0-Tabellenregister und unpräzisierten M2-Passagen in 40/60/70. Für sonstige K-01…K-07-Konflikte gelten ADR [60](60_ARCHITECTURE_DECISION.md) und die Schnittstellen [40](40_SOFTWARE_ARCHITECTURE.md)/[70](70_IMPLEMENTATION_READINESS.md). Die historischen Arbeiterdokumente wurden nicht umgeschrieben.

## Herkunft / feste Commit-Evidenz

- Basis des Projekts: `main` an `1595d6d38e77804760612621657721b3699d2fea`.
- Backend-Fachbericht: `d3ab97e170eb6eeb5064dc3058b497f5c954af58`.
- Requirements/Canonical/Validation: `f2705338e3d79e12a46ae44a8d7a008a81c04b3b`.
- S-GOV-Pre-M2-Freeze: `e595335d511af6f8c9c05c88276553363ed37045`.
- M2-Architekturcommit: `0275f48231a0794bea324b9cab34700bb0de8f5b`.
- M3-Reviewcommit: `ea62050a867c27036552af28d3e0102a8689f4ec`.
- Konsolidierter Korrektur-Branch: `research/iosn-m0-cgmes-m2-m3-repair-20261101`; exakter HEAD im abschließenden S-GOV-Bericht.

## Nächste Governance-Schritte

1. **M3 abgeschlossen:** Der unabhängige Bericht bleibt unverändert und trägt die historische Entscheidung REPAIRS_REQUIRED.
2. **Eine M2-Korrekturrunde durchgeführt:** Normative Reparaturen M3-P1-01…07 und P2-Dispositionen sind in 85 festgelegt und in 40/60/70 eingeordnet; 39 MUSS und T-01…T-24 bleiben unverändert.
3. **S-GOV-Freezeentscheidung ausgesprochen:** ausschließlich dokumentarischer Freeze gemäß 90 nach Hash-/Traceability-/Konsistenzprüfung des korrigierten Branches. Kein Runtime-/Software-Release und kein neuer unabhängiger M3-Bericht.
4. **M4-0 statisch abgeschlossen:** 95/96/98 fixieren echte Software- und CGMES-Quellenbelege, **Python-first** PowSyBl-API, Grenzen der CGMES-Metadaten-/SSH-only-Exportqualifikation, G0-Gates und Ressourcenbudgets. Es fanden keine Runtime-Imports/Exports statt.
5. **Zwei ausführbare Folgeaufträge vorbereitet:** PoC-M1-Implementierung und unabhängige T-06-Quelle auf getrennten Branches, erst nach gesonderter Ownerfreigabe; PoC-M2/M3 später parallel nach Source-/Canonical-Basis. CREATE/F08/M1-E2E getrennt.

**Wichtige Nichtgleichheiten:** Python-API im Upstream nachgewiesen ≠ erfolgreicher SSH-only-CGM-Roundtrip; M4-0 Quellen/Release verifiziert ≠ erfolgreiche Host-/Datensatzrechte-/Runtimeprüfung; Architektur dokumentiert ≠ CGMES-konform; PYPSA_ACPF_READY ≠ REDUCTION_ADAPTER_READY; UPDATE_IMPORTED ≠ CREATE_FROM_PYPSA; QUICK_CGM_SSH_SV ≠ SSH-only; CANONICAL_IMPORT_PROVISIONAL ≠ CANONICAL_IMPORT_READY; M2-Fachentscheidung ≠ ausgeführtes QUAL-PASS.


## Aktualisierung 2026-11-03 — Ein koordinierter Gesamtmakroauftrag (M0-MA-01)

**Neuer ausführbarer Orchestrierungsauftrag:** [101_M0_MA01_PARALLEL_ORCHESTRATED_IMPLEMENTATION_AND_REVIEW_2026_11_03.md](101_M0_MA01_PARALLEL_ORCHESTRATED_IMPLEMENTATION_AND_REVIEW_2026_11_03.md).

Der User-facing-Ablauf M5A/M5B/M6/M7A/M7B/M8 aus Dokument 100 wird nun **durch einen einzigen ausdrücklich zu startenden Gesamtauftrag M0-MA-01 ersetzt**. Die Fachinhalte und Test-/RunRelease-Verträge von Dokument 97/100 bleiben als Referenz bestehen, ihre gesonderten Chat-Freigaben sind für den neuen Orchestrierungsmodus nicht erforderlich. Der Hauptworker darf separate lokale Worktrees/Subagenten/Chats parallel einsetzen; echte unabhängige T-06-Parität und ein von den Implementierern getrenntes E2E-Review bleiben Pflicht. Der ursprüngliche dokumentarische Architektur-Freeze (85/90) und G0-Gates (96) bleiben unverändert. Keine Modul-1-/PECD-Arbeit, keine Änderung an main, keine automatische Start-/READY-Freigabe durch die Erstellung des Handoffs.
