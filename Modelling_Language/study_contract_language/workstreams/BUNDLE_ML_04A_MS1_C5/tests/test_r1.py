"""C5-R1 executed adversarial controls against the native mathspec-backed profile.
Fixture keys are ephemeral; no owner or independently authored review is claimed."""
import copy,json,sys,unittest,subprocess
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
import vmodel as vm
from closure import Reject,canon,digest
from closure_v1 import definition,metadata,composition
import r1_semantics as r1
from cba_reference import build,variant,claim,requirement,metric,test,TEST,REVIEW,SYSTEM,STUDY,METRIC,SCOPE,SOURCE
from research_assembly import frame,source_row,sig,source_for_slot,make_slot,bundle,to_definition,to_instance,repin,assertion,fixture,q,dataset,scalar,pkg

def run(d,i):return vm.instantiate(d,digest(d),i,digest(i))
def reb(d,i):
    i["base"]["definition_ref"]=definition.admit(d["base"],digest(d["base"]))["semantic_identity"]
    i["definition_ref"]=vm.admit(d,digest(d))["semantic_identity"]
def add_requirement(d,i,identifier,target,method,scope=SCOPE,metric_target=None,kind="VERIFICATION"):
    m=metric("metric:"+identifier,"VERIFICATION" if kind=="VERIFICATION" else "VALIDATION","Synthetic check",metric_target or target)
    a=requirement("requirement:"+identifier,"SYSTEM" if kind=="VERIFICATION" else "STUDY","Explicit controlled requirement",[STUDY] if kind=="VERIFICATION" else [],[target],[m["id"]])
    a.update(scope=scope,normativity="RESEARCH_ASSUMPTION",refinement_policy="DIRECT_AND_CHILDREN",depends_on=[])
    t=test("test:"+identifier,kind,[a["id"]],m["id"],target,method)
    t["scope"]=scope
    targets=r1.extra_targets(d["base"],vm.targets(d["base"]))
    inputs=r1.input_population(d["base"],targets[target])
    external=method in r1.EXTERNAL
    t.update(input_refs=sorted(inputs or []),preconditions=[],procedure_ref=SOURCE,reviewer_refs=[s["id"] for s in d["base"]["sources"] if s["id"].startswith("reviewer:")] if external else [],applicability={"slot":None,"guard":{"truth":"TRUE","reason":None}},coverage="EXTERNAL_SCOPE" if external else "ALL_DECLARED_SUPPORT",evidence="EXTERNAL_REVIEW_RECEIPT" if external else "COMPUTED_NATIVE_RECEIPT")
    d["requirements"].append(a);d["metrics"].append(m);d["tests"].append(t);i["requested_tests"].append(t["id"])
    return a,m,t

