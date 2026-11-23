'use strict';
const {structuralExperiments,freedomExperiments}=require('./ablation_and_freedom.js');
const c=require('../frozen/rc01_typed_contract.json');
const a=structuralExperiments(c),f=freedomExperiments();
console.log(JSON.stringify({ablation:a,freedom:f},null,2));
if(!a.dropTests.every(x=>x.detected)||!a.losslessRelocation||!Object.values(f).every(v=>v.pass))process.exitCode=1;
