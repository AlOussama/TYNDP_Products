"""Sparse multi-island lossless DC physical reference (T), not country slacks.

A[:,e] = +1 at bus0 and -1 at bus1. f_e = (Sbase/x_e)*
(theta_bus0 - theta_bus1 - PST_phase_e). A f = p_base + p_HVDC.
HVDC terminal p0/p1 are signed into the AC buses, with p0+p1<=0.
Operating PST/HVDC signals must be supplied, never implicitly zeroed.
Calibration is an explicitly different scenario and may fail island balance.
"""
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import splu

from .contracts import ContractError, DetailedGridSnapshot, ReferenceDispatchSet, TimeSet


def _canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(data):
    return sha256(_canonical(data).encode("utf-8")).hexdigest()


def _matrix(values, shape, label):
    arr = np.asarray(values, dtype=float)
    if arr.shape != shape or not np.all(np.isfinite(arr)):
        raise ContractError("BLOCKED_DATA: invalid " + label + " matrix or nonfinite values")
    return arr


@dataclass(frozen=True)
class ReferenceFlowCache:
    """Canonical immutable JSON payload with self-verifying SHA-256."""
    canonical_json: str
    sha256: str

    def payload(self):
        if sha256(self.canonical_json.encode("utf-8")).hexdigest() != self.sha256:
            raise ContractError("BLOCKED_DATA: reference-flow cache hash mismatch")
        return json.loads(self.canonical_json)

    def write_once(self, path):
        path = Path(path)
        self.payload()  # integrity validation
        path.parent.mkdir(parents=True, exist_ok=True)
        # x means never overwrite a frozen flow witness, even with same name.
        with path.open("x", encoding="utf-8") as stream:
            stream.write(self.canonical_json + "\n")

    @classmethod
    def from_file(cls, path, expected_sha256=None):
        raw = Path(path).read_text(encoding="utf-8").strip()
        digest = sha256(raw.encode("utf-8")).hexdigest()
        if expected_sha256 is not None and digest != expected_sha256:
            raise ContractError("BLOCKED_DATA: cached file differs from pinned reference hash")
        return cls(raw, digest)



