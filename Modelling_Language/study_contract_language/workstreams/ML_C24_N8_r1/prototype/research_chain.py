"""R1 research slice; not a replacement for C20/C21, not normative."""
import copy, hashlib, itertools, json, re
from fractions import Fraction as F
from pathlib import Path
import csnf_validator as c21
VERSION='R1-research-0.1'
ROLES=c21.COLLECTIONS
class Reject(ValueError): pass
def need(p,msg):
    if not p: raise Reject(msg)
def shape(d,*keys): need(type(d) is dict and set(d)==set(keys),'FIELDS')
def enc(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)
def digest(x): return hashlib.sha256(enc(x).encode()).hexdigest()
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'DUPLICATE_KEY');d[k]=v
    return d
def read(s): return json.loads(s,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'NONFINITE'),parse_float=lambda _:need(False,'EXACT_NUMBER_REQUIRED'))
def number(x):
    need(type(x) in (str,int) and x!='UNKNOWN','NUMERIC_UNKNOWN')
    try: return F(x)
    except (ValueError,ZeroDivisionError): raise Reject('NUMBER')
def qid(x): need(type(x) is str and re.fullmatch(r'[A-Za-z][\w.-]*:[\w.:-]+',x),'QID');return x
# C20-A declaration/block subset, with explicit versioned extension fields in Frame.
TOK=re.compile(r'\s+|"(?:[^"\\\x00-\x1f]|\\.)*"|[A-Za-z_][A-Za-z0-9_./-]*|[{}\[\]():;,=]')
class Parser:
    def __init__(self,s):
        self.ts=[];i=0
        while i<len(s):
            m=TOK.match(s,i);need(m is not None,'LEXICAL');i=m.end()
            if not m.group().isspace():self.ts.append(m.group())
        self.i=0
    def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
    def pop(self,w=None):
        t=self.peek();need(t is not None and (w is None or t==w),'SYNTAX');self.i+=1;return t
    def string(self):
        t=self.pop();need(t.startswith('"'),'STRING');return read(t)
    def word(self):
        t=self.pop();need(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_./-]*',t),'WORD');return t
    def seq(self,a,b,fn):
        self.pop(a);v=[]
        if self.peek()!=b:
            v.append(fn())
            while self.peek()==',':self.pop();v.append(fn())
        self.pop(b);return v
    def block(self):
        self.pop('{');v=[]
        while self.peek()!='}':
            k=self.word();self.pop(':');v.append((k,self.value()));self.pop(';')
        self.pop('}');return pairs(v)
    def value(self):
        t=self.peek()
        if t=='{':return self.block()
        if t=='[':return self.seq('[',']',self.value)
        if t and t.startswith('"'):return self.string()
        t=self.word();return {'true':True,'false':False}.get(t,t)
    def expr(self):
        t=self.value()
        if self.peek()=='(':return {'op':t,'args':self.seq('(',')',self.expr)}
        return t
    def parse(self):
        self.pop('contract');cid=self.string();self.pop('schema');s=self.string();self.pop('rules');r=self.string();self.pop('registry');g=self.string();self.pop('{');d={k:[] for k in ROLES};frame=None
        while self.peek()!='}':
            tag=self.word();i=self.string();n={'id':i}
            if tag=='frame':
                need(frame is None and cid==i,'FRAME');frame=self.block();need(not set(frame)&{'id','schema','ruleset','registry'},'OVERRIDE');frame.update(id=i,schema=s,ruleset=r,registry=g);continue
            if tag=='referent':self.pop(':');n['kind']=self.word();k='referents'
            elif tag=='relation':
                self.pop(':');n['kind']=self.word();a=self.seq('(',')',self.string);need(len(a)==2,'ARITY');n.update({'from':a[0],'to':a[1]});k='relations'
            elif tag=='predicate':self.pop('=');n['expr']=self.expr();self.pop(';');d['predicates'].append(n);continue
            elif tag=='assert':
                n.update(modality=self.word(),semantic_role=self.word());self.pop('predicate');n['predicate_ref']=self.string();self.pop('scope');n['scope']=self.string();self.pop('guard');n['guard']=self.expr();self.pop('authority');n['authority_refs']=self.seq('[',']',self.string);self.pop('decision');n['decision_state']=self.word();self.pop(';');d['assertions'].append(n);continue
            elif tag=='observe':self.pop('from');n['subject']=self.string();k='observables'
            elif tag=='variation':self.pop('on');n['subject']=self.string();k='variations'
            elif tag=='evidence':self.pop(':');n['role']=self.word();self.pop('for');n['subject_ref']=self.string();k='evidences'
            elif tag=='authority':self.pop(':');n['role']=self.word();k='authorities'
            else:raise Reject('DECLARATION')
            b=self.block();need(not set(b)&set(n),'OVERRIDE');n.update(b);d[k].append(n)
        self.pop('}');need(self.peek() is None and frame is not None,'EOF');d['frame']=frame;return d

