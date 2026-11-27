"""Canonical static Study Contract definition, independent of data availability.
Instance binding and evidence are separate. No solver or code generator.
"""
from copy import deepcopy
from fractions import Fraction as F
from closure import need,fields,qualified,exact,digest,text_hash,canon,c1
from interface import resolve_method
from WS_B.methods import check_static
from closure_v1 import graph,metadata as md,obligations as ob,identity,ledger
from closure_v1.diagnostics import call as checked,pointer,scope as diagnostic_scope

DEF="c2-closure-definition-0.2"
INST="c2-closure-instance-0.2"
PACKAGE="c2-closure-contract-package-0.3"
STATIC_FIELDS=("id","package","profile","source_ref","bindings","assertions","policies","states","comparisons","verification","ledger")
INSTANCE_FIELDS=("id","profile_ref","package_ref","data_status","data","snapshot_digest","case_context","witnesses","contributions","expected_events")

def ledger_static(spec,bound,bind):
    if spec is None:return
    fields(spec,("bindings","key_axes","policy","global_disjoint","coverage"),"LEDGER_DEFINITION_FIELDS")
    sig={z["native_name"]:z for z in bound.symbols.values() if z["role"] not in ("DERIVED_EXPRESSION","METHOD_PARAMETER")}
    need(set(spec["bindings"])==set(sig)==set(spec["key_axes"]),"LEDGER_INPUT_BINDINGS")
    for n,r in spec["bindings"].items():
        fields(r,("role","observable","case","data_ref"),"LEDGER_BINDING_FIELDS")
        s=sig[n];k=s["symbol_id"];ax=spec["key_axes"][n]
        need(type(ax) is list and len(ax)==len(set(ax)) and set(ax)==set(s["domain_ids"]),"LEDGER_KEY_AXES")
        if r["role"]=="contribution":
            need(k in bind["observables"] and r["observable"]==bind["observables"][k] and r["case"]==bound.tables["observables"][r["observable"]]["subject"] and r["data_ref"]=="","CONTRIBUTION_SIGNATURE")
        else:need(r["role"]=="auxiliary" and r["data_ref"]==k and r["observable"]==r["case"]=="","AUXILIARY_SIGNATURE")
    rules=spec["policy"];names=set(bound.program.expressions)
    need(type(rules) is dict and set(rules)==names and all(v in ("DISJOINT","ALLOW_REUSE") for v in rules.values()),"LEDGER_POLICY_SCOPE")
    for key in ("global_disjoint","coverage"):md.refs(spec[key],rules,"LEDGER_EXPECTED_SCOPE",False)
    for r,s in bind["producers"].items():
        if bound.tables["outputs"][r]["contribution_policy"]=="REQUIRED":
            need(bound.symbols[s]["native_name"] in spec["coverage"],"CONTRIBUTION_COVERAGE_REQUIRED")

