from pathlib import Path
import argparse,json,re
parser=argparse.ArgumentParser(); parser.add_argument('--root',default=None); args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def text(rel):
    p=root/rel
    if not p.is_file(): errors.append(f'missing {rel}'); return ''
    return p.read_text(encoding='utf-8')
app=text('assets/app.v1310.js'); compat=text('assets/browser-compat.v1310.js'); boot=text('assets/release-bootstrap.v1310.js'); css=text('assets/site.v1309.css'); index=text('index.html'); rules=text('rules/PROJECT_RULES.md'); worker=text('worker/src/index.js'); build=text('tools/build_pages_artifact.py'); repair=text('tools/repair_repository.py'); workflow=text('.github/workflows/pages.yml'); template=text('tools/pages.workflow.yml')

# Release/cache identity. CSS is intentionally unchanged from 1.3.9.
need("const DATABASE_VERSION='1.3.10'" in app,'frontend release identity missing')
need("Unsupported browser for VulkanScope Database 1.3.10" in app,'frontend browser-error identity missing')
for token in ['assets/app.v1310.js?v=1310','assets/browser-compat.v1310.js?v=1310','assets/release-bootstrap.v1310.js?v=1310','site.v1309.css?v=1309','config.js?v=1310','VulkanScope Database <strong>1.3.10</strong>']:
    need(token in index,f'index identity/reference missing: {token}')
need("const LOCAL='1.3.10'" in boot,'release bootstrap identity missing')
need('chromium:84,firefox:86,safari:14.1' in compat,'browser floor changed')

# Root-cause guard: Settings Country/Time-zone must opt into the shared searchable selector family.
need("const SETTINGS_SEARCHABLE_SELECTS=new Set(['settingsRegionalCountry','settingsRegionalTimeZone'])" in app,'Settings large-selector searchable allow-list missing')
need("SETTINGS_SEARCHABLE_SELECTS.has(String(sel.id||''))" in app and "!!sel?.closest?.('#contentView,#detailView')" in app,'searchability no longer preserves Settings + existing content/detail selectors')
need("const customSelectBrowseFromFirstPage=sel=>SETTINGS_SEARCHABLE_SELECTS.has(String(sel?.id||''))" in app,'Settings browse-from-page-one guard missing')
need("sel.id==='settingsRegionalCountry'?'Search country / region':sel.id==='settingsRegionalTimeZone'?'Search time zones'" in app,'country/time-zone search labels missing')
need("search.placeholder=searchLabel+'…'" in app and "search.setAttribute('aria-label',searchLabel)" in app,'search label/placeholder accessibility contract missing')

# Full-list-before-pagination and deterministic 50-option paging.
need('const CUSTOM_SELECT_OPTION_LIMIT=50;' in app,'custom selector option page size changed')
need("const opts=[...sel.options]" in app and "query=searchable?search.value.trim().toLocaleLowerCase():''" in app,'search does not start from full native select option set')
need("matches=opts.map((o,i)=>({o,i})).filter(x=>!query||selectSearchText(x.o).includes(query))" in app,'search is not applied before pagination')
need('optionPages=Math.max(1,Math.ceil(matches.length/CUSTOM_SELECT_OPTION_LIMIT))' in app,'selector page-count math missing')
need('visible=matches.slice(start,start+CUSTOM_SELECT_OPTION_LIMIT)' in app,'selector page slicing missing')
need("if(searchable)search.addEventListener('input',()=>{optionPage=1;renderOptions({resetScroll:true})})" in app,'selector search must reset to page 1')
need('pager.hidden=!searchable' in app and "pageJumpMarkup(1,1,'custom-select-page-jump')" in app,'searchable selector pager/page jump wiring missing')
need("pager.querySelector('.custom-select-page-prev').onclick=e=>{e.stopPropagation();setOptionPage(optionPage-1)}" in app and "pager.querySelector('.custom-select-page-next').onclick=e=>{e.stopPropagation();setOptionPage(optionPage+1)}" in app,'Previous/Next selector paging missing')
need("bindPageJump(pager.querySelector('.custom-select-page-jump'),{getCurrent:()=>optionPage,getPages:()=>optionPages,onGo:page=>setOptionPage(page)})" in app,'direct numeric selector page jump missing')
need('input.disabled=single' in app,'one-page direct page-jump disabled contract missing')

