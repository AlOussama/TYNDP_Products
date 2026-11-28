"""C5-R1 semantic services. Reuse pinned C4 public native Program and
obligation evaluator. No new mathematical syntax, AST, or evaluator.
External attestations verify exact bytes under a definition-pinned key;
they never establish real-world reviewer independence or owner approval.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,base64,binascii
import mathspec.program as mp
from closure import digest,canon,need,fields,qualified
from closure_v1 import obligations as ob
from interface import resolve_predicate

DEF="c5-vmodel-definition-0.2"
INST="c5-vmodel-instance-0.2"
PACKAGE="c5-vmodel-package-0.2"
EXTERNAL=("EXTERNAL_REVIEW","EXTERNAL_PROCEDURE")
NATIVE=("NATIVE_ASSERTION","NATIVE_COMPARISON","NATIVE_POLICY","NATIVE_STATE","NATIVE_DATA_QUALITY")
MAX_POINT_REPLAYS=10000

def contains(tabs,parent,child):
    if child is None:return True
    p,c=tabs["scopes"][parent],tabs["scopes"][child]
    # Axes are dimensions, not nested sets of coordinates. Dropping axes
    # is projection, not refinement. Subject containment on equal axes is safe.
    return set(p["domains"])==set(c["domains"]) and set(c["subjects"])<=set(p["subjects"])

def scope_signature(tabs,scope):
    s=tabs["scopes"][scope]
    return {"domains":{a:list(tabs["domains"][a]["members"]) if tabs["domains"][a]["ordered"] else sorted(tabs["domains"][a]["members"]) for a in sorted(s["domains"])},
            "subjects":sorted(s["subjects"])}

def validate_requirement(req,tabs,r):
    need(r["normativity"] in ("RESEARCH_ASSUMPTION","INFORMATIVE","NORMATIVE_REQUIREMENT_PENDING_OWNER"),"R1_REQUIREMENT_NORMATIVITY")
    need(not(r["required"] and r["normativity"]=="INFORMATIVE"),"R1_INFORMATIVE_REQUIRED")
    need(r["refinement_policy"] in ("DIRECT_AND_CHILDREN","COMPLETE_SUBJECT_COVERAGE"),"R1_REFINEMENT_POLICY")
    for p in r["parents"]:
        need(contains(tabs,req[p]["scope"],r["scope"]),"R1_REFINEMENT_SCOPE")
    if r["refinement_policy"]=="COMPLETE_SUBJECT_COVERAGE":
        children=[x for x in req.values() if r["id"] in x["parents"] and x["required"]]
        need(bool(children) and set().union(*(set(tabs["scopes"][x["scope"]]["subjects"]) for x in children))==set(tabs["scopes"][r["scope"]]["subjects"]),"R1_DECOMPOSITION_COVERAGE")

def extra_targets(base,targs):
    f=base["frame"]
    ss={s["id"]:s["scope"] for s in f["slots"]}
    for slot in base["slots"]:
        for collection,kind in (("policies","POLICY"),("states","STATE")):
            for a in slot[collection]:
                targs[a["id"]]={"kind":kind,"scope":ss[slot["id"]],"slot":slot["id"],"record":a}
    # A data contract shares its identity with the declared input/observable.
    # No new parallel object is introduced. Data quality tests consume the
    # actual C4 quality receipt, not a second quality predicate.
    for a in base["requirements"]["data_contracts"]:
        targs[a["id"]]={"kind":"DATA_QUALITY","scope":None,"slot":None,"record":a}
    return targs

def criterion_depends(base,tabs,metric_target,criterion):
    """Read native reference/dependency graph; never compare formula text.
    For cross-slot use the existing typed UPSTREAM binding, recursively.
    """
    rows={r["id"]:r for r in base["slots"]}
    outputs={b["ref"]:(r["id"],k) for r in rows.values() for k,b in r["bindings"].items() if b["kind"]=="OUTPUT"}
    memo={}
    def bound(s):
        if s not in memo:memo[s]=ob.Bound(rows[s]["package"],tabs,None)
        return memo[s]
    wanted=metric_target["record"]["id"]
    def expression_reads(s,expr,seen):
        bd=bound(s)
        for node in mp.walk(expr):
            if isinstance(node,mp.ExpressionReference):
                ref=next((k for k,x in bd.symbols.items() if x["native_name"]==node.name),None)
                if ref is not None and rows[s]["bindings"][ref]=={"kind":"OUTPUT","ref":wanted}:return True
            if isinstance(node,mp.ParameterReference) and parameter_reads(s,node.name,seen):return True
        return False
    def parameter_reads(s,name,seen):
        bd=bound(s);ref=next((k for k,x in bd.symbols.items() if x["native_name"]==name),None)
        if ref is None:return False
        b=rows[s]["bindings"][ref]
        if b["kind"]!="UPSTREAM":return False
        out=b["ref"]
        if out==wanted:return True
        if out in seen or out not in outputs:return False
        prev,sym=outputs[out];pr=bound(prev)
        return expression_reads(prev,pr.program.expressions[pr.symbols[sym]["native_name"]].expression,seen|{out})
    def condition_reads(s,cond):
        if isinstance(cond,mp.ExpressionComparison):
            return expression_reads(s,cond.left,set()) or expression_reads(s,cond.right,set())
        if isinstance(cond,(mp.ParameterComparison,mp.ParameterDefined)):
            return parameter_reads(s,cond.name,set())
        return any(condition_reads(s,c) for c in mp.condition_children(cond))
    s=criterion["slot"];bd=bound(s)
    p=resolve_predicate(rows[s]["package"],criterion["record"]["predicate"])
    return condition_reads(s,bd.program.conditions[p["native_name"]].condition.root)

def input_population(base,target):
    f=base["frame"]
    if target["kind"]=="DATA_QUALITY":return {target["record"]["id"]}
    if target["slot"] is None:return None
    s=next(r for r in f["slots"] if r["id"]==target["slot"])
    out=set(s["inputs"]+s["observables"])
    if target["kind"]=="COMPARISON":
        for pair in [*target["record"]["exogenous"].values(),*target["record"]["project"].values()]:
            out.update(pair.values())
    if target["kind"]=="DATA_QUALITY":out.add(target["record"]["id"])
    return out

def key_fingerprint(text):
    need(type(text) is str and len(text)<=8192,"R1_REVIEWER_PUBLIC_KEY")
    lines=text.strip().splitlines()
    need(len(lines)>=3 and lines[0]=="-----BEGIN PUBLIC KEY-----" and lines[-1]=="-----END PUBLIC KEY-----","R1_REVIEWER_PUBLIC_KEY")
    try:der=base64.b64decode("".join(lines[1:-1]),validate=True)
    except (ValueError,binascii.Error):need(False,"R1_REVIEWER_PUBLIC_KEY")
    need(len(der)==44 and der.startswith(bytes.fromhex("302a300506032b6570032100")),"R1_REVIEWER_ED25519_KEY")
    return sha256(der).hexdigest()

def validate_test(t,target,m,metric_target,base,tabs,source,targs):
    refs=lambda xs,universe: type(xs) is list and all(type(x) is str and x in universe for x in xs) and len(xs)==len(set(xs))
    universe={x["id"] for n in ("inputs","observables","outputs","context_fields") for x in base["frame"][n]}
    need(refs(t["input_refs"],universe),"R1_TEST_INPUT_REFERENCE")
    need(refs(t["preconditions"],{k for k,x in targs.items() if x["kind"]=="ASSERTION"}),"R1_PRECONDITION_REFERENCE")
    need(all(contains(tabs,targs[x]["scope"],t["scope"]) for x in t["preconditions"]),"R1_PRECONDITION_SCOPE")
    need(t["criterion"] not in t["preconditions"],"R1_SELF_PRECONDITION")
    need(t["procedure_ref"] in source,"R1_PROCEDURE_REFERENCE")
    app_inputs=validate_applicability(t,base,tabs)
    if target["kind"]=="DATA_QUALITY":
        k=target["record"]["id"];records={x["id"]:x for c in ("inputs","observables","context_fields") for x in base["frame"][c]}
        record=records[k];scope=tabs["scopes"][t["scope"]]
        need(set(record["axes"])<=set(scope["domains"]) and ("subject" not in record or record["subject"] in scope["subjects"]),"R1_DATA_TEST_SCOPE")
    if t["method"] in NATIVE:
        wanted=input_population(base,target)
        need(wanted is not None,"R1_TEST_INPUT_COVERAGE")
        wanted.update(x for p in t["preconditions"] for x in input_population(base,targs[p]));wanted.update(app_inputs)
        need(set(t["input_refs"])==wanted,"R1_TEST_INPUT_COVERAGE")
        need(not t["reviewer_refs"],"R1_NATIVE_REVIEWER")
        need(t["coverage"]=="ALL_DECLARED_SUPPORT" and t["evidence"]=="COMPUTED_NATIVE_RECEIPT","R1_NATIVE_EVIDENCE_ROLE")
    else:
        need(t["method"] in EXTERNAL and target["kind"]=="REPORT","R1_EXTERNAL_METHOD_TARGET")
        need(app_inputs|{x for p in t["preconditions"] for x in input_population(base,targs[p])}<=set(t["input_refs"]),"R1_EXTERNAL_PREREQUISITE_INPUTS")
        need(t["coverage"] in ("EXTERNAL_SCOPE","ALL_DECLARED_SUPPORT") and t["evidence"]=="EXTERNAL_REVIEW_RECEIPT","R1_EXTERNAL_EVIDENCE_ROLE")
        need(refs(t["reviewer_refs"],source) and bool(t["reviewer_refs"]),"R1_REVIEWER_REFERENCE")
        # A separate pinned key, not the method source, oracle or model source.
        forbidden={t["oracle_ref"],t["procedure_ref"],*([s["source_ref"] for s in base["slots"]]),*([x["source_ref"] for x in base["requirements"]["models"]])}
        need(not set(t["reviewer_refs"])&forbidden,"R1_REVIEWER_ROLE_COLLISION")
        need(target["record"]["oracle_ref"]==t["oracle_ref"],"R1_REPORT_ORACLE")
        need(target["record"]["subject"]==base["frame"]["id"] or target["record"]["subject"] in tabs["scopes"][t["scope"]]["subjects"],"R1_REPORT_SCOPE")
        fingerprints=[]
        for r in t["reviewer_refs"]:
            need(tabs["authorities"][r]["role"]=="PROVENANCE","R1_REVIEWER_AUTHORITY_ROLE")
            fingerprints.append(key_fingerprint(source[r]["content"]))
        need(len(fingerprints)==len(set(fingerprints)),"R1_DUPLICATE_REVIEWER_KEY")
    need(target["scope"] is None or t["scope"]==target["scope"],"R1_TEST_TARGET_SCOPE")

def mandatory_coverage(req,met,tests,targs,tabs):
    for k,r in req.items():
        linked=[t for t in tests.values() if k in t["requirements"]]
        if not r["required"]:continue
        nonstudy={x for x in r["metric_refs"] if met[x]["role"]!="STUDY"}
        need({t["metric"] for t in linked}==nonstudy,"R1_REQUIREMENT_METRIC_COVERAGE")
        study_targets={met[x]["target"] for x in r["metric_refs"] if met[x]["role"]=="STUDY"}
        need(all(contains(tabs,r["scope"],targs[x]["scope"]) for x in study_targets),"R1_STUDY_METRIC_SCOPE")
        need(study_targets<=set().union(*(set(t["input_refs"]) for t in linked)),"R1_STUDY_METRIC_VALIDATION_COVERAGE")
        # Each mandatory requirement scope must be covered by its declared tests,
        # not merely by their IDs. A report test binds its own explicit scope.
        need(set().union(*(set(tabs["scopes"][t["scope"]]["subjects"]) for t in linked))==set(tabs["scopes"][r["scope"]]["subjects"]),"R1_REQUIREMENT_SUBJECT_COVERAGE")
    used={m for r in req.values() for m in r["metric_refs"]}
    need(used==set(met),"R1_ORPHAN_METRIC")

def graph_of(native):
    return (native.get("result") or {}).get("graph",{})

def native_inputs(t,native):
    g=graph_of(native)
    values=dict(g.get("data_bindings",{}))
    values.update({k:digest(v) for k,v in g.get("outputs",{}).items()})
    return {k:values[k] for k in sorted(t["input_refs"]) if k in values}

def preconditions(t,native):
    g=graph_of(native)
    actual={a["id"]:a for slot in g.get("slots",{}).values() for a in slot["obligations"]["assertions"]}
    return {k:actual[k]["truth"] if k in actual else "UNKNOWN" for k in t["preconditions"]}

def verify_signature(public,payload,signature):
    need(type(signature) is str and len(signature)==128 and all(x in "0123456789abcdef" for x in signature),"R1_SIGNATURE_ENCODING")
    with TemporaryDirectory() as tmp:
        p=Path(tmp);(p/"key.pem").write_text(public,encoding="utf-8")
        (p/"message").write_bytes(canon(payload).encode("utf-8"));(p/"signature").write_bytes(bytes.fromhex(signature))
        # No shell and no externally supplied executable or arguments.
        proc=subprocess.run(["openssl","pkeyutl","-verify","-pubin","-inkey",str(p/"key.pem"),"-rawin","-in",str(p/"message"),"-sigfile",str(p/"signature")],capture_output=True,timeout=5)
        need(proc.returncode==0,"R1_EXTERNAL_SIGNATURE")

def verify_attestations(d,dp,i,static,tests,tabs,native):
    source={r["id"]:r for r in d["base"]["sources"]};out={}
    need(type(i["attestations"]) is list,"R1_ATTESTATION_LIST")
    ids=set();pair=set()
    for r in i["attestations"]:
        fields(r,("id","version","payload","signature"),"R1_ATTESTATION_FIELDS")
        need(qualified(r["id"]) and r["id"] not in ids and type(r["version"]) is str and bool(r["version"]),"R1_ATTESTATION_ID");ids.add(r["id"])
        p=r["payload"]
        fields(p,("test","test_version","definition_pin","base_instance_pin","run_id","reviewer_ref","method_identities","criterion","verdict","observed","artifact","artifact_sha256","coverage","data_identities"),"R1_ATTESTATION_PAYLOAD")
        need(p["test"] in tests,"R1_ATTESTATION_TEST");t=tests[p["test"]]
        need(t["method"] in EXTERNAL and p["test_version"]==t["version"] and p["criterion"]==t["criterion"] and p["reviewer_ref"] in t["reviewer_refs"],"R1_ATTESTATION_ROLE")
        need((p["test"],p["reviewer_ref"]) not in pair,"R1_DUPLICATE_REVIEWER");pair.add((p["test"],p["reviewer_ref"]))
        need(p["definition_pin"]==dp and p["base_instance_pin"]==digest(i["base"]) and p["run_id"]==i["run_id"] and p["method_identities"]==static["method_identities"],"R1_ATTESTATION_STALE")
        need(p["verdict"] in ("PASS","FAIL","INCONCLUSIVE") and type(p["observed"]) is str and bool(p["observed"].strip()),"R1_ATTESTATION_VERDICT")
        need(type(p["artifact"]) is str and 0<len(p["artifact"])<=1000000 and sha256(p["artifact"].encode()).hexdigest()==p["artifact_sha256"],"R1_ATTESTATION_ARTIFACT")
        need(p["coverage"]==scope_signature(tabs,t["scope"]),"R1_ATTESTATION_COVERAGE")
        verify_signature(source[p["reviewer_ref"]]["content"],{"id":r["id"],"version":r["version"],"payload":p},r["signature"])
        actual=native_inputs(t,native)
        need(type(p["data_identities"]) is dict and set(p["data_identities"])==set(t["input_refs"]),"R1_ATTESTATION_DATA_COVERAGE")
        if len(actual)==len(t["input_refs"]):need(p["data_identities"]==actual,"R1_ATTESTATION_DATA_DRIFT")
        out.setdefault(p["test"],[]).append({"id":r["id"],"payload":p,"signature":r["signature"],"key_source_sha256":source[p["reviewer_ref"]]["sha256"],"signature_status":"VERIFIED_PINNED_KEY","independence":"UNVERIFIED","authority":"OWNER_TBD","data_binding_complete":len(actual)==len(t["input_refs"])})
    return out

def external_result(t,verified,native):
    inputs=native_inputs(t,native)
    if not graph_of(native) or len(inputs)!=len(t["input_refs"]):
        return "BLOCKED","UNKNOWN",{},{"reason":"R1_EXTERNAL_INPUTS_MISSING"}
    rs=verified.get(t["id"],[])
    if not rs:return "NOT_EXECUTED","UNKNOWN",{},{"reason":"EXTERNAL_REVIEW_NOT_VERIFIED"}
    ev={"verified_attestations":sorted(rs,key=lambda x:x["id"])}
    if {r["payload"]["reviewer_ref"] for r in rs}!=set(t["reviewer_refs"]):
        return "BLOCKED","TRUE",ev,{"reason":"R1_REQUIRED_REVIEWERS_MISSING"}
    if not all(r["data_binding_complete"] for r in rs):
        return "BLOCKED","UNKNOWN",ev,{"reason":"R1_EXTERNAL_INPUTS_MISSING"}
    statuses={r["payload"]["verdict"] for r in rs}
    status=next(iter(statuses)) if len(statuses)==1 else "INCONCLUSIVE"
    return status,"TRUE",ev,{"reason":"R1_PINNED_EXTERNAL_ATTESTATION" if len(statuses)==1 else "R1_CONFLICTING_SIGNED_EVIDENCE"}

def native_extra_result(target,native):
    g=graph_of(native)
    if not g:return "BLOCKED","UNKNOWN",{},{"reason":"R1_NATIVE_RECEIPT_UNAVAILABLE"}
    k=target["record"]["id"];kind=target["kind"]
    if kind=="DATA_QUALITY":
        status=native["result"]["data_quality"].get(k)
        receipt={"id":k,"status":status,"data_identity":g["data_bindings"].get(k)}
        mapped={"FINITE_CHECKED":"PASS","FINITE_REJECTED":"FAIL","BLOCKED":"BLOCKED"}
    else:
        field="policies" if kind=="POLICY" else "boundaries"
        hit=[x for x in g["slots"][target["slot"]][field] if x["id"]==k]
        need(len(hit)==1,"R1_NATIVE_TARGET_RECEIPT")
        receipt=hit[0];status=receipt["status"]
        if kind=="STATE":
            # C4 boundary receipt validates binding, NOT satisfaction. Read
            # actual evaluated endpoint/cycle assertions from the same slot.
            st=target["record"];ids=[st["initial"],st["terminal"]]+([st["cycle"]["assertion"]] if st["mode"]=="CYCLIC" else [])
            actual={a["id"]:a for a in g["slots"][target["slot"]]["obligations"]["assertions"]}
            need(all(a in actual for a in ids),"R1_STATE_ASSERTION_RECEIPT")
            checks=[actual[a] for a in ids];truth=[a["truth"] for a in checks]
            receipt={"boundary_binding":receipt,"assertions":checks}
            if status!="BOUND_NATIVE_ASSERTIONS":status="BLOCKED"
            elif "FALSE" in truth:status="FINITE_COUNTEREXAMPLE"
            elif all(x=="TRUE" for x in truth):status="FINITE_OBSERVED_TRUE"
            else:status="BLOCKED"
        mapped={"FINITE_OBSERVED_TRUE":"PASS","FINITE_COUNTEREXAMPLE":"FAIL","BLOCKED":"BLOCKED","NOT_APPLICABLE":"NOT_EXECUTED"}
    return mapped.get(status,"INCONCLUSIVE"),"FALSE" if status=="NOT_APPLICABLE" else "UNKNOWN" if status in (None,"BLOCKED") else "TRUE",{"native_target":receipt},{"reason":"R1_NATIVE_TARGET_ASSESSMENT"}

def assertion_support(base,i,tabs,target,native):
    # Reuse actual C4 evaluation of one restricted coordinate at a time.
    # Only universal safety/prohibition assertions have this explicit
    # point-coverage adapter. Service semantics remain C4 request/witness folds.
    g=graph_of(native)
    if not g:return None
    a=target["record"];r=next(x for x in base["slots"] if x["id"]==target["slot"])
    ir=next(x for x in i["slots"] if x["id"]==target["slot"])
    if a["role"] not in ("SAFETY_GUARANTEE","PROHIBITED_BEHAVIOUR"):return None
    axes=[b["axis"] for b in a["binders"]];members=[tabs["domains"][ax]["members"] for ax in axes]
    count=1
    for m in members:count*=len(m)
    if count>MAX_POINT_REPLAYS:return {"complete":False,"expected":count,"reason":"R1_POINT_REPLAY_LIMIT"}
    bd=ob.Bound(r["package"],tabs,ir["data"])
    points=[]
    for key in product(*members):
        if any(ax in a["at"] and val not in a["at"][ax] for ax,val in zip(axes,key,strict=True)):
            points.append({"key":list(key),"truth":None,"reasons":["OUTSIDE_DECLARED_SCOPE"]});continue
        specs=deepcopy(r["assertions"]);z=next(x for x in specs if x["id"]==a["id"])
        z["at"]={ax:[v] for ax,v in zip(axes,key,strict=True)}
        rr=ob.evaluate(bd,specs,ir["witnesses"]);hit=next(x for x in rr["assertions"] if x["id"]==a["id"])
        points.append({"key":list(key),"truth":hit["truth"],"reasons":hit["reasons"]})
    return {"axes":axes,"expected":count,"observed":len(points),"complete":len(points)==count,
            "points":points,"applicable":sum(x["truth"] in ("TRUE","FALSE") for x in points),
            "excluded":sum(x["truth"] is None for x in points),"unknown":sum(x["truth"]=="UNKNOWN" for x in points)}

def improve_assertion(status,app,evidence,reason,base,i,tabs,target,native):
    support=assertion_support(base,i,tabs,target,native)
    if support is None:return status,app,evidence,reason
    # An observed native counterexample cannot be erased by replay limits.
    if status=="FAIL" and not support["complete"]:evidence["coverage"]=support;return status,app,evidence,reason
    evidence["coverage"]=support
    if not support["complete"]:return "INCONCLUSIVE","UNKNOWN",evidence,{"reason":"R1_INCOMPLETE_POINT_COVERAGE"}
    if any(x["truth"]=="FALSE" for x in support["points"]):return "FAIL","TRUE",evidence,{"reason":"R1_NATIVE_POINT_COUNTEREXAMPLE"}
    if support["unknown"]:return "INCONCLUSIVE","UNKNOWN",evidence,{"reason":"R1_UNKNOWN_APPLICABILITY_OR_TRUTH"}
    if not support["applicable"]:return "NOT_EXECUTED","FALSE",evidence,{"reason":"R1_ALL_COORDINATES_NOT_APPLICABLE"}
    return "PASS","TRUE",evidence,{"reason":"R1_NATIVE_ALL_APPLICABLE_POINTS_TRUE"}

def aggregate_children(req,assessments):
    """Keep local test assessment separate from derived requirement assessment.
    Required descendants must not be hidden by a parent's local PASS.
    No logical entailment or universal decomposition proof is claimed.
    """
    done=set()
    def walk(k):
        if k in done:return assessments[k]["status"]
        children=sorted(x for x,r in req.items() if k in r["parents"] and r["required"])
        statuses={x:walk(x) for x in children}
        deps={x:walk(x) for x in req[k]["depends_on"]}
        a=assessments[k];local=a["status"];a["local_status"]=local;a["child_assessments"]=statuses;a["dependency_assessments"]=deps
        all_=[local,*statuses.values()]
        if local!="NOT_APPLICABLE" and any(x!="PASS" for x in deps.values()):all_.append("BLOCKED")
        for s in ("FAIL","INCONCLUSIVE","BLOCKED","NOT_EXECUTED"):
            if s in all_:a["status"]=s;break
        else:a["status"]="NOT_APPLICABLE" if all(x=="NOT_APPLICABLE" for x in all_) else "PASS"
        done.add(k);return a["status"]
    for k in sorted(req):walk(k)
    return assessments

def validate_dependencies(req):
    # Assessment edges are parent -> required child and dependent ->
    # prerequisite. Detect cycles over the combined evaluation graph.
    for k,r in req.items():
        ds=r["depends_on"]
        need(type(ds) is list and all(type(x) is str and x in req and x!=k for x in ds) and len(ds)==len(set(ds)),"R1_REQUIREMENT_DEPENDENCY_REFERENCE")
    done=set()
    def visit(k,path):
        need(k not in path,"R1_REQUIREMENT_DEPENDENCY_CYCLE")
        if k in done:return
        children=[x for x,r in req.items() if k in r["parents"] and r["required"]]
        for x in set(children+req[k]["depends_on"]):visit(x,path|{k})
        done.add(k)
    for k in req:visit(k,set())

def validate_applicability(t,base,tabs):
    a=t["applicability"];fields(a,("slot","guard"),"R1_APPLICABILITY_FIELDS")
    g=a["guard"];need(type(g) is dict,"R1_APPLICABILITY_GUARD")
    if a["slot"] is None:
        fields(g,("truth","reason"),"R1_APPLICABILITY_CONSTANT")
        need(g["truth"] in ob.TRUTH and (g["reason"] in ob.UNKNOWN_REASONS if g["truth"]=="UNKNOWN" else g["reason"] is None),"R1_APPLICABILITY_REASON")
        return set()
    slots={x["id"]:x for x in base["slots"]};need(a["slot"] in slots,"R1_APPLICABILITY_SLOT")
    f=next(x for x in base["frame"]["slots"] if x["id"]==a["slot"])
    need(contains(tabs,f["scope"],t["scope"]),"R1_APPLICABILITY_SCOPE")
    bd=ob.Bound(slots[a["slot"]]["package"],tabs,None)
    bd.guard_refs(g,set(tabs["scopes"][t["scope"]]["domains"]))
    return set(f["inputs"]+f["observables"])

def test_applicability(t,base,i,tabs,native):
    a=t["applicability"];g=a["guard"]
    if a["slot"] is None:return {"truth":g["truth"],"reason":g["reason"],"source":"DECLARED_CONSTANT"}
    if not graph_of(native):return {"truth":"UNKNOWN","reason":"MISSING_NATIVE_RECEIPT"}
    row=next(x for x in base["slots"] if x["id"]==a["slot"])
    ir=next(x for x in i["slots"] if x["id"]==a["slot"])
    bd=ob.Bound(row["package"],tabs,ir["data"])
    axes=sorted(bd.guard_refs(g,set(tabs["scopes"][t["scope"]]["domains"])))
    count=1
    for ax in axes:count*=len(tabs["domains"][ax]["members"])
    if count>MAX_POINT_REPLAYS:return {"truth":"UNKNOWN","reason":"R1_APPLICABILITY_REPLAY_LIMIT","expected":count}
    pts=[]
    for key in product(*(tabs["domains"][ax]["members"] for ax in axes)):
        truth,reasons=bd.guard(g,dict(zip(axes,key,strict=True)));pts.append({"key":list(key),"truth":truth,"reasons":reasons})
    truths={x["truth"] for x in pts}
    truth=next(iter(truths)) if len(truths)==1 else "UNKNOWN"
    return {"truth":truth,"axes":axes,"points":pts,"expected":count,"source":"NATIVE_GUARD",
            "reason":"MIXED_OR_UNKNOWN_WHOLE_TEST_APPLICABILITY" if truth=="UNKNOWN" else None}

def validate_evidence_ids(d,i,targs):
    ids={x["id"] for c in ("requirements","metrics","tests") for x in d[c]}|set(targs)|{x["id"] for x in d["base"]["sources"]}
    ids|={x["id"] for c in d["base"]["frame"].values() if type(c) is list for x in c if type(x) is dict and "id" in x}
    ids|={d["base"]["frame"]["id"],d["base"]["study"]["id"]}
    for c in ("claims","attestations"):
        need(type(i[c]) is list,"R1_EVIDENCE_LIST")
        for r in i[c]:
            need(type(r) is dict and "id" in r and qualified(r["id"]) and r["id"] not in ids,"R1_EVIDENCE_ID_COLLISION")
            ids.add(r["id"])

def revision_changes(old,proposed):
    result=[]
    for c in ("requirements","metrics","tests"):
        a={r["id"]:r for r in old[c]};b={r["id"]:r for r in proposed[c]}
        for k in sorted(set(a)|set(b)):
            x,y=a.get(k),b.get(k)
            if x==y:continue
            if x is not None and y is not None:need(x["version"]!=y["version"],"R1_REVISION_VERSION_REQUIRED")
            result.append({"collection":c,"id":k,"old_ref":digest(x) if x is not None else None,"new_ref":digest(y) if y is not None else None})
    return result
