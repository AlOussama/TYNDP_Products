# D1 reproducible open-real-topology witness (not yet executed)

**Pinned source:** Zenodo record [14144752](https://zenodo.org/records/14144752), release 0.6, 2024-11-13; files `buses.csv`, `lines.csv`, `links.csv`, `transformers.csv`, `converters.csv`. ODbL 1.0 obligations apply. No raw data committed.

**Executable local reference:** `source1_verifier.py` (accompanying local reproducibility attachment in this macro). It verifies 5 published MD5 values, computes original-file SHA-256 and byte size, checks IDs/foreign keys and x > 0, and searches a shortest **two-country AC-only graph cycle with >= 3 buses and an original cross-border AC line**, without treating HVDC as AC. Report devices induced by selected node set and maintain blocker if unsupported; chosen test S_base=100 MVA must never be mistaken for source owner/base choice. Missing original bytes or missing x-schema fail closed.

```bash
python3 source1_verifier.py --quota docs/current/IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv --self-test
python3 source1_verifier.py --raw-dir /controlled/pypsa_osm_v06 --acquire > /controlled/pilot_result.json
```

**Caution:** The proof of a cycle alone is not an operational plant. Any boundary-truncated subset or heuristic x_ohm counts as a limited *real-world reconstructed topology* witness, not official TSO grid; no source dispatch exists in the OSM topology archive. Even a successful D1 acquisition must undergo independent R-DATA replay for promotion to an accepted limited real witness.

**Current result:** no complete original source CSV bytes were acquired in this runtime. `PARTIAL_REAL_TOPOLOGY_WITNESS` **not established**; D1 gate `BLOCKED`.
