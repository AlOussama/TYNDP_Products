# GEMS pinned excerpt, documentation-level only
ML-C22 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
CSNF base 2f0297b754e3a96a2523a34d3af98782b26181f3; mathspec 5f1464c334c1012cdee2947d4d55b4d1d6bef40a; GEMS c463e30b610443c1f59b20074bb7acffa2844cce. OMG SysML 2.0, KerML 1.0, Systems Modeling API 1.0; pilot 2026-09.1 is IMPLEMENTATION, not normative. G1 BLOCKED.

GEMS `library.yml` example at https://github.com/AntaresSimulatorTeam/GEMS/blob/c463e30b610443c1f59b20074bb7acffa2844cce/doc/user-guide/input-files/library.md defines a `port-types` collection with a scalar field `flow`, a `models` collection with `bus` and `binding-constraints` expression `sum_connections(flow_port.flow) = 0`. This is a source quotation of one expression for analysis; it is *not* a CSNF external-port type, not KVL, and not a runnable adapted model in this repository.
