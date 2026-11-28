"""Native bounded discount extension of CL24; original P5 oracle remains external.
This is a numerical projection, not full original P5 A/B authoring, governance,
event-lineage or model conformity evidence.
"""
import json,sys,math
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
C2=ROOT/"BUNDLE_ML_04A_MS1_C2"
sys.path.insert(0,str(C2))
from interface import finite_consumer,import_package
from WS_B import affine_boundary
from test_closure import fixture,q,dataset,scalar

def main(oracle_path):
    p=C2/"closure_v1"/"p5_fixture.json"
    raw=p.read_bytes()
    source=json.loads(raw)
    oracle=json.loads(Path(oracle_path).read_text())
    assert oracle["passed"]==oracle["total"],"ORIGINAL_ORACLE_FAILURE"
    expected=oracle["baseline"]["synthetic_numeric_results"]
    labels=[s["id"] for s in source["scenarios"]]
    econ=source["economics"];h=econ["horizon_years"]
    assert type(h) is int and 1<=h<=100
    years=list(range(1,h+1))
    receipt=[]
    money=q("EUR","currency","EUR:real:2025")
    for model in source["models"]:
        mid=model["id"]
        sample={(s["scenario_id"],s["case_id"]):s for s in source["samples"] if s["model_id"]==mid}
        # Annual rates are projected to amounts for one year, as in CL24.
        # Repetition of the same annual amount each year is exactly the
        # original independent illustrative discounting convention.
        def amounts(case):
            return [{"key":[sid],"value":str(sample[sid,case]["operating_cost_proxy_eur_per_year"])} for sid in labels]
        doc={"version":0,"dimensions":{"s":{"dtype":"str"},"y":{"dtype":"int","ordered":True}},
             "parameters":{"baseline":{"dims":["s"]},"project":{"dims":["s"]},"prob":{"dims":["s"]},
                           "rate":{"dims":[]},"year":{"dims":["y"],"dtype":"int"},
                           "capex":{"dims":[]},"threshold":{"dims":[]}},
             "expressions":{"annual":"sum((baseline-project)*prob, over=s)",
                            "pv_factor":"sum((1 + rate)**(-year), over=y)",
                            "npv":"annual * pv_factor - capex"},
             "conditions":{"positive":"npv > threshold","negative":"npv < threshold","neutral":"npv == threshold"}}
        ctx=fixture(doc,quant={n:money for n in ("baseline","project","capex","threshold","annual","npv")},
                    roles={n:"INPUT" for n in doc["parameters"]},
                    domain_rules={"rate":"NONNEGATIVE","year":"POSITIVE"},
                    domains={"s":labels,"y":years},
                    pred_axes={n:[] for n in doc["conditions"]})
        ctx["power_domains"]={"year":{"min":1,"max":h}}
        data=dataset({"baseline":amounts(source["comparison"]["reference"]),
                      "project":amounts(source["comparison"]["project"]),
                      "prob":[{"key":[s["id"]],"value":str(s["weight"])} for s in source["scenarios"]],
                      "rate":scalar(str(econ["discount_rate"])),"year":[{"key":[y],"value":y} for y in years],
                      "capex":scalar(econ["capex_eur"]),"threshold":scalar(source["comparison"]["decision_threshold_eur"])})
        native_source=json.dumps(doc,sort_keys=True)
        package=affine_boundary.export_package(affine_boundary.admit(native_source,ctx))
        imported=import_package(package)
        assert affine_boundary.export_package(imported)==package
        consumer=finite_consumer(package,data)
        outputs=consumer.outputs();conditions=consumer.conditions()
        annual=Fraction(outputs["annual"][0]);npv=Fraction(outputs["npv"][0])
        decision=int(conditions["positive"])-int(conditions["negative"])
        assert sum(bool(v) for v in conditions.values())==1
        e=expected[mid]
        assert math.isclose(float(annual),e["illustrative_annual_cost_saving_eur"],rel_tol=0,abs_tol=1e-9)
        assert math.isclose(float(npv),e["illustrative_npv_proxy_eur"],rel_tol=0,abs_tol=1e-9)
        assert decision==e["decision_sign"],(mid,decision,e)
        receipt.append({"model":mid,"annual_exact":str(annual),"npv_exact":str(npv),"decision":decision,
                        "oracle":e,"native_source_sha256":sha256(native_source.encode()).hexdigest(),
                        "package_sha256":sha256(package.encode()).hexdigest(),
                        "data_sha256":sha256(json.dumps(data,sort_keys=True).encode()).hexdigest(),
                        "roundtrip":True})
    print("C3_P5_DISCOUNT_PROJECTION="+json.dumps({"scope":"NUMERICAL_PROJECTION_NOT_ORIGINAL_AB",
          "fixture_sha256":sha256(raw).hexdigest(),"oracle_blob":"ef2c7fa4ea4deab919f0c84ac7020aa1a32ff0a2",
          "owner":"OWNER_TBD","comparison_tolerance_eur":1e-9,"rows":receipt},sort_keys=True))

if __name__=="__main__":main(sys.argv[1])
