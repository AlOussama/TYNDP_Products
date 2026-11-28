"""C5 bounded V-model research profile over existing C4 Definition/Instance.
No mathematical expression grammar, AST, evaluator, or solver here.
Only native C4 contract evaluations can produce computed technical evidence.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import product
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"BUNDLE_ML_04A_MS1_C3"))
from authoring import decode,emit_control
from closure import digest,canon,need,fields,qualified
from closure_v1 import definition,diagnostics
from closure_v1 import metadata as md
from interface import resolve_predicate

DEF="c5-vmodel-definition-0.1"
INST="c5-vmodel-instance-0.1"
PACKAGE="c5-vmodel-package-0.1"
GOVERNANCE="NON-NORMATIVE / RESEARCH ONLY"

def nonempty(x):
    return type(x) is str and bool(x.strip())

def index(rows,keys,code):
    need(type(rows) is list,code)
    out={}
    for r in rows:
        fields(r,keys,code)
        need(qualified(r["id"]) and r["id"] not in out,code+"_ID")
        need(nonempty(r["version"]),code+"_VERSION")
        out[r["id"]]=r
    return out

def refs(xs,table,code,empty=False):
    need(type(xs) is list and (empty or bool(xs)) and all(type(x) is str and x in table for x in xs) and len(xs)==len(set(xs)),code)

def targets(base):
    f=base["frame"]
    out={}
    for slot in base["slots"]:
        for a in slot["assertions"]:
            if a["modality"]!="MAY" and a["role"] not in ("DATA_ASSUMPTION","ENVIRONMENT_ASSUMPTION","TECHNICAL_ASSUMPTION"):
                out[a["id"]]={"kind":"ASSERTION","scope":a["scope"],"slot":slot["id"],"record":a}
        for c in slot["comparisons"]:
            row=next(z for z in f["comparisons"] if z["id"]==c["policy"])
            out[row["id"]]={"kind":"COMPARISON","scope":next(z["scope"] for z in f["slots"] if z["id"]==slot["id"]),"slot":slot["id"],"record":row}
        for bind in slot["bindings"].values():
            if bind["kind"]=="OUTPUT":
                row=next(z for z in f["outputs"] if z["id"]==bind["ref"])
                out[row["id"]]={"kind":"OUTPUT","scope":next(z["scope"] for z in f["slots"] if z["id"]==slot["id"]),"slot":slot["id"],"record":row}
    for r in f["report_requests"]:
        out[r["id"]]={"kind":"REPORT","scope":None,"slot":None,"record":r}
    return out

def check_design(d,dp):
    fields(d,("schema","base","requirements","metrics","tests"),"C5_DEFINITION_FIELDS")
    need(d["schema"]==DEF and digest(d)==dp,"C5_DEFINITION_PIN")
    b=d["base"]; bd=digest(b); static=definition.admit(b,bd)
    tabs=md.validate(b["frame"])
    source={r["id"]:r for r in b["sources"]}
    targs=targets(b)
    req=index(d["requirements"],("id","version","level","statement","source_ref","source_kind","authority_ref","scope","required","parents","targets","metric_refs"),"C5_REQUIREMENT")
    met=index(d["metrics"],("id","version","role","meaning","target","source_ref"),"C5_METRIC")
    tests=index(d["tests"],("id","version","kind","objective","requirements","metric","criterion","scope","oracle_ref","method","coverage","evidence"),"C5_TEST")
    ids=set(req)|set(met)|set(tests)
    need(len(ids)==len(req)+len(met)+len(tests) and not ids.intersection({k for t in tabs.values() for k in t}|set(targs)|set(source)|{b["study"]["id"],b["frame"]["id"]}),"C5_ID_COLLISION")
    for k,r in req.items():
        need(r["level"] in ("STUDY","SYSTEM") and type(r["required"]) is bool and nonempty(r["statement"]),"C5_REQUIREMENT_KIND")
        need(r["source_ref"] in source and r["source_kind"] in ("ORIGINAL_SOURCE","RESEARCH_REQUIREMENT") and r["authority_ref"] in tabs["authorities"] and r["authority_ref"] in source,"C5_REQUIREMENT_SOURCE")
        need(r["scope"] in tabs["scopes"],"C5_REQUIREMENT_SCOPE")
        refs(r["parents"],req,"C5_PARENT",r["level"]=="STUDY")
        refs(r["targets"],targs,"C5_REQUIREMENT_TARGET",r["level"]=="STUDY")
        refs(r["metric_refs"],met,"C5_REQUIREMENT_METRICS",not r["required"])
        need(all(met[x]["role"] in (("STUDY","VALIDATION") if r["level"]=="STUDY" else ("VERIFICATION",)) for x in r["metric_refs"]),"C5_REQUIREMENT_METRIC_ROLE")
        need(r["level"]!="STUDY" or not r["parents"],"C5_STUDY_PARENT")
        need(all(targs[t]["scope"] in (None,r["scope"]) for t in r["targets"]),"C5_TARGET_SCOPE")
        need(all(req[p]["scope"]==r["scope"] for p in r["parents"]),"C5_REFINEMENT_SCOPE")
    # Directed derivation is a DAG; every system requirement reaches a study requirement.
    def visit(k,path):
        need(k not in path,"C5_DERIVATION_CYCLE")
        for p in req[k]["parents"]:visit(p,path|{k})
    for k in req:visit(k,set())
    for k,m in met.items():
        need(nonempty(m["meaning"]) and m["source_ref"] in source and m["target"] in targs,"C5_METRIC_REFERENCE")
        kind=targs[m["target"]]["kind"]
        need((m["role"],kind) in {("STUDY","OUTPUT"),("VERIFICATION","ASSERTION"),("VERIFICATION","COMPARISON"),("VERIFICATION","OUTPUT"),("VALIDATION","REPORT")},"C5_METRIC_ROLE")
    coverage={k:set() for k in req}
    for k,t in tests.items():
        refs(t["requirements"],req,"C5_TEST_REQUIREMENTS")
        need(nonempty(t["objective"]) and t["metric"] in met and t["oracle_ref"] in source and t["scope"] in tabs["scopes"],"C5_TEST_REFERENCE")
        m=met[t["metric"]];need(t["criterion"] in targs,"C5_CRITERION_REFERENCE");target=targs[t["criterion"]]
        metric_target=targs[m["target"]]
        need(t["coverage"]==("ALL_DECLARED_SUPPORT" if t["kind"]=="VERIFICATION" else "EXTERNAL_SCOPE"),"C5_COVERAGE_POLICY")
        if metric_target["kind"]=="OUTPUT":
            need(target["kind"]=="ASSERTION" and target["slot"]==metric_target["slot"],"C5_METRIC_CRITERION_BINDING")
            row=next(z for z in b["slots"] if z["id"]==target["slot"])
            symbols=[k for k,v in row["bindings"].items() if v["kind"]=="OUTPUT" and v["ref"]==m["target"]]
            p=resolve_predicate(row["package"],target["record"]["predicate"])
            need(len(symbols)==1 and symbols[0] in p["required_symbols"],"C5_METRIC_CRITERION_DEPENDENCY")
        else:need(t["criterion"]==m["target"],"C5_METRIC_CRITERION_BINDING")
        need(t["evidence"]=="COMPUTED_NATIVE_RECEIPT" if t["kind"]=="VERIFICATION" else t["evidence"]=="EXTERNAL_REVIEW_RECEIPT","C5_TEST_EVIDENCE_ROLE")
        need((t["kind"],m["role"],target["kind"],t["method"]) in {
            ("VERIFICATION","VERIFICATION","ASSERTION","NATIVE_ASSERTION"),
            ("VERIFICATION","VERIFICATION","COMPARISON","NATIVE_COMPARISON"),
            ("VALIDATION","VALIDATION","REPORT","EXTERNAL_REVIEW")},"C5_TEST_METHOD")
        need(target["scope"] in (None,t["scope"]),"C5_TEST_SCOPE")
        for r in t["requirements"]:
            a=req[r]
            need(a["scope"]==t["scope"] and ((a["level"]=="SYSTEM" and t["kind"]=="VERIFICATION") or (a["level"]=="STUDY" and t["kind"]=="VALIDATION")),"C5_TEST_LEVEL_SCOPE")
            need(t["criterion"] in a["targets"] and m["id"] in a["metric_refs"],"C5_TEST_TARGET")
            coverage[r].add(t["criterion"])
    for k,r in req.items():
        if r["required"]:
            need(bool(r["targets"]) and coverage[k]==set(r["targets"]),"C5_REQUIREMENT_TEST_COVERAGE")
    # No orphan verification/validation metric or test.
    need({t["metric"] for t in tests.values()}=={k for k,m in met.items() if m["role"]!="STUDY"},"C5_METRIC_TEST_COVERAGE")
    sem={"schema":DEF,"base_semantic":static["semantic_identity"],
         "requirements":[{**r,"parents":sorted(r["parents"]),"targets":sorted(r["targets"]),"metric_refs":sorted(r["metric_refs"])} for _,r in sorted(req.items())],
         "metrics":[r for _,r in sorted(met.items())],
         "tests":[{**r,"requirements":sorted(r["requirements"])} for _,r in sorted(tests.items())]}
    return static,req,met,tests,targs,digest(sem)

def admit(d,dp):
    static,req,met,tests,targs,semantic=check_design(d,dp)
    return {"status":"STATIC_VALID","semantic_identity":semantic,"definition_pin":dp,"base":static,
            "test_count":len(tests),"conformance":"NOT_PROVED","owner":"OWNER_TBD"}

def comparison_support(base,i,target):
    # This is coverage metadata, not a second comparison predicate.
    # Actual exogeneity and change authorization are judged by native C4 graph.
    f=base["frame"];dims={x["id"]:x["members"] for x in f["domains"]}
    contexts={x["id"]:x for x in f["context_fields"]};fields_={}
    for pair in [*target["record"]["exogenous"].values(),*target["record"]["project"].values()]:
        for side in ("reference","alternative"):
            k=pair[side];axes=contexts[k]["axes"]
            expected=set(product(*(dims[a] for a in axes)))
            actual=i.get("context_data",{}).get(k) if type(i.get("context_data")) is dict else None
            if type(actual) is not list:
                fields_[k]={"expected":len(expected),"observed":None,"complete":False,"identity":None}
                continue
            if any(type(r) is not dict or set(r)!={"key","value"} or type(r["key"]) is not list or any(type(v) not in (str,int) for v in r["key"]) or type(r["value"]) is not str for r in actual):
                fields_[k]={"expected":len(expected),"observed":None,"complete":False,"identity":None};continue
            keys=[tuple(r["key"]) for r in actual]
            complete=set(keys)==expected and len(keys)==len(expected)
            fields_[k]={"expected":len(expected),"observed":len(keys),"complete":complete,
                        "missing":[list(x) for x in sorted(expected-set(keys))],
                        "identity":digest(sorted(actual,key=lambda r:r["key"]))}
    return fields_

def result_for(t,target,native,base,i):
    if t["kind"]=="VALIDATION":
        return "NOT_EXECUTED","UNKNOWN",{},{"reason":"EXTERNAL_REVIEW_NOT_VERIFIED"}
    graph=native.get("result") or {}
    graph=graph.get("graph",{})
    evidence={}
    if target["kind"]=="COMPARISON":
        support=comparison_support(base,i,target)
        evidence["coverage"]=support
        if not all(x["complete"] for x in support.values()):
            return "BLOCKED","TRUE",evidence,{"reason":"INCOMPLETE_COMPARISON_SUPPORT"}
        if native["status"]=="RETURNED" and graph:
            matches=[r for r in graph["slots"][target["slot"]]["comparisons"] if r["policy"]==target["record"]["id"]]
            need(len(matches)==1,"C5_COMPARISON_RECEIPT")
            need(all(graph["data_bindings"].get(k)==v["identity"] for k,v in support.items()),"C5_COMPARISON_DATA_RECEIPT")
            evidence["native_comparison"]=matches[0]
            return "PASS","TRUE",evidence,{"reason":"FINITE_NATIVE_COMPARISON_SATISFIED"}
        diags=native.get("diagnostics",[])
        # A rejection is attributable only to this slot and a unique policy.
        # Unknown/internal/multi-policy errors never become expected FAIL.
        same_slot=[z for z in base["slots"] if z["id"]==target["slot"]]
        if len(diags)==1 and diags[0]["status"]=="REJECTED" and diags[0]["subject"]==target["slot"] and len(same_slot[0]["comparisons"])==1 and diags[0]["code"] in ("COUNTERFACTUAL_EXOGENEITY","UNAUTHORIZED_PROJECT_CHANGE"):
            evidence["native_diagnostic"]=diags[0]
            return "FAIL","TRUE",evidence,{"reason":"ATTRIBUTABLE_NATIVE_COUNTEREXAMPLE"}
        return "BLOCKED","TRUE",evidence,{"reason":"NO_ATTRIBUTABLE_NATIVE_RECEIPT","diagnostics":diags}
    if native["status"]!="RETURNED" or not graph:
        return "BLOCKED","UNKNOWN",evidence,{"reason":"NATIVE_EVALUATION_UNAVAILABLE","diagnostics":native.get("diagnostics",[])}
    rows=graph["slots"][target["slot"]]["obligations"]["assertions"]
    hit=[r for r in rows if r["id"]==target["record"]["id"]]
    need(len(hit)==1,"C5_ASSERTION_RECEIPT")
    a=hit[0];evidence["native_assertion"]=a
    # C4 records the finite fold, not full point-level coverage certificates.
    # Do not claim complete coordinate coverage when guard/witness reasons exist.
    if a["truth"] is None:
        return "NOT_EXECUTED","FALSE",evidence,{"reason":"NATIVE_NOT_APPLICABLE"}
    if a["truth"]=="FALSE":
        return "FAIL","TRUE",evidence,{"reason":"NATIVE_FINITE_COUNTEREXAMPLE"}
    if a["truth"]=="TRUE" and not a["reasons"] and not a["missing_witnesses"]:
        return "PASS","TRUE",evidence,{"reason":"NATIVE_FINITE_ASSERTION_TRUE"}
    return "INCONCLUSIVE","UNKNOWN",evidence,{"reason":"NATIVE_UNKNOWN_OR_CONDITIONAL_COVERAGE"}

def instantiate(d,dp,i,ip):
    static,req,met,tests,targs,semantic=check_design(d,dp)
    fields(i,("schema","definition_ref","base","requested_tests","run_id","claims"),"C5_INSTANCE_FIELDS")
    need(i["schema"]==INST and digest(i)==ip and i["definition_ref"]==semantic,"C5_INSTANCE_PIN")
    need(nonempty(i["run_id"]),"C5_RUN_ID")
    refs(i["requested_tests"],tests,"C5_REQUESTED_TESTS",True)
    base=d["base"];b=i["base"];bd=digest(base);bi=digest(b)
    # The outer pinned roots commit to the nested bytes. Derived inner pins
    # do not confer independent authority or normative approval.
    native=diagnostics.candidate_receipt(definition.instantiate,base,bd,b,bi)
    if native["status"]=="BLOCKED_INTERNAL":raise RuntimeError("C5_NATIVE_INTERNAL:"+str(native["diagnostics"]))
    claims=index(i["claims"],("id","version","test","test_version","definition_pin","base_instance_pin","verdict","source_ref"),"C5_DECLARED_EVIDENCE")
    for r in claims.values():
        need(r["test"] in tests and r["test_version"]==tests[r["test"]]["version"] and r["definition_pin"]==dp and r["base_instance_pin"]==bi and r["source_ref"] in {s["id"] for s in base["sources"]} and r["verdict"] in ("PASS","FAIL","INCONCLUSIVE"),"C5_DECLARED_EVIDENCE_BINDING")
    result={};evidences=[]
    for k,t in sorted(tests.items()):
        m=met[t["metric"]];target=targs[t["criterion"]];record=None
        c=[r for r in claims.values() if r["test"]==k]
        if k not in i["requested_tests"]:
            status,app,execution="NOT_EXECUTED","UNKNOWN","NOT_EXECUTED";reason={"reason":"TEST_NOT_REQUESTED"}
        else:
            status,app,observed,reason=result_for(t,target,native,base,b)
            if targs[m["target"]]["kind"]=="OUTPUT":
                observed["metric_value"]=(native.get("result") or {}).get("graph",{}).get("outputs",{}).get(m["target"])
                if status=="PASS" and observed["metric_value"] is None:status="BLOCKED";reason={"reason":"MISSING_METRIC_OUTPUT"}
            execution="NOT_EXECUTED" if t["kind"]=="VALIDATION" else "BLOCKED" if status=="BLOCKED" else "EXECUTED"
            if t["kind"]=="VERIFICATION":
                record={"test":k,"test_version":t["version"],"requirement_refs":sorted(t["requirements"]),
                        "metric":m["id"],"metric_version":m["version"],"oracle_ref":t["oracle_ref"],"subject":t["criterion"],"metric_target":m["target"],"expected":"DECLARED_CRITERION_SATISFIED",
                        "definition_pin":dp,"instance_pin":ip,"base_definition_pin":bd,"base_instance_pin":bi,
                        "method_identities":static["method_identities"],"run_id":i["run_id"],"execution":execution,
                        "applicability":app,"observed":observed,"data_identities":(native.get("result") or {}).get("graph",{}).get("data_bindings",{}),"observed_verdict":status,"diagnostic":reason,
                        "kind":"COMPUTED_NATIVE_RECEIPT","independence":"UNVERIFIED","scope":"FINITE_DECLARED_SUPPORT"}
                record={"id":"evidence:"+digest(record),**record}
                evidences.append(record)
            if (status in ("PASS","FAIL") and any(z["verdict"]!=status for z in c)) or len({z["verdict"] for z in c})>1:
                status="INCONCLUSIVE";reason={"reason":"CONFLICTING_DECLARED_EVIDENCE"}
        result[k]={"execution":execution,"verdict":status,"applicability":app,"diagnostic":reason,
                   "computed_evidence":None if record is None else record["id"],"declared_evidence":[z["id"] for z in c]}
    assessments={}
    for k,r in sorted(req.items()):
        linked=[result[t] for t,v in tests.items() if k in v["requirements"]]
        statuses={x["verdict"] for x in linked}
        if "FAIL" in statuses:status="FAIL"
        elif "INCONCLUSIVE" in statuses:status="INCONCLUSIVE"
        elif "BLOCKED" in statuses:status="BLOCKED"
        elif linked and all(x["applicability"]=="FALSE" for x in linked):status="NOT_APPLICABLE"
        elif linked and all(x["verdict"]=="PASS" or x["applicability"]=="FALSE" for x in linked):status="PASS"
        else:status="NOT_EXECUTED"
        assessments[k]={"status":status,"test_refs":sorted(t for t,v in tests.items() if k in v["requirements"]),"required":r["required"],"scope":"FINITE_ONLY"}
    outputs=(native.get("result") or {}).get("graph",{}).get("outputs",{})
    study_metrics={k:{"output":m["target"],"value":outputs.get(m["target"]),"status":"COMPUTED_NOT_VALIDATED" if m["target"] in outputs else "NOT_EXECUTED"} for k,m in sorted(met.items()) if m["role"]=="STUDY"}
    return {"schema":PACKAGE,"definition_semantic_identity":semantic,"definition_pin":dp,"instance_pin":ip,
            "native_receipt":native,"study_metrics":study_metrics,"tests":result,"requirements":assessments,"evidence":evidences,
            "declared_evidence":list(claims.values()),"contract_conformance":"NOT_PROVED","owner":"OWNER_TBD"}

def export(d,dp,i,ip):
    return canon({"schema":PACKAGE,"definition":d,"instance":i,"receipt":instantiate(d,dp,i,ip)})

def reimport(text,dp,ip):
    from closure import c1
    x=c1.parse(text)
    fields(x,("schema","definition","instance","receipt"),"C5_PACKAGE_FIELDS")
    need(x["schema"]==PACKAGE and export(x["definition"],dp,x["instance"],ip)==text,"C5_CANONICAL_TAMPER")
    return x

def evaluate_source(raw,syntax,source_pin,dp,ip):
    need(type(raw) is bytes and sha256(raw).hexdigest()==source_pin,"C5_SOURCE_PIN")
    x=decode(raw,syntax)
    text=export(x["definition"],dp,x["instance"],ip)
    r=reimport(text,dp,ip)["receipt"]
    return {"receipt":r,"package_sha256":sha256(text.encode()).hexdigest(),"source_sha256":source_pin,
            "audit_identity":digest({"source":source_pin,"syntax":syntax,"definition":dp,"instance":ip,"canonical":sha256(text.encode()).hexdigest()})}
