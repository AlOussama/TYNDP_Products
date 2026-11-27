"""Check frozen population IDs and closure test manifest. No new oracle or reclassification."""
import csv,json,re
from pathlib import Path
p=Path(__file__).resolve().parent
def read(name):return list(csv.DictReader((p/name).open()))
a=read("../requirement_coverage_matrix.csv");b=read("requirement_traceability.csv")
assert len(a)==len(b)==125 and len({r["identity"] for r in b})==125
for x,y in zip(a,b,strict=True):
    assert all(y[k]==v for k,v in x.items())
    assert y["closure_general_conformance"]=="NOT_PROVED"
assert sum(r["population"]=="original_105" for r in b)==105
assert sum(r["population"]=="MS-K" for r in b)==20
m=json.loads((p/"native_test_manifest.json").read_text())
actual=set(re.findall(r"def test_(CL\d+)_",(p/"test_closure_v1.py").read_text()))
assert len(actual)==m["test_count"] and actual=={r["id"] for r in m["controls"]}
print("C2_CLOSURE_POPULATION="+json.dumps({"traceability":105,"MS-K":20,"targeted_tests":len(actual),"full_original_paths_executed":0}))
