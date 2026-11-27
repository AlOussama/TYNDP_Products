"""Research-only canonical-first mathematical boundary, v0.2.
Public native Spec/Program is the sole mathematical representation.
No solver, data evaluator, Bool3 engine, or legacy AST translation.
"""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import re,sys
import yaml
import mathspec as ms
import mathspec.program as mp
from mathspec.errors import LanguageError
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"WS_A_mathematical_foundation/native_adapter"))
import foundation as c1
from foundation import Reject,need,fields,digest,canon,qualified,exact,quantity,DIMLESS,constant
VERSION="canonical-first-research-0.2"
CONVERSION_UNITS={"MWh_H2_LHV/kg","MWh_H2_HHV/kg","LHV_ratio","HHV_ratio","HHV_per_LHV"}
NEUTRAL=("NONE","NONE","NONE")
SECTIONS={"version","description","dimensions","relations","parameters","expressions","conditions","assumptions"}

def text_hash(s):return sha256(s.encode("utf-8")).hexdigest()
def sha(s):return type(s) is str and bool(re.fullmatch(r"[a-f0-9]{64}",s))
def keys(d,required,optional=(),code="FIELDS"):
    need(type(d) is dict and set(required)<=set(d)<=set(required)|set(optional),code)
def string(s):return type(s) is str and bool(s)
def ids(xs):
    need(type(xs) is list and all(type(x) is str for x in xs) and len(xs)==len(set(xs)),"UNIQUE_NAMES")
    return set(xs)

class StrictLoader(yaml.SafeLoader):pass
def mapping(loader,node):
    out={}
    for a,b in node.value:
        k=loader.construct_object(a)
        need(type(k) is str and k not in out,"YAML_DUPLICATE_OR_NONSTRING_KEY")
        out[k]=loader.construct_object(b)
    return out
StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
def source_map(s):
    need(type(s) is str,"SOURCE_REQUIRED")
    try:
        need(not any(isinstance(t,(yaml.tokens.AliasToken,yaml.tokens.AnchorToken,yaml.tokens.TagToken)) for t in yaml.scan(s)),"YAML_ALIAS_OR_TAG")
        doc=yaml.load(s,Loader=StrictLoader)
    except yaml.YAMLError as e:raise Reject("SOURCE_YAML:"+str(e)) from e
    need(type(doc) is dict,"SOURCE_MAPPING")
    return doc
def lex(s,condition=False):
    """Exact-number admission, not a second expression grammar.
    Refuse constant Bool literals before native Mask folding can discard branches.
    Only quoted wrap is admitted; label comparisons use separately typed data.
    """
    if type(s) is int:s=str(s)
    need(type(s) is str and bool(s.strip()),"EXPRESSION_SOURCE")
    need(not re.search(r"(?<![A-Za-z_0-9])[0-9]+[A-Za-z_]",s),"NUMERIC_LITERAL_ADJACENCY")
    pos=0
    for m in re.finditer(r"\s+|'wrap'|\"wrap\"|[A-Za-z_][A-Za-z_0-9]*|[0-9]+|[()\[\]+*/=,<>!\-]",s):
        need(m.start()==pos,"NUMERIC_OR_TOKEN")
        t=m.group()
        if t.isdigit():
            need(len(t)<=16 and int(t)<=2**53-1 and (len(t)==1 or not t.startswith("0")),"NUMERIC_PRECISION")
        else:
            need(t.lower() not in ("inf","nan","infinity"),"NONFINITE_LITERAL")
            if condition:need(t.lower() not in ("true","false"),"FOLDED_CONDITION_LITERAL")
        pos=m.end()
    need(pos==len(s),"NUMERIC_OR_TOKEN")
