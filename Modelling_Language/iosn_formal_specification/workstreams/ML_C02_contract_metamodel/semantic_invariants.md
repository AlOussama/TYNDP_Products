# ML-C02 — Semantic invariants, guard semantics and forbidden states

**Research-only.** Invariant IDs INV-xx are **design assertions**, not MA01-SR nor officially approved mathematical acceptance thresholds. Classification: **STRUCT** = directly checkable on authored graph; **SEM** = domain/property check requiring typed meaning; **OWNER** = requires unresolved authoritative input; **RUN** = native execution and evidence required.

| ID | Class | Research invariant / executable interpretation | Counterexample or blocker |
|---|---|---|---|
| **INV-01** | STRUCT | Exactly the active 48 unique MA01-SR from MA-01; SR-012/049 absent; 1 provisional L2 baseline | Additional synthetic SR-049 |
| **INV-02** | STRUCT | Exactly P00–P17, M01–M18, LR01–LR20 in contract graph | Omitting P17 because it is a review step |
| **INV-03** | STRUCT | All 87 R03 B01-D001…D087 have typed nodes and ≥1 P link; 20 process-only nodes preserved with zero permitted SR links | Dropping D085 or inventing SR to cover it |
| **INV-04** | STRUCT | Exactly 38 proposed MLR03-Txx-yy transformation definitions; ≥1 input/output type and 1 P reference each | Undefined intermediate reference |
| **INV-05** | STRUCT | Every active SR has SourceClause reference, research capability link, verification need, proposed R04 test and an applicability scope | Orphan test or untyped source link |
| **INV-06** | STRUCT | All relationship endpoints exist and have permitted domain/range; node identity (namespace, ID, revision) unique | NTC capacity pointing to a currency object |
| **INV-07** | STRUCT/SEM | Source draft, historic source, research decision and approved source are non-interchangeable, dated and scoped | O26 marked ADOPTED by schema pass |
| **INV-08** | SEM/OWNER | D1–D6 belong to the named research profile; owner MD/CL unresolved until owner evidence; source O26 claim not rewritten | Silent resolution of D2–O26 disagreement |
| **INV-09** | STRUCT | Target study years Y={2035,2040,2050}, separate study/run identity; no added cross-year endogenous optimisation | Single unmarked 2030 run |
| **INV-10** | STRUCT/SEM | Exactly five **externally supplied** CY1…CY5 per year in D2 research profile; weather selection is out of IoSN | Deriving CY cases with internal PCA as a new mandatory process |
| **INV-11** | SEM/OWNER | For each c: w(2035,c)=w(2040,c)=w(2050,c)=symbolic w(c); **not** w(CY1)=...=w(CY5). Actual numerical w(c) TBD; normalisation/nonnegativity, if used as probabilities, require declared semantics | Uniform 0.2 productive default, or differing year-vectors |
| **INV-12** | SEM/RUN | Investment decision x(y,k,stage) is common across CY; replicated x(y,k,c) requires equality links for all c; independent weather-specific dispatch is allowed | Free x(CY1)≠x(CY2) |
| **INV-13** | SEM | Objective counts investment term once outside CY expectation; operating quantities have transparent CY/Δt accounting | Multiply CAPEX by 5, or ENS MW as MWh |
| **INV-14** | STRUCT/SEM | TimeInterval = [startUTC,endUTC) with start<end and Δt consistent; overlap prohibited for same typed series key; coverage / leap / DST rules explicitly bound | Local DST hour duplicated as two UTC intervals |
| **INV-15** | SEM | All quantities have physical dimensions, canonical unit and aggregation operator; MW×h→MWh, not MW+MWh | Adding MW_e directly to MWh_H2 |
| **INV-16** | SEM/OWNER | Spatial/asset identity crosswalks use version, direction and factors. Aggregation of extensive quantities conserves total modulo documented loss; ratios are recomputed, not summed | Sum RES availability percentages |
| **INV-17** | SEM/RUN | Physical existing/reduced electric branches maintain DC-mesh/KCL/KVL semantics (with appropriate offset/PST/HVDC representation); one angle reference per connected island or equivalent cycle form | Treat all physical links as unconstrained controllable transfers |
| **INV-18** | SEM/RUN | Expansion candidates, irrespective of intended physical AC/DC technology, act as **controllable DC market links** with explicitly directional, possibly indirect NTC effects | Candidate given physical AC branch KVL by default |
| **INV-19** | SEM/OWNER | P05 cluster partition is total/disjoint and internally connected; P06 reduction has six required output families, 4 season×direction ratings per applicable link, detailed-grid quality hooks | Flow sums matched while PTDF/mesh broken |
| **INV-20** | SEM/RUN | Storage charge/discharge and state transitions respect energy/power dimensions and boundaries; state boundary policy remains owner-defined | SOC gain 1 MWh from 1 MW during 30 min |
| **INV-21** | SEM/OWNER | Electrical and H2 balances are carrier/basis-consistent; H2 network expansion exogenous; hydro and implicit/explicit DSR do not double count | Undeclared LHV↔HHV equivalence or DSR duplicated |
| **INV-22** | SEM | P10/P11 are distinct expansion decisions with explicit stage eligibility/carry-forward reconciliation; P12 storage-only expansion applies to 2040/2050 | Re-optimize S1 in S2 without recorded rule, or run S3 for 2035 |
| **INV-23** | SEM/RUN | LF expansion retains physical DC mesh while interzonal internal transfer ratings are not binding in the designated LF mode; an OPF-specific mode changes applicable limit set | Disabling impedances with LF limits |
| **INV-24** | SEM | P13 comparison preserves comparable baseline axes with/without LF portfolio; P14 sensitivity freezes **hourly** pre-expansion electrolyser load; P15 OPF is conditional and separately bounded by applicable LF portfolio | Freeze only annual H2 totals, or OPF x>LF cap |
| **INV-25** | SEM/OWNER | Raw ModelOutput is not a DerivedMetric; unapproved KPI/formula/discount/filter remains UNDEFINED_OWNER_TBD and cannot be published as approved | Reporting “system need” as authorized project |
| **INV-26** | STRUCT | Applicability is TRUE/FALSE/UNKNOWN; only a witnessed false conditional permits NOT_APPLICABLE; unknown mandatory applicability remains BLOCKED | P15 N/A without branch state evidence |
| **INV-27** | STRUCT | Test outcome enum is exactly PASS, FAIL, BLOCKED, UNSUPPORTED, NOT_EXECUTED, NOT_APPLICABLE; scope, oracle authority, source status and G1 each have independent fields | FAIL assigned solely because a test was never run |
| **INV-28** | SEM/RUN | PASS requires actual scoped execution, accepted oracle and immutable evidence; a synthetic arithmetic pass cannot certify a native energy model | Promote C01 synthetic case PASS to tool conformance |
| **INV-29** | SEM/RUN | Equivalence compares scientific constraints/observables under an explicit projection, feasible-set/objective/property consistency and adopted tolerances; multiple optima need not share identical x | Reject two feasible optimal portfolios solely because x differs |
| **INV-30** | OWNER | G1 stays BLOCKED; owner, data release, normative status, independent sign-off and productive conformance do not follow from graph closure | Set G1 GO after 48-row CSV validation |

