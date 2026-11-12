# ML-C03 — Data and Transformation Verification Cases

**Baseline:** ML-R00 PR #32 `9162def25d22c37b1fbc38f7d80fe929425cc8d2`; R03 87 Objekte/38 T-Vorschläge; R01 M01–M18; [R04 Test Catalogue](../ML_R04_verification/test_catalogue.csv) und [R04 synthetic reference cases](../ML_R04_verification/synthetic_reference_cases/README.md). **TEST-DESIGN_ONLY; NO_ORIGINAL_PAYLOAD_OR_NATIVE_SOLVER_EXECUTION; G1 BLOCKED.** R04-Test IDs, V1–V6, D0–D4-Tiefen, E01–E08 werden übernommen; D4 als Testtiefe darf nicht mit Projektentscheidung D4 (UTC/Einheiten) verwechselt werden.

## 1. Nachweisebenen und Ergebnissemantik

| Ebene | Gegenstand | Erforderliche Quellen/Evidenz | Aktueller Nachweisstatus |
|---|---|---|---|
| V1 Data | Original und abgeleitete Instanzen, IDs, UTC, Einheiten, Quellfreezes, Coverage | E01–E03/Daten-/Metadaten, originale Datei-Hashes | Originaldaten noch nicht qualifiziert |
| V2 Semantic | Carrier-/Netz-/Raum-/Zeitschnitt-/Kandidaten-/Output-Semantik | Prozess-/Daten-/Modell-Semantikref, Negativfälle | Nicht produktiv verifiziert |
| V3 Generated math | Erzeugte Variablen, Zielfunktion, Nebenbedingungen, LF/OPF, gemeinsame x | Gleichungs-/Variablenmanifest E04 | Kein nativer Toolrun |
| V4 Numerical | Feasibility, Residuen, Optionality, alternative Optima, Referenz-Solves | Solver/Nummerik E05 und Owner-Toleranz | Reale numerische Orakel TBD |
| V5 KPI/output | RawResult vs abgeleitete und veröffentlichte Kennzahl/Bedarfe | Raw E06, Formel/KPI E07, Origin/Approval | Formel-/Filterowner TBD |
| V6 Evidence/review | Vollständige Replay-Kette und unabhängige Disposition | Release-/Signatur-/Tool-/Execution-Manifest E01–E08 | Kein unabhängiger Organisation-Review |

`PASS/FAIL/BLOCKED/UNSUPPORTED/NOT_EXECUTED/NOT_APPLICABLE` sind **nur Test-/Claim-Ergebnisse**, getrennt von Source/Data/Owner-Zuständen. Reale Tests werden nicht als PASS behauptet. Ein im ursprünglichen R04-Beispiel erfolgreiches synthetisches Arithmetikorakel ist lediglich `SYNTHETIC_FIXTURE`, nie eine IoSN-Toolkonformität.

## 2. Strukturprüfungen des ML-C03-Crosswalks (in-memory bei Erstellung geprüft)

| Prüf-ID | Prüfalgorithmus / Erwartung | Forschungsstand | Nicht bewiesen |
|---|---|---|---|
| MLC03-S-01 | Katalog eindeutige `B01-D001...D087`: 87 | 87 Zeilen gelesen, 87 IDs | Originaldatenqualität |
| MLC03-S-02 | 67 Dataobjekte haben direkte SR-Relation; 20 sind Process-only | 67/20 rekonziliert | Owner-SR-Abnahme |
| MLC03-S-03 | Über alle Objektzeilen genau 93 direkte Data–SR-Paare und exakt 93 B01-T-IDs | 93/93 zeilenweise paarbar | fachliche Richtigkeit jeder Zuordnung |
| MLC03-S-04 | Alle SR-IDs referenzieren aktive 48 R00-SR, keine SR-012/SR-049 neu | 48 active R00-Matrix, referenzierbar | Normative SR-Freigabe |
| MLC03-S-05 | 35 interne Datenobjekte erhalten mindestens einen R03-Producer-Proposal | 35/35 T-output-Abdeckung | Ausführung und H2-/Filter-Autorität |
| MLC03-S-06 | Einzigartige R03-T IDs auf P00–P17, 38 Einträge | 38/38, alle 18 P | Software-ETL oder Solverausführung |
| MLC03-S-07 | `T_i.outputs ∩ T_j.inputs` ergibt 47 eindeutige Kanten; Toposort erreicht 38 Knoten | 47/47, keine Zyklen | Methodisch vollständige Lifecycle-Abhängigkeiten |
| MLC03-S-08 | Neue Matrix enthält 93+20+35+38+18 = **204** getrennt klassifizierte Records | 204 | Formale/physikalische semantische Konformität |
| MLC03-S-09 | Ausnahme-Register enthält 87 Objektrecords + 21 explizite Prozess- und Cross-Layer-Ausnahmen | 108 | Schließung/Owner-Entscheidung der Ausnahmen |

