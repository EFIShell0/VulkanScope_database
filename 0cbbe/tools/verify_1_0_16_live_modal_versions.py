from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json

parser=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.16 live/modal/Versions contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')
def sha(rel): return hashlib.sha256((root/rel).read_bytes()).hexdigest()

app=read('assets/app.v1016.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

if not args.skip_version:
    need(pkg.get('version')=='1.0.16','Worker package release identity must be 1.0.16')
    need(data.get('databaseVersion')=='1.0.16','static databaseVersion must be 1.0.16')
    need('VulkanScope Database <strong>1.0.16</strong>' in index,'footer release identity missing')
    need('assets/app.v1016.js?v=1016' in index,'1.0.16 app/cache identity missing')
    need('site.v0390.css?v=1016' in index,'1.0.16 stylesheet cache key missing')
    need('config.js?v=1016' in index,'1.0.16 config cache key missing')
    need('Database 1.0.16 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')

# Pinned disclosure controls and enough expanded width for complete values.
need("bindReportColumnDisclosure(7,'vendorToggle','Vendor','reportVendorExpanded'" in app,'Vendor disclosure control missing')
need("bindReportColumnDisclosure(8,'typeToggle','Type','reportTypeExpanded'" in app,'Type disclosure control missing')
need('<div class="submitted-head"><button id="submittedToggle"' in app,'Submitted fixed-left control missing')
need('.reports-table{width:max-content;min-width:100%;table-layout:auto}' in css,'Reports table must grow horizontally instead of squeezing')
need('.reports-table.submitted-expanded .submitted-head{width:320px!important}' in css,'Submitted expanded width is not large enough')
need('.reports-table.submitted-expanded th:first-child,.reports-table.submitted-expanded td.submitted-cell{width:344px!important;min-width:344px!important;max-width:344px!important}' in css,'Submitted cell width contract missing')
need('.submitted-stack>span{grid-template-columns:66px minmax(228px,1fr)!important}' in css and '.submitted-stack .submitted-value{white-space:nowrap!important' in css,'date/time/time-zone values can still wrap or clip')
need('.reports-table.vendor-expanded th:nth-child(7),.reports-table.vendor-expanded td:nth-child(7){width:286px!important' in css,'Vendor expanded width contract missing')
need('.reports-table.vendor-expanded .vendor-reveal{width:260px!important;max-width:260px!important;white-space:nowrap!important;overflow:visible!important}' in css,'Vendor value can still clip')
need('.reports-table.type-expanded th:nth-child(8),.reports-table.type-expanded td:nth-child(8){width:380px!important' in css,'Type expanded width contract missing')
need('@media(max-width:760px){.reports-table.submitted-expanded .submitted-head{width:320px!important}' in css,'mobile must retain horizontal-scroll widths instead of shrinking expanded data')

# Distinct/value details are modal/right-arrow parity with Coverage reports.
need('const modalListMarkup=(label,title,body,ariaLabel=title,eyebrow=\'EVIDENCE\')=>' in app,'generic modal-list primitive missing')
need("const distinctDetails=values=>modalListMarkup(`${values.length} distinct`" in app,'Distinct modal trigger missing')
need('M9 6l6 6-6 6' in app,'modal-list triggers must use a right arrow')
need("const dist=distinctDetails(values);" in app,'aggregate Distinct cells do not use modal detail')
need('data-modal-title="${esc(title)}" data-modal-eyebrow="${esc(eyebrow)}"' in app,'modal title/eyebrow metadata missing')
need('background:rgba(0,0,0,.78)' in css,'modal dark backdrop missing')
cap_start=app.find('function capRows(items)'); cap_end=app.find('function queryRows(items)',cap_start)
qry_start=cap_end; qry_end=app.find('function renderProperties',qry_start)
need('accordionMarkup(' not in app[cap_start:cap_end] and 'accordionMarkup(' not in app[qry_start:qry_end],'Distinct aggregate rows regressed to inline accordion')

# Versions uses Statistics donut language and an exact GPU/version/report table with no coverage bars.
need("versionSliceLimit:8,statisticsSliceLimit:8" in app,'Versions chart detail state missing')
need("donutChart('GPU / Vulkan version / reports',chartItems,rs.length,'',state.versionSliceLimit)" in app,'Versions does not use the Statistics donut renderer')
need('Each slice is one GPU/version cohort' in app,'Versions GPU/version cohort semantics missing')
need("table(['GPU','Device API','Loader / instance API','Reports','Share'],rows)" in app,'Versions combined GPU/version/report table missing')
need("table(['GPU',g==='loader'?'Loader / instance API version':'Device API version','Reports','Share'],rows)" in app,'Versions single-version GPU/report table missing')
vs=app[app.find('function renderVersions(){'):app.find('function statusOk(c)',app.find('function renderVersions(){'))]
need('coverage(' not in vs and 'stateCoverage(' not in vs and 'groupedCoverage(' not in vs,'Versions must not render coverage bars')
need('.version-statistics-chart .distribution-card' in css,'Versions Statistics-style chart layout missing')

# Live report synchronization and release-version notification.
need("const DATABASE_VERSION='1.0.16',LIVE_SYNC_INTERVAL_MS=10000;" in app,'live sync/release constants missing or interval drifted')
need('window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)' in app,'periodic live synchronization missing')
need("document.addEventListener('visibilitychange',()=>{if(!document.hidden)runLiveSync()})" in app,'visibility recovery sync missing')
need("window.addEventListener('focus',runLiveSync" in app and "window.addEventListener('online',runLiveSync" in app,'focus/online recovery sync missing')
need("const missing=validIndex.filter(x=>!nextReports.has(x.id));" in app,'live sync must fetch only missing report payloads')
need("if(nextReports.size!==liveIds.size)throw new Error('Live report set could not be completed atomically');state.reports=nextReports" in app,'live report set is not swapped atomically')
need("if(changed){initFilters();if(renderAfter&&state.routeReady){render();" in app,'live universe change does not refresh all rendered metrics/views')
need("if(liveSyncBusy||!state.routeReady||!liveSyncApi||document.hidden||navigator.onLine===false)return" in app,'live sync concurrency/visibility guard missing')
need("databaseVersion:'1.0.16'" in worker and worker.count("databaseVersion:'1.0.16'")>=2,'Worker health/list databaseVersion metadata missing')
need('function maybeShowDatabaseUpdate(meta)' in app and 'compareVersion(remote,DATABASE_VERSION)<=0' in app,'newer database release detection missing')
need('id="databaseUpdateRefresh"' in app and "modal.querySelector('#databaseUpdateRefresh').onclick=()=>location.reload()" in app,'new-version Refresh now action missing')
need("modal.className='coverage-report-modal database-update-modal'" in app and 'New database version available' in app,'new-version centered modal missing')
need('.database-update-modal .coverage-report-backdrop{background:rgba(0,0,0,.82)}' in css,'new-version dark backdrop missing')

# Preserved 1.0.15 user-visible contracts.
need('reportSubmittedExpanded:false,reportVendorExpanded:false,reportTypeExpanded:false' in app,'report disclosure state regression')
need('const coverageRank=(value,values)=>' in app and "return v===max?'dominant':'subordinate'" in app,'multi-state coverage dominance regression')
need("zero=ratio===0?' zero':''" in app and '.coverage.zero .coverage-bar{' in css,'zero-state hatched coverage regression')
need('<section class="developer-info" aria-label="Developer Info">' in index and '<strong>Semih Boran</strong><small>Nickname · EFI Shell</small>' in index,'Developer Info regression')
need("const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');" in app,'vendor ID provenance regression')
need("[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']" in app,'HDR10+ exact asset mapping regression')
need('.hdr-logo-hdr10plus img{filter:none!important;max-height:30px}' in css,'HDR10+ filter regression')
need('const displayValueChip=' in app and "resolutionCell=v=>hasValue(v)?displayValueChip(v,'resolution')" in app,'resolution/gamut chip regression')
need('function render(){pulseUiLoading();' in app and '@keyframes uiBoxLoadingSweep' in css,'loading accent regression')
need('.search-clear-button.is-hidden{opacity:0;visibility:hidden;pointer-events:none;transform:scale(.72)}' in css,'search clear soft animation regression')
need('@media(prefers-reduced-motion:reduce)' in css,'reduced-motion contract missing')

# Release workflow / rules integration.
need('Repair release checkout before canonical verification' in workflow and 'python tools/repair_repository.py --apply' in workflow and 'python tools/repair_repository.py --check' in workflow,'workflow stale-overlay repair missing')
need('verify_1_0_16_live_modal_versions.py' in workflow and 'assets/app.v1016.js' in workflow,'workflow 1.0.16 verification missing')
need(workflow==deployed,'deployed workflow must byte-match tools/pages.workflow.yml')
need("CURRENT_APP = 'app.v1016.js'" in read('tools/repair_repository.py'),'repository repair current-app identity missing')
need('## Release 1.0.16 live synchronization / modal-details / Versions parity' in project,'PROJECT_RULES 1.0.16 section missing')
need((root/'rules/1.0.16_LIVE_MODAL_VERSIONS_AUDIT.md').is_file(),'1.0.16 audit document missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.16 live/modal/Versions + preserved UI contract')
