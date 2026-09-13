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
app=text('assets/app.v1208.js'); compat=text('assets/browser-compat.v1208.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
# Release identity / CI freshness.
need("const DATABASE_VERSION='1.2.8'" in app,'frontend 1.2.8 identity missing')
need('assets/app.v1208.js?v=1208' in index and 'browser-compat.v1208.js?v=1208' in index and 'site.v0390.css?v=1208' in index,'1.2.8 cache references missing')
need('VulkanScope Database <strong>1.2.8</strong>' in index,'footer identity missing')
need('"databaseVersion":"1.2.8"' in text('data/release.json').replace(' ',''),'release marker version missing')
need('"databaseVersion":"1.2.8"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_8_compare_fixed_follow.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_8_compare_fixed_follow_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
    need('python tools/verify_1_2_7_compare_hero_scroll.py' not in wf,f'{name}: stale 1.2.7 verifier remains in active CI')
    need('for attempt in 1 2 3 4 5' in wf and 'HTTP 429|HTTP 5[0-9][0-9]|rate limit|temporarily unavailable' in wf,f'{name}: bounded GitHub release retry missing')
# Browser floor retained.
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors missing')
# Compare follow: explicit fixed pin + placeholder, not ancestor-sensitive CSS sticky.
for token in ['id="compareStickySentinel"','id="compareStickyPlaceholder" class="compare-sticky-placeholder"','id="compareStickyShell" class="compare-sticky-shell"']:
    need(token in app,f'Compare fixed-follow markup missing: {token}')
need('function clearComparePinnedGeometry(shell,placeholder,workspace)' in app,'Compare fixed geometry reset missing')
need("shell.style.position='fixed'" in app and "shell.style.top=`${top}px`" in app and "shell.style.left=`${left}px`" in app and "shell.style.width=`${width}px`" in app,'Compare shell is not explicitly fixed to live viewport geometry')
need("placeholder.style.height=`${compareStickyFlowHeight}px`" in app and "placeholder.style.height='0px'" in app,'Compare flow placeholder lifecycle missing')
need("const pageRect=page.getBoundingClientRect()" in app and "viewportWidth=Math.max(1,document.documentElement.clientWidth||window.innerWidth||1)" in app,'Compare fixed width/left geometry is not viewport-aware')
need("rightReserve=$('#viewportScrollbar')?.classList.contains('is-scrollable')?20:4" in app,'Compare fixed shell does not reserve authoritative viewport rail')
need('.compare-sticky-shell{position:relative' in css and '.compare-sticky-shell.is-pinned{position:fixed' in css,'Compare fixed-follow CSS contract missing')
need('.compare-sticky-placeholder{height:0' in css,'Compare fixed-follow placeholder CSS missing')
need('.compare-sticky-shell{position:sticky' not in css,'ancestor-sensitive Compare CSS sticky ownership still active')
need("w.closest('.compare-report-card')?.classList.remove('select-open')" in app and "wrap.closest('.compare-report-card')?.classList.add('select-open')" in app,'Compare selector card elevation lifecycle missing')
need('.compare-sticky-shell.is-pinned .custom-select-menu' in css and 'z-index:460' in css,'Pinned Compare selector menu elevation missing')
# Existing authoritative viewport rail + report detail behavior retained.
for token in ['id="viewportScrollbar"','id="viewportScrollbarUp"','id="viewportScrollbarTrack"','id="viewportScrollbarThumb"','id="viewportScrollbarDown"']:
    need(token in index,f'viewport scrollbar markup missing: {token}')
need('document.scrollingElement' in app and 'remaining=Math.max(0,max-y)' in app,'viewport endpoint metrics regression')
need('atBottom=!scrollable||remaining<=2' in app and 'down.disabled=atBottom' in app,'viewport bottom endpoint state regression')
need('.viewport-scrollbar-thumb,.viewport-scrollbar-thumb:hover,.viewport-scrollbar.is-dragging .viewport-scrollbar-thumb{cursor:default!important}' in css,'viewport thumb default cursor regression')
need('full 64 hexadecimal characters' in app and 'detail-report-id' in app and 'detail-overview-report-id' in app,'full report identity regression')
# Hero / row motion from 1.2.7 retained.
need('id="databaseHero"' in index and 'hero.dataset.workspace=state.view' in app and '.hero-v127{' in css,'workspace-aware hero regression')
need('.reports-table .click-row{--report-row-surface:transparent}' in css and '.reports-table .click-row:hover{--report-row-surface:#211416}' in css,'synchronous report-row motion regression')
# Data/transport invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need("databaseReleaseVersion:'1.2.8'" in worker and "workerReleaseVersion:'1.2.8'" in worker,'Worker release identity missing')
need('## Release 1.2.8 Compare fixed-follow reliability requirements' in rules,'1.2.8 rules section missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.compare-sticky-shell' in css,'fixed-follow reduced-motion coverage missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.8','releaseReady':False,'appAsset':'assets/app.v1208.js','cacheKey':'1208'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.8 Compare fixed-follow contract')
