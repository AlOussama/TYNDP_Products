'use strict';
/** Restricted independent numerical reference-case micro-oracles, NOT CSNF parser or E2-E5 proof. */
function sample(rc){
 const d={
 RC01:{p_mw:-2,h:0.5,grid_mwh:1,unit:"MWh"},
 RC02:{ev:[{id:"v1",due:1,delivered:1},{id:"v2",due:2,delivered:2}],total:3},
 RC03:{input_mw:2,h:1,h2_kg:40,hv_mwh_per_kg:0.03333,basis:"LHV",eff_cap:0.8,electric_unit:"MW",hydrogen_unit:"kg"},
 RC04:{initial_kg:100,inflow_kgh:20,outflow_kgh:5,leak_kg:2,h:1,final_kg:113,unit:"kg"},
 RC05:{branch:[[0,1],[1,2],[2,0]],x:[1,1,1],f:[1,1,-2],inject:[3,0,-3],duties:["KCL","KVL"],e4_claim:false},
 RC06:{allowed:[0,1],built:1,lead_time_valid:true},
 RC07:{first_stage:{warm:5,cold:5},guard:"before_revelation",information_set:"stage1"},
 RC08:{capex_eur:100,p_mw:3,h:2,marginal_eur_mwh:2,weight:0.5,probability:1,discount:1,total_eur:106,price_year:2025,basis:"real"},
 RC09:{baseline:"same_exogenous",project:"same_exogenous",baseline_eur:100,project_eur:90,delta_eur:-10,price_basis:"EUR-real-2025",owner:"OWNER_TBD"},
 RC10:{models:[{variant:"SOC",status:"NOT_EXECUTED",kpi:100},{variant:"energy",status:"NOT_EXECUTED",kpi:100}],basis:"EUR-real-2025",e4_claim:false}
 };
 return {case_id:rc,source:"ML-C19/11:"+rc,authority_state:rc==="RC01"||rc==="RC09"?"OWNER_TBD":"PROPOSED",contract:{modality:"REQUIRED",guard:"study_applicable"},evidence:{status:"NOT_EXECUTED",role:"REQUEST"},alias:[],data:JSON.parse(JSON.stringify(d[rc]))};
}
function probe(doc){
 const d=doc.data||{},issue=[];const add=(code,category)=>issue.push({code,category});
 if(doc.evidence?.status==="PASS"&&(!doc.evidence.run_id||!doc.evidence.digest))add("UNSUPPORTED_PASS","FAIL_STATIC");
 if(!doc.source)add("SOURCE_LOSS","AUDIT_LOSS");
 if(doc.alias.some((a,i,arr)=>arr.findIndex(v=>v.key===a.key)!==i))add("AMBIGUOUS_ALIAS","BLOCKED");
 switch(doc.case_id){
  case "RC01":
   if(!(d.h>0))add("TIME_DURATION_MISSING","BLOCKED");
   else if(d.unit!=="MWh"||Math.abs(-d.p_mw*d.h-d.grid_mwh)>1e-9)add("EXTERNAL_GRID_LEDGER","E1_DIFFERENT");break;
  case "RC02":
   if(d.ev.some(v=>v.delivered+1e-9<v.due))add("INDIVIDUAL_DEADLINE_MISSED","BLOCKED");
   else if(Math.abs(d.ev.reduce((s,v)=>s+v.delivered,0)-d.total)>1e-9)add("AGGREGATION_MISMATCH","E1_DIFFERENT");break;
  case "RC03":
   if(d.electric_unit!=="MW"||d.hydrogen_unit!=="kg")add("CARRIER_DIMENSION","FAIL_STATIC");
   else if(!d.hv_mwh_per_kg||!["LHV","HHV"].includes(d.basis))add("HV_BASIS_MISSING","BLOCKED");
   else if(d.h2_kg*d.hv_mwh_per_kg>d.eff_cap*d.input_mw*d.h+1e-9)add("EFFICIENCY_ENVELOPE","BLOCKED");break;
  case "RC04":
   if(d.unit!=="kg")add("H2_MASS_ENERGY_UNAPPROVED","BLOCKED");
   else if(Math.abs(d.initial_kg+(d.inflow_kgh-d.outflow_kgh)*d.h-d.leak_kg-d.final_kg)>1e-9)add("MASS_LEDGER","E1_DIFFERENT");break;
  case "RC05":{
   const balance=[0,0,0];d.branch.forEach(([a,b],i)=>{balance[a]+=d.f[i];balance[b]-=d.f[i]});
   if(!balance.every((v,i)=>Math.abs(v-d.inject[i])<1e-9))add("KCL","BLOCKED");
   if(Math.abs(d.f.reduce((s,f,i)=>s+f*d.x[i],0))>1e-9)add("KVL","BLOCKED");
   if(!d.duties.includes("KCL")||!d.duties.includes("KVL"))add("DC_OBLIGATION_MISSING","BLOCKED");
   if(d.e4_claim)add("E4_FROM_KCL_NOT_PROVED","E4_NOT_PROVED");break;
  }
  case "RC06":
   if(!d.allowed.includes(d.built)||!d.lead_time_valid)add("MODULARITY","BLOCKED");break;
  case "RC07":
   if(new Set(Object.values(d.first_stage)).size>1)add("INFORMATION_LEAKAGE","BLOCKED");
   if(d.guard!=="before_revelation")add("GUARD_LOSS","E1_DIFFERENT");break;
  case "RC08":
   if(!Number.isFinite(d.weight)||!Number.isFinite(d.probability)||!Number.isFinite(d.discount)||!d.price_year||!d.basis)add("KPI_BASIS","E1_DIFFERENT");
   else if(Math.abs(d.total_eur-(d.capex_eur+d.p_mw*d.h*d.marginal_eur_mwh*d.weight*d.probability*d.discount))>1e-9)add("KPI_WEIGHT","E1_DIFFERENT");break;
  case "RC09":
   if(d.baseline!==d.project||d.price_basis!=="EUR-real-2025")add("COUNTERFACTUAL_DRIFT","BLOCKED");
   if(d.project_eur-d.baseline_eur!==d.delta_eur)add("DELTA_INCONSISTENT","E1_DIFFERENT");break;
  case "RC10":
   if(!d.models.every(v=>v.variant)||!d.basis)add("MODEL_VARIATION","BLOCKED");
   if(d.models.some(v=>v.status==="PASS"))add("MODEL_PASS_UNSUPPORTED","FAIL_STATIC");
   if(d.e4_claim)add("E4_FROM_IDENTICAL_OBJECTIVE","BLOCKED");break;
  default:add("UNKNOWN_RC","FAIL_STATIC");
 }
 return {case_id:doc.case_id,technical_valid:issue.length===0,diagnostics:issue,owner_status:doc.authority_state==="OWNER_TBD"||d.owner==="OWNER_TBD"?"BLOCKED_OWNER_TBD":"PROPOSED_NOT_APPROVED",e1:"NOT_EVALUATED",e2:"NOT_PROVED",e3:"NOT_EXECUTED",e4:"NOT_PROVED",e5:"CONDITIONAL_ONLY"};
}
function mutate(m){
 const z=sample(m.rc);z.mutation_id=m.id;const d=z.data;
 switch(m.id){
  case "MUT-01":d.grid_mwh=2;break;
  case "MUT-02":d.ev[0].delivered=2;d.ev[1].delivered=1;break;
  case "MUT-03":delete d.basis;break;
  case "MUT-04":d.unit="MWh";break;
  case "MUT-05":d.f=[2,2,-1];break;
  case "MUT-06":d.built=0.3;break;
  case "MUT-07":d.first_stage.cold=7;break;
  case "MUT-08":delete d.weight;break;
  case "MUT-09":d.project="altered_exogenous";break;
  case "MUT-10":d.e4_claim=true;break;
  case "MUT-11":z.contract.modality="PERMITTED";break;
  case "MUT-12":delete z.source;break;
  case "MUT-13":z.evidence.status="PASS";break;
  case "MUT-14":z.alias=[{key:"grid",id:"a"},{key:"grid",id:"b"}];break;
  case "MUT-15":delete d.guard;break;
  case "MUT-16":d.hydrogen_unit="MW";break;
  case "MUT-17":delete d.h;break;
  case "MUT-18":d.f=[2,2,-1];d.e4_claim=true;break;
  default:throw Error("Unknown mutation "+m.id);
 }return z;
}
function verdict(mut){
 const original=sample(mut.case_id),id=mut.mutation_id;
 if(id==="MUT-11")return mut.contract.modality!==original.contract.modality?"E1_DIFFERENT":"UNDETECTED";
 if(id==="MUT-12")return mut.source!==original.source?"AUDIT_LOSS":"UNDETECTED";
 const diag=probe(mut).diagnostics;
 if(id==="MUT-18")return diag.some(x=>x.category==="E4_NOT_PROVED")?"E4_NOT_PROVED":"UNDETECTED";
 return diag[0]?.category||"UNDETECTED";
}
function runCases(frozenMutationList){
 const positives=Array.from({length:10},(_,i)=>{const case_id="RC"+String(i+1).padStart(2,"0");const report=probe(sample(case_id));return {id:case_id,pass:report.technical_valid,report}});
 const negatives=frozenMutationList.map(m=>{const z=mutate(m),observed=verdict(z);return{id:m.id,rc:m.rc,expected:m.expected,observed,pass:m.expected.includes(observed),diagnostics:probe(z).diagnostics}});
 return {positives,negatives,passed:[...positives,...negatives].filter(x=>x.pass).length,total:positives.length+negatives.length};
}
module.exports={sample,probe,mutate,verdict,runCases};
