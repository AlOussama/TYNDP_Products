import numpy as np
from tyndp_reduce.demo import synthetic_system
from tyndp_reduce.aggregation import build_aggregation
from tyndp_reduce.distribution import uniform_reference,capacity_reference,merit_order_reference,technology_reference
from tyndp_reduce.equivalent import fit_reference_ptdf,reduced_ptdf


def test_reference_ptdf_projection_preserves_balance():
    d,cap,cost,res,wind,solar,load,conv,p=synthetic_system(T=24)
    agg=build_aggregation(d,np.repeat(np.arange(3),3))
    T=np.vstack([np.eye(2),-np.ones((1,2))])
    for ref in (uniform_reference(agg.zone_of_bus),
                capacity_reference(agg.zone_of_bus,cap),
                merit_order_reference(agg.zone_of_bus,cap,cost)):
        x,err,heq=fit_reference_ptdf(agg,d,ref)
        assert np.all(x>0) and np.isfinite(err)
        assert np.allclose(agg.A_z@heq@T,T,atol=1e-7)

def test_technology_reference_null_output_fallback():
    d,cap,cost,res,wind,solar,load,conv,p=synthetic_system(T=24)
    z=np.repeat(np.arange(3),3)
    q=np.zeros((9,24))
    q[0,:]=3
    refs=technology_reference(z,q)
    agg=build_aggregation(d,z)
    for t in range(24):
        assert np.allclose(agg.P@refs[:,:,t],np.eye(3))
