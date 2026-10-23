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
app=text('assets/app.v1303.js'); compat=text('assets/browser-compat.v1303.js'); boot=text('assets/release-bootstrap.v1303.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.3'" in app,'frontend identity missing')
for token in ['assets/app.v1303.js?v=1303','assets/browser-compat.v1303.js?v=1303','assets/release-bootstrap.v1303.js?v=1303','site.v0390.css?v=1303','config.js?v=1303','VulkanScope Database <strong>1.3.3</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Cache-convergence behavior remains mandatory.
for token in ["cache:'no-store'",'data/release.json','index.html','marker.appAsset','release-bootstrap.v${key}.js','browser-compat.v${key}.js','setInterval(()=>void check(),STEADY_RETRY)',"document.addEventListener('visibilitychange'","window.addEventListener('pageshow'","window.addEventListener('online'",'location.replace']:
    need(token in boot,f'convergence freshness token missing: {token}')
need("if(compareVersion(remote,DATABASE_VERSION)>0&&await publishedFrontendReady(marker))navigateToPublishedRelease(remote)" in app,'runtime newer-release auto-navigation missing')
# Compare direction: JS geometry is the single source; no state CSS rotation may double-invert it.
need('function setCompareMinimizeControl(toggle,minimized)' in app,'Compare minimize state helper missing')
need("minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'" in app,'Compare chevron path direction mismatch')
need("label.textContent=minimized?'Expand':'Minimize'" in app and "aria-expanded',minimized?'false':'true'" in app,'Compare label/ARIA state mismatch')
need('.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}' not in css,'Compare chevron double inversion remains in CSS')
need('.compare-minimize-toggle svg{transform:none}' in css,'Compare chevron CSS single-source guard missing')
need("setCompareMinimizeControl(toggle,false)" in app,'Compare reset/unpin does not restore full-state chevron')
# Shared page motion is compositor-only, state-after-commit and reduced-motion aware.
need('const animatePagedSurfaceIn=(host,direction=0)=>' in app,'shared page-motion helper missing')
for token in ['prefersReducedMotion()','host.getAnimations?.().forEach','opacity:.28','translate3d(${dx}px,0,0)',"transform:'translate3d(0,0,0)'",'duration:155']:
    need(token in app,f'page-motion contract missing: {token}')
need('const previousPage=optionPage;optionPage=target;renderOptions({resetScroll:true});animatePagedSurfaceIn(optionsHost,target>previousPage?1:-1)' in app,'custom-select page transition is not state-after-render/direction-aware')
need('const renderPage=(direction=0)=>' in app and 'animatePagedSurfaceIn(list,direction)' in app,'bounded modal pagination motion missing')
need('const direction=target>page?1:target<page?-1:0;page=target;renderPage(direction)' in app,'modal direct page jump is not direction-aware')
# License viewer symmetric open/close with stale completion guard.
for token in ['let licenseViewerLastFocus=null,licenseViewerMotionToken=0',"const token=++licenseViewerMotionToken", "dialog.classList.remove('open')", "backdrop?.classList.remove('open')", 'if(token!==licenseViewerMotionToken', 'setTimeout(finish,230)']:
    need(token in app,f'License viewer symmetric motion token missing: {token}')
need(app.count("dialog.classList.add('open')")>=2 and app.count("backdrop?.classList.add('open')")>=2,'License viewer open motion must cover reduced and animated paths')
need("if(token!==licenseViewerMotionToken||dialog.classList.contains('open'))return" in app,'License viewer stale-close completion guard missing')
for token in ['.license-viewer-backdrop.open{opacity:1;visibility:visible;pointer-events:auto', '.license-viewer-dialog.open{opacity:1;visibility:visible;pointer-events:auto', 'translate(-50%,calc(-50% + 10px)) scale(.985)', 'translate(-50%,-50%) scale(1)']:
    need(token in css,f'License viewer CSS transition state missing: {token}')
need('@media(prefers-reduced-motion:reduce){.license-viewer-backdrop,.license-viewer-dialog{transition:none!important}' in css,'License viewer reduced-motion override missing')
# Immediate predecessor 1.3.2 remains staged; older 1.3.1 bridge must not be staged/current.
for token in ["'assets/app.v1302.js'","'assets/browser-compat.v1302.js'","'assets/release-bootstrap.v1302.js'","'assets/app.v1303.js'","'assets/browser-compat.v1303.js'","'assets/release-bootstrap.v1303.js'"]:
    need(token in build,f'Pages predecessor/current bridge asset missing: {token}')
need("'assets/app.v1301.js'" not in build and "'assets/browser-compat.v1301.js'" not in build and "'assets/release-bootstrap.v1301.js'" not in build,'stale 1.3.1 frontend triplet still staged')
need("PREDECESSOR_BRIDGE = {'app.v1302.js','browser-compat.v1302.js','release-bootstrap.v1302.js'}" in repair,'repository repair predecessor bridge mismatch')
# Existing non-motion semantics/floors remain intact.
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("databaseReleaseVersion:'1.3.3'" in worker and "workerReleaseVersion:'1.3.3'" in worker,'Worker release identity mismatch')
need('## Release 1.3.3 Compare-direction / symmetric-motion requirements' in rules,'1.3.3 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_3_compare_direction_symmetric_motion.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_3_compare_direction_symmetric_motion_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.3','releaseReady':False,'appAsset':'assets/app.v1303.js','cacheKey':'1303'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.3 Compare direction / symmetric motion contract')
