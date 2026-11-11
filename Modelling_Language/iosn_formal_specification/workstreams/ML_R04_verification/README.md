# ML-R04 — Scope, baseline, traceability

**Status:** NONNORMATIVE_SCIENTIFIC_DRAFT · **Date:** 2026-11-11 · **G1:** BLOCKED / AUTHORITY_UNCONFIRMED.

## Exact input baseline

- Repository: `AlOussama/TYNDP_Products`, commit `5c13d4d63f18d30c308997cd7a01f2977fcc6b7b`, PR #25; branch `research/iosn-ml-r04-verification-2026-11-11` created **at this commit**, not at `main`.
- Source rows: `../../iosn_requirements_catalogue.csv` (48 MA01-SR, 48 L4 MA01-VN; sparse IDs **012 and 049 intentionally absent**); `../BUNDLE01R_C_requirements_reconciliation/requirements_blocker_matrix.csv`; BUNDLE-01R D closure report and unsigned G1 record.
- Matrix generation carries across **original provisional text, L4 key, verification method, priority, MD/CL blockers and approval status**, not a rewritten normative baseline.
- Source is the O26 public consultation draft; approved successor / effective date unverified. 21 MD/CL open; 0/28 genuine source-data validations; 23 findings open. All per-tool execution fields begin `NOT_EXECUTED`.

## Project overlay (non-normative; not an MA01 edit)

|Concern|Working decision applied to ML-R04|Boundary|
|---|---|---|
|D5-A1|Risk-based tiers; full algebraic 1:1 verification is **not** a universal requirement|Core mathematical invariants remain required; deeper proof when triggered|
|D4 weather|For each **2035 / 2040 / 2050**, use exactly 5 externally selected IDs `CY1..CY5` with equal, numeric **TBD** weights|Original SR-010 still says *three* in its 2026 draft acceptance criteria; do not silently amend; owner reconciliation later|
|Time / units|UTC-indexed instants; explicit duration and quantity semantics (MW, MWh, €/MWh, investment costs)|Calendar, DST, leap-day, tolerance values still MD-12/TBD|
|Fail-closed|Any mandatory FAIL / UNSUPPORTED / BLOCKED / NOT_EXECUTED disallows overall PASS|A positive synthetic assertion never grants productive conformance|
|Tool independence|Independently realised, tool-neutral contract and evidence interfaces|No model translation or preselected reference tool|
|D1–D6|Only effects **explicitly evidenced in this request/project context** are operationalised|No invented wording or missing details for D1–D6; binding decision ledger must be attached when released|

### File overview

- `requirements_verification_matrix.csv`: **48** traceable requirement-specific rows, proposed test depths and conformance evidence, with unchanged MA01 wording.
- `test_catalogue.csv`: **48** atomic test proposals, including falsifying mutations and evidence.
- `verification_architecture.md`, `risk_based_conformance_policy.md`, `mathematical_verification_rules.md`, `failure_and_evidence_semantics.md`, `tool_conformance_evidence_specification.md`, `future_multi_tool_pilot_requirements.md`, `independent_verification_review.md`.
- `synthetic_reference_cases/`: ten analytical fixtures, including intentional negatives; explicitly synthetic, not methodology parameters.

### Automatic construction audit

All 48 IDs were matched 1:1 against the frozen source catalogue and B01R blocker rows; tier counts **A=33; B=12; C=3**; 48 test IDs; initial statuses are `NOT_EXECUTED`. This is only a structural / traceability construction check, not execution or acceptance of any scientific benchmark.