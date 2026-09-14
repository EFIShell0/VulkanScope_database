from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1213.js','assets/browser-compat.v1213.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_13_filter_pagination_compare_audit.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1213-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('page-size','assets/app.v1213.js','const CUSTOM_SELECT_OPTION_LIMIT=50;','const CUSTOM_SELECT_OPTION_LIMIT=75;')
fixture('page-count','assets/app.v1213.js','optionPages=Math.max(1,Math.ceil(matches.length/CUSTOM_SELECT_OPTION_LIMIT))','optionPages=1')
fixture('page-slice','assets/app.v1213.js','const start=(optionPage-1)*CUSTOM_SELECT_OPTION_LIMIT,visible=matches.slice(start,start+CUSTOM_SELECT_OPTION_LIMIT)','const start=0,visible=matches.slice(0,CUSTOM_SELECT_OPTION_LIMIT)')
fixture('search-page-reset','assets/app.v1213.js',"search.addEventListener('input',()=>{optionPage=1;renderOptions({resetScroll:true})})","search.addEventListener('input',()=>renderOptions({resetScroll:true}))")
fixture('arrow-direction','assets/app.v1213.js',"minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'","minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'")
fixture('mobile-containment','assets/site.v0390.css','@media(max-width:760px){.custom-select{min-width:0}','@media(max-width:760px){.custom-select{min-width:190px}')
fixture('option-overflow','assets/site.v0390.css','.custom-select-option .filter-choice-label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}','.custom-select-option .filter-choice-label{white-space:nowrap}')
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_2_13_filter_pagination_compare_audit.py','python tools/verify_1_2_12_filter_search_overlay.py')
print('PASS 1.2.13 negative mutation suite')