def row(id,key,val):return {"key":key,"value":val}
def base_graph(variant="cross",bad=False,unrelated=False):
    f=frame();src=[source_row(SOURCE,"fixture:source","Synthetic native verification oracle.")]
    if variant=="cross":
        f["domains"]=[{"id":"domain:s","kind":"scenario","members":["s1","s2"],"ordered":False}]
        f["scopes"]=[{"id":SCOPE,"domains":["domain:s"],"subjects":[]}]
        qty=q("EUR","currency","EUR:real:2025")
        f["inputs"]=[sig("input:a",qty,["domain:s"]),sig("input:expected",qty,["domain:s"])]
        f["outputs"]=[sig("output:mid",qty,["domain:s"],contribution_policy="NOT_REQUIRED"),sig("output:residual",qty,["domain:s"],contribution_policy="NOT_REQUIRED")]
        doc={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{"a":{"dims":["s"]}},"expressions":{"v":"a*2"}}
        c=fixture(doc,quant={"a":qty,"v":qty},roles={"a":"INPUT"},domains={"s":["s1","s2"]})
        p1=make_slot(f,source_for_slot(f,src,"first"),"first",doc,c,dataset({"a":[row("",["s1"],3),row("",["s2"],4)]}),{"ref:a":{"kind":"INPUT","ref":"input:a"},"ref:v":{"kind":"OUTPUT","ref":"output:mid"}},["input:a"],[],["output:mid"],["ref:v"])
        cond="expected == expected" if unrelated else "b == expected"
        doc={"version":0,"dimensions":{"s":{"dtype":"str"}},"parameters":{n:{"dims":["s"]} for n in ("b","expected")},"expressions":{"residual":"b-expected"},"conditions":{"ok":cond}}
        c=fixture(doc,quant={n:qty for n in ("b","expected","residual")},roles={"b":"INPUT","expected":"INPUT"},domains={"s":["s1","s2"]},pred_axes={"ok":["s"]})
        a=assertion(pkg(doc,c),"assertion:cross","ok",["domain:s"],["scenario"])
        p2=make_slot(f,source_for_slot(f,src,"second"),"second",doc,c,dataset({"b":[row("",["s1"],6),row("",["s2"],8)],"expected":[row("",["s1"],6),row("",["s2"],7 if bad else 8)]}),{"ref:b":{"kind":"UPSTREAM","ref":"output:mid"},"ref:expected":{"kind":"INPUT","ref":"input:expected"},"ref:residual":{"kind":"OUTPUT","ref":"output:residual"}},["output:mid","input:expected"],[],["output:residual"],["ref:residual"],assertions=[a],depends=["process:first"])
        x,_=bundle(f,[p1,p2],src)
    elif variant=="policy":
        f["domains"]=[{"id":"domain:t","kind":"time","members":[0,1],"ordered":True},{"id":"domain:s","kind":"scenario","members":["a","b"],"ordered":False}]
        f["chronologies"]=[{"id":"chronology:t","domain":"domain:t","mode":"NONCYCLIC","authority_refs":[SOURCE],"intervals":[{"label":i,"start_h":i,"end_h":i+1,"duration_h":1} for i in range(2)]}]
        f["information_sets"]=[{"id":"info:"+str(i),"time_domain":"domain:t","stage":i,"scenario_domain":"domain:s","partition":[["a","b"]] if i==0 else [["a"],["b"]]} for i in range(2)]
        f["scopes"]=[{"id":SCOPE,"domains":["domain:t","domain:s"],"subjects":[]}]
        f["inputs"]=[sig("input:decision",q(),["domain:s","domain:t"])]
        f["outputs"]=[sig("output:decision",q(),["domain:s","domain:t"],contribution_policy="NOT_REQUIRED")]
        doc={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True},"s":{"dtype":"str"}},"parameters":{"decision":{"dims":["s","t"]}},"expressions":{"v":"decision"}}
        c=fixture(doc,roles={"decision":"INPUT"},domains={"t":[0,1],"s":["a","b"]})
        data=dataset({"decision":[row("",[s,t],val) for s,vs in (("a",[10,20]),("b",[11 if bad else 10,30])) for t,val in enumerate(vs)]})
        p=make_slot(f,source_for_slot(f,src,"policy"),"policy",doc,c,data,{"ref:decision":{"kind":"INPUT","ref":"input:decision"},"ref:v":{"kind":"OUTPUT","ref":"output:decision"}},["input:decision"],[],["output:decision"],["ref:v"])
        p["policies"]=[{"id":"policy:decision","symbol":"ref:decision","time_domain":"domain:t","scenario_domain":"domain:s","authority_refs":[SOURCE]}]
        p["verification"].append({"id":"verification:policy","subject":"policy:decision","kind":"FINITE_OBSERVATION","oracle_ref":SOURCE,"status":"NOT_EXECUTED"})
        x,_=bundle(f,[p],src)
    elif variant=="state":
        f["domains"]=[{"id":"domain:t","kind":"time","members":[0,1],"ordered":True}]
        f["chronologies"]=[{"id":"chronology:t","domain":"domain:t","mode":"CYCLIC","authority_refs":[SOURCE],"intervals":[{"label":i,"start_h":i,"end_h":i+1,"duration_h":1} for i in range(2)]}]
        f["scopes"]=[{"id":SCOPE,"domains":["domain:t"],"subjects":[]}]
        qty=q("MWh","electricity")
        f["inputs"]=[sig("input:"+n,qty,["domain:t"] if n=="state" else []) for n in ("state","start","end")]
        f["outputs"]=[sig("output:state",qty,["domain:t"],contribution_policy="NOT_REQUIRED")]
        doc={"version":0,"dimensions":{"t":{"dtype":"int","ordered":True}},"parameters":{"state":{"dims":["t"]},"start":{"dims":[]},"end":{"dims":[]}},"expressions":{"v":"state"},"conditions":{"initial":"state == start","terminal":"state == end","cycle":"start == end"}}
        c=fixture(doc,quant={n:qty for n in ("state","start","end","v")},roles={n:"INPUT" for n in ("state","start","end")},domains={"t":[0,1]},pred_axes={"initial":["t"],"terminal":["t"],"cycle":[]})
        pp=pkg(doc,c)
        aa=[assertion(pp,"assertion:"+n,n,["domain:t"],["time"],at={"domain:t":[j]}) for n,j in (("initial",0),("terminal",1))]
        aa.append(assertion(pp,"assertion:cycle","cycle",[],[]))
        data=dataset({"state":[row("",[0],1),row("",[1],3 if bad else 1)],"start":scalar(1),"end":scalar(3 if bad else 1)})
        b={ "ref:"+n:{"kind":"INPUT","ref":"input:"+n} for n in ("state","start","end")};b["ref:v"]={"kind":"OUTPUT","ref":"output:state"}
        p=make_slot(f,source_for_slot(f,src,"state"),"state",doc,c,data,b,["input:state","input:start","input:end"],[],["output:state"],["ref:v"],assertions=aa)
        p["states"]=[{"id":"state:ledger","symbol":"ref:state","time_domain":"domain:t","mode":"CYCLIC","initial":"assertion:initial","terminal":"assertion:terminal","cycle":{"assertion":"assertion:cycle","initial_value":"ref:start","terminal_value":"ref:end"},"authority_refs":[SOURCE]}]
        p["verification"].append({"id":"verification:state","subject":"state:ledger","kind":"FINITE_OBSERVATION","oracle_ref":SOURCE,"status":"NOT_EXECUTED"})
        x,_=bundle(f,[p],src)
    else:raise ValueError(variant)
    b,bp=to_definition(x);i=to_instance(x,b,bp)
    return b,i

