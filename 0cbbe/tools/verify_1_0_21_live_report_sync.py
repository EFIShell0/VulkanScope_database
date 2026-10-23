from __future__ import annotations
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.21 foreground live-report synchronization contract')
p.add_argument('--root',default=None); p.add_argument('--skip-version',action='store_true'); a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def read(rel): return (root/rel).read_text(encoding='utf-8')
app=read('assets/app.v1021.js'); worker=read('worker/src/index.js'); tests=read('worker/tests/contract.mjs'); rules=read('rules/PROJECT_RULES.md'); workflow=read('tools/pages.workflow.yml'); deployed=read('.github/workflows/pages.yml'); pkg=json.loads(read('worker/package.json')); marker=json.loads(read('data/release.json')); data=json.loads(read('data/index.json')); index=read('index.html')
if not a.skip_version:
    need(pkg.get('version')=='1.0.21','Worker package identity must be 1.0.21')
    need(data.get('databaseVersion')=='1.0.21','static databaseVersion must be 1.0.21')
    need('VulkanScope Database <strong>1.0.21</strong>' in index,'footer Database identity missing')
    need('assets/app.v1021.js?v=1021' in index and 'site.v0390.css?v=1021' in index and 'config.js?v=1021' in index,'1.0.21 cache identity missing')
    need("const DATABASE_VERSION='1.0.21'" in app,'runtime Database identity mismatch')
need('LIVE_SYNC_INTERVAL_MS=3000' in app,'foreground live-sync interval must remain 3000 ms')
need('RELEASE_CHECK_INTERVAL_MS=10000' in app,'release-check interval must remain 10000 ms')
need('Database 1.0.21 · schema' in app,'runtime footer Database identity mismatch')
need(marker=={'schemaVersion':2,'databaseVersion':'1.0.21','releaseReady':False,'appAsset':'assets/app.v1021.js','cacheKey':'1021'},'source release marker mismatch')
# Lightweight head endpoint + one-query freshness semantics.
for token,msg in [
    ("url.pathname==='/v1/sync'&&request.method==='GET'",'GET /v1/sync missing'),
    ('COUNT(*) OVER() AS report_count','sync head must use one count/latest D1 query'),
    ("ORDER BY submitted_at DESC, id DESC LIMIT 1",'sync head latest ordering missing'),
    ('syncToken=`${reportCount}:${latestSubmittedAt}:${latestReportId}`','deterministic sync token missing'),
    ("const known=['/v1/health','/v1/sync','/v1/reports']",'sync endpoint method-boundary registration missing'),
]: need(token in worker,msg)
need(worker.count("databaseReleaseVersion:'1.0.21'")>=3,'Worker release identity not exposed on health/sync/reports')
need(worker.count("workerReleaseVersion:'1.0.21'")>=3,'Worker release identity mismatch')
# Foreground poll is cache-resistant, lightweight, and atomic on change.
for token,msg in [
    ("new URL(`${api}/v1/sync`)",'frontend sync-head request missing'),
    ("u.searchParams.set('_live',String(Date.now()))",'live requests lack nonce cache busting'),
    ("const head=await fetchJsonBounded(u,{cache:'no-store'})",'sync head no-store fetch missing'),
    ("const reportSyncTokenFromIndex=entries=>",'committed index sync-token helper missing'),
    ("if(!force&&head.syncToken===liveSyncToken)",'unchanged sync head does not avoid full reload'),
    ("window.setInterval(()=>void runLiveSync(false),LIVE_SYNC_INTERVAL_MS)",'3-second foreground live timer missing'),
    ("void runLiveSync(false);void runPublishedReleaseCheck()",'initial foreground sync kick missing'),
    ("visibilitychange',()=>{if(!document.hidden){void runLiveSync(true)",'visibility recovery must force reconcile'),
    ("addEventListener('focus',()=>{void runLiveSync(true)",'focus recovery must force reconcile'),
    ("addEventListener('online',()=>{void runLiveSync(true)",'online recovery must force reconcile'),
    ("addEventListener('pageshow',()=>{void runLiveSync(true)",'pageshow recovery must force reconcile'),
    ("u.searchParams.set('_live',String(Date.now()));if(cursor)",'full live index requests lack nonce'),
    ("if(nextReports.size!==liveIds.size)throw new Error('Live report set could not be completed atomically')",'atomic report-set gate missing'),
    ("state.reports=nextReports;state.index=indexState(meta,validIndex);const syncToken=reportSyncTokenFromIndex(validIndex)",'committed Map/index/token order missing'),
    ("if(changed){initFilters();if(renderAfter&&state.routeReady){render();queuePageScrollUi(false)}}",'live change does not rerender metrics/active view'),
    ("catch{return{ok:false,changed:false,added:0,syncToken:liveSyncToken}}",'failed refresh may advance committed sync state'),
]: need(token in app,msg)
need(app.count('?compact=1&_live=${Date.now()}')>=2,'live/requested payload fetches must both use cache-busting nonce')
# Worker contract proves token changes immediately after an accepted row.
for token,msg in [
    ("r=await call('/v1/sync');",'Worker sync endpoint is not contract-tested'),
    ("assert.equal(j.reportCount,0);",'empty sync-head contract missing'),
    ("assert.notEqual(j.syncToken,emptySyncToken);",'accepted-report sync-token change not tested'),
    ("assert.equal(j.syncToken,`1:${j.latestSubmittedAt}:${accepted.id}`);",'accepted-report exact sync token not tested'),
]: need(token in tests,msg)
# Release handshake/security boundaries remain independent.
need('maybeShowDatabaseUpdate(meta)' not in app,'Worker metadata regressed into frontend refresh signaling')
need("fetchJsonBounded(`./data/release.json?_=${Date.now()}`,{cache:'no-store'})" in app,'Pages release marker handshake regressed')
need('UPDATE_RETRY_SUPPRESS_MS=120000' in app,'refresh-loop suppression regressed')
need(workflow==deployed,'deployed workflow must byte-match canonical workflow')
need('## Release 1.0.21 foreground live-report reconciliation / sync-head requirements' in rules,'PROJECT_RULES 1.0.21 section missing')
need((root/'rules/1.0.21_LIVE_REPORT_SYNC_AUDIT.md').is_file(),'1.0.21 audit document missing')
if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.0.21 foreground live-report synchronization contract')
