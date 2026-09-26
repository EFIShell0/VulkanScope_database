from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
cases=[
 ('worker-floor','worker/src/index.js','const supportedProducer=p=>producerAtLeast2006(p)','const supportedProducer=p=>producerAtLeast1403(p)'),
 ('worker-floor-message','worker/src/index.js','VulkanScope 2.0.6 or newer is required for new submissions','VulkanScope 2.0.5 or newer is required for new submissions'),
 ('producer-identity','worker/src/index.js','if(v.major===2)return p.application.versionCode===2000+v.minor*100+v.patch','if(v.major===2)return true'),
 ('registry-selector','worker/src/index.js',"producerAtLeast2006(p)?'1.4.364':producerAtLeast08010(p)?'1.4.362':'1.4.361'","producerAtLeast2006(p)?'1.4.362':producerAtLeast08010(p)?'1.4.362':'1.4.361'"),
 ('device-field','report.schema.json','"googlebookEnvironmentEvidence"','"googlebookEnvironmentEvidence_REMOVED"'),
 ('schema-floor','report.schema.json','"minimum": 2006','"minimum": 2005'),
 ('frontend-baseline','assets/app.v1408.js','VulkanScope 2.0.6 · Vulkan 1.4.364','VulkanScope 2.0.5 · Vulkan 1.4.362'),
 ('static-compatible','data/index.json','VulkanScope 2.0.6+ · schema 2 / technical report 3','VulkanScope 2.0.5+ · schema 2 / technical report 3'),
 ('registry-lock','registry/registry_lock.json','"apiVersion": "1.4.364"','"apiVersion": "1.4.362"'),
]
for name,rel,old,new in cases:
    with tempfile.TemporaryDirectory(prefix='vsdb-148-neg-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture source missing for {name}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_8_vulkanscope_2_0_6_compatibility.py')],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if cp.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
with tempfile.TemporaryDirectory(prefix='vsdb-148-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
    p=dst/'SECURITY.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_8_vulkanscope_2_0_6_compatibility.py')],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if cp.returncode!=0: raise SystemExit('unrelated documentation mutation should not fail focused verifier: '+cp.stdout)
print(f'PASS Database 1.4.8 negative mutations: {len(cases)} + unrelated-control')
