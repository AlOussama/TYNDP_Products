"""MS1 bounded, solver-free public Program consumer. No own math parser.
Research only. Complete finite numeric observations; no general interpreter.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from pathlib import Path
import json, re
import mathspec as ms
import mathspec.program as mp

class Rejected(ValueError): pass

def need(ok, code):
    if not ok: raise Rejected(code)

def digest(x): return sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def file_hash(p): return sha256(Path(p).read_bytes()).hexdigest()
def dim(d): return tuple(sorted((k,v) for k,v in d.items() if v))
def combine(a,b,sign=1):
    d=dict(a)
    for k,v in b: d[k]=d.get(k,0)+sign*v
    return dim(d)
UNITS={"1":{}, "MW":{"electric_energy":1,"time":-1},
       "MWh":{"electric_energy":1},"h":{"time":1},
       "kg":{"H2_mass":1},"kg/h":{"H2_mass":1,"time":-1},
       "MWh_H2_LHV/kg":{"H2_LHV_energy":1,"H2_mass":-1},
       "MW_H2_LHV":{"H2_LHV_energy":1,"time":-1},
       "LHV_ratio":{"H2_LHV_energy":1,"electric_energy":-1}}
def type_of(unit,basis=""):
    if unit=="EUR":
        need(bool(re.fullmatch(r"EUR:(real|nominal):[0-9]{4}",basis)),"PRICE_BASIS")
        return dim({basis:1})
    need(unit in UNITS and not basis,"UNIT_OR_BASIS")
    return dim(UNITS[unit])

@dataclass(frozen=True)
class Q:
    value:F
    type:tuple=()
    def add(self,b):
        need(self.type==b.type,"PHYSICAL_TYPE_MISMATCH")
        return Q(self.value+b.value,self.type)
    def mul(self,b): return Q(self.value*b.value,combine(self.type,b.type))
    def div(self,b):
        need(b.value!=0,"DIVISION_UNDEFINED")
        return Q(self.value/b.value,combine(self.type,b.type,-1))
    def power(self,b):
        need(not b.type and b.value.denominator==1 and abs(b.value)<=100,"POWER_DOMAIN")
        n=int(b.value)
        need(self.value!=0 or n>0,"POWER_UNDEFINED")
        return Q(self.value**n,dim({k:v*n for k,v in self.type}))

def finite(v):
    need(type(v) in (str,int),"UNKNOWN_OR_NONEXACT_VALUE")
    try: return F(v)
    except (ValueError,ZeroDivisionError): raise Rejected("UNKNOWN_OR_NONEXACT_VALUE")

def coords(axes,names):
    return (dict(zip(names,k)) for k in product(*(axes[n] for n in names)))

class Consumer:
    def __init__(self, axes, declarations, data, expressions):
        need(all(v and len(v)==len(set(v)) for v in axes.values()),"EMPTY_OR_DUPLICATE_DOMAIN")
        self.axes=axes; self.declarations=declarations; self.data={}
        need(set(declarations)==set(data),"BINDING_MISMATCH")
        for name,d in declarations.items():
            need(d["role"] in ("OBSERVABLE","INPUT","METHOD_PARAMETER"),"ROLE")
            names=d["axes"]; need(len(set(names))==len(names) and set(names)<=set(axes),"AXES")
            expected={tuple(c[a] for a in names) for c in coords(axes,names)}
            table=data[name]
            need(set(table)==expected,"INCOMPLETE_SUPPORT")
            typ=type_of(d["unit"],d.get("basis",""))
            self.data[name]={k:Q(finite(v),typ) for k,v in table.items()}
            if d.get("dtype")=="int": need(all(q.value.denominator==1 for q in self.data[name].values()),"INTEGER_DOMAIN")
        doc={"version":0,"dimensions":{a:{} for a in axes},
             "parameters":{n:{"dims":d["axes"],"dtype":d.get("dtype","float"),"missing":"refused"} for n,d in declarations.items()},
             "expressions":expressions}
        self.spec=ms.to_spec(doc)
        self.canonical=self.spec.to_yaml(canonical=True)
        again=ms.to_spec(self.canonical)
        need(again.to_yaml(canonical=True)==self.canonical,"CANONICAL_ROUNDTRIP")
        self.program=again.program
        need(not self.program.variables and not self.program.constraints,"SOLVER_CONSTRUCT")

    def expr(self,node,env):
        t=type(node)
        if t is mp.Constant:
            # Only exact integral literals in this experiment; rational ratios use division.
            need(float(node.value).is_integer(),"NONINTEGRAL_NATIVE_LITERAL")
            return Q(F(int(node.value)))
        if t is mp.ParameterReference:
            d=self.declarations[node.name]
            return self.data[node.name][tuple(env[a] for a in d["axes"])]
        if t is mp.ExpressionReference: return self.expr(node.body,env)
        if t is mp.Negate:
            v=self.expr(node.operand,env); return Q(-v.value,v.type)
        if t is mp.Add: return self.expr(node.left,env).add(self.expr(node.right,env))
        if t is mp.Multiply: return self.expr(node.left,env).mul(self.expr(node.right,env))
        if t is mp.Divide: return self.expr(node.numerator,env).div(self.expr(node.divisor,env))
        if t is mp.Power: return self.expr(node.base,env).power(self.expr(node.exponent,env))
        if t is mp.Sum:
            need(all(a.column is None for a in node.over),"RELATION_SUM_DEFERRED")
            names=[a.dimension for a in node.over]
            vals=[self.expr(node.operand,env|c) for c in coords(self.axes,names)]
            need(bool(vals),"EMPTY_SUM")
            out=vals[0]
            for v in vals[1:]: out=out.add(v)
            return out
        raise Rejected("NODE_NOT_IN_EXECUTABLE_SUBSET:"+t.__name__)

    def table(self,name):
        n=self.program.expressions[name].expression
        return {tuple(c[a] for a in n.dims):self.expr(n,c) for c in coords(self.axes,n.dims)}
    def scalar(self,name): return self.table(name)[()]

    def verify(self,left,right,op,guard=None):
        # Contract comparator, not a claim of native condition semantics.
        l=self.program.expressions[left].expression; r=self.program.expressions[right].expression
        names=sorted(set(l.dims)|set(r.dims))
        if guard: names=sorted(set(names)|set(self.declarations[guard]["axes"]))
        count=0; ok=True
        for c in coords(self.axes,names):
            if guard:
                d=self.declarations[guard]; g=self.data[guard][tuple(c[a] for a in d["axes"])]
                need(g.type==() and g.value in (0,1),"INVALID_GUARD")
                if not g.value: continue
            a,b=self.expr(l,c),self.expr(r,c)
            need(a.type==b.type,"PHYSICAL_TYPE_MISMATCH")
            need(op in ("eq","ge","le"),"COMPARISON")
            ok &= {"eq":a.value==b.value,"ge":a.value>=b.value,"le":a.value<=b.value}[op]
            count+=1
        need(count>0,"VACUOUS_SUPPORT")
        return ok

def decl(axes,unit="1",role="OBSERVABLE",basis="",dtype="float"):
    return dict(axes=axes,unit=unit,role=role,basis=basis,dtype=dtype)

def input_series(axes, declarations, values):
    return {k:dict(zip((tuple(c[a] for a in d["axes"]) for c in coords(axes,d["axes"])),values[k],strict=True)) for k,d in declarations.items()}

def named(s):
    need(isinstance(s,str) and bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z_0-9]*",s)),"INVALID_IDENTIFIER")
    return s

def compile_profile(method,study,snapshot):
    """Narrow R1 profile AST -> native mathspec expression syntax.
    Not an alternative authority or CSNF validator.
    """
    ed=snapshot["engine_data"]; axmap={a:named(a.split(":")[-1]) for a in ed["axes"]}
    need(len(set(axmap.values()))==len(axmap),"AXIS_ALIAS")
    axes={axmap[a]:v["ids"] for a,v in ed["axes"].items()}
    ds={}; data={}
    need(set(method["inputs"])==set(ed["series"]),"INPUT_SET")
    for n,s in method["inputs"].items():
        named(n); z=ed["series"][n]
        need(all(z[k]==s[k] for k in ("axes","unit","basis","role")),"INPUT_SIGNATURE")
        ds[n]=decl([axmap[a] for a in s["axes"]],s["unit"],"INPUT",s["basis"])
        rows=z["rows"]; table={tuple(row["key"]):row["value"] for row in rows}
        need(len(table)==len(rows),"DUPLICATE_COORDINATE")
        data[n]=table
    need(set(study["parameters"])==set(method["parameters"]),"PARAMETER_SET")
    for n,d in method["parameters"].items():
        named(n); v=finite(study["parameters"][n])
        need(finite(d["min"])<=v<=finite(d["max"]),"PARAMETER_RANGE")
        ds[n]=decl([],d["unit"],"METHOD_PARAMETER"); data[n]={():str(v)}
    pairs={x["id"]:x for x in ed["pairs"]}
    need(len(pairs)==len(ed["pairs"]),"PAIR_ID")
    def e(n):
        op=n["op"]
        if op=="literal":
            need(n["unit"]=="1","LITERAL_TYPE")
            v=finite(n["value"]); return "("+str(v.numerator)+" / "+str(v.denominator)+")"
        if op in ("param","input","rule"):
            i=named(n["id"]); need(i in (method["rules"] if op=="rule" else method["parameters"] if op=="param" else method["inputs"]),"UNBOUND_REFERENCE")
            return i
        if op=="select_case":
            p=pairs[n["pair"]]; need(n["side"] in ("reference","alternative"),"PAIR_SIDE")
            need(p["reference_snapshot"]==p["alternative_snapshot"],"EXOGENEITY")
            return named(p[n["side"]])
        if op in ("add","sub","mul","div","pow"):
            token={"add":"+","sub":"-","mul":"*","div":"/","pow":"**"}[op]
            return "("+e(n["lhs"])+" "+token+" "+e(n["rhs"])+")"
        if op=="weighted_sum":
            w=named(n["weight"]); need(w in ds,"WEIGHT_REFERENCE")
            return "sum(("+e(n["expr"])+") * "+w+", over="+axmap[n["axis"]]+")"
        raise Rejected("PROFILE_OPERATOR_NOT_ALLOWED")
    expressions={named(n):e(r["expr"]) for n,r in method["rules"].items()}
    c=Consumer(axes,ds,data,expressions)
    for n,r in method["rules"].items():
        node=c.program.expressions[n].expression
        need(set(node.dims)=={axmap[a] for a in r["axes"]},"RULE_AXES")
        need(all(q.type==type_of(r["unit"],r["basis"]) for q in c.table(n).values()),"RULE_TYPE")
    return c
