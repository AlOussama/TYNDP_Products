"""Configured structural and relational contract obligations.
This layer handles records, IDs, governance and source support; all numerical
predicates and calculations are delegated to native mathspec below.
No candidate verdict is read from the frozen independent oracle.
"""
import json
from itertools import product
from fractions import Fraction
from closure import digest,Reject
from closure_v1.diagnostics import RULE_SOURCE,pointer
from test_closure import fixture,q,dataset,scalar
from package_interface import export_package
from closure import admit
from interface import finite_consumer,import_package

MISSING=object()
def at(record,path,default=MISSING):
    x=record
    for part in path:
        try:x=x[part]
        except (KeyError,IndexError,TypeError):
            if default is not MISSING:return default
            raise
    return x
def present(x):return x is not MISSING and x is not None and x!="" and x!=[]
def freeze(x):return digest(x)
def get(record,path):return at(record,path,None)

class CandidateReject(Reject):
    def __init__(self,code,path,rule,reason,stage="STRUCTURAL_ADMISSION",native_code=None):
        self.record={"schema":"c3-actual-diagnostic-0.1","status":"REJECTED","code":code,
                     "candidate_path":pointer(*path),"path_kind":"DECODED_CANDIDATE_OBJECT",
                     "rule_id":rule,"rule_source":RULE_SOURCE,"reason":reason,
                     "stage":stage,"native_code":native_code,"owner":"OWNER_TBD","conformance":"NOT_PROVED"}
        super().__init__(code+": "+self.record["candidate_path"]+" — "+reason)

def reject(rule,path,reason,stage="STRUCTURAL_ADMISSION",native_code=None):
    raise CandidateReject(rule["code"],["instance","record",*path],rule["rule"],reason,stage,native_code)

def structural(record,rules):
    checked=[]
    for rule in rules:
        kind=rule["kind"];path=rule.get("path",rule.get("table",[]));x=get(record,path)
        def need(ok,p=path,reason="Declared structural obligation violated"):
            if not ok:reject(rule,p,reason)
        if kind=="equals":
            try:actual=at(record,path);exists=True
            except (KeyError,IndexError,TypeError):actual=None;exists=False
            need(exists and actual==rule["equals"],reason="Actual field absent or differs from declared contract value")
        elif kind=="equals_ref":
            need(x==get(record,rule["other"]),reason="Declared context reference differs")
        elif kind=="present":need(present(x),reason="Required explicit field absent or null")
        elif kind=="unique":
            need(type(x) is list and len({freeze(y) for y in x})==len(x),reason="Declared identifier population not unique")
        elif kind=="exact_population":
            need(type(x) is list and x==rule["values"],reason="Declared ordered source population lost or changed")
        elif kind=="references":
            table=get(record,rule["target"]);need(type(table) is list and type(x) is list and (bool(x) or not rule["nonempty"]),reason="Required source/reference table absent")
            ids={r[rule["key"]] for r in table}
            need(all(a in ids for a in x) and len(x)==len(set(x)),reason="Unresolved or duplicate declared source reference")
        elif kind in ("table_key","exact_keys","foreign_key","row_equals","row_ref_equals","selected_row_equals","selected_row_ref_equals","row_present","join_equals","product_coverage","quantity_registry"):
            need(type(x) is list,reason="Required declared table absent")
            if kind=="table_key":
                keys=[tuple(row.get(k) for k in rule["keys"]) for row in x]
                need(all(all(present(v) for v in key) for key in keys) and len(keys)==len(set(keys)),reason="Nonunique or missing table key")
            elif kind=="exact_keys":
                need(sorted(r.get(rule["key"]) for r in x)==sorted(rule["values"]),reason="Declared finite table population differs")
            elif kind=="product_coverage":
                keys=[tuple(row.get(k) for k in rule["keys"]) for row in x]
                domains=[z["values"] if "values" in z else [row[z["key"]] for row in get(record,z["table"])] for z in rule["domains"]]
                required=set(product(*domains))
                need(set(keys)==required and len(keys)==len(required),reason="Exact declared Cartesian support not covered; missing="+repr(sorted(required-set(keys)))+"; duplicate="+str(len(keys)-len(set(keys))))
            elif kind=="foreign_key":
                ids={r[rule["target_key"]] for r in get(record,rule["target"])}
                for j,row in enumerate(x):need(row.get(rule["field"]) in ids,path+[j,rule["field"]],"Foreign key not in declared target population")
            elif kind=="join_equals":
                target={r[rule["target_key"]]:r for r in get(record,rule["target"])}
                for j,row in enumerate(x):
                    need(row.get(rule["key"]) in target,path+[j,rule["key"]],"Joined reference missing")
                    for field in rule["fields"]:need(row.get(field)==target[row[rule["key"]]].get(field),path+[j,field],"Actual joined context differs")
            elif kind=="quantity_registry":
                for j,row in enumerate(x):
                    allowed=rule["admitted"].get(row.get(rule["carrier"]))
                    need(allowed is not None and row.get(rule["kind_field"])==allowed["kind"] and row.get(rule["unit"]) in allowed["units"],path+[j],"Carrier, physical kind and unit signature incompatible")
            else:
                for j,row in enumerate(x):
                    if kind.startswith("selected") and any(row.get(k)!=v for k,v in rule["selector"].items()):continue
                    if kind=="row_present":
                        for field in rule["fields"]:need(present(row.get(field)),path+[j,field],"Required row field missing")
                    else:
                        value=rule["equals"] if "equals" in rule else get(record,rule["other"])
                        field=rule["field"]
                        need(field in row and row[field]==value,path+[j,field],"Actual row violates declared field contract")
        else:raise RuntimeError("Unknown configured structural operation "+kind)
        checked.append({"code":rule["code"],"rule_id":rule["rule"],"path":pointer("instance","record",*path),"status":"SATISFIED"})
    return checked

