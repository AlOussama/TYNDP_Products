# M2-MA2-PRE / W-EQ-SPEC — Global equivalent network, x/c0 and affine KVL

**Status:** PROPOSED_DESIGN_ONLY; **no MA2 production code**, no solver execution, no runtime/real-data approval. Version: M2.MA2.EQ.v0.1, 2026-11-12. Read with sibling files in this directory.

## 1. Source hierarchy and compatibility

- Governing task: [98](../98_M2_MA2_PRE_DOCUMENT_FIXTURE_MACRO_20261111.md); prior [MA2 handoff 85](../85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md), [five-review gate 93](../93_GOV_M2_FIVE_REVIEW_CONSOLIDATION_AND_GATES_20261111.md).
- Working scientific source: ENTSO-E *TYNDP 2026 Identification of System Needs Methodology*, **25 February 2026 consultation draft**, §3.8 and Annex 6.1. Authority remains **AUTHORITY_UNCONFIRMED** (R-METH SHA 754a79e11370dca2c25f1102d83ced5beb251522); the optimization solver, objective weights, gauge and affine KVL formulation below are **project I**, not an alleged ENTSO-E implementation.
- Implementation-reference SHA: MA1 0254d867a34b66ec7b56c90225605d29ea328916 / documentation 70e92ba9e62a320e58227ce9c2f03fad266f44bf. These contain **six open P1 findings** across R-PHY/R-CLU. Treat APIs as **provisional**, not an owner-selected canonical contract. R-API recommends option C (A canonical, selective typed B adapter); OWNER_PENDING.
- Real data not available as qualified payload (D-REAL SHA 6a8262f128ae3dd7e108afe2ade09028ea4f651f). In particular a **separately balanced** neutral dispatch is missing. MA2 G06 is NOT_RUN, not PASS.

## 2. Typed inputs and outputs (proposed versioned boundary)

| Type / interface | Required fields and invariant | Provisional MA1 source |
|---|---|---|
| MA2FrozenInputV1 | schema_version, run_id, actual checkout SHA, MA1 manifest/hash, grid, time, operational reference, neutral dispatch/reference, country labels/budget, ratings, protected policy, monitors, split manifest, source-byte hashes | A: execute_ma1 / MA1Result / export; wrapper is NEW DESIGN |
| DetailedGridSnapshot | ordered bus_ids, raw_country_ids, active ACBranch records and AC-island IDs, base_mva, lossless HVDCTerminals, provenance; no mutable caller-owned sequences | A contracts.py; PHY-R01/R02/R03/R04 repair gate outstanding |
| OperationalReference | ReferenceFlowCache(flow_mw [L,T], nodal_net_mw [N,T], branch_ids, bus_ids, snapshot_ids, input_sha256, neutral_calibration=False), validated against A_d; cached and immutable for **all candidates** | A physical.py, MA1Result.reference |
| NeutralCalibrationReference | separate ReferenceDispatchSet with explicit zero HVDC terminal schedule and zero PST schedule, independently physically balanced **per AC island**; matching ReferenceFlowCache(neutral_calibration=True), separate source/content hash | A reference_flows(grid, neutral_dispatch, time, neutral_calibration=True) is a provisional helper; **do not call it with the operational injections merely switched to neutral flags** |
| Country/zone | resolved_country_of_bus; CountryZoneBudget; frozen valid seed.zone_of_bus and protected_line_ids; full official input: 37 separate labels, 102 exact zones, NI and UK separate; synthetic fixture: SYNTHETIC_BUDGET only | A country.py and seed.py |
| CalibrationConfigV1 | x_ref_e, x lower/upper relative bounds, gauge definition by actual **reduced AC island**, weights, regularizers, optimizer settings, rank/conditioning limits, absolute+relative physical tolerances, source-model mode, deterministic seed | NEW DESIGN / project I, owner approval pending |
| MA2CandidateProjection | complete candidate busmap, P [Z,N], Gamma [E,L], A_z [Z,E], A_d [N,L], sorted named zonepairs, cut membership, AC-islands, operator hash and source linkage | A build_oriented_projection(grid, zone_of_bus) **recomputed for every candidate** |
| EquivalentFitResultV1 | positive x_pu [E], cycle-coordinate alpha [r], c0_mw [E], island gauge ledger, rank report, objective and residuals, source-provider semantics, convergence, train hash, candidate/operator hashes and status | NEW DESIGN; no claim of implemented API |

