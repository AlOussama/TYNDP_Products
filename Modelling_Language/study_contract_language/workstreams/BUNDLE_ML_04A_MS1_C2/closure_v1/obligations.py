"""Scoped external obligation semantics over qualified native binary predicates.
Outer logic carries no mathematical expressions. Finite evidence is not
universal behavioral proof or owner approval.
"""
from itertools import product
from closure import fields,need,qualified,digest,Reject
from interface import import_package,resolve_predicate,finite_consumer
from WS_A.contract import TRUTH,not3,fold3,ROLES
from closure_v1.metadata import index,refs,validate_package_domains

ASSUMPTIONS=("DATA_ASSUMPTION","TECHNICAL_ASSUMPTION","ENVIRONMENT_ASSUMPTION")
SERVICES=("SERVICE_GUARANTEE","CAPABILITY_GUARANTEE")
UNKNOWN_REASONS=("MISSING_DATA","MISSING_EVIDENCE","AUTHORITY_UNRESOLVED","UNSUPPORTED_EXECUTION")

class Bound:
    def __init__(self,package,tables,data):
        self.leaf=import_package(package);self.program=validate_package_domains(self.leaf,tables)
        self.tables=tables;self.package=package
        self.axes={z["id"]:n for n,z in self.leaf["context"]["domains"].items()}
        self.symbols={z["symbol_id"]:z for z in self.leaf["interface"]["symbols"].values()}
        self.consumer=finite_consumer(package,data) if data is not None else None
        self.data_identity=self.consumer.receipt["data_identity"] if self.consumer else None
    def resolve(self,ref,roles):
        p=resolve_predicate(self.package,ref);need(p["role"] in roles,"PREDICATE_ROLE")
        return p
    def at(self,ref,env):
        if self.consumer is None:return "UNKNOWN",["MISSING_DATA"]
        e={self.axes[k]:v for k,v in env.items() if k in self.axes}
        n=ref["native_name"]
        if ref["role"]=="DATA_ASSUMPTION":
            a=self.program.assumptions[n]
            if a.where is not None and not self.consumer.cond(a.where.root,e):return None,["ASSUMPTION_NOT_APPLICABLE"]
            v=self.consumer.cond(a.holds.root,e)
        else:v=self.consumer.cond(self.program.conditions[n].condition.root,e)
        need(type(v) is bool,"NONBINARY_NATIVE_PREDICATE")
        return ("TRUE" if v else "FALSE"),[]
    def guard_refs(self,g,scope):
        need(type(g) is dict,"GUARD_FIELDS")
        if "truth" in g:
            fields(g,("truth","reason"),"GUARD_FIELDS");v=g["truth"]
            need(v in TRUTH and (g["reason"] in UNKNOWN_REASONS if v=="UNKNOWN" else g["reason"] is None),"GUARD_REASON")
            return set()
        if "predicate" in g:
            fields(g,("predicate",),"GUARD_FIELDS")
            p=self.resolve(g["predicate"],("GUARD",));need(set(p["qualified_axes"])<=scope,"SCOPE_ESCAPE")
            # Guard conditions must read inputs/parameters, not the response
            # or derived observation they could otherwise silently exempt.
            need(all(self.symbols[k]["role"] in ("INPUT","METHOD_PARAMETER") for k in p["required_symbols"]),"GUARD_DEPENDENCY")
            return set(p["qualified_axes"])
        fields(g,("op","args"),"GUARD_FIELDS")
        op=g["op"];a=g["args"]
        need(type(a) is list and ((op=="NOT" and len(a)==1) or (op in ("AND","OR") and len(a)>=2)),"GUARD_ARITY")
        return set().union(*(self.guard_refs(x,scope) for x in a))
    def guard(self,g,env):
        if "truth" in g:return g["truth"],[g["reason"]] if g["reason"] else []
        if "predicate" in g:return self.at(self.resolve(g["predicate"],("GUARD",)),env)
        rows=[self.guard(x,env) for x in g["args"]];v=[r[0] for r in rows]
        truth=not3(v[0]) if g["op"]=="NOT" else fold3("FORALL" if g["op"]=="AND" else "EXISTS",v)
        return truth,sorted({reason for _,rs in rows for reason in rs})
    def table(self,symbol):
        need(self.consumer is not None,"MISSING_DATA")
        s=self.symbols[symbol];n=s["native_name"]
        values=self.consumer.data[n] if n in self.program.parameters else self.consumer.table(n)
        return s,values

