from pathlib import Path
import tempfile, shutil, subprocess, sys
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_0_0_producer_baseline.py'
mutations=[
 ('worker/src/index.js',"/^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)$/","/^0\\.([1-9]\\d*)\\.(0|[1-9]\\d*)$/",'major-version-parser-regression'),
 ('worker/src/index.js','p.application.versionCode===1000','p.application.versionCode===816','current-versioncode-identity'),
 ('worker/src/index.js',"producerQueryBaseline:'VulkanScope 1.0.0 · Vulkan 1.4.362'","producerQueryBaseline:'VulkanScope 0.80.12 · Vulkan 1.4.362'",'current-producer-metadata'),
 ('worker/src/index.js','baseline=`Vulkan ${registryVersion}`','baseline=registryVersion','registry-prefix-contract'),
 ('index.html','app.v1000.js?v=1000','app.v03927.js?v=03927','frontend-release-identity'),
]
for rel,a,b,name in mutations:
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/'db';shutil.copytree(root,dst)
        p=dst/rel;s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit('FAIL mutation source missing: '+name)
        p.write_text(s.replace(a,b),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: '+name)
with tempfile.TemporaryDirectory() as td:
    dst=Path(td)/'db';shutil.copytree(root,dst)
    p=dst/'changelog.md';p.write_text(p.read_text(encoding='utf-8')+'\nRelease-note wording only.\n',encoding='utf-8')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit('FAIL unrelated wording false-positive control rejected\n'+r.stdout+r.stderr)
print('PASS VulkanScope Database 1.0.0 producer-baseline negative mutations and false-positive control')
