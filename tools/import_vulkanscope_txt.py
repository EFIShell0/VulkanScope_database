from pathlib import Path
import argparse,json,re,hashlib,datetime
def val(lines,prefix,default="Unknown"):
    for line in lines:
        if line.startswith(prefix): return line[len(prefix):].strip()
    return default
def status(value):
    x=value.strip().lower()
    if x in {"true","supported","available","yes","pass"}: return "supported"
    if x in {"false","not supported","unsupported","no","fail"}: return "unsupported"
    if "not applicable" in x or x == "not_applicable": return "not_applicable"
    if "unavailable" in x or "not available" in x: return "unavailable"
    if "unknown" in x or "not queried" in x or "not reported" in x: return "unknown"
    return "available"
def append_capability(items,seen,section,name,value,state):
    key=(section,name)
    if key in seen: return
    seen.add(key)
    items.append({"section":section,"name":name,"value":value,"status":state})
ap=argparse.ArgumentParser()
ap.add_argument("txt")
ap.add_argument("--output",default=None)
a=ap.parse_args()
p=Path(a.txt); lines=p.read_text(encoding="utf-8",errors="replace").splitlines()
device_line=next((x for x in lines if x.startswith("DEVICE #1: ")),None)
gpu_name=(device_line.split(": ",1)[1] if device_line else val(lines,"GPU: "))
api=val(lines,"API: ")
driver_version=val(lines,"Driver version: ")
vendor_id=val(lines,"Vendor: ")
device_id=val(lines,"Device ID: ")
android=val(lines,"Android: ")
manufacturer_model=android.split(",")[0] if "," in android else android
parts=manufacturer_model.split(" ",1)
manufacturer=parts[0] if parts else "Unknown"; model=parts[1] if len(parts)>1 else "Unknown"
sdkm=re.search(r"SDK\s+(\d+)",android); sdk=int(sdkm.group(1)) if sdkm else 0
extensions=[]; capabilities=[]; seen=set(); section=""
for raw in lines:
    line=raw.strip()
    if not line: continue
    if re.fullmatch(r"[A-Z][A-Z0-9 &/()._-]+(?: \([^\r\n]*\))?",line) and not line.startswith("VK_"):
        section=re.sub(r" \([^\r\n]*\)$","",line); continue
    prop=re.match(r"^\[([^\]]+)\] (.+?) = (.*)$",line)
    if prop:
        append_capability(capabilities,seen,prop.group(1),prop.group(2),prop.group(3),status(prop.group(3))); continue
    if section=="DEVICE EXTENSIONS":
        m=re.match(r"^(VK_[^ |]+) \| ([^|]+) \| spec (\d+)$",line)
        if m: extensions.append({"name":m.group(1),"scope":m.group(2).strip(),"specVersion":int(m.group(3)),"status":"supported"}); continue
    if section=="FEATURES":
        m=re.match(r"^(.+?) = (true|false)$",line,re.I)
        if m: append_capability(capabilities,seen,"FEATURES",m.group(1),m.group(2),"supported" if m.group(2).lower()=="true" else "unsupported"); continue
    if section=="FORMATS":
        m=re.match(r"^([^:]+): (SUPPORTED|NOT SUPPORTED)(?:, (.*))?$",line)
        if m: append_capability(capabilities,seen,"FORMATS",m.group(1),m.group(3) or m.group(2),"supported" if m.group(2)=="SUPPORTED" else "unsupported"); continue
    if section=="SURFACE":
        m=re.match(r"^Available=(true|false), presentation=(true|false)$",line,re.I)
        if m:
            append_capability(capabilities,seen,"SURFACE","Available",m.group(1),"available" if m.group(1).lower()=="true" else "unavailable")
            append_capability(capabilities,seen,"SURFACE","Presentation supported",m.group(2),"supported" if m.group(2).lower()=="true" else "unsupported")
            continue
        m=re.match(r"^([^|]+) \| ([^|]+) \| ([^|]+) \| (SUPPORTED|NOT SUPPORTED) \| (.*)$",line)
        if m: append_capability(capabilities,seen,"SURFACE FORMATS",f"{m.group(1).strip()} / {m.group(2).strip()}",f"{m.group(3).strip()} · {m.group(5).strip()}","supported" if m.group(4)=="SUPPORTED" else "unsupported"); continue
        m=re.match(r"^(.+?) = (.*)$",line)
        if m: append_capability(capabilities,seen,"SURFACE",m.group(1),m.group(2),status(m.group(2))); continue
    if section=="LIMITS":
        m=re.match(r"^(.+?) = (.*)$",line)
        if m: append_capability(capabilities,seen,"LIMITS",m.group(1),m.group(2),status(m.group(2))); continue
base={"schemaVersion":1,"submittedAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"application":{"name":"VulkanScope","version":val(lines,"Application version: "),"versionCode":val(lines,"Application version code: ")},"device":{"manufacturer":manufacturer,"model":model,"android":android,"sdk":sdk,"applicationAbi":val(lines,"Application ABI: "),"supportedAbis":[x.strip() for x in val(lines,"Supported device ABIs: ","").split(",") if x.strip()]},"gpu":{"name":gpu_name,"vendor":"Unknown","vendorId":vendor_id,"deviceId":device_id},"driver":{"name":val(lines,"Driver mode: "),"version":driver_version,"mode":val(lines,"Driver mode: ")},"vulkan":{"loaderInstanceApiVersion":val(lines,"Loader / instance API: "),"deviceApiVersion":api,"registryBaseline":val(lines,"Baseline=","Unknown / report-defined")},"collection":{"status":"available"},"extensions":extensions,"capabilities":capabilities}
canonical=json.dumps(base,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
base["id"]=hashlib.sha256(canonical).hexdigest()
out=Path(a.output) if a.output else Path("data/reports")/f"{base['id']}.json"
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(base,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(out)
