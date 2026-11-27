"""Controlled counterexamples and semantic-layer ablations.
Never compare heterogeneous stages as architecture pass percentages.
"""
import json,copy,sys
from fractions import Fraction as F
from pathlib import Path
from common_fixtures import cases,frozen,CORPUS,ROOT
from closure import admit,native,bind_data,preflight,Reject,digest,canon
from package_interface import export_package,import_package
from native_consumer import FiniteNative
from legacy_comparison import map_profile,map_predicates,n1r,R1
import mathspec as ms
sys.path.insert(0,str(CORPUS/"independent_oracles"))
import oracles
from profile_engine import Engine

def reject(fn,code):
    try:fn()
    except (ValueError,TypeError,KeyError) as e:
        if code not in str(e):raise AssertionError((code,str(e))) from e
        return str(e)
    raise AssertionError("Unexpected acceptance: "+code)
def open_(x):return admit(json.dumps(x["doc"]),x["context"])
def prog(x):preflight(x["doc"]);return ms.to_spec(x["doc"]).program
def control(id,description,actual,limit):
    return {"id":id,"description":description,"actual":actual,"limit":limit,"status":"PASS"}

def main():
    cc={c["id"]:c for c in cases()};r=[]
    # 1. Native math alone is not a physical contract.
    a=copy.deepcopy(cc["RC01"]);x=open_(a);b=copy.deepcopy(a)
    b["context"]["symbols"]["e"]["quantity"]={**b["context"]["symbols"]["e"]["quantity"],"unit":"kg","carrier":"hydrogen"}
    assert ms.to_spec(a["doc"]).to_yaml(canonical=True)==ms.to_spec(b["doc"]).to_yaml(canonical=True)
    m3=reject(lambda:open_(b),"COMPARISON_TYPE")
    m2=reject(lambda:map_predicates(b,prog(b)),"LEGACY_RC01_QUANTITY_OR_ROLE")
    r.append(control("ABL01","Remove physical compatibility while keeping identical native math",{"native_load":"ACCEPTS_IDENTICAL_MATH","M3":m3,"M2":m2},"Both require a semantic binding; M2 fixed-duration adapter must validate its target specialization."))
    # 2. Conversions must retain typed basis and authority context.
    a=copy.deepcopy(cc["RC03"]);a["context"]["conversions"]={}
    r.append(control("ABL02","Remove conversion metadata",{"M3":reject(lambda:open_(a),"CONVERSION_BINDING"),"native_load":"ACCEPTS"},"No scientific proof of authenticity of declared conversion source."))
    # 3. Common data completeness requirement.
    a=copy.deepcopy(cc["RC02"]);leaf=open_(a);data=copy.deepcopy(a["data"]);data["parameters"]["delivered"].pop()
    r.append(control("ABL03","Remove one identical EV observation row",{"M3":reject(lambda:bind_data(leaf,data),"INCOMPLETE_PARAMETER_SUPPORT"),"M2":reject(lambda:map_profile(a,prog(a),data),"DOMAIN_COVERAGE")},"Comparable finite data-support control."))
    # 4. Native relation declarations cannot attest attached cardinality.
    a=copy.deepcopy(cc["RC05"]);leaf=open_(a);data=copy.deepcopy(a["data"]);data["relations"]["sending"].pop()
    r.append(control("ABL04","Remove an oriented endpoint row",{"M3":reject(lambda:bind_data(leaf,data),"RELATION_KEY_COVERAGE"),"native_load":"ACCEPTS_WITH_NO_DATA","M2":"NO_LEGACY_RELATION_MAPPER"},"No general proof of arbitrary sparse topology."))
    # 5. Symbol role matters even when native canonical bytes do not change.
    a=copy.deepcopy(cc["RC10"]);x=open_(a);a["context"]["symbols"]["a"]["role"]="INPUT";y=open_(a)
    assert x["native_identity"]==y["native_identity"] and x["semantic_identity"]!=y["semantic_identity"]
    r.append(control("ABL05","Change OBSERVABLE to INPUT with identical native math",{"native_identity_equal":True,"M3_bound_identity_equal":False,"M2":reject(lambda:map_predicates(a,prog(a)),"LEGACY_SYMBOL_ROLE")},"Both preserve role separation in their tested admitted scopes."))
    # 6. Source audit change must not become semantic change.
    a=copy.deepcopy(cc["RC01"]);x=open_(a);l=map_predicates(a,prog(a))
    a["context"]["audit"]["source_ref"]="fixture:alternate-source";y=open_(a);m=map_predicates(a,prog(a))
    assert x["native_identity"]==y["native_identity"] and x["semantic_identity"]==y["semantic_identity"] and x["audit_identity"]!=y["audit_identity"]
    assert l["audit_digest"]==m["audit_digest"]
    d=copy.deepcopy(l["contract"]);d["authorities"][0]["immutable_ref"]="urn:comparison:alternate-source"
    legacy=n1r.run(json.dumps(d),"B")
    assert legacy["semantic_digest"]==l["semantic_digest"] and legacy["audit_digest"]!=l["audit_digest"]
    r.append(control("ABL06","Change original audit source, compare native-bound and legacy identities",{"M3_semantic_same":True,"M3_audit_changed":True,"M2_current_mapping_audit_changed":False,"R1_can_preserve_audit_if_explicitly_mapped":True},"Actual M2 adapter gap, not intrinsic inability of R1; prior legacy digest equality was only in the legacy projection."))
    # 7. Both native routes share lexical float risks.
    a={"version":0,"parameters":{"a":{"dims":[]}},"expressions":{"v":"a*9007199254740992"}}
    b=copy.deepcopy(a);b["expressions"]["v"]="a*9007199254740993"
    assert ms.to_spec(a).to_yaml(canonical=True)==ms.to_spec(b).to_yaml(canonical=True)
    r.append(control("ABL07","Distinct integer literals collide after native float parsing",{"native_canonical_equal":True,"shared_preflight_rejects":reject(lambda:preflight(b),"NUMERIC_PRECISION")},"No intrinsic advantage of M2 or M3 when both start from lossy native math."))
    # 8. M3 source-description bytes are part of its current bound identity.
    a=copy.deepcopy(cc["RC10"]);x=open_(a);a["doc"]["description"]="Documentation change only";y=open_(a)
    assert x["native_identity"]!=y["native_identity"] and x["semantic_identity"]!=y["semantic_identity"]
    r.append(control("ABL08","Documentation-only edit in native Spec changes current semantic identity",{"native_identity_changed":True,"M3_bound_identity_changed":True},"Current identity over-distinguishes documentation; define semantic projection policy separately from canonical text and audit."))
    # 9. Crucial counterexample: arithmetic agreement with invalid probability.
    a=copy.deepcopy(cc["RC09"]);leaf=open_(a);bad=copy.deepcopy(a["data"])
    bad["parameters"]["weight"][1]["value"]="3/5"
    bad["parameters"]["reported"][0]["value"]="1500/11"
    n=FiniteNative(leaf,bad);out=n.outputs();pred=n.conditions()
    assert out=={"annual":["150"],"discounted":["1500/11"]} and pred["result_ok"]
    m2=reject(lambda:map_profile(a,prog(a),bad),"PROBABILITY_NORMALIZATION")
    doc=frozen("RC09");doc["synthetic_data"]["inputs"]["weights"]=["3/5","3/5"];doc["synthetic_data"]["observed"].update(annual="150",discounted="1500/11")
    independent=reject(lambda:oracles.run(doc),"WEIGHT")
    r.append(control("ABL09","Methodologically invalid probability weights, but arithmetic and reported result agree",{"weight_sum":"6/5","M3_static_and_finite_math_accepts":True,"M3_math":out,"M3_predicates":pred,"M2_original_profile_engine":m2,"independent_oracle":independent},"Mandatory method-role normalization semantics missing in current M3; no contract PASS claimed."))
    # 10. C1 native package prohibits evidence promotion and raw injected AST.
    a=copy.deepcopy(cc["RC10"]);pkg=json.loads(export_package(open_(a)));pkg["evidence"]["obligations"]="PASS"
    r.append(control("ABL10","Promote evidence without actual contract execution",{"M3":reject(lambda:import_package(canon(pkg)),"PACKAGE_TAMPER_OR_NONCANONICAL")},"This protects package integrity, not a complete evidence lifecycle."))
    # 11. Existing R1 Engine carries a native-to-legacy method context strength.
    root=R1/"fixtures";m=json.loads((root/"method-begin.json").read_text());s=json.loads((root/"study-begin.json").read_text());ed=json.loads((root/"data.json").read_text())["engine_data"]
    st={k:s[k] for k in ("id","version","method_ref","data_ref","contract_ref","parameters","status")};st["schema"]="profile-r1"
    bad=copy.deepcopy(ed);bad["pairs"][0]["alternative_snapshot"]="other:snapshot"
    r.append(control("ABL11","Break exogeneity of original paired method dataset",{"original_R1_profile_engine":reject(lambda:Engine(m,st,bad),"COUNTERFACTUAL_EXOGENEITY"),"M3":"Current arithmetic package has no typed counterfactual pair context"},"The compared M2 arithmetic adapter also does not yet carry full pair context; strength lies in original R1 profile machinery."))
    # 12. Matched M2/M3 negative numeric output, independently derived service mutation.
    a=copy.deepcopy(cc["RC02"]);data=copy.deepcopy(a["data"])
    for row,v in zip(data["parameters"]["delivered"],a["negative"]["values"],strict=True):row["value"]=v
    n=FiniteNative(open_(a),data);m=map_profile(a,prog(a),data)
    assert n.outputs()==m["outputs"]=={"outside":["0","0"],"received":["1/200","1/200"]}
    assert n.conditions()["service"] is False
    doc=frozen("RC02");doc["synthetic_data"]["observed"]["delivered"]=[["5","0"],["2","3"]]
    r.append(control("ABL12","Equal fleet total but unmet individual EV deadline",{"both_numeric_outputs":n.outputs(),"M3_service_predicate":False,"M2_legacy_profile_predicate":"NOT_EXECUTED","independent_oracle":reject(lambda:oracles.run(doc),"EV_SERVICE")},"Same finite arithmetic; M2 still needs separate obligation evaluation."))
    # Code metrics are raw inspected source, never equal-scope savings.
    paths=[Path(__file__).parent/"legacy_comparison.py",Path(__file__).parent/"native_consumer.py",ROOT/"canonical_closure"/"closure.py",ROOT/"canonical_closure"/"package_interface.py",R1/"n1r.py",R1/"pinned"/"profile_engine.py"]
    metrics=[{"path":str(p.relative_to(ROOT.parent)),"nonblank_noncomment_lines":sum(bool(l.strip()) and not l.lstrip().startswith("#") for l in p.read_text().splitlines())} for p in paths]
    print("C1_COMP_ABLATION="+json.dumps({"schema":"c1-comp-ablation-0.1","controls":r,"source_metrics":metrics,"scope":"12 independent additional control identities; raw file size not equivalent-scope LOC savings"},separators=(",",":")))
if __name__=="__main__":main()
