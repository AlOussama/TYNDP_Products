"""New targeted controls; no original full-chain paths are counted."""
import sys,json,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from interface import finite_consumer
from closure import admit,Reject
from package_interface import export_package
from test_closure import fixture,q,arithmetic,timepolicy,dataset,series,relation_fixture
from closure_v1 import metadata

def pkg(d,c):return export_package(admit(json.dumps(d),c))
def auth():return {"id":"authority:source","role":"SOURCE","immutable_ref":"fixture:source","revision":"1","decision_state":"OWNER_TBD"}
def frame():
    f={"schema":"c2-study-frame-0.1","id":"frame:test","version":"1","question":"Finite synthetic research"}
    f.update({k:[] for k in metadata.COLLECTIONS});f["authorities"]=[auth()]
    return f
def ts():
    f=frame();f["domains"]=[{"id":"domain:t","kind":"time","members":[0,1,2],"ordered":True},{"id":"domain:s","kind":"scenario","members":["a","b"],"ordered":False}]
    f["chronologies"]=[{"id":"chronology:t","domain":"domain:t","mode":"NONCYCLIC","authority_refs":["authority:source"],"intervals":[{"label":i,"start_h":i,"end_h":i+1,"duration_h":1} for i in range(3)]}]
    f["information_sets"]=[{"id":"info:"+str(i),"time_domain":"domain:t","stage":i,"scenario_domain":"domain:s","partition":[["a","b"]] if i==0 else [["a"],["b"]]} for i in range(3)]
    return f
class ClosureControls(unittest.TestCase):
    def test_CL01_native_shift_window(self):
        for expr,policy,expected in [("shift(a, along=t, offset=1, edge=0)",timepolicy(),["0","2","3"]),("shift(a, along=t, offset=1, edge='wrap')",timepolicy("WRAP"),["5","2","3"]),("sum_back(a, along=t, window=2)",timepolicy(),["2","5","8"])]:
            d,c=arithmetic(expr);c=fixture(d,temporal=policy)
            p=pkg(d,c);r=finite_consumer(p,dataset({"a":series([2,3,5]),"b":series([1,1,1])}))
            self.assertEqual(r.outputs()["v"],expected)
    def test_CL02_native_defined_count(self):
        d={"version":0,"dimensions":{"t":{"dtype":"int"}},"parameters":{"g":{"dims":["t"],"dtype":"bool"}},"conditions":{"available":"g","enough":"count(available, over=t) >= 3"}}
        c=fixture(d,pred_axes={"available":["t"],"enough":[]})
        r=finite_consumer(pkg(d,c),dataset({"g":series([False,True,False])}))
        self.assertEqual(r.conditions(),{"available":True,"enough":True})
        with self.assertRaisesRegex(Reject,"UNKNOWN_BOOL"):finite_consumer(pkg(d,c),dataset({"g":series([False,None,False])}))
    def test_CL03_native_joined_condition(self):
        d,c,data=relation_fixture();d["conditions"]={"positive":"a > 0","at_branch":"at(positive, by=endpoint[bus])"}
        c=fixture(d,domains={"bus":["b1","b2"],"branch":["l1","l2","l3"]},pred_axes={"positive":["bus"],"at_branch":["branch"]})
        r=finite_consumer(pkg(d,c),data);self.assertEqual(r.conditions(),{"positive":True,"at_branch":True})
        data["parameters"]["a"][0]["value"]=-1
        self.assertFalse(finite_consumer(pkg(d,c),data).conditions()["at_branch"])
    def test_CL04_metadata_ports_and_carrier(self):
        f=frame();f["components"]=[{"id":"component:a","kind":"storage","authority_refs":["authority:source"]},{"id":"component:b","kind":"network","authority_refs":["authority:source"]}]
        f["ports"]=[{"id":"port:"+n,"component_ref":"component:"+n,"direction":di,"quantity":q("MW","electricity"),"axes":[],"authority_refs":["authority:source"]} for n,di in (("a","OUT"),("b","IN"))]
        f["relations"]=[{"id":"relation:connection","kind":"connected_to","from":"port:a","to":"port:b","authority_refs":["authority:source"]}]
        f["observables"]=[{"id":"observable:p","subject":"port:a","quantity":q("MW","electricity"),"axes":[],"projection":"IDENTITY","value_type":"REAL","authority_refs":["authority:source"]}]
        metadata.validate(f)
        bad=copy.deepcopy(f);bad["ports"][1]["quantity"]=q("MW_heat","heat")
        with self.assertRaisesRegex(Reject,"RELATION_TYPE"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["ports"][1]["direction"]="OUT"
        with self.assertRaisesRegex(Reject,"PORT_COMPATIBILITY"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["observables"][0]["quantity"]=q("MWh","electricity")
        with self.assertRaisesRegex(Reject,"OBSERVABLE_TYPE"):metadata.validate(bad)
    def test_CL05_chronology_information(self):
        f=ts();metadata.validate(f)
        bad=copy.deepcopy(f);bad["information_sets"][2]["partition"]=[["a","b"]]
        with self.assertRaisesRegex(Reject,"INFORMATION_REFINEMENT"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["chronologies"][0]["intervals"][1]["duration_h"]=0
        with self.assertRaisesRegex(Reject,"DURATION_OR_CHRONOLOGY"):metadata.validate(bad)
        bad=copy.deepcopy(f);bad["information_sets"].pop()
        with self.assertRaisesRegex(Reject,"INFORMATION_STAGE_COVERAGE"):metadata.validate(bad)
def assertion(package,id,name,axes,kinds,role="SAFETY_GUARANTEE",guard=None,at=None,assumptions=None):
    from interface import predicate_client
    pr=predicate_client(package,"pred:"+name,"DATA_ASSUMPTION" if role=="DATA_ASSUMPTION" else "PREDICATE")
    return {"id":id,"role":role,"modality":"MUST","predicate":{"predicate_id":pr["predicate_id"],"role":pr["role"],"axes":pr["qualified_axes"],"scope_id":pr["scope_id"]},"scope":"scope:main","binders":[{"axis":a,"kind":k,"quantifier":"EXISTS" if k=="response" and role in ("SERVICE_GUARANTEE","CAPABILITY_GUARANTEE") else "FORALL"} for a,k in zip(axes,kinds,strict=True)],"at":at or {},"guard":guard or {"truth":"TRUE","reason":None},"assumptions":assumptions or [],"authority_refs":["authority:source"]}

class ObligationControls(unittest.TestCase):
    def service(self,role):
        from common_fixtures import build,p
        from interface import predicate_client
        from closure_v1.obligations import Bound
        c=build("C2SERVICE",{"r":["r1","r2"],"y":["y1","y2"]},{"a":p("r","y"),"threshold":p(),"available":p("r")},{},{"ok":"a >= threshold","enabled":"available >= 1"},{"a":[1,0,0,1],"threshold":1,"available":[1,1]},{},{},None,roles={"available":"INPUT","threshold":"INPUT"},pred_axes={"ok":["r","y"],"enabled":["r"]})
        c["context"]["predicates"]["enabled"]["role"]="GUARD"
        pck=pkg(c["doc"],c["context"]);f=frame()
        f["domains"]=[{"id":"domain:r","kind":"request","members":["r1","r2"],"ordered":False},{"id":"domain:y","kind":"response","members":["y1","y2"],"ordered":False}]
        f["scopes"]=[{"id":"scope:main","domains":["domain:r","domain:y"],"subjects":[]}]
        t=metadata.validate(f);bound=Bound(pck,t,c["data"])
        g=predicate_client(pck,"pred:enabled","GUARD")
        ref={"predicate_id":g["predicate_id"],"role":g["role"],"axes":g["qualified_axes"],"scope_id":g["scope_id"]}
        a=assertion(pck,"assertion:service","ok",["domain:r","domain:y"],["request","response"],role,{"predicate":ref})
        return c,pck,f,bound,a
    def test_CL06_service_requires_actual_witness(self):
        from closure_v1.obligations import evaluate,Bound
        c,pck,f,b,a=self.service("SERVICE_GUARANTEE")
        self.assertEqual(evaluate(b,[a],[])["status"],"BLOCKED")
        w=[{"id":"witness:"+r,"assertion":a["id"],"key":[r],"response":y,"source_ref":"authority:source","data_identity":b.data_identity} for r,y in (("r1","y1"),("r2","y2"))]
        self.assertEqual(evaluate(b,[a],w)["status"],"FINITE_OBSERVATIONS_ONLY")
        w[0]["response"]="y2"
        self.assertEqual(evaluate(b,[a],w)["status"],"FINITE_COUNTEREXAMPLE")
        w[0]["data_identity"]="wrong"
        with self.assertRaisesRegex(Reject,"WITNESS_SNAPSHOT"):evaluate(b,[a],w)
    def test_CL07_capability_order_and_nonvacuity(self):
        from closure_v1.obligations import evaluate,Bound
        c,pck,f,b,a=self.service("CAPABILITY_GUARANTEE")
        self.assertEqual(evaluate(b,[a],[])["status"],"FINITE_OBSERVATIONS_ONLY")
        a["binders"].reverse()
        with self.assertRaisesRegex(Reject,"REQUEST_RESPONSE_ORDER"):evaluate(b,[a],[])
        a["binders"].reverse()
        for row in c["data"]["parameters"]["available"]:row["value"]=0
        b=Bound(pck,metadata.validate(f),c["data"])
        self.assertEqual(evaluate(b,[a],[])["status"],"BLOCKED")
    def test_CL08_scoped_assumptions_unknown(self):
        from closure_v1.obligations import Bound,evaluate
        d,c=arithmetic();d["assumptions"]={"valid":"a >= b"}
        c=fixture(d,roles={"a":"INPUT","b":"INPUT"})
        pck=pkg(d,c);f=ts();f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":[]}]
        b=Bound(pck,metadata.validate(f),dataset({"a":series([1,0,3]),"b":series([1,1,1])}))
        a=assertion(pck,"assertion:assume","valid",["domain:t"],["time"],"DATA_ASSUMPTION")
        g=assertion(pck,"assertion:guarantee","match",["domain:t"],["time"],assumptions=[a["id"]])
        r=evaluate(b,[a,g],[]);self.assertEqual(r["status"],"FINITE_OBSERVATIONS_ONLY")
        a["guard"]={"truth":"UNKNOWN","reason":"AUTHORITY_UNRESOLVED"}
        self.assertEqual(evaluate(b,[a,g],[])["status"],"BLOCKED")
        g["assumptions"]=[]
        with self.assertRaisesRegex(Reject,"UNBOUND_ASSUMPTION"):evaluate(b,[a,g],[])
    def test_CL09_full_information_policy(self):
        from closure_v1.obligations import Bound,nonanticipativity
        d={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True},"s":{"dtype":"str"}},"parameters":{"decision":{"dims":["s","t"]}}}
        c=fixture(d,domains={"t":[0,1,2],"s":["a","b"]});pck=pkg(d,c)
        rows=[{"key":[s,t],"value":v} for s,vs in (("a",[10,20,30]),("b",[10,40,50])) for t,v in enumerate(vs)]
        data=dataset({"decision":rows});f=ts()
        p=[{"id":"policy:decision","symbol":"ref:decision","time_domain":"domain:t","scenario_domain":"domain:s","authority_refs":["authority:source"]}]
        b=Bound(pck,metadata.validate(f),data);self.assertEqual(nonanticipativity(b,p)[0]["status"],"FINITE_OBSERVED_TRUE")
        rows[3]["value"]=11
        b=Bound(pck,metadata.validate(f),data);self.assertEqual(nonanticipativity(b,p)[0]["status"],"FINITE_COUNTEREXAMPLE")
    def test_CL10_explicit_state_boundary_scope(self):
        from closure_v1.obligations import Bound,boundaries,evaluate
        d={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True}},"parameters":{"state":{"dims":["t"]},"start":{"dims":[]},"end":{"dims":[]}},"conditions":{"initial":"state == start","terminal":"state == end"}}
        c=fixture(d,quant={n:q("MWh","electricity") for n in ("state","start","end")},pred_axes={"initial":["t"],"terminal":["t"]})
        pck=pkg(d,c);f=ts();f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":[]}]
        data=dataset({"state":series([1,2,3]),"start":[{"key":[],"value":1}],"end":[{"key":[],"value":3}]})
        b=Bound(pck,metadata.validate(f),data)
        aa=[assertion(pck,"assertion:"+n,n,["domain:t"],["time"],at={"domain:t":[v]}) for n,v in (("initial",0),("terminal",2))]
        st=[{"id":"state:ledger","symbol":"ref:state","time_domain":"domain:t","mode":"NONCYCLIC","initial":"assertion:initial","terminal":"assertion:terminal","authority_refs":["authority:source"]}]
        self.assertEqual(boundaries(b,aa,st)[0]["status"],"BOUND_NATIVE_ASSERTIONS")
        self.assertEqual(evaluate(b,aa,[])["status"],"FINITE_OBSERVATIONS_ONLY")
        aa[1]["at"]["domain:t"]=[1]
        with self.assertRaisesRegex(Reject,"BOUNDARY_SCOPE_OR_SYMBOL"):boundaries(b,aa,st)

