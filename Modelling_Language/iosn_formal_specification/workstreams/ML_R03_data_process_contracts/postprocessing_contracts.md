# ML-R03 — Postprocessing & IoSN Output Contracts
**Version:** 0.1 · **Status:** NON_NORMATIVE_RESEARCH_DRAFT · **Keine endgültigen KPI-Formeln festgelegt**

## 1. Eingangsgrenze und Resultatspeicher
Postprocessing beginnt **nach** der Exportkontrolle der Modellläufe. Ein `RawResultRecord` ist ein Ergebnis einer Rechenstufe, **kein** veröffentlichungsfähiger Systembedarf. Die P16-Eingänge sind vorläufig B01-D060 (Stage 1), D062 (Stage 2), D066 (Storage), D071 (paired internal dispatch), D074 (H2-Sensitivität), optional D077 (OPF), die Kennzahlen-/Filtervorgaben D079/D081 und zusätzlich Offshore-Geometrie D050–D052/D080. Ergebnisprovenienz B01-D082 und Bericht B01-D078 bleiben getrennt.

Der Output-Workflow ist als nachvollziehbarer gerichteter Graph zu modellieren:
```text
P10/P11 LF-portfolio ────────────────┐
P12 storage ─────────────────────────┤
P13 with/without dispatch ──────────┼─> P16 raw-result register (unit/axis/lineage)
P14 frozen-H2 sensitivity ───────────┤         │
P15 optional OPF (if approved) ──────┘         ├─> metric definition resolution
Candidate/corridor geometry/economics ─────────┤       │
                                                  ├─> derived indicator objects
                                                  ├─> published SYSTEM_NEED opportunities
                                                  └─> P17 verification and release gate
```
Jeder Input enthält `run_id`, `study_year`, `branch_type`, `stage`, `source_freeze_ref`, `model_version`, `result_schema_version`, `solve_quality` und indikatorspezifische Achsen. Ein unvollständiger oder nicht gelöster Lauf darf kein als endgültig veröffentlichtes Ergebnis erzeugen.

## 2. Methodisch neutrale KPI-Definitionsstruktur
`MetricDefinition = {metric_id, intent, input_quantity_types, formula_or_TBD, aggregation_operator_or_TBD, aggregation_axes, currency_and_price_year_if_needed, unit, baseline_run_rule, weather_weight_rule, time_duration_rule, spatial_reference, validity_scope, zero_and_null_policy, filter_id, rounding_rule, responsible_owner, approval_state, version}`.

Ein `MetricValue = {metric_id, definition_version, value_or_null, status, reason_code, unit, study_year, CY_id_or_aggregate, spatial_scope, stage, comparator_refs, source_run_ids, provenance_refs, approval_state}`. **TBD-Formel → `value=null` und `FORMULA_TBD`**, keinesfalls null durch 0 ersetzen. Auch ein von einem Tool berechneter numerischer Wert ist ohne anerkannte Definition und Laufstatus nicht automatisch berichtbar.

