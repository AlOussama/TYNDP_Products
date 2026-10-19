"""Narrow PyPSA 1.4 adapter. Never silently drop unsupported components.

Tested mathematically in isolation. Runtime with PyPSA must be validated
externally where pypsa is installed. This adapter rejects transformers,
nonzero phase shifts, Links, Stores and StorageUnits as a safety gate.
"""
import numpy as np
import pandas as pd
from .dc import DetailedDC


def require_pypsa():
    try: import pypsa
    except ImportError as e:
        raise RuntimeError("Install PyPSA: pip install 'pypsa>=1.4,<2'; not present here") from e
    return pypsa


def from_pypsa_network(n,ac_voltage_tolerance=1e-6):
    """Build a lossless single-island line-only DC kernel from network.

    n.lpf() is called to construct effective x values. Generators/loads
    must already have correct snapshot time series. Extra components
    are REJECTED rather than silently disregarded.
    """
    require_pypsa()
    for attribute in ('transformers','links','storage_units','stores'):
        df=getattr(n,attribute)
        if len(df)>0:
            raise NotImplementedError(f"{attribute} requires explicit topology/injection adapter")
    if len(n.lines)==0:raise ValueError("No AC lines")
    if 'phase_shift' in n.lines and np.any(np.abs(n.lines.phase_shift.fillna(0))>ac_voltage_tolerance):
        raise NotImplementedError("Nonneutral phase shifts require explicit affine offsets")
    if 'v_nom' in n.buses:
        for line in n.lines.itertuples():
            va=n.buses.at[line.bus0,'v_nom'];vb=n.buses.at[line.bus1,'v_nom']
            if abs(float(va)-float(vb))>ac_voltage_tolerance:
                raise NotImplementedError("Mismatched voltage levels: explicit transformer needed")
    n.lpf()  # creates x_pu_eff and DC subnetworks
    buses=list(map(str,n.buses.index));names=list(map(str,n.lines.index))
    pos={b:i for i,b in enumerate(buses)}
    x=n.lines['x_pu_eff'].to_numpy(dtype=float)
    rating=n.lines['s_nom'].to_numpy(dtype=float)
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(rating)):
        raise ValueError("Finite x_pu_eff and s_nom required")
    d=DetailedDC(tuple(buses),tuple(names),n.lines.bus0.map(pos).to_numpy(int),
                n.lines.bus1.map(pos).to_numpy(int),x,rating)
    return d


def aggregate_with_pypsa(n,zone_by_bus):
    """Use PyPSA's built-in busmap, then re-calibrate x/c0/limits separately."""
    require_pypsa()
    busmap=pd.Series({str(k):str(v) for k,v in zone_by_bus.items()})
    if not n.buses.index.astype(str).isin(busmap.index).all():
        raise ValueError("Incomplete busmap")
    cluster=n.cluster.spatial.get_clustering_from_busmap(busmap,with_time=True)
    return cluster.n,cluster.linemap


def injected_time_series(n,field='p'):
    """Read a restricted Generator/Load-only balanced nodal time series.

    For complete Marktdispatch integrations, implement Storage/Link/HVDC
    adapters with correct endpoint signs, and never use this shortcut.
    """
    require_pypsa()
    if any(len(getattr(n,name)) for name in ('links','storage_units','stores')):
        raise NotImplementedError("Links/storage not handled; add explicit endpoint injection mapping")
    buses=n.buses.index.astype(str);times=n.snapshots
    p=pd.DataFrame(0.,index=times,columns=buses)
    for component,static,dynamic,sgn in (
        ('Generator',n.generators,n.generators_t,+1),('Load',n.loads,n.loads_t,-1)):
        if len(static)==0:continue
        table=None
        if field=='p' and component=='Generator' and 'p' in dynamic and not dynamic.p.empty:
            table=dynamic.p
        elif 'p_set' in dynamic and not dynamic.p_set.empty:
            table=dynamic.p_set
        for name,row in static.iterrows():
            if table is not None and name in table.columns:
                v=table[name].reindex(times).astype(float)
            else:
                v=pd.Series(float(row.get('p_set',0.)),index=times)
            p[str(row['bus'])]+=sgn*v.to_numpy()
    pp=p.to_numpy().T
    if not np.allclose(pp.sum(axis=0),0,atol=1e-5):
        raise ValueError("Nodal injections are unbalanced: do not hide slack dispatch")
    return pp
