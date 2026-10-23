from __future__ import annotations
from pathlib import Path
import argparse, json, re

parser=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.18 UI, spec, security and audit contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1018.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))
audit=read('tools/audit_database.py')
quality=read('tools/quality_gate.py')

if not args.skip_version:
    need(pkg.get('version')=='1.0.18','Worker package release identity must be 1.0.18')
    need(data.get('databaseVersion')=='1.0.18','static databaseVersion must be 1.0.18')
    need('VulkanScope Database <strong>1.0.18</strong>' in index,'footer release identity missing')
    need('assets/app.v1018.js?v=1018' in index,'1.0.18 app/cache identity missing')
    need('site.v0390.css?v=1018' in index,'1.0.18 stylesheet cache key missing')
    need('config.js?v=1018' in index,'1.0.18 config cache key missing')
    need("const DATABASE_VERSION='1.0.18',LIVE_SYNC_INTERVAL_MS=10000;" in app,'runtime Database version/live-sync identity missing')
    need('Database 1.0.18 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')
    need(worker.count("databaseVersion:'1.0.18'")>=2,'Worker API databaseVersion metadata missing')

# Modal page-size selector must remain entirely usable inside the bounded dialog.
need("enhanceSelect(size);size.closest('.custom-select')?.classList.add('modal-page-size-select','drop-up')" in app,'modal page-size selector is not explicitly enhanced and anchored upward')
need('.modal-pagination .modal-page-size-select{min-width:92px!important;max-width:112px!important;flex:0 0 92px!important}' in css,'modal page-size selector is not compact/bounded')
need('.modal-pagination .modal-page-size-select .custom-select-menu{top:auto!important;bottom:calc(100% + 7px)!important' in css,'modal page-size menu is not forced inside the dialog above its trigger')
need('<select class="modal-page-size">${[10,25,50].map' in app,'modal page-size choices changed from 10/25/50')
need('Math.min(50,Math.max(1,Number(size.value)||25))' in app,'modal visible-page hard cap is not 50')

# Android robot official online color and non-tinted details.
need('fill="#3DDC84"' in app,'Android robot is not using official online green #3DDC84')
need('fill="#202124"' in app,'Android robot detail color is not preserved as dark neutral')
need('fill="#E2676A"' not in app,'legacy Vulkan red Android tint remains')
need('.filter-option-icon.android-app-icon' in css and 'fill:initial' in css,'Android icon CSS must preserve intrinsic SVG colors')

# Devices receives Versions/Statistics-style circular report distribution plus exact table.
dev=app[app.find('function renderDevices(){'):app.find('const versionValueFor=',app.find('function renderDevices(){'))]
need('deviceSliceLimit:8' in app,'Devices chart detail state missing')
need("donutChart('GPU / reports',chartItems,rs.length,'',state.deviceSliceLimit)" in dev,'Devices Statistics-style circular chart missing')
need('version-statistics device-statistics' in dev,'Devices does not reuse Versions statistics visual language')
need('GPU / REPORT DISTRIBUTION' in dev and 'GPU submission totals' in dev,'Devices chart/table headings missing')
need('gpuNameCell(x.r)' in dev and 'gpuLogoCell(x.r)' in dev and 'vendorDisplay(x.r)' in dev,'Devices table GPU identity parity regressed')
need("table(['Device','Logo','Vendor / family / ID','Max API','Driver variants','Reports','Share'],rows)" in dev,'Devices exact report-count table columns missing')
need('market share' in dev.lower(),'Devices distribution disclaimer missing')

