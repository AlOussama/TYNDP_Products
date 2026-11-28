"""Native C5 tests: no expected verdict embedded in candidate input."""
import copy,json,sys,unittest
from pathlib import Path
from hashlib import sha256
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from vmodel import admit,instantiate,export,reimport,evaluate_source,emit_control,digest,DEF,compose_method
from closure import Reject
from cba_reference import (build,variant,claim,rebind,math_only,requirement,metric,test,TEST,REVIEW,SYSTEM,STUDY,METRIC)

def run(d,i):return instantiate(d,digest(d),i,digest(i))
class C5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=build()
    def setUp(self):self.d,self.i=copy.deepcopy(self.base)
    def test_vt01_vt02_requirements_and_tests(self):
        static=admit(self.d,digest(self.d))
        self.assertEqual(static["status"],"STATIC_VALID")
        r=run(self.d,self.i)
        self.assertEqual(r["requirements"][SYSTEM]["status"],"PASS",r)
        self.assertEqual(r["requirements"][STUDY]["status"],"NOT_EXECUTED")
        self.assertEqual(r["tests"][REVIEW]["execution"],"NOT_EXECUTED")
        self.assertEqual(r["contract_conformance"],"NOT_PROVED")
    def test_vt03_multiple_requirements_and_tests(self):
        a=copy.deepcopy(self.d["requirements"][1]);a["id"]="requirement:second";self.d["requirements"].append(a)
        self.d["tests"][0]["requirements"].append(a["id"])
        t=copy.deepcopy(self.d["tests"][0]);t["id"]="test:second";self.d["tests"].append(t)
        self.i["requested_tests"].append(t["id"]);rebind(self.d,self.i)
        r=run(self.d,self.i);self.assertEqual(r["requirements"][a["id"]]["status"],"PASS")
        self.assertEqual(len(r["requirements"][SYSTEM]["test_refs"]),2)
    def test_vt04_references_and_cycles(self):
        d=copy.deepcopy(self.d);d["tests"][0]["requirements"]=["requirement:missing"]
        with self.assertRaisesRegex(Reject,"C5_TEST_REQUIREMENTS"):admit(d,digest(d))
        d=copy.deepcopy(self.d);d["requirements"][1]["parents"]=[SYSTEM]
        with self.assertRaisesRegex(Reject,"C5_DERIVATION_CYCLE"):admit(d,digest(d))
        d=copy.deepcopy(self.d);d["tests"].pop(0)
        with self.assertRaisesRegex(Reject,"C5_REQUIREMENT_TEST_COVERAGE"):admit(d,digest(d))
    def test_vt05_vt06_roles_native_metric(self):
        r=run(self.d,self.i);self.assertEqual([x["value"] for x in r["study_metrics"][METRIC]["value"]],["15","20"])
        self.assertEqual(r["study_metrics"][METRIC]["status"],"COMPUTED_NOT_VALIDATED")
        d=copy.deepcopy(self.d);d["tests"][0]["metric"]=METRIC
        with self.assertRaises(Reject):admit(d,digest(d))
    def test_vt07_vt08_incompatible_types(self):
        from research_assembly import q
        for qty in (q("MW","electricity"),q("EUR","currency","EUR:real:2020")):
            with self.assertRaises(Reject):build(numeric=True,quant_expected=qty)
    def test_vt09_vt10_native_benchmark(self):
        d,i=build(numeric=True)
        r=run(d,i);self.assertEqual(r["tests"]["test:benchmark"]["verdict"],"PASS",r)
        self.assertEqual(r["tests"]["test:benchmark"]["execution"],"EXECUTED")
        d,i=build(numeric=True,expected=[15,21])
        r=run(d,i);self.assertEqual(r["tests"]["test:benchmark"]["verdict"],"FAIL",r)
        # Positive and negative absolute tolerances with an explicit typed input.
        condition="benefit - expected <= atol and expected - benefit <= atol"
        d,i=build(numeric=True,condition=condition,thresholds={"atol":2},expected=[17,22])
        self.assertEqual(run(d,i)["tests"]["test:benchmark"]["verdict"],"PASS")
        d,i=build(numeric=True,condition=condition,thresholds={"atol":2},expected=[18,22])
        self.assertEqual(run(d,i)["tests"]["test:benchmark"]["verdict"],"FAIL")
        # Native relative tolerance, with explicit typed zero-reference branch.
        d,i=build(numeric=True,condition="(expected > zero and benefit - expected <= expected / 10 and expected - benefit <= expected / 10) or (expected == zero and benefit == zero)",thresholds={"zero":0},expected=[16,22])
        self.assertEqual(run(d,i)["tests"]["test:benchmark"]["verdict"],"PASS")
        d,i=build(numeric=True,condition="(expected > zero and benefit - expected <= expected / 10 and expected - benefit <= expected / 10) or (expected == zero and benefit == zero)",thresholds={"zero":0},expected=[0,20])
        self.assertEqual(run(d,i)["tests"]["test:benchmark"]["verdict"],"FAIL")
    def test_vt11_vt12_applicability(self):
        d,i=build(numeric=True,guard={"truth":"FALSE","reason":None})
        r=run(d,i);self.assertEqual(r["tests"]["test:benchmark"]["applicability"],"FALSE")
        self.assertEqual(r["requirements"]["requirement:benchmark"]["status"],"NOT_APPLICABLE")
        d,i=build(numeric=True,guard={"truth":"UNKNOWN","reason":"MISSING_DATA"})
        r=run(d,i);self.assertEqual(r["tests"]["test:benchmark"]["applicability"],"UNKNOWN")
        self.assertNotEqual(r["requirements"]["requirement:benchmark"]["status"],"PASS")
    def test_vt13_vt14_missing_support(self):
        d,i=variant("missing_scenario")
        r=run(d,i);self.assertEqual(r["tests"][TEST]["verdict"],"BLOCKED",r)
        self.assertNotEqual(r["requirements"][SYSTEM]["status"],"PASS")
        d,i=copy.deepcopy(self.base)
        b=i["base"]["slots"][0]
        b.update(data_status="MISSING_DATA",data=None,snapshot_digest=None,witnesses=[],contributions=[],expected_events={})
        self.assertEqual(run(d,i)["tests"][TEST]["verdict"],"BLOCKED")
    def test_vt15_vt16_native_pass_fail(self):
        for name,expected in (("consistent","PASS"),("weather","FAIL"),("demand","FAIL"),("allowed_project","PASS"),("extra_network","FAIL"),("price_basis","FAIL")):
            d,i=variant(name);r=run(d,i)
            self.assertEqual(r["tests"][TEST]["verdict"],expected,(name,r))
            self.assertEqual(r["contract_conformance"],"NOT_PROVED")
    def test_vt17_vt18_evidence(self):
        d,i=variant("missing_evidence");r=run(d,i)
        self.assertEqual(r["tests"][TEST]["verdict"],"NOT_EXECUTED")
        self.assertIsNone(r["tests"][TEST]["computed_evidence"])
        self.i["claims"]=[claim(self.d,self.i,"FAIL")]
        self.assertEqual(run(self.d,self.i)["tests"][TEST]["verdict"],"INCONCLUSIVE")
        self.i["claims"]=[claim(self.d,self.i,"PASS",version="stale")]
        with self.assertRaisesRegex(Reject,"C5_DECLARED_EVIDENCE_BINDING"):run(self.d,self.i)
    def test_vt19_vt20_vt21_method_composition(self):
        from closure_v1 import composition
        d,i=self.d,self.i
        new,ni=build(formula="base-alt+base",method_version="0.3")
        oldslot=d["base"]["slots"][0];newslot=new["base"]["slots"][0]
        bp=digest(d["base"])
        req={"schema":composition.VERSION,"base_ref":bp,"overrides":[{"id":"override:one","slot":oldslot["id"],"expected_old":digest(oldslot),"replacement":newslot,"allowed_expressions":["benefit"]}]}
        rp=digest(req)
        auth={"schema":composition.APPROVAL,"base_ref":bp,"request_ref":rp,"decision_scope":"NON_NORMATIVE_RESEARCH_ONLY","approvals":[{"id":"override:one","slot":oldslot["id"],"old_ref":digest(oldslot),"new_ref":digest(newslot),"allowed_expressions":["benefit"],"authority_ref":oldslot["source_ref"],"source_sha256":oldslot["profile"]["source_sha256"],"decision":"APPROVED_RESEARCH_OVERRIDE","reason":"Synthetic method exchange control"}]}
        with self.assertRaises(Reject):
            compose_method(d,digest(d),req,rp,auth,"0"*64)
        res=compose_method(d,digest(d),req,rp,auth,digest(auth))
        effective=res["definition"]
        self.assertEqual(effective,new)
        self.assertEqual(effective["requirements"],d["requirements"])
        self.assertEqual(effective["tests"],d["tests"])
        with self.assertRaisesRegex(Reject,"C5_INSTANCE_PIN"):run(effective,i)
        n=run(effective,ni);o=run(d,i)
        self.assertEqual(n["requirements"][SYSTEM]["status"],"PASS")
        self.assertEqual([x["value"] for x in n["study_metrics"][METRIC]["value"]],["115","150"])
        self.assertNotEqual(o["evidence"][0]["id"],n["evidence"][0]["id"])
        ni["claims"]=[claim(d,i,"PASS")]
        with self.assertRaisesRegex(Reject,"C5_DECLARED_EVIDENCE_BINDING"):run(effective,ni)
    def test_metric_unrelated_criterion_rejected(self):
        with self.assertRaisesRegex(Reject,"C5_METRIC_CRITERION_DEPENDENCY"):
            build(numeric=True,condition="base == expected")
    def test_vt22_vt23_canonical_and_pin_integrity(self):
        d,i=self.d,self.i;dp,ip=digest(d),digest(i);canonical=export(d,dp,i,ip)
        self.assertEqual(reimport(canonical,dp,ip)["receipt"],run(d,i))
        a,b=[evaluate_source(raw,k,sha256(raw).hexdigest(),dp,ip) for k in ("A","B") for raw in [emit_control(d,i,k)]]
        self.assertEqual(a["package_sha256"],b["package_sha256"])
        self.assertNotEqual(a["audit_identity"],b["audit_identity"])
        self.assertIn(SYSTEM,a["receipt"]["requirements"]);self.assertIn(TEST,a["receipt"]["tests"])
        with self.assertRaisesRegex(Reject,"C5_INSTANCE_PIN"):instantiate(d,dp,i,"0"*64)
        with self.assertRaisesRegex(Reject,"C5_CANONICAL_TAMPER"):reimport(canonical+" ",dp,ip)
        swapped=copy.deepcopy(d);swapped["requirements"].reverse();swapped["metrics"].reverse();swapped["tests"].reverse()
        self.assertEqual(admit(swapped,digest(swapped))["semantic_identity"],admit(d,dp)["semantic_identity"])
    def test_vt24_vt25_projected_model_formulations(self):
        # Independent finite dispatch formulations; not real solver integrations.
        demand=[10,13]; reference_cap=0; project_cap=3
        def enumerate_cost(d,cap):
            return min(5*x+10*(d-x) for x in range(min(d,cap)+1))
        def analytical_cost(d,cap):
            return 10*d-5*min(d,cap)
        for model,cost in (("integer_dispatch",enumerate_cost),("merit_order",analytical_cost)):
            costs=([cost(x,reference_cap) for x in demand],[cost(x,project_cap) for x in demand])
            d,i=build(numeric=True,expected=[15,15],costs=costs,implementation="fixture:"+model)
            r=run(d,i)
            self.assertEqual(r["tests"]["test:benchmark"]["verdict"],"PASS",r)
            self.assertEqual(r["tests"][TEST]["verdict"],"PASS",r)
        # Relaxing cheap capacity beyond authorized project capacity changes the
        # observable benefit and fails the externally declared benchmark.
        costs=([10*x for x in demand],[5*x for x in demand])
        d,i=build(numeric=True,expected=[15,15],costs=costs,implementation="fixture:invalid_relaxation")
        r=run(d,i);self.assertEqual(r["tests"]["test:benchmark"]["verdict"],"FAIL",r)
        self.assertEqual(r["tests"][TEST]["verdict"],"PASS",r)
        print("C5_MODEL_FREEDOM=2 accepted finite projections;1 rejected benchmark;no universal equivalence")
    def test_vt26_qualitative_review(self):
        self.assertEqual(run(self.d,self.i)["tests"][REVIEW]["diagnostic"]["reason"],"EXTERNAL_REVIEW_NOT_VERIFIED")
    def test_vt27_migration(self):
        with self.assertRaises(Reject):admit(self.d["base"],digest(self.d["base"]))
        self.assertEqual(self.d["base"],self.base[0]["base"])
        r=run(self.d,self.i);self.assertEqual(r["native_receipt"]["status"],"RETURNED")
    def test_vt28_integrated_nine_variants(self):
        cases={"consistent":"PASS","weather":"FAIL","demand":"FAIL","missing_scenario":"BLOCKED","allowed_project":"PASS","extra_network":"FAIL","price_basis":"FAIL","missing_evidence":"NOT_EXECUTED","math_correct_invalid":"FAIL"}
        output=HERE/"generated"
        for name,expected in cases.items():
            d,i=variant(name);dp,ip=digest(d),digest(i);results=[]
            for kind in ("A","B"):
                raw=emit_control(d,i,kind);result=evaluate_source(raw,kind,sha256(raw).hexdigest(),dp,ip)
                self.assertEqual(result["receipt"]["tests"][TEST]["verdict"],expected,(name,kind,result))
                results.append(result)
                if output.exists():(output/(name+"."+kind+".txt")).write_bytes(raw)
            self.assertEqual(results[0]["package_sha256"],results[1]["package_sha256"])
            if output.exists():(output/(name+".canonical.json")).write_text(export(d,dp,i,ip))
            if name=="math_correct_invalid":self.assertEqual(math_only(d,i),["15","20"])
            print("C5_VARIANT="+json.dumps({"name":name,"expected":expected,"actual":results[0]["receipt"]["tests"][TEST],"requirement":results[0]["receipt"]["requirements"][SYSTEM],"native":results[0]["receipt"]["native_receipt"]["status"],"math_only":math_only(d,i) if name=="math_correct_invalid" else None,"definition_pin":dp,"instance_pin":ip,"package_sha256":results[0]["package_sha256"],"A_source":results[0]["source_sha256"],"B_source":results[1]["source_sha256"]},sort_keys=True))
    def test_controlled_ablation(self):
        # Same scope and target; removing explicit Requirement-to-Test links or
        # criterion reference makes the V-model profile unadmittable.
        for key in ("requirements","criterion","metric","coverage","oracle_ref"):
            d=copy.deepcopy(self.d);del d["tests"][0][key]
            with self.assertRaises(Reject):admit(d,digest(d))
            print("C5_ABLATION="+key+":REJECTED")
    def test_maintenance_metric_criterion_and_reuse(self):
        d,i=build(numeric=True)
        a=copy.deepcopy(d["metrics"][-1]);a["id"]="metric:benchmark2"
        d["metrics"].append(a)
        d["requirements"][-1]["metric_refs"].append(a["id"])
        z=copy.deepcopy(d["tests"][-1]);z["id"]="test:benchmark2";z["metric"]=a["id"];d["tests"].append(z)
        i["requested_tests"].append(z["id"]);rebind(d,i)
        self.assertEqual(run(d,i)["tests"][z["id"]]["verdict"],"PASS")
        print("C5_CHANGE=metric_reuse:2_new_records,2_ref_updates,1_definition_ref_update;0_base_or_validator_edits")
        relaxed,ri=build(numeric=True,condition="benefit <= expected",expected=[15,21])
        exact,ei=build(numeric=True,expected=[15,21])
        self.assertEqual(run(relaxed,ri)["tests"]["test:benchmark"]["verdict"],"PASS")
        self.assertEqual(run(exact,ei)["tests"]["test:benchmark"]["verdict"],"FAIL")
        self.assertEqual(relaxed["tests"],exact["tests"])
        self.assertEqual(relaxed["requirements"],exact["requirements"])
        print("C5_CHANGE=criterion:one_native_condition,derived_repinning;0_outer_requirement_or_test_edits")
        old=run(relaxed,ri);relaxed["requirements"][0]["statement"]+=" Revised research wording."
        rebind(relaxed,ri);new=run(relaxed,ri)
        self.assertEqual(old["native_receipt"],new["native_receipt"])
        self.assertNotEqual(old["definition_pin"],new["definition_pin"])
        print("C5_CHANGE=semantic_wording:1_requirement_field,1_definition_ref_update;0_native_math_edits")
    def test_maintenance_add_requirement_and_test(self):
        d,i=self.d,self.i
        before=admit(d,digest(d))["semantic_identity"]
        a=copy.deepcopy(d["requirements"][1]);a["id"]="requirement:additional";d["requirements"].append(a)
        t=copy.deepcopy(d["tests"][0]);t["id"]="test:additional";t["requirements"]=[a["id"]];d["tests"].append(t)
        i["requested_tests"].append(t["id"]);rebind(d,i)
        self.assertEqual(run(d,i)["requirements"][a["id"]]["status"],"PASS")
        self.assertNotEqual(before,admit(d,digest(d))["semantic_identity"])
        print("C5_CHANGE=2_new_records,1_requested_test_ref,1_definition_ref_update;0_base_or_validator_edits")
if __name__=="__main__":unittest.main(verbosity=2)
