"""New R1 finite tests; original RC/mutation IDs are not claimed executed."""
import copy,json,unittest,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
from research_chain import *
P=Path(__file__).parent
A=(P/'contract.a').read_text();B=(P/'contract.b.json').read_text()
def obj(n):return read((P/n).read_text())
D=obj('data.json'); M=obj('method-undiscounted.json');S=obj('study-undiscounted.json')
def bound(m=M,d=D,s=S,src=B,syntax='B'):
    s=copy.deepcopy(s);s.update(method_hash=digest(m),data_hash=digest(d),contract_semantic=chain(src,syntax)[0]['semantic_digest']);return run(src,syntax,s,m,d)
def modify(x,fn):x=copy.deepcopy(x);fn(x);return x
class R1(unittest.TestCase):
    def test_01_original_blob(self):
        b=(P/'csnf_validator.py').read_bytes();self.assertEqual(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),'5201bda3c0a611d27e2bc335bbfebc191f252ec7')
    def test_02_dual_syntax(self):
        a,b=chain(A,'A')[0],chain(B,'B')[0];self.assertEqual(a['graph'],b['graph']);self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertNotEqual(a['source_sha256'],b['source_sha256']);self.assertNotEqual(a['audit_digest'],b['audit_digest'])
    def test_03_idempotence(self):
        x=chain(B,'B')[0];self.assertEqual(chain(enc(x['graph']),'B')[0]['graph'],x['graph']);self.assertEqual(c21.normalize(x['legacy'])[0],x['legacy'])
    def test_04_full_finite_swap(self):
        # Independent hand-derived oracle: expected deltas 27.5 and 55; year-end r=10%.
        expected={'undiscounted':F(55,2)+55,'discounted':F(55,2)/F(11,10)+F(55)/F(121,100)};out=[]
        for syn,src in [('A',A),('B',B)]:
            for variant,y in expected.items():
                r=run(src,syn,obj('study-'+variant+'.json'),obj('method-'+variant+'.json'),D);a=r['audit'];self.assertEqual(F(a['outputs']['rule:result']),y);self.assertEqual(a['finite_assertion_checks']['assert:bounds'],'FINITE_TRUE');self.assertEqual(a['status'],'OWNER_TBD');self.assertEqual(r['graph']['evidences'][0]['status'],'NOT_EXECUTED');out.append(r)
        self.assertEqual(len({enc(x['audit']['code_hashes']) for x in out}),1);self.assertEqual(len({x['audit']['data_hash'] for x in out}),1);self.assertEqual(len({x['audit_digest'] for x in out}),4);self.assertEqual(len({x['audit']['method_hash'] for x in out}),2)
    def test_05_unbound_A(self):
        with self.assertRaisesRegex(Reject,'UNBOUND_VARIABLE'):chain(A.replace('var("t")','var("u")'),'A')
    def test_06_unknown_operator_A(self):
        with self.assertRaisesRegex(Reject,'UNKNOWN_OPERATOR'):chain(A.replace('le(at','invented(at'),'A')
    def test_07_invalid_guard_A(self):
        with self.assertRaisesRegex(Reject,'GUARD_REF'):chain(A.replace('flag("flag:applicable")','flag("flag:missing")'),'A')
    def test_08_wrong_axis_A(self):
        with self.assertRaisesRegex(Reject,'INDEX_TYPE'):chain(A.replace('var("t")','var("s")'),'A')
    def test_09_scope_A(self):
        with self.assertRaisesRegex(Reject,'OUTER_SCOPE'):chain(A.replace('scope "axis:t"','scope "axis:s"'),'A')
    def test_10_authority_A(self):
        with self.assertRaisesRegex(Reject,'AUTHORITY_CONFLICT'):chain(A.replace('decision OWNER_TBD','decision APPROVED'),'A')
    def test_11_evidence_A(self):
        with self.assertRaisesRegex(Reject,'EVIDENCE_PROMOTION'):chain(A.replace('status: NOT_EXECUTED','status: PASS'),'A')
    def test_12_duplicate_B(self):
        with self.assertRaisesRegex(Reject,'DUPLICATE_KEY'):chain(B.replace('"frame": {','"frame": {}, "frame": {'),'B')
    def test_13_unknown_operator_B(self):
        with self.assertRaisesRegex(Reject,'UNKNOWN_OPERATOR'):chain(B.replace('"op": "le"','"op": "invented"'),'B')
    def test_14_guard_B(self):
        with self.assertRaisesRegex(Reject,'GUARD_REF'):chain(B.replace('"args": [\n          "flag:applicable"','"args": [\n          "flag:missing"'),'B')
    def test_15_incompatible_type(self):
        d=read(B);d['referents'][0]['quantity']['basis']='EUR:real:2025';
        with self.assertRaises(Reject):chain(enc(d),'B')
    def test_16_data_hash(self):
        d=modify(D,lambda x:x['context'].update(demand='changed'))
        with self.assertRaisesRegex(Reject,'HASH_OR_VERSION'):run(B,'B',S,M,d)
    def test_17_method_hash(self):
        m=modify(M,lambda x:x.update(version='2'))
        with self.assertRaisesRegex(Reject,'HASH_OR_VERSION'):run(B,'B',S,m,D)
    def test_18_exogeneity(self):
        d=modify(D,lambda x:x['cases'].update({'case:alt':'changed'}))
        with self.assertRaisesRegex(Reject,'EXOGENEITY_HASH'):bound(d=d)
    def test_19_unknown_observable(self):
        m=modify(M,lambda x:x['rules'][0].update(expr=call('at','obs:unknown')))
        with self.assertRaisesRegex(Reject,'OBSERVABLE_REF'):bound(m=m)
    def test_20_unknown_operator_profile(self):
        m=modify(M,lambda x:x['rules'][0].update(expr=call('eval','arbitrary')))
        with self.assertRaisesRegex(Reject,'UNKNOWN_OPERATOR'):bound(m=m)
    def test_21_duplicate_contribution(self):
        m=modify(M,lambda x:x['ledger'].append(copy.deepcopy(x['ledger'][0])))
        with self.assertRaisesRegex(Reject,'DUPLICATE_CONTRIBUTION'):bound(m=m)
    def test_22_overlap(self):
        m=modify(M,lambda x:x['ledger'].append({'id':'contribution:other','atoms':['impact:operating-cost']}))
        with self.assertRaisesRegex(Reject,'OVERLAP'):bound(m=m)
    def test_23_missing_contribution(self):
        m=modify(M,lambda x:x['ledger'].clear())
        with self.assertRaisesRegex(Reject,'INCOMPLETE_LEDGER'):bound(m=m)
    def test_24_unknown_not_zero(self):
        d=modify(D,lambda x:x['observations']['obs:alt'][0].update(value='UNKNOWN'))
        with self.assertRaisesRegex(Reject,'UNKNOWN_ARITHMETIC'):bound(d=d)
    def test_25_unknown_guard(self):
        d=modify(D,lambda x:x['flags'].update({'flag:applicable':'UNKNOWN'}));self.assertEqual(bound(d=d)['audit']['finite_assertion_checks']['assert:bounds'],'BLOCKED_UNKNOWN_GUARD')
    def test_26_false_guard(self):
        d=modify(D,lambda x:x['flags'].update({'flag:applicable':False}));self.assertEqual(bound(d=d)['audit']['finite_assertion_checks']['assert:bounds'],'NOT_APPLICABLE')
    def test_27_weight_probability(self):
        d=modify(D,lambda x:x['weights']['w:p'].update(low='1'))
        with self.assertRaisesRegex(Reject,'WEIGHT_VALUES'):bound(d=d)
    def test_28_parameter_range(self):
        s=modify(S,lambda x:x['parameters'].update(rate='2'))
        with self.assertRaisesRegex(Reject,'PARAM_RANGE'):bound(s=s)
    def test_29_rule_cycle(self):
        m=modify(M,lambda x:x['rules'][0].update(expr=call('rule','rule:result')))
        with self.assertRaisesRegex(Reject,'RULE_REF'):bound(m=m)
    def test_30_authority_promotion(self):
        m=modify(M,lambda x:x.update(authority='APPROVED'))
        with self.assertRaisesRegex(Reject,'AUTHORITY_PROMOTION'):bound(m=m)
    def test_31_capability_order(self):
        d=read(B);d['frame']['domains'][0]['kind']='request';d['frame']['domains'][1]['kind']='response';d['frame']['weights']=[];d['assertions'][0]['semantic_role']='CAPABILITY_GUARANTEE';d['predicates'][0]['expr']['args'][2]['op']='exists';chain(enc(d),'B');d['predicates'][0]['expr']['args'][2]['op']='forall'
        with self.assertRaisesRegex(Reject,'CAPABILITY_ORDER'):chain(enc(d),'B')
    def test_32_capability_counterexample(self):
        ctx={'domains':{'d:r':{'members':['r1','r2']},'d:a':{'members':['r1','r2']}}};values={};e=call('forall','r','d:r',call('exists','a','d:a',call('eq',call('var','r'),call('var','a'))));self.assertTrue(evaluate(e,ctx,{},values,{},{},{},{}));e=call('exists','a','d:a',call('forall','r','d:r',call('eq',call('var','r'),call('var','a'))));self.assertFalse(evaluate(e,ctx,{},values,{},{},{},{}))
        # This control is untyped: cross-domain index equality is intentionally not permitted by infer.
    def test_33_sampled_negative(self):
        d=modify(D,lambda x:x['observations']['obs:alt'][0].update(value='101'));self.assertEqual(bound(d=d)['audit']['finite_assertion_checks']['assert:bounds'],'FINITE_FALSE')
    def test_34_guard_projection_loss(self):
        # Known defect demonstration, not closure: C21 projection stores placeholder.
        r=chain(B,'B')[0];self.assertNotEqual(r['legacy']['assertions'][0]['guard'],r['graph']['assertions'][0]['guard'])
    def test_35_currency_basis(self):
        d=read(B);d['referents'][0]['quantity']['basis']='USD:real:2024'
        with self.assertRaisesRegex(Reject,'BASIS'):chain(enc(d),'B')
if __name__=='__main__':unittest.main(verbosity=2)
