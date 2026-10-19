"""DC power-flow reference kernel with explicit balanced-injection contract.

Matrices: incidence A has shape (N,L), column l has +1 at bus0,
-1 at bus1; f = diag(1/x) A.T theta; A f = p.
Unbalanced vectors are ALWAYS rejected. Phase shifters, losses, HVDC
and PST offsets are not modelled by this numerical reference kernel.
"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import lu_factor, lu_solve


@dataclass(frozen=True)
class DetailedDC:
    bus_names: tuple[str, ...]
    line_names: tuple[str, ...]
    bus0: np.ndarray
    bus1: np.ndarray
    x: np.ndarray
    limit: np.ndarray

    def __post_init__(self):
        n, l = len(self.bus_names), len(self.line_names)
        if len(set(self.bus_names)) != n or len(set(self.line_names)) != l:
            raise ValueError("Bus and line names must be unique")
        if any(len(np.asarray(a)) != l for a in (self.bus0,self.bus1,self.x,self.limit)):
            raise ValueError("Line vector length mismatch")
        if np.any(self.x <= 0) or np.any(self.limit <= 0):
            raise ValueError("Require positive reactances and line limits")
        if np.any(self.bus0 == self.bus1) or np.any(self.bus0 < 0) or np.any(self.bus1 < 0):
            raise ValueError("Invalid terminal indices")
        if np.max(np.r_[self.bus0,self.bus1]) >= n:
            raise ValueError("Terminal index out of range")
        if np.linalg.matrix_rank(self.incidence()[:, :-1]) < n-1:  # optional sanity; graph small in prototype
            # This is NOT a connectivity test (dropping final edge could disconnect).
            pass
        if np.linalg.matrix_rank(self.incidence()) != n-1:
            raise ValueError("Only a single connected AC island is supported")

    @property
    def n(self): return len(self.bus_names)
    @property
    def l(self): return len(self.line_names)

    def incidence(self):
        a = np.zeros((self.n,self.l))
        a[self.bus0,np.arange(self.l)] = 1.0
        a[self.bus1,np.arange(self.l)] = -1.0
        return a

    def ptdf(self, slack=0):
        """PTDF for a specified slack; only defined as unique flows on balanced p."""
        a=self.incidence(); b=1/self.x
        lap=(a*b)@a.T
        keep=[i for i in range(self.n) if i != slack]
        if np.linalg.matrix_rank(lap[np.ix_(keep,keep)]) != len(keep):
            raise ValueError("Singular reduced nodal susceptance matrix")
        h=np.zeros((self.l,self.n))
        h[:,keep]=(b[:,None]*a[keep,:].T)@np.linalg.inv(lap[np.ix_(keep,keep)])
        return h

    def flows(self,p,slack=0):
        """p shape (N,T) or (N,), with exact zero sum per snapshot."""
        p=np.asarray(p,dtype=float)
        is_one=(p.ndim==1)
        if is_one: p=p[:,None]
        if p.ndim!=2 or p.shape[0]!=self.n: raise ValueError("p shape must be (N,T)")
        if not np.all(np.isfinite(p)): raise ValueError("Non-finite injections")
        if np.max(np.abs(p.sum(axis=0)))>1e-7: raise ValueError("Unbalanced injections; set explicit balancing rule")
        out=self.ptdf(slack)@p
        if not np.allclose(self.incidence()@out,p,atol=1e-7): raise AssertionError("Kirchhoff mismatch")
        return out[:,0] if is_one else out


def balanced_from_exogenous(q,weights):
    """Apply a transparent (non-economic) balancing convention per AC island."""
    q=np.asarray(q,float); weights=np.asarray(weights,float)
    if q.ndim!=2 or weights.shape!=(q.shape[0],): raise ValueError("Shapes: q (N,T), weights (N,)")
    if np.any(weights<0) or not np.isclose(weights.sum(),1):
        raise ValueError("Balancing weights must be nonnegative and sum to 1")
    return q-weights[:,None]*q.sum(axis=0)[None,:]