Strict ordering: the active branch order and bus order in both references must equal the original grid and candidate-projection order. Snapshot keys, the five externally supplied year IDs, durations and time/season metadata must be identical for reference, neutral calibration, splits and ratings. Do not infer byte-level source authenticity from a self-declared source_sha256. Freeze and verify original file bytes upstream. No country-specific MW slack.

## 3. Original projection: dimensions, orientation, conservation

Let N original AC buses, L original active AC branches, Z reduced zones and E aggregated **oriented unique zonepairs**. A_d is N×L with +1 at the source endpoint and -1 at sink. In the reduced graph A_z is Z×E in the same convention. P is Z×N country-pure assignment, Gamma is E×L signed original-cut summation. The existing MA1 operator contract is

\[
 A_z\Gamma=P A_d,\qquad
 p_z(t)=P p_d(t),\qquad f_{\mathrm{target}}(t)=\Gamma f_d(t).
\]

Here p_d includes **explicit HVDC terminal injections** in operational mode. HVDC is **not** an AC edge; PST and permitted transformer phase sources are associated with AC branches. For every snapshot and **every proposed map**, verify the exact sparse operator equality and

\[
 A_z f_{\mathrm{target}}(t)=p_z(t),\quad
 \sum_{i\in\mathcal I}p_{z,i}(t)=0
\]

for each *actual electrically connected reduced AC island* \(\mathcal I\). Intercountry ties remain active; country boundaries never define extra electrical islands or power slacks. Recompute P/Gamma/A_z, zonepairs, all target flows and all regional monitor operators even for a small local move. Never carry zonepair positions across different candidate maps as identities.

## 4. Source-free affine reduced DC model

For a reduced graph, B(x)=diag(S_base/x_e) in MW/rad, x_e>0 p.u., L(x)=A_z B(x) A_z^T. Reference angle in each **true AC island** is fixed to zero for numerical uniqueness (not an MW slack). C is a full-column-rank sparse cycle basis of ker(A_z): A_z C=0; cycle dimension per connected island \(r_i=E_i-Z_i+1\). Choose \(c_0=C\alpha\) in **MW**, so A_z c0=0 structurally and not just approximately.

The *actual operational reduced solver* for a source-free/neutral reduced network must solve

\[
 L(x)\theta=p_z,\qquad
 f_z=B(x)A_z^{\mathsf T}\theta+c_0.
\]

Equivalent simultaneous constraints are

\[
 A_z f_z=p_z,\qquad A_zc_0=0,\qquad
 C^{\mathsf T}\operatorname{diag}(x)(f_z-c_0)=0.
\]

The last equality is the **affine KVL**, not homogeneous KVL on the entire f_z. Testing the extra c0 after a conventional DC powerflow but ignoring it in the **model contract/output** is prohibited. The returned solver must expose theta, f_z, c0 and independent KCL/KVL residuals. Using a sparse direct factorization of each AC-island reduced Laplacian is acceptable; forming a dense inverse for Europe is prohibited.

**Important limitation:** KCL and the affine homogeneous form above describe \(\phi=0\). The A-input can include fixed transformer phase_shift_rad even while PST is neutral. Those known source terms cannot silently be treated as zero. For a *known, validated* reduced phase-source vector \(\phi(t)\) (radians), the general physics is

\[
 f_z=B(x)(A_z^{\mathsf T}\theta-\phi(t))+c_0,\quad
 L(x)\theta=p_z+A_z B(x)\phi(t),
\]
\[
 C^{\mathsf T}\!\left[\frac{\operatorname{diag}(x)}{S_{\mathrm{base}}}(f_z-c_0)+\phi(t)\right]=0.
\]

