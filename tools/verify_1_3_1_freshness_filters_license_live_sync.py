from pathlib import Path
import argparse,json
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1301.js'); compat=text('assets/browser-compat.v1301.js'); boot=text('assets/release-bootstrap.v1301.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.1'" in app,'frontend identity missing')
for token in ['assets/app.v1301.js?v=1301','assets/browser-compat.v1301.js?v=1301','assets/release-bootstrap.v1301.js?v=1301','site.v0390.css?v=1301','config.js?v=1301','VulkanScope Database <strong>1.3.1</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
notice='VulkanScope is not affiliated with the Khronos Group and is not an official Khronos Group project.'
need(notice in index and notice in app,'English Khronos independence notice missing')
need('VulkanScope projesinin Khronos Group' not in index+app,'Turkish independence notice remains in current UI')
need("go.disabled=max<=1||target===value" in app and "go.disabled=max<=1||!valid||target===currentPage()" in app,'Go-current-page disabled contract missing')
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app and "pager.hidden=!searchable" in app,'all searchable filters do not retain 50-option pagination controls')
need("scrollArea.className='custom-select-scroll'" in app and 'scrollArea.append(optionsHost,status);menu.append(scrollArea,pager)' in app,'filter menu regions are not separated')
need('.custom-select-menu.is-searchable{display:grid;grid-template-rows:auto minmax(0,1fr) auto;overflow:hidden!important' in css,'filter menu containment CSS missing')
need('.custom-select-scroll{position:relative;min-width:0;min-height:0;overflow-y:auto;overflow-x:hidden' in css,'filter options scroll region missing')
need("wrap.closest('.filter-family')?.classList.add('select-open')" in app and '.filter-family.select-open' in css,'filter menu stacking repair missing')
need("data-license-file" in app and "button.addEventListener('click',()=>openLicenseViewer(button.dataset.licenseFile,button.dataset.licenseName))" in app and "target=\"_blank\"" not in app[app.find('function renderSettingsInformation'):app.find('function renderNetworkInfo')],'licenses are not bound to the inline viewer or still open a new tab')
need("ALLOWED_LICENSE_DOCUMENTS" in app and "raw.length>524288" in app and "credentials:'same-origin'" in app,'bounded same-origin license viewer contract missing')
need('.license-viewer-dialog{' in css and '.license-viewer-body{' in css,'license modal styling missing')
need("cache:'no-store'" in boot and 'data/release.json' in boot and 'index.html' in boot and 'marker.appAsset' in boot and 'location.replace' in boot,'startup release-ready bootstrap incomplete')
need('release-check-pending' in boot and 'html.release-check-pending body{visibility:hidden}' in css,'startup stale-UI conceal/reveal handshake missing')
need('http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"' in index,'defensive HTML no-cache metadata missing')
need('showNewReportNotification(result.added)' in app and "result.added>0" in app,'new-report notification is not tied to actual additions')
need("new-report-toast" in app and '.new-report-toast{' in css and '1 new report added' in app and 'new reports added' in app,'green live-report popup missing')
need("$('#schemaFooter').textContent=`Database ${DATABASE_VERSION}" in app,'stale hard-coded schema footer identity remains')
need('assets/release-bootstrap.v1301.js' in build,'startup bootstrap is not staged to Pages')
need("CURRENT_APP = 'app.v1301.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1301.js'" in repair,'repair tool current assets mismatch')
need("databaseReleaseVersion:'1.3.1'" in worker and "workerReleaseVersion:'1.3.1'" in worker,'Worker release identity mismatch')
need('## Release 1.3.1 startup-freshness / filter-integrity / inline-license / live-report-notification requirements' in rules,'1.3.1 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_1_freshness_filters_license_live_sync.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_1_freshness_filters_license_live_sync_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.1','releaseReady':False,'appAsset':'assets/app.v1301.js','cacheKey':'1301'},'source release marker mismatch')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.1 freshness/filter/license/live-sync contract')
