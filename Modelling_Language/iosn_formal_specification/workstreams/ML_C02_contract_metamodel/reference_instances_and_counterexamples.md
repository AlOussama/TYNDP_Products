# ML-C02 — Reference instances, metamorphic properties and counterexamples

**Research examples only.** All numerical fixtures in this document are **synthetic** and not sourced real CY weights, original input releases, owner-approved tolerance or productive tool executions. References point to ML-R00 / ML-R01 / ML-R03 / ML-R04 research descriptions; no official methodology or tool release is certified. Use these cases for architecture-independent logical conformance experiments.

## 1. R1 — valid project-profile, unequal common CY weights

~~~text
MethodologyProfile: profile:MLR00-D1D6-RESEARCH (authority=UNCONFIRMED)
StudyCases: 2035, 2040, 2050 [each independent run]
WeatherCase IDs per StudyCase: CY1 CY2 CY3 CY4 CY5 [externally selected]
weightRef: symbolic w(CY1)…w(CY5); numeric state=OWNER_TBD
equality obligation: for each c, w(2035,c)=w(2040,c)=w(2050,c)
sample synthetic fixture ONLY: [0.10, 0.20, 0.15, 0.25, 0.30] (sum=1.00)
~~~

**Expected:** structural/semantic equality across years passes; no **uniformity** obligation across c. In a productive contract, the absence of the real values is still an explicit blocking condition. D2 is a research profile deviation from the O26 consultation draft three-cases-per-year claim, not an adopted amendment.

**Counterexample CE-01:** use [0.10,0.20,0.15,0.25,0.30] in 2035, but [0.2,0.2,0.2,0.2,0.2] in 2040. Reject D2 cross-year equality. **CE-02:** force all five to 0.2 and claim D2 mandates equality *between* CYs; reject the source semantics even though a synthetic vector happens to be valid.

## 2. R2 — valid first-stage variable scope

~~~text
decision x(year=2040, candidate=K1, stage=S1): one 2 MW capacity decision
operating dispatch p(2040,CY1,t), ..., p(2040,CY5,t): case-specific
replicated form: x_CY1 = x_CY2 = x_CY3 = x_CY4 = x_CY5 = x
investment cost counted once; variable run cost weighted across CY
~~~

**Expected:** native single x and five replicated x with explicit linking equations have equivalent **contract-relevant projection** if all other assumptions match. **CE-03:** x_CY1=0 and x_CY2=4 with independent decisions is nonanticipativity violation. **CE-04:** multiply a single CAPEX by five CYs without a justified cost accounting transformation; objective distortion.

## 3. R3 — valid UTC/unit/axis binding and negative tests

~~~text
DataObject: B01-Dxxx (definition only)
DataInstance: instance:synthetic-demand-2040-CY2-t1
scope: year=2040, weather=CY2, spatial=zone:Z1, carrier=electricity
time: [2040-01-01T00:00:00Z,2040-01-01T00:30:00Z), duration=0.5 h
power: 10 MW interval mean; energy: 5 MWh
release: SYNTHETIC_FIXTURE (no original-source SHA-256 claimed)
~~~

**CE-05:** report energy=10 MWh by summing interval-mean MW without Δt → dimension violation. **CE-06:** declare 02:30 local time twice without UTC offset and still assert unique time key → unresolved time mapping; MD-12, BLOCKED for productive use. **CE-07:** implicitly convert 1 MWh_H2_HHV to 1 MWh_H2_LHV → invalid basis conversion.

## 4. R4 — valid physical-branch versus candidate-market-link semantics

~~~text
Existing physical reduced branch L1: from zone A to B; DC relation f_L1=b(θA-θB)+offset
Expansion candidate K2: proposed physical technology AC, MODEL role CONTROLLABLE_MARKET_LINK
K2 operating market flow m_K2: directional bounds -NTCminus(K2,x) ≤ m ≤ NTCplus(K2,x)
Both flows enter the same nodal conservation law with their signed incidence.
~~~

**Expected:** the market-link flow is not automatically constrained by the physical branch angle difference. Angle-flow vs consistent cycle-flow for the *existing* branch network is a candidate equivalence relation with a topology and offset witness. **CE-08:** add an unapproved KVL equation to K2 because its intended physical technology is AC → invalid role collapse. **CE-09:** replace all existing mesh branches by free bilateral transfers → may satisfy KCL, fails DC mesh/KVL.

