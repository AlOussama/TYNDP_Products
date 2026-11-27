/* Independent original oracle invocation. This process is not imported by the candidate. */
const fs=require("fs"),path=require("path");
const oracle=require(path.resolve(process.argv[2]));
const base=oracle.makeFixture(),results=oracle.runSuite();
if(results.passed!==results.total)throw Error("Frozen original P5 oracle failure");
const rows=oracle.mutations.map(([id,code,edit])=>{
  const record=JSON.parse(JSON.stringify(base));edit(record);
  const observed=oracle.evaluateFixture(record);
  if(!observed.diagnostics.some(x=>x.code===code))throw Error("Frozen mutation replay drift "+id);
  return {id,expected:code,record,observed};
});
fs.writeFileSync(process.argv[3],JSON.stringify({base,base_result:oracle.evaluateFixture(base),mutations:rows,suite:results}));
console.log("C3_P5_ORACLE_REPLAY="+JSON.stringify({identities:rows.length,passed:rows.length,baseline:results.passed,total:results.total}));
