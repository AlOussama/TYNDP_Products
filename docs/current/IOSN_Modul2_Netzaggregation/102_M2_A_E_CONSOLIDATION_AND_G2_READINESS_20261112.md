# S-GOV-M2 G2 – Konsolidierung der fünf abgeschlossenen Makros A–E

**Datum:** 2026-11-12. **Scope:** ausschließlich Modul 2 / Netzaggregation und Netzreduktion. **Status:** EVIDENCE_CONSOLIDATED / MA1_RR1_READY / OWNER_GATE_PENDING / DATA_BLOCKED / MA2_CODE_NOT_AUTHORIZED. **Modus:** Dokumentation, keine Runtime-, Merge- oder Norm-Freigabe.

## 1. Gepinnte Rückläufe (alle Commits und Dateien auf GitHub verifiziert)

| Auftrag | Unveränderlicher HEAD, Kernartefakte | Belastbare Aussage | Offene Freigabe |
|---|---|---|---|
| A – M2-MA1-RP1 | `fb201ef5f120f64696dea9aa99f77ece77546f9a`, [Report 101](https://github.com/AlOussama/TYNDP_Products/blob/fb201ef5f120f64696dea9aa99f77ece77546f9a/docs/current/IOSN_Modul2_Netzaggregation/101_M2_MA1_RP1_INTEGRATION_AND_RR1_HANDOFF_20261111.md), [Draft PR 41](https://github.com/AlOussama/TYNDP_Products/pull/41), [Worker findings](https://github.com/AlOussama/TYNDP_Products/blob/fb201ef5f120f64696dea9aa99f77ece77546f9a/docs/current/IOSN_Modul2_Netzaggregation/M2_MA1_RP1_WORKER_FINDINGS_20261111.json) | W-PHY vier P1 und W-CLU zwei P1 sowie P2 003/004 `FIXED_BY_WORKER_TEST`; opt-in Country alias resolver gebaut, original source attestation offen. [Exact-SHA Push CI 43113044448](https://github.com/AlOussama/TYNDP_Products/actions/runs/43113044448): **66 fokussierte + 92 alle PASS**, 0 failed/error/skipped; 15 synthetische Evidenzdateien | **R-PHY-RE und R-CLU-RE nicht ausgeführt**; PR41 Draft, keine Review-Einreichung, kein Owner-/Merge-/MA2-Go |
| B – M2-API-G1 | `ed42d051a7234f7f062d94d06291f66e56657bbc`, [API-G1 Owner Option](https://github.com/AlOussama/TYNDP_Products/blob/ed42d051a7234f7f062d94d06291f66e56657bbc/docs/current/IOSN_Modul2_Netzaggregation/M2_API_G1_20261111/api_owner_options_and_recommendation.md), [Input Gate](https://github.com/AlOussama/TYNDP_Products/blob/ed42d051a7234f7f062d94d06291f66e56657bbc/docs/current/IOSN_Modul2_Netzaggregation/M2_API_G1_20261111/ma2_input_gate.json) | **Option C empfohlen**: `iosn_official` allein kanonisch; optionaler, einseitig typisierter und fail-closed B→A-Adapter; Draft v1 Schnittstelle und Risiko-/Testmatrix | `RECOMMEND_C_OWNER_PENDING`; kein beschlossenes API Freeze; kein Adapterporting |
| C – M2-D-SOURCE1 | `05dd0db3fc15fd6e091b8dd96d854adcedf8302c`, [Data status 100](https://github.com/AlOussama/TYNDP_Products/blob/05dd0db3fc15fd6e091b8dd96d854adcedf8302c/docs/current/IOSN_Modul2_Netzaggregation/100_M2_D_SOURCE1_CONSOLIDATED_STATUS_20261111.md), [D0–D3 issues 35–38](https://github.com/AlOussama/TYNDP_Products/issues/35) | 37/102-Quotentabelle SHA256 verifiziert; D1 PyPSA-Eur v0.6 Open-Topology-Metadata als Kandidat; Quellprüfer/DR01–17 und Owner-Action-Handoffs vorhanden | **D0–D3 BLOCKED**: original network, echter D1-Dateireplay, fünf echte Wetter-IDs, Dispatch/neutral, security fehlen; D4 [Issue 39](https://github.com/AlOussama/TYNDP_Products/issues/39) nur nach bytes/manifest |
| D – M2-METHOD-G1 | `c980bbd341b1051257bcf31b0a904dd7937f7241`, [Owner Entscheidungen](https://github.com/AlOussama/TYNDP_Products/blob/c980bbd341b1051257bcf31b0a904dd7937f7241/docs/current/IOSN_Modul2_Netzaggregation/m2_owner_decision_register.md), [Gate Readout](https://github.com/AlOussama/TYNDP_Products/blob/c980bbd341b1051257bcf31b0a904dd7937f7241/docs/current/IOSN_Modul2_Netzaggregation/m2_gov_gate_readout.md), [Draft PR 40](https://github.com/AlOussama/TYNDP_Products/pull/40) | 12 M2 Owner-Entscheidungsfälle samt Optionen/Empfehlungen dokumentiert, Quell-/18 NR-Matrix abgeglichen; keine gesichert verabschiedete/effective spätere ENTSO-E-IoSN-Fassung | `OWNER_PENDING`, `ENTSOE_AUTHORITY_UNCONFIRMED`, übergreifendes G1 weiterhin BLOCKED |
| E – M2-MA2-PRE | `b73bb3c595bff515aeca052f02fc83f72289b5f0`, [Readme und sieben Designdateien](https://github.com/AlOussama/TYNDP_Products/blob/b73bb3c595bff515aeca052f02fc83f72289b5f0/docs/current/IOSN_Modul2_Netzaggregation/ma2_pre_20261112/README.md), [45-Test-G05–08-Matrix](https://github.com/AlOussama/TYNDP_Products/blob/b73bb3c595bff515aeca052f02fc83f72289b5f0/docs/current/IOSN_Modul2_Netzaggregation/ma2_pre_20261112/ma2_test_and_gate_matrix.json) | x/c0, affine KVL, identifizierbare Gauge/rank, coupled-country moves, full global refit, frozen split/fixed monitors, numerische Orakel und 45 **geplante** Tests dokumentiert | **DESIGN_READY_ONLY**, 0 MA2-Tests aus Designmatrix als echte MA2-Implementierung ausgeführt; R-NUM NOT_RUN; Code-GO noch nicht erteilt |

**Achtung doppelte Dokumentnummer 100 auf verschiedenen Branches:** D-SOURCE1 Report `100_M2_D_SOURCE1...` auf Source-Branch ist **nicht** das bedingte MA2-Makro `100_M2_MA2_CONDITIONAL...` auf S-GOV-Branch. Referenziere stets exakte Commit-SHA plus Pfad, niemals nur Dokumentnummer.

## 2. Tatsächlich erfüllte, nicht erfüllte Gates

- MA1 code/worker: **PASS_SYNTHETIC_WORKER_TESTS**, mit gezielten Negativtests, numerischer Fixture und Genauigkeitsorakeln. Die vorherigen 6 P1 sind als Worker-Fix markiert, **nicht als unabhängig geschlossen**.
- **MA1_RR1_READY:** Zwei unabhängige Re-Reviews dürfen sofort auf exakt `fb201ef5f120f64696dea9aa99f77ece77546f9a` starten, jeweils separate Reviewer und SHA-gebundene CI. Keine Review-Freigabe aus den bisherigen Workerläufen ableiten.
- **MA1_SYNTHETIC_QUALIFIED:** PENDING, solange beide Re-Reviews nicht PASS und P0/P1=0 gemeinsam bestätigen. G11 weiterhin `PARTIAL_LOSSLESS_DC_ONLY`.
- **API:** Option C **empfohlen**, noch nicht Owner-entschieden. Feste A-Contract-v1 / B-Adapterpolitik als dokumentierte Empfehlung, noch kein Releasevertrag.
- **Methodik:** `O26` (ENTSO-E Konsultation 25.02.2026) nur als vorläufige wissenschaftliche Arbeitsbaseline, keine normative/Final-Konformität.
- **Daten:** `BLOCKED_DATA`; D1 möglicher offener realer **Topologie**-Pilot ist nicht der offizielle 37/102-Realnetz- oder Markt-Dispatch-/N-1-Witness. D0/D2/D3 erfordern tatsächliche Source-Owner-Aktion/Dateien; D4 erst mit eingefrorenen Originalbytes.
- **MA2:** `MA2_PREP_READY_FOR_GATE`, **nicht** `MA2_IMPLEMENTED`; 45 Fälle sind Design, keine bestandenen MA2-Läufe. **MA2_CODE_NOT_AUTHORIZED** bis RRs und expliziter Ownerentscheidung. MA3 bleibt downstream.
- **Code-/Merge-Grenze:** PR41 Draft/open/unmerged, PR13 Draft/open/unmerged, Main `1595d6d38e77804760612621657721b3699d2fea` bei zuletzt geprüfter Abfrage. Keine M0/CGMES-, M1/PECD-, Wetterjahrselektions- oder Legacy-Änderung.

## 3. Nächste Makros und Startreihenfolge

### Sofort parallel ausführbar (ohne new Code-GO)
1. **RR1-R-PHY – Independent repair re-review**: exact `fb201ef5...`; originale vier P1-Gegenbeispiele als reguläre PASS, KCL/KVL 10 bus, 1001 sparse, immutable fingerprint, 15-file evidence, neuer Reviewer-/CI-SHA; unabhängig von W-PHY, W-CLU, W-INT.
2. **RR1-R-CLU – Independent repair re-review**: same exact `fb201ef5...`; 729 edge-state graphs, 1804 feasible, 0 false-infeasible, 400-kV class0/90 MWh, P2 hash/page/aliases, multi-country; unabhängiger Reviewer-/CI-SHA.
3. **G2-OWNER – Scoped project-owner decision**: Owner bestätigt oder verwirft getrennt Option C/A/B, strict-lossless/QA/screen-policy, O26 als vorläufige wissenschaftliche Grundlage, isoliertes nur-synthetisches künftiges MA2-Go **nach RR1**; v1 I-Parameter erst auf vollständiger testbarer Vertragsgrundlage. Kein Autogo.
4. **D-SOURCE-OWNER – Source acquisition follow-through**: D0 institutionelle Netzrelease-Anfrage, D1 tatsächlich offene Bytes/Lizenzen, D2 fixe Wetterjahr-IDs/nodaler Dispatch/balancierte Neutralreferenz, D3 TSO Kontingenz/Limit; bei fehlendem externem Zugriff `BLOCKED_SOURCE_ACCESS` statt fingiertem Datensatz. R-DATA D4 erst nach Input Freeze.
5. **MA2-PRE-REVIEW (optional)**: unabhängige formale wissenschaftliche Prüfung von x/c0, affiner KVL mit festen Phasenquellen, Gauge/Unidentifiability, globalem Refit und 45 Testorakeln als *read-only*, nicht als MA2 Numerik-PASS.

### Danach nachweisgebunden
- **S-GOV-M2-G2:** beide RR1-Reviews am **gleichen** Repair SHA + API-/Owner-Gate und Datenstatus konsolidieren. `MA1_SYNTHETIC_QUALIFIED` nur mit explizit bestandenen Gateinvarianten; `OWNER_PENDING` separat lassen, nicht still schließen.
- **M2-MA2 code**: [ursprünglicher bedingter Handoff 100](100_M2_MA2_CONDITIONAL_IMPLEMENTATION_MACRO_20261111.md) plus E Design, **erst** nach RR1-Gate und ausdrücklicher Project-Owner-Freigabe für **SYNTHETIC_IMPLEMENTATION_ONLY**; keine Real-Netze oder M0/M1/Weather Änderungen, R-NUM später getrennt.
- **MA3**: erst nach nachweisbarer MA2-Schnittstelle, sicherheitsbezogener Fixturefreigabe; Real-Security erst mit D3/D4.

## 4. Empfohlene, noch **nicht beschlossene** Ownerwahl

- `OD-M2-API-01=C`: `iosn_official` einzige kanonische Schnittstelle, B optional geprüfter, versionierter B→A Adapter.
- `OD-M2-API-02=STRICT_LOSSLESS`, `OD-M2-API-03=SEPARATE_MODEL_DISCREPANCY_QA`, `OD-M2-API-04=AUDITED_CLASS_AND_PROTECTION`, `OD-M2-API-05=DOC_GATE_ONLY_NO_MERGE`.
- `OD-M2-METH-01=O26_PROVISIONAL_SCIENTIFIC_BASELINE` für Forschung; dieser Projektbeschluss ersetzt **niemals** die fehlende ENTSO-E-Methodenautorität.
- `OD-M2-MA2-CODE=DEFER_UNTIL_RR1_AND_API_OWNER_GATE`; `OD-M2-MERGE=NO_MERGE_NOW`.
- Keine festen numerischen x/c0-/RMSE-/Fairness-Produktionstoleranzen ohne testbare I-Wahl, Reviewer- und Owner-Freeze. D0-D3 nicht als Freigabe deklarieren.

**Freigabebeschluss hier: KEINER.** Dokumentation ist eine unabhängige Konsolidierung von bereits veröffentlichten Belegen. Keine unautorisierten API-/Owner-/Methodikentscheidungen oder MA2/MA3-Run-Starts.
