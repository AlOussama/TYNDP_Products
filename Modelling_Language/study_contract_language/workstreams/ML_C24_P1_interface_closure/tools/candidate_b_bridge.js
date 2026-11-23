'use strict';
/** P1 r0.1 restricted Candidate B JSON decoder, typed predicate checks and explicitly versioned C20->C21 lowering; NON-NORMATIVE. */
function runContract(input) {
  "use strict";
  const SOURCE = ["C20-research-0.1","CSNF-R0","energy-r0"];
  const TARGET = ["CSNF-C21-0.1","CSNF-R0","energy-c21-0.1"];
  const roles = ["referents","relations","predicates","assertions","observables","variations","evidences","authorities"];
  const decisions = ["APPROVED","PROPOSED","OWNER_TBD","REJECTED","SUPERSEDED","UNKNOWN"];
  const statuses = ["PASS","FAIL","NOT_EXECUTED","INCONCLUSIVE","NOT_APPLICABLE","BLOCKED"];
  const legal = {"electricity:active_power":["MW","kW"],"electricity:energy":["MWh","kWh"],"hydrogen:mass_flow":["kg/h","kg/s"],"hydrogen:mass":["kg"],"currency:cost":["EUR","kEUR","MEUR"]};
  const clone = x=>JSON.parse(JSON.stringify(x));
  const stable = x=>JSON.stringify(x,(_k,v)=>(v && !Array.isArray(v) && typeof v==="object")?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v);
  const issues=[],diag=(code,path,severity="ERROR",detail="")=>issues.push({code,path,severity,detail});
  let c;
  try {c=typeof input==="string"?JSON.parse(input):clone(input)}catch(e){return {status:"FAIL_STATIC",diagnostics:[{code:"JSON_DECODE",path:"$",severity:"ERROR",detail:String(e)}]}}
  if(!c||typeof c!=="object"||Array.isArray(c))return {status:"FAIL_STATIC",diagnostics:[{code:"ROOT_OBJECT",path:"$",severity:"ERROR"}]};
  function keys(x,allowed,path){if(!x||typeof x!=="object"||Array.isArray(x)){diag("OBJECT_REQUIRED",path);return false;} for(const k of Object.keys(x))if(!allowed.includes(k))diag("UNKNOWN_FIELD",path+"."+k);return true}
  keys(c,["frame",...roles],"$");
  const frame=c.frame;
  if(keys(frame,["id","schema","ruleset","registry","question","boundary","time","scenario","counterfactual","study_kind"],"$.frame")){
    const actual=[frame.schema,frame.ruleset,frame.registry];
    if(stable(actual)!==stable(SOURCE))diag("UNDECLARED_VERSION_MIGRATION","$.frame","ERROR",stable({expected:SOURCE,actual}));
    if(typeof frame.id!=="string"||!frame.id)diag("FRAME_ID","$.frame.id");
    if(frame.time!==undefined){
      if(keys(frame.time,["id","duration","duration_unit","intervals"],"$.frame.time")){
        if(typeof frame.time.id!=="string"||!frame.time.id)diag("TIME_ID","$.frame.time.id");
        if(!["h","min"].includes(frame.time.duration_unit))diag("DURATION_UNIT","$.frame.time.duration_unit");
        if(!Number.isFinite(Number(frame.time.duration))||Number(frame.time.duration)<=0)diag("DURATION_POSITIVE","$.frame.time.duration");
      }
    }
  }
  const ids=new Map();
  for(const role of roles){
    if(!Array.isArray(c[role])){diag("COLLECTION_REQUIRED","$."+role);continue}
    for(let i=0;i<c[role].length;i++){
      const x=c[role][i],p="$."+role+"["+i+"]";
      if(!x||typeof x!=="object"||typeof x.id!=="string"||!x.id){diag("ID_REQUIRED",p);continue}
      if(ids.has(x.id))diag("DUPLICATE_ID",p,"ERROR",x.id);
      ids.set(x.id,{role,node:x});
    }
  }
  function ref(id,role,path){
    if(typeof id!=="string"||!ids.has(id)){diag("UNRESOLVED_REFERENCE",path,"ERROR",String(id));return null}
    if(role&&ids.get(id).role!==role){diag("REFERENCE_ROLE",path,"ERROR",String(role));return null}
    return ids.get(id).node;
  }
  function quantity(q,path){
    if(!keys(q,["carrier","kind","unit","value","sign","basis"],path))return null;
    const kind=q.carrier+":"+q.kind;
    if(!(kind in legal)){diag("UNKNOWN_DIMENSION",path);return null}
    if(!legal[kind].includes(q.unit))diag("INVALID_UNIT",path+".unit");
    if(!["INJECTION","CONSUMPTION","BIDIRECTIONAL","NONE"].includes(q.sign))diag("INVALID_SIGN",path+".sign");
    if(!("value" in q)||!Number.isFinite(Number(q.value)))diag("EXPLICIT_QUANTITY_REQUIRED",path+".value");
    if(kind==="currency:cost"&&!q.basis)diag("PRICE_BASIS_MISSING",path+".basis");
    return {carrier:q.carrier,kind:q.kind,unit:q.unit,sign:q.sign,basis:q.basis||null};
  }
  for(const [i,r] of (c.referents||[]).entries()){
    const path="$.referents["+i+"]";
    if(!keys(r,["id","kind","type","role","quantity","direction","scope","external"],path))continue;
    if(r.kind!=="external_port" && r.kind!=="entity" && r.kind!=="domain"){
      diag("REFERENT_KIND_UNSUPPORTED",path+".kind");continue;
    }
    if(r.kind==="external_port"){
      if(!["IN","OUT","BIDIRECTIONAL"].includes(r.direction))diag("PORT_DIRECTION",path+".direction");
      quantity(r.quantity,path+".quantity");
    }
  }
  for(const [i,rel] of (c.relations||[]).entries()){
    const path="$.relations["+i+"]";
    if(!keys(rel,["id","kind","from","to","authority_refs"],path))continue;
    const a=ref(rel.from,"referents",path+".from"),b=ref(rel.to,"referents",path+".to");
    if(rel.kind==="connected_to"&&a&&b){
      if(a.kind!=="external_port"||b.kind!=="external_port")diag("CONNECTED_TO_NONPORT",path);
      else if(a.quantity?.carrier!==b.quantity?.carrier||a.quantity?.kind!==b.quantity?.kind)diag("PORT_CARRIER_MISMATCH",path);
    }
    for(const s of rel.authority_refs||[])ref(s,"authorities",path+".authority_refs");
  }
  function guard(g,path){
    if(typeof g==="boolean"||g==="UNKNOWN")return;
    if(g&&typeof g==="object"&&typeof g.atom==="string"&&Object.keys(g).length===1)return;
    if(!g||typeof g!=="object"||!["AND","OR","NOT"].includes(g.op)||!Array.isArray(g.args)||g.args.length<(g.op==="NOT"?1:2)||(g.op==="NOT"&&g.args.length!==1)) {diag("GUARD_AST",path);return}
    g.args.forEach((child,i)=>guard(child,path+".args["+i+"]"));
  }
  function expression(e,path){
    if(!e||typeof e!=="object"||Array.isArray(e)){diag("PREDICATE_AST_REQUIRED",path);return null}
    switch(e.op){
      case "bool3":
        keys(e,["op","value"],path);
        if(!["TRUE","FALSE","UNKNOWN"].includes(e.value))diag("BOOL3_VALUE",path);
        return {type:"Bool3"};
      case "and":case "or":case "not":
        keys(e,["op","args"],path);
        if(!Array.isArray(e.args)||e.args.length<(e.op==="not"?1:2)||(e.op==="not"&&e.args.length!==1)){diag("BOOLEAN_ARITY",path);return null}
        e.args.forEach((v,i)=>{const t=expression(v,path+".args["+i+"]");if(t?.type!=="Bool3")diag("EXPECTED_BOOL3",path+".args["+i+"]")});
        return {type:"Bool3"};
      case "forall":case "exists":{
        keys(e,["op","var","domain","body"],path);
        if(typeof e.var!=="string"||!e.var||!e.domain||!["time","scenario","vehicle"].includes(e.domain.kind)||typeof e.domain.ref!=="string")
          diag("QUANTIFIER_DOMAIN",path);
        else if(e.domain.ref!==frame?.time?.id&&e.domain.ref!==frame?.scenario?.id&&!ids.has(e.domain.ref))
          diag("DOMAIN_NOT_FOUND",path+".domain.ref");
        const t=expression(e.body,path+".body");
        if(t?.type!=="Bool3")diag("QUANTIFIER_BODY_BOOL3",path);
        return {type:"Bool3"};
      }
      case "measure":{
        keys(e,["op","ref"],path);
        const r=ref(e.ref,"referents",path+".ref");
        if(r?.kind!=="external_port"){diag("MEASURE_NEEDS_PORT",path);return null}
        const q=r.quantity;
        return q?{type:"Quantity",carrier:q.carrier,kind:q.kind,sign:q.sign,basis:q.basis||null}:null;
      }
      case "literal":{
        keys(e,["op","quantity"],path);
        const q=quantity(e.quantity,path+".quantity");
        return q?{type:"Quantity",carrier:q.carrier,kind:q.kind,sign:q.sign,basis:q.basis}:null;
      }
      case "integrate":{
        keys(e,["op","expr","duration_ref"],path);
        const t=expression(e.expr,path+".expr");
        if(e.duration_ref!==frame?.time?.id||!frame?.time?.duration)diag("INTEGRATION_DURATION_MISSING",path+".duration_ref");
        if(t?.type!=="Quantity"||t?.carrier!=="electricity"||t?.kind!=="active_power"){diag("INTEGRATION_DIMENSION",path);return null}
        return {...t,kind:"energy"};
      }
      case "compare":{
        keys(e,["op","cmp","lhs","rhs"],path);
        if(!["eq","le","ge","lt","gt"].includes(e.cmp))diag("COMPARISON_OPERATOR",path+".cmp");
        const a=expression(e.lhs,path+".lhs"),b=expression(e.rhs,path+".rhs");
        if(!a||!b||a.type!=="Quantity"||b.type!=="Quantity"||a.carrier!==b.carrier||a.kind!==b.kind||a.sign!==b.sign||a.basis!==b.basis)
          diag("DIMENSION_OR_BASIS_MISMATCH",path);
        return {type:"Bool3"};
      }
      default:diag("UNKNOWN_PREDICATE_OPERATOR",path+".op","ERROR",String(e.op));return null;
    }
  }
  for(const [i,p] of (c.predicates||[]).entries()){
    const path="$.predicates["+i+"]";if(!keys(p,["id","expr"],path))continue;
    if(expression(p.expr,path+".expr")?.type!=="Bool3")diag("PREDICATE_NOT_BOOL3",path);
  }
  for(const [i,a] of (c.authorities||[]).entries()){
    const path="$.authorities["+i+"]";
    if(!keys(a,["id","role","immutable_ref","revision","decision_state"],path))continue;
    if(!["SOURCE","OWNER","DECISION","PROVENANCE"].includes(a.role))diag("AUTHORITY_ROLE",path+".role");
    if(!decisions.includes(a.decision_state))diag("AUTHORITY_DECISION",path+".decision_state");
    if(!a.immutable_ref)diag("SOURCE_IMMUTABLE_REF",path+".immutable_ref");
  }
  for(const [i,a] of (c.assertions||[]).entries()){
    const path="$.assertions["+i+"]";
    if(!keys(a,["id","modality","semantic_role","predicate_ref","scope","guard","authority_refs","decision_state"],path))continue;
    if(!["REQUIRED","PROHIBITED","PERMITTED","IMPLEMENTATION_DEFINED","CONDITIONAL"].includes(a.modality))diag("MODALITY",path+".modality");
    if(!["SAFETY_GUARANTEE","SERVICE_GUARANTEE","CAPABILITY_GUARANTEE","DATA_ASSUMPTION","ENVIRONMENT_ASSUMPTION","TECHNICAL_ASSUMPTION"].includes(a.semantic_role))diag("ASSERTION_ROLE",path+".semantic_role");
    if(!decisions.includes(a.decision_state))diag("ASSERTION_DECISION",path+".decision_state");
    else if(["OWNER_TBD","UNKNOWN"].includes(a.decision_state))diag("OWNER_UNRESOLVED",path+".decision_state","BLOCKED");
    if(!a.scope)diag("SCOPE_REQUIRED",path+".scope");
    if(!Object.prototype.hasOwnProperty.call(a,"guard"))diag("GUARD_REQUIRED",path+".guard");else guard(a.guard,path+".guard");
    ref(a.predicate_ref,"predicates",path+".predicate_ref");
    if(!Array.isArray(a.authority_refs)||!a.authority_refs.length)diag("SOURCE_REQUIRED",path+".authority_refs");
    else a.authority_refs.forEach((id,j)=>ref(id,"authorities",path+".authority_refs["+j+"]"));
  }
  for(const [i,o] of (c.observables||[]).entries()){
    const path="$.observables["+i+"]";
    if(!keys(o,["id","subject","projection","quantity","aggregation","basis","selection","tolerance"],path))continue;
    ref(o.subject,"referents",path+".subject");
    const p=expression(o.projection,path+".projection"),q=quantity(o.quantity,path+".quantity");
    if(!p||!q||p.type!=="Quantity"||p.carrier!==q.carrier||p.kind!==q.kind||p.sign!==q.sign)diag("OBSERVABLE_PROJECTION_TYPE",path);
    if(o.aggregation==="energy_integration"&&!frame?.time?.duration)diag("INTEGRATION_DURATION_MISSING",path);
  }
  for(const [i,v] of (c.variations||[]).entries()){
    const path="$.variations["+i+"]";
    if(!keys(v,["id","subject","alternatives","disclosure","source_refs","proof_duty"],path))continue;
    ref(v.subject,"referents",path+".subject");
    if(!Array.isArray(v.alternatives)||v.alternatives.length<2||!v.alternatives.every(x=>typeof x==="string"&&x))diag("VARIATION_CHOICES",path);
    if(v.disclosure!==true&&v.disclosure!==false)diag("VARIATION_DISCLOSURE",path);
    if(!Array.isArray(v.source_refs)||!v.source_refs.length)diag("VARIATION_SOURCE",path);
    else v.source_refs.forEach(s=>ref(s,"authorities",path+".source_refs"));
  }
  for(const [i,e] of (c.evidences||[]).entries()){
    const path="$.evidences["+i+"]";
    if(!keys(e,["id","role","subject_ref","status","run_id","evidence_digest","oracle","level","source_refs"],path))continue;
    if(!["REQUEST","RESULT"].includes(e.role))diag("EVIDENCE_ROLE",path+".role");
    if(!statuses.includes(e.status))diag("EVIDENCE_STATUS",path+".status");
    if(!["assertions","observables"].includes(ids.get(e.subject_ref)?.role))diag("EVIDENCE_SUBJECT",path+".subject_ref");
    if(e.status==="PASS"&&(e.role!=="RESULT"||!e.run_id||!e.evidence_digest))diag("UNSUPPORTED_PASS",path);
  }
  if(issues.some(x=>x.severity==="ERROR"))return {status:"FAIL_STATIC",diagnostics:issues};
  const target=clone(c);
  target.frame.schema=TARGET[0];target.frame.ruleset=TARGET[1];target.frame.registry=TARGET[2];
  target.referents.forEach(r=>{if(r.kind==="external_port"){r.kind="port";r.external=true;}});
  target.assertions.forEach(a=>{a.decision=a.decision_state;delete a.decision_state});
  target.authorities.forEach(a=>{a.decision=a.decision_state;delete a.decision_state});
  for(const role of roles)target[role].sort((a,b)=>a.id.localeCompare(b.id,"en"));
  const canonicalGuard=g=>{
    if(!g||typeof g!=="object")return g;
    if(g.op==="AND"||g.op==="OR")return {op:g.op,args:g.args.map(canonicalGuard).sort((a,b)=>stable(a).localeCompare(stable(b),"en"))};
    if(g.op==="NOT")return {op:"NOT",args:g.args.map(canonicalGuard)};
    return g;
  };
  target.assertions.forEach(a=>{a.guard=canonicalGuard(a.guard);a.authority_refs.sort()});
  const semantic=clone(target);
  const authorityStates=new Map(semantic.authorities.map(a=>[a.id,a.decision]));
  semantic.assertions.forEach(a=>{a.authority_states=[...new Set(a.authority_refs.map(id=>authorityStates.get(id)))].sort();delete a.authority_refs});
  delete semantic.authorities;
  const audit={source_versions:SOURCE,target_versions:TARGET,adapter:"ML-C24-P1-bridge-r0.1",original_authorities:clone(c.authorities),target_authorities:clone(target.authorities),original_assertions:clone(c.assertions),source_document_id:c.frame.id};
  return {status:issues.some(x=>x.severity==="BLOCKED")?"BLOCKED":"PASS_STATIC",diagnostics:issues,target,semantic,audit,canonical_semantic:stable(semantic),canonical_audit:stable(audit)};
}
function makeRc01() {
  const power=(value,unit="MW")=>({carrier:"electricity",kind:"active_power",unit,value,sign:"INJECTION"});
  const energy=(value)=>({carrier:"electricity",kind:"energy",unit:"MWh",value,sign:"INJECTION"});
  const measure=()=>({op:"measure",ref:"RC01:grid"});
  const lit=v=>({op:"literal",quantity:power(v)});
  return {
    frame:{id:"RC01:study",schema:"C20-research-0.1",ruleset:"CSNF-R0",registry:"energy-r0",question:"Battery external bounds and energy trace",time:{id:"RC01:time",duration:"0.5",duration_unit:"h"}},
    referents:[{id:"RC01:grid",kind:"external_port",type:"electricity.active_power",direction:"BIDIRECTIONAL",quantity:power("0")}],
    relations:[],
    predicates:[
      {id:"RC01:Pbounds",expr:{op:"forall",var:"t",domain:{kind:"time",ref:"RC01:time"},body:{op:"and",args:[
        {op:"compare",cmp:"ge",lhs:measure(),rhs:lit("-3")},
        {op:"compare",cmp:"le",lhs:measure(),rhs:lit("4")}
      ]}}},
      {id:"RC01:Pledger",expr:{op:"compare",cmp:"eq",lhs:{op:"integrate",expr:measure(),duration_ref:"RC01:time"},rhs:{op:"literal",quantity:energy("-1")}}}
    ],
    assertions:[
      {id:"RC01:A",modality:"REQUIRED",semantic_role:"SAFETY_GUARANTEE",predicate_ref:"RC01:Pbounds",scope:"RC01:time",guard:true,authority_refs:["RC01:SRC"],decision_state:"OWNER_TBD"},
      {id:"RC01:B",modality:"CONDITIONAL",semantic_role:"SERVICE_GUARANTEE",predicate_ref:"RC01:Pledger",scope:"RC01:time",guard:{atom:"battery:connected"},authority_refs:["RC01:SRC"],decision_state:"OWNER_TBD"}
    ],
    observables:[{id:"RC01:O",subject:"RC01:grid",projection:{op:"integrate",expr:measure(),duration_ref:"RC01:time"},quantity:energy("0"),aggregation:"energy_integration"}],
    variations:[{id:"RC01:V",subject:"RC01:grid",alternatives:["SOC-state","energy-state"],disclosure:true,source_refs:["RC01:SRC"]}],
    evidences:[{id:"RC01:E",role:"REQUEST",subject_ref:"RC01:A",status:"NOT_EXECUTED",oracle:"ML-C23/research-r0.1"}],
    authorities:[{id:"RC01:SRC",role:"SOURCE",immutable_ref:"ML-C19/11:RC01",revision:"r0.1",decision_state:"OWNER_TBD"}]
  };
}
module.exports={runContract,makeRc01};
