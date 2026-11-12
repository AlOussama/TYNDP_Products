# ML-C01 — Decision Semantics D1–D6

**Authority class:** CONFIRMED_PROJECT_DECISION_IN_NONNORMATIVE_RESEARCH_PROFILE; **not** an ENTSO-E method approval. **Basis:** ML-R00 PR #32 @ 9162def25d22c37b1fbc38f7d80fe929425cc8d2. **G1=BLOCKED.**

This ledger restates, rather than changes, the existing decisions. None of the 21 owner MD/CL is closed here. Original MA-01 statements and original R01–R04 artifacts remain unchanged.

## 1. Canonical decision ledger

| Decision ID | Confirmed meaning | Research consequences | Explicit limitations |
|---|---|---|---|
| **project_decision:D1** | MA-01 is the **sole active provisional** L2 requirements baseline: exactly 48 MA01-SR. | All M/LR/T/Data/VN links refer to the 48 IDs without modifying them. | No SR-012/SR-049, no implemented upstream weather selection; 50 MA01-MR are not 50 active SR. |
| **project_decision:D2** | Exactly five externally selected CY1–CY5 per y in 2035/2040/2050; identical **case-indexed vector across the three years**, numerical weights TBD. | w[2035,c]=w[2040,c]=w[2050,c]=w[c] for each c. | **Not** w[CY1]=…=w[CY5]. No 0.2 default, weather selection, adopted 5-case method claim or fabricated source manifest. |
| **project_decision:D3** | Fail-Closed for mandatory, applicable obligations. | No scoped/full PASS while required capability, oracle, data/source or test evidence is insufficient. Cause codes remain distinct. | Missing proof ≠ demonstrated scientific FAIL. Synthetic result ≠ productive approval; optional-disabled P15 alone is not a failure. |
| **project_decision:D4** | Canonical UTC time and dimensional/unit semantics. | Explicit source→UTC transforms, unique instants and interval durations; dimensionally sound MW/MWh, H2, price-year treatment. | DST/leap/missing-hour policy, interpolation/resampling, tolerance and source-calendar handling **MD-12 OPEN**. |
| **project_decision:D5-A1** | Risk-based mathematical verification. | Risk justifies different proposed D0–D4 test depths across mathematical V1–V6 axes; formal proof or 1:1 equation syntax not universally required. | R04 33 A/12 B/3 C = proposed allocation, not owner-approved acceptance; no automatic tool certification. |
| **project_decision:D6-A** | One shared, **tool-independent** scientific Requirements Contract with independent tool implementations. | Common meaning of inputs, preprocess, mathematical obligations, output/postprocess and evidence; each modelling tool constructs its own realization. | No mandatory model conversion M1→M2; no imposed solver, common data schema, specific DSL, GEMS/CESM/INES/mathspec, A/B/C architecture or runtime. |

**ID collision prevention:** project_decision:D4 denotes UTC/units; **test_depth:D4** denotes deep mathematical-equivalence checks. project_decision:D6-A is not R02 architecture A; project_decision:D5-A1 is not risk_tier:A.

## 2. Deliberate O26 versus D2 non-reconciliation

- **Source fact:** O26 = ENTSO-E *TYNDP 2026 Identification of System Needs Methodology*, *Version for Public Consultation*, **25 February 2026**, §3.7, describes **three** weather cases per study year and year-specific weighting. Authority = CONSULTATION_ONLY / ADOPTION_UNVERIFIED.
- **Project research profile:** D2 specifies five already selected **CY1–CY5** per study year and a case-wise shared symbolic vector. Authority = PROJECT_DECISION, **research scope only**, not formal revision of O26.
- **Conflict record:** O26_THREE_VERSUS_D2_FIVE; impact MA01-SR-010, -011, -027, -029, -040; MD-01/12/18/19/20 remain OPEN as applicable; no silent replacement of either source statement.
- **No numeric substitution:** A scientific probabilistic convention w[c] ≥ 0 and sum_c w[c]=1 may be used in analytical proposals, but the correct real values, source identities and numerical normalization tolerance remain TBD. An illustration of 0.2 per c is explicitly SYNTHETIC.

**Counterexample to “equal CY weights”:** [0.05, 0.10, 0.20, 0.25, 0.40] is a *synthetic* normalized nonuniform vector. If the same vector is used for 2035, 2040 and 2050 by CY identity, D2's cross-year equality is satisfied; the five weights are not equal to one another. Conversely vectors with equal *unordered* numbers but shifted identity assignments between years violate case-wise equality. Neither vector is an approved IoSN parameter.

