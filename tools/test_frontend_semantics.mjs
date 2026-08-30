import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const source=fs.readFileSync(new URL('../assets/app.v03912.js',import.meta.url),'utf8');

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

function declarationLine(prefix){
  const line=source.split(/\r?\n/).find(x=>x.startsWith(prefix));
  if(!line)throw new Error(`missing declaration ${prefix}`);
  return line;
}

const statusLine=declarationLine('const semanticStatus=');
const statusHelpers=statusLine.slice(0,statusLine.indexOf(';const compareEvidenceStatus=')+1);
const displayHelpers=[
  declarationLine('const displayWideGamutState='),
  declarationLine('const displayValueState='),
  declarationLine('const displayValueLabel='),
  declarationLine('const displayModesState=')
].join('\n');
const context={};
vm.createContext(context);
vm.runInContext(`${statusHelpers}\n${displayHelpers}\n${declarationLine('const bytesLabel=')}\n${extractFunction('applyStructuredTechnicalReport')}\nthis.api={availabilityStatus,displayWideGamutState,displayValueState,displayValueLabel,displayModesState,bytesLabel,applyStructuredTechnicalReport};`,context);
const api=context.api;

const report={
  gpu:{name:'Fixture GPU'},
  capabilities:[
    {section:'FEATURES',name:'staleFeature',value:'true',status:'supported'},
    {section:'VkPhysicalDeviceExampleProperties',name:'staleProperty',value:'false',status:'available'},
    {section:'LIMITS',name:'staleLimit',value:'0',status:'available'},
    {section:'DEVICE',name:'Driver mode',value:'System Vulkan driver',status:'available'}
  ],
  detailedProperties:[{section:'VkPhysicalDeviceExampleProperties',name:'staleProperty',value:'false',status:'available'}],
  limits:[{section:'LIMITS',name:'staleLimit',value:'0',status:'available'}],
  technicalReport:{schemaVersion:3,devices:[{name:'Fixture GPU',features:[],detailedProperties:[],limits:[]}]}
};
api.applyStructuredTechnicalReport(report);
assert.equal(report.capabilities.some(x=>x.name==='staleFeature'),false,'empty structured features must clear TXT fallback feature evidence');
assert.equal(report.capabilities.some(x=>x.name==='staleProperty'),false,'empty structured detailedProperties must clear TXT fallback property evidence');
assert.equal(report.capabilities.some(x=>x.name==='staleLimit'),false,'empty structured limits must clear TXT fallback limit evidence');
assert.equal(report.capabilities.some(x=>x.section==='DEVICE'),true,'unrelated compatibility metadata must remain accessible');

const structured={
  gpu:{name:'Fixture GPU'},capabilities:[],detailedProperties:[],limits:[],
  technicalReport:{schemaVersion:3,devices:[{name:'Fixture GPU',features:[{name:'featureFalse',supported:false}],detailedProperties:[{section:'VkPhysicalDeviceExampleProperties',name:'propertyFalse',value:false}],limits:[{name:'zeroLimit',value:0}]}]}
};
api.applyStructuredTechnicalReport(structured);
assert.equal(structured.capabilities.find(x=>x.name==='featureFalse')?.status,'unsupported','feature false remains direct Unsupported evidence');
assert.equal(structured.detailedProperties.find(x=>x.name==='propertyFalse')?.status,'available','generic false property remains query-available');
assert.equal(structured.limits.find(x=>x.name==='zeroLimit')?.status,'available','zero limit remains query-available');

assert.equal(api.displayValueState(undefined),'unknown','missing display evidence must remain Unknown');
assert.equal(api.displayValueLabel(undefined),'Unknown');
assert.equal(api.displayValueState(null),'unavailable','explicit null display evidence is Unavailable');
assert.equal(api.displayModesState({}),'unknown','missing display-mode list must remain Unknown');
assert.equal(api.displayModesState({modes:[]}),'unavailable','explicitly empty display-mode list is Unavailable');
assert.equal(api.displayWideGamutState({}),'unknown','missing wide-gamut evidence must remain Unknown');

const maxU64='18446744073709551615';
const memoryLabel=api.bytesLabel(maxU64);
assert.match(memoryLabel,/18,446,744,073,709,551,615 B|18\.446\.744\.073\.709\.551\.615 B|18446744073709551615 B/,'exact U64 byte value must remain visible without Number rounding');

const searchProjectionLine=declarationLine('const reportSearchCache=');
assert.equal(searchProjectionLine.includes('reportText'),false,'search cache must not duplicate raw reportText');
assert.equal(searchProjectionLine.includes('technicalReport:r'),false,'search cache must not duplicate structured technicalReport payloads');
assert.equal(source.includes('queue.shift()'),false,'bounded report loader must avoid quadratic Array.shift work');
assert.equal(source.includes("availabilityStatus(v));for(const [i,x] of (s.formats"),true,'Compare must treat generic Surface values as availability evidence');

console.log('VulkanScope Database frontend normalization semantics: ALL PASS');
