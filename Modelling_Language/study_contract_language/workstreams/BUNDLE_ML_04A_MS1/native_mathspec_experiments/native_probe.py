"""MS1 non-normative native public-API experiments, not a solver or full contract."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import importlib.metadata as md
import mathspec as ms
from mathspec.errors import LanguageError
import mathspec.program as mp
import json
import sys

HERE = Path(__file__).resolve().parent
PIN = "5f1464c334c1012cdee2947d4d55b4d1d6bef40a"

def h(b): return sha256(b).hexdigest()

def assert_native_identity():
    source = Path.cwd() / "src/mathspec"
    installed = Path(ms.__file__).resolve().parent
    files = sorted(source.rglob("*.py"))
    assert files
    for f in files:
        assert h(f.read_bytes()) == h((installed/f.relative_to(source)).read_bytes()), f
    print(json.dumps({"source_pin_expected": PIN, "module_count_checked": len(files),
                      "imported": str(installed), "python": sys.version,
                      "versions": {p: md.version(p) for p in ("mathspec","pydantic","pyparsing","PyYAML")}}))

def spec(dims, parameters, expressions=None, assumptions=None):
    return {"version":0, "dimensions":dims, "parameters":parameters,
            **({"expressions": expressions} if expressions else {}),
            **({"assumptions": assumptions} if assumptions else {})}

def param(*dims, dtype="float"): return {"dims": list(dims), "dtype":dtype, "missing":"refused"}
t = {"t":{"dtype":"int","ordered":True}}
cases = {
 "RC01":spec(t,{"p":param("t"),"dt":param("t"),"intake":param("t")},
  {"integral":"-p * dt"}, {"observed_intake":{"holds":"intake == integral","where":"p < 0"}}),
 "RC02":spec({"ev":{}},{"delivered":param("ev"),"required":param("ev")}, None, {"service":"delivered >= required"}),
 "RC03":spec(t,{"power":param("t"),"hydrogen":param("t"),"lhv":param(),"eta_low":param(),"eta_high":param()},
  {"output_energy":"hydrogen * lhv"}, {"low":"output_energy >= power * eta_low","high":"output_energy <= power * eta_high"}),
 "RC04":spec(t,{"stock":param("t"),"inflow":param("t"),"outflow":param("t"),"dt":param("t")},
  {"delta":"(inflow - outflow) * dt"}, {"ledger":{"holds":"stock == shift(stock, along=t, offset=1, edge=0) + delta","where":"position(t) > 0"}}),
 "RC05":spec({"branch":{}},{"f":param("branch"),"incidence":param("branch"),"x":param("branch"),"cycle":param("branch"),"injection":param()},
  {"nodal":"sum(f * incidence, over=branch)","loop_sum":"sum(f * x * cycle, over=branch)"},
  {"kcl":"nodal == injection","kvl":"loop_sum == 0"}),
 "RC06":spec({"site":{}},{"modules":param("site",dtype="int"),"max_modules":param("site",dtype="int")},None,
  {"limit":"modules >= 0 AND modules <= max_modules"}),
 "RC07":spec({"pair":{}},{"a":param("pair"),"b":param("pair"),"same_info":param("pair",dtype="bool")},None,
  {"paired_decision":{"holds":"a == b","where":"same_info"}}),
 "RC08":spec(t,{"cost":param("t"),"dt":param("t"),"weight":param("t"),"reported":param()},
  {"weighted":"sum(cost * dt * weight, over=t)"},{"reported_total":"reported == weighted"}),
 "RC09":spec({"period":{}},{"project":param("period"),"baseline":param("period"),"discount":param("period"),"reported":param()},
  {"difference":"sum((baseline - project) * discount, over=period)"},{"result":"reported == difference"})
}
# These encode observed data checks, NOT assumptions about permissible study inputs.
# RC10 has no mathematical leaf sufficient for its evidence lifecycle; not represented here.
def accepted(doc):
    obj=ms.to_spec(doc)
    canonical=obj.to_yaml(canonical=True)
    again=ms.to_spec(canonical)
    assert again.to_yaml(canonical=True)==canonical, "canonical idempotence"
    assert list(obj.program.parameters)==list(again.program.parameters)
    # Original typed nodes can differ in ordering; do not assert general semantic equivalence.
    return obj,canonical

def expect_refused(doc):
    try:
        ms.to_spec(doc)
    except LanguageError as exc:
        return str(exc)
    raise AssertionError("native API unexpectedly accepted probe")

def run():
    assert_native_identity()
    outcomes=[]
    for name,doc in cases.items():
        try:
            obj,y=accepted(doc)
            outcomes.append({"id":name,"stage":"NATIVE_STATIC_FRAGMENT_ONLY","hash":h(y.encode()),
                             "expressions":list(obj.program.expressions),"assumptions":list(obj.program.assumptions)})
        except Exception as exc:
            outcomes.append({"id":name,"stage":"NATIVE_PROBE_FAILED","error":repr(exc)})
    checks={}
    # Canonical equal for commutative exact-scalar arithmetic in a declared safe subset.
    a=spec({},{"a":param(),"b":param(),"c":param()},{"value":"a + b"})
    b=deepcopy(a); b["expressions"]["value"]="b + a"
    checks["commutative"] = accepted(a)[1] == accepted(b)[1]
    a["expressions"]["value"]="a - b"; b["expressions"]["value"]="b - a"
    checks["ordered_subtraction"] = accepted(a)[1] != accepted(b)[1]
    a["expressions"]["value"]="a / b"; b["expressions"]["value"]="b / a"
    checks["ordered_division"] = accepted(a)[1] != accepted(b)[1]
    a["expressions"]["value"]="unregistered(a)"
    checks["unknown_operator"] = expect_refused(a)
    a["expressions"]["value"]="undeclared + b"
    checks["unknown_name"] = expect_refused(a)
    a["expressions"]["value"]="a + b"
    a["arbitrary_ast"]={"python":"never"}
    checks["unknown_section"] = expect_refused(a)
    # Counterexample: dimensions are index axes, not units. The native input has no carrier/basis.
    bad=spec(t,{"mw":param("t"),"kg_per_h":param("t")},{"nonsense":"mw + kg_per_h"})
    accepted(bad)
    checks["physical_type_gap"]="NATIVE_ACCEPTS_NUMERIC_SAME_AXIS_REQUIRES_CONTRACT_TYPE_CHECK"
    # No native claim that a data predicate verifies all models or any attached observations.
    checks["data_evaluation"]="NOT_EXECUTED_BY_MATHSPEC"
    print(json.dumps({"cases":outcomes,"checks":checks},indent=2))
    assert all(x["stage"]=="NATIVE_STATIC_FRAGMENT_ONLY" for x in outcomes), outcomes
    assert checks["commutative"] and checks["ordered_subtraction"] and checks["ordered_division"]

if __name__=="__main__": run()
