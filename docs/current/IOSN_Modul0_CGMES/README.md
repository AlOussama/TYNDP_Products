# IoSN Modul 0 – CGMES ↔ kanonische Netztabellen ↔ PyPSA

**Stand: 2026-11-01.** Die fachlichen Berichte und die **dokumentarische M2-Architektur-Synthese** sind vorhanden. **M3 unabhängig statisch zu prüfen; keine produktive Implementierung, keine Netzsimulation, kein CGMES-/PyPSA-/Export-Test, keine externe Konformitätszertifizierung.** Die Änderungen dieses M2-Branches betreffen ausschließlich Dokumentation.

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
| [70_IMPLEMENTATION_READINESS.md](70_IMPLEMENTATION_READINESS.md) | **M2-Planung** | 48 REQ-Mappings, 24 Testrollen, PoC-Makros, späteres Qualitätsgate |

**Auslegungspriorität:** Der Original-REQ- und T-Katalog bleibt maßgeblich. Bei ausdrücklich dokumentierten K-01…K-07-Kollisionen präzisieren die ADR in [60](60_ARCHITECTURE_DECISION.md) sowie die Schnittstellen in [40](40_SOFTWARE_ARCHITECTURE.md) und [70](70_IMPLEMENTATION_READINESS.md) die Anwendung. Die historischen Arbeiterdokumente wurden nicht umgeschrieben.

## Herkunft / feste Commit-Evidenz

- Basis des Projekts: `main` an `1595d6d38e77804760612621657721b3699d2fea`.
- Backend-Fachbericht: `d3ab97e170eb6eeb5064dc3058b497f5c954af58`.
- Requirements/Canonical/Validation: `f2705338e3d79e12a46ae44a8d7a008a81c04b3b`.
- S-GOV-Pre-M2-Freeze: `e595335d511af6f8c9c05c88276553363ed37045`.
- M2-Branch: `research/iosn-m0-cgmes-m2-architecture-20261031`; finaler HEAD wird im S-GOV-Abschlussbericht verifiziert.

## Nächste Governance-Schritte

1. **M3:** Ein unabhängiger statischer Architektur-Reviewer liest diesen Dokumentationsstand nach immutable Commit, prüft K-01…K-07 und REQ→Owner→T; veröffentlicht einen konsolidierten Bericht. M3 führt keine Netz-/Python-Tests und keine produktive Implementierung aus.
2. **Architektur-Freeze:** S-GOV/Owner nach M3, ggf. mit einer konsolidierten Reparaturrunde für belastbare P0/P1-Findings.
3. **PoC-Makros:** erst nach gesonderter Ownerfreigabe. PowSyBl-Import/Canonical, Sondergeräte, Update-Export und Create-Export in separaten Capability-Stufen.

**Wichtige Nichtgleichheiten:** Architektur dokumentiert ≠ CGMES-konform; PYPSA_ACPF_READY ≠ REDUCTION_ADAPTER_READY; UPDATE_IMPORTED ≠ CREATE_FROM_PYPSA; M2-Fachentscheidung ≠ ausgeführtes QUAL-PASS.
