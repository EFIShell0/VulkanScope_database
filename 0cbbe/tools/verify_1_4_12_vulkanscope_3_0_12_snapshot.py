from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
def text(rel): return (root/rel).read_text(encoding='utf-8')
def need(cond,msg):
    if not cond: raise SystemExit('FAIL '+msg)
app=text('assets/app.v1412.js'); worker=text('worker/src/index.js'); preload=text('tools/build_preload_snapshot.py'); index=text('index.html'); workflow=text('tools/pages.workflow.yml')
marker=json.loads(text('data/release.json')); static=json.loads(text('data/index.json')); schema=json.loads(text('report.schema.json')); lock=json.loads(text('registry/registry_lock.json')); curated=json.loads(text('registry/encyclopedia_curated.json')); rules=text('rules/PROJECT_RULES.md'); repair=text('tools/repair_repository.py'); pages=text('tools/build_pages_artifact.py'); ency=text('assets/encyclopedia.v1412.js'); wr=json.loads(text('worker/wrangler.jsonc'))
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.12','releaseReady':False,'appAsset':'assets/app.v1412.js','cacheKey':'1412'},'release marker mismatch')
for token in ['./assets/site.v1412.css?v=1412','./assets/release-bootstrap.v1412.js?v=1412','./assets/browser-compat.v1412.js?v=1412','./assets/app.v1412.js?v=1412','./config.js?v=1412','./assets/encyclopedia.v1412.js','VulkanScope Database <strong>1.4.12</strong>']:
    need(token in index,f'index current identity missing: {token}')
need("const DATABASE_VERSION='1.4.12'" in app,'frontend Database identity mismatch')
need("CURRENT_PRODUCER_QUERY_BASELINE='VulkanScope 3.0.12 · Vulkan 1.4.364'" in app,'frontend producer baseline mismatch')
need("CURRENT_COMPATIBLE_PRODUCER='VulkanScope 3.0.12+ · schema 2 / technical report 3'" in app,'frontend compatible producer mismatch')
need("'databaseVersion': '1.4.12'" in preload and "'producerQueryBaseline': 'VulkanScope 3.0.12 · Vulkan 1.4.364'" in preload,'preload metadata mismatch')
need("--expect-report-id" in preload and 'fresh report' in preload and "'triggerReportId': expected or None" in preload,'fresh-report snapshot gate missing')
need('const producerAtLeast3012' in worker and 'versionAtLeast(v,3,0,12)' in worker and 'const supportedProducer=p=>producerAtLeast3012(p)' in worker,'Worker 3.0.12 floor predicate missing')
need('VulkanScope 3.0.12 or newer is required for new submissions' in worker,'Worker 3.0.12 rejection missing')
need('if(v.major===3)return p.application.versionCode===3000+v.minor*100+v.patch' in worker,'3.x fail-closed identity mapping missing')
for token in ['snapshotDispatchConfigured','SNAPSHOT_GITHUB_TOKEN','actions/workflows/${encodeURIComponent(workflow)}/dispatches','snapshot_refresh_dispatch_failed','inserted=Number(results?.[0]?.meta?.changes||0)>0']:
    need(token in worker,f'snapshot dispatch contract missing: {token}')
need('if(inserted&&ctx?.waitUntil)ctx.waitUntil(dispatchSnapshotRefresh(env,id,submittedAt).catch(' in worker,'snapshot dispatch must be scheduled only for a newly inserted report through ctx.waitUntil')
need("snapshotAutomation:{configured:snapshotDispatchConfigured(env),mode:'async-github-actions-workflow-dispatch'}" in worker,'health snapshot automation state missing')
for token in ["databaseReleaseVersion:'1.4.12'","workerReleaseVersion:'1.4.12'",'VulkanScope 3.0.12 · Vulkan 1.4.364','VulkanScope 3.0.12+ · schema 2 / technical report 3','Vulkan 1.4.364 (2026-09-25)']:
    need(token in worker,f'Worker current metadata missing: {token}')
need(static.get('databaseVersion')=='1.4.12','static Database identity mismatch')
need(static.get('producerQueryBaseline')=='VulkanScope 3.0.12 · Vulkan 1.4.364','static producer baseline mismatch')
need(static.get('compatibleProducer')=='VulkanScope 3.0.12+ · schema 2 / technical report 3','static compatible producer mismatch')
need(lock.get('apiVersion')=='1.4.364' and lock.get('headerVersion')==364,'registry/header lock drifted')
reg=root/lock['bundledRegistryPath']; need(reg.is_file() and hashlib.sha256(reg.read_bytes()).hexdigest()==lock.get('registrySha256'),'bundled registry hash mismatch')
need(curated.get('appVersion')=='3.0.12' and curated.get('registryBaseline')=='Vulkan 1.4.364','Encyclopedia producer metadata mismatch')
need('"appVersion":"3.0.12"' in ency and '"registryBaseline":"Vulkan 1.4.364"' in ency,'generated Encyclopedia metadata mismatch')
app_schema=schema['properties']['application']['properties']
need(app_schema['versionCode'].get('minimum')==3012,'report schema versionCode floor mismatch')
need('3.0.12 or newer' in app_schema['version'].get('description',''),'report schema floor description mismatch')
need('## Release 1.4.12 VulkanScope 3.0.12 floor and asynchronous snapshot-refresh requirements' in rules,'1.4.12 rules section missing')
need((root/'rules/1.4.12_VULKANSCOPE_3_0_12_SNAPSHOT_AUDIT.md').is_file(),'1.4.12 audit file missing')
vars=wr.get('vars',{})
for k,v in {'SNAPSHOT_GITHUB_OWNER':'EFIShell0','SNAPSHOT_GITHUB_REPO':'VulkanScope_database','SNAPSHOT_GITHUB_WORKFLOW':'pages.yml','SNAPSHOT_GITHUB_REF':'main'}.items(): need(vars.get(k)==v,f'Worker snapshot var mismatch: {k}')
need('SNAPSHOT_GITHUB_TOKEN' not in vars,'snapshot token must not be committed as a Worker var')
for token in ['mode:','snapshot-refresh:','inputs.mode == \'snapshot\'','--expect-report-id "$REPORT_ID"','tools/verify_published_snapshot.py','actions/deploy-pages@v4','vulkanscope-database-${{ inputs.mode || \'release\' }}','queue: max']:
    need(token in workflow,f'snapshot workflow contract missing: {token}')
need(workflow.count('group: vulkanscope-database-pages-deployment')==2,'release and snapshot Pages deployments must share one serialized deployment concurrency group')
need("CURRENT_APP = 'app.v1412.js'" in repair and "PREDECESSOR_BRIDGE = {'app.v1411.js','browser-compat.v1411.js','release-bootstrap.v1411.js'}" in repair,'repository current/bridge mismatch')
need("'assets/app.v1411.js'" in pages and "'assets/app.v1412.js'" in pages and "'assets/app.v1410.js'" not in pages,'Pages current/predecessor bridge mismatch')
need((root/'tools/verify_published_snapshot.py').is_file(),'published snapshot verifier missing')
print('PASS Database 1.4.12 VulkanScope 3.0.12 floor + asynchronous snapshot-refresh contract')
