from pathlib import Path
import argparse, json, re

parser=argparse.ArgumentParser(description='Verify Database 1.0.10 Reports render-array hotfix')
parser.add_argument('--root', default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1010.js')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

# Release/cache identity.
need('assets/app.v1010.js?v=1010' in index,'current app asset/cache key missing')
need('site.v0390.css?v=1010' in index,'stylesheet cache key missing')
need('VulkanScope Database <strong>1.0.10</strong>' in index,'footer release identity missing')
need('app.v1009.js' not in index,'stale 1.0.9 application asset remains referenced by index')
need(pkg.get('version')=='1.0.10','Worker package release identity must be 1.0.10')
need(data.get('databaseVersion')=='1.0.10','static databaseVersion must be 1.0.10')

# Exact failure class: table() owns serialization; renderReports must pass an Array.
start=app.find('function renderReports()')
end=app.find('function renderDevices()', start)
need(start>=0 and end>start,'renderReports function boundary missing')
reports=app[start:end] if start>=0 and end>start else ''
need("const table=(heads,rows)=>" in app and "${rows.join('')}" in app,'table row-array serialization contract drift')
need('const rows=rs.map(r=>' in reports,'Reports row-array construction missing')
need("}).join('');const pager=" not in reports,'Reports rows are prematurely serialized before table()')
need(re.search(r"const rows=rs\.map\(r=>\{.*?return `.*?</tr>`\}\);const pager=", reports, re.S) is not None,
     'Reports rows must remain an Array through pager construction')
need("table(['Submitted','Device','Logo','Driver','Device API','Loader API','Vendor','Type','OS','VulkanScope','Platform / ABI','Report ID'],rows)+pager" in reports,
     'Reports table must receive the row Array directly')

# Preserve every 1.0.9 behavior involved in the user-visible fix.
need('submittedParts=value=>' in app and "timeZoneName:'longOffset'" in app,'server-time presentation formatter regressed')
need('class="submitted-stack"' in reports and '<b>Date</b>' in reports and '<b>Time</b>' in reports and '<b>Time zone</b>' in reports,
     'stacked Date/Time/Time zone presentation regressed')
need('data-copy-report-id=' in reports and 'Copy the full 64-character Report ID' in reports,'full Report ID copy action regressed')
need('const nextReports=new Map()' in app and 'state.reports=nextReports;state.index=indexState(meta,validIndex)' in app,
     'atomic live reconciliation regressed')
need("if(nextReports.size!==liveIds.size)throw new Error('Live report set could not be completed atomically')" in app,
     'live-set cardinality gate regressed')
need("ratio>0&&ratio<.2?' low':''" in app and "ratio>0&&ratio<.05?' very-low':''" in app,
     'low-coverage visual thresholds regressed')
need('const producerAtLeast1019=p=>' in worker and 'supportedProducer=p=>producerAtLeast1019(p)' in worker,
     'VulkanScope 1.0.19 submission floor regressed')
need('Release 1.0.10 Reports render-array hotfix requirements' in project,'PROJECT_RULES 1.0.10 override missing')
need('0d75cfe949901636635a1039ac53921834fe690be7099ad96d45ef14a4ee6517' in project,
     'immutable 1.0.9 predecessor hash missing from rules')

if errors:
    for e in errors: print('FAIL',e)
    raise SystemExit(1)
print('PASS Database 1.0.10 Reports render-array hotfix / retained 1.0.9 live/UI/floor behavior')