# Integrated graph fixtures. No CBA/IoSN-specific rule is in the validator.
from closure import digest,text_hash
from fractions import Fraction as F
from closure_v1 import graph,identity
from interface import resolve_method
from WS_B.methods import identities as old_identities
def source_row(i,ref,content):
    return {"id":i,"immutable_ref":ref,"revision":"1","content":content,"sha256":text_hash(content)}
def sig(id,qty,axes=None,**extra):return {"id":id,"quantity":qty,"axes":axes or [],"value_type":"REAL","authority_refs":["authority:source"],**extra}
def source_for_slot(f,source_rows,k):
    src=source_row("authority:"+k,"fixture:"+k,"synthetic method "+k)
    f["authorities"].append({"id":src["id"],"role":"SOURCE","immutable_ref":src["immutable_ref"],"revision":"1","decision_state":"OWNER_TBD"})
    source_rows.append(src);return src
def make_slot(f,src,k,d,c,data,bindings,inputs,obs,outputs,external_symbols,assertions=None,comparison_pairs=None,case_context=None,weight_roles=None,ledger=None,depends=None):
    c["method"]["id"]="method:"+k;c["study"]["method_ref"]=digest(c["method"])
    pck=pkg(d,c);r=resolve_method(pck,data);s=r["signature"]
    prof={"id":s["id"],"version":s["version"],"native_signature":r["method_signature_identity"],"native_semantic_identity":old_identities(pck)["semantic"],"source_ref":src["immutable_ref"],"source_sha256":src["sha256"],"approval":"RESEARCH_ASSUMPTION",
          "input_roles":{z["symbol_id"]:(weight_roles or {}).get(z["symbol_id"],"VALUE") for z in s["inputs"]},
          "axis_roles":{z["id"]:next(a["kind"] if a["kind"] in ("time","scenario") else "sample" for a in f["domains"] if a["id"]==z["id"]) for z in c["domains"].values()},
          "parameter_ranges":{},"probability_rules":{},"counterfactual_pairs":comparison_pairs or [],"outputs":[z["symbol_id"] for z in s["outputs"]]}
    if s["outputs"]:prof["output_contract"]={"external":external_symbols,"intermediate":[z["symbol_id"] for z in s["outputs"] if z["symbol_id"] not in external_symbols]}
    ctx=case_context or {"pairs":[]}
    st={"id":c["study"]["id"],"version":c["study"]["version"],"profile_identity":digest(prof),"native_study_identity":r["study_identity"],"data_context_identity":r["context_receipt"]["context_identity"],"case_context_identity":digest(ctx),"owner":"OWNER_TBD"}
    a=assertions or [];verify=[{"id":"verification:"+k+":"+str(i),"subject":v,"kind":"FINITE_OBSERVATION","oracle_ref":"authority:source","status":"NOT_EXECUTED"} for i,v in enumerate([*outputs,*[z["id"] for z in a if z["modality"]!="MAY"]])]
    f["slots"].append({"id":"slot:"+k,"inputs":inputs,"observables":obs,"outputs":outputs,"scope":"scope:main","authority_refs":[src["id"]]})
    f["processes"].append({"id":"process:"+k,"slot":"slot:"+k,"depends_on":depends or [],"authority_refs":[src["id"]]})
    return {"id":"slot:"+k,"package":pck,"profile":prof,"study":st,"source_ref":src["id"],"data":data,"case_context":ctx,"bindings":bindings,"assertions":a,"witnesses":[],"policies":[],"states":[],"comparisons":[],"verification":verify,"ledger":ledger}
def repin(x):
    for row in x["slots"]:
        p=row["profile"];r=resolve_method(row["package"],row["data"])
        row["study"].update(profile_identity=digest(p),native_study_identity=r["study_identity"],data_context_identity=r["context_receipt"]["context_identity"],case_context_identity=digest(row["case_context"]))
    x["trust"]=graph.pins(x);x["study"]["frame_ref"]=x["trust"]["frame"];x["study"]["slot_refs"]=x["trust"]["slots"]
    return digest(x["trust"])
def bundle(f,slots,src,events=None):
    x={"schema":graph.INPUT,"study":{"id":"study:research","version":"0.2","owner":"OWNER_TBD","frame_ref":"","slot_refs":{}},"frame":f,"slots":slots,"sources":src,"disclosures":[],"events":events or [],"context_data":{},"reports":[],"trust":{}}
    return x,repin(x)
def simple_graph(second="b+1",description=None):
    f=frame();src=[source_row("authority:source","fixture:source","synthetic independent oracle specification")]
    f["scopes"]=[{"id":"scope:main","domains":[],"subjects":[]}]
    f["inputs"]=[sig("input:a",q())]
    f["outputs"]=[sig("output:mid",q(),contribution_policy="NOT_REQUIRED"),sig("output:result",q(),contribution_policy="NOT_REQUIRED")]
    s1=source_for_slot(f,src,"first");s2=source_for_slot(f,src,"second")
    a={"version":0,"parameters":{"a":{"dims":[]}},"expressions":{"v":"a*2"}}
    if description is not None:a["parameters"]["a"]["description"]=description
    c=fixture(a,roles={"a":"INPUT"});p1=make_slot(f,s1,"first",a,c,dataset({"a":[{"key":[],"value":3}]}),{"ref:a":{"kind":"INPUT","ref":"input:a"},"ref:v":{"kind":"OUTPUT","ref":"output:mid"}},["input:a"],[],["output:mid"],["ref:v"])
    b={"version":0,"parameters":{"b":{"dims":[]}},"expressions":{"w":second}}
    c=fixture(b,roles={"b":"INPUT"});p2=make_slot(f,s2,"second",b,c,dataset({"b":[{"key":[],"value":6}]}),{"ref:b":{"kind":"UPSTREAM","ref":"output:mid"},"ref:w":{"kind":"OUTPUT","ref":"output:result"}},["output:mid"],[],["output:result"],["ref:w"],depends=["process:first"])
    return bundle(f,[p1,p2],src)
