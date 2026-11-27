import copy,json,unittest
from methods import validate,identities,migrate_with_audit
from common_fixtures import cases,extra_cases
from closure import admit,native,digest,text_hash,Reject
from package_interface import export_package,method_client
from legacy_comparison import map_profile
from run_comparison import original_profile_controls
def setup(case,pairs=False):
    pkg=export_package(admit(json.dumps(case["doc"]),case["context"]))
    r=method_client(pkg,case["data"]);s=r["signature"];c=case["context"]
    source="synthetic research method source: "+case["id"]
    profile={"id":s["id"],"version":s["version"],"native_signature":r["method_signature_identity"],"native_semantic_identity":identities(pkg)["semantic"],"source_ref":"fixture:"+case["id"],"source_sha256":text_hash(source),"approval":"RESEARCH_ASSUMPTION",
      "input_roles":{z["symbol_id"]:case["weight_roles"].get(z["native_name"],"value").upper() for z in s["inputs"]},
      "axis_roles":{z["id"]:case["axis_roles"].get(n,"sample") for n,z in c["domains"].items()},
      "parameter_ranges":{z["symbol_id"]:{"min":"1/100","max":"100"} for z in s["parameters"]},
      "probability_rules":{z["symbol_id"]:"SUM_ONE" for z in s["inputs"] if case["weight_roles"].get(z["native_name"])=="probability"},
      "counterfactual_pairs":[{"id":"pair:cost","reference":"ref:baseline","alternative":"ref:project"}] if pairs else [],
      "outputs":[z["symbol_id"] for z in s["outputs"]]}
    context={"pairs":[{"id":"pair:cost","reference_exogenous":{"scenario":["a","b"],"weather":"synthetic"},"alternative_exogenous":{"scenario":["a","b"],"weather":"synthetic"}}] if pairs else []}
    return pkg,profile,source,context
def study(case,pkg,profile,context):
    r=method_client(pkg,case["data"]);s=case["context"]["study"]
    return {"id":s["id"],"version":s["version"],"profile_identity":digest(profile),"native_study_identity":r["study_identity"],"data_context_identity":r["context_receipt"]["context_identity"],"case_context_identity":digest(context),"owner":"OWNER_TBD"}
def evaluate(case,pkg,profile,source,context):
    return validate(pkg,case["data"],profile,study(case,pkg,profile,context),source,context)
class Methods(unittest.TestCase):
    def rc(self,n):return next(c for c in cases() if c["id"]==n)
    def test_C2_B01_ABL09(self):
        c=self.rc("RC09");p,m,s,x=setup(c,True)
        good=evaluate(c,p,m,s,x);self.assertEqual(good["outputs"],c["expected"])
        bad=copy.deepcopy(c);bad["data"]["parameters"]["weight"][1]["value"]="3/5";bad["data"]["parameters"]["reported"][0]["value"]="1500/11"
        with self.assertRaisesRegex(Reject,"PROBABILITY_NORMALIZATION"):evaluate(bad,p,m,s,x)
        with self.assertRaisesRegex(ValueError,"PROBABILITY_NORMALIZATION"):map_profile(bad,native(json.dumps(bad["doc"])).program,bad["data"])
    def test_C2_B02_ABL11(self):
        c=self.rc("RC09");p,m,s,x=setup(c,True)
        x["pairs"][0]["alternative_exogenous"]["weather"]="other"
        with self.assertRaisesRegex(Reject,"COUNTERFACTUAL_EXOGENEITY"):evaluate(c,p,m,s,x)
    def test_C2_B03_ABL08(self):
        c=self.rc("RC10");p=export_package(admit(json.dumps(c["doc"]),c["context"]));a=identities(p)
        c["doc"]["description"]="documentation only";b=identities(export_package(admit(json.dumps(c["doc"]),c["context"])))
        self.assertEqual(a["semantic"],b["semantic"]);self.assertNotEqual(a["native"],b["native"]);self.assertNotEqual(a["audit"],b["audit"])
        c["context"]["symbols"]["a"]["role"]="INPUT"
        z=identities(export_package(admit(json.dumps(c["doc"]),c["context"])))
        self.assertNotEqual(b["semantic"],z["semantic"])
    def test_C2_B04_ABL06(self):
        c=self.rc("RC01");p=export_package(admit(json.dumps(c["doc"]),c["context"]));a=migrate_with_audit(c,p)
        c["context"]["audit"]["source_ref"]="fixture:changed"
        q=export_package(admit(json.dumps(c["doc"]),c["context"]));b=migrate_with_audit(c,q)
        self.assertNotEqual(a["migration_audit_identity"],b["migration_audit_identity"])
        self.assertEqual(a["target"]["semantic_digest"],b["target"]["semantic_digest"])
    def test_C2_B05_original_profile_controls(self):
        r=original_profile_controls()["profile_swaps"]
        self.assertEqual([x["expected"] for x in r],["415/11","4150/121"])
    def test_C2_B06_method_swap(self):
        c=self.rc("RC09");p,m,s,x=setup(c,True);a=evaluate(c,p,m,s,x)
        d=copy.deepcopy(c);d["doc"]["expressions"]["discounted"]="annual / factor / 2"
        d["context"]["method"]["version"]="0.3";d["context"]["study"]["version"]="0.3"
        d["context"]["study"]["method_ref"]=digest(d["context"]["method"])
        from fractions import Fraction as F
        d["data"]["parameters"]["reported"][0]["value"]=str(F(a["outputs"]["discounted"][0])/2)
        q,n,t,y=setup(d,True);b=evaluate(d,q,n,t,y)
        self.assertTrue(all(b["conditions"].values()))
        self.assertNotEqual(a["profile_identity"],b["profile_identity"])
        self.assertEqual(a["outputs"]["annual"],b["outputs"]["annual"])
        from fractions import Fraction as F
        self.assertEqual(F(b["outputs"]["discounted"][0]),F(a["outputs"]["discounted"][0])/2)
        self.assertEqual(m["outputs"],n["outputs"])
        with self.assertRaisesRegex(Reject,"METHOD_SIGNATURE"):evaluate(d,q,m,s,x)
        print("C2_SYNTHETIC_SWAP="+json.dumps({"a":a,"b":b},sort_keys=True))
    def test_C2_B07_unpinned_context(self):
        c=self.rc("RC09");p,m,s,x=setup(c,True);st=study(c,p,m,x);st["data_context_identity"]="invalid"
        with self.assertRaisesRegex(Reject,"STUDY_DATA_CONTEXT"):validate(p,c["data"],m,st,s,x)
if __name__=="__main__":unittest.main(verbosity=2)
