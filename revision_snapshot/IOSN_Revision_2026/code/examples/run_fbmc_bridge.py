"""Reproducible static FBMC research example using the shared synthetic grid.

python examples/run_fbmc_bridge.py

All quantities synthetic, NOT market-published Core/Jao data.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from tyndp_reduce.demo import synthetic_system
from tyndp_reduce.fbmc_bridge import (
    market_partition,gsk_uniform,gsk_from_positive_weights,cnec_operator,
    build_domain,select_sensitive_cnecs,bilateral_capacity,structural_offset)


def run(output):
    d,cap,cost,res,wind,solar,load,conv,p=synthetic_system()
    # These are MARKET zones, independent of the A/B planning-cluster busmaps.
    P=market_partition([0,0,0,1,1,1,2,2,2])
    choices={'uniform':gsk_uniform(P),
             'capacity':gsk_from_positive_weights(P,cap),
             'merit_order':gsk_from_positive_weights(P,cap/(1+cost/50))}
    # Deliberately indicative marginal-cost weighting, not actual TSO GLSK.
    reference=.25*p[:,:80].mean(axis=1)
    reference-=reference.mean()  # numerical balance projection of toy forecast
    H=d.ptdf()
    monitored=[];outages=[];identifiers=[]
    for l in range(d.l):
        monitored.append(l);outages.append(None);identifiers.append(f'{d.line_names[l]} N0')
    from tyndp_reduce.security import bodf_from_ptdf
    _,invalid=bodf_from_ptdf(d)
    for k in range(d.l):
        if k in invalid: continue
        for l in range(d.l):
            if l!=k:
                monitored.append(l);outages.append(k)
                identifiers.append(f'{d.line_names[l]} outage {d.line_names[k]}')
    K=cnec_operator(d,monitored,outages)
    fmax=d.limit[monitored];frm=.10*fmax
    rows=[];domains={}
    for name,G in choices.items():
        dom=build_domain(H,P,G,K,reference,fmax,frm,labels=identifiers)
        good=select_sensitive_cnecs(dom, .05)
        # Candidate selection retains both signs for each screened CNEC.
        idx=np.r_[np.flatnonzero(good),np.flatnonzero(good)+len(good)]
        # Use all constraints in this demonstration; screening is diagnostic.
        rows.append({'gsk':name,'market_zones':P.shape[0],
                     'candidate_CNEC_N0_N1':len(monitored),
                     'candidate_with_sensitivity_ge_5pct':int(good.sum()),
                     'zero_NP_offset_rmse_MW':float(np.sqrt(np.mean(dom.f0**2))),
                     'bilateral_A_to_B_MW':bilateral_capacity(dom,0,1),
                     'bilateral_A_to_C_MW':bilateral_capacity(dom,0,2),
                     'reference_feasible':dom.feasible(dom.np_ref),
                     'status':'synthetic research, no official RAM or markets'})
        domains[name]=dom
        assert np.allclose(dom.f0,structural_offset(H,P,G,K,reference),atol=1e-7)
        assert np.allclose(dom.f_ref,dom.zonal_ptdf@dom.np_ref+dom.f0,atol=1e-7)
    result=pd.DataFrame(rows)
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    result.to_csv(out/'fbmc_gsk_comparison.csv',index=False)
    for name,dom in domains.items():
        df=pd.DataFrame(dom.coefficient,columns=['market_zone_A','market_zone_B','market_zone_C'])
        df.insert(0,'CNEC_direction',dom.labels)
        df['RAM_MW']=dom.ram
        df.to_csv(out/f'fbmc_domain_{name}.csv',index=False)
    print(result.to_string(index=False))
    return result


if __name__=='__main__':
    run(Path(__file__).resolve().parents[1]/'outputs'/'fbmc')
