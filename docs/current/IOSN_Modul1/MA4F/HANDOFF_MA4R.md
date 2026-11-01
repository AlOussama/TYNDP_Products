# Handoff M1-MA4F → S-GOV / M1-MD1 / M1-MA4R

**Released technical fixture integration (not real):** cd71f36ddf07fb3ecc1cb4be5701a2586b9950c8
**Branch:** impl/iosn-m1-ma4f-fixture-integration-20261101
**CI:** https://github.com/AlOussama/TYNDP_Products/actions/runs/41315496732
**Evidence:** 92 tests PASS, five synthetic PyPSA-NetCDF roundtrips, all 16 static tables invariant, Snakemake 16/16 steps.
**Decision:** M1_MA4F_FIXTURE_INTEGRATION_QUALIFIED; REAL_SOURCE_NOT_QUALIFIED; M2_RELEASE=false.

## MD1 — one consolidated upstream source/M0 package, not repeated questions

MD1 Data Owner and M0 reference owner must deliver the immutable, source-hashed physical package required by MA1C IN-01..IN-10 and G1-C/D/E. Required are the exactly **five already selected** real weather IDs plus actual horizons (no reselection), physical PECD v4.2 wind/PV source bytes and masks/CRS/licensing, original generator/plant ID binding, PV MWp/DC→MW_AC conversion evidence, original Hydro region DAY/WEEK/53rd native intervals/MWh semantics and hydrological plant allocation, owner-approved Store/Link ports or explicit NOT_APPLICABLE, required DFT load files, and the ACTUALLY EXECUTED M0 DetailedNetworkReference/1.0.0 NetCDF+sidecar+full original source-to-view/asset and component capability mapping.

M0 Owner must independently witness source_revision_id, operating_state_id, canonical_revision_id, projection_id and source/policy hashes, original equipment, buses, capacities, 3W star and no-fabricated-geo policy. A normative design document or synthetic network is NOT enough.

If any required physical source is absent, MD1 must report M1_SOURCE_CONTRACT_BLOCKED. Do not emulate a real witness by editing MA4F fixture metadata.

## MA4R — single later real integration macro after MD1 and M0 approval

1. Start a separate isolated MA4R branch anchored on this tested MA4F code and the independently approved real M0/MD1 immutable SHAs. Make a **reviewed real-mode extension**; do not just switch the MA4F fixture-only evidence flag.
2. Build the exact original 5 weather sets across required planning horizons for the existing physical M0 network. Validate original generator/bus IDs, PEON/P2ON and PEOF/P2OF and PV ORIG/Regional geo grids, source CF units, PV clipping/MWp→AC, RoR availability, HRI/HPI/HOL energy intervals, HCL classified no-inflow, basin shares, and native MWh / modeled plant energy equality.
3. Fail closed for missing source profiles, missing hours, unauthorized source/horizon aliases, synthetic star geography, non-physical nearest-bus weather assignment, unqualified hydro conversion/ports, and any ambiguous Generator.p_max_pu owner conflict. Do not claim capacity factors are dispatch.
4. Materialize one full PyPSA Network NetCDF plus QA/ownership/energy ledgers per (horizon,weather_id). Compare ALL original static tables, loads_t.p_set and preexisting dynamic data before/after, verify PyPSA NetCDF export/import. Honor documented default-valued dynamic-column elision only with exact semantic equality.
5. Reconcile Demand/DFT only if physically witnessed under load owner strategy. Analyze memory/CPU with actual network sizes, snapshot counts and data precision; separate any authorized AC power-flow validation from simple availability binding.
6. Publish one MA4R producer commitment with real sources and tests as M1_REAL_REFERENCE_READY_FOR_INDEPENDENT_REVIEW, then commission an INDEPENDENT R-M1-MA4 technical/scientific reviewer. S-GOV alone decides any M1_DETAILED_REFERENCE_READY_FOR_M2 or S_GOV_M1_M2_RELEASED status after review.

## Responsibility matrix

| Owner | Responsibility |
|---|---|
| MD1 Data Owner | Actual five weather IDs, physical PECD/Hydro/DFT source bytes/versions/licenses/SHAs and real spatial/basin mapping |
| M0 Owner | Qualified existing M0 DNR/1.0.0, canonical/projection/source/operating IDs and original topology/ports |
| MA4R integration owner | Real five-case pipeline, original M0 invariance, energy/network/CPU/memory evidence |
| Independent R-M1-MA4 | Independent static, numerical and source validation on frozen MA4R commit |
| S-GOV / Project Owner | Integration review, main merge, eventual Module 2 gate |

**Current prohibitions:** no merge into main; no M2 release; no new weather selection or three-source-to-five fallback; no aggregation/network reduction; no Store/Link dynamic write without explicit owner clearance; no synthetic data passed off as real.

## Synthetic reproduction command (only synthetic fixtures)

    python -m pip install -r config/iosn_m1/MA4F_REQUIREMENTS.txt
    python -m pip install --no-deps -e ".[test]"
    PYTHONPATH=.:tests/iosn_m1 python -m pytest -q
    PYTHONPATH=.:tests/iosn_m1 python tests/iosn_m1/fixture_ma4f.py --out /tmp/ma4f_fixture_e2e
    PYTHONPATH=.:tests/iosn_m1 snakemake -s Snakefile.iosn_m1_ma4f --configfile /tmp/ma4f_fixture_e2e/snakemake_fixture_config.yaml --cores 2 -n
    PYTHONPATH=.:tests/iosn_m1 snakemake -s Snakefile.iosn_m1_ma4f --configfile /tmp/ma4f_fixture_e2e/snakemake_fixture_config.yaml --cores 2

Fresh checkout and no prior output directory required. This is **not** a real-data qualification command.