## 1. Three-valued applicability and evidence

Proposed evaluation semantics:

~~~text
resolve(profile, required_axes, guard):
    if any relevant profile/source/guard dependency unresolved: UNKNOWN
    else evaluate guard as TRUE or FALSE with witness
test_status:
    if CONDITIONAL and guard == FALSE with proof: NOT_APPLICABLE
    else if required feature demonstrably unavailable: UNSUPPORTED
    else if mandatory oracle/release/authority absent: BLOCKED
    else if no scoped execution: NOT_EXECUTED
    else: PASS or FAIL based on accepted assertions and evidence
~~~

These are evaluation rules for future contracts, **not** claims that the 48 R04 tests have run. Current R04 baseline records all 48 native tool tests as **NOT_EXECUTED**. Evidence qualification, test outcome, review and G1 are orthogonal, not one cascading status.

## 2. Cross-cutting closure obligations

An implementation is rejected for semantic comparison if it loses: source authority/version; D2 common investment and shared **symbolic** CY weight profile; UTC/Δt and dimensions; branch vs market-link distinction; process-only R03 data; P10/P11 transfer and P15 conditionality; separate raw/derived need semantics; six R04 outcome labels with evidence scope. Later approved mathematical thresholds and numeric profiles are required for **productive** conclusions, not for the nonnormative concept graph.

## 3. Known intentionally open predicates

Not machine-resolvable today: MD-01 effective methodology; MD-02 costs, discount and timing; MD-03/-13/-15 physical-grid reduced-model oracles; MD-04/-17 output/KPI equivalence; MD-06 storage details; MD-07 stage carry-forward; MD-08 LF/OPF modes; MD-09 NTC mappings; MD-10 hydrogen basis; MD-11 source-qualified original data; MD-12 time conversion/tolerances; MD-14 topology; MD-16 hydro/DSR; MD-18/-19 upstream CY binding; MD-20 variant/scope; missing independent review. These predicates must remain explicit typed unknowns and cannot be filled by software defaults.