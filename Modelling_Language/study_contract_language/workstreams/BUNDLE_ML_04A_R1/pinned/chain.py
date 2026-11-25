"""N1 restricted dual syntax research adapter. No model or predicate execution."""
import copy, hashlib, json, re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import csnf_validator as c21
SOURCE=('C20-research-0.1','CSNF-R0','energy-r0')
TARGET=(c21.VERSION,c21.RULES,c21.REGISTRY)
ROLES=c21.COLLECTIONS
class Reject(ValueError): pass
def need(ok,code):
    if not ok: raise Reject(code)
def strict_pairs(items):
    out={}
    for k,v in items:
        need(k not in out,'DUPLICATE_KEY:'+k);out[k]=v
    return out
def reject_constant(v): raise Reject('NONFINITE_JSON')
def decode_b(text):
    return json.loads(text,object_pairs_hook=strict_pairs,parse_constant=reject_constant,parse_float=str)
def fields(x,required,optional=()):
    need(type(x) is dict,'OBJECT_REQUIRED')
    need(set(required)<=x.keys()<=set(required)|set(optional),'FIELD_SET:'+str(sorted(x)))
def ident(x):
    need(type(x) is str and re.fullmatch(r'[A-Za-z][\w.-]*:[^\s]+',x) is not None,'QUALIFIED_ID');return x
def num(x):
    need(type(x) in (str,int),'DECIMAL_TYPE')
    try: n=Decimal(str(x))
    except InvalidOperation: raise Reject('DECIMAL_TYPE')
    need(n.is_finite(),'DECIMAL_FINITE');return n
# Candidate A implements the C20 declaration/block grammar with explicit P1 operator arities.
TOKEN=re.compile(r'\s+|"(?:[^"\\\x00-\x1f]|\\.)*"|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|[A-Za-z_][A-Za-z0-9_./-]*|[{}\[\]():;,=]')
class Parser:
    def __init__(self,s):
        self.t=[];i=0
        while i<len(s):
            m=TOKEN.match(s,i);need(m is not None,'LEXICAL_ERROR:'+str(i));i=m.end()
            if not m.group().isspace(): self.t.append(m.group())
        self.i=0
    def peek(self): return self.t[self.i] if self.i<len(self.t) else None
    def pop(self,w=None):
        t=self.peek();need(t is not None and (w is None or t==w),'SYNTAX_EXPECTED:'+str(w));self.i+=1;return t
    def string(self):
        t=self.pop();need(t.startswith('"'),'QID_OR_STRING_REQUIRED');return json.loads(t)
    def word(self):
        t=self.pop();need(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_./-]*',t) is not None,'IDENT_REQUIRED');return t
    def many(self,start,end,fn):
        self.pop(start);a=[]
        if self.peek()!=end:
            a.append(fn())
            while self.peek()==',': self.pop();a.append(fn())
        self.pop(end);return a
    def block(self):
        self.pop('{');a=[]
        while self.peek()!='}':
            k=self.word();self.pop(':');a.append((k,self.value()));self.pop(';')
        self.pop('}');return strict_pairs(a)
    def value(self):
        t=self.peek()
        if t=='{': return self.block()
        if t=='[': return self.many('[',']',self.value)
        if t and t.startswith('"'):return self.string()
        t=self.pop()
        if t in ('true','false'):return t=='true'
        need(t not in '{}[]():;,=','VALUE_REQUIRED');return t
    def expr(self):
        t=self.value()
        if self.peek()!='(':return t
        need(type(t) is str,'CALL_NAME')
        a=self.many('(',')',self.expr)
        return ('call',t,a)
    def parse(self):
        self.pop('contract');cid=self.string();self.pop('schema');s=self.string();self.pop('rules');r=self.string();self.pop('registry');g=self.string();self.pop('{')
        out={k:[] for k in ROLES};f=None
        while self.peek()!='}':
            tag=self.word();i=self.string()
            if tag=='frame':
                need(f is None and i==cid,'FRAME_ID');f=self.block();need(not set(f)&{'id','schema','ruleset','registry'},'FRAME_OVERRIDE');f.update(id=i,schema=s,ruleset=r,registry=g);continue
            n={'id':i};k=None
            if tag=='referent':self.pop(':');n['kind']=self.word();k='referents'
            elif tag=='relation':
                self.pop(':');n['kind']=self.word();v=self.many('(',')',self.string);need(len(v)==2,'RELATION_ARITY');n.update({'from':v[0],'to':v[1]});k='relations'
            elif tag=='predicate':
                self.pop('=');n['expr']=call(self.expr());self.pop(';');out['predicates'].append(n);continue
            elif tag=='assert':
                n.update(modality=self.word(),semantic_role=self.word());self.pop('predicate');n['predicate_ref']=self.string();self.pop('scope');n['scope']=self.string();self.pop('guard');n['guard']=guard_call(self.expr());self.pop('authority');n['authority_refs']=self.many('[',']',self.string);self.pop('decision');n['decision_state']=self.word();self.pop(';');out['assertions'].append(n);continue
            elif tag=='observe':self.pop('from');n['subject']=self.string();k='observables'
            elif tag=='variation':self.pop('on');n['subject']=self.string();k='variations'
            elif tag=='evidence':self.pop(':');n['role']=self.word();self.pop('for');n['subject_ref']=self.string();k='evidences'
            elif tag=='authority':self.pop(':');n['role']=self.word();k='authorities'
            else:raise Reject('UNKNOWN_DECLARATION:'+tag)
            v=self.block();need(not set(v)&set(n),'DECLARATION_OVERRIDE');n.update(v);out[k].append(n)
        self.pop('}');need(self.peek() is None and f is not None,'END_OR_FRAME');out['frame']=f;return out
