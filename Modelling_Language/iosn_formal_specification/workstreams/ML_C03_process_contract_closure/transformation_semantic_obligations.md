# ML-C03 — Transformation Semantic Obligations

**Baseline:** ML-R00 `9162def25d22c37b1fbc38f7d80fe929425cc8d2`; R01 P00–P17/M01–M18, R03 38 proposals, R04 V1–V6. **NON_NORMATIVE; NOT_EXECUTED; G1 BLOCKED.**

## 1. Semantische Grundunterscheidungen

Ein **Source-Ingest** bestätigt Datenobjektidentität und versionierte Herkunft, aber nicht Quellautorität. **Fachliches Preprocessing** erzeugt neue Dateninstanzen unter expliziten Zuordnungs-/Verlust-/Umrechnungsregeln. **Netzclustering und physische Reduktion** verändern die mathematische Modellrepräsentation und erfordern eigene physikalische Gegenproben (PTDF/LODF/N−1, Referenzfluss, Mesh, PST/HVDC, saisons/richtungen); ein reines ETL-Schema ist dafür unzureichend. **Modellgenerierung und Solve** erzeugen Nebenbedingungen, Variablen, Zielfunktion und Solverresultate. **Reporting** erzeugt nur unter Formel- und Ownerautorität KPIs/Systembedarfe. **Governance/Review** ist Status-, Beleg- und Freigabekontrolle, keine numerische Datenumwandlung.

## 2. Transformationsklassifikation aller 38 Vorschläge

| ID | P | Fachlicher Operationstyp | Originale R03-Semantik (gekürzt) | Offene Regel |
|---|---|---|---|---|
| `MLR03-T00-01` | P00 | Governance and evidence control | Authoritative source-profile and frozen-input release reconciliation | `MD-01;MD-11` |
| `MLR03-T01-01` | P01 | External data intake | Validate separate horizon and variant applicability | `MD-01;MD-20` |
| `MLR03-T01-02` | P01 | External data intake | Bind exact source release extraction slices without silent defaults | `MD-11` |
| `MLR03-T02-01` | P02 | External data intake | Accept externally selected CY1-CY5 cases for each study year | `MD-12;MD-18;MD-19` |
| `MLR03-T03-01` | P03 | Temporal preprocessing | Project declared native calendars onto UTC intervals | `MD-12;MD-16` |
| `MLR03-T03-02` | P03 | Temporal preprocessing | Align demand RES and hydro by study_year CY and temporal reference | `MD-11;MD-12` |
| `MLR03-T04-01` | P04 | Grid baseline composition | Reconcile 2025 grid to 2035 starting reference and project eligibility | `MD-14;MA02-CL-001` |
| `MLR03-T04-02` | P04 | Grid baseline composition | Apply exogenous offshore targets and qualified hybrid projects | `MD-14` |
| `MLR03-T05-01` | P05 | Network clustering | Cluster connected detailed grid into IoSN zones | `MD-13` |
| `MLR03-T05-02` | P05 | Network clustering | Measure congestion size and climate-coherence quality | `MD-13` |
| `MLR03-T06-01` | P06 | Physical network reduction / calibration | Derive equivalent impedances offsets mesh and controllable injection effects | `MD-03;MD-08` |
| `MLR03-T06-02` | P06 | Physical network reduction / calibration | Derive directional seasonal N-1 equivalent capacities | `MD-03` |
| `MLR03-T06-03` | P06 | Physical network reduction / calibration | Reconcile reduction against detailed flows LODF and ratings | `MD-03;MD-13` |
| `MLR03-T07-01` | P07 | Zonal allocation | Map market assets and plants to reduced electrical zones | `MD-11` |
| `MLR03-T07-02` | P07 | Zonal allocation | Aggregate and disaggregate demand RES and generation profiles by zone | `MD-11;MD-12` |
| `MLR03-T08-01` | P08 | Model-semantic assembly | Create carrier and conversion network electrical H2 and DSR semantics | `MD-10;MD-16` |
| `MLR03-T08-02` | P08 | Model-semantic assembly | Construct hydro classes reservoir states and exogenous storage basis | `MD-16` |
| `MLR03-T09-01` | P09 | Candidate/economic preparation | Normalize candidates stage eligibility and controllable DC market links | `MD-07;MD-09` |
| `MLR03-T09-02` | P09 | Candidate/economic preparation | Combine approved offshore geometry length and route factors | `MD-05` |
| `MLR03-T09-03` | P09 | Candidate/economic preparation | Prepare cost and storage candidate coefficients | `MD-02;MD-06` |
| `MLR03-T10-01` | P10 | LP model-generation and solve | Assemble real-only LP expansion with shared first-stage investments | `MD-07;MD-15` |
| `MLR03-T10-02` | P10 | LP model-generation and solve | Export stage1 portfolio objective components and solver status | `MD-15` |
| `MLR03-T11-01` | P11 | LP model-generation and solve | Carry stage1 state and enable remaining candidate classes | `MD-07` |
| `MLR03-T11-02` | P11 | LP model-generation and solve | Export stage2 incremental and total portfolio with economic reconciliation | `MD-07;MD-15` |
| `MLR03-T12-01` | P12 | LP model-generation and solve | Assemble separate 2040 and 2050 storage-stage LP | `MD-06;MD-07` |
| `MLR03-T12-02` | P12 | LP model-generation and solve | Export generic storage needs and explicitly not a sanctioned project | `MD-06` |
| `MLR03-T13-01` | P13 | Paired optimisation/dispatch | Create paired with/without dispatch configuration and internal topology/capacity control artefacts | `MD-08` |
| `MLR03-T13-02` | P13 | Paired optimisation/dispatch | Compute paired dispatch differences including ENS and cost | `MD-04;MD-17` |
| `MLR03-T14-00` | P14 | Baseline-dependent sensitivity | Extract pre-grid-expansion reference hourly electrolyser demand from a separately identified and validated baseline run; baseline solve generation method TBD | `MD-10` |
| `MLR03-T14-01` | P14 | Baseline-dependent sensitivity | Freeze hourly pre-expansion electrolyser load for sensitivity | `MD-10` |
| `MLR03-T14-02` | P14 | Baseline-dependent sensitivity | Export separate electrical expansion response with frozen H2 | `MD-10` |
| `MLR03-T15-01` | P15 | Conditional OPF optimisation | Conditionally assemble OPF capped by selected LF capacities | `MD-08` |
| `MLR03-T15-02` | P15 | Conditional OPF optimisation | Produce OPF result separately identified from core LF output | `MD-08` |
| `MLR03-T16-00` | P16 | Postprocessing and KPI governance | Resolve owner-issued insignificance filter rule reference; if no approved rule, issue UNRESOLVED_CONTROL and do not filter | `MD-04;MD-17` |
| `MLR03-T16-01` | P16 | Postprocessing and KPI governance | Normalize raw output grains sign and run provenance | `MD-04;MD-17` |
| `MLR03-T16-02` | P16 | Postprocessing and KPI governance | Derive metric-definition bound result status/values (B01-D079) and system-needs record (B01-D078) only where approved | `MD-04;MD-17` |
| `MLR03-T16-03` | P16 | Postprocessing and KPI governance | Compute offshore length cost capacity reporting with provenance | `MD-05;MD-04` |
| `MLR03-T17-01` | P17 | Governance and evidence control | Apply structure/source/semantic/model/output checks and preserve disposition | `MD-01;MD-15` |

