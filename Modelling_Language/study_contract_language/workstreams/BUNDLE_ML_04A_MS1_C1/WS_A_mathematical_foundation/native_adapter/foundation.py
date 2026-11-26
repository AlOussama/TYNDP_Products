"""C1 bounded public-API foundation. Research only; no solver or Bool3 engine."""
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json, re, sys
import mathspec as ms
import mathspec.program as mp
from mathspec.errors import LanguageError
ROOT=Path(__file__).resolve().parents[1]
R1=ROOT.parents[1]/"BUNDLE_ML_04A_R1"
sys.path.insert(0,str(R1))
from units_r1 import Dimension
VERSION="c1-math-interface-0.1"
UPSTREAM="5f1464c334c1012cdee2947d4d55b4d1d6bef40a"
REGISTRY=json.loads((ROOT/"physical_type_registry.json").read_text())
ROLES={"INPUT","OBSERVABLE","METHOD_PARAMETER","DERIVED_EXPRESSION","EXTERNAL_WITNESS"}
class Reject(ValueError): pass
def need(x,code):
    if not x: raise Reject(code)
def fields(d,keys,code="FIELDS"):
    need(type(d) is dict and set(d)==set(keys),code)
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def digest(x): return sha256(canon(x).encode()).hexdigest()
def pairs(p):
    d={}
    for k,v in p:
        need(k not in d,"DUPLICATE_KEY")
        d[k]=v
    return d
def parse(source):
    need(type(source) is str,"SOURCE_REQUIRED")
    def fail(x): raise Reject("NONFINITE")
    try: return json.loads(source,object_pairs_hook=pairs,parse_constant=fail)
    except json.JSONDecodeError as e: raise Reject("SOURCE_JSON") from e
def identifier(s):
    return type(s) is str and bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",s))
def qualified(s):
    return type(s) is str and bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.:-]*:[A-Za-z0-9_.:-]+",s))
def exact(x):
    need(type(x) in (str,int),"UNKNOWN_OR_NONEXACT_VALUE")
    need(type(x) is int or bool(re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]+)?|[0-9]+/[0-9]+)",x)),"UNKNOWN_OR_NONEXACT_VALUE")
    try: return Fraction(x)
    except (ValueError,ZeroDivisionError) as e: raise Reject("NUMERIC_DOMAIN") from e
def check_literal_tokens(s):
    # Lexical admission only: native mathspec parses expressions; no parallel grammar.
    need(type(s) is str,"CONSTRUCT_NOT_ALLOWED")
    need(not re.search(r"(?<![A-Za-z_0-9])[0-9]+[A-Za-z_]",s),"NUMERIC_LITERAL")
    pos=0
    for m in re.finditer(r"\s+|[A-Za-z_][A-Za-z0-9_]*|[0-9]+|[()+*/=,-]",s):
        need(m.start()==pos,"NUMERIC_LITERAL_OR_TOKEN")
        t=m.group()
        if t.isdigit(): need(len(t)<=16 and int(t)<=2**53-1 and (len(t)==1 or t[0]!="0"),"NUMERIC_PRECISION")
        pos=m.end()
    need(pos==len(s) and bool(s.strip()),"NUMERIC_LITERAL_OR_TOKEN")
@dataclass(frozen=True)
class Q:
    physical:Dimension
    atoms:Dimension
    convention:tuple
    def combine(self,b,sign=1):
        a1,b1=self.convention,b.convention
        need(a1==b1 or a1==("NONE","NONE","NONE") or b1==("NONE","NONE","NONE"),"CONVENTION_MISMATCH")
        return Q(self.physical.combine(b.physical,sign),self.atoms.combine(b.atoms,sign),b1 if a1==("NONE","NONE","NONE") else a1)
    def power(self,n):
        need(self.convention==("NONE","NONE","NONE") or n==1,"POWER_CONVENTION")
        return Q(Dimension.make({k:v*n for k,v in self.physical.exponents}),Dimension.make({k:v*n for k,v in self.atoms.exponents}),self.convention)
