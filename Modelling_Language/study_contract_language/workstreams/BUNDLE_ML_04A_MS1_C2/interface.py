"""C2 shared outer interface; explicit dispatch of admitted versions, no raw AST."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/"BUNDLE_ML_04A_MS1_C1"/"canonical_closure"))
sys.path.insert(0,str(ROOT.parent/"BUNDLE_ML_04A_MS1_C1"/"comparative_canonical"))
import package_interface as old
from closure import need,fields,c1
V1="canonical-mathematical-contract-package-0.1"
V2="canonical-mathematical-contract-package-0.2"
def package_version(package):
    obj=c1.parse(package)
    need(type(obj) is dict and obj.get("schema") in (V1,V2),"PACKAGE_VERSION")
    return obj["schema"]
def _power():
    from WS_B import power_boundary
    return power_boundary
def import_package(package):
    return _power().import_package(package) if package_version(package)==V2 else old.import_package(package)
def predicate_client(package,predicate_id,expected_role):
    return old._predicate_from_leaf(import_package(package),predicate_id,expected_role)
def resolve_predicate(package,ref):
    fields(ref,("predicate_id","role","axes","scope_id"),"C2_PREDICATE_FIELDS")
    p=predicate_client(package,ref["predicate_id"],ref["role"])
    need(type(ref["axes"]) is list and p["qualified_axes"]==ref["axes"],"C2_AXIS_ALIGNMENT")
    need(p["scope_id"]==ref["scope_id"],"C2_SCOPE_ALIGNMENT")
    return p
def resolve_method(package,data):
    return _power().method_client(package,data) if package_version(package)==V2 else old.method_client(package,data)
def finite_consumer(package,data):
    leaf=import_package(package)
    if package_version(package)==V2:return _power().FinitePowerNative(leaf,data)
    from native_consumer import FiniteNative
    return FiniteNative(leaf,data)
