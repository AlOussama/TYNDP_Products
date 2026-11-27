import copy,json,unittest
from closure import admit,reimport,bind_data,digest,Reject
def q(unit="1",carrier="none",basis="NONE"):
    return {"unit":unit,"carrier":carrier,"basis":basis,"sign":"NONE","direction":"NONE","time_basis":"NONE"}
def fixture(d,quant=None,roles=None,domain_rules=None,domains=None,pred_axes=None,temporal=None,conversions=None):
    quant=quant or {};roles=roles or {};domain_rules=domain_rules or {};domains=domains or {};pred_axes=pred_axes or {};temporal=temporal or {};conversions=conversions or {}
    dims=d.get("dimensions",{});params=d.get("parameters",{});expr=d.get("expressions",{})
    sym={}
    for n in list(params)+list(expr):
        sym[n]={"id":"ref:"+n,"role":"DERIVED_EXPRESSION" if n in expr else roles.get(n,"OBSERVABLE"),"quantity":quant.get(n,q()),"domain_rule":domain_rules.get(n,"ANY_EXACT")}
    m={"id":"method:research","version":"0.2","inputs":[n for n,z in sym.items() if z["role"] in ("INPUT","OBSERVABLE","EXTERNAL_WITNESS")],"parameters":[n for n,z in sym.items() if z["role"]=="METHOD_PARAMETER"],"outputs":list(expr)}
    c={"domains":{n:{"id":"domain:"+n,"labels":domains.get(n,[0,1,2] if z.get("dtype")=="int" else ["a","b"])} for n,z in dims.items()},
       "relations":{n:{"id":"relation:"+n,"source_ref":"fixture:"+n} for n in d.get("relations",{})},
       "symbols":sym,
       "predicates":{n:{"id":"pred:"+n,"role":"DATA_ASSUMPTION" if n in d.get("assumptions",{}) else "PREDICATE","axes":pred_axes.get(n,list(dims))} for n in list(d.get("conditions",{}))+list(d.get("assumptions",{}))},
       "scope":{"id":"scope:research","binders":list(dims),"alignment":"SAME_OR_SCALAR"},
       "temporal":temporal,"conversions":conversions,"method":m,
       "study":{"id":"study:research","version":"0.2","method_ref":digest(m),"data_id":"data:research","data_version":"0.2","owner":"OWNER_TBD"},
       "audit":{"source_id":"source:research","source_ref":"fixture:0.2","evidence_id":"evidence:request","authority":"RESEARCH_ASSUMPTION"}}
    return c
def open_(d,c):return admit(json.dumps(d),c)
def arithmetic(expr="a + b"):
    d={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True}},"parameters":{"a":{"dims":["t"]},"b":{"dims":["t"]}},"expressions":{"v":expr},"conditions":{"match":"a >= b"}}
    c=fixture(d)
    return d,c
def timepolicy(shift="ZERO",window="TRUNCATE"):
    return {"t":{"id":"time:research","chronology_ref":"fixture:ordered-t","shift_edge":shift,"window_edge":window}}
def dataset(p,r=None):
    return {"id":"data:research","version":"0.2","parameters":p,"relations":r or {}}
def series(xs):return [{"key":[i],"value":v} for i,v in enumerate(xs)]
def scalar(x):return [{"key":[],"value":x}]
def relation_fixture(group=False):
    d={"version":0,"dimensions":{"bus":{},"branch":{}},"relations":{"endpoint":{"key":"branch","values":"bus"}},"parameters":{"a":{"dims":["branch" if group else "bus"]}},"expressions":{"v":"sum(a, over=branch, by=endpoint[bus])" if group else "at(a, by=endpoint[bus])"}}
    c=fixture(d,domains={"bus":["b1","b2"],"branch":["l1","l2","l3"]},quant={"a":q("MW","electricity"),"v":q("MW","electricity")})
    rows=[{"branch":"l1","bus":"b1"},{"branch":"l2","bus":"b1"},{"branch":"l3","bus":"b2"}]
    values=[{"key":[n],"value":i+1} for i,n in enumerate(c["domains"]["branch" if group else "bus"]["labels"])]
    return d,c,dataset({"a":values},{"endpoint":rows})
