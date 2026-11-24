# C1–C9 mapping and candidate generic operator signatures

## Semantic role allocation
| Generic role | CBA stress obligations | Keep general |
|---|---|---|
| C1 ContractFrame | purpose, boundary, time, scenarios, reference/project ids, method pins | Any study frame |
| C2 Referent | cases, project asset, scenario, model, data, owner, KPI role | Any named external study referent |
| C3 TypedRelation | counterfactual_pair, uses_source, project_delta, depends_on | Typed graph relation |
| C4 Predicate | same input, sampled projection, unit/guard, pairing, comparator | Typed composable predicate AST |
| C5 ScopedAssertion | required KPI/guard and conditional study obligations | No choice of LP variables |
| C6 ObservableDefinition | economic/cost proxy, climate and security indicators, time/price bases | Generic typed observable |
| C7 VariationPolicy | model formulation and method differentiation within source-approved bounds | Method freedoms vs obligations |
| C8 EvidenceRecord | request, actual validation artifact, model run and status | Evidence not equal to claimed result |
| C9 AuthorityRecord | regulatory source, method owner, provenance, decision | No promotion from documented to approved |

## Candidate expression typing / unresolved design
```text
sameExogenousSnapshot : CaseRef × CaseRef × DimensionScope -> Bool3
pairedDelta           : Observable[T] × CasePair[SAME_MODEL,SAME_SCENARIO] × SignRule -> Observable[T]
weightedAggregate     : Observable[T] × IndexSet × Weight[Role] -> Observable[Aggregate(T,Role)]
discountedValue       : Observable[CurrencyFlow] × TimeAxis × DiscountBasis -> Observable[PresentCurrency]
selectObservable      : ObservableSet[T] × SelectionPolicy -> Observable[T] | UNKNOWN
```
These signatures are **candidate semantic decompositions**, not accepted core grammar or executable operator implementation. In particular, `pairedDelta` could be a standard typed relation+subtraction composition; proof of necessity for primitive operator has **not** been established. Missing source or incompatible units must cause failure/blocker, not default.

## Modelling freedom and conformance
- Outer contract fixes reference/project semantics, KPI meaning, data/authority, admissible variation and required evidence.
- Inner battery/SOC, grid angle/PTDF, electrolyser part-load, UC, solver algorithm and model structure are not forced by this CBA role mapping.
- A role label `nodal_angle_dispatch` in the synthetic fixture is not a fully implemented grid model. Two status-preserving names are not E5 proof.
- Counterfactual variants can be compared even if internal feasible sets differ; then result spread is a subject of robustness, not a structural equivalence claim.
- No normative ENTSO-E method rules, discount rates, VOLL, dNTC or project boundary definitions were invented.
