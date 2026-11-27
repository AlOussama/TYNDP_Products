import copy,json,sys,unittest
from contract import evaluate,not3,fold3,TRUTH
from common_fixtures import cases,build,p
from closure import admit,Reject
from package_interface import export_package,predicate_client
def package(c):return export_package(admit(json.dumps(c["doc"]),c["context"]))
def assertion(pkg,name,role="SAFETY_GUARANTEE",guard="TRUE",kinds=None,qs=None):
    r=predicate_client(pkg,"pred:"+name,"PREDICATE");axes=r["qualified_axes"]
    return {"id":"assertion:"+name,"role":role,"modality":"MUST","predicate":{"predicate_id":r["predicate_id"],"role":r["role"],"axes":axes,"scope_id":r["scope_id"]},"binders":[{"axis":a,"kind":(kinds or ["sample"]*len(axes))[i],"quantifier":(qs or ["FORALL"]*len(axes))[i]} for i,a in enumerate(axes)],"guard":guard,"authority":"OWNER_TBD"}
class Contract(unittest.TestCase):
    def test_C2_A01_bool3(self):
        for i,x in enumerate(TRUTH):
            self.assertEqual(not3(not3(x)),x)
            for j,y in enumerate(TRUTH):
                self.assertEqual(fold3("FORALL",[x,y]),TRUTH[min(i,j)])
                self.assertEqual(fold3("EXISTS",[x,y]),TRUTH[max(i,j)])
        with self.assertRaisesRegex(Reject,"NONEMPTY"):fold3("FORALL",[])
    def test_C2_A02_ordered_quantification(self):
        c=build("C2Q",{"r":["r1","r2"],"y":["y1","y2"]},{"a":p("r","y"),"b":p()},{},{"ok":"a >= b"},{"a":[1,0,0,1],"b":1},{},{},None)
        pkg=package(c);a=assertion(pkg,"ok","CAPABILITY_GUARANTEE",kinds=["request","response"],qs=["FORALL","EXISTS"])
        self.assertEqual(evaluate(pkg,c["data"],a)["truth"],"TRUE")
        a["binders"].reverse()
        with self.assertRaisesRegex(Reject,"REQUEST_RESPONSE_ORDER"):evaluate(pkg,c["data"],a)
        a["role"]="SAFETY_GUARANTEE"
        self.assertEqual(evaluate(pkg,c["data"],a)["truth"],"FALSE") # exists y forall r
    def test_C2_A03_guard_and_static_validation(self):
        c=cases()[0];pkg=package(c);a=assertion(pkg,"exchange_ok",guard="UNKNOWN")
        self.assertEqual(evaluate(pkg,c["data"],a)["finite_status"],"BLOCKED")
        a["guard"]="FALSE";self.assertEqual(evaluate(pkg,c["data"],a)["finite_status"],"NOT_APPLICABLE")
        bad=copy.deepcopy(c["data"]);bad["parameters"]["e"].pop()
        with self.assertRaisesRegex(Reject,"INCOMPLETE_PARAMETER_SUPPORT"):evaluate(pkg,bad,a)
        a["guard"]="TRUE";self.assertEqual(evaluate(pkg,None,a)["reason"],"MISSING_DATA")
    def test_C2_A04_original_fragments(self):
        for c in cases():
            if c["id"] not in ("RC01","RC02","RC03","RC04","RC05","RC06","RC07","RC10"):continue
            pkg=package(c)
            for n in c["doc"]["conditions"]:
                a=assertion(pkg,n);r=evaluate(pkg,c["data"],a);self.assertEqual(r["truth"],"TRUE",c["id"]+n);self.assertEqual(r["conformance"],"NOT_PROVED")
            neg=c["negative"]
            if "condition" in neg:
                data=copy.deepcopy(c["data"])
                for row,v in zip(data["parameters"][neg["param"]],neg["values"],strict=True):row["value"]=v
                r=evaluate(pkg,data,assertion(pkg,neg["condition"]));self.assertEqual(r["truth"],"FALSE",c["id"])
    def test_C2_A05_unbound_axis_and_authority(self):
        c=cases()[0];pkg=package(c);a=assertion(pkg,"exchange_ok");a["binders"]=[]
        with self.assertRaisesRegex(Reject,"UNBOUND"):evaluate(pkg,c["data"],a)
        a=assertion(pkg,"exchange_ok");a["authority"]="APPROVED"
        with self.assertRaisesRegex(Reject,"AUTHORITY"):evaluate(pkg,c["data"],a)
if __name__=="__main__":unittest.main(verbosity=2)
