from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_3_compare_direction_symmetric_motion.py'
fixtures=[
 ('chevron-path','assets/app.v1303.js',"minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'","minimized?'M6 9l6 6 6-6':'M6 9l6 6 6-6'"),
 ('chevron-css-guard','assets/site.v0390.css','.compare-minimize-toggle svg{transform:none}', '.compare-workspace.is-minimized .compare-minimize-toggle svg{transform:rotate(180deg)}'),
 ('filter-page-motion','assets/app.v1303.js','animatePagedSurfaceIn(optionsHost,target>previousPage?1:-1)','void previousPage'),
 ('modal-page-motion','assets/app.v1303.js','animatePagedSurfaceIn(list,direction)','void direction'),
 ('license-open-motion','assets/app.v1303.js',"dialog.classList.add('open')","dialog.classList.add('never-open')"),
 ('license-stale-close','assets/app.v1303.js','if(token!==licenseViewerMotionToken||dialog.classList.contains(\'open\'))return','if(dialog.classList.contains(\'open\'))return'),
 ('reduced-motion','assets/site.v0390.css','@media(prefers-reduced-motion:reduce){.license-viewer-backdrop,.license-viewer-dialog{transition:none!important}','@media(prefers-reduced-motion:reduce){.license-viewer-backdrop{transition:none!important}'),
 ('predecessor-bridge','tools/build_pages_artifact.py',"'assets/app.v1302.js'","'assets/app.v1301.js'"),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_3_compare_direction_symmetric_motion.py','python tools/verify_1_3_2_cache_pointer_browser_ui.py'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb133-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        # Keep canonical workflow equality from masking the intended workflow fixture.
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.3 negative mutation suite')
