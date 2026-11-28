"""Separate, measured C5-R1 change tasks and restricted matched-scope ablation.
Synthetic controlled tasks, not human authoring effort or global minimality.
"""
import copy,json,time
from pathlib import Path
import test_r1 as C
from test_r1 import vm,r1,digest,canon,Reject,composition,metadata,build,variant,run,reb,add_requirement,STUDY,SYSTEM,TEST,REVIEW,METRIC,SOURCE
from hashlib import sha256
HERE=Path(__file__).resolve().parents[1]
OUT=HERE/"generated"
OUT.mkdir(exist_ok=True)
records=[];alternatives=[]

def check(ok,msg):
    if not ok:raise AssertionError(msg)

def leaves(x,path=()):
    if isinstance(x,dict):
        if not x:return {path:"{}"}
        return {k:v for a,b in x.items() for k,v in leaves(b,path+(a,)).items()}
    if isinstance(x,list):
        if not x:return {path:"[]"}
        # Stable registry record IDs rather than changed array offsets.
        if all(isinstance(z,dict) and isinstance(z.get("id"),str) for z in x):
            return {k:v for z in x for k,v in leaves(z,path+(z["id"],)).items()}
        return {k:v for n,z in enumerate(x) for k,v in leaves(z,path+(str(n),)).items()}
    return {path:json.dumps(x,sort_keys=True,ensure_ascii=False)}

def differences(a,b):
    x,y=leaves(a),leaves(b)
    return sum(x.get(k)!=y.get(k) for k in set(x)|set(y))

def changed_ids(a,b,key):
    x={z["id"]:z for z in a.get(key,[])};y={z["id"]:z for z in b.get(key,[])}
    return sorted(k for k in set(x)|set(y) if x.get(k)!=y.get(k))

def assess(d,i,tid):
    r=run(d,i)
    return {"test":r["tests"][tid]["verdict"],"definition":r["definition_semantic_identity"],
            "method_identities":(r["native_receipt"].get("result") or {}).get("definition",{}).get("method_identities",{}),
            "requirement":r["requirements"].get(STUDY,{}).get("status"),"conformance":r["contract_conformance"]}

def measure(id,before,after,manual,target,expected_before,expected_after,start):
    d0,i0=before;d1,i1=after
    a,b=assess(d0,i0,target[0]),assess(d1,i1,target[1])
    check(a["test"]==expected_before and b["test"]==expected_after,id+" verdict drift")
    out={"id":id,"authored_edit_operations":manual,"logical_artefacts_changed":int(d0!=d1)+int(i0!=i1),
         "definition_leaf_changes":differences(d0,d1),"instance_leaf_changes":differences(i0,i1),
         "base_definition_leaf_changes":differences(d0["base"],d1["base"]),
         "changed_requirements":changed_ids(d0,d1,"requirements"),"changed_metrics":changed_ids(d0,d1,"metrics"),"changed_tests":changed_ids(d0,d1,"tests"),
         "canonical_definition_bytes_before":len(canon(d0).encode()),"canonical_definition_bytes_after":len(canon(d1).encode()),
         "before":a,"after":b,"elapsed_seconds":round(time.monotonic()-start,4),
         "language_code_changes":0,"limit":"Controlled authored object changes; machine time is not human authoring effort."}
    records.append(out);print("R1_CHANGE="+json.dumps(out,sort_keys=True))

def exchange(ctl):
    d,i,_=ctl.migrate(*build());n,ni,_=ctl.migrate(*build(formula="base-alt+base",method_version="0.3"))
    old,new=d["base"]["slots"][0],n["base"]["slots"][0];bp=digest(d["base"])
    req={"schema":composition.VERSION,"base_ref":bp,"overrides":[{"id":"override:one","slot":old["id"],"expected_old":digest(old),"replacement":new,"allowed_expressions":["benefit"]}]}
    rp=digest(req)
    auth={"schema":composition.APPROVAL,"base_ref":bp,"request_ref":rp,"decision_scope":"NON_NORMATIVE_RESEARCH_ONLY","approvals":[{"id":"override:one","slot":old["id"],"old_ref":digest(old),"new_ref":digest(new),"allowed_expressions":["benefit"],"authority_ref":old["source_ref"],"source_sha256":old["profile"]["source_sha256"],"decision":"APPROVED_RESEARCH_OVERRIDE","reason":"Synthetic R1 method exchange control"}]}
    effective=vm.compose_method(d,digest(d),req,rp,auth,digest(auth))["definition"]
    check(effective==n,"composed R1 differs from explicitly authored method replacement")
    try:vm.compose_method(d,digest(d),req,rp,auth,"0"*64)
    except Reject:pass
    else:raise AssertionError("unauthorized method exchange")
    return d,i,n,ni

