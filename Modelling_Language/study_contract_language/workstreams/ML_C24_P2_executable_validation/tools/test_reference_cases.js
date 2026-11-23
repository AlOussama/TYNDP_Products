'use strict';
const {runCases}=require('./reference_case_oracles.js');
const frozen=require('../frozen/mutation_cases.json');
if(frozen.oracle_version!=='ML-C23/research-r0.1')throw Error('Unexpected oracle version');
const r=runCases(frozen.cases);console.log(JSON.stringify(r,null,2));if(r.passed!==28||r.total!==28)process.exitCode=1;
