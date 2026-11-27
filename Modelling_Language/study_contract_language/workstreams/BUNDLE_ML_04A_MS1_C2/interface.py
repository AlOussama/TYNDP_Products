"""C2 shared outer interface. No math parser or AST."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/"BUNDLE_ML_04A_MS1_C1"/"canonical_closure"))
from package_interface import predicate_client,method_client,import_package
from closure import need,fields
def resolve_predicate(package,ref):
    fields(ref,("predicate_id","role","axes","scope_id"),"C2_PREDICATE_FIELDS")
    p=predicate_client(package,ref["predicate_id"],ref["role"])
    need(type(ref["axes"]) is list and p["qualified_axes"]==ref["axes"],"C2_AXIS_ALIGNMENT")
    need(p["scope_id"]==ref["scope_id"],"C2_SCOPE_ALIGNMENT")
    return p
def resolve_method(package,data):
    return method_client(package,data)