# Fix selected-page trap without changing selection semantics.
need('optionPage=1;renderOptions({resetScroll:true,ensureSelected:!customSelectBrowseFromFirstPage(sel)})' in app,'Settings Country/Time-zone must open from first browse page')
need("const setOptionPage=(nextPage,{focus='none'}={})=>" in app and 'optionPage=target;renderOptions({resetScroll:true})' in app,'selector authoritative page-state path missing')
need("sel.selectedIndex=idx;sel.dispatchEvent(new Event('change',{bubbles:true}))" in app,'native select is no longer authoritative on explicit choice')

# Country list completeness, ordering and code-visible search text.
cm=re.search(r"const COUNTRY_CODES=Object\.freeze\('([^']+)'\.split\(','\)\);",app)
need(bool(cm),'country code declaration missing')
if cm:
    codes=cm.group(1).split(',')
    need(len(codes)==250,f'expected 250 country/region codes, found {len(codes)}')
    need(len(set(codes))==250,'country code list contains duplicates')
need("items=COUNTRY_CODES.map(code=>[code,display?.of(code)||code]).sort((a,b)=>naturalCollator.compare(a[1],b[1]))" in app,'country options are not sorted by English display name')
need('items.map(([code,name])=>`<option value="${code}">${esc(name)} (${code})</option>`)' in app,'country option text no longer exposes the two-letter code to search')
need("<option value=\"auto\">Browser / system region" in app,'Browser/system first country option missing')

# Preserve 1.3.9 regional ownership/profile/timestamp behavior.
need("const enabled=mode==='country'?id==='settingsRegionalCountry':mode==='manual'?id!=='settingsRegionalCountry':false" in app,'Automatic/Country/Manual lock matrix regressed')
need("else if(state.regionalMode==='manual')state.regionalCountry='auto'" in app,'Manual mode no longer clears country override')
need("if(mode==='auto'||mode==='manual')return browserLanguage()" in app,'Manual locale is unexpectedly country-derived')
need('const countryRegionalProfile=' in app and 'const COUNTRY_PRIMARY_TIME_ZONES=Object.freeze(' in app,'country presentation profile regressed')
need('const submissionEpoch=value=>' in app and "Date.parse(String(value||''))" in app,'server timestamp epoch path regressed')
need('.settings-regional-group .settings-select-row{grid-template-columns:minmax(0,1fr)!important' in css,'1.3.9 full-width regional layout regressed')
need('.custom-select-scroll{padding-right:0!important}' in css and '.custom-select-scroll.has-surface-scrollbar{padding-right:23px!important}' in css,'1.3.9 demand-driven scrollbar gutter regressed')

# Release rules / Worker / cache bridge / release pipeline.
need('## Release 1.3.10 country-selector search / pagination requirements' in rules,'1.3.10 rules section missing')
need("databaseReleaseVersion:'1.3.10'" in worker and "workerReleaseVersion:'1.3.10'" in worker,'Worker release identity mismatch')
need("PREDECESSOR_BRIDGE = {'app.v1309.js','browser-compat.v1309.js','release-bootstrap.v1309.js'}" in repair,'repository predecessor bridge mismatch')
need("'assets/app.v1309.js'" in build and "'assets/app.v1310.js'" in build and "'assets/app.v1308.js'" not in build,'Pages immediate predecessor/current app bridge mismatch')
for name,wf in [('.github/workflows/pages.yml',workflow),('tools/pages.workflow.yml',template)]:
    need(wf.count('python tools/verify_1_3_10_country_selector_search_pagination.py')>=3,f'{name}: current verifier missing from release stages')
    need(wf.count('python tools/test_1_3_10_country_selector_search_pagination_negative_mutations.py')>=3,f'{name}: negative suite missing from release stages')
marker=json.loads(text('data/release.json') or '{}')
need(marker=={'schemaVersion':2,'databaseVersion':'1.3.10','releaseReady':False,'appAsset':'assets/app.v1310.js','cacheKey':'1310'},'source release marker mismatch')

if errors:
    print('\n'.join('FAIL '+e for e in errors)); raise SystemExit(1)
print('PASS VulkanScope Database 1.3.10 country selector search/pagination contract')
