"""Frozen RC source-coordinate adapter; not part of generic M3 semantics."""
import json
from hashlib import sha1
from fractions import Fraction
from closure import need
from record_contract import at

def values_norm(v):
    if type(v) is list:return [values_norm(x) for x in v]
    if v is None or type(v) is bool:return v
    try:return str(Fraction(v))
    except (ValueError,TypeError,ZeroDivisionError):return v

def source_binding(d,i,raw_original):
    blob=sha1((f"blob {len(raw_original)}\0").encode()+raw_original).hexdigest()
    need(blob==d["original_source"]["blob"],"ORIGINAL_SOURCE_BLOB")
    need(json.loads(raw_original)["id"]==d["reference"]==i["record"]["id"],"ORIGINAL_REFERENCE_BINDING")
    # Independent of the oracle: declared source paths must actually bind
    # the authored data, including explicit source-specific coordinate maps.
    r=i["record"];rc=d["reference"];p=d["parameters"];actual=i["parameters"]
    if rc=="RC02":
        s=r["synthetic_data"];v=s["domains"]["vehicle"];t=s["domains"]["interval"]
        x=s["inputs"];o=s["observed"]
        raw=[o["delivered"][j][k] for k in range(len(t)) for j in range(len(v))]
        need(values_norm(i["raw_transfers"]["delivered"])==values_norm(raw),"SOURCE_DATA_BINDING:delivered")
        need(values_norm(i["raw_transfers"]["required"])==values_norm(x["required"]),"SOURCE_DATA_BINDING:required")
        need(actual["connected"]==[int(x["connected"][j][k]) for k in range(len(t)) for j in range(len(v))],"SOURCE_DATA_BINDING:connected")
        need(actual["eligible"]==[int(x["connected"][j][k] and k<x["departure"][j]) for k in range(len(t)) for j in range(len(v))],"SOURCE_DATA_BINDING:eligible")
    if rc=="RC07":
        s=r["synthetic_data"];x=s["observed"]["decision"]
        need(values_norm(actual["decision"])==values_norm([x[k][j] for j in range(len(s["domains"]["scenario"])) for k in range(len(s["domains"]["stage"]))]),"SOURCE_DATA_BINDING:decision")
    if rc=="RC05":
        s=r["synthetic_data"];bs=s["domains"]["bus"];ls=s["domains"]["branch"]
        for n,side in (("sending",0),("receiving",1)):
            need(i["relation_rows"][n]==[{"branch":b,"bus":bs[s["inputs"]["orientation"][j][side]]} for j,b in enumerate(ls)],"SOURCE_RELATION_BINDING")
    for n,z in p.items():
        path=z.get("source_path")
        if path is None or (rc=="RC02" and n in ("delivered","required","connected","eligible")) or (rc=="RC07" and n=="decision"):continue
        raw=at(r,path)
        if n in i["raw_transfers"]:
            raw_values=i["raw_transfers"][n];want=raw if type(raw) is list else [raw]
            need(values_norm(raw_values)==values_norm(want),"SOURCE_RAW_DATA_BINDING:"+n);continue
        if type(raw) is bool:raw=int(raw)
        if z["dims"] and type(raw) is not list:raw=[raw]
        need(values_norm(actual[n])==values_norm(raw),"SOURCE_DATA_BINDING:"+n)
    if d["ledgers"]:
        need(i["observed_contributions"]==[r["synthetic_data"]["observed"]["contributions"]],"SOURCE_CONTRIBUTION_BINDING")
    if d["comparison"] is not None:
        x=r["synthetic_data"]["inputs"];c=i["comparison"]
        need(c["reference_context"]==x["reference_snapshot"] and c["alternative_context"]==x["project_snapshot"] and c["project_delta"]==x["project_delta"],"SOURCE_CONTEXT_BINDING")
