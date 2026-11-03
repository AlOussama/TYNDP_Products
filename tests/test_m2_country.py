"""W-CLU / M2-MA1 deterministic quota, screening, projection and negative gates."""
from dataclasses import replace

import numpy as np
import pytest

from tyndp_reduce.m2.contracts import (
    Bus, ACBranch, DetailedGridSnapshot, HVDCTerminalPair, Evidence,
    CountryZoneBudget, TimeSet, TimePoint, ReferenceDispatchSet,
    NormalContingencyRatings, PSTDispatch, ContractError
)
from tyndp_reduce.m2.country import (
    load_official_budget, country_quota_busmap, assert_country_zones,
    validate_country_feasibility
)
from tyndp_reduce.m2.physical import SparseACReference
from tyndp_reduce.m2.screening import screen_annual_overload, protect_congested_union
from tyndp_reduce.m2.projection import build_oriented_projection
from tyndp_reduce.m2.preflight import preflight_ledger, save_ledger_once

from test_m2_physical import ev, island_case, yearset


def budget():
    return CountryZoneBudget(ev("quota"), (("Germany", 2), ("France", 1)), official=False)


def ratings():
    return NormalContingencyRatings(
        ev("ratings"), ("ab","bc","de"), ("t0","t1"),
        ((40.,40.),(8.,15.),(10.,20.)),
        contingency_MW=((45.,45.),(12.,20.),(18.,25.)))


def test_published_csv_37_entries_102_exact_and_northern_ireland_distinct():
    b = load_official_budget()
    assert len(b.quotas) == 37
    assert sum(b.by_label.values()) == 102
    assert b.by_label["Northern Ireland"] == 1
    assert b.by_label["United Kingdom"] == 1
    assert b.by_label["Germany"] == 11
    assert b.by_label["France"] == 16


def test_quota_csv_corruption_rejected_even_when_most_entries_valid(tmp_path):
    b = load_official_budget()
    original = open(b.evidence.source, encoding="utf-8").read()
    forged = tmp_path / "quota.csv"
    forged.write_text(original.replace("Germany,11,26", "Germany,10,26"), encoding="utf-8")
    with pytest.raises(ContractError, match="pinned"):
        load_official_budget(forged)


def test_unknown_country_label_without_hidden_alias():
    grid,_,_=island_case()
    altered = replace(grid, buses=tuple(replace(b, country="Deutschland")
                              if b.name=="a" else b for b in grid.buses))
    with pytest.raises(ContractError, match="country-label coverage"):
        validate_country_feasibility(altered,budget())


def test_impossible_quota_from_disconnected_country_islands():
    grid=DetailedGridSnapshot(
        ev("alternating"),100.,
        (Bus("a","Germany",225),Bus("x","France",225),Bus("b","Germany",225)),
        (ACBranch("ax","a","x",.2,225),
         ACBranch("xb","x","b",.2,225)),
        ties_110kv_complete=True, fixture=True)
    b=CountryZoneBudget(ev("alt-budget"),(("Germany",1),("France",1)))
    with pytest.raises(ContractError, match="infeasible country quota"):
        country_quota_busmap(grid,b,np.ones(2))


def test_country_quota_merge_is_deterministic_and_protects_critical_line():
    grid,_,_=island_case()
    z1=country_quota_busmap(grid,budget(),[2.,3.,4.],protected=("bc",))
    z2=country_quota_busmap(grid,budget(),[2.,3.,4.],protected=("bc",))
    assert z1==z2
    assert z1[0]==z1[1] and z1[1]!=z1[2]
    assert z1[3]==z1[4]
    assert len(set(z1))==3
    assert_country_zones(grid,budget(),z1,protected=("bc",))


def test_negative_mixed_zone_and_swallowed_critical_line():
    grid,_,_=island_case()
    with pytest.raises(ContractError,match="mixed-country"):
        assert_country_zones(grid,budget(),(0,0,1,1,2))
    with pytest.raises(ContractError,match="critical physical line swallowed"):
        assert_country_zones(grid,budget(),(0,1,1,2,2),protected=("bc",))


def test_protected_cut_with_too_few_available_quota_is_rejected():
    grid,_,_=island_case()
    # Germany 2 zones but both internal edges are protected -> at least 3 zones.
    with pytest.raises(ContractError,match="quota cannot be met"):
        country_quota_busmap(grid,budget(),np.zeros(3),protected=("ab","bc"))


def test_hourly_summer_winter_limits_and_separate_years_mwh():
    grid,times,q=island_case()
    cache=SparseACReference(grid).solve(q,times)
    scores=screen_annual_overload(grid,times,ratings(),cache)
    assert set(scores)=={"wyA","wyB"}
    a={row["branch_id"]:row for row in scores["wyA"]}
    b={row["branch_id"]:row for row in scores["wyB"]}
    assert set(a)=={"bc","de"}  # 220 kV transformer is not screened
    assert a["bc"]["overload_MWh"]==pytest.approx(4.)
    assert a["de"]["overload_MWh"]==pytest.approx(10.)
    assert a["bc"]["overload_hours"]==pytest.approx(2.)
    assert b["bc"]["overload_MWh"]==pytest.approx(0.)
    assert b["de"]["overload_MWh"]==pytest.approx(0.)
    assert protect_congested_union(scores)==frozenset({"bc","de"})


