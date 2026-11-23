"""B1 research-only cross-workstream incompatibility witness; NOT a complete adapter."""
from __future__ import annotations
import json
from pathlib import Path
from csnf_validator import validate, normalize, CSNFError

p = Path(__file__).resolve().parent / 'data' / 'b1_c20_candidate_b_rc01.json'
c = json.loads(p.read_text(encoding='utf8'))
issues = validate(c)
codes = [i['code'] for i in issues]
assert codes.count('VERSION_MISMATCH') == 2, issues
assert 'OWNER_STATE' in codes, issues
assert 'OWNER_UNRESOLVED' in codes, issues
try:
    normalize(c)
except CSNFError:
    pass
else:
    raise AssertionError('B1 candidate must not be silently accepted')
print(json.dumps({'status':'INCOMPATIBLE_EXPECTED', 'case':'RC01:C20-Candidate-B',
                  'diagnostics':issues, 'note':'No syntax parser or C22 native adapter was executed'},
                 indent=2))
