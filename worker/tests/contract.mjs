import worker, { normalizeReport } from '../src/index.js';
import assert from 'node:assert/strict';

class DB {
  prepare(sql) {
    return {
      bind: (...args) => ({
        run: async () => ({ success: true }),
        first: async () => sql.includes('SELECT submitted_at') ? ({ submitted_at: '2026-08-21T09:00:00.000Z' }) : null,
        all: async () => ({ results: [] }),
      }),
    };
  }
}
const env={DB:new DB(),ALLOWED_ORIGIN:'https://efishell0.github.io'};
const reportText=(p)=>{
  const lines=[
    'VulkanScope report','=================','Application: VulkanScope',
    `Application version: ${p.application.version}`,
    `Application version code: ${p.application.versionCode}`,
    'Application package: com.efishell.vulkanscope',
    `GPU: ${p.gpu.name}`,
    `Driver mode: ${p.driver.mode}`,
    `Loader / instance API: ${p.vulkan.loaderInstanceApiVersion}`,
    '', 'VULKAN REGISTRY COVERAGE','Baseline=1.4.360','',
    'INSTANCE EXTENSIONS','VK_KHR_surface | spec 25','',
    'VULKAN PROFILE EVALUATION','VP_KHR_roadmap_2024 | 1 | UNKNOWN | fixture','',
    `DEVICE #1: ${p.gpu.name}`,'API: 1.4.0','',
    'FEATURES','robustBufferAccess = true','',
    'IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (0 non-success tuples; excluded from property/query totals)','',
    'LIMITS','maxImageDimension2D = 16384','',
    'FORMATS','VK_FORMAT_R8G8B8A8_UNORM: SUPPORTED, linear=1, optimal=1, buffer=1','',
    'SURFACE','Available=true, presentation=true','Present modes: VK_PRESENT_MODE_FIFO_KHR',''
  ];
  while(lines.join('\n').length<1300) lines.push(`[VkPhysicalDeviceProperties] fixture${lines.length} = ${lines.length}`);
  return lines.join('\n');
};
function fixture(){
 const p={
  schemaVersion:2,
  application:{name:'VulkanScope',version:'0.41.9',versionCode:419,packageName:'com.efishell.vulkanscope',applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a']},
  device:{manufacturer:'Example',brand:'Example',model:'Phone',device:'phone',product:'phone',androidRelease:'17',sdk:37,securityPatch:'2026-08-01'},
  gpu:{name:'Adreno Fixture',vendorId:'0x5143',deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU'},
  driver:{mode:'System Vulkan driver',version:'512.1',rawVersion:'1'},
  vulkan:{loaderInstanceApiVersion:'1.4.0',deviceApiVersion:'1.4.0',registryBaseline:'1.4.360',headerBaseline:'1.4.360',reportSchema:'3'},
  collection:{status:'available',error:null,deviceCount:1},
  technicalReport:{schemaVersion:3,loaderInstanceApiVersion:'1.4.0',driverMode:'System Vulkan driver',collectionError:null,applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a'],display:{resolution:'2400 × 1080',refreshRate:'120 Hz',wideGamut:true,preferredWideGamut:'DISPLAY_P3',preferredWideGamutColorSpace:'DISPLAY_P3',hdrTypes:[],hdrCapabilityStatus:'unavailable',minLuminance:'Unavailable',maxLuminance:'Unavailable',averageLuminance:'Unavailable',modes:[]},registryCoverage:{baseline:'1.4.360',mode:'registry-driven',implementedPhysicalDeviceStructCount:109,validatedRuntimeQueryGroupCount:104,runtimeExtensionTokenCount:268,catalogSchemaVersion:1,reportSchema:'3',headerBaseline:'1.4.360',instanceDependencyCandidateCount:1,implementedPhysicalDeviceStructs:[],validatedRuntimeQueryGroups:[]},instanceExtensions:[],instanceLayers:[],devices:[{name:'Adreno Fixture',apiVersion:'1.4.0',driverVersionRaw:1,driverVersionText:'512.1',vendorId:'0x5143',vendorIdRaw:20803,deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU',deviceExtensionStatus:'available',deviceExtensionReason:'',extendedQueryStatus:'available',extendedQueryReason:'',vulkan14Status:'available',vulkan14Reason:'',deviceLayers:[],extensions:[{name:'VK_KHR_video_queue',scope:'Device',specVersion:8,supported:true}],features:[],detailedProperties:[{section:'Vulkan Query Status',name:'Queue Family Properties 2 query',value:'Available'}],imageFormatQueryResults:[],limits:[],memoryHeaps:[],memoryTypes:[],queues:[{index:0,count:1,timestampBits:64,flags:3,flagsU64:'3',flagsCanonical:'VK_QUEUE_GRAPHICS_BIT | VK_QUEUE_COMPUTE_BIT',graphics:true,compute:true,transfer:false,sparse:false,protected:false,videoDecode:false,videoEncode:false,opticalFlow:false,dataGraph:false,unknownFlags:0,granularity:'1 × 1 × 1',videoCodecOperations:0,videoCodecOperationsU64:'0',videoCodecOperationsCanonical:'VK_VIDEO_CODEC_OPERATION_NONE_KHR',videoCodecQueryStatus:'available',videoCodecQueryReason:''}],formats:[],surface:{available:true,presentationSupported:true,colorSpaceExtensionAvailable:false,colorSpaceExtensionEnabled:false,formatQueryResult:0,formatQueryResultSecond:0,formatQuerySecondAttempted:false,formatQuerySafetyRejected:false,capabilities:[],formats:[],presentModes:[],presentationQueues:[]},profileEvaluation:[]}],profileCatalog:[]},
 };
 p.reportText=reportText(p);return p;
}
async function call(path,{method='GET',body,origin,contentType='application/json'}={}){
 const headers={};if(origin)headers.origin=origin;if(body!==undefined)headers['content-type']=contentType;
 return worker.fetch(new Request(`https://vulkanscope-database-api.vulkanscope.workers.dev${path}`,{method,headers,body:body===undefined?undefined:(typeof body==='string'?body:JSON.stringify(body))}),env);
}
let r=await call('/v1/health');assert.equal(r.status,200);let j=await r.json();assert.equal(j.normalizerVersion,15);assert.match(j.publishedVulkanSpec,/1\.4\.360/);assert.match(j.producerQueryBaseline,/0\.41\.9/);
r=await call('/v1/reports',{method:'POST',body:fixture()});assert.equal(r.status,201,await r.text());

