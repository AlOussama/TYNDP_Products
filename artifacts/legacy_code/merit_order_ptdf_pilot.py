import numpy as np
from scipy.optimize import least_squares
import csv
rng=np.random.default_rng(20261016)
# Synthetic six-bus network: A={0,1}, B={2,3}, C={4,5}; MW/radians, DC model.
N=6; zones=np.array([0,0,1,1,2,2]); Z=3
lines=[(0,1,.12),(2,3,.15),(4,5,.13),(0,2,.22),(1,3,.30),(2,4,.25),(3,5,.28),(0,4,.40),(1,5,.36)]
L=len(lines); A=np.zeros((L,N)); x=np.array([e[2] for e in lines]);
for k,(i,j,_) in enumerate(lines): A[k,i]=1; A[k,j]=-1
B=A.T@np.diag(1/x)@A
# PTDF slack bus 5; applying zero-sum injections makes slack choice irrelevant.
H=np.zeros((L,N)); H[:,:5]=np.diag(1/x)@A[:,:5]@np.linalg.inv(B[:5,:5]);
# Interzonal physical cut flow: positive A->B, B->C, A->C.
Gamma=np.zeros((3,L)); pair_idx={(0,1):0,(1,2):1,(0,2):2}
for k,(i,j,_) in enumerate(lines):
 a,b=zones[i],zones[j]
 if a!=b: Gamma[pair_idx[tuple(sorted((a,b)))],k]=1 if a<b else -1
P=np.zeros((Z,N))
for i,z in enumerate(zones): P[z,i]=1
# capacities: node 0 nuclear 90, 1 gas 140, 2 coal 120, 3 gas 90, 4 nuclear 100, 5 gas 130;
# invented costs [30,100,45,95,32,110] EUR/MWh.
cap=np.array([90,140,120,90,100,130],float); cost=np.array([30,100,45,95,32,110],float)
Rcap=np.zeros((N,Z)); Rmo=np.zeros((N,Z)); Runif=np.zeros((N,Z))
# Pick three dispatch levels as fractions of nameplate to generate fixed merit-order probabilities.
levels=[.35,.6,.85]; pi=np.array([.3,.45,.25]);
for z in range(Z):
 ids=np.where(zones==z)[0]; Runif[ids,z]=1/len(ids); Rcap[ids,z]=cap[ids]/cap[ids].sum()
 mean=np.zeros(len(ids))
 for level,weight in zip(levels,pi):
  resid=level*cap[ids].sum(); p=np.zeros(len(ids))
  for q in np.argsort(cost[ids]):
   p[q]=min(cap[ids[q]],resid); resid-=p[q]
  mean+=weight*p
 Rmo[ids,z]=mean/mean.sum()
# RES and load footprints (fixed by zone), all signed load entries positive in matrix.
Rwind=np.zeros((N,Z)); Rsolar=np.zeros((N,Z)); Rload=np.zeros((N,Z))
for z in range(Z):
 ids=np.where(zones==z)[0]
 Rwind[ids,z]=[.85,.15]; Rsolar[ids,z]=[.15,.85]; Rload[ids,z]=[.4,.6]
assert np.allclose(P@Rcap,np.eye(Z)) and np.allclose(P@Rmo,np.eye(Z))
# Reduced 3-node triangle: A->B, B->C, A->C
Ar=np.array([[1.,-1,0],[0,1,-1],[1,0,-1]])
T=np.array([[1.,0],[0,1],[-1,-1]]) # independent, balanced zonal injections

def heq(xx):
 br=Ar.T@np.diag(1/xx)@Ar
 h=np.zeros((3,3)); h[:,:2]=np.diag(1/xx)@Ar[:,:2]@np.linalg.inv(br[:2,:2]); return h

def calibrate(R):
 target=Gamma@H@R@T
 fun=lambda v:(heq(np.exp(v))@T-target).ravel()
 sol=least_squares(fun,np.log(np.array([.24,.29,.42])),max_nfev=2000,xtol=1e-12,ftol=1e-12,gtol=1e-12)
 xx=np.exp(sol.x)
 return xx,np.linalg.norm(fun(sol.x)),heq(xx)
refs={'Uniform':Runif,'Capacity':Rcap,'Merit order':Rmo}
fits={name:calibrate(R) for name,R in refs.items()}
# Dispatch samples are merit-order biased but imperfect. Balanced demand across zones by scaling load.
samples=[]
for t in range(1000):
 conv=np.zeros(N)
 for z in range(Z):
  ids=np.where(zones==z)[0]; target=rng.uniform(.25,.85)*cap[ids].sum(); remaining=target
  for q in np.argsort(cost[ids]):
   avail=cap[ids[q]]*rng.uniform(.85,1)
   conv[ids[q]]=min(avail,remaining); remaining-=conv[ids[q]]
  # Allow some suboptimal plant use / dispatch variation while preserving zonal total
  i,j=ids; swap=rng.uniform(0,.20)*min(conv[i],cap[j]-conv[j]); conv[i]-=swap;conv[j]+=swap
 pconv=P@conv
 pw=rng.uniform(5,50,size=Z); ps=rng.uniform(3,30,size=Z)
 pl=rng.uniform(.7,1.3,size=Z); pl*= (sum(pconv)+sum(pw)+sum(ps))/sum(pl)
 pnode=conv+Rwind@pw+Rsolar@ps-Rload@pl
 assert abs(pnode.sum())<1e-7
 samples.append((pconv,pw,ps,pl,pnode))
rows=[]
for name,R in refs.items():
 xx,fiterr,hr=fits[name]
 err0=[];err1=[];actual=[]
 for pc,pw,ps,pl,pnode in samples:
  pz=pc+pw+ps-pl
  true=Gamma@H@pnode
  plain=hr@pz
  correction=Gamma@H@((Rwind-R)@pw+(Rsolar-R)@ps-(Rload-R)@pl)
  corrected=plain+correction
  err0.extend(plain-true);err1.extend(corrected-true);actual.extend(true)
 root=lambda a:float(np.sqrt(np.mean(np.asarray(a)**2)))
 rows.append({'reference':name,'x_AB_pu':float(xx[0]),'x_BC_pu':float(xx[1]),'x_AC_pu':float(xx[2]),'PTDF_fit_frobenius':float(fiterr),'RMSE_plain_MW':root(err0),'RMSE_corrected_MW':root(err1),'reference_flow_RMS_MW':root(actual)})
with open('/mnt/data/merit_order_ptdf_results.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('REF WEIGHTS')
for k,r in refs.items():print(k,np.round([r[i,zones[i]] for i in range(N)],3))
print('RESULTS')
for r in rows:print(r)
