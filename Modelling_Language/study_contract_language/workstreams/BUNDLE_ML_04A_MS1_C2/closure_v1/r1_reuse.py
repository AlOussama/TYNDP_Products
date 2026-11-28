"""R1 metadata validation extraction, no mathematical AST.
Source: BUNDLE_ML_04A_R1/n1r.py, blob 005f8fc0172c71eb1b2d7110b0e2cbc921921d6b.
Information partition and refinement checks lifted from typed(), with the
only adaptation allowing homogeneous exact int/string domain coordinates.
R1 table/unique/ident/quantity and C21 diagnostics are reused directly.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"BUNDLE_ML_04A_R1"))
from n1r import table,unique,ident,quantity as old_quantity,need,fields,c21,pins
from units_r1 import monetary
def unique_members(xs):
    need(type(xs) is list and all(type(x) in (int,str) for x in xs) and len(xs)==len(set(xs)),'SET_TYPE')
    return xs
def information(dom,infos):
    for a in infos.values():
        need(a.get('time_domain') in dom and a.get('scenario_domain') in dom,'INFORMATION_DOMAIN')
    for a in infos.values():
        fields(a,('id','time_domain','stage','scenario_domain','partition'));td=dom[a['time_domain']];sd=dom[a['scenario_domain']];need(td['kind'] in ('time','stage') and sd['kind']=='scenario' and a['stage'] in td['members'],'INFORMATION_DOMAIN');need(type(a['partition']) is list and all(bool(unique_members(group)) for group in a['partition']),'INFORMATION_PARTITION');flat=[v for group in a['partition'] for v in group];need(len(flat)==len(set(flat)) and set(flat)==set(sd['members']),'INFORMATION_PARTITION')
    for a in infos.values():
        for b in infos.values():
            if a['time_domain']==b['time_domain'] and a['scenario_domain']==b['scenario_domain']:
                order=dom[a['time_domain']]['members'];ia,ib=order.index(a['stage']),order.index(b['stage'])
                if ia<=ib:need(all(any(set(g)<=set(h) for h in a['partition']) for g in b['partition']),'INFORMATION_REFINEMENT')

