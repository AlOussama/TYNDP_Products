# ML-C23/03 – Adversarial Mutations, frozen research-r0.1
Version: ML-C23 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
Common baseline: 2f0297b754e3a96a2523a34d3af98782b26181f3 (ML-C19 draft PR #55). External: mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce; OMG SysML 2.0 / KerML 1.0 / API 1.0. No independent human audit. G1 BLOCKED.

## Protocol
For each baseline case, apply one semantically minimal mutation. Oracle must report `E1_DIFFERENT`, `BLOCKED`, or `FAIL_STATIC` depending on exact typed input and documented rule; it may not report `E1_EQUAL` or `CONFORMANCE_PASS`. A DIFFERENT verdict is not a proof of scientific nonconformance: a coherent alternate contract can be well-typed and meaningful.

| ID | Mutation | Expected outcome | Safety assertion |
|---|---|---|---|
| MUT-01 RC01 | 2 MWh inferred or missing terminal owner rule | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-02 RC02 | aggregate MWh right but EV2 misses departure | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-03 RC03 | MW compared to kg/h or missing heating value | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-04 RC04 | kg treated as MWh or HHV/LHV substituted | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-05 RC05 | circulating flow satisfies KCL but violates KVL | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-06 RC06 | 0.3 module accepted as physically buildable | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-07 RC07 | future weather revelation changes first-stage choice | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-08 RC08 | omits time weight or double-counts CAPEX | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-09 RC09 | counterfactual demand altered without approved scope | BLOCKED when authority not approved; otherwise E1_DIFFERENT | No silent semantic merge |
| MUT-10 RC10 | unsupported E4 assertion from equal objective or concealed extra assumption | E1_DIFFERENT or BLOCKED per supplied missing basis | No silent semantic merge |
| MUT-11 | REQUIRED changed to PERMITTED | E1_DIFFERENT | Normativity preserved |
| MUT-12 | two authority IDs reduced to one | AUDIT_DIFFERENT/LOSS | Provenance multiset preserved |
| MUT-13 | evidence request NOT_EXECUTED promoted to PASS | FAIL_STATIC | no claim without executed run |
| MUT-14 | alias battery.grid resolves to two qualified ports | BLOCKED | no ambiguous reference resolution |
| MUT-15 | scope guard omitted and treated as TRUE | BLOCKED or E1_DIFFERENT | no default guard |
| MUT-16 | port electricity/active_power gets hydrogen/kg type | FAIL_STATIC | carrier/dimension mismatch |
| MUT-17 | time snapshot 2 MW labelled 2 MWh with no duration | BLOCKED | time integration required |
| MUT-18 | KCL-only asserted E4-equivalent to KCL+KVL | E4_NOT_PROVED | no false positive equivalence |

## Adjudication
The exact categorical expected outcome is frozen at the fully typed fixture level; this prose permits a limited disjunction only when an input deliberately lacks a field. The JSON data fixtures use specific conservatively labeled outcomes. For incomplete cases the test cannot be counted as a successful rejection until evaluated against a concrete input and fixed oracle.