def call(x):
    if type(x) is bool or x=='unknown':return {'op':'bool3','value':'UNKNOWN' if x=='unknown' else str(x).upper()}
    need(type(x) is tuple and len(x)==3,'TYPED_CALL_REQUIRED');_,op,a=x
    if op in ('and','or','not'):return dict(op=op,args=[call(v) for v in a])
    if op in ('forall','exists'):
        need(len(a)==4,'ARITY');return dict(op=op,var=a[0],domain=dict(kind=a[1],ref=a[2]),body=call(a[3]))
    if op=='measure':need(len(a)==1,'ARITY');return dict(op=op,ref=a[0])
    if op=='literal':
        need(len(a) in (5,6),'ARITY');return dict(op=op,quantity=dict(zip(('carrier','kind','unit','value','sign','basis'),a)))
    if op=='integrate':need(len(a)==2,'ARITY');return dict(op=op,expr=call(a[0]),duration_ref=a[1])
    if op in ('eq','le','ge','lt','gt'):need(len(a)==2,'ARITY');return dict(op='compare',cmp=op,lhs=call(a[0]),rhs=call(a[1]))
    raise Reject('UNKNOWN_OPERATOR:'+op)
def guard_call(x):
    if type(x) is bool:return x
    if x=='unknown':return 'UNKNOWN'
    need(type(x) is tuple,'GUARD_TYPE');_,op,a=x
    if op=='atom':need(len(a)==1 and type(a[0]) is str,'GUARD_ATOM');return {'atom':a[0]}
    need(op in ('and','or','not'),'GUARD_OPERATOR');return dict(op=op.upper(),args=[guard_call(v) for v in a])
# Structural encoding only; source text and source locations have their own audit identity.
def val(x):
    if type(x) is dict:return '{ '+' '.join(f'{k}: {val(v)};' for k,v in x.items())+' }'
    if type(x) is list:return '['+', '.join(map(val,x))+']'
    return json.dumps(x,ensure_ascii=False)