def preflight(doc):
    keys(doc,(),SECTIONS,"NATIVE_SECTION")
    need(doc.get("version",0)==0 and type(doc.get("version",0)) is int,"NATIVE_VERSION")
    for section in ("dimensions","relations","parameters","expressions","conditions","assumptions"):
        need(type(doc.get(section,{})) is dict,"SECTION_MAPPING")
        for n,e in doc.get(section,{}).items():
            need(c1.identifier(n),"NATIVE_NAME")
            if section=="dimensions":
                keys(e,(),("dtype","ordered","one_of","description"),"DIMENSION_FIELDS")
            elif section=="relations":
                keys(e,("key",),("values","missing","description"),"RELATION_FIELDS")
                need(e.get("missing","refused")=="refused","RELATION_MISSING")
            elif section=="parameters":
                keys(e,("dims",),("dtype","missing","description"),"PARAMETER_FIELDS")
                need(e.get("missing","refused")=="refused","MISSING_POLICY")
            elif section=="expressions":
                if type(e) is str or type(e) is int:lex(e)
                elif type(e) is dict:
                    if "cases" in e:
                        keys(e,("dims","cases","otherwise"),("description",),"CASE_FIELDS")
                        need(type(e["cases"]) is dict and bool(e["cases"]),"CASE_REGIONS")
                        for region in e["cases"].values():
                            fields(region,("when","expression"),"CASE_REGION_FIELDS")
                            lex(region["when"],True);lex(region["expression"])
                        lex(e["otherwise"])
                    else:
                        keys(e,("expression",),("dims","description"),"EXPRESSION_FIELDS");lex(e["expression"])
                else:raise Reject("EXPRESSION_SOURCE")
            elif section=="conditions":
                if type(e) is dict:keys(e,("condition",),("description",),"CONDITION_FIELDS");e=e["condition"]
                lex(e,True)
            elif section=="assumptions":
                if type(e) is dict:
                    keys(e,("holds",),("where","description"),"ASSUMPTION_FIELDS")
                    lex(e["holds"],True)
                    if "where" in e:lex(e["where"],True)
                else:lex(e,True)
def native(s):
    doc=source_map(s);preflight(doc)
    try:return ms.to_spec(doc)
    except LanguageError as e:raise Reject("NATIVE_REJECT:"+str(e)) from e
def alignment(a,b):
    a,b=set(a),set(b)
    need(a==b or not a or not b,"IMPLICIT_CROSS_ALIGNMENT")
    return a|b
def as_signature(name,entry,z,q):
    return {"native_name":name,"symbol_id":z["id"],"role":z["role"],"axes":list(entry.dims),
            "dtype":entry.dtype if isinstance(entry,mp.Parameter) else "rational",
            "quantity":z["quantity"],"algebra":c1.qdesc(q),"domain_rule":z["domain_rule"]}

