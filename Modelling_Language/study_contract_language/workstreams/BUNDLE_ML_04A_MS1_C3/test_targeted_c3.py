"""C3 targeted native semantic additions; original corpus credit requires separate sources."""
from pathlib import Path
import sys,json,unittest,copy
ROOT=Path(__file__).resolve().parents[1]
C2=ROOT/"BUNDLE_ML_04A_MS1_C2"
# Test public authoring import before any test helpers initialize the interface.
import authoring
sys.path.insert(0,str(C2/"closure_v1"))
from test_closure_v1 import (frame,source_row,sig,source_for_slot,make_slot,bundle,repin,
    to_definition,to_instance,assertion,fixture,q,dataset,pkg,digest,resolve_method,old_identities)
from closure_v1 import definition,metadata,obligations,diagnostics
from closure import Reject
from test_closure import scalar
from interface import finite_consumer

class Targeted(unittest.TestCase):
    def test_signed_charging_transfer(self):
        f=frame();src=[source_row("authority:source","fixture:source","Signed port P; charging magnitude -P, only P<=0")]
        f["scopes"]=[{"id":"scope:main","domains":[],"subjects":["port:grid"]}]
        power=q("MW","electricity");signed={**power,"sign":"INJECTION"}
        f["components"]=[{"id":"component:battery","kind":"storage","authority_refs":["authority:source"]}]
        f["ports"]=[{"id":"port:grid","component_ref":"component:battery","direction":"BIDIRECTIONAL","quantity":signed,"axes":[],"authority_refs":["authority:source"]}]
        f["observables"]=[sig("observable:p",signed,subject="port:grid",projection="IDENTITY")]
        f["inputs"]=[sig("input:charge",power),sig("input:dt",q("h"))]
        f["outputs"]=[sig("output:intake",q("MWh","electricity"),contribution_policy="NOT_REQUIRED")]
        doc={"version":0,"parameters":{n:{"dims":[]} for n in ("p","charge","dt")},
             "expressions":{"intake":"charge*dt"}}
        ctx=fixture(doc,quant={"p":signed,"charge":power,"dt":q("h"),"intake":q("MWh","electricity")},
                    roles={"charge":"INPUT","dt":"INPUT"})
        vals=dataset({"p":scalar("-2"),"charge":scalar("2"),"dt":scalar("1/2")})
        row=make_slot(f,source_for_slot(f,src,"charge"),"charge",doc,ctx,vals,
                {"ref:p":{"kind":"OBSERVABLE","ref":"observable:p"},"ref:charge":{"kind":"INPUT","ref":"input:charge"},
                 "ref:dt":{"kind":"INPUT","ref":"input:dt"},"ref:intake":{"kind":"OUTPUT","ref":"output:intake"}},
                ["input:charge","input:dt"],["observable:p"],["output:intake"],["ref:intake"])
        x,_=bundle(f,[row],src);d,dp=to_definition(x)
        cv={"kind":"SIGN_CONVENTION","source_quantity":signed,"source_observable":"observable:p",
            "factor":"-1","scope":"CHARGING_ONLY","source_ref":"authority:source"}
        contract=next(r for r in d["requirements"]["data_contracts"] if r["id"]=="input:charge");contract["conversion"]=cv
        dp=digest(d);i=to_instance(x,d,dp)
        rr=next(r for r in i["data_receipts"] if r["id"]=="input:charge");rr["raw_rows"]=scalar("-2")
        ip=digest(i);res=definition.instantiate(d,dp,i,ip)
        self.assertEqual(res["graph"]["outputs"]["output:intake"][0]["value"],"1")
        self.assertEqual(definition.reimport(definition.export(d,dp,i,ip),dp,ip)["receipt"],res)
        rr["raw_rows"]=scalar("-3")
        with self.assertRaisesRegex(Reject,"SIGN_CONVERSION_RAW_SOURCE_DRIFT"):definition.instantiate(d,dp,i,digest(i))
        with self.assertRaisesRegex(Reject,"SIGN_CONVERSION_CHARGING_SCOPE"):definition.converted_rows(scalar("2"),cv,power)
        cv["factor"]="1"
        with self.assertRaisesRegex(Reject,"SIGN_CONVERSION_POLICY"):definition.admit(d,digest(d))
        print("C3_SIGN_CONVERSION="+json.dumps({"intake":res["graph"]["outputs"]["output:intake"],"scope":"CHARGING_ONLY","original_paths":0}))

    def test_stage_information_without_duration(self):
        f=frame();f["domains"]=[{"id":"domain:t","kind":"stage","members":["t0","t1"],"ordered":True},
                 {"id":"domain:s","kind":"scenario","members":["s1","s2"],"ordered":False}]
        f["information_sets"]=[{"id":"info:0","time_domain":"domain:t","stage":"t0","scenario_domain":"domain:s","partition":[["s1","s2"]]},
                              {"id":"info:1","time_domain":"domain:t","stage":"t1","scenario_domain":"domain:s","partition":[["s1"],["s2"]]}]
        doc={"version":0,"dimensions":{"s":{"dtype":"str"},"t":{"dtype":"str","ordered":True}},
             "parameters":{"decision":{"dims":["s","t"]}}}
        ctx=fixture(doc,domains={"s":["s1","s2"],"t":["t0","t1"]})
        p=pkg(doc,ctx)
        rows=[{"key":[s,t],"value":v} for s,vs in (("s1",[10,12]),("s2",[10,8])) for t,v in zip(["t0","t1"],vs)]
        data=dataset({"decision":rows});policy=[{"id":"policy:decision","symbol":"ref:decision","time_domain":"domain:t","scenario_domain":"domain:s","authority_refs":["authority:source"]}]
        bound=obligations.Bound(p,metadata.validate(f),data)
        self.assertEqual(obligations.nonanticipativity(bound,policy)[0]["status"],"FINITE_OBSERVED_TRUE")
        rows[2]["value"]=11
        bound=obligations.Bound(p,metadata.validate(f),data)
        self.assertEqual(obligations.nonanticipativity(bound,policy)[0]["status"],"FINITE_COUNTEREXAMPLE")
        self.assertFalse(f["chronologies"])
        print("C3_STAGE_INFORMATION="+json.dumps({"valid":"FINITE_OBSERVED_TRUE","counterexample":"FINITE_COUNTEREXAMPLE","physical_durations":0}))

    def test_derived_typed_ratio(self):
        # A computed ratio is not a user-provided conversion factor.
        # Native expression typing must still prove the full carrier ratio.
        doc={"version":0,"parameters":{"a":{"dims":[]},"b":{"dims":[]}},"expressions":{"eta":"a/b"}}
        quant={"a":q("MW_H2_LHV","hydrogen","LHV"),"b":q("MW","electricity"),"eta":q("LHV_ratio","conversion","LHV")}
        ctx=fixture(doc,quant=quant,domain_rules={"b":"POSITIVE"})
        p=pkg(doc,ctx)
        self.assertEqual(finite_consumer(p,dataset({"a":scalar("20"),"b":scalar("30")})).outputs()["eta"],["2/3"])
        bad=copy.deepcopy(ctx);bad["symbols"]["eta"]["quantity"]=q()
        with self.assertRaisesRegex(Reject,"EXPRESSION_TYPE"):pkg(doc,bad)
        print("C3_DERIVED_RATIO="+json.dumps({"eta":"2/3","typed":"LHV_ratio","authority":"native Program"}))
if __name__=="__main__":unittest.main(verbosity=2)
