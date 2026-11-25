"""Typed finite expression experiment; no dynamic code, no domain method constants."""
import hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
from dataclasses import dataclass
from itertools import product
class Rejected(ValueError):pass
def req(c,msg):
    if not c:raise Rejected(msg)
def pairs(items):
    d={}
    for k,v in items:req(k not in d,'DUPLICATE_KEY');d[k]=v
    return d
def read(p):return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Rejected('NONFINITE')))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def shape(x,keys):req(type(x) is dict and set(x)==set(keys.split()),'FIELDS')
def rational(x):
    req(type(x) in (int,str),'NUMBER_TYPE')
    try:return F(x)
    except (ValueError,ZeroDivisionError):raise Rejected('NUMBER_TYPE')
@dataclass(frozen=True)
class Type:
    unit:str;basis:str;axes:tuple
@dataclass(frozen=True)
class Value:
    type:Type;values:dict
class Engine:
    def __init__(self,method,study,data):
        shape(method,'id version schema operator_version source approval assumptions parameters inputs rules');shape(study,'id version schema method_ref parameters data_ref contract_ref status');shape(data,'axes series pairs')
        req(method['schema']==study['schema']=='profile-r1' and method['operator_version']=='operators-r1','VERSION')
        req(method['approval']=='RESEARCH_ASSUMPTION' and study['status']=='OWNER_TBD','AUTHORITY')
        req(all(type(method[k]) is str and method[k] for k in ('id','version')) and all(type(study[k]) is str and study[k] for k in ('id','version')),'IDENTITY')
        req(type(method['assumptions']) is list and method['assumptions'] and all(type(a) is str and a for a in method['assumptions']),'ASSUMPTIONS')
        self.axes=data['axes'];self.method=method;self.study=study;self.data=data;self.params={};self.series={};self.rules={};self.cache={};self.active=set()
        req(type(self.axes) is dict and self.axes,'AXES')
        for k,a in self.axes.items():
            shape(a,'role ids');req(a['role'] in ('time','scenario','sample') and type(a['ids']) is list and a['ids'] and all(type(i) is str and i for i in a['ids']) and len(set(a['ids']))==len(a['ids']),'AXIS')
        req(type(method['parameters']) is dict and type(study['parameters']) is dict and set(method['parameters'])==set(study['parameters']),'PARAMETER_SET')
        for k,p in method['parameters'].items():
            shape(p,'unit min max');req(p['unit'] in ('1','year'),'PARAMETER_UNIT');v=rational(study['parameters'][k]);req(rational(p['min'])<=v<=rational(p['max']),'PARAMETER_RANGE');self.params[k]=Value(Type(p['unit'],'',()),{():v})
        req(type(method['inputs']) is dict and set(method['inputs'])==set(data['series']),'INPUT_SET')
        for k,p in method['inputs'].items():
            shape(p,'unit basis axes role');s=data['series'][k];shape(s,'unit basis axes role rows');req(all(s[x]==p[x] for x in p),'INPUT_TYPE');req(type(p['axes']) is list and len(set(p['axes']))==len(p['axes']) and all(a in self.axes for a in p['axes']),'INPUT_AXES')
            req(p['unit'] in ('EUR','1','year','MWh') and ((p['unit']=='EUR' and type(p['basis']) is str and p['basis'].startswith('EUR:real:')) or (p['unit']!='EUR' and p['basis']=='')),'BASIS')
            if p['role'] in ('probability','time_weight'):req(p['unit']=='1' and len(p['axes'])==1 and self.axes[p['axes'][0]]['role']==('scenario' if p['role']=='probability' else 'time'),'WEIGHT_ROLE')
            else:req(p['role'] in ('value','elapsed_years'),'INPUT_ROLE')
            v={}
            for row in s['rows']:
                shape(row,'key value');req(type(row['key']) is list and all(type(x) is str for x in row['key']),'ROW_KEY');key=tuple(row['key']);req(key not in v,'DUPLICATE_ROW');v[key]=rational(row['value'])
            req(set(v)==set(self.keys(tuple(p['axes']))),'DOMAIN_COVERAGE')
            if p['role']=='probability':req(all(z>=0 for z in v.values()) and sum(v.values())==1,'PROBABILITY_NORMALIZATION')
            if p['role']=='time_weight':req(all(z>0 for z in v.values()),'TIME_WEIGHT')
            if p['role']=='elapsed_years':req(p['unit']=='year' and all(z>=0 and z.denominator==1 for z in v.values()),'TIME_COORDINATE')
            self.series[k]=Value(Type(p['unit'],p['basis'],tuple(p['axes'])),v)
        req(type(data['pairs']) is list,'PAIR_SET');self.pairs={};used=set()
        for pair in data['pairs']:
            shape(pair,'id reference alternative reference_snapshot alternative_snapshot');i=pair['id'];a=pair['reference'];b=pair['alternative'];req(type(i) is str and i and i not in self.pairs and a!=b and a in self.series and b in self.series,'PAIR_IDENTITY')
            req(type(pair['reference_snapshot']) is str and bool(pair['reference_snapshot']) and pair['reference_snapshot']==pair['alternative_snapshot'],'COUNTERFACTUAL_EXOGENEITY');req(self.series[a].type==self.series[b].type,'PAIR_TYPE');req((a,b) not in used and (b,a) not in used,'DUPLICATE_PAIR');used.add((a,b));self.pairs[i]=pair
        req(type(method['rules']) is dict and method['rules'],'RULES')
        for k,r in method['rules'].items():shape(r,'expr unit basis axes');self.rules[k]=r
    def keys(self,axes):return product(*(self.axes[k]['ids'] for k in axes))
    def broadcast(self,v,axes,key):return v.values[tuple(key[axes.index(a)] for a in v.type.axes)]
    def binary(self,op,a,b):
        x,y=a.type,b.type;axes=x.axes+tuple(k for k in y.axes if k not in x.axes)
        if op in ('add','sub'):req((x.unit,x.basis)==(y.unit,y.basis),'DIMENSION_BASIS');unit,basis=x.unit,x.basis
        elif op=='mul':req('1' in (x.unit,y.unit),'UNSUPPORTED_DIMENSION_PRODUCT');unit,basis=(y.unit,y.basis) if x.unit=='1' else (x.unit,x.basis)
        elif op=='div':req(y.unit=='1','UNSUPPORTED_DIMENSION_DIVISION');unit,basis=x.unit,x.basis
        else:req(x.unit=='1' and y.unit in ('1','year'),'POWER_TYPE');unit,basis='1',''
        out={}
        for key in self.keys(axes):
            u=self.broadcast(a,axes,key);v=self.broadcast(b,axes,key)
            if op=='pow':req(v.denominator==1 and abs(v)<=200 and (u!=0 or v>=0),'POWER_DOMAIN');z=u**int(v)
            elif op=='div':req(v!=0,'ZERO_DIVISOR');z=u/v
            elif op=='add':z=u+v
            elif op=='sub':z=u-v
            else:z=u*v
            out[key]=z
        return Value(Type(unit,basis,axes),out)
    def evaluate(self,e):
        req(type(e) is dict and type(e.get('op')) is str,'TYPED_AST');op=e['op']
        if op in ('input','param','rule'):
            shape(e,'op id');k=e['id'];table=self.series if op=='input' else self.params if op=='param' else self.rules;req(type(k) is str and k in table,'UNRESOLVED_REFERENCE');return self.rule(k) if op=='rule' else table[k]
        if op=='literal':shape(e,'op value unit');req(e['unit'] in ('1','year'),'LITERAL_UNIT');return Value(Type(e['unit'],'',()),{():rational(e['value'])})
        if op=='select_case':
            shape(e,'op pair side');req(e['pair'] in self.pairs and e['side'] in ('reference','alternative'),'PAIR_SELECTION');return self.series[self.pairs[e['pair']][e['side']]]
        if op in ('add','sub','mul','div','pow'):shape(e,'op lhs rhs');return self.binary(op,self.evaluate(e['lhs']),self.evaluate(e['rhs']))
        if op=='weighted_sum':
            shape(e,'op expr axis weight');v=self.evaluate(e['expr']);axis=e['axis'];w=e['weight'];req(axis in v.type.axes and w in self.series,'AGGREGATION_DOMAIN');weight=self.series[w];role=self.method['inputs'][w]['role'];req(weight.type==Type('1','',(axis,)) and role in ('probability','time_weight'),'WEIGHT_TYPE');axes=tuple(a for a in v.type.axes if a!=axis);i=v.type.axes.index(axis);out={k:F(0) for k in self.keys(axes)}
            for k,x in v.values.items():out[k[:i]+k[i+1:]]+=x*weight.values[(k[i],)]
            return Value(Type(v.type.unit,v.type.basis,axes),out)
        raise Rejected('UNSUPPORTED_OPERATOR:'+op)
    def rule(self,k):
        if k in self.cache:return self.cache[k]
        req(k not in self.active,'RULE_CYCLE');self.active.add(k);r=self.rules[k];v=self.evaluate(r['expr']);req(v.type==Type(r['unit'],r['basis'],tuple(r['axes'])),'RULE_TYPE');self.cache[k]=v;self.active.remove(k);return v
    def run(self):
        return {k:{'unit':v.type.unit,'basis':v.type.basis,'axes':v.type.axes,'rows':[{'key':key,'value':str(x)} for key,x in v.values.items()]} for k in self.rules for v in [self.rule(k)]}
