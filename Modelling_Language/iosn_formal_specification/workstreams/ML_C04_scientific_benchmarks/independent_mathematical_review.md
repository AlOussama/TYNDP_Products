# ML-C04 — Independent Mathematical Review (Adversarial Role)

**Review type:** separate adversarial mathematical reading and independently formulated JavaScript fixture cross-check of the authored artefacts, **within the same AI-assisted production session**. This is **not** an independent person/institution and is not an external expert attestation, owner sign-off, tool audit or certification. G1 BLOCKED.

## Review approach and cross-evidence
Review reference: ML-R00 cross_workstream_consistency_review.md (INT-01–INT-15), original ML-R01 M01–M18 and original ML-R04 R04-T catalogue. Coverage checked against ML-R00 integrated_requirement_traceability.csv at 9162def2. The **74** ML-C04 family→SR edges cover **48/48 existing active SR** by ID; **35 edges DIRECT_MICRO_INVARIANT** and **39 CONTEXT_OR_PARTIAL_NOT_FULL_COVERAGE**. This is *mapping reachability*, not 48 passing conformance tests. MA01-SR-012 and MA01-SR-049 were not recreated. Tests and results documented in benchmark_execution_and_limits.md.

## Findings and dispositions

|Review ID|Priority|Finding|Status / disposition|
|---|---|---|---|
|C04-REV-01|Critical|B05 draft LODF=.5 inconsistent with its own post-AB-outage oracle: base (60,30,30) implies post (0,60,60), not (0,90,90).|**CORRECTED AND RECHECKED:** LODF=(90−30)/60=1; failed first run EX-01 and passing rerun EX-02 both retained.|
|C04-REV-02|High|Disconnected-cluster witness must not use the same triangle graph that contains direct A1–B link.|**CORRECTED:** separate path connectivity_graph_arcs explicitly present; triangle remains for Cut/KCL and separate PTDF test.|
|C04-REV-03|Critical|D2 equal across study years vs equal across five CY is an easy false equivalence; 0.2 from R04 cannot become official input.|**MITIGATED IN SYNTHETIC SCOPE:** heterogenous w=(.10,.20,.30,.15,.25), equality only across Y; real weights MD-12/18/19 still blocked.|
|C04-REV-04|High|Low wrong objective with independently optimised x_c can misleadingly appear superior.|**CORRECTLY FLAGGED:** 6.75 vs 11.5 is evidence of nonanticipativity relaxation; generated-index proof required.|
|C04-REV-05|High|KCL-only transport equality does not imply physical DC mesh; new candidate market links must not be AC angle-coupled.|**PARTIAL VALIDATION:** synthetic triangle witness valid; no actual PST/no-load/PTDF real model.|
|C04-REV-06|Critical|Cluster cut conservation and PTDF/LODF toy checks do not certify network electrical equivalent.|**OPEN MD-03/13/15:** six classes / 4 rating axes only inventory-checked, no 102-zone grid, RMSE or owner oracle.|
|C04-REV-07|Critical|B06 fixed Stage1 carry-over is an unapproved assumption, not the only methodic possible option.|**CONDITIONAL ONLY:** counterexample documents non-equivalence with joint LP; Stage transition F_y and economic accounting MD-07/02 unresolved.|
|C04-REV-08|High|B07 SoC normalisation bijection applies only fixed E>0, not arbitrary endogenous E.|**LIMITED CORRECTLY:** fixed-E proof; no assertion of linearising endogenous E·s.|
|C04-REV-09|High|B08 frozen profile's annual energy equality can mask hourly mismatch.|**DETECTED:** [3,7] vs [6,6] with same synthetic energy. Actual upstream pre-expansion provenance missing.|
|C04-REV-10|High|Hydro five-class taxonomy and DSR asset no-double-use cannot be validated from scalar reservoir or energy-conserving shift alone.|**PARTIAL:** class list / identity metadata only; class-specific hydro/DSR rules MD-16 unresolved.|
|C04-REV-11|Critical|Equivalence claims must distinguish feasible projection, full optimum sets and observed KPI; identical outputs not enough.|**PROOFS AND COUNTEREXAMPLES PROVIDED:** E-FEAS/E-OPT/E-OBS scope explicit, owner choice of contract observation/degeneracy MD-17 open.|
|C04-REV-12|High|Python smoke-check was committed but not actually executed; a matching expected JSON isn't runtime evidence.|**TRANSPARENT:** EX-02 ran separate JS arithmetic/metadata predicates, not Python and not native tool. Runtime status of Python harness remains NOT_EXECUTED.|
|C04-REV-13|High|No productive tolerance may arise from internal floating-point comparator or arbitrary synthetic prices.|**CONTROLLED:** toy comparison constants explicitly nonproductive; MD-15 numerics and MD-02 prices remain open.|
|C04-REV-14|High|Optional OPF off cannot justify skipping always-mandatory LF physics; mandatory missing capability UNSUPPORTED.|**METAMODEL-LEVEL PASS LOCAL ONLY:** formal condition test B10/B14; no real tool-feature inventory.|
|C04-REV-15|High|74 trace links to 48 SR could be misread as complete behavioural coverage.|**QUALIFIED:** 35 direct micro-invariant edges, 39 contextual/partial, no native SR test passed.|
|C04-REV-16|Critical|Original O26 is consultation material, source authority and 21 MD/CL have not been accepted.|**UNCHANGED:** AUTHORITY_UNCONFIRMED, all gate dependencies deferred, G1 BLOCKED.|

## Independent mathematical cross-examination

1. **Falsifiability:** Every B01–B15 includes at least one concrete positive statement and a deliberately distinguishable negative signature; especially B01/B04/B06/B08/B11/B12 expose classes that scalar output equality hides.
2. **Proof scope:** B11 slack bijection, B04 DC cycle and B05 LODF are valid for *declared* idealised networks. None establishes all-input equivalence of real IoSN generators. B05 conservation-only detailed flow fixture is **not** claimed KVL-feasible with arbitrary homogeneous branch impedances.
3. **Completeness:** The 15 families are suitable for a future conformant-generator acceptance suite, but cannot determine MD-02 discount, MD-03 reduction, MD-04 KPI/filter, MD-07 transfer, MD-08 LF/OPF exception, MD-09 indirect NTC, MD-10 H2 freeze source, MD-12 time or MD-15 numerical tolerance.
4. **Genuine independence:** Separately written arithmetic checking offers useful error detection (as B05 showed), but is insufficient for D6-A's two independent energy-system implementations or a third-party audit.
5. **Syntactic code QA:** No Python execution or runtime/formatter QA of the committed Python file is claimed. It remains a reproducibility candidate to be run with a logged output and commit hash.

### Scientific disposition
**MICRO_BENCHMARK_RESEARCH_COMPLETE_WITH_LIMITATIONS** for the stated artificial fixtures, contingent on correct assumptions. **No CERTIFIED PASS**, no real model conformance, no verified official IoSN equations, no decision on DSL or architecture. **G1 BLOCKED**, keep Draft.
