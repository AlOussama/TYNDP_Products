# BUNDLE-01R B — Reproducibility / Status Semantics

The `metadata_technical_check_results.json` was created from the **unchanged** BUNDLE-01 GitHub CSV file contents at commit `09cff8a8f9d82282d2e307f32ba8b139c3eb3824`; the JSON preserves each rule and result. Checks implement deterministic CSV quoting/column parsing, uniqueness, key presence and reference joins (see `tests`). Their original blob SHAs are recorded in the JSON to support later reproduction. The exact test version label is `B01R-META-v1.0`; not an independent third-party compliance validator.

For the 28 original data acceptance cases, the named current validator is `NOT_RUN_NO_ORIGINAL_SOURCE_DATA`, because no payload or approved numerical oracle is accessible. A future run **must** report tool versions, signed input SHA256, stdout/stderr, times, deterministic fixture, result and reproducible checks; none are claimed here.

Status distinction: `STRUCTURE_PASS_PROJECT_METADATA` ≠ `FILE_CONTENT_READ` ≠ `SOURCE_REVISION_APPROVED` ≠ `DOMAIN_RULE_SIGNED` ≠ `REAL_DATA_VALIDATION_PASS` ≠ `GATE_G1_APPROVED`.
