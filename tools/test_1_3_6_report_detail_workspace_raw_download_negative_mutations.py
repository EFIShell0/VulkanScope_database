from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_6_report_detail_workspace_raw_download.py'
fixtures=[
 ('overview-redesign','assets/app.v1306.js','<div class="detail-overview-grid">','<div class="detail-section-intro">'),
 ('memory-workspace','assets/app.v1306.js',"detailWorkspace('memory'","detailWorkspace('memory-old'"),
 ('raw-source','assets/app.v1306.js',"function downloadRawReport(r,button){const text=String(r?.reportText??'')","function downloadRawReport(r,button){const text=String(r?.reportText??'')+'\\n'"),
 ('raw-blob','assets/app.v1306.js',"new Blob([text],{type:'text/plain;charset=utf-8'})","new Blob([text+'\\n'],{type:'text/plain;charset=utf-8'})"),
 ('raw-scroll-selector','assets/app.v1306.js',',.raw-report-scroll\';',"';"),
 ('raw-scroll-css','assets/site.v0390.css','.raw-report-scroll.surface-scroll-host{padding-right:0}', '.raw-report-scroll.legacy-scroll{padding-right:0}'),
 ('mobile-detail','assets/site.v0390.css','@media(max-width:760px){.detail-section-intro','@media(max-width:760px){.detail-section-intro-broken'),
 ('timezone-regression','assets/site.v0390.css','.submitted-stack .submitted-zone-value{white-space:normal','.submitted-stack .submitted-zone-value{white-space:nowrap'),
 ('compare-regression','assets/app.v1306.js',"minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'","minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'"),
 ('predecessor-bridge','tools/build_pages_artifact.py',"'assets/app.v1305.js'","'assets/app.v1304.js'"),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_6_report_detail_workspace_raw_download.py','python tools/verify_1_3_5_submitted_timezone_wrap.py'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb136-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}: {a!r}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.6 negative mutation suite')
