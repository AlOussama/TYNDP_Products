"""Synthetic C5 CBA-oriented reference, not the original P5 oracle or full SEW."""
from copy import deepcopy
from vmodel import DEF,INST,admit,targets
from research_assembly import (frame,source_row,sig,source_for_slot,make_slot,bundle,
    repin,to_definition,to_instance,assertion,fixture,q,dataset,digest)
from closure_v1 import definition
from interface import finite_consumer

SCENARIOS=["s1","s2"]
SOURCE="authority:source"
SCOPE="scope:main"
TEST="test:compare"
REVIEW="test:validate"
SYSTEM="requirement:pair"
STUDY="requirement:benefit"
METRIC="metric:benefit"

def row(v):return [{"key":[s],"value":x} for s,x in zip(SCENARIOS,v,strict=True)]
def requirement(id,level,statement,parents,targets,metrics,required=True):
    return {"id":id,"version":"1","level":level,"statement":statement,"source_ref":SOURCE,
            "source_kind":"RESEARCH_REQUIREMENT","authority_ref":SOURCE,"scope":SCOPE,"required":required,
            "parents":parents,"targets":targets,"metric_refs":metrics}
def metric(id,role,meaning,target):
    return {"id":id,"version":"1","role":role,"meaning":meaning,"target":target,"source_ref":SOURCE}
def test(id,kind,requirements,metric,criterion,method):
    return {"id":id,"version":"1","kind":kind,"objective":"Evaluate "+criterion,"requirements":requirements,
            "metric":metric,"criterion":criterion,"scope":SCOPE,"oracle_ref":SOURCE,"method":method,
            "coverage":"ALL_DECLARED_SUPPORT" if kind=="VERIFICATION" else "EXTERNAL_SCOPE",
            "evidence":"COMPUTED_NATIVE_RECEIPT" if kind=="VERIFICATION" else "EXTERNAL_REVIEW_RECEIPT"}

def build(numeric=False,guard=None,condition="benefit == expected",quant_expected=None,expected=None,formula="base-alt",method_version="0.2",costs=None,implementation="fixture:external_model"):
    f=frame();f["question"]="Synthetic paired project/reference cost comparison; no CBA compliance claim."
    source=[source_row(SOURCE,"fixture:source","Synthetic research requirement: identical exogenous inputs; only explicit project asset change; benefit reference cost minus project cost; scientific review pending.")]
    f["domains"]=[{"id":"domain:s","kind":"scenario","members":SCENARIOS,"ordered":False}]
    f["scopes"]=[{"id":SCOPE,"domains":["domain:s"],"subjects":["case:R","case:P"]}]
    money=q("EUR","currency","EUR:real:2025")
    for case in ("R","P"):
        f["referents"].append({"id":"case:"+case,"kind":"study_case","quantity":money,"axes":["domain:s"],"authority_refs":[SOURCE],"model_id":"model:synthetic"})
        f["observables"].append(sig("observable:"+case,money,["domain:s"],subject="case:"+case,projection="IDENTITY"))
    f["relations"]=[{"id":"relation:pair","kind":"counterfactual_of","from":"case:P","to":"case:R","authority_refs":[SOURCE]}]
    ctxt={};exog={};projects={}
    for field,values in {
        "weather":["weather-2012","weather-2013"],
        "demand":["demand-A","demand-B"],
        "price_basis":["EUR:real:2025","EUR:real:2025"],
        "asset":["existing","existing"],
        "network":["network-A","network-A"]}.items():
        pair={}
        for case,side in (("R","reference"),("P","alternative")):
            key="context:"+case+":"+field;pair[side]=key
            f["context_fields"].append({"id":key,"axes":["domain:s"],"value_type":"TOKEN","allowed_values":[],"authority_refs":[SOURCE]})
            ctxt[key]=row(values)
        (exog if field in ("weather","demand","price_basis") else projects)[field]=pair
    f["comparisons"]=[{"id":"comparison:pair","relation":"relation:pair","exogenous":exog,"project":projects,"allowed_changes":["asset"],"authority_refs":[SOURCE]}]
    f["outputs"]=[sig("output:benefit",money,["domain:s"],contribution_policy="NOT_REQUIRED")]
    f["report_requests"]=[{"id":"report:scientific_review","subject":f["id"],"value_type":"QUALITATIVE","declared_unit":None,"basis":"SYNTHETIC_RESEARCH_ONLY","oracle_ref":SOURCE,"authority_refs":[SOURCE]}]
    doc={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{n:{"dims":["s"]} for n in ("base","alt")},"expressions":{"benefit":formula}}
    costs=costs or ([100,130],[85,110])
    params={"base":row(costs[0]),"alt":row(costs[1])}
    quant={"base":money,"alt":money,"benefit":money};roles={};inputs=[]
    binds={"ref:base":{"kind":"OBSERVABLE","ref":"observable:R"},"ref:alt":{"kind":"OBSERVABLE","ref":"observable:P"},"ref:benefit":{"kind":"OUTPUT","ref":"output:benefit"}}
    if numeric:
        doc["parameters"]["expected"]={"dims":["s"]}
        doc["conditions"]={"within":condition}
        quant["expected"]=quant_expected or money
        roles["expected"]="INPUT";params["expected"]=row(expected if expected is not None else [15,20])
        f["inputs"]=[sig("input:expected",quant["expected"],["domain:s"])]
        inputs=["input:expected"];binds["ref:expected"]={"kind":"INPUT","ref":"input:expected"}
    c=fixture(doc,quant=quant,roles=roles,domains={"s":SCENARIOS},pred_axes={"within":["s"]} if numeric else {})
    c["method"]["version"]=method_version
    c["study"]["method_ref"]=digest(c["method"])
    hashes={field:digest(ctxt[pair["reference"]]) for field,pair in exog.items()}
    slot=make_slot(f,source_for_slot(f,source,"benefit"),"benefit",doc,c,dataset(params),binds,
        inputs,["observable:R","observable:P"],["output:benefit"],["ref:benefit"],
        comparison_pairs=[{"id":"pair:benefit","reference":"ref:base","alternative":"ref:alt"}],
        case_context={"pairs":[{"id":"pair:benefit","reference_exogenous":hashes,"alternative_exogenous":hashes}]})
    slot["comparisons"]=[{"id":"pair:benefit","policy":"comparison:pair","source_ref":SOURCE}]
    if numeric:
        a=assertion(slot["package"],"assertion:benchmark","within",["domain:s"],["scenario"],guard=guard)
        slot["assertions"]=[a]
        slot["verification"].append({"id":"verification:benchmark","subject":a["id"],"kind":"FINITE_OBSERVATION","oracle_ref":SOURCE,"status":"NOT_EXECUTED"})
    x,_=bundle(f,[slot],source);x["context_data"]=ctxt
    x["reports"]=[{"id":"report:scientific_review","status":"NOT_EXECUTED","reason":"NO_INDEPENDENT_REVIEW","value":None,"source_ref":SOURCE}]
    repin(x)
    b,bp=to_definition(x)
    b["requirements"]["models"]=[{"id":"model:synthetic","implementation_ref":implementation,"source_ref":SOURCE,"license_ref":SOURCE,"access_ref":SOURCE,"observables":["observable:R","observable:P"],"variations":[]}]
    bp=digest(b);bi=to_instance(x,b,bp)
    d={"schema":DEF,"base":b,
       "requirements":[requirement(STUDY,"STUDY","Benefit must arise from a methodologically consistent pair.",[],["report:scientific_review"],[METRIC,"metric:review"]),
                       requirement(SYSTEM,"SYSTEM","All prescribed exogenous fields equal; only allowed project change.",[STUDY],["comparison:pair"],["metric:exogeneity"])],
       "metrics":[metric(METRIC,"STUDY","Simplified benefit per scenario; not full CBA SEW","output:benefit"),
                  metric("metric:exogeneity","VERIFICATION","Boolean native counterfactual criterion","comparison:pair"),
                  metric("metric:review","VALIDATION","Scientific suitability review","report:scientific_review")],
       "tests":[test(TEST,"VERIFICATION",[SYSTEM],"metric:exogeneity","comparison:pair","NATIVE_COMPARISON"),
                test(REVIEW,"VALIDATION",[STUDY],"metric:review","report:scientific_review","EXTERNAL_REVIEW")]}
    if numeric:
        d["requirements"].append(requirement("requirement:benchmark","SYSTEM","Synthetic analytical benchmark only.",[STUDY],["assertion:benchmark"],["metric:benchmark"]))
        d["metrics"].append(metric("metric:benchmark","VERIFICATION","Benchmark output subject to native typed condition","output:benefit"))
        d["tests"].append(test("test:benchmark","VERIFICATION",["requirement:benchmark"],"metric:benchmark","assertion:benchmark","NATIVE_ASSERTION"))
    dp=digest(d);s=admit(d,dp)
    i={"schema":INST,"definition_ref":s["semantic_identity"],"base":bi,
       "requested_tests":[t["id"] for t in d["tests"]],"run_id":"synthetic-run-1","claims":[]}
    return d,i

