import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const root=path.resolve('.');
const verifier=path.join(root,'tools/test_producer_baseline_04146.mjs');
const copyFiles=['index.html','assets/app.v03926.js','worker/src/index.js','worker/package.json','tools/build_index.py'];
const runMutation=(relative,from,to,label)=>{
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'vulkanscope-db-03919-negative-'));
  try{
    for(const rel of copyFiles){const dst=path.join(temp,rel);fs.mkdirSync(path.dirname(dst),{recursive:true});fs.copyFileSync(path.join(root,rel),dst)}
    const target=path.join(temp,relative); const text=fs.readFileSync(target,'utf8');
    if(!text.includes(from))throw new Error(`mutation source missing: ${label}`);
    fs.writeFileSync(target,text.split(from).join(to),'utf8');
    const result=spawnSync(process.execPath,[verifier,temp],{encoding:'utf8'});
    if(result.status===0)throw new Error(`mutation was not rejected: ${label}`);
  }finally{fs.rmSync(temp,{recursive:true,force:true})}
};
runMutation('assets/app.v03926.js','VulkanScope 0.80.12 · Vulkan 1.4.362','VulkanScope 0.80.7 · Vulkan 1.4.361','frontend-producer-baseline');
runMutation('worker/src/index.js',"producerQueryBaseline:'VulkanScope 0.80.12 · Vulkan 1.4.362'","producerQueryBaseline:'VulkanScope 0.80.7 · Vulkan 1.4.361'",'worker-producer-baseline');
runMutation('index.html','./assets/app.v03926.js','./assets/app.v03918.js','frontend-asset-version');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'vulkanscope-db-03919-control-'));
try{
  for(const rel of copyFiles){const dst=path.join(temp,rel);fs.mkdirSync(path.dirname(dst),{recursive:true});fs.copyFileSync(path.join(root,rel),dst)}
  const target=path.join(temp,'tools/build_index.py'); const text=fs.readFileSync(target,'utf8');
  fs.writeFileSync(target,text.replace('generatedAt','generatedAt'),'utf8');
  const result=spawnSync(process.execPath,[verifier,temp],{encoding:'utf8'});
  if(result.status!==0)throw new Error('unrelated generated timestamp false-positive control');
}finally{fs.rmSync(temp,{recursive:true,force:true})}
console.log('PASS VulkanScope Database 0.39.26 producer-baseline negative mutations');