Die hier ergänzte Operationstyp-Klassifikation ist **ML-C03-Analyse**, während `DATA_OR_SEMANTIC_TRANSFORMATION` und `MODEL_WORKFLOW_OR_SOLVE` die originalen vorgeschlagenen R03-Labels bleiben. Die 38 Einträge sind keine 38 produktiv verfügbaren ETL-Tasks.

## 3. Obligationsfamilien mit wissenschaftlichen Gegenbeispielen

| Familie | Gültige Invariante / Nachweis | Nicht zulässige Vereinfachung | Relevante Schritte |
|---|---|---|---|
| External Source | Quelle, Version, Quelle-zu-Release, Ownerstatus und Originalbyte-Hash, wo real vorliegend; ohne solche Belege BLOCKED | Syntaktisch valider Link = freigegebene Originaldatei | P00–P04, P09 |
| Time/Calendar | UTC-Intervalle (halboffen), `duration_h`, eindeutige Zuordnung; MW→MWh nur über Zeitintegration, dokumentierte Lücken und Resampling | Lokalzeit mit DST doppelt zählen; eine Stundenlücke als Nullleistung kaschieren | P02–P03 |
| Spatial Allocation | Exklusive, vollständige Zuordnung, additive extensive Mengen reaggregiert unter passendem Support; intensive Kenngrößen mit korrektem Gewichtsnenner | Preise, Effizienz und Leistungsfaktoren einfach aufsummieren | P05, P07 |
| Network reduction | Einbettung der physikalischen Bestandselemente, Referenzinjektionen, PTDF/LODF/Schaltfälle, saisonal/gerichtete N−1-Grenzen, Impedanzen, Offset, HVDC, PST, Mesh | Alle Kapazitäten addieren oder reduced network als identischen detaillierten Flow deklarieren | P04–P06, P13 |
| Market-link distinction | Neubaukandidat als steuerbarer DC-Marktlink mit je Richtung passendem NTC und Kapazitätsdeckel; physisches Bestandnetz DC-Mesh | Neuer AC-Technologiekandidat automatisch als Kirchhoff-Zweig in Bestandsgleichungen | P09–P11 |
| Model & Energy | Carriergetrennte Bilanzen, benannte Strom↔H2-Umrechnungsbasis, Speicherzustände, Hydroklassen und DSR-Subtypen | Elektrische MWh = H2 MWh ohne Wirkungsgrad und HHV/LHV-Status | P08, P10–P12 |
| Multi-CY LP | Shared investment `x_y` pro Studienjahr über CY; Dispatch `u_{y,c,t}` je CY; `w_c` jahrübergreifend gleich, numerisch offen | `x_{y,c}` unabhängig optimieren oder `w_c=1/5` als Produktivdefault | P02, P10–P12 |
| Stage & Cost | Stage-1- und Stage-2-Kapazität und Kosten nur nach `F_y` (Owner) übergeben; Währung, Preisjahr, CAPEX/OPEX & Discount getrennt | Zweimal CAPEX zählen oder Stage-1-Teilwerte ignorieren | P09–P12 |
| Paired & Sensitive | P13 referenzidentische Paare, P14 Freeze gegen versionierten *präexpansiven* Referenzsolve; P15 nur bedingt mit LF-Deckel | P12 Resultat als Vor-Expansions-H2-Basis verwenden; OPF-Lauf automatisch anschließen | P13–P15 |
| Reporting | Rohdaten bleiben verfügbar; KPI nur nach genehmigter Formel und Filterautorität B01-D081, Bedürfnisstatus getrennt | KPI aus Solver-Objective ableiten oder dünne Ausbauentscheidungen ungefragt herausfiltern | P16–P17 |
| Evidence | V1 Daten, V2 Semantik, V3 generierte Mathematik, V4 numerisch, V5 Reporting, V6 Herkunft/Review unterscheiden | Synthetic `PASS` als Tool- und Methodik-Certification | P17 |