def source_refs(xs,source):md.refs(xs,source,"SOURCE_REFERENCE")
def requirement_design(req,tables,source,prepared):
    fields(req,("boundary","data_contracts","process_roles","normativity","models","comparisons","time_policies"),"REQUIREMENT_DESIGN_FIELDS")
    b=req["boundary"];fields(b,("included","environment","space_domains","functional_scopes","authority_refs"),"SYSTEM_BOUNDARY_FIELDS")
    subs={**tables["components"],**tables["ports"],**tables["referents"]}
    md.refs(b["included"],subs,"SYSTEM_BOUNDARY",False);md.refs(b["environment"],subs,"SYSTEM_BOUNDARY",False)
    need(not set(b["included"])&set(b["environment"]) and set(b["included"])|set(b["environment"])==set(subs),"SYSTEM_BOUNDARY_COVERAGE")
    md.refs(b["space_domains"],tables["domains"],"GEOGRAPHICAL_DOMAIN",False)
    need(all(tables["domains"][k]["kind"]=="space" for k in b["space_domains"]),"GEOGRAPHICAL_DOMAIN")
    md.refs(b["functional_scopes"],tables["scopes"],"FUNCTIONAL_SCOPE");source_refs(b["authority_refs"],source)
    process=req["process_roles"];need(type(process) is dict and set(process)==set(tables["processes"]) and all(v in ("PREPROCESS","EVALUATION","POSTPROCESS","VALIDATION") for v in process.values()),"PROCESS_ROLE_COVERAGE")
    # Normativity applies to every actual obligation; no owner promotion.
    ass={a["id"]:(k,a) for k,(row,_,_) in prepared.items() for a in row["assertions"]}
    norm=req["normativity"];need(type(norm) is dict and set(norm)==set(ass),"NORMATIVITY_COVERAGE")
    for k,n in norm.items():
        fields(n,("status","authority_ref"),"NORMATIVITY_FIELDS")
        need(n["status"] in ("RESEARCH_ASSUMPTION","INFORMATIVE","NORMATIVE_REQUIREMENT_PENDING_OWNER") and n["authority_ref"] in ass[k][1]["authority_refs"],"AUTHORITY_PROMOTION")
        need(n["status"]!="INFORMATIVE" or ass[k][1]["modality"]=="MAY","INFORMATIVE_NOT_OBLIGATION")
    data=md.index(req["data_contracts"])
    ext={**tables["inputs"],**tables["context_fields"],**{k:v for k,v in tables["observables"].items() if v["projection"]=="IDENTITY"}}
    need(set(data)==set(ext),"DATA_CONTRACT_COVERAGE")
    for k,r in data.items():
        fields(r,("id","source_ref","license_ref","access_ref","reproducibility","quality","quality_assertions","missing","conversion"),"DATA_CONTRACT_FIELDS")
        source_refs([r["source_ref"]],source);source_refs([r["license_ref"]],source);source_refs([r["access_ref"]],source)
        need(r["reproducibility"]=="PINNED_SNAPSHOT" and r["missing"]=="BLOCK","DATA_GOVERNANCE_POLICY")
        need(r["quality"] in ("TYPE_AND_COMPLETE_SUPPORT","NATIVE_ASSERTION"),"DATA_QUALITY_POLICY")
        md.refs(r["quality_assertions"],ass,"QUALITY_ASSERTION",False)
        need((r["quality"]=="NATIVE_ASSERTION")==bool(r["quality_assertions"]),"QUALITY_ASSERTION_COVERAGE")
        for a in r["quality_assertions"]:
            slot,ar=ass[a];row,bd,_=prepared[slot]
            pred=bd.resolve(ar["predicate"],("PREDICATE","DATA_ASSUMPTION"))
            need(any(row["bindings"][s]["ref"]==k for s in pred["required_symbols"]),"QUALITY_ASSERTION_BINDING")
        if k in tables["context_fields"]:need(r["conversion"] is None and r["quality"]=="TYPE_AND_COMPLETE_SUPPORT","CONTEXT_NOT_MATHEMATICS")
        else:
            cv=r["conversion"]
            validate_conversion(cv,ext[k]["quantity"],source)
            if cv is not None and cv["kind"]=="SIGN_CONVENTION":
                src=tables["observables"].get(cv["source_observable"])
                need(src is not None and src["projection"]=="IDENTITY" and src["quantity"]==cv["source_quantity"]
                     and src["axes"]==ext[k]["axes"] and src["value_type"]==ext[k]["value_type"],"SIGN_CONVERSION_SOURCE_BINDING")
    models=md.index(req["models"]);implementations=set()
    for k,m in models.items():
        fields(m,("id","implementation_ref","source_ref","license_ref","access_ref","observables","variations"),"MODEL_FIELDS")
        need(type(m["implementation_ref"]) is str and bool(m["implementation_ref"]) and m["implementation_ref"] not in implementations,"MODEL_IMPLEMENTATION_ALIAS");implementations.add(m["implementation_ref"])
        for f in ("source_ref","license_ref","access_ref"):source_refs([m[f]],source)
        md.refs(m["observables"],tables["observables"],"MODEL_OBSERVABLE");md.refs(m["variations"],tables["variations"],"MODEL_VARIATION",False)
    for r in tables["referents"].values():
        if "model_id" in r:need(r["model_id"] in models,"CASE_MODEL_REFERENCE")
    for r in tables["report_requests"].values():source_refs([r["oracle_ref"]],source)
    comps=md.index(req["comparisons"])
    for k,r in comps.items():
        fields(r,("id","models","metric_outputs","decision_assertions","tolerances","sensitivity_domains","selection_policy","equivalence_target","oracle_ref","authority_refs"),"MODEL_COMPARISON_FIELDS")
        need(len(md.refs(r["models"],models,"MODEL_COMPARISON_MODELS"))>=2,"MODEL_COMPARISON_MODELS")
        md.refs(r["metric_outputs"],tables["outputs"],"METRIC_OUTPUT");md.refs(r["decision_assertions"],ass,"DECISION_ASSERTION")
        md.refs(r["sensitivity_domains"],tables["domains"],"SENSITIVITY_DOMAIN",False)
        need(r["selection_policy"] in ("ALL_ADMISSIBLE","DECLARED_NATIVE_SELECTOR","REPORT_RANGE") and r["equivalence_target"] in ("E1","E2","E3","E4","E5"),"COMPARISON_POLICY")
        source_refs([r["oracle_ref"]],source);source_refs(r["authority_refs"],source)
        allobs=[x for m in r["models"] for x in models[m]["observables"]]
        need(len(allobs)==len(set(allobs)),"MODEL_OBSERVATION_ALIAS")
        # A common projection is a typed signature, not identity of internal variables.
        first=models[r["models"][0]]["observables"]
        def shape(o):
            z=tables["observables"][o]
            return digest([z["quantity"],z["axes"],z["value_type"]])
        wanted=sorted(shape(o) for o in first)
        need(all(sorted(shape(o) for o in models[m]["observables"])==wanted for m in r["models"]),"MODEL_PROJECTION_SIGNATURE")
        # Each metric must depend on declared projections; sensitivity coordinates
        # must actually occur in a metric. An unrelated true assertion is not a comparison.
        observed_by_metric=set();metric_dependencies={}
        for out in r["metric_outputs"]:
            owner=[(row,bd,bi) for row,bd,bi in prepared.values() if out in bi["producers"]]
            need(len(owner)==1,"METRIC_PRODUCER");row,bd,bi=owner[0]
            sym=bi["producers"][out];expr=bd.program.expressions[bd.symbols[sym]["native_name"]].expression
            names=graph.read_params(expr);deps={obs for k,obs in bi["observables"].items() if bd.symbols[k]["native_name"] in names}
            need(bool(deps&set(allobs)),"METRIC_MODEL_BINDING");observed_by_metric|=deps;metric_dependencies[out]=(row["id"],sym,names)
        need(set(allobs)<=observed_by_metric,"METRIC_MODEL_COVERAGE")
        need(set(r["sensitivity_domains"])<=set().union(*(set(tables["outputs"][o]["axes"]) for o in r["metric_outputs"])),"SENSITIVITY_METRIC_BINDING")
        for a in r["decision_assertions"]:
            slot,ar=ass[a];row,bd,bi=prepared[slot]
            pred=bd.resolve(ar["predicate"],("PREDICATE",))
            symbols={bd.symbols[k]["native_name"] for k in pred["required_symbols"]}
            need(any(slot==owner and bool(names) and names<=symbols for owner,sym,names in metric_dependencies.values()),"DECISION_METRIC_BINDING")
        if r["selection_policy"]=="DECLARED_NATIVE_SELECTOR":
            from closure_v1.selection import validate as validate_selector
            groups={}
            for aid in r["decision_assertions"]:groups.setdefault(ass[aid][0],[]).append(aid)
            found=[]
            for sk,ids in groups.items():
                row,bd,bi=prepared[sk]
                # All selector-shaped obligations in the relevant slot must
                # pair; unrelated decision assertions cannot stand in for membership.
                from closure_v1.selection import native_pair
                specs=ob.validate(bd,row["assertions"])
                if any(native_pair(bd,specs[i]) for i in ids):
                    pairs=validate_selector(bd,row["assertions"],ids)
                    for pair in pairs:
                        need(pair["candidate"] in {sym for owner,sym,_ in metric_dependencies.values() if owner==sk},"SELECTOR_METRIC_BINDING")
                    found.extend(pairs)
            need(bool(found),"SELECTOR_MEMBERSHIP_AND_ORDER_REQUIRED")
        for tol in r["tolerances"]:
            fields(tol,("slot","parameter","metric_output"),"TOLERANCE_FIELDS")
            need(tol["slot"] in prepared and tol["metric_output"] in r["metric_outputs"],"TOLERANCE_REFERENCE")
            row,bd,bi=prepared[tol["slot"]];s=bd.symbols.get(tol["parameter"])
            need(s is not None and s["role"]=="METHOD_PARAMETER" and md.qcompat(s["quantity"],tables["outputs"][tol["metric_output"]]["quantity"]),"TOLERANCE_TYPE")
            rg=row["profile"]["parameter_ranges"][tol["parameter"]]
            need("min" in rg and exact(rg["min"])>=0,"TOLERANCE_RANGE")
            need(any(ass[a][0]==tol["slot"] and tol["parameter"] in bd.resolve(ass[a][1]["predicate"],("PREDICATE",))["required_symbols"] for a in r["decision_assertions"]),"TOLERANCE_DECISION_BINDING")
    time=md.index(req["time_policies"]);td={k for k,v in tables["domains"].items() if v["kind"]=="time"}
    need(set(time)==td,"TEMPORAL_POLICY_COVERAGE")
    for k,r in time.items():
        fields(r,("id","resolution","interpolation","aggregation","rule_outputs","authority_refs"),"TEMPORAL_POLICY_FIELDS")
        need(r["resolution"] in ("EXPLICIT_INTERVALS","REPRESENTATIVE_INTERVALS") and r["interpolation"] in ("NONE","NATIVE_RULE") and r["aggregation"] in ("NONE","NATIVE_RULE"),"TEMPORAL_POLICY")
        md.refs(r["rule_outputs"],tables["outputs"],"TEMPORAL_RULE_OUTPUT",False)
        need(bool(r["rule_outputs"])==(r["interpolation"]=="NATIVE_RULE" or r["aggregation"]=="NATIVE_RULE"),"TEMPORAL_RULE_REQUIRED")
        source_refs(r["authority_refs"],source)
    return data,comps

