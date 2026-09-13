from __future__ import annotations
from pathlib import Path
import argparse,json

p=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.23 connectivity / Settings privacy / report motion contract')
p.add_argument('--root',default=None); p.add_argument('--skip-version',action='store_true'); a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def read(rel): return (root/rel).read_text(encoding='utf-8')
app=read('assets/app.v1023.js'); worker=read('worker/src/index.js'); tests=read('worker/tests/contract.mjs'); rules=read('rules/PROJECT_RULES.md'); workflow=read('tools/pages.workflow.yml'); deployed=read('.github/workflows/pages.yml'); pkg=json.loads(read('worker/package.json')); marker=json.loads(read('data/release.json')); data=json.loads(read('data/index.json')); index=read('index.html'); css=read('assets/site.v0390.css')
if not a.skip_version:
    need(pkg.get('version')=='1.0.23','Worker package identity must be 1.0.23')
    need(data.get('databaseVersion')=='1.0.23','static databaseVersion must be 1.0.23')
    need('VulkanScope Database <strong>1.0.23</strong>' in index,'footer Database identity missing')
    need('assets/app.v1023.js?v=1023' in index and 'site.v0390.css?v=1023' in index and 'config.js?v=1023' in index,'1.0.23 cache identity missing')
    need("const DATABASE_VERSION='1.0.23'" in app,'runtime Database identity mismatch')
need(marker=={'schemaVersion':2,'databaseVersion':'1.0.23','releaseReady':False,'appAsset':'assets/app.v1023.js','cacheKey':'1023'},'source release marker mismatch')
need(workflow==deployed,'deployed workflow must byte-match canonical workflow')

# 1.0.21/1.0.22 data freshness and atomic state guarantees remain intact.
for token,msg in [
    ('LIVE_SYNC_INTERVAL_MS=3000','3-second live sync interval changed'),
    ("url.pathname==='/v1/sync'&&request.method==='GET'",'GET /v1/sync missing'),
    ('COUNT(*) OVER() AS report_count','sync-head query missing'),
    ("new URL(`${api}/v1/sync`)",'frontend sync-head request missing'),
    ("fetchJsonBounded(u,{cache:'no-store'})",'no-store sync request missing'),
    ('const snapshotReports=new Map()','preload private staging Map missing'),
    ("if(nextReports.size!==liveIds.size)throw new Error('Current report set could not be completed atomically')",'atomic exact-cardinality gate missing'),
    ('state.reports=nextReports;state.index=indexState(live.meta,validIndex)','atomic current-set commit missing'),
    ('suppressReportNavigationUntil=performance.now()+400','text-selection navigation guard missing'),
]: need(token in (worker if token.startswith("url.pathname") or token.startswith('COUNT') else app),msg)

# Live connectivity banner: immediate native events plus API reachability state.
need('id="networkStatusShell"' in index and 'id="networkStatusTitle"' in index and 'id="networkStatusMessage"' in index,'top connectivity status surface missing')
for token,msg in [
    ("window.addEventListener('offline'",'offline event monitor missing'),
    ("window.addEventListener('online'",'online event monitor missing'),
    ("setNetworkBannerState('offline')",'persistent offline state missing'),
    ("setNetworkBannerState('checking')",'online recovery checking state missing'),
    ("setNetworkBannerState('restored',{temporary:true})",'successful recovery state missing'),
    ("},3000);renderNetworkInfo()",'restored banner must auto-collapse after three seconds'),
    ('markNetworkFailure(liveSyncFailures>=2)','live-sync reachability failure bridge missing'),
    ('markNetworkReachable();return true','successful live-sync reachability bridge missing'),
    ('void loadNetworkInfo(true);void runLiveSync(true);void runPublishedReleaseCheck()','online recovery must immediately refresh network/live/release state'),
]: need(token in app,msg)
need('Network connection lost. Live reports, synchronization, and Database update checks are unavailable until the connection returns.' in app,'offline Database-unavailable explanation missing')
need('.network-status-shell{position:sticky' in css and 'max-height:0' in css and '.network-status-shell.is-visible{max-height:' in css,'layout-participating animated network banner CSS missing')
need('body.network-banner-visible{--network-banner-offset:58px}' in css and '.topbar{top:var(--network-banner-offset)' in css,'top bar must smoothly account for status banner height')

# Exactly three Settings categories.
need(index.count('data-settings-category=')==3,'Settings must expose exactly three category controls')
for name in ('internet','favorites','preferences'):
    need(f'data-settings-category="{name}"' in index and f'data-settings-panel="{name}"' in index,f'Settings category/panel missing: {name}')
need('role="tablist" aria-label="Settings categories"' in index,'Settings categories must be exposed as an accessible tablist')
need('setSettingsCategory' in app and "e.key==='ArrowRight'||e.key==='ArrowDown'" in app,'Settings category keyboard navigation missing')

