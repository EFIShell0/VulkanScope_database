from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_4_filter_scrollbar_compare_chevron.py'
fixtures=[
 ('filter-rail-unconditional','assets/site.v0390.css','.custom-select.open .custom-select-menu>.surface-scrollbar.is-scrollable{opacity:1;visibility:visible}', '.custom-select.open .custom-select-menu>.surface-scrollbar{opacity:1;visibility:visible}'),
 ('filter-rail-hide','assets/site.v0390.css','.custom-select.open .custom-select-menu>.surface-scrollbar:not(.is-scrollable){opacity:0!important;visibility:hidden!important;pointer-events:none!important}', '.custom-select.open .custom-select-menu>.surface-scrollbar:not(.is-scrollable){opacity:1!important;visibility:visible!important;pointer-events:auto!important}'),
 ('scroll-overflow-owner','assets/app.v1304.js',"scrollable=visible&&max>2","scrollable=visible"),
 ('chevron-path','assets/app.v1304.js',"minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'","minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'"),
 ('chevron-css-guard','assets/site.v0390.css','.compare-minimize-toggle svg{transform:none}', '.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}'),
 ('motion-regression','assets/app.v1304.js','animatePagedSurfaceIn(optionsHost,target>previousPage?1:-1)','void previousPage'),
 ('predecessor-bridge','tools/build_pages_artifact.py',"'assets/app.v1303.js'","'assets/app.v1302.js'"),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_4_filter_scrollbar_compare_chevron.py','python tools/verify_1_3_3_compare_direction_symmetric_motion.py'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb134-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}')
        p.write_text(t.replace(a,b),encoding='utf-8')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.4 negative mutation suite')
