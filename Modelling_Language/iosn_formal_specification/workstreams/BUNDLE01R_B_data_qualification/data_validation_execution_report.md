# BUNDLE-01R B — Data Validation Execution Report

**Date:** 2026-11-10. **Reference commit:** `09cff8a8f9d82282d2e307f32ba8b139c3eb3824`. **No original physical IoSN study data payloads were successfully downloaded/inspected.**

## Two different types of evidence

### 1. Real source-data validations (V001–V028)

**0/28 executed on original frozen IoSN input files. 0 PASS, 0 synthetic tests executed.** Every validation is retained with its original ID, expected assertion, primary/secondary class (schema, reference, semantic, content or governance), required artifacts, owner oracle, and `BLOCKED_SOURCE_OR_OWNER_ORACLE` state in `data_validation_results.csv`. There is no native LP, grid, H2, storage, time-series or KPI result and **no Real-Data Conformance claim**.

### 2. Actual executed technical review of **repository metadata**, not real IoSN data

`metadata_technical_check_results.json` records **16 actual programmatic checks (16 PASS, 0 FAIL)**: CSV reference/source identities, counts, field presence, P00–P17 coverage, direct trace allocation, source-status claims and unresolved original hashes. **These are project-inventory checks only.** No real data quality validation status is advanced from `NOT_EXECUTED`.

## Original-file retrieval attempts and outcomes

- Original official IoSN PDF: public web PDF viewed/rendered, binary download via dedicated downloader failed, direct HTTPS request from container failed at DNS; no byte-level hash. The PDF cannot be hashed from text/screenshot.
- 2026 scenario download page: https://2026.entsos-tyndp-scenarios.eu/download/ visibly exposes README, PEMMDB, PECD, Demand, Hydro, Hydrogen, Lines, Nodes, Prices and P2G. Exact candidate direct URLs are recorded in `physical_source_evidence_ledger.csv`. Web file resolver rejected ZIP/XLSX/DOCX types as unsupported; that does **not** establish contents, complete availability, or frozen IoSN study version. Separate file-download attempt for README also failed.
- No direct credentialed owner data export or G1-authorized sample is connected. Original SHA-256 remains `NOT_COMPUTED` for every file; do **not** substitute file name, ETag, Git blob hash, web URL or ZIP listing.

## Required execution procedure after access

For each V001–V028: (a) obtain signed approved source/study version, input bytes and SHA256, (b) pin validator version and rule, (c) define target-year/scenario/weather/hour/zone/asset grain, (d) execute on original frozen files, (e) store machine-readable input+run manifest and output, (f) distinguish PASS/FAIL and owner-approved exception. Do not accept a synthetic fixture in lieu of a true IoSN-source result.

**Weather boundary:** V004–V006 check only received already-selected case IDs, weights, profiles and time series. Never implement/select/reproduce PCA/K-Means weather-year selection.
