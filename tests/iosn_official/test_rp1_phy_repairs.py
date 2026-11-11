"""W-PHY RP1: repaired immutable contracts, boolean safety and KCL tolerance."""
from dataclasses import replace
from hashlib import sha256
import numpy as np
import pytest

from tyndp_reduce.iosn_official.contracts import (
    ACBranch, HVDCTerminals, DetailedGridSnapshot, DataContractError,
    RejectedComponent, Provenance,
)
from tyndp_reduce.iosn_official.physical import reference_flows, ac_topology
from tyndp_reduce.iosn_official.fixture_evidence import build_synthetic_fixture


def prov(tag):
    return Provenance(tag, "synthetic://rp1/" + tag, "rp1",
                      sha256(tag.encode()).hexdigest(), synthetic=True)


def test_mutable_grid_inputs_cannot_change_topology_or_sha():
    grid, dispatch, time, *_ = build_synthetic_fixture()
    branches, ids = list(grid.ac_branches), list(grid.bus_ids)
    raw, links, other = list(grid.raw_country_ids), list(grid.hvdc), []
    frozen = replace(grid, ac_branches=branches, bus_ids=ids,
                     raw_country_ids=raw, hvdc=links, unsupported_components=other)
    before = frozen.fingerprint()
    branches.append(ACBranch("new", "d0", "d1", .1, 400))
    ids.append("ghost"); raw.append("UK"); links.clear(); other.append("SVC")
    assert frozen.fingerprint() == before
    assert frozen.active_branches == grid.active_branches
    assert reference_flows(frozen, dispatch, time).input_sha256 == reference_flows(grid, dispatch, time).input_sha256


def test_mutable_time_dispatch_ratings_and_cache_sequences_are_owned():
    grid, dispatch, time, ratings, *_ = build_synthetic_fixture()
    t_ids, years, seasons, year_per = map(list, (time.snapshot_ids, time.weather_year_ids,
                                               time.season, time.year_for_snapshot))
    ts = replace(time, snapshot_ids=t_ids, weather_year_ids=years,
                 year_for_snapshot=year_per, season=seasons)
    for seq in (t_ids, years, seasons, year_per): seq.clear()
    assert ts.snapshot_ids == time.snapshot_ids and ts.weather_year_ids == time.weather_year_ids
    b, s = list(dispatch.bus_ids), list(dispatch.snapshot_ids)
    dp = replace(dispatch, bus_ids=b, snapshot_ids=s)
    b.clear(); s.clear()
    assert dp.bus_ids == dispatch.bus_ids and dp.snapshot_ids == dispatch.snapshot_ids
    r = list(ratings.snapshot_ids)
    rt = replace(ratings, snapshot_ids=r)
    r.clear()
    assert rt.snapshot_ids == ratings.snapshot_ids
    original = reference_flows(grid, dispatch, time)
    a, b, c, d = (list(original.branch_ids), list(original.bus_ids),
                  list(original.snapshot_ids), list(original.island_of_bus))
    frozen = replace(original, branch_ids=a, bus_ids=b,
                     snapshot_ids=c, island_of_bus=d)
    for seq in (a, b, c, d): seq.clear()
    assert frozen.to_manifest() == original.to_manifest()


@pytest.mark.parametrize("flag", ["False", 0, 1, None, [], "True", 2.0])
def test_hvdc_lossless_nonbool_rejected(flag):
    with pytest.raises((DataContractError, TypeError)):
        HVDCTerminals("d", "a", "b", lossless=flag)


def test_lossy_hvdc_remains_unsupported():
    with pytest.raises(RejectedComponent):
        HVDCTerminals("d", "a", "b", lossless=False)


@pytest.mark.parametrize("flag", ["False", 0, 1, None, [], "True"])
def test_topology_and_source_nonbool_flags_rejected(flag):
    with pytest.raises((DataContractError, TypeError)):
        ACBranch("l", "a", "b", .1, 400, in_service=flag)
    grid, *_ = build_synthetic_fixture()
    with pytest.raises((DataContractError, TypeError)):
        replace(grid, incomplete_110kv_ties=flag)
    with pytest.raises((DataContractError, TypeError)):
        replace(grid.provenance, synthetic=flag)


def test_real_false_service_is_excluded_from_topology():
    grid = DetailedGridSnapshot(("a", "b"), ("DE", "DE"),
        (ACBranch("off", "a", "b", .1, 400, in_service=False),),
        (), 100., prov("off"))
    assert grid.active_branches == ()
    assert ac_topology(grid)[3] == 2


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf"),
                                 1., 1e8, 0., -1., True, None])
def test_unsafe_tolerance_rejected(bad):
    grid, dispatch, time, *_ = build_synthetic_fixture()
    with pytest.raises(DataContractError, match="atol_mw"):
        reference_flows(grid, dispatch, time, atol_mw=bad)


def test_one_mw_unbalanced_island_rejected_even_at_ceiling():
    grid, dispatch, time, *_ = build_synthetic_fixture()
    changed = dispatch.injections_mw.copy()
    changed[0] += 20.; changed[1] -= 19.
    with pytest.raises(DataContractError, match="island"):
        reference_flows(grid, replace(dispatch, injections_mw=changed), time, atol_mw=1e-6)


def test_unvalidated_nested_mutable_items_rejected():
    grid, *_ = build_synthetic_fixture()
    with pytest.raises(DataContractError):
        replace(grid, ac_branches=[{"identifier": "x"}])
    with pytest.raises(DataContractError):
        replace(grid, bus_ids=[["d0"]])
