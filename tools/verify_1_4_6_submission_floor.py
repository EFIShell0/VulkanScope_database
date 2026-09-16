from __future__ import annotations
from pathlib import Path
import argparse, json, sys

ap=argparse.ArgumentParser()
ap.add_argument('--root',default=None)
a=ap.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')

index=text('index.html')
app=text('assets/app.v1406.js')
css=text('assets/site.v1406.css')
worker=text('worker/src/index.js')
contract=text('worker/tests/contract.mjs')
rules=text('rules/PROJECT_RULES.md')
static_index=text('data/index.json')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')
try: static=json.loads(static_index)
except Exception as e: static={}; errors.append(f'invalid data/index.json: {e}')

# Release/cache identity.
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.6','releaseReady':False,'appAsset':'assets/app.v1406.js','cacheKey':'1406'},'1.4.6 release marker mismatch')
for token in ['./assets/site.v1406.css?v=1406','./assets/release-bootstrap.v1406.js?v=1406','./assets/browser-compat.v1406.js?v=1406','./assets/app.v1406.js?v=1406','./config.js?v=1406','VulkanScope Database <strong>1.4.6</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.6'" in app,'frontend Database version mismatch')
for token in ["databaseReleaseVersion:'1.4.6'","workerReleaseVersion:'1.4.6'"]:
    need(worker.count(token)>=3,f'Worker 1.4.6 release metadata missing: {token}')

# Requested new-submission floor. The version comparison is semantic, not versionCode-only.
need("const producerAtLeast1403=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,1,4,3)}" in worker,'1.4.3 producer-floor predicate missing')
need('const supportedProducer=p=>producerAtLeast1403(p)' in worker,'supportedProducer is not owned by the 1.4.3 floor')
need('producerAtLeast1400' not in worker,'obsolete 1.4.0 floor helper remains in current Worker')
need('VulkanScope 1.4.3 or newer is required for new submissions' in worker,'1.4.3 POST rejection message missing')
need('VulkanScope 1.4.0 or newer is required for new submissions' not in worker,'obsolete 1.4.0 POST rejection remains')
need("if(v.major===1)return p.application.versionCode===1000+v.minor*100+v.patch" in worker,'1.x semantic version/versionCode identity mapping missing')

# Floor must belong to POST admission; historical GET remains reachable independently.
get=worker.find("url.pathname.startsWith('/v1/reports/')&&request.method==='GET'")
post=worker.find("url.pathname==='/v1/reports'&&request.method==='POST'")
floor=worker.find('!supportedProducer(p)',post)
valid=worker.find('!validSubmission(p)',post)
need(get>=0 and post>get and floor>post and valid>floor,'producer floor must be POST-only and run before generic validation while historical GET stays independent')

# Worker/static producer metadata must describe the same baseline/floor.
for token in ['VulkanScope 1.4.3 · Vulkan 1.4.362','VulkanScope 1.4.3+ · schema 2 / technical report 3']:
    need(worker.count(token)>=2,f'Worker producer metadata missing: {token}')
need(static.get('databaseVersion')=='1.4.6','static index Database version mismatch')
need(static.get('producerQueryBaseline')=='VulkanScope 1.4.3 · Vulkan 1.4.362','static index producer baseline mismatch')
need(static.get('compatibleProducer')=='VulkanScope 1.4.3+ · schema 2 / technical report 3','static index compatible producer mismatch')

# Runtime contract must prove floor acceptance/rejection and historical readability.
for token in [
    "current.application.version='1.4.3'",
    'current.application.versionCode=1403',
    "below.application.version='1.4.2'",
    'below.application.versionCode=1402',
    "oldMajor.application.version='1.4.0'",
    'oldMajor.application.versionCode=1400',
    "historicalPayload.application.version='0.80.9'",
    "assert.equal(historical.application.version,'0.80.9')",
]:
    need(token in contract,f'Worker floor/historical contract missing: {token}')
need(contract.count('/1\\.4\\.3 or newer/')>=2,'Worker contract does not assert the 1.4.3 floor message for lower producers')
need('VulkanScope 1.4.2 must be rejected by the 1.4.3 floor' in contract,'1.4.2 boundary rejection assertion missing')
need('every producer below 1.4.3 must be rejected before generic validation' in contract,'lower-producer fail-closed assertion missing')

# Preserve the 1.4.5 interaction-only behavior while changing admission only.
need('return`<span class="network-address-toggle ${revealed?' in app,'1.4.5 non-interactive address shell regressed')
need('<button class="network-address-toggle' not in app,'entire address shell became clickable again')
need('<button class="network-address-action" type="button" data-network-address-toggle="${esc(key)}"' in app,'dedicated Show/Hide action regressed')
need("clearSearch.className='search-clear-button custom-select-search-clear is-hidden'" in app,'searchable-filter X clear control regressed')
need("if(!search.value)return;search.value='';syncSearchClear();optionPage=1;renderOptions({resetScroll:true});search.focus({preventScroll:true})" in app,'searchable-filter clear/reset/focus behavior regressed')
need('.network-address-toggle{cursor:default}' in css and '.custom-select-search-clear.is-hidden{width:0;flex-basis:0' in css,'1.4.5 address/filter presentation contract regressed')
need('.page-progress{position:fixed;inset:0 0 auto 0;height:3px;z-index:230;' in css,'viewport-fixed page progress regressed')

# Rules and immediate predecessor bridge.
need('## Release 1.4.6 VulkanScope 1.4.3 new-submission floor requirements' in rules,'1.4.6 project-rules section missing')
repair=text('tools/repair_repository.py')
need("PREDECESSOR_BRIDGE = {'app.v1405.js','browser-compat.v1405.js','release-bootstrap.v1405.js'}" in repair,'1.4.6 predecessor bridge mismatch')
pages=text('tools/build_pages_artifact.py')
need("'assets/app.v1405.js'" in pages and "'assets/app.v1406.js'" in pages and "'assets/app.v1404.js'" not in pages,'Pages current/predecessor app bridge mismatch')
need("'assets/site.v1405.css'" in pages and "'assets/site.v1406.css'" in pages,'Pages current stylesheet identity missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.6 VulkanScope 1.4.3 new-submission floor + historical-read contract')
