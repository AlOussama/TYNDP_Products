"""Versioned, bounded dynamic integer power admission. Reuses all C1 checks.
No new AST or parser. C1 v0.2 and package v0.1 stay unchanged by default."""
from copy import deepcopy
import mathspec.program as mp
from closure import (Checked,need,fields,native,constant,DIMLESS,digest,canon,c1,
                     semantic_context,exact,_admit,_bind_data)
from native_consumer import FiniteNative
VERSION="canonical-first-research-0.3"
PACKAGE="canonical-mathematical-contract-package-0.2"
class PowerChecked(Checked):
    def __init__(self,spec,context):
        need(type(context) is dict and "power_domains" in context,"POWER_POLICY_REQUIRED")
        self.power_domains=context["power_domains"];self.used_exponents=set()
        need(type(self.power_domains) is dict and bool(self.power_domains),"POWER_POLICY_REQUIRED")
        for b in self.power_domains.values():
            fields(b,("min","max"),"POWER_RANGE_FIELDS")
            need(type(b["min"]) is int and type(b["max"]) is int and -100<=b["min"]<=b["max"]<=100,"POWER_RANGE")
        super().__init__(spec,{k:v for k,v in context.items() if k!="power_domains"})
        need(self.used_exponents==set(self.power_domains),"POWER_POLICY_COVERAGE")
    def expr(self,e,opened=False):
        if type(e) is mp.Power and constant(e.exponent) is None:
            a,b=self.expr(e.base),self.expr(e.exponent)
            n=e.exponent
            need(type(n) is mp.ParameterReference and n.name in self.p.parameters and self.p.parameters[n.name].dtype=="int","POWER_INTEGER_PARAMETER")
            need(self.c["symbols"][n.name]["role"] in ("INPUT","METHOD_PARAMETER") and n.name in self.power_domains,"POWER_PARAMETER_ROLE")
            need(a==b==DIMLESS,"DYNAMIC_POWER_DIMENSIONLESS")
            v=constant(e.base)
            need((v is not None and v>0) or (type(e.base) is mp.ParameterReference and self.c["symbols"][e.base.name]["domain_rule"]=="POSITIVE"),"POWER_POSITIVE_BASE_REQUIRED")
            self.used_exponents.add(n.name)
            return DIMLESS
        return super().expr(e,opened)

def admit(source,context,require_canonical=False):
    return _admit(source,context,require_canonical,PowerChecked,VERSION)
def reimport(leaf):
    need(type(leaf) is dict and leaf.get("schema")==VERSION and {"source","context","origin"}<=set(leaf),"POWER_LEAF_VERSION")
    got=admit(leaf["source"],leaf["context"],leaf["origin"]["kind"]=="CANONICAL_AS_SOURCE")
    need(got==leaf,"POWER_LEAF_TAMPER");return got
def bind_data(leaf,data):
    r=_bind_data(leaf,data,reimport)
    for n,b in leaf["context"]["power_domains"].items():
        need(all(b["min"]<=exact(x["value"])<=b["max"] for x in data["parameters"][n]),"POWER_RANGE")
    return r
def export_package(leaf):
    leaf=reimport(leaf);p=native(leaf["native_canonical"])
    return canon({"schema":PACKAGE,"mathematics":{"upstream":leaf["upstream"],"canonical":leaf["native_canonical"],"identity":leaf["native_identity"]},
      "binding":{"version":VERSION,"quantity_registry_identity":digest(c1.REGISTRY),"semantic_context":semantic_context(p,leaf["context"]),"interface":leaf["interface"],"identity":leaf["semantic_identity"]},
      "audit":{"origin":leaf["origin"],"source":leaf["source"],"context_as_received":leaf["context"],"identity":leaf["audit_identity"]},
      "evidence":{"stage":"STATIC_MATHEMATICAL_BOUNDARY_ONLY","obligations":"NOT_EXECUTED","owner":"OWNER_TBD"}})
def import_package(text):
    obj=c1.parse(text)
    fields(obj,("schema","mathematics","binding","audit","evidence"),"POWER_PACKAGE_FIELDS")
    need(obj["schema"]==PACKAGE,"POWER_PACKAGE_VERSION")
    a=obj["audit"];fields(a,("origin","source","context_as_received","identity"),"POWER_PACKAGE_AUDIT")
    need(type(a["origin"]) is dict and a["origin"].get("kind") in ("CANONICAL_AS_SOURCE","AUTHOR_SOURCE_PRECHECKED"),"ORIGIN_KIND")
    leaf=admit(a["source"],a["context_as_received"],a["origin"]["kind"]=="CANONICAL_AS_SOURCE")
    need(export_package(leaf)==text,"POWER_PACKAGE_TAMPER_OR_NONCANONICAL");return leaf
def method_client(package,data):
    leaf=import_package(package);receipt=bind_data(leaf,data)
    return {"schema":"c2-method-interface-0.1","signature":deepcopy(leaf["interface"]["method_signature"]),
            "method_signature_identity":leaf["interface"]["method_identity"],"study_identity":leaf["interface"]["study_identity"],
            "context_receipt":receipt,"method_result":"NOT_EXECUTED","owner":"OWNER_TBD"}
class FinitePowerNative(FiniteNative):
    def __init__(self,leaf,data):
        self._initialize(leaf,data,bind_data)
