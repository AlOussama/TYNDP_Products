# 11 — Independent critical review: five separate rounds

**Scope:** Independent design/source review, **not** independently commissioned external expert opinion. The earlier CBA review was read for background only; IoSN conclusions are driven by O26 and the derived SyRS. Source [O26] is a consultation document, not verified final. All unresolved issues remain explicit.

## R1 — Requirements completeness

**Findings:**
- **R1-F01 (critical):** O26 version authority unresolved; later 2026 final/adopted release not demonstrated. A complete signed SyRS cannot be claimed without source control.
- **R1-F02 (high):** O26 provides many explicit mathematical/method requirements (e.g. weighted investments, power balance, LF expansion), but some detail-level defaults and reporting rules are not made machine-executable.
- **R1-F03 (high):** Annex 6.3 representative weather algorithm and Annex 6.1 network reduction require parameter closure before independent reproducibility can be claimed. Published final weather IDs != reproducible selection method.
- **R1-F04 (medium):** §4.6 contains broken internal reference; requires erratum.
- **R1-F05 (high):** Full system-needs report KPI/aggregation specification not demonstrably complete; UC-03 remains illustrated, not a confirmed contract.

**Risks:** tools pass a syntactic schema while implementing different implicit planning assumptions. **Counterargument:** domain specialists may resolve ambiguities through existing operational procedures; **response:** such decisions must be signed and encoded/versioned in the contract, not left as undocumented tool defaults. **Corrections:** source release gate, MD-01–MD-07 issue register, requirement statuses, owner decision log. **Required evidence:** authoritative source and signed trace to SR-001–021.

## R2 — Formal semantics

**Findings:**
- **R2-F01 (high):** YAML/JSON serialization is not semantics; JSON Schema alone lacks cross-record algorithmic invariants, conservation and LP objective interpretation.
- **R2-F02 (high):** Non-anticipativity must mean **one common investment value for every weather scenario**, not simply the same investment key in three output files.
- **R2-F03 (high):** Hourly energy (MWh) vs instantaneous power (MW), positive flow signs, hydrogen input/output basis, time-step weights and objective probabilities require consistent domain definitions.
- **R2-F04 (high):** Zonal flow conservation does not imply an electrically valid reduced meshed network; network reduction reference cases must inspect impedance/PTDF and seasonal/directional restrictions.
- **R2-F05 (medium):** Different mathematical notation may be equivalent but require a specified relation, not an undocumented assumption of identical variable objects.

**Risks:** stable-looking common-mode errors; impossible independent KPI recomputation. **Counterargument:** domain ontology plus a good model schema may be sufficient for structural checks; **response:** structural checks are useful but cannot prove optimization constraints were enforced. **Corrections:** define canonical unit, sign, dimension, index, method-profile and result dictionary; explicit mathematical obligations for O26 §3.1.1. **Required evidence:** positive/negative physical microfixtures and algebraic model inspection.

## R3 — Tool independence

**Findings:**
- **R3-F01 (high):** UC-02 identifies plausible PyPSA/Antares-GEMS mappings, **not verified feature parity**. Antares-specific hydrogen coupling, stochastic investment and full O26 2-stage LP capabilities must be proven in selected pinned releases.
- **R3-F02 (high):** A common requirement system must not force `PyPSA.Link`, `GEMS.Unit` or a specific internal solver variable.
- **R3-F03 (high):** Although tool data structures may differ, mandatory O26 formulation classes (LP, DC flow, objective weighting, common investments) **cannot** be weakened into optional labels.
- **R3-F04 (medium):** One translator may hide component loss, apply mismatched time scales or silently change constraints; declared capability/coverage gates required.
- **R3-F05 (medium):** PoC's two exporters are *synthetic* and generated for this experiment, not externally independent software implementations.

**Risks:** false claim of actual tool interoperability; regulatory methodology drift. **Counterargument:** solver-specific strategies sometimes ensure efficiency; **response:** fine if their observable semantics and approved mathematical class are preserved. **Corrections:** capability matrix by tool+version+requirement, fail-closed mapping, conformance kit in native tools. **Required evidence:** two independently built real system models of a common signed UC-02 fixture and extracted residuals.

## R4 — Verification feasibility

**Findings:**
- **R4-F01 (high):** Structure validated ≠ semantic rule satisfied ≠ method implementation correct ≠ complete system accepted.
- **R4-F02 (high):** Static test can validate published weather tuples; it cannot validate Annex 6.3 PCA/k-means unless original data, preprocessing and stochastic controls are specified.
- **R4-F03 (high):** Different feasible optimizer solutions (degeneracy) can be correct even if candidate selections differ; acceptance should target approved objective/feasibility equivalence and only mandatory output rules.
- **R4-F04 (medium):** Numerical tolerance, solver feasibility status, evidence signing and opaque model introspection remain unapproved.
- **R4-F05 (medium):** Initial test report from `poc/` concerns only UC-01 output manifest, even when tests all pass.

