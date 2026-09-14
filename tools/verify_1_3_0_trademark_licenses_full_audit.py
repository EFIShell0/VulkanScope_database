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
app=text('assets/app.v1300.js'); compat=text('assets/browser-compat.v1300.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); audit=text('rules/1.3.0_TRADEMARK_LICENSES_FULL_AUDIT.md'); worker=text('worker/src/index.js'); package=text('worker/package.json'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml'); repair=text('tools/repair_repository.py'); build_index=text('tools/build_index.py'); build_pages=text('tools/build_pages_artifact.py'); source_audit=text('tools/audit_database.py')
# Release identity / cache boundary.
need("const DATABASE_VERSION='1.3.0'" in app,'frontend 1.3.0 identity missing')
need('assets/app.v1300.js?v=1300' in index and 'browser-compat.v1300.js?v=1300' in index and 'site.v0390.css?v=1300' in index and 'config.js?v=1300' in index,'1.3.0 cache references missing')
need('VulkanScope Database <strong>1.3.0</strong>' in index,'footer release identity missing')
need(not (root/'assets/app.v1215.js').exists() and not (root/'assets/browser-compat.v1215.js').exists(),'stale 1.2.15 browser-visible bundles remain')
need("CURRENT_APP = 'app.v1300.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1300.js'" in repair,'repair current asset identity missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor regression')
# Vulkan® presentation is display-only and must preserve canonical/raw evidence.
need("const VULKAN_TRADEMARK_RE=/\\bVulkan\\b(?!®)/g" in app,'standalone Vulkan trademark presentation regex missing')
need("replace(VULKAN_TRADEMARK_RE,'Vulkan®')" in app,'Vulkan® presentation replacement missing')
need('function initVulkanTrademark()' in app and 'new MutationObserver(' in app and 'initVulkanTrademark();enhanceSelects()' in app,'dynamic trademark presentation observer not initialized')
need("closest?.('pre,code,script,style,textarea,.raw,[data-preserve-vulkan-canonical=\"true\"]')" in app,'canonical/raw Vulkan preservation boundary missing')
need(not re.search(r'\bVulkan\b(?!®)',index),'static HTML still contains unregistered standalone Vulkan presentation')
notice='VulkanScope projesinin Khronos Group ile hiçbir ilgisi yoktur, resmi Khronos Group projesi değildir'
need(index.count(notice)==1,'footer Khronos independence notice missing/duplicated')
need(app.count(notice)==1,'Information Khronos independence notice missing/duplicated')
need('khronos-independence-notice' in css and 'color:var(--accent)' in css,'red Khronos independence styling missing')
need('footer-brand-stack' in index and '.footer-brand-stack{' in css and '.footer-independence-notice{' in css,'footer notice layout/containment missing')
# Information inventory + local Markdown license reading.
need(index.count('data-settings-category=')==4 and 'data-settings-category="information"' in index,'Information Settings category missing')
need('SETTINGS_DEPENDENCY_INVENTORY' in app and 'function renderSettingsInformation()' in app,'Information dependency renderer missing')
license_docs={
 'wrangler.md':['MIT OR Apache-2.0','github.com/cloudflare/workers-sdk'],
 'sharp.md':['Apache','github.com/lovell/sharp'],
 'esbuild.md':['MIT License','github.com/evanw/esbuild'],
 'workerd.md':['Apache','github.com/cloudflare/workerd'],
 'nodejs.md':['Node.js','github.com/nodejs/node'],
 'python.md':['Python','github.com/python/cpython'],
}
for name,tokens in license_docs.items():
    body=text('licenses/'+name)
    need(len(body)>300,f'license Markdown unexpectedly short: {name}')
    for token in tokens: need(token in body,f'license Markdown provenance/content missing {token!r}: {name}')
for comp,file_name in [('Wrangler','wrangler.md'),('sharp','sharp.md'),('esbuild','esbuild.md'),('workerd','workerd.md'),('Node.js standard library','nodejs.md'),('Python standard library','python.md')]:
    need(f"licenseFile:'./licenses/{file_name}'" in app,f'{comp} local Markdown license action missing')
