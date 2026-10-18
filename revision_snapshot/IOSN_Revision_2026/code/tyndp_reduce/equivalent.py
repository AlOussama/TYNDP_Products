"""Fit physically realizable reduced DC sensitivity with constrained constant F0.

All interzonal branches have positive x. Global x scale is unidentifiable;
the first reactance is anchored to a chosen initial scale. No claim that
this matches ENTSO-E's unpublished internal optimization algorithm.
"""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import least_squares
from scipy.linalg import null_space


@dataclass
class EquivalentFit:
    x: np.ndarray
    c0: np.ndarray
    predicted: np.ndarray
    residual_rmse: float
    success: bool
    message: str


def reduced_ptdf(Az,x):
    a=np.asarray(Az,float);x=np.asarray(x,float)
    z,e=a.shape
    if np.any(x<=0) or len(x)!=e: raise ValueError("Invalid reduced reactances")
    b=1/x;L=(a*b[None,:])@a.T
    H=np.zeros((e,z));H[:,1:]=(b[:,None]*a[1:,:].T)@np.linalg.inv(L[1:,1:])
    return H


def fit_equivalent(agg,zonal_injections,target_flows,initial_x=None,
                   regularization=1e-3,offset_penalty=0.02,known_structure=None):
    """Fit Heq(x) p_z + c0 + known_structure to physical target cut flows.

    `known_structure` if supplied must be available also during prediction;
    not an invisible run-time correction. All inputs E,T / Z,T.
    """
    Az=agg.A_z.toarray();Z,E=Az.shape
    P=np.asarray(zonal_injections,float);Targ=np.asarray(target_flows,float)
    if P.ndim!=2 or P.shape[0]!=Z or Targ.shape!=(E,P.shape[1]):
        raise ValueError("Wrong shapes for reduced fit")
    if not np.allclose(P.sum(axis=0),0,atol=1e-7):raise ValueError("Zonal injections not balanced")
    if not np.allclose(Az@Targ,P,atol=1e-7):raise ValueError("Target cut-flow violates zonal balance")
    if E==0:raise ValueError("At least one interzonal branch required")
    init=np.ones(E) if initial_x is None else np.asarray(initial_x,float)
    if len(init)!=E or np.any(init<=0):raise ValueError("initial_x must be positive")
    c_basis=null_space(Az)
    fixed=np.zeros_like(Targ) if known_structure is None else np.asarray(known_structure,float)
    if fixed.shape!=Targ.shape or not np.allclose(Az@fixed,0,atol=1e-7):
        raise ValueError("Known structure must be divergence-free E,T")
    scale=max(1,float(np.sqrt(np.mean(Targ*Targ))))
    def unpack(z):
        x=init.copy()
        if E>1: x[1:]=init[1:]*np.exp(np.clip(z[:E-1],-10,10))
        c=c_basis@z[E-1:] if c_basis.shape[1] else np.zeros(E)
        return x,c
    def resid(z):
        x,c=unpack(z)
        try:
            pr=reduced_ptdf(Az,x)@P+c[:,None]+fixed
            err=(pr-Targ).ravel()/scale
        except np.linalg.LinAlgError:
            err=np.full(Targ.size,1e6)
        reg=np.sqrt(regularization)*z[:E-1]
        regc=np.sqrt(offset_penalty)*z[E-1:]/scale
        return np.r_[err,reg,regc]
    result=least_squares(resid,np.zeros(E-1+c_basis.shape[1]),max_nfev=500,ftol=1e-10,xtol=1e-10)
    x,c=unpack(result.x)
    pred=reduced_ptdf(Az,x)@P+c[:,None]+fixed
    return EquivalentFit(x,c,pred,float(np.sqrt(np.mean((pred-Targ)**2))),result.success,str(result.message))


def fit_reference_ptdf(agg,detailed,Rref,initial_x=None,regularization=1e-4):
    """Project a chosen effective zonal Href=Gamma Hd Rref onto passive x.

    Gauge-free calibration uses independent balanced columns T=[I;-1].
    Anchors x[0]; output is (x, fitting residual, Heq). c0 not fitted here.
    """
    from scipy.optimize import least_squares
    AZ=agg.A_z.toarray();Z,E=AZ.shape
    if Z<2 or E<1:raise ValueError('Reduced graph too small')
    R=np.asarray(Rref,float)
    if not np.allclose(agg.P@R,np.eye(Z)):raise ValueError('P Rref != I')
    T=np.vstack([np.eye(Z-1),-np.ones((1,Z-1))])
    target=(agg.Gamma@detailed.ptdf()@R)@T
    x0=np.ones(E) if initial_x is None else np.asarray(initial_x,float)
    def fun(v):
        x=x0.copy()
        if E>1:x[1:]=x0[1:]*np.exp(np.clip(v,-8,8))
        try:res=(reduced_ptdf(AZ,x)@T-target).ravel()
        except np.linalg.LinAlgError:res=np.full(target.size,1e5)
        return np.r_[res,np.sqrt(regularization)*v]
    opt=least_squares(fun,np.zeros(E-1),max_nfev=500)
    xx=x0.copy()
    if E>1:xx[1:]=x0[1:]*np.exp(opt.x)
    heq=reduced_ptdf(AZ,xx)
    return xx,float(np.sqrt(np.mean((heq@T-target)**2))),heq
