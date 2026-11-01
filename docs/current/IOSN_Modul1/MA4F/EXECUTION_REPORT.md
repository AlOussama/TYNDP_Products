# M1-MA4F — Consolidated Fixture Integration and Interface Reconciliation

**Date:** 2026-11-01
**Repository:** AlOussama/TYNDP_Products
**Isolated branch:** impl/iosn-m1-ma4f-fixture-integration-20261101
**Tested code SHA:** cd71f36ddf07fb3ecc1cb4be5701a2586b9950c8
**Complete CI:** https://github.com/AlOussama/TYNDP_Products/actions/runs/41315496732
**Evidence artifact:** https://github.com/AlOussama/TYNDP_Products/actions/runs/41315496732/artifacts/13087730084
**Exit status:** M1_MA4F_FIXTURE_INTEGRATION_QUALIFIED
**Source status:** REAL_SOURCE_NOT_QUALIFIED
**M2 release:** FALSE

## 1. Authority, sources and immutable component reuse

- Authoritative S-GOV handoff: 03fa261850da8c940283668741bb7a17c46bd769, §1.
- S-GOV consolidation: 91f5d5f4df23188478764b2149928d3f3939a426.
- Common integration base: 2c0b482f0cec8b3e0fbc2e59a814e7d6fc66a994.
- MA1C physical data gate: f366f8162e1023ff959721d5fed14ad80dcba890 — BLOCKED.
- MA2 Wind/PV producer: 11700baa8df8cafc6bd71b96998f8b2bca647ca0.
- MA3 Hydro producer: b3b9bf133d1b5c968323a31f8ac76090f1f2e182.
- M0 CAN/2 and DNR/1.0 normative work: b1e284996fa69f81651daf9150b829e6a42e4ce3; M0 95/96: ba55e4a12819a88605474606888ca23ee2108584.

The first integration commit c1fd58e29d9c452c772458f3f5a3958c9d970419 copied 50 original MA1C/MA2/MA3/S-GOV blobs onto the isolated common-base branch, without editing the producer branches or main. Hydro adapter blob f3fa38928ca9eedc701dcbdcbd1ebec1e6a63308 remains byte-identical. The one shared package initializer chose MA3 blob 19d19604cc7cf5db21bfe6985820ef049b89422b. The MA2 adapter required a one-line actual regression fix: bitwise NOT of Pandas boolean was replaced with Python logical not in the synthetic 3W-star guard; final blob 823fc3084f349077f5d1c443d68bc2b57a4325b0, original MA2 blob 66fe4772860e8f6fadcf39a7be980d13244ee647.

No M0 components were added to, removed from, aggregated or edited in the **input** network. No weather year was selected. Only clearly marked synthetic reference network creation and composition was performed.

## 2. Implementation and interfaces

- MA2 producer scripts/iosn_m1/res/{adapter.py,run.py} retains original PECD source spatial/technology validation, PV MWp/DC vs MW_AC clipping, five-set UTC checks, and emits renewable_cf(time, existing_generator_id), ledgers and QA. Availability is NOT dispatch.
- MA3 producer scripts/iosn_m1/hydro/{adapter.py,cli.py} retains native MWh DAY/WEEK interval validation, basin/TSO shares and native hourly energy conservation. It emits hydro_inflow.csv, ror_availability.csv, store_link_staged.csv, interval-energy ledger, hydro-allocation ledger, closed-loop HCL absence ledger and QA. Uniform hourly distribution is a documented assumption, not an hourly source measurement.
- New single PyPSA writer scripts/iosn_m1/compose.py owns all write operations, original-target-ID checks, exact five-ID/horizon/UTC axis, source SHA/QA consistency, M0 source-to-view ledger, 3W synthetic-bus restrictions, fail-closed collision and prior profile overwrite policy. It writes a NEW network file and never overwrites M0.
- Versioned contracts: schemas/iosn_m1/master_input_manifest_1_0_0.json; m0_dnr_identity_bridge_1_0_0.json; target_ownership_1_0_0.json. The legacy producer network_revision_id is authorized to equal canonical_revision_id ONLY, never projection_id or source_revision_id.
- Orchestration: Snakefile.iosn_m1_ma4f includes rules/iosn_m1_res.smk, rules/iosn_m1_hydro.smk and the sole new rules/iosn_m1_compose.smk. The shared Snakemake manifest is strictly fixture-only. Inputs include producer source manifests/catalog and QA files, exact five weather source files and immutable M0.
- Dependency BOM: config/iosn_m1/MA4F_REQUIREMENTS.txt, pins PyPSA/Pandas/NumPy/SciPy/xarray/Geo/Snakemake/pytest; resolved full transitive pip freeze recorded in the successful CI artifact.

**Target ownership per scenario:** 5 Wind/PV Generator.p_max_pu targets (MA2); 1 disjoint run-of-river Generator.p_max_pu target (MA3); 2 StorageUnit.inflow targets (MA3). All 8 source-target ownership entries must be disjoint, on existing original IDs and non-synthetic buses. Store/Link Generator.p_set is always staged and not applied without M0 owner authorization. No unqualified DFT inputs are used; all original loads_t.p_set and all non-allowed dynamic tables remain unchanged.