class Closure(unittest.TestCase):
    def bad(self,d,c,code):
        with self.assertRaisesRegex(Reject,code):open_(d,c)
    def test_A01_all_arithmetic_nodes(self):
        for expr in ("a+b","-a","a*b","a/2","a**2","sum(a, over=t)","a+1"):
            d,c=arithmetic(expr);leaf=open_(d,c);self.assertEqual(leaf,reimport(leaf))
        d,c=arithmetic();d["expressions"]["w"]="v + a";c=fixture(d);self.assertEqual(open_(d,c)["interface"]["symbols"]["w"]["role"],"DERIVED_EXPRESSION")
    def test_A02_native_roundtrip_and_canonical_as_source(self):
        d,c=arithmetic();a=open_(d,c);b=admit(a["native_canonical"],c,True)
        self.assertEqual(a["native_identity"],b["native_identity"]);self.assertEqual(a["semantic_identity"],b["semantic_identity"])
        self.assertNotEqual(a["audit_identity"],b["audit_identity"])
    def test_A03_exact_admission_before_float(self):
        for x in ("9007199254740993 * a","a * 1.00000000000000001","inf * a","a / 0","a * 1e-324","a * 1e3"):
            d,c=arithmetic(x);self.bad(d,c,"NUMERIC|NONFINITE|DIVISOR|NATIVE_REJECT")
    def test_A04_nonzero_bound_domain(self):
        d,c=arithmetic("a / b");self.bad(d,c,"DIVISOR_NONZERO_REQUIRED")
        c["symbols"]["b"]["domain_rule"]="NONZERO";leaf=open_(d,c)
        with self.assertRaisesRegex(Reject,"DATA_NUMERIC_DOMAIN"):bind_data(leaf,dataset({"a":series([1,2,3]),"b":series([1,0,1])}))
        self.assertEqual(bind_data(leaf,dataset({"a":series([1,2,3]),"b":series([1,2,1])}))["predicate_verdict"],"NOT_EXECUTED")
    def test_A05_quantity_in_unused_expression(self):
        d,c=arithmetic();c["symbols"]["a"]["quantity"]=q("MW","electricity")
        c["symbols"]["b"]["quantity"]=q("MW_heat","heat")
        self.bad(d,c,"PHYSICAL_TYPE")
    def test_C01_conditions_and_refs(self):
        d,c=arithmetic();d["conditions"].update(other="a <= b",both="match AND NOT other",either="match OR other")
        c=fixture(d);leaf=open_(d,c);self.assertEqual(len(leaf["interface"]["predicates"]),4)
    def test_C02_physical_comparison(self):
        d,c=arithmetic("a");c["symbols"]["a"]["quantity"]=q("MW","electricity");c["symbols"]["v"]["quantity"]=q("MW","electricity")
        c["symbols"]["b"]["quantity"]=q("kg/h","hydrogen")
        self.bad(d,c,"COMPARISON_TYPE")
    def test_C03_folded_invalid_condition(self):
        d,c=arithmetic("a");d["conditions"]["match"]="False AND a >= b";c=fixture(d)
        self.bad(d,c,"FOLDED_CONDITION_LITERAL")
    def test_C04_explicit_typed_literal(self):
        d,c=arithmetic("a");d["conditions"]["match"]="a > 0"
        for n in ("a","v"):c["symbols"][n]["quantity"]=q("MW","electricity")
        self.bad(d,c,"TYPED_LITERAL_REQUIRED|COMPARISON_TYPE")
    def test_C05_cross_axis_comparison(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"},"s":{}},"parameters":{"a":{"dims":["t"]},"b":{"dims":["s"]}},"conditions":{"match":"a >= b"}}
        self.bad(d,fixture(d),"IMPLICIT_CROSS_ALIGNMENT")
    def test_C06_assumption_role(self):
        d,c=arithmetic();d["assumptions"]={"domain_check":"a >= b"};c=fixture(d,roles={"a":"INPUT","b":"METHOD_PARAMETER"})
        self.assertEqual(open_(d,c)["interface"]["predicates"]["domain_check"]["role"],"DATA_ASSUMPTION")
        c=fixture(d);self.bad(d,c,"ASSUMPTION_IS_NOT_GUARANTEE")
    def test_C07_bool_guard_no_unknown(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"}},"parameters":{"g":{"dims":["t"],"dtype":"bool"}},"conditions":{"available":"g"}}
        c=fixture(d);leaf=open_(d,c)
        with self.assertRaisesRegex(Reject,"UNKNOWN_BOOL"):bind_data(leaf,dataset({"g":series([True,None,False])}))
        self.assertEqual(bind_data(leaf,dataset({"g":series([True,True,False])}))["predicate_verdict"],"NOT_EXECUTED")
    def test_C08_cases_all_regions(self):
        d,c=arithmetic();d["expressions"]={"v":{"dims":["t"],"cases":{"early":{"when":"position(t) == 0","expression":"a"}},"otherwise":"b"}}
        c=fixture(d,temporal=timepolicy());self.assertEqual(open_(d,c)["interface"]["temporal_domains"],["t"])
        c["symbols"]["b"]["quantity"]=q("MW","electricity");self.bad(d,c,"CASE_PHYSICAL_TYPE")
    def test_C09_case_requires_explicit_else(self):
        d,c=arithmetic();d["expressions"]={"v":{"dims":["t"],"cases":{"early":{"when":"position(t) == 0","expression":"a"}}}}
        self.bad(d,c,"CASE_FIELDS")
    def test_R01_lookup_native(self):
        d,c,data=relation_fixture();a=open_(d,c);self.assertEqual(bind_data(a,data)["stage"],"FINITE_INPUT_SUPPORT_ONLY")
    def test_R02_group_sum_native(self):
        d,c,data=relation_fixture(True);a=open_(d,c);self.assertEqual(bind_data(a,data)["predicate_verdict"],"NOT_EXECUTED")
    def test_R03_duplicate_key(self):
        d,c,data=relation_fixture();a=open_(d,c);data["relations"]["endpoint"].append(data["relations"]["endpoint"][0])
        with self.assertRaisesRegex(Reject,"RELATION_DUPLICATE_KEY"):bind_data(a,data)
    def test_R04_missing_key(self):
        d,c,data=relation_fixture();a=open_(d,c);data["relations"]["endpoint"].pop()
        with self.assertRaisesRegex(Reject,"RELATION_KEY_COVERAGE"):bind_data(a,data)
    def test_R05_empty_group(self):
        d,c,data=relation_fixture(True);a=open_(d,c);data["relations"]["endpoint"][-1]["bus"]="b1"
        with self.assertRaisesRegex(Reject,"RELATION_GROUP_COVERAGE"):bind_data(a,data)
    def test_R06_unknown_coordinate(self):
        d,c,data=relation_fixture();a=open_(d,c);data["relations"]["endpoint"][-1]["bus"]="unknown"
        with self.assertRaisesRegex(Reject,"DATA_COORDINATE"):bind_data(a,data)
    def test_T01_explicit_shift(self):
        d,c=arithmetic("shift(a, along=t, offset=1, edge=0)");c=fixture(d,temporal=timepolicy())
        self.assertEqual(open_(d,c)["interface"]["temporal_domains"],["t"])
    def test_T02_implicit_edge_rejected(self):
        d,c=arithmetic("shift(a, along=t, offset=1)");c=fixture(d,temporal=timepolicy())
        self.bad(d,c,"SHIFT_EDGE|NATIVE_REJECT")
    def test_T03_window_policy(self):
        d,c=arithmetic("sum_back(a, along=t, window=2)");c=fixture(d,temporal=timepolicy())
        self.assertEqual(open_(d,c)["interface"]["temporal_domains"],["t"])
        c["temporal"]["t"]["window_edge"]="WRAP";self.bad(d,c,"WINDOW_EDGE")
    def test_T04_future_shift_rejected(self):
        d,c=arithmetic("shift(a, along=t, offset=-1, edge=0)");c=fixture(d,temporal=timepolicy())
        self.bad(d,c,"SHIFT_SCOPE")
    def test_T05_order_changes_bound_identity(self):
        d,c=arithmetic("shift(a, along=t, offset=1, edge=0)");c=fixture(d,temporal=timepolicy())
        a=open_(d,c);c["domains"]["t"]["labels"].reverse();b=open_(d,c)
        self.assertEqual(a["native_identity"],b["native_identity"]);self.assertNotEqual(a["semantic_identity"],b["semantic_identity"])
    def test_M01_rc03_conversion(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"}},"parameters":{"flow":{"dims":["t"]},"h":{"dims":[]}},"expressions":{"power":"flow*h"}}
        cv={"h":{"id":"conversion:lhv","version":"1","source_ref":"fixture:lhv","source_sha256":"a"*64,"authority":"RESEARCH_ASSUMPTION"}}
        c=fixture(d,quant={"flow":q("kg/h","hydrogen"),"h":q("MWh_H2_LHV/kg","conversion","LHV"),"power":q("MW_H2_LHV","hydrogen","LHV")},roles={"h":"METHOD_PARAMETER"},domain_rules={"h":"POSITIVE"},conversions=cv)
        a=open_(d,c);r=bind_data(a,dataset({"flow":series([600,600,600]),"h":scalar("1/30")}))
        self.assertEqual(r["owner"],"OWNER_TBD")
        c["conversions"]={};self.bad(d,c,"CONVERSION_BINDING")
    def test_M02_rc08_cost_and_price_basis(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"}},"parameters":{"cost":{"dims":["t"]},"dt":{"dims":["t"]},"capex":{"dims":[]}},"expressions":{"total":"sum(cost*dt, over=t)+capex"}}
        c=fixture(d,quant={"cost":q("EUR/h","currency","EUR:real:2025"),"dt":q("h"),"capex":q("EUR","currency","EUR:real:2025"),"total":q("EUR","currency","EUR:real:2025")})
        a=open_(d,c);self.assertEqual(a["interface"]["method_signature"]["outputs"][0]["quantity"]["unit"],"EUR")
        c["symbols"]["capex"]["quantity"]=q("EUR","currency","EUR:nominal:2025");self.bad(d,c,"PHYSICAL_TYPE")
    def test_M03_method_and_study_signatures(self):
        d,c=arithmetic();a=open_(d,c);data=dataset({"a":series([1,2,3]),"b":series([1,2,3])});r=bind_data(a,data)
        c["method"]["version"]="0.3";self.bad(d,c,"STUDY_BINDING")
        c["study"]["method_ref"]=digest(c["method"]);b=open_(d,c);z=bind_data(b,data)
        self.assertEqual(a["native_identity"],b["native_identity"]);self.assertNotEqual(r["context_identity"],z["context_identity"])
    def test_M04_role_signature_mismatch(self):
        d,c=arithmetic();c["symbols"]["a"]["role"]="METHOD_PARAMETER";self.bad(d,c,"METHOD_SIGNATURE")
    def test_M05_data_context_and_exact_identity(self):
        d,c=arithmetic();a=open_(d,c);data=dataset({"a":series(["1/2","2","3"]),"b":series([1,2,3])})
        x=bind_data(a,data);data["parameters"]["a"][0]["value"]="0.5";y=bind_data(a,data)
        self.assertEqual(x["data_identity"],y["data_identity"]);self.assertNotEqual(x["data_audit_identity"],y["data_audit_identity"])
        data["version"]="wrong"
        with self.assertRaisesRegex(Reject,"DATA_CONTEXT"):bind_data(a,data)
    def test_M06_integer_and_unknown(self):
        d,c=arithmetic();d["parameters"]["a"]["dtype"]="int";a=open_(d,c)
        for val,code in [("1/2","INTEGER_DOMAIN"),(None,"UNKNOWN_OR_NONEXACT"),(True,"UNKNOWN_OR_NONEXACT")]:
            with self.assertRaisesRegex(Reject,code):bind_data(a,dataset({"a":series([1,val,3]),"b":series([1,2,3])}))
    def test_G01_tamper_and_solver(self):
        d,c=arithmetic();a=open_(d,c);a["raw_ast"]={}
        with self.assertRaisesRegex(Reject,"LEAF_TAMPER"):reimport(a)
        d["variables"]={"x":{"dims":["t"]}};self.bad(d,c,"NATIVE_SECTION")
    def test_G02_duplicate_source(self):
        d,c=arithmetic()
        with self.assertRaisesRegex(Reject,"YAML_DUPLICATE"):admit('version: 0\nversion: 0\n',c)
    def test_G03_unauthorized_authority(self):
        d,c=arithmetic();c["study"]["owner"]="APPROVED";self.bad(d,c,"STUDY_BINDING")
    def test_G04_duplicate_ids(self):
        d,c=arithmetic();c["symbols"]["a"]["id"]=c["symbols"]["b"]["id"];self.bad(d,c,"AMBIGUOUS_ID")
    def test_C10_scalar_parameter_condition(self):
        d,c=arithmetic();d["conditions"]["positive"]="a >= 0";c=fixture(d)
        self.assertIn("positive",open_(d,c)["interface"]["predicates"])
    def test_C11_dimension_comparison(self):
        d,c=arithmetic();d["conditions"]["late"]="t >= 1";c=fixture(d)
        self.assertIn("late",open_(d,c)["interface"]["predicates"])
    def test_C12_native_count(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"}},"parameters":{"g":{"dims":["t"],"dtype":"bool"}},"conditions":{"available":"g","enough":"count(available, over=t) >= 1"}}
        c=fixture(d,pred_axes={"available":["t"],"enough":[]})
        self.assertEqual(open_(d,c)["interface"]["predicates"]["enough"]["axes"],[])
    def test_C13_native_joined_condition(self):
        d,c,data=relation_fixture();d["conditions"]={"positive":"a > 0","at_branch":"at(positive, by=endpoint[bus])"}
        # Named condition numeric literal is dimensionless in this fixture.
        c=fixture(d,domains={"bus":["b1","b2"],"branch":["l1","l2","l3"]},pred_axes={"positive":["bus"],"at_branch":["branch"]})
        self.assertEqual(bind_data(open_(d,c),data)["predicate_verdict"],"NOT_EXECUTED")
    def test_T06_explicit_wrap(self):
        d,c=arithmetic("shift(a, along=t, offset=1, edge='wrap')");c=fixture(d,temporal=timepolicy("WRAP"))
        self.assertEqual(open_(d,c)["interface"]["temporal_domains"],["t"])
        c["temporal"]["t"]["shift_edge"]="ZERO";self.bad(d,c,"SHIFT_EDGE")
    def test_T07_window_beyond_support(self):
        d,c=arithmetic("sum_back(a, along=t, window=4)");c=fixture(d,temporal=timepolicy())
        self.bad(d,c,"WINDOW_SCOPE")
    def test_R07_rc05_oriented_net(self):
        d={"version":0,"dimensions":{"bus":{},"branch":{}},"relations":{"sending":{"key":"branch","values":"bus"},"receiving":{"key":"branch","values":"bus"}},
           "parameters":{"flow":{"dims":["branch"]},"injection":{"dims":["bus"]},"zero":{"dims":[]},"x":{"dims":["branch"]}},
           "expressions":{"net":"sum(flow, over=branch, by=sending[bus]) - sum(flow, over=branch, by=receiving[bus])","cycle":"sum(flow*x, over=branch)"},
           "conditions":{"kcl":"net == injection","kvl":"cycle == zero"}}
        quant={k:q("MW","electricity") for k in ("flow","injection","zero","net","cycle")}
        c=fixture(d,quant=quant,domains={"bus":["b1","b2","b3"],"branch":["l1","l2","l3"]},pred_axes={"kcl":["bus"],"kvl":[]})
        leaf=open_(d,c)
        data=dataset({"flow":[{"key":["l"+str(i+1)],"value":v} for i,v in enumerate([2,1,-3])],
                      "injection":[{"key":["b"+str(i+1)],"value":v} for i,v in enumerate([5,-1,-4])],
                      "zero":scalar(0),"x":[{"key":["l"+str(i+1)],"value":1} for i in range(3)]},
                     {"sending":[{"branch":"l"+str(i+1),"bus":"b"+str(i+1)} for i in range(3)],
                      "receiving":[{"branch":"l"+str(i+1),"bus":"b"+str((i+1)%3+1)} for i in range(3)]})
        self.assertEqual(bind_data(leaf,data)["stage"],"FINITE_INPUT_SUPPORT_ONLY")
        # Independent finite arithmetic, NOT an evaluation of the native AST.
        from fractions import Fraction as F
        flows=[F(v["value"]) for v in data["parameters"]["flow"]]
        self.assertEqual([flows[i]-flows[(i-1)%3] for i in range(3)],[F(5),F(-1),F(-4)])
        self.assertEqual(sum(flows),0)
        self.assertEqual([flows[i]+1-(flows[(i-1)%3]+1) for i in range(3)],[F(5),F(-1),F(-4)])
        self.assertNotEqual(sum(v+1 for v in flows),0)
    def test_M07_qualified_method_axes(self):
        d,c=arithmetic();a=open_(d,c)
        self.assertEqual(a["interface"]["method_signature"]["inputs"][0]["domain_ids"],["domain:t"])
        c["domains"]["t"]["id"]="domain:other_t";b=open_(d,c)
        self.assertNotEqual(a["interface"]["method_identity"],b["interface"]["method_identity"])
    def test_G05_process_determinism(self):
        import subprocess,sys,os
        from pathlib import Path
        here=str(Path(__file__).parent)
        cmd=[sys.executable,"-c","import sys;sys.path.insert(0,"+repr(here)+");from test_closure import *;d,c=arithmetic();print(open_(d,c)['semantic_identity'])"]
        a=subprocess.check_output(cmd,env=dict(os.environ,PYTHONHASHSEED="7"))
        b=subprocess.check_output(cmd,env=dict(os.environ,PYTHONHASHSEED="101"))
        self.assertEqual(a,b)
if __name__=="__main__":unittest.main(verbosity=2)
