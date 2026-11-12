// ML-C06 controlled semantic-change tests (local contract checker, NOT native standard/parser or tool).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {cp,parseCsv,encode,decode,canon,graphErrors,semanticErrors} from './shared/experiment_kernel.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));const read=x=>fs.readFileSync(path.join(root,x),'utf8');const graph=parseCsv(read('frozen_sources/c02_traceability_model.csv')),sem=JSON.parse(read('shared/research_semantics.json'));
const cases=[["CH01_SOURCE_AUTHORITY","O26 draft source authority silently promoted","SOURCE_STATUS_UNAUTHORIZED","sourceclause:O26:SR-001"],["CH02_DATA_PROFILE","Proposed data definition falsely qualified","DATA_QUALIFICATION_UNAUTHORIZED","B01-D001"],["CH03_NEW_MATH_OPERATOR","Undeclared mathematical operator introduced","OPERATOR_COMPATIBILITY","operator:semantic_revision"],["CH04_MANDATORY_TIME","Δt erased from mandatory half-open interval","TIME_UNITS","time:duration_h"],["CH05_BROKEN_SOURCE_REFERENCE","Requirement source reference points to nonexistent clause","DANGLING_REFERENCE","MA01-SR-001"],["CH06_INCOMPATIBLE_REVISION","Unmigrated profile/metamodel/view revision","PROFILE_VERSION_MISMATCH","profile:input"],["CH07_LOSSY_VIEW","A declared source lifecycle status lost on roundtrip","ROUND_TRIP_LOSS","sourceclause:O26:SR-001"],["CH08_PROCESS_ONLY_MISSING","Original process-only data object dropped","PROCESS_ONLY_OBJECT_LOSS","B01-D001"]];
function versionErrors(view){
const err=[];
if(view.architecture==="A"){for(const [name,v] of Object.entries(view.profiles))if(v.version!=="0.1.0")err.push("PROFILE_VERSION_MISMATCH:"+name);}
else if(view.architecture==="B"){if(view.revision!=="0.1.0")err.push("METAMODEL_VERSION_MISMATCH");}
else for(const [name,v] of Object.entries(view.views))if(v.version!=="0.1.0")err.push("VIEW_VERSION_MISMATCH:"+name);
return err;
}
function check(view,which,original){const all=decode(view),find=id=>all.find(x=>x.record_kind==='NODE'&&x.subject_id===id);switch(which){
case'CH01_SOURCE_AUTHORITY':return find('sourceclause:O26:SR-001').lifecycle_state==='O26_CONSULTATION_DRAFT'?[]:['SOURCE_STATUS_UNAUTHORIZED'];
case'CH02_DATA_PROFILE':return find('B01-D001').lifecycle_state==='DOCUMENTED_NEED_NOT_QUALIFIED_PAYLOAD'?[]:['DATA_QUALIFICATION_UNAUTHORIZED'];
case'CH03_NEW_MATH_OPERATOR':case'CH04_MANDATORY_TIME':return semanticErrors(view.semantics);
case'CH05_BROKEN_SOURCE_REFERENCE':case'CH08_PROCESS_ONLY_MISSING':return graphErrors(all);
case'CH06_INCOMPATIBLE_REVISION':return versionErrors(view);
case'CH07_LOSSY_VIEW':return canon(all)===canon(original)?[]:['ROUND_TRIP_LOSS'];
}return['UNKNOWN_CHANGE'];}
function mutate(view,which){const all=decode(view),find=id=>all.find(x=>x.record_kind==='NODE'&&x.subject_id===id);switch(which){
case'CH01_SOURCE_AUTHORITY':find('sourceclause:O26:SR-001').lifecycle_state='OWNER_APPROVED';break;
case'CH02_DATA_PROFILE':find('B01-D001').lifecycle_state='QUALIFIED_DATA';break;
case'CH03_NEW_MATH_OPERATOR':view.semantics.operator_kind='NONLINEAR_UNAPPROVED';break;
case'CH04_MANDATORY_TIME':view.semantics.time.duration_h=null;break;
case'CH05_BROKEN_SOURCE_REFERENCE':all.find(x=>x.record_kind==='EDGE'&&x.subject_id==='MA01-SR-001'&&x.predicate==='DERIVED_FROM').object_id='sourceclause:UNKNOWN';break;
case'CH06_INCOMPATIBLE_REVISION':if(view.architecture==='A')view.profiles.input.version='1.0.0';else if(view.architecture==='B')view.revision='1.0.0';else view.views.input.version='1.0.0';break;
case'CH07_LOSSY_VIEW':find('sourceclause:O26:SR-001').lifecycle_state='';break;
case'CH08_PROCESS_ONLY_MISSING':if(view.architecture==='A')view.profiles.input.rows=view.profiles.input.rows.filter(x=>x.subject_id!=='B01-D001'||x.record_kind!=='NODE');else if(view.architecture==='B')view.nodes=view.nodes.filter(x=>x.row.subject_id!=='B01-D001');else view.views.input.entries=view.views.input.entries.filter(x=>x.canonical.subject_id!=='B01-D001'||x.canonical.record_kind!=='NODE');break;
}}
const cols=['architecture','change_id','expect','observed','verdict','witness_rule','affected_id','description','scope'],results=[];
for(const a of ['A','B','C']){const positive=encode(a,graph,sem);for(const [id,description,witness,affected]of cases){const base=check(positive,id,graph);if(base.length)throw Error('INVALID_BASELINE:'+id+':'+base.join(';'));const mutated=cp(positive);mutate(mutated,id);const errors=check(mutated,id,graph);results.push({architecture:a,change_id:id,expect:'REJECT',observed:errors.length?'REJECT':'ACCEPT',verdict:errors.length?'EXPECTED':'UNEXPECTED',witness_rule:errors.join('|')||'NONE',affected_id:affected,description,scope:'PINNED_CUSTOM_CONTRACT_ONLY'});}}
const q=s=>'"'+String(s).replaceAll('"','""')+'"',csv=cols.join(',')+'\n'+results.map(x=>cols.map(k=>q(x[k])).join(',')).join('\n')+'\n';if(process.argv.includes('--write'))fs.writeFileSync(path.join(root,'semantic_change_test_results.csv'),csv);else if(read('semantic_change_test_results.csv')!==csv)throw Error('RECORDED_CHANGE_RESULTS_DRIFT');console.log(JSON.stringify({changes:cases.length,architecture_repeats:3,checks:results.length,matched:results.filter(x=>x.verdict==='EXPECTED').length},null,2));if(results.some(x=>x.verdict!=='EXPECTED'))process.exitCode=1;
