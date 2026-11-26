"""Preserve the complete original denominator; independent oracles and M0 partial probes separate."""
from pathlib import Path
import argparse,copy,csv,hashlib,json,sys,platform
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"independent_oracles"))
from oracles import run,Reject
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
    b=p.read_bytes();return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
def verify():
    m=read(ROOT/"frozen_original_test_manifest.json")
    for name,pin in m["catalog_blobs"].items():
        assert blob(ROOT/"frozen"/name)==pin,name
    assert len(m["originals"])==58 and len({r["id"] for r in m["originals"]})==58
    assert len(m["paths"])==116 and len({(r["id"],r["syntax"]) for r in m["paths"]})==116
    with (ROOT/"frozen/traceability.csv").open() as p:assert len(list(csv.DictReader(p)))==105
    return m
def case(id):return ROOT/"reference_cases"/id/"contract.json"
def reference_oracles():
    results=[]
    for i in range(1,11):
        id=f"RC{i:02}";p=case(id);doc=read(p)
        try:
            actual=run(doc);ok=actual==doc["synthetic_data"]["expected"]
        except Exception as e:actual=repr(e);ok=False
        results.append({"id":id,"family":"RC","fixture_sha256":sha(p),"stage":"DERIVED_FINITE_ORACLE","expected":doc["synthetic_data"]["expected"],"actual":actual,"status":"PASS" if ok else "FAIL","original_expected":doc["expected_original"],"scope":"No full contract verdict"})
    for p in sorted((ROOT/"original_c23_mutations").glob("MUT-*.json")):
        r=read(p);doc=copy.deepcopy(read(case(r["original"]["rc"])))
        for edit in r["edits"]:
            x=doc
            for k in edit["path"][:-1]:x=x[k]
            x[edit["path"][-1]]=edit["value"]
        try:actual=run(doc)
        except Reject as e:actual=str(e)
        except Exception as e:actual=repr(e)
        results.append({"id":r["original"]["id"],"family":"C23","fixture_sha256":sha(p),"stage":"DERIVED_FINITE_ORACLE","expected":r["derived_diagnostic"],"actual":actual,"status":"PASS" if actual==r["derived_diagnostic"] else "FAIL","original_expected":r["original_expected"],"scope":"Original E1/AUDIT verdict NOT evaluated"})
    return results
class ArchitectureAdapter:
    architecture=None
    def evaluate_full(self,path):
        raise NotImplementedError("Full-chain adapter not implemented")
class M0(ArchitectureAdapter):
    architecture="M0"
    def partial(self):
        base=ROOT.parents[1]/"BUNDLE_ML_04A_R1"
        sys.path.insert(0,str(base))
        import n1r
        records=[]
        for s,file in [("A","syntax_A/RC01.partial.scn"),("B","syntax_B/RC01.partial.json")]:
            p=ROOT/file
            try:
                r=n1r.run(p.read_text(),s)
                records.append({"id":"RC01","syntax":s,"architecture":"M0","stage":"STATIC_FRAGMENT_ONLY","fixture_sha256":sha(p),"expected":"BLOCKED_OWNER_TBD","actual":r["status"],"blocked":r.get("blocked",[]),"semantic_digest":r.get("semantic_digest"),"audit_digest":r.get("audit_digest"),"status":"EXECUTED_PARTIAL"})
            except Exception as e:records.append({"id":"RC01","syntax":s,"architecture":"M0","stage":"STATIC_FRAGMENT_ONLY","fixture_sha256":sha(p),"expected":"BLOCKED_OWNER_TBD","actual":repr(e),"status":"FAIL"})
        return records
def main():
    p=argparse.ArgumentParser();p.add_argument("--m0",action="store_true");p.add_argument("--output",required=True);args=p.parse_args()
    manifest=verify();oracles=reference_oracles()
    partial=M0().partial() if args.m0 else []
    rows=[]
    for r in manifest["paths"]:
        path=dict(r,architecture="M0",stage="FULL_CONTRACT",actual="NOT_EXECUTED",verdict="BLOCKED",evidence_id=None)
        rows.append(path)
    result={"schema":"c1-runner-receipt-0.1","python":platform.python_version(),"original_identities":58,"traceability":105,"original_full_paths":116,"full_paths_executed":0,"full_paths_passed":0,"original_paths":rows,"derived_independent_oracles":oracles,"partial_m0":partial,"scope":"Original full-chain execution blocked; derived checks never promoted."}
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print("C1_CORPUS_ORACLES="+json.dumps(oracles))
    print("C1_M0_PARTIAL="+json.dumps(partial))
    print("C1_ORIGINAL_PATHS=0/116")
    if any(r["status"]!="PASS" for r in oracles):raise SystemExit(1)
    if args.m0 and (len(partial)!=2 or any(r["status"]!="EXECUTED_PARTIAL" or r["actual"]!="BLOCKED" for r in partial) or partial[0].get("semantic_digest")!=partial[1].get("semantic_digest") or partial[0].get("audit_digest")!=partial[1].get("audit_digest")):raise SystemExit(2)
if __name__=="__main__":main()
