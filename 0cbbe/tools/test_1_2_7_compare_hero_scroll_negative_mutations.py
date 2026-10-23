from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1207.js','assets/browser-compat.v1207.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_7_compare_hero_scroll.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-127-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('compare-sticky-shell','assets/app.v1207.js','id="compareStickyShell" class="compare-sticky-shell"','id="compareStickyShellMissing" class="compare-shell-missing"')
fixture('compare-select-elevation','assets/app.v1207.js',"wrap.closest('.compare-report-card')?.classList.add('select-open')","void 0")
fixture('bottom-gray-state','assets/site.v0390.css','.viewport-scrollbar.at-bottom .viewport-scrollbar-down,.viewport-scrollbar[data-endpoint="bottom"] .viewport-scrollbar-down,.viewport-scrollbar-down:disabled{color:#66636a!important;background:#0d0b0c!important;opacity:.72!important;filter:grayscale(1) saturate(0)!important;cursor:default!important}', '.viewport-scrollbar.at-bottom .viewport-scrollbar-down{color:#ff5c66!important}')
fixture('thumb-default-cursor','assets/site.v0390.css','.viewport-scrollbar-thumb,.viewport-scrollbar-thumb:hover,.viewport-scrollbar.is-dragging .viewport-scrollbar-thumb{cursor:default!important}', '.viewport-scrollbar-thumb{cursor:grab!important}')
fixture('scrolling-endpoint-metrics','assets/app.v1207.js','remaining=Math.max(0,max-y)','remaining=999')
fixture('adaptive-hero','index.html','id="databaseHero"','id="databaseHeroMissing"')
fixture('hero-meta-binding','assets/app.v1207.js','hero.dataset.workspace=state.view','hero.dataset.workspace="reports"')
fixture('row-synchronous-hover','assets/site.v0390.css','.reports-table .click-row{--report-row-surface:transparent}', '.reports-table .click-row{--broken-report-row:transparent}')
fixture('stale-workflow','tools/pages.workflow.yml','python tools/verify_1_2_7_compare_hero_scroll.py','python tools/verify_1_2_6_cross_browser_detail.py')
print('PASS 1.2.7 negative mutation suite')
