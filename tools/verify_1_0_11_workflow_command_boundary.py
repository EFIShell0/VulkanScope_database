from pathlib import Path
import argparse, json, re

parser=argparse.ArgumentParser(description='Verify Database 1.0.11 GitHub Actions command-boundary hotfix')
parser.add_argument('--root', default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1011.js')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
worker=read('worker/src/index.js')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))
workflow=read('.github/workflows/pages.yml')
template=read('tools/pages.workflow.yml')

# Release/cache identity.
need('assets/app.v1011.js?v=1011' in index,'current app asset/cache key missing')
need('site.v0390.css?v=1011' in index,'stylesheet cache key missing')
need('VulkanScope Database <strong>1.0.11</strong>' in index,'footer release identity missing')
need('app.v1010.js' not in index,'stale 1.0.10 application asset remains referenced by index')
need(pkg.get('version')=='1.0.11','Worker package release identity must be 1.0.11')
need(data.get('databaseVersion')=='1.0.11','static databaseVersion must be 1.0.11')

# Exact GitHub Actions failure class: multi-command reverify step must be a block scalar.
need(workflow==template,'deployed workflow must be byte-identical to canonical tools/pages.workflow.yml')
expected="""      - name: Reverify generated index metadata\n        run: |\n          python tools/verify_1_0_11_workflow_command_boundary.py\n          python tools/test_1_0_11_workflow_command_boundary_negative_mutations.py\n"""
need(expected in workflow,'Reverify generated index metadata must use a YAML run block with two distinct commands')
bad=re.search(r"- name: Reverify generated index metadata\n\s+run:\s+python\s+tools/verify_[^\n]+\n\s+python\s+tools/test_",workflow)
need(bad is None,'workflow command boundary regressed: second Python command is folded into run scalar arguments')
need(workflow.count('python tools/verify_1_0_11_workflow_command_boundary.py')>=3,'current workflow verifier must run in Windows/build/release paths')
need(workflow.count('python tools/test_1_0_11_workflow_command_boundary_negative_mutations.py')>=3,'current workflow negative mutation must run in Windows/build/release paths')

# Retain 1.0.10 Reports row-array contract.
start=app.find('function renderReports()'); end=app.find('function renderDevices()',start)
need(start>=0 and end>start,'renderReports function boundary missing')
reports=app[start:end] if start>=0 and end>start else ''
need("const table=(heads,rows)=>" in app and "${rows.join('')}" in app,'table row-array serialization contract drift')
need('const rows=rs.map(r=>' in reports,'Reports row-array construction missing')
need("}).join('');const pager=" not in reports,'Reports rows are prematurely serialized before table()')
need(re.search(r"const rows=rs\.map\(r=>\{.*?return `.*?</tr>`\}\);const pager=",reports,re.S) is not None,'Reports rows must remain an Array through pager construction')
need("table(['Submitted','Device','Logo','Driver','Device API','Loader API','Vendor','Type','OS','VulkanScope','Platform / ABI','Report ID'],rows)+pager" in reports,'Reports table must receive row Array directly')

# Retain 1.0.9 user-visible/live/floor behavior.
need('submittedParts=value=>' in app and "timeZoneName:'longOffset'" in app,'server-time presentation formatter regressed')
need('class="submitted-stack"' in reports and '<b>Date</b>' in reports and '<b>Time</b>' in reports and '<b>Time zone</b>' in reports,'stacked Date/Time/Time zone presentation regressed')
need('data-copy-report-id=' in reports and 'Copy the full 64-character Report ID' in reports,'full Report ID copy action regressed')
need('const nextReports=new Map()' in app and 'state.reports=nextReports;state.index=indexState(meta,validIndex)' in app,'atomic live reconciliation regressed')
need("if(nextReports.size!==liveIds.size)throw new Error('Live report set could not be completed atomically')" in app,'live-set cardinality gate regressed')
need("ratio>0&&ratio<.2?' low':''" in app and "ratio>0&&ratio<.05?' very-low':''" in app,'low-coverage visual thresholds regressed')
need('const producerAtLeast1019=p=>' in worker and 'supportedProducer=p=>producerAtLeast1019(p)' in worker,'VulkanScope 1.0.19 submission floor regressed')

need('Release 1.0.11 GitHub Actions command-boundary hotfix requirements' in project,'PROJECT_RULES 1.0.11 override missing')
need('6d18b5378235a5ff556576ff9d2d91ff5608dcea8076bc17ef0f32d12ec08aa4' in project,'immutable 1.0.10 predecessor hash missing from rules')

if errors:
    for e in errors: print('FAIL',e)
    raise SystemExit(1)
print('PASS Database 1.0.11 workflow command boundary / retained 1.0.10 Reports and 1.0.9 live/UI/floor behavior')
