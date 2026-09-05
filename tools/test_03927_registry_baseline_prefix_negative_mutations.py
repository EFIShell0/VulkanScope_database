from pathlib import Path
import tempfile, shutil, subprocess, sys
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_03927_registry_baseline_prefix.py'
mutations=[
    ('worker/src/index.js','baseline=`Vulkan ${registryVersion}`','baseline=registryVersion','validator-prefix-removal'),
    ('worker/tests/contract.mjs',"registryBaseline:'Vulkan 1.4.361'","registryBaseline:'1.4.361'",'legacy-fixture-prefix-removal'),
    ('worker/tests/contract.mjs',"current0810.vulkan.registryBaseline='Vulkan 1.4.362'","current0810.vulkan.registryBaseline='1.4.362'",'current-fixture-prefix-removal'),
]
for rel,a,b,name in mutations:
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/'db';shutil.copytree(root,dst)
        p=dst/rel;s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit('FAIL mutation source missing: '+name)
        p.write_text(s.replace(a,b,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),str(dst)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: '+name)
with tempfile.TemporaryDirectory() as td:
    dst=Path(td)/'db';shutil.copytree(root,dst)
    p=dst/'changelog.md';s=p.read_text(encoding='utf-8');p.write_text(s+'\n',encoding='utf-8')
    r=subprocess.run([sys.executable,str(ver),str(dst)],capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit('FAIL harmless changelog whitespace false-positive control rejected')
print('PASS Database 0.39.27 registry-baseline negative mutations and false-positive control')
