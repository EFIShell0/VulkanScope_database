from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json

parser=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.15 UI/data-provenance integrity contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')
def sha(rel): return hashlib.sha256((root/rel).read_bytes()).hexdigest()

app=read('assets/app.v1015.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

if not args.skip_version:
    need(pkg.get('version')=='1.0.15','Worker package release identity must be 1.0.15')
    need(data.get('databaseVersion')=='1.0.15','static databaseVersion must be 1.0.15')
    need('VulkanScope Database <strong>1.0.15</strong>' in index,'footer release identity missing')
    need('assets/app.v1015.js?v=1015' in index,'1.0.15 app/cache identity missing')
    need('site.v0390.css?v=1015' in index,'1.0.15 stylesheet cache key missing')
    need('config.js?v=1015' in index,'1.0.15 config cache key missing')
    need('Database 1.0.15 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')

# 1. Submitted disclosure control remains pinned left; the label grows only to its right.
need('<div class="submitted-head"><button id="submittedToggle"' in app,'Submitted three-line control must precede the label in DOM order')
need('</svg></button><span class="submitted-label">Submitted</span></div>' in app,'Submitted label must follow the fixed toggle')
need('.submitted-head{width:30px;min-width:30px;justify-content:flex-start!important;gap:0!important}' in css,'Submitted toggle is not pinned to the left edge')
need('.submitted-toggle{order:0;flex:0 0 30px}' in css and '.submitted-label{order:1;' in css,'Submitted toggle/label ordering is not fixed')
need('.reports-table.submitted-expanded .submitted-head{width:250px;justify-content:flex-start!important;gap:0!important}' in css,'expanded Submitted header must grow right without moving the toggle')
need('.reports-table th:nth-child(8),.reports-table td:nth-child(8){min-width:320px}' in css,'Type column minimum width missing')
need('.reports-table th:nth-child(7),.reports-table td:nth-child(7){min-width:190px}' in css,'Vendor column minimum width missing')
need('.reports-table{width:max-content;min-width:100%;table-layout:auto}' in css,'Reports table must horizontally grow rather than squeeze')
need('.reports-table.submitted-expanded th:first-child,.reports-table.submitted-expanded td.submitted-cell{padding-left:6px;padding-right:12px}' in css,'Submitted disclosure left padding must stay pinned between collapsed and expanded states')

# 1b. Vendor and Type use the same fixed-left three-line disclosure pattern as Submitted.
need('reportVendorExpanded:false,reportTypeExpanded:false' in app,'Reports Vendor/Type disclosure state missing')
need("bindReportColumnDisclosure(7,'vendorToggle','Vendor','reportVendorExpanded'" in app,'Vendor three-line disclosure control missing')
need("bindReportColumnDisclosure(8,'typeToggle','Type','reportTypeExpanded'" in app,'Type three-line disclosure control missing')
need('class="report-column-reveal vendor-reveal"' in app and 'class="report-column-reveal type-reveal code"' in app,'Vendor/Type reveal wrappers missing')
need('.reports-table.vendor-collapsed th:nth-child(7)' in css and '.reports-table.type-collapsed th:nth-child(8)' in css,'Vendor/Type compact collapsed widths missing')
need('.report-column-head{width:30px;min-width:30px;' in css and '.report-column-toggle{order:0;flex:0 0 30px;' in css,'Vendor/Type hamburger buttons are not physically fixed left')
need('.reports-table.vendor-expanded .vendor-reveal{' in css and '.reports-table.type-expanded .type-reveal{' in css,'Vendor/Type expanded reveal sizing missing')

# 2. Every compared state participates, including Unknown and N/A; unique losers hatch; zero stays visible as an empty hatched track.
need('const coverageRank=(value,values)=>' in app and "const max=Math.max(...xs);if(max<=0)return'';return v===max?'dominant':'subordinate'" in app,'coverage rank must keep maximum state(s) solid and classify every strictly lower value as subordinate')
need('winners=xs.filter(x=>x===max).length' not in app,'coverage ranking must not suppress lower-state hatching when the maximum is tied')
need("const coverageValues=[x.supported,x.unsupported,x.available,x.unavailable,x.not_applicable,x.unknown]" in app,'capability denominator/rank omits a state')
need("const coverageValues=[x.available,x.unavailable,x.not_applicable,x.unknown]" in app,'query denominator/rank omits Unknown or N/A')
need("const coverageValues=[x.supported,x.unsupported,x.unknown]" in app,'support tables must include Unknown in comparison')
need("const coverageValues=[supported,unsupported,unknown]" in app,'format tables must include Unknown in comparison')
need("const coverageValues=[available,unavailable,unknown]" in app,'memory tables must include Unknown in comparison')
need("tier=rank===true||rank==='dominant'?' dominant':rank==='subordinate'?' subordinate':''" in app,'coverage tier classes missing')
need("zero=ratio===0?' zero':''" in app,'zero coverage state class missing')
need('.coverage.subordinate .coverage-fill{' in css and 'repeating-linear-gradient(135deg,rgba(0,0,0,.86)' in css,'subordinate bars must use black hatch')
need('.coverage.zero .coverage-bar{' in css and '--coverage-zero-border' in css and '.coverage.zero .coverage-fill{width:0!important' in css,'0.0% must remain visible as an empty hatched track')

# 3. Developer identity under GitHub repository control.
need('<div class="hero-side"><a class="repo-link"' in index,'GitHub/developer side stack missing')
need('<section class="developer-info" aria-label="Developer Info">' in index,'Developer Info section missing')
need('<strong>Semih Boran</strong><small>Nickname · EFI Shell</small>' in index,'Developer name/nickname missing or altered')

# 4. Raw GPU vendor ID provenance: frontend never fabricates an ID from a vendor/name field; Worker stores/validates submitted gpu.vendorId.
need("const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');" in app,'frontend vendor ID must come only from explicit gpu.vendorId')
need("r?.gpu?.vendor??'Unknown'" not in app,'textual vendor field must not be a raw vendor-ID fallback')
need('text(d.vendorId)!==text(p.gpu.vendorId)' in worker,'technicalReport/top-level vendor ID equality validation missing')
need("text(p.gpu.vendorId)||'Unknown'" in worker,'Worker storage must persist submitted gpu.vendorId directly')
for vid in ['0x5143','0x13B5','0x1010','0x19E5','0x10DE','0x1002','0x8086','0x144D','0x14E4','0x10000','0x10001','0x10002','0x10003','0x10004','0x10005','0x10006','0x10007','0x10008']:
    need(vid in app,f'presentation vendor label map lost {vid}')

# 5. Coverage reports are a modal with dark backdrop and right arrow, not a down-chevron accordion.
need('class="coverage-report-trigger"' in app and 'aria-haspopup="dialog"' in app,'coverage reports modal trigger missing')
need('aria-label="Open ${count} coverage reports"><span>${count} reports</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/>' in app,'coverage reports trigger must use a right arrow')
need("modal.className='coverage-report-modal'" in app and 'aria-modal="true"' in app,'centered coverage-report dialog missing')
need('background:rgba(0,0,0,.78)' in css and '.coverage-report-dialog{position:relative;z-index:1;width:min(760px' in css,'dark modal backdrop/centered dialog styling missing')
need('bindCoverageReportDialogs(scope)' in app,'coverage report modal binding missing')

# 6. High-percent glow/spray is anchored on the track endpoint so 100% cannot clip it away.
need('.coverage.high .coverage-fill::before,.coverage.high .coverage-fill::after{display:none!important}' in css,'old fill-clipped high effect must be disabled')
need('.coverage.high .coverage-bar::before{' in css and '.coverage.high .coverage-bar::after{' in css,'high effect must be emitted from the bar')
need(css.count('left:clamp(4px,calc(var(--coverage-pct)*1%),calc(100% - 4px))')>=2,'both high-effect endpoint layers must be clamped inside the bar')
need('animation:coverageEndpointPulse' in css and 'animation:coverageEndpointSpray' in css,'high semantic light/spray animations missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.coverage.high .coverage-bar::before,.coverage.high .coverage-bar::after{animation:none!important}' in css,'high effect reduced-motion fallback missing')

# 7. HDR10+ uses the exact local application artwork without inversion/filter mutation.
need("[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']" in app,'HDR10+ cache-busted exact asset mapping missing')
need((root/'assets/hdr/hdr10_plus_v1014.png').is_file(),'HDR10+ retained audited asset missing')
if (root/'assets/hdr/hdr10_plus_v1014.png').is_file():
    need(sha('assets/hdr/hdr10_plus_v1014.png')=='8c38222517cd48357da8a93623e3c40aa06cccc7046e806b89cf81350907aba8','HDR10+ asset is not the audited VulkanScope application artwork')
need('.hdr-logo-hdr10plus img{filter:none!important;max-height:30px}' in css,'HDR10+ must not be color-inverted/filter-mutated')

# 8. Resolution/gamut share the proportional boxed typography in aggregate and detail views.
need("const displayValueChip=(v,kind='')=>" in app,'display value chip helper missing')
need("resolutionCell=v=>hasValue(v)?displayValueChip(v,'resolution')" in app,'aggregate resolution chip missing')
need("gamutCell=v=>hasValue(v)?displayValueChip(v,'gamut')" in app,'aggregate gamut chip missing')
need("displayStateChipKv('Resolution',d.resolution,'resolution')" in app,'detail resolution chip missing')
need("displayStateChipKv('Preferred wide-gamut color space',d.preferredWideGamut,'gamut')" in app,'detail gamut chip missing')
need('.display-value-chip{' in css and 'font-family:inherit' in css and '.display-value-chip.gamut{' in css,'display chips must use proportional inherited typography and boxes')

# Release/process boundaries.
need(workflow.encode('utf-8')==deployed.encode('utf-8'),'canonical/deployed workflow copies must remain byte-identical')
need('python tools/verify_1_0_15_database_ui_integrity.py' in workflow and 'python tools/test_1_0_15_database_ui_integrity_negative_mutations.py' in workflow,'1.0.15 verifier gates missing from workflow')
need('Release 1.0.14 Reports/data-presentation integrity requirements' in project,'PROJECT_RULES preserved 1.0.14 override missing')



# 9. Route/filter/search loading accents are present across every major box family.
need('const pulseUiLoading=()=>' in app and 'body.classList.add(\'ui-loading\')' in app,'per-view loading pulse controller missing')
need('function render(){pulseUiLoading();' in app,'every main/detail render must start the loading accent')
for token in ['body.ui-loading .metric::after','body.ui-loading .card::after','body.ui-loading .table-wrap::after','body.ui-loading .kv::after','body.ui-loading .version-statistics::after']:
    need(token in css,f'loading accent missing for {token}')
need('@keyframes uiBoxLoadingSweep' in css,'box loading-bar animation missing')

# 10. Versions uses circular share statistics plus a separate count/share table, never coverage bars.
need('const versionRingCard=(g,v,n,total)=>' in app,'Versions circular statistic renderer missing')
need('class="version-ring" role="img"' in app and '--version-share:${share}' in app,'Versions ring share geometry missing')
need('class="version-ring-grid"' in app and 'class="version-report-counts"' in app,'Versions visual/table split missing')
need("table(['Device API','Loader / instance API','Reports','Share'],rows)" in app,'Versions pair report-count table missing')
versions_start=app.find('function renderVersions(){'); versions_end=app.find('function statusOk(c)',versions_start)
versions_block=app[versions_start:versions_end] if versions_start>=0 and versions_end>versions_start else ''
need('coverage(' not in versions_block and 'stateCoverage(' not in versions_block,'Versions must not render percentage bars')
need('.version-ring{--version-share:0;' in css and 'background:conic-gradient(' in css,'Versions circular CSS missing')
need('.version-share-text{' in css,'Versions plain share-table typography missing')

# 11. Every search surface has the shared animated custom clear control and shared click/focus motion.
need('const searchClearIcon=()=>' in app and 'function bindSearchClear(input,button,onClear)' in app,'shared search-clear primitive missing')
need("bindSearchClear($('#globalSearch'),$('#globalSearchClear'))" in app,'global search clear binding missing')
need("bindSearchClear(search,$('#encyclopediaSearchClear'))" in app,'Encyclopedia search clear binding missing')
need('data-search-clear="${esc(id)}"' in app,'row-search clear controls missing')
need('id="globalSearchClear"' in index,'global search clear button missing from document')
need('input[type="search"]::-webkit-search-cancel-button' in css and '-webkit-appearance:none' in css,'native abrupt search cancel button is not suppressed')
need('.search-clear-button{' in css and 'transition:opacity .18s ease' in css and '.search-clear-button.is-hidden{opacity:0;visibility:hidden;pointer-events:none;transform:scale(.72)}' in css,'smooth search clear-button motion missing')
need('button:not(:disabled):active,.repo-link:active,.card:active,.custom-select-button:active,.custom-select-option:active,.accordion-trigger:active,.inline-link:active,.chart-filter-button:active{transform:scale(.97)}' in css,'shared soft click/press animation missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.search-clear-button,.version-stat-card,.version-ring{transition:none!important}' in css,'new interaction motion lacks reduced-motion fallback')

# Screenshot regression: a history-bearing checkout is repaired before Windows canonical-state verification.
need('Repair release checkout before canonical verification' in workflow,'Windows stale-overlay repair step missing')
need('python tools/repair_repository.py --apply' in workflow and 'python tools/repair_repository.py --check' in workflow,'workflow must apply then verify repository cleanup')
need("CURRENT_APP = 'app.v1015.js'" in read('tools/repair_repository.py'),'repository repair current-app identity missing')
need('Release 1.0.15 Versions/motion/loading/overlay requirements' in project,'PROJECT_RULES 1.0.15 override missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.15 UI/data-provenance + Versions/motion/loading/overlay contract')
