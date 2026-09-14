from __future__ import annotations
from pathlib import Path
import argparse, json, os, re, shutil, sqlite3, subprocess, sys
from urllib.parse import urlsplit

AUDIT_VERSION='1.3.3'
DB_VERSION='1.3.3'
APP_ASSET='app.v1303.js'
CACHE_KEY='1303'
PRODUCER='VulkanScope 1.2.5 · Vulkan 1.4.362'
SPEC='Vulkan 1.4.362 (2026-09-04)'

parser=argparse.ArgumentParser(description='Audit VulkanScope Database source or staged Pages artifact')
parser.add_argument('--source-tree',type=Path)
parser.add_argument('--artifact-tree',type=Path)
parser.add_argument('--version',action='store_true')
parser.add_argument('--require-release-ready',action='store_true',help='Require the staged Pages release marker to be releaseReady=true')
args=parser.parse_args()
if args.version:
    print(f'VulkanScope Database audit tool {AUDIT_VERSION}')
    raise SystemExit(0)

ASSET_ALLOW={
    'app.v1302.js','browser-compat.v1302.js','release-bootstrap.v1302.js',APP_ASSET,'browser-compat.v1303.js','release-bootstrap.v1303.js','encyclopedia.v03924.js','site.v0390.css','apple-touch-icon-v0311.png','favicon-v0311.ico','favicon-v0311.png','favicon.ico','favicon.png','vulkanscope_logo_horizontal.png',
    'gpu-vendors/gpu_vendor_amd.png','gpu-vendors/gpu_vendor_arm.png','gpu-vendors/gpu_vendor_broadcom.png','gpu-vendors/gpu_vendor_huawei.png','gpu-vendors/gpu_vendor_imagination.png','gpu-vendors/gpu_vendor_intel.png','gpu-vendors/gpu_vendor_nvidia.png','gpu-vendors/gpu_vendor_qualcomm.png','gpu-vendors/gpu_vendor_samsung.png','gpu-vendors/gpu_vendor_unknown.png','gpu-vendors/gpu_vendor_vivante.png','gpu-vendors/gpu_vendor_vsi.png',
    'hdr/dolby_vision.png','hdr/dolby_vision_2.png','hdr/hdr10.svg','hdr/hdr10_plus.png','hdr/hdr10_plus_advanced.png','hdr/hdr10_plus_v1014.png','hdr/hdr_vivid.webp',
}
ERROR_PAGES={'400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html'}
TOP_ALLOW={'.nojekyll','index.html','config.js','report.schema.json','assets','data','licenses',*ERROR_PAGES}
HTML_REF=re.compile(r'''(?:href|src)=["']([^"']+)["']''',re.I)

def local_ref_errors(base:Path, html:Path, errors:list[str]):
    body=html.read_text(encoding='utf-8')
    for ref in HTML_REF.findall(body):
        if ref.startswith(('http://','https://','data:','#','mailto:','javascript:')): continue
        clean=urlsplit(ref).path
        if not clean or clean in {'.','./','/','/VulkanScope_database/'} or clean.endswith('/'): continue
        if clean.startswith('/VulkanScope_database/'):
            target=(base/clean[len('/VulkanScope_database/'):]).resolve()
        else:
            target=(html.parent/clean).resolve()
        try: target.relative_to(base.resolve())
        except ValueError:
            errors.append(f'local asset escapes root {html.name}: {ref}'); continue
        if not target.is_file(): errors.append(f'broken local asset {html.name}: {ref}')

