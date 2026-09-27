from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
cases=[
 ('profile-size','assets/site.v1410.css','.profile-evaluation-name{font-size:16px!important','.profile-evaluation-name{font-size:12px!important'),
 ('loader-spinner','index.html','<div class="database-loading-spinner"><span></span></div>','<div class="database-loading-spinner"></div>'),
 ('loader-overflow','assets/site.v1410.css','max-height:calc(100dvh - 24px);overflow:hidden!important','max-height:calc(100dvh - 24px);overflow:auto!important'),
 ('predecessor-visibility-gate','assets/release-bootstrap.v1409.js',"html.classList.add('release-check-pending');",""),
 ('submitted-season','assets/app.v1410.js','Year-round offset · no seasonal clock change','Season unknown'),
 ('submitted-report-row','assets/app.v1410.js','<b>Seasonal</b>','<b>Season</b>'),
 ('collapse-animation','assets/app.v1410.js',"cell.style.setProperty('width',px,'important')","cell.style.width=px"),
]
for name,rel,old,new in cases:
    with tempfile.TemporaryDirectory(prefix='vsdb-1410-neg-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture source missing for {name}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_10_profiles_loader_submitted_time.py'),'--root',str(dst)],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if cp.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
with tempfile.TemporaryDirectory(prefix='vsdb-1410-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
    p=dst/'SECURITY.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_10_profiles_loader_submitted_time.py'),'--root',str(dst)],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if cp.returncode!=0: raise SystemExit('unrelated documentation mutation should not fail focused verifier: '+cp.stdout)
print(f'PASS Database 1.4.10 negative mutations: {len(cases)} + unrelated-control')
