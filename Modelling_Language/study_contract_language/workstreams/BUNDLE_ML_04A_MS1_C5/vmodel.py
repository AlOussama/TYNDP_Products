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
from closure_v1.obligations import Bound
from closure_v1 import composition
import mathspec.program as mp
from interface import resolve_predicate
import r1_semantics as r1

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
    need(d["schema"] in (DEF,r1.DEF) and digest(d)==dp,"C5_DEFINITION_PIN")
    advanced=d["schema"]==r1.DEF
    b=d["base"]; bd=digest(b); static=definition.admit(b,bd)
    tabs=md.validate(b["frame"])
    source={r["id"]:r for r in b["sources"]}
    targs=targets(b)
    if advanced:targs=r1.extra_targets(b,targs)
    req=index(d["requirements"],("id","version","level","statement","source_ref","source_kind","authority_ref","scope","required","parents","targets","metric_refs")+(("normativity","refinement_policy","depends_on") if advanced else ()),"C5_REQUIREMENT")
    met=index(d["metrics"],("id","version","role","meaning","target","source_ref"),"C5_METRIC")
    tests=index(d["tests"],("id","version","kind","objective","requirements","metric","criterion","scope","oracle_ref","method","coverage","evidence")+(("input_refs","preconditions","procedure_ref","reviewer_refs","applicability") if advanced else ()),"C5_TEST")
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
        if advanced:
            need(all(r1.contains(tabs,r["scope"],targs[t]["scope"]) for t in r["targets"]),"R1_TARGET_SCOPE")
            r1.validate_requirement(req,tabs,r)
        else:
            need(all(targs[t]["scope"] in (None,r["scope"]) for t in r["targets"]),"C5_TARGET_SCOPE")
            need(all(req[p]["scope"]==r["scope"] for p in r["parents"]),"C5_REFINEMENT_SCOPE")
    # Directed derivation is a DAG; every system requirement reaches a study requirement.
    def visit(k,path):
        need(k not in path,"C5_DERIVATION_CYCLE")
        for p in req[k]["parents"]:visit(p,path|{k})
    for k in req:visit(k,set())
    if advanced:r1.validate_dependencies(req)
    for k,m in met.items():
        need(nonempty(m["meaning"]) and m["source_ref"] in source and m["target"] in targs,"C5_METRIC_REFERENCE")
        kind=targs[m["target"]]["kind"]
        allowed={("STUDY","OUTPUT"),("VERIFICATION","ASSERTION"),("VERIFICATION","COMPARISON"),("VERIFICATION","OUTPUT"),("VALIDATION","REPORT")}
        if advanced:allowed|={("VERIFICATION",x) for x in ("POLICY","STATE","DATA_QUALITY","REPORT")}
        need((m["role"],kind) in allowed,"C5_METRIC_ROLE")
    coverage={k:set() for k in req}
    for k,t in tests.items():
        refs(t["requirements"],req,"C5_TEST_REQUIREMENTS")
        need(nonempty(t["objective"]) and t["metric"] in met and t["oracle_ref"] in source and t["scope"] in tabs["scopes"],"C5_TEST_REFERENCE")
        m=met[t["metric"]];need(t["criterion"] in targs,"C5_CRITERION_REFERENCE");target=targs[t["criterion"]]
        metric_target=targs[m["target"]]
        if advanced:
            r1.validate_test(t,target,m,metric_target,b,tabs,source,targs)
            if metric_target["kind"]=="OUTPUT":
                need(target["kind"]=="ASSERTION" and r1.criterion_depends(b,tabs,metric_target,target),"R1_METRIC_CRITERION_DEPENDENCY")
            else:need(t["criterion"]==m["target"],"C5_METRIC_CRITERION_BINDING")
        else:need(t["coverage"]==("ALL_DECLARED_SUPPORT" if t["kind"]=="VERIFICATION" else "EXTERNAL_SCOPE"),"C5_COVERAGE_POLICY")
        if not advanced and metric_target["kind"]=="OUTPUT":
            need(target["kind"]=="ASSERTION" and target["slot"]==metric_target["slot"],"C5_METRIC_CRITERION_BINDING")
            row=next(z for z in b["slots"] if z["id"]==target["slot"])
            symbols=[k for k,v in row["bindings"].items() if v["kind"]=="OUTPUT" and v["ref"]==m["target"]]
            p=resolve_predicate(row["package"],target["record"]["predicate"])
            # required_symbols reports underlying parameter reads; a derived output
            # is represented as ExpressionReference in the public native Program.
            bound=Bound(row["package"],tabs,None)
            def reads_output(cond,name):
                if isinstance(cond,mp.ExpressionComparison):
                    return any(isinstance(n,mp.ExpressionReference) and n.name==name
                               for n in mp.walk(cond.left,cond.right))
                return any(reads_output(child,name) for child in mp.condition_children(cond))
            root=bound.program.conditions[p["native_name"]].condition.root
            need(len(symbols)==1 and reads_output(root,bound.symbols[symbols[0]]["native_name"]),"C5_METRIC_CRITERION_DEPENDENCY")
        elif not advanced:need(t["criterion"]==m["target"],"C5_METRIC_CRITERION_BINDING")
        if not advanced:need(t["evidence"]=="COMPUTED_NATIVE_RECEIPT" if t["kind"]=="VERIFICATION" else t["evidence"]=="EXTERNAL_REVIEW_RECEIPT","C5_TEST_EVIDENCE_ROLE")
        methods={("VERIFICATION","VERIFICATION","ASSERTION","NATIVE_ASSERTION"),
            ("VERIFICATION","VERIFICATION","COMPARISON","NATIVE_COMPARISON"),
            ("VALIDATION","VALIDATION","REPORT","EXTERNAL_REVIEW")}
        if advanced:methods|={("VERIFICATION","VERIFICATION",k,meth) for k,meth in (("POLICY","NATIVE_POLICY"),("STATE","NATIVE_STATE"),("DATA_QUALITY","NATIVE_DATA_QUALITY"),("REPORT","EXTERNAL_PROCEDURE"),("REPORT","EXTERNAL_REVIEW"))}|{("VALIDATION","VALIDATION","REPORT","EXTERNAL_PROCEDURE")}
        need((t["kind"],m["role"],target["kind"],t["method"]) in methods,"C5_TEST_METHOD")
        need(target["scope"] in (None,t["scope"]),"C5_TEST_SCOPE")
        for r in t["requirements"]:
            a=req[r]
            need((r1.contains(tabs,a["scope"],t["scope"]) if advanced else a["scope"]==t["scope"]) and ((a["level"]=="SYSTEM" and t["kind"]=="VERIFICATION") or (a["level"]=="STUDY" and t["kind"]=="VALIDATION")),"C5_TEST_LEVEL_SCOPE")
            need(t["criterion"] in a["targets"] and m["id"] in a["metric_refs"],"C5_TEST_TARGET")
            coverage[r].add(t["criterion"])
    for k,r in req.items():
        if r["required"]:
            need(bool(r["targets"]) and coverage[k]==set(r["targets"]),"C5_REQUIREMENT_TEST_COVERAGE")
    # No orphan verification/validation metric or test.
    need({t["metric"] for t in tests.values()}=={k for k,m in met.items() if m["role"]!="STUDY"},"C5_METRIC_TEST_COVERAGE")
    if advanced:r1.mandatory_coverage(req,met,tests,targs,tabs)
    sem={"schema":d["schema"],"base_semantic":static["semantic_identity"],
         "requirements":[{**r,"parents":sorted(r["parents"]),"targets":sorted(r["targets"]),"metric_refs":sorted(r["metric_refs"]),**({"depends_on":sorted(r["depends_on"])} if advanced else {})} for _,r in sorted(req.items())],
         "metrics":[r for _,r in sorted(met.items())],
         "tests":[{**r,"requirements":sorted(r["requirements"]),**({k:sorted(r[k]) for k in ("input_refs","preconditions","reviewer_refs")} if advanced else {})} for _,r in sorted(tests.items())]}
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
    advanced=d["schema"]==r1.DEF
    tabs=md.validate(d["base"]["frame"]) if advanced else None
    fields(i,("schema","definition_ref","base","requested_tests","run_id","claims")+(("attestations",) if advanced else ()),"C5_INSTANCE_FIELDS")
    need(i["schema"]==(r1.INST if advanced else INST) and digest(i)==ip and i["definition_ref"]==semantic,"C5_INSTANCE_PIN")
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
    if advanced:r1.validate_evidence_ids(d,i,targs)
    verified=r1.verify_attestations(d,dp,i,static,tests,tabs,native) if advanced else {}
    result={};evidences=[]
    for k,t in sorted(tests.items()):
        m=met[t["metric"]];target=targs[t["criterion"]];record=None
        c=[r for r in claims.values() if r["test"]==k]
        if k not in i["requested_tests"]:
            status,app,execution="NOT_EXECUTED","UNKNOWN","NOT_EXECUTED";reason={"reason":"TEST_NOT_REQUESTED"}
        else:
            applicability=r1.test_applicability(t,base,b,tabs,native) if advanced else None
            if advanced and applicability["truth"]!="TRUE":
                app=applicability["truth"];status="NOT_EXECUTED" if app=="FALSE" else "INCONCLUSIVE"
                observed={"test_applicability":applicability};reason={"reason":"R1_TEST_NOT_APPLICABLE" if app=="FALSE" else "R1_TEST_APPLICABILITY_UNKNOWN"}
            elif advanced and any(x!="TRUE" for x in r1.preconditions(t,native).values()):
                status,app,observed,reason="BLOCKED","UNKNOWN",{"preconditions":r1.preconditions(t,native)},{"reason":"R1_PRECONDITION_UNSATISFIED_OR_UNKNOWN"}
            elif advanced and t["method"] in r1.EXTERNAL:
                status,app,observed,reason=r1.external_result(t,verified,native)
            elif advanced and target["kind"] in ("POLICY","STATE","DATA_QUALITY"):
                status,app,observed,reason=r1.native_extra_result(target,native)
            else:
                status,app,observed,reason=result_for(t,target,native,base,b)
                if advanced and target["kind"]=="ASSERTION":
                    status,app,observed,reason=r1.improve_assertion(status,app,observed,reason,base,b,tabs,target,native)
            if advanced:observed["test_applicability"]=applicability
            if targs[m["target"]]["kind"]=="OUTPUT":
                observed["metric_value"]=(native.get("result") or {}).get("graph",{}).get("outputs",{}).get(m["target"])
                if status=="PASS" and observed["metric_value"] is None:status="BLOCKED";reason={"reason":"MISSING_METRIC_OUTPUT"}
            execution=("BLOCKED" if status=="BLOCKED" else "NOT_EXECUTED" if status=="NOT_EXECUTED" else "EXECUTED") if advanced else ("NOT_EXECUTED" if t["kind"]=="VALIDATION" else "BLOCKED" if status=="BLOCKED" else "EXECUTED")
            if (t["kind"]=="VERIFICATION" and (not advanced or t["method"] not in r1.EXTERNAL)) or (advanced and observed.get("verified_attestations")):
                record={"test":k,"test_version":t["version"],"requirement_refs":sorted(t["requirements"]),
                        "metric":m["id"],"metric_version":m["version"],"oracle_ref":t["oracle_ref"],"subject":t["criterion"],"metric_target":m["target"],"expected":"DECLARED_CRITERION_SATISFIED",
                        "definition_pin":dp,"instance_pin":ip,"base_definition_pin":bd,"base_instance_pin":bi,
                        "method_identities":static["method_identities"],"run_id":i["run_id"],"execution":execution,
                        "applicability":app,"observed":observed,"data_identities":(native.get("result") or {}).get("graph",{}).get("data_bindings",{}),"observed_verdict":status,"diagnostic":reason,
                        "kind":("VERIFIED_PINNED_EXTERNAL_ATTESTATION" if advanced and t["method"] in r1.EXTERNAL else "COMPUTED_NATIVE_RECEIPT"),"independence":"UNVERIFIED","scope":"FINITE_DECLARED_SUPPORT"}
                if advanced:record["input_identities"]=r1.native_inputs(t,native);record["procedure_ref"]=t["procedure_ref"];record["coverage_policy"]=t["coverage"]
                record={"id":"evidence:"+digest(record),**record}
                evidences.append(record)
            if (status in ("PASS","FAIL") and any(z["verdict"]!=status for z in c)) or len({z["verdict"] for z in c})>1:
                # Preserve an actually observed counterexample in R1; untrusted
                # contradictory declarations may not erase it.
                if advanced and status=="FAIL":reason={"reason":"COUNTEREXAMPLE_WITH_CONFLICTING_DECLARED_EVIDENCE"}
                else:
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
    if advanced:r1.aggregate_children(req,assessments)
    outputs=(native.get("result") or {}).get("graph",{}).get("outputs",{})
    study_metrics={k:{"output":m["target"],"value":outputs.get(m["target"]),"status":"COMPUTED_NOT_VALIDATED" if m["target"] in outputs else "NOT_EXECUTED"} for k,m in sorted(met.items()) if m["role"]=="STUDY"}
    if advanced:
        for k,r in study_metrics.items():
            linked=[z for z in req.values() if k in z["metric_refs"] and z["level"]=="STUDY" and z["required"]]
            r["validation_assessments"]={z["id"]:assessments[z["id"]]["status"] for z in linked}
            validated=all(any(z["id"] in t["requirements"] and t["kind"]=="VALIDATION" and r["output"] in t["input_refs"] and result[t["id"]]["verdict"]=="PASS" and result[t["id"]]["computed_evidence"] is not None for t in tests.values()) for z in linked)
            r["status"]="COMPUTED_WITH_PINNED_VALIDATION_ATTESTATION" if r["value"] is not None and linked and validated and all(assessments[z["id"]]["status"]=="PASS" for z in linked) else r["status"]
    return {"schema":r1.PACKAGE if advanced else PACKAGE,"definition_semantic_identity":semantic,"definition_pin":dp,"instance_pin":ip,
            "native_receipt":native,"study_metrics":study_metrics,"tests":result,"requirements":assessments,"evidence":evidences,
            "declared_evidence":list(claims.values()),"contract_conformance":"NOT_PROVED","owner":"OWNER_TBD"}

