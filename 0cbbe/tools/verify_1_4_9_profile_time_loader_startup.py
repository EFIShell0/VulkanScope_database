from pathlib import Path
import argparse, json
parser=argparse.ArgumentParser()
parser.add_argument('--root',default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
def text(rel): return (root/rel).read_text(encoding='utf-8')
def need(cond,msg):
    if not cond: raise SystemExit('FAIL '+msg)
app=text('assets/app.v1409.js'); css=text('assets/site.v1409.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); repair=text('tools/repair_repository.py'); pages=text('tools/build_pages_artifact.py'); worker=text('worker/src/index.js')
marker=json.loads(text('data/release.json')); static=json.loads(text('data/index.json'))
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.9','releaseReady':False,'appAsset':'assets/app.v1409.js','cacheKey':'1409'},'release marker mismatch')
need(static.get('databaseVersion')=='1.4.9','static index release mismatch')
for token in ['./assets/site.v1409.css?v=1409','./assets/release-bootstrap.v1409.js?v=1409','./assets/browser-compat.v1409.js?v=1409','./assets/app.v1409.js?v=1409','./assets/encyclopedia.v1409.js','./config.js?v=1409','VulkanScope Database <strong>1.4.9</strong>']:
    need(token in index,f'current index identity missing: {token}')
need("const DATABASE_VERSION='1.4.9'" in app,'frontend release identity mismatch')
need("v.profiles=d.profileEvaluation.map(x=>({...x" in app,'structured profileEvaluation fields are not preserved losslessly')
for token in ['checkedRequirementCount','metRequirementCount','failedRequirementCount','unknownRequirementCount','checkBreakdown','minimumApiVersion','coverageNote','missingExtensions','unknownExtensions','missingFeatures','unknownFeatures','failingLimits','unknownLimits','failingFormats','unknownFormats','failingRequirementGroups','unknownRequirementGroups']:
    need(token in app,f'profile evaluator detail missing: {token}')
need('profileEvaluationCard' in app and 'Mapped check breakdown' in app and 'Detailed evaluator counters were not reported by this producer' in app,'application-style profile detail renderer missing')
need('.page-scroll-controls{right:30px}' in css and '@media(max-width:760px){.page-scroll-controls{right:26px}' in css,'page arrows are not separated from viewport scrollbar')
for token in ['Current UTC offset','Standard / winter offset','Daylight / summer offset','Seasonal clock change','Seasonal offset setting','Current offset state','setRegionalPreviewContent']:
    need(token in app,f'regional time detail/animation missing: {token}')
need("mode==='auto'?'Automatic · browser / system'" in app and "mode==='manual'?'Selected IANA zone'" in app,'regional details do not cover auto/manual modes')
need('preview.animate([' in app and 'prefersReducedMotion()' in app,'regional height animation/reduced-motion gate missing')
need('const snapshotPromise=loadPreloadedSnapshot(),livePromise=fetchLiveIndex(api,{showProgress:false})' in app and 'Promise.allSettled([snapshotPromise,livePromise])' in app,'snapshot/live startup is not parallel')
need('assembleCurrentDatabase(api,snapshot=null,liveOverride=undefined)' in app and "if(!live){if(!snapshot)throw new Error('Current database index and preload snapshot are unavailable')" in app,'parallel startup fallback contract missing')
need('LIVE_SYNC_INTERVAL_MS=3000' in app and '/v1/sync' in app and 'void runLiveSync(false)' in app,'live per-report delta sync missing')
need('class="database-loading-logo" src="assets/vulkanscope_logo_horizontal.png"' in index,'startup application logo missing')
for token in ['databaseLoaderHalo','databaseLoaderLogo','databaseLoaderLine','databaseLoaderDot','.database-loading-logo{','@media(prefers-reduced-motion:reduce){.database-loading-logo']:
    need(token in css,f'startup logo animation/responsiveness missing: {token}')
need("CURRENT_APP = 'app.v1409.js'" in repair and "PREDECESSOR_BRIDGE = {'app.v1408.js','browser-compat.v1408.js','release-bootstrap.v1408.js'}" in repair,'repository bridge mismatch')
need("'assets/app.v1408.js'" in pages and "'assets/app.v1409.js'" in pages and "'assets/app.v1407.js'" not in pages,'Pages bridge/current app mismatch')
need("databaseReleaseVersion:'1.4.9'" in worker and "workerReleaseVersion:'1.4.9'" in worker,'Worker release identity mismatch')
need('const supportedProducer=p=>producerAtLeast2006(p)' in worker and 'VulkanScope 2.0.6 or newer is required for new submissions' in worker,'2.0.6 producer floor regressed')
need('## Release 1.4.9 profile-detail / temporal-preview / live-startup / loader-polish requirements' in rules,'1.4.9 rule section missing')
need((root/'rules/1.4.9_PROFILE_TIME_LOADER_STARTUP_AUDIT.md').is_file(),'1.4.9 audit file missing')
print('PASS Database 1.4.9 profile/time/live-startup/loader contract')
