from pathlib import Path
import argparse, json
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1304.js'); compat=text('assets/browser-compat.v1304.js'); boot=text('assets/release-bootstrap.v1304.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.4'" in app,'frontend identity missing')
for token in ['assets/app.v1304.js?v=1304','assets/browser-compat.v1304.js?v=1304','assets/release-bootstrap.v1304.js?v=1304','site.v0390.css?v=1304','config.js?v=1304','VulkanScope Database <strong>1.3.4</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Cache convergence remains mandatory.
for token in ["cache:'no-store'",'data/release.json','index.html','marker.appAsset','release-bootstrap.v${key}.js','browser-compat.v${key}.js','setInterval(()=>void check(),STEADY_RETRY)',"document.addEventListener('visibilitychange'","window.addEventListener('pageshow'","window.addEventListener('online'",'location.replace']:
    need(token in boot,f'convergence freshness token missing: {token}')
need("if(compareVersion(remote,DATABASE_VERSION)>0&&await publishedFrontendReady(marker))navigateToPublishedRelease(remote)" in app,'runtime newer-release auto-navigation missing')
# Filter rails must be gated by actual overflow state, not menu-open state.
need("scrollable=visible&&max>2" in app,'surface scrollbar overflow-state calculation missing')
need("rail.classList.toggle('is-scrollable',scrollable)" in app,'surface scrollbar is-scrollable state owner missing')
need("rail.setAttribute('aria-hidden',scrollable?'false':'true')" in app,'surface scrollbar ARIA state mismatch')
need('.custom-select.open .custom-select-menu>.surface-scrollbar:not(.is-scrollable){opacity:0!important;visibility:hidden!important;pointer-events:none!important}' in css,'non-scrollable open-filter rail hide rule missing')
need('.custom-select.open .custom-select-menu>.surface-scrollbar.is-scrollable{opacity:1;visibility:visible}' in css,'scrollable open-filter rail reveal rule missing')
need('.custom-select.open .custom-select-menu>.surface-scrollbar{opacity:1;visibility:visible}' not in css,'unconditional open-filter rail reveal remains')
# Compare direction requested by user: full/open Minimize = up, minimized/closed Expand = down.
need('function setCompareMinimizeControl(toggle,minimized)' in app,'Compare minimize state helper missing')
need("minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'" in app,'Compare chevron path semantics mismatch')
need("label.textContent=minimized?'Expand':'Minimize'" in app and "aria-expanded',minimized?'false':'true'" in app,'Compare label/ARIA state mismatch')
need('.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}' not in css,'Compare state CSS rotation must not own direction')
need('.compare-minimize-toggle svg{transform:none}' in css,'Compare SVG direction guard missing')
need("setCompareMinimizeControl(toggle,false)" in app,'Compare reset/unpin does not restore full/open state')
# Preserve 1.3.3 smooth transitions/reduced-motion contract.
for token in ['const animatePagedSurfaceIn=(host,direction=0)=>','prefersReducedMotion()','host.getAnimations?.().forEach','animatePagedSurfaceIn(optionsHost,target>previousPage?1:-1)','animatePagedSurfaceIn(list,direction)','let licenseViewerLastFocus=null,licenseViewerMotionToken=0']:
    need(token in app,f'1.3.3 motion regression: {token}')
need('@media(prefers-reduced-motion:reduce){.license-viewer-backdrop,.license-viewer-dialog{transition:none!important}' in css,'License reduced-motion override missing')
# Immediate predecessor bridge must be 1.3.3 only.
for token in ["'assets/app.v1303.js'","'assets/browser-compat.v1303.js'","'assets/release-bootstrap.v1303.js'","'assets/app.v1304.js'","'assets/browser-compat.v1304.js'","'assets/release-bootstrap.v1304.js'"]:
    need(token in build,f'Pages predecessor/current bridge asset missing: {token}')
need("'assets/app.v1302.js'" not in build and "'assets/browser-compat.v1302.js'" not in build and "'assets/release-bootstrap.v1302.js'" not in build,'stale 1.3.2 frontend triplet still staged')
need("PREDECESSOR_BRIDGE = {'app.v1303.js','browser-compat.v1303.js','release-bootstrap.v1303.js'}" in repair,'repository repair predecessor bridge mismatch')
# Existing floors and release identity remain intact.
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("databaseReleaseVersion:'1.3.4'" in worker and "workerReleaseVersion:'1.3.4'" in worker,'Worker release identity mismatch')
need('## Release 1.3.4 filter-scrollbar / Compare-chevron requirements' in rules,'1.3.4 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_4_filter_scrollbar_compare_chevron.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_4_filter_scrollbar_compare_chevron_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.4','releaseReady':False,'appAsset':'assets/app.v1304.js','cacheKey':'1304'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.4 filter scrollbar / Compare chevron contract')
