from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1205.js','assets/browser-compat.v1205.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_5_scrollbar_motion.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-125-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('literal-escaped-newline','assets/site.v0390.css','/* VulkanScope Database 1.2.5','\\n/* VulkanScope Database 1.2.5')
fixture('body-top-state','assets/app.v1205.js',"document.body?.classList.toggle('at-page-top',atTop)","void atTop")
fixture('top-gray-arrow','assets/site.v0390.css','html.at-page-top::-webkit-scrollbar-button:vertical:decrement','html.no-top-state::-webkit-scrollbar-button:vertical:decrement')
fixture('bottom-red-arrow','assets/site.v0390.css','html.at-page-bottom::-webkit-scrollbar-button:vertical:increment','html.no-bottom-state::-webkit-scrollbar-button:vertical:increment')
fixture('table-motion','assets/site.v0390.css','.table-wrap tbody tr,.table-wrap tbody td{transition:','.table-wrap tbody tr,.table-wrap tbody td{animation:')
fixture('confirm-close-motion','assets/app.v1205.js','const animations=[dialog.animate','const animations=[dialog.noAnimate')
fixture('bounded-table','assets/app.v1205.js',"boundedReportTable('devices-main'","table(['Device'")
fixture('stale-workflow','tools/pages.workflow.yml','python tools/verify_1_2_5_scrollbar_motion.py','python tools/verify_1_2_4_ci_bounded_tables.py')
print('PASS 1.2.5 negative mutation suite')