def ec(e):
    op=e['op'];a=[]
    if op=='bool3':return e['value'].lower()
    if op in ('and','or','not'):a=[ec(v) for v in e['args']]
    elif op in ('forall','exists'):a=[val(e['var']),val(e['domain']['kind']),val(e['domain']['ref']),ec(e['body'])]
    elif op=='measure':a=[val(e['ref'])]
    elif op=='literal':a=[val(e['quantity'][k]) for k in ('carrier','kind','unit','value','sign','basis') if k in e['quantity']]
    elif op=='integrate':a=[ec(e['expr']),val(e['duration_ref'])]
    elif op=='compare':op=e['cmp'];a=[ec(e['lhs']),ec(e['rhs'])]
    else:raise Reject('UNKNOWN_OPERATOR')
    return op+'('+', '.join(a)+')'
def gc(g):
    if type(g) is bool:return val(g)
    if g=='UNKNOWN':return 'unknown'
    if 'atom' in g:return 'atom('+val(g['atom'])+')'
    return g['op'].lower()+'('+', '.join(map(gc,g['args']))+')'
def emit_a(d):
    f=d['frame'];i=val(f['id']);lines=[f'contract {i} schema {val(f["schema"])} rules {val(f["ruleset"])} registry {val(f["registry"])} {{',f'frame {i} '+val({k:v for k,v in f.items() if k not in ('id','schema','ruleset','registry')})]
    for role in ROLES:
        for raw in d[role]:
            n=copy.deepcopy(raw);i=val(n.pop('id'))
            if role=='referents':prefix=f'referent {i}: '+n.pop('kind')
            elif role=='relations':prefix=f'relation {i}: '+n.pop('kind')+'('+val(n.pop('from'))+', '+val(n.pop('to'))+')'
            elif role=='predicates':lines.append(f'predicate {i} = '+ec(n['expr'])+';');continue
            elif role=='assertions':lines.append(f'assert {i} {n["modality"]} {n["semantic_role"]} predicate {val(n["predicate_ref"])} scope {val(n["scope"])} guard {gc(n["guard"])} authority {val(n["authority_refs"])} decision {n["decision_state"]};');continue
            elif role=='observables':prefix=f'observe {i} from '+val(n.pop('subject'))
            elif role=='variations':prefix=f'variation {i} on '+val(n.pop('subject'))
            elif role=='evidences':prefix=f'evidence {i}: '+n.pop('role')+' for '+val(n.pop('subject_ref'))
            else:prefix=f'authority {i}: '+n.pop('role')
            lines.append(prefix+' '+val(n))
    return '\n'.join(lines+['}'])+'\n'
@dataclass(frozen=True)
class TypedAST:
    document: dict
    unresolved: tuple

