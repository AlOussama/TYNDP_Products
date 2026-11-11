# M2-MA2-PRE — Global Equivalent & Coupled Iteration: Document-Only Design Readiness

**Projekt:** AlOussama/TYNDP_Products. **Rolle:** Lead Scientific Optimization/Power-Flow Architect. **Scope:** sofort ausführbare **read-only/doc-only** MA2-Vorbereitung; keine Implementierung in `src/tyndp_reduce/iosn_official/`, kein produktiver MA2-Branch-Run, keine Runtime-/Realnetzfreigabe.

## 1. Verbindliche Quellen

- [MA2-Handoff 85](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md), `70e92ba9e62a320e58227ce9c2f03fad266f44bf`.
- [GOV-Fünf-Review-Konsolidierung 93](93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md).
- [R-PHY 87](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md), [R-CLU 87](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md).
- [R-API Zielarchitektur](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md).
- [R-METH Autorität](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_INDEPENDENT_METHODOLOGY_AUTHORITY_DELTA_REVIEW_2026_11_11.md).

## 2. Getrennte Spezifikations-Worker (parallel)

**W-EQ-SPEC:** Mathematischen und typisierten v1-Vertrag für europaweiten Netzäquivalent-Fit aus frozen MA1-Busmap und Original-Detailreferenz beschreiben. Für jede gültige Busmap z neue P/Gamma/Az/Zonepairs und Flüsse `p_z=P p_detail`, `f_target=Gamma f_detail` bestimmen. Fit x>0 mit documented Gauge je AC-Insel und rank/sensitivity checks; c0 bilanzneutral `A_z c0=0`; der operative Solver muss affine KVL `C^T diag(x)(f-c0)=0` **wirklich** implementieren, nicht bloß c0 nachträglich addieren. Baumzonen ohne identifizierbare Reaktanz als `UNIDENTIFIABLE`, keine Optimierungszahl erfinden. Neutraler Kalibrierfall braucht **eigenen** physikalisch bilanzierten Dispatch mit HVDC=0/PST neutral. Keine Country-Slacks, keine dichte Europainverse. Regularisierung/Gauge/Gewichtung als Projekt-I mit Testorakel, nicht offiziell.

**W-ITER-SPEC:** L3-Kandidatengenerator ausschließlich mit feasilibitätsbewahrenden Grenzknoten-Moves/Swaps innerhalb Country-Labels, mehreren gekoppelten Ländern, harten Quoten/Connectedness, protected critical lines und expliziten Try/Reject-Statuses; nach **jedem** Kandidaten **voller europaweiter x/c0-Re-Fit**. Trenne Train/Selection/Final-Holdout als eingeschlossene Partitionen *derselben* fünf unveränderten externen Jahre; Selection steuert Accept/Rollback, Holdout bleibt bis finalem unabhängigen Replay versiegelt. Konfigurierbare vergleichbare Fixed-Monitor-Metriken, weil Zonepair-/Linkzahl zwischen Busmaps wechselt; globale Link-RMSE allein nicht ausreichend. Stoppkriterien/Plateau/CPU-Budget dokumentieren und jedes rejected Move dokumentieren.

**W-TEST-SPEC:** analytische Triangle-/Cycle-/Tree-/Multi-Island-/PST-/HVDC-neutral Tests, drei gekuppelte Länder mit mindestens einem angenommenen und einem verworfenen Swap, identische Split-/Source-SHA bei jedem Candidate, additiver Loop-c0-Gegenbeispiel, Inputmutation und fail-closed, numerisch unabhängiger Sparse-/Dense-Abgleich, veränderte Linkzahl inklusive festen Monitoren. Output `test_matrix.csv`, Prüforakel und erwartete Sollwerte, *ohne* eine eigentliche MA2-Produktion oder künstlich erzeugte Real-Daten zu behaupten.

## 3. Deliverables und Gate

- `ma2_equivalent_network_contract.md`; `ma2_iteration_spec.md`; `ma2_analytic_oracle_cases.md`; `ma2_test_and_gate_matrix.json`; `owner_i_decisions.md` + erkennbar als PROPOSED;
- Branch/Commit, neue Dokumentation, keine Änderungen an produktivem MA1, main/M0/M1 oder Wetterjahrwahl;
- `MA2_PREP_READY_FOR_GATE` nur als **Designstatus**, nicht `MA2_IMPLEMENTED` oder `MA2_AUTHORIZED`.

Der **echte MA2-Code-Makro** beginnt ausschließlich nach Integration der MA1-Reparaturen, getrenntem R-PHY-/R-CLU-Re-Review und ausdrücklicher Ownerwahl für die kanonische API. Siehe [Handoff 100](100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md).
