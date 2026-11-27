"""R10: controlled, explicit research composition, not normative owner approval.
Only exact, externally authorized method-slot replacements. No last-writer-wins.
"""
from copy import deepcopy
from closure import fields,need,qualified,digest,canon,c1,native,source_map
from interface import import_package,package_version
from closure_v1 import definition,metadata,identity,graph

VERSION="c2-approved-composition-0.1"
APPROVAL="c2-research-composition-authorization-0.1"
RECEIPT="c2-approved-composition-package-0.1"

def _changed(old,new):
    need(package_version(old["package"])==package_version(new["package"]),"OVERRIDE_PACKAGE_VERSION")
    a,b=import_package(old["package"]),import_package(new["package"])
    ca,cb=deepcopy(a["context"]),deepcopy(b["context"])
    for c in (ca,cb):
        c.pop("audit")
        c["method"].pop("id");c["method"].pop("version")
        c["study"].pop("method_ref")
    need(ca==cb,"OVERRIDE_CONTEXT_OR_SIGNATURE_DRIFT")
    need(a["interface"]["symbols"]==b["interface"]["symbols"],"OVERRIDE_SYMBOL_SIGNATURE")
    need(a["interface"]["predicates"]==b["interface"]["predicates"],"OVERRIDE_PREDICATE_SIGNATURE")
    da,db=source_map(a["native_canonical"]),source_map(b["native_canonical"])
    for d in (da,db):d.pop("description",None)
    ea,eb=da.pop("expressions",{}),db.pop("expressions",{})
    need(da==db and set(ea)==set(eb),"OVERRIDE_PROTECTED_NATIVE_SECTION")
    changed=sorted(k for k in ea if ea[k]!=eb[k]);need(bool(changed),"OVERRIDE_NO_EXPRESSION_CHANGE")
    pa,pb=native(a["native_canonical"]).program,native(b["native_canonical"]).program
    # Resolved public Program includes reference bodies. Compare every
    # native predicate/assumption (including guards and transitive reads).
    need(pa.conditions==pb.conditions and pa.assumptions==pb.assumptions,"OVERRIDE_PROTECTED_NATIVE_OBLIGATION")
    # Also protect derived observable projections and state/policy symbols:
    # these express external obligations, not freely replaceable methods.
    protected={k for k,x in old["bindings"].items() if x["kind"]=="OBSERVABLE"}
    protected|={x["symbol"] for x in old["policies"]+old["states"]}
    sig={z["symbol_id"]:z for z in a["interface"]["symbols"].values()}
    for k in protected:
        n=sig[k]["native_name"]
        if n in pa.expressions:need(pa.expressions[n]==pb.expressions[n],"OVERRIDE_PROTECTED_OBSERVABLE")
    return changed

