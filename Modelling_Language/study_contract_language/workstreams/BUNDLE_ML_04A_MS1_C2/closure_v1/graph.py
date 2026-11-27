"""General multi-profile Study Contract integration, native mathspec authority only.
Source allowlists are explicitly pinned by the caller; not normative approval.
"""
from copy import deepcopy
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import mathspec.program as mp
from closure import need,fields,qualified,exact,digest,text_hash,canon,c1,Reject
from WS_B.methods import validate as validate_method
from closure_v1 import metadata as md,obligations as ob,identity

VERSION="c2-closure-study-contract-0.1"
INPUT="c2-closure-study-input-0.1"
def pins(obj):
    # Test/authoring helper only; evaluate requires the external digest.
    return {"schema":"c2-research-trust-0.1","study":obj["study"]["id"],"version":obj["study"]["version"],
            "frame":digest(obj["frame"]),"slots":{x["id"]:digest(x) for x in obj["slots"]},
            "sources":{x["id"]:x["sha256"] for x in obj["sources"]},"disclosures":digest(obj["disclosures"]),
            "events":digest(obj["events"]),"authority":"OWNER_TBD","publication":"SYNTHETIC"}
def trust(obj,expected):
    t=obj["trust"];need(type(expected) is str and digest(t)==expected,"TRUST_PIN_MISMATCH")
    need(t==pins(obj),"TRUST_CONTEXT_MISMATCH")
    s=obj["study"];fields(s,("id","version","frame_ref","slot_refs","owner"),"STUDY_FIELDS")
    need(qualified(s["id"]) and type(s["version"]) is str and bool(s["version"]) and s["owner"]=="OWNER_TBD","STUDY_IDENTITY")
    need(s["frame_ref"]==t["frame"] and s["slot_refs"]==t["slots"],"STUDY_CONTEXT_NOT_PERMITTED")
    return t
def sources(obj,tables):
    out=md.index(obj["sources"]);auth=tables["authorities"]
    need(set(out)=={k for k,a in auth.items() if a["role"] in ("SOURCE","PROVENANCE")},"SOURCE_COVERAGE")
    for k,r in out.items():
        fields(r,("id","immutable_ref","revision","content","sha256"),"SOURCE_FIELDS")
        need(r["immutable_ref"]==auth[k]["immutable_ref"] and r["revision"]==auth[k]["revision"] and type(r["content"]) is str and text_hash(r["content"])==r["sha256"],"SOURCE_BYTES")
    return out
def disclosures(obj,tables,source):
    rows=md.index(obj["disclosures"]);seen=set()
    for k,r in rows.items():
        fields(r,("id","variation","choice","source_ref"),"DISCLOSURE_FIELDS")
        v=tables["variations"].get(r["variation"])
        need(v is not None and r["variation"] not in seen and r["choice"] in v["alternatives"],"VARIATION_DISCLOSURE")
        need(r["source_ref"] in source and r["source_ref"] in v["source_refs"],"VARIATION_SOURCE")
        seen.add(r["variation"])
    need(seen==set(tables["variations"]),"VARIATION_DISCLOSURE_COVERAGE")
    return rows
def value_type(s):
    return {"int":"INTEGER","bool":"BOOLEAN","float":"REAL","rational":"REAL"}[s["dtype"]]
def signature(s,r):
    need(s["domain_ids"]==r["axes"] and md.qcompat(s["quantity"],r["quantity"]) and value_type(s)==r["value_type"],"BINDING_SIGNATURE")
def values(bound,sym):
    s,rows=bound.table(sym)
    # Canonical coordinate identity; domain order in the signature is explicit.
    return [{"key":list(k),"value":str(v.value)} for k,v in sorted(rows.items())]
def read_params(n):
    if type(n) is mp.ParameterReference:return {n.name}
    return set().union(*(read_params(c) for c in mp.children(n)))
