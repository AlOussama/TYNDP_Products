"""ML-C19 synthetic-only CSNF-R0 subset microchecks (stdlib only).
No mathspec/GEMS/SysML parser, no energy model or solver is exercised.
"""
from __future__ import annotations
import copy
import json
import unittest

VALID_STATES = {"REQUIRED", "PROHIBITED", "PERMITTED", "IMPLEMENTATION_DEFINED"}
VALID_EVIDENCE = {"PASS", "FAIL", "NOT_EXECUTED", "INCONCLUSIVE", "BLOCKED"}
VALID_OWNER = {"APPROVED", "OWNER_TBD", "PROPOSED"}

def canonical_guard(x):
    if not isinstance(x, dict):
        raise ValueError("guard AST must be object")
    if "atom" in x and len(x) == 1:
        return {"atom": str(x["atom"])}
    op = x.get("op")
    if op not in ("AND", "OR", "NOT"):
        raise ValueError("unknown guard operator")
    args = x.get("args", [])
    if op == "NOT":
        if len(args) != 1:
            raise ValueError("NOT arity")
        return {"op": op, "args": [canonical_guard(args[0])]}
    if len(args) < 2:
        raise ValueError("AND/OR arity")
    flat = []
    for a in args:
        a = canonical_guard(a)
        if a.get("op") == op:
            flat.extend(a["args"])
        else:
            flat.append(a)
    flat.sort(key=lambda q: json.dumps(q, sort_keys=True))
    return {"op": op, "args": flat}

def canonical(c):
    """Fixed schema subset. Reject unknown conversions; preserve all authority IDs."""
    c = copy.deepcopy(c)
    if c.get("schema") != "CSNF-R0":
        raise ValueError("schema mismatch")
    if not isinstance(c.get("obligations"), list):
        raise ValueError("missing obligations")
    out = []
    ids = set()
    for a in c["obligations"]:
        if a["id"] in ids:
            raise ValueError("duplicate assertion id")
        ids.add(a["id"])
        if a["modality"] not in VALID_STATES or a["evidence"] not in VALID_EVIDENCE:
            raise ValueError("invalid normative/evidence status")
        if a["owner"] not in VALID_OWNER:
            raise ValueError("invalid owner status")
        if not a["sources"]:
            raise ValueError("source required")
        if len(a["sources"]) != len(set(a["sources"])):
            raise ValueError("duplicate source reference")
        a["sources"].sort()
        a["guard"] = canonical_guard(a["guard"])
        q = a["quantity"]
        if q["kind"] == "active_power" and q["unit"] == "kW":
            q["value"] /= 1000
            q["unit"] = "MW"
        elif q["unit"] == "MWh" and q["kind"] == "h2_mass":
            raise ValueError("H2 kg to energy needs external basis")
        elif (q["kind"], q["unit"]) not in {
            ("active_power", "MW"), ("h2_mass", "kg"), ("energy", "MWh")
        }:
            raise ValueError("unsupported physical kind/unit combination")
        out.append(a)
    out.sort(key=lambda v: v["id"])
    return {"schema": "CSNF-R0", "obligations": out}

def text(c):
    return json.dumps(canonical(c), sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def model():
    return {"schema": "CSNF-R0", "obligations": [
        {"id": "a1", "modality": "REQUIRED", "owner": "APPROVED",
         "evidence": "NOT_EXECUTED", "semantic_role": "BEHAVIOURAL_GUARANTEE",
         "role": "physical_branch", "carrier": "electricity",
         "direction": "INJECTION", "scope": "scenario:S1,t=0:2",
         "constraint": "KCL_AND_KVL", "sources": ["D:2", "D:1"],
         "guard": {"op": "AND", "args": [{"atom": "Available"}, {"atom": "GridConnected"}]},
         "quantity": {"kind": "active_power", "unit": "MW", "value": 1.0}}
    ]}

class Check(unittest.TestCase):
    def test_normalized_repeat(self):
        self.assertEqual(canonical(canonical(model())), canonical(model()))
    def test_ordered_sources_deterministic(self):
        a=model(); b=model(); b["obligations"][0]["sources"].reverse()
        self.assertEqual(text(a), text(b))
    def test_commutative_guard(self):
        a=model(); b=model(); b["obligations"][0]["guard"]["args"].reverse()
        self.assertEqual(text(a), text(b))
    def test_guard_associativity(self):
        a=model(); b=model()
        a["obligations"][0]["guard"]={"op":"AND","args":[{"atom":"a"},{"op":"AND","args":[{"atom":"b"},{"atom":"c"}]}]}
        b["obligations"][0]["guard"]={"op":"AND","args":[{"atom":"c"},{"atom":"a"},{"atom":"b"}]}
        self.assertEqual(text(a), text(b))
    def test_unit_conversion(self):
        a=model(); b=model(); b["obligations"][0]["quantity"].update(value=1000.0,unit="kW")
        self.assertEqual(text(a), text(b))
    def test_unordered_obligations(self):
        a=model(); a["obligations"].append(copy.deepcopy(a["obligations"][0]))
        a["obligations"][1]["id"]="a2"
        b=copy.deepcopy(a); b["obligations"].reverse()
        self.assertEqual(text(a), text(b))

def mutation_test(name, changes):
    def fn(self):
        a=model(); b=model()
        for key,val in changes.items():
            b["obligations"][0][key]=val
        self.assertNotEqual(text(a), text(b), name)
    setattr(Check, "test_distinguish_"+name, fn)

base = model()["obligations"][0]
for name,change in {
    "injection_consumption": {"direction":"CONSUMPTION"},
    "kcl_only": {"constraint":"KCL"},
    "physical_marketlink": {"role":"market_link"},
    "required_permitted": {"modality":"PERMITTED"},
    "owner_tbd": {"owner":"OWNER_TBD"},
    "not_executed_pass": {"evidence":"PASS"},
    "data_assumption_guarantee": {"semantic_role":"DATA_ASSUMPTION"},
    "different_source_authority": {"sources":["D:1","D:3"]},
    "scenario_change": {"scope":"scenario:S2,t=0:2"},
    "carrier_change": {"carrier":"hydrogen"},
    "guard_change": {"guard":{"op":"AND","args":[{"atom":"GridConnected"},{"atom":"ServiceRequired"}]}},
    "different_feasible_set": {"constraint":"OBJECTIVE_EQUAL_ONLY"},
}.items():
    mutation_test(name, change)

class Reject(unittest.TestCase):
    def test_h2_energy_without_basis_rejected(self):
        a=model(); a["obligations"][0]["quantity"]={"kind":"h2_mass","unit":"MWh","value":1}
        with self.assertRaisesRegex(ValueError, "H2"):
            canonical(a)
    def test_unknown_owner_rejected(self):
        a=model(); a["obligations"][0]["owner"]="UNSPECIFIED"
        with self.assertRaises(ValueError):
            canonical(a)
    def test_source_absence_rejected(self):
        a=model(); a["obligations"][0]["sources"]=[]
        with self.assertRaises(ValueError):
            canonical(a)
    def test_duplicate_assertion_rejected(self):
        a=model(); a["obligations"].append(copy.deepcopy(a["obligations"][0]))
        with self.assertRaises(ValueError):
            canonical(a)

if __name__ == "__main__":
    unittest.main(verbosity=2)
