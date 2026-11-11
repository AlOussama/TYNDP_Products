// ML-R02 research; integrated bespoke AST, NOT SysML/LinkML standard implementation.
import {readFileSync} from "node:fs";
import {dirname,resolve} from "node:path";
import {fileURLToPath} from "node:url";
const dir=dirname(fileURLToPath(import.meta.url));

function validateB(m) {
 const e=[],E=s=>e.push(s),nodes=m.nodes||[],N=id=>nodes.find(n=>n.id===id)||{},f=m.fixture||{},cy=["CY1","CY2","CY3","CY4","CY5"];
 if(m.version!=="0.1.0"||!String(m.status).startsWith("RESEARCH_ONLY")||m.requirements?.length!==48||new Set(m.requirements||[]).size!==48)E("model_baseline_version");
 if(new Set(nodes.map(n=>n.id)).size!==nodes.length)E("unique_entities");
 if(JSON.stringify(N("study").years)!=="[2035,2040,2050]")E("years");
 const ws=N("weather");
 if(ws.kind!=="WeatherSet"||JSON.stringify(ws.ids)!==JSON.stringify(cy)||ws.scope!=="shared_across_years"||cy.some(c=>ws.symbols?.[c]!==`w_${c}`))E("weather_scope");
 const w=f.weight_binding||{};
 if(Object.keys(w).sort().join()!==cy.slice().sort().join()||cy.some(c=>!Number.isFinite(w[c])||w[c]<0)||Math.abs(cy.reduce((v,c)=>v+Number(w[c]||0),0)-1)>1e-9)E("weather_binding");
 const d=N("load"),t=d.interval||{};
 if(d.kind!=="Dataset"||!d.source_ref||!d.unit||d.timezone!=="UTC"||!t.start?.endsWith("Z")||!t.end?.endsWith("Z")||!(Date.parse(t.end)>Date.parse(t.start)))E("dataset_clock_provenance");
 if(d.class==="ACTUAL"&&!d.sha256)E("actual_hash_required");
 const v=N("x"),by=f.decision_by_weather||{};
 if(v.kind!=="Decision"||JSON.stringify(v.indices)!=='["year","candidate"]'||v.shared_across!=="weather"||v.candidate!=="C1")E("nonanticipative_signature");
 if(cy.some(c=>!Number.isFinite(by[c])||Math.abs(by[c]-by.CY1)>1e-9||by[c]<v.lower||by[c]>v.upper))E("nonanticipative_fixture");
 const line=N("L1"),dc=f.branch_flow||{};
 if(line.kind!=="PhysicalBranch"||line.law!=="DC_KIRCHHOFF")E("dc_law");
 if(!Number.isFinite(dc.flow_mw)||Math.abs(dc.flow_mw-line.b_mw_per_rad*(dc.theta_from-dc.theta_to))>1e-9)E("dc_microtest");
 const link=N("C1");
 if(link.kind!=="MarketLink"||link.law!=="CONTROLLABLE_NTC_LINK")E("market_link_law");
 if(!Number.isFinite(f.market_flow_mw)||f.market_flow_mw>link.forward_mw||f.market_flow_mw< -link.reverse_mw)E("market_link_bounds");
 const tr=N("T-P06");
 if(tr.kind!=="Transformation"||!tr.source_ref||!tr.busmap_ref||!tr.provenance_ref||tr.output_classes?.length!==6||!tr.quality_oracle)E("reduction_provenance");
 if(N("P15").kind!=="ConditionalStage"||N("P15").optional!==true||(N("P15").enabled&&!N("P15").cap_ref))E("conditional_opf");
 if(N("N1").kind!=="Output"||N("N1").semantic_type!=="SYSTEM_NEED"||!N("N1").formula_ref)E("output_semantics");
 const traces=(m.edges||[]).filter(x=>x.relation==="verified_by");
 if(traces.length!==9)E("case_trace_count");
 for(const t of traces)if(!m.requirements?.includes(t.source)||N(t.target).kind!=="Verification"||N(t.target).requirement!==t.source)E("broken_trace");
 for(const t of m.edges||[])if(!nodes.some(n=>n.id===t.target))E("dangling_edge");
 return {structural_status:e.length?"FAIL_CLOSED":"PASS_SYNTHETIC_STRUCTURAL",errors:e,math_conformity:"NOT_DEMONSTRATED",blocked_oracles:["network_reduction","kpi","authority","actual_data"]};
}
function changesB(base) {
 const mk=(name,fn)=>{let x=JSON.parse(JSON.stringify(base));fn(x);return {name,x,expected:"FAIL_CLOSED"};},get=(x,id)=>x.nodes.find(n=>n.id===id);
 return [{name:"BASE_VALID_STRUCTURE_ONLY",x:base,expected:"PASS_SYNTHETIC_STRUCTURAL"},
 mk("RC01_IDS",x=>get(x,"weather").ids[4]="CY6"),
 mk("RC01_WEIGHTS",x=>x.fixture.weight_binding.CY1=0.5),
 mk("RC02_NONANT_INDEX",x=>get(x,"x").indices.push("weather")),
 mk("RC02_NONANT_VALUE",x=>x.fixture.decision_by_weather.CY4=55),
 mk("RC03_DC_LAW",x=>get(x,"L1").law="NTC_ONLY"),
 mk("RC03_MARKET_LINK_KIRCHHOFF",x=>get(x,"C1").law="DC_KIRCHHOFF"),
 mk("RC04_REDUCTION_PROVENANCE",x=>delete get(x,"T-P06").busmap_ref),
 mk("RC05_OPTIONAL_NO_CAP",x=>get(x,"P15").enabled=true),
 mk("RC06_OUTPUT_MISLABEL",x=>get(x,"N1").semantic_type="APPROVED_PROJECT"),
 mk("RC07_BROKEN_TRACE",x=>get(x,"VC-029").requirement="MA01-SR-001"),
 mk("RC08_MISSING_DATA",x=>delete get(x,"load").source_ref),
 mk("RC08_SEMANTIC_CONFLICT",x=>get(x,"L1").kind="MarketLink"),
 mk("VERSION_MAJOR_BREAK",x=>x.version="1.0.1")];
}
function suite(cases,fn){return cases.map(t=>{const v=fn(t.x);return {test:t.name,expected:t.expected,observed:v.structural_status,correct:t.expected===v.structural_status,errors:v.errors,math_conformity:v.math_conformity};});}
const x=JSON.parse(readFileSync(resolve(dir,"model.json"),"utf8"));
const results=suite(changesB(x),validateB);
console.log(JSON.stringify({prototype:"B",results},null,2));
if(results.some(t=>!t.correct))process.exitCode=1;