def validate_bindings(row,bound,slot):
    tb=bound.tables;sig=bound.symbols;b=row["bindings"]
    need(type(b) is dict and set(b)==set(sig),"SYMBOL_BINDING_COVERAGE")
    used_in=set();used_obs=set();used_out=set();producer={};upstream={};observations={}
    external=set(row["profile"].get("output_contract",{}).get("external",[]))
    derived={k for k,z in sig.items() if z["role"]=="DERIVED_EXPRESSION"}
    need(not derived or "output_contract" in row["profile"],"OUTPUT_CONTRACT_REQUIRED")
    for k,s in sig.items():
        x=b[k];fields(x,("kind","ref"),"SYMBOL_BINDING_FIELDS")
        role=s["role"];kind=x["kind"];ref=x["ref"]
        if role=="INPUT":
            need(kind in ("INPUT","UPSTREAM"),"SYMBOL_ROLE")
            t=tb["inputs"] if kind=="INPUT" else tb["outputs"];need(ref in t and ref in slot["inputs"],"SLOT_INPUT_BINDING")
            signature(s,t[ref]);used_in.add(ref)
            if kind=="UPSTREAM":upstream[k]=ref
        elif role in ("OBSERVABLE","EXTERNAL_WITNESS"):
            need(kind=="OBSERVABLE" and ref in tb["observables"] and ref in slot["observables"],"SLOT_OBSERVABLE_BINDING")
            r=tb["observables"][ref];need(r["projection"]=="IDENTITY","OBSERVABLE_PROJECTION")
            signature(s,r);used_obs.add(ref);observations[k]=ref
        elif role=="METHOD_PARAMETER":
            need(kind=="PARAMETER" and ref==k,"PARAMETER_BINDING")
        elif role=="DERIVED_EXPRESSION":
            if k in external:
                if kind=="OUTPUT":
                    need(ref in tb["outputs"] and ref in slot["outputs"],"SLOT_OUTPUT_BINDING")
                    signature(s,tb["outputs"][ref]);need(ref not in used_out,"DUPLICATE_OUTPUT_PRODUCER");used_out.add(ref);producer[ref]=k
                elif kind=="OBSERVABLE":
                    need(ref in tb["observables"] and ref in slot["observables"] and tb["observables"][ref]["projection"]=="NATIVE_EXPRESSION","OBSERVABLE_PROJECTION")
                    signature(s,tb["observables"][ref]);used_obs.add(ref);observations[k]=ref
                else:need(False,"OUTPUT_BINDING")
            else:need(kind=="INTERMEDIATE" and ref==k,"INTERMEDIATE_NOT_EXTERNAL")
        else:need(False,"SYMBOL_ROLE")
    need(used_in==set(slot["inputs"]) and used_obs==set(slot["observables"]) and used_out==set(slot["outputs"]),"SLOT_BINDING_COVERAGE")
    for k,ref in observations.items():
        r=tb["observables"][ref]
        if r["projection"]=="NATIVE_EXPRESSION":
            n=sig[k]["native_name"];names=read_params(bound.program.expressions[n].expression)
            subjects={tb["observables"][v]["subject"] for s,v in observations.items() if sig[s]["native_name"] in names and sig[s]["role"]!="DERIVED_EXPRESSION"}
            need(r["subject"] in subjects,"OBSERVABLE_SUBJECT_PROJECTION")
    scope=tb["scopes"][slot["scope"]]
    need(all(set(z["domain_ids"])<=set(scope["domains"]) for z in sig.values()),"SLOT_SCOPE_ESCAPE")
    need(all(tb["observables"][r]["subject"] in scope["subjects"] for r in observations.values()),"SLOT_SUBJECT_SCOPE")
    # Map duration weights to actual physical interval durations, not sample weights.
    for k,role in row["profile"]["input_roles"].items():
        if role=="DURATION_WEIGHT":
            s=sig[k];ax=s["domain_ids"];need(len(ax)==1,"DURATION_BINDING")
            ch=[r for r in tb["chronologies"].values() if r["domain"]==ax[0]]
            need(len(ch)==1,"DURATION_BINDING")
            actual=values(bound,k);expected={r["label"]:exact(r["duration_h"]) for r in ch[0]["intervals"]}
            need(all(exact(x["value"])==expected[x["key"][0]] for x in actual),"DURATION_BINDING")
    return {"producers":producer,"upstream":upstream,"observables":observations}
