"""General qualified metadata. Reuse R1 structural validation and C1 quantity algebra.
The metadata contains references only, never mathematical expressions.
"""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from closure import need,fields,quantity,qualified,exact,digest,Reject
from closure_v1 import r1_reuse as r1

KINDS=("time","scenario","trace","request","response","component","port","sample","space","event","stage")
COLLECTIONS=("domains","scopes","components","ports","referents","observables","inputs","outputs","relations","authorities","variations","chronologies","information_sets","slots","processes")
def index(rows):
    # The original R1 table validates uniqueness and identifier grammar.
    try:return r1.table(rows)
    except (ValueError,TypeError,KeyError) as e:raise Reject(str(e)) from e
def string(x):return type(x) is str and bool(x)
def members(xs):
    need(type(xs) is list and bool(xs) and all(type(x) in (str,int) and (type(x) is int or bool(x)) for x in xs),"DOMAIN")
    need(len({type(x) for x in xs})==1 and len(xs)==len(set(xs)),"DOMAIN")
    return xs
def refs(xs,table,code,nonempty=True):
    need(type(xs) is list and (not nonempty or bool(xs)) and all(type(x) is str and x in table for x in xs) and len(xs)==len(set(xs)),code)
    return xs
def qcompat(a,b,port=False):
    x,y=quantity(a),quantity(b)
    if port:
        # Direction describes the endpoint, not the carrier measure.
        return x.physical==y.physical and x.atoms==y.atoms and a["sign"]==b["sign"] and a["time_basis"]==b["time_basis"]
    return x==y
def legacy_quantity(q):
    # Actual R1/C21 quantity validation for the exact representable subset.
    k={("electricity","MW"):"active_power",("electricity","MWh"):"energy",("hydrogen","kg/h"):"mass_flow",("hydrogen","kg"):"mass",("currency","EUR"):"cost"}.get((q["carrier"],q["unit"]))
    if k is None:return
    old={"carrier":q["carrier"],"kind":k,"unit":q["unit"],"value":"0","sign":q["sign"]}
    if q["basis"]!="NONE":old["basis"]=q["basis"]
    try:r1.old_quantity(old)
    except ValueError as e:raise Reject(str(e)) from e
