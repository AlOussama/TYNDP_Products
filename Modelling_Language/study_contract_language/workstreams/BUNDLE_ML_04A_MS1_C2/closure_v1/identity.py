"""Versioned semantic projection with explicit ordered/unordered fields.
Original bytes and exact input remain in audit; no general math equivalence claim.
"""
from copy import deepcopy
import json
from closure import digest,native,source_map,semantic_context,c1
from interface import import_package,package_version

def mathematics(package):
    leaf=import_package(package)
    doc=source_map(leaf["native_canonical"]);doc.pop("description",None)
    # Only documented native description fields in admitted sections.
    for sec in ("dimensions","relations","parameters","expressions","conditions","assumptions"):
        for v in doc.get(sec,{}).values():
            if type(v) is dict:v.pop("description",None)
    spec=native(json.dumps(doc));context=semantic_context(spec,leaf["context"])
    context["study"]["method_ref"]=digest(context["method"])
    return digest({"projection":"c2-closure-native-semantic-0.1","package_schema":package_version(package),"upstream":leaf["upstream"],"registry":digest(c1.REGISTRY),"canonical":spec.to_yaml(canonical=True),"binding":context})
def byid(xs):return sorted(xs,key=lambda x:x["id"])
def frame(value):
    x=deepcopy(value)
    for k,v in x.items():
        if type(v) is not list:continue
        x[k]=byid(v)
        for r in x[k]:
            for f in ("authority_refs","source_refs","subjects","domains","alternatives","inputs","outputs","observables","depends_on","allowed_changes"):
                if f in r:r[f]=sorted(r[f])
            if k=="domains" and not r["ordered"]:r["members"]=sorted(r["members"])
            if k=="information_sets":r["partition"]=sorted([sorted(g) for g in r["partition"]])
    return x
def assertion(a):
    x=deepcopy(a)
    for k in ("assumptions","authority_refs"):x[k]=sorted(x[k])
    for k,v in x["at"].items():x["at"][k]=sorted(v)
    # Binders are ordered. AND/OR order is conservatively retained.
    return x
def profile(p,package):
    x=deepcopy(p)
    # Method source bytes are audit; source_ref and version stay semantic.
    x.pop("source_sha256");x.pop("native_signature");x["native_semantic_identity"]=mathematics(package)
    x["outputs"]=sorted(x["outputs"]);x["counterfactual_pairs"]=byid(x["counterfactual_pairs"])
    if "output_contract" in x:
        for k in ("external","intermediate"):x["output_contract"][k]=sorted(x["output_contract"][k])
    return x
