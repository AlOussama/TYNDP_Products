# R-PHY – Prüfanforderung, internes Befundledger und Re-Review-Protokoll

**Dokument:** M2-MA1-R-PHY-20261104 · **Status:** INDEPENDENT_REVIEW_PENDING. Dies ist **kein** von einem anderen menschlichen oder KI-Reviewer signierter unabhängiger Prüfbericht. Das interne Befundledger belegt technische Reparaturen; die separate R-PHY-Rolle muss durch eine tatsächlich andere Instanz ausgeführt werden.

**Verbindlicher Ausgangspunkt:** [82 – MA1-Ausführungsbericht](82_M2_MA1_EXECUTION_REPORT_2026_11_04.md). Eingangs-Commit 2d0b830375c71f3e727d303cdd2ca037da1c67f4; W-PHY-Source-Commit 2f7a56600dc86a6b79a2ae1932b80b7e25614b48; W-PHY-Repair 33e0487f681a8229e79f4df2e89208e01303dde2; Code-Freeze der Integration 0254d867a34b66ec7b56c90225605d29ea328916.

## 1. Separater Prüfgegenstand (R-PHY, nicht W-PHY)

- src/tyndp_reduce/iosn_official/contracts.py
- src/tyndp_reduce/iosn_official/physical.py
- src/tyndp_reduce/iosn_official/preflight.py
- src/tyndp_reduce/iosn_official/ma1.py (nur preflight, Referenzfluss-Eingang und Referenz-Cache)
- src/tyndp_reduce/iosn_official/fixture_evidence.py
- tests/iosn_official/test_ma1_physical.py, test_ma1_integration.py, test_ma1_fixture_evidence.py.

R-PHY soll den eingefrorenen Commit **selbst** auschecken, keine ungeprüfte Zusicherung des implementierenden W-PHY übernehmen und eine neue, zitierbare Run-/Job-Referenz mit unabhängigen Tests erzeugen. Ein Reviewer darf keine M0-/M1-/Wetterjahrauswahl-Dateien reparieren; Reparaturen gehen als eigene W-PHY-Folgerevision zurück zum Review.

## 2. Interne Findings – Reparaturkette

| Finding | Priorität | Prüfbefund | Reparatur | Vorhandener Nachweis |
|---|---|---|---|---|
| PHY-INT-01 | P1, RESOLVED_BY_TEST | NumPy-owning Referenzcache mit writeable=False konnte Flag erneut auf True setzen | immutable bytes-backed Arrays in contracts.py, W-PHY 33e0487f… | Negativtest auf setflags(write=True); 50/50 CI 41792068668 |
| PHY-INT-02 | P1, RESOLVED_BY_TEST | Zeitachse akzeptierte synthetische freie Labels als physische Zeitstempel | ISO-8601 UTC, streng monotone Chronologie, W-PHY 33e0487f… | Negative Zeitstempeltests; 50/50 CI 41792068668 |
| PHY-INT-03 | P1, RESOLVED_BY_TEST | Der MA1-Eingabefingerprint war bei geänderten Grenzwertarrays und unverändertem deklariertem Quellenhash nicht zwingend verschieden | Content-Hash aller normalen und Notfallratings, Integration 0e457d81… | Test test_ma1_run_fingerprint_tracks_actual_rating_values; 52/52 CI 41792893139 |
| PHY-INT-04 | P1, OPEN_DATA | Deklarierte Original-Quellenhashes sind ohne reale Inputbytes und Manifeste nicht unabhängig verifiziert | Keine Ersatzannahme zulässig; externer Datenwitness erforderlich | BLOCKED_DATA, nicht PASS_REAL |
| PHY-INT-05 | P1, OPEN_INTEGRATION | Original-PyPSA-Ausrüstungssemantik, nichttriviale Trafo-Taps, HVDC-Verluste, umfassende Speicher-/Steuergeräte-Abbildung sind nicht numerisch mit einem Realnetz belegt | Vor Realzulassung gesonderter Adapter/solverseitiger Vergleich mit unabhängigen Beispielen | PARTIAL_LOSSLESS_DC_ONLY |
| PHY-INT-06 | P0-GATE, OPEN_REVIEW | Eine technisch andere R-PHY-Reviewinstanz hat bislang keine Findings/Unterschrift/Gate-Replay geliefert | Tatsächlich unabhängigen Reviewer beauftragen; anschließend unabhängigen Re-Review archivieren | INDEPENDENT_REVIEW_PENDING |

