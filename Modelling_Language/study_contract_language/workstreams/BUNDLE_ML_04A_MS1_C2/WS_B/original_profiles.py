"""Bounded, source-preserving migration of the four original research profiles.
The existing MS1 compiler produces native mathspec syntax; C2 admits it via public Program.
No reverse translation, no second mathematical authority. R1 N2R is an independent legacy check.
"""
from pathlib import Path
import sys,json
from fractions import Fraction
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from interface import resolve_method
from closure import admit,source_map,native,digest,text_hash,need
from package_interface import export_package
from WS_B import affine_boundary as affine
from methods import validate,identities
from adapter import compile_profile
import n2r
R1=ROOT.parent/"BUNDLE_ML_04A_R1"/"fixtures"
MS1=ROOT.parent/"BUNDLE_ML_04A_MS1"/"architecture_prototypes"/"profiles"
PIN="9435ac2db07df4313b942f11c09f8268bc0206a5"
def read(path):return json.loads(path.read_text())
def hashfile(path):return sha256(path.read_bytes()).hexdigest()
def quantity(unit,basis=""):
    need(unit in ("EUR","MW","MWh","h","1"),"LEGACY_UNIT_UNSUPPORTED")
    return {"unit":unit,"carrier":"currency" if unit=="EUR" else "electricity" if unit in ("MW","MWh") else "none",
            "basis":basis or "NONE","sign":"NONE","direction":"NONE","time_basis":"NONE"}
def load(family,label):
    root=R1 if family=="R1" else MS1
    mp=root/(("method-"+label+".json") if family=="R1" else label+".json")
    sp=root/(("study-"+label+".json") if family=="R1" else "study.json")
    dp=root/"data.json"
    method,study,data=read(mp),read(sp),read(dp)
    source=mp.read_text()
    legacy=None
    contract=None
    if family=="R1":
        need(hashfile(mp)==study["method_ref"]["sha256"] and hashfile(dp)==study["data_ref"]["sha256"],"ORIGINAL_SOURCE_PIN")
        contract=read(root/"contract.b.json")
        legacy=n2r.evaluate((root/"contract.a.scn").read_text(),"A",sp,root/"trust.json")
        need(legacy["audit"]["authority"]["owner"]=="OWNER_TBD","ORIGINAL_AUTHORITY")
    return method,study,data,source,mp,sp,dp,legacy,contract
