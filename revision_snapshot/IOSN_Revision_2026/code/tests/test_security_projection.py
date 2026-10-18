import numpy as np
import pytest
from tyndp_reduce.dc import DetailedDC
from tyndp_reduce.aggregation import build_aggregation
from tyndp_reduce.distribution import uniform_reference
from tyndp_reduce.security_projection import (
    lodf_from_ptdf, dual_cycle_lodf, woodbury_single_outage_inverse,
    cnec_operator, zonal_security, bilateral_transfer_limit,
    robust_uniform_derating,
)
from tyndp_reduce.demo import synthetic_system


def triangle():
    return DetailedDC(('A','B','C'), ('AB','BC','CA'),
                      np.array([0,1,2]), np.array([1,2,0]),
                      np.ones(3), np.array([100.,100.,80.]))


def test_dual_lodf_matches_primal_triangle():
    d = triangle()
    primal, bad = lodf_from_ptdf(d.ptdf(), d.incidence())
    dual, bad2 = dual_cycle_lodf(d.incidence(), d.x)
    assert not bad and not bad2
    np.testing.assert_allclose(primal, dual, atol=1e-10)
    assert np.allclose(np.diag(primal), -1)


def test_dual_lodf_matches_primal_meshed_nine_bus():
    d = synthetic_system(T=24)[0]
    primal, bad = lodf_from_ptdf(d.ptdf(), d.incidence())
    dual, bad2 = dual_cycle_lodf(d.incidence(), d.x)
    assert not bad and not bad2
    np.testing.assert_allclose(primal, dual, atol=1e-9)


def test_woodbury_matches_direct_after_outage():
    d = triangle()
    A = d.incidence(); L = (A / d.x) @ A.T
    keep = [1,2]
    Ar = A[keep]
    direct = L[np.ix_(keep, keep)] - (1/d.x[0])*np.outer(Ar[:,0], Ar[:,0])
    expected = np.linalg.inv(direct)
    calculated = woodbury_single_outage_inverse(L[np.ix_(keep,keep)], Ar[:,0], 1/d.x[0])
    np.testing.assert_allclose(calculated, expected, atol=1e-11)


def test_bridges_fail_closed_and_dual_flags():
    d = DetailedDC(('A','B','C'), ('AB','BC'), np.array([0,1]),
                   np.array([1,2]), np.array([1.,1.]), np.array([80.,80.]))
    _, bad = dual_cycle_lodf(d.incidence(), d.x)
    assert len(bad) == 2
    with pytest.raises(ValueError, match='Islanding'):
        cnec_operator(d.ptdf(), d.incidence(), d.limit)


def test_exact_affine_zonal_baseline_and_balance():
    d, cap, cost, res, wind, solar, load, conv, p = synthetic_system(T=24)
    agg = build_aggregation(d, np.repeat(np.arange(3),3))
    R = uniform_reference(agg.zone_of_bus)
    assert np.allclose(agg.P@R,np.eye(3))
    C = cnec_operator(d.ptdf(), d.incidence(), d.limit)
    ref = p[:,0]
    mod = zonal_security(d.ptdf(),agg.P.toarray(),R,ref,C)
    assert np.allclose(mod.Hcz @ (agg.P @ ref) + mod.f0, C.K@(d.ptdf()@ref))
    assert np.allclose((agg.P.toarray()@(ref-R@(agg.P@ref))),0)


def test_triangle_transfer_n0_150_n1_80():
    d = triangle()
    H = d.ptdf(); A = d.incidence()
    C = cnec_operator(H, A, d.limit)
    P = np.eye(3); R = np.eye(3); ref = np.zeros(3)
    mod = zonal_security(H,P,R,ref,C)
    tau, binding = bilateral_transfer_limit(mod,0,1)
    assert np.isclose(tau, 80.)
    assert binding[0] == 'N1'
    dvec = np.array([1.,-1.,0.])
    assert np.all(np.abs(mod.Hcz @(tau*dvec) + mod.f0) <= C.limits + 1e-9)
    # At least one actual constraint must be violated above the margin.
    assert np.any(np.abs(mod.Hcz@((tau+1.)*dvec)) > C.limits + 1e-8)


def test_uniform_derating_is_sufficient():
    d = triangle(); H = d.ptdf(); D, bad = lodf_from_ptdf(H,d.incidence())
    alpha = robust_uniform_derating(D,d.limit,bad)
    assert 0 < alpha < 1
    for k in range(d.l):
        for l in range(d.l):
            if l == k: continue
            assert alpha*d.limit[l] + abs(D[l,k])*alpha*d.limit[k] <= d.limit[l] + 1e-10


def test_infeasible_baseline_is_rejected():
    d = triangle(); C = cnec_operator(d.ptdf(),d.incidence(),d.limit)
    m = zonal_security(d.ptdf(),np.eye(3),np.eye(3),np.array([130.,-130.,0.]),C)
    with pytest.raises(ValueError, match='not N-1 feasible'):
        bilateral_transfer_limit(m,0,1)