def ledger_graph(second="b*2",mode="DISJOINT"):
    f=frame();src=[source_row("authority:source","fixture:source","synthetic event catalogue")]
    f["domains"]=[{"id":"domain:t","kind":"time","members":[0,1],"ordered":True}]
    f["chronologies"]=[{"id":"chronology:t","domain":"domain:t","mode":"NONCYCLIC","authority_refs":["authority:source"],"intervals":[{"label":i,"start_h":i,"end_h":i+1,"duration_h":1} for i in range(2)]}]
    f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":["case:base"]}]
    money=q("EUR","currency","EUR:real:2025")
    f["referents"]=[{"id":"case:base","kind":"cost_series","quantity":money,"axes":["domain:t"],"authority_refs":["authority:source"]}]
    f["observables"]=[sig("observable:a",money,["domain:t"],subject="case:base",projection="IDENTITY")]
    f["outputs"]=[sig("output:subtotal",money,contribution_policy="REQUIRED"),sig("output:total",money,contribution_policy="REQUIRED")]
    events=[{"id":"event:"+str(i),"case":"case:base","event_key":"operating_cost","coordinate":{"domain:t":i},"source_ref":"authority:source"} for i in range(2)]
    ids=[e["id"] for e in events]
    led1={"bindings":{"a":{"role":"contribution","observable":"observable:a","case":"case:base","data_ref":""}},"key_axes":{"a":["domain:t"]},"contributions":[{"id":"contribution:"+str(i),"series":"a","key":[i],"case":"case:base","observable":"observable:a","event":e["id"]} for i,e in enumerate(events)],"policy":{"v":"DISJOINT"},"global_disjoint":["v"],"expected":{"v":ids}}
    s1=source_for_slot(f,src,"first");s2=source_for_slot(f,src,"second")
    a={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True}},"parameters":{"a":{"dims":["t"]}},"expressions":{"v":"sum(a, over=t)"}}
    c=fixture(a,quant={"a":money,"v":money},domains={"t":[0,1]})
    p1=make_slot(f,s1,"first",a,c,dataset({"a":series([2,4])}),{"ref:a":{"kind":"OBSERVABLE","ref":"observable:a"},"ref:v":{"kind":"OUTPUT","ref":"output:subtotal"}},[],["observable:a"],["output:subtotal"],["ref:v"],ledger=led1)
    b={"version":0,"parameters":{"b":{"dims":[]}},"expressions":{"w":second}}
    c=fixture(b,roles={"b":"INPUT"},quant={"b":money,"w":money})
    led2={"bindings":{"b":{"role":"auxiliary","observable":"","case":"","data_ref":"ref:b"}},"key_axes":{"b":[]},"contributions":[],"policy":{"w":mode},"global_disjoint":["w"] if mode=="DISJOINT" else [],"expected":{"w":ids}}
    p2=make_slot(f,s2,"second",b,c,dataset({"b":[{"key":[],"value":6}]}),{"ref:b":{"kind":"UPSTREAM","ref":"output:subtotal"},"ref:w":{"kind":"OUTPUT","ref":"output:total"}},["output:subtotal"],[],["output:total"],["ref:w"],ledger=led2,depends=["process:first"])
    return bundle(f,[p1,p2],src,events)
def counterfactual_graph():
    f=frame();src=[source_row("authority:source","fixture:source","synthetic paired comparison policy")]
    f["scopes"]=[{"id":"scope:main","domains":[],"subjects":["case:reference","case:alternative"]}]
    money=q("EUR","currency","EUR:real:2025")
    for n in ("reference","alternative"):
        f["referents"].append({"id":"case:"+n,"kind":"study_case","quantity":money,"axes":[],"authority_refs":["authority:source"]})
        f["observables"].append(sig("observable:"+n,money,subject="case:"+n,projection="IDENTITY"))
    f["relations"]=[{"id":"relation:pair","kind":"counterfactual_of","from":"case:alternative","to":"case:reference","authority_refs":["authority:source"]}]
    f["inputs"]=[sig("input:"+n,q()) for n in ("load_ref","load_alt","cap_ref","cap_alt")]
    f["outputs"]=[sig("output:delta",money,contribution_policy="NOT_REQUIRED")]
    f["comparisons"]=[{"id":"comparison:policy","relation":"relation:pair","exogenous":{"load":{"reference":"input:load_ref","alternative":"input:load_alt"}},"project":{"capacity":{"reference":"input:cap_ref","alternative":"input:cap_alt"}},"allowed_changes":["capacity"],"authority_refs":["authority:source"]}]
    s=source_for_slot(f,src,"pair")
    vals={"base":100,"alt":80,"load_ref":10,"load_alt":10,"cap_ref":2,"cap_alt":3}
    d={"version":0,"parameters":{n:{"dims":[]} for n in vals},"expressions":{"delta":"base-alt"}}
    c=fixture(d,roles={n:"INPUT" for n in ("load_ref","load_alt","cap_ref","cap_alt")},quant={n:money for n in ("base","alt","delta")})
    data=dataset({n:[{"key":[],"value":v}] for n,v in vals.items()})
    bind={"ref:"+n:{"kind":"INPUT","ref":"input:"+n} for n in ("load_ref","load_alt","cap_ref","cap_alt")}
    bind.update({"ref:base":{"kind":"OBSERVABLE","ref":"observable:reference"},"ref:alt":{"kind":"OBSERVABLE","ref":"observable:alternative"},"ref:delta":{"kind":"OUTPUT","ref":"output:delta"}})
    context={"pairs":[{"id":"pair:cost","reference_exogenous":{"load":digest([{"key":[],"value":"10"}])},"alternative_exogenous":{"load":digest([{"key":[],"value":"10"}])}}]}
    row=make_slot(f,s,"pair",d,c,data,bind,[x["id"] for x in f["inputs"]],["observable:reference","observable:alternative"],["output:delta"],["ref:delta"],comparison_pairs=[{"id":"pair:cost","reference":"ref:base","alternative":"ref:alt"}],case_context=context)
    row["comparisons"]=[{"id":"pair:cost","policy":"comparison:policy","source_ref":"authority:source"}]
    return bundle(f,[row],src)
