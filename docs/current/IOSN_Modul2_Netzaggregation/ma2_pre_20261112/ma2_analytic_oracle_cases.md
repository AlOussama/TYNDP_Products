# M2-MA2-PRE / W-TEST-SPEC — Independent analytic fixtures and numerical oracles

**Status:** DESIGN-ONLY oracle definitions, v0.1 (2026-11-12). Numbers below are **synthetic exact mathematical expectations** independently evaluated for design; they are **not results of a MA2 implementation**. All buses/years are MOCK and do not represent real grid data or ENTSO-E scenario selection.

## 0. Independent oracle construction (not the intended production solver)

Use original orientation **A: +1 at bus0, −1 at bus1**, base S_base=100 MVA, flows MW, x p.u., phase sources radians. For each AC island, construct full-row-rank \(\widetilde A\) by dropping one KCL row (the drop has **no** MW slack), and independently build an integer oriented cycle basis C with A C=0. For p with zero island sum, solve the square direct system

\[
\begin{bmatrix}\widetilde A\\
 C^{\mathsf T}\operatorname{diag}(x)/S_{\rm base}
\end{bmatrix}f =
\begin{bmatrix}
 \widetilde p\\
 C^{\mathsf T}\operatorname{diag}(x)c_0/S_{\rm base}-C^{\mathsf T}\phi
\end{bmatrix}.
\]

This is an **independent cycle/KCL linear-system oracle**; the future production design is a sparse angle Laplacian factorization. For small fixtures compute both dense direct system and sparse angle result; check all undropped KCL rows, cycle constraints, correct source sign, exact orientation and no hidden island slack. For prospective tests use project-I synthetic thresholds max abs KCL ≤1e−8 MW, max abs generalized-cycle residual ≤1e−10 rad, sparse/dense flow difference ≤1e−8 MW; these are **proposal values**, not official TSO tolerances or a bypass for unsafe input tolerances.

## EQ-01 — Three-bus triangle, no structural correction

Directed original/reduced edges e12:1→2, e23:2→3, e31:3→1. Let \(x=(1,2,3)\), \(\phi=(0,0,0)\), \(c_0=0\), and \(C=(1,1,1)^\mathsf T\). For injection \(p=(+6,-6,0)\) MW, unique expected \(f=(5,-1,-1)\) MW. KCL:

- bus1: f12−f31=6
- bus2: f23−f12=−6
- bus3: f31−f23=0

Loop KVL: \(1(5)+2(-1)+3(-1)=0\) MW·pu. Fix \(\theta_1=0\) rad; expected \(\theta=(0,-0.05,-0.03)\) rad. Positive x and exact gauge \(x_{\rm ref}=x\) are a valid closed-form ground truth; an **independent fit** needs more than one excitation to identify *relative* reactances.

## EQ-02 — Triangle: jointly identifiable x ratios and a nonzero structural c0

Use same graph/x/C, \(c_0=(2,2,2)\) MW (A c0=0). Three TRAIN injections and their **exact** affine-solver outputs are:

| t | p bus1,bus2,bus3 (MW) | f12,f23,f31 (MW) |
|---|---|---|
| T1 | (6,−6,0) | (7,1,1) |
| T2 | (0,6,−6) | (0,6,0) |
| T3 | (6,0,−6) | (5,5,−1) |

Because p(T3)=p(T1)+p(T2) and the source-free H is linear, \(c_0=f(T1)+f(T2)-f(T3)=(2,2,2)\). Subtract c0: \(g(T1)=(5,-1,-1)\), \(g(T2)=(-2,4,-2)\), \(g(T3)=(3,3,-3)\); each satisfies \(C^\mathsf T\operatorname{diag}(x)g=0\). T1 **total** flow has \(C^\mathsf T\operatorname{diag}(x)f=12\ne0\), whereas the affine KVL residual is **exactly zero**. This is a counterexample to applying homogeneous KVL directly to corrected total flows or interpreting c0 as a harmless visualization offset.

The unregularized fit must recover \(x_1:x_2:x_3=1:2:3\), \(c_0=(2,2,2)\), with scale chosen by the **stated** gauge (e.g. log geometric mean relative to x_ref=(1,2,3) equals zero). For the numerical oracle set regularizers to 0; positive bounded x, rank of the gauge-restricted data sensitivity = 3 (two x ratios + one cycle alpha), tolerances declared. If scale is not pinned, x and \(7x\) produce identical flows, not sevenfold quality.

**Critical analytic check:** a postprocessor that solves the source-free Laplacian then adds an arbitrary cycle vector can match these flows, but **must also return an explicit validated affine network contract that consumes c0 and reproduces the flows under replay**. Without that operational c0 contract and independent KVL residual, classify POSTPROCESS_ONLY_FAIL.

## EQ-03 — Four-node square with diagonal: two independent cycles

Nodes 1,2,3,4; directed edges in order (12,23,34,41,13). Let x=(1,1,1,1,2), p=(10,0,−10,0), phi=0 and independent oriented cycles

