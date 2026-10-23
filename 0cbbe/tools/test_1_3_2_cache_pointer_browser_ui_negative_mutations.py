from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_2_cache_pointer_browser_ui.py'
fixtures=[
 ('freshness-retry','assets/release-bootstrap.v1302.js','setInterval(()=>void check(),STEADY_RETRY)','setInterval(()=>void 0,STEADY_RETRY)'),
 ('runtime-auto-update','assets/app.v1302.js','navigateToPublishedRelease(remote)','showPublishedDatabaseUpdate(remote)'),
 ('filter-internal-click','assets/app.v1302.js',"e.target.closest('.custom-select')","e.target.closest('.never-custom-select')"),
 ('rail-pointer','assets/site.v0390.css','.viewport-scrollbar.is-scrollable,.surface-scrollbar.is-scrollable{pointer-events:none!important}', '.viewport-scrollbar.is-scrollable,.surface-scrollbar.is-scrollable{pointer-events:auto!important}'),
 ('pager-width','assets/site.v0390.css','grid-template-columns:36px minmax(0,1fr) 36px!important','grid-template-columns:minmax(0,1fr) minmax(118px,auto) minmax(0,1fr)!important'),
 ('browser-scope','assets/app.v1302.js',"['Samsung Internet',/SamsungBrowser","['Samsung Browser',/SamsungBrowser"),
 ('info-notice','assets/site.v0390.css','color:#b9d2ff!important','color:var(--accent)!important'),
 ('predecessor-bridge','tools/build_pages_artifact.py',"'assets/app.v1301.js'","'assets/app.v1299.js'"),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb132-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.2 negative mutation suite')