## 5. R5 — valid network-reduction result family

~~~text
P05 clustering: every detailed bus maps to exactly one connected IoSN zone.
P06 reduced result family:
  no-load/reference flow; mesh relations; HVDC impacts;
  seasonal/directional capacity (Summer+/Summer-/Winter+/Winter-);
  equivalent impedance; PST impacts
verified_from: detailed-grid reference + topology revision + calibration provenance
qualityOracle: OWNER_TBD (PTDF/LODF/N-1/reference RMSE still unresolved)
~~~

**CE-10:** zone aggregation preserves total 50 MW injection/withdrawal but produces a reduced grid with zero cycle constraints; the successful 50 MW sum is **not sufficient** for electrical equivalence. **CE-11:** store only one “net transfer capacity” scalar rather than directional and seasonal ratings. Research schema can reject missing dimensions; actual numeric acceptance remains MD-03/13/15.

## 6. R6 — valid stage, optionality and status

~~~text
P10: eligible real on-/offshore candidates, LP mode=LF
P11: residual real + conceptual onshore + theoretical offshore; Stage1TransferRef=OWNER_TBD
P12: storage extension ONLY for years 2040 and 2050
P15: optional OPF, enabled=false with witnessed run configuration
R04 test for P15 conditional branch: NOT_APPLICABLE
LF mandatory checks: remain applicable, not automatically NOT_APPLICABLE
R04 native tool test status otherwise: NOT_EXECUTED
G1: BLOCKED
~~~

**CE-12:** execute storage expansion P12 for 2035 as if in scope. **CE-13:** call P15 “passed” without running it or provide no evidence that disabled branch was selected. **CE-14:** set P15 OPF candidate x=4 against comparable LF cap x=3 in a genuinely enabled run: **FAIL** on the scoped cap if the owner-approved mapping is applicable. Without approved mapping/oracle, label the research case **SYNTHETIC_ONLY** and productive outcome BLOCKED.

## 7. R7 — process-only data and traceability

Take original inventory object **B01-D001** (Methodology authority release manifest). It has a declared P00 link and **no direct SR link**. The valid graph contains DataObject(B01-D001) **LINKED_TO_PROCESS** P00. It does **not** invent MA01-SR-012, MA01-SR-049 or any SR. The remaining 19 process-only objects are listed in traceability_closure_report.md. **CE-15:** a generator requires every DataObject to have ≥1 direct SR and therefore either drops B01-D001 or creates a new SR → graph violates D1 and the R03 inventory.

## 8. R8 — derived KPI and multi-optimum observations

A raw output records a feasible expansion portfolio, objective value, solver status and run lineage. A derived KPI needs separately versioned formula, discount/aggregation and provenance. **CE-16:** promote an unapproved “system need” metric to **approved project** or synthesize a discount rate; blocked by MD-02/04/17. **CE-17:** portfolios xA≠xB satisfy the same feasible-set and optimal-objective criteria but are declared nonconformant solely because vector entries differ. This is not a valid universal criterion under multiple optima.

A valid comparison checks primal feasibility, objective / dual-bound witness, required physical and result invariants, KPI projection and owner-defined output tolerances. If portfolio-dependent output identity is itself methodically essential, request a tie-break rule rather than silently accept all differences.

## 9. R9 — negative evidence and governance

A proposed case R04-T-SR-029 has a falsifiable assertion, placeholder oracle and EvidenceRequest but no actual Evidence. This must remain **NOT_EXECUTED** in the native-tool test dimension, with **OWNER_ORACLE_TBD** and Gate G1 **BLOCKED** as separate dimensions. **CE-18:** creating a HAS_EVIDENCE relation to an *EvidenceRequest* and then promoting a test to PASS → invalid reference type and review semantics.

## 10. Suggested tests for all architectural realizations

Run all reference/negative cases through independent A/B/C graph exports; compare canonical semantic IDs, scopes, type errors, rejected examples and preservation of UNKNOWN. For native-tool pilots, replace synthetic payloads with frozen, qualified sources and approved oracles only in a later governed phase. A syntactic pass for these examples is **not** a productive IoSN conformance claim.