# ML-R04 — zehn synthetische, analytisch prüfbare Referenzfälle

Alle Parameter und Zahlen sind **ausschließlich illustrative Testparameter**. Der C01/C08-Wert 0,2 ist **kein echtes Wettergewicht**; die fünf echten gemeinsamen Gewichte sind numerisch offen und extern zu liefern. Die 2035/2040/2050-Läufe sind eigenständige Studien, die CY1–CY5-IDs gehören pro Zieljahr in ihr eigenes Manifest.

|Fall|Falsifizierbare Haupteigenschaft|Erwartetes positives Orakel / Negativprobe|
|---|---|---|
|[C01](./C01_five_weather_shared_investment.md)|Fünf gewichtete Wetterfälle – eine Investition|{"common_x_mw":2,"ens_mw":[0,0,0,0,2],"weighted_ens_mwh":0.4,"capex_eur":6,"weighted_ens_cost_eur":4,"objective_eur":10} / Gegenprobe im Falltext|
|[C02](./C02_broken_nonanticipativity.md)|Absichtlich fehlende Nichtantizipativität|{"faulty_objective_eur":8.8,"valid_objective_eur":10,"investment_values_mw":[1,1,2,2,2],"test_status":"FAIL"} / Gegenprobe im Falltext|
|[C03](./C03_time_resolution_units.md)|Zeitauflösung, UTC, MW-/MWh-Bilanz|{"energy_mwh":1,"cost_eur":50,"bad_naive_sum_of_mw":2} / Gegenprobe im Falltext|
|[C04](./C04_dc_flow_versus_market_link.md)|Vermaschtes DC-Flussgesetz gegenüber steuerbarem Marktlink|{"dc_physical_AB_mw":60,"dc_physical_AC_mw":30,"dc_physical_CB_mw":30,"link_variant_AB_mw":90,"physical_link_flow_difference_mw":30} / Gegenprobe im Falltext|
|[C05](./C05_network_aggregation_conservation.md)|Netzaggregation – notwendige Erhaltung des Cut-Flusses|{"cluster_x_mw":50,"cluster_y_mw":-50,"cut_x_y_mw":50,"energy_through_cut_mwh":50} / Gegenprobe im Falltext|
|[C06](./C06_equivalent_lp_formulations.md)|Äquivalente algebraische LP-Formulierungen|{"opt_x":4,"opt_y":0,"opt_slack":0,"optimal_objective":8,"projection_equivalent":true} / Gegenprobe im Falltext|
|[C07](./C07_multiple_optimal_portfolios.md)|Mehrfach optimale Investitionsportfolios|{"all_objectives":1,"invariant_total_mw":1,"distinct_vectors":3} / Gegenprobe im Falltext|
|[C08](./C08_broken_kpi_aggregation.md)|KPI-Zeit- und Wetteraggregation – positive/negative Fälle|{"ens_mwh_by_weather":[1,3,2,0,4],"weighted_ens_mwh":2,"weighted_ens_cost_eur":200,"unweighted_ens_mwh":10} / Gegenprobe im Falltext|
|[C09](./C09_unsupported_mandatory_capability.md)|Fehlende verpflichtende Toolfunktion|{"test_status":"UNSUPPORTED","overall_conformance_pass":false} / Gegenprobe im Falltext|
|[C10](./C10_optional_opf_conditional.md)|Optionale OPF-Variante und bedingte Pflichtprüfungen|{"off_test_status":"NOT_APPLICABLE","on_pass_test_status":"PASS","on_fail_test_status":"FAIL","on_unsupported_test_status":"UNSUPPORTED"} / Gegenprobe im Falltext|

`oracles.json` ist eine deklarative Fixture-Liste mit Modelltext, Parametern und analytischen Erwartungen; `run_reference_oracles.py` prüft ohne fremde Solver nur ausgewählte arithmetische Aussagen und Mutanten. Er ersetzt weder V3-Generatorprüfung noch V4-Solverevidenz. Der ursprüngliche MA01-SR-010-Draft weist noch *drei* Wetterfälle aus; die vom Nutzer bestätigte **D4-Forschungsüberlagerung** mit fünf Fällen ist hier transparent als Abweichung ausgewiesen, nicht normativ freigegeben.

**Harness usage:** `python3 run_reference_oracles.py` aus diesem Verzeichnis. Das Programm gibt nur `SYNTHETIC_ORACLE_SELF_CHECK` aus. Der globale MA01-/Tool-Nachweisstatus bleibt `NOT_EXECUTED`, G1 bleibt `BLOCKED`.
