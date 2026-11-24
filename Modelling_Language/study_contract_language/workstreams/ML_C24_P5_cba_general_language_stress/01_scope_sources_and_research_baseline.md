# ML-C24-P5 / Scope, pinned sources and status
**Stand:** 2026-11-24. **Governance:** NON-NORMATIVE / RESEARCH ONLY. **Purpose:** use CBA to stress-test an **unrestricted general Study Contract Language**, not to define a CBA-only language.

## What is tested
A research interconnector CBA setting with two project states (without/with), two scenarios, two distinct declared model methods, typed inputs, paired scenario-specific comparisons, illustrative cost-proxy outcomes, controlled variation, source/owner/evidence lifecycle and negative fault injections. Distinguish language representation, test-oracle execution and actual model conformance.

## Immutable repository sources
- B0: `2f0297b754e3a96a2523a34d3af98782b26181f3`
- C20: `b81edeb7551aa786e0d309ccd5bc2271d244e450`
- C21: `cad6d30edf32476ee5e915dbea7566127cbffa5f`
- C22: `828c87eb100646da6fcce5f8751af5f3f42c7600`
- C23: `d3d5362231d81a00fd6a19501bc7187f4ad12da5`
- P1: `506be1607e1e8a6eb50db2f1317961d5bbaffcce`
- P2: `01f4eb798aff5391a51aff2365e6841850907464`
- P3: `0e85be6d9d2a84dffd7bb2685e6548671be3ef17`
- P4: `4b61addb0e87205e6670e253bd65cb0428e08681`
- mathspec: `5f1464c334c1012cdee2947d4d55b4d1d6bef40a`
- GEMS: `c463e30b610443c1f59b20074bb7acffa2844cce`

Associated drafts: [C19 PR55](https://github.com/AlOussama/TYNDP_Products/pull/55), [C20 PR57](https://github.com/AlOussama/TYNDP_Products/pull/57), [C21 PR59](https://github.com/AlOussama/TYNDP_Products/pull/59), [C22 PR58](https://github.com/AlOussama/TYNDP_Products/pull/58), [C23 PR56](https://github.com/AlOussama/TYNDP_Products/pull/56), [P1 PR60](https://github.com/AlOussama/TYNDP_Products/pull/60), [P2 PR61](https://github.com/AlOussama/TYNDP_Products/pull/61), [P3 PR62](https://github.com/AlOussama/TYNDP_Products/pull/62), [P4 PR63](https://github.com/AlOussama/TYNDP_Products/pull/63). All are unmerged independent research branches as inspected 2026-11-24. No retroactive changes to original workstreams.

Prior project CBA source (source checked at B0, not executed): `Modelling_Language/analysis/cba_contracts_and_tests.md`, `cba_interoperation_scenarios.md`, `cba_pilot_plan.md`. These contain draft/review requirements, not approved method details.

## Independent external method context – authority levels
- EU [Regulation (EU) 2022/869, Annex V](https://eur-lex.europa.eu/eli/reg/2022/869/oj/deu): regulatory source; mandates harmonised, transparent and cross-sector-relevant CBA and benefit/cost differentiation. It is **not** a CBA language or direct permission to invent all thresholds.
- [ENTSO-E 4th CBA Guideline](https://tyndp.entsoe.eu/explore/resources/guideline-for-cost-benefit-analysis-4.0): documented sectoral CBA-method source; selected indicators and interpretation must be pinned per study.
- [TYNDP 2026 Implementation Guidelines consultation](https://consultations.entsoe.eu/tyndp/tyndp-2026-cba-imp-public-consultation/): consultation text, not by itself proof that the final cycle-specific version was approved; status needs a separate current-document and methodology-owner check before normative use.
- [ACER CBA overview](https://www.acer.europa.eu/electricity/infrastructure/network-development/cost-benefit-analysis): independent regulator context, not an approval substitute.

External source titles, their authoritative status and the study-specific Owner decision are **separate fields**. The synthetic study uses `OWNER_TBD`, `NOT_EXECUTED`, and no officially authorised CBA-B1/SEW number. Changes to any normative methodology/source hierarchy must undergo explicit review.

## No scope reduction
All ML-C18 SLR01–42, ML-C19 NFR01–18, C1–C9 and E1–E5 remain governing research requirements. CBA tests only a subset of the general language; RC01–RC10 remain necessary controls. The general language is not to become a specialised CBA report schema nor a universal optimisation algebra.
