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

index=text('index.html'); app=text('assets/app.v1402.js'); css=text('assets/site.v1402.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')

need(marker=={'schemaVersion':2,'databaseVersion':'1.4.2','releaseReady':False,'appAsset':'assets/app.v1402.js','cacheKey':'1402'},'1.4.2 release marker mismatch')
for token in ['./assets/site.v1402.css?v=1402','./assets/release-bootstrap.v1402.js?v=1402','./assets/browser-compat.v1402.js?v=1402','./assets/app.v1402.js?v=1402','VulkanScope Database <strong>1.4.2</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.2'" in app,'frontend Database version mismatch')

# Submission floor / stored semantics remain untouched.
need("const producerAtLeast1400=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,1,4,0)}" in worker,'1.4.0 producer floor predicate missing')
need('const supportedProducer=p=>producerAtLeast1400(p)' in worker,'supportedProducer no longer uses 1.4.0 floor')
need('VulkanScope 1.4.0 or newer is required for new submissions' in worker,'1.4.0 POST rejection message missing')
for token in ["databaseReleaseVersion:'1.4.2'","workerReleaseVersion:'1.4.2'"]:
    need(worker.count(token)>=3,f'Worker 1.4.2 release metadata missing: {token}')

# Stable startup shell: parse-time hold, stable loading card, first render before reveal.
need('<body class="database-loading startup-layout-hold">' in index,'parse-time startup layout hold missing')
need('<div class="filters" id="filters" hidden>' in index,'HTML filter fallback must remain hidden')
need("document.body?.classList.toggle('database-loading',!!visible)" in app,'database-loading owner missing')
need("body.classList.remove('startup-layout-hold');body.classList.add('startup-layout-ready')" in app,'one-way startup-layout reveal owner missing')
need('body.database-loading #filters{display:none!important}' in css,'loading-time filter suppression missing')
need('body.startup-layout-hold #networkStatusShell' in css and 'body.startup-layout-hold .topbar' in css and 'body.startup-layout-hold .hero' in css and 'body.startup-layout-hold #contentView' in css and 'body.startup-layout-hold footer{display:none!important}' in css,'unstable startup shell is not fully suppressed')
need('body.startup-layout-hold #databaseLoading{' in css,'stable startup loading card styling missing')
need('body.startup-layout-ready #appRoot{animation:startupShellReveal' in css,'post-render shell reveal missing')
need('@media(prefers-reduced-motion:reduce){body.startup-layout-ready #appRoot{animation:none!important}' in css,'reduced-motion startup reveal suppression missing')
load_start=app.find('async function load(){')
render_pos=app.find('render();',load_start)
loading_finish=app.find('setDatabaseLoading(false)',load_start)
layout_finish=app.find('finishStartupLayout()',load_start)
need(load_start>=0 and render_pos>load_start and loading_finish>render_pos and layout_finish>loading_finish,'startup hold/loading must clear only after first committed render')
catch_pos=app.rfind('load().catch(')
need(catch_pos>=0 and 'setDatabaseLoading(false);finishStartupLayout();' in app[catch_pos:catch_pos+500],'fatal startup must release both loading and layout hold before fatal presentation')

# Independent IP privacy state and improved presentation.
need('const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};' in app,'independent address reveal slots missing')
for token in ["networkAddressMarkup(n.activeAddress,activeFamily,'active')","networkAddressMarkup(n.ipv4.address,'IPv4','ipv4')","networkAddressMarkup(n.ipv6.address,'IPv6','ipv6')","networkAddressMarkup(n.pseudoIPv4,'IPv4','pseudo')"]:
    need(token in app,f'independent address row missing: {token}')
need('const networkAddressShieldIcon=' in app and 'class="network-address-privacy-mark"' in app,'privacy shield/status mark missing')
need('data-network-address-toggle=' in app and 'button.dataset.networkAddressToggle' in app,'row-local address toggle ownership missing')
need('for(const key of Object.keys(networkAddressReveal))setNetworkAddressReveal(key,false)' in app,'leaving Internet no longer remasks all address slots')
need("settingsNetworkData?.ipv4?.address!==fresh?.ipv4?.address)networkAddressReveal.ipv4=false" in app,'changed IPv4 does not remask')
need("settingsNetworkData?.ipv6?.address!==fresh?.ipv6?.address)networkAddressReveal.ipv6=false" in app,'changed IPv6 does not remask')
need("n.ipv4?.address?networkAddressMarkup(n.ipv4.address,'IPv4','ipv4'):'Not observed on this request'" in app,'unobserved IPv4 handling regressed')
need("n.ipv6?.address?networkAddressMarkup(n.ipv6.address,'IPv6','ipv6'):'Not observed on this request'" in app,'unobserved IPv6 handling regressed')
for token in ['.network-address-privacy-mark{','.network-address-mosaic::before{','.network-address-mosaic::after{','@keyframes networkMosaicSheen','.network-address-ipv4{--network-address-accent:','.network-address-ipv6{--network-address-accent:','.network-address-toggle.is-masked .network-address-text{filter:blur(8px)','.network-address-toggle.is-revealed .network-address-mosaic{opacity:0']:
    need(token in css,f'1.4.2 address privacy presentation missing: {token}')
need('.network-address-mosaic::after{animation:none!important;display:none}' in css,'reduced-motion mosaic sheen suppression missing')

# Predecessor bridge and release rules.
need('## Release 1.4.2 stable startup layout / address privacy presentation requirements' in rules,'1.4.2 project-rules section missing')
need("PREDECESSOR_BRIDGE = {'app.v1401.js','browser-compat.v1401.js','release-bootstrap.v1401.js'}" in text('tools/repair_repository.py'),'1.4.2 predecessor bridge mismatch')
pages=text('tools/build_pages_artifact.py')
need("'assets/app.v1401.js'" in pages and "'assets/app.v1402.js'" in pages and "'assets/app.v1400.js'" not in pages,'Pages predecessor/current app bridge mismatch')

if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.2 stable startup layout + address privacy presentation contract')
