from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_1_freshness_filters_license_live_sync.py'
fixtures=[
 ('go-current','assets/app.v1301.js','go.disabled=max<=1||target===value','go.disabled=max<=1'),
 ('filter-pager','assets/app.v1301.js','pager.hidden=!searchable','pager.hidden=matches.length<=CUSTOM_SELECT_OPTION_LIMIT'),
 ('inline-license','assets/app.v1301.js',"button.addEventListener('click',()=>openLicenseViewer(button.dataset.licenseFile,button.dataset.licenseName))","button.addEventListener('click',()=>void 0)"),
 ('freshness','assets/release-bootstrap.v1301.js',"cache:'no-store'","cache:'default'"),
 ('notice','index.html','VulkanScope is not affiliated with the Khronos Group','VulkanScope project notice'),
 ('live-toast','assets/app.v1301.js','showNewReportNotification(result.added)','void 0'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb131-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.1 negative mutation suite')
