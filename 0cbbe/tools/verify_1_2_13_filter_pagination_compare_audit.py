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
app=text('assets/app.v1213.js'); compat=text('assets/browser-compat.v1213.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.13'" in app,'frontend 1.2.13 identity missing')
need('assets/app.v1213.js?v=1213' in index and 'browser-compat.v1213.js?v=1213' in index and 'site.v0390.css?v=1213' in index,'1.2.13 cache references missing')
need('VulkanScope Database <strong>1.2.13</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1212.js').exists() and not (root/'assets/browser-compat.v1212.js').exists(),'stale 1.2.12 browser-visible bundles remain')
need("CURRENT_APP = 'app.v1213.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1213.js'" in repair,'repository repair current bundle identities missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors changed')
# Search + true 50-item pagination.
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'50-option selector page size missing')
need("customSelectShouldSearch=sel=>!!sel?.closest?.('#contentView,#detailView')&&!sel.closest('.modal-pagination')" in app,'main/detail selectors are not consistently search-enabled')
need('matches=opts.map((o,i)=>({o,i})).filter(x=>!query||selectSearchText(x.o).includes(query))' in app,'search is not sourced from the complete native option set')
need('optionPages=Math.max(1,Math.ceil(matches.length/CUSTOM_SELECT_OPTION_LIMIT))' in app,'50-item page count missing')
need('const start=(optionPage-1)*CUSTOM_SELECT_OPTION_LIMIT,visible=matches.slice(start,start+CUSTOM_SELECT_OPTION_LIMIT)' in app,'selector page slicing is not deterministic 50-at-a-time')
need("pager.className='custom-select-pagination'" in app and 'custom-select-page-prev' in app and 'custom-select-page-next' in app,'selector Previous/Next pager missing')
need('pageStatus.textContent=`Page ${optionPage} of ${optionPages}`' in app,'selector page number/status missing')
need("search.addEventListener('input',()=>{optionPage=1;renderOptions({resetScroll:true})})" in app,'search must reset selector pagination to page 1')
need("e.key==='PageDown'&&optionPage<optionPages" in app and "e.key==='PageUp'&&optionPage>1" in app,'keyboard page navigation missing')
need("status.textContent=query?'No matching options.':'No options available.'" in app,'zero-result search state missing')
need('.custom-select-pagination{' in css and '.custom-select-page-button{' in css and '.custom-select-page-status{' in css,'selector pager styling missing')
need('@media(max-width:760px){.custom-select{min-width:0}' in css and '.custom-select-page-button span{display:none}' in css,'mobile selector/pager containment missing')
need('.custom-select{max-width:100%}' in css and '.custom-select-option .filter-choice-label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' in css,'long selector content containment missing')
# Compare direction state: full=down/minimize, small=up/expand.
need('function setCompareMinimizeControl(toggle,minimized)' in app,'Compare minimize state helper missing')
need("minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'" in app,'Compare arrow direction is not minimized=up/full=down')
need('setCompareMinimizeControl(compareMinimizeToggle,minimized)' in app and 'setCompareMinimizeControl(toggle,false)' in app,'Compare arrow state is not synchronized on click/reset')
# Prior collision/overlay/responsive contracts.
need('.compare-sticky-shell.has-select-open .compare-minimize-dock{opacity:0!important;visibility:hidden!important;pointer-events:none!important' in css,'Compare dock/listbox collision protection regressed')
need('function setSettingsOpen(open){settingsOpen=!!open;if(settingsOpen)closeCustomSelects();' in app,'Settings no longer closes transient listboxes')
need('.settings-backdrop{z-index:600;backdrop-filter:blur(8px) saturate(.82);-webkit-backdrop-filter:blur(8px) saturate(.82)}' in css,'Settings full-page blur layer regressed')
need('@media(max-width:900px)' in css and '#contentView[data-main-view="compare"] .compare-filter-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important' in css,'non-Reports/Compare mobile filter containment regressed')
need('.compare-identity-line{max-height:20rem;min-width:0}' in css,'Compare identity mobile flow regressed')
# Data/transport invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("databaseReleaseVersion:'1.2.13'" in worker and "workerReleaseVersion:'1.2.13'" in worker,'Worker release identity missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need('## Release 1.2.13 filter-pagination / Compare-direction / full-UI audit requirements' in rules,'1.2.13 rules section missing')
need('"databaseVersion":"1.2.13"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_13_filter_pagination_compare_audit.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_13_filter_pagination_compare_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.13','releaseReady':False,'appAsset':'assets/app.v1213.js','cacheKey':'1213'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.13 filter pagination / Compare direction / UI containment contract')
