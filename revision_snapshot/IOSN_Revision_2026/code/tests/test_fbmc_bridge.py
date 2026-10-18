import numpy as np
import pytest
from tyndp_reduce.dc import DetailedDC
from tyndp_reduce.fbmc_bridge import (
    market_partition,gsk_uniform,gsk_from_positive_weights,validate_gsk,
    cnec_operator,build_domain,structural_offset,select_sensitive_cnecs,
    bilateral_capacity,maximise_net_position,
)


def toy():
    # Two nodes A, one B, one C, all connected + meshed.
    lines=[(0,1,.20,50),(1,2,.11,45),(2,3,.17,40),
           (3,0,.13,37),(0,2,.25,30)]
    d=DetailedDC(tuple('abcd'),tuple(f'e{k}' for k in range(len(lines))),
      np.array([e[0] for e in lines]),np.array([e[1] for e in lines]),
      np.array([e[2] for e in lines]),np.array([e[3] for e in lines]))
    P=market_partition([0,0,1,2]);G=gsk_from_positive_weights(P,[1,3,1,1]);
    ref=np.array([4.,-1.,-2.,-1.])
    return d,P,G,ref


def test_partition_and_gsk():
    d,P,G,p=toy()
    assert validate_gsk(P,G)
    assert np.allclose(P@G,np.eye(3))
    assert np.allclose(P@gsk_uniform(P),np.eye(3))
    with pytest.raises(ValueError): validate_gsk(P,G*.5)


def test_base_point_and_structural_zero_position():
    d,P,G,p=toy();K=cnec_operator(d,[0,1,2],[None,None,None])
    domain=build_domain(d.ptdf(),P,G,K,p,np.array([50.,45,40]),np.array([1.,1,1.]))
    assert np.allclose(domain.f0,structural_offset(d.ptdf(),P,G,K,p))
    assert np.allclose(domain.f_ref,domain.zonal_ptdf@domain.np_ref + domain.f0)
    assert domain.feasible(domain.np_ref)
    assert np.allclose(domain.coefficient@domain.np_ref-domain.ram,
                       np.r_[domain.f_ref - np.array([49.,44.,39.]),
                              -domain.f_ref-np.array([49.,44.,39.])])


def test_contingency_operator_against_direct_outage_dc():
    d,P,G,p=toy()
    H=d.ptdf();K=cnec_operator(d,[0],[2]);pred=(K@H@p).item()
    keep=[k for k in range(d.l) if k!=2]
    isolated=DetailedDC(d.bus_names,tuple(d.line_names[k] for k in keep),
                       d.bus0[keep],d.bus1[keep],d.x[keep],d.limit[keep])
    actual=isolated.flows(p)[keep.index(0)]
    assert np.isclose(pred,actual,atol=1e-8)


def test_slack_reference_and_gsk_change():
    d,P,G,p=toy();K=cnec_operator(d,[0,1],[None,None])
    alt=gsk_uniform(P)
    a=build_domain(d.ptdf(slack=0),P,G,K,p,[50,45],[1,1])
    b=build_domain(d.ptdf(slack=3),P,G,K,p,[50,45],[1,1])
    assert np.allclose(a.f0,b.f0)
    assert np.allclose(a.zonal_ptdf@np.array([1,-1,0]),b.zonal_ptdf@np.array([1,-1,0]))
    c=build_domain(d.ptdf(),P,alt,K,p,[50,45],[1,1])
    assert not np.allclose(a.zonal_ptdf@np.array([1,-1,0]),c.zonal_ptdf@np.array([1,-1,0]))


def test_internal_cnec_kept_and_not_equal_interzone_reduction():
    d,P,G,p=toy()
    K=cnec_operator(d,[0],[None])  # edge 0 connects nodes a,b IN SAME market bidding zone
    dom=build_domain(d.ptdf(),P,G,K,p,[50],[1])
    assert (P[:,d.bus0[0]]==P[:,d.bus1[0]]).all()
    assert dom.zonal_ptdf.shape==(1,3)
    assert isinstance(select_sensitive_cnecs(dom,0),np.ndarray)


def test_bilateral_capacity_and_market_constraints():
    d,P,G,p=toy();K=cnec_operator(d,[0,1,2,3],[None]*4)
    dom=build_domain(d.ptdf(),P,G,K,p,d.limit[:4],np.ones(4))
    t=bilateral_capacity(dom,0,1)
    assert np.isfinite(t) and t>0
    move=np.array([1.,-1.,0.])
    assert dom.feasible(.99*t*move)
    assert not dom.feasible(1.01*t*move)
    m,_=maximise_net_position(dom,0)
    assert m+1e-8>=t


def test_unbalanced_reference_rejected():
    d,P,G,p=toy();K=cnec_operator(d,[0],[None])
    with pytest.raises(ValueError):build_domain(d.ptdf(),P,G,K,p+1,[50],[1])
