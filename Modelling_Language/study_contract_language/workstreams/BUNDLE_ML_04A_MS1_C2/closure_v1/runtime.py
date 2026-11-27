"""Finite public-Program consumer, extending C1's checked exact consumer.
Native mathspec remains the only mathematical syntax and normal form.
"""
from fractions import Fraction as F
import mathspec.program as mp
from native_consumer import FiniteNative, Q, compare, coords
from closure import need, native, Checked
from interface import import_package, package_version, _api, V1, V2

class CompleteFinite(FiniteNative):
    def __init__(self,leaf,data,binder,checker):
        self._initialize(leaf,data,binder)
        self.checker=checker
    def neighbors(self,n,env):
        axis=n.along; labels=self.axes[axis]; i=labels.index(env[axis])
        need(n.partition is None,"PARTITIONED_TEMPORAL_NOT_ADMITTED")
        if type(n) is mp.Translate:
            need(type(n.offset) is int and n.offset>=0,"SHIFT_SCOPE")
            j=i-n.offset
            if n.wrap:return [{**env,axis:labels[j%len(labels)]}]
            return [{**env,axis:labels[j]}] if j>=0 else []
        need(type(n.width) is int and 1<=n.width<=len(labels),"WINDOW_SCOPE")
        return [{**env,axis:labels[j%len(labels)]} for j in range(i-n.width+1,i+1) if n.wrap or j>=0]
    def expr(self,n,env):
        if type(n) in (mp.Translate,mp.WindowSum):
            points=self.neighbors(n,env)
            if not points:
                need(type(n) is mp.Translate and n.fill==0,"SHIFT_EDGE")
                # Static physical type, not evaluation of an inactive coordinate.
                typ=self.checker.expr(n.operand).atoms.exponents
                return Q(F(0),typ)
            vals=[self.expr(n.operand,p) for p in points]
            value=vals[0]
            for v in vals[1:]:value=value.add(v)
            return value
        return super().expr(n,env)
    def cond(self,n,env):
        t=type(n)
        if t is mp.ParameterDefined:
            # Native definedness is presence, NOT boolean value. Full support
            # is checked by admission: a present False is still defined.
            need(self.program.parameters[n.name].dtype=="bool","DEFINED_IS_NOT_TRUTH")
            return tuple(env[a] for a in n.dims) in self.data[n.name]
        if t is mp.JoinedCondition:
            rows=self.matches(n.columns,env)
            need(n.columns.one_row_per_group and len(rows)==1,"LOOKUP_CARDINALITY")
            updated=dict(env)
            for role in n.columns.joined:updated[n.columns.dim(role)]=rows[0][role]
            return self.cond(n.operand.root,updated)
        if t is mp.CountComparison:
            count=sum(self.cond(n.condition.root,{**env,n.over:x}) for x in self.axes[n.over])
            return compare(Q(F(count)),Q(F(n.value)),n.op)
        # Evaluate both branches, so unsupported admitted execution never
        # hides behind short circuit. Native conditions have binary semantics.
        if t in (mp.And,mp.Or):
            a,b=self.cond(n.left,env),self.cond(n.right,env)
            return (a and b) if t is mp.And else (a or b)
        return super().cond(n,env)

def consumer(package,data):
    leaf=import_package(package);api=_api(package);version=package_version(package)
    checker=Checked if version==V1 else api.PowerChecked if version==V2 else api.AffinePowerChecked
    checked=checker(native(leaf["native_canonical"]),leaf["context"])
    return CompleteFinite(leaf,data,api.bind_data,checked)
