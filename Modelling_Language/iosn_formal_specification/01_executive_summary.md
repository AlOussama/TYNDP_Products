# 01 — Executive summary

## Research decision frame
The question is whether a **single normative semantic interface** can replace repeated, tool-specific interpretation of IoSN methodology text. The interface must span data, preprocessing, mathematical model obligations, execution profiles, postprocessing and acceptance evidence without prescribing object classes or solver implementations beyond explicit methodological rules.

**Status of evidence:** [O26] is the public-consultation text of 25 February 2026; no later approved 2026 IoSN version has been verified. Results are **conditional** and cannot claim full 2026 regulatory conformity. Repository-based IoSN analyses are secondary interpretations, and the earlier A/A+/B/B+ work is not used to derive these requirements.

## Substantiated source observations
1. [O26 §§3.1.1, 3.10, pp.12–14, 30] sets out an investment-and-operation optimisation with cross-weather **non-anticipative investment choices**, separate planning years, a two-stage LP process and limited investment options. Some mathematics therefore belongs in **method constraints**, not merely optional implementation details.
2. [O26 §3.7, pp.18–20] fixes three weighted weather scenarios for each 2035, 2040 and 2050 horizon. [O26 Annex 6.3] describes a statistical selection procedure. Validating the declared selections is easier than reproducing every selection decision.
3. [O26 §§3.8–3.9, pp.21–30] distinguishes network reduction, expansion optimisation in LF mode and subsequent internal-grid-constraint studies. Combining these into one generic transmission formulation would change the prescribed workflow.
4. [O26 §§3.3, 3.6, pp.15, 18] requires electricity/hydrogen sector representation, while hydrogen-network investments are outside the expansion choices described there; hydrogen dispatch and electricity/hydrogen conversion interactions are in scope.
5. [O26 §5.1, pp.41–44] reports Plexos/Antares sanity checks on simplified examples; these are **not a certification of arbitrary multi-tool equivalence**.

## Preliminary feasibility
A composite specification is technically **feasible for deterministically formalizable obligations**: typed artifacts, periods, locations, scenario weights, required ports/balances, allowed investment classes, process states, auditable outputs and test oracles. Yet a machine-readable file cannot decide by itself which undefined source convention is binding, whether a reduced network is physically adequate, or whether an opaque tool has enforced an equation. These cases need a signed method decision and/or independent evidence.

**No language winner is declared as a fact.** The comparative study in 05–07 yields a conditional decision in 12: start with a small, versioned method/requirements/data/verification contract, maintain explicitly scoped mathematical obligation profiles where O26 prescribes formulation classes. Use existing standards selectively, assess SysML v2 and alternatives against cost and tool access, and only then choose how much bespoke DSL is warranted.

## Immediate demonstrator and its limits
The reproducible `poc/` validates the **already selected and weighted 2035 weather scenario manifest** from O26 §3.7. It tests a JSON Schema plus independent semantic invariants using two structurally different *example export adapters*. It does **not** run an actual PyPSA/Antares/Sienna solver or execute the PCA/k-means selection algorithm. The two adapters show interface-level independence only.

## Methodology gaps requiring adjudication
- Source release gate: replace O26 draft if an approved/updated text exists.
- Exact PCA preprocessing, tie-breaking, statistical inputs and reproducibility parameters for Annex 6.3.
- Quantitative/acceptable residual thresholds for reduced-grid physical consistency and model verification.
- Disambiguation of the broken cross-reference appearing in O26 §4.6.
- Exact output schema and acceptance thresholds for system-needs identification and use of supplementary OPF analysis.
- Evidence needed to demonstrate that tool-specific model configurations actually implement non-anticipativity, nodal balances, DC power flow and the two-stage LP procedure.

## Decision criterion
Adopt a normative IoSN contract only after (i) methodology version sign-off; (ii) resolution of normative ambiguities; (iii) trace coverage review; (iv) independently executed contract tests; and (v) at least two **real tool implementations** verified against the same signed method and evidence profile. See `12_architecture_decision.md`.
