# ML-C07 — Cross-Tool Scientific Comparison Rules

**NONNORMATIVE DESIGN · 2026-11-12 · NO NATIVE COMPARISON EXECUTED · G1 BLOCKED.** Sources: ML-R04 future_multi_tool_pilot_requirements.md (ML-R00 #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2), ML-C03 #46 @ 212bad6811877f9b974b20a1047913c18b1ba756, ML-C04 #45 @ 256541e763147dcb118a3a9d24ca2f52035c672e, ML-C05 #44 @ 1d1bfd18e92d457b415bbad54450bd5aec10963a.

## 1. Scientific claim: compare *separately verified models*, not two output files

An equality of reported costs, energy outputs or portfolios is **neither a proof of the same feasible set nor an independent reference oracle**. First establish the contract/input identity and per-arm evidence. Then select exactly which proposition is being compared: semantic input identity, E-FEAS projected feasible sets, E-OPT-VALUE optimal objective values, E-OPT-SET optimal solution set, or E-OBS selected observables/KPI. A claimed relation must state quantifiers, projection, objective basis, oracle authority, tolerance and proof method.

**Separation-of-implementations rule:** Team B must generate its mathematical model from the same *semantic contract* as A and independently authored implementation code. Running Tool B on Tool A's LP/MPS/translated model is a **translation-portability experiment**, not this two-tool independence trial. Report shared third-party libraries and generated code, use independent review to assess whether they encode common scientific decisions.

## 2. Comparison ordering and validity checks

| Stage | Required input / independent check | Outcome when unmet |
|---|---|---|
| **X0 Version/authority** | Same frozen contract semantics, 48-SR coverage, method/source release identity, decision profile D1–D6 and conditional variant | Stop comparison; record mismatched contract/authority, no cross-tool verdict |
| **X1 Source/data** | Observed source byte provenance, original vs synthetic class, study-year/CY/time/unit/region/carrier and candidate maps, w(c)/Δt and all transformations | Different scientific input ⇒ comparison **not valid**; V1/V2 assertion may FAIL on proven mismatch or BLOCKED on unknown source |
| **X2 Independent native generation** | Two independent generator code/builds, actual E04 model IDs, sufficient E03 lineage and native→semantic mappings | Reject two-arm independence inference; inspectability loss may yield UNSUPPORTED/BLOCKED |
| **X3 Per-arm obligations** | V1–V3 and relevant D0–D3; high-risk invariants proved for *each* model against independent oracle and actual generated rows | Mathematical FAIL or unresolved result recorded for affected arm independent of other arm |
| **X4 Per-arm solver/certificate** | E05 feasibility, reconstructed objective, certificate/bounds for claimed optimality; compatible numerical conventions and approved tolerances | Withhold optimality comparison if no sound certificate or acceptance oracle |
| **X5 Per-arm raw & KPI** | E06 raw vector with complete axes; E07 independently calculated formula, correct weights/Δt/units and owner status | Block undefined KPI; raw differences not silently filtered or suppressed |
| **X6 Cross-arm relations** | Explicit mapping to same projected decisions and cost/observable basis, accepted oracle/analytical proof or bounded empirical evidence | Report only narrow observed agreement; trigger D4 for material unproved equivalence |
| **X7 Review/claim** | Full assertion universe including P15 guard; E08 six-state vectors and exceptions, qualified external reviewer and separate owner/gate decision | Conformance claim withheld; no G1 promotion |

Compare **within an identical study-year horizon**; three study years are separate optimisations. CY weights are shared across years as a vector, not forced uniform across the five cases. A difference in file ordering or variable names has no semantic force once a typed mapping is validated.

## 3. Reconciliation dimensions and allowed differences

| Item | Must be semantically equal | Permissible variation | Falsification / escalations |
|---|---|---|---|
| Contract applicability | Same adopted/declared research obligations, 48 IDs, stage and guard | Internal feature flags if provably mapped to same condition | Missing mandatory SR or false P15 N/A |
| Data/time | Same source identity, valid crosswalk, five external cases per year, vector w(c), UTC intervals and unit dimensions | CSV versus columnar storage, internal timestamps/index order | Misaligned local time, case weights, Δt, geographic identity |
| Transforms | Same required before→after semantics/invariants and data exceptions | Different independent ETL code or representation | False producer edge, lost power/energy, altered baseline |
| Decision structure | One per-study-year investment portfolio shared across CY | Native shared variable or explicitly equality-coupled copies | Missing nonanticipativity row, cost counted per CY |
| Physical electricity | Correct KCL and physical KVL/angle/PTDF/cycle and owner-defined offsets | Different slack/reference and formulation with proven projection | Free physical cycle, wrong PTDF/LODF, unproven N−1 |
| Market candidates | Controllable directional NTC, KCL and asset type mapping | Different auxiliary flow variables and candidate IDs | Erroneous inclusion in AC physical cycle; unsourced cap |
| Stages & coupled assets | Correct stage eligibility/carry state, storage SoC, H2 exogeneity and hydro/DSR restrictions | Different constraint decomposition and canonical units | Hidden expansion 2035 storage, final H2 baseline substituted, lost efficiency |
| LP/solver | Primal feasible and proper optimality proof for each identified instance | Interior point vs simplex, presolve, dual conventions, basis, numerical rounding | Objective equivalence with bad generated constraints does not suffice |
| Optimum portfolios | Correct feasible optimal-set relation under accepted cost and input | Distinct equally optimal physical investment vectors | Do not FAIL on differing IDs/vectors alone; inspect optimal face/invariants |
| KPI | Same **approved** formula and raw lineage for same selected observable | Different derived values when KPI is portfolio-dependent | Need E07 replay, certified range or explicit non-invariance |
| P15 | When invoked, LF-reference portfolio cap and conditional model/result | Absent P15 if independently proven OFF | OFF unproven ⇒ BLOCKED; ON missing ⇒ UNSUPPORTED |

## 4. Proposed comparison algorithm

~~~text
compare(A, B, contract, fixture, oracle_profile):
  assert both independently implemented; otherwise RECORD_INVALID_INDEPENDENCE
  freeze X0..X2 identity, guards and maps; otherwise RECORD_INCOMPARABLE
  for each applicable SR-linked assertion q:
      evaluate A(q) and B(q) independently under C05 six-state rules
      preserve actual evidence E01..E08 per target and cause
  establish native-to-common-projection maps for investment/operation/network/KPI
  compare only relations for which scope, objective basis and accepted oracle exist
  if a material formulation change cannot be proved:
      require D4 targeted equivalence proof/counterexample search
      return EQUIVALENCE_UNRESOLVED for that relation (not a C05 status)
  record E-FEAS / E-OPT-VALUE / E-OPT-SET / E-OBS independently
  keep different optimal portfolios if independently feasible and optimal
  recompute each KPI from its own raw portfolio; declare invariance only if proven
  report full six-state vectors + independent reviewer disposition + external G1
~~~

**EQUIVALENCE_UNRESOLVED** and **RECORD_INCOMPARABLE** are *comparison report labels*, **not** additional C05 atomic test statuses. An assertion that cannot be evaluated because required mapping/oracle is absent receives BLOCKED with the cause in its own E08 record.

## 5. Cases that require more than observed equality

1. **Nonanticipativity (SR-029, B01/C02):** matching x on one synthetic solution is insufficient. Inspect shared variable index or scenario-copy equalities, objective coefficients and feasible-set projection. Wrong scenario-specific decisions can coincide accidentally on a small fixture.
2. **Physics (SR-018/035, B04/C04):** matching nodal injections and cost does not prove physical mesh KVL, nor that controllable market links have the required freedom. Inspect physical-cycle basis and market-link exclusion; angle/PTDF/cycle equality depends on compatible graph, offsets and rank.
3. **Grid reduction (SR-017/019, B05):** simple cut conservation does not imply PTDF/LODF/N−1 equivalence. A later owner-approved detailed-network reference and quality threshold are necessary.
4. **Objective (SR-027, B02/B11):** a positive affine rescaling may preserve minimisers but changes raw objective values; only a documented conversion to the same cost basis enables E-OPT-VALUE.
5. **Stages (SR-031/032):** a final portfolio match may conceal forbidden candidate or lost stage carry-forward; require native variable allowlists and state/cost transfer evidence.
6. **Storage/H2 (SR-007/009/034/050):** an equal energy aggregate can conceal dimension/efficiency/SoC or invalid P14 baseline; reconstruct source and constraint-level evidence.
7. **Multiple optima (B12/C07):** differing optimal portfolios are compatible with a valid equivalent model. Compare certified optimum values, feasible projected decisions and invariant or separately replayed noninvariant KPI.
8. **KPI (SR-001/045/046, B13/C08):** a shared erroneous filter or discount convention may make two dashboards agree; independently compute from E06 with approved formula. If formula or threshold TBD, report BLOCKED/UNDEFINED rather than guessed numeric PASS.

## 6. Numerical comparability: no hard-coded productive tolerance

The later protocol must freeze per-measure absolute/relative thresholds with **units, scales, feasible/primal/dual certification conditions, solver reliability assumptions and versioned authority**. Price/currency horizon, cost discount and CY/time weights need exact mapping. A single global epsilon is inappropriate across MW, MWh, currency, percentage and PTDF/LODF. Until authoritative tolerances exist, log unrounded numbers and informative differences **without PASS/FAIL for unresolved numerical assertions**. Exact rational synthetic expected values may be used with explicitly research-scoped floating-point diagnostics, never as production limits.

An instance-level optimality certificate requires independent primal feasibility and a sound bound/dual/other justified proof, not simply the solver's status. A model may return a feasible, not certified optimal, solution and still allow scoped feasibility observations.

## 7. Difference triage taxonomy

| Cross-arm observation | First diagnosis | Claim disposition |
|---|---|---|
| Different input digests/case maps | Input/source/provenance and transformation scope | INCOMPARABLE until reconciled; per-arm V1/V2 separately |
| Different row counts but mapped same projection | Index-elimination, redundant row or scaling proof | Potential EQUIVALENT_WITH_EVIDENCE; D4 if material |
| Same objective but a missing required row in one model | E04 constraint counterexample | Mathematical FAIL of affected actual assertion if established |
| Different certified optimal objectives for same valid instance | Costs/bounds/units/solver numerical or semantic mismatch | Investigate; no automatic selection of A or B as oracle |
| Equal certified optimal values but different portfolios | Multiple optimum face and candidate crosswalk | No automatic FAIL; evaluate E-OPT-SET/E-OBS/invariants |
| Different KPI but same correct objective | Portfolio-sensitive observable, formula authority, raw lineage | Compare independently and identify non-invariance |
| Tool cannot expose required native row family | Inspection capability not supported or unknown | UNSUPPORTED if established required absence; BLOCKED if evidence unclear |
| P15 not run, variant unknown | Guard/manifest inconsistency | BLOCKED; not NOT_APPLICABLE |
| Solver crashes on one tool | Run/solver diagnosis; retain model + errors | Not automatically V3 FAIL; status per actual assertion cause |
| Negative mutant passes undetected | Oracle/test sensitivity or generator trace defect | Audit test framework; no false conforming PASS |

## 8. Reporting rule and scope limitations

The cross-arm report must include: frozen input and contract version tuple; disclosure of team independence; model/solver evidence links per arm; tested domain and counterexample domain; six-state counts **with IDs**; exact N/A exclusion witnesses; status-specific blockers; each claimed relation E-FEAS/E-OPT-VALUE/E-OPT-SET/E-OBS with quantifiers, confidence/proof and non-implications; independent review role and owner/G1 states.

No partial score can bury UNSUPPORTED or BLOCKED obligations. Do not multiply coverage by number of passed synthetic fixtures. **Current ML-C07 result: comparison rules written, comparisons NOT_EXECUTED, actual tool capability NOT_ASSESSED, G1 BLOCKED.**
