"""C2 bounded integrated research snapshot. Native mathematics is never lowered to a second AST."""
from copy import deepcopy
from interface import import_package
from closure import fields,need,canon,digest,c1
from WS_A.contract import evaluate_group
from WS_B.methods import validate,identities

VERSION="c2-canonical-study-contract-0.1"
INPUT_VERSION="c2-study-contract-input-0.1"
def semantic_contract(package,contract):
    p=deepcopy(contract)
    p["assertions"]=sorted(p["assertions"],key=lambda a:a["id"])
    return digest({"schema":VERSION,"mathematics":identities(package)["semantic"],"contract":p})

def evaluate(obj):
    fields(obj,("schema","package","contract","contract_ref","profile","study","source","data","case_context","verification"),"C2_INTEGRATED_FIELDS")
    need(obj["schema"]==INPUT_VERSION,"C2_INTEGRATED_VERSION")
    pkg=obj["package"];leaf=import_package(pkg)
    contract=obj["contract"]
    a=evaluate_group(pkg,obj["data"],contract)
    need(obj["contract_ref"]==semantic_contract(pkg,contract),"STUDY_CONTRACT_REFERENCE")
    b=validate(pkg,obj["data"],obj["profile"],obj["study"],obj["source"],obj["case_context"])
    for k,v in contract["domain_kinds"].items():
        need(obj["profile"]["axis_roles"][k]==(v if v in ("time","scenario") else "sample"),"CROSS_DOMAIN_ROLE")
    assumption_ids={v["id"] for v in leaf["interface"]["predicates"].values() if v["role"]=="DATA_ASSUMPTION"}
    bound=[z["predicate"]["predicate_id"] for z in contract["assertions"] if z["role"]=="DATA_ASSUMPTION"]
    need(len(bound)==len(set(bound)) and set(bound)==assumption_ids,"NATIVE_ASSUMPTION_COVERAGE")
    # Explicit evidence requests do not permit self-certification or promote finite results.
    vr=obj["verification"];need(type(vr) is list,"VERIFICATION_LIST")
    expected={z["id"] for z in contract["assertions"] if z["modality"]!="MAY"}
    ids=set();covered=set()
    for z in vr:
        fields(z,("id","assertion_id","kind","authority"),"VERIFICATION_FIELDS")
        need(type(z["id"]) is str and bool(z["id"]) and z["id"] not in ids,"VERIFICATION_ID")
        need(z["assertion_id"] in expected and z["assertion_id"] not in covered,"VERIFICATION_REFERENCE")
        need(z["kind"]=="FINITE_OBSERVATION" and z["authority"]=="OWNER_TBD","VERIFICATION_AUTHORITY")
        ids.add(z["id"]);covered.add(z["assertion_id"])
    need(expected==covered,"VERIFICATION_COVERAGE")
    sem=digest({"schema":VERSION,"contract":obj["contract_ref"],"profile":b["profile_identity"],
                "study":b["study_identity"],"verification":sorted(vr,key=lambda z:z["id"])})
    receipt={"semantic_identity":sem,"native_identity":b["identities"]["native"],"mathematical_semantic_identity":b["identities"]["semantic"],
             "original_source_identity":b["identities"]["original_source"],"contract":a,"method":b,
             "evidence_scope":"BOUNDED_FINITE_SYNTHETIC_OBSERVATIONS","owner":"OWNER_TBD","conformance":"NOT_PROVED"}
    receipt["audit_identity"]=digest({"input":obj,"receipt":receipt})
    return receipt
def export(obj):
    return canon({"schema":VERSION,"input":obj,"receipt":evaluate(obj)})
def reimport(text):
    p=c1.parse(text);fields(p,("schema","input","receipt"),"C2_CANONICAL_FIELDS")
    need(p["schema"]==VERSION,"C2_CANONICAL_VERSION")
    need(export(p["input"])==text,"C2_CANONICAL_TAMPER_OR_NONCANONICAL")
    return p
