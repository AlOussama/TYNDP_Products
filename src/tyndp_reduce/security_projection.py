"""Analytical N-1 references for zonal network reduction (research prototype).

A CNEC polytope is N-1 exact only for a specified intrazonal injection map,
physical baseline, and outage/monitoring set. Bilateral margins are not
unconditional ratings of equivalent zonal links.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np
from scipy.linalg import null_space
from scipy.sparse import csr_matrix


@dataclass(frozen=True)
class CNECSet:
    K: csr_matrix
    limits: np.ndarray
    labels: tuple[tuple[str, int, int | None], ...]
    lodf: np.ndarray
    invalid_outages: tuple[int, ...]


@dataclass(frozen=True)
class ZonalSecurity:
    Hcz: np.ndarray
    f0: np.ndarray
    pz_ref: np.ndarray
    base_cnec_flow: np.ndarray
    cnecs: CNECSet


def lodf_from_ptdf(H: np.ndarray, A: np.ndarray, tol: float = 1e-9):
    H = np.asarray(H, dtype=float)
    A = np.asarray(A, dtype=float)
    if H.ndim != 2 or A.shape != (H.shape[1], H.shape[0]):
        raise ValueError("H must be (L,N), A must be (N,L)")
    T = H @ A
    L = T.shape[0]
    D = np.full((L, L), np.nan, dtype=float)
    invalid = []
    for k in range(L):
        den = 1.0 - T[k, k]
        if abs(den) <= tol:
            invalid.append(k)
            continue
        D[:, k] = T[:, k] / den
        D[k, k] = -1.0
    return D, tuple(invalid)


def dual_cycle_lodf(A: np.ndarray, x: np.ndarray, tol: float = 1e-10):
    A = np.asarray(A, float)
    x = np.asarray(x, float)
    if A.ndim != 2 or x.shape != (A.shape[1],) or np.any(x <= 0):
        raise ValueError("Require A (N,L) and strictly positive x (L,)")
    C = null_space(A)
    L = A.shape[1]
    D = np.full((L, L), np.nan)
    if C.size == 0:
        return D, tuple(range(L))
    M = C @ np.linalg.solve(C.T @ (x[:, None] * C), C.T)
    invalid = []
    for k in range(L):
        if M[k, k] <= tol:
            invalid.append(k)
            continue
        D[:, k] = -M[:, k] / M[k, k]
        D[k, k] = -1.0
    return D, tuple(invalid)


def woodbury_single_outage_inverse(Lred: np.ndarray, a: np.ndarray,
                                   susceptance: float, tol: float = 1e-10):
    Lred = np.asarray(Lred, dtype=float)
    a = np.asarray(a, dtype=float)
    if Lred.ndim != 2 or Lred.shape[0] != Lred.shape[1] or a.shape != (Lred.shape[0],):
        raise ValueError("Shapes Lred=(N-1,N-1), a=(N-1,)")
    if susceptance <= 0:
        raise ValueError("Susceptance must be positive")
    inverse = np.linalg.inv(Lred)
    v = inverse @ a
    denominator = 1 - susceptance * float(a @ v)
    if abs(denominator) <= tol:
        raise ValueError("Bridge/islanding contingency: singular Woodbury denominator")
    return inverse + (susceptance / denominator) * np.outer(v, v)


def cnec_operator(H: np.ndarray, A: np.ndarray, limits: np.ndarray,
                  contingencies: Sequence[int] | None = None,
                  monitored: Sequence[int] | None = None,
                  include_n0: bool = True,
                  fail_on_islanding: bool = True) -> CNECSet:
    H = np.asarray(H, float)
    A = np.asarray(A, float)
    limits = np.asarray(limits, float)
    L = H.shape[0]
    if limits.shape != (L,) or np.any(limits <= 0):
        raise ValueError("limits must be positive vector for detailed branches")
    D, invalid = lodf_from_ptdf(H, A)
    checked = tuple(range(L)) if contingencies is None else tuple(map(int, contingencies))
    watched = tuple(range(L)) if monitored is None else tuple(map(int, monitored))
    if any(k < 0 or k >= L for k in checked + watched):
        raise ValueError("Invalid branch index")
    invalid_checked = tuple(k for k in checked if k in invalid)
    if invalid_checked and fail_on_islanding:
        raise ValueError(f"Islanding outages need special handling: {invalid_checked}")
    rows = []
    cols = []
    vals = []
    lim = []
    label = []
    def append(coeffs, monitored_l, outage, typ):
        row = len(lim)
        for j, v in coeffs.items():
            if abs(v) > 1e-14:
                rows.append(row); cols.append(j); vals.append(v)
        lim.append(float(limits[monitored_l]))
        label.append((typ, int(monitored_l), outage))
    if include_n0:
        for l in watched:
            append({l: 1.}, l, None, 'N0')
    for k in checked:
        if k in invalid:
            continue
        for l in watched:
            if l == k:
                continue
            append({l: 1., k: float(D[l, k])}, l, int(k), 'N1')
    K = csr_matrix((vals, (rows, cols)), shape=(len(lim), L))
    return CNECSet(K, np.array(lim), tuple(label), D, invalid_checked)


def zonal_security(H: np.ndarray, P: np.ndarray, R: np.ndarray,
                   p_ref: np.ndarray, cnecs: CNECSet,
                   physical_offset: np.ndarray | None = None,
                   atol: float = 1e-8) -> ZonalSecurity:
    H = np.asarray(H, float)
    P = np.asarray(P, float)
    R = np.asarray(R, float)
    p_ref = np.asarray(p_ref, float)
    L, N = H.shape
    if P.ndim != 2 or P.shape[1] != N or R.shape != (N, P.shape[0]):
        raise ValueError("P, R and H dimensions mismatch")
    if p_ref.shape != (N,) or abs(np.sum(p_ref)) > atol:
        raise ValueError("p_ref must be balanced nodal injection vector")
    if not np.allclose(P @ R, np.eye(P.shape[0]), atol=atol):
        raise ValueError("P R != I: invalid disaggregation")
    physical_offset = np.zeros(L) if physical_offset is None else np.asarray(physical_offset, float)
    if physical_offset.shape != (L,):
        raise ValueError("physical_offset must have one value per branch")
    pz = P @ p_ref
    Hcz = np.asarray(cnecs.K @ H @ R)
    residual = p_ref - R @ pz
    f0 = np.asarray(cnecs.K @ (H @ residual + physical_offset)).reshape(-1)
    fref = np.asarray(cnecs.K @ (H @ p_ref + physical_offset)).reshape(-1)
    if not np.allclose(Hcz @ pz + f0, fref, atol=atol):
        raise AssertionError("Affine CNEC reference reconstruction mismatch")
    return ZonalSecurity(Hcz, f0, pz, fref, cnecs)


def bilateral_transfer_limit(model: ZonalSecurity, zone_from: int, zone_to: int,
                             base_pz: np.ndarray | None = None,
                             atol: float = 1e-7):
    Z = model.Hcz.shape[1]
    if not (0 <= zone_from < Z and 0 <= zone_to < Z) or zone_from == zone_to:
        raise ValueError("Distinct zones required")
    pz = model.pz_ref if base_pz is None else np.asarray(base_pz, float)
    if pz.shape != (Z,) or abs(pz.sum()) > atol:
        raise ValueError("Base zonal vector must be balanced")
    b = model.Hcz @ pz + model.f0
    lim = model.cnecs.limits
    if lim.size == 0:
        raise ValueError("Cannot certify safety without monitored CNECs")
    if np.max(np.abs(b) - lim) > atol:
        raise ValueError("Reference/baseline is not N-1 feasible")
    d = np.zeros(Z); d[zone_from] = 1.; d[zone_to] = -1.
    g = model.Hcz @ d
    nonzero = np.abs(g) > atol
    if not np.any(nonzero):
        return float('inf'), None
    margins = (lim[nonzero] - np.sign(g[nonzero]) * b[nonzero]) / np.abs(g[nonzero])
    i = int(np.argmin(margins))
    row = int(np.flatnonzero(nonzero)[i])
    return float(max(0., margins[i])), model.cnecs.labels[row]


def robust_uniform_derating(D: np.ndarray, limits: np.ndarray,
                            invalid_outages: Sequence[int] = ()):
    D = np.asarray(D, float)
    limits = np.asarray(limits, float)
    if invalid_outages:
        raise ValueError("Cannot certify a uniform N-1 derating with unresolved islanding outages")
    L = len(limits)
    if D.shape != (L, L) or np.any(limits <= 0):
        raise ValueError("Wrong shapes or nonpositive limits")
    values = [1.]
    for k in range(L):
        if not np.all(np.isfinite(D[:, k])):
            raise ValueError("NaN LODF: unresolved contingency")
        for l in range(L):
            if l != k:
                values.append(limits[l] / (limits[l] + abs(D[l, k]) * limits[k]))
    return float(min(values))