**PyPSA 1.4 default elision:** PyPSA intentionally omits a dynamic column on NetCDF export when every value equals the component default. The composer verifies that any missing reimported column consists EXCLUSIVELY of exact default values, that the unchanged static value equals the default, and records a per-target elision ledger in QA. Any non-default loss is blocked. The fully clipped 1.0 utility-PV profile exercises this expected semantic equivalence. No static values or source values were perturbed to defeat PyPSA serialization.

## 3. Actual qualification

**Host:** GitHub Actions ubuntu-latest; Python 3.11.17, PyPSA 1.4.0, Pandas 3.1.0, NumPy 2.2.6, SciPy 1.15.3, xarray 2025.10.1, Snakemake 9.13.3, pytest 9.0.2. Full workflow run 41315496732 at tested code commit cd71f36ddf07fb3ecc1cb4be5701a2586b9950c8 finished SUCCESS.

| Gate | Result |
|---|---|
| Unified Python suite: producer+integrator+negative tests | 92 passed, 0 failed, 52 nonfatal warnings, 9.83 seconds |
| Five synthetic weather identifiers in 2030 horizon | 5/5 generated, bound and integrated independently |
| PyPSA source network | Synthetic 7 Generators, 3 StorageUnits, Load, Store, Link, Line, 2W Transformer, 3W Transformer arms and synthetic star bus |
| Static invariance | All 16/16 PyPSA static component tables fingerprinted before writes, after writes and after NetCDF reimport; exact equality |
| Target ownership | 8/8 distinct approved target IDs per weather scenario |
| Source resolution | Two consecutive 2020-01-01 UTC hourly snapshots, NOT full real years |
| Hydro source MWh | Per area 4 MWh native / 2h, allocated 60/40 percent to two existing StorageUnits; separate RoR source; HCL no natural inflow |
| Pre-existing dynamic data | Load profiles unchanged; other unapproved dynamic attributes unchanged |
| Snakemake DAG dry run | PASS |
| Complete Snakemake execution | 16/16 jobs including five RES, five Hydro, five composer and aggregate rule |
| PyPSA-NetCDF import/export with full static and time-semantic checks | 5/5 PASS |
| Real source qualification / M2 authorization | FALSE / FALSE |

**Network fixture SHA256 after PyPSA composition (ephemeral CI outputs):**

| Fixture weather ID | NetCDF SHA256 |
|---|---|
| FIXTURE_WS_1 | 928f6ec13a468454e0dbb1d7d5d5b50d1d9681d38759692b589c115edbd4f390 |
| FIXTURE_WS_2 | d332bf70622aa08b3cb4861c7d3465642740486d09cd3449468aaab2f0d356f0 |
| FIXTURE_WS_3 | eacbc7d16d894d9ef7572baae9e88a857dcae1366eaa6b421ef596f923b8993f |
| FIXTURE_WS_4 | 0687f99f367aecbdb6c26b2039099f38d5e7dd1dca1263b92bdeaf12f34be3f7 |
| FIXTURE_WS_5 | 49a6c70744b66075802aa39a8bdb45ca64b156e9d4e8b9c47a365e76b17a45e3 |

CI artifact 13087730084 contains JUnit XML, direct BOM SHA, pip freeze, Snakemake dry/full-run logs and five per-weather QA JSON records. No fixture NetCDF is presented as a licensed/real M0 network.

## 4. CPU and memory scaling without fabricated real metrics

Five fixtures × 2 snapshots × 8 allowed numeric time-series targets = 80 double values (640 B before Pandas/PyPSA/xarray/NetCDF/ledgers and original-network overhead). The actual Snakemake run used --cores 2; the Pytest execution time was 9.83 s. Peak RSS for the real full-scale system was NOT measured and cannot be inferred from these tiny fixtures.

For a future horizon with H hourly snapshots, N authorized time-series assets and five original weather sources, uncompressed dynamic double payload alone scales at least as 5 × H × N × 8 bytes, before source tables, copies, metadata, NetCDF compression, plotting or multiple horizons. MA4R must measure peak memory, file size and actual wall time on the real M0 network.

## 5. Gate

**ACCEPTED: M1_MA4F_FIXTURE_INTEGRATION_QUALIFIED.** The integration implementation is demonstrably executable using physically labeled synthetic inputs. It is NOT a qualified source witness: the actual M0 DNR, five externally chosen real weather datasets, PECD and Hydro bytes/geo masks/native boundary witnesses, real hydro basin/port mapping and any real DFT load inputs remain unavailable. Thus REAL_SOURCE_NOT_QUALIFIED, independent reviewer NOT_DONE and S_GOV_M1_M2_RELEASED = FALSE. No merge into main or direct M2 handoff was performed.

See INTEGRATION_CONFLICT_LEDGER.md and HANDOFF_MA4R.md for the combined residual gates.