def export(d,dp,i,ip):
    return canon({"schema":r1.PACKAGE if d["schema"]==r1.DEF else PACKAGE,"definition":d,"instance":i,"receipt":instantiate(d,dp,i,ip)})

def reimport(text,dp,ip):
    from closure import c1
    x=c1.parse(text)
    fields(x,("schema","definition","instance","receipt"),"C5_PACKAGE_FIELDS")
    need(x["schema"] in (PACKAGE,r1.PACKAGE) and export(x["definition"],dp,x["instance"],ip)==text,"C5_CANONICAL_TAMPER")
    return x

def evaluate_source(raw,syntax,source_pin,dp,ip):
    need(type(raw) is bytes and sha256(raw).hexdigest()==source_pin,"C5_SOURCE_PIN")
    x=decode(raw,syntax)
    text=export(x["definition"],dp,x["instance"],ip)
    r=reimport(text,dp,ip)["receipt"]
    return {"receipt":r,"package_sha256":sha256(text.encode()).hexdigest(),"source_sha256":source_pin,
            "audit_identity":digest({"source":source_pin,"syntax":syntax,"definition":dp,"instance":ip,"canonical":sha256(text.encode()).hexdigest()})}

def compose_method(d,dp,request,request_pin,authorization,authorization_pin):
    """Explicit approved research replacement; no implicit authorization.
    Existing external test design remains immutable; new definition and evidence roots required."""
    old=admit(d,dp)
    receipt=composition.compose(d["base"],digest(d["base"]),request,request_pin,authorization,authorization_pin)
    effective=deepcopy(d);effective["base"]=receipt["effective_definition"]
    new=admit(effective,digest(effective))
    return {"definition":effective,"definition_pin":digest(effective),
            "old_semantic_identity":old["semantic_identity"],"semantic_identity":new["semantic_identity"],
            "composition_receipt":receipt,"retained_requirements":sorted(r["id"] for r in d["requirements"]),
            "retained_tests":sorted(t["id"] for t in d["tests"]),"evidence_policy":"REEXECUTE_NEW_ROOT",
            "owner":"OWNER_TBD","conformance":"NOT_PROVED"}

