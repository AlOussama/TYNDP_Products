# BUNDLE-01R A — Methodology Authority Reassessment

**Scope:** ENTSO-E TYNDP 2026 Electricity IoSN, as of 2026-11-10. **Verdict: `AUTHORITY_UNCONFIRMED`, `G1-A=BLOCKED`.** Baseline O26 only; PR16–PR21 unchanged. No A/B source-version delta can be substantiated.

## Verified governance source hierarchy

1. **O26**, ENTSO-E IoSN Methodology, printed title page: *Version for Public Consultation, 25 February 2026*, 65 pages. Official source: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf. PDF visually inspected page 1 and page 40 via public PDF reader. This is **not** an adopted/effective version claim.
2. **P26**, ENTSO-E Citizen Space: 26 February to 3 April 2026, consultation closed (https://consultations.entsoe.eu/system-development/tyndp-2026-identification-of-system-needs-methodol/); closure is not adoption. ENTSO-E announcement: https://www.entsoe.eu/news/2026/02/26/entso-e-releases-public-consultation-on-the-system-needs-methodology/, explicitly calls it a draft.
3. **Additional audited evidence SDC26FEB**, 113th ENTSO-E SDC final meeting minutes dated 3/4 Feb 2026, agenda 15.3 on printed page 9: the IoSN methodology was discussed as to be finalized for **written approval**. The nearby SDC decision on project portfolio updating (agenda 15.2) is **not a methodology adoption, not the 2035 IoSN-grid-eligibility crosswalk**. https://eepublicdownloads.entsoe.eu/clean-documents/sdc-documents/meeting-documents/2026/260203-04-SDC_Minutes_vFinal_for_publication.pdf. This strengthens governance provenance without closing MD-01.
4. **CBA4** already formally EC-approved as its own guideline; O26 §3.4 points to CBA4 §2.5.1 for project maturity. A CBA4 approval is not an IoSN methodology approval. https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/news/2024/entso-e_4th_CBA_Guideline_240409.pdf
5. **2026 Draft Scenarios download index** (https://2026.entsos-tyndp-scenarios.eu/download/) lists PEMMDB, PECD, hydro, demand, H2, network files; no direct authority over IoSN methodology and no frozen study-data file list or hashes.

## What was not verified

A later formally adopted/effective 2026 IoSN method, related authoritative adoption minutes or resolution, signed erratum, final consultation-outcome approval or Methodology Owner direction. Negative public-search results are **not** proof of nonexistence. Search trail: ENTSO-E IoSN/TYNDP hub, official news, Citizen Space, public download domain and publicly indexed SDC records (10 Nov 2026); exact separate approval/document could be internal/unindexed. `VERSION_B=NOT_VERIFIED`, `A_B_DELTA=NOT_ASSESSABLE`.

## Original-file integrity attempts

- Public PDF renderer fetched and displayed O26; an attempted raw file download via container download failed. An independent HTTPS curl attempt failed DNS resolution. Web extraction/visualization returns **rendered text/images, not the original PDF bytes**. Hence `O26_SHA256=NOT_COMPUTED`; no surrogate hash of a URL, scraped text or re-serialized PDF.
- Raw downloadable data files at 2026 TYNDP were not extracted as bytes; item-level release and hash `NOT_VERIFIED`.
- A **Git blob SHA from the repository is not equivalent to SHA-256 of an original ENTSO-E document**.

## Assessment of 21 decision points

`decision_resolution_register.csv` re-expresses 20 MD + MA02-CL-001 with priority, exact legacy context, source clause, MA01-MR/SR links, owner question, possible impacts, evidence, sign-off requirement and gate. **0/21 OWNER_APPROVED**, 0/21 safe to close. Source facts verified (e.g. damaged O26 §4.6 reference) are distinguished from owner decisions. The CBA4/O26 2035 discrepancy is still an **interpretation question, not an officially established conflict**.

## No policy/architecture drift

Selected weather IDs, weights and files are upstream-provided inputs only; `MA01-MR-012/049` remain outside active weather selection implementation. No PCA/K-Means reimplementation, no CBA interoperation, no robustness requirement, no adapter or tool/language design. All 48 SR remain provisional.

**Release prerequisite:** An authorized ENTSO-E IoSN owner must supply original final file or explicitly adopted O26, checksum, resolution/authority, publication and effective dates, annex coverage and any errata/consultation response; only then may a real version A/B reconciliation or written no-change attestation be undertaken.
