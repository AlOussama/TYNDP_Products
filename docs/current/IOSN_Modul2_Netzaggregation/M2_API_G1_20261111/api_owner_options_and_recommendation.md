# M2-API-G1 — Kanonische Architektur: Owner-Optionen und Empfehlung

**Status:** `RECOMMEND_C_OWNER_PENDING` · **Stand:** 2026-11-11 · **Verbindlichkeit:** entscheidungsreifer Entwurf, **keine** Owner-Genehmigung.  
**Projekt:** `AlOussama/TYNDP_Products` · **Scope:** ausschließlich M2 API/MA1→MA2-Vertrag; **keine Produktivcodeänderungen**.

## 1. Verifizierte Referenzen

| Dokument/Quelle | Unveränderliche Identität | Evidenz |
|---|---|---|
| Verbindlicher G1-Auftrag 95 | `27dfd810b39e17e6b616a2b0aeb813eb8948d8a0` | [Handoff 95](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/95_M2_API_G1_OWNER_CONTRACT_GATE_20261111.md) |
| Variante A | `70e92ba9e62a320e58227ce9c2f03fad266f44bf` | [A-Code](https://github.com/AlOussama/TYNDP_Products/tree/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official), [Draft PR #13](https://github.com/AlOussama/TYNDP_Products/pull/13) |
| Variante B | `88374dd38792146ca55fa3fe2d4b35dac842c0b9` | [B-Code](https://github.com/AlOussama/TYNDP_Products/tree/88374dd38792146ca55fa3fe2d4b35dac842c0b9/src/tyndp_reduce/m2) |
| R-M2-API | `075c50903b7d51ec19befb4a4b8db1322ae33b2a` | [Review](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md), [unabhängiger CI-Run 43078255397](https://github.com/AlOussama/TYNDP_Products/actions/runs/43078255397) |
| MA2 technischer Zielvertrag | `85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md` @ A | [Dokument 85](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/current/IOSN_Modul2_Netzaggregation/85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) |
| S-GOV / voneinander getrennte R-PHY, R-CLU | `93` @ `27dfd810` | [Konsolidierung](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md) |

R-M2-API: 11/11 unabhängige Paritätstests und 58/58 originale Regressionen bestanden; **nicht** semantisch identische Geräte oder Clusterentscheidungen. R-PHY: vier offene P1; R-CLU: zwei offene P1 und drei P2; diese sechs P1 sind **keine** der neun R-API-P1-Vertragspositionen. Eine unabhängig bestätigte Reparatur derselben integrierten Codeversion liegt in diesen Quellen nicht vor. Realnetz `BLOCKED_DATA`; methodische Autorität der O26-Konsultation `AUTHORITY_UNCONFIRMED`.

## 2. Entscheidung OD-M2-API-01 — Kanonische Schnittstelle

| Option | Inhalt | Auswirkungen auf MA2 / Risiken | Vertragskosten (Review-Schätzung) |
|---|---|---|---|
| **A** | `tyndp_reduce.iosn_official` allein; keine B-Integration | `execute_ma1`, `MA1Result`, NPZ/CSV/Sparse-Operatoren und Handoff 85 bleiben direkt; keine B-Regression als Integrationsfunktion | 2–4 Personentage |
| **B** | `tyndp_reduce.m2` allein kanonisch | Zusätzlicher Produktions-Orchestrator, Umgestaltung von Time/Device/Flow-/Country-Semantik, neuer MA2-Export und Handoff-85-Migration; hohes ungewolltes Semantikrisiko | 8–14 Personentage |
| **C (empfohlen)** | **A einzige Kanonik; B unabhängiger Parity-Oracle; optionale explizite, einseitige B→A-Konverter** | B niemals direkte MA2-API, keine Fusion; Port nur in verlustloser, vollständig nachgewiesener Teilmenge; MA2-Laufpfad darf vom optionalen B-Konverter nicht abhängen | 4–7 Personentage |

Die Personentage sind unvalidierte Engineering-Schätzungen **nur** der Schnittstellenarbeit; sie umfassen keine Echt-Europa-Skalierung, Datenakquise, MA2-x/c0 oder MA3. Option C gilt **nur als TECHNICAL_RECOMMENDATION**. Keine automatische Umstellung des Produktionscodes. Sollte A gewählt werden, ist der MA2-Pfad ohne B-Adapter gültig; sollte B gewählt werden, wird der bestehende Entwurf **nicht** stillschweigend umdefiniert, sondern zunächst neu vorgelegt.

## 3. Weitere zu bestätigende Owner-Entscheidungen

| Entscheidungs-ID | Wahlmöglichkeiten | Technische Empfehlung | Ohne Bestätigung |
|---|---|---|---|
| `OD-M2-API-02` — HVDC-MA2-v1 | `STRICT_LOSSLESS` / `SIGNED_LOSSES_WITH_NEW_DEVICE_GATE` | **STRICT_LOSSLESS** (nur `p0=-p1` mit expliziter MW-Orientierung), asymmetrisch/lossy `UNSUPPORTED_SEMANTICS` bis eigener Physik-/Source-/Solver-Gate | kein lossy Port |
| `OD-M2-API-03` — beobachtete reale AC-Flüsse | `FORCE_DC_EQUALITY_AT_1E-6_MW` / `SEPARATE_MODEL_DISCREPANCY_QA` | **SEPARATE_MODEL_DISCREPANCY_QA**; gehashte reale beobachtete Flüsse sind ein eigenständiges Qualitätsorakel, nicht mathematisch gleich der DC-Näherung | keine harte Gleichheitsfiktion |
| `OD-M2-API-04` — Screening/Schutz | `NOMINAL_EXACT_WITH_IMPLICIT_PROTECTION` / `AUDITED_CLASS_AND_PROTECTION` | **AUDITED_CLASS_AND_PROTECTION**; 380→400 und 220→225 nur explizit belegt; keine unprotokollierte Class-0-Ausnahme; validiertes Critical-Line-Union-/Schutzledger | keine Null-Protection als stiller Default |
| `OD-M2-API-05` — Freigabegrenze | `DOC_GATE_ONLY_NO_MERGE` / `ADDITIONAL_IMPLEMENTATION_AUTHORIZATION` | **DOC_GATE_ONLY_NO_MERGE**; allein Dokumentation, keine Code-Migration, kein Merge, kein MA2-Run | weiterhin `NOT_AUTHORIZED` |

**Nachgelagerte Umsetzungseinstellungen (keine voreiligen Normbehauptungen):** kritische Überlast-MWh-Schwelle und Year-Weights, Screening-Class-Ausnahmekatalog, Einheitenkonvertierung und Geräteprovenienz, RNG-/Tiebreak, Solver-Toleranzen, RAM/IO-Limits, fixierte Monitorgruppen und Train/Selection/Holdout-Blöcke werden als projektinterne **I-Entscheidungen** versioniert. Die konkrete Schwelle ist nicht allein aus dem API-Review beweisbar; `THRESHOLD_PENDING` ist kein zulässiger produktiver Schutzmodus. Details im `api_v1_contract.md`.

## 4. Reconciliation-/Implementierungsgrenze

**Zwingend vor MA2-Codebeginn:** dokumentierte Ownerwahl A/B/C; Abnahme des genau einen `M2.MA2Input.v1`-Vertrags (oder expliziter B-Neuverhandlung); kanonische Quota-/Screen-/Protection-/Neutral-Dispatch-Policy; dispositionierte API-P1-01..09; vier PHY- und zwei CLU-P1 nach W-PHY/W-CLU-Fix **unabhängig** re-reviewed und P1=0; identitätsfestes G05-Gate; Code-/Output-/Source-SHA. Ein Dokument-Gate allein ersetzt keine unabhängige Runtime-Freigabe.

**Später / separat:** W-EQ und W-ITER für G06–G08 mit eigenem R-NUM; B-Adapter und B-Vorteile als optionale QA; 37/102 Realwitness, unabhängige Datenfreigabe, ENTSO-E Authority-Gate, MA3 N-1, M0/M1/Weather-Year-Reader. Schutz vor 380/400- und Country-Alias-Fehlern ist trotz optionalem B-Konverter **nicht** optional.

**Präziser Abschlussstatus dieses Entwurfs:** `RECOMMEND_C_OWNER_PENDING`, `CONTRACT_DRAFT`, `NO_MERGE`, `MA2_RUNTIME_NOT_AUTHORIZED`, `REAL_DATA_BLOCKED`. Bitte Entscheidungen nur durch ausdrückliche Project-Owner-Erklärung mit IDs und gewählten Optionen eintragen; die Vorlage `owner_decision_template.md` enthält die dafür nötige Form.

## 5. Zugehörige Dokumente

- [Typisierter A-v1-/MA2-Vertrag](api_v1_contract.md)
- [Sämtliche Befunde und MA2-Pflichten (CSV)](api_compatibility_matrix.csv)
- [Optionaler B→A-Adapter (Design, kein Code)](optional_b_adapter_design.md)
- [Maschinenlesbares MA2-Input-Gate](ma2_input_gate.json)
- [Owner-Entscheidungsvorlage – PENDING](owner_decision_template.md)

**Keine Ownerentscheidung, kein freigegebenes API-Upgrade oder produktives B-Porting aus diesem Dokument ableiten.**
