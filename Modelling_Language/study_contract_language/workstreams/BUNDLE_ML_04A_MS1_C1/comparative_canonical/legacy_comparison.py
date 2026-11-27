"""M2 native-to-existing R1 adapters, no modifications to R1/C21.
Two distinct targets: outer R1 predicate AST and original method Engine.
"""
import json,sys,copy
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import mathspec.program as mp
ROOT=Path(__file__).resolve().parents[1]
R1=ROOT.parent/"BUNDLE_ML_04A_R1"
sys.path.insert(0,str(R1))
import n1r
from profile_engine import Engine
from make_fixtures import measure,quant,cmp
class Unsupported(ValueError):pass
def need(x,code):
    if not x:raise Unsupported(code)
def get_scalar(rows):need(len(rows)==1 and rows[0]["key"]==[],"SCALAR_REQUIRED");return F(rows[0]["value"])
def opref(op,id):return {"op":op,"id":id}
def lit(v):return {"op":"literal","value":str(F(v)),"unit":"1"}
def binary(op,a,b):return {"op":op,"lhs":a,"rhs":b}
OPS={"==":"eq","=":"eq","<=":"le",">=":"ge","<":"lt",">":"gt"}

def map_profile(case,program,data=None):
    """Native Program -> original executable profile AST, finite fixture scope.

    Translation preserves weight roles supplied by fixture; explicit unity
    vector for unweighted time sum is a derived adapter artifact. No false
    substitution of physical units by dimensionless weights.
    """
    data=data or case["data"];c=case["context"]
    axes={n:{"role":case["axis_roles"].get(n,"sample"),"ids":z["labels"]} for n,z in c["domains"].items()}
    # Engine requires a nonempty axis registry even for scalar rules.
    if not axes:axes={"aux_scalar_axis":{"role":"sample","ids":["only"]}}
    series={};inputs={};parameters={};values={};generated=[];mapped=set()
    for n,p in program.parameters.items():
        z=c["symbols"][n];q=z["quantity"];basis="" if q["basis"]=="NONE" else q["basis"]
        role=z["role"]
        if role=="METHOD_PARAMETER":
            need(not p.dims and q["unit"]=="1","PROFILE_PARAMETER_TYPE:"+n)
            v=get_scalar(data["parameters"][n])
            # Finite specialization: original profile engine needs an explicit range.
            parameters[n]={"unit":"1","min":str(v),"max":str(v)};values[n]=str(v)
            continue
        spec={"unit":q["unit"],"basis":basis,"axes":list(p.dims),"role":case["weight_roles"].get(n,"value")}
        inputs[n]=spec;series[n]={**spec,"rows":data["parameters"][n]}
    def e(node):
        t=type(node);mapped.add(t.__name__)
        if t is mp.ParameterReference:return opref("param" if node.name in parameters else "input",node.name)
        if t is mp.ExpressionReference:return opref("rule",node.name)
        if t is mp.Constant:
            need(float(node.value).is_integer() and abs(node.value)<=2**53-1,"PROFILE_LITERAL")
            return lit(int(node.value))
        if t is mp.Negate:return binary("mul",lit(-1),e(node.operand))
        if t in (mp.Add,mp.Multiply):return binary("add" if t is mp.Add else "mul",e(node.left),e(node.right))
        if t is mp.Divide:return binary("div",e(node.numerator),e(node.divisor))
        if t is mp.Power:return binary("pow",e(node.base),e(node.exponent))
        if t is mp.Sum:
            need(len(node.over)==1 and node.over[0].column is None,"PROFILE_RELATION_OR_MULTI_SUM")
            ax=node.over[0].dimension;body=node.operand;w=None
            if type(body) is mp.Multiply:
                for x,y in ((body.left,body.right),(body.right,body.left)):
                    if type(x) is mp.ParameterReference and x.name in inputs and inputs[x.name]["role"] in ("probability","time_weight") and inputs[x.name]["axes"]==[ax]:
                        w=x.name;body=y;break
            if w is None:
                need(axes[ax]["role"]=="time","PROFILE_UNWEIGHTED_NON_TIME_SUM")
                w="__unity_"+ax;need(w not in program.parameters,"UNITY_ALIAS")
                if w not in inputs:
                    inputs[w]={"unit":"1","basis":"","axes":[ax],"role":"time_weight"}
                    series[w]={**inputs[w],"rows":[{"key":[i],"value":"1"} for i in axes[ax]["ids"]]}
                    generated.append({"id":w,"reason":"Unweighted algebraic sum; explicit unity reduction, not physical duration."})
            return {"op":"weighted_sum","expr":e(body),"axis":ax,"weight":w}
        raise Unsupported("PROFILE_NODE_UNMAPPED:"+t.__name__)
    rules={}
    for n,x in program.expressions.items():
        q=c["symbols"][n]["quantity"];rules[n]={"expr":e(x.expression),"unit":q["unit"],"basis":"" if q["basis"]=="NONE" else q["basis"],"axes":list(x.dims)}
    need(bool(rules),"NO_PROFILE_OUTPUT")
    method={"id":"method:comparison","version":"1","schema":"profile-r1","operator_version":"operators-r1","source":{},"approval":"RESEARCH_ASSUMPTION","assumptions":["Finite shared mathematical fragment; not full method governance."],"parameters":parameters,"inputs":inputs,"rules":rules}
    study={"id":"study:comparison","version":"1","schema":"profile-r1","method_ref":{},"parameters":values,"data_ref":{},"contract_ref":"","status":"OWNER_TBD"}
    engine=Engine(method,study,{"axes":axes,"series":series,"pairs":[]})
    result=engine.run()
    return {"outputs":{n:[r["value"] for r in v["rows"]] for n,v in result.items()},"mapped_nodes":sorted(mapped),"generated_bindings":generated,"mapped_rules":rules,"stage":"ORIGINAL_R1_PROFILE_ENGINE_ONLY","owner":"OWNER_TBD","method_parameter_specializations":parameters}

