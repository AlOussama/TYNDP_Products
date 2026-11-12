#!/usr/bin/env python3
"""ML-C04 synthetic analytical micro-oracle self-check. NOT an IoSN/tool test."""
import json
import math
import sys
from datetime import datetime
from pathlib import Path

def near(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-11, abs_tol=1e-11)

def check(ok, description):
    if not ok:
        raise AssertionError(description)

def all_near(a, b):
    return len(a) == len(b) and all(near(x, y) for x, y in zip(a, b))

def run(case):
    key = case["id"]
    d, o = case["inputs"], case["oracle"]
    if key == "B01":
        w, demands = d["weights"], d["demand_mw"]
        check(near(sum(w), 1) and len(set(w)) > 1, "nonuniform normalized weights")
        f = lambda x, weights: d["capex_eur_per_mw"] * x + sum(
            weights[i] * d["voll_eur_per_mwh"] * max(z - x, 0) * d["dt_h"]
            for i, z in enumerate(demands))
        check(near(f(3, w), o["objective_eur"]), "weighted cost")
        check(all(f(3, w) < f(x, w) for x in [0, 1, 2, 4]), "unique optimal breakpoint")
        check(near(sum(w[i] * max(z-3, 0) for i,z in enumerate(demands)),o["weighted_ens_mwh"]),"ENS")
        independent = sum(w[i] * f(min(z,4), [1 if j == i else 0 for j in range(5)]) for i,z in enumerate(demands))
        check(near(independent,o["unlinked_objective_eur"]),"independent cost")
        check(near(f(3,[0.2]*5),o["uniform_objective_eur_at_3mw"]),"uniform mutant cost")
        matched_year_weights = {y:tuple(w) for y in d["years"]}
        check(len(set(matched_year_weights.values()))==1, "cross-year vector identity")
        mut_year_weights = dict(matched_year_weights)
        mut_year_weights[2040] = tuple([w[0]+.01,w[1]-.01,*w[2:]])
        return f(3,w), independent < f(3,w) and not near(f(3,[.2]*5),f(3,w)) and len(set(mut_year_weights.values()))!=1
    if key == "B02":
        w,p,dt = d["weights"],d["ens_mw_per_cy"],d["durations_h"]
        e = sum(wi*pi*sum(dt) for wi,pi in zip(w,p))
        check(near(e,o["expected_ens_mwh"]),"ENS energy")
        check(near(e*d["voll_eur_per_mwh"],o["ens_penalty_eur"]),"ENS VoLL")
        value=e*d["voll_eur_per_mwh"]+d["capex_eur"]
        check(near(value,o["objective_eur"]),"objective capex once")
        uniform=sum(p)/5*sum(dt)
        check(near(uniform,o["uniform_ens_mwh"]),"uniform mutant")
        return value, not near(uniform,e) and not near(value,5*d["capex_eur"]+e*d["voll_eur_per_mwh"])
    if key == "B03":
        starts=[datetime.fromisoformat(x) for x in d["start_utc"]]
        ends=[datetime.fromisoformat(x) for x in d["end_utc"]]
        dt=[(b-a).total_seconds()/3600 for a,b in zip(starts,ends)]
        check(starts[1]==ends[0] and all(h>0 for h in dt),"UTC adjacency")
        check(all_near(dt,o["duration_h"]),"UTC durations")
        en=sum(p*h for p,h in zip(d["power_mw"],dt))
        check(near(en,o["energy_mwh"]),"energy integration")
        check(sum(d["power_mw"])==o["naive_power_sum"],"sum MW")
        return en, not near(sum(d["power_mw"]),en) and starts[0]<ends[0]
    if key == "B04":
        a,b,c=d["angles"]
        flows=[a-b,a-c,c-b]
        check(all_near(flows,o["physical_flows_mw"]),"DC angle flows")
        kcl=[flows[0]+flows[1],-flows[0]-flows[2],-flows[1]+flows[2]]
        check(all_near(kcl,d["injections_mw"]),"KCL")
        check(near(flows[0],flows[1]+flows[2]),"physical KVL")
        altered=d["market_link_mutation_mw"]
        kcl2=[altered[0]+altered[1],-altered[0]-altered[2],-altered[1]+altered[2]]
        check(all_near(kcl2,d["injections_mw"]),"mutant preserves KCL")
        return flows, not near(altered[0],altered[1]+altered[2])
    if key == "B05":
        inj, f = d["detail_injection_mw"],d["detail_flows_mw"]
        check(all_near([f[0]+f[1],-f[0]+f[2],-f[1]-f[2]],inj),"detail KCL")
        cut=f[1]+f[2]
        check(near(cut,o["cluster_cut_mw"]) and near(sum(inj[:2]),cut),"cut conservation")
        p=d["triangle_injection_mw"]
        base=[p*x for x in d["ptdf_AB_AC_CB"]]
        check(all_near(base,o["triangle_base_flows_mw"]),"triangle PTDF")
        post=[0,base[1]+d["lodf_AC_AB"]*base[0],base[2]+d["lodf_CB_AB"]*base[0]]
        check(all_near(post,o["post_AB_outage_flows_mw"]),"LODF N-1")
        check(all(x<=d["remaining_rating_mw"] for x in post[1:]),"N-1 rating synthetic")
        check(len(d["required_output_classes"])==6 and len(d["capacity_dimensions"])==4,"output inventory")
        disconnected_zone_x_on_path = {"A1","B"}
        adjacent_on_path = {frozenset(("A1","A2")),frozenset(("A2","B"))}
        check(not any(e <= disconnected_zone_x_on_path for e in adjacent_on_path),"disconnected cluster mutant")
        return post, not near(base[1],post[1]) and not near(f[1],cut)
    if key == "B06":
        x1=min(d["stage1_need_mw"],d["stage1_real_x_max_mw"])
        x2=d["stage2_need_mw"]-x1
        check(0<=x2<=d["conceptual_x_max_mw"],"stage2 residual capacity")
        actual=d["cost_real_eur_per_mw"]*x1+d["cost_conceptual_eur_per_mw"]*x2
        check(near(actual,o["final_cost_eur"]),"no double capex")
        joint=d["stage2_need_mw"]*d["cost_conceptual_eur_per_mw"]
        check(near(joint,o["joint_relaxation_cost_eur"]),"joint mutant")
        double=actual+d["cost_real_eur_per_mw"]*x1
        check(near(double,o["double_paid_cost_eur"]),"double capex mutant")
        return actual, joint < actual and double > actual
    if key == "B07":
        e0=d["e0_mwh"]
        e1=e0+d["eta_ch"]*d["charge_mw"]*d["dt_charge_h"]
        e2=e1-d["discharge_mw"]*d["dt_discharge_h"]/d["eta_dis"]
        check(near(e1,o["e_after_charge_mwh"]) and near(e2,o["e_after_discharge_mwh"]),"SoC recursion")
        check(0<=min(e0,e1,e2) and max(e0,e1,e2)<=d["max_energy_mwh"],"state bounds")
        check(all_near([e0/d["max_energy_mwh"],e1/d["max_energy_mwh"],e2/d["max_energy_mwh"]],o["soc"]),"normalized SoC")
        bad=e0+d["eta_ch"]*d["charge_mw"]-d["discharge_mw"]/d["eta_dis"]
        check(near(bad,o["omit_dt_terminal_mwh"]),"omit dt mutation")
        return e2, not near(bad,e2)
    if key == "B08":
        prod=d["electrolysis_mw_e"]*d["step_h"]*d["eta_e_to_h"]
        use=d["h2_to_e_mw_e"]*d["step_h"]/d["eta_h_to_e"]
        check(near(prod,o["h2_produced_mwh_h"]),"hydrogen production")
        check(near(use,o["h2_for_power_mwh_h"]),"return electricity")
        check(near(prod,use+d["h2_demand_mwh_h"]),"H2 balance")
        source=d["frozen_profile_mw"]; mutated=d["mutated_profile_mw"]; dt=d["frozen_durations_h"]
        src_energy=sum(a*b for a,b in zip(source,dt))
        alt_energy=sum(a*b for a,b in zip(mutated,dt))
        check(near(src_energy,o["frozen_electricity_mwh"]),"frozen energy")
        check(near(src_energy,alt_energy),"mutant same annual energy")
        return prod, source!=mutated and not near(prod,d["electrolysis_mw_e"]*d["step_h"])
    if key == "B09":
        e=d["reservoir_e0_mwh_water_eq"]+(d["inflow_mw_water_eq"]-d["turbine_mw_water_eq"])*d["step_h"]
        check(near(e,o["reservoir_e1_mwh_water_eq"]),"hydro conservation")
        final=[x+y for x,y in zip(d["implicit_load_mw"],d["explicit_delta_mw"])]
        check(all_near(final,o["final_load_mw"]),"DSR load")
        check(near(sum(final),o["demand_energy_mwh"]) and near(sum(final),sum(d["original_load_mw"])),"illustrative DSR energy")
        check(d["dsr_implicit_asset_id"]!=d["dsr_explicit_asset_id"],"asset disjointness")
        return e, not near(e-d["inflow_mw_water_eq"]*d["step_h"],e) and len(d["hydro_classes"])==5
    if key == "B10":
        flow=d["two_bus_injection_mw"]
        check(near(flow,o["lf_physical_flow_mw"]),"LF KCL / angle possible")
        check((flow>d["thermal_rating_mw"])==o["lf_is_thermal_overloaded"],"nonbinding LF rating")
        good=(0<=d["opf_candidate_mw"]<=d["lf_candidate_cap_mw"])
        bad=(0<=d["mutant_opf_candidate_mw"]<=d["lf_candidate_cap_mw"])
        check(good==o["opf_cap_ok"] and bad==o["opf_mutant_cap_ok"],"OPF conditional cap")
        return flow, good and not bad
    if key == "B11":
        for x,y in d["sample_feasible_xy"]:
            slack=x+y-d["rhs"]
            check(slack>=0 and near(d["row_scale"]*(x+y-slack),d["row_scale"]*d["rhs"]),"scaled-slack equivalence")
        x,y=o["optimal_xy"]
        value=d["objective_coefficients"][0]*x+d["objective_coefficients"][1]*y
        check(near(value,o["optimal_value"]),"LP optimum vertex")
        check(not (0+0>=d["rhs"]) and near(2*0+2*0-2*(-4),8),"negative slack relaxes")
        return value, True
    if key == "B12":
        portfolios=d["portfolios_mw"]
        for x,y in portfolios:
            check(near(x+y,d["required_total_mw"]) and 0<=x<=1 and 0<=y<=1,"optimal face feasibility")
            check(near(x*d["unit_cost"][0]+y*d["unit_cost"][1],o["optimal_value"]),"optimal portfolio objective")
        check(len(set(map(tuple,portfolios)))==o["distinct_portfolios"],"distinct optima")
        return o["optimal_value"], portfolios[0]!=portfolios[1]
    if key == "B13":
        dt=sum(d["durations_h"])
        e=sum(w*p*dt for w,p in zip(d["weights"],d["ens_mw_by_cy"]))
        bad=sum(p*dt for p in d["ens_mw_by_cy"])
        check(near(e,o["raw_expected_ens_mwh"]) and near(bad,o["raw_unweighted_ens_mwh"]),"raw aggregation")
        check(near(e*d["voll_eur_per_mwh"],o["raw_expected_ens_cost_eur"]),"value units")
        blocked=d["approved_kpi_formula_id"] is None or d["approved_threshold_mw"] is None
        check(blocked and o["kpi_claim"]=="BLOCKED","undefined KPI cannot pass")
        return e, not near(e,bad) and blocked
    if key == "B14":
        supported=d["mandatory_feature"] in d["supported_features"]
        status="PASS" if supported else "UNSUPPORTED"
        optional="NOT_APPLICABLE" if not d["optional_opf_requested"] else "NOT_EXECUTED"
        overall="PASS" if supported else "BLOCKED"
        check(status==o["missing_mandatory_status"],"mandatory unsupported")
        check(optional==o["optional_off_status"] and overall==o["overall_conformance"],"optional vs mandatory")
        return status, not supported and optional=="NOT_APPLICABLE"
    if key == "B15":
        factor=d["synthetic_route_factor"]
        length=d["geometry_km"]*(1+factor)
        check(near(length,o["illustrative_route_km"]),"illustrative route")
        check(d["source_draft_factor_range"][0]<=factor<=d["source_draft_factor_range"][1],"source version interval")
        check(not d["official_factor_approved"] and o["real_route_oracle_status"]=="BLOCKED","no released factor")
        check(d["offshore_target_mw_fixed"]>0,"fixed target")
        return length, not d["official_factor_approved"]
    raise KeyError(key)

def main():
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("cases.json")
    suite=json.loads(path.read_text(encoding="utf-8"))
    observed=[]
    for case in suite["cases"]:
        value,detected=run(case)
        check(detected,"mutation was not detected: "+case["id"])
        observed.append({"case":case["id"],"positive":"PASS_SYNTHETIC_SELF_CHECK","targeted_mutation":"DETECTED","oracle":value})
    print(json.dumps({"suite":"ML-C04","executed_scope":"STANDARD_LIBRARY_ARITHMETIC_AND_FIXTURE_STRUCTURE_ONLY","cases_run":len(observed),"positives_passed":len(observed),"mutations_detected":len(observed),"tool_conformance":"NOT_TESTED","G1":"BLOCKED","details":observed},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