def governed_revision(d,n):
    changes=r1.revision_changes(d,n);src=next(x for x in d["base"]["sources"] if x["id"]==SOURCE)
    a={"schema":"c5-r1-revision-authorization-0.1","base_ref":digest(d),"proposed_ref":digest(n),"changes":changes,"authority_ref":SOURCE,"source_sha256":src["sha256"],"decision":"APPROVED_RESEARCH_REVISION","reason":"Controlled synthetic change"}
    receipt=vm.revise_requirements(d,digest(d),n,digest(n),a,digest(a));check(receipt["changes"]==changes,"revision receipt drift")
    return receipt

def tasks(ctl):
    start=time.monotonic();d,i,_=ctl.migrate();n,ni=copy.deepcopy((d,i))
    a=copy.deepcopy(n["requirements"][1]);a["id"]="requirement:new";n["requirements"].append(a);n["tests"][0]["requirements"].append(a["id"]);n["tests"][0]["version"]="2";reb(n,ni);governed_revision(d,n)
    measure("M01_ADD_REQUIREMENT",(d,i),(n,ni),["add requirement record","link requirement in existing test","increment test version","authorize exact revision"],(TEST,TEST),"PASS","PASS",start)

    start=time.monotonic();d,i,_=ctl.migrate();n,ni=copy.deepcopy((d,i));t=copy.deepcopy(n["tests"][0]);m=next(x for x in n["metrics"] if x["id"]==t["metric"]);m=copy.deepcopy(m);m["id"]="metric:new";n["metrics"].append(m);n["requirements"][1]["metric_refs"].append(m["id"]);n["requirements"][1]["version"]="2";t.update(id="test:new",metric=m["id"]);n["tests"].append(t);ni["requested_tests"].append(t["id"]);reb(n,ni);governed_revision(d,n)
    measure("M02_ADD_METRIC",(d,i),(n,ni),["add metric record","link metric in requirement","increment requirement version","add test","request test","authorize exact revision"],(TEST,t["id"]),"PASS","PASS",start)

    start=time.monotonic();d,i,_=ctl.migrate(*build(numeric=True,expected=[15,21]));n,ni,_=ctl.migrate(*build(numeric=True,condition="benefit <= expected",expected=[15,21]));check(d["requirements"]==n["requirements"] and d["tests"]==n["tests"],"criterion change touched outer records")
    measure("M03_CHANGE_CRITERION",(d,i),(n,ni),["edit one native condition; regenerate package/pins"],("test:benchmark","test:benchmark"),"FAIL","PASS",start)

    start=time.monotonic();d,i,n,ni=exchange(ctl)
    measure("M04_SWAP_METHOD",(d,i),(n,ni),["change one native expression","change method version","explicit composition request","explicit research authorization"],(TEST,TEST),"PASS","PASS",start)
    check(run(n,ni)["study_metrics"][METRIC]["value"]==[{"key":["s1"],"value":"115"},{"key":["s2"],"value":"150"}],"method result unexpected")

    start=time.monotonic();d,i=ctl.independent_native("state");n,ni=copy.deepcopy((d,i));a=copy.deepcopy(n["requirements"][-1]);a["id"]="requirement:state-reuse";n["requirements"].append(a);t=copy.deepcopy(n["tests"][-1]);t.update(id="test:state-reuse",requirements=[a["id"]]);n["tests"].append(t);ni["requested_tests"].append(t["id"]);reb(n,ni);governed_revision(d,n);check(n["base"]==d["base"],"contract reuse edited base")
    measure("M05_REUSE_COMPONENT_STATE_CONTRACT",(d,i),(n,ni),["add requirement","add test referring to existing state contract","request test","authorize exact revision"],("test:state","test:state-reuse"),"PASS","PASS",start)

    start=time.monotonic();d,i,_=ctl.migrate();n,ni=copy.deepcopy((d,i));t=copy.deepcopy(n["tests"][0]);t["id"]="test:another";n["tests"].append(t);ni["requested_tests"].append(t["id"]);reb(n,ni);governed_revision(d,n)
    measure("M06_ADD_SYSTEM_TEST",(d,i),(n,ni),["add test record reusing criterion/metric","request test","authorize exact revision"],(TEST,t["id"]),"PASS","PASS",start)

    start=time.monotonic();d,i,n,ni=exchange(ctl);i["attestations"]=[ctl.sign(d,i)];old=copy.deepcopy(ni);old["attestations"]=copy.deepcopy(i["attestations"])
    try:run(n,old)
    except Reject as e:check("R1_ATTESTATION_STALE" in str(e),"unexpected stale evidence code")
    else:raise AssertionError("stale signed evidence accepted")
    ni["attestations"]=[ctl.sign(n,ni)]
    check(d["requirements"]==n["requirements"] and d["tests"]==n["tests"],"trace changed")
    measure("M07_REBIND_TRACE_AND_EVIDENCE_AFTER_METHOD_CHANGE",(d,i),(n,ni),["rebind instance roots","obtain fresh signed evidence; prior evidence rejected"],(REVIEW,REVIEW),"PASS","PASS",start)

    start=time.monotonic();d,i=build();n,ni,receipt=ctl.migrate(d,i);check(receipt["previous_definition_pin"]==digest(d),"migration provenance")
    measure("M08_WIRE_MIGRATION",(d,i),(n,ni),["explicit reviewer source","run versioned migration; generated records/pins"],(TEST,TEST),"PASS","PASS",start)

    start=time.monotonic();d,i,_=ctl.migrate();n,ni=copy.deepcopy((d,i));n["requirements"][0]["statement"]+=" Clarified synthetic purpose.";n["requirements"][0]["version"]="2";reb(n,ni);governed_revision(d,n)
    check(d["base"]==n["base"],"wording edit changed native")
    measure("M09A_WORDING_WITHOUT_MATH",(d,i),(n,ni),["edit one requirement statement","increment requirement version","authorize exact revision"],(TEST,TEST),"PASS","PASS",start)
    start=time.monotonic();d,i,n,ni=exchange(ctl);check(d["requirements"]==n["requirements"] and d["tests"]==n["tests"],"math edit changed trace")
    measure("M09B_MATH_WITHOUT_WORDING",(d,i),(n,ni),["authorized native expression/version change"],(TEST,TEST),"PASS","PASS",start)