def rebind(d,i):
    # Test fixture only. Never substitutes for caller-pinned external trust.
    i["definition_ref"]=admit(d,digest(d))["semantic_identity"]
    return d,i

def change_context(d,i,key,values):
    i["base"]["context_data"][key]=row(values)
    for r in i["base"]["data_receipts"]:
        if r["id"]==key:r["snapshot_identity"]=digest(i["base"]["context_data"][key])
    field=key.split(":")[-1]
    if field in ("weather","demand","price_basis"):
        side="reference" if ":R:" in key else "alternative"
        i["base"]["slots"][0]["case_context"]["pairs"][0][side+"_exogenous"][field]=digest(i["base"]["context_data"][key])

def claim(d,i,verdict,identity="claim:one",version="1"):
    return {"id":identity,"version":"1","test":TEST,"test_version":version,"definition_pin":digest(d),
            "base_instance_pin":digest(i["base"]),"verdict":verdict,"source_ref":SOURCE}

def variant(name):
    d,i=build();i["run_id"]="synthetic-"+name
    if name=="weather":change_context(d,i,"context:P:weather",["weather-2015","weather-2013"])
    elif name=="demand":change_context(d,i,"context:P:demand",["demand-unauthorized","demand-B"])
    elif name=="missing_scenario":i["base"]["context_data"]["context:P:weather"].pop()
    elif name=="allowed_project":change_context(d,i,"context:P:asset",["new-asset","new-asset"])
    elif name=="extra_network":change_context(d,i,"context:P:network",["network-B","network-B"])
    elif name=="price_basis":change_context(d,i,"context:P:price_basis",["EUR:real:2020","EUR:real:2025"])
    elif name=="missing_evidence":i["requested_tests"].remove(TEST);i["claims"].append(claim(d,i,"PASS"))
    elif name=="math_correct_invalid":change_context(d,i,"context:P:demand",["other-demand","demand-B"])
    elif name!="consistent":raise ValueError(name)
    return d,i

def math_only(d,i):
    return finite_consumer(d["base"]["slots"][0]["package"],i["base"]["slots"][0]["data"]).outputs()["benefit"]
