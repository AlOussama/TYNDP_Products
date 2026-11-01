# IoSN M1 / MA2 PECD RES adapter

The adapter reads versioned PECD v4.2 wind-onshore, wind-offshore, PV-utility and PV-rooftop capacity factors and binds them exclusively to **original M0 existing_generator_id**. It does not read or mutate a PyPSA network: static CGMES/PyPSA topology, generator IDs, buses, p_nom and all other component tables remain unchanged.

## Requirements and usage

Python 3.11+, pandas, numpy, xarray, scipy, shapely, pyproj. PyPSA and Snakemake are **not** dependencies of the standalone compiler. Use PYTHONPATH=. when executing at repository root. For production Snakemake separately include rules/iosn_m1_res.smk in your main Snakefile and set config/iosn_m1/MA2_SNAKEMAKE_EXAMPLE.yaml with real verified paths. The example paths and weather IDs are placeholders, not sanctioned source records.

Execute with the following required arguments:

    python -m scripts.iosn_m1.res.run --weather-manifest <JSON> --source-catalog <CSV> --m0-assets <CSV> --m0-reference-manifest <JSON> --technology-crosswalk data/iosn_m1/technology_crosswalk_v1.csv --assignment-map <CSV> --geometry-registry <OFFICIAL_MASK_GEOJSON> --horizon 2030 --weather-id <ACTUAL_EXTERNAL_ID> --output-cf renewable_cf.nc --output-source-ledger source_ledger.csv --output-assignment-ledger assignment_ledger.csv --output-profile-catalog profile_catalog.csv --output-qa qa.json

The weather JSON must contain exactly **five externally selected weather IDs**, an explicit planning horizon, evidence class FIXTURE or REAL_SOURCE_CANDIDATE, time_semantics=HOURLY_UTC_NAIVE_OUTPUT and full_native_year_required=true for real inputs. Source catalog entries must exist for each of those five weather IDs for every profile and include individual SHA256, corrected source revision, technology, source unit, year/time origin, file and geometry evidence.

CSV reader formats:
* TYNDP_RAW10_DATE_HOUR: upstream-style 10 metadata rows, Date, Hour (1..24), WS###; ISO year from the source catalog.
* TYNDP_DATE_HOUR: prepared Date, Hour (1..24), WS###.
* ISO_CSV: timestamped time,cf columns. ISO offset information is converted to UTC. A naive local timestamp needs a source timezone, and DST ambiguity or nonexistent local time is rejected.

Input m0_generator_registry.csv must list **every** unchanged M0 generator, including res_profile_required=true/false, a stable source asset identifier, original generator and bus IDs, p_nom, carrier, network revision, bus role and geo-quality. Reference manifest must hash that CSV, state total generator_count, network_revision_id, source_set_hash, mapping_policy_hash and reference the M0 sidecar and identity ledger. The actual M0 owner must independently attest that this projection is faithful to the original M0 network.

The asset_profile_map is keyed by network_revision_id, planning_horizon, asset_id, existing_generator_id, existing_bus_id and source_profile_id; source method and evidence are mandatory. Location matching accepts official/verified per-profile GeoJSON polygons and explicit EPSG CRS; offshore landfall or a synthetic 3W star is rejected as turbine location. Region-level profiles do not purport to provide grid-cell resolution. Multi-profile mappings require documented MW/MWp shares summing exactly to the original capacity basis.

For PECD PV MW/MWp, a source-verified DC nameplate rating, unchanged AC p_nom, unclipped DC-normalized semantics, approved clipping policy and conversion evidence are mandatory. With the approved simplifying policy, effective availability factor is min(PECD_CF * DC_MWp / AC_MW, 1); without evidence the adapter blocks. For PECD already normalized on AC MW, the conversion is not applied. For wind the source unit must be MW/MW.

Emitted NetCDF variable: renewable_cf(time, existing_generator_id). Other outputs: source_ledger.csv, assignment_ledger.csv, profile_catalog.csv, qa.json. This is an availability constraint, **not dispatch**. A generated QA record always retains real_data_qualified=false until a separate MA1C/M0/MA4 real-source qualification and independent review.

For verified fixture tests: PYTHONPATH=. pytest -q tests/iosn_m1/test_res_adapter.py. See docs/current/IOSN_Modul1/MA2/EXECUTION_REPORT.md for the qualified evidence scope.
