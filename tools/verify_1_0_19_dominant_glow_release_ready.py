from __future__ import annotations
from pathlib import Path
import argparse, json
parser=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.19 dominant glow and release-ready publication contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')
app=read('assets/app.v1019.js'); css=read('assets/site.v0390.css'); index=read('index.html'); project=read('rules/PROJECT_RULES.md'); workflow=read('tools/pages.workflow.yml'); deployed=read('.github/workflows/pages.yml'); worker=read('worker/src/index.js'); pkg=json.loads(read('worker/package.json')); data=json.loads(read('data/index.json')); marker=json.loads(read('data/release.json')); audit=read('tools/audit_database.py'); quality=read('tools/quality_gate.py')
if not args.skip_version:
    need(pkg.get('version')=='1.0.19','Worker package release identity must be 1.0.19')
    need(data.get('databaseVersion')=='1.0.19','static databaseVersion must be 1.0.19')
    need(marker=={'schemaVersion':1,'databaseVersion':'1.0.19','releaseReady':True},'release marker must be exact 1.0.19 release-ready identity')
    need('VulkanScope Database <strong>1.0.19</strong>' in index,'footer release identity missing')
    need('assets/app.v1019.js?v=1019' in index,'1.0.19 app/cache identity missing')
    need('site.v0390.css?v=1019' in index and 'config.js?v=1019' in index,'1.0.19 CSS/config cache identity missing')
    need("const DATABASE_VERSION='1.0.19',LIVE_SYNC_INTERVAL_MS=10000,RELEASE_CHECK_INTERVAL_MS=10000;" in app,'runtime release/live-sync identity missing')
    need(worker.count("databaseVersion:'1.0.19'")>=2,'Worker API metadata must remain current 1.0.19')
need(marker.get('releaseReady') is True,'published release marker must be releaseReady true')
# Root-cause 1: glow follows row dominance, not an 80% cliff.
need("high=ratio>0&&(rank===true||rank==='dominant')?' high':''" in app,'dominant non-zero coverage does not own glow class')
need("high=ratio>=.8?' high':''" not in app,'obsolete absolute 80% glow threshold remains')
need("return v===max?'dominant':'subordinate'" in app,'coverage ranking semantics missing')
need("if(max<=0)return''" in app,'all-zero row must not produce a dominant glow')
need('.coverage.high .coverage-bar{position:relative!important;overflow:visible!important' in css,'glow endpoint anchor regression')
need('--coverage-position:${ratio*100}%' in app,'exact endpoint percentage property missing')
# Root-cause 2: release readiness is same-origin published state, not Worker metadata.
need("fetchJsonBounded(`./data/release.json?_=${Date.now()}`,{cache:'no-store'})" in app,'same-origin no-store release marker polling missing')
need("marker?.releaseReady===true" in app,'releaseReady gate missing')
need('maybeShowDatabaseUpdate(meta)' not in app,'Worker metadata still triggers update prompt')
need('showPublishedDatabaseUpdate(String(marker.databaseVersion' in app,'published release version is not the update-dialog source')
need("u.searchParams.set('_r',String(Date.now()))" in app and 'location.replace(u.toString())' in app,'cache-busting refresh navigation missing')
need('releaseCheckTimer=window.setInterval(runPublishedReleaseCheck,RELEASE_CHECK_INTERVAL_MS)' in app,'periodic published-release check missing')
need('window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)' in app,'live report synchronization regressed')
# Publication ordering: no main Pages publication; tagged release must complete first.
need("deploy:\n    if: startsWith(github.ref, 'refs/tags/v')" in workflow,'Pages deploy is not tag-only')
need('needs: [build, release]' in workflow,'Pages deploy does not wait for release job')
need("release:\n    if: startsWith(github.ref, 'refs/tags/v')" in workflow,'tag release job missing')
need(workflow.find('  release:') < workflow.find('  deploy:'),'canonical workflow should present release before deploy')
need('Publish release-ready GitHub Pages artifact' in workflow,'release-ready Pages publication step missing')
need(workflow==deployed,'deployed workflow must byte-match canonical workflow')
# Preserve prior UI/security/spec contracts.
for token in ["classList.add('modal-page-size-select','drop-up')",'fill="#3DDC84"',"donutChart('GPU / reports',chartItems,rs.length,'',state.deviceSliceLimit)",'modal-value-list modal-paged-list','coverage-report-list modal-paged-list',"const vendorId=r=>canonicalVendorId(r?.gpu?.vendorId??'Unknown');", "[/^HDR10\\+$/i,'hdr10_plus_v1014.png','hdr10plus']"]:
    need(token in app,f'preserved frontend contract missing: {token}')
for token in ['Vulkan 1.4.362 (2026-09-04)','VulkanScope producer/query baseline 1.4.362','VulkanScope 1.0.19 · Vulkan 1.4.362']:
    need(token in worker,f'Worker Vulkan metadata missing: {token}')
need("AUDIT_VERSION='1.0.19'" in audit and "APP_ASSET='app.v1019.js'" in audit,'current source/artifact audit identity missing')
need("run(sys.executable,'tools/verify_1_0_19_dominant_glow_release_ready.py')" in quality,'quality gate current verifier missing')
need("run(sys.executable,'tools/audit_database.py','--source-tree','.')" in quality,'quality gate source audit missing')
need(pkg.get('devDependencies',{}).get('wrangler')=='4.130.0','Wrangler pin changed')
need((pkg.get('overrides') or {}).get('sharp')=='0.35.4','sharp override changed')
need("default-src 'self'" in index and "object-src 'none'" in index and "frame-ancestors 'none'" in index,'CSP hardening regressed')
need('2*1024*1024' in worker and 'readBoundedBody' in worker and "new TextDecoder('utf-8',{fatal:true})" in worker,'Worker bounded/strict UTF-8 security controls regressed')
need('## Release 1.0.19 dominant coverage glow / release-ready publication requirements' in project,'PROJECT_RULES 1.0.19 section missing')
need((root/'rules/1.0.19_DOMINANT_GLOW_RELEASE_READY_AUDIT.md').is_file(),'1.0.19 audit document missing')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.0.19 dominant glow + release-ready publication contract')
