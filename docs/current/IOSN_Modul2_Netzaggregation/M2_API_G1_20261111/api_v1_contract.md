# M2.API.v1 / M2.MA2Input.v1 — exact typed contract design (DRAFT, not approved)

**Stand:** 2026-11-11 · **Canonical recommendation:** A = `tyndp_reduce.iosn_official`; optional B→A validation only after owner approval.  
**Status:** `PROPOSED` / `OWNER_PENDING` / `MA2_NOT_AUTHORIZED` · **Version:** `M2.API.v1-DRAFT-20261111`, `M2.MA2Input.v1-DRAFT-20261111`.  
**Unveränderliche Belege:** [A 70e92ba9](https://github.com/AlOussama/TYNDP_Products/tree/70e92ba9e62a320e58227ce9c2f03fad266f44bf/src/tyndp_reduce/iosn_official), [B 88374dd3](https://github.com/AlOussama/TYNDP_Products/tree/88374dd38792146ca55fa3fe2d4b35dac842c0b9/src/tyndp_reduce/m2), [Review 075c5090](https://github.com/AlOussama/TYNDP_Products/blob/075c50903b7d51ec19befb4a4b8db1322ae33b2a/docs/current/IOSN_Modul2_Netzaggregation/R_M2_API_INDEPENDENT_ARCHITECTURE_REVIEW_2026_11_11.md), [MA2 Handoff 85](https://github.com/AlOussama/TYNDP_Products/blob/70e92ba9e62a320e58227ce9c2f03fad266f44bf/docs/current/IOSN_Modul2_Netzaggregation/85_M2_MA2_COLD_START_HANDOFF_2026_11_04.md).

## 0. Normative Geltung und Nachweisklassen

- **A-ACTUAL** = exakt aus dem A-Quellstand gelesen; vorhandene Annotation allein ist **kein** Beweis für Laufzeit-Enforcement.
- **V1-MUST** = vorgeschlagene Vertragsverschärfung/Preflight vor MA2; bedarf Owner-Entscheidung und Implementierungs-/Re-Review-Gate, soweit derzeit nicht erfüllt. Vor Freigabe kein rückwirkend behaupteter Status.
- **MA2-INPUT** = neue, **noch nicht implementierte** Anforderungs-/Handoff-Hülle; keine Änderung an `execute_ma1` durch dieses Dokument.
- **OPTIONAL** = nur Zusatz-/QA-Funktion; kein Abhängigkeitszwang für den A-MA2-Pfad.

Original-Netz bleibt ein zusammenhängender *pan-europäisch modellierter AC-Graph* mit möglicherweise mehreren **physisch** getrennten AC-Inseln. Länder sind reine Clustereinschränkungen und **keine** elektrischen Slacks; HVDC ist signiertes Terminal-Power-Injection-Device, kein AC-Zweig. M0/CGMES, M1/PECD und die externe Auswahl der fünf Wetterjahr-IDs bleiben unverändert. IoSN 25.02.2026 ist Konsultationsbaseline; Originalsolver/-heuristik wird nicht als verfügbar behauptet.

## 1. Exakte A-API-Typen und Semantik

Die folgende **Interface-Declaration** spiegelt Feldnamen/Annotationen am geprüften A-Commit wider. Sie ist eine typisierte Vertragsskizze, **nicht** ausführbarer Code und keine Behauptung, dass die P1-Typprüfungen bereits implementiert sind. `N=len(grid.bus_ids)`, `L=len(grid.active_branches)`, `T=len(time.snapshot_ids)`, `Z=sum(k_c)`, `E=len(projection.cut_pairs)`. Float-Arrays: NumPy `float64`, endlich, C-kontiguierlich, intern defensiv kopiert, unveränderlich; sparse Matrizen: `scipy.sparse.csr_matrix` mit konsistenten sortierten IDs.

```python
from dataclasses import dataclass
from typing import Literal, Mapping
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix

# A: contracts.py
@dataclass(frozen=True)
class Provenance:
    dataset_id: str
    source_uri: str
    version: str
    source_sha256: str                # lowercase SHA-256, 64 hex
    synthetic: bool = False

@dataclass(frozen=True)
class ACBranch:
    identifier: str
    bus0: str                         # signed orientation: + at bus0
    bus1: str                         # signed orientation: - at bus1
    x_pu: float                       # positive, on grid.base_mva
    voltage_kv: float                 # positive nominal kV
    kind: Literal["line", "transformer", "pst"] = "line"
    in_service: bool = True
    phase_shift_rad: float = 0.0      # fixed non-PST phase
    screening_class_kv: float | None = None # 225, 400, 0, None

@dataclass(frozen=True)
class HVDCTerminals:
    identifier: str
    bus0: str
    bus1: str
    lossless: bool = True

@dataclass(frozen=True)
class DetailedGridSnapshot:
    bus_ids: tuple[str, ...]          # (N,), unique
    raw_country_ids: tuple[str, ...]  # (N,), same indexing
    ac_branches: tuple[ACBranch, ...]
    hvdc: tuple[HVDCTerminals, ...]
    base_mva: float
    provenance: Provenance
    unsupported_components: tuple[str, ...] = ()
    incomplete_110kv_ties: bool = False
    # active_branches: tuple[ACBranch,...] (property)
    # fingerprint() -> str

@dataclass(frozen=True)
class TimeSet:
    snapshot_ids: tuple[str, ...]      # T ISO-8601 UTC-aware timestamps, ordered
    year_for_snapshot: tuple[str, ...] # T, member of 5 frozen year IDs
    weather_year_ids: tuple[str, ...]  # exactly five unique external IDs
    duration_hours: np.ndarray        # (T,), >0, hour
    season: tuple[str, ...]           # T; "summer" or "winter"
    provenance: Provenance
    timezone: Literal["UTC"] = "UTC"

@dataclass(frozen=True)
class ReferenceDispatchSet:
    bus_ids: tuple[str, ...]          # identical grid.bus_ids
    snapshot_ids: tuple[str, ...]     # identical time.snapshot_ids
    injections_mw: np.ndarray        # (N,T), pre-HVDC base injections
    hvdc_transfer_mw: Mapping[str, np.ndarray] # link_id -> (T,)
    pst_phase_rad: Mapping[str, np.ndarray]    # active PST id -> (T,)
    provenance: Provenance

@dataclass(frozen=True)
class NormalContingencyRatings:
    snapshot_ids: tuple[str, ...]
    normal_mw: Mapping[str, np.ndarray]      # ALL active AC IDs -> (T,), >0
    contingency_mw: Mapping[str, np.ndarray] # ALL active AC IDs -> (T,), >0
    provenance: Provenance
    unit: Literal["MW"] = "MW"

# A: country.py
@dataclass(frozen=True)
class CountryZoneBudget:
    quotas: Mapping[str, int]         # country_label -> positive exact int
    official: bool
    source_sha256: str
    # synthetic(...) / load_official_country_budget(...)

# A: contracts.py
@dataclass(frozen=True)
class ReferenceFlowCache:
    branch_ids: tuple[str, ...]       # active AC order (L,)
    bus_ids: tuple[str, ...]          # N
    snapshot_ids: tuple[str, ...]     # T
    flow_mw: np.ndarray              # (L,T), + from bus0 to bus1
    nodal_net_mw: np.ndarray         # (N,T), includes HVDC terminal actions
    island_of_bus: tuple[int, ...]    # (N,), actual AC connected components
    input_sha256: str                 # 64-char SHA-256 provenance fingerprint
    neutral_calibration: bool        # operational False, neutral True
    # to_manifest() -> dict

# A: screen.py and seed.py
@dataclass(frozen=True)
class AnnualScreen:
    year_ids: tuple[str, ...]
    rows: tuple[dict, ...]            # year/line/class/overload-MWh/hours
    screened_line_ids: tuple[str, ...]

@dataclass(frozen=True)
class SeedResult:
    zone_of_bus: tuple[str, ...]      # (N,), country-specific stable labels
    quota_counts: dict[str, int]
    merge_ledger: tuple[dict, ...]
    protected_line_ids: tuple[str, ...]
    retained_cross_country_branch_ids: tuple[str, ...]

# A: operators.py
@dataclass(frozen=True)
class OrientedProjection:
    P: csr_matrix                     # (Z,N)
    Gamma: csr_matrix                 # (E,L)
    A_z: csr_matrix                   # (Z,E)
    A_d: csr_matrix                   # (N,L)
    zone_ids: tuple[str, ...]         # (Z,), sorted
    cut_pairs: tuple[tuple[str,str], ...] # (E,), ordered, unique
    branch_ids: tuple[str, ...]       # (L,), active-grid order
    bus_ids: tuple[str, ...]          # (N,)
    zone_of_bus: tuple[str, ...]      # (N,)
    # verify(flow_cache=None, atol_mw=1e-7) -> bool
    # aggregate(flow_cache) -> tuple[np.ndarray, np.ndarray]  # (Z,T),(E,T)

# A: ma1.py
@dataclass(frozen=True)
class MA1Result:
    preflight: PreflightLedger
    reference: ReferenceFlowCache
    screen: AnnualScreen
    seed: SeedResult
    projection: OrientedProjection
    resolved_country_of_bus: tuple[str, ...]
    input_manifest_sha256: str
    gate_statuses: dict[str, str]
    # export(output_directory: str|Path, *, code_commit: str) -> dict

def execute_ma1(
    grid: DetailedGridSnapshot,
    dispatch: ReferenceDispatchSet,
    time: TimeSet,
    ratings: NormalContingencyRatings,
    budget: CountryZoneBudget,
    explicit_country_map: dict[str, str],
    explicit_year_weights: dict[str, float],
    *,
    protected_line_ids=(),
) -> MA1Result: ...
```

`PreflightLedger` (A `preflight.py`) has fields `status: str`, `grid_sha256: str`, `source_provenance: dict`, `model_sizes: dict`, `ac_islands: list`, `country_ids: dict`, `component_status: dict`, `checks: dict`, `blockers: tuple[str,...]` and `require_pass()->None`. The incomplete annotation of the last `execute_ma1` keyword argument is **actual A**, not proposed v1 strictness.

### 1.1 V1-MUST validations (including open independent P1)

| Object | Typed/semantic requirement before MA2 admission | Original A state |
|---|---|---|
| `DetailedGridSnapshot` | unique bus/branch/HVDC IDs; all endpoints known; `base_mva>0`; positive finite `x_pu`; fixed phase finite; actual AC topology derived only from strictly boolean `in_service`; defensive tuple-ownership; explicit complete 110-kV tie evidence | Basic validation exists; **PHY-R01/R03 open** |
| `HVDCTerminals` | `type(lossless) is bool` AND `lossless is True` for v1; exact paired signed MW terminal balance; unrepresentable losses rejected | **PHY-R02 open** |
| Flags | `type(synthetic/incomplete_110kv_ties/in_service/lossless/official) is bool`; no truthy coercion | safety typing repair required |
| `TimeSet` | `T>0`; exactly five externally fixed distinct weather-year IDs, each represented; strictly ascending, unique absolute ISO-8601 UTC-aware timestamps; positive durations in **hours**, seasons provided, not inferred; no sorting/resampling in adapter | A strict axis implemented; **B not equivalent** |
| `ReferenceDispatchSet` | IDs exactly match grid/time; (N,T), all and only HVDC/PST schedules each (T); finite, immutable arrays; per-AC-island balanced **after terminal actions**, no MW slack | A implemented for shared subset; strict tolerance **PHY-R04 open** |
| `NormalContingencyRatings` | MW active-power proxies, explicitly converted and evidenced if source MVA/A; strictly positive finite (T) for **all active AC branches** and both normal/emergency maps; time aligned | A validation + preflight exists; source conversion witness still required |
| `CountryZoneBudget` | exact per-country `k_c`, each ≥1; **official iff exact 37 published names + 102 quotas**; Northern Ireland and United Kingdom separate; synthetic budgets conspicuously marked and never reclassified | A official dict exact; R-CLU source-page provenance P2 |
| `ReferenceFlowCache` | `branch_ids` equals active AC order; `flow_mw (L,T)`; `nodal_net_mw (N,T)`; no country slack; `A_d f=p` and island injection sums within independently bounded tolerance; operational vs neutral flag exact | A performs KCL but **PHY-R04**; output digest additionally required |
| `OrientedProjection` | complete busmap, country-pure, AC-connected; exact quota, protected active AC cut not internal; `A_z Γ=P A_d`; `A_z Γ f = P p`; stable oriented ZonePair schema | A checks; **R-CLU-001** seed false infeasibility |
| `AnnualScreen` | screened **AC lines** at 225/400 classes, absolute flow vs hourly normal MW limit and duration-weighted annual MWh, five years separately; 220/380 require **source-qualified** class mapping; nominal 225/400 cannot silently opt out via 0 | **R-CLU-002** real 400-kV class-zero bypass |
| `execute_ma1` | explicit nonempty *policy record* for protected IDs, sorted canonical immutable set, fixed I-rule from annual overload; exact five-year nonnegative finite declared weights; no one-shot generator fingerprint divergence | actual protected defaults empty; **R-CLU-003** iterable hash inconsistency |

### 1.2 Gerätesemantik und Upstream-Attestation

Supported MA2-v1 **lossless common subset**, not an AC grid model of arbitrary equipment:

- **AC line:** real positive `x_pu` on common `base_mva`, fixed branch orientation; only declared `in_service=True` enters `A_d`. Inactive elements retain identity/input fingerprint.
- **Transformer:** A supports already normalized equivalent `x_pu` and finite fixed `phase_shift_rad`. **No** native tap-ratio field. Any source non-unit tap, winding/base normalization or unknown regulation **requires independent upstream equivalent+source certificate or `UNSUPPORTED_SEMANTICS`**. B only models `tap_ratio=1`, and cannot preserve A's nonzero fixed phase.
- **PST:** separate operational `pst_phase_rad[branch_id][T]`; fixed `ACBranch.phase_shift_rad=0` for kind `pst`; neutral scenario suppresses PST operating angles. Explicit orientation and radians mandatory.
- **HVDC:** transfer `h(t)` exports `-h` from `bus0` and imports `+h` at `bus1`, with p0+p1=0; HVDC does not add any AC incidence column. B's general unequal terminal injections **cannot** be mapped into A without physics loss; rejected.
- **Other components** (storage constraints, shunts, 110-kV holes, unmodeled controls/losses) must be classified by verified equivalent or blocked. `G11=PARTIAL_LOSSLESS_DC_ONLY`; never call the current kernel generally device-qualified.
- **Observed measured/OPF AC branch flows** may be supplied in an independent quality witness with their own signed orientation, hour IDs and SHA; they are **not** substituted for the DC `ReferenceFlowCache` and do not need equal DC flows to within 1e-6 MW. Real-data discrepancy bounds need a separate method-gate.

## 2. Country, screening and protection policies (V1-MUST)

### 2.1 Country and zone identity

Upstream provides an injective, explicit `raw_country_id -> published_country_label` relation for A. Legitimate many-to-one **raw aliases** must first be converted by a provenance-preserving *upstream normalizer* with a reversible source-to-canonical ledger, not by disabling A's injective guard. Never combine `Northern Ireland` with `United Kingdom`. Country quotas are immutable over all MA2 candidates. A-generated zone IDs `Country::NNN` and ZonePairs `(min_label,max_label)`, with fixed orientation from first to second. A B-integer zone is never intrinsically the same A-zone.

### 2.2 Screening policy

Proposed policy identifier `SCREEN_AUDITED_225_400_v1`:
1. Source provides nominal kV, `kind` and an explicit screened/not-screened class (`225`/`400`/`0`) plus provenance. Genuine nominal 225/400 AC **lines** automatically screened. Other nominal 220/380 classes may map to 225/400 **only when source rule names original circuit and explains class equivalence**. Ambiguous line classes block intake.
2. Class 0 / out-of-scope bypass is **not self-authorizing**. A source-backed `exclusion_ledger` with branch ID, physical nominal kV, reason, source/TSO owner, date, source SHA and approved policy version must justify each exclusion. Unjustified class=0 on nominal 225/400 ⇒ `BLOCKED_POLICY` (R-CLU-002).
3. For each eligible line `l` and chosen year `y`: `E[l,y] = Σ(t in y) max(0, |f[l,t]| - normal_rating[l,t]) · duration_h[t]` [MWh]; time-aligned normal limits positive MW; seasonal and contingency values retained for later phases, not secretly used as normal limits. `weighted_edge_costs` needs explicit year-weight mapping, no hidden averaging.
4. Screens/weights are **seed diagnostics only**. Different valid greedy clusterings are not an MA2 quality proof. End-to-end objective is independently defined and monitored on fixed global reference hours.

### 2.3 Protected-line seed contract

Proposed `PROTECT_CRITICAL_UNION_v1`: derived from the five **separate** annual criticality tables according to a **declared** per-year threshold/criterion plus any independently justified protected branch IDs. The threshold and tie policy are project-owned I-decisions and **MUST NOT** be guessed from the consultation. Freeze sorted distinct protected active AC IDs; record selection reason, year/MWh, source SHA, policy ID, explicit year weights, exceptions and final protected-set SHA. For **each** candidate, a protected AC branch's endpoints MUST belong to distinct zones. `protected_line_ids=()` is allowed syntactically by existing A, but prohibited as an implicit policy at MA2 acceptance; an empty audited result is allowed only when policy was actually evaluated and justified. R-CLU-001 requires distinguishing `HEURISTIC_STUCK` from demonstrated `INFEASIBLE`; a greedy dead-end is never a proof of infeasibility.

## 3. Export ABI: exact A 15-artifact contract (A-ACTUAL)

A's `MA1Result.export(new_output_directory, code_commit=...)` writes **14 hashed outputs + one `manifest.json` = 15 files**. They are required as a single self-consistent input set. Byte SHA-256 hashes in `manifest.output_sha256` cover only the 14 payloads; the manifest itself is hashed separately by MA2 intake.

| Name | Format | Required content |
|---|---|---|
| `preflight_ledger.json` | UTF-8 JSON | preflight status/source provenance/grid hash, islands, blockers |
| `gate_ledger.json` | JSON | G01..G05, G11, blocked real/review states |
| `merge_ledger.json` | JSON | seed merge sequence |
| `counterflow_ledger.json` | JSON | opposite-oriented parallel flow diagnostics |
| `reference_flow_manifest.json` | JSON | input hash, ordered bus/branch/hour IDs, islands, operational flag, MW |
| `country_quotas.csv` | CSV | `country_label,zone_count` |
| `busmap.csv` | CSV | `bus_id,country_label,zone_id` |
| `annual_criticality.csv` | CSV | `year_id,line_id,screening_voltage_class_kv,nominal_voltage_kv,overload_MWh,overload_hours,observation_hours` |
| `zone_cuts.csv` | CSV | `zone0,zone1` |
| `global_reference_flows.npz` | NumPy compressed NPZ | `branch_ids,bus_ids,snapshot_ids,flow_mw,nodal_net_mw,island_of_bus` |
| `operator_P.npz` | SciPy sparse NPZ | `P` (Z,N) |
| `operator_Gamma.npz` | SciPy sparse NPZ | `Gamma` (E,L) |
| `operator_A_z.npz` | SciPy sparse NPZ | `A_z` (Z,E) |
| `operator_A_d.npz` | SciPy sparse NPZ | `A_d` (N,L) |
| `manifest.json` | JSON | `status,code_commit,input_manifest_sha256,reference_input_sha256,output_sha256,real_network_qualified=false,independent_reviewer_release=false,calibration_equivalent_x_c0=NOT_IN_MA1,source_versions,units` |

**Intake invariant:** require exactly the expected 15 artifact names (unknown additional files either rejected or separately namespaced), 14 SHA digests independently recomputed from raw files, separate manifest byte digest, no path traversal/symlink substitution, internal manifest IDs/shapes/order independently compared to CSV and NPZ, source-code SHA compared against Git checkout/tree (not mere caller-entered `code_commit`), and re-derived projection/KCL invariants. For datasets `source_sha256` is currently declared provenance; REAL admission requires rehashing actual source bytes and documenting owner/usage rights. This prevents conflating a source declaration with attested bytes.

**A-ACTUAL limitation R-API-P2-03:** A creates a new directory then writes files sequentially; the directory itself is **not an atomic transaction**. V1-MUST before release: staging + hashes + fsync as appropriate + atomic rename/READY marker or strict verified-directory quarantine. A partial directory is always `ARTIFACT_INCOMPLETE`, not accepted. This documentation does **not** implement that change.

## 4. Proposed MA2 admission envelope: `M2.MA2Input.v1` (MA2-INPUT)

This is a **new input manifest/validation layer**, **not** a new current A function signature. It refers to exactly one verified A `MA1Result`/15-file export and supplements properties absent from MA1. For clarity these are required typed fields; identity fields are SHA-256 lowercase ASCII hex.

```python
# Design-only structural typing for a future MA2 reader/validator:
from typing import TypedDict, Literal, Mapping
class SHASet(TypedDict):
    grid: str; dispatch_operational: str; dispatch_neutral: str
    time: str; normal_and_emergency_ratings: str
    country_budget: str; country_resolution: str
    protection_policy: str; screen_policy: str
    ma1_input_manifest: str; ma1_export_manifest: str

class FrozenSplit(TypedDict):
    train_snapshot_ids: tuple[str, ...]
    selection_snapshot_ids: tuple[str, ...]
    holdout_snapshot_ids: tuple[str, ...]
    split_manifest_sha256: str

class MA2InputV1(TypedDict):
    schema_id: Literal["M2.MA2Input.v1"]
    canonical_api: Literal["tyndp_reduce.iosn_official"]
    ma1_code_sha: str
    ma1_export_root: str
    ma1_manifest_sha256: str
    source_hashes: SHASet
    operational_reference: ReferenceFlowCache  # neutral_calibration=False
    neutral_reference: ReferenceFlowCache      # neutral_calibration=True
    grid: DetailedGridSnapshot
    time: TimeSet
    ratings: NormalContingencyRatings
    budget: CountryZoneBudget
    ma1_result: MA1Result
    baseline_projection: OrientedProjection
    protected_line_ids: tuple[str, ...]
    monitor_policy_sha256: str
    screening_policy_sha256: str
    split: FrozenSplit
    numeric_policy_sha256: str   # tolerances/gauge/bounds/solver/resource plan
    qualification: Literal["SYNTHETIC_ONLY", "REAL_GATE_PENDING"]
```

### 4.1 Freeze rules / independent neutral calibration

- `operational_reference` is immutable across **all** candidates (same source SHA, L×T values, bus and active-branch indices); `p_detail` is its `nodal_net_mw` and `f_detail` its `flow_mw`. Do not dispatch anew, swap years, or recompute per country.
- Independently supplied **neutral calibration** `ReferenceDispatchSet`, its provenance and `ReferenceFlowCache(neutral_calibration=True)` are separate and hash-bound. HVDC setpoints neutral, PST scheduled phase neutral; residual AC-island balances still **MUST** pass with no fictitious MW slack. Simply zeroing operational HVDC/PST without independent redispatch can break feasibility and must fail `NEUTRAL_DISPATCH_UNBALANCED`.
- Recompute neutral case with the same documented active grid and branch orientation; fixed non-PST transformer phase remains physically explicit, unlike scheduled PST angles. Preserve distinct operational and neutral digests.
- Source manifest includes real observed AC-flow oracle **separately** when available and a declared discrepancy metric; no B-style 1e-6-MW hard equality requirement for observed vs simplified DC physics.

### 4.2 G05 – per-candidate geometry and conservation

For every baseline and modified `zone_of_bus`, validate all N original bus memberships exactly once, hard per-country `k_c`, AC-connected zones, unchanged physical AC islands/active branches, NI/UK distinct, protected cuts retained. Recreate **from the original detailed grid** `P(z)`, `Γ(z)`, `A_z(z)`, `A_d`, and sorted zone-pair identity. Shapes `P:Z×N`, `Γ:E×L`, `A_z:Z×E`, `A_d:N×L`. Assert `A_z Γ=P A_d` exactly to declared sparse tolerance; `p_z=P p_detail`, `f_target=Γ f_detail` and `A_z f_target=p_z` to independent MW tolerances. All candidate-specific projection/target data must carry their **own hash**; moving boundaries does **not** preserve the old link list.

### 4.3 G06 – global positive x / structural affine c0

Calibrate over the **whole** reduced European AC graph, not one country. Physical reduced model:
- `x_e>0` finite and bounded, with a declared independent *gauge/scale convention* for each connected AC **reduced** island; ensure fitted parameters identifiable by rank/sensitivity/loop excitation, else `UNIDENTIFIABLE`.
- `f_eq(t) = H_eq(x) p_z(t) + c0`, with `A_z c0=0`; `c0` is a genuine implementable affine correction, not a post-hoc plotting offset.
- For the actual reduced simulator `Cᵀ diag(x) (f_eq(t)-c0)=0` with `C` an oriented cycle basis (and documented dimensions/angle units). If the simulator cannot represent this relation, `AFFINE_KVL_FAIL` even if RMSE looks good.
- Independently check rank/conditioning, KCL, KVL, gauge, reference replay, and sparse vs dense oracle on small cases. Trees/degenerate loops that do not identify x fail rather than returning fabricated values. Solver exception/negative x/nonfinite residual => `GATE_FAIL`.

### 4.4 G07 – coupled-country search and candidate isolation

Start from independently validated MA1 seed. Permit country-pure single-boundary moves, balanced swaps and coupled ≥2-country moves, **never** changing `k_c`. Apply all invariants before running optimizer; reject/ledger failures without modifying frozen references. For **every** admissible candidate: rebuild G05 *globally*, execute complete global W-EQ x/c0 fit, evaluate **only** on fixed SELECTION block, accept if its predefined comparable objective improves beyond frozen threshold, else rollback. Deterministic candidate ordering, fixed tie-break and seed, max iterations/plateau, bound checks and complete immutable ledger are required.

### 4.5 G08 – fairness and frozen monitors/splits

`train`, `selection` and `holdout` partition exactly the **existing fixed** time/snapshot IDs; no missing, duplicate, overlapping or unauthorized changed hours. TRAIN for fit, SELECTION for accept/reject, HOLDOUT sealed until final independent replay (never use holdout to tune). Freeze a monitor definition that is **independent of candidate-dependent ZonePair labels**: e.g. original named physical branch/corridor monitor sets plus policy-fixed country/border groups, with explicit coverage/weighting and projection-to-monitor map, alongside candidate-specific E count. Compute per-link MW-RMSE (only matched IDs), global comparable RMSE, MAE, P95/P99, critical capture and country/border fairness. Different E/cut sets cannot be compared by plain mean link-RMSE alone. Changing monitor/split SHA invalidates comparability, not a 'better' candidate.

### 4.6 Mandatory resource/numeric preflight

Before real-European runs freeze a **measured** sparse resource plan: N,L,Z,E,T, precision/dtype, upper-bound RSS, I/O bytes, disk, snapshot block size, streaming strategy and spill policy. Compute `L·T` and `N·T` storage, check both workflow peak and artifacts. Current A holds L×T and N×T and outputs a monolithic compressed NPZ; B additionally serializes JSON lists. The 500-/1001-bus synthetic sparse chains **do not** certify European RAM/IO scalability. Any missing plan, exceeded hard budget or insufficient sparse replay ⇒ `RESOURCE_BUDGET_FAIL`, not unbounded allocation.

## 5. Gate semantics / exceptions / provenance

**Existing A exceptions:** `DataContractError` / `RejectedComponent` (`contracts.py`), `CountryContractError` (`country.py`), `ScreeningError` (`screen.py`), `ProjectionError` (`operators.py`). **Proposed v1 ledger codes** must be mapped to those exceptions and never silently coerced:

| Code | Trigger / required behavior |
|---|---|
| `BLOCKED_DATA` | missing/invalid original bytes, IDs, time, units, topology, country map, normal/emergency limits or neutral dispatch; stop |
| `UNSUPPORTED_SEMANTICS` | non-unit tap without certified equivalent, unequal HVDC terminals, unproven fixed phase, unknown active component or unsupported controls; stop |
| `INVALID_TYPE_OR_SHAPE` | mutable caller-owned fields, nonboolean flags, nonfinite/nonpositive values, wrong N/L/T/E/Z dimensions; stop |
| `INVALID_TIME_AXIS` | timezone not UTC, duplicate, unsorted or externally altered five-year snapshots; stop |
| `BLOCKED_POLICY` | ambiguous 220/380 class, unjustified class=0, unknown screening/protection threshold or unaudited empty protect set; stop |
| `HEURISTIC_STUCK` | greedy cluster algorithm blocked without infeasibility proof; never label `INFEASIBLE` automatically |
| `INFEASIBLE` | independently demonstrated country/quota/cut topology impossibility with certificate; no silent quota relaxation |
| `INVALID_FINGERPRINT` | input/manifest/output byte mismatch, unauthorized code SHA or source mutation; stop |
| `ARTIFACT_INCOMPLETE` | any missing/partial/unvalidated output file or staged run; stop |
| `G05_FAIL` / `UNIDENTIFIABLE` / `AFFINE_KVL_FAIL` | candidate integrity, physical rank/gauge or structural affine KVL fails; reject candidate/run |
| `SPLIT_OR_MONITOR_CHANGED` | holdout leak / selection comparison changes; stop or reject candidate |
| `RESOURCE_BUDGET_FAIL` | estimated/measured resource cap exceeded; stop |
| `REVIEW_PENDING` / `AUTHORITY_UNCONFIRMED` / `REAL_BLOCKED` | code may be documented/tested; no synthetic-independent or real authorization claim |

**Fingerprint specification for a future frozen v1:** domain-separated SHA-256 over canonical UTF-8 JSON metadata (sorted keys, no NaN/Inf, explicit schema tag, exact ID order and units), plus byte SHA of each explicit NumPy array (canonical float64 little-endian, C order, shape/dtype in hash) and sparse CSR (`shape`, ordered `indptr/indices/data`), plus code commit/tree SHA and source-byte SHA. Do **not** hash mutable live references or rely only on named source SHA declarations. Freeze all input versions and actual object contents before computing one run/MA2 envelope digest. Any change creates a **new Run ID**. The present A `input_manifest_sha256`, reference input SHA and output hashes are **separate existing identities**, not interchangeable with this proposed stronger MA2 envelope hash.

## 6. Required vs optional implementation surface

| Surface | Requirement | Timing / condition |
|---|---|---|
| A `execute_ma1` / `MA1Result` / `ReferenceFlowCache` / `OrientedProjection` / 15 outputs | **MANDATORY** as the C/A MA2-Input ABI | MA2 v1 before any authorized implementation |
| Field type safety, KCL/balance finite tolerance, correct class/protection, feasible seed, exact IDs and fingerprints | **MANDATORY**; independent W-PHY/W-CLU repair and R-PHY/R-CLU re-review | before MA1 synthetic admission and MA2 code gate |
| Stable source, neutral dispatch, split/monitor/solver/resource policies, G05–G08 design | **MANDATORY** | before MA2 authorization / monitored runtime |
| Staged atomic export implementation | **DESIRED P2**, but strict full-directory post-read/hash quarantine is non-negotiable admission guard | no need to block *design* solely for optional export refactor; fix before durable production publication |
| B→A converter, B numerical parity/oracle and content-hash ideas, write-once helper, LU factor reuse | **OPTIONAL**, versioned, separately reviewed; cannot become mandatory MA2 path | separate future owner-approved adapter task |
| Lossy HVDC, non-unit taps, uncontrolled storage, general AC-OPF observed flows as model equality | **NOT SUPPORTED** by lossless v1; use `UNSUPPORTED_SEMANTICS` or separate extension gate | no silent fallback |
| M0/M1 readers, weather-year selection, MA3 N-1 four capacities | **OUT OF SCOPE** | separate modules/gates |

## 7. Versioning / breaking changes / review gate

1. **Draft is not v1 freeze.** Owner must explicitly accept A/B/C, semantics, screening and protection. Independent PHY/CLU re-review of the **same integrated repaired SHA**, no open P0/P1. R-API-P1-01..09 dispositioned; R-NUM remains separate for G06–G08.
2. After approval, record `api_schema="M2.API.v1"` and `ma2_input_schema="M2.MA2Input.v1"`, exact file schema, default/optional behavior, code SHA, canonical serialization+hash policy in an immutable manifest. Until then use `-DRAFT` identifiers and reject claims of `FROZEN`.
3. **Patch change:** behavior preserving stricter validation without schema shape/meaning change, with negative tests and review; **minor**: optional, feature-flagged fields that cannot change physics/output digest when absent; **major**: positional signature, timezone, sign, unit, branch/zone orientation, Device capability, screening/protection defaults, geometry semantics, export files/dtype or fingerprint algorithm. A major change creates `v2` and dual-reader migration/replay, not silent overwrite.
4. Fail closed on schema major unknown, source SHA mismatch, enum unknown, unsupported version or past candidate hash reuse. No unapproved conversion between B and A.
5. **Release state machine:** `DOCUMENTED_DRAFT` → `OWNER_ACCEPTED` (not runtime) → `MA1_SYNTHETIC_QUALIFIED` (independent repaired replay) → `MA2_G05_08_SYNTHETIC_TESTED` + `R_NUM_ACCEPTED` (separate runtime decision) → `REAL_QUALIFIED` only after source/authority/G12. None is implied by this document.

**Controlling gates:** [M2-API-G1 Handoff 95](https://github.com/AlOussama/TYNDP_Products/blob/27dfd810b39e17e6b616a2b0aeb813eb8948d8a0/docs/current/IOSN_Modul2_Netzaggregation/95_M2_API_G1_OWNER_CONTRACT_GATE_20261111.md), [R-PHY](https://github.com/AlOussama/TYNDP_Products/blob/c004e5330df2a018e567c8ef955ef2fc9d71e0ea/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_PHY_INDEPENDENT_REVIEW_2026_11_11.md), [R-CLU](https://github.com/AlOussama/TYNDP_Products/blob/7d7d07d7af5966ddc26d0be1100a69013763d2e8/docs/current/IOSN_Modul2_Netzaggregation/87_R_M2_MA1_CLU_INDEPENDENT_REVIEW_20261111.md).