class GraphControls(unittest.TestCase):
    def test_CL11_multi_method_graph(self):
        x,p=simple_graph();r=graph.evaluate(x,p)
        self.assertEqual(r["execution_order"],["slot:first","slot:second"])
        self.assertEqual(r["outputs"]["output:result"],[{"key":[],"value":"7"}])
        self.assertEqual(r["conformance"],"NOT_PROVED")
        t=graph.export(x,p);self.assertEqual(graph.reimport(t,p)["receipt"],r)
        print("C2_CLOSURE_GRAPH="+json.dumps(r,sort_keys=True))
    def test_CL12_graph_drift_and_dependency(self):
        x,p=simple_graph();bad=copy.deepcopy(x);bad["slots"][1]["data"]["parameters"]["b"][0]["value"]=7
        with self.assertRaisesRegex(Reject,"TRUST_CONTEXT_MISMATCH"):graph.evaluate(bad,p)
        with self.assertRaisesRegex(Reject,"UPSTREAM_RESULT_BINDING"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["frame"]["processes"][1]["depends_on"]=[]
        with self.assertRaisesRegex(Reject,"PROCESS_DEPENDENCY_BINDING"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["slots"][0]["bindings"]["ref:a"]={"kind":"UPSTREAM","ref":"output:result"};bad["frame"]["slots"][0]["inputs"]=["output:result"];bad["frame"]["inputs"]=[]
        bad["frame"]["processes"][0]["depends_on"]=["process:second"]
        with self.assertRaisesRegex(Reject,"METHOD_DEPENDENCY_CYCLE"):graph.evaluate(bad,repin(bad))
    def test_CL13_counterfactual_context(self):
        x,p=counterfactual_graph();r=graph.evaluate(x,p)
        self.assertEqual(r["outputs"]["output:delta"][0]["value"],"20")
        self.assertEqual(r["slots"]["slot:pair"]["comparisons"][0]["changed"],["capacity"])
        bad=copy.deepcopy(x);bad["frame"]["comparisons"][0]["allowed_changes"]=[]
        with self.assertRaisesRegex(Reject,"UNAUTHORIZED_PROJECT_CHANGE"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["slots"][0]["data"]["parameters"]["load_alt"][0]["value"]=11
        with self.assertRaisesRegex(Reject,"COUNTERFACTUAL_EXOGENEITY"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["slots"][0]["case_context"]["pairs"][0]["reference_exogenous"]={"load":"fake"}
        with self.assertRaisesRegex(Reject,"COUNTERFACTUAL_CONTEXT_CONTENT"):graph.evaluate(bad,repin(bad))
    def test_CL14_coordinate_ledger_and_cross_slot(self):
        x,p=ledger_graph();r=graph.evaluate(x,p)
        self.assertEqual(r["outputs"]["output:total"][0]["value"],"12")
        self.assertEqual(r["slots"]["slot:second"]["lineage"]["w"][0]["events"],{"event:0":1,"event:1":1})
        bad=copy.deepcopy(x);bad["slots"][0]["ledger"]["contributions"].pop()
        with self.assertRaisesRegex(Reject,"MISSING_CONTRIBUTION"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["events"][1]["coordinate"]={"domain:t":0}
        with self.assertRaisesRegex(Reject,"DUPLICATE_EVENT_IDENTITY"):graph.evaluate(bad,repin(bad))
        bad,p=ledger_graph("b+b")
        with self.assertRaisesRegex(Reject,"SEMANTIC_DOUBLE_COUNT"):graph.evaluate(bad,p)
        good,p=ledger_graph("b+b","ALLOW_REUSE");r=graph.evaluate(good,p)
        self.assertEqual(r["slots"]["slot:second"]["lineage"]["w"][0]["events"],{"event:0":2,"event:1":2})
        print("C2_CLOSURE_LEDGER="+json.dumps(r["slots"]["slot:second"]["lineage"],sort_keys=True))
    def test_CL15_semantic_and_audit_order(self):
        x,p=ledger_graph();a=graph.evaluate(x,p)
        y=copy.deepcopy(x);y["slots"].reverse();y["frame"]["outputs"].reverse();y["events"].reverse()
        first=next(r for r in y["slots"] if r["id"]=="slot:first");first["data"]["parameters"]["a"].reverse();first["ledger"]["contributions"].reverse()
        b=graph.evaluate(y,repin(y));self.assertEqual(a["semantic_identity"],b["semantic_identity"]);self.assertNotEqual(a["audit_identity"],b["audit_identity"])
        x,p=simple_graph();a=graph.evaluate(x,p)
        y,p=simple_graph(description="Only author documentation");b=graph.evaluate(y,p)
        self.assertEqual(a["semantic_identity"],b["semantic_identity"]);self.assertNotEqual(a["audit_identity"],b["audit_identity"])
        z,p=simple_graph(second="b+2");self.assertNotEqual(a["semantic_identity"],graph.evaluate(z,p)["semantic_identity"])
    def test_CL16_evidence_and_variation(self):
        x,p=ledger_graph();bad=copy.deepcopy(x);bad["slots"][1]["verification"][0]["status"]="PASS"
        with self.assertRaisesRegex(Reject,"VERIFICATION_COVERAGE_OR_PROMOTION"):graph.evaluate(bad,repin(bad))
        y=copy.deepcopy(x);y["frame"]["variations"]=[{"id":"variation:formulation","subject":"case:base","alternatives":["energy","soc"],"disclosure":True,"source_refs":["authority:source"]}]
        with self.assertRaisesRegex(Reject,"VARIATION_DISCLOSURE_COVERAGE"):graph.evaluate(y,repin(y))
        y["disclosures"]=[{"id":"disclosure:1","variation":"variation:formulation","choice":"soc","source_ref":"authority:source"}]
        y["slots"][1]["verification"][0]["kind"]="TOOL_CONFORMANCE";r=graph.evaluate(y,repin(y))
        self.assertEqual(r["slots"]["slot:second"]["verification"][0]["status"],"NOT_EXECUTED")
        self.assertEqual(r["owner"],"OWNER_TBD")
# Static definitions and separately pinned study instances.
from closure_v1 import definition
def to_definition(x):
    ds=[]
    for row in x["slots"]:
        d={k:copy.deepcopy(row[k]) for k in definition.STATIC_FIELDS}
        if d["ledger"] is not None:
            d["ledger"].pop("contributions");d["ledger"]["coverage"]=list(d["ledger"].pop("expected"))
        ds.append(d)
    f=copy.deepcopy(x["frame"]);subjects=[a["id"] for k in ("components","ports","referents") for a in f[k]]
    ext=[*f["inputs"],*f["context_fields"],*[z for z in f["observables"] if z["projection"]=="IDENTITY"]]
    req={"boundary":{"included":subjects,"environment":[],"space_domains":[],"functional_scopes":["scope:main"],"authority_refs":["authority:source"]},
         "data_contracts":[{"id":a["id"],"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","reproducibility":"PINNED_SNAPSHOT","quality":"TYPE_AND_COMPLETE_SUPPORT","quality_assertions":[],"missing":"BLOCK","conversion":None} for a in ext],
         "process_roles":{r["id"]:"EVALUATION" for r in f["processes"]},
         "normativity":{a["id"]:{"status":"RESEARCH_ASSUMPTION","authority_ref":a["authority_refs"][0]} for row in ds for a in row["assertions"]},
         "models":[],"comparisons":[],"time_policies":[{"id":a["id"],"resolution":"EXPLICIT_INTERVALS","interpolation":"NONE","aggregation":"NONE","rule_outputs":[],"authority_refs":["authority:source"]} for a in f["domains"] if a["kind"]=="time"]}
    d={"schema":definition.DEF,"study":{k:x["study"][k] for k in ("id","version","owner")},"frame":f,"slots":ds,"sources":copy.deepcopy(x["sources"]),"requirements":req}
    return d,digest(d)
def to_instance(x,d,dp):
    static=definition.admit(d,dp);rows=[]
    for r in x["slots"]:
        rows.append({"id":r["id"],"profile_ref":static["method_identities"][r["id"]],"package_ref":identity.mathematics(r["package"]),"data_status":"PRESENT","data":copy.deepcopy(r["data"]),"snapshot_digest":digest(r["data"]),"case_context":copy.deepcopy(r["case_context"]),"witnesses":copy.deepcopy(r["witnesses"]),"contributions":copy.deepcopy(r["ledger"]["contributions"]) if r["ledger"] else [],"expected_events":copy.deepcopy(r["ledger"]["expected"]) if r["ledger"] else {}})
    values=graph.evaluate(x,digest(x["trust"]))["data_bindings"]
    return {"schema":definition.INST,"definition_ref":static["semantic_identity"],"slots":rows,"events":copy.deepcopy(x["events"]),"disclosures":copy.deepcopy(x["disclosures"]),"context_data":copy.deepcopy(x["context_data"]),"reports":copy.deepcopy(x["reports"]),
            "data_receipts":[{"id":k,"snapshot_identity":v,"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","raw_rows":None} for k,v in values.items()]}
class DefinitionControls(unittest.TestCase):
    def test_CL17_static_no_data_and_instance_roundtrip(self):
        x,p=ledger_graph();d,dp=to_definition(x)
        s=definition.admit(d,dp);self.assertEqual(s["status"],"STATIC_VALID");self.assertEqual(s["data_status"],"NOT_EXECUTED")
        t=definition.export(d,dp);self.assertEqual(definition.reimport(t,dp)["receipt"],s)
        inst=to_instance(x,d,dp);ip=digest(inst);res=definition.instantiate(d,dp,inst,ip)
        self.assertEqual(res["graph"]["outputs"]["output:total"][0]["value"],"12")
        self.assertEqual(definition.reimport(definition.export(d,dp,inst,ip),dp,ip)["receipt"],res)
        inst["slots"][0].update(data_status="MISSING_DATA",data=None,snapshot_digest=None,witnesses=[],contributions=[],expected_events={})
        self.assertEqual(definition.instantiate(d,dp,inst,digest(inst))["status"],"BLOCKED")
        print("C2_CLOSURE_STATIC="+json.dumps(s,sort_keys=True))
    def test_CL18_method_identity_cross_study(self):
        from interface import import_package,resolve_method
        d,c=arithmetic();c=fixture(d,roles={"a":"INPUT","b":"INPUT"});p=pkg(d,c);data=dataset({"a":series([1,2,3]),"b":series([1,1,1])})
        r=resolve_method(p,data);s=r["signature"]
        pr={"id":s["id"],"version":s["version"],"native_signature":r["method_signature_identity"],"native_semantic_identity":old_identities(p)["semantic"],"source_ref":"fixture:method","source_sha256":text_hash("method"),"approval":"RESEARCH_ASSUMPTION","input_roles":{"ref:a":"VALUE","ref:b":"VALUE"},"axis_roles":{"domain:t":"time"},"parameter_ranges":{},"probability_rules":{},"counterfactual_pairs":[],"outputs":["ref:v"]}
        a=identity.method_identity(pr,p)
        c["study"]["id"]="study:other";c["study"]["version"]="2";c["domains"]["t"]["labels"]=[5,6];c["study"]["data_id"]="data:other"
        p2=pkg(d,c);pr2=copy.deepcopy(pr);pr2["native_semantic_identity"]=old_identities(p2)["semantic"]
        self.assertEqual(a,identity.method_identity(pr2,p2))
        self.assertNotEqual(identity.mathematics(p),identity.mathematics(p2))
    def test_CL19_data_policy_and_explicit_conversion(self):
        x,p=simple_graph();d,dp=to_definition(x);inst=to_instance(x,d,dp)
        bad=copy.deepcopy(d);bad["requirements"]["data_contracts"]=[]
        with self.assertRaisesRegex(Reject,"DATA_CONTRACT_COVERAGE"):definition.admit(bad,digest(bad))
        inst["data_receipts"][0]["license_ref"]="authority:other"
        with self.assertRaisesRegex(Reject,"DATA_PROVENANCE_PIN"):definition.instantiate(d,dp,inst,digest(inst))
        source={"authority:source":source_row("authority:source","fixture:source","exact unit rule")}
        cv={"kind":"UNIT","source_unit":"kW","source_basis":"NONE","factor":"1/1000","source_ref":"authority:source"}
        target=q("MW","electricity");definition.validate_conversion(cv,target,source)
        self.assertEqual(definition.converted_rows([{"key":[],"value":"2000"}],cv,target),[{"key":[],"value":"2"}])
        cv["factor"]="1"
        with self.assertRaisesRegex(Reject,"CONVERSION_FACTOR"):definition.validate_conversion(cv,target,source)
    def test_CL20_relation_support_binding(self):
        from closure_v1.obligations import Bound
        d,c,data=relation_fixture();p=pkg(d,c);f=frame()
        f["domains"]=[{"id":"domain:"+n,"kind":"sample","members":z["labels"],"ordered":False} for n,z in c["domains"].items()]
        f["authorities"][0]["immutable_ref"]="fixture:endpoint"
        f["relation_domains"]=[{"id":"relation:endpoint","roles":{"branch":"domain:branch","bus":"domain:bus"},"key":["branch"],"support":"CARTESIAN","rows":copy.deepcopy(data["relations"]["endpoint"]),"topology":None,"authority_refs":["authority:source"]}]
        Bound(p,metadata.validate(f),data)
        data["relations"]["endpoint"][0]["bus"]="b2"
        with self.assertRaisesRegex(Reject,"RELATION_SUPPORT_BINDING"):Bound(p,metadata.validate(f),data)
        # Sparse tuples represented by an explicit key-domain, not implicit missing rows.
        f["relation_domains"][0]["support"]="EXPLICIT_TUPLES"
        with self.assertRaisesRegex(Reject,"EXPLICIT_TUPLE_ALIAS"):metadata.validate(f)
    def test_CL21_configurable_probability_scope(self):
        from WS_B.methods import probability_policy
        self.assertEqual(probability_policy("SUM_ONE"),(1,1))
        self.assertEqual(probability_policy({"kind":"SUM_RANGE","min":"1/2","max":"1","scope":"DECLARED_SUBPROBABILITY"}),(F(1,2),F(1)))
        with self.assertRaisesRegex(Reject,"PROBABILITY_POLICY_RANGE"):probability_policy({"kind":"SUM_RANGE","min":"0","max":"6/5","scope":"DECLARED_SUBPROBABILITY"})
class FinalControls(unittest.TestCase):
    def test_CL22_cyclic_endpoint_equality(self):
        from closure_v1.obligations import Bound,boundaries,evaluate
        d={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True}},"parameters":{"state":{"dims":["t"]},"start":{"dims":[]},"end":{"dims":[]}},"conditions":{"initial":"state == start","terminal":"state == end","cycle":"start == end"}}
        c=fixture(d,pred_axes={"initial":["t"],"terminal":["t"],"cycle":[]})
        p=pkg(d,c);f=ts();f["chronologies"][0]["mode"]="CYCLIC";f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":[]}]
        t=metadata.validate(f)
        data=dataset({"state":series([1,2,1]),"start":[{"key":[],"value":1}],"end":[{"key":[],"value":1}]})
        b=Bound(p,t,data)
        a=[assertion(p,"assertion:"+n,n,["domain:t"],["time"],at={"domain:t":[v]}) for n,v in (("initial",0),("terminal",2))]
        a.append(assertion(p,"assertion:cycle","cycle",[],[]))
        st=[{"id":"state:ledger","symbol":"ref:state","time_domain":"domain:t","mode":"CYCLIC","initial":"assertion:initial","terminal":"assertion:terminal","cycle":{"assertion":"assertion:cycle","initial_value":"ref:start","terminal_value":"ref:end"},"authority_refs":["authority:source"]}]
        boundaries(b,a,st);self.assertEqual(evaluate(b,a,[])["status"],"FINITE_OBSERVATIONS_ONLY")
        bad=copy.deepcopy(st);bad[0]["terminal"]="assertion:initial"
        with self.assertRaisesRegex(Reject,"BOUNDARY_DISTINCT"):boundaries(b,a,bad)
        data["parameters"]["state"][-1]["value"]=3;data["parameters"]["end"][0]["value"]=3
        self.assertEqual(evaluate(Bound(p,t,data),a,[])["status"],"FINITE_COUNTEREXAMPLE")
    def test_CL23_model_comparison_native_metric(self):
        f=frame();src=[source_row("authority:source","fixture:source","synthetic comparison oracle")]
        f["domains"]=[{"id":"domain:s","kind":"scenario","members":["a","b"],"ordered":False}]
        f["scopes"]=[{"id":"scope:main","domains":["domain:s"],"subjects":["case:a","case:b"]}]
        for n in ("a","b"):
            f["referents"].append({"id":"case:"+n,"kind":"study_case","quantity":q(),"axes":["domain:s"],"authority_refs":["authority:source"]})
            f["observables"].append(sig("observable:"+n,q(),["domain:s"],subject="case:"+n,projection="IDENTITY"))
        f["outputs"]=[sig("output:delta",q(),["domain:s"],contribution_policy="NOT_REQUIRED")]
        src1=source_for_slot(f,src,"compare")
        d={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{"a":{"dims":["s"]},"b":{"dims":["s"]},"tol":{"dims":[]}},"expressions":{"delta":"a-b"},"conditions":{"ok":"delta <= tol and delta >= -tol"}}
        c=fixture(d,roles={"tol":"METHOD_PARAMETER"},domains={"s":["a","b"]},pred_axes={"ok":["s"]})
        a=assertion(pkg(d,c),"assertion:compare","ok",["domain:s"],["scenario"])
        data=dataset({"a":[{"key":["a"],"value":2},{"key":["b"],"value":3}],"b":[{"key":["a"],"value":2},{"key":["b"],"value":4}],"tol":[{"key":[],"value":1}]})
        bindings={"ref:a":{"kind":"OBSERVABLE","ref":"observable:a"},"ref:b":{"kind":"OBSERVABLE","ref":"observable:b"},"ref:tol":{"kind":"PARAMETER","ref":"ref:tol"},"ref:delta":{"kind":"OUTPUT","ref":"output:delta"}}
        row=make_slot(f,src1,"compare",d,c,data,bindings,[],["observable:a","observable:b"],["output:delta"],["ref:delta"],assertions=[a])
        row["profile"]["parameter_ranges"]={"ref:tol":{"min":"0","max":"2"}}
        x,p=bundle(f,[row],src)
        d,dp=to_definition(x)
        req=d["requirements"];req["models"]=[{"id":"model:"+n,"implementation_ref":"impl:"+n,"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","observables":["observable:"+n],"variations":[]} for n in ("a","b")]
        req["comparisons"]=[{"id":"comparison:models","models":["model:a","model:b"],"metric_outputs":["output:delta"],"decision_assertions":["assertion:compare"],"tolerances":[{"slot":"slot:compare","parameter":"ref:tol","metric_output":"output:delta"}],"sensitivity_domains":["domain:s"],"selection_policy":"ALL_ADMISSIBLE","equivalence_target":"E3","oracle_ref":"authority:source","authority_refs":["authority:source"]}]
        dp=digest(d);inst=to_instance(x,d,dp);res=definition.instantiate(d,dp,inst,digest(inst))
        self.assertEqual(res["comparison_evidence"][0]["status"],"FINITE_OBSERVATIONS_ONLY")
        self.assertEqual(res["graph"]["outputs"]["output:delta"],[{"key":["a"],"value":"0"},{"key":["b"],"value":"-1"}])
        self.assertEqual(res["conformance"],"NOT_PROVED")
        d["requirements"]["comparisons"][0]["equivalence_target"]="E4"
        dp=digest(d);inst=to_instance(x,d,dp);self.assertEqual(definition.instantiate(d,dp,inst,digest(inst))["comparison_evidence"][0]["status"],"NOT_PROVED")
        print("C2_CLOSURE_MODEL_COMPARISON="+json.dumps(res["comparison_evidence"],sort_keys=True))
class OriginalProjectionControls(unittest.TestCase):
    def test_CL24_original_p5_numeric_projection_and_external_context(self):
        # Original fixture bytes retained from its pinned Git blob. This is a
        # deliberately narrow semantic projection, not the original full A/B path.
        p5_text=(Path(__file__).parent/"p5_fixture.json").read_text();p5=json.loads(p5_text)
        f=frame();src=[source_row("authority:source","fixture:source",p5_text)]
        labels=[r["id"] for r in p5["scenarios"]]
        f["domains"]=[{"id":"domain:s","kind":"scenario","members":labels,"ordered":False}]
        f["scopes"]=[{"id":"scope:main","domains":["domain:s"],"subjects":[]}]
        money=q("EUR","currency","EUR:real:2025")
        f["inputs"]=[sig("input:probability",q(),["domain:s"])]
        models=[];slots=[];contexts={};raw={};events=[]
        for m in p5["models"]:
            mid=m["id"];key=mid.lower();cases={case:"case:"+key+":"+case for case in ("R","P")}
            for case,k in cases.items():
                f["referents"].append({"id":k,"kind":"study_case","model_id":"model:"+key,"quantity":money,"axes":["domain:s"],"authority_refs":["authority:source"]})
                f["observables"].append(sig("observable:"+key+":"+case,money,["domain:s"],subject=k,projection="IDENTITY"))
            f["scopes"][0]["subjects"]+=list(cases.values())
            rel="relation:"+key;f["relations"].append({"id":rel,"kind":"counterfactual_of","from":cases["P"],"to":cases["R"],"authority_refs":["authority:source"]})
            fields_={}
            samples={case:[next(x for x in p5["samples"] if x["model_id"]==mid and x["scenario_id"]==s and x["case_id"]==case) for s in labels] for case in ("R","P")}
            for field in ("exogenous_digest","weather_year"):
                pair={}
                for case,side in (("R","reference"),("P","alternative")):
                    name="context:"+key+":"+case+":"+field;pair[side]=name
                    f["context_fields"].append({"id":name,"axes":["domain:s"],"value_type":"TOKEN","allowed_values":[],"authority_refs":["authority:source"]})
                    contexts[name]=[{"key":[r["scenario_id"]],"value":r[field]} for r in samples[case]]
                fields_[field]=pair
            policy="comparison:"+key
            # Explicit project delta token is allowed to change; use a declared
            # token for absent asset rather than an invented numeric value.
            pr={}
            for case,side in (("R","reference"),("P","alternative")):
                name="context:"+key+":"+case+":project";pr[side]=name
                f["context_fields"].append({"id":name,"axes":["domain:s"],"value_type":"TOKEN","allowed_values":[],"authority_refs":["authority:source"]})
                contexts[name]=[{"key":[r["scenario_id"]],"value":r["project_delta_id"] or "NO_PROJECT_DELTA"} for r in samples[case]]
            f["comparisons"].append({"id":policy,"relation":rel,"exogenous":fields_,"project":{"project_delta":pr},"allowed_changes":["project_delta"],"authority_refs":["authority:source"]})
            out="output:"+key;f["outputs"].append(sig(out,money,contribution_policy="REQUIRED"))
            d={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{n:{"dims":["s"]} for n in ("base","alt","prob")},"expressions":{"benefit":"sum((base-alt)*prob, over=s)"}}
            c=fixture(d,roles={"prob":"INPUT"},quant={"base":money,"alt":money,"benefit":money},domains={"s":labels})
            # One stated study-year amount: actual original annual rate * 1 year.
            rows={case:[{"key":[r["scenario_id"]],"value":str(r["operating_cost_proxy_eur_per_year"])} for r in samples[case]] for case in ("R","P")}
            raw.update({"observable:"+key+":"+case:rr for case,rr in rows.items()})
            data=dataset({"base":copy.deepcopy(rows["R"]),"alt":copy.deepcopy(rows["P"]),"prob":[{"key":[r["id"]],"value":str(r["weight"])} for r in p5["scenarios"]]})
            pairid="pair:"+key
            ds={field:digest(sorted(contexts[pair["reference"]],key=lambda r:r["key"])) for field,pair in fields_.items()}
            ctx={"pairs":[{"id":pairid,"reference_exogenous":ds,"alternative_exogenous":ds}]}
            row=make_slot(f,source_for_slot(f,src,key),key,d,c,data,{"ref:base":{"kind":"OBSERVABLE","ref":"observable:"+key+":R"},"ref:alt":{"kind":"OBSERVABLE","ref":"observable:"+key+":P"},"ref:prob":{"kind":"INPUT","ref":"input:probability"},"ref:benefit":{"kind":"OUTPUT","ref":out}},["input:probability"],["observable:"+key+":R","observable:"+key+":P"],[out],["ref:benefit"],comparison_pairs=[{"id":pairid,"reference":"ref:base","alternative":"ref:alt"}],case_context=ctx,weight_roles={"ref:prob":"PROBABILITY"})
            row["profile"]["probability_rules"]={"ref:prob":"SUM_ONE"};row["comparisons"]=[{"id":pairid,"policy":policy,"source_ref":"authority:source"}]
            # Derived event catalogue: each original sample ID determines a
            # unique case/scenario contribution to the annual benefit.
            contributions=[];event_ids=[]
            for case,series_name in (("R","base"),("P","alt")):
                for r in samples[case]:
                    eid="event:"+r["id"];event_ids.append(eid)
                    events.append({"id":eid,"case":cases[case],"event_key":r["id"]+":operating_cost_proxy","coordinate":{"domain:s":r["scenario_id"]},"source_ref":"authority:source"})
                    contributions.append({"id":"contribution:"+r["id"],"series":series_name,"key":[r["scenario_id"]],"case":cases[case],"observable":"observable:"+key+":"+case,"event":eid})
            row["ledger"]={"bindings":{"base":{"role":"contribution","observable":"observable:"+key+":R","case":cases["R"],"data_ref":""},"alt":{"role":"contribution","observable":"observable:"+key+":P","case":cases["P"],"data_ref":""},"prob":{"role":"auxiliary","observable":"","case":"","data_ref":"ref:prob"}},"key_axes":{n:["domain:s"] for n in ("base","alt","prob")},"contributions":contributions,"policy":{"benefit":"DISJOINT"},"global_disjoint":["benefit"],"expected":{"benefit":event_ids}}
            slots.append(row)
            models.append({"id":"model:"+key,"implementation_ref":m["generator_identity"],"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","observables":["observable:"+key+":R","observable:"+key+":P"],"variations":[]})
        for r in p5["additional_indicators"]:
            k="report:"+r["id"];qual=r["unit"]=="qualitative"
            f["report_requests"].append({"id":k,"subject":f["id"],"value_type":"QUALITATIVE" if qual else "QUANTITY","declared_unit":None if qual else r["unit"],"basis":"ORIGINAL_P5_NOT_MONETIZED","oracle_ref":"authority:source","authority_refs":["authority:source"]})
        x,_=bundle(f,slots,src,events);x["context_data"]=contexts;x["reports"]=[{"id":r["id"],"status":"NOT_EXECUTED","reason":"ORIGINAL_P5_INDICATOR_NOT_EXECUTED","value":None,"source_ref":"authority:source"} for r in f["report_requests"]];repin(x)
        d,dp=to_definition(x);d["requirements"]["models"]=models
        for r in d["requirements"]["data_contracts"]:
            if r["id"] in raw:r["conversion"]={"kind":"ANNUAL_RATE_TO_PERIOD_AMOUNT","source_unit":"EUR/year","source_basis":"EUR:real:2025","period_years":"1","period_ref":"authority:source","source_ref":"authority:source"}
        dp=digest(d);inst=to_instance(x,d,dp)
        for r in inst["data_receipts"]:
            if r["id"] in raw:r["raw_rows"]=raw[r["id"]]
        res=definition.instantiate(d,dp,inst,digest(inst))
        self.assertEqual(res["graph"]["outputs"],{"output:m-a":[{"key":[],"value":"120"}],"output:m-b":[{"key":[],"value":"104"}]})
        self.assertEqual(res["status"],"BLOCKED");self.assertEqual(res["conformance"],"NOT_PROVED")
        self.assertEqual(len(res["graph"]["external_reports"]),2)
        for row in res["graph"]["slots"].values():
            self.assertEqual(len(row["lineage"]["benefit"][0]["events"]),4)
            self.assertTrue(all(v==1 for v in row["lineage"]["benefit"][0]["events"].values()))
        bad=copy.deepcopy(x);bad["slots"][0]["ledger"]["contributions"].pop()
        with self.assertRaisesRegex(Reject,"MISSING_CONTRIBUTION"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["context_data"]["context:m-a:P:weather_year"][0]["value"]="DRIFT"
        with self.assertRaisesRegex(Reject,"COUNTERFACTUAL_EXOGENEITY"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["frame"]["referents"][1]["model_id"]="model:m-b"
        with self.assertRaisesRegex(Reject,"CROSS_MODEL_PAIRING_FORBIDDEN"):graph.evaluate(bad,repin(bad))
        bad=copy.deepcopy(x);bad["reports"][0]["value"]=0
        with self.assertRaisesRegex(Reject,"REPORT_EVIDENCE_PROMOTION"):graph.evaluate(bad,repin(bad))
        print("C2_CLOSURE_P5_PROJECTION="+json.dumps({"outputs":res["graph"]["outputs"],"reports":res["graph"]["external_reports"],"lineage":{k:r["lineage"] for k,r in res["graph"]["slots"].items()},"status":res["status"],"full_path":False},sort_keys=True))
class CriticalControls(unittest.TestCase):
    def test_CL25_conflict_fail_closed(self):
        from closure_v1.obligations import Bound,evaluate
        d,c=arithmetic();p=pkg(d,c);f=ts();f["scopes"]=[{"id":"scope:main","domains":["domain:t"],"subjects":[]}]
        b=Bound(p,metadata.validate(f),dataset({"a":series([1,2,3]),"b":series([1,1,1])}))
        a=assertion(p,"assertion:safety","match",["domain:t"],["time"])
        neg=copy.deepcopy(a);neg.update(id="assertion:prohibition",role="PROHIBITED_BEHAVIOUR",modality="MUST_NOT")
        with self.assertRaisesRegex(Reject,"DIRECT_OBLIGATION_CONFLICT"):evaluate(b,[a,neg],[])
        neg["guard"]={"truth":"FALSE","reason":None}
        self.assertEqual(evaluate(b,[a,neg],[])["status"],"FINITE_OBSERVATIONS_ONLY")
    def test_CL26_native_finite_robustness_and_selector(self):
        # Unweighted variance and an explicit finite selected result. No
        # universal optimization or hidden selection implementation is used.
        d={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{"cost":{"dims":["s"]},"selected":{"dims":[]},"weight":{"dims":["s"]}},"expressions":{"mean":"sum(cost*weight, over=s)","variance":"sum((cost-mean)**2*weight, over=s)"},"conditions":{"selected_is_min":"selected <= cost"}}
        c=fixture(d,domains={"s":["a","b"]},pred_axes={"selected_is_min":["s"]})
        p=pkg(d,c);f=frame();f["domains"]=[{"id":"domain:s","kind":"sample","members":["a","b"],"ordered":False}];f["scopes"]=[{"id":"scope:main","domains":["domain:s"],"subjects":[]}]
        data=dataset({"cost":[{"key":["a"],"value":1},{"key":["b"],"value":3}],"selected":[{"key":[],"value":1}],"weight":[{"key":["a"],"value":"1/2"},{"key":["b"],"value":"1/2"}]})
        from closure_v1.obligations import Bound,evaluate
        b=Bound(p,metadata.validate(f),data)
        self.assertEqual(b.consumer.outputs(),{"mean":["2"],"variance":["1"]})
        a=assertion(p,"assertion:selection","selected_is_min",["domain:s"],["sample"])
        self.assertEqual(evaluate(b,[a],[])["status"],"FINITE_OBSERVATIONS_ONLY")
        data["parameters"]["selected"][0]["value"]=3
        self.assertEqual(evaluate(Bound(p,metadata.validate(f),data),[a],[])["status"],"FINITE_COUNTEREXAMPLE")
# Final closure: exact selector membership, controlled override, diagnostics.
from closure_v1 import selection,composition,diagnostics
from interface import import_package
from closure import source_map
def select_case():
    f=frame();src=[source_row("authority:source","fixture:source","synthetic selector and oracle")]
    f["domains"]=[{"id":"domain:s","kind":"sample","members":["a","b"],"ordered":False}]
    f["scopes"]=[{"id":"scope:main","domains":["domain:s"],"subjects":["case:a","case:b"]}]
    for n in ("a","b"):
        f["referents"].append({"id":"case:"+n,"kind":"study_case","quantity":q(),"axes":["domain:s"],"authority_refs":["authority:source"]})
        f["observables"].append(sig("observable:"+n,q(),["domain:s"],subject="case:"+n,projection="IDENTITY"))
    f["inputs"]=[sig("input:selected",q())]
    f["outputs"]=[sig("output:delta",q(),["domain:s"],contribution_policy="NOT_REQUIRED")]
    s=source_for_slot(f,src,"select")
    d={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{"a":{"dims":["s"]},"b":{"dims":["s"]},"selected":{"dims":[]}},"expressions":{"delta":"a-b"},"conditions":{"lower":"selected <= delta","member":"selected == delta"}}
    c=fixture(d,roles={"selected":"INPUT"},domains={"s":["a","b"]},pred_axes={"lower":["s"],"member":["s"]})
    p=pkg(d,c);low=assertion(p,"assertion:lower","lower",["domain:s"],["sample"])
    mem=assertion(p,"assertion:member","member",["domain:s"],["sample"],role="CONDITIONAL_OBLIGATION");mem["binders"][0]["quantifier"]="EXISTS"
    data=dataset({"a":[{"key":["a"],"value":2},{"key":["b"],"value":4}],"b":[{"key":["a"],"value":1},{"key":["b"],"value":1}],"selected":[{"key":[],"value":1}]})
    row=make_slot(f,s,"select",d,c,data,{"ref:a":{"kind":"OBSERVABLE","ref":"observable:a"},"ref:b":{"kind":"OBSERVABLE","ref":"observable:b"},"ref:selected":{"kind":"INPUT","ref":"input:selected"},"ref:delta":{"kind":"OUTPUT","ref":"output:delta"}},["input:selected"],["observable:a","observable:b"],["output:delta"],["ref:delta"],assertions=[low,mem])
    x,p=bundle(f,[row],src)
    de,dp=to_definition(x);de["requirements"]["models"]=[{"id":"model:"+n,"implementation_ref":"impl:"+n,"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","observables":["observable:"+n],"variations":[]} for n in ("a","b")]
    de["requirements"]["comparisons"]=[{"id":"comparison:selector","models":["model:a","model:b"],"metric_outputs":["output:delta"],"decision_assertions":["assertion:lower","assertion:member"],"tolerances":[],"sensitivity_domains":["domain:s"],"selection_policy":"DECLARED_NATIVE_SELECTOR","equivalence_target":"E3","oracle_ref":"authority:source","authority_refs":["authority:source"]}]
    return x,de,digest(de)
def replacement(row,expression,protected_condition=False):
    old=import_package(row["package"]);doc=source_map(old["native_canonical"]);c=copy.deepcopy(old["context"])
    doc["expressions"]["w"]=expression
    c["method"]["version"]="0.3";c["study"]["method_ref"]=digest(c["method"])
    p=pkg(doc,c);new=copy.deepcopy(row);new["package"]=p
    new["profile"].update(version="0.3",native_signature=import_package(p)["interface"]["method_identity"],native_semantic_identity=old_identities(p)["semantic"])
    return new
def authorize(d,old,new,allowed=None):
    bp=digest(d);r={"schema":composition.VERSION,"base_ref":bp,"overrides":[{"id":"override:second","slot":old["id"],"expected_old":digest(old),"replacement":new,"allowed_expressions":allowed or ["w"]}]}
    rp=digest(r);a={"schema":composition.APPROVAL,"base_ref":bp,"request_ref":rp,"decision_scope":"NON_NORMATIVE_RESEARCH_ONLY","approvals":[{"id":"override:second","slot":old["id"],"old_ref":digest(old),"new_ref":digest(new),"allowed_expressions":allowed or ["w"],"authority_ref":old["source_ref"],"source_sha256":old["profile"]["source_sha256"],"decision":"APPROVED_RESEARCH_OVERRIDE","reason":"synthetic research-only method choice"}]}
    return r,rp,a,digest(a)
class FinalClosure(unittest.TestCase):
    def test_CL27_selection_membership_and_order(self):
        x,d,dp=select_case();static=definition.admit(d,dp)
        self.assertEqual(static["status"],"STATIC_VALID")
        def run(v,tie=False):
            y=copy.deepcopy(x);row=y["slots"][0];row["data"]["parameters"]["selected"][0]["value"]=v
            if tie:row["data"]["parameters"]["a"][1]["value"]=2
            repin(y);i=to_instance(y,d,dp);return definition.instantiate(d,dp,i,digest(i))
        a=run(1);self.assertEqual(a["status"],"FINITE_OBSERVATIONS_ONLY")
        self.assertEqual(run(1,True)["status"],"FINITE_OBSERVATIONS_ONLY")
        below=run(0);above=run(3)
        for z in (below,above):self.assertEqual(z["status"],"FINITE_COUNTEREXAMPLE");self.assertEqual(z["comparison_evidence"][0]["status"],"NOT_PROVED")
        b={r["id"]:r["truth"] for r in below["graph"]["slots"]["slot:select"]["obligations"]["assertions"]}
        self.assertEqual(b,{"assertion:lower":"TRUE","assertion:member":"FALSE"})
        bad=copy.deepcopy(d);bad["requirements"]["comparisons"][0]["decision_assertions"]=["assertion:lower"]
        with self.assertRaisesRegex(Reject,"SELECTOR_MEMBERSHIP_AND_ORDER_REQUIRED"):definition.admit(bad,digest(bad))
        bad=copy.deepcopy(d);bad["slots"][0]["assertions"][1]["binders"][0]["quantifier"]="FORALL"
        with self.assertRaisesRegex(Reject,"SELECTOR_MEMBERSHIP_AND_ORDER_REQUIRED"):definition.admit(bad,digest(bad))
        print("C2_FINAL_SELECTOR="+json.dumps({"valid":a["status"],"below":below["status"],"above":above["status"],"below_truth":b,"owner":a["owner"]},sort_keys=True))
    def test_CL28_authorized_composition_and_roundtrip(self):
        x,p=simple_graph();d,dp=to_definition(x);old=d["slots"][1];new=replacement(old,"b+2")
        r,rp,a,ap=authorize(d,old,new)
        out=composition.compose(d,dp,r,rp,a,ap)
        self.assertEqual(out["owner"],"OWNER_TBD");self.assertEqual(out["conformance"],"NOT_PROVED")
        self.assertNotEqual(out["base_semantic_identity"],out["effective_receipt"]["semantic_identity"])
        self.assertEqual(out["effective_definition"]["frame"],d["frame"])
        self.assertEqual(out["effective_definition"]["sources"],d["sources"])
        self.assertEqual(out["effective_definition"]["slots"][0],d["slots"][0])
        t=composition.export(d,dp,r,rp,a,ap);self.assertEqual(composition.reimport(t,dp,rp,ap)["receipt"],out)
        y=copy.deepcopy(x);y["slots"][1].update(package=new["package"],profile=new["profile"]);repin(y)
        effective=out["effective_definition"];ep=out["effective_pin"];i=to_instance(y,effective,ep)
        got=definition.instantiate(effective,ep,i,digest(i));self.assertEqual(got["graph"]["outputs"]["output:result"][0]["value"],"8")
        original=to_instance(x,d,dp)
        with self.assertRaisesRegex(Reject,"INSTANCE_PIN"):definition.instantiate(effective,ep,original,digest(original))
        print("C2_FINAL_OVERRIDE="+json.dumps({"before":"7","after":"8","overrides":out["overrides"],"owner":out["owner"],"base":out["base_semantic_identity"],"effective":out["effective_receipt"]["semantic_identity"]},sort_keys=True))
    def test_CL29_override_rejection(self):
        x,p=simple_graph();d,dp=to_definition(x);old=d["slots"][1];new=replacement(old,"b+2")
        r,rp,a,ap=authorize(d,old,new)
        with self.assertRaisesRegex(Reject,"OVERRIDE_AUTHORIZATION_PIN"):composition.compose(d,dp,r,rp,a,"wrong")
        bad=copy.deepcopy(a);bad["approvals"][0]["decision"]="PROPOSED"
        with self.assertRaisesRegex(Reject,"OVERRIDE_NOT_AUTHORIZED"):composition.compose(d,dp,r,rp,bad,digest(bad))
        bad=copy.deepcopy(a);bad["decision_scope"]="NORMATIVE_APPROVAL"
        with self.assertRaisesRegex(Reject,"OVERRIDE_AUTHORITY_PROMOTION"):composition.compose(d,dp,r,rp,bad,digest(bad))
        bad=copy.deepcopy(r);bad["overrides"][0]["expected_old"]="wrong";a2=copy.deepcopy(a);a2["request_ref"]=digest(bad)
        with self.assertRaisesRegex(Reject,"OVERRIDE_STALE_BASE"):composition.compose(d,dp,bad,digest(bad),a2,digest(a2))
        bad=copy.deepcopy(new);bad["verification"]=[]
        r2,rp2,a2,ap2=authorize(d,old,bad)
        with self.assertRaisesRegex(Reject,"OVERRIDE_PROTECTED_FIELD"):composition.compose(d,dp,r2,rp2,a2,ap2)
        r2,rp2,a2,ap2=authorize(d,old,new,["unrelated"])
        with self.assertRaisesRegex(Reject,"OVERRIDE_EXPRESSION_SCOPE"):composition.compose(d,dp,r2,rp2,a2,ap2)
        r2=copy.deepcopy(r);a2=copy.deepcopy(a);r2["overrides"].append({**r2["overrides"][0],"id":"override:duplicate"});a2["approvals"].append({**a2["approvals"][0],"id":"override:duplicate"});a2["request_ref"]=digest(r2)
        with self.assertRaisesRegex(Reject,"OVERRIDE_DUPLICATE_OR_UNKNOWN_TARGET"):composition.compose(d,dp,r2,digest(r2),a2,digest(a2))
    def test_CL30_protect_transitive_native_obligation(self):
        x,p=simple_graph();d,dp=to_definition(x);old=d["slots"][1]
        a=import_package(old["package"]);doc=source_map(a["native_canonical"]);c=copy.deepcopy(a["context"])
        doc["conditions"]={"required":"w <= b+1"}
        c["predicates"]["required"]={"id":"pred:required","role":"PREDICATE","axes":[]}
        pk=pkg(doc,c);old["package"]=pk;old["profile"].update(native_signature=import_package(pk)["interface"]["method_identity"],native_semantic_identity=old_identities(pk)["semantic"])
        old["assertions"]=[assertion(pk,"assertion:protected","required",[],[])]
        old["verification"].append({"id":"verification:protected","subject":"assertion:protected","kind":"FINITE_OBSERVATION","oracle_ref":"authority:source","status":"NOT_EXECUTED"})
        d["requirements"]["normativity"]["assertion:protected"]={"status":"RESEARCH_ASSUMPTION","authority_ref":"authority:source"};dp=digest(d)
        definition.admit(d,dp)
        new=replacement(old,"b+2")
        r,rp,a,ap=authorize(d,old,new)
        with self.assertRaisesRegex(Reject,"OVERRIDE_PROTECTED_NATIVE_OBLIGATION"):composition.compose(d,dp,r,rp,a,ap)
    def test_CL31_structured_diagnostic_boundary(self):
        x,d,dp=select_case()
        bad=copy.deepcopy(d);bad["slots"][0]["profile"]["source_sha256"]="wrong"
        rec=diagnostics.candidate_receipt(definition.admit,bad,digest(bad));self.assertEqual(rec["status"],"REJECTED")
        e=rec["diagnostics"][0]
        self.assertEqual(e["code"],"METHOD_SOURCE");self.assertEqual(e["path"],"/slots/0/profile");self.assertEqual(e["subject"],"slot:select")
        self.assertEqual(e["rule_id"],"R09");self.assertIn("authority:select",e["source_refs"]);self.assertEqual(e["source_pins"][0]["sha256"],d["slots"][0]["profile"]["source_sha256"]);self.assertEqual(e["rule_source"]["blob"],"7e9f506183bdce7a7c76e08fb7a2f316649088b7")
        bad=copy.deepcopy(d);bad["requirements"]["comparisons"][0]["decision_assertions"]=["assertion:lower"]
        rec2=diagnostics.candidate_receipt(definition.admit,bad,digest(bad));e2=rec2["diagnostics"][0]
        self.assertEqual(e2["rule_id"],"R12");self.assertEqual(e2["path"],"/requirements")
        self.assertEqual(e2["code"],"SELECTOR_MEMBERSHIP_AND_ORDER_REQUIRED")
        self.assertEqual(diagnostics.pointer("a/b","~x",1),"/a~1b/~0x/1")
        print("C2_FINAL_DIAGNOSTICS="+json.dumps([e,e2],sort_keys=True))
    def test_CL32_diagnostic_internal_failure_not_rejection(self):
        def bug():raise KeyError("internal implementation error")
        r=diagnostics.candidate_receipt(diagnostics.call,"/slots/0","R00","slot:select",(),bug)
        self.assertEqual(r["status"],"BLOCKED_INTERNAL")
        self.assertEqual(r["diagnostics"][0]["code"],"VALIDATION_EXCEPTION")
        self.assertEqual(r["diagnostics"][0]["path_kind"],"VALIDATION_OBJECT")
        self.assertEqual(r["diagnostics"][0]["source_pins"],[])
    def test_CL33_disjoint_override_precedence(self):
        x,p=simple_graph();d,dp=to_definition(x);first,second=d["slots"]
        # Two explicitly disjoint override requests. Their sequence cannot
        # alter the effective definition; exact request audit retains order.
        old=import_package(first["package"]);doc=source_map(old["native_canonical"]);c=copy.deepcopy(old["context"])
        doc["expressions"]["v"]="a*3";c["method"]["version"]="0.3";c["study"]["method_ref"]=digest(c["method"])
        pk=pkg(doc,c);n1=copy.deepcopy(first);n1["package"]=pk;n1["profile"].update(version="0.3",native_signature=import_package(pk)["interface"]["method_identity"],native_semantic_identity=old_identities(pk)["semantic"])
        n2=replacement(second,"b+2")
        r,rp,a,ap=authorize(d,second,n2);rr,_,aa,_=authorize(d,first,n1,["v"])
        r["overrides"].append({**rr["overrides"][0],"id":"override:first"});a["approvals"].append({**aa["approvals"][0],"id":"override:first"});a["request_ref"]=digest(r)
        z=composition.compose(d,dp,r,digest(r),a,digest(a))
        r2=copy.deepcopy(r);a2=copy.deepcopy(a);r2["overrides"].reverse();a2["approvals"].reverse();a2["request_ref"]=digest(r2)
        zz=composition.compose(d,dp,r2,digest(r2),a2,digest(a2))
        self.assertEqual(z["effective_pin"],zz["effective_pin"]);self.assertNotEqual(z["audit_identity"],zz["audit_identity"])
        y=copy.deepcopy(x);y["slots"][0].update(package=n1["package"],profile=n1["profile"]);y["slots"][1].update(package=n2["package"],profile=n2["profile"]);y["slots"][1]["data"]["parameters"]["b"][0]["value"]=9;repin(y)
        effective=z["effective_definition"];ep=z["effective_pin"];i=to_instance(y,effective,ep)
        self.assertEqual(definition.instantiate(effective,ep,i,digest(i))["graph"]["outputs"]["output:result"][0]["value"],"11")
if __name__=="__main__":unittest.main(verbosity=2)
