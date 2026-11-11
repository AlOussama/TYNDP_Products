# D4 — R-DATA independent frozen-source reviewer handoff

**Role:** a reviewer independent of data acquisition and the MA1 R-PHY/R-CLU reviews. **Status:** criteria ready, actual review **NOT STARTED**. This document is not a reviewer verdict.

**Entry condition:** D0–D3 source-owner original bytes or genuinely limited D1 source files frozen, with original SHA-256/size/license release, topology/asset/revision fingerprint, preserved snapshots and equipment ledger. No empty or placeholder SHA-256 is accepted. Reviewer receives restricted bytes by authorised channel only.

**First actions:**
1. Independently retrieve and compare byte size, SHA-256 and upstream published checksums/release/rights (DR-01). Validate parser/version and source-to-canonical joins without borrowing producer's outputs (DR-02–06).
2. Independently reproduce the source-country mapping, AC islands (HVDC links excluded), full voltage/tap/transformer coverage, ratings/UTC/duration/year mapping, and precise asset/nodal MW balance (DR-03–11).
3. Replay DC KCL, KVL and source-vs-solver branch-flow oracle with explicit owner-approved numerical tolerances and comparable source conditions (DR-12); do not treat internally computed flows as independent truth.
4. Recheck complete annual 225/400-class time/rating screening, balance of separate physical neutral cases, N-1 outage and monitoring applicability, exceptional TSO decisions (DR-13–16).
5. Publish independent environment/solver/parser SHA, source and output checksums, dataset splits, reproducible commands, findings P0/P1/P2, remediation and new reviewer replay digest (DR-17).

**Decision permitted:** `BLOCKED`, `REAL_TOPOLOGY_ONLY`, `REAL_MA1_WITNESS`, `REAL_MA2_CALIBRATION_WITNESS` or `REAL_MA3_SECURITY_WITNESS`, always with explicit source and subsystem scope. A pass at a lower tier does not grant a higher tier. D1 open OSM **cannot** be promoted to `REAL_IOSN`.

**P0 rejection cases:** absent originals/hash; unsettled 110-kV AC connections; silently removed PST/HVDC or unsupported equipment; fabricated 5 weather years; nodal island imbalance; absent independent reference-flow witness; incomplete/derived N-1 sources; wrong voltage/units; inherited tests claimed as independent.

**Current independent review:** **NOT EXECUTED**. Return only once producer freezes original manifests. No MA2/MA3 runtime GO, no M0/M1 modifications, no weather-year selection and no merge.
