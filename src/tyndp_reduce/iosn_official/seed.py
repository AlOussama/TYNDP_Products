"""Deterministic country-quota AC graph contraction (documented I-01).

Never runs separate country PTDFs; countries constrain only feasible
contractions. All original cross-country physical branches remain in the
source network and in oriented P/Gamma/Az aggregation.
"""
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappush, heappop
import math
from typing import Mapping

from .country import (
    CountryZoneBudget, CountryContractError, validate_country_feasibility,
    validate_busmap,
)


@dataclass(frozen=True)
class SeedResult:
    zone_of_bus: tuple[str, ...]
    quota_counts: dict[str, int]
    merge_ledger: tuple[dict, ...]
    protected_line_ids: tuple[str, ...]
    retained_cross_country_branch_ids: tuple[str, ...]

    def as_busmap(self, grid) -> dict[str, str]:
        return dict(zip(grid.bus_ids, self.zone_of_bus))


def quota_seed(
    grid, resolved_labels: tuple[str, ...], budget: CountryZoneBudget,
    *, merge_cost_by_branch: Mapping[str, float] | None,
    protected_line_ids=(),
) -> SeedResult:
    """Collapse low-criticality *in-country* AC edges until each k_c is exact.

    Costs are nonnegative, caller-supplied scores (typically annual MWh with
    declared weighting). No new purported ENTSO-E objective is introduced.
    Explicitly protected cuts never disappear; infeasible protection fails.
    """
    validate_country_feasibility(grid, resolved_labels, budget)
    branches = grid.active_branches
    edge_ids = {x.identifier for x in branches}
    protected = frozenset(protected_line_ids)
    if not protected.issubset(edge_ids):
        raise CountryContractError("Protected line is not an active AC line")
    if merge_cost_by_branch is None:
        if budget.official:
            raise CountryContractError("Official seed requires declared criticality costs")
        costs = {id: 0.0 for id in edge_ids}     # I: deterministic topology-only fixture
    else:
        if set(merge_cost_by_branch) != edge_ids:
            raise CountryContractError("Missing/extra edge criticality cost")
        costs = dict(merge_cost_by_branch)
        if any(not math.isfinite(x) or x < 0 for x in costs.values()):
            raise CountryContractError("Criticality cost must be finite and nonnegative")
    pos = {bus: i for i, bus in enumerate(grid.bus_ids)}
    parent = list(range(len(grid.bus_ids)))
    counts = {name: resolved_labels.count(name) for name in budget.quotas}
    # Per-component boundary: adjacent root -> (sum of all tie costs, is protected).
    boundary: list[dict[int, tuple[float, bool]]] = [
        {} for _ in range(len(grid.bus_ids))
    ]
    for edge in branches:
        i, j = pos[edge.bus0], pos[edge.bus1]
        if resolved_labels[i] != resolved_labels[j]:
            continue                          # retain cross-country branch
        cost, lock = costs[edge.identifier], edge.identifier in protected
        oldcost, oldlock = boundary[i].get(j, (0., False))
        boundary[i][j] = (oldcost + cost, oldlock or lock)
        oldcost, oldlock = boundary[j].get(i, (0., False))
        boundary[j][i] = (oldcost + cost, oldlock or lock)

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    heap = []
    for i, adj in enumerate(boundary):
        for j, (cost, locked) in adj.items():
            if i < j and not locked:
                heappush(heap, (cost, resolved_labels[i], i, j))
    merges = []
    while any(counts[name] > budget.quotas[name] for name in budget.quotas):
        selected = None
        while heap:
            cost, label, i, j = heappop(heap)
            if root(i) != i or root(j) != j or i == j:
                continue
            if counts[label] <= budget.quotas[label]:
                continue
            current = boundary[i].get(j)
            if current is None or current[1] or current[0] != cost:
                continue                            # stale after merged parallel ties
            selected = (cost, label, i, j)
            break
        if selected is None:
            raise CountryContractError(
                "Cannot meet exact quotas with connected country-pure AC clusters "
                "and protected critical cuts"
            )
        cost, label, i, j = selected
        # Canonical root is min original index to make seeds reproducible.
        a, b = min(i, j), max(i, j)
        parent[b] = a
        counts[label] -= 1
        neighbors = set(boundary[a]) | set(boundary[b])
        neighbors.discard(a)
        neighbors.discard(b)
        merged_boundary = {}
        for neighbor in neighbors:
            nbr = root(neighbor)
            if nbr in (a, b):
                continue
            left = boundary[a].get(nbr, (0., False))
            right = boundary[b].get(nbr, (0., False))
            combined = (left[0] + right[0], left[1] or right[1])
            merged_boundary[nbr] = combined
            boundary[nbr].pop(a, None)
            boundary[nbr].pop(b, None)
            boundary[nbr][a] = combined
            if not combined[1]:
                heappush(heap, (combined[0], label, a, nbr) if a < nbr else
                         (combined[0], label, nbr, a))
        boundary[a] = merged_boundary
        boundary[b].clear()
        merges.append({
            "country": label, "root_bus": grid.bus_ids[a],
            "absorbed_bus": grid.bus_ids[b], "lost_cut_score": cost,
            "country_zone_count_after": counts[label],
        })

    roots_by_country = {
        country: sorted({root(i) for i, c in enumerate(resolved_labels) if c == country})
        for country in sorted(budget.quotas)
    }
    root_to_zone = {
        r: f"{country}::{j:03d}"
        for country, roots in roots_by_country.items()
        for j, r in enumerate(roots, start=1)
    }
    zone_of_bus = tuple(root_to_zone[root(i)] for i in range(len(grid.bus_ids)))
    verified = validate_busmap(grid, zone_of_bus, resolved_labels, budget, protected)
    cross_country = tuple(
        edge.identifier for edge in branches
        if resolved_labels[pos[edge.bus0]] != resolved_labels[pos[edge.bus1]]
    )
    return SeedResult(zone_of_bus, verified, tuple(merges), tuple(sorted(protected)),
                      cross_country)