def validate(bound,assertions):
    ts=bound.tables;ds=ts["domains"];auth=ts["authorities"];scopes=ts["scopes"]
    a=index(assertions);need(bool(a),"NO_ASSERTIONS")
    specs={}
    for k,z in a.items():
        fields(z,("id","role","modality","predicate","scope","binders","at","guard","assumptions","authority_refs"),"ASSERTION_FIELDS")
        need(qualified(k) and z["role"] in ROLES and z["scope"] in scopes,"ASSERTION_ROLE_OR_SCOPE")
        role=z["role"];m=z["modality"]
        need(m==("MAY" if role=="PERMITTED_BEHAVIOUR" else "MUST_NOT" if role=="PROHIBITED_BEHAVIOUR" else "MUST"),"MODALITY")
        refs(z["authority_refs"],auth,"AUTHORITY_REQUIRED")
        p=bound.resolve(z["predicate"],("DATA_ASSUMPTION",) if role=="DATA_ASSUMPTION" else ("PREDICATE",))
        if role in ASSUMPTIONS:
            need(all(bound.symbols[k]["role"] in ("INPUT","METHOD_PARAMETER") for k in p["required_symbols"]),"ASSUMPTION_IS_NOT_GUARANTEE")
        b=z["binders"];need(type(b) is list,"BINDERS")
        for binder in b:
            fields(binder,("axis","kind","quantifier"),"BINDER_FIELDS")
            ax=binder["axis"];need(ax in ds and binder["kind"]==ds[ax]["kind"] and binder["quantifier"] in ("FORALL","EXISTS"),"BINDER_DOMAIN_KIND")
        axes=[x["axis"] for x in b];scope=set(scopes[z["scope"]]["domains"])
        need(len(axes)==len(set(axes)) and set(axes)<=scope and set(axes)<=set(bound.axes),"BINDER_SCOPE")
        gaxes=bound.guard_refs(z["guard"],scope)
        need(set(p["qualified_axes"])|gaxes<=set(axes),"UNBOUND_OR_DUPLICATE_AXIS")
        need(type(z["at"]) is dict and set(z["at"])<=set(axes),"RESTRICTION_AXIS")
        for ax,vals in z["at"].items():
            need(type(vals) is list and bool(vals) and len(vals)==len(set(vals)) and set(vals)<=set(ds[ax]["members"]),"RESTRICTION_DOMAIN")
        refs(z["assumptions"],a,"ASSUMPTION_REF",False)
        if role in ASSUMPTIONS:
            need(not z["assumptions"] and all(x["quantifier"]=="FORALL" for x in b),"ASSUMPTION_SCOPE")
        if role in ("SAFETY_GUARANTEE","PROHIBITED_BEHAVIOUR"):
            need(all(x["quantifier"]=="FORALL" for x in b),"UNIVERSAL_SAFETY_REQUIRED")
        if role in SERVICES:
            need(len(b)>=2 and b[-2]["kind"]=="request" and b[-1]["kind"]=="response" and b[-1]["quantifier"]=="EXISTS" and all(x["quantifier"]=="FORALL" for x in b[:-1]),"REQUEST_RESPONSE_ORDER")
            need(sum(x["kind"]=="request" for x in b)==sum(x["kind"]=="response" for x in b)==1,"REQUEST_RESPONSE_ORDER")
            need(b[-1]["axis"] not in gaxes and b[-1]["axis"] not in z["at"],"RESPONSE_DEPENDENT_APPLICABILITY")
        specs[k]={"row":z,"predicate":p,"axes":axes,"guard_axes":gaxes}
    used=set()
    for k,s in specs.items():
        z=s["row"];assaxes=set()
        for r in z["assumptions"]:
            t=specs[r];need(t["row"]["role"] in ASSUMPTIONS and set(t["axes"])<=set(s["axes"]),"ASSUMPTION_SCOPE")
            if z["role"] in SERVICES:need(s["axes"][-1] not in t["axes"],"RESPONSE_DEPENDENT_APPLICABILITY")
            used.add(r);assaxes.update(t["axes"])
        need(set(s["axes"])==set(s["predicate"]["qualified_axes"])|s["guard_axes"]|assaxes,"UNUSED_BINDER")
    # Every declared native assumption is represented and used in a guarantee.
    nset={p["id"] for p in bound.leaf["interface"]["predicates"].values() if p["role"]=="DATA_ASSUMPTION"}
    given=[s["predicate"]["predicate_id"] for s in specs.values() if s["row"]["role"]=="DATA_ASSUMPTION"]
    need(len(given)==len(set(given)) and set(given)==nset,"NATIVE_ASSUMPTION_COVERAGE")
    need({k for k,s in specs.items() if s["row"]["role"] in ASSUMPTIONS}<=used,"UNBOUND_ASSUMPTION")
    need(any(s["row"]["role"] not in ASSUMPTIONS and s["row"]["modality"]!="MAY" for s in specs.values()),"NO_OBLIGATION")
    return specs

