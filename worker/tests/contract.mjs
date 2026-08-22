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
  application:{name:'VulkanScope',version:'0.34.1',versionCode:342,packageName:'com.efishell.vulkanscope',applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a']},
  device:{manufacturer:'Example',brand:'Example',model:'Phone',device:'phone',product:'phone',androidRelease:'17',sdk:37,securityPatch:'2026-08-01'},
  gpu:{name:'Adreno Fixture',vendorId:'0x5143',deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU'},
  driver:{mode:'System Vulkan driver',version:'512.1',rawVersion:'1'},
  vulkan:{loaderInstanceApiVersion:'1.4.0',deviceApiVersion:'1.4.0',registryBaseline:'1.4.360',headerBaseline:'1.4.360',reportSchema:'3'},
  collection:{status:'available',error:null,deviceCount:1},
  technicalReport:{schemaVersion:3,loaderInstanceApiVersion:'1.4.0',driverMode:'System Vulkan driver',collectionError:null,applicationAbi:'arm64-v8a',supportedDeviceAbis:['arm64-v8a'],display:{resolution:'2400 × 1080',refreshRate:'120 Hz',wideGamut:true,preferredWideGamut:'DISPLAY_P3',preferredWideGamutColorSpace:'DISPLAY_P3',hdrTypes:[],hdrCapabilityStatus:'unavailable',minLuminance:'Unavailable',maxLuminance:'Unavailable',averageLuminance:'Unavailable',modes:[]},registryCoverage:{baseline:'1.4.360',mode:'registry-driven',implementedPhysicalDeviceStructCount:109,validatedRuntimeQueryGroupCount:104,runtimeExtensionTokenCount:268,catalogSchemaVersion:1,reportSchema:'3',headerBaseline:'1.4.360',instanceDependencyCandidateCount:1,implementedPhysicalDeviceStructs:[],validatedRuntimeQueryGroups:[]},instanceExtensions:[],instanceLayers:[],devices:[{name:'Adreno Fixture',apiVersion:'1.4.0',driverVersionRaw:1,driverVersionText:'512.1',vendorId:'0x5143',vendorIdRaw:20803,deviceId:'0x0001',deviceType:'VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU',deviceExtensionStatus:'available',deviceExtensionReason:'',extendedQueryStatus:'available',extendedQueryReason:'',vulkan14Status:'available',vulkan14Reason:'',deviceLayers:[],extensions:[],features:[],detailedProperties:[],limits:[],memoryHeaps:[],memoryTypes:[],queues:[],formats:[],surface:{available:true,presentationSupported:true,colorSpaceExtensionAvailable:false,colorSpaceExtensionEnabled:false,formatQueryResult:0,formatQueryResultSecond:0,formatQuerySecondAttempted:false,formatQuerySafetyRejected:false,capabilities:[],formats:[],presentModes:[],presentationQueues:[]},profileEvaluation:[]}],profileCatalog:[]},
 };
 p.reportText=reportText(p);return p;
}
async function call(path,{method='GET',body,origin,contentType='application/json'}={}){
 const headers={};if(origin)headers.origin=origin;if(body!==undefined)headers['content-type']=contentType;
 return worker.fetch(new Request(`https://vulkanscope-database-api.vulkanscope.workers.dev${path}`,{method,headers,body:body===undefined?undefined:(typeof body==='string'?body:JSON.stringify(body))}),env);
}
let r=await call('/v1/health');assert.equal(r.status,200);let j=await r.json();assert.equal(j.normalizerVersion,12);assert.match(j.publishedVulkanSpec,/1\.4\.360/);assert.match(j.producerQueryBaseline,/0\.34\.2/);
r=await call('/v1/reports',{method:'POST',body:fixture()});assert.equal(r.status,201,await r.text());
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
  {section:'VkPhysicalDeviceVulkan14Properties',name:'lineRasterizationMode',value:'1'}
];
metricFixture.technicalReport.devices[0].limits=[{name:'maxImageDimension2D',value:'16384'}];

metricFixture.technicalReport.devices[0].detailedProperties.push(
  {section:'CapsViewer 4.12 parity · VkPhysicalDeviceHostImageCopyPropertiesEXT',name:'pCopySrcLayouts',value:'VK_IMAGE_LAYOUT_GENERAL (raw=1), VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL (raw=6)'},
  {section:'CapsViewer 4.12 parity · VkPhysicalDeviceHostImageCopyPropertiesEXT',name:'pCopyDstLayouts',value:'VK_IMAGE_LAYOUT_GENERAL (raw=1), VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL (raw=7)'}
);
const normalized=normalizeReport(metricFixture);
assert.equal(normalized.detailedProperties.length,4,'structured detailedProperties must be authoritative');
assert.equal(normalized.detailedProperties.filter(x=>x.name==='pCopySrcLayouts'||x.name==='pCopyDstLayouts').length,2,'Host Image Copy layout arrays must survive normalization');
assert.equal(normalized.limits.length,1,'structured limits must be authoritative');
assert.equal(normalized.detailedProperties.some(x=>x.section==='DEVICE'||x.section==='SURFACE'),false,'metadata must not contaminate properties');
assert.equal(normalized.limits.some(x=>/Sparse Properties/i.test(x.section)),false,'detailed properties must not be reclassified as limits');
console.log('VulkanScope Database worker contract tests: ALL PASS');