def migrate_r1(d,dp,i,ip,reviewer_sources,normativity_by_id=None):
    """Explicit wire migration, not proof of approval or lossless satisfaction.
    Add independent reviewer key sources explicitly; invalidate all old claims.
    """
    old=instantiate(d,dp,i,ip)
    need(d["schema"]==DEF and i["schema"]==INST,"R1_MIGRATION_VERSION")
    nd,ni=deepcopy(d),deepcopy(i);nd["schema"]=r1.DEF;ni["schema"]=r1.INST
    base=nd["base"];f=base["frame"]
    for s in reviewer_sources:
        need(s["id"] not in {x["id"] for x in base["sources"]},"R1_MIGRATION_REVIEWER_ID")
        base["sources"].append(deepcopy(s))
        f["authorities"].append({"id":s["id"],"role":"PROVENANCE","immutable_ref":s["immutable_ref"],"revision":s["revision"],"decision_state":"OWNER_TBD"})
    ts=r1.extra_targets(base,targets(base))
    normativity_by_id=normativity_by_id or {}
    need(set(normativity_by_id)<= {r["id"] for r in nd["requirements"]},"R1_MIGRATION_NORMATIVITY_REFERENCE")
    for req in nd["requirements"]:
        need(req["source_kind"]!="ORIGINAL_SOURCE" or req["id"] in normativity_by_id,"R1_MIGRATION_NORMATIVITY_REQUIRED")
        req.update(normativity=normativity_by_id.get(req["id"],"RESEARCH_ASSUMPTION"),refinement_policy="DIRECT_AND_CHILDREN",depends_on=[])
    for t in nd["tests"]:
        target=ts[t["criterion"]]
        inputs=r1.input_population(base,target)
        if inputs is None:
            inputs={m["target"] for m in nd["metrics"] if m["role"]=="STUDY" and any(m["id"] in req["metric_refs"] for req in nd["requirements"] if req["id"] in t["requirements"])}
        t.update(input_refs=sorted(inputs),preconditions=[],procedure_ref=t["oracle_ref"],reviewer_refs=[s["id"] for s in reviewer_sources] if t["method"] in r1.EXTERNAL else [],applicability={"slot":None,"guard":{"truth":"TRUE","reason":None}})
    ni["base"]["definition_ref"]=definition.admit(base,digest(base))["semantic_identity"]
    ni["definition_ref"]=admit(nd,digest(nd))["semantic_identity"]
    ni["claims"]=[];ni["attestations"]=[]
    return nd,ni,{"previous_definition_pin":dp,"previous_instance_pin":ip,"previous_receipt_sha256":digest(old),"definition_pin":digest(nd),"instance_pin":digest(ni),"discarded_claim_ids":[x["id"] for x in i["claims"]],"policy":"EXPLICIT_REAUTHOR_AND_REEXECUTE","owner":"OWNER_TBD"}

