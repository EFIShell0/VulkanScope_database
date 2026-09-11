from __future__ import annotations
from pathlib import Path
import argparse, json

parser=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.17 glow/Versions/paged-modal contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1017.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

if not args.skip_version:
    need(pkg.get('version')=='1.0.17','Worker package release identity must be 1.0.17')
    need(data.get('databaseVersion')=='1.0.17','static databaseVersion must be 1.0.17')
    need('VulkanScope Database <strong>1.0.17</strong>' in index,'footer release identity missing')
    need('assets/app.v1017.js?v=1017' in index,'1.0.17 app/cache identity missing')
    need('site.v0390.css?v=1017' in index,'1.0.17 stylesheet cache key missing')
    need('config.js?v=1017' in index,'1.0.17 config cache key missing')
    need("const DATABASE_VERSION='1.0.17',LIVE_SYNC_INTERVAL_MS=10000;" in app,'runtime Database version/live-sync identity missing')
    need('Database 1.0.17 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')
    need("databaseVersion:'1.0.17'" in worker and worker.count("databaseVersion:'1.0.17'")>=2,'Worker API databaseVersion metadata missing')

# Reliable >=80% high coverage effect: valid unit-bearing position + positioned anchor + persistent halo.
need("high=ratio>=.8?' high':''" in app,'80% high-coverage threshold changed')
need('--coverage-position:${ratio*100}%' in app,'coverage endpoint does not carry a percentage-valued custom property')
need('.coverage.high .coverage-bar{position:relative!important;overflow:visible!important' in css,'high coverage bar is not a positioned visible-overflow endpoint anchor')
need('left:clamp(4px,var(--coverage-position),calc(100% - 4px))!important' in css,'high coverage endpoint does not use the valid percentage custom property')
need('coverageEndpointPulseStable' in css and 'opacity:.38' in css,'high coverage halo can disappear completely during its animation')
need('.coverage.high .coverage-fill{position:relative;overflow:visible;box-shadow:0 0 12px var(--coverage-glow)' in css,'high coverage fill does not retain persistent semantic glow')
need('calc(var(--coverage-pct)*1%)' not in css,'invalid legacy CSS multiplication still controls endpoint placement')
# Existing ranking/zero contracts remain.
need("return v===max?'dominant':'subordinate'" in app,'coverage dominance/subordinate ranking regression')
need('.coverage.subordinate .coverage-fill{' in css and 'repeating-linear-gradient' in css,'subordinate hatching regression')
need("zero=ratio===0?' zero':''" in app and '.coverage.zero .coverage-bar{' in css,'0.0% hatched-empty track regression')

# Versions table uses Devices-parity GPU identity while retaining donut/no coverage bars.
vs=app[app.find('function renderVersions(){'):app.find('function statusOk(c)',app.find('function renderVersions(){'))]
need("m.set(key,{gpu,version,count:0,r})" in vs,'Versions cohorts do not preserve representative report identity')
need('gpuNameCell(x.r,x.gpu)' in vs,'Versions table is missing bold Devices-parity GPU name cell')
need('gpuLogoCell(x.r)' in vs,'Versions table is missing GPU vendor logo cell')
need('vendorDisplay(x.r)' in vs,'Versions table is missing canonical vendor/family/raw-ID text')
need("table(['GPU','Logo','Vendor / family / ID','Device API','Loader / instance API','Reports','Share'],rows)" in vs,'Versions pair table identity columns missing')
need("table(['GPU','Logo','Vendor / family / ID',g==='loader'?'Loader / instance API version':'Device API version','Reports','Share'],rows)" in vs,'Versions single-dimension table identity columns missing')
need("donutChart('GPU / Vulkan version / reports',chartItems,rs.length,'',state.versionSliceLimit)" in vs,'Versions Statistics-style donut regression')
need('coverage(' not in vs and 'stateCoverage(' not in vs and 'groupedCoverage(' not in vs,'Versions must not reintroduce percentage coverage bars')

# Shared bounded modal pagination for Reports + Distinct.
need('modalPageSize:25' in app,'modal page-size session state missing')
need("data-modal-paged=\"${paged?'1':'0'}\"" in app,'generic modal pagination metadata missing')
need('modal-value-list modal-paged-list' in app,'Distinct modal does not use paged list primitive')
need('coverage-report-list modal-paged-list' in app,'Coverage Reports modal does not use paged list primitive')
need('<select class=\"modal-page-size\">${[10,25,50].map' in app,'modal page-size choices are not bounded to 10/25/50')
need('Math.min(50,Math.max(1,Number(state.modalPageSize)||25))' in app,'modal initial page size is not capped at 50')
need('Math.min(50,Math.max(1,Number(size.value)||25))' in app,'modal page-size changes are not capped at 50')
need('Page ${page} of ${pages}' in app and 'Showing ${start+1}–${end} of ${total}' in app,'modal page/range status missing')
need("if(launch.dataset.modalPaged==='1')setupModalPagination(body)" in app,'paged modal initialization missing')
need('.modal-paged-list{min-height:0;max-height:min(52vh,520px);overflow-y:auto' in css,'paged modal visible vertical scrollbar/height bound missing')
need('.modal-paged-list::-webkit-scrollbar{width:10px}' in css and 'scrollbar-width:thin' in css,'paged modal scrollbar styling missing')
need('.modal-pagination{' in css and '.modal-page-actions{' in css,'modal pagination controls styling missing')

# Preserve 1.0.16 live/disclosure/HDR/vendor contracts.
need("bindReportColumnDisclosure(7,'vendorToggle','Vendor','reportVendorExpanded'" in app,'Vendor disclosure regression')
need("bindReportColumnDisclosure(8,'typeToggle','Type','reportTypeExpanded'" in app,'Type disclosure regression')
need('<div class="submitted-head"><button id="submittedToggle"' in app,'Submitted disclosure regression')
need('window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)' in app,'live synchronization regression')
need("modal.querySelector('#databaseUpdateRefresh').onclick=()=>location.reload()" in app,'new-version Refresh now regression')
need("const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');" in app,'raw vendor-ID provenance regression')
need("[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']" in app,'HDR10+ exact asset mapping regression')
need('<section class="developer-info" aria-label="Developer Info">' in index,'Developer Info regression')
need('@media(prefers-reduced-motion:reduce)' in css,'reduced-motion contract missing')

# Release integration.
need('Verify Database 1.0.17 release contract' in workflow,'workflow release gate name missing')
need('verify_1_0_17_glow_versions_paged_modals.py' in workflow,'workflow 1.0.17 verifier missing')
need('test_1_0_17_glow_versions_paged_modals_negative_mutations.py' in workflow,'workflow 1.0.17 negative mutations missing')
need('assets/app.v1017.js' in workflow,'workflow current app syntax check missing')
need(workflow==deployed,'deployed workflow must byte-match tools/pages.workflow.yml')
need("CURRENT_APP = 'app.v1017.js'" in read('tools/repair_repository.py'),'repository repair current-app identity missing')
need('## Release 1.0.17 coverage-glow / Versions identity / paged evidence-modal parity' in project,'PROJECT_RULES 1.0.17 section missing')
need((root/'rules/1.0.17_COVERAGE_GLOW_VERSIONS_PAGED_MODAL_AUDIT.md').is_file(),'1.0.17 audit document missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.17 glow/Versions/paged-modal + preserved contract')