def call(op,*a):return {'op':op,'args':list(a)}
# Semantic types: Bool3, index(domain ID), or quantity(carrier, kind, basis, sign).
BOOL=('Bool3',); ONE=('scalar','dimensionless','','NONE')
def quantity(q):
    shape(q,'carrier','kind','unit','value','sign','basis');number(q['value']);need((q['carrier'],q['kind']) in c21.UNITS,'DIMENSION');need(q['unit']==c21.CANON_UNIT[(q['carrier'],q['kind'])],'CANONICAL_UNIT_REQUIRED');need(q['sign'] in ('NONE','INJECTION','CONSUMPTION','BIDIRECTIONAL'),'SIGN');need((q['carrier']=='currency' and re.fullmatch(r'EUR:(real|nominal):[0-9]{4}',q['basis'])) or (q['carrier']!='currency' and q['basis']==''),'BASIS');return (q['carrier'],q['kind'],q['basis'],q['sign'])
def indexed(items):
    d={}
    for n in items:
        i=qid(n['id']);need(i not in d,'DUPLICATE_ID');d[i]=n
    return d

def infer(e,ctx,env,ruletypes=None,params=None):
    if type(e) is bool or e=='unknown':return BOOL
    shape(e,'op','args');op=e['op'];a=e['args'];need(type(a) is list,'ARITY')
    def sub(x):return infer(x,ctx,env,ruletypes,params)
    if op=='var':need(len(a)==1 and a[0] in env,'UNBOUND_VARIABLE');return ('index',env[a[0]])
    if op in ('forall','exists','sum'):
        need(len(a)==3 and type(a[0]) is str and re.fullmatch(r'[A-Za-z_]\w*',a[0]) and a[0] not in env and a[1] in ctx['domains'],'BINDER');t=infer(a[2],ctx,{**env,a[0]:a[1]},ruletypes,params);need((op=='sum' and t!=BOOL and t[0]!='index') or (op!='sum' and t==BOOL),'QUANTIFIER_BODY');return t
    if op=='at':
        need(len(a)>0 and a[0] in ctx['observables'],'OBSERVABLE_REF');o=ctx['observables'][a[0]];need([sub(i) for i in a[1:]]==[('index',d) for d in o['axes']],'INDEX_TYPE');return quantity(o['quantity'])
    if op=='flag':need(len(a)==1 and a[0] in ctx['flags'],'GUARD_REF');return BOOL
    if op=='scalar':need(len(a)==1,'ARITY');number(a[0]);return ONE
    if op=='rule':need(len(a)==1 and ruletypes is not None and a[0] in ruletypes,'RULE_REF');return ruletypes[a[0]]
    if op=='param':need(len(a)==1 and params is not None and a[0] in params,'PARAM_REF');return ONE
    if op=='weight':
        need(len(a)==2 and a[0] in ctx['weights'],'WEIGHT_REF');need(sub(a[1])==('index',ctx['weights'][a[0]]['axis']),'WEIGHT_AXIS');return ONE
    if op in ('and','or','not','implies'):
        need((len(a)==1 if op=='not' else len(a)==2 if op=='implies' else len(a)>=2) and all(sub(x)==BOOL for x in a),'BOOL_TYPE');return BOOL
    need(op in ('eq','le','ge','add','sub','mul','div','pow'),'UNKNOWN_OPERATOR');need(len(a)==2,'ARITY');x,y=map(sub,a)
    if op=='eq':need(x==y,'DIMENSION_BASIS');return BOOL
    need(x!=BOOL and y!=BOOL and x[0]!='index' and y[0]!='index','QUANTITY_TYPE')
    if op in ('le','ge','add','sub'):need(x==y,'DIMENSION_BASIS');return BOOL if op in ('le','ge') else x
    if op=='mul':need(ONE in (x,y),'DIMENSION_PRODUCT');return y if x==ONE else x
    if op=='pow':need(x==y==ONE,'POWER_TYPE');return ONE
    need(y==ONE,'DIMENSION_DIVISION');return x

