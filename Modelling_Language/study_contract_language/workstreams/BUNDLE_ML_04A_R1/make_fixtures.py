"""One-time fixture generation; never invoked during a profile swap."""
from pathlib import Path
from copy import deepcopy
import json
from n1r import c21, typed, lower, digest, file_sha, emit_a, VERSION
ROOT=Path(__file__).parent/'fixtures'
def save(name,x):
    p=ROOT/name;p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');return {'path':name,'sha256':file_sha(p)}
def q(value='0',kind='cost',carrier='currency',unit='EUR',sign='NONE',basis='EUR:real:2024'):
    out=dict(carrier=carrier,kind=kind,unit=unit,value=value,sign=sign)
    if basis:out['basis']=basis
    return out
def domain(id,kind,members):return dict(id=id,kind=kind,members=members)
def var(name):return dict(op='var',name=name)
def measure(ref,*names):return dict(op='measure',ref=ref,indices=[var(n) for n in names])
def quant(op,var,kind,ref,body):return dict(op=op,var=var,domain=dict(kind=kind,ref=ref),body=body)
def cmp(lhs,rhs,cmp='le'):return dict(op='compare',cmp=cmp,lhs=lhs,rhs=rhs)
def contract():
    axes=['domain:scenario','domain:period'];f=dict(id='study:paired',schema=VERSION[0],ruleset=VERSION[1],registry=VERSION[2],question='Finite synthetic paired observable study',time=dict(id='study:duration',duration='1',duration_unit='h'),domains=[domain(axes[0],'scenario',['s1','s2']),domain(axes[1],'time',['t0','t1'])],scopes=[dict(id='scope:pair',domains=list(axes))],guards=[dict(id='guard:available',expr=dict(op='bool3',value='TRUE'))],information_sets=[dict(id='info:initial',time_domain=axes[1],stage='t0',scenario_domain=axes[0],partition=[['s1','s2']]),dict(id='info:revealed',time_domain=axes[1],stage='t1',scenario_domain=axes[0],partition=[['s1'],['s2']])],data_inputs=[dict(id='input:probability',role='probability',axes=[axes[0]],unit='1',basis=''),dict(id='input:duration_weight',role='time_weight',axes=[axes[1]],unit='1',basis=''),dict(id='input:elapsed',role='period_count',axes=[axes[1]],unit='1',basis='')],method_slots=[dict(id='slot:cost',observables=['observable:base','observable:alt'],data_inputs=['input:probability','input:duration_weight','input:elapsed'])]);d={k:[] for k in c21.COLLECTIONS};d['frame']=f
    for name in ('base','alt'):
        d['referents'].append(dict(id='case:'+name,kind='entity',type='currency.cost',quantity=q(),axes=list(axes)));d['observables'].append(dict(id='observable:'+name,subject='case:'+name,projection=measure('case:'+name,'s','t'),quantity=q(),aggregation='identity',bindings=[dict(var='s',domain=axes[0]),dict(var='t',domain=axes[1])]))
    d['authorities']=[dict(id='source:research',role='SOURCE',immutable_ref='urn:research:synthetic-source',revision='1',decision_state='OWNER_TBD')];d['relations']=[{'id':'relation:pair','kind':'counterfactual_of','from':'case:alt','to':'case:base','authority_refs':['source:research']}]
    d['predicates']=[dict(id='predicate:comparison',expr=quant('forall','s','scenario',axes[0],quant('forall','t','time',axes[1],cmp(measure('case:alt','s','t'),measure('case:base','s','t')))))];d['assertions']=[dict(id='assertion:comparison',modality='REQUIRED',semantic_role='SAFETY_GUARANTEE',predicate_ref='predicate:comparison',scope='scope:pair',guard=True,authority_refs=['source:research'],decision_state='OWNER_TBD')];d['evidences']=[dict(id='evidence:comparison',role='REQUEST',subject_ref='assertion:comparison',status='NOT_EXECUTED',oracle='research:finite-paired')];return d