**Reproduktionsskizze:** RFC4180-CSV parsen; Primärschlüssel/ID-Mengen vergleichen; pro B01-D Zeile `len(direct_SR_ids) == len(original_B01_T_ids)`; `∀t.inputRef, t.outputRef` vorhandenes B01-D-Objekt oder deklariertes `MLR03-I-...`; für jede Producer-/Consumer-Kombination eine Kante; Kahn-Toposort und Anzahl erreichter T-Knoten; P=00..17/Original-SR-IDs erneut prüfen. Dies sind statische Tabellen-/Graphprüfungen, nicht die R04 native Ausführung.

## 3. Ein Prüffall je Prozess inklusive Negativfall

| Prüffall | Prozess | Positiv zu prüfen | Falsifizierender Negativfall | Bezug auf R04-Test IDs über Prozesslink |
|---|---|---|---|---|
| `MLC03-P-P00` | P00 | Owner method-release manifest and actual input freeze | Remove release/approval/hash; status must remain BLOCKED, not 'adopted' | No direct SR — P00 |
| `MLC03-P-P01` | P01 | Three separate Y={2035,2040,2050} scenario run identities | Insert 2030 or cross-year investment dependency; reject | R04-T-SR-002; R04-T-SR-004; R04-T-SR-039 |
| `MLC03-P-P02` | P02 | Exactly five exogenous distinct CY IDs and identical weight vector across study years | Duplicate CY3, change one year's CY2 weight, or impose uniform 0.2; reject/flag | R04-T-SR-004; R04-T-SR-010; R04-T-SR-011; R04-T-SR-040 |
| `MLC03-P-P03` | P03 | UTC interval uniqueness, duration and units, source-specific gap policy | Two local DST hours map to one UTC interval or MW treated as MWh; reject | R04-T-SR-004; R04-T-SR-011; R04-T-SR-040; R04-T-SR-042 |
| `MLC03-P-P04` | P04 | 2035 starting-grid eligible projects, fixed offshore targets, exogenous baseline | Inject unqualified project or endogenous baseline offshore capacity; reject | R04-T-SR-005; R04-T-SR-006; R04-T-SR-048 |
| `MLC03-P-P05` | P05 | Complete bus-to-zone partition and graph connectedness | Duplicate bus, drop bus or disconnect one zone; reject | R04-T-SR-013; R04-T-SR-014; R04-T-SR-015; R04-T-SR-016; R04-T-SR-022 |
| `MLC03-P-P06` | P06 | N−1/PTDF/LODF, directional/seasonal ratings, impedance, mesh, HVDC/PST calibration | Swap +/- direction, drop PST effect or claim numeric quality without oracle; reject/block | R04-T-SR-017; R04-T-SR-018; R04-T-SR-019; R04-T-SR-020; R04-T-SR-021; R04-T-SR-022 |
| `MLC03-P-P07` | P07 | Total eligible zonal allocation with distinct additive and intensive rules | Sum prices directly, double-count demand, drop asset or duplicate zone mapping | R04-T-SR-023 |
| `MLC03-P-P08` | P08 | Carrier-specific power/energy balance, five hydro classes and DSR types | Remove H2 conversion efficiency or flatten Hydro/DSR distinctions; reject | R04-T-SR-007; R04-T-SR-008; R04-T-SR-039; R04-T-SR-041; R04-T-SR-042; R04-T-SR-050 |
| `MLC03-P-P09` | P09 | Candidate class/stage/capacity, directional DC market links, cost units | Model market link as pre-existing mesh branch; combine real/nominal cashflows | R04-T-SR-018; R04-T-SR-024; R04-T-SR-028; R04-T-SR-034; R04-T-SR-035; R04-T-SR-036; R04-T-SR-037; R04-T-SR-038; R04-T-SR-043; R04-T-SR-044 |
| `MLC03-P-P10` | P10 | Shared x_y across all CY and correct Stage-1 Real LF expansion | Introduce independent x_(y,CY) or relax Kirchhoff mesh; reject | R04-T-SR-003; R04-T-SR-024; R04-T-SR-027; R04-T-SR-028; R04-T-SR-029; R04-T-SR-030; R04-T-SR-031; R04-T-SR-035 |
| `MLC03-P-P11` | P11 | Stage-1-to-2 carry F_y including residual capacity and CAPEX accounting | Duplicate stage-1 CAPEX or double-allow used capacity; blocker until owner rule | R04-T-SR-003; R04-T-SR-024; R04-T-SR-027; R04-T-SR-028; R04-T-SR-029; R04-T-SR-030; R04-T-SR-032; R04-T-SR-035 |
| `MLC03-P-P12` | P12 | Separate 2040/2050 storage LP and country/power/energy bounds | Optimize 2035 new storage, use MW as MWh or ignore SOC efficiency | R04-T-SR-003; R04-T-SR-024; R04-T-SR-027; R04-T-SR-028; R04-T-SR-029; R04-T-SR-030; R04-T-SR-033; R04-T-SR-034 |
| `MLC03-P-P13` | P13 | Comparable with/without-portfolio dispatch pairs using internal network caps | Vary other inputs secretly, remove N−1 ratings, flip delta orientation | R04-T-SR-025 |
| `MLC03-P-P14` | P14 | Freeze against *pre-expansion* H2 hourly CY/zone reference, not final LF | Use post-expansion electrolyser time series as B01-D072 or omit baseline run ID | R04-T-SR-009 |
| `MLC03-P-P15` | P15 | Optional OPF only on explicit antecedent and capped by LF selections | Run OPF by default or choose x_OPF > x_LF for any component | R04-T-SR-026 |
| `MLC03-P-P16` | P16 | Raw result lineage distinct from KPI and published SystemNeed, owner filter only | Infer missing KPI formula, assign project approval or silently filter small links | R04-T-SR-001; R04-T-SR-044; R04-T-SR-045; R04-T-SR-046 |
| `MLC03-P-P17` | P17 | Per-claim six-valued R04 status and separated source/math/evidence dimensions | Promote structural/synthetic PASS to global model/owner/G1 PASS | R04-T-SR-047 |

