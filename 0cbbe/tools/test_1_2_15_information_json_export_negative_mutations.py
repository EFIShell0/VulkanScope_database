from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1215.js','assets/browser-compat.v1215.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','rules/1.2.15_INFORMATION_JSON_EXPORT_AUDIT.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/package.json']
verifier=root/'tools/verify_1_2_15_information_json_export.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1215-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('information-category','assets/app.v1215.js',"['internet','favorites','preferences','information']","['internet','favorites','preferences']")
fixture('settings-four-column','assets/site.v0390.css','grid-template-columns:repeat(4,minmax(0,1fr))','grid-template-columns:repeat(3,minmax(0,1fr))')
fixture('mobile-settings-grid','assets/site.v0390.css','.settings-category-nav{grid-template-columns:repeat(2,minmax(0,1fr))}', '.settings-category-nav{grid-template-columns:repeat(4,minmax(0,1fr))}')
fixture('download-compact-read','assets/app.v1215.js','?compact=1&_download=${Date.now()}','?_download=${Date.now()}')
fixture('download-local-json','assets/app.v1215.js',"type:'application/json;charset=utf-8'","type:'text/plain;charset=utf-8'")
fixture('wrangler-version','assets/app.v1215.js',"version:'4.130.0',license:'MIT OR Apache-2.0'","version:'4.129.0',license:'MIT OR Apache-2.0'")
fixture('unpinned-transitive','assets/app.v1215.js',"{name:'esbuild',version:'Resolved by Wrangler 4.130.0'","{name:'esbuild',version:'0.0.0'")
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_2_15_information_json_export.py','python tools/verify_1_2_14_page_jump_browser_info.py')
print('PASS 1.2.15 Information / JSON export negative mutation suite')
