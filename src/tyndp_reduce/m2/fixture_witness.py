"""Reproduce MA1 G01-G05/G11-part synthetic gate files without external data.

CLI: python -m tyndp_reduce.m2.fixture_witness --output m2_ma1_witness
All output is synthetic, *not* a 102-zone / European real-grid validation.
"""
import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from .contracts import (
    Evidence, Bus, ACBranch, HVDCTerminalPair, DetailedGridSnapshot,
    CountryZoneBudget, ReferenceDispatchSet, HVDCDispatch, NormalContingencyRatings,
    TimePoint, TimeSet,
)
from .country import load_official_budget, country_quota_busmap
from .physical import SparseACReference, _hash
from .preflight import preflight_ledger, save_ledger_once
from .projection import build_oriented_projection
from .screening import screen_annual_overload, protect_congested_union


def _ev(name):
    return Evidence("synthetic:"+name, "fixture-MA1-v1",
                    sha256(name.encode("utf-8")).hexdigest(), "2040")


def synthetic_reference():
    grid = DetailedGridSnapshot(
        _ev("grid"), 100.0,
        (Bus("a","Germany",220),Bus("b","Germany",220),
         Bus("c","Germany",225),Bus("d","France",400),Bus("e","France",400)),
        (ACBranch("ab","a","b",.2,220,"transformer"),
         ACBranch("bc","b","c",.1,225),
         ACBranch("de","d","e",.2,400)),
        (HVDCTerminalPair("dc","c","d"),),
        ties_110kv_complete=True,fixture=True)
    times=TimeSet(_ev("times"),("wyA","wyB"),
                  (TimePoint("t0","2020-01-01T00:00:00+00:00","wyA","summer",2.),
                   TimePoint("t1","2021-01-01T00:00:00+00:00","wyB","winter",3.)),
                  fixture=True)
    dispatch=ReferenceDispatchSet(
        _ev("dispatch"),("a","b","c","d","e"),("t0","t1"),
        ((20.,20.),(-10.,-10.),(0.,0.),(5.,5.),(-15.,-15.)),
        hvdc=(HVDCDispatch("dc",(-10.,-10.),(10.,10.)),),
        observed_ac_flows_MW=((20.,20.),(10.,10.),(15.,15.)))
    ratings=NormalContingencyRatings(
        _ev("ratings"),("ab","bc","de"),("t0","t1"),
        ((40.,40.),(8.,15.),(20.,20.)),
        contingency_MW=((45.,45.),(12.,20.),(25.,25.)))
    budget=CountryZoneBudget(_ev("fixture-quota"),
                             (("Germany",2),("France",1)),official=False)
    return grid,times,dispatch,ratings,budget


