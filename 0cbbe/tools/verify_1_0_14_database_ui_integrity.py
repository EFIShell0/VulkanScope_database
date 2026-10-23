from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json

parser=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.14 UI/data-provenance integrity contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')
def sha(rel): return hashlib.sha256((root/rel).read_bytes()).hexdigest()

app=read('assets/app.v1014.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

if not args.skip_version:
    need(pkg.get('version')=='1.0.14','Worker package release identity must be 1.0.14')
    need(data.get('databaseVersion')=='1.0.14','static databaseVersion must be 1.0.14')
    need('VulkanScope Database <strong>1.0.14</strong>' in index,'footer release identity missing')
    need('assets/app.v1014.js?v=1014' in index,'1.0.14 app/cache identity missing')
    need('site.v0390.css?v=1014' in index,'1.0.14 stylesheet cache key missing')
    need('config.js?v=1014' in index,'1.0.14 config cache key missing')
    need('Database 1.0.14 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')

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
need((root/'assets/hdr/hdr10_plus_v1014.png').is_file(),'HDR10+ 1.0.14 asset missing')
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
need('python tools/verify_1_0_14_database_ui_integrity.py' in workflow and 'python tools/test_1_0_14_database_ui_integrity_negative_mutations.py' in workflow,'1.0.14 verifier gates missing from workflow')
need('Release 1.0.14 Reports/data-presentation integrity requirements' in project,'PROJECT_RULES 1.0.14 override missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.14 UI/data-provenance integrity contract')
