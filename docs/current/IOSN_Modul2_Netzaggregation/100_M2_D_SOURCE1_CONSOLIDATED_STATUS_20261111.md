# 100 — M2-D-SOURCE1 consolidated data acquisition and qualification

**Scope:** Module 2 data acquisition only. **Date:** 2026-11-11. **Result:** `BLOCKED_DATA`. This is not an architecture/runtime release.

## Pinned input and executed verification

- Source Auftrag: [96](96_M2_D_SOURCE1_PARALLEL_REAL_DATA_ACQUISITION_20261111.md), commit `27dfd810b39e17e6b616a2b0aeb813eb8948d8a0`.
- Independent review: commit `6a8262f128ae3dd7e108afe2ade09028ea4f651f`, documents 88–92. The five documents and the full Auftrag were read.
- Repository source-table checked from GitHub pinned bytes: `docs/current/IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv`, Git blob SHA-1 `e147ba7143ecc21647055d9413f0973338a25b0f`, 560 bytes, SHA-256 `8ebd0bc239cd62760944a68deb53a0af710e56d5ea3c379d7526b4255fc4c391`. Parsing gives **37 published country labels, 102 zones, NI and UK separate**. This validates a methodological **table only**, not the detailed European grid.
- PyPSA-Eur OSM release **Zenodo 14144752 v0.6** (2024-11-13), ODbL-1.0, five source CSV catalogued (buses, lines, links, transformers, converters). Published MD5 recorded in manifest. Full original bytes were **not** downloaded or SHA-256 hashed; attempted direct acquisition failed due to network/DNS restriction in this execution environment. A web preview of `buses.csv` and the official record catalogue do not constitute original full-file SHA-256 or real topology execution.
- Local deterministic tests: quota file Git-object comparison, source table counts, synthetic two-country-cycle algorithm and Python syntax passed. **No real two-country topology witness or real load flow was executed**.

## Four parallel source lanes — outcomes

| Lane | Evidence now available | Missing and disposition | Gate |
|---|---|---|---|
| D0 official TSO/IoSN grid | Official ENTSO-E institutional dataset request mechanism; the project quota table | Owner-approved grid 2025 vintage + 2035 changes, permission/NDA, complete AC/DC devices, IDs, country mapping, 110-kV ties, frozen original SHA-256 | `BLOCKED` |
| D1 open topological pilot | Pinned OSM PyPSA-Eur v0.6 metadata and ODbL-1.0; download/file MD5 metadata | Download exact 5 CSV source bytes, check MD5 and SHA-256, parse IDs/units, extract real cross-border AC cycle, full induced equipment ledger | `BLOCKED_TOPOLOGY_PENDING_BYTES` |
| D2 dispatch/time/neutral | M1 five *slots* in independent project source; all values `NOT_PROVIDED` in inspected snapshot | Exact five owner-fixed weather IDs, synchronized nodal MW and UTC/year/season, HVDC/PST, separately physically balanced neutral dataset, independent branch flows | `BLOCKED` |
| D3 security | Required DR15–DR16 method and proposed SecurityData contract | TSO-authorised outage list, seasonal emergency/normal limits, monitored branches, islanding, exception approvals, four directional/seasonal bins | `BLOCKED` |

## Executed DR-01–DR-17

See [machine ledger](source1/dr01_dr17_qualification_ledger.json). **All full-input DR checks are blocked**; DR-03 is independently verified **only for 37/102 quota-table invariants** and DR-01 only for the repository source-table byte identity. Not tested: source grid, KCL, AC/DC electrical parameters, real dispatch, N-1 and annual time coverage. No substitute values or source hashes were assigned. [Local test evidence](source1/local_test_evidence.json).

## Owner/data-source actions

1. D0: authorised institution to submit a version-scoped data request through [ENTSO-E STUM](https://stum.entsoe.eu/) and confirm its explicit license/usage, source model vintage and access grant. The public request form requires institutional identity. **Not submitted** by this macro.
2. D1: acquire the five pinned CSV files from [Zenodo record 14144752](https://zenodo.org/records/14144752); compare exact bytes with recorded published MD5, compute fresh SHA-256 and run limited topology extraction. A candidate two-country subnetwork must have a **real AC** cross-border edge and a cycle; HVDC never counts toward AC connectivity. Refuse real PASS if transformer/PST/DC/110-kV exclusions or x-unit uncertainty remain unaccounted for.
3. D2: request five exact external year IDs from upstream owners without new selection. Dispatch must be per original bus and synchronized with actual grid/asset flow oracle. Balanced HVDC=0/PST-neutral injections must be separately generated and independently checked.
4. D3: obtain genuine TSO outage/monitor/limit/exception source files; do not confuse IoSN 99.5%/1%/130% statistical fallbacks with TSO-signed exceptions.
5. D4: invite a **separate independent R-DATA reviewer** only after frozen original source manifests exist. Criteria and replay procedure in [R-DATA handoff](source1/R_DATA_INDEPENDENT_HANDOFF.md).

## Governance / constraints

- No changes to M0/CGMES, M1/PECD, weather-year selection, MA1 physical code, or main; no PR #13 merge, MA2/MA3 runtime GO or official real-network validation.
- Source metadata and test evidence are nonconfidential. Do not commit restricted TSO original bytes, personal identification of portal applicant, NDA terms, access tokens or credentials.
- Original IoSN source unavailable in inspected Git trees is **NOT_PROVIDED in audited scope**, not a claim it does not exist on owner/private storage.
- Status progression is **BLOCKED_DATA -> limited topology pilot only after D1 originals -> further independent gates only after D0+D2+D3**.
