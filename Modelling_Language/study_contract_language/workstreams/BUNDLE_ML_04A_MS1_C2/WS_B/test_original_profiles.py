import copy,json,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from original_profiles import prepare,run
from closure import Reject,digest
from WS_B import affine_boundary as affine
from test_methods import setup,evaluate
from common_fixtures import build,p
class OriginalProfiles(unittest.TestCase):
    def test_C2_B09_original_profiles_native(self):
        receipts=[]
        for family,label,expected in (("R1","begin","415/11"),("R1","end","4150/121"),("MS1","gross","5"),("MS1","eligible","3")):
            x=prepare(family,label);r=run(x)
            self.assertEqual(r["external_outputs"]["output:summary"],[expected])
            self.assertEqual(x["reference_summary"],expected)
            if x["legacy"]:
                self.assertEqual(r["ledger"]["lineage"],x["legacy"]["ledger"])
            receipts.append({"family":family,"label":label,"receipt":r,"migration":x["audit"]})
        for i,j in ((0,1),(2,3)):
            self.assertNotEqual(receipts[i]["receipt"]["profile_identity"],receipts[j]["receipt"]["profile_identity"])
            self.assertEqual(receipts[i]["receipt"]["context"]["data_identity"],receipts[j]["receipt"]["context"]["data_identity"])
            self.assertEqual(set(receipts[i]["receipt"]["external_outputs"]),set(receipts[j]["receipt"]["external_outputs"]))
        print("C2_ORIGINAL_PROFILE_SWAPS="+json.dumps(receipts,sort_keys=True))
    def test_C2_B10_n7_original_negative(self):
        x=prepare("R1","begin");bad=copy.deepcopy(x);bad["context"]["contributions"].append(bad["context"]["contributions"][0])
        with self.assertRaisesRegex(Reject,"DUPLICATE_CONTRIBUTION"):run(bad)
        bad=copy.deepcopy(x);bad["context"]["contributions"].pop()
        with self.assertRaisesRegex(Reject,"MISSING_CONTRIBUTION"):run(bad)
        bad=copy.deepcopy(x);bad["context"]["contributions"][0]["event"]="different"
        with self.assertRaisesRegex(Reject,"CONTRIBUTION_COMPLETENESS"):run(bad)
    def test_C2_B11_disjoint_vs_reuse(self):
        c=build("LEDGER",{"t":["t0"]},{"a":p("t")},{"v":"a + a"},{},{"a":[2]},{},{"v":["4"]},None)
        pkg,m,source,x=setup(c)
        m["ledger"]={"policy":{"schema":"ledger-policy-r1","id":"policy:test","version":"1","rules":{"v":"DISJOINT"},"expected":{}},"bindings":{"a":{"role":"contribution","observable":"ref:a","case":"case:a","data_ref":""}},"key_axes":{"a":["domain:t"]}}
        x["contributions"]=[{"id":"contribution:a","series":"a","key":["t0"],"case":"case:a","observable":"ref:a","event":"event:a"}]
        with self.assertRaisesRegex(Reject,"SEMANTIC_DOUBLE_COUNT"):evaluate(c,pkg,m,source,x)
        m["ledger"]["policy"]["rules"]["v"]="ALLOW_REUSE";r=evaluate(c,pkg,m,source,x)
        self.assertEqual(list(r["ledger"]["lineage"]["v"].values()),[2])
    def test_C2_B12_positive_and_exponent_range(self):
        x=prepare("R1","end")
        c=copy.deepcopy(x["native_context"]);c["symbols"]["rate"]["domain_rule"]="ANY_EXACT"
        with self.assertRaisesRegex(Reject,"POWER_POSITIVE_BASE_REQUIRED"):affine.admit(json.dumps(x["doc"]),c)
        c=copy.deepcopy(x["native_context"]);c["power_domains"]["elapsed"]["max"]=100
        with self.assertRaisesRegex(Reject,"POWER_EXPRESSION_RANGE"):affine.admit(json.dumps(x["doc"]),c)
if __name__=="__main__":unittest.main(verbosity=2)