let unavailableVideo=fixture();
unavailableVideo.technicalReport.devices[0].queues[0].videoCodecOperations=null;
unavailableVideo.technicalReport.devices[0].queues[0].videoCodecOperationsU64=null;
unavailableVideo.technicalReport.devices[0].queues[0].videoCodecOperationsCanonical='Unknown';
unavailableVideo.technicalReport.devices[0].queues[0].videoCodecQueryStatus='unavailable';
unavailableVideo.technicalReport.devices[0].queues[0].videoCodecQueryReason='VkQueueFamilyVideoPropertiesKHR evidence was not returned for this queue family.';
r=await call('/v1/reports',{method:'POST',body:unavailableVideo});assert.equal(r.status,201,'0.41.7 unavailable video query must preserve null mask semantics');
let invalidUnavailableVideo=fixture();
invalidUnavailableVideo.technicalReport.devices[0].queues[0].videoCodecQueryStatus='unavailable';
invalidUnavailableVideo.technicalReport.devices[0].queues[0].videoCodecOperations=0;
invalidUnavailableVideo.technicalReport.devices[0].queues[0].videoCodecOperationsU64='0';
r=await call('/v1/reports',{method:'POST',body:invalidUnavailableVideo});assert.equal(r.status,400,'0.41.7 unavailable video query must not carry a fabricated zero mask');
let partialExtensions=fixture();partialExtensions.technicalReport.devices[0].deviceExtensionStatus='incomplete';partialExtensions.technicalReport.devices[0].deviceExtensionReason='Device-extension enumeration remained VK_INCOMPLETE; returned entries are partial positive evidence.';r=await call('/v1/reports',{method:'POST',body:partialExtensions});assert.equal(r.status,201,'0.41.7 incomplete device-extension enumeration must remain valid partial evidence');
let invalidQueryDiagnostics=fixture();invalidQueryDiagnostics.technicalReport.devices[0].deviceExtensionStatus='complete-ish';r=await call('/v1/reports',{method:'POST',body:invalidQueryDiagnostics});assert.equal(r.status,400,'0.41.7 runtime query status must use an allow-listed evidence state');
let futureProducer=fixture();futureProducer.application.version='0.42.0';futureProducer.application.versionCode=420;futureProducer.technicalReport.devices[0].queues[0].videoCodecQueryStatus='unavailable';futureProducer.technicalReport.devices[0].queues[0].videoCodecOperations=0;futureProducer.technicalReport.devices[0].queues[0].videoCodecOperationsU64='0';futureProducer.reportText=reportText(futureProducer);r=await call('/v1/reports',{method:'POST',body:futureProducer});assert.equal(r.status,400,'0.41.4+ strict queue semantics must apply to future compatible producers');
let futureDiagnostics=fixture();futureDiagnostics.application.version='0.42.0';futureDiagnostics.application.versionCode=420;futureDiagnostics.technicalReport.devices[0].deviceExtensionStatus='complete-ish';futureDiagnostics.reportText=reportText(futureDiagnostics);r=await call('/v1/reports',{method:'POST',body:futureDiagnostics});assert.equal(r.status,400,'0.41.4+ strict query diagnostics must apply to future compatible producers');
let previousCurrent=fixture();previousCurrent.application.version='0.41.6';previousCurrent.application.versionCode=416;previousCurrent.reportText=reportText(previousCurrent);r=await call('/v1/reports',{method:'POST',body:previousCurrent});assert.equal(r.status,201,'0.41.6 schema-compatible producer must remain accepted');
let previousStrict=fixture();previousStrict.application.version='0.41.4';previousStrict.application.versionCode=414;previousStrict.reportText=reportText(previousStrict);r=await call('/v1/reports',{method:'POST',body:previousStrict});assert.equal(r.status,201,'0.41.4 schema-compatible producer must remain accepted');
let olderCurrent=fixture();olderCurrent.application.version='0.41.3';olderCurrent.application.versionCode=413;olderCurrent.reportText=reportText(olderCurrent);r=await call('/v1/reports',{method:'POST',body:olderCurrent});assert.equal(r.status,201,'0.41.3 schema-compatible producer must remain accepted');
let previousProducer=fixture();previousProducer.application.version='0.41.2';previousProducer.application.versionCode=412;previousProducer.reportText=reportText(previousProducer);r=await call('/v1/reports',{method:'POST',body:previousProducer});assert.equal(r.status,201,'0.41.2 schema-compatible producer must remain accepted');
let currentMismatch=fixture();currentMismatch.application.versionCode=416;currentMismatch.reportText=reportText(currentMismatch);r=await call('/v1/reports',{method:'POST',body:currentMismatch});assert.equal(r.status,400);
let badProducer=fixture();badProducer.application.version='1.0.0';badProducer.application.versionCode=1000;badProducer.reportText=reportText(badProducer);r=await call('/v1/reports',{method:'POST',body:badProducer});assert.equal(r.status,400);
let belowFloor=fixture();belowFloor.application.version='0.32.3';belowFloor.application.versionCode=323;belowFloor.reportText=reportText(belowFloor);r=await call('/v1/reports',{method:'POST',body:belowFloor});assert.equal(r.status,400);
let badPatch=fixture();badPatch.device.securityPatch='August 2026';badPatch.reportText=reportText(badPatch);r=await call('/v1/reports',{method:'POST',body:badPatch});assert.equal(r.status,400);
let badAbi=fixture();badAbi.technicalReport.applicationAbi='x86_64';r=await call('/v1/reports',{method:'POST',body:badAbi});assert.equal(r.status,400);
let p=fixture();p.technicalReport.devices[0].apiVersion='1.3.0';r=await call('/v1/reports',{method:'POST',body:p});assert.equal(r.status,400);
p=fixture();p['account_id']='x';r=await call('/v1/reports',{method:'POST',body:p});assert.equal(r.status,400);
r=await call('/v1/reports',{method:'POST',body:fixture(),contentType:'text/plain'});assert.equal(r.status,415);
r=await call('/v1/reports',{method:'POST',body:fixture(),origin:'https://evil.example'});assert.equal(r.status,403);
r=await call('/v1/reports',{method:'PUT'});assert.equal(r.status,405);
r=await call('/nope');assert.equal(r.status,404);
const huge='{"x":"'+'a'.repeat(2*1024*1024+64)+'"}';r=await call('/v1/reports',{method:'POST',body:huge});assert.equal(r.status,413);

