#!/usr/bin/env python3
import shutil,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];ver=root/'tools/verify_0808_floor_loading_scroll.py'
mut=[
('worker/src/index.js','v.minor>80||v.minor===80&&v.patch>=3','v.minor>32||v.minor===32&&v.patch>=4','producer-floor'),
('assets/app.v03925.js','VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU','Integrated GPU','canonical-type'),
('index.html','id="databaseLoading"','id="databaseLoadingRemoved"','loading-surface'),
('index.html','id="pageScrollDown"','id="pageScrollDownRemoved"','scroll-control')]
for rel,a,b,name in mut:
  with tempfile.TemporaryDirectory(prefix='vsdb3922-mut-') as d:
    dst=Path(d)/'root';shutil.copytree(root,dst);p=dst/rel;s=p.read_text(encoding='utf-8')
    if a not in s:raise SystemExit('FAIL mutation source absent '+name)
    p.write_text(s.replace(a,b,1),encoding='utf-8')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if r.returncode==0:raise SystemExit('FAIL mutation accepted '+name)
print('PASS Database 0.39.23 negative mutations')
