"""R1 finite typed research interface; original N1 and C21 are immutable dependencies."""
import copy, hashlib, json, re, sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0, str(Path(__file__).parent/'pinned'))
import chain as old
import csnf_validator as c21
from chain import need, fields, ident, num
VERSION = ('C20-research-r1','CSNF-R0','energy-r1')
PIN = {'chain.py':'86737b73d6d8add9f46726704aaa1e716cec5829466b2cc89a8bc7235b5f1de0','csnf_validator.py':'b59c7f1c4570df2ac3141fb75a1c0d3432d8259ffa3ebee142a2470988f4adc1','profile_engine.py':'3e1842f817830a7fd15db0f3ead72339f51a5f5fed28389fae836ba5c9416959'}
def sha(b): return hashlib.sha256(b).hexdigest()
def file_sha(p): return sha(Path(p).read_bytes())
def digest(x): return c21.digest(x)
def pins():
    p=Path(__file__).parent/'pinned'; got={k:file_sha(p/k) for k in PIN}; need(got==PIN,'PIN_MISMATCH'); return got

def ast_call(x):
    # R1 adds one structured AST encoding in the existing declaration syntax.
    if type(x) is tuple and x[1]=='ast':
        need(len(x[2])==1 and type(x[2][0]) is dict,'AST_VALUE'); return x[2][0]
    return old.call(x)

class Parser(old.Parser):
    """Reuse N1 lexer/Value grammar; R1 predicates may contain a structured AST."""
    def parse(self):
        self.pop('contract');cid=self.string();self.pop('schema');s=self.string();self.pop('rules');r=self.string();self.pop('registry');g=self.string();self.pop('{')
        out={k:[] for k in old.ROLES};f=None
        while self.peek()!='}':
            tag=self.word();i=self.string();n={'id':i};k=None
            if tag=='frame':
                need(f is None and i==cid,'FRAME_ID');f=self.block();need(not set(f)&{'id','schema','ruleset','registry'},'FRAME_OVERRIDE');f.update(id=i,schema=s,ruleset=r,registry=g);continue
            if tag=='referent':self.pop(':');n['kind']=self.word();k='referents'
            elif tag=='relation':
                self.pop(':');n['kind']=self.word();v=self.many('(',')',self.string);need(len(v)==2,'RELATION_ARITY');n.update({'from':v[0],'to':v[1]});k='relations'
            elif tag=='predicate':self.pop('=');n['expr']=ast_call(self.expr());self.pop(';');out['predicates'].append(n);continue
            elif tag=='assert':
                n.update(modality=self.word(),semantic_role=self.word());self.pop('predicate');n['predicate_ref']=self.string();self.pop('scope');n['scope']=self.string();self.pop('guard');n['guard']=old.guard_call(self.expr());self.pop('authority');n['authority_refs']=self.many('[',']',self.string);self.pop('decision');n['decision_state']=self.word();self.pop(';');out['assertions'].append(n);continue
            elif tag=='observe':self.pop('from');n['subject']=self.string();k='observables'
            elif tag=='variation':self.pop('on');n['subject']=self.string();k='variations'
            elif tag=='evidence':self.pop(':');n['role']=self.word();self.pop('for');n['subject_ref']=self.string();k='evidences'
            elif tag=='authority':self.pop(':');n['role']=self.word();k='authorities'
            else:raise old.Reject('UNKNOWN_DECLARATION:'+tag)
            v=self.block();need(not set(v)&set(n),'DECLARATION_OVERRIDE');n.update(v);out[k].append(n)
        self.pop('}');need(self.peek() is None and f is not None,'END_OR_FRAME');out['frame']=f;return out

def decode(source,syntax):
    need(syntax in ('A','B'),'SYNTAX');return Parser(source).parse() if syntax=='A' else old.decode_b(source)
def emit_a(d):
    # Use original renderer for every non-predicate declaration; no global monkey patch.
    base=copy.deepcopy(d); pp=base['predicates'];base['predicates']=[]
    text=old.emit_a(base);return text[:-2]+''.join('predicate '+old.val(p['id'])+' = ast('+old.val(p['expr'])+');\n' for p in pp)+'}\n'
