# Handoff to BUNDLE-02 — CONTRACT WORK CONDITIONALLY ON HOLD

**From:** BUNDLE-01 workstreams A (methodology), B (input/provenance) and C (readiness assessment), 2026-11-10.
**Gate G1:** `BLOCKED / AUTHORITY_UNCONFIRMED` — **do not automatically initiate a normative Contract-development workstream.**

## Inventory of input baselines (read-only as delivered)

- MA-01: Draft PR #17, `research/iosn-ma01-requirements-baseline-2026-11-05`, commit `a86bbeb8377ac1c9a5c77d900ad287691397e506`. 50 MA01-MR, 48 active provisional SR, 18 P00–P17. All MA01-MR-012/049 remain **UPSTREAM_ONLY**.
- MA-02: Draft PR #18, `research/iosn-ma02-methodology-authority-2026-11-05`, commit `1c32643a578ec7a6531cf9d314a343dfb9c7fa5d`. 18 methodology change topics and 48 impact dispositions, no confirmed approved B release.
- BUNDLE-01 A: Draft PR #19, `research/iosn-bundle01-a-authority-2026-11-10`, explicit 21 owner decisions.
- BUNDLE-01 B: Draft PR #20, `research/iosn-bundle01-b-input-data-2026-11-10`, 87 objects, 17 source groups, 93 trace links, 28 proposed validation checks; no source payloads verified.
- BUNDLE-01 C: Separate Draft PR upon completion, `research/iosn-bundle01-c-readiness-review-2026-11-10`; signed review **not** obtained.

## Explicit conditional acceptance contract for BUNDLE-02

**Do not begin normative Contract specification unless ALL of these are evidenced and signed:**
1. Methodology release + source bytes + SHA256 + version + formal approving authority + effective date for 2026; complete 50 MR/48 SR delta and change-control decisions.
2. Owner-validated input inventory (source ID, dataset and file release, content hash, timestamp, legal/access conditions, study year, scenario and selected weather-ID references, time/space/units, transformations) including all required input families and 18 step boundaries.
3. All P0 methodology, data and model semantics decisions closed with authoritative domain owners; remaining open items either closed or expressly justified as nonblocking by gate authority.
4. Approved verification acceptance cases for data, reduction, LF/optional OPF, two-stage LP, storage, H2 sensitivity, economics and report KPIs; no fabricated numeric tolerances.
5. Independent human/organizational reviewer sign-off including the 23 open findings, 20 process-only data object disposition and actual executed evidence.
6. Explicit written Gate G1 PASS decision signed by accountable owner/approver; existing Draft PRs remain unmerged unless separately approved.

## Work that MAY be performed before G1 PASS

- Read-only public source discovery and original-file checksum retrieval, official owner clarification preparation, contractual terminology reconciliation as **non-normative exploratory analysis**.
- Owner-specific checklists, synthetic data-validation prototypes **explicitly flagged as provisional** if separately commissioned, not promoted as accepted IoSN controls; no alterations to IoSN production implementation.
- Independent review work, evidence collection and requirements allocation of 20 process-only objects.
- Add controlled revisions on separate branches/PRs; protect original MA01/MA02 baselines.

## Out of scope even after preliminary work

No PCA/K-Means weather-year selection/reproduction (upstream only). No choice of YAML/GEMS/math-spec/other language or software/tool adapter by BUNDLE-01. No CBA interoperability programme conflation, no blanket robustness requirement, no solver-specific implementation mandate, no automatic merges.

**Handoff state:** `READY_FOR_OWNER_CLARIFICATION_AND_INDEPENDENT_AUDIT`; `NOT_READY_FOR_NORMATIVE_BUNDLE02`.
