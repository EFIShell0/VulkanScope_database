from pathlib import Path
import argparse, json, subprocess, shutil, sys, re, os
from urllib.parse import urlsplit


parser=argparse.ArgumentParser(description="Audit VulkanScope Database source or staged Pages artifact")
parser.add_argument("--source-tree", type=Path, help="Audit a source checkout tree; top-level .git metadata is allowed and never traversed")
parser.add_argument("--artifact-tree", type=Path, help="Audit only a staged/deployable Pages artifact tree")
parser.add_argument("--version", action="store_true", help="Print the audit tool/database version and exit")
args=parser.parse_args()
AUDIT_VERSION="0.39.4"
if args.version:
    print(f"VulkanScope Database audit tool {AUDIT_VERSION}")
    sys.exit(0)
print(f"VulkanScope Database audit tool {AUDIT_VERSION}")

def audit_artifact_tree(artifact_root: Path):
    artifact_root=artifact_root.resolve()
    artifact_errors=[]
    def acheck(cond,msg):
        if not cond: artifact_errors.append(msg)
    acheck(artifact_root.is_dir(), f'artifact tree missing: {artifact_root}')
    if not artifact_root.is_dir():
        print("\n".join(artifact_errors)); sys.exit(1)
    allowed_top={'.nojekyll','index.html','config.js','report.schema.json','assets','data','400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html'}
    actual_top={x.name for x in artifact_root.iterdir()}
    for extra in sorted(actual_top-allowed_top): artifact_errors.append(f'forbidden Pages artifact top-level entry {extra}')
    allowed_assets={
        'app.v0394.js','site.v0390.css','apple-touch-icon-v0311.png','favicon-v0311.ico','favicon-v0311.png',
        'favicon.ico','favicon.png','vulkanscope_logo_horizontal.png',
        'gpu-vendors/gpu_vendor_amd.png','gpu-vendors/gpu_vendor_arm.png','gpu-vendors/gpu_vendor_broadcom.png',
        'gpu-vendors/gpu_vendor_huawei.png','gpu-vendors/gpu_vendor_imagination.png','gpu-vendors/gpu_vendor_intel.png',
        'gpu-vendors/gpu_vendor_nvidia.png','gpu-vendors/gpu_vendor_qualcomm.png','gpu-vendors/gpu_vendor_samsung.png',
        'gpu-vendors/gpu_vendor_unknown.png','gpu-vendors/gpu_vendor_vivante.png','gpu-vendors/gpu_vendor_vsi.png',
        'hdr/dolby_vision.png','hdr/dolby_vision_2.png','hdr/hdr10.svg','hdr/hdr10_plus.png',
        'hdr/hdr10_plus_advanced.png','hdr/hdr_vivid.webp'
    }
    for required in ['index.html','config.js','report.schema.json','assets','data','.nojekyll']:
        acheck((artifact_root/required).exists(), f'missing Pages artifact entry {required}')
    forbidden_dirs={'.git','.github','worker','tools','rules','.gradle','build','__pycache__','.idea','node_modules','.wrangler'}
    bad_names={'.DS_Store','Thumbs.db','local.properties'}
    for f in artifact_root.rglob('*'):
        rel=f.relative_to(artifact_root)
        if any(part in forbidden_dirs for part in rel.parts): artifact_errors.append(f'forbidden Pages artifact {rel}')
        if rel.as_posix()!='.nojekyll' and any(part.startswith('.') for part in rel.parts): artifact_errors.append(f'forbidden hidden Pages artifact {rel}')
        if f.is_symlink(): artifact_errors.append(f'symlink not permitted in Pages artifact {rel}')
        if f.is_file() and (f.name in bad_names or f.suffix in {'.pyc','.pyo','.o','.so','.class'}): artifact_errors.append(f'forbidden Pages artifact file {rel}')
        if f.is_file() and rel.parts and rel.parts[0]=='data' and f.suffix.lower()!='.json': artifact_errors.append(f'non-JSON file not permitted in Pages data {rel}')
        if f.is_file() and rel.parts and rel.parts[0]=='assets' and f.suffix.lower() not in {'.js','.css','.png','.jpg','.jpeg','.webp','.svg','.ico'}: artifact_errors.append(f'unexpected Pages asset type {rel}')
        if f.is_file() and rel.parts and rel.parts[0]=='assets':
            asset_rel=Path(*rel.parts[1:]).as_posix()
            if asset_rel not in allowed_assets: artifact_errors.append(f'unexpected/stale Pages asset {rel}')
    idx=artifact_root/'index.html'
    if idx.is_file():
        body=idx.read_text(encoding='utf-8')
        acheck('app.v0394.js' in body and 'config.js?v=0394' in body and 'site.v0390.css' in body,'Pages artifact current asset references')
    attr=re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']",re.I)
    for html in artifact_root.glob('*.html'):
        body=html.read_text(encoding='utf-8')
        for ref in attr.findall(body):
            if ref.startswith(('http://','https://','data:','#','mailto:','javascript:')): continue
            clean=urlsplit(ref).path
            if not clean or clean in {'.','./','/','/VulkanScope_database/'} or clean.endswith('/'): continue
            if clean.startswith('/VulkanScope_database/'):
                target=(artifact_root/clean[len('/VulkanScope_database/'):]).resolve()
            else:
                target=(html.parent/clean).resolve()
            try:
                target.relative_to(artifact_root)
                contained=True
            except ValueError:
                contained=False
            acheck(contained,f'Pages artifact local asset escapes artifact root {html.name}: {ref}')
            if contained: acheck(target.is_file(),f'broken Pages artifact local asset {html.name}: {ref}')
    if artifact_errors:
        print("\n".join(artifact_errors)); sys.exit(1)
    print('VulkanScope Database 0.39.4 Pages artifact audit: PASS')
    sys.exit(0)

