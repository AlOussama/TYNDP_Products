"""Explicit diagnostic provenance boundaries. No invented failing leaf path.
R00–R13 source map is fixed to the original C19 rules. Original oracle codes
and candidate validator codes are distinct; C3 attaches actual A/B leaf paths.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from closure import Reject,digest,need
RULE_SOURCE={"commit":"2f0297b754e3a96a2523a34d3af98782b26181f3","path":"Modelling_Language/study_contract_language/workstreams/ML_C19_canonical_normal_form_research/07_normalization_rules.md","blob":"7e9f506183bdce7a7c76e08fb7a2f316649088b7"}
_CTX=ContextVar("c2_diagnostic_context",default=())
def pointer(*parts):return "".join("/"+str(p).replace("~","~0").replace("/","~1") for p in parts)
class DiagnosticReject(Reject):
    def __init__(self,record):
        self.record=record
        super().__init__(record["code"]+": "+record["path"]+" — "+record["reason"])
def rule_for(code,default):
    # Explicit code-to-rule map for existing and new tested semantics.
    if code.startswith(("OVERRIDE_", "METHOD_DEPENDENCY_", "PROCESS_DEPENDENCY_", "UPSTREAM_")):return "R10"
    if code.startswith(("EVIDENCE_", "VERIFICATION_", "WITNESS_", "REPORT_EVIDENCE_")):return "R13"
    if code.startswith(("GUARD_", "ASSUMPTION_", "UNBOUND_ASSUMPTION", "DIRECT_OBLIGATION_", "REQUEST_RESPONSE_", "BINDER_", "UNIVERSAL_", "RESPONSE_DEPENDENT_")):return "R09"
    if code.startswith(("CHRONOLOGY_", "DURATION_", "STATE_", "BOUNDARY_", "CYCLE_", "INFORMATION_", "SHIFT_", "WINDOW_")):return "R07"
    if code.startswith(("PORT_", "RELATION_TYPE", "TOPOLOGY_")):return "R08"
    if code.startswith(("QUANTITY", "PHYSICAL_TYPE", "CARRIER", "PRICE_BASIS", "CONVERSION_", "ANNUAL_INTEGRATION", "UNIT_", "HEATING_VALUE")):return "R06"
    if code.startswith(("SELECTOR_", "METRIC_", "TOLERANCE_", "CONTRIBUTION_", "SEMANTIC_DOUBLE_COUNT", "N7_CONTRIBUTION", "PROBABILITY_", "COUNTERFACTUAL_", "UNAUTHORIZED_PROJECT_CHANGE", "CROSS_MODEL_")):return "R12"
    if code.startswith(("AUTHORITY_PROMOTION","NORMATIVITY_","INFORMATIVE_","METHOD_SOURCE","SOURCE_")):return "R09"
    if code.startswith(("UNKNOWN_", "MISSING_")):return "R11"
    if code.startswith(("DUPLICATE_ID","UNRESOLVED_","AMBIGUOUS_ID")):return "R01"
    return default

@contextmanager
def scope(path,rule,subject=None,source_refs=()):
    # Paths identify the precise validated field or nearest validated object.
    # For opaque native/source errors the enclosing object is explicit.
    frame={"path":path,"default_rule":rule,"subject":subject,"source_refs":list(source_refs)}
    token=_CTX.set(_CTX.get()+(frame,))
    try:yield
    except DiagnosticReject:raise
    except (Reject,ValueError,TypeError,KeyError,IndexError) as e:
        reason=str(e);code=reason.split(":",1)[0].split(";",1)[0]
        if not code or not code.replace("_","").isalnum() or code!=code.upper():code="VALIDATION_EXCEPTION"
        ctx=_CTX.get()
        record={"schema":"c2-structured-diagnostic-0.1","code":code,"path":path,"path_kind":"VALIDATION_OBJECT","rule_id":rule_for(code,rule),
                "rule_source":RULE_SOURCE,"subject":subject,"source_refs":list(source_refs),"trace":[deepcopy(x) for x in ctx],"reason":reason,
                "status":"REJECTED","owner":"OWNER_TBD","conformance":"NOT_PROVED"}
        raise DiagnosticReject(record) from e
    finally:_CTX.reset(token)
def call(path,rule,subject,source_refs,fn,*args,**kw):
    with scope(path,rule,subject,source_refs):return fn(*args,**kw)

def candidate_receipt(fn,*args,**kw):
    """External C3 adapter entry point: success receipt or actual diagnostic."""
    try:return {"status":"RETURNED","result":fn(*args,**kw),"diagnostics":[]}
    except DiagnosticReject as e:return {"status":"REJECTED","result":None,"diagnostics":[e.record]}