class Checked:
    def __init__(self,spec,c):
        self.p=spec.program;self.c=c;self.q={};self.sig={};self.groups=set();self.used_time=set();self.used_conversions=set()
        p=self.p
        fields(c,("domains","relations","symbols","predicates","scope","temporal","conversions","method","study","audit"),"CONTEXT_FIELDS")
        need(not spec.given and not spec.macros and not p.variables and not p.constraints and not p.sos and not p.piecewise and p.objective is None,"SOLVER_OR_COMPOSITION")
        for k in ("domains","relations","symbols","predicates","temporal","conversions"):need(type(c[k]) is dict,"CONTEXT_MAP")
        allids=[]
        def claim(s):
            need(qualified(s) and s not in allids,"AMBIGUOUS_ID");allids.append(s)
        need(set(c["domains"])==set(p.dimensions),"DOMAIN_BINDING")
        for n,d in p.dimensions.items():
            z=c["domains"][n];fields(z,("id","labels"),"DOMAIN_FIELDS");claim(z["id"])
            labels=z["labels"];need(d.dtype in ("int","str"),"DOMAIN_DTYPE")
            kind=int if d.dtype=="int" else str
            need(type(labels) is list and bool(labels) and all(type(x) is kind for x in labels) and len(labels)==len(set(labels)),"DOMAIN_LABELS")
            if d.one_of is not None:need(set(labels)<=set(d.one_of),"DOMAIN_ALLOWED_LABELS")
        fields(c["scope"],("id","binders","alignment"),"SCOPE_FIELDS");claim(c["scope"]["id"])
        need(ids(c["scope"]["binders"])==set(p.dimensions) and c["scope"]["alignment"]=="SAME_OR_SCALAR","SCOPE_ALIGNMENT")
        need(set(c["relations"])==set(p.relations),"RELATION_BINDING")
        for n,r in p.relations.items():
            z=c["relations"][n];fields(z,("id","source_ref"),"RELATION_CONTEXT");claim(z["id"])
            need(string(z["source_ref"]) and r.missing=="refused","RELATION_POLICY")
            need(len(set(r.dim(k) for k in r.key))==len(r.key),"REPEATED_KEY_DIMENSION")
        need(set(c["symbols"])==set(p.parameters)|set(p.expressions),"SYMBOL_BINDING")
        for n,z in c["symbols"].items():
            fields(z,("id","role","quantity","domain_rule"),"SYMBOL_FIELDS");claim(z["id"])
            entry=p.parameters[n] if n in p.parameters else p.expressions[n]
            need(z["role"] in c1.ROLES and (z["role"]=="DERIVED_EXPRESSION")== (n in p.expressions),"SYMBOL_ROLE")
            q=quantity(z["quantity"]);self.q[n]=q
            need(z["domain_rule"] in ("ANY_EXACT","NONZERO","POSITIVE","NONNEGATIVE"),"DOMAIN_RULE")
            if n in p.parameters:
                need(entry.dtype in ("float","int","bool") and entry.missing=="refused" and entry.where is None,"PARAMETER_PROFILE")
                if entry.dtype=="bool":need(q==DIMLESS and z["domain_rule"]=="ANY_EXACT","BOOL_QUANTITY")
            else:need(z["domain_rule"]=="ANY_EXACT","DERIVED_DOMAIN_RULE")
            self.sig[n]=as_signature(n,entry,z,q)
            self.sig[n]["domain_ids"]=[c["domains"][a]["id"] for a in entry.dims]
        need(set(c["conversions"])=={n for n,z in c["symbols"].items() if z["quantity"]["unit"] in CONVERSION_UNITS},"CONVERSION_BINDING")
        for n,z in c["conversions"].items():
            fields(z,("id","version","source_ref","source_sha256","authority"),"CONVERSION_FIELDS");claim(z["id"])
            need(string(z["version"]) and string(z["source_ref"]) and sha(z["source_sha256"]) and z["authority"]=="RESEARCH_ASSUMPTION","CONVERSION_PROVENANCE")
            need(n in p.parameters and c["symbols"][n]["role"]=="METHOD_PARAMETER" and c["symbols"][n]["domain_rule"]=="POSITIVE","CONVERSION_ROLE")
        for n,z in c["temporal"].items():
            fields(z,("id","chronology_ref","shift_edge","window_edge"),"TEMPORAL_FIELDS");claim(z["id"])
            need(n in p.dimensions and p.dimensions[n].ordered and string(z["chronology_ref"]),"TEMPORAL_ORDER")
            need(z["shift_edge"] in ("ZERO","WRAP","FORBIDDEN") and z["window_edge"] in ("TRUNCATE","WRAP","FORBIDDEN"),"TEMPORAL_POLICY")
        # Entire public typed Program, including unused declarations and cases.
        for n,e in p.expressions.items():
            need(self.expr(e.expression)==self.q[n],"EXPRESSION_TYPE:"+n)
        for n,e in p.conditions.items():self.mask(e.condition)
        for n,e in p.assumptions.items():
            self.mask(e.holds)
            if e.where is not None:self.mask(e.where);alignment(e.holds.dims,e.where.dims)
            names=set(e.holds.names_read)|(set(e.where.names_read) if e.where is not None else set())
            need(all(x in c["relations"] or c["symbols"][x]["role"] in ("INPUT","METHOD_PARAMETER") for x in names),"ASSUMPTION_IS_NOT_GUARANTEE")
        need(set(c["temporal"])==self.used_time,"TEMPORAL_POLICY_SCOPE")
        # Native conditions are the sole mathematical predicate expressions.
        need(set(c["predicates"])==set(p.conditions)|set(p.assumptions),"PREDICATE_BINDING")
        self.predicates={}
        for n,z in c["predicates"].items():
            fields(z,("id","role","axes"),"PREDICATE_FIELDS");claim(z["id"])
            if n in p.conditions:
                need(z["role"] in ("PREDICATE","GUARD"),"CONDITION_ROLE");dims=set(p.conditions[n].dims)
            else:
                need(z["role"]=="DATA_ASSUMPTION","ASSUMPTION_ROLE")
                a=p.assumptions[n];dims=set(a.holds.dims)|(set(a.where.dims) if a.where else set())
            ordered=[a for a in c["scope"]["binders"] if a in dims]
            need(z["axes"]==ordered,"PREDICATE_SCOPE")
            self.predicates[n]={"id":z["id"],"role":z["role"],"axes":[c["domains"][a]["id"] for a in ordered],"truth_contract":"COMPLETE_BINARY_INPUTS_ONLY"}
        # Method signature is separate from native maths and from study binding.
        m=c["method"];fields(m,("id","version","inputs","parameters","outputs"),"METHOD_FIELDS");claim(m["id"]);need(string(m["version"]),"METHOD_VERSION")
        mi,mpa,mo=(ids(m[k]) for k in ("inputs","parameters","outputs"))
        need(mi=={n for n,z in c["symbols"].items() if z["role"] in ("INPUT","OBSERVABLE","EXTERNAL_WITNESS")} and mpa=={n for n,z in c["symbols"].items() if z["role"]=="METHOD_PARAMETER"} and mo==set(p.expressions),"METHOD_SIGNATURE")
        self.method_signature={"id":m["id"],"version":m["version"],**{k:[self.sig[n] for n in sorted(m[k])] for k in ("inputs","parameters","outputs")}}
        self.method_id=digest(self.method_signature)
        st=c["study"];fields(st,("id","version","method_ref","data_id","data_version","owner"),"STUDY_FIELDS");claim(st["id"])
        need(string(st["version"]) and st["method_ref"]==digest(m) and qualified(st["data_id"]) and string(st["data_version"]) and st["owner"]=="OWNER_TBD","STUDY_BINDING")
        self.study_id=digest({"study":st,"typed_method":self.method_id})
        a=c["audit"];fields(a,("source_id","source_ref","evidence_id","authority"),"AUDIT_FIELDS")
        need(qualified(a["source_id"]) and string(a["source_ref"]) and qualified(a["evidence_id"]) and a["authority"]=="RESEARCH_ASSUMPTION","AUDIT_AUTHORITY")
    def time(self,n):
        need(n in self.c["temporal"],"TEMPORAL_POLICY_REQUIRED")
        self.used_time.add(n);return self.c["temporal"][n]
    def join(self,columns):
        need(columns.name in self.p.relations,"RELATION_REF")
        need(len(set(columns.joined_dims))==len(columns.joined_dims) and len(set(columns.grouped_dims))==len(columns.grouped_dims),"JOIN_ROLE_COLLISION")
        self.groups.add((columns.name,tuple(columns.grouped)))
    def combine(self,a,b,sign):
        # Avoid inventing sign/direction composition; admissible neutral
        # factor or denominator only. Conservatively defer other conventions.
        need(a.convention==NEUTRAL or b.convention==NEUTRAL,"COMPOUND_CONVENTION_DEFERRED")
        need(sign==1 or b.convention==NEUTRAL,"DENOMINATOR_CONVENTION_DEFERRED")
        return a.combine(b,sign)
    def expr(self,e,opened=False):
        t=type(e)
        if t is mp.Constant:constant(e);return DIMLESS
        if t is mp.ParameterReference:
            need(e.name in self.p.parameters and self.p.parameters[e.name].dtype!="bool","NUMERIC_ROLE")
            if e.name in self.c["conversions"]:self.used_conversions.add(e.name)
            return self.q[e.name]
        if t is mp.ExpressionReference:
            q=self.expr(e.body);need(q==self.q[e.name],"EXPRESSION_REFERENCE_TYPE");return q
        if t is mp.Negate:return self.expr(e.operand)
        if t is mp.Add:
            a,b=self.expr(e.left),self.expr(e.right);need(a==b,"PHYSICAL_TYPE_MISMATCH");return a
        if t is mp.Multiply:return self.combine(self.expr(e.left),self.expr(e.right),1)
        if t is mp.Divide:
            a,b=self.expr(e.numerator),self.expr(e.divisor);v=constant(e.divisor)
            need((v is not None and v!=0) or (type(e.divisor) is mp.ParameterReference and self.c["symbols"][e.divisor.name]["domain_rule"] in ("NONZERO","POSITIVE")),"DIVISOR_NONZERO_REQUIRED")
            return self.combine(a,b,-1)
        if t is mp.Power:
            a,b=self.expr(e.base),self.expr(e.exponent);v=constant(e.exponent)
            need(b==DIMLESS and v is not None and 1<=v<=8,"POWER_DOMAIN")
            return a.power(v)
        if t is mp.Sum:
            if any(a.column is not None for a in e.over):
                need(type(e.operand) is mp.Join and set(e.over)==set(e.operand.columns.axes),"JOIN_AXIS_SCOPE")
                return self.expr(e.operand,True)
            return self.expr(e.operand)
        if t is mp.Join:
            need(e.columns.one_row_per_group or opened,"OPEN_JOIN")
            self.join(e.columns);return self.expr(e.operand)
        if t is mp.Translate:
            z=self.time(e.along)
            need(e.partition is None and type(e.offset) is int and e.offset>=0,"SHIFT_SCOPE")
            need((e.wrap and z["shift_edge"]=="WRAP") or (not e.wrap and e.fill==0 and z["shift_edge"]=="ZERO"),"SHIFT_EDGE")
            return self.expr(e.operand)
        if t is mp.WindowSum:
            z=self.time(e.along)
            need(e.partition is None and type(e.width) is int and 1<=e.width<=len(self.c["domains"][e.along]["labels"]),"WINDOW_SCOPE")
            need(z["window_edge"]==("WRAP" if e.wrap else "TRUNCATE"),"WINDOW_EDGE")
            return self.expr(e.operand)
        if t is mp.Cases:
            values=[]
            for r in e.regions:
                self.mask(r.when);values.append(self.expr(r.value))
            need(bool(values) and all(q==values[0] for q in values),"CASE_PHYSICAL_TYPE")
            return values[0]
        raise Reject("NODE_NOT_ALLOWED:"+t.__name__)
    def mask(self,mask):return self.cond(mask.root)
    def cond(self,e):
        t=type(e)
        if t is mp.BooleanLiteral:return set() # only synthetic native branch masks
        if t is mp.ConditionReference:return self.cond(e.body)
        if t is mp.Not:return self.cond(e.operand)
        if t in (mp.And,mp.Or):return alignment(self.cond(e.left),self.cond(e.right))
        if t is mp.ExpressionComparison:
            need(self.expr(e.left)==self.expr(e.right),"COMPARISON_TYPE")
            return alignment(e.left.dims,e.right.dims)
        if t is mp.ParameterComparison:
            need(self.q[e.name]==DIMLESS and type(e.value) in (int,float) and float(e.value).is_integer() and abs(e.value)<=2**53-1,"TYPED_LITERAL_REQUIRED")
            return set(e.dims)
        if t is mp.ParameterDefined:
            need(self.p.parameters[e.name].dtype=="bool","DEFINED_IS_NOT_TRUTH")
            return set(e.dims)
        if t is mp.DimensionPosition:
            need(e.partition is None,"PARTITION_DEFERRED");self.time(e.name);return {e.name}
        if t is mp.DimensionComparison:
            need(self.p.dimensions[e.name].dtype=="int" and type(e.value) in (int,float) and float(e.value).is_integer() and abs(e.value)<=2**53-1,"DIMENSION_COMPARISON_SCOPE")
            return {e.name}
        if t is mp.JoinedCondition:
            need(e.columns.one_row_per_group,"JOIN_CONDITION_CARDINALITY")
            self.join(e.columns);self.mask(e.operand);return set(e.dims)
        if t is mp.CountComparison:
            self.mask(e.condition);need(float(e.value).is_integer() and 0<=e.value<=2**53-1,"COUNT_LITERAL")
            return set(e.dims)
        # TranslatedCondition absent-at-edge, relation label comparisons,
        # sparse masks and other constructs have not been admitted.
        raise Reject("CONDITION_NOT_ALLOWED:"+t.__name__)
    def summary(self):
        return {"symbols":self.sig,"predicates":self.predicates,"method_signature":self.method_signature,
                "method_identity":self.method_id,"study_identity":self.study_id,
                "join_support":[[n,list(cols)] for n,cols in sorted(self.groups)],
                "temporal_domains":sorted(self.used_time)}
