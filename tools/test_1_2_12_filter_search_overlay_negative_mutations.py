from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1212.js','assets/browser-compat.v1212.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_12_filter_search_overlay.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1212-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('option-bound','assets/app.v1212.js','const CUSTOM_SELECT_OPTION_LIMIT=50;','const CUSTOM_SELECT_OPTION_LIMIT=500;')
fixture('full-native-search','assets/app.v1212.js','matches=opts.map((o,i)=>({o,i})).filter(x=>!query||selectSearchText(x.o).includes(query))','matches=opts.slice(0,50).map((o,i)=>({o,i})).filter(x=>!query||selectSearchText(x.o).includes(query))')
fixture('search-scope','assets/app.v1212.js',"customSelectShouldSearch=sel=>!!sel?.closest?.('#contentView,#detailView')&&!sel.closest('.modal-pagination')","customSelectShouldSearch=sel=>sel?.id==='vendorFilter'")
fixture('compare-minimize-collision','assets/site.v0390.css','.compare-sticky-shell.has-select-open .compare-minimize-dock{opacity:0!important;visibility:hidden!important;pointer-events:none!important','.compare-sticky-shell.has-select-open .compare-minimize-dock{opacity:1!important;visibility:visible!important;pointer-events:auto!important')
fixture('settings-layer','assets/site.v0390.css','.settings-backdrop{z-index:600;backdrop-filter:blur(8px) saturate(.82);-webkit-backdrop-filter:blur(8px) saturate(.82)}','.settings-backdrop{z-index:140;backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px)}')
fixture('settings-close-transients','assets/app.v1212.js','function setSettingsOpen(open){settingsOpen=!!open;if(settingsOpen)closeCustomSelects();','function setSettingsOpen(open){settingsOpen=!!open;')
fixture('mobile-search','assets/site.v0390.css','@media(max-width:760px){.custom-select-search{height:42px;font-size:13px}','@media(max-width:760px){.custom-select-search{height:20px;font-size:8px}')
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_2_12_filter_search_overlay.py','python tools/verify_1_2_11_compare_mobile_identity.py')
print('PASS 1.2.12 negative mutation suite')
