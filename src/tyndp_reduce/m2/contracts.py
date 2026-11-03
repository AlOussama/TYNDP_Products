"""Fail-closed input contracts for IoSN M2, independent of M0/M1 readers.

D: published country boundaries / congestion approach.
T: oriented AC/DC balances and unit checks.
I: this module's deterministic representations and tolerances.
"""
from dataclasses import dataclass, field
from datetime import datetime
from math import isfinite


class ContractError(ValueError):
    """An input cannot be used as qualified physical data."""


class RejectedComponent(ContractError):
    """A physical component is not supported without a proven equivalent."""


@dataclass(frozen=True)
class Evidence:
    source: str
    revision: str
    sha256: str
    target_year: str

    def __post_init__(self):
        if not all((self.source, self.revision, self.target_year)):
            raise ContractError("BLOCKED_DATA: missing source, revision or target year")
        if len(self.sha256) != 64 or any(c not in "0123456789abcdef" for c in self.sha256):
            raise ContractError("BLOCKED_DATA: source SHA-256 must be lowercase hex")


@dataclass(frozen=True)
class Bus:
    name: str
    country: str
    voltage_kv: float

    def __post_init__(self):
        if not self.name or not self.country or self.country != self.country.strip():
            raise ContractError("BLOCKED_DATA: exact nonempty bus/country labels required")
        if not isfinite(self.voltage_kv) or self.voltage_kv <= 0:
            raise ContractError("BLOCKED_DATA: invalid bus voltage")


@dataclass(frozen=True)
class ACBranch:
    name: str
    bus0: str
    bus1: str
    x_pu: float
    voltage_kv: float
    kind: str = "line"   # line, transformer, pst
    tap_ratio: float = 1.0
    in_service: bool = True

    def __post_init__(self):
        if not self.name or not self.bus0 or not self.bus1 or self.bus0 == self.bus1:
            raise ContractError("BLOCKED_DATA: invalid oriented AC branch")
        if self.kind not in ("line", "transformer", "pst") or not self.in_service:
            raise RejectedComponent("REJECTED_COMPONENT: unsupported/offline AC branch " + self.name)
        if not isfinite(self.tap_ratio) or abs(self.tap_ratio - 1.0) > 1e-12:
            raise RejectedComponent("REJECTED_COMPONENT: non-unity tap needs validated model " + self.name)
        if not isfinite(self.x_pu) or self.x_pu <= 0:
            raise ContractError("BLOCKED_DATA: positive finite x_pu required")
        if not isfinite(self.voltage_kv) or self.voltage_kv <= 0:
            raise ContractError("BLOCKED_DATA: positive finite voltage_kv required")


@dataclass(frozen=True)
class HVDCTerminalPair:
    name: str
    bus0: str   # p0<0 exports from AC node 0
    bus1: str   # p1>0 injects into AC node 1; losses may make p0+p1<0

    def __post_init__(self):
        if not self.name or not self.bus0 or not self.bus1 or self.bus0 == self.bus1:
            raise ContractError("BLOCKED_DATA: invalid HVDC terminal pair")


@dataclass(frozen=True)
class DetailedGridSnapshot:
    evidence: Evidence
    base_mva: float
    buses: tuple[Bus, ...]
    branches: tuple[ACBranch, ...]
    hvdc: tuple[HVDCTerminalPair, ...] = ()
    ties_110kv_complete: bool = False
    fixture: bool = False

    def __post_init__(self):
        if not isfinite(self.base_mva) or self.base_mva <= 0:
            raise ContractError("BLOCKED_DATA: common positive base MVA required")
        names = [x.name for x in self.buses]
        if not names or len(set(names)) != len(names):
            raise ContractError("BLOCKED_DATA: duplicate/absent buses")
        branches = [x.name for x in self.branches]
        if not branches or len(set(branches)) != len(branches):
            raise ContractError("BLOCKED_DATA: duplicate/absent AC branches")
        hvdc = [x.name for x in self.hvdc]
        if len(set(hvdc)) != len(hvdc) or set(hvdc).intersection(branches):
            raise ContractError("BLOCKED_DATA: ambiguous HVDC/AC IDs")
        for x in (*self.branches, *self.hvdc):
            if x.bus0 not in names or x.bus1 not in names:
                raise ContractError("BLOCKED_DATA: missing terminal bus on " + x.name)


