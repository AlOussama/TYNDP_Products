# ML-C22/04 – Pinned GEMS Library / System reuse and semantic boundaries
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

**Source read:** https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md, https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/system.md. Library YAML `library.port-types[].fields[]` has scalar-valued port field identifiers, and `library.models[]` defines mathematical formulations with variables/constraints and binding-constraints. System YAML `system.components[]` instances `library.model`; `system.connections[]` links `component1/port1` to `component2/port2`. GEMS source example `sum_connections(flow_port.flow)=0` is a library balance equation, **not** a declared universal KVL or physical carrier schema.

| CSNF external element | Reuseable GEMS notion | Boundary / added profile field |
|---|---|---|
| ComponentRole | model ID / component instance | role identity != same internal equations |
| ExternalPort | port-type + port field | carrier, physical kind, unit, sign, direction, temporal support |
| Connected_to | system connections | physical vs market-link and orientation, cardinality |
| A/G safety | library binding constraints as possible implementation | external claim, assumption, scope and source are separate |
| Dynamic ledger | scenario/time parameters and candidate constraints | integration, terminal, efficiency basis must be source-bound |
| Observable | views/outputs | price basis, aggregation, verification oracle |
| Variation | alternative libraries/models | explicit allowed alternatives and disclosure status |
| Authority+Evidence | library/system revision plus independent external ledger | Owner, method version, run and audit provenance |

### Positive and negative RC03
Positive conceptual mapping: component `electrolyser_1` with separately tagged electricity MW consumption and hydrogen kg/h output ports, referenced external conversion basis and evidence request. Negative: field `flow` reused as common numeric across carriers without profile quantity typing; GEMS connectivity alone cannot certify mass-energy conversion. **No GEMS parser, solver, or port-conformance run was executed.** Reuse recommendation: component/graph mapping, not binding every compliant tool to GEMS's internal algebra.
