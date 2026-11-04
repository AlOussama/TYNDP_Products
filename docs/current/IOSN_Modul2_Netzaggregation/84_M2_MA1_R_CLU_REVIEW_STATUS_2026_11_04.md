# R-CLU – Prüfanforderung, internes Befundledger und Re-Review-Protokoll

**Dokument:** M2-MA1-R-CLU-20261104 · **Status:** INDEPENDENT_REVIEW_PENDING. Interne Checks und CI sind nachvollziehbar; ein getrennt arbeitender R-CLU hat sie **noch nicht** als unabhängiger Reviewer reproduziert oder signiert.

**Verbindlicher Ausgangspunkt:** [82 – MA1-Ausführungsbericht](82_M2_MA1_EXECUTION_REPORT_2026_11_04.md). W-CLU-Ausgangscommit 9e20862c7aaf48f003cb59a8e0fc45fb3feaf33e, Repairs ea3aed6d04b912c0a6f93699da8ab4defb4fd89b und 16920d80b24b3f3d2b70cd5ead9fd5cda461f81b, integrierter Code-Freeze 0254d867a34b66ec7b56c90225605d29ea328916.

## 1. Separater Prüfgegenstand (R-CLU, nicht W-CLU)

- docs/current/IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv (37 Originalzeilen/102; Northern Ireland und United Kingdom getrennt)
- src/tyndp_reduce/iosn_official/country.py, seed.py, screen.py, operators.py
- src/tyndp_reduce/iosn_official/ma1.py (Screening→Kosten→Länderquoten→Gamma-Integrität)
- tests/iosn_official/test_ma1_clustering.py, test_ma1_integration.py, test_ma1_fixture_evidence.py
- Methodik-Mapping [NR-01 bis NR-18](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md).

R-CLU muss alle 37 Original-Länderlabels gegen Tabelle 3 der ENTSO-E-Konsultationsfassung 25.02.2026 überprüfen; NORTHERN IRELAND darf **nicht** als stilles Alias des UNITED KINGDOM zusammengezogen werden. Die synthetische 2+1+1-Quote ist absichtlich nicht die europäische 102-Zonen-Quote.

## 2. Interne Findings – Reparaturkette

