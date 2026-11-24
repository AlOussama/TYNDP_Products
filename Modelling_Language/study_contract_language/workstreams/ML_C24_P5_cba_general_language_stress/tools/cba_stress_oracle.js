'use strict';
/** ML-C24-P5 CBA-as-stress-case independent synthetic oracle. NOT an executable Study Contract Language, not a CBA methodology implementation or normative approval. */
function makeFixture() {
 const scenarios=[
  {id:"S1",study_year:2030,weather_year:"WX-1",exogenous_digest:"synthetic:exog:s1",weight:0.6,weight_role:"SCENARIO_PROBABILITY",duration_h:1,timezone:"UTC"},
  {id:"S2",study_year:2030,weather_year:"WX-2",exogenous_digest:"synthetic:exog:s2",weight:0.4,weight_role:"SCENARIO_PROBABILITY",duration_h:1,timezone:"UTC"}
 ];
 const models=[
  {id:"M-A",generator_identity:"GEN-A",internal_method:"nodal_angle_dispatch",variation_disclosed:true,allowed_under_study:"CONDITIONAL_NOT_OWNER_APPROVED"},
  {id:"M-B",generator_identity:"GEN-B",internal_method:"aggregated_flow_dispatch",variation_disclosed:true,allowed_under_study:"CONDITIONAL_NOT_OWNER_APPROVED"}
 ];
 const costs={"M-A":[[1200,1100],[1500,1350]],"M-B":[[1220,1120],[1520,1410]]};
 const samples=[];
 for(const model of models)for(let i=0;i<scenarios.length;i++)for(let j=0;j<2;j++){
  const sc=scenarios[i],variant=j===0?"R":"P";
  samples.push({id:`${model.id}:${sc.id}:${variant}`,model_id:model.id,scenario_id:sc.id,case_id:variant,exogenous_digest:sc.exogenous_digest,weather_year:sc.weather_year,project_delta_id:variant==="P"?"P1":null,operating_cost_proxy_eur_per_year:costs[model.id][i][j],unit:"EUR/year",price_year:2025,origin:"SYNTHETIC_FIXTURE_NOT_MODEL_RESULT"});
 }
 return {
  research_kind:"LANGUAGE_BOUNDARY_EXPERIMENT_NOT_CBA_COMPLIANCE",
  study:{id:"STUDY:CBA-DEMO",study_family:"COST_BENEFIT_ANALYSIS",language_scope:"GENERAL_CSNF",study_year:2030,reference_case:"R",project_case:"P",method_profile:"SYNTHETIC-CBA-PROXY-0.1",method_profile_version:"0.1",method_source_status:"RESEARCH_ONLY",study_boundary:"TWO_SYNTHETIC_AREAS"},
  authority:{owner_state:"OWNER_TBD",approval_evidence:null,source_refs:["SRC:TENE","SRC:ENTSOE-CBA4","SRC:ENTSOE-IMP2026-DRAFT","SRC:EXAMPLE"],provenance_revision:"research-r0.1"},
  source_ledger:[
   {id:"SRC:TENE",uri:"https://eur-lex.europa.eu/eli/reg/2022/869/oj",status:"REGULATORY_REFERENCE"},
   {id:"SRC:ENTSOE-CBA4",uri:"https://tyndp.entsoe.eu/explore/resources/guideline-for-cost-benefit-analysis-4.0",status:"DOCUMENTED_REFERENCE"},
   {id:"SRC:ENTSOE-IMP2026-DRAFT",uri:"https://consultations.entsoe.eu/tyndp/tyndp-2026-cba-imp-public-consultation/",status:"CONSULTATION_REFERENCE_NOT_APPROVED"},
   {id:"SRC:EXAMPLE",uri:"synthetic:research-fixture",status:"ILLUSTRATIVE_ONLY"}
  ],
  project:{id:"P1",asset_role:"INTERCONNECTOR",baseline_asset_present:false,allowed_changes:["capacity_MW"],additional_exogenous_changes:[],interdependencies_declared:true},
  scenarios, models, samples,
  observable:{
   id:"OPERATING_COST_PROXY",quantity_kind:"CURRENCY_RATE",unit:"EUR/year",price_year:2025,price_basis:"real_2025",
   value_kind:"COST_PROXY_NOT_SEW",cba_b1_claim:false,positive_benefit_sign:"REFERENCE_MINUS_PROJECT",
   selection_policy:"SINGLE_SYNTHETIC_SAMPLE",weather_aggregation:"SCENARIO_PROBABILITY",double_counting_policy:"NO_OVERLAPPING_COMPONENTS",
   additional_indicator_refs:["SUPPLY_SECURITY","CLIMATE_ADAPTATION"]
  },
  additional_indicators:[
   {id:"SUPPLY_SECURITY",unit:"MWh/year",status:"NOT_EXECUTED",value:null,monetization:"NOT_DEFINED"},
   {id:"CLIMATE_ADAPTATION",unit:"qualitative",status:"NOT_EXECUTED",value:null,monetization:"NOT_DEFINED"}
  ],
  comparison:{pairing:"SAME_MODEL_SAME_SCENARIO",sign:"REFERENCE_MINUS_PROJECT",reference:"R",project:"P",annual_aggregation:"SCENARIO_PROBABILITY",decision_threshold_eur:0,e4_claim:false},
  economics:{cost_currency:"EUR",price_year:2025,capex_eur:830,discount_rate:0.05,horizon_years:10,capex_scope:"SYNTHETIC_ONCE_AT_T0",discount_policy:"EXPLICIT_RESEARCH_EXAMPLE"},
  evidence:{role:"REQUEST",status:"NOT_EXECUTED",run_id:null,artifact_digest:null},
  physical_interfaces:[{id:"PORT:GRID",carrier:"electricity",physical_kind:"active_power",unit:"MW",sign:"INJECTION",direction:"BIDIRECTIONAL"}],
  information:{first_stage:{WX1:1,WX2:1},decision_before_revelation:true},
  sensitivities:{cases:["demand_low","demand_high"],status:"SPECIFIED_NOT_EXECUTED"}
 };
}
function evaluateFixture(c){
 const diagnostics=[],blockers=[];
 const add=(code,path,reason)=>diagnostics.push({code,path,reason});
 const block=(code,path)=>blockers.push({code,path});
 const one=(x)=>x&&typeof x==="object";
 if(!one(c)||!one(c.study))return {status:"FAIL_STATIC_FRAGMENT",diagnostics:[{code:"STUDY_MISSING",path:"$.study"}],blockers:[]};
 if(c.study.language_scope!=="GENERAL_CSNF")add("CORE_SCOPE_DRIFT","$.study.language_scope","Use case must not redefine generic language");
 if(!c.study.id||!c.study.method_profile||!c.study.method_profile_version||c.study.method_source_status!=="RESEARCH_ONLY")add("METHOD_PROFILE_UNVERSIONED_OR_PREMATURE","$.study","Method/pin/status required");
 const sourceIds=new Set((c.source_ledger||[]).map(x=>x.id));
 if(!Array.isArray(c.authority?.source_refs)||!c.authority.source_refs.length||c.authority.source_refs.some(x=>!sourceIds.has(x)))add("SOURCE_LEDGER_LOSS","$.authority.source_refs","Immutable per-source identity required");
 if(c.authority?.owner_state==="OWNER_TBD")block("OWNER_UNRESOLVED","$.authority.owner_state");
 else if(c.authority?.owner_state==="APPROVED"&&!c.authority?.approval_evidence)add("UNSUPPORTED_OWNER_APPROVAL","$.authority","No implicit owner approval");
 else if(!["APPROVED","OWNER_TBD","PROPOSED","UNKNOWN"].includes(c.authority?.owner_state))add("OWNER_STATE_INVALID","$.authority.owner_state");
 if(!c.authority?.provenance_revision)add("PROVENANCE_REVISION_MISSING","$.authority.provenance_revision");
 if((c.source_ledger||[]).some(s=>s.id==="SRC:ENTSOE-IMP2026-DRAFT"&&s.status!=="CONSULTATION_REFERENCE_NOT_APPROVED"))add("CONSULTATION_SOURCE_PROMOTION","$.source_ledger","A consultation is not owner-approved");
 if(c.project?.id!=="P1"||c.project?.baseline_asset_present!==false||c.project?.interdependencies_declared!==true||!Array.isArray(c.project?.allowed_changes)||!c.project.allowed_changes.includes("capacity_MW")||c.project.additional_exogenous_changes?.length)add("PROJECT_SCOPE_DRIFT","$.project","Reference and project intervention must remain explicit");
 const scenarios=new Map(),models=new Map(),pairs=new Map();
 for(const [i,s] of (c.scenarios||[]).entries()){
  const path=`$.scenarios[${i}]`;
  if(!s.id||scenarios.has(s.id))add("SCENARIO_ID_INVALID",path+".id");
  scenarios.set(s.id,s);
  if(!s.exogenous_digest||!s.weather_year) add("SCENARIO_PROVENANCE",""+path,"Missing weather/source identity");
  if(!Number.isFinite(s.weight)||s.weight<0) add("SCENARIO_WEIGHT_INVALID",path+".weight","Nonnegative explicit sample probability required");
  if(s.weight_role!=="SCENARIO_PROBABILITY")add("WEIGHT_ROLE_CONFLATION",path+".weight_role","MC / integration weight is distinct from sample probability");
  if(!(s.duration_h>0)||s.timezone!=="UTC")add("TIME_SUPPORT_INVALID",path,"Explicit duration and calendar reference required for this sample");
 }
 if((c.scenarios||[]).length!==2)add("SCENARIO_POPULATION","$.scenarios","Frozen synthetic comparison has two scenarios");
 else if(Math.abs((c.scenarios||[]).reduce((s,x)=>s+(Number.isFinite(x.weight)?x.weight:0),0)-1)>1e-12)add("SCENARIO_WEIGHT_SUM","$.scenarios","Research sample probability weights must total 1");
 for(const [i,m] of (c.models||[]).entries()){
  if(!m.id||models.has(m.id))add("MODEL_ID_INVALID",`$.models[${i}]`);
  models.set(m.id,m);
  if(!m.variation_disclosed||m.allowed_under_study!=="CONDITIONAL_NOT_OWNER_APPROVED")add("MODEL_VARIATION_NOT_DISCLOSED",`$.models[${i}]`,"Variation is conditional, not automatically authorised");
  if(!m.generator_identity)add("MODEL_GENERATOR_ID_MISSING",`$.models[${i}]`);
 }
 if((c.models||[]).length!==2||new Set((c.models||[]).map(x=>x.generator_identity)).size!==2)add("INDEPENDENCE_IDENTITY_COLLISION","$.models","Distinct generators are an assertion, not proof of independence");
 for(const [i,r] of (c.samples||[]).entries()){
  const path=`$.samples[${i}]`,s=scenarios.get(r.scenario_id);
  if(!s||!models.has(r.model_id)){add("UNKNOWN_SAMPLE_REFERENCE",path,"Sample refers to unknown model or scenario");continue}
  if(!["R","P"].includes(r.case_id)){add("CASE_ROLE_INVALID",path);continue}
  const key=r.model_id+"/"+r.scenario_id+"/"+r.case_id;
  if(pairs.has(key))add("DUPLICATE_PAIR_MEMBER",path);
  pairs.set(key,r);
  if(r.exogenous_digest!==s.exogenous_digest||r.weather_year!==s.weather_year)add("EXOGENOUS_SNAPSHOT_DRIFT",path,"R/P must reference same scenario input");
  if((r.case_id==="R"&&r.project_delta_id!==null)||(r.case_id==="P"&&r.project_delta_id!==c.project?.id))add("PROJECT_DELTA_MISASSIGNED",path,"Project intervention must be absent from R");
  if(r.unit!==c.observable?.unit||r.price_year!==c.observable?.price_year)add("OUTPUT_BASIS_MISMATCH",path,"Unit and price-year must match");
  if(!Number.isFinite(r.operating_cost_proxy_eur_per_year))add("COST_SAMPLE_TYPE",path);
  if(r.origin!=="SYNTHETIC_FIXTURE_NOT_MODEL_RESULT")add("RESULT_PROVENANCE_PROMOTED",path,"Do not present synthetic numbers as runs");
 }
 for(const model of models.values())for(const s of scenarios.values())for(const kind of ["R","P"])if(!pairs.has(model.id+"/"+s.id+"/"+kind))add("PAIR_INCOMPLETE",`$.samples`,model.id+"/"+s.id+"/"+kind);
 if(c.comparison?.pairing!=="SAME_MODEL_SAME_SCENARIO"||c.comparison?.reference!=="R"||c.comparison?.project!=="P")add("CROSS_MODEL_PAIRING_FORBIDDEN","$.comparison","Paired deltas within each model and scenario only");
 if(c.comparison?.sign!=="REFERENCE_MINUS_PROJECT"||c.observable?.positive_benefit_sign!=="REFERENCE_MINUS_PROJECT")add("BENEFIT_SIGN_CONVENTION","$.comparison.sign");
 if(c.comparison?.annual_aggregation!=="SCENARIO_PROBABILITY"||c.observable?.weather_aggregation!=="SCENARIO_PROBABILITY")add("AGGREGATION_ROLE_MISMATCH","$.comparison");
 if(c.observable?.value_kind!=="COST_PROXY_NOT_SEW"||c.observable?.cba_b1_claim!==false)add("COST_PROXY_MISLABELED_AS_SEW","$.observable","Operating-cost proxy cannot be asserted as system welfare B1");
 if(!c.observable?.selection_policy)add("OBSERVABLE_SELECTION_UNDEFINED","$.observable.selection_policy");
 if(!c.observable?.double_counting_policy||c.observable.double_counting_policy!=="NO_OVERLAPPING_COMPONENTS")add("KPI_DOUBLE_COUNTING_POLICY","$.observable.double_counting_policy");
 if(c.observable?.price_basis!=="real_2025")add("KPI_PRICE_BASIS_MISSING","$.observable.price_basis");
 if(!Array.isArray(c.additional_indicators)||c.additional_indicators.length!==2)add("NON_MONETIZED_INDICATORS_MISSING","$.additional_indicators");
 for(const [i,v] of (c.additional_indicators||[]).entries())if(v.status==="NOT_EXECUTED"&&v.value!==null)add("UNKNOWN_COERCED_TO_NUMBER",`$.additional_indicators[${i}]`,"Unknown indicator cannot become zero");
 if(c.evidence?.status!=="NOT_EXECUTED"||c.evidence?.role!=="REQUEST")add("EVIDENCE_PROMOTION_UNSUPPORTED","$.evidence","Synthetic values are not independent model execution");
 else block("MODEL_EVIDENCE_NOT_EXECUTED","$.evidence");
 if(!c.economics||c.economics.cost_currency!=="EUR"||c.economics.price_year!==2025)add("DISCOUNT_CURRENCY_BASIS","$.economics","Cost and observable price basis must agree");
 if(!Number.isFinite(c.economics?.discount_rate)||c.economics.discount_rate<0||c.economics.discount_rate>=1||!Number.isInteger(c.economics?.horizon_years)||c.economics.horizon_years<=0)add("DISCOUNT_POLICY_INVALID","$.economics");
 if(!Number.isFinite(c.economics?.capex_eur)||c.economics.capex_eur<0)add("CAPEX_INVALID","$.economics.capex_eur");
 if(c.comparison?.e4_claim) add("E4_UNSUPPORTED","$.comparison.e4_claim","Equal KPIs never establish feasible-set equivalence");
 if(!Array.isArray(c.physical_interfaces)||c.physical_interfaces.some(p=>p.carrier==="electricity"&&(p.physical_kind!=="active_power"||!["MW","kW"].includes(p.unit)))||c.physical_interfaces.some(p=>p.carrier==="hydrogen"&&(p.physical_kind!=="mass_flow"||!["kg/h","kg/s"].includes(p.unit)))||c.physical_interfaces.some(p=>!["electricity","hydrogen"].includes(p.carrier)))add("CARRIER_UNIT_TYPE_MISMATCH","$.physical_interfaces");
 if(c.information?.decision_before_revelation===true&&new Set(Object.values(c.information.first_stage||{})).size>1)add("STAGE1_INFORMATION_LEAKAGE","$.information");
 if(c.sensitivities?.status!=="SPECIFIED_NOT_EXECUTED")add("SENSITIVITY_EXECUTION_PROMOTION","$.sensitivities");
 else block("SENSITIVITY_NOT_EXECUTED","$.sensitivities");
 block("CBA_METHOD_NOT_OWNER_APPROVED","$.study.method_profile");
 const numeric={};
 if(diagnostics.length===0){
  const pvfactor=Array.from({length:c.economics.horizon_years},(_,i)=>Math.pow(1+c.economics.discount_rate,-(i+1))).reduce((a,b)=>a+b,0);
  for(const m of models.values()){
   let annual=0;
   for(const s of scenarios.values()){
    const R=pairs.get(`${m.id}/${s.id}/R`),P=pairs.get(`${m.id}/${s.id}/P`);
    annual+=s.weight*(R.operating_cost_proxy_eur_per_year-P.operating_cost_proxy_eur_per_year);
   }
   numeric[m.id]={illustrative_annual_cost_saving_eur:annual,illustrative_npv_proxy_eur:annual*pvfactor-c.economics.capex_eur,decision_sign:Math.sign(annual*pvfactor-c.economics.capex_eur)};
  }
 }
 return {status:diagnostics.length?"FAIL_STATIC_FRAGMENT":"STATIC_FRAGMENT_VALID_WITH_BLOCKERS",diagnostics,blockers,synthetic_numeric_results:numeric,e1:"NOT_EVALUATED_AS_CSNF",e2:"NOT_PROVED",e3:"NOT_EXECUTED_REAL_MODELS",e4:"NOT_PROVED",e5:"NOT_ASSESSED_WITH_FULL_CONFORMANCE"};
}
const mutations=[
  ["M01","PAIR_INCOMPLETE",c=>{c.samples[1].model_id="M-B";}],
  ["M02","EXOGENOUS_SNAPSHOT_DRIFT",c=>{c.samples[1].exogenous_digest="synthetic:other";}],
  ["M03","SCENARIO_WEIGHT_INVALID",c=>{c.scenarios[0].weight=null;}],
  ["M04","SCENARIO_WEIGHT_SUM",c=>{c.scenarios[0].weight=0.8;}],
  ["M05","OUTPUT_BASIS_MISMATCH",c=>{c.samples[0].unit="MWh";}],
  ["M06","OUTPUT_BASIS_MISMATCH",c=>{c.samples[0].price_year=2024;}],
  ["M07","BENEFIT_SIGN_CONVENTION",c=>{c.comparison.sign="PROJECT_MINUS_REFERENCE";}],
  ["M08","COST_PROXY_MISLABELED_AS_SEW",c=>{c.observable.value_kind="B1_SEW";c.observable.cba_b1_claim=true;}],
  ["M09","UNSUPPORTED_OWNER_APPROVAL",c=>{c.authority.owner_state="APPROVED";}],
  ["M10","EVIDENCE_PROMOTION_UNSUPPORTED",c=>{c.evidence.status="PASS";}],
  ["M11","SOURCE_LEDGER_LOSS",c=>{c.source_ledger=[];}],
  ["M12","MODEL_VARIATION_NOT_DISCLOSED",c=>{c.models[1].variation_disclosed=false;}],
  ["M13","PROJECT_SCOPE_DRIFT",c=>{c.project.additional_exogenous_changes.push("demand");}],
  ["M14","PROJECT_DELTA_MISASSIGNED",c=>{c.samples[1].project_delta_id=null;}],
  ["M15","CROSS_MODEL_PAIRING_FORBIDDEN",c=>{c.comparison.pairing="CROSS_MODEL";}],
  ["M16","TIME_SUPPORT_INVALID",c=>{c.scenarios[0].duration_h=0;}],
  ["M17","UNKNOWN_COERCED_TO_NUMBER",c=>{c.additional_indicators[0].value=0;}],
  ["M18","CARRIER_UNIT_TYPE_MISMATCH",c=>{c.physical_interfaces[0].carrier="hydrogen";c.physical_interfaces[0].physical_kind="mass_flow";c.physical_interfaces[0].unit="MW";}],
  ["M19","PROJECT_DELTA_MISASSIGNED",c=>{c.samples[0].project_delta_id="P1";}],
  ["M20","DISCOUNT_POLICY_INVALID",c=>{c.economics.discount_rate=-0.1;}],
  ["M21","INDEPENDENCE_IDENTITY_COLLISION",c=>{c.models[1].generator_identity="GEN-A";}],
  ["M22","DISCOUNT_CURRENCY_BASIS",c=>{c.economics.cost_currency="GBP";}],
  ["M23","WEIGHT_ROLE_CONFLATION",c=>{c.scenarios[0].weight_role="MONTE_CARLO_OUTAGE_FREQUENCY";}],
  ["M24","OBSERVABLE_SELECTION_UNDEFINED",c=>{c.observable.selection_policy=null;}],
  ["M25","UNKNOWN_SAMPLE_REFERENCE",c=>{c.samples[0].scenario_id="future_unknown";}],
  ["M26","CONSULTATION_SOURCE_PROMOTION",c=>{c.source_ledger[2].status="FINAL_APPROVED";}],
  ["M27","METHOD_PROFILE_UNVERSIONED_OR_PREMATURE",c=>{delete c.study.method_profile_version;}],
  ["M28","KPI_DOUBLE_COUNTING_POLICY",c=>{c.observable.double_counting_policy="ADD_EVERY_COMPONENT";}],
  ["M29","STAGE1_INFORMATION_LEAKAGE",c=>{c.information.first_stage.WX2=2;}],
  ["M30","E4_UNSUPPORTED",c=>{c.comparison.e4_claim=true;}]
];
function runSuite(){
 const input=makeFixture(), base=evaluateFixture(input);
 const clone=x=>JSON.parse(JSON.stringify(x));
 const positives=[
 {id:"P01_BASE_STRUCTURAL",ok:base.status==="STATIC_FRAGMENT_VALID_WITH_BLOCKERS"&&base.blockers.some(x=>x.code==="OWNER_UNRESOLVED")},
 {id:"P02_SYNTHETIC_NPV_SIGNS",ok:base.synthetic_numeric_results["M-A"]?.decision_sign===1&&base.synthetic_numeric_results["M-B"]?.decision_sign===-1},
 {id:"P03_NO_FALSE_MODEL_EVIDENCE",ok:base.e3==="NOT_EXECUTED_REAL_MODELS"&&base.e4==="NOT_PROVED"&&base.e5==="NOT_ASSESSED_WITH_FULL_CONFORMANCE"},
 {id:"P04_SAMPLE_ORDER_PERMUTATION",ok:(()=>{const x=clone(input);x.samples.reverse();return JSON.stringify(evaluateFixture(x).synthetic_numeric_results)===JSON.stringify(base.synthetic_numeric_results)})()},
 {id:"P05_MODEL_DIVERSITY_NOT_MODEL_FAIL",ok:base.diagnostics.length===0&&Object.values(base.synthetic_numeric_results).some(x=>x.decision_sign<0)},
 {id:"P06_UNKNOWN_MONETISATION_PRESERVED",ok:input.additional_indicators.every(x=>x.status==="NOT_EXECUTED"&&x.value===null)}
 ];
 const negative=mutations.map(([id,code,edit])=>{const c=clone(input);edit(c);const res=evaluateFixture(c);return{id,expected_diagnostic:code,actual_diagnostics:res.diagnostics.map(x=>x.code),passed:res.status==="FAIL_STATIC_FRAGMENT"&&res.diagnostics.some(x=>x.code===code)};});
 return {run_id:"P5-CBA-SYNTHETIC-V8-20261124-r0.1",baseline:base,positive:positives,negative,passed:positives.filter(x=>x.ok).length+negative.filter(x=>x.passed).length,total:positives.length+negative.length,notes:["Independent synthetic CBA research oracle only; not C20/C21 parser or CSNF validation","OWNER_TBD and NOT_EXECUTED remain blockers","NPV is illustrative operating-cost-proxy sensitivity, not approved CBA-B1/SEW or decision"]};
}
module.exports={makeFixture,evaluateFixture,mutations,runSuite};
