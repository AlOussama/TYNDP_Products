// ML-R02 research; zero external dependencies; no solver or mathematical conformity certification.
import {readFileSync} from "node:fs";
import {dirname,resolve} from "node:path";
import {fileURLToPath} from "node:url";
const dir=dirname(fileURLToPath(import.meta.url));

function validateA(x) {
 const e=[],E=s=>e.push(s),r=x.registry||{},p=x.profiles||{},f=x.fixture||{},I=p.input||{},P=p.process||{},M=p.math||{},O=p.output||{},V=p.verification||{};
 if(r.status!=="RESEARCH_ONLY_NOT_APPROVED"||r.requirements_catalogue?.ids?.length!==48||new Set(r.requirements_catalogue?.ids||[]).size!==48)E("baseline_status");
 for(const n of ["input","process","math","output","verification"])if(p[n]?.profile_id!==n||p[n]?.version!==r.profile_versions?.[n])E("profile_version:"+n);
 if(JSON.stringify(I.years)!=="[2035,2040,2050]")E("years");
 const cy=["CY1","CY2","CY3","CY4","CY5"],ok=a=>JSON.stringify(a)===JSON.stringify(cy);
 if(!ok(I.weather_ids)||I.weather_by_year?.length!==3||I.weather_by_year.some(y=>!ok(y.ids)||cy.some(c=>y.weight_symbols?.[c]!==`w_${c}`)))E("weather_scope");
 const w=f.weight_binding||{};
 if(Object.keys(w).sort().join()!==cy.slice().sort().join()||cy.some(c=>!Number.isFinite(w[c])||w[c]<0)||Math.abs(cy.reduce((v,c)=>v+Number(w[c]||0),0)-1)>1e-9)E("weather_binding");
 const d=I.dataset||{},t=d.interval||{};
 if(!d.source_ref||!d.unit||d.timezone!=="UTC"||!t.start?.endsWith("Z")||!t.end?.endsWith("Z")||!(Date.parse(t.end)>Date.parse(t.start)))E("dataset_clock_provenance");
 if(d.class==="ACTUAL"&&!d.sha256)E("actual_hash_required");
 const roles=new Map();
 for(const x of I.asset_roles||[]){if(roles.has(x.id)&&roles.get(x.id)!==x.role)E("asset_semantic_conflict");roles.set(x.id,x.role);}
 const v=M.decision||{},by=f.decision_by_weather||{};
 if(JSON.stringify(v.indices)!=='["year","candidate"]'||v.shared_across!=="weather"||v.lower!==0||!Number.isFinite(v.upper))E("nonanticipative_signature");
 if(cy.some(c=>!Number.isFinite(by[c])||Math.abs(by[c]-by.CY1)>1e-9||by[c]<0||by[c]>v.upper))E("nonanticipative_fixture");
 const line=M.physical_branch||{},dc=f.branch_flow||{};
 if(line.law!=="DC_KIRCHHOFF"||roles.get(line.id)!=="physical_branch")E("dc_law");
 if(!Number.isFinite(dc.flow_mw)||Math.abs(dc.flow_mw-line.b_mw_per_rad*(dc.theta_from-dc.theta_to))>1e-9)E("dc_microtest");
 const link=M.candidate_link||{};
 if(link.law!=="CONTROLLABLE_NTC_LINK"||roles.get(link.id)!=="candidate_link")E("market_link_law");
 if(!Number.isFinite(f.market_flow_mw)||f.market_flow_mw>link.forward_mw||f.market_flow_mw< -link.reverse_mw)E("market_link_bounds");
 const tr=P.network_reduction||{};
 if(!tr.source_ref||!tr.target_ref||!tr.busmap_ref||!tr.provenance_ref||tr.output_classes?.length!==6||!tr.quality_oracle)E("reduction_provenance");
 if(P.steps?.length!==18||P.steps?.[0]!=="P00"||P.steps?.[17]!=="P17")E("process_steps");
 if(P.optional_opf?.optional!==true||(P.optional_opf?.enabled&&!P.optional_opf.cap_ref))E("conditional_opf");
 if(O.need?.type!=="SYSTEM_NEED"||!O.kpi?.formula_ref||!O.kpi?.aggregation_ref)E("output_semantics");
 const tests=new Map((V.tests||[]).map(t=>[t.id,t]));
 if(r.traceability?.length!==9)E("case_trace_count");
 for(const t of r.traceability||[])if(!r.requirements_catalogue?.ids?.includes(t.requirement)||tests.get(t.test)?.requirement!==t.requirement||tests.get(t.test)?.case_id!==t.case_id)E("broken_trace:"+t.case_id);
 return {structural_status:e.length?"FAIL_CLOSED":"PASS_SYNTHETIC_STRUCTURAL",errors:e,math_conformity:"NOT_DEMONSTRATED",blocked_oracles:["network_reduction","kpi","authority","actual_data"]};
}
function changesA(base) {
 const mk=(name,fn)=>{let x=JSON.parse(JSON.stringify(base));fn(x);return {name,x,expected:"FAIL_CLOSED"};};
 return [{name:"BASE_VALID_STRUCTURE_ONLY",x:base,expected:"PASS_SYNTHETIC_STRUCTURAL"},
 mk("RC01_IDS",x=>x.profiles.input.weather_by_year[1].ids[4]="CY6"),
 mk("RC01_WEIGHTS",x=>x.fixture.weight_binding.CY1=0.5),
 mk("RC02_NONANT_INDEX",x=>x.profiles.math.decision.indices.push("weather")),
 mk("RC02_NONANT_VALUE",x=>x.fixture.decision_by_weather.CY4=55),
 mk("RC03_DC_LAW",x=>x.profiles.math.physical_branch.law="NTC_ONLY"),
 mk("RC03_MARKET_LINK_KIRCHHOFF",x=>x.profiles.math.candidate_link.law="DC_KIRCHHOFF"),
 mk("RC04_REDUCTION_PROVENANCE",x=>delete x.profiles.process.network_reduction.busmap_ref),
 mk("RC05_OPTIONAL_NO_CAP",x=>x.profiles.process.optional_opf.enabled=true),
 mk("RC06_OUTPUT_MISLABEL",x=>x.profiles.output.need.type="APPROVED_PROJECT"),
 mk("RC07_BROKEN_TRACE",x=>x.profiles.verification.tests.find(t=>t.id==="VC-029").requirement="MA01-SR-001"),
 mk("RC08_MISSING_DATA",x=>delete x.profiles.input.dataset.source_ref),
 mk("RC08_SEMANTIC_CONFLICT",x=>x.profiles.input.asset_roles.push({id:"L1",role:"candidate_link"})),
 mk("VERSION_MAJOR_BREAK",x=>x.profiles.math.version="1.0.0")];
}
function suite(cases,fn){return cases.map(t=>{const v=fn(t.x);return {test:t.name,expected:t.expected,observed:v.structural_status,correct:t.expected===v.structural_status,errors:v.errors,math_conformity:v.math_conformity};});}
const read=f=>JSON.parse(readFileSync(resolve(dir,f),"utf8"));
const x={registry:read("registry.json"),profiles:Object.fromEntries(["input","process","math","output","verification"].map(n=>[n,read("profiles/"+n+".json")])),fixture:read("fixtures/synthetic.json")};
const results=suite(changesA(x),validateA);
console.log(JSON.stringify({prototype:"A",results},null,2));
if(results.some(t=>!t.correct))process.exitCode=1;
