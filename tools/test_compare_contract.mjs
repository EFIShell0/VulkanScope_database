import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const source=fs.readFileSync(new URL('../assets/app.v0395.js',import.meta.url),'utf8');
function extractFunction(name){
  const start=source.indexOf(`function ${name}(`);
  if(start<0)throw new Error(`missing ${name}`);
  const open=source.indexOf('{',start);
  let depth=0,quote=null,escape=false;
  for(let i=open;i<source.length;i++){
    const ch=source[i];
    if(quote){if(escape)escape=false;else if(ch==='\\')escape=true;else if(ch===quote)quote=null;continue}
    if(ch==='"'||ch==="'"||ch==='`'){quote=ch;continue}
    if(ch==='{')depth++;else if(ch==='}'&&--depth===0)return source.slice(start,i+1);
  }
  throw new Error(`unterminated ${name}`);
}
const context={
  hostImageCopyCompareIdentity:(section,name)=>({section,name}),canonicalPropertyValue:(_n,v)=>v,
  formatFlags:v=>String(v??''),bytesLabel:v=>String(v??''),memoryHeapFlags:v=>String(v??''),memoryFlags:v=>String(v??''),
  canonicalQueueFlags:v=>String(v??''),canonicalVideoCodecOperations:v=>String(v??''),queueVideoCodecState:q=>q.videoCodecQueryStatus||'unknown',
  boolState:v=>v===true?'supported':v===false?'unsupported':'unknown',canonicalSurfaceValue:(_k,v)=>String(v??''),semanticStatus:()=> 'available',
  vendorId:r=>r.gpu?.vendorId||'Unknown',reportOs:()=> 'Android',reportPlatform:()=> 'arm64-v8a',formatSubmitted:v=>String(v??'')
};
vm.createContext(context);vm.runInContext(`${extractFunction('compareMap')};this.compareMap=compareMap`,context);
const base={capabilities:[{section:'VULKAN PROFILES',name:'VP_KHR_roadmap_2026 r.1',value:'FAIL old',status:'unsupported'}],profiles:[{name:'VP_KHR_roadmap_2026',revision:'r.2',summary:'UNKNOWN · partial evaluator',status:'unknown'}],extensions:[],instanceExtensions:[],formats:[],memoryHeaps:[],memoryTypes:[],queues:[],surface:{},instanceLayers:[],deviceLayers:[],queryDiagnostics:{},display:{},gpu:{vendorId:'0x5143'},driver:{},vulkan:{},application:{}};
let map=context.compareMap(base);
assert.equal([...map.keys()].some(k=>k.startsWith('VULKAN PROFILES /')),false,'normalized profiles must suppress duplicate legacy compare rows');
assert.equal(map.get('PROFILES / VP_KHR_roadmap_2026')?.value,'rev r.2 · UNKNOWN · partial evaluator','normalized profile name is canonical and revision stays in value');
const legacy={...base,profiles:[]};
map=context.compareMap(legacy);
assert.equal(map.get('PROFILES / VP_KHR_roadmap_2026')?.value,'rev r.1 · FAIL old','legacy profile fallback must canonicalize revision out of row identity');
assert.equal(source.includes('Common evidence only'),true);
assert.equal(source.includes('Cross-producer comparison:'),true);
assert.equal(source.includes('Profile definition revisions differ:'),true);
console.log('VulkanScope Database compare contract tests: ALL PASS');
