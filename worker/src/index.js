const MAX_BODY=2*1024*1024;
const forbidden=/\b(imei|android[_ -]?id|serial(?: number)?|mac(?: address)?|auth(?:entication)?[_ -]?token|access[_ -]?token|refresh[_ -]?token|private[_ -]?file[_ -]?path)\b/i;
const json=(body,status=200,origin="*")=>new Response(JSON.stringify(body),{status,headers:{"content-type":"application/json; charset=utf-8","access-control-allow-origin":origin,"cache-control":"no-store","x-content-type-options":"nosniff"}});
const text=v=>typeof v==="string"?v:"";
const normalizeReport=p=>{const lines=p.reportText.split(/\r?\n/);const capabilities=[];const extensions=[];let section="";for(const line of lines){if(/^[A-Z][A-Z0-9 &/()._-]+$/.test(line.trim())){section=line.trim();continue}const prop=line.match(/^\[([^\]]+)\] (.+?) = (.*)$/);if(prop)capabilities.push({section:prop[1],name:prop[2],value:prop[3],status:"available"});if(section==="DEVICE EXTENSIONS"){const ext=line.match(/^(VK_[^ |]+) \| ([^|]+) \| spec (\d+)$/);if(ext)extensions.push({name:ext[1],scope:ext[2].trim(),specVersion:Number(ext[3]),status:"supported"})}}return {capabilities,extensions}};
const sha256=async value=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value)))).map(x=>x.toString(16).padStart(2,"0")).join("");
export default {async fetch(request,env){
 const url=new URL(request.url);const origin=env.ALLOWED_ORIGIN||"*";
 if(request.method==="OPTIONS")return new Response(null,{status:204,headers:{"access-control-allow-origin":origin,"access-control-allow-methods":"GET,POST,OPTIONS","access-control-allow-headers":"content-type"}});
 if(url.pathname==="/v1/health"&&request.method==="GET")return json({status:"ok",schemaVersion:2},200,origin);
 if(url.pathname==="/v1/reports"&&request.method==="GET"){
  const limit=Math.min(Math.max(Number(url.searchParams.get("limit"))||100,1),500);
  const {results}=await env.DB.prepare("SELECT id,submitted_at,schema_version,gpu_name,vendor_id,device_id,driver_mode,driver_version,device_api_version,manufacturer,model FROM reports ORDER BY submitted_at DESC LIMIT ?").bind(limit).all();
  return json({schemaVersion:2,reports:results},200,origin);
 }
 if(url.pathname.startsWith("/v1/reports/")&&request.method==="GET"){
  const id=url.pathname.slice(12);if(!/^[a-f0-9]{64}$/.test(id))return json({error:"Invalid report id"},400,origin);
  const row=await env.DB.prepare("SELECT payload_json,submitted_at,id FROM reports WHERE id=?").bind(id).first();if(!row)return json({error:"Report not found"},404,origin);
  const payload=JSON.parse(row.payload_json);payload.id=row.id;payload.submittedAt=row.submitted_at;Object.assign(payload,normalizeReport(payload));return json(payload,200,origin);
 }
 if(url.pathname==="/v1/reports"&&request.method==="POST"){
  const length=Number(request.headers.get("content-length")||0);if(length>MAX_BODY)return json({error:"Report exceeds 2 MiB"},413,origin);
  const raw=await request.text();if(new TextEncoder().encode(raw).length>MAX_BODY)return json({error:"Report exceeds 2 MiB"},413,origin);
  let p;try{p=JSON.parse(raw)}catch{return json({error:"Invalid JSON"},400,origin)}
  if(p?.schemaVersion!==2||!p.application||!p.device||!p.gpu||!p.driver||!p.vulkan||!p.collection||typeof p.reportText!=="string")return json({error:"Incomplete VulkanScope submission schema"},400,origin);
  if(p.reportText.length<1000)return json({error:"Technical report is incomplete"},400,origin);
  if(forbidden.test(raw))return json({error:"Submission contains a forbidden personal identifier field"},400,origin);
  const canonical=JSON.stringify(p);const id=await sha256(canonical);const now=new Date().toISOString();
  await env.DB.prepare("INSERT OR IGNORE INTO reports(id,submitted_at,schema_version,gpu_name,vendor_id,device_id,driver_mode,driver_version,device_api_version,manufacturer,model,payload_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)").bind(id,now,2,text(p.gpu.name)||"Unknown",text(p.gpu.vendorId)||"Unknown",text(p.gpu.deviceId)||"Unknown",text(p.driver.mode)||"Unknown",text(p.driver.version)||"Unknown",text(p.vulkan.deviceApiVersion)||"Unknown",text(p.device.manufacturer)||"Unknown",text(p.device.model)||"Unknown",canonical).run();
  return json({id,submittedAt:now,status:"accepted"},201,origin);
 }
 return json({error:"Not found"},404,origin);
}};
