from pathlib import Path
import json, re, sys

root=Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)

def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1009.js')
css=read('assets/site.v0390.css')
worker=read('worker/src/index.js')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

need('assets/app.v1009.js?v=1009' in index,'current app asset/cache key missing')
need('site.v0390.css?v=1009' in index,'stylesheet cache key missing')
need('VulkanScope Database <strong>1.0.9</strong>' in index,'footer release identity missing')
need(pkg.get('version')=='1.0.9','Worker package version must be 1.0.9')
need(data.get('databaseVersion')=='1.0.9','static databaseVersion must be 1.0.9')
need(data.get('producerQueryBaseline')=='VulkanScope 1.0.19 · Vulkan 1.4.362','static producer baseline drift')
need(data.get('compatibleProducer')=='VulkanScope 1.0.19+ · schema 2 / technical report 3','static compatibility floor drift')

# Atomic live reconciliation: staging map first, exactly one visible state assignment after complete success.
need('const nextReports=new Map()' in app,'live reconciliation staging Map missing')
need('loadedReports=new Map()' in app,'payload staging Map missing')
need('state.reports=nextReports;state.index=indexState(meta,validIndex)' in app,'atomic report/index commit missing')
need('if(staged.failed)throw new Error' in app,'partial live payload failure is not fail-closed')
need("if(nextReports.size!==liveIds.size)throw new Error('Live report set could not be completed atomically')" in app,'complete live-set cardinality gate missing')
need("await refreshLiveDatabase(api,{showProgress:true,renderAfter:false});initFilters();applyInitialRoute();state.routeReady=true;render();" in app,'preload path must reconcile live data before first render')
need('void refreshLiveDatabase(api)' not in app,'old post-render asynchronous row insertion path remains')
load_entry=app[app.index('async function loadReportEntries'):app.index('async function loadPreloadedSnapshot')]
need('state.reports.set(' not in load_entry,'loadReportEntries must not mutate visible report state')
need('live reports ·' in app,'loading UI does not expose authoritative live count')

# Report identity/time UI.
need('submittedParts=value=>' in app and "timeZoneName:'longOffset'" in app,'separate submitted date/time/time-zone formatter missing')
need('class="submitted-stack"' in app and '<b>Date</b>' in app and '<b>Time</b>' in app and '<b>Time zone</b>' in app,'Reports submitted timestamp is not three stacked lines')
need('data-copy-report-id=' in app and 'Copy the full 64-character Report ID' in app,'full Report ID copy action missing')
need("e.stopPropagation()" in app,'Report ID copy click can bubble into row navigation')
need("VALID_REPORT_ID.test(text)" in app,'copy path does not validate exact report identifier shape')
need("r.id?.slice(0,12)" not in app,'truncated Report ID is still rendered in Reports')
need('.submitted-stack{' in css and '.report-id-copy{' in css,'new Reports controls lack design-system CSS')

# Low-percentage progress bars preserve ratio while changing shape/pattern only.
need("ratio>0&&ratio<.2?' low':''" in app,'low coverage threshold is not 20%')
need("ratio>0&&ratio<.05?' very-low':''" in app,'very-low coverage threshold is not 5%')
need('width:${ratio*100}%' in app,'coverage visual no longer uses exact numerical width')
need('.coverage.low .coverage-fill' in css and 'repeating-linear-gradient' in css and 'clip-path:' in css,'low coverage patterned/angled shape missing')
need('.coverage.very-low .coverage-fill' in css,'very-low coverage shape missing')

# Producer floor and historical read boundary.
need('const producerAtLeast1019=p=>' in worker,'1.0.19 producer predicate missing')
need('supportedProducer=p=>producerAtLeast1019(p)' in worker,'new submission floor is not 1.0.19')
need('VulkanScope 1.0.19 or newer is required for new submissions' in worker,'new submission rejection text drift')
need("producerQueryBaseline:'VulkanScope 1.0.19 · Vulkan 1.4.362'" in worker,'Worker producer metadata drift')
need("compatibleProducer:'VulkanScope 1.0.19+ · schema 2 / technical report 3'" in worker,'Worker compatibility metadata drift')
need("if(url.pathname.startsWith('/v1/reports/')&&request.method==='GET')" in worker,'historical report GET path missing')
need('1.0.18' in read('worker/tests/contract.mjs') and 'historical stored rows remain readable' in read('worker/tests/contract.mjs').lower(),'Worker tests do not cover floor/historical-read boundary')

need('Release 1.0.9 live-report consistency' in project,'PROJECT_RULES 1.0.9 release override missing')
need('aa406aafdf52bfa8e008e093e3518f4313ffd8ff4efaac1722ce923fe6f1744c' in project,'immutable 1.0.8 predecessor hash missing from rules')

if errors:
    for e in errors: print('FAIL',e)
    raise SystemExit(1)
print('PASS Database 1.0.9 live consistency / Reports identity-time UI / low-coverage / 1.0.19 floor contract')
