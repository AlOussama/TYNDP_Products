"""Same frozen C1 synthetic data for all architecture probes.
One derived mathematical fragment per original RC. Not full original paths.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"canonical_closure"))
from test_closure import fixture,q
from closure import digest
CORPUS=ROOT/"WS_B_original_reference_corpus"
def frozen(id):
    return json.loads((CORPUS/"reference_cases"/id/"contract.json").read_text())
def rows(dims,domains,values):
    ks=list(product(*(domains[a] for a in sorted(dims))))
    if not dims:values=[values]
    return [{"key":list(k),"value":v} for k,v in zip(ks,values,strict=True)]
def build(id,labels,params,expr,cond,values,quant,expected,negative,roles=None,rules=None,relations=None,relation_data=None,temporal=None,conversions=None,pred_axes=None,weight_roles=None,note="",axis_roles=None):
    roles=roles or {};rules=rules or {};axis_roles=axis_roles or {}
    dd={n:{"dtype":"int" if type(v[0]) is int else "str","ordered":axis_roles.get(n)=="time"} for n,v in labels.items()}
    d={"version":0,"dimensions":dd,"parameters":params,"expressions":expr,"conditions":cond}
    if relations:d["relations"]=relations
    c=fixture(d,quant=quant,roles=roles,domain_rules=rules,domains=labels,pred_axes=pred_axes or {},temporal=temporal,conversions=conversions)
    c["audit"]["source_ref"]="fixture:C1-"+id
    data={"id":c["study"]["data_id"],"version":c["study"]["data_version"],"parameters":{n:rows(p["dims"],labels,values[n]) for n,p in params.items()},"relations":relation_data or {}}
    return {"id":id,"doc":d,"context":c,"data":data,"expected":expected,"negative":negative,"note":note,
            "weight_roles":weight_roles or {},"axis_roles":axis_roles}
def p(*dims,dtype="float"):return {"dims":list(dims),"dtype":dtype}
def money(unit="EUR",basis="EUR:real:2025"):return q(unit,"currency",basis)
def power():return q("MW","electricity")
def energy():return q("MWh","electricity")
def cases():
    out=[]
    s=frozen("RC01")["synthetic_data"];i,o=s["inputs"],s["observed"]
    qp=power();qp["sign"]="INJECTION";qe=energy();qe["sign"]="INJECTION"
    out.append(build("RC01",{"t":s["domains"]["interval"]},{"p":p("t"),"dt":p(),"e":p("t")},
      {"exchange":"p * dt"},{"exchange_ok":"exchange == e"},{"p":[i["p"]],"dt":i["dt"],"e":[str(-F(o["intake"]))]},
      {"p":qp,"dt":q("h"),"e":qe,"exchange":qe},{"exchange":["-1"]},{"param":"e","values":["-2"],"condition":"exchange_ok"},
      roles={"dt":"INPUT"},rules={"dt":"POSITIVE"},axis_roles={"t":"time"},note="Signed grid exchange only; terminal/efficiency ledger outside comparison. R1 fixed duration specialization uses the original 0.5 h frame."))
    s=frozen("RC02")["synthetic_data"];i,o=s["inputs"],s["observed"];vs=s["domains"]["vehicle"];ts=s["domains"]["interval"]
    def ev(vals):return [str(F(vals[v][t])/1000) for t in range(len(ts)) for v in range(len(vs))]
    delivered=ev(o["delivered"]);eligible=[int(i["connected"][v][t] and t<i["departure"][v]) for t in range(len(ts)) for v in range(len(vs))]
    out.append(build("RC02",{"interval":ts,"vehicle":vs},
      {"delivered":p("interval","vehicle"),"eligible":p("interval","vehicle",dtype="int"),"required":p("vehicle"),"zero":p()},
      {"received":"sum(delivered * eligible, over=interval)","outside":"sum(delivered * (1-eligible), over=interval)"},
      {"service":"received >= required","window_ok":"outside == zero"},
      {"delivered":delivered,"eligible":eligible,"required":[str(F(x)/1000) for x in i["required"]],"zero":"0"},
      {n:energy() for n in ("delivered","required","zero","received","outside")},
      {"received":["1/250","3/500"],"outside":["0","0"]},{"param":"delivered","values":ev([["5","0"],["2","3"]]),"condition":"service"},
      roles={"eligible":"INPUT","required":"INPUT","zero":"INPUT"},pred_axes={"service":["vehicle"],"window_ok":["vehicle"]},
      axis_roles={"interval":"time","vehicle":"sample"},note="Exact explicit kWh to MWh conversion (1/1000); eligibility derived from original connection/departure. Finite service, not forall-request capability."))
    s=frozen("RC03")["synthetic_data"];i,o=s["inputs"],s["observed"]
    cv={n:{"id":"conversion:"+n,"version":"1","source_ref":"fixture:RC03:"+n,"source_sha256":digest({"RC03":n,"value":i[k]}),"authority":"RESEARCH_ASSUMPTION"} for n,k in (("h","lhv"),("lo","eta_min"),("hi","eta_max"))}
    hydrogen=q("MW_H2_LHV","hydrogen","LHV")
    out.append(build("RC03",{"t":s["domains"]["interval"]},{"power":p("t"),"flow":p("t"),"h":p(),"lo":p(),"hi":p()},
      {"chemical":"flow*h","lower":"power*lo","upper":"power*hi"},
      {"low_ok":"chemical >= lower","high_ok":"chemical <= upper"},
      {"power":[i["power"]],"flow":[o["flow"]],"h":i["lhv"],"lo":i["eta_min"],"hi":i["eta_max"]},
      {"power":power(),"flow":q("kg/h","hydrogen"),"h":q("MWh_H2_LHV/kg","conversion","LHV"),"lo":q("LHV_ratio","conversion","LHV"),"hi":q("LHV_ratio","conversion","LHV"),"chemical":hydrogen,"lower":hydrogen,"upper":hydrogen},
      {"chemical":["20"],"lower":["18"],"upper":["24"]},{"param":"flow","values":["900"],"condition":"high_ok"},
      roles={n:"METHOD_PARAMETER" for n in cv},rules={n:"POSITIVE" for n in cv},conversions=cv,axis_roles={"t":"time"},note="Original synthetic heating value and efficiency envelope; extra finite negative excessive flow."))
    s=frozen("RC04")["synthetic_data"];i,o=s["inputs"],s["observed"];mass=q("kg","hydrogen")
    out.append(build("RC04",{"t":s["domains"]["interval"]},
      {"initial":p(),"inflow":p("t"),"outflow":p("t"),"dt":p(),"loss":p("t"),"reported":p("t")},
      {"stock":"initial + (inflow-outflow)*dt - loss"},{"ledger":"stock == reported"},
      {"initial":i["initial"],"inflow":[i["inflow"]],"outflow":[i["outflow"]],"dt":i["dt"],"loss":[i["loss"]],"reported":[o["final"]]},
      {"initial":mass,"inflow":q("kg/h","hydrogen"),"outflow":q("kg/h","hydrogen"),"dt":q("h"),"loss":mass,"reported":mass,"stock":mass},
      {"stock":["109"]},{"param":"reported","values":["110"],"condition":"ledger"},roles={"dt":"INPUT"},rules={"dt":"POSITIVE"},axis_roles={"t":"time"},note="Single-interval mass ledger; not general temporal recursion or basis conversion."))
    s=frozen("RC05")["synthetic_data"];i,o=s["inputs"],s["observed"];bs=s["domains"]["bus"];ls=s["domains"]["branch"]
    rd={"sending":[{"branch":n,"bus":bs[x[0]]} for n,x in zip(ls,i["orientation"])],"receiving":[{"branch":n,"bus":bs[x[1]]} for n,x in zip(ls,i["orientation"])]}
    out.append(build("RC05",{"bus":bs,"branch":ls},{"flow":p("branch"),"injection":p("bus"),"x":p("branch"),"zero":p()},
      {"net":"sum(flow, over=branch, by=sending[bus])-sum(flow, over=branch, by=receiving[bus])","cycle":"sum(flow*x, over=branch)"},
      {"kcl":"net == injection","kvl":"cycle == zero"},{"flow":o["flow"],"injection":i["injection"],"x":[str(F(a)*F(b)) for a,b in zip(i["reactance"],i["cycle"])],"zero":"0"},
      {n:power() for n in ("flow","injection","zero","net","cycle")},{"net":s["expected"]["nodal"],"cycle":["0"]},
      {"param":"flow","values":[str(F(v)+1) for v in o["flow"]],"condition":"kvl"},
      relations={n:{"key":"branch","values":"bus"} for n in rd},relation_data=rd,pred_axes={"kcl":["bus"],"kvl":[]},
      note="Equal-coefficient triangle. x is explicitly normalized dimensionless coefficient; not arbitrary physical reactance. KCL-preserving KVL counterexample."))
    s=frozen("RC06")["synthetic_data"];i,o=s["inputs"],s["observed"];module=q("module");cap=power()
    out.append(build("RC06",{"stage":s["domains"]["stage"]},{"n":p(dtype="int"),"size":p(),"capex":p(),"zero_capacity":p(),"reported":p("stage"),"limit":p(dtype="int"),"reported_cost":p()},
      {"capacity":{"dims":["stage"],"cases":{"commissioned":{"when":"stage >= "+str(o["commission"]),"expression":"n*size"}},"otherwise":"zero_capacity"},"cost":"n*capex"},
      {"capacity_ok":"capacity == reported","module_limit":"n <= limit","cost_ok":"cost == reported_cost"},
      {"n":o["modules"],"size":i["module_capacity"],"capex":i["capex"],"zero_capacity":"0","reported":o["capacity"],"limit":i["max_modules"],"reported_cost":o["cost"]},
      {"n":module,"size":q("MW/module","electricity"),"capex":money("EUR/module"),"zero_capacity":cap,"reported":cap,"limit":module,"capacity":cap,"cost":money(),"reported_cost":money()},
      {"capacity":o["capacity"],"cost":[o["cost"]]},{"param":"n","values":["3/10"],"reject":"INTEGER_DOMAIN"},
      roles={n:"INPUT" for n in ("size","capex","limit","zero_capacity")},rules={"n":"NONNEGATIVE"},pred_axes={"capacity_ok":["stage"],"module_limit":[],"cost_ok":[]},axis_roles={"stage":"time"},note="Finite commission date specialized from original lead time; integer data and typed discrete capacity/cost."))
    s=frozen("RC07")["synthetic_data"];o=s["observed"]
    out.append(build("RC07",{"t":[s["domains"]["stage"][0]]},{"a":p("t"),"b":p("t")},{},{"nonanticipativity":"a == b"},
      {"a":[o["decision"][0][0]],"b":[o["decision"][0][1]]},{"a":power(),"b":power()},{},{"param":"b","values":["11"],"condition":"nonanticipativity"},
      axis_roles={"t":"time"},note="Explicit pre-revelation pair projection; full information-partition and quantifier semantics not evaluated."))
    s=frozen("RC08")["synthetic_data"];i,o=s["inputs"],s["observed"]
    out.append(build("RC08",{"t":s["domains"]["interval"]},{"opex":p("t"),"dt":p("t"),"capex":p(),"prob":p(),"discount":p(),"reported":p()},
      {"total":"sum(opex*dt, over=t)*prob*discount + capex"},{"kpi":"total == reported"},
      {"opex":i["opex"],"dt":i["duration"],"capex":i["capex"],"prob":i["probability"],"discount":i["discount"],"reported":o["kpi"]},
      {"opex":money("EUR/h"),"dt":q("h"),"capex":money(),"reported":money(),"total":money()},
      {"total":[o["kpi"]]},{"param":"reported","values":["270"],"condition":"kpi"},roles={n:"INPUT" for n in ("dt","prob","discount")},rules={"dt":"POSITIVE"},pred_axes={"kpi":[]},axis_roles={"t":"time"},note="Physical rate × duration, exact cost; contribution-event deduplication remains outer contract."))
    s=frozen("RC09")["synthetic_data"];i,o=s["inputs"],s["observed"]
    out.append(build("RC09",{"s":s["domains"]["scenario"]},{"baseline":p("s"),"project":p("s"),"weight":p("s"),"factor":p(),"reported":p()},
      {"annual":"sum((baseline-project)*weight, over=s)","discounted":"annual/factor"},{"result_ok":"discounted == reported"},
      {"baseline":i["baseline"],"project":i["project"],"weight":i["weights"],"factor":str(1+F(i["discount_rate"])),"reported":o["discounted"]},
      {n:money() for n in ("baseline","project","reported","annual","discounted")},
      {"annual":[o["annual"]],"discounted":[o["discounted"]]},{"param":"reported","values":["120"],"condition":"result_ok"},
      roles={"weight":"INPUT","factor":"METHOD_PARAMETER"},rules={"factor":"POSITIVE"},pred_axes={"result_ok":[]},weight_roles={"weight":"probability"},axis_roles={"s":"scenario"},note="Finite cost proxy; exact discount factor derived from original 1/10 rate. Pair/exogeneity remains outer context, not validated by arithmetic."))
    s=frozen("RC10")["synthetic_data"];o=s["observed"]
    out.append(build("RC10",{},{"a":p(),"b":p()},{},{"agree":"a == b"},
      {"a":o["cost"][0],"b":o["cost"][1]},{"a":money(),"b":money()},{},{"param":"b","values":["171"],"condition":"agree"},
      note="Scalar agreement only; no E4/E5 promotion or proof of independent models."))
    return out
def extra_cases():
    # Alternative projection: explicitly preintegrated monetary amounts,
    # not a replacement for RC08 physical rate x duration.
    s=frozen("RC08")["synthetic_data"];i=s["inputs"];o=s["observed"]
    costs=[str(F(a)*F(b)) for a,b in zip(i["opex"],i["duration"])]
    x=build("EX08",{"t":s["domains"]["interval"]},{"amount":p("t"),"capex":p()},{"total":"sum(amount, over=t)+capex"},{},
      {"amount":costs,"capex":i["capex"]},{n:money() for n in ("amount","capex","total")},{"total":[o["kpi"]]},None,axis_roles={"t":"time"},note="Explicitly preintegrated EUR amounts; narrower alternative, not original RC08 physical contract.")
    y=build("EXPOW",{"t":["t0","t1"]},{"base":p(),"n":p("t",dtype="int")},{"v":"base**n"},{},
      {"base":"11/10","n":[1,2]},{},{"v":["11/10","121/100"]},None,roles={"base":"INPUT","n":"INPUT"},axis_roles={"t":"time"},note="Counterexample to current M3 admission: data-dependent integer exponent, exact R1 profile support.")
    return [x,y]
