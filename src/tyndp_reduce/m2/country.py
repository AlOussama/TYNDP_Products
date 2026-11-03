"""Country-pure, connected, exact-quota initial graph contraction (D/T/I-01).

The published country quota table is *data*, not an inferred region heuristic.
Unknown country labels, impossible quotas and swallowed protected lines fail
closed. The deterministic merge score is an explicit NON-PUBLISHED I-choice.
"""
import csv
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path

import numpy as np

from .contracts import ContractError, CountryZoneBudget, DetailedGridSnapshot, Evidence

# Exact transcription of Table 3, pages 26-27, consultation version 2026-02-25.
PUBLISHED_TABLE_3 = (
    ("Albania",1),("Austria",4),("Belgium",3),("Bosnia",1),
    ("Bulgaria",1),("Croatia",1),("Cyprus",1),("Czech Republic",2),
    ("Denmark",2),("Estonia",1),("Finland",1),("France",16),
    ("Germany",11),("Greece",2),("Hungary",1),("Ireland",1),
    ("Italy",7),("Latvia",1),("Lithuania",1),("Luxembourg",1),
    ("Macedonia",1),("Malta",1),("Montenegro",1),("Netherlands",5),
    ("Northern Ireland",1),("Norway",3),("Poland",5),("Portugal",2),
    ("Romania",3),("Serbia",1),("Slovakia",1),("Slovenia",1),
    ("Spain",10),("Sweden",4),("Switzerland",2),("Turkey",1),
    ("United Kingdom",1)
)


def load_official_budget(path=None, target_year="all"):
    if path is None:
        path = (Path(__file__).resolve().parents[3] / "docs" / "current" /
                "IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv")
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ContractError("BLOCKED_DATA: country CSV is not UTF-8") from exc
    import io
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ["country_label_as_published", "n_zones", "source_page"]:
        raise ContractError("BLOCKED_DATA: unknown official CSV columns")
    rows = []
    for row in reader:
        try:
            label, n, page = row["country_label_as_published"], int(row["n_zones"]), int(row["source_page"])
        except (TypeError, ValueError) as exc:
            raise ContractError("BLOCKED_DATA: invalid official country row") from exc
        if page not in (26, 27) or not label or str(n) != row["n_zones"]:
            raise ContractError("BLOCKED_DATA: CSV country/page/quota malformed")
        rows.append((label, n))
    if tuple(rows) != PUBLISHED_TABLE_3:
        raise ContractError("BLOCKED_DATA: official Table 3 differs from pinned 37/102 transcription")
    return CountryZoneBudget(Evidence(str(path), "IoSN-2026-consultation-2026-02-25",
                                        sha256(raw).hexdigest(), target_year),
                             tuple(rows), official=True)


def _graph_components(nodes, branches, pos, excluded=frozenset()):
    """Connected components of a country-induced AC graph, not via foreign buses."""
    s = set(nodes)
    neighbors = {u: set() for u in nodes}
    for e in branches:
        a, b = pos[e.bus0], pos[e.bus1]
        if e.name not in excluded and a in s and b in s:
            neighbors[a].add(b)
            neighbors[b].add(a)
    components = []
    while s:
        seed = min(s)
        stack = [seed]
        seen = {seed}
        while stack:
            for v in neighbors[stack.pop()]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        components.append(seen)
        s -= seen
    return components


def validate_country_feasibility(grid: DetailedGridSnapshot,
                                 budget: CountryZoneBudget,
                                 full_geography=False):
    labels = [b.country for b in grid.buses]
    actual, expected = set(labels), set(budget.by_label)
    if actual != expected:
        raise ContractError("BLOCKED_DATA: exact country-label coverage differs; no synonyms/UK-NI merge: " +
                            repr(sorted(actual.symmetric_difference(expected))))
    if full_geography and (not budget.official or grid.fixture):
        raise ContractError("BLOCKED_DATA: official full-European input required")
    if not full_geography and budget.official:
        raise ContractError("BLOCKED_DATA: official quota is not a synthetic fixture budget")
    pos = {b.name: i for i, b in enumerate(grid.buses)}
    for country, quota in budget.quotas:
        nodes = [i for i, c in enumerate(labels) if c == country]
        components = _graph_components(nodes, grid.branches, pos)
        if quota > len(nodes) or quota < len(components):
            raise ContractError("BLOCKED_DATA: infeasible country quota/components: " + country)
    return True


