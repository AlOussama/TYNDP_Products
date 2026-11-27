import unittest,sys
from pathlib import Path
from interface import resolve_predicate,resolve_method
from closure import Reject
from package_interface import export_package
from test_closure import arithmetic,open_,dataset,series
class Interface(unittest.TestCase):
    def setUp(self):
        d,c=arithmetic();self.package=export_package(open_(d,c))
        from package_interface import predicate_client
        p=predicate_client(self.package,"pred:match","PREDICATE")
        self.ref={"predicate_id":"pred:match","role":"PREDICATE","axes":p["qualified_axes"],"scope_id":p["scope_id"]}
    def test_C2_I01_reference(self):
        self.assertEqual(resolve_predicate(self.package,self.ref)["verdict"],"NOT_EXECUTED")
    def test_C2_I02_axis_scope_role(self):
        for k,v,code in [("axes",[],"C2_AXIS_ALIGNMENT"),("scope_id","scope:other","C2_SCOPE_ALIGNMENT"),("role","GUARD","PREDICATE_ROLE")]:
            with self.assertRaisesRegex(Reject,code):resolve_predicate(self.package,{**self.ref,k:v})
    def test_C2_I03_method_separate(self):
        r=resolve_method(self.package,dataset({"a":series([1,2,3]),"b":series([1,2,3])}))
        self.assertEqual(r["method_result"],"NOT_EXECUTED")
        self.assertEqual(r["owner"],"OWNER_TBD")
if __name__=="__main__":unittest.main(verbosity=2)