def admit(source,context,require_canonical=False):
    """Preflight authored source, then native load, then full public-Program walk.
    Both source and roundtrip Programs must satisfy the same restrictions.
    """
    spec=native(source);first=Checked(spec,context);text=spec.to_yaml(canonical=True)
    if require_canonical:need(source==text,"NOT_NATIVE_CANONICAL")
    again=native(text);second=Checked(again,context)
    need(again.to_yaml(canonical=True)==text and first.summary()==second.summary(),"CANONICAL_BOUNDARY_ROUNDTRIP")
    sctx=deepcopy({k:v for k,v in context.items() if k!="audit"})
    for n,z in sctx["domains"].items():
        if not spec.program.dimensions[n].ordered:z["labels"]=sorted(z["labels"])
    for k in ("inputs","parameters","outputs"):sctx["method"][k]=sorted(sctx["method"][k])
    # study method_ref names original profile bytes; preserve it deliberately.
    ni=digest({"upstream":c1.UPSTREAM,"canonical":text})
    sem=digest({"version":VERSION,"native":ni,"registry":digest(c1.REGISTRY),"context":sctx})
    origin={"kind":"CANONICAL_AS_SOURCE" if require_canonical else "AUTHOR_SOURCE_PRECHECKED","sha256":text_hash(source)}
    audit=digest({"semantic":sem,"source":origin,"context_as_received":context})
    return {"schema":VERSION,"upstream":c1.UPSTREAM,"native_canonical":text,"source":source,"context":deepcopy(context),
            "origin":origin,"native_identity":ni,"semantic_identity":sem,"audit_identity":audit,"interface":second.summary(),
            "stage":"STATIC_MATHEMATICAL_BOUNDARY_ONLY"}
