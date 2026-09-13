from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1210.js','assets/browser-compat.v1210.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_10_mobile_filters_compare_versions.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1210-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('mobile-breakpoint','assets/site.v0390.css','.compare-warning .compare-version-token{color:#fff;font-weight:900}\n@media(max-width:900px){','.compare-warning .compare-version-token{color:#fff;font-weight:900}\n@media(max-width:699px){')
fixture('nonreports-global-grid','assets/site.v0390.css','#contentView[data-main-view]:not([data-main-view="reports"]):not([data-main-view="encyclopedia"]) #filters{display:grid!important;grid-template-columns:minmax(0,1fr)!important','#contentView[data-main-view]:not([data-main-view="reports"]):not([data-main-view="encyclopedia"]) #filters{display:flex!important;grid-template-columns:minmax(0,1fr)!important')
fixture('family-control-grid','assets/site.v0390.css','.filter-family-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important','.filter-family-controls{display:flex!important;grid-template-columns:minmax(0,1fr)!important')
fixture('compare-subfilter-grid','assets/site.v0390.css','#contentView[data-main-view="compare"] .compare-filter-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important','#contentView[data-main-view="compare"] .compare-filter-controls{display:flex!important;grid-template-columns:minmax(0,1fr)!important')
fixture('version-a-emphasis','assets/app.v1210.js','<strong class="compare-version-token">${esc(producerA)}${codeA?','${esc(producerA)}${codeA?')
fixture('version-style','assets/site.v0390.css','.compare-warning .compare-version-token{color:#fff;font-weight:900}','.compare-warning .compare-version-token{color:var(--muted);font-weight:400}')
fixture('version-escaping','assets/app.v1210.js','<strong class="compare-version-token">${esc(producerB)}${codeB?','<strong class="compare-version-token">${producerB}${codeB?')
fixture('overlay-app-cleanup','tools/repair_repository.py','for p in stale_apps():','for p in []:')
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_2_10_mobile_filters_compare_versions.py','python tools/verify_1_2_9_ui_responsive_scroll.py')
print('PASS 1.2.10 negative mutation suite')
