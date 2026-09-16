from __future__ import annotations
from pathlib import Path
import argparse, json, re, sys

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

index=text('index.html'); app=text('assets/app.v1403.js'); css=text('assets/site.v1403.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')

need(marker=={'schemaVersion':2,'databaseVersion':'1.4.3','releaseReady':False,'appAsset':'assets/app.v1403.js','cacheKey':'1403'},'1.4.3 release marker mismatch')
for token in ['./assets/site.v1403.css?v=1403','./assets/release-bootstrap.v1403.js?v=1403','./assets/browser-compat.v1403.js?v=1403','./assets/app.v1403.js?v=1403','VulkanScope Database <strong>1.4.3</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.3'" in app,'frontend Database version mismatch')
for token in ["databaseReleaseVersion:'1.4.3'","workerReleaseVersion:'1.4.3'"]:
    need(worker.count(token)>=3,f'Worker 1.4.3 release metadata missing: {token}')
need("const producerAtLeast1400=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,1,4,0)}" in worker,'1.4.0 producer floor predicate missing')
need('VulkanScope 1.4.0 or newer is required for new submissions' in worker,'1.4.0 POST rejection message missing')

# Recorded startup bug: state/presentation class collision must be impossible.
need('<body class="database-loading startup-layout-hold">' in index,'parse-time body loading/layout state missing')
need('<section id="databaseLoading" class="database-loading-panel" role="status" aria-live="polite" aria-atomic="true">' in index,'loading panel must have a presentation class distinct from body state')
need('<section id="databaseLoading" class="database-loading"' not in index,'loading panel reuses body database-loading state class')
need('.database-loading-panel{' in css and '.database-loading-panel[hidden]{display:none!important}' in css,'dedicated loading-panel styling missing')
need(re.search(r'(?<![\w-])\.database-loading\s*\{',css) is None,'generic .database-loading panel rule still styles the body state')
need("document.body?.classList.toggle('database-loading',!!visible)" in app,'database-loading runtime state owner missing')
need('body.database-loading #filters{display:none!important}' in css,'loading-time filter suppression missing')

# Viewport-owned startup centering, not shell geometry.
need('body.startup-layout-hold #networkStatusShell' in css and 'body.startup-layout-hold .topbar' in css and 'body.startup-layout-hold .hero' in css and 'body.startup-layout-hold #contentView' in css and 'body.startup-layout-hold footer{display:none!important}' in css,'unstable startup shell is not fully suppressed')
startup_rule='body.startup-layout-hold #databaseLoading{position:fixed;z-index:590;left:50%;top:50%;right:auto;bottom:auto;transform:translate(-50%,-50%);width:min(760px,calc(100vw - 36px));max-width:calc(100vw - 36px);max-height:calc(100dvh - 36px);overflow:auto;margin:0;padding:20px 22px}'
need(startup_rule in css,'viewport-centered desktop startup loading rule missing')
need('body.startup-layout-hold #databaseLoading{width:calc(100vw - 20px);max-width:calc(100vw - 20px);max-height:calc(100dvh - 20px);padding:16px 15px;border-radius:17px}' in css,'mobile startup loading bounds missing')
need("body.classList.remove('startup-layout-hold');body.classList.add('startup-layout-ready')" in app,'one-way startup layout release owner missing')
load_start=app.find('async function load(){'); render_pos=app.find('render();',load_start); loading_finish=app.find('setDatabaseLoading(false)',load_start); layout_finish=app.find('finishStartupLayout()',load_start)
need(load_start>=0 and render_pos>load_start and loading_finish>render_pos and layout_finish>loading_finish,'startup hold/loading must clear only after first committed render')
catch_pos=app.rfind('load().catch(')
need(catch_pos>=0 and 'setDatabaseLoading(false);finishStartupLayout();' in app[catch_pos:catch_pos+500],'fatal startup must release loading/layout hold before fatal presentation')

# Address controls: independent privacy plus no truncation at desktop/mobile widths.
need('const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};' in app,'independent address reveal slots missing')
for token in ["networkAddressMarkup(n.activeAddress,activeFamily,'active')","networkAddressMarkup(n.ipv4.address,'IPv4','ipv4')","networkAddressMarkup(n.ipv6.address,'IPv6','ipv6')","networkAddressMarkup(n.pseudoIPv4,'IPv4','pseudo')"]:
    need(token in app,f'independent address row missing: {token}')
need("settings-info-row${html&&String(v).includes('network-address-toggle')?' settings-info-row-address':''}" in app,'observed address rows do not receive the full-width address-row class')
for token in ['.settings-info-row-address{grid-template-columns:minmax(0,1fr)!important;gap:6px!important;align-items:stretch}', '.settings-info-row-address>strong{display:block;min-width:0;width:100%;text-align:left!important}', '.settings-info-row-address .network-address-toggle{width:100%;max-width:100%;min-width:0;grid-template-columns:30px minmax(0,1fr) auto}', '.settings-info-row-address .network-address-value{width:100%;min-width:0;max-width:none}']:
    need(token in css,f'full-width address layout missing: {token}')
need('.network-address-text{max-width:none;overflow:visible;text-overflow:clip;white-space:normal;overflow-wrap:anywhere;word-break:break-all;line-height:1.28}' in css,'address text can still truncate instead of wrapping safely')
need('@media(max-width:520px)' in css and '.settings-info-row-address .network-address-toggle{grid-template-columns:28px minmax(0,1fr) auto;gap:6px}' in css,'520px address fit rule missing')
need('@media(max-width:340px)' in css and '.settings-info-row-address .network-address-toggle{grid-template-columns:26px minmax(0,1fr) auto;gap:5px}' in css,'340px address fit rule missing')
need('.network-address-mosaic::before{' in css and '.network-address-mosaic::after{' in css and '.network-address-toggle.is-masked .network-address-text{filter:blur(8px)' in css and '.network-address-toggle.is-revealed .network-address-mosaic{opacity:0' in css,'opaque address privacy presentation regressed')
need('.network-address-mosaic::after{animation:none!important;display:none}' in css,'reduced-motion mosaic behavior missing')

# Release boundary / bridge.
need('## Release 1.4.3 startup-loader isolation / address-fit requirements' in rules,'1.4.3 project-rules section missing')
need("PREDECESSOR_BRIDGE = {'app.v1402.js','browser-compat.v1402.js','release-bootstrap.v1402.js'}" in text('tools/repair_repository.py'),'1.4.3 predecessor bridge mismatch')
pages=text('tools/build_pages_artifact.py')
need("'assets/app.v1402.js'" in pages and "'assets/app.v1403.js'" in pages and "'assets/app.v1401.js'" not in pages,'Pages predecessor/current app bridge mismatch')
need("'assets/site.v1402.css'" in pages and "'assets/site.v1403.css'" in pages,'Pages stylesheet predecessor/current assets missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.3 startup-loader isolation + responsive address-fit contract')
