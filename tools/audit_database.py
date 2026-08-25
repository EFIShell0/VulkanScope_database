from pathlib import Path
import json, subprocess, shutil, sys, re
from urllib.parse import urlsplit

root=Path(__file__).resolve().parents[1]
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
def text(path): return path.read_text(encoding='utf-8')

index=text(root/'index.html')
app=text(root/'assets/app.v0391.js')
css=text(root/'assets/site.v0390.css')
worker=text(root/'worker/src/index.js')
rules=text(root/'rules/PROJECT_RULES.md')
workflow=text(root/'.github/workflows/pages.yml')

# Release identity / cache busting
check('VulkanScope Database <strong>0.39.1</strong>' in index,'index version')
check('site.v0390.css' in index and 'app.v0391.js' in index and 'config.js?v=0391' in index,'0.39.1 cache-busted asset refs')
check('Database 0.39.1' in app,'frontend database version')
check('VulkanScope 0.41.5 · Vulkan 1.4.360' in app,'frontend producer baseline')
check("connect-src 'self' https://vulkanscope-database-api.vulkanscope.workers.dev" in index,'CSP API pin')
check('node --check assets/app.v0391.js' in workflow,'workflow frontend syntax check')

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
'Release 0.39.1 VulkanScope 0.41.5 compatibility hardening requirements']
for token in required_rules: check(token in rules,f'release rule {token}')
for rel in ['rules/0.37.0_VULKANSCOPE_0.41.0_TRENDS_PERMALINK_AUDIT.md','rules/0.37.1_QUEUE_VIDEO_QUERY_STATE_AUDIT.md','rules/0.38.0_STATISTICS_HASH_ROUTING_0.41.4_FULL_AUDIT.md','rules/0.39.0_FILTER_STATISTICS_FULL_AUDIT.md','rules/0.39.1_VULKANSCOPE_0.41.5_COMPATIBILITY_HARDENING.md']:
    check((root/rel).is_file(),f'audit document {rel}')

# Static metadata / toolchain
schema=json.loads(text(root/'report.schema.json'))
check('technicalReport' in schema.get('required',[]),'published schema requires technicalReport')
check(schema.get('properties',{}).get('technicalReport',{}).get('properties',{}).get('schemaVersion',{}).get('const')==3,'published schema technicalReport v3')
static=json.loads(text(root/'data/index.json'))
check(static.get('databaseVersion')=='0.39.1','static database version')
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
check(pkg.get('version')=='0.39.1','worker package version')
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
            target=root/clean[len('/VulkanScope_database/'):]
        else:
            target=(html.parent/clean).resolve()
        check(target.is_file(),f'broken local asset {html.name}: {ref}')
for name in ['400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html']:
    check('site.v0390.css' in text(root/name),f'{name} current stylesheet')

# Packaging hygiene
bad_names={'.DS_Store','Thumbs.db','local.properties'}
for f in root.rglob('*'):
    rel=f.relative_to(root)
    if any(part in {'.gradle','build','__pycache__','.idea','.git'} for part in rel.parts): errors.append(f'forbidden release artifact {rel}')
    if f.is_file() and (f.name in bad_names or f.suffix in {'.pyc','.pyo','.o','.so','.class'}): errors.append(f'forbidden release file {rel}')

# Syntax / contract tests
node=shutil.which('node')
if node:
    for f in [root/'assets/app.v0391.js',root/'worker/src/index.js',root/'worker/tests/contract.mjs']:
        r=subprocess.run([node,'--check',str(f)],capture_output=True,text=True)
        if r.returncode: errors.append(f'node-check {f.relative_to(root)}: {r.stderr.strip()}')
    r=subprocess.run([node,str(root/'tools/test_routes.mjs')],capture_output=True,text=True,cwd=root)
    if r.returncode: errors.append(f'route-contract: {r.stdout.strip()} {r.stderr.strip()}')
    r=subprocess.run([node,str(root/'worker/tests/contract.mjs')],capture_output=True,text=True,cwd=root/'worker')
    if r.returncode: errors.append(f'worker-contract: {r.stdout.strip()} {r.stderr.strip()}')

if errors:
    print('\n'.join(errors)); sys.exit(1)
print('VulkanScope Database 0.39.1 audit: PASS')
