from pathlib import Path
import argparse,json,re,hashlib,datetime
def val(lines,prefix,default="Unknown"):
    for line in lines:
        if line.startswith(prefix): return line[len(prefix):].strip()
    return default
def status(value):
    x=value.strip().lower()
    if x in {"true","supported","available","yes"}: return "supported"
    if x in {"false","not supported","unsupported","no"}: return "unsupported"
    if "unavailable" in x or "not applicable" in x: return "unavailable"
    return "unknown"
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
extensions=[]; capabilities=[]; section=None
for line in lines:
    if line=="DEVICE EXTENSIONS": section="extensions"; continue
    if line=="DETAILED QUERY RESULTS" or line.startswith("DETAILED QUERY RESULTS ("): section="details"; continue
    if line and line==line.upper() and not line.startswith("[") and line not in {"DEVICE EXTENSIONS","DETAILED QUERY RESULTS"}: section=None
    if section=="extensions" and line.startswith("VK_"):
        parts=[x.strip() for x in line.split("|")]
        spec=parts[2].removeprefix("spec ").strip() if len(parts)>2 else "Unknown"
        extensions.append({"name":parts[0],"scope":parts[1] if len(parts)>1 else "device","specVersion":spec,"status":"supported"})
    elif section=="details" and line.startswith("[") and "] " in line and " = " in line:
        sec,rest=line[1:].split("] ",1); name,value=rest.split(" = ",1)
        capabilities.append({"section":sec,"name":name,"value":value,"status":status(value)})
base={"schemaVersion":1,"submittedAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"application":{"name":"VulkanScope","version":val(lines,"Application version: "),"versionCode":val(lines,"Application version code: ")},"device":{"manufacturer":manufacturer,"model":model,"android":android,"sdk":sdk,"applicationAbi":val(lines,"Application ABI: "),"supportedAbis":[x.strip() for x in val(lines,"Supported device ABIs: ","").split(",") if x.strip()]},"gpu":{"name":gpu_name,"vendor":"Unknown","vendorId":vendor_id,"deviceId":device_id},"driver":{"name":val(lines,"Driver mode: "),"version":driver_version,"mode":val(lines,"Driver mode: ")},"vulkan":{"loaderInstanceApiVersion":val(lines,"Loader / instance API: "),"deviceApiVersion":api,"registryBaseline":val(lines,"Baseline=","1.4.357")},"collection":{"status":"available"},"extensions":extensions,"capabilities":capabilities}
canonical=json.dumps(base,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
base["id"]=hashlib.sha256(canonical).hexdigest()
out=Path(a.output) if a.output else Path("data/reports")/f"{base['id']}.json"
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(base,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(out)