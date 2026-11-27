"""Bounded native profile binding. Existing legacy engine is a reference, not an authority."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT.parent/"BUNDLE_ML_04A_MS1_C1"/"comparative_canonical"))
from interface import resolve_method,import_package,package_version,finite_consumer,V1
from closure import need,fields,digest,native,source_map,semantic_context,text_hash
from closure import c1
from legacy_comparison import map_predicates
from profile_engine import rational
from WS_B.native_ledger import check as check_ledger

def identities(package):
    leaf=import_package(package)
    doc=source_map(leaf["native_canonical"])
    doc.pop("description",None)  # allowlisted ONLY top-level field
    spec=native(json.dumps(doc))
    sem=digest({"projection":"c2-top-description-0.1","canonical":spec.to_yaml(canonical=True),
                "binding":semantic_context(spec,leaf["context"]),"upstream":leaf["upstream"]})
    return {"native":leaf["native_identity"],"semantic":sem,"original_source":leaf["origin"]["sha256"],"audit":leaf["audit_identity"]}

def migrate_with_audit(case,package):
    need(package_version(package)==V1,'LEGACY_POWER_PACKAGE_UNSUPPORTED')
    leaf=import_package(package)
    need(native(json.dumps(case["doc"])).to_yaml(canonical=True)==leaf["native_canonical"] and case["context"]==leaf["context"],"MIGRATION_SOURCE_MISMATCH")
    target=map_predicates(case,native(leaf["native_canonical"]).program)
    audit={"original_source":leaf["source"],"original_source_sha256":text_hash(leaf["source"]),"original_context":leaf["context"],
           "native_audit":leaf["audit_identity"],"legacy_audit":target["audit_digest"]}
    return {"target":target,"migration_audit":audit,"migration_audit_identity":digest(audit),"scope":"BOUNDED_LEGACY_MAPPING_NOT_FULL_EQUIVALENCE"}

def validate(package,data,profile,study,source,context):
    leaf=import_package(package)
    receipt=resolve_method(package,data)
    signature=receipt["signature"]
    optional=tuple(k for k in ("ledger","output_contract") if k in profile)
    fields(profile,("id","version","native_signature","native_semantic_identity","source_ref","source_sha256","approval","input_roles","axis_roles","parameter_ranges","probability_rules","counterfactual_pairs","outputs")+optional,"PROFILE_FIELDS")
    fields(study,("id","version","profile_identity","native_study_identity","data_context_identity","case_context_identity","owner"),"STUDY_FIELDS")
    need(type(source) is str and profile["source_sha256"]==text_hash(source) and type(profile["source_ref"]) is str and bool(profile["source_ref"]),"METHOD_SOURCE")
    need(profile["approval"]=="RESEARCH_ASSUMPTION" and study["owner"]=="OWNER_TBD","AUTHORITY_PROMOTION")
    need(profile["id"]==signature["id"] and profile["version"]==signature["version"] and profile["native_signature"]==receipt["method_signature_identity"],"METHOD_SIGNATURE")
    need(profile["native_semantic_identity"]==identities(package)["semantic"],"METHOD_MATHEMATICAL_IDENTITY")
    need(study["id"]==leaf["context"]["study"]["id"] and study["version"]==leaf["context"]["study"]["version"],"STUDY_ID")
    need(study["profile_identity"]==digest(profile) and study["native_study_identity"]==receipt["study_identity"],"STUDY_METHOD_BINDING")
    need(study["data_context_identity"]==receipt["context_receipt"]["context_identity"] and study["case_context_identity"]==digest(context),"STUDY_DATA_CONTEXT")
    ins={z["symbol_id"]:z for z in signature["inputs"]};params={z["symbol_id"]:z for z in signature["parameters"]};outs={z["symbol_id"]:z for z in signature["outputs"]}
    need(type(profile["outputs"]) is list and len(set(profile["outputs"]))==len(profile["outputs"]) and set(profile["outputs"])==set(outs),"OUTPUT_COVERAGE")
    roles=profile["input_roles"];axis_roles=profile["axis_roles"]
    need(type(roles) is dict and set(roles)==set(ins) and all(v in ("VALUE","PROBABILITY","TIME_WEIGHT","DURATION_WEIGHT") for v in roles.values()),"INPUT_ROLE_COVERAGE")
    need(type(axis_roles) is dict and set(axis_roles)=={z["id"] for z in leaf["context"]["domains"].values()} and all(v in ("scenario","time","sample") for v in axis_roles.values()),"AXIS_ROLE_COVERAGE")
    rules=profile["probability_rules"];need(type(rules) is dict and set(rules)=={k for k,v in roles.items() if v=="PROBABILITY"},"PROBABILITY_POLICY_COVERAGE")
    for k,role in roles.items():
        if role=="VALUE":continue
        z=ins[k];axes=z["domain_ids"];q=z["quantity"]
        need(len(axes)==1 and axis_roles[axes[0]]==("scenario" if role=="PROBABILITY" else "time") and q["unit"]==("h" if role=="DURATION_WEIGHT" else "1") and q["carrier"]=="none" and q["basis"]=="NONE","WEIGHT_ROLE")
        values=[rational(row["value"]) for row in data["parameters"][z["native_name"]]]
        if role=="PROBABILITY":
            need(rules[k]=="SUM_ONE","UNSUPPORTED_PROBABILITY_POLICY")
            need(all(v>=0 for v in values) and sum(values)==1,"PROBABILITY_NORMALIZATION")
        else:need(all(v>0 for v in values),"TIME_WEIGHT")
    ranges=profile["parameter_ranges"]
    need(type(ranges) is dict and set(ranges)==set(params),"PARAMETER_RANGE_COVERAGE")
    for k,bounds in ranges.items():
        fields(bounds,("min","max"),"PARAMETER_RANGE_FIELDS")
        lo,hi=rational(bounds["min"]),rational(bounds["max"])
        need(lo<=hi and all(lo<=rational(x["value"])<=hi for x in data["parameters"][params[k]["native_name"]]),"PARAMETER_RANGE")
    fields(context,("pairs","contributions") if "ledger" in profile else ("pairs",),"CASE_CONTEXT_FIELDS")
    declared=profile["counterfactual_pairs"];actual=context["pairs"]
    need(type(declared) is list and type(actual) is list,"PAIR_SET")
    def index(rows,keys):
        result={}
        for x in rows:
            fields(x,keys,"PAIR_FIELDS")
            need(type(x["id"]) is str and x["id"] not in result,"PAIR_IDENTITY")
            result[x["id"]]=x
        return result
    dp=index(declared,("id","reference","alternative"));ap=index(actual,("id","reference_exogenous","alternative_exogenous"))
    need(set(dp)==set(ap),"COUNTERFACTUAL_COVERAGE")
    for k,p in dp.items():
        a,b=p["reference"],p["alternative"]
        need(a!=b and a in ins and b in ins,"COUNTERFACTUAL_IDENTITY")
        need(all(ins[a][f]==ins[b][f] for f in ("quantity","domain_ids","dtype")),"COUNTERFACTUAL_SIGNATURE")
        r=ap[k]["reference_exogenous"];s=ap[k]["alternative_exogenous"]
        need(type(r) is dict and bool(r) and type(s) is dict and bool(s) and digest(r)==digest(s),"COUNTERFACTUAL_EXOGENEITY")
    consumer=finite_consumer(package,data)
    ledger=check_ledger(consumer,leaf,profile,context) if "ledger" in profile else "NOT_EXECUTED"
    outputs=consumer.outputs();external={}
    if "output_contract" in profile:
        oc=profile["output_contract"];fields(oc,("external","intermediate"),"OUTPUT_CONTRACT_FIELDS")
        a,b=oc["external"],oc["intermediate"]
        need(type(a) is list and type(b) is list and bool(a) and len(a+b)==len(set(a+b)) and set(a+b)==set(outs),"OUTPUT_PARTITION")
        external={k:outputs[outs[k]["native_name"]] for k in a}
    return {"profile_identity":digest(profile),"study_identity":digest(study),"context":receipt["context_receipt"],
            "identities":identities(package),"outputs":outputs,"external_outputs":external,"conditions":consumer.conditions(),
            "evidence_scope":"BOUNDED_FINITE_NATIVE_METHOD","owner":"OWNER_TBD","ledger":ledger,"conformance":"NOT_PROVED"}
