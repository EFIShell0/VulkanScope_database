from __future__ import annotations
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.24 regional time / Compare / country contract')
p.add_argument('--root',default=None); p.add_argument('--skip-version',action='store_true'); a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def read(rel): return (root/rel).read_text(encoding='utf-8')
app=read('assets/app.v1024.js'); css=read('assets/site.v0390.css'); index=read('index.html'); worker=read('worker/src/index.js'); tests=read('worker/tests/contract.mjs'); rules=read('rules/PROJECT_RULES.md'); workflow=read('tools/pages.workflow.yml'); deployed=read('.github/workflows/pages.yml'); pkg=json.loads(read('worker/package.json')); marker=json.loads(read('data/release.json')); data=json.loads(read('data/index.json'))
if not a.skip_version:
    need(pkg.get('version')=='1.0.24','Worker package identity must be 1.0.24')
    need(data.get('databaseVersion')=='1.0.24','static databaseVersion must be 1.0.24')
    need('VulkanScope Database <strong>1.0.24</strong>' in index,'footer Database identity missing')
    need('assets/app.v1024.js?v=1024' in index and 'site.v0390.css?v=1024' in index and 'config.js?v=1024' in index,'1.0.24 cache identity missing')
    need("const DATABASE_VERSION='1.0.24'" in app,'runtime Database identity mismatch')
need(marker=={'schemaVersion':2,'databaseVersion':'1.0.24','releaseReady':False,'appAsset':'assets/app.v1024.js','cacheKey':'1024'},'source release marker mismatch')
need(workflow==deployed,'deployed workflow must byte-match canonical workflow')

# Immutable live data / Worker boundaries retained.
for token,msg in [
    ('LIVE_SYNC_INTERVAL_MS=3000','3-second live sync interval changed'),
    ("url.pathname==='/v1/sync'&&request.method==='GET'",'GET /v1/sync missing'),
    ('const snapshotReports=new Map()','private snapshot staging Map missing'),
    ("state.reports=nextReports;state.index=indexState(live.meta,validIndex)",'atomic report-set commit missing'),
    ("fetchJsonBounded(`${api}/v1/network-info?_=${Date.now()}`,{cache:'no-store'})",'network-info no-store request missing'),
]: need(token in (worker if token.startswith("url.pathname") else app),msg)
need(len(list((root/'worker/migrations').glob('*.sql')))==3,'unexpected D1 migration introduced')

# Connectivity regression: no redundant unavailable chip and complete restored interval.
need("unavailable:{title:'Database connection unavailable'" in app and "badge:''" in app,'Database unavailable banner must not render the right-side UNAVAILABLE label')
need("if(badge){badge.textContent=copy.badge||'';badge.hidden=!copy.badge}" in app,'empty network badge must be hidden')
need("if(networkUiState==='restored')return" in app,'successful reachability probes must not collapse restored state early')
need("setNetworkBannerState('restored',{temporary:true});return" in app,'recovery must enter temporary restored state')
need('},3000);renderNetworkInfo()' in app,'restored state must remain on the 3000ms timer')
need('.network-status-badge[hidden]{display:none!important}' in css,'hidden unavailable badge CSS missing')

# Exactly three Settings categories remain; regional controls are under Preferences.
need(index.count('data-settings-category=')==3,'Settings must expose exactly three category controls')
for category in ('internet','favorites','preferences'):
    need(f'data-settings-category="{category}"' in index and f'data-settings-panel="{category}"' in index,f'Settings category/panel missing: {category}')
for id_ in ('settingsRegionalCountry','settingsRegionalDateFormat','settingsRegionalClock','settingsRegionalTimeZone','settingsRegionalSeason','settingsRegionalPreview'):
    need(f'id="{id_}"' in index,f'regional preference control missing: {id_}')
for value in ('DD/MM/YYYY','MM/DD/YYYY','YYYY-MM-DD','12-hour (AM/PM)','24-hour','Standard / winter time','Daylight / summer time'):
    need(value in index,f'regional preference option missing: {value}')

# Regional preference validation/storage is bounded and still opt-in.
for token,msg in [
    ("regionalCountry:'auto'",'regional country default missing'),
    ("REGIONAL_DATE_FORMATS=new Set(['auto','dmy','mdy','ymd','long'])",'date-format allow-list missing'),
    ("REGIONAL_CLOCKS=new Set(['auto','12','24'])",'clock allow-list missing'),
    ("REGIONAL_SEASONS=new Set(['auto','standard','daylight'])",'seasonal allow-list missing'),
    ("Intl.supportedValuesOf?.('timeZone')",'browser-supported IANA time-zone enumeration missing'),
    ('const saveUiPrefs=()=>!rememberLocalState||writeJsonStorage','persistent preference writes must remain Remember-gated'),
    ('regionalTimeZone:validRegionalTimeZone','stored time-zone validation missing'),
    ('regionalSeason:REGIONAL_SEASONS.has','stored seasonal-mode validation missing'),
]: need(token in app,msg)
need('data-native-select="1"' in index and "sel.dataset.nativeSelect==='1'" in app,'large country/time-zone controls must remain usable native selects')

