"use strict";
// Call the ORIGINAL pinned mutation functions and evaluator. No reimplementation.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),assert=require("assert");
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,"original_diagnostic_contracts.json"),"utf8"));
const source=path.resolve(process.argv[2]);
const bytes=fs.readFileSync(source), hash=crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
const oracle=require(source),rows=manifest.originals.filter(x=>x.family==="P5"),records=[];
assert.strictEqual(rows.length,30);
assert.strictEqual(oracle.mutations.length,30);
for(const [id,expected,edit] of oracle.mutations){
 const row=rows.find(x=>x.id===id);assert(row);assert.strictEqual(row.expected,expected);assert.strictEqual(row.oracle.blob,hash);
 const c=oracle.makeFixture();edit(c);const actual=oracle.evaluateFixture(c);assert.strictEqual(actual.status,"FAIL_STATIC_FRAGMENT");
 assert(actual.diagnostics.some(x=>x.code===expected));assert(actual.diagnostics.every(x=>typeof x.path==="string"&&x.path.startsWith("$")));
 records.push({id,original_expected:expected,rule_id:row.rule_id,rule_source:manifest.rule_source,source:row.oracle,path_kind:"ACTUAL_ORIGINAL_MICRO_ORACLE_JSONPATH",diagnostics:actual.diagnostics,candidate_path:null,full_path:"NOT_EXECUTED"});
}
console.log("C2_FINAL_P5_DIAGNOSTICS="+JSON.stringify(records));
