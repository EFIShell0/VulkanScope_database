from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_4_7_floor_metadata_coherence.py'
cases=[
 ('frontend-baseline','assets/app.v1407.js','VulkanScope 1.4.3 · Vulkan 1.4.362','VulkanScope 1.4.0 · Vulkan 1.4.362'),
 ('frontend-compatible','assets/app.v1407.js','VulkanScope 1.4.3+ · schema 2 / technical report 3','VulkanScope 1.4.0+ · schema 2 / technical report 3'),
 ('frontend-live-baseline','assets/app.v1407.js','producerQueryBaseline:CURRENT_PRODUCER_QUERY_BASELINE','producerQueryBaseline:meta?.producerQueryBaseline||CURRENT_PRODUCER_QUERY_BASELINE'),
 ('frontend-live-compatible','assets/app.v1407.js','compatibleProducer:CURRENT_COMPATIBLE_PRODUCER','compatibleProducer:meta?.compatibleProducer||CURRENT_COMPATIBLE_PRODUCER'),
 ('preload-live-compatible','tools/build_preload_snapshot.py',"'compatibleProducer': 'VulkanScope 1.4.3+ · schema 2 / technical report 3'", "'compatibleProducer': meta.get('compatibleProducer', 'VulkanScope 1.4.3+ · schema 2 / technical report 3')"),
 ('worker-floor','worker/src/index.js','const supportedProducer=p=>producerAtLeast1403(p)','const supportedProducer=p=>producerAtLeast1019(p)'),
 ('worker-message','worker/src/index.js','VulkanScope 1.4.3 or newer is required for new submissions','VulkanScope 1.4.0 or newer is required for new submissions'),
 ('static-compatible','data/index.json','VulkanScope 1.4.3+ · schema 2 / technical report 3','VulkanScope 1.4.0+ · schema 2 / technical report 3'),
]
for name,rel,old,new in cases:
    with tempfile.TemporaryDirectory(prefix='vsdb-147-neg-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture source missing for {name}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_7_floor_metadata_coherence.py')],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if cp.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
print(f'PASS Database 1.4.7 negative mutations: {len(cases)}')
