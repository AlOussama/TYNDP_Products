# ML-C20/06 – Domain profiles, without polluting CSNF core
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

| Profile | Controlled terms / typing | Must stay an explicit source choice |
|---|---|---|
| Storage | battery, grid port signed MW, energy ledger MWh, eta, state boundary, service ability | Eterminal, loss law, quantifier domain, availability |
| EV | fleet, vehicle_id, individual departure, charging window, V2G flag | aggregation error proof and V2G authorization |
| Electricity Networks | bus, branch, physical connection, oriented flow, KCL and KVL guards | DC assumptions, reactance, topology/slack, mandatory network detail |
| Hydrogen | mass flow kg/h, energy basis MWh_LHV/MWh_HHV, converter | conversion factor/vintage/temperature/reference policy |
| Investment | staged decision, lead time, discrete module and infoset | integrality and resolution policy |
| KPI/CBA | cost ledger, currency, price year, discount, counterfactual and selection | N2E authority, discount rates and KPI inclusions |
| Multi-Model | common snapshots, comparison contract, independent evidence and variation | allowed structural model differences and robustness rule |

Profile IDs have semantic versions and approved source refs. Unknown policy or owner stays unresolved. Domain vocabulary is a registry of typed referent kinds, operators, quantity bases and oracles, not extra core classes by default. Explicitly prohibit implicit model-specific variable domains, PTDF topology or Solver IDs as requirement except when source-authorized.
