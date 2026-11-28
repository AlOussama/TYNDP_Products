"""P5 uses a configured outer record contract and the unchanged M3 native graph.
The original JS oracle is never imported or called by the candidate.
"""
import json,copy
from hashlib import sha256
from closure import digest,admit,Reject
from test_closure import fixture,q,dataset,scalar
from package_interface import export_package
from WS_B import affine_boundary
from interface import import_package,finite_consumer
from closure_v1 import definition,diagnostics
from record_contract import structural,native_checks,CandidateReject,at
import p5_graph_projection

def admit_method(profile,record):
    """Actual static native method admission before any record verdict."""
    s=[v["id"] for v in record["scenarios"]]
    h=record["economics"]["horizon_years"]
    if type(h) is not int or h<=0 or h>100:
        raise CandidateReject("DISCOUNT_POLICY_INVALID",["instance","record","economics","horizon_years"],"R12","Declared discount support outside admitted bounded integer horizon")
    y=list(range(1,h+1));money=q("EUR","currency",profile["currency_basis"])
    annual={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{n:{"dims":["s"]} for n in ("base","alt","prob")},"expressions":{"benefit":profile["annual_source"]}}
    a=fixture(annual,quant={"base":money,"alt":money,"benefit":money},domains={"s":s},roles={"prob":"INPUT"})
    p=export_package(admit(json.dumps(annual,sort_keys=True),a))
    doc={"version":0,"dimensions":{"y":{"dtype":"int","ordered":True}},
         "parameters":{"annual":{"dims":[]},"capex":{"dims":[]},"rate":{"dims":[]},"year":{"dims":["y"],"dtype":"int"}},
         "expressions":{"factor":profile["discount_factor_source"],"npv":profile["npv_source"]},"conditions":{"valid_rate":profile["rate_guard"]}}
    ctx=fixture(doc,quant={n:money for n in ("annual","capex","npv")},roles={"annual":"INPUT","rate":"INPUT","year":"INPUT"},
                domains={"y":y},domain_rules={"rate":"NONNEGATIVE","year":"POSITIVE"},pred_axes={"valid_rate":[]})
    ctx["power_domains"]={"year":{"min":1,"max":h}}
    p2=affine_boundary.export_package(affine_boundary.admit(json.dumps(doc,sort_keys=True),ctx))
    leaves=[import_package(z) for z in (p,p2)]
    if export_package(leaves[0])!=p or affine_boundary.export_package(leaves[1])!=p2:raise RuntimeError("P5 native method roundtrip")
    return [{"native_identity":l["native_identity"],"package_sha256":sha256(z.encode()).hexdigest(),"roundtrip":True} for l,z in zip(leaves,(p,p2),strict=True)]

def decision_package(profile):
    if profile["decision_sign_policy"]!="THREE_WAY_THRESHOLD":raise RuntimeError("Unknown decision classifier")
    money=q("EUR","currency",profile["currency_basis"])
    doc={"version":0,"parameters":{"npv":{"dims":[]},"threshold":{"dims":[]}},
         "expressions":{"margin":"npv-threshold"},
         "conditions":{"positive":"npv > threshold","negative":"npv < threshold","neutral":"npv == threshold"}}
    ctx=fixture(doc,quant={n:money for n in ("npv","threshold","margin")},roles={"npv":"INPUT","threshold":"INPUT"},
                pred_axes={n:[] for n in doc["conditions"]})
    package=export_package(admit(json.dumps(doc,sort_keys=True),ctx))
    leaf=import_package(package)
    if export_package(leaf)!=package:raise RuntimeError("Native decision roundtrip drift")
    return package,{"native_identity":leaf["native_identity"],"package_sha256":sha256(package.encode()).hexdigest(),"roundtrip":True}

def decision_receipts(profile,record,outputs,package,static):
    threshold=at(record,profile["decision_threshold_ref"])
    result={}
    for model in record["models"]:
        key=model["id"].lower();npv=outputs["output:"+key+":npv"][0]["value"]
        data=dataset({"npv":scalar(npv),"threshold":scalar(threshold)})
        c=finite_consumer(package,data)
        conditions=c.conditions()
        if sum(bool(v) for v in conditions.values())!=1:raise RuntimeError("Nonexclusive native decision")
        result[model["id"]]={**static,"data_sha256":sha256(json.dumps(data,sort_keys=True).encode()).hexdigest(),
            "upstream_output":"output:"+key+":npv","npv":npv,"threshold":threshold,"threshold_source":profile["decision_threshold_ref"],
            "conditions":conditions,"decision_sign":int(conditions["positive"])-int(conditions["negative"]),"margin":c.outputs()["margin"][0]}
    return result

def compile_p5(x,stage):
    d,i=x["definition"],x["instance"];rec=i["record"];p=d["method_profile"]
    if set(rec)!=set(d["context_scope"]):raise CandidateReject("CONTEXT_COVERAGE",["instance","record"],"R00","Required full context population differs")
    native=admit_method(p,rec);decision,decision_static=decision_package(p);native.append(decision_static);stage["static_native_packages"]=native
    metadata_receipts=structural(rec,p["rules"]);stage["structural_admission_count"]=len(metadata_receipts)
    numeric_receipts=native_checks(rec,p["native_checks"]);stage["numeric_native_receipts"]=numeric_receipts
    # Valid baseline and any valid source use actual record data through the
    # full existing graph. Invalid metadata/numeric candidates must stop first.
    source_text=json.dumps({"profile":p,"record":rec,"original_source":d["original_source"]},sort_keys=True,ensure_ascii=False,separators=(",",":"))
    nd,dp,inst=p5_graph_projection.build(rec,p,source_text)
    ip=digest(inst)
    res=definition.instantiate(nd,dp,inst,ip)
    canonical=definition.export(nd,dp,inst,ip)
    if definition.reimport(canonical,dp,ip)["receipt"]!=res:raise RuntimeError("P5 graph canonical roundtrip drift")
    decisions=decision_receipts(p,rec,res["graph"]["outputs"],decision,decision_static)
    return {"status":res["status"],"semantic_identity":res["definition"]["semantic_identity"],"native_decision_context":decisions,
            "graph_semantic_identity":res["graph"]["semantic_identity"],"graph_audit_identity":res["graph"]["audit_identity"],
            "package_sha256":sha256(canonical.encode()).hexdigest(),"definition_pin":dp,"instance_pin":ip,"roundtrip":True,
            "outputs":res["graph"]["outputs"],"lineage":{k:r["lineage"] for k,r in res["graph"]["slots"].items()},
            "comparison_evidence":res["comparison_evidence"],"external_reports":res["graph"]["external_reports"],
            "structural_checks":metadata_receipts,"numeric_checks":numeric_receipts,"native_static":native,
            "conformance":"NOT_PROVED","owner":"OWNER_TBD"}
