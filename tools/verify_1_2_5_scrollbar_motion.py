from pathlib import Path
import argparse,json
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1205.js'); compat=text('assets/browser-compat.v1205.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.5'" in app,'frontend 1.2.5 identity missing')
need('assets/app.v1205.js?v=1205' in index and 'browser-compat.v1205.js?v=1205' in index,'1.2.5 cache/browser references missing')
need('VulkanScope Database <strong>1.2.5</strong>' in index,'footer identity missing')
need('"databaseVersion":"1.2.5"' in text('data/release.json').replace(' ',''),'release marker version missing')
need('"databaseVersion":"1.2.5"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_5_scrollbar_motion.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_5_scrollbar_motion_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
    need('verify_1_2_4_ci_bounded_tables.py' not in wf,f'{name}: stale 1.2.4 verifier remains')
    need('Reverify generated index metadata' in wf and 'python tools/build_index.py' in wf,f'{name}: generated-index verification stage missing')
    need('for attempt in 1 2 3 4 5' in wf and 'HTTP 429|HTTP 5[0-9][0-9]|rate limit|temporarily unavailable' in wf,f'{name}: bounded GitHub release retry missing')
    need('git rev-list -n 1 "$TAG"' in wf and 'bump the Database version instead of retargeting' in wf,f'{name}: immutable tag ownership check missing')
# Inherited browser/locale/mobile contract.
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors missing')
need("const browserLanguage=()=> 'en-US'" in app,'English-only UI locale missing')
need('@media(max-width:430px)' in css and 'html,body{max-width:100%;overflow-x:hidden}' in css,'mobile overflow containment missing')
# Root viewport scrollbar: mirror state to both possible root owners, no malformed escaped-newline payload.
need("document.documentElement.classList.toggle('at-page-top',atTop)" in app and "document.body?.classList.toggle('at-page-top',atTop)" in app,'top endpoint class not mirrored to html/body')
need("document.documentElement.classList.toggle('at-page-bottom',atBottom)" in app and "document.body?.classList.toggle('at-page-bottom',atBottom)" in app,'bottom endpoint class not mirrored to html/body')
need('\\n' not in css,'stylesheet contains literal escaped-newline sequence')
need('html.at-page-top::-webkit-scrollbar-button:vertical:decrement' in css and '#59565d' in css,'top viewport UP arrow gray state missing')
need('html.at-page-bottom::-webkit-scrollbar-button:vertical:increment' in css and '#ff5c66' in css,'bottom viewport DOWN arrow red state missing')
need('body.at-page-top::-webkit-scrollbar-button:vertical:decrement' in css and 'body.at-page-bottom::-webkit-scrollbar-button:vertical:increment' in css,'body-owned root scrollbar endpoint selectors missing')
# Smooth interaction language + reduced-motion accessibility.
need(':where(button,a,[role="button"],[role="tab"],[role="option"]' in css,'shared interaction motion selector missing')
need('.table-wrap tbody tr,.table-wrap tbody td{transition:' in css,'table motion missing')
need('@media(prefers-reduced-motion:reduce)' in css and 'transition:none!important' in css,'reduced-motion fallback missing')
need('const animations=[dialog.animate' in app and 'Promise.allSettled(animations.map(a=>a.finished)).then(finish)' in app and 'destructiveConfirmClosing' in app,'destructive confirmation close motion missing')
# Inherited bounded report tables must remain intact.
for token in ["function boundedReportTable(key,heads,rows,label='rows')",'rows.slice(start,end)','[10,25,50].map','function bindBoundedReportTables(renderFn)','state.tablePages[safeKey]=page']:
    need(token in app,f'bounded table core missing: {token}')
for key in ['devices-main','versions-main','memory-heaps','memory-reports','queues-main','surface-formats','surface-queues','display-main','portability-main','statistics-gpus']:
    need(f"boundedReportTable('{key}'" in app,f'bounded GPU/device table missing: {key}')
# Worker/data invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker floor fixtures missing')
need('## Release 1.2.5 root-scrollbar endpoint / complete motion requirements' in rules,'1.2.5 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.5','releaseReady':False,'appAsset':'assets/app.v1205.js','cacheKey':'1205'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.5 root-scrollbar / motion contract')