Die Original-R04-Test IDs stammen aus R00 `process_ids_expanded`; ein Zuordnungsjoin ist **keine neue Origin-SR-Verknüpfung**. P00 hat keinen direkten aktiven MA01-SR und erhält dennoch einen Governance-Check.

## 4. Kritische / metamorphe Prüffälle (Design, nicht ausgeführt)

### MLC03-C-01 — CY/weights, StudyYears

**Prüfobjekt und positives Orakel (sobald autorisiert):** Y=2035,2040,2050; w shared across years but not forced uniform. **Negativ-/metamorpher Fall:** Uniform 1/5 override or separate year weights fail semantic profile. **Bezug:** R04 C01/C02, V1/V3. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** BLOCKED for numeric weight release; synthetic design only; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-02 — UTC/time dimension

**Prüfobjekt und positives Orakel (sobald autorisiert):** Same interval's MW×hours matches expected MWh and stays traceable. **Negativ-/metamorpher Fall:** DST overlap or raw MW sum labelled as energy is rejected. **Bezug:** R04 C03; V1. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Original calendar policy TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-03 — Spatial extensive data

**Prüfobjekt und positives Orakel (sobald autorisiert):** Allocation fractions for additively conserved quantities sum to 1 on an exhaustive partition. **Negativ-/metamorpher Fall:** Lost/doubled load on zonal split. **Bezug:** R04 C05; V1/V2. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Accepted tolerance MD-12/13 TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-04 — Spatial nonadditive data

**Prüfobjekt und positives Orakel (sobald autorisiert):** Price, coefficient, factors or means have explicit calculation/denominator. **Negativ-/metamorpher Fall:** Simple summation of nodal mean prices is flagged. **Bezug:** R03 P07, V2. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Weighting policy by data type TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-05 — Reduced electric network

