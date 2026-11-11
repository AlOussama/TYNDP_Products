# M2-MA1-RP1 — Consolidated Independent Findings Repair Macro

**Projekt:** \`AlOussama/TYNDP_Products\`. **Rolle:** M2-Implementierungskoordinator, mit parallelen *separaten* W-PHY und W-CLU, eigenem Integrator W-INT.  
**Start:** sofort zulässige Worker-Reparatur auf einem **neuen Draft-Branch**. Keine Main-Änderung, keine PR #13-Merge, kein MA2-Runtime-GO und **keine** Selbstfreigabe als unabhängiger Reviewer.  
**Fix-Baseline:** PR #13, \`70e92ba9e62a320e58227ce9c2f03fad266f44bf\`; Code-Freeze \`0254d867a34b66ec7b56c90225605d29ea328916\`.

## 0. Verbindliche vollständige Quellen und Unveränderlichkeit

- [S-GOV konsolidierter Review 93](93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md).
- [R-PHY 87](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md), [Findings JSON](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/R_M2_MA1_PHY_FINDINGS_20261111.json), [Worker-Handoff 88](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/88_R_M2_MA1_PHY_W_PHY_REPAIR_HANDOFF_2026_11_11.md).
- [R-CLU 87](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md), [Findings JSON](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/88_R_M2_MA1_CLU_FINDINGS_LEDGER_20261111.json).
- [R-API Compatibility Review](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md).
- [PR #13](https://github.com/AlOussama/TYNDP_Products/pull/13), [R-PHY #14](https://github.com/AlOussama/TYNDP_Products/issues/14), [R-CLU #15](https://github.com/AlOussama/TYNDP_Products/issues/15).

Lies alle relevanten Codepfade unter \`src/tyndp_reduce/iosn_official/\` und Tests. Prufe zuerst Commit-Existenz, Parent/HEAD und Branch-Trees. Die beiden externen Review-Branches dürfen **nicht** verändert werden. Keinen der defektreproduzierenden Tests löschen, schwächen oder stillschweigend aus der Evidenz entfernen. Kein M0, M1, Weather Year oder Legacy-Algorithmus.

## 1. W-PHY – vier P1 reparieren

**PHY-R01 – Mutable Contract / TOCTOU:** \`DetailedGridSnapshot\`, \`ReferenceDispatchSet\`, \`TimeSet\`, \`ReferenceFlowCache\` und alle annotierten Tupel-/Sequenzfelder gegen nachträgliche Caller-Mutation absichern. Defensive, vollständig validierte Tuple-Freeze oder strikte Abweisung; Fingerprint und vorhandene Array-SHA/Eigentumsregeln erhalten. Negative Tests mutieren Liste nach validiertem Object-Create und erzwingen Fail oder identische unveränderliche Snapshot-Semantik.

**PHY-R02 – Lossless-Flag:** \`HVDCTerminals.lossless\` streng auf tatsächlichen Python-Boolean prüfen. \`False\` bleibt für nicht unterstützte Verlustmodelle fail-closed; \`"False"\`, \`0\`, \`1\`, \`None\` dürfen nicht als supported durchgehen. Kein neues asymmetrisches HVDC-Modell ohne gesonderten Geräte-Owner-Gate.

**PHY-R03 – In-service-Flag:** \`ACBranch.in_service\` streng boolean, ebenso sicherheitsrelevante \`incomplete_110kv_ties\` und \`Provenance.synthetic\`; keine implizite Truthiness. Test, dass out-of-service Zweige nicht als aktive elektrische Verbindung wirken.

**PHY-R04 – Toleranz:** \`atol_mw\` muss endlich, positiv und plausibel beschränkt oder intern unabhängig durch eine fest eingefrorene harte Island-/KCL-Sicherheitsgrenze geschützt sein; \`inf\`, \`nan\`, extrem hohe endliche Werte und physikalisch unbilanzierte +/-20/-19-MW-Fälle strikt abweisen. Fachliche numerische Toleranz dokumentieren als eigene I-Festlegung, nicht als ENTSO-E-Vorgabe.

Abnahmetests: neue Worker-Positive/Negative Tests; von R-PHY unabhängiger 10-Bus/3-AC-Island/2-HVDC/2-PST-Cycle-Orakel; 1001-Bus-Sparse-Test; bestehende MA1-15-Artefaktfixture; umfassender \`pytest\` ohne unerklärte XFAIL/XPASS. Reviewer-Tests sind weiterhin unter originalen Sha/Review-Branch auffindbar.

## 2. W-CLU – zwei P1, zwei P2 reparieren und einen P2-Vertrag dokumentieren

**R-CLU-001 – False infeasible:** Greedy protected-edge contraction darf nicht aus einer lokalen Sackgasse auf globale Unrealisierbarkeit schließen. Implementiere deterministisches alternatives Merge-/Backtracking/Feasibility-Gate mit klaren Status \`HEURISTIC_STUCK\` vs. \`PROVEN_INFEASIBLE\`; keine behauptete proof-complete Suche auf beliebigen großen Graphen, falls nur begrenzt. Verifiziert durch **729 Vierknoten-Graphvarianten × k=1..4**, alle **1804** zulässigen Fälle müssen ohne falsche \`INFEASIBLE\`-Markierung bleiben (vorher 10 falsche Blockierungen). Bewahre Connectedness, harte Landesquote, harte Protected-Cuts, NI/UK-Trennung, Determinismus. Ergänze größere Graph-/Mehrländerfixtures und CPU/Feasibility-Abbruchledger.

**R-CLU-002 – Screening-Abdeckung:** nominell 225-/400-kV-eligible Leitungen dürfen durch \`screening_class_kv=0\` nicht ohne belegte und prüfbare Exclusion samt Scope/Source aus dem 225/400-MWh-Ranking verschwinden. Test 400-kV, 100 MW, 10 MW limit, 1h/Jahr = **90 MWh pro Jahr**. 220/380→225/400 nur mit expliziter Quellenklasse; 110 kV/Trafo/PST nicht umdefinieren. Kein Ersatz durch ein unautorisiertes \`method_b\`.

**R-CLU-003:** \`protected_line_ids\` einmalig vor jeder Verwendung materialisieren, validieren, deterministisch sortieren/hashen. Tupel und Generator für gleiche Schutzmenge ergeben denselben Input-Fingerprint und dieselbe Busmap.

**R-CLU-004:** Budget-\`source_page\` exakt je Originalcountry/label validieren (UK = 27 statt fälschlich 26 akzeptieren), alternativ keinen behaupteten seitenscharfen Nachweis speichern.

**R-CLU-005:** bisherige Many-to-one-Raw-Alias-Limitierung dokumentieren, zulässigen vorgezogenen quellentreuen Resolver **innerhalb des M2-Vertrags** designen/testen. NI und UK niemals zusammensetzen; keine Änderungen an M0/M1.

## 3. W-INT – zusammenführen, vollständig erneut testen, kein Gate-Selbstentscheid

Parallel W-PHY/W-CLU auf getrennten Arbeitsbranches aus \`70e92...\`; W-INT integriert nur nach Worker-Kommit; zuerst normaler 52/26-Testsatz, danach unabhängige Repro-Cases und neue Tests. Alle nachgewiesenen offenen P1 behoben; neue Regressionsfehler mit eigener Repair-Runde beheben. Review-Test-Transkripte auf den alten SHAs unverändert erhalten; bei strict-XFAIL→XPASS ist der alte Tester erwartungsgemäß rot – **der neue unabhängige Reviewer** verwaltet allein die spätere Umklassifizierung in reguläre PASS-Tests.

Verifiziere G01–G05 und G11 Partial; vollständige SHA-gebundene Evidence-Fixture neu erzeugen, inklusive Rating-Content-Fingerprint, Protected-IDs und Source-Page. Am Ende ein **einziges neues integriertes Repair-Commit**, branch \`feature/iosn-m2-ma1-rp1-integration-20261111\` oder eindeutig anders benannt, dokumentieren.

## 4. Pflichten zur Publikation und unabhängige Re-Review-Übergabe

- W-PHY-Branch + SHA + Diff + Tests; W-CLU-Branch + SHA + Diff + Tests; integrierter Repair-SHA, CI URL und Maschinenmanifest.
- P1-Status pro Finding \`FIXED_BY_WORKER_TEST\` (bis unabhängiger Reviewer separat bestätigt); P2 dispositioniert.
- Kein eigenes \`ACCEPT_SYNTHETIC\`, \`REAL_QUALIFIED\` oder \`MA2_READY\` ausgeben. Reparatur ist keine unabhängige Freigabe.
- **Zwei unabhängige Re-Reviews** auf exakt demselben integrierten Repair-SHA anfordern: [Handoff 99](99_M2_MA1_RR1_INDEPENDENT_REREVIEW_AND_GATE_20261111.md), getrennte R-PHY und R-CLU-Instanzen, getrennt von implementierenden Workern.
- Lücken: echter 37/102-Realnetzinput und gerätegenauer PyPSA-/TSO-Zeuge weiterhin \`BLOCKED_DATA\`; keine automatische Freigabe.
