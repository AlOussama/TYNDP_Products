"""Compare actual C4 native output to frozen C3 native receipt; no new expected verdict."""
import json,sys
from pathlib import Path
C3=Path(__file__).resolve().parents[1]/"BUNDLE_ML_04A_MS1_C3"
old=json.loads((C3/"actual_original_results_46086101815.json").read_text())
new=json.loads(Path(sys.argv[1]).read_text())
a={(x["id"],x["syntax"]):x for x in old["rows"]};b={(x["id"],x["syntax"]):x for x in new["rows"]}
assert len(a)==len(b)==116 and a.keys()==b.keys()
fields=("status","candidate_status","source_blob","source_sha256","authored_structural_identity","representation_audit_identity","owner","conformance","result","diagnostics","assessment")
diff=[]
for key in a:
    for f in fields:
        if a[key].get(f)!=b[key].get(f):diff.append([key,f])
assert len(new["pairs"])==58 and all(x["accounted_for"] and x["canonical_pair"] for x in new["pairs"])
assert new["counts"]==old["summary"]
for x,y in zip(old["p5_controls"],new["p5_baseline_controls"],strict=True):
    for f in ("status","candidate_status","source_blob","source_sha256","result","control_passed","diagnostics"):
        if x.get(f)!=y.get(f):diff.append([["P5-BASE",x["syntax"]],f])
print("C4_BEFORE_AFTER="+json.dumps({"rows_compared":116,"pairs":58,"p5_controls":2,"diff":diff,"counts":new["counts"]}))
assert not diff,diff
