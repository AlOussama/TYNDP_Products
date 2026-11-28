"""Materialized source-to-native execution and independent original assessment.
The candidate and oracle do not share mathematical or verdict implementation.
The final gate refuses an unexpected diagnostic, missing source or mismatch.
"""
import sys,json,copy,csv,subprocess,math,traceback
from pathlib import Path
from hashlib import sha256,sha1
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parents[2]
C1=ROOT/"BUNDLE_ML_04A_MS1_C1"/"WS_B_original_reference_corpus"
C2=ROOT/"BUNDLE_ML_04A_MS1_C2"/"closure_v1"
import authoring
from authoring import AParser,pairs,no_float,AuthoringError
from closure import digest,Reject
from closure_v1.diagnostics import DiagnosticReject,RULE_SOURCE
from record_contract import CandidateReject
from original_compiler import compile_rc
from original_p5 import compile_p5
SCHEMA="c3-original-authoring-0.2"

def read(p):return json.loads(Path(p).read_text())
def blob(raw):return sha1(("blob "+str(len(raw))+"\0").encode()+raw).hexdigest()
def sha(raw):return sha256(raw).hexdigest()
def stable(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def decode(raw,syntax):
    s=raw.decode("utf-8")
    x=AParser(s).parse() if syntax=="A" else json.loads(s,object_pairs_hook=pairs,parse_float=no_float,parse_constant=no_float)
    if set(x)!={"schema","definition","instance"} or x["schema"]!=SCHEMA or x["definition"]["schema"]!="c3-authored-native-contract-0.2":raise AuthoringError("ORIGINAL_AUTHORING_SCHEMA")
    return x
def candidate_source(identity,syntax,control=False):
    p=HERE/("controls" if control else "originals")/syntax/(identity+(".scn" if syntax=="A" else ".json"))
    raw=p.read_bytes()
    rel=str(p.relative_to(REPO));git_blob=subprocess.check_output(["git","rev-parse","HEAD:"+rel],cwd=REPO,text=True).strip()
    if blob(raw)!=git_blob:raise RuntimeError("Committed source blob mismatch "+rel)
    x=decode(raw,syntax)
    if x["instance"]["id"]!=identity:raise RuntimeError("Candidate identity mismatch")
    src=x["definition"]["original_source"];sp=(REPO/src["path"]).resolve()
    if REPO not in sp.parents or blob(sp.read_bytes())!=src["blob"]:raise RuntimeError("Pinned original source mismatch")
    return x,raw,sp.read_bytes(),rel,git_blob
def execute(identity,syntax,control=False):
    record={"id":identity,"syntax":syntax,"status":"BLOCKED_INTERNAL","owner":"OWNER_TBD","conformance":"NOT_PROVED","full_source":False,"diagnostics":[],"stage_receipts":{}}
    doc=None
    try:
        doc,raw,original,path,git_blob=candidate_source(identity,syntax,control)
        record.update(full_source=True,source_path=path,source_blob=git_blob,source_sha256=sha(raw),
                      authored_structural_identity=digest(doc),original_source_blob=blob(original),
                      original_source_sha256=sha(original),representation_audit_identity=digest([syntax,sha(raw),git_blob,sha(original)]))
        if doc["definition"]["family"]=="RC":
            record["result"]=compile_rc(doc,original)
        else:
            record["result"]=compile_p5(doc,record["stage_receipts"])
        record["status"]="RETURNED";record["candidate_status"]=record["result"]["status"]
    except CandidateReject as e:
        record.update(status="REJECTED",candidate_status="REJECTED",diagnostics=[e.record])
    except DiagnosticReject as e:
        r=e.record
        record.update(status=r["status"],candidate_status=r["status"],diagnostics=[{**r,"candidate_path":r["path"],"path_kind":"LOWERED_C2_VALIDATION_OBJECT"}])
    except Reject as e:
        # Non-attributed errors never satisfy expected negative verdicts.
        record.update(status="BLOCKED_INTERNAL",error_type=type(e).__name__,reason=str(e))
    except Exception as e:
        record.update(status="BLOCKED_INTERNAL",error_type=type(e).__name__,reason=str(e),traceback=traceback.format_exc(limit=5))
    for diag in record["diagnostics"]:
        diag["candidate_source_path"]=record.get("source_path")
        diag["candidate_source_sha256"]=record.get("source_sha256")
        diag["original_source_blob"]=record.get("original_source_blob")
    return doc,record
def clean_rc(x):
    x=copy.deepcopy(x)
    for k in ("expected_original","negative_original","analytic_derivation","expression_gap","status","original"):x.pop(k,None)
    x["synthetic_data"].pop("expected",None)
    return x
def exact_record(x):
    if type(x) is float:return str(x)
    if type(x) is list:return [exact_record(y) for y in x]
    if type(x) is dict:return {k:exact_record(v) for k,v in x.items()}
    return x
def source_fidelity(doc,row,p5):
    if row["family"]=="P5":
        expected=next(x for x in p5["mutations"] if x["id"]==row["id"])["record"]
        return doc["instance"]["record"]==exact_record(expected)
    raw=read(C1/"reference_cases"/row["rc"]/"contract.json")
    if row["family"]=="C23" and row["id"]!="MUT-11":
        m=read(C1/"original_c23_mutations"/(row["id"]+".json"))
        for e in m["edits"]:
            x=raw
            for k in e["path"][:-1]:x=x[k]
            x[e["path"][-1]]=e["value"]
    return doc["instance"]["record"]==clean_rc(raw)
def analytical_receipts():
    # Deliberately separate invocation of unchanged original analytical oracle.
    sys.path.insert(0,str(C1/"regression_runner"))
    import run as frozen_runner
    frozen_runner.verify()
    return {r["id"]:r for r in frozen_runner.reference_oracles()}
def out(result,n):return [r["value"] for r in result["outputs"]["output:"+n]]
def true_assertions(r):return all(a["truth"]=="TRUE" for a in r["obligations"]["assertions"])
def numerical_compare(rc,result,expected):
    if rc=="RC01":actual={k:out(result,k)[0] for k in ("intake","final","loss")}
    elif rc=="RC02":actual={"individual":[str(F(x)*1000) for x in out(result,"received")],"fleet":str(F(out(result,"fleet_total")[0])*1000)}
    elif rc=="RC03":actual={k:out(result,k)[0] for k in ("hydrogen_power","eta")}
    elif rc=="RC04":actual={k:out(result,k)[0] for k in ("final","converted_energy")}
    elif rc=="RC05":actual={"nodal":out(result,"nodal"),"cycle":out(result,"cycle")[0]}
    elif rc=="RC06":actual={"modules":out(result,"count_binary")[0],"commission":int(F(out(result,"commission")[0])),"capacity":out(result,"capacity"),"cost":out(result,"cost")[0]}
    elif rc=="RC07":
        actual={"pre_revelation_equal":result["policies"][0]["status"]=="FINITE_OBSERVED_TRUE",
                "after_revelation_may_differ":len(set(out(result,"decision_projection")))>1}
    elif rc=="RC08":actual={"kpi":out(result,"total")[0]}
    elif rc=="RC09":actual={"annual":out(result,"annual")[0],"discounted":out(result,"discounted")[0],"owner":result["owner"]}
    elif rc=="RC10":actual={"finite_agreement":F(out(result,"delta")[0])==0,"e4":result["comparison_evidence"][0]["status"],"e5":"NOT_ASSESSED"}
    else:raise RuntimeError("Unknown frozen RC")
    return actual,actual==expected
def observed_counterexample(r,assertion):
    if r["status"]!="RETURNED":return False
    return any(z["id"]=="assertion:"+assertion and z["truth"]=="FALSE" for z in r["result"]["obligations"]["assertions"])
def codes(r):return [x["code"] for x in r.get("diagnostics",[])]
def rejected(r,allowed):return r["status"]=="REJECTED" and bool(set(codes(r))&set(allowed))
def observed_diagnostic(row,doc,r,baselines):
    """Derive diagnostics only from returned, independently executed candidate evidence.
    These are actual authored source object paths; they are not oracle JSONPaths."""
    if row["family"]!="C23" or r["status"]!="RETURNED":return
    oid=row["id"]
    mapping={"MUT-01":("intake_balance","R07"),"MUT-02":("service","R09"),
             "MUT-05":("kvl","R09"),"MUT-18":("kvl","R09")}
    if oid in mapping:
        name,rule=mapping[oid]
        if not observed_counterexample(r,name):return
        evidence=next(a for a in r["result"]["obligations"]["assertions"] if a["id"]=="assertion:"+name)
        code,path,reason="FINITE_COUNTEREXAMPLE","/definition/conditions/"+name,"Native evaluated assertion is FALSE"
    elif oid=="MUT-07":
        evidence=next((a for a in r["result"]["policies"] if a["status"]=="FINITE_COUNTEREXAMPLE"),None)
        if evidence is None:return
        index=next(j for j,a in enumerate(doc["definition"]["policies"]) if a["id"]==evidence["id"])
        code,path,rule,reason="FINITE_COUNTEREXAMPLE","/definition/policies/"+str(index),"Native information policy has violating coordinates"
    elif oid=="MUT-11":
        base=baselines[("RC01",r["syntax"])]
        if base["status"]!="RETURNED":return
        a,b=base["result"],r["result"]
        if a["lowered_normativity"]==b["lowered_normativity"] or a["semantic_identity"]==b["semantic_identity"]:return
        evidence={"base":a["lowered_normativity"],"candidate":b["lowered_normativity"],
                  "base_semantic_identity":a["semantic_identity"],"candidate_semantic_identity":b["semantic_identity"]}
        code,path,rule,reason="E1_DIFFERENT","/definition/metadata/normativity","Admitted canonical requirement normativity and semantic identity differ"
    else:return
    r["diagnostics"].append({"schema":"c3-actual-diagnostic-0.1","status":"OBSERVED","code":code,
        "candidate_path":path,"path_kind":"DECODED_CANDIDATE_OBJECT","rule_id":rule,"rule_source":RULE_SOURCE,
        "reason":reason,"stage":"NATIVE_RETURNED_EVIDENCE","native_evidence":evidence,"owner":"OWNER_TBD","conformance":"NOT_PROVED",
        "candidate_source_path":r["source_path"],"candidate_source_sha256":r["source_sha256"],"original_source_blob":r["original_source_blob"]})

def assess(row,doc,r,baselines,analytical,p5):
    """Original expectation assessment is independent of candidate validation.
    BLOCKED denotes refusal of a positive research claim; actual finite
    counterexample/static rejection remains visible and is not relabelled PASS.
    """
    oid=row["id"];family=row["family"];expected=row["expected"]
    receipt={"original_expected":expected,"actual_original_verdict":"UNRESOLVED","accounted_for":False}
    if doc is None or not source_fidelity(doc,row,p5) or r["status"]=="BLOCKED_INTERNAL":
        return {**receipt,"reason":"SOURCE_FIDELITY_OR_INTERNAL_EXECUTION_FAILURE"}
    if family=="P5":
        o=next(z for z in p5["mutations"] if z["id"]==oid)
        actual_codes=[z["code"] for z in o["observed"]["diagnostics"]]
        ok=rejected(r,[expected]) and expected==o["expected"] and expected in actual_codes and bool(r["stage_receipts"].get("static_native_packages"))
        return {**receipt,"actual_original_verdict":expected if ok else "UNRESOLVED","accounted_for":ok,
                "independent_oracle":{"status":o["observed"]["status"],"diagnostics":o["observed"]["diagnostics"],"expected":o["expected"]},
                "scope":"Actual candidate static/typed/finite rejection, no post-rejection graph evaluation"}
    o=analytical[oid]
    receipt["independent_oracle"]=o
    if o["status"]!="PASS":return receipt
    if family=="RC":
        if r["status"]!="RETURNED" or r["candidate_status"] not in ("FINITE_OBSERVATIONS_ONLY","BLOCKED"):return receipt
        result=r["result"];actual,ok=numerical_compare(oid,result,o["actual"])
        ok=ok and result["roundtrip"] and true_assertions(result) and all(z["status"]=="FINITE_OBSERVED_TRUE" for z in result["policies"])
        # Positive original expectation was conceptual, not normative PASS.
        return {**receipt,"actual_original_verdict":expected if ok else "UNRESOLVED","accounted_for":ok,"actual_finite_observations":actual,
                "scope":"Finite authored obligations; original conceptual expectation retained; owner and proof not promoted"}
    # Original C23 verdict mapping, independent from analytical micro-oracle
    # edit paths. Each rule requires actual relevant candidate evidence.
    a=oid
    v=None
    if a=="MUT-01" and observed_counterexample(r,"intake_balance"):v="BLOCKED"
    elif a=="MUT-02" and observed_counterexample(r,"service"):v="BLOCKED"
    elif a=="MUT-03" and rejected(r,["HEATING_VALUE_BASIS"]):v="BLOCKED"
    elif a=="MUT-04" and rejected(r,["MASS_UNIT"]):v="BLOCKED"
    elif a=="MUT-05" and observed_counterexample(r,"kvl"):v="BLOCKED"
    elif a=="MUT-06" and rejected(r,["INTEGER_DOMAIN"]):v="BLOCKED"
    elif a=="MUT-07" and r["status"]=="RETURNED" and any(z["status"]=="FINITE_COUNTEREXAMPLE" for z in r["result"]["policies"]):v="BLOCKED"
    elif a=="MUT-08" and r["status"]=="REJECTED" and any(c.startswith(("N7_CONTRIBUTION","DUPLICATE_CONTRIBUTION","SEMANTIC_DOUBLE_COUNT")) for c in codes(r)):v="BLOCKED"
    elif a=="MUT-09" and rejected(r,["COUNTERFACTUAL_EXOGENEITY"]):v="BLOCKED"
    elif a=="MUT-10" and rejected(r,["E4_UNSUPPORTED"]):v="BLOCKED"
    elif a=="MUT-11" and r["status"]=="RETURNED":
        base=baselines[("RC01",r["syntax"])]
        if base["status"]=="RETURNED" and base["result"]["semantic_identity"]!=r["result"]["semantic_identity"] and base["result"]["lowered_normativity"]!=r["result"]["lowered_normativity"] and doc["definition"]["metadata"]["normativity"]=="NORMATIVE_REQUIREMENT_PENDING_OWNER":v="E1_DIFFERENT"
        receipt["mapping_note"]="Original normativity mutation is valid pending-owner normativity, separate from the C1 derived invalid APPROVED edit."
    elif a=="MUT-12" and rejected(r,["SOURCE_LOSS"]):v="AUDIT_LOSS"
    elif a=="MUT-13" and rejected(r,["EVIDENCE_PROMOTION"]):v="FAIL_STATIC"
    elif a=="MUT-14" and rejected(r,["AMBIGUOUS_ALIAS"]):v="BLOCKED"
    elif a=="MUT-15" and rejected(r,["GUARD_REQUIRED"]):v="BLOCKED"
    elif a=="MUT-16" and rejected(r,["CARRIER_UNIT"]):v="FAIL_STATIC"
    elif a=="MUT-17" and rejected(r,["DURATION_REQUIRED"]):v="BLOCKED"
    elif a=="MUT-18" and observed_counterexample(r,"kvl") and r["result"]["conformance"]=="NOT_PROVED":
        if any(z["id"]=="report:e4_proof" and z["status"]=="NOT_EXECUTED" for z in r["result"]["external_reports"]):v="E4_NOT_PROVED"
    return {**receipt,"actual_original_verdict":v or "UNRESOLVED","accounted_for":v in expected if v is not None else False,
            "scope":"Actual native candidate evidence or actual structural diagnostic, separately mapped to original C23 verdict"}
def pair_check(a,b):
    if not(a["full_source"] and b["full_source"] and a["authored_structural_identity"]==b["authored_structural_identity"] and a["source_sha256"]!=b["source_sha256"] and a["representation_audit_identity"]!=b["representation_audit_identity"]):return False
    if a["status"]!=b["status"] or a["candidate_status"]!=b["candidate_status"]:return False
    if a["status"]=="RETURNED":
        return all(a["result"][k]==b["result"][k] for k in ("semantic_identity","graph_semantic_identity","package_sha256","roundtrip"))
    if a["status"]=="REJECTED":
        return [(x["code"],x["candidate_path"],x["rule_id"]) for x in a["diagnostics"]]==[(x["code"],x["candidate_path"],x["rule_id"]) for x in b["diagnostics"]]
    return False
def p5_control(p5):
    rows=[]
    for syntax in ("A","B"):
        doc,r=execute("P5-BASE",syntax,True)
        if r["status"]=="RETURNED":
            res=r["result"];ok=doc["instance"]["record"]==exact_record(p5["base"]) and res["status"]=="BLOCKED"
            for mid,z in p5["base_result"]["synthetic_numeric_results"].items():
                key=mid.lower();annual=F(res["outputs"]["output:"+key][0]["value"]);npv=F(res["outputs"]["output:"+key+":npv"][0]["value"])
                refs=res["lineage"]["slot:"+key+":discount"]["npv"][0]["events"]
                ok=ok and math.isclose(float(annual),z["illustrative_annual_cost_saving_eur"],abs_tol=1e-9,rel_tol=0) and math.isclose(float(npv),z["illustrative_npv_proxy_eur"],abs_tol=1e-9,rel_tol=0)
                ok=ok and (1 if npv>0 else -1 if npv<0 else 0)==z["decision_sign"] and len(refs)==5 and all(v==1 for v in refs.values())
            r["control_passed"]=ok
        else:r["control_passed"]=False
        rows.append(r);print("C3_P5_BASE_CONTROL="+stable(r))
    return rows,all(z["control_passed"] for z in rows) and pair_check(*rows)
def main(p5_path,output_path):
    p5=read(p5_path);manifest=read(C1/"frozen_original_test_manifest.json")
    if blob((C1/"frozen_original_test_manifest.json").read_bytes())!="ca75ee61c1fe1cdab15bb2287e04a41cf34430d9":raise RuntimeError("Original catalogue pin drift")
    originals=manifest["originals"];assert len(originals)==58
    contract_path=C2/"original_diagnostic_contracts.json"
    if blob(contract_path.read_bytes())!="2d9321293450511d7bafdd6b8b2ffa7fe0f7b814":raise RuntimeError("Frozen diagnostic contract drift")
    frozen_diagnostics={d["id"]:d for d in read(contract_path)["originals"]}
    analytical=analytical_receipts()
    rows=[];base={};pairs_out=[]
    for original in originals:
        path_results=[]
        for syntax in ("A","B"):
            doc,r=execute(original["id"],syntax)
            r["family"]=original["family"];r["rc"]=original["rc"]
            contract=frozen_diagnostics[original["id"]]
            r["original_diagnostic_contract"]=contract
            catalogue=(REPO/contract["catalogue"]["path"]).read_bytes()
            if blob(catalogue)!=contract["catalogue"]["blob"]:raise RuntimeError("Frozen original source catalogue drift")
            r["original_catalogue_sha256"]=sha(catalogue)
            if "derived_mutation" in contract:
                mutation=(REPO/contract["derived_mutation"]["path"]).read_bytes()
                if blob(mutation)!=contract["derived_mutation"]["blob"]:raise RuntimeError("Frozen mutation recipe drift")
                r["derived_mutation_sha256"]=sha(mutation)
            if doc is not None:observed_diagnostic(original,doc,r,base)
            r["assessment"]=assess(original,doc,r,base,analytical,p5)
            rule_ok=original["family"]=="RC" or any(z["rule_id"]==contract["rule_id"] and z.get("candidate_source_sha256")==r.get("source_sha256") for z in r["diagnostics"])
            r["assessment"]["original_rule_matched"]=rule_ok
            if not rule_ok:r["assessment"].update(accounted_for=False,reason="ORIGINAL_DIAGNOSTIC_RULE_NOT_MATCHED")
            if original["family"]=="RC":base[(original["id"],syntax)]=r
            path_results.append(r);rows.append(r)
            print("C3_ORIGINAL_PATH="+stable(r),flush=True)
        same=pair_check(*path_results) if all(z["status"]!="BLOCKED_INTERNAL" for z in path_results) else False
        pairs_out.append({"id":original["id"],"canonical_pair":same,"accounted_for":same and all(z["assessment"]["accounted_for"] for z in path_results)})
    control,control_ok=p5_control(p5)
    counts={"source_files":sum(z["full_source"] for z in rows),"paths_attempted":len(rows),
            "paths_accounted_for":sum(z["assessment"]["accounted_for"] for z in rows),"pairs_accounted_for":sum(z["accounted_for"] for z in pairs_out),
            "original_rules_matched":sum(z["assessment"]["original_rule_matched"] for z in rows),
            "internal_failures":sum(z["status"]=="BLOCKED_INTERNAL" for z in rows),"returned":sum(z["status"]=="RETURNED" for z in rows),"rejected":sum(z["status"]=="REJECTED" for z in rows),
            "p5_control_passed":control_ok}
    result={"schema":"c3-original-corpus-results-0.2","counts":counts,"rows":rows,"pairs":pairs_out,"p5_baseline_controls":control,
            "independent_analytical":list(analytical.values()),"independent_p5_suite":p5["suite"],
            "scope":"Finite synthetic research only; no E4/E5 general proof, no owner approval or real model conformity"}
    Path(output_path).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print("C3_ORIGINAL_SUMMARY="+stable(counts),flush=True)
    if counts["source_files"]!=116 or counts["paths_accounted_for"]!=116 or counts["pairs_accounted_for"]!=58 or counts["internal_failures"] or not control_ok:
        raise SystemExit("C3 original corpus exit NOT_MET")

if __name__=="__main__":main(sys.argv[1],sys.argv[2])