def reimport(leaf):
    need(type(leaf) is dict and {"source","context","origin"}<=set(leaf),"LEAF_FIELDS")
    got=admit(leaf["source"],leaf["context"],leaf["origin"]["kind"]=="CANONICAL_AS_SOURCE")
    need(got==leaf,"LEAF_TAMPER");return got

def bind_data(leaf,data):
    leaf=reimport(leaf);c=leaf["context"];p=native(leaf["native_canonical"]).program
    fields(data,("id","version","parameters","relations"),"DATA_FIELDS")
    need(data["id"]==c["study"]["data_id"] and data["version"]==c["study"]["data_version"],"DATA_CONTEXT")
    need(type(data["parameters"]) is dict and set(data["parameters"])==set(p.parameters),"DATA_PARAMETERS")
    need(type(data["relations"]) is dict and set(data["relations"])==set(p.relations),"DATA_RELATIONS")
    norm={"id":data["id"],"version":data["version"],"parameters":{},"relations":{}}
    def domain(n):return c["domains"][n]["labels"]
    def coordinates(axes):return set(product(*(domain(n) for n in axes)))
    def check_coord(v,n):
        need(type(v) is (int if p.dimensions[n].dtype=="int" else str) and v in domain(n),"DATA_COORDINATE")
    for n,rows in data["parameters"].items():
        pp=p.parameters[n];want=coordinates(pp.dims);got={}
        need(type(rows) is list,"DATA_ROWS")
        for r in rows:
            fields(r,("key","value"),"DATA_ROW")
            need(type(r["key"]) is list and len(r["key"])==len(pp.dims),"DATA_KEY")
            for v,a in zip(r["key"],pp.dims):check_coord(v,a)
            k=tuple(r["key"]);need(k not in got,"DUPLICATE_COORDINATE")
            v=r["value"]
            if pp.dtype=="bool":need(type(v) is bool,"UNKNOWN_BOOL")
            else:
                v=exact(v);rule=c["symbols"][n]["domain_rule"]
                if pp.dtype=="int":need(v.denominator==1,"INTEGER_DOMAIN")
                need((rule=="ANY_EXACT") or (rule=="NONZERO" and v!=0) or (rule=="POSITIVE" and v>0) or (rule=="NONNEGATIVE" and v>=0),"DATA_NUMERIC_DOMAIN")
                v=str(v)
            got[k]=v
        need(set(got)==want,"INCOMPLETE_PARAMETER_SUPPORT")
        norm["parameters"][n]=[{"key":list(k),"value":got[k]} for k in sorted(got)]
    for n,rows in data["relations"].items():
        r=p.relations[n];need(type(rows) is list,"RELATION_ROWS")
        got={}
        for row in rows:
            fields(row,r.roles,"RELATION_ROW")
            for role,axis in r.columns:check_coord(row[role],axis)
            k=tuple(row[role] for role in r.key);need(k not in got,"RELATION_DUPLICATE_KEY");got[k]=row
        need(set(got)==coordinates([r.dim(k) for k in r.key]),"RELATION_KEY_COVERAGE")
        for rel,cols in leaf["interface"]["join_support"]:
            if rel==n:
                groups={tuple(row[k] for k in cols) for row in rows}
                need(groups==coordinates([r.dim(k) for k in cols]),"RELATION_GROUP_COVERAGE")
        norm["relations"][n]=[got[k] for k in sorted(got)]
    di=digest(norm)
    return {"schema":VERSION,"stage":"FINITE_INPUT_SUPPORT_ONLY","data_identity":di,"data_audit_identity":digest(data),
            "leaf_identity":leaf["semantic_identity"],"method_identity":leaf["interface"]["method_identity"],"study_identity":leaf["interface"]["study_identity"],
            "context_identity":digest({"leaf":leaf["semantic_identity"],"data":di,"study":leaf["interface"]["study_identity"]}),
            "owner":"OWNER_TBD","predicate_verdict":"NOT_EXECUTED","scientific_claim":"NONE"}
