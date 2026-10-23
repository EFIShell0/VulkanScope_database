from __future__ import annotations
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.20 release-state handshake and refresh-loop recovery')
p.add_argument('--root',default=None); p.add_argument('--skip-version',action='store_true'); a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def read(rel): return (root/rel).read_text(encoding='utf-8')
app=read('assets/app.v1020.js'); index=read('index.html'); worker=read('worker/src/index.js'); tests=read('worker/tests/contract.mjs'); workflow=read('tools/pages.workflow.yml'); deployed=read('.github/workflows/pages.yml'); rules=read('rules/PROJECT_RULES.md'); mark=read('tools/mark_release_ready.py'); audit=read('tools/audit_database.py'); q=read('tools/quality_gate.py'); pkg=json.loads(read('worker/package.json')); marker=json.loads(read('data/release.json')); data=json.loads(read('data/index.json'))
if not a.skip_version:
    need(pkg.get('version')=='1.0.20','Worker package identity must be 1.0.20')
    need(data.get('databaseVersion')=='1.0.20','static index databaseVersion must be 1.0.20')
    need('VulkanScope Database <strong>1.0.20</strong>' in index,'footer Database identity missing')
    need('assets/app.v1020.js?v=1020' in index and 'site.v0390.css?v=1020' in index and 'config.js?v=1020' in index,'1.0.20 cache identity missing')
    need("const DATABASE_VERSION='1.0.20',LIVE_SYNC_INTERVAL_MS=10000,RELEASE_CHECK_INTERVAL_MS=10000;" in app,'runtime Database identity missing')
need(marker=={'schemaVersion':2,'databaseVersion':'1.0.20','releaseReady':False,'appAsset':'assets/app.v1020.js','cacheKey':'1020'},'source release marker must be exact schema-2 non-ready marker')
# Legacy-loop rescue: old 1.0.18 only knows databaseVersion.
need("databaseVersion:" not in worker,'legacy Worker databaseVersion refresh signal remains')
need(worker.count("databaseReleaseVersion:'1.0.20'")>=2,'informational databaseReleaseVersion missing')
need(worker.count("workerReleaseVersion:'1.0.20'")>=2,'informational workerReleaseVersion missing')
need(worker.count("frontendUpdateSignal:'same-origin-pages-marker'")>=2,'frontend update signal metadata missing')
need("assert.equal(j.databaseVersion,undefined);" in tests,'Worker contract does not lock legacy databaseVersion removal')
# Browser publication handshake + loop suppression.
for token,msg in [
    ("fetchJsonBounded(`./data/release.json?_=${Date.now()}`,{cache:'no-store'})",'release marker no-store fetch missing'),
    ('releaseMarkerShapeValid','schema-2 marker validation missing'),
    ("compareVersion(remote,DATABASE_VERSION)>0&&await publishedFrontendReady(marker)",'published frontend readiness probe missing'),
    ("html.includes(`./${asset}?v=${cacheKey}`)",'published index/app binding check missing'),
    ("js.includes(`const DATABASE_VERSION='${remote}'`)",'published app version binding check missing'),
    ('UPDATE_RETRY_SUPPRESS_MS=120000','bounded repeated-prompt suppression missing'),
    ('sessionStorage.setItem(UPDATE_ATTEMPT_KEY','refresh attempt persistence missing'),
    ('suppressRepeatedUpdatePrompt(remote)','repeat-refresh suppression not enforced'),
    ('clearCompletedUpdateAttempt();liveSyncApi=api','completed-attempt cleanup missing'),
    ("u.searchParams.set('_r',String(Date.now()))",'cache-busting navigation missing'),
]: need(token in app,msg)
need('maybeShowDatabaseUpdate(meta)' not in app,'Worker metadata still drives update dialog')
# Publication state machine.
need(workflow==deployed,'deployed workflow must byte-match canonical workflow')
need('branches: ["main"]' in workflow and 'tags:' not in workflow,'workflow must publish from main only')
need('Create or refresh GitHub Release from validated main commit' in workflow,'GitHub Release creation from main missing')
need('gh release create "$TAG"' in workflow and '--target "$GITHUB_SHA"' in workflow,'Release/tag must bind validated main commit')
need('TAG_SHA="$(git rev-list -n 1 "$TAG")"' in workflow and '[ "$TAG_SHA" != "$GITHUB_SHA" ]' in workflow,'existing release tag must fail closed if it targets a different commit')
need('needs: [build, release]' in workflow,'deploy does not wait for Release success')
need(workflow.find('  release:') < workflow.find('  deploy:'),'Release job must precede deploy')
need('python tools/mark_release_ready.py _site' in workflow,'staged ready transition missing')
need(workflow.find('python tools/mark_release_ready.py _site') < workflow.find('actions/upload-pages-artifact@v4'),'marker must transition before Pages artifact upload')
need('actions/configure-pages@v5' in workflow and 'actions/upload-pages-artifact@v4' in workflow and 'actions/deploy-pages@v4' in workflow,'documented Pages action versions missing')
need('actions/upload-pages-artifact@v5' not in workflow and 'actions/deploy-pages@v5' not in workflow,'unsupported/undocumented Pages v5 action reference remains')
need("data['releaseReady']=True" in mark and "expected={'schemaVersion':2,'databaseVersion':'1.0.20','releaseReady':False" in mark,'staged marker transition utility is not fail-closed')
# Preserve prior feature/data/security boundaries.
for token in ["high=ratio>0&&(rank===true||rank==='dominant')?' high':''","return v===max?'dominant':'subordinate'",'--coverage-position:${ratio*100}%','modal-value-list modal-paged-list','coverage-report-list modal-paged-list',"donutChart('GPU / reports',chartItems,rs.length,'',state.deviceSliceLimit)","const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');",'fill="#3DDC84"',"[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']"]: need(token in app,f'preserved frontend contract missing: {token}')
for token in ['Vulkan 1.4.362 (2026-09-04)','VulkanScope producer/query baseline 1.4.362','VulkanScope 1.0.19 · Vulkan 1.4.362','VulkanScope 1.0.19+ · schema 2 / technical report 3']: need(token in worker,f'producer/spec contract missing: {token}')
need('2*1024*1024' in worker and 'readBoundedBody' in worker and "new TextDecoder('utf-8',{fatal:true})" in worker,'Worker bounded/strict UTF-8 security controls regressed')
need(pkg.get('devDependencies',{}).get('wrangler')=='4.130.0','Wrangler pin changed')
need((pkg.get('overrides') or {}).get('sharp')=='0.35.4','sharp override changed')
need("AUDIT_VERSION='1.0.20'" in audit and "APP_ASSET='app.v1020.js'" in audit,'current audit identity missing')
need("verify_1_0_20_release_state_handshake.py" in q and 'mark_release_ready.py' in q,'quality gate does not exercise 1.0.20 release-state transition')
need('## Release 1.0.20 release-state handshake / refresh-loop recovery / Pages publication repair' in rules,'PROJECT_RULES 1.0.20 section missing')
need((root/'rules/1.0.20_RELEASE_STATE_HANDSHAKE_AUDIT.md').is_file(),'1.0.20 audit document missing')
if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.0.20 release-state handshake + refresh-loop recovery contract')
