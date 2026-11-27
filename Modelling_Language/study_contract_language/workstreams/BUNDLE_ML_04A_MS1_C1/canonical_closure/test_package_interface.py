import json,unittest
from test_closure import arithmetic,open_,fixture,dataset,series,Reject
from closure import admit,canon
from package_interface import export_package,import_package,predicate_client,method_client

class Package(unittest.TestCase):
    def test_P01_canonical_package_roundtrip(self):
        d,c=arithmetic();leaf=open_(d,c)
        text=export_package(leaf);self.assertEqual(import_package(text),leaf)
        self.assertEqual(export_package(import_package(text)),text)
        obj=json.loads(text);self.assertEqual(obj["mathematics"]["canonical"],leaf["native_canonical"])
        self.assertNotIn("ast",obj["mathematics"])
        self.assertEqual(obj["evidence"]["obligations"],"NOT_EXECUTED")
    def test_P02_source_audit_separation(self):
        d,c=arithmetic();a=open_(d,c);b=admit(a["native_canonical"],c,True)
        x,y=map(lambda leaf:json.loads(export_package(leaf)),(a,b))
        self.assertEqual(x["mathematics"],y["mathematics"])
        self.assertEqual(x["binding"],y["binding"])
        self.assertNotEqual(x["audit"]["identity"],y["audit"]["identity"])
    def test_P03_external_contract_client(self):
        d,c=arithmetic();p=predicate_client(export_package(open_(d,c)),"pred:match","PREDICATE")
        self.assertEqual(p["qualified_axes"],["domain:t"])
        self.assertEqual(p["required_symbols"],["ref:a","ref:b"])
        self.assertEqual(p["verdict"],"NOT_EXECUTED")
        with self.assertRaisesRegex(Reject,"PREDICATE_ROLE"):
            predicate_client(export_package(open_(d,c)),"pred:match","GUARD")
    def test_P04_assumption_not_predicate(self):
        d,c=arithmetic();d["assumptions"]={"domain_check":"a >= b"};c=fixture(d,roles={"a":"INPUT","b":"METHOD_PARAMETER"})
        text=export_package(open_(d,c))
        with self.assertRaisesRegex(Reject,"PREDICATE_ROLE"):predicate_client(text,"pred:domain_check","PREDICATE")
        self.assertEqual(predicate_client(text,"pred:domain_check","DATA_ASSUMPTION")["verdict"],"NOT_EXECUTED")
    def test_P05_independent_method_client(self):
        d,c=arithmetic();text=export_package(open_(d,c))
        data=dataset({"a":series([1,2,3]),"b":series([1,2,3])})
        r=method_client(text,data);self.assertEqual(r["signature"]["outputs"][0]["symbol_id"],"ref:v")
        self.assertEqual(r["context_receipt"]["predicate_verdict"],"NOT_EXECUTED")
        self.assertEqual(r["method_result"],"NOT_EXECUTED")
        self.assertEqual(r["owner"],"OWNER_TBD")
    def test_P06_package_tamper(self):
        d,c=arithmetic();text=export_package(open_(d,c))
        for group,key,value in [("mathematics","canonical","other"),("binding","identity","other"),("audit","identity","other"),("evidence","obligations","PASS"),("binding","invented_ast",{})]:
            obj=json.loads(text);obj[group][key]=value
            with self.assertRaisesRegex(Reject,"PACKAGE_TAMPER"):import_package(canon(obj))
    def test_P07_different_method_context_same_native_math(self):
        d,c=arithmetic();data=dataset({"a":series([1,2,3]),"b":series([1,2,3])})
        a=export_package(open_(d,c));c["study"]["version"]="0.3";b=export_package(open_(d,c))
        self.assertEqual(json.loads(a)["mathematics"],json.loads(b)["mathematics"])
        self.assertNotEqual(method_client(a,data)["context_receipt"]["context_identity"],method_client(b,data)["context_receipt"]["context_identity"])
if __name__=="__main__":unittest.main(verbosity=2)
