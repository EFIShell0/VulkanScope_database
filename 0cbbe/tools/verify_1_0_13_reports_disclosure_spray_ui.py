from __future__ import annotations
from pathlib import Path
import argparse, json

parser=argparse.ArgumentParser(description='Verify Database 1.0.13 Reports disclosure/color-spray UI contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1013.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

if not args.skip_version:
    need(pkg.get('version')=='1.0.13','Worker package release identity must be 1.0.13')
    need(data.get('databaseVersion')=='1.0.13','static databaseVersion must be 1.0.13')
    need('VulkanScope Database <strong>1.0.13</strong>' in index,'footer release identity missing')
    need('assets/app.v1013.js?v=1013' in index,'1.0.13 app/cache identity missing')
    need('site.v0390.css?v=1013' in index,'1.0.13 stylesheet cache key missing')
    need('config.js?v=1013' in index,'1.0.13 config cache key missing')
    need('Database 1.0.13 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')

# Submitted disclosure: compact by default, no reserved detail width, animated expansion.
need('reportSubmittedExpanded:false' in app,'Submitted detail must remain collapsed by default')
need('class="submitted-reveal" aria-hidden="${state.reportSubmittedExpanded?' in app,'Submitted detail must use an aria-aware reveal wrapper')
need("reportsTable.classList.add('reports-table',state.reportSubmittedExpanded?'submitted-expanded':'submitted-collapsed')" in app,'Reports table disclosure state class missing')
need("tableEl.classList.toggle('submitted-expanded',expanded)" in app and "tableEl.classList.toggle('submitted-collapsed',!expanded)" in app,'Submitted toggle does not drive table disclosure classes')
need("querySelectorAll('.submitted-reveal').forEach(reveal=>reveal.setAttribute('aria-hidden',expanded?'false':'true'))" in app,'Submitted reveal aria state not synchronized')
need("window.setTimeout(()=>{document.querySelectorAll('.table-scroll-shell').forEach(updateTableScroller)" in app,'table scroller is not recalculated after disclosure animation')
need('.submitted-reveal{width:0;max-width:0;max-height:0;opacity:0;overflow:hidden;visibility:hidden' in css,'collapsed Submitted reveal must consume zero detail width/height')
need('.reports-table.submitted-collapsed th:first-child,.reports-table.submitted-collapsed td.submitted-cell{width:42px;min-width:42px;max-width:42px}' in css,'collapsed Submitted column is not compact')
need('.reports-table{width:max-content;min-width:100%;table-layout:auto}' in css,'Reports table must grow horizontally instead of squeezing adjacent columns')
need('.reports-table.submitted-expanded .submitted-reveal{width:232px;max-width:232px;max-height:100px;opacity:1;visibility:visible;transform:none' in css,'expanded Submitted reveal geometry missing')
need('transition:width .32s cubic-bezier(.2,.8,.2,1),max-width .32s' in css and 'visibility 0s linear .32s' in css,'Submitted width/visibility animation missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.submitted-head,.submitted-label,.submitted-reveal' in css and 'transition:none!important' in css,'Submitted animation must respect reduced motion')

# High coverage: semantic color spray/halo, no white sweep contract.
need("high=ratio>=.8?' high':''" in app,'high coverage threshold must remain 80%')
for token in ['--coverage-spray:var(--green)','--coverage-spray:var(--red)','--coverage-spray:var(--blue)','--coverage-spray:var(--amber)']:
    need(token in css,f'missing semantic high-coverage spray token: {token}')
need('.coverage.high .coverage-bar{position:relative;overflow:visible;isolation:isolate}' in css,'high coverage spray would be clipped by the bar')
need('.coverage.high .coverage-fill::before{' in css and 'animation:coverageColorPulse' in css,'high coverage color halo missing')
need('.coverage.high .coverage-fill::after{' in css and 'box-shadow:4px -7px' in css and 'animation:coverageColorSpray' in css,'high coverage particle spray missing')
need('@keyframes coverageColorPulse' in css and '@keyframes coverageColorSpray' in css,'high coverage spray keyframes missing')
need('background:currentColor;color:var(--coverage-spray)' in css,'high spray must inherit semantic state color')
need('.coverage.high .coverage-fill::before,.coverage.high .coverage-fill::after{animation:none!important}' in css,'high spray/pulse must respect reduced motion')

# Retained 1.0.12 contracts.
need('rgba(0,0,0,.9) 0 3px,transparent 3px 6px' in css,'low coverage black hatch regressed')
need('.coverage.low .coverage-fill,.coverage.very-low .coverage-fill{clip-path:none!important;filter:none!important;' in css,'low coverage non-deforming geometry regressed')
need('const routeScrollPositions=new Map()' in app and "history.scrollRestoration='manual'" in app,'report-back scroll restoration regressed')
need('const ANDROID_APP_FILTER_ICON=' in app and 'viewBox="0 0 152 89"' in app and "key==='android'?ANDROID_APP_FILTER_ICON" in app,'Android application filter artwork regressed')
need('data-copy-report-id="${rid}"' in app and 'Copy the full 64-character Report ID' in app,'full Report ID copy contract regressed')

# Workflow command boundary retained and current release verifier wired.
need(workflow.encode('utf-8')==deployed.encode('utf-8'),'canonical/deployed workflow copies must remain byte-identical')
expected="""      - name: Reverify generated index metadata\n        run: |\n          python tools/verify_1_0_13_reports_disclosure_spray_ui.py\n          python tools/test_1_0_13_reports_disclosure_spray_ui_negative_mutations.py\n"""
need(expected in workflow,'generated-index reverify commands must be distinct block-scalar lines')
need('Release 1.0.13 Reports disclosure animation / high-coverage color-spray requirements' in project,'PROJECT_RULES 1.0.13 override missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS Database 1.0.13 Reports disclosure animation / semantic high-coverage spray contract')
