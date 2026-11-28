"""C4 controls; never counted as frozen original paths."""
import sys,copy,unittest
from pathlib import Path
C3=Path(__file__).resolve().parents[1]/"BUNDLE_ML_04A_MS1_C3"
sys.path.insert(0,str(C3))
from run_originals import candidate_source
from original_record_binding import source_binding
from closure import Reject
from original_compiler import compile_rc
from authoring import emit_control,decode
from research_assembly import q,fixture,pkg,dataset,scalar
from interface import finite_consumer

class C4Controls(unittest.TestCase):
    def setUp(self):
        self.x,_,self.raw,_,_=candidate_source("RC02","B")
    def test_candidate_has_no_test_module_dependency(self):
        self.assertFalse({"test_closure","test_closure_v1"} & set(sys.modules))
    def test_original_source_binding(self):
        source_binding(self.x["definition"],self.x["instance"],self.raw)
    def test_reference_rename_rejected(self):
        x=copy.deepcopy(self.x)
        x["definition"]["reference"]="RENAMED"
        x["instance"]["record"]["id"]="RENAMED"
        with self.assertRaisesRegex(Reject,"ORIGINAL_REFERENCE_BINDING"):
            source_binding(x["definition"],x["instance"],self.raw)
    def test_source_bytes_rejected(self):
        with self.assertRaisesRegex(Reject,"ORIGINAL_SOURCE_BLOB"):
            source_binding(self.x["definition"],self.x["instance"],self.raw+b" ")
    def test_coordinate_tamper_rejected(self):
        x=copy.deepcopy(self.x)
        x["instance"]["raw_transfers"]["delivered"][0]="999"
        with self.assertRaisesRegex(Reject,"SOURCE_DATA_BINDING:delivered"):
            source_binding(x["definition"],x["instance"],self.raw)

    def test_external_obligation_change_is_observed(self):
        x,_,raw,_,_=candidate_source("RC01","B")
        old=compile_rc(x,raw)
        self.assertEqual(old["conformance"],"NOT_PROVED")
        d=x["definition"]
        d["conditions"]["c4_extra_balance"]={"formula":"intake == intake_obs","axes":["t"],"role":"SAFETY_GUARANTEE"}
        added=compile_rc(x,raw)
        a=next(z for z in added["obligations"]["assertions"] if z["id"]=="assertion:c4_extra_balance")
        self.assertEqual(a["truth"],"TRUE")
        d["conditions"]["c4_extra_balance"]["formula"]="intake > intake_obs"
        changed=compile_rc(x,raw)
        a=next(z for z in changed["obligations"]["assertions"] if z["id"]=="assertion:c4_extra_balance")
        self.assertEqual(a["truth"],"FALSE")
        self.assertEqual(changed["conformance"],"NOT_PROVED")
        self.assertNotEqual(added["semantic_identity"],changed["semantic_identity"])
        print("C4_CHANGE_OBLIGATION: one authored condition; no validator change; true/false observed")
    def test_missing_evidence_does_not_promote(self):
        x,_,raw,_,_=candidate_source("RC01","B")
        d,i=x["definition"],x["instance"]
        z=copy.deepcopy(d["report_requests"][0]);z["id"]="report:c4_new_evidence";d["report_requests"].append(z)
        r=copy.deepcopy(i["external_reports"][0]);r["id"]=z["id"];i["external_reports"].append(r)
        result=compile_rc(x,raw)
        self.assertTrue(any(z["id"]=="report:c4_new_evidence" and z["status"]=="NOT_EXECUTED" for z in result["external_reports"]))
        self.assertEqual(result["conformance"],"NOT_PROVED")
        print("C4_CHANGE_EVIDENCE: one request and one pending receipt; no validator change")
    def test_new_method_and_domain_member(self):
        def run(formula,members,values):
            d={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{"a":{"dims":["s"]}},"expressions":{"kpi":formula}}
            c=fixture(d,domains={"s":members},quant={"a":q(),"kpi":q()},roles={"a":"INPUT"})
            return finite_consumer(pkg(d,c),dataset({"a":[{"key":[s],"value":v} for s,v in zip(members,values,strict=True)]})).outputs()["kpi"]
        self.assertEqual(run("a",["a","b"],[1,2]),["1","2"])
        self.assertEqual(run("2*a",["a","b"],[1,2]),["2","4"])
        self.assertEqual(run("2*a",["a","b","c"],[1,2,3]),["2","4","6"])
        print("C4_CHANGE_METHOD_DOMAIN: new native expression, changed formula, added one domain member and one value; no grammar/validator change")
    def test_authoring_proxy_roundtrip(self):
        for id in ("RC01","RC02","RC04","RC08"):
            x,_,raw,_,_=candidate_source(id,"B")
            a=emit_control(x["definition"],x["instance"],"A")
            b=emit_control(x["definition"],x["instance"],"B")
            self.assertEqual(decode(a,"A"),decode(b,"B"))
            print("C4_AUTHORING_PROXY "+id+" A="+str(len(a))+" B="+str(len(b))+" (same-design emitted roundtrip, not independent authors)")
if __name__=="__main__":unittest.main(verbosity=2)

