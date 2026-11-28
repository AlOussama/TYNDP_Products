"""Versioned lossless structural A/B boundary over the unchanged M3 definition.
Only metadata/structure is parsed here. Native packages remain opaque strings
and are admitted by the unchanged C2/native mathspec boundary.
"""
import json,re,sys
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"BUNDLE_ML_04A_MS1_C2"))
# Initialize the existing C2 interface explicitly, without test-module side effects.
import interface as _native_interface
from closure_v1 import r1_reuse
from n1r import old, pins as r1_pins
SCHEMA="c3-authoring-0.1"

class AuthoringError(ValueError):
    pass

def require(test,code):
    if not test: raise AuthoringError(code)

def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,"DUPLICATE_KEY:"+k)
        d[k]=v
    return d

def no_float(value):
    raise AuthoringError("EXACT_NUMBER_STRING_REQUIRED:"+value)

class AParser(old.Parser):
    """Reuse R1 lexer/list/string machinery, not its mathematical AST."""
    def block(self):
        self.pop("{");items=[]
        while self.peek()!="}":
            k=self.string() if (self.peek() or "").startswith('"') else self.word()
            self.pop(":");items.append((k,self.value()));self.pop(";")
        self.pop("}")
        return pairs(items)

    def value(self):
        t=self.peek()
        if t=="{": return self.block()
        if t=="[": return self.many("[","]",self.value)
        if (t or "").startswith('"'): return self.string()
        t=self.pop()
        if t in ("true","false"): return t=="true"
        if t=="null": return None
        if re.fullmatch(r"-?(0|[1-9][0-9]*)",t): return int(t)
        raise AuthoringError("UNSUPPORTED_STRUCTURAL_VALUE:"+t)

    def parse(self):
        self.pop("study_contract");version=self.string()
        self.pop("{");self.pop("definition");d=self.block()
        self.pop("instance");i=self.block();self.pop("}")
        require(self.peek() is None,"TRAILING_SOURCE")
        return {"schema":version,"definition":d,"instance":i}

def decode(raw,syntax):
    require(type(raw) is bytes,"RAW_SOURCE_BYTES_REQUIRED")
    try:
        s=raw.decode("utf-8")
        if syntax=="A":
            r1_pins()
            x=AParser(s).parse()
        elif syntax=="B":
            x=json.loads(s,object_pairs_hook=pairs,parse_float=no_float,parse_constant=no_float)
        else:
            raise AuthoringError("UNKNOWN_SYNTAX")
    except (old.Reject,UnicodeError,json.JSONDecodeError) as e:
        raise AuthoringError(str(e)) from e
    require(type(x) is dict and set(x)=={"schema","definition","instance"} and x["schema"]==SCHEMA,"AUTHORING_ENVELOPE")
    require(type(x["definition"]) is dict and type(x["instance"]) is dict,"DEFINITION_INSTANCE_REQUIRED")
    return x

def emit_value(x):
    if type(x) is dict:
        return "{ "+" ".join(json.dumps(k,ensure_ascii=False)+": "+emit_value(v)+";" for k,v in x.items())+" }"
    if type(x) is list: return "["+", ".join(emit_value(v) for v in x)+"]"
    require(type(x) in (str,int,bool,type(None)),"EXACT_STRUCTURAL_VALUE_REQUIRED")
    return json.dumps(x,ensure_ascii=False)

def emit_control(d,i,syntax):
    """For roundtrip controls only, not evidence of independent original authoring."""
    if syntax=="A": return ("study_contract "+json.dumps(SCHEMA)+" {\n definition "+emit_value(d)+"\n instance "+emit_value(i)+"\n}\n").encode()
    require(syntax=="B","UNKNOWN_SYNTAX")
    return (json.dumps({"schema":SCHEMA,"definition":d,"instance":i},ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()

def evaluate(raw,syntax,source_pin,definition_pin,instance_pin):
    """Source hash and object roots are caller-supplied; do not self-authorize."""
    from closure import digest
    from closure_v1 import definition,diagnostics
    actual=sha256(raw).hexdigest()
    info={"schema":"c3-path-receipt-0.1","syntax":syntax,"source_sha256":actual,
          "source_pin":source_pin,"definition_pin":definition_pin,"instance_pin":instance_pin,
          "owner":"OWNER_TBD","general_conformance":"NOT_PROVED"}
    try:
        require(actual==source_pin,"SOURCE_PIN_MISMATCH")
        x=decode(raw,syntax)
        d,i=x["definition"],x["instance"]
        require(digest(d)==definition_pin,"DEFINITION_PIN_MISMATCH")
        require(digest(i)==instance_pin,"INSTANCE_PIN_MISMATCH")
        result=diagnostics.candidate_receipt(definition.instantiate,d,definition_pin,i,instance_pin)
        if result["status"]!="RETURNED":
            return {**info,**result,"stage":"C2_NATIVE_DEFINITION_INSTANCE"}
        receipt=result["result"]
        package=definition.export(d,definition_pin,i,instance_pin)
        reread=definition.reimport(package,definition_pin,instance_pin)
        if reread["receipt"]!=receipt: raise RuntimeError("ROUNDTRIP_RECEIPT_DRIFT")
        package_hash=sha256(package.encode("utf-8")).hexdigest()
        graph=receipt.get("graph",{})
        audit=digest({"source_sha256":actual,"syntax":syntax,"definition_pin":definition_pin,
                      "instance_pin":instance_pin,"package_sha256":package_hash})
        return {**info,"status":"RETURNED","stage":"NATIVE_ADMISSION_BINDING_NORMALIZATION_ROUNDTRIP",
                "result":receipt,"diagnostics":[],"package_sha256":package_hash,
                "semantic_identity":receipt["definition"]["semantic_identity"],
                "graph_semantic_identity":graph.get("semantic_identity"),
                "graph_audit_identity":graph.get("audit_identity"),"representation_audit_identity":audit}
    except AuthoringError as e:
        # This is an actual source/envelope rejection, not a candidate leaf
        # diagnostic or an original expected code. No fabricated source spans.
        return {**info,"status":"REJECTED_SOURCE","stage":"AUTHORING","reason":str(e),"diagnostics":[]}
    except diagnostics.DiagnosticReject as e:
        return {**info,"status":e.record["status"],"stage":"C2_NATIVE_ROUNDTRIP","diagnostics":[e.record]}
    except Exception as e:
        return {**info,"status":"BLOCKED_INTERNAL","stage":"INTERNAL",
                "error_type":type(e).__name__,"reason":str(e),"diagnostics":[]}
