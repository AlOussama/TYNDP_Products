# ML-R03 — Model Input and Output Contracts
**Status:** NON_NORMATIVE_DRAFT · **Abstraktion:** fachliche Mengen, Parameter, Entscheidungen, Bedingungen, Resultate und ihre Evidenz, **kein** PyPSA-/GenzOE-/Antares-/Sienna-Schema.

## 1. Fachlicher Modellinput (toolneutral)
| Vertragsobjekt | Indizes / Minimalattribute | Dimensions- und Semantikregel |
|---|---|---|
| `StudyCase` | `study_year∈{2035,2040,2050}`, `variant`, `run_id`, `method_profile` | getrennte Zieljahrsmodelle; Revision explizit |
| `WeatherContext` | `CY∈{CY1,…,CY5}`, `weight_ref`, `profile_ref`, `study_year` | gleiche `weight(CY)` in allen Zieljahren; numerische Gewichte **TBD** |
| `TimeStep` | `[start_utc,end_utc)`, `duration_h`, `calendar_ref` | Stundenmodell nicht ohne Zeit-/Calendar-Ownerentscheidung erzwingen |
| `RegionAndTopology` | zone, bus_map, branch/link, country, geometry_ref, topology_version | Marktzone, IoSN-Zone und physischer Netzbus getrennte Identitäten |
| `CarrierGraph` | electricity, H2 und ggf. andere explizit modellierte Carrier, conversion edge | physikalische Einheiten und Brennwertbasis getrennt |
| `DemandAndAvailability` | `(year,CY,interval,zone,carrier,technology)` | demand MW bzw energy MWh klar differenzieren |
| `Assets` | thermal, RES, hydro class, storage, DSR, P2G, H2-to-power, fixed exchange | Parameter, Betriebsrestriktionen, exogen/endogen als Flag |
| `GridEquivalent` | zone links, mesh constraints, impedance, offsets, PST/HVDC, directional N−1 ratings | Netzreduktionsnachweise getrennt von Model-Feasibility |
| `ExpansionCandidate` | candidate_id, class, stage, max_units, directional capacities, market_link_semantics, route_ref | steuerbarer DC-Marktlink im LF; physische AC/DC-Technologie separat |
| `EconomicBasis` | capex, opex, fuel/CO2, startup, price_year, currency, WACC/life/block_ref | kein impliziter WACC, Diskontierungs- oder Preiserhöhungswert |
| `RunControl` | stage, optional_branch, initial_portfolio, solver_flags, `approval_state` | P10/P11/P12/P13/P14/P15 unterscheiden |
| `DataLineage` | input_dataset_ref, transformation_ids, config_revision, exact_SOURCE_qualification_status | vollständige Herkunft, selbst wenn Source `UNVERIFIED` |

Eine Umsetzung darf die Eingänge intern anders zerlegen, sofern eine explizite, prüfbare semantische Abbildung existiert. **Fehlende Pflichtfelder führen zur Zurückweisung des produktiven ModelInputBundle.** Für den Forschungsmodus bleiben nicht verifizierte Parameter als `TBD` ausweisbar.

## 2. Mathematische Modellstruktur (Semantikskizze)
Definiere Studienjahre `Y`; Wetterfälle `C={CY1,…,CY5}`; Zeitintervalle `T_yc`; elektrische Zonen `Z^e`; H2-Zonen `Z^h`; Dispatchanlagen `G`; Speicher `S`; Interkonnektoren `L`; Ausbaukandidaten `K`. Die Indexierung `(y,c,t)` verhindert stille Vermischung der Fälle.

**Gemeinsam geplante Entscheidung:** `x_{k,y}` bezeichnet die Investitionsgröße eines Kandidaten in einer Expansionsstufe; `x` darf **nicht** automatisch einen zusätzlichen CY-Index erhalten. Betriebliche Entscheidungen wie `p_{g,y,c,t}`, `f_{l,y,c,t}`, `SOC_{s,y,c,t}` sind dagegen fall-/zeitabhängig. Eine andere toolinterne Variablenbenennung ist zulässig, wenn diese Nichtantizipativitätssemantik erhalten bleibt.

