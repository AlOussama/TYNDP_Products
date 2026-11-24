# BUNDLE-ML-04 — research decision record (2026-11-24)

Status: APPROVED RESEARCH DIRECTION; WORKSTREAM EXECUTION NOT STARTED.
Governance: NON-NORMATIVE / RESEARCH ONLY. This decision record does NOT constitute owner approval of a production method, a tool, a new language or any G1 release.

## User decisions: scope and sequence

- D04-01 — The Study Contract Language remains GENERAL. ENTSO-E's 4th CBA Guideline is a VERSIONED, TRACEABLE DOMAIN REFERENCE for ONE STRESS-TEST USE CASE, not the language's normative target semantics or a reason to add CBA-only primitives. Cycle-specific TYNDP 2026 Implementation Guidelines require a separate source-version and publication/approval-status check.
- D04-02 — First execute the COMPLETE syntax/parse -> typed AST -> CSNF -> conservative validator -> evidence/report chain on SYNTHETIC CBA input. Only subsequently compare two independent energy-system models; no real-data or solver conformance is claimed in this bundle.
- D04-03 — Prioritize B1 interface closure and B2 scientific validation. Reuse-first comparisons of SysML v2/KerML, GEMS and mathspec continue in parallel; their native runtime readiness must be reported truthfully and must not artificially stall B1/B2.
- D04-04 — Unresolved methodological details may be used as explicitly documented, VERSIONED RESEARCH ASSUMPTIONS only. Never silently treat them as approved guidance, authoritative calculations, or OWNER-SIGNED decisions.
- D04-05 — Methodological assumptions, method choices, calculation rules and parameters MUST REMAIN EXTERNALLY CONFIGURABLE and readily replaceable. Do not bake a CBA discount rate, scenario weights, indicator formulas, selection conventions, price-base treatment, source priority or methodological choice into a language core or validator. A supported method/profile switch must NOT require modifying, recompiling or redeploying the core/validator. New mathematical operators are an explicit, justified extension boundary: do NOT promise arbitrary unseen algorithms are configurable without a corresponding executable semantics implementation.

## Binding research invariants

1. A general, compact typed semantic contract with C1-C9 remains a research HYPOTHESIS, not an architecture choice. Existing SLR01-SLR42, NFR01-NFR18, K01-K17, R00-R13, E1-E5 and RC01-RC10 are NOT narrowed or rewritten by CBA.
2. Strict separation of: syntax, AST, semantic normal form, method-specific declarative profile, inputs/snapshot, mathematical model internals, outputs, and authority/evidence ledger. A model retains internal formulation freedom; do not impose one optimization algebra.
3. A method profile must carry immutable identifier/version/content digest, provenance/source/version/publication status, method authority, assumptions/overrides, parameter units and domains, scope, rules with typed signatures, and compatibility with semantic-operator versions. The executed study must pin the resolved profile and parameter snapshot in a reproducible audit record.
4. A research assumption is not automatically an owner decision. OWNER_TBD remains BLOCKED as appropriate. G1 remains BLOCKED even if all syntactic tests pass.
5. Methods and profiles are DATA/SPECIFICATIONS, never unsafe free-text execution or dynamic arbitrary code. Validate compatibility first; reject unknown operators, invalid units, conflicting versions, missing lineage and unauthorized evidence promotions.
6. Both semantic meaning and audit/authority/provenance identity must survive supported roundtrips; compare separately. No upgrade to PASS without executed evidence, no assumption that equal KPI values prove feasible-set equivalence.
7. CBA study profiles are replaceable, but non-CBA RC and service-contract reference cases remain independently mandatory to test generality.

## Frozen repository research references

- ML-C19 B0 = 2f0297b754e3a96a2523a34d3af98782b26181f3; PR #55.
- ML-C20 = b81edeb7551aa786e0d309ccd5bc2271d244e450; PR #57.
- ML-C21 = cad6d30edf32476ee5e915dbea7566127cbffa5f; PR #59.
- ML-C22 = 828c87eb100646da6fcce5f8751af5f3f42c7600; PR #58.
- ML-C23 = d3d5362231d81a00fd6a19501bc7187f4ad12da5; PR #56.
- ML-C24-P1 = 506be1607e1e8a6eb50db2f1317961d5bbaffcce; PR #60.
- ML-C24-P2 = 01f4eb798aff5391a51aff2365e6841850907464; PR #61.
- ML-C24-P3 = 0e85be6d9d2a84dffd7bb2685e6548671be3ef17; PR #62.
- ML-C24-P4 = 4b61addb0e87205e6670e253bd65cb0428e08681; PR #63.
- ML-C24-P5 = eaea6dd99b736f2560866abda722cde78b908bce; PR #64.
- P3's previously pinned mathspec = 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS = c463e30b610443c1f59b20074bb7acffa2844cce.

Every execution workstream must verify actual available refs at kickoff, preserve these as immutable source pins, and register any later revision separately. No rewriting, merging or deleting earlier draft PRs to simulate integration.

## Official methodological references to verify/pin for EACH test

- ENTSO-E 4th CBA Guideline: https://tyndp.entsoe.eu/resources/guideline-for-cost-benefit-analysis-4.0
- ENTSO-E TYNDP 2026 Implementation Guidelines consultation: https://consultations.entsoe.eu/tyndp/tyndp-2026-cba-imp-public-consultation/
- TEN-E Regulation (EU) 2022/869: https://eur-lex.europa.eu/eli/reg/2022/869/oj

The 2026 consultation is not sufficient evidence of a later final approved publication. Retrieve the chosen exact official document, publication/status metadata, retrieval time, version and checksum at experiment start. Clearly separate official method source from synthetic methodological profile; use no unverified claim of official compliance.

## Evidence status at planning time

- B0: MET (pinned).
- B1: PARTIAL (P1 tests do not execute the pinned C21 Python validator end-to-end).
- B2: PARTIAL (P2 / P5 synthetic microoracles; not a complete typed-contract language benchmark).
- B3: NOT_READY. SysML/GEMS/mathspec native: NOT_EXECUTED. G1: BLOCKED.
- P5 36/36 independent finite synthetic checks, including 30 mutations, MUST NOT be recast as whole-language compliance.
- This bundle creates a RESEARCH PLAN AND HANDOFF ONLY. No new B1/B2 successful tests, native runs or owner approval are asserted.
