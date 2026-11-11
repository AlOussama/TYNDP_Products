"""Executable, re-generable machine-readable M2-MA1 gate artifact witness."""
import json
from tyndp_reduce.m2.fixture_witness import generate
from tyndp_reduce.m2.physical import ReferenceFlowCache


def test_gate_witness_generation_and_frozen_hashes(tmp_path):
    out=tmp_path/"ma1"
    result=generate(out)
    assert result["basis"]=="ONLY_SYNTHETIC_FIXTURE"
    assert result["real_network_qualification"]=="BLOCKED_DATA"
    assert all(str(v).startswith("PASS_SYNTHETIC") for k,v in result["gates"].items()
               if k in ("G01","G02","G03","G04","G05","G11_PART"))
    expected={"gate_witness.json","preflight_ledger.json","reference_flow_cache.json",
              "country_busmap.json","annual_overload.json","oriented_projection.json"}
    assert {p.name for p in out.iterdir()}==expected
    witness=json.loads((out/"gate_witness.json").read_text())
    assert witness["reference_cache_sha256"]==result["reference_cache_sha256"]
    cache=ReferenceFlowCache.from_file(out/"reference_flow_cache.json",
                                      expected_sha256=result["reference_cache_sha256"])
    assert cache.payload()["schema"]=="M2_ReferenceFlowCache_v1"