def typed(d):
    fields(d,('frame',*ROLES));f=d['frame'];fields(f,('id','schema','ruleset','registry','question','time'))
    ident(f['id']);need(tuple(f[k] for k in ('schema','ruleset','registry'))==SOURCE,'SOURCE_VERSION');need(type(f['question']) is str,'QUESTION')
    t=f['time'];fields(t,('id','duration','duration_unit'));ident(t['id']);need(num(t['duration'])>0 and t['duration_unit'] in ('h','min'),'TIME_TYPE')
    index={};unresolved=[]
    for role in ROLES:
        need(type(d[role]) is list,'COLLECTION_TYPE')
        for n in d[role]:
            need(type(n) is dict and 'id' in n,'NODE_ID');i=ident(n['id']);need(i not in index and i not in (f['id'],t['id']),'DUPLICATE_ID');index[i]=(role,n)
    def ref(i,role):
        need(type(i) is str and i in index and index[i][0]==role,'REFERENCE_KIND:'+str(i));return index[i][1]
    def qtype(q):
        fields(q,('carrier','kind','unit','value','sign'),('basis',));num(q['value']);need(not c21_errors_quantity(q),'QUANTITY_UNIT_SIGN_BASIS');return (q['carrier'],q['kind'],q['sign'],q.get('basis'))
    def refs(a,role):
        need(type(a) is list and len(a)>0 and all(type(i) is str for i in a) and len(set(a))==len(a),'REFERENCE_SET');[ref(i,role) for i in a]
    def expr(e):
        need(type(e) is dict and type(e.get('op')) is str,'EXPR_AST');op=e['op']
        if op=='bool3':fields(e,('op','value'));need(e['value'] in ('TRUE','FALSE','UNKNOWN'),'BOOL3');return 'Bool3'
        if op in ('and','or','not'):
            fields(e,('op','args'));a=e['args'];need(type(a) is list and (len(a)==1 if op=='not' else len(a)>=2),'BOOLEAN_ARITY');need(all(expr(v)=='Bool3' for v in a),'BOOL3_EXPECTED');return 'Bool3'
        if op in ('forall','exists'):
            fields(e,('op','var','domain','body'));fields(e['domain'],('kind','ref'));need(type(e['var']) is str and re.fullmatch(r'[A-Za-z_]\w*',e['var']) and e['domain']==dict(kind='time',ref=t['id']),'DOMAIN_UNSUPPORTED');need(expr(e['body'])=='Bool3','BOOL3_EXPECTED');unresolved.append('P1_IMPLICIT_TIME_BINDING');return 'Bool3'
        if op=='measure':
            fields(e,('op','ref'));r=ref(e['ref'],'referents');need('quantity' in r,'MEASURE_QUANTITY');return qtype(r['quantity'])
        if op=='literal':fields(e,('op','quantity'));return qtype(e['quantity'])
        if op=='integrate':
            fields(e,('op','expr','duration_ref'));q=expr(e['expr']);need(e['duration_ref']==t['id'] and type(q) is tuple and q[:2]==('electricity','active_power'),'INTEGRATION_DIMENSION');return ('electricity','energy',q[2],q[3])
        if op=='compare':
            fields(e,('op','cmp','lhs','rhs'));a=expr(e['lhs']);b=expr(e['rhs']);need(e['cmp'] in ('eq','le','ge','lt','gt') and type(a) is tuple and a==b,'COMPARISON_DIMENSION_BASIS');return 'Bool3'
        raise Reject('UNKNOWN_OPERATOR:'+op)
    def guard(g):
        if type(g) is bool or g=='UNKNOWN':return
        need(type(g) is dict,'GUARD_TYPE')
        if set(g)=={'atom'}:need(type(g['atom']) is str,'GUARD_ATOM');ident(g['atom']);unresolved.append('P1_UNRESOLVED_GUARD_ATOM');return
        fields(g,('op','args'));a=g['args'];need(type(a) is list and (len(a)==1 if g['op']=='NOT' else g['op'] in ('AND','OR') and len(a)>=2),'GUARD_ARITY');[guard(v) for v in a]
    for n in d['referents']:
        fields(n,('id','kind','type','quantity'),('direction',));qtype(n['quantity']);need(n['kind'] in ('external_port','entity'),'REFERENT_KIND');need(n['type']==n['quantity']['carrier']+'.'+n['quantity']['kind'],'REFERENT_TYPE')
        if n['kind']=='external_port':need(n.get('direction') in ('IN','OUT','BIDIRECTIONAL'),'PORT_DIRECTION')
        else:need('direction' not in n,'ENTITY_DIRECTION')
    for n in d['relations']:
        fields(n,('id','kind','from','to','authority_refs'));a=ref(n['from'],'referents');b=ref(n['to'],'referents');refs(n['authority_refs'],'authorities');need(a['id']!=b['id'],'RELATION_SELF');need(n['kind'] in ('connected_to','counterfactual_of'),'RELATION_KIND');need(qtype(a['quantity'])==qtype(b['quantity']),'RELATION_TYPE');need(n['kind']!='connected_to' or a['kind']==b['kind']=='external_port','PORT_RELATION')
        if n['kind']=='counterfactual_of':unresolved.append('COUNTERFACTUAL_CONTEXT_NOT_BOUND')
    for n in d['predicates']:fields(n,('id','expr'));need(expr(n['expr'])=='Bool3','PREDICATE_BOOL3')
    for n in d['authorities']:
        fields(n,('id','role','immutable_ref','revision','decision_state'));need(n['role'] in ('SOURCE','OWNER','DECISION','PROVENANCE') and all(type(n[k]) is str and n[k] for k in ('immutable_ref','revision')),'AUTHORITY_SOURCE');need(n['decision_state'] in ('OWNER_TBD','PROPOSED','UNKNOWN'),'UNVERIFIED_AUTHORITY_PROMOTION')
    for n in d['assertions']:
        fields(n,('id','modality','semantic_role','predicate_ref','scope','guard','authority_refs','decision_state'));ref(n['predicate_ref'],'predicates');need(n['scope']==t['id'],'SCOPE_UNRESOLVED');guard(n['guard']);refs(n['authority_refs'],'authorities');need(n['decision_state'] in ('OWNER_TBD','UNKNOWN','PROPOSED'),'UNVERIFIED_AUTHORITY_PROMOTION');need(all(ref(i,'authorities')['decision_state']==n['decision_state'] for i in n['authority_refs']),'AUTHORITY_STATE_CONFLICT')
    for n in d['observables']:
        fields(n,('id','subject','projection','quantity','aggregation'));ref(n['subject'],'referents');need(expr(n['projection'])==qtype(n['quantity']),'OBSERVABLE_TYPE');need(n['aggregation'] in ('identity','energy_integration') and (n['projection']['op']=='integrate')==(n['aggregation']=='energy_integration'),'OBSERVABLE_AGGREGATION')
    for n in d['variations']:
        fields(n,('id','subject','alternatives','disclosure','source_refs'));ref(n['subject'],'referents');refs(n['source_refs'],'authorities');a=n['alternatives'];need(type(a) is list and len(a)>=2 and all(type(v) is str and v for v in a) and len(set(a))==len(a) and n['disclosure'] is True,'VARIATION_POLICY')
    for n in d['evidences']:
        fields(n,('id','role','subject_ref','status','oracle'));need(n['subject_ref'] in index and index[n['subject_ref']][0] in ('assertions','observables'),'EVIDENCE_SUBJECT');need(n['role']=='REQUEST' and n['status']=='NOT_EXECUTED' and type(n['oracle']) is str and n['oracle'],'UNVERIFIED_EVIDENCE_PROMOTION')
    return TypedAST(copy.deepcopy(d),tuple(sorted(set(unresolved))))
