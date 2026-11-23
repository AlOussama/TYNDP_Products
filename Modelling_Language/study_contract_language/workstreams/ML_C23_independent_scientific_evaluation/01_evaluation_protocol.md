# ML-C23/01 – Präregistriertes wissenschaftliches Evaluationsprotokoll
Version: ML-C23 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
Common baseline: 2f0297b754e3a96a2523a34d3af98782b26181f3 (ML-C19 draft PR #55). External: mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce; OMG SysML 2.0 / KerML 1.0 / API 1.0. No independent human audit. G1 BLOCKED.

## Reihenfolge und Unabhängigkeit
B0 SHA fixed -> freeze benchmark research-r0.1 -> development handoffs B1 -> identical case submissions -> B2 evidence evaluation -> B3 C24 comparison. The evaluation group does not tune expected labels based on C21 diagnostics or C20 parser design. Material revisions use a new immutable oracle version with rationale and changed case list.

## Eligibility / blind evaluation
Accept A standalone CSNF, B SysML/KerML profile, C federated CSNF and H0 small standard profile, each with fixed public interfaces and running instructions. Case-specific authoring is allowed; additional unjustified internal equations count against K03. Mask candidate labels in blind review; randomized but logged task order; separate technical and domain review.

## Outcome semantics
`PASS` requires executed tests plus exact evidence references; `FAIL` requires reproduced contradiction; `BLOCKED` unresolved authority or missing precondition; `INCONCLUSIVE` insufficient/incompatible evidence; `NOT_EXECUTED` no run. E1 equality = same typed canonical graph in proven ruleset fragment; E2 contract interpretation, E3 observable, E4 feasible-set mathematics, E5 permissible structural difference are separately recorded. `NOT_EVALUATED` is missing metric, never numeric zero.

## Reproducibility contract
Record source pin, case revision, tool and environment hashes, commands, input/output checksums, run ID, author role and blind reviewer; capture failures and unexecuted tests. Separate semantic graph equality from audit ledger equality. Only explicit authority may settle N2E or D1–D6. G1 remains BLOCKED.
