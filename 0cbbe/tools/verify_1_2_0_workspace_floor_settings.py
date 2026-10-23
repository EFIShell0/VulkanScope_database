from __future__ import annotations
from pathlib import Path
import argparse,re,sys,json

parser=argparse.ArgumentParser()
parser.add_argument('--root',default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')

app=text('assets/app.v1200.js'); css=text('assets/site.v0390.css'); index=text('index.html'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md'); contract=text('worker/tests/contract.mjs')
need("const DATABASE_VERSION='1.2.0',LIVE_SYNC_INTERVAL_MS=3000,RELEASE_CHECK_INTERVAL_MS=10000,NETWORK_INFO_INTERVAL_MS=3000,NETWORK_PROBE_TIMEOUT_MS=2200;" in app,'1.2.0 frontend identity/timers missing')
need('assets/app.v1200.js?v=1200' in index and 'site.v0390.css?v=1200' in index and 'config.js?v=1200' in index,'1.2.0 cache-busted index references missing')
need('VulkanScope Database <strong>1.2.0</strong>' in index,'1.2.0 footer identity missing')

# Server-side producer floor and historical read compatibility.
need("const producerAtLeast1205=p=>" in worker and "const supportedProducer=p=>producerAtLeast1205(p)" in worker,'1.2.5 producer floor helper missing')
need("VulkanScope 1.2.5 or newer is required for new submissions" in worker,'1.2.5 POST rejection message missing')
need("if(v.major===1)return p.application.versionCode===1000+v.minor*100+v.patch" in worker,'1.x versionCode identity mapping missing')
need("current.application.version='1.2.5'" in contract and "current.application.versionCode=1205" in contract,'Worker contract does not accept 1.2.5/1205')
need("below.application.version='1.2.4'" in contract and "below.application.versionCode=1204" in contract,'Worker contract does not reject 1.2.4/1204')
need("historicalPayload.application.version='0.80.9'" in contract and "assert.equal(r.status,200)" in contract,'historical stored-report readability test missing')

# Silent automatic Internet observation after initial data.
need("settingsNetworkBusy=true;if(!settingsNetworkData)renderNetworkInfo();try{" in app,'background network observation should render busy state only before first data')
need('Updating connection observation…' not in app,'recurring automatic network update message must be absent')
need('NETWORK_INFO_INTERVAL_MS=3000' in app and 'syncNetworkInfoAutoRefresh' in app,'automatic network refresh cadence missing')

# Country selector is readable, English-UI consistent, and fully locally flagged.
need("new Intl.DisplayNames(['en'],{type:'region'})" in app,'country selector must use English UI country names')
need("sel?.id==='settingsRegionalCountry'" in app and 'filter-country-flag' in app,'country custom-select flag rendering missing')
need("wrap.classList.add('country-custom-select')" in app and "classList.add('settings-country-row')" in app,'country custom-select layout marker missing')
need('.country-custom-select' in css and '.settings-country-row' in css and '.filter-country-flag' in css,'country selector readable/wide flag CSS missing')
m=re.search(r"const COUNTRY_CODES=Object\.freeze\('([^']+)'\.split\(','\)\);",app)
need(bool(m),'country code allow-list missing')
codes=m.group(1).split(',') if m else []
flags=root/'assets/country-flags'; actual=sorted(p.stem.upper() for p in flags.glob('*.png')) if flags.is_dir() else []
need(len(codes)==250 and len(set(codes))==250,'country code allow-list must contain 250 unique codes')
need(actual==sorted(codes),f'country flag asset set mismatch expected={len(codes)} actual={len(actual)}')
need('flagcdn' not in app.lower() and 'countryflags' not in app.lower(),'third-party flag service forbidden')

# Compare producer version emphasis.
need('class="compare-producer-version"' in app and '.compare-producer-version' in css,'Compare producer-version emphasis missing')
need('color:#fff!important' in css and 'font-weight:900!important' in css,'Compare producer-version bold white style missing')
need('Cross-producer comparison:' in app,'cross-producer explanatory warning missing')

# Every non-Reports primary view gets a distinct workspace purpose; filters are grouped without changing semantics.
expected={'devices','versions','properties','limits','features','formats','memory','queues','surface','display','extensions','instance','profiles','portability','trends','encyclopedia','compare'}
block=re.search(r"const WORKSPACE_UI=Object\.freeze\(\{(.*?)\}\);",app,re.S)
need(bool(block),'WORKSPACE_UI missing')
found=set(re.findall(r"\n\s*([a-z]+):\{tone:",block.group(1) if block else ''))
need(found==expected,f'non-Reports workspace coverage mismatch missing={sorted(expected-found)} extra={sorted(found-expected)}')
for token in ['Hardware','Vulkan & driver','Platform','Producer','Submission','Evidence state','Display evidence']:
    need(token in app,f'global filter family missing: {token}')
need('function organizeGlobalFilters()' in app and 'function decorateWorkspaceView' in app,'workspace/filter organizer functions missing')
need('.workspace-context' in css and '.filter-family' in css and '#contentView[data-main-view]:not([data-main-view="reports"]) .subfilters' in css,'non-Reports workspace/filter workbench CSS missing')
for token in ['encyclopedia-workspace','surface-workspace','compare-workspace']:
    need(token in app and f'.{token}' in css,f'specialized workspace missing: {token}')

# Settings messages: icon + semantic color, not color alone.
need('settingsMessageMarkup' in app and 'settingsMessageIcon' in app,'Settings semantic message helper missing')
need('settings-message-info' in css and 'settings-message-warning' in css and 'settings-message-icon' in css,'Settings info/warning CSS missing')
need('.settings-message-info{color:#cbd7ff!important' in css and '.settings-message-warning{color:#ffe3a0!important' in css,'Settings semantic info/warning colors missing')
need('<circle cx="12" cy="12" r="9"/>' in app and 'M12 3 2.8 20h18.4L12 3Z' in app,'information/warning SVG icons missing')
need('settings-message settings-message-info' in index,'static Settings informational callouts missing')

# Release rules + immutable model.
need('## Release 1.2.0 submission floor / workspace / Settings clarity requirements' in rules,'1.2.0 rules section missing')
need('1.2.5 or newer' in rules and 'historical GET readability remain unchanged' in rules,'1.2.0 submission-floor/legacy-read rules missing')
need('No D1 migration' in rules or 'D1 schema/migrations' in rules,'D1 immutability rule missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.0','releaseReady':False,'appAsset':'assets/app.v1200.js','cacheKey':'1200'},'source release marker mismatch')

if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print(f'PASS VulkanScope Database 1.2.0 workspace/floor/settings contract flags={len(actual)} workspaces={len(found)}')