def main():
    ROOT.mkdir(exist_ok=True);d=contract();save('contract.b.json',d);(ROOT/'contract.a.scn').write_text(emit_a(d),encoding='utf-8');norm,_=c21.normalize(lower(typed(d)[0]));ch=digest(norm)
    axes=['domain:scenario','domain:period'];ctx=dict(id='context:shared',load=['1','2'],scenario_set=['s1','s2'],period_set=['t0','t1']);ex=digest(ctx);keys=[['s1','t0'],['s1','t1'],['s2','t0'],['s2','t1']]
    def series(unit,basis,axs,role,ks,vs):return dict(unit=unit,basis=basis,axes=axs,role=role,rows=[dict(key=k,value=v) for k,v in zip(ks,vs)])
    ed=dict(axes={axes[0]:dict(role='scenario',ids=['s1','s2']),axes[1]:dict(role='time',ids=['t0','t1'])},series={'base':series('EUR','EUR:real:2024',axes,'value',keys,['100']*4),'alternative':series('EUR','EUR:real:2024',axes,'value',keys,['80','70','90','80']),'probability':series('1','',[axes[0]],'probability',[['s1'],['s2']],['1/2','1/2']),'duration_weight':series('1','',[axes[1]],'time_weight',[['t0'],['t1']],['1','1']),'elapsed':series('1','',[axes[1]],'value',[['t0'],['t1']],['0','1'])},pairs=[dict(id='pair-1',reference='base',alternative='alternative',reference_snapshot=ex,alternative_snapshot=ex)])
    bindings={k:dict(role='auxiliary',observable='',case='',data_ref='input:'+k) for k in ed['series']};bindings['base']=dict(role='contribution',observable='observable:base',case='case:base',data_ref='');bindings['alternative']=dict(role='contribution',observable='observable:alt',case='case:alt',data_ref='');rows=[]
    for k in ('base','alternative'):
        for i,key in enumerate(keys):rows.append(dict(id='contribution:'+k+str(i),series=k,key=key,case=bindings[k]['case'],observable=bindings[k]['observable'],event='cost:operation'))
    data=dict(schema='snapshot-r1',engine_data=ed,bindings=bindings,contexts={ex:ctx},cases={k:dict(referent=k,exogenous_ref=ex) for k in ('case:base','case:alt')},contributions=rows);dataref=save('data.json',data)
    srcref=save('source.json',dict(id='urn:research:synthetic-source',version='1',status='SYNTHETIC_RESEARCH',description='Illustrative timing alternatives, no official method.'))
    def binary(op,lhs,rhs):return dict(op=op,lhs=lhs,rhs=rhs)
    def ref(op,id):return dict(op=op,id=id)
    def rule(expr,axs):return dict(expr=expr,unit='EUR',basis='EUR:real:2024',axes=axs)
    def lit(v):return dict(op='literal',value=v,unit='1')
    def weighted(expr,axis,weight):return dict(op='weighted_sum',expr=expr,axis=axis,weight=weight)
    policy=dict(schema='ledger-policy-r1',id='policy:disjoint',version='1',rules={k:'DISJOINT' for k in ('delta','discounted','summary')},expected={'summary':sorted(digest([r['case'],r['key'],r['event']]) for r in rows)})
    methods=[]
    for timing in ('begin','end'):
        elapsed=ref('input','elapsed');exponent=elapsed if timing=='begin' else binary('add',elapsed,lit('1'))
        rules={'delta':rule(binary('sub',dict(op='select_case',pair='pair-1',side='reference'),dict(op='select_case',pair='pair-1',side='alternative')),axes),'discounted':rule(binary('div',ref('rule','delta'),binary('pow',binary('add',lit('1'),ref('param','rate')),exponent)),axes),'summary':rule(weighted(weighted(ref('rule','discounted'),axes[1],'duration_weight'),axes[0],'probability'),[])}
        m=dict(id='urn:method:'+timing,version='1',schema='profile-r1',operator_version='operators-r1',source=srcref,approval='RESEARCH_ASSUMPTION',assumptions=['Finite synthetic period-count discounting; '+timing],parameters={'rate':dict(unit='1',min='0',max='1')},inputs={k:{a:v for a,v in s.items() if a!='rows'} for k,s in ed['series'].items()},rules=rules);mr=save('method-'+timing+'.json',m);methods.append(mr['sha256']);save('study-'+timing+'.json',dict(schema='study-r1',id='urn:study:paired',version=timing+'-1',method_ref=mr,data_ref=dataref,contract_ref=ch,parameters={'rate':'1/10'},status='OWNER_TBD',slot='slot:cost',ledger_policy=policy))
    save('trust.json',dict(source_id='urn:research:synthetic-source',source_version='1',source_sha256=srcref['sha256'],authenticity='UNVERIFIED',publication='SYNTHETIC',method_allowlist=methods,ledger_policy_sha256=digest(policy),data_allowlist=[dataref['sha256']],contract_allowlist=[ch],study_id='urn:study:paired'))
if __name__=='__main__':main()
