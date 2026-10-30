# IoSN Modul 0 – CGMES ↔ kanonische Netztabellen ↔ PyPSA

**Stand 2026-10-30:** fachliche Architekturvorbereitung, weder implementiert noch numerisch getestet.

## Konsolidierter Ausgangsstand

- [00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md](00_S_GOV_CONSOLIDATION_AND_MACRO_PLAN.md) — S-GOV-Synthese zweier unabhängiger Fachrückläufer, Konfliktregeln K-01–K-07, Makros M2–M4.
- [10_REQUIREMENTS.md](10_REQUIREMENTS.md) — Anforderungen REQ-001 bis REQ-048 und REQ-X01 bis REQ-X08.
- [20_BACKEND_ASSESSMENT.md](20_BACKEND_ASSESSMENT.md) — Backendbewertung, PowSyBl-Primärpfad, VeraGrid-Fallback.
- [30_CANONICAL_DATA_CONTRACT.md](30_CANONICAL_DATA_CONTRACT.md) — logischer Tabellenvertrag, Provenienz und mathematische Projektion.
- [50_VALIDATION_CONTRACT.md](50_VALIDATION_CONTRACT.md) — T-01 bis T-24, Capabilities und beide Exportmodi.

## Unveränderte wissenschaftliche Ausgangsbelege

- Backendbericht ursprünglich an Commit d3ab97e170eb6eeb5064dc3058b497f5c954af58, Branch research/iosn-m0-cgmes-backend-20261030.
- Requirements/Canonical/Validation ursprünglich an Commit f2705338e3d79e12a46ae44a8d7a008a81c04b3b, Branch research/iosn-m0-cgmes-contracts-20261030.
- Beide entstanden auf Basis von main 1595d6d38e77804760612621657721b3699d2fea. Die hier übernommenen Fachberichte sind inhaltlich unverändert.

## Nächster Schritt

Im S-GOV-Chat M2 als ein großes Dokumentationsmakro durchführen: 40_SOFTWARE_ARCHITECTURE.md, 60_ARCHITECTURE_DECISION.md, 70_IMPLEMENTATION_READINESS.md. Danach genau ein unabhängiger statischer Architektur-Review M3. PoC M4 nur nach separater Freigabe. Kein Merge nach main.
