import copy, json, sys, tempfile, shutil, unittest, hashlib, platform
from pathlib import Path
from fractions import Fraction as F
import profile_engine as e
D=Path(__file__).parent
N1=D.parent/'N1';sys.path.insert(0,str(N1))
import chain
m=e.read(D/'method-begin.json');s=e.read(D/'study-begin.json');d=e.read(D/'data.json')
class Tests(unittest.TestCase):
    def test_00_swap(self):
        paths=[D/'profile_engine.py',N1/'chain.py',N1/'csnf_validator.py'];before=[e.digest(p) for p in paths]
        results=[]
        for case in ('begin','end'):
            a=chain.run((D/'contract.json').read_text(),'B');b=chain.run(chain.emit_a(e.read(D/'contract.json')),'A');self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertEqual(a['audit_digest'],b['audit_digest']);self.assertEqual(a['status'],'BLOCKED');results.append(e.run(D/f'study-{case}.json',D/'contract.json'))
        self.assertEqual(before,[e.digest(p) for p in paths]);x,y=results;self.assertEqual(x['result']['summary']['rows'][0]['value'],str(F(15)+F(25)/F('1.1')));self.assertEqual(y['result']['summary']['rows'][0]['value'],str(F(15)/F('1.1')+F(25)/F('1.1')**2));self.assertNotEqual(x['audit_digest'],y['audit_digest']);self.assertEqual(x['audit']['contract_sha256'],y['audit']['contract_sha256']);self.assertNotEqual(x['audit']['method_sha256'],y['audit']['method_sha256']);self.assertEqual(x['audit']['status'],'OWNER_TBD')
    def mutate(self,fn):
        a,b,c=copy.deepcopy((m,s,d));fn(a,b,c)
        with self.assertRaises(e.Rejected):e.Engine(a,b,c).run()
    def test_01_unknown_op(self):self.mutate(lambda a,b,c:a['rules']['delta'].update(expr={'op':'eval','code':'x'}))
    def test_02_units(self):self.mutate(lambda a,b,c:c['series']['base'].update(unit='MWh'))
    def test_03_basis(self):self.mutate(lambda a,b,c:c['series']['alternative'].update(basis='EUR:real:2025'))
    def test_04_weights_missing(self):self.mutate(lambda a,b,c:c['series']['probability']['rows'].pop())
    def test_05_weights_sum(self):self.mutate(lambda a,b,c:c['series']['probability']['rows'][0].update(value='3/4'))
    def test_06_wrong_weight_role(self):self.mutate(lambda a,b,c:a['rules']['summary']['expr'].update(weight='duration_weight'))
    def test_07_exogenous(self):self.mutate(lambda a,b,c:c['pairs'][0].update(alternative_snapshot='different'))
    def test_08_same_case(self):self.mutate(lambda a,b,c:c['pairs'][0].update(alternative='base'))
    def test_09_double_row(self):self.mutate(lambda a,b,c:c['series']['base']['rows'].append(c['series']['base']['rows'][0]))
    def test_10_operator_version(self):self.mutate(lambda a,b,c:a.update(operator_version='future'))
    def test_11_reference(self):self.mutate(lambda a,b,c:a['rules']['delta'].update(expr={'op':'rule','id':'missing'}))
    def test_12_authority(self):self.mutate(lambda a,b,c:a.update(approval='APPROVED'))
    def test_13_study_status(self):self.mutate(lambda a,b,c:b.update(status='PASS'))
    def test_14_parameter_domain(self):self.mutate(lambda a,b,c:b['parameters'].update(rate='-1'))
    def test_15_hash(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            for n in ('method-begin.json','study-begin.json','method-source.json','data.json','contract.json'):shutil.copyfile(D/n,p/n)
            (p/'method-begin.json').write_bytes((p/'method-begin.json').read_bytes()+b' ')
            with self.assertRaisesRegex(e.Rejected,'HASH_MISMATCH'):e.run(p/'study-begin.json',p/'contract.json')
    def test_16_cycle(self):self.mutate(lambda a,b,c:a['rules']['delta'].update(expr={'op':'rule','id':'delta'}))
    def test_17_rule_type(self):self.mutate(lambda a,b,c:a['rules']['summary'].update(unit='MWh'))
    def test_18_double_formula_limit(self):
        # Semantically double-counting the same rule remains legal arithmetic: negative capability finding.
        a,b,c=copy.deepcopy((m,s,d));original=a['rules']['summary']['expr'];a['rules']['summary']['expr']={'op':'add','lhs':original,'rhs':original};v=e.Engine(a,b,c).run();self.assertEqual(v['summary']['rows'][0]['value'],str(2*(F(15)+F(25)/F('1.1'))))
if __name__=='__main__':
    print('Python',platform.python_version(),flush=True);unittest.main(verbosity=2)
