from __future__ import annotations
from pathlib import Path
import argparse, json, sys

ap=argparse.ArgumentParser()
ap.add_argument('--root',default=None)
a=ap.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def text(rel):
    p=root/rel
    if not p.is_file():
        errors.append(f'missing {rel}')
        return ''
    return p.read_text(encoding='utf-8')

index=text('index.html'); app=text('assets/app.v1400.js'); css=text('assets/site.v1400.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')

need(marker=={'schemaVersion':2,'databaseVersion':'1.4.0','releaseReady':False,'appAsset':'assets/app.v1400.js','cacheKey':'1400'},'1.4.0 release marker mismatch')
for token in ['./assets/site.v1400.css?v=1400','./assets/release-bootstrap.v1400.js?v=1400','./assets/browser-compat.v1400.js?v=1400','./assets/app.v1400.js?v=1400','VulkanScope Database <strong>1.4.0</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.0'" in app,'frontend Database version mismatch')

# Requested submission floor: 1.4.0 accepted, everything lower blocked at POST boundary.
need("const producerAtLeast1400=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,1,4,0)}" in worker,'1.4.0 producer floor predicate missing')
need('const supportedProducer=p=>producerAtLeast1400(p)' in worker,'supportedProducer does not use 1.4.0 floor')
need('VulkanScope 1.4.0 or newer is required for new submissions' in worker,'1.4.0 POST rejection message missing')
need('VulkanScope 1.2.5 or newer is required for new submissions' not in worker,'obsolete 1.2.5 POST floor remains')
post=worker.find("url.pathname==='/v1/reports'&&request.method==='POST'"); floor=worker.find('!supportedProducer(p)',post); get=worker.find("url.pathname.startsWith('/v1/reports/')&&request.method==='GET'")
need(get>=0 and post>get and floor>post,'producer floor must be POST-only and historical GET path must remain before it')
for token in ["databaseReleaseVersion:'1.4.0'","workerReleaseVersion:'1.4.0'",'VulkanScope 1.4.0 · Vulkan 1.4.362','VulkanScope 1.4.0+ · schema 2 / technical report 3']:
    need(token in worker,f'Worker 1.4.0 metadata missing: {token}')

# Settings category ordering and ownership.
nav_start=index.find('<div class="settings-category-nav"'); nav_end=index.find('</div><div class="settings-drawer-body">',nav_start); nav=index[nav_start:nav_end]
pos=[nav.find('data-settings-category="favorites"'),nav.find('data-settings-category="preferences"'),nav.find('data-settings-category="internet"'),nav.find('data-settings-category="information"')]
need(nav_start>=0 and all(x>=0 for x in pos) and pos==sorted(pos),'Settings tabs are not Favorites, Preferences, Internet, Information')
need('data-settings-category="favorites"' in nav and 'settings-category-button active' in nav.split('data-settings-category="favorites"')[0][-300:],'Favorites is not the default active Settings category')
need("settingsActiveCategory='favorites'" in app,'Settings default state is not Favorites')
need("const allowed=new Set(['favorites','preferences','internet','information'])" in app,"Settings JS category order/fallback contract missing")

# Request-scoped IP privacy: observed values only, mosaicked initially, reversible, and remasked.
need('const networkAddressReveal={ipv4:false,ipv6:false};' in app,'address reveal state must default masked')
for token in ['networkAddressMarkup','data-network-address-toggle','setNetworkAddressReveal','maskNetworkAddresses','wireNetworkAddressToggles']:
    need(token in app,f'address mosaic control missing: {token}')
need("n.ipv4?.address?networkAddressMarkup(n.ipv4.address,'IPv4'):'Not observed on this request'" in app,'IPv4 absent-family handling/in-place mosaic missing')
need("n.ipv6?.address?networkAddressMarkup(n.ipv6.address,'IPv6'):'Not observed on this request'" in app,'IPv6 absent-family handling/in-place mosaic missing')
need("if(previousCategory==='internet'&&category!=='internet')maskNetworkAddresses()" in app,'leaving Internet must remask addresses')
need('stopNetworkInfoAutoRefresh();maskNetworkAddresses();' in app,'closing Settings must remask addresses')
need("if(settingsNetworkData?.ipv4?.address!==fresh?.ipv4?.address)networkAddressReveal.ipv4=false" in app and "if(settingsNetworkData?.ipv6?.address!==fresh?.ipv6?.address)networkAddressReveal.ipv6=false" in app,'newly observed addresses must not inherit reveal state')
for token in ['.network-address-toggle::after','.network-address-toggle.is-masked .network-address-text','.network-address-toggle.is-revealed::after','transition:filter .24s','@media(prefers-reduced-motion:reduce){.network-address-text,.network-address-toggle::after{transition:none!important}']:
    need(token in css,f'address mosaic/animation CSS missing: {token}')

# Native filters remain authoritative but cannot flash before the first report-backed render.
need('<div class="filters" id="filters" hidden>' in index,'filters must be HTML-hidden during startup')
need('if(filterPanel)filterPanel.hidden=encyclopediaView' in app,'rendered-view owner must restore/hide filters after loading')
need('enhanceSelects()' in app,'native-select progressive enhancement missing')

# Preserve the immediately previous selector correction.
need("const SETTINGS_SEARCHABLE_SELECTS=new Set(['settingsRegionalCountry','settingsRegionalTimeZone'])" in app,'1.3.10 regional searchable-selector contract regressed')
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'1.3.10 deterministic selector pagination regressed')
need('## Release 1.4.0 submission floor / Settings order / address mosaic / startup-filter requirements' in rules,'1.4.0 project-rules section missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.0 submission floor + Settings order + IP mosaic + startup-filter contract')