def quantity(d):
    fields(d,("unit","carrier","basis","sign","direction","time_basis"),"QUANTITY_FIELDS")
    u=d["unit"]; need(u in REGISTRY["units"],"UNIT")
    z=REGISTRY["units"][u]; atoms=dict(z["atoms"])
    if u.startswith("EUR"):
        need(d["carrier"]=="currency" and type(d["basis"]) is str and re.fullmatch(r"EUR:(real|nominal):[0-9]{4}",d["basis"]),"PRICE_BASIS")
        atoms[d["basis"]]=atoms.pop("EUR")
    elif "hydrogen_LHV_MWh" in atoms or "hydrogen_HHV_MWh" in atoms:
        b="HHV/LHV" if "hydrogen_LHV_MWh" in atoms and "hydrogen_HHV_MWh" in atoms else "LHV" if "hydrogen_LHV_MWh" in atoms else "HHV"
        need(d["basis"]==b,"HEATING_VALUE_BASIS")
        need(d["carrier"]==("conversion" if u in ("LHV_ratio","HHV_ratio","HHV_per_LHV","MWh_H2_LHV/kg","MWh_H2_HHV/kg") else "hydrogen"),"CARRIER")
    else:
        c="electricity" if "electricity_MWh" in atoms else "heat" if "heat_MWh" in atoms else "hydrogen" if "hydrogen_kg" in atoms else "none"
        need(d["carrier"]==c and d["basis"]=="NONE","CARRIER_OR_BASIS")
    need(d["sign"] in ("NONE","INJECTION","CONSUMPTION","BIDIRECTIONAL") and d["direction"] in ("NONE","IN","OUT","BIDIRECTIONAL"),"CONVENTION")
    need(d["time_basis"]=="NONE" or qualified(d["time_basis"]),"TIME_BASIS")
    return Q(Dimension.make(z["physical"]),Dimension.make(atoms),(d["sign"],d["direction"],d["time_basis"]))
DIMLESS=quantity(dict(unit="1",carrier="none",basis="NONE",sign="NONE",direction="NONE",time_basis="NONE"))
def constant(node):
    if type(node) is mp.Constant:
        v=node.value
        need(float(v).is_integer() and abs(v)<=2**53-1,"NUMERIC_PRECISION")
        return int(v)
    if type(node) is mp.Negate:
        v=constant(node.operand)
        return None if v is None else -v
    return None
