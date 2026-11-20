# ML-C18 / 15 – Research Validation and Reproducibility Report

**Research timestamp:** 2026-11-20, local Europe/Berlin. **Governance:** NON_NORMATIVE, IoSN D1–D6 unchanged, MD/CL OPEN, `G1=BLOCKED`. No native GEMS/mathspec Component/Study Contract parser, solver model, independent R1–R4 experiment or product certification performed.

## 1 Verifizierter Ausgangsstand und Schreibisolation
| Source | Überprüfter Ref/Commit | Methode/Beobachtung |
|---|---|---|
| Interne ML-C17-Branch | `research/iosn-ml-c17-language-maturity-2026-11-18` @ `c8bbedad390d0ba00604a0f499e79e9cff087138` | GitHub REST `GET branches/<branch>`, `GET commits/<SHA>`; exakt mit Auftrag |
| Interne ML-C17-Tree | `387c78daaf62a8a49d7f6a81d433e7d6be07d5dc` | GitHub commit tree, 420 Entries; C17/C08 Artefakte per pinned `fetch_file` gelesen |
| GEMS main | `9c52d63b3b81c72554a13b6d4f2ef702dfdf7b3a` | GitHub branch SHA; 626 Tree-Entries; Source docs/library/test examples geöffnet; extern read-only |
| mathspec main | `5f1464c334c1012cdee2947d4d55b4d1d6bef40a` | GitHub branch SHA; 507 Tree-Entries; Source docs/code/test files geöffnet; extern read-only |
| Power-Agent/PowerSkills main | `636102954ff9522e7b161cbb2e3863746afa78cc` | GitHub branch SHA; PyPSA, operations planning and interconnection impact SKILL.md gelesen, **engineering workflow evidence only** |
| Research branch | `research/ml-c18-general-study-contract-2026-11-20`, from verified C17 commit | Github `create_branch` confirmed; subsequent `create_file` writes confined to `Modelling_Language/study_contract_language/workstreams/ML_C18_general_contract_language_research/` |

Keine Veränderung der älteren `Modelling_Language/iosn_formal_specification/**`-Dateien vorgenommen.

## 2 Verifikation der Phasenreihenfolge
1. `01_study_contract_language_requirements.md` mit den vorgeschlagenen 42 SLR in fünf Bereichen vor dem Sprachenvergleich committed.
2. `02_requirements_and_metrics_matrix.csv` mit K01–K17 operational definitions/method/evidence/limits und Freeze research-r1 unmittelbar danach committed, vor ersten K-Scorings.
3. Versionierte GEMS-/mathspec-Dokumentation und echte `src/`/`tests/`-Inhalte untersucht und `03`, `04` getrennt committed.
4. Gemeinsame Referenzfälle `05`/`07` und `06` Vergleich mit separaten Q/E Bewertungen; kein Score-Average.
5. Erst nach Vergleich Source-Review und Bewertung des existierenden Kerns in `08`, Reuse in `09`, Multimodel in `10`, Architektur in `11`, KI-internem Review in `12`, Decision Brief in `13`, Roadmap in `14`.

## 3 Tatsächlich ausgeführte strukturierte Source-/Dokumentationschecks
Per GitHub API auf neuem Forschungsbranch wurden die folgenden automatischen Assertions **tatsächlich** in einer JS-Prüfung ausgeführt:
| Assertion | Beobachtung | Status |
|---|---|---|
| 01–14-Dateien vorhanden | Directory listing: **14** Dateien plus `tools/` vor Erstellung dieses Berichts | PASS |
| Requirements rows | **42** `"SLR","SLR-XX"`-Zeilen im Matrix-CSV | PASS |
| Metrics rows | **17** `"METRIC","KXX"`-Zeilen im Matrix-CSV | PASS |
| Evaluation rows | **17** separate `"KXX"` Zeilen in `06` | PASS |
| Reference cases | **10** `### RC01...` bis RC10 Überschriften in `07` | PASS |
| Counterexamples | **10** positive und **10** negative pro-RC Felder in `07` | PASS |
| Adversarial Review | **20** nummerierte KI-interne R-01–R-20 Befunde in `12` | PASS |
| F1–F15 research answers | **15** nummerierte Fragen in `13` | PASS |
| Numeric script assertions | **27** `ck(...)` Assertions in `tools/synthetic_microchecks.py` | PASS |
| Native test status correctly declared | `NATIVE_PARSED=NO` in `07`, `NOT_EVALUATED` in `06` | PASS |