def native_checks(record,checks):
    results=[]
    for index,spec in enumerate(checks):
        kind=spec["kind"];path=spec.get("table",spec.get("path"))
        values=get(record,path)
        domains={};params={};data={};quant={};axes={}
        if kind=="native_record_equality":
            labels=list(values);axis=spec["axis"];domains[axis]=labels
            params={"decision":{"dims":[axis]},"common":{"dims":[]}}
            data={"decision":[{"key":[label],"value":values[label]} for label in labels],"common":scalar(values[labels[0]])}
            rules=[spec["condition"]];expr={}
        else:
            axis=spec.get("axis");labels=[row[spec["key"]] for row in values] if kind=="native_table" else []
            if axis:domains[axis]=labels
            rules=spec["conditions"];expr=spec["expressions"]
            for n,p in spec["parameters"].items():
                if "quantity" in p:quant[n]=p["quantity"]
                if "constant" in p:
                    params[n]={"dims":[],"dtype":p["dtype"]};data[n]=scalar(p["constant"]);continue
                dims=[axis] if axis else []
                params[n]={"dims":dims,"dtype":p["dtype"]}
                field=p["field"]
                rows=[{"key":[label],"value":r.get(field)} for label,r in zip(labels,values,strict=True)] if axis else scalar(values.get(field))
                for j,row in enumerate(rows):
                    if row["value"] is None or type(row["value"]) is bool:
                        # Missing required numeric field is a static typed data admission
                        # failure; no coercion to zero. Actual source path retained.
                        relevant=next((z for z in rules if z.get("field")==field),rules[0])
                        reject(relevant,path+([j,field] if axis else [field]),"Required exact numeric value is missing or not numeric","NATIVE_DATA_ADMISSION","MISSING_NUMERIC")
                data[n]=rows
        doc={"version":0,"dimensions":{n:{"dtype":"int" if type(v[0]) is int else "str"} for n,v in domains.items()},
             "parameters":params,"expressions":expr,"conditions":{z["name"]:z["formula"] for z in rules}}
        ctx=fixture(doc,quant=quant,domains=domains,roles={n:"INPUT" for n in params},pred_axes={z["name"]:z["axes"] for z in rules})
        package=export_package(admit(json.dumps(doc,sort_keys=True),ctx))
        imported=import_package(package)
        if export_package(imported)!=package:raise RuntimeError("Native constraint roundtrip drift")
        try:consumer=finite_consumer(package,dataset(data))
        except Reject as e:
            # Unknown or unexpected native admission failure is not mapped to
            # an expected negative. Keep its actual code and block completion.
            raise RuntimeError("Unexpected native record check binding: "+str(e)) from e
        actual=consumer.conditions()
        for rule in rules:
            name=rule["name"]
            if not actual[name]:
                predicate=consumer.program.conditions[name]
                bad=[]
                for key in product(*(consumer.axes[a] for a in predicate.dims)):
                    env=dict(zip(predicate.dims,key,strict=True))
                    if not consumer.cond(predicate.condition.root,env):bad.append(env)
                target=path
                if bad and predicate.dims:
                    if kind=="native_record_equality":target=path+[bad[0][spec["axis"]]]
                    elif kind=="native_table":
                        label=bad[0][spec["axis"]];j=labels.index(label)
                        target=path+[j,rule["field"]]
                elif kind=="native_scalar" and "field" in rule:target=path+[rule["field"]]
                reject(rule,target,"Native Program predicate "+name+" is false; violating coordinates="+repr(bad),"NATIVE_PREDICATE_EVALUATION","FINITE_COUNTEREXAMPLE")
        results.append({"path":pointer("definition","method_profile","native_checks",index),
                        "native_identity":imported["native_identity"],"package_identity":digest(package),
                        "data_identity":consumer.receipt["data_identity"],"conditions":actual,"outputs":consumer.outputs(),"roundtrip":True})
    return results
