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
asset=root/'assets/app.v1008.js'
app=asset.read_text(encoding='utf-8') if asset.is_file() else ''
if not a.skip_version:
    if 'VulkanScope Database <strong>1.0.8</strong>' not in index: errors.append('Database 0.39.25 footer missing')
    if pkg.get('version')!='1.0.8': errors.append('Worker package version must be 1.0.1')
if './assets/app.v1008.js' not in index or './config.js?v=1008' not in index: errors.append('0.39.22 cache-busted frontend references missing')
for token in ['id="databaseLoading"','role="status"','aria-live="polite"','id="databaseLoadingDetail"','id="databaseLoadingProgress"']:
    if token not in index: errors.append('loading surface missing '+token)
for token in ['id="pageScrollControls"','id="pageScrollUp"','id="pageScrollDown"','aria-label="Scroll page up"','aria-label="Scroll page down"']:
    if token not in index: errors.append('page scroll control missing '+token)
for token in ['setDatabaseLoading','updatePageScrollUi','databaseLoadingProgress','pageScrollUp','pageScrollDown','window.scrollBy','prefers-reduced-motion','ResizeObserver']:
    if token not in app: errors.append('frontend loading/scroll behavior missing '+token)
if 'VulkanScope 1.0.15 · Vulkan 1.4.362' not in app or "producerQueryBaseline:'VulkanScope 1.0.15 · Vulkan 1.4.362'" not in worker: errors.append('current producer baseline is not 1.0.1')
if 'VulkanScope 0.80.3+' not in worker or 'VulkanScope 0.80.3+' not in build: errors.append('new-submission floor metadata is not 0.80.3+')
if 'producerAtLeast0803=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,0,80,3)}' not in worker or 'supportedProducer=p=>producerAtLeast0803(p)' not in worker: errors.append('Worker submission floor does not reject versions below 0.80.3')
if 'if(v.major===0&&v.minor===80)return p.application.versionCode===800+v.patch' not in worker: errors.append('0.80.x versionCode identity contract missing')
for token in ['canonicalPhysicalDeviceType','Integrated GPU','VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU']:
    if token not in worker or token not in app: errors.append('historical device-type canonicalization missing '+token)
for path in ['rules/0.39.22_VULKANSCOPE_0.80.8_LOADING_FLOOR_CANONICAL_TYPE_AUDIT.md','tools/test_0808_floor_loading_scroll_state_machine.py','tools/test_0808_floor_loading_scroll_negative_mutations.py']:
    if not (root/path).is_file(): errors.append('missing 0.39.22 release gate '+path)
if errors:raise SystemExit('FAIL Database retained loading/scroll/floor contract\n- '+'\n- '.join(errors))
print('PASS Database 1.0.8 retained loading/scroll/floor/device-type contract')