def comparison(row,bound,binding,source,external):
    tb=bound.tables;spec=md.index(row["comparisons"])
    pairs={x["id"]:x for x in row["profile"]["counterfactual_pairs"]};ctx={x["id"]:x for x in row["case_context"]["pairs"]}
    need(set(spec)==set(pairs)==set(ctx),"COUNTERFACTUAL_COVERAGE")
    used=set();receipts=[]
    for k,r in spec.items():
        fields(r,("id","policy","source_ref"),"COMPARISON_BINDING_FIELDS")
        p=tb["comparisons"].get(r["policy"]);need(p is not None and p["id"] not in used,"COUNTERFACTUAL_POLICY")
        need(r["source_ref"] in source and r["source_ref"] in p["authority_refs"],"COUNTERFACTUAL_SOURCE")
        used.add(p["id"]);rel=tb["relations"][p["relation"]];pr=pairs[k];obs=binding["observables"]
        need(pr["reference"] in obs and pr["alternative"] in obs,"COUNTERFACTUAL_OBSERVABLE")
        need(tb["observables"][obs[pr["reference"]]]["subject"]==rel["to"] and tb["observables"][obs[pr["alternative"]]]["subject"]==rel["from"],"COUNTERFACTUAL_RELATION")
        def compare(fields_):
            a,b={},{}
            for field,x in fields_.items():
                need(x["reference"] in external and x["alternative"] in external,"COUNTERFACTUAL_DATA_COVERAGE")
                a[field]=digest(external[x["reference"]]);b[field]=digest(external[x["alternative"]])
            return a,b
        a,b=compare(p["exogenous"]);need(a==b,"COUNTERFACTUAL_EXOGENEITY")
        need(ctx[k]["reference_exogenous"]==a and ctx[k]["alternative_exogenous"]==b,"COUNTERFACTUAL_CONTEXT_CONTENT")
        x,y=compare(p["project"]);changed=sorted(f for f in x if x[f]!=y[f]);need(set(changed)<=set(p["allowed_changes"]),"UNAUTHORIZED_PROJECT_CHANGE")
        receipts.append({"pair":k,"policy":p["id"],"exogenous":a,"project_reference":x,"project_alternative":y,"changed":changed,"authority":"RESEARCH_ASSUMPTION","owner":"OWNER_TBD"})
    return used,receipts
def verify_requests(row,bound,slot,source,obligations,policies,boundaries):
    subjects={a["id"] for a in row["assertions"] if a["modality"]!="MAY"}|set(slot["outputs"])|{a["id"] for a in row["policies"]}|{a["id"] for a in row["states"]}
    actual=md.index(row["verification"]);seen=set();pending=[]
    statuses={a["id"]:a["finite_status"] for a in obligations["assertions"]}
    statuses.update({a["id"]:a["status"] for a in policies+boundaries});statuses.update({k:"FINITE_OUTPUT_COMPUTED" for k in slot["outputs"]})
    for k,r in actual.items():
        fields(r,("id","subject","kind","oracle_ref","status"),"VERIFICATION_FIELDS")
        need(r["subject"] in subjects and r["subject"] not in seen and r["status"]=="NOT_EXECUTED","VERIFICATION_COVERAGE_OR_PROMOTION")
        need(r["oracle_ref"] in source and r["kind"] in ("FINITE_OBSERVATION","BEHAVIORAL","FORMAL_PROOF","TOOL_CONFORMANCE"),"VERIFICATION_REFERENCE")
        seen.add(r["subject"])
        pending.append({"request":k,"subject":r["subject"],"requested_kind":r["kind"],"oracle_ref":r["oracle_ref"],"status":("BLOCKED" if statuses[r["subject"]]=="BLOCKED" else "NOT_APPLICABLE" if statuses[r["subject"]]=="NOT_APPLICABLE" else "FINITE_CHECK_EXECUTED_UNJUDGED") if r["kind"]=="FINITE_OBSERVATION" else "NOT_EXECUTED","observed_status":statuses[r["subject"]] if r["kind"]=="FINITE_OBSERVATION" else None})
    need(seen==subjects,"VERIFICATION_COVERAGE")
    return sorted(pending,key=lambda r:r["request"])