## 3. Bereits ausgeführte numerische Eigenschaften (nicht unabhängiger Review)

1. A f = p je **elektrischer** AC-Insel mit Sparsity und Insel-Referenzwinkel (keine versteckte Leistungs-Slack).
2. HVDC positiv bus0→bus1 erzeugt -MW an Bus0 und +MW an Bus1, auch zwischen getrennten AC-Inseln; HVDC niemals als passive AC-Leitung.
3. PST-Fluss f_l=(Sbase/x_l)[theta0−theta1−phi_l], unabhängiger Dense-Referenzvergleich auf kleiner vermaschter Fixture; der neutrale Kalibrierungsfall ist gegenüber operationalen Setpoints ausdrücklich getrennt.
4. Trafo mit bereits nach gemeinsamer MVA-Basis normalisierter DC-Reaktanz; keine unzulässige Behauptung vollständiger AC-Trafo-Modelltreue.
5. Fehlende HVDC-/PST-Zeitreihen, unbalancierte Inseln, zu wenig Ratings, ungültige Quelleinheit (MVA statt MW), 110-kV-Gap und unbekannte Geräte werden abgewiesen.
6. Zwei-AC-Insel-/drei-Länder-Evidence aus [CI 41792893144](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893144), 26 synthetische MA1-Tests bestanden; Input/Output-Evidenz als [Artefakt](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893144/artifacts/13303539283).

## 4. Noch vom externen R-PHY zu prüfende Angriffstests

R-PHY führt eigenständig mindestens drei bisher nicht vom implementierenden Worker definierte Fälle aus: ein stark vermaschtes Netz mit mehreren AC-Islands und nichtzero HVDC, eine PST-Phase mit mehrfacher Maschenverkopplung sowie einen unsymmetrischen Terminalfluss/Verlustmodellversuch, der **fail closed** abgewiesen werden muss. Zusätzlicher Echt-PyPSA-Vergleich n.lpf bzw. anderer unabhängiger Solver erst nach geklärter Komponenten-/Einheiten-Provenienz. Abgleich der Cache-SHA und Zeitordnung gegen tatsächliche Sourcebytes. Skalierbarkeit unter realistischen Sparse-Topologien prüfen (keine dichte Referenzrekonstruktion als Produktionssolver).

Reviewer schreibt für jeden Befund P0/P1/P2, exakte Eingabe, reproduzierbare Kommandos, erwartetes/ist Verhalten, Codezeile und eigenständige Entscheidung. Eine Null-Findings-Entscheidung ist nur nach dokumentiertem Re-Run zulässig. Re-Review kontrolliert konkrete Reparatur-Commits, nicht dieselbe unveränderte Vorversion.

## 5. R-PHY-Gate

**G01/G03:** PASS_SYNTHETIC durch implementierungsnahe CI, **R-PHY_INDEPENDENT: NOT_RUN**. **G11:** PARTIAL_LOSSLESS_DC_ONLY, realer Komponenten-/PyPSA-Witness fehlt. Erst nach unabhängigen Checks darf R-PHY einen Status wie ACCEPT_SYNTHETIC / REPAIRS_REQUIRED vergeben; REAL_QUALIFIED bleibt ohne G12 und Realnetz manifest BLOCKED_DATA.

Die vorliegende Dokumentation **ernennt niemanden automatisch zum Reviewer, behauptet keinen Agentenstart und ist kein signierter Review**.
