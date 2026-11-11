"""R-CLU independent frozen-commit adversarial review, not W-CLU code.

Proof-oriented fixtures; observations of known defects are asserted here as
REPRODUCERS, not interpreted as acceptance of those behaviors.
Original source freeze: 0254d867a34b66ec7b56c90225605d29ea328916.
"""
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from tyndp_reduce.iosn_official.country import (
    CountryContractError, CountryZoneBudget, load_official_country_budget,
    resolve_country_ids, validate_busmap,
)
from tyndp_reduce.iosn_official.seed import quota_seed
from tyndp_reduce.iosn_official.screen import (
    ScreeningError, screen_annual_overload, weighted_edge_costs,
)
from tyndp_reduce.iosn_official.operators import build_oriented_projection


@dataclass(frozen=True)
class Edge:
    identifier: str
    bus0: str
    bus1: str
    voltage_kv: float = 225.0
    kind: str = "line"
    screening_class_kv: float | None = None


def grid(names, edges, raw_ids=None, gap=False):
    return SimpleNamespace(
        bus_ids=tuple(names), active_branches=tuple(edges),
        raw_country_ids=tuple(raw_ids or ("X",) * len(names)),
        incomplete_110kv_ties=gap,
    )


# Expected values copied independently from the ENTSO-E PDF Table 3,
# 25 February 2026, printed pp. 26-27, NOT from PUBLISHED_QUOTAS.
TABLE3 = {
    "Albania": 1, "Austria": 4, "Belgium": 3, "Bosnia": 1,
    "Bulgaria": 1, "Croatia": 1, "Cyprus": 1, "Czech Republic": 2,
    "Denmark": 2, "Estonia": 1, "Finland": 1, "France": 16,
    "Germany": 11, "Greece": 2, "Hungary": 1, "Ireland": 1,
    "Italy": 7, "Latvia": 1, "Lithuania": 1, "Luxembourg": 1,
    "Macedonia": 1, "Malta": 1, "Montenegro": 1, "Netherlands": 5,
    "Northern Ireland": 1, "Norway": 3, "Poland": 5, "Portugal": 2,
    "Romania": 3, "Serbia": 1, "Slovakia": 1, "Slovenia": 1,
    "Spain": 10, "Sweden": 4, "Switzerland": 2, "Turkey": 1,
    "United Kingdom": 1,
}


def test_01_official_table3_independent_exact_reference():
    budget = load_official_country_budget()
    assert dict(budget.quotas) == TABLE3
    assert len(TABLE3) == 37 and sum(TABLE3.values()) == 102
    assert TABLE3["Northern Ireland"] == TABLE3["United Kingdom"] == 1
    path = (Path(__file__).resolve().parents[2] / "docs" / "current"
            / "IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv")
    assert len(path.read_text(encoding="utf-8").splitlines()) == 38


def _canonical_partitions(n):
    a = [0] * n

    def walk(index, last):
        if index == n:
            yield tuple(a)
        else:
            for z in range(last + 2):
                a[index] = z
                yield from walk(index + 1, max(last, z))

    yield from walk(1, 0)


def _feasible_partitions(n, k, edges, protected):
    """Independent exhaustive set-partition/connectivity/protection oracle."""
    good = []
    for assignment in _canonical_partitions(n):
        if len(set(assignment)) != k:
            continue
        if any(assignment[u] == assignment[v] for u, v in protected):
            continue
        valid = True
        for z in range(k):
            members = {i for i in range(n) if assignment[i] == z}
            reached = {min(members)}
            while True:
                expanded = reached | {
                    v for u, v in edges if u in reached and v in members
                } | {
                    u for u, v in edges if v in reached and u in members
                }
                if expanded == reached:
                    break
                reached = expanded
            if reached != members:
                valid = False
                break
        if valid:
            good.append(assignment)
    return good


