# S-GOV-M2 — Konsolidierung fünf unabhängiger Rückläufe & nächster Makroplan

**Projekt:** AlOussama/TYNDP_Products  
**Stand:** 11.11.2026  
**Modus:** Read-only-Faktenkonsolidierung, dokumentarischer Handoff. Keine Release-/Merge-/MA2-Runtime-Freigabe durch diesen Bericht.  
**Verifizierter Prüfgegenstand:** Draft PR #13, Implementierungs-HEAD \`70e92ba9e62a320e58227ce9c2f03fad266f44bf\`, Code-Freeze \`0254d867a34b66ec7b56c90225605d29ea328916\`.  
**Unveränderliche Modulgrenze:** Ausschließlich M2 Netzaggregation/-reduktion. M0/CGMES, M1/PECD und externe Auswahl der fünf Wetterjahre bleiben unberührt.

## 1. Fünf getrennte, veröffentlichte Rückläufe

| Auftrag | Verifiziertes Evidence-HEAD | Ergebnis | Konsequenz |
|---|---|---|---|
| R-M2-MA1-PHY | \`c004e5330df2a018e567c8ef955ef2fc9d71e0ea\` | **REPAIRS_REQUIRED**, 0 P0, **4 P1** | W-PHY repariert; unabhängiger R-PHY replayt neuen SHA |
| R-M2-MA1-CLU | \`7d7d07d7af5966ddc26d0be1100a69013763d2e8\` | **REPAIRS_REQUIRED**, 0 P0, **2 P1 + 3 P2** | W-CLU repariert; R-CLU replayt neuen SHA |
| R-M2-API | \`075c50903b7d51ec19befb4a4b8db1322ae33b2a\` | **RECOMMEND_A_CANONICAL_WITH_LIMITED_ADAPTER**, Owner-Entscheidung offen | Option C als **Empfehlung**, nicht angenommener Freeze |
| M2-D-REAL | \`6a8262f128ae3dd7e108afe2ade09028ea4f651f\` | **BLOCKED_DATA** | Source Acquisition D0–D3 parallel, D4 unabhängig nach Manifest |
| R-M2-METH | \`754a79e11370dca2c25f1102d83ced5beb251522\` | **AUTHORITY_UNCONFIRMED**, keine positiv nachgewiesene neue M2-Norm | O26-Konsultationsbaseline weiter **nur wissenschaftlich**, kein official PASS |

**Quellen / exakte Reports:**

- [R-PHY 87](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md), [findings JSON](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/R_M2_MA1_PHY_FINDINGS_20261111.json), [CI 43077807614](https://github.com/AlOussama/TYNDP_Products/actions/runs/43077807614): **57 passed, 4 strict-XFAIL**. XFAIL sind reproduzierte offene Fehler, **keine** bestandene Reparatur.
- [R-CLU 87](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md), [findings JSON](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/88_R_M2_MA1_CLU_FINDINGS_LEDGER_20261111.json), [CI 43078445311](https://github.com/AlOussama/TYNDP_Products/actions/runs/43078445311): **36 passed einschließlich Defekt-Reproduktion**, keine Reparatur.
- [R-API Architekturvergleich](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md), [CI 43078255397](https://github.com/AlOussama/TYNDP_Products/actions/runs/43078255397): 11 unabhängige Parity-Tests, 58 originale Regressionstests, Unterschiede bei HVDC-Verlusten, Zeitachsen, 380-kV-Klassifizierung, Trafo-Phasen, Clustering.
- [D-REAL 89](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/89_M2_D_REAL_GAP_GATES_AND_WITNESS_2026_11_11.md), [Readiness 90](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/90_M2_D_REAL_READINESS_MATRIX_2026_11_11.json), [D0–D4 Handoffs 92](https://github.com/AlOussama/TYNDP_Products/blob/6a8262f128ae3dd7e108afe2ade09028ea4f651f/docs/current/IOSN_Modul2_Netzaggregation/92_M2_D_REAL_ACQUISITION_HANDOFFS_2026_11_11.md).
- [R-METH 88](https://github.com/AlOussama/TYNDP_Products/blob/754a79e11370dca2c25f1102d83ced5beb251522/docs/current/IOSN_Modul2_Netzaggregation/88_M2_INDEPENDENT_METHODOLOGY_AUTHORITY_DELTA_REVIEW_2026_11_11.md), [Draft PR #30](https://github.com/AlOussama/TYNDP_Products/pull/30).

**Dokumentkollision:** Die Kennzeichnungen 87/88 wurden auf *unterschiedlichen unverheirateten Review-Branches* wiederverwendet. Sie sind nicht austauschbar, nicht Teil des PR-#13-HEAD und dürfen **nicht** per Dateinamen allein zusammengeführt werden. Diese S-GOV-Dokumentation bekommt einen getrennten 93+-Namensraum.

## 2. Bestätigte sechs P1 – keine Doppelzählung von R-API-Schnittstellenrisiken

| ID | Befund | Wissenschaftlich-technisches Risiko | Worker |
|---|---|---|---|
| PHY-R01 | Frozen Dataclasses behalten caller-owned mutable Listen | TOCTOU/Fingerprint-/Topologie-Mutation | W-PHY |
| PHY-R02 | \`lossless="False"\` ist truthy und wird als verlustlos angenommen | unerlaubte HVDC-Modellsemantik | W-PHY |
| PHY-R03 | \`in_service="False"\` wird als eingeschaltete Leitung behandelt | falsche AC-Konnektivität | W-PHY |
| PHY-R04 | \`atol_mw=inf\` und gefährlich große endliche Toleranz umgehen KCL/Islandbilanz | physikalisch ungültige Referenz akzeptiert | W-PHY |
| R-CLU-001 | Greedy Protected-Cut-Bildung deklariert realisierbare Fälle als unmöglich: 10/1804 feasible Fälle bei erschöpfender vier-Knoten-Enumeration | falsche Infeasibility statt alternative Merges | W-CLU |
| R-CLU-002 | echte nominale 400-kV-Leitung mit \`screening_class_kv=0\` wird still nicht bewertet | Verschweigen von Überlastungen | W-CLU |

**Weitere R-CLU P2:** R-CLU-003 konsumierbarer Generator verfälscht Protected-Line-Hash; R-CLU-004 UK-Seitenquellenänderung wird akzeptiert; R-CLU-005 viele Raw-Aliase pro Gebiet benötigen dokumentierte quellenerhaltende Upstream-Normalisierung, **ohne** NI/UK-Verschmelzung und ohne Änderung an M0/M1.

R-API-P1-01..09 sind **zusätzliche Vertrags- und Kompatibilitätsrisiken** (z.B. B 380-kV, asymmetrische HVDC-Verluste, beobachtete AC-Flüsse, Protection-Policy, Speicher/I/O, Tap), **keine neun zusätzlich bewiesenen Fehler der Linie A**. Sie sind in der API-Gate-Matrix getrennt abzuarbeiten.

**Positive Evidenz:** Die R-PHY-Ersatzreferenz auf 10 Knoten/3 AC-Islands ergab KCL-Maximalresiduum 1.42e-14 MW und unabhängige Oracle-Differenz 2.71e-12 MW; 1001-Bus-Sparse-Chain getestet. R-CLU bestätigte korrekte Quoten, Connectedness, A_z Γ=P A_d und 37/102-Budget bei gültig zurückgegebenen Lösungen. Kein kompletter Europanetz-Nachweis.

## 3. Statusmatrix und wissenschaftliche Scope-Grenze

| Gate | Status am 11.11.2026 | Weiterarbeit |
|---|---|---|
| G01–G05 bestehende MA1-CI | **synthetic code tests pass, independent review REPAIRS_REQUIRED** | P1-Reparatur + eigenständiger Re-Review |
| G11 | **PARTIAL_LOSSLESS_DC_ONLY** | Extended-Device-Semantik/Source-Oracle vor Real |
| API Contract | **Option C empfohlen, OWNER_PENDING** | A-Kanonik nur nach ausdrücklicher Owner-Entscheidung |
| O26 Methodik-Autorität | **AUTHORITY_UNCONFIRMED** | O26 als wissenschaftliche Konsultationsbaseline; MD-01, MD-03, MD-13 klären |
| Real Grid/Data | **BLOCKED_DATA** | D0–D3 parallel, D4 nach Fixierung |
| MA2 G06–G08 | **NOT_IMPLEMENTED / NOT_AUTHORIZED_FOR_RUNTIME** | nur isolierte Dokument-/Fixture-Vorbereitung vor Gate |
| MA3 G09–G10 | **NOT_IMPLEMENTED** | spätere Stufe; methodische Sonderfälle können jetzt spezifiziert werden |
| PR #13 / main | **DRAFT / UNMERGED** | **NO_MERGE_NOW** als Empfehlung, bestehender Zustand unverändert |

**Unveränderliche Grenzen:** Ein gesamteuropäisches Netz mit länderreinen Clustern (37 Label, 102 Zonen nur bei vollständiger Geographie), gemeinsame Referenzflüsse, 225/400-MWh-Screening, fünf unveränderte externe Projektjahre (nicht als offizielle Zahl deklariert), später x/c0-KVL und vier N-1-Kapazitäten. Kein M0-CGMES-/M1-PECD-Reader und keine Wetterjahrselektion in M2.

## 4. Unmittelbar parallel ausführbare Makros und Folgestufen

### Sofort (keine MA2-Runtime- oder Merge-Freigabe erforderlich)
- **M2-MA1-RP1 — konsolidierter Code-Repair-Makro**: parallele W-PHY/W-CLU-Reparaturen, gemeinsamer W-INT-Test und Branch-Freeze, eigene Regression, unabhängige Reviewer noch nicht selbst als PASS behaupten. **Handoff 94**.
- **M2-API-G1 — Architektur-/Owner-Contract-Gate**: schriftliche Entscheidungsvorlage A/B/C, Option C als Empfehlung, ein einziger kanonischer A-Input v1; optionalen B→A-Adapter **nur designieren**, nicht stillschweigend einführen; Ownerentscheidung einholen. **Handoff 95**.
- **M2-D-SOURCE1 — gebündelte parallele Datenarbeit**: D0 Startnetz, D1 offenes reales Topologienetz, D2 Referenzdispatch, D3 Kontingenzen; D4 unabhängiger Data-Review *nach* Originalbytes. **Handoff 96**.
- **M2-METHOD-G1 — fokussiertes Methoden-/Owner-Entscheidungspaket**: MD-01/03/13/11/12/08, O26 status, keine zweite unverbindliche Recherche und kein pseudonormativer Pass. **Handoff 97**.
- **M2-MA2-PRE — dokumentarische Vorbereitung**: Branchread-only Spezifikation der globalen x/c0-, affinen KVL-, gekoppelte Länder-, fixed-monitor-/Train/Selection/Holdout-Gates, Fixture-/Testdesign; **keine produktive MA2-Implementierung, kein Runtime-GO**. **Handoff 98**.

### Nach Reparatur, eigenen Reviewer-Runs und Owner-Vertrag
- **M2-MA1-RR1 — unabhängige getrennte R-PHY/R-CLU Re-Reviews** auf einem exakten **neuen integrierten** Repair-Code-SHA, nicht dem alten 0254; 4 PHY-XFAIL in normale PASS überführen; 10/1804 False-Blocking auf 0 bringen; P1=0, P2 dispositioniert. **Handoff 99**.
- **S-GOV-M2-GATE**: Zusammenführung der Re-Reviews, MA1-SYNTHETIC-Decision, Owner API C oder andere; weiterhin NO_MERGE bis ausdrückliche Entscheidung.
- **M2-MA2 – Global x/c0 + Coupled-Country Loop**: als produktiver Code-Makro nur nach erfüllter MA1/Owner-API-Gate; Grundlage weiterhin [85](85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md); W-EQ/W-ITER + unabhängiger R-NUM; nur SYNTHETIC, niemals REAL-GO ohne Daten. **Handoff 100 (conditional)**.
- **M2-MA3 – N-1/Vierfachkapazitäten**: nach MA2-Interface/Gate, besondere 99.5-/1-/130-%-Fälle; N-1-Realbetrieb separat. Noch **nicht** Runtime-startbereit.
- **D4 unabhängige Realwitness-Qualifikation**: erst nach tatsächlichen Originalbytes, Eingangsmanifesten und Sourceowner-Nachweisen; D0–D3-Recherchen sind kein Ersatz.

## 5. Präzise Owner-Gate-Empfehlungen (nicht als bereits bestätigt ausgeben)

| Entscheidungs-ID | Empfohlene Option | Wirkung |
|---|---|---|
| OD-M2-API-01 | **C: A kanonisch, optional schmaler B→A-Adapter** | API-Reconciliation-Plan; impliziert keinen Merge |
| OD-M2-REPAIR-02 | **AUTHORIZE_DOCUMENTED_MA1_REPAIRS** | zwei Worker + unabhängige Re-Reviews |
| OD-M2-MA2-03 | **DOCUMENT_AND_FIXTURE_PREP_ONLY_NOW** | keine MA2-Runtime bis positivem GATE |
| OD-M2-METH-04 | **O26_AS_PROVISIONAL_SCIENTIFIC_BASELINE** | konsultativer Quellenstatus sichtbar halten |
| OD-M2-DATA-05 | **AUTHORIZE_ACQUISITION_ONLY** | Zugriff/Lizenzen/Hashes, kein Real-GO |
| OD-M2-MERGE-06 | **NO_MERGE_NOW** | PR #13 bleibt Draft, main unberührt |

**Externe Methodik-Owner-IDs:** MD-01 (adopted/effective Version), MD-03 (x/c0/RMSE/N-1 Orakel), MD-13 (Clustering/Country-Kanonik), MD-11/12 (Originaldaten und Zeit-/Einheitenvertrag), MD-08 (LF/OPF-Modustrennung). Ein Projekt-Owner kann die provisorische wissenschaftliche Implementation wählen, **nicht** eine nicht belegte ENTSO-E-Verabschiedung ersetzen.

## 6. Definition of Done und No-Go

**MA1_SYNTHETIC_QUALIFIED erst wenn:** nachweisbar unabhängige R-PHY/R-CLU Replay-Entscheidungen des **gleichen integrierten Repair-SHA** ohne offene P0/P1, alle alten und neuen Tests tatsächlich PASS, heuristische Feasible-Gegenbeispiele repariert, Screening-Exklusionen nachweisbar, P2 dispositions dokumentiert, Owner/Contract-Gate nicht widersprochen.

**MA2 runtime** bleibt bis zu MA1-Gate und Owner-API-Entscheidung **NOT_AUTHORIZED**. Der Nutzer kann separate Dokument-/Isolated-Fixture-Vorbereitung starten, nicht als eigentliche MA2-Freigabe deklarieren.

**REAL_QUALIFIED** benötigt zusätzlich Originalbytes/Hashes, reale 37/102-Topologie, synchronen Dispatch, neutrales Kalibrierungsset, physische Lastflussorakel, Rating-/Kontingenz-/TSO-Nachweise, 5 reale feste Jahre sowie unabhängigen D4-Review; Source-Catalogue-URLs reichen nicht.

**Kein** impliziter PR-Merge, kein main-Push, keine automatische Owner-Entscheidung, keine Änderungen an M0/M1/Jahresselektion.
