"""C3 targeted P5 contribution/discount graph, extending the pinned CL24 test.
A/B forms generated as integration controls, not independently authored original
paths. No original verdict, model equivalence or CBA compliance is inferred.
"""
import json,sys,copy,math
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
C2=ROOT/"BUNDLE_ML_04A_MS1_C2"
sys.path.insert(0,str(C2/"closure_v1"));sys.path.insert(0,str(C2))
from research_assembly import (frame,source_row,sig,source_for_slot,make_slot,bundle,repin,
    to_definition,to_instance,assertion,fixture,q,dataset,pkg,digest,resolve_method,old_identities)
from research_assembly import scalar
from interface import finite_consumer
from WS_B import affine_boundary
from closure_v1 import definition
from authoring import emit_control,evaluate

def make_slot_affine(f,src,k,d,c,data,bindings,inputs,obs,outputs,external_symbols,assertions=None,comparison_pairs=None,case_context=None,weight_roles=None,ledger=None,depends=None):
    return make_slot(f,src,k,d,c,data,bindings,inputs,obs,outputs,external_symbols,assertions,comparison_pairs,case_context,weight_roles,ledger,depends,package_builder=lambda d,c: affine_boundary.export_package(affine_boundary.admit(json.dumps(d),c)))

def build(p5_override=None, authored_method=None, authored_source=None):
    # Original fixture bytes retained from its pinned Git blob. This is a
    # deliberately narrow semantic projection, not the original full A/B path.
    p5_text=(C2/"closure_v1"/"p5_fixture.json").read_text() if authored_source is None else authored_source
    p5=json.loads(p5_text) if p5_override is None else copy.deepcopy(p5_override)
    f=frame();src=[source_row("authority:source","fixture:source",p5_text)]
    labels=[r["id"] for r in p5["scenarios"]]
    f["domains"]=[{"id":"domain:s","kind":"scenario","members":labels,"ordered":False}]
    f["scopes"]=[{"id":"scope:main","domains":["domain:s"],"subjects":[]}]
    money=q("EUR","currency","EUR:real:2025")
    f["inputs"]=[sig("input:probability",q(),["domain:s"])]
    models=[];slots=[];contexts={};raw={};events=[]
    for m in p5["models"]:
        mid=m["id"];key=mid.lower();cases={case:"case:"+key+":"+case for case in ("R","P")}
        for case,k in cases.items():
            f["referents"].append({"id":k,"kind":"study_case","model_id":"model:"+key,"quantity":money,"axes":["domain:s"],"authority_refs":["authority:source"]})
            f["observables"].append(sig("observable:"+key+":"+case,money,["domain:s"],subject=k,projection="IDENTITY"))
        f["scopes"][0]["subjects"]+=list(cases.values())
        rel="relation:"+key;f["relations"].append({"id":rel,"kind":"counterfactual_of","from":cases["P"],"to":cases["R"],"authority_refs":["authority:source"]})
        fields_={}
        samples={case:[next(x for x in p5["samples"] if x["model_id"]==mid and x["scenario_id"]==s and x["case_id"]==case) for s in labels] for case in ("R","P")}
        for field in ("exogenous_digest","weather_year"):
            pair={}
            for case,side in (("R","reference"),("P","alternative")):
                name="context:"+key+":"+case+":"+field;pair[side]=name
                f["context_fields"].append({"id":name,"axes":["domain:s"],"value_type":"TOKEN","allowed_values":[],"authority_refs":["authority:source"]})
                contexts[name]=[{"key":[r["scenario_id"]],"value":r[field]} for r in samples[case]]
            fields_[field]=pair
        policy="comparison:"+key
        # Explicit project delta token is allowed to change; use a declared
        # token for absent asset rather than an invented numeric value.
        pr={}
        for case,side in (("R","reference"),("P","alternative")):
            name="context:"+key+":"+case+":project";pr[side]=name
            f["context_fields"].append({"id":name,"axes":["domain:s"],"value_type":"TOKEN","allowed_values":[],"authority_refs":["authority:source"]})
            contexts[name]=[{"key":[r["scenario_id"]],"value":r["project_delta_id"] or "NO_PROJECT_DELTA"} for r in samples[case]]
        f["comparisons"].append({"id":policy,"relation":rel,"exogenous":fields_,"project":{"project_delta":pr},"allowed_changes":["project_delta"],"authority_refs":["authority:source"]})
        out="output:"+key;f["outputs"].append(sig(out,money,contribution_policy="REQUIRED"))
        d={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{n:{"dims":["s"]} for n in ("base","alt","prob")},"expressions":{"benefit":authored_method["annual_source"] if authored_method is not None else "sum((base-alt)*prob, over=s)"}}
        c=fixture(d,roles={"prob":"INPUT"},quant={"base":money,"alt":money,"benefit":money},domains={"s":labels})
        # One stated study-year amount: actual original annual rate * 1 year.
        rows={case:[{"key":[r["scenario_id"]],"value":str(r["operating_cost_proxy_eur_per_year"])} for r in samples[case]] for case in ("R","P")}
        raw.update({"observable:"+key+":"+case:rr for case,rr in rows.items()})
        data=dataset({"base":copy.deepcopy(rows["R"]),"alt":copy.deepcopy(rows["P"]),"prob":[{"key":[r["id"]],"value":str(r["weight"])} for r in p5["scenarios"]]})
        pairid="pair:"+key
        ds={field:digest(sorted(contexts[pair["reference"]],key=lambda r:r["key"])) for field,pair in fields_.items()}
        ctx={"pairs":[{"id":pairid,"reference_exogenous":ds,"alternative_exogenous":ds}]}
        row=make_slot(f,source_for_slot(f,src,key),key,d,c,data,{"ref:base":{"kind":"OBSERVABLE","ref":"observable:"+key+":R"},"ref:alt":{"kind":"OBSERVABLE","ref":"observable:"+key+":P"},"ref:prob":{"kind":"INPUT","ref":"input:probability"},"ref:benefit":{"kind":"OUTPUT","ref":out}},["input:probability"],["observable:"+key+":R","observable:"+key+":P"],[out],["ref:benefit"],comparison_pairs=[{"id":pairid,"reference":"ref:base","alternative":"ref:alt"}],case_context=ctx,weight_roles={"ref:prob":"PROBABILITY"})
        row["profile"]["probability_rules"]={"ref:prob":"SUM_ONE"};row["comparisons"]=[{"id":pairid,"policy":policy,"source_ref":"authority:source"}]
        # Derived event catalogue: each original sample ID determines a
        # unique case/scenario contribution to the annual benefit.
        contributions=[];event_ids=[]
        for case,series_name in (("R","base"),("P","alt")):
            for r in samples[case]:
                eid="event:"+r["id"];event_ids.append(eid)
                events.append({"id":eid,"case":cases[case],"event_key":r["id"]+":operating_cost_proxy","coordinate":{"domain:s":r["scenario_id"]},"source_ref":"authority:source"})
                contributions.append({"id":"contribution:"+r["id"],"series":series_name,"key":[r["scenario_id"]],"case":cases[case],"observable":"observable:"+key+":"+case,"event":eid})
        row["ledger"]={"bindings":{"base":{"role":"contribution","observable":"observable:"+key+":R","case":cases["R"],"data_ref":""},"alt":{"role":"contribution","observable":"observable:"+key+":P","case":cases["P"],"data_ref":""},"prob":{"role":"auxiliary","observable":"","case":"","data_ref":"ref:prob"}},"key_axes":{n:["domain:s"] for n in ("base","alt","prob")},"contributions":contributions,"policy":{"benefit":"DISJOINT"},"global_disjoint":["benefit"],"expected":{"benefit":event_ids}}
        slots.append(row)
        models.append({"id":"model:"+key,"implementation_ref":m["generator_identity"],"source_ref":"authority:source","license_ref":"authority:source","access_ref":"authority:source","observables":["observable:"+key+":R","observable:"+key+":P"],"variations":[]})
    # Extend the exact original annual-amount graph with explicit native discount
    # and independent one-off capex contributions. Year is an economic sample
    # coordinate, not a physical chronology or a scenario probability.
    h=p5["economics"]["horizon_years"];years=list(range(1,h+1))
    f["domains"].append({"id":"domain:y","kind":"sample","members":years,"ordered":True})
    f["scopes"][0]["domains"].append("domain:y")
    f["inputs"] += [sig("input:discount_rate",q()),sig("input:discount_year",q(),["domain:y"],value_type="INTEGER")]
    for model,annual_row in zip(models,list(slots),strict=True):
        key=annual_row["id"].split(":",1)[1]
        mid=next(m["id"] for m in p5["models"] if m["id"].lower()==key)
        annual_id="output:"+key
        # The upstream finite value is obtained from the native candidate,
        # never from independent oracle expectations.
        annual=finite_consumer(annual_row["package"],annual_row["data"]).outputs()["benefit"][0]
        case="case:"+key+":capex";obs="observable:"+key+":capex";out="output:"+key+":npv"
        f["referents"].append({"id":case,"kind":"cost_series","quantity":money,"axes":[],"authority_refs":["authority:source"]})
        f["observables"].append(sig(obs,money,subject=case,projection="IDENTITY"))
        f["scopes"][0]["subjects"].append(case)
        model["observables"].append(obs)
        f["outputs"].append(sig(out,money,contribution_policy="REQUIRED"))
        doc={"version":0,"dimensions":{"y":{"dtype":"int","ordered":True}},
             "parameters":{"annual":{"dims":[]},"capex":{"dims":[]},"rate":{"dims":[]},"year":{"dims":["y"],"dtype":"int"}},
             "expressions":{"factor":authored_method["discount_factor_source"] if authored_method is not None else "sum((1 + rate)**(-year), over=y)",
                            "npv":authored_method["npv_source"] if authored_method is not None else "annual * factor - capex"},
             "conditions":{"valid_rate":authored_method["rate_guard"] if authored_method is not None else "rate >= 0 and rate < 1"}}
        ctx=fixture(doc,roles={"annual":"INPUT","rate":"INPUT","year":"INPUT"},
                    quant={n:money for n in ("annual","capex","npv")},
                    domains={"y":years},domain_rules={"rate":"NONNEGATIVE","year":"POSITIVE"},pred_axes={"valid_rate":[]})
        ctx["power_domains"]={"year":{"min":1,"max":h}}
        data=dataset({"annual":scalar(annual),"capex":scalar(p5["economics"]["capex_eur"]),
                      "rate":scalar(str(p5["economics"]["discount_rate"])),"year":[{"key":[y],"value":y} for y in years]})
        bind={"ref:annual":{"kind":"UPSTREAM","ref":annual_id},"ref:capex":{"kind":"OBSERVABLE","ref":obs},
              "ref:rate":{"kind":"INPUT","ref":"input:discount_rate"},"ref:year":{"kind":"INPUT","ref":"input:discount_year"},
              "ref:factor":{"kind":"INTERMEDIATE","ref":"ref:factor"},"ref:npv":{"kind":"OUTPUT","ref":out}}
        sk=key+":discount"
        row=make_slot_affine(f,source_for_slot(f,src,sk),sk,doc,ctx,data,bind,
                             [annual_id,"input:discount_rate","input:discount_year"],[obs],[out],["ref:npv"],depends=["process:"+key])
        a=assertion(row["package"],"assertion:"+key+":valid_rate","valid_rate",[],[])
        row["assertions"]=[a]
        row["verification"].append({"id":"verification:"+key+":discount:rate","subject":a["id"],"kind":"FINITE_OBSERVATION","oracle_ref":"authority:source","status":"NOT_EXECUTED"})
        eid="event:"+mid+":CAPEX_T0"
        events.append({"id":eid,"case":case,"event_key":mid+":CAPEX_T0","coordinate":{},"source_ref":"authority:source"})
        row["ledger"]={"bindings":{**{n:{"role":"auxiliary","observable":"","case":"","data_ref":"ref:"+n} for n in ("annual","rate","year")},
                                    "capex":{"role":"contribution","observable":obs,"case":case,"data_ref":""}},
                       "key_axes":{"annual":[],"capex":[],"rate":[],"year":["domain:y"]},
                       "contributions":[{"id":"contribution:"+mid+":CAPEX_T0","series":"capex","key":[],"case":case,"observable":obs,"event":eid}],
                       "policy":{"factor":"DISJOINT","npv":"DISJOINT"},"global_disjoint":["npv"],
                       "expected":{"npv":[*annual_row["ledger"]["expected"]["benefit"],eid]}}
        slots.append(row)

    for r in p5["additional_indicators"]:
        k="report:"+r["id"];qual=r["unit"]=="qualitative"
        f["report_requests"].append({"id":k,"subject":f["id"],"value_type":"QUALITATIVE" if qual else "QUANTITY","declared_unit":None if qual else r["unit"],"basis":"ORIGINAL_P5_NOT_MONETIZED","oracle_ref":"authority:source","authority_refs":["authority:source"]})
    x,_=bundle(f,slots,src,events);x["context_data"]=contexts;x["reports"]=[{"id":r["id"],"status":"NOT_EXECUTED","reason":"ORIGINAL_P5_INDICATOR_NOT_EXECUTED","value":None,"source_ref":"authority:source"} for r in f["report_requests"]];repin(x)
    d,dp=to_definition(x);d["requirements"]["models"]=models
    for r in d["requirements"]["data_contracts"]:
        if r["id"] in raw:r["conversion"]={"kind":"ANNUAL_RATE_TO_PERIOD_AMOUNT","source_unit":"EUR/year","source_basis":"EUR:real:2025","period_years":"1","period_ref":"authority:source","source_ref":"authority:source"}
    dp=digest(d);inst=to_instance(x,d,dp)
    for r in inst["data_receipts"]:
        if r["id"] in raw:r["raw_rows"]=raw[r["id"]]
    return d,dp,inst

