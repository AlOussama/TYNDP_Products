# 92 — M2-D-REAL: Parallel Data Acquisition and Qualification Handoffs

**Date:** 2026-11-11. **Status:** PLANNED_NOT_EXECUTED. These are concise, executable read-only/acquisition tasks; no M0/M1 implementation or weather-year selection.

## M2-D0 — TSO Starting Grid and Provenance (P0, Data Owner / Source Liaison)

Obtain an owner-approved and license-compliant frozen 2025 detailed AC/DC reference-grid payload and project-adjusted IoSN 2035 start-grid definition. Include bus/terminal/branch IDs, original 2025->2035 change ledger, country map, voltage levels/base, 110-kV tie completeness, transformers (including nontrivial tap/3W), PST, HVDC, rating vintages and a TSO-signed equipment support matrix. Deliver inventory.csv + source_manifest.json (original byte SHA-256, source filename, access grant and condition) + device_status.csv + reference_topology_check.json. If unavailable, issue a concrete data access request through [ENTSO-E portal](https://stum.entsoe.eu/) or networkdataset@entsoe.eu as publicly documented, observing NDAs. An allowed M0 output may be consumed when actually supplied; **do not change M0**. Gate G-D0: SOURCE_BYTES_VERIFIED and TOPOLOGY_COHERENT, else BLOCKED.

## M2-D1 — Open Real Topology Pilot (P1, Independent Data Worker)

In parallel to D0, inspect and acquire one **pinned, open-source** PyPSA-Eur OSM high-voltage base-network release ([v0.6 source](https://zenodo.org/records/14144752), [documentation](https://pypsa-eur.readthedocs.io/en/v2026.02.0/data-base-network.html)). Record ODbL requirements, exact archives/hashes; select smallest two-country mesh with a genuine AC border, preserving country/terminal/tie identity and all actual components. Document every heuristic electrical parameter, required x units and any missing PST/110-kV representation. Build M2-only adapter/input witness; no fabricated market dispatch. Execute DR-01..DR-07, DR-11/12 only with independently sourced dispatch. Deliver pilot_source_manifest.json + extraction_ledger.csv + topology_witness.json; classify REAL_TOPOLOGY_ONLY, never official IoSN or MA2/MA3 pass. Gate G-D1: PARTIAL_REAL_TOPOLOGY_WITNESS or BLOCKED.

## M2-D2 — Fixed Time, Synchronous Nodal Dispatch and Flows (P0, Dispatch/Time Owner)

Request five externally fixed weather-year identities and per-year real time-key/profile release *only* from upstream owners, plus source/target-year crosswalk. Obtain actual market-dispatch source with nodal generating and consuming assets, storage schedule, embedded source-to-bus mappings, losses/slack convention, HVDC/PST settings and independent detailed branch-flow reference. Map to DetailedGridSnapshot and ReferenceDispatchSet and TimeSet, preserving same grid/state/source revision. Provide a separate physically balanced neutral calibration dataset (HVDC=0, PST neutral) rather than reusing operational injections. Source/hash everything. Deliver dispatch_source_manifest.json, weather_contract.json, operating.csv/parquet, neutral.csv/parquet, reference_flow_oracle and DR-08..14 ledger. **Do not select climate years; do not modify M1.** G-D2: OPERATIONAL_AND_NEUTRAL_BALANCED or BLOCKED.

## M2-D3 — Contingency, Limits and Exceptions (P0, Security/TSO Owner)

Obtain exhaustive admissible N-1 outage set and monitoring basis, source-specific season/winter definitions, normal/emergency MW/MVA/A data plus explicit conversion policy, PST/HVDC contingency treatment, disconnected-island cases, system limits and list of individual TSO exclusions/waivers with a signed justification and scope. Distinguish published generic 99.5%/1%/130% sample-quality fallbacks from actual source-owner exceptions. Deliver security_source_manifest.json, contingency.csv, monitored_limits.csv, exception_ledger.csv, season_direction_matrix.csv; fully reconstruct N-1 sensitivity plus 4 result cells per interzone. Gate G-D3: VALIDATED_SECURITY_DATA or BLOCKED.

## M2-D4 — Independent Real Source Reviewer and Gate (P0, R-DATA; separate actor)

Read only frozen source bytes/manifests and reviewer SHA. Rerun DR-01..DR-17 independently with exact input source hashes and numerical witnesses; issue findings P0/P1/P2, reproduction steps and separate re-review SHA. A source URL, screenshot, CI-green synthetic run or a Git object hash alone cannot be accepted as source evidence. Decide REAL_TOPOLOGY_ONLY, REAL_MA1_WITNESS, REAL_MA2_CALIBRATION_WITNESS, REAL_MA3_SECURITY_WITNESS, or BLOCKED with explicit scope. Do not assume this is an R-PHY or R-CLU review. Gate G-D4: INDEPENDENT_REPLAY_PASS only after complete evidence.

## Coordination / executable parallelism

- Start **D0, D1, D2, D3 concurrently**: they request different source/owner inputs; D1 does not wait for restricted TSO data.
- Start D4 criteria review immediately; run its actual re-evaluation **only after** frozen inputs arrive.
- D2 cannot manufacture missing five-year identifiers; D3 cannot derive authoritative TSO limits from model proxy outputs.
- Consolidation into full 37/102 pan-Europe real run depends jointly on D0+D2+D3 and a pre-agreed canonical MA1 API (iosn_official vs m2); this task does **not** adjudicate the API.
- Store only permitted data; restricted raw files may remain outside Git. Commit **non-sensitive manifests and reviewer output**, with encrypted/controlled-access URI pointers where necessary, never credential URLs or NDA-protected payloads.
- No automatic Runtime-Go, MA1/MA2/MA3, M0/M1 or PR merge release from acquisition tasks.
