'use strict';
const {runSuite}=require('./cba_stress_oracle.js');
const r=runSuite();
console.log(JSON.stringify({run_id:r.run_id,passed:r.passed,total:r.total,positive:r.positive,negative:r.negative,baseline:r.baseline},null,2));
if(r.passed!==r.total)process.exitCode=1;
