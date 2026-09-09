from pathlib import Path
import argparse, json

parser=argparse.ArgumentParser()
parser.add_argument('--root')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(value,message):
    if not value: errors.append(message)
def text(rel):
    p=root/rel
    return p.read_text(encoding='utf-8') if p.is_file() else ''
def data(rel):
    try:return json.loads(text(rel))
    except:return {}

index=text('index.html'); app=text('assets/app.v1003.js'); css=text('assets/site.v0390.css')
worker=text('worker/src/index.js'); tests=text('worker/tests/contract.mjs'); workflow=text('tools/pages.workflow.yml')
rules=text('rules/PROJECT_RULES.md'); pkg=data('worker/package.json'); static=data('data/index.json'); compat=data('compat/vulkanscope-1.0.15-database-contract.json')

need(pkg.get('version')=='1.0.3','Worker package version must be 1.0.3')
need('VulkanScope Database <strong>1.0.3</strong>' in index,'1.0.3 footer identity missing')
need('app.v1003.js?v=1003' in index and 'site.v0390.css?v=1003' in index and 'config.js?v=1003' in index,'1.0.3 cache identity missing')
need(static.get('databaseVersion')=='1.0.3','static databaseVersion must be 1.0.3')
need(static.get('producerQueryBaseline')=='VulkanScope 1.0.15 · Vulkan 1.4.362','static producer baseline must be VulkanScope 1.0.15 / Vulkan 1.4.362')
need(sorted(p.name for p in (root/'assets').glob('app.v*.js'))==['app.v1003.js'],'exactly one current versioned app asset must remain')

# Smooth page-scroll controls + top reading progress.
need('id="pageProgress" class="page-progress"' in index and 'id="pageProgressBar"' in index,'top page reading progress markup missing')
for token in ['updatePageScrollUi','queuePageScrollUi','markPageScrollActivity','scaleX(${scrollable?Math.min(1,Math.max(0,y/max)):0})','classList.toggle(\'is-visible\'','setTimeout(()=>wrap.classList.remove(\'is-active\'),900)']:
    need(token in app,f'scroll/progress runtime missing: {token}')
for token in ['.page-progress{','transform-origin:left center','transition:opacity .22s ease,transform .28s','cubic-bezier(.2,.8,.2,1)','.page-scroll-controls.is-active button.is-visible']:
    need(token in css,f'scroll/progress transition CSS missing: {token}')
need('.page-scroll-controls button[hidden]{display:none!important}' not in css,'abrupt hidden-button switching must not remain')

# Deploy-time static preload first, then live delta only.
for token in ['loadPreloadedSnapshot','./data/preload/manifest.json',"cache:'force-cache'",'refreshLiveDatabase','allIndex.filter(x=>!state.reports.has(x.id))','preloadRequestedRoute','requestedRouteReportIds']:
    need(token in app,f'preload/delta runtime missing: {token}')
need('build_preload_snapshot.py _site/data/preload' in workflow,'Pages workflow must build deploy-time preload snapshot')
need((root/'tools/build_preload_snapshot.py').is_file(),'preload snapshot builder missing')

# Meaningful local inline SVG filter icons.
for key in ['loader','driver','extension','deviceType','android','device','abi','app','calendar','hdr','gamut','resolution','refresh','displayMode']:
    need(f"{key}:" in app,f'meaningful filter icon missing: {key}')
for pair in ["loaderApiFilter:'loader'","driverModeFilter:'driver'","extensionFilter:'extension'","androidFilter:'android'","abiFilter:'abi'","submissionAgeFilter:'calendar'","hdrTypeFilter:'hdr'","resolutionFilter:'resolution'","refreshRateFilter:'refresh'","displayModeFilter:'displayMode'"]:
    need(pair in app,f'filter-to-icon mapping missing: {pair}')

# VulkanScope 1.0.15 producer compatibility stays schema-preserving and fail-closed.
need('if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch' in worker,'1.0.x producer identity mapping must be exact')
need(worker.count("producerQueryBaseline:'VulkanScope 1.0.15 · Vulkan 1.4.362'")>=2,'Worker health/list 1.0.15 producer metadata missing')
need("current1015.application.version='1.0.15'" in tests and 'current1015.application.versionCode=1015' in tests and '1.0.15 / 1015 must be accepted' in tests,'Worker 1.0.15 acceptance fixture missing')
need('bad1015Identity.application.versionCode=1014' in tests,'Worker 1.0.15 mismatched identity rejection fixture missing')
need(compat.get('submissionEnvelopeSchemaVersion')==2 and compat.get('technicalReportSchemaVersion')==3 and compat.get('normalizerVersion')==16,'1.0.15 compatibility contract schema drift')
need(compat.get('sourceEvidence',{}).get('technicalReportJson',{}).get('byteEquivalentToVulkanScope1_0_2') is True,'technicalReport serializer equivalence evidence missing')
need(compat.get('sourceEvidence',{}).get('databaseSubmissionJson',{}).get('byteEquivalentToVulkanScope1_0_2') is True,'database submission serializer equivalence evidence missing')
need(sorted(p.name for p in (root/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],'D1 migration set must remain unchanged')
need('Release 1.0.3 / VulkanScope 1.0.15 preloaded UI and compatibility requirements' in rules,'1.0.3 rules section missing')
need((root/'rules/1.0.3_VULKANSCOPE_1.0.15_PRELOAD_UI_COMPATIBILITY_AUDIT.md').is_file(),'1.0.3 release audit missing')

if errors:
    print('FAIL VulkanScope Database 1.0.3 preload/UI/compatibility audit')
    for error in errors: print('-',error)
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.3: smooth scroll UI, reading progress, deploy preload/live delta, semantic filter icons, VulkanScope 1.0.15 schema-compatible producer')