## 3. Ergebnisfamilien und Berechnungsabhängigkeiten
| Ergebnisfamilie | Rohquellen | nötige Indizes, Bezugsgrößen und Metadaten | Formel-/Entscheidungsstatus |
|---|---|---|---|
| **Netzausbauentscheidung, Investitionsbedarf** | `candidate_units`, `new_transfer_MW`, stage1/2 `x` | study_year; candidate; corridor; real/conceptual/theoretical; direction; market link; stage; cost basis | Stage-Carry (MD-07), Filter (MD-04) offen |
| **Grenzüberschreitender Übertragungsbedarf** | LF-Portfolio, directional transfer, reference capacities | geordnete Länder-/Zonenpaare, NTC+/NTC−, corridor ID, MW, baseline grid ID | Aggregation über parallele Links und Richtungen TBD |
| **Speicherbedarf** | P12 `storage_power_MW`, `storage_energy_MWh` | 2040/2050, country, technology/duration class, exogenes Referenzportfolio | Ländergrenze und Kostenstatus MD-06 |
| **Flexibilitätsbedarf / DSR** | DSR dispatch bounds/activation, storage and curtailment | source category, dispatch time, unit, normal/implicit DSR marker | Offen, DSR/implizite Flex-Abgrenzung MD-16 |
| **Stromsystembetrieb** | generation, exchange, ENS, curtailment, branch loads | CY, UTC intervals, electrical zone, unit and energy/power measurement | stunden-/wettergewichtete Aggregation nach freigegebener Definition |
| **Wasserstoff-Systembezug** | electrolyser input, H2 production/storage/exchanges, P14 | H2 zone, electricity zone, conversion link, `MWh_H2_(LHV/HHV)`, frozen status | H2-Baseline und physikalische Referenz MD-10 |
| **Betriebs- und Systemkosten** | variable, startup, CO2, fuel, dispatch and investment costs | currency, real/nominal, price_year, cost_component, discount_basis, objective scope | WACC/discount and aggregation MD-02/04 offen |
| **Wirkung internen Netzes** | P13 paired with/without costs, ENS, flows | pair_id, baseline/with run IDs, identical external assumptions, delta sign | genaues KPI-/Vergleichsorakel MD-04/17 |
| **Offshore-/ONDP-Bedarfe** | selected offshore links; route geometry/length; cost split | corridor, endpoints, km, MW, geographic protection, detour factor, EUR | Faktor (Draft 10–15%) und finale Kostenregel MD-05/04 offen |
| **Optionaler OPF-Output** | P15 results plus LF upper bounds | branch_type=OPF_OPTIONAL, explicit LF reference, ceiling proof | kein Austausch der Haupt-LF-Resultate |
| **Zuverlässigkeit / Nichtbelieferung** | unserved power and dispatch comparison | CY, time, area, `MW` versus `MWh`, occurrence, definition | Monetarisierung/ENS-KPI ohne Ownerformel offen |
| **Technologie-/Projektstatus** | investment and candidates | output_type=SYSTEM_NEED; project_status=NOT_APPROVED, candidate identity | keine Projektreife aus Modellbedarf ableiten |

Diese Tabelle ist eine **semantische Verpflichtung zur Vollständigkeit der Definition**, nicht die Behauptung, alle Größen seien von der Konsultationsmethodik bereits als veröffentlichtes KPI vorgegeben.

## 4. Zulässige rechnerische Operationen und offene fachliche Entscheidungen
**Zeit:** Leistung aus einem Intervall wird für eine *technische* Energieberechnung mit `duration_h` multipliziert; das ist dimensionsbezogen und noch keine genehmigte Kennzahlenformel. Zeitachsen dürfen nicht die Werte eines ungleichen 8760-/8784-Stundenkalenders ohne Protokoll mischen. Lückenprüfung ist pro `(study_year,CY,zone,carrier,series_type)` durchzuführen.

**Wetter:** dieselben `CY1–CY5` und identischen `w_i` über alle Zieljahre; eine *offizielle gewichtete Kennzahl* darf erst berechnet werden, wenn `w_i` numerisch und autorisiert sind und die definierte Aggregationsart feststeht. Kein implizites arithmetisches Mittel. Synthetische 0,2 sind nur technische Fixtures.

**Raum:** Summen über exklusive Regionen sind bei geeigneten extensiven Größen plausibel; überlappende Markt-/IoSN-Zonenkarten erfordern veröffentlichte Crosswalk-Faktoren. Nichtadditive Kennzahlen (Mittelpreise, normierte Einspeisefaktoren, Quoten) können nicht durch simple Summe konsolidiert werden.

**Korridore und Richtung:** Vorzeichen/Orientierung, Richtungsgrenzen und Zuordnung von mehreren Kandidaten zu einem Korridor sind explizit. Kilometerwerte brauchen Geometriestandard und Factor-Rule; MW ist nicht direkt mit MWh oder GW ohne Konversion vergleichbar.

**Kosten:** Nominal-, Real-, Preisjahr- und Diskontierungsdefinition, Kostenkomponenten, CAPEX/OPEX, doppelte Kosten in Stufe 1/2 und räumliche Allokationen müssen getrennt geführt werden. `objective_value` des Solvers ist ohne bestätigte Kostenkonvention nicht automatisch `system_cost`.

**Vergleich:** P13-Delta benötigt `baseline_run_ref`, `policy_run_ref`, geprüfte gemeinsame Annahmen, explizite Differenzrichtung und vollständigen Paarstatus. Der Ausdruck `base - intervention` darf nur als dokumentierte **technische Delta-Orientierung**, nicht als automatisch freigegebener Benefit-KPI verwendet werden.