def audit_artifact(root:Path,require_release_ready=False):
    root=root.resolve(); errors=[]
    if not root.is_dir(): raise SystemExit(f'artifact tree missing: {root}')
    actual={x.name for x in root.iterdir()}
    for x in sorted(actual-TOP_ALLOW): errors.append(f'forbidden Pages top-level entry {x}')
    for x in sorted(TOP_ALLOW-actual): errors.append(f'missing Pages entry {x}')
    forbidden={'.git','.github','worker','tools','rules','regression','registry','compat','node_modules','.wrangler','dist','build','__pycache__'}
    for f in root.rglob('*'):
        rel=f.relative_to(root); pos=rel.as_posix()
        if f.is_symlink(): errors.append(f'symlink not permitted {pos}')
        if any(part in forbidden for part in rel.parts): errors.append(f'forbidden Pages path {pos}')
        if pos!='.nojekyll' and any(part.startswith('.') for part in rel.parts): errors.append(f'forbidden hidden Pages path {pos}')
        if f.is_file() and rel.parts and rel.parts[0]=='assets':
            a=Path(*rel.parts[1:]).as_posix()
            if a not in ASSET_ALLOW and not re.fullmatch(r'country-flags/[a-z]{2}\.png',a): errors.append(f'unexpected/stale Pages asset {pos}')
        if f.is_file() and rel.parts and rel.parts[0]=='data' and f.suffix.lower()!='.json': errors.append(f'non-JSON Pages data {pos}')
        if f.is_file() and rel.parts and rel.parts[0]=='licenses' and (f.suffix.lower()!='.md' or f.name not in {'wrangler.md','sharp.md','esbuild.md','workerd.md','nodejs.md','python.md'}): errors.append(f'unexpected Pages license document {pos}')
    idx=(root/'index.html').read_text(encoding='utf-8')
    for token in [f'assets/{APP_ASSET}?v={CACHE_KEY}',f'site.v0390.css?v={CACHE_KEY}',f'config.js?v={CACHE_KEY}',f'VulkanScope Database <strong>{DB_VERSION}</strong>']:
        if token not in idx: errors.append(f'Pages current identity/reference missing: {token}')
    marker_path=root/'data/release.json'
    if not marker_path.is_file(): errors.append('Pages release marker missing')
    else:
        try: marker=json.loads(marker_path.read_text(encoding='utf-8'))
        except Exception as exc: errors.append(f'Pages release marker invalid JSON: {exc}'); marker={}
        expected={'schemaVersion':2,'databaseVersion':DB_VERSION,'appAsset':f'assets/{APP_ASSET}','cacheKey':CACHE_KEY}
        for key,value in expected.items():
            if marker.get(key)!=value: errors.append(f'Pages release marker {key} mismatch: {marker.get(key)!r} != {value!r}')
        if marker.get('releaseReady') is not bool(require_release_ready): errors.append(f'Pages releaseReady mismatch: {marker.get("releaseReady")!r} expected {bool(require_release_ready)!r}')
    for html in root.glob('*.html'): local_ref_errors(root,html,errors)
    if errors:
        print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
    print(f'VulkanScope Database {AUDIT_VERSION} Pages artifact audit: PASS ({root})')

