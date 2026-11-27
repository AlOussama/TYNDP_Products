"""Finite selection contract: native equality membership AND universal ordering.
No solver, new math AST, or comparison computed outside native Program.
"""
import mathspec.program as mp
from closure import need
from closure_v1 import obligations as ob

def native_pair(bound, spec):
    z=spec["row"]
    if z["guard"]!={"truth":"TRUE","reason":None} or z["assumptions"] or z["at"] or z["modality"]!="MUST":
        return None
    if spec["predicate"]["role"]!="PREDICATE":return None
    node=bound.program.conditions[spec["predicate"]["native_name"]].condition.root
    if type(node) is not mp.ExpressionComparison:return None
    refs=(mp.ParameterReference,mp.ExpressionReference)
    if type(node.left) not in refs or type(node.right) not in refs:return None
    byname={s["native_name"]:s for s in bound.symbols.values()}
    a,b=byname[node.left.name],byname[node.right.name];op=node.op
    # Candidate must have exactly one additional finite axis.
    if len(a["domain_ids"])>len(b["domain_ids"]):
        a,b=b,a;op={"<=":">=",">=":"<=","==":"=="}.get(op)
    common=a["domain_ids"]; axes=b["domain_ids"];extra=set(axes)-set(common)
    if len(extra)!=1 or set(common)-set(axes) or len(axes)!=len(common)+1:return None
    if a["quantity"]!=b["quantity"] or a["dtype"]=="bool" or b["dtype"]=="bool":return None
    axis=next(iter(extra))
    if bound.tables["domains"][axis]["kind"] not in ("sample","scenario","response","trace"):return None
    bind=z["binders"]
    if op=="==":
        if z["role"]!="CONDITIONAL_OBLIGATION" or not bind or bind[-1]["axis"]!=axis or bind[-1]["quantifier"]!="EXISTS" or any(x["quantifier"]!="FORALL" for x in bind[:-1]):return None
    elif op in ("<=",">="):
        if z["role"]!="SAFETY_GUARANTEE" or any(x["quantifier"]!="FORALL" for x in bind):return None
    else:return None
    if set(x["axis"] for x in bind)!=set(axes):return None
    return (a["symbol_id"],b["symbol_id"],axis,z["scope"]),op

def validate(bound,assertions,required_ids):
    specs=ob.validate(bound,assertions)
    need(type(required_ids) is list and len(required_ids)==len(set(required_ids)) and all(x in specs for x in required_ids),"SELECTOR_ASSERTION_REF")
    parts={}
    for k in required_ids:
        p=native_pair(bound,specs[k])
        if p:
            key,op=p
            parts.setdefault(key,{}).setdefault(op,[]).append(k)
    need(bool(parts),"SELECTOR_NATIVE_PAIR_REQUIRED")
    pairs=[]
    for key,ops in sorted(parts.items()):
        need(set(ops) in ({"==","<="},{"==",">="}) and all(len(v)==1 for v in ops.values()),"SELECTOR_MEMBERSHIP_AND_ORDER_REQUIRED")
        sel,cand,axis,scope=key;op=next(x for x in ops if x!="==")
        pairs.append({"selected":sel,"candidate":cand,"axis":axis,"scope":scope,"membership":ops["=="][0],"ordering":ops[op][0],"direction":"MIN" if op=="<=" else "MAX"})
    return pairs
