# 88 — M2-D-REAL: Independent Source and Data Inventory

**Date:** 2026-11-11. **Scope:** Module 2 inputs and data qualification only.
**Pinned MA1 evidence:** 70e92ba9e62a320e58227ce9c2f03fad266f44bf (verified GitHub commit and recursive tree; 175 entries, not truncated).
**Decision:** BLOCKED_DATA. This is a data audit, not a runtime or architecture release.

## 1. Evidence semantics

- **REPO_FILE_VERIFIED**: path, blob SHA and textual contents verified at the pinned commit. Git blob SHA is **not** an original external source SHA-256.
- **SYNTHETIC_ONLY**: committed test or demo files, never real network acceptance.
- **CATALOGUE_ONLY**: publicly identified source URL or download index; original bytes, content and exact IoSN vintage not checked.
- **CANDIDATE_OPEN_MODEL**: externally described reconstruction of real-world assets; not an official synchronous TSO network, not downloaded/admitted.
- **NOT_PROVIDED**: no qualifying source payload found in the examined Git trees. Does not prove that the data do not exist on a private workstation, untracked directory or at a TSO.
- **REQUIRES_OWNER_RELEASE**: external owner must provide access, source license/release, frozen bytes, SHA-256, device and parameter quality.

## 2. Exact repository inventory

