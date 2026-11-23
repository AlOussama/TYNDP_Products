# Five finite examples of internal modelling freedom

| Pair | Executed finite witness | Exact limited scope | General equivalence |
|---|---|---|---|
| RC01_battery_SOC_vs_energy | PASS_SYNTHETIC | one idealized one-hour trace | E4 NOT_PROVED |
| RC02_EV_individual_vs_aggregate | PASS_SYNTHETIC | finite departure witness | E4 NOT_PROVED |
| RC05_angle_vs_cycle | PASS_SYNTHETIC | single 3-node equal-x DC triangle | E4 NOT_PROVED |
| RC03_electrolyser_const_vs_partload | PASS_SYNTHETIC | two admissible but non-identical output samples | E4 NOT_PROVED |
| RC07_investment_shared_vs_scenario_indexed | PASS_SYNTHETIC | two-scenario first-stage value | E4 NOT_PROVED |

For the electrolyser, two physically permitted outputs are deliberately **different**, showing permitted variation is not mathematical E4 equivalence. For the battery the SOC and MWh-state samples agree on one idealized external ledger only. The DC angle and cycle traces agree for one triangle, not across all topologies. These checks cannot replace formal proof or solver-model comparison.