**No additional selection scope:** MR-012 and MR-049 are upstream weather selection/reconstruction references only; original SR-012 and SR-049 are absent and must stay absent. Requirements for a source manifest, QA and externally supplied weights (SR-010/011/040) are **intake** obligations, not new selection algorithms.

## 3. Terminology harmonization without editing upstream text

| Upstream wording | ML-C01 interpretation | Disposition |
|---|---|---|
| R04 “D4 weather overlay” | Wrong project ID; intended project_decision:D2 | Record INT-02; preserve R04 text |
| R04 “equal weights” | Ambiguous unless scoped to **same case across years**; uniform-per-case examples only fixtures | Record INT-01; no production 1/5 |
| R04 “D4 deep equivalence” | test_depth:D4 | Preserve as a separate verification-depth namespace |
| R02 source/maturity states, R03 source/data states, R04 test PASS | Orthogonal status fields; not a single ordered APPROVED ladder | Record INT-03 |
| R03 “transformation” for P00/P10/P17 | Typed governance / model-operation / verification in addition to data transformations | Record INT-09 |
| R01/R02/R03/R04 “compliant” | Must qualify exact claim scope and axis (source, structure, mathematics, result, signoff) | Record INT-12/15 |

No automatic upstream fix or prior PR modification is authorized.

## 4. Decision → SR → verification impact

| Decision | Key affected requirement examples | Condition to be evaluated later |
|---|---|---|
| D1 | all 48 | Set identity equals original MA01 catalogue, reference integrity only |
| D2 | SR-010, 011, 027, 029, 040 | Actual manifest, five mapped CY identities, case-wise cross-year weights, correct common x[y,k], no weather selection |
| D3 | SR-017, 022, 024, 027, 029, 035, 047 and other applicable obligations | Missing or invalid mandatory proof prevents PASS; reason-specific status |
| D4 | SR-004, 007, 010, 011, 020, 027, 040, 042, 043, 044 | Unambiguous UTC and units; proper Δt and price/H2 basis; MD-12 still open |
| D5-A1 | SR-017–022, 024, 026–035, 041, 042, 047 | Proposed depth/risk and independent valid mathematical/physical oracles, not formula-string matching |
| D6-A | all 48; particularly SR-047 | Independently generated implementations and evidence; no cross-tool translation assumed |

## 5. Preserved pending decision set

Exactly **21** existing owner items remain open: **MD-01…MD-20 and MA02-CL-001**. Grouped consequences:
- MD-01/20: source authority, methodology scope/controlled change.
- MD-02/07/08/09: economics/discount, stages, LF/OPF and candidate-to-NTC semantics.
- MD-03/13/15: reduced-network reference, quality and numerical verification.
- MD-04/05/17: needs/ONDP/KPI, offshore factor, multiple-optimum/result policy.
- MD-06/10/16: storage, frozen H2, hydro/DSR.
- MD-11/12/18/19: real source-data releases, UTC calendar conventions, upstream five-case manifest and weights.
- MD-14, MA02-CL-001: 2035 start-grid eligibility.

A future owner closing event must carry a **new** real decision reference, dated issuer, changed scope, affected SR/M/transform/test links and evidence. A future adopted method version requires versioned clause delta and a **separate** controlled revision process, not retroactive rewriting.

## 6. Correctness tests and no-go examples

1. A research profile that labels O26's three-case definition “obsolete/overruled by ENTSO-E” solely based on D2 is **invalid**: D2 is a project research-profile override only.
2. If a test labelled project_decision:D4 asserts exactly five CY with uniform weights, **fail semantic naming/authority checks**; five CY is D2 and uniformity is not D2.
3. A model with x[y,c] freely varying across CY violates nonanticipativity even if solver status is OPTIMAL.
4. An OPF feature not selected, proven false, gives SR-026 NOT_APPLICABLE, but LF and P13 remain required and still need separate proof.
5. Structural PASS for all 48 crosswalk rows does not change G1, data release, source adoption or native conformance claims.

**End state:** D1–D6 semantically preserved, no owner or baseline changes, no normative release, **G1=BLOCKED**.

**Trace references:** [ML-R00 consistency review](../ML_R00_consolidation/cross_workstream_consistency_review.md), [R01 source assessment](../ML_R01_methodology/scientific_methodology_specification.md), [R04 status semantics](../ML_R04_verification/failure_and_evidence_semantics.md), [unchanged MA01 catalogue](../../iosn_requirements_catalogue.csv).