class SparseACReference:
    def __init__(self, grid: DetailedGridSnapshot):
        self.grid = grid
        self.bus_order = tuple(b.name for b in grid.buses)
        self.branch_order = tuple(b.name for b in grid.branches)
        self.pos = {name: i for i, name in enumerate(self.bus_order)}
        n, m = len(self.bus_order), len(self.branch_order)
        self.bus0 = np.array([self.pos[e.bus0] for e in grid.branches], dtype=int)
        self.bus1 = np.array([self.pos[e.bus1] for e in grid.branches], dtype=int)
        self.incidence = coo_matrix(
            (np.r_[np.ones(m), -np.ones(m)],
             (np.r_[self.bus0, self.bus1], np.tile(np.arange(m), 2))),
            shape=(n, m)).tocsr()
        self.susceptance_MW = grid.base_mva / np.array([e.x_pu for e in grid.branches])
        edges = coo_matrix((np.ones(2*m),
                            (np.r_[self.bus0, self.bus1], np.r_[self.bus1, self.bus0])),
                           shape=(n, n)).tocsr()
        n_islands, labels = connected_components(edges, directed=False)
        self.island_label = labels
        self.islands = tuple(tuple(int(i) for i in np.flatnonzero(labels == j))
                             for j in range(n_islands))
        self.laplacian = (self.incidence @ diags(self.susceptance_MW)
                          @ self.incidence.T).tocsc()
        self.factors = []
        for nodes in self.islands:
            free = np.array(nodes[1:], dtype=int)
            self.factors.append((free, splu(self.laplacian[free, :][:, free])
                                 if len(free) else None))

    def solve(self, dispatch: ReferenceDispatchSet, times: TimeSet,
              mode: str = "operational") -> ReferenceFlowCache:
        if mode not in ("operational", "neutral_calibration"):
            raise ContractError("BLOCKED_DATA: unknown solver mode")
        t = len(times.points)
        if dispatch.bus_order != self.bus_order or dispatch.time_keys != tuple(p.key for p in times.points):
            raise ContractError("BLOCKED_DATA: bus/time ordering mismatch")
        n, m = len(self.bus_order), len(self.branch_order)
        p_base = _matrix(dispatch.nodal_injections_MW, (n, t), "nodal injections")
        p = p_base.copy()
        hd = {d.name: d for d in dispatch.hvdc}
        pst = {d.name: d for d in dispatch.pst}
        if len(hd) != len(dispatch.hvdc) or set(hd) != {x.name for x in self.grid.hvdc}:
            raise ContractError("BLOCKED_DATA: all and only HVDC terminal trajectories required")
        expected_pst = {x.name for x in self.grid.branches if x.kind == "pst"}
        if len(pst) != len(dispatch.pst) or set(pst) != expected_pst:
            raise ContractError("BLOCKED_DATA: all and only PST phase trajectories required")
        terminal_signals = {}
        for component in self.grid.hvdc:
            signal = hd[component.name]
            p0 = _matrix(signal.p0_MW, (t,), "HVDC bus0 terminal")
            p1 = _matrix(signal.p1_MW, (t,), "HVDC bus1 terminal")
            if np.any(p0+p1 > 1e-8) or np.any(p0*p1 > 1e-8):
                raise ContractError("BLOCKED_DATA: HVDC losses/signs violate terminal convention")
            terminal_signals[component.name] = (p0.tolist(), p1.tolist())
            if mode == "operational":
                p[self.pos[component.bus0]] += p0
                p[self.pos[component.bus1]] += p1
        phase = np.zeros((m, t))
        for row, component in enumerate(self.grid.branches):
            if component.kind == "pst":
                v = _matrix(pst[component.name].phase_rad, (t,), "PST phase radians")
                if mode == "operational":
                    phase[row] = v
        for island in self.islands:
            residual = p[np.asarray(island), :].sum(axis=0)
            if np.max(np.abs(residual)) > 1e-7:
                raise ContractError("BLOCKED_DATA: AC island injection imbalance; no implicit slack")
        rhs = p + self.incidence @ (self.susceptance_MW[:, None]*phase)
        theta = np.zeros((n, t))
        for free, factor in self.factors:
            if factor is not None:
                theta[free] = factor.solve(rhs[free])
        flows = self.susceptance_MW[:, None]*(self.incidence.T @ theta - phase)
        if not np.allclose(self.incidence @ flows, p, rtol=0, atol=1e-6):
            raise AssertionError("G03: multi-island KCL violation")
        if dispatch.observed_ac_flows_MW is not None and mode == "operational":
            observed = _matrix(dispatch.observed_ac_flows_MW, (m, t), "observed AC flows")
            if not np.allclose(observed, flows, rtol=0, atol=1e-6):
                raise ContractError("BLOCKED_DATA: observed flows disagree with DC reference")
        elif not self.grid.fixture and mode == "operational":
            raise ContractError("BLOCKED_DATA: synchronized observed AC flow witness missing")
        payload = {
            "schema": "M2_ReferenceFlowCache_v1",
            "mode": mode,
            "grid_content_hash": _hash(asdict(self.grid)),
            "dispatch_content_hash": _hash(asdict(dispatch)),
            "timeset_content_hash": _hash(asdict(times)),
            "bus_order": self.bus_order,
            "branch_order": self.branch_order,
            "time_keys": dispatch.time_keys,
            "weather_year_ids": times.weather_year_ids,
            "islands": tuple(tuple(self.bus_order[i] for i in island) for island in self.islands),
            "phase_rad": phase.tolist(),
            "hvdc_terminals": terminal_signals,
            "p_net_MW": p.tolist(),
            "ac_flows_MW": flows.tolist(),
        }
        raw = _canonical(payload)
        return ReferenceFlowCache(raw, sha256(raw.encode("utf-8")).hexdigest())