def test_02_false_infeasibility_minimal_reproducer():
    # Protect (0,1) and (0,2). Feasible k=2: {0}, {1,2,3}.
    edges = ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3))
    protected = {(0, 1), (0, 2)}
    assert (0, 1, 1, 1) in _feasible_partitions(4, 2, edges, protected)
    names = tuple(f"v{i}" for i in range(4))
    g = grid(names, [Edge(f"e{i}{j}", names[i], names[j]) for i, j in edges])
    costs = {"e01": 7., "e02": 4., "e03": 0.,
             "e13": 7., "e23": 0.}
    # BUG REPRODUCER: greedy commits to {0,3}; then both protected
    # 0-1 and 0-2 prevent reaching 2 zones, despite the feasible witness.
    with pytest.raises(CountryContractError, match="Cannot meet exact quotas"):
        quota_seed(g, ("X",) * 4, CountryZoneBudget.synthetic({"X": 2}),
                   merge_cost_by_branch=costs,
                   protected_line_ids={"e01", "e02"})


def test_03_exhaustive_n4_finds_false_infeasibility_and_no_invalid_passes():
    # 3 states per possible edge: absent, ordinary, protected.
    # All 3**6 = 729 simple undirected labelled topologies;
    # all quotas k=1..4; canonical partitions enumerate all solutions.
    pairs = tuple(combinations(range(4), 2))
    names = tuple(f"n{i}" for i in range(4))
    valid_instances = 0
    false_blocked = 0
    for states in product((0, 1, 2), repeat=len(pairs)):
        active = [(i, j, state) for (i, j), state
                  in zip(pairs, states) if state != 0]
        if not active:
            continue
        graph_edges = [(i, j) for i, j, _ in active]
        protected_pairs = {(i, j) for i, j, s in active if s == 2}
        branches = [Edge(f"e{i}{j}", names[i], names[j])
                    for i, j, _ in active]
        g = grid(names, branches)
        costs = {b.identifier: float(index + 1)
                 for index, b in enumerate(branches)}
        protected_ids = {f"e{i}{j}" for i, j in protected_pairs}
        for k in range(1, 5):
            feasible = _feasible_partitions(4, k, graph_edges, protected_pairs)
            if not feasible:
                continue
            valid_instances += 1
            budget = CountryZoneBudget.synthetic({"X": k})
            try:
                actual = quota_seed(g, ("X",) * 4, budget,
                                    merge_cost_by_branch=costs,
                                    protected_line_ids=protected_ids)
            except CountryContractError:
                false_blocked += 1
            else:
                # The core safety invariants MUST hold even if the heuristic
                # does not find an optimum.
                validate_busmap(g, actual.zone_of_bus, ("X",) * 4,
                                budget, protected_ids)
    print(f"R-CLU exhaustive oracle: {valid_instances=}, {false_blocked=}")
    # Frozen-commit defect measurement, NOT a desired property.
    assert valid_instances == 1804
    assert false_blocked == 10


def test_04_two_islands_country_quota_and_110kv_gap():
    names = ("a", "b", "c", "d")
    g = grid(names, (Edge("ab", "a", "b"), Edge("cd", "c", "d")))
    with pytest.raises(CountryContractError, match="underbudgeted"):
        quota_seed(g, ("X",) * 4, CountryZoneBudget.synthetic({"X": 1}),
                   merge_cost_by_branch={"ab": 0., "cd": 0.})
    result = quota_seed(g, ("X",) * 4, CountryZoneBudget.synthetic({"X": 2}),
                        merge_cost_by_branch={"ab": 0., "cd": 0.})
    assert len(set(result.zone_of_bus)) == 2
    with pytest.raises(CountryContractError, match="110-kV"):
        quota_seed(grid(names, g.active_branches, gap=True), ("X",) * 4,
                   CountryZoneBudget.synthetic({"X": 2}),
                   merge_cost_by_branch={"ab": 0., "cd": 0.})


