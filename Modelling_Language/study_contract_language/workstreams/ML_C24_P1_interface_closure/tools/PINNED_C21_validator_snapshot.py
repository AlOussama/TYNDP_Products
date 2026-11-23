"""CSNF-C21-0.1: conservative typed-CSNF fragment normalizer, stdlib only.
NOT a language parser, mathematical solver, formal equivalence engine or certification.
"""
from __future__ import annotations
import copy
import hashlib
import json
from decimal import Decimal, InvalidOperation

VERSION = 'CSNF-C21-0.1'
RULES = 'CSNF-R0'
REGISTRY = 'energy-c21-0.1'
COLLECTIONS = ('referents','relations','predicates','assertions','observables','variations','evidences','authorities')
MODALITIES = {'REQUIRED','PROHIBITED','PERMITTED','IMPLEMENTATION_DEFINED','CONDITIONAL'}
DECISIONS = {'APPROVED','PROPOSED','OWNER_TBD','REJECTED','SUPERSEDED','UNKNOWN'}
EVIDENCE_STATUS = {'PASS','FAIL','NOT_EXECUTED','INCONCLUSIVE','NOT_APPLICABLE','BLOCKED'}
CARRIERS = {'electricity','hydrogen','heat','currency'}
UNITS = {
    ('electricity','active_power'): {'MW': Decimal('1'), 'kW': Decimal('.001')},
    ('electricity','energy'): {'MWh': Decimal('1'), 'kWh': Decimal('.001')},
    ('hydrogen','mass_flow'): {'kg/h': Decimal('1'), 'kg/s': Decimal('3600')},
    ('hydrogen','mass'): {'kg': Decimal('1')},
    ('currency','cost'): {'EUR': Decimal('1'), 'kEUR': Decimal('1000'), 'MEUR': Decimal('1000000')},
}
CANON_UNIT = {k: next(iter(v)) for k,v in UNITS.items()}

