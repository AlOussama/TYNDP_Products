function exactFormulations(){
  const storageE=[],storageS=[];const C=4;
  for(let e=0;e<=4;e++)for(let ch=0;ch<=2;ch++)for(let dis=0;dis<=2;dis++)for(let z=0;z<=4;z++)if(z===e+ch-dis)storageE.push([e,ch,dis,z].join(","));
  for(let s=0;s<=4;s++)for(let ch=0;ch<=2;ch++)for(let dis=0;dis<=2;dis++)for(let t=0;t<=4;t++)if(t/4===s/4+ch/4-dis/4)storageS.push([C*s/4,ch,dis,C*t/4].join(","));
  // Equal b=1 on triangle orientation (0->1,1->2,2->0).
  // For injections p0,p1,p2, reference theta2=0: theta0=(2p0+p1)/3; theta1=(p0+2p1)/3.
  const network=[];for(let p0=-2;p0<=2;p0++)for(let p1=-2;p1<=2;p1++){const p2=-p0-p1;const a=2*p0+p1,b=p0+2*p1;const fAngle=[a-b,b,-a];const fPTDF=[p0-p1,p1-p2,p2-p0];const balance=[fAngle[0]-fAngle[2],fAngle[1]-fAngle[0],fAngle[2]-fAngle[1]];network.push({injections:[p0,p1,p2],flows_scaled_by_3:fAngle,ptdf_scaled_by_3:fPTDF,match:JSON.stringify(fAngle)===JSON.stringify(fPTDF)&&JSON.stringify(balance)===JSON.stringify([3*p0,3*p1,3*p2]),line_limit_equal:(fAngle.every(x=>Math.abs(x)<=3)===fPTDF.every(x=>Math.abs(x)<=3))});}
  // Independently enumerate feasible individual schedules; aggregate feasible schedules have existential allocation.
  const individual=new Set(),aggregateEnvelope=new Set();for(let x00=0;x00<=1;x00++)for(let x01=0;x01<=1;x01++)for(let x10=0;x10<=1;x10++)for(let x11=0;x11<=1;x11++){if(x00===1&&x01===0&&x10+x11===1)individual.add(`${x00+x10},${x01+x11}`);}
  for(let a=0;a<=2;a++)for(let b=0;b<=2;b++)if(a+b===2)aggregateEnvelope.add(`${a},${b}`);
  const results={storage:{scope:"integer MWh grid, C=4 MWh, fixed 1h, eta=1; objective 2ch+3dis invariant",absolute:storageE.length,soc:storageS.length,same:JSON.stringify(storageE)===JSON.stringify(storageS),charge_negative_control:3+2>4},network:{scope:"lossless DC equal b=1, fixed triangle, balanced injections, reference angle theta2=0, flows represented exactly as integer numerator/3, line capacity 1",injection_cases:network.length,matches:network.filter(x=>x.match&&x.line_limit_equal).length,feasible:network.filter(x=>x.flows_scaled_by_3.every(f=>Math.abs(f)<=3)).length,rows:network},ev:{scope:"EV1 requires unit by t0, EV2 by t1, both charging power max 1, total 2",projected:[...individual].sort(),unconstrained_aggregate:[...aggregateEnvelope].sort(),invalid:[...aggregateEnvelope].filter(x=>!individual.has(x)).sort()}};
  results.pass=results.storage.same&&results.network.matches===25&&results.ev.invalid.includes("0,2");return results;
}
const result=exactFormulations();console.log(JSON.stringify(result,null,2));if(!result.pass)process.exitCode=1;
