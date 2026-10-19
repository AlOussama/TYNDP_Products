# Repository inventory and open issues (2026-10-19)

## Confirmed remote inventory before restructuring
- 102 blobs in the original tree, including 20+ report/source variants, ZIP collections, source snippets, four tests, and synthetic CSV outputs.
- Canonical source had been nested under `revision_snapshot/IOSN_Revision_2026/code/`, which made package discovery and CI setup difficult.
- Identical reports/results occurred in multiple places; the original content is retained under `docs/archive/` and `artifacts/snapshots/`.
- **Missing in the original extracted source tree:** `__init__.py`, `screening.py`, `security.py`, and `security_projection.py`. These were present within the retained original code ZIP and must be restored before tests are considered executable.

## Scientific and integration restrictions
- IoSN normative algorithm is not fully public. The implementation is IoSN-near; do not claim exact ENTSO-E reproduction.
- Branch/PST/HVDC handling and nodal reference-data provenance need separate qualification.
- `F_0` structural no-load flow versus a FBMC reference-flow residual must be clearly distinguished.
- An individual N-1 bilaterally computed transfer bound is not a universal zone-link limit; keep the coupled CNEC region for formal security.
- Islanding contingencies cannot silently be excluded in a security-certifying path.
- Previous synthetic performance figures are **not** real-network verification.
- A real PyPSA end-to-end integration test and benchmark on a pinned network/dataset remain outstanding.

## Repository controls
- Canonical Python under `src/tyndp_reduce/`, tests `tests/`, examples `examples/`.
- Formal methods/report documentation `docs/current/`, historic reports `docs/archive/`.
- Historic zipped bundles and unchanged previous report versions under `artifacts/`.
- Synthetic sample results `results/synthetic/`.
- Unverified components shall be explicitly labelled and must not be called complete.
