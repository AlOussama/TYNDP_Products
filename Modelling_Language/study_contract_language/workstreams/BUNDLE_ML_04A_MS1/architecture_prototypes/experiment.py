"""Executable finite checks and separate arithmetic oracles for MS1.
Run in the locked upstream environment; not original contract paths."""
from copy import deepcopy
from pathlib import Path
from hashlib import sha256
import json, sys
import mathspec as ms
from adapter import Consumer, Rejected, decl, input_series, F, compile_profile, file_hash, type_of, digest, need
HERE=Path(__file__).resolve().parent
R1=HERE.parent.parent/"BUNDLE_ML_04A_R1"
def read(p): return json.loads(Path(p).read_text())
def check_reject(fn,code):
    try: fn()
    except Rejected as exc:
        assert str(exc)==code,(str(exc),code);return
    raise AssertionError("accepted negative: "+code)
def consumer(axes,d,v,e):
    return Consumer(axes,d,input_series(axes,d,v),e)
def check_rc():
    out=[]
    def record(id,passed,negative,scope):
        assert passed and negative,id
        out.append(dict(id=id,positive=bool(passed),negative=bool(negative),scope=scope))
    a={"t":["0"]}; d={k:decl(["t"],u) for k,u in {"p":"MW","dt":"h","intake":"MWh","soc":"1","capacity":"MWh","energy":"MWh"}.items()}
    e={"expected":"-p * dt","observed":"intake","from_soc":"soc * capacity","state":"energy"}
    v={"p":[-2],"dt":["1/2"],"intake":[1],"soc":["19/40"],"capacity":[4],"energy":["19/10"]}
    c=consumer(a,d,v,e); v2=deepcopy(v);v2["intake"]=[2]; bad=consumer(a,d,v2,e)
    record("RC01",c.verify("expected","observed","eq") and c.verify("from_soc","state","eq") and c.table("expected")[("0",)].value==F(1),not bad.verify("expected","observed","eq"),"single-step projected observations")
    a={"ev":["a","b"]};d={k:decl(["ev"],"MWh") for k in ("delivered","required")}
    e={"actual":"delivered","request":"required"};v={"delivered":[1,1],"required":[1,1]}
    c=consumer(a,d,v,e);v["delivered"]=[0,2];bad=consumer(a,d,v,e)
    record("RC02",c.verify("actual","request","ge"),not bad.verify("actual","request","ge"),"complete per-EV witness; not universal service")
    a={"t":["0"]};d={k:decl(["t"],u) for k,u in {"power":"MW","hydrogen":"kg/h","lhv":"MWh_H2_LHV/kg","eta_low":"LHV_ratio","eta_high":"LHV_ratio"}.items()}
    e={"output":"hydrogen * lhv","low":"power * eta_low","high":"power * eta_high"}; v={"power":[1],"hydrogen":[21],"lhv":["1/30"],"eta_low":["3/5"],"eta_high":["4/5"]}
    def envelope(c):return c.verify("output","low","ge") and c.verify("output","high","le")
    c=consumer(a,d,v,e); v["hydrogen"]=[18];c2=consumer(a,d,v,e);v["hydrogen"]=[30];bad=consumer(a,d,v,e)
    record("RC03",envelope(c) and envelope(c2) and c.table("output")!=c2.table("output"),not envelope(bad),"two different feasible outputs; common envelope")
    a={"t":["0"]};d={k:decl(["t"],u) for k,u in {"initial":"kg","final":"kg","inflow":"kg/h","outflow":"kg/h","dt":"h"}.items()}
    e={"expected":"initial + (inflow - outflow) * dt","observed":"final"};v={"initial":[2],"final":[3],"inflow":[3],"outflow":[1],"dt":["1/2"]}
    c=consumer(a,d,v,e);v["final"]=[4];bad=consumer(a,d,v,e)
    record("RC04",c.verify("expected","observed","eq"),not bad.verify("expected","observed","eq"),"explicit boundary state only; shift execution deferred")
    a={"bus":["a","b","c"],"branch":["1","2","3"]}
    d={"flow":decl(["branch"],"MW"),"incidence":decl(["bus","branch"]),"injection":decl(["bus"],"MW"),"zero":decl([],"MW")}
    e={"nodal":"sum(flow * incidence, over=branch)","p":"injection","loop":"sum(flow, over=branch)","target":"zero"}
    v={"flow":[-1,-1,2],"incidence":[1,0,-1,-1,1,0,0,-1,1],"injection":[-3,0,3],"zero":[0]}
    c=consumer(a,d,v,e);v["flow"]=[0,0,3];bad=consumer(a,d,v,e)
    record("RC05",c.verify("nodal","p","eq") and c.verify("loop","target","eq"),bad.verify("nodal","p","eq") and not bad.verify("loop","target","eq"),"equal reactances triangle; KCL not sufficient for KVL")
    a={"site":["a"]};d={"modules":decl(["site"],dtype="int"),"capacity":decl(["site"],dtype="int")};e={"built":"modules","limit":"capacity"};v={"modules":[2],"capacity":[3]}
    c=consumer(a,d,v,e);v["modules"]=["1/2"];check_reject(lambda:consumer(a,d,v,e),"INTEGER_DOMAIN")
    record("RC06",c.verify("built","limit","le"),True,"integer domain")
    a={"pair":["a","b"]};d={k:decl(["pair"]) for k in ("a","b","info")};e={"left":"a","right":"b"};v={"a":[2,1],"b":[2,3],"info":[1,0]}
    c=consumer(a,d,v,e);v["b"]=[3,3];bad=consumer(a,d,v,e);v["info"]=[0,0];empty=consumer(a,d,v,e)
    check_reject(lambda:empty.verify("left","right","eq","info"),"VACUOUS_SUPPORT");v["info"]=[1,"UNKNOWN"];check_reject(lambda:consumer(a,d,v,e),"UNKNOWN_OR_NONEXACT_VALUE")
    record("RC07",c.verify("left","right","eq","info"),not bad.verify("left","right","eq","info"),"provided information pairs only")
    print("FINITE_RC="+json.dumps(out,sort_keys=True))
    # ablation: native index typing alone accepts physically incompatible symbols
    c=consumer({"t":["0"]},{"p":decl(["t"],"MW"),"m":decl(["t"],"kg/h")},{"p":[1],"m":[1]},{"bad":"p + m"})
    check_reject(lambda:c.table("bad"),"PHYSICAL_TYPE_MISMATCH")
    check_reject(lambda:Consumer({"t":[]},{},{},{}),"EMPTY_OR_DUPLICATE_DOMAIN")
    check_reject(lambda:Consumer({"t":["0","1"]},{"p":decl(["t"],"MW")},{"p":{("0",):1}},{"out":"p"}),"INCOMPLETE_SUPPORT")
    print("ABLATION_WITNESSES=unit_mismatch_native_accepts_consumer_rejects;missing_support;empty_domain;unknown_guard;vacuous_guard")
