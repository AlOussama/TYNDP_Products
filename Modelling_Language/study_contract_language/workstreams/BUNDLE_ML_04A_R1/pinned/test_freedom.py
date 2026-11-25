"""Finite exact synthetic controls; no general E4/E5 or real-model claims."""
from fractions import Fraction as F
from itertools import product
import unittest,platform
P=product
class Freedom(unittest.TestCase):
    def test_RC01_battery(self):
        # Injection positive, half-hour intervals, charge efficiency 0.8, discharge 1, Emax=4 MWh.
        dt=F(1,2);eta=F(4,5);cap=F(4)
        def energy(p):
            state=F(2)
            for x in p:
                state+=dt*(-x*eta if x<0 else -x)
                if not 0<=state<=cap:return False
            return state==2
        def soc(p):
            state=F(1,2)
            for x in p:
                state+=dt*(-x*eta if x<0 else -x)/cap
                if not 0<=state<=1:return False
            return state==F(1,2)
        traces=list(P([-2,-1,0,1,2],repeat=3));a={p for p in traces if energy(p)};b={p for p in traces if soc(p)}
        self.assertEqual(a,b);self.assertTrue(a);self.assertFalse(energy((-2,-2,-2)));self.assertEqual(-2*dt,-1)
    def test_RC02_EV(self):
        # EV1 leaves after t0; EV2 after t1, each needs 1 MWh, 1 MW per slot.
        individual=[]
        for a,b,c in P((0,1),repeat=3):
            if a==1 and b+c==1:individual.append((a+b,c))
        aggregate={p for p in P(range(3),range(2)) if sum(p)==2 and 1<=p[0]<=2 and p[1]<=1}
        self.assertEqual(set(individual),aggregate);self.assertNotIn((0,2),aggregate)
        # Total 2 MWh does not prove the deadlines; EV1 gets 0 in t0, EV2 overcharged later.
        self.assertEqual(sum((0,2)),2)
    def test_RC03_electrolysis(self):
        # Synthetic LHV=1/30 MWh/kg, common external efficiency envelope 0.6..0.8.
        lhv=F(1,30);pows=(1,2,3,4)
        a=[(p,21*p) for p in pows];b=[(p,18*p if p<=2 else 24*p) for p in pows]
        def contract(pair):
            p,h=pair;return p>=0 and h>=0 and F(3,5)*p<=h*lhv<=F(4,5)*p
        self.assertTrue(all(map(contract,a+b)));self.assertNotEqual(a,b);self.assertFalse(contract((1,30)))
        # These models satisfy the common sampled envelope, not identical feasible sets.
    def test_RC04_H2(self):
        # No energy conversion without declared LHV. Synthetic 1/30 MWh/kg.
        lhv=F(1,30);dt=F(1,2);loss=F(1,10);m=F(60);e=m*lhv
        for f in (12,-4,0,8):
            m=(1-loss)*m+dt*f;e=(1-loss)*e+dt*f*lhv;self.assertEqual(e,m*lhv);self.assertTrue(m>=0)
        self.assertNotEqual(e,m);self.assertNotEqual(e,m*F(1,25))
    def test_RC05_grid(self):
        # Oriented triangle 0->1->2->0, x=1, flow=(theta0-theta1,...), theta0=0.
        flows=set(P(range(-2,3),repeat=3))
        def kcl(f):return (f[0]-f[2],f[1]-f[0],f[2]-f[1])
        cycle={f for f in flows if sum(f)==0 and all(abs(v)<=2 for v in kcl(f))}
        angles=set()
        for t1,t2 in P(range(-2,3),repeat=2):
            f=(-t1,t1-t2,t2)
            if f in flows and all(abs(v)<=2 for v in kcl(f)):angles.add(f)
        self.assertEqual(cycle,angles);self.assertEqual(kcl((1,1,1)),(0,0,0));self.assertNotIn((1,1,1),cycle)
    def test_RC06_expansion(self):
        discrete={(n,10*n) for n in range(4)};binary={(a+2*b,10*(a+2*b)) for a,b in P((0,1),repeat=2)};self.assertEqual(discrete,binary);self.assertNotIn((F(3,10),3),discrete)
    def test_RC07_information(self):
        shared={(x,x,y,z) for x,y,z in P(range(3),repeat=3)};explicit={v for v in P(range(3),repeat=4) if v[0]==v[1]};self.assertEqual(shared,explicit);self.assertNotIn((0,1,0,0),explicit)
if __name__=='__main__':print('Python',platform.python_version(),flush=True);unittest.main(verbosity=2)
