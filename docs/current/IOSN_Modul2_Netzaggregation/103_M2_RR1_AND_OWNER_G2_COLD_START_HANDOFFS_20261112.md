# S-GOV-M2 – RR1-R-PHY, RR1-R-CLU und Project Owner-G2: getrennte Copy-ready-Handoffs

**Projekt:** AlOussama/TYNDP_Products. **Verbindliche Konsolidierung:** [Dok. 102](102_M2_A_E_CONSOLIDATION_AND_G2_READINESS_20261112.md). **Status:** zwei Reviewer-Replays **jetzt** ausführbar; Owner-Entscheidungsvorbereitung **jetzt**; Datenbeschaffung nur mit tatsächlichem externem Zugang; MA2-Code **noch gesperrt**.

## RR1-R-PHY — Independent Repair Re-Review, Chat R-PHY-RE

**Rolle:** Unabhängiger Power-Systems/Python-Sparse-Reviewer, weder W-PHY, W-CLU noch W-INT.

1. Prüfe zuerst [integrierten Worker-Repair-SHA fb201ef5](https://github.com/AlOussama/TYNDP_Products/commit/fb201ef5f120f64696dea9aa99f77ece77546f9a) auf [Draft PR #41](https://github.com/AlOussama/TYNDP_Products/pull/41), dessen Parent `70e92ba9...` und den [W-INT-Report 101](https://github.com/AlOussama/TYNDP_Products/blob/fb201ef5f120f64696dea9aa99f77ece77546f9a/docs/current/IOSN_Modul2_Netzaggregation/101_M2_MA1_RP1_INTEGRATION_AND_RR1_HANDOFF_20261111.md).
2. Lies den [originalen unabhängigen R-PHY-Report mit allen vier P1-Repros](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md) und den [RR1-Vertrag 99](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/99_M2_MA1_RR1_INDEPENDENT_REREVIEW_AND_GATE_20261111.md).
3. Reproduziere **unabhängig** auf dem neuen integrierten SHA sämtliche vier Angriffe als erwartete **gewöhnliche PASS**: mutable caller sequences/TOCTOU-Fingerprint, `lossless="False"`, `in_service="False"` mit related flags, `atol_mw=inf/nan/huge` plus unbalanced [+20,-19] MW. Bewahre ursprüngliche XFAIL-Zeugen unverändert auf dem Originalreview-Branch; eigene normalisierte Assertions im **neuen** Review-Branch, ohne deren Inputs/erwartete Fehlerschwellen zu schwächen.
4. Baue eigenständige 10-Bus/3-AC-Island/2-HVDC/PST Sparse-vs-Dense-Cycle/KCL/KVL-Gegentests, 1001-Bus-Sparse-Stress, UTC/Source/Ratings/Hash-Fail-Closed und 15-Dateien-Synthetic-Witness; überprüfe den numerischen tolerierten Wert >0 und <=1e-6 MW samt begründetem absoluten/skalierungsbewusstem Hard-Gate.
5. Dokumentiere exact checkout, Repo-/pytest-Version, JUnit, unabhängiges CI/run SHA, gefundenen P0/P1/P2, G01/G03/G11-Teilaussage und `ACCEPT_SYNTHETIC` oder `REPAIRS_REQUIRED` als **eigene** Entscheidung. Falls P0/P1 verbleiben: konkrete Worker-Reparatur und neuer unabhängiger Re-Review.
6. Veröffentliche auf eigenem unveränderten Review-Branch und melde Ergebnis bei [Issue #14](https://github.com/AlOussama/TYNDP_Products/issues/14). Kein main/PR-Merge, kein MA2/Real-Go, kein M0/M1/Weather-Change.

## RR1-R-CLU — Independent Repair Re-Review, Chat R-CLU-RE

**Rolle:** Unabhängiger Scientific Graph/Clustering/Optimization Reviewer, nicht W-CLU/W-INT und nicht derselbe Implementierungsreviewer wie R-PHY-RE.

1. Pinned Integrations-SHA **`fb201ef5f120f64696dea9aa99f77ece77546f9a`**, [PR #41](https://github.com/AlOussama/TYNDP_Products/pull/41). Lies [Original R-CLU-Report](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md), [Findings JSON](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/88_R_M2_MA1_CLU_FINDINGS_LEDGER_20261111.json), [RR1 #99](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/99_M2_MA1_RR1_INDEPENDENT_REREVIEW_AND_GATE_20261111.md).
2. Berechne unabhängige vollständige Vierknoten-Graphenumeration: 729 Edge-State-Graphen, k=1..4 und alle **1804** feasible Cases; `FALSE_PROVEN_INFEASIBLE=0`, `FALSE_REJECTED_FEASIBLE=0` innerhalb der vereinbarten vollständigen kleinen Oracle-Familie. Größere 5/6-/Mehrländer- und Budget-Stop-Gegenfälle prüfen, `HEURISTIC_STUCK` darf nicht als bewiesene Unmöglichkeit gelten.
3. R-CLU-002: echte 400-kV-Leitung bei 100 MW/10-MW-limit/1 Stunde je Jahr ergibt **90 MWh/Jahr** oder explizites fail-closed bei nicht nachgewiesener Exklusion. 380/220→400/225 nur mit source-backed mapping; kein stilles Class0.
4. P2: protected Generator/Tupel identische Input-Fingerprints, UK-Page27/NI-UK, Source Country Aliases opt-in und source metadata vs originale Datei-SHA-Qualität getrennt.
5. Prüfe harte Country-Quoten, AC Connectedness, protected branches und A_zΓ=P A_d, inselrichtige Netzphysik und Counterflow-/Grenzkorridorlogik; eigene neue Gegenbeispiele; CI/JUnit/Branch und SHA.
6. Publiziere unabhängige Findings, Entscheidung und Update [Issue #15](https://github.com/AlOussama/TYNDP_Products/issues/15); niemals Worker-Evidenz als Reviewer-Signoff übernehmen, kein Merge/Real-/MA2-Go.

## S-GOV-M2-G2 / Project Owner – API, Methode und scoped Runtime

**Start:** Owner-Entscheidung kann parallel zu beiden RR1-Reviews vorbereitet und getroffen werden; **positive MA2-Code-Freigabe wird erst nach positivem RR1-SHA-Nachweis wirksam**.

1. Lies [API Owner-Vorlage B](https://github.com/AlOussama/TYNDP_Products/blob/ed42d051a7234f7f062d94d06291f66e56657bbc/docs/current/IOSN_Modul2_Netzaggregation/M2_API_G1_20261111/api_owner_options_and_recommendation.md), [M2-METHOD-G1 Entscheidungen D](https://github.com/AlOussama/TYNDP_Products/blob/c980bbd341b1051257bcf31b0a904dd7937f7241/docs/current/IOSN_Modul2_Netzaggregation/m2_owner_decision_register.md), [MA2-PRE I-Entscheidungen E](https://github.com/AlOussama/TYNDP_Products/blob/b73bb3c595bff515aeca052f02fc83f72289b5f0/docs/current/IOSN_Modul2_Netzaggregation/ma2_pre_20261112/owner_i_decisions.md).
2. Hole eine **ausdrückliche Owner-Entscheidung** ein: `OD-M2-API-01=A/B/C` (C empfohlen, A als einzige Kanonik, B nur optional one-way, kein Merge); `OD-M2-API-02=STRICT_LOSSLESS`, `03=SEPARATE_MODEL_DISCREPANCY_QA`, `04=AUDITED_CLASS_AND_PROTECTION`, `05=DOC_GATE_ONLY_NO_MERGE`; `OD-M2-METH-01=O26_AS_PROVISIONAL_SCIENTIFIC_BASELINE` (nicht adopted ENTSO-E); `OD-M2-MA2-CODE=DEFER/SCOPED_SYNTHETIC_ONLY_AFTER_RR1`; `OD-M2-MERGE=NO_MERGE_NOW`. Diese sind Empfehlungen, **nicht** bereits entschieden.
3. Minimaler spezifischer I-Parameter-Freeze vor MA2-Code: gauge/rank/tolerances, x positive bounds, c0 affine Mesh, neutral reference, blocked Train/Selection/Final-Holdout, fixed monitor catalogue, fair RMSE accept, plateau/budget and rejection ledger. Ein methodisch nicht beschlossener Zahlenwert darf nicht als ENTSO-E-Grenzwert etikettiert werden.
4. Nach den zwei getrennten RR1-Berichten verifiziere SHA-Gleichheit, CI/Repro, offene P0/P1=0 und P2-Disposition. Erst dann `MA1_SYNTHETIC_QUALIFIED` als enger Scope; `REAL_QUALIFIED=false`, `G11_PARTIAL`.
5. Publiziere Ownerakte als expliziten signierten/auditierbaren Repo-/Issue-Beschluss **nur nach tatsächlicher Ownerwahl**, auf eigenem Governance-Branch; ohne Wahl `OWNER_PENDING` beibehalten. Keine automatische Runtime/PR-Merge. MA2 startet mit [Conditional Code Macro 100](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md) auf tatsächlich geprüfter Repair-Basis und 45 Testfällen von E **erst** nach allen Gates.

## D-SOURCE-OWNER — Keine Wiederholung von D-SOURCE1-Statusreports

[D-SOURCE1 Ergebnis](https://github.com/AlOussama/TYNDP_Products/blob/05dd0db3fc15fd6e091b8dd96d854adcedf8302c/docs/current/IOSN_Modul2_Netzaggregation/100_M2_D_SOURCE1_CONSOLIDATED_STATUS_20261111.md) markiert D0–D3 BLOCKED; fortsetzen ausschließlich mit **tatsächlichem** source-owner Zugang:
- [D0 #35](https://github.com/AlOussama/TYNDP_Products/issues/35): TSO 2025/2035 Netzrelease/License/NDA/SHA, 110kV, HVDC/PST/Trafos;
- [D1 #36](https://github.com/AlOussama/TYNDP_Products/issues/36): Pin open PyPSA-Eur v0.6 originale Dateien (nicht nur Metadata), SHA/Lizenz und echtes Zwei-Länder-AC-Mesh. Nur REAL_TOPOLOGY_ONLY, nicht offiziellen IoSN-Dispatch behaupten;
- [D2 #37](https://github.com/AlOussama/TYNDP_Products/issues/37): fünf *extern* bestätigte reale Wetterjahr-IDs, synchrone node MW und neutral balancing, unabhängiger Flow-Witness;
- [D3 #38](https://github.com/AlOussama/TYNDP_Products/issues/38): TSO N-1 Contingencies, normale/Notfallgrenzen, Ausnahmeregeln;
- [R-DATA #39](https://github.com/AlOussama/TYNDP_Products/issues/39): erst bei fixierten Originalbytes/Revisionshashes tatsächlich unabhängig prüfen. Kein M0/M1/Weather-Reader-Code, keine fingierte Zugangserteilung.

**Gate-Ende:** vor MA2 bleibt `MA1_RR1_PENDING` und `OWNER_PENDING`; vor Real `BLOCKED_DATA`; vor ENTSO-E-Konformität `AUTHORITY_UNCONFIRMED`. Alle Arbeitsbranches Draft, main unberührt.
