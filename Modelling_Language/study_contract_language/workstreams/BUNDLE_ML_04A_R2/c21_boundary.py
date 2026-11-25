"""N10 finite canonical-boundary experiment, NOT a full C20/R1 language chain.
No caller-supplied method extension; no replacement of the pinned C21 code.
"""
import hashlib
import importlib.util
from pathlib import Path

PIN = 'b59c7f1c4570df2ac3141fb75a1c0d3432d8259ffa3ebee142a2470988f4adc1'
ROOT = Path(__file__).resolve().parent
C21_PATH = ROOT.parent/'BUNDLE_ML_04A_R1'/'pinned'/'csnf_validator.py'
if not C21_PATH.is_file(): C21_PATH = ROOT/'pinned'/'csnf_validator.py'

def require(ok, diagnostic):
    if not ok: raise ValueError(diagnostic)

def load_c21():
    require(hashlib.sha256(C21_PATH.read_bytes()).hexdigest() == PIN, 'C21_PIN_MISMATCH')
    spec = importlib.util.spec_from_file_location('r2_pinned_c21', C21_PATH)
    c21 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c21)
    return c21

# Exactly the existing R1 predicate operator set, not a proposed new core.
SIGNATURES = {
    'bool3': ('value',), 'var': ('name',), 'forall': ('var','domain','body'),
    'exists': ('var','domain','body'), 'and': ('args',), 'or': ('args',),
    'not': ('args',), 'measure': ('ref','indices'), 'literal': ('quantity',),
    'integrate': ('expr','duration_ref'), 'compare': ('cmp','lhs','rhs'),
    'in_information': ('info','scenario','time')
}

def inspect_expr(e, bound=frozenset()):
    require(type(e) is dict and type(e.get('op')) is str, 'AST_SHAPE')
    op = e['op']
    require(op in SIGNATURES, 'UNKNOWN_OPERATOR:'+op)
    require(set(e) == {'op',*SIGNATURES[op]}, 'AST_FIELDS:'+op)
    if op == 'bool3': require(e['value'] in ('TRUE','FALSE','UNKNOWN'), 'BOOL3')
    elif op == 'var': require(type(e['name']) is str and e['name'] in bound, 'UNBOUND_VARIABLE')
    elif op in ('forall','exists'):
        require(type(e['var']) is str and e['var'] and e['var'] not in bound, 'BINDER')
        require(type(e['domain']) is dict and set(e['domain']) == {'kind','ref'}, 'DOMAIN_SHAPE')
        inspect_expr(e['body'], bound | {e['var']})
    elif op in ('and','or','not'):
        a=e['args']; require(type(a) is list and (len(a)==1 if op=='not' else len(a)>=2), 'BOOL_ARITY')
        for item in a: inspect_expr(item,bound)
    elif op == 'measure':
        require(type(e['ref']) is str and type(e['indices']) is list, 'MEASURE_SHAPE')
        for item in e['indices']: inspect_expr(item,bound)
    elif op == 'literal': require(type(e['quantity']) is dict, 'QUANTITY_SHAPE')
    elif op == 'integrate': inspect_expr(e['expr'],bound)
    elif op == 'compare':
        require(e['cmp'] in ('eq','le','ge','lt','gt'), 'COMPARE_OPERATOR')
        inspect_expr(e['lhs'],bound); inspect_expr(e['rhs'],bound)
    elif op == 'in_information':
        inspect_expr(e['scenario'],bound); inspect_expr(e['time'],bound)

FRAME_FIELDS={'id','schema','ruleset','registry','question','time','domains','scopes','guards','information_sets','data_inputs','method_slots'}

def normalize_boundary(graph):
    """Fail closed on extension, operator shape and lexical binding; C21 still native.
    Input is a canonical graph, not source syntax. Full type/scope/profile checking
    remains the obligation of the original R1 front end and future integrated R2.
    """
    c21=load_c21()
    require(type(graph) is dict and set(graph)=={'frame',*c21.COLLECTIONS}, 'GRAPH_FIELDS')
    f=graph['frame']; require(type(f) is dict and set(f)<=FRAME_FIELDS, 'UNVALIDATED_FRAME_EXTENSION')
    for p in graph['predicates']: inspect_expr(p['expr'])
    for g in f.get('guards',[]): inspect_expr(g['expr'])
    for o in graph['observables']:
        bindings=o.get('bindings',[])
        names=[b['var'] for b in bindings]
        require(len(names)==len(set(names)), 'DUPLICATE_OBSERVABLE_BINDER')
        inspect_expr(o['projection'],frozenset(names))
    normal,report=c21.normalize(graph)
    require(c21.normalize(normal)[0]==normal, 'NON_IDEMPOTENT')
    return normal,report
