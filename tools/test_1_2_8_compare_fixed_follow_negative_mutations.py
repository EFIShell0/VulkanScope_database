from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1208.js','assets/browser-compat.v1208.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_8_compare_fixed_follow.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-128-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('compare-placeholder','assets/app.v1208.js','id="compareStickyPlaceholder" class="compare-sticky-placeholder"','id="compareStickyPlaceholderMissing" class="compare-placeholder-missing"')
fixture('compare-fixed-position','assets/app.v1208.js',"shell.style.position='fixed'","shell.style.position='relative'")
fixture('compare-flow-height','assets/app.v1208.js','placeholder.style.height=`${compareStickyFlowHeight}px`',"placeholder.style.height='0px'")
fixture('compare-live-width','assets/app.v1208.js','const pageRect=page.getBoundingClientRect()','const pageRect={left:0,width:320}')
fixture('compare-rail-reserve','assets/app.v1208.js',"rightReserve=$('#viewportScrollbar')?.classList.contains('is-scrollable')?20:4","rightReserve=0")
fixture('compare-css-fixed','assets/site.v0390.css','.compare-sticky-shell.is-pinned{position:fixed','.compare-sticky-shell.is-pinned{position:sticky')
fixture('compare-select-elevation','assets/site.v0390.css','.compare-sticky-shell.is-pinned .custom-select-menu{z-index:460','.compare-sticky-shell.is-pinned .custom-select-menu{z-index:4')
fixture('stale-workflow','tools/pages.workflow.yml','python tools/verify_1_2_8_compare_fixed_follow.py','python tools/verify_1_2_7_compare_hero_scroll.py')
print('PASS 1.2.8 negative mutation suite')
