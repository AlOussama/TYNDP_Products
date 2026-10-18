"""Reference distributions, technology footprints and representative bus selection."""
import numpy as np


def uniform_reference(zones):
    zones=np.asarray(zones,int); Z=int(zones.max())+1;N=len(zones)
    R=np.zeros((N,Z))
    for z in range(Z):
        ids=np.flatnonzero(zones==z);R[ids,z]=1/len(ids)
    return R


def capacity_reference(zones,capacities):
    z=np.asarray(zones,int);cap=np.asarray(capacities,float)
    if np.any(cap<0) or len(cap)!=len(z): raise ValueError("Invalid capacities")
    R=uniform_reference(z)
    for k in range(R.shape[1]):
        ids=np.flatnonzero(z==k)
        if cap[ids].sum()>0: R[ids,k]=cap[ids]/cap[ids].sum()
    return R


def merit_order_reference(zones,capacities,marginal_costs,levels=(.35,.60,.85),weights=(.3,.45,.25)):
    """Fixed screening merit-order reference, NOT an economic dispatch model.

    Dispatch each zone independently across explicitly weighted demand levels.
    Weighted zero-demand zones use uniform fallback. No ramp/start-up/network limits.
    """
    z=np.asarray(zones,int);cap=np.asarray(capacities,float);cost=np.asarray(marginal_costs,float)
    levels=np.asarray(levels,float);w=np.asarray(weights,float)
    if not (len(z)==len(cap)==len(cost)): raise ValueError("Input length mismatch")
    if np.any(cap<0) or np.any(~np.isfinite(cost)) or np.any(levels<0) or np.any(levels>1):
        raise ValueError("Invalid cost, capacity or demand level")
    if np.any(w<0) or len(w)!=len(levels) or not np.isclose(w.sum(),1):
        raise ValueError("Invalid scenario weights")
    R=uniform_reference(z)
    for zone in range(R.shape[1]):
        ids=np.flatnonzero(z==zone); accum=np.zeros(len(ids))
        order=np.argsort(cost[ids],kind='stable')
        for level,weight in zip(levels,w):
            rem=level*cap[ids].sum();out=np.zeros(len(ids))
            for k in order:
                out[k]=min(rem,cap[ids[k]]);rem-=out[k]
            accum+=weight*out
        if accum.sum()>0:R[ids,zone]=accum/accum.sum()
    return R


def technology_reference(zones,technology_by_bus,defaults=None):
    """Build R_k(t) of shape N,Z,T from nodal nonnegative quantities N,T.

    Zero-output zone snapshots use a documented fallback distribution.
    """
    z=np.asarray(zones,int);qty=np.asarray(technology_by_bus,float)
    if qty.ndim!=2 or qty.shape[0]!=len(z) or np.any(qty<0):
        raise ValueError("technology_by_bus must be nonnegative (N,T)")
    N,T=qty.shape;Z=z.max()+1
    default=uniform_reference(z) if defaults is None else np.asarray(defaults,float)
    out=np.zeros((N,Z,T))
    for k in range(Z):
        idx=np.flatnonzero(z==k);den=qty[idx,:].sum(axis=0)
        for t in range(T):
            out[idx,k,t]=qty[idx,t]/den[t] if den[t]>0 else default[idx,k]
    return out


def representative_buses(detailed,aggregation,R,H=None):
    """Select one physical bus per zone closest to its weighted PTDF column.

    This is a local sensitivity heuristic; combined-node realizability
    and reference balancing must be tested separately.
    """
    H=detailed.ptdf() if H is None else H
    HD=aggregation.Gamma@H
    scores=HD@R
    choices={}
    for zone in range(R.shape[1]):
        candidates=np.flatnonzero(aggregation.zone_of_bus==zone)
        delta=HD[:,candidates]-scores[:,zone,None]
        idx=int(candidates[np.argmin(np.linalg.norm(delta,axis=0))])
        choices[zone]=(detailed.bus_names[idx],float(np.linalg.norm(HD[:,idx]-scores[:,zone])))
    return choices