def qdesc(q): return {"physical":dict(q.physical.exponents),"atoms":dict(q.atoms.exponents),"convention":list(q.convention)}
def validate(source):
    d=parse(source)
    fields(d,("version","native","domains","symbols","predicates","scope","method","audit"),"ENVELOPE_FIELDS")
    need(d["version"]==VERSION,"LANGUAGE_VERSION")
    fields(d["audit"],("source_id","source_ref","evidence_id"),"AUDIT_REQUIRED")
    need(all(type(v) is str and v for v in d["audit"].values()),"AUDIT_REQUIRED")
    need(type(d["method"]) is str and d["method"],"METHOD_ID")
    n=d["native"]; fields(n,("version","dimensions","parameters","expressions"),"NATIVE_SECTION")
    need(type(n["version"]) is int and n["version"]==0,"NATIVE_VERSION")
    need(all(type(n[k]) is dict for k in ("dimensions","parameters","expressions")),"NATIVE_SECTION")
    need(type(d["domains"]) is dict and set(d["domains"])==set(n["dimensions"]),"DOMAIN_BINDING")
    ids=[]
    for name,z in d["domains"].items():
        need(identifier(name),"NATIVE_NAME")
        fields(z,("id","ordered","labels","dtype"),"DOMAIN_FIELDS")
        need(qualified(z["id"]) and type(z["ordered"]) is bool,"DOMAIN_ID")
        need(z["dtype"] in ("int","str"),"DOMAIN_DTYPE")
        a=z["labels"];need(type(a) is list and bool(a) and all(type(v)==(int if z["dtype"]=="int" else str) for v in a) and len(a)==len(set(a)),"DOMAIN_SUPPORT")
        need(n["dimensions"][name]=={"dtype":z["dtype"],"ordered":z["ordered"]},"DOMAIN_NATIVE_MISMATCH")
        ids.append(z["id"])
    fields(d["scope"],("id","binders"),"SCOPE_FIELDS")
    need(qualified(d["scope"]["id"]),"SCOPE_ID")
    bind=d["scope"]["binders"]
    need(type(bind) is list and len(bind)==len(set(bind)) and set(bind)==set(d["domains"]),"SCOPE_BINDERS")
    sy=d["symbols"]
    need(type(sy) is dict and set(sy)==set(n["parameters"])|set(n["expressions"]) and not set(n["parameters"])&set(n["expressions"]),"SYMBOL_BINDING")
    qs={}
    for name,z in sy.items():
        need(identifier(name),"NATIVE_NAME")
        fields(z,("id","role","axes","dtype","quantity","nonzero"),"SYMBOL_FIELDS")
        need(qualified(z["id"]),"SYMBOL_ID")
        ids.append(z["id"])
        need(z["role"] in ROLES and (z["role"]=="DERIVED_EXPRESSION")== (name in n["expressions"]),"SYMBOL_ROLE")
        a=z["axes"];need(type(a) is list and len(a)==len(set(a)) and set(a)<=set(d["domains"]),"INDEX_BINDING")
        need(z["dtype"] in ("float","int","bool") and type(z["nonzero"]) is bool,"SYMBOL_DTYPE")
        qs[name]=quantity(z["quantity"])
        if z["dtype"]=="bool":need(qs[name]==DIMLESS and not z["nonzero"],"BOOL_QUANTITY")
        if name in n["parameters"]:
            need(n["parameters"][name]=={"dims":a,"dtype":z["dtype"],"missing":"refused"},"PARAMETER_SIGNATURE_OR_DEFAULT")
        else:
            need(z["dtype"]=="float" and not z["nonzero"],"DERIVED_DTYPE_DEFERRED")
            check_literal_tokens(n["expressions"][name])
    need(len(set(ids+[d["scope"]["id"]]))==len(ids)+1,"AMBIGUOUS_ALIAS")
    try: spec=ms.to_spec(n)
    except LanguageError as e: raise Reject("NATIVE_REJECT:"+str(e)) from e
    def infer(node):
        t=type(node)
        if t is mp.Constant: constant(node);return DIMLESS
        if t is mp.ParameterReference:
            need(node.name in n["parameters"] and sy[node.name]["dtype"]!="bool","NUMERIC_ROLE")
            return qs[node.name]
        if t is mp.ExpressionReference:
            need(node.name in n["expressions"],"UNBOUND_REFERENCE")
            q=infer(node.body);need(q==qs[node.name],"EXPRESSION_TYPE");return q
        if t is mp.Negate:return infer(node.operand)
        if t is mp.Add:
            a,b=infer(node.left),infer(node.right);need(a==b,"PHYSICAL_TYPE_MISMATCH");return a
        if t is mp.Multiply:return infer(node.left).combine(infer(node.right))
        if t is mp.Divide:
            a,b=infer(node.numerator),infer(node.divisor)
            v=constant(node.divisor)
            need((v is not None and v!=0) or (type(node.divisor) is mp.ParameterReference and sy[node.divisor.name]["nonzero"]),"DIVISOR_NONZERO_REQUIRED")
            return a.combine(b,-1)
        if t is mp.Power:
            a,b=infer(node.base),infer(node.exponent);v=constant(node.exponent)
            need(b==DIMLESS and v is not None and 1<=v<=8,"POWER_DOMAIN")
            return a.power(v)
        if t is mp.Sum:
            need(all(a.column is None and a.dimension in d["domains"] for a in node.over),"RELATION_SUM_DEFERRED")
            return infer(node.operand)
        raise Reject("NODE_NOT_ALLOWED:"+t.__name__)
    def check_program(p):
        need(not p.variables and not p.constraints and not p.assumptions,"SOLVER_OR_CONDITION_CONSTRUCT")
        need(set(p.expressions)==set(n["expressions"]) and set(p.parameters)==set(n["parameters"]),"PROGRAM_BINDING")
        for name in sorted(p.expressions):
            e=p.expressions[name].expression
            need(infer(e)==qs[name],"EXPRESSION_TYPE:"+name)
            need(set(e.dims)==set(sy[name]["axes"]),"INDEX_TYPE:"+name)
    check_program(spec.program)
    # All declared predicates, including inactive guards, checked before data.
    need(type(d["predicates"]) is dict,"PREDICATES")
    for name,p in d["predicates"].items():
        need(qualified(name) and name not in ids,"PREDICATE_ID")
        fields(p,("lhs","rhs","cmp","guard"),"PREDICATE_FIELDS")
        a,b=p["lhs"],p["rhs"]
        need(a in sy and b in sy and sy[a]["dtype"]!="bool" and sy[b]["dtype"]!="bool","PREDICATE_REFERENCE")
        need(p["cmp"] in ("eq","le","ge","lt","gt") and qs[a]==qs[b],"COMPARISON_TYPE")
        g=p["guard"]
        need(type(g) is bool or (type(g) is str and g in n["parameters"] and sy[g]["dtype"]=="bool"),"GUARD_TYPE")
    native=spec.to_yaml(canonical=True)
    again=ms.to_spec(native);check_program(again.program)
    need(again.to_yaml(canonical=True)==native,"CANONICAL_ROUNDTRIP")
    # Original source and audit identities remain separately verifiable.
    context={k:d[k] for k in ("version","domains","symbols","predicates","scope","method")}
    sem={"upstream":UPSTREAM,"registry":digest(REGISTRY),"native":native,"context":context}
    source_id=sha256(source.encode()).hexdigest()
    leaf={"schema":VERSION,"upstream":UPSTREAM,"native_canonical":native,"source":source,"source_digest":source_id,
          "native_identity":digest({"upstream":UPSTREAM,"canonical":native}),"semantic_identity":digest(sem),
          "audit_identity":digest({"semantic":digest(sem),"source":source_id,"audit":d["audit"]}),
          "audit":d["audit"],"scope":d["scope"],"method":d["method"],"types":{k:qdesc(v) for k,v in qs.items()}}
    return leaf
