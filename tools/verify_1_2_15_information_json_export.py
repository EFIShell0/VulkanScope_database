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
app=text('assets/app.v1215.js'); compat=text('assets/browser-compat.v1215.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); audit=text('rules/1.2.15_INFORMATION_JSON_EXPORT_AUDIT.md'); worker=text('worker/src/index.js'); package=text('worker/package.json'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml'); repair=text('tools/repair_repository.py'); build_index=text('tools/build_index.py')
# Release identity / immutable predecessor boundary.
need("const DATABASE_VERSION='1.2.15'" in app,'frontend 1.2.15 identity missing')
need('assets/app.v1215.js?v=1215' in index and 'browser-compat.v1215.js?v=1215' in index and 'site.v0390.css?v=1215' in index,'1.2.15 cache references missing')
need('VulkanScope Database <strong>1.2.15</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1214.js').exists() and not (root/'assets/browser-compat.v1214.js').exists(),'stale 1.2.14 browser-visible bundles remain')
need("CURRENT_APP = 'app.v1215.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1215.js'" in repair,'repair current asset identity missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor regression')
# Exactly four Settings category buttons/panels, including Information.
buttons=re.findall(r'data-settings-category="([^"]+)"',index)
panels=re.findall(r'data-settings-panel="([^"]+)"',index)
need(buttons==['internet','favorites','preferences','information'],f'Settings category order/count mismatch: {buttons}')
need(panels==['internet','favorites','preferences','information'],f'Settings panel order/count mismatch: {panels}')
need('data-settings-category="information"' in index and '<span>Information</span>' in index,'Information Settings tab missing')
need('data-settings-panel="information"' in index and 'id="settingsInformation"' in index,'Information Settings panel missing')
need("new Set(['internet','favorites','preferences','information'])" in app,'Information category not allowed by Settings state')
need("if(category==='information')renderSettingsInformation()" in app,'Information renderer not bound to Settings category')
need('function renderSettingsInformation()' in app and 'SETTINGS_DEPENDENCY_INVENTORY' in app,'Information dependency renderer missing')
# Inventory: direct pins, licenses and explicitly unpinned transitive/runtime identities.
for token,msg in [
    ("{name:'Wrangler',version:'4.130.0',license:'MIT OR Apache-2.0'",'Wrangler pin/license missing'),
    ("{name:'sharp',version:'0.35.4',license:'Apache-2.0'",'sharp pin/license missing'),
    ("{name:'esbuild',version:'Resolved by Wrangler 4.130.0',license:'MIT'",'esbuild unpinned/license disclosure missing'),
    ("{name:'workerd',version:'Resolved by Wrangler 4.130.0',license:'Apache-2.0'",'workerd unpinned/license disclosure missing'),
    ("{name:'Cloudflare D1',version:'Managed service'",'D1 runtime disclosure missing'),
    ("{name:'Web Platform APIs',version:'Browser-provided'",'Web Platform runtime disclosure missing'),
    ("{name:'Node.js standard library',version:'Runtime-provided'",'Node.js runtime disclosure missing'),
    ("{name:'Python standard library',version:'Python 3 runtime-provided'",'Python runtime disclosure missing'),
    ("0 third-party runtime libraries",'zero third-party frontend runtime statement missing'),
    ("does not commit a package-lock",'unpinned transitive-version disclosure missing')]: need(token in app,msg)
try:
    pkg=json.loads(package)
    need(pkg.get('version')=='1.2.15','worker package release mismatch')
    need(pkg.get('devDependencies',{}).get('wrangler')=='4.130.0','Wrangler direct pin mismatch')
    need(pkg.get('overrides',{}).get('sharp')=='0.35.4','sharp override mismatch')
    need(pkg.get('allowScripts',{}).get('esbuild') is True and pkg.get('allowScripts',{}).get('workerd') is True,'toolchain script allow-list mismatch')
