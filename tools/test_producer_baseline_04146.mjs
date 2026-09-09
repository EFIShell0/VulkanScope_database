import fs from 'node:fs';
import path from 'node:path';

const root=path.resolve(process.argv[2]||'.');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const errors=[];
const need=(condition,message)=>{if(!condition)errors.push(message)};
const index=read('index.html');
const appPath='assets/app.v1005.js';
need(fs.existsSync(path.join(root,appPath)),'current frontend asset missing');
need(index.includes('VulkanScope Database <strong>1.0.5</strong>'),'index database version stale');
need(index.includes('./config.js?v=1005'),'config cache key stale');
need(index.includes('./assets/app.v1005.js'),'frontend asset cache key stale');
if(fs.existsSync(path.join(root,appPath))){
  const app=read(appPath);
  need(app.includes('VulkanScope 1.0.15 · Vulkan 1.4.362'),'frontend producer/query baseline stale');
  need(app.includes('Database 1.0.5 · schema'),'frontend footer database version stale');
}
const worker=read('worker/src/index.js');
need(worker.includes("producerQueryBaseline:'VulkanScope 1.0.15 · Vulkan 1.4.362'"),'Worker producer/query baseline stale');
const packageJson=JSON.parse(read('worker/package.json'));
need(packageJson.version==='1.0.5','Worker package version stale');
const buildIndex=read('tools/build_index.py');
need(buildIndex.includes('"databaseVersion":"1.0.5"'),'build_index database version stale');
need(buildIndex.includes('"producerQueryBaseline":"VulkanScope 1.0.15 · Vulkan 1.4.362"'),'build_index producer/query baseline stale');
if(errors.length){for(const error of errors)console.log('FAIL:',error);process.exit(1)}
console.log('PASS retained 0.41.46 producer-baseline surface on Database 1.0.5');