def validate_conversion(cv,target,source):
    if cv is None:return
    from closure_v1.r1_reuse import c21,monetary
    if cv.get("kind")=="UNIT":
        fields(cv,("kind","source_unit","source_basis","factor","source_ref"),"UNIT_CONVERSION_FIELDS")
        source_refs([cv["source_ref"]],source)
        need(cv["source_basis"]==target["basis"],"CONVERSION_BASIS")
        matches=[z for (carrier,_),z in c21.UNITS.items() if carrier==target["carrier"] and cv["source_unit"] in z and target["unit"] in z]
        need(len(matches)==1,"EXPLICIT_CONVERSION_UNSUPPORTED")
        need(exact(cv["factor"])==F(matches[0][cv["source_unit"]])/F(matches[0][target["unit"]]),"CONVERSION_FACTOR")
    elif cv.get("kind")=="SIGN_CONVENTION":
        fields(cv,("kind","source_quantity","source_observable","factor","scope","source_ref"),"SIGN_CONVERSION_FIELDS")
        source_refs([cv["source_ref"]],source)
        src=cv["source_quantity"]
        from closure import quantity
        quantity(src);quantity(target)
        # Controlled charging-only transfer: same physical quantity, explicit
        # injection-positive -> unsigned nonnegative charging magnitude.
        # Neither the source port sign nor native expression typing is erased.
        need(cv["scope"]=="CHARGING_ONLY" and src["sign"]=="INJECTION" and target["sign"]=="NONE"
             and {**src,"sign":"NONE"}==target and exact(cv["factor"])==-1,"SIGN_CONVERSION_POLICY")
    elif cv.get("kind")=="ANNUAL_RATE_TO_PERIOD_AMOUNT":
        fields(cv,("kind","source_unit","source_basis","period_years","period_ref","source_ref"),"ANNUAL_INTEGRATION_FIELDS")
        source_refs([cv["source_ref"]],source);source_refs([cv["period_ref"]],source)
        need(cv["source_unit"]=="EUR/year" and target["unit"]=="EUR" and cv["source_basis"]==target["basis"] and exact(cv["period_years"])>0,"ANNUAL_INTEGRATION_BASIS")
    elif cv.get("kind")=="MONETARY":
        fields(cv,("kind","source_unit","source_basis","registry","registry_digest","rule_id","source_ref"),"MONETARY_CONVERSION_FIELDS")
        source_refs([cv["source_ref"]],source);need(cv["source_unit"]==target["unit"]=="EUR","MONETARY_UNIT")
        monetary("1",cv["source_basis"],target["basis"],cv["registry"],cv["rule_id"],cv["registry_digest"])
        rule=next(r for r in cv["registry"]["rules"] if r["id"]==cv["rule_id"])
        need(rule["source_id"]==cv["source_ref"] and rule["source_hash"]==source[cv["source_ref"]]["sha256"],"CONVERSION_SOURCE_BINDING")
    else:need(False,"CONVERSION_KIND")
