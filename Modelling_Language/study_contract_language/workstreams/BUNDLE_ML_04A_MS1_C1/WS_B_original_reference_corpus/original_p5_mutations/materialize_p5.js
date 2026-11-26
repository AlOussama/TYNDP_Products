"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const pinned=path.join(__dirname,"original_cba_stress_oracle.js");
const bytes=fs.readFileSync(pinned),blob=crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
if(blob!=="ef2c7fa4ea4deab919f0c84ac7020aa1a32ff0a2")throw Error("P5_BLOB");
const orig=require(pinned),manifest=require("../frozen/p5_negative_case_manifest.json");
const suite=orig.runSuite(),out=process.argv[2];
if(!out)throw Error("Output directory required");
fs.mkdirSync(out,{recursive:true});
for(const [id,code,edit] of orig.mutations){
 const expected=manifest.find(m=>m.id===id);if(!expected||expected.expected_diagnostic!==code)throw Error(id);
 const c=orig.makeFixture();edit(c);
 fs.writeFileSync(path.join(out,id+".json"),JSON.stringify({id,original_expected:code,fixture:c,actual:orig.evaluateFixture(c)},null,2)+"\n");
}
fs.writeFileSync(path.join(out,"original_p5_oracle_results.json"),JSON.stringify(suite,null,2)+"\n");
console.log("P5_ORIGINAL="+JSON.stringify(suite));
if(suite.negative.length!==30||suite.positive.length!==6||suite.passed!==36||suite.total!==36)process.exit(1);