# Central temporal formatting must drive all user-facing submission/server timestamps without changing sort semantics.
for token,msg in [
    ('const submittedParts=value=>','central submitted timestamp formatter missing'),
    ('const temporalContext=date=>','time-zone/season presentation context missing'),
    ('const seasonalOffsets=(zone,date)=>','standard/daylight current-year offset derivation missing'),
    ("if(state.regionalDateFormat==='dmy')",'DD/MM/YYYY rendering missing'),
    ("if(state.regionalDateFormat==='mdy')",'MM/DD/YYYY rendering missing'),
    ("if(state.regionalDateFormat==='ymd')",'YYYY-MM-DD rendering missing'),
    ("if(state.regionalClock==='12')opts.hour12=true",'12-hour AM/PM rendering missing'),
    ("else if(state.regionalClock==='24')opts.hourCycle='h23'",'24-hour rendering missing'),
    ("['Server time',formatSubmitted(n.serverTime),'']",'Internet server time must use the same regional formatter'),
    ("k==='submittedAt'?formatSubmitted(v):v",'report overview submittedAt must use selected regional format'),
    ("const submitted=submittedParts(r.submittedAt)", 'report table/Compare submitted formatting bridge missing'),
]: need(token in app,msg)
need("if(field==='submitted')return Date.parse(String(r.submittedAt||''))||0" in app,'submission sorting must still use the source instant rather than display text')

# Country code -> localized full country name + current platform country flag, with no third-party flag service.
for token,msg in [
    ("new Intl.DisplayNames([regionalLocale()],{type:'region'})",'localized country-name expansion missing'),
    ('String.fromCodePoint(...[...cc].map(c=>127397+c.charCodeAt(0)))','regional-indicator country flag generation missing'),
    ("['Country',countryDisplay(n.country),'country-info-value']",'Internet country row must use full country display'),
    ("COUNTRY_CODE_SET.has(cc)",'flag generation must validate country codes'),
]: need(token in app,msg)
need('flagcdn' not in app.lower() and 'countryflags' not in app.lower(),'runtime third-party flag service must not be introduced')

# Compare workspace design/usability while preserving semantic warnings/filtering.
for token,msg in [
    ('class="compare-workspace"','distinct Compare workspace surface missing'),
    ('class="compare-report-card compare-report-a"','A/baseline identity card missing'),
    ('class="compare-report-card compare-report-b"','B/candidate identity card missing'),
    ('id="swapCompare"','Swap reports action missing'),
    ('class="compare-mode-panel"','grouped comparison-mode controls missing'),
    ('class="compare-filter-panel subfilters"','dedicated evidence-filter panel missing'),
    ('class="compare-overview"','comparison difference overview missing'),
    ('compare-row-one-sided','one-sided compare row distinction missing'),
    ('Cross-producer comparison:','cross-producer warning lost'),
    ('Profile definition revisions differ:','profile revision warning lost'),
    ('Common evidence only','common-evidence control lost'),
]: need(token in app,msg)
for token,msg in [
    ('.compare-report-a:before','A visual lane missing'),
    ('.compare-report-b:before','B visual lane missing'),
    ('.compare-section table th:nth-child(2)','A column differentiation missing'),
    ('.compare-section table th:nth-child(3)','B column differentiation missing'),
]: need(token in css,msg)

# Release/rules boundaries.
need('## Release 1.0.24 regional time / country identity / Compare workspace requirements' in rules,'PROJECT_RULES 1.0.24 section missing')
need((root/'rules/1.0.24_REGIONAL_TIME_COMPARE_COUNTRY_AUDIT.md').is_file(),'1.0.24 audit document missing')
need(worker.count("databaseReleaseVersion:'1.0.24'")>=3,'Worker database release identity mismatch')
need(worker.count("workerReleaseVersion:'1.0.24'")>=3,'Worker release identity mismatch')
for token in ["assert.equal(j.databaseReleaseVersion,'1.0.24')","await call('/v1/network-info',{method:'POST'})"]:
    need(token in tests,f'Worker current contract test missing: {token}')

if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.0.24 regional time / Compare / country contract')
