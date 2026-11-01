# MA3 Hydro — runtime contract and physical semantics

**Contract:** IOSN-M1-MA3/1.0.0. **Scope:** bind Hydro energy to pre-existing M0 assets, never construct or mutate network topology. **Current real data:** NOT_PROVIDED.

## Inputs and binding authority

| File | Contract |
|---|---|
| Hydro manifest JSON | Exactly five externally selected weather IDs, horizon, source SHA256/version/correction/license, source semantics/tech/basin, original timezone, temporal policy, M0 revision |
| Native source interval CSV | start, end, energy_mwh; explicit UTC offset for each original half-open interval; verified DAY or WEEK resolution |
| Hydro allocation CSV | hydro_area_id, hydro_tech, asset_id, share, hydrological/TSO evidence, source-to-model energy conversion, approved port |
| M0 asset inventory CSV | asset_id, existing_component_id, component_class, hydro_tech, bus_id, network_revision_id, role, p_nom_mw, max_hours, efficiency_dispatch, e_nom_mwh |
| Snapshot CSV | timestamp and duration_hours; uninterrupted one-hour UTC offset-aware timestamps; output becomes timezone-naive UTC |
| REAL-only M0 reference | Actual PyPSA network, sidecar, full original identity mapping, source and capability witness, MA1C qualification |

MA1 uses network_revision_id; MA1C has identified subsequent M0 CAN/2.0.0 fields canonical_revision_id and projection_id, still pending owner alignment. Real M0 qualification **cannot** proceed by silently relabeling these fields.

The optional strict Open-TYNDP 2026 normalizer reads a raw WEEK/DAY table with a **selected exact WS### column**, an independently verified period-key-to-boundaries CSV, SHA256 for both files, source revision and timezone. It never invents Jan01+7days intervals or chooses the first available WS column.

## Conservation equations

For each native interval k of source area z, use actual UTC duration h[k] = (end-start)/3600. With independently evidenced asset share B[a,z] and conversion c[a,z]:

- E_native[a,z,k] = B[a,z] × E_source[z,k], with B >= 0 and sum over assets B = 1.
- E_model[a,z,k] = c[a,z] × E_native[a,z,k], c in (0,1] and evidence required.
- P_model[a,z,k] = E_model[a,z,k] / h[k].
- Separate audit equations: sum over assets E_native = E_source; sum over complete hourly snapshots P_model × 1h = E_model.

The source-conservation check occurs **before** source-to-model conversion. A hydraulic MWh value is never implicitly identical to electricity MWh. Already storage-energy-equivalent inflows use c=1; discharge efficiency applies later to StorageUnit dispatch and must **not be double-counted**.

Only the explicitly evidenced UNIFORM_WITHIN_NATIVE_INTERVAL disaggregation policy is supported. Uniform within each native interval is energy-conserving, **not actual hourly observed water flow or generation**, and needs temporal_policy_evidence_ref. No 168/24 divisor except when actual duration is exactly 168/24 hours. A 53rd or partial week, leap-year or 23/25-hour DST day uses true elapsed UTC hours.

## Source-to-PyPSA port matrix

| Type | Valid treatment |
|---|---|
| HRR Run of river | Existing Generator only from evidenced AVAILABLE_GENERATION_ENERGY_MWH or explicitly converted hydraulic energy: stage generators_t.p_max_pu = MW_available / unchanged p_nom (availability, not dispatch); optionally approved StorageUnit if that is actual M0 plant model |
| HRI Reservoir | Natural inflow to existing StorageUnit state of charge: storage_units_t.inflow in MW |
| HPI Pondage | Same energy-state qualification, distinct plant type and available buffer |
| HOL Open-loop pumped storage | Only separately sourced **natural** inflow; pump electricity is not included in natural inflow |
| HCL Closed-loop/pure pumped storage | Evidenced NO_NATURAL_INFLOW_BY_DESIGN statement, not an artificial missing-source zero time series |
| HRO/HPO/HRG | Generation-energy products, not natural inflow; rejected as inflow |

A PyPSA **StorageUnit** has a native inflow input to its state of charge. A **Store** does not. For Store+Link, a pre-existing auxiliary Generator on the store-energy bus must have an explicit M0-approved inflow port and special generators_t.p_set allowlist permission; MA3 emits only store_link_staged.csv. MA4 must verify full Store/Link charging and discharging directions, bus carrier, efficiencies and existing setpoints before any injection. No Store/Link/Generator is created.

RoR inferred MW above existing p_nom is blocked instead of clipped. StorageUnit natural inflow is not falsely capped at discharge p_nom, but p_nom, max_hours and discharge efficiency must be physically valid; feasibility/spillage is separately qualified in MA4.

## How to execute when external data actually exist

First normalize a raw TYNDP WEEK/DAY file, supplying original raw data bytes, SHA256 and independently witnessed interval boundaries:

~~~sh
python -m scripts.iosn_m1.hydro.normalize_tyndp2026 --raw RAW.csv --bounds VERIFIED_BOUNDS.csv --source-column WS003 --weather-id EXTERNAL_ID --timezone UTC --raw-sha256 VERIFIED_RAW_HASH --bounds-sha256 VERIFIED_BOUNDS_HASH --native-unit MWh --source-version VERIFIED_VERSION --bounds-evidence-ref VERIFIED_EVIDENCE --output NATIVE_INTERVALS.csv
~~~

Then run per external scenario:

~~~sh
python -m scripts.iosn_m1.hydro.cli --manifest HYDRO_MANIFEST.json --allocations HYDRO_ALLOCATION.csv --assets M0_ASSETS.csv --snapshots UTC_HOURLY.csv --source-root VERIFIED_SOURCE_DIRECTORY --planning-horizon 2030 --weather-id EXTERNAL_ID --output-dir OUTPUT_DIRECTORY
~~~

For REAL mode also provide --m0-network and --m0-sidecar, plus an actually qualified MA1C/M0 witness. The weather ID in these commands is a **placeholder**, not one of the unavailable project IDs. The Snakemake rule is in rules/iosn_m1_hydro.smk and uses config key iosn_m1_hydro (manifest, allocations, assets, source_root, snapshots keyed by horizon and weather ID, optional m0_network_flags). All five source CSV files are dependencies, not fake scenarios.

Outputs: hydro_inflow.csv (existing StorageUnit MW); ror_availability.csv (existing Generator per-unit availability); store_link_staged.csv (approved auxiliary port MW, **not auto-written**); interval_energy_ledger.csv (native period MWh closure); hydro_allocation_ledger.csv (per original asset energy and conversion); closed_loop_policy_ledger.csv (evidenced HCL noninflow); qa.json (source gate, file-count, time and energy checks, no-static-write assertion).

No wind/PV, DFT demand, invented dispatch, new topology, or network aggregation exists in this adapter.
