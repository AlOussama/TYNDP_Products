import unittest, json, copy, sys, os, subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"native_adapter"))
from foundation import *
def q(u="1",carrier="none",basis="NONE"):
    return dict(unit=u,carrier=carrier,basis=basis,sign="NONE",direction="NONE",time_basis="NONE")
def sym(n,role="OBSERVABLE",unit=None,axes=None,dtype="float",nonzero=False):
    return dict(id="ref:"+n,role=role,axes=axes or [],dtype=dtype,quantity=unit or q(),nonzero=nonzero)
def base():
    s={n:sym(n,unit=q("MW","electricity"),axes=["t"]) for n in ("a","b")}
    s["x"]=sym("x","DERIVED_EXPRESSION",q("MW","electricity"),["t"])
    s["g"]=sym("g","INPUT",q(),["t"],"bool")
    return dict(version=VERSION,native=dict(version=0,dimensions={"t":{"dtype":"int","ordered":True}},parameters={n:{"dims":z["axes"],"dtype":z["dtype"],"missing":"refused"} for n,z in s.items() if n!="x"},expressions={"x":"a + b"}),domains={"t":{"id":"domain:t","ordered":True,"labels":[0,1],"dtype":"int"}},symbols=s,predicates={"pred:p":{"lhs":"a","rhs":"b","cmp":"ge","guard":True}},scope={"id":"scope:s","binders":["t"]},method="method:synthetic@0.1",audit={"source_id":"source:synthetic","source_ref":"fixture:0.1","evidence_id":"evidence:request"})