Define \(q_\phi(x,t)=B A_z^{\mathsf T}L^\dagger A_zB\phi-B\phi\) with one angle reference per island: A_z q_phi=0 and \(f_z=H(x)p_z+c_0+q_\phi\). The pseudo-inverse symbol denotes the *mathematical mapping*, **not permission to compute a dense pseudo-inverse**. The source-free affine KVL must hold on \(f_z-q_\phi\). PST operational schedules may be evaluated only when a separately validated ReducedDeviceSourceProvider can represent all original phase effects on that candidate map. If provider absent/unrepresentable, status **DEVICE_SOURCE_UNQUALIFIED** and no operational RMSE acceptance. Do not fold time-varying PST responses into a time-invariant c0. Fixed phase offsets must likewise be represented or excluded with a documented fail-closed gate.

## 5. Parameterization, identifiability and gauge

- Parameterize \(u_e=\log(x_e/x_{\rm ref,e})\). All x_ref are positive, source-labeled, frozen before the split; bounds on u are finite. One **scale gauge for each meshed AC island**: \(\sum_{e\in E_i}w_e u_e=0\), with fixed positive w_e summing to one. Scale is unidentifiable from DC **flows alone**, because x→k x leaves H(x) unchanged. The gauge is mathematical, not evidence of absolute physical x; external angle witness would be required for absolute x.
- Compute cycle topology once per candidate and a sparse null-space/cycle coordinate system. Parameter count after gauge: \(\sum_i(E_i-1+r_i)\) for meshed islands (assuming one gauge/island and one alpha/cycle). **Do not count fixed x on a tree as identified**: r=0 and H independent of every x, regardless of regularization or numerical bounds.
- For source-qualified training conditions compute the **unregularized, gauge-restricted** data Jacobian \(J_{\rm data}=\partial\operatorname{vec}(f_z)/\partial(u_{\rm free},\alpha)\). Require full effective column rank, adequate smallest nonzero singular value / conditioning, and sufficiently diverse independent dispatch. If no loops, insufficient excitation, unqualified phase source or rank cannot be certified: **UNIDENTIFIABLE** or **RANK_UNDETERMINED**, no synthetic G06 PASS. A regularized numerical minimum must not conceal a rank defect.
- Per-island checks must not become per-country independent fits: the reduced graph is global (block-separated only by actual AC islands). Isolated one-zone islands have no branch reactance; classify NO_X_PARAMETERS and exclude from a numeric x claim, with an explicit scope flag.
- When a map causes a formerly meshed island to become a tree, a joint x/c0 calibration is NOT_QUALIFIED; do not invent tree x. A distinct future FLOW_ONLY mode could return KCL-fixed flows but must not pass G06.

## 6. Proposed global calibration objective (project I, not official)

On **TRAIN only**, for candidate map z, neutral snapshots t and validated known source model, let

\[
 \widehat f_t(x,\alpha)=
 B(x)(A_z^{\mathsf T}\theta_t-\phi_t)+C\alpha,\quad
 L(x)\theta_t=p_{z,t}+A_zB(x)\phi_t.
\]

Fit *all AC islands jointly under a single run identity*:

\[
\min_{u,\alpha}\;
 \sum_{t\in\mathrm{TRAIN}}\sum_{e=1}^E
   w_{e,t}\big(\widehat f_{e,t}-\Gamma_zf^{\mathrm{neutral}}_{d,e,t}\big)^2
 +\lambda_u\|R_u u\|_2^2+\lambda_\alpha\|R_\alpha\alpha\|_2^2
\]

subject to the gauge, bounds and physical/source admissibility. Weights must be nonnegative, nonzero for every admitted training feature, normalized independently of topology in a documented manner, and based on **TRAIN or fixed source metadata only**. \(\lambda\), x_ref, bounds, rank tolerance, solver choice, tolerance and optimizer starting points are **PROPOSED_OWNER_I**: an oracle can set lambda=0 and x_ref to analytic reference; no published ENTSO-E objective weights are claimed. If unregularized rank fails, regularization cannot upgrade the status. Target recomputation must use original detailed reference arrays and the *current* Gamma, never averaged prior candidate targets.

