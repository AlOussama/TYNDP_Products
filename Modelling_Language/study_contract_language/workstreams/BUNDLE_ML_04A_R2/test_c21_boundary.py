import copy, unittest, hashlib, platform
from c21_boundary import load_c21, normalize_boundary, C21_PATH, PIN

class Boundary(unittest.TestCase):
    def setUp(self):
        self.c=load_c21(); c=self.c
        self.g={k:[] for k in c.COLLECTIONS}
        self.g['frame']={'id':'urn:r2:boundary','schema':c.VERSION,'ruleset':c.RULES,'registry':c.REGISTRY}
        self.g['predicates']=[{'id':'urn:r2:p','expr':{'op':'bool3','value':'TRUE'}}]
    def test_native_pin_and_baseline(self):
        n,r=normalize_boundary(self.g)
        self.assertEqual(n,self.g); self.assertEqual(r['phase'],'P0_P6_PARTIAL')
        self.assertEqual(hashlib.sha256(C21_PATH.read_bytes()).hexdigest(),PIN)
    def test_original_unknown_operator_defect(self):
        self.g['predicates'][0]['expr']={'op':'invented'}
        n,_=self.c.normalize(self.g)
        self.assertEqual(n['predicates'][0]['expr'],{'op':'invented'})
        with self.assertRaisesRegex(ValueError,'UNKNOWN_OPERATOR:invented'): normalize_boundary(self.g)
    def test_nested_unknown_operator(self):
        self.g['predicates'][0]['expr']={'op':'not','args':[{'op':'invented'}]}
        with self.assertRaisesRegex(ValueError,'UNKNOWN_OPERATOR:invented'): normalize_boundary(self.g)
    def test_arbitrary_extension_rejected(self):
        self.g['frame']['resolved_profile']={'rules':{'x':{'op':'invented'}}}
        self.c.normalize(self.g)
        with self.assertRaisesRegex(ValueError,'UNVALIDATED_FRAME_EXTENSION'): normalize_boundary(self.g)
    def test_unbound_guard_variable(self):
        self.g['frame']['guards']=[{'id':'urn:r2:g','expr':{'op':'var','name':'unbound'}}]
        with self.assertRaisesRegex(ValueError,'UNBOUND_VARIABLE'): normalize_boundary(self.g)
    def test_existing_bool3_unknown_retained(self):
        self.g['predicates'][0]['expr']['value']='UNKNOWN'
        self.assertEqual(normalize_boundary(self.g)[0]['predicates'][0]['expr']['value'],'UNKNOWN')
    def test_unknown_field_rejected(self):
        self.g['predicates'][0]['expr']['method_override']='unchecked'
        with self.assertRaisesRegex(ValueError,'AST_FIELDS'): normalize_boundary(self.g)
if __name__=='__main__':
    print('Python',platform.python_version(), 'C21 SHA256',PIN,flush=True)
    unittest.main(verbosity=2)
