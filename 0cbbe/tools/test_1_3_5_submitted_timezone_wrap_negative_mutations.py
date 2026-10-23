from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_5_submitted_timezone_wrap.py'
fixtures=[
 ('zone-nowrap','assets/site.v0390.css','.submitted-stack .submitted-zone-value{white-space:normal;overflow-wrap:anywhere;word-break:normal}', '.submitted-stack .submitted-zone-value{white-space:nowrap;overflow-wrap:anywhere;word-break:normal}'),
 ('season-inline','assets/site.v0390.css','.submitted-zone-season{display:block;', '.submitted-zone-season{display:inline;'),
 ('season-helper','assets/app.v1305.js',"suffixes=['Daylight / summer offset','Standard / winter offset']","suffixes=[]"),
 ('zone-render','assets/app.v1305.js','${submittedZoneMarkup(submitted.zone)}','${esc(submitted.zone)}'),
 ('filter-regression','assets/app.v1305.js','scrollable=visible&&max>2','scrollable=visible'),
 ('compare-regression','assets/app.v1305.js',"minimized?'M6 9l6 6 6-6':'M6 15l6-6 6 6'","minimized?'M6 15l6-6 6 6':'M6 9l6 6 6-6'"),
 ('predecessor-bridge','tools/build_pages_artifact.py',"'assets/app.v1304.js'","'assets/app.v1303.js'"),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_5_submitted_timezone_wrap.py','python tools/verify_1_3_4_filter_scrollbar_compare_chevron.py'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb135-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.5 negative mutation suite')
