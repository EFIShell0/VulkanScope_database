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
app=text('assets/app.v1306.js'); compat=text('assets/browser-compat.v1306.js'); boot=text('assets/release-bootstrap.v1306.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.3.6'" in app,'frontend identity missing')
need("Unsupported browser for VulkanScope Database 1.3.6" in app,'frontend browser-error identity missing')
for token in ['assets/app.v1306.js?v=1306','assets/browser-compat.v1306.js?v=1306','assets/release-bootstrap.v1306.js?v=1306','site.v0390.css?v=1306','config.js?v=1306','VulkanScope Database <strong>1.3.6</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
# Overview stays on established layout; every other detail section adopts the evidence workspace.
need("if(t==='overview')" in app and 'detail-overview-grid' in app,'Overview contract missing')
need("detailWorkspace('overview'" not in app,'Overview was incorrectly moved into the redesigned non-Overview workspace')
for tab in ['registry','properties','limits','features','formats','memory','queues','surface','display','extensions','instance','profiles','raw']:
    need(f"detailWorkspace('{tab}'" in app,f'{tab} does not use redesigned detail workspace')
    need(f"{tab}:{{kicker:" in app,f'{tab} detail metadata missing')
need('const DETAIL_TAB_META={' in app and 'const detailSectionIntro=' in app and 'const detailPanel=' in app and 'const detailEmpty=' in app,'shared detail-workspace primitives missing')
need('.detail-section-intro{' in css and '.detail-evidence-panel{' in css and '.detail-evidence-stack{' in css,'detail-workspace CSS missing')
need('@media(max-width:760px){.detail-section-intro{padding:' in css,'detail-workspace mobile containment missing')
need('@media(prefers-reduced-motion:reduce){.detail-evidence-panel' in css,'detail-workspace reduced-motion override missing')
# Preserve semantic/canonical rendering paths.
for token in ['canonicalPropertyValue(x.name,x.value)','canonicalQueueFlags(x.flags)','formatFlags(x.linear)','memoryHeapFlags(x.flags)','memoryFlags(x.flags)','surfaceQueueState(s,x)','queryBadge(x.status)','badge(x.status)']:
    need(token in app,f'canonical/state rendering path missing: {token}')
# Raw report local download must use the stored reportText directly, not a network export path.
need("const rawReportFileName=r=>`VulkanScope-raw-report-" in app,'raw report filename helper missing')
need("function downloadRawReport(r,button){const text=String(r?.reportText??''),label=" in app,'raw report downloader does not source reportText directly')
need("new Blob([text],{type:'text/plain;charset=utf-8'})" in app,'raw report UTF-8 text/plain Blob missing or mutated')
need("a.download=rawReportFileName(r)" in app and 'URL.createObjectURL(blob)' in app,'raw report local download path missing')
raw_fn=app[app.find('function downloadRawReport'):app.find('async function downloadReportJson')]
need('fetch(' not in raw_fn and 'POST' not in raw_fn,'raw report downloader unexpectedly uses network/export request')
need('Download saves this text locally as UTF-8 TXT without normalization or reformatting.' in app,'Raw report explanation missing')
need('id="downloadRawReport"' in app and 'downloadRawReport(r,button)' in app,'Raw report tab download action not wired')
# Raw report uses the same demand-driven first-party surface scrollbar.
need(".license-viewer-body,.raw-report-scroll'" in app,'Raw report is not in shared surface-scrollbar selector')
need('class="raw-report-scroll"' in app and 'enhanceKnownSurfaceScrollbars(el)' in app,'Raw report shared scrollbar enhancement missing')
need('.raw-report-scroll{' in css and '.raw-report-scroll.surface-scroll-host' in css and '.raw-report-shell>.surface-scrollbar' in css,'Raw report themed scrollbar CSS missing')
need("scrollable=visible&&max>2" in app and "rail.classList.toggle('is-scrollable',scrollable)" in app,'demand-driven surface scrollbar regressed')
# Preserve prior requested fixes.
need('const submittedZoneMarkup=zone=>' in app and 'submitted-zone-season' in app,'1.3.5 Submitted time-zone wrapping regressed')
need('.submitted-stack .submitted-zone-value{white-space:normal' in css and '.submitted-zone-season{display:block' in css,'1.3.5 Submitted CSS wrapping regressed')
need("minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'" in app,'1.3.4 Compare chevron semantics regressed')
need('.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}' not in css,'Compare state CSS rotation returned')
# Freshness bridge and current release identity.
for token in ["'assets/app.v1305.js'","'assets/browser-compat.v1305.js'","'assets/release-bootstrap.v1305.js'","'assets/app.v1306.js'","'assets/browser-compat.v1306.js'","'assets/release-bootstrap.v1306.js'"]:
    need(token in build,f'Pages predecessor/current bridge asset missing: {token}')
need("'assets/app.v1304.js'" not in build,'stale 1.3.4 app bridge still staged')
need("PREDECESSOR_BRIDGE = {'app.v1305.js','browser-compat.v1305.js','release-bootstrap.v1305.js'}" in repair,'repository predecessor bridge mismatch')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')
need("databaseReleaseVersion:'1.3.6'" in worker and "workerReleaseVersion:'1.3.6'" in worker,'Worker release identity mismatch')
need('## Release 1.3.6 report-detail evidence-workspace / Raw-report download requirements' in rules,'1.3.6 rules section missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_6_report_detail_workspace_raw_download.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_6_report_detail_workspace_raw_download_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.6','releaseReady':False,'appAsset':'assets/app.v1306.js','cacheKey':'1306'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.6 report-detail workspace / Raw-report download contract')
