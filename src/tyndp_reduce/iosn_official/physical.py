"""Sparse, full-graph, island-balanced lossless AC-DC reference flow.

T: A f = p_base + p_HVDC, f_l = (S_base/x_l)(theta_0-theta_1-phi_l)
I: Every AC island has a fixed numerical slack *angle*, never hidden MW slack.
HVDC transfer >0 means export at bus0 (-MW) and import at bus1 (+MW).
Only passive AC branches enter A and the Kirchhoff Laplacian; an HVDC bridge
does not make two synchronous AC components into a single AC island.
"""
from __future__ import annotations
from hashlib import sha256
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import splu

from .contracts import (
    DataContractError, RejectedComponent, DetailedGridSnapshot,
    ReferenceDispatchSet, TimeSet, ReferenceFlowCache,
)


def ac_topology(grid: DetailedGridSnapshot):
    """Return signed incidence, susceptance [MW/rad], AC-island IDs.

    No dense inverse, dense PTDF, or dense rank computation is performed.
    """
    buses = {name: i for i, name in enumerate(grid.bus_ids)}
    branches = grid.active_branches
    starts = np.array([buses[b.bus0] for b in branches], dtype=int)
    ends = np.array([buses[b.bus1] for b in branches], dtype=int)
    l, n = len(branches), len(buses)
    incidence = coo_matrix((
        np.r_[np.ones(l), -np.ones(l)],
        (np.r_[starts, ends], np.tile(np.arange(l), 2))
    ), shape=(n, l)).tocsr()
    positive = incidence.copy()
    positive.data = np.abs(positive.data)
    adjacency = positive @ positive.T
    count, labels = connected_components(adjacency, directed=False)
    b_mw = grid.base_mva / np.array([branch.x_pu for branch in branches], dtype=float)
    return incidence, b_mw, labels, count


def reference_flows(
    grid: DetailedGridSnapshot,
    dispatch: ReferenceDispatchSet,
    time: TimeSet,
    *,
    neutral_calibration: bool = False,
    atol_mw: float = 1e-7,
) -> ReferenceFlowCache:
    """Solve all snapshots on the *entire* European reference AC graph.

    PST neutral mode suppresses only PST phase schedule; HVDC is held at 0 MW.
    Never implicitly redispatch/balance a deficient AC island.
    """
    if grid.unsupported_components:
        raise RejectedComponent("REJECTED_COMPONENT: " + ", ".join(grid.unsupported_components))
    if grid.incomplete_110kv_ties:
        raise DataContractError("BLOCKED_DATA: incomplete AC 110-kV tie representation")
    if dispatch.bus_ids != grid.bus_ids or dispatch.snapshot_ids != time.snapshot_ids:
        raise DataContractError("Dispatch/grid/time IDs or chronology mismatch")
    hvdc_ids = {x.identifier for x in grid.hvdc}
    pst_ids = {x.identifier for x in grid.active_branches if x.kind == "pst"}
    if set(dispatch.hvdc_transfer_mw) != hvdc_ids:
        raise DataContractError("HVDC terminal schedules missing or unexpected")
    if set(dispatch.pst_phase_rad) != pst_ids:
        raise DataContractError("PST operation schedules missing or unexpected")
    incidence, b, island_ids, n_islands = ac_topology(grid)
    branches = grid.active_branches
    t_count = len(time.snapshot_ids)
    injections = dispatch.injections_mw.copy()
    injections.flags.writeable = True
    buspos = {name: i for i, name in enumerate(grid.bus_ids)}
    if not neutral_calibration:
        for link in grid.hvdc:
            transfer = dispatch.hvdc_transfer_mw[link.identifier]
            injections[buspos[link.bus0]] -= transfer
            injections[buspos[link.bus1]] += transfer

    phase = np.zeros((len(branches), t_count), dtype=float)
    for j, branch in enumerate(branches):
        if branch.kind == "pst" and not neutral_calibration:
            phase[j] = dispatch.pst_phase_rad[branch.identifier]
        elif branch.kind != "pst":
            phase[j] = branch.phase_shift_rad

    laplacian = (incidence @ diags(b) @ incidence.T).tocsc()
    bias = -b[:, None] * phase
    rhs = injections - incidence @ bias
    theta = np.zeros_like(injections)
    for island in range(n_islands):
        members = np.flatnonzero(island_ids == island)
        imbalance = np.sum(injections[members], axis=0)
        if not np.all(np.abs(imbalance) <= atol_mw):
            raise DataContractError(
                f"BLOCKED_DATA: AC island {island} unbalanced after HVDC actions; "
                f"max MW={float(np.max(np.abs(imbalance))):.9g}"
            )
        if len(members) == 1:
            continue
        keep = members[1:]              # per-island angle reference, never MW slack
        try:
            lu = splu(laplacian[keep, :][:, keep])
            theta[keep] = lu.solve(rhs[keep])
        except RuntimeError as exc:
            raise DataContractError(f"AC island {island}: sparse solve failed") from exc

    flows = b[:, None] * (incidence.T @ theta - phase)
    kcl_residual = incidence @ flows - injections
    if kcl_residual.size and np.max(np.abs(kcl_residual)) > atol_mw:
        raise DataContractError("Physical reference solve failed AC-island Kirchhoff test")
    if not np.all(np.isfinite(flows)):
        raise DataContractError("Nonfinite solved reference flow")

    fingerprint = sha256()
    for part in (grid.fingerprint(), time.provenance.source_sha256,
                 dispatch.provenance.source_sha256, str(time.snapshot_ids),
                 str(time.weather_year_ids), str(time.year_for_snapshot),
                 str(time.season), str(tuple(time.duration_hours)),
                 str(bool(neutral_calibration))):
        fingerprint.update(part.encode("utf-8"))
    fingerprint.update(dispatch.injections_mw.tobytes())
    for name, values in sorted(dispatch.hvdc_transfer_mw.items()):
        fingerprint.update(name.encode("utf-8"))
        fingerprint.update(values.tobytes())
    for name, values in sorted(dispatch.pst_phase_rad.items()):
        fingerprint.update(name.encode("utf-8"))
        fingerprint.update(values.tobytes())

    return ReferenceFlowCache(
        tuple(branch.identifier for branch in branches),
        grid.bus_ids, time.snapshot_ids, flows, injections,
        tuple(map(int, island_ids)), fingerprint.hexdigest(),
        neutral_calibration,
    )
