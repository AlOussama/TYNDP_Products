"""Pure synthetic, stdlib-only tests of CSNF-C21-0.1 executable fragment."""
import copy
import unittest
from csnf_validator import normalize, validate, compare_e1, digest, CSNFError

def base():
    return {
        'frame':{'id':'urn:study:r01','schema':'CSNF-C21-0.1','ruleset':'CSNF-R0',
                 'registry':'energy-c21-0.1','time':{'duration':'0.5','duration_unit':'h'}},
        'referents':[
            {'id':'urn:port:grid','kind':'port','quantity':{'carrier':'electricity','kind':'active_power','unit':'MW','value':'1','sign':'INJECTION'}},
            {'id':'urn:port:bus','kind':'port','quantity':{'carrier':'electricity','kind':'active_power','unit':'MW','value':'1','sign':'CONSUMPTION'}}],
        'relations':[{'id':'urn:edge:1','kind':'connected_to','from':'urn:port:grid','to':'urn:port:bus'}],
        'predicates':[{'id':'urn:pred:1','kind':'KCL_AND_KVL','expr':'typed-external-obligation'}],
        'assertions':[{'id':'urn:assert:1','modality':'REQUIRED','decision':'APPROVED',
                        'semantic_role':'SAFETY_GUARANTEE','predicate_ref':'urn:pred:1',
                        'scope':'urn:scope:all','guard':{'op':'AND','args':[{'atom':'connected'},{'atom':'available'}]},
                        'authority_refs':['urn:auth:1','urn:auth:2']}],
        'observables':[{'id':'urn:obs:1','aggregation':'energy_integration',
                        'quantity':{'carrier':'electricity','kind':'energy','unit':'MWh','value':'1','sign':'NONE'}}],
        'variations':[{'id':'urn:var:1','allowed':['SOC','ENERGY_STATE'],'disclosure':True}],
        'evidences':[{'id':'urn:evidence:1','role':'REQUEST','subject_ref':'urn:assert:1','status':'NOT_EXECUTED'}],
        'authorities':[{'id':'urn:auth:1','immutable_ref':'doc:1@v1','decision':'APPROVED'},
                       {'id':'urn:auth:2','immutable_ref':'doc:2@v1','decision':'APPROVED'}]
    }

