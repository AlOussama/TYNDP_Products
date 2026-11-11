"""Sparse zonal P/Gamma/A_z: the complete original AC graph remains intact.

T: A_z Gamma = P A_d, f_cut = Gamma f_detail, p_z = P p_detail,
and A_z f_cut = p_z. HVDC terminal injections are included in p_detail
after the physical solve, but HVDC is never inserted as an AC branch.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix


class ProjectionError(ValueError):
    pass


@dataclass(frozen=True)
class OrientedProjection:
    P: csr_matrix
    Gamma: csr_matrix
    A_z: csr_matrix
    A_d: csr_matrix
    zone_ids: tuple[str, ...]
    cut_pairs: tuple[tuple[str, str], ...]
    branch_ids: tuple[str, ...]
    bus_ids: tuple[str, ...]
    zone_of_bus: tuple[str, ...]

    def verify(self, flow_cache=None, atol_mw=1e-7):
        discrepancy = (self.A_z @ self.Gamma - self.P @ self.A_d).tocsr()
        discrepancy.eliminate_zeros()
        if discrepancy.nnz and np.max(np.abs(discrepancy.data)) > 1e-12:
            raise ProjectionError("A_z Gamma != P A_d")
        if flow_cache is not None:
            if (self.branch_ids != flow_cache.branch_ids or
                    self.bus_ids != flow_cache.bus_ids):
                raise ProjectionError("Frozen reference ordering incompatible with projection")
            f = flow_cache.flow_mw
            p = flow_cache.nodal_net_mw
            if np.max(np.abs(self.A_d @ f - p)) > atol_mw:
                raise ProjectionError("Detailed AC nodal KCL violation")
            if np.max(np.abs(self.A_z @ (self.Gamma @ f) - (self.P @ p))) > atol_mw:
                raise ProjectionError("Zonal KCL violation after physical cut projection")
        return True

    def aggregate(self, flow_cache):
        self.verify(flow_cache)
        return self.P @ flow_cache.nodal_net_mw, self.Gamma @ flow_cache.flow_mw

    def counterflow_ledger(self, flow_cache, tolerance_mw=1e-9) -> tuple[dict, ...]:
        """Diagnose opposing *oriented* parallel currents per zone-pair/hour.

        Cancellation can hide stressed individual branches. This is not a
        substitute for a thermal/N-1 gate or time-weighted screening.
        """
        self.verify(flow_cache)
        events = []
        for row, pair in enumerate(self.cut_pairs):
            entries = self.Gamma.getrow(row)
            if entries.nnz < 2:
                continue
            contribution = entries.data[:, None] * flow_cache.flow_mw[entries.indices]
            pos = np.sum(np.maximum(contribution, 0.), axis=0)
            neg = np.sum(np.maximum(-contribution, 0.), axis=0)
            for t in np.flatnonzero((pos > tolerance_mw) & (neg > tolerance_mw)):
                events.append({
                    "zone_pair": pair, "snapshot": flow_cache.snapshot_ids[t],
                    "positive_MW": float(pos[t]), "negative_MW": float(neg[t]),
                    "net_MW": float(pos[t] - neg[t]),
                    "cancelled_absolute_MW": float(2 * min(pos[t], neg[t])),
                })
        return tuple(events)


def build_oriented_projection(grid, zone_of_bus) -> OrientedProjection:
    if len(zone_of_bus) != len(grid.bus_ids) or any(not z for z in zone_of_bus):
        raise ProjectionError("Complete, nonempty busmap required")
    zone_of_bus = tuple(zone_of_bus)
    zones = tuple(sorted(set(zone_of_bus)))
    lookup = {zone: i for i, zone in enumerate(zones)}
    z = np.array([lookup[q] for q in zone_of_bus], dtype=int)
    buspos = {bus: i for i, bus in enumerate(grid.bus_ids)}
    branches = grid.active_branches
    n, l, nz = len(grid.bus_ids), len(branches), len(zones)
    u = np.array([buspos[b.bus0] for b in branches], dtype=int)
    v = np.array([buspos[b.bus1] for b in branches], dtype=int)
    ad = coo_matrix((np.r_[np.ones(l), -np.ones(l)],
                     (np.r_[u, v], np.tile(np.arange(l), 2))),
                    shape=(n, l)).tocsr()
    p = coo_matrix((np.ones(n), (z, np.arange(n))), shape=(nz, n)).tocsr()
    pairs = tuple(sorted({tuple(sorted((int(z[i]), int(z[j]))))
                          for i, j in zip(u, v) if z[i] != z[j]}))
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    g_rows, g_cols, g_data = [], [], []
    for j, (start, end) in enumerate(zip(u, v)):
        a, b = int(z[start]), int(z[end])
        if a == b:
            continue
        pair = tuple(sorted((a, b)))
        g_rows.append(pair_index[pair])
        g_cols.append(j)
        g_data.append(1. if a < b else -1.)
    gamma = coo_matrix((g_data, (g_rows, g_cols)),
                       shape=(len(pairs), l)).tocsr()
    e = len(pairs)
    az = coo_matrix(
        (np.r_[np.ones(e), -np.ones(e)],
         (np.r_[[a for a, _ in pairs], [b for _, b in pairs]],
          np.tile(np.arange(e), 2))),
        shape=(nz, e)
    ).tocsr()
    result = OrientedProjection(
        p, gamma, az, ad, zones,
        tuple((zones[a], zones[b]) for a, b in pairs),
        tuple(branch.identifier for branch in branches),
        grid.bus_ids, zone_of_bus
    )
    result.verify()
    return result
