#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root');p.add_argument('--skip-version',action='store_true');a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
index=(root/'index.html').read_text(encoding='utf-8')
worker=(root/'worker/src/index.js').read_text(encoding='utf-8')
build=(root/'tools/build_index.py').read_text(encoding='utf-8')
pkg=json.loads((root/'worker/package.json').read_text(encoding='utf-8'))
asset=root/'assets/app.v03924.js'
app=asset.read_text(encoding='utf-8') if asset.is_file() else ''
if not a.skip_version:
    if 'VulkanScope Database <strong>0.39.24</strong>' not in index: errors.append('Database 0.39.24 footer missing')
    if pkg.get('version')!='0.39.24': errors.append('Worker package version must be 0.39.24')
if './assets/app.v03924.js' not in index or './config.js?v=03924' not in index: errors.append('0.39.22 cache-busted frontend references missing')
for token in ['id="databaseLoading"','role="status"','aria-live="polite"','id="databaseLoadingDetail"','id="databaseLoadingProgress"']:
    if token not in index: errors.append('loading surface missing '+token)
for token in ['id="pageScrollControls"','id="pageScrollUp"','id="pageScrollDown"','aria-label="Scroll page up"','aria-label="Scroll page down"']:
    if token not in index: errors.append('page scroll control missing '+token)
for token in ['setDatabaseLoading','updatePageScrollControls','databaseLoadingProgress','pageScrollUp','pageScrollDown','window.scrollBy','prefers-reduced-motion','ResizeObserver']:
    if token not in app: errors.append('frontend loading/scroll behavior missing '+token)
if 'VulkanScope 0.80.10 · Vulkan 1.4.362' not in app or "producerQueryBaseline:'VulkanScope 0.80.10 · Vulkan 1.4.362'" not in worker: errors.append('current producer baseline is not 0.80.9')
if 'VulkanScope 0.80.3+' not in worker or 'VulkanScope 0.80.3+' not in build: errors.append('new-submission floor metadata is not 0.80.3+')
if 'producerAtLeast0803=p=>{const v=producerVersion(p);return!!v&&(v.minor>80||v.minor===80&&v.patch>=3)}' not in worker or 'supportedProducer=p=>producerAtLeast0803(p)' not in worker: errors.append('Worker submission floor does not reject versions below 0.80.3')
if 'if(v.minor===80)return p.application.versionCode===800+v.patch' not in worker: errors.append('0.80.x versionCode identity contract missing')
for token in ['canonicalPhysicalDeviceType','Integrated GPU','VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU']:
    if token not in worker or token not in app: errors.append('historical device-type canonicalization missing '+token)
for path in ['rules/0.39.22_VULKANSCOPE_0.80.8_LOADING_FLOOR_CANONICAL_TYPE_AUDIT.md','tools/test_0808_floor_loading_scroll_state_machine.py','tools/test_0808_floor_loading_scroll_negative_mutations.py']:
    if not (root/path).is_file(): errors.append('missing 0.39.22 release gate '+path)
if errors:raise SystemExit('FAIL Database 0.39.24 contract\n- '+'\n- '.join(errors))
print('PASS Database 0.39.24 retained loading/scroll/floor/device-type contract')
