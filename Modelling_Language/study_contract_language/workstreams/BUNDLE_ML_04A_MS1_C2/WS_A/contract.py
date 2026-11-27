"""Bounded C2 external assertion evaluation. Native conditions are mathematical authority."""
import sys
from pathlib import Path
from itertools import product
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT.parent/"BUNDLE_ML_04A_MS1_C1"/"comparative_canonical"))
from interface import resolve_predicate
from package_interface import import_package
from closure import need,fields
from native_consumer import FiniteNative

TRUTH=("FALSE","UNKNOWN","TRUE")
ROLES=("SAFETY_GUARANTEE","SERVICE_GUARANTEE","CAPABILITY_GUARANTEE","DATA_ASSUMPTION","TECHNICAL_ASSUMPTION","ENVIRONMENT_ASSUMPTION","CONDITIONAL_OBLIGATION","PERMITTED_BEHAVIOUR","PROHIBITED_BEHAVIOUR")
def not3(x):
    need(x in TRUTH,"BOOL3");return TRUTH[2-TRUTH.index(x)]
def fold3(op,values):
    need(op in ("FORALL","EXISTS"),"QUANTIFIER")
    need(bool(values) and all(v in TRUTH for v in values),"NONEMPTY_BOOL3_DOMAIN")
    return (min if op=="FORALL" else max)(values,key=TRUTH.index)

def evaluate(package,data,assertion):
    leaf=import_package(package)  # admit ALL mathematics before evaluating guard
    fields(assertion,("id","role","modality","predicate","binders","guard","authority"),"ASSERTION_FIELDS")
    role=assertion["role"];need(role in ROLES,"SEMANTIC_ROLE")
    need(type(assertion["id"]) is str and bool(assertion["id"]),"ASSERTION_ID")
    need(assertion["modality"] in ("MUST","MUST_NOT","MAY"),"MODALITY")
    need((role=="PERMITTED_BEHAVIOUR")== (assertion["modality"]=="MAY"),"PERMISSION_MODALITY")
    need((role=="PROHIBITED_BEHAVIOUR")== (assertion["modality"]=="MUST_NOT"),"PROHIBITION_MODALITY")
    need(assertion["authority"]=="OWNER_TBD","AUTHORITY_PROMOTION")
    pred=resolve_predicate(package,assertion["predicate"])
    need((role=="DATA_ASSUMPTION")== (pred["role"]=="DATA_ASSUMPTION"),"ASSUMPTION_GUARANTEE_ROLE")
    need(pred["role"]!="GUARD","GUARD_AS_OBLIGATION")
    c=leaf["context"];domains={d["id"]:(n,d["labels"]) for n,d in c["domains"].items()}
    bs=assertion["binders"];need(type(bs) is list,"BINDERS")
    for b in bs:
        fields(b,("axis","kind","quantifier"),"BINDER_FIELDS")
        need(b["axis"] in domains and b["quantifier"] in ("FORALL","EXISTS") and b["kind"] in ("time","scenario","trace","request","response","component","port","sample"),"BINDER")
    axes=[b["axis"] for b in bs]
    need(len(axes)==len(set(axes)) and set(axes)==set(pred["qualified_axes"]),"UNBOUND_OR_DUPLICATE_AXIS")
    if role in ("SERVICE_GUARANTEE","CAPABILITY_GUARANTEE"):
        need(len(bs)>=2 and (bs[0]["kind"],bs[0]["quantifier"],bs[1]["kind"],bs[1]["quantifier"])==("request","FORALL","response","EXISTS"),"REQUEST_RESPONSE_ORDER")
    guard=assertion["guard"];need(guard in TRUTH,"BOOL3_GUARD")
    consumer=FiniteNative(leaf,data) if data is not None else None  # validate all supplied data even on inactive guard
    reason=None
    if guard=="FALSE":status="NOT_APPLICABLE";truth=None
    elif guard=="UNKNOWN":status="BLOCKED";truth="UNKNOWN";reason="UNKNOWN_GUARD"
    elif consumer is None:status="BLOCKED";truth="UNKNOWN";reason="MISSING_DATA"
    elif pred["role"]=="DATA_ASSUMPTION":status="BLOCKED";truth="UNKNOWN";reason="NATIVE_ASSUMPTION_EVALUATION_NOT_IMPLEMENTED"
    elif role=="PERMITTED_BEHAVIOUR":status="NOT_EXECUTED";truth=None;reason="PERMISSION_NOT_OBLIGATION"
    else:
        cond=consumer.program.conditions[pred["native_name"]].condition.root
        def walk(i,env):
            if i==len(bs):
                value=consumer.cond(cond,env)
                need(type(value) is bool,"NONBINARY_NATIVE_PREDICATE")
                truth="TRUE" if value else "FALSE"
                return not3(truth) if assertion["modality"]=="MUST_NOT" else truth
            b=bs[i];n,labels=domains[b["axis"]]
            return fold3(b["quantifier"],[walk(i+1,{**env,n:x}) for x in labels])
        truth=walk(0,{})
        status="FINITE_OBSERVED_TRUE" if truth=="TRUE" else "FINITE_OBSERVED_FALSE" if truth=="FALSE" else "BLOCKED"
        if role in ("SERVICE_GUARANTEE","CAPABILITY_GUARANTEE"):
            reason="BEHAVIOURAL_EVIDENCE_REQUIRED"  # finite matrix is not complete actual behavior
    return {"assertion_id":assertion["id"],"truth":truth,"finite_status":status,"reason":reason,"owner":"OWNER_TBD","authority_status":"UNRESOLVED","conformance":"NOT_PROVED","mathematical_identity":pred["mathematical_identity"],"evidence_scope":"FINITE_DECLARED_SUPPORT_ONLY"}
