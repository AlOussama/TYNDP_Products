"""Separate A-overload and B-general-loading rankings."""
import numpy as np
import pandas as pd
from .dc import balanced_from_exogenous


def method_a(detailed,p_dispatch,hours=None):
    flows=detailed.flows(p_dispatch)
    w=np.ones(flows.shape[1]) if hours is None else np.asarray(hours,dtype=float)
    over=np.maximum(np.abs(flows)-detailed.limit[:,None],0.)
    return flows,pd.DataFrame({"line":detailed.line_names,
        "overload_MWh":over@w,
        "overload_hours":(over>0)@w,
        "relative_loading_mean":(np.abs(flows)/detailed.limit[:,None])@w/w.sum()})


def method_b(detailed,res_available,load,balancing_weights,hours=None):
    q=np.asarray(res_available)-np.asarray(load)
    p=balanced_from_exogenous(q,balancing_weights)
    flows=detailed.flows(p)
    w=np.ones(flows.shape[1]) if hours is None else np.asarray(hours,float)
    rel=np.abs(flows)/detailed.limit[:,None]
    return flows,pd.DataFrame({"line":detailed.line_names,
        "transport_MWh":np.abs(flows)@w,
        "loading_mean":rel@w/w.sum(),
        "loading_p95":np.quantile(rel,0.95,axis=1)})


def capture_fraction(agg,ranking,metric):
    val=np.asarray(ranking[metric],dtype=float)
    mask=(agg.Gamma.getnnz(axis=0)>0)
    return float(val[mask].sum()/val.sum()) if val.sum()>0 else 1.0
