import numpy as np
import pytest
from tyndp_reduce.demo import synthetic_system
from tyndp_reduce.dc import balanced_from_exogenous
from tyndp_reduce.aggregation import build_aggregation
from tyndp_reduce.clustering import greedy_busmap,assert_connected_zones
from tyndp_reduce.distribution import uniform_reference,capacity_reference,merit_order_reference,technology_reference
from tyndp_reduce.offsets import split_reference,structure_correction
from tyndp_reduce.equivalent import fit_equivalent
from tyndp_reduce.security import bodf_from_ptdf,n1_worst_loading,seasonal_directional_limits

@pytest.fixture
def sample():return synthetic_system(T=48)

def test_balancing_is_required(sample):
    d,cap,co,re,wi,so,lo,cv,p=sample
    with pytest.raises(ValueError):d.flows(wi+so-lo)
    b=balanced_from_exogenous(wi+so-lo,cap/cap.sum())
    assert np.allclose(b.sum(axis=0),0)
    assert np.allclose(d.incidence()@d.flows(b),b)

def test_exact_aggregation_identity(sample):
    d,cap,co,re,wi,so,lo,cv,p=sample
    z=np.repeat(np.arange(3),3)
    ag=build_aggregation(d,z)
    pz,fz=ag.aggregate(p,d.flows(p))
    assert ag.verify(d)
    assert np.allclose(ag.A_z@fz,pz)

def test_merit_order_distribution(sample):
    d,cap,co,*_=sample;z=np.repeat(np.arange(3),3)
    ag=build_aggregation(d,z)
    for R in (uniform_reference(z),capacity_reference(z,cap),merit_order_reference(z,cap,co)):
        assert np.allclose(ag.P@R,np.eye(3))
        _,_,f=split_reference(d,ag,R,sample[-1])
        assert f.shape==(len(ag.pairs),48)

def test_carrier_structural_zero_divergence(sample):
    d,cap,co,re,wi,so,lo,cv,p=sample;ag=build_aggregation(d,np.repeat(np.arange(3),3))
    parts,total=structure_correction(d,ag,uniform_reference(ag.zone_of_bus),{'wind':wi,'solar':so,'load':-lo})
    assert np.allclose(ag.A_z@total,0)
    assert np.allclose(sum(parts.values()),total)

def test_connected_contraction_and_nonzero_overload(sample):
    d,cap,co,re,wi,so,lo,cv,p=sample
    result=greedy_busmap(d,np.linspace(0,1,d.l),3)
    assert len(set(result))==3
    assert assert_connected_zones(d,result)

def test_equivalent_fit_contract(sample):
    d,cap,co,re,wi,so,lo,cv,p=sample;ag=build_aggregation(d,np.repeat(np.arange(3),3))
    pz,fz=ag.aggregate(p,d.flows(p))
    fit=fit_equivalent(ag,pz,fz)
    assert fit.success and np.all(fit.x>0)
    assert np.allclose(ag.A_z@fit.c0,0,atol=1e-7)
    assert np.allclose(ag.A_z@fit.predicted,pz,atol=1e-6)

def test_security_explicit_flags(sample):
    d,cap,co,re,wi,so,lo,cv,p=sample;ag=build_aggregation(d,np.repeat(np.arange(3),3))
    f=d.flows(p);B,invalid=bodf_from_ptdf(d);r,invalid2=n1_worst_loading(d,f)
    assert r.shape==f.shape and invalid==invalid2
    season=np.array(['winter']*24+['summer']*24)
    df=seasonal_directional_limits(ag,f,r,season)
    assert len(df)==len(ag.pairs)*4
    assert set(df.status).issubset({'insufficient_data','weak_relationship','insufficient_stress_range',
                  'nonpositive_intercept_solution','estimated_extrapolated','estimated_interpolated'})