\[
 C_1=(1,1,1,1,0)^\mathsf T,\quad
 C_2=(1,1,0,0,-1)^\mathsf T.
\]

Choose alpha=(2,1) MW and hence \(c_0=2C_1+C_2=(3,3,2,2,-1)\) MW. Source-free current is

\[
 f-c_0=(10/3,10/3,-10/3,-10/3,10/3)\ \mathrm{MW}.
\]

Expected total \(f=(19/3,19/3,-4/3,-4/3,7/3)\) MW. All four nodal KCL rows yield p; \(A c_0=0\). The **incorrect** homogeneous loop residuals on f, before subtracting c0, are \(C_1^\mathsf T\operatorname{diag}(x)f=10\) and \(C_2^\mathsf T\operatorname{diag}(x)f=8\), respectively. After subtracting c0 both equal **0**. Require rank(C)=2 and independent sparse/dense equality; reject incorrect sign of edge 41 or diagonal 13.

## EQ-04 — Tree: x unidentifiable despite exact flows

Three-bus chain e12 (1→2), e23 (2→3), p=(8,0,−8) MW; exact \(f=(8,8)\) MW for **any** positive x: e.g. (1,3) **and** (5,7). Cycle dimension 0, c0 must be 0; no flow response contains x information. A solver may compute physically valid **flows**, but returning chosen x with a G06 qualified fit is a scientific error. Expected **UNIDENTIFIABLE** even with strong prior, bounds, regularization, a finite optimizer termination or negligible RMSE. An isolated single-node AC island has E=0 and status NO_X_PARAMETERS, not a fictitious fit.

## EQ-05 — Two meshed AC islands and independent gauges

Two disconnected 3-bus AC triangles A and B, with no HVDC tie required. A has xA=(1,2,3), pA=(6,−6,0), c0A=0 => \(f_A=(5,-1,-1)\) MW. B has xB=(2,3,5), pB=(10,−10,0), c0B=0 => \(f_B=(8,-2,-2)\) MW. Two distinct reference angles and **two independent scale gauges** are necessary: replacing xA by 2xA and xB by 7xB does not alter flows. No global power slack or single-Europe-angle solve; an imbalance of +1 MW in either island must be rejected even if the other island has −1 MW. Two block-local factorizations are valid inside **one global run**.

## EQ-06 — HVDC terminal action and separately balanced neutral source

Four buses (a1,a2) and (b1,b2) form **two distinct 2-node AC islands**, each with one AC line directed first→second. An HVDC link exports +5 MW from a2 to b1. For the *operational* base nodal injections **excluding HVDC** \(q=(15,-10,5,-10)\) MW, terminal actions are \((0,-5,+5,0)\), so effective p=(15,−15,10,−10) MW and AC flows \(f=(15,10)\) MW. Distinct AC-island balances are zero.

**Invalid neutral attempt:** switching HVDC transfer to zero but reusing q gives island sums **+5 and −5 MW** => must return BLOCKED_DATA / ISLAND_IMBALANCE; no hidden redispatch.

**Valid independent neutral dispatch:** provide a *different, separately sourced* \(q^0=(12,-12,8,-8)\) MW and explicitly HVDC=0 => p0=q0 and AC flows \(f^0=(12,8)\) MW. PST phase neutral (none present). Both trees here remain x-UNIDENTIFIABLE; this test certifies only dispatch/source semantics and island KCL, **not** an identified MA2 equivalent.

## EQ-07 — Operational PST circulation; source-free affine KVL cannot be applied blindly

Triangle EQ-01 with p=(0,0,0), x=(1,2,3), S_base=100, structural c0=(2,2,2) MW and a **known reduced** phase source \(\phi=(+0.06,0,0)\) radians in the e12 orientation. The phase-induced circulation is \(q_\phi=(-1,-1,-1)\) MW. Expected actual operational flow **f=(1,1,1) MW** (KCL zero). Independent generalized KVL:

\[
 C^\mathsf T \left[(x/100)\odot(f-c_0)+\phi\right]
 =(-6/100)+0.06=0\ {\rm rad}.
\]

With phi neutral, expected \(f=c_0=(2,2,2)\) MW; \(C^\mathsf T x(f-c_0)=0\) holds. The wrong operational homogeneous affine residual \(C^\mathsf T x(f-c_0)=-6\ne0\) correctly flags **source term missing**, not an x/c0 failure. The wrong homogeneous KVL on total f gives +6. Unknown PST/transformer phase mapping **must** produce DEVICE_SOURCE_UNQUALIFIED rather than fitting a time-varying c0. Also test reversal of the phase-source orientation/sign.

## EQ-08 — Insufficient excitation, improper gauge and numeric robustness

Same triangle EQ-02 but TRAIN contains only proportional injections p and 2p (plus the same c0), not two independently spanning nodal patterns. Data can determine c0 but cannot uniquely determine both independent x ratios: require **UNIDENTIFIABLE** based on *unregularized* gauge-restricted rank. Also verify scale invariance x→7x before gauge, and post-gauge same x ratio recovery under different positive absolute x_ref choices. Inject near-zero loop excitation/ill-conditioned Jacobian, very large/small x, NaN, nonfinite/huge atol, singular Laplacian, invalid fixed phase and empty TRAIN; all fail closed with clear reason. No optimizer-success-only PASS.

