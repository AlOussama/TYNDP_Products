"""Machine-readable M2 G01/G02/G03/G11 partial data qualification ledger."""
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from .contracts import ContractError, RejectedComponent
from .country import validate_country_feasibility
from .physical import SparseACReference, _hash
from .screening import _ratings_array


def preflight_ledger(grid, times, dispatch, ratings, budget, full_geography=False):
    """No claim of real qualification; fail closed with an explicit blocker."""
    ledger = {
        "schema": "M2_MA1_Preflight_v1",
        "scope": "M2 only", "official_algorithm_reproduction": False,
        "grid_sha256": _hash(asdict(grid)),
        "time_sha256": _hash(asdict(times)),
        "dispatch_sha256": _hash(asdict(dispatch)),
        "ratings_sha256": _hash(asdict(ratings)),
        "budget_sha256": _hash(asdict(budget)),
        "weather_year_ids": list(times.weather_year_ids),
        "full_geography": bool(full_geography),
        "component_status": [], "gates": {},
        "status": "BLOCKED_DATA"
    }
    try:
        if not grid.ties_110kv_complete:
            raise ContractError("BLOCKED_DATA: 110-kV and AC tie completeness unverified")
        if full_geography and (times.fixture or len(times.weather_year_ids) != 5):
            raise ContractError("BLOCKED_DATA: full geography requires five fixed real weather years")
        validate_country_feasibility(grid, budget, full_geography)
        physical = SparseACReference(grid)
        ledger["model_size"] = {"buses": len(grid.buses), "ac_branches": len(grid.branches),
                                "hvdc_pairs": len(grid.hvdc), "snapshots": len(times.points),
                                "ac_islands": len(physical.islands)}
        ledger["islands"] = [[grid.buses[i].name for i in island] for island in physical.islands]
        ledger["country_bus_counts"] = {
            label: sum(bus.country == label for bus in grid.buses) for label, _ in budget.quotas}
        _ratings_array(ratings, grid.branches, times)
        ledger["gates"]["G01"] = "PASS_INPUT_CONTRACT"
        cache = physical.solve(dispatch, times)
        ledger["flow_cache_sha256"] = cache.sha256
        ledger["gates"]["G03"] = "PASS_AC_ISLAND_KCL"
        ledger["gates"]["G02"] = "PASS_COUNTRY_FEASIBILITY"
        ledger["component_status"] = [
            {"id": e.name, "kind": e.kind, "status": "SUPPORTED_LOSSLESS_DC_UNITY_TAP"}
            for e in grid.branches
        ] + [
            {"id": e.name, "kind": "hvdc", "status": "SUPPORTED_SIGNED_TERMINALS"}
            for e in grid.hvdc
        ]
        ledger["gates"]["G11_PART"] = "PASS_COMPONENT_FIXTURE_SEMANTICS_ONLY"
        ledger["status"] = "PASS_SYNTHETIC" if grid.fixture and times.fixture and \
            not full_geography else "PREFLIGHT_ONLY_REAL_NOT_QUALIFIED"
    except (ContractError, RejectedComponent) as exc:
        ledger["blocker"] = str(exc)
        ledger["gates"]["BLOCKER"] = str(exc)
        ledger["status"] = "REJECTED_COMPONENT" if isinstance(exc, RejectedComponent) \
            else "BLOCKED_DATA"
    return ledger


def save_ledger_once(ledger, filename):
    target = Path(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as out:
        json.dump(ledger, out, sort_keys=True, indent=2)
        out.write("\n")