**Unwesentlichkeitsfilter:** B01-D081/MD-04/MD-17. Ohne bestätigten Grenzwert und Bezug (`MW` oder Prozent etc.) keine Filterung; Rohdaten bleiben erhalten. Bei genehmigter Filterung müssen Vorher-/Nachher-Werte, Filterregel, Ausschlüsse und Auswirkung auf Summen nachvollziehbar bleiben.

## 5. Postprocessing Contract-Manifest
| Contract ID | Eingang | Ausgang | Technische Prüfkriterien | Blockierend |
|---|---|---|---|---|
| `POST-01` | alle RawRun-Referenzen | `RawResultIndex` | Run-/Stage-/branch-FKs und eindeutige Ergebnisgrains | unbekannter Run, unqualifizierter Solverstatus |
| `POST-02` | Raw Units und Flow-Signs | `NormalizedResults` | dimensionsgleiche Einheiten; Faktor/Sign-Protokoll | inkonsistente Dimension |
| `POST-03` | Geo-/Identity Crosswalk | `SpatiallyAllocatedValues` | keine doppelte extensive Zuordnung | unauflösbare N:M-Mapping-Fälle |
| `POST-04` | Intervalldaten | `TemporallyReconciledValues` | UTC, lücken-/dauerbewusste Aggregation | Zeitlücken, nicht genehmigte Konversion |
| `POST-05` | CY-Ergebnisse + Gewichtsmanifest | `WeatherAggregates` oder `UNDEFINED` | CY1–5 vollständig; w-Vektor geteilt über Y | Gewichtswerte oder Aggregationsregel TBD |
| `POST-06` | Stage 1/2/P12 | `InvestmentAndStorageNeeds` | Portfolio-Reconciliation und Länder-/Technologiebindung | Carry-/Cap-Semantik fehlt |
| `POST-07` | P13 Run-Paare | `ComparisonMetrics` | identische Komparatorbasis, signierter Delta-Operator | Paar fehlt oder Formula TBD |
| `POST-08` | P14 Frozen-H2 | `HydrogenSensitivityIndicators` | baseline freeze proof; separate branch | H2-Freeze nicht belegt |
| `POST-09` | P15 optional OPF | `SeparateOPFIndicators` | freigegebene Opt-in und LF-Caps | OPF ohne explizite Entscheidung |
| `POST-10` | Offshore, Filter, Kosten | `OffshoreNeeds` / `SystemNeedRegister` | definierte Routen, Kostenbasis, nicht projektgenehmigt | Detour-/Filter-/KPI-Formel TBD |
| `POST-11` | sämtliche abgeleitete Resultate | `PublishableEvidencePackage` oder `RELEASE_BLOCKED` | Kennzahlversion, Provenienz, Prüfungen, Ownerstatus | Quelle oder Ownerfreigabe offen |

## 6. Statusmodell für unvollständige Ergebnisse
`RAW_AVAILABLE_UNVERIFIED`, `RAW_SOLVE_INVALID`, `INPUT_MISSING`, `AXIS_INCOMPATIBLE`, `UNDEFINED_METRIC`, `COMPARATOR_MISSING`, `AGGREGATION_TBD`, `SOURCE_QUALIFICATION_MISSING`, `OWNER_APPROVAL_MISSING`, `TECHNICAL_TEST_PASS`, `RELEASE_BLOCKED`, `RELEASE_APPROVED`. Bei gleichzeitig mehreren Problemen werden alle Ursachen gemeldet; kein `PASS` aus Schema-Konformität. `UNDEFINED` und `MISSING` sind niemals als gemessene 0 zu schreiben.

Jeder abgeleitete Wert erhält einen Lineage-Pfad `SourceArtifact → SourceDataInstance → TransformationExecution(s) → ModelInputBundle → ModelRunResult → MetricDefinition → MetricValue → PublishedNeed`; optional `TransformationExecution` oder `ModelRunResult` ist nur dann auslassbar, wenn der Datenobjekttyp keine solche Stufe benötigt.

## 7. Offen zu übergeben, nicht von ML-R03 entschieden
Definitive KPI-Definitionen, Kosten-/Zinsbasis, Stage-1/2-Reconciliation, Kleinmengenfilter, Offshore-Routen-/Kostenregel, Gewichtswerte, DSR-/Hydro-Semantik, P13-Referenzpaar und Akzeptanztoleranzen sind **TBD**. Vorliegt eine Rückverfolgbarkeitsarchitektur, **nicht** die Aussage, dass IoSN-Originalergebnisse oder eine freigabefähige Nutzenrechnung bereits hergestellt wären.
