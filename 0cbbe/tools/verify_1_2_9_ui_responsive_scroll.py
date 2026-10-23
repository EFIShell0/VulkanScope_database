from pathlib import Path
import argparse,json,re
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1209.js'); compat=text('assets/browser-compat.v1209.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml'); repair=text('tools/repair_repository.py')
# Release/cache identity and stale-asset prevention.
need("const DATABASE_VERSION='1.2.9'" in app,'frontend 1.2.9 identity missing')
need('assets/app.v1209.js?v=1209' in index and 'browser-compat.v1209.js?v=1209' in index and 'site.v0390.css?v=1209' in index,'1.2.9 cache references missing')
need('VulkanScope Database <strong>1.2.9</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1208.js').exists() and not (root/'assets/browser-compat.v1208.js').exists(),'stale predecessor browser assets remain in successor tree')
need("CURRENT_BROWSER_COMPAT = 'browser-compat.v1209.js'" in repair,'repository repair current browser-compat identity missing')
need('def stale_browser_compats()' in repair and 'for p in stale_browser_compats():' in repair,'repository repair does not remove stale versioned browser-compat assets from overlay checkouts')
need("compats=stale_browser_compats()" in repair and 'stale versioned browser-compat assets:' in repair,'repository repair check does not reject stale browser-compat assets')
need('"databaseVersion":"1.2.9"' in text('data/release.json').replace(' ',''),'release marker version missing')
need('"databaseVersion":"1.2.9"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_9_ui_responsive_scroll.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_9_ui_responsive_scroll_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
    need('python tools/verify_1_2_8_compare_fixed_follow.py' not in wf,f'{name}: stale 1.2.8 verifier remains in active CI')
# Compatibility gate: hidden by default, shown only after a real failed check.
need('<section id="browserCompatibilityGate" class="browser-compatibility-gate" role="main" hidden>' in index,'compatibility gate is not parse-time hidden')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors changed')
need("if(ok){if(gate)gate.hidden=true;if(app)app.hidden=false" in compat,'compatible branch no longer keeps warning hidden')
need("else{if(gate)gate.hidden=false;if(app)app.hidden=true" in compat,'incompatible branch no longer reveals warning')
# Reports filter parity and mobile width safety.
need("if(state.view==='encyclopedia')return;" in app and "if(state.view==='reports'||state.view==='encyclopedia')return;" not in app,'Reports still bypasses FILTER_FAMILIES grouping')
need('filter-family report-toolbar-family' in app and 'report-toolbar-control' in app,'Reports Sort/Per-page grouped design missing')
need('#contentView[data-main-view="reports"] #filters{display:flex' in css,'Reports filter-family layout missing')
need('@media(max-width:760px)' in css and '#contentView[data-main-view="reports"] #filters{display:grid;grid-template-columns:minmax(0,1fr)' in css,'Reports mobile single-column filter layout missing')
need('#contentView[data-main-view="reports"] .filter-family-controls>.custom-select' in css and 'min-width:0!important;width:100%;max-width:100%' in css,'Reports mobile enhanced-select width containment missing')
# Existing fixed-follow ownership plus new manual minimization.
for token in ['id="compareStickySentinel"','id="compareStickyPlaceholder" class="compare-sticky-placeholder"','id="compareStickyShell" class="compare-sticky-shell"','id="compareMiniBar" class="compare-mini-bar"','id="compareMiniA"','id="compareMiniB"','id="compareMinimizeToggle"']:
    need(token in app,f'Compare 1.2.9 markup missing: {token}')
need("shell.style.position='fixed'" in app and "placeholder.style.height=`${compareStickyFlowHeight}px`" in app,'1.2.8 explicit fixed-follow contract regressed')
need("workspace.classList.remove('is-compact','is-minimized')" in app,'return-to-top minimized-state reset missing')
need("workspace.classList.toggle('is-minimized')" in app and "miniA.textContent=a.gpu?.name||'Unknown'" in app and "miniB.textContent=b.gpu?.name||'Unknown'" in app,'Compare mini strip is not derived from authoritative selected reports')
need('maxWidth=Math.max(1,viewportWidth-left-rightReserve)' in app and 'width=Math.max(1,Math.min(Math.round(pageRect.width),maxWidth))' in app,'Compare mobile width clamp missing')
need('maxWidth=Math.max(260' not in app and 'width=Math.max(260' not in app,'old 260px Compare pinned minimum remains')
need('.compare-sticky-shell.is-pinned .compare-minimize-dock' in css and '.compare-workspace.is-minimized .compare-mini-bar' in css and '.compare-mini-divider' in css,'Compare minimize presentation CSS missing')
need('.compare-workspace.is-compact:not(.is-minimized) .compare-report-grid{grid-template-columns:minmax(0,1fr)!important' in css,'Compare compact mobile overflow fix missing')
# In-panel scroll rails use the same visual classes and real host scroll state.
need("const SURFACE_SCROLL_SELECTOR='.settings-drawer-body,.custom-select-menu,.coverage-report-dialog-body,.modal-paged-list'" in app,'required local scrollbar surfaces missing')
for token in ['function enhanceSurfaceScrollbar(host)','const surfaceScrollMetrics=host=>','host?.clientHeight','host?.scrollHeight','host?.scrollTop','surfaceScrollbarRailMarkup','viewport-scrollbar-arrow viewport-scrollbar-up surface-scrollbar-up','viewport-scrollbar-track surface-scrollbar-track','viewport-scrollbar-thumb surface-scrollbar-thumb']:
    need(token in app,f'local scrollbar contract missing: {token}')
need("host.scrollTop=Math.max(0,Math.min(drag.max,next))" in app,'local draggable thumb does not drive authoritative host scrollTop')
need("else if(e.key==='PageUp')" in app and "else if(e.key==='End')target=m.max" in app,'local scrollbar keyboard paging/home-end missing')
need('const surfaceScrollObserver=new MutationObserver' in app and 'window.addEventListener(\'resize\',queueAllSurfaceScrollbars' in app,'shared dynamic scrollbar synchronization missing')
need('.surface-scrollbar{position:absolute' in css and 'background:#100c0d;border-left:1px solid #2d1b1e' in css,'local rail viewport-style surface missing')
need('.surface-scroll-host{scrollbar-width:none!important' in css,'native duplicate local scrollbar not hidden after enhancement')
need('.custom-select:not(.open)>.surface-scrollbar' in css,'closed listbox rail visibility guard missing')
# Motion/accessibility and immutable data/transport invariants.
need('@media(prefers-reduced-motion:reduce)' in css and '.surface-scrollbar' in css and '.compare-minimize-toggle' in css,'1.2.9 reduced-motion coverage missing')
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need("databaseReleaseVersion:'1.2.9'" in worker and "workerReleaseVersion:'1.2.9'" in worker,'Worker release identity missing')
need('## Release 1.2.9 browser-gate / Reports filters / Compare minimization / local-scrollbar requirements' in rules,'1.2.9 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.9','releaseReady':False,'appAsset':'assets/app.v1209.js','cacheKey':'1209'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.9 UI/responsive/scroll contract')
