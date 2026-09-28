from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
cases=[
 ('worker-floor','worker/src/index.js','const supportedProducer=p=>producerAtLeast3002(p)','const supportedProducer=p=>producerAtLeast2006(p)'),
 ('worker-floor-message','worker/src/index.js','VulkanScope 3.0.2 or newer is required for new submissions','VulkanScope 3.0.1 or newer is required for new submissions'),
 ('producer-identity','worker/src/index.js','if(v.major===3)return p.application.versionCode===3000+v.minor*100+v.patch','if(v.major===3)return true'),
 ('schema-floor','report.schema.json','"minimum": 3002','"minimum": 3001'),
 ('schema-semver','report.schema.json','^3\\\\.(?:0\\\\.(?:[2-9]|[1-9][0-9]+)|[1-9][0-9]*\\\\.[0-9]+)$','^3\\\\.(?:0\\\\.(?:[1-9]|[1-9][0-9]+)|[1-9][0-9]*\\\\.[0-9]+)$'),
 ('frontend-baseline','assets/app.v1411.js','VulkanScope 3.0.2 · Vulkan 1.4.364','VulkanScope 3.0.1 · Vulkan 1.4.364'),
 ('static-compatible','data/index.json','VulkanScope 3.0.2+ · schema 2 / technical report 3','VulkanScope 3.0.1+ · schema 2 / technical report 3'),
 ('encyclopedia-producer','registry/encyclopedia_curated.json','"appVersion": "3.0.2"','"appVersion": "2.0.6"'),
 ('registry-lock','registry/registry_lock.json','"apiVersion": "1.4.364"','"apiVersion": "1.4.362"'),
]
for name,rel,old,new in cases:
    with tempfile.TemporaryDirectory(prefix='vsdb-1411-neg-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture source missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_11_vulkanscope_3_0_2_compatibility.py')],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if cp.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
with tempfile.TemporaryDirectory(prefix='vsdb-1411-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
    p=dst/'SECURITY.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_11_vulkanscope_3_0_2_compatibility.py')],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if cp.returncode!=0: raise SystemExit('unrelated documentation mutation should not fail focused verifier: '+cp.stdout)
print(f'PASS Database 1.4.11 negative mutations: {len(cases)} + unrelated-control')