const metricFixture=fixture();
metricFixture.technicalReport.devices[0].detailedProperties=[
  {section:'VkPhysicalDeviceProperties',name:'apiVersion',value:'1.4.0'},
  {section:'VkPhysicalDeviceVulkan14Properties',name:'lineRasterizationMode',value:'1'},
  {section:'VkPhysicalDeviceExampleProperties',name:'booleanPropertyFalse',value:'false'}
];
metricFixture.technicalReport.devices[0].limits=[{name:'maxImageDimension2D',value:'16384'}];

metricFixture.technicalReport.devices[0].detailedProperties.push(
  {section:'CapsViewer 4.12 parity · VkPhysicalDeviceHostImageCopyPropertiesEXT',name:'pCopySrcLayouts',value:'VK_IMAGE_LAYOUT_GENERAL (raw=1), VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL (raw=6)'},
  {section:'CapsViewer 4.12 parity · VkPhysicalDeviceHostImageCopyPropertiesEXT',name:'pCopyDstLayouts',value:'VK_IMAGE_LAYOUT_GENERAL (raw=1), VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL (raw=7)'}
);
const normalized=normalizeReport(metricFixture);
assert.equal(normalized.detailedProperties.length,5,'structured detailedProperties must be authoritative');
assert.equal(normalized.detailedProperties.filter(x=>x.name==='pCopySrcLayouts'||x.name==='pCopyDstLayouts').length,2,'Host Image Copy layout arrays must survive normalization');
assert.equal(normalized.limits.length,1,'structured limits must be authoritative');
assert.equal(normalized.detailedProperties.some(x=>x.section==='DEVICE'||x.section==='SURFACE'),false,'metadata must not contaminate properties');
assert.equal(normalized.limits.some(x=>/Sparse Properties/i.test(x.section)),false,'detailed properties must not be reclassified as limits');
assert.equal(normalized.queues.length,1,'structured queues must be authoritative');
assert.equal(normalized.detailedProperties.find(x=>x.name==='booleanPropertyFalse')?.status,'available','false property value must retain query-available semantics');
assert.equal(normalized.queryDiagnostics.deviceExtensionStatus,'available','device extension enumeration status must survive normalization');
assert.equal(normalized.queryDiagnostics.extendedQueryStatus,'available','extended query status must survive normalization');
assert.equal(normalized.queryDiagnostics.vulkan14Status,'available','Vulkan 1.4 query status must survive normalization');
assert.equal(normalized.queues[0].videoCodecQueryStatus,'available','video codec query state must survive normalization');
assert.equal(String(normalized.queues[0].videoCodecOperations),'0','queried zero video codec mask must survive normalization');

