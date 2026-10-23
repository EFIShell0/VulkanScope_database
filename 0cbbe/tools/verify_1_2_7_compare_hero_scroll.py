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
app=text('assets/app.v1207.js'); compat=text('assets/browser-compat.v1207.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
# Release identity / CI freshness.
need("const DATABASE_VERSION='1.2.7'" in app,'frontend 1.2.7 identity missing')
need('assets/app.v1207.js?v=1207' in index and 'browser-compat.v1207.js?v=1207' in index and 'site.v0390.css?v=1207' in index,'1.2.7 cache references missing')
need('VulkanScope Database <strong>1.2.7</strong>' in index,'footer identity missing')
need('"databaseVersion":"1.2.7"' in text('data/release.json').replace(' ',''),'release marker version missing')
need('"databaseVersion":"1.2.7"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_7_compare_hero_scroll.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_7_compare_hero_scroll_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
    need('python tools/verify_1_2_6_cross_browser_detail.py' not in wf,f'{name}: stale 1.2.6 verifier remains in active CI')
    need('for attempt in 1 2 3 4 5' in wf and 'HTTP 429|HTTP 5[0-9][0-9]|rate limit|temporarily unavailable' in wf,f'{name}: bounded GitHub release retry missing')
# Browser floor / same-origin assets.
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors missing')
# Compare sticky shell + unclipped selectors.
need('id="compareStickyShell" class="compare-sticky-shell"' in app,'dedicated Compare sticky shell missing')
need("const shell=$('#compareStickyShell')" in app and "shell.style.setProperty('--compare-sticky-top'" in app and "shell.classList.toggle('is-pinned',pinned)" in app,'Compare sticky state is not synchronized to shell')
need('.compare-sticky-shell{position:sticky' in css and 'overflow:visible' in css,'Compare sticky shell positioning/overflow missing')
need('.compare-sticky-shell>.compare-workspace{position:relative!important' in css and 'overflow:visible!important' in css,'Compare workspace still owns sticky/clipping')
need("w.closest('.compare-report-card')?.classList.remove('select-open')" in app and "wrap.closest('.compare-report-card')?.classList.add('select-open')" in app,'Compare selector card elevation lifecycle missing')
need('.compare-report-card.select-open' in css and '.compare-report-card.select-open .custom-select-menu' in css,'Compare selector z-index presentation missing')
# Viewport rail endpoint semantics + default cursor.
for token in ['id="viewportScrollbar"','id="viewportScrollbarUp"','id="viewportScrollbarTrack"','id="viewportScrollbarThumb"','id="viewportScrollbarDown"']:
    need(token in index,f'viewport scrollbar markup missing: {token}')
need('scrolling?.clientHeight' in app and 'scrollHeight-viewport' in app and 'remaining=Math.max(0,max-y)' in app,'scrollingElement authoritative endpoint metrics missing')
need('atBottom=!scrollable||remaining<=2' in app and 'down.disabled=atBottom' in app,'bottom endpoint disabled-state synchronization missing')
need('.viewport-scrollbar.at-bottom .viewport-scrollbar-down,.viewport-scrollbar[data-endpoint="bottom"] .viewport-scrollbar-down,.viewport-scrollbar-down:disabled{color:#66636a!important;background:#0d0b0c!important;opacity:.72!important;filter:grayscale(1) saturate(0)!important;cursor:default!important}' in css,'bottom DOWN gray disabled state missing')
need('.viewport-scrollbar-down:not(:disabled){color:#ff5c66!important' in css,'available DOWN Vulkan-red state missing')
need('.viewport-scrollbar-thumb,.viewport-scrollbar-thumb:hover,.viewport-scrollbar.is-dragging .viewport-scrollbar-thumb{cursor:default!important}' in css,'viewport thumb default cursor contract missing')
need("thumb.addEventListener('pointerdown'" in app and "thumb.addEventListener('keydown'" in app,'viewport thumb lost drag/keyboard controls')
# Workspace-aware hero on every tab.
for token in ['id="databaseHero"','class="hero hero-v127"','id="heroWorkspaceEyebrow"','id="heroWorkspaceTitle"','id="heroWorkspaceDescription"','class="hero-command-deck"','id="globalSearch"','id="metrics"']:
    need(token in index,f'adaptive hero surface missing: {token}')
need("hero.dataset.workspace=state.view" in app and "heroKicker.textContent=`${m[0]} WORKSPACE`" in app and 'heroTitle.textContent=m[1]' in app and 'heroDescription.textContent=m[2]' in app,'active-tab META is not projected into hero')
need('.hero-v127{' in css and '.hero-workspace-card{' in css and '.hero-command-deck{' in css and '.hero-v127 .metrics{' in css,'hero redesign CSS missing')
need('.hero-v127[data-workspace="compare"]' in css and '.hero-v127[data-workspace="surface"]' in css,'workspace-aware hero visual states missing')
# Reports row synchronous motion.
need('.reports-table .click-row{--report-row-surface:transparent}' in css and '.reports-table .click-row>td{background-color:var(--report-row-surface)!important' in css,'row-wide hover surface contract missing')
need('.reports-table .click-row:hover{--report-row-surface:#211416}' in css and 'background-color .3s cubic-bezier(.2,.8,.2,1)' in css,'smooth reports hover transition missing')
need('.submitted-reveal' in css and '.submitted-stack' in css and 'transition:' in css,'Submitted/date-time motion coverage missing')
# Inherited detail identity and data invariants.
need('detail-back-button' in index and 'full 64 hexadecimal characters' in app and 'detail-report-id' in app and 'detail-overview-report-id' in app,'1.2.6 full report-detail identity regression')
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need("databaseReleaseVersion:'1.2.7'" in worker and "workerReleaseVersion:'1.2.7'" in worker,'Worker release identity missing')
need('## Release 1.2.7 compare follow-rail / adaptive hero / viewport endpoint requirements' in rules,'1.2.7 rules section missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.compare-sticky-shell' in css and '.hero-workspace-card' in css,'new surfaces reduced-motion coverage missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.7','releaseReady':False,'appAsset':'assets/app.v1207.js','cacheKey':'1207'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.7 compare/hero/viewport-scroll contract')
