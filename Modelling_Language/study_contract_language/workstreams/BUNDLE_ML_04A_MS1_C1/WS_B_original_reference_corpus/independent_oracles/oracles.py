"""Architecture-independent finite analytical reference, no mathspec/R1 imports."""
from fractions import Fraction as F
class Reject(ValueError):pass
def need(x,code):
    if not x:raise Reject(code)
def run(doc):
    i=doc["id"];s=doc["synthetic_data"];d=s["inputs"];o=s["observed"];u=s["units"];f=doc["study_frame"]
    need(f["authority"]=="OWNER_TBD","AUTHORITY_DRIFT")
    need(all(len(v)==len(set(v)) for v in f["domains"].values()),"AMBIGUOUS_ALIAS")
    if i=="RC01":
        need(d["dt"] is not None and F(d["dt"])>0,"DURATION_REQUIRED")
        p,t,eta,e,cap=map(F,(d["p"],d["dt"],d["eta"],d["initial"],d["capacity"]))
        need(F(d["min_p"])<=p<=F(d["max_p"]) and p<=0 and 0<eta<=1,"BATTERY_SCOPE")
        a=-p*t; b=e+a*eta
        need(F(o["intake"])==a and F(o["final"])==b and F(o["loss"])==a*(1-eta) and 0<=b<=cap,"ENERGY_LEDGER")
        return {"intake":str(a),"final":str(b),"loss":str(a*(1-eta))}
    if i=="RC02":
        vals=[]
        for j,rs in enumerate(o["delivered"]):
            need(len(rs)==len(d["connected"][j]),"TIME_SUPPORT")
            for k,r in enumerate(rs):
                need((d["connected"][j][k] or F(r)==0) and (F(r)>=0 or d["v2g_authority"]),"CONNECTION_OR_V2G")
            val=sum(F(r) for r in rs[:d["departure"][j]]);need(val>=F(d["required"][j]),"EV_SERVICE");vals.append(val)
        return {"individual":list(map(str,vals)),"fleet":str(sum(vals))}
    if i=="RC03":
        need(d["basis"]=="LHV","HEATING_VALUE_BASIS");need(u["flow"]=="kg/h","CARRIER_UNIT")
        m,p,h=F(o["flow"]),F(d["power"]),F(d["lhv"])
        need(p>0 and m>=0 and h>0,"ELECTROLYSER_DOMAIN")
        e=m*h;eta=e/p
        need(F(d["eta_min"])<=eta<=F(d["eta_max"]),"EFFICIENCY")
        return {"hydrogen_power":str(e),"eta":str(eta)}
    if i=="RC04":
        need(o["inventory_unit"]=="kg","MASS_UNIT");need(o["energy_basis"]==d["basis"]=="LHV","HEATING_VALUE_BASIS")
        x=F(d["initial"])+(F(d["inflow"])-F(d["outflow"]))*F(d["dt"])-F(d["loss"])
        need(x>=0 and x==F(o["final"]),"MASS_LEDGER")
        return {"final":str(x),"converted_energy":str(x*F(d["heating_value"]))}
    if i=="RC05":
        flows=list(map(F,o["flow"]));res=[F(0)]*len(s["domains"]["bus"])
        for (a,b),v in zip(d["orientation"],flows,strict=True):res[a]+=v;res[b]-=v
        need(res==list(map(F,d["injection"])),"KCL")
        loop=sum(F(x)*F(c)*v for x,c,v in zip(d["reactance"],d["cycle"],flows,strict=True));need(loop==0,"KVL")
        return {"nodal":list(map(str,res)),"cycle":str(loop)}
    if i=="RC06":
        n=F(o["modules"]);need(n.denominator==1 and 0<=n<=d["max_modules"],"INTEGER_MODULE")
        t=d["invest_time"]+d["lead_time"];need(o["commission"]==t,"LEAD_TIME")
        cap=[str(n*F(d["module_capacity"]) if k>=t else 0) for k in s["domains"]["stage"]];cost=n*F(d["capex"])
        need(cap==o["capacity"] and cost==F(o["cost"]),"INVESTMENT_LEDGER")
        return {"modules":str(n),"commission":t,"capacity":cap,"cost":str(cost)}
    if i=="RC07":
        need(d["guard_present"],"GUARD_REQUIRED")
        for stage,groups in enumerate(d["partitions"]):
            need(sorted(j for g in groups for j in g)==list(range(len(s["domains"]["scenario"]))),"INFORMATION_PARTITION")
            for g in groups:need(len({F(o["decision"][stage][j]) for j in g})==1,"NONANTICIPATIVITY")
        return {"pre_revelation_equal":True,"after_revelation_may_differ":True}
    if i=="RC08":
        need(len(o["contributions"])==len(set(o["contributions"])),"DUPLICATE_CONTRIBUTION")
        need(set(o["contributions"])==set(s["domains"]["event"]),"CONTRIBUTION_SUPPORT")
        need(d["basis"]=="EUR:real:2025","PRICE_BASIS")
        val=F(d["capex"])+sum(F(a)*F(b) for a,b in zip(d["opex"],d["duration"],strict=True))*F(d["probability"])*F(d["discount"])
        need(val==F(o["kpi"]),"KPI_VALUE");return {"kpi":str(val)}
    if i=="RC09":
        need(d["reference_snapshot"]==d["project_snapshot"],"EXOGENEITY")
        need(sum(map(F,d["weights"]))==1 and all(F(v)>=0 for v in d["weights"]),"WEIGHT")
        a=sum((F(r)-F(p))*F(w) for r,p,w in zip(d["baseline"],d["project"],d["weights"],strict=True));b=a/(1+F(d["discount_rate"]))
        need(a==F(o["annual"]) and b==F(o["discounted"]),"COUNTERFACTUAL_VALUE")
        need(d["owner"]=="OWNER_TBD","OWNER")
        return {"annual":str(a),"discounted":str(b),"owner":"OWNER_TBD"}
    if i=="RC10":
        need(len(d["source_ids"])==2 and len(set(d["source_ids"]))==2,"SOURCE_LOSS")
        need(len(set(d["generator_ids"]))==2 and all(d["variation_disclosed"]),"VARIATION")
        need(o["evidence_status"]=="NOT_EXECUTED" and o["evidence_role"]=="REQUEST","EVIDENCE_PROMOTION")
        need(not o["e4_claim"],"E4_UNSUPPORTED")
        return {"finite_agreement":F(o["cost"][0])==F(o["cost"][1]),"e4":"NOT_PROVED","e5":"NOT_ASSESSED"}
    raise Reject("UNKNOWN_RC")
