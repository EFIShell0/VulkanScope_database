from __future__ import annotations
from pathlib import Path
import argparse, json, re, sys
ap=argparse.ArgumentParser(); ap.add_argument('--root',default=None); a=ap.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
index=text('index.html'); app=text('assets/app.v1404.js'); css=text('assets/site.v1404.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md')
try: marker=json.loads(text('data/release.json'))
except Exception as e: marker={}; errors.append(f'invalid release marker: {e}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.4','releaseReady':False,'appAsset':'assets/app.v1404.js','cacheKey':'1404'},'1.4.4 release marker mismatch')
for token in ['./assets/site.v1404.css?v=1404','./assets/release-bootstrap.v1404.js?v=1404','./assets/browser-compat.v1404.js?v=1404','./assets/app.v1404.js?v=1404','VulkanScope Database <strong>1.4.4</strong>']:
    need(token in index,f'current frontend identity missing: {token}')
need("const DATABASE_VERSION='1.4.4'" in app,'frontend Database version mismatch')
for token in ["databaseReleaseVersion:'1.4.4'","workerReleaseVersion:'1.4.4'"]:
    need(worker.count(token)>=3,f'Worker 1.4.4 release metadata missing: {token}')
# Preserve the 1.4.3 startup/address fixes.
need('<body class="database-loading startup-layout-hold">' in index,'parse-time startup hold missing')
need('<section id="databaseLoading" class="database-loading-panel" role="status" aria-live="polite" aria-atomic="true">' in index,'dedicated loading panel class missing')
need('body.startup-layout-hold #databaseLoading{position:fixed;z-index:590;left:50%;top:50%;right:auto;bottom:auto;transform:translate(-50%,-50%)' in css,'viewport-centered startup loader regressed')
need('const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};' in app,'independent address reveal state regressed')
need('.settings-info-row-address .network-address-toggle{width:100%;max-width:100%;min-width:0' in css,'responsive address row regressed')
# Recorded scroll-chrome bug: no containing-block-producing transform on #appRoot reveal.
reveal='body.startup-layout-ready #appRoot{animation:startupShellReveal .22s cubic-bezier(.2,.8,.2,1) both}'
need(reveal in css,'startup reveal owner missing')
m=re.search(r'@keyframes\s+startupShellReveal\s*\{([^}]*(?:\}[^@}]*)?)\}',css)
need('@keyframes startupShellReveal{from{opacity:0}to{opacity:1}}' in css,'startup reveal must be opacity-only')
need('body.startup-layout-ready #appRoot{transform:' not in css,'appRoot startup-ready rule applies transform')
need('body.startup-layout-ready #appRoot{filter:' not in css,'appRoot startup-ready rule applies filter')
need('body.startup-layout-ready #appRoot{perspective:' not in css,'appRoot startup-ready rule applies perspective')
# Fixed page chrome remains viewport-owned and synchronized to actual document metrics.
need('.page-progress{position:fixed;inset:0 0 auto 0;height:3px;z-index:230;' in css,'page progress is not viewport-fixed above sticky header')
need('.viewport-scrollbar{position:fixed;z-index:220;top:0;right:0;bottom:0;width:18px;' in css,'viewport scrollbar is not fixed to viewport')
need('const viewportScrollMetrics=()=>{' in app and 'scrolling?.scrollHeight' in app and 'scrolling?.scrollTop' in app,'viewport scrollbar metrics are not sourced from actual document scroll state')
need('thumbHeight=Math.max(46,Math.min(trackHeight,trackHeight*(viewport/doc)))' in app,'viewport thumb visible-fraction formula changed')
viewport_sync=app.split('const updatePageScrollUi',1)[0].split('const syncViewportScrollbar',1)[1]
need('thumb.style.transform=`translateY(${travel*ratio}px)`' in viewport_sync,'viewport thumb position mapping changed')
need("if(progress)progress.classList.toggle('is-scrollable',scrollable)" in app and "bar.style.transform=`scaleX(${scrollable?Math.min(1,Math.max(0,y/max)):0})`" in app,'top page-progress scroll synchronization missing')
need("window.addEventListener('scroll',()=>{queuePageScrollUi(true);queueCompareStickyState()},{passive:true})" in app,'scroll event no longer synchronizes page chrome')
need("const pageResizeObserver=new ResizeObserver(()=>queuePageScrollUi(false));pageResizeObserver.observe(document.body)" in app,'content resize no longer resynchronizes page chrome')
need('@media(max-width:760px){.viewport-scrollbar{width:16px;' in css,'mobile viewport scrollbar geometry missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.viewport-scrollbar' in css,'reduced-motion scrollbar contract missing')
# Release boundary / bridge.
need('## Release 1.4.4 viewport-scroll / page-progress containing-block requirements' in rules,'1.4.4 project-rules section missing')
need("PREDECESSOR_BRIDGE = {'app.v1403.js','browser-compat.v1403.js','release-bootstrap.v1403.js'}" in text('tools/repair_repository.py'),'1.4.4 predecessor bridge mismatch')
pages=text('tools/build_pages_artifact.py')
need("'assets/app.v1403.js'" in pages and "'assets/app.v1404.js'" in pages and "'assets/app.v1402.js'" not in pages,'Pages predecessor/current app bridge mismatch')
need("'assets/site.v1403.css'" in pages and "'assets/site.v1404.css'" in pages,'Pages stylesheet predecessor/current assets missing')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); sys.exit(1)
print('PASS Database 1.4.4 viewport-scroll + fixed page-progress containing-block contract')
