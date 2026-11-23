# ML-C23/10 – Frozen benchmark handoff to ML-C24
Version: ML-C23 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
Common baseline: 2f0297b754e3a96a2523a34d3af98782b26181f3 (ML-C19 draft PR #55). External: mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce; OMG SysML 2.0 / KerML 1.0 / API 1.0. No independent human audit. G1 BLOCKED.

Freeze identity: `ML-C23/research-r0.1` + common B0 SHA. Artifacts: `02_reference_case_golden_baseline.md` (domain oracle), `03_adversarial_mutation_suite.md`, `04_metric_operationalization.csv`, `data/golden_cases.json`, `data/mutation_cases.json`. C24 must use the same oracle version for all compared approaches and preserve NOT_EVALUATED. Any change is an explicit re-baseline with review and impact table.

Handoff conditions: schema signatures and AST/validator/mapping versions from C20–C22 known; test receipts with environment+run ID; B1 typed handshake; B2 evidence and uncertainty per K01–17/NFR01–18. No C24 architecture score or release until conditions documented. E1/E2_obligation/E2_audit/E3/E4/E5 statuses separate. Gate G1 BLOCKED.