def revise_requirements(old,old_pin,proposed,proposed_pin,authorization,authorization_pin):
    """Research-only revision against an externally pinned prior definition.
    Direct authoring remains a new baseline, not an authorized history transition.
    C4 base is immutable here: native method exchange uses compose_method.
    """
    before=admit(old,old_pin);after=admit(proposed,proposed_pin)
    need(old["schema"]==proposed["schema"]==r1.DEF and old["base"]==proposed["base"],"R1_REVISION_BASE_DRIFT")
    changes=r1.revision_changes(old,proposed)
    fields(authorization,("schema","base_ref","proposed_ref","changes","authority_ref","source_sha256","decision","reason"),"R1_REVISION_AUTHORIZATION_FIELDS")
    need(digest(authorization)==authorization_pin and authorization["schema"]=="c5-r1-revision-authorization-0.1" and authorization["base_ref"]==old_pin and authorization["proposed_ref"]==proposed_pin and authorization["decision"]=="APPROVED_RESEARCH_REVISION" and nonempty(authorization["reason"]),"R1_REVISION_AUTHORIZATION")
    need(authorization["changes"]==changes and bool(changes),"R1_REVISION_CHANGE_SET")
    src={r["id"]:r for r in old["base"]["sources"]};a=authorization["authority_ref"]
    need(a in src and src[a]["sha256"]==authorization["source_sha256"],"R1_REVISION_AUTHORITY")
    for ch in changes:
        for d in (old,proposed):
            rows={r["id"]:r for r in d[ch["collection"]]}
            if ch["id"] in rows:
                r=rows[ch["id"]];ref=r.get("authority_ref",r.get("source_ref",r.get("oracle_ref")))
                need(ref==a,"R1_REVISION_AUTHORITY_SCOPE")
    return {"schema":"c5-r1-revision-receipt-0.1","base_ref":old_pin,"proposed_ref":proposed_pin,"authorization_pin":authorization_pin,"changes":changes,
            "old_semantic_identity":before["semantic_identity"],"semantic_identity":after["semantic_identity"],"evidence_policy":"REEXECUTE_NEW_ROOT","owner":"OWNER_TBD","conformance":"NOT_PROVED"}