def go(d):return validate(json.dumps(d))
class Foundation(unittest.TestCase):
    def bad(self,edit,code):
        d=base();edit(d)
        with self.assertRaisesRegex(Reject,code):go(d)
    def test_A_N01(self):self.bad(lambda d:d["symbols"]["b"].update(quantity=q("kg/h","hydrogen")),"PHYSICAL_TYPE")
    def test_A_N02(self):self.bad(lambda d:d["symbols"]["b"].update(quantity=q("MW_heat","heat")),"PHYSICAL_TYPE")
    def test_A_N03(self):self.bad(lambda d:d["symbols"]["b"].update(quantity=q("MW_H2_LHV","hydrogen")),"HEATING_VALUE_BASIS")
    def test_A_N04(self):
        def edit(d):
            for n,b in [("a","EUR:real:2025"),("b","EUR:nominal:2025"),("x","EUR:real:2025")]:d["symbols"][n]["quantity"]=q("EUR","currency",b)
        self.bad(edit,"PHYSICAL_TYPE")
    def test_A_N05(self):self.bad(lambda d:d["native"]["expressions"].update(x="a + missing"),"NATIVE_REJECT")
    def test_A_N06(self):self.bad(lambda d:d["symbols"]["b"].update(id="ref:a"),"AMBIGUOUS_ALIAS")
    def test_A_N07(self):self.bad(lambda d:d["native"].update(variables={"a":{}}),"NATIVE_SECTION")
    def test_A_N08(self):self.bad(lambda d:d["symbols"]["x"].update(axes=[]),"INDEX_TYPE")
    def test_A_N09(self):
        def edit(d):d["predicates"]["pred:p"].update(guard=False);d["symbols"]["b"].update(quantity=q("kg","hydrogen"))
        self.bad(edit,"PHYSICAL_TYPE")
    def test_A_N10(self):
        def edit(d):
            d["symbols"]["y"]=sym("y","DERIVED_EXPRESSION",q("kg","hydrogen"),["t"])
            d["native"]["expressions"]["y"]="a"
        self.bad(edit,"EXPRESSION_TYPE")
    def test_A_N11(self):self.bad(lambda d:d["native"]["expressions"].update(x="invented(a)"),"NATIVE_REJECT")
    def test_A_N12(self):
        self.bad(lambda d:d["native"]["expressions"].update(x={"op":"invented"}),"CONSTRUCT_NOT_ALLOWED")
        l=go(base());l["extra"]={"op":"invented"}
        with self.assertRaisesRegex(Reject,"LEAF_TAMPER"):reimport(l)
    def test_A_N13(self):self.bad(lambda d:d["native"]["expressions"].update(x="9007199254740993 * a"),"NUMERIC_PRECISION")
    def test_A_N14(self):self.bad(lambda d:d["native"]["expressions"].update(x="a / 0"),"DIVISOR_NONZERO|NATIVE_REJECT")
    def test_A_N15(self):
        l=go(base())
        data={n:[{"key":[0],"value":"1"},{"key":[1],"value":"1"}] for n in ("a","b")}
        data["g"]=[{"key":[0],"value":True},{"key":[1],"value":False}]
        self.assertEqual(bind_data(l,data)["stage"],"FINITE_DATA_DOMAIN_ONLY")
        data["a"][0]["value"]=None
        with self.assertRaisesRegex(Reject,"UNKNOWN_OR_NONEXACT"):bind_data(l,data)
    def test_A_N16(self):self.bad(lambda d:d["native"]["parameters"]["a"].pop("missing"),"PARAMETER_SIGNATURE_OR_DEFAULT")
    def test_A_N17(self):
        l=go(base());d=base();d["domains"]["t"]["labels"].reverse();other=go(d)
        self.assertNotEqual(l["semantic_identity"],other["semantic_identity"])
        l["scope"]["binders"]=[]
        with self.assertRaisesRegex(Reject,"LEAF_TAMPER"):reimport(l)
    def test_A_N18(self):self.bad(lambda d:d["native"].update(relations={"r":{}}),"NATIVE_SECTION")
    def test_A_N19(self):self.bad(lambda d:d.update(version="unknown"),"LANGUAGE_VERSION")
    def test_A_N20(self):
        l=go(base());l.pop("audit")
        with self.assertRaisesRegex(Reject,"LEAF_TAMPER"):reimport(l)
    def test_roundtrip(self):
        a=go(base());self.assertEqual(reimport(a),a);self.assertEqual(m3(a)["mathematical_leaf"],a)
        b=base();b["native"]["expressions"]["x"]="b + a";self.assertEqual(go(b)["semantic_identity"],a["semantic_identity"])
        b=base();b["audit"]["source_ref"]="other";z=go(b);self.assertEqual(z["semantic_identity"],a["semantic_identity"]);self.assertNotEqual(z["audit_identity"],a["audit_identity"])
        b=base();b["native"]["expressions"]["x"]="a - b";c=base();c["native"]["expressions"]["x"]="b - a";self.assertNotEqual(go(b)["native_identity"],go(c)["native_identity"])
    def test_static_sum_and_rational(self):
        d=base();d["symbols"]["x"]["axes"]=[];d["native"]["expressions"]["x"]="sum(a / 3, over=t)";self.assertTrue(go(d)["semantic_identity"])
    def test_m2_mapping(self):
        l=go(base());x=m2_measure_predicate(l,"pred:p",{"t":"t"});self.assertEqual(x,{"op":"compare","cmp":"ge","lhs":{"op":"measure","ref":"ref:a","indices":[{"op":"var","name":"t"}]},"rhs":{"op":"measure","ref":"ref:b","indices":[{"op":"var","name":"t"}]}})
    def test_processes(self):
        p=str(Path(__file__).resolve().parent);cmd=[sys.executable,"-c","import sys;sys.path.insert(0,"+repr(p)+");from test_foundation import *;print(go(base())['semantic_identity'])"]
        a=subprocess.check_output(cmd,env=dict(os.environ,PYTHONHASHSEED="1"));b=subprocess.check_output(cmd,env=dict(os.environ,PYTHONHASHSEED="77"));self.assertEqual(a,b)
if __name__=="__main__":unittest.main(verbosity=2)