def assert_country_zones(grid, budget, busmap, protected=()):
    if any(not isinstance(x, (int, np.integer)) or isinstance(x, (bool, np.bool_))
           for x in busmap):
        raise ContractError("G02: integer zone IDs required; no implicit rounding")
    z = tuple(int(x) for x in busmap)
    if len(z) != len(grid.buses) or set(z) != set(range(len(set(z)))):
        raise ContractError("G02: zone IDs must be contiguous and total")
    if len(set(z)) != sum(budget.by_label.values()):
        raise ContractError("G02: exact total zone count violated")
    actual = {}
    for zone in sorted(set(z)):
        nodes = [i for i, v in enumerate(z) if v == zone]
        countries = {grid.buses[i].country for i in nodes}
        if len(countries) != 1:
            raise ContractError("G02: mixed-country zone " + str(zone))
        country = next(iter(countries))
        actual[country] = actual.get(country, 0) + 1
        pos = {b.name: i for i, b in enumerate(grid.buses)}
        if len(_graph_components(nodes, grid.branches, pos)) != 1:
            raise ContractError("G03: disconnected AC zone " + str(zone))
    if actual != budget.by_label:
        raise ContractError("G02: per-country zone quotas violated")
    by_name = {b.name: i for i, b in enumerate(grid.buses)}
    by_branch = {e.name: e for e in grid.branches}
    for name in protected:
        if name not in by_branch:
            raise ContractError("G03: unknown critical/protected line " + name)
        e = by_branch[name]
        if z[by_name[e.bus0]] == z[by_name[e.bus1]]:
            raise ContractError("G03: critical physical line swallowed " + name)
    return True


def country_quota_busmap(grid: DetailedGridSnapshot, budget: CountryZoneBudget,
                         edge_importance, protected=(), full_geography=False):
    """I-01: deterministic near-linear country-constrained Kruskal growth.

    Original *parallel pair* weights are summed and edges sorted once.
    This is NOT ENTSO-E's unpublished optimisation or globally optimal cut
    minimisation. Hard cannot-link pairs preserve protected critical branches
    even when an alternate AC path exists. Borders stay in the AC graph.
    """
    validate_country_feasibility(grid, budget, full_geography)
    n, m = len(grid.buses), len(grid.branches)
    importance = np.asarray(edge_importance, dtype=float)
    if importance.shape != (m,) or not np.all(np.isfinite(importance)) or np.any(importance < 0):
        raise ContractError("BLOCKED_DATA: nonnegative finite edge-importance required")
    names = {edge.name for edge in grid.branches}
    protected = frozenset(protected)
    if not protected <= names:
        raise ContractError("G03: protected IDs not in AC network")
    countries = [bus.country for bus in grid.buses]
    pos = {bus.name: i for i, bus in enumerate(grid.buses)}
    parent = list(range(n))
    members = [{i} for i in range(n)]
    forbidden = [set() for _ in range(n)]
    weights = {}
    for i, edge in enumerate(grid.branches):
        u, v = pos[edge.bus0], pos[edge.bus1]
        if edge.name in protected:
            forbidden[u].add(v)
            forbidden[v].add(u)
        if countries[u] == countries[v]:
            a, b = sorted((u, v))
            weights[(a,b)] = weights.get((a,b), 0.) + float(importance[i])
    candidate_edges = sorted((score, a, b) for (a,b), score in weights.items())

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for country, quota in budget.quotas:
        remaining = sum(c == country for c in countries)
        for _score, u, v in candidate_edges:
            if remaining == quota:
                break
            if countries[u] != country:
                continue
            a, b = find(u), find(v)
            if a == b or not forbidden[a].isdisjoint(members[b]) or \
               not forbidden[b].isdisjoint(members[a]):
                continue
            a, b = sorted((a, b))
            parent[b] = a
            members[a].update(members[b])
            forbidden[a].update(forbidden[b])
            members[b].clear()
            forbidden[b].clear()
            remaining -= 1
        if remaining != quota:
            raise ContractError("BLOCKED_DATA: quota cannot be met while preserving critical AC lines: " +
                                country)
    rank = {label: i for i, (label, _) in enumerate(budget.quotas)}
    roots = sorted({find(i) for i in range(n)},
                   key=lambda root: (rank[countries[root]], min(members[root])))
    remap = {root: i for i, root in enumerate(roots)}
    busmap = tuple(remap[find(i)] for i in range(n))
    assert_country_zones(grid, budget, busmap, protected)
    return busmap