def legacy_exact():
    old=json.loads((HERE/"scientific_validation"/"system_verification_test_results.json").read_text())
    rows=[]
    for p in old["variants"]:
        d,i=variant(p["name"]);dp,ip=digest(d),digest(i);canonical=vm.export(d,dp,i,ip)
        actual={"definition_pin":dp,"instance_pin":ip,"package_sha256":sha256(canonical.encode()).hexdigest(),"A_source":sha256(vm.emit_control(d,i,"A")).hexdigest(),"B_source":sha256(vm.emit_control(d,i,"B")).hexdigest()}
        check(all(actual[k]==p[k] for k in actual),p["name"]+" legacy bytes drift")
        rows.append({"id":p["name"],**actual,"match":True})
    (OUT/"r1_legacy_exact.json").write_text(json.dumps(rows,indent=2))
    print("R1_LEGACY_EXACT="+json.dumps({"variants":len(rows),"hash_fields_per_variant":5,"mismatches":0}))

def old_sidecar_metric_lint(d,study_inputs):
    """Alternative 0.1 plus externally maintained metadata; deliberately
    restricted to two common-scope coverage obligations, no canonical integration."""
    met={m["id"]:m for m in d["metrics"]}
    for r in d["requirements"]:
        if not r["required"]:continue
        links=[t for t in d["tests"] if r["id"] in t["requirements"]]
        expected={x for x in r["metric_refs"] if met[x]["role"]!="STUDY"}
        if expected!={x["metric"] for x in links}:return "REJECT"
        needed={met[x]["target"] for x in r["metric_refs"] if met[x]["role"]=="STUDY"}
        if not needed<=set().union(*(set(study_inputs.get(t["id"],[])) for t in links)):return "REJECT"
    return "ACCEPT"

def admit_verdict(d):
    try:vm.admit(d,digest(d))
    except Reject:return "REJECT"
    return "ACCEPT"

def alternatives_run(ctl):
    d,i=build(numeric=True);n,ni,_=ctl.migrate(d,i);side={REVIEW:["output:benefit"]}
    pairs=[("valid",d,n,side,"ACCEPT")]
    o,b=copy.deepcopy((d,n))
    for a in (o,b):
        req=copy.deepcopy(a["requirements"][1]);req["id"]="requirement:other";req["metric_refs"].append("metric:benchmark");a["requirements"].append(req);a["tests"][0]["requirements"].append(req["id"])
    pairs.append(("missing_per_requirement_metric",o,b,side,"REJECT"))
    o,b=copy.deepcopy((d,n));next(x for x in b["tests"] if x["id"]==REVIEW)["input_refs"]=[]
    pairs.append(("missing_study_metric_validation_input",o,b,{REVIEW:[]},"REJECT"))
    for name,o,b,side,want in pairs:
        a=admit_verdict(o);c=old_sidecar_metric_lint(o,side);r=admit_verdict(b)
        check(c==r==want,"matched coverage alternatives disagree")
        z={"case":name,"expected":want,"C5_unchanged":a,"C5_plus_sidecar":c,"R1_integrated":r,
           "sidecar_in_canonical_root":False,"R1_in_canonical_root":True,"scope":"Two exact coverage obligations, not full architecture"}
        alternatives.append(z);print("R1_ABLATION="+json.dumps(z,sort_keys=True))

def main():
    C.R1.setUpClass();ctl=C.R1()
    try:legacy_exact();tasks(ctl);alternatives_run(ctl)
    finally:C.R1.tearDownClass()
    (OUT/"r1_change_experiments.json").write_text(json.dumps(records,indent=2))
    (OUT/"r1_comparative_ablation.json").write_text(json.dumps(alternatives,indent=2))
    print("R1_EXPERIMENT_SUMMARY="+json.dumps({"nine_groups":9,"actual_records":len(records),"matched_cases":len(alternatives),"full_global_minimality":False,"independent_human_authoring":False}))
if __name__=="__main__":main()
