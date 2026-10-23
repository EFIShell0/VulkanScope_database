import fs from 'node:fs';
import path from 'node:path';

const root=path.resolve(process.argv[2]||'.');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const errors=[];
const need=(condition,message)=>{if(!condition)errors.push(message)};
const index=read('index.html');
const appPath='assets/app.v03920.js';
need(fs.existsSync(path.join(root,appPath)),'current frontend asset missing');
need(index.includes('VulkanScope Database <strong>0.39.20</strong>'),'index database version stale');
need(index.includes('./config.js?v=03920'),'config cache key stale');
need(index.includes('./assets/app.v03920.js'),'frontend asset cache key stale');
if(fs.existsSync(path.join(root,appPath))){
  const app=read(appPath);
  need(app.includes('VulkanScope 0.41.45 · Vulkan 1.4.361'),'frontend producer/query baseline stale');
  need(app.includes('Database 0.39.20 · schema'),'frontend footer database version stale');
}
const worker=read('worker/src/index.js');
need(worker.includes("producerQueryBaseline:'VulkanScope 0.41.45 · Vulkan 1.4.361'"),'Worker producer/query baseline stale');
const packageJson=JSON.parse(read('worker/package.json'));
need(packageJson.version==='0.39.20','Worker package version stale');
const buildIndex=read('tools/build_index.py');
need(buildIndex.includes('"databaseVersion":"0.39.20"'),'build_index database version stale');
need(buildIndex.includes('"producerQueryBaseline":"VulkanScope 0.41.45 · Vulkan 1.4.361"'),'build_index producer/query baseline stale');
if(errors.length){for(const error of errors)console.log('FAIL:',error);process.exit(1)}
console.log('PASS VulkanScope Database 0.39.20 producer baseline for VulkanScope 0.41.45');