# Preserve 1.0.17 coverage and paged evidence semantics.
need("high=ratio>=.8?' high':''" in app,'80% high-coverage threshold changed')
need('--coverage-position:${ratio*100}%' in app,'coverage endpoint percentage property missing')
need('.coverage.high .coverage-bar{position:relative!important;overflow:visible!important' in css,'coverage glow positioned anchor regression')
need('modal-value-list modal-paged-list' in app and 'coverage-report-list modal-paged-list' in app,'paged Reports/Distinct modal regression')
need('.modal-paged-list{min-height:0;max-height:min(52vh,520px);overflow-y:auto' in css,'modal scrollbar/height bound missing')
need('window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)' in app,'live synchronization regression')
need("modal.querySelector('#databaseUpdateRefresh').onclick=()=>location.reload()" in app,'new database refresh action regression')

# Latest official Vulkan baseline locked by this release remains 1.4.362 / 2026-09-04.
for token in ['Vulkan 1.4.362 (2026-09-04)','VulkanScope producer/query baseline 1.4.362','VulkanScope 1.0.19 · Vulkan 1.4.362']:
    need(token in worker, f'Worker current Vulkan metadata missing: {token}')
    need(token in read('tools/build_index.py'), f'index builder current Vulkan metadata missing: {token}')
need('"apiVersion": "1.4.362"' in read('registry/registry_lock.json') or '"apiVersion":"1.4.362"' in read('registry/registry_lock.json'),'registry lock is not Vulkan 1.4.362')
need('"headerVersion": 362' in read('registry/registry_lock.json') or '"headerVersion":362' in read('registry/registry_lock.json'),'registry header lock is not 362')

# Full source/deploy audit is current and mandatory, not a stale historical checker.
need("AUDIT_VERSION='1.0.18'" in audit,'source/artifact audit tool is not current 1.0.18')
need("APP_ASSET='app.v1018.js'" in audit and "app=text(f'assets/{APP_ASSET}')" in audit,'source audit does not inspect current frontend')
need("'app.v1018.js'" in audit and 'hdr10_plus_v1014.png' in audit,'artifact allow-list is stale')
need("run(sys.executable,'tools/audit_database.py','--source-tree','.')" in quality,'quality gate does not execute comprehensive source audit')
need("run(sys.executable,'tools/audit_database.py','--artifact-tree',td)" in quality,'quality gate does not execute staged Pages audit')

# Security / resource boundaries stay fail-closed.
need(pkg.get('devDependencies',{}).get('wrangler')=='4.130.0','Wrangler pin changed from audited 4.130.0')
need(pkg.get('overrides',{}).get('sharp')=='0.35.4','sharp override changed from audited 0.35.4')
need("default-src 'self'" in index and "object-src 'none'" in index and "base-uri 'none'" in index and "frame-ancestors 'none'" in index,'CSP hardening regressed')
need('2*1024*1024' in worker and 'readBoundedBody' in worker,'2 MiB bounded request-body path regressed')
need("new TextDecoder('utf-8',{fatal:true})" in worker,'strict UTF-8 request decoding regressed')
need('eval(' not in app and 'new Function(' not in app and 'document.write(' not in app,'unsafe dynamic frontend execution primitive introduced')

# Release integration.
need('Verify Database 1.0.18 release contract' in workflow,'workflow release gate name missing')
need('verify_1_0_18_full_audit.py' in workflow,'workflow 1.0.18 verifier missing')
need('test_1_0_18_full_audit_negative_mutations.py' in workflow,'workflow 1.0.18 negative mutations missing')
need('assets/app.v1018.js' in workflow,'workflow current app syntax check missing')
need('python tools/audit_database.py --source-tree .' in workflow,'workflow source audit missing')
need(workflow==deployed,'deployed workflow must byte-match tools/pages.workflow.yml')
need("CURRENT_APP = 'app.v1018.js'" in read('tools/repair_repository.py'),'repository repair current-app identity missing')
need('## Release 1.0.18 bounded modal selector / Android brand color / Devices statistics / full audit' in project,'PROJECT_RULES 1.0.18 section missing')
need((root/'rules/1.0.18_FULL_UI_SPEC_SECURITY_OPTIMIZATION_AUDIT.md').is_file(),'1.0.18 audit document missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.18 UI/spec/security/optimization + preserved contract')