def validate(frame):
    fields(frame,("schema","id","version","question",*COLLECTIONS),"FRAME_FIELDS")
    need(frame["schema"]=="c2-study-frame-0.1" and qualified(frame["id"]) and string(frame["version"]) and string(frame["question"]),"FRAME_IDENTITY")
    tables={k:index(frame[k]) for k in COLLECTIONS}
    allids=[frame["id"]]+[i for t in tables.values() for i in t]
    need(all(qualified(i) for i in allids) and len(allids)==len(set(allids)),"DUPLICATE_ID")
    dom=tables["domains"];auth=tables["authorities"];components=tables["components"]
    ports=tables["ports"];referents=tables["referents"];obs=tables["observables"];inputs=tables["inputs"];outputs=tables["outputs"]
    subjects={**components,**ports,**referents}
    def authorities(xs):refs(xs,auth,"AUTHORITY_REQUIRED")
    def axes(xs):refs(xs,dom,"AXIS",False)
    def typed(q):
        quantity(q);legacy_quantity(q)
    for a in auth.values():
        fields(a,("id","role","immutable_ref","revision","decision_state"),"AUTHORITY_FIELDS")
        need(a["role"] in ("SOURCE","OWNER","DECISION","PROVENANCE") and string(a["immutable_ref"]) and string(a["revision"]) and a["decision_state"] in ("OWNER_TBD","PROPOSED","UNKNOWN"),"AUTHORITY_PROMOTION")
    for a in dom.values():
        fields(a,("id","kind","members","ordered"),"DOMAIN_FIELDS")
        need(a["kind"] in KINDS and type(a["ordered"]) is bool,"DOMAIN_KIND")
        members(a["members"])
        if a["kind"] in ("time","stage"):need(a["ordered"],"CHRONOLOGY_ORDER")
        if a["kind"] in ("component","port"):
            refs(a["members"],components if a["kind"]=="component" else ports,"DOMAIN_MEMBER_KIND")
    for a in tables["scopes"].values():
        fields(a,("id","domains","subjects"),"SCOPE_FIELDS");axes(a["domains"]);refs(a["subjects"],subjects,"SCOPE_SUBJECT",False)
    for a in components.values():
        fields(a,("id","kind","authority_refs"),"COMPONENT_FIELDS")
        need(string(a["kind"]),"COMPONENT_KIND");authorities(a["authority_refs"])
    for a in ports.values():
        fields(a,("id","component_ref","direction","quantity","axes","authority_refs"),"PORT_FIELDS")
        need(a["component_ref"] in components,"COMPONENT_REF");need(a["direction"] in ("IN","OUT","BIDIRECTIONAL"),"PORT_DIRECTION")
        typed(a["quantity"]);need(a["quantity"]["direction"] in ("NONE",a["direction"]),"PORT_DIRECTION")
        axes(a["axes"]);authorities(a["authority_refs"])
    for a in referents.values():
        fields(a,("id","kind","quantity","axes","authority_refs"),"REFERENT_FIELDS")
        need(string(a["kind"]),"REFERENT_TYPE");typed(a["quantity"]);axes(a["axes"]);authorities(a["authority_refs"])
    for a in obs.values():
        fields(a,("id","subject","quantity","axes","projection","authority_refs"),"OBSERVABLE_FIELDS")
        need(a["subject"] in {**ports,**referents},"OBSERVABLE_SUBJECT")
        typed(a["quantity"]);axes(a["axes"]);authorities(a["authority_refs"])
        s=subjects[a["subject"]]
        need(a["projection"] in ("IDENTITY","NATIVE_EXPRESSION"),"OBSERVABLE_PROJECTION")
        if a["projection"]=="IDENTITY":
            need(qcompat(a["quantity"],s["quantity"]) and a["axes"]==s["axes"],"OBSERVABLE_TYPE")
    for k,t in (("inputs",inputs),("outputs",outputs)):
        for a in t.values():
            fields(a,("id","quantity","axes","authority_refs"),"SIGNATURE_FIELDS")
            typed(a["quantity"]);axes(a["axes"]);authorities(a["authority_refs"])
    for a in tables["relations"].values():
        fields(a,("id","kind","from","to","authority_refs"),"RELATION_FIELDS");authorities(a["authority_refs"])
        x,y=a["from"],a["to"];need(x!=y and x in subjects and y in subjects,"RELATION_REFERENCE")
        if a["kind"]=="connected_to":
            need(x in ports and y in ports,"PORT_COMPATIBILITY");p,q=ports[x],ports[y]
            need(p["direction"]=="BIDIRECTIONAL" or q["direction"]=="BIDIRECTIONAL" or {p["direction"],q["direction"]}=={"IN","OUT"},"PORT_COMPATIBILITY")
            need(p["axes"]==q["axes"] and qcompat(p["quantity"],q["quantity"],True),"RELATION_TYPE")
        elif a["kind"]=="counterfactual_of":
            need(x in referents and y in referents and referents[x]["axes"]==referents[y]["axes"] and qcompat(referents[x]["quantity"],referents[y]["quantity"]),"COUNTERFACTUAL_RELATION")
        else:need(False,"RELATION_KIND")
    for a in tables["variations"].values():
        fields(a,("id","subject","alternatives","disclosure","source_refs"),"VARIATION_FIELDS")
        need(a["subject"] in subjects,"VARIATION_SUBJECT")
        need(len(members(a["alternatives"]))>=2 and all(string(x) for x in a["alternatives"]) and a["disclosure"] is True,"VARIATION")
        authorities(a["source_refs"])
    times=set()
    for a in tables["chronologies"].values():
        fields(a,("id","domain","intervals","mode","authority_refs"),"CHRONOLOGY_FIELDS")
        k=a["domain"];need(k in dom and dom[k]["kind"]=="time" and k not in times,"CHRONOLOGY_DOMAIN")
        times.add(k);authorities(a["authority_refs"])
        need(a["mode"] in ("CYCLIC","NONCYCLIC"),"CHRONOLOGY_MODE")
        intervals=a["intervals"];need(type(intervals) is list and len(intervals)==len(dom[k]["members"]),"TIME_SUPPORT")
        previous=None
        for label,row in zip(dom[k]["members"],intervals,strict=True):
            fields(row,("label","start_h","end_h","duration_h"),"INTERVAL_FIELDS")
            x,y,dt=(exact(row[f]) for f in ("start_h","end_h","duration_h"))
            need(row["label"]==label and dt>0 and y-x==dt and (previous is None or x>=previous),"DURATION_OR_CHRONOLOGY")
            previous=y
    need(times=={k for k,a in dom.items() if a["kind"]=="time"},"CHRONOLOGY_COVERAGE")
    # Actual original R1 partition/refinement rules, extracted without its math AST.
    try:r1.information(dom,tables["information_sets"])
    except (ValueError,KeyError,TypeError) as e:raise Reject(str(e)) from e
    partitions={}
    for a in tables["information_sets"].values():
        key=(a["time_domain"],a["scenario_domain"])
        seen=partitions.setdefault(key,set());need(a["stage"] not in seen,"INFORMATION_STAGE_DUPLICATE");seen.add(a["stage"])
    for (t,s),stages in partitions.items():need(stages==set(dom[t]["members"]),"INFORMATION_STAGE_COVERAGE")
    for a in tables["slots"].values():
        fields(a,("id","inputs","observables","outputs","scope","authority_refs"),"SLOT_FIELDS")
        refs(a["inputs"],inputs,"SLOT_INPUT",False);refs(a["observables"],obs,"SLOT_OBSERVABLE",False);refs(a["outputs"],outputs,"SLOT_OUTPUT",False)
        need(a["scope"] in tables["scopes"],"SLOT_SCOPE");authorities(a["authority_refs"])
    for a in tables["processes"].values():
        fields(a,("id","slot","depends_on","authority_refs"),"PROCESS_FIELDS")
        need(a["slot"] in tables["slots"],"PROCESS_SLOT");refs(a["depends_on"],tables["processes"],"PROCESS_DEPENDENCY",False);authorities(a["authority_refs"])
    # The graph validator checks actual dataflow against these explicit declarations.
    need(len({p["slot"] for p in tables["processes"].values()})==len(tables["processes"])==len(tables["slots"]),"PROCESS_COVERAGE")
    return tables
