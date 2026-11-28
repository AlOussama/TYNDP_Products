"""Compile authored C3 source into the existing native M3 Definition/Instance.
No oracle import, expected verdict, secondary mathematics AST or solver.
"""
import json,copy,sys
from itertools import product
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
C2=ROOT/"BUNDLE_ML_04A_MS1_C2"
sys.path.insert(0,str(C2));import interface
sys.path.insert(0,str(C2/"closure_v1"))
from test_closure_v1 import frame,source_row,sig,assertion,fixture,q,dataset,digest,old_identities
from closure import admit,Reject,need,text_hash
from package_interface import export_package
from closure_v1 import definition,metadata,obligations,graph,identity,diagnostics
from record_contract import structural,at,CandidateReject

REPO=ROOT.parents[2]
AUTH=["authority:source"]
def auth(row):
    return {**copy.deepcopy(row),"authority_refs":list(AUTH)}
def rows(dims,domains,values):
    keys=list(product(*(domains[a]["labels"] for a in dims)))
    vals=values if dims else [values]
    need(type(vals) is list and len(vals)==len(keys),"AUTHORED_DATA_SUPPORT")
    return [{"key":list(k),"value":v} for k,v in zip(keys,vals,strict=True)]
def values_norm(v):
    if type(v) is list:return [values_norm(x) for x in v]
    if v is None or type(v) is bool:return v
    try:return str(Fraction(v))
    except (ValueError,TypeError,ZeroDivisionError):return v
def source_binding(d,i):
    # Independent of the oracle: declared source paths must actually bind
    # the authored data, including explicit source-specific coordinate maps.
    r=i["record"];rc=d["reference"];p=d["parameters"];actual=i["parameters"]
    if rc=="RC02":
        s=r["synthetic_data"];v=s["domains"]["vehicle"];t=s["domains"]["interval"]
        x=s["inputs"];o=s["observed"]
        raw=[o["delivered"][j][k] for k in range(len(t)) for j in range(len(v))]
        need(values_norm(i["raw_transfers"]["delivered"])==values_norm(raw),"SOURCE_DATA_BINDING:delivered")
        need(values_norm(i["raw_transfers"]["required"])==values_norm(x["required"]),"SOURCE_DATA_BINDING:required")
        need(actual["connected"]==[int(x["connected"][j][k]) for k in range(len(t)) for j in range(len(v))],"SOURCE_DATA_BINDING:connected")
        need(actual["eligible"]==[int(x["connected"][j][k] and k<x["departure"][j]) for k in range(len(t)) for j in range(len(v))],"SOURCE_DATA_BINDING:eligible")
    if rc=="RC07":
        s=r["synthetic_data"];x=s["observed"]["decision"]
        need(values_norm(actual["decision"])==values_norm([x[k][j] for j in range(len(s["domains"]["scenario"])) for k in range(len(s["domains"]["stage"]))]),"SOURCE_DATA_BINDING:decision")
    if rc=="RC05":
        s=r["synthetic_data"];bs=s["domains"]["bus"];ls=s["domains"]["branch"]
        for n,side in (("sending",0),("receiving",1)):
            need(i["relation_rows"][n]==[{"branch":b,"bus":bs[s["inputs"]["orientation"][j][side]]} for j,b in enumerate(ls)],"SOURCE_RELATION_BINDING")
    for n,z in p.items():
        path=z.get("source_path")
        if path is None or (rc=="RC02" and n in ("delivered","required","connected","eligible")) or (rc=="RC07" and n=="decision"):continue
        raw=at(r,path)
        if n in i["raw_transfers"]:
            raw_values=i["raw_transfers"][n];want=raw if type(raw) is list else [raw]
            need(values_norm(raw_values)==values_norm(want),"SOURCE_RAW_DATA_BINDING:"+n);continue
        if type(raw) is bool:raw=int(raw)
        if z["dims"] and type(raw) is not list:raw=[raw]
        need(values_norm(actual[n])==values_norm(raw),"SOURCE_DATA_BINDING:"+n)
    if d["ledgers"]:
        need(i["observed_contributions"]==[r["synthetic_data"]["observed"]["contributions"]],"SOURCE_CONTRIBUTION_BINDING")
    if d["comparison"] is not None:
        x=r["synthetic_data"]["inputs"];c=i["comparison"]
        need(c["reference_context"]==x["reference_snapshot"] and c["alternative_context"]==x["project_snapshot"] and c["project_delta"]==x["project_delta"],"SOURCE_CONTEXT_BINDING")

