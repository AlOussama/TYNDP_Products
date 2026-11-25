"""New finite regression cases; NOT the original RC or C23/P5 mutation suite."""
import copy, json, shutil, tempfile, unittest, platform
from pathlib import Path
from fractions import Fraction as F
from n1r import run, emit_a, decode, typed, lower, c21, digest, file_sha, pins, old
from n2r import evaluate
from make_fixtures import contract, q, domain, quant, var, measure, cmp
from units_r1 import Dimension, monetary
ROOT=Path(__file__).parent/'fixtures'
def read(p):return json.loads(Path(p).read_text())
def put(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n');return file_sha(p)
def src(s):return (ROOT/('contract.a.scn' if s=='A' else 'contract.b.json')).read_text()
def logical(d):return json.dumps(d)

class N1R(unittest.TestCase):
    def reject(self,fn,code):
        with self.assertRaisesRegex((ValueError,KeyError,TypeError,AttributeError),code):fn()
    def both(self,d):return [run(emit_a(d),'A'),run(logical(d),'B')]
    def reject_both(self,d,code):
        for syntax,source in [('A',emit_a(d)),('B',logical(d))]:
            with self.subTest(syntax=syntax):self.reject(lambda:run(source,syntax),code)
    def test_dual_syntax_idempotence_and_source(self):
        a,b=[run(src(s),s) for s in ('A','B')];self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertEqual(a['audit_digest'],b['audit_digest']);self.assertNotEqual(a['source_digest'],b['source_digest']);self.assertEqual(c21.normalize(a['normalized'])[0],a['normalized']);self.assertEqual(a['status'],'BLOCKED');self.assertIn('OWNER_UNRESOLVED',a['blocked']);self.assertEqual(a['normalized']['evidences'][0]['status'],'NOT_EXECUTED')
    def test_unknown_operator_c21_defect_and_reject(self):
        d=contract();x=lower(typed(d)[0]);x['predicates'][0]['expr']={'op':'invented'};c21.normalize(x);d['predicates'][0]['expr']={'op':'invented'}
        for s,t in [('A',emit_a(d)),('B',logical(d))]:self.reject(lambda:run(t,s),'UNKNOWN_OPERATOR')
    def test_unbound_variable(self):
        d=contract();d['predicates'][0]['expr']['body']['body']['lhs']['indices'][0]['name']='missing';self.reject_both(d,'UNBOUND_VARIABLE')
    def test_wrong_index_domain(self):
        d=contract();d['predicates'][0]['expr']['body']['body']['lhs']['indices'].reverse();self.reject_both(d,'INDEX_TYPE')
    def test_scope_escape(self):
        d=contract();d['frame']['scopes'][0]['domains']=['domain:scenario'];self.reject_both(d,'SCOPE_ESCAPE')
    def test_guard_ref(self):
        d=contract();d['assertions'][0]['guard']={'atom':'guard:missing'};self.reject_both(d,'GUARD_REF')
    def test_guard_typed_but_unexecuted(self):
        d=contract();d['assertions'][0]['guard']={'atom':'guard:available'}
        for x in self.both(d):self.assertIn('GUARD_APPLICABILITY_NOT_EVALUATED',x['blocked'])
    def test_guard_nonboolean(self):
        d=contract();d['frame']['guards'][0]['expr']={'op':'literal','quantity':q()};self.reject_both(d,'GUARD_TYPE')
    def test_guard_unknown_not_false(self):
        d=contract();d['assertions'][0]['guard']='UNKNOWN'
        for x in self.both(d):self.assertIn('UNKNOWN_GUARD',x['blocked'])
    def test_information_refinement(self):
        d=contract();d['frame']['information_sets'][0]['partition']=[['s1'],['s2']];d['frame']['information_sets'][1]['partition']=[['s1','s2']];self.reject_both(d,'INFORMATION_REFINEMENT')
    def test_duplicate_id(self):
        d=contract();d['referents'].append(copy.deepcopy(d['referents'][0]));self.reject_both(d,'DUPLICATE_ID')
    def test_invalid_observable_projection(self):
        d=contract();d['observables'][0]['projection']['ref']='case:alt';self.reject_both(d,'OBSERVABLE_SUBJECT_PROJECTION')
    def test_authority_conflict(self):
        d=contract();d['assertions'][0]['decision_state']='PROPOSED';self.reject_both(d,'AUTHORITY_CONFLICT')
    def test_evidence_promotion(self):
        d=contract();d['evidences'][0]['status']='PASS';self.reject_both(d,'EVIDENCE_PROMOTION')
    def test_unsupported_approval(self):
        d=contract();d['authorities'][0]['decision_state']='APPROVED';self.reject_both(d,'AUTHORITY')
    def test_nested_quantifier_order(self):
        d=contract();e=d['predicates'][0]['expr'];a=run(logical(d),'B');d['predicates'][0]['expr']=quant('forall','t','time','domain:period',quant('forall','s','scenario','domain:scenario',e['body']['body']));b=run(logical(d),'B');self.assertNotEqual(a['semantic_digest'],b['semantic_digest']);self.assertEqual(a['normalized']['predicates'][0]['expr'],e)
    def test_authority_source_audit_not_semantics(self):
        d=contract();a=run(logical(d),'B');d['authorities'][0]['immutable_ref']='urn:other:source';b=run(logical(d),'B');self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertNotEqual(a['audit_digest'],b['audit_digest'])
    def test_exact_units_and_no_silent_rounding(self):
        d=contract();d['referents'][0]['quantity'].update(unit='kEUR',value='0.1');a=run(logical(d),'B');self.assertEqual(a['normalized']['referents'][1]['quantity']['value'],'100');d['referents'][0]['quantity']['value']='123456789012345678901234567890123456789';self.reject(lambda:run(logical(d),'B'),'INEXACT_DECIMAL_NORMALIZATION')
    def test_duplicate_json_key(self):self.reject(lambda:run('{"frame":{},"frame":{}}','B'),'DUPLICATE_KEY')
    def test_capability_vs_service(self):
        d=contract();d['frame']['domains'] += [domain('domain:req','request',['r1','r2']),domain('domain:res','response',['a1','a2'])];d['frame']['scopes'][0]['domains'] += ['domain:req','domain:res'];body={'op':'bool3','value':'TRUE'};p=d['predicates'][0];p['expr']=quant('forall','r','request','domain:req',quant('exists','a','response','domain:res',body));d['assertions'][0]['semantic_role']='CAPABILITY_GUARANTEE';a=run(logical(d),'B');d['assertions'][0]['semantic_role']='SERVICE_GUARANTEE';b=run(logical(d),'B');self.assertNotEqual(a['semantic_digest'],b['semantic_digest']);self.assertIn('SERVICE_BEHAVIOURAL_EVIDENCE_REQUIRED',b['blocked']);p['expr']=quant('exists','a','response','domain:res',quant('forall','r','request','domain:req',body));self.reject_both(d,'REQUEST_RESPONSE_ORDER')
    def test_legacy_path(self):
        d=contract();d['frame']={k:v for k,v in d['frame'].items() if k in ('id','schema','ruleset','registry','question','time')};d['frame'].update(zip(('schema','ruleset','registry'),old.SOURCE));d['referents']=[];d['relations']=[];d['predicates']=[];d['assertions']=[];d['observables']=[];d['evidences']=[];d['authorities']=[];s=logical(d);self.assertEqual(run(s,'B'),old.run(s,'B'));self.assertEqual(run(old.emit_a(d),'A'),old.run(old.emit_a(d),'A'))

class N2N7(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'fixtures';shutil.copytree(ROOT,self.root)
    def tearDown(self):self.tmp.cleanup()
    def run_profile(self,s='B',timing='begin'):return evaluate(src(s),s,self.root/f'study-{timing}.json',self.root/'trust.json')
    def reject(self,code):
        with self.assertRaisesRegex((ValueError,KeyError,TypeError,AttributeError),code):self.run_profile()
    def mutate(self,name,fn,authorize=False):
        p=self.root/name;x=read(p);fn(x);h=put(p,x)
        if authorize:
            st=self.root/'study-begin.json';s=read(st);trust=self.root/'trust.json';t=read(trust)
            if name=='method-begin.json':s['method_ref']['sha256']=h;t['method_allowlist'].append(h)
            elif name=='data.json':s['data_ref']['sha256']=h;t['data_allowlist'].append(h)
            elif name=='study-begin.json':raise AssertionError('explicit study policy test')
            put(st,s);put(trust,t)
        return h
    def test_integrated_swap_four_runs_oracle_and_hashes(self):
        files=[Path(__file__).parent/k for k in ('n1r.py','n2r.py','n7.py')];before=pins()|{p.name:file_sha(p) for p in files};results={(s,t):self.run_profile(s,t) for s in ('A','B') for t in ('begin','end')};r=F(11,10);oracle={'begin':F(15)+F(25)/r,'end':F(15)/r+F(25)/(r*r)}
        for t in oracle:
            a,b=results['A',t],results['B',t];self.assertEqual(F(a['result']['summary']['rows'][0]['value']),oracle[t]);self.assertEqual(a['result'],b['result']);self.assertEqual(a['chain']['semantic_digest'],b['chain']['semantic_digest']);self.assertEqual(a['audit_digest'],b['audit_digest']);self.assertNotEqual(a['receipt']['run_id'],b['receipt']['run_id']);self.assertEqual(a['audit']['code'],before);self.assertEqual(a['chain']['normalized']['frame']['resolved_profile']['rules'],read(self.root/f'method-{t}.json')['rules']);self.assertEqual(a['audit']['authority']['owner'],'OWNER_TBD');self.assertEqual(a['audit']['authority']['authenticity'],'UNVERIFIED');self.assertEqual(a['receipt']['contract_request_status'],'NOT_EXECUTED')
        a,b=results['A','begin'],results['A','end'];self.assertEqual(a['audit']['data_sha256'],b['audit']['data_sha256']);self.assertNotEqual(a['audit']['method_sha256'],b['audit']['method_sha256']);self.assertNotEqual(a['audit_digest'],b['audit_digest']);self.assertEqual(before,pins()|{p.name:file_sha(p) for p in files})
    def test_method_bytes_changed(self):self.mutate('method-begin.json',lambda x:x.update(version='2'));self.reject('HASH_OR_PATH')
    def test_data_bytes_changed(self):self.mutate('data.json',lambda x:x['contexts'].clear());self.reject('HASH_OR_PATH')
    def test_unauthorized_method_rehash(self):
        h=self.mutate('method-begin.json',lambda x:x.update(version='2'));self.mutate('study-begin.json',lambda x:x['method_ref'].update(sha256=h));self.reject('METHOD_SOURCE_NOT_PERMITTED')
    def test_unauthorized_data_rehash(self):
        h=self.mutate('data.json',lambda x:x['contexts'].clear());self.mutate('study-begin.json',lambda x:x['data_ref'].update(sha256=h));self.reject('STUDY_CONTEXT_NOT_PERMITTED')
    def test_source_substitution(self):
        h=self.mutate('source.json',lambda x:x.update(id='urn:other:source'));self.mutate('method-begin.json',lambda x:x['source'].update(sha256=h),True);self.reject('SOURCE_IDENTITY')
    def test_source_missing(self): (self.root/'source.json').unlink();self.reject('HASH_OR_PATH')
    def test_ledger_policy_override(self):self.mutate('study-begin.json',lambda x:x['ledger_policy']['rules'].update(summary='ALLOW_REUSE'));self.reject('LEDGER_POLICY_NOT_PERMITTED')
    def test_unknown_operator(self):self.mutate('method-begin.json',lambda x:x['rules']['delta']['expr'].update(op='invented'),True);self.reject('UNSUPPORTED_OPERATOR')
    def test_rule_cycle(self):self.mutate('method-begin.json',lambda x:x['rules']['delta'].update(expr={'op':'rule','id':'summary'}),True);self.reject('RULE_CYCLE')
    def test_invalid_basis(self):self.mutate('data.json',lambda x:x['engine_data']['series']['base'].update(basis='USD:real:2030'),True);self.reject('OBSERVABLE_SIGNATURE')
    def test_bad_probability(self):self.mutate('data.json',lambda x:x['engine_data']['series']['probability']['rows'][0].update(value='1'),True);self.reject('PROBABILITY_NORMALIZATION')
    def test_unknown_not_zero(self):self.mutate('data.json',lambda x:x['engine_data']['series']['base']['rows'][0].update(value='UNKNOWN'),True);self.reject('NUMBER_TYPE')
    def test_period_count(self):self.mutate('data.json',lambda x:x['engine_data']['series']['elapsed']['rows'][0].update(value='1/2'),True);self.reject('PERIOD_COUNT')
    def test_observable_binding(self):self.mutate('data.json',lambda x:x['bindings']['base'].update(observable='observable:alt'),True);self.reject('CASE_SUBJECT')
    def test_auxiliary_binding(self):self.mutate('data.json',lambda x:x['bindings']['probability'].update(data_ref='input:elapsed'),True);self.reject('AUXILIARY_INPUT')
    def test_context_content_changed_with_authorized_data(self):
        self.mutate('data.json',lambda x:next(iter(x['contexts'].values())).update(load=['9']),True);self.reject('EXOGENOUS_CONTENT_HASH')
    def test_missing_contribution(self):self.mutate('data.json',lambda x:x['contributions'].pop(),True);self.reject('MISSING_CONTRIBUTION')
    def test_duplicate_contribution(self):self.mutate('data.json',lambda x:x['contributions'].append(copy.deepcopy(x['contributions'][0])),True);self.reject('DUPLICATE_CONTRIBUTION')
    def test_double_count_reject(self):
        self.mutate('method-begin.json',lambda x:x['rules']['delta'].update(expr={'op':'add','lhs':{'op':'input','id':'base'},'rhs':{'op':'input','id':'base'}}),True);self.reject('SEMANTIC_DOUBLE_COUNT')
    def test_permitted_reuse_separate_policy(self):
        def mod(m):m['rules']['aux']=copy.deepcopy(m['rules']['summary']);m['rules']['aux']['expr']={'op':'add','lhs':{'op':'rule','id':'summary'},'rhs':{'op':'rule','id':'summary'}}
        self.mutate('method-begin.json',mod,True);p=self.root/'study-begin.json';s=read(p);s['ledger_policy']['rules']['aux']='ALLOW_REUSE';put(p,s);p=self.root/'trust.json';t=read(p);t['ledger_policy_sha256']=digest(s['ledger_policy']);put(p,t);x=self.run_profile();self.assertEqual(F(x['result']['aux']['rows'][0]['value']),2*F(x['result']['summary']['rows'][0]['value']));self.assertTrue(all(v==2 for v in x['ledger']['aux'].values()));self.assertTrue(all(v==1 for v in x['ledger']['summary'].values()))
    def test_no_result_promotion(self):self.mutate('study-begin.json',lambda x:x.update(status='APPROVED'));self.reject('AUTHORITY_PROMOTION')

class Units(unittest.TestCase):
    def test_dimensional_product(self):self.assertEqual(Dimension.make({'E':1,'T':-1}).combine(Dimension.make({'T':1}),1),Dimension.make({'E':1}));self.assertNotEqual(Dimension.make({'M':1}),Dimension.make({'E':1}))
    def test_explicit_basis_conversion(self):
        r={'schema':'conversion-r1','id':'registry:synthetic','version':'1','rules':[{'id':'rule:fx','from':'USD:nominal:2020','to':'EUR:real:2024','factor':'9/10','source_id':'source:synthetic','source_hash':'a'*64,'authority':'RESEARCH_ASSUMPTION'}]};self.assertEqual(monetary('100','USD:nominal:2020','EUR:real:2024',r,'rule:fx',digest(r))['value'],'90')
        with self.assertRaisesRegex(ValueError,'CONVERSION_SCOPE'):monetary('100','USD:nominal:2021','EUR:real:2024',r,'rule:fx',digest(r))
        with self.assertRaisesRegex(ValueError,'CONVERSION_REGISTRY_HASH'):monetary('100','USD:nominal:2020','EUR:real:2024',r,'rule:fx','b'*64)
if __name__=='__main__':print('Python',platform.python_version(),flush=True);unittest.main(verbosity=2)
