from __future__ import annotations
from pathlib import Path
import argparse, json

p=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.22 atomic current-set / settings / favorites / selection-safety contract')
p.add_argument('--root',default=None); p.add_argument('--skip-version',action='store_true'); a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def read(rel): return (root/rel).read_text(encoding='utf-8')
app=read('assets/app.v1022.js'); worker=read('worker/src/index.js'); tests=read('worker/tests/contract.mjs'); rules=read('rules/PROJECT_RULES.md'); workflow=read('tools/pages.workflow.yml'); deployed=read('.github/workflows/pages.yml'); pkg=json.loads(read('worker/package.json')); marker=json.loads(read('data/release.json')); data=json.loads(read('data/index.json')); index=read('index.html'); css=read('assets/site.v0390.css')
if not a.skip_version:
    need(pkg.get('version')=='1.0.22','Worker package identity must be 1.0.22')
    need(data.get('databaseVersion')=='1.0.22','static databaseVersion must be 1.0.22')
    need('VulkanScope Database <strong>1.0.22</strong>' in index,'footer Database identity missing')
    need('assets/app.v1022.js?v=1022' in index and 'site.v0390.css?v=1022' in index and 'config.js?v=1022' in index,'1.0.22 cache identity missing')
    need("const DATABASE_VERSION='1.0.22'" in app,'runtime Database identity mismatch')
need(marker=={'schemaVersion':2,'databaseVersion':'1.0.22','releaseReady':False,'appAsset':'assets/app.v1022.js','cacheKey':'1022'},'source release marker mismatch')
need(workflow==deployed,'deployed workflow must byte-match canonical workflow')

# 1.0.21 freshness guarantees retained.
for token,msg in [
    ("url.pathname==='/v1/sync'&&request.method==='GET'",'GET /v1/sync missing'),
    ('COUNT(*) OVER() AS report_count','sync head count/latest query missing'),
    ("new URL(`${api}/v1/sync`)",'frontend sync-head request missing'),
    ("fetchJsonBounded(u,{cache:'no-store'})",'no-store live request missing'),
    ("if(!force&&head.syncToken===liveSyncToken)",'sync-token shortcut missing'),
    ('LIVE_SYNC_INTERVAL_MS=3000','3-second live sync interval changed'),
]: need(token in (worker if token.startswith('url.pathname') or token.startswith('COUNT') else app),msg)

# Initial state must be staged and committed as one complete current set.
pre_start=app.find('async function loadPreloadedSnapshot()'); pre_end=app.find('const requestedRouteReportIds=',pre_start)
pre=app[pre_start:pre_end]
need(pre_start>=0 and pre_end>pre_start,'preload snapshot loader missing')
need('const snapshotReports=new Map()' in pre,'preload must hydrate a private staging Map')
need('snapshotReports.set(id,hydrateReport' in pre,'snapshot staging hydration missing')
need('state.reports.set(' not in pre and 'state.reports=' not in pre,'preload must not mutate visible state.reports')
need('state.index=' not in pre,'preload must not mutate visible state.index')
asm_start=app.find('async function assembleCurrentDatabase('); asm_end=app.find('async function load(){',asm_start); asm=app[asm_start:asm_end]
need(asm_start>=0 and asm_end>asm_start,'assembleCurrentDatabase missing')
for token,msg in [
    ('const nextReports=new Map()','current-set staging Map missing'),
    ('const missing=validIndex.filter(x=>!nextReports.has(x.id))','live-index missing set calculation missing'),
    ("targetTotal:validIndex.length,baseReady:nextReports.size",'single current-set progress accounting missing'),
    ("if(nextReports.size!==liveIds.size)throw new Error('Current report set could not be completed atomically')",'atomic exact-cardinality gate missing'),
    ('state.reports=nextReports;state.index=indexState(live.meta,validIndex)','atomic current-set commit missing'),
]: need(token in asm,msg)
need('snapshot reports ·' not in app,'legacy snapshot + delta loading wording remains')
need('new payload' not in app and 'payload to load' not in app,'public loading UI still exposes additive payload wording')
need("'Building current database…'" in app and 'reports ready' in app,'single current-set loading wording missing')