class CSNFError(ValueError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__('; '.join(x['code']+': '+x['path'] for x in diagnostics if x['severity']=='ERROR'))

def diagnostic(code, path, severity='ERROR', detail=''):
    return {'code':code,'path':path,'severity':severity,'detail':detail}

def normalized_number(value):
    try:
        d=Decimal(str(value))
        if not d.is_finite(): raise ValueError('nonfinite number')
        return format(d.normalize(),'f')
    except (ValueError,InvalidOperation) as exc:
        raise ValueError('invalid decimal quantity') from exc

def quantity(q, path, issues):
    if not isinstance(q,dict):
        issues.append(diagnostic('QUANTITY_TYPE',path));return
    k=(q.get('carrier'),q.get('kind'))
    if k not in UNITS:
        issues.append(diagnostic('CARRIER_KIND',path,detail=str(k)));return
    if q.get('unit') not in UNITS[k]:
        issues.append(diagnostic('UNIT_OR_CONVERSION_BASIS',path,detail='No approved conversion; H2 mass != energy'))
    if q.get('sign') not in ('INJECTION','CONSUMPTION','BIDIRECTIONAL','NONE'):
        issues.append(diagnostic('SIGN_UNDEFINED',path))
    try: normalized_number(q.get('value','0'))
    except ValueError: issues.append(diagnostic('QUANTITY_NUMERIC',path))
    if k==('currency','cost') and not q.get('basis'):
        issues.append(diagnostic('PRICE_BASIS_MISSING',path))


def guard(g,path,issues):
    if g in (True,False,'UNKNOWN'):
        return
    if isinstance(g,dict) and set(g)=={'atom'} and isinstance(g['atom'],str):
        return
    if not isinstance(g,dict):
        issues.append(diagnostic('GUARD_TYPE',path));return
    op=g.get('op');args=g.get('args')
    if op not in ('AND','OR','NOT') or not isinstance(args,list) or len(args)!=(1 if op=='NOT' else len(args)) or (op!='NOT' and len(args)<2):
        issues.append(diagnostic('GUARD_ARITY',path));return
    for i,x in enumerate(args):guard(x,f'{path}.args[{i}]',issues)

def validate(contract):
    out=[]
    if not isinstance(contract,dict):return [diagnostic('CONTRACT_TYPE','$')]
    frame=contract.get('frame')
    if not isinstance(frame,dict):
        out.append(diagnostic('FRAME_REQUIRED','$.frame'))
    else:
        for field,expected in [('schema',VERSION),('ruleset',RULES),('registry',REGISTRY)]:
            if frame.get(field)!=expected:out.append(diagnostic('VERSION_MISMATCH','$.frame.'+field))
        if not frame.get('id'):out.append(diagnostic('FRAME_ID','$.frame.id'))
        time=frame.get('time')
        if isinstance(time,dict) and time.get('duration_unit') not in ('h','min'):
            out.append(diagnostic('TIME_DURATION_UNIT','$.frame.time.duration_unit'))
        if isinstance(time,dict) and time.get('duration') is not None:
            try:
                if Decimal(str(time['duration']))<=0:out.append(diagnostic('DURATION_POSITIVE','$.frame.time.duration'))
            except InvalidOperation:out.append(diagnostic('DURATION_NUMERIC','$.frame.time.duration'))
        if frame.get('imports'):
            out.append(diagnostic('UNAPPROVED_COMPOSITION','$.frame.imports',detail='R10 requires explicit authority and precedence'))
    ids={}
    for collection in COLLECTIONS:
        nodes=contract.get(collection)
        if not isinstance(nodes,list):
            out.append(diagnostic('COLLECTION_REQUIRED','$.'+collection));continue
        for idx,node in enumerate(nodes):
            path=f'$.{collection}[{idx}]'
            if not isinstance(node,dict) or not isinstance(node.get('id'),str) or not node['id']:
                out.append(diagnostic('NODE_ID',path));continue
            id_=node['id']
            if id_ in ids:out.append(diagnostic('DUPLICATE_ID',path,detail=id_))
            ids[id_]=(collection,node)
    def check_ref(ref,expected,path):
        if not isinstance(ref,str) or ref not in ids:out.append(diagnostic('UNRESOLVED_REFERENCE',path));return
        if expected and ids[ref][0] not in expected:out.append(diagnostic('WRONG_REFERENCE_KIND',path,detail=ids[ref][0]))
    for i,r in enumerate(contract.get('referents',[])):
        if not isinstance(r,dict):continue
        if r.get('kind')=='port':quantity(r.get('quantity'),f'$.referents[{i}].quantity',out)
    for i,r in enumerate(contract.get('relations',[])):
        if not isinstance(r,dict):continue
        path=f'$.relations[{i}]'
        check_ref(r.get('from'),{'referents'},path+'.from');check_ref(r.get('to'),{'referents'},path+'.to')
        if r.get('kind')=='connected_to' and r.get('from') in ids and r.get('to') in ids:
            a=ids[r['from']][1].get('quantity',{});b=ids[r['to']][1].get('quantity',{})
            if (a.get('carrier'),a.get('kind'))!=(b.get('carrier'),b.get('kind')):
                out.append(diagnostic('PORT_CARRIER_MISMATCH',path))
    for i,a in enumerate(contract.get('assertions',[])):
        if not isinstance(a,dict):continue
        path=f'$.assertions[{i}]'
        if a.get('modality') not in MODALITIES:out.append(diagnostic('MODALITY',path+'.modality'))
        if a.get('decision') not in DECISIONS:out.append(diagnostic('DECISION',path+'.decision'))
        elif a['decision'] in ('OWNER_TBD','UNKNOWN'):
            out.append(diagnostic('OWNER_UNRESOLVED',path+'.decision','BLOCKED'))
        if a.get('semantic_role') not in {'SAFETY_GUARANTEE','SERVICE_GUARANTEE','CAPABILITY_GUARANTEE','DATA_ASSUMPTION','ENVIRONMENT_ASSUMPTION','TECHNICAL_ASSUMPTION'}:
            out.append(diagnostic('SEMANTIC_ROLE',path+'.semantic_role'))
        check_ref(a.get('predicate_ref'),{'predicates'},path+'.predicate_ref')
        if 'guard' not in a:out.append(diagnostic('GUARD_REQUIRED',path+'.guard'))
        else:guard(a['guard'],path+'.guard',out)
        if not a.get('scope'):out.append(diagnostic('SCOPE_REQUIRED',path+'.scope'))
        sources=a.get('authority_refs')
        if not isinstance(sources,list) or not sources:out.append(diagnostic('SOURCE_REQUIRED',path+'.authority_refs'))
        else:
            if len(sources)!=len(set(sources)):out.append(diagnostic('DUPLICATE_SOURCE',path+'.authority_refs'))
            for j,s in enumerate(sources):check_ref(s,{'authorities'},path+f'.authority_refs[{j}]')
        if a.get('internal_variable_required') and not a.get('internal_restriction_authority'):
            out.append(diagnostic('UNJUSTIFIED_INTERNAL_RESTRICTION',path))
    for i,e in enumerate(contract.get('evidences',[])):
        if not isinstance(e,dict):continue
        path=f'$.evidences[{i}]'
        if e.get('status') not in EVIDENCE_STATUS:out.append(diagnostic('EVIDENCE_STATUS',path+'.status'))
        if e.get('role') not in ('REQUEST','RESULT'):out.append(diagnostic('EVIDENCE_ROLE',path+'.role'))
        check_ref(e.get('subject_ref'),{'assertions','observables'},path+'.subject_ref')
        if e.get('status')=='PASS' and (e.get('role')!='RESULT' or not e.get('run_id')):
            out.append(diagnostic('UNSUPPORTED_PASS',path))
    for i,a in enumerate(contract.get('authorities',[])):
        if not isinstance(a,dict):continue
        path=f'$.authorities[{i}]'
        if a.get('decision') not in DECISIONS:out.append(diagnostic('OWNER_STATE',path+'.decision'))
        if not a.get('immutable_ref'):out.append(diagnostic('SOURCE_IMMUTABLE_REF',path))
    for i,o in enumerate(contract.get('observables',[])):
        if not isinstance(o,dict):continue
        path=f'$.observables[{i}]'
        if 'quantity' in o:quantity(o['quantity'],path+'.quantity',out)
        if o.get('aggregation')=='energy_integration':
            duration=(frame or {}).get('time',{}).get('duration')
            if duration is None:out.append(diagnostic('TIME_INTEGRATION_DURATION_MISSING',path))
    scen=(frame or {}).get('scenario',{})
    if isinstance(scen,dict):
        for j,d in enumerate(scen.get('stage1_decisions',[])):
            if not isinstance(d,dict):continue
            if d.get('before_revelation') and len(set(str(x) for x in d.get('values_by_scenario',{}).values()))>1:
                out.append(diagnostic('INFORMATION_LEAKAGE',f'$.frame.scenario.stage1_decisions[{j}]'))
    return out

def canonical_guard(g):
    if isinstance(g,dict) and g.get('op') in ('AND','OR'):
        op=g['op'];items=[]
        for child in g['args']:
            c=canonical_guard(child)
            if isinstance(c,dict) and c.get('op')==op:items.extend(c['args'])
            else:items.append(c)
        return {'op':op,'args':sorted(items,key=encode)}
    if isinstance(g,dict) and g.get('op')=='NOT':return {'op':'NOT','args':[canonical_guard(g['args'][0])]}
    return copy.deepcopy(g)

def encode(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def normalize(contract):
    issues=validate(contract)
    errors=[x for x in issues if x['severity']=='ERROR']
    if errors:raise CSNFError(errors)
    c=copy.deepcopy(contract);tr=[]
    for name in COLLECTIONS:
        c[name].sort(key=lambda x:x['id'])
    tr.append('R02:unordered_roles')
    for a in c['assertions']:
        a['guard']=canonical_guard(a['guard'])
        a['authority_refs'].sort()
    tr.extend(['R03:boolean_commutativity','R04:boolean_flattening','R05:negation_structure','R09:authority_preservation'])
    for node in c['referents']+c['observables']:
        if 'quantity' not in node:continue
        q=node['quantity'];key=(q['carrier'],q['kind'])
        q['value']=normalized_number(Decimal(str(q.get('value',0)))*UNITS[key][q['unit']])
        q['unit']=CANON_UNIT[key]
    tr.extend(['R06:explicit_exact_units','R12:typed_observables'])
    t=c['frame'].get('time')
    if isinstance(t,dict) and t.get('duration') is not None:
        d=Decimal(str(t['duration']))
        if t['duration_unit']=='min':d=d/Decimal(60)
        t['duration']=normalized_number(d);t['duration_unit']='h'
        tr.append('R07:duration_converted')
    tr.extend(['R01:strict_qualified_ids','R08:port_compatibility_check_only','R10:no_implicit_imports','R11:no_implicit_defaults','R13:evidence_status_preserved'])
    return c,{'rules':tr,'diagnostics':issues,'phase':'P0_P6_PARTIAL'}

def semantic_projection(normalized):
    c=copy.deepcopy(normalized)
    authorities={a['id']:a['decision'] for a in c['authorities']}
    for a in c['assertions']:
        a['authority_states']=sorted({authorities[id_] for id_ in a['authority_refs']})
        del a['authority_refs']
    del c['authorities']
    return c

def digest(obj):return hashlib.sha256(encode(obj).encode('utf8')).hexdigest()

def compare_e1(a,b):
    na,_=normalize(a);nb,_=normalize(b)
    same=(digest(semantic_projection(na))==digest(semantic_projection(nb)))
    return {'e1':'E1_EQUAL' if same else 'E1_DIFFERENT','audit_equal':digest(na)==digest(nb),
            'e2':'NOT_PROVED','e3':'NOT_EXECUTED','e4':'NOT_PROVED','e5':'NOT_ASSESSED'}
