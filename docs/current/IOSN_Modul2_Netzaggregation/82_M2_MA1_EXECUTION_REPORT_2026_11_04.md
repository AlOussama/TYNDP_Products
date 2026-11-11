# M2-MA1 – Physical Foundation + Country-Quota Clustering: Konsolidierter Ausführungsbericht

**Dokument:** M2-MA1-EXEC-20261104 · **Stand:** 04.11.2026 · **Verbindlicher Handoff:** [81_M2_MA1_COLD_START_HANDOFF_2026_11_03.md](81_M2_MA1_COLD_START_HANDOFF_2026_11_03.md) @ 2d0b830375c71f3e727d303cdd2ca037da1c67f4.

**Entscheidung:** CODE_IMPLEMENTED / SYNTHETIC_TESTS_PASS / BLOCKED_INDEPENDENT_REVIEW / BLOCKED_REAL_DATA. **Keine automatische SYNTHETIC_QUALIFIED- oder REAL_QUALIFIED-Freigabe.** Eine grüne CI ist kein unabhängiges wissenschaftliches Review.

## 1. Versions- und Quellennachweis

- Eingangs-Commit exakt verifiziert: 2d0b830375c71f3e727d303cdd2ca037da1c67f4; Review-/Handoff-Branch review/iosn-m2-network-aggregation-plan-20261103.
- Übernommener wissenschaftlicher Audit: 3dc719a35f57bd9516bef8486bf262b75509d6b1.
- Unveränderte historische main-Basis: 1595d6d38e77804760612621657721b3699d2fea.
- Verbindliche Quellen: [80_M2_NETWORK_AGGREGATION_REVIEW_AND_EXECUTION_PLAN_2026_11_03.md](80_M2_NETWORK_AGGREGATION_REVIEW_AND_EXECUTION_PLAN_2026_11_03.md), [18-Punkte-Matrix](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md), [Tabelle-3-CSV](../IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv), ENTSO-E IoSN-Methodik 25.02.2026 **Konsultationsfassung** §§3.8, 3.9, Annex 6.1. Konsultationsfassung nicht als endgültige proprietäre Algorithmenfreigabe deklarieren.
- Beide Implementierungsstränge erben genau vom Eingangs-Commit; sie sind technisch getrennt veröffentlicht. **Das ist keine Behauptung unabhängiger Personen/Agenten-Reviews.**

## 2. Veröffentlichung und Zuständigkeit

| Rolle | Branch/Commit | Befund |
|---|---|---|
| W-PHY | work/iosn-m2-ma1-w-phy-20261104 · 2f7a56600dc86a6b79a2ae1932b80b7e25614b48; Repair 33e0487f681a8229e79f4df2e89208e01303dde2 | Sparse physikalischer Referenzfluss, Multi-AC-Island, PST/Trafo/HVDC, Verträge, Preflight, gezielte Negative-Tests |
| W-CLU | work/iosn-m2-ma1-w-clu-20261104 · 9e20862c7aaf48f003cb59a8e0fc45fb3feaf33e; Repairs ea3aed6d04b912c0a6f93699da8ab4defb4fd89b und 16920d80b24b3f3d2b70cd5ead9fd5cda461f81b | Exakte Landquoten, Länderreinheit, AC-Konnektivität, deterministisches Clustering, 225/400-MWh, P/Gamma/Az |
| Integration | feature/iosn-m2-ma1-integration-20261104 · Code-Freeze 0254d867a34b66ec7b56c90225605d29ea328916 | Zusammengeführt, einmaliger execute_ma1-Ablauf und reproduzierbarer Evidence-CLI |
| R-PHY | [83 – Prüfstatus](83_M2_MA1_R_PHY_REVIEW_STATUS_2026_11_04.md) | Interne Befundprüfung und Reparaturen dokumentiert; unabhängiger Reviewer **noch nicht beauftragt/ausgeführt** |
| R-CLU | [84 – Prüfstatus](84_M2_MA1_R_CLU_REVIEW_STATUS_2026_11_04.md) | Interne Befundprüfung und Reparaturen dokumentiert; unabhängiger Reviewer **noch nicht beauftragt/ausgeführt** |
| MA2 | [85 – Implementierungs-Handoff](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) | Konkreter Folgeauftrag; keine automatische Runtime-Freigabe |