def unique(xs): need(type(xs) is list and all(type(i) is str for i in xs) and len(xs)==len(set(xs)),'SET_TYPE');return xs
def table(rows):
    need(type(rows) is list,'TABLE');out={}
    for r in rows:
        need(type(r) is dict and 'id' in r,'ROW_ID');i=ident(r['id']);need(i not in out,'DUPLICATE_ID');out[i]=r
    return out

def quantity(q):
    fields(q,('carrier','kind','unit','value','sign'),('basis',));num(q['value']);need(not old.c21_errors_quantity(q),'QUANTITY');return (q['carrier'],q['kind'],q['sign'],q.get('basis'))
def normalize_q(q):
    # Check original C21 conversion against exact rational arithmetic; fail closed on precision loss.
    k=(q['carrier'],q['kind']);target=c21.CANON_UNIT[k];v=F(str(q['value']))*F(c21.UNITS[k][q['unit']]);z=c21.normalized_number(num(q['value'])*c21.UNITS[k][q['unit']]);need(F(z)==v,'INEXACT_DECIMAL_NORMALIZATION');q.update(unit=target,value=z)

def typed(d):
    fields(d,('frame',*old.ROLES));f=d['frame'];fields(f,('id','schema','ruleset','registry','question','time','domains','scopes','guards','information_sets','data_inputs','method_slots'))
    need(tuple(f[k] for k in ('schema','ruleset','registry'))==VERSION,'R1_VERSION');ident(f['id']);need(type(f['question']) is str,'QUESTION')
    t=f['time'];fields(t,('id','duration','duration_unit'));ident(t['id']);need(num(t['duration'])>0 and t['duration_unit'] in ('h','min'),'TIME');need(F(str(t['duration']))/(60 if t['duration_unit']=='min' else 1)==F(c21.normalized_number(num(t['duration'])/(60 if t['duration_unit']=='min' else 1))),'INEXACT_TIME')
    dom=table(f['domains']);scopes=table(f['scopes']);guards=table(f['guards']);infos=table(f['information_sets']);slots=table(f['method_slots']);data_inputs=table(f['data_inputs']);ix={};blocked=[]
    allids=[f['id'],t['id'],*dom,*scopes,*guards,*infos,*slots,*data_inputs];need(len(allids)==len(set(allids)),'DUPLICATE_ID')
    for k in old.ROLES:
        for i,n in table(d[k]).items():need(i not in ix and i not in allids,'DUPLICATE_ID');ix[i]=(k,n)
    def ref(i,k):need(type(i) is str and i in ix and ix[i][0]==k,'REFERENCE_KIND');return ix[i][1]
    for a in dom.values():fields(a,('id','kind','members'));need(a['kind'] in ('time','scenario','trace','request','response','component','port') and bool(unique(a['members'])),'DOMAIN')
    for a in scopes.values():fields(a,('id','domains'));need(all(i in dom for i in unique(a['domains'])),'SCOPE_DOMAIN')
    for a in infos.values():
        fields(a,('id','time_domain','stage','scenario_domain','partition'));td=dom[a['time_domain']];sd=dom[a['scenario_domain']];need(td['kind']=='time' and sd['kind']=='scenario' and a['stage'] in td['members'],'INFORMATION_DOMAIN');need(type(a['partition']) is list and all(bool(unique(group)) for group in a['partition']),'INFORMATION_PARTITION');flat=[v for group in a['partition'] for v in group];need(len(flat)==len(set(flat)) and set(flat)==set(sd['members']),'INFORMATION_PARTITION')
    for a in infos.values():
        for b in infos.values():
            if a['time_domain']==b['time_domain'] and a['scenario_domain']==b['scenario_domain']:
                order=dom[a['time_domain']]['members'];ia,ib=order.index(a['stage']),order.index(b['stage'])
                if ia<=ib:need(all(any(set(g)<=set(h) for h in a['partition']) for g in b['partition']),'INFORMATION_REFINEMENT')
    for a in d['referents']:
        fields(a,('id','kind','type','quantity','axes'),('direction','component_ref'));q=quantity(a['quantity']);need(a['kind'] in ('entity','external_port') and a['type']=='.'.join(q[:2]),'REFERENT_TYPE');need(all(i in dom for i in unique(a['axes'])),'AXIS');need((a['kind']=='external_port' and a.get('direction') in ('IN','OUT','BIDIRECTIONAL')) or (a['kind']=='entity' and 'direction' not in a),'PORT_DIRECTION')
        if 'component_ref' in a:need(a['kind']=='external_port' and ref(a['component_ref'],'referents')['kind']=='entity','COMPONENT_REF')
    for a in dom.values():
        if a['kind'] in ('component','port'):need(all(ref(i,'referents')['kind']==('entity' if a['kind']=='component' else 'external_port') for i in a['members']),'DOMAIN_MEMBER_KIND')
    def expr(e,env,used):
        need(type(e) is dict and type(e.get('op')) is str,'EXPR');op=e['op']
        if op=='bool3':fields(e,('op','value'));need(e['value'] in ('TRUE','FALSE','UNKNOWN'),'BOOL3');return 'Bool3'
        if op=='var':fields(e,('op','name'));need(e['name'] in env,'UNBOUND_VARIABLE');return ('Index',env[e['name']])
        if op in ('forall','exists'):
            fields(e,('op','var','domain','body'));fields(e['domain'],('kind','ref'));v=e['var'];i=e['domain']['ref'];need(type(v) is str and re.fullmatch(r'[A-Za-z_]\w*',v) and v not in env and i in dom and dom[i]['kind']==e['domain']['kind'],'BINDER');used.add(i);need(expr(e['body'],env|{v:i},used)=='Bool3','QUANTIFIER_BODY');return 'Bool3'
        if op in ('and','or','not'):
            fields(e,('op','args'));a=e['args'];need(type(a) is list and (len(a)==1 if op=='not' else len(a)>=2),'BOOL_ARITY');need(all(expr(v,env,used)=='Bool3' for v in a),'BOOL_TYPE');return 'Bool3'
        if op=='measure':
            fields(e,('op','ref','indices'));a=ref(e['ref'],'referents');need(type(e['indices']) is list and [expr(i,env,used) for i in e['indices']]==[('Index',i) for i in a['axes']],'INDEX_TYPE');used.update(a['axes']);return quantity(a['quantity'])
        if op=='literal':fields(e,('op','quantity'));return quantity(e['quantity'])
        if op=='integrate':
            fields(e,('op','expr','duration_ref'));q=expr(e['expr'],env,used);need(e['duration_ref']==t['id'] and type(q) is tuple and q[:2]==('electricity','active_power'),'INTEGRATION_TYPE');return ('electricity','energy',q[2],q[3])
        if op=='compare':
            fields(e,('op','cmp','lhs','rhs'));a=expr(e['lhs'],env,used);b=expr(e['rhs'],env,used);need(e['cmp'] in ('eq','le','ge','lt','gt') and type(a) is tuple and a==b and (a[0]!='Index' or e['cmp']=='eq'),'COMPARISON_TYPE');return 'Bool3'
        if op=='in_information':
            fields(e,('op','info','scenario','time'));a=infos[e['info']];need(expr(e['scenario'],env,used)==('Index',a['scenario_domain']) and expr(e['time'],env,used)==('Index',a['time_domain']),'INFO_TYPE');return 'Bool3'
        raise old.Reject('UNKNOWN_OPERATOR:'+op)
    for a in guards.values():fields(a,('id','expr'));need(expr(a['expr'],{},set())=='Bool3','GUARD_TYPE')
    def guard(g,used):
        if type(g) is bool:return
        if g=='UNKNOWN':blocked.append('UNKNOWN_GUARD');return
        need(type(g) is dict,'GUARD_TYPE')
        if set(g)=={'atom'}:
            need(g['atom'] in guards,'GUARD_REF');expr(guards[g['atom']]['expr'],{},used);blocked.append('GUARD_APPLICABILITY_NOT_EVALUATED');return
        fields(g,('op','args'));need(type(g['args']) is list and (len(g['args'])==1 if g['op']=='NOT' else g['op'] in ('AND','OR') and len(g['args'])>=2),'GUARD_ARITY');[guard(a,used) for a in g['args']]
    puses={}
    for a in d['predicates']:fields(a,('id','expr'));used=set();need(expr(a['expr'],{},used)=='Bool3','PREDICATE');puses[a['id']]=used
    def authorities(ids,state=None):
        need(bool(unique(ids)),'AUTHORITY_REQUIRED')
        for i in ids:
            a=ref(i,'authorities');need(state is None or a['decision_state']==state,'AUTHORITY_CONFLICT')
    for a in d['authorities']:
        fields(a,('id','role','immutable_ref','revision','decision_state'));need(a['role'] in ('SOURCE','OWNER','DECISION','PROVENANCE') and a['decision_state'] in ('OWNER_TBD','PROPOSED','UNKNOWN') and all(type(a[k]) is str and a[k] for k in ('immutable_ref','revision')),'AUTHORITY')
    for a in d['relations']:
        fields(a,('id','kind','from','to','authority_refs'));x=ref(a['from'],'referents');y=ref(a['to'],'referents');authorities(a['authority_refs']);need(x['id']!=y['id'] and quantity(x['quantity'])==quantity(y['quantity']) and x['axes']==y['axes'],'RELATION_TYPE');need(a['kind'] in ('connected_to','counterfactual_of'),'RELATION_KIND')
        if a['kind']=='connected_to':need(x['kind']==y['kind']=='external_port' and (x['direction']=='BIDIRECTIONAL' or y['direction']=='BIDIRECTIONAL' or (x['direction'],y['direction']) in (('IN','OUT'),('OUT','IN'))),'PORT_COMPATIBILITY')
        else:blocked.append('COUNTERFACTUAL_CONTEXT_REQUIRES_PROFILE')
    for a in d['assertions']:
        fields(a,('id','modality','semantic_role','predicate_ref','scope','guard','authority_refs','decision_state'));p=ref(a['predicate_ref'],'predicates')['expr'];authorities(a['authority_refs'],a['decision_state']);need(a['modality'] in c21.MODALITIES and a['scope'] in scopes,'ASSERTION_SCOPE');used=set(puses[a['predicate_ref']]);guard(a['guard'],used);need(used<=set(scopes[a['scope']]['domains']),'SCOPE_ESCAPE')
        role=a['semantic_role'];need(role in ('SAFETY_GUARANTEE','SERVICE_GUARANTEE','CAPABILITY_GUARANTEE','DATA_ASSUMPTION','ENVIRONMENT_ASSUMPTION','TECHNICAL_ASSUMPTION'),'SEMANTIC_ROLE')
        if role in ('CAPABILITY_GUARANTEE','SERVICE_GUARANTEE'):need(p['op']=='forall' and p['domain']['kind']=='request' and p['body']['op']=='exists' and p['body']['domain']['kind']=='response','REQUEST_RESPONSE_ORDER')
        if role=='SERVICE_GUARANTEE':blocked.append('SERVICE_BEHAVIOURAL_EVIDENCE_REQUIRED')
        if a['decision_state'] in ('OWNER_TBD','UNKNOWN','PROPOSED'):blocked.append('OWNER_UNRESOLVED')
    for a in d['observables']:
        fields(a,('id','subject','projection','quantity','aggregation','bindings'));r=ref(a['subject'],'referents');env={}
        for b in a['bindings']:fields(b,('var','domain'));need(type(b['var']) is str and re.fullmatch(r'[A-Za-z_]\w*',b['var']) and b['var'] not in env and b['domain'] in dom,'OBS_BINDER');env[b['var']]=b['domain']
        need(list(env.values())==r['axes'] and expr(a['projection'],env,set())==quantity(a['quantity']),'OBSERVABLE_TYPE');need(a['aggregation'] in ('identity','energy_integration') and (a['projection']['op']=='integrate')==(a['aggregation']=='energy_integration'),'OBS_AGGREGATION')
        proj=a['projection'] if a['aggregation']=='identity' else a['projection']['expr'];need(proj['op']=='measure' and proj['ref']==a['subject'],'OBSERVABLE_SUBJECT_PROJECTION')
    for a in data_inputs.values():
        fields(a,('id','role','axes','unit','basis'));need(a['role'] in ('probability','time_weight','period_count') and a['unit']=='1' and a['basis']=='' and len(unique(a['axes']))==1,'DATA_INPUT_TYPE');need(dom[a['axes'][0]]['kind']==('scenario' if a['role']=='probability' else 'time'),'DATA_INPUT_AXIS')
    for a in slots.values():fields(a,('id','observables','data_inputs'));need(bool(unique(a['observables'])),'SLOT');[ref(i,'observables') for i in a['observables']];need(all(i in data_inputs for i in unique(a['data_inputs'])),'SLOT_DATA_INPUT')
    for a in d['variations']:fields(a,('id','subject','alternatives','disclosure','source_refs'));ref(a['subject'],'referents');authorities(a['source_refs']);need(len(unique(a['alternatives']))>=2 and a['disclosure'] is True,'VARIATION')
    for a in d['evidences']:fields(a,('id','role','subject_ref','status','oracle'));need(a['subject_ref'] in ix and ix[a['subject_ref']][0] in ('assertions','observables') and a['role']=='REQUEST' and a['status']=='NOT_EXECUTED' and type(a['oracle']) is str and a['oracle'],'EVIDENCE_PROMOTION')
    return copy.deepcopy(d),sorted(set(blocked))