def resolve(root,ref):
    shape(ref,'path sha256');p=(root/ref['path']).resolve();req(p.is_relative_to(root) and p.is_file(),'SOURCE_PATH');req(digest(p)==ref['sha256'],'HASH_MISMATCH');return p

def run(study_path,contract_path):
    root=Path(study_path).resolve().parent;s=read(study_path);mp=resolve(root,s['method_ref']);m=read(mp);dp=resolve(root,s['data_ref']);sp=resolve(root,m['source']);source=read(sp);shape(source,'id version status description');req(source['status']=='SYNTHETIC_RESEARCH','SOURCE_STATUS');req(digest(contract_path)==s['contract_ref'],'CONTRACT_HASH');result=Engine(m,s,read(dp)).run()
    audit=dict(method_id=m['id'],method_version=m['version'],study_id=s['id'],study_version=s['version'],method_sha256=digest(mp),study_sha256=digest(study_path),source_sha256=digest(sp),data_sha256=digest(dp),contract_sha256=digest(contract_path),operator_version=m['operator_version'],parameters=s['parameters'],result=result,status='OWNER_TBD',engine_sha256=digest(__file__))
    return dict(result=result,audit=audit,audit_digest=canon(audit))
if __name__=='__main__':print(json.dumps(run(sys.argv[1],sys.argv[2]),indent=2))
