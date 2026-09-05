#!/usr/bin/env python3
import argparse,hashlib,json,re
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',default='.');ap.add_argument('--skip-version',action='store_true');args=ap.parse_args();root=Path(args.root).resolve();errors=[]
def need(c,m):
    if not c:errors.append(m)
def text(p):
    q=root/p
    return q.read_text(encoding='utf-8',errors='ignore') if q.is_file() else ''
package=json.loads(text('worker/package.json'))
if not args.skip_version: need(package.get('version')=='0.39.25','Database version is not 0.39.25')
lock=json.loads(text('registry/registry_lock.json'));reg=(root/lock.get('bundledRegistryPath','registry/upstream/vk.xml')).read_bytes()
need(lock.get('apiBaseline')=='Vulkan 1.4.362' and lock.get('registryRef')=='1.4.362','Database registry baseline/ref not 1.4.362')
need(lock.get('registrySha256')=='cf31c965cf6e788697139601da0c7e02a75a9b6c7ac764e7641f5521ffd9da06'==hashlib.sha256(reg).hexdigest(),'Database registry SHA mismatch')
need(lock.get('headerVersion')==362 and lock.get('headerCommit')=='ee2ec5fd83dafce291024683b50dc89219333076','Database header provenance is not 1.4.362')
index=text('index.html'); need('Database <strong>0.39.25</strong>' in index and 'encyclopedia.v03924.js' in index and 'app.v03925.js' in index,'index asset/version identity not 0.39.25')
worker=text('worker/src/index.js'); need("VulkanScope 0.80.10 · Vulkan 1.4.362" in worker,'Worker producer/query baseline not 0.80.10 / 1.4.362'); need('Vulkan 1.4.362 (2026-09-04)' in worker,'Worker published Vulkan spec not 1.4.362'); need('VulkanScope 0.80.3 or newer is required for new submissions' in worker,'0.80.3 producer floor drifted'); need('producerAtLeast08010' in worker and "producerAtLeast08010(p)?'1.4.362':'1.4.361'" in worker,'Worker does not preserve 0.80.3-0.80.9 1.4.361 compatibility while requiring 1.4.362 for 0.80.10+')
app=text('assets/app.v03925.js'); need('VulkanScope 0.80.10 · Vulkan 1.4.362' in app and 'Vulkan 1.4.362 (2026-09-04)' in app,'frontend baseline not 0.80.10 / 1.4.362'); need('Vulkan 1.4.362 reference' in app and 'locked Vulkan 1.4.362 registry' in app and 'Vulkan 1.4.361 reference' not in app,'Database Encyclopedia visible copy is stale')
asset=text('assets/encyclopedia.v03924.js'); m=re.search(r'window\.VULKANSCOPE_ENCYCLOPEDIA=(\{.*\});\s*$',asset,re.S); need(bool(m),'Encyclopedia payload missing')
if m:
    data=json.loads(m.group(1)); need(data.get('registryBaseline')=='Vulkan 1.4.362','Encyclopedia registry baseline not 1.4.362'); need(data.get('counts')=={'commands':842,'tokens':6248,'types':2461,'extensions':476,'vkResults':50},f'Encyclopedia census mismatch {data.get("counts")}')
cur=json.loads(text('registry/encyclopedia_curated.json')); need(cur.get('appVersion')=='0.80.10' and cur.get('registryBaseline')=='Vulkan 1.4.362','curated Encyclopedia metadata not 0.80.10 / 1.4.362')
gen=text('tools/generate_encyclopedia_03924.py'); need("'tokens':6248" in gen and "'types':2461" in gen and "'extensions':476" in gen,'Database Encyclopedia generator census not 1.4.362')
if errors:
    print('FAIL Database 0.39.25 / Vulkan 1.4.362 contract')
    for e in errors:print('-',e)
    raise SystemExit(1)
print('PASS Database 0.39.25 / Vulkan 1.4.362 contract: producer=0.80.10 floor=0.80.3 symbols=842/6248/2461 extensions=476')