def template(case):
    id=case["id"];c=case["context"]
    if id=="RC01":
        path=ROOT/"WS_B_original_reference_corpus"/"syntax_B"/"RC01.partial.json"
        return json.loads(path.read_text())
    # General skeleton for direct comparison fragments. Static representative
    # quantity values are not an evaluation of data series.
    d={k:[] for k in n1r.c21.COLLECTIONS}
    domains=[{"id":z["id"],"kind":"time","members":[str(v) for v in z["labels"]]} for n,z in c["domains"].items()]
    need(all(case["axis_roles"].get(n)=="time" and all(type(v) is str for v in z["labels"]) for n,z in c["domains"].items()),"LEGACY_DOMAIN_KIND")
    d["frame"]={"id":"study:"+id,"schema":n1r.VERSION[0],"ruleset":n1r.VERSION[1],"registry":n1r.VERSION[2],"question":"Comparative direct observable fragment "+id,
      "time":{"id":"duration:research","duration":"1","duration_unit":"h"},"domains":domains,
      "scopes":[{"id":"scope:research","domains":[x["id"] for x in domains]}],"guards":[],"information_sets":[],"data_inputs":[],"method_slots":[]}
    d["authorities"]=[{"id":"source:comparison","role":"SOURCE","immutable_ref":"fixture:"+id,"revision":"1","decision_state":"OWNER_TBD"}]
    for n,z in c["symbols"].items():
        if z["role"]!="OBSERVABLE" or n not in case["doc"]["parameters"]:continue
        qq=z["quantity"];kind={"MW":"active_power","MWh":"energy","kg":"mass","kg/h":"mass_flow","EUR":"cost"}.get(qq["unit"])
        need(kind is not None,"LEGACY_QUANTITY:"+qq["unit"])
        x={"carrier":qq["carrier"],"kind":kind,"unit":qq["unit"],"value":"0","sign":qq["sign"]}
        if qq["basis"]!="NONE":x["basis"]=qq["basis"]
        d["referents"].append({"id":z["id"],"kind":"entity","type":qq["carrier"]+"."+kind,"quantity":x,"axes":[c["domains"][a]["id"] for a in sorted(case["doc"]["parameters"][n]["dims"])]})
    for k in case["doc"]["conditions"]:
        pid=c["predicates"][k]["id"]
        d["predicates"].append({"id":pid,"expr":{"op":"bool3","value":"UNKNOWN"}})
        aid="assert:"+k
        d["assertions"].append({"id":aid,"modality":"REQUIRED","semantic_role":"SAFETY_GUARANTEE","predicate_ref":pid,"scope":"scope:research","guard":True,"authority_refs":["source:comparison"],"decision_state":"OWNER_TBD"})
        d["evidences"].append({"id":"evidence:"+k,"role":"REQUEST","subject_ref":aid,"status":"NOT_EXECUTED","oracle":"research:static-only"})
    return d