Recommended algorithmic profile for future implementation: log-x bounded trust-region nonlinear least squares with analytic/JVP sensitivity, sparse factor solves, structured c0 cycle coordinates and deterministic multi-start only when explicitly budgeted. Perform a separate **independent** small-graph dense cycle-space solve as regression oracle. Profile execution/memory in streaming time blocks; factorization may be cached **within one candidate/iteration only**, not reused as authoritative final fit from an earlier busmap.

## 7. Normative fail-closed algorithm shape (pseudocode, NOT executable production code)

~~~text
fit_global_equivalent(frozen, candidate, config):
    verify_original_byte_hashes_and_contracts(frozen)   # abort on mismatch
    assert source_SHA/time_SHA/split_SHA match frozen run
    validate_country_quota_connectedness_protected(candidate)
    projection = build_oriented_projection(original_grid, candidate)
    projection.verify(original_operational_reference)
    projection.verify(separate_neutral_reference)
    assert A_z @ Gamma == P @ A_d
    for mode in (operational, neutral):
        target[mode] = Gamma @ original_reference[mode].flow_mw
        injection[mode] = P @ original_reference[mode].nodal_net_mw
        assert island_balance and A_z @ target[mode] == injection[mode]
    build_global_reduced_island_graph_and_sparse_cycle_basis()
    require_phase_source_provider_for_each_requested_mode()
    require_meshed_identifiable_islands_and_unregularized_rank_on_TRAIN()
    optimize_all_islands_x_and_cycle_alpha_against_TRAIN_neutral_only()
    if optimizer_failure or bound_or_rank_failure: FAIL_CLOSED
    for t in TRAIN:
        replay_through_ACTUAL_affine_reduced_solver(x,c0,phase[t],p_z[t])
        check KCL, A_z*c0, generalized_affine_KVL and numeric residuals
    recompute unregularized_sensitivity_rank_at_final_solution()
    return candidate-tagged complete result and source/split/operator hashes
~~~

Do not call Selection during fitting or use Holdout for rank, weights, tuning, early stopping, trial metrics or logging raw values. Operational validation (if source-qualified) is a distinct replay; the default device-neutral fit cannot be silently advertised as an operational prediction.

## 8. Gate G06 and result/witness schema

**Mandatory diagnostics** in EquivalentFitResultV1: candidate_sha256; original_source_manifest_sha256; operational_reference_sha256; neutral_reference_sha256; exact train_snapshot_sha256; reduced_island_bus/edge counts; r_i; gauge definition and measured residual; positive x vector (ordered zonepairs); alpha/c0 vector and norm(A_z c0)_inf; source mode/PST/HVDC treatment; x scales relative to x_ref; effective unregularized Jacobian rank and condition; iteration/solver failure mode; objective before/after, fit residuals in MW, sparse method/environment and stage timestamps; independent replay payload; release flags false.

**Statuses:** PASS_SYNTHETIC_DESIGN_TEST (future independent run only), UNIDENTIFIABLE, RANK_UNDETERMINED, INVALID_SOURCE, INVALID_SPLIT, INVALID_BUSMAP, DEVICE_SOURCE_UNQUALIFIED, NUMERICAL_FAIL, G06_FAIL, BLOCKED_DATA. Documentation alone remains NOT_RUN. Tolerances must be finite and safely bounded; a caller-selected infinity or huge physical tolerance must not disable KCL checks (PHY-R04).

**Gate:** G06 requires physical evidence of x>0, documented gauge, unregularized data rank, cycle-space c0, KCL, **affine** KVL in the *actual reduced solver*, numerical convergence, independent small-graph parity, and separated neutral/operational source semantics. R-NUM, MA1 repairs and Owner-API decisions remain separate mandatory gates for MA2 implementation/release.
