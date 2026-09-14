from pathlib import Path
import argparse, json, re
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1302.js'); compat=text('assets/browser-compat.v1302.js'); boot=text('assets/release-bootstrap.v1302.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.2'" in app,'frontend identity missing')
for token in ['assets/app.v1302.js?v=1302','assets/browser-compat.v1302.js?v=1302','assets/release-bootstrap.v1302.js?v=1302','site.v0390.css?v=1302','config.js?v=1302','VulkanScope Database <strong>1.3.2</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Freshness must be persistent and generation-consistent, not one-shot.
for token in ["cache:'no-store'",'data/release.json','index.html','marker.appAsset','release-bootstrap.v${key}.js','browser-compat.v${key}.js','setInterval(()=>void check(),STEADY_RETRY)',"document.addEventListener('visibilitychange'","window.addEventListener('pageshow'","window.addEventListener('online'",'location.replace']:
    need(token in boot,f'convergence freshness token missing: {token}')
need("app.includes(`const DATABASE_VERSION='${remote}'`)" in boot and "bootJs.includes(`const LOCAL='${remote}'`)" in boot and "compatJs.includes('window.__VULKANSCOPE_BROWSER_INFO__')" in boot,'startup generation proof incomplete')
need("if(compareVersion(remote,DATABASE_VERSION)>0&&await publishedFrontendReady(marker))navigateToPublishedRelease(remote)" in app,'runtime newer-release check still requires manual refresh')
need("const navigateToPublishedRelease=remote=>" in app and "new URL('./index.html',location.href)" in app,'automatic cache-busted release navigation missing')
# Immediate immutable predecessor asset triplet is retained in staged artifact; older assets remain repair targets.
for token in ["'assets/app.v1301.js'","'assets/browser-compat.v1301.js'","'assets/release-bootstrap.v1301.js'","'assets/app.v1302.js'","'assets/browser-compat.v1302.js'","'assets/release-bootstrap.v1302.js'"]:
    need(token in build,f'Pages predecessor/current bridge asset missing: {token}')
need("PREDECESSOR_BRIDGE = {'app.v1301.js','browser-compat.v1301.js','release-bootstrap.v1301.js'}" in repair,'repository repair predecessor bridge missing')
# Filter/pointer behavior.
need("e.target.closest('.custom-select')" in app and "e.composedPath" in app and "closeCustomSelects()" in app,'document outside-click guard does not exempt custom-select internals')
need('.viewport-scrollbar.is-scrollable,.surface-scrollbar.is-scrollable{pointer-events:none!important}' in css,'blank scrollbar rail remains pointer-active')
need('.surface-scrollbar.is-scrollable>.viewport-scrollbar-arrow' in css and '.surface-scrollbar.is-scrollable>.viewport-scrollbar-track' in css and 'pointer-events:auto!important' in css,'intended scrollbar controls are not explicitly pointer-enabled')
need('grid-template-columns:36px minmax(0,1fr) 36px!important' in css,'filter Previous/Next pager is not compact width-safe')
need('.custom-select-page-button span{display:none!important}' in css,'filter Previous/Next text still forces narrow overflow')
need('.custom-select-pagination .page-jump{width:100%!important;min-width:0!important;max-width:124px!important' in css,'filter page-jump flex containment missing')
# Browser information is intentionally unchanged in this release; no logo bundle is introduced.
need(not (root/'assets/browser-logos').exists(),'out-of-scope browser-logo bundle was introduced')
need('BROWSER_LOGO_ASSETS' not in app and 'settings-browser-logo' not in app,'out-of-scope browser-logo rendering was introduced')
need("['Samsung Internet',/SamsungBrowser" in app,'1.3.1 browser identity presentation changed unexpectedly')
# Independence notice exact text, info icon, blue informational design.
notice='VulkanScope is not affiliated with the Khronos Group and is not an official Khronos Group project.'
need(notice in index and notice in app,'exact English Khronos independence notice missing')
need(index.count('independence-info-icon')>=1 and 'independence-info-icon' in app,'information icon missing from independence notice')
need('color:#b9d2ff!important' in css and 'rgba(62,126,238,.12)' in css,'independence notice is not blue informational styling')
need('rgba(255,92,102,.28)' in css,'historical red rule unexpectedly deleted instead of safely overridden')
# Existing semantics/floors unchanged.
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("databaseReleaseVersion:'1.3.2'" in worker and "workerReleaseVersion:'1.3.2'" in worker,'Worker release identity mismatch')
need('## Release 1.3.2 cache-convergence / pointer-integrity / pagination / information-notice requirements' in rules,'1.3.2 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_2_cache_pointer_browser_ui.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_2_cache_pointer_browser_ui_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.2','releaseReady':False,'appAsset':'assets/app.v1302.js','cacheKey':'1302'},'source release marker mismatch')
need('http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"' in index,'defensive HTML no-cache metadata missing')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.2 cache/pointer/pagination/information contract')
