#!/usr/bin/env python3
import json,re,tempfile,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def accepted(v):
    a=v.split('.')
    if len(a)!=3:return False
    major,minor,patch=map(int,a)
    return major>0 or minor>80 or (minor==80 and patch>=3)
for v,want in [('0.80.0',False),('0.80.1',False),('0.80.2',False),('0.80.3',True),('0.80.9',True),('0.81.0',True),('0.41.46',False)]:
    if accepted(v)!=want:raise SystemExit('FAIL producer floor '+v)
with tempfile.TemporaryDirectory(prefix='vsdb3923-enc-') as d:
    out=Path(d)/'encyclopedia.js'
    subprocess.run([sys.executable,str(root/'tools/generate_encyclopedia_03924.py'),'--registry',str(root/'registry/upstream/vk.xml'),'--curated',str(root/'registry/encyclopedia_curated.json'),'--output',str(out)],check=True,stdout=subprocess.DEVNULL)
    expected=(root/'assets/encyclopedia.v03924.js').read_bytes()
    if out.read_bytes()!=expected:raise SystemExit('FAIL Encyclopedia regeneration drift')
text=(root/'assets/encyclopedia.v03924.js').read_text(encoding='utf-8')
prefix='window.VULKANSCOPE_ENCYCLOPEDIA=';payload=text[len(prefix):].rstrip().removesuffix(';')
data=json.loads(payload)
want={'commands':842,'tokens':6248,'types':2461,'extensions':476,'vkResults':50}
if data.get('counts')!=want:raise SystemExit('FAIL Encyclopedia census')
for symbol,family in [('VK_SUCCESS','vkResults'),('vkGetPhysicalDeviceFeatures2','commands'),('VkPhysicalDeviceProperties2','types'),('VK_KHR_swapchain','extensions')]:
    rows=data[family]
    found=any((x.get('name') if isinstance(x,dict) else x[0])==symbol for x in rows)
    if not found:raise SystemExit('FAIL Encyclopedia symbol '+symbol)
print('PASS Database 0.39.25 producer-floor/Encyclopedia state machine')