let badCurrentEmbeddedTuple=fixture();
badCurrentEmbeddedTuple.technicalReport.devices[0].detailedProperties.push({section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED'});
r=await call('/v1/reports',{method:'POST',body:badCurrentEmbeddedTuple});assert.equal(r.status,400,'0.41.9 non-success Image Format Properties2 tuples must not inflate detailedProperties');

let goodSeparatedUnsupported=fixture();
goodSeparatedUnsupported.technicalReport.devices[0].imageFormatQueryResults.push({name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unsupported',vkResult:-11});
goodSeparatedUnsupported.reportText=reportText(goodSeparatedUnsupported).replace('IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (0 non-success tuples; excluded from property/query totals)','IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (1 non-success tuples; excluded from property/query totals)\nVK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER | UNSUPPORTED | VkResult=-11');
r=await call('/v1/reports',{method:'POST',body:goodSeparatedUnsupported});assert.equal(r.status,201,'0.41.9 exact unsupported tuple must be accepted in the separated query-result dataset');
let normalizedSeparated=normalizeReport(goodSeparatedUnsupported);assert.equal(normalizedSeparated.detailedProperties.some(x=>x.name.includes('VK_FORMAT_S8_UINT')),false,'separated negative tuple must not enter normalized detailedProperties');assert.equal(normalizedSeparated.imageFormatQueryResults.length,1,'separated tuple result must survive normalization');

let goodSeparatedUnavailable=fixture();
goodSeparatedUnavailable.technicalReport.devices[0].imageFormatQueryResults.push({name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:-1});
goodSeparatedUnavailable.reportText=reportText(goodSeparatedUnavailable).replace('IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (0 non-success tuples; excluded from property/query totals)','IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (1 non-success tuples; excluded from property/query totals)\nVK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER | UNAVAILABLE | VkResult=-1');
r=await call('/v1/reports',{method:'POST',body:goodSeparatedUnavailable});assert.equal(r.status,201,'0.41.9 numeric unavailable tuple must be accepted separately');

for (const bad of [
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unsupported',vkResult:-1},
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:-11},
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:0},
  {name:'not-a-canonical-tuple',status:'unsupported',vkResult:-11},
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unknown',vkResult:-11}
]){const x=fixture();x.technicalReport.devices[0].imageFormatQueryResults.push(bad);r=await call('/v1/reports',{method:'POST',body:x});assert.equal(r.status,400,`0.41.9 malformed separated tuple result must be rejected: ${JSON.stringify(bad)}`)}
let duplicateTuple=fixture();duplicateTuple.technicalReport.devices[0].imageFormatQueryResults.push({name:'VK_FORMAT_S8_UINT · LINEAR',status:'unsupported',vkResult:-11},{name:'VK_FORMAT_S8_UINT · LINEAR',status:'unsupported',vkResult:-11});r=await call('/v1/reports',{method:'POST',body:duplicateTuple});assert.equal(r.status,400,'duplicate 0.41.9 tuple identities must be rejected');

let legacy0818=fixture();legacy0818.application.version='0.41.8';legacy0818.application.versionCode=418;delete legacy0818.technicalReport.devices[0].imageFormatQueryResults;legacy0818.technicalReport.devices[0].detailedProperties.push({section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED'});legacy0818.reportText=reportText(legacy0818).replace('IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (0 non-success tuples; excluded from property/query totals)','')+'\n[Image Format Properties2] VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER = Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED\n';r=await call('/v1/reports',{method:'POST',body:legacy0818});assert.equal(r.status,201,'historical 0.41.8 embedded tuple evidence must remain accepted');

console.log('VulkanScope Database worker contract tests: ALL PASS');
