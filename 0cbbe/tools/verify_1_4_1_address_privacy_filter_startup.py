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

index=text('index.html'); app=text('assets/app.v1401.js'); css=text('assets/site.v1401.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')

need(marker=={'schemaVersion':2,'databaseVersion':'1.4.1','releaseReady':False,'appAsset':'assets/app.v1401.js','cacheKey':'1401'},'1.4.1 release marker mismatch')
for token in ['./assets/site.v1401.css?v=1401','./assets/release-bootstrap.v1401.js?v=1401','./assets/browser-compat.v1401.js?v=1401','./assets/app.v1401.js?v=1401','VulkanScope Database <strong>1.4.1</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.1'" in app,'frontend Database version mismatch')

# Submission floor remains 1.4.0+; this patch must not change report-admission semantics.
need("const producerAtLeast1400=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,1,4,0)}" in worker,'1.4.0 producer floor predicate missing')
need('const supportedProducer=p=>producerAtLeast1400(p)' in worker,'supportedProducer no longer uses 1.4.0 floor')
need('VulkanScope 1.4.0 or newer is required for new submissions' in worker,'1.4.0 POST rejection message missing')
for token in ["databaseReleaseVersion:'1.4.1'","workerReleaseVersion:'1.4.1'"]:
    need(worker.count(token)>=3,f'Worker 1.4.1 release metadata missing: {token}')

# Independent address-row reveal ownership.
need('const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};' in app,'independent address reveal slots missing')
need("networkAddressMarkup(n.activeAddress,activeFamily,'active')" in app,'Active address does not own an independent reveal slot')
need("networkAddressMarkup(n.ipv4.address,'IPv4','ipv4')" in app,'IPv4 row reveal slot missing')
need("networkAddressMarkup(n.ipv6.address,'IPv6','ipv6')" in app,'IPv6 row reveal slot missing')
need("networkAddressMarkup(n.pseudoIPv4,'IPv4','pseudo')" in app,'Pseudo IPv4 row reveal slot missing')
need('data-network-address-family=' in app and 'button.dataset.networkAddressFamily' in app,'row family metadata/accessibility ownership missing')
need('for(const key of Object.keys(networkAddressReveal))setNetworkAddressReveal(key,false)' in app,'closing/leaving Internet does not remask every reveal slot')
need("settingsNetworkData?.activeAddress!==fresh?.activeAddress)networkAddressReveal.active=false" in app,'changed Active address does not remask its slot')
need("settingsNetworkData?.ipv4?.address!==fresh?.ipv4?.address)networkAddressReveal.ipv4=false" in app,'changed IPv4 does not remask its slot')
need("settingsNetworkData?.ipv6?.address!==fresh?.ipv6?.address)networkAddressReveal.ipv6=false" in app,'changed IPv6 does not remask its slot')
need("settingsNetworkData?.pseudoIPv4!==fresh?.pseudoIPv4)networkAddressReveal.pseudo=false" in app,'changed Pseudo IPv4 does not remask its slot')
need("n.ipv4?.address?networkAddressMarkup(n.ipv4.address,'IPv4','ipv4'):'Not observed on this request'" in app,'unobserved IPv4 handling regressed')
need("n.ipv6?.address?networkAddressMarkup(n.ipv6.address,'IPv6','ipv6'):'Not observed on this request'" in app,'unobserved IPv6 handling regressed')
for token in ['.network-address-value{','.network-address-mosaic{grid-area:1/1;','.network-address-action{','@keyframes networkMosaicSheen','.network-address-toggle.is-revealed .network-address-mosaic{opacity:0','@media(prefers-reduced-motion:reduce){.network-address-toggle,.network-address-text,.network-address-mosaic,.network-address-action{transition:none!important}']:
    need(token in css,f'1.4.1 address privacy CSS missing: {token}')

# Hard startup filter hold: active before app execution, remains active throughout DB loading.
need('<body class="database-loading">' in index,'body must enter database-loading at parse time')
need('<div class="filters" id="filters" hidden>' in index,'HTML filter fallback must remain hidden')
need("document.body?.classList.toggle('database-loading',!!visible)" in app,'database loading owner does not control body startup class')
need('body.database-loading #filters{display:none!important}' in css,'loading-time filter suppression rule missing')
load_start=app.find('async function load(){'); render_pos=app.find('render();',load_start); finish_pos=app.find('setDatabaseLoading(false)',load_start)
need(load_start>=0 and render_pos>load_start and finish_pos>render_pos,'database-loading class must be cleared only after first committed render')
need('if(filterPanel)filterPanel.hidden=encyclopediaView' in app,'rendered-view filter owner regressed')
need('enhanceSelects()' in app,'native-select progressive enhancement missing')

# Settings order and regional selector corrections remain intact.
nav_start=index.find('<div class="settings-category-nav"'); nav_end=index.find('</div><div class="settings-drawer-body">',nav_start); nav=index[nav_start:nav_end]
pos=[nav.find('data-settings-category="favorites"'),nav.find('data-settings-category="preferences"'),nav.find('data-settings-category="internet"'),nav.find('data-settings-category="information"')]
need(nav_start>=0 and all(x>=0 for x in pos) and pos==sorted(pos),'Settings tabs order regressed')
need("const SETTINGS_SEARCHABLE_SELECTS=new Set(['settingsRegionalCountry','settingsRegionalTimeZone'])" in app,'regional searchable-selector contract regressed')
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'deterministic selector pagination regressed')
need('## Release 1.4.1 independent address controls / hard startup-filter hold requirements' in rules,'1.4.1 project-rules section missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.1 independent address privacy + hard startup-filter hold contract')
