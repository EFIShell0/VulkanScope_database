from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_4_0_submission_settings_ip_filter_boot.py'
required=['index.html','assets/app.v1400.js','assets/site.v1400.css','worker/src/index.js','rules/PROJECT_RULES.md','data/release.json']
cases=[
 ('floor','worker/src/index.js','versionAtLeast(v,1,4,0)','versionAtLeast(v,1,3,13)'),
 ('settings-order','index.html','data-settings-category="favorites"','data-settings-category="favorites-broken"'),
 ('mosaic-state','assets/app.v1400.js','const networkAddressReveal={ipv4:false,ipv6:false};','const networkAddressReveal={ipv4:true,ipv6:false};'),
 ('mosaic-css','assets/site.v1400.css','.network-address-toggle.is-masked .network-address-text','.network-address-toggle.was-masked .network-address-text'),
 ('startup-filters','index.html','<div class="filters" id="filters" hidden>','<div class="filters" id="filters">'),
 ('release-marker','data/release.json','"databaseVersion":"1.4.0"','"databaseVersion":"1.3.10"'),
]
temps=[]; procs=[]
try:
    for name,rel,old,new in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-1400-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'
        for src_rel in required:
            src=root/src_rel; out=dst/src_rel; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'negative fixture token missing for {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        procs.append((name,subprocess.Popen([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)))
    for name,proc in procs:
        out,err=proc.communicate()
        if proc.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{out}{err}')
finally:
    for td in temps: td.cleanup()
print(f'PASS Database 1.4.0 negative mutations: {len(cases)} expected failures')
