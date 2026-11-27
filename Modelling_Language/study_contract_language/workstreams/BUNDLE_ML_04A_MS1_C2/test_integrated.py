import sys,json,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/"WS_A"),str(ROOT/"WS_B")]
from canonical import export,reimport,semantic_contract,evaluate,INPUT_VERSION
from interface import predicate_client
from closure import Reject,canon
from test_methods import setup,study
from common_fixtures import cases,extra_cases

def integrated(c,pairs=False):
    p,m,source,x=setup(c,pairs)
    kinds=m["axis_roles"]
    assertions=[]
    for n,z in c["context"]["predicates"].items():
        q=predicate_client(p,z["id"],z["role"])
        assertions.append({"id":"assertion:"+n,"role":"DATA_ASSUMPTION" if z["role"]=="DATA_ASSUMPTION" else "SAFETY_GUARANTEE",
            "modality":"MUST","predicate":{"predicate_id":q["predicate_id"],"role":q["role"],"axes":q["qualified_axes"],"scope_id":q["scope_id"]},
            "binders":[{"axis":k,"kind":kinds[k],"quantifier":"FORALL"} for k in q["qualified_axes"]],"guard":"TRUE","authority":"OWNER_TBD"})
    contract={"schema":"c2-external-contract-0.2","id":"contract:"+c["id"],"domain_kinds":kinds.copy(),"assertions":assertions}
    return {"schema":INPUT_VERSION,"package":p,"contract":contract,"contract_ref":semantic_contract(p,contract),
            "profile":m,"study":study(c,p,m,x),"source":source,"data":c["data"],"case_context":x,
            "verification":[{"id":"verification:"+a["id"],"assertion_id":a["id"],"kind":"FINITE_OBSERVATION","authority":"OWNER_TBD"} for a in assertions]}
class Integrated(unittest.TestCase):
    def rc09(self):return next(c for c in cases() if c["id"]=="RC09")
    def test_C2_C01_roundtrip(self):
        c=self.rc09();x=integrated(c,True);t=export(x);q=reimport(t);r=q["receipt"]
        self.assertEqual(export(q["input"]),t)
        self.assertEqual(r["method"]["outputs"],c["expected"])
        self.assertEqual(r["contract"]["finite_status"],"FINITE_OBSERVATIONS_ONLY")
        self.assertEqual(r["conformance"],"NOT_PROVED")
        q=copy.deepcopy(q)  # retain unmodified actual receipt for the evidence log
        q["receipt"]["conformance"]="PROVED"
        with self.assertRaisesRegex(Reject,"TAMPER"):reimport(canon(q))
        print("C2_INTEGRATED_RC09="+json.dumps(r,sort_keys=True))
    def test_C2_C02_cross_layer(self):
        x=integrated(self.rc09(),True)
        x["contract"]["domain_kinds"]["domain:s"]="sample"
        x["contract_ref"]=semantic_contract(x["package"],x["contract"])
        with self.assertRaisesRegex(Reject,"CROSS_DOMAIN_ROLE"):evaluate(x)
        x=integrated(self.rc09(),True);x["contract_ref"]="invalid"
        with self.assertRaisesRegex(Reject,"STUDY_CONTRACT_REFERENCE"):evaluate(x)
    def test_C2_C03_no_bypass(self):
        x=integrated(self.rc09(),True);x["verification"]=[]
        with self.assertRaisesRegex(Reject,"VERIFICATION_COVERAGE"):evaluate(x)
        x=integrated(self.rc09(),True);x["extension"]={"raw_ast":{}}
        with self.assertRaisesRegex(Reject,"INTEGRATED_FIELDS"):evaluate(x)
        x=integrated(self.rc09(),True);x["verification"][0]["authority"]="APPROVED"
        with self.assertRaisesRegex(Reject,"VERIFICATION_AUTHORITY"):evaluate(x)
    def test_C2_C04_power_shared_clients(self):
        c=next(x for x in extra_cases() if x["id"]=="EXPOW")
        c["context"]["symbols"]["base"]["domain_rule"]="POSITIVE"
        c["context"]["power_domains"]={"n":{"min":-2,"max":2}}
        c["doc"]["conditions"]={"ok":"v >= base"}
        c["context"]["predicates"]["ok"]={"id":"pred:ok","role":"PREDICATE","axes":["t"]}
        x=integrated(c);r=evaluate(x)
        self.assertEqual(r["method"]["outputs"],c["expected"])
        self.assertEqual(r["contract"]["assertion_receipts"][0]["truth"],"TRUE")
        self.assertEqual(reimport(export(x))["receipt"],r)
if __name__=="__main__":unittest.main(verbosity=2)
