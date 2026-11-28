"""Actual bounded A/B source-to-native integration controls, not original paths."""
import json,sys,unittest
from pathlib import Path
from hashlib import sha256
from authoring import decode,emit_control,evaluate,AuthoringError
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"BUNDLE_ML_04A_MS1_C2"/"closure_v1"))
from test_closure_v1 import ledger_graph,to_definition,to_instance
from closure import digest

class Authoring(unittest.TestCase):
    def test_exact_structural_types_and_independent_source_forms(self):
        a=b'study_contract "c3-authoring-0.1" { definition { "ref:x": [1,"1",null,true,false]; } instance { } }'
        b=b'{"schema":"c3-authoring-0.1","definition":{"ref:x":[1,"1",null,true,false]},"instance":{}}'
        self.assertEqual(decode(a,"A"),decode(b,"B"))
        for raw,kind in [(a+b" extra","A"),(a.replace(b"1,\"1\"",b"1.0,\"1\""),"A"),
                         (b.replace(b'"instance":{}',b'"instance":{},"instance":{}'),"B"),
                         (b.replace(b'[1,',b'[1.0,'),"B")]:
            with self.assertRaises(AuthoringError):decode(raw,kind)
        with self.assertRaises(AuthoringError):decode(a.replace(b'"ref:x":',b'"ref:x":1; "ref:x":'),"A")

    def test_native_roundtrip_and_pins(self):
        x,_=ledger_graph();d,dp=to_definition(x);i=to_instance(x,d,dp);ip=digest(i)
        rows=[]
        for kind in ("A","B"):
            raw=emit_control(d,i,kind);sp=sha256(raw).hexdigest()
            result=evaluate(raw,kind,sp,dp,ip)
            self.assertEqual(result["status"],"RETURNED",result)
            self.assertEqual(result["result"]["graph"]["outputs"]["output:total"][0]["value"],"12")
            self.assertEqual(evaluate(raw,kind,sp,dp,ip),result)
            self.assertEqual(evaluate(raw,kind,"0"*64,dp,ip)["status"],"REJECTED_SOURCE")
            self.assertEqual(evaluate(raw,kind,sp,"0"*64,ip)["status"],"REJECTED_SOURCE")
            self.assertEqual(evaluate(raw,kind,sp,dp,"0"*64)["status"],"REJECTED_SOURCE")
            rows.append({k:v for k,v in result.items() if k!="result"})
        for key in ("semantic_identity","graph_semantic_identity","graph_audit_identity","package_sha256"):
            self.assertEqual(rows[0][key],rows[1][key],key)
        for key in ("source_sha256","representation_audit_identity"):
            self.assertNotEqual(rows[0][key],rows[1][key],key)
        print("C3_AUTHORING_CONTROL="+json.dumps({"scope":"SYNTHETIC_CONTROL_NOT_ORIGINAL","rows":rows},sort_keys=True))

if __name__=="__main__":unittest.main(verbosity=2)
