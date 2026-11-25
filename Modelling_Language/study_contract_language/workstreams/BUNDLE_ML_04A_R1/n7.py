"""Finite contribution/provenance controls, not authenticity or owner certification."""
from collections import Counter
from pathlib import Path
from n1r import need, fields, unique, digest, file_sha, ident

def verified_file(root,ref):
    fields(ref,('path','sha256'));need(type(ref['path']) is str and type(ref['sha256']) is str,'SOURCE_REF');p=(root/ref['path']).resolve();need(p.is_relative_to(root) and p.is_file() and file_sha(p)==ref['sha256'],'HASH_OR_PATH');return p

def authority(source,manifest,method,study):
    fields(source,('id','version','status','description'));fields(manifest,('source_id','source_version','source_sha256','authenticity','publication','method_allowlist','ledger_policy_sha256','data_allowlist','contract_allowlist','study_id'))
    need(source['id']==manifest['source_id'] and source['version']==manifest['source_version'] and source['status']=='SYNTHETIC_RESEARCH','SOURCE_IDENTITY')
    need(method['source']['sha256']==manifest['source_sha256'] and study['method_ref']['sha256'] in unique(manifest['method_allowlist']),'METHOD_SOURCE_NOT_PERMITTED');need(digest(study['ledger_policy'])==manifest['ledger_policy_sha256'],'LEDGER_POLICY_NOT_PERMITTED');need(study['id']==manifest['study_id'] and study['data_ref']['sha256'] in unique(manifest['data_allowlist']) and study['contract_ref'] in unique(manifest['contract_allowlist']),'STUDY_CONTEXT_NOT_PERMITTED')
    need(manifest['authenticity']=='UNVERIFIED' and manifest['publication']=='SYNTHETIC' and method['approval']=='RESEARCH_ASSUMPTION' and study['status']=='OWNER_TBD','AUTHORITY_PROMOTION')
    return {'integrity':'VERIFIED_BYTES','authenticity':'UNVERIFIED','publication':'SYNTHETIC','method_authority':'RESEARCH_ASSUMPTION','owner':'OWNER_TBD'}

def contribution_table(rows,series,bindings):
    """Stable atomic identities are distinct from input aliases; overlap is checked per declared method policy."""
    ids=set();atoms={k:Counter() for k in series};coverage=set()
    for r in rows:
        fields(r,('id','series','key','case','observable','event'));i=ident(r['id']);k=r['series'];b=bindings[k];key=tuple(r['key']);need(k in series and key in series[k].values and b['role']=='contribution' and r['case']==b['case'] and r['observable']==b['observable'],'CONTRIBUTION_BINDING');need(type(r['event']) is str and r['event'],'EVENT_ID');need(i not in ids and (k,key) not in coverage,'DUPLICATE_CONTRIBUTION');ids.add(i);coverage.add((k,key));atom=digest([r['case'],list(key),r['event']]);atoms[k][atom]+=1
    expected={(k,key) for k,v in series.items() if bindings[k]['role']=='contribution' for key in v.values};need(coverage==expected,'MISSING_CONTRIBUTION');return atoms

def lineage(method,engine,atoms,policy):
    """Conservative whole-series lineage, exact for same-support affine contributions in this experiment."""
    fields(policy,('schema','id','version','rules','expected'));need(policy['schema']=='ledger-policy-r1','LEDGER_VERSION');ident(policy['id']);need(type(policy['version']) is str and bool(policy['version']),'LEDGER_VERSION');need(set(policy['rules'])==set(method['rules']) and set(policy['expected'])<=set(method['rules']),'LEDGER_POLICY_SCOPE');cache={};active=set()
    def rule(k):
        if k in cache:return cache[k].copy()
        need(k not in active,'LEDGER_CYCLE');active.add(k);v=expr(method['rules'][k]['expr']);mode=policy['rules'][k];need(mode in ('ALLOW_REUSE','DISJOINT'),'LEDGER_POLICY')
        if mode=='DISJOINT':need(all(x==1 for x in v.values()),'SEMANTIC_DOUBLE_COUNT')
        if k in policy['expected']:need(set(v)==set(unique(policy['expected'][k])),'CONTRIBUTION_COMPLETENESS')
        active.remove(k);cache[k]=v;return v.copy()
    def expr(e):
        op=e['op']
        if op=='input':return atoms[e['id']].copy()
        if op=='select_case':return atoms[engine.pairs[e['pair']][e['side']]].copy()
        if op=='rule':return rule(e['id'])
        if op in ('literal','param'):return Counter()
        if op=='weighted_sum':need(not atoms[e['weight']],'CONTRIBUTION_WEIGHT');return expr(e['expr'])
        if op in ('add','sub','mul','div','pow'):
            a,b=expr(e['lhs']),expr(e['rhs'])
            out=set(engine.evaluate(e).type.axes);need((not a or set(engine.evaluate(e['lhs']).type.axes)==out) and (not b or set(engine.evaluate(e['rhs']).type.axes)==out),'CONTRIBUTION_BROADCAST_UNSUPPORTED')
            if op in ('add','sub'):return a+b
            if op=='mul':need(not(a and b),'NONLINEAR_CONTRIBUTION_PRODUCT');return a+b
            if op=='div':need(not b,'CONTRIBUTION_DIVISOR');return a
            need(not(a or b),'CONTRIBUTION_POWER');return Counter()
        raise ValueError('UNKNOWN_LEDGER_OPERATOR')
    return {k:dict(sorted(rule(k).items())) for k in method['rules']}
