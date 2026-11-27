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
if __name__=="__main__":unittest.main(verbosity=2)