def evaluate(obj,expected_trust):
    fields(obj,("schema","study","frame","slots","sources","disclosures","events","trust"),"CLOSURE_FIELDS")
    need(obj["schema"]==INPUT,"CLOSURE_VERSION");t=trust(obj,expected_trust)
    tables=md.validate(obj["frame"]);source=sources(obj,tables);disc=disclosures(obj,tables,source)
    slots=md.index(obj["slots"]);need(bool(slots) and set(slots)==set(tables["slots"]),"STUDY_SLOT_COVERAGE")
    prepared={};producers={};external={};observed={};bound_obs=set()
    global_ids={obj["frame"]["id"],*(k for t in tables.values() for k in t)}
    for r in [*obj["events"],*obj["disclosures"]]:
        need(qualified(r["id"]) and r["id"] not in global_ids,"DUPLICATE_ID");global_ids.add(r["id"])
    # Admit and type-check every slot before evaluating any of them.
    for k,row in slots.items():
        fields(row,("id","package","profile","study","source_ref","data","case_context","bindings","assertions","witnesses","policies","states","comparisons","verification","ledger"),"SLOT_INSTANCE_FIELDS")
        slot=tables["slots"][k];p=row["profile"]
        for r in [*row["assertions"],*row["witnesses"],*row["policies"],*row["states"],*row["verification"],*(row["ledger"]["contributions"] if row["ledger"] is not None else [])]:
            need(qualified(r["id"]) and r["id"] not in global_ids,"DUPLICATE_ID");global_ids.add(r["id"])
        need(row["source_ref"] in source and row["source_ref"] in slot["authority_refs"],"METHOD_SOURCE_AUTHORITY")
        src=source[row["source_ref"]];need(p["source_ref"]==src["immutable_ref"] and p["source_sha256"]==src["sha256"],"METHOD_SOURCE")
        need("ledger" not in p,"USE_VERSIONED_NATIVE_LEDGER")
        b=ob.Bound(row["package"],tables,row["data"])
        need(b.leaf["context"]["study"]["id"]==obj["study"]["id"] and b.leaf["context"]["study"]["version"]==obj["study"]["version"],"STUDY_IDENTITY")
        bind=validate_bindings(row,b,slot)
        for n,z in b.leaf["context"]["conversions"].items():
            matches=[x for x in source.values() if x["immutable_ref"]==z["source_ref"] and x["sha256"]==z["source_sha256"] and x["revision"]==z["version"]]
            need(len(matches)==1,"CONVERSION_SOURCE_BINDING")
        for out,sym in bind["producers"].items():
            need(out not in producers,"DUPLICATE_OUTPUT_PRODUCER");producers[out]=(k,sym)
        for sym,x in row["bindings"].items():
            if x["kind"]=="INPUT":
                r=x["ref"];v=values(b,sym);need(r not in external or external[r]==v,"SHARED_DATA_DRIFT");external[r]=v
        for sym,r in bind["observables"].items():
            v=values(b,sym);need(r not in observed or observed[r]==v,"SHARED_OBSERVABLE_DRIFT");observed[r]=v;bound_obs.add(r)
        prepared[k]=(row,b,bind)
    need(set(producers)==set(tables["outputs"]) and set(external)==set(tables["inputs"]) and bound_obs==set(tables["observables"]),"FRAME_BINDING_COVERAGE")
    proc={r["slot"]:r for r in tables["processes"].values()};deps={}
    for k,(row,b,bind) in prepared.items():
        actual={producers[ref][0] for ref in bind["upstream"].values()}
        need(k not in actual and set(proc[k]["depends_on"])=={proc[x]["id"] for x in actual},"PROCESS_DEPENDENCY_BINDING")
        deps[k]=actual
    order=[];pending=set(slots)
    while pending:
        ready=sorted(k for k in pending if deps[k]<=set(order));need(bool(ready),"METHOD_DEPENDENCY_CYCLE")
        order+=ready;pending-=set(ready)
    from closure_v1 import ledger
    events=ledger.validate_events(obj["events"],tables,source)
    results={};out_values={};out_lineage={};used_comparisons=set();event_usage=set();sem_slots={}
    for k in order:
        row,b,bind=prepared[k];slot=tables["slots"][k];src=source[row["source_ref"]]
        for sym,ref in bind["upstream"].items():
            need(values(b,sym)==out_values[ref],"UPSTREAM_RESULT_BINDING")
        used,comp=comparison(row,b,bind,source,external)
        need(not used_comparisons&used,"DUPLICATE_COMPARISON_POLICY");used_comparisons|=used
        # Original C2 exact method/profile/weight/range/context validation.
        m=validate_method(row["package"],row["data"],row["profile"],row["study"],src["content"],row["case_context"])
        # Guards, assumptions and metadata scopes are validated before any verdict.
        native_required={z["id"] for z in b.leaf["interface"]["predicates"].values() if z["role"] in ("PREDICATE","DATA_ASSUMPTION")}
        need({a["predicate"]["predicate_id"] for a in row["assertions"]}==native_required,"PREDICATE_COVERAGE")
        if row["assertions"]:
            specs=ob.validate(b,row["assertions"])
            for a in specs.values():
                z=a["row"];need(z["scope"]==slot["scope"] or set(tables["scopes"][z["scope"]]["domains"])<=set(tables["scopes"][slot["scope"]]["domains"]),"ASSERTION_SLOT_SCOPE")
                allowed=set(tables["scopes"][z["scope"]]["subjects"])
                need(all(tables["observables"][bind["observables"][s]]["subject"] in allowed for s in a["predicate"]["required_symbols"] if s in bind["observables"]),"ASSERTION_SUBJECT_SCOPE")
            for w in row["witnesses"]:need(w["source_ref"] in source,"WITNESS_SOURCE_BYTES")
            obligations=ob.evaluate(b,row["assertions"],row["witnesses"])
        else:
            need(not row["witnesses"] and not row["states"],"UNBOUND_EVIDENCE_OR_STATE");obligations={"status":"NOT_APPLICABLE","assertions":[],"conformance":"NOT_PROVED"}
        policy=ob.nonanticipativity(b,row["policies"]);states=ob.boundaries(b,row["assertions"],row["states"]) if row["states"] else []
        incoming={sym:out_lineage[ref] for sym,ref in bind["upstream"].items()}
        required=any(tables["outputs"][r]["contribution_policy"]=="REQUIRED" for r in bind["producers"])
        need(not required or row["ledger"] is not None,"LEDGER_REQUIRED")
        need(row["ledger"] is not None or not any(any(v for v in x.values()) for x in incoming.values()),"UPSTREAM_LINEAGE_REQUIRED")
        lr,used_events=ledger.evaluate(b,row["ledger"],events,incoming,bind["observables"]) if row["ledger"] is not None else ({},set())
        event_usage|=used_events
        for ref,sym in bind["producers"].items():
            out_values[ref]=values(b,sym)
            n=b.symbols[sym]["native_name"];out_lineage[ref]=lr.get(n,{})
            if tables["outputs"][ref]["contribution_policy"]=="REQUIRED":need(n in lr and n in row["ledger"]["expected"] and bool(row["ledger"]["expected"][n]) and any(lr[n].values()),"CONTRIBUTION_COMPLETENESS")
        verification=verify_requests(row,b,slot,source,obligations,policy,states)
        results[k]={"method":m,"obligations":obligations,"policies":policy,"boundaries":states,"comparisons":comp,
                    "lineage":ledger.receipt(lr),"verification":verification,"data_identity":b.data_identity,"owner":"OWNER_TBD"}
        sem_slots[k]={"math":identity.mathematics(row["package"]),"profile":identity.profile(row["profile"],row["package"]),"data":b.data_identity,
                      "bindings":row["bindings"],"assertions":[identity.assertion(a) for a in identity.byid(row["assertions"])],
                      "policies":identity.byid(row["policies"]),"states":identity.byid(row["states"]),"comparisons":identity.byid(row["comparisons"]),
                      "case_context":{**row["case_context"],"pairs":identity.byid(row["case_context"]["pairs"])},
                      "verification":identity.byid(row["verification"]),"ledger":ledger.semantic(row["ledger"])}
    need(used_comparisons==set(tables["comparisons"]),"COUNTERFACTUAL_COVERAGE")
    need(event_usage==set(events) and {e for rows in out_lineage.values() for c in rows.values() for e in c}==set(events),"EVENT_COVERAGE")
    sem=digest({"schema":VERSION,"frame":identity.frame(obj["frame"]),"study":{"id":obj["study"]["id"],"version":obj["study"]["version"]},"slots":sem_slots,
                "events":identity.byid(obj["events"]),"disclosures":identity.byid(obj["disclosures"])})
    negative=any(r["obligations"]["status"]=="FINITE_COUNTEREXAMPLE" or any(p["status"]=="FINITE_COUNTEREXAMPLE" for p in r["policies"]) for r in results.values())
    blocked=any(r["obligations"]["status"]=="BLOCKED" for r in results.values())
    receipt={"schema":VERSION,"semantic_identity":sem,"study":obj["study"]["id"],"execution_order":order,"slots":results,"outputs":out_values,
             "finite_status":"FINITE_COUNTEREXAMPLE" if negative else "BLOCKED" if blocked else "FINITE_OBSERVATIONS_ONLY",
             "owner":"OWNER_TBD","conformance":"NOT_PROVED","authority_authenticity":"UNVERIFIED","scope":"BOUNDED_NATIVE_RESEARCH"}
    receipt["audit_identity"]=digest({"input_as_received":obj,"receipt":receipt,"trust_root":expected_trust})
    return receipt
def export(obj,trust_pin):
    return canon({"schema":VERSION,"input":obj,"receipt":evaluate(obj,trust_pin)})
def reimport(text,trust_pin):
    x=c1.parse(text);fields(x,("schema","input","receipt"),"CLOSURE_CANONICAL_FIELDS")
    need(x["schema"]==VERSION and export(x["input"],trust_pin)==text,"CANONICAL_TAMPER_OR_NONCANONICAL")
    return x
