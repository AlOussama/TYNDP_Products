"""Independent RR1-CLU adversarial replay against pinned integration fb201ef5.

Does not import worker test oracles, and does not modify production.
Counts the mathematical empty graph separately from the original nonempty
1,804-case domain. Graph feasibility is decided by a bitmask partition oracle.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from types import SimpleNamespace
import json
import time

import numpy as np
import pytest

from tyndp_reduce.iosn_official.country import (
    CountryContractError, CountryZoneBudget,
    canonicalize_country_aliases, load_official_country_budget,
)
from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture
from tyndp_reduce.iosn_official.ma1 import execute_ma1
from tyndp_reduce.iosn_official.operators import build_oriented_projection
from tyndp_reduce.iosn_official.screen import ScreeningError, screen_annual_overload
from tyndp_reduce.iosn_official.seed import (
    QuotaFeasibilityError, quota_seed,
)


@dataclass(frozen=True)
class Edge:
    identifier: str
    bus0: str
    bus1: str
    voltage_kv: float = 225.0
    kind: str = "line"
    screening_class_kv: float | None = None


def network(nodes, branches, labels=None, *, gap=False):
    return SimpleNamespace(
        bus_ids=tuple(nodes),
        raw_country_ids=tuple(labels if labels is not None else ("X",) * len(nodes)),
        active_branches=tuple(branches),
        incomplete_110kv_ties=gap,
    )


@lru_cache(maxsize=None)
def partitions_by_mask(n):
    """Canonical unordered set partitions from bit-subsets, not greedy merges."""
    def walk(remaining):
        if not remaining:
            yield ()
            return
        pivot = remaining & -remaining
        free = remaining ^ pivot
        sub = free
        while True:
            block = pivot | sub
            for tail in walk(remaining ^ block):
                yield (block,) + tail
            if sub == 0:
                break
            sub = (sub - 1) & free
    return tuple(walk((1 << n) - 1))


def connected(mask, edges):
    seen = mask & -mask
    while True:
        nxt = seen
        for a, b in edges:
            if (seen & (1 << a)) and (mask & (1 << b)):
                nxt |= 1 << b
            if (seen & (1 << b)) and (mask & (1 << a)):
                nxt |= 1 << a
        if nxt == seen:
            return seen == mask
        seen = nxt


def oracle_partition(n, quota, edges, protected):
    for groups in partitions_by_mask(n):
        if len(groups) != quota:
            continue
        if any(any((g & (1 << a)) and (g & (1 << b)) for g in groups)
               for a, b in protected):
            continue
        if all(connected(g, edges) for g in groups):
            return groups
    return None


def check_returned_zones(g, labels, budget, result, protected_ids):
    """Independent validator: country identity, exact quotas, cuts, AC paths."""
    assert len(result.zone_of_bus) == len(g.bus_ids)
    p = {name: i for i, name in enumerate(g.bus_ids)}
    edges = [(p[b.bus0], p[b.bus1]) for b in g.active_branches]
    grouped = {}
    for i, zone in enumerate(result.zone_of_bus):
        assert isinstance(zone, str) and zone
        grouped.setdefault(zone, set()).add(i)
    actual = Counter()
    for members in grouped.values():
        assert len({labels[i] for i in members}) == 1
        actual[labels[next(iter(members))]] += 1
        mask = sum(1 << i for i in members)
        assert connected(mask, edges), ("disconnected_zone", members)
    assert dict(actual) == dict(budget.quotas)
    for b in g.active_branches:
        if b.identifier in protected_ids:
            assert result.zone_of_bus[p[b.bus0]] != result.zone_of_bus[p[b.bus1]]
    return grouped


def test_complete_independent_four_node_oracle_including_empty_graph():
    """Check every 3^6 graph and k=1..4; distinguish 1805 vs 1804 domains."""
    started = time.perf_counter()
    assert len(partitions_by_mask(4)) == 15
    pairs = tuple(combinations(range(4), 2))
    nodes = tuple(f"v{i}" for i in range(4))
    feasible_by_k = Counter()
    accepted = 0
    false_blocked = 0
    false_proven = 0
    false_accepted = 0
    graph_count = 0
    for states in product((0, 1, 2), repeat=len(pairs)):
        graph_count += 1
        active = [(a, b, s) for (a, b), s in zip(pairs, states) if s]
        edges = [(a, b) for a, b, _ in active]
        locked = [(a, b) for a, b, s in active if s == 2]
        branches = tuple(Edge(f"l{a}{b}", nodes[a], nodes[b]) for a, b, _ in active)
        by_id = {b.identifier: float(((i + 3) * 11 + (j + 7) * 19) % 29)
                 for b, (i, j, _) in zip(branches, active)}
        protected_ids = tuple(f"l{a}{b}" for a, b in locked)
        g = network(nodes, branches)
        for k in range(1, 5):
            truth = oracle_partition(4, k, edges, locked)
            possible = truth is not None
            if possible:
                feasible_by_k[k] += 1
            budget = CountryZoneBudget.synthetic({"X": k})
            try:
                got = quota_seed(
                    g, ("X",) * 4, budget,
                    merge_cost_by_branch=by_id,
                    protected_line_ids=protected_ids,
                )
            except CountryContractError as error:
                if possible:
                    false_blocked += 1
                    if getattr(error, "status", "") == "PROVEN_INFEASIBLE":
                        false_proven += 1
                continue
            if not possible:
                false_accepted += 1
            else:
                accepted += 1
                check_returned_zones(g, ("X",) * 4, budget, got, set(protected_ids))
                again = quota_seed(
                    g, ("X",) * 4, budget,
                    merge_cost_by_branch=dict(reversed(tuple(by_id.items()))),
                    protected_line_ids=iter(reversed(protected_ids)),
                )
                assert got.zone_of_bus == again.zone_of_bus
    assert graph_count == 729
    assert dict(feasible_by_k) == {1: 38, 2: 373, 3: 665, 4: 729}
    assert sum(feasible_by_k.values()) == 1805
    assert sum(feasible_by_k.values()) - 1 == 1804
    assert (false_blocked, false_proven, false_accepted, accepted) == (0, 0, 0, 1805)
    print("RR1_CLU_ORACLE=" + json.dumps({
        "graphs": graph_count, "feasible_mathematical": 1805,
        "feasible_nonempty_graph_domain": 1804,
        "empty_graph_k4_verified": True, "feasible_by_quota": dict(feasible_by_k),
        "false_rejected_feasible": false_blocked,
        "false_proven_infeasible": false_proven,
        "false_accepted_infeasible": false_accepted,
        "recovered_feasible": accepted,
        "seconds": round(time.perf_counter() - started, 3),
    }, sort_keys=True))


def test_original_protected_cut_and_new_five_node_trap():
    for n in (4, 5):
        nodes = tuple(f"v{i}" for i in range(n))
        data = [
            ("p01", 0, 1, 7., True), ("p02", 0, 2, 4., True),
            ("p03", 0, 3, 0., False), ("p13", 1, 3, 7., False),
            ("p23", 2, 3, 0., False),
        ]
        if n == 5:
            data.append(("p14", 1, 4, 0., False))
        g = network(nodes, tuple(Edge(eid, nodes[a], nodes[b])
                                 for eid, a, b, _, _ in data))
        costs = {eid: cost for eid, _, _, cost, _ in data}
        protected = tuple(eid for eid, _, _, _, lock in data if lock)
        truth = oracle_partition(
            n, 2, [(a, b) for _, a, b, _, _ in data],
            [(a, b) for _, a, b, _, lock in data if lock],
        )
        assert truth is not None
        result = quota_seed(g, ("X",) * n, CountryZoneBudget.synthetic({"X": 2}),
                            merge_cost_by_branch=costs, protected_line_ids=protected)
        groups = check_returned_zones(g, ("X",) * n,
                                      CountryZoneBudget.synthetic({"X": 2}),
                                      result, set(protected))
        assert {frozenset(m) for m in groups.values()} == {
            frozenset({0}), frozenset(range(1, n))
        }
        assert any(row.get("feasibility_method") == "BOUNDED_EXACT_FALLBACK"
                   for row in result.merge_ledger)


def multi_country_fixture():
    nodes = tuple([f"x{i}" for i in range(7)] +
                  [f"y{i}" for i in range(4)] +
                  [f"z{i}" for i in range(3)])
    labels = ("X",) * 7 + ("Y",) * 4 + ("Z",) * 3
    data = [
        ("x01", "x0", "x1", 7., True),
        ("x02", "x0", "x2", 4., True),
        ("x03", "x0", "x3", 0., False),
        ("x13", "x1", "x3", 7., False),
        ("x23", "x2", "x3", 0., False),
        ("x14", "x1", "x4", 0., False),
        ("x45", "x4", "x5", 0., False),
        ("y01", "y0", "y1", 1., False),
        ("y12", "y1", "y2", 2., False),
        ("y23", "y2", "y3", 1., False),
        ("z01", "z0", "z1", 1., False),
        ("z12", "z1", "z2", 1., False),
        ("cross_xy_forward", "x5", "y0", 1., True),
        ("cross_xy_reverse", "y0", "x5", 1., False),
        ("cross_yz", "y3", "z0", 1., False),
        ("cross_xz", "z2", "x2", 1., False),
    ]
    edges = tuple(Edge(i, a, b, 110. if i == "y12" else 225.)
                  for i, a, b, _, _ in data)
    costs = {i: v for i, _, _, v, _ in data}
    protected = tuple(i for i, _, _, _, lock in data if lock)
    budget = CountryZoneBudget.synthetic({"X": 3, "Y": 2, "Z": 2})
    return network(nodes, edges, labels), labels, budget, costs, protected


def dense_oriented_reference(g, zones):
    zs = tuple(sorted(set(zones)))
    zi = {name: j for j, name in enumerate(zs)}
    bi = {name: j for j, name in enumerate(g.bus_ids)}
    n, m = len(g.bus_ids), len(g.active_branches)
    ad = np.zeros((n, m), dtype=int)
    p = np.zeros((len(zs), n), dtype=int)
    for i, zid in enumerate(zones):
        p[zi[zid], i] = 1
    pairs = set()
    for j, branch in enumerate(g.active_branches):
        a, b = bi[branch.bus0], bi[branch.bus1]
        ad[a, j] = 1
        ad[b, j] = -1
        if zones[a] != zones[b]:
            pairs.add(tuple(sorted((zi[zones[a]], zi[zones[b]]))))
    pairs = sorted(pairs)
    gamma = np.zeros((len(pairs), m), dtype=int)
    az = np.zeros((len(zs), len(pairs)), dtype=int)
    for row, (a, b) in enumerate(pairs):
        az[a, row] = 1
        az[b, row] = -1
    by_pair = {pair: row for row, pair in enumerate(pairs)}
    for j, branch in enumerate(g.active_branches):
        a, b = zi[zones[bi[branch.bus0]]], zi[zones[bi[branch.bus1]]]
        if a != b:
            gamma[by_pair[tuple(sorted((a, b)))], j] = 1 if a < b else -1
    return p, gamma, az, ad


def test_larger_6node_three_country_two_island_protection_and_dense_identity():
    g, labels, budget, costs, protected = multi_country_fixture()
    x_edges = [(int(e.bus0[1:]), int(e.bus1[1:]))
               for e in g.active_branches
               if e.bus0.startswith("x") and e.bus1.startswith("x")]
    x_locks = [(int(e.bus0[1:]), int(e.bus1[1:]))
               for e in g.active_branches
               if e.identifier in {"x01", "x02"}]
    assert oracle_partition(6, 2, x_edges, x_locks) is not None
    result = quota_seed(g, labels, budget, merge_cost_by_branch=costs,
                        protected_line_ids=protected)
    groups = check_returned_zones(g, labels, budget, result, set(protected))
    assert {frozenset(m) for m in groups.values() if 0 in m} == {frozenset({0})}
    assert any(m == {6} for m in groups.values())
    assert {"cross_xy_forward", "cross_xy_reverse", "cross_yz", "cross_xz"}.issubset(
        set(result.retained_cross_country_branch_ids))
    assert len(groups) == 7
    assert len(result.merge_ledger) == len(g.bus_ids) - 7
    # The X6 vertex is a separate global AC island; it cannot be joined via HVDC.
    pos = {s: i for i, s in enumerate(g.bus_ids)}
    edge_pairs = [(pos[e.bus0], pos[e.bus1]) for e in g.active_branches]
    assert not connected((1 << len(g.bus_ids)) - 1, edge_pairs)
    assert connected(((1 << len(g.bus_ids)) - 1) ^ (1 << 6), edge_pairs)
    with pytest.raises(CountryContractError, match="110-kV"):
        quota_seed(network(g.bus_ids, g.active_branches, labels, gap=True),
                   labels, budget, merge_cost_by_branch=costs,
                   protected_line_ids=protected)

    projection = build_oriented_projection(g, result.zone_of_bus)
    pd, gd, azd, add = dense_oriented_reference(g, result.zone_of_bus)
    for actual, expected in (
        (projection.P.toarray(), pd), (projection.Gamma.toarray(), gd),
        (projection.A_z.toarray(), azd), (projection.A_d.toarray(), add),
    ):
        np.testing.assert_array_equal(actual, expected)
    np.testing.assert_array_equal(azd @ gd, pd @ add)

    flows = np.zeros((len(g.active_branches), 2))
    line_index = {b.identifier: j for j, b in enumerate(g.active_branches)}
    flows[line_index["cross_xy_forward"], :] = 32.
    flows[line_index["cross_xy_reverse"], :] = 30.
    nodal = add @ flows
    reference = SimpleNamespace(
        branch_ids=projection.branch_ids, bus_ids=projection.bus_ids,
        snapshot_ids=("new-s0", "new-s1"), flow_mw=flows,
        nodal_net_mw=nodal,
    )
    assert projection.verify(reference)
    zp, zf = projection.aggregate(reference)
    np.testing.assert_array_equal(zp, pd @ nodal)
    np.testing.assert_array_equal(zf, gd @ flows)
    np.testing.assert_array_equal(azd @ zf, zp)
    events = projection.counterflow_ledger(reference)
    relevant = [r for r in events if
                abs(r["cancelled_absolute_MW"] - 60.) < 1e-12]
    assert len(relevant) == 2
    assert all(abs(abs(r["net_MW"]) - 2.) < 1e-12 for r in relevant)


def test_proven_infeasible_is_distinct_from_resource_limited_feasible():
    closed = network(("u0", "u1", "u2"),
                     (Edge("a", "u0", "u1"), Edge("b", "u1", "u2")))
    assert oracle_partition(3, 1, [(0, 1), (1, 2)], [(0, 1), (1, 2)]) is None
    with pytest.raises(QuotaFeasibilityError) as caught:
        quota_seed(closed, ("X",) * 3, CountryZoneBudget.synthetic({"X": 1}),
                   merge_cost_by_branch={"a": 1., "b": 1.},
                   protected_line_ids=("a", "b"))
    assert caught.value.status == "PROVEN_INFEASIBLE"
    assert caught.value.visited >= 1

    # A constructive feasible solution exists but the 16-node cap prevents proof.
    nodes = tuple(f"b{i}" for i in range(17))
    data = [
        ("e01", 0, 1, 7., True), ("e02", 0, 2, 4., True),
        ("e03", 0, 3, 0., False), ("e13", 1, 3, 7., False),
        ("e23", 2, 3, 0., False),
    ]
    data.extend((f"leaf{i}", 1, i, 0., False) for i in range(4, 17))
    edges = tuple(Edge(name, nodes[a], nodes[b]) for name, a, b, _, _ in data)
    costs = {name: value for name, _, _, value, _ in data}
    protected = tuple(name for name, _, _, _, yes in data if yes)
    # {b0} / {b1,b2,...,b16} is an explicit AC-connected protected-safe partition.
    assert connected(sum(1 << i for i in range(1, 17)),
                     [(a, b) for _, a, b, _, _ in data])
    with pytest.raises(QuotaFeasibilityError) as caught:
        quota_seed(network(nodes, edges), ("X",) * 17,
                   CountryZoneBudget.synthetic({"X": 2}),
                   merge_cost_by_branch=costs, protected_line_ids=protected)
    assert caught.value.status == "HEURISTIC_STUCK"
    assert caught.value.visited == 0
    print("RR1_CLU_LIMITED_SEARCH=" + json.dumps({
        "vertices": 17, "constructively_feasible": True,
        "status": caught.value.status, "max_nodes": 16,
    }, sort_keys=True))


def test_annual_90mwh_and_voltage_class_fail_closed():
    years = tuple(f"Y{i}" for i in range(5))
    snapshots = tuple(f"{y}-{half}" for y in years for half in ("a", "b"))
    time_set = SimpleNamespace(
        snapshot_ids=snapshots,
        year_for_snapshot=tuple(y for y in years for _ in (0, 1)),
        weather_year_ids=years,
        duration_hours=np.array([0.25, 0.75] * 5),
    )
    flow = SimpleNamespace(
        branch_ids=("m",), bus_ids=("a", "b"), snapshot_ids=snapshots,
        flow_mw=np.array([[100., -100.] * 5]), neutral_calibration=False,
    )
    rating = SimpleNamespace(
        snapshot_ids=snapshots, normal_mw={"m": np.full(10, 10.)},
    )
    def run(kv, declared=None, kind="line"):
        return screen_annual_overload(
            network(("a", "b"), (Edge("m", "a", "b", kv, kind, declared),)),
            flow, time_set, rating)
    for kv in (225., 400.):
        admitted = run(kv)
        assert admitted.screened_line_ids == ("m",)
        assert all(admitted.year_score("m", y) == 90. for y in years)
        with pytest.raises(ScreeningError):
            run(kv, 0.)
    for kv, mapped in ((220., 225.), (380., 400.)):
        with pytest.raises(ScreeningError, match="explicit screening_class_kv"):
            run(kv)
        with pytest.raises(ScreeningError, match="exclusion"):
            run(kv, 0.)
        assert all(run(kv, mapped).year_score("m", y) == 90. for y in years)
    with pytest.raises(ScreeningError):
        run(400., 225.)
    assert run(400., 0., kind="transformer").screened_line_ids == ()
    assert run(110.).screened_line_ids == ()


def test_protected_tuple_generator_fingerprint_and_source_pages(tmp_path):
    args = build_synthetic_fixture()
    fixed = execute_ma1(*args, protected_line_ids=("d12",))
    streamed = execute_ma1(*args, protected_line_ids=(s for s in ["d12"]))
    assert fixed.seed.zone_of_bus == streamed.seed.zone_of_bus
    assert fixed.seed.protected_line_ids == streamed.seed.protected_line_ids
    assert fixed.input_manifest_sha256 == streamed.input_manifest_sha256
    assert len(fixed.input_manifest_sha256) == 64
    with pytest.raises(CountryContractError, match="Duplicate"):
        execute_ma1(*args, protected_line_ids=("d12", "d12"))

    path = Path("docs/current/IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv")
    raw = path.read_bytes()
    official = load_official_country_budget()
    assert sha256(raw).hexdigest() == official.source_sha256
    assert len(official.quotas) == 37 and sum(official.quotas.values()) == 102
    assert official.quotas["United Kingdom"] == 1
    assert official.quotas["Northern Ireland"] == 1
    assert official.source_pages["United Kingdom"] == 27
    forged = tmp_path / "table3_wrong_page.csv"
    text = raw.decode("utf-8-sig")
    assert "United Kingdom,1,27" in text
    forged.write_text(text.replace("United Kingdom,1,27", "United Kingdom,1,26"))
    with pytest.raises(CountryContractError, match="page"):
        load_official_country_budget(forged)


def test_opt_in_alias_witness_pins_uk_ni_and_is_metadata_not_original_sha():
    budget = CountryZoneBudget.synthetic({
        "Germany": 1, "Northern Ireland": 1, "United Kingdom": 1})
    labels = ("DE-A", "DE-B", "NIR", "GBR")
    records = {
        "DE-A": {"country_label": "Germany", "source_uri": "source://one",
                 "source_sha256": "0" * 64},
        "DE-B": {"country_label": "Germany", "source_uri": "source://two",
                 "source_sha256": "1" * 64},
        "NIR": {"country_label": "Northern Ireland", "source_uri": "source://ni",
                "source_sha256": "2" * 64},
        "GBR": {"country_label": "United Kingdom", "source_uri": "source://gb",
                "source_sha256": "3" * 64},
    }
    witness = canonicalize_country_aliases(labels, records, budget)
    assert witness.original_raw_ids == labels
    assert witness.normalized_raw_ids == (
        "Germany", "Germany", "Northern Ireland", "United Kingdom")
    assert witness.status == "SOURCE_DECLARED_BYTES_NOT_INDEPENDENTLY_ATTESTED"
    revised = {r: dict(v) for r, v in records.items()}
    revised["DE-A"]["source_sha256"] = "9" * 64
    assert (canonicalize_country_aliases(labels, revised, budget)
            .alias_manifest_sha256 != witness.alias_manifest_sha256)
    revised = {r: dict(v) for r, v in records.items()}
    revised["NIR"]["country_label"] = "United Kingdom"
    with pytest.raises(CountryContractError, match="merging"):
        canonicalize_country_aliases(labels, revised, budget)
