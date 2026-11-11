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




class QuotaFeasibilityError(CountryContractError):
    """Separate a proven small-graph obstruction from exhausted heuristics."""
    def __init__(self, status: str, country: str, visited: int):
        self.status, self.country, self.visited = status, country, visited
        super().__init__(
            f"Cannot meet exact quotas: {status}; country={country}, "
            f"feasibility_states={visited}"
        )


def canonical_protected_ids(values) -> tuple[str, ...]:
    """One-shot iterable ownership, strict IDs, canonical order and deduplication."""
    if isinstance(values, (str, bytes)):
        raise CountryContractError("Protected line IDs must be an iterable of distinct strings")
    try:
        owned = tuple(values)
    except TypeError as exc:
        raise CountryContractError("Protected line IDs must be iterable") from exc
    if any(type(x) is not str or not x.strip() for x in owned):
        raise CountryContractError("Protected line IDs must be nonempty strings")
    if len(owned) != len(set(owned)):
        raise CountryContractError("Duplicate protected line IDs")
    return tuple(sorted(owned))


def _bounded_country_partition(grid, labels, country, quota, costs, protected,
                               *, max_nodes=16, max_states=100000):
    """Deterministic complete merge-state DFS only within stated resource bounds.

    Unlike a greedy dead end, exhausted DFS on <=max_nodes vertices and
    <=max_states distinct partitions proves infeasibility for THIS finite case.
    Otherwise HEURISTIC_STUCK means no global infeasibility claim.
    """
    indices = tuple(i for i, label in enumerate(labels) if label == country)
    if len(indices) > max_nodes:
        raise QuotaFeasibilityError("HEURISTIC_STUCK", country, 0)
    pos = {bus: i for i, bus in enumerate(grid.bus_ids)}
    edges = tuple(
        (pos[e.bus0], pos[e.bus1], costs[e.identifier],
         e.identifier in protected)
        for e in grid.active_branches
        if labels[pos[e.bus0]] == country and labels[pos[e.bus1]] == country
    )
    seen = set()
    visited = 0

    def visit(groups):
        nonlocal visited
        key = tuple(tuple(sorted(g)) for g in sorted(groups, key=min))
        if key in seen:
            return None
        if visited >= max_states:
            raise QuotaFeasibilityError("HEURISTIC_STUCK", country, visited)
        visited += 1
        seen.add(key)
        if len(groups) == quota:
            return groups, ()
        options = []
        for a in range(len(groups)):
            for b in range(a + 1, len(groups)):
                left, right = groups[a], groups[b]
                crossing = [(value, lock) for i, j, value, lock in edges
                            if (i in left and j in right) or (j in left and i in right)]
                if crossing and not any(lock for _, lock in crossing):
                    options.append((sum(v for v, _ in crossing),
                                    min(left), min(right), a, b))
        for cost, start, end, a, b in sorted(options):
            merged = groups[a] | groups[b]
            reduced = tuple(g for j, g in enumerate(groups) if j not in (a, b))
            next_groups = tuple(sorted((*reduced, merged), key=min))
            answer = visit(next_groups)
            if answer is not None:
                final, steps = answer
                log = {
                    "country": country,
                    "root_bus": grid.bus_ids[min(start, end)],
                    "absorbed_bus": grid.bus_ids[max(start, end)],
                    "lost_cut_score": float(cost),
                    "country_zone_count_after": len(next_groups),
                    "feasibility_method": "BOUNDED_EXACT_FALLBACK",
                }
                return final, (log,) + steps
        return None

    answer = visit(tuple(frozenset((i,)) for i in indices))
    if answer is None:
        raise QuotaFeasibilityError("PROVEN_INFEASIBLE", country, visited)
    return answer, visited

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
    protected = frozenset(canonical_protected_ids(protected_line_ids))
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
            # A greedy local dead end is NOT proof that a feasible country
            # partition does not exist. Rebuild unfinished countries from
            # singleton buses using bounded exact state-space enumeration.
            for blocked_country in sorted(budget.quotas):
                if counts[blocked_country] <= budget.quotas[blocked_country]:
                    continue
                (groups, steps), explored = _bounded_country_partition(
                    grid, resolved_labels, blocked_country,
                    budget.quotas[blocked_country], costs, protected,
                )
                # Undo any incorrect earlier greedy merges in this country.
                nodes = [i for i, c in enumerate(resolved_labels)
                         if c == blocked_country]
                for node in nodes:
                    parent[node] = node
                for group in groups:
                    leader = min(group)
                    for node in group:
                        parent[node] = leader
                counts[blocked_country] = len(groups)
                merges = [m for m in merges if m["country"] != blocked_country]
                merges.extend(steps)
            break
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
