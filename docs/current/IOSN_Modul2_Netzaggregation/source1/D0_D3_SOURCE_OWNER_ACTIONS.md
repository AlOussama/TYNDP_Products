# D0–D3 source-owner acquisition ledger — M2-D-SOURCE1

Date 2026-11-11. These are **requests to be made by authorised owners**, not proof that external third parties were contacted. All deliverables can be published as metadata only.

## D0 — Official transmission grid and starting-grid identity
**Owner:** network/TSO grid-data authority; institutional applicant. **Acquisition route:** ENTSO-E official [statistics and data](https://www.entsoe.eu/publications/statistics-and-data/) and [dataset request form](https://stum.entsoe.eu/). Official site states CGMES grid datasets may require specific application and NDA and that market/TYNDP data are different.

**Required request content:** exact TYNDP2026 IoSN model release for detailed 2025 AC/DC reference, which projects make the adopted 2035 starting grid, permitted M2 scientific use/re-distribution restrictions, confidential/derivative boundaries, full files and boundary file with origin/version SHA-256, CGMES reference IDs, time scope, country mapping, source voltage/base, 110-kV ties, AC lines, 2W/3W transformers, taps/PST, HVDC, ratings, outage compatibility and unsupported-device statement.

**Result:** No authorised source bytes or grant supplied. Cannot submit a form on behalf of an unidentified organisation; **REQUEST_READY_OWNER_ACTION_REQUIRED**. No assertion that legacy ENTSO-E publicly offered TYNDP 2020/2018 releases equal IoSN 2026.

## D1 — Open OSM network
**Owner:** independent open-data acquisition worker. **Source:** [Xiong et al., Zenodo 14144752, v0.6](https://zenodo.org/records/14144752), ODbL-1.0. Five source tables listed in [manifest](source_manifest.json). Public catalogue and buses preview accessed; original file acquisition failed in current environment. No full-byte checksum claimed.

**Required route:** download all five CSV files locally (not to public Git), verify published MD5 against downloaded bytes, compute SHA-256 and size; check original stable IDs, duplicate/orphan endpoints, country and DC flags, x_ohm/v_nom, transformers and converters; select a pair **only from observed AC border lines** and verify a >=3-vertex AC cycle. Generate real source IDs and induced-element ledger; no market MW. Additional explicit owner/maintainer unit confirmation needed if the CSV x representation is ambiguous. **Gate:** BLOCKED pending original files.

## D2 — Time and dispatch
**Owner:** external weather selection owner plus dispatch/grid identity owner. **Required:** 5 fixed exact weather IDs with signatures/source hashes, source/target-year mapping, strictly monotonic UTC snapshots/duration/season, nodal generator/load/storage/embedded MW, HVDC/PST, per-AC-island loss/slack reconciliation, branch-flow oracle, grid revision key, independent neutral re-dispatch with HVDC=0 and PST neutral. Read-only upstream; **no weather-year selection or M1 modifications**. Five slot records have weather_id NOT_PROVIDED in the reviewed M1 file. **Gate:** BLOCKED.

## D3 — Network security
**Owner:** TSO security authority. **Required:** full legal outage list, monitored branches, islanding/LODF invalid-case disposition, normal and emergency ratings with original A/MVA/MW units and justified conversion, season/calendar mapping, four directed seasonal outputs, signed individual TSO exceptions with expiration and scope. Generic algorithm fallback 99.5%/1%/130% is not an exemption. **Gate:** BLOCKED.

Each owner shall deliver a source release manifest with original byte SHA-256 and byte count, immutable acquisition identity and access/license record, then a local original-file witness. No raw restricted data shall be committed.