| Finding | Priorität | Prüfbefund | Reparatur | Vorhandener Nachweis |
|---|---|---|---|---|
| CLU-INT-01 | P1, RESOLVED_BY_TEST | Ein 3-h-Snapshot mit Stromüberlastung erwartete fehlerhaft 0 statt 3 Überlastungsstunden | W-CLU ea3aed6d…; Integration 7f7d3dc… | Ursprünglicher [FAIL 41790704745](https://github.com/AlOussama/TYNDP_Products/actions/runs/41790704745) und [PASS 41790847217](https://github.com/AlOussama/TYNDP_Products/actions/runs/41790847217) |
| CLU-INT-02 | P1, RESOLVED_BY_TEST | Ein nomineller 380-kV-AC-Korridor konnte bei exakter 225/400-Abfrage ohne Gate verloren gehen | W-CLU 16920d80… und Integration 0254d867…: explizite screening_class_kv=225/400 bzw. 0 für bewusstes Exkludieren; 200–450-kV-Ambiguität fail closed | test_nonstandard_380kv_requires_explicit_400kv_screening_class; 52/52 CI 41792893139 |
| CLU-INT-03 | P1, OPEN_DATA | Keine geografisch vollständige, eindeutig zuordenbare reale Bus-ID→37-Country-Zuordnung | Nie synthetisch ergänzen; vollständiges Originalreferenznetz/Mapping erforderlich | BLOCKED_DATA |
| CLU-INT-04 | P2, SPEC_RESTRICTION | Country-Resolver verlangt injektive Raw-ID→Original-Label-Tabelle. Mehrere Rohalias-IDs eines Landes würden ohne Vor-Normalisierung abgewiesen | Dokumentierte Upstream-Normalisierung nach Originaltaxonomie; weiterhin keine stille NI/UK-Zusammenlegung | Fail-closed-Kontrakt, keine reale Durchgängigkeit versprochen |
| CLU-INT-05 | P2, METHOD_LIMIT | Deterministische Greedy-Kantenkontraktion ist ein deklariertes I-01-Verfahren, keine vollständige veröffentlichte ENTSO-E-Suchheuristik. Gegenläufige Korridorflüsse werden gemeldet, aber nicht als finale N-1-/RMSE-Qualität eingestuft | MA2 gekoppelte globale RMSE-Schleife; MA3 N-1 nachschalten, kein ad hoc Multi-Kriterien-Clustering als offiziell etikettieren | Gate G08/G09 bleiben MA2/MA3 |
| CLU-INT-06 | P0-GATE, OPEN_REVIEW | Ein unabhängiger R-CLU-Reviewer hat weder eigenständig getestete Fixtures noch eine Gateentscheidung vorgelegt | Unabhängiger Reviewer + Re-Review nach etwaiger Reparatur nötig | INDEPENDENT_REVIEW_PENDING |

## 3. Bereits ausgeführte numerische Eigenschaften (nicht unabhängiger Review)

- Tabelle-3-CSV wird als exakte **37/102-Abschrift** erkannt; Originalbezeichnungen bleiben textgenau; ein manipuliertes Summenbudget wird als nicht-offiziell verworfen.
- Jede Originalbus-ID hat exakt eine Zone, Country-Purity und AC-Konnektivität sind hart, nicht bloß Teil einer Penalty-Funktion.
- Unterbudgetierte getrennte AC-Komponenten innerhalb desselben Landes, unbekannte Raw-Country-IDs und Verschlucken geschützter kritischer Leitungen führen zur Abweisung.
- Cross-Country-AC-Ties bleiben im **gemeinsamen** orientierten Originalgraphen. Nur die Clusterzugehörigkeit ist länderrein. Kein per-country getrenntes PTDF-Verfahren.
- Original-Spannungsklassen 225/400 werden aus expliziten Angaben gemappt, 110-kV-Leitung/PST/Trafo nicht als Screening-AC-Line verwechselt; annual MWh mit variabler Grenze und eigener Dauer pro Jahr.
- Für jeden Kandidaten gilt A_z Gamma=P A_d und A_z (Gamma f_d)=P p_d. Entgegengesetzte Parallelflüsse werden separat als Gegenflussdiagnose ausgegeben.
- Ergebnis [dedizierte MA1 CI 41792893144](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893144) 26 passed sowie [Core 41792893139](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893139) 52 passed; kein Realnetz-PASS.

## 4. Noch vom externen R-CLU zu prüfende Angriffstests

R-CLU prüft **unabhängig** die 37/102-Originalquelle einschließlich CSV-Duplikaten/GB–NI-Abgrenzung; unmögliche nationale Quoten bei AC-Inseltrennung; drei geografische Länder mit Triple-Junction-Bus und 110-kV-Tie-Lücke; kritische Grenzzweige, deren Schutz durch Quoten unmöglich wird (explizites BLOCKED, keine stillschweigende Relaxation); parallel gegenläufige Flüsse und Ties mit entgegengesetzter Orientierung; 220/380-kV-Klassifizierungsprovenienz; tatsächliche Lastfluss-Synchronität der fünf *unveränderten* Wetterjahre.

Zusätzlich ist die Greedy-Auswahl gegen kleine vollständige Graphenumeration zu prüfen: valide Quoten/Konnektivität müssen unabhängig von heuristischer Qualität stets gelten. Das aktuelle Greedy-Verfahren darf nicht als international optimales oder veröffentlichungsidentisches Ergebnis etikettiert werden.

R-CLU liefert ein signiertes Ledger mit P0/P1/P2-Findings, Testkonfiguration, Testjobs, beobachteten/erwarteten Ausgaben, offener Physik/Data-Klassifikation und Entscheidung. Auf Reparaturen folgt eine neue unabhängige Re-Review-Referenz.

## 5. R-CLU-Gate

**G02–G05:** numerisch PASS_SYNTHETIC; **R-CLU_INDEPENDENT: NOT_RUN**. Der offizielle vollständige 102-Zonen-Fall benötigt reale Country-/AC-Topologie-Inputs. Unabhängige Reviewerfreigabe und reale E2E-Qualifikation sind nicht durch diesen Bericht ersetzt.