**Illustrative Zielfunktionskomponenten, keine Freigabe einer konkreten Formel:**
```text
InvestmentTerm = cost_rule(stage, x, CAPEX, price_year, discount_blocks=TBD)
OperationTerm  = aggregate_rule(weight[CY], duration_h, dispatch_cost, ENS_cost,
                                fuel_CO2_cost, storage_cost, cost_reconciliation=TBD)
Objective      = approved_objective_rule(InvestmentTerm, OperationTerm, ...)
```
Insbesondere `discount_blocks`, numerischer `WACC`, `ENS`-Kostenregeln, Kraftwerksanfahrsemantik und alle Gewichtsparameter sind **nicht** aus dieser Skizze abzuleiten. Testbare Struktur: `weight[CY]` für die drei Zieljahre identisch; aus dem Owner-Release müssen bei einem produktiven Solve gültige konkrete Werte kommen. Bei gesonderten Studienjahren werden keine stillschweigenden intertemporalen Ausbaukopplungen eingeführt.

**Konstraintfamilien:** (a) Elektrizitätsknoten-/Zonenbilanzen, (b) H2-Massen-/Energiebilanz und P2G/H2-to-power mit deklarierter Effizienz und LHV/HHV, (c) Speicherzustände und zyklische/grenzwertbezogene Betriebsbedingungen, (d) Hydro-Betriebs- und Inflowrestriktionen fünf Klassen, (e) Netzfluss-/Mesh-/N−1-Limits im gewählten Äquivalent, (f) Emission/Fuel-/DSR-/Reserve-/Transferbedingungen soweit methodisch vorgegeben, (g) Expansionskandidaten und Stufenzulässigkeit, (h) gefrorenes H2 für P14, (i) LF-Cap für optionale P15-OPF. **Exakte Gleichungen, Bindungen, Grenzfälle und Toleranzen** müssen aus verifizierter Methodik und Ownerbeschlüssen ergänzt werden.

## 3. Modelllauf-Typen und Schnittstellen
| Laufart | Inputs | Raw-Output und Pflichtmetadaten | Besondere Grenze |
|---|---|---|---|
| `P10_STAGE1_REAL_LP` | P08 model, Real-Kandidaten, CY-Gewichte | `x_stage1`, Dispatch, Kostenanteile, Status, Witness, `run_id` | nur reale zulässige Kandidaten |
| `P11_STAGE2_LP` | Stage1-Carry, verbliebene Kandidaten | inkrementelle und finale Portfolios, Kosten-Dekomposition, Duale falls verfügbar | Carry-over-Fachregel TBD; keine Doppelzählung |
| `P12_STORAGE_LP` | 2040/2050, Country-Caps, fixierte Netzausbauportfolio-Referenz | Speicher-MW/MWh, Land/Technologie, Status, Need-Flag | keine P12-2035-Expansion |
| `P13_INTERNAL_DISPATCH_PAIR` | with/without-Portfolio, gleiche Basis | dispatch, ENS, system costs, branch flows je Paar | Vergleichsachsen vollständig dokumentieren |
| `P14_H2_FROZEN_SENSITIVITY` | elektrisches Modell und präexpansive H2-Stundenlast | sensitivity `x`, Betrieb, freeze_witness, Status | separate Sensitivität, keine Base-Replacement |
| `P15_OPTIONAL_OPF` | explizites `run_opf` und LF-gekappte Kandidaten | OPF-Investition/Flows, LF-cap_reference, Solverstatus | optional; separate Methodenkennzeichnung |

### 3.1 Rohresultat-Vertrag (nicht bereits ein KPI)
`RawResultRecord` hat `result_id, run_id, stage_id, study_year, CY_id_if_applicable, interval_if_applicable, object_id, network_ref, carrier, quantity_type, unit, value, status, solver_witness_ref, data_freeze_ref, model_version, transform_lineage`. `null` ist nicht automatisch Nullmenge; explizite Nichtverfügbarkeit ist Status.