# Favorites and persistent Settings controls are local-only.
for token,msg in [
    ("FAVORITES_STORAGE_KEY='vulkanscopeDatabaseFavorites.v1'",'favorites localStorage key missing'),
    ("UI_PREFS_STORAGE_KEY='vulkanscopeDatabaseUiPrefs.v1'",'settings localStorage key missing'),
    ('normalizeFavoriteIds','favorites ID validation/bounding missing'),
    ('favoriteButtonMarkup','report favorite controls missing'),
    ('data-favorite-report','favorite report binding missing'),
    ('renderSettingsFavorites','Settings favorite list missing'),
    ('settingsSubmittedDefault','Submitted default-expansion setting missing'),
    ('settingsVendorDefault','Vendor default-expansion setting missing'),
    ('settingsTypeDefault','Type default-expansion setting missing'),
]: need(token in app or token in index,msg)
need('id="settingsButton"' in index and index.find('id="settingsButton"') < index.find('class="brand"'),'Settings button must be immediately before/left of brand')
need('id="settingsDrawer"' in index and 'id="settingsFavorites"' in index and 'id="networkInfo"' in index,'Settings drawer sections missing')
need('.settings-drawer' in css and 'translateX(-102%)' in css and 'body.settings-open .settings-drawer' in css,'left sliding Settings drawer CSS missing')
need('localStorage' not in worker,'Worker must not persist browser favorites/preferences')

# Request-scoped network information; no DNS invention / no D1.
net_start=worker.find('const currentNetworkInfo='); net_end=worker.find('export default',net_start); net=worker[net_start:net_end]
route_start=worker.find("if(url.pathname==='/v1/network-info'&&request.method==='GET')")
need(net_start>=0 and route_start>=0,'GET /v1/network-info missing')
for token,msg in [
    ("request.headers.get('cf-connecting-ip')",'CF-Connecting-IP observation missing'),
    ("request.headers.get('cf-connecting-ipv6')",'CF-Connecting-IPv6 observation missing'),
    ("request.headers.get('cf-pseudo-ipv4')",'Pseudo IPv4 distinction missing'),
    ("dns:{resolver:null,status:'not_observable'",'DNS must be explicitly non-observable'),
    ('const cf=request.cf||{}','allow-listed Cloudflare request metadata source missing'),
]: need(token in net,msg)
need('env.DB' not in net,'network-info helper must not touch D1')
need("const known=['/v1/health','/v1/network-info','/v1/sync','/v1/reports']" in worker,'network-info method boundary missing')
need("fetchJsonBounded(`${api}/v1/network-info?_=${Date.now()}`,{cache:'no-store'})" in app,'frontend network-info no-store fetch missing')
need("['DNS resolver','Not observable from this site request']" in app,'frontend DNS non-observable labeling missing')
for token in ["assert.equal(j.accessFamily,'IPv6')","assert.equal(j.dns.status,'not_observable')","await call('/v1/network-info',{method:'POST'})"]: need(token in tests,f'Worker network-info contract test missing: {token}')

# Text drag selection must suppress only report navigation click.
for token,msg in [
    ("document.addEventListener('pointerdown'",'selection pointerdown guard missing'),
    ("document.addEventListener('pointerup'",'selection pointerup guard missing'),
    ('window.getSelection?.()','selection-state check missing'),
    ('suppressReportNavigationUntil=performance.now()+400','post-selection navigation suppression window missing'),
    ("document.addEventListener('click',e=>{if(performance.now()<suppressReportNavigationUntil",'capture click suppression missing'),
    ('shouldSuppressReportNavigation','report click handlers lack selection guard'),
]: need(token in app,msg)

# Immutable/release rules.
need('## Release 1.0.22 atomic current-set / local preferences / network-observation / selection-safety requirements' in rules,'PROJECT_RULES 1.0.22 section missing')
need((root/'rules/1.0.22_ATOMIC_CURRENT_SET_SETTINGS_FAVORITES_SELECTION_AUDIT.md').is_file(),'1.0.22 audit document missing')
need(worker.count("databaseReleaseVersion:'1.0.22'")>=3,'Worker database release identity mismatch')
need(worker.count("workerReleaseVersion:'1.0.22'")>=3,'Worker release identity mismatch')
if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.0.22 atomic current-set / settings / favorites / network / selection-safety contract')
