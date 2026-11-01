# M1-MA2 — PECD v4.2 Renewable Profiles & Original-Asset Mapping

**Date:** 2026-11-01  
**Owner scope:** MA-2 only (Wind_Onshore, Wind_Offshore, Solar PV Utility, Solar PV Rooftop)  
**Assigned immutable base:** `AlOussama/TYNDP_Products@2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994`  
**Working branch:** `impl/iosn-m1-ma2-pecd-res-20261101`  
**Producer disposition:** `M1_RES_FIXTURE_QUALIFIED__REAL_DATA_GATE_BLOCKED` (not `M1_RES_REAL_DATA_QUALIFIED`).

## 1. Source study and reuse decision

Read the full MA2 assignment, MA1 source and spatial audit, MA1 logical YAML contract, M1 architecture/spatial plan, and M0 DetailedNetworkReference v1 specifications (30, 40, 60, 70) at `0275f48231a0794bea324b9cab34700bb0de8f5b`. Verified Open-TYNDP `tyndp-2026@71a3a9a15b77114cd79458bceabc98e1a64dd58a`: `scripts/sb/prepare_tyndp_pecd_release.py`, `clean_tyndp_pecd_data.py`, `build_renewable_profiles_pecd.py`, `rules/sb.smk`, `data/tyndp_technology_map.csv`, `data/tyndp_versions.csv`.

The upstream MIT-licensed *parser conventions* are adapted: raw PECD 10 metadata lines + `Date`, `Hour` 1..24, `WS###` field; alternatively prepared CSV or explicitly timestamped ISO CSV. The Open-TYNDP `TYNDP_NODE` busmap, `buses_tyndp`, name substitutions, safe planning horizon, `get_wscenario_tyndp(...)[0]`, missing-column zero/mean filling, global year overrides, and full upstream network composition are **not** used. Source code is original adaptation, not verbatim upstream copy. Upstream PECD `4.2+pre-built.0.1` dated 2026-08-13 and corrected TYNDP 2026 inputs dated 2026-08-21 are not considered mutually verified without actual file evidence. Upstream MIT code license does **not** establish PECD data-use rights.

## 2. Implemented interfaces

- `scripts/iosn_m1/res/adapter.py`: strict five-ID/horizon manifests, SHA256-verified source catalogue, TYNDP Date/Hour and ISO readers, UTC normalization with DST fail-closed, hourly/year coverage, M0 identity+revision gates, exact carrier-to-variant crosswalk, asset-to-profile matching, GeoJSON official-mask point-in-polygon with `pyproj` CRS conversion, offshore/synthetic-bus veto, MW-verified composite weights, PV MWp→AC conversion with explicit clipping evidence, xarray `renewable_cf(time, existing_generator_id)`.
- `scripts/iosn_m1/res/run.py`: command-line scenario compiler, NetCDF roundtrip check, source, assignment and catalogue ledgers, QA JSON. No PyPSA network mutation. Existing `Generator.bus`/`p_nom` are read-only. Dispatch is not synthesized.
- `rules/iosn_m1_res.smk`: opt-in per `(horizon,weather_id)` inputs and outputs; five external IDs required, native files registered as dependencies; no implicit network build or hydro/DFT.
- `config/iosn_m1/MA2_SCHEMA_V1.json`, `MA2_SNAKEMAKE_EXAMPLE.yaml`: versioned physical fields/vocabulary and illustrative config. `data/iosn_m1/technology_crosswalk_v1.csv`, source/assignment CSV templates: no fictitious real matching.
- `tests/iosn_m1/test_res_adapter.py`: self-contained PECD/M0 **synthetic** fixtures (including generated source files for five different fixture weather IDs). No fixture is claimed to be an ENTSO-E PECD or CGMES source.

**Important physical boundary:** `m0_res_registry.csv` is a read-only, SHA256-pinned M0 identity projection containing **all** generator IDs including `res_profile_required=true/false`. The resulting output contains only the eligible renewable generator IDs; other generators remain untouched. M0 owner must qualify that the registry and sidecar match the actual PyPSA `Network.generators` table; the MA2 adapter alone cannot confer this qualification.

**PV policy:** For a PECD `MW_per_MWp` signal `c_DC`, source-verified DC panel capacity `P_DC` and existing M0 AC rating `P_AC=p_nom`, the *approved* modeled AC availability is `min(c_DC * P_DC/P_AC, 1)`; only used when `pv_source_ac_semantics=UNCLIPPED_DC_NORMALIZED`, `pv_clipping_policy=CLIP_AC_AT_P_NOM_WITH_APPROVED_EVIDENCE` and inverter/conversion provenance are supplied. This is an explicitly authorized simplifying clipping policy, **not** a claim that the actual plant output is known or that a source-provided CF has not already been clipped. Without evidence: BLOCK. If source is already `MW_per_MW_AC`, no new DC conversion is performed and AC-unit provenance is required.

**Composite policy:** A multi-region generator is a *pre-existing M0 generator*, never newly assembled. Mapping weights are established by documented component MW for Wind or DC MWp for PV (sum shares must equal corresponding existing capacity/basis). `CF_g(t) = sum_p w_gp CF_p(t)`, then PV DC/AC conversion. No interpolated wind profile or reallocated electrical asset. A genuine geographically composite multi-plant ID needs plant-specific share evidence from M0 or the owner.

