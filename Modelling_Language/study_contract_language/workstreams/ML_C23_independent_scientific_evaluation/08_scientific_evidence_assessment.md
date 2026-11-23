# ML-C23/08 – Evidence ladder and falsification criteria
Version: ML-C23 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
Common baseline: 2f0297b754e3a96a2523a34d3af98782b26181f3 (ML-C19 draft PR #55). External: mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce; OMG SysML 2.0 / KerML 1.0 / API 1.0. No independent human audit. G1 BLOCKED.

| Evidenz | What it supports | What it does NOT support |
|---|---|---|
| CONCEPTUAL | design plausibility and open proof obligations | parser correctness, human usability |
| SOURCE_INSPECTED | observed behavior/documented mechanisms at pinned version | fresh execution in this bundle |
| EXECUTED_SYNTHETIC | case and environment-specific asserted properties | general soundness or realistic study conformance |
| NATIVE_EXECUTED | observed parser/API behavior at a specified implementation version | normative mathematical equivalence |
| FORMALLY_PROVED | theorem only under explicit assumptions and fragment | wider architecture fitness without other evidence |
| HUMAN_EXECUTED | measured authoring/interpretation outcomes | full external validity without replication |

Case-level record fields: case_id, candidate, artifact_SHA, oracle_revision, executable_steps, observed, expected, PASS/FAIL/BLOCKED/INCONCLUSIVE/NOT_EXECUTED, E1..E5 claim-kind, source+audit link count, diagnostic, risk, reviewer. Predefine no evidence = NOT_EXECUTED. Do not equate normalization with verifier compliance.