def test_missing_hourly_limit_mva_and_time_mismatch_fail_closed():
    grid,times,q=island_case()
    cache=SparseACReference(grid).solve(q,times)
    with pytest.raises(ContractError,match="MVA/A"):
        replace(ratings(),unit="MVA")
    r=replace(ratings(),normal_MW=((40.,40.),(float("nan"),15.),(10.,20.)))
    with pytest.raises(ContractError,match="invalid hourly normal"):
        screen_annual_overload(grid,times,r,cache)
    r=replace(ratings(),time_keys=("wrong","t1"))
    with pytest.raises(ContractError,match="not aligned"):
        screen_annual_overload(grid,times,r,cache)


def test_sparse_projection_p_gamma_az_and_hvdc_net_injections():
    grid,times,q=island_case()
    model=SparseACReference(grid)
    cache=model.solve(q,times)
    z=country_quota_busmap(grid,budget(),[2.,3.,4.],protected=("bc",))
    projection=build_oriented_projection(model,budget(),z,protected=("bc",))
    pz,cut=projection.verify(model,cache)
    np.testing.assert_allclose(projection.A_z@cut,pz,atol=1e-9)
    # The 10-MW HVDC injection changes p_net; no artificial AC HVDC edge.
    np.testing.assert_allclose(pz.sum(axis=0),0.,atol=1e-9)
    assert "bc" in [name for group in projection.grouped_branch_ids for name in group]
    assert "dc" not in [name for group in projection.grouped_branch_ids for name in group]


def test_european_ac_cross_border_edge_is_retained_not_two_country_slacks():
    grid=DetailedGridSnapshot(
        ev("cross-country"),100.,
        (Bus("a","Germany",225),Bus("b","Germany",225),Bus("c","France",225)),
        (ACBranch("ab","a","b",.1,225),
         ACBranch("bc","b","c",.2,225)),
        ties_110kv_complete=True,fixture=True)
    q=ReferenceDispatchSet(ev("cross-q"),("a","b","c"),("t0","t1"),
                           ((10.,10.),(0.,0.),(-10.,-10.)),
                           observed_ac_flows_MW=((10.,10.),(10.,10.)))
    b=CountryZoneBudget(ev("cross-budget"),(("Germany",1),("France",1)))
    model=SparseACReference(grid)
    cache=model.solve(q,yearset())
    assert len(model.islands)==1
    z=country_quota_busmap(grid,b,[0.,0.])
    projection=build_oriented_projection(model,b,z)
    assert projection.zone_pairs==((0,1),)
    assert projection.grouped_branch_ids==(("bc",),)
    pz,cut=projection.verify(model,cache)
    np.testing.assert_allclose(cut,10.,atol=1e-10)


def test_opposed_parallel_physical_flows_detected_before_export():
    grid=DetailedGridSnapshot(
        ev("counterflow"),100.,
        (Bus("a","Germany",225),Bus("b","France",225)),
        (ACBranch("line","a","b",.1,225),
         ACBranch("phase","a","b",.1,225,"pst")),
        ties_110kv_complete=True,fixture=True)
    q=ReferenceDispatchSet(ev("counter-q"),("a","b"),("t0","t1"),
                           ((0.,0.),(0.,0.)),pst=(PSTDispatch("phase",(.1,.1)),))
    b=CountryZoneBudget(ev("counter-budget"),(("Germany",1),("France",1)))
    model=SparseACReference(grid)
    cache=model.solve(q,yearset())
    p=build_oriented_projection(model,b,(0,1))
    p.verify(model,cache)
    d=p.counterflow_diagnostic(cache)
    assert len(d)==1
    assert d[0]["max_cancellation_ratio"]==pytest.approx(1.)
    assert d[0]["opposing_parallel_flows"] is True


def test_preflight_machine_ledger_and_immutable_writer(tmp_path):
    grid,times,q=island_case()
    result=preflight_ledger(grid,times,q,ratings(),budget())
    assert result["status"]=="PASS_SYNTHETIC"
    assert result["model_size"]["ac_islands"]==2
    assert result["model_size"]["hvdc_pairs"]==1
    assert result["gates"]["G01"]=="PASS_INPUT_CONTRACT"
    assert result["gates"]["G11_PART"].startswith("PASS_COMPONENT")
    assert len(result["flow_cache_sha256"])==64
    path=tmp_path/"ledger.json"
    save_ledger_once(result,path)
    with pytest.raises(FileExistsError):
        save_ledger_once(result,path)


def test_preflight_blocked_on_unknown_110kv_tie_completeness():
    grid,times,q=island_case()
    result=preflight_ledger(replace(grid,ties_110kv_complete=False),
                            times,q,ratings(),budget())
    assert result["status"]=="BLOCKED_DATA"
    assert "110-kV" in result["blocker"]


def test_no_invented_weather_year_selection_and_five_year_real_contract():
    pts=tuple(TimePoint(f"p{i}",f"20{20+i}-01-01T00:00:00+00:00",
                        f"y{i}","winter",1.) for i in range(5))
    full=TimeSet(ev("five"),tuple(f"y{i}" for i in range(5)),pts,fixture=False)
    assert len(full.weather_year_ids)==5
    with pytest.raises(ContractError,match="five externally fixed years"):
        TimeSet(ev("four"),("a","b","c","d"),pts[:4],fixture=False)
    with pytest.raises(ContractError,match="duplicate timestamps"):
        replace(full,points=pts[:1]+(replace(pts[1],timestamp=pts[0].timestamp),)+pts[2:])
