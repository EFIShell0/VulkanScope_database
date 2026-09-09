from pathlib import Path
import argparse,json,re
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
worker=txt('worker/src/index.js'); tests=txt('worker/tests/contract.mjs'); index=txt('index.html'); app=txt('assets/app.v1004.js'); rules=txt('rules/PROJECT_RULES.md'); audit=txt('rules/1.0.1_FULL_SECURITY_SPEC_CORRECTNESS_USABILITY_AUDIT.md'); static=js('data/index.json'); pkg=js('worker/package.json')
if not a.skip_version:
    need(pkg.get('version') in {'1.0.1','1.0.2'},'Worker package version must preserve 1.0.1+ retained compatibility')
    need(('VulkanScope Database <strong>1.0.1</strong>' in index) or ('VulkanScope Database <strong>1.0.2</strong>' in index),'retained footer identity missing')
    need((('app.v1004.js?v=1001' in index and 'config.js?v=1001' in index) or ('app.v1004.js?v=1004' in index and 'config.js?v=1002' in index)),'retained cache identity missing')
    need(static.get('databaseVersion') in {'1.0.1','1.0.2'},'static databaseVersion must preserve retained 1.0.1+ identity')
    need(static.get('producerQueryBaseline') in {'VulkanScope 1.0.1 · Vulkan 1.4.362','VulkanScope 1.0.2 · Vulkan 1.4.362'},'static current producer baseline drifted')
need(("if(v.major===1&&v.minor===0&&v.patch===0)return p.application.versionCode===1000" in worker) or ("if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch" in worker),'historical 1.0.0/1000 identity rule missing')
need(("if(v.major===1&&v.minor===0&&v.patch===1)return p.application.versionCode===1001" in worker) or ("if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch" in worker),'current 1.0.1/1001 identity rule missing')
need("producerAtLeast0803=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,0,80,3)}" in worker,'0.80.3 producer floor drifted')
need("producerQueryBaseline:'VulkanScope 1.0." in worker and "· Vulkan 1.4.362'" in worker,'Worker health/list current 1.0.x producer metadata drifted')
need('normalizerVersion:16' in worker and static.get('normalizerVersion')==16,'normalizer 16 drifted')
need("const surfaceQueryState=" in worker and "const surfaceAvailableState=" in worker and "const surfacePresentationState=" in worker,'Worker Surface evidence helpers missing')
need("if(a){surface.available=a[1].toLowerCase()==='true';surface.presentationSupported=a[2].toLowerCase()==='true';continue}" in worker,'Surface Boolean parse must defer evidence classification')
need("syncSurfaceEvidence('Available'" in worker and "syncSurfaceEvidence('Presentation supported'" in worker,'post-parse Surface evidence synchronization missing')
need("q==='available'?'unsupported'" in worker,'false presentation may be Unsupported only after available query')
need("const av=surfaceAvailableState(s),pr=surfacePresentationState(s),diag=" in app,'Pages Surface renderer must use query-aware state helpers')
need("s.presentationSupported?'supported':'unsupported'" not in app[app.find("if(t==='surface')"):app.find("if(t==='display')") if app.find("if(t==='display')")>0 else None],'Pages Surface renderer still has direct Boolean-only presentation classification')
need("current1001.application.version='1.0.1'" in tests and 'current1001.application.versionCode=1001' in tests and '1.0.1 / 1001 must be accepted' in tests,'canonical 1.0.1 Worker acceptance fixture missing')
need("current1000.application.version='1.0.0'" in tests and 'current1000.application.versionCode=1000' in tests,'historical 1.0.0 fixture missing')
need('Release 1.0.1 full security, specification, correctness and Surface evidence requirements' in rules,'1.0.1 rules section missing')
need('Surface evidence-state' in audit or 'Surface evidence' in audit,'1.0.1 audit missing Surface semantics')
need((root/'regression/1.0.0_to_1.0.1_contract.json').is_file(),'1.0.1 immutable regression contract missing')
need(sorted(x.name for x in (root/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],'D1 migration set changed')
if errors:
    print('FAIL VulkanScope Database 1.0.1 full audit')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.1 full security/spec/correctness/Surface-evidence contract')
