from pathlib import Path
import argparse, json
parser=argparse.ArgumentParser()
parser.add_argument('--root',default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
def text(rel): return (root/rel).read_text(encoding='utf-8')
def need(cond,msg):
    if not cond: raise SystemExit('FAIL '+msg)
app=text('assets/app.v1410.js'); css=text('assets/site.v1410.css'); index=text('index.html'); boot=text('assets/release-bootstrap.v1410.js'); bridge=text('assets/release-bootstrap.v1409.js'); rules=text('rules/PROJECT_RULES.md'); repair=text('tools/repair_repository.py'); pages=text('tools/build_pages_artifact.py'); worker=text('worker/src/index.js')
marker=json.loads(text('data/release.json')); static=json.loads(text('data/index.json'))
need(marker=={'schemaVersion':2,'databaseVersion':'1.4.10','releaseReady':False,'appAsset':'assets/app.v1410.js','cacheKey':'1410'},'release marker mismatch')
need(static.get('databaseVersion')=='1.4.10','static index release mismatch')
for token in ['./assets/site.v1410.css?v=1410','./assets/release-bootstrap.v1410.js?v=1410','./assets/browser-compat.v1410.js?v=1410','./assets/app.v1410.js?v=1410','./assets/encyclopedia.v1410.js','./config.js?v=1410','VulkanScope Database <strong>1.4.10</strong>']:
    need(token in index,f'current index identity missing: {token}')
need("const DATABASE_VERSION='1.4.10'" in app,'frontend release identity mismatch')

# Profiles: preserve evaluator semantics and enforce larger, readable typography.
need("v.profiles=d.profileEvaluation.map(x=>({...x" in app,'structured profileEvaluation fields are not preserved losslessly')
for token in ['checkedRequirementCount','metRequirementCount','failedRequirementCount','unknownRequirementCount','checkBreakdown','missingExtensions','unknownExtensions','missingFeatures','unknownFeatures','failingLimits','unknownLimits','failingFormats','unknownFormats','failingRequirementGroups','unknownRequirementGroups']:
    need(token in app,f'profile evaluator detail missing: {token}')
for token in ['.profile-evaluation-name{font-size:16px!important','.profile-evaluation-summary{font-size:14px!important','.profile-breakdown-row{font-size:13px!important','.profile-evidence-values span{padding:7px 8px!important;font-size:12.5px!important','@media(max-width:760px){.profile-evaluation-card{padding:14px!important}.profile-evaluation-name{font-size:15px!important}']:
    need(token in css,f'profile readability contract missing: {token}')

# Loader: one visible branded panel, rotating circle restored, no native loader scrollbar / page scroll chrome.
need('class="database-loading-logo" src="assets/vulkanscope_logo_horizontal.png"' in index,'startup application logo missing')
need('<div class="database-loading-spinner"><span></span></div>' in index,'startup rotating circle missing')
need('database-loading-accent' not in index,'obsolete accent loader stage still present in startup markup')
for token in ['body.startup-layout-hold #databaseLoading{width:min(640px,calc(100vw - 32px));max-width:calc(100vw - 32px);max-height:calc(100dvh - 24px);overflow:hidden!important','@keyframes databaseLoaderSpin','animation:databaseLoaderSpin .78s linear infinite','body.database-loading #pageScrollControls,body.database-loading #viewportScrollbar,body.database-loading #pageProgress{display:none!important}']:
    need(token in css,f'loader isolation/spinner contract missing: {token}')
need("if(document.body?.classList.contains('database-loading'))" in app and "wrap.classList.remove('is-scrollable','is-active')" in app,'runtime page-scroll chrome is not fail-closed during loading')
for body,name in [(boot,'current bootstrap'),(bridge,'predecessor bridge')]:
    need("html.classList.add('release-check-pending')" in body and "html.classList.remove('release-check-pending')" in body,f'{name} release-check visibility gate missing')
need("const LOCAL='1.4.10'" in boot and "const LOCAL='1.4.9'" in bridge,'release bootstrap current/predecessor identity mismatch')
need('html.release-check-pending body{visibility:hidden}' in css,'release-check body hiding rule missing')

# Reports Submitted: all seasonal details must render from the submission instant.
need('const submissionSeasonDetails=ctx=>' in app and 'sourceDate:date' in app,'submission seasonal-time calculation missing source instant')
for token in ['standardOffset','daylightOffset','seasonalClock','offsetState','Year-round offset · no seasonal clock change','Daylight / summer time','Standard / winter time','Not observed in this time zone for this year']:
    need(token in app,f'Submitted seasonal detail missing: {token}')
for token in ['<b>Standard</b>','<b>Daylight</b>','<b>Seasonal</b>','<b>At submit</b>']:
    need(token in app,f'Reports Submitted row detail missing: {token}')
need('const submittedParts=value=>' in app and 'submissionEpoch(value)' in app,'Submitted detail no longer derives from submitted_at input')

# Both open and close must animate measured table width; temporary inline-important widths beat historical CSS !important rules.
need('const animateSubmittedColumnWidth=(tableEl,fromWidth,toWidth)=>' in app,'Submitted width animation helper missing')
for token in ["requestAnimationFrame(frame)","cell.style.setProperty('width',px,'important')","cell.style.setProperty('min-width',px,'important')","cell.style.setProperty('max-width',px,'important')","cell.style.removeProperty('width')","--submitted-column-size","window.setTimeout(()=>{document.querySelectorAll('.table-scroll-shell').forEach(updateTableScroller);queuePageScrollUi(false)},380)"]:
    need(token in app or token in css,f'Submitted close/open animation contract missing: {token}')
need('prefersReducedMotion()' in app and '@media(prefers-reduced-motion:reduce)' in css,'reduced-motion contract missing')

need("CURRENT_APP = 'app.v1410.js'" in repair and "PREDECESSOR_BRIDGE = {'app.v1409.js','browser-compat.v1409.js','release-bootstrap.v1409.js'}" in repair,'repository bridge mismatch')
need("'assets/app.v1409.js'" in pages and "'assets/app.v1410.js'" in pages and "'assets/app.v1408.js'" not in pages,'Pages bridge/current app mismatch')
need("databaseReleaseVersion:'1.4.10'" in worker and "workerReleaseVersion:'1.4.10'" in worker,'Worker release identity mismatch')
need('const supportedProducer=p=>producerAtLeast2006(p)' in worker and 'VulkanScope 2.0.6 or newer is required for new submissions' in worker,'2.0.6 producer floor regressed')
need('## Release 1.4.10 profile-readability / single-stage-loader / submitted-seasonal-time requirements' in rules,'1.4.10 rule section missing')
need((root/'rules/1.4.10_PROFILES_LOADER_SUBMITTED_TIME_AUDIT.md').is_file(),'1.4.10 audit file missing')
print('PASS Database 1.4.10 profiles/loader/Submitted-time contract')
