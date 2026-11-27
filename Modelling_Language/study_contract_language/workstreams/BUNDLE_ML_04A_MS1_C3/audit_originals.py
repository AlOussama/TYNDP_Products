"""Fail-closed population and traceability verification. Never promotes controls."""
import csv,json,sys,subprocess
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
C1=ROOT/"BUNDLE_ML_04A_MS1_C1"/"WS_B_original_reference_corpus"
C2=ROOT/"BUNDLE_ML_04A_MS1_C2"/"closure_v1"

def read(p):return json.loads(p.read_text())
def blob(p):return subprocess.check_output(["git","hash-object",str(p)],text=True).strip()

def main():
    mpath=C1/"frozen_original_test_manifest.json";dpath=C2/"original_diagnostic_contracts.json"
    assert blob(mpath)=="ca75ee61c1fe1cdab15bb2287e04a41cf34430d9"
    m=read(mpath);d=read(dpath);c=read(HERE/"original_path_coverage.json")
    assert c["manifest_blob"]==blob(mpath) and c["diagnostic_contract_blob"]==blob(dpath)
    assert len(m["originals"])==58 and len(m["paths"])==116
    assert len({x["id"] for x in m["originals"]})==58
    a={(x["id"],x["syntax"]):x for x in m["paths"]}
    r={(x["id"],x["syntax"]):x for x in c["records"]}
    assert len(a)==len(r)==len(c["records"])==116 and set(a)==set(r)
    assert all(v==2 for v in Counter(x["id"] for x in c["records"]).values())
    assert set(k[1] for k in r)=={"A","B"}
    dm={x["id"]:x for x in d["originals"]}
    for k,row in r.items():
        assert all(row[field]==value for field,value in a[k].items()),k
        assert row["oracle_contract"]==dm[k[0]],k
        assert row["c3_representation_status"]=="NOT_MATERIALIZED_FULL",k
        assert row["c3_execution_status"]=="NOT_EXECUTED" and row["candidate_result"] is None,k
    assert c["full_materialized"]==c["full_executed"]==0
    with (C2/"requirement_traceability.csv").open(newline="") as f:old=list(csv.DictReader(f))
    with (HERE/"requirement_coverage.csv").open(newline="") as f:new=list(csv.DictReader(f))
    assert len(old)==len(new)==125 and len({x["identity"] for x in new})==125
    for a,b in zip(old,new,strict=True):
        assert all(b[k]==v for k,v in a.items())
        assert b["C3_full_original_evidence"]=="NOT_EXECUTED"
    print("C3_POPULATION_AUDIT="+json.dumps({"identities":58,"paths":116,"materialized_full":0,
          "executed_full":0,"requirements":125,"scope":"POPULATION_INTEGRITY_ONLY","status":"PASS"},sort_keys=True))
    # Historic partial receipt is unchanged; committed source population
    # is verified separately. Full execution is decided by run_originals.py.
    actual={(r["id"],s) for r in m["originals"] for s in ("A","B")
            if (HERE/"originals"/s/(r["id"]+(".scn" if s=="A" else ".json"))).is_file()}
    print("C3_COMMITTED_SOURCE_POPULATION="+json.dumps({"source_files":len(actual),"target":116}))
    if "--require-sources" in sys.argv:
        assert actual==set(a),"C3_COMMITTED_SOURCE_COVERAGE"

if __name__=="__main__":main()
