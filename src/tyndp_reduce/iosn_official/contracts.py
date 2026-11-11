"""Immutable Module-2 input contracts. MW, p.u. and radians are not interchangeable.

All contracts are for an *already assembled* grid and dispatch. No CGMES,
PECD, weather selection or external input parsing belongs here.
Implementation decisions (I): all snapshots are UTC, MW limits must be
declared as active-power proxies, and DC phase shifts are in radians.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import sha256
from types import MappingProxyType
from typing import Mapping
import json
import math
import numpy as np


class DataContractError(ValueError):
    """Fail-closed provenance, shape or physical input error."""


class RejectedComponent(DataContractError):
    """Equipment cannot safely be represented by the supported DC kernel."""


def immutable_array(value, shape=None):
    out = np.array(value, dtype=float, copy=True, order="C")
    if (shape is not None and out.shape != shape) or not np.all(np.isfinite(out)):
        raise DataContractError(f"Nonfinite or incorrect array shape: {out.shape}, expected {shape}")
    # A writeable=False NumPy owning array can be made writeable again. Bytes-
    # backed storage is truly immutable, including attempts to reset its flag.
    return np.frombuffer(out.tobytes(order="C"), dtype=np.float64).reshape(out.shape)


def digest_object(value) -> str:
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def freeze_tuple(value, label: str, element_type: type) -> tuple:
    """Own validated immutable tuple fields, never retain a caller-owned list."""
    if not isinstance(value, (tuple, list)):
        raise DataContractError(f"{label} must be a tuple or list")
    owned = tuple(value)
    if any(type(item) is not element_type for item in owned):
        raise DataContractError(f"{label} contains an invalid element type")
    return owned


@dataclass(frozen=True)
class Provenance:
    dataset_id: str
    source_uri: str
    version: str
    source_sha256: str
    synthetic: bool = False

    def __post_init__(self):
        if type(self.synthetic) is not bool:
            raise DataContractError("Provenance.synthetic must be a Python bool")
        if not isinstance(self.source_sha256, str):
            raise DataContractError("Source SHA-256 must be a string")
        if any(not isinstance(x, str) or not x.strip()
               for x in (self.dataset_id, self.source_uri, self.version)):
            raise DataContractError("Missing dataset provenance")
        if len(self.source_sha256) != 64 or any(c not in "0123456789abcdef"
                                               for c in self.source_sha256):
            raise DataContractError("Require lowercase 64-digit SHA-256 for source provenance")


@dataclass(frozen=True)
class ACBranch:
    identifier: str
    bus0: str
    bus1: str
    x_pu: float
    voltage_kv: float
    kind: str = "line"                  # line, transformer, pst
    in_service: bool = True
    phase_shift_rad: float = 0.0         # fixed transformer phase, not PST schedule
    screening_class_kv: float | None = None  # 225/400; 0=deliberate exclusion

    def __post_init__(self):
        if type(self.in_service) is not bool:
            raise DataContractError("ACBranch.in_service must be a Python bool")
        if not self.identifier or not self.bus0 or not self.bus1 or self.bus0 == self.bus1:
            raise DataContractError("Invalid AC branch identity/terminals")
        if self.kind not in {"line", "transformer", "pst"}:
            raise RejectedComponent(f"REJECTED_COMPONENT: {self.kind} on {self.identifier}")
        if not math.isfinite(self.x_pu) or self.x_pu <= 0:
            raise DataContractError(f"Positive x_pu required for {self.identifier}")
        if not math.isfinite(self.voltage_kv) or self.voltage_kv <= 0:
            raise DataContractError(f"Positive nominal kV required for {self.identifier}")
        if self.screening_class_kv is not None and self.screening_class_kv not in (0., 225., 400.):
            raise DataContractError("Invalid screening_class_kv: use 225/400, 0 or none")
        if not math.isfinite(self.phase_shift_rad):
            raise DataContractError("Nonfinite fixed phase shift")
        if self.kind == "pst" and self.phase_shift_rad != 0:
            raise DataContractError("PST phase must be provided as a snapshot schedule")


@dataclass(frozen=True)
class HVDCTerminals:
    identifier: str
    bus0: str                  # positive transfer exports from bus0
    bus1: str                  # and imports at bus1
    lossless: bool = True

    def __post_init__(self):
        if type(self.lossless) is not bool:
            raise DataContractError("HVDCTerminals.lossless must be a Python bool")
        if not self.identifier or not self.bus0 or not self.bus1 or self.bus0 == self.bus1:
            raise DataContractError("Invalid HVDC terminal identities")
        if not self.lossless:
            raise RejectedComponent("REJECTED_COMPONENT: HVDC losses need explicit terminal injection model")


@dataclass(frozen=True)
class DetailedGridSnapshot:
    bus_ids: tuple[str, ...]
    raw_country_ids: tuple[str, ...]
    ac_branches: tuple[ACBranch, ...]
    hvdc: tuple[HVDCTerminals, ...]
    base_mva: float
    provenance: Provenance
    unsupported_components: tuple[str, ...] = ()
    incomplete_110kv_ties: bool = False

    def __post_init__(self):
        for name, item_type in (
            ("bus_ids", str), ("raw_country_ids", str),
            ("ac_branches", ACBranch), ("hvdc", HVDCTerminals),
            ("unsupported_components", str),
        ):
            object.__setattr__(self, name, freeze_tuple(getattr(self, name), name, item_type))
        if type(self.incomplete_110kv_ties) is not bool:
            raise DataContractError("incomplete_110kv_ties must be a Python bool")
        if not isinstance(self.provenance, Provenance):
            raise DataContractError("Detailed grid requires validated provenance")
        if not self.bus_ids or any(not x for x in self.bus_ids) or len(set(self.bus_ids)) != len(self.bus_ids):
            raise DataContractError("Bus IDs must be nonempty and unique")
        if len(self.raw_country_ids) != len(self.bus_ids) or any(not x for x in self.raw_country_ids):
            raise DataContractError("Country ID must exist for every bus")
        if not math.isfinite(self.base_mva) or self.base_mva <= 0:
            raise DataContractError("Explicit positive system base MVA required")
        ids = [b.identifier for b in self.ac_branches] + [d.identifier for d in self.hvdc]
        if len(set(ids)) != len(ids):
            raise DataContractError("AC/HVDC identifiers must be globally unique")
        for device in (*self.ac_branches, *self.hvdc):
            if device.bus0 not in self.bus_ids or device.bus1 not in self.bus_ids:
                raise DataContractError("Unresolved branch/HVDC endpoint")
        if any(not c for c in self.unsupported_components):
            raise DataContractError("Unnamed unsupported component")

    @property
    def active_branches(self) -> tuple[ACBranch, ...]:
        return tuple(x for x in self.ac_branches if x.in_service)

    def fingerprint(self) -> str:
        return digest_object({
            "bus_ids": self.bus_ids, "raw_country_ids": self.raw_country_ids,
            "ac_branches": [vars(x) for x in self.ac_branches],
            "hvdc": [vars(x) for x in self.hvdc],
            "base_mva": self.base_mva, "source": vars(self.provenance),
            "unsupported": self.unsupported_components,
            "incomplete_110kv_ties": self.incomplete_110kv_ties,
        })


@dataclass(frozen=True)
class TimeSet:
    snapshot_ids: tuple[str, ...]
    year_for_snapshot: tuple[str, ...]
    weather_year_ids: tuple[str, ...]     # already selected, exactly five
    duration_hours: np.ndarray
    season: tuple[str, ...]              # summer or winter: supplied, not inferred
    provenance: Provenance
    timezone: str = "UTC"

    def __post_init__(self):
        for name in ("snapshot_ids", "year_for_snapshot", "weather_year_ids", "season"):
            object.__setattr__(self, name, freeze_tuple(getattr(self, name), name, str))
        t = len(self.snapshot_ids)
        if t == 0 or len(set(self.snapshot_ids)) != t:
            raise DataContractError("Snapshots must be nonempty and unique")
        timestamps = []
        for name in self.snapshot_ids:
            try:
                parsed = datetime.fromisoformat(name.replace("Z", "+00:00"))
            except (AttributeError, TypeError, ValueError) as exc:
                raise DataContractError("Snapshots must be ISO-8601 UTC timestamps") from exc
            if parsed.utcoffset() != timedelta(0):
                raise DataContractError("Snapshots must be explicitly UTC-aware")
            timestamps.append(parsed)
        if any(a >= b for a, b in zip(timestamps, timestamps[1:])):
            raise DataContractError("Snapshots must be strictly chronological in UTC")
        if len(self.weather_year_ids) != 5 or len(set(self.weather_year_ids)) != 5:
            raise DataContractError("Five distinct external weather year identifiers are required")
        if len(self.year_for_snapshot) != t or set(self.year_for_snapshot) != set(self.weather_year_ids):
            raise DataContractError("Every external year needs its own represented snapshots")
        if len(self.season) != t or set(self.season) - {"summer", "winter"}:
            raise DataContractError("Explicit summer/winter season per snapshot required")
        if self.timezone != "UTC":
            raise DataContractError("UTC-aligned times only; convert upstream with provenance")
        durations = immutable_array(self.duration_hours, (t,))
        if np.any(durations <= 0):
            raise DataContractError("Positive snapshot durations in hours required")
        object.__setattr__(self, "duration_hours", durations)


@dataclass(frozen=True)
class ReferenceDispatchSet:
    bus_ids: tuple[str, ...]
    snapshot_ids: tuple[str, ...]
    injections_mw: np.ndarray             # N x T; excludes HVDC terminals
    hvdc_transfer_mw: Mapping[str, np.ndarray]
    pst_phase_rad: Mapping[str, np.ndarray]
    provenance: Provenance

    def __post_init__(self):
        for name in ("bus_ids", "snapshot_ids"):
            object.__setattr__(self, name, freeze_tuple(getattr(self, name), name, str))
        if not self.bus_ids or not self.snapshot_ids:
            raise DataContractError("Dispatch requires bus IDs and snapshots")
        object.__setattr__(self, "injections_mw",
                           immutable_array(self.injections_mw,
                                           (len(self.bus_ids), len(self.snapshot_ids))))
        for name in ("hvdc_transfer_mw", "pst_phase_rad"):
            original = getattr(self, name)
            vals = {str(k): immutable_array(v, (len(self.snapshot_ids),))
                    for k, v in original.items()}
            object.__setattr__(self, name, MappingProxyType(vals))


@dataclass(frozen=True)
class NormalContingencyRatings:
    """Normal and emergency thermal DC-active-power *MW proxy*, by AC branch."""
    snapshot_ids: tuple[str, ...]
    normal_mw: Mapping[str, np.ndarray]
    contingency_mw: Mapping[str, np.ndarray]
    provenance: Provenance
    unit: str = "MW"

    def __post_init__(self):
        object.__setattr__(self, "snapshot_ids",
                           freeze_tuple(self.snapshot_ids, "snapshot_ids", str))
        if self.unit != "MW":
            raise DataContractError("Ratings in MVA or A require an upstream declared MW conversion")
        if not self.snapshot_ids:
            raise DataContractError("Ratings need snapshots")
        for name in ("normal_mw", "contingency_mw"):
            vals = {str(k): immutable_array(v, (len(self.snapshot_ids),))
                    for k, v in getattr(self, name).items()}
            if any(np.any(v <= 0) for v in vals.values()):
                raise DataContractError("Every normal/emergency MW rating must be positive")
            object.__setattr__(self, name, MappingProxyType(vals))


@dataclass(frozen=True)
class ReferenceFlowCache:
    branch_ids: tuple[str, ...]
    bus_ids: tuple[str, ...]
    snapshot_ids: tuple[str, ...]
    flow_mw: np.ndarray                    # L x T, oriented bus0 to bus1
    nodal_net_mw: np.ndarray               # N x T, including HVDC terminal actions
    island_of_bus: tuple[int, ...]
    input_sha256: str
    neutral_calibration: bool

    def __post_init__(self):
        for name, element_type in (
            ("branch_ids", str), ("bus_ids", str), ("snapshot_ids", str),
            ("island_of_bus", int),
        ):
            object.__setattr__(self, name,
                               freeze_tuple(getattr(self, name), name, element_type))
        if type(self.neutral_calibration) is not bool:
            raise DataContractError("neutral_calibration must be a Python bool")
        object.__setattr__(self, "flow_mw",
                           immutable_array(self.flow_mw, (len(self.branch_ids), len(self.snapshot_ids))))
        object.__setattr__(self, "nodal_net_mw",
                           immutable_array(self.nodal_net_mw, (len(self.bus_ids), len(self.snapshot_ids))))
        if len(self.input_sha256) != 64:
            raise DataContractError("Reference cache missing input digest")

    def to_manifest(self) -> dict:
        return {"input_sha256": self.input_sha256, "branch_ids": list(self.branch_ids),
                "bus_ids": list(self.bus_ids), "snapshot_ids": list(self.snapshot_ids),
                "island_of_bus": list(self.island_of_bus),
                "neutral_calibration": self.neutral_calibration, "units": "MW"}