Die Anzahl von Dateien im fertigen Repository **soll 15 + tools/** betragen, sobald dieser Bericht geschrieben wurde; eine finale API-Verifikation erfolgt nach dem Commit. Diese Checks belegen **strukturelle Vollständigkeit und Kennzeichnung**, nicht fachlich-semantische Richtigkeit sämtlicher 42 SLRs.

## 4 Tatsächlich ausgeführte eigene synthetische Mathematik-Microchecks
**Reproduzierbares Testartefakt:** `tools/synthetic_microchecks.py` (3.982 Byte), zusätzlich im Arbeitscontainer unter `/mnt/data/ml_c18_synthetic_microchecks.py`; lokaler Python-Befehl:

```bash
python /mnt/data/ml_c18_synthetic_microchecks.py
# ML_C18_SYNTHETIC_MICROCHECKS: 27 / 27 PASS
```

**Datei-SHA256:** `01a05d4dda081a396395dcffd67d9c4b48e397774b69abcf17889e349c52c25d` (lokaler `sha256sum`-Check); Python + NumPy verwendet, mit einfachen analytisch/synthetisch definierten Inputs.

| RC | Mathematische Kontrollgegenprobe | Eigene beobachtete Ergebnisgrenze |
|---|---|---|
| RC01 | 2 MW × 0,5 h = 1 MWh; 90% Ladeeffizienz = 0,9 MWh; andere State-Coordinates mit gleicher Energie | Unit-/Rechenwitness, kein Speicheroptimierer |
| RC02 | 10 MWh Gesamtenergie bei 2×4 MWh Mobilitätsbedarf; frühes EV hat dennoch 0 MWh; V2G-Vorzeichentest | Aggregat gesamt erfüllt, individuelle Dienstpflicht verletzt |
| RC03 | 1000 kWh/h ÷ 50 kWh/kg = 20 kg/h H2; LHV-Basis 33,33 kWh/kg synthetisch | Conversion-Orakel, nicht validierte Stack-Dynamik |
| RC04 | 100 kg H2 − 10 kg/h × 2 h = 80 kg; elektrische Energie durch η=0,55/LHV begrenzt | Ledger-Witness, kein reales H2-Netzmodell |
| RC05 | 3-Bus-DC triangle, KCL/KVL, Angle/Cycle/PTDF und absichtlicher circulation flow | **Angle=Cycle=PTDF = [0,33333333; 0,33333333; 0,66666667]**; negative circulating flow erfüllt KCL, verletzt KVL |
| RC06 | ganzzahlige 3×50 MW modular gültig, 0,3 Module unzulässig | Granularitätswitness, kein MILP |
| RC07 | Erststufeninvestition vor Szenarioinformation gleich über Szenarien, Gegenfall nicht | Nichtantizipativitätswitness, kein Multi-stage Model |
| RC08 | CAPEX 100 € + 10 €/MWh × 2 MW × 0,5 h = 110 €; fehlende Δt korrumpiert KPI | Kostenaggregation, kein CBA-Modell |
| RC09 | gleiche `case_1`-Referenz vs verschachtelte inkompatible case IDs | Reference equality, keine autoritative N2E Methodik |
| RC10 | Zwei Modelle liefern verschiedene Kosten, aber gleiche Maßnahme X als günstigstes Ergebnis | Demonstration nichtidentischer Outputs mit gleichem Ranking, keine gemessene Robustheit |

**Ergebnis:** `27/27 PASS` auf selbst entworfene, explizit synthetische Rechenfälle. Das ist keine mathematische Vollständigkeitsbehauptung, keine GEMS-/mathspec-Laufzeittestbestätigung, keine statistische R1–R4-Robustheit und keine unabhängige fachliche Auditierung.

## 5 Fremde, aber tatsächlich vorhandene Code-/CI-Evidenz
- **mathspec GitHub CI:** `https://github.com/energy-models/mathspec/actions/runs/44263210102` auf SHA `5f1464c334...`: Status success, Job "CI" mit Steps `Run pytest`, Linting, Build docs, LaTeX compilability jeweils success. Die Sprachtests in `tests/test_parser.py`, `tests/test_validation.py` enthalten echte positive/negative Spracheingaben. Klassifikation `I_IMPL + T_EXISTING + T_CI_E3` für *mathspec native Sprachfunktion im eigenen Testumfang*, **nicht** E4 für unsere gemeinsamen RCs.
- **GEMS GitHub Actions:** `https://github.com/AntaresSimulatorTeam/GEMS/actions/runs/43884814876`, checked SHA `9c52d63b...`: success für "Check Antares Simulator Update"; Job "E2E Tests against Antares v10.2.0" **skipped**. E2E Python test files liegen im Repository, darunter `tests/e2e_tests/test_pypsa_eur_tutorial.py`; sie wurden in ML-C18 weder installiert noch ausgeführt. Klassifikation `D_DOC + I_EXAMPLES + T_EXISTING`, **nicht** ein durchgeführter E2E-Nachweis.
- **ML-C17:** 20/20 Source-Struktur- und 26/26 boolesche Micro-Fixtures sind im früheren `evaluation_validation_report.md` reported, **nicht** als hier erneut ausgeführte 46 Checks auszugeben.
- **Tool-/Package installations:** Kein natives `GemsPy`, `Antares-Simulator` oder `mathspec` Testpaket wurde für die RCs im Container installiert und aufgerufen. `PARSER_RC01_RC10 = NOT_EXECUTED`.

## 6 Forschungs- und Quellenlücken
**Power QA Question Answers:** Projekt-Dateisuche fand keine bereitgestellten Files; öffentliches `Power-Agent/PowerQA` Repository nicht verfügbar (GitHub API 404), andere QA-Quelle nicht belastbar identifiziert. Deshalb `POWER_QA_SOURCE=NOT_IDENTIFIED`. Inhalte **nicht erfunden**, keine externen Antworten als Evidenz zitiert. Power-Agent/PowerSkills direkt mit Pfaden/SHA verwendet.

**N2E-CBA-Methode:** Konkrete normative Methodikquelle für N2E konnte nicht zuverlässig zugeordnet werden; breit gestreute Suche nach dem Akronym ergab fachfremde Treffer. `N2E_CBA_METHOD_AUTHORITY=NOT_IDENTIFIED`. UC2 bleibt methodisch generische synthetische CBA-Forschungsinstanz mit Owner-TBD, nicht falsche ENTSO-E-N2E-Verbindlichkeit. Spezifische Netzplanungs-Methode ebenso nur nach eindeutiger Quelle zu normieren.

**Blind-Handoff:** Kein unabhängiger Model-Author, keine kontrollierte Authoring-Time-Study, kein native Proof-of-Representation und kein externally independent Audit. Für K17 überall `NOT_EVALUATED/E0`, für K02–K09 keine E4/E5.

## 6a Nachträgliche Library-/Power-Agent-Primärquellenprüfung
Nach Erfassung der ersten Quellen wurde eine **Library-Datei** `PowerAgent_Wissensbasis_Architekturreview_2026-11-17.md` (Research Review vom 17.11.2026) zugänglich und als **sekundärer technischer Reuse-Index** gelesen. Primärquellen auf GitHub wurden dazu eigens gegengeprüft:
- Power-Agent/PowerMCP main `3510a884694a563cd22234522347f9e4a5ed82eb`: README, PyPSA/README; PowerIO IR Gen2 `pio-ir`, typed data/fidelity, PTDF-Fähigkeit auf PowerIO-Ebene ≠ noch geplantes generisches PyPSA-MCP-`calculate_ptdf`.
- Power-Agent/PowerWF main `a3c437146e7263a45db940edc5e4c66a4cd170cf`: `cross_engine_validation/README.md` mit `StudySpec`, two-engine data isolation, comparator outcome semantics; Tests dokumentiert mit Fake-MCP-Adaptern, keine Live-Runtime in ML-C18.
- Power-Agent/PowerAgentBench main `77fe638482af94dd20ce28bfa4301658660d283d`: `benchmarks/steady/level_3/README.md` beschreibt unabhängig reproduzierbare RestoreBench-Scorer- und Dataset-Versionierung, kein generischer Study Contract.
- Power-Agent/PowerFM main `4c6e9b3dd1e035d7abf8c526b2947380b6667fa3`: Quellinventar, kein verifizierter eindeutiger Beleg für separat angefragte `Power QA Question Answers`-Wissensbasis.

Die 09-Reuse-Matrix wurde um diese drei **pinned** Reusezeilen ergänzt und ein separater Quellnachweis `sources/poweragent_cross_engine_reference.md` angelegt. Alle Sourceprüfungen sind **D_DOC / I_SOURCE**; `POWER_AGENT_RUNS_EXECUTED = 0`, **QA-Quellenidentität bleibt unresolved**. Zuvor genannter Hinweis, dass keine *Projektdateien* gefunden wurden, ist mit der später erfolgreich gefundenen **Library-Datei** zu unterscheiden. Diese Ergänzung ändert die 27 numerischen Microchecks, K01–K17-Auswertung und E0–E5-Transparenz nicht.

## 7 Fehler-/Evidenzstatus und Urteil
| Prüfebene | ML-C18-Ergebnis | Zulässige Aussage |
|---|---|---|
| Repository identity/branch isolation | VERIFIED | Reproduzierbare Quellen, isolierter Researchbranch |
| Requirement/K metric freeze | PASS structure | Vergleich wurde nach Forschungsmetriken aufgebaut, keine Owner-Freigabe |
| Source/Implementation review | PASS source inspection | Tatsächliche vorhandene Konstrukte und Testquellen identifiziert |
| Native RC language syntax | NOT_EXECUTED | Keine konkrete RC-YAML als erfolgreich parsed behaupten |
| Synthetic numerical semantics | PASS 27/27 | Kleine definierte Fach-/Negativorakel stimmen in Python |
| Semantic conformance independent implementations | INSUFFICIENT_EVIDENCE | K02/K03/K05/K06 müssen nativ/extern geprüft werden |
| Empirical multi-model R1–R4 | NOT_EXECUTED | Nur Studienprotokoll, keine gemessene Robustheit |
| Human-independent audit and normative approvals | NOT_PERFORMED | Kein Audit oder G1-Owner-Freigabe |

**Validation report verdict:** `RESEARCH_PACKAGE_SOURCE_AND_STRUCTURE_VALIDATED`, `SCIENTIFIC_LANGUAGE_CONFORMANCE_UNPROVEN`, `ARCHITECTURE_DECISION_DEFERRED`. Keine Möglichkeit, Originalmodell-/Solver-/Realdaten-Konformität aus erfolgreichem Parser/CSV-Check abzuleiten. **G1=BLOCKED, D1–D6 unverändert.**