def compile_rc(x,raw_original):
    d,i=x["definition"],x["instance"];rec=i["record"];source=d["original_source"]
    structural_receipts=structural(rec,d["checks"])
    source_binding(d,i)
    # Native mathematical authoring data are read from this actual source,
    # never from a case-ID branch or expected-result catalogue.
    dims=d["domains"];params=d["parameters"];expr=d["expressions"];conditions=d["conditions"]
    doc={"version":0,"dimensions":{n:{"dtype":"int" if type(z["labels"][0]) is int else "str","ordered":z["ordered"]} for n,z in dims.items()},
         "parameters":{n:{"dims":z["dims"],"dtype":z["dtype"]} for n,z in params.items()},
         "expressions":{n:z["formula"] for n,z in expr.items()},"conditions":{n:z["formula"] for n,z in conditions.items()}}
    if d["native_relations"]:doc["relations"]=d["native_relations"]
    original_text=raw_original.decode("utf-8")
    orig=source_row("authority:source","git:"+source["blob"],original_text)
    method_text=json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(",",":"))
    method=source_row("authority:method","candidate-method:"+digest(d),method_text)
    src=[orig,method]
    f=frame();f["id"]="frame:research";f["question"]=d["question"]
    f["authorities"]=[{"id":s["id"],"role":"SOURCE","immutable_ref":s["immutable_ref"],"revision":s["revision"],"decision_state":"OWNER_TBD"} for s in src]
    f["domains"]=[{"id":"domain:"+n,"kind":z["kind"],"members":z["labels"],"ordered":z["ordered"]} for n,z in dims.items()]
    for k in ("components","ports","relations","chronologies","relation_domains","report_requests"):
        f[k]=[auth(v) for v in d[k]]
    for v in f["report_requests"]:v["oracle_ref"]="authority:source"
    f["information_sets"]=copy.deepcopy(d["information_sets"])
    conversions={n:{"id":"conversion:"+n,"version":"1","source_ref":orig["immutable_ref"],"source_sha256":orig["sha256"],"authority":"RESEARCH_ASSUMPTION"} for n,z in params.items() if z["role"]=="METHOD_PARAMETER" and z["quantity"]["carrier"]=="conversion"}
    ctx=fixture(doc,quant={n:z["quantity"] for n,z in {**params,**expr}.items()},roles={n:z["role"] for n,z in params.items()},
                domain_rules={n:z["domain_rule"] for n,z in params.items()},domains={n:z["labels"] for n,z in dims.items()},
                pred_axes={n:z["axes"] for n,z in conditions.items()},conversions=conversions)
    # Predicate axes use canonical lexical scope order; service binder order remains separately authored.
    ctx["scope"]["binders"]=sorted(dims)
    ctx["study"]["id"]=d["study_id"]
    ctx["method"]["id"]="method:"+d["reference"]
    ctx["study"]["method_ref"]=digest(ctx["method"])
    ctx["audit"]["source_ref"]=method["immutable_ref"]
    for z in ctx["relations"].values():z["source_ref"]=orig["immutable_ref"]
    package=diagnostics.call("/definition/native","R00",d["study_id"],src,
                            lambda:export_package(admit(json.dumps(doc,sort_keys=True),ctx)))
    leaf=interface.import_package(package)
    s=leaf["interface"]["method_signature"]
    syms={z["native_name"]:z for z in leaf["interface"]["symbols"].values()}
    input_refs=[];obs_refs=[];output_refs=[];bindings={};model_decls=[]
    model_by_observable={z["observable"]:z for z in i["models"]}
    for n,z in params.items():
        sg=syms[n];ax=sg["domain_ids"];qty=z["quantity"];vt=graph.value_type(sg)
        r=z["role"]
        if r=="INPUT":
            ref="input:"+n;f["inputs"].append(sig(ref,qty,ax,value_type=vt));input_refs.append(ref)
            bindings[sg["symbol_id"]]={"kind":"INPUT","ref":ref}
        elif r in ("OBSERVABLE","EXTERNAL_WITNESS"):
            ref="observable:"+n;subject=z.get("subject","referent:"+n)
            existing={v["id"] for v in f["ports"]+f["referents"]}
            if subject not in existing:
                row={"id":subject,"kind":"study_case" if subject.startswith("case:") else "external_quantity","quantity":qty,"axes":ax,"authority_refs":list(AUTH)}
                if n in model_by_observable:row["model_id"]=model_by_observable[n]["id"]
                f["referents"].append(row)
            f["observables"].append(sig(ref,qty,ax,value_type=vt,subject=subject,projection="IDENTITY"));obs_refs.append(ref)
            bindings[sg["symbol_id"]]={"kind":"OBSERVABLE","ref":ref}
        elif r=="METHOD_PARAMETER":bindings[sg["symbol_id"]]={"kind":"PARAMETER","ref":sg["symbol_id"]}
        else:raise RuntimeError("Unknown authored role "+r)
    for n,z in expr.items():
        sg=syms[n];ref="output:"+n
        f["outputs"].append(sig(ref,z["quantity"],sg["domain_ids"],value_type=graph.value_type(sg),
                          contribution_policy="REQUIRED" if any(l["output"]==n for l in d["ledgers"]) else "NOT_REQUIRED"))
        output_refs.append(ref);bindings[sg["symbol_id"]]={"kind":"OUTPUT","ref":ref}
    # Model-source ledger keeps distinct declared source identities, while
    # explicitly not claiming independently authenticated real implementations.
    for model in i["models"]:
        n=model["observable"];k=model["id"]
        sr=source_row("authority:"+k,"git:"+source["blob"]+"#"+model["source_ref"],original_text)
        src.append(sr);f["authorities"].append({"id":sr["id"],"role":"SOURCE","immutable_ref":sr["immutable_ref"],"revision":"1","decision_state":"OWNER_TBD"})
        model_decls.append({"id":k,"implementation_ref":model["implementation_ref"],"source_ref":sr["id"],"license_ref":sr["id"],"access_ref":sr["id"],"observables":["observable:"+n],"variations":[]})
    # Explicit declared alternatives, not a proof of either real implementation.
    disclosures=[]
    subject=(f["ports"]+f["referents"])[0]["id"] if f["ports"]+f["referents"] else None
    if subject and len(d["variants"])>=2:
        alternatives=[z["id"] for z in d["variants"]]
        f["variations"]=[{"id":"variation:reference","subject":subject,"alternatives":alternatives,"disclosure":True,"source_refs":list(AUTH)}]
        disclosures=[{"id":"disclosure:reference","variation":"variation:reference","choice":alternatives[0],"source_ref":"authority:source"}]
    case_ctx={"pairs":[]};context_data={};pairs=[];comparison_bindings=[]
    if d["comparison"] is not None:
        c=i["comparison"];ref=c["reference"];alt=c["alternative"]
        ra=params[ref]["subject"];aa=params[alt]["subject"]
        f["relations"].append(auth({"id":"relation:pair","kind":"counterfactual_of","from":aa,"to":ra}))
        for name,val in (("ref",c["reference_context"]),("alt",c["alternative_context"]),("project_ref","NO_PROJECT_DELTA"),("project_alt",c["project_delta"])):
            k="context:"+name;f["context_fields"].append(auth({"id":k,"axes":[],"value_type":"TOKEN","allowed_values":[]}))
            context_data[k]=[{"key":[],"value":val}]
        f["comparisons"].append(auth({"id":"comparison:pair","relation":"relation:pair",
            "exogenous":{"snapshot":{"reference":"context:ref","alternative":"context:alt"}},
            "project":{"project_delta":{"reference":"context:project_ref","alternative":"context:project_alt"}},"allowed_changes":["project_delta"]}))
        pairs=[{"id":"pair:cost","reference":"ref:"+ref,"alternative":"ref:"+alt}]
        case_ctx={"pairs":[{"id":"pair:cost","reference_exogenous":{"snapshot":digest(context_data["context:ref"])},"alternative_exogenous":{"snapshot":digest(context_data["context:alt"])}}]}
        comparison_bindings=[{"id":"pair:cost","policy":"comparison:pair","source_ref":"authority:source"}]
    subjects=[r["id"] for k in ("components","ports","referents") for r in f[k]]
    f["scopes"]=[{"id":"scope:main","domains":[v["id"] for v in f["domains"]],"subjects":subjects}]
    f["slots"]=[{"id":"slot:main","inputs":input_refs,"observables":obs_refs,"outputs":output_refs,"scope":"scope:main","authority_refs":["authority:method"]}]
    f["processes"]=[{"id":"process:main","slot":"slot:main","depends_on":[],"authority_refs":["authority:method"]}]
    profile={"id":s["id"],"version":s["version"],"native_signature":leaf["interface"]["method_identity"],
             "native_semantic_identity":old_identities(package)["semantic"],"source_ref":method["immutable_ref"],"source_sha256":method["sha256"],
             "approval":"RESEARCH_ASSUMPTION","input_roles":{z["symbol_id"]:params[z["native_name"]].get("weight_role","VALUE") for z in s["inputs"]},
             "axis_roles":{"domain:"+n:z["kind"] if z["kind"] in ("time","scenario") else "sample" for n,z in dims.items()},
             "parameter_ranges":{z["symbol_id"]:params[z["native_name"]]["range"] for z in s["parameters"]},
             "probability_rules":{z["symbol_id"]:"SUM_ONE" for z in s["inputs"] if params[z["native_name"]].get("weight_role")=="PROBABILITY"},
             "counterfactual_pairs":pairs,"outputs":[z["symbol_id"] for z in s["outputs"]]}
    if s["outputs"]:profile["output_contract"]={"external":profile["outputs"],"intermediate":[]}
    assertions=[]
    for n,z in conditions.items():
        order=z.get("binder_order",z["axes"])
        a=assertion(package,"assertion:"+n,n,["domain:"+v for v in order],[dims[v]["kind"] for v in order],z["role"])
        assertions.append(a)
    policies=[auth(z) for z in d["policies"]]
    verify=[{"id":"verification:"+str(j),"subject":v,"kind":"FINITE_OBSERVATION","oracle_ref":"authority:source","status":"NOT_EXECUTED"} for j,v in enumerate(output_refs+[a["id"] for a in assertions]+[a["id"] for a in policies])]
    ledger_def=None;contrib=[];events=[];expected={}
    if d["ledgers"]:
        need(len(d["ledgers"])==1,"LEDGER_PROFILE")
        l=d["ledgers"][0];series=l["series"];event_by_id={}
        for n,z in series.items():
            subject=next(v["subject"] for v in f["observables"] if v["id"]=="observable:"+n)
            for e,key in zip(z["events"],z["keys"],strict=True):
                eid="event:"+e;events.append({"id":eid,"case":subject,"event_key":e,"coordinate":dict(zip(syms[n]["domain_ids"],key,strict=True)),"source_ref":"authority:source"})
                event_by_id[e]={"series":n,"key":key,"case":subject,"observable":"observable:"+n,"event":eid}
        for j,e in enumerate(i["observed_contributions"][0]):
            need(e in event_by_id,"CONTRIBUTION_SOURCE_REFERENCE")
            contrib.append({"id":"contribution:"+str(j),**event_by_id[e]})
        expected={l["output"]:["event:"+v for v in l["event_catalog"]]}
        ledger_def={"bindings":{n:({"role":"contribution","observable":"observable:"+n,"case":next(v["subject"] for v in f["observables"] if v["id"]=="observable:"+n),"data_ref":""} if n in series else {"role":"auxiliary","observable":"","case":"","data_ref":"ref:"+n}) for n,z in params.items() if z["role"]!="METHOD_PARAMETER"},
                    "key_axes":{n:syms[n]["domain_ids"] for n,z in params.items() if z["role"]!="METHOD_PARAMETER"},
                    "policy":{n:"DISJOINT" for n in expr},"global_disjoint":[l["output"]],"coverage":[l["output"]]}
    row={"id":"slot:main","package":package,"profile":profile,"source_ref":"authority:method","bindings":bindings,"assertions":assertions,
         "policies":policies,"states":[],"comparisons":comparison_bindings,"verification":verify,"ledger":ledger_def}
    all_data=f["inputs"]+f["observables"]+f["context_fields"]
    contracts=[{"id":a["id"],"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","reproducibility":"PINNED_SNAPSHOT",
                "quality":"TYPE_AND_COMPLETE_SUPPORT","quality_assertions":[],"missing":"BLOCK","conversion":None} for a in all_data]
    for n,cv in d["transfers"].items():
        ref=bindings[syms[n]["symbol_id"]]["ref"]
        next(a for a in contracts if a["id"]==ref)["conversion"]={**cv,"source_ref":"authority:source"}
    requirement={"boundary":{"included":subjects,"environment":[],"space_domains":[v["id"] for v in f["domains"] if v["kind"]=="space"],
                    "functional_scopes":["scope:main"],"authority_refs":list(AUTH)},"data_contracts":contracts,"process_roles":{"process:main":d["metadata"]["process_role"]},
                "normativity":{a["id"]:{"status":d["metadata"]["normativity"],"authority_ref":"authority:source"} for a in assertions},
                "models":model_decls,"comparisons":[],"time_policies":[{"id":v["id"],"resolution":"EXPLICIT_INTERVALS","interpolation":"NONE","aggregation":"NONE","rule_outputs":[],"authority_refs":list(AUTH)} for v in f["domains"] if v["kind"]=="time"]}
    if model_decls:
        requirement["comparisons"]=[{"id":"comparison:models","models":[m["id"] for m in model_decls],"metric_outputs":["output:delta"],
            "decision_assertions":["assertion:agreement"],"tolerances":[],"sensitivity_domains":[],"selection_policy":"ALL_ADMISSIBLE","equivalence_target":"E4","oracle_ref":"authority:source","authority_refs":list(AUTH)}]
    native_d={"schema":definition.DEF,"study":{"id":d["study_id"],"version":ctx["study"]["version"],"owner":"OWNER_TBD"},"frame":f,"slots":[row],"sources":src,"requirements":requirement}
    dp=digest(native_d);static=definition.admit(native_d,dp)
    data=dataset({n:rows(z["dims"],dims,i["parameters"][n]) for n,z in params.items()},i["relation_rows"])
    # Actual typed data admission before constructing externally rooted
    # receipts. A failure here is the original candidate binding diagnostic.
    try:bound=obligations.Bound(package,metadata.validate(f),data)
    except Reject as e:
        raise CandidateReject(str(e).split(":")[0],["instance","parameters"],"R00" if str(e).startswith("INTEGER_DOMAIN") else "R11",str(e),"NATIVE_DATA_BINDING",str(e)) from e
    witnesses=[]
    for n,z in conditions.items():
        for j,v in enumerate(z.get("witnesses",[])):
            witnesses.append({"id":"witness:"+n+":"+str(j),"assertion":"assertion:"+n,"key":v["key"],"response":v["response"],"source_ref":"authority:source","data_identity":bound.data_identity})
    raw_by_ref={bindings[syms[n]["symbol_id"]]["ref"]:rows(params[n]["dims"],dims,v) for n,v in i["raw_transfers"].items()}
    # Raw rows are exact, canonical coordinate order; physical conversion
    # verified independently by the unchanged native graph + C3 sign seam.
    for k,rr in raw_by_ref.items():
        for v in rr:v["value"]=str(Fraction(v["value"]))
    data_bindings={bindings[z["symbol_id"]]["ref"]:digest(graph.values(bound,z["symbol_id"])) for n,z in syms.items() if n in params and params[n]["role"] in ("INPUT","OBSERVABLE","EXTERNAL_WITNESS")}
    data_bindings.update({k:digest(v) for k,v in context_data.items()})
    receipts=[{"id":k,"snapshot_identity":v,"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","raw_rows":raw_by_ref.get(k)} for k,v in sorted(data_bindings.items())]
    inst={"schema":definition.INST,"definition_ref":static["semantic_identity"],"slots":[{"id":"slot:main","profile_ref":static["method_identities"]["slot:main"],"package_ref":identity.mathematics(package),"data_status":"PRESENT","data":data,"snapshot_digest":digest(data),"case_context":case_ctx,"witnesses":witnesses,"contributions":contrib,"expected_events":expected}],"events":events,"disclosures":disclosures,"data_receipts":receipts,"context_data":context_data,"reports":i["external_reports"]}
    ip=digest(inst)
    result=definition.instantiate(native_d,dp,inst,ip)
    canonical=definition.export(native_d,dp,inst,ip)
    if definition.reimport(canonical,dp,ip)["receipt"]!=result:raise RuntimeError("Native canonical receipt drift")
    return {"status":result["status"],"semantic_identity":static["semantic_identity"],"graph_semantic_identity":result["graph"]["semantic_identity"],
            "graph_audit_identity":result["graph"]["audit_identity"],"package_sha256":sha256(canonical.encode()).hexdigest(),"definition_pin":dp,"instance_pin":ip,
            "outputs":result["graph"]["outputs"],"obligations":result["graph"]["slots"]["slot:main"]["obligations"],"policies":result["graph"]["slots"]["slot:main"]["policies"],
            "lineage":result["graph"]["slots"]["slot:main"]["lineage"],"comparison_evidence":result["comparison_evidence"],"external_reports":result["graph"]["external_reports"],
            "structural_checks":structural_receipts,"lowered_normativity":native_d["requirements"]["normativity"],"native_identity":leaf["native_identity"],"native_package_sha256":sha256(package.encode()).hexdigest(),"roundtrip":True,
            "conformance":"NOT_PROVED","owner":"OWNER_TBD"}
