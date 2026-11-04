# IoSN formal specification — Independent process-first study

**Stand:** 2026-11-04. **Scope:** IoSN 2026 only; no CBA interoperability or generic robustness stream. **Status:** Research/architecture proposal, not ENTSO-E endorsement; draft methodology. **Branch:** `research/iosn-formal-specification-2026-11-04`.

## Source-of-truth hierarchy
1. **O / Official:** ENTSO-E *TYNDP 2026 Identification of System Needs Methodology*, **Version for Public Consultation**, 25 Feb 2026, [official PDF](https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf). This is **not verified as final/approved**. Citation syntax: `[O26 §x, p.y]`; page numbers refer to printed document pages.
2. **OS / Official scenario source:** ENTSO-E/ENTSOG *TYNDP 2026 Scenarios Methodology Report*, Annex III, [online](https://2026.entsos-tyndp-scenarios.eu/scenarios-methodology-report/annex-iii-weather-year-selection-methodology/); independently dated/versioned release status is an open issue.
3. **R / Research:** Repository `docs/current/` contains scientific research and PyPSA prototypes. These are **not normative IoSN requirements**.
4. **D / Derived:** Solution-neutral System Requirements inferred from O26; require methodology-owner sign-off.
5. **X / Demonstrator:** Illustrative constructs, algorithms, adapters and acceptance thresholds **not asserted to be required by ENTSO-E**.

## Deliverables
- `01_executive_summary.md`: source-first interpretation and key findings.
- `02_iosn_process_analysis.md`: process matrix, dependences, output and unresolved method decisions.
- `03_system_requirements.md`: SyRS with stable IDs and full requirement attributes.
- `04_language_requirements.md`: LRC derived from SyRS.
- `05_existing_languages_review.md`, `06_language_capability_matrix.csv`, `07_architecture_options.md`: language evaluation, evidence levels and architecture comparison.
- `08_formalisation_use_cases.md`: UC-01 weather, UC-02 electricity/H2 & investments, UC-03 system needs.
- `09_verification_traceability.md`: conformance and verification architecture.
- `10_poc_specification.md` and `poc/`: executable prototype, schemas, case files and verification report.
- `11_critical_review.md`, `12_architecture_decision.md`, `13_implementation_roadmap.md`: review, conditional ADR and implementation gates.
- `sources_inventory.csv`: auditable primary/secondary source index.

## Governance / exclusions
The repository branch is an exploratory document set, **not** a normative version of the methodology. No existing IoSN implementation has been changed. Every executable test validates its narrowly scoped **X demonstration contract**, not formal compliance of PyPSA, Antares, Sienna or a complete IoSN implementation. Architecture recommendations are conditional. The earlier CBA architecture review is background only.

## Notation
`MR-*`: method obligation as paraphrased from source (confirmation pending); `SR-*`: tool-neutral derived System Requirement; `LRC-*`: language capability; `VC-*`: verification case; `EV-*`: evidence artifact. Status `O` = evidenced source; `D` = derived requirement; `X` = illustrative; `OPEN` = unconfirmed. Normative modality applies only to proposed contractual documents **after approval**.
