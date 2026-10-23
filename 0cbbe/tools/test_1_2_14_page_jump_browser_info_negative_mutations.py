from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1214.js','assets/browser-compat.v1214.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_14_page_jump_browser_info.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1214-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('out-of-range-page','assets/app.v1214.js','Number.isSafeInteger(n)&&n>=1&&n<=limit','Number.isSafeInteger(n)&&n>=1')
fixture('non-digit-insert','assets/app.v1214.js',"if(!/^\\d+$/.test(data)){e.preventDefault();return}","if(!/^\\d+$/.test(data)){return}")
fixture('paste-range','assets/app.v1214.js','if(validPageJumpValue(raw,maxPage())){input.value=raw','if(raw){input.value=raw')
fixture('filter-jump','assets/app.v1214.js',"pageJumpMarkup(1,1,'custom-select-page-jump')","'<span>Page 1</span>'")
fixture('reports-jump','assets/app.v1214.js',"pageJumpMarkup(state.reportPage,pages,'report-page-jump')","`<span>Page ${state.reportPage}</span>`")
fixture('bounded-jump','assets/app.v1214.js',"pageJumpMarkup(page,pages,'bounded-table-page-jump')","`<span>Page ${page}</span>`")
fixture('modal-jump','assets/app.v1214.js',"pageJumpMarkup(page,1,'modal-page-jump')","'<span>Page 1</span>'")
fixture('browser-section','index.html','id="settingsBrowserTitle">Browser information</h3>','id="settingsBrowserTitle">Runtime</h3>')
fixture('browser-local-only','assets/app.v1214.js','Browser information is read locally from standard browser APIs','Browser information may be uploaded for analytics')
fixture('mobile-containment','assets/site.v0390.css','@media(max-width:420px){.reports-pagination,.bounded-table-pagination{display:grid','@media(max-width:420px){.reports-pagination,.bounded-table-pagination{display:flex')
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_2_14_page_jump_browser_info.py','python tools/verify_1_2_13_filter_pagination_compare_audit.py')
print('PASS 1.2.14 negative mutation suite')
