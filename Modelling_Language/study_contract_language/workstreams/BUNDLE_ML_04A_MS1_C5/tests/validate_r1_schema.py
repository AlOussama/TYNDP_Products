"""Independent structural validation (not semantic admission)."""
import json
from pathlib import Path
import jsonschema
from importlib.metadata import version
here=Path(__file__).resolve().parents[1]
s=json.loads((here/"specification"/"final_schema.json").read_text())
jsonschema.Draft202012Validator.check_schema(s)
v=jsonschema.Draft202012Validator(s)
for n in ("schema-valid-r1.json","schema-valid-c5.json","schema-invalid-r1.json"):
    x=json.loads((here/"generated"/n).read_text())
    valid=v.is_valid(x);expected=not n.startswith("schema-invalid")
    if valid!=expected:raise SystemExit(n+" schema verdict differs: "+str(list(v.iter_errors(x))[:1]))
    print("R1_SCHEMA="+json.dumps({"file":n,"valid":valid,"expected":expected,"jsonschema":version("jsonschema")}))
