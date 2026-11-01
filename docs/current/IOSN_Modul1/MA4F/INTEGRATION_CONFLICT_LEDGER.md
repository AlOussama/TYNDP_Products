# MA4F — Consolidated Integration Conflict and Error Ledger

All resolved fixes are scoped to the five-scenario synthetic integration, not automatically transferred to real source authority.

| ID | Conflict or observed defect | Disposition | Evidence |
|---|---|---|---|
| I-01 | Parallel MA2/MA3 branches share scripts/iosn_m1/__init__.py | FIXED: copied original Git blobs on isolated common-base branch; chose MA3 init blob 19d19604cc7cf5db21bfe6985820ef049b89422b | c1fd58e29d9c452c772458f3f5a3958c9d970419 |
| I-02 | No executed physical M0 DNR, actual source/view IDs or M0 owner witness | BLOCKED REAL, fixture sidecar only | MA1C G1-C, M0 preflight 95/96 |
| I-03 | Legacy producer network_revision_id conflicts with CAN/2 canonical_revision_id/projection_id | FIXED FIXTURE: explicit versioned bridge; canonical only, separate source/projection and operating IDs | schemas/iosn_m1/m0_dnr_identity_bridge_1_0_0.json |
| I-04 | MA2 JSON weather manifest, MA3 hydro source manifest and exact five weather IDs uncoordinated | FIXED FIXTURE: master owns IDs, horizon, SHA, UTC and quality, adapters retain native schemas | master_input_manifest_1_0_0.json, fixture_ma4f.py |
| I-05 | RES/RoR collide on Generator.p_max_pu; Store/Link port may overwrite Generator.p_set; DFT load may mutate original loads | FIXED FIXTURE: per-target ownership, collision and overwrite negatives, Store staged veto, no load writing | composer, integrated negative tests |
| I-06 | Inconsistent Python/PyPSA/Geo/xarray/Snakemake environments | FIXED FIXTURE: precise direct BOM, full pip freeze and actual CI E2E | Actions 41315496732 |
| F-01 | PyPSA 1.4 requires pandas>=3, original BOM pinned pandas 2.3.3 | FIXED: pandas==3.1.0, exact direct BOM installed before editable package | failed Actions 41314890924; successful Actions 41315496732 |
| F-02 | Inherited MA2 synthetic 3W bus guard uses bitwise NOT on boolean .any() | FIXED with Python not and retested producer negative case (Pandas 3) | res adapter final blob 823fc3084f349077f5d1c443d68bc2b57a4325b0 |
| F-03 | GeoDataFrame.to_json does not implement Pandas split orient, causing all-static fingerprint exception | FIXED: convert component static table to plain DataFrame before canonical JSON | 16/16 PyPSA static tables checked |
| F-04 | PyPSA 1.4 represents missing synthetic 3W-star coordinates as zero-placeholder after NetCDF import | FIXED FOR FIXTURE ONLY: require sidecar null country/source_geo, permit NaN or 0,0 placeholder, never geographic proof | integrated negative tests, sidecar |
| F-05 | PyPSA NetCDF exporter drops all-default dynamic columns, including fully clipped PV CF 1.0 | FIXED SEMANTICALLY: only exact default equality plus identical static default accepted; per-target ledger; any nondefault missing fails | PyPSA 1.4 source and 5 real NetCDF roundtrips |
| F-06 | Combined MA2+MA3+composer Snakemake DAG had never been executed | FIXED FIXTURE: five sets, Snakemake dry run PASS, 16/16 jobs | Actions 41315496732 |
| R-01 | Real 5 weather ID binding and PECD spatial products/native files/checksums absent | BLOCKED REAL, no synthetic substitution | MA1C IN-01..IN-03 |
| R-02 | Physical hydro MWh source bytes/native interval boundary witness/basin shares/Store-Link approval absent | BLOCKED REAL | MA1C IN-05/06 |
| R-03 | Owner-qualified physical M0 DNR and projection/canonical/source mapping absent | BLOCKED REAL | MA1C IN-04, M0 95/96 |
| R-04 | Real DFT demand source/crosswalk and independent review absent | BLOCKED REAL | MA1C IN-08, MA4R |

**Trace of integrated failures repaired:**

- 41314890924 — dependency resolution failed (Pandas vs PyPSA); no tests run.
- 41314980273 — 86 PASS / 6 FAIL; exposed anti-star guard, geo hash and 3W-placeholder interpretation.
- 41315161560 — 91 PASS / 1 FAIL; first exact PyPSA default-elision case.
- 41315338464 — diagnosis confirmed Generator.p_max_pu[G-CGMES-PVU] missing after export with 1.0 default-equivalent values.
- **41315496732 — 92 PASS / 0 FAIL, Snakemake 16/16, full 16 static table fingerprints and all five NetCDF roundtrips.**

All real gate blockers R-01 to R-04 remain open, not waived by fixture success.
