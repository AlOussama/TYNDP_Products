"""W-CLU RP1: protected-cut bounded feasibility, screening and provenance."""
from dataclasses import dataclass
from itertools import combinations, product
from types import SimpleNamespace
from pathlib import Path
from dataclasses import replace
import numpy as np
import pytest

from tyndp_reduce.iosn_official.country import (
    CountryZoneBudget, CountryContractError, load_official_country_budget,
    validate_busmap, canonicalize_country_aliases,
)
from tyndp_reduce.iosn_official.seed import quota_seed, QuotaFeasibilityError
from tyndp_reduce.iosn_official.screen import screen_annual_overload, ScreeningError
from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture
from tyndp_reduce.iosn_official.ma1 import execute_ma1


@dataclass(frozen=True)
class E:
    identifier: str
    bus0: str
    bus1: str
    voltage_kv: float = 225.
    kind: str = "line"
    screening_class_kv: float | None = None


def graph(nodes, edges, raw=None):
    return SimpleNamespace(bus_ids=tuple(nodes), raw_country_ids=tuple(raw or ("X",) * len(nodes)),
                           active_branches=tuple(edges), incomplete_110kv_ties=False)


def partitions(n):
    assignment = [0] * n
    def walk(pos, max_label):
        if pos == n:
            yield tuple(assignment)
        else:
            for label in range(max_label + 2):
                assignment[pos] = label
                yield from walk(pos + 1, max(max_label, label))
    yield from walk(1, 0)


def oracle_feasible(n, k, edges, protected):
    for a in partitions(n):
        if len(set(a)) != k or any(a[i] == a[j] for i, j in protected):
            continue
        valid = True
        for z in range(k):
            group = {i for i in range(n) if a[i] == z}
            visited = {min(group)}
            while True:
                newer = visited | {v for u, v in edges if u in visited and v in group} | {
                    u for u, v in edges if v in visited and u in group}
                if newer == visited: break
                visited = newer
            if visited != group:
                valid = False
                break
        if valid: return True
    return False


def test_729_graphs_1804_feasible_no_false_infeasible():
    pairs = tuple(combinations(range(4), 2))
    nodes = tuple(f"v{i}" for i in range(4))
    feasible, false_blocked, invalid_passes = 0, 0, 0
    for states in product((0, 1, 2), repeat=6):
        active = [(i, j, state) for (i, j), state in zip(pairs, states) if state]
        if not active: continue
        edges = [(i, j) for i, j, _ in active]
        locks = {(i, j) for i, j, s in active if s == 2}
        branches = tuple(E(f"e{i}{j}", nodes[i], nodes[j]) for i, j, _ in active)
        costs = {b.identifier: float(j + 1) for j, b in enumerate(branches)}
        protected = {f"e{i}{j}" for i, j in locks}
        g = graph(nodes, branches)
        for k in range(1, 5):
            if not oracle_feasible(4, k, edges, locks): continue
            feasible += 1
            budget = CountryZoneBudget.synthetic({"X": k})
            try:
                result = quota_seed(g, ("X",) * 4, budget,
                                    merge_cost_by_branch=costs,
                                    protected_line_ids=protected)
            except CountryContractError:
                false_blocked += 1
            else:
                try:
                    validate_busmap(g, result.zone_of_bus, ("X",) * 4, budget, protected)
                except CountryContractError:
                    invalid_passes += 1
    assert feasible == 1804
    assert false_blocked == 0
    assert invalid_passes == 0


def test_original_protected_merges_recover_feasible_partition():
    nodes = tuple(f"v{i}" for i in range(4))
    links = [(0, 1, 7., True), (0, 2, 4., True), (0, 3, 0., False),
             (1, 3, 7., False), (2, 3, 0., False)]
    branches = tuple(E(f"e{i}{j}", nodes[i], nodes[j]) for i, j, _, _ in links)
    costs = {f"e{i}{j}": c for i, j, c, _ in links}
    g = graph(nodes, branches)
    r = quota_seed(g, ("X",)*4, CountryZoneBudget.synthetic({"X":2}),
                   merge_cost_by_branch=costs, protected_line_ids=("e01","e02"))
    groups = {z: set() for z in r.zone_of_bus}
    for i, z in enumerate(r.zone_of_bus): groups[z].add(nodes[i])
    assert set(map(frozenset, groups.values())) == {frozenset({"v0"}), frozenset({"v1","v2","v3"})}
    assert any(m.get("feasibility_method") == "BOUNDED_EXACT_FALLBACK" for m in r.merge_ledger)


