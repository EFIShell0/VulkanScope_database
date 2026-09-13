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
app=text('assets/app.v1204.js'); compat=text('assets/browser-compat.v1204.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py')
workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.4'" in app,'frontend 1.2.4 identity missing')
need('assets/app.v1204.js?v=1204' in index and 'browser-compat.v1204.js?v=1204' in index,'1.2.4 cache/browser references missing')
need('VulkanScope Database <strong>1.2.4</strong>' in index,'footer identity missing')
need('"databaseVersion":"1.2.4"' in text('data/release.json').replace(' ',''),'release marker database version missing')
need("'databaseVersion':'1.2.4'" in build_index or '"databaseVersion":"1.2.4"' in build_index.replace(' ',''),'build_index current version missing')
# CI must verify current, not predecessor, after generated index and in source/release jobs.
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need('verify_1_2_2_release_retry.py' not in wf and 'test_1_2_2_release_retry_negative_mutations.py' not in wf,f'{name}: predecessor verifier still wired into current workflow')
    need(wf.count('python tools/verify_1_2_4_ci_bounded_tables.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_4_ci_bounded_tables_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
    need('Reverify generated index metadata' in wf and 'python tools/build_index.py' in wf,f'{name}: generated-index verification stage missing')
    need('for attempt in 1 2 3 4 5' in wf and 'HTTP 429|HTTP 5[0-9][0-9]|rate limit|temporarily unavailable' in wf,f'{name}: inherited bounded release retry missing')
    need('git rev-list -n 1 "$TAG"' in wf and 'bump the Database version instead of retargeting' in wf,f'{name}: immutable tag ownership check missing')
# Inherited browser/motion/mobile requirements.
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors missing')
need("const browserLanguage=()=> 'en-US'" in app,'English-only UI locale missing')
need("classList.toggle('at-page-top',atTop)" in app and "classList.toggle('at-page-bottom',atBottom)" in app,'scroll endpoint state classes missing')
need('@media(prefers-reduced-motion:reduce)' in css,'reduced-motion fallback missing')
need('html,body{max-width:100%;overflow-x:hidden}' in css and '@media(max-width:430px)' in css,'mobile overflow containment missing')
# Bounded GPU/device/report-derived table contract. Pagination must slice final row arrays only.
for token in ['function boundedReportTable(key,heads,rows,label=\'rows\')','rows.slice(start,end)','[10,25,50].map','function bindBoundedReportTables(renderFn)','state.tablePages[safeKey]=page']:
    need(token in app,f'bounded table core missing: {token}')
for key in ['devices-main','versions-main','memory-heaps','memory-reports','queues-main','surface-formats','surface-queues','display-main','portability-main','statistics-gpus']:
    need(f"boundedReportTable('{key}'" in app,f'bounded GPU/device table missing: {key}')
for fn in ['renderDevices','renderVersions','renderMemory','renderQueues','renderSurface','renderDisplay','renderPortability','renderTrends']:
    need(f'bindBoundedReportTables({fn})' in app,f'bounded table controls not bound in {fn}')
need('state.reportPageSize=Math.min(50,Math.max(1,Number(sel.value)||25));state.reportPage=1;state.tablePages={};renderFn()' in app,'page-size change does not reset bounded/report page state')
need('function resetReportPage(){state.reportPage=1;state.tablePages={}}' in app,'filter/navigation reset does not reset bounded table page state')
# Worker/data invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker floor fixtures missing')
need('## Release 1.2.4 CI generated-index verification / bounded GPU-device report-table requirements' in rules,'1.2.4 rules section missing')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.4','releaseReady':False,'appAsset':'assets/app.v1204.js','cacheKey':'1204'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.4 CI/bounded report-table contract')
