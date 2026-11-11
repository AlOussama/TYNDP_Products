# M2-API-G1 — Owner Contract Gate & Minimal Interface Reconciliation

**Projekt:** AlOussama/TYNDP_Products. **Rolle:** S-GOV-M2 + Lead Scientific Software Architect. **Modus:** jetzt READ-ONLY/Document-and-contract-only; keine automatische Implementierung, kein Merge, kein MA2-Go.

## 1. Verbindliche Quellen

- [S-GOV-Konsolidierung 93](93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md)
- [R-API vollständiger Review, SHA 075c509...](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md)
- [A PR #13 / SHA 70e92...](https://github.com/AlOussama/TYNDP_Products/pull/13)
- [B alternative Linie SHA 88374dd...](https://github.com/AlOussama/TYNDP_Products/tree/88374dd38792146ca55fa3fe2d4b35dac842c0b9/src/tyndp_reduce/m2)
- [MA2 Handoff 85](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md)
- [R-PHY und R-CLU Findings](93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md)

## 2. Auftrag

Unterscheide die drei tatsächlich geprüften Optionen:
- **A:** `tyndp_reduce.iosn_official` ist allein kanonisch, keine B-Integration;
- **B:** `tyndp_reduce.m2` wird allein kanonisch (hohe Migration des Dokument-85-Vertrages nötig);
- **C — Empfehlung:** `iosn_official` ist die **einzige** kanonische API, B bleibt als unabhängiger Parity-Oracle und liefert ggf. **optionale einseitige, geprüfte B→A-Adapter**.

**Kein automatischer Owner-Beschluss:** Stelle Project Owner das konkrete Entscheidungsregister und notwendige Zustimmung bereit. Das technisch empfohlene C ist bis zur ausdrücklichen Bestätigung `PROPOSED`, kein `FROZEN`.

Erstelle ein exact typed v1-Contract-Schema für `DetailedGridSnapshot`, `ReferenceDispatchSet`, `TimeSet`, `NormalContingencyRatings`, `CountryZoneBudget`, `ReferenceFlowCache`, `MA1Result`, `OrientedProjection`, 15 Artefakte + SHA und `execute_ma1`. Dokumentiere Versionierungs- und Breaking-Change-Policy; Reconciliation gegen MA2-Eingang G05–G08.

Kontrolliere R-API P1-01..09 **separat** von echten R-PHY/CLU-P1-Findings: 380→400 Klassifizierung, strenge UTC/Zeitachsen, HVDC verlustlos vs. asymmetrisch, fixe Trafo-PST-Phase, beobachteter Real-AC-Flow als separate Referenz, differente Cluster-Heuristik und fairer gleicher Monitor-RMSE, Protection-Policy im Seed, europaweites RAM/IO-Budget, Tap-Provenienz. Verwechsle 11/11 Parity-Test-PASS nicht mit semantischer Gleichheit.

Bei Owner-Option C: nur die **Design-Spezifikation** des B→A-Konverters mit erlaubten Fällen `lossless p0=-p1`, `tap=1`, explizite Phase, Country-NI/UK und UTC-Versionierung erstellen; unrepräsentierbare Fälle `UNSUPPORTED_SEMANTICS` fail-closed. Einzelne B-Features (Content-Hash, Write-once, Faktor-Reuse) mit dokumentierten Kosten/Nutzen nennen, **nicht** ohne Abnahme produktiv importieren. Der optionale Adapter darf MA2-Pfad nicht unnötig blockieren.

Verlange vor jeder MA2-Implementierung: Ownerwahl A/B/C dokumentiert, kanonische Quota-/Screening-/Protection- und Neutral-Dispatch-Verträge, P1-Reparaturstatus und Re-Review-Ledger. Autoritative ENTSO-E-Methode und reale Daten bleiben unabhängig davon blockiert.

## 3. Liefergegenstände / Gate

- `api_owner_options_and_recommendation.md` und ein Owner-Entscheidungstemplate, Status PENDING;
- `api_v1_contract.md`, `api_compatibility_matrix.csv`, `optional_b_adapter_design.md`, `ma2_input_gate.json`;
- links zu originalen Testergebnissen, konkrete Source-SHAs/Branch; Dokumentationsbranch (nicht main).
- Abschlussstatus: `RECOMMEND_C_OWNER_PENDING` / `OWNER_ACCEPTED_A/B/C` (nur bei explizitem Owner-Zitat) / `CONTRACT_BLOCKED`.

**Weder Projekt-Owner-Zustimmung noch Review-Freigabe simulieren.** Kein produktiver B→A-Import, kein Merge, kein MA2-Runtime-Go. M0/M1/Wetterjahrauswahl unverändert.