def compose(base,base_pin,request,request_pin,authorization,authorization_pin):
    original=definition.admit(base,base_pin)
    fields(request,("schema","base_ref","overrides"),"OVERRIDE_REQUEST_FIELDS")
    need(request["schema"]==VERSION and digest(request)==request_pin and request["base_ref"]==base_pin,"OVERRIDE_REQUEST_PIN")
    fields(authorization,("schema","base_ref","request_ref","approvals","decision_scope"),"OVERRIDE_AUTHORIZATION_FIELDS")
    need(authorization["schema"]==APPROVAL and digest(authorization)==authorization_pin and authorization["base_ref"]==base_pin and authorization["request_ref"]==request_pin,"OVERRIDE_AUTHORIZATION_PIN")
    need(authorization["decision_scope"]=="NON_NORMATIVE_RESEARCH_ONLY","OVERRIDE_AUTHORITY_PROMOTION")
    base_slots=metadata.index(base["slots"]); tables=metadata.validate(base["frame"]);src=graph.sources(base,tables)
    rows=metadata.index(request["overrides"]);approvals=metadata.index(authorization["approvals"])
    need(bool(rows) and set(rows)==set(approvals),"OVERRIDE_APPROVAL_COVERAGE")
    targets=set(); replacements={}; receipts=[]
    for k,r in rows.items():
        fields(r,("id","slot","expected_old","replacement","allowed_expressions"),"OVERRIDE_FIELDS")
        need(qualified(k) and r["slot"] in base_slots and r["slot"] not in targets,"OVERRIDE_DUPLICATE_OR_UNKNOWN_TARGET");targets.add(r["slot"])
        old=base_slots[r["slot"]];new=r["replacement"];fields(new,definition.STATIC_FIELDS,"OVERRIDE_REPLACEMENT_FIELDS")
        need(r["expected_old"]==digest(old),"OVERRIDE_STALE_BASE")
        a=approvals[k];fields(a,("id","slot","old_ref","new_ref","allowed_expressions","authority_ref","source_sha256","decision","reason"),"OVERRIDE_APPROVAL_FIELDS")
        need(a["decision"]=="APPROVED_RESEARCH_OVERRIDE" and type(a["reason"]) is str and bool(a["reason"]),"OVERRIDE_NOT_AUTHORIZED")
        # A separate, externally pinned authorization is required. Source
        # bytes are pinned in the base and only declared research authorities
        # may be used. No assertion of real-world authority authenticity.
        auth=tables["authorities"].get(a["authority_ref"])
        need(auth is not None and auth["role"] in ("SOURCE","PROVENANCE") and a["authority_ref"] in src and a["authority_ref"] in tables["slots"][r["slot"]]["authority_refs"] and src[a["authority_ref"]]["sha256"]==a["source_sha256"],"OVERRIDE_AUTHORITY_SCOPE")
        need(a["slot"]==r["slot"] and a["old_ref"]==digest(old) and a["new_ref"]==digest(new) and a["allowed_expressions"]==r["allowed_expressions"],"OVERRIDE_APPROVAL_TARGET")
        # No loss or replacement of any frame, assertion, verification,
        # relation, observable, scope, normativity, or data/evidence policy.
        need(all(old[x]==new[x] for x in definition.STATIC_FIELDS if x not in ("package","profile","source_ref")),"OVERRIDE_PROTECTED_FIELD")
        need(new["source_ref"] in src and new["source_ref"] in tables["slots"][r["slot"]]["authority_refs"],"OVERRIDE_METHOD_SOURCE")
        p,q=old["profile"],new["profile"]
        allowed={"id","version","native_signature","native_semantic_identity","source_ref","source_sha256"}
        need({x:v for x,v in p.items() if x not in allowed}=={x:v for x,v in q.items() if x not in allowed},"OVERRIDE_PROFILE_POLICY")
        need((p["id"],p["version"])!=(q["id"],q["version"]),"OVERRIDE_METHOD_VERSION")
        changed=_changed(old,new)
        need(type(r["allowed_expressions"]) is list and r["allowed_expressions"]==sorted(set(r["allowed_expressions"])) and changed==r["allowed_expressions"],"OVERRIDE_EXPRESSION_SCOPE")
        replacements[r["slot"]]=deepcopy(new)
        receipts.append({"id":k,"slot":r["slot"],"old_ref":digest(old),"new_ref":digest(new),"changed_expressions":changed,"authority_ref":a["authority_ref"],"source_sha256":a["source_sha256"],"decision":a["decision"],"reason":a["reason"]})
    effective=deepcopy(base)
    effective["slots"]=[replacements.get(r["id"],r) for r in effective["slots"]]
    result=definition.admit(effective,digest(effective))
    out={"schema":RECEIPT,"effective_definition":effective,"effective_pin":digest(effective),"base_semantic_identity":original["semantic_identity"],"effective_receipt":result,"precedence":"EXPLICIT_DISJOINT_REPLACEMENT_ONLY","overrides":sorted(receipts,key=lambda r:r["slot"]),"owner":"OWNER_TBD","conformance":"NOT_PROVED","authority_authenticity":"UNVERIFIED","research_only":True}
    out["audit_identity"]=digest({"base_pin":base_pin,"request_pin":request_pin,"authorization_pin":authorization_pin,"receipt":out})
    return out

def export(base,base_pin,request,request_pin,authorization,authorization_pin):
    r=compose(base,base_pin,request,request_pin,authorization,authorization_pin)
    return canon({"schema":RECEIPT,"base":base,"request":request,"authorization":authorization,"receipt":r})

def reimport(text,base_pin,request_pin,authorization_pin):
    p=c1.parse(text);fields(p,("schema","base","request","authorization","receipt"),"OVERRIDE_CANONICAL_FIELDS")
    need(p["schema"]==RECEIPT and export(p["base"],base_pin,p["request"],request_pin,p["authorization"],authorization_pin)==text,"OVERRIDE_CANONICAL_TAMPER")
    return p
