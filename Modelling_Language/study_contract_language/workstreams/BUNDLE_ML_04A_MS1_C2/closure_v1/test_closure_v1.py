"""New targeted controls; no original full-chain paths are counted."""
import sys,json,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from interface import finite_consumer
from closure import admit,Reject
from package_interface import export_package
from test_closure import fixture,q,arithmetic,timepolicy,dataset,series,relation_fixture
from closure_v1 import metadata

def pkg(d,c):return export_package(admit(json.dumps(d),c))
def auth():return {"id":"authority:source","role":"SOURCE","immutable_ref":"fixture:source","revision":"1","decision_state":"OWNER_TBD"}
def frame():
    f={"schema":"c2-study-frame-0.1","id":"frame:test","version":"1","question":"Finite synthetic research"}
    f.update({k:[] for k in metadata.COLLECTIONS});f["authorities"]=[auth()]
    return f
def ts():
    f=frame();f["domains"]=[{"id":"domain:t","kind":"time","members":[0,1,2],"ordered":True},{"id":"domain:s","kind":"scenario","members":["a","b"],"ordered":False}]
    f["chronologies"]=[{"id":"chronology:t","domain":"domain:t","mode":"NONCYCLIC","authority_refs":["authority:source"],"intervals":[{"label":i,"start_h":i,"end_h":i+1,"duration_h":1} for i in range(3)]}]
    f["information_sets"]=[{"id":"info:"+str(i),"time_domain":"domain:t","stage":i,"scenario_domain":"domain:s","partition":[["a","b"]] if i==0 else [["a"],["b"]]} for i in range(3)]
    return f
