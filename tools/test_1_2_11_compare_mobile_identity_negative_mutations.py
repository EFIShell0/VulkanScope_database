from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1211.js','assets/browser-compat.v1211.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_11_compare_mobile_identity.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1211-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('identity-full-height','assets/site.v0390.css','.compare-identity-line{max-height:20rem;min-width:0}','.compare-identity-line{max-height:40px;min-width:0}')
fixture('mobile-identity-grid','assets/site.v0390.css','#contentView[data-main-view="compare"] .compare-identity-line{display:grid;grid-template-columns:minmax(0,1fr);gap:5px;align-items:start;min-width:0;max-width:100%}','#contentView[data-main-view="compare"] .compare-identity-line{display:flex;grid-template-columns:minmax(0,1fr);gap:5px;align-items:start;min-width:0;max-width:100%}')
fixture('identity-wrap','assets/site.v0390.css','#contentView[data-main-view="compare"] .compare-identity-line span{display:block;min-width:0;max-width:100%;overflow-wrap:anywhere}','#contentView[data-main-view="compare"] .compare-identity-line span{display:block;min-width:0;max-width:100%;overflow-wrap:normal}')
fixture('compact-collapse','assets/site.v0390.css','#contentView[data-main-view="compare"] .compare-workspace.is-compact .compare-identity-line{max-height:0}','#contentView[data-main-view="compare"] .compare-workspace.is-compact .compare-identity-line{max-height:20rem}')
fixture('driver-evidence','assets/app.v1211.js','<span>${esc(driver)} ${esc(dv)}</span>','<span>${esc(driver)}</span>')
fixture('filter-regression','assets/site.v0390.css','#contentView[data-main-view="compare"] .compare-filter-controls{display:grid!important;grid-template-columns:minmax(0,1fr)!important','#contentView[data-main-view="compare"] .compare-filter-controls{display:flex!important;grid-template-columns:minmax(0,1fr)!important')
fixture('version-emphasis-regression','assets/site.v0390.css','.compare-warning .compare-version-token{color:#fff;font-weight:900}','.compare-warning .compare-version-token{color:var(--muted);font-weight:400}')
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_2_11_compare_mobile_identity.py','python tools/verify_1_2_10_mobile_filters_compare_versions.py')
print('PASS 1.2.11 negative mutation suite')