def validate_package_domains(leaf,tables):
    from closure import native
    program=native(leaf["native_canonical"]).program
    for name,z in leaf["context"]["domains"].items():
        k=z["id"];need(k in tables["domains"],"UNRESOLVED_DOMAIN")
        d=tables["domains"][k]
        need(d["ordered"]==program.dimensions[name].ordered and (z["labels"]==d["members"] if d["ordered"] else set(z["labels"])==set(d["members"])),"DOMAIN_ALIGNMENT")
    for n,z in leaf["context"]["temporal"].items():
        k=leaf["context"]["domains"][n]["id"];ch=[x for x in tables["chronologies"].values() if x["domain"]==k]
        need(len(ch)==1 and z["chronology_ref"]==ch[0]["id"],"CHRONOLOGY_BINDING")
        import mathspec.program as mp
        # The checked native leaf already validates edge policies. Only
        # operators actually used impose chronology-mode restrictions.
        def visit(node):
            if type(node) in (mp.Translate,mp.WindowSum) and node.along==n:
                need(node.wrap==(ch[0]["mode"]=="CYCLIC"),"CYCLIC_EDGE" if node.wrap else "NONCYCLIC_EDGE")
            for child in mp.children(node):visit(child)
        for exp in program.expressions.values():visit(exp.expression)
    return program