class ClosureControls(unittest.TestCase):
    def test_CL01_native_shift_window(self):
        for expr,policy,expected in [("shift(a, along=t, offset=1, edge=0)",timepolicy(),["0","2","3"]),("shift(a, along=t, offset=1, edge='wrap')",timepolicy("WRAP"),["5","2","3"]),("sum_back(a, along=t, window=2)",timepolicy(),["2","5","8"])]:
            d,c=arithmetic(expr);c=fixture(d,temporal=policy)
            p=pkg(d,c);r=finite_consumer(p,dataset({"a":series([2,3,5]),"b":series([1,1,1])}))
            self.assertEqual(r.outputs()["v"],expected)
    def test_CL02_native_defined_count(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"}},"parameters":{"g":{"dims":["t"],"dtype":"bool"}},"conditions":{"available":"g","enough":"count(available, over=t) >= 3"}}
        c=fixture(d,pred_axes={"available":["t"],"enough":[]})
        r=finite_consumer(pkg(d,c),dataset({"g":series([False,True,False])}))
        self.assertEqual(r.conditions(),{"available":True,"enough":True})
        with self.assertRaisesRegex(Reject,"UNKNOWN_BOOL"):finite_consumer(pkg(d,c),dataset({"g":series([False,None,False])}))
    def test_CL03_native_joined_condition(self):
        d,c,data=relation_fixture();d["conditions"]={"positive":"a > 0","at_branch":"at(positive, by=endpoint[bus])"}
        c=fixture(d,domains={"bus":["b1","b2"],"branch":["l1","l2","l3"]},pred_axes={"positive":["bus"],"at_branch":["branch"]})
        r=finite_consumer(pkg(d,c),data);self.assertEqual(r.conditions(),{"positive":True,"at_branch":True})
        data["parameters"]["a"][0]["value"]=-1
        self.assertFalse(finite_consumer(pkg(d,c),data).conditions()["at_branch"])
    def test_CL04_metadata_ports_and_carrier(self):
        f=frame();f["components"]=[{"id":"component:a","kind":"storage","authority_refs":["authority:source"]},{"id":"component:b","kind":"network","authority_refs":["authority:source"]}]
        f["ports"]=[{"id":"port:"+n,"component_ref":"component:"+n,"direction":di,"quantity":q("MW","electricity"),"axes":[],"authority_refs":["authority:source"]} for n,di in (("a","OUT"),("b","IN"))]
        f["relations"]=[{"id":"relation:connection","kind":"connected_to","from":"port:a","to":"port:b","authority_refs":["authority:source"]}]
        f["observables"]=[{"id":"observable:p","subject":"port:a","quantity":q("MW","electricity"),"axes":[],"projection":"IDENTITY","authority_refs":["authority:source"]}]
        metadata.validate(f)
        bad=copy.deepcopy(f);bad["ports"][1]["quantity"]=q("MW_heat","heat")
        with self.assertRaisesRegex(Reject,"RELATION_TYPE"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["ports"][1]["direction"]="OUT"
        with self.assertRaisesRegex(Reject,"PORT_COMPATIBILITY"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["observables"][0]["quantity"]=q("MWh","electricity")
        with self.assertRaisesRegex(Reject,"OBSERVABLE_TYPE"):metadata.validate(bad)
    def test_CL05_chronology_information(self):
        f=ts();metadata.validate(f)
        bad=copy.deepcopy(f);bad["information_sets"][2]["partition"]=[["a","b"]]
        with self.assertRaisesRegex(Reject,"INFORMATION_REFINEMENT"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["chronologies"][0]["intervals"][1]["duration_h"]=0
        with self.assertRaisesRegex(Reject,"DURATION_OR_CHRONOLOGY"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["information_sets"].pop()
        with self.assertRaisesRegex(Reject,"INFORMATION_STAGE_COVERAGE"):metadata.validate(bad)
def assertion(package,id,name,axes,kinds,role="SAFETY_GUARANTEE",guard=None,at=None,assumptions=None):
    from interface import predicate_client
    pr=predicate_client(package,"pred:"+name,"DATA_ASSUMPTION" if role=="DATA_ASSUMPTION" else "PREDICATE")
    return {"id":id,"role":role,"modality":"MUST","predicate":{"predicate_id":pr["predicate_id"],"role":pr["role"],"axes":pr["qualified_axes"],"scope_id":pr["scope_id"]},"scope":"scope:main","binders":[{"axis":a,"kind":k,"quantifier":"EXISTS" if k=="response" and role in ("SERVICE_GUARANTEE","CAPABILITY_GUARANTEE") else "FORALL"} for a,k in zip(axes,kinds,strict=True)],"at":at or {},"guard":guard or {"truth":"TRUE","reason":None},"assumptions":assumptions or [],"authority_refs":["authority:source"]}

class ObligationControls(unittest.TestCase):
    def service(self,role):
        from common_fixtures import build,p
        from interface import predicate_client
        from closure_v1.obligations import Bound
        c=build("C2SERVICE",{"r":["r1","r2"],"y":["y1","y2"]},{"a":p("r","y"),"threshold":p(),"available":p("r")},{},{"ok":"a >= threshold","enabled":"available >= 1"},{"a":[1,0,0,1],"threshold":1,"available":[1,1]},{},{},None,roles={"available":"INPUT","threshold":"INPUT"},pred_axes={"ok":["r","y"],"enabled":["r"]})
        c["context"]["predicates"]["enabled"]["role"]="GUARD"
        pck=pkg(c["doc"],c["context"]);f=frame()
        f["domains"]=[{"id":"domain:r","kind":"request","members":["r1","r2"],"ordered":False},{"id":"domain:y","kind":"response","members":["y1","y2"],"ordered":False}]
        f["scopes"]=[{"id":"scope:main","domains":["domain:r","domain:y"],"subjects":[]}]
        t=metadata.validate(f);bound=Bound(pck,t,c["data"])
        g=predicate_client(pck,"pred:enabled","GUARD")
        ref={"predicate_id":g["predicate_id"],"role":g["role"],"axes":g["qualified_axes"],"scope_id":g["scope_id"]}
        a=assertion(pck,"assertion:service","ok",["domain:r","domain:y"],["request","response"],role,{"predicate":ref})
        return c,pck,f,bound,a
    def test_CL06_service_requires_actual_witness(self):
        from closure_v1.obligations import evaluate,Bound
        c,pck,f,b,a=self.service("SERVICE_GUARANTEE")
        self.assertEqual(evaluate(b,[a],[])["status"],"BLOCKED")
        w=[{"id":"witness:"+r,"assertion":a["id"],"key":[r],"response":y,"source_ref":"authority:source","data_identity":b.data_identity} for r,y in (("r1","y1"),("r2","y2"))]
        self.assertEqual(evaluate(b,[a],w)["status"],"FINITE_OBSERVATIONS_ONLY")
        w[0]["response"]="y2"
        self.assertEqual(evaluate(b,[a],w)["status"],"FINITE_COUNTEREXAMPLE")
        w[0]["data_identity"]="wrong"
        with self.assertRaisesRegex(Reject,"WITNESS_SNAPSHOT"):evaluate(b,[a],w)
    def test_CL07_capability_order_and_nonvacuity(self):
        from closure_v1.obligations import evaluate,Bound
        c,pck,f,b,a=self.service("CAPABILITY_GUARANTEE")
        self.assertEqual(evaluate(b,[a],[])["status"],"FINITE_OBSERVATIONS_ONLY")
        a["binders"].reverse()
        with self.assertRaisesRegex(Reject,"REQUEST_RESPONSE_ORDER"):evaluate(b,[a],[])
        a["binders"].reverse()
        for row in c["data"]["parameters"]["available"]:row["value"]=0
        b=Bound(pck,metadata.validate(f),c["data"])
        self.assertEqual(evaluate(b,[a],[])["status"],"BLOCKED")
    def test_CL08_scoped_assumptions_unknown(self):
        from closure_v1.obligations import Bound,evaluate
        d,c=arithmetic();d["assumptions"]={"valid":"a >= b"}
        c=fixture(d,roles={"a":"INPUT","b":"INPUT"})
        pck=pkg(d,c);f=ts();f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":[]}]
        b=Bound(pck,metadata.validate(f),dataset({"a":series([1,0,3]),"b":series([1,1,1])}))
        a=assertion(pck,"assertion:assume","valid",["domain:t"],["time"],"DATA_ASSUMPTION")
        g=assertion(pck,"assertion:guarantee","match",["domain:t"],["time"],assumptions=[a["id"]])
        r=evaluate(b,[a,g],[]);self.assertEqual(r["status"],"FINITE_OBSERVATIONS_ONLY")
        a["guard"]={"truth":"UNKNOWN","reason":"AUTHORITY_UNRESOLVED"}
        self.assertEqual(evaluate(b,[a,g],[])["status"],"BLOCKED")
        g["assumptions"]=[]
        with self.assertRaisesRegex(Reject,"UNBOUND_ASSUMPTION"):evaluate(b,[a,g],[])
    def test_CL09_full_information_policy(self):
        from closure_v1.obligations import Bound,nonanticipativity
        d={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True},"s":{"dtype":"str"}},"parameters":{"decision":{"dims":["s","t"]}}}
        c=fixture(d,domains={"t":[0,1,2],"s":["a","b"]});pck=pkg(d,c)
        rows=[{"key":[s,t],"value":v} for s,vs in (("a",[10,20,30]),("b",[10,40,50])) for t,v in enumerate(vs)]
        data=dataset({"decision":rows});f=ts()
        p=[{"id":"policy:decision","symbol":"ref:decision","time_domain":"domain:t","scenario_domain":"domain:s","authority_refs":["authority:source"]}]
        b=Bound(pck,metadata.validate(f),data);self.assertEqual(nonanticipativity(b,p)[0]["status"],"FINITE_OBSERVED_TRUE")
        rows[3]["value"]=11
        b=Bound(pck,metadata.validate(f),data);self.assertEqual(nonanticipativity(b,p)[0]["status"],"FINITE_COUNTEREXAMPLE")
    def test_CL10_explicit_state_boundary_scope(self):
        from closure_v1.obligations import Bound,boundaries,evaluate
        d={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True}},"parameters":{"state":{"dims":["t"]},"start":{"dims":[]},"end":{"dims":[]}},"conditions":{"initial":"state == start","terminal":"state == end"}}
        c=fixture(d,quant={n:q("MWh","electricity") for n in ("state","start","end")},pred_axes={"initial":["t"],"terminal":["t"]})
        pck=pkg(d,c);f=ts();f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":[]}]
        data=dataset({"state":series([1,2,3]),"start":[{"key":[],"value":1}],"end":[{"key":[],"value":3}]})
        b=Bound(pck,metadata.validate(f),data)
        aa=[assertion(pck,"assertion:"+n,n,["domain:t"],["time"],at={"domain:t":[v]}) for n,v in (("initial",0),("terminal",2))]
        st=[{"id":"state:ledger","symbol":"ref:state","time_domain":"domain:t","mode":"NONCYCLIC","initial":"assertion:initial","terminal":"assertion:terminal","authority_refs":["authority:source"]}]
        self.assertEqual(boundaries(b,aa,st)[0]["status"],"BOUND_NATIVE_ASSERTIONS")
        self.assertEqual(evaluate(b,aa,[])["status"],"FINITE_OBSERVATIONS_ONLY")
        aa[1]["at"]["domain:t"]=[1]
        with self.assertRaisesRegex(Reject,"BOUNDARY_SCOPE_OR_SYMBOL"):boundaries(b,aa,st)

if __name__=="__main__":unittest.main(verbosity=2)
