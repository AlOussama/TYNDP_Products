from pathlib import Path
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'N1'))
from test_chain import cba_fragment
import profile_engine as e
D=Path(__file__).parent
write=lambda p,d:(D/p).write_text(json.dumps(d,indent=2)+'\n')
write('contract.json',cba_fragment())
write('method-source.json',dict(id='urn:research:synthetic-source',version='1',status='SYNTHETIC_RESEARCH',description='Illustrative paired value ledger and two timing conventions, not ENTSO-E rules.'))
ref=lambda p:dict(path=p,sha256=e.digest(D/p))
basis='EUR:real:2024';axes=['scenario','period'];schema=lambda unit,basis,axes,role:dict(unit=unit,basis=basis,axes=axes,role=role)
inputs={'base':schema('EUR',basis,axes,'value'),'alternative':schema('EUR',basis,axes,'value'),'probability':schema('1','',['scenario'],'probability'),'duration_weight':schema('1','',['period'],'time_weight'),'elapsed':schema('year','',['period'],'elapsed_years')}
keys=[['s1','t0'],['s1','t1'],['s2','t0'],['s2','t1']]
series=lambda k,keys,vs:dict(**inputs[k],rows=[dict(key=x,value=str(v)) for x,v in zip(keys,vs)])
data=dict(axes=dict(scenario=dict(role='scenario',ids=['s1','s2']),period=dict(role='time',ids=['t0','t1'])),series={'base':series('base',keys,[100,100,100,100]),'alternative':series('alternative',keys,[80,70,90,80]),'probability':series('probability',[['s1'],['s2']],['1/2','1/2']),'duration_weight':series('duration_weight',[['t0'],['t1']],[1,1]),'elapsed':series('elapsed',[['t0'],['t1']],[0,1])},pairs=[dict(id='pair-1',reference='base',alternative='alternative',reference_snapshot='synthetic:shared-exogenous:v1',alternative_snapshot='synthetic:shared-exogenous:v1')]);write('data.json',data)
def node(op,**kw):return dict(op=op,**kw)
bi=lambda op,a,b:node(op,lhs=a,rhs=b)
param=lambda k:node('param',id=k)
inp=lambda k:node('input',id=k)
rule=lambda k:node('rule',id=k)
lit=lambda v,u='1':node('literal',value=str(v),unit=u)
sel=lambda side:node('select_case',pair='pair-1',side=side)
red=lambda x,a,w:node('weighted_sum',expr=x,axis=a,weight=w)
expr=bi('sub',sel('reference'),sel('alternative'))
base=bi('add',lit(1),param('rate'))
ruledef=lambda x,ax:dict(expr=x,unit='EUR',basis=basis,axes=ax)
for name,shift in [('begin',0),('end',1)]:
    exponent=inp('elapsed') if shift==0 else bi('add',inp('elapsed'),lit(1,'year'))
    discounted=bi('div',rule('delta'),bi('pow',base,exponent))
    summary=red(red(rule('discounted'),'period','duration_weight'),'scenario','probability')
    m=dict(id='urn:method:timing-'+name,version='1',schema='profile-r1',operator_version='operators-r1',source=ref('method-source.json'),approval='RESEARCH_ASSUMPTION',assumptions=['Finite paired case data; '+name+'-period timing; no official CBA conformity'],parameters={'rate':dict(unit='1',min='0',max='1')},inputs=inputs,rules={'delta':ruledef(expr,axes),'discounted':ruledef(discounted,axes),'summary':ruledef(summary,[])})
    write('method-'+name+'.json',m)
    write('study-'+name+'.json',dict(id='urn:study:paired',version=name+'-1',schema='profile-r1',method_ref=ref('method-'+name+'.json'),parameters={'rate':'1/10'},data_ref=ref('data.json'),contract_ref=e.digest(D/'contract.json'),status='OWNER_TBD'))