# Browser-local persistence is opt-in and clearable.
for token,msg in [
    ("REMEMBER_LOCAL_STATE_KEY='vulkanscopeDatabaseRememberLocalState.v1'",'Remember opt-in storage key missing'),
    ('let rememberLocalState=persistentLocalStateEnabled()','Remember state loader missing'),
    ('let favoriteReportIds=new Set(rememberLocalState?normalizeFavoriteIds','favorites must not hydrate persistently unless Remember is enabled'),
    ('const saveUiPrefs=()=>!rememberLocalState||writeJsonStorage','UI preference writes must be gated by Remember'),
    ('const saveFavorites=()=>!rememberLocalState||writeJsonStorage','Favorite writes must be gated by Remember'),
    ('const setRememberLocalState=enabled=>','Remember state transition missing'),
    ('removeStorage(FAVORITES_STORAGE_KEY);removeStorage(UI_PREFS_STORAGE_KEY)','persistent Favorite/UI preference removal missing'),
    ('const clearSavedLocalState=()=>','clear-saved-data reset missing'),
    ('id="settingsRememberLocalState"','Remember control missing'),
    ('id="settingsClearSavedData"','Clear saved browser data control missing'),
    ('They are not sent to VulkanScope and are never stored in the Database.','browser-local privacy disclosure missing'),
]: need(token in app or token in index,msg)
need('localStorage' not in worker,'Worker must not persist browser favorites/preferences')

# Internet category presentation remains observational and non-persistent.
need("fetchJsonBounded(`${api}/v1/network-info?_=${Date.now()}`,{cache:'no-store'})" in app,'network-info no-store fetch missing')
need("dns:{resolver:null,status:'not_observable'" in worker,'DNS resolver must remain explicitly non-observable')
net_start=worker.find('const currentNetworkInfo='); net_end=worker.find('export default',net_start); net=worker[net_start:net_end]
need(net_start>=0 and 'env.DB' not in net,'network-info helper must not touch D1')
need("['IPv4',n.ipv4?.address||'Not observed on this request','network-ipv4']" in app,'IPv4 presentation class missing')
need("['IPv6',n.ipv6?.address||'Not observed on this request','network-ipv6']" in app,'IPv6 presentation class missing')
need('.network-ipv4{color:#ff9f55!important}' in css,'IPv4 must be orange')
need('.network-ipv6{color:var(--green)!important}' in css,'IPv6 must be green')

# Report-detail actions and interactions are grouped and smoothly animated.
need('class="detail-actions" role="group" aria-label="Report actions"' in app,'grouped report-detail action surface missing')
for token in ['detail-favorite detail-action-button','id="shareReportLink" class="detail-action-button"','id="copyReportLink" class="detail-action-button"']:
    need(token in app,f'detail action styling missing: {token}')
need('Share permalink' not in app and 'Copy permalink' not in app,'legacy separated permalink labels remain')
need('.detail-actions{display:inline-flex' in css and '.detail-action-button' in css,'grouped report-action CSS missing')
need('.click-row td{transition:background-color .22s' in css and '.click-row:hover td{background:#211416}' in css,'smooth report-row hover transition missing')
for token,msg in [
    ('let reportViewTransitionToken=0','report route animation token missing'),
    ('function animateReportViewIn','report detail enter animation missing'),
    ("transform:'translate3d(0,8px,0) scale(.996)'",'report detail compositor transition missing'),
    ('function closeReportDetail()','animated report detail exit missing'),
]: need(token in app,msg)
need('@media(prefers-reduced-motion:reduce)' in css and '.click-row td' in css.split('@media(prefers-reduced-motion:reduce)')[-1],'reduced-motion override for new report/network transitions missing')

# Release/rules boundaries.
need('## Release 1.0.23 live connectivity / Settings privacy / report interaction requirements' in rules,'PROJECT_RULES 1.0.23 section missing')
need((root/'rules/1.0.23_CONNECTIVITY_SETTINGS_PRIVACY_MOTION_AUDIT.md').is_file(),'1.0.23 audit document missing')
need(worker.count("databaseReleaseVersion:'1.0.23'")>=3,'Worker database release identity mismatch')
need(worker.count("workerReleaseVersion:'1.0.23'")>=3,'Worker release identity mismatch')
need(len(list((root/'worker/migrations').glob('*.sql')))==3,'unexpected D1 migration introduced')
for token in ["assert.equal(j.databaseReleaseVersion,'1.0.23')","await call('/v1/network-info',{method:'POST'})"]:
    need(token in tests,f'Worker current contract test missing: {token}')

if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.0.23 connectivity / Settings privacy / report motion contract')
