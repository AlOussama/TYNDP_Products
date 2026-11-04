"""IoSN Annex 6.1 screening (D/T), not experimental method B.

Screen 225- and 400-kV AC *lines* with duration-weighted annual overload
energy in MWh, using snapshot-specific normal operating MW limits.
Keep the five externally supplied weather-year IDs separated.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Mapping
import numpy as np


class ScreeningError(ValueError):
    pass


@dataclass(frozen=True)
class AnnualScreen:
    year_ids: tuple[str, ...]
    rows: tuple[dict, ...]          # (year_id, line_id, voltage_kv, ...)
    screened_line_ids: tuple[str, ...]

    def year_score(self, line_id: str, year_id: str) -> float:
        return next((row["overload_MWh"] for row in self.rows
                     if row["line_id"] == line_id and row["year_id"] == year_id), 0.0)


def screen_annual_overload(grid, flow_cache, time, ratings) -> AnnualScreen:
    branches = grid.active_branches
    if tuple(b.identifier for b in branches) != flow_cache.branch_ids:
        raise ScreeningError("Reference flow branch ordering/content mismatches grid")
    if (flow_cache.bus_ids != grid.bus_ids or
            flow_cache.snapshot_ids != time.snapshot_ids or
            ratings.snapshot_ids != time.snapshot_ids):
        raise ScreeningError("Reference/time/rating snapshots or bus ordering mismatched")
    if flow_cache.neutral_calibration:
        raise ScreeningError("Screening requires operational, not neutral-calibration flows")
    if {b.identifier for b in branches} != set(ratings.normal_mw):
        raise ScreeningError("Missing/extra MW limits; no silent imputation")
    eligible = []
    for i, branch in enumerate(branches):
        if branch.kind != "line":
            continue
        declared = getattr(branch, "screening_class_kv", None)
        if declared is None:
            if branch.voltage_kv in (225., 400.):
                declared = branch.voltage_kv
            elif 200. <= branch.voltage_kv <= 450.:
                raise ScreeningError(
                    f"Ambiguous nominal voltage class on {branch.identifier}: "
                    "explicit screening_class_kv=225/400 (or 0 for exclusion) required"
                )
            else:
                continue
        if declared in (225., 400.):
            eligible.append((i, branch, float(declared)))
        elif declared != 0.:
            raise ScreeningError("Invalid explicit screening voltage class")
    rows: list[dict] = []
    for y in time.weather_year_ids:
        mask = np.array([item == y for item in time.year_for_snapshot])
        if not np.any(mask):
            raise ScreeningError("Each external weather year must have snapshots")
        for i, branch, voltage_class in eligible:
            flow = flow_cache.flow_mw[i, mask]
            limit = ratings.normal_mw[branch.identifier][mask]
            durations = time.duration_hours[mask]
            overload = np.maximum(0.0, np.abs(flow) - limit)
            rows.append({
                "year_id": y, "line_id": branch.identifier,
                "voltage_kv": voltage_class,
                "nominal_voltage_kv": branch.voltage_kv,
                "overload_MWh": float(np.sum(overload * durations)),
                "overload_hours": float(np.sum(durations[overload > 0])),
                "observation_hours": float(np.sum(durations)),
            })
    return AnnualScreen(tuple(time.weather_year_ids), tuple(rows),
                        tuple(b.identifier for _, b, _ in eligible))


def weighted_edge_costs(screen: AnnualScreen, grid,
                        explicit_year_weights: Mapping[str, float]) -> dict[str, float]:
    """I: no hidden averaging of separate annual IoSN scores.

    Caller must specify one nonnegative weight per externally fixed year.
    """
    if set(explicit_year_weights) != set(screen.year_ids):
        raise ScreeningError("Explicit weights required for all five fixed external years")
    if any(not math.isfinite(float(w)) or w < 0 for w in explicit_year_weights.values()):
        raise ScreeningError("Invalid yearly weight")
    if sum(explicit_year_weights.values()) <= 0:
        raise ScreeningError("Zero total year weight")
    return {
        b.identifier: float(sum(float(explicit_year_weights[y]) *
                                screen.year_score(b.identifier, y)
                                for y in screen.year_ids))
        for b in grid.active_branches
    }