need('Read license (.md)' in app and 'target="_blank" rel="noopener noreferrer"' in app,'license-reading action security/label missing')
need('.settings-library-actions{' in css and '.settings-license-read{' in css and '@media(max-width:760px)' in css and '.settings-license-read{width:100%}' in css,'license action responsive styling missing')
need("license_files=['wrangler.md','sharp.md','esbuild.md','workerd.md','nodejs.md','python.md']" in build_pages,'Pages license allow-list/copy missing')
need("'licenses'" in source_audit and "rel.parts[0]=='licenses'" in source_audit,'Pages/source audit does not validate licenses directory')
# Inventory truthfulness: exact pins only when repository pins them.
for token,msg in [
 ("{name:'Wrangler',version:'4.130.0',license:'MIT OR Apache-2.0'",'Wrangler pin/license missing'),
 ("{name:'sharp',version:'0.35.4',license:'Apache-2.0'",'sharp pin/license missing'),
 ("{name:'esbuild',version:'Resolved by Wrangler 4.130.0',license:'MIT'",'esbuild transitive disclosure missing'),
 ("{name:'workerd',version:'Resolved by Wrangler 4.130.0',license:'Apache-2.0'",'workerd transitive disclosure missing'),
 ("does not commit a package-lock",'unpinned transitive truth disclosure missing')]: need(token in app,msg)
try:
    pkg=json.loads(package)
    need(pkg.get('version')=='1.3.0','worker package release mismatch')
    need(pkg.get('devDependencies',{}).get('wrangler')=='4.130.0','Wrangler direct pin mismatch')
    need(pkg.get('overrides',{}).get('sharp')=='0.35.4','sharp override mismatch')
except Exception as exc: errors.append(f'worker/package.json invalid: {exc}')
need(not (root/'worker/package-lock.json').exists(),'unexpected package-lock changes transitive-version truth model')
# Prior UI behavior preserved: JSON export, 50-option selector paging, bounded page jump, Compare and Settings layers, Browser info.
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'50-option selector page size changed')
need('optionPages=Math.max(1,Math.ceil(matches.length/CUSTOM_SELECT_OPTION_LIMIT))' in app and 'matches.slice(start,start+CUSTOM_SELECT_OPTION_LIMIT)' in app,'selector 50-option pagination regressed')
need('validPageJumpValue=(value,max)=>' in app and 'n<=limit' in app,'bounded direct page jump regressed')
need("minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'" in app,'Compare arrow direction regressed')
need('.compare-sticky-shell.has-select-open .compare-minimize-dock{opacity:0!important' in css,'Compare/listbox collision protection regressed')
need('function setSettingsOpen(open){settingsOpen=!!open;if(settingsOpen)closeCustomSelects();' in app,'Settings/listbox close contract regressed')
need('.settings-backdrop{z-index:600;backdrop-filter:blur(8px)' in css,'Settings blur/layer contract regressed')
need('id="settingsBrowserTitle">Browser information</h3>' in index and 'function renderBrowserInfo()' in app,'Browser information regression')
need('canvas.toDataURL' not in app and 'WEBGL_debug_renderer_info' not in app,'forbidden browser fingerprinting primitive introduced')
need('id="downloadReportJson"' in app and '?compact=1&_download=${Date.now()}' in app and "type:'application/json;charset=utf-8'" in app,'report JSON export regression')
need('/v1/export' not in worker and '/v1/reports/export' not in worker,'unexpected export Worker endpoint')
# Transport/data semantics stay untouched except release identity.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 producer floor missing')
need(worker.count("databaseReleaseVersion:'1.3.0'")>=3 and worker.count("workerReleaseVersion:'1.3.0'")>=3,'Worker release identity missing')
need(len(list((root/'worker/migrations').glob('*.sql')))==3,'unexpected D1 migration added/removed')
need('## Release 1.3.0 Vulkan® presentation / license-reading / full-audit requirements' in rules,'1.3.0 rules section missing')
need('immutable predecessor' in audit.lower() and 'full audit' in audit.lower(),'1.3.0 audit record incomplete')
need('"databaseVersion":"1.3.0"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_3_0_trademark_licenses_full_audit.py')>=3,f'{name}: 1.3.0 verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_3_0_trademark_licenses_full_audit_negative_mutations.py')>=3,f'{name}: 1.3.0 negative suite not used in Windows/build/release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.0','releaseReady':False,'appAsset':'assets/app.v1300.js','cacheKey':'1300'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.0 Vulkan® / licenses / full-audit contract')