def bind(d):
    shape(d,'frame',*ROLES);f=d['frame'];shape(f,'id','schema','ruleset','registry','question','time','domains','flags','weights');qid(f['id']);need((f['schema'],f['ruleset'],f['registry'])==('C20-research-0.1','CSNF-R0',VERSION),'VERSION');shape(f['time'],'id','duration','duration_unit');need(f['time']['duration_unit']=='h' and number(f['time']['duration'])>0,'TIME')
    domains=indexed(f['domains']);flags=indexed(f['flags']);weights=indexed(f['weights']);allnodes=indexed([n for k in ROLES for n in d[k]]+f['domains']+f['flags']+f['weights']+[{'id':f['id']},{'id':f['time']['id']}]);refs=indexed(d['referents']);obs=indexed(d['observables']);auth=indexed(d['authorities']);pred=indexed(d['predicates']);asserts=indexed(d['assertions']);ctx=dict(domains=domains,flags=flags,weights=weights,observables=obs)
    for x in domains.values():
        shape(x,'id','kind','members');need(x['kind'] in ('time','scenario','information','component','port','request','response') and type(x['members']) is list and x['members'] and all(type(v) is str for v in x['members']) and len(set(x['members']))==len(x['members']),'DOMAIN')
    for x in flags.values():shape(x,'id','type');need(x['type']=='Bool3','FLAG_TYPE')
    for x in weights.values():shape(x,'id','axis','role');need(x['axis'] in domains and (domains[x['axis']]['kind'],x['role']) in (('time','time_weight'),('time','elapsed_years'),('scenario','probability')),'WEIGHT_ROLE')
    for x in refs.values():shape(x,'id','kind','quantity');need(x['kind']=='entity','REFERENT_KIND_UNSUPPORTED');quantity(x['quantity'])
    for x in obs.values():
        shape(x,'id','subject','quantity','axes','aggregation');need(x['subject'] in refs and quantity(x['quantity'])==quantity(refs[x['subject']]['quantity']) and x['aggregation']=='identity','OBSERVABLE_TYPE');need(type(x['axes']) is list and len(set(x['axes']))==len(x['axes']) and all(a in domains for a in x['axes']),'OBSERVABLE_AXES')
    for x in auth.values():shape(x,'id','role','immutable_ref','revision','decision_state');need(x['role']=='SOURCE' and x['decision_state']=='OWNER_TBD' and type(x['immutable_ref']) is str and x['immutable_ref'] and type(x['revision']) is str and x['revision'],'AUTHORITY')
    for x in d['relations']:
        shape(x,'id','kind','from','to','authority_refs');need(x['kind']=='counterfactual_of' and x['from'] in refs and x['to'] in refs and x['from']!=x['to'] and quantity(refs[x['from']]['quantity'])==quantity(refs[x['to']]['quantity']),'RELATION');need(x['authority_refs'] and all(a in auth for a in x['authority_refs']),'AUTHORITY_REF')
    for x in pred.values():shape(x,'id','expr');need(infer(x['expr'],ctx,{})==BOOL,'PREDICATE')
    for x in asserts.values():
        shape(x,'id','modality','semantic_role','predicate_ref','scope','guard','authority_refs','decision_state');need(x['predicate_ref'] in pred and x['scope'] in domains,'SCOPE');need(x['decision_state']=='OWNER_TBD' and type(x['authority_refs']) is list and x['authority_refs'] and len(set(x['authority_refs']))==len(x['authority_refs']) and all(a in auth and auth[a]['decision_state']==x['decision_state'] for a in x['authority_refs']),'AUTHORITY_CONFLICT');need(infer(x['guard'],ctx,{})==BOOL,'GUARD_TYPE');need(x['modality'] in c21.MODALITIES and x['semantic_role'] in ('SAFETY_GUARANTEE','CAPABILITY_GUARANTEE','SERVICE_GUARANTEE'),'ROLE')
        e=pred[x['predicate_ref']]['expr'];need(type(e) is dict and e['op']=='forall' and e['args'][1]==x['scope'],'OUTER_SCOPE')
        if x['semantic_role']=='CAPABILITY_GUARANTEE':
            b=e['args'][2];need(domains[x['scope']]['kind']=='request' and type(b) is dict and b['op']=='exists' and domains[b['args'][1]]['kind']=='response','CAPABILITY_ORDER')
    for x in d['evidences']:shape(x,'id','role','subject_ref','status','oracle');need(x['role']=='REQUEST' and x['status']=='NOT_EXECUTED' and x['subject_ref'] in {*asserts,*obs},'EVIDENCE_PROMOTION')
    for x in d['variations']:shape(x,'id','subject','alternatives','disclosure','source_refs');need(x['subject'] in refs and type(x['alternatives']) is list and len(set(x['alternatives']))>=2 and x['disclosure'] is True and x['source_refs'] and all(a in auth for a in x['source_refs']),'VARIATION')
    return ctx