def c21_errors_quantity(q):
    issues=[];c21.quantity(q,'$',issues);return issues

def lower(ast):
    d=copy.deepcopy(ast.document);d['frame'].update(zip(('schema','ruleset','registry'),TARGET))
    for r in d['referents']:
        if r['kind']=='external_port':r['kind']='port';r['external']=True
    for k in ('assertions','authorities'):
        for a in d[k]:a['decision']=a.pop('decision_state')
    return d

def run(source,syntax):
    try:
        d=Parser(source).parse() if syntax=='A' else decode_b(source) if syntax=='B' else None
        ast=typed(d);csnf=lower(ast);norm,report=c21.normalize(csnf)
        need(c21.normalize(norm)[0]==norm,'NON_IDEMPOTENT')
        semantic=c21.semantic_projection(norm)
        audit={'source_versions':SOURCE,'target_versions':TARGET,'source_ast':ast.document,'normalized':norm,'unresolved':ast.unresolved,'validator_blob':'5201bda3c0a611d27e2bc335bbfebc191f252ec7'}
        return dict(status='BLOCKED' if ast.unresolved or any(x['severity']=='BLOCKED' for x in report['diagnostics']) else 'STATIC_VALID_ONLY',semantic_digest=c21.digest(semantic),audit_digest=c21.digest(audit),source_digest=hashlib.sha256(source.encode()).hexdigest(),syntax=syntax,normalized=norm,report=report,unresolved=ast.unresolved)
    except (Reject,c21.CSNFError,ValueError,TypeError,KeyError,AttributeError,RecursionError) as e:return {'status':'REJECTED','error':str(e),'syntax':syntax}
