"""Official Table-3 budget and explicit, reversible country labels for Module 2.

D: original published 37 separate entries, total 102.
T: a zone must be country-pure and AC-connected; HVDC does not join islands.
I: a user-supplied one-to-one label map is mandatory, even for ISO-like IDs.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from types import MappingProxyType
from typing import Mapping
import csv

# Pinned transcription of ENTSO-E 25 Feb 2026 consultation, Table 3, pp.26-27.
PUBLISHED_QUOTAS = {
    "Albania": 1, "Austria": 4, "Belgium": 3, "Bosnia": 1,
    "Bulgaria": 1, "Croatia": 1, "Cyprus": 1, "Czech Republic": 2,
    "Denmark": 2, "Estonia": 1, "Finland": 1, "France": 16,
    "Germany": 11, "Greece": 2, "Hungary": 1, "Ireland": 1,
    "Italy": 7, "Latvia": 1, "Lithuania": 1, "Luxembourg": 1,
    "Macedonia": 1, "Malta": 1, "Montenegro": 1, "Netherlands": 5,
    "Northern Ireland": 1, "Norway": 3, "Poland": 5, "Portugal": 2,
    "Romania": 3, "Serbia": 1, "Slovakia": 1, "Slovenia": 1,
    "Spain": 10, "Sweden": 4, "Switzerland": 2, "Turkey": 1,
    "United Kingdom": 1,
}


class CountryContractError(ValueError):
    pass


@dataclass(frozen=True)
class CountryZoneBudget:
    quotas: Mapping[str, int]
    official: bool
    source_sha256: str

    def __post_init__(self):
        q = dict(self.quotas)
        if not q or any(not isinstance(c, str) or not c for c in q):
            raise CountryContractError("Country labels must be nonempty")
        if any(type(k) is not int or k < 1 for k in q.values()):
            raise CountryContractError("Country quota must be a positive integer")
        if self.official and q != PUBLISHED_QUOTAS:
            raise CountryContractError("Official budget must exactly match all 37 published country quotas")
        if len(self.source_sha256) != 64:
            raise CountryContractError("Budget source SHA-256 required")
        object.__setattr__(self, "quotas", MappingProxyType(q))

    @classmethod
    def synthetic(cls, quotas: Mapping[str, int]):
        raw = repr(sorted(dict(quotas).items())).encode()
        return cls(quotas, False, sha256(b"synthetic-country-budget:" + raw).hexdigest())


def load_official_country_budget(csv_path: str | Path | None = None) -> CountryZoneBudget:
    if csv_path is None:
        # Editable repo path; wheel consumers explicitly supply the source CSV.
        csv_path = (Path(__file__).resolve().parents[3] / "docs/current"
                    / "IOSN_2026_OFFICIAL_COUNTRY_ZONE_BUDGET.csv")
    raw = Path(csv_path).read_bytes()
    import io
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if reader.fieldnames != ["country_label_as_published", "n_zones", "source_page"]:
        raise CountryContractError("Unexpected official CSV schema")
    entries: dict[str, int] = {}
    for row in reader:
        name = row["country_label_as_published"]
        if name in entries or not name or row["source_page"] not in ("26", "27"):
            raise CountryContractError("Duplicate/invalid country label or source page")
        try:
            value = int(row["n_zones"])
        except (TypeError, ValueError) as exc:
            raise CountryContractError("Noninteger country zone quota") from exc
        entries[name] = value
    result = CountryZoneBudget(entries, True, sha256(raw).hexdigest())
    assert len(result.quotas) == 37 and sum(result.quotas.values()) == 102
    assert "Northern Ireland" in result.quotas and "United Kingdom" in result.quotas
    return result


def resolve_country_ids(grid, explicit_map: Mapping[str, str],
                        budget: CountryZoneBudget) -> tuple[str, ...]:
    raw = set(grid.raw_country_ids)
    if set(explicit_map) != raw:
        raise CountryContractError("Every raw country ID requires exactly one explicit mapping")
    if len(set(explicit_map.values())) != len(explicit_map):
        raise CountryContractError("Ambiguous many-to-one country normalization is forbidden")
    if not set(explicit_map.values()).issubset(budget.quotas):
        raise CountryContractError("Unpublished or unbudgeted country label")
    labels = tuple(explicit_map[r] for r in grid.raw_country_ids)
    if budget.official and set(labels) != set(budget.quotas):
        raise CountryContractError("Full official Europe input missing one or more of 37 countries")
    return labels


def country_ac_components(grid, labels: tuple[str, ...]) -> dict[str, int]:
    buspos = {x: i for i, x in enumerate(grid.bus_ids)}
    neighbors = [set() for _ in grid.bus_ids]
    for branch in grid.active_branches:
        i, j = buspos[branch.bus0], buspos[branch.bus1]
        if labels[i] == labels[j]:
            neighbors[i].add(j)
            neighbors[j].add(i)
    counts: dict[str, int] = {}
    visited: set[int] = set()
    for start in range(len(grid.bus_ids)):
        if start in visited:
            continue
        label = labels[start]
        counts[label] = counts.get(label, 0) + 1
        stack = [start]
        visited.add(start)
        while stack:
            for j in neighbors[stack.pop()]:
                if j not in visited:
                    visited.add(j)
                    stack.append(j)
    return counts


def validate_country_feasibility(grid, labels: tuple[str, ...],
                                 budget: CountryZoneBudget):
    if grid.incomplete_110kv_ties:
        raise CountryContractError("BLOCKED_DATA: incomplete 110-kV tie data")
    if len(labels) != len(grid.bus_ids):
        raise CountryContractError("Country-label vector length mismatch")
    components = country_ac_components(grid, labels)
    for name, k in budget.quotas.items():
        n = labels.count(name)
        if n < k:
            raise CountryContractError(f"Country {name}: fewer buses than required quota {k}")
        if components.get(name, 0) > k:
            raise CountryContractError(
                f"Country {name}: underbudgeted disconnected AC islands "
                f"({components[name]} components, {k} zones)"
            )


def validate_busmap(grid, zone_of_bus: tuple[str, ...],
                    labels: tuple[str, ...],
                    budget: CountryZoneBudget,
                    protected_line_ids=()) -> dict[str, int]:
    if len(zone_of_bus) != len(grid.bus_ids):
        raise CountryContractError("Busmap must assign every original bus exactly once")
    if any(not x for x in zone_of_bus):
        raise CountryContractError("Empty/unnamed zone")
    members: dict[str, set[int]] = {}
    for i, zid in enumerate(zone_of_bus):
        members.setdefault(zid, set()).add(i)
    for zid, indices in members.items():
        if len({labels[i] for i in indices}) != 1:
            raise CountryContractError(f"Mixed-country cluster {zid}")
    pos = {name: i for i, name in enumerate(grid.bus_ids)}
    adjacency = [set() for _ in grid.bus_ids]
    for branch in grid.active_branches:
        i, j = pos[branch.bus0], pos[branch.bus1]
        adjacency[i].add(j)
        adjacency[j].add(i)
        if branch.identifier in protected_line_ids and zone_of_bus[i] == zone_of_bus[j]:
            raise CountryContractError(f"Protected critical branch swallowed: {branch.identifier}")
    if not set(protected_line_ids).issubset({x.identifier for x in grid.active_branches}):
        raise CountryContractError("Protected critical branch not in active AC network")
    for zid, indices in members.items():
        seen = {min(indices)}
        stack = list(seen)
        while stack:
            for j in adjacency[stack.pop()]:
                if j in indices and j not in seen:
                    seen.add(j)
                    stack.append(j)
        if seen != indices:
            raise CountryContractError(f"Disconnected AC zone {zid}")
    actual = {label: 0 for label in budget.quotas}
    for indices in members.values():
        label = labels[next(iter(indices))]
        actual[label] += 1
    if actual != dict(budget.quotas):
        raise CountryContractError(f"Incorrect country quotas {actual} != {dict(budget.quotas)}")
    return actual
