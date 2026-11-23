# ML-C22/03 – Actual SysML pilot feasibility and native test ledger
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

## Sources actually inspected
Official OMG SysML v2.0, KerML v1.0 and Systems Modeling API 1.0 specification pages confirm current normative bases and machine-readable representations. Release `2026-09.1` of Systems-Modeling SysML-v2-Pilot-Implementation was located at https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation/releases/tag/2026-09.1. Release notes identify Eclipse plugin version 0.63.1 and a regression fix relative to 2026-09, while API and Services remain on their separate release cadence. Reference release https://github.com/Systems-Modeling/SysML-v2-Release/releases/tag/2026-09.1 includes standard libraries, BNF, and **informative** pilot material. Preliminary SysML 2.1/KerML 1.1 issue-resolution documents in that package do not supersede the named normative baselines for this experiment.

## Native execution ledger
| Planned test | Input | Environment/protocol | Actual status |
|---|---|---|---|
| N-S01 parse Port/Part/Requirement fragment | examples/sysml_contract_fragment.sysml | version-pinned pilot language parser | NOT_EXECUTED |
| N-S02 reject wrong carrier/quantity stereotype | RC03 negative | type-check + profile validation | NOT_EXECUTED |
| N-S03 export via Systems Modeling API v1 and import | identity+Owner source+Evidence links | diff semantic and audit projections | NOT_EXECUTED |
| N-S04 reparse canonical roundtrip RC01/03/05/07/08/10 | positive and negative | golden version ML-C23/r0.1 | NOT_EXECUTED |

The candidate `.sysml` file is an **unvalidated research sketch**, not verified native SysML syntax. A Java runtime alone is not sufficient evidence that Eclipse/Xtext/REST API parser+libraries are present; no native parser invocation or logs were produced. Request full packaged tool environment and run IDs before claiming H0 test results.
