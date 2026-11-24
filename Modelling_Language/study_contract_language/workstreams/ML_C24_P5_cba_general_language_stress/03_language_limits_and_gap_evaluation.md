# CBA language boundary assessment: evidence-based gap analysis

**Key result:** A general C1–C9 meaning representation is a plausible conceptual allocation of the relevant CBA contract responsibilities, but the currently executed P1 adapter and C21 validator do not support a complete typed CBA.

## Specific semantic gaps
1. **Counterfactual pairing must be a semantic relation**, not just similarly named datasets: `R/P` refer to one `(model,scenario)` scope and an authorised project delta. Mutations detect cross-model pairing, sample drift, missing paired runs and baseline contamination in the independent P5 oracle.
2. **Observables need typed expression trees:** `pairedDelta`, weighted aggregation, discounting, price conventions, multi-optimal selection, nonmonetized values and Double-counting rules. Existing C20 surface syntax design is richer than executable P1 operators.
3. **Time/scenario weights are distinct:** temporal integration, scenario sampling, weather weights, Monte Carlo outage occurrence, discount factors and information revelation cannot be reduced to one numeric `weight`. Temporal and universal quantifier semantics remain incomplete.
4. **A/G and capability contracts cannot be reduced to cost intervals**: CBA tests output comparison, but dedicated RC01–05 service/physical cases must still establish power/energy, mass, ports, laws and quantifier ordering.
5. **Authority is independent from documentation availability**: external ENTSO-E/EC/ACER source status, owner decision, immutable revision and evidence request/result must not collapse. An independently verified URL does not imply an approved method profile.
6. **KPI equivalence is not mathematical equivalence:** equal cost or objective values would not yield E4. Different plausible investment-sign results do not by themselves imply a violation either; E3/E5 require scope-specific evidence.
7. **Language-level normalization, semantic/audit roundtrip and native mappings are absent**: independently passing numerical/structural oracles cannot substitute for typed syntax→CSNF→validator experiments.

## Core vs profile – avoid premature language inflation
A candidate generic base already provides semantic families C1–C9: scope identity, referents, typed relations, predicates, guarded assertions, observables, variation, evidence and authority. Candidate CBA profile semantics may comprise:
- typed referent roles for `ReferenceCase`, `ProjectCase`, `ProjectIntervention`, `ScenarioSnapshot`, `Comparison`, `IndicatorDefinition`;
- relation signatures `counterfactual_pair`, `approved_intervention`, `uses_exogenous_snapshot`, `verified_by`;
- **candidate** operators `sameExogenousSnapshot`, `pairedDelta`, `weightedAggregate`, `discountedValue`, `selectObservable`, possibly built from simpler existing typed functions;
- source and owner metadata, scopes, guard/ref typed AST and observable projector compositional rules.

These are **requirements on expressive mechanisms**, not authorisation to create C10+ classes, mandatory optimising equations or a CBA-specific compiler. Before accepting any new operator, attempt composition in existing CSNF, SysML/KerML profiles, GEMS graph roles, mathspec AST/normalisation.

## Feature matrix
Generated versioned machine-readable baseline: `04_capability_gap_matrix.csv` with 28 capability requirements and both conceptual and executable evidence status.

| Requirement | Desired capability | CSNF roles | Current P1 support | Priority |
|---|---|---|---|---|
| CBA-L01 | Studienziel und Geltungsbereich | C1,C2 | FRAME_FRAGMENT | P0 |
| CBA-L02 | Referenz-/Projektfall und Rolle | C1,C2,C3 | NOT_TYPED | P0 |
| CBA-L03 | Projekt-Delta und weitere Projektabhängigkeiten | C2,C3,C5 | NOT_TYPED | P0 |
| CBA-L04 | Szenario-, Wetter- und Zieljahridentität | C1,C2 | PARTIAL_FRAME | P0 |
| CBA-L05 | Exogenitätsparität je (Modell,Szenario,R/P) | C3,C4,C5 | OPERATOR_MISSING | P0 |
| CBA-L06 | Zeitdauer, Kalender, Granularität | C1,C2,C4 | TIME_FRAGMENT_ONLY | P0 |
| CBA-L07 | Gewichtsrollen: Wetter, Szenario, Monte Carlo | C1,C4,C6 | OPERATOR_MISSING | P0 |
| CBA-L08 | Physikalische Energieträger, Ports, Vorzeichen | C2,C3,C4 | BASIC_PORT_TYPES_ONLY | P0 |
| CBA-L09 | Assume-/Guarantee- und Servicekontrakte | C4,C5 | QUANTIFIED_SEMANTICS_MISSING | P0 |
| CBA-L10 | Scope, Guards, Normativität | C4,C5,C9 | PARTIAL_GUARDS_ONLY | P0 |
| CBA-L11 | Getypte KPI-Projektoren und Selektion | C4,C6 | ARITHMETIC_PROJECTOR_MISSING | P0 |
| CBA-L12 | Preisjahr, Währung, physikalische Einheiten | C2,C6 | PARTIAL_QUANTITY_TYPES | P0 |
| CBA-L13 | Kostenproxy vs vollständiger SEW/CBA-B1 | C4,C5,C6,C9 | NO_SEW_OPERATOR | P0 |
| CBA-L14 | Getrennte nichtmonetarisierte Indikatoren | C6,C8 | NO_RESULT_STATUS_PROJECTION | P0 |
| CBA-L15 | Paarweise Delta-Auswertung je Modell/Szenario | C3,C4,C6 | DELTA_OPERATOR_MISSING | P0 |
| CBA-L16 | Szenarioaggregation / Barwert / Zeithorizont | C1,C4,C6 | WEIGHTED_DISCOUNT_AST_MISSING | P0 |
| CBA-L17 | Doppelerfassung, Komponenten-Ledger | C4,C5,C6 | NO_LEDGER_SEMANTICS | P1 |
| CBA-L18 | VariationPolicy ohne interne Gleichungspflicht | C5,C7 | PARTIAL_VARIATION | P0 |
| CBA-L19 | Multi-Model-Rollen und run/pair-Identitäten | C2,C3,C7,C8 | INDEPENDENCE_UNVERIFIED | P0 |
| CBA-L20 | E1–E5-Statusgrenzen und Vergleichsaussagen | C4,C5,C8,C9 | E4_NOT_IMPLEMENTED | P0 |
| CBA-L21 | Data lineage / Transformationsverlust | C3,C5,C8,C9 | NOT_IMPLEMENTED | P1 |
| CBA-L22 | Quellen/Owner/Version/Audit | C1,C8,C9 | PARTIAL_AUTHORITY | P0 |
| CBA-L23 | Ausgeführte Evidenz vs Request | C8,C9 | PARTIAL_STATUS_CHECK | P0 |
| CBA-L24 | Sensitivität, Unsicherheit, Klima-Anpassung | C1,C4,C6,C8 | NOT_IMPLEMENTED | P1 |
| CBA-L25 | Szenariobäume und Nichtantizipativität | C1,C4,C5 | FINITE_FRAGMENT_ONLY | P1 |
| CBA-L26 | Geltung für alternative Studientypen | C1-C9 | NOT_TESTED | P0 |
| CBA-L27 | Native Interoperabilität und Audit-Roundtrip | C1-C9 | NOT_EXECUTED | P0 |
| CBA-L28 | Minimalität und Autorenverständlichkeit | C1-C9 | NOT_EXECUTED | P1 |

No numerical percentage of full language expressiveness is inferred from this mapping.