except Exception as exc: errors.append(f'worker/package.json invalid: {exc}')
need(not (root/'worker/package-lock.json').exists(),'unexpected package-lock changes transitive-version truth model')
# JSON report export: existing read path only; local Blob download; no write/export endpoint.
need('id="downloadReportJson"' in app and '>Download JSON</span>' in app,'report Download JSON action missing')
need('async function downloadReportJson(r,button)' in app,'JSON download implementation missing')
need("/v1/reports/${encodeURIComponent(r.id)}?compact=1&_download=${Date.now()}" in app,'JSON download does not use canonical compact report GET')
need("new Blob([JSON.stringify(payload,null,2)+'\\n'],{type:'application/json;charset=utf-8'})" in app,'UTF-8 JSON Blob serialization missing')
need('URL.createObjectURL(blob)' in app and 'a.download=reportJsonFileName(r)' in app,'local browser download primitive missing')
need('downloadJson.onclick=()=>downloadReportJson(r,downloadJson)' in app,'Download JSON button not bound')
need("if(url.pathname.startsWith('/v1/reports/')&&request.method==='GET')" in worker and "url.searchParams.get('compact')==='1'" in worker,'existing Worker compact report GET changed/missing')
need('/v1/export' not in worker and '/v1/reports/export' not in worker,'export-specific Worker endpoint unexpectedly added')
# Existing action group remains present and JSON sits with them.
for token in ['id="shareReportLink"','id="copyReportLink"','id="downloadReportJson"']:
    need(token in app,f'report action missing: {token}')
# Responsive containment.
need('.settings-category-nav{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))' in css,'desktop four-column Settings category grid missing')
need('@media(max-width:430px){' in css and '.settings-category-nav{grid-template-columns:repeat(2,minmax(0,1fr))}' in css,'mobile 2x2 Settings category grid missing')
need('.settings-library-card{' in css and '.settings-library-license{' in css and 'overflow-wrap:anywhere' in css,'Information card/wrapping styles missing')
need('@media(max-width:760px)' in css and '.detail-actions{display:flex;flex-wrap:wrap;width:100%}' in css,'mobile detail-action wrapping missing')
need('.detail-action-button,.report-favorite-button.detail-action-button{flex:1 1 calc(50% - 2px)' in css,'mobile detail action sizing missing')
need('.detail-action-button.downloaded{' in css and '.detail-action-button.download-failed{' in css,'JSON action state styling missing')
# Security/frontend dependency invariant: no remote JS/font runtime introduced.
need("script-src 'self'" in index and "connect-src 'self' https://vulkanscope-database-api.vulkanscope.workers.dev" in index,'CSP script/connect boundary changed')
need(not re.search(r'<script[^>]+src=["\']https?://',index,re.I),'remote script introduced')
need('fonts.googleapis.com' not in index and 'fonts.gstatic.com' not in index,'remote font introduced')
# Existing key semantic contracts remain.
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'50-option selector page size changed')
need("validPageJumpValue=(value,max)=>" in app and 'n<=limit' in app,'bounded direct page jump regressed')
need("minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'" in app,'Compare arrow direction regressed')
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 producer floor missing')
need("databaseReleaseVersion:'1.2.15'" in worker and "workerReleaseVersion:'1.2.15'" in worker,'Worker release identity missing')
need('## Release 1.2.15 Information / report-JSON-export requirements' in rules,'1.2.15 rules section missing')
need('Sascha Willems' in audit and 'Vulkan Profile JSON' in audit,'reference/audit distinction missing')
need('"databaseVersion":"1.2.15"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_15_information_json_export.py')>=3,f'{name}: 1.2.15 verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_15_information_json_export_negative_mutations.py')>=3,f'{name}: 1.2.15 negative suite not used in Windows/build/release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.15','releaseReady':False,'appAsset':'assets/app.v1215.js','cacheKey':'1215'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.15 Information / report JSON export contract')
