import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const source=fs.readFileSync(new URL('../assets/app.v0398.js',import.meta.url),'utf8');
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
vm.createContext(context);
const helperStart=source.indexOf('const compareEvidenceStatus=');
const helperEnd=source.indexOf(';const boolState=',helperStart);
if(helperStart<0||helperEnd<0)throw new Error('missing compareEvidenceStatus');
vm.runInContext(`${source.slice(helperStart,helperEnd)};${extractFunction('compareMap')};this.compareMap=compareMap`,context);
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

const imageOld={capabilities:[{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'tiling=LINEAR, extent=1 × 1 × 1',status:'available'}],profiles:[]};
const imageNew={capabilities:[{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED',status:'available'}],profiles:[]};
const oldImage=context.compareMap(imageOld).get('Image Format Properties2 / VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER');
const newImage=context.compareMap(imageNew).get('Image Format Properties2 / VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER');
assert.equal(oldImage.status,'available');
assert.equal(newImage.status,'unsupported');
assert.equal(newImage.value,'Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED');


const imageUnavailable={capabilities:[{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',value:'Unavailable: VkResult=-1',status:'available'}],profiles:[]};
const unavailableImage=context.compareMap(imageUnavailable).get('Image Format Properties2 / VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER');
assert.equal(unavailableImage.status,'unavailable');
assert.equal(unavailableImage.value,'Unavailable: VkResult=-1');


const imageSeparated={capabilities:[],imageFormatQueryResults:[{name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unsupported',vkResult:-11}],profiles:[]};
const separatedImage=context.compareMap(imageSeparated).get('Image Format Properties2 / VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER');
assert.equal(separatedImage.status,'unsupported');
assert.equal(separatedImage.value,'VK_ERROR_FORMAT_NOT_SUPPORTED');
const imageSeparatedUnavailable={capabilities:[],imageFormatQueryResults:[{name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:-1}],profiles:[]};
const separatedUnavailable=context.compareMap(imageSeparatedUnavailable).get('Image Format Properties2 / VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER');
assert.equal(separatedUnavailable.status,'unavailable');
assert.equal(separatedUnavailable.value,'VkResult=-1');

const imageCompleteAvailable={capabilities:[{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'tiling=LINEAR, extent=16384 × 16384 × 1, externalHandle=ANDROID_HARDWARE_BUFFER',status:'available'}],imageFormatQueryResults:[{name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'available',vkResult:0,reason:''}],profiles:[]};
const completeAvailable=context.compareMap(imageCompleteAvailable).get('Image Format Properties2 / VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER');
assert.equal(completeAvailable.status,'available');
assert.match(completeAvailable.value,/extent=16384/,'0.41.10 Available ledger row must not overwrite the full successful property payload');
const imageNotApplicable={capabilities:[],imageFormatQueryResults:[{name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',status:'not_applicable',vkResult:null,reason:'VK_ANDROID_external_memory_android_hardware_buffer was not enumerated for this device.'}],profiles:[]};
const notApplicableImage=context.compareMap(imageNotApplicable).get('Image Format Properties2 / VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER');
assert.equal(notApplicableImage.status,'not_applicable');
assert.equal(notApplicableImage.value,'VK_ANDROID_external_memory_android_hardware_buffer was not enumerated for this device.');
assert.equal(source.includes('complete tuple-state ledger is excluded from Properties & Limits totals'),true,'Formats detail must explain separated outcome accounting');
console.log('VulkanScope Database compare contract tests: ALL PASS');
