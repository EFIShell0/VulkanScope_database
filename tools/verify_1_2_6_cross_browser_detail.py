from pathlib import Path
import argparse,json
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1206.js'); compat=text('assets/browser-compat.v1206.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.6'" in app,'frontend 1.2.6 identity missing')
need('assets/app.v1206.js?v=1206' in index and 'browser-compat.v1206.js?v=1206' in index and 'site.v0390.css?v=1206' in index,'1.2.6 cache references missing')
need('VulkanScope Database <strong>1.2.6</strong>' in index,'footer identity missing')
need('"databaseVersion":"1.2.6"' in text('data/release.json').replace(' ',''),'release marker version missing')
need('"databaseVersion":"1.2.6"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_6_cross_browser_detail.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_6_cross_browser_detail_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
    need('verify_1_2_5_scrollbar_motion.py' not in wf,f'{name}: stale 1.2.5 verifier remains')
    need('for attempt in 1 2 3 4 5' in wf and 'HTTP 429|HTTP 5[0-9][0-9]|rate limit|temporarily unavailable' in wf,f'{name}: bounded GitHub release retry missing')
# Browser floor inherited.
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors missing')
# Cross-browser DOM viewport scrollbar.
for token in ['id="viewportScrollbar"','id="viewportScrollbarUp"','id="viewportScrollbarTrack"','id="viewportScrollbarThumb"','id="viewportScrollbarDown"']:
    need(token in index,f'viewport scrollbar markup missing: {token}')
need("document.documentElement.classList.add('viewport-scrollbar-mounted')" in app,'native viewport scrollbar replacement mount missing')
need('const viewportScrollMetrics=()=>' in app and 'document.scrollingElement||document.documentElement' in app and 'const syncViewportScrollbar=(metrics=viewportScrollMetrics())=>' in app and "rail.classList.toggle('at-top',atTop)" in app and "rail.classList.toggle('at-bottom',atBottom)" in app and "rail.dataset.endpoint=atTop?'top':atBottom?'bottom':'middle'" in app,'cross-browser viewport scrollbar endpoint synchronization missing')
need("up.disabled=atTop" in app and "down.disabled=atBottom" in app,'viewport scrollbar boundary semantics missing')
need("thumb.addEventListener('pointerdown'" in app and "thumb.addEventListener('keydown'" in app and "track.addEventListener('pointerdown'" in app,'viewport scrollbar drag/keyboard/track controls missing')
need('html.viewport-scrollbar-mounted,body.viewport-scrollbar-mounted{scrollbar-width:none!important' in css and 'body.viewport-scrollbar-mounted::-webkit-scrollbar' in css and "document.body?.classList.add('viewport-scrollbar-mounted')" in app,'native viewport chrome hide-after-mount missing')
need('.viewport-scrollbar.at-top .viewport-scrollbar-up' in css and '.viewport-scrollbar[data-endpoint="top"] .viewport-scrollbar-up' in css and '#66636a' in css and 'filter:grayscale(1) saturate(0)!important' in css,'top UP gray state missing')
need('.viewport-scrollbar.at-bottom .viewport-scrollbar-down' in css and '.viewport-scrollbar[data-endpoint="bottom"] .viewport-scrollbar-down' in css and '#ff5c66' in css,'bottom DOWN Vulkan-red state missing')
# Detail workspace and full report identity.
need('detail-back-button' in index and '<span>Back</span>' in index and 'position:sticky' in css and 'min-height:50px' in css,'large persistent detail Back control missing')
need('detail-hero-v126' in app and 'detail-identity-grid' in app,'redesigned detail hero missing')
need('full 64 hexadecimal characters' in app and 'detail-report-id' in app and '.detail-id-full{grid-column:1/-1' in css,'full-width 64-character report ID hero presentation missing')
need("navigator.clipboard.writeText(reportId)" in app,'copy full report ID action missing')
need('detail-overview-grid' in app and 'detail-overview-report-id' in app,'grouped Overview/full report ID missing')
need('word-break:break-all' in css and '.detail-report-id' in css,'full report ID mobile wrapping missing')
need('.detail-back-button{' in css and '.detail-overview-section{' in css,'detail/back redesign CSS missing')
# Motion/reduced motion inherited and extended.
need('@media(prefers-reduced-motion:reduce)' in css and '.viewport-scrollbar-thumb' in css and '.detail-identity-card' in css,'new detail/scrollbar reduced-motion coverage missing')
# Data invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need("databaseReleaseVersion:'1.2.6'" in worker and "workerReleaseVersion:'1.2.6'" in worker,'Worker release identity missing')
need('## Release 1.2.6 cross-browser viewport-scrollbar / report-detail workspace requirements' in rules,'1.2.6 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.6','releaseReady':False,'appAsset':'assets/app.v1206.js','cacheKey':'1206'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.6 cross-browser viewport-scrollbar / detail contract')
