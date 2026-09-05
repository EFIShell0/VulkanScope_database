from pathlib import Path
import hashlib,json,sys,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
lock=json.loads((root/'registry/registry_lock.json').read_text(encoding='utf-8'))
p=root/lock['snapshotPath']
b=p.read_bytes(); errors=[]
def check(v,m):
    if not v: errors.append(m)
check(hashlib.sha256(b).hexdigest()==lock['snapshotSha256'],'vk.xml SHA-256 does not match registry lock')
r=ET.fromstring(b)
header=[]
for t in r.findall("./types/type"):
    if t.get('api') in ('vulkan,vulkanbase','vulkan') and t.findtext('name')=='VK_HEADER_VERSION':
        text=''.join(t.itertext());
        import re
        m=re.search(r'VK_HEADER_VERSION\s+(\d+)',text)
        if m: header.append(int(m.group(1)))
check(lock['headerVersion'] in header,f"expected VK_HEADER_VERSION {lock['headerVersion']}, got {header}")
exts=[e for e in r.findall('./extensions/extension') if 'vulkan' in e.get('supported','').split(',') and e.get('supported')!='disabled']
check(len(exts)==lock['registeredVulkanExtensionCount'],f"registered Vulkan extension count {len(exts)} != {lock['registeredVulkanExtensionCount']}")
by_name={e.get('name'):e for e in exts}
e=by_name.get(lock['requiredCurrentExtension']);check(e is not None,'required current Vulkan extension missing')
if e is not None:
    names={x.get('name') for req in e.findall('./require') for x in req if x.get('name')}
    check(lock['requiredCurrentFeatureStruct'] in names,'required current feature struct not required by extension')
if errors:
    print('\n'.join('FAIL '+x for x in errors));sys.exit(1)
print(f"PASS Vulkan registry lock api={lock['apiVersion']} header={lock['headerVersion']} extensions={len(exts)} sha256={lock['snapshotSha256']}")