def evaluate(bound,assertions,witnesses):
    specs=validate(bound,assertions);ds=bound.tables["domains"];w=index(witnesses)
    by_assertion={}
    for row in w.values():
        fields(row,("id","assertion","key","response","source_ref","data_identity"),"WITNESS_FIELDS")
        k=row["assertion"];need(k in specs and specs[k]["row"]["role"]=="SERVICE_GUARANTEE","WITNESS_SUBJECT")
        need(row["data_identity"]==bound.data_identity and bound.data_identity is not None,"WITNESS_SNAPSHOT")
        need(row["source_ref"] in bound.tables["authorities"] and bound.tables["authorities"][row["source_ref"]]["role"] in ("SOURCE","PROVENANCE"),"WITNESS_SOURCE")
        ss=specs[k];prefix=ss["axes"][:-1];axis=ss["axes"][-1];key=row["key"]
        need(type(key) is list and len(key)==len(prefix) and all(v in ds[a]["members"] and type(v) is type(ds[a]["members"][0]) for a,v in zip(prefix,key)) and row["response"] in ds[axis]["members"] and type(row["response"]) is type(ds[axis]["members"][0]),"WITNESS_COORDINATE")
        m=by_assertion.setdefault(k,{});need(tuple(key) not in m,"DUPLICATE_WITNESS");m[tuple(key)]=row
    def point(s,env,apply_assumptions=True):
        z=s["row"]
        if any(env[ax] not in vals for ax,vals in z["at"].items()):return None,["OUTSIDE_SCOPE"]
        g,why=bound.guard(z["guard"],env)
        if g=="FALSE":return None,why+["GUARD_FALSE"]
        if g=="UNKNOWN":return g,why
        if apply_assumptions:
            ar=[point(specs[k],env,False) for k in z["assumptions"]]
            if any(v=="FALSE" for v,_ in ar):return None,["OUTSIDE_ASSUMPTIONS"]
            if any(v!="TRUE" for v,_ in ar):return "UNKNOWN",sorted({"BLOCKED_ASSUMPTIONS",*(x for _,rs in ar for x in rs)})
        v,why=bound.at(s["predicate"],env)
        if v is not None and z["modality"]=="MUST_NOT":v=not3(v)
        return v,why
    def fold(op,items):
        vals=[v for v,_ in items if v is not None];why=sorted({x for _,rs in items for x in rs})
        return (fold3(op,vals) if vals else None),why
    def walk(s,i,env):
        if i==len(s["axes"]):return point(s,env)
        ax=s["axes"][i];q=s["row"]["binders"][i]["quantifier"]
        return fold(q,[walk(s,i+1,{**env,ax:x}) for x in ds[ax]["members"]])
    results=[]
    for k,s in specs.items():
        role=s["row"]["role"];missing=[];actual_keys=set();finite_requests=0
        if role in SERVICES:
            prefix=s["axes"][:-1];a=s["axes"][-1];rows=[];wr=by_assertion.get(k,{})
            for key in product(*(ds[x]["members"] for x in prefix)):
                env=dict(zip(prefix,key));candidates=[(r,point(s,{**env,a:r})) for r in ds[a]["members"]]
                truth,why=fold("EXISTS",[p for _,p in candidates])
                if truth is None:
                    # An inapplicable request never contributes a vacuous pass.
                    continue
                finite_requests+=1
                if role=="SERVICE_GUARANTEE":
                    if key not in wr:
                        missing.append(list(key));truth="UNKNOWN" if truth!="FALSE" else "FALSE";why=why+["MISSING_EVIDENCE"]
                    else:
                        actual_keys.add(key);observed=dict(candidates)[wr[key]["response"]]
                        truth=observed[0] if observed[0] is not None else "UNKNOWN";why=why+observed[1]
                rows.append((truth,why))
            need(actual_keys==set(wr),"WITNESS_OUTSIDE_APPLICABILITY")
            truth,why=fold("FORALL",rows)
            if finite_requests==0:truth="UNKNOWN";why=why+["NONVACUOUS_SERVICE_REQUIRED"]
        elif s["row"]["modality"]=="MAY":truth,why=None,["PERMISSION_NOT_OBLIGATION"]
        else:truth,why=walk(s,0,{})
        status="FINITE_OBSERVED_TRUE" if truth=="TRUE" else "FINITE_COUNTEREXAMPLE" if truth=="FALSE" else "BLOCKED" if truth=="UNKNOWN" else "NOT_APPLICABLE"
        results.append({"id":k,"truth":truth,"finite_status":status,"reasons":sorted(set(why)),"applicable_requests":finite_requests if role in SERVICES else None,"missing_witnesses":missing,"owner":"OWNER_TBD","conformance":"NOT_PROVED"})
    gr=[r for r in results if specs[r["id"]]["row"]["role"] not in ASSUMPTIONS and specs[r["id"]]["row"]["modality"]!="MAY"]
    v="FINITE_COUNTEREXAMPLE" if any(r["truth"]=="FALSE" for r in gr) else "BLOCKED" if any(r["truth"]=="UNKNOWN" for r in gr) else "NOT_APPLICABLE" if all(r["truth"] is None for r in gr) else "FINITE_OBSERVATIONS_ONLY"
    return {"status":v,"assertions":sorted(results,key=lambda r:r["id"]),"scope":"FINITE_DECLARED_SUPPORT_AND_WITNESSES_ONLY","owner":"OWNER_TBD","conformance":"NOT_PROVED"}

