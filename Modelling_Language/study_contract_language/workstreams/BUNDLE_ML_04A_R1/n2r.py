"""Integrated finite profile experiment using the unchanged original N1/C21/N2 code."""
import copy, json
from pathlib import Path
from n1r import need, fields, unique, digest, file_sha, pins, decode, typed, lower, run, c21, PIN, quantity
from n7 import verified_file, authority, contribution_table, lineage
from profile_engine import Engine, read, rational

def evaluate(source,syntax,study_path,trust_path):
    root=Path(study_path).resolve().parent;study=read(study_path);manifest=read(trust_path)
    fields(study,('schema','id','version','method_ref','data_ref','contract_ref','parameters','status','slot','ledger_policy'));need(study['schema']=='study-r1','STUDY_VERSION')
    method=read(verified_file(root,study['method_ref']));data=read(verified_file(root,study['data_ref']));source_doc=read(verified_file(root,method['source']));auth=authority(source_doc,manifest,method,study)
    d,blocked=typed(decode(source,syntax));canonical,_=c21.normalize(lower(d));need(study['contract_ref']==digest(canonical),'CONTRACT_SEMANTIC_HASH')
    slots={s['id']:s for s in d['frame']['method_slots']};slot=slots[study['slot']];obs={o['id']:o for o in d['observables']};refs={r['id']:r for r in d['referents']};dom={a['id']:a for a in d['frame']['domains']};inputs={a['id']:a for a in d['frame']['data_inputs']};need(any(a['role']=='SOURCE' and a['immutable_ref']==source_doc['id'] and a['revision']==source_doc['version'] for a in d['authorities']),'CONTRACT_SOURCE_IDENTITY')
    fields(data,('schema','engine_data','bindings','contexts','cases','contributions'));need(data['schema']=='snapshot-r1','DATA_VERSION');ed=data['engine_data'];bindings=data['bindings'];need(set(bindings)==set(ed['series']),'BINDINGS')
    for i,a in ed['axes'].items():need(i in dom and a['role']==dom[i]['kind'] and a['ids']==dom[i]['members'],'AXIS_CONTEXT')
    for k,b in bindings.items():
        fields(b,('role','observable','case','data_ref'));s=ed['series'][k];need(b['role'] in ('contribution','auxiliary'),'BINDING_ROLE')
        if b['role']=='contribution':
            o=obs[b['observable']];q=o['quantity'];need(b['data_ref']=='' and s['role']=='value','CONTRIBUTION_ROLE');need(b['observable'] in slot['observables'] and q['unit']==s['unit'] and q.get('basis','')==s['basis'] and [v['domain'] for v in o['bindings']]==s['axes'],'OBSERVABLE_SIGNATURE');need(b['case'] in data['cases'] and data['cases'][b['case']]['referent']==o['subject'],'CASE_SUBJECT')
        else:
            a=inputs[b['data_ref']];need(b['observable']==b['case']=='' and b['data_ref'] in slot['data_inputs'] and (s['unit'],s['basis'],s['axes'])==(a['unit'],a['basis'],a['axes']) and s['role']==('value' if a['role']=='period_count' else a['role']),'AUXILIARY_INPUT');need(a['role']!='period_count' or all(rational(row['value'])>=0 and rational(row['value']).denominator==1 for row in s['rows']),'PERIOD_COUNT')
    need({b['observable'] for b in bindings.values() if b['role']=='contribution'}==set(slot['observables']),'OBSERVABLE_COVERAGE');need({b['data_ref'] for b in bindings.values() if b['role']=='auxiliary'}==set(slot['data_inputs']),'DATA_INPUT_COVERAGE')
    for k,case in data['cases'].items():fields(case,('referent','exogenous_ref'));need(case['referent'] in refs and case['exogenous_ref'] in data['contexts'],'CASE_CONTEXT')
    for k,ctx in data['contexts'].items():need(k==digest(ctx),'EXOGENOUS_CONTENT_HASH')
    matched=set()
    for pair in ed['pairs']:
        a,b=bindings[pair['reference']],bindings[pair['alternative']];need(a['case']!=b['case'],'COUNTERFACTUAL_IDENTITY');ca,cb=data['cases'][a['case']],data['cases'][b['case']];need(ca['exogenous_ref']==cb['exogenous_ref']==pair['reference_snapshot']==pair['alternative_snapshot'],'EXOGENEITY');matches=[r['id'] for r in d['relations'] if r['kind']=='counterfactual_of' and r['from']==cb['referent'] and r['to']==ca['referent']];need(len(matches)==1 and matches[0] not in matched,'COUNTERFACTUAL_RELATION');matched.add(matches[0])
    need(matched=={r['id'] for r in d['relations'] if r['kind']=='counterfactual_of'},'COUNTERFACTUAL_COVERAGE')
    # The existing N2 evaluator requires its original schema; explicit version mapping.
    s={k:study[k] for k in ('id','version','method_ref','data_ref','contract_ref','parameters','status')};s['schema']='profile-r1';e=Engine(method,s,ed);result=e.run()
    atoms=contribution_table(data['contributions'],e.series,bindings);ledger=lineage(method,e,atoms,study['ledger_policy'])
    # N2's finite evaluator has already checked the complete rule AST and all declared input/result types.
    # Preserve those rules in the canonical graph, not merely a method ID/hash.
    extension={'schema':'resolved-profile-r1','method_id':method['id'],'method_version':method['version'],'operator_version':method['operator_version'],'inputs':method['inputs'],'rules':method['rules'],'parameter_definitions':method['parameters'],'parameter_values':study['parameters'],'slot':slot,'axes':ed['axes'],'bindings':bindings,'cases':data['cases'],'pairs':ed['pairs'],'resolved_counterfactuals':sorted(matched),'contexts':data['contexts'],'contributions':data['contributions'],'input_data_snapshot':study['data_ref']['sha256'],'ledger_policy':study['ledger_policy'],'owner_state':study['status'],'approval':method['approval'],'assumptions':method['assumptions']}
    chain=run(source,syntax,extension);resolved=chain['normalized']['frame']['resolved_profile'];need(resolved==extension,'METHOD_AST_LOSS')
    # Evaluate FROM the normalized graph as well, rather than only attaching the AST after evaluation.
    nm=copy.deepcopy(method);nm.update(rules=resolved['rules'],inputs=resolved['inputs'],parameters=resolved['parameter_definitions']);ns=copy.deepcopy(s);ns['parameters']=resolved['parameter_values'];ne=Engine(nm,ns,ed);normalized_result=ne.run();need(normalized_result==result,'NORMALIZED_RESULT_MISMATCH');result=normalized_result
    need(lineage(nm,ne,atoms,resolved['ledger_policy'])==ledger,'NORMALIZED_LINEAGE_MISMATCH')
    audit={'chain_audit':chain['audit_digest'],'method_sha256':study['method_ref']['sha256'],'data_sha256':study['data_ref']['sha256'],'study_sha256':file_sha(study_path),'source_sha256':method['source']['sha256'],'trust_sha256':file_sha(trust_path),'authority':auth,'result':result,'lineage':ledger,'code':pins()|{k:file_sha(Path(__file__).parent/k) for k in ('n1r.py','n2r.py','n7.py')},'verification_scope':'FINITE_SYNTHETIC_PROFILE_EVALUATION','request_status':'NOT_EXECUTED','conformance':'NOT_PROVED'}
    receipt={'run_id':'run:'+digest([digest(audit),chain['source_digest'],syntax]),'source_digest':chain['source_digest'],'syntax':syntax,'verification_scope':audit['verification_scope'],'result_status':'EXECUTED_UNJUDGED','contract_request_status':'NOT_EXECUTED'}
    return {'result':result,'chain':chain,'ledger':ledger,'audit':audit,'audit_digest':digest(audit),'receipt':receipt}
