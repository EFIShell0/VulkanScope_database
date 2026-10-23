from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
def text(rel): return (root/rel).read_text(encoding='utf-8')
def need(cond,msg):
    if not cond: raise SystemExit('FAIL '+msg)
app=text('assets/app.v1411.js'); worker=text('worker/src/index.js'); preload=text('tools/build_preload_snapshot.py'); index=text('index.html')
marker=json.loads(text('data/release.json')); static=json.loads(text('data/index.json')); schema=json.loads(text('report.schema.json')); lock=json.loads(text('registry/registry_lock.json')); curated=json.loads(text('registry/encyclopedia_curated.json')); rules=text('rules/PROJECT_RULES.md'); repair=text('tools/repair_repository.py'); pages=text('tools/build_pages_artifact.py'); ency=text('assets/encyclopedia.v1411.js')
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.11','releaseReady':False,'appAsset':'assets/app.v1411.js','cacheKey':'1411'},'release marker mismatch')
for token in ['./assets/site.v1411.css?v=1411','./assets/release-bootstrap.v1411.js?v=1411','./assets/browser-compat.v1411.js?v=1411','./assets/app.v1411.js?v=1411','./config.js?v=1411','./assets/encyclopedia.v1411.js','VulkanScope Database <strong>1.4.11</strong>']:
    need(token in index,f'index current identity missing: {token}')
need("const DATABASE_VERSION='1.4.11'" in app,'frontend Database identity mismatch')
need("CURRENT_PRODUCER_QUERY_BASELINE='VulkanScope 3.0.2 · Vulkan 1.4.364'" in app,'frontend producer baseline mismatch')
need("CURRENT_COMPATIBLE_PRODUCER='VulkanScope 3.0.2+ · schema 2 / technical report 3'" in app,'frontend compatible producer mismatch')
need("'producerQueryBaseline': 'VulkanScope 3.0.2 · Vulkan 1.4.364'" in preload,'preload producer baseline mismatch')
need("'compatibleProducer': 'VulkanScope 3.0.2+ · schema 2 / technical report 3'" in preload,'preload producer floor metadata mismatch')
need('const producerAtLeast3002' in worker and 'versionAtLeast(v,3,0,2)' in worker and 'const supportedProducer=p=>producerAtLeast3002(p)' in worker,'Worker 3.0.2 floor predicate missing')
need('VulkanScope 3.0.2 or newer is required for new submissions' in worker,'Worker 3.0.2 rejection missing')
need('if(v.major===3)return p.application.versionCode===3000+v.minor*100+v.patch' in worker,'3.x fail-closed identity mapping missing')
need('return false};const validCurrentQueryDiagnostics' in worker,'unknown producer identity no longer fails closed')
for key in ['platform','chromeOsArcRuntime','androidPcFormFactor','freeformWindowManagement','googlebookEnvironmentEvidence','googlebookOsVersion','hostOsVersion']:
    need(key in worker,f'3.0.2 device environment field missing: {key}')
for token in ["databaseReleaseVersion:'1.4.11'","workerReleaseVersion:'1.4.11'",'VulkanScope 3.0.2 · Vulkan 1.4.364','VulkanScope 3.0.2+ · schema 2 / technical report 3','Vulkan 1.4.364 (2026-09-25)']:
    need(token in worker,f'Worker current metadata missing: {token}')
need("producerAtLeast2006(p)?'1.4.364':producerAtLeast08010(p)?'1.4.362':'1.4.361'" in worker,'1.4.364 registry selector drifted')
need(static.get('databaseVersion')=='1.4.11','static Database identity mismatch')
need(static.get('producerQueryBaseline')=='VulkanScope 3.0.2 · Vulkan 1.4.364','static producer baseline mismatch')
need(static.get('compatibleProducer')=='VulkanScope 3.0.2+ · schema 2 / technical report 3','static compatible producer mismatch')
need(lock.get('apiVersion')=='1.4.364' and lock.get('headerVersion')==364,'registry/header lock drifted')
need(lock.get('registeredVulkanExtensionCount')==477,'registry extension census drifted')
reg=root/lock['bundledRegistryPath']; need(reg.is_file() and hashlib.sha256(reg.read_bytes()).hexdigest()==lock.get('registrySha256'),'bundled registry hash mismatch')
need(curated.get('appVersion')=='3.0.2' and curated.get('registryBaseline')=='Vulkan 1.4.364','Encyclopedia producer metadata mismatch')
need('"appVersion":"3.0.2"' in ency and '"registryBaseline":"Vulkan 1.4.364"' in ency,'generated Encyclopedia metadata mismatch')
app_schema=schema['properties']['application']['properties']
need(app_schema['versionCode'].get('minimum')==3002,'report schema versionCode floor mismatch')
need(app_schema['version'].get('pattern')==r'^3\.(?:0\.(?:[2-9]|[1-9][0-9]+)|[1-9][0-9]*\.[0-9]+)$','report schema semantic floor mismatch')
need('3.0.2 or newer' in app_schema['version'].get('description',''),'report schema floor description mismatch')
need(schema.get('properties',{}).get('technicalReport',{}).get('type')=='object','technicalReport schema contract missing')
need('## Release 1.4.11 VulkanScope 3.0.2 compatibility and submission-floor requirements' in rules,'1.4.11 rules section missing')
need((root/'rules/1.4.11_VULKANSCOPE_3_0_2_COMPATIBILITY_AUDIT.md').is_file(),'1.4.11 audit file missing')
need("CURRENT_APP = 'app.v1411.js'" in repair and "PREDECESSOR_BRIDGE = {'app.v1410.js','browser-compat.v1410.js','release-bootstrap.v1410.js'}" in repair,'repository current/bridge mismatch')
need("'assets/app.v1410.js'" in pages and "'assets/app.v1411.js'" in pages and "'assets/app.v1409.js'" not in pages,'Pages current/predecessor bridge mismatch')
print('PASS Database 1.4.11 VulkanScope 3.0.2 compatibility/submission-floor contract')
