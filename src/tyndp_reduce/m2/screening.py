"""IoSN Method A (D/T): yearly overload energy [MWh] on 225/400-kV AC lines.

No renewable/load alternative (method B), no annual averaging, no MVA=MW
assumption. Normal ratings are indexed by exact snapshot and may vary hourly.
"""
import numpy as np

from .contracts import ContractError, NormalContingencyRatings, TimeSet


def _ratings_array(ratings, branches, times):
    if ratings.branch_order != tuple(x.name for x in branches) or \
       ratings.time_keys != tuple(x.key for x in times.points):
        raise ContractError("G01: rating line/time indices not aligned")
    shape = (len(branches), len(times.points))
    normal = np.asarray(ratings.normal_MW, dtype=float)
    if normal.shape != shape or not np.all(np.isfinite(normal)) or np.any(normal <= 0):
        raise ContractError("G01: missing/nonpositive/invalid hourly normal MW rating")
    if ratings.contingency_MW is not None:
        emergency = np.asarray(ratings.contingency_MW, dtype=float)
        if emergency.shape != shape or not np.all(np.isfinite(emergency)) or np.any(emergency <= 0):
            raise ContractError("G11: invalid contingency/emergency MW rating")
    return normal


def screen_annual_overload(grid, times: TimeSet,
                           ratings: NormalContingencyRatings, flow_cache):
    flow = flow_cache.payload()
    if flow["grid_content_hash"] != __import__("tyndp_reduce.m2.physical", fromlist=["_hash"])._hash(
            __import__("dataclasses").asdict(grid)):
        raise ContractError("G01: flow cache from different grid")
    if tuple(flow["time_keys"]) != tuple(x.key for x in times.points) or \
       tuple(flow["weather_year_ids"]) != times.weather_year_ids:
        raise ContractError("G01: flow cache time/year mismatch")
    arr = np.asarray(flow["ac_flows_MW"], dtype=float)
    normal = _ratings_array(ratings, grid.branches, times)
    if arr.shape != normal.shape:
        raise ContractError("G01: flow/rating shapes differ")
    selected = [i for i, branch in enumerate(grid.branches) if
                branch.kind == "line" and
                (abs(branch.voltage_kv-225.) < 1e-9 or abs(branch.voltage_kv-400.) < 1e-9)]
    if not selected:
        raise ContractError("BLOCKED_DATA: no identified 225/400-kV AC lines")
    years = {}
    for year in times.weather_year_ids:
        idx = [i for i, point in enumerate(times.points) if point.weather_year == year]
        dt = np.array([times.points[i].duration_h for i in idx])
        records = []
        for line in selected:
            over = np.maximum(np.abs(arr[line, idx]) - normal[line, idx], 0.)
            records.append({
                "branch_id": grid.branches[line].name,
                "voltage_kv": grid.branches[line].voltage_kv,
                "year_id": year,
                "overload_MWh": float(over @ dt),
                "overload_hours": float((over > 0) @ dt),
            })
        years[year] = sorted(records, key=lambda row: (-row["overload_MWh"], row["branch_id"]))
    return years


def protect_congested_union(annual_scores, minimum_MWh=0.):
    """I-01: do not average yearly risks; preserve any line exceeding a threshold."""
    if minimum_MWh < 0:
        raise ContractError("G04: threshold must be nonnegative")
    return frozenset(record["branch_id"] for year in annual_scores.values()
                     for record in year if record["overload_MWh"] > minimum_MWh)
