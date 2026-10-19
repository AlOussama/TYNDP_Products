"""Synthetic reproducible example for BOTH methods and reference variants."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from .dc import DetailedDC
from .screening import method_a,method_b,capture_fraction
from .clustering import greedy_busmap,assert_connected_zones
from .aggregation import build_aggregation
from .distribution import uniform_reference,capacity_reference,merit_order_reference,representative_buses
from .offsets import split_reference,structure_correction
from .equivalent import fit_equivalent,fit_reference_ptdf,reduced_ptdf
from .security import n1_worst_loading,seasonal_directional_limits


def synthetic_system(seed=20261016,T=120):
    rng=np.random.default_rng(seed)
    # 9-bus connected mesh, 3 representative geographical groups
    lines=[(0,1,.12,42),(1,2,.09,45),(3,4,.10,40),(4,5,.11,43),(6,7,.12,40),(7,8,.11,42),
           (0,3,.18,35),(1,4,.22,32),(2,5,.19,30),(3,6,.16,34),(4,7,.20,32),(5,8,.17,30),
           (0,6,.28,24),(2,8,.27,24),(1,7,.25,28)]
    d=DetailedDC(tuple(f'b{i}' for i in range(9)),tuple(f'l{k}' for k in range(len(lines))),
        np.array([e[0] for e in lines]),np.array([e[1] for e in lines]),
        np.array([e[2] for e in lines]),np.array([e[3] for e in lines]))
    cap=np.array([100,65,42,105,50,55,110,60,45.])
    cost=np.array([35,72,95,32,83,65,28,79,100.])
    x=np.arange(T); wind_base=(.55+.35*np.sin(x*2*np.pi/24+1)).clip(.02,.95)
    pv_base=(.8*np.maximum(0,np.sin(2*np.pi*(x%24)/24-np.pi/2))).clip(0,.85)
    wind=np.maximum(0, rng.uniform(.5,1.3,(9,T))*cap[:,None]*.28*wind_base)
    solar=np.maximum(0,rng.uniform(.7,1.3,(9,T))*cap[:,None]*.14*pv_base)
    load=(np.maximum(8,24+7*np.sin(x*2*np.pi/24))*rng.uniform(.6,1.5,(9,1)))
    # complete dispatch: allocate global residual via fixed cost merit order,
    # then adapt renewable dispatch to ensure enough demand for balance.
    conv=np.zeros((9,T));res=wind+solar
    for t in range(T):
        residual=float(load[:,t].sum()-res[:,t].sum())
        if residual<0:
            res[:,t]*=load[:,t].sum()/res[:,t].sum();residual=0
        if residual>cap.sum():raise ValueError('Synthetic generation shortage')
        for j in np.argsort(cost):
            conv[j,t]=min(cap[j],residual);residual-=conv[j,t]
    p_full=res+conv-load
    assert np.allclose(p_full.sum(axis=0),0,atol=1e-7)
    return d,cap,cost,res,wind,solar,load,conv,p_full


def run_demo(output,seed=20261016):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    d,cap,cost,res,wind,solar,load,conv,p=synthetic_system(seed)
    fA,rA=method_a(d,p)
    # B zero-optimisation balance convention, area independent support weights.
    fB,rB=method_b(d,wind+solar,load,cap/cap.sum())
    data=[]
    for label,importance,flows,ranks,metric in (
        ('A',rA.overload_MWh.to_numpy(),fA,rA,'overload_MWh'),
        ('B',rB.loading_mean.to_numpy(),fB,rB,'loading_mean')):
        zones=greedy_busmap(d,importance,5)
        assert_connected_zones(d,zones)
        agg=build_aggregation(d,zones)
        pz,fcut=agg.aggregate(p,fA) # SAME full physical reference across both busmaps
        refs={'uniform':uniform_reference(zones),
              'capacity':capacity_reference(zones,cap),
              'merit_order':merit_order_reference(zones,cap,cost)}
        # 80 calibration, 40 independent validation snapshots.
        split=80
        for name,R in refs.items():
            xref,href_rmse,href=fit_reference_ptdf(agg,d,R)
            ptrain=pz[:,:split];ptest=pz[:,split:]
            # Only exogenous high-resolution RES and load structure.
            _,fstruct=structure_correction(d,agg,R,{'wind':wind,'solar':solar,'load':-load})
            residual=fcut[:,:split]-href@ptrain-fstruct[:,:split]
            from scipy.linalg import null_space
            cycles=null_space(agg.A_z.toarray())
            c0=(cycles@cycles.T)@residual.mean(axis=1) if cycles.size else np.zeros(len(agg.pairs))
            target=fcut[:,split:]
            plain=href@ptest+c0[:,None]
            corrected=plain+fstruct[:,split:]
            rmse=lambda a:float(np.sqrt(np.mean((a-target)**2)))
            joint=fit_equivalent(agg,pz[:,:split],fcut[:,:split])
            joint_val=reduced_ptdf(agg.A_z.toarray(),joint.x)@ptest+joint.c0[:,None]
            choices=representative_buses(d,agg,R)
            data.append({'clustering':label,'reference':name,
                'reference_PTDFeq_RMSE':href_rmse,
                'validation_plain_RMSE_MW':rmse(plain),
                'validation_corrected_RMSE_MW':rmse(corrected),
                'validation_joint_fit_RMSE_MW':rmse(joint_val),
                'n_zones':len(np.unique(zones)),
                'n_cuts':len(agg.pairs),'cycle_rank':len(agg.pairs)-len(np.unique(zones))+1,
                'screening_coverage':capture_fraction(agg,ranks,metric),
                'busmap':zones.tolist(),
                'representative_buses':{str(k):v[0] for k,v in choices.items()},
                'status':'synthetic_dc_only'})
        pd.DataFrame({'bus':d.bus_names,'zone':zones}).to_csv(out/f'busmap_{label}.csv',index=False)
        pd.DataFrame({'from_zone':[v[0] for v in agg.pairs],
                      'to_zone':[v[1] for v in agg.pairs]}).to_csv(out/f'cuts_{label}.csv',index=False)
        # N-1 proxy, no guarantee that every cut has an identifiable limit.
        rho,invalid=n1_worst_loading(d,fA)
        seasons=np.array(['summer' if t%48<24 else 'winter' for t in range(fA.shape[1])])
        capacities=seasonal_directional_limits(agg,fA,rho,seasons)
        capacities.to_csv(out/f'security_limits_{label}.csv',index=False)
        with open(out/f'validation_{label}.json','w') as f:
            json.dump({'aggregation_identity':True,'invalid_n1_outages':[int(k) for k in invalid],
                'warning':'Empirical capacity estimates are not firm security guarantees'},f,indent=2)
    pd.DataFrame(data).to_csv(out/'comparison.csv',index=False)
    rA.to_csv(out/'rank_A.csv',index=False);rB.to_csv(out/'rank_B.csv',index=False)
    (out/'manifest.json').write_text(json.dumps({'seed':seed,'snapshots':p.shape[1],
        'pypsa_execution':False,'network':'synthetic 9 bus DC network',
        'data_source':'generated invented data; NOT ENTSO-E'},indent=2))
    return pd.DataFrame(data)
