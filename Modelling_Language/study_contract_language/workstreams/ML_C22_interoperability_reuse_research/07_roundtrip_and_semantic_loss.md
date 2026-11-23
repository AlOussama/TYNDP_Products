# ML-C22/07 – Semantic mapping and audit roundtrip experiment design
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

## Two non-substitutable comparison functions
`semantics_equal`: compare typed C1–C8 obligations including guards, modal strength, port carriers, units, information sets, KPI basis, variation and evidence request/result status. `audit_equal`: compare semantic projection **and** independent Authority/source/owner decision identities and provenance multiplicity. A field cannot be moved to plain prose without a retrievable typed roundtrip promise.

## Deep positive/negative mapping oracles
| RC | Positive mapping | Required retention | Negative mapping to reject |
|---|---|---|---|
| RC01 | port usage / requirement+assumed and required; energy basis tagged | battery port + external ledger | nonapproved terminal default; performance-specific internal part requirement |
| RC03 | distinct PortUsages / carrier-quantity types and conversion precondition | electricity consumption and H2 production | mass-energy dimension erased, no LHV/HHV source |
| RC05 | port, connection, requirements to both KCL and KVL | physical graph + KCL AND KVL | KCL-only interpreted as both KCL+KVL |
| RC07 | nested scenario features plus typed time-indexed constraint | scenario InfoSet and nonanticipativity | first-stage leakage |
| RC08 | analysis/view + custom metadata for price year, weights, selection | KPI cost price-basis+aggregation | same number but inconsistent discount/weights |
| RC10 | model usages linked to common requirements, distinct verification records | shared contract independent models, evidence and variation | different source/evidence identities merged |

Other RC coverage: RC02 vehicle individual deadline and service capability; RC04 H2 mass/energy inventory basis; RC06 module integrality and commissioned stage; RC09 CBA baseline/counterfactual, price basis and unresolved N2E authority. These four cases require full C1–C9 mapping coverage but do not imply executed native roundtrip tests.

## Loss classification
FATAL_OBLIGATION_LOSS (mandatory predicates or scope changed); FATAL_OWNER_STATUS_LOSS (`OWNER_TBD` became APPROVED); FATAL_SOURCE_LOSS (distinct authority IDs merged); FATAL_EVIDENCE_LOSS (`NOT_EXECUTED` elevated to PASS); PHYSICAL_TYPE_LOSS (carrier/sign/dimension); OBSERVABLE_BASIS_LOSS (KPI price or weights); VARIATION_LOSS (required disclosure removed); OPAQUE_UNMAPPABLE (candidate can carry only raw unvalidated blob). No numeric loss rate reported; all export/import probes NOT_EXECUTED.
