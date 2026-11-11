#!/usr/bin/env node
// ML-R03 non-normative synthetic-only checks; Node.js 18+; no external dependencies
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const here=dirname(fileURLToPath(import.meta.url));
function validateContract(o){
  const err=[],assert=(ok,code)=>{if(!ok)err.push(code)};
  if(!o || typeof o!=="object")return ["ROOT_NOT_OBJECT"];
  assert(o.schema_version==="MLR03-SYN-0.1","SCHEMA_VERSION");
  assert(o.mode==="SYNTHETIC_TEST_ONLY"||o.mode==="PRODUCTION","MODE_UNKNOWN");
  const yrs=[2035,2040,2050],cs=["CY1","CY2","CY3","CY4","CY5"];
  const arr=x=>Array.isArray(x)?x:[];
  const def=new Set(arr(o.definitions)),spec=new Set(arr(o.transformation_spec_ids));
  const sy=arr(o.study_years);assert(sy.length===3&&yrs.every(y=>sy.includes(y))&&new Set(sy).size===3,"STUDY_YEARS");
  const ww=arr(o.weather_cases);const vector={};
  for(const y of yrs){const set=ww.filter(w=>w.study_year===y);assert(set.length===5&&set.every(w=>cs.includes(w.case_id))&&new Set(set.map(w=>w.case_id)).size===5&&cs.every(c=>set.some(w=>w.case_id===c)),"WEATHER_CASES_"+y);
    vector[y]=Object.fromEntries(set.map(w=>[w.case_id,w.weight]));
    for(const w of set){assert(typeof w.profile_ref==="string"&&w.profile_ref.length>0,"WEATHER_PROFILE_REF");
      assert(typeof w.weight==="number"&&Number.isFinite(w.weight)&&w.weight>=0,"WEATHER_WEIGHT_NUMERIC");}
    assert(set.length===5&&set.every(w=>Number.isFinite(w.weight))&&Math.abs(set.reduce((a,w)=>a+w.weight,0)-1)<1e-10,"SYNTHETIC_WEIGHT_SUM_"+y);
  }
  assert(ww.length===15,"WEATHER_RECORD_COUNT");
  for(const c of cs)assert(yrs.every(y=>typeof vector[y][c]==="number"&&Math.abs(vector[y][c]-vector[yrs[0]][c])<1e-12),"WEIGHT_SHARED_"+c);
  const releases=arr(o.releases),runs=arr(o.runs),inst=arr(o.data_instances),trans=arr(o.transformations),raw=arr(o.raw_outputs);
  const relIds=new Set(releases.map(x=>x.release_id)),runIds=new Set(runs.map(x=>x.run_id)),instIds=new Set(inst.map(x=>x.instance_id)),transIds=new Set(trans.map(x=>x.transformation_id));
  const unique=a=>new Set(a).size===a.length;
  assert(unique([...relIds])&&unique(releases.map(x=>x.release_id)),"RELEASE_ID_DUPLICATE");
  assert(unique(runs.map(x=>x.run_id)),"RUN_ID_DUPLICATE");assert(unique(inst.map(x=>x.instance_id)),"INSTANCE_ID_DUPLICATE");
  assert(unique(trans.map(x=>x.transformation_id)),"TRANSFORM_ID_DUPLICATE");
  for(const r of releases){assert(typeof r.source_id==="string"&&r.source_id.length>0,"SOURCE_ID_REQUIRED");
    if(o.mode==="PRODUCTION")assert(r.qualification_status==="SOURCE_QUALIFIED"&&/^[a-f0-9]{64}$/.test(r.original_sha256||""),"REAL_SOURCE_NOT_QUALIFIED");}
  for(const r of runs){assert(yrs.includes(r.study_year),"RUN_STUDY_YEAR");}
  const units={MW:"power",GW:"power",MWh:"energy",GWh:"energy",kg_H2:"mass"};
  const intv={};
  for(const d of inst){
    assert(def.has(d.object_id),"DATA_DEFINITION_FK");
    assert(yrs.includes(d.study_year)&&cs.includes(d.case_id),"DATA_AXES");
    assert(units[d.unit]===d.dimension,"UNIT_DIMENSION");
    assert(typeof d.value==="number"&&Number.isFinite(d.value),"VALUE_NOT_FINITE");
    assert(typeof d.zone_id==="string"&&d.zone_id.length>0&&typeof d.carrier==="string"&&d.carrier.length>0,"SPATIAL_CARRIER_ID");
    const timePattern=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
    assert(timePattern.test(d.start_utc||"")&&timePattern.test(d.end_utc||""),"TIME_NOT_UTC_Z");
    const st=Date.parse(d.start_utc||""),en=Date.parse(d.end_utc||"");
    assert(Number.isFinite(st)&&Number.isFinite(en)&&en>st,"INTERVAL_INVALID");
    const key=[d.object_id,d.study_year,d.case_id,d.zone_id,d.carrier,d.series_key].join("|");
    (intv[key]??=[]).push([st,en]);
    assert(d.provenance&&Array.isArray(d.provenance.source_instance_ids),"PROVENANCE_MISSING");
    if(d.role==="SOURCE_INPUT"){
      assert(relIds.has(d.release_id),"SOURCE_RELEASE_FK");
      assert(d.provenance?.transformation_id===null,"SOURCE_TRANSFORM_UNEXPECTED");
    }else if(d.role==="INTERNAL_DERIVED"){
      assert(runIds.has(d.run_id),"DERIVED_RUN_FK");
      assert(transIds.has(d.provenance?.transformation_id),"DERIVED_TRANSFORM_FK");
      assert(arr(d.provenance?.source_instance_ids).length>0&&arr(d.provenance?.source_instance_ids).every(x=>instIds.has(x)),"DERIVED_SOURCE_INSTANCE_FK");
      assert(d.instance_id!==d.provenance?.source_instance_ids?.[0],"SELF_LINEAGE");
    }else err.push("INSTANCE_ROLE_UNKNOWN");
  }
  for(const intervals of Object.values(intv)){
    intervals.sort((a,b)=>a[0]-b[0]);
    for(let i=1;i<intervals.length;i++)assert(intervals[i][0]>=intervals[i-1][1],"TIME_INTERVAL_OVERLAP");
  }
  for(const t of trans){
    assert(spec.has(t.spec_ref),"TRANSFORMATION_SPEC_FK");
    assert(runIds.has(t.run_id),"TRANSFORMATION_RUN_FK");
    assert(arr(t.input_instance_ids).length>0&&arr(t.output_instance_ids).length>0,"TRANSFORM_IO_MISSING");
    assert(arr(t.input_instance_ids).every(x=>instIds.has(x))&&arr(t.output_instance_ids).every(x=>instIds.has(x)),"TRANSFORMATION_INSTANCE_FK");
    for(const id of arr(t.output_instance_ids)){let oinst=inst.find(i=>i.instance_id===id);
      assert(oinst?.provenance?.transformation_id===t.transformation_id,"OUTPUT_LINEAGE_INCONSISTENT");}
  }
  for(const r of raw){
    assert(runIds.has(r.run_id),"RAW_RUN_FK");
    assert(units[r.unit]!==undefined&&typeof r.value==="number"&&Number.isFinite(r.value),"RAW_UNIT_VALUE");
    assert(r.status==="SYNTHETIC_RAW_NOT_A_KPI"||o.mode==="PRODUCTION","RAW_KPI_CONFLATION");
  }
  if(o.mode==="SYNTHETIC_TEST_ONLY"){
    assert(o.publishable===false&&o.gate_status==="RELEASE_BLOCKED","SYNTHETIC_RELEASE_FORBIDDEN");
    assert(releases.every(r=>r.original_sha256===null&&r.qualification_status==="SYNTHETIC_NO_ORIGINAL_BYTES"),"SYNTHETIC_SOURCE_CLAIM");
  } else {
    assert(o.gate_status==="RELEASE_AUTHORIZED"&&o.publishable===true,"PRODUCTION_GATE_NOT_AUTHORIZED");
    assert(releases.every(r=>r.qualification_status==="SOURCE_QUALIFIED"),"PRODUCTION_SOURCE_APPROVAL");
  }
  return [...new Set(err)];
}
const read=name=>JSON.parse(readFileSync(join(here,name),"utf8"));
const valid=read("valid_synthetic_fixture.json"),failures=[];
const errors=validateContract(valid);
if(errors.length)failures.push({test:"valid_synthetic_fixture",errors});
const badFiles=["invalid_weight_mismatch.json","invalid_missing_weather_case.json","invalid_non_utc_offset.json","invalid_overlap.json","invalid_missing_source_release.json","invalid_unit_dimension.json","invalid_missing_provenance.json","invalid_production_unqualified.json","invalid_data_definition.json","invalid_duplicate_instance_id.json","invalid_missing_derived_run.json","invalid_transform_reference.json","invalid_missing_numeric_weight.json","invalid_synthetic_release_claim.json"];
for(const name of badFiles){
  const errors=validateContract(read(name));
  if(!errors.length)failures.push({test:name,errors:["UNEXPECTED_ACCEPT"]});
}
const results={test_type:"TECHNICAL_SYNTHETIC_ONLY",tests:1+badFiles.length,passed:1+badFiles.length-failures.length,failed:failures.length,failures};
console.log(JSON.stringify(results,null,2));
if(failures.length)process.exitCode=1;
