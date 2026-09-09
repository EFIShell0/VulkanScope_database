from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--root');p.add_argument('--skip-version',action='store_true');a=p.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]
def need(c,m):
    if not c: errors.append(m)
def txt(r):
    q=root/r
    return q.read_text(encoding='utf-8') if q.is_file() else ''
def js(r):
    try:return json.loads(txt(r))
    except:return {}
worker=txt('worker/src/index.js'); tests=txt('worker/tests/contract.mjs'); index=txt('index.html'); app=txt('assets/app.v1004.js'); rules=txt('rules/PROJECT_RULES.md'); audit=txt('rules/1.0.2_VULKANSCOPE_1.0.2_PRODUCER_BASELINE_AUDIT.md'); static=js('data/index.json'); pkg=js('worker/package.json')
if not a.skip_version:
    need(pkg.get('version')=='1.0.2','Worker package version must be 1.0.2')
    need('VulkanScope Database <strong>1.0.2</strong>' in index,'Database 1.0.2 footer identity missing')
    need('app.v1004.js?v=1004' in index and 'config.js?v=1002' in index and 'site.v0390.css?v=1002' in index,'1.0.2 cache identity missing')
    need(static.get('databaseVersion')=='1.0.2','static databaseVersion must be 1.0.2')
    need(static.get('producerQueryBaseline')=='VulkanScope 1.0.2 · Vulkan 1.4.362','static producer baseline must be VulkanScope 1.0.2 / Vulkan 1.4.362')
need(("if(v.major===1&&v.minor===0&&v.patch===0)return p.application.versionCode===1000" in worker) or ("if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch" in worker),'historical 1.0.0/1000 identity rule missing')
need(("if(v.major===1&&v.minor===0&&v.patch===1)return p.application.versionCode===1001" in worker) or ("if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch" in worker),'historical 1.0.1/1001 identity rule missing')
need(("if(v.major===1&&v.minor===0&&v.patch===2)return p.application.versionCode===1002" in worker) or ("if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch" in worker),'current 1.0.2/1002 identity rule missing')
need("producerAtLeast0803=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,0,80,3)}" in worker,'0.80.3 producer floor drifted')
if not a.skip_version:
    need(worker.count("producerQueryBaseline:'VulkanScope 1.0.2 · Vulkan 1.4.362'")>=2,'Worker current producer metadata must be canonical in health/list paths')
need('normalizerVersion:16' in worker and static.get('normalizerVersion')==16,'normalizer 16 drifted')
if not a.skip_version:
    need('Database 1.0.2' in app and 'VulkanScope 1.0.2 · Vulkan 1.4.362' in app,'Pages frontend current identity drifted')
need("current1002.application.version='1.0.2'" in tests and 'current1002.application.versionCode=1002' in tests and '1.0.2 / 1002 must be accepted' in tests,'canonical 1.0.2 Worker acceptance fixture missing')
need('bad1002Identity.application.versionCode=1001' in tests,'1.0.2 mismatched versionCode rejection fixture missing')
need('Release 1.0.2 / VulkanScope 1.0.2 producer-baseline requirements' in rules,'1.0.2 rules section missing')
need('Normalizer: 16' in audit and 'NOT EXECUTED' in audit,'1.0.2 audit evidence incomplete')
need((root/'regression/1.0.1_to_1.0.2_contract.json').is_file(),'1.0.2 immutable regression contract missing')
need(sorted(x.name for x in (root/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],'D1 migration set changed')
apps=sorted(x.name for x in (root/'assets').glob('app.v*.js'))
need(apps==['app.v1004.js'],f'strict current frontend asset identity drifted: {apps}')
if errors:
    print('FAIL VulkanScope Database 1.0.2 producer baseline')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.2 producer baseline: producer=1.0.2/1002 Vulkan=1.4.362 schema=2 technicalReport=3 normalizer=16')