if args.artifact_tree:
    audit_artifact_tree(args.artifact_tree)

default_root=Path(__file__).resolve().parents[1]
root=(args.source_tree if args.source_tree is not None else default_root).resolve()
if not root.is_dir():
    print(f'source tree missing: {root}')
    sys.exit(1)
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
def text(path): return path.read_text(encoding='utf-8')

index=text(root/'index.html')
app=text(root/'assets/app.v0394.js')
css=text(root/'assets/site.v0390.css')
worker=text(root/'worker/src/index.js')
rules=text(root/'rules/PROJECT_RULES.md')
workflow=text(root/'.github/workflows/pages.yml')
workflow_template=text(root/'tools/pages.workflow.yml')
workflow_dir=root/'.github/workflows'
workflow_files=sorted(p.name for p in workflow_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.yml','.yaml'}) if workflow_dir.is_dir() else []
check_workflows_pending=True

check(workflow_files==['pages.yml'],f'exactly one GitHub Actions workflow is permitted; remove stale workflows: {workflow_files}')
check(workflow==workflow_template,'pages.yml must exactly match tools/pages.workflow.yml; run python tools/repair_repository.py --apply')
# Release identity / cache busting
check('VulkanScope Database <strong>0.39.4</strong>' in index,'index version')
check('site.v0390.css' in index and 'app.v0394.js' in index and 'config.js?v=0394' in index,'0.39.4 cache-busted asset refs')
check('Database 0.39.4' in app,'frontend database version')
check('VulkanScope 0.41.5 · Vulkan 1.4.360' in app,'frontend producer baseline')
check("connect-src 'self' https://vulkanscope-database-api.vulkanscope.workers.dev" in index,'CSP API pin')
check('node --check assets/app.v0394.js' in workflow,'workflow frontend syntax check')
check('actions/checkout@v7' in workflow and 'persist-credentials: false' in workflow,'workflow current checkout and credential hardening')
check('actions/setup-python@v7' in workflow,'workflow current setup-python')
check('actions/configure-pages@v6' in workflow,'workflow current configure-pages')
check('actions/upload-pages-artifact@v5' in workflow and 'include-hidden-files: true' in workflow,'workflow current Pages upload and .nojekyll preservation')
check('actions/deploy-pages@v5' in workflow,'workflow current deploy-pages')
check('python tools/audit_database.py --version' in workflow and 'python tools/repair_repository.py --check' in workflow,'workflow exposes audit/repair fingerprints')
check('python tools/audit_database.py --source-tree .' in workflow,'workflow explicit source-tree audit')
build_workflow=workflow.split('  deploy:',1)[0]
deploy_workflow=workflow.split('  deploy:',1)[1] if '  deploy:' in workflow else ''
check('pages: write' not in build_workflow and 'id-token: write' not in build_workflow,'build job uses read-only token permissions')
check('pages: write' in deploy_workflow and 'id-token: write' in deploy_workflow,'deploy job owns Pages/id-token write permissions')
check('actions/configure-pages@v6' in deploy_workflow,'configure-pages runs only in deploy job')

check('python tools/test_audit_hygiene.py' in workflow,'workflow audit-mode regression test')
check('python tools/build_pages_artifact.py _site' in workflow,'workflow stages allow-listed Pages artifact')
check('python tools/audit_database.py --artifact-tree _site' in workflow,'workflow audits staged Pages artifact')
check('path: _site' in workflow,'workflow uploads staged Pages artifact only')

# Existing end-to-end data semantics
check('fetchJsonBounded' in app and '20000' in app and '4194304' in app,'bounded frontend API reads')
check('seenCursors' in app and 'Math.min(4,queue.length)' in app,'cursor/concurrency bounds')
check('v.detailedProperties=d.detailedProperties.map' in app and 'v.limits=d.limits.map' in app,'structured property/limit authority')
check("aggregateEntryLists(r=>r.detailedProperties||[]" in app,'properties aggregate separated')
check("aggregateEntryLists(r=>r.limits||[])" in app,'limits aggregate separated')
check("Properties (${(r.detailedProperties||[]).length})" in app,'detail property count separated')
check("Limits (${(r.limits||[]).length})" in app,'detail limit count separated')
check('canonicalMask(q.flags,QUEUE_FLAG_BITS)' not in app,'queue zero flags must not use generic VK_NONE')
for token in ['canonicalQueueFlags','VK_VIDEO_CODEC_OPERATION_NONE_KHR','videoCodecQueryStatus','videoCodecQueryReason','queryDiagnostics','Runtime query status','Device extension enumeration','Extended feature/property query','Vulkan 1.4 query','queryBadge','QUERY AVAILABLE','Property state describes query availability']:
    check(token in app,f'queue/query semantics {token}')

# 0.38 routing contract
route_tokens=[
    'DETAIL_TABS=new Set', 'DETAIL_ROUTE_SEGMENTS', 'DETAIL_ROUTE_LOOKUP',
    'routeReportHash=', '`#reports/${id}/', 'routeCompareUrl=', 'applyHashRoute()',
    'applyLegacyQueryRoute()', 'applyInitialRoute()', 'handleRouteEvent()', "head==='reports'&&(parts.length===2||parts.length===3)", "requested=parts[2]", "tab=requested===undefined?'overview':DETAIL_ROUTE_LOOKUP",
    "window.addEventListener('hashchange',handleRouteEvent)",
    "window.addEventListener('popstate',handleRouteEvent)",
    "trends:'statistics'", "statistics:'trends'", 'history[push?', 'syncRouteUrl(true)'
]
for token in route_tokens: check(token in app,f'hash routing {token}')
check('const VALID_REPORT_ID=/^[a-f0-9]{64}$/;' in app,'lowercase 64-hex route id validation')
check("const DETAIL_TABS=new Set(['overview','registry','properties','limits','features','formats','memory','queues','surface','display','extensions','instance','profiles','raw'])" in app,'report detail allow-list')
check("new URLSearchParams(location.search)" in app and "q.get('report')" in app and "q.get('compare')" in app,'legacy query migration parser')
check('`${location.origin}${location.pathname}${routeReportHash(id,tab)}`' in app,'generated report permalink uses canonical hash')
check('`${location.origin}${location.pathname}${routeCompareHash(ids)}`' in app or '#compare/' in app,'generated compare permalink uses hash')

# Statistics / chart semantics
for token in ['Filtered-submission statistics','Filtered-submission share','donutChart','compactDistribution','distribution-grid','donut-chart','Other']:
    check(token in app or token in css,f'statistics chart {token}')
check('market share' in app.lower(),'statistics market-share disclaimer')
check('Extension enumeration ranking' in app and 'statisticsExtensionNamespace' in app and 'statisticsExtensionMinShare' in app,'extension frequency remains ranked and filterable')
check('<svg' in app and 'role="img"' in app,'local accessible SVG donut chart')
# No runtime third-party chart/analytics dependencies.
for bad in ['chart.js','highcharts','google-analytics','googletagmanager','cdn.jsdelivr.net','unpkg.com']:
    check(bad not in app.lower() and bad not in index.lower(),f'no third-party runtime dependency {bad}')

# 0.39 view-scoped filters / interactive distributions
for token in ['driverVersionFilter','extensionFilter','deviceModelFilter','submissionAgeFilter','FILTER_APPLICABILITY','viewSpecificFilterActive','clearVisibleFilters']:
    check(token in app,f'cohort filter architecture {token}')
# Display/HDR must remain free from GPU/vendor/Vulkan API/driver filters.
filter_matrix=app.split('const FILTER_APPLICABILITY={',1)[1] if 'const FILTER_APPLICABILITY={' in app else ''
display_match=re.search(r"display:\[(.*?)\]",filter_matrix,re.S)
check(bool(display_match),'display filter matrix present')
if display_match:
    display_filters=display_match.group(1)
    for forbidden in ['vendorFilter','gpuFilter','apiFilter','loaderApiFilter','driverModeFilter','driverVersionFilter','extensionFilter','deviceTypeFilter','abiFilter','appVersionFilter','statusFilter']:
        check(forbidden not in display_filters,f'Display/HDR excludes irrelevant filter {forbidden}')
    for required in ['androidFilter','deviceModelFilter','submissionAgeFilter','hdrStateFilter','hdrTypeFilter','wideGamutFilter','preferredWideGamutFilter','resolutionFilter','refreshRateFilter','displayModeFilter','displayOrderFilter']:
        check(required in display_filters,f'Display/HDR relevant filter {required}')
# Properties/Limits are query-state views, not feature-support views.
check("properties:[['available','Query available'],['unavailable','Query unavailable'],['unknown','Unknown / not reported']]" in app,'properties query-state filter only')
check("limits:[['available','Query available'],['unavailable','Query unavailable'],['unknown','Unknown / not reported']]" in app,'limits query-state filter only')
check("table(['Section','Property','Query available','Query unavailable','Unknown'" in app,'properties table removes support columns')
check("table(['Section','Limit','Query available','Query unavailable','Unknown'" in app,'limits table removes support columns')
check('const hasFormatEvidence=' in app and "!['unknown','not reported','not queried','unavailable'].includes(x)" in app,'format zero mask remains explicit evidence')
check('const formatFieldState=' in app and "if(requiredFlag)return known.some" in app,'format selected-bit support uses exact bit evidence')
check('state.formatFlag&&supported===0' in app,'format feature-bit filter excludes rows with no positive selected-bit evidence')
for token in ['propertyVariation','limitVariation','featureCoverage','formatFlag','formatCoverage','memoryFlag','queueFamily','queueFlag','queuePresentation','queueVideoState','queueVideoCodec','queueMinCount','surfaceValue','extensionNamespace','extensionCoverage','instanceNamespace','profileRevision','profileCoverage','compareSection','compareFieldSearch']:
    check(token in app,f'view-specific filter {token}')
check("state.view==='queues'&&state.queueGroup==='all'" in app,'queue generic state hidden until capability selected')
check("state.view==='surface'&&state.surfaceGroup==='all'" in app,'surface generic state hidden until subgroup selected')
for token in ['data-chart-filter','donut-interactive','statisticsSliceLimit','statisticsExtensionScope','statisticsExtensionNamespace','statisticsExtensionMinShare','statisticsExtensionSearch','Other (']:
    check(token in app or token in css,f'interactive statistics {token}')
check('aria-pressed' in app and 'target.value=String(target.value)===String(value)' in app,'donut active-state and click-again-to-clear behavior')
check('.donut-interactive.is-selected' in css and '.chart-filter-button.is-selected' in css,'donut selected-state styling')
check('market share' in app.lower() and 'Extension membership overlaps' in app,'statistics semantic disclaimer')
check('third-party chart runtime' not in app.lower() or 'no third-party chart runtime' in app.lower(),'statistics local chart wording')


# Clear-filters and Display/HDR search isolation contract.
for token in [
    "if(view==='reports'){state.reportSort='submitted-desc'",
    "if(view==='properties'){state.propertyGroup='all'",
    "if(view==='features'){state.featureGroup='all'",
    "if(view==='formats'){state.formatGroup='all'",
    "if(view==='memory'){state.memoryGroup='types'",
    "if(view==='queues'){state.queueGroup='all'",
    "if(view==='surface'){state.surfaceGroup='all'",
    "if(view==='instance'){state.instanceGroup='all'",
    "if(v==='properties')return state.propertyGroup!=='all'",
    "if(v==='features')return state.featureGroup!=='all'",
    "if(v==='formats')return state.formatGroup!=='all'",
    "if(v==='memory')return state.memoryGroup!=='types'",
]:
    check(token in app,f'clear-filters default grouping {token}')
check("state.reportSort=sort.value;resetReportPage();setHeader();renderReports()" in app,'Reports sort updates Clear filters visibility')
check('displaySearchCache' in app and "const viewSearchText=r=>state.view==='display'?displaySearchText(r):reportSearchText(r)" in app,'Display/HDR global search uses display/device evidence only')
check("Search display/device evidence: model, HDR, color space, mode" in app,'Display/HDR view-aware search guidance')

# Worker current producer / security contract
check('normalizerVersion:15' in worker,'normalizer version 15')
check('detailedProperties=[],limits=[]' in worker,'worker separate fallback arrays')
check('tr?.schemaVersion===3&&d' in worker,'worker structured override')
check("publishedVulkanSpec:'Vulkan 1.4.360 (2026-08-14)'" in worker,'published spec metadata')
check('VulkanScope producer/query baseline 1.4.360' in worker,'producer registry metadata')
check('VulkanScope 0.41.5 · Vulkan 1.4.360' in worker,'current producer metadata')
for token in ['producerVersion=p=>','supportedProducer=p=>','producerAtLeast0414=p=>','currentProducerIdentity=p=>','validSecurityPatch=p=>','applicationAbiConsistent=p=>',"p.application.version!=='0.41.5'||p.application.versionCode===415",'validCurrentQueueSemantics=p=>','validCurrentQueryDiagnostics=p=>']:
    check(token in worker,f'producer contract {token}')
check('producerAtLeast0414(p)' in worker,'0.41.4+ semantics range helper is used')
check("if(!producerAtLeast0414(p))return true" in worker,'strict query/queue semantics apply to 0.41.4+ producers')
check("['available','unavailable','not_applicable','unknown']" in worker,'current queue status allow-list')
check("['available','incomplete','unavailable','not_applicable','unknown']" in worker,'current runtime-query status allow-list')
check('q.videoCodecOperations!==null||q.videoCodecOperationsU64!==null' in worker,'non-available queue numeric fields fail closed')
check('cross-origin-resource-policy' in worker and 'cross-origin-opener-policy' in worker and 'content-security-policy' in worker,'API response security headers')
check("'clientip'" in worker and 'normalizedKey' in worker and 'hasSensitiveKey' in worker,'privacy key filter')
check('2*1024*1024' in worker and 'readBoundedBody' in worker,'streaming request-body bound')

# Rules and audit docs
required_rules=[
'Release 0.35.9 Display & HDR / ABI / home-metric parity',
'Release 0.36.0 luminance-unit typography parity',
'Release 0.36.2 VulkanScope 0.34.2 complete-report parity',
'Release 0.36.3 technical-differences compare filter',
'Release 0.37.0 VulkanScope 0.41.0 trends and permalink requirements',
'Release 0.37.1 queue, Vulkan Video and query-state semantics',
'Release 0.38.0 statistics / hash routing / VulkanScope 0.41.4 requirements',
'Release 0.39.0 filter architecture and interactive statistics requirements',
'Release 0.39.1 VulkanScope 0.41.5 compatibility hardening requirements',
'Release 0.39.2 CI checkout and Pages artifact hygiene requirements',
'Release 0.39.3 GitHub Actions / source-audit hardening requirements',
'Release 0.39.4 tracked-source audit / repository repair requirements']
for token in required_rules: check(token in rules,f'release rule {token}')
for rel in ['rules/0.37.0_VULKANSCOPE_0.41.0_TRENDS_PERMALINK_AUDIT.md','rules/0.37.1_QUEUE_VIDEO_QUERY_STATE_AUDIT.md','rules/0.38.0_STATISTICS_HASH_ROUTING_0.41.4_FULL_AUDIT.md','rules/0.39.0_FILTER_STATISTICS_FULL_AUDIT.md','rules/0.39.1_VULKANSCOPE_0.41.5_COMPATIBILITY_HARDENING.md','rules/0.39.2_CI_PAGES_ARTIFACT_HYGIENE.md','rules/0.39.3_GITHUB_ACTIONS_SOURCE_AUDIT_HARDENING.md','rules/0.39.4_TRACKED_SOURCE_AUDIT_REPOSITORY_REPAIR.md']:
    check((root/rel).is_file(),f'audit document {rel}')

# Static metadata / toolchain
schema=json.loads(text(root/'report.schema.json'))
check('technicalReport' in schema.get('required',[]),'published schema requires technicalReport')
check(schema.get('properties',{}).get('technicalReport',{}).get('properties',{}).get('schemaVersion',{}).get('const')==3,'published schema technicalReport v3')
static=json.loads(text(root/'data/index.json'))
check(static.get('databaseVersion')=='0.39.4','static database version')
check(static.get('normalizerVersion')==15,'static normalizer')
check(static.get('producerQueryBaseline')=='VulkanScope 0.41.5 · Vulkan 1.4.360','static producer baseline')
wr=json.loads(text(root/'worker/wrangler.jsonc'))
check(wr.get('compatibility_date')=='2026-08-23','worker deployment-verified compatibility date')
check(wr.get('account_id')=='ccf3de9d3f2a4394af2fb7be7fd5bbf4','Cloudflare account pin')
dbs=wr.get('d1_databases',[])
check(bool(dbs) and dbs[0].get('binding')=='DB' and dbs[0].get('database_id')=='8fa65ef5-701d-4110-993d-87381f9763ab','D1 pin')
check(wr.get('observability',{}).get('enabled') is True,'Cloudflare observability enabled')
check(wr.get('observability',{}).get('logs',{}).get('head_sampling_rate')==0.1,'Cloudflare log sampling')
check(wr.get('observability',{}).get('traces',{}).get('head_sampling_rate')==0.01,'Cloudflare trace sampling')
pkg=json.loads(text(root/'worker/package.json'))
check(pkg.get('version')=='0.39.4','worker package version')
check(pkg.get('devDependencies',{}).get('wrangler')=='4.125.0','Wrangler pin')
for key in ['predeploy','premigrate','premigrations:list','pred1:count']:
    check('verify:account' in pkg.get('scripts',{}).get(key,''),f'account guard {key}')

# Broken same-package local HTML resources, including static error pages.
attr=re.compile(r'''(?:href|src)=["']([^"']+)["']''',re.I)
for html in list(root.glob('*.html')):
    body=text(html)
    for ref in attr.findall(body):
        if ref.startswith(('http://','https://','data:','#','mailto:','javascript:')): continue
        clean=urlsplit(ref).path
        if not clean or clean in {'.','./','/','/VulkanScope_database/'} or clean.endswith('/'): continue
        if clean.startswith('/VulkanScope_database/'):
            target=(root/clean[len('/VulkanScope_database/'):]).resolve()
        else:
            target=(html.parent/clean).resolve()
        try:
            target.relative_to(root)
            contained=True
        except ValueError:
            contained=False
        check(contained,f'local asset escapes source root {html.name}: {ref}')
        if contained: check(target.is_file(),f'broken local asset {html.name}: {ref}')
for name in ['400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html']:
    check('site.v0390.css' in text(root/name),f'{name} current stylesheet')

# Packaging hygiene. GitHub checkout metadata is never audited as release content.
# In a real Git checkout, use Git's tracked-file manifest rather than walking the filesystem.
# This makes root/.git structurally unreachable to the source-artifact audit.
source_forbidden_dirs={'.gradle','build','dist','__pycache__','.idea','node_modules','.wrangler','_site','.pytest_cache','.mypy_cache','.ruff_cache','coverage','.tmp','tmp'}
bad_names={'.DS_Store','Thumbs.db','Desktop.ini','local.properties'}
def secret_name(name):
    return name=='.dev.vars' or name.startswith('.dev.vars.') or name=='.env' or (name.startswith('.env.') and name!='.env.example')
def validate_source_rel(rel: Path):
    name=rel.name
    if '.git' in rel.parts or any(part in source_forbidden_dirs for part in rel.parts):
        errors.append(f'forbidden tracked source artifact {rel}')
    if name in bad_names or secret_name(name) or rel.suffix.lower() in {'.pyc','.pyo','.o','.so','.class','.zip','.7z','.rar','.tar','.gz','.apk','.log','.tmp'}:
        errors.append(f'forbidden tracked source file {rel}')

git=shutil.which('git')
git_meta=root/'.git'
if git_meta.is_symlink():
    errors.append('symlink not permitted for source checkout .git metadata')
used_git_manifest=False
if git and git_meta.exists() and not git_meta.is_symlink():
    r=subprocess.run([git,'-C',str(root),'ls-files','-z'],capture_output=True)
    if r.returncode==0:
        used_git_manifest=True
        for raw in r.stdout.split(b'\0'):
            if not raw: continue
            try: rel=Path(raw.decode('utf-8'))
            except UnicodeDecodeError:
                errors.append('tracked source path is not valid UTF-8')
                continue
            f=root/rel
            if f.is_symlink(): errors.append(f'symlink not permitted in tracked source tree {rel}')
            validate_source_rel(rel)
if not used_git_manifest:
    # Release-ZIP/local fallback: filesystem traversal with root VCS metadata pruned before descent.
    for current, dirs, names in os.walk(root, topdown=True, followlinks=False):
        cur=Path(current)
        if cur==root and '.git' in dirs: dirs.remove('.git')
        for d in list(dirs):
            path=cur/d; rel=path.relative_to(root)
            if path.is_symlink(): errors.append(f'symlink not permitted in source tree {rel}')
            validate_source_rel(rel)
        for name in names:
            f=cur/name; rel=f.relative_to(root)
            if cur==root and name=='.git' and not f.is_symlink(): continue
            if f.is_symlink(): errors.append(f'symlink not permitted in source tree {rel}')
            validate_source_rel(rel)

# Critical update files must be unique/canonical, because archive extraction does not delete stale files.
versioned_apps=sorted(p.name for p in (root/'assets').glob('app.v*.js') if p.is_file())
check(versioned_apps==['app.v0394.js'],f'exactly one versioned frontend app asset is permitted; run repository repair: {versioned_apps}')
check((root/'tools/repair_repository.py').is_file(),'repository repair tool present')
check((root/'tools/pages.workflow.yml').is_file(),'canonical workflow template present')

# Syntax / contract tests
node=shutil.which('node')
if node:
    for f in [root/'assets/app.v0394.js',root/'worker/src/index.js',root/'worker/tests/contract.mjs']:
        r=subprocess.run([node,'--check',str(f)],capture_output=True,text=True)
        if r.returncode: errors.append(f'node-check {f.relative_to(root)}: {r.stderr.strip()}')
    r=subprocess.run([node,str(root/'tools/test_routes.mjs')],capture_output=True,text=True,cwd=root)
    if r.returncode: errors.append(f'route-contract: {r.stdout.strip()} {r.stderr.strip()}')
    r=subprocess.run([node,str(root/'worker/tests/contract.mjs')],capture_output=True,text=True,cwd=root/'worker')
    if r.returncode: errors.append(f'worker-contract: {r.stdout.strip()} {r.stderr.strip()}')

if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'VulkanScope Database {AUDIT_VERSION} source audit: PASS ({root})')
