from __future__ import annotations
from pathlib import Path
import argparse, json, sys

parser=argparse.ArgumentParser(description='Verify Database 1.0.12 Reports visual/navigation UI contract')
parser.add_argument('--root',default=None)
parser.add_argument('--skip-version',action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

app=read('assets/app.v1012.js')
css=read('assets/site.v0390.css')
index=read('index.html')
project=read('rules/PROJECT_RULES.md')
workflow=read('tools/pages.workflow.yml')
deployed=read('.github/workflows/pages.yml')
pkg=json.loads(read('worker/package.json'))
data=json.loads(read('data/index.json'))

if not args.skip_version:
    need(pkg.get('version')=='1.0.12','Worker package release identity must be 1.0.12')
    need(data.get('databaseVersion')=='1.0.12','static databaseVersion must be 1.0.12')
    need('VulkanScope Database <strong>1.0.12</strong>' in index,'footer release identity missing')
    need('assets/app.v1012.js?v=1012' in index,'1.0.12 app/cache identity missing')
    need('site.v0390.css?v=1012' in index,'1.0.12 stylesheet cache key missing')
    need('config.js?v=1012' in index,'1.0.12 config cache key missing')
    need('Database 1.0.12 · schema ${state.index.schemaVersion}' in app,'runtime footer identity missing')

# Low percentage: exact width retained, thick black hatch only, no wedge/end marker.
need("low=ratio>0&&ratio<.2?' low':''" in app,'low coverage threshold must remain below 20%')
need("veryLow=ratio>0&&ratio<.05?' very-low':''" in app,'very-low threshold must remain below 5%')
need('style="width:${ratio*100}%"' in app,'coverage fill must retain exact ratio width')
need('rgba(0,0,0,.9) 0 3px,transparent 3px 6px' in css,'low coverage must use thick black hatch')
need('.coverage.low .coverage-fill,.coverage.very-low .coverage-fill{clip-path:none!important;filter:none!important;' in css,'low/very-low coverage must explicitly remove deforming clip/filter geometry')
need('.coverage.low .coverage-bar::after{display:none!important}' in css,'low coverage endpoint marker must be disabled')

# High percentage glow/highlight with reduced-motion containment.
need("high=ratio>=.8?' high':''" in app,'high coverage threshold must be 80%')
need('.coverage.high .coverage-fill{' in css and 'box-shadow:0 0 8px var(--coverage-glow)' in css,'high coverage glow missing')
need('animation:coverageHighShine' in css and '@keyframes coverageHighShine' in css,'high coverage shine animation missing')
need('@media(prefers-reduced-motion:reduce)' in css and '.coverage.high .coverage-fill::after{animation:none' in css,'high coverage shine must respect reduced motion')

# Submitted timestamp collapse/toggle and readable expansion.
need('reportSubmittedExpanded:false' in app,'submission metadata must be collapsed by default')
need('<div class="submitted-stack"${state.reportSubmittedExpanded?\'\':\' hidden\'}>' in app,'submission metadata rows must honor collapsed state')
need('id="submittedToggle"' in app and 'M5 7h14 M5 12h14 M5 17h14' in app,'Submitted header three-line toggle missing')
need("aria-expanded=\"${state.reportSubmittedExpanded?'true':'false'}\"" in app,'Submitted toggle aria-expanded state missing')
need('.submitted-stack{min-width:212px' in css and 'overflow-wrap:anywhere' in css,'expanded submission metadata width/wrapping contract missing')

# Route reading-position restoration.
need('const routeScrollPositions=new Map()' in app,'route scroll-position store missing')
need("history.scrollRestoration='manual'" in app,'manual history scroll restoration missing')
need("if(push)rememberRouteScroll(location.hash)" in app,'push navigation must remember source scroll position')
need('render();restoreRouteScroll(location.hash)' in app,'route-event render must restore destination scroll position')
need('function openReportDetail(id)' in app and 'resetRouteScrollTop()' in app,'report detail must open through scroll-aware helper and start at top')
need("$('#detailBack').onclick=()=>{state.detailId=null;syncDocumentTitle();syncRouteUrl(true);render();restoreRouteScroll(location.hash)}" in app,'in-page Back must restore source route position')
need("x.onclick=()=>openReportDetail(x.dataset.id)" in app,'Reports rows must use scroll-aware detail navigation')
need("x.onclick=()=>openReportDetail(x.dataset.reportId)" in app,'aggregate report links must use scroll-aware detail navigation')

# Exact current VulkanScope app Android artwork (ic_android.xml) embedded locally.
need('const ANDROID_APP_FILTER_ICON=' in app,'application Android filter artwork constant missing')
need('viewBox="0 0 152 89"' in app,'Android application artwork viewport mismatch')
need('<path fill="#E2676A" d="M151.025,85.224' in app,'Android application head fill/geometry mismatch')
need('<path fill="#351719" d="M115.225,67.663' in app,'Android application eye fill/geometry mismatch')
need("key==='android'?ANDROID_APP_FILTER_ICON" in app,'Android-version filter must select application artwork')
need('.filter-option-icon.android-app-icon{' in css and 'stroke:none' in css,'application Android filter artwork style override missing')

# Retain the previous CI command-boundary repair and workflow identity.
need(workflow.encode('utf-8')==deployed.encode('utf-8'),'canonical/deployed workflow copies must remain byte-identical')
expected_reverify="""      - name: Reverify generated index metadata\n        run: |\n          python tools/verify_1_0_12_reports_visual_navigation_ui.py\n          python tools/test_1_0_12_reports_visual_navigation_ui_negative_mutations.py\n"""
need(expected_reverify in workflow,'generated-index reverify step must retain explicit YAML command boundaries')
need('run: python tools/verify_1_0_12_reports_visual_navigation_ui.py python tools/test_' not in workflow,'workflow commands must not collapse into one scalar run line')
need('Release 1.0.12 Reports visual/navigation UI requirements' in project,'PROJECT_RULES 1.0.12 override missing')

if errors:
    print('\n'.join('FAIL '+e for e in errors))
    raise SystemExit(1)
print('PASS Database 1.0.12 coverage/timestamp/scroll/Android-filter UI contract')
