from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
cases=[
 ('worker-floor','worker/src/index.js','const supportedProducer=p=>producerAtLeast3012(p)','const supportedProducer=p=>producerAtLeast3002(p)'),
 ('worker-floor-message','worker/src/index.js','VulkanScope 3.0.12 or newer is required for new submissions','VulkanScope 3.0.11 or newer is required for new submissions'),
 ('snapshot-background','worker/src/index.js','ctx?.waitUntil','false&&ctx?.waitUntil'),
 ('snapshot-new-row-only','worker/src/index.js','if(inserted&&ctx?.waitUntil)','if(ctx?.waitUntil)'),
 ('schema-floor','report.schema.json','"minimum": 3012','"minimum": 3002'),
 ('frontend-baseline','assets/app.v1412.js','VulkanScope 3.0.12 · Vulkan 1.4.364','VulkanScope 3.0.2 · Vulkan 1.4.364'),
 ('snapshot-workflow','tools/pages.workflow.yml','snapshot-refresh:','snapshot-refresh-disabled:'),
 ('snapshot-freshness-gate','tools/pages.workflow.yml','--expect-report-id "$REPORT_ID"',''),
 ('pages-deploy-serialization','tools/pages.workflow.yml','group: vulkanscope-database-pages-deployment','group: vulkanscope-database-release-only',),
 ('token-secret-boundary','worker/wrangler.jsonc','"SNAPSHOT_GITHUB_REF": "main"','"SNAPSHOT_GITHUB_REF": "main",\n    "SNAPSHOT_GITHUB_TOKEN": "committed-secret"'),
]
for name,rel,old,new in cases:
    with tempfile.TemporaryDirectory(prefix='vsdb-1412-neg-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','dist','_site','node_modules','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture source missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        cp=subprocess.run([sys.executable,str(dst/'tools/verify_1_4_12_vulkanscope_3_0_12_snapshot.py')],cwd=dst,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if cp.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
print(f'PASS Database 1.4.12 negative mutations: {len(cases)}')
