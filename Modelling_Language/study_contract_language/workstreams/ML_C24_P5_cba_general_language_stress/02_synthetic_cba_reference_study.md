# CBA reference stress scenario – an intentionally **non-authoritative** specimen

## Design objective
A generic Study Contract must express the question: *What are the benefits and costs of a prescribed synthetic interconnector P relative to a matching reference R under identical exogenous study inputs, across scenarios, according to precisely versioned indicators and method variations?*

For **each model m and scenario s**, the research specimen has two externally labelled case records `(m,s,R)` and `(m,s,P)`. Pairing crosses neither model nor scenario:
```text
annual_proxy_benefit(m) = Σ_s w(s) · [cost_proxy(m,s,R) - cost_proxy(m,s,P)]
illustrative_npv_proxy(m) = Σ_{y=1}^{10} annual_proxy_benefit(m)/(1+0.05)^y - 830 EUR
```
Only an **illustrative operating-cost proxy** is used; it is not the full CBA benefit indicator B1/socio-economic welfare (SEW), not a regulatory net present value and not an investment appraisal.

### Independent finite fixture
- Two synthetic weather/scenario IDs `S1` and `S2` with research weights `0.6/0.4`, study year `2030`, explicit UTC and a 1-hour duration field. Weights are typed `SCENARIO_PROBABILITY`; duration hours and Monte Carlo outage probabilities are distinct fields.
- M-A: declared `nodal_angle_dispatch`; M-B: declared `aggregated_flow_dispatch`. These are **labels in a synthetic data set, not implemented mathematical models**.
- Eight synthetic cost records indexed by `model × scenario × R/P`, with shared exogenous digests. No generator, solver, simulator or actual tool produced these values.
- `P1` adds a declared transmission-capacity intervention; no baseline project asset or unapproved exogenous drift. Proper interdependencies have to be declared explicitly.
- `OPERATING_COST_PROXY`: `EUR/year` in `real_2025`; benefits use `R - P` sign convention. Security and climate-adaptation indicators remain `NOT_EXECUTED`, `value=null`, not zero.
- CAPEX `830 EUR`, 10-year horizon and 5% discount rate are arbitrary **research choices**, not guideline rates or project valuations.

### Synthetic numerical sensitivity
The executed finite micro-oracle yields:
| Declared model role | Cost saving proxy (EUR/year) | Research NPV proxy (EUR) | Sign |
|---|---:|---:|---|
| M-A | 120 | +96.6081915 | positive |
| M-B | 104 | -26.9395674 | negative |

This is a **counterexample to equating declared common study purpose with identical decision outputs**. A difference of sign should cause analysis of method assumptions and tolerances rather than an automatic declaration of implementation error. Neither model has E5 conformance evidence; the two labels do **not** prove independent code implementations. E2–E4 remain unproved.

### Artefact separation
- `data/synthetic_cba_fixture.json` is an independent **research-oracle input**, not a valid instance of an existing C20 or C21 schema.
- `data/cba_csnf_role_sketch.json` illustrates C1–C9 roles, explicitly marks proposed operators and is **not executable**.
- `tools/cba_stress_oracle.js` evaluates research test expectations, not a Study Contract Language parser, validator or energy-system model.
- Owner `OWNER_TBD` and execution `NOT_EXECUTED` remain visible in every positive synthetic check.