def map_predicates(case,program):
    c=case["context"];mapped=set();special=[]
    # Translation must not discard a native expression or obligation just to
    # manufacture a pass: only inline supported expressions in the predicates.
    def expression(e):
        t=type(e);mapped.add(t.__name__)
        if t is mp.ExpressionReference:return expression(e.body)
        if t is mp.ParameterReference:
            z=c["symbols"][e.name];need(z["role"]=="OBSERVABLE","LEGACY_SYMBOL_ROLE:"+z["role"])
            return measure(z["id"],*e.dims)
        if t is mp.Multiply and case["id"]=="RC01":
            for a,b in ((e.left,e.right),(e.right,e.left)):
                if type(a) is mp.ParameterReference and type(b) is mp.ParameterReference and b.name=="dt" and not b.dims and a.name=="p":
                    need(get_scalar(case["data"]["parameters"]["dt"])==F(1,2),"LEGACY_DURATION_MISMATCH")
                    special.append("Native dt parameter specialized to original frame duration:t0 = 0.5 h")
                    return {"op":"integrate","duration_ref":"duration:t0","expr":expression(a)}
        raise Unsupported("LEGACY_PREDICATE_EXPRESSION:"+t.__name__)
    def condition(n):
        t=type(n);mapped.add(t.__name__)
        if t is mp.ConditionReference:return condition(n.body)
        if t is mp.ExpressionComparison:
            need(n.op in OPS,"LEGACY_COMPARISON_OPERATOR")
            return cmp(expression(n.left),expression(n.right),OPS[n.op])
        if t in (mp.And,mp.Or):return {"op":"and" if t is mp.And else "or","args":[condition(n.left),condition(n.right)]}
        if t is mp.Not:return {"op":"not","args":[condition(n.operand)]}
        raise Unsupported("LEGACY_CONDITION:"+t.__name__)
    body={}
    for n,p in program.conditions.items():
        x=condition(p.condition.root)
        for ax in reversed(c["scope"]["binders"]):
            if ax in p.dims:
                need(case["axis_roles"].get(ax)=="time","LEGACY_DOMAIN_KIND")
                x=quant("forall",ax,"time",c["domains"][ax]["id"],x)
        body[n]=x
    need(bool(body),"NO_LEGACY_PREDICATE")
    d=template(case)
    if case["id"]=="RC01":d["predicates"][0]["expr"]=body["exchange_ok"]
    else:
        for a in d["predicates"]:a["expr"]=body[next(n for n,z in c["predicates"].items() if z["id"]==a["id"])]
    a=n1r.run(n1r.emit_a(d),"A");b=n1r.run(json.dumps(d),"B")
    need(a["semantic_digest"]==b["semantic_digest"] and a["audit_digest"]==b["audit_digest"],"LEGACY_DUAL_ROUNDTRIP")
    return {"stage":"R1_C21_STATIC_ONLY","status":b["status"],"blocked":b["blocked"],"semantic_digest":b["semantic_digest"],"audit_digest":b["audit_digest"],"mapped_nodes":sorted(mapped),"specializations":special,"body":body,"contract":d,"full_path":False}
def m0_control(case):
    id=case["id"]
    if id=="RC01":
        r=ROOT/"WS_B_original_reference_corpus";a=n1r.run((r/"syntax_A/RC01.partial.scn").read_text(),"A");b=n1r.run((r/"syntax_B/RC01.partial.json").read_text(),"B")
    elif id in ("RC07","RC10"):
        d=template(case)
        # Independently authored legacy expression, not a call to native mapper.
        x={"op":"compare","cmp":"eq","lhs":{"op":"measure","ref":"ref:a","indices":[]},"rhs":{"op":"measure","ref":"ref:b","indices":[]}}
        if id=="RC07":
            for side in ("lhs","rhs"):x[side]["indices"]=[{"op":"var","name":"t"}]
            x={"op":"forall","var":"t","domain":{"kind":"time","ref":"domain:t"},"body":x}
        d["predicates"][0]["expr"]=x
        a=n1r.run(n1r.emit_a(d),"A");b=n1r.run(json.dumps(d),"B")
    else:raise Unsupported("NO_INDEPENDENT_LEGACY_CONTROL_FOR_THIS_FRAGMENT")
    need(a["semantic_digest"]==b["semantic_digest"] and a["audit_digest"]==b["audit_digest"],"M0_DUAL")
    return {"stage":"R1_C21_STATIC_ONLY","status":b["status"],"blocked":b["blocked"],"semantic_digest":b["semantic_digest"],"audit_digest":b["audit_digest"],"full_path":False}