def test_05_country_purity_ni_uk_and_crossborder_ties():
    names = ("ni0", "ni1", "uk0", "uk1", "fr0", "fr1")
    edges = (
        Edge("ni", "ni0", "ni1"), Edge("uk", "uk0", "uk1"),
        Edge("fr", "fr0", "fr1"),
        Edge("ni_uk", "ni1", "uk0"),
        Edge("uk_ni", "uk1", "ni0"),
        Edge("uk_fr", "uk1", "fr0"),
        Edge("ni_fr", "ni0", "fr1"),
    )
    g = grid(names, edges, ("NI", "NI", "UK", "UK", "FR", "FR"))
    budget = CountryZoneBudget.synthetic({
        "Northern Ireland": 1, "United Kingdom": 1, "France": 1})
    labels = resolve_country_ids(g, {
        "NI": "Northern Ireland", "UK": "United Kingdom", "FR": "France"}, budget)
    seed = quota_seed(g, labels, budget,
                      merge_cost_by_branch={e.identifier: 0. for e in edges})
    assert len(set(seed.zone_of_bus)) == 3
    assert set(seed.retained_cross_country_branch_ids) == {
        "ni_uk", "uk_ni", "uk_fr", "ni_fr"}
    with pytest.raises(CountryContractError, match="many-to-one"):
        resolve_country_ids(g, {
            "NI": "United Kingdom", "UK": "United Kingdom", "FR": "France"}, budget)


def test_06_oriented_projection_independent_sign_matrix_and_counterflow():
    names = ("a", "b", "c", "d")
    edges = (Edge("internal_a", "a", "b"),
             Edge("forward", "a", "c"),
             Edge("reverse", "d", "b"),
             Edge("forward2", "b", "c"),
             Edge("internal_b", "c", "d"))
    g = grid(names, edges)
    p = build_oriented_projection(g, ("ZA", "ZA", "ZB", "ZB"))
    np.testing.assert_array_equal(p.Gamma.toarray(), [[0., 1., -1., 1., 0.]])
    np.testing.assert_array_equal(p.A_z.toarray(), [[1.], [-1.]])
    np.testing.assert_array_equal(
        (p.A_z @ p.Gamma).toarray(), (p.P @ p.A_d).toarray())
    f = np.array([[3., 0.], [30., 30.], [30., 30.],
                  [2., 2.], [-5., -5.]])
    cache = SimpleNamespace(
        branch_ids=p.branch_ids, bus_ids=p.bus_ids,
        snapshot_ids=("t0", "t1"), flow_mw=f, nodal_net_mw=p.A_d @ f)
    assert p.verify(cache)
    np.testing.assert_allclose(p.Gamma @ f, [[2., 2.]])
    events = p.counterflow_ledger(cache)
    assert len(events) == 2
    assert all(x["cancelled_absolute_MW"] == 60. for x in events)
    assert all(x["net_MW"] == 2. for x in events)


def test_07_exact_annual_mwh_variable_limits_and_voltage_class():
    branches = (
        Edge("l400", "a", "b", 400.),
        Edge("l220", "a", "b", 220., screening_class_kv=225.),
        Edge("l380", "a", "b", 380., screening_class_kv=400.),
        Edge("l110", "a", "b", 110.),
        Edge("trafo", "a", "b", 400., kind="transformer"),
    )
    g = grid(("a", "b"), branches)
    years = tuple(f"Y{i}" for i in range(5))
    time = SimpleNamespace(
        snapshot_ids=tuple(f"t{i}" for i in range(10)),
        year_for_snapshot=tuple(y for y in years for _ in range(2)),
        weather_year_ids=years,
        duration_hours=np.array([1., 3.] * 5))
    flow = np.zeros((5, 10))
    flow[0] = [12., -20.] * 5
    flow[1] = [11., 8.] * 5
    flow[2] = [9., 15.] * 5
    flow[3] = [100., 100.] * 5
    flow[4] = [100., 100.] * 5
    cache = SimpleNamespace(
        branch_ids=tuple(b.identifier for b in branches),
        bus_ids=g.bus_ids, snapshot_ids=time.snapshot_ids,
        flow_mw=flow, neutral_calibration=False)
    ratings = SimpleNamespace(
        snapshot_ids=time.snapshot_ids,
        normal_mw={b.identifier: np.array([10., 18.] * 5)
                   for b in branches})
    result = screen_annual_overload(g, cache, time, ratings)
    assert set(result.screened_line_ids) == {"l400", "l220", "l380"}
    assert [result.year_score("l400", y) for y in years] == [8.] * 5
    assert [result.year_score("l220", y) for y in years] == [1.] * 5
    row = next(x for x in result.rows
               if x["year_id"] == "Y0" and x["line_id"] == "l400")
    assert (row["overload_hours"], row["observation_hours"]) == (4., 4.)
    assert next(x["voltage_kv"] for x in result.rows
                if x["line_id"] == "l380") == 400.
    assert weighted_edge_costs(result, g, dict.fromkeys(years, 1.))["l400"] == 40.
    ambiguous = grid(g.bus_ids, (Edge("ambiguous", "a", "b", 220.),))
    with pytest.raises(ScreeningError, match="explicit screening_class_kv"):
        screen_annual_overload(
            ambiguous,
            SimpleNamespace(branch_ids=("ambiguous",), bus_ids=g.bus_ids,
                            snapshot_ids=time.snapshot_ids, flow_mw=flow[:1],
                            neutral_calibration=False),
            time, SimpleNamespace(snapshot_ids=time.snapshot_ids,
                                  normal_mw={"ambiguous": np.array([10., 18.] * 5)}))


