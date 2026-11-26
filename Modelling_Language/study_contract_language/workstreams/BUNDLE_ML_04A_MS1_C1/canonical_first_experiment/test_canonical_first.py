import unittest,json,copy
import mathspec as ms
import mathspec.program as mp
from mathspec.errors import LanguageError
from canonical_first import admit_canonical,reimport,c1

def mathdoc(expr="a + b",dims=None):
    dims=dims or {"t":{"dtype":"int","ordered":True}}
    axis=list(dims)
    return {"version":0,"dimensions":dims,"parameters":{"a":{"dims":axis,"dtype":"float","missing":"refused"},"b":{"dims":axis,"dtype":"float","missing":"refused"}},"expressions":{"total":expr}}
def canon(d):return ms.to_spec(d).to_yaml(canonical=True)
def quantity(unit="MW",carrier="electricity",basis="NONE"):
    return {"unit":unit,"carrier":carrier,"basis":basis,"sign":"NONE","direction":"NONE","time_basis":"NONE"}
def context(d):
    names=list(d["dimensions"])
    return {"domains":{n:{"id":"domain:"+n,"labels":[0,1]} for n in names},
            "symbols":{n:{"id":"ref:"+n,"role":"DERIVED_EXPRESSION" if n=="total" else "OBSERVABLE","quantity":quantity(),"nonzero":False} for n in ("a","b","total")},
            "scope":{"id":"scope:study","binders":list(names)},
            "predicates":{"pred:balance":{"lhs":"a","rhs":"b","cmp":"eq","guard":True,"axes":list(names),"alignment":"SAME_AXES","guard_alignment":"CONSTANT"}},
            "method":"method:synthetic@0.1","audit":{"source_id":"source:research","source_ref":"fixture:canonical-first","evidence_id":"evidence:request"}}