class R1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=TemporaryDirectory();p=Path(cls.tmp.name);cls.keys=[];cls.sources=[]
        for j in range(2):
            key=p/f"key{j}.pem"
            subprocess.run(["openssl","genpkey","-algorithm","ED25519","-out",str(key)],check=True,capture_output=True)
            public=subprocess.check_output(["openssl","pkey","-in",str(key),"-pubout"],text=True)
            cls.keys.append(key);cls.sources.append(source_row("reviewer:"+str(j),"fixture:ephemeral-reviewer:"+str(j),public))
        cls.old=build(numeric=True)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def migrate(self,d=None,i=None,n=1):
        if d is None:d,i=copy.deepcopy(self.old)
        return vm.migrate_r1(d,digest(d),i,digest(i),self.sources[:n])
    def sign(self,d,i,tid=REVIEW,j=0,verdict="PASS",alter=None,key=None):
        rr=run(d,i);t=next(t for t in d["tests"] if t["id"]==tid)
        art="Synthetic test report. This demonstrates signature and binding, not independent review."
        p={"test":tid,"test_version":t["version"],"definition_pin":digest(d),"base_instance_pin":digest(i["base"]),"run_id":i["run_id"],"reviewer_ref":"reviewer:"+str(j),"method_identities":rr["native_receipt"]["result"]["definition"]["method_identities"],"criterion":t["criterion"],"verdict":verdict,"observed":"Synthetic reviewer judgment: "+verdict,"artifact":art,"artifact_sha256":sha256(art.encode()).hexdigest(),"coverage":r1.scope_signature(metadata.validate(d["base"]["frame"]),t["scope"]),"data_identities":r1.native_inputs(t,rr["native_receipt"])}
        if alter:alter(p)
        r={"id":"attestation:"+tid.split(":")[-1]+":"+str(j),"version":"1","payload":p}
        with TemporaryDirectory() as tmp:
            f=Path(tmp)/"m";f.write_bytes(canon(r).encode())
            sig=subprocess.check_output(["openssl","pkeyutl","-sign","-inkey",str(key or self.keys[j]),"-rawin","-in",str(f)])
        r["signature"]=sig.hex();return r
    def independent_native(self,kind="cross",bad=False,unrelated=False):
        b,bi=base_graph(kind,bad,unrelated)
        d={"schema":r1.DEF,"base":b,"requirements":[],"metrics":[],"tests":[]}
        i={"schema":r1.INST,"base":bi,"definition_ref":"","requested_tests":[],"run_id":"synthetic-"+kind,"claims":[],"attestations":[]}
        # A nonmandatory study root allows focused native controls without fabricating review.
        a=requirement(STUDY,"STUDY","Synthetic verification experiment",[],[],[],required=False)
        a.update(normativity="RESEARCH_ASSUMPTION",refinement_policy="DIRECT_AND_CHILDREN",depends_on=[]);d["requirements"].append(a)
        if kind=="cross":add_requirement(d,i,"cross","assertion:cross","NATIVE_ASSERTION",metric_target="output:mid")
        if kind=="policy":add_requirement(d,i,"policy","policy:decision","NATIVE_POLICY")
        if kind=="state":add_requirement(d,i,"state","state:ledger","NATIVE_STATE")
        reb(d,i);return d,i
    def test_r1_01_migration_preserves_legacy(self):
        d,i=copy.deepcopy(self.old);before=run(d,i);i["claims"].append(claim(d,i,"PASS"))
        nd,ni,receipt=self.migrate(d,i)
        self.assertEqual(receipt["discarded_claim_ids"],["claim:one"]);self.assertEqual(ni["claims"],[])
        self.assertEqual(run(d,dict(i,claims=[])),before)
        self.assertEqual(run(nd,ni)["tests"][TEST]["verdict"],"PASS")
        self.assertEqual(run(nd,ni)["requirements"][STUDY]["status"],"NOT_EXECUTED")
        self.assertNotEqual(digest(nd),digest(d))
    def test_r1_02_per_requirement_metric_coverage(self):
        d,i,_=self.migrate();a=copy.deepcopy(d["requirements"][1]);a["id"]="requirement:other";a["metric_refs"].append("metric:benchmark");d["requirements"].append(a)
        d["tests"][0]["requirements"].append(a["id"])
        with self.assertRaisesRegex(Reject,"R1_REQUIREMENT_METRIC_COVERAGE"):vm.admit(d,digest(d))
        d,i,_=self.migrate();next(x for x in d["tests"] if x["id"]==REVIEW)["input_refs"]=[]
        with self.assertRaisesRegex(Reject,"R1_STUDY_METRIC_VALIDATION_COVERAGE"):vm.admit(d,digest(d))
    def test_r1_03_orphan_metric_and_normativity(self):
        d,i,_=self.migrate();m=copy.deepcopy(d["metrics"][0]);m["id"]="metric:orphan";d["metrics"].append(m)
        with self.assertRaisesRegex(Reject,"R1_ORPHAN_METRIC"):vm.admit(d,digest(d))
        d,i,_=self.migrate();d["requirements"][1]["normativity"]="INFORMATIVE"
        with self.assertRaisesRegex(Reject,"R1_INFORMATIVE_REQUIRED"):vm.admit(d,digest(d))
    def test_r1_04_scope_refinement_external_report(self):
        d,i,_=self.migrate();f=d["base"]["frame"]
        f["scopes"].append({"id":"scope:child","domains":["domain:s"],"subjects":["case:P"]})
        rpt={"id":"report:external","subject":"case:P","value_type":"QUALITATIVE","declared_unit":None,"basis":"SYNTHETIC_PROCEDURE","oracle_ref":SOURCE,"authority_refs":[SOURCE]}
        f["report_requests"].append(rpt);i["base"]["reports"].append({"id":rpt["id"],"status":"NOT_EXECUTED","reason":"EXTERNAL_PENDING","value":None,"source_ref":SOURCE})
        a,m,t=add_requirement(d,i,"external","report:external","EXTERNAL_PROCEDURE","scope:child")
        t["input_refs"]=["observable:P"];reb(d,i)
        i["attestations"]=[self.sign(d,i,t["id"]),self.sign(d,i)]
        rr=run(d,i);self.assertEqual(rr["tests"][t["id"]]["verdict"],"PASS");self.assertEqual(rr["requirements"][STUDY]["status"],"PASS")
        next(x for x in d["requirements"] if x["id"]==SYSTEM)["scope"]="scope:child"
        with self.assertRaisesRegex(Reject,"R1_TARGET_SCOPE"):vm.admit(d,digest(d))
    def test_r1_05_scope_axis_and_decomposition(self):
        d,i,_=self.migrate()
        f=d["base"]["frame"];f["scopes"].append({"id":"scope:projected","domains":[],"subjects":["case:R","case:P"]})
        d["requirements"][1]["scope"]="scope:projected"
        with self.assertRaisesRegex(Reject,"R1_TARGET_SCOPE"):vm.admit(d,digest(d))
        d,i,_=self.migrate()
        d["requirements"][1]["refinement_policy"]="COMPLETE_SUBJECT_COVERAGE"
        with self.assertRaisesRegex(Reject,"R1_DECOMPOSITION_COVERAGE"):vm.admit(d,digest(d))
        d,i,_=self.migrate();d["requirements"][0]["refinement_policy"]="COMPLETE_SUBJECT_COVERAGE";reb(d,i)
        self.assertEqual(run(d,i)["requirements"][STUDY]["status"],"NOT_EXECUTED")
    def test_r1_06_signed_external_positive(self):
        d,i,_=self.migrate();i["attestations"]=[self.sign(d,i)];rr=run(d,i)
        self.assertEqual(rr["requirements"][STUDY]["status"],"PASS")
        self.assertEqual(rr["tests"][REVIEW]["verdict"],"PASS")
        e=next(x for x in rr["evidence"] if x["test"]==REVIEW)
        self.assertEqual(e["observed"]["verified_attestations"][0]["signature_status"],"VERIFIED_PINNED_KEY")
        self.assertEqual(e["independence"],"UNVERIFIED");self.assertEqual(rr["contract_conformance"],"NOT_PROVED")
    def test_r1_07_external_negative_and_unsupported_claim(self):
        d,i,_=self.migrate()
        i["claims"]=[dict(claim(d,i,"PASS"),test=REVIEW)]
        self.assertEqual(run(d,i)["tests"][REVIEW]["verdict"],"NOT_EXECUTED")
        i["claims"]=[];i["attestations"]=[self.sign(d,i,verdict="FAIL")]
        self.assertEqual(run(d,i)["requirements"][STUDY]["status"],"FAIL")
    def test_r1_08_tamper_signature(self):
        d,i,_=self.migrate();a=self.sign(d,i);a["payload"]["verdict"]="FAIL";i["attestations"]=[a]
        with self.assertRaisesRegex(Reject,"R1_EXTERNAL_SIGNATURE"):run(d,i)
        i["attestations"]=[self.sign(d,dict(i,attestations=[]),key=self.keys[1])]
        with self.assertRaisesRegex(Reject,"R1_EXTERNAL_SIGNATURE"):run(d,i)
    def test_r1_09_stale_coverage_and_artifact(self):
        d,i,_=self.migrate()
        for code,alter in [("R1_ATTESTATION_STALE",lambda p:p.update(run_id="wrong")),("R1_ATTESTATION_COVERAGE",lambda p:p["coverage"]["subjects"].clear()),("R1_ATTESTATION_ARTIFACT",lambda p:p.update(artifact="changed")),("R1_ATTESTATION_DATA_DRIFT",lambda p:p["data_identities"].update({"output:benefit":"0"*64}))]:
            a=self.sign(d,dict(i,attestations=[]),alter=alter);i["attestations"]=[a]
            with self.assertRaisesRegex(Reject,code):run(d,i)
    def test_r1_10_multi_reviewer_conflict(self):
        d,i,_=self.migrate(n=2);i["attestations"]=[self.sign(d,i)]
        self.assertEqual(run(d,i)["tests"][REVIEW]["verdict"],"BLOCKED")
        i["attestations"].append(self.sign(d,i,j=1,verdict="FAIL"))
        self.assertEqual(run(d,i)["tests"][REVIEW]["verdict"],"INCONCLUSIVE")
    def test_r1_11_no_role_or_key_alias(self):
        d,i,_=self.migrate(n=2);t=next(t for t in d["tests"] if t["id"]==REVIEW);t["reviewer_refs"]=[SOURCE]
        with self.assertRaisesRegex(Reject,"R1_REVIEWER_ROLE_COLLISION"):vm.admit(d,digest(d))
        d,i,_=self.migrate(n=2);s=next(x for x in d["base"]["sources"] if x["id"]=="reviewer:1");s["content"]=self.sources[0]["content"];s["sha256"]=self.sources[0]["sha256"]
        with self.assertRaisesRegex(Reject,"R1_DUPLICATE_REVIEWER_KEY"):vm.admit(d,digest(d))
    def test_r1_12_required_child_failure_dominates(self):
        d,i,_=self.migrate(*build(numeric=True,expected=[15,21]))
        i["attestations"]=[self.sign(d,i)]
        rr=run(d,i);self.assertEqual(rr["requirements"][STUDY]["local_status"],"PASS");self.assertEqual(rr["requirements"][STUDY]["status"],"FAIL")
        self.assertEqual(rr["tests"]["test:benchmark"]["verdict"],"FAIL")
    def test_r1_13_native_counterexample_not_erased(self):
        d,i,_=self.migrate(*variant("weather"));i["claims"]=[claim(d,i,"PASS")]
        self.assertEqual(run(d,i)["tests"][TEST]["verdict"],"FAIL")
    def test_r1_14_cross_slot_dependency(self):
        for bad in (False,True):
            d,i=self.independent_native("cross",bad)
            rr=run(d,i);self.assertEqual(rr["tests"]["test:cross"]["verdict"],"FAIL" if bad else "PASS")
            ev=next(x for x in rr["evidence"] if x["test"]=="test:cross")
            self.assertIn("output:mid",ev["input_identities"])
        with self.assertRaisesRegex(Reject,"R1_METRIC_CRITERION_DEPENDENCY"):self.independent_native("cross",unrelated=True)
    def test_r1_15_explicit_input_and_precondition(self):
        d,i,_=self.migrate();t=next(t for t in d["tests"] if t["id"]==TEST);t["input_refs"].pop()
        with self.assertRaisesRegex(Reject,"R1_TEST_INPUT_COVERAGE"):vm.admit(d,digest(d))
        d,i,_=self.migrate(*build(numeric=True,expected=[15,21]));t=next(t for t in d["tests"] if t["id"]==TEST)
        t["preconditions"]=["assertion:benchmark"];reb(d,i)
        self.assertEqual(run(d,i)["tests"][TEST]["verdict"],"BLOCKED")
    def test_r1_16_native_point_coverage(self):
        d,i,_=self.migrate();r=run(d,i);ev=next(e for e in r["evidence"] if e["test"]=="test:benchmark")
        self.assertEqual(ev["observed"]["coverage"]["expected"],2);self.assertEqual(ev["observed"]["coverage"]["applicable"],2)
        d,i,_=self.migrate(*build(numeric=True,guard={"truth":"FALSE","reason":None}))
        rr=run(d,i);self.assertEqual(rr["requirements"]["requirement:benchmark"]["status"],"NOT_APPLICABLE")
        d,i,_=self.migrate(*build(numeric=True,guard={"truth":"UNKNOWN","reason":"MISSING_DATA"}))
        self.assertEqual(run(d,i)["tests"]["test:benchmark"]["verdict"],"INCONCLUSIVE")
    def test_r1_17_native_policy(self):
        for bad in (False,True):
            d,i=self.independent_native("policy",bad)
            self.assertEqual(run(d,i)["tests"]["test:policy"]["verdict"],"FAIL" if bad else "PASS")
    def test_r1_18_native_state(self):
        for bad in (False,True):
            d,i=self.independent_native("state",bad)
            rr=run(d,i);self.assertEqual(rr["tests"]["test:state"]["verdict"],"FAIL" if bad else "PASS")
    def test_r1_19_native_data_quality(self):
        d,i=self.independent_native();add_requirement(d,i,"quality","input:a","NATIVE_DATA_QUALITY");reb(d,i)
        self.assertEqual(run(d,i)["tests"]["test:quality"]["verdict"],"PASS")
        i["base"]["slots"][0].update(data_status="MISSING_DATA",data=None,snapshot_digest=None,witnesses=[],contributions=[],expected_events={})
        self.assertEqual(run(d,i)["tests"]["test:quality"]["verdict"],"BLOCKED")
    def test_r1_20_precise_native_types(self):
        for qty in (q("MW","electricity"),q("EUR","currency","EUR:real:2020")):
            with self.assertRaisesRegex(Reject,"COMPARISON_TYPE"):build(numeric=True,quant_expected=qty)
    def test_r1_21_roundtrip_signed_and_order(self):
        d,i,_=self.migrate();i["attestations"]=[self.sign(d,i)]
        dp,ip=digest(d),digest(i);canonical=vm.export(d,dp,i,ip)
        self.assertEqual(vm.reimport(canonical,dp,ip)["receipt"],run(d,i))
        a,b=[vm.evaluate_source(raw,k,sha256(raw).hexdigest(),dp,ip) for k in ("A","B") for raw in [vm.emit_control(d,i,k)]]
        self.assertEqual(a["package_sha256"],b["package_sha256"]);self.assertNotEqual(a["audit_identity"],b["audit_identity"])
        d2=copy.deepcopy(d);d2["requirements"].reverse();d2["tests"].reverse();d2["tests"][0]["input_refs"].reverse()
        self.assertEqual(vm.admit(d2,digest(d2))["semantic_identity"],vm.admit(d,dp)["semantic_identity"])
        self.assertNotEqual(digest(d2),dp)
        with self.assertRaisesRegex(Reject,"C5_INSTANCE_PIN"):vm.instantiate(d,dp,i,"0"*64)
        out=HERE/"generated";out.mkdir(exist_ok=True)
        for k in ("A","B"):(out/("r1-signed."+k+".txt")).write_bytes(vm.emit_control(d,i,k))
        (out/"r1-signed.canonical.json").write_text(canonical)
    def test_r1_22_nine_native_cba_variants(self):
        out=HERE/"generated";out.mkdir(exist_ok=True)
        for name,want in (("consistent","PASS"),("weather","FAIL"),("demand","FAIL"),("missing_scenario","BLOCKED"),("allowed_project","PASS"),("extra_network","FAIL"),("price_basis","FAIL"),("missing_evidence","NOT_EXECUTED"),("math_correct_invalid","FAIL")):
            d,i,_=self.migrate(*variant(name));r=run(d,i)
            self.assertEqual(r["tests"][TEST]["verdict"],want)
            dp,ip=digest(d),digest(i);a,b=[vm.evaluate_source(raw,k,sha256(raw).hexdigest(),dp,ip) for k in ("A","B") for raw in [vm.emit_control(d,i,k)]]
            self.assertEqual(a["package_sha256"],b["package_sha256"])
            for k in ("A","B"):(out/("r1-"+name+"."+k+".txt")).write_bytes(vm.emit_control(d,i,k))
            (out/("r1-"+name+".canonical.json")).write_text(vm.export(d,dp,i,ip))
            print("R1_VARIANT="+json.dumps({"id":name,"actual":r["tests"][TEST]["verdict"],"expected":want,"package_sha256":a["package_sha256"],"overall":r["contract_conformance"]},sort_keys=True))
    def test_r1_23_metamodel_schema(self):
        # The structural schema must match both wire versions. jsonschema is
        # supplied in CI only if present; semantic checks are always native.
        d,i,_=self.migrate();p=json.loads(vm.export(d,digest(d),i,digest(i)))
        schema=json.loads((HERE/"specification"/"final_schema.json").read_text())
        self.assertEqual(schema["oneOf"][1]["properties"]["schema"]["const"],r1.PACKAGE)
        out=HERE/"generated";out.mkdir(exist_ok=True)
        (out/"schema-valid-r1.json").write_text(json.dumps(p))
        d,i=self.old;(out/"schema-valid-c5.json").write_text(vm.export(d,digest(d),i,digest(i)))
        p["definition"]["tests"][0].pop("input_refs")
        (out/"schema-invalid-r1.json").write_text(json.dumps(p))

    def test_r1_24_requirement_dependency_and_cycle(self):
        d,i,_=self.migrate(*build(numeric=True,expected=[15,21]))
        a=next(x for x in d["requirements"] if x["id"]==SYSTEM);a["depends_on"]=["requirement:benchmark"];reb(d,i)
        rr=run(d,i);self.assertEqual(rr["requirements"][SYSTEM]["local_status"],"PASS");self.assertEqual(rr["requirements"][SYSTEM]["status"],"BLOCKED")
        a["depends_on"]=[STUDY]
        with self.assertRaisesRegex(Reject,"R1_REQUIREMENT_DEPENDENCY_CYCLE"):vm.admit(d,digest(d))
    def test_r1_25_explicit_test_applicability(self):
        d,i,_=self.migrate();t=next(x for x in d["tests"] if x["id"]==REVIEW)
        t["applicability"]={"slot":None,"guard":{"truth":"FALSE","reason":None}};reb(d,i)
        rr=run(d,i);self.assertEqual(rr["tests"][REVIEW]["applicability"],"FALSE");self.assertEqual(rr["tests"][REVIEW]["execution"],"NOT_EXECUTED")
        t["applicability"]["guard"]={"truth":"UNKNOWN","reason":"MISSING_DATA"};reb(d,i)
        self.assertEqual(run(d,i)["tests"][REVIEW]["verdict"],"INCONCLUSIVE")
        t["applicability"]={"slot":"slot:benefit","guard":{"truth":"TRUE","reason":None}}
        t["input_refs"]=sorted(set(t["input_refs"])|set(next(s for s in d["base"]["frame"]["slots"] if s["id"]=="slot:benefit")["inputs"]+next(s for s in d["base"]["frame"]["slots"] if s["id"]=="slot:benefit")["observables"]))
        reb(d,i);i["attestations"]=[self.sign(d,i)];rr=run(d,i)
        self.assertEqual(rr["tests"][REVIEW]["verdict"],"PASS")
        self.assertEqual(rr["study_metrics"][METRIC]["status"],"COMPUTED_WITH_PINNED_VALIDATION_ATTESTATION")
    def test_r1_26_context_data_quality(self):
        d,i,_=self.migrate();a,m,t=add_requirement(d,i,"weather-quality","context:R:weather","NATIVE_DATA_QUALITY");reb(d,i)
        self.assertEqual(t["input_refs"],["context:R:weather"])
        self.assertEqual(run(d,i)["tests"][t["id"]]["verdict"],"PASS")
        i["base"]["context_data"]["context:R:weather"].pop()
        self.assertEqual(run(d,i)["tests"][t["id"]]["verdict"],"BLOCKED")
    def test_r1_27_requirement_revision_authorization(self):
        d,i,_=self.migrate();n,ni=copy.deepcopy((d,i));n["requirements"][1]["statement"]+=" Revised research wording."
        with self.assertRaisesRegex(Reject,"R1_REVISION_VERSION_REQUIRED"):r1.revision_changes(d,n)
        n["requirements"][1]["version"]="2";reb(n,ni)
        changes=r1.revision_changes(d,n);src=next(x for x in d["base"]["sources"] if x["id"]==SOURCE)
        a={"schema":"c5-r1-revision-authorization-0.1","base_ref":digest(d),"proposed_ref":digest(n),"changes":changes,"authority_ref":SOURCE,"source_sha256":src["sha256"],"decision":"APPROVED_RESEARCH_REVISION","reason":"Synthetic research revision"}
        with self.assertRaisesRegex(Reject,"R1_REVISION_AUTHORIZATION"):vm.revise_requirements(d,digest(d),n,digest(n),a,"0"*64)
        r=vm.revise_requirements(d,digest(d),n,digest(n),a,digest(a));self.assertEqual(r["changes"],changes)
        with self.assertRaisesRegex(Reject,"C5_INSTANCE_PIN"):run(n,i)
        self.assertEqual(run(n,ni)["tests"][TEST]["verdict"],"PASS")
    def test_r1_28_original_normativity_migration(self):
        d,i=copy.deepcopy(self.old);d["requirements"][1]["source_kind"]="ORIGINAL_SOURCE";reb(d,i)
        with self.assertRaisesRegex(Reject,"R1_MIGRATION_NORMATIVITY_REQUIRED"):self.migrate(d,i)
        n,ni,_=vm.migrate_r1(d,digest(d),i,digest(i),self.sources[:1],{SYSTEM:"NORMATIVE_REQUIREMENT_PENDING_OWNER"})
        self.assertEqual(n["requirements"][1]["normativity"],"NORMATIVE_REQUIREMENT_PENDING_OWNER")
        self.assertEqual(run(n,ni)["owner"],"OWNER_TBD")
    def test_r1_29_duplicate_evidence_id(self):
        d,i,_=self.migrate();a=self.sign(d,i);a["id"]=TEST;i["attestations"]=[a]
        with self.assertRaisesRegex(Reject,"R1_EVIDENCE_ID_COLLISION"):run(d,i)

if __name__=="__main__":unittest.main(verbosity=2)
