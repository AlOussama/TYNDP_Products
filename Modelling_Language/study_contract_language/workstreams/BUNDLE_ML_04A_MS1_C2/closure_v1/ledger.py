"""Coordinate-level native Program contribution lineage.
Reuse original N7 atomic coverage and identities as a first validation step.
Event identity is globally declared and canonical across axis order/aliases.
"""
from collections import Counter
from types import SimpleNamespace
from itertools import product
from copy import deepcopy
import mathspec.program as mp
from closure import fields,need,qualified,digest,Reject
from closure_v1.metadata import index
from closure_v1.r1_reuse import ident
from n7 import contribution_table

def validate_events(rows,tables,sources):
    out=index(rows);seen=set()
    for k,r in out.items():
        fields(r,("id","case","event_key","coordinate","source_ref"),"EVENT_FIELDS")
        need(qualified(k) and qualified(r["case"]) and type(r["event_key"]) is str and bool(r["event_key"]) and r["source_ref"] in sources,"EVENT_ID")
        coord=r["coordinate"];need(type(coord) is dict and all(a in tables["domains"] and v in tables["domains"][a]["members"] and type(v) is type(tables["domains"][a]["members"][0]) for a,v in coord.items()),"EVENT_COORDINATE")
        key=digest([r["case"],r["event_key"],coord]);need(key not in seen,"DUPLICATE_EVENT_IDENTITY");seen.add(key)
    return out
def semantic(spec):
    if spec is None:return None
    x=deepcopy(spec);x["contributions"]=sorted(x["contributions"],key=lambda r:r["id"])
    x["global_disjoint"]=sorted(x["global_disjoint"])
    for k,v in x["expected"].items():x["expected"][k]=sorted(v)
    return x
def receipt(lineage):
    return {n:[{"key":list(k),"events":dict(sorted(v.items()))} for k,v in sorted(rows.items())] for n,rows in sorted(lineage.items())}

