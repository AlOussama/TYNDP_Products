"""Actual admission probe for RC01 signed-grid-to-unsigned-storage boundary.
Not a full original path or an original expected verdict.
"""
import sys,json
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"BUNDLE_ML_04A_MS1_C2"))
from interface import finite_consumer
from closure import admit,Reject
from package_interface import export_package
from test_closure import q,fixture,dataset,scalar

def main():
    source=ROOT/"BUNDLE_ML_04A_MS1_C1"/"WS_B_original_reference_corpus"/"reference_cases"/"RC01"/"contract.json"
    raw=source.read_bytes();data=json.loads(raw)["synthetic_data"]["inputs"]
    # Preserve injection-positive port semantics. Negation changes numeric
    # value, not the native quantity convention; do not strip sign silently.
    mw=q("MW","electricity");mw["sign"]="INJECTION"
    signed=q("MWh","electricity");signed["sign"]="INJECTION"
    unsigned=q("MWh","electricity")
    doc={"version":0,"parameters":{"p":{"dims":[]},"dt":{"dims":[]}},
         "expressions":{"intake":"-p*dt"}}
    src=json.dumps(doc,sort_keys=True)
    s=fixture(doc,quant={"p":mw,"dt":q("h"),"intake":signed})
    p=export_package(admit(src,s))
    got=finite_consumer(p,dataset({"p":scalar(data["p"]),"dt":scalar(data["dt"])})).outputs()
    assert got["intake"]==["1"]
    u=fixture(doc,quant={"p":mw,"dt":q("h"),"intake":unsigned})
    try:
        admit(src,u)
    except Reject as e:
        print("C3_RC01_SIGN_GAP="+json.dumps({"scope":"NATIVE_ADMISSION_PROBE_NOT_ORIGINAL_AB","fixture_sha256":sha256(raw).hexdigest(),
             "native_source_sha256":sha256(src.encode()).hexdigest(),"signed_control":got["intake"],
             "candidate_stage":"NATIVE_ADMISSION","candidate_object":"expression:intake","actual_reason":str(e),
             "interpretation":"Numeric negation is not an explicit signed-flow to unsigned stock semantic conversion; no historical E1 verdict claimed."},sort_keys=True))
    else:
        raise AssertionError("Expected typed signed-to-unsigned boundary rejection; inspect policy before declaring closure")

if __name__=="__main__":main()
