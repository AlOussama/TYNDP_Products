"""Fail-closed, JSON-serializable input preflight (MA1 G01/G03/G11)."""
from __future__ import annotations
from dataclasses import dataclass
import json
import numpy as np

from .contracts import (
    DataContractError, RejectedComponent, DetailedGridSnapshot,
    ReferenceDispatchSet, TimeSet, NormalContingencyRatings,
)
from .physical import ac_topology, reference_flows


@dataclass(frozen=True)
class PreflightLedger:
    status: str
    grid_sha256: str
    source_provenance: dict
    model_sizes: dict
    ac_islands: list
    country_ids: dict
    component_status: dict
    checks: dict
    blockers: tuple[str, ...]

    def to_dict(self):
        return {
            "status": self.status, "grid_sha256": self.grid_sha256,
            "source_provenance": self.source_provenance,
            "model_sizes": self.model_sizes, "ac_islands": self.ac_islands,
            "country_ids": self.country_ids,
            "component_status": self.component_status,
            "checks": self.checks, "blockers": list(self.blockers),
        }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=2, ensure_ascii=False)

    def require_pass(self):
        if self.status != "PASS":
            raise DataContractError(f"{self.status}: {'; '.join(self.blockers)}")


def preflight(
    grid: DetailedGridSnapshot,
    dispatch: ReferenceDispatchSet,
    time: TimeSet,
    ratings: NormalContingencyRatings,
    *,
    country_label_map: dict[str, str],
) -> PreflightLedger:
    """Explicitly distinguish P0 physical problems from unsupported equipment.

    This verifies dataset contracts, not quality/availability of a real ENTSO-E
    reference dataset. Synthetic inputs remain synthetic even on PASS.
    """
    incidence, _, island, n_islands = ac_topology(grid)
    branches = grid.active_branches
    groups = [tuple(grid.bus_ids[i] for i in np.flatnonzero(island == k))
              for k in range(n_islands)]
    raw = set(grid.raw_country_ids)
    reasons: list[str] = []
    checks: dict[str, str] = {}
    statuses = {
        "AC_line": "SUPPORTED",
        "transformer": "SUPPORTED_LOSSLESS_DC_EQUIVALENT",
        "PST": "SUPPORTED_EXPLICIT_PHASE_MW",
        "HVDC": "SUPPORTED_EXPLICIT_LOSSLESS_TERMINALS",
        "other": "REJECTED_COMPONENT" if grid.unsupported_components else "NONE",
    }
    if grid.unsupported_components:
        reasons.append("REJECTED_COMPONENT: " + ", ".join(grid.unsupported_components))
    if grid.incomplete_110kv_ties:
        reasons.append("BLOCKED_DATA: flagged incomplete 110-kV ties")
    if set(country_label_map) != raw:
        reasons.append("BLOCKED_DATA: unresolved or extra raw country IDs")
    if len(set(country_label_map.values())) != len(country_label_map):
        # A many-to-one taxonomy mapping could merge NI and UK or another label.
        reasons.append("BLOCKED_DATA: ambiguous country-label normalization")
    if dispatch.bus_ids != grid.bus_ids or dispatch.snapshot_ids != time.snapshot_ids:
        reasons.append("BLOCKED_DATA: dispatch/time/grid index mismatch")
    if ratings.snapshot_ids != time.snapshot_ids:
        reasons.append("BLOCKED_DATA: normal/emergency rating timestamps mismatch")
    expected = {b.identifier for b in branches}
    if set(ratings.normal_mw) != expected or set(ratings.contingency_mw) != expected:
        reasons.append("BLOCKED_DATA: incomplete or extra normal/N-1 branch ratings")
    if not reasons:
        try:
            operational = reference_flows(grid, dispatch, time)
            checks["operational_reference_kcl"] = "PASS"
            checks["operational_reference_hash"] = operational.input_sha256
        except RejectedComponent as exc:
            reasons.append(str(exc))
        except DataContractError as exc:
            reasons.append(str(exc))
    status = ("REJECTED_COMPONENT" if any("REJECTED_COMPONENT" in x for x in reasons)
              else "BLOCKED_DATA" if reasons else "PASS")
    return PreflightLedger(
        status=status,
        grid_sha256=grid.fingerprint(),
        source_provenance={
            "grid": vars(grid.provenance),
            "dispatch": vars(dispatch.provenance),
            "time": vars(time.provenance),
            "ratings": vars(ratings.provenance),
        },
        model_sizes={"buses": len(grid.bus_ids), "active_ac_branches": len(branches),
                     "all_ac_branches": len(grid.ac_branches),
                     "hvdc_links": len(grid.hvdc), "snapshots": len(time.snapshot_ids),
                     "weather_year_count": len(time.weather_year_ids)},
        ac_islands=[{"id": i, "buses": list(g)} for i, g in enumerate(groups)],
        country_ids={raw_id: {"resolved": country_label_map.get(raw_id),
                              "bus_count": grid.raw_country_ids.count(raw_id)}
                     for raw_id in sorted(raw)},
        component_status=statuses,
        checks=checks,
        blockers=tuple(reasons),
    )
