# M2-MA1-RR1 — Two Independent Re-Reviews & Synthetic Gate Reconciliation

**Projekt:** AlOussama/TYNDP_Products. **Trigger:** **erst wenn** M2-MA1-RP1 einen neuen integrierten Repair-Commit und Testergebnisse veröffentlicht hat. **Nicht jetzt blind gegen den alten 0254-Code erneut prüfen.**

## 0. Verbindlicher Eingang

- [S-GOV-Review 93](93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md).
- [RP1 Worker-/Integration-Handoff 94](94_M2_MA1_RP1_CONSOLIDATED_REPAIR_MACRO_20261111.md).
- [R-PHY unabhängige Vorlage](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md), Tests `test_r_phy_independent_20261111.py` und [CI 43077807614](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077807614).
- [R-CLU unabhängige Vorlage](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md), Tests `test_r_clu_independent_frozen.py` und [CI 43078445311](https://github.com/AlOussama/TYNDP_Products/actions/runs/43078445311).

**Eingangsgate:** Integrator übergibt in einer einzigen SHA: gefixte `iosn_official`-Implementierung, P1/P2-Repair-Matrix, alle alten/neuen Tests und neue Output-SHA/Fixture. Ohne genau diesen SHA `NOT_READY_FOR_REVIEW`.

## 1. R-PHY-RE (separater Reviewer, nicht W-PHY und nicht W-INT)

Den Repair-Commit unabhängig auschecken, alle **vier** originalen P1-Proben mit den ursprünglichen Angriffsdaten reproduzieren und nun normales tatsächliches PASS bestätigen:
- PHY-R01: Callerlist-Mutation verschiebt weder Netztopologie noch Fingerprint;
- PHY-R02: falsches `lossless`-Flag wird hart abgewiesen;
- PHY-R03: falsches `in_service` und verwandte Flags werden hart abgewiesen;
- PHY-R04: `nan`/`inf`/huge tolerances und 1-MW-Island-Unbalance werden hart abgewiesen.

Die **Originalreviewtests unverändert** als historische Defektzeugen behalten. Strict-XFAIL→XPASS bedeutet auf der alten Testsuite **rot**, obwohl der Defekt repariert ist; der **Reviewer** erstellt im neuen Review-Branch eine nachweisbare Korrektur der XFAIL-Markierung zu gewöhnlichen Assertions, ohne die Attack Cases zu entschärfen. Unabhängig: 10-Bus/3-Island/2-HVDC/2-PST Cycle-Oracle, 1001-Bus Sparse-Fixture, Bilanz-KCL/KVL, Hash-/Zeitsynchronität und 15 Artefakte neu ausführen. Befunde P0/P1/P2 und genaue SHA/CI-Jobs/Logs.

## 2. R-CLU-RE (anderer Reviewer, nicht W-CLU und nicht W-INT)

- R-CLU-001: komplette 729 Vierknoten-Graphen × 1..4 Quotencases mit **allen 1804** realisierbaren Fälle: `FALSE_INFEASIBLE=0`; keine falsche `PROVEN_INFEASIBLE`-Behauptung, keine verletzten Länderquoten/Protected-Cuts.
- R-CLU-002: nominal echte 400-kV-Überlastung mit deklarierter Klasse 0 wird ohne autorisierte Exception nicht still ausgelassen; 90 MWh/Jahr im Minimalfall; 380→400 nur durch explizite Klassenevidenz.
- R-CLU-003/004: gleiche Generator/Tupel-Protected-IDs ergeben gleiche Hashes; UK-Sourcepage-Manipulation wird abgewiesen.
- R-CLU-005: Status des Country-Alias-/NI-UK-Vertrags separat P2/EXTERNAL_DEPENDENCY, nicht automatisch wegdeklarieren.
- Neue nicht vom Worker bekannte Gegenbeispiele mit gekoppelten Mehrländern, 110-kV-Tie, AC-Islands und gegenläufigen parallelen Korridoren. Alle Gate-G02–G05 Tests neu ausführen.

## 3. S-GOV-GATE nach beiden unabhängigen Rückläufen

Prüfe, dass beide Reviewer **denselben neuen integrierten SHA** tatsächlich getestet haben. Zero offene P0/P1 oder `REPAIRS_REQUIRED`; P2 mit expliziter Disposition, nicht still verschwunden. Source-/CI-Provenienz und neue Run-IDs verifizieren. Entscheide:

- `MA1_SYNTHETIC_QUALIFIED` wenn alle Reparatur- und unabhängigen Gatechecks erfüllt sind; **nur** für die explizit modellierte verlustlose DC-Fixture-Welt.
- `REPAIRS_REQUIRED` wenn reproduzierbare offene P0/P1 oder falsch deklarierte G01–G05 nachweisbar.
- `BLOCKED_CONTRACT` wenn API-Kanonik, Gerätesemantik oder Prüfverträge nicht formal entschiedenen sind.

**Separat:** `REAL_QUALIFIED=false` bis D0–D4 echte source/replay; `ENTSOE_AUTHORITY_UNCONFIRMED` bis offiziell bewiesene Methodikfreigabe. Selbst `MA1_SYNTHETIC_QUALIFIED` ist **kein** PR#13-Merge-Go, kein automatischer MA2-G06–G08-Lauf und keine MA3-Freigabe.

Publiziere zwei unabhängige Reviews + gemeinsames S-GOV-Gateledger, Branch/Commits/CI URLs; Status in #14/#15 nach bestätigter Reviewregel aktualisieren. Kein Selbstreview durch Worker; keine M0/M1/Wetterjahränderung.
