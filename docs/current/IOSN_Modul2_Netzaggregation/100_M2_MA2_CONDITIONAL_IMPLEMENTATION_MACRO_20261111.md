# M2-MA2 — Global Equivalent x/c0 & Coupled-Country Re-Clustering (Conditional Implementation Macro)

**Projekt:** AlOussama/TYNDP_Products. **Rolle:** M2 Lead Scientific Software Architect für elektrische Ersatznetze, Sparse-Solver, nichtlineare Optimierung, Graphsearch und statistische Validierung. **Status:** PREPARED_NOT_AUTHORIZED. Dieser Auftrag ist **erst nach Erfüllung der Eintrittsgates** produktiv ausführbar; vorher gilt nur [M2-MA2-PRE 98](98_M2_MA2_PRE_DOCUMENT_FIXTURE_MACRO_20261111.md).

## 0. Strikte Startgates

Vor der Implementierung **alle** drei Bedingungen nachweisbar erfüllen:

1. **MA1_SYNTHETIC_QUALIFIED:** [RR1-Gate 99](99_M2_MA1_RR1_INDEPENDENT_REREVIEW_AND_GATE_20261111.md) mit **zwei unabhängigen** positiven R-PHY-/R-CLU-Gates auf demselben **neuen integrierten Repair-SHA**, keine offene P0/P1 und vollständige Gate/CI-Logs. Der alte 0254-Code und PR #13 allein genügen nicht.
2. **Owner API Entscheidung:** dokumentiert eine kanonische API. Fachliche Empfehlung Option C: `tyndp_reduce.iosn_official` als einziger MA2-Kern, B optional einseitig/typisiert; kein stiller Merge beider Branches. Ohne Ownerfreigabe `BLOCKED_CONTRACT`.
3. **Scoped code authorization:** explizite projektseitige MA2-**SYNTHETIC IMPLEMENTATION ONLY**-Freigabe, O26 weiterhin wissenschaftliche Konsultationsbaseline, nicht behauptete ENTSO-E-approved Methode. Kein Realnetzlauf und kein Merge auf main.

**Normativer Ausgangspunkt:** [MA2-Handoff 85](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) und [18 NR-Matrix](../IOSN_2026_OFFICIAL_NETWORK_REDUCTION_CODE_MAPPING_20261026.md) bleiben detaillierte Basis. Dieses Dokument ergänzt nur die nach unabhängigen Reviews erforderlichen Gates. Quellversion von Handoff 85 `70e92ba9e62a320e58227ce9c2f03fad266f44bf`. Der tatsächlich zu verwendende **reparierte** MA1-Commit wird durch RR1 ermittelt und **nicht im Voraus erfunden**.

## 1. Zwei parallele Worker & unabhängiger Reviewer

**W-EQ:** Implementiere unter eigenem Branch das gesamteuropäische äquivalente DC-Modell mit positiven Ersatzreaktanzen x, deterministischem Gauge je AC-island, rank/conditioning checks und bilanzneutralem strukturellen Offset c0; KCL `A_z f=p_z`, `A_z c0=0` und **operative affine** KVL `Cᵀ diag(x)(f-c0)=0`. Integriere c0 **im Zielsolver**, nicht nur als Postprocessing. Fitte mit versioniertem neutralen HVDC=0/PST-neutral **separat physikalisch bilanzierten** Referenzdispatch; reale Datenlücke wird als BLOCKED_DATA gemeldet. Numerische Methoden als Projekt-I dokumentieren. Sparse numerische Rechnung; keine europaweite Dense-Inverse. Bäume/unidentifizierbare x liefern `UNIDENTIFIABLE`, nicht beliebige Parameter.

**W-ITER:** Entwickle zulässige grenzreine Kandidaten mit exakten Länder-/Gebietsquoten, Connectedness, Protected-Cut Policy und Multi-Country-Boundary-Moves. Für **jeden** gültigen Candidate bilde P, Gamma, A_z, Zonepairs und Flussschnitte **aus denselben eingefrorenen gesamteuropäischen Detailstunden neu**; rufe den globalen W-EQ-Fit vollständig erneut auf. Training/Selection/Final-Holdout strikt getrennt und gehasht über die fünf unverändert extern festgelegten Jahre. Bewertungsmetriken mit robusten **fixed monitors**, Link-RMSE, Summen/Quantilen, kritischer Linienabdeckung, geänderter Linkanzahl, Counterflow und Fairness. Auswahlentscheidung nur nach nachvollziehbarer Selection-Verbesserung, sonst Rollback. Deterministische Tie-Breaker/Plateau-Suchbudget; Kandidatenledger inkl. rejected moves.

**W-INT & R-NUM:** Vereinige nur nach komponentenbezogenen Tests und diffbarem Contract; ein tatsächlich anderer Reviewer reproduziert analytische Cycle-/Tree-/Multi-Island- und gekuppelte Multi-Country-Beispiele aus eingefrorenem SHA, kontrolliert affine KVL, Gauge, identische Source-/Split-Hashes, vollständigen Refit, unveränderlichen Holdout, Richtungsvorzeichen, GPU/Memory-Ausnahmen, invalid Cases. Bei Finding → Worker-Repair → **neuer R-NUM-Re-Review**, kein Selbst-PASS.

## 2. Gates und Output

- **G05:** A_z Γ=P A_d, originaler globaler Fluss, genaue Quoten/Connectedness vor jedem Fit.
- **G06:** positive x und Rang/Gauge; divergence-free c0; KCL/affine KVL in tatsächlichem Zielmodell; neutrale/operationale Gerätesemantik getrennt; solver failure = FAIL.
- **G07:** globale Multi-Country-Kandidatensuche, kompletter Refit je Versuch, verschlossene 3-fach-Splitverwaltung und Candidate-Ledger; Accept/Rollback/Plateau.
- **G08:** RMSE auf reproduzierbaren selection/holdout und festen Vergleichsmonitoren trotz geänderter Zonepairs; nicht erfindbare normative Schwellen; kritische Branch-Quality.
- **R-NUM:** tatsächlich getrennte Re-Review-Evidenz.
- **G12 Real:** weiterhin BLOCKED_DATA ohne vollständige Originaldaten und D4, keine Europavolllast-Behauptung.

Publiziere neuen M2-Code auf separaten Worker-/Integrationsbranches, Tests, reproduzierbare schreibgeschützte Inputmanifeste, Run-Fingerprint, `fit.json`, `equivalent_network.json`, `rmse_per_link.csv`, `candidate_ledger.csv`, `input_split_manifest.json`, `holdout_report.json`, unabhängige Reviewberichte, Abschlussbericht und **MA3-Handoff** im selben Makro. PR bleibt Draft bis Gate/Owner.

**Unverrückbar:** Keine M0/CGMES-, M1/PECD- oder Wetterjahrauswahl-Änderung; kein automatischer main-Merge; keine REAL_QUALIFIED- oder endgültige ENTSO-E-Methodikfreigabe. MA3 N-1-Sommer/Winter×Hin/Rück folgt separat nach geeignetem MA2-Contract/Gate, D3-TSO-Inputs für Realmodus.