@dataclass(frozen=True)
class TimePoint:
    key: str
    timestamp: str       # timezone-aware ISO 8601
    weather_year: str
    season: str          # summer or winter, supplied externally
    duration_h: float

    def __post_init__(self):
        try:
            ts = datetime.fromisoformat(self.timestamp)
        except (ValueError, TypeError) as exc:
            raise ContractError("BLOCKED_DATA: invalid timestamp") from exc
        if ts.tzinfo is None or ts.utcoffset() is None:
            raise ContractError("BLOCKED_DATA: timestamp timezone missing")
        if not self.key or not self.weather_year or self.season not in ("summer", "winter"):
            raise ContractError("BLOCKED_DATA: invalid time/year/season label")
        if not isfinite(self.duration_h) or self.duration_h <= 0:
            raise ContractError("BLOCKED_DATA: invalid duration in hours")


@dataclass(frozen=True)
class TimeSet:
    evidence: Evidence
    weather_year_ids: tuple[str, ...]
    points: tuple[TimePoint, ...]
    fixture: bool = False

    def __post_init__(self):
        if not self.weather_year_ids or len(set(self.weather_year_ids)) != len(self.weather_year_ids):
            raise ContractError("BLOCKED_DATA: duplicate/absent year IDs")
        if not self.fixture and len(self.weather_year_ids) != 5:
            raise ContractError("BLOCKED_DATA: five externally fixed years required")
        if not self.points or len({p.key for p in self.points}) != len(self.points):
            raise ContractError("BLOCKED_DATA: duplicate/absent time IDs")
        if set(p.weather_year for p in self.points) != set(self.weather_year_ids):
            raise ContractError("BLOCKED_DATA: time/year contract incomplete")
        if len({p.timestamp for p in self.points}) != len(self.points):
            raise ContractError("BLOCKED_DATA: duplicate timestamps")


@dataclass(frozen=True)
class HVDCDispatch:
    name: str
    p0_MW: tuple[float, ...]
    p1_MW: tuple[float, ...]


@dataclass(frozen=True)
class PSTDispatch:
    name: str
    phase_rad: tuple[float, ...]


@dataclass(frozen=True)
class ReferenceDispatchSet:
    evidence: Evidence
    bus_order: tuple[str, ...]
    time_keys: tuple[str, ...]
    nodal_injections_MW: tuple[tuple[float, ...], ...]    # N x T, before HVDC
    hvdc: tuple[HVDCDispatch, ...] = ()
    pst: tuple[PSTDispatch, ...] = ()
    observed_ac_flows_MW: tuple[tuple[float, ...], ...] | None = None  # L x T


@dataclass(frozen=True)
class NormalContingencyRatings:
    evidence: Evidence
    branch_order: tuple[str, ...]
    time_keys: tuple[str, ...]
    normal_MW: tuple[tuple[float, ...], ...]   # L x T, not MVA
    contingency_MW: tuple[tuple[float, ...], ...] | None = None
    unit: str = "MW"

    def __post_init__(self):
        if self.unit != "MW":
            raise ContractError("BLOCKED_DATA: MVA/A ratings need explicit conversion, not MW assumption")


@dataclass(frozen=True)
class CountryZoneBudget:
    evidence: Evidence
    quotas: tuple[tuple[str, int], ...]
    official: bool = False

    def __post_init__(self):
        labels = [s for s, _ in self.quotas]
        if not labels or len(set(labels)) != len(labels) or any(not s or s != s.strip() for s in labels):
            raise ContractError("BLOCKED_DATA: country identifiers must be exact/unique")
        if any(not isinstance(k, int) or isinstance(k, bool) or k < 1 for _, k in self.quotas):
            raise ContractError("BLOCKED_DATA: positive integer country quotas required")
        if self.official and (len(labels) != 37 or sum(k for _, k in self.quotas) != 102):
            raise ContractError("BLOCKED_DATA: official quota must have 37 entries and sum 102")
        if self.official and ("Northern Ireland" not in labels or "United Kingdom" not in labels):
            raise ContractError("BLOCKED_DATA: NI and UK are separate published areas")

    @property
    def by_label(self):
        return dict(self.quotas)
