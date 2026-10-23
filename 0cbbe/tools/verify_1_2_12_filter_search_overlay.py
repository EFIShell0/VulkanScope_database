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
app=text('assets/app.v1212.js'); compat=text('assets/browser-compat.v1212.js'); css=text('assets/site.v0390.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); contract=text('worker/tests/contract.mjs'); build_index=text('tools/build_index.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); workflow_template=text('tools/pages.workflow.yml')
need("const DATABASE_VERSION='1.2.12'" in app,'frontend 1.2.12 identity missing')
need('assets/app.v1212.js?v=1212' in index and 'browser-compat.v1212.js?v=1212' in index and 'site.v0390.css?v=1212' in index,'1.2.12 cache references missing')
need('VulkanScope Database <strong>1.2.12</strong>' in index,'footer identity missing')
need(not (root/'assets/app.v1211.js').exists() and not (root/'assets/browser-compat.v1211.js').exists(),'stale 1.2.11 browser-visible bundles remain')
need("CURRENT_APP = 'app.v1212.js'" in repair and "CURRENT_BROWSER_COMPAT = 'browser-compat.v1212.js'" in repair,'repository repair current bundle identities missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'validated browser floors changed')
# Search/bounding behavior.
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'50-option custom selector bound missing')
need("customSelectShouldSearch=sel=>!!sel?.closest?.('#contentView,#detailView')&&!sel.closest('.modal-pagination')" in app,'all main/detail workspace selectors are not search-enabled')
need("search.type='search'" in app and "search.placeholder='Search options…'" in app,'local option search input missing')
need('matches=opts.map((o,i)=>({o,i})).filter(x=>!query||selectSearchText(x.o).includes(query))' in app,'filter search is not sourced from the complete native option set')
need('matches.slice(start,start+CUSTOM_SELECT_OPTION_LIMIT)' in app,'rendered listbox is not bounded to 50 options')
need('Showing ${start+1}–${start+visible.length} of ${matches.length} options. Search to narrow.' in app,'bounded-result disclosure missing')
need("status.textContent=query?'No matching options.':'No options available.'" in app,'zero-result search state missing')
need("search.addEventListener('input',()=>renderOptions({resetScroll:true}))" in app,'search input does not live-filter options')
need("inSearch&&(e.key==='ArrowDown'||e.key==='Enter')" in app and "e.key==='Escape'" in app and "e.key==='Home'" in app and "e.key==='End'" in app,'search/listbox keyboard contract missing')
need('.custom-select-search-shell{' in css and '.custom-select-search{' in css and '@media(max-width:760px){.custom-select-search{height:42px;font-size:13px}' in css,'desktop/mobile search presentation missing')
# Compare button collision and Settings backdrop ownership.
need("wrap.closest('.compare-sticky-shell')?.classList.add('has-select-open')" in app,'Compare sticky shell does not receive open-listbox state')
need("syncCompareSelectLayerState(wrap)" in app,'Compare open-listbox state is not synchronized on close')
need('.compare-sticky-shell.has-select-open .compare-minimize-dock{opacity:0!important;visibility:hidden!important;pointer-events:none!important' in css,'Compare minimize dock is not suppressed while listbox is open')
need('function setSettingsOpen(open){settingsOpen=!!open;if(settingsOpen)closeCustomSelects();' in app,'Settings does not close transient listboxes before opening')
need('.settings-backdrop{z-index:600;backdrop-filter:blur(8px) saturate(.82);-webkit-backdrop-filter:blur(8px) saturate(.82)}' in css,'Settings backdrop does not own a full-page blur layer above pinned Compare')
need('.settings-drawer{z-index:610}' in css and '.settings-drawer>.surface-scrollbar{z-index:620}' in css,'Settings drawer/rail layering missing')
need('.destructive-confirm-backdrop{z-index:700}.destructive-confirm-dialog{z-index:701}' in css,'destructive confirmation is not above Settings')
# Prior responsive/identity fixes remain present.
need('@media(max-width:900px)' in css and '#contentView[data-main-view="compare"] .compare-filter-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important' in css,'1.2.10 mobile filter containment regressed')
need('.compare-identity-line{max-height:20rem;min-width:0}' in css,'1.2.11 Compare identity flow regressed')
# Transport/data invariants.
need('const supportedProducer=p=>producerAtLeast1205(p)' in worker,'VulkanScope 1.2.5 submission floor missing')
need("databaseReleaseVersion:'1.2.12'" in worker and "workerReleaseVersion:'1.2.12'" in worker,'Worker release identity missing')
need("current.application.version='1.2.5'" in contract and "below.application.version='1.2.4'" in contract,'Worker producer-floor fixtures missing')
need('## Release 1.2.12 searchable-filter and overlay-layer requirements' in rules,'1.2.12 rules section missing')
need('"databaseVersion":"1.2.12"' in build_index.replace(' ',''),'build_index current version missing')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',workflow_template)]:
    need(wf.count('python tools/verify_1_2_12_filter_search_overlay.py')>=3,f'{name}: current verifier not used in Windows/build/release stages')
    need(wf.count('python tools/test_1_2_12_filter_search_overlay_negative_mutations.py')>=3,f'{name}: current negative suite not used in Windows/build/release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.2.12','releaseReady':False,'appAsset':'assets/app.v1212.js','cacheKey':'1212'},'source release marker mismatch')
if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.2.12 searchable-filter / overlay-layer contract')
