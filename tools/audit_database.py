from __future__ import annotations
from pathlib import Path
import argparse, json, os, re, shutil, sqlite3, subprocess, sys
from urllib.parse import urlsplit

AUDIT_VERSION='1.0.20'
DB_VERSION='1.0.20'
APP_ASSET='app.v1020.js'
CACHE_KEY='1020'
PRODUCER='VulkanScope 1.0.19 · Vulkan 1.4.362'
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
    APP_ASSET,'encyclopedia.v03924.js','site.v0390.css','apple-touch-icon-v0311.png','favicon-v0311.ico','favicon-v0311.png','favicon.ico','favicon.png','vulkanscope_logo_horizontal.png',
    'gpu-vendors/gpu_vendor_amd.png','gpu-vendors/gpu_vendor_arm.png','gpu-vendors/gpu_vendor_broadcom.png','gpu-vendors/gpu_vendor_huawei.png','gpu-vendors/gpu_vendor_imagination.png','gpu-vendors/gpu_vendor_intel.png','gpu-vendors/gpu_vendor_nvidia.png','gpu-vendors/gpu_vendor_qualcomm.png','gpu-vendors/gpu_vendor_samsung.png','gpu-vendors/gpu_vendor_unknown.png','gpu-vendors/gpu_vendor_vivante.png','gpu-vendors/gpu_vendor_vsi.png',
    'hdr/dolby_vision.png','hdr/dolby_vision_2.png','hdr/hdr10.svg','hdr/hdr10_plus.png','hdr/hdr10_plus_advanced.png','hdr/hdr10_plus_v1014.png','hdr/hdr_vivid.webp'
}
ERROR_PAGES={'400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html'}
TOP_ALLOW={'.nojekyll','index.html','config.js','report.schema.json','assets','data',*ERROR_PAGES}
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
            if a not in ASSET_ALLOW: errors.append(f'unexpected/stale Pages asset {pos}')
        if f.is_file() and rel.parts and rel.parts[0]=='data' and f.suffix.lower()!='.json': errors.append(f'non-JSON Pages data {pos}')
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
    required=['index.html','config.js','report.schema.json',f'assets/{APP_ASSET}','assets/site.v0390.css','assets/encyclopedia.v03924.js','worker/src/index.js','worker/package.json','worker/wrangler.jsonc','worker/tests/contract.mjs','rules/PROJECT_RULES.md','tools/quality_gate.py','tools/repair_repository.py','tools/mark_release_ready.py','tools/verify_1_0_20_release_state_handshake.py','tools/pages.workflow.yml','.github/workflows/pages.yml','registry/registry_lock.json','registry/upstream/vk.xml']
    for rel in required: need((root/rel).is_file(),f'missing required source file {rel}')
    if errors:
        print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
    index=text('index.html'); app=text(f'assets/{APP_ASSET}'); css=text('assets/site.v0390.css'); worker=text('worker/src/index.js'); rules=text('rules/PROJECT_RULES.md'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
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
    need(f"const DATABASE_VERSION='{DB_VERSION}',LIVE_SYNC_INTERVAL_MS=10000,RELEASE_CHECK_INTERVAL_MS=10000;" in app,'frontend release/live-sync identity mismatch')
    need(pkg.get('version')==DB_VERSION,'Worker package version mismatch')
    need(static.get('databaseVersion')==DB_VERSION,'static index database version mismatch')
    need("databaseVersion:" not in worker,'legacy Worker databaseVersion refresh signal must be absent')
    need(worker.count("databaseReleaseVersion:'1.0.20'")>=2,'Worker databaseReleaseVersion mismatch')
    need(worker.count("workerReleaseVersion:'1.0.20'")>=2,'Worker workerReleaseVersion mismatch')
    need(worker.count("frontendUpdateSignal:'same-origin-pages-marker'")>=2,'Worker frontendUpdateSignal metadata missing')

    # Current Vulkan/producer metadata and immutable evidence model.
    for token in [SPEC,'VulkanScope producer/query baseline 1.4.362',PRODUCER,'VulkanScope 1.0.19+ · schema 2 / technical report 3']:
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

    # Requested 1.0.20 UI/release behavior and preserved evidence semantics.
    for token in ["classList.add('modal-page-size-select','drop-up')",'fill="#3DDC84"',"donutChart('GPU / reports',chartItems,rs.length,'',state.deviceSliceLimit)",'GPU / REPORT DISTRIBUTION','device-report-counts','modal-value-list modal-paged-list','coverage-report-list modal-paged-list','--coverage-position:${ratio*100}%']:
        need(token in app,f'current frontend contract missing: {token}')
    need('fill="#E2676A"' not in app,'legacy red Android tint remains')
    need('bottom:calc(100% + 7px)!important' in css and '.modal-page-size-select' in css,'modal page-size menu containment CSS missing')
    need('.modal-paged-list{min-height:0;max-height:min(52vh,520px);overflow-y:auto' in css,'bounded modal scrollbar missing')
    need("high=ratio>0&&(rank===true||rank==='dominant')?' high':''" in app,'dominant non-zero coverage glow semantics missing')
    need("const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');" in app,'raw GPU vendor-ID provenance changed')
    need("[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']" in app,'audited HDR10+ asset mapping changed')
    need('window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)' in app,'live report synchronization missing')
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
    need(versioned==[APP_ASSET],f'exactly one versioned frontend app is permitted: {versioned}')
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
        for rel in [f'assets/{APP_ASSET}','assets/encyclopedia.v03924.js','worker/src/index.js','worker/tests/contract.mjs']:
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