def converted_rows(rows,cv,target):
    from closure_v1.r1_reuse import monetary
    need(type(rows) is list,"RAW_CONVERSION_ROWS");out=[];seen=set()
    for r in rows:
        fields(r,("key","value"),"RAW_CONVERSION_ROW")
        key=tuple(r["key"]);need(key not in seen,"DUPLICATE_COORDINATE");seen.add(key)
        v=exact(r["value"])
        if cv["kind"]=="SIGN_CONVENTION":
            need(v<=0,"SIGN_CONVERSION_CHARGING_SCOPE");v=v*exact(cv["factor"])
        elif cv["kind"]=="UNIT":v=v*exact(cv["factor"])
        elif cv["kind"]=="ANNUAL_RATE_TO_PERIOD_AMOUNT":v=v*exact(cv["period_years"])
        else:v=F(monetary(str(v),cv["source_basis"],target["basis"],cv["registry"],cv["rule_id"],cv["registry_digest"])["value"])
        out.append({"key":r["key"],"value":str(v)})
    return sorted(out,key=lambda r:r["key"])

def _admit(definition,expected_definition):
    fields(definition,("schema","study","frame","slots","sources","requirements"),"DEFINITION_FIELDS")
    need(definition["schema"]==DEF and digest(definition)==expected_definition,"DEFINITION_PIN")
    s=definition["study"];fields(s,("id","version","owner"),"STUDY_DEFINITION_FIELDS")
    need(qualified(s["id"]) and type(s["version"]) is str and bool(s["version"]) and s["owner"]=="OWNER_TBD","STUDY_IDENTITY")
    tables=checked("/frame","R00",None,(),md.validate,definition["frame"]);source=checked("/sources","R13",None,(),graph.sources,definition,tables);slots=checked("/slots","R01",None,(),md.index,definition["slots"])
    need(bool(slots) and set(slots)==set(tables["slots"]),"STUDY_SLOT_COVERAGE")
    prepared={};producers={};ext=set();obs=set();relations=set();comparison_policies=set();allids={definition["frame"]["id"],s["id"],*(k for t in tables.values() for k in t)}
    for k,row in slots.items():
        fields(row,STATIC_FIELDS,"SLOT_DEFINITION_FIELDS")
        slot=tables["slots"][k];p=row["profile"]
        need(row["source_ref"] in source and row["source_ref"] in slot["authority_refs"] and p["source_ref"]==source[row["source_ref"]]["immutable_ref"],"METHOD_SOURCE_AUTHORITY")
        need("ledger" not in p,"USE_VERSIONED_NATIVE_LEDGER")
        path=pointer("slots",next(i for i,s in enumerate(definition["slots"]) if s["id"]==k))
        sources=[source[row["source_ref"]]]
        checked(path+"/profile","R12",k,sources,check_static,row["package"],p,source[row["source_ref"]]["content"])
        b=checked(path+"/package","R00",k,sources,ob.Bound,row["package"],tables,None)
        need(b.leaf["context"]["study"]["id"]==s["id"] and b.leaf["context"]["study"]["version"]==s["version"],"STUDY_IDENTITY")
        relations|={z["id"] for z in b.leaf["context"]["relations"].values()}
        bi=checked(path+"/bindings","R01",k,sources,graph.validate_bindings,row,b,slot)
        for out,sym in bi["producers"].items():need(out not in producers,"DUPLICATE_OUTPUT_PRODUCER");producers[out]=(k,sym)
        ext|={x["ref"] for x in row["bindings"].values() if x["kind"]=="INPUT"};obs|=set(bi["observables"].values())
        for r in [*row["assertions"],*row["policies"],*row["states"],*row["verification"]]:
            need(qualified(r["id"]) and r["id"] not in allids,"DUPLICATE_ID");allids.add(r["id"])
        required={z["id"] for z in b.leaf["interface"]["predicates"].values() if z["role"] in ("PREDICATE","DATA_ASSUMPTION")}
        need({a["predicate"]["predicate_id"] for a in row["assertions"]}==required,"PREDICATE_COVERAGE")
        if row["assertions"]:
            specs=checked(path+"/assertions","R09",k,sources,ob.validate,b,row["assertions"])
            for a in specs.values():
                ar=a["row"];sc=tables["scopes"][ar["scope"]];slot_scope=tables["scopes"][slot["scope"]]
                need(set(sc["domains"])<=set(slot_scope["domains"]) and set(sc["subjects"])<=set(slot_scope["subjects"]),"ASSERTION_SLOT_SCOPE")
                need(all(tables["observables"][bi["observables"][z]]["subject"] in sc["subjects"] for z in a["predicate"]["required_symbols"] if z in bi["observables"]),"ASSERTION_SUBJECT_SCOPE")
        for po in md.index(row["policies"]).values():
            fields(po,("id","symbol","time_domain","scenario_domain","authority_refs"),"POLICY_FIELDS");md.refs(po["authority_refs"],tables["authorities"],"AUTHORITY_REQUIRED")
            sg=b.symbols.get(po["symbol"]);td,sd=po["time_domain"],po["scenario_domain"]
            need(sg is not None and td in sg["domain_ids"] and sd in sg["domain_ids"] and td!=sd,"POLICY_AXES")
            need(any(i["time_domain"]==td and i["scenario_domain"]==sd for i in tables["information_sets"].values()),"INFORMATION_PARTITION_REQUIRED")
        if row["states"]:checked(path+"/states","R07",k,sources,ob.boundaries,b,row["assertions"],row["states"])
        prs={x["id"]:x for x in p["counterfactual_pairs"]};cs=md.index(row["comparisons"]);need(set(cs)==set(prs),"COUNTERFACTUAL_COVERAGE")
        for pair,cr in cs.items():
            fields(cr,("id","policy","source_ref"),"COMPARISON_BINDING_FIELDS")
            cp=tables["comparisons"].get(cr["policy"]);need(cp is not None and cp["id"] not in comparison_policies and cr["source_ref"] in source and cr["source_ref"] in cp["authority_refs"],"COUNTERFACTUAL_POLICY")
            comparison_policies.add(cp["id"]);rel=tables["relations"][cp["relation"]];pr=prs[pair]
            need(pr["reference"] in bi["observables"] and pr["alternative"] in bi["observables"],"COUNTERFACTUAL_OBSERVABLE")
            need(tables["observables"][bi["observables"][pr["reference"]]]["subject"]==rel["to"] and tables["observables"][bi["observables"][pr["alternative"]]]["subject"]==rel["from"],"COUNTERFACTUAL_RELATION")
        reqs=md.index(row["verification"]);expected={a["id"] for a in row["assertions"] if a["modality"]!="MAY"}|set(slot["outputs"])|{p["id"] for p in row["policies"]+row["states"]}
        need(len(reqs)==len(expected) and {r["subject"] for r in reqs.values()}==expected,"VERIFICATION_COVERAGE")
        for r in reqs.values():
            fields(r,("id","subject","kind","oracle_ref","status"),"VERIFICATION_FIELDS")
            need(r["status"]=="NOT_EXECUTED" and r["oracle_ref"] in source and r["kind"] in ("FINITE_OBSERVATION","BEHAVIORAL","FORMAL_PROOF","TOOL_CONFORMANCE"),"VERIFICATION_COVERAGE_OR_PROMOTION")
        need(row["ledger"] is not None or not any(tables["outputs"][out]["contribution_policy"]=="REQUIRED" for out in bi["producers"]),"LEDGER_REQUIRED")
        checked(path+"/ledger","R12",k,sources,ledger_static,row["ledger"],b,bi)
        for z in b.leaf["context"]["conversions"].values():
            need(sum(x["immutable_ref"]==z["source_ref"] and x["sha256"]==z["source_sha256"] and x["revision"]==z["version"] for x in source.values())==1,"CONVERSION_SOURCE_BINDING")
        prepared[k]=(row,b,bi)
    need(set(producers)==set(tables["outputs"]) and ext==set(tables["inputs"]) and obs==set(tables["observables"]) and relations==set(tables["relation_domains"]) and comparison_policies==set(tables["comparisons"]),"FRAME_BINDING_COVERAGE")
    proc={r["slot"]:r for r in tables["processes"].values()};deps={}
    for k,(row,b,bi) in prepared.items():
        d={producers[ref][0] for ref in bi["upstream"].values()}
        need(k not in d and set(proc[k]["depends_on"])=={proc[x]["id"] for x in d},"PROCESS_DEPENDENCY_BINDING");deps[k]=d
    order=[];pending=set(slots)
    while pending:
        ready=sorted(k for k in pending if deps[k]<=set(order));need(bool(ready),"METHOD_DEPENDENCY_CYCLE");order+=ready;pending-=set(ready)
    data,comps=checked("/requirements","R00",None,(),requirement_design,definition["requirements"],tables,source,prepared)
    semantic_slots={}
    for k,(row,b,bi) in prepared.items():
        ld=deepcopy(row["ledger"])
        if ld is not None:
            ld["coverage"]=sorted(ld["coverage"]);ld["global_disjoint"]=sorted(ld["global_disjoint"])
        semantic_slots[k]={"math":identity.mathematics(row["package"]),"method":identity.method_identity(row["profile"],row["package"]),
                           "source_ref":row["source_ref"],"bindings":row["bindings"],"assertions":[identity.assertion(a) for a in identity.byid(row["assertions"])],
                           **{name:identity.byid(row[name]) for name in ("policies","states","comparisons","verification")},"ledger":ld}
    req=deepcopy(definition["requirements"])
    for f in ("data_contracts","models","comparisons","time_policies"):req[f]=identity.byid(req[f])
    for f in ("included","environment","space_domains","functional_scopes","authority_refs"):req["boundary"][f]=sorted(req["boundary"][f])
    for k in ("data_contracts","models","comparisons","time_policies"):
        for r in req[k]:
            for f in ("quality_assertions","observables","variations","models","metric_outputs","decision_assertions","sensitivity_domains","authority_refs","rule_outputs"):
                if f in r:r[f]=sorted(r[f])
            if "tolerances" in r:r["tolerances"]=sorted(r["tolerances"],key=digest)
    semantic=digest({"schema":DEF,"study":s,"frame":identity.frame(definition["frame"]),"slots":semantic_slots,"requirements":req})
    return {"schema":DEF,"semantic_identity":semantic,"source_identity":expected_definition,"method_identities":{k:identity.method_identity(r["profile"],r["package"]) for k,(r,_,_) in prepared.items()},"execution_order":order,
            "status":"STATIC_VALID","data_status":"NOT_EXECUTED","owner":"OWNER_TBD","conformance":"NOT_PROVED"}