**Pull Request:** [#13](https://github.com/AlOussama/TYNDP_Products/pull/13), Draft. main nicht gemergt.

## 3. Realisierte Modul-2-Software

Neuer isolierter Namensraum src/tyndp_reduce/iosn_official/:

- contracts.py: vollständige persistente Datenverträge, explizite MW / MWh / p.u. / rad-Einheiten, fünf unveränderte externe Jahres-IDs, UTC-Zeitstempel und verifizierbare Formen. Provenienz-Hashes sind deklariert, nicht automatisch mit einem externen Originaldatensatz abgeglichen.
- physical.py: Sparse-SciPy-LU auf dem **gemeinsamen** europäischen AC-Graphen, separat nach tatsächlich elektrischen AC-Inseln bilanziert. HVDC-Terminal-MW als explizite Nettoeinspeisung, kein AC-Zweig und keine verdeckte Slack-Leistung. PST-Phase als affiner Winkelterm. Trafo als bereits normierte verlustlose DC-Ersatzreaktanz; nicht unterstützte Wirkungen REJECTED_COMPONENT.
- preflight.py: PreflightLedger mit Quelle, Einheiten/IDs, Island-Mitgliedern, Country-Mapping, Gerätestatus, Blocker und G01/G03-Prüfungen. Fehlende 110-kV-Ties oder unbalancierte AC-Islands: BLOCKED_DATA.
- country.py: explizite originale Tabelle-3-CSV, exakt 37 Einträge mit Summe 102; „Northern Ireland“ und „United Kingdom“ getrennt. Explizite Mapping-Tabelle und harte Länder-/Zonen-/Konnektivitätsprüfung.
- screen.py: pro externer Wetterjahres-ID aufgelaufene Überlastungsenergie aus stündlichen physikalischen Leitungsflüssen und MW-Grenzen: max(0, |f|-F) mal Stundendauer. **Nur deklarierte 225-/400-kV-Klassen von AC-Lines**, nicht Trafo, PST oder 110-kV-Lines. 220-/380-kV-Nennwerte bedürfen einer expliziten Klassenzuordnung, nicht einer stillen Annahme.
- seed.py: deterministische, länderinterne verbundene Kantenkontraktion bis exakt zu den je Land festgelegten Quoten. Schutz kritischer Zweige, AC-Komponentenfeasibility, Gegenfluss/Parallelkorridor-Aggregation als Diagnose. Dies ist **I-01 (eigene deterministische Heuristik)** und kein von ENTSO-E veröffentlichtes Clustering-Framework.
- operators.py: Sparse-P, Gamma, A_z und A_d mit exakter gerichteter Identität A_z Gamma=P A_d und resultierender KCL. HVDC bleibt terminalseitig, nicht in der AC-Inzidenz.
- ma1.py: ein vollständiger, fail-closed MA1-Ablauf, eingefrorene Originalflüsse, busmap, jährliche Scores, gerichtete Zonenschnitte, nachgeprüfte Gate-Matrizen; Lauf-Fingerprint schließt tatsächliche normale/Notfall-Ratings ein.
- fixture_evidence.py: öffentlich ausführbarer **synthetischer** 7-Bus/3-Country/2-AC-Island/1-HVDC/PST/Trafo-Zeuge mit fünf expliziten MOCK-Jahres-IDs; schreibt ausschließlich neue Output-Verzeichnisse.

Tests liegen unter tests/iosn_official/, die dedizierte GitHub-CI unter .github/workflows/m2-ma1-gates.yml. Die Legacy-Module unter src/tyndp_reduce/*.py, M0-, M1- und Wetterjahrauswahl-Code wurden **nicht geändert**.

## 4. Ausgeführte numerische Tests und Gate-Nachweise

**Code-Freeze CI:**
- [Core Workflow 41792893139](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893139): **52 passed**. Beinhaltet alte Pakettests plus neue MA1-Tests und bestehenden Demo-Run.
- [Dedizierter MA1 Workflow 41792893144](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893144): **26 passed**.
- [Maschinenlesbarer CI-Artefakt-Download](https://github.com/AlOussama/TYNDP_Products/actions/runs/41792893144/artifacts/13303539283): **15 Dateien (14 SHA-256-Einträge plus Manifest)**; Input-Fingerprint a378e22fde234cdf9275bcb5685f1034c1e41eeb442b81a8cfe06ed988882661.
- Synthetische Referenz: 7 AC-Knoten, 8 passive AC-Zweige inklusive Trafo/PST, 1 kontrollierter HVDC-Korridor, **2** AC-Inseln, 3 Country-Labels, synthetische Quoten 2+1+1=4, **5 MOCK-Jahre**, 5 synchronisierte Snapshots. Keine echten ENTSO-E-/PECD-Stunden.

| Gate | Tatsächlich überprüft | Status und Grenze |
|---|---|---|
| G01 | Datenidentität, SHA-/Provenienzfelder, UTC, fünf Jahres-IDs, Snapshot-Ordnung, Bilanz je AC-Island, Einheiten | **PASS_SYNTHETIC**; reale Quelldaten und deren Byte-Hashes fehlen |
| G02 | Original-CSV 37 Länder/102 Zonen, gesondert NI/UK; synthetische exakte Country-Quoten und Falschmapping-Negativfälle | **PASS_SCHEMA + PASS_SYNTHETIC**, offizielle Vollgeographie **BLOCKED_DATA** |
| G03 | Country-Purity, Connectedness, AC-Island-Komponenten, geschützte Grenzlinien, 110-kV-Fail-Closed, keine HVDC-Verwechslung als AC-Kante | **PASS_SYNTHETIC** |
| G04 | 225-/400-kV-Klassenscreening, Jahres-MWh, Zeitdauer, variable Limits, explizite Jahresgewichte, negative 380-kV-Klasse | **PASS_SYNTHETIC**; Marktergebnisse fehlen |
| G05 | A_z Gamma=P A_d, A_z Gamma f_d=P p_d, Vorzeichenwechsel, parallel gegenläufige Ströme; Sparse-Export/Reload | **PASS_SYNTHETIC** |
| G11 Teil | PST-Winkeloffset, HVDC-Terminalvorzeichen, AC-Inselbalance, neutral vs operativ, Trafo-x als DC-Ersatz | **PARTIAL_LOSSLESS_DC_ONLY**; Geräte- und PyPSA-Realnetz-QA fehlt |
| G06–G10, G12 | Globale x/c0-Kalibrierung, coupled iterations, N-1 / 4 Kapazitäten und Realnetz | **NOT_IN_MA1 / BLOCKED**, nicht freigegeben |

## 5. Reparatur- und Re-Test-Ledger

| Befund | Evidenz / Ursache | Reparatur | Re-Test |
|---|---|---|---|
| CLU-P1-01 | Erster integrierter CI-Run 41790704745: bei drittem Jahres-Snapshot 3 Überlastungsstunden; Test fälschlich 0 erwartet | W-CLU ea3aed6d…, Integration 7f7d3dc… | 44/44 bestanden in 41790847217 |
| PHY-P1-01 | NumPy-owning Array mit writeable=False erlaubt manuell writeable=True | W-PHY 33e0487f…: immutable bytes-backed NumPy-Arrays; zusätzlicher Negativtest | 50/50 in 41792068668 |
| PHY-P1-02 | Zeitstempel akzeptierten freie Strings ohne UTC-Nachweis | W-PHY 33e0487f…: ISO-8601 UTC und streng monotone Chronologie | 50/50 in 41792068668 |
| INT-P1-01 | Bei unverändert deklariertem Ratings-Source-Hash konnten geänderte MW-Grenzen Lauf-Fingerprint wiederverwenden | Integration 0e457d81…: Rating-Array-Content-Hash und Regression | 50/50 in 41792068668 |
| CLU-P1-02 | 380-kV-Nennspannungen konnten still aus dem Screening fallen | W-CLU 16920d80…, Integration 0254d867…: explizite Klasse 225/400 oder Ausschluss 0 | 52/52 und 26/26 in Code-Freeze-CI |

Die Reparaturen wurden nach ihrer Umsetzung erneut numerisch getestet. Ein **unabhängiger Re-Review durch einen anderen Reviewer** wurde nicht durchgeführt und ist deshalb kein PASS.

## 6. Veröffentlichter Output- und Gate-Vertrag

Die Fixture-CLI erzeugt ein **neues, niemals überschriebenes** Ergebnisverzeichnis, in dem (a) preflight_ledger.json, (b) gate_ledger.json, (c) merge_ledger.json, (d) counterflow_ledger.json, (e) reference_flow_manifest.json, (f) country_quotas.csv, (g) busmap.csv, (h) annual_criticality.csv, (i) zone_cuts.csv, (j) global_reference_flows.npz, (k–n) operator_P/Gamma/A_z/A_d.npz und (o) manifest.json vorhanden sind. Das Manifest trägt den ausführenden SHA, Input-Fingerprint, Output-SHA-256s, Dimensions-/Einheitenbezug, kein x/c0-Fit und die unverrückbaren Flags real_network_qualified=false und independent_reviewer_release=false.

Reproduktion für einen akzeptierten SHA (Repository-Root):

~~~bash
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/iosn_official
python -m tyndp_reduce.iosn_official.fixture_evidence --output /tmp/ma1-gates-example --commit <PINNED_HEAD_SHA>
~~~

Der Output-Ordner darf beim Start noch nicht existieren. Der wissenschaftlich gültige Realinput wird ausschließlich upstream gemäß Datenvertrag erzeugt; die Fixture darf niemals als reale ENTSO-E-102-Zonen-Abnahme ausgegeben werden.

## 7. Offene Grenzen und Freigabeentscheidung

**BLOCKED_DATA:** synchrones europäisches AC-Netz mit vollständigen Trafos, PSTs, HVDC-Terminals und Verlust-/Tap-Semantik, Country-Label-Resolver für sämtliche 37 veröffentlichten Labels, zeitabhängige MW-Grenzen und Kontingenz-/TSO-Daten. Ein echter PyPSA-Netzadapter wird mit MA1 nicht still als validiert deklariert. Zurückgewiesene Sondergeräte benötigen explizite Erweiterungen und Tests. Weder M0-Reader noch M1-Reader wurden mitgezogen.

**BLOCKED_INDEPENDENT_REVIEW:** Es steht kein tatsächlich voneinander verschiedener R-PHY- und R-CLU-Reviewer-Ausführungsnachweis zur Verfügung. Die beiden Rollen sind im separaten Review-Handoff unter 83/84 angefordert. CI und unsere interne Befundprüfung ersetzen keinen solchen Reviewer.

**Divergierende andere Linie:** Der separat bestehende Branch [restructure/iosn-m2-ma1-integration-20261103](https://github.com/AlOussama/TYNDP_Products/tree/restructure/iosn-m2-ma1-integration-20261103) @ 88374dd38792146ca55fa3fe2d4b35dac842c0b9 führt eine alternative MA1-API unter src/tyndp_reduce/m2/. Es erfolgte **weder ein Merge noch ein Vertragsschwenk**. Vor Übernahme in main bzw. MA2-Integration muss die kanonische Linie festgelegt oder durch unabhängiges Interface-Reconciliation geprüft werden.

**Release:** Code/Tests/Fixture-Evidence veröffentlicht, Draft PR offen, main unberührt. Kein Auto-Merge, keine reale numerische Qualifikation, keine automatische Folge-Runtime-Freigabe. MA2-Handoff ist als **technischer, branchgebundener Folgeauftrag** vorbereitet.
