#!/usr/bin/env python3
"""ML-R04: stdlib-only arithmetic self-check; NOT a tool-conformance test."""
import json
from fractions import Fraction as Q
from pathlib import Path

FIX = json.loads((Path(__file__).parent / "oracles.json").read_text(encoding="utf-8"))
C = {v["id"]: v for v in FIX["cases"]}
def q(v): return Q(str(v))
def check(name, ok):
    if not ok: raise AssertionError(name)
    print(f"SYNTHETIC_ORACLE_SELF_CHECK {name}: OK")
def max0(v): return max(q(0), v)

p = C["C01"]["parameters"]
w = [q(x) for x in p["weights"]]
d = [q(x) for x in p["demands_mw"]]
cap = q(p["capex_eur_per_mw"])
voll = q(p["voll_eur_per_mwh"])
def j(x):
    return cap*x + sum(wi*voll*max0(di-x)*q(p["duration_h"]) for wi,di in zip(w,d))
check("C01 weights", len(w)==5 and sum(w)==1 and len(set(w))==1)
check("C01 objective", j(q(2))==q(10) and j(q(2))<j(q(1))<j(q(0)))
xs = [q(x) for x in C["C02"]["parameters"]["candidate_x_by_cy_mw"]]
j2 = sum(wi*(cap*x+voll*max0(di-x)*q(p["duration_h"])) for wi,di,x in zip(w,d,xs))
check("C02 broken nonanticipativity", len(set(xs))>1 and j2==q("8.8") and j2<j(q(2)))

p = C["C03"]["parameters"]
energy = sum(q(a)*q(b) for a,b in zip(p["half_hour_power_mw"],p["half_hour_duration_h"]))
check("C03 energy-dimension", energy==1 and energy==q(p["hourly_power_mw"])*q(p["hourly_duration_h"]) and energy*q(p["cost_eur_per_mwh"])==50)

p = C["C04"]["parameters"]; t=p["angles"]; f=p["physical_flows_mw"]
check("C04 physical KCL/KVL", f["AB"]==t["A"]-t["B"] and f["AC"]==t["A"]-t["C"] and f["CB"]==t["C"]-t["B"] and f["AB"]==f["AC"]+f["CB"] and f["AB"]+f["AC"]==90)
g=p["controllable_link_variant_mw"]
check("C04 link distinction", g["AB"]+g["AC"]==90 and g["AB"] != f["AB"] and g["AC"]==0 and g["CB"]==0)

p=C["C05"]["parameters"]; f=p["flows_mw"]; i=p["injection_mw"]
check("C05 cluster cut", f["A1_A2"]+f["A1_B"]==i["A1"] and -f["A1_A2"]+f["A2_B"]==i["A2"] and -(f["A1_B"]+f["A2_B"])==i["B"] and i["A1"]+i["A2"]==f["A1_B"]+f["A2_B"]==50)
check("C05 missing edge mutation", f["A1_B"]!=i["A1"]+i["A2"])

p=C["C06"]["parameters"]; x=q(4); y=q(0); slack=x+y-q(p["rhs"])
check("C06 projected LP equivalence", x+y>=q(p["rhs"]) and 2*x+2*y-2*slack==8 and slack>=0 and q(p["objective_coefficient_x"])*x+q(p["objective_coefficient_y"])*y==8)
check("C06 omitted slack sign", (2*q(0)+2*q(0)-2*q(-4)==8) and q(-4)<0)

p=C["C07"]["parameters"]; ports=p["portfolios_mw"]
check("C07 multiple-optimum portfolios", len({tuple(z) for z in ports})==3 and all(sum(q(x) for x in z)==1 for z in ports) and all(sum(q(x) for x in z)==q(1) for z in ports))

p=C["C08"]["parameters"]; e=[sum(q(x)*q(dt) for x,dt in zip(v,p["durations_h"])) for v in p["ens_mw_by_weather"]]
weighted=sum(q(wi)*ei for wi,ei in zip(p["weights"],e))
check("C08 time-weather weighted KPI", e==[q(x) for x in [1,3,2,0,4]] and weighted==2 and weighted*q(p["voll_eur_per_mwh"])==200 and sum(e)==10)
check("C08 wrong unweighted KPI", sum(e)!=weighted)

p=C["C09"]["parameters"]
check("C09 mandatory unsupported", p["mandatory_requirement"]=="MA01-SR-029" and p["supported"] is False and C["C09"]["expected"]["test_status"]=="UNSUPPORTED" and C["C09"]["expected"]["overall_conformance_pass"] is False)

p=C["C10"]["parameters"]; lim=q(p["lf_cap_mw"])
check("C10 conditional OPF", p["opf_variant_off"] is False and p["opf_variant_on"] is True and 0<=q(p["opf_passing_investment_mw"])<=lim<q(p["opf_failing_investment_mw"]))
check("C10 statuses", C["C10"]["expected"]["off_test_status"]=="NOT_APPLICABLE" and C["C10"]["expected"]["on_pass_test_status"]=="PASS" and C["C10"]["expected"]["on_fail_test_status"]=="FAIL" and C["C10"]["expected"]["on_unsupported_test_status"]=="UNSUPPORTED")
print("SELF_CHECK_COMPLETE; no solver, tool implementation, owner approval, conformance assessment or G1 decision performed.")
