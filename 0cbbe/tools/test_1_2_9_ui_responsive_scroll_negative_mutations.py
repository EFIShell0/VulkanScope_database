from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1209.js','assets/browser-compat.v1209.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_9_ui_responsive_scroll.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-129-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('browser-gate-flash','index.html','role="main" hidden><div class="browser-compatibility-card"','role="main"><div class="browser-compatibility-card"')
fixture('reports-family-bypass','assets/app.v1209.js',"if(state.view==='encyclopedia')return;","if(state.view==='reports'||state.view==='encyclopedia')return;")
fixture('reports-mobile-column','assets/site.v0390.css','#contentView[data-main-view="reports"] #filters{display:grid;grid-template-columns:minmax(0,1fr)','#contentView[data-main-view="reports"] #filters{display:flex;grid-template-columns:minmax(0,1fr)')
fixture('compare-minimize-reset','assets/app.v1209.js',"workspace.classList.remove('is-compact','is-minimized')","workspace.classList.remove('is-compact')")
fixture('compare-mobile-width','assets/app.v1209.js','maxWidth=Math.max(1,viewportWidth-left-rightReserve)','maxWidth=Math.max(260,viewportWidth-left-rightReserve)')
fixture('compare-mini-identity','assets/app.v1209.js',"miniA.textContent=a.gpu?.name||'Unknown'","miniA.textContent='GPU A'")
fixture('local-scroll-surfaces','assets/app.v1209.js',".settings-drawer-body,.custom-select-menu,.coverage-report-dialog-body,.modal-paged-list",".settings-drawer-body,.custom-select-menu")
fixture('local-scroll-host-state','assets/app.v1209.js','host?.scrollHeight','document.documentElement.scrollHeight')
fixture('local-scroll-visual-parity','assets/app.v1209.js','viewport-scrollbar-thumb surface-scrollbar-thumb','surface-scrollbar-thumb')
fixture('stale-workflow','tools/pages.workflow.yml','python tools/verify_1_2_9_ui_responsive_scroll.py','python tools/verify_1_2_8_compare_fixed_follow.py')
fixture('overlay-browser-compat-cleanup','tools/repair_repository.py','for p in stale_browser_compats():','for p in []:')
print('PASS 1.2.9 negative mutation suite')
