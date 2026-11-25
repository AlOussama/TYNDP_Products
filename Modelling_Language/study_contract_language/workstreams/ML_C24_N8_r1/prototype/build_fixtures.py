from pathlib import Path
import json,copy,itertools
from research_chain import call,VERSION,chain,digest
P=Path(__file__).parent
def put(n,d): (P/n).write_text(json.dumps(d,indent=2)+'\n')
q={'carrier':'currency','kind':'cost','unit':'EUR','value':'0','sign':'NONE','basis':'EUR:real:2024'}
d={'frame':{'id':'study:paired','schema':'C20-research-0.1','ruleset':'CSNF-R0','registry':VERSION,'question':'Synthetic paired cost observables','time':{'id':'time:base','duration':'1','duration_unit':'h'},'domains':[{'id':'axis:t','kind':'time','members':['y1','y2']},{'id':'axis:s','kind':'scenario','members':['low','high']}],'flags':[{'id':'flag:applicable','type':'Bool3'}],'weights':[{'id':'w:p','axis':'axis:s','role':'probability'},{'id':'w:t','axis':'axis:t','role':'time_weight'},{'id':'w:y','axis':'axis:t','role':'elapsed_years'}]},'referents':[{'id':'case:'+i,'kind':'entity','quantity':q} for i in ('base','alt')],'relations':[{'id':'pair:1','kind':'counterfactual_of','from':'case:alt','to':'case:base','authority_refs':['auth:synthetic']}],'predicates':[{'id':'pred:bounds','expr':call('forall','t','axis:t',call('forall','s','axis:s',call('le',call('at','obs:alt',call('var','t'),call('var','s')),call('at','obs:base',call('var','t'),call('var','s')))))}],'assertions':[{'id':'assert:bounds','modality':'CONDITIONAL','semantic_role':'SAFETY_GUARANTEE','predicate_ref':'pred:bounds','scope':'axis:t','guard':call('flag','flag:applicable'),'authority_refs':['auth:synthetic'],'decision_state':'OWNER_TBD'}],'observables':[{'id':'obs:'+i,'subject':'case:'+i,'quantity':q,'axes':['axis:t','axis:s'],'aggregation':'identity'} for i in ('base','alt')],'variations':[],'evidences':[{'id':'ev:bounds','role':'REQUEST','subject_ref':'assert:bounds','status':'NOT_EXECUTED','oracle':'oracle:finite'}],'authorities':[{'id':'auth:synthetic','role':'SOURCE','immutable_ref':'synthetic:paired-cost-v1','revision':'1','decision_state':'OWNER_TBD'}]}
put('contract.b.json',d)
context={'demand':'synthetic-dataset-1','network':'synthetic-network-1','weather':'synthetic-weather-1'}
keys=list(itertools.product(['y1','y2'],['low','high']))
data={'id':'data:paired','context':context,'cases':{'case:base':digest(context),'case:alt':digest(context)},'observations':{k:[{'key':list(key),'value':str(v)} for key,v in zip(keys,vs)] for k,vs in [('obs:base',[100,120,150,180]),('obs:alt',[80,90,110,120])]},'flags':{'flag:applicable':True},'weights':{'w:p':{'low':'1/4','high':'3/4'},'w:t':{'y1':'1','y2':'1'},'w:y':{'y1':'1','y2':'2'}}}
put('data.json',data)
t,s=call('var','t'),call('var','s');delta=call('sub',call('at','obs:base',t,s),call('at','obs:alt',t,s));type_cost=['currency','cost','EUR:real:2024','NONE']
for variant in ('undiscounted','discounted'):
    inner=delta if variant=='undiscounted' else call('div',delta,call('pow',call('add',call('scalar','1'),call('param','rate')),call('weight','w:y',t)))
    expr=call('sum','t','axis:t',call('mul',call('weight','w:t',t),call('sum','s','axis:s',call('mul',call('weight','w:p',s),inner))))
    method={'id':'method:'+variant,'version':'1','registry':VERSION,'authority':'OWNER_TBD','parameters':{'rate':{'min':'0','max':'1'}},'rules':[{'id':'rule:result','expr':expr,'type':type_cost}],'ledger':[{'id':'contribution:paired','atoms':['impact:operating-cost']}],'expected_atoms':['impact:operating-cost']}
    study={'id':'study-profile:paired','version':'1','method_hash':digest(method),'data_hash':digest(data),'contract_semantic':chain((P/'contract.b.json').read_text(),'B')[0]['semantic_digest'],'parameters':{'rate':'1/10'},'status':'OWNER_TBD'}
    put('method-'+variant+'.json',method);put('study-'+variant+'.json',study)
