'use strict';
/** Run with: node test_bridge.js. This suite tests the bridge fragment, NOT C21's Python validator or physical model conformance. */
const {runContract,makeRc01}=require('./candidate_b_bridge.js');
function testContract() {
  const good=makeRc01(), results=[];
  const check=(id,ok)=>{results.push({id,pass:Boolean(ok)});if(!ok)throw Error("FAILED "+id)};
  const base=runContract(good);
  check("positive_typed_RCI_bridge_blocked_owner",base.status==="BLOCKED"&&base.target?.frame.schema==="CSNF-C21-0.1"&&base.target?.referents[0].kind==="port"&&base.target?.referents[0].external===true);
  check("owner_no_promotion",base.target.authorities[0].decision==="OWNER_TBD"&&base.target.assertions[0].decision==="OWNER_TBD");
  check("original_ast_projection_preserved",base.target.predicates.length===2&&base.target.observables[0].projection.op==="integrate");
  check("candidate_b_json_decoder",runContract(JSON.stringify(good)).canonical_semantic===base.canonical_semantic);
  check("determinism",runContract(good).canonical_audit===base.canonical_audit);
  check("role_order_commutation",(()=>{let z=JSON.parse(JSON.stringify(good));z.predicates.reverse();z.assertions.reverse();return runContract(z).canonical_semantic===base.canonical_semantic})());
  check("guard_no_silent_drop",(()=>{let z=JSON.parse(JSON.stringify(good));z.assertions[1].guard=true;return runContract(z).canonical_semantic!==base.canonical_semantic})());
  check("reject_unknown_operator",(()=>{let z=JSON.parse(JSON.stringify(good));z.predicates[0].expr.op="contractPredicate";return runContract(z).status==="FAIL_STATIC"})());
  check("reject_dimension_mismatch",(()=>{let z=JSON.parse(JSON.stringify(good));z.predicates[1].expr.rhs.quantity={carrier:"hydrogen",kind:"mass",unit:"kg",value:"1",sign:"INJECTION"};return runContract(z).status==="FAIL_STATIC"})());
  check("reject_missing_observable_projection",(()=>{let z=JSON.parse(JSON.stringify(good));delete z.observables[0].projection;return runContract(z).status==="FAIL_STATIC"})());
  check("reject_undocumented_registry",(()=>{let z=JSON.parse(JSON.stringify(good));z.frame.registry="energy-unknown";return runContract(z).status==="FAIL_STATIC"})());
  check("reject_evidence_promotion",(()=>{let z=JSON.parse(JSON.stringify(good));z.evidences[0].status="PASS";return runContract(z).status==="FAIL_STATIC"})());
  check("reject_source_loss",(()=>{let z=JSON.parse(JSON.stringify(good));z.authorities=[];return runContract(z).status==="FAIL_STATIC"})());
  check("audit_detects_source_change",(()=>{let z=JSON.parse(JSON.stringify(good));z.authorities[0].immutable_ref="ML-C19/11:other";let x=runContract(z);return x.status==="BLOCKED"&&x.canonical_semantic===base.canonical_semantic&&x.canonical_audit!==base.canonical_audit})());
  check("evidence_is_not_execution",base.target.evidences[0].status==="NOT_EXECUTED");
  return {n:results.length,passed:results.filter(x=>x.pass).length,results,baseline_status:base.status,baseline_diagnostics:base.diagnostics,base};
}
const r=testContract();console.log(JSON.stringify({tests:r.results,passed:r.passed,n:r.n},null,2));