## IT-01 — Three electrically coupled countries with accepted and rejected swaps

Use synthetic A, B, C topology and quotas defined in [iteration spec §8](ma2_iteration_spec.md): four buses per country, square + protected diagonal 1-3, two country-pure connected zones/country; cross-country AC ties a2-b1, b2-c1, c2-a1. Candidate A+B exchange 2↔4 within each touched country; A+B+C three-country bundle is separately admissible. Run the **real** global-fit call path on each *eligible* candidate (or in a **unit test explicitly mocked and asserted**); frozen operational and neutral source SHA, five synthetic-year snapshot identities, train/select/holdout SHA must remain bitwise identical. No Country slack and no filter to touched countries.

An independently defined **test-double selection score oracle**, consistent with invariant country injections p_country=(−4,+2,+2) MW, uses fixed original-country-interface monitors oriented A→B, B→C, C→A:

| State | fixed selection monitor prediction MW | fixed target MW | primary J_SEL, MW | expected |
|---|---|---|---|---|
| Baseline | (6,8,10) | (2,4,6) | 4 | incumbent |
| 2-country swap A+B | (3,5,7) | (2,4,6) | 1 | **ACCEPT** |
| 3-country swap A+B+C | (5,7,9) | (2,4,6) | 3 | **REJECT_NO_IMPROVEMENT / ROLLBACK** |

Each vector satisfies country KCL: A flow_AB−flow_CA=−4; B flow_BC−flow_AB=+2; C flow_CA−flow_BC=+2. Strict improvement threshold proposed <1 MW yields decisions as shown. These are **predeclared mock evaluator outputs**, **not** claimed sparse-equivalent model-calibrated flows; test checks search/ledger/rollback and global-refit invocation independently of the analytic EQ-01…08 power-flow tests. Never report them as a physical MA2 calibration result.

Negative: country boundary violation, nonconnected swap and internalization of protected diagonal (1-3) => PRE_FIT_REJECT, global-fit call count = 0. Different zonepair count E between valid candidates must mark raw link-RMSE NOT_COMPARABLE; the **same three fixed intercountry monitors** retain identical target, shape, signed orientation, weights and selection snapshots, hence J_SEL remains comparable in this small interface toy. A candidate that drops one mandatory monitor => REJECT_UNCOMPARABLE rather than lower denominator.

## IT-02 — Freeze/holdout/TOCTOU/exception negatives

- Reorder/duplicate/remove one snapshot, alter the externally supplied year ID or duration, leak one HOLDOUT snapshot into TRAIN/SELECTION, change ratings/protection/source bytes, reorder original AC branch identities without a new manifest, or present mismatched source/checkouts: INVALID_SPLIT / INVALID_SOURCE and zero accepted candidates.
- Cause deterministic solver exception, rank failure or invalid c0 on one candidate **after** an accepted incumbent exists: preserve the entire previous incumbent map, x, c0, reference hashes and selection score bit-for-bit; append exception ledger + ROLLBACK reason. Never return a partially fitted candidate.
- Test caller-owned mutation of lists/arrays after a frozen contract construction: either construction must reject, or immutable owned copies and input SHA must remain invariant. This replays MA1 PHY-R01; it **cannot pass release until the separate repair SHA is independently reviewed**.
- Test link-count changes and parallel physical corridor +32 MW and −30 MW giving net +2 MW and **cancelled absolute=60 MW**; an aggregated single-link net does not certify per-branch critical flows or N-1 safety. If a fixed original protected-branch monitor becomes unrepresentable, hard reject or report mandatory coverage failure; never invent its reconstructed MW.

## Implementation-ready fixture/test protocol (future authorized code only)

1. Store one **canonical source manifest** of all arrays, orientations, split masks and analytical outputs above; include exact byte SHA only after file bytes exist, never fabricate them here.
2. Independent reviewer computes dense KCL+cycle oracle from first principles, not by calling the production 'fit' or projector; compare with production sparse *angle* model on EQ-01…07 under identical units.
3. Compare optimized recovered **ratios** and c0, not absolute x before gauge; prove rank **from data-only sensitivity** at the solution, independent of regularizer.
4. Run IT-01 with injected evaluator and separately real fit-replay; log all accepted/rejected attempts, full refit call counts and SHA equality. Use all five externally provided year IDs unchanged in real mode, or visibly synthetic MOCK IDs in fixtures.
5. Produce immutable machine-readable test results, exact tested SHA, JUnit/CI URLs, residuals and separate independent R-NUM signature; until then every test here is **DESIGNED_NOT_EXECUTED**.

See [test matrix](ma2_test_and_gate_matrix.json) and [test_matrix.csv](test_matrix.csv) for IDs/expected statuses and [owner I decisions](owner_i_decisions.md) for unresolved numerical defaults.