def audit_source(root:Path):
    root=root.resolve(); errors=[]
    def need(cond,msg):
        if not cond: errors.append(msg)
    def text(rel): return (root/rel).read_text(encoding='utf-8')
    need(root.is_dir(),f'source tree missing: {root}')
    if not root.is_dir():
        print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
    required=['index.html','config.js','report.schema.json','assets/app.v1302.js','assets/browser-compat.v1302.js','assets/release-bootstrap.v1302.js',f'assets/{APP_ASSET}','assets/browser-compat.v1303.js','assets/release-bootstrap.v1303.js','assets/site.v0390.css','assets/encyclopedia.v03924.js','worker/src/index.js','worker/package.json','worker/wrangler.jsonc','worker/tests/contract.mjs','rules/PROJECT_RULES.md','tools/quality_gate.py','tools/repair_repository.py','tools/mark_release_ready.py','tools/verify_1_2_1_compare_temporal_detail.py','tools/verify_1_2_11_compare_mobile_identity.py','tools/test_1_2_11_compare_mobile_identity_negative_mutations.py','tools/verify_1_2_12_filter_search_overlay.py','tools/test_1_2_12_filter_search_overlay_negative_mutations.py','tools/verify_1_2_13_filter_pagination_compare_audit.py','tools/test_1_2_13_filter_pagination_compare_negative_mutations.py','tools/verify_1_2_14_page_jump_browser_info.py','tools/test_1_2_14_page_jump_browser_info_negative_mutations.py','tools/verify_1_3_2_cache_pointer_browser_ui.py','tools/test_1_3_2_cache_pointer_browser_ui_negative_mutations.py','rules/1.3.2_CACHE_POINTER_BROWSER_UI_AUDIT.md','tools/verify_1_3_3_compare_direction_symmetric_motion.py','tools/test_1_3_3_compare_direction_symmetric_motion_negative_mutations.py','rules/1.3.3_COMPARE_DIRECTION_SYMMETRIC_MOTION_AUDIT.md','tools/pages.workflow.yml','.github/workflows/pages.yml','registry/registry_lock.json','registry/upstream/vk.xml','licenses/wrangler.md','licenses/sharp.md','licenses/esbuild.md','licenses/workerd.md','licenses/nodejs.md','licenses/python.md']
    for rel in required: need((root/rel).is_file(),f'missing required source file {rel}')
    if errors:
        print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
    index=text('index.html'); app=text(f'assets/{APP_ASSET}'); compat=text('assets/browser-compat.v1303.js'); css=text('assets/site.v0390.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
    pkg=json.loads(text('worker/package.json')); schema=json.loads(text('report.schema.json')); static=json.loads(text('data/index.json')); lock=json.loads(text('registry/registry_lock.json')); wr=json.loads(text('worker/wrangler.jsonc'))

    # Release/cache identity and canonical workflow.
    need(workflow==workflow_template,'pages.yml differs from canonical tools/pages.workflow.yml')
    workflows=sorted(p.name for p in (root/'.github/workflows').glob('*') if p.is_file() and p.suffix.lower() in {'.yml','.yaml'})
    need(workflows==['pages.yml'],f'exactly one workflow is permitted: {workflows}')
    need(not (root/'README.md').exists(),'root README.md is forbidden in source release')
    need(not (root/'release.md').exists(),'root release.md is forbidden in source release')
    need(not (root/'fastlane').exists(),'Fastlane/store metadata is forbidden in source release')
    for token in [f'VulkanScope Database <strong>{DB_VERSION}</strong>',f'assets/{APP_ASSET}?v={CACHE_KEY}',f'site.v0390.css?v={CACHE_KEY}',f'config.js?v={CACHE_KEY}']:
        need(token in index,f'current index identity missing: {token}')
    need(f"const DATABASE_VERSION='{DB_VERSION}',LIVE_SYNC_INTERVAL_MS=3000,RELEASE_CHECK_INTERVAL_MS=10000" in app,'frontend release/live-sync identity mismatch')
    need('browser-compat.v1303.js?v=1303' in index and 'release-bootstrap.v1303.js?v=1303' in index and 'browserCompatibilityGate' in index,'browser compatibility/startup freshness references missing')
    need("chromium:84,firefox:86,safari:14.1" in compat and 'Element.prototype.getAnimations' in compat and 'window.ResizeObserver' in compat,'browser minimum/feature gate mismatch')
    boot=text('assets/release-bootstrap.v1303.js')
    notice='VulkanScope is not affiliated with the Khronos Group and is not an official Khronos Group project.'
    need(notice in index and notice in app,'English Khronos independence notice missing')
    need('VulkanScope projesinin Khronos Group' not in index+app,'non-English Khronos independence notice remains')
    need("go.disabled=max<=1||target===value" in app and "go.disabled=max<=1||!valid||target===currentPage()" in app,'page Go current-state disabling missing')
    need("pager.hidden=!searchable" in app and "scrollArea.className='custom-select-scroll'" in app,'filter pagination/scroll region contract missing')
    need('openLicenseViewer' in app and 'data-license-file' in app and 'license-viewer-dialog' in css,'inline license modal missing')
    need("cache:'no-store'" in boot and 'data/release.json' in boot and 'location.replace' in boot,'startup no-store release bootstrap missing')
    need('showNewReportNotification(result.added)' in app and '.new-report-toast{' in css,'new-report notification missing')
    need("$('#schemaFooter').textContent=`Database ${DATABASE_VERSION}" in app,'schema footer release identity is hard-coded/stale')
    need("const browserLanguage=()=> 'en-US'" in app and "new Intl.DisplayNames(['en'],{type:'region'})" in app,'English-only regional presentation contract missing')
    need("classList.toggle('at-page-top',atTop)" in app and "classList.toggle('at-page-bottom',atBottom)" in app,'native scrollbar endpoint state classes missing')
    need('html.at-page-top::-webkit-scrollbar-button' in css and 'html.at-page-bottom::-webkit-scrollbar-button' in css,'native scrollbar endpoint visual states missing')
    need('@media(max-width:430px)' in css and 'overflow-x:hidden' in css,'mobile overflow containment contract missing')
    need(pkg.get('version')==DB_VERSION,'Worker package version mismatch')
    need(static.get('databaseVersion')==DB_VERSION,'static index database version mismatch')
    need("databaseVersion:" not in worker,'legacy Worker databaseVersion refresh signal must be absent')
    need(worker.count("databaseReleaseVersion:'1.3.3'")>=3,'Worker databaseReleaseVersion mismatch')
    need(worker.count("workerReleaseVersion:'1.3.3'")>=3,'Worker workerReleaseVersion mismatch')
    need(worker.count("frontendUpdateSignal:'same-origin-pages-marker'")>=2,'Worker frontendUpdateSignal metadata missing')

    # Current Vulkan/producer metadata and immutable evidence model.
    for token in [SPEC,'VulkanScope producer/query baseline 1.4.362',PRODUCER,'VulkanScope 1.2.5+ · schema 2 / technical report 3']:
        need(token in worker,f'Worker metadata missing: {token}')
    need(static.get('publishedVulkanSpec')==SPEC,'static published Vulkan spec mismatch')
    need(static.get('producerQueryBaseline')==PRODUCER,'static producer baseline mismatch')
    need(lock.get('apiVersion')=='1.4.362','registry lock API version mismatch')
    need(lock.get('headerVersion')==362,'registry lock header version mismatch')
    need(lock.get('registeredVulkanExtensionCount')==476,'registry lock extension census mismatch')
    need(lock.get('publishedDate')=='2026-09-04','registry lock publication date mismatch')
    need(schema.get('properties',{}).get('technicalReport',{}).get('properties',{}).get('schemaVersion',{}).get('const')==3,'technicalReport schema v3 contract missing')
    need('technicalReport' in schema.get('required',[]),'technicalReport must remain required')
    need(static.get('normalizerVersion')==16,'normalizer version changed unexpectedly')

    # Retained connectivity/UI behavior plus preserved evidence semantics.
    for token in ["classList.add('modal-page-size-select','drop-up')",'fill="#3DDC84"',"donutChart('GPU / reports',chartItems,rs.length,'',state.deviceSliceLimit)",'GPU / REPORT DISTRIBUTION','device-report-counts','modal-value-list modal-paged-list','coverage-report-list modal-paged-list','--coverage-position:${ratio*100}%']:
        need(token in app,f'current frontend contract missing: {token}')
    need('fill="#E2676A"' not in app,'legacy red Android tint remains')
    need('bottom:calc(100% + 7px)!important' in css and '.modal-page-size-select' in css,'modal page-size menu containment CSS missing')
    need('.modal-paged-list{min-height:0;max-height:min(52vh,520px);overflow-y:auto' in css,'bounded modal scrollbar missing')
    need("high=ratio>0&&(rank===true||rank==='dominant')?' high':''" in app,'dominant non-zero coverage glow semantics missing')
    need("const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');" in app,'raw GPU vendor-ID provenance changed')
    need("[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']" in app,'audited HDR10+ asset mapping changed')
    need('window.setInterval(()=>void runLiveSync(false),LIVE_SYNC_INTERVAL_MS)' in app,'foreground live report synchronization timer missing')
    need("new URL(`${api}/v1/sync`)" in app and "fetchJsonBounded(u,{cache:'no-store',timeoutMs:NETWORK_PROBE_TIMEOUT_MS})" in app,'bounded no-store sync-head polling missing')
    need("if(!force&&head.syncToken===liveSyncToken)" in app,'sync-head unchanged-token shortcut missing')
    need("COUNT(*) OVER() AS report_count" in worker and "url.pathname==='/v1/sync'&&request.method==='GET'" in worker,'Worker sync-head endpoint/query missing')
    need("fetchJsonBounded(`./data/release.json?_=${Date.now()}`,{cache:'no-store'})" in app,'release-ready same-origin marker polling missing')
    need('releaseMarkerShapeValid' in app and 'publishedFrontendReady(marker)' in app,'published frontend readiness probe missing')
    need('UPDATE_RETRY_SUPPRESS_MS=120000' in app and 'sessionStorage.setItem(UPDATE_ATTEMPT_KEY' in app,'repeat-refresh loop suppression missing')
    need("html.includes(`./${asset}?v=${cacheKey}`)" in app and "js.includes(`const DATABASE_VERSION='${remote}'`)" in app,'release marker/index/app handshake verification missing')
    need('maybeShowDatabaseUpdate(meta)' not in app,'Worker databaseVersion must not trigger frontend refresh notices')
    need((root/'data/release.json').is_file(),'release marker source missing')
    if (root/'data/release.json').is_file():
        marker=json.loads(text('data/release.json'))
        need(marker=={'schemaVersion':2,'databaseVersion':DB_VERSION,'releaseReady':False,'appAsset':f'assets/{APP_ASSET}','cacheKey':CACHE_KEY},'source release marker must remain exact non-ready identity until deploy job')
    need('branches: ["main"]' in workflow and 'tags:' not in workflow,'production workflow must originate from main, not a tag ref')
    need('needs: [build, release]' in workflow,'Pages deployment must wait for both build and GitHub Release completion')
    need('python tools/mark_release_ready.py _site' in workflow,'deploy must mark only the staged artifact release-ready after Release success')
    need(workflow.find('  release:') < workflow.find('  deploy:'),'release job must precede deploy job')
    need('Create or refresh GitHub Release from validated main commit' in workflow,'main-commit GitHub Release step missing')
    need('Upload release-ready GitHub Pages artifact' in workflow and 'Deploy release-ready GitHub Pages artifact' in workflow,'release-ready upload/deploy steps missing')

    flag_dir=root/'assets/country-flags'
    flag_files=sorted(flag_dir.glob('*.png')) if flag_dir.is_dir() else []
    need(len(flag_files)==250,f'exactly 250 bundled country flag PNGs required, found {len(flag_files)}')
    need('countryFlagAsset' in app and 'assets/country-flags/${cc.toLowerCase()}.png' in app,'local country flag rendering path missing')
    need('networkInfoRefresh' not in index and 'networkInfoRefresh' not in app,'manual network refresh control must be removed')
    need('NETWORK_INFO_INTERVAL_MS=3000' in app and 'syncNetworkInfoAutoRefresh' in app,'automatic Internet-information refresh contract missing')
    need("},5000);renderNetworkInfo()" in app,'five-second restored banner interval missing')
    need("badge:''}};" in app and "restored:{title:'Connection restored'" in app,'restored banner must not expose Online badge text')
    need("liveSyncFailures++;markNetworkFailure(true)" in app,'first failed live-sync probe must surface API-unavailable state immediately')
    need("navigator.connection?.addEventListener?.('change',forceConnectivityRecheck)" in app,'connection-change reachability recheck missing')
    need('.encyclopedia-workspace' in css and '.surface-workspace' in css,'redesigned Encyclopedia/Surface workspace CSS missing')
    need('scrollbar-color:#684047 #100c0d' in css and '*::-webkit-scrollbar-thumb' in css,'site-wide design scrollbar contract missing')
    need("producerAtLeast1205" in worker and "VulkanScope 1.2.5 or newer is required for new submissions" in worker,'VulkanScope 1.2.5 POST floor missing')
    need("if(v.major===1)return p.application.versionCode===1000+v.minor*100+v.patch" in worker,'1.x producer versionCode identity mapping missing')
    need("new Intl.DisplayNames(['en'],{type:'region'})" in app and 'filter-country-flag' in app and 'country-custom-select' in css,'English full country selector with bundled flag icons missing')
    need('Updating connection observation…' not in app,'automatic Internet refresh must remain silent after initial observation')
    need('WORKSPACE_UI' in app and 'FILTER_FAMILIES' in app and 'workspace-context' in css and 'filter-family' in css,'non-Reports workspace/filter redesign contract missing')
    need('compare-producer-version' in app and '.compare-producer-version' in css,'Compare producer-version emphasis missing')
    need('settings-message-info' in css and 'settings-message-warning' in css and 'settingsMessageMarkup' in app,'Settings semantic info/warning callouts missing')
    need('pageJumpMarkup' in app and 'bindPageJump' in app and 'validPageJumpValue' in app,'direct page-jump primitive missing')
    need("pageJumpMarkup(1,1,'custom-select-page-jump')" in app and "pageJumpMarkup(state.reportPage,pages,'report-page-jump')" in app and "pageJumpMarkup(page,pages,'bounded-table-page-jump')" in app and "pageJumpMarkup(page,1,'modal-page-jump')" in app,'direct page jump missing from one or more pagination families')
    need('id="settingsBrowserTitle">Browser information</h3>' in index and 'id="browserInfo"' in index and 'function renderBrowserInfo()' in app,'Browser information Settings section missing')
    need('canvas.toDataURL' not in app and 'WEBGL_debug_renderer_info' not in app,'browser fingerprinting primitive forbidden')
    need(index.count('data-settings-category=')==4 and 'data-settings-category="information"' in index and 'data-settings-panel="information"' in index,'four-category Settings / Information surface missing')
    need('SETTINGS_DEPENDENCY_INVENTORY' in app and "{name:'Wrangler',version:'4.130.0',license:'MIT OR Apache-2.0'" in app and "{name:'sharp',version:'0.35.4',license:'Apache-2.0'" in app,'Information dependency/license inventory missing')
    need("{name:'esbuild',version:'Resolved by Wrangler 4.130.0'" in app and "{name:'workerd',version:'Resolved by Wrangler 4.130.0'" in app,'unpinned transitive tooling disclosure missing')
    need('id="downloadReportJson"' in app and 'downloadReportJson(r,downloadJson)' in app and '?compact=1&_download=${Date.now()}' in app,'stored-report JSON download action missing')
    need("type:'application/json;charset=utf-8'" in app and 'URL.createObjectURL(blob)' in app,'local JSON download serialization missing')
    need('/v1/export' not in worker and '/v1/reports/export' not in worker,'unexpected JSON export Worker endpoint added')

    # 1.3.3 Compare direction / symmetric motion contract.
    need("function setCompareMinimizeControl(toggle,minimized)" in app and "minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'" in app,'Compare state-specific chevron geometry missing')
    need('.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}' not in css,'Compare chevron is double-inverted by minimized CSS rotation')
    need('.compare-minimize-toggle svg{transform:none}' in css,'Compare chevron single-direction-source CSS guard missing')
    need('const animatePagedSurfaceIn=(host,direction=0)=>' in app and 'host.getAnimations?.().forEach' in app and "prefersReducedMotion()" in app,'shared reduced-motion-aware pagination motion primitive missing')
    need('animatePagedSurfaceIn(optionsHost,target>previousPage?1:-1)' in app,'custom-selector page transition missing')
    need('const renderPage=(direction=0)=>' in app and 'animatePagedSurfaceIn(list,direction)' in app,'bounded modal page transition missing')
    need('licenseViewerMotionToken' in app and "dialog.classList.add('open')" in app and "dialog.classList.remove('open')" in app and "backdrop?.classList.add('open')" in app and "backdrop?.classList.remove('open')" in app,'symmetric License viewer state motion missing')
    need('.license-viewer-dialog.open' in css and '.license-viewer-backdrop.open' in css,'License viewer open-state CSS missing')
    need('@media(prefers-reduced-motion:reduce){.license-viewer-backdrop,.license-viewer-dialog{transition:none!important}' in css,'License viewer reduced-motion override missing')
    need('## Release 1.3.3 Compare-direction / symmetric-motion requirements' in rules,'1.3.3 rules section missing')
    need("'assets/app.v1302.js'" in text('tools/build_pages_artifact.py') and "'assets/app.v1303.js'" in text('tools/build_pages_artifact.py'),'Pages immediate-predecessor/current app bridge mismatch')
    need("PREDECESSOR_BRIDGE = {'app.v1302.js','browser-compat.v1302.js','release-bootstrap.v1302.js'}" in text('tools/repair_repository.py'),'1.3.3 repository predecessor bridge mismatch')
    for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
        need(wf.count('python tools/verify_1_3_3_compare_direction_symmetric_motion.py')>=3,f'{name}: 1.3.3 verifier missing from release stages')
        need(wf.count('python tools/test_1_3_3_compare_direction_symmetric_motion_negative_mutations.py')>=3,f'{name}: 1.3.3 negative suite missing from release stages')

    # Browser/Worker security and resource ceilings.
    for token in ["default-src 'self'","connect-src 'self' https://vulkanscope-database-api.vulkanscope.workers.dev","object-src 'none'","base-uri 'none'","form-action 'none'","frame-ancestors 'none'"]:
        need(token in index,f'CSP directive missing: {token}')
    need('eval(' not in app and 'new Function(' not in app and 'document.write(' not in app,'unsafe dynamic frontend execution primitive present')
    for token in ['2*1024*1024','readBoundedBody',"new TextDecoder('utf-8',{fatal:true})",'hasSensitiveKey','stableStringify','cross-origin-resource-policy','cross-origin-opener-policy','content-security-policy']:
        need(token in worker,f'Worker security/resource control missing: {token}')
    need(pkg.get('devDependencies',{}).get('wrangler')=='4.130.0','Wrangler must remain pinned to audited 4.130.0')
    need((pkg.get('overrides') or {}).get('sharp')=='0.35.4','sharp must remain overridden to audited 0.35.4')
    need(pkg.get('scripts',{}).get('security:audit')=='node scripts/security-audit.mjs','security:audit script missing')
    sec=text('worker/scripts/security-audit.mjs')
    need("runNpm(['audit','--audit-level=high'])" in sec,'npm high-severity audit gate missing')
    need(wr.get('compatibility_date')=='2026-08-23','Worker compatibility date changed without audit')
    need(bool(wr.get('d1_databases')) and wr['d1_databases'][0].get('binding')=='DB','D1 binding missing')

    # CI/release safety and current full-audit wiring.
    for token in ['actions/checkout@v7','persist-credentials: false','actions/setup-python@v7','actions/setup-node@v7','actions/upload-pages-artifact@v4','actions/deploy-pages@v4','python tools/audit_database.py --source-tree .','python tools/audit_database.py --artifact-tree _site','python tools/quality_gate.py','python tools/repair_repository.py --apply','python tools/repair_repository.py --check']:
        need(token in workflow,f'workflow safety/gate missing: {token}')
    need('pages: write' not in workflow.split('  deploy:',1)[0],'pre-deploy jobs must not have Pages write permission')

    # Source/package hygiene and local-resource integrity.
    versioned=sorted(p.name for p in (root/'assets').glob('app.v*.js') if p.is_file())
    need(versioned==['app.v1302.js',APP_ASSET],f'exactly current + predecessor versioned frontend apps are permitted: {versioned}')
    forbidden_dirs={'.gradle','build','dist','__pycache__','.idea','node_modules','.wrangler','_site','.pytest_cache','.mypy_cache','.ruff_cache','coverage','.tmp','tmp'}
    bad_names={'.DS_Store','Thumbs.db','Desktop.ini','local.properties','.dev.vars','.env'}
    for current,dirs,names in os.walk(root,topdown=True,followlinks=False):
        cur=Path(current)
        if cur==root and '.git' in dirs: dirs.remove('.git')
        for d in list(dirs):
            rel=(cur/d).relative_to(root)
            if d in forbidden_dirs: errors.append(f'forbidden source directory {rel}')
            if (cur/d).is_symlink(): errors.append(f'symlink not permitted {rel}')
        for name in names:
            f=cur/name; rel=f.relative_to(root)
            if f.is_symlink(): errors.append(f'symlink not permitted {rel}')
            if name in bad_names or name.startswith('.dev.vars.') or (name.startswith('.env.') and name!='.env.example') or f.suffix.lower() in {'.pyc','.pyo','.o','.so','.class','.apk','.log','.tmp'}:
                errors.append(f'forbidden source file {rel}')
    for html in root.glob('*.html'): local_ref_errors(root,html,errors)

    # Syntax/crash-contract checks without generating pycache.
    for py in (root/'tools').glob('*.py'):
        try: compile(py.read_text(encoding='utf-8'),str(py),'exec')
        except Exception as exc: errors.append(f'Python syntax {py.name}: {exc}')
    node=shutil.which('node')
    if node:
        for rel in [f'assets/{APP_ASSET}','assets/browser-compat.v1303.js','assets/encyclopedia.v03924.js','worker/src/index.js','worker/tests/contract.mjs']:
            r=subprocess.run([node,'--check',str(root/rel)],capture_output=True,text=True)
            if r.returncode: errors.append(f'node --check {rel}: {r.stderr.strip()}')
        for rel,cwd in [('tools/test_routes.mjs',root),('tools/test_compare_contract.mjs',root),('worker/tests/contract.mjs',root/'worker')]:
            if (root/rel).is_file():
                r=subprocess.run([node,str(root/rel)],capture_output=True,text=True,cwd=cwd)
                if r.returncode: errors.append(f'{rel}: {r.stdout.strip()} {r.stderr.strip()}')
    try:
        con=sqlite3.connect(':memory:')
        for migration in sorted((root/'worker/migrations').glob('*.sql')): con.executescript(migration.read_text(encoding='utf-8'))
        need(bool(con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='report_payload_chunks'").fetchone()),'D1 payload chunk table missing after migration replay')
    except Exception as exc: errors.append(f'D1 migration replay failed: {exc}')

    if errors:
        print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
    print(f'VulkanScope Database {AUDIT_VERSION} source audit: PASS ({root})')

if args.artifact_tree:
    audit_artifact(args.artifact_tree,args.require_release_ready)
elif args.source_tree:
    audit_source(args.source_tree)
else:
    audit_source(Path(__file__).resolve().parents[1])