**Prüfobjekt und positives Orakel (sobald autorisiert):** A reference case compares detailed/reduced flows, overload and contingency with declared direction/season. **Negativ-/metamorpher Fall:** Drop LODF contingency, reverse NTC or replace physical mesh with marketlink. **Bezug:** R04 C04/C05, V3/V4. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Reference grid and numerical oracle TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-06 — Market-link model

**Prüfobjekt und positives Orakel (sobald autorisiert):** Expansion candidate is controllable DC link with signed directional NTC and bounds. **Negativ-/metamorpher Fall:** A new candidate inherits physical Kirchhoff relation without methodological justification. **Bezug:** R04 C04, V2/V3. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Exact NTC mapping and cost values TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-07 — Equivalent model representations

**Prüfobjekt und positives Orakel (sobald autorisiert):** Two mathematical encodings have equivalent feasible-set projections and objective/residual behavior. **Negativ-/metamorpher Fall:** Require syntactically identical equations or blindly accept matching CSV. **Bezug:** R04 C06, V3/V4. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Native generator models unexecuted; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-08 — Multiple optima

**Prüfobjekt und positives Orakel (sobald autorisiert):** Distinct but feasible optimal portfolios may both conform if objective/optimality witnesses agree. **Negativ-/metamorpher Fall:** Fail solely on different x vectors despite equal optimum/witnesses. **Bezug:** R04 C07, V4/V5. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Accepted numerical gap/tolerance TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-09 — Stage-1/2 continuation

**Prüfobjekt und positives Orakel (sobald autorisiert):** F_y is explicit and cost/remainder references reconcile. **Negativ-/metamorpher Fall:** Double-pay CAPEX for already selected Stage-1 x or ignore partial x. **Bezug:** R04 SR-003/032, V3/V4. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** MD-07 Owner transition TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-10 — Storage conservation

**Prüfobjekt und positives Orakel (sobald autorisiert):** SOC energy is integrated over interval with charge/discharge efficiency and bounded both MW/MWh. **Negativ-/metamorpher Fall:** MW↔MWh swap or free energy creation by SOC update. **Bezug:** R04 C03, M13. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Duration/terminal SOC Owner rules TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-11 — Hydro five classes

**Prüfobjekt und positives Orakel (sobald autorisiert):** Run-of-river, pondage, reservoir, open-loop and closed-loop pumped classes distinct. **Negativ-/metamorpher Fall:** Flatten run-of-river and reservoir seasonal water storage. **Bezug:** M14; V2/V3. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Hydrological source calibration TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-12 — Hydrogen and DSR balance

**Prüfobjekt und positives Orakel (sobald autorisiert):** Electricity/H2 exchange converts on declared HHV/LHV and no implicit H2 network expansion; DSR class explicit. **Negativ-/metamorpher Fall:** Convert 1 MWh_e to 1 MWh_H2 without efficiency or silently invest in pipeline. **Bezug:** M15/M16; V2/V3. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** MD-10/16; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-13 — Frozen H2 reference run

**Prüfobjekt und positives Orakel (sobald autorisiert):** There is a source/run witness for pre-expansion B01-D072, all (Y,CY,t,zone) values frozen. **Negativ-/metamorpher Fall:** Use P12-final post-expansion output or leave baseline reference null. **Bezug:** R03 T14-00/T14-01; M18. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** BLOCKED: missing named validated baseline run; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-14 — Optional OPF gating

**Prüfobjekt und positives Orakel (sobald autorisiert):** False antecedent with evidence produces NOT_APPLICABLE, true antecedent enforces LF cap. **Negativ-/metamorpher Fall:** OPF x=4 when LF bound=3, or always-on OPF despite disabled condition. **Bezug:** R04 C10, V3/V4. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** P15 branch optional; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-15 — P13 pair controls

**Prüfobjekt und positives Orakel (sobald autorisiert):** Only intervention dimension changes, identical frozen source and model parameters. **Negativ-/metamorpher Fall:** Change weather/price-year between runs or sign of comparison silently. **Bezug:** R04 SR-025; V4/V5. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Comparative KPI formula TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-16 — Raw vs KPI