| Rohklasse | Beispielhafte `quantity_type` | Kennzeichnung |
|---|---|---|
| Ausbauentscheidung | `candidate_selected`, `candidate_units`, `new_transfer_MW` | stage-/candidate-/country-/corridor-gebunden |
| Netzbetrieb | `link_flow_MW`, `branch_flow_MW`, `N1_loading_ratio` | Richtung, Season, Contingency, Referenz |
| Erzeugung und Nachfrage | `generation_MW`, `demand_MW`, `unserved_power_MW` | Zeit- und CY-Indizes |
| Flexibilität | `DSR_dispatch_MW`, `curtailment_MW`, `storage_charge_MW`, `discharge_MW`, `soc_MWh` | Technologie- und Zustandsbezug |
| Wasserstoff | `electrolyser_input_MW_e`, `hydrogen_output_MWh_H2`, `h2_storage_state`, `h2_exchange` | Carrier- und LHV/HHV-Basis |
| Kosten | `investment_cost`, `variable_cost`, `start_cost`, `operating_cost`, `solver_objective` | Währung, Preisjahr, Kostenkomponenten |
| Vergleich/Sensitivität | `paired_dispatch`, `frozen_h2_input`, `optional_opf_capacity` | parent_run_refs und branch_type |

Fehlende oder solverunabhängig nicht verfügbare duale Größen gelten nicht als verpflichtendes Ergebnis, solange keine offizielle Fachanforderung dies verlangt. Dass zwei optimale Solves verschiedene Kandidaten wählen können, erfordert geeignete Ergebnisvergleichsorakel; Gleichwertigkeit nicht nur über elementweise identische `x` behaupten.

## 4. Berichtsfähige Resultate (separat von RawResult)
`SystemNeed` (Need-Klasse, Netz-/Korridor- bzw. Speicherbezug, Jahr, Mengeneinheit, Herkunft, nicht projektgenehmigt); `TransmissionCapacityNeed`; `StoragePowerAndEnergyNeed`; `FlexibilityNeed`; `ElectricityAndHydrogenImpact`; `SystemCostIndicator`; `OffshoreNeed`; `ReliabilityOrCurtailmentIndicator`. Jede Berichtsklasse benötigt eine `MetricDefinition` mit `formula_ref/version, input_raw_types, aggregation_dimensions, baseline/comparator, missing_value_policy, reporting_units, filter_rule, owner_approval`. Solange die methodische Formel fehlt, werden **nur Typ, Referenzen und erforderliche Metadaten** spezifiziert; weder Kostenvorteil noch ENS-KPI wird numerisch fingiert.

## 5. Tooladapter als überprüfbare Grenzen
**Import:** Prüfe Schema, Identität, UTC-Intervall, Einheiten, CY-Profilbezug, exogen/endogen, Kandidatenklassifikation, Link-/Flowrichtung, Parameterautorität, referenzielle Konsistenz. Nicht unterstützte Konstraintfamilie meldet `UNSUPPORTED_SEMANTICS`, **nicht** stiller Ersatz durch verwandte Toolschemas.

**Export:** Rückabbildung jeder endogenen Größe in `RawResultRecord` plus Konsistenzbeweise (Units, Indizes, Status, Vorzeichen, Solverzustand, Budget-/Kostenseparierung) und optionalem Fehler-/Gap-Manifest. Erst danach führt Postprocessing Report-Contracts aus. Ein syntaktisch valider YAML-/JSON-Transport garantiert keine mathematische Äquivalenz.

## 6. Offene Fach-/Verifikationsbedingungen
Methodikauthority O26, Stage-Transition/Real vs. Conceptual Kandidaten, Netzreduktionsorakel, Hydrogen-Detail, hydro classes, Storage-Limits, WACC/Discount, offshore detour, KPI-Formeln, P15-OPF-Entscheidung, numerische Akzeptanzgrenzen und originale Daten-Releases fehlen weiterhin. Die in anderen Forschungsworkstreams möglichen Methodikformalismen werden **nicht** als hier entschiedene Modellierungssprache vorweggenommen.
