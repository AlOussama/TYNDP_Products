"""Exact zonal incidence and oriented physical-cut operators."""
from dataclasses import dataclass
import numpy as np
from scipy.sparse import csr_matrix


@dataclass
class Aggregation:
    P: csr_matrix
    Gamma: csr_matrix
    A_z: csr_matrix
    pairs: list[tuple[int,int]]
    zone_of_bus: np.ndarray

    def verify(self, detailed, atol=1e-12):
        residual=(self.A_z@self.Gamma-self.P@csr_matrix(detailed.incidence())).toarray()
        if not np.allclose(residual,0,atol=atol):
            raise AssertionError(f"A_z Gamma != P A_d, max={np.max(np.abs(residual))}")
        return True

    def aggregate(self,p,f):
        p=np.asarray(p);f=np.asarray(f)
        return self.P@p,self.Gamma@f


def build_aggregation(detailed,busmap):
    """busmap length N, each integer zone present, edge aggregation by zone pair."""
    z=np.asarray(busmap,dtype=int)
    if z.shape!=(detailed.n,) or np.any(z<0): raise ValueError("busmap length/values invalid")
    unique=np.unique(z)
    if not np.array_equal(unique,np.arange(len(unique))):
        raise ValueError("Zones must be consecutive 0..Z-1")
    Z=len(unique); P=csr_matrix((np.ones(detailed.n),(z,np.arange(detailed.n))),shape=(Z,detailed.n))
    pairs=sorted({tuple(sorted((int(z[i]),int(z[j]))))
                  for i,j in zip(detailed.bus0,detailed.bus1) if z[i]!=z[j]})
    edges={pair:pos for pos,pair in enumerate(pairs)}
    rows=[];cols=[];vals=[]
    for ell,(i,j) in enumerate(zip(detailed.bus0,detailed.bus1)):
        zi,zj=int(z[i]),int(z[j]);
        if zi==zj: continue
        rows.append(edges[tuple(sorted((zi,zj)))]);cols.append(ell)
        vals.append(1.0 if zi<zj else -1.0)
    Gamma=csr_matrix((vals,(rows,cols)),shape=(len(pairs),detailed.l))
    az=csr_matrix((np.r_[np.ones(len(pairs)),-np.ones(len(pairs))],
        (np.r_[np.array([x for x,_ in pairs]),np.array([y for _,y in pairs])],
         np.tile(np.arange(len(pairs)),2))),shape=(Z,len(pairs)))
    agg=Aggregation(P,Gamma,az,pairs,z)
    agg.verify(detailed)
    return agg
