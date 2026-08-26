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
  const imageResults=p.technicalReport?.devices?.[0]?.imageFormatQueryResults||[];
  const imageLines=imageResults.map(x=>`${x.name} | ${String(x.status).toUpperCase()} | VkResult=${x.vkResult===null?'null':x.vkResult}${x.reason?` | Reason=${x.reason}`:''}`);
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
    `IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES (${imageResults.length} exact tuple states; excluded from property/query totals)`,...imageLines,'',
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
  application:{name:'VulkanScope',version:'0.41.13',versionCode:423,packageName:'com.efishell.vulkanscope',applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a']},
  device:{manufacturer:'Example',brand:'Example',model:'Phone',device:'phone',product:'phone',androidRelease:'17',sdk:37,securityPatch:'2026-08-01'},
  gpu:{name:'Adreno Fixture',vendorId:'0x5143',deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU'},
  driver:{mode:'System Vulkan driver',version:'512.1',rawVersion:'1'},
  vulkan:{loaderInstanceApiVersion:'1.4.0',deviceApiVersion:'1.4.0',registryBaseline:'1.4.360',headerBaseline:'1.4.360',reportSchema:'3'},
  collection:{status:'available',error:null,deviceCount:1},
  technicalReport:{schemaVersion:3,loaderInstanceApiVersion:'1.4.0',driverMode:'System Vulkan driver',collectionError:null,applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a'],display:{resolution:'2400 × 1080',refreshRate:'120 Hz',wideGamut:true,preferredWideGamut:'DISPLAY_P3',preferredWideGamutColorSpace:'DISPLAY_P3',hdrTypes:[],hdrCapabilityStatus:'unavailable',minLuminance:'Unavailable',maxLuminance:'Unavailable',averageLuminance:'Unavailable',modes:[]},registryCoverage:{baseline:'1.4.360',mode:'registry-driven',implementedPhysicalDeviceStructCount:109,validatedRuntimeQueryGroupCount:104,runtimeExtensionTokenCount:268,catalogSchemaVersion:1,reportSchema:'3',headerBaseline:'1.4.360',instanceDependencyCandidateCount:1,implementedPhysicalDeviceStructs:[],validatedRuntimeQueryGroups:[]},instanceExtensions:[],instanceLayers:[],devices:[{name:'Adreno Fixture',apiVersion:'1.4.0',driverVersionRaw:1,driverVersionText:'512.1',vendorId:'0x5143',vendorIdRaw:20803,deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU',deviceExtensionStatus:'available',deviceExtensionReason:'',extendedQueryStatus:'available',extendedQueryReason:'',vulkan14Status:'available',vulkan14Reason:'',imageFormatQueryStatus:'available',imageFormatQueryReason:'',deviceLayers:[],extensions:[{name:'VK_KHR_video_queue',scope:'Device',specVersion:8,supported:true}],features:[],detailedProperties:[{section:'Vulkan Query Status',name:'Queue Family Properties 2 query',value:'Available'},{section:'Vulkan Query Status',name:'Image Format Properties 2 query',value:'Available'},{section:'Image Format Properties2 Query Diagnostics',name:'Query parameters',value:'imageType=VK_IMAGE_TYPE_2D, usage=VK_IMAGE_USAGE_TRANSFER_SRC_BIT | VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT, flags=0'},{section:'Image Format Properties2 Query Diagnostics',name:'Base image-format queries',value:'attempted=2, success=2, formatNotSupported=0, otherErrors=0'},{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR',value:'tiling=LINEAR, extent=16384 × 16384 × 1, mipLevels=1, arrayLayers=2048, sampleCounts=0x1, maxResourceSize=4294967295'},{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · OPTIMAL',value:'tiling=OPTIMAL, extent=16384 × 16384 × 1, mipLevels=1, arrayLayers=2048, sampleCounts=0x1, maxResourceSize=4294967295'}],imageFormatQueryResults:[{name:'VK_FORMAT_S8_UINT · LINEAR',status:'available',vkResult:0,reason:''},{name:'VK_FORMAT_S8_UINT · LINEAR · OPAQUE_FD',status:'not_applicable',vkResult:null,reason:'VK_KHR_external_memory_fd was not enumerated for this device.'},{name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'not_applicable',vkResult:null,reason:'VK_ANDROID_external_memory_android_hardware_buffer was not enumerated for this device.'},{name:'VK_FORMAT_S8_UINT · OPTIMAL',status:'available',vkResult:0,reason:''},{name:'VK_FORMAT_S8_UINT · OPTIMAL · OPAQUE_FD',status:'not_applicable',vkResult:null,reason:'VK_KHR_external_memory_fd was not enumerated for this device.'},{name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',status:'not_applicable',vkResult:null,reason:'VK_ANDROID_external_memory_android_hardware_buffer was not enumerated for this device.'}],limits:[],memoryHeaps:[],memoryTypes:[],queues:[{index:0,count:1,timestampBits:64,flags:3,flagsU64:'3',flagsCanonical:'VK_QUEUE_GRAPHICS_BIT | VK_QUEUE_COMPUTE_BIT',graphics:true,compute:true,transfer:false,sparse:false,protected:false,videoDecode:false,videoEncode:false,opticalFlow:false,dataGraph:false,unknownFlags:0,granularity:'1 × 1 × 1',videoCodecOperations:0,videoCodecOperationsU64:'0',videoCodecOperationsCanonical:'VK_VIDEO_CODEC_OPERATION_NONE_KHR',videoCodecQueryStatus:'available',videoCodecQueryReason:''}],formats:[],surface:{available:true,presentationSupported:true,colorSpaceExtensionAvailable:false,colorSpaceExtensionEnabled:false,formatQueryResult:0,formatQueryResultSecond:0,formatQuerySecondAttempted:false,formatQuerySafetyRejected:false,capabilities:[],formats:[],presentModes:[],presentationQueues:[]},profileEvaluation:[]}],profileCatalog:[]},
 };
 p.reportText=reportText(p);return p;
}
async function call(path,{method='GET',body,origin,contentType='application/json'}={}){
 const headers={};if(origin)headers.origin=origin;if(body!==undefined)headers['content-type']=contentType;
 return worker.fetch(new Request(`https://vulkanscope-database-api.vulkanscope.workers.dev${path}`,{method,headers,body:body===undefined?undefined:(typeof body==='string'?body:JSON.stringify(body))}),env);
}
let r=await call('/v1/health');assert.equal(r.status,200);let j=await r.json();assert.equal(j.normalizerVersion,16);assert.match(j.publishedVulkanSpec,/1\.4\.360/);assert.match(j.producerQueryBaseline,/0\.41\.13/);
r=await call('/v1/reports',{method:'POST',body:fixture()});assert.equal(r.status,201,await r.text());


let unavailableImageFormatGroup=fixture();
{
 const d=unavailableImageFormatGroup.technicalReport.devices[0];
 d.detailedProperties=d.detailedProperties.filter(x=>!['Image Format Properties2','Image Format Properties2 Query Diagnostics'].includes(x.section));
 const status=d.detailedProperties.find(x=>x.section==='Vulkan Query Status'&&x.name==='Image Format Properties 2 query');
 status.value='Unavailable: The isolated imageFormat2 query did not complete within the timeout.';
 d.imageFormatQueryStatus='unavailable'; d.imageFormatQueryReason='The isolated imageFormat2 query did not complete within the timeout.';
 d.imageFormatQueryResults=[];
 unavailableImageFormatGroup.reportText=reportText(unavailableImageFormatGroup);
}
r=await call('/v1/reports',{method:'POST',body:unavailableImageFormatGroup});assert.equal(r.status,201,'0.41.12 explicit group-level Image Format Properties2 Unavailable evidence must remain a complete report without fabricated tuple rows');
let historicalUnavailable04112=structuredClone(unavailableImageFormatGroup);historicalUnavailable04112.application.version='0.41.12';historicalUnavailable04112.application.versionCode=422;delete historicalUnavailable04112.technicalReport.devices[0].imageFormatQueryStatus;delete historicalUnavailable04112.technicalReport.devices[0].imageFormatQueryReason;historicalUnavailable04112.reportText=reportText(historicalUnavailable04112);r=await call('/v1/reports',{method:'POST',body:historicalUnavailable04112});assert.equal(r.status,201,'0.41.12 explicit group-level Unavailable remains compatible without 0.41.13 structured provenance');


let notApplicableImageFormatGroup=structuredClone(unavailableImageFormatGroup);
notApplicableImageFormatGroup.technicalReport.devices[0].detailedProperties.find(x=>x.section==='Vulkan Query Status'&&x.name==='Image Format Properties 2 query').value='Not applicable: No physical Vulkan devices were enumerated by the isolated query.';
notApplicableImageFormatGroup.technicalReport.devices[0].imageFormatQueryStatus='not_applicable';
notApplicableImageFormatGroup.technicalReport.devices[0].imageFormatQueryReason='No physical Vulkan devices were enumerated by the isolated query.';
notApplicableImageFormatGroup.reportText=reportText(notApplicableImageFormatGroup);
r=await call('/v1/reports',{method:'POST',body:notApplicableImageFormatGroup});assert.equal(r.status,201,'0.41.12 explicit group-level Not applicable evidence must not require a fabricated tuple ledger');

let missingImageFormatState=structuredClone(unavailableImageFormatGroup);
missingImageFormatState.technicalReport.devices[0].detailedProperties=missingImageFormatState.technicalReport.devices[0].detailedProperties.filter(x=>!(x.section==='Vulkan Query Status'&&x.name==='Image Format Properties 2 query'));
missingImageFormatState.reportText=reportText(missingImageFormatState);
r=await call('/v1/reports',{method:'POST',body:missingImageFormatState});assert.equal(r.status,400,'0.41.12 empty Image Format Properties2 evidence without an explicit query-group state must fail closed');
let missingImageFormatBody=await r.json();assert.match(missingImageFormatBody.error,/image_format_query_state/,'HTTP 400 must expose the bounded failing validation class');

let contradictoryUnavailable=structuredClone(unavailableImageFormatGroup);
contradictoryUnavailable.technicalReport.devices[0].imageFormatQueryResults=[{name:'VK_FORMAT_S8_UINT · LINEAR',status:'unsupported',vkResult:-11,reason:''}];
contradictoryUnavailable.reportText=reportText(contradictoryUnavailable);
r=await call('/v1/reports',{method:'POST',body:contradictoryUnavailable});assert.equal(r.status,400,'group-level Unavailable must reject contradictory tuple evidence rather than silently normalizing it');

let unavailableWithSuccess=structuredClone(unavailableImageFormatGroup);
unavailableWithSuccess.technicalReport.devices[0].detailedProperties.push({section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR',value:'tiling=LINEAR, extent=1 × 1 × 1, mipLevels=1, arrayLayers=1, sampleCounts=0x1, maxResourceSize=1'});
unavailableWithSuccess.reportText=reportText(unavailableWithSuccess);
r=await call('/v1/reports',{method:'POST',body:unavailableWithSuccess});assert.equal(r.status,400,'group-level Unavailable must reject contradictory successful property evidence');

let astcCanonical=fixture();
for(const row of astcCanonical.technicalReport.devices[0].detailedProperties){if(row.section==='Image Format Properties2')row.name=row.name.replace('VK_FORMAT_S8_UINT','VK_FORMAT_ASTC_10x8_SRGB_BLOCK');}
for(const row of astcCanonical.technicalReport.devices[0].imageFormatQueryResults)row.name=row.name.replace('VK_FORMAT_S8_UINT','VK_FORMAT_ASTC_10x8_SRGB_BLOCK');
astcCanonical.reportText=reportText(astcCanonical);
r=await call('/v1/reports',{method:'POST',body:astcCanonical});assert.equal(r.status,201,'canonical ASTC Vulkan format names with lowercase x must be accepted');
let astc3dCanonical=fixture();
for(const row of astc3dCanonical.technicalReport.devices[0].detailedProperties){if(row.section==='Image Format Properties2')row.name=row.name.replace('VK_FORMAT_S8_UINT','VK_FORMAT_ASTC_4x4x3_UNORM_BLOCK_EXT');}
for(const row of astc3dCanonical.technicalReport.devices[0].imageFormatQueryResults)row.name=row.name.replace('VK_FORMAT_S8_UINT','VK_FORMAT_ASTC_4x4x3_UNORM_BLOCK_EXT');
astc3dCanonical.reportText=reportText(astc3dCanonical);
r=await call('/v1/reports',{method:'POST',body:astc3dCanonical});assert.equal(r.status,201,'canonical ASTC 3D Vulkan format names with multiple lowercase x separators must be accepted');
let malformedLowercase=fixture();
for(const row of malformedLowercase.technicalReport.devices[0].detailedProperties){if(row.section==='Image Format Properties2')row.name=row.name.replace('VK_FORMAT_S8_UINT','VK_FORMAT_ASTC_10y8_SRGB_BLOCK');}
for(const row of malformedLowercase.technicalReport.devices[0].imageFormatQueryResults)row.name=row.name.replace('VK_FORMAT_S8_UINT','VK_FORMAT_ASTC_10y8_SRGB_BLOCK');
malformedLowercase.reportText=reportText(malformedLowercase);
r=await call('/v1/reports',{method:'POST',body:malformedLowercase});assert.equal(r.status,400,'non-registry lowercase separators must remain rejected');

let historical04110=fixture();historical04110.application.version='0.41.10';historical04110.application.versionCode=420;historical04110.reportText=reportText(historical04110);r=await call('/v1/reports',{method:'POST',body:historical04110});assert.equal(r.status,201,'historical 0.41.10 producer remains accepted');
let historical04111=fixture();historical04111.application.version='0.41.11';historical04111.application.versionCode=421;historical04111.reportText=reportText(historical04111);r=await call('/v1/reports',{method:'POST',body:historical04111});assert.equal(r.status,201,'historical 0.41.11 producer remains accepted');
let badCurrentIdentity=fixture();badCurrentIdentity.application.versionCode=421;badCurrentIdentity.reportText=reportText(badCurrentIdentity);r=await call('/v1/reports',{method:'POST',body:badCurrentIdentity});assert.equal(r.status,400,'0.41.12 current producer requires versionCode 422');


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

let currentAhbUnsupported=fixture();
const currentDevice=currentAhbUnsupported.technicalReport.devices[0];
currentDevice.extensions.push({name:'VK_ANDROID_external_memory_android_hardware_buffer',scope:'Device',specVersion:5,supported:true});
currentDevice.detailedProperties.push({section:'Image Format Properties2 Query Diagnostics',name:'ANDROID_HARDWARE_BUFFER external image-format queries',value:'attempted=2, success=0, formatNotSupported=2, otherErrors=0'});
for(const x of currentDevice.imageFormatQueryResults)if(x.name.endsWith('ANDROID_HARDWARE_BUFFER'))Object.assign(x,{status:'unsupported',vkResult:-11,reason:''});
currentAhbUnsupported.reportText=reportText(currentAhbUnsupported);
r=await call('/v1/reports',{method:'POST',body:currentAhbUnsupported});assert.equal(r.status,201,'0.41.10 S8/AHB VK_ERROR_FORMAT_NOT_SUPPORTED must be accepted as exact Unsupported evidence');
let currentAhbUnavailable=fixture();
const unavailableAhbDevice=currentAhbUnavailable.technicalReport.devices[0];
unavailableAhbDevice.extensions.push({name:'VK_ANDROID_external_memory_android_hardware_buffer',scope:'Device',specVersion:5,supported:true});
unavailableAhbDevice.detailedProperties.push({section:'Image Format Properties2 Query Diagnostics',name:'ANDROID_HARDWARE_BUFFER external image-format queries',value:'attempted=2, success=0, formatNotSupported=0, otherErrors=2, firstOtherVkResult=-1'});
for(const x of unavailableAhbDevice.imageFormatQueryResults)if(x.name.endsWith('ANDROID_HARDWARE_BUFFER'))Object.assign(x,{status:'unavailable',vkResult:-1,reason:''});
currentAhbUnavailable.reportText=reportText(currentAhbUnavailable);
r=await call('/v1/reports',{method:'POST',body:currentAhbUnavailable});assert.equal(r.status,201,'0.41.10 non-format Vulkan errors must remain exact Unavailable evidence');
let normalizedCurrent=normalizeReport(currentAhbUnsupported);assert.equal(normalizedCurrent.imageFormatQueryResults.find(x=>x.name==='VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER')?.status,'unsupported','current S8/AHB unsupported state must survive normalization');

let missingAhbTuple=structuredClone(currentAhbUnsupported);missingAhbTuple.technicalReport.devices[0].imageFormatQueryResults=missingAhbTuple.technicalReport.devices[0].imageFormatQueryResults.filter(x=>x.name!=='VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER');missingAhbTuple.reportText=reportText(missingAhbTuple);r=await call('/v1/reports',{method:'POST',body:missingAhbTuple});assert.equal(r.status,400,'0.41.10 must reject a silently missing scheduled S8/AHB tuple');
let availableWithoutProperty=fixture();availableWithoutProperty.technicalReport.devices[0].detailedProperties=availableWithoutProperty.technicalReport.devices[0].detailedProperties.filter(x=>x.name!=='VK_FORMAT_S8_UINT · LINEAR');availableWithoutProperty.reportText=reportText(availableWithoutProperty);r=await call('/v1/reports',{method:'POST',body:availableWithoutProperty});assert.equal(r.status,400,'0.41.10 Available tuple state requires its successful full property payload');
let propertyWithoutAvailable=fixture();propertyWithoutAvailable.technicalReport.devices[0].imageFormatQueryResults.find(x=>x.name==='VK_FORMAT_S8_UINT · LINEAR').status='unsupported';propertyWithoutAvailable.technicalReport.devices[0].imageFormatQueryResults.find(x=>x.name==='VK_FORMAT_S8_UINT · LINEAR').vkResult=-11;propertyWithoutAvailable.technicalReport.devices[0].detailedProperties.find(x=>x.name==='Base image-format queries').value='attempted=2, success=1, formatNotSupported=1, otherErrors=0';propertyWithoutAvailable.reportText=reportText(propertyWithoutAvailable);r=await call('/v1/reports',{method:'POST',body:propertyWithoutAvailable});assert.equal(r.status,400,'0.41.10 successful property evidence cannot disagree with the exact tuple ledger');
let badNotApplicableWithExtension=fixture();badNotApplicableWithExtension.technicalReport.devices[0].extensions.push({name:'VK_ANDROID_external_memory_android_hardware_buffer',scope:'Device',specVersion:5,supported:true});badNotApplicableWithExtension.reportText=reportText(badNotApplicableWithExtension);r=await call('/v1/reports',{method:'POST',body:badNotApplicableWithExtension});assert.equal(r.status,400,'0.41.10 must not accept Not applicable when the prerequisite AHB extension is enumerated');
let badNotApplicableResult=fixture();let badNa=badNotApplicableResult.technicalReport.devices[0].imageFormatQueryResults.find(x=>x.name.endsWith('LINEAR · ANDROID_HARDWARE_BUFFER'));badNa.vkResult=-11;badNotApplicableResult.reportText=reportText(badNotApplicableResult);r=await call('/v1/reports',{method:'POST',body:badNotApplicableResult});assert.equal(r.status,400,'0.41.10 Not applicable tuple must carry null VkResult');
let badNotApplicableReason=fixture();badNa=badNotApplicableReason.technicalReport.devices[0].imageFormatQueryResults.find(x=>x.name.endsWith('LINEAR · ANDROID_HARDWARE_BUFFER'));badNa.reason='missing';badNotApplicableReason.reportText=reportText(badNotApplicableReason);r=await call('/v1/reports',{method:'POST',body:badNotApplicableReason});assert.equal(r.status,400,'0.41.10 Not applicable tuple must preserve the exact prerequisite reason');
let badBaseNotApplicable=fixture();let badBase=badBaseNotApplicable.technicalReport.devices[0].imageFormatQueryResults.find(x=>x.name==='VK_FORMAT_S8_UINT · LINEAR');badBase.status='not_applicable';badBase.vkResult=null;badBase.reason='missing';badBaseNotApplicable.reportText=reportText(badBaseNotApplicable);r=await call('/v1/reports',{method:'POST',body:badBaseNotApplicable});assert.equal(r.status,400,'base image-format queries can never be Not applicable');
let badDiagnostics=fixture();badDiagnostics.technicalReport.devices[0].detailedProperties.find(x=>x.name==='Base image-format queries').value='attempted=4, success=2, formatNotSupported=2, otherErrors=0';badDiagnostics.reportText=reportText(badDiagnostics);r=await call('/v1/reports',{method:'POST',body:badDiagnostics});assert.equal(r.status,400,'0.41.10 tuple ledger must cross-check aggregate attempted/result counts');

const historical0419=()=>{const x=fixture();x.application.version='0.41.9';x.application.versionCode=419;const d=x.technicalReport.devices[0];d.detailedProperties=d.detailedProperties.filter(p=>!['Image Format Properties2','Image Format Properties2 Query Diagnostics'].includes(p.section));d.imageFormatQueryResults=[];x.reportText=reportText(x);return x};
let badCurrentEmbeddedTuple=historical0419();
badCurrentEmbeddedTuple.technicalReport.devices[0].detailedProperties.push({section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED'});
r=await call('/v1/reports',{method:'POST',body:badCurrentEmbeddedTuple});assert.equal(r.status,400,'0.41.9 non-success Image Format Properties2 tuples must not inflate detailedProperties');

let goodSeparatedUnsupported=historical0419();
goodSeparatedUnsupported.technicalReport.devices[0].imageFormatQueryResults.push({name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unsupported',vkResult:-11});
goodSeparatedUnsupported.reportText=reportText(goodSeparatedUnsupported);
r=await call('/v1/reports',{method:'POST',body:goodSeparatedUnsupported});assert.equal(r.status,201,'historical 0.41.9 exact unsupported tuple remains accepted in the separated query-result dataset');
let normalizedSeparated=normalizeReport(goodSeparatedUnsupported);assert.equal(normalizedSeparated.detailedProperties.some(x=>x.name.includes('VK_FORMAT_S8_UINT')),false,'historical separated negative tuple must not enter normalized detailedProperties');assert.equal(normalizedSeparated.imageFormatQueryResults.length,1,'historical separated tuple result must survive normalization');

let goodSeparatedUnavailable=historical0419();
goodSeparatedUnavailable.technicalReport.devices[0].imageFormatQueryResults.push({name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:-1});
goodSeparatedUnavailable.reportText=reportText(goodSeparatedUnavailable);
r=await call('/v1/reports',{method:'POST',body:goodSeparatedUnavailable});assert.equal(r.status,201,'historical 0.41.9 numeric unavailable tuple remains accepted separately');

for (const bad of [
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unsupported',vkResult:-1},
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:-11},
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unavailable',vkResult:0},
  {name:'not-a-canonical-tuple',status:'unsupported',vkResult:-11},
  {name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'unknown',vkResult:-11}
]){const x=historical0419();x.technicalReport.devices[0].imageFormatQueryResults.push(bad);x.reportText=reportText(x);r=await call('/v1/reports',{method:'POST',body:x});assert.equal(r.status,400,`historical 0.41.9 malformed separated tuple result must be rejected: ${JSON.stringify(bad)}`)}
let duplicateTuple=historical0419();duplicateTuple.technicalReport.devices[0].imageFormatQueryResults.push({name:'VK_FORMAT_S8_UINT · LINEAR',status:'unsupported',vkResult:-11},{name:'VK_FORMAT_S8_UINT · LINEAR',status:'unsupported',vkResult:-11});duplicateTuple.reportText=reportText(duplicateTuple);r=await call('/v1/reports',{method:'POST',body:duplicateTuple});assert.equal(r.status,400,'duplicate historical 0.41.9 tuple identities must be rejected');

let legacy0818=fixture();legacy0818.application.version='0.41.8';legacy0818.application.versionCode=418;delete legacy0818.technicalReport.devices[0].imageFormatQueryResults;legacy0818.technicalReport.devices[0].detailedProperties=legacy0818.technicalReport.devices[0].detailedProperties.filter(p=>!['Image Format Properties2','Image Format Properties2 Query Diagnostics'].includes(p.section));legacy0818.technicalReport.devices[0].detailedProperties.push({section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',value:'Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED'});legacy0818.reportText=reportText(legacy0818).replace(/IMAGE FORMAT PROPERTIES2 QUERY OUTCOMES[^\n]*\n?/,'')+'\n[Image Format Properties2] VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER = Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED\n';r=await call('/v1/reports',{method:'POST',body:legacy0818});assert.equal(r.status,201,'historical 0.41.8 embedded tuple evidence must remain accepted');

console.log('VulkanScope Database worker contract tests: ALL PASS');
