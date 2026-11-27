"""Join frozen original IDs to actual derived diagnostic paths; no C3 execution."""
from pathlib import Path
import json,sys,hashlib
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/".git").exists())
def read(p):return json.loads(Path(p).read_text())
def blob(p):
    b=Path(p).read_bytes();return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
def ptr(parts):return "".join("/"+str(x).replace("~","~0").replace("/","~1") for x in parts)
m=read(HERE/"original_diagnostic_contracts.json")
corpus=HERE.parents[1]/"BUNDLE_ML_04A_MS1_C1"/"WS_B_original_reference_corpus"
orig=read(corpus/"frozen_original_test_manifest.json")
assert blob(corpus/"frozen_original_test_manifest.json")==m["manifest_blob"]
assert blob(REPO/m["rule_source"]["path"])==m["rule_source"]["blob"]
assert len(orig["originals"])==len(m["originals"])==58
assert len(orig["paths"])==116
for row,o in zip(m["originals"],orig["originals"],strict=True):
    assert all(row[k]==v for k,v in o.items())
    assert blob(REPO/row["catalogue"]["path"])==row["catalogue"]["blob"]
    assert row["rule_id"] in {"R"+str(i).zfill(2) for i in range(14)}
    assert row["candidate_path"] is None and row["original_full_paths"]=="NOT_EXECUTED"
oracle=read(sys.argv[1]);assert oracle["full_paths_executed"]==0
actual={r["id"]:r for r in oracle["derived_independent_oracles"]}
records=[]
for row in m["originals"]:
    if row["family"]!="C23":continue
    dm=row["derived_mutation"];p=REPO/dm["path"];assert blob(p)==dm["blob"]
    d=read(p);r=actual[row["id"]]
    assert d["original"]["id"]==row["id"] and d["original_expected"]==row["expected"]
    assert r["actual"]==d["derived_diagnostic"]==r["expected"] and r["status"]=="PASS"
    records.append({"id":row["id"],"original_expected":row["expected"],"actual_code":r["actual"],"rule_id":row["rule_id"],"rule_source":m["rule_source"],"path_kind":"DERIVED_EDIT_PATH","paths":[ptr(e["path"]) for e in d["edits"]],"source":dm,"candidate_path":None,"full_path":"NOT_EXECUTED"})
assert len(records)==18 and all(r["paths"] for r in records)
print("C2_FINAL_C23_DIAGNOSTICS="+json.dumps(records,sort_keys=True))
print("C2_FINAL_DIAGNOSTIC_CATALOGUE="+json.dumps({"originals":58,"c23_derived":18,"p5_expected":30,"original_full_paths":116,"full_executed":0}))
