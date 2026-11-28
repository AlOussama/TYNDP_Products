"""Research assembly utilities extracted from pinned C1/C2 controls.
Synthetic defaults retained; not a production authoring API or a new mathematics layer.
"""
import copy,json,sys
from pathlib import Path
C2=Path(__file__).resolve().parents[1]/"BUNDLE_ML_04A_MS1_C2"
sys.path.insert(0,str(C2))
from interface import resolve_method
from closure import digest,text_hash,admit
from package_interface import export_package
from closure_v1 import metadata,graph,identity,definition
from WS_B.methods import identities as old_identities

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

def dataset(p,r=None):
    return {"id":"data:research","version":"0.2","parameters":p,"relations":r or {}}

def scalar(x):return [{"key":[],"value":x}]

def pkg(d,c):return export_package(admit(json.dumps(d),c))

def auth():return {"id":"authority:source","role":"SOURCE","immutable_ref":"fixture:source","revision":"1","decision_state":"OWNER_TBD"}

def frame():
    f={"schema":"c2-study-frame-0.1","id":"frame:test","version":"1","question":"Finite synthetic research"}
    f.update({k:[] for k in metadata.COLLECTIONS});f["authorities"]=[auth()]
    return f

def assertion(package,id,name,axes,kinds,role="SAFETY_GUARANTEE",guard=None,at=None,assumptions=None):
    from interface import predicate_client
    pr=predicate_client(package,"pred:"+name,"DATA_ASSUMPTION" if role=="DATA_ASSUMPTION" else "PREDICATE")
    return {"id":id,"role":role,"modality":"MUST","predicate":{"predicate_id":pr["predicate_id"],"role":pr["role"],"axes":pr["qualified_axes"],"scope_id":pr["scope_id"]},"scope":"scope:main","binders":[{"axis":a,"kind":k,"quantifier":"EXISTS" if k=="response" and role in ("SERVICE_GUARANTEE","CAPABILITY_GUARANTEE") else "FORALL"} for a,k in zip(axes,kinds,strict=True)],"at":at or {},"guard":guard or {"truth":"TRUE","reason":None},"assumptions":assumptions or [],"authority_refs":["authority:source"]}

def source_row(i,ref,content):
    return {"id":i,"immutable_ref":ref,"revision":"1","content":content,"sha256":text_hash(content)}

def sig(id,qty,axes=None,**extra):return {"id":id,"quantity":qty,"axes":axes or [],"value_type":"REAL","authority_refs":["authority:source"],**extra}

def source_for_slot(f,source_rows,k):
    src=source_row("authority:"+k,"fixture:"+k,"synthetic method "+k)
    f["authorities"].append({"id":src["id"],"role":"SOURCE","immutable_ref":src["immutable_ref"],"revision":"1","decision_state":"OWNER_TBD"})
    source_rows.append(src);return src

def make_slot(f,src,k,d,c,data,bindings,inputs,obs,outputs,external_symbols,assertions=None,comparison_pairs=None,case_context=None,weight_roles=None,ledger=None,depends=None,package_builder=None):
    c["method"]["id"]="method:"+k;c["study"]["method_ref"]=digest(c["method"])
    pck=(package_builder or pkg)(d,c);r=resolve_method(pck,data);s=r["signature"]
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
