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
app=text('assets/app.v1214.js'); compat=text('assets/browser-compat.v1214.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.14'" in app,'frontend 1.2.14 identity missing')
need('assets/app.v1214.js?v=1214' in index and 'browser-compat.v1214.js?v=1214' in index and 'site.v0390.css?v=1214' in index,'1.2.14 cache references missing')
need('VulkanScope Database <strong>1.2.14</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1213.js').exists() and not (root/'assets/browser-compat.v1213.js').exists(),'stale 1.2.13 browser-visible bundles remain')
need("CURRENT_APP = 'app.v1214.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1214.js'" in repair,'repository repair current bundle identities missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors changed')
# Direct page jump primitive: range validation + keyboard/paste/input enforcement.
need("validPageJumpValue=(value,max)=>" in app and "/^[1-9]\\d*$/.test(raw)" in app and 'n<=limit' in app,'bounded page-number validator missing')
need('inputmode="numeric"' in app and 'pattern="[0-9]*"' in app and 'maxlength="${String(max).length}"' in app,'numeric page input contract missing')
need("input.addEventListener('beforeinput'" in app and "if(!/^\\d+$/.test(data)){e.preventDefault();return}" in app,'non-digit keyboard/beforeinput rejection missing')
need("input.addEventListener('paste'" in app and 'validPageJumpValue(raw,maxPage())' in app,'paste range rejection missing')
need("input.addEventListener('input'" in app and "if(input.value==='')return" in app,'input-event fallback validation missing')
need("e.key==='Enter'" in app and "e.key==='Escape'" in app and "e.key==='ArrowUp'||e.key==='ArrowDown'" in app,'page jump keyboard semantics missing')
need("page-jump-go" in app and 'title="Go to page"' in app,'explicit Go control missing')
# Every pagination family must use the shared page jump.
for token,msg in [
    ("pageJumpMarkup(1,1,'custom-select-page-jump')",'filter selector page jump missing'),
    ("pageJumpMarkup(page,pages,'bounded-table-page-jump')",'bounded aggregate-table page jump missing'),
    ("pageJumpMarkup(state.reportPage,pages,'report-page-jump')",'Reports page jump missing'),
    ("pageJumpMarkup(page,1,'modal-page-jump')",'modal page jump missing')]: need(token in app,msg)
need("bindPageJump(pager.querySelector('.custom-select-page-jump')" in app,'filter selector page jump not bound')
need("bindPageJump($('#content .report-page-jump')" in app,'Reports page jump not bound')
need("querySelectorAll('.bounded-table-pagination').forEach" in app and 'bindPageJump(jump' in app,'bounded table page jump not bound')
need("bindPageJump(jump,{getCurrent:()=>page,getPages:()=>Math.max(1,Math.ceil(total/pageSize))" in app,'modal page jump not bound')
# 50-item selector paging from 1.2.13 remains authoritative.
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'50-option selector page size changed')
need('optionPages=Math.max(1,Math.ceil(matches.length/CUSTOM_SELECT_OPTION_LIMIT))' in app,'selector page count regression')
need('const start=(optionPage-1)*CUSTOM_SELECT_OPTION_LIMIT,visible=matches.slice(start,start+CUSTOM_SELECT_OPTION_LIMIT)' in app,'selector 50-item slice regression')
need("search.addEventListener('input',()=>{optionPage=1;renderOptions({resetScroll:true})})" in app,'search no longer resets selector to page 1')
# Responsive presentation.
need('.page-jump{' in css and '.page-jump-input{' in css and '.page-jump-go{' in css,'shared page-jump styling missing')
need('.custom-select-pagination{grid-template-columns:minmax(0,1fr) minmax(118px,auto) minmax(0,1fr)' in css,'filter pager containment layout missing')
need('@media(max-width:420px){.reports-pagination,.bounded-table-pagination{display:grid' in css,'small-mobile table pagination containment missing')
need('.modal-page-actions .page-jump{order:4;flex:1 1 150px' in css,'mobile modal page-jump wrapping missing')
# Browser info section and local-only detailed runtime rendering.
need('id="settingsBrowserTitle">Browser information</h3>' in index and 'id="browserInfo"' in index,'Browser information Settings section missing')
need('It is not attached to reports, sent to the VulkanScope Database, or stored in D1.' in index,'Browser information local-only disclosure missing')
need('function browserIdentity()' in app and 'function renderBrowserInfo()' in app,'browser identity/runtime renderer missing')
for token in ['Client Hint brands','User agent','Rendering engine','Logical CPU cores','Device memory','Maximum touch points','Viewport','Preferred color scheme','Global Privacy Control','WebGPU','WebGL 2 API','Local storage','IndexedDB']:
    need(token in app,f'Browser information field/capability missing: {token}')
need("if(category==='internet'){updateSettingsClock();renderBrowserInfo();syncNetworkInfoAutoRefresh()}" in app,'Browser information is not refreshed with Internet settings')
need("if(settingsOpen&&settingsActiveCategory==='internet')renderBrowserInfo()" in app,'Browser viewport/runtime detail is not refreshed on resize')
need('Browser information is read locally from standard browser APIs' in app and 'not attached to VulkanScope reports' in app,'Browser renderer privacy disclosure missing')
need('canvas.toDataURL' not in app and 'WEBGL_debug_renderer_info' not in app,'forbidden browser/GPU fingerprinting primitive present')
need('.settings-browser-summary{' in css and '.settings-browser-grid .browser-long-row{' in css,'Browser information responsive styling missing')
# Existing compare direction and data contracts remain.
need("minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'" in app,'Compare arrow direction regressed')
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("databaseReleaseVersion:'1.2.14'" in worker and "workerReleaseVersion:'1.2.14'" in worker,'Worker release identity missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need('## Release 1.2.14 direct-page-jump / Browser-information requirements' in rules,'1.2.14 rules section missing')
need('"databaseVersion":"1.2.14"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_14_page_jump_browser_info.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_14_page_jump_browser_info_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.14','releaseReady':False,'appAsset':'assets/app.v1214.js','cacheKey':'1214'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.14 direct page-jump / Browser information contract')