def chain(source,syntax):
    need(syntax in ('A','B'),'SYNTAX_ID');d=Parser(source).parse() if syntax=='A' else read(source);ctx=bind(d);c=copy.deepcopy(d);c['frame'].update(schema=c21.VERSION,ruleset=c21.RULES,registry=c21.REGISTRY)
    # Legacy C21 projection: retain extension AST and source fields; C21 only checks its legacy fields.
    for k in ('assertions','authorities'):
        for a in c[k]:a['decision']=a.pop('decision_state')
    for a in c['assertions']:a['guard']={'atom':'R1:typed-guard'} if type(a['guard']) is dict else ('UNKNOWN' if a['guard']=='unknown' else a['guard'])
    legacy,diag=c21.normalize(c);need(c21.normalize(legacy)[0]==legacy,'C21_IDEMPOTENCE')
    # Canonical semantic graph is authoritative for extension, not the legacy projection.
    graph=copy.deepcopy(d)
    for k in ROLES:graph[k].sort(key=lambda n:n['id'])
    for a in graph['assertions']:a['authority_refs'].sort()
    sem=copy.deepcopy(graph);sem.pop('authorities')
    return {'graph':graph,'legacy':legacy,'legacy_diagnostics':diag,'semantic_digest':digest(sem),'source_sha256':sha(source.encode()),'audit_digest':digest({'graph':graph,'source_sha256':sha(source.encode()),'legacy':legacy})},ctx

def evaluate(e,ctx,env,values,flags,weights,params,rules):
    if type(e) is bool:return e
    if e=='unknown':return None
    op=e['op'];a=e['args'];ev=lambda x:evaluate(x,ctx,env,values,flags,weights,params,rules)
    if op in ('forall','exists','sum'):
        vs=[evaluate(a[2],ctx,{**env,a[0]:i},values,flags,weights,params,rules) for i in ctx['domains'][a[1]]['members']]
        if op=='sum':need(None not in vs,'UNKNOWN_ARITHMETIC');return sum(vs,F(0))
        return (False if False in vs else None if None in vs else True) if op=='forall' else (True if True in vs else None if None in vs else False)
    if op=='var':return env[a[0]]
    if op=='at':return values[a[0]][tuple(ev(i) for i in a[1:])]
    if op=='flag':return flags[a[0]]
    if op=='weight':return weights[a[0]][ev(a[1])]
    if op=='scalar':return number(a[0])
    if op=='param':return params[a[0]]
    if op=='rule':return rules[a[0]]
    v=[ev(x) for x in a]
    if op=='not':return None if v[0] is None else not v[0]
    if op=='and':return False if False in v else None if None in v else True
    if op=='or':return True if True in v else None if None in v else False
    if op=='implies':return True if v[0] is False or v[1] is True else None if None in v else False
    need(None not in v,'UNKNOWN_ARITHMETIC');x,y=v
    if op=='eq':return x==y
    if op=='le':return x<=y
    if op=='ge':return x>=y
    if op=='add':return x+y
    if op=='sub':return x-y
    if op=='mul':return x*y
    if op=='pow':need(y.denominator==1 and 0<=y<=200,'POWER_DOMAIN');return x**int(y)
    need(op=='div' and y!=0,'DIVISION');return x/y

def ledger(items,expected):
    ids=set();support=set()
    for x in items:
        shape(x,'id','atoms');need(x['id'] not in ids,'DUPLICATE_CONTRIBUTION');ids.add(x['id']);need(type(x['atoms']) is list and x['atoms'] and len(set(x['atoms']))==len(x['atoms']),'ATOMS');a=set(x['atoms']);need(not support&a,'OVERLAP');support|=a
    need(support==set(expected),'INCOMPLETE_LEDGER');return sorted(support)

