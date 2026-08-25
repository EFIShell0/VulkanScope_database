from pathlib import Path
import json,hashlib,datetime
root=Path(__file__).resolve().parents[1]
reports=[]
seen=set()
for p in sorted((root/"data"/"reports").glob("*.json")):
    d=json.loads(p.read_text(encoding="utf-8"))
    if d.get("schemaVersion")!=1: raise SystemExit(f"{p}: unsupported schemaVersion")
    rid=d.get("id","")
    if len(rid)!=64 or any(c not in "0123456789abcdef" for c in rid): raise SystemExit(f"{p}: invalid id")
    if rid in seen: raise SystemExit(f"{p}: duplicate report id")
    seen.add(rid)
    reports.append({"id":rid,"submittedAt":d.get("submittedAt",""),"gpu":d.get("gpu",{}),"device":d.get("device",{}),"driver":d.get("driver",{}),"vulkan":d.get("vulkan",{}),"collection":d.get("collection",{}),"capabilityCount":len(d.get("capabilities",[])),"extensionCount":len(d.get("extensions",[]))})
idx={"schemaVersion":1,"databaseVersion":"0.39.1","normalizerVersion":15,"publishedVulkanSpec":"Vulkan 1.4.360 (2026-08-14)","vulkanRegistryBaseline":"VulkanScope producer/query baseline 1.4.360","producerQueryBaseline":"VulkanScope 0.41.5 · Vulkan 1.4.360","compatibleProducer":"VulkanScope 0.32.4+ · schema 2 / technical report 3","generatedAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"reports":reports}
(root/"data"/"index.json").write_text(json.dumps(idx,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Indexed {len(reports)} report(s)")