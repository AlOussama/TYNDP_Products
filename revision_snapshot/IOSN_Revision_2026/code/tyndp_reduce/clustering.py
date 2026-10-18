"""Simple connected-graph greedy contractions for a transparent initial busmap.

Prototype: edge cost reflects information LOST by merging endpoints;
only connected clusters merge, with hard country-group barriers optional.
Unlike the ENTSO-E method this is NOT an exact published algorithm.
"""
import numpy as np


def greedy_busmap(detailed, edge_importance, n_zones, regions=None, locked_edges=None):
    n=detailed.n; edge_importance=np.asarray(edge_importance,float)
    if n_zones<1 or n_zones>n or edge_importance.shape!=(detailed.l,):
        raise ValueError("n_zones or edge_importance invalid")
    region=np.zeros(n,dtype=int) if regions is None else np.asarray(regions)
    if region.shape!=(n,): raise ValueError("regions length mismatch")
    locked=set() if locked_edges is None else set(locked_edges)
    parent=list(range(n)); groups=[{i} for i in range(n)]
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    count=n
    while count>n_zones:
        best=None
        for k,(u,v) in enumerate(zip(detailed.bus0,detailed.bus1)):
            a,b=find(int(u)),find(int(v))
            if a==b or k in locked: continue
            if region[next(iter(groups[a]))]!=region[next(iter(groups[b]))]:continue
            # Cost of contracting ALL ties between components, not merely one edge.
            cut_edges=[j for j,(s,t) in enumerate(zip(detailed.bus0,detailed.bus1))
                      if {find(int(s)),find(int(t))}=={a,b}]
            if any(j in locked for j in cut_edges): continue
            score=sum(max(0.,edge_importance[j]) for j in cut_edges)
            candidate=(score,min(a,b),max(a,b))
            if best is None or candidate<best[0]: best=(candidate,a,b)
        if best is None: raise ValueError("Cannot reach requested zone count without breaking constraints")
        _,a,b=best;root=min(a,b);other=max(a,b)
        parent[other]=root;groups[root]|=groups[other];groups[other]=set();count-=1
    reps=sorted(set(find(i) for i in range(n)))
    remap={r:j for j,r in enumerate(reps)}
    return np.array([remap[find(i)] for i in range(n)],dtype=int)


def protected_indices(scores,top_k):
    scores=np.asarray(scores,float)
    return set(np.argsort(-scores)[:top_k].tolist())


def assert_connected_zones(detailed,busmap):
    z=np.asarray(busmap)
    for zone in np.unique(z):
        members=set(np.flatnonzero(z==zone).tolist())
        seen={next(iter(members))};stack=list(seen)
        while stack:
            u=stack.pop()
            for a,b in zip(detailed.bus0,detailed.bus1):
                v=int(b) if int(a)==u else (int(a) if int(b)==u else None)
                if v is not None and v in members and v not in seen:
                    seen.add(v);stack.append(v)
        if seen!=members: raise AssertionError(f"Disconnected cluster {zone}")
    return True