def prepare(family,label):
    method,oldstudy,snapshot,source,mp,sp,dp,legacy,contract=load(family,label)
    # The *same* original compiler used by the frozen MS1 experiments.
    reference=compile_profile(method,oldstudy,snapshot)
    doc=source_map(reference.canonical);ed=snapshot["engine_data"]
    ax={k:k.split(":")[-1] for k in ed["axes"]}
    need(len(ax)==len(set(ax.values())),"MIGRATION_AXIS_ALIAS")
    for k,v in ed["axes"].items():
        z=doc["dimensions"][ax[k]]
        z["dtype"]="int" if type(v["ids"][0]) is int else "str"
        z["ordered"]=v["role"]=="time"
    roles={};ids={};rules={};power={}
    bindings=snapshot.get("bindings",{})
    contract_inputs={z["id"]:z for z in contract["frame"]["data_inputs"]} if contract else {}
    for n,v in method["inputs"].items():
        if family=="R1":
            b=bindings[n];roles[n]="OBSERVABLE" if b["role"]=="contribution" else "INPUT"
            ids[n]=b["observable"] if b["role"]=="contribution" else b["data_ref"]
            if b["role"]=="auxiliary" and contract_inputs[b["data_ref"]]["role"]=="period_count":
                doc["parameters"][n]["dtype"]="int";rules[n]="NONNEGATIVE"
                # explicit research subset admission bound, not a normative R1 method parameter
                power[n]={"min":0,"max":99}
        else:roles[n]="INPUT";ids[n]="input:"+n
        if v["role"]=="time_weight":rules[n]="POSITIVE"
        if v["role"]=="probability":rules[n]="NONNEGATIVE"
    for n,v in method["parameters"].items():
        roles[n]="METHOD_PARAMETER";ids[n]="parameter:"+n
        if Fraction(v["min"])>=0:rules[n]="NONNEGATIVE"
    symbols={}
    for n,v in method["inputs"].items():
        symbols[n]={"id":ids[n],"role":roles[n],"quantity":quantity(v["unit"],v["basis"]),"domain_rule":rules.get(n,"ANY_EXACT")}
    for n,v in method["parameters"].items():
        symbols[n]={"id":ids[n],"role":roles[n],"quantity":quantity(v["unit"]),"domain_rule":rules.get(n,"ANY_EXACT")}
    for n,v in method["rules"].items():
        symbols[n]={"id":"output:"+n,"role":"DERIVED_EXPRESSION","quantity":quantity(v["unit"],v["basis"]),"domain_rule":"ANY_EXACT"}
    m={"id":method["id"],"version":method["version"],"inputs":list(method["inputs"]),"parameters":list(method["parameters"]),"outputs":list(method["rules"])}
    c={"domains":{ax[k]:{"id":k,"labels":v["ids"]} for k,v in ed["axes"].items()},"relations":{},"symbols":symbols,"predicates":{},
       "scope":{"id":"scope:original-profile","binders":list(doc["dimensions"]),"alignment":"SAME_OR_SCALAR"},"temporal":{},"conversions":{},
       "method":m,"study":{"id":oldstudy["id"],"version":oldstudy["version"],"method_ref":digest(m),"data_id":"data:original-"+family.lower(),"data_version":hashfile(dp),"owner":"OWNER_TBD"},
       "audit":{"source_id":"source:original-profile","source_ref":"git:"+PIN+":"+str(mp.relative_to(ROOT.parent)),"evidence_id":"evidence:original-profile","authority":"RESEARCH_ASSUMPTION"}}
    if power:c["power_domains"]=power
    # Native dims may have canonical order different from original R1 key order. Preserve identities explicitly.
    program=native(json.dumps(doc)).program
    params={}
    for n,p in program.parameters.items():
        if n in method["parameters"]:
            params[n]=[{"key":[],"value":oldstudy["parameters"][n]}];continue
        orig=ed["series"][n]["axes"];order=[ax[a] for a in orig]
        params[n]=[{"key":[row["key"][order.index(a)] for a in p.dims],"value":row["value"]} for row in ed["series"][n]["rows"]]
    data={"id":c["study"]["data_id"],"version":c["study"]["data_version"],"parameters":params,"relations":{}}
    pkg=affine.export_package(affine.admit(json.dumps(doc),c)) if power else export_package(admit(json.dumps(doc),c))
    r=resolve_method(pkg,data)
    pair_specs=[{"id":p["id"],"reference":ids[p["reference"]],"alternative":ids[p["alternative"]]} for p in ed["pairs"]]
    ctx={"pairs":[{"id":p["id"],"reference_exogenous":snapshot["contexts"][p["reference_snapshot"]],"alternative_exogenous":snapshot["contexts"][p["alternative_snapshot"]]} for p in ed["pairs"]]}
    profile={"id":m["id"],"version":m["version"],"native_signature":r["method_signature_identity"],"native_semantic_identity":identities(pkg)["semantic"],
             "source_ref":c["audit"]["source_ref"],"source_sha256":text_hash(source),"approval":"RESEARCH_ASSUMPTION",
             "input_roles":{ids[n]:("DURATION_WEIGHT" if v["role"]=="time_weight" and v["unit"]=="h" else v["role"].upper()) for n,v in method["inputs"].items()},
             "axis_roles":{k:v["role"] for k,v in ed["axes"].items()},
             "parameter_ranges":{ids[n]:{"min":v["min"],"max":v["max"]} for n,v in method["parameters"].items()},
             "probability_rules":{ids[n]:"SUM_ONE" for n,v in method["inputs"].items() if v["role"]=="probability"},"counterfactual_pairs":pair_specs,
             "outputs":["output:"+n for n in method["rules"]],"output_contract":{"external":["output:summary"],"intermediate":["output:"+n for n in method["rules"] if n!="summary"]}}
    if family=="R1":
        profile["ledger"]={"policy":oldstudy["ledger_policy"],"bindings":bindings,"key_axes":{n:v["axes"] for n,v in method["inputs"].items()}}
        ctx["contributions"]=snapshot["contributions"]
    audit={"source_pin":PIN,"method_path":str(mp.relative_to(ROOT.parent)),"method_sha256":hashfile(mp),"study_sha256":hashfile(sp),"data_sha256":hashfile(dp),
           "legacy_math_canonical_sha256":text_hash(reference.canonical),"migration_package_identity":identities(pkg)["audit"],
           "legacy_audit_identity":legacy["audit_digest"] if legacy else None,"legacy_scope":"FINITE_RESEARCH_MIGRATION_NOT_GENERAL_EQUIVALENCE"}
    return {"package":pkg,"data":data,"profile":profile,"source":source,"context":ctx,"native_context":c,"doc":doc,"legacy":legacy,
            "reference_summary":str(reference.scalar("summary").value),"audit":audit}
def run(x):
    p=x["package"];r=resolve_method(p,x["data"]);s=x["native_context"]["study"];m=x["profile"];ctx=x["context"]
    st={"id":s["id"],"version":s["version"],"profile_identity":digest(m),"native_study_identity":r["study_identity"],
        "data_context_identity":r["context_receipt"]["context_identity"],"case_context_identity":digest(ctx),"owner":"OWNER_TBD"}
    return validate(p,x["data"],m,st,x["source"],ctx)
