from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_10_country_selector_search_pagination.py'
fixture_files=(
    'assets/app.v1310.js','assets/browser-compat.v1310.js','assets/release-bootstrap.v1310.js','assets/site.v1309.css',
    'index.html','rules/PROJECT_RULES.md','worker/src/index.js','tools/build_pages_artifact.py','tools/repair_repository.py',
    '.github/workflows/pages.yml','tools/pages.workflow.yml','data/release.json',
)
fixtures=[
 ('country-search-opt-in','assets/app.v1310.js',"const SETTINGS_SEARCHABLE_SELECTS=new Set(['settingsRegionalCountry','settingsRegionalTimeZone'])","const SETTINGS_SEARCHABLE_SELECTS=new Set(['settingsRegionalTimeZone'])"),
 ('page-size','assets/app.v1310.js','const CUSTOM_SELECT_OPTION_LIMIT=50;','const CUSTOM_SELECT_OPTION_LIMIT=100;'),
 ('full-list-search','assets/app.v1310.js',"matches=opts.map((o,i)=>({o,i})).filter(x=>!query||selectSearchText(x.o).includes(query))","matches=opts.map((o,i)=>({o,i})).slice(0,50)"),
 ('search-reset-page','assets/app.v1310.js',"if(searchable)search.addEventListener('input',()=>{optionPage=1;renderOptions({resetScroll:true})})","if(searchable)search.addEventListener('input',()=>{renderOptions({resetScroll:true})})"),
 ('browse-page-one','assets/app.v1310.js','optionPage=1;renderOptions({resetScroll:true,ensureSelected:!customSelectBrowseFromFirstPage(sel)})','optionPage=1;renderOptions({resetScroll:true,ensureSelected:true})'),
 ('country-search-label','assets/app.v1310.js',"sel.id==='settingsRegionalCountry'?'Search country / region':sel.id==='settingsRegionalTimeZone'?'Search time zones'","sel.id==='settingsRegionalTimeZone'?'Search time zones':'Search filter options'"),
 ('country-sort','assets/app.v1310.js',"items=COUNTRY_CODES.map(code=>[code,display?.of(code)||code]).sort((a,b)=>naturalCollator.compare(a[1],b[1]))","items=COUNTRY_CODES.map(code=>[code,display?.of(code)||code]).sort((a,b)=>naturalCollator.compare(a[0],b[0]))"),
 ('pager-hidden','assets/app.v1310.js','pager.hidden=!searchable','pager.hidden=true'),
 ('native-selection','assets/app.v1310.js',"sel.selectedIndex=idx;sel.dispatchEvent(new Event('change',{bubbles:true}))","sel.dispatchEvent(new Event('change',{bubbles:true}))"),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_10_country_selector_search_pagination.py','python tools/verify_1_3_9_regional_filter_layout_profile.py'),
]

def make_fixture(dst:Path):
    for rel in fixture_files:
        src=root/rel; out=dst/rel
        out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,out)

with tempfile.TemporaryDirectory(prefix='vsdb1310-mut-suite-') as td:
    base=Path(td); jobs=[]
    for i,(name,rel,a,b) in enumerate(fixtures):
        dst=base/f'{i:02d}-{name}'; dst.mkdir(); make_fixture(dst)
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}: {a!r}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        proc=subprocess.Popen([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        jobs.append((name,proc))
    escaped=[]
    for name,proc in jobs:
        if proc.wait()==0: escaped.append(name)
    if escaped: raise SystemExit('negative mutation escaped verifier: '+', '.join(escaped))
print('PASS 1.3.10 negative mutation suite')
