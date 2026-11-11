"""CLU worker: official budget, exact country quotas, MWh and oriented cuts."""
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pytest

from tyndp_reduce.iosn_official.country import (
    CountryZoneBudget, CountryContractError, load_official_country_budget,
    resolve_country_ids, validate_busmap,
)
from tyndp_reduce.iosn_official.seed import quota_seed
from tyndp_reduce.iosn_official.screen import (
    screen_annual_overload, weighted_edge_costs, ScreeningError,
)
from tyndp_reduce.iosn_official.operators import build_oriented_projection


@dataclass(frozen=True)
class Branch:
    identifier: str
    bus0: str
    bus1: str
    voltage_kv: float
    kind: str = "line"
    screening_class_kv: float | None = None


def graph():
    # Cross-country physical ties remain in this continental graph.
    edges = (
        Branch("de01", "d0", "d1", 225),
        Branch("critical", "d1", "d2", 400),
        Branch("de23", "d2", "d3", 225),
        Branch("de30_110", "d3", "d0", 110),
        Branch("fr01", "f0", "f1", 225),
        Branch("de_fr_1", "d1", "f0", 400),
        Branch("fr_de_2", "f1", "d0", 400),
        Branch("fr_ni", "f1", "n0", 400),
        Branch("not_screened_trafo", "d0", "d2", 400, "transformer"),
    )
    g = SimpleNamespace(
        bus_ids=("d0", "d1", "d2", "d3", "f0", "f1", "n0"),
        raw_country_ids=("DE", "DE", "DE", "DE", "FR", "FR", "NI"),
        active_branches=edges, incomplete_110kv_ties=False,
    )
    budget = CountryZoneBudget.synthetic({"Germany": 2, "France": 1,
                                          "Northern Ireland": 1})
    mapping = {"DE": "Germany", "FR": "France", "NI": "Northern Ireland"}
    labels = resolve_country_ids(g, mapping, budget)
    return g, budget, labels


def test_official_csv_exact_37_102_and_distinct_ni_uk():
    official = load_official_country_budget()
    assert official.official
    assert len(official.quotas) == 37
    assert sum(official.quotas.values()) == 102
    assert official.quotas["Northern Ireland"] == 1
    assert official.quotas["United Kingdom"] == 1
    assert official.quotas["Germany"] == 11
    assert official.quotas["France"] == 16


def test_budget_cannot_forge_37_label_counts():
    altered = dict(load_official_country_budget().quotas)
    altered["Germany"] = 12
    altered["France"] = 15
    with pytest.raises(CountryContractError, match="exactly"):
        CountryZoneBudget(altered, True, "0" * 64)
    with pytest.raises(CountryContractError, match="Full official"):
        g, _, _ = graph()
        resolve_country_ids(g, {"DE": "Germany", "FR": "France",
                                "NI": "Northern Ireland"},
                            load_official_country_budget())


def test_country_exact_quota_connected_and_crossborder_preserved():
    g, budget, labels = graph()
    costs = {b.identifier: (100.0 if b.identifier == "critical" else 0.)
             for b in g.active_branches}
    result = quota_seed(g, labels, budget,
                        merge_cost_by_branch=costs, protected_line_ids={"critical"})
    assert result.quota_counts == {"Germany": 2, "France": 1, "Northern Ireland": 1}
    assert len(set(result.zone_of_bus)) == 4
    assert "critical" in result.protected_line_ids
    assert {"de_fr_1", "fr_de_2", "fr_ni"}.issubset(
        set(result.retained_cross_country_branch_ids))
    assert validate_busmap(g, result.zone_of_bus, labels, budget,
                           {"critical"}) == result.quota_counts
    assert len(result.merge_ledger) == len(g.bus_ids) - sum(budget.quotas.values())
    assert quota_seed(g, labels, budget, merge_cost_by_branch=costs,
                      protected_line_ids={"critical"}).zone_of_bus == result.zone_of_bus
    projection = build_oriented_projection(g, result.zone_of_bus)
    assert projection.verify()
    assert set(projection.branch_ids) == {b.identifier for b in g.active_branches}


