# MA3 — immutable source study, reuse, physics boundaries

**M1 source contract:** AlOussama/TYNDP_Products at 2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994.

**Open-TYNDP source anchor:** open-energy-transition/open-tyndp, branch tyndp-2026, 71a3a9a15b77114cd79458bceabc98e1a64dd58a. Directly inspected: [clean_tyndp_hydro_inflows.py](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/clean_tyndp_hydro_inflows.py), [build_tyndp_hydro_profile.py](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/scripts/sb/build_tyndp_hydro_profile.py), [technology crosswalk](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/data/tyndp_technology_map.csv) and [Snakemake rules](https://github.com/open-energy-transition/open-tyndp/blob/71a3a9a15b77114cd79458bceabc98e1a64dd58a/rules/sb.smk).

**Independent source-witness authority:** [MA1C source audit](https://github.com/AlOussama/TYNDP_Products/blob/f366f8162e1023ff959721d5fed14ad80dcba890/docs/current/IOSN_Modul1/MA1C/CONSOLIDATED_EXECUTION_REPORT.md) at f366f8162e1023ff959721d5fed14ad80dcba890. Decision M1_SOURCE_CONTRACT_BLOCKED; five project weather IDs and real Hydro/M0 evidence not supplied.

| Reviewed behavior | MA3 disposition |
|---|---|
| Open-TYNDP WEEK/DAY and WS### input format | Strict selected-column and SHA-verified parser designed independently |
| Synthetic weekly index Jan01 + 7 days for 53 periods | Rejected; witnessed original period-key boundaries required |
| Reindex + forward fill + divide by fixed 168/24 | Rejected; actual elapsed UTC period with exact hourly cover |
| fillna(0) for missing regions/nodes | Rejected; missing source blocks; genuine hashed source zero allowed |
| Three available TYNDP weather scenarios or first scenario fallback | Rejected; five externally assigned weather IDs are not inferred |
| TYNDP bus dimension as Hydro region | Replaced with documented hydro_area_id + actual original M0 asset ID, not electrical bus coordinates |
| Crosswalk HRR/HRI/HPI/HOL/HCL | Separate source-energy and port type semantic checks; HCL is no-natural-inflow policy only |
| Open-TYNDP regional profile NetCDF | MA3 uses original-asset long-form time series and double energy ledgers; composition occurs only at MA4 |

PyPSA's [StorageUnit definition](https://docs.pypsa.org/latest/user-guide/components/storage-units/) distinguishes state-of-charge inflow from generated power, while the [Store definition](https://docs.pypsa.org/latest/user-guide/components/stores/) has no built-in inflow and describes a separate auxiliary injection component. The modelblocks-org [module_hydropower](https://github.com/modelblocks-org/module_hydropower/tree/1daecde3e653d53da3f1ae740cc70d5d14d480eb) is useful for basin-to-plant methodological comparisons, **not** an original PECD source or permitted artificial inflow replacement.

**Licensing:** inspected upstream hydro scripts are SPDX MIT. The MA3 implementation is newly authored rather than copied verbatim. Data rights/licensing remain NOT_VERIFIED until actual source bytes and license notices are delivered; upstream code licensing does not grant source-data rights.

**Limits:** no physical Hydro input samples, true source bounds, basin shares, full five-weather manifest, M0 DNR PyPSA+sidecar, qualified approved Store/Link port or resolved M0 CAN/2.0.0 projection identity bridge are currently available. The uniform hourly distribution is a declared allocation policy, not measured hourly flow. Shares are constant across source intervals in adapter v1; seasonally varying shares would require a separately approved versioned contract. Real operating feasibility, storage spillage, pumping and power flow are **not** proven by energy-integral tests. Snakemake rule is committed but Snakemake runtime execution is not claimed.
