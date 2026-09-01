import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const verifier=path.join(root,'tools','test_compare_04141_compat.mjs');
const source=fs.readFileSync(path.join(root,'assets','app.v03916.js'),'utf8');
function run(candidate){const dir=fs.mkdtempSync(path.join(os.tmpdir(),'vulkanscope-db-03916-'));try{fs.mkdirSync(path.join(dir,'assets'));fs.writeFileSync(path.join(dir,'assets','app.v03916.js'),candidate);return spawnSync(process.execPath,[verifier,dir],{encoding:'utf8'}).status??1}finally{fs.rmSync(dir,{recursive:true,force:true})}}
function failMutation(oldValue,newValue,label){if(!source.includes(oldValue))throw new Error(`mutation source missing: ${label}`);if(run(source.replace(oldValue,newValue))===0)throw new Error(`mutation was not rejected: ${label}`)}
failMutation("if(!producerBefore04140(r)||s!=='FEATURES'", "if(s!=='FEATURES'", 'producer-version-bound');
failMutation("/^(VkPhysicalDevice[A-Za-z0-9_]*Properties[A-Za-z0-9_]*) · (.+)$/", "/^(VkPhysicalDevice[A-Za-z0-9_]*) · (.+)$/", 'property-struct-identity');
failMutation("const visibleMetricLabel=diff?'Visible differences':'Visible fields'", "const visibleMetricLabel='Visible differences'", 'visible-metric-semantics');
const harmless=source.replace('Cross-producer comparison:', 'Cross-version producer comparison:');
if(run(harmless)!==0)throw new Error('unrelated notice text false-positive control');
console.log('PASS Database 0.39.16 Compare negative mutation gate');