## 3. Executed fixture evidence

Command (local Python 3.13 environment):

```bash
PYTHONPATH=. pytest -q tests/iosn_m1/test_res_adapter.py
```

**Result: 20 passed.** Verified five distinct weather-ID outputs, exact original IDs and two onshore generators using the same PEON series at different buses, offshore location-vs.-landfall guard, PV ORIG/region and DC→AC clipping, composite 40/60 MW shares, explicit source hashes, NetCDF roundtrip, no input M0 asset table or reference-manifest byte change. Negative tests: incomplete five sets, unselected WS fallback, corrupt/missing file, synthetic 3W bus, offshore bus proxy, ambiguous overlapping masks, missing PV evidence, invalid MW shares, missing native hour, local DST ambiguity/nonexistence, missing bus proxy provenance, wrong generator carrier. Also tested TYNDP raw10 parser and ISO UTC offset input.

Runtime module versions in local test environment: Python 3.13, pandas 2.2.3, xarray 2026.4.0, shapely 2.1.2, pyproj 3.7.2, pytest 9.0.2. **Snakemake was not installed, hence rules were statically prepared but not executed. PyPSA was not installed; neither network import/export nor composition was run.** No actual PECD source file or actual M0 sidecar was supplied to this execution; no real-data MW coverage claims.

## 4. Gate matrix and bounded findings

| Gate | Status | Evidence/requirement |
|---|---|---|
| MA2-F0 contracts/static | PASS | Immutable MA1/M0 specs and Open-TYNDP reader/API study |
| MA2-F1 input parsing, five fixtures | PASS / FIXTURE | 20 tests, native hour checks and source-hash guards |
| MA2-F2 original M0 IDs and source mapping | PASS / FIXTURE | all renewable fixture IDs covered, zero topology writes; real ID ledger unwitnessed |
| MA2-F3 geo, offshore, PV, composite | PASS / FIXTURE | positive and negative geo/ratio/weight cases |
| MA2-F4 source NetCDF roundtrip | PASS / FIXTURE | in-memory vs. reread `renewable_cf` exact numeric/index match |
| MA2-F5 Snakemake execution | NOT_EXECUTED | Runtime not available; validate in authorized integration runner |
| G1-C M0 real reference | BLOCKED | Actual DetailedNetworkReference v1, original IDs/asset geo, sidecar and M0 import QA not witnessed |
| G1-D real five-WS PECD | BLOCKED | Five preselected **real** weather IDs, licenses, corrected release, SHA256 files, real masks not witnessed |
| MA2 final real gate | NOT_QUALIFIED | No real source-to-generator roundtrip, grid/PEON/PEOF MW coverage, independent witness |

**No reason to promote fixture evidence to real-data status.** Two verified weather datasets may never be silently replaced with placeholder outputs from the three populated TYNDP 2026 `WS` columns per horizon.

## 5. Single consolidated real-data input list (not microtasks)

1. From MA1C: five finalized actual weather IDs and horizon binding; per `(horizon,weather_id,profile_id)` raw/offline CSV, exact SHA256, version/correction/date, license, time basis/year, technology/unit and geographic-resolution product, with authoritative PECD regions/masks or explicit profile ID crosswalk. Whether the preliminary August PECD prebuilt matches the corrected August TYNDP release must be evidenced.
2. From M0: full actual DetailedNetworkReference v1 and revision keys, complete unmodified Generator/asset/source-ID crosswalk, `Generator.carrier`, `bus`, `p_nom`, geo-quality, original plant/offshore coordinates or explicitly qualified proxy, synthetic bus roles; qualifier that `res_profile_required` correctly covers *all* RES assets.
3. For PV: authoritative MWp DC and MW AC capacities and documented inverter/clipping semantics, or a source-qualified AC-normalized availability product. For multi-region: verified per-plant MW/MWp allocations. For offshore: the turbine/park location or official offshore profile region, not shore connection bus.
4. Integration/runtime: Snakemake/PyPSA installed at approved pins, MA1C physical source witness, and independent end-to-end validation against original M0 network in MA4.

**Decision:** `M1_RES_FIXTURE_QUALIFIED__REAL_DATA_GATE_BLOCKED`. This branch is suitable for isolated upstream review and subsequent real-data qualification but is not a declaration that M0 or the five weather datasets have been physically integrated.

## 6. Concurrent MA1C actual-source witness, 2026-11-01

The separate upstream physical-source audit was published on branch `research/iosn-m1-ma1c-source-witness-20261101` after implementation began. Its `CONTRACT_FREEZE_DECISION.md` declares `M1_SOURCE_CONTRACT_BLOCKED`. All five slots in `FIVE_WEATHER_ID_LEDGER.csv` remain `NOT_PROVIDED`, and the actual PECD bytes/masks and executed M0 DetailedNetworkReference package remain absent. This independently confirms the MA2 real-source block. The MA1C handoff further requires an M0 owner handshake on `network_revision_id` versus the possible newer `canonical_revision_id`/`projection_id` DNR/CAN-2.0.0 semantics; the MA2 implementation deliberately retains the frozen M1-MA1 YAML field until an approved versioned mapping is received.

The 20th-test scope includes separate PEON/P2ON onshore and PEOF/P2OF offshore profile-code branches plus general IANA timezone verification. No five real weather IDs were inferred from official three-scenario TYNDP-2026 lists.