def reimport(leaf):
    need(type(leaf) is dict and "source" in leaf,"LEAF_SCHEMA")
    rebuilt=validate(leaf["source"])
    need(rebuilt==leaf,"LEAF_TAMPER_OR_AUDIT_LOSS")
    return rebuilt
def bind_data(leaf,data):
    leaf=reimport(leaf);d=parse(leaf["source"]);sy=d["symbols"]
    need(type(data) is dict and set(data)==set(d["native"]["parameters"]),"DATA_BINDINGS")
    for name,rows in data.items():
        z=sy[name];axes=z["axes"];want=set(product(*(d["domains"][a]["labels"] for a in axes)))
        need(type(rows) is list,"DATA_ROWS");got=set()
        for r in rows:
            fields(r,("key","value"),"ROW_FIELDS")
            need(type(r["key"]) is list,"ROW_KEY");k=tuple(r["key"])
            need(k in want and k not in got,"DATA_COORDINATE");got.add(k)
            if z["dtype"]=="bool":need(type(r["value"]) is bool,"UNKNOWN_GUARD")
            else:
                x=exact(r["value"])
                if z["dtype"]=="int":need(x.denominator==1,"INTEGER_DOMAIN")
                if z["nonzero"]:need(x!=0,"DIVISOR_NONZERO_REQUIRED")
        need(got==want,"DATA_SUPPORT")
    return {"stage":"FINITE_DATA_DOMAIN_ONLY","leaf_identity":leaf["semantic_identity"],"data_identity":digest(data)}
def m3(leaf):return {"architecture":"M3","mathematical_leaf":reimport(leaf),"stage":"MATHEMATICAL_BOUNDARY_ONLY"}
def m2_measure_predicate(leaf,name,binder_names):
    """Restricted actual R1 measure/compare AST mapping, not a generic M2 implementation."""
    d=parse(reimport(leaf)["source"]);p=d["predicates"][name]
    need(p["guard"] is True,"M2_GUARD_DEFERRED")
    def measure(n):
        need(n in d["native"]["parameters"] and d["symbols"][n]["role"]=="OBSERVABLE","M2_EXPRESSION_UNSUPPORTED")
        z=d["symbols"][n]
        need(all(a in binder_names for a in z["axes"]),"M2_BINDER")
        return {"op":"measure","ref":z["id"],"indices":[{"op":"var","name":binder_names[a]} for a in z["axes"]]}
    return {"op":"compare","cmp":p["cmp"],"lhs":measure(p["lhs"]),"rhs":measure(p["rhs"])}
