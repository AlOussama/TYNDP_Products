"""Versioned mathematical contract package and independent C2 research clients.

The package is not a full Study Contract: external obligations and method
execution remain unresolved. It contains native mathspec bytes and typed
bindings only, never a second mathematical AST.
"""
from copy import deepcopy
from closure import (admit,reimport,bind_data,native,semantic_context,
                     c1,need,fields,digest,canon,VERSION)
PACKAGE="canonical-mathematical-contract-package-0.1"

def export_package(leaf):
    leaf=reimport(leaf)
    p=native(leaf["native_canonical"])
    return canon({
      "schema":PACKAGE,
      "mathematics":{"upstream":leaf["upstream"],"canonical":leaf["native_canonical"],"identity":leaf["native_identity"]},
      "binding":{"version":VERSION,"quantity_registry_identity":digest(c1.REGISTRY),"semantic_context":semantic_context(p,leaf["context"]),
                 "interface":leaf["interface"],"identity":leaf["semantic_identity"]},
      "audit":{"origin":leaf["origin"],"source":leaf["source"],"context_as_received":leaf["context"],"identity":leaf["audit_identity"]},
      "evidence":{"stage":"STATIC_MATHEMATICAL_BOUNDARY_ONLY","obligations":"NOT_EXECUTED","owner":"OWNER_TBD"}})

def import_package(text):
    obj=c1.parse(text)
    fields(obj,("schema","mathematics","binding","audit","evidence"),"PACKAGE_FIELDS")
    need(obj["schema"]==PACKAGE,"PACKAGE_VERSION")
    a=obj["audit"];fields(a,("origin","source","context_as_received","identity"),"PACKAGE_AUDIT")
    need(type(a["origin"]) is dict and a["origin"].get("kind") in ("CANONICAL_AS_SOURCE","AUTHOR_SOURCE_PRECHECKED"),"ORIGIN_KIND")
    leaf=admit(a["source"],a["context_as_received"],a["origin"]["kind"]=="CANONICAL_AS_SOURCE")
    need(export_package(leaf)==text,"PACKAGE_TAMPER_OR_NONCANONICAL")
    return leaf

def predicate_client(package,predicate_id,expected_role):
    """C2 external-contract client: no method evaluation or A/G implementation."""
    return _predicate_from_leaf(import_package(package),predicate_id,expected_role)

def _predicate_from_leaf(leaf,predicate_id,expected_role):
    p=native(leaf["native_canonical"]).program
    matches=[(n,z) for n,z in leaf["interface"]["predicates"].items() if z["id"]==predicate_id]
    need(len(matches)==1,"PREDICATE_ID")
    n,z=matches[0]
    need(expected_role in ("PREDICATE","GUARD","DATA_ASSUMPTION") and z["role"]==expected_role,"PREDICATE_ROLE")
    if n in p.conditions:
        names=set(p.conditions[n].condition.names_read)
    else:
        a=p.assumptions[n];names=set(a.holds.names_read)|(set(a.where.names_read) if a.where else set())
    c=leaf["context"]
    return {"schema":"c2-predicate-interface-0.1","mathematical_identity":leaf["semantic_identity"],
            "native_name":n,"predicate_id":predicate_id,"role":expected_role,"qualified_axes":z["axes"],
            "required_symbols":[c["symbols"][x]["id"] for x in sorted(names) if x in c["symbols"]],
            "required_relations":[c["relations"][x]["id"] for x in sorted(names) if x in c["relations"]],
            "truth_contract":z["truth_contract"],"scope_id":c["scope"]["id"],
            "verdict":"NOT_EXECUTED","behavioural_semantics":"C2_REQUIRED"}

def method_client(package,data):
    """C2 profile client: uses no contract/predicate client, verifies input binding."""
    leaf=import_package(package)
    receipt=bind_data(leaf,data)
    return {"schema":"c2-method-interface-0.1","signature":deepcopy(leaf["interface"]["method_signature"]),
            "method_signature_identity":leaf["interface"]["method_identity"],
            "study_identity":leaf["interface"]["study_identity"],
            "context_receipt":receipt,"method_result":"NOT_EXECUTED","owner":"OWNER_TBD"}
