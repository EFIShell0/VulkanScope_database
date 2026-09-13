from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1206.js','assets/browser-compat.v1206.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_6_cross_browser_detail.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-126-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('custom-scrollbar-markup','index.html','id="viewportScrollbar"','id="viewportScrollbarMissing"')
fixture('top-gray-state','assets/site.v0390.css','.viewport-scrollbar.at-top .viewport-scrollbar-up','.viewport-scrollbar.no-top .viewport-scrollbar-up')
fixture('bottom-red-state','assets/site.v0390.css','.viewport-scrollbar.at-bottom .viewport-scrollbar-down','.viewport-scrollbar.no-bottom .viewport-scrollbar-down')
fixture('thumb-drag','assets/app.v1206.js',"thumb.addEventListener('pointerdown'","thumb.noPointerDown('")
fixture('thumb-keyboard','assets/app.v1206.js',"thumb.addEventListener('keydown'","thumb.noKeydown('")
fixture('full-report-id','assets/app.v1206.js','full 64 hexadecimal characters','truncated report identity')
fixture('detail-overview','assets/app.v1206.js','detail-overview-grid','detail-overview-missing')
fixture('stale-workflow','tools/pages.workflow.yml','python tools/verify_1_2_6_cross_browser_detail.py','python tools/verify_1_2_5_scrollbar_motion.py')
print('PASS 1.2.6 negative mutation suite')