def test_critical_internal_swallow_rejected():
    g, _, labels = graph()
    budget = CountryZoneBudget.synthetic({"Germany": 1, "France": 1,
                                          "Northern Ireland": 1})
    busmap = ("DE", "DE", "DE", "DE", "FR", "FR", "NI")
    with pytest.raises(CountryContractError, match="swallowed"):
        validate_busmap(g, busmap, labels, budget, {"critical"})


def test_bad_country_map_mixed_cluster_and_quota():
    g, budget, labels = graph()
    with pytest.raises(CountryContractError, match="every raw|Every raw"):
        resolve_country_ids(g, {"DE": "Germany", "FR": "France"}, budget)
    with pytest.raises(CountryContractError, match="many-to-one"):
        resolve_country_ids(g, {"DE": "Germany", "FR": "Germany",
                                "NI": "Northern Ireland"}, budget)
    with pytest.raises(CountryContractError, match="Mixed-country"):
        validate_busmap(g, ("mix", "mix", "de", "de", "mix", "fr", "ni"),
                        labels, budget)
    with pytest.raises(CountryContractError, match="quotas"):
        validate_busmap(g, ("de", "de", "de", "de", "fr", "fr", "ni"),
                        labels, budget)


def test_underbudgeted_disconnected_country_and_incomplete_ties():
    g, budget, labels = graph()
    edges = tuple(b for b in g.active_branches
                  if b.identifier not in {"critical", "de23", "de30_110",
                                          "not_screened_trafo"})
    detached = SimpleNamespace(bus_ids=g.bus_ids, raw_country_ids=g.raw_country_ids,
                               active_branches=edges, incomplete_110kv_ties=False)
    with pytest.raises(CountryContractError, match="underbudgeted"):
        quota_seed(detached, labels, budget,
                   merge_cost_by_branch={x.identifier: 0. for x in edges})
    incomplete = SimpleNamespace(bus_ids=g.bus_ids,
                                 raw_country_ids=g.raw_country_ids,
                                 active_branches=g.active_branches,
                                 incomplete_110kv_ties=True)
    with pytest.raises(CountryContractError, match="110-kV"):
        quota_seed(incomplete, labels, budget, merge_cost_by_branch=None)


def test_unreachable_quota_due_to_protected_merges():
    g, budget, labels = graph()
    costs = {b.identifier: 0. for b in g.active_branches}
    with pytest.raises(CountryContractError, match="Cannot meet"):
        quota_seed(g, labels, budget, merge_cost_by_branch=costs,
                   protected_line_ids={"de01", "critical", "de23", "de30_110",
                                       "not_screened_trafo"})


def test_screen_exact_annual_225_400_mwh_seasonal_ratings():
    g, _, _ = graph()
    ids = tuple(f"t{i}" for i in range(5))
    years = tuple(f"W{i}" for i in range(5))
    time = SimpleNamespace(snapshot_ids=ids, year_for_snapshot=years,
                           weather_year_ids=years, duration_hours=np.array([1., 2., 3., 1., 1.]),
                           season=("winter", "summer", "winter", "summer", "winter"))
    f = np.zeros((len(g.active_branches), 5))
    f[1] = [15., 8., -18., 20., 2.]
    f[3] = [100.] * 5                  # 110-kV excluded
    f[-1] = [100.] * 5                 # 400-kV transformer excluded
    flow_cache = SimpleNamespace(bus_ids=g.bus_ids, snapshot_ids=ids,
                                 branch_ids=tuple(x.identifier for x in g.active_branches),
                                 flow_mw=f, neutral_calibration=False)
    normal = {x.identifier: np.full(5, 50.) for x in g.active_branches}
    normal["critical"] = np.array([10., 10., 15., 12., 3.])
    ratings = SimpleNamespace(snapshot_ids=ids, normal_mw=normal)
    score = screen_annual_overload(g, flow_cache, time, ratings)
    assert "de30_110" not in score.screened_line_ids
    assert "not_screened_trafo" not in score.screened_line_ids
    assert [score.year_score("critical", y) for y in years] == [5., 0., 9., 8., 0.]
    assert next(row["overload_hours"] for row in score.rows if row["year_id"] == "W2"
                and row["line_id"] == "critical") == 3.0
    weighted = weighted_edge_costs(score, g, {y: 1 for y in years})
    assert weighted["critical"] == 22.
    assert weighted["de30_110"] == 0.
    with pytest.raises(ScreeningError, match="weights"):
        weighted_edge_costs(score, g, {"W1": 1})


