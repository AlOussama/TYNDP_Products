# Executable restricted Candidate B adapter

`tools/candidate_b_bridge.js` exports `runContract(jsonOrObject)` and `makeRc01()`. Route: JSON decoder -> unique-ID/ref and typed-expression checks -> version bridge -> C21-compatible structure -> canonical semantic and audit projections. `tools/test_bridge.js` is a standalone Node.js test. Candidate A full EBNF parser: NOT_IMPLEMENTED. Direct invocation of the original pinned C21 Python validator from Node: NOT_EXECUTED. No assertion of full B1 compatibility.

Call: `node Modelling_Language/study_contract_language/workstreams/ML_C24_P1_interface_closure/tools/test_bridge.js`.