def profiles():
    fx=R1/"fixtures"; code=[HERE/"adapter.py",Path(ms.__file__).parent/"_expression_parser.py",Path(ms.__file__).parent/"_condition_parser.py",Path(ms.__file__).parent/"_lowering.py",Path(ms.__file__).parent/"_canonical.py"]
    before={p.name:file_hash(p) for p in code}
    receipts=[]
    def run(method,study,data,expected,out_unit,basis,source_id):
        c=compile_profile(method,study,data);q=c.scalar("summary")
        assert q.value==expected and q.type==type_of(out_unit,basis)
        assert study["status"]=="OWNER_TBD"
        receipt=dict(method=method["id"],method_identity=digest(method),data_identity=digest(data),
                     output_observable=source_id,unit=out_unit,basis=basis,value=str(q.value),owner=study["status"],
                     canonical_sha256=sha256(c.canonical.encode()).hexdigest(),code_hashes=before)
        receipt["audit_identity"]=digest(receipt);receipts.append(receipt)
    for label,expected in [("begin",F(415,11)),("end",F(4150,121))]:
        mp=fx/f"method-{label}.json"; dp=fx/"data.json"; st=read(fx/f"study-{label}.json")
        assert file_hash(mp)==st["method_ref"]["sha256"] and file_hash(dp)==st["data_ref"]["sha256"]
        run(read(mp),st,read(dp),expected,"EUR","EUR:real:2024","ms1:cost-summary")
    pro=HERE/"profiles"
    for label,expected in [("gross",F(5)),("eligible",F(3))]:
        run(read(pro/f"{label}.json"),read(pro/"study.json"),read(pro/"data.json"),expected,"MWh","","ms1:energy-summary")
    assert before=={p.name:file_hash(p) for p in code}
    assert len({r["method_identity"] for r in receipts})==4 and len({r["audit_identity"] for r in receipts})==4
    assert receipts[0]["data_identity"]==receipts[1]["data_identity"] and receipts[2]["data_identity"]==receipts[3]["data_identity"]
    bad=read(pro/"gross.json");bad["rules"]["summary"]["expr"]={"op":"python"}
    check_reject(lambda:compile_profile(bad,read(pro/"study.json"),read(pro/"data.json")),"PROFILE_OPERATOR_NOT_ALLOWED")
    bad=read(pro/"gross.json");bad["rules"]["summary"]["unit"]="MW"
    check_reject(lambda:compile_profile(bad,read(pro/"study.json"),read(pro/"data.json")),"RULE_TYPE")
    print("METHOD_RECEIPTS="+json.dumps(receipts,sort_keys=True))
    print("METHOD_SCOPE=FOUR_NATIVE_MATH_LAYER_SWAPS;FULL_CSNF_INTEGRATION_NOT_PROVED")
if __name__=="__main__":
    check_rc();profiles()