def test_projection_balances_oriented_counterflows_without_dropping_ties():
    g, budget, labels = graph()
    result = quota_seed(g, labels, budget,
                        merge_cost_by_branch={b.identifier: 0. for b in g.active_branches})
    projection = build_oriented_projection(g, result.zone_of_bus)
    flow = np.zeros((len(g.active_branches), 2))
    k = {b.identifier: i for i, b in enumerate(g.active_branches)}
    flow[k["de_fr_1"]] = 30.
    flow[k["fr_de_2"]] = 30.  # opposed in global zone-pair orientation
    net = projection.A_d @ flow
    fake_cache = SimpleNamespace(branch_ids=projection.branch_ids,
                                 bus_ids=projection.bus_ids,
                                 snapshot_ids=("t0", "t1"),
                                 flow_mw=flow, nodal_net_mw=net)
    assert projection.verify(fake_cache)
    pz, fc = projection.aggregate(fake_cache)
    np.testing.assert_allclose(projection.A_z @ fc, pz, atol=1e-12)
    diag = projection.counterflow_ledger(fake_cache)
    assert any(row["cancelled_absolute_MW"] == 60. for row in diag)
    assert any(row["net_MW"] == 0 for row in diag)


def test_protected_input_or_missing_scores_cannot_be_silently_fixed():
    g, budget, labels = graph()
    with pytest.raises(CountryContractError, match="Missing/extra"):
        quota_seed(g, labels, budget, merge_cost_by_branch={"critical": 1})
    with pytest.raises(CountryContractError, match="not an active"):
        quota_seed(g, labels, budget, merge_cost_by_branch=None,
                   protected_line_ids={"invented"})


def test_nonstandard_380kv_requires_explicit_400kv_screening_class():
    from dataclasses import replace
    g, _, _ = graph()
    new_branches = tuple(
        replace(branch, voltage_kv=380.) if branch.identifier == "critical" else branch
        for branch in g.active_branches
    )
    amended = SimpleNamespace(bus_ids=g.bus_ids, raw_country_ids=g.raw_country_ids,
                              active_branches=new_branches, incomplete_110kv_ties=False)
    ids = tuple(f"x{i}" for i in range(5))
    years = tuple(f"Y{i}" for i in range(5))
    time = SimpleNamespace(snapshot_ids=ids, year_for_snapshot=years,
                           weather_year_ids=years,
                           duration_hours=np.ones(5),
                           season=("winter",) * 5)
    flows = np.zeros((len(new_branches), 5))
    flows[1] = [12., 12., 12., 12., 12.]
    cache = SimpleNamespace(bus_ids=g.bus_ids, snapshot_ids=ids,
                            branch_ids=tuple(b.identifier for b in new_branches),
                            flow_mw=flows, neutral_calibration=False)
    ratings = SimpleNamespace(
        snapshot_ids=ids, normal_mw={b.identifier: np.full(5, 10.) for b in new_branches})
    with pytest.raises(ScreeningError, match="explicit screening_class_kv"):
        screen_annual_overload(amended, cache, time, ratings)
    clarified = tuple(
        replace(b, screening_class_kv=400.) if b.identifier == "critical" else b
        for b in new_branches
    )
    amended.active_branches = clarified
    screened = screen_annual_overload(amended, cache, time, ratings)
    assert "critical" in screened.screened_line_ids
    assert screened.year_score("critical", "Y0") == 2.
    relevant = next(row for row in screened.rows if row["line_id"] == "critical")
    assert relevant["voltage_kv"] == 400.
    assert relevant["nominal_voltage_kv"] == 380.
