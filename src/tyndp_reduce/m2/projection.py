"""Sparse oriented AC cut operators, including physical cross-border branches.

P maps detailed *net* (base plus HVDC terminal) injections to zones.
Gamma maps AC branch flows to oriented zone-pair sums, not HVDC transfers.
A_z Gamma = P A_d holds identically with AC islands present.
"""
from dataclasses import dataclass

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

from .contracts import ContractError
from .country import assert_country_zones


@dataclass(frozen=True)
class OrientedProjection:
    P: csr_matrix
    Gamma: csr_matrix
    A_z: csr_matrix
    zone_pairs: tuple[tuple[int, int], ...]
    busmap: tuple[int, ...]
    grouped_branch_ids: tuple[tuple[str, ...], ...]

    def verify(self, physical, cache, atol=1e-7):
        residual = (self.A_z @ self.Gamma-self.P @ physical.incidence).tocsr()
        if residual.nnz and np.max(np.abs(residual.data)) > 1e-12:
            raise ContractError("G05: A_z Gamma != P A_d")
        data = cache.payload()
        p = np.asarray(data["p_net_MW"], dtype=float)
        f = np.asarray(data["ac_flows_MW"], dtype=float)
        pz = self.P @ p
        cut = self.Gamma @ f
        if not np.allclose(self.A_z @ cut, pz, rtol=0, atol=atol):
            raise ContractError("G05: aggregated KCL failed")
        # Explicitly verify each AC island; country borders are not islands.
        for island in physical.islands:
            if not np.allclose(p[np.asarray(island), :].sum(axis=0), 0., rtol=0, atol=atol):
                raise ContractError("G03: AC-island KCL failed")
        return pz, cut

    def counterflow_diagnostic(self, flow_cache, tolerance=0.5):
        """I diagnostic: cancellation from opposite-oriented physical ties."""
        flows = np.asarray(flow_cache.payload()["ac_flows_MW"], dtype=float)
        result = []
        for e, pair in enumerate(self.zone_pairs):
            row = self.Gamma.getrow(e)
            signed = row.data[:, None] * flows[row.indices, :]
            denom = np.abs(signed).sum(axis=0)
            summed = signed.sum(axis=0)
            ratio = np.divide(np.abs(summed), denom, out=np.ones_like(denom),
                              where=denom > 1e-12)
            cancellation = 1.-ratio
            result.append({"zone_pair": pair,
                           "physical_branches": self.grouped_branch_ids[e],
                           "max_cancellation_ratio": float(np.max(cancellation)),
                           "opposing_parallel_flows": bool(np.any(cancellation > tolerance))})
        return result


def build_oriented_projection(physical, budget, busmap, protected=()):
    grid = physical.grid
    assert_country_zones(grid, budget, busmap, protected)
    z = np.asarray(busmap, dtype=int)
    Z, n, m = max(z)+1, len(z), len(grid.branches)
    P = coo_matrix((np.ones(n), (z, np.arange(n))), shape=(Z, n)).tocsr()
    pairs = tuple(sorted({tuple(sorted((int(z[u]), int(z[v]))))
                          for u, v in zip(physical.bus0, physical.bus1) if z[u] != z[v]}))
    pair_id = {pair: i for i, pair in enumerate(pairs)}
    rows, cols, signs, grouped = [], [], [], [[] for _ in pairs]
    for k, (u, v) in enumerate(zip(physical.bus0, physical.bus1)):
        zu, zv = int(z[u]), int(z[v])
        if zu != zv:
            j = pair_id[tuple(sorted((zu, zv)))]
            rows.append(j); cols.append(k)
            signs.append(1. if zu < zv else -1.)
            grouped[j].append(grid.branches[k].name)
    Gamma = coo_matrix((signs, (rows, cols)), shape=(len(pairs), m)).tocsr()
    azrows = [u for u, _ in pairs] + [v for _, v in pairs]
    azcols = list(range(len(pairs))) * 2
    azdata = [1.] * len(pairs) + [-1.] * len(pairs)
    Az = coo_matrix((azdata, (azrows, azcols)), shape=(Z, len(pairs))).tocsr()
    proj = OrientedProjection(P, Gamma, Az, pairs, tuple(busmap),
                              tuple(tuple(names) for names in grouped))
    if (proj.A_z@proj.Gamma-proj.P@physical.incidence).nnz:
        raise ContractError("G05: sparse incidence identity violated")
    return proj
