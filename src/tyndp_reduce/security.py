"""N-1 screening and diagnostic seasonal/directional limit identification.

Important: point-cloud-based transfer limits are empirical proxies, NOT
formal universal N-1 certificates or ENTSO-E's internal estimator.
"""
import numpy as np
import pandas as pd


def bodf_from_ptdf(detailed,atol=1e-8):
    H=detailed.ptdf();a=detailed.incidence();D=H@a
    m=detailed.l;B=np.zeros((m,m));invalid=[]
    for k in range(m):
        denom=1-D[k,k]
        if abs(denom)<atol:
            B[:,k]=np.nan;invalid.append(k)
        else:
            B[:,k]=D[:,k]/denom
            B[k,k]=-1
    return B,invalid


def n1_worst_loading(detailed,flows,contingencies=None,monitor=None):
    """Return (L,T) max(N0,N1) stress, `invalid` islanding/non-identifiable outages."""
    flows=np.asarray(flows,float)
    if flows.ndim!=2 or flows.shape[0]!=detailed.l:raise ValueError("flows L,T required")
    B,invalid=bodf_from_ptdf(detailed)
    cand=range(detailed.l) if contingencies is None else contingencies
    mask=np.ones(detailed.l,dtype=bool) if monitor is None else np.asarray(monitor,dtype=bool)
    rho=np.abs(flows)/detailed.limit[:,None]
    for k in cand:
        if k in invalid:continue
        post=flows+B[:,k,None]*flows[k,None,:]
        stress=np.abs(post)/detailed.limit[:,None]
        stress[k,:]=0
        stress[~mask,:]=0
        rho=np.maximum(rho,stress)
    return rho,invalid


def seasonal_directional_limits(agg,detail_flows,stress,season,minimum=12,
                                min_correlation=.75,minimum_observed_rho=.25):
    """Regress stress on |cut-flow| with intercept, solve for rho=1.

    NaN returned if identifiable conditions fail. Empirical proxy, not proof.
    """
    fcut=np.asarray(agg.Gamma@detail_flows,float)
    rho=np.asarray(stress,float)
    season=np.asarray(season)
    if season.shape!=(fcut.shape[1],):raise ValueError("season length mismatch")
    rows=[]
    for e,(i,j) in enumerate(agg.pairs):
        original_lines=agg.Gamma.getrow(e).indices
        stress_e=rho[original_lines,:].max(axis=0)
        for label in sorted(set(season.tolist())):
            for direction in (+1,-1):
                mask=(season==label)&(fcut[e]*direction>1e-7)
                xx=np.abs(fcut[e,mask]); yy=stress_e[mask]
                result={"zone_from":i,"zone_to":j,"season":str(label),"direction":direction,
                        "n":len(xx),"correlation":float('nan'),"limit_MW":float('nan'),
                        "status":"insufficient_data"}
                if len(xx)>=minimum and np.std(xx)>1e-8 and np.std(yy)>1e-8:
                    corr=float(np.corrcoef(xx,yy)[0,1]);result['correlation']=corr
                    slope,intercept=np.polyfit(xx,yy,1)
                    if corr<min_correlation or slope<=0:
                        result['status']='weak_relationship'
                    elif yy.max()<minimum_observed_rho:
                        result['status']='insufficient_stress_range'
                    elif (1-intercept)/slope<=0:
                        result['status']='nonpositive_intercept_solution'
                    else:
                        result['limit_MW']=float((1-intercept)/slope)
                        result['status']='estimated_extrapolated' if yy.max()<1 else 'estimated_interpolated'
                rows.append(result)
    return pd.DataFrame(rows)
