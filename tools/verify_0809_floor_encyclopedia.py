#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root');p.add_argument('--skip-version',action='store_true');a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
index=(root/'index.html').read_text(encoding='utf-8')
worker=(root/'worker/src/index.js').read_text(encoding='utf-8')
pkg=json.loads((root/'worker/package.json').read_text(encoding='utf-8'))
app_path=root/'assets/app.v1007.js'; enc_path=root/'assets/encyclopedia.v03924.js'
app=app_path.read_text(encoding='utf-8') if app_path.is_file() else ''
enc=enc_path.read_text(encoding='utf-8') if enc_path.is_file() else ''
errors=[]
if not a.skip_version:
    if 'VulkanScope Database <strong>1.0.7</strong>' not in index: errors.append('Database 1.0.7 footer missing')
    if pkg.get('version')!='1.0.7': errors.append('Worker package version must be 1.0.1')
if './assets/encyclopedia.v03924.js' not in index or './assets/app.v1007.js' not in index: errors.append('0.39.25 Encyclopedia/app assets are not loaded')
if "['encyclopedia','Encyclopedia']" not in app: errors.append('Encyclopedia main navigation destination missing')
if 'renderEncyclopedia' not in app or 'encyclopediaSearch' not in app: errors.append('Encyclopedia renderer/search missing')
for token in ['All','VkResult','Commands','VK_*','Types','Extensions']:
    if token not in app: errors.append('Encyclopedia category missing '+token)
for token in ['VULKANSCOPE_ENCYCLOPEDIA','"registryBaseline":"Vulkan 1.4.362"','"commands":842','"tokens":6248','"types":2461','"extensions":476','"vkResults":50']:
    if token not in enc: errors.append('Encyclopedia locked corpus missing '+token)
if 'Registry/reference presence is not runtime capability evidence.' not in app: errors.append('registry/runtime evidence separation missing')
if 'producerAtLeast0803=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,0,80,3)}' not in worker or 'supportedProducer=p=>producerAtLeast0803(p)' not in worker: errors.append('Worker producer floor is not exactly 0.80.3')
if 'VulkanScope 0.80.3+' not in worker: errors.append('Worker compatibility metadata is not 0.80.3+')
if 'VulkanScope 0.80.3 or newer is required for new submissions' not in worker: errors.append('floor rejection message is not 0.80.3')
if errors: raise SystemExit('FAIL Database retained floor/Encyclopedia contract\n- '+'\n- '.join(errors))
print('PASS Database 1.0.7 retained floor/Encyclopedia contract')