def test_proven_impossible_and_resource_bound_are_distinct():
    n = ("a", "b", "c")
    g = graph(n, (E("ab", "a", "b"), E("bc", "b", "c")))
    with pytest.raises(QuotaFeasibilityError) as exc:
        quota_seed(g, ("X",)*3, CountryZoneBudget.synthetic({"X":1}),
                   merge_cost_by_branch={"ab": 1., "bc": 1.},
                   protected_line_ids=("ab", "bc"))
    assert exc.value.status == "PROVEN_INFEASIBLE"


def test_p2_protected_generator_has_identical_manifest_identity():
    args = build_synthetic_fixture()
    tuple_obj = execute_ma1(*args, protected_line_ids=("d12",))
    gen_obj = execute_ma1(*args, protected_line_ids=(x for x in ("d12",)))
    assert tuple_obj.seed.zone_of_bus == gen_obj.seed.zone_of_bus
    assert tuple_obj.input_manifest_sha256 == gen_obj.input_manifest_sha256
    with pytest.raises(CountryContractError, match="Duplicate"):
        execute_ma1(*args, protected_line_ids=("d12", "d12"))


def test_uk_source_page_forgery_rejected(tmp_path):
    original = Path("docs/current/IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv").read_text()
    assert "United Kingdom,1,27" in original
    p = tmp_path / "wrong.csv"
    p.write_text(original.replace("United Kingdom,1,27", "United Kingdom,1,26"))
    with pytest.raises(CountryContractError, match="source page"):
        load_official_country_budget(p)


def test_400kv_cannot_silently_hide_90mwh_per_year():
    years = tuple(f"Y{i}" for i in range(5))
    time = SimpleNamespace(snapshot_ids=years, year_for_snapshot=years,
                           weather_year_ids=years, duration_hours=np.ones(5))
    flow = SimpleNamespace(branch_ids=("l400",), bus_ids=("a","b"),
                           snapshot_ids=years, flow_mw=np.full((1,5), 100.),
                           neutral_calibration=False)
    ratings = SimpleNamespace(snapshot_ids=years,
                              normal_mw={"l400": np.full(5,10.)})
    excluded = graph(("a","b"), (E("l400","a","b",400.,screening_class_kv=0.),))
    with pytest.raises(ScreeningError, match="exclusion"):
        screen_annual_overload(excluded, flow, time, ratings)
    eligible = graph(("a","b"), (E("l400","a","b",400.),))
    result = screen_annual_overload(eligible, flow, time, ratings)
    assert result.screened_line_ids == ("l400",)
    assert [result.year_score("l400",y) for y in years] == [90.] * 5


def test_m2_opt_in_alias_canonicalization_keeps_ni_and_uk_disjoint():
    budget = CountryZoneBudget.synthetic({"Germany": 1, "Northern Ireland": 1,
                                          "United Kingdom": 1})
    records = {
        "DE-1": {"country_label":"Germany", "source_uri":"test://de/1","source_sha256":"0"*64},
        "DE-2": {"country_label":"Germany", "source_uri":"test://de/2","source_sha256":"1"*64},
        "NI": {"country_label":"Northern Ireland", "source_uri":"test://ni","source_sha256":"2"*64},
        "UK": {"country_label":"United Kingdom", "source_uri":"test://uk","source_sha256":"3"*64},
    }
    witness = canonicalize_country_aliases(("DE-1","DE-2","NI","UK"), records, budget)
    assert witness.normalized_raw_ids == ("Germany","Germany","Northern Ireland","United Kingdom")
    assert dict(witness.explicit_country_map) == {
        "Germany":"Germany","Northern Ireland":"Northern Ireland","United Kingdom":"United Kingdom"}
    wrong = {key: dict(v) for key,v in records.items()}
    wrong["NI"]["country_label"] = "United Kingdom"
    with pytest.raises(CountryContractError, match="merging"):
        canonicalize_country_aliases(("DE-1","DE-2","NI","UK"), wrong, budget)


def test_multi_country_large_fixture_keeps_protected_boundaries():
    nodes = ("a0","a1","a2","a3","a4","a5", "uk0","uk1","ni0","ni1")
    links = [E(f"a{i}{i+1}",f"a{i}",f"a{i+1}") for i in range(5)]
    links += [E("a05","a0","a5"), E("uk","uk0","uk1"),
              E("ni","ni0","ni1"), E("cross_uk_ni","uk1","ni0"),
              E("cross_ni_a","ni1","a0")]
    labels = ("Germany",)*6 + ("United Kingdom",)*2 + ("Northern Ireland",)*2
    budget = CountryZoneBudget.synthetic({"Germany":2,"United Kingdom":1,"Northern Ireland":1})
    g = graph(nodes, links, labels)
    result = quota_seed(g, labels, budget,
                        merge_cost_by_branch={e.identifier:1. for e in links},
                        protected_line_ids=("a05","cross_uk_ni"))
    assert result.quota_counts == dict(budget.quotas)
    validate_busmap(g, result.zone_of_bus, labels, budget, ("a05","cross_uk_ni"))
