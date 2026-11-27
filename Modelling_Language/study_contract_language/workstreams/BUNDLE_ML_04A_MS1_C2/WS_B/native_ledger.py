"""Bounded N7-compatible contribution lineage over the *native* public Program."""
from collections import Counter
from types import SimpleNamespace
import mathspec.program as mp
from closure import fields,need,Reject
from n7 import contribution_table,ident,unique

def check(consumer,leaf,profile,context):
    spec=profile["ledger"]
    fields(spec,("policy","bindings","key_axes"),"LEDGER_FIELDS")
    policy=spec["policy"];bindings=spec["bindings"]
    fields(policy,("schema","id","version","rules","expected"),"LEDGER_POLICY_FIELDS")
    need(policy["schema"]=="ledger-policy-r1","LEDGER_VERSION")
    ident(policy["id"]);need(type(policy["version"]) is str and bool(policy["version"]),"LEDGER_VERSION")
    p=consumer.program
    need(set(policy["rules"])==set(p.expressions) and set(policy["expected"])<=set(p.expressions),"LEDGER_POLICY_SCOPE")
    inputs={z["native_name"]:z for z in leaf["interface"]["method_signature"]["inputs"]}
    need(type(bindings) is dict and set(bindings)==set(inputs),"LEDGER_INPUT_BINDINGS")
    axes=spec["key_axes"];need(type(axes) is dict and set(axes)==set(inputs),"LEDGER_KEY_AXES")
    ordered={}
    for n,b in bindings.items():
        fields(b,("role","observable","case","data_ref"),"LEDGER_BINDING_FIELDS")
        z=inputs[n];sym=z["symbol_id"];role=leaf["context"]["symbols"][n]["role"]
        want=z["domain_ids"];have=axes[n]
        need(type(have) is list and len(have)==len(want) and set(have)==set(want),"LEDGER_KEY_AXES")
        ordered[n]={tuple(k[want.index(a)] for a in have):v for k,v in consumer.data[n].items()}
        if b["role"]=="contribution":
            need(role=="OBSERVABLE" and profile["input_roles"][sym]=="VALUE" and b["observable"]==sym and type(b["case"]) is str and bool(b["case"]) and b["data_ref"]=="","CONTRIBUTION_SIGNATURE")
        else:
            need(b["role"]=="auxiliary" and role=="INPUT" and b["data_ref"]==sym and b["observable"]==b["case"]=="","AUXILIARY_SIGNATURE")
    byid={z["symbol_id"]:n for n,z in inputs.items()}
    for pair in profile["counterfactual_pairs"]:
        a=bindings[byid[pair["reference"]]];b=bindings[byid[pair["alternative"]]]
        need(a["role"]==b["role"]=="contribution" and a["case"]!=b["case"],"LEDGER_COUNTERFACTUAL_CASE")
    need(type(context["contributions"]) is list,"CONTRIBUTION_LIST")
    try:
        # Original implementation, not a C2 reimplementation of atomic identity or coverage.
        atoms=contribution_table(context["contributions"],{n:SimpleNamespace(values=ordered[n]) for n in inputs},bindings)
    except (ValueError,KeyError,TypeError) as e:
        raise Reject("N7_CONTRIBUTION:"+str(e)) from e
    cache={};active=set()
    def rule(n):
        if n in cache:return cache[n].copy()
        need(n not in active,"LEDGER_CYCLE");active.add(n)
        x=walk(p.expressions[n].expression);mode=policy["rules"][n]
        need(mode in ("DISJOINT","ALLOW_REUSE"),"LEDGER_POLICY")
        if mode=="DISJOINT":need(all(v==1 for v in x.values()),"SEMANTIC_DOUBLE_COUNT")
        if n in policy["expected"]:
            need(set(x)==set(unique(policy["expected"][n])),"CONTRIBUTION_COMPLETENESS")
        active.remove(n);cache[n]=x;return x.copy()
    def walk(n):
        t=type(n)
        if t is mp.Constant:return Counter()
        if t is mp.ParameterReference:return atoms.get(n.name,Counter()).copy()
        if t is mp.ExpressionReference:return rule(n.name)
        if t is mp.Negate:return walk(n.operand)
        if t is mp.Sum:
            need(all(a.column is None for a in n.over),"LEDGER_RELATION_SUM_DEFERRED")
            return walk(n.operand)
        if t in (mp.Add,mp.Multiply,mp.Divide,mp.Power):
            a,b=(n.left,n.right) if t in (mp.Add,mp.Multiply) else (n.numerator,n.divisor) if t is mp.Divide else (n.base,n.exponent)
            x,y=walk(a),walk(b);out=set(n.dims)
            need((not x or set(a.dims)==out) and (not y or set(b.dims)==out),"CONTRIBUTION_BROADCAST_UNSUPPORTED")
            if t is mp.Add:return x+y
            if t is mp.Multiply:need(not(x and y),"NONLINEAR_CONTRIBUTION_PRODUCT");return x+y
            if t is mp.Divide:need(not y,"CONTRIBUTION_DIVISOR");return x
            need(not(x or y),"CONTRIBUTION_POWER");return Counter()
        raise Reject("LEDGER_NATIVE_NODE_DEFERRED:"+t.__name__)
    return {"status":"FINITE_EXECUTED","lineage":{n:dict(sorted(rule(n).items())) for n in p.expressions},"scope":"SAME_SUPPORT_AFFINE_FINITE_LINEAGE","conformance":"NOT_PROVED"}