def _write_once(path, data):
    with path.open("x",encoding="utf-8") as stream:
        json.dump(data,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write("\n")
    return sha256(path.read_bytes()).hexdigest()


def _entries(sparse):
    c=sparse.tocoo()
    return [[int(r),int(col),float(v)] for r,col,v in zip(c.row,c.col,c.data)]


def generate(output):
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    grid,times,dispatch,ratings,budget=synthetic_reference()
    official=load_official_budget(target_year=grid.evidence.target_year)
    if not (len(official.quotas)==37 and sum(official.by_label.values())==102):
        raise AssertionError("G02: published table 3 mismatches")
    ledger=preflight_ledger(grid,times,dispatch,ratings,budget)
    if ledger["status"]!="PASS_SYNTHETIC":
        raise AssertionError("G01/G03/G11: preflight fixture rejected: "+str(ledger))
    physical=SparseACReference(grid)
    cache=physical.solve(dispatch,times)
    score=screen_annual_overload(grid,times,ratings,cache)
    if {x["branch_id"]:x["overload_MWh"] for x in score["wyA"]} != {"bc":4.,"de":0.}:
        raise AssertionError("G04: annual overload MWh regression")
    protected=protect_congested_union(score)
    if protected != frozenset(("bc",)):
        raise AssertionError("G03: critical-line protection not reproducible")
    # I-choice for fixtures: transformer + uncritical corridor may be contracted.
    # No real geography or missing external AC boundary can be inferred.
    z=country_quota_busmap(grid,budget,[0.,4.,0.],protected=protected)
    proj=build_oriented_projection(physical,budget,z,protected=protected)
    pz,cut=proj.verify(physical,cache)
    if not np.allclose(proj.A_z@cut,pz,atol=1e-9):
        raise AssertionError("G05: zonal KCL failed")
    ids=tuple(bus.name for bus in grid.buses)
    by_country={label:len({z[i] for i,bus in enumerate(grid.buses)
                           if bus.country==label}) for label,_ in budget.quotas}
    if by_country != budget.by_label:
        raise AssertionError("G02: country budget failed")
    cache.write_once(output/"reference_flow_cache.json")
    save_ledger_once(ledger,output/"preflight_ledger.json")
    sha_map={
        "reference_flow_cache.json":sha256((output/"reference_flow_cache.json").read_bytes()).hexdigest(),
        "preflight_ledger.json":sha256((output/"preflight_ledger.json").read_bytes()).hexdigest()
    }
    sha_map["country_busmap.json"]=_write_once(output/"country_busmap.json",{
        "schema":"M2_CountryBusmap_v1","bus_order":ids,"busmap":z,
        "country_quotas":budget.quotas,"protected_branch_ids":sorted(protected),
        "grid_sha256":_hash(asdict(grid)), "flow_cache_sha256":cache.sha256})
    sha_map["annual_overload.json"]=_write_once(output/"annual_overload.json",{
        "schema":"M2_AnnualOverload_v1","unit":"MWh","years":score,
        "weather_year_ids":times.weather_year_ids,"method":"A_225_400_kV"})
    sha_map["oriented_projection.json"]=_write_once(output/"oriented_projection.json",{
        "schema":"M2_OrientedProjection_v1",
        "zone_pairs":proj.zone_pairs, "physical_branch_groups":proj.grouped_branch_ids,
        "P":_entries(proj.P), "Gamma":_entries(proj.Gamma),
        "A_z":_entries(proj.A_z), "p_z_MW":pz.tolist(), "f_cut_MW":cut.tolist(),
        "counterflow":proj.counterflow_diagnostic(cache)})
    result={
        "schema":"M2_MA1_GateWitness_v1",
        "basis":"ONLY_SYNTHETIC_FIXTURE",
        "methodology_reproduction":"NOT_CLAIMED",
        "real_network_qualification":"BLOCKED_DATA",
        "weather_year_selection":"EXCLUDED; fixture ids not external five real years",
        "official_country_budget":{"entries":len(official.quotas),
                                    "zones":sum(official.by_label.values()),
                                    "sha256":official.evidence.sha256},
        "worker_contracts":{"W-PHY":"m2.contracts / m2.physical",
                            "W-CLU":"m2.country / m2.screening / m2.projection"},
        "gates":{
            "G01":"PASS_SYNTHETIC",
            "G02":"PASS_SYNTHETIC_QUOTAS; REAL_BLOCKED_DATA",
            "G03":"PASS_SYNTHETIC_ISLANDS_CRITICAL_AC_CONNECTED",
            "G04":"PASS_SYNTHETIC_YEARLY_MWh",
            "G05":"PASS_SYNTHETIC_SPARSE_ORIENTED_IDENTITIES",
            "G11_PART":"PASS_SYNTHETIC_COMPONENT_SEMANTICS; REAL_BLOCKED_DATA",
            "G06_TO_G12_REMAIN":"OUT_OF_SCOPE_MA1"
        },
        "evidence_files_sha256":sha_map,
        "reference_cache_sha256":cache.sha256,
        "resolved_islands":ledger["islands"],
        "limitations":["No actual European grid, observed snapshots or verified rating source",
                       "No non-unity-tap transformer model; REJECTED_COMPONENT",
                       "No MA2 x/c0 optimizer, no MA3 N-1 capacity qualification"]
    }
    _write_once(output/"gate_witness.json",result)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    result=generate(args.output)
    print(json.dumps({"status":"PASS_SYNTHETIC_ONLY","gates":result["gates"],
                      "reference_cache_sha256":result["reference_cache_sha256"]},
                     sort_keys=True))


if __name__=="__main__":
    main()