| ID | Location | Verified observation | Classification | Missing for real use |
|---|---|---|---|---|
| R01 | [Official country CSV](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/current/IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv) | 37 published labels, quotas sum to 102; NI distinct from UK. Git blob e147ba7143ecc21647055d9413f0973338a25b0f | REPO_FILE_VERIFIED / method table | Every real bus-to-country mapping |
| R02 | [MA1 report 82](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/current/IOSN_Modul2_Netzaggregation/82_M2_MA1_EXECUTION_REPORT_2026_11_04.md) | 52 core and 26 MA1 tests reported; 7-bus/3-country fixture; real-data gate blocked | REPO_FILE_VERIFIED / report | Independent real test |
| R03 | [Gate evidence 86](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/current/IOSN_Modul2_Netzaggregation/86_M2_MA1_GATE_EVIDENCE_2026_11_04.json) | synthetic=true; 2 islands, 5 MOCK years; real_qualified=false | SYNTHETIC_ONLY | Non-synthetic input manifests |
| R04 | [MA2 handoff 85](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/current/IOSN_Modul2_Netzaggregation/85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md) | operational and separate neutral dispatch required; x/c0 fit; train/select/holdout | REPO_FILE_VERIFIED / specification | Actual synchronized reference states |
| R05 | [MA1 contracts.py](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official/contracts.py) | Typed DetailedGridSnapshot, ReferenceDispatchSet, TimeSet, NormalContingencyRatings; provenance SHA field is format-validated | REPO_FILE_VERIFIED / interface | Source-byte verification and missing real fields |
| R06 | [MA1 preflight.py](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official/preflight.py) | Country IDs, timestamp, ratings, KCL and rejected components checked | REPO_FILE_VERIFIED / validator | Actual real run; access and oracle |
| R07 | [results/synthetic](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/results/synthetic/manifest.json) | historical legacy demonstration; synthetic results incl security_limits_A/B.csv | SYNTHETIC_ONLY | May not be treated as N-1 witness |
| R08 | [artifacts/snapshots](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/artifacts/snapshots/VALIDATION_MANIFEST_2026-10-16.json) | historical 9-bus DC/3-bus triangle, real_network_integration=NOT_EXECUTED | SYNTHETIC_ONLY | Real network |
| R09 | [artifacts/bundles](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/artifacts/bundles/) | three committed ZIP code/report bundles identified in tree (approx. 1.35 MB, 211 kB, 637 kB); no claim of original IoSN data | HISTORICAL_CODE_BUNDLE | ZIP member inspection would be needed for a stronger assertion |
| R10 | [provenance/artifact_manifest.json](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/provenance/artifact_manifest.json) | hashes for historic generated artifacts, not the required source-grid/dispatch/security archive | HISTORICAL_MANIFEST | Distinct input SHA-256 ledger |
| R11 | [examples/pypsa_real_network.py](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/examples/pypsa_real_network.py) and [tutorial](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/tutorials/05_reale_pypsa_netze.md) | path argument for external .nc; output is reduced_unqualified.nc, not x/c0/N-1 | REPO_FILE_VERIFIED / optional example | Actual supplied .nc; qualified adapter. Legacy path is not the iosn_official MA1 interface |
| R12 | [M1 source witness (separate branch)](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/FIVE_WEATHER_IDS.csv) | 5 slots marked EXTERNALLY_FINALIZED but all weather_id=NOT_PROVIDED, native hashes=NOT_COMPUTED_NO_BYTES as of its 2026-11-01 audit | DOCUMENTED_ONLY | Actual fixed IDs + evidence; M2 must not select/reselect |
| R13 | [M0 DNR identity witness (separate branch)](https://github.com/AlOussama/TYNDP_Products/blob/5c68198984b6f2f430a49ff3e23d17c0b27320e1/docs/current/IOSN_Modul1/MD1/M0_DNR_IDENTITY_WITNESS.md) | no demonstrated original CGMES/PyPSA-DNR/sidecar real output at that audit | DOCUMENTED_ONLY | Source revision, projection/reference ID and hashes |
| R14 | [BUNDLE01R physical source ledger](https://github.com/AlOussama/TYNDP_Products/blob/3fd3b0e6ede30f863228d426389e880bdb09f1d0/Modelling_Language/iosn_formal_specification/workstreams/BUNDLE01R_B_data_qualification/physical_source_evidence_ledger.csv) | candidate URLs identified; zero original frozen IoSN payloads byte-inspected in cited independent 2026-11-10 report | CROSS_PROJECT_AUDIT / CATALOGUE_ONLY | Data acquisition, audit against Module 2 contracts |

**Repository tree audit:** The pinned MA1 commit, main and selected additional 2026-11-10/11 research and alternative M2 branches were enumerated through GitHub recursive trees. No checked tree contained an obvious original detailed grid .nc/.h5/.parquet, complete five-year nodal dispatch, emergency ratings with contingencies or physical IoSN reference-flow bundle. The pinned tree has no tracked top-level data/ or datasets/ directory. This is a **tracked-Git scope statement**, not a check of local ignored/untracked or private storage. The pinned .gitignore does not itself prove local dataset presence or absence. New research branches mostly add documentation and model-language validation metadata.

## 3. External source and access inventory

| ID | Exact public locator | Verified scope | Status for M2 | Acquisition route |
|---|---|---|---|---|
| E01 | [ENTSO-E IoSN consultation methodology](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf) | 65-page public consultation version, 25 February 2026: §3.4, §§3.8–3.9, Annex 6.1 | METHODOLOGY_READABLE_NOT_SOURCE_GRID; PDF byte hash not computed here | Pin approved method release and byte hash with owner |
| E02 | [TYNDP 2026 scenarios download](https://2026.entsos-tyndp-scenarios.eu/download/) | public index: Line Data, Nodes, PEMMDB, PECD, Demand, Hydro | CATALOGUE_ONLY; NOT an admitted 2025 detailed IoSN AC grid | Download original records, SHA-256, inspect fields and scenario-vintage match |
| E03 | [Line-data.zip candidate](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/Line-data.zip) | discovered download candidate, content not inspected | CANDIDATE_UNVERIFIED | Structural inspection; do not infer AC x, PST, 110 kV ties |
| E04 | [Nodes.zip candidate](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/Nodes.zip) | discovered download candidate, content not inspected | CANDIDATE_UNVERIFIED | Verify nodal asset and topology identity; no substitution for GRID25 |
| E05 | [PEMMDB_2.X.zip candidate](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/PEMMDB_2.X.zip) | market data candidate | CATALOGUE_ONLY | Obtain physical nodal mapping, market-dispatch and reference flows separately |
| E06 | [PECD.zip candidate](https://2026-data.entsos-tyndp-scenarios.eu/input/model-input/national-trends/PECD.zip) | scenario weather data candidate | CATALOGUE_ONLY / upstream | Consume M1 owner-delivered fixed profiles only |
| E07 | [ENTSO-E grid dataset access policy](https://www.entsoe.eu/publications/statistics-and-data/) and [request form](https://stum.entsoe.eu/) | CGMES grid datasets may require institutional request and/or NDA | ACCESS_REQUEST_REQUIRED; no granted project rights demonstrated | TSO/network source owner to request correct release |
| E08 | [PyPSA-Eur OSM base network v0.6](https://zenodo.org/records/14144752) and [documentation](https://pypsa-eur.readthedocs.io/en/v2026.02.0/data-base-network.html) | publicly described topology at 220–750 kV; parameters partly heuristic; ODbL | CANDIDATE_OPEN_MODEL; not downloaded, not TSO-authoritative | Acquire fixed version and build restricted two-country witness |
| E09 | [PyPSA-Eur dataset overview](https://zenodo.org/records/15143557) | transmission grid, HVDC, plant database and time-series candidates | CANDIDATE_OPEN_MODEL; exact prepared netCDF unverified | Inventory actual archive contents and units |
| E10 | [Netzschleuder PyPSA Europe grid](https://networks.skewed.de/net/pypsa_eur_grid) | documents OSM substation/line IDs, country codes, x in ohm (v0.6+), transformers, HVDC type | CANDIDATE_OPEN_MODEL / topology | Check per-type coverage, PST gaps, country scope and derived parameters |

**Crucial distinction:** official quota CSV != per-node country assignment; published scenarios line/node files != TSO detailed synchronized grid; publicly downloadable reconstruction != verified ENTSO-E IoSN reference; synthetic test output != an independently observed real snapshot.

## 4. Reproducibility and caveats

The external sources above were inspected as public documentation/catalogue, not as original downloaded binaries. Their hashes, precise file members and applicable licenses per concrete file remain unverified unless explicitly stated. All dataset admission requires source-side release/vintage/authorization plus exact byte SHA-256, immutable extraction manifest and a representative parser/physics witness. **No hashes were invented.**
