// Independent synthetic experiments; no candidate or original oracle imports.
function analytical(){
const out=[];const add=(id,pass,details)=>out.push({id,pass,details});
const abs=[],soc=[];for(let e=0;e<=4;e++)for(let c=0;c<=4;c++)for(let d=0;d<=4;d++)if(e+c-d>=0&&e+c-d<=4){abs.push([e,c,d,e+c-d]);soc.push([e/4,c,d,(e+c-d)/4]);}
add("C4-A-STORAGE",JSON.stringify(abs)===JSON.stringify(soc.map(([s,c,d,t])=>[4*s,c,d,4*t])),{count:abs.length,capacity:4,proof:"positive fixed C; map E=C*s bijective; multiply SOC equation by C",negative:"C=0 map undefined; wrong sign violates balance"});
const individual=new Set(),aggregate=new Set();for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){if(x===1)individual.add(`${x},${y}`);if(x+y>=1)aggregate.add(`${x},${y}`)}
add("C4-A-EV",aggregate.has("0,1")&&!individual.has("0,1"),{individual:[...individual],aggregate:[...aggregate],counterexample:[0,1],scope:"EV A must charge in t0 before departure; aggregate energy alone misses deadline"});
const flows=[];for(let a=-3;a<=3;a++)for(let b=-3;b<=3;b++)for(let c=-3;c<=3;c++)if(a-b===0&&b-c===0&&c-a===0)flows.push([a,b,c]);
add("C4-A-KVL",flows.length===7&&flows.filter(f=>f.reduce((x,y)=>x+y,0)===0).length===1,{KCL_only:flows,KCL_KVL:[[0,0,0]],PTDF:[0,0,0],assumptions:"triangle oriented cycle, equal unit reactance, zero injections, no phase shift"});
const integer=[0,2,4],continuous=[0,1,2,3,4];add("C4-A-INVEST",continuous.includes(1)&&!integer.includes(1),{common:"0<=capacity<=4; deliver>=1",discreteOptimum:2,continuousOptimum:1,cost:"unit capex",scope:"explicitly permitted granularity required; E4 false"});
const mass=[0,1,2,3],energy=mass.map(m=>33*m);add("C4-A-H2",energy.every((e,i)=>e===33*mass[i])&&33!==39,{mass,energy,basis:"synthetic 33 kWh/kg LHV; 39 alternate HHV deliberately incompatible",scope:"fixed positive factor; power and mass flow convert with same duration and basis"});
const cand=[{id:"a",eligible:true,cost:5},{id:"b",eligible:true,cost:5},{id:"c",eligible:false,cost:1},{id:"d",eligible:true,cost:6}];const accepted=cand.filter(x=>x.eligible&&cand.filter(y=>y.eligible).every(y=>x.cost<=y.cost)).map(x=>x.id);
add("C4-A-SELECT",JSON.stringify(accepted)==='["a","b"]',{accepted,rejected:["c","d"],scope:"declared complete finite candidate support, no global optimizer"});
const outcomes=[10,14,18,22];const mean=outcomes.reduce((a,b)=>a+b)/4;const variance=outcomes.reduce((a,b)=>a+(b-mean)**2,0)/4;
add("C4-A-SENS",mean===16&&variance===20,{outcomes,mean,variance,scope:"equal weights; no attribution without factorial design"});
return {scope:"INDEPENDENT_SYNTHETIC_ANALYTICAL_PROXIES_NOT_NATIVE_TESTS",tests:out,passed:out.filter(r=>r.pass).length,total:out.length};
}
const result=analytical(); console.log(JSON.stringify(result,null,2)); if(result.passed!==result.total) process.exitCode=1;