**Risks:** inflated conformance claims and unjustified PASS labels. **Counterargument:** trusted framework APIs may expose standard model builders; **response:** use them, but verify generated system constraints or independent counterexamples. **Corrections:** evidence classes, conditional test-oracle status, explicit negative test cases. **Required evidence:** reference fixtures, generated LP inspection, independent KPI recomputation, signed report.

## R5 — Architectural alternatives

**Findings:**
- **R5-F01 (high):** L4 modular contract is a plausible pilot choice but could introduce dual sources of truth between SysML/ReqIF, LinkML, BPMN and mathematics; one canonical governed registry is essential.
- **R5-F02 (medium):** A custom full DSL would duplicate requirements, schema, orchestration and algorithm ecosystems; justify it only by demonstrated missing capabilities and total ownership cost.
- **R5-F03 (medium):** A SysML v2-first enterprise could implement one coherent model, reducing need for a separate contract DSL; usability and versioned interface still need proof.
- **R5-F04 (high):** Reusing GEMS/Mathspec as a universal IoSN language mixes LP algebra and method lifecycle; reusing CESM/INES alone lacks method constraints and acceptance.
- **R5-F05 (medium):** An IoSN-specific lightweight profile still counts as custom standardization and has maintenance costs; do not call it cost-free.

**Risks:** fragmented specifications and non-validated dependencies. **Counterargument:** modular standards enable best-of-breed validators with limited new syntax; **response:** only with a shared semantic registry, version pinning and conflict resolution. **Corrections:** evaluate L1/L2/L3 and L4 on the **same three source-derived UC fixtures**, measure coverage/effort/evidence before final ADR. **Required evidence:** cross-profile conflict-injection and user acceptance test.

## Review closure register
|ID|Severity|Blocking criterion|Current resolution|
|---|---|---|---|
|R1-F01|Critical|Approved or effective source confirmed|**OPEN**|
|R1-F03|High|Annex 6.3 and network reduction algorithms testable|**OPEN**|
|R1-F05|High|Authorized output KPI schema|**OPEN**|
|R2-F02|High|Real two-scenario investment model conformance|**OPEN**|
|R3-F01|High|Two actual tool adapters complete UC-02|**OPEN**|
|R4-F02|High|Full weather selection algorithm demonstrated|**OPEN**|
|R5-F01|High|One registry survives conflict-injection|**OPEN**|
|UC-01 manifest fixture tests|Low (bounded)|Published tuple validation in two synthetic formats|**PASSED LOCALLY: 11/11 expected outcomes**|

## Source correction discipline
The source classification O/D/X and issue IDs must accompany **every** published use case. No A+/B+ inheritance, no CBA use-case transfer and no generic robustness programme were introduced.

## Supplemental review findings after detailed clause inventory

- **R1-F06 — Critical source completeness correction:** initial P01–P12 high-level matrix underrepresented §3.4 starting grid, §3.5 offshore starting grid, §3.11 marine routing and §§4.3–4.5.3 hydro/DSR and market-link candidates. Corrected with `source_clause_coverage.csv` (34 rows), P01A/P01B/P04A/P08A/P08B/P09A/P11A, SR-022–036 and LRC-18–21. **Risk:** another missing clause could remain because this is still a desktop extraction. **Required evidence:** clause-level external audit against every page and owner signature; **status OPEN**.
- **R2-F06 — High mathematical domain ambiguity:** source §4.5.2 mandates a **controllable DC market-link** representation for investment candidates regardless of AC/DC physical construction, while source §3.1.1 mandates DC load-flow/Kirchhoff for the existing network. **Risk:** equivalent model compilers can inappropriately impose mesh/angle constraints on new market-link candidates. **Correction:** semantic types `existing_grid_electrical_branch` vs `investment_candidate_market_link`, plus VC-20; **status OPEN**.
- **R1-F07 — Medium final-value omissions clearly documented by source itself:** §3.11 says the exact sea-use factor will be set in the final document, while §4.5.1 says storage costs/details will be added to the final version. **Risk:** treating an illustrative value within the 10–15% band as already normative. **Correction:** method profile requires source version and explicit signed exact factor before a fully passing report; **status OPEN**.
- **R4-F06 — High source economics issue:** the literal broken link in §4.6 for the discount-rate block prevents reliable automatic generation of a complete economic normalization oracle. **Correction:** block all claims of complete economic model conformance until the discount definition is resolved; **status OPEN**.

The earlier conclusion that a small fixed-weather-manifest PoC is executable remains intact. The completeness claim is now **explicitly limited to a targeted 34-clause methodology inventory**, not a formally signed full enumeration of the 65-page source.
