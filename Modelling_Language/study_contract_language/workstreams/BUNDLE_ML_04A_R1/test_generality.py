"""New finite language-chain fragments, not original RC01–10 executions."""
import json, unittest, platform
from make_fixtures import contract, q, domain, quant, var, measure, cmp
from n1r import run, emit_a

def base():
    d=contract();d['relations']=[];d['frame']['method_slots']=[];d['frame']['data_inputs']=[];return d

def port(d,i,carrier,kind,unit,direction):
    a=d['referents'][i];a.update(kind='external_port',type=carrier+'.'+kind,quantity=q(kind=kind,carrier=carrier,unit=unit,sign='INJECTION',basis=''),direction=direction)
    d['observables'][i]['quantity']=a['quantity'].copy()

class Fragments(unittest.TestCase):
    def both(self,d):
        a,b=run(emit_a(d),'A'),run(json.dumps(d),'B');self.assertEqual(a['semantic_digest'],b['semantic_digest']);self.assertEqual(a['audit_digest'],b['audit_digest']);return a
    def rejects(self,d,code):
        for s,t in [('A',emit_a(d)),('B',json.dumps(d))]:
            with self.assertRaisesRegex((ValueError,TypeError,KeyError),code):run(t,s)
    def test_RC01_power_energy_fragment(self):
        d=base()
        for i,direction in enumerate(('OUT','IN')):port(d,i,'electricity','active_power','MW',direction)
        o=d['observables'][0];o['aggregation']='energy_integration';o['projection']={'op':'integrate','expr':o['projection'],'duration_ref':'study:duration'};o['quantity']=q(kind='energy',carrier='electricity',unit='MWh',sign='INJECTION',basis='')
        self.assertEqual(self.both(d)['normalized']['observables'][1]['quantity']['unit'],'MWh');o['quantity']['unit']='MW';self.rejects(d,'QUANTITY')
    def test_RC03_RC04_hydrogen_mass_flow_fragment(self):
        d=base()
        for i,direction in enumerate(('OUT','IN')):port(d,i,'hydrogen','mass_flow','kg/h',direction)
        self.both(d);d['referents'][1]['quantity']['unit']='MWh';self.rejects(d,'QUANTITY')
    def test_RC05_port_connection_fragment(self):
        d=base()
        for i,direction in enumerate(('OUT','IN')):port(d,i,'electricity','active_power','MW',direction)
        d['relations']=[{'id':'relation:link','kind':'connected_to','from':'case:base','to':'case:alt','authority_refs':['source:research']}];self.both(d);d['referents'][1]['direction']='OUT';self.rejects(d,'PORT_COMPATIBILITY')
    def test_RC07_information_fragment(self):
        d=base();p=d['predicates'][0]['expr'];p['body']['body']={'op':'in_information','info':'info:initial','scenario':var('s'),'time':var('t')};self.both(d);d['frame']['information_sets'][0]['partition']=[['s1']];self.rejects(d,'INFORMATION_PARTITION')
    def test_RC10_variation_fragment(self):
        d=base();d['variations']=[{'id':'variation:internal','subject':'case:base','alternatives':['formulation:state','formulation:flow'],'disclosure':True,'source_refs':['source:research']}];self.both(d);d['variations'][0]['disclosure']=False;self.rejects(d,'VARIATION')
if __name__=='__main__':print('Python',platform.python_version(),flush=True);unittest.main(verbosity=2)
