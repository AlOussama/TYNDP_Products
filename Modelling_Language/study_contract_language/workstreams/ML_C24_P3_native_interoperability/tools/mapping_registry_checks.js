'use strict';
/** Checks pinned C22 conceptual mapping registry only, not native tool compatibility. */
function assessRegistry(reg){
 const failures=[];
 if(reg.roles?.length!==9)failures.push("ROLE_COUNT_NOT_NINE");
 const roles=reg.roles||[];
 for(let i=1;i<=9;i++){const x=roles.find(y=>y.role==="C"+i);if(!x)failures.push("MISSING_C"+i);else for(const k of ["name","sysml","gems","mathspec","gap","proof"])if(!x[k])failures.push("MISSING_C"+i+"_"+k)}
 if(reg.native_execution!=="NOT_EXECUTED")failures.push("PREMATURE_NATIVE_EVIDENCE");
 if(reg.roundtrip?.semantic!=="NOT_EXECUTED"||reg.roundtrip?.audit!=="NOT_EXECUTED")failures.push("PREMATURE_ROUNDTRIP");
 if(!reg.links?.gems?.includes("c463e30b610443c1f59b20074bb7acffa2844cce"))failures.push("GEMS_PIN_DRIFT");
 if(!reg.links?.mathspec?.includes("5f1464c334c1012cdee2947d4d55b4d1d6bef40a"))failures.push("MATHSPEC_PIN_DRIFT");
 return {status:failures.length?"FAIL_METADATA":"PASS_CONCEPTUAL_REGISTRY_ONLY",failures,roles:roles.length,language_columns:3,semantic_loss:"NOT_MEASURED",audit_loss:"NOT_MEASURED",native_executed:false};
}
module.exports={assessRegistry};