**Prüfobjekt und positives Orakel (sobald autorisiert):** Every KPI has formula source, aggregation scope, status and owner authority; raw output persists. **Negativ-/metamorpher Fall:** Generate system cost from solver objective without authorized conversion rule. **Bezug:** R04 C08, V5. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** MD-04/17; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-17 — B01-D081 filter authority

**Prüfobjekt und positives Orakel (sobald autorisiert):** No filter before documented external owner rule, preserve unfiltered raw rows. **Negativ-/metamorpher Fall:** Invent a 1 MW or 1% threshold and drop candidates. **Bezug:** R03 T16-00; V5. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** BLOCKED: filter rule authority TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-18 — SystemNeed status

**Prüfobjekt und positives Orakel (sobald autorisiert):** SystemNeed never converted to project approval implicitly. **Negativ-/metamorpher Fall:** Publish project_status=APPROVED from optimisation alone. **Bezug:** R04 C08; V5/V6. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Reporting method TBD; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-19 — Required unsupported capability

**Prüfobjekt und positives Orakel (sobald autorisiert):** Missing mandatory H2/storage/network mathematical feature returns UNSUPPORTED. **Negativ-/metamorpher Fall:** Recode unavailable constraint as 'not applicable' and mark PASS. **Bezug:** R04 C09; V2/V3/V6. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** Native tool capability assessment NOT_EXECUTED; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.

### MLC03-C-20 — Source/evidence / signoff

**Prüfobjekt und positives Orakel (sobald autorisiert):** G1 remains BLOCKED without source, owner and independent review certificates. **Negativ-/metamorpher Fall:** Promote R03 synthetic checks or in-memory count audit into release PASS. **Bezug:** R04 E01–E08, V6. **Benötigte Evidenz:** Source-IDs, Original-Releases und validierter Datenfreeze soweit erforderlich, daten-/mathematische Witness, parametrisiertes erwartetes Resultat, accepted numeric tolerance, Tester/Independent Reviewer und Run-/Model-Version. **Aktueller Status:** BLOCKED / NOT_EXECUTED; Prüffall geplant, keine produktive Toolprüfung durchgeführt. Bei offenen erforderlichen Fachparametern `BLOCKED`, bei nicht durchgeführt `NOT_EXECUTED`.


## 5. Stop-Regeln und Test-Exit

1. **Quellen-/Methodikowner unbekannt** → je abhängigem produktivem Claim `BLOCKED`; keine automatische Datenfreigabe.
2. **Fehlender Name eines benötigten Präexpansionslaufes, KPI-/Filterdefinition oder Stage-Carry** → entsprechender Test `BLOCKED` und als fehlende Kante im Lineage-DAG dokumentiert.
3. **Fehlende verpflichtende Fähigkeit** → `UNSUPPORTED` und keine positive Gesamt-Konformität, auch wenn andere Tests PASS zeigen.
4. **Ausführbarer und akzeptiert falsifizierter numerischer Test** → `FAIL` mit konkretem Witness. Fehlende Toleranz ist kein numerisches FAIL, sondern Oracle-Blockade.
5. **Nicht gestarteter echter Testlauf** → `NOT_EXECUTED`. Ein synthetischer oder struktureller Eigencheck bleibt in gesonderter Evidence-Klasse.
6. **P15 OPF explizit nicht anwendbar** → nur P15-spezifische Tests `NOT_APPLICABLE` mit Beweis; verpflichtende LF-Tests bleiben anwendbar.
7. **Owner- und unabhängiger Sign-off / G1** werden nicht aus Testabdeckung inferiert: `G1 BLOCKED`.

## 6. Späteres Pilot-Handoff (nur fachliche Vorbereitung)

Für jedes Testobjekt sind `test_id, claim_ref, applicable_conditions, source_run_ref, producer_input_hashes, expected_behavior, expected_failure, evidence_ports, accepted_oracle_ref, tolerance_ref, actual_execution_status, independent_reviewer_ref` als eigenständige Felder erforderlich. Zwei künftige unabhängige Modellimplementierungen dürfen unterschiedliche interne Variablen haben; die Prüfung vergleicht semantische Projektion, zulässige Mengen, Zielfunktionswert/Optimalitätsgrenzen, Residuen sowie berichtete Rohgrößen, nicht zwingend identische Portfoliolisten. Kein Pilot oder Realdata-Test wurde hier ausgeführt.
