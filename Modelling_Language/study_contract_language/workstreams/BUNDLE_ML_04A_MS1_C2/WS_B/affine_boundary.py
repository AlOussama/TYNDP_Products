"""Versioned proof of positive native expressions for original R1 discount profiles.
No general symbolic prover; all nodes still undergo the inherited type/domain checks."""
import mathspec.program as mp
from closure import _admit,constant,need
from WS_B import power_boundary as old
VERSION="canonical-first-research-0.4"
PACKAGE="canonical-mathematical-contract-package-0.3"
class AffinePowerChecked(old.PowerChecked):
    def nonnegative(self,e):
        v=constant(e)
        if v is not None:return v>=0
        if type(e) is mp.ParameterReference:return self.c["symbols"][e.name]["domain_rule"] in ("POSITIVE","NONNEGATIVE")
        if type(e) is mp.ExpressionReference:return self.nonnegative(e.body)
        if type(e) is mp.Add:return self.nonnegative(e.left) and self.nonnegative(e.right)
        if type(e) is mp.Multiply:return self.nonnegative(e.left) and self.nonnegative(e.right)
        return self.base_positive(e)
    def base_positive(self,e):
        if super().base_positive(e):return True
        if type(e) is mp.ExpressionReference:return self.base_positive(e.body)
        if type(e) is mp.Add:
            return (self.base_positive(e.left) and self.nonnegative(e.right)) or (self.nonnegative(e.left) and self.base_positive(e.right))
        if type(e) is mp.Multiply:return self.base_positive(e.left) and self.base_positive(e.right)
        if type(e) is mp.Power:return self.base_positive(e.base)  # integer and bound checked by expr before use
        return False
    def expr(self,e,opened=False):
        if type(e) is mp.Divide:
            a,b=self.expr(e.numerator),self.expr(e.divisor);v=constant(e.divisor)
            if (v is not None and v!=0) or (type(e.divisor) is mp.ParameterReference and self.c["symbols"][e.divisor.name]["domain_rule"] in ("NONZERO","POSITIVE")) or self.base_positive(e.divisor):
                return self.combine(a,b,-1)
            need(False,"DIVISOR_NONZERO_REQUIRED")
        return super().expr(e,opened)
def admit(source,context,require_canonical=False):return _admit(source,context,require_canonical,AffinePowerChecked,VERSION)
def reimport(leaf):return old._reimport(leaf,admit,VERSION)
def bind_data(leaf,data):return old._bind_power_data(leaf,data,reimport)
def export_package(leaf):return old._export_package(leaf,reimport,PACKAGE,VERSION)
def import_package(text):return old._import_package(text,admit,export_package,PACKAGE)
def method_client(package,data):return old._method_client(package,data,import_package,bind_data)
class FinitePowerNative(old.FiniteNative):
    def __init__(self,leaf,data):self._initialize(leaf,data,bind_data)
