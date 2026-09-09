import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const workerRoot=path.resolve(here,'..');
const wantWrangler='4.130.0';
const wantSharp='0.35.4';

function fail(message){
  console.error(`FAIL security audit preflight: ${message}`);
  process.exit(1);
}
function npmCli(){
  const fromRun=process.env.npm_execpath;
  if(fromRun && fs.existsSync(fromRun)) return fromRun;
  const adjacent=path.join(path.dirname(process.execPath),'node_modules','npm','bin','npm-cli.js');
  if(fs.existsSync(adjacent)) return adjacent;
  fail('npm CLI JavaScript entry point is unavailable; invoke this check with `npm run security:audit`');
}
function runNpm(args){
  // Do not spawn npm.cmd directly. On Windows/Node combinations that can fail with
  // spawnSync EINVAL. Running npm-cli.js through the current node executable is
  // shell-free, preserves argv boundaries, and is portable across Windows/Linux.
  const cli=npmCli();
  const r=spawnSync(process.execPath,[cli,...args],{
    cwd:workerRoot,
    stdio:'inherit',
    env:{...process.env}
  });
  if(r.error) fail(`node ${cli} ${args.join(' ')} could not start: ${r.error.message}`);
  if(r.status!==0) process.exit(r.status ?? 1);
}
function jsonFile(name){
  try{return JSON.parse(fs.readFileSync(path.join(workerRoot,name),'utf8'));}
  catch(e){fail(`${name} is missing or invalid JSON: ${e.message}`);}
}

const pkg=jsonFile('package.json');
if(pkg?.devDependencies?.wrangler!==wantWrangler) fail(`worker/package.json must pin wrangler exactly ${wantWrangler}`);
if(pkg?.overrides?.sharp!==wantSharp) fail(`worker/package.json must override sharp exactly ${wantSharp}`);

const lockPath=path.join(workerRoot,'package-lock.json');
if(!fs.existsSync(lockPath)){
  runNpm(['install','--package-lock-only','--ignore-scripts','--no-audit','--no-fund']);
}
const lock=jsonFile('package-lock.json');
if(Number(lock.lockfileVersion||0)<2) fail('package-lock.json lockfileVersion must be >= 2');
const packages=lock.packages||{};
const rootPkg=packages['']||{};
if(rootPkg?.devDependencies?.wrangler!==wantWrangler) fail(`audit lock root wrangler pin must be ${wantWrangler}`);
const wr=packages['node_modules/wrangler']||{};
if(wr.version!==wantWrangler || !wr.integrity) fail(`audit lock must resolve wrangler ${wantWrangler} with integrity metadata`);
const sharp=packages['node_modules/sharp']||{};
if(sharp.version!==wantSharp || !sharp.integrity) fail(`audit lock must resolve patched sharp ${wantSharp} with integrity metadata`);

console.log(`PASS security audit lock: wrangler=${wantWrangler} sharp=${wantSharp} lockfileVersion=${lock.lockfileVersion}`);
runNpm(['audit','--audit-level=high']);
