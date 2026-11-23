'use strict';
const {assessRegistry}=require('./mapping_registry_checks.js');
const registry=require('../frozen/mapping_registry.json');
const r=assessRegistry(registry);if(r.failures.length)throw Error(JSON.stringify(r));
const bad=JSON.parse(JSON.stringify(registry));bad.roles=bad.roles.filter(x=>x.role!=='C9');
if(!assessRegistry(bad).failures.includes('MISSING_C9'))throw Error('Negative C9 ablation not detected');
console.log(JSON.stringify({positive:r,negative:assessRegistry(bad)},null,2));