class TestValidator(unittest.TestCase):
    def assertCode(self,c,code):
        self.assertIn(code,[x['code'] for x in validate(c)])
        with self.assertRaises(CSNFError):normalize(c)
    def test_valid(self):self.assertFalse([x for x in validate(base()) if x['severity']=='ERROR'])
    def test_idempotent(self):
        first,_=normalize(base()); second,_=normalize(first);self.assertEqual(first,second)
    def test_deterministic(self):
        a=base();b=base();b['authorities'].reverse();b['referents'].reverse();self.assertEqual(normalize(a)[0],normalize(b)[0])
    def test_boolean_commutativity(self):
        a=base();b=base();b['assertions'][0]['guard']['args'].reverse();self.assertEqual(compare_e1(a,b)['e1'],'E1_EQUAL')
    def test_boolean_associativity(self):
        a=base();b=base();b['assertions'][0]['guard']={'op':'AND','args':[{'atom':'connected'},{'op':'AND','args':[{'atom':'available'},{'atom':'true'}]}]};a['assertions'][0]['guard']['args'].append({'atom':'true'});self.assertEqual(compare_e1(a,b)['e1'],'E1_EQUAL')
    def test_kW_to_MW(self):
        a=base();b=base();b['referents'][0]['quantity'].update(value='1000',unit='kW');self.assertEqual(compare_e1(a,b)['e1'],'E1_EQUAL')
    def test_min_to_h(self):
        a=base();b=base();b['frame']['time'].update(duration='30',duration_unit='min');self.assertEqual(compare_e1(a,b)['e1'],'E1_EQUAL')
    def test_owner_tbd_preserved(self):
        a=base();a['assertions'][0]['decision']='OWNER_TBD';b,trace=normalize(a);self.assertEqual(b['assertions'][0]['decision'],'OWNER_TBD');self.assertIn('OWNER_UNRESOLVED',[d['code'] for d in trace['diagnostics']]);self.assertEqual(compare_e1(base(),a)['e1'],'E1_DIFFERENT')
    def test_not_executed_preserved(self):
        a,_=normalize(base());self.assertEqual(a['evidences'][0]['status'],'NOT_EXECUTED')
    def test_two_sources_preserved(self):
        a,_=normalize(base());self.assertEqual(len(a['authorities']),2);self.assertEqual(len(a['assertions'][0]['authority_refs']),2)
    def test_audit_diff_same_body(self):
        a=base();b=base();b['authorities'][1]['id']='urn:auth:other';b['authorities'][1]['immutable_ref']='doc:other@v1';b['assertions'][0]['authority_refs'][1]='urn:auth:other';q=compare_e1(a,b);self.assertEqual(q['e1'],'E1_EQUAL');self.assertFalse(q['audit_equal'])
    def test_kcl_kvl_distinct(self):
        a=base();b=base();b['predicates'][0]['kind']='KCL';self.assertEqual(compare_e1(a,b)['e1'],'E1_DIFFERENT')
    def test_injection_consumption_distinct(self):
        b=base();b['referents'][0]['quantity']['sign']='CONSUMPTION';self.assertEqual(compare_e1(base(),b)['e1'],'E1_DIFFERENT')
    def test_required_permitted_distinct(self):
        b=base();b['assertions'][0]['modality']='PERMITTED';self.assertEqual(compare_e1(base(),b)['e1'],'E1_DIFFERENT')
    def test_evidence_result_diff(self):
        b=base();b['evidences'][0].update(role='RESULT',status='PASS',run_id='synthetic-run-01');self.assertEqual(compare_e1(base(),b)['e1'],'E1_DIFFERENT')
    def test_h2_mass_to_energy_block(self):
        b=base();b['referents'][0]['quantity'].update(carrier='hydrogen',kind='mass',unit='MWh');self.assertCode(b,'UNIT_OR_CONVERSION_BASIS')
    def test_wrong_carrier_connection(self):
        b=base();b['referents'][1]['quantity'].update(carrier='hydrogen',kind='mass',unit='kg');self.assertCode(b,'PORT_CARRIER_MISMATCH')
    def test_evidence_fake_pass(self):
        b=base();b['evidences'][0]['status']='PASS';self.assertCode(b,'UNSUPPORTED_PASS')
    def test_missing_source(self):
        b=base();b['assertions'][0]['authority_refs']=[];self.assertCode(b,'SOURCE_REQUIRED')
    def test_unknown_reference(self):
        b=base();b['assertions'][0]['predicate_ref']='unresolved';self.assertCode(b,'UNRESOLVED_REFERENCE')
    def test_missing_guard(self):
        b=base();del b['assertions'][0]['guard'];self.assertCode(b,'GUARD_REQUIRED')
    def test_missing_time_duration(self):
        b=base();del b['frame']['time']['duration'];self.assertCode(b,'TIME_INTEGRATION_DURATION_MISSING')
    def test_first_stage_information_leak(self):
        b=base();b['frame']['scenario']={'stage1_decisions':[{'before_revelation':True,'values_by_scenario':{'s1':1,'s2':2}}]};self.assertCode(b,'INFORMATION_LEAKAGE')
    def test_no_forced_soc(self):
        b=base();b['assertions'][0]['internal_variable_required']='SOC';self.assertCode(b,'UNJUSTIFIED_INTERNAL_RESTRICTION')
    def test_ambiguous_id(self):
        b=base();b['referents'][1]['id']=b['referents'][0]['id'];self.assertCode(b,'DUPLICATE_ID')
    def test_reject_unknown_status(self):
        b=base();b['assertions'][0]['decision']='IMPLICIT_DEFAULT';self.assertCode(b,'DECISION')
    def test_prevent_unapproved_imports(self):
        b=base();b['frame']['imports']=['urn:unapproved:module'];self.assertCode(b,'UNAPPROVED_COMPOSITION')
    def test_no_price_basis_default(self):
        b=base();b['observables'][0]['quantity'].update(carrier='currency',kind='cost',unit='EUR');self.assertCode(b,'PRICE_BASIS_MISSING')
    def test_no_mandated_math_formulation(self):
        a=base();b=base();b['variations'][0]['allowed']=['ENERGY_STATE','SOC'];self.assertEqual(compare_e1(a,b)['e1'],'E1_DIFFERENT') # choice-list sorting not assumed
    def test_no_e2_e4_automatic_proof(self):
        q=compare_e1(base(),base());self.assertEqual(q['e4'],'NOT_PROVED');self.assertEqual(q['e2'],'NOT_PROVED')
    def test_no_implicit_evidence_promotion(self):
        a=base(); b,_=normalize(a);self.assertEqual(b['evidences'][0]['role'],'REQUEST')

if __name__=='__main__':unittest.main(verbosity=2)
