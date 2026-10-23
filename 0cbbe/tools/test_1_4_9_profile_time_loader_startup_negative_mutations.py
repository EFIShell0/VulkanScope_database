from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
cases=[
 ('profile-loss','assets/app.v1409.js','v.profiles=d.profileEvaluation.map(x=>({...x','v.profiles=d.profileEvaluation.map(x=>({'),
 ('page-gap','assets/site.v1409.css','.page-scroll-controls{right:30px}', '.page-scroll-controls{right:18px}'),
 ('season-detail','assets/app.v1409.js','Seasonal offset setting','Season setting removed'),
 ('parallel-startup','assets/app.v1409.js','Promise.allSettled([snapshotPromise,livePromise])','Promise.all([snapshotPromise,livePromise])'),
 ('loader-logo','index.html','class="database-loading-logo" src="assets/vulkanscope_logo_horizontal.png"','class="database-loading-logo" src="assets/missing_logo.png"'),
]
for name,rel,old,new in cases:
    with tempfile.TemporaryDirectory(prefix='vsdb-149-neg-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture source missing for {name}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_9_profile_time_loader_startup.py'),'--root',str(dst)],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if cp.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
with tempfile.TemporaryDirectory(prefix='vsdb-149-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
    p=dst/'SECURITY.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_9_profile_time_loader_startup.py'),'--root',str(dst)],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if cp.returncode!=0: raise SystemExit('unrelated documentation mutation should not fail focused verifier: '+cp.stdout)
print(f'PASS Database 1.4.9 negative mutations: {len(cases)} + unrelated-control')