class CanonicalFirst(unittest.TestCase):
    def test_N01_native_commutativity(self):
        a,b=mathdoc("a + b"),mathdoc("b + a")
        self.assertEqual(canon(a),canon(b))
        self.assertEqual(canon(mathdoc("a * b")),canon(mathdoc("b * a")))
    def test_N02_native_not_equivalence(self):
        self.assertNotEqual(canon(mathdoc("a + a")),canon(mathdoc("2 * a")))
        self.assertNotEqual(canon(mathdoc("a / b")),canon(mathdoc("b / a")))
        self.assertNotEqual(canon(mathdoc("a - b")),canon(mathdoc("b - a")))
    def test_N03_defaults_and_order(self):
        a=mathdoc(dims={"t":{"dtype":"str","ordered":False}})
        b=copy.deepcopy(a);b["dimensions"]["t"]={}
        for p in b["parameters"].values():p.pop("dtype");p.pop("missing")
        self.assertEqual(canon(a),canon(b))
        b["dimensions"]["t"]["ordered"]=True
        self.assertNotEqual(canon(a),canon(b))
    def test_N04_numeric_preimage_collision(self):
        a,b=mathdoc("a * 9007199254740992"),mathdoc("a * 9007199254740993")
        self.assertEqual(canon(a),canon(b))
        with self.assertRaisesRegex(c1.Reject,"NUMERIC_PRECISION"):admit_canonical(canon(a),context(a))
    def test_N05_native_conditions(self):
        a=mathdoc();a["conditions"]={"match":"a >= b"}
        a["assumptions"]={"require_match":"match"}
        s=ms.to_spec(a)
        self.assertIn("match",s.program.conditions)
        self.assertIn("require_match",s.program.assumptions)
        self.assertEqual(s.to_yaml(canonical=True),canon(s.to_yaml(canonical=True)))
        with self.assertRaisesRegex(c1.Reject,"OUTSIDE_BOUNDED_PROFILE"):admit_canonical(s.to_yaml(canonical=True),context(a))
    def test_N06_native_relation_and_temporal(self):
        a=mathdoc(dims={"t":{"dtype":"int","ordered":True},"bus":{"dtype":"str"}})
        a["relations"]={"location":{"key":"t","values":"bus"}}
        a["parameters"]={"a":{"dims":["t"]},"b":{"dims":["t"]}}
        a["expressions"]={"lag":"shift(a, along=t, offset=1, edge=0)"}
        s=ms.to_spec(a)
        self.assertIn("location",s.program.relations)
        self.assertIsInstance(s.program.expressions["lag"].expression,mp.Translate)
        self.assertEqual(s.to_yaml(canonical=True),canon(s.to_yaml(canonical=True)))
    def test_N07_native_condition_cases(self):
        a=mathdoc()
        a["expressions"]={"total":{"dims":["t"],"cases":{"early":{"when":"position(t) == 0","expression":"a"}},"otherwise":"b"}}
        s=ms.to_spec(a)
        self.assertIsInstance(s.program.expressions["total"].expression,mp.Cases)
        self.assertEqual(s.to_yaml(canonical=True),canon(s.to_yaml(canonical=True)))
    def test_B01_direct_canonical_admission(self):
        d=mathdoc();c=context(d);leaf=admit_canonical(canon(d),c)
        self.assertEqual(leaf,reimport(leaf))
        self.assertEqual(leaf["native_canonical"],canon(d))
        self.assertEqual(leaf["origin"]["kind"],"CANONICAL_AS_SOURCE")
    def test_B02_role_and_quantity_outside_math(self):
        d=mathdoc();c=context(d);a=admit_canonical(canon(d),c)
        c["symbols"]["a"]["role"]="INPUT";b=admit_canonical(canon(d),c)
        self.assertEqual(a["native_identity"],b["native_identity"])
        self.assertNotEqual(a["semantic_identity"],b["semantic_identity"])
        c["symbols"]["a"]["quantity"]=quantity("MW_heat","heat")
        with self.assertRaisesRegex(c1.Reject,"PHYSICAL_TYPE"):admit_canonical(canon(d),c)
    def test_B03_ordered_binding(self):
        d=mathdoc(dims={"t":{"dtype":"int","ordered":True},"s":{"dtype":"int","ordered":False}})
        c=context(d);a=admit_canonical(canon(d),c)
        c["domains"]["s"]["labels"].reverse();b=admit_canonical(canon(d),c)
        self.assertEqual(a["semantic_identity"],b["semantic_identity"])
        self.assertNotEqual(a["audit_identity"],b["audit_identity"])
        c["domains"]["t"]["labels"].reverse();z=admit_canonical(canon(d),c)
        self.assertNotEqual(a["semantic_identity"],z["semantic_identity"])
        c["scope"]["binders"].reverse();c["predicates"]["pred:balance"]["axes"].reverse()
        self.assertNotEqual(z["semantic_identity"],admit_canonical(canon(d),c)["semantic_identity"])
    def test_B04_alignment(self):
        d=mathdoc(dims={"t":{"dtype":"int","ordered":True},"s":{"dtype":"int"}})
        d["parameters"]["a"]["dims"]=["t"];d["parameters"]["b"]["dims"]=["s"]
        c=context(d)
        with self.assertRaisesRegex(c1.Reject,"PREDICATE_ALIGNMENT"):admit_canonical(canon(d),c)
        d["parameters"]["b"]["dims"]=[];c["predicates"]["pred:balance"].update(alignment="SCALAR_BROADCAST",axes=["t"])
        self.assertEqual(admit_canonical(canon(d),c)["predicate_support"]["pred:balance"]["axes"],["t"])
    def test_B05_original_and_audit(self):
        d=mathdoc();c=context(d);a=admit_canonical(canon(d),c,json.dumps(d))
        self.assertEqual(a["origin"]["kind"],"ORIGINAL_JSON_CHECKED")
        self.assertEqual(a,reimport(a))
        b=admit_canonical(canon(d),c)
        self.assertEqual(a["semantic_identity"],b["semantic_identity"])
        self.assertNotEqual(a["audit_identity"],b["audit_identity"])
        a["context"]["audit"]["source_ref"]="changed"
        with self.assertRaisesRegex(c1.Reject,"LEAF_TAMPER"):reimport(a)
        with self.assertRaisesRegex(c1.Reject,"ORIGINAL_CANONICAL_MISMATCH"):admit_canonical(canon(d),c,json.dumps(mathdoc("a - b")))
    def test_B06_raw_extension_and_defaults(self):
        d=mathdoc();c=context(d)
        leaf=admit_canonical(canon(d),c);leaf["invented_ast"]={}
        with self.assertRaisesRegex(c1.Reject,"LEAF_TAMPER"):reimport(leaf)
        d["parameters"]["a"]["missing"]=0
        with self.assertRaisesRegex(c1.Reject,"MISSING_OR_PROFILE_POLICY"):admit_canonical(canon(d),c)
    def test_B07_explicit_guard_signature(self):
        d=mathdoc();d["parameters"]["g"]={"dims":[],"dtype":"bool","missing":"refused"}
        c=context(d);c["symbols"]["g"]={"id":"ref:g","role":"INPUT","quantity":quantity("1","none"),"nonzero":False}
        c["predicates"]["pred:balance"]["guard"]="g"
        with self.assertRaisesRegex(c1.Reject,"GUARD_ALIGNMENT"):admit_canonical(canon(d),c)
        c["predicates"]["pred:balance"]["guard_alignment"]="SCALAR_BROADCAST"
        self.assertEqual(admit_canonical(canon(d),c)["predicate_support"]["pred:balance"]["guard_alignment"],"SCALAR_BROADCAST")
    def test_N08_canonical_origin_limit(self):
        # Native binary floating-point normalisation can erase the source
        # distinction even when the resulting canonical literal is admitted.
        a,b=mathdoc("a * 1"),mathdoc("a * 1.00000000000000001")
        self.assertEqual(canon(a),canon(b))
        c=context(a)
        leaf=admit_canonical(canon(b),c)
        self.assertEqual(leaf["origin"]["kind"],"CANONICAL_AS_SOURCE")
        with self.assertRaisesRegex(c1.Reject,"NUMERIC_"):
            admit_canonical(canon(b),c,json.dumps(b))
    def test_B08_RC03_cross_carrier_conversion(self):
        d=mathdoc()
        d["parameters"]={"flow":{"dims":["t"]},"heating_value":{"dims":[]},"reported":{"dims":["t"]}}
        d["expressions"]={"chemical_power":"flow * heating_value"}
        c=context(d)
        def symbol(n,role,q):
            return {"id":"ref:"+n,"role":role,"quantity":q,"nonzero":False}
        c["symbols"]={
            "flow":symbol("flow","OBSERVABLE",quantity("kg/h","hydrogen")),
            "heating_value":symbol("heating_value","METHOD_PARAMETER",quantity("MWh_H2_LHV/kg","conversion","LHV")),
            "reported":symbol("reported","OBSERVABLE",quantity("MW_H2_LHV","hydrogen","LHV")),
            "chemical_power":symbol("chemical_power","DERIVED_EXPRESSION",quantity("MW_H2_LHV","hydrogen","LHV"))}
        c["predicates"]["pred:balance"].update(lhs="chemical_power",rhs="reported")
        self.assertEqual(admit_canonical(canon(d),c)["predicate_support"]["pred:balance"]["axes"],["t"])
        c["symbols"]["heating_value"]["quantity"]=quantity("MWh_H2_HHV/kg","conversion","HHV")
        with self.assertRaisesRegex(c1.Reject,"EXPRESSION_TYPE"):
            admit_canonical(canon(d),c)
    def test_B09_RC08_weighted_cost(self):
        d=mathdoc()
        d["parameters"]={"opex":{"dims":["t"]},"duration":{"dims":["t"]},"capex":{"dims":[]},"reported":{"dims":[]}}
        d["expressions"]={"total_cost":"sum(opex * duration, over=t) + capex"}
        c=context(d)
        def symbol(n,role,q):
            return {"id":"ref:"+n,"role":role,"quantity":q,"nonzero":False}
        c["symbols"]={
            "opex":symbol("opex","OBSERVABLE",quantity("EUR/h","currency","EUR:real:2025")),
            "duration":symbol("duration","INPUT",quantity("h","none")),
            "capex":symbol("capex","OBSERVABLE",quantity("EUR","currency","EUR:real:2025")),
            "reported":symbol("reported","OBSERVABLE",quantity("EUR","currency","EUR:real:2025")),
            "total_cost":symbol("total_cost","DERIVED_EXPRESSION",quantity("EUR","currency","EUR:real:2025"))}
        c["predicates"]["pred:balance"].update(lhs="total_cost",rhs="reported",axes=[])
        self.assertEqual(admit_canonical(canon(d),c)["predicate_support"]["pred:balance"]["axes"],[])
        c["symbols"]["capex"]["quantity"]=quantity("EUR","currency","EUR:nominal:2025")
        with self.assertRaisesRegex(c1.Reject,"PHYSICAL_TYPE_MISMATCH"):
            admit_canonical(canon(d),c)
if __name__=="__main__":unittest.main(verbosity=2)
