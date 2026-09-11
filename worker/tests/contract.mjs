import worker, { normalizeReport } from '../src/index.js';
import assert from 'node:assert/strict';

class DB {
  constructor(){this.rows=new Map();this.chunks=new Map()}
  statement(sql,args=[]){
    const self=this;
    return {sql,args,
      bind(...next){return self.statement(sql,next)},
      async run(){
        if(sql.startsWith('INSERT OR IGNORE INTO reports')){const [id,submittedAt,,,,,,,,,,payload]=args;if(!self.rows.has(id))self.rows.set(id,{id,submitted_at:submittedAt,payload_json:payload})}
        if(sql.startsWith('INSERT OR IGNORE INTO report_payload_chunks')){const [id,index,chunk]=args;const key=`${id}:${index}`;if(!self.chunks.has(key))self.chunks.set(key,{report_id:id,chunk_index:index,payload_chunk:chunk})}
        return {success:true}
      },
      async first(){
        if(sql.includes('SELECT submitted_at FROM reports WHERE id=?')){const row=self.rows.get(args[0]);return row?{submitted_at:row.submitted_at}:null}
        if(sql.includes('SELECT payload_json,submitted_at,id FROM reports WHERE id=?'))return self.rows.get(args[0])||null;
        return null
      },
      async all(){
        if(sql.includes('SELECT payload_chunk FROM report_payload_chunks')){return {results:[...self.chunks.values()].filter(x=>x.report_id===args[0]).sort((a,b)=>a.chunk_index-b.chunk_index).map(x=>({payload_chunk:x.payload_chunk}))}}
        return {results:[]}
      }
    }
  }
  prepare(sql){return this.statement(sql)}
  async batch(statements){for(const statement of statements)await statement.run();return statements.map(()=>({success:true}))}
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
    ...((()=>{const m=/^(\d+)\.(\d+)\.(\d+)$/.exec(String(p.application.version||''));const modern=m&&(Number(m[1])>0||Number(m[1])===0&&(Number(m[2])>41||Number(m[2])===41&&Number(m[3])>=24));return modern?[`Loader API: ${p.vulkan.loaderApiVersion}`,`Base probe instance API: ${p.vulkan.instanceApiVersion}`]:[`Loader / instance API: ${p.vulkan.loaderInstanceApiVersion}`]})()),
    '', 'VULKAN REGISTRY COVERAGE',`Baseline=${p.vulkan.registryBaseline}`,'',
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
  application:{name:'VulkanScope',version:'0.80.9',versionCode:809,packageName:'com.efishell.vulkanscope',applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a']},
  device:{manufacturer:'Example',brand:'Example',model:'Phone',device:'phone',product:'phone',androidRelease:'17',sdk:37,securityPatch:'2026-08-01'},
  gpu:{name:'Adreno Fixture',vendorId:'0x5143',deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU',summaryScope:'singlePhysicalDevice',physicalDeviceCount:1},
  driver:{mode:'System Vulkan driver',version:'512.1',rawVersion:'1',summaryScope:'singlePhysicalDevice'},
  vulkan:{loaderInstanceApiVersion:'1.4.0',loaderApiVersion:'1.4.0',instanceApiVersion:'1.4.0',deviceApiVersion:'1.4.0',deviceApiSummaryScope:'singlePhysicalDevice',registryBaseline:'Vulkan 1.4.361',headerBaseline:'Vulkan 1.4.361 compile headers; validated query catalog Vulkan 1.4.361',reportSchema:'4'},
  collection:{status:'available',error:null,deviceCount:1},
  technicalReport:{schemaVersion:3,loaderInstanceApiVersion:'1.4.0',loaderApiVersion:'1.4.0',instanceApiVersion:'1.4.0',driverMode:'System Vulkan driver',collectionError:null,baseReportComplete:true,physicalDeviceEnumerationResult:0,physicalDeviceEnumerationResultName:'VK_SUCCESS',physicalDeviceEnumerationComplete:true,physicalDeviceEnumerationSafetyRejected:false,physicalDeviceEnumerationReason:'',applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a'],display:{resolution:'2400 × 1080',refreshRate:'120 Hz',wideGamut:true,preferredWideGamut:'DISPLAY_P3',preferredWideGamutColorSpace:'DISPLAY_P3',hdrTypes:[],hdrCapabilityStatus:'unavailable',minLuminance:'Unavailable',maxLuminance:'Unavailable',averageLuminance:'Unavailable',modes:[]},registryCoverage:{baseline:'Vulkan 1.4.361',mode:'offline registry-driven validated query catalog',implementedPhysicalDeviceStructCount:110,validatedRuntimeQueryGroupCount:104,runtimeRegistryTokenReferenceCount:268,runtimeExtensionTokenCount:268,catalogSchemaVersion:6,reportSchema:'4',headerBaseline:'Vulkan 1.4.361 compile headers; validated query catalog Vulkan 1.4.361',instanceDependencyCandidateCount:1,implementedPhysicalDeviceStructs:['VkPhysicalDevicePrivateDataBaseHandleFeaturesNV'],validatedRuntimeQueryGroups:[]},instanceExtensions:[],instanceLayers:[],devices:[{name:'Adreno Fixture',apiVersion:'1.4.0',driverVersionRaw:1,driverVersionText:'512.1',vendorId:'0x5143',vendorIdRaw:20803,deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU',deviceExtensionStatus:'available',deviceExtensionReason:'',extendedQueryStatus:'available',extendedQueryReason:'',vulkan14Status:'available',vulkan14Reason:'',imageFormatQueryStatus:'available',imageFormatQueryReason:'',deviceLayers:[],extensions:[{name:'VK_KHR_video_queue',scope:'Device',specVersion:8,supported:true}],features:[],detailedProperties:[{section:'Vulkan Query Status',name:'Queue Family Properties 2 query',value:'Available'},{section:'Vulkan Query Status',name:'Image Format Properties 2 query',value:'Available'},{section:'Image Format Properties2 Query Diagnostics',name:'Query parameters',value:'imageType=VK_IMAGE_TYPE_2D, usage=VK_IMAGE_USAGE_TRANSFER_SRC_BIT | VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT, flags=0'},{section:'Image Format Properties2 Query Diagnostics',name:'Base image-format queries',value:'attempted=2, success=2, formatNotSupported=0, otherErrors=0'},{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · LINEAR',value:'tiling=LINEAR, extent=16384 × 16384 × 1, mipLevels=1, arrayLayers=2048, sampleCounts=0x1, maxResourceSize=4294967295'},{section:'Image Format Properties2',name:'VK_FORMAT_S8_UINT · OPTIMAL',value:'tiling=OPTIMAL, extent=16384 × 16384 × 1, mipLevels=1, arrayLayers=2048, sampleCounts=0x1, maxResourceSize=4294967295'}],imageFormatQueryResults:[{name:'VK_FORMAT_S8_UINT · LINEAR',status:'available',vkResult:0,reason:''},{name:'VK_FORMAT_S8_UINT · LINEAR · OPAQUE_FD',status:'not_applicable',vkResult:null,reason:'VK_KHR_external_memory_fd was not enumerated for this device.'},{name:'VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER',status:'not_applicable',vkResult:null,reason:'VK_ANDROID_external_memory_android_hardware_buffer was not enumerated for this device.'},{name:'VK_FORMAT_S8_UINT · OPTIMAL',status:'available',vkResult:0,reason:''},{name:'VK_FORMAT_S8_UINT · OPTIMAL · OPAQUE_FD',status:'not_applicable',vkResult:null,reason:'VK_KHR_external_memory_fd was not enumerated for this device.'},{name:'VK_FORMAT_S8_UINT · OPTIMAL · ANDROID_HARDWARE_BUFFER',status:'not_applicable',vkResult:null,reason:'VK_ANDROID_external_memory_android_hardware_buffer was not enumerated for this device.'}],limits:[],memoryHeaps:[],memoryTypes:[],queues:[{index:0,count:1,timestampBits:64,flags:3,flagsU64:'3',flagsCanonical:'VK_QUEUE_GRAPHICS_BIT | VK_QUEUE_COMPUTE_BIT',graphics:true,compute:true,transfer:false,sparse:false,protected:false,videoDecode:false,videoEncode:false,opticalFlow:false,dataGraph:false,unknownFlags:0,granularity:'1 × 1 × 1',videoCodecOperations:0,videoCodecOperationsU64:'0',videoCodecOperationsCanonical:'VK_VIDEO_CODEC_OPERATION_NONE_KHR',videoCodecQueryStatus:'available',videoCodecQueryReason:''}],formats:[],surface:{available:true,presentationSupported:true,colorSpaceExtensionAvailable:false,colorSpaceExtensionEnabled:false,formatQueryResult:0,formatQueryResultSecond:0,formatQuerySecondAttempted:false,formatQuerySafetyRejected:false,capabilities:[],formats:[],presentModes:[],presentationQueues:[]},profileEvaluation:[]}],profileCatalog:[]},
 };
 p.reportText=reportText(p);return p;
}
async function call(path,{method='GET',body,origin,contentType='application/json'}={}){
 const headers={};if(origin)headers.origin=origin;if(body!==undefined)headers['content-type']=contentType;
 return worker.fetch(new Request(`https://vulkanscope-database-api.vulkanscope.workers.dev${path}`,{method,headers,body:body===undefined?undefined:(typeof body==='string'?body:JSON.stringify(body))}),env);
}
let r=await call('/v1/health');
assert.equal(r.status,200);
let j=await r.json();
assert.equal(j.normalizerVersion,16);
assert.match(j.publishedVulkanSpec,/1\.4\.362/);
assert.match(j.producerQueryBaseline,/1\.0\.19/);
assert.match(j.compatibleProducer,/1\.0\.19\+/);

r=await call('/v1/reports');
assert.equal(r.status,200);
j=await r.json();
assert.match(j.producerQueryBaseline,/1\.0\.19/);
assert.match(j.compatibleProducer,/1\.0\.19\+/);

const current=fixture();
current.application.version='1.0.19';
current.application.versionCode=1019;
current.vulkan.registryBaseline='Vulkan 1.4.362';
current.vulkan.headerBaseline='Vulkan 1.4.362 compile headers; validated query catalog Vulkan 1.4.362';
current.technicalReport.registryCoverage.baseline='Vulkan 1.4.362';
current.technicalReport.registryCoverage.headerBaseline=current.vulkan.headerBaseline;
current.reportText=reportText(current);
r=await call('/v1/reports',{method:'POST',body:current});
assert.equal(r.status,201);
const accepted=await r.json();
assert.match(accepted.id,/^[a-f0-9]{64}$/);
assert.equal(accepted.status,'accepted');

const below=structuredClone(current);
below.application.version='1.0.18';
below.application.versionCode=1018;
below.reportText=reportText(below);
r=await call('/v1/reports',{method:'POST',body:below});
assert.equal(r.status,400,'VulkanScope 1.0.18 must be rejected by the 1.0.19 floor');
assert.match(await r.text(),/1\.0\.19 or newer/);

const oldMajor=structuredClone(current);
oldMajor.application.version='0.80.12';
oldMajor.application.versionCode=812;
oldMajor.reportText=reportText(oldMajor);
r=await call('/v1/reports',{method:'POST',body:oldMajor});
assert.equal(r.status,400,'every producer below 1.0.19 must be rejected before generic validation');
assert.match(await r.text(),/1\.0\.19 or newer/);

const badIdentity=structuredClone(current);
badIdentity.application.versionCode=1018;
badIdentity.reportText=reportText(badIdentity);
r=await call('/v1/reports',{method:'POST',body:badIdentity});
assert.equal(r.status,400);
assert.match(await r.text(),/producer_identity/);

const malformedCurrent={application:{name:'VulkanScope',version:'1.0.19',versionCode:1019}};
r=await call('/v1/reports',{method:'POST',body:malformedCurrent});
assert.equal(r.status,400);
assert.match(await r.text(),/Incomplete or invalid VulkanScope submission schema/);

r=await call(`/v1/reports/${accepted.id}?compact=1`);
assert.equal(r.status,200);
const compact=await r.json();
assert.equal(compact.application.version,'1.0.19');
assert.equal(compact.id,accepted.id);
assert.ok(compact.submittedAt);

// Historical stored rows remain readable even though their producer is below the new POST floor.
const historicalId='a'.repeat(64);
const historicalPayload=fixture();
historicalPayload.application.version='0.80.9';
historicalPayload.application.versionCode=809;
historicalPayload.reportText=reportText(historicalPayload);
env.DB.rows.set(historicalId,{id:historicalId,submitted_at:'2026-01-01T00:00:00.000Z',payload_json:JSON.stringify(historicalPayload)});
r=await call(`/v1/reports/${historicalId}?compact=1`);
assert.equal(r.status,200);
const historical=await r.json();
assert.equal(historical.application.version,'0.80.9');
assert.equal(historical.submittedAt,'2026-01-01T00:00:00.000Z');

r=await call('/v1/reports',{method:'POST',body:current,contentType:'text/plain'});
assert.equal(r.status,415);
r=await call('/v1/reports',{method:'POST',body:current,origin:'https://evil.example'});
assert.equal(r.status,403);
r=await call('/v1/reports',{method:'PUT'});
assert.equal(r.status,405);
r=await call('/nope');
assert.equal(r.status,404);
const huge='{"x":"'+'a'.repeat(2*1024*1024+64)+'"}';
r=await call('/v1/reports',{method:'POST',body:huge});
assert.equal(r.status,413);

console.log('PASS Worker 1.0.10 contract: 1.0.19 floor/current producer + historical reads + transport/security basics');
