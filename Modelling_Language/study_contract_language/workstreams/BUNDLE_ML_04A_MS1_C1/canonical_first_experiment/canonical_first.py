"""Canonical-first bounded research experiment; native Spec is the only stored math.
No claim of mathematical equivalence, complete CSNF, or C2 interface freeze.
"""
from pathlib import Path
from copy import deepcopy
from hashlib import sha256
import sys
import mathspec as ms
from mathspec.errors import LanguageError
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"WS_A_mathematical_foundation/native_adapter"))
import foundation as c1

VERSION="canonical-first-research-0.1"
def hash_text(s):return sha256(s.encode("utf-8")).hexdigest()
def load(s):
    try:return ms.to_spec(s)
    except LanguageError as e:raise c1.Reject("NATIVE_REJECT:"+str(e)) from e

def admit_canonical(text,context,original_json=None):
    """Canonical YAML + external semantic bindings; no alternate math AST.

    If original_json is absent, the canonical artifact is itself the source.
    This does NOT establish fidelity to any pre-canonical authoring artifact.
    """
    c1.need(type(text) is str,"CANONICAL_TEXT_REQUIRED")
    spec=load(text)
    c1.need(spec.to_yaml(canonical=True)==text,"NOT_NATIVE_CANONICAL")
    c1.fields(context,("domains","symbols","scope","predicates","method","audit"),"CONTEXT_FIELDS")
    for k in ("domains","symbols","predicates"):
        c1.need(type(context[k]) is dict,"CONTEXT_MAP")
    c1.need(not any(getattr(spec,k) for k in ("relations","conditions","variables","constraints","sos","piecewise","assumptions","macros")) and spec.objective is None,"OUTSIDE_BOUNDED_PROFILE")
    # Existing C1 bridge is temporary. Derive mathematical shape/defaults
    # from public Spec, never persist a second mathematical representation.
    native={"version":spec.version,"dimensions":{},"parameters":{},"expressions":{}}
    domains={};symbols={}
    c1.need(set(context["domains"])==set(spec.dimensions),"DOMAIN_BINDING")
    for n,d in spec.dimensions.items():
        z=context["domains"][n]
        c1.fields(z,("id","labels"),"DOMAIN_CONTEXT")
        c1.need(d.one_of is None and d.description is None,"PROFILE_DIMENSION_FEATURE")
        native["dimensions"][n]={"dtype":d.dtype,"ordered":d.ordered}
        domains[n]={**z,"dtype":d.dtype,"ordered":d.ordered}
    c1.need(set(context["symbols"])==set(spec.parameters)|set(spec.expressions),"SYMBOL_BINDING")
    for n,p in spec.parameters.items():
        z=context["symbols"][n]
        c1.fields(z,("id","role","quantity","nonzero"),"SYMBOL_CONTEXT")
        c1.need(p.where is None and p.missing=="refused" and p.description is None,"MISSING_OR_PROFILE_POLICY")
        axes=list(p.dims)
        native["parameters"][n]={"dims":axes,"dtype":p.dtype,"missing":p.missing}
        symbols[n]={**z,"axes":axes,"dtype":p.dtype}
    for n,e in spec.expressions.items():
        z=context["symbols"][n]
        c1.fields(z,("id","role","quantity","nonzero"),"SYMBOL_CONTEXT")
        c1.need(type(e.expression) is str,"PROFILE_EXPRESSION_FEATURE")
        native["expressions"][n]=e.expression
        symbols[n]={**z,"axes":list(spec.program.expressions[n].expression.dims),"dtype":"float"}
    # Mandatory explicit pointwise/scalar comparison support. No Cartesian
    # joins between unrelated non-scalar axes, no implicit guard support.
    predicates={};supports={}
    for name,p in context["predicates"].items():
        c1.fields(p,("lhs","rhs","cmp","guard","axes","alignment","guard_alignment"),"PREDICATE_SIGNATURE")
        a,b=p["lhs"],p["rhs"]
        c1.need(a in symbols and b in symbols,"PREDICATE_REFERENCE")
        aa,bb=set(symbols[a]["axes"]),set(symbols[b]["axes"])
        c1.need((p["alignment"]=="SAME_AXES" and aa==bb) or (p["alignment"]=="SCALAR_BROADCAST" and (not aa or not bb) and aa!=bb),"PREDICATE_ALIGNMENT")
        support=aa|bb
        c1.need(p["axes"]==[n for n in context["scope"]["binders"] if n in support],"PREDICATE_AXES")
        g=p["guard"]
        if type(g) is bool:
            c1.need(p["guard_alignment"]=="CONSTANT","GUARD_ALIGNMENT")
        else:
            c1.need(type(g) is str and g in symbols and symbols[g]["dtype"]=="bool","GUARD_TYPE")
            ga=set(symbols[g]["axes"])
            c1.need((p["guard_alignment"]=="SAME_AXES" and ga==support) or (p["guard_alignment"]=="SCALAR_BROADCAST" and not ga and bool(support)),"GUARD_ALIGNMENT")
        predicates[name]={k:p[k] for k in ("lhs","rhs","cmp","guard")}
        supports[name]={"axes":p["axes"],"alignment":p["alignment"],"guard_alignment":p["guard_alignment"]}
    envelope={"version":c1.VERSION,"native":native,"domains":domains,"symbols":symbols,"scope":context["scope"],"predicates":predicates,"method":context["method"],"audit":context["audit"]}
    checked=c1.validate(c1.canon(envelope))
    c1.need(checked["native_canonical"]==text,"BRIDGE_CHANGED_NATIVE_SPEC")
    # Optional original exact JSON authoring source. Validate before native
    # canonicalisation: canonical bytes alone cannot attest the preimage.
    if original_json is not None:
        raw=c1.parse(original_json)
        c1.fields(raw,("version","dimensions","parameters","expressions"),"ORIGINAL_PROFILE")
        for e in raw["expressions"].values():c1.check_literal_tokens(e)
        c1.need(load(raw).to_yaml(canonical=True)==text,"ORIGINAL_CANONICAL_MISMATCH")
        # Only verify lexical literal preservation and canonical match in the
        # bounded profile; authority of the source remains external.
        origin={"kind":"ORIGINAL_JSON_CHECKED","sha256":hash_text(original_json)}
    else:origin={"kind":"CANONICAL_AS_SOURCE","sha256":hash_text(text)}
    semantic_context=deepcopy({k:v for k,v in context.items() if k!="audit"})
    for n,z in semantic_context["domains"].items():
        if not spec.dimensions[n].ordered:z["labels"]=sorted(z["labels"])
    # Native dtype and index frame are already in the native spec. Outer
    # scope order and domain coordinates are explicit semantic additions.
    native_id=c1.digest({"upstream":c1.UPSTREAM,"canonical":text})
    sem=c1.digest({"schema":VERSION,"native":native_id,"registry":c1.digest(c1.REGISTRY),"context":semantic_context})
    audit=c1.digest({"semantic":sem,"origin":origin,"context_as_received":context})
    return {"schema":VERSION,"upstream":c1.UPSTREAM,"native_canonical":text,
            "context":deepcopy(context),"origin":origin,"original_json":original_json,
            "native_identity":native_id,"semantic_identity":sem,"audit_identity":audit,
            "predicate_support":supports,"stage":"BOUNDED_MATHEMATICAL_INTERFACE_ONLY"}

def reimport(leaf):
    c1.need(type(leaf) is dict and {"native_canonical","context","original_json"}<=set(leaf),"LEAF_FIELDS")
    rebuilt=admit_canonical(leaf["native_canonical"],leaf["context"],leaf["original_json"])
    c1.need(rebuilt==leaf,"LEAF_TAMPER")
    return rebuilt
