import copy,json,hashlib,sys,platform,unittest
from pathlib import Path
import chain as m
import csnf_validator as c21
D=Path(__file__).parent
rc=m.decode_b((D/'rc01.json').read_text())
def cba_fragment():
    q=lambda v:dict(carrier='currency',kind='cost',unit='EUR',value=v,sign='NONE',basis='EUR:real:2024')
    a=copy.deepcopy(rc['authorities'][0]);a.update(id='CBA:SRC',immutable_ref='synthetic:method-fragment:v1',revision='1')
    f=copy.deepcopy(rc['frame']);f.update(id='CBA:study',question='Synthetic paired cost outputs',time=dict(id='CBA:time',duration='1',duration_unit='h'))
    ref=lambda id,v:dict(id=id,kind='entity',type='currency.cost',quantity=q(v))
    ms=lambda i:dict(op='measure',ref=i)
    return dict(frame=f,referents=[ref('CBA:reference','100'),ref('CBA:project','80')],relations=[{'id':'CBA:pair','kind':'counterfactual_of','from':'CBA:project','to':'CBA:reference','authority_refs':['CBA:SRC']}],predicates=[dict(id='CBA:P',expr=dict(op='compare',cmp='le',lhs=ms('CBA:project'),rhs=ms('CBA:reference')))],assertions=[dict(id='CBA:A',modality='REQUIRED',semantic_role='SERVICE_GUARANTEE',predicate_ref='CBA:P',scope='CBA:time',guard=True,authority_refs=['CBA:SRC'],decision_state='OWNER_TBD')],observables=[dict(id='CBA:O',subject='CBA:project',projection=ms('CBA:project'),quantity=q('80'),aggregation='identity')],variations=[],evidences=[dict(id='CBA:E',role='REQUEST',subject_ref='CBA:A',status='NOT_EXECUTED',oracle='N1-fragment-v1')],authorities=[a])
def run_b(d):return m.run(json.dumps(d),'B')
class Tests(unittest.TestCase):
    def test_00_pin(self):
        for name,sha in [('csnf_validator.py','5201bda3c0a611d27e2bc335bbfebc191f252ec7'),('rc01.json','8cc701c1c841cfc5af266cbcabf89f3570d3fe02'),('rc01_negative.json','0906281f75f187f505da65c5b1376a03360d80fc')]:
            raw=(D/name).read_bytes();self.assertEqual(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest(),sha)
    def pair(self,d):
        a=m.emit_a(d);b=json.dumps(d);self.assertEqual(m.Parser(a).parse(),d)
        x=m.run(a,'A');y=m.run(b,'B');self.assertEqual(x['status'],'BLOCKED',x);self.assertEqual(y['status'],'BLOCKED',y)
        self.assertEqual(x['semantic_digest'],y['semantic_digest']);self.assertEqual(x['audit_digest'],y['audit_digest']);self.assertNotEqual(x['source_digest'],y['source_digest']);self.assertTrue(any(i['code']=='OWNER_UNRESOLVED' for i in x['report']['diagnostics']));self.assertTrue(all(e['status']=='NOT_EXECUTED' for e in x['normalized']['evidences']))
        return x,y
    def test_01_rc01(self):self.pair(rc)
    def test_02_cba(self):self.pair(cba_fragment())
    def test_03_original_negative(self):
        raw=(D/'rc01_negative.json').read_text();d=m.decode_b(raw);issues=c21.validate(d);self.assertEqual([i['code'] for i in issues].count('VERSION_MISMATCH'),2);self.assertIn('OWNER_STATE',[i['code'] for i in issues]);self.assertEqual(m.run(raw,'B')['status'],'REJECTED')
    def test_04_duplicates_b(self):self.assertEqual(m.run('{"frame":{},"frame":{}}','B')['status'],'REJECTED')
    def test_05_duplicates_a(self):self.assertEqual(m.run(m.emit_a(rc).replace('question:', 'question: "extra"; question:',1),'A')['status'],'REJECTED')
    def test_06_version(self):self.mutate(lambda d:d['frame'].update(schema='future'))
    def test_07_unit(self):self.mutate(lambda d:d['referents'][0]['quantity'].update(unit='MWh'))
    def test_08_dimension(self):self.mutate(lambda d:d['predicates'][1]['expr']['rhs']['quantity'].update(kind='active_power',unit='MW'))
    def test_09_scope(self):self.mutate(lambda d:d['assertions'][0].update(scope='RC01:missing'))
    def test_10_unknown_operator(self):self.mutate(lambda d:d['predicates'][0].update(expr={'op':'eval','args':['code']}),both=False)
    def test_11_authority_promotion(self):self.mutate(lambda d:d['authorities'][0].update(decision_state='APPROVED'))
    def test_12_evidence_promotion(self):self.mutate(lambda d:d['evidences'][0].update(status='PASS'))
    def test_13_lexical(self):self.assertEqual(m.run(m.emit_a(rc)+' #extra','A')['status'],'REJECTED')
    def test_14_bool_guard(self):self.mutate(lambda d:d['assertions'][0].update(guard={'op':'NOT','args':[]}))
    def test_15_missing_value(self):self.mutate(lambda d:d['referents'][0]['quantity'].pop('value'))
    def test_16_audit_identity(self):
        a=run_b(rc);d=copy.deepcopy(rc);d['authorities'][0]['immutable_ref']='synthetic:changed-source';b=run_b(d);self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertNotEqual(a['audit_digest'],b['audit_digest'])
    def test_17_exact_conversion(self):
        a=run_b(rc);d=copy.deepcopy(rc);d['frame']['time'].update(duration='30',duration_unit='min');d['referents'][0]['quantity'].update(unit='kW');b=run_b(d);self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertNotEqual(a['audit_digest'],b['audit_digest'])
    def test_18_price_basis(self):self.mutate(lambda d:d['referents'][0]['quantity'].update(basis='EUR:real:2025'),cba_fragment())
    def test_19_unresolved_c21(self):
        # Critical adversarial control: C21 alone does not validate predicate operators.
        d=m.lower(m.typed(rc));d['predicates'][0]['expr']={'op':'invented'};self.assertFalse(any(i['severity']=='ERROR' for i in c21.validate(d)))
    def mutate(self,fn,original=rc,both=True):
        d=copy.deepcopy(original);fn(d);self.assertEqual(run_b(d)['status'],'REJECTED')
        if both:self.assertEqual(m.run(m.emit_a(d),'A')['status'],'REJECTED')
if __name__=='__main__':
    print('Python',platform.python_version(), 'validator',c21.VERSION,flush=True)
    unittest.main(verbosity=2)
