#!/usr/bin/env python3
import shutil,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];ver=root/'tools/verify_0809_floor_encyclopedia.py'
mut=[
('worker/src/index.js','v.patch>=3','v.patch>=1','producer-floor'),
('assets/app.v03926.js',"['encyclopedia','Encyclopedia']","['encyclopediaRemoved','Encyclopedia']",'encyclopedia-route'),
('assets/app.v03926.js','Registry/reference presence is not runtime capability evidence.','Registry reference proves runtime capability.','evidence-separation'),
('assets/encyclopedia.v03924.js','"commands":842','"commands":841','locked-census')]
for rel,a,b,name in mut:
    with tempfile.TemporaryDirectory(prefix='vsdb3923-mut-') as d:
        dst=Path(d)/'root';shutil.copytree(root,dst);p=dst/rel;s=p.read_text(encoding='utf-8')
        if a not in s:raise SystemExit('FAIL mutation source absent '+name)
        p.write_text(s.replace(a,b) if name=='evidence-separation' else s.replace(a,b,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0:raise SystemExit('FAIL mutation accepted '+name)
with tempfile.TemporaryDirectory(prefix='vsdb3923-fp-') as d:
    dst=Path(d)/'root';shutil.copytree(root,dst);p=dst/'assets/site.v0390.css';s=p.read_text(encoding='utf-8')
    p.write_text(s+'\n',encoding='utf-8')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if r.returncode!=0:raise SystemExit('FAIL false-positive harmless CSS whitespace rejected')
print('PASS Database 0.39.25 floor/Encyclopedia negative mutations and false-positive control')
