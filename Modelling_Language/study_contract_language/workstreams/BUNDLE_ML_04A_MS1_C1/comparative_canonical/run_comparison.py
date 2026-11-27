"""Actual bounded comparative run; no original full-chain claims."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import json,sys,hashlib,platform
from common_fixtures import cases,extra_cases,frozen,CORPUS,ROOT
from closure import admit,native,bind_data,Reject,digest,source_map,preflight
from package_interface import export_package,import_package
from native_consumer import FiniteNative
from legacy_comparison import map_profile,map_predicates,m0_control,n1r,R1
import mathspec as ms
sys.path.insert(0,str(CORPUS/"independent_oracles"))
import oracles
from adapter import compile_profile
import n2r

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def attempt(fn):
    try:return {"status":"EXECUTED","result":fn()}
    except (ValueError,KeyError,TypeError) as e:return {"status":"UNSUPPORTED_OR_REJECTED","diagnostic":str(e)}
def mutant(case):
    d=deepcopy(case["data"]);m=case["negative"]
    if m:
        for row,v in zip(d["parameters"][m["param"]],m["values"],strict=True):row["value"]=v
    return d
def m3(case):
    leaf=admit(json.dumps(case["doc"]),case["context"]);pkg=export_package(leaf);leaf=import_package(pkg)
    e=FiniteNative(leaf,case["data"])
    out=e.outputs();pred=e.conditions()
    if out!=case["expected"] or not all(pred.values()):raise AssertionError((case["id"],out,pred,case["expected"]))
    neg=case["negative"];negative=None
    if neg:
        try:
            n=FiniteNative(leaf,mutant(case))
            vals=n.conditions();negative={"kind":"FINITE_PREDICATE","conditions":vals,"expected_false":neg.get("condition")}
            if neg.get("reject") or vals.get(neg["condition"]) is not False:raise AssertionError(("M3 negative",case["id"],vals))
        except Reject as ex:
            if neg.get("reject") not in str(ex):raise
            negative={"kind":"DATA_DOMAIN_REJECTION","diagnostic":str(ex)}
    return {"stage":"CANONICAL_STATIC_AND_BOUNDED_FINITE_CONSUMER","outputs":out,"conditions":pred,"negative":negative,"native_identity":leaf["native_identity"],"semantic_identity":leaf["semantic_identity"],"audit_identity":leaf["audit_identity"],"package_bytes":len(pkg.encode()),"native_canonical_bytes":len(leaf["native_canonical"].encode()),"data_receipt":e.receipt,"full_path":False}
def compare_case(case):
    # Both M2 target paths consume exactly the native public Program.
    # Do NOT require the M3-specific domain admission policy before M2.
    preflight(case["doc"]);spec=ms.to_spec(case["doc"]);p=spec.program
    oracle=oracles.run(frozen(case["id"])) if case["id"].startswith("RC") else None
    if oracle is not None and oracle!=frozen(case["id"])["synthetic_data"]["expected"]:raise AssertionError("FROZEN_ORACLE")
    r={"id":case["id"],"scope":case["note"],"fixture_identity":digest(case),"independent_original_oracle":oracle,
       "M0":attempt(lambda:m0_control(case)),"M2_predicate":attempt(lambda:map_predicates(case,p)),
       "M2_profile":attempt(lambda:map_profile(case,p)),"M3":attempt(lambda:m3(case))}
    if r["M2_profile"]["status"]=="EXECUTED":
        out=r["M2_profile"]["result"]["outputs"]
        if out!=case["expected"]:raise AssertionError(("M2 profile output",case["id"],out,case["expected"]))
        # Re-evaluate the exact same mutated input where it affects computed outputs.
        if case["negative"] is not None:
            r["M2_profile"]["result"]["negative_numeric"]=attempt(lambda:map_profile(case,p,mutant(case))["outputs"])
            # This is not a predicate/contract verdict.
    if r["M0"]["status"]==r["M2_predicate"]["status"]=="EXECUTED":
        a,b=r["M0"]["result"],r["M2_predicate"]["result"]
        r["legacy_equal"]={"semantic":a["semantic_digest"]==b["semantic_digest"],"audit":a["audit_digest"]==b["audit_digest"]}
        if not all(r["legacy_equal"].values()):raise AssertionError(("legacy comparison",case["id"],r["legacy_equal"]))
    if r["M2_profile"]["status"]==r["M3"]["status"]=="EXECUTED":
        r["same_numeric_outputs"]=r["M2_profile"]["result"]["outputs"]==r["M3"]["result"]["outputs"]
        if not r["same_numeric_outputs"]:raise AssertionError(case["id"])
    return r
def original_profile_controls():
    root=R1/"fixtures";data=json.loads((root/"data.json").read_text());out=[]
    for timing,expected in (("begin","415/11"),("end","4150/121")):
        m=json.loads((root/("method-"+timing+".json")).read_text());s=json.loads((root/("study-"+timing+".json")).read_text())
        native_consumer=compile_profile(m,s,data)
        nv=str(native_consumer.scalar("summary").value)
        a=n2r.evaluate((root/"contract.a.scn").read_text(),"A",root/("study-"+timing+".json"),root/"trust.json")
        b=n2r.evaluate((root/"contract.b.json").read_text(),"B",root/("study-"+timing+".json"),root/"trust.json")
        av=a["result"]["summary"]["rows"][0]["value"];bv=b["result"]["summary"]["rows"][0]["value"]
        if not av==bv==nv==expected:raise AssertionError((timing,av,bv,nv,expected))
        out.append({"timing":timing,"M0_R1_A":av,"M0_R1_B":bv,"MS1_native_consumer":nv,"expected":expected,"same":True,
                    "R1_integrated_result_receipt":a["receipt"],"R1_audit_digest":a["audit_digest"],
                    "M3_scope":"MS1 finite mathematical control; not current canonical package method governance",
                    "method_blob_sha256":sha(root/("method-"+timing+".json"))})
    # Explicit R1 outer-semantics capability, not a numerical conformance claim.
    from make_fixtures import contract,quant
    x=contract();x["frame"]["domains"] += [{"id":"domain:req","kind":"request","members":["r1","r2"]},{"id":"domain:res","kind":"response","members":["a1","a2"]}]
    x["frame"]["scopes"][0]["domains"] += ["domain:req","domain:res"]
    x["predicates"][0]["expr"]=quant("forall","r","request","domain:req",quant("exists","a","response","domain:res",{"op":"bool3","value":"UNKNOWN"}))
    x["assertions"][0]["semantic_role"]="SERVICE_GUARANTEE";x["assertions"][0]["guard"]="UNKNOWN"
    z=n1r.run(json.dumps(x),"B")
    if "SERVICE_BEHAVIOURAL_EVIDENCE_REQUIRED" not in z["blocked"] or "UNKNOWN_GUARD" not in z["blocked"]:raise AssertionError(z["blocked"])
    return {"profile_swaps":out,"outer_semantics_control":{"M0_R1":z["status"],"blocked":z["blocked"],"M3":"C2_REQUIRED; no A/G or Bool3 execution","scope":"static declaration, no service conformance"}}
def main():
    rr=[compare_case(c) for c in cases()+extra_cases()]
    primary=rr[:10];extra=rr[10:]
    # Explicit expected scope outcomes. Errors are not credited as successful
    # representations. Any unexpected result fails the research CI.
    expected={"RC01":(True,False),"RC02":(False,True),"RC03":(False,False),"RC04":(False,False),"RC05":(False,False),"RC06":(False,False),"RC07":(True,False),"RC08":(False,False),"RC09":(False,True),"RC10":(True,False)}
    for r in primary:
        if r["M3"]["status"]!="EXECUTED":raise AssertionError(("M3 primary",r))
        actual=tuple(r[k]["status"]=="EXECUTED" for k in ("M2_predicate","M2_profile"))
        if actual!=expected[r["id"]]:raise AssertionError(("M2 scope",r["id"],actual,expected[r["id"]],r))
    if not extra[0].get("same_numeric_outputs") or extra[1]["M2_profile"]["status"]!="EXECUTED" or extra[1]["M3"]["status"]=="EXECUTED" or "POWER_DOMAIN" not in extra[1]["M3"]["diagnostic"]:raise AssertionError(("extra",extra))
    controls=original_profile_controls()
    def count(k):return sum(r[k]["status"]=="EXECUTED" for r in primary)
    results={"schema":"c1-comp-receipt-0.1","scope":"Derived mathematical fragments, not original full contract paths","python":platform.python_version(),"original_population":{"identities":58,"AB_paths":116,"full_paths_executed":0,"traceability":105},
      "counts":{"primary_fragments":10,"M0_static_controls":count("M0"),"M2_legacy_predicate_static":count("M2_predicate"),"M2_legacy_profile_numeric":count("M2_profile"),"M3_static_and_finite":count("M3"),"matched_numeric_M2_M3":sum(r.get("same_numeric_outputs",False) for r in primary),"matched_legacy_M0_M2":sum(all(r.get("legacy_equal",{}).values()) and bool(r.get("legacy_equal")) for r in primary)},
      "cases":rr,"controls":controls,"limitations":["M2 and M3 different maturity; supported legacy mapping not a proof of intrinsic architecture limits.","R1 predicate static is not numeric conformance; R1 profile math is not full CSNF contract.","M3 finite consumer reuses MS1 arithmetic and limited test-only join/cases checks, not native execution or complete model conformance.","No independent human audit; no full M0/M2/M3 equal-scope performance or ablation."]}
    Path("comparison_results.json").write_text(json.dumps(results,indent=2)+"\n")
    print("C1_COMP_RESULTS="+json.dumps(results,separators=(",",":")))
if __name__=="__main__":main()
