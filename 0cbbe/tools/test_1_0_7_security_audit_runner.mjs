import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const helper=fs.readFileSync(path.join(root,'worker','scripts','security-audit.mjs'),'utf8');
const pkg=fs.readFileSync(path.join(root,'worker','package.json'),'utf8');

const lock=()=>({
  name:'vulkanscope-database-worker',
  lockfileVersion:3,
  packages:{
    '':{name:'vulkanscope-database-worker',devDependencies:{wrangler:'4.130.0'}},
    'node_modules/wrangler':{version:'4.130.0',integrity:'sha512-test-wrangler-integrity'},
    'node_modules/sharp':{version:'0.35.4',integrity:'sha512-test-sharp-integrity'}
  }
});

function runCase(existingLock){
  const base=fs.mkdtempSync(path.join(os.tmpdir(),'vsdb107-audit-runner-'));
  try{
    const worker=path.join(base,'worker');
    const scripts=path.join(worker,'scripts');
    fs.mkdirSync(scripts,{recursive:true});
    fs.writeFileSync(path.join(worker,'package.json'),pkg);
    fs.writeFileSync(path.join(scripts,'security-audit.mjs'),helper);
    if(existingLock) fs.writeFileSync(path.join(worker,'package-lock.json'),JSON.stringify(lock()));
    const calls=path.join(base,'calls.jsonl');
    const fake=path.join(base,'fake-npm-cli.mjs');
    fs.writeFileSync(fake,`import fs from 'node:fs';\nimport path from 'node:path';\nconst args=process.argv.slice(2);\nfs.appendFileSync(${JSON.stringify(calls)},JSON.stringify(args)+'\\n');\nif(args[0]==='install'){const lock=${JSON.stringify(lock())};fs.writeFileSync(path.join(process.cwd(),'package-lock.json'),JSON.stringify(lock));}\nprocess.exit(0);\n`);
    const env={...process.env,npm_execpath:fake};
    const r=spawnSync(process.execPath,[path.join(scripts,'security-audit.mjs')],{cwd:worker,env,encoding:'utf8'});
    if(r.status!==0) throw new Error(`security audit helper failed: ${r.stdout}\n${r.stderr}`);
    const seen=fs.readFileSync(calls,'utf8').trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
    const audit=['audit','--audit-level=high'];
    if(JSON.stringify(seen.at(-1))!==JSON.stringify(audit)) throw new Error(`audit argv drift: ${JSON.stringify(seen)}`);
    if(existingLock){
      if(seen.length!==1) throw new Error(`existing lock must be reused, calls=${JSON.stringify(seen)}`);
    }else{
      const install=['install','--package-lock-only','--ignore-scripts','--no-audit','--no-fund'];
      if(seen.length!==2 || JSON.stringify(seen[0])!==JSON.stringify(install)) throw new Error(`missing-lock bootstrap argv drift: ${JSON.stringify(seen)}`);
    }
  } finally {
    fs.rmSync(base,{recursive:true,force:true});
  }
}

runCase(true);
runCase(false);
console.log('PASS Database 1.0.7 security-audit npm-cli runner / existing+missing lock state machine');
