# M1-MA2 → Integration owner / MA4

**Producer status:** `M1_RES_FIXTURE_QUALIFIED__REAL_DATA_GATE_BLOCKED`  
**Branch:** `impl/iosn-m1-ma2-pecd-res-20261101`  
**Baseline:** `2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994`  
**Output contract:** `renewable_cf(time, existing_generator_id)` (xarray/NetCDF), separate files per `(planning_horizon, weather_id)` and `source_ledger.csv`, `assignment_ledger.csv`, `profile_catalog.csv`, `qa.json`.

MA4 must treat this as an **unqualified producer**, not a completed PECD real-data source. Accept only the actual immutable M0 source-to-view ID crosswalk, the entire static component ledger and the MA1C qualified PECD five-set witness. Check `qa.real_data_qualified` (currently deliberately `false`), m0 revision/source hashes, source file hashes and native UTC interval before writing any `generators_t.p_max_pu`; do not write `generators_t.p` or any static `generators`, `buses`, `lines`, `transformers`, `links`, `storage_units`, `stores`, `loads`.

After new real sources become available, use the same contract and run one complete qualification across all supplied horizons and the five *existing* IDs, not a new weather-year choice. Compare all renewable M0 `p_nom` MW coverage and every generator/technology/region, verify AC/DC PV clipping and offshore original-plant position, original source CF vs emitted NetCDF and PyPSA NetCDF reimport. For M0 comparison, compare **every** static table pre/post (including `p_nom`, `bus`, original ID order) and preexisting time-dependent attributes before overwriting. Require an independent reviewer. This does not authorize hydro, DFT, PF, grid reduction or cross-chat merges on the MA2 branch.

Real-data release condition: MA1C G1-C/G1-D witnesses + complete five-WS PECD source and M0 original assets + Snakemake/NetCDF integration + independent QA. Otherwise remain `M1_RES_BLOCKED_MISSING_SOURCE` regardless of fixture tests.