def admit(definition,expected_definition):
    return checked("","R00",None,(),_admit,definition,expected_definition)

def _instantiate(definition,definition_pin,instance,instance_pin):
    static=admit(definition,definition_pin)
    fields(instance,("schema","definition_ref","slots","events","disclosures","context_data","reports","data_receipts"),"INSTANCE_FIELDS")
    need(instance["schema"]==INST and digest(instance)==instance_pin and instance["definition_ref"]==static["semantic_identity"],"INSTANCE_PIN")
    rows=md.index(instance["slots"]);defs=md.index(definition["slots"]);need(set(rows)==set(defs),"INSTANCE_SLOT_COVERAGE")
    missing=[]
    for k,r in rows.items():
        fields(r,INSTANCE_FIELDS,"SLOT_INSTANCE_FIELDS")
        d=defs[k];need(r["profile_ref"]==static["method_identities"][k] and r["package_ref"]==identity.mathematics(d["package"]),"INSTANCE_METHOD_VERSION")
        if r["data_status"]=="MISSING_DATA":
            need(r["data"] is None and r["snapshot_digest"] is None and not r["witnesses"] and not r["contributions"] and not r["expected_events"],"MISSING_DATA_STATUS");missing.append(k)
        else:need(r["data_status"]=="PRESENT" and type(r["data"]) is dict and r["snapshot_digest"]==digest(r["data"]),"DATA_SNAPSHOT_PIN")
    if missing:
        return {"definition":static,"instance_identity":instance_pin,"status":"BLOCKED","reasons":[{"slot":k,"reason":"MISSING_DATA"} for k in sorted(missing)],"owner":"OWNER_TBD","conformance":"NOT_PROVED"}
    obj={"schema":graph.INPUT,"study":{**definition["study"],"frame_ref":"","slot_refs":{}},"frame":definition["frame"],"slots":[],
         "sources":definition["sources"],"events":instance["events"],"disclosures":instance["disclosures"],"context_data":instance["context_data"],"reports":instance["reports"],"trust":{}}
    for k,r in rows.items():
        d=defs[k];p=d["profile"];rr=resolve_method(d["package"],r["data"]);ctx=r["case_context"]
        st={"id":definition["study"]["id"],"version":definition["study"]["version"],"owner":"OWNER_TBD","profile_identity":digest(p),"native_study_identity":rr["study_identity"],"data_context_identity":rr["context_receipt"]["context_identity"],"case_context_identity":digest(ctx)}
        ld=deepcopy(d["ledger"])
        if ld is not None:
            need(set(r["expected_events"])==set(ld.pop("coverage")),"LEDGER_EXPECTED_SCOPE");ld["expected"]=r["expected_events"];ld["contributions"]=r["contributions"]
        else:need(not r["expected_events"] and not r["contributions"],"UNDECLARED_LEDGER")
        obj["slots"].append({**d,"study":st,"data":r["data"],"case_context":ctx,"witnesses":r["witnesses"],"ledger":ld})
    # This inner pin is derived ONLY after both separately supplied roots have
    # matched their exact objects. It adds no authority or self-certification.
    obj["trust"]=graph.pins(obj);obj["study"]["frame_ref"]=obj["trust"]["frame"];obj["study"]["slot_refs"]=obj["trust"]["slots"]
    result=checked("/slots","R00",None,(),graph.evaluate,obj,digest(obj["trust"]))
    contracts=md.index(definition["requirements"]["data_contracts"]);receipts=md.index(instance["data_receipts"])
    need(set(receipts)==set(contracts)==set(result["data_bindings"]),"DATA_PROVENANCE_COVERAGE")
    tabs=md.validate(definition["frame"]);ext={**tabs["inputs"],**tabs["observables"],**tabs["context_fields"]}
    assertions={a["id"]:a for slot in result["slots"].values() for a in slot["obligations"]["assertions"]}
    qualities={}
    for k,r in receipts.items():
        fields(r,("id","snapshot_identity","source_ref","license_ref","access_ref","raw_rows"),"DATA_RECEIPT_FIELDS")
        c=contracts[k];need(r["snapshot_identity"]==result["data_bindings"][k] and all(r[f]==c[f] for f in ("source_ref","license_ref","access_ref")),"DATA_PROVENANCE_PIN")
        if c["conversion"] is None:need(r["raw_rows"] is None,"UNDECLARED_CONVERSION")
        else:
            cv=c["conversion"]
            if cv["kind"]=="SIGN_CONVENTION":
                need(digest(sorted(r["raw_rows"],key=lambda z:z["key"]))==result["data_bindings"][cv["source_observable"]],"SIGN_CONVERSION_RAW_SOURCE_DRIFT")
            need(digest(converted_rows(r["raw_rows"],cv,ext[k]["quantity"]))==r["snapshot_identity"],"CONVERTED_DATA_BINDING")
        qs=[assertions[a]["truth"] for a in c["quality_assertions"]]
        qualities[k]="FINITE_REJECTED" if "FALSE" in qs else "BLOCKED" if any(q!="TRUE" for q in qs) else "FINITE_CHECKED"
    # Design may request stronger evidence than this consumer can supply.
    comps=[]
    for c in definition["requirements"]["comparisons"]:
        status="FINITE_OBSERVATIONS_ONLY" if c["equivalence_target"]=="E3" and all(assertions[a]["truth"]=="TRUE" for a in c["decision_assertions"]) else "NOT_PROVED"
        comps.append({"id":c["id"],"requested":c["equivalence_target"],"status":status,"independence":"UNVERIFIED","owner":"OWNER_TBD"})
    return {"definition":static,"instance_identity":instance_pin,"status":"FINITE_COUNTEREXAMPLE" if result["finite_status"]=="FINITE_COUNTEREXAMPLE" or any(v=="FINITE_REJECTED" for v in qualities.values()) else "BLOCKED" if any(v=="BLOCKED" for v in qualities.values()) else result["finite_status"],
            "graph":result,"data_quality":qualities,"comparison_evidence":comps,"owner":"OWNER_TBD","conformance":"NOT_PROVED"}
def instantiate(definition,definition_pin,instance,instance_pin):
    return checked("","R00",None,(),_instantiate,definition,definition_pin,instance,instance_pin)

def export(definition,definition_pin,instance=None,instance_pin=None):
    if instance is None:
        need(instance_pin is None,"INSTANCE_PIN");r=admit(definition,definition_pin)
    else:r=instantiate(definition,definition_pin,instance,instance_pin)
    return canon({"schema":PACKAGE,"definition":definition,"instance":instance,"receipt":r})
def reimport(text,definition_pin,instance_pin=None):
    x=c1.parse(text);fields(x,("schema","definition","instance","receipt"),"CANONICAL_FIELDS")
    need(x["schema"]==PACKAGE and export(x["definition"],definition_pin,x["instance"],instance_pin)==text,"CANONICAL_TAMPER_OR_NONCANONICAL")
    return x