**Achtung:** Eine physikalische Verlust- oder Wirkungsgradfunktion ist keine Erhaltung von ursprünglicher transportierter Energie an allen Schnittstellen; Hydro-Randbedingungen und Zeitauflösung können bilanzielle Umrechnungen erfordern. Netz-Äquivalenz wird nur relativ zu ausgewiesenen Referenzzuständen und akzeptierten Owner-Maßen überprüft; es existiert kein ungültiges universelles 1:1-Flussgleichheitsgebot.

## 4. Individuelle Pre-/Postcondition- und Ausnahme-Verträge

### MLR03-T00-01 — P00

**Semantik:** Authoritative source-profile and frozen-input release reconciliation; **Kategorie:** Governance and evidence control (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D001`, `B01-D002`.
- **Output-Referenzen:** `MLR03-I-P00-source_manifest`.
- **Preconditions / applicability:** signed releases mandatory before real run. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** No silent promotion of draft or unqualified file. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** validate provenance references and approval signatures. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** manifest serializer; registry implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** MISSING_AUTHORITY;MISSING_RELEASE;HASH_UNVERIFIED. Offene fachliche Entscheidungen: `MD-01;MD-11`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T01-01 — P01

**Semantik:** Validate separate horizon and variant applicability; **Kategorie:** External data intake (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D003`, `B01-D005`.
- **Output-Referenzen:** `MLR03-I-P01-study_manifest`.
- **Preconditions / applicability:** scenario authorization available. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** study_year exactly 2035,2040,2050; no 2030 run. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** enum and per-year isolation. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** storage format; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNAPPROVED_VARIANT;STUDY_YEAR_MISMATCH. Offene fachliche Entscheidungen: `MD-01;MD-20`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T01-02 — P01

**Semantik:** Bind exact source release extraction slices without silent defaults; **Kategorie:** External data intake (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D004`, `MLR03-I-P00-source_manifest`.
- **Output-Referenzen:** `MLR03-I-P01-extraction_index`.
- **Preconditions / applicability:** source pointers and extraction specification exist. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** each extract references run+release+scenario+study_year. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** foreign-key coverage and source-vintage check. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** file access tech; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNRESOLVED_EXTRACTION;AMBIGUOUS_VERSION. Offene fachliche Entscheidungen: `MD-11`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T02-01 — P02

**Semantik:** Accept externally selected CY1-CY5 cases for each study year; **Kategorie:** External data intake (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D006`, `B01-D007`, `B01-D008`, `B01-D003`.
- **Output-Referenzen:** `MLR03-I-P02-weather_manifest`.
- **Preconditions / applicability:** upstream selection signed or kept PENDING. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** same five CY IDs all years; weights shared across years; numeric TBD; no selection. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** technical equality and weight non-negativity when resolved. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** manifest serialisation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** DUPLICATE_CY;MISMATCH_WEIGHTS;WEIGHTS_TBD_FOR_EXECUTION. Offene fachliche Entscheidungen: `MD-12;MD-18;MD-19`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T03-01 — P03

**Semantik:** Project declared native calendars onto UTC intervals; **Kategorie:** Temporal preprocessing (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D013`, `B01-D009`, `B01-D010`, `B01-D011`, `B01-D012`.
- **Output-Referenzen:** `MLR03-I-P03-utc_time_axis`.
- **Preconditions / applicability:** explicit timezone; calendar; unit metadata. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** half-open UTC; duration known; no overlaps or unreported dropped hours. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** interval overlap and duration-based unit tests. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** timezone conversion engine; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** DST_AMBIGUITY;LEAP_POLICY_TBD;INTERVAL_GAP. Offene fachliche Entscheidungen: `MD-12;MD-16`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T03-02 — P03

**Semantik:** Align demand RES and hydro by study_year CY and temporal reference; **Kategorie:** Temporal preprocessing (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `MLR03-I-P02-weather_manifest`, `MLR03-I-P03-utc_time_axis`, `B01-D009`, `B01-D011`, `B01-D012`.
- **Output-Referenzen:** `MLR03-I-P03-aligned_timeseries`.
- **Preconditions / applicability:** complete approved source slice and coverage criteria. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** no silent interpolation; source-profile lineage preserved; energy integral reconciled under approved tolerance. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** compare source to target energy and coverage. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** ETL engine and storage; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** MISSING_CY;TIME_SERIES_GAP;BAD_UNIT. Offene fachliche Entscheidungen: `MD-11;MD-12`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T04-01 — P04

**Semantik:** Reconcile 2025 grid to 2035 starting reference and project eligibility; **Kategorie:** Grid baseline composition (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D014`, `B01-D015`, `B01-D016`.
- **Output-Referenzen:** `MLR03-I-P04-start_grid`.
- **Preconditions / applicability:** owner-approved eligible project list and network vintage. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** unique asset IDs and explicit include/exclude lineage. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** graph integrity and decision-evidence audit. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** graph representation and mapping software; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** PROJECT_ELIGIBILITY_TBD;TOPOLOGY_CONFLICT. Offene fachliche Entscheidungen: `MD-14;MA02-CL-001`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T04-02 — P04

**Semantik:** Apply exogenous offshore targets and qualified hybrid projects; **Kategorie:** Grid baseline composition (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D017`, `B01-D018`, `MLR03-I-P04-start_grid`.
- **Output-Referenzen:** `MLR03-I-P04-offshore_reference`.
- **Preconditions / applicability:** approved target and included-project source refs. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** fixed reference not double counted as expansion candidate. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** compare source target and resulting baseline. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** geographic mapping; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** FIXED_TARGET_MISMATCH;DOUBLE_COUNTING. Offene fachliche Entscheidungen: `MD-14`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T05-01 — P05

**Semantik:** Cluster connected detailed grid into IoSN zones; **Kategorie:** Network clustering (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D019`, `B01-D020`, `MLR03-I-P04-start_grid`.
- **Output-Referenzen:** `B01-D021`.
- **Preconditions / applicability:** network connectivity and clustering criteria available. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** each mapped node has one zone; zones connected; unassigned buses rejected. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** graph connectivity and uniqueness. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** clustering algorithm conditional on quality oracle; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** DISCONNECTED_ZONE;UNMAPPED_NODE. Offene fachliche Entscheidungen: `MD-13`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T05-02 — P05

**Semantik:** Measure congestion size and climate-coherence quality; **Kategorie:** Network clustering (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D020`, `B01-D021`.
- **Output-Referenzen:** `B01-D022`.
- **Preconditions / applicability:** approved metric definitions. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** every clustering metric traceable to detailed cases. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** structural coverage; numeric oracle deferred. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** calculation implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** ZONE_COUNT_OR_THRESHOLD_TBD. Offene fachliche Entscheidungen: `MD-13`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T06-01 — P06

**Semantik:** Derive equivalent impedances offsets mesh and controllable injection effects; **Kategorie:** Physical network reduction / calibration (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D021`, `B01-D023`, `B01-D024`, `B01-D025`.
- **Output-Referenzen:** `B01-D026`, `B01-D027`, `B01-D028`, `B01-D086`, `B01-D087`.
- **Preconditions / applicability:** reference snapshots and parameter convention. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** orientation consistency; physical units and branch reference preserved. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** reconstruct flows versus reference test cases. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** equivalent optimisation approach under approved oracle; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** SINGULAR_NETWORK;MODEL_EQUIVALENCE_TBD. Offene fachliche Entscheidungen: `MD-03;MD-08`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T06-02 — P06

**Semantik:** Derive directional seasonal N-1 equivalent capacities; **Kategorie:** Physical network reduction / calibration (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D024`, `B01-D026`, `B01-D027`, `B01-D028`.
- **Output-Referenzen:** `B01-D029`.
- **Preconditions / applicability:** contingency definitions and reference weather cases known. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** ratings tagged by season and direction; no sign reversal. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** limit and scenario coverage. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** numerical fitting implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** CAPACITY_ORACLE_TBD;MISSING_CONTINGENCY. Offene fachliche Entscheidungen: `MD-03`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T06-03 — P06

**Semantik:** Reconcile reduction against detailed flows LODF and ratings; **Kategorie:** Physical network reduction / calibration (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D023`, `B01-D024`, `B01-D026`, `B01-D027`, `B01-D029`.
- **Output-Referenzen:** `B01-D030`.
- **Preconditions / applicability:** aligned comparison cases available. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** metrics computed on identical case set and sign convention. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** paired-case RMSE LODF and capacity comparison. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** RMSE algorithm under defined formula; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** MISSING_REF_CASE;TOLERANCE_TBD. Offene fachliche Entscheidungen: `MD-03;MD-13`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T07-01 — P07

**Semantik:** Map market assets and plants to reduced electrical zones; **Kategorie:** Zonal allocation (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D031`, `B01-D032`, `B01-D021`.
- **Output-Referenzen:** `B01-D033`.
- **Preconditions / applicability:** source identities and approved crosswalk coverage. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** 100 percent mapped or explicit exceptions; no silent duplicate assets. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** mapping cardinality and allocation validation. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** mapping technology; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** MAPPING_AMBIGUITY;ASSET_DUPLICATE. Offene fachliche Entscheidungen: `MD-11`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T07-02 — P07

**Semantik:** Aggregate and disaggregate demand RES and generation profiles by zone; **Kategorie:** Zonal allocation (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D033`, `MLR03-I-P03-aligned_timeseries`.
- **Output-Referenzen:** `B01-D034`, `MLR03-I-P07-zonal_market_bundle`.
- **Preconditions / applicability:** mapping factors and profile keys complete. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** extensive totals preserved; no assumption for intensive quantities. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** source-target energy and capacity reconciliations. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** allocation algorithm if approved; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** ALLOCATION_NOT_CLOSED;CONSERVATION_FAILURE. Offene fachliche Entscheidungen: `MD-11;MD-12`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T08-01 — P08

**Semantik:** Create carrier and conversion network electrical H2 and DSR semantics; **Kategorie:** Model-semantic assembly (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D035`, `B01-D036`, `B01-D038`, `B01-D039`, `B01-D040`, `B01-D041`, `B01-D042`, `MLR03-I-P07-zonal_market_bundle`.
- **Output-Referenzen:** `B01-D057`.
- **Preconditions / applicability:** units and carrier efficiency reference declared. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** carrier balances distinguish MWh_e and MWh_H2; H2 grid exogenous. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** graph reachability and dimensional balance. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** native tool component decomposition; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** H2_INVESTMENT_UNAUTHORIZED;LHV_HHV_UNKNOWN. Offene fachliche Entscheidungen: `MD-10;MD-16`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T08-02 — P08

**Semantik:** Construct hydro classes reservoir states and exogenous storage basis; **Kategorie:** Model-semantic assembly (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D037`, `B01-D043`, `B01-D044`, `B01-D057`.
- **Output-Referenzen:** `MLR03-I-P08-storage_hydro_constraints`, `B01-D067`.
- **Preconditions / applicability:** hydro model class and inflow semantics known. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** five distinct class labels; time-coupled state consistency. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** unit and temporal balance fixtures. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** constraint algebra implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** STORAGE_BOUNDARY_TBD;HYDRO_CLASS_MISSING. Offene fachliche Entscheidungen: `MD-16`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T09-01 — P09

**Semantik:** Normalize candidates stage eligibility and controllable DC market links; **Kategorie:** Candidate/economic preparation (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D045`, `B01-D046`, `B01-D047`, `B01-D048`, `B01-D049`, `B01-D050`.
- **Output-Referenzen:** `B01-D059`, `B01-D061`.
- **Preconditions / applicability:** candidate class mapping RDFIDs and stage rules. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** candidate has stable ID; distinct candidate link versus physical network. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** eligible set and bidirectional link test. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** link translation representation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** WRONG_CANDIDATE_STAGE;AC_MESH_SUBSTITUTION. Offene fachliche Entscheidungen: `MD-07;MD-09`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T09-02 — P09

**Semantik:** Combine approved offshore geometry length and route factors; **Kategorie:** Candidate/economic preparation (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D051`, `B01-D052`, `B01-D050`.
- **Output-Referenzen:** `MLR03-I-P09-offshore_routing`.
- **Preconditions / applicability:** route scope and protected layers available. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** distance km; factor provenance; factor numeric TBD. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** route-factor dimensional checks. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** geospatial engine; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** FACTOR_TBD;ROUTE_GEOMETRY_MISSING. Offene fachliche Entscheidungen: `MD-05`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T09-03 — P09

**Semantik:** Prepare cost and storage candidate coefficients; **Kategorie:** Candidate/economic preparation (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D053`, `B01-D054`, `B01-D055`, `B01-D056`.
- **Output-Referenzen:** `MLR03-I-P09-economic_bundle`.
- **Preconditions / applicability:** currency price-year lifetime discount method approved. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** currency basis explicit; costs counted once. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** test unit transformations and no duplicate cost terms. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** cost coefficient implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** PRICE_YEAR_MISSING;DISCOUNT_TBD. Offene fachliche Entscheidungen: `MD-02;MD-06`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T10-01 — P10

**Semantik:** Assemble real-only LP expansion with shared first-stage investments; **Kategorie:** LP model-generation and solve (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D057`, `B01-D028`, `B01-D059`, `MLR03-I-P09-economic_bundle`, `MLR03-I-P02-weather_manifest`.
- **Output-Referenzen:** `B01-D058`, `MLR03-I-P10-stage1_model_input`.
- **Preconditions / applicability:** weather weights numerically approved for real execution. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** identical investment x across CY; candidate-stage segregation. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** model-input semantic constraints. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** solver and algebra implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNRESOLVED_WEIGHT;CANDIDATE_MISCLASSIFIED. Offene fachliche Entscheidungen: `MD-07;MD-15`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T10-02 — P10

**Semantik:** Export stage1 portfolio objective components and solver status; **Kategorie:** LP model-generation and solve (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `MLR03-I-P10-stage1_model_input`.
- **Output-Referenzen:** `B01-D060`.
- **Preconditions / applicability:** solver run completed and primal validation. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** solutions must contain valid witness not only objective label. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** solver status and feasibility witness check. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** LP solver free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** SOLVE_FAILED;PRIMAL_INVALID. Offene fachliche Entscheidungen: `MD-15`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T11-01 — P11

**Semantik:** Carry stage1 state and enable remaining candidate classes; **Kategorie:** LP model-generation and solve (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D060`, `B01-D061`.
- **Output-Referenzen:** `B01-D063`, `MLR03-I-P11-stage2_model_input`.
- **Preconditions / applicability:** stage1 portfolio and fixed/carry policy approved. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** no stage1 investment cost or capacity double counting. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** candidate identity reconciliation. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** implementation of transition free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** INHERITANCE_TBD;DOUBLE_COUNT. Offene fachliche Entscheidungen: `MD-07`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T11-02 — P11

**Semantik:** Export stage2 incremental and total portfolio with economic reconciliation; **Kategorie:** LP model-generation and solve (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `MLR03-I-P11-stage2_model_input`, `B01-D063`.
- **Output-Referenzen:** `B01-D062`, `B01-D068`.
- **Preconditions / applicability:** stage2 solve witness. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** stage2 final = carried stage1 + incremental under chosen rule. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** portfolio and cost decomposition test. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** LP solver free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNRECONCILED_PORTFOLIO;INVALID_SOLVE. Offene fachliche Entscheidungen: `MD-07;MD-15`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T12-01 — P12

**Semantik:** Assemble separate 2040 and 2050 storage-stage LP; **Kategorie:** LP model-generation and solve (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D064`, `B01-D067`, `B01-D062`, `B01-D056`.
- **Output-Referenzen:** `B01-D065`, `MLR03-I-P12-storage_model_input`.
- **Preconditions / applicability:** country caps and storage classes approved. Ausführungsbedingung: `ONLY_2040_2050`.
- **Erhaltungs-/Vergleichseigenschaften:** no 2035 storage expansion decision in this stage. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** country-year set and cap checks. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** LP representation free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** YEAR_NOT_ALLOWED;COUNTRY_CAP_TBD. Offene fachliche Entscheidungen: `MD-06;MD-07`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T12-02 — P12

**Semantik:** Export generic storage needs and explicitly not a sanctioned project; **Kategorie:** LP model-generation and solve (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `MLR03-I-P12-storage_model_input`.
- **Output-Referenzen:** `B01-D066`.
- **Preconditions / applicability:** validated storage stage solver results. Ausführungsbedingung: `ONLY_2040_2050`.
- **Erhaltungs-/Vergleichseigenschaften:** needs values retain country type duration and run identity. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** class and portfolio provenance. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** solver platform free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** NEED_AS_PROJECT;RUN_INVALID. Offene fachliche Entscheidungen: `MD-06`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T13-01 — P13

**Semantik:** Create paired with/without dispatch configuration and internal topology/capacity control artefacts; **Kategorie:** Paired optimisation/dispatch (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D068`, `B01-D014`, `B01-D029`.
- **Output-Referenzen:** `B01-D069`, `B01-D070`, `MLR03-I-P13-paired_dispatch_inputs`.
- **Preconditions / applicability:** validated LF portfolio, internal network topology and capacities; comparator-run definition. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** comparison cases have identical non-portfolio assumptions; explicit grid reference. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** pair-key and diff scope check. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** dispatch implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** PAIR_NOT_COMPARABLE;NETWORK_VERSION_MISMATCH. Offene fachliche Entscheidungen: `MD-08`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T13-02 — P13

**Semantik:** Compute paired dispatch differences including ENS and cost; **Kategorie:** Paired optimisation/dispatch (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `MLR03-I-P13-paired_dispatch_inputs`.
- **Output-Referenzen:** `B01-D071`.
- **Preconditions / applicability:** both run statuses accepted. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** difference direction explicit; no mixed units or unmatched runs. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** recalculate from raw pair. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** postprocessing implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** MISSING_PAIR;INVALID_BASELINE. Offene fachliche Entscheidungen: `MD-04;MD-17`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T14-00 — P14

**Semantik:** Extract pre-grid-expansion reference hourly electrolyser demand from a separately identified and validated baseline run; baseline solve generation method TBD; **Kategorie:** Baseline-dependent sensitivity (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D057`, `B01-D040`, `B01-D042`.
- **Output-Referenzen:** `B01-D072`.
- **Preconditions / applicability:** Owner-authorised pre-expansion reference run and exact CY/time mapping required. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** each baseline hour has source_run_id and original carrier and input-power unit; no inferred default run. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** lineage to declared preexp run, completeness over CY UTC time. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** No assumption of specific solver or ETL engine; only versioned source-to-target mapping; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** BASELINE_SOLVE_NOT_DEFINED;SOURCE_RUN_MISSING. Offene fachliche Entscheidungen: `MD-10`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T14-01 — P14

**Semantik:** Freeze hourly pre-expansion electrolyser load for sensitivity; **Kategorie:** Baseline-dependent sensitivity (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D072`, `B01-D040`, `B01-D042`.
- **Output-Referenzen:** `B01-D073`.
- **Preconditions / applicability:** approved exact preexp source and time axis. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** every frozen entry identical baseline value and dimension. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** exact interval keyed equality. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** native P2G implementation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** FROZEN_BASELINE_MISSING;H2_DRIFT. Offene fachliche Entscheidungen: `MD-10`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T14-02 — P14

**Semantik:** Export separate electrical expansion response with frozen H2; **Kategorie:** Baseline-dependent sensitivity (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D073`, `B01-D057`.
- **Output-Referenzen:** `B01-D074`.
- **Preconditions / applicability:** sensitivity run comparable with declared baseline. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** results are labelled sensitivity not replacement base LF. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** freeze invariance and model-run linkage. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** LP platform free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** SENS_NOT_FROZEN;MIXED_RUNS. Offene fachliche Entscheidungen: `MD-10`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T15-01 — P15

**Semantik:** Conditionally assemble OPF capped by selected LF capacities; **Kategorie:** Conditional OPF optimisation (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `B01-D075`, `B01-D068`.
- **Output-Referenzen:** `B01-D076`, `MLR03-I-P15-opf_model_input`.
- **Preconditions / applicability:** optional OPF decision approved. Ausführungsbedingung: `OPTIONAL_ONLY`.
- **Erhaltungs-/Vergleichseigenschaften:** each OPF candidate bound does not exceed corresponding LF bound. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** cap inequalities and LF reference integrity. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** OPF solver and network formulation; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** NO_RUN_DECISION;UNBOUNDED_CANDIDATE. Offene fachliche Entscheidungen: `MD-08`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T15-02 — P15

**Semantik:** Produce OPF result separately identified from core LF output; **Kategorie:** Conditional OPF optimisation (R03-Label: `MODEL_WORKFLOW_OR_SOLVE`).

- **Input-Referenzen:** `MLR03-I-P15-opf_model_input`.
- **Output-Referenzen:** `B01-D077`.
- **Preconditions / applicability:** OPF solved and caps verified. Ausführungsbedingung: `OPTIONAL_ONLY`.
- **Erhaltungs-/Vergleichseigenschaften:** OPF cannot silently replace LP/LF published basis. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** separate method label and caps audit. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** OPF platform; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** SOURCE_SUBSTITUTION;CAP_VIOLATION. Offene fachliche Entscheidungen: `MD-08`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T16-00 — P16

**Semantik:** Resolve owner-issued insignificance filter rule reference; if no approved rule, issue UNRESOLVED_CONTROL and do not filter; **Kategorie:** Postprocessing and KPI governance (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D001`, `B01-D002`.
- **Output-Referenzen:** `B01-D081`.
- **Preconditions / applicability:** explicit signed reporting owner rule required for active threshold. Ausführungsbedingung: `ONLY_IF_FILTER_AUTHORISED`.
- **Erhaltungs-/Vergleichseigenschaften:** threshold has dimension, unit, applicability and approver or is null+TBD status. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** filter version/signature and unit test; missing threshold blocks filtering not raw retention. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** No assumption of specific solver or ETL engine; only versioned source-to-target mapping; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** FILTER_RULE_TBD;UNAUTHORISED_DEFAULT. Offene fachliche Entscheidungen: `MD-04;MD-17`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T16-01 — P16

**Semantik:** Normalize raw output grains sign and run provenance; **Kategorie:** Postprocessing and KPI governance (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D060`, `B01-D062`, `B01-D066`, `B01-D071`, `B01-D074`, `B01-D077`.
- **Output-Referenzen:** `MLR03-I-P16-raw_result_index`, `B01-D082`.
- **Preconditions / applicability:** run IDs method branches and dimensions declared. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** raw solution not confused with report indicator; optional fields marked. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** FKs to solver runs and provenance graph. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** ETL and result store free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNKNOWN_RUN;AXIS_COLLISION. Offene fachliche Entscheidungen: `MD-04;MD-17`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T16-02 — P16

**Semantik:** Derive metric-definition bound result status/values (B01-D079) and system-needs record (B01-D078) only where approved; **Kategorie:** Postprocessing and KPI governance (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `MLR03-I-P16-raw_result_index`, `B01-D081`.
- **Output-Referenzen:** `B01-D079`, `B01-D078`.
- **Preconditions / applicability:** owner-approved KPI formula or status UNDEFINED. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** no invented formula; needs not project approvals. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** metric definition version and aggregate grain audit. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** report design free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** FORMULA_TBD;FILTER_THRESHOLD_TBD. Offene fachliche Entscheidungen: `MD-04;MD-17`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T16-03 — P16

**Semantik:** Compute offshore length cost capacity reporting with provenance; **Kategorie:** Postprocessing and KPI governance (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D050`, `B01-D051`, `B01-D052`, `MLR03-I-P16-raw_result_index`.
- **Output-Referenzen:** `B01-D080`, `MLR03-I-P16-offshore_report`.
- **Preconditions / applicability:** geometry and cost allocation authority available. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** length and cost unit consistency; allocation no double counting. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** reconcile route and candidate ids. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** report tooling free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNRESOLVED_FACTOR;MISSING_LENGTH. Offene fachliche Entscheidungen: `MD-05;MD-04`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.

### MLR03-T17-01 — P17

**Semantik:** Apply structure/source/semantic/model/output checks and preserve disposition; **Kategorie:** Governance and evidence control (R03-Label: `DATA_OR_SEMANTIC_TRANSFORMATION`).

- **Input-Referenzen:** `B01-D083`, `B01-D084`, `B01-D085`, `B01-D082`, `B01-D078`.
- **Output-Referenzen:** `MLR03-I-P17-review_evidence`.
- **Preconditions / applicability:** approved test oracles for substantive run certification. Ausführungsbedingung: `RUN_APPLICABLE`.
- **Erhaltungs-/Vergleichseigenschaften:** NO executed test passes by schema only; blocks remain visible. Nur unter Quell- und Größenartbedingungen gültig; kein universeller Mengen- oder Stromflusserhaltungssatz.
- **Prüfbedarf:** adversarial sample checks and evidence register. Erforderlich sind Input-/Outputinstanzen, unveränderte Quellbezüge, Transformation-/Parameter-Version, Run-ID, nachvollziehbares Statusresultat und ggf. genehmigtes numerisches Orakel.
- **Erlaubte technische Freiheit:** test runner free; kann **keine** fehlende Methodikentscheidung ersetzen.
- **Fehler-/Blockerfälle:** UNAPPROVED_ORACLE;MISSING_SIGNOFF. Offene fachliche Entscheidungen: `MD-01;MD-15`. Owner approval: `NON_NORMATIVE_TBD_OWNER`; native uitvoering: `NOT_EXECUTED`.


## 5. Speziell unvollständige Verträge

- **T14-00 / B01-D072:** Die Beschreibung `Extract pre-grid-expansion reference hourly electrolyser demand` enthält keine tatsächlich freigegebene Referenzmodellrechnung oder `baseline_run_id`; der veröffentlichbare Freeze bleibt `BLOCKED`, auch wenn die B01-D072-Prozesskante vorhanden ist. Prüfartefakt: benanntes Prä-Expansions-Run-/Modell-/Quellfreeze-Manifest, vollständiger Stunden-/Zonen-/CY-Vektor, Witness und Gleichheit der eingefrorenen Werte.
- **T16-00 / B01-D081:** Eine reporting-Owner-Filterregel ist eine externe kontrollierende Autorität. `Resolve owner-issued...` darf nur auf eine solche Regel referenzieren; sie wird nicht durch P16 oder einen Default erst erzeugt. Fehlende Definition → `UNRESOLVED_CONTROL`, keine stille Filterung.
- **T11-01 / B01-D063:** Eine syntaktische Transformation von `stage1_portfolio` zu `stage2_model_input` ist ohne fachliche Übernahme- und Kostenregel nicht gleichbedeutend mit dem korrekten Zwei-Stufen-LP.
- **T06-01..03 / B01-D026..30,D086,D087:** Erst eigenständige Netzreferenz- und Fehlerorakel können über physikalische Äquivalenz urteilen. Keine numerischen Akzeptanzwerte fingieren.
- **T16-02..03 / B01-D078..80:** Report und veröffentlichter KPI müssen `formula_ref, version, denominator, time/CY/space aggregation, missing-value rule, filter_rule, approval` tragen; solange diese fehlen, bleiben die fachlichen Ergebnisse `BLOCKED_ORACLE`.

## 6. Exit-/Fehlersemantik

Für jede Ausführung sind `NOT_EXECUTED, PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_APPLICABLE` nach R04 **pro Test/Claim** und getrennt von Source-/Ownerstatus zu führen. Ein physikalischer Qualitätsfehler mit belegtem Testresultat ist FAIL; ein nicht freigegebenes numerisches Orakel ist BLOCKED; kein getesteter Solverlauf ist NOT_EXECUTED. P15 darf nur bei belegter falscher Antezedenz NOT_APPLICABLE sein. G1 unverändert BLOCKED.
