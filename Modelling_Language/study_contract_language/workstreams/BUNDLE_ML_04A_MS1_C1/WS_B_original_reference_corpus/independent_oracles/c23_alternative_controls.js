'use strict';
// NON-NORMATIVE / RESEARCH ONLY. Additional C23 interpretations, never original test IDs.
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const ROOT=path.resolve(__dirname,'..');
const PIN="2eb4c2d162665424c0cb43262f2d54e448e08c2c";
const BLOBS={
  "frozen/c23_mutation_cases.json": "71b48ce7627eb8417a0ab906d465c519dffa415f",
  "reference_cases/RC01/contract.json": "7135ca77e2a89f4bcac015a073cd2524d7a8df4f",
  "reference_cases/RC03/contract.json": "617e545a51f3b5f66f815129271b1d2eefcc1fb4",
  "reference_cases/RC04/contract.json": "ee401d0c1da56137c45d0f58e9bd14b2680dee2c",
  "reference_cases/RC08/contract.json": "9b2e69652b5a16634a23cc29ffe03578f3ac65cd",
  "reference_cases/RC10/contract.json": "e775b67b54eaddd596d366860f75ec82b4806c4c"
};
function runAlternativeControls(cases,originals,blobs){
  // Independent finite reference controls; no mathspec, R1, validator or candidate architecture imports.
  const clone=o=>JSON.parse(JSON.stringify(o));
  const exact=x=>{if(typeof x!=="string"||!/^[-+]?\d+(\/[1-9]\d*)?$/.test(x))throw Error("NONEXACT_REFERENCE");let [a,b="1"]=x.split("/");return [BigInt(a),BigInt(b)]};
  const add=([a,b],[c,d])=>[a*d+c*b,b*d];
  const mul=([a,b],[c,d])=>[a*c,b*d];
  const equal=([a,b],[c,d])=>a*d===c*b;
  const show=([a,b])=>{if(a===0n)return "0";let x=a<0n?-a:a,y=b;while(y){[x,y]=[y,x%y]}a/=x;b/=x;return b===1n?String(a):`${a}/${b}`};
  const rows=[];
  const validate=(id,doc,extra)=>{
    const s=doc.synthetic_data, d=s.inputs,o=s.observed,u=s.units;
    if(id==="RC01"){
      return !Object.hasOwn(o,"terminal_policy")||!o.terminal_policy?{diagnostic:"TERMINAL_POLICY_UNDECLARED"}:{diagnostic:"ADMITTED_OWNER_STATUS_ONLY",owner:o.terminal_policy};
    }
    if(id==="RC03"){
      if(d.basis!=="LHV"||!Object.hasOwn(d,"lhv")||d.lhv===null)return {diagnostic:"HEATING_VALUE_REQUIRED"};
      const hv=exact(d.lhv);if(hv[0]<=0n)return {diagnostic:"HEATING_VALUE_REQUIRED"};
      if(extra.comparison!=="CONVERT_FLOW_TO_H2_POWER"||u.flow!=="kg/h"||u.lhv!=="MWh_H2_LHV/kg"||u.power!=="MW electricity consumption")return {diagnostic:"INCOMPATIBLE_DIMENSIONS"};
      const hp=mul(exact(o.flow),hv);
      return {diagnostic:"EXPLICIT_CONVERSION_ONLY",hydrogen_power:show(hp)};
    }
    if(id==="RC04")return o.energy_basis!==d.basis?{diagnostic:"HEATING_VALUE_BASIS_MISMATCH"}:{diagnostic:"BASIS_MATCH_ONLY",basis:d.basis};
    if(id==="RC08"){
      const k=add(exact(d.capex),mul(mul(d.opex.reduce((a,x,i)=>add(a,mul(exact(x),exact(d.duration[i]))),[0n,1n]),exact(d.probability)),exact(d.discount)));
      const actual=exact(o.kpi);
      return {diagnostic:equal(k,actual)?"WEIGHTED_KPI_MATCH":"KPI_TIME_WEIGHT_OMITTED_OR_VALUE_MISMATCH",expected:show(k),reported:show(actual)};
    }
    if(id==="RC10"){
      const hidden=extra.actual.flatMap((xs,i)=>xs.filter(x=>!extra.disclosed[i].includes(x)).map(x=>({model:d.model_ids[i],assumption:x})));
      return {diagnostic:hidden.length?"UNDISCLOSED_ASSUMPTION":"DISCLOSURE_MATCH_ONLY",hidden};
    }
    throw Error("unknown RC");
  };
  const emit=(id,kind,rc,doc,extra,expected,originalId,edits)=>{
    const actual=validate(rc,doc,extra),original=originalId?originals.cases.find(x=>x.id===originalId):null;
    if(originalId&&(!original||original.rc!==rc))throw Error("original mapping mismatch");
    const ok=JSON.stringify(expected)===JSON.stringify(actual);
    rows.push({id,kind,original_id:originalId,rc,source_fixture_blob:blobs[`reference_cases/${rc}/contract.json`],original_expected:original?.expected??null,original_description:original?.mutation??null,edits,derived_context:extra,expected,actual,status:ok?"PASS":"FAIL",stage:"ADDITIONAL_INDEPENDENT_FINITE_CONTROL",scope:"No original E1/AUDIT or full A/B verdict; synthetic control only"});
  };
  const rc01=clone(cases.RC01);
  emit("ALT-CTRL-01","positive_control","RC01",rc01,{}, {diagnostic:"ADMITTED_OWNER_STATUS_ONLY",owner:"OWNER_TBD"},null,[]);
  const m01=clone(rc01);delete m01.synthetic_data.observed.terminal_policy;
  emit("ALT-MUT-01B","alternative_mutation","RC01",m01,{}, {diagnostic:"TERMINAL_POLICY_UNDECLARED"},"MUT-01",[{op:"remove",path:["synthetic_data","observed","terminal_policy"]}]);
  const rc03=clone(cases.RC03);
  emit("ALT-CTRL-03","positive_control","RC03",rc03,{comparison:"CONVERT_FLOW_TO_H2_POWER"},{diagnostic:"EXPLICIT_CONVERSION_ONLY",hydrogen_power:"20"},null,[]);
  emit("ALT-MUT-03B","alternative_mutation","RC03",rc03,{comparison:"DIRECT_MW_VS_KG_PER_H"},{diagnostic:"INCOMPATIBLE_DIMENSIONS"},"MUT-03",[{op:"replace",path:["derived_context","comparison"],value:"DIRECT_MW_VS_KG_PER_H"}]);
  const m03=clone(rc03);delete m03.synthetic_data.inputs.lhv;
  emit("ALT-MUT-03C","alternative_mutation","RC03",m03,{comparison:"CONVERT_FLOW_TO_H2_POWER"},{diagnostic:"HEATING_VALUE_REQUIRED"},"MUT-03",[{op:"remove",path:["synthetic_data","inputs","lhv"]}]);
  const rc04=clone(cases.RC04);
  emit("ALT-CTRL-04","positive_control","RC04",rc04,{}, {diagnostic:"BASIS_MATCH_ONLY",basis:"LHV"},null,[]);
  const m04=clone(rc04);m04.synthetic_data.observed.energy_basis="HHV";
  emit("ALT-MUT-04B","alternative_mutation","RC04",m04,{}, {diagnostic:"HEATING_VALUE_BASIS_MISMATCH"},"MUT-04",[{op:"replace",path:["synthetic_data","observed","energy_basis"],value:"HHV"}]);
  const rc08=clone(cases.RC08);
  emit("ALT-CTRL-08","positive_control","RC08",rc08,{}, {diagnostic:"WEIGHTED_KPI_MATCH",expected:"170",reported:"170"},null,[]);
  const m08=clone(rc08);const d=m08.synthetic_data.inputs;
  m08.synthetic_data.observed.kpi=show(add(exact(d.capex),mul(mul(d.opex.reduce((a,x)=>add(a,exact(x)),[0n,1n]),exact(d.probability)),exact(d.discount))));
  emit("ALT-MUT-08B","alternative_mutation","RC08",m08,{}, {diagnostic:"KPI_TIME_WEIGHT_OMITTED_OR_VALUE_MISMATCH",expected:"170",reported:"160"},"MUT-08",[{op:"replace",path:["synthetic_data","observed","kpi"],value:m08.synthetic_data.observed.kpi,derivation:"100 + 20 + 40 (omits declared durations)"}]);
  const rc10=clone(cases.RC10);
  const x={actual:[["common","synthetic-extra"],["common"]],disclosed:[["common","synthetic-extra"],["common"]]};
  emit("ALT-CTRL-10","positive_control","RC10",rc10,x,{diagnostic:"DISCLOSURE_MATCH_ONLY",hidden:[]},null,[]);
  const y=clone(x);y.disclosed[0]=["common"];
  emit("ALT-MUT-10B","alternative_mutation","RC10",rc10,y,{diagnostic:"UNDISCLOSED_ASSUMPTION",hidden:[{model:"M-A",assumption:"synthetic-extra"}]},"MUT-10",[{op:"remove",path:["derived_context","disclosed",0,1]}]);
  return rows;
}
function readPinned(name){const b=fs.readFileSync(path.join(ROOT,name));const h=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');if(h!==BLOBS[name])throw Error('fixture blob mismatch: '+name);return JSON.parse(b);}
if(require.main===module){const originals=readPinned('frozen/c23_mutation_cases.json');const cases=Object.fromEntries(Object.keys(BLOBS).filter(x=>x.startsWith('reference_cases/')).map(x=>{const d=readPinned(x);return [d.id,d]}));const rows=runAlternativeControls(cases,originals,BLOBS);console.log(JSON.stringify({source_pin:PIN,results:rows},null,2));if(rows.some(r=>r.status!=='PASS'))process.exitCode=1;}
module.exports={runAlternativeControls};
