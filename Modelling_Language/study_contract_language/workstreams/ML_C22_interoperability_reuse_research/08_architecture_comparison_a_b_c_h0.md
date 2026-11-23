# ML-C22/08 – A/B/C/H0 architecture falsifiable comparison
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

| Candidate | Plausible advantage | Critical cost to measure | Falsifier |
|---|---|---|---|
| A independent small semantic kernel | explicit C1–C9 contracts and straightforward validator | new grammar, schema, independent tooling | unacceptably high author errors or standard profile with lower effort |
| B SysML/KerML-based CSNF | mature standard type/part/port/requirement concept inventory | metamodel, profile annotations, API roundtrips and training | source/Owner/evidence loss or implicit internal model architecture |
| C federated CSNF mappings | existing languages used in context, common audit layer | adapter/registry maintenance and cross-tool drift | mappings fail roundtrip or external ledger breaks authority tracing |
| H0 small standard profile sufficient | no new authoring language needed | must show full C1–C9 external obligation + audit retention | any irreducible semantic loss or intolerable total operational complexity |

H0 is not rejected merely because base SysML lacks an energy-specific unit concept: a **small controlled profile** may be acceptable. H0 is not accepted merely because a text sample looks expressive: native parser/type/API export and a controlled human-use study are prerequisites. No weighted score where K01–17 weights are unapproved. Known evidence is source-level mechanism support and conceptual mapping only; therefore `H0_STATUS=UNRESOLVED`.