def nonanticipativity(bound,policies):
    t=bound.tables;out=[]
    for k,p in index(policies).items():
        fields(p,("id","symbol","time_domain","scenario_domain","authority_refs"),"POLICY_FIELDS")
        refs(p["authority_refs"],t["authorities"],"AUTHORITY_REQUIRED")
        need(p["symbol"] in bound.symbols,"POLICY_SYMBOL")
        s,vals=bound.table(p["symbol"]);axes=s["domain_ids"];td,sd=p["time_domain"],p["scenario_domain"]
        need(td in axes and sd in axes and td!=sd,"POLICY_AXES")
        infos=[x for x in t["information_sets"].values() if x["time_domain"]==td and x["scenario_domain"]==sd]
        need(bool(infos),"INFORMATION_PARTITION_REQUIRED")
        ti,si=axes.index(td),axes.index(sd);others=[a for a in axes if a not in (td,sd)];bad=[]
        for info in infos:
            for group in info["partition"]:
                for key in product(*(t["domains"][a]["members"] for a in others)):
                    env=dict(zip(others,key));env[td]=info["stage"];qq=[]
                    for v in group:
                        env[sd]=v;coord=tuple(env[a] for a in axes);qq.append(vals[coord])
                    if any(x!=qq[0] for x in qq[1:]):bad.append({"stage":info["stage"],"group":group,"other":list(key)})
        out.append({"id":k,"status":"FINITE_COUNTEREXAMPLE" if bad else "FINITE_OBSERVED_TRUE","violations":bad,"conformance":"NOT_PROVED"})
    return sorted(out,key=lambda r:r["id"])

def boundaries(bound,assertions,states):
    """State-boundary obligation declarations are references to native conditions.
    No balance equation or target value is supplied by the outer layer."""
    specs=validate(bound,assertions);out=[]
    for k,r in index(states).items():
        fields(r,("id","symbol","time_domain","mode","initial","terminal","authority_refs"),"STATE_FIELDS")
        refs(r["authority_refs"],bound.tables["authorities"],"AUTHORITY_REQUIRED")
        s=bound.symbols.get(r["symbol"]);td=r["time_domain"];need(s is not None and td in s["domain_ids"],"STATE_AXIS")
        ch=[x for x in bound.tables["chronologies"].values() if x["domain"]==td];need(len(ch)==1 and r["mode"]==ch[0]["mode"],"STATE_CHRONOLOGY")
        labels=bound.tables["domains"][td]["members"]
        if r["mode"]=="NONCYCLIC":need(r["initial"]!=r["terminal"],"BOUNDARY_DISTINCT")
        else:need(r["initial"]==r["terminal"],"CYCLIC_BOUNDARY_REFERENCE")
        for name,label in (("initial",labels[0]),("terminal",labels[-1] if r["mode"]=="NONCYCLIC" else labels[0])):
            a=specs.get(r[name]);need(a is not None and a["row"]["role"]=="SAFETY_GUARANTEE","BOUNDARY_ASSERTION")
            need(a["row"]["at"].get(td)==[label] and r["symbol"] in a["predicate"]["required_symbols"],"BOUNDARY_SCOPE_OR_SYMBOL")
        out.append({"id":k,"status":"BOUND_NATIVE_ASSERTIONS","conformance":"NOT_PROVED"})
    return sorted(out,key=lambda r:r["id"])