def evaluate(bound,spec,events,incoming,observables):
    fields(spec,("bindings","key_axes","contributions","policy","global_disjoint","expected"),"LEDGER_FIELDS")
    p=bound.program;consumer=bound.consumer;sig=bound.symbols
    inputs={z["native_name"]:z for z in sig.values() if z["role"]!="DERIVED_EXPRESSION" and z["role"]!="METHOD_PARAMETER"}
    bindings=spec["bindings"];axes=spec["key_axes"];need(type(bindings) is dict and set(bindings)==set(inputs)==set(axes),"LEDGER_INPUT_BINDINGS")
    byname={n:z["symbol_id"] for n,z in inputs.items()}
    ordered={};cells={};used=set()
    for n,b in bindings.items():
        fields(b,("role","observable","case","data_ref"),"LEDGER_BINDING_FIELDS")
        z=inputs[n];sym=z["symbol_id"];want=z["domain_ids"];have=axes[n]
        need(type(have) is list and len(have)==len(want) and set(have)==set(want),"LEDGER_KEY_AXES")
        ordered[n]={tuple(k[want.index(a)] for a in have):v for k,v in consumer.data[n].items()};cells[n]={k:Counter() for k in consumer.data[n]}
        if sym in incoming:
            need(b["role"]=="auxiliary" and b["data_ref"]==sym and b["observable"]==b["case"]=="","UPSTREAM_LEDGER_ROLE")
            upstream=incoming[sym];need(not upstream or set(upstream)==set(cells[n]),"UPSTREAM_LINEAGE_SUPPORT")
            if upstream:cells[n]={k:Counter(v) for k,v in upstream.items()}
        elif b["role"]=="contribution":
            need(sym in observables and b["observable"]==observables[sym] and bound.tables["observables"][b["observable"]]["subject"]==b["case"] and b["data_ref"]=="","CONTRIBUTION_SIGNATURE")
        else:
            need(b["role"]=="auxiliary" and b["data_ref"]==sym and b["observable"]==b["case"]=="","AUXILIARY_SIGNATURE")
    try:
        # Original unchanged N7 row coverage/duplicate ID validation.
        contribution_table(spec["contributions"],{n:SimpleNamespace(values=v) for n,v in ordered.items()},bindings)
    except (ValueError,TypeError,KeyError) as e:raise Reject("N7_CONTRIBUTION:"+str(e)) from e
    for r in spec["contributions"]:
        n=r["series"];z=inputs[n];ev=events.get(r["event"]);need(ev is not None and ev["case"]==r["case"],"EVENT_CASE")
        env=dict(zip(axes[n],r["key"],strict=True))
        need(all(env.get(a)==v for a,v in ev["coordinate"].items()),"EVENT_COORDINATE_BINDING")
        key=tuple(env[a] for a in z["domain_ids"]);cells[n][key][ev["id"]]+=1;used.add(ev["id"])
    policy=spec["policy"];expected=spec["expected"]
    need(type(policy) is dict and set(policy)==set(p.expressions) and all(v in ("DISJOINT","ALLOW_REUSE") for v in policy.values()),"LEDGER_POLICY_SCOPE")
    need(type(expected) is dict and set(expected)<=set(p.expressions),"LEDGER_EXPECTED_SCOPE")
    gd=spec["global_disjoint"];need(type(gd) is list and len(gd)==len(set(gd)) and set(gd)<=set(p.expressions),"LEDGER_DISJOINT_SCOPE")
    cache={};active=set()
    def total(xs):
        a=Counter()
        for x in xs:a.update(x)
        return a
    def envkey(n,env):return tuple(env[a] for a in n.dims)
    def rule(n,env):
        node=p.expressions[n].expression;k=(n,envkey(node,env))
        if k in cache:return cache[k].copy()
        need(k not in active,"LEDGER_CYCLE");active.add(k);v=walk(node,env)
        if policy[n]=="DISJOINT":need(all(x==1 for x in v.values()),"SEMANTIC_DOUBLE_COUNT")
        cache[k]=v;active.remove(k);return v.copy()
    def has_atoms(n):return any(cells.get(n,{}).values())
    def joined(n,env,row):
        updated=dict(env)
        for role in n.columns.joined:updated[n.columns.dim(role)]=row[role]
        return walk(n.operand,updated)
    def walk(n,env):
        t=type(n)
        if t is mp.Constant:return Counter()
        if t is mp.ParameterReference:return cells[n.name][envkey(n,env)].copy() if n.name in cells else Counter()
        if t is mp.ExpressionReference:return rule(n.name,env)
        if t is mp.Negate:return walk(n.operand,env)
        if t in (mp.Translate,mp.WindowSum):return total(walk(n.operand,x) for x in consumer.neighbors(n,env))
        if t is mp.Join:
            rows=consumer.matches(n.columns,env);need(n.columns.one_row_per_group and len(rows)==1,"LEDGER_RELATION_CARDINALITY")
            return joined(n,env,rows[0])
        if t is mp.Sum:
            if any(a.column is not None for a in n.over):
                j=n.operand;need(type(j) is mp.Join,"LEDGER_GROUP_SUM")
                return total(joined(j,env,row) for row in consumer.matches(j.columns,env))
            names=[a.dimension for a in n.over]
            return total(walk(n.operand,{**env,**dict(zip(names,key))}) for key in product(*(consumer.axes[a] for a in names)))
        if t is mp.Cases:
            need(not any(has_atoms(x) for r in n.regions for x in r.when.names_read),"CONTRIBUTION_CONTROL_DEPENDENCY")
            selected=[r for r in n.regions if consumer.cond(r.when.root,env)];need(len(selected)==1,"CASE_TOTALITY")
            return walk(selected[0].value,env)
        if t in (mp.Add,mp.Multiply,mp.Divide,mp.Power):
            a,b=(n.left,n.right) if t in (mp.Add,mp.Multiply) else (n.numerator,n.divisor) if t is mp.Divide else (n.base,n.exponent)
            x,y=walk(a,env),walk(b,env)
            if t is mp.Add:return x+y
            if t is mp.Multiply:need(not(x and y),"NONLINEAR_CONTRIBUTION_PRODUCT");return x+y
            if t is mp.Divide:need(not y,"CONTRIBUTION_DIVISOR");return x
            need(not(x or y),"CONTRIBUTION_POWER");return Counter()
        raise Reject("LEDGER_NATIVE_NODE_DEFERRED:"+t.__name__)
    results={}
    for n,e in p.expressions.items():
        dims=e.expression.dims
        rr={key:rule(n,dict(zip(dims,key))) for key in product(*(consumer.axes[a] for a in dims))}
        all_=total(rr.values())
        if n in gd:need(all(v==1 for v in all_.values()),"SEMANTIC_DOUBLE_COUNT")
        if n in expected:
            want=expected[n];need(type(want) is list and len(want)==len(set(want)) and set(want)<=set(events) and set(all_)==set(want),"CONTRIBUTION_COMPLETENESS")
        results[n]=rr
    return results,used
