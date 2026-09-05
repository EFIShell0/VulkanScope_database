from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_vulkan_1_4_362_03924.py'
mutations=[
('registry/registry_lock.json','"registryRef": "1.4.362"','"registryRef": "1.4.361"','registry-ref-drift'),
('worker/src/index.js',"producerAtLeast08010(p)?'1.4.362':'1.4.361'","producerAtLeast08010(p)?'1.4.361':'1.4.361'",'producer-registry-contract-drift'),
('assets/encyclopedia.v03924.js','"tokens":6248','"tokens":6247','encyclopedia-census-drift'),
('tools/generate_encyclopedia_03924.py',"'extensions':476","'extensions':475",'generator-census-drift')]
for rel,a,b,name in mutations:
    with tempfile.TemporaryDirectory(prefix='db03924-mut-') as d:
        dst=Path(d)/'root';shutil.copytree(root,dst)
        p=dst/rel;s=p.read_text(encoding='utf-8')
        if a not in s:raise SystemExit('FAIL mutation source absent '+name)
        p.write_text(s.replace(a,b),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst),'--skip-version'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0:raise SystemExit('FAIL mutation accepted '+name)
with tempfile.TemporaryDirectory(prefix='db03924-fp-') as d:
    dst=Path(d)/'root';shutil.copytree(root,dst)
    p=dst/'changelog.md';s=p.read_text(encoding='utf-8')
    needle='VulkanScope Database 0.39.25'
    if needle not in s:raise SystemExit('FAIL false-positive source absent')
    p.write_text(s.replace(needle,needle+' ',1),encoding='utf-8')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst),'--skip-version'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if r.returncode!=0:raise SystemExit('FAIL false-positive wording mutation rejected')
print('PASS Database 0.39.25 Vulkan 1.4.362 negative mutations and false-positive control')
