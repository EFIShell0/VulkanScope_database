from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_4_6_submission_floor.py'
required=[
    'index.html','assets/app.v1406.js','assets/site.v1406.css','worker/src/index.js','worker/tests/contract.mjs',
    'rules/PROJECT_RULES.md','data/release.json','data/index.json','tools/repair_repository.py','tools/build_pages_artifact.py'
]
cases=[
    ('lower-floor','worker/src/index.js','versionAtLeast(v,1,4,3)','versionAtLeast(v,1,4,2)'),
    ('stale-supported-owner','worker/src/index.js','const supportedProducer=p=>producerAtLeast1403(p)','const supportedProducer=p=>versionAtLeast(producerVersion(p),1,4,0)'),
    ('stale-floor-message','worker/src/index.js','VulkanScope 1.4.3 or newer is required for new submissions','VulkanScope 1.4.0 or newer is required for new submissions'),
    ('stale-worker-baseline','worker/src/index.js','VulkanScope 1.4.3 · Vulkan 1.4.362','VulkanScope 1.4.0 · Vulkan 1.4.362'),
    ('boundary-fixture','worker/tests/contract.mjs',"below.application.version='1.4.2'","below.application.version='1.4.3'"),
    ('static-baseline','data/index.json','VulkanScope 1.4.3+ · schema 2 / technical report 3','VulkanScope 1.4.0+ · schema 2 / technical report 3'),
    ('release-marker','data/release.json','"databaseVersion":"1.4.6"','"databaseVersion":"1.4.5"'),
    ('predecessor-bridge','tools/repair_repository.py',"PREDECESSOR_BRIDGE = {'app.v1405.js','browser-compat.v1405.js','release-bootstrap.v1405.js'}","PREDECESSOR_BRIDGE = {'app.v1404.js','browser-compat.v1404.js','release-bootstrap.v1404.js'}"),
]

temps=[]; procs=[]
try:
    for name,rel,old,new in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-146-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'
        for src_rel in required:
            src=root/src_rel; out=dst/src_rel; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,out)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'negative fixture token missing for {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        procs.append((name,subprocess.Popen([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)))
    for name,proc in procs:
        out,err=proc.communicate()
        if proc.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{out}{err}')
finally:
    for td in temps: td.cleanup()
print(f'PASS Database 1.4.6 negative mutations: {len(cases)} expected failures')
