'use strict';
/** Structural semantic role preservation and finite modelling freedom research. No E2/E4 general proof. */
function structuralExperiments(input){
 const clone=x=>JSON.parse(JSON.stringify(x));
 const roles=["frame","referents","relations","predicates","assertions","observables","variations","evidences","authorities"];
 const data=clone(input);
 data.referents.push({id:"RC01:BUS_A",kind:"external_port",type:"electricity.active_power",direction:"BIDIRECTIONAL",quantity:clone(data.referents[0].quantity)});
 data.relations.push({id:"RC01:connection",kind:"connected_to",from:"RC01:grid",to:"RC01:BUS_A",authority_refs:["RC01:SRC"]});
 function canonical(v){
   if(Array.isArray(v))return v.map(canonical);
   if(v&&typeof v==="object")return Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])]));
   return v;
 }
 const signature=x=>JSON.stringify(canonical(Object.fromEntries(roles.map(k=>[k,k in x?x[k]:null]))));
 const base=signature(data);
 const dropTests=roles.map((key,i)=>{const mutant=clone(data);delete mutant[key];return {role:"C"+(i+1),dropped:key,detected:base!==signature(mutant)}});
 function pack(x){
  const z=clone(x);
  for(const e of z.evidences)z.referents.push({__csnf_reified:"C8",record:e});
  for(const a of z.authorities)z.referents.push({__csnf_reified:"C9",record:a});
  delete z.evidences;delete z.authorities;
  return z;
 }
 function unpack(z){
  const out=clone(z);
  out.evidences=out.referents.filter(v=>v.__csnf_reified==="C8").map(v=>v.record);
  out.authorities=out.referents.filter(v=>v.__csnf_reified==="C9").map(v=>v.record);
  out.referents=out.referents.filter(v=>!v.__csnf_reified);
  return out;
 }
 const encoded=pack(data),decoded=unpack(encoded),lossless=signature(decoded)===base;
 const cost={original_bytes:JSON.stringify(data).length,reified_bytes:JSON.stringify(encoded).length,
 core_collection_slots_before:9,core_collection_slots_after:7,extra_discriminators:["__csnf_reified:C8","__csnf_reified:C9"],validator_footprint:"NOT_MEASURED"};
 return {dropTests,losslessRelocation:lossless,cost};
}
function freedomExperiments(){
 const eq=(a,b)=>Math.abs(a-b)<1e-9;
 const soc={capacity_mwh:100,soc_start:0.5,soc_end:0.48,p_grid_mw:2,delta_hours:1};
 const battery=eq((soc.soc_start-soc.soc_end)*soc.capacity_mwh,soc.p_grid_mw*soc.delta_hours)&&eq(50-48,2);
 const individual=[{id:"EV1",demand:1,delivered:1},{id:"EV2",demand:2,delivered:2}];
 const aggregate={total:3,individual_witness:individual};
 const ev=aggregate.individual_witness.every(x=>x.delivered>=x.demand)&&eq(aggregate.individual_witness.reduce((s,x)=>s+x.delivered,0),aggregate.total);
 const theta=[1,0,-1],thetaFlows=[theta[0]-theta[1],theta[1]-theta[2],theta[2]-theta[0]],cycleFlows=[1,1,-2];
 const network=thetaFlows.every((v,i)=>eq(v,cycleFlows[i]))&&eq(cycleFlows.reduce((s,v)=>s+v,0),0);
 const elec={electric_mwh:2,hydrogen_energy_mwh_constant:1.4,hydrogen_energy_mwh_partload:1.36,efficiency_envelope_max:0.8};
 const electrolyser=[elec.hydrogen_energy_mwh_constant,elec.hydrogen_energy_mwh_partload].every(e=>e/elec.electric_mwh<=elec.efficiency_envelope_max)&&!eq(elec.hydrogen_energy_mwh_constant,elec.hydrogen_energy_mwh_partload);
 const investment=(()=>{const shared=5,indexed={"warm":5,"cold":5};return Object.values(indexed).every(v=>v===shared)})();
 return {RC01_battery_SOC_vs_energy:{pass:battery,scope:"one idealized one-hour trace"},
 RC02_EV_individual_vs_aggregate:{pass:ev,scope:"finite departure witness"},
 RC05_angle_vs_cycle:{pass:network,scope:"single 3-node equal-x DC triangle"},
 RC03_electrolyser_const_vs_partload:{pass:electrolyser,scope:"two admissible but non-identical output samples"},
 RC07_investment_shared_vs_scenario_indexed:{pass:investment,scope:"two-scenario first-stage value"}};
}
module.exports={structuralExperiments,freedomExperiments};