def lower(d):
    n=old.lower(old.TypedAST(d,()))
    # Preserve R1 typed declarations and canonicalize nested physical quantities.
    def visit(x):
        if type(x) is dict:
            if 'quantity' in x: normalize_q(x['quantity'])
            for v in x.values():visit(v)
        elif type(x) is list:
            for v in x:visit(v)
    visit(n)
    for k in ('domains','scopes','guards','information_sets','data_inputs','method_slots'):n['frame'][k].sort(key=lambda a:a['id'])
    for a in n['frame']['scopes']:a['domains']=sorted(a['domains'])
    for a in n['frame']['method_slots']:a['observables']=sorted(a['observables']);a['data_inputs']=sorted(a['data_inputs'])
    for a in n['frame']['information_sets']:a['partition']=sorted(sorted(g) for g in a['partition'])
    return n

def run(source,syntax,extension=None):
    pins();d=decode(source,syntax)
    if tuple(d['frame'][k] for k in ('schema','ruleset','registry'))==old.SOURCE:
        need(extension is None,'LEGACY_EXTENSION_UNSUPPORTED');return old.run(source,syntax)
    d,blocked=typed(d);n=lower(d)
    if extension is not None:
        # Only trusted caller N2R passes its validated extension; direct untrusted input cannot add it.
        n['frame']['resolved_profile']=copy.deepcopy(extension)
    norm,report=c21.normalize(n);need(c21.normalize(norm)[0]==norm,'NON_IDEMPOTENT')
    need(norm['frame'].get('resolved_profile')==extension,'PROFILE_LOSS')
    semantic=c21.semantic_projection(norm);audit={'normalized':norm,'source_ast':d,'source_versions':VERSION,'pins':PIN,'blocked':blocked}
    return {'status':'BLOCKED' if blocked or any(x['severity']=='BLOCKED' for x in report['diagnostics']) else 'STATIC_VALID_ONLY','blocked':blocked,'normalized':norm,'report':report,'semantic_digest':digest(semantic),'audit_digest':digest(audit),'source_digest':sha(source.encode()),'syntax':syntax}