def run(source,syntax,study,method,data):
    result,ctx=chain(source,syntax);g=result['graph'];shape(study,'id','version','method_hash','data_hash','contract_semantic','parameters','status');shape(method,'id','version','registry','authority','parameters','rules','ledger','expected_atoms');shape(data,'id','context','cases','observations','flags','weights');need(study['status']==method['authority']=='OWNER_TBD','AUTHORITY_PROMOTION');need(method['registry']==VERSION and digest(method)==study['method_hash'] and digest(data)==study['data_hash'] and result['semantic_digest']==study['contract_semantic'],'HASH_OR_VERSION');need(set(study['parameters'])==set(method['parameters']),'PARAMETERS')
    params={}
    for k,p in method['parameters'].items():shape(p,'min','max');v=number(study['parameters'][k]);need(number(p['min'])<=v<=number(p['max']),'PARAM_RANGE');params[k]=v
    values={};need(set(data['observations'])==set(ctx['observables']),'DATA_BINDING');need(set(data['flags'])==set(ctx['flags']) and all(type(v) is bool or v=='UNKNOWN' for v in data['flags'].values()),'FLAG_DATA');need(set(data['weights'])==set(ctx['weights']),'WEIGHT_BINDING')
    for k,o in ctx['observables'].items():
        rows={}
        for row in data['observations'][k]:shape(row,'key','value');key=tuple(row['key']);need(key not in rows,'DUPLICATE_ROW');rows[key]=None if row['value']=='UNKNOWN' else number(row['value'])
        need(set(rows)==set(itertools.product(*(ctx['domains'][a]['members'] for a in o['axes']))),'DATA_COVERAGE');values[k]=rows
    weights={}
    for k,w in ctx['weights'].items():
        v={i:number(x) for i,x in data['weights'][k].items()};need(set(v)==set(ctx['domains'][w['axis']]['members']) and all(x>=0 for x in v.values()) and (sum(v.values())==1 if w['role']=='probability' else all(x.denominator==1 for x in v.values()) if w['role']=='elapsed_years' else all(x>0 for x in v.values())),'WEIGHT_VALUES');weights[k]=v
    for r in g['relations']:
        a,b=r['from'],r['to'];need(a in data['cases'] and b in data['cases'],'PAIR_BINDING');need(data['cases'][a]==data['cases'][b]==digest(data['context']),'EXOGENEITY_HASH')
    flags={k:None if v=='UNKNOWN' else v for k,v in data['flags'].items()}
    ruletypes={};vals={}
    for r in method['rules']:
        shape(r,'id','expr','type');need(r['id'] not in ruletypes,'RULE_DUPLICATE');t=infer(r['expr'],ctx,{},ruletypes,params);need(list(t)==r['type'] and t!=BOOL,'RULE_TYPE_OR_ORDER');ruletypes[r['id']]=t;vals[r['id']]=evaluate(r['expr'],ctx,{},values,flags,weights,params,vals)
    checks={}
    predicates={x['id']:x['expr'] for x in g['predicates']}
    for x in g['assertions']:
        guard=evaluate(x['guard'],ctx,{},values,flags,weights,params,vals)
        if guard is not True: checks[x['id']]='NOT_APPLICABLE' if guard is False else 'BLOCKED_UNKNOWN_GUARD';continue
        v=evaluate(predicates[x['predicate_ref']],ctx,{},values,flags,weights,params,vals)
        checks[x['id']]='FINITE_TRUE' if v is True else 'FINITE_FALSE' if v is False else 'INCONCLUSIVE'
    support=ledger(method['ledger'],method['expected_atoms']);hashes={p:sha((Path(__file__).parent/p).read_bytes()) for p in ('research_chain.py','csnf_validator.py')}
    audit=dict(chain=result['audit_digest'],semantic=result['semantic_digest'],method_id=method['id'],method_hash=digest(method),data_hash=digest(data),study_hash=digest(study),code_hashes=hashes,outputs={k:str(v) for k,v in vals.items()},finite_assertion_checks=checks,contributions=support,status='OWNER_TBD',verification_scope='FINITE_RESEARCH_ONLY')
    return {'audit':audit,'audit_digest':digest(audit),'graph':result['graph'],'legacy':result['legacy'],'diagnostics':result['legacy_diagnostics']}
