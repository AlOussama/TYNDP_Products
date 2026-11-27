"""Bounded numeric test consumer; reuse MS1 arithmetic implementation.
Extensions are only for the finite selected RC projections, not language execution.
"""
from pathlib import Path
import sys
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"canonical_closure"))
sys.path.insert(0,str(ROOT.parent/"BUNDLE_ML_04A_MS1"/"architecture_prototypes"))
from closure import native,bind_data,quantity
from adapter import Consumer,Q,coords
import mathspec.program as mp
class Unsupported(ValueError):pass
def need(x,code):
    if not x:raise Unsupported(code)
def compare(a,b,op):
    need(a.type==b.type,"EVALUATION_TYPE")
    if op in ("==","="):return a.value==b.value
    if op=="!=":return a.value!=b.value
    if op=="<":return a.value<b.value
    if op=="<=":return a.value<=b.value
    if op==">":return a.value>b.value
    if op==">=":return a.value>=b.value
    raise Unsupported("COMPARISON:"+op)
class FiniteNative(Consumer):
    def __init__(self,leaf,data):
        self._initialize(leaf,data,bind_data)
    def _initialize(self,leaf,data,binder):
        self.receipt=binder(leaf,data)
        self.program=native(leaf["native_canonical"]).program
        c=leaf["context"];self.axes={n:z["labels"] for n,z in c["domains"].items()}
        self.declarations={n:{"axes":list(p.dims)} for n,p in self.program.parameters.items()}
        self.data={}
        for n,rows in data["parameters"].items():
            typ=quantity(c["symbols"][n]["quantity"]).atoms.exponents
            self.data[n]={tuple(r["key"]):Q(F(r["value"]),typ) for r in rows}
        self.relations=data["relations"]
    def matches(self,columns,env):
        return [r for r in self.relations[columns.name] if all(r[role]==env[columns.dim(role)] for role in columns.grouped)]
    def at_row(self,operand,columns,env,row):
        updated=dict(env)
        for role in columns.joined:updated[columns.dim(role)]=row[role]
        return self.expr(operand,updated)
    def expr(self,n,env):
        t=type(n)
        if t is mp.Sum and any(a.column is not None for a in n.over):
            j=n.operand;need(type(j) is mp.Join,"GROUP_SUM_PROFILE")
            vals=[self.at_row(j.operand,j.columns,env,r) for r in self.matches(j.columns,env)]
            need(bool(vals),"EMPTY_GROUP")
            z=vals[0]
            for v in vals[1:]:z=z.add(v)
            return z
        if t is mp.Join:
            rr=self.matches(n.columns,env);need(n.columns.one_row_per_group and len(rr)==1,"LOOKUP_CARDINALITY")
            return self.at_row(n.operand,n.columns,env,rr[0])
        if t is mp.Cases:
            active=[r for r in n.regions if self.cond(r.when.root,env)]
            need(len(active)==1,"CASE_TOTALITY")
            return self.expr(active[0].value,env)
        return super().expr(n,env)
    def cond(self,n,env):
        t=type(n)
        if t is mp.BooleanLiteral:return n.value
        if t is mp.ConditionReference:return self.cond(n.body,env)
        if t is mp.And:return self.cond(n.left,env) and self.cond(n.right,env)
        if t is mp.Or:return self.cond(n.left,env) or self.cond(n.right,env)
        if t is mp.Not:return not self.cond(n.operand,env)
        if t is mp.ExpressionComparison:return compare(self.expr(n.left,env),self.expr(n.right,env),n.op)
        if t is mp.ParameterComparison:return compare(self.data[n.name][tuple(env[a] for a in n.dims)],Q(F(n.value)),n.op)
        if t is mp.DimensionComparison:return compare(Q(F(env[n.name])),Q(F(n.value)),n.op)
        if t is mp.DimensionPosition:return compare(Q(F(self.axes[n.name].index(env[n.name]))),Q(F(n.position)),n.op)
        raise Unsupported("FINITE_CONDITION_PROFILE:"+t.__name__)
    def outputs(self):
        return {n:[str(v.value) for v in self.table(n).values()] for n in self.program.expressions}
    def conditions(self):
        return {n:all(self.cond(p.condition.root,e) for e in coords(self.axes,p.dims)) for n,p in self.program.conditions.items()}