def test_08_400kv_zero_class_can_silently_omit_normative_line_reproducer():
    # Known audit issue: declared class 0 excludes even an exact 400-kV line.
    # This asserts frozen behavior; it is NOT methodological approval.
    branch = Edge("400_protected", "a", "b", 400.,
                  screening_class_kv=0.)
    g = grid(("a", "b"), (branch,))
    years = tuple(f"Y{i}" for i in range(5))
    time = SimpleNamespace(snapshot_ids=tuple(f"t{i}" for i in range(5)),
                           year_for_snapshot=years, weather_year_ids=years,
                           duration_hours=np.ones(5))
    cache = SimpleNamespace(branch_ids=("400_protected",), bus_ids=g.bus_ids,
                            snapshot_ids=time.snapshot_ids,
                            flow_mw=np.full((1, 5), 100.),
                            neutral_calibration=False)
    ratings = SimpleNamespace(
        snapshot_ids=time.snapshot_ids,
        normal_mw={"400_protected": np.full(5, 10.)})
    result = screen_annual_overload(g, cache, time, ratings)
    assert result.screened_line_ids == ()
    assert result.rows == ()


def test_09_generator_protected_ids_changes_input_hash_reproducer():
    # Same protection and same output, but one-shot iterators are consumed by
    # quota_seed before execute_ma1 constructs its own manifest fingerprint.
    from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture
    from tyndp_reduce.iosn_official.ma1 import execute_ma1

    args = build_synthetic_fixture()
    with_tuple = execute_ma1(*args, protected_line_ids=("d12",))
    with_generator = execute_ma1(*args, protected_line_ids=(x for x in ("d12",)))
    assert with_tuple.seed.zone_of_bus == with_generator.seed.zone_of_bus
    assert with_tuple.seed.protected_line_ids == with_generator.seed.protected_line_ids
    # BUG REPRODUCER: logically identical input yields different fingerprint.
    assert with_tuple.input_manifest_sha256 != with_generator.input_manifest_sha256


def test_10_source_page_for_uk_is_not_checked_against_original_pdf_reproducer(tmp_path):
    from tyndp_reduce.iosn_official.country import load_official_country_budget

    original = (Path(__file__).resolve().parents[2] / "docs" / "current"
                / "IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv").read_text()
    assert "United Kingdom,1,27" in original
    modified = original.replace("United Kingdom,1,27", "United Kingdom,1,26")
    path = tmp_path / "falsified_source_page.csv"
    path.write_text(modified, encoding="utf-8")
    # BUG REPRODUCER: original source page 27 can be falsified as page 26.
    assert dict(load_official_country_budget(path).quotas) == TABLE3