def main(oracle_path):
    e=json.loads(Path(oracle_path).read_text())
    assert e["passed"]==e["total"]
    expected=e["baseline"]["synthetic_numeric_results"]
    d,dp,inst=build();ip=digest(inst)
    rows=[]
    for syntax in ("A","B"):
        raw=emit_control(d,inst,syntax)
        got=evaluate(raw,syntax,sha256(raw).hexdigest(),dp,ip)
        assert got["status"]=="RETURNED",got
        res=got["result"];g=res["graph"];outs=g["outputs"]
        assert res["status"]=="BLOCKED" and res["conformance"]=="NOT_PROVED"
        actual={}
        for mid in ("M-A","M-B"):
            key=mid.lower()
            annual=Fraction(outs["output:"+key][0]["value"])
            npv=Fraction(outs["output:"+key+":npv"][0]["value"])
            refs=g["slots"]["slot:"+key+":discount"]["lineage"]["npv"][0]["events"]
            assert len(refs)==5 and all(v==1 for v in refs.values()) and refs["event:"+mid+":CAPEX_T0"]==1,refs
            exp=expected[mid]
            assert math.isclose(float(annual),exp["illustrative_annual_cost_saving_eur"],rel_tol=0,abs_tol=1e-9)
            assert math.isclose(float(npv),exp["illustrative_npv_proxy_eur"],rel_tol=0,abs_tol=1e-9)
            assert (1 if npv>0 else -1 if npv<0 else 0)==exp["decision_sign"]
            actual[mid]={"annual_exact":str(annual),"npv_exact":str(npv),"contributions":refs,"oracle":exp}
        rows.append({"syntax":syntax,"source_sha256":got["source_sha256"],"semantic_identity":got["semantic_identity"],
                     "graph_semantic_identity":got["graph_semantic_identity"],"package_sha256":got["package_sha256"],
                     "representation_audit_identity":got["representation_audit_identity"],"result_status":res["status"],
                     "models":actual})
    assert rows[0]["models"]==rows[1]["models"]
    assert rows[0]["semantic_identity"]==rows[1]["semantic_identity"] and rows[0]["graph_semantic_identity"]==rows[1]["graph_semantic_identity"]
    assert rows[0]["package_sha256"]==rows[1]["package_sha256"]
    assert rows[0]["representation_audit_identity"]!=rows[1]["representation_audit_identity"]
    print("C3_P5_GRAPH_PROJECTION="+json.dumps({"scope":"EXTENDED_CL24_GRAPH_CONTROL_NOT_ORIGINAL_AB","rows":rows},sort_keys=True))

if __name__=="__main__":main(sys.argv[1])
